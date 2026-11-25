# BACKLOG v0.8

Dicatat pada 2026-11-25, dari baseline v0.7.0 (commit `7039fed`). Tidak ada item di sini yang sudah dikerjakan kecuali ditandai.
Kolom "Persetujuan" menunjukkan apakah langkah berikutnya memerlukan keputusan Anda.

## A. Router

| ID | Item | Bukti | Langkah berikutnya | Persetujuan |
|---|---|---|---|---|
| R1 | Set uji beku 20/23. Tiga miss: kueri "pilih teknologi..." jatuh ke remotion; "cek fps dan resolusi..." jatuh ke canvas; "ukuran posisi trading..." jatuh ke trade-statistics. | `benchmarks/router_labels_v07.json`, eksekusi pertama dan kedua | Perluas glosarium ("teknologi", "resolusi", "ukuran", "posisi") dan kurangi bonus nama untuk kata generik. Evaluasi pada **set baru**, bukan set beku ini. | Ya, untuk set uji baru |
| R2 | Routing hanya berbasis kata kunci. Tidak ada embedding dan tidak ada konteks percakapan. | `scripts/route_skill.py` | Evaluasi apakah pendekatan ini cukup setelah ada set uji dari pengguna. | Tidak |
| R3 | Konflik hanya untuk tiga skill yang punya metadata batasan. | `references/skill-constraints.json` | Tinjau skill lain yang punya larangan di deskripsinya. | Tidak |

## B. Verifikasi

| ID | Item | Bukti | Langkah berikutnya | Persetujuan |
|---|---|---|---|---|
| V1 | 40 skill VALIDATED dan 24 IMPORTED upstream belum diuji perilakunya. | Registry | Uji tugas nyata per skill yang benar-benar dipakai di proyek. | Ya, per proyek |
| V2 | Status VERIFIED pada skill custom baru berarti lulus test unit atau integrasi mekanismenya, **bukan** tugas produksi nyata. | `tests/skills/test_v07_*.py` | Putuskan definisi VERIFIED yang lebih ketat, lalu tandai ulang registry. | Ya |
| V3 | Konstanta IEC 60255-151 (kurva inverse-time), IEC 60751 (Callendar-Van Dusen), dan NAMUR NE43 belum diverifikasi ke dokumen primer. | `references/sources-and-licenses.md` | Verifikasi ke dokumen standar yang Anda miliki sebelum dipakai untuk setting. | Ya |
| V4 | `multi-agent-orchestration` hanya penjadwal DAG. Perilaku agen tidak dievaluasi. | `scripts/task_graph.py` | Uji pada tugas paralel nyata. | Ya |
| V5 | `quality-gate` tidak memeriksa loudness target atau kejernihan frame per frame. | `scripts/qc_gate.py` | Tambahkan pemeriksaan loudness lewat ffmpeg, jika diminta. | Ya |
| V6 | `strategy-backtesting` hanya crossover MA, tanpa slippage, tanpa multi-aset, dan belum diuji pada data pasar nyata. | `scripts/backtest.py` | Tambah model biaya dan data pasar yang lisensinya jelas. | Ya (lihat M1) |
| V7 | Kriteria Golden Master EarthStop belum didefinisikan. | — | Definisikan bersama pemilik proyek. | Ya |

## C. Blocked

| ID | Item | Alasan konkret | Langkah berikutnya | Persetujuan |
|---|---|---|---|---|
| B1 | Generasi live ElevenLabs. | Layanan sibuk pada sesi ("free generations are busy"). Kuota gratis tersedia: 297 dari 10.000 karakter terpakai. Tidak ada kredit dibeli. | Coba ulang generasi satu segmen pendek dengan `estimate_only` terlebih dahulu. | Tidak |
| B2 | Game mobile (Flutter / Flame). | Tidak ada Flutter SDK di sesi. Memasangnya besar dan memerlukan persetujuan. | Setujui pemasangan SDK jika proyek game akan dikerjakan. | Ya |
| B3 | Word alignment bahasa Jepang. | Tidak ada model Jepang offline yang terjangkau (host model tidak dapat diakses). | Pakai timing dari sumber pengguna (JSON), atau cari model yang lisensinya jelas dan terjangkau. | Ya |
| B4 | Discovery Codex. | `developers.openai.com` tidak dapat di-resolve dari sesi. | Buka akses hanya jika Anda menyetujuinya. | Ya |
| B5 | Akses GitHub dari Claude Chat dan Android. | Tidak ada bukti dari sesi. | Uji langsung di perangkat, lalu catat hasilnya. | Tidak |

## D. Belum selesai

