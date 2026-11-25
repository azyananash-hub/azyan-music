---
name: cinematic-storyboarding
description: Lint a cinematic storyboard: shot integrity, durations against a target runtime, allowed camera moves, and character continuity via a registry that requires costume and palette for every character. Use when planning a short film or cinematic sequence where characters must stay visually consistent across shots.
license: MIT
compatibility: Python 3.9+ standard library only
metadata: {"category": "creative-production", "status": "verified", "owner": "zy"}
---

# cinematic-storyboarding

## Activation Triggers
- User meminta "storyboard", "shot list", "kontinuitas karakter", atau "konsistensi karakter antar-shot".

## Scope dan Batas Kemampuan
- Dicakup: validasi JSON storyboard, durasi total terhadap target, gerak kamera dari daftar izin, dan referensi karakter dari registry.
- TIDAK dicakup: pembuatan gambar atau video, penilaian estetika, dan kualitas akting.

## Required Tools
- Python 3.9+ standard library. `scripts/storyboard_lint.py`

## Input dan Output Specification
Input: JSON dengan target_s, allowed_camera, characters (name, costume, palette wajib), shots (id, duration_s, camera, characters). Output JSON: issues, status PASS/FAIL.

## Execution Workflow
1. Tulis registry karakter dengan kostum dan palet. 2. Susun shot dengan ID unik dan karakter yang merujuk registry. 3. Jalankan lint. 4. Perbaiki semua issue sebelum produksi.

## Decision Rules
- Kostum atau palet kosong berarti kontinuitas tidak bisa dijamin: tolak sampai diisi.
- Gerak kamera di luar daftar izin harus ditambahkan secara sadar, bukan dilewati.

## Error Handling
- JSON rusak atau berkas tidak ada: exit 2 dengan pesan.

## Quality Control
- Total durasi harus sama dengan target bila target diisi.

## Acceptance Criteria
- Storyboard konsisten lulus; karakter tak dikenal, kamera tak diizinkan, dan durasi tak cocok terdeteksi.

## Contoh Implementasi
```bash
python scripts/storyboard_lint.py storyboard.json
```

## Test Cases
`tests/skills/test_v07_batch1.py` (StoryboardTests).

## Referensi dan Sumber
- Metode continuity-by-registry: rancangan internal ZY, tidak menyalin sumber lain.

## Informasi Lisensi
- Skill: MIT.
