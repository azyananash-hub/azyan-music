---
name: electrical-troubleshooting
description: Walk a fault-finding decision tree over measured values: each node tests one measurement against a threshold from the user's own procedure, and missing measurements stop the walk instead of guessing. Use for electrical fault diagnosis when measurements and SOP limits are available.
license: MIT
compatibility: Python 3.9+ standard library only
metadata: {"category": "engineering", "status": "verified", "owner": "zy"}
---

# electrical-troubleshooting

## Activation Triggers
- User meminta "troubleshooting listrik", "gangguan kelistrikan", "pohon keputusan", atau "cari penyebab gangguan".

## Scope dan Batas Kemampuan
- Dicakup: penelusuran pohon keputusan atas pengukuran yang sudah ada, dengan status NEED_MEASUREMENT jika data kurang.
- TIDAK dicakup: standar instalasi, keselamatan kerja listrik (ikuti SOP dan izin kerja), dan nilai batas standar.

## Required Tools
- Python 3.9+ standard library. `scripts/fault_tree.py`

## Input dan Output Specification
Input: tree.json (start, nodes) dan observations.json (nama pengukuran -> nilai). Output JSON: status (CAUSE, NEED_MEASUREMENT, ERROR), path, cause, action.

## Execution Workflow
1. Susun pohon dari SOP dan data pabrikan, dengan batas yang Anda tetapkan. 2. Ukur sesuai urutan yang diminta. 3. Jalankan penelusuran. 4. Lakukan tindakan hanya di bawah izin kerja.

## Decision Rules
- Batas (value) tidak boleh diisi dari perkiraan; kosongkan dan minta SOP.
- Jika pengukuran tidak ada, berhenti dan minta pengukuran; jangan menebak penyebab.

## Error Handling
- Simpul tidak ada, operator tak dikenal, atau pohon berputar: status ERROR.

## Quality Control
- Setiap jalur keputusan tercatat di path.

## Acceptance Criteria
- Tiga kombinasi pengukuran uji mencapai tiga penyebab berbeda; pengukuran yang hilang menghasilkan NEED_MEASUREMENT.

## Contoh Implementasi
```bash
python scripts/fault_tree.py tree.json observations.json
```

## Test Cases
`tests/skills/test_v07_batch1.py` (TroubleshootTests). Nilai batas dalam uji adalah nilai uji mesin penelusuran, bukan standar.

## Referensi dan Sumber
- Metode pohon keputusan diagnosis: rancangan internal; batas harus dari SOP pengguna.

## Informasi Lisensi
- Skill: MIT.
