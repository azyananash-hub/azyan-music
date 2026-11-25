"""Lint spesifikasi (PRD) berbasis template spec-kit: placeholder tersisa, bagian wajib, kriteria terukur,
dan ID kebutuhan. Hasilnya juga menjadi daftar tugas handoff untuk AI coding (satu tes per FR-ID).

Usage: python prd_lint.py spec.md [--handoff handoff.json]
"""
from __future__ import annotations

import json
import re
import sys

REQUIRED_SECTIONS = ("## User Scenarios & Testing", "## Requirements", "## Success Criteria")
PLACEHOLDER_RE = re.compile(r"\[(FEATURE NAME|Brief Title|DATE|Describe [^\]]*|Explain [^\]]*|[###-feature-name])\]|NEEDS CLARIFICATION")
FR_RE = re.compile(r"\bFR-\d{3}\b")
PRIORITY_RE = re.compile(r"\(Priority:\s*P[1-3]\)")
MEASURABLE_RE = re.compile(r"\d|%|seconds?|detik|minutes?|menit")


def lint(text: str) -> dict:
    issues: list[str] = []
    for m in sorted({m.group(0) for m in PLACEHOLDER_RE.finditer(text)}):
        issues.append(f"placeholder template tersisa: {m}")
    for sec in REQUIRED_SECTIONS:
        if sec not in text:
            issues.append(f"bagian wajib hilang: '{sec}'")
    stories = re.findall(r"^### User Story \d+ - .*$", text, flags=re.M)
    for s in stories:
        if not PRIORITY_RE.search(s):
            issues.append(f"user story tanpa prioritas P1-P3: {s[:60]}")
    if "## Success Criteria" in text:
        block = text.split("## Success Criteria", 1)[1].split("\n## ", 1)[0]
        items = [ln for ln in block.splitlines() if ln.strip().startswith(("-", "*")) and "SC-" in ln]
        if not items:
            issues.append("success criteria tanpa item SC-### yang terukur")
        for ln in items:
            if not MEASURABLE_RE.search(ln):
                issues.append(f"kriteria tidak terukur: {ln.strip()[:70]}")
    frs = sorted(set(FR_RE.findall(text)))
    if "## Requirements" in text and not frs:
        issues.append("tidak ada ID kebutuhan FR-###")
    handoff = [{"id": fr, "task": f"implementasi {fr}", "test": f"TEST-{fr}"} for fr in frs]
    return {"issues": issues, "requirement_ids": frs, "handoff_tasks": handoff,
            "status": "PASS" if not issues else "FAIL"}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: prd_lint.py spec.md [--handoff out.json]", file=sys.stderr)
        sys.exit(2)
    with open(sys.argv[1], encoding="utf-8") as fh:
        res = lint(fh.read())
    if "--handoff" in sys.argv:
        with open(sys.argv[sys.argv.index("--handoff") + 1], "w", encoding="utf-8") as fh:
            json.dump(res["handoff_tasks"], fh, indent=2, ensure_ascii=False)
    print(json.dumps({k: res[k] for k in ("issues", "requirement_ids", "status")}, indent=2, ensure_ascii=False))
    sys.exit(0 if res["status"] == "PASS" else 1)
