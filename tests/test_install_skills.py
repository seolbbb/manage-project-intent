from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = REPO_ROOT / "tooling" / "install_skills.py"
SOURCE = REPO_ROOT / "skills" / "manage-project-intent"


class InstallerTests(unittest.TestCase):
    def run_installer(self, codex_home: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(INSTALLER), "--codex-home", str(codex_home), *args],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def test_dry_run_is_default_and_changes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary) / ".codex"
            result = self.run_installer(codex_home)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("DRY-RUN", result.stdout)
            self.assertFalse((codex_home / "skills" / "manage-project-intent").exists())

    def test_apply_installs_exact_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary) / ".codex"

            result = self.run_installer(codex_home, "--apply")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            installed = codex_home / "skills" / "manage-project-intent"
            self.assertEqual(
                (installed / "SKILL.md").read_text(encoding="utf-8"),
                (SOURCE / "SKILL.md").read_text(encoding="utf-8"),
            )

    def test_apply_replaces_stale_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary) / ".codex"
            installed = codex_home / "skills" / "manage-project-intent"
            installed.mkdir(parents=True)
            (installed / "stale.txt").write_text("stale", encoding="utf-8")

            result = self.run_installer(codex_home, "--apply")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertFalse((installed / "stale.txt").exists())


if __name__ == "__main__":
    unittest.main()
