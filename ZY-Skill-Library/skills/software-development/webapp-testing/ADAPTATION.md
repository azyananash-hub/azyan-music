# Adaptasi ZY: webapp-testing

Klasifikasi: **ADAPTED** (dari IMPORTED).

## Perubahan
- File: `scripts/with_server.py`
- Masalah upstream: server dijalankan dengan `shell=True`; cleanup hanya memanggil `process.terminate()` pada shell. Proses server anak (mis. `python -m http.server`) tetap hidup sebagai yatim dan memblokir port pada run berikutnya. Ini teramati langsung: test pertama meninggalkan proses di port 8765 dan run kedua gagal dengan "Waiting for server".
- Perbaikan: `start_new_session=True` saat start, dan cleanup mengirim SIGTERM/SIGKILL ke process group (`os.killpg`) melalui helper `_signal_group`.

## Verifikasi
- Test `tests/skills/test_governance_and_creative.py::WebappTests` lulus.
- Setelah run, tidak ada proses `http.server 8765` yang tersisa.

## Asal
- SHA-256 (16 karakter, sebelum adaptasi): `b0dcf4918935b795`
- Lisensi: Apache-2.0 (lihat LICENSE.txt). Perubahan ini juga berlisensi Apache-2.0 mengikuti berkas aslinya.
