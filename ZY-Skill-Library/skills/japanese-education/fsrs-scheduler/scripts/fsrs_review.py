"""Penjadwal FSRS (paket `fsrs`, MIT) untuk kartu kosakata/kanji. Alternatif lebih akurat dari SM-2.

Rating: 1 Again, 2 Hard, 3 Good, 4 Easy (sesuai enum fsrs.Rating).
Usage: python fsrs_review.py 3 3 1 3   # urutan jawaban
"""
from __future__ import annotations

import datetime as dt
import sys

from fsrs import Card, Rating, Scheduler


def review_sequence(ratings: list[int], start: dt.datetime) -> list[dict]:
    sched = Scheduler()
    card = Card()
    now = start
    out = []
    for r in ratings:
        if r not in (1, 2, 3, 4):
            raise ValueError("rating harus 1-4")
        card, _log = sched.review_card(card, Rating(r), now)
        out.append({"rating": r, "state": card.state.name, "due": card.due.isoformat(),
                    "interval_days": round((card.due - now).total_seconds() / 86400, 3)})
        now = card.due
    return out


if __name__ == "__main__":
    try:
        seq = review_sequence([int(x) for x in sys.argv[1:]],
                              dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc))
    except (ValueError, IndexError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
    for row in seq:
        print(row)
