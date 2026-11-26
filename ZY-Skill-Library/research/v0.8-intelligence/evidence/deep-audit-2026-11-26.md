# Deep audit 2026-11-26: pembacaan mendalam dan pertanyaan terbuka

Status: pembacaan statis dan hanya-baca pada klon dangkal di luar repositori. Tidak ada kode upstream yang dieksekusi, tidak ada instalasi, dan tidak ada data yang dikirim ke layanan mana pun. Kandidat yang sudah memiliki bukti memadai tidak diulang.

Ketertelusuran: setiap temuan memuat hash commit (12 karakter; hash penuh ada di `identity-ls-remote.tsv`), path relatif di dalam repositori, dan nomor baris. Klon dapat dibuat ulang dari URL pada `identity-ls-remote.tsv` lalu diperiksa pada commit yang sama. Pola pencarian ada di bagian 5.

## 1. Kandidat yang naik dari triage ke pembacaan mendalam

Delapan kandidat yang sebelumnya hanya triage sekarang dibaca mendalam. Cakupan register menjadi 49 dibaca mendalam, 2 pemeriksaan terarah (04, 32), dan 0 hanya triage.

| ID | Kandidat @ commit | Lisensi | Temuan (path:baris) | Status | Pengaruh keputusan |
|---|---|---|---|---|---|
| 25 | Shadcn Admin @a156d9b90519 | MIT | `package.json` tidak memiliki skrip preinstall, postinstall, prepare, atau install. Tidak ada konfigurasi hook. Dependensi: 43 `dependencies`, 27 `devDependencies`. Host yang disebut: w3.org (37, namespace SVG), randomuser.me (10; konteks pemakaian belum ditelusuri), github.com (7). `axios` dipakai untuk penanganan error (`src/lib/handle-server-error.ts`). | VERIFIED | Tidak berubah: DOMAIN ONLY |
| 29 | OpenMontage @2e003e65fa99 | AGPL-3.0 | LICENSE: AGPL-3.0. 141 SKILL.md: 92 di `.agents/skills`, 49 di `.claude/skills`. Host yang paling sering disebut: api.heygen.com (450 referensi), files.heygen.ai (70), cdn.jsdelivr.net (66). Ada `remotion-composer/`, yaitu komposer kedua berbasis Remotion. Tidak ada package.json di root. | VERIFIED | Tidak berubah: REJECT. Ketergantungan API HeyGen berbayar dan copyleft AGPL. Pengetahuan hanya BATAS (konsep saja). |
| 31 | FFmpeg Skill @31b47c263348 (impor dari 73436cb) | MIT | Salinan impor `skills/creative-production/ffmpeg-skill/SKILL.md` (227 baris) identik dengan `skills/ffmpeg-skill/SKILL.md` di upstream saat ini (0 baris berbeda). Upstream memiliki 19 SKILL.md: 1 di `skills/ffmpeg-skill`, 1 di root (berbeda isinya, tidak diimpor), dan 17 di `.claude/skills` (skill pengembangan internal repositori, bukan skill FFmpeg). | VERIFIED | P16 ditutup: tidak perlu impor ulang. Angka "19 SKILL.md" pada register tidak mewakili skill FFmpeg. |
| 34 | VoiceStudio @d9061408c204 | AGPL-3.0 | LICENSE: AGPL-3.0. Telemetri opt-in: `backend/core/analytics.py:9–10` (instalasi default tidak mengirim apa pun) dan `:138–143` (default `False`). Jepang di kode: `backend/services/tts_backend.py:2795` (`"japanese": "ja"`), `:4787` (Kokoro `"j"`), `backend/services/qwen_cuda.py:26`. Indonesia: hanya `backend/services/text_normalization.py:108` (`"indonesian": "id"`) untuk normalisasi angka; tidak ada daftar bahasa engine TTS yang memuat Indonesia. Installer: `deploy/install-worker/worker.mjs:10–13` memuat `curl … \| sh` pada halaman instalasi. | VERIFIED (telemetri, Jepang); NOT EVIDENCED (Indonesia) | Tetap REJECT (AGPL dan installer). Jepang terbukti di tingkat kode. Indonesia tidak terbukti. |
| 38 | MCP for Blender @a5a8acf2c6ae | MIT | `src/blender_mcp/bundled/addon.py:2445–2455`: `execute_code` menjalankan `exec(code, namespace)`. README:412: "By default, the AI can run any Python code in Blender". `BLENDER_MCP_SAFE_MODE=1` bersifat opt-in (`src/blender_mcp/safe_mode.py:72–76`). Bind socket default `localhost` (`addon.py:130–136`), tetapi dapat diatur ke alamat IPv4. `install.ps1:43`: `uvx … mcp-for-blender@latest setup` (tanpa versi terkunci). Telemetri: `telemetry.py:325` (`upload_screenshot`) dipanggil dari `trajectory.py:748` dan `telemetry_decorator.py:330`. Default `enabled` belum ditentukan: `telemetry.py:85` hanya menonaktifkan bila variabel lingkungan diset, dan definisi konfigurasinya tidak ditemukan dalam pembacaan ini. | VERIFIED (dasar REJECT); UNRESOLVED (default telemetri) | Tetap REJECT. Dasar penolakan sekarang berupa bukti kode, bukan triage. |
| 41 | ComfyUI @a2103ae69d98 | GPL-3.0 | LICENSE: GPL-3.0. README:22 mengklaim "as low as 4GB vram + 8GB ram". Ini klaim vendor dan belum diukur. | PARTIAL (klaim tercatat, belum diuji) | Tetap DEFER: GPL (konsep saja) dan hardware belum diuji pada GTX 1650. |
| 50 | MuMuAINovel @9a9f275993e1 | GPL-3.0 | LICENSE: GPL-3.0. `mcp_config.json` ada di root, berarti konfigurasi MCP (runtime tetap REJECT). Pola literal kredensial (`api_key`, `secret`, `token` dengan nilai minimal 16 karakter) tidak ditemukan. | VERIFIED (sebagian) | Tetap KNOWLEDGE ONLY (BATAS). |
| 51 | Hacking-Tools @eac2233fc86b | MIT | 13 berkas: README, LICENSE, `.github/FUNDING.yml`, dan gambar pendukung. Tidak ada skrip atau biner. README: "A curated list of penetration testing and ethical hacking tools". | VERIFIED | Tetap REJECT: katalog ofensif; tidak ada nilai defensif yang dibutuhkan. |

