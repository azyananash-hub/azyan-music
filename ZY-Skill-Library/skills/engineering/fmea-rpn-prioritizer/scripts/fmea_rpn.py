"""FMEA prioritizer berbasis Risk Priority Number (RPN) = Severity x Occurrence x Detection.

Input: file CSV dengan kolom:
  item, failure_mode, effect, cause, severity, occurrence, detection [, control]

Skala 1-10 (konvensi FMEA klasik). Nilai di luar 1-10 ditolak, bukan diklip diam-diam.

Catatan metodologi:
  - RPN klasik tidak memperhitungkan bobot relatif antar faktor; dua kombinasi berbeda
    bisa memberi RPN yang sama. Karena itu aturan tambahan "severity tinggi selalu
    ditindaklanjuti" diterapkan.
  - AIAG-VDA (2019) memakai Action Priority (AP); script ini menyediakan RPN dan
    flag severity sebagai pelengkap, bukan pengganti AP.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass

REQUIRED_COLUMNS = ("item", "failure_mode", "severity", "occurrence", "detection")


@dataclass(frozen=True)
class FailureRow:
    item: str
    failure_mode: str
    effect: str
    cause: str
    severity: int
    occurrence: int
    detection: int
    control: str

    @property
    def rpn(self) -> int:
        return self.severity * self.occurrence * self.detection


def _parse_score(name: str, raw: str, line_no: int) -> int:
    try:
        value = int(str(raw).strip())
    except ValueError as exc:
        raise ValueError(f"baris {line_no}: {name} bukan bilangan bulat: {raw!r}") from exc
    if not 1 <= value <= 10:
        raise ValueError(f"baris {line_no}: {name} harus 1-10, dapat {value}")
    return value


def load_rows(lines) -> list[FailureRow]:
    reader = csv.DictReader(lines)
    if reader.fieldnames is None:
        raise ValueError("file CSV kosong")
    missing = [c for c in REQUIRED_COLUMNS if c not in reader.fieldnames]
    if missing:
        raise ValueError(f"kolom wajib hilang: {', '.join(missing)}")
    rows: list[FailureRow] = []
    for line_no, rec in enumerate(reader, start=2):
        rows.append(
            FailureRow(
                item=(rec.get("item") or "").strip(),
                failure_mode=(rec.get("failure_mode") or "").strip(),
                effect=(rec.get("effect") or "").strip(),
                cause=(rec.get("cause") or "").strip(),
                severity=_parse_score("severity", rec["severity"], line_no),
                occurrence=_parse_score("occurrence", rec["occurrence"], line_no),
                detection=_parse_score("detection", rec["detection"], line_no),
                control=(rec.get("control") or "").strip(),
            )
        )
    return rows


def prioritise(rows: list[FailureRow], rpn_threshold: int = 100, severity_threshold: int = 9) -> list[dict]:
    """Urutkan dari RPN tertinggi dan beri flag tindak lanjut."""
    if rpn_threshold < 1:
        raise ValueError("rpn_threshold harus >= 1")
    ordered = sorted(rows, key=lambda r: (r.rpn, r.severity), reverse=True)
    out = []
    for r in ordered:
        flags = []
        if r.rpn >= rpn_threshold:
            flags.append("RPN_ABOVE_THRESHOLD")
        if r.severity >= severity_threshold:
            flags.append("HIGH_SEVERITY_REVIEW")
        d = asdict(r)
        d["rpn"] = r.rpn
        d["flags"] = flags
        out.append(d)
    return out


def _main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv_file", help="Path file CSV FMEA")
    p.add_argument("--rpn-threshold", type=int, default=100)
    p.add_argument("--severity-threshold", type=int, default=9)
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    try:
        with open(args.csv_file, newline="", encoding="utf-8") as fh:
            rows = load_rows(fh)
        result = prioritise(rows, args.rpn_threshold, args.severity_threshold)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        for i, r in enumerate(result, 1):
            print(f"{i:>2}. RPN={r['rpn']:<4} S={r['severity']} O={r['occurrence']} D={r['detection']} "
                  f"{r['item']} | {r['failure_mode']} {' '.join(r['flags'])}")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
