"""Uji word alignment (narration-subtitle-sync): pocketsphinx pada fixture asli + logika pemetaan."""
import importlib.util
import os
import shutil
import subprocess
import tempfile
import unittest

from _helpers import LIBRARY_ROOT

SKILL = os.path.join(LIBRARY_ROOT, "skills", "creative-production", "narration-subtitle-sync")
wa = importlib.util.module_from_spec(importlib.util.spec_from_file_location(
    "word_align", os.path.join(SKILL, "scripts", "word_align.py")))
importlib.util.spec_from_file_location("word_align", os.path.join(SKILL, "scripts", "word_align.py")).loader.exec_module(wa)
FIXTURE = os.path.join(SKILL, "tests-fixtures", "goforward_16k_s16le.raw")
AUDIO_S = 2.786  # durasi fixture (278.6 ms per 100 frame) dari 89160 byte / (16000*2)


def _has(mod):
    try:
        __import__(mod)
        return True
    except ImportError:
        return False


@unittest.skipUnless(_has("pocketsphinx"), "butuh pocketsphinx")
class PocketsphinxAlignmentTests(unittest.TestCase):
    def test_fixture_words_and_timing(self):
        with open(FIXTURE, "rb") as fh:
            pcm = fh.read()
        words = wa.align_en_pocketsphinx(pcm, "go forward ten meters")
        self.assertEqual([w["word"] for w in words], ["go", "forward", "ten", "meters"])
        starts = [w["start"] for w in words]
        self.assertEqual(starts, sorted(starts))
        self.assertTrue(all(0 <= w["start"] <= w["end"] <= AUDIO_S for w in words), words)
        # Angka acuan dari eksekusi nyata: 'meters' berakhir pada frame 211 (2.11 s).
        self.assertAlmostEqual(words[-1]["end"], 2.11, places=2)

    @unittest.skipUnless(shutil.which("ffmpeg"), "butuh ffmpeg")
    def test_audio_to_pcm_is_16k_mono(self):
        with tempfile.TemporaryDirectory() as tmp:
            wav = os.path.join(tmp, "s.wav")
            subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "sine=duration=0.5:sample_rate=44100",
                            wav], check=True)
            pcm = wa.pcm16k_from_audio(wav)
            self.assertAlmostEqual(len(pcm), 0.5 * 16000 * 2, delta=64)


class MappingTests(unittest.TestCase):
    def test_exact_match_has_no_interpolation(self):
        aligned = [{"word": w, "start": i * 0.5, "end": i * 0.5 + 0.4, "source": "external"}
                   for i, w in enumerate(["go", "forward", "ten", "meters"])]
        mapped = wa.map_tokens(wa.transcript_tokens("Go forward, ten meters."), aligned)
        self.assertFalse(any(m["interpolated"] for m in mapped))

    def test_missing_word_is_interpolated_and_monotonic(self):
        aligned = [{"word": "go", "start": 0.0, "end": 0.4, "source": "external"},
                   {"word": "meters", "start": 1.2, "end": 1.8, "source": "external"}]
        mapped = wa.map_tokens(["go", "forward", "ten", "meters"], aligned)
        flags = [m["interpolated"] for m in mapped]
        self.assertEqual(flags, [False, True, True, False])
        starts = [m["start"] for m in mapped]
        self.assertEqual(starts, sorted(starts))

    def test_cue_times_from_tokens(self):
        aligned = [{"word": w, "start": i * 0.5, "end": i * 0.5 + 0.4, "source": "external"}
                   for i, w in enumerate(["go", "forward", "ten", "meters"])]
        mapped = wa.map_tokens(wa.transcript_tokens("go forward ten meters"), aligned)
        cues = wa.cue_times(["go forward", "ten meters"], mapped)
        self.assertEqual((cues[0]["start"], cues[0]["end"]), (0.0, 0.9))
        self.assertEqual((cues[1]["start"], cues[1]["end"]), (1.0, 1.9))

    def test_external_json_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, "t.json")
            with open(p, "w", encoding="utf-8") as fh:
                fh.write('[{"word": "go", "start": 1.0}]')
            with self.assertRaises(ValueError):
                wa.load_external(p)


if __name__ == "__main__":
    unittest.main()
