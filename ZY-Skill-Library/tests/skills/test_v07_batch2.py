"""Uji v0.7 batch 2: JLPT (dataset asli), PRD (template spec-kit), SMC, backtest, dokumenter, novel, kamera 3D, narasi."""
import csv
import glob
import importlib.util
import os
import tempfile
import unittest

from _helpers import LIBRARY_ROOT

SK = os.path.join(LIBRARY_ROOT, "skills")


def mod(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(SK, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


jl = mod("jlpt_lint", "japanese-education/jlpt-curriculum/scripts/jlpt_lint.py")
pl = mod("prd_lint", "governance/prd-engineering/scripts/prd_lint.py")
bt = mod("backtest", "quantitative-trading/strategy-backtesting/scripts/backtest.py")
cl = mod("claim_ledger", "academic-research/documentary-production/scripts/claim_ledger.py")
mc = mod("manuscript_check", "office-documents/novel-typesetting/scripts/manuscript_check.py")
cp = mod("camera_path", "motion-graphics/cinematic-3d-camera/scripts/camera_path.py")
np_ = mod("narration_plan", "creative-production/elevenlabs-narration/scripts/narration_plan.py")
OJ = os.path.join(SK, "japanese-education", "jlpt-curriculum", "references", "openjlpt")
SPEC_T = os.path.join(SK, "governance", "prd-engineering", "references", "spec-kit", "spec-template.md")


class JlptTests(unittest.TestCase):
    # Jumlah entri = jumlah baris berkas dikurangi header; nilai dihitung dengan `wc -l` pada berkas asli.
    EXPECTED = {"N5": 674, "N4": 630, "N3": 1659, "N2": 1778, "N1": 3070}

    def test_counts_match_raw_files(self):
        for level, n in self.EXPECTED.items():
            path = os.path.join(OJ, f"vocab-{level.lower()}.csv")
            with open(path, encoding="utf-8", newline="") as fh:
                self.assertEqual(sum(1 for _ in csv.DictReader(fh)), n, level)

    def test_imported_dataset_lints_clean(self):
        res = jl.lint_dir(OJ)
        self.assertEqual(res["status"], "PASS", res["levels"])
        self.assertEqual(res["total_entries"], sum(self.EXPECTED.values()))

    def test_script_kind(self):
        self.assertEqual(jl.script_kind("会う"), "campuran")
        self.assertEqual(jl.script_kind("ああ"), "kana")
        self.assertEqual(jl.script_kind("東京"), "kanji")

    def test_fixture_errors_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "vocab-n5.csv"), "w", encoding="utf-8", newline="") as fh:
                w = csv.writer(fh)
                w.writerow(["id", "word", "reading", "meanings", "level"])
                w.writerow(["1", "犬", "いぬ", "dog", "N5"])
                w.writerow(["2", "猫", "neko", "cat", "N5"])       # bacaan bukan kana
                w.writerow(["3", "鳥", "とり", "", "N5"])           # arti kosong
                w.writerow(["4", "犬", "いぬ", "dog again", "N5"])  # duplikat (word, reading)
                w.writerow(["5", "魚", "さかな", "fish", "N4"])     # level tidak sesuai berkas
            res = jl.lint_dir(tmp)
            text = " | ".join(res["levels"][0]["issues"])
            for needle in ("bukan kana murni", "kosong", "duplikat", "tidak sesuai berkas"):
                self.assertIn(needle, text)


class PrdTests(unittest.TestCase):
    def test_untouched_template_fails_on_placeholders(self):
        with open(SPEC_T, encoding="utf-8") as fh:
            res = pl.lint(fh.read())
        self.assertEqual(res["status"], "FAIL")
        self.assertTrue(any("placeholder" in i for i in res["issues"]))

    FILLED = """# Feature Specification: Pengingat Latihan Kanji

## User Scenarios & Testing

### User Story 1 - Ingatkan latihan harian (Priority: P1)

Pengguna menerima pengingat pada jam yang dipilih.

## Requirements

### Functional Requirements

- **FR-001**: Sistem MUST mengirim pengingat sekali sehari pada jam pilihan pengguna.
- **FR-002**: Sistem MUST menyimpan pilihan jam per pengguna.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Pengingat terkirim dalam 60 detik dari jam yang dijadwalkan pada 99% kasus.
"""

    def test_filled_spec_passes_and_builds_handoff(self):
        res = pl.lint(self.FILLED)
        self.assertEqual(res["status"], "PASS", res["issues"])
        self.assertEqual(res["requirement_ids"], ["FR-001", "FR-002"])
        self.assertEqual(res["handoff_tasks"][0]["test"], "TEST-FR-001")

    def test_missing_section_and_unmeasurable_criterion(self):
        bad = self.FILLED.replace("## Success Criteria", "## Kriteria").replace(
            "Pengingat terkirim dalam 60 detik dari jam yang dijadwalkan pada 99% kasus.", "Pengingat terasa cepat.")
        issues = " | ".join(pl.lint(bad)["issues"])
        self.assertIn("bagian wajib hilang", issues)


