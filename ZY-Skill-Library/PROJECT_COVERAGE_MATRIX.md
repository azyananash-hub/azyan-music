# PROJECT COVERAGE MATRIX (v0.7, tahap audit)

Dasar: `SKILL_REGISTRY.json` (98 skill) dan deskripsi skill. Tidak ada skill baru dibuat pada tahap ini.

## Legenda klasifikasi
- **COVERED**: skill berstatus VERIFIED memenuhi kebutuhan inti, dan ada test yang membuktikannya.
- **PARTIAL**: sebagian kebutuhan tercakup, atau cakupannya hanya dari skill yang belum diuji.
- **UNTESTED**: ada skill yang tampaknya memenuhi kebutuhan, tetapi belum ada bukti perilaku (VALIDATED atau IMPORTED).
- **MISSING**: tidak ada skill yang relevan, atau sumber terverifikasinya belum ditemukan.

Status mengikuti registry: VERIFIED = diuji nyata; VALIDATED = struktur, lisensi, dan risiko lolos, perilaku belum diuji; IMPORTED = smoke sintaks saja.

## 1. AmiraVerse (aplikasi belajar bahasa Jepang, Flutter)
| Kebutuhan | Klasifikasi | Skill (status) | Catatan |
|---|---|---|---|
| Arsitektur dan state Flutter | UNTESTED | flutter-architecture, state-management-riverpod (VALIDATED) | Tidak ada proyek Flutter di repo ini; tidak bisa dijalankan. |
| Navigasi, persistensi, i18n, aksesibilitas | UNTESTED | navigation-and-routing, persistence-drift, i18n-rtl-l10n, accessibility-as-code (VALIDATED) | Uji perlu SDK Flutter dan proyek nyata. |
| Strategi pengujian dan async | UNTESTED | testing-strategy, async-safety (VALIDATED) | Sama. |
| Jadwal review kosakata | COVERED | fsrs-scheduler, srs-sm2-scheduler (VERIFIED) | Unit test lulus. |
| Backend dan RLS Supabase | UNTESTED | supabase, supabase-postgres-best-practices (VALIDATED) | Belum diuji terhadap proyek Supabase. |
| Desain UI/UX | UNTESTED | frontend-design (IMPORTED) | Instruksi saja. |

## 2. ZII Industrial Intelligence
| Kebutuhan | Klasifikasi | Skill (status) | Catatan |
|---|---|---|---|
| Hubung singkat | COVERED | short-circuit-calculator (VERIFIED) | Hanya 3 fasa simetris. |
| Load flow | COVERED | load-flow-pandapower (VERIFIED) | Jaringan kecil. |
| Proteksi arus lebih | PARTIAL | overcurrent-relay-curves (VERIFIED) | Hanya bentuk kurva; tidak ada koordinasi antar-relai. Konstanta belum diverifikasi ke dokumen IEC. |
| Transformator | COVERED | transformer-rating-regulation (VERIFIED) | Pendekatan regulasi. |
| Motor control | PARTIAL | motor-starting-sizing (VERIFIED) | Tanpa VFD dan soft starter. |
| Instrumentasi | COVERED | instrument-loop-calc (VERIFIED) | 4-20 mA dan Pt100 saja. |
| PLC programming dan troubleshooting | PARTIAL | plc-skill (VALIDATED), modbus-tcp-client (VERIFIED) | Logika PLC belum diuji; Modbus sudah. |
| Digital twin industri | MISSING | - | Tidak ada sumber terverifikasi. |
| Troubleshooting kelistrikan | MISSING | - | Tidak ada sumber terverifikasi. |
| Preventive maintenance dan RCA | PARTIAL | reliability-pm-metrics, fmea-rpn-prioritizer (VERIFIED), structured-root-cause-research (VALIDATED) | RCA belum diuji. |
| Energi industri | COVERED | industrial-energy-metrics (VERIFIED) | Qc dan kWh per unit. |
| Utilitas (boiler, cooling tower, RO, uap) | COVERED | boiler-efficiency-indirect, cooling-tower-performance, ro-mass-balance, steam-water-properties (VERIFIED) | Data sintetis berlabel. |

## 3. DEAMIRA (ide ke spesifikasi teknis)
| Kebutuhan | Klasifikasi | Skill (status) | Catatan |
|---|---|---|---|
| PRD dan spesifikasi | PARTIAL | brainstorming, writing-plans (IMPORTED) | Tidak ada template PRD. spec-kit (MIT, terverifikasi sebelumnya) belum diimpor. |
| Handoff ke AI coding | PARTIAL | writing-plans, executing-plans (IMPORTED) | Belum diuji. |
| Orkestrasi multi-agent | PARTIAL | dispatching-parallel-agents, subagent-driven-development (IMPORTED) | Belum diuji. |
| Dokumen keluaran | COVERED | docx (VERIFIED) | |
| Riset terstruktur | UNTESTED | structured-root-cause-research (VALIDATED) | |

