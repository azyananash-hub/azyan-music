import datetime as dt
import unittest
from urllib.parse import parse_qs, urlparse, unquote

from _helpers import POSITION, RENDER, SM2, load_module

pos = load_module("position_size", POSITION)
sm2 = load_module("sm2", SM2)
render = load_module("build_render_link", RENDER)


class PositionSizeTests(unittest.TestCase):
    def test_base_case(self):
        # equity 10000, risk 1% = 100; jarak stop 10; value 100/poin/lot -> loss/lot 1000 -> 0.1 lot
        r = pos.position_size(10000, 1, 2650, 2640, 100)
        self.assertEqual(r["risk_amount"], 100.0)
        self.assertEqual(r["units"], 0.1)
        self.assertEqual(r["direction"], "long")
        self.assertLessEqual(r["actual_risk_amount"], r["risk_amount"])

    def test_short_direction(self):
        self.assertEqual(pos.position_size(10000, 1, 2650, 2665, 100)["direction"], "short")

    def test_cap_applied_and_reported(self):
        r = pos.position_size(10000, 1, 2650, 2640, 100, max_units=0.05)
        self.assertEqual(r["units"], 0.05)
        self.assertTrue(r["capped_by_max_units"])

    def test_invalid_inputs(self):
        cases = [
            dict(equity=0, risk_pct=1, entry=2, stop=1, value_per_price_unit=100),
            dict(equity=100, risk_pct=11, entry=2, stop=1, value_per_price_unit=100),
            dict(equity=100, risk_pct=1, entry=2, stop=2, value_per_price_unit=100),
            dict(equity=100, risk_pct=1, entry=2, stop=1, value_per_price_unit=0),
            dict(equity=float("nan"), risk_pct=1, entry=2, stop=1, value_per_price_unit=100),
        ]
        for kwargs in cases:
            with self.assertRaises(ValueError, msg=str(kwargs)):
                pos.position_size(**kwargs)


class SM2Tests(unittest.TestCase):
    def test_interval_sequence_for_quality_4(self):
        s = sm2.CardState()
        s = sm2.review(s, 4)
        self.assertEqual((s.interval_days, s.repetitions), (1, 1))
        self.assertAlmostEqual(s.ease_factor, 2.5, places=9)
        s = sm2.review(s, 4)
        self.assertEqual(s.interval_days, 6)
        s = sm2.review(s, 4)
        self.assertEqual(s.interval_days, 15)  # round(6 * 2.5)

    def test_failure_resets(self):
        s = sm2.review(sm2.review(sm2.CardState(), 4), 4)
        f = sm2.review(s, 2)
        self.assertEqual((f.repetitions, f.interval_days), (0, 1))

    def test_ease_floor(self):
        s = sm2.CardState(ease_factor=1.35)
        for _ in range(10):
            s = sm2.review(s, 0)
        self.assertEqual(s.ease_factor, sm2.MIN_EF)

    def test_quality_validation(self):
        for bad in (-1, 6, 3.0, True):
            with self.assertRaises(ValueError, msg=repr(bad)):
                sm2.review(sm2.CardState(), bad)

    def test_next_due(self):
        s = sm2.CardState(ease_factor=2.5, repetitions=3, interval_days=15)
        self.assertEqual(sm2.next_due(s, dt.date(2026, 1, 1)), dt.date(2026, 1, 16))


class RenderLinkTests(unittest.TestCase):
    HTML = """<!doctype html>
<html>
  <!-- komentar dihapus -->
  <body>
    <p>Halo dunia</p>
    <script>
      const t = `baris 1
        baris 2`;
    </script>
  </body>
</html>
"""

    def test_default_horizontal_dimensions(self):
        r = render.build_link(self.HTML)
        q = parse_qs(urlparse(r["url"]).query)
        self.assertEqual(q["width"], ["1920"])
        self.assertEqual(q["height"], ["1080"])
        self.assertEqual(q["auto"], ["true"])
        self.assertTrue(r["url"].startswith("https://clipacanvas.vercel.app/render?code="))

    def test_vertical_dimensions(self):
        r = render.build_link(self.HTML, orientation="vertical")
        q = parse_qs(urlparse(r["url"]).query)
        self.assertEqual((q["width"], q["height"]), (["1080"], ["1920"]))

    def test_script_block_preserved_and_comment_removed(self):
        m = render.minify_html(self.HTML)
        self.assertNotIn("komentar dihapus", m)
        self.assertIn("baris 1\n        baris 2", m)  # isi template literal tidak berubah
        self.assertIn("<p>Halo dunia</p>", m)

    def test_round_trip_code_param(self):
        r = render.build_link(self.HTML)
        code = parse_qs(urlparse(r["url"]).query)["code"][0]
        self.assertEqual(code, r["html_minified"])

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            render.build_link(self.HTML, orientation="square")
        with self.assertRaises(ValueError):
            render.build_link("   ")
        with self.assertRaises(ValueError):
            render.build_link(self.HTML, fps=0)

    def test_words_across_lines_not_merged(self):
        self.assertIn("foo\nbar", render.minify_html("<p>foo\nbar</p>"))


if __name__ == "__main__":
    unittest.main()
