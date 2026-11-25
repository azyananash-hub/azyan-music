"""Lint storyboard: integritas shot, durasi, gerak kamera yang diizinkan, dan kontinuitas karakter.

Kontinuitas karakter ditegakkan lewat registry: setiap shot hanya boleh merujuk ID karakter yang ada,
dan setiap karakter wajib punya kostum dan palet. Ini mencegah karakter berubah diam-diam antar-shot.
Input JSON: {"target_s": 60, "allowed_camera": [...], "characters": {...}, "shots": [...]}
Usage: python storyboard_lint.py storyboard.json
"""
from __future__ import annotations

import json
import sys

REQUIRED_CHAR_FIELDS = ("name", "costume", "palette")


def lint(sb: dict) -> list[str]:
    issues: list[str] = []
    chars = sb.get("characters", {})
    allowed = set(sb.get("allowed_camera", []))
    ids = [s.get("id") for s in sb.get("shots", [])]
    for cid, c in chars.items():
        for f in REQUIRED_CHAR_FIELDS:
            if not str(c.get(f, "")).strip():
                issues.append(f"karakter {cid}: field '{f}' kosong (wajib untuk kontinuitas)")
    if len(set(ids)) != len(ids):
        dup = sorted({i for i in ids if ids.count(i) > 1})
        issues.append(f"id shot duplikat: {', '.join(map(str, dup))}")
    total = 0.0
    for s in sb.get("shots", []):
        sid = s.get("id", "?")
        d = s.get("duration_s")
        if not isinstance(d, (int, float)) or d <= 0:
            issues.append(f"shot {sid}: duration_s harus > 0")
        else:
            total += d
        if allowed and s.get("camera") not in allowed:
            issues.append(f"shot {sid}: gerak kamera '{s.get('camera')}' tidak ada di daftar yang diizinkan")
        for cid in s.get("characters", []):
            if cid not in chars:
                issues.append(f"shot {sid}: karakter '{cid}' tidak ada di registry")
    target = sb.get("target_s")
    if target is not None and abs(total - target) > 1e-6:
        issues.append(f"total durasi {total:.2f}s tidak sama dengan target {target}s")
    return issues


def _main(argv=None) -> int:
    if not argv and len(sys.argv) < 2:
        print("usage: storyboard_lint.py storyboard.json", file=sys.stderr)
        return 2
    path = (argv or sys.argv[1:])[0]
    try:
        with open(path, encoding="utf-8") as fh:
            sb = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    issues = lint(sb)
    print(json.dumps({"issues": issues, "status": "PASS" if not issues else "FAIL"}, indent=2, ensure_ascii=False))
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(_main())
