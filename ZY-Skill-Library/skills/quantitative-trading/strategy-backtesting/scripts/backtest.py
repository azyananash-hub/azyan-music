"""Backtest minimal crossover MA dengan eksekusi tanpa lookahead.

Aturan: sinyal dihitung dari close bar t (hanya data sampai t), posisi dibuka/ditutup pada OPEN bar t+1.
Posisi terbuka di akhir data ditutup pada close bar terakhir. Biaya dinyatakan per sisi (fraksi).
Hasil berupa return per trade dan return majemuk. Ini uji historis, bukan jaminan.
"""
from __future__ import annotations

import math


def sma(values: list[float], n: int) -> list[float | None]:
    out: list[float | None] = []
    for i in range(len(values)):
        out.append(None if i + 1 < n else sum(values[i + 1 - n:i + 1]) / n)
    return out


def crossover_signal(closes: list[float], fast: int, slow: int) -> list[int]:
    if not 0 < fast < slow:
        raise ValueError("harus 0 < fast < slow")
    f, s = sma(closes, fast), sma(closes, slow)
    return [1 if (f[i] is not None and s[i] is not None and f[i] > s[i]) else 0 for i in range(len(closes))]


def run(opens: list[float], closes: list[float], fast: int, slow: int, fee_per_side: float = 0.0) -> dict:
    if len(opens) != len(closes) or len(closes) < 2:
        raise ValueError("opens dan closes harus sama panjang, minimal 2 bar")
    sig = crossover_signal(closes, fast, slow)
    trades, pos, entry = [], 0, None
    for t in range(len(closes) - 1):
        desired = sig[t]
        if desired == pos:
            continue
        px = opens[t + 1]  # eksekusi di open bar berikutnya
        if desired == 1:
            entry = px
        else:
            trades.append(_trade(entry, px, fee_per_side, t + 1))
        pos = desired
    if pos == 1:
        trades.append(_trade(entry, closes[-1], fee_per_side, len(closes) - 1))
    growth = math.prod(1 + tr["return"] for tr in trades) if trades else 1.0
    return {"trades": trades, "trade_count": len(trades), "total_return": round(growth - 1, 6)}


def _trade(entry: float, exit_px: float, fee: float, idx: int) -> dict:
    gross = exit_px / entry - 1
    net = (1 + gross) * (1 - fee) * (1 - fee) - 1
    return {"exit_index": idx, "entry": entry, "exit": exit_px, "return": round(net, 6)}
