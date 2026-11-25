---
name: motor-starting-sizing
description: Compute three-phase motor full-load current and starting current for direct-on-line and star-delta starting from nameplate power, voltage, PF, efficiency and LRC ratio. Use for motor control and starter selection checks.
license: MIT
compatibility: Python 3.9+ standard library only
metadata: {"category": "engineering", "status": "verified", "owner": "zy"}
---

# motor-starting-sizing

## Activation Triggers
- User meminta "FLC motor", "arus start", "star-delta", atau "pemilihan starter".

## Scope dan Batas Kemampuan
- Dicakup: FLC, arus start DOL, dan arus start star-delta berdasarkan rasio nameplate.
- TIDAK dicakup: dinamika torsi-kecepatan beban, soft starter, VFD, dan proteksi motor detail.

## Required Tools
- Python 3.9+. `scripts/motor_calc.py`

## Input dan Output Specification
Input: kW, V, PF, efisiensi (0-1], LRC/FLC dari nameplate. Output JSON: flc_a, dol_start_current_a, star_delta_start_current_a, star_delta_torque_ratio.

## Execution Workflow
1. Ambil data nameplate motor. 2. Hitung FLC dan arus start. 3. Periksa apakah drop tegangan saat start diterima sistem (di luar skill ini).

## Decision Rules
- Rasio LRC/FLC harus dari nameplate; jangan diasumsikan.
- Star-delta mengurangi arus dan torsi start ke sepertiga; pastikan torsi beban mencukupi.

## Error Handling
- Input tidak valid atau LRC <= 1: ValueError, exit 2.

## Quality Control
- 75 kW, 400 V, PF 0.85, eta 0.93: FLC 136.92 A.

## Acceptance Criteria
- Test MotorTests lulus.

## Contoh Implementasi
```bash
python scripts/motor_calc.py --kw 75 --v 400 --pf 0.85 --eta 0.93 --lrc-ratio 7
```

## Test Cases
`tests/skills/test_v05_custom.py` (MotorTests).

## Referensi dan Sumber
- Relasi FLC dan star-delta (dirumuskan ulang dari prinsip motor induksi).

## Informasi Lisensi
- Skill: MIT.
