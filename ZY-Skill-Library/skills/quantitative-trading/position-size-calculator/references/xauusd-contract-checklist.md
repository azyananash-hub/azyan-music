# Checklist verifikasi kontrak sebelum menghitung lot

Isi dari spesifikasi broker Anda sendiri. Nilai di bawah adalah placeholder yang harus diverifikasi:

- [ ] Ukuran kontrak 1 lot (umumnya dinyatakan dalam ons untuk XAUUSD; verifikasi).
- [ ] Nilai mata uang akun per 1.00 pergerakan harga per 1 lot (konversi bila akun bukan USD).
- [ ] Minimum lot, step lot, dan maksimum lot.
- [ ] Spread dan komisi yang berlaku (masukkan ke biaya, bukan ke asumsi nol).
- [ ] Jam perdagangan dan perilaku gap saat pembukaan/penutupan.
- [ ] Margin requirement dan leverage. Ukuran posisi tidak boleh membuat margin call dalam skenario normal.
