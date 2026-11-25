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
