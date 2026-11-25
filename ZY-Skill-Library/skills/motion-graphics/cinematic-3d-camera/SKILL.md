---
name: cinematic-3d-camera
description: Generate smooth 3D camera paths from keyframes with Catmull-Rom interpolation that passes exactly through each keyframe and keeps velocity continuous, sampled at a fixed frame rate. Use to drive the camera of Three.js, Remotion, or other 3D scenes in cinematic shots.
license: MIT
compatibility: Python 3.9+ standard library only
metadata: {"category": "motion-graphics", "status": "verified", "owner": "zy", "classification": "CUSTOM"}
---

# cinematic-3d-camera

## Activation Triggers
- User meminta "jalur kamera", "camera path", "keyframe kamera", "gerak kamera halus", atau "dolly 3D".

## Scope dan Batas Kemampuan
- Dicakup: interpolasi Catmull-Rom uniform dari keyframe posisi, sampling fps tetap.
- TIDAK dicakup: rotasi kamera (quaternion), easing per segmen, rendering 3D, dan collision.

## Required Tools
- Python 3.9+ standard library. `scripts/camera_path.py`

## Input dan Output Specification
Input: keyframes [{t, pos:[x,y,z]}] dengan t naik, fps. Output: daftar {t, pos} per frame.

## Execution Workflow
1. Tetapkan keyframe posisi dari storyboard. 2. Sample jalur. 3. Kirim posisi ke scene 3D per frame. 4. Periksa visual di renderer sebelum rilis.

## Decision Rules
- Keyframe terlalu rapat menimbulkan overshoot; tambah jarak waktu atau kurangi keyframe.
- Kualitas visual tetap perlu tinjauan manusia (artistic QC).

## Error Handling
- Kurang dari dua keyframe atau waktu tidak naik: ValueError.

## Quality Control
- Posisi tepat sama dengan keyframe; kontinuitas turunan di keyframe.

## Acceptance Criteria
- Empat keyframe dengan fps 60 menghasilkan 181 frame; posisi pada t=1 tepat [1,0,0]; kontinuitas C1 dalam 1e-3.

## Contoh Implementasi
```python
from camera_path import sample
frames = sample([{'t':0,'pos':[0,0,0]},{'t':1,'pos':[1,0,0]}], fps=60)
```

## Test Cases
`tests/skills/test_v07_batch2.py` (CameraTests).

## Referensi dan Sumber
- Catmull-Rom spline (formula standar), diimplementasikan ulang.

## Informasi Lisensi
- Skill: MIT. Lihat juga threejs-camera dan remotion-motion-graphics (upstream) untuk pemakaian scene.
