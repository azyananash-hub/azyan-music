---
name: manhwa-production
description: Check manhwa page layout: panels inside margins, no overlaps, minimum panel size, and reading order computed right-to-left for Japanese manga or left-to-right otherwise. Use when laying out comic pages before lettering or export.
license: MIT
compatibility: Python 3.9+ standard library only
metadata: {"category": "creative-production", "status": "verified", "owner": "zy"}
---

# manhwa-production

## Activation Triggers
- User meminta "panel manhwa", "layout halaman komik", "urutan baca kanan ke kiri", atau "tata letak panel".

## Scope dan Batas Kemampuan
- Dicakup: geometri panel pada satu halaman, margin, tumpang tindih, dan urutan baca berbasis baris.
- TIDAK dicakup: penggambaran, lettering, balon dialog, dan penilaian estetika layout.

## Required Tools
- Python 3.9+ standard library. `scripts/panel_check.py`

## Input dan Output Specification
Input: JSON page (width, height, margin, reading rtl|ltr) dan panels (id, x, y, w, h), opsional order. Output JSON: reading_order, issues, status.

## Execution Workflow
1. Tentukan ukuran halaman dan margin dari spesifikasi penerbit. 2. Tulis koordinat panel. 3. Jalankan check. 4. Bandingkan urutan baca dengan naskah.

## Decision Rules
- Urutan baca mengikuti baris lalu kanan-ke-kiri untuk rtl. Jika naskah berbeda, perbaiki layout, bukan urutan.
- Batas minimum 80 px adalah parameter praktis, bukan standar cetak.

## Error Handling
- Reading bukan rtl/ltr: issue dan exit 1. Berkas rusak: exit 2.

## Quality Control
- Tidak ada panel yang melewati margin atau saling tumpang tindih.

## Acceptance Criteria
- Tiga panel dengan dua di baris atas menghasilkan urutan kanan-ke-kiri yang benar; tumpang tindih dan margin terdeteksi.

## Contoh Implementasi
```bash
python scripts/panel_check.py page.json
```

## Test Cases
`tests/skills/test_v07_batch1.py` (PanelTests).

## Referensi dan Sumber
- Konvensi baca manga kanan-ke-kiri (praktik umum), diimplementasikan ulang.

## Informasi Lisensi
- Skill: MIT.
