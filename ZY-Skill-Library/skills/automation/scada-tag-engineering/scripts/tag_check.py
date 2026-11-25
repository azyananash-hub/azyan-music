"""Periksa daftar tag SCADA/HMI: nama unik, pola nama, rentang engineering, dan urutan batas alarm.

Input JSON: {"name_pattern": "^[A-Z]{2,4}-\\d{3}[A-Z]?$", "tags": [{"name", "type": "AI|DI|AO|DO",
  "eng_lo", "eng_hi", "alarm": {"LL", "L", "H", "HH"} (opsional), "device", "address"}]}
Aturan: AI/AO wajib punya rentang engineering dengan eng_lo < eng_hi; DI/DO tidak boleh punya rentang.
Batas alarm harus urut LL <= L <= H <= HH dan berada dalam rentang engineering.
Alamat (device + address) harus unik per perangkat.
"""
from __future__ import annotations

import json
import re
import sys

TYPES = {"AI", "AO", "DI", "DO"}


def lint(doc: dict) -> list[str]:
    issues: list[str] = []
    pattern = re.compile(doc.get("name_pattern", r"^[A-Z]{2,4}-\d{3}[A-Z]?$"))
    names = [t["name"] for t in doc["tags"]]
    for n in sorted({n for n in names if names.count(n) > 1}):
        issues.append(f"nama tag duplikat: {n}")
    addr_seen: dict[tuple, str] = {}
    for t in doc["tags"]:
        n = t["name"]
        if not pattern.match(n):
            issues.append(f"{n}: tidak sesuai pola nama")
        if t.get("type") not in TYPES:
            issues.append(f"{n}: tipe '{t.get('type')}' tidak dikenal")
            continue
        analog = t["type"] in ("AI", "AO")
        has_range = "eng_lo" in t and "eng_hi" in t
        if analog and not has_range:
            issues.append(f"{n}: tag analog wajib punya eng_lo dan eng_hi")
        if analog and has_range and not t["eng_lo"] < t["eng_hi"]:
            issues.append(f"{n}: eng_lo harus lebih kecil dari eng_hi")
        if not analog and has_range:
            issues.append(f"{n}: tag digital tidak boleh punya rentang engineering")
        al = t.get("alarm") or {}
        if al:
            if not analog:
                issues.append(f"{n}: alarm batas hanya untuk tag analog")
            order = [al[k] for k in ("LL", "L", "H", "HH") if k in al]
            if order != sorted(order):
                issues.append(f"{n}: batas alarm tidak urut LL <= L <= H <= HH")
            if has_range and any(not (t["eng_lo"] <= v <= t["eng_hi"]) for v in order):
                issues.append(f"{n}: batas alarm di luar rentang engineering")
        if "device" in t and "address" in t:
            key = (t["device"], t["address"])
            if key in addr_seen:
                issues.append(f"{n}: alamat {t['address']} di {t['device']} dipakai juga oleh {addr_seen[key]}")
            addr_seen[key] = n
    return issues


def _main(argv=None) -> int:
    if len(sys.argv) < 2:
        print("usage: tag_check.py tags.json", file=sys.stderr)
        return 2
    try:
        with open(sys.argv[1], encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    issues = lint(doc)
    print(json.dumps({"issues": issues, "status": "PASS" if not issues else "FAIL"}, indent=2, ensure_ascii=False))
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(_main())
