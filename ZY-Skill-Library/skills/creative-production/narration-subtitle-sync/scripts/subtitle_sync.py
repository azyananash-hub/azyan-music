"""Sinkronisasi subtitle SRT ke durasi audio narasi, validasi, dan pengukuran loudness.

Narasi bisa berasal dari: rekaman pengguna, audio eksternal, atau TTS yang sudah Anda sediakan.
Skill ini TIDAK mengunduh model TTS. Durasi audio diukur dengan ffprobe (jika tersedia).
Batas kecepatan baca (cps) adalah parameter yang Anda tetapkan, bukan standar yang dikutip di sini.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys

TIME_RE = re.compile(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})")


def _to_ms(s: str) -> int:
    m = TIME_RE.fullmatch(s.strip())
    if not m:
        raise ValueError(f"timestamp SRT tidak valid: {s!r}")
    h, mi, se, ms = map(int, m.groups())
    return ((h * 60 + mi) * 60 + se) * 1000 + ms


def _fmt(ms: int) -> str:
    h, rem = divmod(ms, 3600_000)
    mi, rem = divmod(rem, 60_000)
    se, ms = divmod(rem, 1000)
    return f"{h:02d}:{mi:02d}:{se:02d},{ms:03d}"


def parse_srt(text: str) -> list[dict]:
    blocks = [b for b in re.split(r"\n\s*\n", text.strip()) if b.strip()]
    cues = []
    for b in blocks:
        lines = b.strip().splitlines()
        if len(lines) < 2:
            raise ValueError("blok SRT terlalu pendek")
        idx = 1 if "-->" not in lines[0] else 0
        start, end = (x.strip() for x in lines[idx].split("-->"))
        cues.append({"start": _to_ms(start), "end": _to_ms(end), "text": "\n".join(lines[idx + 1:])})
    return cues


def to_srt(cues: list[dict]) -> str:
    parts = [f"{i}\n{_fmt(c['start'])} --> {_fmt(c['end'])}\n{c['text']}" for i, c in enumerate(cues, 1)]
    return "\n\n".join(parts) + "\n"


def scale_to_duration(cues: list[dict], audio_ms: int) -> list[dict]:
    if not cues:
        raise ValueError("tidak ada cue")
    total = cues[-1]["end"]
    if total <= 0:
        raise ValueError("durasi subtitle nol")
    f = audio_ms / total
    return [{**c, "start": round(c["start"] * f), "end": round(c["end"] * f)} for c in cues]


def validate(cues: list[dict], max_cps: float = 17.0) -> list[str]:
    issues = []
    for i, c in enumerate(cues, 1):
        if c["end"] <= c["start"]:
            issues.append(f"cue {i}: end <= start")
        dur_s = (c["end"] - c["start"]) / 1000
        chars = len(c["text"].replace("\n", ""))
        if dur_s > 0 and chars / dur_s > max_cps:
            issues.append(f"cue {i}: {chars / dur_s:.1f} karakter/detik > {max_cps} (parameter Anda)")
        if i > 1 and c["start"] < cues[i - 2]["end"]:
            issues.append(f"cue {i}: overlap dengan cue {i - 1}")
    return issues


def audio_duration_ms(path: str) -> int | None:
    if not shutil.which("ffprobe"):
        return None
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", path], capture_output=True, text=True, check=True).stdout
    return round(float(out.strip()) * 1000)


def loudness(path: str) -> dict:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af",
                        "loudnorm=print_format=json", "-f", "null", "-"], capture_output=True, text=True)
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr)
    if not m:
        raise RuntimeError("ffmpeg tidak mengembalikan pengukuran loudnorm")
    d = json.loads(m.group(0))
    return {"integrated_lufs": float(d["input_i"]), "true_peak_dbtp": float(d["input_tp"]),
            "loudness_range_lu": float(d["input_lra"])}


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("srt")
    p.add_argument("--audio", help="file audio narasi untuk menyesuaikan durasi")
    p.add_argument("--max-cps", type=float, default=17.0)
    p.add_argument("--out")
    a = p.parse_args()
    try:
        with open(a.srt, encoding="utf-8") as fh:
            cues = parse_srt(fh.read())
        if a.audio:
            dur = audio_duration_ms(a.audio)
            if dur is None:
                raise RuntimeError("ffprobe tidak tersedia")
            cues = scale_to_duration(cues, dur)
        issues = validate(cues, a.max_cps)
        if a.out:
            with open(a.out, "w", encoding="utf-8") as fh:
                fh.write(to_srt(cues))
        print(json.dumps({"cues": len(cues), "issues": issues}, indent=2, ensure_ascii=False))
        if a.audio:
            print(json.dumps(loudness(a.audio), indent=2))
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
