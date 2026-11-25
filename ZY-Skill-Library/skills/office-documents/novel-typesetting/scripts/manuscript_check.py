"""Periksa naskah novel (bab, jumlah kata/karakter per bab) dan ekspor ke DOCX dengan gaya judul bab.

Format naskah: baris "Bab N" atau "Chapter N" memulai bab; teks lain adalah paragraf.
Hitungan: 'words' (spasi sebagai pemisah, untuk bahasa berspasi) atau 'chars' (karakter non-spasi, untuk Jepang).
Pemeriksaan: nomor bab harus berurutan mulai 1, bab kosong ditolak, bab di bawah batas diberi peringatan.
Usage: python manuscript_check.py naskah.txt [--docx out.docx] [--mode words|chars] [--min 500]
"""
from __future__ import annotations

import argparse
import json
import re
import sys

HEADING_RE = re.compile(r"^(Bab|Chapter)\s+(\d+)\b.*$")


def parse(text: str) -> list[dict]:
    chapters: list[dict] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = HEADING_RE.match(line)
        if m:
            chapters.append({"number": int(m.group(2)), "title": line, "paragraphs": []})
        elif chapters:
            chapters[-1]["paragraphs"].append(line)
        else:
            raise ValueError("teks sebelum bab pertama; beri judul bab di awal naskah")
    return chapters


def count(paragraphs: list[str], mode: str) -> int:
    if mode == "chars":
        return sum(len(re.sub(r"\s", "", p)) for p in paragraphs)
    return sum(len(p.split()) for p in paragraphs)


def check(chapters: list[dict], mode: str = "words", min_count: int = 0) -> dict:
    issues, warnings = [], []
    for i, ch in enumerate(chapters, start=1):
        if ch["number"] != i:
            issues.append(f"nomor bab {ch['number']} seharusnya {i}")
        if not ch["paragraphs"]:
            issues.append(f"bab {ch['number']} kosong")
        n = count(ch["paragraphs"], mode)
        ch["count"] = n
        if min_count and n < min_count:
            warnings.append(f"bab {ch['number']}: {n} {mode} di bawah batas {min_count}")
    return {"chapters": [{k: v for k, v in c.items() if k != "paragraphs"} for c in chapters],
            "issues": issues, "warnings": warnings, "status": "PASS" if not issues else "FAIL"}


def to_docx(chapters: list[dict], path: str) -> None:
    from docx import Document

    doc = Document()
    for ch in chapters:
        doc.add_heading(ch["title"], level=1)
        for p in ch["paragraphs"]:
            doc.add_paragraph(p)
    doc.save(path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("txt")
    ap.add_argument("--docx")
    ap.add_argument("--mode", choices=["words", "chars"], default="words")
    ap.add_argument("--min", type=int, default=0)
    a = ap.parse_args()
    try:
        with open(a.txt, encoding="utf-8") as fh:
            chapters = parse(fh.read())
        res = check(chapters, a.mode, a.min)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
    if a.docx and res["status"] == "PASS":
        to_docx(chapters, a.docx)
    print(json.dumps(res, indent=2, ensure_ascii=False))
    sys.exit(0 if res["status"] == "PASS" else 1)
