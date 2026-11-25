# Sumber dan lisensi (ZY Skill Library)

Aturan: lisensi ditulis hanya jika sudah diverifikasi. Kolom **Status verifikasi** menunjukkan seberapa kuat bukti yang didapat. Tanggal verifikasi: 2026-11-25.

**Catatan metode:** GitHub API di sesi ini hanya mengizinkan repository `azyan-music`, sehingga repository eksternal **tidak dibaca langsung** lewat integrasi GitHub. Lisensi di bawah berasal dari pencarian web publik (halaman GitHub, PyPI, dan halaman LICENSE yang muncul di hasil pencarian). Sebelum adopsi kode, baca file LICENSE asli di repository tersebut.

## Kandidat riset dari daftar awal

| Repository | Lisensi (hasil verifikasi) | Status verifikasi | Keputusan library |
|---|---|---|---|
| anthropics/skills | Berlisensi per-skill. README menyebut banyak skill Apache-2.0; setiap skill punya LICENSE.txt sendiri | Parsial (pencarian web, file LICENSE tidak dibuka) | Hanya pola struktur/konvensi SKILL.md. Tidak ada file disalin. |
| obra/superpowers | MIT | Terverifikasi dari halaman GitHub hasil pencarian | Kandidat referensi metodologi (verifikasi, debugging). Belum diadopsi. |
| obra/superpowers-skills | MIT; repo diarsipkan (read-only) sejak Okt 2025 | Sekunder (listing pihak ketiga) | Tidak dipakai. |
| github/spec-kit | MIT | Terverifikasi (GitHub dan PyPI `specify-cli`) | Kandidat untuk workflow spec-driven; belum diadopsi. |
| langchain-ai/langgraph | Belum diverifikasi | Belum | Belum diputuskan. Untuk AI agent multi-step. |
| microsoft/playwright | Belum diverifikasi (umumnya Apache-2.0; perlu dicek) | Belum | Kandidat untuk QA web/Flutter web. |
| appium/appium | Belum diverifikasi | Belum | Kandidat QA mobile; perlu evaluasi terhadap kebutuhan Flutter. |
| e2nIEE/pandapower | BSD-3-Clause (LICENSE master dan develop) | Terverifikasi | Kandidat utama untuk load flow dan short circuit lanjutan. |
| Power-Agent/PowerMCP | MIT (pencarian + PyPI) | Terverifikasi sebagian | Kandidat referensi MCP untuk power system. |
| Power-Agent/PowerSkills | README menyebut MIT, tetapi PR menyatakan repo sebelumnya tidak punya LICENSE | Konflik/tidak pasti | Jangan disalin sebelum LICENSE dipastikan. |
| thiagoralves/OpenPLC_v3 | GPL-3.0 | Terverifikasi (file LICENSE) | Copyleft. Jangan menyalin kode; boleh dijadikan referensi konsep PLC. |
| node-red/node-red | Belum diverifikasi | Belum | Belum diputuskan. |
| pymodbus-dev/pymodbus | Belum diverifikasi | Belum | Kandidat Modbus; perlu cek lisensi. |
| CoolProp/CoolProp | Belum diverifikasi | Belum | Relevan untuk utilitas (boiler, cooling tower). |
| remotion-dev/skills | Tidak jelas: issue #28 menyatakan repo tidak punya file LICENSE | Ambigu | **Tidak disalin.** Lisensi remotion utama bersifat khusus (lisensi perusahaan untuk entitas tertentu). |
| motion-canvas/motion-canvas | Belum diverifikasi | Belum | Kandidat animasi programatik. |
| mrdoob/three.js | Belum diverifikasi (umumnya MIT) | Belum | Kandidat 3D web. |
| ManimCommunity/manim | Belum diverifikasi | Belum | Kandidat animasi matematika/edukasi. |
| hexgrad/kokoro | Belum diverifikasi | Belum | Kandidat TTS ringan; cek ukuran model sebelum unduh (lihat constraint hardware). |
| microsoft/markitdown | Belum diverifikasi | Belum | Kandidat konversi dokumen ke Markdown. |
| docling-project/docling | Belum diverifikasi | Belum | Kandidat parsing PDF; cek kebutuhan resource. |
| yomidevs/yomitan | Belum diverifikasi (proyek ini umumnya GPL-3.0; perlu cek) | Belum | Jangan disalin. Referensi UX kamus saja. |
| open-spaced-repetition/fsrs4anki | MIT (LICENSE, copyright 2022) | Terverifikasi | Referensi algoritma FSRS untuk pengembangan lanjutan. |
| kernc/backtesting.py | AGPL-3.0 | Terverifikasi (setup.py, dokumentasi, PyPI) | Copyleft kuat; jangan disalin. Perhatikan klausul jaringan jika dijalankan sebagai layanan. |
| polakowo/vectorbt | Apache-2.0 dengan Commons Clause (membatasi penjualan produk utamanya) | Terverifikasi (LICENSE.md) | Bukan open source murni (OSI). Hindari sebagai dependensi produk komersial. |
| ranaroussi/quantstats | Apache-2.0 | Terverifikasi (LICENSE.txt, header file, registry) | Kandidat tearsheet/metrik portofolio. |

## Tooling eksternal yang disebut di skill (belum diverifikasi)
| Nama | Dipakai di | Status |
|---|---|---|
| gitleaks | secret-leak-scan (disebut sebagai alternatif) | Lisensi belum diverifikasi |
| trufflehog | secret-leak-scan (disebut sebagai alternatif) | Lisensi belum diverifikasi |
| terser | render-link-builder (disebut untuk minifikasi JS) | Lisensi belum diverifikasi |
| IEC 60909-0 | short-circuit-calculator (rumus dirujuk) | Standar berbayar; hanya rumus dirujuk, teks tidak disalin. Edisi terbaru perlu diverifikasi. |

