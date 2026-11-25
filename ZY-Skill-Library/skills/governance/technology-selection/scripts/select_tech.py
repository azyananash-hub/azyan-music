"""Pilih teknologi produksi berdasarkan kebutuhan dan target kualitas (aturan deterministik).

Skor = jumlah kebutuhan yang didukung + syarat kualitas. Opsi yang tidak memenuhi target kualitas
diberi tanda. Keluaran menyebut kebutuhan yang tidak terpenuhi, supaya keputusan tidak tersembunyi.
Matriks di references/tech-matrix.json adalah penilaian kualitatif, bukan benchmark.
Usage: python select_tech.py --need 2d --need text-heavy --need vertical --quality broadcast
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load_matrix(path: str | None = None) -> dict:
    path = path or os.path.join(HERE, "..", "references", "tech-matrix.json")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def select(needs: list[str], quality: str, matrix: dict | None = None) -> list[dict]:
    m = matrix or load_matrix()
    rank = m["quality_rank"]
    if quality not in rank:
        raise ValueError(f"quality harus salah satu dari {sorted(rank)}")
    results = []
    for name, opt in m["options"].items():
        met = [n for n in needs if n in opt["supports"]]
        missing = [n for n in needs if n not in opt["supports"]]
        quality_ok = rank[opt["quality_max"]] >= rank[quality]
        score = len(met) - (0 if not needs else len(missing) / len(needs)) * 0.5
        if not quality_ok:
            score -= 2.0  # target kualitas tidak tercapai: turun jauh, tetapi tetap ditampilkan
        results.append({"option": name, "score": round(score, 3), "needs_met": met, "needs_missing": missing,
                        "quality_target_met": quality_ok, "requires": opt["requires"], "skill": opt["skill"],
                        "skill_status": opt["skill_status"]})
    results.sort(key=lambda r: r["score"], reverse=True)
    return results


def _main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--need", action="append", default=[], help="kebutuhan (boleh diulang), mis. 3d, vertical")
    p.add_argument("--quality", default="broadcast", choices=["draft", "broadcast", "cinematic"])
    a = p.parse_args(argv)
    if not a.need:
        p.error("beri minimal satu --need")
    try:
        res = select(a.need, a.quality)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(_main())
