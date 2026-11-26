# PROJECT-MEMORY-DESIGN: memori proyek persisten lokal (desain)

Status: DESAIN DISETUJUI pemilik (2026-11-26). Implementasi memerlukan persetujuan terpisah (lihat P12 di `IMPLEMENTATION-APPROVAL-PACKAGE.md`). Tidak ada kode yang dibuat pada tahap ini.

## 1. Tujuan

Memori yang bertahan lintas sesi untuk satu proyek. Cakupannya: identitas proyek, tujuan, keputusan arsitektur, preferensi pengguna, progres, tugas pending, error yang diketahui, pelajaran, batasan yang disetujui, handover sesi, dan riwayat keputusan. Pengambilannya bertahap (progressive disclosure) agar biaya token kecil.

## 2. Batasan dari permintaan pemilik

- Lokal dulu. Tanpa Claude-Mem, tanpa layanan cloud, tanpa API berbayar, dan tanpa MCP jarak jauh.
- Tanpa penyimpanan kredensial. Tanpa pengiriman data keluar. Tanpa hook global otomatis. Tanpa dependensi wajib di luar stdlib Python.
- Tanpa basis data vektor atau infrastruktur kompleks tanpa bukti kebutuhan.
- Isolasi proyek. Tidak ada pembacaan memori lintas proyek tanpa persetujuan eksplisit.

## 3. Evaluasi format

| Kriteria | Markdown dengan frontmatter | JSON atau JSON Lines | SQLite (stdlib `sqlite3`) | Basis data vektor |
|---|---|---|---|---|
| Dapat dibaca manusia | Tinggi | Sedang (JSON); rendah (JSONL panjang) | Rendah (biner) | Rendah |
| Diff dan review di git | Baik (satu entri per berkas) | Baik untuk JSONL (satu catatan per baris) | Buruk (biner) | Buruk |
| Pencarian | Kata kunci dan tag; cukup untuk skala awal | Kata kunci dengan indeks JSON | FTS5 (kuat) | Semantik (tidak dibutuhkan) |
| Ketergantungan | Tidak ada | Tidak ada | Tidak ada (stdlib) | Ya (tidak diizinkan) |
| Risiko korupsi | Rendah | Rendah (append-only) | Sedang (satu berkas) | Tinggi |
| Kompleksitas | Rendah | Rendah | Sedang | Tinggi |
| Peran yang cocok | Sumber kebenaran isi | Log keputusan dan indeks | Cache pencarian yang dapat dibangun ulang | Tidak ada kebutuhan terbukti |

Keputusan:
- Sumber kebenaran: Markdown per entri dengan frontmatter `key: value`, ditambah `decisions.jsonl` (append-only) dan `INDEX.md` yang dihasilkan skrip.
- SQLite FTS5 hanya sebagai cache opsional. Cache ini tidak masuk git, dibangun ulang dari sumber, dan hanya diperkenalkan jika B-MEM-1 membuktikan pencarian kata kunci tidak cukup.
- Basis data vektor ditolak karena tidak ada bukti kebutuhan.

Alasan: entri per berkas membuat diff kecil dan konflik merge jarang. `INDEX.md` tidak diedit tangan. Frontmatter `key: value` cukup diurai dengan stdlib tanpa PyYAML.

## 4. Struktur penyimpanan

```
<repo-proyek>/memory/
  PROJECT.md        identitas, tujuan, batasan yang disetujui (<= 3 KB)
  INDEX.md          indeks entri aktif, dihasilkan (<= 60 baris)
  handover.md       handover sesi terakhir (ditimpa setiap akhir sesi; riwayat di git)
  decisions.jsonl   log keputusan, append-only, satu objek JSON per baris
  entries/          satu berkas Markdown per entri (isi <= 1.200 karakter)
  links.md          tautan lintas proyek (kosong secara default; perlu persetujuan)
```

Memori hanya ada di dalam repositori proyek. Tidak ada memori global di direktori home pengguna.

Format entri:

