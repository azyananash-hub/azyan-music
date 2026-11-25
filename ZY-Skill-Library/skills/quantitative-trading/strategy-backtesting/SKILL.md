---
name: strategy-backtesting
description: Backtest a moving-average crossover on OHLC bars with strict no-lookahead execution: signals use closes up to bar t and fill at the open of bar t+1, with per-side fees and compounded returns. Use to test a rule's historical behavior before any live decision; never a profit guarantee.
license: MIT
compatibility: Python 3.9+ standard library only
metadata: {"category": "quantitative-trading", "status": "verified", "owner": "zy", "classification": "CUSTOM"}
---

# strategy-backtesting

## Activation Triggers
- User meminta "backtest", "crossover MA", "lookahead bias", atau "uji strategi historis".

## Scope dan Batas Kemampuan
- Dicakup: sinyal crossover MA, eksekusi tanpa lookahead, biaya per sisi, return per trade dan majemuk.
- TIDAK dicakup: slippage berbasis volume, multi-aset, manajemen margin, dan data pasar (harus disediakan user).

## Required Tools
- Python 3.9+ standard library. `scripts/backtest.py`

## Input dan Output Specification
Fungsi: crossover_signal(closes, fast, slow), run(opens, closes, fast, slow, fee_per_side). Output: trades (entry, exit, return), trade_count, total_return.

## Execution Workflow
1. Siapkan OHLC historis yang sudah dibersihkan. 2. Jalankan run dengan parameter tetap. 3. Laporkan jumlah trade dan dispersi return bersama total return. 4. Uji ulang pada periode lain.

## Decision Rules
- Parameter yang dicoba banyak kali menghasilkan overfitting; laporkan jumlah percobaan.
- Trade sedikit berarti statistik tidak berarti.

## Error Handling
- fast >= slow atau data tidak sepanjang: ValueError.

## Quality Control
- Tidak ada sinyal yang memakai data bar setelah t; entri selalu di open t+1.

## Acceptance Criteria
- Pada deret 8 bar dengan open bar 2 = 3.5: entri 3.5, dua trade, total return -0.619048.

## Contoh Implementasi
```python
from backtest import run
print(run(opens, closes, 5, 20, fee_per_side=0.0005))
```

## Test Cases
`tests/skills/test_v07_batch2.py` (BacktestTests).

## Referensi dan Sumber
- Konvensi backtest tanpa lookahead (eksekusi bar berikutnya): praktik umum, diimplementasikan ulang.

## Informasi Lisensi
- Skill: MIT.
