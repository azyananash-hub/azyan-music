"""Periksa layout panel halaman manhwa: batas halaman, tumpang tindih, ukuran minimum, dan urutan baca.

Urutan baca: panel dikelompokkan per baris (rentang y yang beririsan), lalu diurutkan dari kanan ke kiri
untuk manga Jepang (rtl) atau kiri ke kanan (ltr). Jika 'order' diberikan, urutannya harus sama.
Input JSON: {"page": {"width": W, "height": H, "margin": M, "reading": "rtl"|"ltr"},
             "panels": [{"id": "P1", "x": .., "y": .., "w": .., "h": ..}], "order": ["P1", ...] (opsional)}
"""
from __future__ import annotations

import json
import sys

MIN_SIDE = 80  # piksel; batas praktis agar panel tetap terbaca, bukan standar industri


def _overlap(a: dict, b: dict) -> bool:
    return a["x"] < b["x"] + b["w"] and b["x"] < a["x"] + a["w"] and a["y"] < b["y"] + b["h"] and b["y"] < a["y"] + a["h"]


def reading_order(panels: list[dict], reading: str) -> list[str]:
    rows: list[list[dict]] = []
    for p in sorted(panels, key=lambda q: q["y"]):
        for row in rows:
            if any(p["y"] < r["y"] + r["h"] and r["y"] < p["y"] + p["h"] for r in row):
                row.append(p)
                break
        else:
            rows.append([p])
    ordered = []
    for row in sorted(rows, key=lambda r: min(p["y"] for p in r)):
        ordered += sorted(row, key=lambda p: p["x"], reverse=(reading == "rtl"))
    return [p["id"] for p in ordered]


def lint(page: dict, panels: list[dict], order: list[str] | None = None) -> list[str]:
    issues: list[str] = []
    W, H, M = page["width"], page["height"], page.get("margin", 0)
    reading = page.get("reading", "rtl")
    if reading not in ("rtl", "ltr"):
        return [f"reading harus rtl atau ltr, dapat {reading}"]
    for p in panels:
        if p["x"] < M or p["y"] < M or p["x"] + p["w"] > W - M or p["y"] + p["h"] > H - M:
            issues.append(f"panel {p['id']}: di luar margin halaman")
        if p["w"] < MIN_SIDE or p["h"] < MIN_SIDE:
            issues.append(f"panel {p['id']}: lebih kecil dari {MIN_SIDE}px")
    for i, a in enumerate(panels):
        for b in panels[i + 1:]:
            if _overlap(a, b):
                issues.append(f"panel {a['id']} dan {b['id']} saling tumpang tindih")
    if order is not None:
        expected = reading_order(panels, reading)
        if order != expected:
            issues.append(f"urutan baca {order} tidak sama dengan urutan hasil layout {expected}")
    return issues


def _main(argv=None) -> int:
    if len(sys.argv) < 2:
        print("usage: panel_check.py page.json", file=sys.stderr)
        return 2
    try:
        with open(sys.argv[1], encoding="utf-8") as fh:
            d = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    issues = lint(d["page"], d["panels"], d.get("order"))
    print(json.dumps({"reading_order": reading_order(d["panels"], d["page"].get("reading", "rtl")),
                      "issues": issues, "status": "PASS" if not issues else "FAIL"}, indent=2, ensure_ascii=False))
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(_main())
