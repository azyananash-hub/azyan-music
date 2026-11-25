"""Uji fitur v0.7 router: override kontekstual, catatan konflik, dan metrik ukuran (tanpa membaca isi skill)."""
import importlib.util
import json
import os
import unittest

from _helpers import LIBRARY_ROOT

spec = importlib.util.spec_from_file_location("route_skill", os.path.join(LIBRARY_ROOT, "scripts", "route_skill.py"))
rt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rt)
REG = json.load(open(os.path.join(LIBRARY_ROOT, "SKILL_REGISTRY.json"), encoding="utf-8"))["skills"]
CONSTRAINTS = {k: v for k, v in json.load(open(os.path.join(LIBRARY_ROOT, "references", "skill-constraints.json"),
                                             encoding="utf-8")).items() if k != "note"}
PROFILES = {k: v for k, v in json.load(open(os.path.join(LIBRARY_ROOT, "references", "project-profiles.json"),
                                            encoding="utf-8")).items() if k != "note"}


class ContextNoteTests(unittest.TestCase):
    def test_override_when_profile_allows_and_brief_uses_forbidden_term(self):
        notes = rt.context_notes("adegan neon", "cinematic-camera", "earthstop", CONSTRAINTS, PROFILES)
        self.assertEqual(len(notes), 1)
        self.assertTrue(notes[0].startswith("OVERRIDE (EarthStop)"), notes)

    def test_conflict_when_no_profile_override(self):
        notes = rt.context_notes("adegan neon", "cinematic-camera", None, CONSTRAINTS, PROFILES)
        self.assertTrue(notes and notes[0].startswith("KONFLIK"), notes)

    def test_no_note_when_brief_is_clean_or_skill_has_no_constraint(self):
        self.assertEqual(rt.context_notes("adegan malam hari", "cinematic-camera", None, CONSTRAINTS, PROFILES), [])
        self.assertEqual(rt.context_notes("neon", "ro-mass-balance", None, CONSTRAINTS, PROFILES), [])


class RouteWithContextTests(unittest.TestCase):
    def test_results_carry_size_and_resource_metrics_without_reading_bodies(self):
        top = rt.route_with_context("kamera sinematik untuk adegan neon malam hari", REG, 2, project="earthstop")
        self.assertEqual(top[0]["name"], "cinematic-camera")
        self.assertGreater(top[0]["skill_md_bytes"], 0)
        self.assertIsInstance(top[0]["scripts"], int)
        self.assertTrue(any("OVERRIDE" in n for n in top[0]["notes"]))

    def test_unrelated_query_returns_nothing(self):
        self.assertEqual(rt.route_with_context("resep kue cokelat", REG, 3), [])

    def test_project_profile_boosts_preferred_category(self):
        base = {r["name"]: r["score"] for r in rt.route_with_context("animasi", REG, 50)}
        boosted = {r["name"]: r["score"] for r in rt.route_with_context("animasi", REG, 50, project="silent-neon-tokyo-manhwa")}
        preferred = [n for n in base if n in boosted and any(s["name"] == n and s["category"] == "creative-production" for s in REG)]
        self.assertTrue(preferred)
        self.assertGreater(boosted[preferred[0]], base[preferred[0]])


if __name__ == "__main__":
    unittest.main()