## 2. Pertanyaan terbuka yang diselesaikan atau dipertahankan

| Item | Pertanyaan | Temuan (path:baris, commit) | Status |
|---|---|---|---|
| 02 Graphify | Identitas paket | `pyproject.toml:6`: `name = "graphifyy"`. Dokumentasi memakai `graphifyy` (`graphify/skill-opencode.md:78, 93–98`). Nama repositori: `graphify`. Konsisten di dalam repositori. Kepemilikan paket di PyPI tidak diverifikasi karena tidak ada akses ke registry dari sesi ini. | Dalam repositori: VERIFIED. PyPI: UNVERIFIED |
| 02 Graphify | Dukungan Dart dan Flutter | Ekstraktor khusus `graphify/extractors/dart.py` (`extract_dart`). Terdaftar di `graphify/extract.py:4902, 11487` dan `graphify/extractors/__init__.py:18, 48`. | VERIFIED (ada di kode) |
| 02 Graphify | Jaringan pada jalur lokal | Modul yang memanggil jaringan: `graphify/llm.py` (panggilan LLM; pemeriksaan host dengan `socket.getaddrinfo`, baris 3533) dan `graphify/ingest.py` (impor `urllib`, baris 8–9). Apakah jalur lokal default memanggilnya belum ditelusuri. | UNVERIFIED |
| 05 Open Code Review | Data egress | Endpoint ditentukan pengguna: `extensions/frontend/src/shared/providers.generated.ts:14` (api.anthropic.com), `:67` (api.openai.com/v1), `:213` (`http://localhost:4000/v1`), `:291` (ollama.com/v1, cloud). `extensions/idea/README.md:35`: `ocr config set llm.url`. Endpoint default tidak diverifikasi. | Egress hanya ke endpoint yang dikonfigurasi. Default UNVERIFIED |
| 05 Open Code Review | Dukungan Dart | Tidak ditemukan parser atau aturan bahasa Dart. Hasil grep hanya berupa kecocokan substring pada teks non-bahasa. | NOT EVIDENCED |
| 05 Open Code Review | Telemetri default | `internal/telemetry/config_test.go:14–27`: uji menyatakan `Enabled=false` sebagai default, exporter `console`, dan `OTLPEndpoint` kosong. | VERIFIED (berdasarkan uji default) |
| 30 HyperFrames | Telemetri default | `skills/media-use/references/meta.md:46`: "Opt out with DO_NOT_TRACK=1 or HYPERFRAMES_NO_TELEMETRY=1 (also off in CI...)". Artinya aktif secara default di luar CI (model opt-out). Jalur implementasi PostHog belum ditelusuri. | VERIFIED oleh dokumentasi repositori; jalur kode UNVERIFIED |
| 33 Voicebox | Bahasa Jepang | `app/src/lib/constants/languages.ts:24` (`ja: 'Japanese'`); `backend/backends/__init__.py:34` (`"ja": "japanese"`); `backend/backends/kokoro_backend.py:14` (Jepang memerlukan misaki[ja]); `backend/backends/qwen_custom_voice_backend.py:45` (suara Jepang); README:97 ("23 languages … Japanese"). | VERIFIED (bukti kode). Kualitas pengucapan belum diuji |
| 33 Voicebox | Bahasa Indonesia | Tidak ditemukan kode `id` atau "Indonesian" pada daftar bahasa aplikasi (`languages.ts`) maupun pemetaan backend (`backends/__init__.py`). | NOT EVIDENCED |
| 28 App Store Compliance | Lisensi kanonik OpenRoots | `LICENSE:4–5` dan `NOTICE:6–7` menunjuk `https://openroots.org/licenses/ora/2.3/legalcode.txt`. Pengambilan teks gagal: DNS `openroots.org` tidak dapat di-resolve dari sesi (kebijakan jaringan lingkungan). | UNVERIFIED (BLOCKED sampai teks kanonik dibaca) |
| 45 Claude Trading Skills | Jalur integrasi broker | Pencarian pola `POST`, `submit_order`, `place_order`, dan `/v2/orders` pada `skills/**/*.py`: 0 berkas. `order_builder.py` dan `plan_breakout_trades.py` (breakout-trade-planner) tidak memuat panggilan jaringan menurut pola yang sama. 299 berkas menyebut alpaca atau broker (dokumen dan konfigurasi). Referensi setup MCP Alpaca: `skills/portfolio-manager/references/alpaca-mcp-setup.md`. | VERIFIED untuk cakupan pola (tidak ada pengiriman order). Bukan tinjauan kode penuh |
| 39 Blender Skills | Identitas kandidat | Kedua repositori teridentifikasi sebagai repositori berbeda (39a EL4CTEO, 39b arjun988). Kanonik belum dipilih pemilik. Lihat `BLENDER-SKILLS-COMPARISON.md`. | BLOCKED (keputusan pemilik) |

