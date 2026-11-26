# BLENDER-SKILLS-COMPARISON: item 39 (39a dan 39b)

Status: BLOCKED. Kanonik belum dipilih pemilik. Pembacaan statis dan hanya-baca. Tidak ada instalasi Blender dan tidak ada skrip yang dijalankan.

## 1. Identitas

| Aspek | 39a: EL4CTEO/blender-skills | 39b: arjun988/blender-skills |
|---|---|---|
| Commit HEAD (12 karakter) | 1a1cc6c49312 | 904f095d8f36 |
| Tanggal commit HEAD | 2026-11-21 (subjek: "Release 1.3.3") | 2026-11-06 (subjek: Star History di README) |
| Identitas repositori | Terverifikasi (`ls-remote` = HEAD klon) | Terverifikasi (`ls-remote` = HEAD klon) |
| Kanonik | Belum dipilih | Belum dipilih |

Kedua repositori memiliki nama yang sama. Mana yang dimaksud pemilik belum diketahui.

## 2. Lisensi

Keduanya MIT (LICENSE: "MIT License"). Lisensi permisif, sehingga adaptasi dapat dilakukan dengan atribusi.

## 3. Pemeliharaan

Ini berasal dari dokumen dan commit HEAD. Riwayat penuh tidak diukur karena klon dangkal.

- 39a: `CHANGELOG.md` ada, versi rilis 1.3.3 (dari subjek commit), README menyebut 28 skill, folder `tests/` ada.
- 39b: `CHANGELOG.md`, `CONTRIBUTING.md`, `ROADMAP.md`, dan `version.json` (1.3.0 menurut badge README). README mengklaim 94 skill, tetapi ada 188 berkas SKILL.md. Penyebab selisih ini belum ditelusuri.

## 4. Keamanan dan jalur runtime

- 39a: `skills/blender-core/scripts/run_in_blender.py` menjalankan Blender dalam mode headless melalui `subprocess` (baris 18 dan 76) untuk menjalankan skrip skill dan mencetak hasil JSON. Ini adalah jalur eksekusi kode repositori di dalam Blender. Jika ada adaptasi, runner ini tidak ikut. `tests/test_core.py:20` menjalankan `exec(compile(...))` pada blok kode dari SKILL.md selama pengujian. `tests/test_video.py:132` menjalankan Blender lewat subprocess. Tidak ada `.mcp.json` di root.
- 39b: `.mcp.json` dan `.cursor/mcp.json` memanggil `cmd /c uvx --python 3.11 blender-mcp` tanpa versi terkunci. Env yang diset: `BLENDER_HOST=localhost`, `BLENDER_PORT=9876`, `DISABLE_TELEMETRY=true`. Paket `blender-mcp` ini adalah jalur MCP yang sama dengan item 38. Item 38 ditolak karena `execute_code` menjalankan Python secara default (lihat `evidence/deep-audit-2026-11-26.md`). Jadi 39b bergantung pada runtime yang sudah ditolak.

## 5. Isi skill

- 39a: 28 folder `skills/blender-*`. Topiknya mencakup texture-baking, addon-development, game-optimization, stylized-npr, scene-setup, animation, character-rigging, hair-grooming, simulation, rendering, asset-qa, retopology-uv, video-editing, clothing, time-of-day, facial-shapekeys, texturing, geometry-nodes, pbr-materials, workflow-recipes, export-pipelines, environment-kits, sculpting, core, hardsurface-modeling, weather-fx, pipeline-automation, dan lighting-lookdev.
  - Contoh: `blender-asset-qa/SKILL.md` (5.185 byte, MIT, metadata versi 1.2.0). Isinya adalah prosedur "review gate" untuk mesh, dengan pemeriksaan berbasis angka sebelum pemeriksaan visual. Format prosedural ini sesuai dengan kebutuhan QA aset.
- 39b: skill berbasis gaya dan genre, misalnya `horror-style`, `noir-style`, `cozy-wholesome-mood`, `genre-racing-sports`, `cloth-sim`, `lod-pipeline`, `export-pipeline`, dan `unity-export`. Banyak skill berupa preferensi gaya, bukan pipeline. Isi per skill belum ditinjau.

## 6. Tumpang tindih dengan library

- Registry tidak memiliki skill Blender. Tidak ada tumpang tindih nama.
- Terkait tetapi tidak menggantikan: `threejs-*` (runtime 3D web), `motion-graphics`, dan `creative-production`. Blender adalah alat pembuatan konten. Three.js adalah runtime web.

## 7. Kesesuaian hardware (GTX 1650 4 GB, RAM 16 GB, i5-10300H)

Ini estimasi dan tidak diukur.

- Scene berat (simulasi, cloth, hair, dan render Cycles) akan dibatasi VRAM 4 GB. EEVEE dan viewport relatif ringan.
- Skill 39a yang berkaitan dengan simulation, hair, dan cloth paling berat untuk mesin ini.
- Blender belum terpasang di container maupun di mesin pemilik. Status di mesin pemilik tidak diverifikasi.

## 8. Relevansi

- Engineering: rendah secara langsung, kecuali visualisasi aset atau produk.
- Creative production: 39a relevan untuk realistic 3D environments, editable source assets, dan asset-level QA. 39b relevan untuk konsistensi gaya, tetapi isinya lebih banyak preferensi estetika.

## 9. Rekomendasi

Rekomendasi: SATU, secara selektif, yaitu 39a (EL4CTEO), dalam bentuk content-only. 39b tidak direkomendasikan saat ini, karena runtime MCP-nya tidak dapat dipisahkan tanpa modifikasi, dan selisih jumlah skill-nya belum dijelaskan.

Syarat sebelum adaptasi apa pun:
1. Pemilik mengonfirmasi bahwa 39a adalah repositori yang dimaksud. Item 39 tetap BLOCKED sampai itu.
2. Runner `run_in_blender.py` dan folder `tests/` tidak diadaptasi.
3. Maksimal tiga skill. Kandidat: `blender-asset-qa`, `blender-export-pipelines`, dan `blender-environment-kits`. Pilihan final ada di tangan pemilik. Setiap adaptasi ditulis ulang dalam format CUSTOM, dengan ADAPTATION.md dan atribusi MIT.
4. Persetujuan dicatat sebagai usulan baru BL-1. Ini bukan bagian P01–P17.
5. Blender tidak dipasang tanpa persetujuan. Benchmark dijalankan pada mesin pemilik.

Opsi lain yang valid: TIDAK ADA. Pilih ini jika pemilik belum memerlukan 3D untuk saat ini. Realistic 3D tetap DEFER.
