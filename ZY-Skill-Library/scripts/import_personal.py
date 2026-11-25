"""Impor skill pribadi (SKILL.md, folder, ZIP, atau URL GitHub publik) ke library.

Aturan keamanan:
- Lisensi wajib dinyatakan (--license). Tanpa itu impor ditolak.
- Risiko HIGH (scan_skill_risk) menolak impor.
- Nama yang sudah ada: identik -> no-op; berbeda -> ditolak kecuali --approve-overwrite.
  Versi lama diarsipkan di research/skill-versions/ sebelum ditimpa.
- Skill yang gagal validasi dihapus lagi (rollback).
Usage:
  python scripts/import_personal.py <sumber> --category <kategori> --license MIT [--label nama] [--approve-overwrite]
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

from zy_lib import LIBRARY_ROOT, SKILLS_DIR, discover_skills, parse_frontmatter, validate_skill

MANIFEST = os.path.join(LIBRARY_ROOT, "research", "import-manifest.json")
ARCHIVE = os.path.join(LIBRARY_ROOT, "research", "skill-versions")
SCANNER = os.path.join(LIBRARY_ROOT, "skills", "governance", "third-party-skill-audit", "scripts", "scan_skill_risk.py")


def materialize(source: str, workdir: str) -> str:
    """Kembalikan folder berisi SKILL.md, di dalam workdir (staging)."""
    dst = os.path.join(workdir, "src")
    if re.match(r"^https://github\.com/[\w.-]+/[\w.-]+(\.git)?/?$", source):
        subprocess.run(["git", "clone", "-q", "--depth", "1", source.rstrip("/"), dst], check=True, timeout=300)
        shutil.rmtree(os.path.join(dst, ".git"), ignore_errors=True)
    elif source.lower().endswith(".zip") and os.path.isfile(source):
        os.makedirs(dst)
        with zipfile.ZipFile(source) as z:
            for m in z.namelist():
                if os.path.isabs(m) or ".." in m.replace("\\", "/").split("/"):
                    raise ValueError(f"path berbahaya di ZIP: {m}")
            z.extractall(dst)
    elif os.path.isdir(source):
        shutil.copytree(source, dst)
    elif os.path.isfile(source) and os.path.basename(source) == "SKILL.md":
        os.makedirs(dst)
        shutil.copy(source, os.path.join(dst, "SKILL.md"))
    else:
        raise ValueError("sumber tidak dikenali: beri file SKILL.md, folder, ZIP, atau URL GitHub publik")
    found = []
    for root, _dirs, files in os.walk(dst):
        if "SKILL.md" in files and root.count(os.sep) - dst.count(os.sep) <= 2:
            found.append(root)
    if len(found) != 1:
        raise ValueError(f"harus tepat satu SKILL.md, ditemukan {len(found)}")
    return found[0]


def sha256_tree(folder: str) -> str:
    h = hashlib.sha256()
    for root, _d, files in sorted(os.walk(folder)):
        for f in sorted(files):
            p = os.path.join(root, f)
            h.update(os.path.relpath(p, folder).encode())
            with open(p, "rb") as fh:
                h.update(fh.read())
    return h.hexdigest()


def _tokens(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", text.lower()) if len(t) > 2}


def similar_existing(desc: str, threshold: float = 0.6) -> list[str]:
    """Peringatan (bukan penolakan) bila deskripsi sangat mirip skill lain."""
    mine = _tokens(desc)
    hits = []
    for d in discover_skills():
        other = _tokens(d.description)
        if mine and other and len(mine & other) / len(mine | other) >= threshold:
            hits.append(d.name or d.folder)
    return hits


def run(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("source")
    p.add_argument("--category", required=True)
    p.add_argument("--license", required=True, help="SPDX atau nama lisensi yang Anda nyatakan")
    p.add_argument("--label", default=None, help="nama sumber untuk provenance")
    p.add_argument("--approve-overwrite", action="store_true")
    a = p.parse_args(argv)

    with tempfile.TemporaryDirectory() as tmp:
        try:
            folder = materialize(a.source, tmp)
        except (ValueError, OSError, subprocess.SubprocessError) as exc:
            print(f"DITOLAK: {exc}")
            return 2
        with open(os.path.join(folder, "SKILL.md"), encoding="utf-8") as fh:
            fm, _body, errs = parse_frontmatter(fh.read())
        name = fm.get("name", "")
        if errs or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name or "") or not fm.get("description"):
            print(f"DITOLAK: frontmatter tidak valid {errs or '(name/description kosong atau tidak kebab-case)'}")
            return 2

        digest = sha256_tree(folder)
        dst = os.path.join(SKILLS_DIR, a.category, name)
        if os.path.exists(dst):
            old = os.path.join(dst, "SOURCE.md")
            old_digest = None
            if os.path.isfile(old):
                m = re.search(r"- SHA-256 isi: ([0-9a-f]{64})", open(old, encoding="utf-8").read())
                old_digest = m.group(1) if m else None
            if old_digest == digest:
                print(f"NO-OP: '{name}' sudah ada dengan isi identik.")
                return 0
            if not a.approve_overwrite:
                print(f"KONFLIK: '{name}' sudah ada dengan isi berbeda. Tidak ditimpa tanpa --approve-overwrite.")
                return 3
            os.makedirs(ARCHIVE, exist_ok=True)
            shutil.copy(os.path.join(dst, "SKILL.md"), os.path.join(ARCHIVE, f"{name}-{(old_digest or 'unknown')[:12]}.md"))

        scan = subprocess.run([sys.executable, SCANNER, folder, "--json"], capture_output=True, text=True)
        findings = json.loads(scan.stdout)["findings"]
        high = [f for f in findings if f["severity"] == "HIGH"]
        if high:
            print(f"DITOLAK: {len(high)} temuan HIGH, contoh: {high[0]['rule']} di {high[0]['file']}")
            return 4
        sims = similar_existing(fm["description"])
        if sims:
            print(f"PERINGATAN: deskripsi mirip dengan skill yang ada: {', '.join(sims)}")

        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(folder, dst, ignore=shutil.ignore_patterns("__pycache__", ".git"))
        label = a.label or os.path.basename(a.source.rstrip("/"))
        today = dt.date.today().isoformat()
        with open(os.path.join(dst, "SOURCE.md"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(f"# Sumber impor\n\n- Klasifikasi: IMPORTED (skill pribadi, tidak dimodifikasi)\n"
                     f"- Sumber: {label}\n- Lisensi (dinyatakan pengguna): {a.license}\n"
                     f"- SHA-256 isi: {digest}\n- Tanggal impor: {today}\n- Risiko: {len(findings)} temuan, 0 HIGH\n")
        with open(os.path.join(dst, "LICENSE.txt"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(f"Lisensi yang dinyatakan pengguna: {a.license}.\nTeks lisensi lengkap tidak disediakan saat impor; "
                     "verifikasi sebelum distribusi.\n")
        problems = validate_skill(next(d for d in discover_skills() if d.folder == name))
        if problems.errors:
            shutil.rmtree(dst)
            print(f"DITOLAK (rollback): {problems.errors}")
            return 2

        with open(MANIFEST, encoding="utf-8") as fh:
            manifest = json.load(fh)
        entry = {"name": name, "category": a.category, "classification": "IMPORTED", "status": "IMPORTED",
                 "source_repo": label, "source_commit": None, "license": a.license,
                 "library_path": os.path.relpath(dst, LIBRARY_ROOT).replace(os.sep, "/"),
                 "imported_on": today, "test_evidence": "Impor pribadi: struktur, lisensi dinyatakan, dan risiko lolos; perilaku belum diuji.",
                 "sha256": digest}
        manifest["entries"] = [e for e in manifest["entries"] if e["name"] != name] + [entry]
        manifest["entries"].sort(key=lambda e: e["name"])
        with open(MANIFEST, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        subprocess.run([sys.executable, os.path.join(LIBRARY_ROOT, "scripts", "build_registry.py")],
                       check=True, capture_output=True)
        print(f"IMPORTED '{name}' -> {entry['library_path']} (sha256 {digest[:12]}); registry diperbarui")
        return 0


if __name__ == "__main__":
    sys.exit(run())
