"""Uji skill CUSTOM: load flow (pandapower), Modbus TCP (pymodbus), dan utilitas industri/finansial.

Nilai harapan dihitung manual di docstring tiap test.
"""

import json
import os
import subprocess
import sys
import tempfile
import time
import unittest

from _helpers import LIBRARY_ROOT

SK = os.path.join(LIBRARY_ROOT, "skills")
LOADFLOW = os.path.join(SK, "engineering", "load-flow-pandapower", "scripts", "load_flow.py")
MODBUS = os.path.join(SK, "automation", "modbus-tcp-client", "scripts", "modbus_client.py")
COOLING = os.path.join(SK, "industrial-utility", "cooling-tower-performance", "scripts", "cooling_tower.py")
BOILER = os.path.join(SK, "industrial-utility", "boiler-efficiency-indirect", "scripts", "boiler_efficiency.py")
RO = os.path.join(SK, "industrial-utility", "ro-mass-balance", "scripts", "ro_mass_balance.py")
SAVINGS = os.path.join(SK, "finance", "compound-savings-projection", "scripts", "savings_projection.py")

sys.path.insert(0, os.path.dirname(COOLING))
sys.path.insert(0, os.path.dirname(BOILER))
sys.path.insert(0, os.path.dirname(RO))
sys.path.insert(0, os.path.dirname(SAVINGS))
sys.path.insert(0, os.path.dirname(MODBUS))
sys.path.insert(0, os.path.dirname(LOADFLOW))


def _has(module):
    try:
        __import__(module)
        return True
    except ImportError:
        return False


class LoadFlowTests(unittest.TestCase):
    @unittest.skipUnless(_has("pandapower"), "butuh pandapower")
    def test_balance_and_voltage_drop(self):
        """Dua bus 20 kV, saluran 2 km, beban 2 MW + 0.8 Mvar.
        Harapan: konvergen; V_load < 1.0 pu; neraca daya tertutup (error < 1e-4 MW)."""
        import load_flow

        spec = {
            "base_kv": 20,
            "ext_grid": {"bus": 0, "vm_pu": 1.0},
            "buses": [{"index": 0, "vn_kv": 20}, {"index": 1, "vn_kv": 20}],
            "lines": [{"from": 0, "to": 1, "length_km": 2.0, "r_ohm_per_km": 0.3, "x_ohm_per_km": 0.35}],
            "loads": [{"bus": 1, "p_mw": 2.0, "q_mvar": 0.8}],
        }
        r = load_flow.solve(spec)
        self.assertTrue(r["converged"])
        self.assertLess(r["bus_vm_pu"][1], 1.0)
        self.assertGreater(r["line_losses_p_mw"], 0)
        self.assertLess(abs(r["power_balance_error_mw"]), 1e-4)
        self.assertAlmostEqual(r["slack_p_mw"], r["load_p_mw"] + r["line_losses_p_mw"], places=4)

    @unittest.skipUnless(_has("pandapower"), "butuh pandapower")
    def test_no_load_gives_flat_profile(self):
        import load_flow

        spec = {
            "ext_grid": {"bus": 0, "vm_pu": 1.0},
            "buses": [{"index": 0, "vn_kv": 20}, {"index": 1, "vn_kv": 20}],
            "lines": [{"from": 0, "to": 1, "length_km": 2.0, "r_ohm_per_km": 0.3, "x_ohm_per_km": 0.35}],
            "loads": [],
        }
        r = load_flow.solve(spec)
        self.assertAlmostEqual(r["bus_vm_pu"][1], 1.0, places=5)

    @unittest.skipUnless(_has("pandapower"), "butuh pandapower")
    def test_cli_error_on_bad_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "bad.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump({"buses": []}, fh)
            r = subprocess.run([sys.executable, LOADFLOW, path], capture_output=True, text=True)
            self.assertEqual(r.returncode, 2)


