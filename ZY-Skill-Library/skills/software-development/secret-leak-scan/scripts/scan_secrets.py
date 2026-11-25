"""Pemindai kebocoran secret (API key, token, private key) pada file proyek.

Heuristik berbasis pola. Tidak menggantikan alat khusus seperti gitleaks (MIT) atau
trufflehog untuk pemindaian riwayat git. Nilai secret TIDAK PERNAH dicetak utuh; output hanya memperlihatkan
beberapa karakter awal dan jumlah karakter.

Exit code: 0 tidak ada temuan, 1 ada temuan, 2 error input.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass

SKIP_DIRS = {".git", "node_modules", "build", ".dart_tool", ".gradle", "__pycache__", ".venv"}
MAX_FILE_BYTES = 2_000_000

PATTERNS: list[tuple[str, re.Pattern]] = [
    ("google-api-key", re.compile(r"AIza[0-9A-Za-z_\-]{35}")),
    ("aws-access-key-id", re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("private-key-block", re.compile(r"-----BEGIN (RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY( BLOCK)?-----")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("stripe-live-secret", re.compile(r"\bsk_live_[0-9A-Za-z]{16,}\b")),
    ("openai-style-key", re.compile(r"\bsk-[A-Za-z0-9_\-]{32,}\b")),
    ("supabase-service-role-jwt", re.compile(r"service_role", re.I)),
    ("generic-assignment", re.compile(
        r"(?i)\b(api[_-]?key|secret|token|password|passwd)\b\s*[:=]\s*['\"]([^'\"\s]{12,})['\"]"
    )),
]

PLACEHOLDER_HINTS = ("example", "your_", "your-", "<", "xxxx", "changeme", "placeholder", "dummy")


@dataclass(frozen=True)
class SecretFinding:
    rule: str
    file: str
    line: int
    preview: str  # sudah dimasking


def mask(value: str) -> str:
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}{'*' * (len(value) - 8)}{value[-4:]}"


def _is_placeholder(value: str) -> bool:
    low = value.lower()
    return any(h in low for h in PLACEHOLDER_HINTS)


def scan_text(rel: str, text: str) -> list[SecretFinding]:
    findings: list[SecretFinding] = []
    for idx, line in enumerate(text.splitlines(), start=1):
        for rule, pattern in PATTERNS:
            for m in pattern.finditer(line):
                if rule == "generic-assignment":
                    value = m.group(2)
                    if _is_placeholder(value):
                        continue
                    preview = mask(value)
                elif rule == "supabase-service-role-jwt":
                    # Hanya sinyal lemah: nama 'service_role' sendiri bukan secret.
                    preview = "menyebut service_role (periksa apakah key ikut tertanam di klien)"
                else:
                    preview = mask(m.group(0))
                findings.append(SecretFinding(rule, rel, idx, preview))
    return findings


def scan_directory(root: str) -> list[SecretFinding]:
    if not os.path.isdir(root):
        raise ValueError(f"bukan direktori: {root}")
    out: list[SecretFinding] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            full = os.path.join(dirpath, name)
            try:
                if os.path.getsize(full) > MAX_FILE_BYTES:
                    continue
                with open(full, "rb") as fh:
                    raw = fh.read()
            except OSError:
                continue
            if b"\x00" in raw[:8000]:  # lewati binary
                continue
            text = raw.decode("utf-8", errors="replace")
            out.extend(scan_text(os.path.relpath(full, root), text))
    return out


def _main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("directory")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    try:
        findings = scan_directory(args.directory)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps([asdict(f) for f in findings], indent=2, ensure_ascii=False))
    elif not findings:
        print("Tidak ada temuan pola secret. Ini bukan jaminan; secret yang sudah di-commit tetap harus di-rotate jika pernah terekspos.")
    else:
        for f in findings:
            print(f"[{f.rule}] {f.file}:{f.line} :: {f.preview}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(_main())
