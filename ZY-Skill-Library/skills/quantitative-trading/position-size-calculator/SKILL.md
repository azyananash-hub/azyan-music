---
name: position-size-calculator
description: Calculate position size from account equity, fixed-fraction risk percent, entry and stop-loss prices, and contract value per unit (e.g. XAUUSD lot specs). Use for risk management planning before a trade. Provides sizing math only, never trade signals or profit guarantees.
license: original-zy
compatibility: Python 3.9+ standard library only
metadata: {"category": "quantitative-trading", "status": "verified", "owner": "zy"}
---

# Position Size Calculator (Fixed-Fractional Risk)

## Activation Triggers
- User meminta "lot size", "position size", "ukuran posisi", "risk per trade", atau "berapa lot".
- User menyebut entry, stop loss, dan persentase risiko dan ingin ukuran posisi.
- Penyusunan rencana manajemen risiko sebelum backtest atau live (paper) trading.

## Scope dan Batas Kemampuan
- Dicakup: perhitungan matematis ukuran posisi dari risiko yang ditentukan user.
- TIDAK dicakup: menentukan arah trade, level entry/stop (itu keputusan strategi user), data harga, dan eksekusi order.
- Tidak menjamin hasil. Mengatur ukuran posisi tidak menghilangkan risiko kerugian.

## Required Tools
- Python 3.9+ standard library.
- `scripts/position_size.py`.

## Input dan Output Specification
Input:
- `--equity` (mata uang akun), `--risk-pct` (0 < x <= 10), `--entry`, `--stop` (satuan harga)
- `--value-per-unit`: nilai mata uang per 1 satuan harga per 1 unit/lot. Contoh XAUUSD dengan 1 lot = 100 oz: 100.
- `--max-units` (opsional, batas broker atau kebijakan pribadi).

Output: `direction, risk_amount, stop_distance, loss_per_unit, units, actual_risk_amount, capped_by_max_units`.

## Execution Workflow
1. Konfirmasi spesifikasi kontrak broker (nilai per point, minimum lot, step lot). Jangan mengasumsikan.
2. Tentukan risk_pct dari kebijakan pribadi (umumnya kecil; batas 10% diterapkan sebagai guard rail).
3. Jalankan: `python scripts/position_size.py --equity 10000 --risk-pct 1 --entry 2650 --stop 2640 --value-per-unit 100`
4. Bulatkan ke step lot broker ke bawah (jangan ke atas, agar risiko tidak melebihi rencana).
5. Verifikasi `actual_risk_amount` <= `risk_amount`.

## Decision Rules
- Jika stop_distance = 0, tolak: sizing tidak terdefinisi.
- Jika hasil units melebihi batas broker atau max-units, gunakan batas dan catat `capped_by_max_units`.
- Jika user meminta angka lot untuk "pasti untung" atau "tanpa stop", tolak dan jelaskan bahwa perhitungan ini membutuhkan stop yang jelas.
- Nilai `value-per-unit` berbeda antara broker dan simbol; selalu minta konfirmasi bila tidak yakin.

## Error Handling
- Equity <= 0, risk_pct di luar (0, 10], value <= 0, entry == stop: error, exit code 2.
- Input non-finite (NaN/inf) ditolak.

## Quality Control
- Verifikasi manual: risk_amount = equity x risk_pct / 100.
- Verifikasi: units x loss_per_unit = actual_risk_amount (<= risk_amount tanpa cap).
- Unit test `tests/test_position_size.py`.

## Acceptance Criteria
- Equity 10000, risk 1%, stop jarak 10 poin, value 100: units = 0.1 lot, risk 100.
- Arah short ditentukan saat stop di atas entry.
- Cap max-units bekerja dan dilaporkan.

## Contoh Implementasi
```bash
python scripts/position_size.py --equity 10000 --risk-pct 1 --entry 2650 --stop 2640 --value-per-unit 100
python scripts/position_size.py --equity 10000 --risk-pct 0.5 --entry 2650 --stop 2665 --value-per-unit 100 --max-units 0.05
```

## Test Cases
Lihat `tests/test_position_size.py`: perhitungan dasar, short vs long, cap, validasi input.

## Referensi dan Sumber
- Konsep fixed-fractional position sizing (umum dalam manajemen risiko).
- Lihat `references/xauusd-contract-checklist.md` untuk daftar verifikasi kontrak.

## Informasi Lisensi
- Kode dan dokumentasi: `original-zy`.
- Skill ini tidak memberikan nasihat keuangan.
