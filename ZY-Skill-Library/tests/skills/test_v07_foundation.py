"""Uji v0.7 fondasi: technology-selection (aturan deterministik) dan quality-gate (ffmpeg nyata)."""
import importlib.util
import os
import shutil
import subprocess
import tempfile
import unittest

from _helpers import LIBRARY_ROOT

GOV = os.path.join(LIBRARY_ROOT, "skills", "governance")


def mod(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(GOV, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


tech = mod("select_tech", "technology-selection/scripts/select_tech.py")
qc = mod("qc_gate", "quality-gate/scripts/qc_gate.py")


class TechSelectionTests(unittest.TestCase):
    def test_vertical_text_heavy_2d_prefers_remotion(self):
        top = tech.select(["2d", "text-heavy", "vertical"], "broadcast")[0]
        self.assertEqual(top["option"], "remotion")
        self.assertEqual(top["needs_missing"], [])

    def test_3d_interactive_prefers_threejs(self):
        top = tech.select(["3d", "interactive", "vertical"], "cinematic")[0]
        self.assertEqual(top["option"], "threejs")

    def test_quality_shortfall_is_reported_not_hidden(self):
        rows = {r["option"]: r for r in tech.select(["2d", "text-heavy"], "cinematic")}
        self.assertFalse(rows["remotion"]["quality_target_met"])  # quality_max = broadcast

    def test_invalid_quality_rejected(self):
        with self.assertRaises(ValueError):
            tech.select(["2d"], "ultra")


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "butuh ffmpeg/ffprobe")
class QcGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.video = os.path.join(cls.tmp, "v.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc=size=1080x1920:rate=60:duration=4",
                        "-f", "lavfi", "-i", "sine=frequency=440:duration=4", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-shortest", cls.video], check=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_correct_spec_passes_technical(self):
        r = qc.technical(self.video, 1080, 1920, 60, 4, 0.1, True)
        self.assertEqual(r["status"], "PASS", r)

    def test_wrong_fps_fails_technical(self):
        r = qc.technical(self.video, 1080, 1920, 30, 4, 0.1, True)
        self.assertEqual(r["status"], "FAIL")
        self.assertTrue(any(c["name"] == "fps" and not c["ok"] for c in r["checks"]))

    def test_wrong_duration_fails_technical(self):
        r = qc.technical(self.video, 1080, 1920, 60, 3, 0.1, True)
        self.assertEqual(r["status"], "FAIL")

    def test_passing_technical_does_not_imply_artistic_approval(self):
        self.assertEqual(qc.technical(self.video, 1080, 1920, 60, 4, 0.1, True)["status"], "PASS")
        self.assertEqual(qc.artistic(None)["status"], "PENDING_REVIEW")

    def test_artistic_requires_reviewer_and_all_criteria(self):
        full = {c: 4 for c in qc.CRITERIA}
        self.assertEqual(qc.artistic({"reviewer": "", "scores": full, "approved": True})["status"], "PENDING_REVIEW")
        self.assertEqual(qc.artistic({"reviewer": "Zyan", "scores": {"komposisi": 4}, "approved": True})["status"],
                         "PENDING_REVIEW")
        self.assertEqual(qc.artistic({"reviewer": "Zyan", "scores": full, "approved": True})["status"], "APPROVED")
        self.assertEqual(qc.artistic({"reviewer": "Zyan", "scores": full, "approved": False})["status"], "REJECTED")


if __name__ == "__main__":
    unittest.main()
