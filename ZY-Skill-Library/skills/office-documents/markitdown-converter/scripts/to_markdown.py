"""Konversi dokumen (docx, pptx, xlsx, pdf, html) ke Markdown memakai markitdown (MIT).

Usage: python to_markdown.py input.docx [output.md]
"""
from __future__ import annotations

import sys

from markitdown import MarkItDown


def convert(path: str) -> str:
    return MarkItDown().convert(path).text_content


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERROR: beri path file input", file=sys.stderr)
        sys.exit(2)
    try:
        text = convert(sys.argv[1])
    except Exception as exc:  # markitdown melempar beragam tipe error per format
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(2)
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w", encoding="utf-8") as fh:
            fh.write(text)
    else:
        print(text)
