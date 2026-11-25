---
name: quality-gate
description: Run a two-layer quality gate on a rendered video: automated technical QC with ffprobe (resolution, frame rate, duration, audio presence) and a separate artistic QC rubric that stays PENDING_REVIEW until a named reviewer approves every criterion. Use before publishing a video, so that passing technical checks is never mistaken for artistic approval.
license: MIT
compatibility: Python 3.9+; ffmpeg and ffprobe on PATH
metadata: {"category": "governance", "status": "verified", "owner": "zy"}
---

# quality-gate

## Activation Triggers
- User meminta "QC video", "cek fps dan resolusi", "gerbang kualitas", atau "review artistik sebelum rilis".

## Scope dan Batas Kemampuan
- Dicakup: pemeriksaan teknis otomatis (dimensi, fps, durasi, audio) dan rubrik artistik dengan status PENDING_REVIEW, APPROVED, atau REJECTED.
- TIDAK dicakup: penilaian estetika otomatis, loudness target (dapat ditambah lewat ffmpeg-skill), dan pemeriksaan frame per frame.

## Required Tools
- Python 3.9+ dengan ffmpeg dan ffprobe. `scripts/qc_gate.py`.

## Input dan Output Specification
Input: video dan parameter --width, --height, --fps, --duration, --audio, opsional --rubric JSON (reviewer, scores untuk 6 kriteria 1-5, approved). Output JSON: technical, artistic, overall.

## Execution Workflow
1. Tetapkan spesifikasi dari brief. 2. Jalankan technical QC. 3. Minta peninjau mengisi rubrik. 4. Rilis hanya bila technical PASS dan artistic APPROVED.

## Decision Rules
- Technical PASS tidak berarti artistic APPROVED.
- Rubrik tanpa nama peninjau atau tanpa semua kriteria tetap PENDING_REVIEW.

## Error Handling
- Video tidak bisa dibaca: exit 2 dengan pesan ffprobe.

## Quality Control
- Setiap kriteria artistik dinilai manual oleh manusia; skill tidak memberi skor otomatis.

## Acceptance Criteria
- Video 1080x1920 60 fps 4 detik lulus technical; fps 30 atau durasi salah gagal; artistic tetap PENDING tanpa rubrik.

## Contoh Implementasi
```bash
python scripts/qc_gate.py video.mp4 --width 1080 --height 1920 --fps 60 --duration 4 --audio --rubric rubrik.json
```

## Test Cases
`tests/skills/test_v07_foundation.py` (QcGateTests) dengan video ffmpeg sungguhan.

## Referensi dan Sumber
- ffprobe (bagian ffmpeg). Kriteria rubrik: rancangan internal ZY.

## Informasi Lisensi
- Skill: MIT.
