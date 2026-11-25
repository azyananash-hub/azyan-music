"""Klien Modbus TCP sederhana (pymodbus, BSD-3-Clause) dengan konversi skala register.

Contoh:
  python modbus_client.py read --host 192.168.1.20 --unit 1 --address 0 --count 2
  python modbus_client.py read --host 192.168.1.20 --unit 1 --address 0 --count 1 --scale 0.1
  python modbus_client.py write --host 192.168.1.20 --unit 1 --address 10 --value 375

PERINGATAN keselamatan: menulis register dapat mengubah setpoint peralatan fisik.
Jalankan 'write' hanya setelah konfirmasi alamat, skala, dan prosedur SOP dari pemilik sistem.
Modbus TCP tidak memiliki autentikasi; gunakan hanya di jaringan terisolasi/VPN.
"""

from __future__ import annotations

import argparse
import sys

from pymodbus.client import ModbusTcpClient


def read_holding(client, address: int, count: int, unit: int) -> list[int]:
    rr = client.read_holding_registers(address=address, count=count, device_id=unit)
    if rr.isError():
        raise IOError(f"read gagal pada alamat {address}: {rr}")
    return list(rr.registers)


def write_register(client, address: int, value: int, unit: int) -> None:
    if not 0 <= value <= 0xFFFF:
        raise ValueError("nilai register harus 0-65535 (unsigned 16-bit)")
    rr = client.write_register(address=address, value=value, device_id=unit)
    if rr.isError():
        raise IOError(f"write gagal pada alamat {address}: {rr}")


def scale_value(raw: int, scale: float = 1.0, signed: bool = False) -> float:
    """Konversi register 16-bit ke nilai teknik. Mode signed memakai two's complement."""
    if not 0 <= raw <= 0xFFFF:
        raise ValueError("raw harus 0-65535")
    value = raw - 0x10000 if signed and raw >= 0x8000 else raw
    return value * scale


def _main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("action", choices=["read", "write"])
    p.add_argument("--host", required=True)
    p.add_argument("--port", type=int, default=502)
    p.add_argument("--unit", type=int, default=1)
    p.add_argument("--address", type=int, required=True)
    p.add_argument("--count", type=int, default=1)
    p.add_argument("--value", type=int)
    p.add_argument("--scale", type=float, default=1.0)
    p.add_argument("--signed", action="store_true")
    args = p.parse_args(argv)
    client = ModbusTcpClient(args.host, port=args.port, timeout=3)
    if not client.connect():
        print(f"ERROR: tidak dapat terhubung ke {args.host}:{args.port}", file=sys.stderr)
        return 2
    try:
        if args.action == "read":
            regs = read_holding(client, args.address, args.count, args.unit)
            for i, raw in enumerate(regs):
                print(f"addr {args.address + i}: raw={raw} value={scale_value(raw, args.scale, args.signed)}")
        else:
            if args.value is None:
                print("ERROR: --value wajib untuk write", file=sys.stderr)
                return 2
            write_register(client, args.address, args.value, args.unit)
            print(f"OK: addr {args.address} = {args.value}")
    except (IOError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    finally:
        client.close()
    return 0


if __name__ == "__main__":
    sys.exit(_main())
