---
name: transformer-rating-regulation
description: Compute transformer rated current and approximate voltage regulation from kVA, line voltage, impedance percent, X/R and power factor. Use for transformer sizing checks and load studies.
license: MIT
compatibility: Python 3.9+ standard library only
metadata: {"category": "engineering", "status": "verified", "owner": "zy"}
---

# transformer-rating-regulation

## Activation Triggers
- User meminta "arus nominal trafo", "regulasi tegangan", "impedansi trafo", atau "kapasitas trafo".

## Scope dan Batas Kemampuan
- Dicakup: arus nominal, komponen R% dan X%, regulasi pendekatan untuk beban lagging.
- TIDAK dicakup: tap changer, beban leading, harmonik, dan rugi inti.

## Required Tools
- Python 3.9+. `scripts/transformer_calc.py`

## Input dan Output Specification
Input: kVA, V line-to-line, Z%, X/R, PF. Output JSON: i_rated_a, r_pct, x_pct, voltage_regulation_pct.

## Execution Workflow
1. Ambil data nameplate (kVA, V, Z%, X/R). 2. Jalankan script dengan PF beban. 3. Bandingkan regulasi dengan batas yang disepakati.

## Decision Rules
- Gunakan nilai nameplate, bukan asumsi.
- Regulasi adalah pendekatan; untuk desain gunakan perhitungan lengkap.

## Error Handling
- Nilai nol/negatif atau PF di luar (0,1]: ValueError, exit 2.

## Quality Control
- Arus nominal 1000 kVA pada 20 kV = 28.868 A.

## Acceptance Criteria
- Test TransformerTests lulus: arus 28.868 A dan regulasi 4.0597 % pada PF 0.8.

## Contoh Implementasi
```bash
python scripts/transformer_calc.py --kva 1000 --v-ll 20000 --z-percent 6 --xr 10 --pf 0.8
```

## Test Cases
`tests/skills/test_v05_custom.py` (TransformerTests).

## Referensi dan Sumber
- Rumus arus nominal dan regulasi pendekatan (formula standar teknik tenaga; dirumuskan ulang).

## Informasi Lisensi
- Skill: MIT.
