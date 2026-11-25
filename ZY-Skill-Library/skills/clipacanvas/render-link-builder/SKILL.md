---
name: render-link-builder
description: Produce a self-contained, lightly minified HTML animation for ClipACanvas and build its direct render link (URL-encoded code, 1920x1080 horizontal by default). Use whenever the user wants an HTML/Canvas/SVG motion graphic that renders through the ClipACanvas render endpoint.
license: original-zy
compatibility: Python 3.9+ standard library only
metadata: {"category": "clipacanvas", "status": "verified", "owner": "zy"}
---

# ClipACanvas Render Link Builder

## Activation Triggers
- User meminta animasi HTML untuk ClipACanvas, "direct render link", atau "render link".
- User meminta motion graphic berbasis HTML Canvas/SVG yang harus berjalan mandiri.
- Setiap kali HTML ClipACanvas selesai dibuat dan perlu dibungkus menjadi link.

## Scope dan Batas Kemampuan
- Dicakup: minifikasi konservatif HTML, URL encoding, dan pembentukan link dengan parameter sesuai spesifikasi.
- TIDAK dicakup: menguji link di server ClipACanvas, pembuatan animasi itu sendiri (lihat skill creative-production di masa depan), dan minifikasi JS mendalam.
- Endpoint `clipacanvas.vercel.app` belum diverifikasi secara langsung dari sesi ini; perlakukan sebagai spesifikasi dari user.

## Required Tools
- Python 3.9+ standard library.
- `scripts/build_render_link.py`.

## Input dan Output Specification
Input: file HTML lengkap (`<!doctype html>` ... ) dan opsi `--orientation` (`horizontal` default = 1920x1080; `vertical` = 1080x1920), `--fps` (default 60), `--duration` (default 4), `--no-auto`, dan `--out-html` (opsional).

Output: URL di stdout. Peringatan di stderr bila URL > 8000 karakter. HTML minified bisa disimpan dengan `--out-html`.

Format link:
`https://clipacanvas.vercel.app/render?code=[URL_ENCODED_HTML]&width=1920&height=1080&fps=60&duration=4&auto=true`

## Execution Workflow
1. Buat HTML mandiri: tanpa CDN eksternal bila memungkinkan; semua CSS/JS inline.
2. Pastikan gerakan nyata: gunakan requestAnimationFrame atau timeline terdefinisi, durasi konsisten dengan `--duration`.
3. Jalankan `python scripts/build_render_link.py animasi.html --orientation horizontal`.
4. Bila ada peringatan panjang URL, perkecil HTML (hapus data tidak perlu) sebelum menyerahkan link.
5. Sajikan HTML dalam blok kode Markdown dan link render kepada user, sesuai preferensi ZY.

## Decision Rules
- Default orientasi horizontal 1920x1080. Gunakan vertical hanya bila user meminta format vertikal/Shorts.
- Catatan spesifikasi: contoh template di spesifikasi ZY memakai `width=1080&height=1920`, tetapi aturan horizontal menyebut 1920x1080. Skill mengikuti aturan horizontal sebagai default dan mengizinkan vertical secara eksplisit.
- Jika HTML memakai dependensi eksternal, nyatakan risikonya (gagal bila offline atau CDN diblokir).
- Jangan memasukkan secret atau token ke HTML yang akan dibagikan via link.

## Error Handling
- HTML kosong atau file tidak bisa dibaca: error, exit code 2.
- Orientasi tidak dikenal: ditolak oleh argparse.
- URL terlalu panjang: peringatan, tetap menghasilkan URL.

## Quality Control
- Tes minifikasi: blok `<script>` dan `<style>` tidak berubah isi.
- Tes URL: `code` ter-decode kembali menjadi HTML minified yang sama.
- Unit test `tests/test_render_link.py` harus lulus.
- Buka link di browser (manual) sebelum menyatakan selesai; skill tidak membuktikan render berhasil.

## Acceptance Criteria
- Parameter `width`, `height`, `fps`, `duration`, `auto` ada dan sesuai input.
- Komentar HTML dihapus di luar blok script/style/pre/textarea.
- JS di dalam `<script>` tidak diubah.
- URL dapat di-decode kembali ke HTML yang sama dengan hasil minify.

## Contoh Implementasi
```bash
python scripts/build_render_link.py scene.html --out-html scene.min.html
python scripts/build_render_link.py scene.html --orientation vertical --duration 6
```

## Test Cases
Lihat `tests/test_render_link.py`:
1. Default horizontal menghasilkan width 1920, height 1080.
2. Vertical menghasilkan 1080x1920.
3. Script tidak berubah; komentar dihapus.
4. Round-trip URL decode.
5. Orientasi/fps/durasi invalid ditolak.

## Referensi dan Sumber
- Spesifikasi ZY Skill Library (prompt dari user): format link dan aturan resolusi.
- Lihat `references/minifier-limitations.md`.

## Informasi Lisensi
- Kode dan dokumentasi: `original-zy`. Tidak ada kode pihak ketiga yang disalin.
