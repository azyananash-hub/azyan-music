---
name: instrument-loop-calc
description: Convert 4-20 mA transmitter signals to engineering values with NAMUR NE43 fault detection, and convert Pt100 resistance to temperature using Callendar-Van Dusen. Use for instrumentation loop checks and calibration.
license: MIT
compatibility: Python 3.9+ standard library only
metadata: {"category": "industrial-utility", "status": "verified", "owner": "zy"}
---

# instrument-loop-calc

## Activation Triggers
- User meminta "4-20 mA", "skala transmitter", "Pt100", "RTD", atau "kalibrasi loop".

## Scope dan Batas Kemampuan
- Dicakup: skala linier 4-20 mA, deteksi fault NE43 (3.6-21.0 mA), Pt100 T >= 0 C.
- TIDAK dicakup: termokopel, RTD selain Pt100, kompensasi lead, dan sinyal HART.

## Required Tools
- Python 3.9+. `scripts/loop_calc.py`

## Input dan Output Specification
Input: arus mA dengan LRV/URV, atau suhu C untuk Pt100. Output JSON: value, percent_of_span, fault_namur_ne43 / r_ohm.

## Execution Workflow
1. Pastikan LRV/URV sesuai konfigurasi transmitter. 2. Hitung nilai. 3. Tandai fault bila di luar 3.6-21.0 mA.

## Decision Rules
- Arus di luar 3.6-21.0 mA diperlakukan sebagai fault, bukan nilai proses.
- Pt100 di bawah 0 C membutuhkan persamaan lengkap (tidak tercakup).

## Error Handling
- URV = LRV, atau T < 0 C: ValueError, exit 2.

## Quality Control
- Pt100 100 C = 138.5055 ohm; invers mengembalikan 100 C.

## Acceptance Criteria
- Test LoopTests lulus.

## Contoh Implementasi
```bash
python scripts/loop_calc.py --ma 12 --lrv 0 --urv 100
python scripts/loop_calc.py --pt100-c 100
```

## Test Cases
`tests/skills/test_v05_custom.py` (LoopTests).

## Referensi dan Sumber
- NAMUR NE43 (batas fault 3.6 dan 21.0 mA; verifikasi dokumen NAMUR terbaru).
- IEC 60751 (konstanta Callendar-Van Dusen; verifikasi terhadap edisi standar).

## Informasi Lisensi
- Skill: MIT.
