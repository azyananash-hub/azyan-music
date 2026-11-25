"""Jalur kamera 3D halus dari keyframe memakai Catmull-Rom (uniform, melewati setiap keyframe).

Untuk setiap segmen [P_i, P_{i+1}] dipakai tetangga P_{i-1} dan P_{i+2} (diduplikasi di ujung).
Turunan kiri dan kanan di keyframe sama, sehingga gerak kamera tidak patah.
Keyframe: [{"t": detik, "pos": [x, y, z]}, ...] dengan t naik. Sampling: fps tetap.
"""
from __future__ import annotations


def catmull_rom(p0, p1, p2, p3, u: float):
    out = []
    for k in range(3):
        a, b, c, d = p0[k], p1[k], p2[k], p3[k]
        out.append(0.5 * ((2 * b) + (-a + c) * u + (2 * a - 5 * b + 4 * c - d) * u * u + (-a + 3 * b - 3 * c + d) * u ** 3))
    return out


def sample(keyframes: list[dict], fps: float = 60.0) -> list[dict]:
    if len(keyframes) < 2:
        raise ValueError("minimal dua keyframe")
    times = [k["t"] for k in keyframes]
    if any(b <= a for a, b in zip(times, times[1:])):
        raise ValueError("waktu keyframe harus naik ketat")
    pts = [k["pos"] for k in keyframes]
    out = []
    n = int(round((times[-1] - times[0]) * fps))
    for f in range(n + 1):
        t = times[0] + f / fps
        seg = max(i for i in range(len(times) - 1) if times[i] <= t + 1e-12)
        seg = min(seg, len(times) - 2)
        u = (t - times[seg]) / (times[seg + 1] - times[seg])
        p0 = pts[max(seg - 1, 0)]
        p1 = pts[seg]
        p2 = pts[seg + 1]
        p3 = pts[min(seg + 2, len(pts) - 1)]
        out.append({"t": round(t, 6), "pos": [round(v, 6) for v in catmull_rom(p0, p1, p2, p3, min(max(u, 0.0), 1.0))]})
    return out
