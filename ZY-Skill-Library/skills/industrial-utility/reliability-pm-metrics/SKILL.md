---
name: reliability-pm-metrics
description: Compute inherent availability from MTBF and MTTR, and Weibull reliability at a given time from fitted scale and shape parameters. Use for preventive maintenance planning and asset reliability reviews.
license: MIT
compatibility: Python 3.9+ standard library only
metadata: {"category": "industrial-utility", "status": "verified", "owner": "zy"}
---

# reliability-pm-metrics

## Activation Triggers
- User meminta "availability", "MTBF", "MTTR", "Weibull", atau "interval preventive maintenance".

## Scope dan Batas Kemampuan
- Dicakup: availability inherent dan reliabilitas Weibull pada satu titik waktu.
- TIDAK dicakup: fitting Weibull dari data (butuh alat statistik), biaya PM, dan optimasi interval.

## Required Tools
- Python 3.9+. `scripts/reliability.py`

## Input dan Output Specification
Input: MTBF dan MTTR (jam), atau t, eta, beta. Output JSON: availability, weibull_reliability.

## Execution Workflow
1. Hitung MTBF/MTTR dari catatan kegagalan. 2. Jika memakai Weibull, fit eta dan beta dari data dulu. 3. Gunakan hasil untuk membandingkan opsi PM.

## Decision Rules
- Parameter Weibull harus hasil fitting data, bukan tebakan.
- beta > 1 menunjukkan pola wear-out; hanya gunakan PM berbasis waktu bila pola itu benar.

## Error Handling
- MTBF <= 0 atau parameter non-positif: ValueError, exit 2.

## Quality Control
- MTBF 100 h dan MTTR 2 h menghasilkan availability 0.980392.

## Acceptance Criteria
- Test ReliabilityTests lulus.

## Contoh Implementasi
```bash
python scripts/reliability.py --mtbf 100 --mttr 2
python scripts/reliability.py --t 1000 --eta 1000 --beta 2.5
```

## Test Cases
`tests/skills/test_v05_custom.py` (ReliabilityTests).

## Referensi dan Sumber
- Definisi availability inherent dan fungsi Weibull (standar analisis keandalan).

## Informasi Lisensi
- Skill: MIT.
