# Progres ZY Skill Library

Terakhir diperbarui: 2026-11-25 (v0.2.0). Sumber kebenaran angka: `SKILL_REGISTRY.json` dan `research/import-manifest.json`.

## Hasil saat ini
- 46 skill di disk, 0 error validasi (`python scripts/validate_library.py`).
- 86 test lulus (`python -m unittest discover -s tests -t tests` dari venv `tests/requirements-test.txt`).

| Klasifikasi | Status | Jumlah |
|---|---|---|
| CUSTOM | VERIFIED | 15 |
| IMPORTED | VERIFIED (diuji dengan tugas nyata) | 6 (pdf, docx, xlsx, pptx, skill-creator, slack-gif-creator) |
| ADAPTED | VERIFIED | 1 (webapp-testing: perbaikan cleanup proses) |
| IMPORTED | belum diuji (instruksi saja) | 24 |
| BLOCKED | tidak diimpor | 1 (doc-coauthoring: tanpa lisensi) |

Target awal 50 skill teruji belum tercapai: 22 skill teruji. Tidak ada skill kosong yang ditambahkan untuk mengejar jumlah.

## Fase
| Fase | Status |
|---|---|
| Riset dan pengambilan sumber (2 repository, clone read-only) | Selesai untuk anthropics/skills dan obra/superpowers |
| Impor dengan provenance (`scripts/import_upstream.py`) | Selesai |
| Inspeksi keamanan script sebelum dijalankan (`third-party-skill-audit`) | Selesai; temuan false positive di dokumentasi |
| Uji fungsional skill impor | Selesai untuk 7 skill; 24 belum |
| Skill custom baru (load flow, Modbus, cooling tower, boiler, RO, tabungan) | Selesai, diuji |
| Adaptasi | Satu (webapp-testing). Lainnya belum |
| Deduplikasi | Belum. Lihat `reports/quality-audit.md` bagian duplikasi |
| Konfigurasi discovery Claude Code | Installer tersedia; belum diverifikasi di sesi Claude Code nyata |
| Konfigurasi discovery Codex | BELUM TERVERIFIKASI. Dokumentasi resmi tidak bisa diakses (DNS) |

## Backlog prioritas
1. Uji fungsional untuk skill instruksi (obra process skills, frontend-design, dll.) dengan tugas nyata.
2. Deduplikasi folder `scripts/office/` (identik di docx, pptx, xlsx) dengan mekanisme shared yang tetap kompatibel saat instalasi.
3. Verifikasi lokasi discovery Codex dari dokumentasi resmi OpenAI.
4. Migrasi datastore pymodbus ke SimDevice (deprecation).
5. PowerMCP (Power-Agent): BLOCKED sampai ada lisensi/akses ke PowerWorld/PSSE yang sah untuk pengujian.

## Keputusan utama
- 2026-11-25: Impor disalin utuh dengan SOURCE.md; adaptasi hanya lewat folder ADAPTATION.md.
- 2026-11-25: Test memakai venv `tests/requirements-test.txt`, bukan Python sistem.
- 2026-11-25: Skill impor tidak wajib 13 section ZY; validasinya minimal (name, description, lisensi).

## Checkpoint v0.3.0 (2026-11-25)
- Hasil: 50 skill di disk, 26 VERIFIED (19 CUSTOM, 6 IMPORTED, 1 ADAPTED), 24 IMPORTED belum diuji perilakunya (smoke sintaks lulus), 0 error validasi, 96 test lulus.
- Baru: steam-water-properties (CoolProp, MIT), portfolio-metrics-quantstats (quantstats, Apache-2.0), fsrs-scheduler (fsrs, MIT), markitdown-converter (markitdown, MIT). Dicek dari metadata PyPI; quantstats Apache-2.0 dari LICENSE repository (pencarian sebelumnya).
- Lisensi: semua skill buatan ZY kini MIT (`LICENSE-ZY.md`). Skill upstream tetap lisensi aslinya.
- Router: `scripts/route_skill.py` (kata kunci, tanpa dependensi). Uji 8 kueri buatan sendiri: 8/8 top-1. Ini uji kewarasan, bukan benchmark.
- Windows: `scripts/install_windows.ps1` dibuat, TIDAK DIUJI (sandbox tanpa Windows/pwsh).
- Codex: `developers.openai.com` tetap tidak bisa dijangkau (DNS gagal, curl kode 000). Discovery Codex BELUM TERVERIFIKASI; tidak ada jalur Codex yang diklaim.
- Tidak dilakukan: deduplikasi office (sesuai keputusan), instalasi global, pengujian ulang 24 skill instruksi.