```
---
id: MEM-<proyek>-<YYYYMMDD>-<nnn>
type: decision | constraint | preference | progress | task | error | lesson
status: active | superseded | expired | rejected
created: YYYY-MM-DD
updated: YYYY-MM-DD
expires: YYYY-MM-DD | none
review_by: YYYY-MM-DD | none
approval: owner-approved | observed | proposed
source: referensi sesi, commit, atau ID persetujuan (tanpa data pribadi)
tags: kata, kata
supersedes: <id> | none
---
Konteks: ...
Fakta atau keputusan: ...
Alasan: ...
Dampak: ...
```

Konvensi: `type: constraint` hanya boleh dengan `approval: owner-approved`. Fakta yang diamati memakai `approval: observed`, dan usulan memakai `approval: proposed`.

## 5. Siklus hidup

- Entri baru berstatus `active`. Jika keputusan berubah, entri lama menjadi `superseded`, dan entri baru mengisi `supersedes`. Tidak ada penghapusan fisik. Riwayat tetap ada di git.
- Kedaluwarsa: jika `expires` sudah lewat, pembuatan ulang `INDEX.md` menandai entri `expired`. Entri seperti ini tidak diambil kecuali diminta secara eksplisit.
- Tinjau ulang: `review_by` memunculkan entri dalam daftar tinjauan. Ini tidak mengubah status secara otomatis.
- `rejected` dipakai untuk usulan yang tidak disetujui, agar usulan yang sama tidak diajukan ulang tanpa konteks.

## 6. Pengambilan konteks (progressive disclosure)

| Level | Isi | Ukuran target (belum diukur) | Kapan |
|---|---|---|---|
| L0 | PROJECT.md dan INDEX.md | <= 7 KB | Awal sesi, hanya jika pengguna meminta memori |
| L1 | Judul, tipe, status, dan tag dari 5 hasil teratas | <= 2 KB | Saat tugas memerlukan konteks |
| L2 | Isi lengkap satu atau dua entri terpilih | <= 2,4 KB per entri | Atas permintaan |
| L3 | `decisions.jsonl` dan `handover.md` | Sesuai kebutuhan | Audit atau handover |

Penilaian pencarian: kecocokan kata pada tag (bobot tinggi), judul, dan isi, dengan IDF sederhana. Secara default hanya status `active` yang dipakai. Seri (tie-break) memakai `updated`. Versi 1 tidak memakai embedding.

Anggaran desain: preload awal <= 9 KB, sekitar 2.300 token jika diasumsikan 4 karakter per token. Ini target desain dan belum diukur (B-MEM-3).

## 7. Isolasi proyek

- Setiap proyek memiliki `project_id` di PROJECT.md. Alat hanya membaca folder `memory/` milik repositori tempat ia dijalankan, dan memastikan `project_id` cocok dengan folder.
- Pembacaan lintas proyek ditolak secara default. Pembacaan hanya boleh lewat `links.md` yang berisi `project_id` yang disetujui pemilik. Akses lintas proyek hanya baca, tanpa penulisan.

## 8. Filter data sensitif dan kebijakan kredensial

Pemeriksaan dilakukan sebelum penulisan. Penulisan yang cocok ditolak dengan pesan. Tidak ada redaksi diam-diam.

