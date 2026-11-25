"""Utilitas bersama untuk ZY Skill Library: parsing SKILL.md, discovery, dan aturan standar.

Tanpa dependensi pihak ketiga (hanya standard library Python 3.9+).
"""

from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass, field

LIBRARY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(LIBRARY_ROOT, "skills")

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME_LEN = 64
MAX_DESCRIPTION_LEN = 1024

# Heading wajib sesuai "Skill Engineering Standard" (lihat skills/governance/skill-engineering-standard).
REQUIRED_SECTIONS = (
    "Activation Triggers",
    "Scope dan Batas Kemampuan",
    "Required Tools",
    "Input dan Output Specification",
    "Execution Workflow",
    "Decision Rules",
    "Error Handling",
    "Quality Control",
    "Acceptance Criteria",
    "Contoh Implementasi",
    "Test Cases",
    "Referensi dan Sumber",
    "Informasi Lisensi",
)

_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_SCRIPT_REF_RE = re.compile(r"scripts/[A-Za-z0-9_\-./]+\.(?:py|sh|js|ps1)")


@dataclass
class SkillDoc:
    path: str                       # path absolut ke SKILL.md
    folder: str                     # nama folder skill
    category: str                   # nama kategori (folder induk)
    frontmatter: dict = field(default_factory=dict)
    body: str = ""
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)

    @property
    def name(self) -> str:
        return self.frontmatter.get("name", "")

    @property
    def description(self) -> str:
        return self.frontmatter.get("description", "")


def parse_frontmatter(text: str) -> tuple[dict, str, list[str]]:
    """Parser frontmatter sederhana yang mendukung:
      - pasangan `key: value` satu baris
      - block scalar `key: >` / `key: |` (baris berindent digabung)
      - key bersarang (baris berindent setelah key kosong) diabaikan, bukan error
    Tanpa PyYAML agar tetap zero-dependency.
    """
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, text, ["frontmatter YAML wajib di baris pertama (---)"]
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text, ["frontmatter tidak ditutup dengan ---"]
    block = text[4:end]
    body = text[end + 4:].lstrip("\n")
    data: dict = {}
    lines = block.splitlines()
    i = 0
    last_plain = False
    while i < len(lines):
        raw = lines[i]
        i += 1
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith((" ", "\t")):
            # Continuation dari nilai plain tidak didukung: laporkan, jangan telan diam-diam.
            if last_plain:
                errors.append(f"frontmatter baris {i}: continuation nilai plain tidak didukung, gunakan '>' atau '|'")
                last_plain = False
            continue  # key bersarang (nilai kosong) diabaikan
        if ":" not in raw:
            errors.append(f"frontmatter baris {i}: format key: value tidak valid")
            continue
        key, value = raw.split(":", 1)
        key, value = key.strip(), value.strip()
        if value in (">", "|", ">-", "|-"):
            chunk = []
            while i < len(lines) and (not lines[i].strip() or lines[i].startswith((" ", "\t"))):
                chunk.append(lines[i].strip())
                i += 1
            sep = " " if value.startswith(">") else "\n"
            data[key] = sep.join(c for c in chunk if c).strip()
            last_plain = False
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        data[key] = value
        last_plain = value != ""
    return data, body, errors


def parse_skill(path: str, category: str) -> SkillDoc:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    fm, body, errors = parse_frontmatter(text)
    doc = SkillDoc(path=path, folder=os.path.basename(os.path.dirname(path)), category=category,
                   frontmatter=fm, body=body, errors=errors)
    return doc


def discover_skills(skills_dir: str = SKILLS_DIR) -> list[SkillDoc]:
    """Temukan semua SKILL.md di skills/<kategori>/<nama-skill>/SKILL.md."""
    docs: list[SkillDoc] = []
    if not os.path.isdir(skills_dir):
        return docs
    for category in sorted(os.listdir(skills_dir)):
        cat_path = os.path.join(skills_dir, category)
        if not os.path.isdir(cat_path):
            continue
        for root, dirs, files in os.walk(cat_path):
            dirs.sort()
            if "SKILL.md" in files:
                docs.append(parse_skill(os.path.join(root, "SKILL.md"), category))
    return docs


