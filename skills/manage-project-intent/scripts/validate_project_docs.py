#!/usr/bin/env python3
"""Validate the structural project-document contract using only the stdlib."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import unquote


DOC_NAMES = ("PRODUCT_SPEC.md", "ROADMAP.md", "PROJECT_STATUS.md", "DECISION_LOG.md")
LEGACY_NAMES = ("PRODUCT_SPEC.md", "PROJECT_STATUS.md", "DECISION_LOG.md")
PHASE_STATES = {"planned", "active", "blocked", "done", "superseded"}
DECISION_STATES = {"proposed", "accepted", "superseded"}
PROJECT_STATES = {"planning", "active", "blocked", "complete"}
START_MARKER = "<!-- manage-project-intent:start -->"
END_MARKER = "<!-- manage-project-intent:end -->"

REQUIRED_HEADINGS = {
    "PRODUCT_SPEC.md": (
        "Document control",
        "Product intent",
        "Product definition",
        "Users and problems",
        "Goals and success criteria",
        "Scope",
        "User experience",
        "Functional requirements",
        "Safety, privacy, and data",
        "Non-functional requirements",
        "Acceptance criteria",
        "Open questions",
    ),
    "ROADMAP.md": ("Document control", "Status vocabulary", "Current phase", "Phases", "Change policy"),
    "PROJECT_STATUS.md": (
        "Snapshot",
        "Implemented",
        "In progress",
        "Verification evidence",
        "Drift and gaps",
        "Blockers",
        "Next task",
        "Resume checklist",
    ),
    "DECISION_LOG.md": ("Status vocabulary", "Decisions"),
}


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    path: str
    line: int
    message: str


@dataclass
class Document:
    path: Path
    text: str
    lines: list[str]

    @classmethod
    def load(cls, path: Path) -> "Document":
        text = path.read_text(encoding="utf-8-sig")
        return cls(path=path, text=text, lines=text.splitlines())


class Validator:
    def __init__(self, root: Path, strict: str, compatibility: str) -> None:
        self.root = root
        self.strict = strict
        self.compatibility = compatibility
        self.issues: list[Issue] = []
        self.docs_dir = root / "docs"
        self.docs: dict[str, Document] = {}
        self.canonical = True

    def add(self, severity: str, code: str, path: Path, line: int, message: str) -> None:
        try:
            shown = str(path.relative_to(self.root))
        except ValueError:
            shown = str(path)
        self.issues.append(Issue(severity, code, shown, line, message))

    def load(self) -> bool:
        present = {name for name in DOC_NAMES if (self.docs_dir / name).is_file()}
        if not present and self.strict == "lite":
            self.add("INFO", "DOCS_NOT_ADOPTED", self.root, 1, "Lite mode permits a project without canonical documents.")
            return False

        if self.compatibility == "auto" and set(LEGACY_NAMES).issubset(present) and "ROADMAP.md" not in present:
            self.canonical = False
            self.add(
                "WARNING",
                "LEGACY_THREE_DOC",
                self.docs_dir,
                1,
                "Legacy three-document project detected; read compatibly and plan migration before adding ROADMAP.md.",
            )

        required = DOC_NAMES if self.canonical else LEGACY_NAMES
        for name in required:
            path = self.docs_dir / name
            if not path.is_file():
                self.add("ERROR", "MISSING_DOCUMENT", path, 1, f"Required document is missing: docs/{name}")
                continue
            try:
                self.docs[name] = Document.load(path)
            except (OSError, UnicodeError) as exc:
                self.add("ERROR", "UNREADABLE_DOCUMENT", path, 1, str(exc))
        return bool(self.docs)

    @staticmethod
    def heading_map(doc: Document) -> dict[str, list[int]]:
        result: dict[str, list[int]] = {}
        for number, line in enumerate(doc.lines, start=1):
            match = re.match(r"^#{2,6}\s+(.+?)\s*$", line)
            if match:
                result.setdefault(match.group(1).casefold(), []).append(number)
        return result

    @staticmethod
    def section(doc: Document, start_line: int, level: int = 2) -> list[tuple[int, str]]:
        output: list[tuple[int, str]] = []
        marker = "#" * level
        for number in range(start_line + 1, len(doc.lines) + 1):
            line = doc.lines[number - 1]
            if re.match(rf"^{re.escape(marker)}\s+", line):
                break
            output.append((number, line))
        return output

    def check_required_headings(self) -> None:
        if not self.canonical:
            return
        for name, required in REQUIRED_HEADINGS.items():
            doc = self.docs.get(name)
            if not doc:
                continue
            headings = self.heading_map(doc)
            for heading in required:
                matches = headings.get(heading.casefold(), [])
                if not matches:
                    self.add("ERROR", "MISSING_HEADING", doc.path, 1, f"Missing required heading: ## {heading}")
                elif len(matches) > 1:
                    self.add("ERROR", "DUPLICATE_HEADING", doc.path, matches[1], f"Heading appears more than once: {heading}")

    def check_placeholders(self) -> None:
        patterns = (
            re.compile(r"\{\{[^}\n]+\}\}"),
            re.compile(r"\b(?:TBD|TODO|NEEDS\s+CLARIFICATION)\b", re.IGNORECASE),
        )
        severity = "WARNING" if self.strict == "lite" else "ERROR"
        for doc in self.docs.values():
            for line_no, line in enumerate(doc.lines, start=1):
                if any(pattern.search(line) for pattern in patterns):
                    self.add(severity, "UNRESOLVED_PLACEHOLDER", doc.path, line_no, "Resolve placeholder before material implementation.")

    def check_stale_head_claims(self) -> None:
        doc = self.docs.get("PROJECT_STATUS.md")
        if not doc:
            return
        pattern = re.compile(
            r"(?:current\s+HEAD|current\s+commit|latest\s+commit|현재\s+HEAD|현재\s+커밋)\s*:\s*`?[0-9a-f]{7,40}`?",
            re.IGNORECASE,
        )
        for line_no, line in enumerate(doc.lines, start=1):
            if pattern.search(line):
                self.add(
                    "ERROR" if self.canonical else "WARNING",
                    "HARDCODED_CURRENT_HEAD",
                    doc.path,
                    line_no,
                    "Do not claim a stored hash is the current repository state; re-observe Git on resume and record dated evidence.",
                )

    def find_next_heading(self, doc: Document) -> list[int]:
        matches: list[int] = []
        for number, line in enumerate(doc.lines, start=1):
            match = re.match(r"^##\s+(.+?)\s*$", line)
            if not match:
                continue
            title = re.sub(r"^\d+[.)]?\s*", "", match.group(1)).strip().casefold()
            if title in {"next task", "다음 작업"}:
                matches.append(number)
        return matches

    def check_next_task(self) -> str | None:
        doc = self.docs.get("PROJECT_STATUS.md")
        if not doc:
            return None
        headings = self.find_next_heading(doc)
        if len(headings) != 1:
            self.add("ERROR", "NEXT_TASK_HEADING_COUNT", doc.path, headings[1] if len(headings) > 1 else 1, "Exactly one Next task heading is required.")
            return None
        content = self.section(doc, headings[0])
        body = "\n".join(line for _, line in content).strip()
        if not body:
            self.add("ERROR", "EMPTY_NEXT_TASK", doc.path, headings[0], "Next task section is empty.")
            return None
        if re.search(r"None\s*[—-]\s*project complete|없음\s*[—-]\s*프로젝트 완료", body, re.IGNORECASE):
            return None

        if not self.canonical:
            markers = [(line_no, line) for line_no, line in content if re.search(r"(?:Next task|다음 작업)\s*:", line, re.IGNORECASE)]
            if len(markers) > 1:
                self.add("ERROR", "MULTIPLE_LEGACY_NEXT_TASKS", doc.path, markers[1][0], "Legacy status contains multiple explicit next-task markers.")
            elif not markers:
                self.add("WARNING", "LEGACY_NEXT_TASK_SHAPE", doc.path, headings[0], "Could not prove a single legacy next-task marker; migrate before implementation.")
            return None

        task_lines = []
        for line_no, line in content:
            match = re.match(r"^\s*-\s+(TASK-\d{3}):\s+(.+?)\s*$", line)
            if match:
                task_lines.append((line_no, match.group(1), match.group(2)))
        if len(task_lines) != 1:
            self.add("ERROR", "NEXT_TASK_COUNT", doc.path, task_lines[1][0] if len(task_lines) > 1 else headings[0], "Canonical status requires exactly one '- TASK-###: action' line.")
            return None
        if not any(re.match(r"^\s*-\s+Acceptance:\s+\S", line) for _, line in content):
            self.add("ERROR", "NEXT_TASK_ACCEPTANCE", doc.path, headings[0], "Next task requires a non-empty Acceptance line.")
        if not any(re.match(r"^\s*-\s+Verify:\s+\S", line) for _, line in content):
            self.add("ERROR", "NEXT_TASK_VERIFY", doc.path, headings[0], "Next task requires a non-empty Verify line.")
        return task_lines[0][1]

    @staticmethod
    def split_h3_sections(doc: Document, id_pattern: str) -> list[tuple[str, int, list[tuple[int, str]]]]:
        headings: list[tuple[str, int]] = []
        for number, line in enumerate(doc.lines, start=1):
            match = re.match(rf"^###\s+({id_pattern})\b", line)
            if match:
                headings.append((match.group(1), number))
        sections = []
        for index, (item_id, start) in enumerate(headings):
            end = headings[index + 1][1] - 1 if index + 1 < len(headings) else len(doc.lines)
            sections.append((item_id, start, [(n, doc.lines[n - 1]) for n in range(start + 1, end + 1)]))
        return sections

    @staticmethod
    def field(section: list[tuple[int, str]], label: str) -> tuple[int, str] | None:
        pattern = re.compile(rf"^\s*-\s+{re.escape(label)}:\s*(.*?)\s*$", re.IGNORECASE)
        for line_no, line in section:
            match = pattern.match(line)
            if match:
                return line_no, match.group(1)
        return None

    def check_roadmap(self, next_task_id: str | None) -> None:
        doc = self.docs.get("ROADMAP.md")
        if not doc:
            return
        sections = self.split_h3_sections(doc, r"PHASE-\d{3}")
        if not sections:
            self.add("ERROR", "ROADMAP_PHASE_MISSING", doc.path, 1, "Roadmap requires at least one PHASE-### section.")
            return
        ids = [item_id for item_id, _, _ in sections]
        for duplicate in sorted({item_id for item_id in ids if ids.count(item_id) > 1}):
            line = next(start for item_id, start, _ in sections if item_id == duplicate)
            self.add("ERROR", "DUPLICATE_PHASE_ID", doc.path, line, f"Duplicate phase ID: {duplicate}")

        task_defs: list[tuple[str, int, bool]] = []
        for line_no, line in enumerate(doc.lines, start=1):
            match = re.match(r"^\s*-\s+\[([ xX])\]\s+(TASK-\d{3}):\s+(.+?)\s*$", line)
            if match:
                task_defs.append((match.group(2), line_no, match.group(1).lower() == "x"))
        task_ids = [item_id for item_id, _, _ in task_defs]
        for duplicate in sorted({item_id for item_id in task_ids if task_ids.count(item_id) > 1}):
            line = next(line_no for item_id, line_no, _ in task_defs if item_id == duplicate)
            self.add("ERROR", "DUPLICATE_TASK_ID", doc.path, line, f"Duplicate roadmap task ID: {duplicate}")
        if next_task_id:
            matching = [entry for entry in task_defs if entry[0] == next_task_id]
            if not matching:
                self.add("ERROR", "NEXT_TASK_NOT_IN_ROADMAP", doc.path, 1, f"Status next task {next_task_id} is not defined in the roadmap.")
            elif matching[0][2]:
                self.add("ERROR", "NEXT_TASK_ALREADY_DONE", doc.path, matching[0][1], f"Status next task {next_task_id} is already checked complete.")

        phase_statuses: dict[str, tuple[int, str]] = {}
        for phase_id, start, section in sections:
            fields: dict[str, tuple[int, str] | None] = {}
            for label in (
                "Status",
                "Outcome",
                "Dependencies",
                "Entry criteria",
                "Exit criteria",
                "Verification evidence",
            ):
                fields[label] = self.field(section, label)
                if not fields[label] or not fields[label][1]:
                    self.add("ERROR", "PHASE_FIELD_MISSING", doc.path, start, f"{phase_id} requires a non-empty '{label}' field.")

            status_field = self.field(section, "Status")
            if not status_field:
                continue
            line_no, status = status_field
            phase_statuses[phase_id] = status_field
            if status not in PHASE_STATES:
                self.add("ERROR", "PHASE_STATUS_INVALID", doc.path, line_no, f"Invalid phase status: {status}")
            phase_tasks = [
                (match.group(2), number, match.group(1).lower() == "x")
                for number, line in section
                if (match := re.match(r"^\s*-\s+\[([ xX])\]\s+(TASK-\d{3}):\s+(.+?)\s*$", line))
            ]
            evidence = fields["Verification evidence"]
            evidence_missing = (
                not evidence
                or not evidence[1]
                or bool(re.search(r"not available|not run|none|pending", evidence[1], re.IGNORECASE))
            )
            checked = [task for task in phase_tasks if task[2]]
            if checked and evidence_missing:
                self.add(
                    "ERROR",
                    "CHECKED_TASK_NO_EVIDENCE",
                    doc.path,
                    checked[0][1],
                    f"{phase_id} has completed tasks without concrete phase verification evidence.",
                )
            if status == "done":
                unchecked = [(n, line) for n, line in section if re.match(r"^\s*-\s+\[ \]\s+TASK-", line)]
                if unchecked:
                    self.add("ERROR", "DONE_PHASE_HAS_OPEN_TASK", doc.path, unchecked[0][0], f"{phase_id} is done but still has unchecked tasks.")
                if evidence_missing:
                    self.add("ERROR", "DONE_PHASE_NO_EVIDENCE", doc.path, evidence[0] if evidence else start, f"{phase_id} is done without verification evidence.")

        status_doc = self.docs.get("PROJECT_STATUS.md")
        if not status_doc:
            return

        roadmap_lines = list(enumerate(doc.lines, start=1))
        status_lines = list(enumerate(status_doc.lines, start=1))
        roadmap_current = self.field(roadmap_lines, "Phase")
        status_current = self.field(status_lines, "Current phase")
        state_field = self.field(status_lines, "State")
        if not roadmap_current or not re.fullmatch(r"PHASE-\d{3}", roadmap_current[1]):
            self.add("ERROR", "ROADMAP_CURRENT_PHASE_INVALID", doc.path, roadmap_current[0] if roadmap_current else 1, "Roadmap Current phase requires one PHASE-### value.")
        elif roadmap_current[1] not in phase_statuses:
            self.add("ERROR", "ROADMAP_CURRENT_PHASE_UNKNOWN", doc.path, roadmap_current[0], f"Current phase is not defined: {roadmap_current[1]}")
        if not status_current or not re.fullmatch(r"PHASE-\d{3}", status_current[1]):
            self.add("ERROR", "STATUS_CURRENT_PHASE_INVALID", status_doc.path, status_current[0] if status_current else 1, "Status Snapshot requires one PHASE-### Current phase.")
        elif status_current[1] not in phase_statuses:
            self.add("ERROR", "STATUS_CURRENT_PHASE_UNKNOWN", status_doc.path, status_current[0], f"Status current phase is not defined in the roadmap: {status_current[1]}")
        if roadmap_current and status_current and roadmap_current[1] != status_current[1]:
            self.add("ERROR", "CURRENT_PHASE_MISMATCH", status_doc.path, status_current[0], "Roadmap and status Current phase values disagree.")

        active_phases = [phase_id for phase_id, (_, status) in phase_statuses.items() if status == "active"]
        if len(active_phases) > 1:
            self.add("ERROR", "MULTIPLE_ACTIVE_PHASES", doc.path, phase_statuses[active_phases[1]][0], "At most one roadmap phase may be active.")

        if not state_field or state_field[1] not in PROJECT_STATES:
            self.add("ERROR", "PROJECT_STATE_INVALID", status_doc.path, state_field[0] if state_field else 1, f"Project State must be one of: {', '.join(sorted(PROJECT_STATES))}.")
            return
        state = state_field[1]
        current_id = status_current[1] if status_current and status_current[1] in phase_statuses else None
        current_phase_state = phase_statuses[current_id][1] if current_id else None
        if state == "active" and (len(active_phases) != 1 or current_phase_state != "active"):
            self.add("ERROR", "ACTIVE_STATE_PHASE_MISMATCH", status_doc.path, state_field[0], "Active project state requires exactly one active roadmap phase matching Current phase.")
        elif state == "planning" and current_phase_state not in {"planned", "active"}:
            self.add("ERROR", "PLANNING_STATE_PHASE_MISMATCH", status_doc.path, state_field[0], "Planning project state requires the current phase to be planned or active.")
        elif state == "blocked" and current_phase_state != "blocked":
            self.add("ERROR", "BLOCKED_STATE_PHASE_MISMATCH", status_doc.path, state_field[0], "Blocked project state requires the current phase to be blocked.")
        elif state == "complete":
            if active_phases:
                self.add("ERROR", "COMPLETE_STATUS_HAS_ACTIVE_PHASE", status_doc.path, state_field[0], "Complete project state cannot have an active roadmap phase.")
            if any(not checked for _, _, checked in task_defs):
                self.add(
                    "ERROR",
                    "COMPLETE_STATUS_HAS_OPEN_ROADMAP_WORK",
                    status_doc.path,
                    state_field[0],
                    "Project status is complete while the roadmap still has unchecked tasks.",
                )

        if state == "blocked":
            headings = self.heading_map(status_doc).get("blockers", [])
            body = "\n".join(line for _, line in self.section(status_doc, headings[0])) if headings else ""
            if not body.strip() or re.fullmatch(r"\s*-?\s*(?:None\.?|없음\.?)\s*", body, re.IGNORECASE):
                self.add("ERROR", "BLOCKED_STATE_WITHOUT_BLOCKER", status_doc.path, headings[0] if headings else state_field[0], "Blocked project state requires a concrete blocker.")

    def check_decisions(self) -> None:
        doc = self.docs.get("DECISION_LOG.md")
        if not doc or not self.canonical:
            return
        sections = self.split_h3_sections(doc, r"DEC-\d{3}")
        ids = [item_id for item_id, _, _ in sections]
        for duplicate in sorted({item_id for item_id in ids if ids.count(item_id) > 1}):
            line = next(start for item_id, start, _ in sections if item_id == duplicate)
            self.add("ERROR", "DUPLICATE_DECISION_ID", doc.path, line, f"Duplicate decision ID: {duplicate}")

        by_id = {item_id: (start, section) for item_id, start, section in sections}
        records: dict[str, dict[str, object]] = {}
        for decision_id, start, section in sections:
            for label in (
                "Status",
                "Date",
                "Initiated by",
                "Context",
                "User intent/value protected",
                "Intervention",
                "Options considered",
                "Decision",
                "Consequences",
                "Reconsider when",
                "Supersedes",
                "Superseded by",
            ):
                value = self.field(section, label)
                if not value or not value[1]:
                    self.add("ERROR", "DECISION_FIELD_MISSING", doc.path, start, f"{decision_id} requires a non-empty '{label}' field.")
            status_field = self.field(section, "Status")
            if status_field and status_field[1] not in DECISION_STATES:
                self.add("ERROR", "DECISION_STATUS_INVALID", doc.path, status_field[0], f"Invalid decision status: {status_field[1]}")
            supersedes_field = self.field(section, "Supersedes")
            replacement_field = self.field(section, "Superseded by")
            links: dict[str, list[str]] = {}
            for label, value in (("Supersedes", supersedes_field), ("Superseded by", replacement_field)):
                raw = value[1].strip() if value else ""
                if raw.casefold() in {"none", "없음"}:
                    links[label] = []
                    continue
                linked_ids = re.findall(r"DEC-\d{3}", raw)
                residue = re.sub(r"DEC-\d{3}|[\s,;]", "", raw)
                if not linked_ids or residue:
                    self.add("ERROR", "DECISION_LINK_INVALID", doc.path, value[0] if value else start, f"{decision_id} has an invalid '{label}' value: {raw}")
                links[label] = linked_ids
                if len(linked_ids) != len(set(linked_ids)):
                    self.add("ERROR", "DUPLICATE_DECISION_LINK", doc.path, value[0] if value else start, f"{decision_id} repeats a decision ID in '{label}'.")
            records[decision_id] = {
                "start": start,
                "status": status_field[1] if status_field else "",
                "supersedes": links.get("Supersedes", []),
                "superseded_by": links.get("Superseded by", []),
            }

        for decision_id, record in records.items():
            status = str(record["status"])
            supersedes = list(record["supersedes"])
            superseded_by = list(record["superseded_by"])
            start = int(record["start"])
            if status == "superseded" and len(superseded_by) != 1:
                self.add("ERROR", "SUPERSEDED_WITHOUT_REPLACEMENT", doc.path, start, f"{decision_id} must name exactly one replacement decision.")
            if status in {"accepted", "proposed"} and superseded_by:
                self.add("ERROR", "ACTIVE_DECISION_HAS_REPLACEMENT", doc.path, start, f"{decision_id} links a replacement but is not marked superseded.")
            for target in supersedes:
                if target not in records:
                    self.add("ERROR", "UNKNOWN_SUPERSEDED_DECISION", doc.path, start, f"Superseded decision does not exist: {target}")
                    continue
                target_record = records[target]
                if target_record["status"] != "superseded":
                    self.add("ERROR", "SUPERSEDED_TARGET_STATUS_INVALID", doc.path, int(target_record["start"]), f"{target} must be marked superseded.")
                if decision_id not in target_record["superseded_by"]:
                    self.add("ERROR", "MISSING_SUPERSEDED_BY_BACKLINK", doc.path, int(target_record["start"]), f"{target} must link to {decision_id} in Superseded by.")
            for target in superseded_by:
                if target not in records:
                    self.add("ERROR", "UNKNOWN_REPLACEMENT_DECISION", doc.path, start, f"Replacement decision does not exist: {target}")
                    continue
                if decision_id not in records[target]["supersedes"]:
                    self.add("ERROR", "MISSING_SUPERSEDES_BACKLINK", doc.path, int(records[target]["start"]), f"{target} must link back to {decision_id} in Supersedes.")

        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(decision_id: str, trail: list[str]) -> None:
            if decision_id in visiting:
                cycle = " -> ".join(trail + [decision_id])
                self.add("ERROR", "DECISION_SUPERSEDE_CYCLE", doc.path, int(records[decision_id]["start"]), f"Decision supersede cycle detected: {cycle}")
                return
            if decision_id in visited:
                return
            visiting.add(decision_id)
            for target in records[decision_id]["superseded_by"]:
                if target in records:
                    visit(str(target), trail + [decision_id])
            visiting.remove(decision_id)
            visited.add(decision_id)

        for decision_id in records:
            visit(decision_id, [])

    def check_links(self) -> None:
        link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        for doc in self.docs.values():
            for line_no, line in enumerate(doc.lines, start=1):
                for match in link_pattern.finditer(line):
                    destination = match.group(1).strip()
                    if destination.startswith("<") and ">" in destination:
                        raw = destination[1 : destination.index(">")]
                    else:
                        raw = destination.split()[0]
                    if not raw or raw.startswith(("#", "http://", "https://", "mailto:", "app://", "chatgpt-")):
                        continue
                    target_text = unquote(raw.split("#", 1)[0])
                    target = Path(target_text)
                    if not target.is_absolute():
                        target = (doc.path.parent / target).resolve()
                    if not target.exists():
                        self.add("ERROR", "BROKEN_LOCAL_LINK", doc.path, line_no, f"Local link target does not exist: {raw}")

    def check_agents(self) -> None:
        path = self.root / "AGENTS.md"
        if not path.is_file():
            self.add("WARNING", "AGENTS_MISSING", path, 1, "No AGENTS.md routes future sessions to the project record.")
            return
        try:
            text = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as exc:
            self.add("ERROR", "AGENTS_UNREADABLE", path, 1, str(exc))
            return
        start = text.count(START_MARKER)
        end = text.count(END_MARKER)
        if start != end:
            self.add("ERROR", "AGENTS_MARKER_MISMATCH", path, 1, "Managed AGENTS snippet markers are unbalanced.")
        if self.canonical and start == 0:
            severity = "ERROR" if self.strict == "full" else "WARNING"
            self.add(severity, "AGENTS_ROUTING_MISSING", path, 1, "AGENTS.md does not contain the managed project-record routing snippet.")

    def run(self) -> list[Issue]:
        if not self.load():
            return self.issues
        self.check_required_headings()
        self.check_placeholders()
        self.check_stale_head_claims()
        next_task_id = self.check_next_task()
        self.check_roadmap(next_task_id)
        self.check_decisions()
        self.check_links()
        self.check_agents()
        return self.issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate canonical project operating documents.")
    parser.add_argument("--root", required=True, type=Path, help="Project root")
    parser.add_argument("--strict", choices=("full", "delta", "lite"), default="full")
    parser.add_argument("--compat", choices=("auto", "canonical"), default="auto")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: project root does not exist or is not a directory: {root}", file=sys.stderr)
        return 2
    validator = Validator(root, args.strict, args.compat)
    issues = validator.run()
    errors = sum(issue.severity == "ERROR" for issue in issues)
    warnings = sum(issue.severity == "WARNING" for issue in issues)

    if args.json:
        print(json.dumps({"root": str(root), "errors": errors, "warnings": warnings, "issues": [asdict(issue) for issue in issues]}, ensure_ascii=False, indent=2))
    else:
        for issue in issues:
            print(f"{issue.severity} {issue.code} {issue.path}:{issue.line} {issue.message}")
        print(f"Validation {'FAILED' if errors else 'PASSED'}: errors={errors} warnings={warnings}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
