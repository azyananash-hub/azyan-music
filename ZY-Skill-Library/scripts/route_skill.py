"""Intelligent Skill Router ringan: pilih skill paling relevan dari SKILL_REGISTRY.json.

Metode: overlap kata (tanpa embedding, tanpa dependensi). Kata di nama skill bobot 3,
kategori bobot 2, deskripsi bobot 1. Stopword ID/EN dibuang. Skor dinormalisasi
dengan akar panjang token skill agar skill dengan deskripsi panjang tidak mendominasi.

Usage:
  python scripts/route_skill.py "hitung arus hubung singkat 11 kV" --top 3
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys

REGISTRY = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "SKILL_REGISTRY.json")
STOPWORDS = set("""a an and are as at be by for from in is it of on or that the this to with
dan atau yang untuk dengan dari ke di ini itu saya aku kita bisa tolong apa bagaimana cara
for how i me my you""".split())
WEIGHTS = {"name": 3.0, "category": 2.0, "description": 1.0}


def tokens(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS and len(t) > 1}


def route(query: str, registry: list[dict], top: int = 3) -> list[dict]:
    q = tokens(query)
    if not q:
        raise ValueError("query kosong setelah stopword dibuang")
    scored = []
    for s in registry:
        fields = {
            "name": tokens(s["name"].replace("-", " ")),
            "category": tokens(s.get("category", "").replace("-", " ")),
            "description": tokens(s.get("description", "")),
        }
        size = sum(len(v) for v in fields.values()) or 1
        raw = sum(WEIGHTS[k] for k, v in fields.items() for t in q if t in v)
        score = raw / math.sqrt(size)
        if score > 0:
            scored.append({"name": s["name"], "category": s["category"], "score": round(score, 4),
                           "classification": s.get("classification"), "status": s.get("status"),
                           "path": s.get("path")})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top]


def _main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("query")
    p.add_argument("--top", type=int, default=3)
    a = p.parse_args(argv)
    with open(REGISTRY, encoding="utf-8") as fh:
        registry = json.load(fh)["skills"]
    try:
        results = route(a.query, registry, a.top)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if not results:
        print("Tidak ada skill yang cocok. Jelaskan tugas lebih spesifik.")
        return 1
    for r in results:
        print(f"{r['score']:>6}  {r['name']}  [{r['classification']}/{r['status']}]  {r['path']}")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
