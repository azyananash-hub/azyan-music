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


# Glosarium kecil Indonesia -> Inggris untuk kosakata produksi dan teknik. Deskripsi skill berbahasa Inggris.
GLOSSARY = {
    "kamera": "camera", "sinematik": "cinematic", "adegan": "scene", "naskah": "script", "narasi": "narration",
    "animasi": "animation", "gerak": "motion", "grafis": "graphics", "vertikal": "vertical", "suara": "audio",
    "gambar": "image", "halaman": "page", "komik": "manhwa", "panel": "panel", "bab": "chapter",
    "kosakata": "vocabulary", "kurikulum": "curriculum", "gangguan": "fault", "kelistrikan": "electrical",
    "gejala": "symptom", "keputusan": "decision", "tugas": "task", "agen": "agent", "sumber": "source",
    "klaim": "claim", "strategi": "strategy", "risiko": "risk", "dokumenter": "documentary", "naskah2": "script",
}


def tokens(text: str) -> set[str]:
    base = {t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS and len(t) > 1}
    return base | {GLOSSARY[t] for t in base if t in GLOSSARY}


NAME_BONUS = 2.0       # kata kunci yang menyebut nama skill langsung (mis. "ffmpeg") diutamakan
MIN_SCORE = 0.1        # di bawah ini dianggap tidak relevan; mencegah aktivasi skill yang salah


def _idf(registry: list[dict]) -> dict[str, float]:
    """Bobot kata = log(N / df): kata yang muncul di banyak skill (mis. "video") tidak spesifik."""
    df: dict[str, int] = {}
    for s in registry:
        for t in tokens(s["name"].replace("-", " ") + " " + s.get("description", "")):
            df[t] = df.get(t, 0) + 1
    n = len(registry)
    return {t: math.log(1 + n / c) for t, c in df.items()}


REFS = os.path.join(os.path.dirname(REGISTRY), "references")


def _load_json(name: str) -> dict:
    path = os.path.join(REFS, name)
    if not os.path.isfile(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


PREFERRED_BOOST = 1.25  # kelipatan skor untuk kategori yang disukai proyek


def context_notes(brief: str, skill_name: str, project: str | None,
                  constraints: dict, profiles: dict) -> list[str]:
    """Catatan konflik atau override antara brief dan batasan skill. Tidak mengubah isi upstream."""
    notes: list[str] = []
    rule = constraints.get(skill_name)
    if not rule:
        return notes
    btoks = {t for t in re.findall(r"[a-z0-9]+", brief.lower())}
    hits = sorted(btoks & set(rule.get("forbids", [])))
    if not hits:
        return notes
    proj = profiles.get(project or "", {})
    override = proj.get("overrides", {}).get(skill_name)
    if override:
        notes.append(f"OVERRIDE ({proj.get('name', project)}): brief memakai {', '.join(hits)}. {override}")
    else:
        notes.append(f"KONFLIK: brief memakai {', '.join(hits)}, tetapi skill ini melarangnya ({rule['source']}). "
                     "Tanyakan atau pakai profil proyek yang punya override.")
    return notes


def route_with_context(query: str, registry: list[dict], top: int = 3, min_score: float = MIN_SCORE,
                       project: str | None = None, brief: str | None = None) -> list[dict]:
    """Routing + konteks proyek + catatan konflik + ukuran konteks (tanpa membaca isi skill)."""
    profiles = _load_json("project-profiles.json")
    constraints = _load_json("skill-constraints.json")
    constraints = {k: v for k, v in constraints.items() if k != "note"}
    profiles = {k: v for k, v in profiles.items() if k != "note"}
    prefer = set(profiles.get(project or "", {}).get("preferred_categories", []))
    results = route(query, registry, top=len(registry), min_score=min_score)
    for r in results:
        if r["category"] in prefer:
            r["score"] = round(r["score"] * PREFERRED_BOOST, 4)
    results.sort(key=lambda x: x["score"], reverse=True)
    results = results[:top]
    text = brief if brief is not None else query
    lib = os.path.dirname(REGISTRY)
    for r in results:
        folder = os.path.join(lib, os.path.dirname(r["path"]))
        md = os.path.join(lib, r["path"])
        r["skill_md_bytes"] = os.path.getsize(md) if os.path.isfile(md) else None
        r["scripts"] = len(os.listdir(os.path.join(folder, "scripts"))) if os.path.isdir(os.path.join(folder, "scripts")) else 0
        r["references"] = len(os.listdir(os.path.join(folder, "references"))) if os.path.isdir(os.path.join(folder, "references")) else 0
        r["notes"] = context_notes(text, r["name"], project, constraints, profiles)
    return results


def route(query: str, registry: list[dict], top: int = 3, min_score: float = MIN_SCORE) -> list[dict]:
    q = tokens(query)
    if not q:
        raise ValueError("query kosong setelah stopword dibuang")
    idf = _idf(registry)
    scored = []
    for s in registry:
        fields = {
            "name": tokens(s["name"].replace("-", " ")),
            "category": tokens(s.get("category", "").replace("-", " ")),
            "description": tokens(s.get("description", "")),
        }
        size = sum(len(v) for v in fields.values()) or 1
        raw = sum(WEIGHTS[k] * idf.get(t, 1.0) for k, v in fields.items() for t in q if t in v)
        if q & fields["name"]:
            raw += NAME_BONUS * max(idf.get(t, 1.0) for t in q & fields["name"])
        score = raw / math.sqrt(size)
        if score > 0 and score >= min_score:
            scored.append({"name": s["name"], "category": s["category"], "score": round(score, 4),
                           "classification": s.get("classification"), "status": s.get("status"),
                           "path": s.get("path")})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top]


def _main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("query")
    p.add_argument("--top", type=int, default=3)
    p.add_argument("--project", default=None, help="id profil proyek, mis. earthstop")
    p.add_argument("--brief", default=None, help="teks brief untuk cek konflik (default: query)")
    a = p.parse_args(argv)
    with open(REGISTRY, encoding="utf-8") as fh:
        registry = json.load(fh)["skills"]
    try:
        results = route_with_context(a.query, registry, a.top, project=a.project, brief=a.brief)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if not results:
        print("Tidak ada skill yang cocok. Jelaskan tugas lebih spesifik.")
        return 1
    for r in results:
        print(f"{r['score']:>6}  {r['name']}  [{r['classification']}/{r['status']}]  {r['path']}"
              f"  (SKILL.md {r['skill_md_bytes']} B, scripts {r['scripts']}, references {r['references']})")
        for n in r["notes"]:
            print(f"        {n}")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
