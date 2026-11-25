---
name: industrial-digital-twin
description: Build a first-order thermal digital twin (C dT/dt = P - (T - Tamb)/R) with an analytic solution, steady state, time constant, and a stability-checked Euler simulation for comparing measured and modeled temperatures. Use for equipment thermal behavior studies and twin prototyping.
license: MIT
compatibility: Python 3.9+ standard library only
metadata: {"category": "industrial-utility", "status": "verified", "owner": "zy"}
---

# industrial-digital-twin

## Activation Triggers
- User meminta "digital twin", "model termal", "time constant", "steady state", atau "simulasi suhu peralatan".

## Scope dan Batas Kemampuan
- Dicakup: model termal satu node orde satu, solusi analitik, simulasi Euler dengan batas stabilitas.
- TIDAK dicakup: model multi-node, sinkronisasi data real-time, dan kalibrasi otomatis dari data.

## Required Tools
- Python 3.9+ standard library. `scripts/twin_rc.py`

## Input dan Output Specification
Fungsi: analytic(t, P, R, C, Tamb), simulate_euler(t_end, dt, P, R, C, Tamb), steady_state(P, R, Tamb). R dalam K/W, C dalam J/K, P dalam W.

## Execution Workflow
1. Ukur R dan C dari uji langkah (step test) alat. 2. Bandingkan kurva simulasi dengan data. 3. Gunakan solusi analitik untuk verifikasi, Euler untuk kasus variabel.

## Decision Rules
- R dan C harus dari pengukuran, bukan tebakan.
- dt harus <= 0.1 tau; jika tidak, simulasi ditolak.

## Error Handling
- Parameter nol/negatif atau dt tidak stabil: ValueError.

## Quality Control
- Pada t = tau, respons mencapai 63.2 % dari kenaikan akhir.

## Acceptance Criteria
- R=2, C=50, P=10, Tamb=25: pada t=100 s suhu 37.6424 C; Euler dengan dt=1 s berada dalam 0.5 C dari analitik.

## Contoh Implementasi
```python
from twin_rc import analytic
print(analytic(100, 10, 2, 50, 25))
```

## Test Cases
`tests/skills/test_v07_batch1.py` (TwinTests).

## Referensi dan Sumber
- Model RC termal orde satu adalah analogi listrik standar; diimplementasikan ulang.

## Informasi Lisensi
- Skill: MIT.
