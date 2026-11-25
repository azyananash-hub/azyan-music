---
name: scada-tag-engineering
description: Validate SCADA/HMI tag lists: unique names, naming pattern, analog and digital type rules, engineering ranges, ordered alarm limits within range, and unique device addresses. Use before commissioning or migrating a tag database.
license: MIT
compatibility: Python 3.9+ standard library only
metadata: {"category": "automation", "status": "verified", "owner": "zy"}
---

# scada-tag-engineering

## Activation Triggers
- User meminta "tag SCADA", "daftar tag", "alarm HI LO", "database tag HMI", atau "alamat Modbus tag".

## Scope dan Batas Kemampuan
- Dicakup: pemeriksaan konsistensi daftar tag (AI/AO/DI/DO), rentang engineering, batas alarm, dan alamat.
- TIDAK dicakup: konfigurasi vendor tertentu, desain layar HMI, dan kebijakan alarm operasi.

## Required Tools
- Python 3.9+ standard library. `scripts/tag_check.py`

## Input dan Output Specification
Input: JSON dengan name_pattern (opsional) dan tags. Output JSON: issues, status PASS/FAIL.

## Execution Workflow
1. Ekspor daftar tag dari sumber desain. 2. Jalankan lint. 3. Perbaiki issue. 4. Verifikasi alamat terhadap map perangkat.

## Decision Rules
- Nilai alarm LL/L/H/HH harus dari desain proses Anda, bukan dari skill.
- Pola nama dapat diganti lewat name_pattern sesuai standar penamaan proyek.

## Error Handling
- JSON rusak: exit 2. Setiap pelanggaran dicatat sebagai issue.

## Quality Control
- Setiap tag punya tipe yang dikenal dan nama unik.

## Acceptance Criteria
- Tag baik lulus; nama duplikat, alarm tak urut, dan alamat ganda terdeteksi.

## Contoh Implementasi
```bash
python scripts/tag_check.py tags.json
```

## Test Cases
`tests/skills/test_v07_batch1.py` (TagTests).

## Referensi dan Sumber
- Aturan konsistensi tag: rancangan internal dari praktik umum engineering SCADA.

## Informasi Lisensi
- Skill: MIT.
