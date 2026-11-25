# MASTER PROTOCOL: ZY Skill Library

Protokol ini berlaku untuk seluruh skill. Setiap skill wajib mematuhinya.

## 1. Prinsip global
1. **Evidence over assumptions.** Angka dan klaim harus berasal dari data, perhitungan, atau sumber yang disebutkan.
2. **Execution over empty promises.** Skill harus punya mekanisme (workflow, script, atau checklist yang dapat dijalankan).
3. **Quality over quantity.** Lebih baik sedikit skill yang teruji daripada banyak skill tidak teruji.
4. **Modular architecture.** Satu skill, satu tanggung jawab. Dependensi antarskill dinyatakan eksplisit.
5. **Token efficiency.** Metadata ringkas; detail dipindahkan ke `references/`.
6. **Zero unnecessary dependencies.** Utamakan Python standard library.
7. **No fabricated results.** Dilarang mengarang data pasar, hasil uji, angka kontrak, atau repository.
8. **No silent failures.** Error harus keluar dengan kode non-nol dan pesan jelas.
9. **No destructive changes without authorization.** Hapus, timpa, atau rotasi kredensial membutuhkan konfirmasi.
10. **No paid API or subscription without approval.**
11. **No execution of untrusted third-party scripts before inspection.** Gunakan `third-party-skill-audit`.
12. **Respect open-source licenses.** Copyleft (GPL/AGPL) tidak disalin tanpa keputusan eksplisit. Lisensi tidak jelas dianggap tidak boleh disalin.
13. **Test before declaring completion.** Kata "selesai" hanya dipakai setelah test lulus.

## 2. Batasan domain
- **Industrial/listrik:** Simulasi dan perhitungan boleh. Instruksi pengoperasian peralatan berbahaya harus mengikuti SOP, batas keselamatan, dan otorisasi personel. Skill tidak menggantikan engineer berkompetensi.
- **Keuangan/trading:** Dilarang mengarang data pasar dan dilarang menjanjikan keuntungan. Statistik adalah deskriptif dari data yang diberikan.
- **Keamanan:** Secret tidak pernah ditampilkan utuh. Rotasi adalah langkah wajib bila secret pernah terekspos.
- **Edukasi:** Materi harus akurat; sumber dicantumkan.

## 3. Struktur skill wajib
Lihat `skills/governance/skill-engineering-standard/SKILL.md` dan `templates/SKILL_TEMPLATE.md`. Ringkasnya: frontmatter (`name`, `description`, `license`), dan 13 section wajib, dengan script dan test bila skill memiliki komputasi.

## 4. Alur kerja pengembangan
1. Inspeksi environment dan repository.
2. Riset dan audit lisensi/keamanan sumber luar; catat di `research/`.
3. Rancang struktur dan kontrak (input/output) skill.
4. Implementasi script dan SKILL.md.
5. Tulis test dan jalankan.
6. Jalankan `scripts/validate_library.py` dan `scripts/build_registry.py`.
7. Perbarui `CHANGELOG.md` dan `research/PROGRESS.md`.
8. Audit kualitas akhir; catat di `reports/`.

## 5. Persistensi progres
Setiap tahap selesai dicatat di `research/PROGRESS.md` agar pekerjaan bisa dilanjutkan dalam sesi lain.

## 6. Definition of Done (library)
- Struktur library ada dan konsisten.
- Skill tersedia sebagai file nyata dan lolos validasi.
- Sumber dan lisensi terdokumentasi (dan keterbatasan verifikasinya dinyatakan).
- Registry sinkron.
- Test lulus.
- Panduan penggunaan dan keterbatasan terdokumentasi.
