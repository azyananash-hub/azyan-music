---
name: xauusd-smc-analysis
description: Detect Smart Money Concept structures on supplied OHLC data for XAUUSD or any instrument: fair value gaps (bullish and bearish) and swing highs and lows, using the MIT smartmoneyconcepts library. Use for concept detection on historical or synthetic candles; it is not a trading signal generator.
license: MIT
compatibility: Python 3.9+; pandas, numpy, smartmoneyconcepts (MIT)
metadata: {"category": "quantitative-trading", "status": "verified", "owner": "zy", "classification": "CUSTOM"}
---

# xauusd-smc-analysis

## Activation Triggers
- User meminta "fair value gap", "FVG", "swing high low", "order block", atau "analisis SMC XAUUSD" pada data yang mereka berikan.

## Scope dan Batas Kemampuan
- Dicakup: deteksi FVG dan swing pada CSV OHLC yang diberikan user.
- TIDAK dicakup: pengunduhan data pasar, sinyal entry atau exit, janji profit, dan analisis berita.
- Konsep ICT/SMC bersifat interpretatif; skill hanya menjalankan definisi library.

## Required Tools
- Python 3.9+, pandas, numpy, smartmoneyconcepts (MIT). `scripts/smc_scan.py`

## Input dan Output Specification
Input: CSV kolom time, open, high, low, close dan --swing. Output JSON: fvg_zones (index, type, top, bottom), swings, disclaimer.

## Execution Workflow
1. Siapkan OHLC dari sumber yang Anda miliki dan berhak gunakan. 2. Jalankan scan. 3. Tinjau setiap zona secara manual sebelum mengambil keputusan apa pun.

## Decision Rules
- Jangan mengubah parameter swing sampai hasilnya terlihat bagus; catat parameter yang dipakai.
- Hasil hanya dianggap valid jika dicek ulang pada data lain.

## Error Handling
- Kolom OHLC hilang: ValueError dan exit 2.

## Quality Control
- Gap dicocokkan dengan definisi tangan pada data sintetis.

## Acceptance Criteria
- Pada data sintetis 7 lilin: bullish di 1 (10.0-10.7), bullish di 2 (10.6-11.0), bearish di 5 (11.2-11.3).

## Contoh Implementasi
```bash
python scripts/smc_scan.py data.csv --swing 5
```

## Test Cases
`tests/skills/test_v07_batch2.py` (SmcTests).

## Referensi dan Sumber
- smartmoneyconcepts (https://github.com/joshyattridge/smartmoneyconcepts), MIT. Berkas LICENSE: Copyright (c) 2020 NeuralNine. Repository commit 1b62fd6 diperiksa.
- Konsep ICT/SMC: deskripsi konseptual, bukan standar terukur.

## Informasi Lisensi
- Skill: MIT. Dependensi smartmoneyconcepts: MIT.
