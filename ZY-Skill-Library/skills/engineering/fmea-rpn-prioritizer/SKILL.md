---
name: fmea-rpn-prioritizer
description: Prioritize failure modes from a FMEA worksheet (CSV with severity, occurrence, detection 1-10) by Risk Priority Number and flag high-severity items for review. Use for preventive maintenance, industrial utility reliability reviews, root cause analysis, and DMAIC improvement planning.
license: MIT
compatibility: Python 3.9+ standard library only
metadata: {"category": "engineering", "status": "verified", "owner": "zy"}
---

# FMEA RPN Prioritizer

## Activation Triggers
- User meminta "FMEA", "RPN", "risk priority", "prioritas perbaikan", atau "failure mode".
- Task preventive maintenance untuk utilitas industri (boiler, cooling tower, kompresor, WTP/RO) yang butuh daftar prioritas.
- Tahap "Analyze" atau "Improve" pada DMAIC yang membutuhkan urutan risiko.

## Scope dan Batas Kemampuan
- Dicakup: validasi worksheet CSV, perhitungan RPN = S x O x D, pengurutan, dan flag tindak lanjut.
- TIDAK dicakup: penilaian S/O/D itu sendiri (harus dari tim dan data nyata), analisis kuantitatif MTBF/MTTR, atau FMEA berbasis AIAG-VDA Action Priority penuh.
- Skor S/O/D adalah keputusan tim. Script tidak boleh diberi skor karangan.

## Required Tools
- Python 3.9+ standard library.
- `scripts/fmea_rpn.py`.

## Input dan Output Specification
Input CSV, kolom wajib: `item, failure_mode, severity, occurrence, detection`. Kolom opsional: `effect, cause, control`.
Setiap skor harus bilangan bulat 1-10.

Output: daftar terurut RPN tertinggi dulu, dengan flag:
- `RPN_ABOVE_THRESHOLD` (default RPN >= 100)
- `HIGH_SEVERITY_REVIEW` (default S >= 9), tetap ditinjau meskipun RPN rendah.

Format teks atau `--json`.

## Execution Workflow
1. Pastikan worksheet memakai skala 1-10 yang didefinisikan tim (lampirkan tabel skala).
2. Simpan sebagai CSV UTF-8.
3. Jalankan `python scripts/fmea_rpn.py worksheet.csv --rpn-threshold 100`.
4. Tinjau item berflag: tentukan tindakan (eliminasi, kontrol, deteksi lebih baik).
5. Setelah tindakan, skor ulang O/D dan hitung ulang; catat perubahan di log.

## Decision Rules
- Severity >= 9 selalu perlu tinjauan, walau RPN kecil. Ini mencegah kombinasi kecil-kecil menutupi risiko keselamatan.
- Jangan menurunkan S hanya karena tindakan ditambahkan; S hanya turun bila desain/proses berubah.
- Jika data kejadian (occurrence) tidak tersedia, tandai skor O sebagai estimasi.
- Untuk item keselamatan personel, tindak lanjuti sesuai SOP dan batas keselamatan, bukan hanya RPN.

## Error Handling
- Kolom wajib hilang: error dan exit code 2.
- Skor di luar 1-10 atau bukan integer: error menyebut nomor baris.
- File CSV kosong: error.

## Quality Control
- Verifikasi jumlah baris input = jumlah baris output.
- Bandingkan satu nilai RPN dengan perhitungan manual.
- Jalankan unit test (`tests/test_fmea_rpn.py`).

## Acceptance Criteria
- RPN untuk (S=8, O=5, D=4) sama dengan 160.
- Urutan output menurun berdasarkan RPN.
- Item S >= 9 selalu ter-flag `HIGH_SEVERITY_REVIEW`.
- Input tidak valid tidak pernah menghasilkan output parsial diam-diam.

## Contoh Implementasi
```csv
item,failure_mode,effect,cause,severity,occurrence,detection,control
Boiler feedwater pump,Seal leak,Loss of feedwater,Seal wear,8,5,4,Monthly vibration check
Cooling tower fan,Bearing failure,Reduced cooling,Lack of lubrication,6,4,6,Oil sample
```
```bash
python scripts/fmea_rpn.py worksheet.csv --rpn-threshold 100 --severity-threshold 9
```

## Test Cases
Lihat `tests/test_fmea_rpn.py`:
1. RPN 8x5x4 = 160.
2. Skor 0 dan 11 ditolak.
3. Kolom wajib hilang ditolak.
4. Urutan descending dan flag berjalan.

## Referensi dan Sumber
- Metode FMEA klasik (konvensi RPN 1-10) dan AIAG-VDA FMEA Handbook (2019) sebagai pembanding Action Priority.
- Lihat `references/fmea-scales-example.md` untuk contoh tabel skala.

## Informasi Lisensi
- Kode dan dokumentasi: `MIT`. Metode FMEA adalah metode publik; skill tidak menyalin teks standar AIAG-VDA.
