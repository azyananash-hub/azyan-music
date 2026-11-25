# QUICKSTART: ZY Skill Library

**Status:** v0.7.0 · 115 skill · dibekukan pada commit `7039fed` (baseline historis `1b326d2`).
**Batasan dan pekerjaan belum selesai:** lihat [research/BACKLOG-V0.8.md](research/BACKLOG-V0.8.md).

## 1. Akses read-only dari proyek lain (tanpa menyalin skill)

```bash
git clone --depth 1 -b ccr-57e40ec8-e8i3fa https://github.com/azyananash-hub/azyan-music ~/zy-lib
L=~/zy-lib/ZY-Skill-Library
python $L/scripts/route_skill.py "tugas Anda" --top 3
```

- Router hanya membaca `SKILL_REGISTRY.json` dan menampilkan path. Tidak ada skill yang disalin ke proyek Anda.
- Akses lintas proyek dilaporkan berhasil pada uji nyata EarthStop. Izin Claude Code untuk membaca folder di luar direktori kerja tetap mengikuti pengaturan Anda.

## 2. Memilih skill

```bash
python $L/scripts/route_skill.py "<tugas>" [--project <id>] [--brief "<teks brief>"] [--top 3]
```

Keluaran per skill: skor, nama, klasifikasi/status, path `SKILL.md`, ukuran `SKILL.md`, jumlah `scripts` dan `references`.
Keluaran kosong berarti tidak ada skill yang relevan. Jangan memaksakan skill.

Id proyek yang tersedia (`references/project-profiles.json`):
`amiraverse`, `clipacanvas`, `deamira`, `earthstop`, `film-sinematik`, `jlpt`, `money-app`, `novel`,
`silent-neon-tokyo-game`, `silent-neon-tokyo-manhwa`, `sisi-gelap-tokoh`, `teknik-elektro`, `xauusd`, `zii`.
Profil menaikkan skor kategori yang disukai proyek.

## 3. Contextual override dan konflik

Batasan skill ada di `references/skill-constraints.json` (saat ini: `cinematic-camera`, `terminal-inserts`, `article-highlights` melarang neon dan glow). Router memberi catatan bila brief memakai kata terlarang:

- `KONFLIK:` brief bertentangan dengan batasan skill. Tanyakan, atau pilih profil proyek yang punya override.
- `OVERRIDE (<proyek>):` hanya jika `references/project-profiles.json` menyatakannya. Saat ini hanya EarthStop untuk `cinematic-camera`.

Override **tidak mengubah** isi `SKILL.md` upstream.

## 4. Membaca secara selektif

1. Baca hanya `SKILL.md` hasil teratas.
2. Muat `scripts/` atau `references/` hanya bila workflow membutuhkannya.
3. Jangan membuka seluruh 115 skill.

## 5. Dependensi (dipasang saat dibutuhkan)

Dependensi test ada di `tests/requirements-test.txt`. Untuk pemakaian skill, pasang hanya yang dibutuhkan:

| Kebutuhan | Dipakai oleh |
|---|---|
| `pocketsphinx` (BSD) | word alignment bahasa Inggris (`narration-subtitle-sync`) |
| `smartmoneyconcepts` (MIT), `pandas` | `xauusd-smc-analysis` |
| `python-docx` | `novel-typesetting`, ekspor DOCX |
| `ffmpeg` dan `ffprobe` di PATH | `quality-gate`, `narration-subtitle-sync` (audio) |
| `playwright` dan Chromium | `webapp-testing` |

Remotion, Three.js, dan Flutter membutuhkan Node atau Flutter SDK. Library ini **tidak** memasangnya otomatis. Tidak ada instalasi global dari library.

## 6. Menambahkan skill buatan sendiri

Di clone yang bisa Anda tulis (bukan clone read-only):

```bash
cd ~/zy-lib/ZY-Skill-Library
python scripts/import_personal.py /path/ke/skill-saya --category ai-agents --license MIT --label "ChatGPT"
cd .. && git add -A && git commit -m "skill: <nama>" && git push
```

- Sumber: file `SKILL.md`, folder, ZIP, atau URL GitHub publik.
- Ditolak: lisensi tidak dinyatakan, risiko HIGH, atau nama sama dengan isi berbeda. Penimpaan hanya dengan `--approve-overwrite`; versi lama diarsipkan di `research/skill-versions/`.
- Jalur URL GitHub belum diuji langsung (lihat backlog).

## 7. Memperbarui library

```bash
cd ~/zy-lib && git pull
cd ZY-Skill-Library && python scripts/build_registry.py && python scripts/validate_library.py
```

## 8. Menonaktifkan skill bermasalah

- Di proyek Anda: hapus folder skill dari target instalasi (mis. `.claude/skills/<nama>`). Library tidak berubah.
- Di library: hapus folder `skills/<kategori>/<nama>`, jalankan `build_registry.py`, dan catat di `CHANGELOG.md`.

## 9. Pemasangan ke proyek (opsional)

Tidak diperlukan untuk akses read-only.

```bash
python scripts/install_skills.py --target .claude/skills            # dry-run
python scripts/install_skills.py --target .claude/skills --apply
```

## 10. Prompt aktivasi universal (Claude Code dan Claude Chat)

> Gunakan ZY Skill Library dari repo azyananash-hub/azyan-music, branch ccr-57e40ec8-e8i3fa, folder ZY-Skill-Library. Jangan menyalin skill ke proyek ini. Pilih skill paling relevan dari `SKILL_REGISTRY.json` (atau jalankan `scripts/route_skill.py` bila ada shell), baca hanya `SKILL.md`-nya, dan muat `scripts/` atau `references/` seperlunya. Jika akses GitHub atau shell tidak tersedia, katakan itu dan berhenti. Tugas: <tulis tugas>.

## 11. Status verifikasi per platform

| Platform | Status | Catatan |
|---|---|---|
| Claude Code (shell) | Router dan installer diuji di sandbox. Akses lintas proyek dilaporkan berhasil pada uji EarthStop. | Pemuatan otomatis skill di sesi Claude Code belum diuji langsung. |
| Claude Chat | NOT VERIFIED | Tidak ada bukti dari sesi bahwa Claude Chat dapat membaca repository GitHub. Gunakan prompt di atas dan catat hasilnya. |
| Codex | NOT VERIFIED | Dokumentasi resmi tidak dapat diakses dari sesi (DNS). |
| Android (cloud) | NOT VERIFIED | Tidak diuji. |

Tidak ada klaim instalasi global atau sinkronisasi lintas platform.