def sections_in(body: str) -> list[str]:
    return [m.group(1).strip() for m in _HEADING_RE.finditer(body)]


def script_references(body: str) -> list[str]:
    return sorted(set(_SCRIPT_REF_RE.findall(body)))


def is_imported(doc: SkillDoc) -> bool:
    """Skill hasil impor dari upstream punya SOURCE.md; standar 13-section tidak berlaku untuknya."""
    return os.path.isfile(os.path.join(os.path.dirname(doc.path), "SOURCE.md"))


def validate_imported(doc: SkillDoc) -> SkillDoc:
    """Validasi minimal untuk skill IMPORTED: tidak diubah, jadi hanya cek kontrak discovery dan provenance."""
    fm = doc.frontmatter
    folder = os.path.dirname(doc.path)
    if not fm.get("name"):
        doc.errors.append("frontmatter 'name' wajib")
    elif fm["name"] != doc.folder:
        doc.errors.append(f"name '{fm['name']}' harus sama dengan nama folder '{doc.folder}'")
    if not fm.get("description"):
        doc.errors.append("frontmatter 'description' wajib")
    elif len(fm["description"]) > MAX_DESCRIPTION_LEN:
        # Skill upstream tidak diubah; panjang berlebih hanya dicatat sebagai warning.
        doc.warnings.append(f"description {len(fm['description'])} karakter melebihi {MAX_DESCRIPTION_LEN} (upstream, tidak diubah)")
    if not any(os.path.isfile(os.path.join(folder, n)) for n in ("LICENSE", "LICENSE.txt", "LICENSE.md")):
        doc.errors.append("file lisensi (LICENSE/LICENSE.txt) wajib untuk skill impor")
    return doc


def validate_skill(doc: SkillDoc) -> SkillDoc:
    """Isi doc.errors dan doc.warnings sesuai standar. Mengembalikan doc yang sama."""
    if is_imported(doc):
        return validate_imported(doc)
    fm = doc.frontmatter
    if not fm.get("name"):
        doc.errors.append("frontmatter 'name' wajib")
    else:
        if fm["name"] != doc.folder:
            doc.errors.append(f"name '{fm['name']}' harus sama dengan nama folder '{doc.folder}'")
        if not NAME_RE.match(fm["name"]) or len(fm["name"]) > MAX_NAME_LEN:
            doc.errors.append("name harus kebab-case huruf kecil/angka, maksimal 64 karakter")
    desc = fm.get("description", "")
    if not desc:
        doc.errors.append("frontmatter 'description' wajib")
    elif len(desc) > MAX_DESCRIPTION_LEN:
        doc.errors.append(f"description {len(desc)} karakter, maksimal {MAX_DESCRIPTION_LEN}")
    elif len(desc) < 40:
        doc.warnings.append("description sangat pendek; sulit untuk discovery")
    if not fm.get("license"):
        doc.errors.append("frontmatter 'license' wajib (mis. MIT, Apache-2.0, original-zy)")

    found = sections_in(doc.body)
    for section in REQUIRED_SECTIONS:
        if section not in found:
            doc.errors.append(f"section wajib hilang: '## {section}'")

    for ref in script_references(doc.body):
        # Path dicari relatif ke folder skill, lalu ke root library (untuk tooling bersama).
        candidates = [os.path.join(os.path.dirname(doc.path), ref), os.path.join(LIBRARY_ROOT, ref)]
        if not any(os.path.isfile(c) for c in candidates):
            doc.errors.append(f"script yang direferensikan tidak ada: {ref}")

    if os.path.isdir(os.path.join(os.path.dirname(doc.path), "scripts")) and not script_references(doc.body):
        doc.warnings.append("folder scripts/ ada tetapi tidak direferensikan di SKILL.md")
    return doc


def file_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()
