---
name: ro-mass-balance
description: Compute ideal reverse osmosis mass balance (recovery, salt rejection, concentrate flow and TDS) from feed and permeate measurements. Use for water treatment plant (WTP/RO) checks and training.
license: original-zy
compatibility: Python 3.9+ standard library
metadata: {"category": "industrial-utility", "status": "verified", "owner": "zy"}
---

# ro-mass-balance

## Activation Triggers
- User meminta "RO", "reverse osmosis", "recovery", "rejection", atau "neraca massa WTP".

## Scope dan Batas Kemampuan
- Dicakup: neraca massa ideal RO (recovery, rejection, debit dan konsentrasi konsentrat).
- TIDAK dicakup: polarisasi konsentrasi, tekanan osmotik, fouling, dan desain membran (gunakan software vendor).

## Required Tools
- Python 3.9+ standard library.
- `scripts/ro_mass_balance.py`

## Input dan Output Specification
Input: Q_feed, C_feed, Q_perm, C_perm (m3/h, mg/L). Output JSON: recovery_pct, rejection_pct, q_concentrate, c_concentrate, salt_balance_error.

## Execution Workflow
1. Ambil data flow dan TDS dari sensor terkalibrasi.
2. Jalankan script.
3. Bandingkan recovery dengan batas membran vendor.

## Decision Rules
- Recovery tinggi meningkatkan risiko scaling: periksa batas vendor dan dosis antiscalant.
- Neraca garam harus tertutup; jika tidak, periksa data.

## Error Handling
- Input tidak masuk akal (q_perm >= q_feed atau c_perm >= c_feed): ValueError, exit 2.

## Quality Control
- Neraca garam: Q_f*C_f = Q_p*C_p + Q_c*C_c.

## Acceptance Criteria
- Qf 10, Cf 1000, Qp 5, Cp 20: recovery 50 %, rejection 98 %, Cc 1980 mg/L, error 0.

## Contoh Implementasi
```bash
python scripts/ro_mass_balance.py --q-feed 10 --c-feed 1000 --q-perm 5 --c-perm 20
```

## Test Cases
`tests/skills/test_custom_engineering.py` (IndustrialTests.test_ro_mass_balance).

## Referensi dan Sumber
- Neraca massa standar pada proses membran (dirumuskan ulang).

## Informasi Lisensi
- Skill: original-zy.
