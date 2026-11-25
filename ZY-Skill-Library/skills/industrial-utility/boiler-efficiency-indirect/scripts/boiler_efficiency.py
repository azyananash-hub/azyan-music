"""Efisiensi boiler metode tidak langsung (indirect / heat loss method).

  efficiency = 100 - sum(losses_%)
  losses: dry flue gas, moisture dalam bahan bakar, H2 dari pembakaran, radiasi, unburnt.

Kerugian gas buang kering dihitung dengan rumus Siegert yang disederhanakan:
  L_flue_% = K * (T_flue - T_ambient) / CO2_%
K adalah konstanta bahan bakar (perkiraan: gas alam ~0.37-0.40, minyak ~0.50; verifikasi
dengan data bahan bakar aktual dan standar ASME PTC 4 / BS EN 12952 sebelum dipakai).

Batas keselamatan: script ini tidak memberi instruksi pengoperasian. Kondisi tekanan dan
suhu tinggi harus mengikuti SOP dan batas keselamatan boiler.
"""

from __future__ import annotations

import argparse
import json
import sys

SIEGERT_K = {"natural_gas": 0.38, "fuel_oil": 0.50}  # perkiraan awal, lihat docstring


def flue_gas_loss_pct(t_flue_c: float, t_ambient_c: float, co2_pct: float, fuel: str = "natural_gas") -> float:
    if fuel not in SIEGERT_K:
        raise ValueError(f"fuel harus salah satu dari {sorted(SIEGERT_K)}")
    if not 0 < co2_pct <= 20:
        raise ValueError("CO2 kering harus di (0, 20] persen")
    if t_flue_c < t_ambient_c:
        raise ValueError("suhu gas buang tidak boleh di bawah suhu ambien")
    return SIEGERT_K[fuel] * (t_flue_c - t_ambient_c) / co2_pct


def efficiency(losses: dict[str, float]) -> dict:
    for k, v in losses.items():
        if not 0 <= v <= 100:
            raise ValueError(f"kerugian {k} harus 0..100 persen, dapat {v}")
    total = sum(losses.values())
    if total >= 100:
        raise ValueError("total kerugian >= 100%, input tidak masuk akal")
    return {"efficiency_pct": round(100.0 - total, 3), "total_losses_pct": round(total, 3), "losses_pct": losses}


def _main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--t-flue", type=float, required=True, help="Suhu gas buang (C)")
    p.add_argument("--t-ambient", type=float, default=30.0)
    p.add_argument("--co2", type=float, required=True, help="CO2 kering dalam gas buang (%)")
    p.add_argument("--fuel", choices=sorted(SIEGERT_K), default="natural_gas")
    p.add_argument("--radiation-pct", type=float, default=0.5)
    p.add_argument("--moisture-fuel-pct", type=float, default=0.0)
    p.add_argument("--hydrogen-pct", type=float, default=0.0)
    p.add_argument("--unburnt-pct", type=float, default=0.0)
    args = p.parse_args(argv)
    try:
        flue = flue_gas_loss_pct(args.t_flue, args.t_ambient, args.co2, args.fuel)
        result = efficiency({
            "dry_flue_gas": round(flue, 3),
            "moisture_in_fuel": args.moisture_fuel_pct,
            "hydrogen_combustion": args.hydrogen_pct,
            "radiation": args.radiation_pct,
            "unburnt": args.unburnt_pct,
        })
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(_main())
