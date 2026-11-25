---
name: short-circuit-calculator
description: Estimate symmetrical three-phase short-circuit current (Ik and peak ip) at a bus from utility short-circuit MVA and transformer impedance percent, using IEC 60909-style simplified formulas. Use for electrical power system pre-checks and student/engineering analysis of fault levels.
license: original-zy
compatibility: Python 3.9+ standard library only
metadata: {"category": "engineering", "status": "verified", "owner": "zy"}
---

# Short-Circuit Calculator (3-phase symmetrical, simplified)

## Activation Triggers
- User meminta "arus hubung singkat", "short circuit current", "Ik''", "fault level", "ip peak", atau "kA bus".
- User memberi data MVA sumber/utility, tegangan bus, atau Z% transformator dan ingin tahu kemampuan interrupting breaker.
- Task pre-check desain panel atau pemilihan kapasitas pemutus (circuit breaker rating).

## Scope dan Batas Kemampuan
- Dicakup: gangguan 3 fasa simetris pada satu bus; sumber sebagai impedansi ekivalen dari MVA hubung singkat; satu transformator opsional; faktor kappa IEC 60909 untuk arus puncak.
- TIDAK dicakup: gangguan tak-simetris (1 fasa ke tanah, fasa-fasa), impedansi urutan nol, kontribusi motor induksi/sinkron, kabel detail (R/X per km), tap changer, sistem multi-sumber, dan koordinasi proteksi.
- Output adalah estimasi untuk analisis dan pre-check. Keputusan desain atau operasi wajib diverifikasi oleh engineer berkompetensi dan studi lengkap (mis. pandapower, MIT/BSD-3 lihat referensi).

## Required Tools
- Python 3.9+ (standard library saja; tidak perlu pip install).
- `scripts/short_circuit.py` di folder skill ini.
- Opsional: pandapower untuk studi jaringan penuh.

## Input dan Output Specification
Input (satuan wajib):
| Parameter | Satuan | Keterangan |
|---|---|---|
| `--v-sec-kv` | kV (LL) | Tegangan bus yang dihitung |
| `--s-sc-mva` | MVA | Short-circuit capacity sumber (di sisi HV bila ada trafo) |
| `--v-hv-kv` | kV | Wajib bila ada trafo |
| `--trafo-mva` | MVA | Rating transformator |
| `--trafo-z-percent` | % | Impedansi transformator |
| `--xr-source`, `--xr-trafo` | - | Rasio X/R (default 10) |

Output: `ik_kA_rms` (Ik'' simetris), `ip_kA_peak`, `kappa`, `z_total_ohm`, `scope_note`. Format teks atau JSON (`--json`).

## Execution Workflow
1. Konfirmasi data: tegangan, MVA sumber, dan (jika ada) MVA dan Z% trafo dengan satuan yang benar.
2. Periksa apakah sumber dinyatakan di sisi HV. Jika ya, sertakan `--v-hv-kv`.
3. Jalankan: `python scripts/short_circuit.py --v-sec-kv 0.4 --s-sc-mva 250 --v-hv-kv 20 --trafo-mva 1 --trafo-z-percent 6 --json`
4. Bandingkan `ik_kA_rms` dengan kapasitas pemutus (kA interrupting) yang tersedia.
5. Laporkan hasil beserta asumsi dan batas cakupan (scope_note).

## Decision Rules
- Jika `--trafo-mva` diisi tanpa `--trafo-z-percent` (atau sebaliknya), script menolak input. Jangan mengisi Z% dari asumsi tanpa menandainya.
- Jika data sumber tidak diketahui, JANGAN mengarang MVA. Minta data dari PLN/utility atau pemilik sistem, atau tandai hasil sebagai "tidak dihitung".
- Jika kasus melibatkan motor besar, sumber generator, atau gangguan tak-simetris, nyatakan di luar cakupan dan sarankan studi lengkap.
- Gunakan kappa IEC 60909 hanya untuk estimasi puncak; jangan menyebutnya sebagai nilai pasti.

## Error Handling
- Nilai nol/negatif/NaN ditolak dengan pesan `ERROR:` dan exit code 2.
- Impedansi total nol ditolak (arus tak terhingga = input salah).
- Jika tegangan/MVA tidak sesuai konvensi (mis. MW vs MVA), hasil tidak valid; minta konfirmasi satuan.

## Quality Control
- Cek konsistensi: `ik_kA_rms` harus sama dengan `S_sc / (sqrt(3) * V)` bila tanpa trafo.
- Pastikan `kappa` berada di rentang 1.02 sampai 2.0.
- Pastikan unit test lulus (`python -m unittest discover -s tests` dari root library).

## Acceptance Criteria
- Tanpa trafo: `Ik` pada 11 kV dengan S_sc 100 MVA sama dengan 5.2486 kA (dihitung dari S/(sqrt3 V)).
- Kappa R/X=0 sama dengan 2.0; R/X sangat besar mendekati 1.02.
- Input invalid menghasilkan error yang jelas, bukan hasil diam-diam.
- Laporan selalu menyertakan scope_note dan asumsi.

## Contoh Implementasi
```bash
# Sumber 100 MVA pada 11 kV, tanpa trafo
python scripts/short_circuit.py --v-sec-kv 11 --s-sc-mva 100

# Sumber 500 MVA di sisi 20 kV, trafo 1 MVA Z=6% menurunkan ke 0.4 kV
python scripts/short_circuit.py --v-sec-kv 0.4 --s-sc-mva 500 --v-hv-kv 20 \
  --trafo-mva 1 --trafo-z-percent 6 --json
```

## Test Cases
Lihat `tests/test_short_circuit.py` di root library. Kasus utama:
1. Tanpa trafo, 11 kV / 100 MVA: Ik = 5.2486 kA (toleransi 1e-3).
2. Kappa(0) = 2.0; kappa(R/X besar) mendekati 1.02.
3. Trafo tanpa `v_hv_kv` ditolak.
4. Nilai negatif dan nol ditolak.

## Referensi dan Sumber
- IEC 60909-0:2016, Short-circuit currents in three-phase a.c. systems (standar; rumus kappa dirujuk dari standar ini, teks standar tidak disalin).
- Lihat `references/short-circuit-theory.md` untuk ringkasan asumsi dan rumus yang dipakai.
- Pembanding studi jaringan: pandapower (BSD-3-Clause, lihat `references/sources-and-licenses.md`).

## Informasi Lisensi
- Kode dan dokumentasi skill ini: `original-zy` (dibuat untuk ZY Skill Library).
- Standar IEC 60909 adalah dokumen berhak cipta IEC; skill hanya merujuk rumusnya, bukan menyalin teksnya.
