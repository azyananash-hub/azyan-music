# Batasan minifier ClipACanvas

- Minifier bersifat konservatif: hanya menghapus komentar HTML, baris kosong, dan indentasi.
- Blok `<script>`, `<style>`, `<pre>`, dan `<textarea>` tidak disentuh, sehingga aman untuk JS template literal dan CSS.
- Tidak ada penghapusan nama variabel atau dead code; untuk JS panjang gunakan minifier khusus (mis. terser, lisensi BSD-2-Clause; verifikasi sebelum pakai).
- Penggabungan baris memakai newline, bukan string kosong, agar kata tidak menyatu.
- Panjang URL: setelah URL encoding, ukuran bisa naik 2-3 kali lipat untuk karakter non-ASCII dan simbol. Periksa `url_chars`.
