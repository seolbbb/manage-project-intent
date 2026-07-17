#!/usr/bin/env python3
"""Safely scaffold the canonical project documents.

Dry-run is the default. Existing files are never overwritten.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


TEMPLATE_NAMES = (
    "PRODUCT_SPEC.md",
    "ROADMAP.md",
    "PROJECT_STATUS.md",
    "DECISION_LOG.md",
)
START_MARKER = "<!-- manage-project-intent:start -->"
CANONICAL_NAMES = frozenset(TEMPLATE_NAMES)
LEGACY_NAMES = frozenset(("PRODUCT_SPEC.md", "PROJECT_STATUS.md", "DECISION_LOG.md"))


@dataclass(frozen=True)
class Action:
    kind: str
    target: Path
    content: str | None = None
    reason: str | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold project operating documents without overwriting existing work."
    )
    parser.add_argument("--root", required=True, type=Path, help="Project root")
    parser.add_argument("--project-name", help="Display name; defaults to the root folder name")
    parser.add_argument(
        "--language",
        default="auto",
        help="Working language label or code recorded in templates; auto detects Korean or English",
    )
    parser.add_argument(
        "--migrate-legacy",
        action="store_true",
        help="Explicitly allow adding ROADMAP.md to an approved legacy three-document project",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Preview actions (default)")
    mode.add_argument("--apply", action="store_true", help="Create missing files and append the AGENTS snippet")
    return parser.parse_args()


def detect_language(root: Path) -> str:
    candidates = [root / "AGENTS.md", root / "README.md"]
    docs = root / "docs"
    if docs.is_dir():
        candidates.extend(sorted(docs.glob("*.md"))[:12])

    sample_parts: list[str] = []
    for path in candidates:
        if not path.is_file():
            continue
        try:
            sample_parts.append(path.read_text(encoding="utf-8-sig")[:20_000])
        except UnicodeError:
            continue
    sample = "\n".join(sample_parts)
    return "ko" if len(re.findall(r"[가-힣]", sample)) >= 20 else "en"


def language_label(code: str) -> str:
    return {"ko": "Korean", "en": "English"}.get(code.casefold(), code)


def resolve_language(value: str, root: Path) -> str:
    if value.casefold() == "auto":
        return detect_language(root)
    label = value.strip()
    if not label or any(character in label for character in "\r\n{}"):
        raise ValueError("--language must be a non-empty single-line label without braces")
    return label


def classify_document_state(root: Path) -> tuple[str, frozenset[str]]:
    docs = root / "docs"
    present = frozenset(name for name in TEMPLATE_NAMES if (docs / name).is_file())
    if not present:
        return "new", present
    if present == CANONICAL_NAMES:
        return "canonical", present
    if present == LEGACY_NAMES:
        return "legacy", present
    return "partial", present


def render(template: str, project_name: str, date: str, language: str) -> str:
    return (
        template.replace("{{PROJECT_NAME}}", project_name)
        .replace("{{DATE}}", date)
        .replace("{{LANGUAGE}}", language_label(language))
    )


def build_actions(root: Path, project_name: str, language: str) -> list[Action]:
    skill_root = Path(__file__).resolve().parents[1]
    templates = skill_root / "assets" / "templates"
    today = datetime.now().astimezone().date().isoformat()
    actions: list[Action] = []

    for name in TEMPLATE_NAMES:
        target = root / "docs" / name
        if target.exists():
            actions.append(Action("SKIP", target, reason="already exists"))
            continue
        source = templates / name
        content = render(source.read_text(encoding="utf-8"), project_name, today, language)
        actions.append(Action("CREATE", target, content=content))

    agents_target = root / "AGENTS.md"
    snippet = (templates / "AGENTS-snippet.md").read_text(encoding="utf-8")
    if not agents_target.exists():
        actions.append(Action("CREATE", agents_target, content=snippet))
    else:
        try:
            existing = agents_target.read_text(encoding="utf-8-sig")
        except UnicodeError as exc:
            raise ValueError(f"Cannot safely read {agents_target} as UTF-8: {exc}") from exc
        if START_MARKER in existing:
            actions.append(Action("SKIP", agents_target, reason="managed snippet already present"))
        else:
            actions.append(Action("APPEND", agents_target, content=snippet))

    return actions


def apply_action(action: Action) -> None:
    if action.kind == "SKIP":
        return
    if action.kind == "CREATE":
        action.target.parent.mkdir(parents=True, exist_ok=True)
        with action.target.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(action.content or "")
        return
    if action.kind == "APPEND":
        raw = action.target.read_bytes()
        prefix = b"" if not raw or raw.endswith((b"\n", b"\r")) else b"\n"
        with action.target.open("ab") as handle:
            handle.write(prefix + b"\n" + (action.content or "").encode("utf-8"))
        return
    raise ValueError(f"Unsupported action: {action.kind}")


def main() -> int:
    args = parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: project root does not exist or is not a directory: {root}", file=sys.stderr)
        return 2

    state, present = classify_document_state(root)
    if state == "partial":
        shown = ", ".join(sorted(present)) or "none"
        print(
            "ERROR: ambiguous partial canonical document set detected "
            f"({shown}); run an audit and repair or approve migration before bootstrapping.",
            file=sys.stderr,
        )
        return 2
    if state == "legacy" and args.apply and not args.migrate_legacy:
        print(
            "ERROR: legacy three-document project requires --migrate-legacy with --apply after migration approval.",
            file=sys.stderr,
        )
        return 3

    try:
        language = resolve_language(args.language, root)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    project_name = args.project_name or root.name
    try:
        actions = build_actions(root, project_name, language)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"{mode}: root={root} language={language} document_state={state}")
    if state == "legacy" and not args.migrate_legacy:
        print("MIGRATION REQUIRED: preview only; pass --migrate-legacy with --apply after approval.")
    for action in actions:
        suffix = f" ({action.reason})" if action.reason else ""
        print(f"{action.kind}: {action.target}{suffix}")

    if args.apply:
        try:
            for action in actions:
                apply_action(action)
        except OSError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        print("Applied without overwriting existing files.")
    else:
        print("No files changed. Re-run with --apply after plan approval.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
