---
name: compound-savings-projection
description: Project savings growth with monthly contributions and compound interest across several return scenarios, reporting contributions and return-driven growth. Use for personal budgeting and savings planning; not investment advice.
license: MIT
compatibility: Python 3.9+ standard library
metadata: {"category": "finance", "status": "verified", "owner": "zy"}
---

# compound-savings-projection

## Activation Triggers
- User meminta "proyeksi tabungan", "compound interest", "bunga majemuk", atau "berapa tabungan saya di tahun ke-N".

## Scope dan Batas Kemampuan
- Dicakup: nilai masa depan dengan kontribusi bulanan dan bunga majemuk bulanan, untuk satu asumsi return per skenario.
- TIDAK dicakup: pajak, inflasi (kecuali bila return riil dimasukkan), volatilitas, nasihat investasi, dan jaminan return.

## Required Tools
- Python 3.9+ standard library.
- `scripts/savings_projection.py`

## Input dan Output Specification
Input: initial, monthly, annual-rate (%), years. Output JSON: future_value, total_contributed, growth_from_returns, assumption.

## Execution Workflow
1. Tanyakan tujuan dan horizon.
2. Jalankan beberapa skenario return (mis. 0 %, 3 %, 6 %) dan tampilkan semuanya.
3. Laporkan asumsi di setiap hasil.

## Decision Rules
- Jangan menyajikan satu skenario sebagai kepastian.
- Gunakan return riil (setelah inflasi) bila user ingin daya beli.

## Error Handling
- Nilai negatif atau years di luar 1..100: ValueError, exit 2.

## Quality Control
- Kasus 0 % harus sama dengan kontribusi total.

## Acceptance Criteria
- 100/bulan, 12 %/tahun, 1 tahun: 1268.25; 0 %, 10 tahun: 12000.

## Contoh Implementasi
```bash
python scripts/savings_projection.py --monthly 100 --annual-rate 12 --years 1
```

## Test Cases
`tests/skills/test_custom_engineering.py` (IndustrialTests.test_savings_closed_form).

## Referensi dan Sumber
- Rumus bunga majemuk dan anuitas standar (dirumuskan ulang).

## Informasi Lisensi
- Skill: MIT. Bukan nasihat keuangan.
