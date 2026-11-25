"""Pasang skill ZY ke folder discovery Claude Code (atau platform lain yang membaca SKILL.md).

Claude Code membaca skill dari:
  - ~/.claude/skills/<nama-skill>/SKILL.md          (global, semua proyek)
  - <proyek>/.claude/skills/<nama-skill>/SKILL.md   (hanya proyek itu)

Usage:
  python scripts/install_skills.py --list
  python scripts/install_skills.py --target ~/.claude/skills                 # dry-run (default)
  python scripts/install_skills.py --target ~/.claude/skills --apply         # benar-benar menyalin
  python scripts/install_skills.py --target ./.claude/skills --apply --only short-circuit-calculator

Keamanan:
  - Hanya skill yang lolos validate_skill (tanpa error) yang disalin.
  - Default dry-run. Tidak pernah menghapus folder yang sudah ada tanpa --force.
  - Tidak menjalankan script apa pun.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys

from zy_lib import discover_skills, validate_skill

SKIP_NAMES = {"__pycache__", ".pytest_cache"}


def _copy_tree(src: str, dst: str) -> None:
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*SKIP_NAMES))


def plan(target: str, only: set[str] | None, force: bool) -> list[tuple[str, str, str]]:
    """Kembalikan daftar (aksi, nama, sumber). Aksi: install | skip-invalid | skip-exists | replace."""
    actions = []
    for doc in discover_skills():
        validate_skill(doc)
        name = doc.name or doc.folder
        if only and name not in only:
            continue
        src = os.path.dirname(doc.path)
        if doc.errors:
            actions.append(("skip-invalid", name, src))
            continue
        dst = os.path.join(target, name)
        if os.path.exists(dst):
            actions.append(("replace" if force else "skip-exists", name, src))
        else:
            actions.append(("install", name, src))
    return actions


def apply(target: str, actions: list[tuple[str, str, str]]) -> int:
    done = 0
    for action, name, src in actions:
        if action in ("install", "replace"):
            dst = os.path.join(target, name)
            if action == "replace":
                shutil.rmtree(dst)
            _copy_tree(src, dst)
            done += 1
    return done


def _main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--target", help="Folder skills tujuan, mis. ~/.claude/skills")
    p.add_argument("--apply", action="store_true", help="Terapkan; tanpa flag ini hanya dry-run")
    p.add_argument("--force", action="store_true", help="Timpa skill yang sudah ada di target")
    p.add_argument("--only", action="append", help="Batasi ke nama skill tertentu (boleh diulang)")
    p.add_argument("--list", action="store_true", help="Tampilkan skill yang tersedia")
    args = p.parse_args(argv)

    if args.list:
        for doc in discover_skills():
            validate_skill(doc)
            status = "OK" if not doc.errors else "INVALID"
            print(f"[{status}] {doc.category}/{doc.name or doc.folder}")
        return 0

    if not args.target:
        p.error("--target wajib (kecuali --list)")
    target = os.path.abspath(os.path.expanduser(args.target))
    actions = plan(target, set(args.only) if args.only else None, args.force)
    for action, name, src in actions:
        print(f"{action:12} {name}  <- {src}")

    if not args.apply:
        print("\nDry-run: tidak ada perubahan. Tambahkan --apply untuk menyalin.")
        return 0
    os.makedirs(target, exist_ok=True)
    count = apply(target, actions)
    print(f"\nSelesai: {count} skill disalin ke {target}")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
