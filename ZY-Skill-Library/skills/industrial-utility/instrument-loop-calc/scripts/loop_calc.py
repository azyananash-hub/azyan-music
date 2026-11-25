"""Konversi loop instrumen: 4-20 mA ke nilai teknik, deteksi fault (NAMUR NE43), dan Pt100 (IEC 60751).

4-20 mA: value = LRV + (I - 4)/16 * (URV - LRV). Di luar 3.6-21.0 mA dianggap fault (NAMUR NE43).
Pt100 (T >= 0 C), Callendar-Van Dusen: R(T) = R0 (1 + A T + B T^2), A = 3.9083e-3, B = -5.775e-7, R0 = 100.
"""
from __future__ import annotations

import argparse
import json
import math
import sys

A, B, R0 = 3.9083e-3, -5.775e-7, 100.0


def ma_to_value(i_ma: float, lrv: float, urv: float) -> dict:
    if urv == lrv:
        raise ValueError("URV dan LRV tidak boleh sama")
    fault = not (3.6 <= i_ma <= 21.0)
    value = lrv + (i_ma - 4.0) / 16.0 * (urv - lrv)
    return {"value": round(value, 6), "percent_of_span": round((i_ma - 4.0) / 16.0 * 100, 4),
            "fault_namur_ne43": fault}


def pt100_resistance(t_c: float) -> float:
    if t_c < 0:
        raise ValueError("rumus ini hanya untuk T >= 0 C")
    return R0 * (1 + A * t_c + B * t_c * t_c)


def pt100_temperature(r_ohm: float) -> float:
    """Invers Callendar-Van Dusen untuk T >= 0 C."""
    if r_ohm < R0:
        raise ValueError("R < R0 berarti T < 0 C, di luar rumus ini")
    c = 1 - r_ohm / R0
    return (-A + math.sqrt(A * A - 4 * B * c)) / (2 * B)


def _main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--ma", type=float)
    p.add_argument("--lrv", type=float, default=0.0)
    p.add_argument("--urv", type=float, default=100.0)
    p.add_argument("--pt100-c", type=float)
    a = p.parse_args(argv)
    try:
        if a.ma is not None:
            print(json.dumps(ma_to_value(a.ma, a.lrv, a.urv), indent=2))
        if a.pt100_c is not None:
            print(json.dumps({"t_c": a.pt100_c, "r_ohm": round(pt100_resistance(a.pt100_c), 4)}, indent=2))
        if a.ma is None and a.pt100_c is None:
            p.error("beri --ma atau --pt100-c")
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_main())
