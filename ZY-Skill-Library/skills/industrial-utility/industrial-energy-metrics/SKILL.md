---
name: industrial-energy-metrics
description: Compute power factor correction capacitor size in kvar and energy intensity in kWh per output unit for industrial energy management reviews.
license: MIT
compatibility: Python 3.9+ standard library only
metadata: {"category": "industrial-utility", "status": "verified", "owner": "zy"}
---

# industrial-energy-metrics

## Activation Triggers
- User meminta "kapasitor PFC", "power factor", "kvar", "kWh per unit", atau "intensitas energi".

## Scope dan Batas Kemampuan
- Dicakup: Qc untuk perbaikan PF dari kW dan PF awal/target, intensitas energi sederhana.
- TIDAK dicakup: desain bank kapasitor, harmonik, tarif listrik, dan audit energi lengkap.

## Required Tools
- Python 3.9+. `scripts/energy_metrics.py`

## Input dan Output Specification
Input: kW, PF awal, PF target; atau kWh dan output. Output JSON: qc_kvar, kwh_per_unit.

## Execution Workflow
1. Ambil kW rata-rata dan PF dari pengukuran. 2. Hitung Qc untuk PF target. 3. Bandingkan intensitas energi antar periode.

## Decision Rules
- PF target harus >= PF awal.
- Kapasitor perlu pemeriksaan harmonik dan resonansi sebelum pemasangan.

## Error Handling
- PF di luar (0,1] atau target < awal: ValueError, exit 2.

## Quality Control
- 100 kW dari PF 0.70 ke 0.95 membutuhkan 69.15 kvar.

## Acceptance Criteria
- Test EnergyTests lulus.

## Contoh Implementasi
```bash
python scripts/energy_metrics.py --kw 100 --pf1 0.70 --pf2 0.95
```

## Test Cases
`tests/skills/test_v05_custom.py` (EnergyTests).

## Referensi dan Sumber
- Rumus Qc = P (tan phi1 - tan phi2) (standar koreksi faktor daya).

## Informasi Lisensi
- Skill: MIT.
