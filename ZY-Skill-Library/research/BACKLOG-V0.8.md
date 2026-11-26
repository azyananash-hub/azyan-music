# BACKLOG v0.8

Dicatat pada 2026-11-25, dari baseline v0.7.0 (commit `7039fed`). Tidak ada item di sini yang sudah dikerjakan kecuali ditandai.
Kolom "Persetujuan" menunjukkan apakah langkah berikutnya memerlukan keputusan Anda.

Checkpoint riset: commit yang memuat revisi ini (hash ada di `git log` dan laporan chat). Frozen code baseline: `7039fed`. Frozen snapshot sebelumnya: `940368f`. Ini research checkpoint, **bukan** implementation baseline.

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

---

# F. Kandidat riset v0.8: Firecrawl, Claude-BugHunter, Google Stitch

**Ringkasan eksekutif:** tidak ada kandidat yang layak di-ADOPT langsung. Tiga kandidat menghasilkan sembilan item backlog (K1–K9) setelah duplikasi digabung. Prioritas P1: K2 (review keamanan defensif), K1 (pipeline DESIGN.md), K8 (sinkronisasi dokumen), dan K9 (keputusan pengguna). Semua item menunggu persetujuan. Tidak ada yang diimplementasikan.

**Aturan tetap** (berlaku untuk F–H, tidak diulang per item):
- Read-only untuk audit. Tidak ada instalasi, eksekusi kode pihak ketiga, atau perubahan kode. Commit dan push hanya untuk checkpoint riset yang disetujui (bagian I).
- Baseline tetap: frozen code `7039fed`; snapshot sebelumnya `940368f`. PROGRESS.md dan CHANGELOG.md tidak diubah.
- Anggaran Rp0. Layanan berbayar, atau layanan cloud dengan biaya belum terverifikasi, tidak diadopsi.
- Setiap ADAPT dan ADOPT menunggu persetujuan. Lisensi dicatat ke `references/sources-and-licenses.md` setelah keputusan disetujui.
- Sumber: clone publik shallow di `/home/user/ext/` (di luar repository).

Singkatan: **ADOPT** (pakai apa adanya), **ADAPT** (tulis ulang dengan batasan), **MERGE** (digabung ke item K), **REJECT** (tidak dipakai), **DEFER** (menunggu bukti atau keputusan).

**Revisi draf.** Klaim berikut sudah dikoreksi: "tidak ada skill yang melakukan web fetch" (tiga SKILL.md menyebut WebFetch); "teks saja" untuk taste-design dan design-md (keduanya memerlukan akses Stitch); "13 dari 16 skill punya izin web_fetch" (yang terverifikasi: 13 SKILL.md menyebut `web_fetch`); "hunt-laravel" dan false positive `| python3` (dihapus, belum ditinjau); "butuh akun Google" (tidak ada di README); "sekitar 50 kelas hunt-*" (angka pasti: 58).

## F. Firecrawl

Repositori: main `98ae8c7` (AGPL-3.0); plugin `d6e42a4` (MIT); mcp-server `f5488e4` (MIT); skills `1d4b072` (ISC).

Bukti:
- `firecrawl-crawl` dan `firecrawl-download` mewajibkan autentikasi ("no keyless free tier", baris 14). `firecrawl-developer-index` keyless dengan batas laju.
- `docker-compose.yaml` mendefinisikan 7 service: playwright-service, api, redis, rabbitmq, nuq-postgres, foundationdb, foundationdb-init. Volume bernama hanya `fdb-data` dan `fdb-cluster-file`. Redis, RabbitMQ, dan NuQ-Postgres tidak punya volume, sehingga datanya hilang saat container dihapus.
- Audit awal: `USE_DB_AUTHENTICATION=false` secara default, sehingga API tidak berautentikasi.
- Konversi HTML lokal ke Markdown: `index.html` 70.869 → 11.754 B (0,166); `interactive_forecast.html` 153.063 → 458 B (0,003); `_review.html` 97.536 → 12 B (0,000). Rasio sekecil itu berarti sebagian besar isi tidak terbawa. Dugaan penyebabnya konten yang dirender JavaScript, tetapi belum dibandingkan dengan hasil render.
- 37 SKILL.md, total 173.381 B.

| ID | Kemampuan | Keputusan | Alasan dan syarat | Digabung ke |
|---|---|---|---|---|
| FC-01 | Layanan cloud (scrape, search, crawl, map, download) | DEFER | Crawl dan download mewajibkan autentikasi. Data keluar ke pihak ketiga. WebSearch bawaan sudah tersedia di sesi ini, dan pengambilan halaman bisa lewat agen web-fetch, sehingga nilai tambah search dan scrape terbatas. | — |
| FC-02 | Self-host (7 service) | DEFER | Rp0 hanya jika mesin memadai; persyaratan hardware tidak didokumentasikan dan belum diuji. API tanpa autentikasi secara default. AGPL perlu ditinjau jika layanan dijalankan untuk pihak lain. | — |
| FC-03 | MCP server `firecrawl-mcp` 3.41.0 (MIT) | REJECT | `npx -y` tanpa versi terkunci. Butuh `FIRECRAWL_API_KEY` atau `FIRECRAWL_API_URL`. | — |
| FC-04 | Plugin Claude (manifest saja, tanpa hook) | REJECT | Tidak menambah kemampuan. | — |
| FC-05 | Skill bisnis (lead, kontak, lowongan, toko, fantasy sports, intel kompetitor) | REJECT | Tidak relevan dengan 14 profil. Pengumpulan kontak berisiko privasi. | — |
| FC-06 | Pola "Markdown-first" untuk scrape dan parse | MERGE | Sama dengan FC-07 dan `markitdown-converter` yang sudah ada. | K4 |
| FC-07 | Penghematan token dengan Markdown lokal | ADAPT (dengan guard) | Perluas `markitdown-converter` dengan deteksi kehilangan konten dan fallback untuk halaman JavaScript. Estimasi token memakai 4 karakter per token, bukan tokenizer. | K4 |

## G. Claude-BugHunter (commit `6a2153d`)