## Lisensi skill di library ini
- Skill buatan ZY: `original-zy`. Kode bersifat milik pemilik repository. Jika repository dipublikasikan, pilih lisensi eksplisit (mis. MIT) setelah keputusan pemilik.
- Tidak ada kode pihak ketiga yang disalin ke dalam skill (lihat keputusan di atas).

## Provenance impor (diverifikasi dari clone lokal, 2026-11-25)

| Repository | Commit | Lisensi terverifikasi | Catatan |
|---|---|---|---|
| anthropics/skills | e4bb5d960d87126ff3b3a8af1a104b7db67560ba (2026-11-16) | Apache-2.0 per skill (`LICENSE.txt` di folder skill). Tidak ada LICENSE di root clone. | `doc-coauthoring` tidak punya file lisensi: BLOCKED, tidak diimpor. |
| obra/superpowers | 22f0b463e7a5e579904dd6211a520321035526f7 (2026-11-03) | MIT (LICENSE root, Copyright 2025 Jesse Vincent) | Disalin sebagai `LICENSE` ke tiap folder skill. |
| pymodbus-dev/pymodbus | 3.16.2 (PyPI) | BSD-3-Clause (metadata PyPI) | Dipakai oleh `modbus-tcp-client`. |
| e2nIEE/pandapower | 3.5.6 (PyPI) | Metadata PyPI kosong; BSD-3-Clause menurut LICENSE repository (pencarian web sebelumnya) | Dipakai oleh `load-flow-pandapower`. |

Dependensi uji (venv `tests/requirements-test.txt`) yang lisensinya belum saya verifikasi satu per satu: pypdf, reportlab, openpyxl, python-pptx, python-docx, pillow, imageio, numpy, defusedxml, lxml, PyYAML, playwright. Ini bukan dependensi runtime skill (kecuali yang disebut di SKILL.md masing-masing).

## Provenance v0.4 (lisensi dibaca dari file LICENSE clone, MIT pada ketujuhnya)
| Repository | Commit | Skill diimpor |
|---|---|---|
| haidrrrry/claude-remotion-skill | 1dcbe5e | remotion-motion-graphics |
| Liamrjohnston/remotion-motion-graphics-skill | b860c79 | cinematic-camera, terminal-inserts, article-highlights |
| kajisho5/ffmpeg-skill | 73436cb | ffmpeg-skill |
| alton47/threejs-skills | 7b8e256 | 14 skill threejs-* |
| MIGO-OvO/plc-skill | 82e5419 | plc-skill |
| zakariaf/Flutter-Skills | e073e5e | 8 skill Flutter |
| supabase/agent-skills | c9be0e9 | supabase, supabase-postgres-best-practices |
Tidak diimpor: remotion-dev/skills (tanpa LICENSE), full-stack-skills/threejs-skills dan flutter-skills (Apache-2.0, tidak dipilih), Liamrjohnston `motion-graphics` (tumpang tindih).

## Provenance v0.5 (lisensi MIT dari file LICENSE clone)
| Repository | Commit | Skill |
|---|---|---|
| siegerts/skill-canvas-video | 6419a14 | creating-canvas-video-animations |
| acelera-agency/html-animation | 8b88879 | motion-graphics (nama frontmatter upstream) |
| iart-ai/web-animation-skills | ed3a045 | svg-animation, accessible-animation, micro-interaction |
| calesthio/generative-media-skills | 8c85352 | audio-mixing-mastering |
| bianbianzhu/procedural-sfx | 5eff10f | procedural-sfx |
| meiiie/structured-root-cause-research-skill | bf2b7ef | structured-root-cause-research |
| K-Dense-AI/scientific-agent-skills | c21d13b | literature-review, citation-management (lisensi per-skill MIT pada metadata) |
| KalarisLabs/research-agent-skills | a74b0db | citation-verification |
Tidak diimpor (tanpa file LICENSE): Zacklinkk/svg-foundry-skill, RandyHaylor/audio-and-vocal-mastering.
Rujukan konstanta custom (belum diverifikasi ke dokumen primer): IEC 60255-151 (kurva inverse-time), IEC 60751 (Callendar-Van Dusen), NAMUR NE43 (batas fault 4-20 mA).

## Provenance v0.7
| Sumber | Commit / versi | Lisensi (dibaca dari berkas) | Dipakai di |
|---|---|---|---|
| evanclan/OpenJLPT | 0d1d341 | CC BY-SA 4.0 (LICENSE, NOTICE.md) | jlpt-curriculum/references/openjlpt |
| github/spec-kit | 3df7575 | MIT (LICENSE) | prd-engineering/references/spec-kit |
| joshyattridge/smartmoneyconcepts | 1b62fd6 (PyPI 0.0.27) | MIT (LICENSE, Copyright 2020 NeuralNine) | xauusd-smc-analysis (dependensi) |
| cmusphinx/pocketsphinx | f20ff1b (PyPI 5.1.1) | BSD (classifier PyPI; LICENSE sumber) | narration-subtitle-sync (dependensi dan fixture goforward) |
| ElevenLabs free tier | paket free, 10.000 karakter/bulan | layanan berbayar dengan kuota gratis | elevenlabs-narration |
Lisensi skill buatan ZY tetap MIT (LICENSE-ZY.md). Turunan data OpenJLPT wajib CC BY-SA 4.0.
