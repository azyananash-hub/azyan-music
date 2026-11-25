# Progres ZY Skill Library

Terakhir diperbarui: 2026-11-25 (v0.2.0). Sumber kebenaran angka: `SKILL_REGISTRY.json` dan `research/import-manifest.json`.

## Hasil saat ini
- 46 skill di disk, 0 error validasi (`python scripts/validate_library.py`).
- 86 test lulus (`python -m unittest discover -s tests -t tests` dari venv `tests/requirements-test.txt`).

| Klasifikasi | Status | Jumlah |
|---|---|---|
| CUSTOM | VERIFIED | 15 |
| IMPORTED | VERIFIED (diuji dengan tugas nyata) | 6 (pdf, docx, xlsx, pptx, skill-creator, slack-gif-creator) |
| ADAPTED | VERIFIED | 1 (webapp-testing: perbaikan cleanup proses) |
| IMPORTED | belum diuji (instruksi saja) | 24 |
| BLOCKED | tidak diimpor | 1 (doc-coauthoring: tanpa lisensi) |

Target awal 50 skill teruji belum tercapai: 22 skill teruji. Tidak ada skill kosong yang ditambahkan untuk mengejar jumlah.

## Fase
| Fase | Status |
|---|---|
| Riset dan pengambilan sumber (2 repository, clone read-only) | Selesai untuk anthropics/skills dan obra/superpowers |
| Impor dengan provenance (`scripts/import_upstream.py`) | Selesai |
| Inspeksi keamanan script sebelum dijalankan (`third-party-skill-audit`) | Selesai; temuan false positive di dokumentasi |
| Uji fungsional skill impor | Selesai untuk 7 skill; 24 belum |
| Skill custom baru (load flow, Modbus, cooling tower, boiler, RO, tabungan) | Selesai, diuji |
| Adaptasi | Satu (webapp-testing). Lainnya belum |
| Deduplikasi | Belum. Lihat `reports/quality-audit.md` bagian duplikasi |
| Konfigurasi discovery Claude Code | Installer tersedia; belum diverifikasi di sesi Claude Code nyata |
| Konfigurasi discovery Codex | BELUM TERVERIFIKASI. Dokumentasi resmi tidak bisa diakses (DNS) |

## Backlog prioritas
1. Uji fungsional untuk skill instruksi (obra process skills, frontend-design, dll.) dengan tugas nyata.
2. Deduplikasi folder `scripts/office/` (identik di docx, pptx, xlsx) dengan mekanisme shared yang tetap kompatibel saat instalasi.
3. Verifikasi lokasi discovery Codex dari dokumentasi resmi OpenAI.
4. Migrasi datastore pymodbus ke SimDevice (deprecation).
5. PowerMCP (Power-Agent): BLOCKED sampai ada lisensi/akses ke PowerWorld/PSSE yang sah untuk pengujian.

## Keputusan utama
- 2026-11-25: Impor disalin utuh dengan SOURCE.md; adaptasi hanya lewat folder ADAPTATION.md.
- 2026-11-25: Test memakai venv `tests/requirements-test.txt`, bukan Python sistem.
- 2026-11-25: Skill impor tidak wajib 13 section ZY; validasinya minimal (name, description, lisensi).
