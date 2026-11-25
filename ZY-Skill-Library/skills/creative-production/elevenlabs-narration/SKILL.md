---
name: elevenlabs-narration
description: Plan an ElevenLabs narration from a script: split into segments, estimate characters and credits (one credit per character per generation), check the free monthly quota before any generation, and hand a checked plan to the ElevenLabs tools. Use when producing narration with ElevenLabs without buying credits.
license: MIT
compatibility: Python 3.9+ standard library only; ElevenLabs MCP tools (free tier quota)
metadata: {"category": "creative-production", "status": "validated", "owner": "zy", "classification": "CUSTOM"}
---

# elevenlabs-narration

## Activation Triggers
- User meminta "narasi ElevenLabs", "voice over dari naskah", atau "estimasi kredit narasi".

## Scope dan Batas Kemampuan
- Dicakup: pemecahan naskah, estimasi karakter dan kredit, pengecekan kuota gratis, dan rencana generasi.
- TIDAK dicakup: pemanggilan API langsung dari skill, pembelian kredit, kloning suara, dan evaluasi kualitas suara.
- Status: planner tervalidasi offline; generasi live belum diuji (layanan sibuk pada sesi uji).

## Required Tools
- Python 3.9+ standard library. `scripts/narration_plan.py`. ElevenLabs MCP tools (creative_list_voices, creative_generate_speech dengan estimate_only).

## Input dan Output Specification
Input: txt naskah, --used dan --limit kuota. Output JSON: segments (text, chars, est_seconds), credits_estimate, remaining_quota, status OK atau ERROR_KUOTA_TIDAK_CUKUP.

## Execution Workflow
1. Jalankan planner untuk memeriksa kuota. 2. Pilih voice dari creative_list_voices. 3. Jalankan estimate_only pada satu segmen. 4. Setelah disetujui, generate satu kali; jangan ulangi generasi yang gagal tanpa diagnosis.

## Decision Rules
- Status ERROR_KUOTA: berhenti dan beri tahu pengguna; jangan membeli kredit.
- Hanya gunakan voice_id dari daftar tool, bukan dari ingatan.

## Error Handling
- Layanan sibuk atau generasi gagal: catat, jangan ulangi dalam giliran yang sama; kredit tidak ditagih saat gagal (sesuai pesan tool).

## Quality Control
- Estimasi kredit harus sama dengan karakter x generasi; dicek terhadap estimate_only.

## Acceptance Criteria
- Teks 9 karakter dengan 2 generasi = 18 kredit (sama dengan estimate_only ElevenLabs); kuota habis ditolak.

## Contoh Implementasi
```bash
python scripts/narration_plan.py naskah.txt --used 297 --limit 10000 --generations 1
```

## Test Cases
`tests/skills/test_v07_batch2.py` (NarrationTests). Generasi live: NOT TESTED (layanan sibuk).

## Referensi dan Sumber
- Tarif kredit: bukti dari estimate_only pada sesi ini (18 kredit untuk 9 karakter x 2 generasi). Kuota gratis: 10.000 karakter per bulan (account_get_usage).

## Informasi Lisensi
- Skill: MIT. Layanan ElevenLabs tunduk pada ketentuannya sendiri.