Lisensi: kode **MIT**; konten **CC BY 4.0** (`LICENSE-CONTENT`). README memuat sponsor komersial.

Klaim: README menyebut "battle-tested across authorized red-team and bug-hunting engagements". `ENGAGEMENTS.md` berisi catatan dari pengelola repository. Catatan itu tidak dapat diverifikasi secara independen dari sini.

Inventaris: 84 SKILL.md. 58 bernama `hunt-*`; 26 lainnya adalah skill red-team, OSINT, dan rekon (mis. `enterprise-vpn-attack`, `m365-entra-attack`, `okta-attack`, `vmware-vcenter-attack`, `apk-redteam-pipeline`, `ios-redteam-pipeline`, `supply-chain-attack-recon`, `offensive-osint`). Total 1.684.794 B; terbesar `osint-methodology` 94.368 B (≈23 ribu token).

Isi (audit awal): 58 dari 84 skill memuat heading payload, exploit, atau bypass. Heading Mitigation: 0 dari 84; Remediation: 1; Fix: 18; Detection: 48; Secure: 9.

Pencarian heading tambahan (`mitigat|remediat|fix|detect|secur|defen|prevent`) menemukan cocokan di 60 file (183 kemunculan). Kata "fix" dan "secur" juga muncul pada konteks ofensif, sehingga angka ini tidak mengukur kontrol defensif secara sahih.

| ID | Kemampuan | Keputusan | Alasan dan syarat | Digabung ke |
|---|---|---|---|---|
| CB-01 | 58 skill `hunt-*` dan 26 skill red-team/OSINT lainnya | REJECT | Berisi payload dan langkah eksploitasi; dual-use; tidak defensif. | — |
| CB-02 | Checklist authz (IDOR), autentikasi (JWT, session, OAuth), dan API (CORS, GraphQL, shadow API) | ADAPT (ruang lingkup dipersempit) | Tulis ulang sebagai review statis dengan langkah mitigasi, tanpa payload. RLS sudah disebut di `supabase` dan `supabase-postgres-best-practices`; bagian itu dikecualikan setelah diff. Butuh persetujuan. | K2 |
| CB-03 | Triage, evidence, dan format laporan | ADAPT (format saja) | Ambil struktur laporan; buang langkah eksploitasi. Pencarian `triage\|vulnerab\|kerentanan\|pentest\|owasp\|penetrasi` di registry tidak menemukan skill pelaporan kerentanan. | K2 |
| CB-04 | Deteksi kebocoran (`hunt-source-leak`) | ADAPT (versi defensif) | Ubah menjadi pemeriksaan artefak build milik sendiri: source map, `.git` yang terbuka, `.env` di dalam artefak. Tidak memindai target eksternal. | K3 |
| CB-05 | Dependensi dan CVE (`refresh-cve-index.py`) | DEFER | Pencarian `vulnerab` di registry nihil. Sumber CVE (NVD, OSV) perlu diverifikasi lisensi dan aksesnya. | K6 |
| CB-06 | `supply-chain-attack-recon` | REJECT | Rekon ofensif terhadap paket pihak ketiga. | — |
| CB-07 | `install.sh` | REJECT | Menulis ke `~/.claude`, `~/.agents`, `~/.hermes`, `~/.gemini`; menambah baris `source` ke `~/.zshrc` atau `~/.bashrc`; `rm -rf` pada target; memotong deskripsi skill diam-diam di salinan. Installer ZY sudah ada (dry-run default). | — |
| CB-08 | `install-community-skills.sh` | REJECT | Clone repository pihak ketiga, lalu menjalankan `echo "n" \| ./install.sh` dari repo itu. Mengeksekusi kode yang belum diperiksa. | — |
| CB-09 | `setup_harness_mcp.py` | REJECT | Membaca `~/.claude.json`; menulis `~/.config/opencode/opencode.json` dan `~/.gemini/config/mcp_config.json`. | — |
| CB-10 | CLI `cbh` | REJECT | Subprocess ke `katana`, `gau`, dan `git`. Alat rekon. | — |
| CB-11 | MCP HackerOne (stdlib, read-only) | DEFER | Butuh `HACKERONE_API_USERNAME` dan `HACKERONE_API_TOKEN`. Relevansi rendah. | — |
| CB-12 | Lab `eval/` | DEFER | Materi pelatihan, bukan kemampuan produksi. | — |
| CB-13 | Kebijakan penggunaan terotorisasi (`SECURITY.md`) | MERGE | Pengguna sudah punya aturan serupa: uji hanya pada repository sendiri, sandbox, atau sistem yang diotorisasi. Tidak perlu skill terpisah. | K2 (syarat cakupan) |
| CB-14 | `mid-engagement-ir-detection`, `report-writing` | DEFER | Belum dinilai isinya pada audit ini. Perlu tinjauan terpisah jika dibutuhkan. | — |

Pemindaian risiko (`scan_skill_risk.py`, read-only, audit awal): HIGH 34 = 32 `pipe-remote-to-shell` (termasuk `curl -sk` ke API Kubernetes di `hunt-k8s`) + 1 `decode-and-exec` (dekode payload JWT di `hunt-k8s`) + 1 `dynamic-eval` (payload di `hunt-xss`). Ada 27 baris bukti `| python3` ikut terdeteksi; sifat false positive-nya belum ditinjau manual. MEDIUM 124 = 81 `credential-path-access` + 39 `unpinned-install` + 3 `os-system` + 1 `shell-profile-write`.

## H. Google Stitch Skills (commit `75f4696`)

Lisensi: **Apache-2.0** (LICENSE root dan manifest plugin). Belum diperiksa: apakah ada `NOTICE`. Jika ADAPT disetujui, periksa dulu dan sertakan bila ada.

Inventaris: 16 SKILL.md dalam 3 plugin (`stitch-design` 6, `stitch-utilities` 5, `stitch-build` 5). Total 142.430 B (≈36 ribu token jika semua dimuat). 3 `plugin.json`, 3 `.codex-plugin/plugin.json`, 1 marketplace. Tanpa hook. Tanpa konfigurasi MCP di dalam manifest.

