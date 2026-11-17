# ARCHER — Design Proposal (STOP 2, DRAFT)

> **Status: DRAFT, belum disetujui. Tidak ada aset yang di-generate.**
>
> Dokumen ini dibuat **tanpa** video walkthrough, tanpa gambar referensi jet/jendela, dan tanpa akses
> ke situs referensi (host diblokir). Karena itu **STOP 1 (Analysis Report) belum ada**, dan urutan
> section + choreography di bawah adalah **hipotesis desain**, bukan hasil analisis video. Begitu video
> tersedia, Bagian 4 akan direvisi agar mengikuti timing aslinya.

---

## 0. Keputusan yang diambil (atas instruksi "lakukan sendiri")

| Item | Keputusan | Alasan |
|---|---|---|
| Stack | Vanilla HTML/CSS/JS + **Vite** + **GSAP 3 ScrollTrigger** + **Lenis** | Efek utama = pin/scrub/zoom berbasis scroll; GSAP paling matang dan seluruh plugin gratis. Tanpa React → bundle kecil, LCP lebih baik. Output statis → hosting gratis. |
| Lokasi kode | Folder `archer-site/` di branch ini | Repo baru butuh tindakan Anda; folder terpisah tidak menyentuh kode Android. Mudah dipindah ke repo sendiri nanti (`git subtree split`). |
| Brand | **ARCHER** (sementara) | ⚠️ Ada perusahaan aviasi nyata "Archer Aviation" (NYSE: ACHR). Disarankan ganti sebelum publik. Nama dibuat sebagai satu token di CSS/HTML sehingga mudah diganti. |
| Pesawat | Fiktif: **ARCHER Meridian** | Tidak memakai nama/spec pabrikan. |
| Bahasa | English | Sesuai brief. |

---

## 1. Palette

Semua rasio dihitung dengan rumus WCAG 2.x relative luminance (skrip, bukan perkiraan).

