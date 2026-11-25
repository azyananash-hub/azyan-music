---
name: steam-water-properties
description: Look up saturation temperature, saturated liquid and vapour enthalpy of water at a given pressure using CoolProp. Use for steam system and boiler property checks in industrial utility work.
license: MIT
compatibility: Python 3.9+; CoolProp (MIT, diuji 8.1.0)
metadata: {"category": "industrial-utility", "status": "verified", "owner": "zy"}
---

# steam-water-properties

## Activation Triggers
- User meminta "tekanan jenuh", "saturation temperature", "entalpi uap", "steam table", atau "hfg air".

## Scope dan Batas Kemampuan
- Dicakup: Tsat, hf, hg, hfg air pada tekanan 0.6-22000 kPa (jenuh).
- TIDAK dicakup: kondisi superheated, campuran non-air, dan desain sistem uap.

## Required Tools
- Python 3.9+, `CoolProp` (MIT).
- `scripts/steam_props.py`

## Input dan Output Specification
Input: tekanan (kPa). Output JSON: t_sat_c, hf_kj_kg, hg_kj_kg, hfg_kj_kg.

## Execution Workflow
1. Pastikan tekanan absolut (bukan gauge). 2. Jalankan `python scripts/steam_props.py --p-kpa 1000`. 3. Bandingkan dengan tabel uap standar bila untuk laporan.

## Decision Rules
- Tekanan gauge harus dikonversi ke absolut sebelum dihitung.
- Untuk keselamatan boiler/bejana tekan, ikuti SOP dan kode desain; skill ini hanya pembanding properti.

## Error Handling
- Tekanan di luar rentang: ValueError, exit 2.

## Quality Control
- Bandingkan dengan NIST steam tables: 101.325 kPa -> 99.974 C; 1000 kPa -> 179.88 C.

## Acceptance Criteria
- Test `tests/skills/test_new_skills.py` (SteamTests) lulus terhadap nilai NIST.

## Contoh Implementasi
```bash
python scripts/steam_props.py --p-kpa 1000
```

## Test Cases
`tests/skills/test_new_skills.py` (SteamTests): acuan NIST dan validasi rentang.

## Referensi dan Sumber
- CoolProp: https://github.com/CoolProp/CoolProp (MIT; diverifikasi dari metadata PyPI).
- Nilai acuan: NIST steam tables (nilai dicocokkan dari ingatan referensi publik; verifikasi ulang untuk laporan resmi).

## Informasi Lisensi
- Skill: MIT. Dependensi CoolProp: MIT.