Dependensi dan data:
- Stitch API: `https://stitch.googleapis.com`, header `X-Goog-Api-Key`. Kredensial wajib.
- `upload_to_stitch.py` mewajibkan `--api-key`. `upload-to-stitch/SKILL.md` (baris 32–45) mencari kunci di berkas konfigurasi MCP dan meminta pengguna jika tidak ditemukan.
- README menyarankan entri MCP di `opencode.json` project atau `~/.config/opencode/opencode.json`, dengan placeholder `YOUR_STITCH_MCP_URL`.
- Biaya dan kuota: tidak ada di repository (**UNVERIFIED**).
- Dependensi JS: `@swc/core` (react-components, react-native).

Keamanan dan izin:
- Pemindaian (audit awal): HIGH 0; MEDIUM 15 (`unpinned-install`, lokasi belum dirinci); LOW 138.
- `web_fetch` disebut di 13 dari 16 SKILL.md, termasuk `allowed-tools` pada `design-md`.
- Wildcard `stitch*:*` dipakai di banyak skill; `stitch-loop` menambah `chrome*:*`.
- `extract-static-html/scripts/snapshot.ts` memanggil `fetch` ke URL arbitrer (baris 466, 1032, 1330; audit awal).

Kompatibilitas: Flutter 0 dari 16 dan Playwright 0 sebutan (diverifikasi ulang pada SKILL.md). React 8, HTML 13, Vue 3, Svelte 2, Tailwind 7 (audit awal).

| ID | Kemampuan | Keputusan | Alasan dan syarat | Digabung ke |
|---|---|---|---|---|
| ST-01 | `taste-design` (12.566 B; `allowed-tools`: StitchMCP, Read, Write; prasyarat akses Stitch) | ADAPT | Inti: aturan teks untuk menulis DESIGN.md. Melarang neon ungu/biru, glow neon, dan gradien neon; membatasi aksen ke 1 dan saturasi di bawah 80%. Ini bertentangan dengan palet Silent Neon Tokyo dan EarthStop. Adaptasi: hapus StitchMCP dan prasyarat Stitch; tambahkan metadata batasan dan override kontekstual seperti `cinematic-camera`. | K1 |
| ST-02 | `design-md` (7.654 B; `allowed-tools`: `stitch*:*`, Read, Write, web_fetch; prasyarat MCP dan proyek Stitch) | ADAPT (skema saja) | Ambil skema DESIGN.md. Buang analisis proyek Stitch dan `web_fetch`. | K1 |
| ST-03 | `extract-design-md` (19.780 B; nama `stitch::extract-design-md`) | ADAPT (mode lokal) | Mode live URL memakai Puppeteer dan headless Chrome lokal. SKILL.md menyatakan tidak ada layanan pihak ketiga dan tidak perlu API key (baris 137–140). Perlu: ganti nama ke kebab-case; ubah output dari `.stitch/` ke folder proyek; periksa paket npm yang dipakai `extract-live-url.mjs`. Mode URL bergantung pada K5. | K1, K5 |
| ST-04 | `enhance-prompt` (6.640 B; Read, Write) | DEFER | Penulis prompt khusus alur generasi Stitch. Tanpa Stitch manfaatnya terbatas. Bila diperlukan, jadikan bagian K1 tanpa skill terpisah. | K1 (opsional) |
| ST-05 | `stitch-loop` (10.328 B) | REJECT | Loop estafet tanpa batas iterasi yang jelas. Izin `chrome*:*` dan `stitch*:*`. | — |
| ST-06 | `code-to-design` (3.649 B) | REJECT | Memerlukan Stitch API key (baris 75) dan alur ke cloud. Termasuk kelas ST-08. | — |
| ST-07 | Stitch MCP (remote, API key) | REJECT (tahap ini) | Keputusan pengguna 2026-11-25: Stitch Cloud dan Stitch MCP ditolak untuk tahap sekarang. Akun, biaya, dan kebijakan data belum terverifikasi. | K9 |
| ST-08 | `upload-to-stitch`, `manage-design-system`, `generate-design` | REJECT | Mengunggah berkas ke layanan Google. Kunci dibaca dari konfigurasi MCP. Melanggar prinsip data keluar. | — |
| ST-09 | `extract-static-html` (`snapshot.ts` memanggil `fetch` ke URL arbitrer) | DEFER | Hanya setelah K5 (allowlist URL). | K5 |
| ST-10 | `remotion` (stitch-build) | REJECT | Duplikat domain `remotion-motion-graphics` (VALIDATED). Bergantung pada Stitch. | — |
| ST-11 | `react-components`, `react-native`, `shadcn-ui` | REJECT | Tumpang tindih dengan `web-artifacts-builder`. Hanya React; Flutter 0 dari 16. | — |
| ST-11b | `react-vite-dashboard` | DEFER | Hanya jika ada kebutuhan dashboard web yang disetujui (mis. HMI ZII). | — |
| ST-12 | `site-md` | DEFER | Memakai `web_fetch`; butuh K5. Relevansi terhadap 14 profil rendah. | K5 |
| ST-13 | Manifest plugin dan marketplace | REJECT | Pengemasan, bukan kemampuan. Library tidak memasang plugin pihak ketiga. | — |

Perbandingan dengan 115 skill:
- **UI/UX Pro Max**: tidak ditemukan di registry (pencarian nama dan deskripsi nihil). Sumber sudah diberikan dan diverifikasi di bagian I.
- **Frontend**: `frontend-design` (IMPORTED) dan `web-artifacts-builder` tumpang tindih dengan `taste-design` dan builder React (ST-01, ST-11).
- **Playwright**: `webapp-testing` (VERIFIED) memakai Playwright lokal. Stitch tidak menyebut Playwright. Komplementer.
- **Remotion**: `remotion-motion-graphics` (VALIDATED) sudah ada. ST-10 ditolak sebagai duplikat.
- **Design system / DESIGN.md**: gap. Tidak ada SKILL.md di library yang menyebut DESIGN.md. Diisi oleh K1.
- **Visual quality gate UI**: gap. `quality-gate` hanya untuk video. Tiga repository ini tidak mengisinya (lihat K7).