## 3. Dampak pada keputusan

- Tidak ada kelas register yang berubah. Semua kandidat yang diperiksa tetap pada kelas sebelumnya, tetapi dasar keputusannya sekarang berupa bukti kode untuk 38, 34, 29, 51, dan 25.
- P16 (31) ditutup: salinan impor sudah sama dengan upstream untuk berkas yang dipakai. Tidak ada impor ulang.
- 02 (Graphify): dukungan Dart terbukti. Penolakan DEFER tetap karena jalur lokal dan kepemilikan paket belum terbukti.
- 05 (OCR): egress hanya ke endpoint yang dikonfigurasi dan telemetri default OFF. DEFER tetap, tetapi jalur "endpoint lokal saja" menjadi pertanyaan untuk keputusan Ollama.
- 30 (HyperFrames): telemetri aktif secara default. Ini tetap melanggar DENY BY DEFAULT, sehingga D3 tetap.
- 33 (Voicebox): Jepang terbukti di kode. Indonesia tidak terbukti. Benchmark bahasa tetap diperlukan.
- 34 (VoiceStudio): telemetri default OFF, tetapi AGPL dan installer tetap menolak runtime.
- 38 (MCP Blender): kode mengeksekusi Python tanpa batas secara default. Alasan penolakan sekarang terbukti.
- 45 (Claude Trading): tidak ditemukan jalur pengiriman order dengan pola yang diperiksa. Pengecualian broker dan MCP tetap berlaku.

