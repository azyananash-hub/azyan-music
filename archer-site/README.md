# ARCHER: website (v0.1)

Static, single-page site. Vite + GSAP ScrollTrigger + Lenis. Fonts are self-hosted (OFL).

## Jalankan

Cara tercepat (pasang dependensi bila perlu, build, lalu serve di port 4173):

```bash
./archer-site/scripts/run-site.sh          # atau: ./scripts/run-site.sh dari dalam archer-site/
```

Otomatis di GitHub: workflow `.github/workflows/archer-site.yml` menjalankan `npm run check`
(build + smoke test) setiap ada perubahan di `archer-site/` dan menyimpan hasil `dist/` sebagai artifact.

```bash
cd archer-site
npm install
npm run dev        # development di http://localhost:5173
npm run build      # hasil statis di dist/
npm run preview    # cek hasil build di http://localhost:4173
```

Deploy: upload isi `dist/` ke host statis mana pun (Netlify, Vercel, GitHub Pages). Tidak ada backend.

## Struktur

- `index.html`: 9 section (hero, manifesto, window, cabin, aircraft, journeys, service, enquire, footer)
- `src/styles.css`: design tokens (`:root`), type scale, responsive, reduced-motion
- `src/main.js`: smooth scroll, animasi scroll, validasi form
- `docs/DESIGN_PROPOSAL.md`: palette, tipografi, dan rencana aset (draft)
- `docs/qa-scroll-desktop-1440.gif`: rekaman scroll turun lalu naik di 1440px

## Yang sudah diuji (Playwright, Chromium)

- Build tanpa error.
- Scroll dari atas ke bawah lalu kembali ke atas di 375, 768, dan 1440px: tidak ada console error, tidak ada overflow horizontal, dan halaman kembali ke posisi awal.
- Pin hanya aktif di desktop (2 pin di 1440px). Dengan `prefers-reduced-motion: reduce`, tidak ada pin sama sekali.
- Validasi form: field kosong, email salah, tanggal lampau, dan jumlah penumpang di luar 1-12 semuanya menampilkan pesan dan `aria-invalid`. Input valid tidak mengirim apa pun; pesan sukses menyatakan bahwa tidak ada yang terkirim.

## Keterbatasan (jujur)

- **Tidak ada aset AI.** Higgsfield (Seedance 2.5, ChatGPT Images 2.5) belum terhubung, jadi jet, awan, dan jendela dibuat dengan CSS dan SVG sederhana. Ini placeholder. Begitu aset tersedia, ganti di `index.html` dan `styles.css`.
- **Choreography bukan hasil analisis video.** Video walkthrough dan situs referensi belum bisa diakses, jadi urutan dan timing dibuat sendiri, bukan dicocokkan dengan referensi.
- **Image sequence dan video scrub belum dibuat.** Rencana di proposal memakai canvas dengan frame WebP. Belum ada frame untuk itu.
- **Tidak ada pengukuran LCP.** Target 2.5 s di HP mid-range belum diukur dengan Lighthouse atau perangkat nyata.
- **Pengujian hanya di Chromium headless.** Belum diuji di Safari iOS.
- **Jet di mobile** masih memakai siluet yang sama dan tidak ada pin di layar kecil.
- **Nama brand "ARCHER"** bentrok dengan Archer Aviation (perusahaan eVTOL terdaftar). Sebelum publik, ganti di `index.html` (`<title>`, `.brand`, footer) dan `package.json`.
- **Form belum terhubung ke backend.** Tidak mengirim apa pun.
- **Pesawat "ARCHER Meridian" dan semua angka spesifikasi fiktif.**
