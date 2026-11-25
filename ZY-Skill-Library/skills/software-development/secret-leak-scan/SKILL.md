---
name: secret-leak-scan
description: Scan a project for accidentally committed secrets (Google API keys, AWS access keys, private keys, GitHub/Stripe/OpenAI-style tokens, generic password or token assignments) and report masked previews only. Use before committing or pushing code, especially Flutter/Supabase or AI-API projects.
license: original-zy
compatibility: Python 3.9+ standard library only
metadata: {"category": "software-development", "status": "verified", "owner": "zy"}
---

# Secret Leak Scan

## Activation Triggers
- User meminta "cek secret", "ada API key di kode?", "audit sebelum push", atau "security review".
- Sebelum commit pertama pada project baru, atau sebelum membuka repository ke publik.
- Setelah menambahkan konfigurasi Supabase, Firebase, atau layanan AI.

## Scope dan Batas Kemampuan
- Dicakup: pola secret umum pada file teks di dalam direktori; output selalu dimasking.
- TIDAK dicakup: pemeriksaan riwayat git (commit lama), validasi apakah secret masih aktif, dan secret dalam binary.
- Untuk pemindaian riwayat git, gunakan alat khusus (mis. gitleaks atau trufflehog). Lisensi keduanya BELUM diverifikasi di sesi ini; cek LICENSE resminya sebelum dipakai.
- Temuan `supabase service_role` hanya sinyal lemah: nama saja tidak membuktikan key bocor.

## Required Tools
- Python 3.9+.
- `scripts/scan_secrets.py`.

## Input dan Output Specification
Input: direktori proyek.
Output: `[rule] file:line :: preview` dengan nilai dimasking (4 karakter awal, akhir, sisanya `*`). Mode `--json` tersedia.
Exit code: 0 tidak ada temuan, 1 ada temuan, 2 error input.

## Execution Workflow
1. Jalankan `python scripts/scan_secrets.py <folder-proyek>`.
2. Untuk setiap temuan: tentukan apakah benar secret atau contoh/placeholder.
3. Jika benar secret: pindahkan ke environment variable atau secret manager, hapus dari kode, dan ROTATE key di penyedia. Menghapus dari kode saja tidak cukup bila sudah pernah di-commit.
4. Tambahkan file konfigurasi lokal (mis. `.env`) ke `.gitignore`.
5. Jalankan ulang scanner sampai bersih atau hanya tersisa temuan yang sudah dijelaskan.

## Decision Rules
- Placeholder seperti `your_api_key_here`, `example`, `<...>` diabaikan oleh pola generik.
- Anon key Supabase bersifat publik secara desain, tetapi `service_role` tidak boleh ada di klien (APK/IPA).
- Jangan pernah mencetak nilai secret penuh di chat, log, atau laporan.
- Jika secret sudah pernah ter-push ke repository publik: anggap terekspos, rotate, lalu bersihkan.

## Error Handling
- Direktori tidak ada: exit 2.
- File terlalu besar (> 2 MB) atau binary: dilewati; disebutkan di dokumentasi sebagai batasan.
- Dekode tidak valid: `errors=replace`, tidak menggagalkan pemindaian.

## Quality Control
- Fixture test memuat key palsu berformat valid dan memastikan terdeteksi.
- Output tidak pernah berisi nilai penuh (test memverifikasi).
- Direktori `.git`, `node_modules`, `build`, `.dart_tool` dilewati.

## Acceptance Criteria
- Fixture `AIza` + 35 karakter terdeteksi sebagai `google-api-key`.
- Fixture `password = "placeholder_example"` tidak menghasilkan temuan.
- Preview tidak memuat nilai penuh.
- Exit code 1 bila ada temuan.

## Contoh Implementasi
```bash
python scripts/scan_secrets.py ../azyan-music
python scripts/scan_secrets.py . --json
```

## Test Cases
Lihat `tests/test_scan_secrets.py`:
1. Pola Google API key terdeteksi.
2. Private key block terdeteksi.
3. Placeholder diabaikan.
4. Preview masked.
5. Direktori dengan file bersih menghasilkan nol temuan.

## Referensi dan Sumber
- Pola format key: dokumentasi masing-masing penyedia (Google, AWS, GitHub, Stripe, OpenAI). Pola ditulis ulang, bukan disalin dari alat lain.
- Lihat `references/rotation-checklist.md`.

## Informasi Lisensi
- Kode dan dokumentasi: `original-zy`.
