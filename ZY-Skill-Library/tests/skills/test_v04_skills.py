"""Uji terarah v0.4: skill ffmpeg-skill (recipe nyata) dan provenance 30 skill impor baru."""
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest

from _helpers import LIBRARY_ROOT

SKILLS = os.path.join(LIBRARY_ROOT, "skills")


def _probe(path, entries):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", entries, "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout.strip()
    return out


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "butuh ffmpeg/ffprobe")
class FfmpegSkillTests(unittest.TestCase):
    def test_version_meets_skill_requirement(self):
        """SKILL.md mensyaratkan FFmpeg 6.1+."""
        v = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True).stdout
        m = re.search(r"ffmpeg version (\d+)\.(\d+)", v)
        self.assertIsNotNone(m, v[:80])
        self.assertGreaterEqual((int(m.group(1)), int(m.group(2))), (6, 1))

    def test_trim_and_vertical_reframe_recipes(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "src.mp4")
            subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc=duration=3:size=1280x720:rate=25",
                            "-pix_fmt", "yuv420p", src], check=True)
            trimmed = os.path.join(tmp, "trim.mp4")
            subprocess.run(["ffmpeg", "-v", "error", "-ss", "0", "-t", "1", "-i", src, "-c", "copy", trimmed], check=True)
            self.assertAlmostEqual(float(_probe(trimmed, "format=duration")), 1.0, delta=0.15)
            vert = os.path.join(tmp, "vert.mp4")
            subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vf", "scale=-2:1920,crop=1080:1920",
                            "-c:v", "libx264", "-crf", "30", vert], check=True)
            self.assertEqual(_probe(vert, "stream=width,height").split(",")[:2], ["1080", "1920"])


class ImportProvenanceTests(unittest.TestCase):
    def test_all_v04_imports_have_skill_md_license_and_source(self):
        with open(os.path.join(LIBRARY_ROOT, "research", "import-manifest.json"), encoding="utf-8") as fh:
            entries = json.load(fh)["entries"]
        new = [e for e in entries if e.get("source_commit", "") and e["license"] == "MIT"
               and e["imported_on"] == entries[-1]["imported_on"] and e["name"] not in
               ("remotion-motion-graphics-x",)]
        self.assertGreaterEqual(len(new), 30)
        for e in new:
            folder = os.path.join(LIBRARY_ROOT, e["library_path"])
            self.assertTrue(os.path.isfile(os.path.join(folder, "SKILL.md")), e["name"])
            self.assertTrue(os.path.isfile(os.path.join(folder, "LICENSE")), e["name"])
            self.assertTrue(os.path.isfile(os.path.join(folder, "SOURCE.md")), e["name"])


if __name__ == "__main__":
    unittest.main()
