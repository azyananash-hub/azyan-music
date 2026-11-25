"""Arus nominal dan regulasi tegangan transformator (pendekatan standar).

I_rated = S / (sqrt(3) * V_LL)
Z_ohm_base = (Z% / 100) * V^2 / S            (dipakai hanya sebagai referensi)
R% = Z% / sqrt(1 + (X/R)^2) ; X% = R% * (X/R)
Regulasi (pendekatan): dV% = R% * cos(phi) + X% * sin(phi)   (phi lagging)
Pendekatan ini mengabaikan orde kedua. Untuk nilai desain gunakan data nameplate dan standar uji.
"""
from __future__ import annotations

import argparse
import json
import math
import sys


def analyse(s_kva: float, v_ll_v: float, z_percent: float, xr: float, pf: float) -> dict:
    if s_kva <= 0 or v_ll_v <= 0 or z_percent <= 0 or xr <= 0:
        raise ValueError("S, V, Z%, dan X/R harus > 0")
    if not 0 < pf <= 1:
        raise ValueError("power factor harus di (0, 1]")
    i_rated = s_kva * 1000.0 / (math.sqrt(3) * v_ll_v)
    r_pct = z_percent / math.sqrt(1 + xr**2)
    x_pct = r_pct * xr
    sin_phi = math.sqrt(1 - pf**2)
    dv_pct = r_pct * pf + x_pct * sin_phi
    return {
        "i_rated_a": round(i_rated, 3),
        "r_pct": round(r_pct, 4),
        "x_pct": round(x_pct, 4),
        "voltage_regulation_pct": round(dv_pct, 4),
        "note": "Pendekatan regulasi lagging; gunakan nameplate dan standar uji untuk nilai desain.",
    }


def _main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--kva", type=float, required=True)
    p.add_argument("--v-ll", type=float, required=True, help="V line-to-line (V)")
    p.add_argument("--z-percent", type=float, required=True)
    p.add_argument("--xr", type=float, required=True)
    p.add_argument("--pf", type=float, default=0.8)
    a = p.parse_args(argv)
    try:
        print(json.dumps(analyse(a.kva, a.v_ll, a.z_percent, a.xr, a.pf), indent=2))
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_main())
