"""Arus beban penuh motor 3 fasa dan perbandingan starter.

FLC (A) = P_kW / (sqrt(3) * V * PF * eta)
Star-delta: arus line saat start = 1/3 arus DOL, torsi start = 1/3 torsi DOL (relasi standar).
Rasio arus start (LRC/FLC) harus diambil dari nameplate motor; skill tidak menebak nilainya.
"""
from __future__ import annotations

import argparse
import json
import math
import sys


def analyse(p_kw: float, v: float, pf: float, eta: float, lrc_ratio: float) -> dict:
    if p_kw <= 0 or v <= 0:
        raise ValueError("P dan V harus > 0")
    if not (0 < pf <= 1 and 0 < eta <= 1):
        raise ValueError("PF dan efisiensi harus di (0, 1]")
    if lrc_ratio <= 1:
        raise ValueError("rasio arus start (LRC/FLC) harus > 1 dari nameplate")
    flc = p_kw * 1000.0 / (math.sqrt(3) * v * pf * eta)
    dol_start = lrc_ratio * flc
    return {
        "flc_a": round(flc, 3),
        "dol_start_current_a": round(dol_start, 3),
        "star_delta_start_current_a": round(dol_start / 3.0, 3),
        "star_delta_torque_ratio": round(1 / 3, 4),
        "note": "Relasi star-delta berlaku ideal; verifikasi dengan data starter dan beban sebenarnya.",
    }


def _main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--kw", type=float, required=True)
    p.add_argument("--v", type=float, required=True)
    p.add_argument("--pf", type=float, required=True)
    p.add_argument("--eta", type=float, required=True)
    p.add_argument("--lrc-ratio", type=float, required=True, help="LRC/FLC dari nameplate")
    a = p.parse_args(argv)
    try:
        print(json.dumps(analyse(a.kw, a.v, a.pf, a.eta, a.lrc_ratio), indent=2))
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_main())
