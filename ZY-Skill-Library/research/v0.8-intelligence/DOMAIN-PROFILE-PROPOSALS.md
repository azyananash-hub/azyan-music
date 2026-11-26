# DOMAIN-PROFILE-PROPOSALS: profil A–D dan analisis kapabilitas kreatif

Status: USULAN. Tidak ada perubahan pada `references/project-profiles.json`.

## 1. Temuan skema

- `project-profiles.json` berisi 14 profil. Setiap profil hanya memiliki tiga field: `name`, `preferred_categories` (menaikkan skor skill di kategori itu), dan `overrides` (batasan yang boleh dikesampingkan, beserta alasannya).
- Tidak ada pewarisan antarprofil.
- Konsekuensi: profil baru hanya bernilai jika menambah kategori yang berbeda atau override yang berbeda. Profil dengan kategori yang sama dengan profil yang sudah ada hanya menggandakan konfigurasi.

## 2. Keputusan per domain

### A. Cinematic Film & Narrative Production (acuan: Sebelum Sepi Menjadi Rumah)

- Profil yang ada: `film-sinematik` (creative-production, motion-graphics), `earthstop` (override cinematic-camera), `novel`, `sisi-gelap-tokoh`.
- Kapabilitas yang ada: cinematic-camera, cinematic-3d-camera, cinematic-storyboarding (CUSTOM), narration-subtitle-sync, elevenlabs-narration (live BLOCKED), audio-mixing-mastering, procedural-sfx, manhwa-production, ffmpeg-skill (reframe, caption, loudness).
- Celah: konsistensi karakter dan kontinuitas adegan belum ada skill. `storyboard_lint` hanya memeriksa referensi registry. Narasi bahasa Indonesia yang alami belum punya engine yang terbukti (lihat bagian 4).
- Keputusan: tidak ada profil baru sekarang. `film-sinematik` sudah mengarah ke kategori yang tepat. Profil `sebelum-sepi-menjadi-rumah` dibuat setelah brief tersedia, dan hanya jika ada override yang berbeda (misalnya batasan palet atau nada). Tanpa override, profil itu duplikat.
- Yang dibutuhkan dari pemilik: brief proyek (durasi, format, sumber naskah, dan batas nada).

### B. Commercial Advertising & Motion Graphics

- Profil yang ada: `amiraverse` (flutter, japanese-education; kebutuhan promo tercakup tetapi tidak dipisahkan), `film-sinematik` (creative-production, motion-graphics).
- Kapabilitas yang ada: remotion-motion-graphics, motion-graphics, micro-interaction, svg-animation, brand-guidelines, procedural-sfx, audio-mixing-mastering, ffmpeg-skill (format sosial).
- Celah: aturan hook dan CTA, panduan safe area per platform. Aset iklan yang dapat diedit sudah dicakup oleh Remotion karena berbasis kode.
- Keputusan: tidak ada profil baru. Preferensi kategorinya sama dengan `film-sinematik`. Aturan promosi (hook, CTA, durasi) dikerjakan sebagai skill konten setelah ada proyek iklan nyata. Kandidat konten: 35 (resep shot, P06) dan 36 (GSAP, P05).
- Yang dibutuhkan dari pemilik: perkiraan jumlah proyek iklan dalam 12 bulan.

### C. Android & Browser Game Development (acuan: Silent Neon Tokyo)

- Profil yang ada: `silent-neon-tokyo-game` (creative-production, software-development) dan `silent-neon-tokyo-manhwa`.
- Kapabilitas yang ada: game-mechanics (software-development), threejs-* (14, termasuk threejs-performance), threejs-animation, threejs-physics, accessibility-as-code (flutter), webapp-testing.
- Celah: sistem survival dan narasi belum punya skill. Panduan performa mobile belum ada (P07 mencakup sebagian). Build Android native belum tersedia. Flame memerlukan SDK, dan itu item B2 yang BLOCKED.
- Keputusan: tidak ada profil generik baru. Profil `silent-neon-tokyo-game` sudah mencakup kategori yang dibutuhkan. Profil generik `game-development` akan menduplikasi preferensi yang sama. Panduan mobile dan survival masuk sebagai skill yang dimuat lewat kategori yang sudah ada, setelah P07 disetujui.
- Android native di luar cakupan sampai ada keputusan Flutter atau Flame (B2).

### D. Industrial Water Treatment (WTP, WWTP, MMF/ACF, RO, dosing, pemantauan kualitas air, instrumentasi, automasi, dokumentasi)

- Profil yang ada: `teknik-elektro` (engineering, industrial-utility). Profil ini sudah mencakup kategori yang dibutuhkan.
- Kapabilitas yang sudah ada: `ro-mass-balance` (RO), `instrument-loop-calc` (instrumentasi), `scada-tag-engineering`, `plc-skill`, `modbus-tcp-client` (automasi), `steam-water-properties`, `industrial-energy-metrics`, `reliability-pm-metrics`, `cooling-tower-performance`, `boiler-efficiency-indirect`, `industrial-digital-twin`.
- Celah (belum ada skill): perhitungan MMF dan ACF (backwash, loading filter, metrik penyaringan); perhitungan dosing bahan kimia (kebutuhan, konsumsi, jadwal); pemantauan kualitas air (parameter, batas, pencatatan); dokumentasi proses (P04).
- Keputusan: tidak ada profil baru. Celah diisi dengan skill baru di kategori `industrial-utility`, yang sudah dipreferensikan `teknik-elektro`. Ini menghindari duplikasi dengan `ro-mass-balance`.
- Syarat: setiap angka standar harus diverifikasi dari dokumen primer. M2 (PUIL dan standar terkait) belum terverifikasi. Tidak ada angka desain yang dikarang.

