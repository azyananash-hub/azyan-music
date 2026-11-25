"""Mekanik game: progresi XP untuk aplikasi belajar (streak, level) dan peluruhan sumber daya survival.

XP per jawaban  = base * min(1 + streak * per_streak, cap)
Ambang level n  = base_level * n * (n - 1) / 2  (total XP untuk mencapai level n; level 1 = 0 XP)
Survival        = nilai berkurang linear 'rate' per detik, dibatasi di [0, 100]
Nilai default adalah parameter desain, bukan standar; atur sesuai playtest Anda.
"""
from __future__ import annotations

import math


def xp_for_answer(base: float, streak: int, per_streak: float = 0.1, cap: float = 2.0) -> float:
    if base < 0 or streak < 0 or per_streak < 0 or cap < 1:
        raise ValueError("parameter XP tidak valid")
    return base * min(1.0 + streak * per_streak, cap)


def level_threshold(level: int, base_level: float = 100.0) -> float:
    if level < 1:
        raise ValueError("level minimal 1")
    return base_level * level * (level - 1) / 2.0


def level_for_xp(xp: float, base_level: float = 100.0) -> int:
    if xp < 0:
        raise ValueError("xp tidak boleh negatif")
    level = 1
    while level_threshold(level + 1, base_level) <= xp:
        level += 1
    return level


def survival_value(start: float, rate_per_s: float, seconds: float) -> float:
    if seconds < 0:
        raise ValueError("durasi tidak boleh negatif")
    return min(100.0, max(0.0, start - rate_per_s * seconds))


def seconds_until_empty(start: float, rate_per_s: float) -> float:
    if rate_per_s <= 0:
        return math.inf
    return max(0.0, start) / rate_per_s
