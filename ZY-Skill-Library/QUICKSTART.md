# QUICKSTART: ZY Skill Library

Persyaratan: Python 3.9+. Tidak ada dependensi wajib untuk router, importer, dan validator.

## 1. Mengaktifkan library
Library ini tidak aktif otomatis. Pasang skill ke folder discovery platform Anda:
```bash
python scripts/install_skills.py --list
python scripts/install_skills.py --target ~/.claude/skills            # dry-run
python scripts/install_skills.py --target ~/.claude/skills --apply    # menyalin
```
Di Windows: `scripts\install_windows.ps1` (tidak diuji di Windows). Lokasi folder adalah konvensi Claude Code yang tercatat di `references/platform-discovery.md`.

## 2. Menggunakan skill
Cari skill yang relevan dari registry, tanpa memuat seluruh library:
```bash
python scripts/route_skill.py "hitung arus hubung singkat 11 kV" --top 3
```
Kemudian baca hanya `SKILL.md` dari path yang dikembalikan. Muat `scripts/` atau `references/` hanya jika workflow membutuhkannya. Router mengembalikan kosong bila tidak ada skill yang relevan; jangan memaksakan skill.

## 3. Menambahkan skill buatan sendiri
Sumber boleh berupa file `SKILL.md`, folder, ZIP, atau URL GitHub publik. Lisensi wajib dinyatakan:
```bash
python scripts/import_personal.py ./skill-saya --category ai-agents --license MIT --label "ChatGPT"
```
Importer menolak: frontmatter tidak valid, risiko HIGH, dan nama yang sudah ada dengan isi berbeda. Menimpa skill lama membutuhkan `--approve-overwrite`; versi lama diarsipkan di `research/skill-versions/`. Setelah impor, registry diperbarui otomatis.

## 4. Memperbarui library
```bash
git pull
python scripts/build_registry.py
python scripts/validate_library.py
```

## 5. Menonaktifkan skill bermasalah
- Di mesin Anda: hapus folder skill dari target instalasi (mis. `~/.claude/skills/<nama>`). Ini tidak mengubah library.
- Di library: hapus folder `skills/<kategori>/<nama>`, catat di `CHANGELOG.md`, lalu jalankan `python scripts/build_registry.py`.

## Platform: apa yang sudah terverifikasi
| Platform | Status | Catatan |
|---|---|---|
| Claude Code (terminal) | Installer dan router diuji di sandbox | Pemuatan otomatis di sesi Claude Code belum diuji langsung. |
| Claude Chat | NOT VERIFIED | Tidak ada bukti dalam sesi ini bahwa Claude Chat memuat folder skill. Unggah manual belum dicoba. |
| Codex | NOT VERIFIED | Dokumentasi resmi tidak terjangkau dari sesi ini. Jangan anggap jalur tertentu benar tanpa mengeceknya. |
| Android (cloud) | NOT VERIFIED | Tidak diuji. Tidak ada klaim kemampuan untuk perangkat ini. |

Tidak ada klaim instalasi global atau sinkronisasi lintas platform. Keduanya membutuhkan langkah dari Anda dan belum dibuktikan.

## Hasil benchmark
Lihat `benchmarks/RESULTS.md`. Yang terukur: perhitungan skill terhadap label dan ketepatan router pada kueri berlabel. A/B dengan-dan-tanpa skill belum dijalankan.
