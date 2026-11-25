---
name: narration-subtitle-sync
description: Align SRT subtitles to a narration audio duration, validate cue timing and overlaps, and measure integrated loudness and true peak with ffmpeg. Use for human or external narration; no TTS model is downloaded.
license: MIT
compatibility: Python 3.9+; ffmpeg and ffprobe on PATH for audio measurement
metadata: {"category": "creative-production", "status": "verified", "owner": "zy"}
---

# narration-subtitle-sync

## Activation Triggers
- User memiliki narasi (rekaman, audio eksternal, atau TTS yang sudah ada) dan subtitle SRT yang harus sinkron.

## Scope dan Batas Kemampuan
- Dicakup: parsing SRT, penyesuaian linier ke durasi audio, validasi overlap dan kecepatan baca (parameter), pengukuran loudness.
- Word alignment (v0.7): forced alignment lokal dengan pocketsphinx (BSD) hanya bahasa Inggris, model ikut di paket pip; bahasa Jepang BLOCKED karena model Jepang tidak terjangkau. Timing dari sumber eksternal (JSON) didukung. TIDAK dicakup: TTS (tidak diunduh) dan mastering penuh.

## Required Tools
- Python 3.9+; ffmpeg/ffprobe (opsional untuk audio). `scripts/subtitle_sync.py`, `scripts/word_align.py` (opsional: pocketsphinx untuk alignment bahasa Inggris)

## Input dan Output Specification
Input: file SRT, file audio (opsional), max-cps (default 17, parameter Anda). Output: JSON isu dan loudness; SRT tersinkron dengan --out.

## Execution Workflow
1. Siapkan narasi (rekaman atau audio eksternal). 2. Jalankan dengan --audio untuk menyesuaikan durasi. 3. Perbaiki isu overlap. 4. Ukur loudness dan cocokkan target yang Anda tetapkan.

## Decision Rules
- Jika narasi tidak sejalan dengan teks subtitle, penyesuaian linier tidak cukup; periksa manual.
- Target loudness diambil dari spesifikasi platform/klien, bukan dari skill.

## Error Handling
- Timestamp tidak valid atau ffprobe tidak tersedia: ValueError/RuntimeError, exit 2.

## Quality Control
- Tidak ada overlap; durasi sesudah scaling sama dengan durasi audio.

## Acceptance Criteria
- Test SubtitleTests lulus termasuk pengukuran loudnorm ffmpeg pada sinyal sinus.

## Contoh Implementasi
```bash
python scripts/subtitle_sync.py narasi.srt --audio narasi.wav --out narasi-sync.srt
```

## Test Cases
`tests/skills/test_v05_custom.py` (SubtitleTests).

## Referensi dan Sumber
- ffmpeg loudnorm (filter bawaan, LGPL/GPL sesuai build ffmpeg; dipanggil sebagai tool, tidak disalin).

## Informasi Lisensi
- Skill: MIT.
