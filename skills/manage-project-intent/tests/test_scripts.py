from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = SKILL_ROOT / "scripts" / "validate_project_docs.py"
BOOTSTRAPPER = SKILL_ROOT / "scripts" / "bootstrap_project_docs.py"
FIXTURES = SKILL_ROOT / "tests" / "fixtures"
EVAL_CASES = SKILL_ROOT / "tests" / "evals" / "cases.json"


class ScriptTests(unittest.TestCase):
    def run_script(self, script: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script), *args],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def copy_valid(self, temporary: str) -> Path:
        root = Path(temporary) / "project"
        shutil.copytree(FIXTURES / "valid", root)
        return root

    def test_valid_fixture_passes(self) -> None:
        result = self.run_script(VALIDATOR, "--root", str(FIXTURES / "valid"), "--strict", "full")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Validation PASSED", result.stdout)

    def test_duplicate_next_task_fails_precisely(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_valid(temporary)
            shutil.copy2(FIXTURES / "broken-next-task" / "PROJECT_STATUS.md", root / "docs" / "PROJECT_STATUS.md")
            result = self.run_script(VALIDATOR, "--root", str(root), "--strict", "full")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("NEXT_TASK_COUNT", result.stdout)

    def test_stale_complete_status_fails_precisely(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_valid(temporary)
            shutil.copy2(FIXTURES / "stale-status" / "PROJECT_STATUS.md", root / "docs" / "PROJECT_STATUS.md")
            result = self.run_script(VALIDATOR, "--root", str(root), "--strict", "full")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("HARDCODED_CURRENT_HEAD", result.stdout)
        self.assertIn("COMPLETE_STATUS_HAS_OPEN_ROADMAP_WORK", result.stdout)

    def test_superseded_decisions_require_and_accept_bidirectional_links(self) -> None:
        replacement = """

### DEC-002 — Preserve intent with canonical documents

- Status: accepted
- Date: 2026-07-18
- Initiated by: User
- Context: Chat history alone did not survive new sessions.
- User intent/value protected: Preserve intent in repository artifacts.
- Intervention: The user required a durable project record.
- Options considered: Chat history; canonical documents.
- Decision: Use canonical documents.
- Consequences: Agents must update the durable record.
- Reconsider when: A stronger durable mechanism replaces it.
- Supersedes: DEC-001
- Superseded by: None
"""
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_valid(temporary)
            log = root / "docs" / "DECISION_LOG.md"
            text = log.read_text(encoding="utf-8")
            text = text.replace("- Status: accepted", "- Status: superseded", 1)
            text = text.replace("- Superseded by: None", "- Superseded by: DEC-002", 1)
            log.write_text(text + replacement, encoding="utf-8")
            result = self.run_script(VALIDATOR, "--root", str(root), "--strict", "full")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_bootstrap_defaults_to_dry_run_and_never_overwrites(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project"
            root.mkdir()
            agents = root / "AGENTS.md"
            agents.write_text("# Existing rules\n", encoding="utf-8")

            preview = self.run_script(BOOTSTRAPPER, "--root", str(root), "--language", "Japanese")
            self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
            self.assertIn("DRY-RUN", preview.stdout)
            self.assertFalse((root / "docs" / "PRODUCT_SPEC.md").exists())
            self.assertEqual(agents.read_text(encoding="utf-8"), "# Existing rules\n")

            applied = self.run_script(BOOTSTRAPPER, "--root", str(root), "--language", "Japanese", "--apply")
            self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
            self.assertTrue((root / "docs" / "PRODUCT_SPEC.md").is_file())
            first = (root / "docs" / "PRODUCT_SPEC.md").read_text(encoding="utf-8")
            self.assertIn("Working language: Japanese", first)
            self.assertIn("# Existing rules", agents.read_text(encoding="utf-8"))

            second = self.run_script(BOOTSTRAPPER, "--root", str(root), "--language", "Japanese", "--apply")
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            self.assertEqual(first, (root / "docs" / "PRODUCT_SPEC.md").read_text(encoding="utf-8"))
            self.assertEqual(agents.read_text(encoding="utf-8").count("manage-project-intent:start"), 1)

    def test_legacy_bootstrap_requires_explicit_migration(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project"
            docs = root / "docs"
            docs.mkdir(parents=True)
            for name in ("PRODUCT_SPEC.md", "PROJECT_STATUS.md", "DECISION_LOG.md"):
                shutil.copy2(FIXTURES / "valid" / "docs" / name, docs / name)
            original = (docs / "PRODUCT_SPEC.md").read_text(encoding="utf-8")

            preview = self.run_script(BOOTSTRAPPER, "--root", str(root))
            self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
            self.assertIn("MIGRATION REQUIRED", preview.stdout)
            self.assertFalse((docs / "ROADMAP.md").exists())

            rejected = self.run_script(BOOTSTRAPPER, "--root", str(root), "--apply")
            self.assertEqual(rejected.returncode, 3, rejected.stdout + rejected.stderr)
            self.assertFalse((docs / "ROADMAP.md").exists())

            migrated = self.run_script(BOOTSTRAPPER, "--root", str(root), "--apply", "--migrate-legacy")
            self.assertEqual(migrated.returncode, 0, migrated.stdout + migrated.stderr)
            self.assertTrue((docs / "ROADMAP.md").is_file())
            self.assertEqual(original, (docs / "PRODUCT_SPEC.md").read_text(encoding="utf-8"))

    def test_partial_document_set_is_rejected_for_audit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project"
            docs = root / "docs"
            docs.mkdir(parents=True)
            shutil.copy2(FIXTURES / "valid" / "docs" / "PRODUCT_SPEC.md", docs / "PRODUCT_SPEC.md")
            result = self.run_script(BOOTSTRAPPER, "--root", str(root))
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("ambiguous partial canonical document set", result.stderr)

    def test_broken_local_link_fails_precisely(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_valid(temporary)
            spec = root / "docs" / "PRODUCT_SPEC.md"
            spec.write_text(spec.read_text(encoding="utf-8") + "\n[Missing](missing.md)\n", encoding="utf-8")
            result = self.run_script(VALIDATOR, "--root", str(root), "--strict", "full")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("BROKEN_LOCAL_LINK", result.stdout)

    def test_duplicate_phase_task_and_decision_ids_fail(self) -> None:
        duplicate_phase = """

### PHASE-001 — Duplicate

- Status: planned
- Outcome: Duplicate IDs fail.
- Dependencies: None
- Entry criteria: None.
- Exit criteria: Validation fails.
- Verification evidence: Pending.

Tasks:

- [ ] TASK-001: Duplicate task.
"""
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_valid(temporary)
            roadmap = root / "docs" / "ROADMAP.md"
            roadmap.write_text(roadmap.read_text(encoding="utf-8") + duplicate_phase, encoding="utf-8")
            log = root / "docs" / "DECISION_LOG.md"
            decision = log.read_text(encoding="utf-8").split("### DEC-001", 1)[1]
            log.write_text(log.read_text(encoding="utf-8") + "\n### DEC-001" + decision, encoding="utf-8")
            result = self.run_script(VALIDATOR, "--root", str(root), "--strict", "full")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("DUPLICATE_PHASE_ID", result.stdout)
        self.assertIn("DUPLICATE_TASK_ID", result.stdout)
        self.assertIn("DUPLICATE_DECISION_ID", result.stdout)

    def test_multiple_active_phases_and_snapshot_mismatch_fail(self) -> None:
        second_phase = """

### PHASE-002 — Conflicting active phase

- Status: active
- Outcome: Demonstrate a conflict.
- Dependencies: PHASE-001
- Entry criteria: The first phase is active.
- Exit criteria: Validation rejects the conflict.
- Verification evidence: Pending.

Tasks:

- [ ] TASK-002: Resolve the conflict.
"""
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_valid(temporary)
            roadmap = root / "docs" / "ROADMAP.md"
            text = roadmap.read_text(encoding="utf-8")
            text = text.replace("- Phase: PHASE-001", "- Phase: PHASE-002", 1)
            roadmap.write_text(text + second_phase, encoding="utf-8")
            result = self.run_script(VALIDATOR, "--root", str(root), "--strict", "full")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("MULTIPLE_ACTIVE_PHASES", result.stdout)
        self.assertIn("CURRENT_PHASE_MISMATCH", result.stdout)

    def test_checked_task_requires_concrete_verification_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_valid(temporary)
            roadmap = root / "docs" / "ROADMAP.md"
            text = roadmap.read_text(encoding="utf-8").replace("- [ ] TASK-001", "- [x] TASK-001")
            roadmap.write_text(text, encoding="utf-8")
            result = self.run_script(VALIDATOR, "--root", str(root), "--strict", "full")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("CHECKED_TASK_NO_EVIDENCE", result.stdout)

    def test_unknown_decision_link_and_supersede_cycle_fail(self) -> None:
        cycle_decision = """

### DEC-002 — Cycle back to the first decision

- Status: superseded
- Date: 2026-07-18
- Initiated by: User
- Context: A deliberately invalid cycle.
- User intent/value protected: Detect invalid history.
- Intervention: The test introduces a cycle.
- Options considered: Acyclic history; cyclic history.
- Decision: Link back to DEC-001.
- Consequences: Validation must fail.
- Reconsider when: Never.
- Supersedes: DEC-001
- Superseded by: DEC-001
"""
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_valid(temporary)
            log = root / "docs" / "DECISION_LOG.md"
            text = log.read_text(encoding="utf-8")
            text = text.replace("- Status: accepted", "- Status: superseded", 1)
            text = text.replace("- Supersedes: None", "- Supersedes: DEC-002", 1)
            text = text.replace("- Superseded by: None", "- Superseded by: DEC-002", 1)
            log.write_text(text + cycle_decision, encoding="utf-8")
            cycle = self.run_script(VALIDATOR, "--root", str(root), "--strict", "full")
            self.assertIn("DECISION_SUPERSEDE_CYCLE", cycle.stdout)

            log.write_text((FIXTURES / "valid" / "docs" / "DECISION_LOG.md").read_text(encoding="utf-8").replace("- Supersedes: None", "- Supersedes: DEC-999", 1), encoding="utf-8")
            unknown = self.run_script(VALIDATOR, "--root", str(root), "--strict", "full")
        self.assertEqual(cycle.returncode, 1, cycle.stdout + cycle.stderr)
        self.assertEqual(unknown.returncode, 1, unknown.stdout + unknown.stderr)
        self.assertIn("UNKNOWN_SUPERSEDED_DECISION", unknown.stdout)

    def test_lite_mode_allows_projects_without_canonical_documents(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project"
            root.mkdir()
            result = self.run_script(VALIDATOR, "--root", str(root), "--strict", "lite")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("DOCS_NOT_ADOPTED", result.stdout)

    def test_spec_kit_presence_does_not_change_canonical_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_valid(temporary)
            without = self.run_script(VALIDATOR, "--root", str(root), "--strict", "full")
            (root / ".specify").mkdir()
            with_spec_kit = self.run_script(VALIDATOR, "--root", str(root), "--strict", "full")
        self.assertEqual(without.returncode, 0, without.stdout + without.stderr)
        self.assertEqual(with_spec_kit.returncode, 0, with_spec_kit.stdout + with_spec_kit.stderr)

    def test_behavioral_eval_cases_cover_the_operating_contract(self) -> None:
        cases = json.loads(EVAL_CASES.read_text(encoding="utf-8"))
        ids = {case["id"] for case in cases}
        self.assertEqual(
            ids,
            {
                "full-new-product",
                "delta-bounded-feature",
                "lite-internal-fix",
                "read-only-status-audit",
                "continue-single-next-task",
                "revise-superseded-decision",
                "goldfish-handoff",
            },
        )
        for case in cases:
            self.assertTrue(case["prompt"].strip())
            self.assertTrue(case["expected_assertions"])
            self.assertTrue(case["forbidden_assertions"])


if __name__ == "__main__":
    unittest.main()