class SmcTests(unittest.TestCase):
    """Data sintetis; gap dihitung dengan tangan: bullish antara high[i-2] dan low[i]."""

    def test_known_fvg_zones(self):
        import pandas as pd
        smcs = mod("smc_scan", "quantitative-trading/xauusd-smc-analysis/scripts/smc_scan.py")
        df = pd.DataFrame({"open": [9.5, 10.0, 10.8, 11.2, 11.6, 11.4, 11.0],
                           "high": [10.0, 10.6, 11.5, 11.8, 11.9, 11.6, 11.2],
                           "low": [9.2, 9.9, 10.7, 11.0, 11.3, 10.9, 10.8],
                           "close": [9.8, 10.5, 11.3, 11.4, 11.5, 11.0, 10.9]})
        res = smcs.scan(df, swing=1)
        zones = {(z["index"], z["type"]): (round(z["bottom"], 2), round(z["top"], 2)) for z in res["fvg_zones"]}
        # bullish i=1: high[0]=10.0 .. low[2]=10.7 ; bullish i=2: high[1]=10.6 .. low[3]=11.0
        # bearish i=5: low[4]=11.3 .. high[6]=11.2 (gap 11.2-11.3)
        self.assertEqual(zones[(1, "bullish")], (10.0, 10.7))
        self.assertEqual(zones[(2, "bullish")], (10.6, 11.0))
        self.assertEqual(zones[(5, "bearish")], (11.2, 11.3))
        self.assertEqual(len(res["fvg_zones"]), 3)

    def test_missing_column_rejected(self):
        import pandas as pd
        smcs = mod("smc_scan", "quantitative-trading/xauusd-smc-analysis/scripts/smc_scan.py")
        with self.assertRaises(ValueError):
            smcs.scan(pd.DataFrame({"close": [1, 2]}))


class BacktestTests(unittest.TestCase):
    """MA(1,2): sinyal t=1,2 dan 5,6,7 = 1. Entri di OPEN t+1 (bukan close t). Open bar 2 sengaja 3.5."""

    def test_trades_use_next_bar_open(self):
        closes = [1, 2, 3, 2, 1, 2, 3, 4]
        opens = [1, 2, 3.5, 2, 1, 2, 3, 4]
        r = bt.run(opens, closes, 1, 2)
        self.assertEqual(r["trade_count"], 2)
        self.assertAlmostEqual(r["trades"][0]["entry"], 3.5)     # open bar 2, bukan close bar 1 (=2)
        self.assertAlmostEqual(r["trades"][0]["return"], 1 / 3.5 - 1, places=6)
        self.assertAlmostEqual(r["trades"][1]["return"], 4 / 3 - 1, places=6)
        self.assertAlmostEqual(r["total_return"], (1 + (1 / 3.5 - 1)) * (4 / 3) - 1, places=6)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            bt.crossover_signal([1, 2, 3], 3, 2)
        with self.assertRaises(ValueError):
            bt.run([1], [1], 1, 2)