## Register kandidat repository (konsolidasi)

Mencakup 26 repository dari daftar awal dan 6 repository v0.8 (Firecrawl 4, Stitch 1, BugHunter 1). Sumber: `references/sources-and-licenses.md`, `research/import-manifest.json`, PROGRESS.md, CHANGELOG.md, dan audit v0.8. Tidak ada audit ulang.

Ketidaksinkronan yang ditemukan: beberapa kolom "Keputusan library" di sources-and-licenses.md sudah usang. Contoh: anthropics/skills tertulis "tidak ada file disalin", padahal skill-nya sudah diimpor; spec-kit tertulis "belum diadopsi", padahal menjadi template ADAPTED. Beberapa baris "Belum diverifikasi" juga bertentangan dengan provenance: CoolProp, pymodbus, markitdown. Tindakan: K8.

| Kelompok | Repository | Lisensi (sumber) | Status aktual | Tindakan |
|---|---|---|---|---|
| R-A: sudah dipakai, register belum sinkron | anthropics/skills | Apache-2.0 per skill (e4bb5d9) | Sebagian skill IMPORTED (v0.2, digabung dengan obra/superpowers: 31) | K8 |
| | obra/superpowers | MIT (22f0b46) | IMPORTED | K8 |
| | github/spec-kit | MIT (3df7575) | Template ADAPTED `prd-engineering` | K8 |
| | e2nIEE/pandapower | BSD-3 (LICENSE repository) | Dipakai `load-flow-pandapower` | K8 |
| | ranaroussi/quantstats | Apache-2.0 | Dipakai `portfolio-metrics-quantstats` | K8 |
| | pymodbus-dev/pymodbus | BSD-3 (metadata PyPI 3.16.2) | Dipakai `modbus-tcp-client` | K8 |
| | CoolProp/CoolProp | MIT (metadata PyPI, PROGRESS) | Dipakai `steam-water-properties` | K8 |
| | microsoft/markitdown | MIT (metadata PyPI, PROGRESS) | Dipakai `markitdown-converter` | K8 |
| | microsoft/playwright | Belum diverifikasi | Dependensi uji; `webapp-testing` memakai Playwright lokal | K8 (verifikasi lisensi) |
| R-B: permisif, belum dipakai sebagai kode | open-spaced-repetition/fsrs4anki | MIT | Referensi algoritma | DEFER |
| | Power-Agent/PowerMCP | MIT (pencarian dan PyPI) | BLOCKED (butuh akses PowerWorld/PSSE yang sah) | DEFER |
| R-C: copyleft atau tidak jelas | thiagoralves/OpenPLC_v3 | GPL-3.0 | Referensi konsep saja | Jangan disalin |
| | kernc/backtesting.py | AGPL-3.0 | — | Jangan disalin |
| | polakowo/vectorbt | Apache-2.0 + Commons Clause | Hindari sebagai dependensi produk | Jangan disalin |
| | yomidevs/yomitan | Belum diverifikasi (umumnya GPL-3) | Referensi UX saja | Jangan disalin |
| | remotion-dev/skills | Tanpa LICENSE | — | Jangan disalin |
| | Power-Agent/PowerSkills | Konflik (README MIT; PR menyatakan tanpa LICENSE) | — | Jangan disalin |
| R-D: belum diverifikasi, belum ada kebutuhan | langchain-ai/langgraph, appium/appium, node-red/node-red, motion-canvas/motion-canvas, mrdoob/three.js, ManimCommunity/manim, docling-project/docling | Belum diverifikasi | Belum diprioritaskan | DEFER (verifikasi saat ada kebutuhan) |
| | hexgrad/kokoro | Belum diverifikasi | Model besar; batas hardware | DEFER (perlu persetujuan unduhan) |
| | obra/superpowers-skills | MIT; diarsipkan | Tidak dipakai | Tutup |
| R-E: kandidat v0.8 | google-labs-code/stitch-skills | Apache-2.0 | Bagian H | K1, K5; Stitch Cloud dan MCP: REJECT (tahap ini) |
| | elementalsouls/Claude-BugHunter | MIT + CC BY 4.0 | Bagian G | K2, K3, K6 |
| | firecrawl/firecrawl, firecrawl-claude-plugin, firecrawl-mcp-server, skills | AGPL-3.0; MIT; MIT; ISC | Bagian F | K4; sisanya DEFER/REJECT |
| | nextlevelbuilder/ui-ux-pro-max-skill | MIT (LICENSE; plugin.json; skill.json; cli/package.json) | Bagian I (diverifikasi, read-only) | MERGE ke K1 sebagai sumber data (bila disetujui); REJECT MCP, installer, CLI, generator berbayar |

## Matriks relevansi 14 profil

Skala: **H** (berdampak tinggi), **M** (relevan), **L** (rendah). Tanda "bersyarat" berarti bergantung pada fakta yang belum dikonfirmasi.

| Profil | Firecrawl (F) | Claude-BugHunter (G) | Google Stitch (H) |
|---|---|---|---|
| EarthStop | L | L | M: palet neon bertentangan dengan ST-01; router perlu override |
| Silent Neon Tokyo — Manhwa | L | L | L–M: konflik neon hanya jika taste-design muncul |
| Silent Neon Tokyo — Game | L | L | L–M: sama; UI game belum diketahui |
| SISI GELAP TOKOH | L–M: riset sumber; verifikasi tetap manusia (M11) | L | L |
| AmiraVerse (Flutter, Jepang) | L | M–H: H bila ada backend akun (bersyarat) | M: token DESIGN.md ke ThemeData; output Stitch bukan Flutter |
| ZII Industrial Intelligence | L | M: OT/SCADA tidak tercakup; API dan HMI web | L–M: hanya ST-11b (DEFER) |
| DEAMIRA | L | M: checklist authz dan API | M: spesifikasi UI |
| ClipACanvas | L | M: link render memuat HTML terkodekan; review input | L |
| Money App | L | H: data keuangan (asumsi dari kategori finance) | M: konsistensi UI |
| Produksi film sinematik | L | L | L: Remotion duplikat |
| Penulisan novel | L | L | L |
| XAUUSD ICT/SMC | L–M: data pasar hanya bila lisensinya jelas (M1) | M: kunci API dan secret (K3) | L |
| Teknik Elektro & Industrial Utility | L–M: sumber standar; PUIL harus terverifikasi (M2) | L | L |
| JLPT N5–N1 | L | L | L |

