# Progres ZY Skill Library

Terakhir diperbarui: 2026-11-25. Format: fase, status, bukti.

| Fase | Status | Bukti / catatan |
|---|---|---|
| 1. Inspeksi environment dan riset repository | Selesai (sebagian) | Repo kerja: `azyan-music` (Android/Kotlin, bukan Flutter). GitHub API di sesi hanya mengizinkan `azyan-music`; riset eksternal memakai pencarian web. Lihat `references/sources-and-licenses.md`. |
| 2. Audit lisensi, keamanan, kompatibilitas | Selesai (sebagian) | 9 repository terverifikasi lisensinya dari pencarian web; sisanya belum. Keputusan: tidak ada kode copyleft/ambigu yang disalin. |
| 3. Arsitektur library dan protokol global | Selesai | `MASTER_PROTOCOL.md`, `AGENTS.md`, `CLAUDE.md`, `references/platform-discovery.md` |
| 4. Akuisisi dan engineering skill | Sebagian | 9 skill validated. Kategori lain belum. |
| 5. Scripts, templates, integrasi | Selesai untuk skill validated | Script per skill, `templates/SKILL_TEMPLATE.md`, installer Claude Code. |
| 6. Testing dan benchmarking | Testing selesai; benchmark belum | `python -m unittest discover -s tests` (lihat hasil di `reports/quality-audit.md`). Benchmark belum dijalankan. |
| 7. Dokumentasi dan panduan instalasi | Selesai | `README.md`, `CHANGELOG.md`, dokumentasi per skill. |
| 8. Audit kualitas akhir | Selesai | `reports/quality-audit.md` |

## Backlog (belum dikerjakan, prioritas)
1. `engineering/load-flow` berbasis pandapower (BSD-3-Clause, terverifikasi). Perlu dependensi pandapower; putuskan apakah diizinkan.
2. `flutter/` untuk proyek AmiraVerse: quality gate `flutter analyze`/test, checklist Supabase RLS. Perlu proyek Flutter nyata di repository.
3. `japanese-education`: upgrade ke FSRS (MIT, terverifikasi).
4. `industrial-utility`: water treatment (RO) mass balance, cooling tower heat balance, dengan CoolProp (lisensi belum diverifikasi).
5. `automation`: Modbus client via pymodbus (lisensi belum diverifikasi), PLC ladder simulator sederhana (tanpa menyalin OpenPLC).
6. `creative-production`/`motion-graphics`: skill Remotion/Motion Canvas hanya setelah lisensi jelas (remotion-dev/skills ambigu).
7. `finance`: budgeting dan projection sederhana berbasis script.
8. `governance`: pengujian ulang setiap kali skill baru ditambahkan.

## Log keputusan utama
- 2026-11-25: Library dibuat sebagai subfolder `ZY-Skill-Library/` di repository ini, bukan repository baru, karena instruksi kerja mengharuskan bekerja di working directory.
- 2026-11-25: Standar Python tanpa dependensi pihak ketiga (zero unnecessary dependencies).
- 2026-11-25: Format discovery mengikuti Claude Code (`.claude/skills/<nama>/SKILL.md`).
- 2026-11-25: Remotion skills tidak disalin karena lisensi tidak jelas.
- 2026-11-25: vectorbt tidak direkomendasikan sebagai dependensi produk (Commons Clause).
