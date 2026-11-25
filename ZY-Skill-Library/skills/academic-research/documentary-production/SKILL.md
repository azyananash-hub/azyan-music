---
name: documentary-production
description: Keep a documentary claim ledger: every narrated claim must reference a source, every source must be complete, claims marked verified need a primary source, and unused sources are flagged. Use when writing or auditing the narration of a documentary or factual video.
license: MIT
compatibility: Python 3.9+ standard library only
metadata: {"category": "academic-research", "status": "verified", "owner": "zy", "classification": "CUSTOM"}
---

# documentary-production

## Activation Triggers
- User meminta "naskah dokumenter", "sumber klaim", "fact check narasi", atau "daftar sumber video".

## Scope dan Batas Kemampuan
- Dicakup: audit keterhubungan klaim dan sumber dalam JSON, serta kelengkapan kutipan.
- TIDAK dicakup: mengambil sumber dari web, menilai kebenaran isi sumber, dan keputusan editorial.

## Required Tools
- Python 3.9+ standard library. `scripts/claim_ledger.py`

## Input dan Output Specification
Input JSON: sources (id, title, type primary|secondary, citation, url, license) dan claims (id, text, source_ids, status). Output JSON: errors, warnings, status.

## Execution Workflow
1. Catat setiap klaim naratif sebelum merekam. 2. Hubungkan ke sumber. 3. Verifikasi sumber primer secara manual. 4. Jalankan audit sebelum produksi.

## Decision Rules
- Klaim tanpa sumber tidak boleh direkam.
- Status verified hanya setelah sumber dibaca sendiri, bukan dari ringkasan.

## Error Handling
- Sumber tak dikenal atau klaim kosong: error. Berkas rusak: exit 2.

## Quality Control
- Tidak ada error; warning ditinjau sebelum rilis.

## Acceptance Criteria
- Ledger lengkap lulus; klaim tanpa sumber dan sumber tak dikenal ditolak; verified tanpa primer diperingatkan.

## Contoh Implementasi
```bash
python scripts/claim_ledger.py ledger.json
```

## Test Cases
`tests/skills/test_v07_batch2.py` (DocumentaryTests).

## Referensi dan Sumber
- Metode buku klaim: rancangan internal. Lihat juga citation-verification (library) untuk verifikasi referensi akademik.

## Informasi Lisensi
- Skill: MIT.