Ringkasan: Firecrawl tidak punya profil H. Claude-BugHunter punya H (Money App) dan M–H (AmiraVerse, bersyarat). Stitch tidak punya H; konflik neon bernilai M.

## Backlog prioritas (versi awal; digantikan oleh bagian J, 2026-11-25)

| ID | Prio | Item (digabung dari) | Prasyarat | Rp0 | Langkah bila disetujui |
|---|---|---|---|---|---|
| K2 | P1 | Review keamanan defensif: authz, autentikasi, API (CB-02, CB-03, CB-13) | Diff terhadap `supabase` dan `supabase-postgres-best-practices`; RLS dikecualikan | Ya | Checklist statis dengan langkah mitigasi, tanpa payload; uji struktur |
| K1 | P1 | Pipeline DESIGN.md dalam satu skill: taste-design + skema design-md + extract-design-md mode sumber kode (ST-01, ST-02, ST-03 lokal) | Override palet neon di `skill-constraints.json`; nama kebab-case; hapus StitchMCP | Ya | ADAPTATION.md dengan sha256 upstream; uji router untuk kueri desain pada profil neon dan EarthStop |
| K8 | P1 | Sinkronisasi dokumen: README.md (masih v0.2.0), header PROGRESS.md (v0.2.0), kolom "Keputusan library" dan baris "Belum diverifikasi" di sources-and-licenses.md | Perubahan repository perlu otorisasi (frozen) | Ya | Angka diambil dari validator dan test; satu sumber kebenaran (import-manifest.json + sources-and-licenses.md), dokumen lain hanya merujuk |
| K9 | P1 | Keputusan pengguna. Status 2026-11-25: URL UI/UX Pro Max diberikan dan diverifikasi (bagian I); Stitch Cloud dan MCP REJECT untuk tahap ini; kebijakan data keluar DENY BY DEFAULT. Sisa: keputusan ADOPT/ADAPT UI/UX Pro Max setelah master audit | — | — | Persetujuan per item |
| K3 | P2 | Pemeriksaan artefak build (CB-04) sebagai perluasan `secret-leak-scan` | — | Ya | Pola source map, `.git`, dan `.env` di artefak; uji dengan fixture lokal |
| K4 | P2 | Markdown lokal dengan guard kehilangan konten (FC-06, FC-07) sebagai perluasan `markitdown-converter` | Fixture HTML milik proyek | Ya | Deteksi kehilangan (bandingkan teks sumber dan keluaran); fallback untuk halaman JavaScript |
| K5 | P2 (prasyarat) | Guard akses URL (W1): allowlist domain, tolak IP privat dan loopback, tanpa kredensial, batas ukuran dan waktu | — | Ya | Dipakai K1 (mode URL), ST-09, dan ST-12 bila disetujui |
| K6 | P3 | Pemindaian CVE dependensi (CB-05) | Sumber data (OSV/NVD) dengan lisensi jelas dan akses jaringan | Ya | Verifikasi lisensi sumber data terlebih dahulu |
| K7 | P3 (gap) | Visual UI quality gate | Tidak ada di tiga repository ini; perlu URL sumber atau dibangun sebagai CUSTOM | Ya | Susun rubrik dulu, lalu cari sumber |

## Keputusan per kandidat

| Kandidat | ADOPT | ADAPT | MERGE | REJECT | DEFER |
|---|---|---|---|---|---|
| Firecrawl | — | FC-07 (→K4) | FC-06 (→K4) | FC-03, FC-04, FC-05 | FC-01, FC-02 |
| Claude-BugHunter | — | CB-02, CB-03 (→K2); CB-04 (→K3) | CB-13 (→K2) | CB-01, CB-06, CB-07, CB-08, CB-09, CB-10 | CB-05 (→K6), CB-11, CB-12, CB-14 |
| Google Stitch | — | ST-01, ST-02 (→K1); ST-03 (→K1, K5) | — | ST-05, ST-06, ST-07, ST-08, ST-10, ST-11, ST-13 | ST-04, ST-09 (→K5), ST-11b, ST-12 (→K5) |
| UI/UX Pro Max (bagian I) | — | — | sumber data untuk K1 (bila K1 disetujui) | MCP stack, installer `npx`, CLI, generator berbayar | brand, banner-design, slides, design-system |

Tidak ada ADOPT langsung: setiap kandidat punya bagian yang harus ditulis ulang atau tidak dapat dipakai.

## Catatan

- Tidak ada instalasi, eksekusi kode pihak ketiga, atau perubahan kode. Checkpoint riset: commit yang disetujui (bagian I). Frozen code baseline tetap `7039fed`.
- Tidak ada audit ulang pada tahap ini. Verifikasi terbatas hanya untuk klaim yang disebut di atas.
- Dokumen yang tidak diubah: PROGRESS.md, CHANGELOG.md, README.md, sources-and-licenses.md. Ketidaksinkronannya dicatat di K8.

---

# I. Checkpoint riset 2026-11-25: kebijakan, verifikasi UI/UX Pro Max, dan standby

## I.1 Checkpoint

- Commit ini adalah **research checkpoint**, bukan implementation baseline.
- Frozen code baseline: `7039fed` (tidak berubah).
- Frozen snapshot sebelumnya: `940368f`.
- Perubahan dalam commit: hanya `ZY-Skill-Library/research/BACKLOG-V0.8.md`.
- K1–K9 tetap backlog. Tidak ada implementasi, termasuk K1, K2, dan K8. Prioritas dievaluasi ulang setelah audit repository berikutnya.
- Setelah checkpoint: STANDBY.

