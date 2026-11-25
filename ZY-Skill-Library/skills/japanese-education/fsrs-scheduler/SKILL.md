---
name: fsrs-scheduler
description: Schedule Japanese vocabulary and kanji reviews with the FSRS algorithm (Again/Hard/Good/Easy ratings) via the fsrs Python package. Use as a more accurate alternative to SM-2 for JLPT study tools such as AmiraVerse.
license: MIT
compatibility: Python 3.9+; fsrs (MIT, diuji 6.3.3)
metadata: {"category": "japanese-education", "status": "verified", "owner": "zy"}
---

# fsrs-scheduler

## Activation Triggers
- User meminta "FSRS", "jadwal review yang lebih akurat", atau integrasi penjadwal ke AmiraVerse.

## Scope dan Batas Kemampuan
- Dicakup: simulasi urutan review satu kartu dan due date berikutnya.
- TIDAK dicakup: penyimpanan database, optimasi parameter per pengguna, dan UI.

## Required Tools
- Python 3.9+, `fsrs` (MIT).
- `scripts/fsrs_review.py`

## Input dan Output Specification
Input: urutan rating 1-4 (1 Again, 2 Hard, 3 Good, 4 Easy). Output: state, due, interval_days per review.

## Execution Workflow
1. Muat state kartu dari penyimpanan aplikasi. 2. Panggil scheduler dengan rating user. 3. Simpan state dan due baru.

## Decision Rules
- Again harus menghasilkan interval lebih pendek daripada Good.
- Gunakan rating yang dijawab user, jangan menebak otomatis.

## Error Handling
- Rating di luar 1-4: ValueError, exit 2.

## Quality Control
- Dengan Good berturut-turut, interval harus naik.

## Acceptance Criteria
- Test FsrsTests lulus: interval Good naik; Again < Good.

## Contoh Implementasi
```bash
python scripts/fsrs_review.py 3 3 1 3
```

## Test Cases
`tests/skills/test_new_skills.py` (FsrsTests).

## Referensi dan Sumber
- FSRS: open-spaced-repetition (fsrs4anki MIT, LICENSE diverifikasi sebelumnya); paket `fsrs` MIT (metadata PyPI).

## Informasi Lisensi
- Skill: MIT. Dependensi fsrs: MIT.
