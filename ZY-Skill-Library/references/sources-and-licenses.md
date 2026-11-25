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
