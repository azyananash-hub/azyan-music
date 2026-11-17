# Azyan Music: Proposal UI dari Referensi Screenshot

Status: **draft untuk review**. Belum ada kode UI yang diubah.

Referensi: dua screenshot dashboard musik gelap (navy/indigo, aksen merah dan ungu) yang dikirim user.
Ini dipakai sebagai **pola layout**, bukan disalin. Gambar, gradasi artwork, dan nama artis di screenshot tidak dipakai.

---

## 1. Pola yang diambil dari referensi

| Pola | Screenshot | Diterapkan di app | Catatan |
|---|---|---|---|
| Mini player bar di bawah (art + judul + play/pause + progress tipis) | 1 & 2 | `MiniPlayer.kt` (sudah ada) | Perlu dicek: progress tipis dan tombol 48dp |
| Chip filter horizontal (genre/mood) | 2 | Baru: `LazyRow` di atas daftar lagu | Berguna setelah tag genre dari MediaStore |
| Kartu hero (lagu/album teratas) | 1 & 2 | Baru: kartu "Lanjutkan" di home | Memakai `LibraryStore` (last session sudah disimpan) |
| Grid kartu album "Popular" | 1 & 2 | `LazyVerticalGrid` adaptif | Artwork fallback: gradasi dari hash judul, bukan gambar pihak lain |
| Panel kanan daftar berurutan | 2 | Tablet/lipat (window class Expanded, lebar ≥ 840dp) | Di HP tidak ditampilkan |
| Sidebar navigasi | 1 & 2 | `NavigationRail` di tablet, `NavigationBar` di HP | Jangan pakai sidebar di HP |

Yang **tidak** diambil: sidebar penuh di HP, banner artis dengan foto tokoh nyata, dan kombinasi tiga aksen warna sekaligus.

---

## 2. Masalah di kode saat ini yang perlu diperbaiki dulu

Dibaca dari `ui/theme/Color.kt`, `Theme.kt`, dan `NowPlayingSheet.kt`:

1. **Dynamic color menimpa palet sendiri.** Di Android 12+ (`dynamicColor = true` default), `AccentBlue` dan `DarkColors` tidak dipakai. Warna UI mengikuti wallpaper. Ini membuat identitas visual tidak konsisten antar perangkat.
   - Usulan: tambah pengaturan "Warna tema: Wallpaper / Azyan" dan default ke **Azyan** agar tampilan sama di semua perangkat.
2. **Now Playing terlalu sederhana untuk Fase 4-5.** Belum ada tempat untuk cover art, lirik, equalizer, atau sleep timer. Sebaiknya disiapkan slot di layout sejak sekarang.
3. **Slider tanpa `contentDescription`.** TalkBack tidak punya label untuk progress. Tambahkan `semantics { contentDescription = ... }` dan teks waktu yang dibacakan.
4. **Kontras teks (dihitung dari nilai hex di kode, rumus WCAG):**
   - `onSurfaceVariant` `#C0C7CD` di atas `background` `#101418`: **10.83:1** (lolos AA dan AAA).
   - `onSurfaceVariant` `#C0C7CD` di atas `surfaceVariant` `#40484D`: **5.46:1** (lolos AA untuk teks normal, tapi tidak AAA).
   - `onBackground` `#E1E3E5` di atas `surfaceVariant` `#40484D`: **7.25:1**.
   - `primary` `#7FD1FF` di atas `#101418`: **10.98:1**. `onPrimary` `#00344A` di atas `primary`: **7.84:1**.

---

## 3. Usulan layout per ukuran layar

| Ukuran | Navigasi | Konten | Now Playing |
|---|---|---|---|
| Compact (HP, < 600dp) | `NavigationBar` bawah | 1 kolom, chip + daftar | Bottom sheet (sudah ada), artwork 72% lebar |
| Medium (lipat/tablet kecil, 600-840dp) | `NavigationRail` kiri | 2 kolom grid | Panel kanan, bukan sheet |
| Expanded (tablet, ≥ 840dp) | `NavigationRail` kiri | Konten tengah + panel kanan "Antrean" | Panel kanan selalu terlihat |

Infinix Note 40 Pro adalah perangkat target utama, jadi **Compact** harus paling matang lebih dulu.

---

## 4. Artwork fallback (tanpa gambar pihak lain)

Lagu tanpa cover art (kasus umum di file lokal) memakai gradasi yang dibuat dari hash judul+artis:
- Dua warna dari hue hash, saturasi dan kecerahan dibatasi agar tetap elegan di tema gelap.
- Ikon nada di tengah dengan alpha 0.85.
- Deterministik: lagu yang sama selalu mendapat gradasi yang sama.

Ini murni kode Compose (`Brush.linearGradient`), tanpa aset dan tanpa lisensi tambahan.

---

## 5. Urutan implementasi yang disarankan

1. Tema: tambah pilihan warna Azyan vs wallpaper, dan default ke Azyan. *(kecil, dampak besar)*
2. Semantics dan kontras: label TalkBack pada slider dan kontrol. *(wajib untuk aksesibilitas)*
3. Artwork fallback gradasi di `SongArtwork.kt`. *(dipakai di mana-mana, jadi kerjakan sebelum layout baru)*
4. Chip genre + kartu "Lanjutkan" di home. *(butuh data, bisa pakai `LibraryStore`)*
5. Layout Expanded dengan `NavigationRail` dan panel antrean. *(setelah Compact stabil)*

Setiap langkah bisa diuji di emulator atau perangkat. Build tetap lewat GitHub Actions (APK debug), jadi tidak ada cara verifikasi visual di container ini.

---

## 6. Keterbatasan

- **Tidak ada screenshot yang dijalankan.** Desain ini belum saya render di perangkat atau emulator. Semua klaim tentang tampilan adalah perkiraan dari kode dan screenshot.
- **Kontras angka** di atas dihitung dari nilai hex di kode, bukan dari pengukuran di layar.
- Saya belum memeriksa `MusicHomeScreen.kt` (692 baris) secara menyeluruh. Rancangan layout di atas perlu dicocokkan dengan struktur itu sebelum implementasi.
