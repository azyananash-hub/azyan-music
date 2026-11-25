---
name: multi-agent-orchestration
description: Plan work for multiple AI agents: validate task dependencies, reject cycles and missing dependencies, and schedule tasks into parallel waves so that no two tasks in a wave write the same file. Use before dispatching several agents to avoid dependency and write conflicts.
license: MIT
compatibility: Python 3.9+ standard library only
metadata: {"category": "software-development", "status": "verified", "owner": "zy"}
---

# multi-agent-orchestration

## Activation Triggers
- User meminta "agen paralel", "orkestrasi multi-agent", "dependensi tugas", atau "rencana kerja beberapa agen".

## Scope dan Batas Kemampuan
- Dicakup: validasi DAG dependensi, deteksi siklus, dan penjadwalan gelombang dengan larangan tulis file yang sama dalam satu gelombang.
- TIDAK dicakup: menjalankan agen, memantau hasil, dan merge kode.

## Required Tools
- Python 3.9+ standard library. `scripts/task_graph.py`

## Input dan Output Specification
Input: JSON tasks (id, deps, writes). Output JSON: waves (daftar id per gelombang) atau ValueError untuk siklus/dependensi hilang.

## Execution Workflow
1. Pecah pekerjaan menjadi tugas dengan file tulis yang jelas. 2. Jalankan plan. 3. Dispatch gelombang satu per satu; tunggu gelombang selesai sebelum berikutnya.

## Decision Rules
- Tugas yang menulis file bersama selalu diserialisasi.
- Jika file tulis tidak diketahui, kosongkan writes hanya bila tugas benar-benar read-only.

## Error Handling
- Siklus, dependensi hilang, atau id duplikat: ValueError.

## Quality Control
- Tugas tanpa dependensi dan tanpa konflik boleh satu gelombang.

## Acceptance Criteria
- Rantai tiga tugas menghasilkan tiga gelombang; dua tugas independen dengan file berbeda satu gelombang; konflik tulis diserialisasi; siklus ditolak.

## Contoh Implementasi
```bash
python scripts/task_graph.py plan.json
```

## Test Cases
`tests/skills/test_v07_batch1.py` (MultiAgentTests).

## Referensi dan Sumber
- Algoritma pengurutan topologis (Kahn) dan pemeriksaan konflik tulis: rancangan internal.

## Informasi Lisensi
- Skill: MIT.
