---
name: trade-statistics
description: Compute backtest or journal performance statistics from a list of per-trade PnL values - win rate, expectancy, profit factor, and maximum drawdown with sample-size warnings. Use for evaluating a trading strategy's historical results, including XAUUSD ICT/SMC backtests. Never promises future profit.
license: original-zy
compatibility: Python 3.9+ standard library only
metadata: {"category": "quantitative-trading", "status": "validated", "owner": "zy"}
---

# Trade Statistics (Expectancy, Profit Factor, Max Drawdown)

## Activation Triggers
- User meminta "expectancy", "profit factor", "max drawdown", "win rate", "statistik backtest", atau "evaluasi strategi".
- User memiliki CSV hasil backtest atau jurnal trade dan ingin ringkasan kuantitatif.
- Sebelum user mempertimbangkan strategi lebih lanjut: script dipakai sebagai gerbang evaluasi, bukan sebagai rekomendasi.

## Scope dan Batas Kemampuan
- Dicakup: metrik deskriptif dari daftar PnL historis.
- TIDAK dicakup: pengambilan data pasar (script tidak mengunduh harga), simulasi slippage/komisi (harus sudah ada di PnL), uji signifikansi statistik lanjutan, dan prediksi.
- Tidak pernah menjanjikan keuntungan. Hasil historis tidak menjamin hasil masa depan.

## Required Tools
- Python 3.9+ standard library.
- `scripts/trade_stats.py`.
- Sumber data: CSV dari platform backtest (mis. backtesting.py, lisensi AGPL-3.0 lihat referensi) atau jurnal manual.

## Input dan Output Specification
Input: CSV dengan kolom `pnl` (default), satu baris per trade, dalam mata uang yang sama. Opsional `--starting-equity` untuk drawdown persentase.

Output: `total_trades, wins, losses, win_rate_pct, avg_win, avg_loss, expectancy, net_pnl, profit_factor, max_drawdown_abs, max_drawdown_pct`, plus `warning` bila sampel < 30.

Definisi:
- Expectancy = rata-rata PnL per trade.
- Profit factor = gross profit / |gross loss|; `None` bila tidak ada trade rugi.
- Max drawdown = penurunan terbesar dari puncak equity sepanjang urutan trade.

## Execution Workflow
1. Pastikan CSV berisi PnL bersih (sudah termasuk biaya). Catat asumsi biaya.
2. Pastikan urutan baris = urutan waktu trade (drawdown bergantung pada urutan).
3. Jalankan `python scripts/trade_stats.py trades.csv --starting-equity 10000 --json`.
4. Laporkan hasil dengan warning sampel dan periode data.
5. Jika metrik buruk, sampaikan apa adanya; jangan menyarankan "tambah leverage" untuk menutupi.

## Decision Rules
- Sampel < 30 trade: tampilkan warning dan jangan membuat kesimpulan kuat.
- Profit factor tinggi dengan sampel kecil dapat menyesatkan; selalu tampilkan jumlah trade.
- Jika user ingin "memastikan profit", jawab bahwa statistik ini deskriptif, bukan jaminan.
- Overfitting: bila strategi dioptimasi pada data yang sama dengan yang dievaluasi, tandai hasilnya sebagai in-sample.

## Error Handling
- CSV tanpa kolom target: error, exit code 2.
- PnL bukan angka: error menyebut baris.
- Daftar kosong: error.

## Quality Control
- Cek: `win_rate + loss_rate + breakeven = 100%`.
- Cek: `expectancy * total_trades = net_pnl` (toleransi pembulatan).
- Unit test `tests/test_trade_stats.py` harus lulus.

## Acceptance Criteria
- Untuk PnL [100, -50, 200, -100]: expectancy 37.5, profit factor 2.0, win rate 50%.
- Max drawdown untuk starting equity 10000 dan PnL [-500, +200, -800]: path equity 10000 -> 9500 -> 9700 -> 8900; puncak 10000, drawdown terbesar 1100 (11.0%).
- Sampel < 30 menghasilkan warning.

## Contoh Implementasi
```bash
python scripts/trade_stats.py examples/trades.csv --starting-equity 10000
```

## Test Cases
Lihat `tests/test_trade_stats.py`:
1. Statistik dasar (expectancy, profit factor, win rate).
2. Tanpa kerugian: profit factor = None.
3. Max drawdown dengan dan tanpa starting equity.
4. Input kosong dan non-numerik ditolak.

## Referensi dan Sumber
- Definisi expectancy dan profit factor adalah konvensi umum analisis trading.
- Lihat `references/metrics-definitions.md`.
- Pembanding library: ranaroussi/quantstats (Apache-2.0) untuk tearsheet; kernc/backtesting.py (AGPL-3.0) untuk backtest. Lisensi AGPL memengaruhi penggunaan jaringan; baca sebelum memakai.

## Informasi Lisensi
- Kode dan dokumentasi: `original-zy`. Tidak menyalin kode dari library pihak ketiga.
- Skill ini tidak memberikan nasihat keuangan atau investasi.