| ID | Item | Bukti | Langkah berikutnya | Persetujuan |
|---|---|---|---|---|
| M1 | Data pasar berlisensi jelas. | Belum dicari pada v0.7. | Cari dan impor jika lisensinya kompatibel. | Ya |
| M2 | Standar instalasi PUIL. | Belum dicari. Tidak boleh dikarang. | Cari sumber yang dapat diverifikasi. | Ya |
| M3 | Grading warna (film dan manhwa), lettering dan tipografi Jepang, plot dan gaya prosa novel, konsistensi karakter dan timeline novel. | Matriks: MISSING | Tentukan prioritas, lalu buat skill baru. | Ya |
| M4 | Validasi render server ClipACanvas. | Endpoint belum diuji dari sesi ini. | Uji satu tautan render nyata. | Ya |
| M5 | Kebijakan disclaimer keuangan. | Matriks: MISSING | Tentukan bentuk (checklist atau skill). | Ya |
| M6 | Dataset kanji (KANJIDIC2, CC BY-SA) dan grammar OpenJLPT belum diimpor. Furigana dan tata bahasa belum dicakup. | `jlpt-curriculum` hanya memeriksa kosakata | Impor setelah keputusan lisensi share-alike. | Ya |
| M7 | Word alignment EN belum terhubung ke timing dari ElevenLabs. | Tidak ada format timing yang sudah diverifikasi | Verifikasi format keluaran dulu. | Ya |
| M8 | Kamera 3D hanya menghasilkan posisi. Tidak ada rotasi, easing, atau integrasi ke Three.js atau Remotion. | `scripts/camera_path.py` | Tambahkan rotasi dan adaptor renderer. | Ya |
| M9 | Manhwa tanpa balon dialog dan lettering. Novel tanpa tata letak cetak dan CJK vertikal. | `manhwa-production`, `novel-typesetting` | Tentukan lingkup. | Ya |
| M10 | Storyboard tanpa generasi gambar. Kontinuitas hanya memeriksa referensi registry. | `storyboard_lint.py` | Tentukan apakah generasi gambar termasuk. | Ya |
| M11 | Dokumenter tidak mengambil sumber dari web. Verifikasi sumber tetap oleh manusia. | `claim_ledger.py` | Tidak ada jika lingkup tetap. | Tidak |
| M12 | Troubleshooting kelistrikan dan SCADA: batas dan desain HMI harus dari SOP pengguna. | `fault_tree.py`, `tag_check.py` | Isi pohon dari SOP proyek. | Tidak |
| M13 | Digital twin hanya model termal satu node tanpa data pabrik. | `twin_rc.py` | Kalibrasi dengan data pengukuran. | Ya |
| M14 | Token efisiensi belum diukur. Hanya ukuran file yang dilaporkan. | `route_skill.py` | Ukur hanya jika runtime melaporkan token. | Ya |
| M15 | Artistic QC bergantung pada peninjau manusia. Belum ada peninjau yang ditetapkan. | `quality-gate` | Tetapkan peninjau untuk EarthStop. | Ya |
| M16 | Duplikasi folder `scripts/office/` di docx, pptx, dan xlsx. | Dibiarkan sesuai keputusan | Deduplikasi hanya jika diminta. | Ya |
| M17 | Upstream `cinematic-camera` tetap melarang neon. Override hanya ada di router dan belum divalidasi di proyek nyata. | `references/project-profiles.json` | Validasi pada EarthStop. | Ya |

## E. Infrastruktur dan dokumentasi

| ID | Item | Bukti | Langkah berikutnya | Persetujuan |
|---|---|---|---|---|
| I1 | `tests/requirements-test.txt` sebelumnya tidak lengkap. Sudah dikoreksi pada commit ini, tetapi **belum diuji pada venv bersih**. | Berkas `tests/requirements-test.txt` | Pasang ulang dari nol dan jalankan test. | Ya (menjalankan test) |
| I2 | Jalur URL GitHub pada `import_personal.py` belum diuji langsung. Test hanya memakai folder dan ZIP. | `tests/test_personal_import.py` | Uji dengan repository publik kecil. | Ya |
| I3 | Proses integrasi pengalaman EarthStop kembali ke library belum didefinisikan. | — | Definisikan setelah Golden Master disepakati. | Ya |
| I4 | Dokumentasi per skill berbahasa campuran dan belum seragam. | Registry | Tidak prioritas. | Tidak |

## Ringkasan
- Batasan utama: routing kata kunci (R1), status VERIFIED yang hanya berarti uji mekanisme (V2), dan skill upstream yang belum diuji perilakunya (V1).
- Blocker utama: ElevenLabs live (B1), Flutter SDK (B2), model Jepang (B3).
- Gap utama: data pasar berlisensi (M1), standar PUIL (M2), dan beberapa kebutuhan MISSING pada matriks.