## 3. Ringkasan keputusan profil

| Domain | Profil baru? | Tindakan | Keputusan pemilik yang dibutuhkan |
|---|---|---|---|
| A | Tidak (sekarang) | `sebelum-sepi-menjadi-rumah` hanya jika ada brief dan override | Brief proyek |
| B | Tidak | Skill aturan promosi setelah ada proyek iklan nyata | Jumlah proyek iklan |
| C | Tidak | Skill mobile dan survival setelah P07 | Android native (B2) |
| D | Tidak | Skill MMF/ACF, dosing, dan kualitas air di `industrial-utility` | Standar yang boleh dipakai |

Jumlah profil tetap 14 kecuali pemilik memutuskan lain.

## 4. Kapabilitas kreatif: analisis celah

Pembanding: Remotion (`remotion-motion-graphics`, sudah ada) dan FFmpeg (`ffmpeg-skill`, IMPORTED). Tidak ada rendering framework kedua yang diusulkan. HyperFrames (DEFER) dan komposer Remotion di OpenMontage (REJECT) akan menduplikasi Remotion.

| Kapabilitas | Yang sudah ada | Bukti kandidat | Celah sebenarnya | Tindakan |
|---|---|---|---|---|
| Narasi bahasa Indonesia yang alami | `elevenlabs-narration` (live BLOCKED); `narration-subtitle-sync` | Voicebox: tidak ada Indonesia (`languages.ts`). VoiceStudio: tidak ada Indonesia di engine (hanya normalisasi angka) | Belum ada engine TTS dengan bukti bahasa Indonesia | Perlu keputusan pemilik sebelum pencarian kandidat baru |
| Pengucapan Jepang yang alami | `japanese-education` (pembelajaran, bukan TTS) | Voicebox: bukti kode Jepang (`languages.ts:24`; Kokoro memerlukan misaki[ja]; suara Qwen Jepang). VoiceStudio: bukti kode Jepang | Kualitas pengucapan belum diukur | B-VOI-1 di mesin pemilik. Memerlukan unduhan model dan persetujuan |
| Storytelling sinematik | `film-sinematik`; `cinematic-camera`; `cinematic-storyboarding` | 35 Video Shotcraft (P06, resep kamera) | Kecil | P06 |
| Motion graphics | `remotion-motion-graphics`; `motion-graphics` | 36 GSAP (P05) | Kecil | P05 untuk motion berbasis HTML |
| Sinkronisasi audio-visual | `narration-subtitle-sync`; `audio-mixing-mastering` | Tidak ada kandidat sinkronisasi beat | Sinkronisasi beat belum dievaluasi | Tidak diusulkan sekarang |
| SFX dan ambience | `procedural-sfx` (IMPORTED); `audio-mixing-mastering` | Tidak ada kandidat tambahan | Ambience berlapis belum eksplisit | Dicatat tanpa kandidat |
| Explainer teknis | Tidak ada skill diagram | 27 Diagram Design (P04) | Celah nyata (C20) | P04 |
| Realistic 3D environments | `threejs-*` (14) | 39a Blender (BL-1, BLOCKED); 42 3Dviz (DEFER) | Pipeline aset 3D | Menunggu keputusan item 39 |
| Karakter yang konsisten | `manhwa-production`; `storyboard_lint` (hanya referensi) | Tidak ada kandidat. Kontinuitas memakai memori proyek (P12) | Konsistensi karakter lintas adegan belum ada | Dicatat sebagai celah. Bergantung pada P12 |
| Aset yang dapat diedit | Remotion dan FFmpeg berbasis kode; `threejs-*` | 39a (export-pipelines) | Pipeline aset 3D belum ada | Menunggu item 39 |
| QA video akhir | `quality-gate` (video; belum ada loudness dan frame, V5); `ffmpeg-skill` (loudness, disebut dalam deskripsi) | 37 Motionmaxxing (rubrik); 22 Impeccable (kritik desain) | Pemeriksaan loudness dan frame belum ada di quality-gate | Usulkan V5 sebagai item backlog dengan pengukuran loudness FFmpeg. Tidak perlu renderer baru |

Kesimpulan: tidak ada kebutuhan rendering framework kedua. Remotion dan FFmpeg sudah menutup render dan edit.

## 5. Ringkasan

- Tidak ada profil baru yang diusulkan sekarang. Dasarnya: skema hanya berisi kategori dan override. Profil baru baru bernilai jika override-nya berbeda.
- Celah kreatif yang nyata: bahasa Indonesia untuk TTS, pengucapan Jepang (perlu benchmark), karakter yang konsisten, pipeline aset 3D (menunggu item 39), QA loudness dan frame, dan diagram teknis (P04).