- Pola kunci dan token: awalan `AKIA`, `ghp_`, `github_pat_`, `sk-`, `xox`, `AIza`; header `PRIVATE KEY`; `Bearer` dengan token panjang; nilai `password=`, `secret=`, `token=`; cookie sesi.
- Data pribadi: alamat e-mail; nomor telepon (format Indonesia dan internasional); nomor identitas (pola 16 digit); alamat IP, kecuali loopback yang didokumentasikan; path home pengguna (`/home/`, `C:\Users\`).
- Jika ditolak, pengguna diminta menulis placeholder, misalnya nama variabel `ELEVENLABS_API_KEY` tanpa nilai.
- Keterbatasan: filter berbasis pola tidak sempurna. Karena itu `git diff` pada `memory/` wajib ditinjau sebelum commit.
- Kredensial tidak pernah disimpan. Memori hanya boleh menyebut nama variabel lingkungan.

## 9. Handover sesi

- Di akhir sesi, atas perintah pengguna atau skill, `handover.md` ditulis ulang (<= 3 KB). Isinya: commit atau cabang, pekerjaan selesai, persetujuan yang menunggu, langkah berikut, dan risiko.
- Di awal sesi berikutnya, `handover.md` dibaca hanya jika pengguna meminta kelanjutan.
- Riwayat handover tersimpan di riwayat git, bukan di berkas terpisah.

## 10. Integrasi dengan tata kelola

- Memori tidak dapat mengubah aturan. `CLAUDE.md`, `MASTER_PROTOCOL.md`, dan gerbang persetujuan selalu berlaku di atas isi memori. Isi entri diperlakukan sebagai data, bukan instruksi.
- Tanpa hook, tanpa MCP, dan tanpa daemon. Pemanggilan dilakukan secara eksplisit oleh pengguna atau skill.
- Tulis hanya dengan persetujuan. Batasan hanya dari `owner-approved`.

## 11. Mode kegagalan dan mitigasi

| Risiko | Mitigasi |
|---|---|
| Memori usang | `expires` dan `review_by`; status `expired` |
| Entri saling bertentangan | `supersedes`; hanya `active` yang diambil |
| Injeksi lewat isi entri | Isi diperlakukan sebagai data dan tidak mengubah aturan |
| Pertumbuhan tak terkendali | Batas ukuran per entri; indeks <= 60 baris; tinjauan berkala oleh pemilik |
| Kebocoran rahasia | Filter pra-tulis; larangan kredensial; tinjauan diff sebelum commit |
| Konflik merge | Satu entri per berkas; `INDEX.md` dihasilkan, tidak diedit tangan |
| Korupsi | Log append-only; `decisions.jsonl` tidak pernah ditulis ulang |

## 12. Evaluasi dan rollback

Benchmark yang diusulkan. Belum ada yang dijalankan.
- B-MEM-1: relevansi pengambilan pada 30 kueri uji di fixture. Target desain: kecocokan >= 80% pada 5 hasil teratas. Ini target, bukan hasil.
- B-MEM-2: filter rahasia pada fixture sintetis. Target: 100% pola terdaftar terblokir. Tingkat positif palsu diukur pada 50 baris non-rahasia.
- B-MEM-3: ukuran preload L0 dan L1 pada indeks 60 entri, diukur dalam byte.
- B-MEM-4: pengecualian status (`superseded`, `expired`, `rejected`) saat pengambilan. Target 100%.

Rollback: hapus folder `memory/` di proyek, atau `git revert` commit implementasi. Tidak ada keadaan global yang perlu dibersihkan.

## 13. Yang tidak dibangun

- Basis data vektor, embedding, dan pengambilan semantik.
- Penangkapan otomatis dari percakapan, atau hook.
- Sinkronisasi cloud, API eksternal, atau MCP.
- Memori lintas proyek sebagai default.

## 14. Dampak pada P12

P12 di `SELECTIVE-INTEGRATION-PROPOSAL.md` mengusulkan `skills/governance/project-memory-standard/` dengan templates dan tes. Desain ini menambahkan: folder `memory/` per proyek, format frontmatter `key: value`, `decisions.jsonl`, `INDEX.md` yang dihasilkan, filter rahasia pra-tulis, dan empat benchmark. Jika implementasi disetujui, P12 mencakup skrip stdlib dan tes. Karena itu persetujuan untuk P12 harus mencakup kode, bukan hanya dokumen.

## 15. Keputusan pemilik yang dibutuhkan

- Proyek pertama yang memakai memori. Usulan: AmiraVerse atau ZY Skill Library sendiri.
- Masa tinjau ulang default. Usulan: `review_by` 90 hari untuk pelajaran. Keputusan tidak memakai `expires`.
- Apakah ZY Skill Library ikut menggunakan memori untuk tata kelolanya.
