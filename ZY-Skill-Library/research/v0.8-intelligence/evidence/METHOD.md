# METHOD — bukti audit ZY v0.8

Status: dokumentasi metode. Tidak berisi perintah yang dapat dijalankan. Tidak ada kode upstream yang dieksekusi.
Tanggal: 2026-11-26. Berkas terkait: `triage-summary.tsv`, `identity-ls-remote.tsv`, dan bagian 2, 3a, serta 7 pada `MASTER-REPOSITORY-REGISTER.md`.

## 1. Batas metode

- Analisis statis: membaca berkas, menghitung pola teks, dan membaca lisensi serta README. Tidak ada instalasi, build, eksekusi skrip repository, atau pemanggilan API repository.
- Hitungan indikator adalah sinyal untuk ditinjau, bukan vonis. Nilai nol tidak membuktikan ketiadaan.
- Klon dangkal (satu commit terakhir) dibuat di luar repository dengan prompt git dinonaktifkan, LFS tidak diunduh, dan batas waktu 900 detik per klon.

## 2. Verifikasi identitas

| Pemeriksaan | Hasil |
|---|---|
| HEAD penuh dari `git ls-remote` dibandingkan dengan `rev-parse HEAD` pada klon | 52 dari 52 cocok |
| Owner/repo dari URL klon dibandingkan dengan nama direktori | 52 dari 52 cocok |
| HEAD yang sama di antara 52 repository | 0 |
| Owner/repo yang sama di antara 52 repository | 0 |
| Tumpang tindih dengan 56 identitas historis | 2: obra/superpowers (04), kajisho5/ffmpeg-skill (31) |
| Alias LPengYang/MotionClone | HEAD sama dengan Bujiazi/MotionClone (item 32); dihitung sekali |
| Nama paket berbeda dari nama repository | Item 02 (paket `graphifyy`); dicatat sebagai identitas paket, bukan repository |
| Kandidat dengan kanonik belum dipilih | Item 39 (39a EL4CTEO, 39b arjun988); tidak diklaim terkonfirmasi |

Hash penuh untuk setiap repository ada di `identity-ls-remote.tsv`.

## 3. Indikator statis (`triage-summary.tsv`, 25 kolom)

Ruang lingkup kode: berkas dengan ekstensi py, js, mjs, cjs, ts, tsx, jsx, dart, go, rs, java, kt, swift, sh, ps1, rb, php, dan cs. Folder `.git` dan `node_modules` dikecualikan.

