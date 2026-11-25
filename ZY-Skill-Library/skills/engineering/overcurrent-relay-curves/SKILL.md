---
name: overcurrent-relay-curves
description: Compute inverse-time overcurrent relay operating times (IEC 60255 NI, VI, EI, LTI curve shapes) for protection coordination studies from TMS and I/Is multiple. Use for electrical protection screening, not final relay settings.
license: MIT
compatibility: Python 3.9+ standard library only
metadata: {"category": "engineering", "status": "verified", "owner": "zy"}
---

# overcurrent-relay-curves

## Activation Triggers
- User meminta "waktu operasi relai", "IEC inverse time", "TMS", "koordinasi proteksi arus lebih".

## Scope dan Batas Kemampuan
- Dicakup: kurva inverse-time standar (bentuk IEC 60255) untuk satu relai, perhitungan waktu operasi.
- TIDAK dicakup: koordinasi antar-relai, instantaneous element, kurva vendor, dan setting final.

## Required Tools
- Python 3.9+ (standard library). `scripts/relay_curve.py`

## Input dan Output Specification
Input: I/Is (>1), TMS (>0), kurva (NI/VI/EI/LTI). Output JSON: t_operate_s.

## Execution Workflow
1. Ambil Is dan TMS dari studi koordinasi. 2. Hitung waktu untuk setiap arus gangguan (I/Is). 3. Bandingkan dengan selang koordinasi yang disetujui.

## Decision Rules
- Konstanta (k, alpha) harus diverifikasi terhadap dokumen IEC 60255-151 sebelum dipakai untuk setting.
- Jangan menentukan TMS atau Is tanpa data beban dan hubung singkat.

## Error Handling
- I/Is <= 1, TMS <= 0, atau kurva tidak dikenal: ValueError, exit 2.

## Quality Control
- VI pada I/Is=10, TMS 1 harus 1.5 s; waktu harus turun saat I/Is naik.

## Acceptance Criteria
- Test `test_v05_custom.py` (RelayTests) lulus.

## Contoh Implementasi
```bash
python scripts/relay_curve.py --multiple 10 --tms 1 --curve VI
```

## Test Cases
`tests/skills/test_v05_custom.py` (RelayTests).

## Referensi dan Sumber
- Bentuk kurva IEC 60255-151 (konstanta belum diverifikasi terhadap sumber primer dalam sesi ini).

## Informasi Lisensi
- Skill: MIT.
