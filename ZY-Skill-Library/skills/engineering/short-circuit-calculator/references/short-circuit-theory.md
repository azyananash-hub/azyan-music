# Ringkasan teori: gangguan 3 fasa simetris (aproksimasi)

## Rumus yang dipakai
- Impedansi sumber dari MVA hubung singkat: `|Z_s| = V^2 / S_sc` (ohm, V dalam kV, S dalam MVA).
- Dengan rasio X/R = k: `X = |Z| * k / sqrt(1 + k^2)`, `R = X / k`.
- Impedansi trafo (referensi sisi sekunder): `Z_T = (Z% / 100) * V_sec^2 / S_rated`.
- Arus simetris: `I_k = V / (sqrt(3) * |Z_total|)`, dengan V kV dan Z ohm menghasilkan kA.
- Faktor puncak (IEC 60909): `kappa = 1.02 + 0.98 * exp(-3 R/X)`.
- Arus puncak: `i_p = sqrt(2) * kappa * I_k`.

## Asumsi
1. Gangguan 3 fasa simetris, tanpa resistansi busur.
2. Sumber dan trafo linier; tap changer diabaikan.
3. Kontribusi motor diabaikan (dapat signifikan di industri, perlu ditambahkan pada studi lengkap).
4. Tegangan sebelum gangguan diasumsikan 1.0 pu (faktor c IEC 60909 tidak dimodelkan).

## Batasan yang harus disampaikan ke pengguna
- Untuk pemilihan rating pemutus atau sistem proteksi, gunakan studi lengkap dan standar yang berlaku.
- Rasio X/R default 10 adalah asumsi umum; isi dengan data nyata bila tersedia.
