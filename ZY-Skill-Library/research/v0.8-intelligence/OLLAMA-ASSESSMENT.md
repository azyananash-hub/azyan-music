# OLLAMA-ASSESSMENT: evaluasi tanpa instalasi dan tanpa unduhan model

Status: DEFER. Tidak ada instalasi, tidak ada unduhan model, dan tidak ada persetujuan yang diberikan.

## 1. Status instalasi

- Container sesi ini: `ollama` tidak ditemukan. Container ini juga tidak memiliki GPU NVIDIA yang terlihat. Ini bukan mesin pemilik.
- Mesin pemilik: TIDAK DAPAT DIVERIFIKASI dari sesi ini. Daftar folder mesin yang tersedia kosong, sehingga tidak ada mesin pemilik yang terhubung.
- Untuk memeriksa, pemilik dapat menjalankan sendiri dua perintah berikut dan mengirim hasilnya. Sesi ini tidak menjalankannya: `ollama --version` dan `ollama list`.

## 2. Hardware target (dari pemilik)

- GPU: GTX 1650 dengan VRAM 4 GB.
- RAM: 16 GB.
- CPU: Intel Core i5-10300H (4 core, 8 thread).

## 3. Perkiraan ukuran model

Ini estimasi, bukan pengukuran. Bobot kuantisasi Q4 umum memakai sekitar 4,5–5 bit per parameter, atau sekitar 0,6 byte per parameter. Ukuran berkas kira-kira sama dengan jumlah parameter (miliar) dikali 0,6 GB. KV cache dan overhead runtime menambah beban yang bergantung pada panjang konteks.

| Kelas model | Perkiraan berkas Q4 | Muat penuh di VRAM 4 GB? | Catatan |
|---|---|---|---|
| ~1B | ~0,6 GB | Ya | Terbatas untuk tugas bahasa |
| ~3B | ~1,8 GB | Ya, dengan konteks sedang | Titik awal yang paling realistis |
| ~7–8B | ~4,2–5 GB | Tidak sepenuhnya; sebagian di RAM | Lebih lambat. RAM 16 GB cukup |
| ~14B | ~8,5 GB | Tidak | Di luar target praktis |

Angka ini belum diverifikasi terhadap model tertentu. Lisensi setiap model harus diperiksa sebelum unduhan.

## 4. Penyimpanan

- Setiap model menempati sekitar ukuran pada tabel di atas. Ruang disk mesin pemilik tidak diketahui.
- Ukuran instalasi Ollama sendiri dan lokasi penyimpanan default belum diverifikasi.

## 5. Performa inferensi

Tidak diukur. Tidak ada angka token per detik yang diklaim.

Hipotesis yang akan diuji (B-LOC-1):
- Model sekitar 3B yang muat penuh di GPU: kemungkinan interaktif.
- Model 7–8B dengan offload sebagian: kemungkinan lebih lambat. Besarnya belum diketahui.
- CPU saja: diperkirakan lambat untuk model 7B ke atas pada 4 core dan 8 thread.

Pengukuran yang diperlukan di mesin pemilik: token per detik, waktu token pertama, dan puncak VRAM serta RAM.

## 6. Kasus penggunaan praktis

1. Ringkasan lokal untuk entri memori proyek (P12). Keuntungan: tidak ada data yang keluar. Syarat: kualitas hasilnya diuji.
2. Normalisasi glosarium dan draf naskah. Syarat: kualitas bahasa Indonesia dan Jepang diuji. Tidak menggantikan TTS.
3. Bantuan klasifikasi untuk router saat pencocokan kata kunci gagal. Ini kandidat fallback, bukan pengganti.

Tidak cocok untuk narasi audio. Ollama adalah LLM teks, bukan TTS.

## 7. Keamanan dan kebijakan

- Ollama menjalankan server HTTP lokal. Bind hanya ke localhost, dan itu harus diverifikasi pada konfigurasi yang dipasang.
- Register item 13 mencatat bahwa README memuat pipe-to-shell untuk macOS dan `cmd/launch/*` menjalankan skrip instalasi pihak ketiga. Pemasangan hanya dari binary resmi yang diverifikasi checksum-nya. Pipe-to-shell ditolak.
- Model dari pihak ketiga memiliki lisensi masing-masing. Belum ada model yang lisensinya diperiksa.
- Ollama adalah runtime, bukan skill. Jika diadopsi, ia menjadi dependensi domain di luar library, bukan kode library.

## 8. Keputusan dan prasyarat

Status tetap DEFER. Prasyarat sebelum instalasi, semuanya harus terpenuhi:
1. Pemilik mengonfirmasi status instalasi di mesin pemilik.
2. Daftar model kandidat dengan lisensi yang sudah diverifikasi.
3. Rencana benchmark B-LOC-1 disetujui.
4. Binding localhost dan penolakan pipe-to-shell tertulis.
5. Persetujuan eksplisit untuk unduhan model, dengan ukuran sesuai tabel bagian 3.

Tidak ada unduhan model tanpa persetujuan.
