---
name: skill-engineering-standard
description: Author, review, and validate ZY Skill Library skills against the 13-section engineering standard (triggers, scope, workflow, decision rules, error handling, QC, acceptance criteria, tests, sources, license). Use when creating a new skill, editing an existing SKILL.md, or checking that the library passes validation before a commit.
license: original-zy
compatibility: Python 3.9+ standard library only; expects the ZY Skill Library repository layout
metadata: {"category": "governance", "status": "verified", "owner": "zy"}
---

# Skill Engineering Standard

## Activation Triggers
- User meminta "buat skill baru", "review skill", "perbaiki SKILL.md", atau "validasi library".
- Sebelum commit perubahan di folder `skills/`.
- Saat menambahkan script, template, atau reference ke sebuah skill.

## Scope dan Batas Kemampuan
- Dicakup: struktur SKILL.md, frontmatter, 13 section wajib, referensi script, sinkronisasi registry, dan checklist kualitas.
- TIDAK dicakup: menilai kualitas isi domain (mis. kebenaran rumus teknik). Itu tanggung jawab reviewer domain.
- Skill tanpa mekanisme penerapan (hanya teori) dianggap tidak lulus standar.

## Required Tools
- Python 3.9+.
- Dari root library: `scripts/validate_library.py`, `scripts/build_registry.py`, `scripts/install_skills.py`.
- `tests/` (unittest) dari root library.

## Input dan Output Specification
Input: folder skill baru atau SKILL.md yang diubah.
Output: daftar error/warning dari validator; registry JSON yang sinkron; laporan ringkas perubahan.

Frontmatter wajib (satu baris per key):
```yaml
---
name: nama-folder-sama-persis        # kebab-case, <= 64 karakter
description: Kalimat yang menjelaskan apa dan kapan dipakai.   # <= 1024 karakter, satu baris
license: MIT | Apache-2.0 | original-zy | ...
---
```

Section wajib (`## Judul` persis):
1. Activation Triggers
2. Scope dan Batas Kemampuan
3. Required Tools
4. Input dan Output Specification
5. Execution Workflow
6. Decision Rules
7. Error Handling
8. Quality Control
9. Acceptance Criteria
10. Contoh Implementasi
11. Test Cases
12. Referensi dan Sumber
13. Informasi Lisensi

## Execution Workflow
1. Salin `templates/SKILL_TEMPLATE.md` ke `skills/<kategori>/<nama>/SKILL.md`.
2. Isi frontmatter. Nama folder dan `name` harus identik.
3. Tulis section. Setiap "Execution Workflow" harus memuat langkah yang bisa dijalankan, bukan teori.
4. Tambahkan script di `scripts/` dalam folder skill bila ada mekanisme komputasi, dan referensikan path relatif `scripts/<nama>.py` di SKILL.md.
5. Tulis unit test di `tests/` dan rujuk di section "Test Cases".
6. Jalankan `python scripts/validate_library.py` lalu `python scripts/build_registry.py`.
7. Jalankan `python -m unittest discover -s tests` dari root library.
8. Catat perubahan di `CHANGELOG.md`.

## Decision Rules
- Bila skill membutuhkan dependensi pihak ketiga, nyatakan di `compatibility` dan pertimbangkan standard library dulu (zero unnecessary dependencies).
- Bila sumber berlisensi copyleft kuat (GPL/AGPL), jangan menyalin kode; tulis ulang dari rumus/metode dan catat sumbernya.
- Bila ada keraguan lisensi, set status skill ke tidak tervalidasi dan jangan distribusikan.
- Bila skill menyentuh keselamatan (listrik, industri, keuangan), wajib ada batas cakupan dan disclaimer di section Scope.

## Error Handling
- Validator menampilkan `ERROR` (menggagalkan) dan `WARNING` (tidak menggagalkan).
- Registry tidak sinkron: jalankan `build_registry.py`, lalu validasi ulang.
- Script yang direferensikan tidak ada: perbaiki path atau hapus referensi.

## Quality Control
- Skill lulus bila `validate_library.py` tidak memberi ERROR untuk skill tersebut.
- Setiap script memiliki minimal satu test yang berjalan.
- Tidak ada angka contoh yang dikarang; setiap angka acceptance dihitung ulang dengan script.

## Acceptance Criteria
- `python scripts/validate_library.py` keluar dengan kode 0.
- `python scripts/build_registry.py --check` menyatakan registry sinkron.
- Semua test di `tests/` lulus.

## Contoh Implementasi
```bash
cd ZY-Skill-Library
python scripts/validate_library.py
python scripts/build_registry.py
python -m unittest discover -s tests -v
```

## Test Cases
Lihat `tests/test_validate_library.py` (validator menolak nama tidak cocok, section hilang, dan frontmatter rusak).

## Referensi dan Sumber
- Format SKILL.md mengikuti konvensi Claude Code (folder `skills/<nama>/SKILL.md` dengan frontmatter `name` dan `description`). Lihat `references/platform-discovery.md` di root library.
- Ide struktur progressive disclosure dan konvensi SKILL.md terinspirasi dari repo anthropics/skills (lisensi per-skill, periksa LICENSE.txt tiap skill sebelum menyalin apa pun). Tidak ada file dari repo itu yang disalin.

## Informasi Lisensi
- Standar dan validator: `original-zy`.