## 4. Silent Neon Tokyo — Game
| Kebutuhan | Klasifikasi | Skill (status) | Catatan |
|---|---|---|---|
| Game mobile (engine, loop, input) | MISSING | - | Tidak ada skill game engine. |
| Karakter konsisten | MISSING | - | |
| SFX dan musik | UNTESTED | procedural-sfx (VALIDATED), audio-mixing-mastering (VALIDATED) | |
| Visual 3D | UNTESTED | threejs-* (14, VALIDATED) | |
| Dialog dan narasi suara | PARTIAL | narration-subtitle-sync (VERIFIED) | Tanpa TTS neural. |
| Naskah dan cerita | MISSING | - | |

## 5. Silent Neon Tokyo — Manhwa
| Kebutuhan | Klasifikasi | Skill (status) | Catatan |
|---|---|---|---|
| Panel dan komposisi | MISSING | canvas-design (IMPORTED, untuk seni umum) | Tidak untuk halaman komik. |
| Lettering dan tipografi Jepang | MISSING | - | |
| Karakter konsisten | MISSING | - | |
| Ekspor PNG/PDF | PARTIAL | pdf (VERIFIED), canvas-design (IMPORTED) | |
| Validasi teks Jepang | MISSING | - | |

## 6. SISI GELAP TOKOH (dokumenter pendek)
| Kebutuhan | Klasifikasi | Skill (status) | Catatan |
|---|---|---|---|
| Storyboard | PARTIAL | cinematic-camera (VALIDATED) | Batasan estetika bertentangan dengan brief (lihat EarthStop). |
| Narasi | PARTIAL | narration-subtitle-sync (VERIFIED) | Tanpa TTS dan tanpa alignment per kata. |
| Subtitle | PARTIAL | narration-subtitle-sync (VERIFIED) | Hanya skala linier ke durasi audio. |
| Mixing dan mastering | UNTESTED | audio-mixing-mastering (VALIDATED) | |
| Verifikasi sumber sejarah | UNTESTED | citation-verification, literature-review (VALIDATED) | |
| Visual motion | UNTESTED | remotion-motion-graphics (VALIDATED), ffmpeg-skill (VERIFIED, resep) | |
| Color grading | MISSING | - | |

## 7. EarthStop
| Kebutuhan | Klasifikasi | Skill (status) | Catatan |
|---|---|---|---|
| Storyboard dan kamera | PARTIAL | cinematic-camera (VALIDATED) | **Cacat nyata:** aturan anti-neon dan larangan gradient berlaku keras dan bertentangan dengan brief. |
| Narasi ElevenLabs | MISSING | - | Tool MCP ElevenLabs terdaftar di sesi, tetapi berbayar dan belum ada skill. |
| Subtitle per kata | PARTIAL | narration-subtitle-sync (VERIFIED) | Hanya per baris. |
| Pemilihan teknologi | MISSING | - | Tidak ada panduan keputusan. |
| QC artistik | MISSING | - | QC yang ada hanya teknis. |
| Motion | UNTESTED | remotion-motion-graphics (VALIDATED) | |
| Render dan encode | COVERED | ffmpeg-skill (VERIFIED, resep) | |

## 8. ClipACanvas
| Kebutuhan | Klasifikasi | Skill (status) | Catatan |
|---|---|---|---|
| Direct render link sesuai protokol | COVERED | render-link-builder (VERIFIED) | Resolusi, FPS, durasi, auto=true, minified. |
| Animasi HTML canvas | UNTESTED | creating-canvas-video-animations (VALIDATED) | |
| Validasi render di server | MISSING | - | Endpoint belum diuji dari sesi ini. |
| Motion graphics vertikal | PARTIAL | motion-graphics (VALIDATED) | |

## 9. Money App
| Kebutuhan | Klasifikasi | Skill (status) | Catatan |
|---|---|---|---|
| Budget dan tabungan | PARTIAL | compound-savings-projection (VERIFIED) | Tidak ada pelacak budget. |
| Laporan | PARTIAL | xlsx, pdf (VERIFIED) | |
| Backend dan data pengguna | UNTESTED | supabase (VALIDATED) | |
| Keamanan kredensial | COVERED | secret-leak-scan (VERIFIED) | |
| Kebijakan disclaimer keuangan | MISSING | - | |