class ModbusTests(unittest.TestCase):
    """Jalankan server Modbus TCP lokal (subprocess) lalu baca/tulis register lewat klien skill."""

    # pymodbus 3.16: ModbusSequentialDataBlock(1, values) -> alamat protokol = indeks list (terverifikasi).
    # Start 0 tidak dipakai karena memicu SimData(address-1) yang gagal validasi.
    SERVER = r'''
import sys
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusDeviceContext, ModbusServerContext
port = int(sys.argv[1])
block = ModbusSequentialDataBlock(1, [375, 0xFFF6] + [0] * 98)  # addr0=375, addr1=-10 (two's complement)
ctx = ModbusServerContext(devices={1: ModbusDeviceContext(hr=block)}, single=False)
StartTcpServer(ctx, address=("127.0.0.1", port))
'''

    @unittest.skipUnless(_has("pymodbus"), "butuh pymodbus")
    def test_read_write_and_scaling(self):
        import socket

        import modbus_client

        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]
        with tempfile.TemporaryDirectory() as tmp:
            srv_path = os.path.join(tmp, "server.py")
            with open(srv_path, "w", encoding="utf-8") as fh:
                fh.write(self.SERVER)
            proc = subprocess.Popen([sys.executable, srv_path, str(port)],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            try:
                from pymodbus.client import ModbusTcpClient

                client = ModbusTcpClient("127.0.0.1", port=port, timeout=3)
                deadline = time.time() + 20
                while not client.connect():
                    if time.time() > deadline or proc.poll() is not None:
                        self.fail(f"server tidak siap: {proc.stderr.read().decode(errors='replace')[-400:]}")
                    time.sleep(0.2)
                regs = modbus_client.read_holding(client, 0, 2, unit=1)
                self.assertEqual(regs[0], 375)
                self.assertEqual(modbus_client.scale_value(regs[0], 0.1), 37.5)
                self.assertEqual(modbus_client.scale_value(regs[1], 1.0, signed=True), -10)
                modbus_client.write_register(client, 5, 1234, unit=1)
                self.assertEqual(modbus_client.read_holding(client, 5, 1, unit=1), [1234])
                client.close()
            finally:
                proc.terminate()
                proc.wait(timeout=10)

    def test_scale_and_validation(self):
        import modbus_client

        self.assertEqual(modbus_client.scale_value(0xFFFF, 1.0, signed=True), -1)
        with self.assertRaises(ValueError):
            modbus_client.scale_value(70000)
        with self.assertRaises(ValueError):
            modbus_client.write_register(None, 0, 70000, unit=1)


class IndustrialTests(unittest.TestCase):
    def test_cooling_tower_hand_calculation(self):
        """Hot 35 C, cold 25 C, wet-bulb 22 C, 360 m3/h.
        Harapan: range 10, approach 3, efektivitas 76.92 %, beban 4186 kW, evaporasi 6.0 m3/h."""
        import cooling_tower as ct

        r = ct.analyse(35, 25, 22, 360)
        self.assertAlmostEqual(r["range_c"], 10.0)
        self.assertAlmostEqual(r["approach_c"], 3.0)
        self.assertAlmostEqual(r["effectiveness_pct"], 76.92, places=2)
        self.assertAlmostEqual(r["heat_load_kw"], 4186.0, places=1)
        self.assertAlmostEqual(r["evaporation_m3_h_estimate"], 6.0, places=3)

    def test_cooling_tower_rejects_impossible_cold_water(self):
        import cooling_tower as ct

        with self.assertRaises(ValueError):
            ct.analyse(35, 20, 22, 360)  # di bawah wet-bulb: tidak mungkin

    def test_boiler_siegert_and_efficiency(self):
        """Gas alam, T_flue 180 C, ambien 30 C, CO2 10 %.
        Harapan: rugi gas buang = 0.38*150/10 = 5.7 %; efisiensi = 100 - (5.7+0.5) = 93.8 %."""
        import boiler_efficiency as be

        loss = be.flue_gas_loss_pct(180, 30, 10, "natural_gas")
        self.assertAlmostEqual(loss, 5.7, places=6)
        r = be.efficiency({"dry_flue_gas": loss, "radiation": 0.5})
        self.assertAlmostEqual(r["efficiency_pct"], 93.8, places=3)

    def test_boiler_rejects_bad_input(self):
        import boiler_efficiency as be

        with self.assertRaises(ValueError):
            be.flue_gas_loss_pct(20, 30, 10)
        with self.assertRaises(ValueError):
            be.efficiency({"a": 60, "b": 50})

    def test_ro_mass_balance(self):
        """Qf 10 m3/h, Cf 1000 mg/L, Qp 5 m3/h, Cp 20 mg/L.
        Harapan: recovery 50 %, rejection 98 %, Qc 5, Cc 1980 mg/L, neraca garam tertutup."""
        import ro_mass_balance as ro

        r = ro.mass_balance(10, 1000, 5, 20)
        self.assertAlmostEqual(r["recovery_pct"], 50.0)
        self.assertAlmostEqual(r["rejection_pct"], 98.0)
        self.assertAlmostEqual(r["q_concentrate"], 5.0)
        self.assertAlmostEqual(r["c_concentrate"], 1980.0, places=2)
        self.assertAlmostEqual(r["salt_balance_error"], 0.0, places=6)

    def test_savings_closed_form(self):
        """100/bulan selama 1 tahun dengan 12 %/tahun (bulanan 1 %): 100*((1.01^12-1)/0.01) = 1268.25.
        Dan 0 % selama 10 tahun = 12000."""
        import savings_projection as sp

        self.assertAlmostEqual(sp.project(0, 100, 12, 1)["future_value"], 1268.25, places=2)
        self.assertAlmostEqual(sp.project(0, 100, 0, 10)["future_value"], 12000.0)
        with self.assertRaises(ValueError):
            sp.project(0, -1, 5, 1)


if __name__ == "__main__":
    unittest.main()
