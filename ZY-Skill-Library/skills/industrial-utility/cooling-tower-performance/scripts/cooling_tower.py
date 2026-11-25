"""Performa cooling tower: range, approach, effectiveness, beban panas, dan estimasi evaporasi.

Definisi (suhu dalam derajat Celsius):
  range         = T_hot_in - T_cold_out
  approach      = T_cold_out - T_wetbulb
  effectiveness = range / (T_hot_in - T_wetbulb)      (0..1; makin tinggi makin baik)
  heat_load_kw  = m_dot_water_kg_s * 4.186 * range    (kJ/kg.K, cair air ~4.186)
  evaporation   = aturan praktis: ~1% dari sirkulasi per 6 C (10 F) range
                  (rule of thumb; bukan pengganti perhitungan vendor)

Catatan: tidak memasukkan drift, blowdown, dan tekanan udara. Gunakan data pengukuran lapangan.
"""

from __future__ import annotations

import argparse
import json
import sys

CP_WATER_KJ_KG_K = 4.186
EVAP_FRACTION_PER_6C = 0.01  # aturan praktis, lihat docstring


def analyse(t_hot_in: float, t_cold_out: float, t_wetbulb: float, flow_m3_h: float) -> dict:
    for name, v in (("t_hot_in", t_hot_in), ("t_cold_out", t_cold_out), ("t_wetbulb", t_wetbulb)):
        if not -10 <= v <= 80:
            raise ValueError(f"{name} di luar rentang wajar (-10..80 C): {v}")
    if flow_m3_h <= 0:
        raise ValueError("flow_m3_h harus > 0")
    if t_hot_in <= t_cold_out:
        raise ValueError("t_hot_in harus lebih besar dari t_cold_out")
    if t_cold_out < t_wetbulb:
        raise ValueError("t_cold_out tidak mungkin di bawah wet-bulb (cooling tower tidak bisa mendinginkan melewati wet-bulb)")
    rng = t_hot_in - t_cold_out
    approach = t_cold_out - t_wetbulb
    effectiveness = rng / (t_hot_in - t_wetbulb)
    m_dot = flow_m3_h * 1000.0 / 3600.0  # kg/s, asumsi massa jenis air 1000 kg/m3
    heat_kw = m_dot * CP_WATER_KJ_KG_K * rng
    evap_m3_h = flow_m3_h * EVAP_FRACTION_PER_6C * (rng / 6.0)
    return {
        "range_c": round(rng, 3),
        "approach_c": round(approach, 3),
        "effectiveness_pct": round(effectiveness * 100, 2),
        "heat_load_kw": round(heat_kw, 2),
        "evaporation_m3_h_estimate": round(evap_m3_h, 3),
        "scope_note": "Estimasi termal dari data suhu/aliran; evaporasi adalah aturan praktis.",
    }


def _main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--t-hot-in", type=float, required=True)
    p.add_argument("--t-cold-out", type=float, required=True)
    p.add_argument("--t-wetbulb", type=float, required=True)
    p.add_argument("--flow-m3-h", type=float, required=True)
    args = p.parse_args(argv)
    try:
        r = analyse(args.t_hot_in, args.t_cold_out, args.t_wetbulb, args.flow_m3_h)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(r, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(_main())
