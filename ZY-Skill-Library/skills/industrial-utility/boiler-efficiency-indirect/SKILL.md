---
name: boiler-efficiency-indirect
description: Estimate boiler efficiency with the indirect heat-loss method (Siegert dry flue gas loss plus radiation and other losses). Use for utility boiler performance screening and loss breakdown.
license: MIT
compatibility: Python 3.9+ standard library
metadata: {"category": "industrial-utility", "status": "verified", "owner": "zy"}
---

# boiler-efficiency-indirect

## Activation Triggers
- User meminta "efisiensi boiler", "indirect method", "heat loss", atau "rugi gas buang".

## Scope dan Batas Kemampuan
- Dicakup: efisiensi metode tidak langsung dari rugi gas buang (Siegert disederhanakan) dan rugi lain yang diinput.
- TIDAK dicakup: metode langsung (input-output), instruksi operasi, dan uji formal (ASME PTC 4 / BS EN 12952).

## Required Tools
- Python 3.9+ standard library.
- `scripts/boiler_efficiency.py`

## Input dan Output Specification
Input: suhu gas buang, suhu ambien, CO2 kering (%), jenis bahan bakar, rugi radiasi/moisture/H2/unburnt (%). Output JSON: efficiency_pct, total_losses_pct, losses_pct.

## Execution Workflow
1. Ukur gas buang dengan analyzer yang terkalibrasi.
2. Masukkan data ke script.
3. Bandingkan dengan target desain dan SOP pabrik.

## Decision Rules
- Konstanta K bahan bakar adalah perkiraan; untuk laporan resmi gunakan data fuel analysis dan standar yang berlaku.
- Jangan memberi instruksi pengoperasian boiler; arahkan ke SOP.

## Error Handling
- Input di luar rentang atau total rugi >= 100 %: ValueError, exit 2.

## Quality Control
- Efisiensi = 100 - total rugi.
- Rugi gas buang = K (T_flue - T_amb) / CO2.

## Acceptance Criteria
- T_flue 180 C, ambien 30 C, CO2 10 %, gas alam: rugi gas buang 5.7 %; efisiensi 93.8 % dengan radiasi 0.5 %.

## Contoh Implementasi
```bash
python scripts/boiler_efficiency.py --t-flue 180 --t-ambient 30 --co2 10 --fuel natural_gas --radiation-pct 0.5
```

## Test Cases
`tests/skills/test_custom_engineering.py` (IndustrialTests.test_boiler_*).

## Referensi dan Sumber
- Metode Siegert untuk rugi gas buang (formula umum; nilai K perkiraan, belum diverifikasi terhadap tabel pabrikan).
- ASME PTC 4 / BS EN 12952 sebagai rujukan uji formal (belum diakses).

## Informasi Lisensi
- Skill: MIT.