## 10. Produksi film sinematik
| Kebutuhan | Klasifikasi | Skill (status) | Catatan |
|---|---|---|---|
| Storyboard | PARTIAL | cinematic-camera (VALIDATED) | Sama dengan EarthStop. |
| 3D sinematik | UNTESTED | threejs-* (VALIDATED) | |
| Suara, SFX, mix | UNTESTED | procedural-sfx, audio-mixing-mastering (VALIDATED) | |
| VFX dan encode | PARTIAL | ffmpeg-skill (VERIFIED) | Hanya trim dan reframe yang diuji. |
| Konsistensi karakter | MISSING | - | |
| Grading warna | MISSING | - | |

## 11. Penulisan novel
| Kebutuhan | Klasifikasi | Skill (status) | Catatan |
|---|---|---|---|
| Struktur plot dan outline | MISSING | - | |
| Gaya prosa | MISSING | - | |
| Konsistensi karakter dan timeline | MISSING | - | |
| Format naskah dan ekspor | PARTIAL | docx (VERIFIED) | |
| Riset latar non-fiksi | UNTESTED | literature-review (VALIDATED) | |

## 12. XAUUSD ICT/SMC
| Kebutuhan | Klasifikasi | Skill (status) | Catatan |
|---|---|---|---|
| Position sizing | COVERED | position-size-calculator (VERIFIED) | |
| Statistik backtest | COVERED | trade-statistics (VERIFIED) | |
| Metrik portofolio | COVERED | portfolio-metrics-quantstats (VERIFIED) | |
| Engine backtest berbasis bar | MISSING | - | backtesting.py berlisensi AGPL-3.0; tidak dipakai. |
| Analisis konsep ICT/SMC | MISSING | - | Tidak ada sumber terverifikasi; tidak boleh diarang. |
| Data historis berlisensi | MISSING | - | Perlu sumber yang lisensinya jelas. |

## 13. Teknik Elektro dan Industrial Utility
| Kebutuhan | Klasifikasi | Skill (status) | Catatan |
|---|---|---|---|
| Hubung singkat, load flow, trafo, motor, instrumentasi, utilitas | COVERED | lihat bagian 2 | |
| Proteksi (koordinasi) | PARTIAL | overcurrent-relay-curves | |
| Troubleshooting kelistrikan | MISSING | - | |
| Standar instalasi (mis. PUIL) | MISSING | - | Tidak ada sumber terverifikasi; tidak boleh dikarang. |

## 14. Pembelajaran JLPT N5–N1
| Kebutuhan | Klasifikasi | Skill (status) | Catatan |
|---|---|---|---|
| Jadwal SRS | COVERED | fsrs-scheduler, srs-sm2-scheduler (VERIFIED) | |
| Kurikulum per level | MISSING | - | |
| Dataset kosakata dan kanji berlabel | MISSING | - | Perlu sumber dengan lisensi jelas. |
| Validasi bahasa Jepang | MISSING | - | Furigana, level kanji, tata bahasa. |
| Narasi audio | MISSING | - | |
| Subtitle | PARTIAL | narration-subtitle-sync (VERIFIED) | |

## Kemampuan lintas proyek (P0 dan P1)
| Kemampuan | Klasifikasi | Catatan |
|---|---|---|
| Context-aware routing | PARTIAL | Router kata kunci dengan IDF; 21/21 pada label buatan sendiri. Belum ada konteks proyek dan konflik. |
| Konflik skill dan brief | MISSING | Belum ada metadata konflik. |
| Pemilihan teknologi berdasarkan kualitas | MISSING | |
| Quality gate: validitas teknis vs kualitas hasil | MISSING | Gate yang ada hanya teknis. |
| Efisiensi token | UNTESTED | Belum diukur. Runtime sesi tidak melaporkan token per tugas. |
| ElevenLabs narration | MISSING | Tool MCP terdaftar; berbayar; belum ada skill. |
| Cinematic 3D | PARTIAL | threejs-* dan remotion (VALIDATED). |
| Cinematic storyboarding | PARTIAL | cinematic-camera (VALIDATED), bermasalah pada brief. |
| JLPT curriculum engineering | MISSING | |
| Japanese language validation | MISSING | |
| Multi-agent orchestration | PARTIAL | IMPORTED, belum diuji. |
| Industrial digital twin | MISSING | |
| PRD engineering | PARTIAL | Lihat DEAMIRA. |
| AI coding handoff | PARTIAL | Lihat DEAMIRA. |
| Mobile game development | MISSING | |
| Character consistency | MISSING | |
| XAUUSD ICT analysis | MISSING | |
| XAUUSD backtesting | PARTIAL | Statistik dan sizing sudah ada; engine bar belum. |

