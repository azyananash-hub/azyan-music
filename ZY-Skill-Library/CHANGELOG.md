# CHANGELOG

## [0.1.0] - 2026-11-25
### Ditambahkan
- Struktur library: `skills/` (14 kategori), `scripts/`, `references/`, `templates/`, `tests/`, `benchmarks/`, `research/`, `reports/`.
- Dokumen root: `README.md`, `AGENTS.md`, `CLAUDE.md`, `MASTER_PROTOCOL.md`, `SKILL_REGISTRY.json`, `CHANGELOG.md`.
- Skill validated (9):
  - `engineering/short-circuit-calculator`
  - `engineering/fmea-rpn-prioritizer`
  - `quantitative-trading/trade-statistics`
  - `quantitative-trading/position-size-calculator`
  - `japanese-education/srs-sm2-scheduler`
  - `clipacanvas/render-link-builder`
  - `governance/skill-engineering-standard`
  - `governance/third-party-skill-audit`
  - `software-development/secret-leak-scan`
- Tooling: `validate_library.py`, `build_registry.py` (dengan `--check`), `install_skills.py` (dry-run default).
- Test unittest (standard library) untuk seluruh script dan tooling.
- Riset: `references/sources-and-licenses.md`, `research/PROGRESS.md`.

### Diketahui belum selesai
- Kategori industrial-utility, automation, ai-agents, flutter, creative-production, motion-graphics, academic-research, finance belum berisi skill.
- Sebagian lisensi repository eksternal belum diverifikasi langsung dari file LICENSE.
- Benchmark belum dijalankan.
- Uji render ClipACanvas di server belum dilakukan.

## [0.2.0] - 2026-11-25
### Ditambahkan
- 31 skill IMPORTED dari `anthropics/skills` (Apache-2.0, commit e4bb5d9) dan `obra/superpowers` (MIT, commit 22f0b46), dengan SOURCE.md dan LICENSE per skill.
- 6 skill CUSTOM baru yang diuji: `load-flow-pandapower`, `modbus-tcp-client`, `cooling-tower-performance`, `boiler-efficiency-indirect`, `ro-mass-balance`, `compound-savings-projection`.
- `scripts/import_upstream.py` (impor berulang dengan provenance dan manifest), `research/import-manifest.json`.
- `tests/skills/`: uji fungsional skill impor dan custom; `tests/requirements-test.txt`.
### Diubah
- `webapp-testing/scripts/with_server.py`: ADAPTED. Cleanup sekarang mematikan process group. Lihat `ADAPTATION.md`.
- Parser frontmatter mendukung block scalar (`>`, `|`); continuation nilai plain menjadi error.
- Registry memuat `classification` dan `status`.
### Diketahui
- 24 skill impor belum diuji fungsinya.
- Folder `scripts/office/` identik di tiga skill (belum dideduplikasi).
- Discovery Codex belum terverifikasi (dokumentasi resmi tidak terjangkau).
- `doc-coauthoring` BLOCKED karena tidak ada lisensi.

## [0.3.0] - 2026-11-25
### Ditambahkan
- Skill custom: steam-water-properties, portfolio-metrics-quantstats, fsrs-scheduler, markitdown-converter (diuji).
- `scripts/route_skill.py` (router kata kunci), `scripts/install_windows.ps1` (tidak diuji di Windows).
- `LICENSE-ZY.md` (MIT) untuk skill buatan ZY.
### Diubah
- Lisensi skill buatan ZY: original-zy -> MIT.
### Diketahui
- 24 skill impor hanya lolos smoke sintaks; perilakunya belum diuji.
- Discovery Codex belum terverifikasi (dokumentasi tidak terjangkau).

## [0.4.0] - 2026-11-25
### Ditambahkan
- 30 skill impor MIT (VALIDATED, kecuali ffmpeg-skill VERIFIED recipe-level): Remotion, Liamrjohnston cinematic/terminal/article, FFmpeg, Three.js (14), PLC (plc-skill), Flutter (8), Supabase (2). Commit upstream dan LICENSE di tiap folder.
- Test `tests/skills/test_v04_skills.py`.
### Diubah
- `scripts/import_upstream.py`: opsi `--commit`.

## [0.5.0] - 2026-11-25
### Ditambahkan
- 11 skill upstream MIT (VALIDATED): canvas, HTML/motion, SVG, accessible/micro-interaction animation, audio mixing, procedural SFX, RCA, literature review, citation management, citation verification.
- 7 skill custom MIT (VERIFIED): overcurrent relay curves, transformer rating/regulation, motor starting, 4-20 mA and Pt100 loop calculations, reliability/PM metrics, energy metrics, narration/subtitle sync.
### Diketahui
- Visual composition, neural TTS narration, electrical troubleshooting, XAUUSD ICT: BLOCKED atau belum dicari (lihat research/PROGRESS.md).
