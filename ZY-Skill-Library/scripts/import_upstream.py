"""Impor skill dari clone lokal repository upstream dan catat provenance-nya.

Setiap skill yang diimpor mendapat:
  - salinan folder utuh (SKILL.md, scripts/, references/, assets/ ...), tanpa modifikasi
  - LICENSE (atau LICENSE.txt) dari repository asal
  - SOURCE.md berisi URL repository, commit, path asal, lisensi, dan tanggal impor
  - entri di research/import-manifest.json

Script ini hanya membaca dari sumber lokal dan menulis ke library. Tidak menjalankan
kode dari sumber. Jalankan dengan --dry-run untuk melihat rencana tanpa menulis.

Usage:
  python scripts/import_upstream.py --source /home/user/anthropics/skills \
      --repo https://github.com/anthropics/skills --commit <sha> --license-file LICENSE.txt \
      --skill pdf:office-documents --skill docx:office-documents [--dry-run]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys

from zy_lib import LIBRARY_ROOT, SKILLS_DIR

MANIFEST_PATH = os.path.join(LIBRARY_ROOT, "research", "import-manifest.json")
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".git", "evals")


def resolve_commit(source: str) -> str:
    out = subprocess.run(["git", "-C", source, "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
    return out.stdout.strip()


def _load_manifest() -> dict:
    if os.path.isfile(MANIFEST_PATH):
        with open(MANIFEST_PATH, encoding="utf-8") as fh:
            return json.load(fh)
    return {"entries": []}


def _save_manifest(data: dict) -> None:
    os.makedirs(os.path.dirname(MANIFEST_PATH), exist_ok=True)
    with open(MANIFEST_PATH, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def import_skill(source: str, repo: str, commit: str, license_file: str, license_name: str,
                 skill: str, category: str, dry_run: bool) -> dict:
    src_dir = os.path.join(source, "skills", skill)
    if not os.path.isfile(os.path.join(src_dir, "SKILL.md")):
        raise FileNotFoundError(f"SKILL.md tidak ditemukan: {src_dir}")
    dst_dir = os.path.join(SKILLS_DIR, category, skill)
    rel_dst = os.path.relpath(dst_dir, LIBRARY_ROOT).replace(os.sep, "/")
    entry = {
        "name": skill,
        "category": category,
        "classification": "IMPORTED",
        "source_repo": repo,
        "source_commit": commit,
        "source_path": f"skills/{skill}",
        "license": license_name,
        "library_path": rel_dst,
        "imported_on": dt.date.today().isoformat(),
    }
    if dry_run:
        print(f"[dry-run] {skill} -> {rel_dst}")
        return entry
    if os.path.exists(dst_dir):
        # Re-import hanya boleh menimpa folder yang memang hasil impor sebelumnya.
        if not os.path.isfile(os.path.join(dst_dir, "SOURCE.md")):
            raise FileExistsError(f"{rel_dst} sudah ada dan bukan hasil impor; tolak menimpa")
        shutil.rmtree(dst_dir)
    shutil.copytree(src_dir, dst_dir, ignore=IGNORE)
    # Lisensi per-skill (mis. LICENSE.txt) sudah ikut tersalin. Lisensi root repository
    # (mis. LICENSE milik obra/superpowers) disalin sebagai LICENSE agar tiap skill berdiri sendiri.
    if license_file and os.path.isfile(os.path.join(source, license_file)):
        shutil.copy2(os.path.join(source, license_file), os.path.join(dst_dir, "LICENSE"))
    with open(os.path.join(dst_dir, "SOURCE.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(
            f"# Sumber impor\n\n"
            f"- Klasifikasi: IMPORTED (tidak dimodifikasi)\n"
            f"- Repository: {repo}\n"
            f"- Commit: {commit}\n"
            f"- Path asal: skills/{skill}\n"
            f"- Lisensi: {license_name}\n"
            f"- Tanggal impor: {entry['imported_on']}\n"
        )
    return entry


def _main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--source", required=True, help="Path clone lokal repository upstream")
    p.add_argument("--repo", required=True, help="URL repository asal (untuk provenance)")
    p.add_argument("--license-name", required=True, help="Nama lisensi, mis. Apache-2.0 atau MIT")
    p.add_argument("--license-file", default=None, help="Path lisensi relatif terhadap source, mis. LICENSE")
    p.add_argument("--skill", action="append", required=True, help="nama_skill:kategori (boleh diulang)")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)

    commit = resolve_commit(args.source)
    manifest = _load_manifest()
    existing = {e["name"]: e for e in manifest["entries"]}
    for spec in args.skill:
        skill, _, category = spec.partition(":")
        if not category:
            p.error(f"format --skill harus nama:kategori, dapat {spec!r}")
        try:
            entry = import_skill(args.source, args.repo, commit, args.license_file, args.license_name,
                                 skill, category, args.dry_run)
        except (OSError, FileNotFoundError) as exc:
            print(f"ERROR {skill}: {exc}", file=sys.stderr)
            return 2
        if not args.dry_run:
            prev = existing.get(skill, {})
            entry["status"] = prev.get("status", "IMPORTED")
            entry["test_evidence"] = prev.get("test_evidence", "")
            existing[skill] = entry
            print(f"IMPORTED {skill} @ {commit[:12]} -> {entry['library_path']}")
    if not args.dry_run:
        manifest["entries"] = sorted(existing.values(), key=lambda e: e["name"])
        _save_manifest(manifest)
    return 0


if __name__ == "__main__":
    sys.exit(_main())
