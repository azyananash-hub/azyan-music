import os
import shutil
import tempfile
import unittest

from _helpers import LIBRARY_ROOT, load_module

SCRIPTS = os.path.join(LIBRARY_ROOT, "scripts")
zy = load_module("zy_lib", "scripts/zy_lib.py")
install = load_module("install_skills", "scripts/install_skills.py")
validate_library = load_module("validate_library", "scripts/validate_library.py")

VALID_BODY = "\n".join(f"## {s}\n\ntext\n" for s in zy.REQUIRED_SECTIONS)


def _skill_text(name: str, description: str = "A valid description that is long enough to pass the check.",
                license_: str = "MIT", body: str = VALID_BODY) -> str:
    return f"---\nname: {name}\ndescription: {description}\nlicense: {license_}\n---\n\n# {name}\n\n{body}"


class ZyLibTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name

    def tearDown(self):
        self._tmp.cleanup()

    def _make(self, category: str, folder: str, text: str) -> str:
        d = os.path.join(self.root, category, folder)
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, "SKILL.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path

    def test_valid_skill_has_no_errors(self):
        doc = zy.parse_skill(self._make("engineering", "good-skill", _skill_text("good-skill")), "engineering")
        zy.validate_skill(doc)
        self.assertEqual(doc.errors, [])

    def test_name_must_match_folder(self):
        doc = zy.parse_skill(self._make("engineering", "folder-name", _skill_text("other-name")), "engineering")
        zy.validate_skill(doc)
        self.assertTrue(any("harus sama dengan nama folder" in e for e in doc.errors))

    def test_missing_section_is_error(self):
        body = VALID_BODY.replace("## Test Cases", "## Something Else")
        doc = zy.parse_skill(self._make("engineering", "missing", _skill_text("missing", body=body)), "engineering")
        zy.validate_skill(doc)
        self.assertTrue(any("Test Cases" in e for e in doc.errors))

    def test_missing_license_is_error(self):
        text = "---\nname: nolic\ndescription: A valid description that is long enough to pass the check.\n---\n" + VALID_BODY
        doc = zy.parse_skill(self._make("engineering", "nolic", text), "engineering")
        zy.validate_skill(doc)
        self.assertTrue(any("license" in e for e in doc.errors))

    def test_broken_frontmatter_detected(self):
        doc = zy.parse_skill(self._make("engineering", "broken", "no frontmatter here"), "engineering")
        self.assertTrue(doc.errors)

    def test_multiline_value_rejected(self):
        fm, _, errors = zy.parse_frontmatter("---\nname: x\n  continued: y\n---\nbody")
        self.assertTrue(errors)

    def test_missing_referenced_script_is_error(self):
        body = VALID_BODY + "\nJalankan scripts/ghost.py\n"
        doc = zy.parse_skill(self._make("engineering", "ghost", _skill_text("ghost", body=body)), "engineering")
        zy.validate_skill(doc)
        self.assertTrue(any("ghost.py" in e for e in doc.errors))

    def test_discover_finds_nested_skills(self):
        self._make("engineering", "a-skill", _skill_text("a-skill"))
        self._make("finance", "b-skill", _skill_text("b-skill"))
        names = sorted(d.folder for d in zy.discover_skills(self.root))
        self.assertEqual(names, ["a-skill", "b-skill"])


class RealLibraryTests(unittest.TestCase):
    """Integration test: library sungguhan harus valid dan registry sinkron."""

    def test_all_skills_valid(self):
        docs = zy.discover_skills()
        self.assertGreater(len(docs), 0)
        for doc in docs:
            zy.validate_skill(doc)
            self.assertEqual(doc.errors, [], msg=f"{doc.path}: {doc.errors}")

    def test_registry_in_sync(self):
        errors, messages = validate_library.run()
        registry_msgs = [m for m in messages if "SKILL_REGISTRY" in m]
        self.assertEqual(registry_msgs, [], msg=registry_msgs)

    def test_install_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "skills")
            install.plan(target, None, False)
            self.assertFalse(os.path.exists(target))

    def test_install_apply_copies_valid_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "skills")
            os.makedirs(target)
            actions = install.plan(target, {"trade-statistics"}, False)
            self.assertEqual([a[0] for a in actions], ["install"])
            install.apply(target, actions)
            self.assertTrue(os.path.isfile(os.path.join(target, "trade-statistics", "SKILL.md")))
            self.assertTrue(os.path.isfile(os.path.join(target, "trade-statistics", "scripts", "trade_stats.py")))
            # kedua kalinya harus skip-exists, bukan menimpa diam-diam
            actions2 = install.plan(target, {"trade-statistics"}, False)
            self.assertEqual([a[0] for a in actions2], ["skip-exists"])


if __name__ == "__main__":
    unittest.main()
