"""Validasi seluruh library: standar SKILL.md, script yang direferensikan, dan sinkronisasi registry.

Usage:
  python scripts/validate_library.py

Exit code: 0 semua valid, 1 ada error. Warning tidak menggagalkan build.
"""

from __future__ import annotations

import os
import sys

from zy_lib import LIBRARY_ROOT, discover_skills, validate_skill

REQUIRED_ROOT_FILES = (
    "AGENTS.md", "CLAUDE.md", "README.md", "MASTER_PROTOCOL.md",
    "SKILL_REGISTRY.json", "CHANGELOG.md",
)


def run() -> tuple[int, list[str]]:
    messages: list[str] = []
    error_count = 0

    for name in REQUIRED_ROOT_FILES:
        if not os.path.isfile(os.path.join(LIBRARY_ROOT, name)):
            messages.append(f"ERROR root: file wajib hilang: {name}")
            error_count += 1

    docs = discover_skills()
    if not docs:
        messages.append("WARNING: tidak ada skill ditemukan di skills/")
    for doc in docs:
        validate_skill(doc)
        rel = os.path.relpath(doc.path, LIBRARY_ROOT)
        for e in doc.errors:
            messages.append(f"ERROR {rel}: {e}")
            error_count += 1
        for w in doc.warnings:
            messages.append(f"WARNING {rel}: {w}")

    # Registry harus sinkron dengan isi skill saat ini.
    from build_registry import REGISTRY_PATH, _render, build_registry  # import lokal agar tidak circular
    expected = _render(build_registry())
    if os.path.isfile(REGISTRY_PATH):
        with open(REGISTRY_PATH, encoding="utf-8") as fh:
            if fh.read() != expected:
                messages.append("ERROR SKILL_REGISTRY.json tidak sinkron; jalankan scripts/build_registry.py")
                error_count += 1

    messages.append(f"Ringkasan: {len(docs)} skill diperiksa, {error_count} error")
    return error_count, messages


def _main() -> int:
    errors, messages = run()
    for m in messages:
        print(m)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(_main())
