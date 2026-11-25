"""Buku klaim dokumenter: setiap klaim naratif harus terhubung ke sumber, dan sumber harus lengkap.

Input JSON: {"sources": [{"id", "title", "type": "primary|secondary", "citation", "url", "license"}],
             "claims": [{"id", "text", "source_ids": [...], "status": "verified|unverified"}]}
Aturan: klaim tanpa sumber = ERROR; sumber tidak dikenal = ERROR; klaim 'verified' yang hanya
bersumber sekunder = WARNING (perlu sumber primer); sumber tanpa klaim = WARNING.
"""
from __future__ import annotations

import json
import sys


def audit(doc: dict) -> dict:
    sources = {s["id"]: s for s in doc.get("sources", [])}
    errors, warnings = [], []
    used: set[str] = set()
    for s in sources.values():
        if not s.get("citation") or not (s.get("url") or s.get("citation")):
            warnings.append(f"sumber {s['id']}: kutipan atau URL belum lengkap")
    for c in doc.get("claims", []):
        ids = c.get("source_ids", [])
        if not ids:
            errors.append(f"klaim {c['id']} tanpa sumber: {c.get('text', '')[:60]}")
            continue
        unknown = [i for i in ids if i not in sources]
        if unknown:
            errors.append(f"klaim {c['id']} merujuk sumber tak dikenal: {', '.join(unknown)}")
        used |= set(ids)
        types = {sources[i]["type"] for i in ids if i in sources}
        if c.get("status") == "verified" and types and "primary" not in types:
            warnings.append(f"klaim {c['id']} 'verified' tanpa sumber primer")
    for sid in sorted(set(sources) - used):
        warnings.append(f"sumber {sid} tidak dipakai klaim mana pun")
    return {"errors": errors, "warnings": warnings, "status": "FAIL" if errors else "PASS"}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: claim_ledger.py ledger.json", file=sys.stderr)
        sys.exit(2)
    with open(sys.argv[1], encoding="utf-8") as fh:
        res = audit(json.load(fh))
    print(json.dumps(res, indent=2, ensure_ascii=False))
    sys.exit(0 if res["status"] == "PASS" else 1)
