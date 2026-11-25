# ZY Skill Library

Kumpulan skill AI yang modular, dapat diuji, dan dapat dipasang ke Claude Code (atau agent lain yang membaca `SKILL.md`).

Library ini **bukan** kumpulan prompt. Setiap skill yang berstatus `validated` memiliki script, test, dan batasan cakupan yang dapat diverifikasi.

Mulai cepat: lihat [QUICKSTART.md](QUICKSTART.md).

## Status singkat (v0.2.0)

46 skill di disk, 0 error validasi, 86 test lulus. Daftar lengkap ada di `SKILL_REGISTRY.json`.

| Klasifikasi | Status | Jumlah |
|---|---|---|
| CUSTOM | VERIFIED | 15 |
| IMPORTED | VERIFIED (diuji) | 6 |
| ADAPTED | VERIFIED | 1 (`webapp-testing`) |
| IMPORTED | belum diuji | 24 |
| BLOCKED | tidak diimpor | 1 (`doc-coauthoring`: tanpa lisensi) |

Sumber impor: `anthropics/skills` (Apache-2.0, per skill) dan `obra/superpowers` (MIT). Detail commit dan lisensi: `research/import-manifest.json` dan `references/sources-and-licenses.md`.

## Struktur

```
ZY-Skill-Library/
├── AGENTS.md / CLAUDE.md        instruksi untuk agent
├── MASTER_PROTOCOL.md           aturan global
├── SKILL_REGISTRY.json          registry (dibangun script)
├── CHANGELOG.md
├── skills/<kategori>/<skill>/   SKILL.md + scripts/ + references/
├── scripts/                     validator, registry builder, installer
├── templates/                   template SKILL.md
├── references/                  sumber, lisensi, platform discovery
├── tests/                       unittest (standard library)
├── benchmarks/                  belum ada benchmark yang dijalankan
├── research/                    riset, progres, keputusan adopsi
└── reports/                     laporan audit kualitas
```

## Instalasi (Claude Code)

Persyaratan: Python 3.9+. Tidak ada dependensi pihak ketiga.

```bash
cd ZY-Skill-Library
python scripts/install_skills.py --list                      # lihat skill
python scripts/install_skills.py --target ~/.claude/skills   # dry-run
python scripts/install_skills.py --target ~/.claude/skills --apply
```

Pemasangan per proyek: ganti target menjadi `<proyek>/.claude/skills`. Detail: `references/platform-discovery.md`.

## Menjalankan dan menguji

```bash
python scripts/validate_library.py
python scripts/build_registry.py --check
python -m unittest discover -s tests -t tests -v   # gunakan venv: pip install -r tests/requirements-test.txt
```

Contoh penggunaan script skill:
```bash
python skills/engineering/short-circuit-calculator/scripts/short_circuit.py --v-sec-kv 11 --s-sc-mva 100
python skills/engineering/fmea-rpn-prioritizer/scripts/fmea_rpn.py worksheet.csv
python skills/quantitative-trading/position-size-calculator/scripts/position_size.py \
  --equity 10000 --risk-pct 1 --entry 2650 --stop 2640 --value-per-unit 100
python skills/japanese-education/srs-sm2-scheduler/scripts/sm2.py   # modul; dipakai dari kode Python
python skills/clipacanvas/render-link-builder/scripts/build_render_link.py scene.html
python skills/governance/third-party-skill-audit/scripts/scan_skill_risk.py <folder-karantina>
python skills/software-development/secret-leak-scan/scripts/scan_secrets.py <folder-proyek>
```

## Keterbatasan yang harus diketahui
- **Target 50 skill teruji belum tercapai** (22 teruji). Skill impor berbasis instruksi belum diuji perilakunya.
- **Discovery Codex belum terverifikasi** (dokumentasi resmi tidak terjangkau dari sesi ini).
- **Perhitungan teknik** (short circuit, FMEA) adalah estimasi/alat bantu. Bukan pengganti studi lengkap, SOP, atau keputusan engineer berkompetensi.
- **Trading**: skill hanya perhitungan matematis dan statistik historis. Tidak ada data pasar, tidak ada sinyal, tidak ada jaminan profit.
- **Riset repository eksternal**: sebagian lisensi sudah diverifikasi; sebagian belum. Status per repository ada di `references/sources-and-licenses.md`.
- **Keamanan**: pemindai adalah heuristik. Hasil bersih bukan bukti aman.
- **ClipACanvas**: endpoint `clipacanvas.vercel.app` belum diuji langsung dari sesi ini.
- **Benchmark** belum dijalankan; folder `benchmarks/` hanya berisi catatan.
- **Konteks repository**: library ini berada di dalam repository Android `azyan-music`. Proyek Flutter yang direncanakan belum ada di repository ini.

## Lisensi
Kode dan dokumentasi skill buatan ZY: `original-zy` (lihat keputusan pemilik sebelum publikasi). Lisensi sumber rujukan tercatat di `references/sources-and-licenses.md`.
