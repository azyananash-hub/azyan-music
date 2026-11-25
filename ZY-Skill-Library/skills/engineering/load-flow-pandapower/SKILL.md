---
name: load-flow-pandapower
description: Run AC power flow (Newton-Raphson) on small distribution or industrial networks from a JSON description using pandapower, reporting bus voltages, slack power, line losses and a power-balance check. Use for preliminary load flow studies.
license: MIT
compatibility: Python 3.9+; pandapower (BSD-3-Clause)
metadata: {"category": "engineering", "status": "verified", "owner": "zy"}
---

# Load Flow (pandapower)

## Activation Triggers
- User meminta "load flow", "aliran daya", "tegangan bus", "rugi daya", atau "power flow".
- Studi awal jaringan distribusi/industri dengan beberapa bus dan saluran.

## Scope dan Batas Kemampuan
- Dicakup: AC power flow Newton-Raphson untuk jaringan kecil via JSON, hasil tegangan, aliran slack, rugi saluran, dan cek neraca daya.
- TIDAK dicakup: hubung singkat (pakai short-circuit-calculator), transformator tap detail, kontrol OLTC, stabilitas transien, dan jaringan besar tanpa validasi data.

## Required Tools
- Python 3.9+ dengan `pandapower` (BSD-3-Clause; diuji dengan 3.5.6). Opsional `numba` untuk kecepatan (hanya warning bila tidak ada).
- `scripts/load_flow.py`

## Input dan Output Specification
Input: file JSON (lihat docstring script): `ext_grid`, `buses`, `lines` (panjang km, R/X per km), `loads` (MW, Mvar).
Output JSON: `converged`, `bus_vm_pu`, `slack_p_mw`, `load_p_mw`, `line_losses_p_mw`, `power_balance_error_mw`, `line_loading_pct`. Exit 0 bila konvergen, 3 bila tidak, 2 input salah.

## Execution Workflow
1. Siapkan data nyata: impedansi saluran dari datasheet kabel, beban dari pengukuran.
2. Simpan sebagai JSON, lalu jalankan `python scripts/load_flow.py jaringan.json`.
3. Periksa `converged` dan `power_balance_error_mw` (harus mendekati 0).
4. Bandingkan `bus_vm_pu` dengan batas tegangan standar (mis. ±5% atau sesuai grid code setempat).

## Decision Rules
- Jika tidak konvergen, jangan melaporkan hasil; periksa data (impedansi terlalu besar, beban tidak realistis).
- Jika `line_loading_pct` > 100, tandai saluran overload.
- Jika data impedansi tidak diketahui, minta data; jangan mengarang.

## Error Handling
- JSON rusak atau kunci hilang: exit 2 dengan pesan.
- Non-konvergen: exit 3.

## Quality Control
- Neraca daya: slack P = beban P + rugi P (toleransi 1e-4 MW).
- Tanpa beban, tegangan semua bus = 1.0 pu.

## Acceptance Criteria
- Dua bus 20 kV, saluran 2 km, beban 2 MW + 0.8 Mvar: konvergen, V_load < 1.0, neraca tertutup.
- Tanpa beban: V = 1.0 pu.

## Contoh Implementasi
```bash
python scripts/load_flow.py examples/two_bus.json
```

## Test Cases
`tests/skills/test_custom_engineering.py` (LoadFlowTests): balance & voltage drop, no-load flat profile, CLI error pada JSON salah.

## Referensi dan Sumber
- pandapower: https://github.com/e2nIEE/pandapower (BSD-3-Clause, terverifikasi lewat pencarian web; lihat references/sources-and-licenses.md).

## Informasi Lisensi
- Skill: MIT. Dependensi pandapower: BSD-3-Clause.