## I.2 Keputusan dan kebijakan (berlaku mulai checkpoint ini)

- **Stitch Cloud dan Stitch MCP: REJECT** untuk tahap sekarang.
- **Kebijakan data keluar: DENY BY DEFAULT.** Dilarang mengirim source code privat, kredensial, data pengguna, dokumen internal, atau informasi proyek ke layanan pihak ketiga tanpa persetujuan eksplisit. Pengambilan informasi publik secara read-only diperbolehkan selama tidak mengirim data sensitif.
- **Anggaran tambahan: Rp0.**
- **Audit berikutnya**: 51 kandidat repository untuk comprehensive intelligence audit. Status: menunggu master audit protocol; belum dimulai.

## I.3 Verifikasi sumber UI/UX Pro Max (read-only; tidak ada yang dipasang)

Sumber: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill. Clone shallow (`--depth 1`, `GIT_LFS_SKIP_SMUDGE=1`) di luar repository. HEAD `bde080f` (2026-11-26 00:34 +0530; author commit "kontributor publik (nama tidak dicantumkan)"; subject "fix(ui-styling): find installed shadcn components under src/ and custom aliases (#602)"). 750 berkas; 25 MB tanpa `.git`. Tidak ada filter LFS di `.gitattributes`.

**Identitas**
- Repository publik milik `nextlevelbuilder`. `plugin.json` dan `skill.json` menunjuk ke repository yang sama.
- Versi tidak konsisten: `plugin.json` dan `skill.json` = 2.15.0; `cli/package.json` = 2.5.0; versi terbaru paket npm `ui-ux-pro-max-cli` = 2.15.0. Paket yang terpublikasi tidak dapat dicocokkan dengan folder `cli/` pada snapshot ini.
- Metadata npm tidak memuat `repository.url`, sehingga tautan sumber paket tidak dapat dicocokkan otomatis.
- Identitas di luar repository (uupm.cc, nextlevelbuilder.io, pemilik hukum) tidak diverifikasi.

**Lisensi**
- MIT (`LICENSE`, Copyright 2024 Next Level Builder). Konsisten di `plugin.json`, `skill.json`, dan `cli/package.json`.
- Font: 54 berkas TTF (5,3 MB). Ada 27 berkas lisensi `*-OFL.txt` di `canvas-fonts/`. Pemetaan setiap TTF ke lisensinya belum diverifikasi.
- Belum diverifikasi: lisensi `data/phosphor-icons-upstream.json` dan `data-provenance.json`.

**Isi dan ukuran**
- 7 skill unik di `.claude/skills/`: ui-ux-pro-max (utama), ui-styling, design-system, design, brand, banner-design, slides.
- Skill utama: 80 gaya (51 aktif), 194 palet, 74 pasangan font, 141 panduan UX, 105 ikon, 17 preset GSAP, 25 jenis chart, 22 stack.
- Duplikasi: 6 salinan di `cli/assets/skills/`; `search.py` dan `core.py` ada di tiga lokasi (`src/`, `cli/assets/`, `.claude/skills/`).
- Data: 144 CSV, 115 JSON, 138 berkas Python (termasuk tes), 54 TTF.
- Perkiraan token (4 karakter per token): SKILL.md utama 18.640 B (≈4,7 ribu token); referensi skill utama 38.278 B (≈9,6 ribu token); SKILL.md dari 7 skill unik 64.610 B (≈16 ribu token). Pemuatan selektif tetap diperlukan.

**Keamanan dan eksekusi** (ditemukan dengan pembacaan dan pencarian pola; tidak dijalankan)
- Tidak ditemukan konfigurasi hook (dicari: PreToolUse, PostToolUse, SessionStart, SessionEnd, Stop, "hooks"). `cli/package.json` tidak memiliki lifecycle `preinstall` atau `postinstall`.
- HIGH: MCP dengan `npx -y <paket>@latest` tanpa versi terkunci di `stack/.mcp.json`: `@playwright/mcp`, `chrome-devtools-mcp`, `shadcn`.
- HIGH: installer `npx ui-ux-pro-max-cli init --ai ...` tanpa versi terkunci (`skill.json`).
- HIGH: generator dengan API berbayar dan kredensial yang mengirim prompt ke pihak ketiga: `design/scripts/cip/generate.py` dan `icon/generate.py` memakai `GEMINI_API_KEY`; `logo/generate.py` juga memakai `ATLASCLOUD_API_KEY`, `MUAPI_API_KEY`, dan `UBERLLM_API_KEY`. Melanggar kebijakan data keluar dan Rp0.
- MEDIUM: mode global CLI menulis ke folder home (`cli/src/utils/template.ts`, baris 337); `uninstall.ts` juga beroperasi di home (baris 99).
- MEDIUM: CLI membaca token GitHub dari `UI_PRO_MAX_GITHUB_TOKEN` atau `GITHUB_TOKEN` (`cli/src/utils/github.ts`, baris 50).
- MEDIUM: `design-system/scripts/slide-token-validator.py` menjalankan subproses (`subprocess.run`, baris 30).
- LOW: HTML hasil generator memuat Google Fonts saat dibuka (`design-system/scripts/generate-slide.py`, baris 49–50).

**Kompatibilitas**
- `search.py` dan `core.py` hanya mengimpor standard library dan modul lokal di folder yang sama (`design_system`, `core`). Tidak ada dependensi pihak ketiga pada dua berkas ini.
- `requirements.txt` hanya berisi pytest untuk pengujian. Python 3.x (fallback `python3` atau `py -3`). Belum diuji pada Windows.
- 22 stack, termasuk Flutter (`data/stacks/flutter.csv`), React Native, SwiftUI, Jetpack Compose, html-tailwind, dan Three.js.
- Format `.claude/skills/<nama>/SKILL.md` kompatibel dengan Claude Code. Struktur library ZY (`skills/<kategori>/<nama>/`) memerlukan pemetaan.

