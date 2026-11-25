---
name: technology-selection
description: Choose a production technology (Remotion, Three.js, HTML canvas, SVG, or clipacanvas render) from stated needs such as 2D or 3D, text-heavy, vertical format, determinism, and quality target, with a deterministic ranking that reports unmet needs and quality shortfalls. Use when deciding how to produce a motion graphic or video before building it.
license: MIT
compatibility: Python 3.9+ standard library only
metadata: {"category": "governance", "status": "verified", "owner": "zy"}
---

# technology-selection

## Activation Triggers
- User meminta "pilih teknologi", "Remotion atau Three.js", "teknologi untuk video vertikal", atau "target kualitas produksi".

## Scope dan Batas Kemampuan
- Dicakup: peringkat deterministik dari kebutuhan yang dinyatakan, dengan kebutuhan tak terpenuhi dan target kualitas ditampilkan.
- TIDAK dicakup: benchmark performa, estimasi biaya render, dan keputusan tim.
- Matriks adalah penilaian kualitatif dari dokumentasi skill, bukan hasil pengukuran.

## Required Tools
- Python 3.9+ standard library. `scripts/select_tech.py`, `references/tech-matrix.json`.

## Input dan Output Specification
Input: --need (berulang, mis. 2d, 3d, text-heavy, vertical, interactive, deterministic, offline) dan --quality draft|broadcast|cinematic. Output JSON: peringkat opsi dengan score, needs_met, needs_missing, quality_target_met.

## Execution Workflow
1. Daftarkan kebutuhan produksi secara eksplisit. 2. Pilih target kualitas. 3. Jalankan select. 4. Periksa opsi teratas beserta kebutuhan yang tidak terpenuhi sebelum membangun.

## Decision Rules
- Opsi yang tidak memenuhi target kualitas diberi penalti, tetapi tetap ditampilkan.
- Jika skor teratas punya kebutuhan tak terpenuhi, putuskan secara sadar, jangan diabaikan.

## Error Handling
- Kualitas di luar draft/broadcast/cinematic: ValueError.

## Quality Control
- Urutan selalu deterministik untuk kebutuhan yang sama.

## Acceptance Criteria
- Kebutuhan 2d, text-heavy, vertical dengan broadcast menempatkan remotion di puncak; kualitas cinematic menandai remotion tidak memenuhi target.

## Contoh Implementasi
```bash
python scripts/select_tech.py --need 2d --need text-heavy --need vertical --quality broadcast
```

## Test Cases
`tests/skills/test_v07_foundation.py` (TechSelectionTests).

## Referensi dan Sumber
- Dokumentasi skill di library (status dan kemampuan); penilaian kualitatif ditandai di references/tech-matrix.json.

## Informasi Lisensi
- Skill: MIT.
