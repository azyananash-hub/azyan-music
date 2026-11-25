"""Word alignment untuk narasi: timing per kata dari audio, lalu dipetakan ke cue subtitle.

Dua sumber timing:
  1) lokal: pocketsphinx forced alignment (BSD, model bahasa Inggris ikut di paket pip).
     Audio dikonversi dulu ke PCM 16 kHz mono 16-bit lewat ffmpeg. Hanya bahasa Inggris.
  2) eksternal: file JSON [{"word": "...", "start": detik, "end": detik}] dari sumber lain
     (mis. timing dari layanan TTS atau dari penyelarasan manual).
Bahasa Jepang: BLOCKED. Tidak ada model Jepang offline yang terjangkau dari sesi ini.
Kata yang tidak ditemukan diberi timing interpolasi dan ditandai, bukan disembunyikan.
"""
from __future__ import annotations

import difflib
import json
import re
import subprocess

FRAME_S = 0.01  # pocketsphinx: 100 frame per detik


def normalize(tok: str) -> str:
    return re.sub(r"[^a-z0-9']", "", tok.lower())


def transcript_tokens(text: str) -> list[str]:
    return [t for t in (normalize(x) for x in text.split()) if t]


def pcm16k_from_audio(path: str) -> bytes:
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True)
    return out.stdout


def align_en_pocketsphinx(pcm: bytes, transcript: str) -> list[dict]:
    """Forced alignment kata. Urutan memakai Decoder(lm=None), sama dengan contoh resmi pocketsphinx."""
    import pocketsphinx as ps

    dec = ps.Decoder(lm=None)
    dec.set_align_text(transcript)
    dec.start_utt()
    dec.process_raw(pcm, False, True)
    dec.end_utt()
    skip = {"<s>", "</s>", "<sil>", "(NULL)"}
    return [{"word": normalize(s.word), "start": round(s.start_frame * FRAME_S, 3),
             "end": round(s.end_frame * FRAME_S, 3), "source": "pocketsphinx"}
            for s in dec.seg() if s.word not in skip]


def load_external(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    out = []
    for i, w in enumerate(data):
        if not {"word", "start", "end"} <= set(w):
            raise ValueError(f"entri {i} tidak punya word/start/end")
        if w["end"] < w["start"]:
            raise ValueError(f"entri {i}: end < start")
        out.append({"word": normalize(w["word"]), "start": float(w["start"]), "end": float(w["end"]),
                    "source": "external"})
    return out


def map_tokens(tokens: list[str], aligned: list[dict]) -> list[dict]:
    """Petakan token transkrip ke kata hasil alignment. Token tanpa padanan diinterpolasi dan ditandai."""
    a_words = [w["word"] for w in aligned]
    matcher = difflib.SequenceMatcher(a=tokens, b=a_words, autojunk=False)
    slot: list[dict | None] = [None] * len(tokens)
    for block in matcher.get_matching_blocks():
        for k in range(block.size):
            slot[block.a + k] = aligned[block.b + k]
    result = []
    last_end = 0.0
    for i, tok in enumerate(tokens):
        if slot[i] is not None:
            s, e, src = slot[i]["start"], slot[i]["end"], slot[i]["source"]
            last_end = e
            result.append({"token": tok, "start": s, "end": e, "source": src, "interpolated": False})
        else:
            result.append({"token": tok, "start": last_end, "end": last_end, "source": "interpolated",
                           "interpolated": True})
    return result


def cue_times(cues: list[str], mapped: list[dict]) -> list[dict]:
    """Waktu awal dan akhir setiap cue dari token yang dipetakan (urutan token dijaga)."""
    out, k = [], 0
    for text in cues:
        n = len(transcript_tokens(text))
        seg = mapped[k:k + n]
        k += n
        if not seg:
            out.append({"text": text, "start": None, "end": None})
            continue
        out.append({"text": text, "start": seg[0]["start"], "end": seg[-1]["end"],
                    "interpolated_tokens": sum(s["interpolated"] for s in seg)})
    return out
