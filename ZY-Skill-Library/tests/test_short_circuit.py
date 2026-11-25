import math
import unittest

from _helpers import SHORT_CIRCUIT, load_module

sc = load_module("short_circuit", SHORT_CIRCUIT)


class ShortCircuitTests(unittest.TestCase):
    def test_source_only_matches_s_over_sqrt3_v(self):
        # 11 kV, 100 MVA: Ik = S / (sqrt(3) * V) = 100 / (1.7320508 * 11) = 5.2486 kA
        result = sc.analyse(v_sec_kv=11, s_sc_mva=100)
        self.assertAlmostEqual(result["ik_kA_rms"], 5.2486, places=3)

    def test_kappa_limits(self):
        self.assertAlmostEqual(sc.iec_kappa(0.0), 2.0, places=12)
        self.assertAlmostEqual(sc.iec_kappa(1000.0), 1.02, places=6)

    def test_peak_is_sqrt2_kappa_ik(self):
        ik = 10.0
        self.assertAlmostEqual(sc.peak_current_ka(ik, 0.0), math.sqrt(2) * 2.0 * ik, places=9)

    def test_transformer_branch_reduces_current(self):
        base = sc.analyse(v_sec_kv=0.4, s_sc_mva=500, v_hv_kv=20)  # tanpa trafo ikut dihitung
        # Trafo tidak diberikan: tetap sumber saja
        self.assertIsNotNone(base["ik_kA_rms"])
        with_trafo = sc.analyse(
            v_sec_kv=0.4, s_sc_mva=500, v_hv_kv=20, transformer_mva=1.0, transformer_z_percent=6.0
        )
        self.assertLess(with_trafo["ik_kA_rms"], base["ik_kA_rms"])

    def test_transformer_impedance_value(self):
        # Z_T = 0.06 * 0.4^2 / 1 = 0.0096 ohm (magnitudo)
        z = sc.transformer_impedance_ohm(v_sec_kv=0.4, s_rated_mva=1.0, z_percent=6.0, x_r_ratio=1e9)
        self.assertAlmostEqual(abs(z), 0.0096, places=6)

    def test_partial_transformer_input_rejected(self):
        with self.assertRaises(ValueError):
            sc.analyse(v_sec_kv=0.4, s_sc_mva=500, transformer_mva=1.0)

    def test_transformer_requires_hv_voltage(self):
        with self.assertRaises(ValueError):
            sc.analyse(v_sec_kv=0.4, s_sc_mva=500, transformer_mva=1.0, transformer_z_percent=6.0)

    def test_nonpositive_inputs_rejected(self):
        for kwargs in ({"v_sec_kv": 0, "s_sc_mva": 100}, {"v_sec_kv": 11, "s_sc_mva": -1},
                       {"v_sec_kv": float("nan"), "s_sc_mva": 100}):
            with self.assertRaises(ValueError):
                sc.analyse(**kwargs)

    def test_bool_and_string_types_rejected(self):
        with self.assertRaises(TypeError):
            sc.source_impedance_ohm(True, 100)

    def test_cli_returns_2_on_bad_input(self):
        import contextlib
        import io

        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(sc.main(["--v-sec-kv", "0", "--s-sc-mva", "100"]), 2)

    def test_cli_json_success(self):
        import contextlib
        import io

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(sc.main(["--v-sec-kv", "11", "--s-sc-mva", "100", "--json"]), 0)
        self.assertIn('"ik_kA_rms": 5.2486', buf.getvalue())


if __name__ == "__main__":
    unittest.main()
