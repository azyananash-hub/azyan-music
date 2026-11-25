"""Kalkulator ukuran posisi berbasis risiko tetap per trade (fixed-fractional risk).

Rumus:
  risk_amount      = equity * risk_pct / 100
  stop_distance    = |entry - stop|                       (satuan harga)
  loss_per_unit    = stop_distance * value_per_price_unit  (mata uang per 1 unit)
  units            = risk_amount / loss_per_unit

Contoh konfigurasi XAUUSD: 1 lot = 100 troy oz, sehingga value_per_price_unit = 100
per 1.00 pergerakan harga per lot. Verifikasi spesifikasi kontrak broker Anda sendiri.

Script ini TIDAK memberi sinyal trading dan TIDAK menjamin hasil.
"""

from __future__ import annotations

import argparse
import math
import sys


def position_size(
    equity: float,
    risk_pct: float,
    entry: float,
    stop: float,
    value_per_price_unit: float,
    max_units: float | None = None,
) -> dict:
    for name, v in (("equity", equity), ("entry", entry), ("stop", stop), ("value_per_price_unit", value_per_price_unit)):
        if not math.isfinite(v):
            raise ValueError(f"{name} harus finite")
    if equity <= 0:
        raise ValueError("equity harus > 0")
    if not 0 < risk_pct <= 10:
        # Batas 10% sebagai guard rail; risiko di atas itu hampir selalu salah konfigurasi.
        raise ValueError("risk_pct harus di (0, 10]")
    if value_per_price_unit <= 0:
        raise ValueError("value_per_price_unit harus > 0")
    stop_distance = abs(entry - stop)
    if stop_distance == 0:
        raise ValueError("stop tidak boleh sama dengan entry")
    # Stop di atas entry = posisi short; di bawah entry = posisi long.
    direction = "short" if stop > entry else "long"

    risk_amount = equity * risk_pct / 100.0
    loss_per_unit = stop_distance * value_per_price_unit
    units = risk_amount / loss_per_unit
    capped = False
    if max_units is not None and units > max_units:
        units = max_units
        capped = True

    return {
        "direction": direction,
        "risk_amount": round(risk_amount, 2),
        "stop_distance": round(stop_distance, 6),
        "loss_per_unit": round(loss_per_unit, 6),
        "units": round(units, 4),
        "actual_risk_amount": round(units * loss_per_unit, 2),
        "capped_by_max_units": capped,
    }


def _main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--equity", type=float, required=True)
    p.add_argument("--risk-pct", type=float, required=True)
    p.add_argument("--entry", type=float, required=True)
    p.add_argument("--stop", type=float, required=True)
    p.add_argument("--value-per-unit", type=float, required=True,
                   help="Nilai mata uang per 1 satuan harga per 1 unit/lot")
    p.add_argument("--max-units", type=float, default=None)
    args = p.parse_args(argv)
    try:
        r = position_size(args.equity, args.risk_pct, args.entry, args.stop, args.value_per_unit, args.max_units)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    for k, v in r.items():
        print(f"{k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