## Ringkasan hitungan
Dihitung dari seluruh baris tabel: **16 COVERED, 29 PARTIAL, 18 UNTESTED, 39 MISSING** (102 baris; bagian 13 merujuk bagian 2 sehingga sebagian baris tidak berdiri sendiri).

## Roadmap v0.7 (usulan, menunggu persetujuan)
Urutan mengikuti gap aktual dan dependensi. Setiap fase punya metode uji; klaim VERIFIED hanya setelah uji nyata.

| Fase | Pekerjaan | Dependensi | Metode uji | Keputusan yang dibutuhkan |
|---|---|---|---|---|
| A1 (P0) | Konteks proyek dan konflik brief di router: profil proyek dan metadata `conflicts_with` per skill, tanpa mengubah router secara besar | - | Label diperluas (>=60 kueri, termasuk brief EarthStop dan kueri negatif); ukur top-1 dan keberadaan peringatan konflik | Tidak ada |
| A2 (P0) | Quality gate dipisah: TEKNIS (otomatis) dan ARTISTIK (rubrik manusia, status NOT TESTED sampai ditinjau) | - | Gate teknis diuji; gate artistik tidak pernah lolos otomatis | Siapa peninjau artistik |
| A3 (P0) | Panduan pemilihan teknologi per target kualitas (Remotion, Three.js, Canvas, FFmpeg) | Bukti dari fase B | Konsistensi tabel diperiksa terhadap status skill | Tidak ada |
| A4 (P0) | Ukuran efisiensi: byte SKILL.md dan jumlah referensi yang dimuat per tugas (tanpa klaim token) | A1 | Skrip menghitung ukuran; token NOT TESTED | Tidak ada |
| B1 (EarthStop) | Penanganan `cinematic-camera`: override brief lewat metadata konflik di A1, **tanpa mengubah isi upstream** | A1 | Kueri brief EarthStop harus menampilkan peringatan konflik | Setujui opsi override (disarankan) atau ADAPTED copy |
| B2 (EarthStop) | Alignment per kata | Sumber timing kata | Akurasi pada audio uji dengan timing acuan | Pilih sumber: timing dari pengguna, atau aligner lokal (cek ukuran model) |
| C1 (P1) | ElevenLabs narration pipeline | Kunci API pengguna; kredit berbayar | Tidak ada tanpa biaya; uji hanya setelah persetujuan biaya | **Persetujuan biaya dan batas kredit wajib** |
| C2 (P1) | JLPT curriculum dan validasi bahasa Jepang | Sumber dataset berlisensi | Validator diuji pada sampel berlabel | Setujui pencarian sumber data berlisensi |
| C3 (P1) | PRD engineering dan AI coding handoff (template dan pemeriksaan kelengkapan) | spec-kit (MIT) jika diimpor | Pemeriksaan struktur spesifikasi pada contoh berlabel | Setujui impor spec-kit |
| C4 (P1) | Industrial digital twin, troubleshooting kelistrikan | Sumber terverifikasi | Simulasi pada data sintetis berlabel | Sumber mana yang diterima |
| C5 (P1) | XAUUSD backtesting engine | Engine bar; hindari AGPL | Statistik diuji terhadap data sintetis berlabel | Setujui sumber engine dan data |
| C6 (P1) | Mobile game dan character consistency | Lisensi engine | Uji build hanya bila SDK tersedia | Setujui engine |
| C7 (P1) | Cinematic 3D dan storyboarding terintegrasi | A1, B1 | Storyboard diperiksa terhadap brief | Tidak ada |

Prioritas yang disarankan: A1 lalu B1, karena keduanya langsung memperbaiki kegagalan EarthStop. A2 dikerjakan paralel karena tidak bergantung pada apa pun.

## Hasil implementasi v0.7 (sebelum → sesudah)

Metode: setiap baris MISSING dan PARTIAL dari tabel di atas dinilai ulang setelah implementasi. Klasifikasi baru mengikuti bukti uji. Angka sebelum dihitung dari tabel asli.

