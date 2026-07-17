#!/usr/bin/env python3
"""Synchronize the repository Skill into a local Codex home after review."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path


SKILL_NAME = "manage-project-intent"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preview or synchronize the repository-owned Codex Skill."
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        help="Codex home directory; defaults to CODEX_HOME or ~/.codex",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Preview actions (default)")
    mode.add_argument("--apply", action="store_true", help="Install the Skill")
    return parser.parse_args()


def ignored(path: Path) -> bool:
    return "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}


def manifest(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    if not root.is_dir():
        return result
    for path in sorted(item for item in root.rglob("*") if item.is_file() and not ignored(item)):
        relative = path.relative_to(root).as_posix()
        result[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def validate_source(source: Path) -> None:
    skill_md = source / "SKILL.md"
    if not skill_md.is_file():
        raise ValueError(f"Missing source SKILL.md: {skill_md}")
    text = skill_md.read_text(encoding="utf-8-sig")
    match = re.search(r"(?m)^name:\s*([^\s]+)\s*$", text)
    if not match or match.group(1) != SKILL_NAME:
        actual = match.group(1) if match else "missing"
        raise ValueError(f"Source Skill name must be {SKILL_NAME}; found {actual}")


def install(source: Path, destination: Path) -> None:
    skills_root = destination.parent
    skills_root.mkdir(parents=True, exist_ok=True)
    if destination.is_symlink():
        raise ValueError(f"Refusing to replace a symlinked Skill destination: {destination}")

    temporary = Path(tempfile.mkdtemp(prefix=f".{SKILL_NAME}-", dir=skills_root))
    staged = temporary / "staged"
    backup = temporary / "previous"
    shutil.copytree(
        source,
        staged,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
    )

    moved_existing = False
    installed = False
    try:
        if destination.exists():
            destination.replace(backup)
            moved_existing = True
        staged.replace(destination)
        installed = True
    except OSError:
        if installed and destination.exists():
            shutil.rmtree(destination)
        if moved_existing and backup.exists():
            backup.replace(destination)
        raise
    finally:
        shutil.rmtree(temporary, ignore_errors=True)


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    source = repo_root / "skills" / SKILL_NAME
    codex_home = (args.codex_home or Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))).expanduser().resolve()
    skills_root = codex_home / "skills"
    destination = skills_root / SKILL_NAME

    try:
        validate_source(source)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    source_manifest = manifest(source)
    destination_manifest = manifest(destination)
    changed = source_manifest != destination_manifest
    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"{mode}: source={source} destination={destination}")
    if not destination.exists():
        print(f"CREATE: {destination} ({len(source_manifest)} files)")
    elif changed:
        print(f"REPLACE: {destination} (installed copy differs from source)")
    else:
        print(f"UP-TO-DATE: {destination}")

    if not args.apply:
        print("No files changed. Re-run with --apply after validation.")
        return 0

    try:
        if changed or not destination.exists():
            install(source, destination)
        if manifest(destination) != source_manifest:
            raise ValueError("Installed Skill does not match the repository source")
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print("Synchronized and verified the repository-owned Skill.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
