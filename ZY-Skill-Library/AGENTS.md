# AGENTS.md: instruksi untuk AI agent yang bekerja di ZY Skill Library

Dokumen ini berlaku untuk agent apa pun (Claude Code, Codex, Cursor, atau lainnya).

## Yang harus dilakukan
1. Baca `MASTER_PROTOCOL.md` sebelum mengubah skill.
2. Untuk skill yang relevan, baca hanya `skills/<kategori>/<nama>/SKILL.md` terlebih dahulu. Buka `references/` dan `scripts/` bila workflow membutuhkannya.
3. Jalankan script di skill sesuai petunjuk SKILL.md; jangan mengandalkan angka dari memori.
4. Setelah mengubah skill: `python scripts/validate_library.py`, `python scripts/build_registry.py`, lalu `python -m unittest discover -s tests`.
5. Catat perubahan di `CHANGELOG.md`.

## Yang dilarang
- Mengarang data pasar, hasil backtest, angka kontrak broker, atau hasil uji.
- Menyalin kode dari repository ber-lisensi copyleft (GPL/AGPL) atau lisensi tidak jelas.
- Menjalankan script atau installer dari skill pihak ketiga sebelum `third-party-skill-audit`.
- Menampilkan nilai secret utuh.
- Menghapus atau menimpa skill tanpa instruksi eksplisit.
- Menjanjikan keuntungan trading atau menyatakan hasil simulasi sebagai jaminan.

## Bahasa
Dokumentasi dan respons ke pengguna: Bahasa Indonesia. Istilah teknis dan kode: Bahasa Inggris.

## Batas keselamatan
Untuk pekerjaan listrik industri, boiler, tekanan, dan bahan kimia (WTP/RO), tampilkan batas cakupan. Prosedur operasi harus mengacu SOP perusahaan dan otorisasi personel.
