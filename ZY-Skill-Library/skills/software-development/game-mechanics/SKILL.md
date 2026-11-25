---
name: game-mechanics
description: Compute game progression mechanics: XP per answer with streak multipliers and caps, level thresholds, and linear survival resource decay such as hunger or stamina. Use for gamifying learning apps or survival game balance checks, with explicit tunable parameters.
license: MIT
compatibility: Python 3.9+ standard library only
metadata: {"category": "software-development", "status": "verified", "owner": "zy"}
---

# game-mechanics

## Activation Triggers
- User meminta "XP", "level", "streak", "gamifikasi", "survival", "hunger", atau "stamina".

## Scope dan Batas Kemampuan
- Dicakup: rumus XP dengan streak dan cap, ambang level, peluruhan linear sumber daya survival.
- TIDAK dicakup: ekonomi game penuh, balancing lewat playtest, dan rendering.

## Required Tools
- Python 3.9+ standard library. `scripts/mechanics.py`

## Input dan Output Specification
Fungsi: xp_for_answer, level_threshold, level_for_xp, survival_value, seconds_until_empty. Parameter desain diberikan pemanggil.

## Execution Workflow
1. Tetapkan parameter dari target retensi atau keseimbangan. 2. Hitung XP dan level untuk skenario uji. 3. Verifikasi dengan playtest sebelum rilis.

## Decision Rules
- Nilai default bukan standar; ubah sesuai data pengguna.
- Cap streak mencegah inflasi XP; jangan dihapus tanpa alasan.

## Error Handling
- Parameter negatif atau level < 1: ValueError.

## Quality Control
- Level naik tepat saat XP mencapai ambang.

## Acceptance Criteria
- XP streak 5 dengan dasar 10 menghasilkan 15; ambang level 2 = 100 dan level 3 = 300; survival 100 turun 20 setelah 10 detik pada laju 2.

## Contoh Implementasi
```python
from mechanics import xp_for_answer, level_for_xp
print(xp_for_answer(10, 5), level_for_xp(300))
```

## Test Cases
`tests/skills/test_v07_batch1.py` (MechanicsTests).

## Referensi dan Sumber
- Rumus progresi dirancang ulang; tidak menyalin mekanik game tertentu.

## Informasi Lisensi
- Skill: MIT.
