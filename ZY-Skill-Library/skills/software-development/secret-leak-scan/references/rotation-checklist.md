# Checklist rotasi secret

1. Identifikasi penyedia (Google Cloud, Supabase, OpenAI, dll.) dan nama key.
2. Buat key baru di konsol penyedia dengan scope terkecil.
3. Perbarui konfigurasi lokal dan CI (GitHub Actions secrets), bukan kode.
4. Nonaktifkan atau hapus key lama.
5. Periksa log penggunaan penyedia untuk aktivitas tak wajar selama masa terekspos.
6. Jika key pernah ada di riwayat git publik, pertimbangkan membersihkan riwayat; tetapi rotasi tetap wajib karena riwayat mungkin sudah tersalin.
