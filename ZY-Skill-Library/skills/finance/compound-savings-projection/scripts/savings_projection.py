"""Proyeksi tabungan dengan kontribusi bulanan dan bunga majemuk bulanan.

  r_m = annual_rate / 12
  FV  = P0 * (1 + r_m)^n + PMT * ((1 + r_m)^n - 1) / r_m      (PMT di akhir bulan)

Hasil adalah SKENARIO matematis dengan asumsi tingkat return yang Anda masukkan.
Tidak ada return yang dijamin; inflasi dan pajak belum diperhitungkan kecuali Anda
memasukkan tingkat return riil.
"""

from __future__ import annotations

import argparse
import json
import sys


def project(initial: float, monthly: float, annual_rate_pct: float, years: int) -> dict:
    if initial < 0 or monthly < 0:
        raise ValueError("initial dan monthly tidak boleh negatif")
    if years <= 0 or years > 100:
        raise ValueError("years harus 1..100")
    if annual_rate_pct <= -100:
        raise ValueError("annual_rate_pct tidak valid")
    n = years * 12
    r = annual_rate_pct / 100.0 / 12.0
    if r == 0:
        fv_pmt = monthly * n
    else:
        fv_pmt = monthly * ((1 + r) ** n - 1) / r
    fv_initial = initial * (1 + r) ** n
    total_contrib = initial + monthly * n
    fv = fv_initial + fv_pmt
    return {
        "months": n,
        "future_value": round(fv, 2),
        "total_contributed": round(total_contrib, 2),
        "growth_from_returns": round(fv - total_contrib, 2),
        "assumption": f"return tahunan {annual_rate_pct}% (asumsi, bukan jaminan), bunga majemuk bulanan",
    }


def _main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--initial", type=float, default=0.0)
    p.add_argument("--monthly", type=float, required=True)
    p.add_argument("--annual-rate", type=float, required=True, help="Persen per tahun, mis. 5 untuk 5%%")
    p.add_argument("--years", type=int, required=True)
    args = p.parse_args(argv)
    try:
        r = project(args.initial, args.monthly, args.annual_rate, args.years)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(r, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(_main())
