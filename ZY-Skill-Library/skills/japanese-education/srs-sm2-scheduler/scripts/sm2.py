"""Penjadwal spaced repetition SM-2 (SuperMemo 2, 1987) untuk kartu kosakata/kanji.

Catatan:
  - SM-2 adalah algoritma publik dan sederhana. Untuk produksi jangka panjang, FSRS
    (open-spaced-repetition, lisensi MIT pada repo fsrs4anki) lebih akurat; modul ini
    dirancang agar mudah diganti.
  - Kualitas jawaban q (0-5):
      5 sempurna, 4 benar dengan ragu, 3 benar sulit,
      2 salah tetapi terasa dekat, 1 salah, 0 blank.
    q < 3 dianggap gagal dan mengulang kartu dari awal.

State kartu: ease_factor (EF, min 1.3), repetitions, interval_days.
"""

from __future__ import annotations

import datetime as _dt
import math
from dataclasses import dataclass, asdict

MIN_EF = 1.3


@dataclass(frozen=True)
class CardState:
    ease_factor: float = 2.5
    repetitions: int = 0
    interval_days: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


def review(state: CardState, quality: int) -> CardState:
    """Terapkan satu review dan kembalikan state baru (immutable)."""
    if not isinstance(quality, int) or isinstance(quality, bool) or not 0 <= quality <= 5:
        raise ValueError("quality harus bilangan bulat 0-5")

    ef = state.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    ef = max(MIN_EF, ef)

    if quality < 3:
        return CardState(ease_factor=ef, repetitions=0, interval_days=1)

    reps = state.repetitions + 1
    if reps == 1:
        interval = 1
    elif reps == 2:
        interval = 6
    else:
        # SM-2 memakai EF yang sudah diperbarui untuk review ini; pembulatan half-up.
        interval = max(1, int(math.floor(state.interval_days * ef + 0.5)))
    return CardState(ease_factor=ef, repetitions=reps, interval_days=interval)


def next_due(state: CardState, reviewed_on: _dt.date) -> _dt.date:
    return reviewed_on + _dt.timedelta(days=state.interval_days)
