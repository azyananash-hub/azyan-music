"""Pemindai risiko statis untuk folder skill/script pihak ketiga SEBELUM dijalankan.

Ini adalah heuristik, bukan antivirus. Hasil "bersih" TIDAK berarti aman.
Script ini tidak pernah mengeksekusi isi file yang dipindai.

Yang dideteksi (contoh):
  HIGH  : pipe ke shell dari internet (curl|sh), decode-lalu-exec (base64 -d | sh),
          Invoke-Expression/iex dengan download, eval/exec pada string dinamis,
          penghapusan rekursif root (rm -rf /), file binary (ELF/PE/Mach-O).
  MEDIUM: os.system / subprocess dengan shell=True, akses ~/.ssh, ~/.aws, .env, browser profile,
          modifikasi shell profile (.bashrc, .zshrc, PowerShell profile),
          pemasangan paket tanpa lock (pip/npm install dalam skrip).
  LOW   : URL jaringan eksternal (untuk ditinjau manual), file tersembunyi, ukuran file besar.

Exit code: 0 tidak ada HIGH, 1 ada HIGH, 2 error input.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict

TEXT_EXTENSIONS = {
    ".md", ".txt", ".py", ".sh", ".bash", ".zsh", ".ps1", ".js", ".mjs", ".ts", ".json",
    ".yaml", ".yml", ".toml", ".cfg", ".ini", ".html", ".css", ".rb", ".go", ".rs", ".java",
    ".kt", ".dart", ".cmd", ".bat",
}
MAX_FILE_BYTES = 1_000_000  # file lebih besar dari ini dilaporkan (LOW)
URL_RE = re.compile(r"https?://[^\s'\"<>)]+")


@dataclass(frozen=True)
class Finding:
    severity: str
    rule: str
    file: str
    line: int
    snippet: str


RULES: list[tuple[str, str, re.Pattern]] = [
    ("HIGH", "pipe-remote-to-shell", re.compile(r"(curl|wget)[^\n|]*\|\s*(sudo\s+)?(sh|bash|zsh|python\d?)\b", re.I)),
    ("HIGH", "decode-and-exec", re.compile(r"base64\s+(-d|--decode)[^\n|]*\|\s*(sh|bash|python\d?)\b", re.I)),
    ("HIGH", "powershell-download-exec", re.compile(r"(iex|invoke-expression)[^\n]*(downloadstring|invoke-webrequest|iwr|irm)", re.I)),
    ("HIGH", "recursive-root-delete", re.compile(r"rm\s+-[a-z]*r[a-z]*f?\s+(/|~|\$HOME)(\s|$)", re.I)),
    ("HIGH", "dynamic-eval", re.compile(r"\beval\s*\(\s*(base64|atob|unescape|decodeURIComponent|String\.fromCharCode)", re.I)),
    ("MEDIUM", "shell-true-subprocess", re.compile(r"subprocess\.\w+\([^)]*shell\s*=\s*True")),
    ("MEDIUM", "os-system", re.compile(r"\bos\.system\s*\(")),
    ("MEDIUM", "credential-path-access", re.compile(r"(~|\$HOME|%USERPROFILE%|/home/\w+)[/\\](\.ssh|\.aws|\.gnupg|\.config/gcloud)|\.env\b")),
    ("MEDIUM", "shell-profile-write", re.compile(r"(>>?\s*~?/?\.(bashrc|zshrc|profile)\b|Add-Content[^\n]*\$PROFILE)", re.I)),
    ("MEDIUM", "unpinned-install", re.compile(r"\b(pip|npm|pnpm|yarn)\s+(install|i|add)\b(?!.*(==|@\d|-r\s|--frozen|--lockfile))", re.I)),
]
# Aturan khusus (binary, symlink, file tersembunyi, ukuran besar) ditangani di scan_path.


def _line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def scan_text(rel_path: str, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for severity, rule, pattern in RULES:
        for m in pattern.finditer(text):
            line = _line_of(text, m.start())
            snippet = text.splitlines()[line - 1].strip()[:160]
            findings.append(Finding(severity, rule, rel_path, line, snippet))
    for m in URL_RE.finditer(text):
        line = _line_of(text, m.start())
        findings.append(Finding("LOW", "external-url", rel_path, line, m.group(0)[:160]))
    return findings


def scan_path(root: str) -> list[Finding]:
    if not os.path.isdir(root):
        raise ValueError(f"bukan direktori: {root}")
    findings: list[Finding] = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Jangan turun ke folder VCS; tetap laporkan keberadaan symlink.
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for name in filenames:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            if os.path.islink(full):
                findings.append(Finding("HIGH", "symlink", rel, 0, "symlink: periksa tujuannya"))
                continue
            if name.startswith("."):
                findings.append(Finding("LOW", "hidden-file", rel, 0, name))
            size = os.path.getsize(full)
            if size > MAX_FILE_BYTES:
                findings.append(Finding("LOW", "large-file", rel, 0, f"{size} bytes"))
            with open(full, "rb") as fh:
                head = fh.read(4)
            if head.startswith((b"\x7fELF", b"MZ", b"\xcf\xfa\xed\xfe")):
                findings.append(Finding("HIGH", "compiled-binary", rel, 0, "binary executable terdeteksi"))
                continue
            ext = os.path.splitext(name)[1].lower()
            if ext not in TEXT_EXTENSIONS and name not in ("Dockerfile", "Makefile"):
                continue
            try:
                with open(full, encoding="utf-8", errors="strict") as fh:
                    text = fh.read(MAX_FILE_BYTES + 1)
            except UnicodeDecodeError:
                findings.append(Finding("MEDIUM", "non-utf8-text", rel, 0, "file bukan UTF-8, tinjau manual"))
                continue
            findings.extend(scan_text(rel, text))
    order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    findings.sort(key=lambda f: (order[f.severity], f.file, f.line))
    return findings


def _main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("directory")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    try:
        findings = scan_path(args.directory)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    has_high = any(f.severity == "HIGH" for f in findings)
    if args.json:
        print(json.dumps({"high_risk": has_high, "findings": [asdict(f) for f in findings]},
                         indent=2, ensure_ascii=False))
    else:
        if not findings:
            print("Tidak ada temuan heuristik. Ini BUKAN jaminan keamanan; tetap tinjau manual.")
        for f in findings:
            print(f"[{f.severity}] {f.rule} {f.file}:{f.line} :: {f.snippet}")
    return 1 if has_high else 0


if __name__ == "__main__":
    sys.exit(_main())
