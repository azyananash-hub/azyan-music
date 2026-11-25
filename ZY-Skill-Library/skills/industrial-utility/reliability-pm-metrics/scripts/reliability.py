"""Metrik keandalan untuk preventive maintenance: availability dan Weibull.

Availability (inherent) A = MTBF / (MTBF + MTTR)
Weibull reliability R(t) = exp(-(t/eta)^beta), eta skala, beta bentuk (beta > 1: wear-out).
Parameter eta dan beta harus dari fitting data kegagalan Anda, bukan asumsi.
"""
from __future__ import annotations

import argparse
import json
import math
import sys


def availability(mtbf_h: float, mttr_h: float) -> float:
    if mtbf_h <= 0 or mttr_h < 0:
        raise ValueError("MTBF > 0 dan MTTR >= 0")
    return mtbf_h / (mtbf_h + mttr_h)


def weibull_reliability(t: float, eta: float, beta: float) -> float:
    if t < 0 or eta <= 0 or beta <= 0:
        raise ValueError("t >= 0, eta > 0, beta > 0")
    return math.exp(-((t / eta) ** beta))


def _main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--mtbf", type=float)
    p.add_argument("--mttr", type=float)
    p.add_argument("--t", type=float)
    p.add_argument("--eta", type=float)
    p.add_argument("--beta", type=float)
    a = p.parse_args(argv)
    out = {}
    try:
        if a.mtbf is not None and a.mttr is not None:
            out["availability"] = round(availability(a.mtbf, a.mttr), 6)
        if None not in (a.t, a.eta, a.beta):
            out["weibull_reliability"] = round(weibull_reliability(a.t, a.eta, a.beta), 6)
        if not out:
            p.error("beri --mtbf/--mttr dan/atau --t/--eta/--beta")
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(_main())