| Kebutuhan (sebelum) | Sesudah | Skill / bukti |
|---|---|---|
| Digital twin industri | PARTIAL | industrial-digital-twin (analitik RC teruji; belum ada data pabrik) |
| Troubleshooting kelistrikan (ZII) | PARTIAL | electrical-troubleshooting (mesin pohon teruji; batas harus dari SOP pengguna) |
| Game mobile (engine, loop, input) | BLOCKED | Flutter SDK tidak tersedia di sesi, sehingga build dan verifikasi tidak bisa dilakukan |
| Karakter konsisten (film) | PARTIAL | cinematic-storyboarding (registry kostum/palet teruji) |
| Naskah dan cerita (game) | MISSING | tidak ada skill plot |
| Panel dan komposisi (manhwa) | PARTIAL | manhwa-production (layout dan urutan baca teruji) |
| Lettering dan tipografi Jepang | MISSING | tidak ada skill |
| Karakter konsisten (manhwa) | PARTIAL | cinematic-storyboarding (pola registry yang sama) |
| Validasi teks Jepang (manhwa) | MISSING | jlpt-curriculum hanya memeriksa kosakata, bukan dialog |
| Color grading | MISSING | tidak ada skill |
| Narasi ElevenLabs | PARTIAL | elevenlabs-narration (planner dan kuota teruji; generasi live BLOCKED sementara, layanan sibuk) |
| Pemilihan teknologi | PARTIAL | technology-selection (mekanisme teruji; penilaian matriks kualitatif) |
| QC artistik | PARTIAL | quality-gate (rubrik teruji; penilaian tetap oleh manusia) |
| Validasi render di server | MISSING | endpoint ClipACanvas belum diuji dari sesi ini |
| Kebijakan disclaimer keuangan | MISSING | belum dibuat sebagai skill |
| Konsistensi karakter (film) | PARTIAL | cinematic-storyboarding |
| Grading warna | MISSING | tidak ada skill |
| Struktur plot dan outline | MISSING | tidak ada skill |
| Gaya prosa | MISSING | tidak ada skill |
| Konsistensi karakter dan timeline (novel) | MISSING | hanya registry karakter untuk storyboard |
| Engine backtest berbasis bar | PARTIAL | strategy-backtesting (crossover MA, eksekusi open t+1, teruji) |
| Analisis konsep ICT/SMC | PARTIAL | xauusd-smc-analysis (deteksi FVG dan swing teruji; interpretasi tidak) |
| Data historis berlisensi | MISSING | belum dicari pada tahap ini |
| Troubleshooting kelistrikan (Teknik Elektro) | PARTIAL | electrical-troubleshooting |
| Standar instalasi (PUIL) | MISSING | belum dicari; tidak boleh dikarang |
| Kurikulum per level | PARTIAL | jlpt-curriculum (7.811 entri, cakupan per level teruji) |
| Dataset kosakata dan kanji berlabel | PARTIAL | OpenJLPT vocab (CC BY-SA 4.0); kanji belum diimpor |
| Validasi bahasa Jepang | PARTIAL | jlpt-curriculum (kana dan jenis penulisan; tanpa tata bahasa) |
| Narasi audio | PARTIAL | elevenlabs-narration |
| Konflik skill dan brief | PARTIAL | router: override dan konflik teruji untuk 3 skill yang punya metadata batasan |
| Pemilihan teknologi berdasarkan kualitas | PARTIAL | technology-selection |
| Quality gate teknis vs artistik | PARTIAL | quality-gate |
| ElevenLabs narration | PARTIAL | elevenlabs-narration |
| JLPT curriculum engineering | PARTIAL | jlpt-curriculum |
| Japanese language validation | PARTIAL | jlpt-curriculum |
| Industrial digital twin | PARTIAL | industrial-digital-twin |
| Mobile game development | BLOCKED | sama dengan baris game mobile |
| Character consistency | PARTIAL | cinematic-storyboarding |
| XAUUSD ICT analysis | PARTIAL | xauusd-smc-analysis |

**Ringkasan 39 MISSING:** 25 menjadi PARTIAL, 2 menjadi BLOCKED, 12 tetap MISSING (termasuk 2 yang belum dicari pada tahap ini: data pasar berlisensi dan standar PUIL).

Kebutuhan yang sebelumnya PARTIAL (29 baris) tetap PARTIAL: cakupannya memang belum lengkap (misalnya proteksi hanya kurva, motor tanpa VFD). Beberapa mendapat bukti uji yang lebih kuat, tetapi belum ada yang naik ke COVERED.

**Catatan jujur:** klasifikasi COVERED tidak bertambah. Semua fungsi baru memiliki test, tetapi keputusan kreatif, penilaian artistik, dan pengujian di runtime (ElevenLabs live, render server, Flutter) belum tercakup.