**Tumpang tindih dengan registry** (pencarian nama, belum dibandingkan isi)
- `brand-guidelines`, `canvas-design`, `theme-factory`, dan `frontend-design` memiliki fungsi serupa dengan `brand`, `banner-design`, `design-system`, dan `ui-styling`. Tidak ada nama yang sama persis.
- `slides` berhubungan fungsional dengan `pptx` (IMPORTED).
- `design-system` menghasilkan `MASTER.md`, setara dengan DESIGN.md pada K1 dan ST-01.

**Relevansi 14 profil**
- H: AmiraVerse (stack Flutter tersedia untuk panduan UI).
- M: EarthStop (gaya dan gerak; konflik palet perlu dicek), Money App, DEAMIRA, ZII (chart dan dashboard).
- L–M: Silent Neon Tokyo (Manhwa dan Game), ClipACanvas, XAUUSD, Teknik Elektro & Industrial Utility, JLPT.
- L: SISI GELAP TOKOH, Produksi film sinematik, Penulisan novel.

**Keputusan awal** (belum ada implementasi; menunggu master audit dan persetujuan)
- **MERGE ke K1** sebagai sumber data (gaya, palet, pasangan font, panduan UX, stack Flutter), hanya jika K1 disetujui. Bukan skill terpisah. Syarat: satu salinan; tanpa MCP; tanpa installer `npx`; tanpa CLI; tanpa generator berbayar; tanpa tautan font eksternal di keluaran.
- **REJECT**: `stack/.mcp.json`, installer di `skill.json`, `cli/`, dan generator `design/` (logo, icon, cip).
- **DEFER**: `brand`, `banner-design`, `slides`, dan `design-system` sampai dibandingkan isinya dengan `brand-guidelines`, `canvas-design`, `theme-factory`, dan `pptx`.

## I.4 Belum dilakukan

- Master audit protocol: belum diterima. Tidak ada implementasi.
- Verifikasi lisensi per font (54 TTF) dan data `phosphor-icons-upstream.json`.
- Verifikasi sumber paket npm: `cli/package.json` (2.5.0) berbeda dengan registry (2.15.0).
- Pengujian perilaku skill: tidak dijalankan.

---

# J. Pembaruan backlog setelah audit intelligence v0.8 (2026-11-25)

Sumber: `ZY-Skill-Library/research/v0.8-intelligence/` (delapan dokumen dan `evidence/triage-summary.tsv`). Tidak ada implementasi, instalasi, atau perubahan kode. Setiap item menunggu persetujuan per ID.

## J.1 Koreksi checkpoint (bagian I)

- Klaim "generator UI/UX Pro Max berbayar" tidak terverifikasi. Yang terverifikasi: generator memakai API key (`GEMINI_API_KEY`, `ATLASCLOUD_API_KEY`, `MUAPI_API_KEY`, `UBERLLM_API_KEY`) dan mengirim prompt ke layanan pihak ketiga. Biaya aktual belum diverifikasi.
- Penolakan generator tetap berlaku berdasarkan kebijakan data keluar DENY BY DEFAULT, terlepas dari harganya.
- "Rp0" di bagian I hanya berlaku untuk pemasangan lokal. Biaya generator tidak diketahui.
- Koreksi ini dimasukkan ke commit riset berikutnya yang disetujui. Commit checkpoint sebelumnya tidak diubah.

## J.2 Prioritas baru (usulan; menunggu persetujuan)

| Prioritas | Item | Alasan |
|---|---|---|
| P1 | K2 (P09), K1 (P02, mode A), K7 (P01), K8 (P17) | Keamanan defensif untuk Money App dan AmiraVerse; sumber desain; gerbang kualitas visual; sinkronisasi dokumen |
| P2 | K3 (P10), K4 (P11), K10 (P12), K11 (P13) | Perluasan skill VERIFIED yang sudah ada; standar memori dan persetujuan |
| P3 | K5 (prasyarat), K6 (CVE, menunggu sumber data), K12 (P14), K13 (P03–P07), K14 (P08, P15) | Prasyarat mode URL; panduan adaptasi; metodologi paper-only |
| DEFER / DOMAIN / BLOCKED | D1–D7 dan item 39 | Lihat `SELECTIVE-INTEGRATION-PROPOSAL.md` dan `MASTER-REPOSITORY-REGISTER.md` bagian 5 |

## J.3 Revisi K1–K9

| ID | Status baru | Perubahan berdasarkan bukti | Paket |
|---|---|---|---|
| K1 | P1 (diperkecil) | Mode A saja, dari sumber kode. Tanpa Node, Puppeteer, Stitch, atau StitchMCP. Data UI/UX Pro Max (bde080f) menjadi sumber opsional dengan persetujuan terpisah. Batasan palet neon tetap | P02 |
| K2 | P1 (RLS dikecualikan) | Cakupan: authz, autentikasi, API. RLS sudah dibahas oleh skill Supabase. Konten CC BY 4.0 dari Claude-BugHunter wajib diberi atribusi. Tanpa payload | P09 |
| K3 | P2 | Perluasan `secret-leak-scan` untuk artefak build: source map, `.git` yang terbuka, `.env` di dalam artefak | P10 |
| K4 | P2 | Perluasan `markitdown-converter` dengan deteksi kehilangan konten untuk halaman yang dirender JavaScript | P11 |
| K5 | P3 (prasyarat) | Wajib sebelum mode URL pada K1 atau kandidat ST-09 dan ST-12. Allowlist domain; tolak IP privat dan loopback; tanpa kredensial | — |
| K6 | P3, DEFER | Belum ada sumber data CVE dengan lisensi jelas | — |
| K7 | P1, sebagian terisi | Gerbang kualitas desain sudah diusulkan (critique dan audit dari Impeccable, gerbang Floor dan Reflex dari Hallmark). Visual QA berbasis render tetap gap | P01 |
| K8 | P1 | Sinkronisasi dokumen. Angka diambil dari validator dan tes, bukan dari ingatan | P17 |
| K9 | Sebagian terjawab | Terjawab: URL UI/UX Pro Max diverifikasi; Stitch Cloud dan MCP REJECT untuk tahap ini; kebijakan data keluar DENY BY DEFAULT. Masih terbuka: enam baris GAP, brief Sebelum Sepi Menjadi Rumah, repo Blender Skills (item 39), keputusan memori lokal, dan persetujuan Ollama | — |

