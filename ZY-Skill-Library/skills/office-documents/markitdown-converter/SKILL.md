---
name: markitdown-converter
description: Convert office documents (docx, pptx, xlsx, pdf, html) to Markdown text with markitdown for reading, summarizing, or feeding content into other skills. Use when a document must be read as plain text.
license: MIT
compatibility: Python 3.9+; markitdown[docx] (MIT, diuji 0.1.9)
metadata: {"category": "office-documents", "status": "verified", "owner": "zy"}
---

# markitdown-converter

## Activation Triggers
- User memberi file docx/pptx/xlsx/pdf dan ingin isinya sebagai teks atau Markdown.

## Scope dan Batas Kemampuan
- Dicakup: ekstraksi teks dan struktur dasar ke Markdown.
- TIDAK dicakup: hasil layout presisi, OCR gambar, dan validasi format dokumen (gunakan skill docx/pdf upstream).

## Required Tools
- Python 3.9+, `markitdown[docx]` (MIT).
- `scripts/to_markdown.py`

## Input dan Output Specification
Input: path file. Output: teks Markdown ke stdout atau file (argumen kedua).

## Execution Workflow
1. Jalankan `python scripts/to_markdown.py laporan.docx laporan.md`. 2. Periksa heading dan tabel penting.

## Decision Rules
- Dokumen dengan gambar penting: periksa manual karena gambar tidak diekstrak.
- File terenkripsi tidak didukung.

## Error Handling
- Format tidak didukung atau file rusak: pesan error dan exit 2.

## Quality Control
- Heading dan paragraf utama harus muncul di output.

## Acceptance Criteria
- Test MarkitdownTests lulus: heading dan paragraf docx terbaca.

## Contoh Implementasi
```bash
python scripts/to_markdown.py laporan.docx laporan.md
```

## Test Cases
`tests/skills/test_new_skills.py` (MarkitdownTests).

## Referensi dan Sumber
- markitdown: https://github.com/microsoft/markitdown (MIT; diverifikasi dari metadata PyPI).

## Informasi Lisensi
- Skill: MIT. Dependensi markitdown: MIT.
