# IMPLEMENTATION-APPROVAL-PACKAGE: P01–P17

Status: NOT AUTHORIZED. Tidak ada implementasi, tidak ada instalasi, dan tidak ada perubahan berkas library. Dokumen ini adalah gerbang persetujuan. Setiap item disetujui, diubah, atau ditolak per ID.

Dasar: `SELECTIVE-INTEGRATION-PROPOSAL.md` (kolom sumber, komponen, dan rollback), `deep-audit-2026-11-26.md`, `PROJECT-MEMORY-DESIGN.md`, `DOMAIN-PROFILE-PROPOSALS.md`, dan `BLENDER-SKILLS-COMPARISON.md`.

## 1. Tabel keputusan

Kolom "Tipe": **K** = adaptasi konten (teks atau data dari upstream, ditulis ulang, dengan atribusi). **Z** = kode ZY sendiri (stdlib, tanpa kode pihak ketiga). **R** = integrasi runtime pihak ketiga. Tidak ada item P01–P17 yang berstatus R.

| ID | Kapabilitas | Sumber (commit, lisensi) | Skill terdampak | Modifikasi yang diusulkan | Keamanan | Biaya | Dampak token | Relevansi proyek | Benchmark | Rollback | Tipe | Prioritas |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P01 | Review kualitas desain (K7) | pbakaus/impeccable @9e460a87ef33 (Apache-2.0, NOTICE); nutlope/hallmark @04977e15f3dfd (MIT) | frontend-design (IMPORTED); quality-gate (video) | CREATE `software-development/design-quality-review/` (SKILL, references/checklist.md, ADAPTATION, SOURCE, NOTICE) + tes | Tanpa jaringan, hook, atau kredensial | Rp0 | Target <= 5 KB per SKILL (belum diukur) | AmiraVerse, Money App, ZII (QA visual) | B-UI-1 | Hapus folder; bangun ulang registry | K | P1 |
| P02 | Token desain DESIGN.md (K1) + data UI/UX Pro Max opsional | google-labs-code/stitch-skills @75f4696 (Apache-2.0; NOTICE perlu dicek); nextlevelbuilder/ui-ux-pro-max-skill @bde080f (MIT; lisensi font per berkas) | taste-design, frontend-design (IMPORTED), theme-factory | CREATE `software-development/design-tokens-md/`; MODIFY `references/skill-constraints.json` (batasan palet neon dengan override) | Mode A saja (kode sumber sebagai input). Tanpa Node, Stitch, StitchMCP | Rp0; lisensi font per berkas harus dicek | Target <= 5 KB | Silent Neon Tokyo, EarthStop, AmiraVerse | B-UI-2 | Hapus folder; kembalikan constraints | K + konfigurasi | P2 |
| P03 | Subset panduan web-platform (26) | GoogleChrome/modern-web-guidance-src @92686ac7d6eb (Apache-2.0) | accessible-animation, micro-interaction, svg-animation (parsial) | CREATE `software-development/web-platform-guidance-subset/` (SKILL, ADAPTATION, SOURCE, LICENSE, NOTICE) | Tanpa `npx ...@latest`, cron, atau postinstall | Rp0 | Target <= 5 KB | ZII web, ClipACanvas | B-UI-3 | Hapus folder | K | P3 |
| P04 | Diagram teknis (27) | cathrynlavery/diagram-design @b228c5d77794 (MIT) | Tidak ada (celah C20) | CREATE `engineering/engineering-diagrams/` (SKILL, references/types.md, templates/*.svg, ADAPTATION). Tanpa tautan font dan tanpa onboarding URL | Tanpa sumber eksternal di keluaran. Well-formedness dicek dengan stdlib | Rp0 | Target <= 5 KB | ZII, pendidikan elektro, dokumen WTP | B-ENG-1 | Hapus folder | K | P1 |
| P05 | Panduan motion GSAP (36) | greensock/gsap-skills @aed9cfd32777 (MIT) | motion-graphics; svg-animation; micro-interaction (parsial) | CREATE `motion-graphics/gsap-motion-guidance/` | Library GSAP tidak dipasang. Tanpa jaringan | Rp0 | Target <= 5 KB | Promo, explainer, motion HTML | B-CRE-2 | Hapus folder | K | P2 |
| P06 | Resep shot sinematik (35) | louiseliu/hyperFrames-video-shotcraft @1df77f1ab080 (Apache-2.0) | cinematic-storyboarding (CUSTOM); cinematic-camera (IMPORTED) (parsial) | CREATE `creative-production/cinematic-shot-recipes/` (SKILL, data/recipes.json, ADAPTATION). Bukan komposisi HyperFrames | Data saja | Rp0 | Target <= 5 KB; data dibaca dengan kueri | film-sinematik; Sebelum Sepi | B-CRE-2 | Hapus folder | K (data) | P2 |
| P07 | Pola game Three.js (43) | majidmanzarpour/threejs-game-skills @8286774b22a2 (MIT) | threejs-* (14, parsial; hindari duplikasi threejs-performance) | CREATE `motion-graphics/threejs-game-patterns/`. Helper Tripo3D dan ElevenLabs dibuang | Tanpa helper API berbayar | Rp0 | Target <= 5 KB | Silent Neon Tokyo (game), game browser | B-GAM-1 | Hapus folder | K | P3 |
| P08 | Metodologi review trading, paper-only (45) | tradermonty/claude-trading-skills @5de030b068d1 (MIT) | trade-statistics, position-size-calculator (parsial) | CREATE `quantitative-trading/trade-review-methodology/` dengan disclaimer | Tanpa API FMP, launchd, data broker, dan skrip | Rp0 | Target <= 5 KB | XAUUSD (paper) | B-TRD-1 | Hapus folder | K | P3 (menunggu keputusan disclaimer M5) |
| P09 | Review keamanan aplikasi defensif (K2; BugHunter CB-02, CB-03, CB-13) | elementalsouls/Claude-BugHunter @6a2153d (kode MIT; konten CC BY 4.0) | supabase, supabase-postgres-best-practices (RLS dikecualikan); secret-leak-scan (parsial) | CREATE `software-development/defensive-app-security-review/` (SKILL, references/checklists.md, ADAPTATION dengan atribusi CC BY 4.0) | Tanpa payload, langkah eksploitasi, atau target eksternal | Rp0 | Target <= 5 KB | Money App, AmiraVerse, DEAMIRA | B-SEC-1 | Hapus folder | K | P1 |
| P10 | Pemeriksaan artefak build (K3; CB-04) | Konsep dari BugHunter @6a2153d; implementasi ditulis ZY (CUSTOM) | secret-leak-scan (VERIFIED) | MODIFY `software-development/secret-leak-scan/scripts/` dan tesnya: pola source map, `.git`, dan `.env` di keluaran | Pemindaian file lokal saja | Rp0 | Skrip; tanpa muatan tambahan | Semua build aplikasi | B-SEC-2 | `git revert` dua berkas | Z | P2 |
| P11 | Penjaga kehilangan konten Markdown (K4; FC-06, FC-07) | Ukuran dari audit Firecrawl; tidak ada kode yang dipakai | markitdown-converter (VERIFIED) | MODIFY skrip dan tes `office-documents/markitdown-converter/` | Lokal saja | Rp0 | Skrip | Dokumenter, riset | B-DOC-1 | `git revert` | Z | P2 |
| P12 | Standar memori proyek lokal (C04) | Desain ZY (`PROJECT-MEMORY-DESIGN.md`, disetujui pemilik) | Tidak ada | CREATE `governance/project-memory-standard/` (SKILL format CUSTOM 13 bagian, templates/memory-entry.md, scripts/memory_tool.py, tes) | Tanpa cloud, hook, atau embedding. Filter rahasia pra-tulis. Batas ukuran | Rp0 | Target preload <= 9 KB (belum diukur) | Semua proyek | B-MEM-1 sampai B-MEM-4 | Hapus folder; `git revert` | Z | P1 |
| P13 | Prosedur gerbang persetujuan (C02) | Desain ZY | prd-engineering, technology-selection (parsial) | CREATE `governance/approval-gate/` (SKILL format CUSTOM) | Tanpa tool | Rp0 | Kecil | Semua proyek | B-GOV-1 | Hapus folder | K (ZY) | P2 |
| P14 | Validasi walk-forward dan out-of-sample (C23) | Metode dari 46 Vibe-Trading dan 47 Qlib (pengetahuan saja; tanpa kode) | strategy-backtesting (VERIFIED); portfolio-metrics-quantstats (parsial) | MODIFY `quantitative-trading/strategy-backtesting/scripts/` ATAU CREATE `quantitative-trading/walk-forward-validation/`; tes | Riset dan paper saja. Tanpa broker | Rp0 | Skrip | XAUUSD (paper) | B-TRD-2 | Hapus folder atau `git revert` | Z | P3 |
| P15 | Pengetahuan debugging browser (17) | ChromeDevTools/chrome-devtools-mcp @8c43179464d3 (Apache-2.0; NOTICE) | webapp-testing (VERIFIED) | MODIFY `software-development/webapp-testing/references/` | Tanpa MCP, npx, atau profil browser berisi sesi login | Rp0 | Referensi | AmiraVerse, ZII, ClipACanvas | B-WEB-1 | `git revert` | K | P3 |
| P16 | Tinjauan pembaruan FFmpeg (31) | kajisho5/ffmpeg-skill @31b47c263348 (MIT) | ffmpeg-skill (IMPORTED @73436cb) | Tidak ada. **DITUTUP**: salinan impor identik dengan upstream untuk berkas yang dipakai | Tidak ada | Rp0 | Tidak ada | Pipeline video | Diff selesai (lihat deep audit bagian 1) | Tidak ada | Ulasan | DITUTUP |
| P17 | Sinkronisasi dokumen (K8) | Paket ini dan registry | README.md (header v0.2.0), research/PROGRESS.md (header), references/sources-and-licenses.md (kolom status) | MODIFY ketiga berkas tersebut. Angka diambil dari validator dan tes. Butuh otorisasi karena berkas dokumen repositori | Tidak ada data eksternal | Rp0 | Tidak ada | Tata kelola | B-DOC-2 | `git revert` | Z (dokumen) | P1 |

Catatan: P16 ditutup karena salinan impor sudah sama dengan `skills/ffmpeg-skill/SKILL.md` pada upstream saat ini. Root `SKILL.md` upstream berbeda, tetapi tidak diimpor dan tidak diusulkan.

## 2. Pemisahan adaptasi konten dan integrasi yang dapat dieksekusi

| Kelompok | Item | Yang terjadi di library | Eksekusi kode pihak ketiga? |
|---|---|---|---|
| Adaptasi konten (K) | P01, P02, P03, P04, P05, P06, P07, P08, P09, P15 | Teks atau data ditulis ulang, dengan atribusi dan ADAPTATION.md | Tidak |
| Kode ZY sendiri (Z) | P10, P11, P12, P14 | Skrip stdlib milik ZY dan tesnya. P13 dan P17 berupa konten ZY | Tidak (hanya kode ZY) |
| Integrasi runtime pihak ketiga (R) | Tidak ada | Tidak ada hook, MCP, npx, installer, CLI, atau API berbayar | Tidak |
| Ditutup | P16 | Tidak ada perubahan | Tidak |

Setiap item K dan Z tetap memerlukan persetujuan per ID. Ini berlaku juga untuk item yang hanya berupa teks.

## 3. Batch pertama yang direkomendasikan

Rekomendasi: **Batch-1 = P12 + P04 + P17**.

Alasan:
- Risiko terendah. Tidak ada kode pihak ketiga, tidak ada jaringan, dan biaya Rp0.
- Menutup dua celah terbesar: memori lintas sesi (C04, sudah disetujui desainnya) dan diagram teknis (C20, celah unik).
- P17 menyelesaikan drift dokumentasi yang sudah tercatat di K8.
- Rollback bersih: hapus folder atau `git revert` satu commit.

Urutan berikutnya:
- Batch-2 = P01 + P09 (P1). Dimulai setelah keputusan K7 dan K2 dikonfirmasi pemilik.
- Batch-3 = P05 + P06 (kreatif, P2). Dimulai setelah P04 selesai.
- Sisanya (P02, P03, P07, P08, P10, P11, P13, P14, P15) menunggu prioritas pemilik.

Batch-1 sebaiknya tidak dicampur dengan item yang memerlukan keputusan pemilik lain (Blender, profil, Ollama, atau OpenRoots).

## 4. Keputusan di luar P01–P17

| ID | Keputusan | Status | Yang dibutuhkan |
|---|---|---|---|
| D-1 | Batch-1 (P12, P04, P17) | Menunggu persetujuan | Setuju, ubah, atau tolak |
| D-2 | BL-1: Blender 39a secara selektif (maksimal tiga skill, content-only) | Menunggu | Konfirmasi bahwa 39a adalah repositori yang dimaksud, atau pilih TIDAK ADA. Lihat `BLENDER-SKILLS-COMPARISON.md` |
| D-3 | Profil baru (A–D) | Usulan: tidak ada profil baru | Konfirmasi, atau berikan brief dan override yang berbeda (lihat `DOMAIN-PROFILE-PROPOSALS.md`) |
| D-4 | Ollama | DEFER | Konfirmasi status di mesin pemilik (`ollama --version`, `ollama list`). Tanpa unduhan model |
| D-5 | Teks kanonik OpenRoots (item 28) | UNVERIFIED | Pengambilan gagal karena DNS `openroots.org` diblokir kebijakan jaringan lingkungan. Pilihan: pemilik menyediakan teks, atau menyetujui penambahan host lewat pengaturan lingkungan. Tanpa itu, item 28 tetap BLOCKED untuk adaptasi |
| D-6 | Pencarian engine TTS dengan bukti bahasa Indonesia | Belum dimulai | Setujui pencarian kandidat baru (menambah kandidat di luar register) |
| D-7 | Pembersihan cache riset (lihat bagian 5) | Diusulkan, belum dijalankan | Setujui perintah penghapusan yang tertulis di bawah |
| D-8 | Commit checkpoint kedua untuk dokumen pasca-checkpoint | Menunggu | Setujui commit. Dokumen ini belum di-commit |

## 5. Usulan pembersihan cache riset

- Jalur tepat: `/home/user/ext/research-cache`
- Isi terverifikasi: 52 folder klon (`<owner>__<repo>`) dan 52 berkas `.err`. Tidak ada entri lain. Ukuran sekitar 5,4 GB.
- Yang tidak disentuh: `/home/user/ext/ui-ux-pro-max-skill` (32 MB, sumber bukti I.3). Direktori ini berada di luar cache.
- Bukti yang tersimpan sebelum penghapusan: `identity-ls-remote.tsv` (hash penuh 52 repositori dan satu alias), `triage-summary.tsv` (25 kolom), `deep-audit-2026-11-26.md` (commit, path, dan baris), dan `METHOD.md` (pola dan SHA-256 skrip).
- Verifikasi tambahan: setiap klon dapat dibuat ulang dari URL pada `identity-ls-remote.tsv` lalu diperiksa pada hash commit yang sama.
- Perintah yang diusulkan (belum dijalankan): `rm -rf -- /home/user/ext/research-cache`, lalu `ls /home/user/ext` untuk memastikan hanya `ui-ux-pro-max-skill` yang tersisa.
- Penghapusan tidak dapat dibatalkan. Klon ulang memerlukan akses jaringan ke GitHub.

## 6. Yang akan terjadi setelah persetujuan

- Setiap item yang disetujui dibuat dalam commit terpisah dengan trailer `Claude-Session`.
- Setiap item memiliki ADAPTATION.md atau SOURCE.md dengan commit upstream, lisensi, dan atribusi.
- Registry dibangun ulang dengan `scripts/build_registry.py`, lalu divalidasi dengan `scripts/validate_library.py` dan unittest.
- Baseline kode `7039fed` tetap menjadi referensi. Setiap perubahan dapat di-revert dengan `git revert`.
- Tidak ada force push, tidak ada amend, dan tidak ada PR.

## 7. Permintaan persetujuan

Jawab per ID: setuju, ubah, atau tolak.
1. D-1: Batch-1 (P12, P04, P17), atau pilih item lain.
2. D-2 sampai D-8 sesuai tabel bagian 4.
3. Item P01–P15 yang tidak masuk Batch-1 tetap NOT AUTHORIZED sampai ada persetujuan per ID.
