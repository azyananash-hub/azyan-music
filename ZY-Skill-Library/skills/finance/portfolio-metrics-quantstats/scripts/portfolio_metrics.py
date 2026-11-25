"""Metrik portofolio dari return harian (CSV kolom 'return') memakai quantstats (Apache-2.0).

Metrik deskriptif historis saja. Tidak ada jaminan performa masa depan.
Usage: python portfolio_metrics.py returns.csv
"""
from __future__ import annotations

import csv
import json
import sys

import numpy as np
import quantstats.stats as qs


def load_returns(path: str) -> "np.ndarray":
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows or "return" not in rows[0]:
        raise ValueError("CSV harus memiliki kolom 'return' dan minimal satu baris")
    vals = np.array([float(r["return"]) for r in rows], dtype=float)
    if not np.all(np.isfinite(vals)):
        raise ValueError("return mengandung nilai non-finite")
    return vals


def summarize(returns: "np.ndarray", periods: int = 252) -> dict:
    import pandas as pd

    # quantstats memerlukan indeks tanggal untuk drawdown; tanggal sintetis harian dipakai
    # hanya sebagai indeks (nilai drawdown tidak bergantung pada tanggal sebenarnya).
    idx = pd.date_range("2000-01-03", periods=len(returns), freq="B")
    s = pd.Series(returns, index=idx)
    equity = pd.Series(np.cumprod(1 + returns), index=idx)
    return {
        "n_days": int(len(returns)),
        "cumulative_return_pct": round(float((np.prod(1 + returns) - 1) * 100), 4),
        "sharpe_rf0": round(float(qs.sharpe(s, rf=0.0, periods=periods)), 4),
        "max_drawdown_pct": round(abs(float(qs.max_drawdown(equity)) * 100), 4),
        "volatility_ann_pct": round(float(qs.volatility(s, periods=periods) * 100), 4),
        "note": "Statistik historis; sampel kecil sangat tidak stabil.",
    }


if __name__ == "__main__":
    try:
        print(json.dumps(summarize(load_returns(sys.argv[1])), indent=2))
    except (OSError, ValueError, IndexError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
