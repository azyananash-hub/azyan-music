---
name: cooling-tower-performance
description: Compute cooling tower range, approach, effectiveness, heat load and rule-of-thumb evaporation from water temperatures and flow. Use for utility-side performance checks of cooling towers in industrial plants.
license: original-zy
compatibility: Python 3.9+ standard library
metadata: {"category": "industrial-utility", "status": "verified", "owner": "zy"}
---

# cooling-tower-performance

## Activation Triggers
- User meminta "cooling tower", "range", "approach", "effectiveness", atau "beban panas menara pendingin".

## Scope dan Batas Kemampuan
- Dicakup: range, approach, efektivitas, beban panas dari suhu dan debit, serta estimasi evaporasi (aturan praktis).
- TIDAK dicakup: drift, blowdown, desain fill/fan, dan kondisi udara non-standar.

## Required Tools
- Python 3.9+ standard library.
- `scripts/cooling_tower.py`

## Input dan Output Specification
Input: T_hot_in, T_cold_out, T_wetbulb (C), debit (m3/h). Output JSON: range_c, approach_c, effectiveness_pct, heat_load_kw, evaporation_m3_h_estimate.

## Execution Workflow
1. Ukur suhu air masuk/keluar dan wet-bulb pada waktu yang sama.
2. Jalankan script.
3. Bandingkan efektivitas dengan data desain vendor.

## Decision Rules
- cold_out di bawah wet-bulb: tolak (secara fisik tidak mungkin).
- Evaporasi hanya estimasi; gunakan data makeup water bila tersedia.

## Error Handling
- Input di luar rentang wajar atau urutan suhu salah: ValueError, exit 2.

## Quality Control
- range = hot_in - cold_out; approach = cold_out - wetbulb; efektivitas = range / (hot_in - wetbulb).

## Acceptance Criteria
- 35/25 C, wet-bulb 22 C, 360 m3/h: range 10, approach 3, efektivitas 76.92 %, beban 4186 kW.

## Contoh Implementasi
```bash
python scripts/cooling_tower.py --t-hot-in 35 --t-cold-out 25 --t-wetbulb 22 --flow-m3-h 360
```

## Test Cases
`tests/skills/test_custom_engineering.py` (IndustrialTests.test_cooling_tower_*).

## Referensi dan Sumber
- Definisi range/approach/effectiveness dirumuskan ulang dari konvensi umum menara pendingin.
- Aturan 1 % per 6 C range untuk evaporasi adalah aturan praktis; belum diverifikasi terhadap sumber primer.

## Informasi Lisensi
- Skill: original-zy.