| Token | Hex | Peran |
|---|---|---|
| `--ink` | `#0A0A0B` | Background utama (hitam hangat, bukan #000 murni agar video gelap tidak "banding") |
| `--surface` | `#141416` | Kartu, form |
| `--surface-2` | `#1C1C1F` | Hover / input |
| `--ivory` | `#F3EFE7` | Teks utama (off-white) |
| `--ivory-muted` | `#B9B3A8` | Teks sekunder, caption |
| `--gold` | `#C8A96A` | Champagne gold: aksen, label, garis aktif, CTA |
| `--gold-deep` | `#A88B4F` | Gold untuk state hover/pressed |
| `--line` | `#3A3833` | Hairline dekoratif (BUKAN untuk teks) |

| Kombinasi | Rasio | WCAG |
|---|---|---|
| ivory on ink | **17.26:1** | AAA |
| ivory on surface-2 | 14.82:1 | AAA |
| ivory-muted on ink | **9.50:1** | AAA |
| ivory-muted on surface-2 | 8.16:1 | AAA |
| gold on ink | **8.80:1** | AAA |
| gold on surface-2 | 7.56:1 | AAA |
| gold-deep on ink | 6.10:1 | AA (AAA untuk teks besar) |
| ink on gold (teks tombol CTA) | 8.80:1 | AAA |
| line on ink | 1.69:1 | ❌ dekorasi saja; border input memakai `--ivory-muted` agar ≥3:1 (non-text contrast) |

**Teks di atas video:** rasio di atas tidak berlaku otomatis. Setiap teks di atas video/gambar mendapat
gradient scrim `rgba(10,10,11,.0 → .65)`; target ≥4.5:1 akan diverifikasi per frame terang saat testing.

---

## 2. Typography (OFL, Google Fonts, tanpa italic)

| Peran | Font | Lisensi | Weight dipakai |
|---|---|---|---|
| Display serif | **Cormorant Garamond** | SIL OFL 1.1 | 400, 500 (upright saja) |
| Body sans | **Manrope** | SIL OFL 1.1 | 400, 500, 600 |

Catatan kritis: Cormorant sangat tipis di ukuran kecil → **hanya dipakai ≥ 28px**. Semua teks UI/body
memakai Manrope. Font di-*self-host* (subset Latin, `woff2`, `font-display: swap`) agar tidak ada
request ke Google saat runtime dan mengurangi layout shift (`size-adjust` fallback).

Type scale (fluid, `clamp()`, rasio ≈ 1.25; min di 375px, max di 1440px):

| Token | Font | Ukuran | Line-height | Tracking |
|---|---|---|---|---|
| `display-xl` | Cormorant 400 | clamp(48px, 9vw, 128px) | 0.95 | -0.01em |
| `display-l` | Cormorant 400 | clamp(40px, 6vw, 88px) | 1.0 | -0.01em |
| `h2` | Cormorant 500 | clamp(32px, 4vw, 56px) | 1.08 | 0 |
| `h3` | Cormorant 500 | clamp(28px, 2.6vw, 36px) | 1.15 | 0 |
| `eyebrow` | Manrope 600 | 12px | 1.4 | 0.24em, uppercase, gold |
| `body-l` | Manrope 400 | clamp(17px, 1.3vw, 20px) | 1.6 | 0 |
| `body` | Manrope 400 | 16px | 1.65 | 0 |
| `small` | Manrope 500 | 13px | 1.5 | 0.02em |
| `spec-num` | Cormorant 400 | clamp(44px, 5vw, 72px) | 1.0 | tabular-nums |

---

## 3. Struktur teknis choreography

- **Smooth scroll:** Lenis, disinkronkan ke `gsap.ticker`.
- **Pinned sections:** `ScrollTrigger` `pin: true`, `scrub: 0.6`, `anticipatePin: 1`.
- **Video yang di-scrub → image sequence di `<canvas>`**, bukan `video.currentTime`. Seek video di iOS
  Safari tidak frame-accurate dan sering patah. Frame: WebP, ~1600px (desktop) / ~900px (mobile),
  di-preload bertahap (frame kunci dulu, lalu sisanya).
- **Video yang hanya loop (tidak di-scrub)** → `<video muted playsinline loop>` MP4 H.264 + WebM,
  dengan `poster`, di-lazy-load via `IntersectionObserver`.
- **Clouds** → 3 layer gambar/video terpisah dengan kecepatan parallax berbeda (lihat Bagian 6).
- `prefers-reduced-motion: reduce` → semua `ScrollTrigger` tidak dibuat; section jadi statis dengan
  fade-in 300ms via `IntersectionObserver`; video tidak autoplay (poster saja).

---

## 4. Section sequence (HIPOTESIS, menunggu video)

Scroll height dalam `vh` = jarak scroll yang dihabiskan section (termasuk durasi pin).

| # | Section | Tujuan | Scroll | Pin | Transisi masuk → keluar |
|---|---|---|---|---|---|
| 1 | **Hero: Above the Clouds** | Kesan pertama, brand | 250vh | ✅ | Load: fade dari hitam + headline mask-reveal per baris → Jet bergerak dari jauh mendekat (image sequence), awan parallax, headline naik & fade |
| 2 | **Manifesto** | Positioning brand (2–3 kalimat) | 120vh | ❌ | Kata-kata menyala dari muted → ivory sesuai scroll (scrub opacity per kata) |
| 3 | **Through the Window** | Transisi eksterior → interior | 300vh | ✅ | Frame jendela membesar (scale 1 → ~8) hingga bukaan jendela memenuhi layar; di dalam bukaan terlihat awan/cakrawala; keluar dengan crossfade ke kabin |
| 4 | **The Cabin** | Pengalaman interior (zona kabin) | 300vh | ✅ | Horizontal scroll 3–4 panel (Lounge, Dining, Suite) didorong scroll vertikal |
| 5 | **The Aircraft: Meridian** | Spec fiktif | 150vh | ✅ (pendek) | Profil jet samping; angka spec count-up saat masuk; garis gold tergambar (stroke-dashoffset) |
| 6 | **Journeys** | Contoh rute/destinasi | 100vh | ❌ | Kartu reveal bertahap (stagger) |
| 7 | **Service** | Concierge, crew, keamanan | 100vh | ❌ | Fade + translateY 24px |
| 8 | **Enquire** | Form booking | auto | ❌ | Fade; form tanpa animasi berat |
| 9 | **Footer** | Navigasi, legal | auto | ❌ | — |

Total ±1.300vh (≈ 13 layar di desktop). **Mobile (<768px):** section 3 dan 4 diganti versi ringan
(window: scale lebih kecil tanpa pin panjang; cabin: kartu vertikal biasa). Akan ditulis eksplisit
di laporan delivery.

---

## 5. Asset plan (belum di-generate)

Model sesuai brief: gambar = **ChatGPT Images 2.5**, video = **Seedance 2.5** (via Higgsfield).
**Status saat ini: Higgsfield belum terhubung → model ID belum terverifikasi.**

| ID | Aset | Model | Ringkasan prompt | Rasio | Resolusi | Durasi | Animasi dengan scroll |
|---|---|---|---|---|---|---|---|
| A1 | Jet concept (still) | Images 2.5 | Business jet fiktif long-range, livery hitam-ivory + pinstripe champagne, 3/4 depan, di atas lautan awan saat golden hour, tanpa logo/registrasi nyata | 16:9 | 2048×1152 | — | Poster/LCP hero, juga first frame video V1 |
| A2 | Window concept (still) | Images 2.5 | Jendela kabin oval dari dalam, bezel kulit krem + trim gold, tampak lurus (orthographic), bukaan **hitam/hijau polos** agar mudah di-mask | 1:1 | 2048×2048 | — | Diolah jadi PNG alpha/SVG mask, di-scale pada section 3 |
| A3 | Cloud plates ×3 | Images 2.5 | (a) lautan awan jauh, (b) awan cumulus tengah, (c) wisps dekat; latar transparan atau hitam untuk `screen` blend | 21:9 | 2560×1100 | — | Parallax 3 layer |
| A4 | Cabin panels ×3 | Images 2.5 | Lounge, dining, suite; material krem/walnut/gold; tanpa merek | 3:2 | 2400×1600 | — | Horizontal pin section 4 |
| A5 | Jet side profile | Images 2.5 | Profil samping bersih di latar hitam untuk spec section | 21:9 | 2560×1100 | — | Reveal + garis spec |
| V1 | Jet approach | Seedance 2.5 (image-to-video dari A1) | Kamera stabil, jet bergerak pelan mendekat & sedikit banking, awan mengalir | 16:9 | 1920×1080 | 6–8 s | **Di-extract ke ±120 frame WebP** → scrub di canvas (hero) |
| V2 | Cloud drift | Seedance 2.5 (dari A3a) | Awan bergerak perlahan, tanpa objek | 16:9 | 1920×1080 | 8–10 s, seamless loop | Loop video di dalam bukaan jendela (section 3) |
| V3 | Cabin ambience (opsional) | Seedance 2.5 (dari A4 lounge) | Dolly-in sangat lambat, cahaya matahari bergeser | 16:9 | 1920×1080 | 6 s | Loop, lazy-load |

Deliverable video: MP4 (H.264, CRF ~24, `+faststart`) + WebM (VP9, CRF ~34), poster JPG/WebP, target
< 3 MB per clip desktop, < 1.5 MB versi mobile 960px. Tidak ada clip > 10 s.

---

## 6. Clouds: gerak & layering

Urutan z-index di hero (belakang → depan):

1. **Sky gradient** (CSS): hitam → amber gelap tipis di cakrawala.
2. **Cloud far (A3a):** `yPercent` 0 → -10 sepanjang pin (paling lambat), sedikit `scale` 1 → 1.05.
3. **Jet (V1 canvas):** frame sequence mengikuti progress scroll.
4. **Cloud mid (A3b):** `yPercent` 0 → -35, `x` -2% → 2%; `mix-blend-mode: screen`. Sebagian melintas
   **di depan** ekor jet → memberi kedalaman.
5. **Cloud near (A3c):** `yPercent` 20 → -80 (paling cepat), blur 4–8px, opacity 0.5 → 0; menyapu
   layar di akhir hero sebagai "wipe" menuju section 2.
6. **Headline + scrim.**

Mobile: hanya layer 1, 2, 3, 5 dan jarak parallax dikurangi 50%.

---

## 7. Window → cinematic frame / mask

1. A2 diproses menjadi PNG dengan **bukaan transparan** (mask dari area polos), plus versi SVG path
   bukaan oval untuk `clip-path` (lebih tajam saat di-scale).
2. Layout section 3 (pinned 300vh):
   - **0–15%:** layar hitam, frame jendela muncul (opacity 0 → 1) di tengah dengan ukuran ±40vh.
     Di dalam bukaan: loop V2 (awan).
   - **15–35%:** eyebrow + headline pendek muncul di samping jendela.
   - **35–85%:** frame jendela **scale 1 → ~8**, origin tepat di pusat bukaan, teks fade out.
     Bukaan membesar sampai memenuhi viewport → pengguna "masuk ke langit".
   - **85–100%:** awan crossfade ke panel kabin pertama (masuk ke section 4).
3. Kinerja: hanya `transform`/`opacity` yang dianimasikan (GPU), `will-change` dipasang selama pin saja.

---

## 8. Yang masih memblokir

| Blocker | Dampak | Yang dibutuhkan dari Anda |
|---|---|---|
| Video walkthrough tidak ada | STOP 1 tidak bisa dibuat; Bagian 4 masih hipotesis | Upload video ke sesi / commit ke repo |
| Gambar referensi jet & jendela | Prompt A1/A2 belum bisa disesuaikan | Upload |
| Higgsfield MCP tidak terhubung | Tidak bisa generate aset apa pun | Hubungkan connector di claude.ai, lalu sesi baru |
| Situs referensi diblokir | Struktur/urutan section tidak bisa diverifikasi | Izinkan host, atau terima tanpa inspeksi |

**Approval yang diminta:** konsep jet (A1/V1), awan (A3/V2, Bagian 6), dan jendela (A2, Bagian 7).
