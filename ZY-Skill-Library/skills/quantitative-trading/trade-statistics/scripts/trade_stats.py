"""Statistik performa dari daftar hasil trade (PnL per trade).

Metrik:
  - total_trades, win_rate, avg_win, avg_loss
  - expectancy  = mean(PnL per trade)            (dalam satuan PnL input)
  - profit_factor = gross_profit / |gross_loss|  (None bila tidak ada loss)
  - max_drawdown  = penurunan terbesar dari puncak equity (absolut dan persen)

PERINGATAN:
  - Ini adalah statistik historis dari data yang diberikan. Tidak ada jaminan performa
    masa depan. Sampel kecil (< 30 trade) menghasilkan statistik yang sangat tidak stabil.
  - Tidak memperhitungkan slippage, komisi, spread, atau swap kecuali sudah termasuk di PnL.
  - Script ini tidak mengambil data pasar dan tidak mengarang data apa pun.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys

MIN_RECOMMENDED_SAMPLE = 30


def compute_stats(pnls: list[float], starting_equity: float | None = None) -> dict:
    if not pnls:
        raise ValueError("daftar PnL kosong")
    for i, v in enumerate(pnls):
        if not isinstance(v, (int, float)) or not math.isfinite(v):
            raise ValueError(f"PnL indeks {i} bukan angka finite: {v!r}")

    n = len(pnls)
    wins = [v for v in pnls if v > 0]
    losses = [v for v in pnls if v < 0]
    gross_profit = sum(wins)
    gross_loss = sum(losses)  # negatif atau nol

    profit_factor = None if gross_loss == 0 else round(gross_profit / abs(gross_loss), 4)

    # Equity curve
    equity = starting_equity if starting_equity is not None else 0.0
    peak = equity
    max_dd_abs = 0.0
    max_dd_pct = None
    for v in pnls:
        equity += v
        if equity > peak:
            peak = equity
        dd = peak - equity
        if dd > max_dd_abs:
            max_dd_abs = dd
            if peak > 0:
                max_dd_pct = dd / peak * 100.0

    result = {
        "total_trades": n,
        "wins": len(wins),
        "losses": len(losses),
        "breakeven": n - len(wins) - len(losses),
        "win_rate_pct": round(len(wins) / n * 100.0, 2),
        "avg_win": round(gross_profit / len(wins), 4) if wins else None,
        "avg_loss": round(gross_loss / len(losses), 4) if losses else None,
        "expectancy": round(sum(pnls) / n, 4),
        "net_pnl": round(sum(pnls), 4),
        "profit_factor": profit_factor,
        "max_drawdown_abs": round(max_dd_abs, 4),
        "max_drawdown_pct": round(max_dd_pct, 2) if max_dd_pct is not None else None,
    }
    if n < MIN_RECOMMENDED_SAMPLE:
        result["warning"] = f"sampel {n} < {MIN_RECOMMENDED_SAMPLE}: statistik belum andal"
    if starting_equity is None:
        result["note"] = "max_drawdown_pct tidak dihitung tanpa starting_equity (drawdown dari 0)"
    return result


def load_pnls(fh, column: str = "pnl") -> list[float]:
    reader = csv.DictReader(fh)
    if reader.fieldnames is None or column not in reader.fieldnames:
        raise ValueError(f"kolom '{column}' tidak ditemukan di CSV")
    out = []
    for line_no, rec in enumerate(reader, start=2):
        try:
            out.append(float(rec[column]))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"baris {line_no}: PnL tidak valid {rec[column]!r}") from exc
    return out


def _main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv_file", help="CSV dengan kolom pnl (satu baris per trade)")
    p.add_argument("--column", default="pnl")
    p.add_argument("--starting-equity", type=float, default=None)
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    try:
        with open(args.csv_file, newline="", encoding="utf-8") as fh:
            pnls = load_pnls(fh, args.column)
        stats = compute_stats(pnls, args.starting_equity)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(stats, indent=2, ensure_ascii=False) if args.json else
          "\n".join(f"{k}: {v}" for k, v in stats.items()))
    return 0


if __name__ == "__main__":
    sys.exit(_main())
