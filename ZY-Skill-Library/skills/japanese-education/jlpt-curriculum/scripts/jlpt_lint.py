"""Lint data kosakata JLPT (format CSV OpenJLPT) dan hitung cakupan per level.

Pemeriksaan: kolom wajib terisi, level sesuai nama berkas, bacaan (reading) hanya kana (hiragana,
katakana, dan tanda panjang), duplikasi (word, reading) dalam satu level, dan jenis penulisan
(kanji/kana/campuran) per level. Dataset dan level bersumber dari komunitas (lihat NOTICE.md).
Usage: python jlpt_lint.py references/openjlpt
"""
from __future__ import annotations

import csv
import glob
import json
import os
import re
import sys
import unicodedata
from collections import Counter

REQUIRED = ("id", "word", "reading", "meanings", "level")
KANA_RE = re.compile(r"^[ぁ-ゖァ-ヺーヽヾ゙゚]+$")  # hiragana, katakana, ー, ゝゞヽヾ, dakuten


def script_kind(text: str) -> str:
    has_kanji = any("CJK UNIFIED" in unicodedata.name(c, "") for c in text)
    has_kana = any(unicodedata.name(c, "").startswith(("HIRAGANA", "KATAKANA")) for c in text)
    if has_kanji and has_kana:
        return "campuran"
    return "kanji" if has_kanji else "kana"


def lint_file(path: str, level: str) -> dict:
    issues: list[str] = []
    rows = []
    with open(path, encoding="utf-8", newline="") as fh:
        for n, row in enumerate(csv.DictReader(fh), start=2):
            rows.append(row)
            for f in REQUIRED:
                if not (row.get(f) or "").strip():
                    issues.append(f"baris {n}: kolom '{f}' kosong")
            if row.get("level") and row["level"] != level:
                issues.append(f"baris {n}: level '{row['level']}' tidak sesuai berkas {level}")
            if row.get("reading") and not KANA_RE.match(row["reading"]):
                issues.append(f"baris {n}: bacaan '{row['reading']}' bukan kana murni")
    seen = Counter((r.get("word", ""), r.get("reading", "")) for r in rows)
    dups = [k for k, v in seen.items() if v > 1 and k[0]]
    for w, rd in dups:
        issues.append(f"duplikat (word, reading) dalam {level}: {w} / {rd}")
    kinds = Counter(script_kind(r.get("word", "")) for r in rows if r.get("word"))
    return {"level": level, "entries": len(rows), "script": dict(kinds), "issues": issues}


def lint_dir(folder: str) -> dict:
    results = []
    for path in sorted(glob.glob(os.path.join(folder, "vocab-n*.csv"))):
        level = "N" + re.search(r"vocab-n(\d)\.csv$", path).group(1)
        results.append(lint_file(path, level))
    total = sum(r["entries"] for r in results)
    issues = sum(len(r["issues"]) for r in results)
    return {"levels": results, "total_entries": total, "issues": issues,
            "status": "PASS" if issues == 0 and results else "FAIL"}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: jlpt_lint.py <folder berisi vocab-n*.csv>", file=sys.stderr)
        sys.exit(2)
    out = lint_dir(sys.argv[1])
    print(json.dumps(out, indent=2, ensure_ascii=False))
    sys.exit(0 if out["status"] == "PASS" else 1)