class DocumentaryTests(unittest.TestCase):
    SOURCES = [{"id": "S1", "title": "Arsip", "type": "primary", "citation": "Arsip A, 1999", "url": "https://x.example/a"},
               {"id": "S2", "title": "Buku", "type": "secondary", "citation": "Penulis B, 2010", "url": "https://x.example/b"}]

    def test_complete_ledger_passes(self):
        doc = {"sources": self.SOURCES, "claims": [{"id": "C1", "text": "Tanggal kejadian", "source_ids": ["S1"], "status": "verified"},
                                                  {"id": "C2", "text": "Latar", "source_ids": ["S2"], "status": "unverified"}]}
        self.assertEqual(cl.audit(doc)["status"], "PASS")

    def test_unsourced_and_unknown_claims_are_errors(self):
        doc = {"sources": self.SOURCES, "claims": [{"id": "C1", "text": "x", "source_ids": []},
                                                  {"id": "C2", "text": "y", "source_ids": ["S9"]}]}
        res = cl.audit(doc)
        self.assertEqual(res["status"], "FAIL")
        self.assertEqual(len(res["errors"]), 2)

    def test_verified_without_primary_source_warns(self):
        doc = {"sources": self.SOURCES, "claims": [{"id": "C2", "text": "y", "source_ids": ["S2"], "status": "verified"}]}
        res = cl.audit(doc)
        self.assertTrue(any("sumber primer" in w for w in res["warnings"]))


class NovelTests(unittest.TestCase):
    TEXT = "Bab 1 Awal\nSatu dua tiga empat.\nLima enam.\n\nBab 2 Lanjut\nTujuh delapan sembilan.\n"

    def test_numbering_and_word_counts(self):
        chapters = mc.parse(self.TEXT)
        res = mc.check(chapters, "words", 0)
        self.assertEqual(res["status"], "PASS")
        self.assertEqual([c["count"] for c in res["chapters"]], [6, 3])

    def test_gap_in_numbering_fails(self):
        res = mc.check(mc.parse(self.TEXT.replace("Bab 2", "Bab 3")))
        self.assertEqual(res["status"], "FAIL")

    def test_docx_export_keeps_chapter_headings(self):
        from docx import Document
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "n.docx")
            mc.to_docx(mc.parse(self.TEXT), out)
            heads = [p.text for p in Document(out).paragraphs if p.style.name.startswith("Heading")]
            self.assertEqual(heads, ["Bab 1 Awal", "Bab 2 Lanjut"])

    def test_text_before_first_chapter_rejected(self):
        with self.assertRaises(ValueError):
            mc.parse("pembuka tanpa bab\nBab 1 X\nisi")


class CameraTests(unittest.TestCase):
    KEYS = [{"t": 0, "pos": [0, 0, 0]}, {"t": 1, "pos": [1, 0, 0]}, {"t": 2, "pos": [1, 1, 0]}, {"t": 3, "pos": [0, 1, 0]}]

    def test_passes_through_keyframes_and_frame_count(self):
        s = cp.sample(self.KEYS, fps=60)
        self.assertEqual(len(s), 3 * 60 + 1)
        at1 = next(f for f in s if abs(f["t"] - 1.0) < 1e-9)
        self.assertEqual(at1["pos"], [1.0, 0.0, 0.0])

    def test_c1_continuity_at_keyframe(self):
        eps = 1e-4
        left = cp.catmull_rom([0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], 1 - eps)
        right = cp.catmull_rom([1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 1, 0], eps)
        for a, b in zip(left, right):
            self.assertLess(abs(a - b), 1e-3)

    def test_non_increasing_time_rejected(self):
        with self.assertRaises(ValueError):
            cp.sample([{"t": 0, "pos": [0, 0, 0]}, {"t": 0, "pos": [1, 0, 0]}])


class NarrationTests(unittest.TestCase):
    def test_credit_estimate_matches_observed_elevenlabs_estimate(self):
        # Bukti: estimate_only untuk "これはテストです。" (9 karakter), 2 generasi = 18 kredit.
        r = np_.plan("これはテストです。", used=297, limit=10000, generations=2)
        self.assertEqual(r["total_chars"], 9)
        self.assertEqual(r["credits_estimate"], 18)
        self.assertEqual(r["status"], "OK")

    def test_quota_refusal_instead_of_buying_credits(self):
        r = np_.plan("これはテストです。", used=9995, limit=10000, generations=2)
        self.assertEqual(r["status"], "ERROR_KUOTA_TIDAK_CUKUP")

    def test_segments_split_by_sentence_and_paragraph(self):
        segs = np_.split_segments("Kalimat satu. Kalimat dua.\n\nParagraf dua。")
        self.assertEqual(len(segs), 3)


if __name__ == "__main__":
    unittest.main()