## 4. Cakupan dan batas

- Tidak ada akses ke PyPI, registry, atau openroots.org dari sesi ini. Klaim yang bergantung pada layanan itu ditandai UNVERIFIED.
- Default telemetri MCP Blender belum ditentukan. Tidak mengubah keputusan karena REJECT sudah didasari eksekusi kode dan installer `@latest`.
- Deteksi berbasis pola tidak membuktikan ketiadaan. Hasil "0 berkas" hanya berarti pola tidak ditemukan pada ruang lingkup pencarian yang tertulis.
- Pemeriksaan kepemilikan dan lisensi hukum tidak dilakukan.

## 5. Pola pencarian (teks, tidak dapat dieksekusi)

| Kandidat | Pola yang dicari (ringkas) | Ruang lingkup |
|---|---|---|
| 38 | `exec(`, `execute_code`, `bind`, `localhost`, `@latest`, `upload_screenshot`, `BLENDER_MCP_SAFE_MODE` | `src/`, `install.*`, `README.md` |
| 34 | `japanese`, `indonesian`, `analytics_enabled`, `user_opted_in`, pipe ke `sh` | `backend/`, `deploy/` |
| 05 | `base_url`, `baseUrl`, `api.openai.com`, `api.anthropic.com`, `localhost`, `ollama`; `Enabled` pada uji telemetri | `extensions/`, `internal/telemetry/`, `README` |
| 30 | `HYPERFRAMES_NO_TELEMETRY`, `DO_NOT_TRACK` | seluruh pohon kecuali `node_modules` |
| 33 | `ja`, `japanese`, `indonesi`, `bahasa`; kode `id` pada daftar bahasa | `app/`, `backend/`, `README` |
| 45 | `place_order`, `submit_order`, `create_order`, `/v2/orders`, `\.post\(` | `skills/**/*.py` |
| 02 | `graphifyy`, `dart`, `urllib`, `socket`, `requests` | seluruh pohon kecuali `.git` |
| 31 | perbandingan berkas SKILL.md impor dengan upstream pada commit saat ini | `skills/ffmpeg-skill/SKILL.md` |
| 39 | `SKILL.md`, berkas `.mcp.json` dan `.cursor/mcp.json`, `run_in_blender.py`, `subprocess`, `exec(compile` | kedua repositori |

## 6. Ketergantungan pada klon sementara

- Setiap temuan di atas dapat diverifikasi ulang dari hash commit di `identity-ls-remote.tsv` dan path relatif di tabel. Tidak ada klaim yang bergantung hanya pada direktori klon.
- Perintah terminal ad hoc tidak disimpan. Polanya ada di bagian 5 agar dapat diulang.
- Skrip triage dan pembacaan mendalam disalin ke `evidence/tools/` (`triage.sh`, `deep.sh`). Hash SHA-256-nya tercatat di `METHOD.md` bagian 5. Library tidak menjalankannya.
- Tidak ada berkas dari klon yang disalin ke repositori. Hanya kutipan pendek (satu baris atau kurang) dan path yang disimpan.
