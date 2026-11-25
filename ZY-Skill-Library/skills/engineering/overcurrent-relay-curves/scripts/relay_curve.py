"""Waktu operasi relai arus lebih inverse-time (bentuk standar IEC 60255-151).

t = TMS * k / ((I/Is)^alpha - 1)   untuk I > Is
Konstanta (k, alpha) untuk NI/VI/EI/LTI diambil dari bentuk standar IEC 60255-151.
Nilai ini belum diverifikasi terhadap dokumen standar dalam sesi ini: verifikasi
sebelum dipakai untuk setting nyata. TMS dan Is adalah setting dari studi koordinasi.
"""
from __future__ import annotations

import argparse
import json
import sys

CURVES = {"NI": (0.14, 0.02), "VI": (13.5, 1.0), "EI": (80.0, 2.0), "LTI": (120.0, 1.0)}


def operate_time_s(multiple: float, tms: float, curve: str = "NI") -> float:
    """multiple = I / Is. Mengembalikan waktu operasi (detik)."""
    if curve not in CURVES:
        raise ValueError(f"kurva harus salah satu dari {sorted(CURVES)}")
    if multiple <= 1.0:
        raise ValueError("multiple (I/Is) harus > 1; relai tidak beroperasi pada atau di bawah pickup")
    if tms <= 0:
        raise ValueError("TMS harus > 0")
    k, a = CURVES[curve]
    return tms * k / (multiple**a - 1.0)


def _main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--multiple", type=float, required=True)
    p.add_argument("--tms", type=float, required=True)
    p.add_argument("--curve", default="NI", choices=sorted(CURVES))
    a = p.parse_args(argv)
    try:
        t = operate_time_s(a.multiple, a.tms, a.curve)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"curve": a.curve, "multiple": a.multiple, "tms": a.tms, "t_operate_s": round(t, 4)}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(_main())
