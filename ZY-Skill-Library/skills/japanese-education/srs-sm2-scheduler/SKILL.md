---
name: srs-sm2-scheduler
description: Schedule spaced-repetition reviews for Japanese vocabulary, kanji, and grammar cards using the SM-2 algorithm (quality 0-5, ease factor, interval days). Use when building or testing review logic for JLPT N5-N1 study tools such as AmiraVerse, or when computing next due dates for flashcards.
license: original-zy
compatibility: Python 3.9+ standard library only
metadata: {"category": "japanese-education", "status": "validated", "owner": "zy"}
---

# SRS SM-2 Scheduler (Japanese Flashcards)

## Activation Triggers
- User meminta "spaced repetition", "SRS", "jadwal review", "SM-2", "flashcard", atau "kapan kartu diulang".
- Pengembangan fitur review pada aplikasi belajar bahasa Jepang (AmiraVerse) atau modul kosakata JLPT.
- Perlu membuat test atau referensi perilaku penjadwalan yang deterministik.

## Scope dan Batas Kemampuan
- Dicakup: state kartu (ease factor, repetitions, interval), satu langkah review, dan tanggal jatuh tempo.
- TIDAK dicakup: penyimpanan database, UI, sinkronisasi, pembelajaran adaptif berbasis model, dan optimasi parameter per pengguna (FSRS).
- Algoritma ini tidak menjamin retensi; ia hanya jadwal heuristik.

## Required Tools
- Python 3.9+ standard library.
- `scripts/sm2.py`.
- Untuk implementasi produksi lanjutan: pertimbangkan FSRS (repo open-spaced-repetition/fsrs4anki, lisensi MIT, diverifikasi pada halaman LICENSE publik). Verifikasi ulang sebelum adopsi.

## Input dan Output Specification
- Input: `CardState(ease_factor, repetitions, interval_days)`, `quality` integer 0-5, dan `reviewed_on` (date).
- Output: `CardState` baru (immutable) dan `next_due(state, reviewed_on)`.
- Skala quality: 5 sempurna; 4 benar dengan sedikit ragu; 3 benar tetapi sulit; 2 salah tetapi terasa dekat; 1 salah; 0 blank.

## Execution Workflow
1. Muat state kartu dari penyimpanan (default baru: EF 2.5, repetitions 0, interval 0).
2. Minta quality dari user setelah jawaban. Jangan memakai quality yang dihitung otomatis tanpa konfirmasi untuk kasus ambigu.
3. Panggil `review(state, quality)`.
4. Simpan state baru dan `next_due`.

## Decision Rules
- quality < 3: reset repetitions ke 0, interval 1 hari, EF tetap diturunkan.
- EF tidak pernah di bawah 1.3.
- Repetition pertama benar: interval 1 hari; kedua: 6 hari; selanjutnya: interval x EF (dibulatkan half-up).
- Kartu yang baru saja gagal sebaiknya diulang dalam sesi yang sama; script ini tidak mengatur sesi.

## Error Handling
- Quality di luar 0-5 atau bukan integer: `ValueError`.
- Tanggal bukan `datetime.date`: tidak tervalidasi oleh fungsi; panggilan harus memberi tipe yang benar.

## Quality Control
- Verifikasi nilai EF untuk quality 4 tetap 2.5 (delta = 0).
- Verifikasi urutan interval 1, 6, lalu kira-kira 15 untuk EF 2.5 pada review ketiga.
- Unit test `tests/test_sm2.py` lulus.

## Acceptance Criteria
- Dari state baru, review quality 4 memberi interval 1, repetitions 1.
- Review kedua quality 4 memberi interval 6.
- Review ketiga quality 4 dengan EF 2.5 memberi interval 15.
- Quality 2 mereset repetitions dan tidak membuat EF < 1.3.

## Contoh Implementasi
```python
import datetime as dt
from scripts.sm2 import CardState, review, next_due

s = CardState()
s = review(s, 4)  # interval 1
s = review(s, 4)  # interval 6
s = review(s, 4)  # interval 15
print(s, next_due(s, dt.date(2026, 1, 1)))
```

## Test Cases
Lihat `tests/test_sm2.py`:
1. Urutan interval 1, 6, 15 untuk quality 4.
2. Kegagalan mereset repetitions.
3. Batas bawah EF 1.3.
4. Quality invalid ditolak.

## Referensi dan Sumber
- Wozniak, P. A. (1990), algoritma SM-2 (SuperMemo). Formula dirujuk, implementasi ditulis ulang.
- FSRS: open-spaced-repetition (lihat `references/sources-and-licenses.md`).

## Informasi Lisensi
- Kode dan dokumentasi: `original-zy`. Algoritma SM-2 adalah metode yang dipublikasikan; implementasi ini ditulis ulang, tidak menyalin kode pihak ketiga.
