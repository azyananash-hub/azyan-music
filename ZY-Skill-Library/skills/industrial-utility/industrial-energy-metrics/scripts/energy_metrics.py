"""Metrik energi industri: power factor correction dan intensitas energi.

Kapasitor untuk memperbaiki PF: Qc = P * (tan(phi1) - tan(phi2)), tan(phi) = sqrt(1/pf^2 - 1).
Intensitas energi (kWh per unit) = energi_kWh / output_unit.
"""
from __future__ import annotations

import argparse
import json
import math
import sys


def pfc_kvar(p_kw: float, pf1: float, pf2: float) -> float:
    if p_kw <= 0:
        raise ValueError("P harus > 0")
    if not (0 < pf1 <= 1 and 0 < pf2 <= 1):
        raise ValueError("PF harus di (0, 1]")
    if pf2 < pf1:
        raise ValueError("pf2 (target) harus >= pf1 (awal)")
    tan1 = math.sqrt(1 / pf1**2 - 1)
    tan2 = math.sqrt(1 / pf2**2 - 1)
    return p_kw * (tan1 - tan2)


def intensity(energy_kwh: float, output_units: float) -> float:
    if energy_kwh < 0 or output_units <= 0:
        raise ValueError("energi >= 0 dan output > 0")
    return energy_kwh / output_units


def _main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--kw", type=float)
    p.add_argument("--pf1", type=float)
    p.add_argument("--pf2", type=float)
    p.add_argument("--kwh", type=float)
    p.add_argument("--output", type=float)
    a = p.parse_args(argv)
    out = {}
    try:
        if None not in (a.kw, a.pf1, a.pf2):
            out["qc_kvar"] = round(pfc_kvar(a.kw, a.pf1, a.pf2), 4)
        if None not in (a.kwh, a.output):
            out["kwh_per_unit"] = round(intensity(a.kwh, a.output), 6)
        if not out:
            p.error("beri --kw/--pf1/--pf2 dan/atau --kwh/--output")
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(_main())
