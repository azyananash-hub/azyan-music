"""Gerbang kualitas dua lapis: TECHNICAL QC (otomatis, ffprobe) dan ARTISTIC QC (rubrik manusia).

Prinsip: lulus technical QC TIDAK berarti hasil artistik lulus. Status artistik hanya APPROVED bila
rubrik punya nama peninjau dan keputusan 'approved': true. Tanpa itu statusnya PENDING_REVIEW.
Usage:
  python qc_gate.py video.mp4 --width 1080 --height 1920 --fps 60 --duration 4 [--audio] [--rubric rubrik.json]
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from fractions import Fraction

CRITERIA = ["komposisi", "ritme", "warna", "keterbacaan_teks", "kesesuaian_brief", "kebersihan_visual"]


def probe(path: str) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", path],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def technical(path: str, width: int | None, height: int | None, fps: float | None, duration: float | None,
              tol: float, need_audio: bool) -> dict:
    data = probe(path)
    v = next((s for s in data["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in data["streams"] if s["codec_type"] == "audio"), None)
    checks = []
    if v is None:
        return {"status": "FAIL", "checks": [{"name": "video stream", "ok": False, "got": None}]}

    def chk(name, got, expected, ok):
        checks.append({"name": name, "got": got, "expected": expected, "ok": bool(ok)})

    if width is not None:
        chk("width", v["width"], width, v["width"] == width)
    if height is not None:
        chk("height", v["height"], height, v["height"] == height)
    got_fps = float(Fraction(v["r_frame_rate"]))
    if fps is not None:
        chk("fps", round(got_fps, 3), fps, math.isclose(got_fps, fps, abs_tol=0.01))
    got_dur = float(data["format"].get("duration", 0.0))
    if duration is not None:
        chk("duration_s", round(got_dur, 3), duration, abs(got_dur - duration) <= tol)
    if need_audio:
        chk("audio stream", a is not None, True, a is not None)
    ok = all(c["ok"] for c in checks)
    return {"status": "PASS" if ok else "FAIL", "checks": checks}


def artistic(rubric: dict | None) -> dict:
    if rubric is None:
        return {"status": "PENDING_REVIEW", "reason": "belum ada rubrik peninjau"}
    reviewer = str(rubric.get("reviewer", "")).strip()
    scores = rubric.get("scores", {})
    missing = [c for c in CRITERIA if c not in scores]
    if not reviewer:
        return {"status": "PENDING_REVIEW", "reason": "nama peninjau kosong"}
    if missing:
        return {"status": "PENDING_REVIEW", "reason": f"kriteria belum dinilai: {', '.join(missing)}"}
    if not all(isinstance(scores[c], int) and 1 <= scores[c] <= 5 for c in CRITERIA):
        return {"status": "PENDING_REVIEW", "reason": "skor harus bilangan bulat 1-5"}
    approved = rubric.get("approved") is True
    return {"status": "APPROVED" if approved else "REJECTED", "reviewer": reviewer,
            "average": round(sum(scores[c] for c in CRITERIA) / len(CRITERIA), 2)}


def _main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("video")
    p.add_argument("--width", type=int)
    p.add_argument("--height", type=int)
    p.add_argument("--fps", type=float)
    p.add_argument("--duration", type=float)
    p.add_argument("--duration-tol", type=float, default=0.1)
    p.add_argument("--audio", action="store_true")
    p.add_argument("--rubric")
    a = p.parse_args(argv)
    try:
        tech = technical(a.video, a.width, a.height, a.fps, a.duration, a.duration_tol, a.audio)
    except (subprocess.CalledProcessError, OSError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: tidak bisa membaca video: {exc}", file=sys.stderr)
        return 2
    rubric = None
    if a.rubric:
        with open(a.rubric, encoding="utf-8") as fh:
            rubric = json.load(fh)
    art = artistic(rubric)
    overall = f"TECH_{tech['status']} / ARTISTIC_{art['status']}"
    print(json.dumps({"technical": tech, "artistic": art, "overall": overall}, indent=2, ensure_ascii=False))
    return 0 if tech["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(_main())
