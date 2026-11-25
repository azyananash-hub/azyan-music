---
name: prd-engineering
description: Turn a product requirements draft into a checked spec: lint for leftover template placeholders, required sections, prioritized user stories, measurable success criteria, and FR requirement IDs, then emit one handoff task per requirement for AI coding agents. Use when preparing a PRD before implementation.
license: MIT
compatibility: Python 3.9+ standard library only
metadata: {"category": "governance", "status": "verified", "owner": "zy", "classification": "ADAPTED"}
---

# prd-engineering

## Activation Triggers
- User meminta "PRD", "spesifikasi", "kriteria penerimaan", atau "siapkan handoff ke AI coding".

## Scope dan Batas Kemampuan
- Dicakup: lint spesifikasi berbasis template spec-kit, ID FR-###, dan daftar tugas handoff.
- TIDAK dicakup: menulis isi produk, validasi kebutuhan bisnis, dan desain arsitektur.

## Required Tools
- Python 3.9+ standard library. `scripts/prd_lint.py`. Template: `references/spec-kit/` (MIT, GitHub spec-kit).

## Input dan Output Specification
Input: spec.md. Output: issues, requirement_ids, status; opsional --handoff berkas JSON berisi tugas per FR dan TEST-FR-###.

## Execution Workflow
1. Mulai dari references/spec-kit/spec-template.md. 2. Isi semua placeholder. 3. Jalankan lint. 4. Buat handoff dan serahkan per tugas ke agen dengan tes yang sesuai.

## Decision Rules
- Placeholder tersisa berarti spesifikasi belum siap; jangan dikirim ke agen.
- Kriteria tanpa angka atau satuan ditolak sebagai tidak terukur.

## Error Handling
- Berkas tidak ada: exit 2.

## Quality Control
- Setiap FR punya tes yang dapat dijalankan sebelum implementasi dianggap selesai.

## Acceptance Criteria
- Template mentah gagal dengan isi placeholder; spesifikasi terisi dengan satu FR dan satu SC terukur lulus.

## Contoh Implementasi
```bash
python scripts/prd_lint.py spec.md --handoff handoff.json
```

## Test Cases
`tests/skills/test_v07_batch2.py` (PrdTests).

## Referensi dan Sumber
- Template: github/spec-kit (MIT), lihat references/spec-kit/SOURCE.md. Skill ini (SKILL.md dan prd_lint.py) ditulis ulang, bukan salinan.
- Tumpang tindih dengan writing-plans (obra): writing-plans menyusun rencana eksekusi, prd-engineering menyusun spesifikasi kebutuhan.

## Informasi Lisensi
- Skill dan script: MIT. Template spec-kit: MIT (references/spec-kit/LICENSE).
