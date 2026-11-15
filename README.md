# Azyan Music

Pemutar musik lokal (native Android, Kotlin + Jetpack Compose + Media3/ExoPlayer) yang dibuat
untuk Infinix Note 40 Pro (XOS / Android 14) yang tidak punya pemutar musik bawaan.

- **Package:** `com.azyan.music` (build debug memakai `com.azyan.music.debug`)
- **minSdk:** 26 (Android 8) · **targetSdk:** 35
- **Build:** GitHub Actions (tanpa perlu Android Studio di PC)

---

## Status: Fase 0 — Fondasi & validasi pipeline

Yang sudah ada:

- [x] Struktur proyek Gradle (Kotlin 2.0.21, AGP 8.7.3, Compose BOM 2024.10.01)
- [x] Tema Material 3 + dynamic color (Material You)
- [x] Ikon adaptif & splash-style theme
- [x] Manifest lengkap dengan permission audio/notifikasi/foreground service (dipakai Fase 1-2)
- [x] Workflow CI yang menghasilkan APK debug

Roadmap berikutnya:

- [ ] **Fase 1** — Scan MediaStore, daftar lagu, folder, playback dasar
- [ ] **Fase 2** — `MediaSessionService`, background playback, kontrol notifikasi & lock screen
- [ ] **Fase 3** — Playlist, favorit, pencarian
- [ ] **Fase 4** — Equalizer, bass boost, sleep timer
- [ ] **Fase 5** — Cover art, lirik (.lrc), widget
- [ ] **Fase 6** — Polish, signing release

---

## Cara build APK (lewat GitHub Actions)

1. Buat repo **kosong** di GitHub (jangan centang "Add a README"), misalnya `azyan-music`.
2. Di folder proyek ini, jalankan:

   ```bash
   git remote add origin https://github.com/<USERNAME>/azyan-music.git
   git push -u origin main
   ```

3. Buka tab **Actions** di repo → workflow **Build APK** akan berjalan otomatis.
4. Setelah selesai (±3-5 menit), buka run terakhir → bagian **Artifacts** →
   download `azyan-music-debug`.
5. Ekstrak zip, isinya `app-debug.apk`.

Build manual tanpa push: tab **Actions** → **Build APK** → **Run workflow**.

---

## Cara install di HP

1. Kirim `app-debug.apk` ke HP (USB, Google Drive, WhatsApp "pesan ke diri sendiri", dll).
2. Buka file APK lewat **Files** / **Chrome**.
3. Jika muncul peringatan, aktifkan **Install unknown apps** untuk aplikasi yang membuka APK tersebut.
4. Setelah terpasang, buka **Azyan Music**.

### Wajib untuk XOS (Infinix) agar musik tidak mati sendiri

1. **Settings → Apps → Azyan Music → Battery → Unrestricted**
2. Buka **Recent apps**, tarik kartu Azyan Music ke bawah / tekan ikon kunci agar tidak dibersihkan.
3. **Settings → Apps → Azyan Music → Autostart** (jika ada) → aktifkan.

Tanpa langkah ini, XOS sering menghentikan pemutaran di background — ini penyebab paling umum
keluhan "musik berhenti sendiri" di perangkat Infinix.

---

## Struktur proyek

```
app/src/main/java/com/azyan/music/
  MainActivity.kt
  ui/
    WelcomeScreen.kt
    theme/           Color.kt, Theme.kt, Type.kt
app/src/main/res/    strings, themes, ikon adaptif
.github/workflows/android.yml
gradle/libs.versions.toml   (semua versi dependensi)
```

## Catatan build

- Semua versi plugin/dependensi terpusat di `gradle/libs.versions.toml`.
- `gradle/wrapper/gradle-wrapper.jar` ikut di-commit supaya CI bisa menjalankan `./gradlew`
  tanpa Gradle terpasang.
- Belum ada annotation processor (tanpa Room/KSP/Hilt) agar build cloud tetap ringan dan stabil.
