"""Uji skill IMPORTED: skill-creator (governance), slack-gif-creator, dan webapp-testing."""

import os
import subprocess
import sys
import tempfile
import unittest

from _helpers import LIBRARY_ROOT

SKILLS = os.path.join(LIBRARY_ROOT, "skills")
QUICK_VALIDATE = os.path.join(SKILLS, "governance", "skill-creator", "scripts", "quick_validate.py")
SLACK_DIR = os.path.join(SKILLS, "creative-production", "slack-gif-creator")
WEBAPP_DIR = os.path.join(SKILLS, "software-development", "webapp-testing")
CHROMIUM = "/opt/pw-browsers/chromium-1243/chrome-linux64/chrome"
PLAYWRIGHT_PY = os.environ.get("ZY_PLAYWRIGHT_PYTHON", sys.executable)


def _has(module: str) -> bool:
    try:
        __import__(module)
        return True
    except ImportError:
        return False


class SkillCreatorTests(unittest.TestCase):
    def _skill(self, root, name, frontmatter):
        d = os.path.join(root, name)
        os.makedirs(d)
        with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8") as fh:
            fh.write(frontmatter + "\n\n# Body\n")
        return d

    @unittest.skipUnless(_has("yaml"), "butuh PyYAML (dipakai quick_validate upstream)")
    def test_accepts_valid_and_rejects_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            ok = self._skill(tmp, "good-skill", "---\nname: good-skill\ndescription: Does a real thing.\n---")
            bad = self._skill(tmp, "bad-skill", "---\nname: Bad Skill!\ndescription: x\n---")
            r_ok = subprocess.run([sys.executable, QUICK_VALIDATE, ok], capture_output=True, text=True)
            r_bad = subprocess.run([sys.executable, QUICK_VALIDATE, bad], capture_output=True, text=True)
            self.assertEqual(r_ok.returncode, 0, r_ok.stdout + r_ok.stderr)
            self.assertIn("valid", r_ok.stdout.lower())
            self.assertNotEqual(r_bad.returncode, 0, r_bad.stdout + r_bad.stderr)


@unittest.skipUnless(_has("imageio") or _has("PIL"), "butuh PIL")
class SlackGifTests(unittest.TestCase):
    def test_builds_valid_emoji_gif(self):
        import numpy as np

        sys.path.insert(0, SLACK_DIR)
        try:
            from core.gif_builder import GIFBuilder
            from core.validators import validate_gif
        except ImportError as exc:  # dependensi (imageio/numpy) belum ada
            self.skipTest(f"dependensi slack-gif-creator hilang: {exc}")
        finally:
            sys.path.remove(SLACK_DIR)

        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "pulse.gif")
            builder = GIFBuilder(width=128, height=128, fps=12)
            for i in range(12):
                frame = np.zeros((128, 128, 3), dtype=np.uint8)
                radius = 10 + i * 4
                yy, xx = np.ogrid[:128, :128]
                mask = (xx - 64) ** 2 + (yy - 64) ** 2 <= radius**2
                frame[mask] = (255, 80 + i * 10, 60)
                builder.add_frame(frame)
            info = builder.save(out, num_colors=64, optimize_for_emoji=True)
            self.assertTrue(os.path.isfile(out))
            ok, report = validate_gif(out, is_emoji=True, verbose=False)
            self.assertTrue(ok, report)
            self.assertLess(os.path.getsize(out), 64 * 1024)  # batas emoji Slack 64 KB (verifikasi ulang batas terbaru)


@unittest.skipUnless(_has("playwright") and os.path.exists(CHROMIUM), "butuh playwright (venv) dan Chromium")
class WebappTests(unittest.TestCase):
    def test_with_server_runs_page_check(self):
        """with_server.py menjalankan server statis, lalu skrip Playwright memeriksa judul halaman."""
        with tempfile.TemporaryDirectory() as tmp:
            site = os.path.join(tmp, "site")
            os.makedirs(site)
            with open(os.path.join(site, "index.html"), "w", encoding="utf-8") as fh:
                fh.write("<!doctype html><title>ZY Uji</title><button id='go'>Mulai</button>")
            check = os.path.join(tmp, "check.py")
            with open(check, "w", encoding="utf-8") as fh:
                fh.write(
                    "from playwright.sync_api import sync_playwright\n"
                    "import sys\n"
                    "with sync_playwright() as p:\n"
                    f"    b = p.chromium.launch(executable_path={CHROMIUM!r}, args=['--no-sandbox'])\n"
                    "    pg = b.new_page()\n"
                    "    pg.goto('http://localhost:8765/index.html')\n"
                    "    print('TITLE=' + pg.title())\n"
                    "    print('BUTTON=' + pg.inner_text('#go'))\n"
                    "    b.close()\n"
                )
            script = os.path.join(WEBAPP_DIR, "scripts", "with_server.py")
            r = subprocess.run(
                [sys.executable, script, "--server", f"{sys.executable} -m http.server 8765 --directory {site}",
                 "--port", "8765", "--timeout", "30", "--", PLAYWRIGHT_PY, check],
                capture_output=True, text=True, timeout=300,
            )
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("TITLE=ZY Uji", r.stdout)
            self.assertIn("BUTTON=Mulai", r.stdout)


if __name__ == "__main__":
    unittest.main()
