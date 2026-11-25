---
name: novel-typesetting
description: Check a novel manuscript for chapter headings in order, empty chapters, and word or character counts per chapter, then export a DOCX with one Heading 1 per chapter. Use when preparing a manuscript draft for review or typesetting handoff.
license: MIT
compatibility: Python 3.9+; python-docx
metadata: {"category": "office-documents", "status": "verified", "owner": "zy", "classification": "CUSTOM"}
---

# novel-typesetting

## Activation Triggers
- User meminta "naskah novel", "format bab", "jumlah kata per bab", atau "ekspor naskah ke DOCX".

## Scope dan Batas Kemampuan
- Dicakup: struktur bab, hitungan kata atau karakter, dan ekspor DOCX dengan judul bab.
- TIDAK dicakup: tata letak cetak (margin, font, widow/orphan), tipografi Jepang vertikal, dan ISBN.

## Required Tools
- Python 3.9+; python-docx. `scripts/manuscript_check.py`

## Input dan Output Specification
Input: txt dengan baris 'Bab N' atau 'Chapter N' sebagai judul. Opsi --mode words|chars, --min, --docx. Output JSON: chapters, issues, warnings, status.

## Execution Workflow
1. Tulis naskah dengan judul bab konsisten. 2. Jalankan check dengan mode yang sesuai bahasa. 3. Ekspor DOCX untuk review. 4. Lakukan penataan cetak di aplikasi penata letak.

## Decision Rules
- Untuk bahasa Jepang gunakan mode chars karena tidak ada spasi antar kata.
- Nomor bab harus berurutan; lompatan berarti ada bab hilang.

## Error Handling
- Teks sebelum bab pertama: ValueError. Berkas tidak ada: exit 2.

## Quality Control
- Nomor bab berurutan dan tidak ada bab kosong.

## Acceptance Criteria
- Naskah dua bab menghasilkan 6 dan 3 kata; ekspor DOCX mempertahankan dua heading bab.

## Contoh Implementasi
```bash
python scripts/manuscript_check.py naskah.txt --mode chars --docx naskah.docx
```

## Test Cases
`tests/skills/test_v07_batch2.py` (NovelTests).

## Referensi dan Sumber
- python-docx (MIT) untuk ekspor. Lihat juga skill docx (upstream) untuk pengeditan DOCX lanjutan.

## Informasi Lisensi
- Skill: MIT.
