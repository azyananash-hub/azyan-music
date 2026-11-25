"""Mass balance Reverse Osmosis (RO) untuk Water Treatment Plant (WTP).

Definisi:
  recovery (%)  = Q_permeate / Q_feed * 100
  rejection (%) = (1 - C_permeate / C_feed) * 100
  Q_concentrate = Q_feed - Q_permeate                  (neraca massa air)
  C_concentrate = (Q_feed*C_feed - Q_perm*C_perm) / Q_concentrate   (neraca massa garam)

Peringatan: recovery terlalu tinggi meningkatkan risiko scaling/fouling. Batas recovery dan
antiscalant harus sesuai rekomendasi membran pabrikan. Script ini tidak menggantikan
proyeksi software vendor (mis. ROSA/IMSDesign).
"""

from __future__ import annotations

import argparse
import json
import sys


def mass_balance(q_feed: float, c_feed: float, q_perm: float, c_perm: float) -> dict:
    if q_feed <= 0 or c_feed <= 0:
        raise ValueError("q_feed dan c_feed harus > 0")
    if not 0 < q_perm < q_feed:
        raise ValueError("q_perm harus di (0, q_feed)")
    if not 0 <= c_perm < c_feed:
        raise ValueError("c_perm harus di [0, c_feed)")
    q_conc = q_feed - q_perm
    c_conc = (q_feed * c_feed - q_perm * c_perm) / q_conc
    recovery = q_perm / q_feed * 100.0
    rejection = (1.0 - c_perm / c_feed) * 100.0
    # Pemeriksaan: neraca garam harus tertutup
    salt_in = q_feed * c_feed
    salt_out = q_perm * c_perm + q_conc * c_conc
    return {
        "recovery_pct": round(recovery, 3),
        "rejection_pct": round(rejection, 3),
        "q_concentrate": round(q_conc, 6),
        "c_concentrate": round(c_conc, 4),
        "salt_balance_error": round(salt_in - salt_out, 9),
        "note": "Neraca massa ideal; tidak memodelkan polarisasi konsentrasi atau tekanan osmotik.",
    }


def _main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--q-feed", type=float, required=True, help="Debit feed (m3/h)")
    p.add_argument("--c-feed", type=float, required=True, help="TDS feed (mg/L)")
    p.add_argument("--q-perm", type=float, required=True, help="Debit permeate (m3/h)")
    p.add_argument("--c-perm", type=float, required=True, help="TDS permeate (mg/L)")
    args = p.parse_args(argv)
    try:
        r = mass_balance(args.q_feed, args.c_feed, args.q_perm, args.c_perm)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(r, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(_main())
