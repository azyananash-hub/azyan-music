"""Bangun SKILL_REGISTRY.json dari seluruh skill di skills/.

Usage:
  python scripts/build_registry.py            # tulis SKILL_REGISTRY.json
  python scripts/build_registry.py --check    # gagal (exit 1) bila registry tidak sinkron

Registry berisi metadata + sha256 SKILL.md agar perubahan tanpa rebuild terdeteksi.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys

from zy_lib import LIBRARY_ROOT, discover_skills, file_sha256, script_references, validate_skill

REGISTRY_PATH = os.path.join(LIBRARY_ROOT, "SKILL_REGISTRY.json")
REGISTRY_VERSION = 1


def build_entries() -> list[dict]:
    entries = []
    for doc in discover_skills():
        validate_skill(doc)
        rel = os.path.relpath(doc.path, LIBRARY_ROOT).replace(os.sep, "/")
        entries.append({
            "name": doc.name or doc.folder,
            "category": doc.category,
            "path": rel,
            "description": doc.description,
            "license": doc.frontmatter.get("license", ""),
            "status": "validated" if not doc.errors else "invalid",
            "scripts": script_references(doc.body),
            "sha256_skill_md": file_sha256(doc.path),
            "errors": doc.errors,
        })
    entries.sort(key=lambda e: (e["category"], e["name"]))
    return entries


def build_registry() -> dict:
    skills = build_entries()
    return {
        "registry_version": REGISTRY_VERSION,
        "library": "ZY Skill Library",
        "generated_by": "scripts/build_registry.py",
        "skill_count": len(skills),
        "skills": skills,
    }


def _render(reg: dict) -> str:
    return json.dumps(reg, indent=2, ensure_ascii=False) + "\n"


def _main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--check", action="store_true", help="Bandingkan dengan registry di disk tanpa menulis")
    args = p.parse_args(argv)

    reg = build_registry()
    text = _render(reg)
    if args.check:
        if not os.path.isfile(REGISTRY_PATH):
            print("ERROR: SKILL_REGISTRY.json belum ada", file=sys.stderr)
            return 1
        with open(REGISTRY_PATH, encoding="utf-8") as fh:
            current = fh.read()
        if current != text:
            print("ERROR: SKILL_REGISTRY.json tidak sinkron; jalankan: python scripts/build_registry.py",
                  file=sys.stderr)
            return 1
        print(f"OK: registry sinkron ({reg['skill_count']} skill)")
        return 0
    with open(REGISTRY_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print(f"Registry ditulis: {REGISTRY_PATH} ({reg['skill_count']} skill)")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
