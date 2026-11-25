"""Uji v0.7 batch 1: storyboard, manhwa, game mechanics, multi-agent, digital twin, SCADA, troubleshooting."""
import importlib.util
import os
import unittest

from _helpers import LIBRARY_ROOT

SK = os.path.join(LIBRARY_ROOT, "skills")


def mod(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(SK, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


sb = mod("storyboard_lint", "creative-production/cinematic-storyboarding/scripts/storyboard_lint.py")
pc = mod("panel_check", "creative-production/manhwa-production/scripts/panel_check.py")
gm = mod("mechanics", "software-development/game-mechanics/scripts/mechanics.py")
tg = mod("task_graph", "software-development/multi-agent-orchestration/scripts/task_graph.py")
tw = mod("twin_rc", "industrial-utility/industrial-digital-twin/scripts/twin_rc.py")
tc = mod("tag_check", "automation/scada-tag-engineering/scripts/tag_check.py")
ft = mod("fault_tree", "engineering/electrical-troubleshooting/scripts/fault_tree.py")

GOOD_SB = {"target_s": 8, "allowed_camera": ["static", "dolly-in"],
           "characters": {"ZYAN": {"name": "Zyan", "costume": "jaket hitam", "palette": "abu-abu"}},
           "shots": [{"id": "S1", "duration_s": 4, "camera": "static", "characters": ["ZYAN"]},
                     {"id": "S2", "duration_s": 4, "camera": "dolly-in", "characters": ["ZYAN"]}]}


class StoryboardTests(unittest.TestCase):
    def test_consistent_storyboard_passes(self):
        self.assertEqual(sb.lint(GOOD_SB), [])

    def test_unknown_character_camera_and_duration(self):
        bad = dict(GOOD_SB, shots=[{"id": "S1", "duration_s": 3, "camera": "crane", "characters": ["MIA"]}])
        issues = " | ".join(sb.lint(bad))
        self.assertIn("MIA", issues)
        self.assertIn("crane", issues)
        self.assertIn("total durasi", issues)

    def test_missing_costume_breaks_continuity(self):
        c = {"ZYAN": {"name": "Zyan", "costume": "", "palette": "abu-abu"}}
        self.assertTrue(any("costume" in i for i in sb.lint(dict(GOOD_SB, characters=c))))


class PanelTests(unittest.TestCase):
    PAGE = {"width": 1000, "height": 1000, "margin": 30, "reading": "rtl"}
    PANELS = [{"id": "A", "x": 500, "y": 50, "w": 400, "h": 400},
              {"id": "B", "x": 50, "y": 50, "w": 400, "h": 400},
              {"id": "C", "x": 50, "y": 500, "w": 850, "h": 400}]

    def test_rtl_reading_order_top_row_right_to_left(self):
        self.assertEqual(pc.reading_order(self.PANELS, "rtl"), ["A", "B", "C"])
        self.assertEqual(pc.reading_order(self.PANELS, "ltr"), ["B", "A", "C"])

    def test_valid_layout_passes(self):
        self.assertEqual(pc.lint(self.PAGE, self.PANELS, ["A", "B", "C"]), [])

    def test_overlap_margin_and_order_mismatch_detected(self):
        panels = self.PANELS + [{"id": "D", "x": 60, "y": 60, "w": 100, "h": 100}, {"id": "E", "x": 5, "y": 5, "w": 100, "h": 100}]
        issues = " | ".join(pc.lint(self.PAGE, panels, ["B", "A", "C", "D", "E"]))
        self.assertIn("tumpang tindih", issues)
        self.assertIn("di luar margin", issues)
        self.assertIn("urutan baca", issues)


class MechanicsTests(unittest.TestCase):
    def test_xp_with_streak_and_cap(self):
        self.assertAlmostEqual(gm.xp_for_answer(10, 5), 15.0)
        self.assertAlmostEqual(gm.xp_for_answer(10, 20), 20.0)  # dibatasi cap 2.0

    def test_level_thresholds(self):
        self.assertEqual(gm.level_threshold(2), 100.0)
        self.assertEqual(gm.level_threshold(3), 300.0)
        self.assertEqual(gm.level_for_xp(299), 2)
        self.assertEqual(gm.level_for_xp(300), 3)

    def test_survival_decay_and_clamp(self):
        self.assertAlmostEqual(gm.survival_value(100, 2, 10), 80.0)
        self.assertEqual(gm.survival_value(10, 2, 100), 0.0)
        self.assertAlmostEqual(gm.seconds_until_empty(50, 2), 25.0)


class MultiAgentTests(unittest.TestCase):
    def test_chain_gives_one_task_per_wave(self):
        r = tg.plan([{"id": "T1", "writes": ["a"]}, {"id": "T2", "deps": ["T1"], "writes": ["b"]},
                     {"id": "T3", "deps": ["T2"], "writes": ["c"]}])
        self.assertEqual(r["waves"], [["T1"], ["T2"], ["T3"]])

    def test_independent_disjoint_tasks_run_in_parallel(self):
        r = tg.plan([{"id": "T1", "writes": ["a"]}, {"id": "T2", "writes": ["b"]}])
        self.assertEqual(r["waves"], [["T1", "T2"]])

    def test_write_conflict_is_serialized(self):
        r = tg.plan([{"id": "T1", "writes": ["same.py"]}, {"id": "T2", "writes": ["same.py"]}])
        self.assertEqual(r["waves"], [["T1"], ["T2"]])

    def test_cycle_and_missing_dependency_rejected(self):
        with self.assertRaises(ValueError):
            tg.plan([{"id": "A", "deps": ["B"]}, {"id": "B", "deps": ["A"]}])
        with self.assertRaises(ValueError):
            tg.plan([{"id": "A", "deps": ["Z"]}])


class TwinTests(unittest.TestCase):
    """R=2 K/W, C=50 J/K, tau=RC=100 s, P=10 W, T_amb=25 C. PR = 20 K."""

    def test_steady_state_and_time_constant(self):
        self.assertAlmostEqual(tw.steady_state(10, 2, 25), 45.0)
        # Pada t = tau: T = T_amb + PR (1 - e^-1) = 25 + 20 * 0.632121 = 37.6424
        self.assertAlmostEqual(tw.analytic(100, 10, 2, 50, 25), 37.6424, places=3)

    def test_euler_tracks_analytic_within_tolerance(self):
        sim = tw.simulate_euler(100, 1.0, 10, 2, 50, 25)
        self.assertLess(abs(sim[-1][1] - tw.analytic(100, 10, 2, 50, 25)), 0.5)

    def test_unstable_step_rejected(self):
        with self.assertRaises(ValueError):
            tw.simulate_euler(100, 50, 10, 2, 50, 25)


class TagTests(unittest.TestCase):
    GOOD = {"tags": [
        {"name": "TT-101", "type": "AI", "eng_lo": 0, "eng_hi": 150, "alarm": {"LL": 5, "L": 20, "H": 120, "HH": 140},
         "device": "PLC1", "address": 40001},
        {"name": "PM-102A", "type": "AI", "eng_lo": 0, "eng_hi": 10, "device": "PLC1", "address": 40002},
        {"name": "PMP-201", "type": "DO", "device": "PLC1", "address": 10}]}

    def test_good_tags_pass(self):
        self.assertEqual(tc.lint(self.GOOD), [])

    def test_common_tag_errors_detected(self):
        bad = {"tags": [
            {"name": "TT-101", "type": "AI", "eng_lo": 0, "eng_hi": 150, "alarm": {"LL": 5, "L": 140, "H": 120, "HH": 130}},
            {"name": "TT-101", "type": "DI", "eng_lo": 0, "eng_hi": 1},
            {"name": "xx", "type": "AI"},
            {"name": "PM-102", "type": "AI", "eng_lo": 0, "eng_hi": 10, "device": "PLC1", "address": 40002},
            {"name": "PM-103", "type": "AI", "eng_lo": 0, "eng_hi": 10, "device": "PLC1", "address": 40002}]}
        issues = " | ".join(tc.lint(bad))
        for needle in ("duplikat", "pola nama", "wajib punya eng_lo", "tidak boleh punya rentang", "tidak urut", "alamat"):
            self.assertIn(needle, issues, issues)


class TroubleshootTests(unittest.TestCase):
    # Nilai batas di bawah ini adalah NILAI UJI untuk memverifikasi mesin penelusuran, bukan nilai standar.
    TREE = {"start": "n1", "nodes": {
        "n1": {"measure": "tegangan_input_v", "op": "between", "value": [200, 240], "yes": "n2", "no": "c_input"},
        "n2": {"measure": "sekring_ok", "op": "eq", "value": True, "yes": "c_load", "no": "c_fuse"},
        "c_input": {"cause": "tegangan input di luar rentang uji", "action": "periksa sumber dan pemutus"},
        "c_fuse": {"cause": "sekring putus", "action": "ganti sekring setelah cari penyebab beban"},
        "c_load": {"cause": "beban berlebih", "action": "ukur arus beban"}}}

    def test_reaches_cause_through_both_branches(self):
        self.assertEqual(ft.walk(self.TREE, {"tegangan_input_v": 230, "sekring_ok": True})["cause"], "beban berlebih")
        self.assertEqual(ft.walk(self.TREE, {"tegangan_input_v": 230, "sekring_ok": False})["cause"], "sekring putus")
        self.assertEqual(ft.walk(self.TREE, {"tegangan_input_v": 180, "sekring_ok": True})["cause"],
                         "tegangan input di luar rentang uji")

    def test_missing_measurement_stops_instead_of_guessing(self):
        r = ft.walk(self.TREE, {"sekring_ok": True})
        self.assertEqual(r["status"], "NEED_MEASUREMENT")
        self.assertEqual(r["measure"], "tegangan_input_v")


if __name__ == "__main__":
    unittest.main()
