---
name: jlpt-curriculum
description: Lint JLPT N5-N1 vocabulary datasets: required fields, level-to-file consistency, kana-only readings, duplicate word and reading pairs, and script mix per level. Ships the OpenJLPT CC BY-SA 4.0 vocabulary CSVs for curriculum counts. Use when building or validating Japanese curriculum data.
license: MIT
compatibility: Python 3.9+ standard library only
metadata: {"category": "japanese-education", "status": "verified", "owner": "zy", "classification": "CUSTOM"}
---

# jlpt-curriculum

## Activation Triggers
- User meminta "kurikulum JLPT", "validasi kosakata Jepang", "hitung kosakata per level", atau "cek data N5-N1".

## Scope dan Batas Kemampuan
- Dicakup: validasi CSV kosakata (format OpenJLPT), cakupan per level, jenis penulisan, dan bacaan kana.
- TIDAK dicakup: validasi tata bahasa, kanji di kalimat, furigana otomatis, dan penilaian kualitas arti.
- Level pada dataset bersumber dari daftar komunitas (lihat NOTICE.md), bukan daftar resmi Japan Foundation.

## Required Tools
- Python 3.9+ standard library. `scripts/jlpt_lint.py`. Data: `references/openjlpt/`.

## Input dan Output Specification
Input: folder berisi vocab-n1.csv sampai vocab-n5.csv (kolom id, word, reading, meanings, level). Output JSON: levels (entries, script, issues), total_entries, status.

## Execution Workflow
1. Jalankan `python scripts/jlpt_lint.py references/openjlpt`. 2. Periksa setiap isu per level. 3. Untuk data sendiri, gunakan kolom yang sama sebelum menjalankan lint.

## Decision Rules
- Bacaan bukan kana murni ditolak; perbaiki data, jangan melonggarkan aturan.
- Level yang tidak sesuai nama berkas harus diperiksa manual.

## Error Handling
- Kolom kosong, duplikat, atau level salah dilaporkan per baris. Tidak ada yang diperbaiki diam-diam.

## Quality Control
- Jumlah entri per level harus sama dengan jumlah baris berkas.

## Acceptance Criteria
- Dataset OpenJLPT (7.811 entri) lolos dengan 0 isu; fixture yang sengaja salah terdeteksi.

## Contoh Implementasi
```bash
python scripts/jlpt_lint.py references/openjlpt
```

## Test Cases
`tests/skills/test_v07_batch2.py` (JlptTests).

## Referensi dan Sumber
- OpenJLPT (https://github.com/evanclan/OpenJLPT, commit di references/openjlpt/SOURCE.md), CC BY-SA 4.0. Atribusi dan NOTICE.md wajib disertakan.

## Informasi Lisensi
- Kode skill: MIT. Data `references/openjlpt/`: CC BY-SA 4.0 (share-alike). Turunan data wajib CC BY-SA 4.0.
