"""Rencana narasi ElevenLabs: pecah naskah, estimasi karakter, dan cek kuota gratis SEBELUM generasi.

Bukti yang dipakai untuk estimasi: pada estimate_only ElevenLabs, teks "これはテストです。" (9 karakter)
dengan 2 generasi dihargai 18 kredit, sehingga 1 kredit per karakter per generasi (model eleven_v4).
Skill ini TIDAK memanggil API. Generasi dilakukan lewat tool MCP hanya setelah rencana ini diperiksa.
Usage: python narration_plan.py naskah.txt --used 297 --limit 10000 --generations 1
"""
from __future__ import annotations

import argparse
import json
import re
import sys

SENTENCE_RE = re.compile(r"(?<=[。！？!?\.])\s*")


def split_segments(text: str) -> list[str]:
    out = []
    for para in re.split(r"\n\s*\n", text.strip()):
        para = " ".join(para.split())
        if not para:
            continue
        out.extend(s for s in SENTENCE_RE.split(para) if s.strip())
    return out


def plan(text: str, used: int, limit: int, generations: int = 1, chars_per_s: float = 6.0) -> dict:
    if limit <= 0 or used < 0 or used > limit:
        raise ValueError("kuota tidak valid")
    if generations < 1:
        raise ValueError("generasi minimal 1")
    segs = split_segments(text)
    chars = [len(re.sub(r"\s", "", s)) for s in segs]
    credits = sum(chars) * generations
    remaining = limit - used
    status = "OK" if credits <= remaining else "ERROR_KUOTA_TIDAK_CUKUP"
    return {"segments": [{"index": i, "text": s, "chars": c, "est_seconds": round(c / chars_per_s, 2)}
                         for i, (s, c) in enumerate(zip(segs, chars), start=1)],
            "total_chars": sum(chars), "credits_estimate": credits, "remaining_quota": remaining,
            "status": status, "note": "Estimasi kredit 1/karakter/generasi (bukti: estimate_only). Kecepatan bicara adalah asumsi."}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("txt")
    ap.add_argument("--used", type=int, required=True)
    ap.add_argument("--limit", type=int, required=True)
    ap.add_argument("--generations", type=int, default=1)
    a = ap.parse_args()
    try:
        with open(a.txt, encoding="utf-8") as fh:
            res = plan(fh.read(), a.used, a.limit, a.generations)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
    print(json.dumps(res, indent=2, ensure_ascii=False))
    sys.exit(0 if res["status"] == "OK" else 1)
