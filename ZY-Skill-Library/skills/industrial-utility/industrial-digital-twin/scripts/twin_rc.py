"""Digital twin termal orde satu: C dT/dt = P - (T - T_amb) / R.

Solusi analitik (suhu awal T_amb): T(t) = T_amb + P R (1 - exp(-t / (R C))).
Simulasi Euler dipakai untuk memeriksa bahwa model numerik mendekati solusi analitik.
Parameter (R, C, P) harus dari data pengukuran alat Anda. Skill ini tidak menebak nilainya.
"""
from __future__ import annotations

import math


def analytic(t: float, p_w: float, r_k_per_w: float, c_j_per_k: float, t_amb: float) -> float:
    if t < 0 or r_k_per_w <= 0 or c_j_per_k <= 0:
        raise ValueError("t >= 0, R > 0, C > 0")
    return t_amb + p_w * r_k_per_w * (1 - math.exp(-t / (r_k_per_w * c_j_per_k)))


def simulate_euler(t_end: float, dt: float, p_w: float, r_k_per_w: float, c_j_per_k: float, t_amb: float) -> list[tuple[float, float]]:
    if dt <= 0 or t_end <= 0:
        raise ValueError("dt dan t_end harus > 0")
    if dt > 0.1 * r_k_per_w * c_j_per_k:
        raise ValueError("dt terlalu besar untuk stabilitas numerik (gunakan dt <= 0.1 tau)")
    t, temp = 0.0, t_amb
    out = [(t, temp)]
    while t < t_end - 1e-12:
        temp += dt * (p_w - (temp - t_amb) / r_k_per_w) / c_j_per_k
        t += dt
        out.append((round(t, 10), temp))
    return out


def steady_state(p_w: float, r_k_per_w: float, t_amb: float) -> float:
    return t_amb + p_w * r_k_per_w