| Kolom | Yang dihitung | Catatan pembacaan |
|---|---|---|
| id, repo, commit | ID kandidat, nama direktori klon, 12 karakter pertama HEAD | — |
| license, license_files | Jenis lisensi dari 6.000 karakter pertama berkas LICENSE, COPYING, atau NOTICE; NONE jika tidak ada | Pencocokan frasa, bukan analisis hukum |
| files, size_mb | Jumlah berkas yang dilacak git; ukuran pohon kerja tanpa `.git` | — |
| skill_md | Jumlah berkas bernama SKILL.md | — |
| hook_files | hooks.json, berkas di folder hooks/, dan .claude/settings*.json | — |
| plugin_manifests | Hingga enam path manifest plugin atau marketplace | Daftar terpotong |
| agent_files | AGENTS.md, CLAUDE.md, GEMINI.md, dan .cursorrules di root | — |
| mcp_configs | .mcp.json, mcp.json, mcp_config*.json (hingga enam path) | Daftar terpotong |
| installers | Berkas install*, setup*, bootstrap* dengan ekstensi sh, ps1, py, js, mjs, ts (hingga enam path) | Daftar terpotong |
| lifecycle_pkgs | package.json dengan kunci preinstall atau postinstall | Hanya kunci; isi skrip dibaca di pembacaan mendalam |
| latest_ref_files | Berkas yang memuat teks `@latest` | Termasuk dokumentasi |
| pipe_sh_files | Berkas yang memuat pola unduhan dipipe ke shell (curl atau wget ke sh, bash, zsh; atau iwr ke iex) | Termasuk contoh di dokumentasi |
| net_lines | Baris kode dengan pemanggilan HTTP umum (requests, urllib, httpx, aiohttp, fetch(, axios, http.request, dan lain-lain) | `fetch(` juga mencakup kode browser |
| subprocess_lines | Baris kode dengan pemanggilan proses (subprocess, os.system, child_process, execSync, spawnSync, spawn(, dan lain-lain) | — |
| eval_lines | Baris kode dengan eval(, new Function(, pickle.load, yaml.load(, exec(compile | — |
| credential_files | Berkas dengan kata kunci kredensial (API_KEY, ACCESS_TOKEN, SECRET_KEY, PASSWORD, cookies, dan lain-lain) | Tidak membedakan contoh dan nilai nyata |
| telemetry_files | Berkas dengan kata telemetry, analytics, sentry, posthog, mixpanel, amplitude, gtag(, dan lain-lain | Tidak membuktikan telemetri aktif; status default harus dibaca dari kode |
| model_files | Berkas dengan huggingface, .safetensors, .gguf, snapshot_download, from_pretrained, ollama pull | — |
| files_gt5mb | Jumlah berkas di atas 5 MB | — |
| lfs_filters | Jumlah baris filter=lfs di .gitattributes | — |
| lockfiles | Lockfile di root | — |
| (dihapus) readme_head | Kutipan 140 karakter README | Dihapus pada revisi ini; lihat bagian 5 |

## 4. Pembacaan mendalam

Enam bagian per repository: (1) tiga baris pertama LICENSE atau COPYING; (2) sepuluh baris README non-HTML pertama; (3) sepuluh host eksternal teratas yang disebut dalam kode beserta hitungannya; (4) enam baris pertama yang memuat pola pipe-to-shell; (5) kunci preinstall, postinstall, prepare, dan install dari package.json di root; (6) empat belas baris pertama dari berkas hooks dan MCP (maksimum tiga berkas).

Batas penafsiran:
- Hitungan regex cenderung melebihkan, karena dokumentasi ikut terhitung.
- Tidak ada parsing AST; pemanggilan yang dibangun secara dinamis tidak tertangkap.
- Berkas LFS tidak dibaca isinya.
- Nilai nol hanya berarti pola tidak ditemukan dalam ruang lingkup tersebut.

## 5. Keterlacakan dan pembuatan ulang

- Setiap bukti terkait satu repository, satu hash commit penuh (`identity-ls-remote.tsv`), dan satu path relatif di dalam repository.
- Klon dapat dibuat ulang dari URL di `identity-ls-remote.tsv` lalu diperiksa pada hash yang sama. Isi pohon git ditentukan oleh hash commit.
- Skrip yang dipakai disalin ke `evidence/tools/` untuk audit ulang. Library tidak menjalankan skrip ini. SHA-256:
  - `triage.sh`: 5b41ec0dd9f877d3af72bd108ce96909cf361c981ca4ff71c9824ad5a9a713f2
  - `deep.sh`: bce573c56b30f1e4f0d0f358de63e764bd1de4b381b89d87263cb01b3ba4b673
- Perubahan kolom: `readme_head` (kutipan README 140 karakter) dihapus. Kolom itu berisi teks pihak ketiga dan tidak dipakai untuk keputusan. Jumlah kolom turun dari 26 menjadi 25; jumlah baris tetap 52.

## 6. Catatan klon

- Dari 52 berkas log klon, hanya `heygen-com__hyperframes.err` yang tidak kosong (2.440 byte): git-lfs melaporkan 35 berkas fixture di folder tests yang seharusnya berupa pointer tetapi bukan. Berkas tersebut ikut dihitung apa adanya dan tidak ditinjau satu per satu.
- Semua 52 folder klon ada dan bernama sesuai pola owner__repo.
