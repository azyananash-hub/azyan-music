"""Sifat air/uap jenuh via CoolProp (MIT). Satuan SI dengan keluaran kPa dan C.

Usage: python steam_props.py --p-kpa 1000
"""
from __future__ import annotations

import argparse
import json
import sys

from CoolProp.CoolProp import PropsSI


def saturation(p_kpa: float) -> dict:
    if not 0.6 <= p_kpa <= 22000:
        raise ValueError("p_kpa di luar rentang 0.6-22000 kPa (batas CoolProp air)")
    p = p_kpa * 1000.0
    t_sat_k = PropsSI("T", "P", p, "Q", 0, "Water")
    h_f = PropsSI("H", "P", p, "Q", 0, "Water") / 1000.0      # kJ/kg, cair jenuh
    h_g = PropsSI("H", "P", p, "Q", 1, "Water") / 1000.0      # kJ/kg, uap jenuh
    return {
        "p_kpa": p_kpa,
        "t_sat_c": round(t_sat_k - 273.15, 3),
        "hf_kj_kg": round(h_f, 3),
        "hg_kj_kg": round(h_g, 3),
        "hfg_kj_kg": round(h_g - h_f, 3),
        "note": "Properti termodinamika ideal dari CoolProp; bukan dasar desain tanpa verifikasi.",
    }


def _main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--p-kpa", type=float, required=True)
    a = p.parse_args(argv)
    try:
        print(json.dumps(saturation(a.p_kpa), indent=2))
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_main())
