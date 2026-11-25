# Platform discovery: cara AI menemukan skill ZY

Library ini menyimpan skill di `skills/<kategori>/<nama-skill>/SKILL.md`. Folder kategori hanya untuk pengorganisasian manusia; platform AI membaca folder skill.

## Claude Code (target utama)
Claude Code memuat skill dari folder yang berisi `SKILL.md` dengan frontmatter `name` dan `description`:
- Global: `~/.claude/skills/<nama-skill>/SKILL.md` (berlaku di semua proyek).
- Per proyek: `<proyek>/.claude/skills/<nama-skill>/SKILL.md`.

Pemasangan dengan installer library (dry-run dulu):
```bash
python scripts/install_skills.py --list
python scripts/install_skills.py --target ~/.claude/skills
python scripts/install_skills.py --target ~/.claude/skills --apply
```
Installer menyalin seluruh folder skill (termasuk `scripts/` dan `references/`). Jika nama sudah ada, installer tidak menimpa kecuali `--force`.

Catatan: cara pasti pemuatan dapat berubah antarversi Claude Code. Verifikasi dengan membuka sesi baru dan memeriksa daftar skill yang tersedia.

## Agent lain (Codex, Cursor, dll.)
- Baca `AGENTS.md` di root library sebagai instruksi umum.
- Skill tetap dapat dibuka sebagai file Markdown; SKILL.md tidak bergantung pada fitur khusus Claude.
- Lokasi discovery agent lain tidak diverifikasi di sesi ini; sesuaikan dengan dokumentasi masing-masing.

## Progressive disclosure
1. Metadata (`name`, `description`) dibaca untuk memutuskan apakah skill relevan.
2. SKILL.md dibaca saat skill dipakai.
3. `references/` dan `scripts/` dibuka hanya bila dibutuhkan workflow.
Dengan begitu AI tidak perlu membaca seluruh library pada setiap pekerjaan.
