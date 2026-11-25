# CLAUDE.md: ZY Skill Library

Instruksi khusus untuk Claude Code ketika bekerja di folder ini.

## Konteks
- Library ini berisi skill untuk kebutuhan pribadi pengguna (mahasiswa Teknik Elektro, praktisi Industrial Utility, pengembang Flutter, pembelajar bahasa Jepang, dan kreator konten).
- Bahasa penjelasan: Bahasa Indonesia. Istilah teknis: Bahasa Inggris.

## Perintah harian
```bash
python scripts/validate_library.py                 # validasi standar skill + registry
python scripts/build_registry.py                   # rebuild SKILL_REGISTRY.json
python scripts/install_skills.py --list            # daftar skill
python -m unittest discover -s tests -v            # semua test
```

## Aturan kerja
- Ikuti `MASTER_PROTOCOL.md` dan `skills/governance/skill-engineering-standard/SKILL.md`.
- Setelah menambah atau mengubah skill, jalankan validator, registry, dan test sebelum menyatakan selesai.
- Jangan mengarang angka. Jika perlu angka, hitung dengan script atau tanyakan.
- Jangan menyalin kode dari repository pihak ketiga tanpa memeriksa lisensinya (lihat `references/sources-and-licenses.md`).
- Gunakan `third-party-skill-audit` sebelum memasang skill dari sumber luar.

## Aturan repository
- Library ini berada di dalam repository Android `azyan-music`. Perubahan di folder ini tidak boleh memengaruhi build Gradle aplikasi.
- Commit hanya saat diminta.
