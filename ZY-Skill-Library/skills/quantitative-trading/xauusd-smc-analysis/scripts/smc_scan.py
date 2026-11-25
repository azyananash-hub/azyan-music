"""Deteksi konsep Smart Money (FVG dan swing high/low) pada data OHLC dengan library smartmoneyconcepts (MIT).

Ini adalah DEFINISI KONSEP pada data yang Anda berikan, bukan sinyal trading. Tidak ada data pasar yang
diunduh atau dikarang. Hasil historis tidak menjamin hasil masa depan.
Input CSV kolom: time,open,high,low,close. Usage: python smc_scan.py data.csv --swing 5
"""
from __future__ import annotations

import argparse
import json
import sys

import pandas as pd
from smartmoneyconcepts import smc


def scan(df: pd.DataFrame, swing: int = 5) -> dict:
    need = {"open", "high", "low", "close"}
    if not need <= set(df.columns):
        raise ValueError(f"kolom wajib: {sorted(need)}")
    fvg = smc.fvg(df)
    zones = []
    for i, row in fvg.iterrows():
        if pd.notna(row["FVG"]):
            zones.append({"index": int(i), "type": "bullish" if row["FVG"] > 0 else "bearish",
                          "top": float(row["Top"]), "bottom": float(row["Bottom"])})
    sw = smc.swing_highs_lows(df, swing_length=swing)
    swings = [{"index": int(i), "type": "swing_high" if row["HighLow"] > 0 else "swing_low",
               "level": float(row["Level"])}
              for i, row in sw.iterrows() if pd.notna(row["HighLow"])]
    return {"fvg_zones": zones, "swings": swings,
            "disclaimer": "Definisi konsep pada data input. Bukan rekomendasi trading."}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--swing", type=int, default=5)
    a = ap.parse_args()
    try:
        df = pd.read_csv(a.csv)
        print(json.dumps(scan(df, a.swing), indent=2))
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