## J.4 Item baru

| ID | Prioritas | Item | Catatan | Paket |
|---|---|---|---|---|
| K10 | P2 | Standar memori proyek lokal (C04) | Tanpa cloud, tanpa hook; batas ukuran per entri; retrieval kata kunci. Gap terbesar di registry | P12 |
| K11 | P2 | Prosedur gerbang persetujuan (C02) | Titik STOP, log keputusan | P13 |
| K12 | P3 | Validasi walk-forward dan out-of-sample (C23) | Riset dan paper saja. Tanpa tuning pada data out-of-sample | P14 |
| K13 | P3 | Panduan adaptasi: web-platform subset (P03), GSAP (P05), diagram (P04), recipe cards (P06), Three.js (P07) | Satu per satu, dengan atribusi dan pin commit | P03–P07 |
| K14 | P3 | Metodologi trading paper-only (P08) dan pengetahuan browser debugging (P15) | Tanpa broker dan tanpa MCP | P08, P15 |

## J.5 Ditolak dan ditunda (tidak masuk backlog)

Lihat `MASTER-REPOSITORY-REGISTER.md` bagian 5: REJECT 20 item, DEFER 7, DOMAIN ONLY 4, KNOWLEDGE ONLY 8, BLOCKED 1 (item 39). Tidak ada item yang di-ADOPT langsung.

## J.6 Status

- Tidak ada implementasi. Tidak ada perubahan kode. Tidak ada instalasi. Tidak ada PR, merge, atau force push.
- Repositori kandidat: 51 ditinjau. 41 dibaca mendalam, 2 dengan pemeriksaan terarah (04, 32), 8 hanya triage (25, 29, 31, 34, 38, 41, 50, 51).
- Repositori unik setelah deduplikasi: 106 (56 historis dan 52 baru, dikurangi 2 tumpang tindih).
- Benchmark: 52 diusulkan, 0 dijalankan. Pengukuran token: NOT MEASURABLE di runtime ini.
- Checkpoint riset berikutnya: menunggu persetujuan diff.

---

# K. Penutupan supervisor (2026-11-26)

Checkpoint ini memuat BACKLOG-V0.8.md dan `research/v0.8-intelligence/` (delapan dokumen dan `evidence/`). Pekerjaan lanjutan (audit mendalam, desain memori, profil domain, dan paket persetujuan implementasi) tidak termasuk checkpoint ini dan belum di-commit.

- **Frozen baseline:** code `7039fed` tidak berubah. Frozen snapshot `940368f` adalah ancestor dari HEAD. Checkpoint ini tidak mengubah kode, skill, skrip, registry, atau tes. Sejak `7039fed` hanya `tests/requirements-test.txt` (+9 baris) yang berubah, dari commit `940368f`, dan itu sudah ada sebelum checkpoint ini.
- **P01–P17: NOT AUTHORIZED.** Tidak ada implementasi, instalasi, atau perubahan berkas library. Lihat `SELECTIVE-INTEGRATION-PROPOSAL.md`.
- **Memori proyek lokal: PRIORITY CANDIDATE.** Desain saja; implementasi menunggu persetujuan. Tidak bergantung pada Claude-Mem, layanan cloud, atau MCP jarak jauh.
- **Item 39 (Blender Skills): BLOCKED.** Dua repository dengan nama sama: 39a (EL4CTEO) dan 39b (arjun988). Kanonik belum dipilih.
- **Ollama: DEFER.** Tidak dipasang dan tidak diunduh. Model besar memerlukan persetujuan.
- **Empat domain GAP: BACKLOG ONLY.** Iklan komersial, explainer edukasi, game Android dan browser, dan lingkungan 3D realistis. Matriks memuat enam baris GAP (`PROJECT-DOMAIN-MATRIX.md` bagian 1). Dua baris lain (Sebelum Sepi Menjadi Rumah dan WTP/WWTP) belum mendapat keputusan supervisor dan menunggu keputusan pemilik.
- **EarthStop Golden Master: AWAITING COMPLETION.** Kriteria belum didefinisikan (V7). Item M15, M17, dan I3 bergantung padanya.
- **Rekonsiliasi angka:** total historis 56; repository audit 52; tumpang tindih 2; entri unik 106; tidak diklaim terkonfirmasi 3 (fsrs, serta item 39a dan 39b); repository unik terkonfirmasi 103. Angka 32 adalah subset register konsolidasi (26 + 6, baris 191 bagian ini) dan dikesampingkan sebagai jumlah historis. Rincian di `MASTER-REPOSITORY-REGISTER.md` bagian 3a.
- **Pemisahan runtime dan pengetahuan:** `MASTER-REPOSITORY-REGISTER.md` bagian 7.
- **Bukti tersimpan:** `evidence/triage-summary.tsv` (25 kolom; `readme_head` dihapus), `evidence/identity-ls-remote.tsv` (52 identitas dan satu alias), dan `evidence/METHOD.md`. Hash penuh dan indikator cukup untuk verifikasi ulang. Klon di `/home/user/ext/research-cache/` dapat dibuat ulang dari URL dan hash; penghapusannya diusulkan setelah audit lanjutan selesai.
- **Koreksi:** "four GAP" menjadi "six" di `PROJECT-DOMAIN-MATRIX.md`, `INTELLIGENCE-ARCHITECTURE-V0.8.md` bagian 6, dan `SELECTIVE-INTEGRATION-PROPOSAL.md` bagian 5. "39b (REJECT)" di matriks domain menjadi "39 (BLOCKED)" sesuai register.
- **Nama:** nama kontributor non-pemilik pada I.3 diganti dengan "kontributor publik". Nama pembuat dan pemegang hak cipta repository publik dipertahankan karena diperlukan untuk verifikasi identitas dan lisensi.
- **Biaya: Rp0.** Tidak ada layanan berbayar, API berbayar, atau unduhan model.