## Checkpoint v0.4.0 (2026-11-25)
- Hasil: 80 skill di disk, 0 error validasi. Status: VERIFIED 27 (19 CUSTOM, 6 IMPORTED, 1 ADAPTED, 1 ffmpeg-skill dengan cakupan resep), VALIDATED 29 (impor baru), IMPORTED 24 (smoke sintaks saja).
- Impor baru 30 skill dari 7 repository MIT (LICENSE dibaca langsung dari clone): haidrrrry/claude-remotion-skill (1), Liamrjohnston/remotion-motion-graphics-skill (3), kajisho5/ffmpeg-skill (1), alton47/threejs-skills (14), MIGO-OvO/plc-skill (1), zakariaf/Flutter-Skills (8 dari 40), supabase/agent-skills (2).
- Dedupe: Liam `motion-graphics` tidak diimpor karena tumpang tindih dengan remotion-motion-graphics.
- Pemindaian risiko: tidak ada HIGH. MEDIUM hanya contoh `npm install` di dokumentasi dan satu false positive `.env`. Tidak ada script upstream yang dijalankan.
- Lazy installation: tidak ada npm/pip upstream yang dipasang.
- Belum tercakup (P0/P1/P2): HTML Canvas/SVG animation, sound design, human-like narration (butuh TTS besar, ditunda), electrical protection, motor control, instrumentation, troubleshooting, academic research, dan XAUUSD sumber MIT yang layak.
- Importer: ditambah opsi `--commit` agar folder staging (bukan git) tetap punya provenance.

## Checkpoint v0.5.0 (2026-11-25)
- Hasil: 98 skill, 0 error validasi. Status: VERIFIED 34, VALIDATED 40, IMPORTED 24 (smoke sintaks).
- Upstream baru (MIT, LICENSE dibaca dari clone): siegerts/skill-canvas-video (creating-canvas-video-animations), acelera-agency/html-animation (motion-graphics; nama frontmatter upstream), iart-ai/web-animation-skills (svg-animation, accessible-animation, micro-interaction), calesthio/generative-media-skills (audio-mixing-mastering), bianbianzhu/procedural-sfx, meiiie/structured-root-cause-research (governance), K-Dense-AI/scientific-agent-skills (literature-review, citation-management), KalarisLabs/research-agent-skills (citation-verification).
- Custom (MIT, diuji dengan nilai acuan terhitung manual): overcurrent-relay-curves, transformer-rating-regulation, motor-starting-sizing, instrument-loop-calc, reliability-pm-metrics, industrial-energy-metrics, narration-subtitle-sync (ffmpeg loudnorm nyata).
- ClipACanvas: render-link-builder (v0.1) sudah memenuhi protokol (1920x1080 horizontal, 1080x1920 vertical, 60 fps, durasi default 4 s, auto=true, minified, URL-encoded). Tidak diubah.
- BLOCKED / tidak tercakup:
  - Visual composition: tidak ditemukan sumber MIT/Apache yang layak dalam pencarian ini; belum dicari lebih lanjut.
  - Human-like narration berbasis neural TTS: butuh unduhan model besar; TTS tidak terpasang. Didukung lewat audio eksternal atau rekaman pengguna (narration-subtitle-sync).
  - Electrical troubleshooting: tidak ditemukan sumber yang layak; PLC troubleshooting sebagian dari plc-skill.
  - Electrical protection (koordinasi antar-relai, setting): hanya kurva bentuk IEC 60255; konstanta belum diverifikasi ke dokumen standar.
  - Engineering report writing dan XAUUSD ICT analysis: belum dicari spesifik; tidak ada sumber yang diverifikasi. Trading risk management dan backtesting tercakup skill yang sudah ada.
  - VERIFIED sumber tanpa LICENSE, tidak diimpor: Zacklinkk/svg-foundry-skill, RandyHaylor/audio-and-vocal-mastering.
