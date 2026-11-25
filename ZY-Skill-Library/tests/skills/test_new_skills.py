"""Uji skill v0.3: steam-water-properties (CoolProp), portfolio-metrics-quantstats, fsrs-scheduler, markitdown-converter.

Acuan:
- Tsat air 101.325 kPa = 99.974 C dan 1000 kPa = 179.88 C (NIST steam tables).
- Drawdown dari return [+10%, -50%]: equity 1.1 -> 0.55, drawdown 50 %.
"""
import datetime as dt
import os
import sys
import tempfile
import unittest

from _helpers import LIBRARY_ROOT

SK = os.path.join(LIBRARY_ROOT, "skills")
for rel in ("industrial-utility/steam-water-properties", "finance/portfolio-metrics-quantstats",
            "japanese-education/fsrs-scheduler", "office-documents/markitdown-converter"):
    sys.path.insert(0, os.path.join(SK, rel, "scripts"))


class SteamTests(unittest.TestCase):
    def test_saturation_matches_nist(self):
        import steam_props as s

        self.assertAlmostEqual(s.saturation(101.325)["t_sat_c"], 99.974, places=2)
        self.assertAlmostEqual(s.saturation(1000)["t_sat_c"], 179.88, places=1)
        self.assertGreater(s.saturation(1000)["hfg_kj_kg"], 0)

    def test_out_of_range_rejected(self):
        import steam_props as s

        with self.assertRaises(ValueError):
            s.saturation(30000)


class FsrsTests(unittest.TestCase):
    START = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)

    def test_good_intervals_grow(self):
        import fsrs_review as f

        seq = f.review_sequence([3, 3, 3], self.START)
        ivs = [row["interval_days"] for row in seq]
        self.assertTrue(ivs[0] < ivs[1] < ivs[2], ivs)

    def test_again_is_shorter_than_good(self):
        import fsrs_review as f

        again = f.review_sequence([1], self.START)[0]["interval_days"]
        good = f.review_sequence([3], self.START)[0]["interval_days"]
        self.assertLess(again, good)

    def test_invalid_rating(self):
        import fsrs_review as f

        with self.assertRaises(ValueError):
            f.review_sequence([5], self.START)


class PortfolioTests(unittest.TestCase):
    def test_drawdown_and_cumulative_on_known_series(self):
        import portfolio_metrics as pm

        r = pm.summarize(__import__("numpy").array([0.10, -0.50]), periods=252)
        self.assertAlmostEqual(r["max_drawdown_pct"], 50.0, places=3)  # 1.1 -> 0.55
        self.assertAlmostEqual(r["cumulative_return_pct"], -45.0, places=3)  # 1.1*0.5 - 1

    def test_csv_loader_rejects_missing_column(self):
        import portfolio_metrics as pm

        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, "r.csv")
            with open(p, "w", encoding="utf-8") as fh:
                fh.write("date,close\n2026-01-01,1\n")
            with self.assertRaises(ValueError):
                pm.load_returns(p)


class MarkitdownTests(unittest.TestCase):
    def test_docx_to_markdown_keeps_heading(self):
        from docx import Document

        import to_markdown as tm

        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, "a.docx")
            d = Document()
            d.add_heading("Laporan Uji ZY", level=1)
            d.add_paragraph("Isi paragraf.")
            d.save(p)
            text = tm.convert(p)
            self.assertIn("Laporan Uji ZY", text)
            self.assertIn("Isi paragraf.", text)


if __name__ == "__main__":
    unittest.main()
