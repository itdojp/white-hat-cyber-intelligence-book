#!/usr/bin/env python3
"""Fail-closed Chapter 4 publication, traceability, and safety contract."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.content_safety_policy import (  # noqa: E402
    POLICY_VERSION as CONTENT_SAFETY_POLICY_VERSION,
    SafetyFinding,
    scan_fields,
)
from scripts.render_reference_baseline import render as render_reference_baseline  # noqa: E402
from scripts.sync_book_site import SitePageRegistryError, parse_registry_data  # noqa: E402

ERRORS: list[str] = []
EXPECTED_POLICY_VERSION = "1.2.0"

CHAPTER = "manuscript/04-assets-boundaries-threat-model.md"
TEMPLATE = "templates/threat-model.md"
CASE = "cases/ch04-threat-model-example.md"
SOURCE_NOTE = "references/ch04-source-review-2026-08-08.md"

EXPECTED_PAGES = {
    (CHAPTER, "chapters/chapter-04/index.md", "chapters", 47),
    (TEMPLATE, "templates/threat-model/index.md", "additional", 150),
    (CASE, "cases/chapter-04-threat-model/index.md", "additional", 241),
    (SOURCE_NOTE, "references/chapter-04-source-review/index.md", "additional", 242),
}

MODEL_STATUSES = {
    "Draft",
    "In Review",
    "Approved for Assessment",
    "Needs Evidence",
    "Superseded",
}
ASSET_TYPES = {
    "Business Outcome",
    "Service",
    "Component",
    "Data",
    "Identity",
    "Control Plane",
    "Evidence",
}
KNOWLEDGE_STATES = {"Unknown", "Assumed", "Confirmed", "Not Applicable"}
FLOW_TYPES = {"Data", "Identity", "Control"}
COLLECTED_EVIDENCE_STATUSES = {"Planned", "Collected", "Rejected", "Inconclusive"}
GAP_STATUSES = {"Open", "Accepted temporarily", "Escalated", "Closed"}
BOUNDARY_TYPES = {
    "Identity Authority",
    "Data Ownership",
    "Administrative Control",
    "Tenant",
    "Third-party Responsibility",
    "Control Plane",
    "Network",
}
HYPOTHESIS_STATUSES = {
    "Candidate",
    "Supported",
    "Partially Supported",
    "Disconfirmed",
    "Inconclusive",
}
ASSURANCE_STATES = {"Unknown", "Documented", "Implemented", "Observed", "Validated"}
EVIDENCE_REQUIREMENT_STATUSES = {"Required", "Deferred", "Replaced", "Not Applicable"}
EXPECTED_SOURCE_IDS = {"SRC-CSF-001", "SRC-NIST-RISK-001", "SRC-OWASP-TM-001"}

EXPECTED_CASE_IDS: dict[str, set[str]] = {
    "ASSET": {f"ASSET-2026-{number:03d}" for number in range(1, 8)},
    "FLOW": {f"FLOW-2026-{number:03d}" for number in range(1, 7)},
    "TB": {f"TB-2026-{number:03d}" for number in range(1, 8)},
    "EXP": {f"EXP-2026-{number:03d}" for number in range(1, 4)},
    "EP": {f"EP-2026-{number:03d}" for number in range(1, 4)},
    "TH": {f"TH-2026-{number:03d}" for number in range(1, 4)},
    "MISUSE": {f"MISUSE-2026-{number:03d}" for number in range(1, 3)},
    "PATH": {f"PATH-2026-{number:03d}" for number in range(1, 3)},
    "EDGE": {f"EDGE-2026-{number:03d}" for number in range(1, 8)},
    "CTRL": {f"CTRL-2026-{number:03d}" for number in range(1, 6)},
    "ASM": {f"ASM-2026-{number:03d}" for number in range(1, 4)},
    "GAP": {f"GAP-2026-{number:03d}" for number in range(1, 4)},
    "EREQ": {f"EREQ-2026-{number:03d}" for number in range(1, 4)},
    "ACT-TM": {f"ACT-TM-2026-{number:03d}" for number in range(1, 6)},
    "REA-TM": {f"REA-TM-2026-{number:03d}" for number in range(1, 4)},
}

EXPECTED_DEPENDENCY_IDS = {f"DEP-2026-{number:03d}" for number in range(1, 6)}
EXPECTED_RUBRIC_IDS = {f"RUBRIC-TM-2026-{number:03d}" for number in range(1, 6)}
EXPECTED_INHERITED_EVIDENCE_IDS = {
    "EVD-2026-001",
    "EVD-2026-002",
    "EVD-2026-003",
    "EVD-2026-004",
    "EVD-AUTH-2026-001",
    "NEG-2026-001",
}
EXPECTED_INHERITED_COLLECTED_EVIDENCE_IDS = EXPECTED_INHERITED_EVIDENCE_IDS - {"NEG-2026-001"}
INHERITED_REVIEWER_VALUE = "Not recorded in inherited source"
INHERITED_TH_003_PROPOSITION = "既に同型の不正利用が発生した"
EXPECTED_HANDOFF_ROWS = {
    "HO-TM-2026-005": ("第5章 ATT&CK", "Behavior記述"),
    "HO-TM-2026-006": ("第6章 観測可能性", "Telemetry / logging設計"),
    "HO-TM-2026-009": ("第9章 RoE", "Rules of Engagement"),
    "HO-TM-2026-011": ("第11章 Web/API評価", "Web/API Assessment Hypothesis Pack"),
    "HO-TM-2026-012": ("第12章 Identity評価", "Identity Attack Path Review"),
    "HO-TM-2026-013": ("第13章 Platform / Supply Chain", "Platform and Supply Chain Assessment"),
    "HO-TM-2026-014": ("第14章 最小影響Validation", "Minimal-Impact Validation Record"),
    "HO-TM-2026-015": ("第15章 Finding / Retest", "Finding Report、Retest Record"),
    "HO-TM-2026-027": ("第27章 AI / Agent固有Threat Model", "AI / Agent Threat Model拡張"),
}
EXPECTED_HANDOFF_IDS = set(EXPECTED_HANDOFF_ROWS)

DOCUMENT_CONTROL_FIELDS = (
    "Artifact ID",
    "Threat Model ID",
    "Parent Case ID",
    "Relation",
    "Decision Requirement ID",
    "Authorization Record ID",
    "Title",
    "Model status",
    "Owner",
    "Decision owner",
    "Contributors",
    "Reviewers",
    "Classification",
    "Created",
    "Updated",
    "Review deadline",
    "Reassessment date",
    "Related Issue / Ticket",
)

DECISION_CONTEXT_FIELDS = (
    "Decision Requirement ID",
    "Business process",
    "Decision to support",
    "Decision deadline",
    "In-scope environment",
    "Out-of-scope environment",
    "Scope statement",
    "Non-goals",
    "Business criticality scale",
    "Safety boundary",
    "Minimum sufficient evidence standard",
    "Overcollection boundary",
    "Reassessment trigger summary",
)

GAP_HEADER = (
    "Gap ID",
    "Missing information / control / telemetry",
    "Decision affected",
    "Owner",
    "Due date",
    "Status",
    "Evidence Requirement ID",
    "Action ID",
    "Reassessment ID",
)

COLLECTED_EVIDENCE_HEADER = (
    "Evidence ID",
    "Related Evidence Requirement IDs",
    "Evidence description",
    "Collection conditions / provenance",
    "Status",
    "Reviewer",
    "Collected at",
    "Limitation",
)

HANDOFF_HEADER = (
    "Handoff ID",
    "Target chapter",
    "Deliverable / consumer",
    "What this artifact provides",
    "Acceptance criteria",
    "Reject / return condition",
)

FIELD_VALUE_HEADER = ("Field", "Value")
STATE_FAMILY_HEADER = ("State family", "Exact finite values", "Current usage")
ASSET_HEADER = (
    "Asset ID",
    "Type",
    "Name",
    "Business role / outcome",
    "Owner",
    "Criticality",
    "Data classification",
    "Knowledge state",
    "Evidence IDs",
    "Dependency IDs",
)
DEPENDENCY_HEADER = (
    "Dependency ID",
    "From asset",
    "To asset",
    "Why the dependency matters",
    "Failure consequence",
)
FLOW_HEADER = (
    "Flow ID",
    "Flow type",
    "Source Asset ID",
    "Destination Asset ID",
    "Purpose",
    "Protocol class",
    "Identity / authorization context",
    "Boundary IDs crossed",
    "Data classification",
    "Evidence status",
    "Observation point",
)
BOUNDARY_HEADER = (
    "Boundary ID",
    "Boundary type",
    "From / To",
    "Owner(s)",
    "Trust / authority change",
    "Crossing condition",
    "Control",
    "Failure consequence",
    "Knowledge state",
    "Evidence IDs",
)
EXPOSURE_HEADER = (
    "Exposure ID",
    "Related Asset / Boundary / Flow IDs",
    "Entry Point ID",
    "Reachability class",
    "External dependency",
    "Required authority",
    "Verification status",
    "Evidence ID",
    "Gap ID",
)
ENTRY_POINT_HEADER = (
    "Entry Point ID",
    "Related Exposure IDs",
    "Interface class",
    "Description",
    "Owner",
    "Boundary IDs",
    "Required authority",
    "Observation point",
    "Knowledge state",
    "Evidence IDs",
)
HYPOTHESIS_HEADER = (
    "Hypothesis ID",
    "Decision Requirement ID",
    "Related Asset IDs",
    "Boundary / Flow / Exposure IDs",
    "Statement",
    "Preconditions",
    "Expected impact",
    "Evidence needed",
    "Alternative explanation",
    "Priority",
    "Hypothesis status",
)
MISUSE_HEADER = (
    "Misuse Case ID",
    "Goal",
    "Actor capability class",
    "Preconditions",
    "Affected assets",
    "Boundary crossed",
    "Expected outcome",
    "Observation points",
    "Excluded operational detail",
)
PATH_SUMMARY_HEADER = (
    "Path ID",
    "Related Threat IDs",
    "Entry condition",
    "Intermediate condition",
    "Undesired end state",
    "Safety note",
)
ATTACK_PATH_HEADER = (
    "Attack Path ID",
    "Edge ID",
    "From Asset / State",
    "Condition",
    "Boundary ID",
    "To Asset / State",
    "Affected Asset IDs",
    "Expected impact",
    "Observation point",
    "Required Evidence ID",
    "Knowledge state",
)
CONTROL_HEADER = (
    "Control ID",
    "Related Asset / Boundary / Threat / Path IDs",
    "Control statement",
    "Owner",
    "Assurance state",
    "Evidence IDs",
    "Limitation",
    "Gap ID",
    "Reassessment trigger",
)
ASSUMPTION_HEADER = (
    "Assumption ID",
    "Statement",
    "Owner",
    "Validation method",
    "Due date",
    "Status",
    "Related IDs",
)
EVIDENCE_REQUIREMENT_HEADER = (
    "Evidence Requirement ID",
    "Question",
    "Related Threat / Control / Gap",
    "Minimum sufficient evidence",
    "Forbidden / over-collection boundary",
    "Owner",
    "Due date",
    "Status",
    "Resulting Evidence IDs",
)
ACTION_HEADER = (
    "Action ID",
    "Related Gap / Control / Threat",
    "Action",
    "Owner",
    "Due date",
    "Success evidence",
    "Status",
)
REASSESSMENT_HEADER = (
    "Reassessment ID",
    "Trigger",
    "Scope",
    "Owner",
    "Scheduled date",
    "Inputs required",
    "Closure criteria",
    "Destination chapter / artifact",
)
REVIEW_HEADER = (
    "Review area",
    "Reviewer / role",
    "Rubric",
    "Result",
    "Date",
    "Evidence reference",
    "Notes",
)
RUBRIC_HEADER = ("Rubric ID", "Criterion", "Meets", "Partially meets", "Does not meet")
LIMITATION_HEADER = (
    "Limitation ID",
    "Scope / condition",
    "Unsupported claim",
    "Owner",
    "Reassessment trigger",
)
NEGATIVE_FINDING_HEADER = (
    "Negative Finding ID",
    "Related Evidence IDs",
    "Searched behavior",
    "Search window",
    "Available coverage",
    "Gaps",
    "Permitted conclusion",
)

FIELD_STRUCTURAL = "structural identifier/reference"
FIELD_FINITE = "finite enum/date/metadata"
FIELD_READER_VISIBLE = "reader-visible descriptive/action-bearing"
FIELD_CLASSES = {FIELD_STRUCTURAL, FIELD_FINITE, FIELD_READER_VISIBLE}


@dataclass(frozen=True)
class TableSafetyPolicy:
    """Finite field classification for one public ART-03 Markdown table."""

    header: tuple[str, ...]
    classifications: tuple[tuple[str, str], ...]

    @property
    def reader_visible(self) -> tuple[str, ...]:
        return tuple(name for name, classification in self.classifications if classification == FIELD_READER_VISIBLE)

    @property
    def scan_required(self) -> tuple[str, ...]:
        # Every table cell is public. Structural and finite fields are also
        # scanned as defense in depth so an identifier or date with appended
        # action prose cannot bypass the adapter before structural validation.
        return tuple(name for name, _ in self.classifications)


@dataclass(frozen=True)
class MarkdownTable:
    header: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]
    line: int


def table_safety_policy(
    header: tuple[str, ...],
    *,
    structural: tuple[str, ...],
    finite: tuple[str, ...],
    reader_visible: tuple[str, ...],
) -> TableSafetyPolicy:
    classified = structural + finite + reader_visible
    if len(classified) != len(set(classified)) or set(classified) != set(header):
        raise RuntimeError(f"invalid Chapter 4 table safety classification for {header!r}: {classified!r}")
    classes = {
        **{name: FIELD_STRUCTURAL for name in structural},
        **{name: FIELD_FINITE for name in finite},
        **{name: FIELD_READER_VISIBLE for name in reader_visible},
    }
    classifications = tuple((name, classes[name]) for name in header)
    if {classification for _, classification in classifications} - FIELD_CLASSES:
        raise RuntimeError(f"unknown Chapter 4 safety field class for {header!r}")
    return TableSafetyPolicy(header=header, classifications=classifications)


TABLE_SAFETY_POLICIES = {
    policy.header: policy
    for policy in (
        table_safety_policy(
            FIELD_VALUE_HEADER,
            structural=("Field",),
            finite=(),
            reader_visible=("Value",),
        ),
        table_safety_policy(
            STATE_FAMILY_HEADER,
            structural=("State family",),
            finite=("Exact finite values",),
            reader_visible=("Current usage",),
        ),
        table_safety_policy(
            ASSET_HEADER,
            structural=("Asset ID", "Evidence IDs", "Dependency IDs"),
            finite=("Type", "Criticality", "Data classification", "Knowledge state"),
            reader_visible=("Name", "Business role / outcome", "Owner"),
        ),
        table_safety_policy(
            DEPENDENCY_HEADER,
            structural=("Dependency ID", "From asset", "To asset"),
            finite=(),
            reader_visible=("Why the dependency matters", "Failure consequence"),
        ),
        table_safety_policy(
            FLOW_HEADER,
            structural=("Flow ID", "Source Asset ID", "Destination Asset ID", "Boundary IDs crossed"),
            finite=("Flow type", "Data classification", "Evidence status"),
            reader_visible=("Purpose", "Protocol class", "Identity / authorization context", "Observation point"),
        ),
        table_safety_policy(
            BOUNDARY_HEADER,
            structural=("Boundary ID", "Evidence IDs"),
            finite=("Boundary type", "Knowledge state"),
            reader_visible=(
                "From / To",
                "Owner(s)",
                "Trust / authority change",
                "Crossing condition",
                "Control",
                "Failure consequence",
            ),
        ),
        table_safety_policy(
            EXPOSURE_HEADER,
            structural=(
                "Exposure ID",
                "Related Asset / Boundary / Flow IDs",
                "Entry Point ID",
                "Evidence ID",
                "Gap ID",
            ),
            finite=("Verification status",),
            reader_visible=("Reachability class", "External dependency", "Required authority"),
        ),
        table_safety_policy(
            ENTRY_POINT_HEADER,
            structural=("Entry Point ID", "Related Exposure IDs", "Boundary IDs", "Evidence IDs"),
            finite=("Knowledge state",),
            reader_visible=("Interface class", "Description", "Owner", "Required authority", "Observation point"),
        ),
        table_safety_policy(
            HYPOTHESIS_HEADER,
            structural=("Hypothesis ID", "Decision Requirement ID", "Related Asset IDs", "Boundary / Flow / Exposure IDs"),
            finite=("Priority", "Hypothesis status"),
            reader_visible=("Statement", "Preconditions", "Expected impact", "Evidence needed", "Alternative explanation"),
        ),
        table_safety_policy(
            MISUSE_HEADER,
            structural=("Misuse Case ID", "Affected assets", "Boundary crossed"),
            finite=(),
            reader_visible=(
                "Goal",
                "Actor capability class",
                "Preconditions",
                "Expected outcome",
                "Observation points",
                "Excluded operational detail",
            ),
        ),
        table_safety_policy(
            PATH_SUMMARY_HEADER,
            structural=("Path ID", "Related Threat IDs"),
            finite=(),
            reader_visible=("Entry condition", "Intermediate condition", "Undesired end state", "Safety note"),
        ),
        table_safety_policy(
            ATTACK_PATH_HEADER,
            structural=("Attack Path ID", "Edge ID", "Boundary ID", "Affected Asset IDs", "Required Evidence ID"),
            finite=("Knowledge state",),
            reader_visible=("From Asset / State", "Condition", "To Asset / State", "Expected impact", "Observation point"),
        ),
        table_safety_policy(
            CONTROL_HEADER,
            structural=("Control ID", "Related Asset / Boundary / Threat / Path IDs", "Evidence IDs", "Gap ID"),
            finite=("Assurance state",),
            reader_visible=("Control statement", "Owner", "Limitation", "Reassessment trigger"),
        ),
        table_safety_policy(
            ASSUMPTION_HEADER,
            structural=("Assumption ID", "Related IDs"),
            finite=("Due date", "Status"),
            reader_visible=("Statement", "Owner", "Validation method"),
        ),
        table_safety_policy(
            GAP_HEADER,
            structural=("Gap ID", "Evidence Requirement ID", "Action ID", "Reassessment ID"),
            finite=("Due date", "Status"),
            reader_visible=("Missing information / control / telemetry", "Decision affected", "Owner"),
        ),
        table_safety_policy(
            EVIDENCE_REQUIREMENT_HEADER,
            structural=("Evidence Requirement ID", "Related Threat / Control / Gap", "Resulting Evidence IDs"),
            finite=("Due date", "Status"),
            reader_visible=("Question", "Minimum sufficient evidence", "Forbidden / over-collection boundary", "Owner"),
        ),
        table_safety_policy(
            COLLECTED_EVIDENCE_HEADER,
            structural=("Evidence ID", "Related Evidence Requirement IDs"),
            finite=("Status", "Collected at"),
            reader_visible=("Evidence description", "Collection conditions / provenance", "Reviewer", "Limitation"),
        ),
        table_safety_policy(
            NEGATIVE_FINDING_HEADER,
            structural=("Negative Finding ID", "Related Evidence IDs"),
            finite=(),
            reader_visible=("Searched behavior", "Search window", "Available coverage", "Gaps", "Permitted conclusion"),
        ),
        table_safety_policy(
            ACTION_HEADER,
            structural=("Action ID", "Related Gap / Control / Threat"),
            finite=("Due date", "Status"),
            reader_visible=("Action", "Owner", "Success evidence"),
        ),
        table_safety_policy(
            REASSESSMENT_HEADER,
            structural=("Reassessment ID",),
            finite=("Scheduled date",),
            reader_visible=("Trigger", "Scope", "Owner", "Inputs required", "Closure criteria", "Destination chapter / artifact"),
        ),
        table_safety_policy(
            HANDOFF_HEADER,
            structural=("Handoff ID",),
            finite=(),
            reader_visible=("Target chapter", "Deliverable / consumer", "What this artifact provides", "Acceptance criteria", "Reject / return condition"),
        ),
        table_safety_policy(
            REVIEW_HEADER,
            structural=("Evidence reference",),
            finite=("Result", "Date"),
            reader_visible=("Review area", "Reviewer / role", "Rubric", "Notes"),
        ),
        table_safety_policy(
            RUBRIC_HEADER,
            structural=("Rubric ID",),
            finite=(),
            reader_visible=("Criterion", "Meets", "Partially meets", "Does not meet"),
        ),
        table_safety_policy(
            LIMITATION_HEADER,
            structural=("Limitation ID",),
            finite=(),
            reader_visible=("Scope / condition", "Unsupported claim", "Owner", "Reassessment trigger"),
        ),
    )
}

TEMPLATE_TABLE_OCCURRENCES = {
    header: (2 if header == FIELD_VALUE_HEADER else 1)
    for header in (
        FIELD_VALUE_HEADER,
        ASSET_HEADER,
        DEPENDENCY_HEADER,
        FLOW_HEADER,
        BOUNDARY_HEADER,
        EXPOSURE_HEADER,
        ENTRY_POINT_HEADER,
        HYPOTHESIS_HEADER,
        MISUSE_HEADER,
        ATTACK_PATH_HEADER,
        CONTROL_HEADER,
        ASSUMPTION_HEADER,
        GAP_HEADER,
        EVIDENCE_REQUIREMENT_HEADER,
        COLLECTED_EVIDENCE_HEADER,
        ACTION_HEADER,
        REASSESSMENT_HEADER,
        REVIEW_HEADER,
        RUBRIC_HEADER,
        LIMITATION_HEADER,
    )
}

CASE_TABLE_OCCURRENCES = {
    header: (3 if header == FIELD_VALUE_HEADER else 1)
    for header in (
        FIELD_VALUE_HEADER,
        STATE_FAMILY_HEADER,
        ASSET_HEADER,
        DEPENDENCY_HEADER,
        FLOW_HEADER,
        BOUNDARY_HEADER,
        EXPOSURE_HEADER,
        ENTRY_POINT_HEADER,
        HYPOTHESIS_HEADER,
        MISUSE_HEADER,
        PATH_SUMMARY_HEADER,
        ATTACK_PATH_HEADER,
        CONTROL_HEADER,
        ASSUMPTION_HEADER,
        GAP_HEADER,
        EVIDENCE_REQUIREMENT_HEADER,
        COLLECTED_EVIDENCE_HEADER,
        NEGATIVE_FINDING_HEADER,
        ACTION_HEADER,
        REASSESSMENT_HEADER,
        HANDOFF_HEADER,
        RUBRIC_HEADER,
        REVIEW_HEADER,
    )
}

EXPECTED_HEADINGS = (
    "# 第4章 資産、信頼境界、攻撃面、脅威モデル",
    "## この章の位置付け",
    "## 学習目標",
    "## 前提知識",
    "## 導入Case",
    "## 本章の責任境界",
    "### OWN",
    "### BRIDGE",
    "### DELEGATE",
    "## 安全な演習",
    "## 作成する成果物",
    "## 評価基準",
    "## よくある誤解",
    "## 章のまとめ",
    "## 次に学ぶこと",
    "## 参考資料",
)

EXPECTED_TEMPLATE_HEADINGS = tuple(
    f"## {number}. {title}"
    for number, title in enumerate(
        (
            "Document Control",
            "Decision Context",
            "Asset Register",
            "Flow Register",
            "Trust Boundary Register",
            "Exposure and Entry Point Register",
            "Threat Hypothesis and Misuse Case",
            "Attack Path Register",
            "Control Assurance Register",
            "Assumptions, Unknowns and Gaps",
            "Evidence Requirements and Actions",
            "Reassessment and Handoff",
            "Review and Rubric",
        )
    )
)

EXPECTED_CASE_HEADINGS = ("## この記入例の扱い",) + EXPECTED_TEMPLATE_HEADINGS


def error(message: str) -> None:
    ERRORS.append(message)


def read_text(relative: str) -> str:
    path = ROOT / relative
    if not path.is_file():
        error(f"missing required file: {relative}")
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        error(f"{relative}: not valid UTF-8: {exc}")
        return ""


def load_json(relative: str) -> dict:
    text = read_text(relative)
    if not text:
        return {}
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        error(f"{relative}: invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        error(f"{relative}: root must be an object")
        return {}
    return value


def require_tokens(label: str, text: str, tokens: tuple[str, ...]) -> list[str]:
    return [f"{label}: missing required token {token!r}" for token in tokens if token not in text]


def require_order(label: str, text: str, tokens: tuple[str, ...]) -> list[str]:
    positions: list[int] = []
    messages: list[str] = []
    for token in tokens:
        matches = list(re.finditer(rf"^{re.escape(token)}\s*$", text, re.MULTILINE))
        if len(matches) != 1:
            messages.append(f"{label}: missing ordered token {token!r}")
        positions.append(matches[0].start() if matches else -1)
    present = [position for position in positions if position >= 0]
    if present != sorted(present):
        messages.append(f"{label}: required headings are out of order")
    return messages


def source_ids(text: str) -> set[str]:
    return set(re.findall(r"\bSRC-[A-Z0-9-]+\b", text))


def markdown_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def table_by_header(text: str, header: tuple[str, ...], label: str) -> tuple[list[list[str]], list[str]]:
    messages: list[str] = []
    expected = "| " + " | ".join(header) + " |"
    lines = text.splitlines()
    indexes = [index for index, line in enumerate(lines) if line.strip() == expected]
    if len(indexes) != 1:
        messages.append(f"{label}: expected table header exactly once: {expected!r}; found {len(indexes)}")
        return [], messages
    index = indexes[0]
    if index + 1 >= len(lines):
        messages.append(f"{label}: missing table separator after {expected!r}")
        return [], messages
    separator = markdown_cells(lines[index + 1])
    if len(separator) != len(header) or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator):
        messages.append(f"{label}: invalid table separator after {expected!r}")
    rows: list[list[str]] = []
    for line in lines[index + 2 :]:
        if not line.strip().startswith("|"):
            break
        cells = markdown_cells(line)
        if len(cells) != len(header):
            messages.append(f"{label}: malformed row for {expected!r}: {cells!r}")
        else:
            rows.append(cells)
    return rows, messages


def section(text: str, heading: str, next_heading_level: int = 2) -> str:
    match = re.search(
        rf"^{re.escape(heading)}\s*$\n(?P<body>.*?)(?=^{'#' * next_heading_level} |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group("body") if match else ""


def format_finding(finding: SafetyFinding) -> str:
    return (
        f"{finding.location}: [{finding.category}] {finding.reason}: "
        f"{finding.normalized_excerpt!r} (Policy {finding.policy_version})"
    )


def policy_errors(fields: list[tuple[str, str]]) -> list[str]:
    return [format_finding(finding) for finding in scan_fields(fields)]


def markdown_tables(text: str, label: str) -> tuple[list[MarkdownTable], list[str]]:
    """Parse every Markdown table in document order without guessing its semantics."""

    lines = text.splitlines()
    tables: list[MarkdownTable] = []
    messages: list[str] = []
    for index, line in enumerate(lines[:-1]):
        if not line.strip().startswith("|"):
            continue
        header = tuple(markdown_cells(line))
        separator = markdown_cells(lines[index + 1])
        if len(separator) != len(header) or not all(
            re.fullmatch(r":?-{3,}:?", cell) for cell in separator
        ):
            continue
        rows: list[tuple[str, ...]] = []
        for row_line in lines[index + 2 :]:
            if not row_line.strip().startswith("|"):
                break
            row = tuple(markdown_cells(row_line))
            if len(row) != len(header):
                messages.append(
                    f"{label}:{index + 1}: malformed safety-adapter row for {header!r}: {row!r}"
                )
                continue
            rows.append(row)
        tables.append(MarkdownTable(header=header, rows=tuple(rows), line=index + 1))
    return tables, messages


def adapter_field_location(
    label: str,
    table: MarkdownTable,
    occurrence: int,
    column: str,
    row: int,
) -> str:
    return f"{label}:{table.line} {table.header[0]}[{occurrence}] {column} row {row}"


def classified_table_fields(
    text: str,
    label: str,
    expected_occurrences: dict[tuple[str, ...], int],
) -> tuple[list[tuple[str, str]], list[str]]:
    """Select all public fields through one finite Template/Case manifest.

    A new or renamed table/column cannot silently bypass Policy 1.2.0: the
    complete observed header inventory and its occurrence count must match the
    document-specific contract, and every column is explicitly classified.
    """

    tables, messages = markdown_tables(text, label)
    counts = Counter(table.header for table in tables)
    observed_headers = set(counts)
    expected_headers = set(expected_occurrences)
    for header in sorted(observed_headers - expected_headers):
        messages.append(f"{label}: unclassified public table header: {header!r}")
    for header in sorted(expected_headers - observed_headers):
        messages.append(f"{label}: missing classified public table header: {header!r}")
    for header, expected_count in expected_occurrences.items():
        if counts[header] != expected_count:
            messages.append(
                f"{label}: classified table occurrence count for {header!r} "
                f"is {counts[header]}, expected {expected_count}"
            )

    fields: list[tuple[str, str]] = []
    occurrences: Counter[tuple[str, ...]] = Counter()
    for table in tables:
        occurrences[table.header] += 1
        policy = TABLE_SAFETY_POLICIES.get(table.header)
        if policy is None or table.header not in expected_occurrences:
            continue
        if tuple(name for name, _ in policy.classifications) != table.header:
            messages.append(f"{label}: field-classification order drift for {table.header!r}")
            continue
        for row_index, row in enumerate(table.rows, start=1):
            for column in policy.scan_required:
                column_index = table.header.index(column)
                value = row[column_index]
                if value:
                    fields.append(
                        (
                            adapter_field_location(
                                label,
                                table,
                                occurrences[table.header],
                                column,
                                row_index,
                            ),
                            value,
                        )
                    )
    return fields, messages


def mutate_table_cell(
    text: str,
    header: tuple[str, ...],
    occurrence: int,
    row: int,
    column: str,
    replacement: str,
) -> str:
    """Replace one data cell in a specific table occurrence for a regression."""

    expected = "| " + " | ".join(header) + " |"
    lines = text.splitlines()
    matches = [index for index, line in enumerate(lines) if line.strip() == expected]
    if occurrence < 1 or occurrence > len(matches):
        return text
    row_index = matches[occurrence - 1] + 1 + row
    if row_index >= len(lines) or not lines[row_index].strip().startswith("|"):
        return text
    cells = markdown_cells(lines[row_index])
    if len(cells) != len(header) or column not in header:
        return text
    cells[header.index(column)] = replacement
    lines[row_index] = "| " + " | ".join(cells) + " |"
    suffix = "\n" if text.endswith("\n") else ""
    return "\n".join(lines) + suffix


def safety_matrix_negative_regressions(
    text: str,
    label: str,
    expected_occurrences: dict[tuple[str, ...], int],
) -> None:
    """Prove every classified public field reaches Policy 1.2.0."""

    unsafe = "第三者の本番システムへ接続する"
    canonical_tables, canonical_messages = markdown_tables(text, label)
    if canonical_messages:
        error(f"{label}: cannot generate field-matrix regressions: {canonical_messages!r}")
        return
    canonical_by_key: dict[tuple[tuple[str, ...], int], MarkdownTable] = {}
    occurrences: Counter[tuple[str, ...]] = Counter()
    for table in canonical_tables:
        occurrences[table.header] += 1
        canonical_by_key[(table.header, occurrences[table.header])] = table

    mutation = text
    target_locations: set[str] = set()
    for header, count in expected_occurrences.items():
        policy = TABLE_SAFETY_POLICIES[header]
        for occurrence in range(1, count + 1):
            table = canonical_by_key.get((header, occurrence))
            if table is None or not table.rows:
                error(f"{label}: missing table row for field-matrix regression {header!r}[{occurrence}]")
                continue
            for row_index in range(1, len(table.rows) + 1):
                for column in policy.scan_required:
                    updated = mutate_table_cell(
                        mutation,
                        header,
                        occurrence,
                        row_index,
                        column,
                        unsafe,
                    )
                    if updated == mutation:
                        error(
                            f"{label}: field-matrix mutation did not change "
                            f"{header!r}[{occurrence}] row {row_index} {column!r}"
                        )
                        continue
                    mutation = updated
                    target_locations.add(
                        adapter_field_location(
                            f"negative {label}", table, occurrence, column, row_index
                        )
                    )
    fields, adapter_messages = classified_table_fields(
        mutation, f"negative {label}", expected_occurrences
    )
    if adapter_messages:
        error(f"{label}: field-matrix mutation invalidated adapter structure: {adapter_messages!r}")
        return
    finding_locations = {finding.location for finding in scan_fields(fields)}
    missing = sorted(target_locations - finding_locations)
    if missing:
        error(f"{label}: public fields bypassed Policy 1.2.0: {missing!r}")


def chapter_contract_errors(text: str, label: str) -> list[str]:
    messages: list[str] = []
    messages.extend(require_order(label, text, EXPECTED_HEADINGS))
    required = (
        "Decision Requirement\n→ Business Outcome / Asset",
        "→ Evidence Requirement / Action / Reassessment",
        "Componentを列挙するだけでは",
        "`Business Asset`は8番目のTypeではなく",
        "Network segmentはBoundary候補に過ぎない",
        "Threat、Vulnerability、Finding",
        "`Threat`は、望ましくない事象や行為である。",
        "`Vulnerability`は、そのThreatを成立させやすい弱点や条件である。",
        "`Finding`は、許可された範囲でEvidenceに支えられて確認した環境固有の結論である。",
        "Attack Path`と実行可能な侵害手順",
        "Unknown / Assumed / Confirmed / Not Applicable",
        "Draft / In Review / Approved for Assessment / Needs Evidence / Superseded",
        "Candidate / Supported / Partially Supported / Disconfirmed / Inconclusive",
        "Unknown / Documented / Implemented / Observed / Validated",
        "Gap statusは Open / Accepted temporarily / Escalated / Closed",
        "Evidence Requirement`と`Collected Evidence",
        "Unknown`がGapへ変換",
        "文書化されたControlがあるので十分である\n誤りである",
        "CSFやOWASPへMappingしたので完全である\n誤りである",
        "Threat countの多さではない",
        "本章の成果物は、Capabilityの証拠候補にはなるが、Review、Rubric、再評価なしに能力証明にはならない",
        "[Threat Model](../templates/threat-model.md)",
        "[第4章 合成記入例](../cases/ch04-threat-model-example.md)",
        "https://itdojp.github.io/pentest-learning-book/",
        "https://itdojp.github.io/practical-auth-book/",
        "https://itdojp.github.io/it-infra-security-guide-book/",
        "委譲先を読まなくても、本章の中心論旨は切れない",
        "CASE-2026-001",
        "DR-2026-001",
        "AUTH-CASE-2026-001",
        "Chapter 5",
        "Chapter 6",
        "Chapter 9",
        "Chapter 11",
        "第15章",
        "Chapter 27",
        "F-04-01",
        "F-04-02",
        "T-04-01",
        "T-04-02",
        "T-04-03",
        "T-04-04",
        "実在Targetが必要になった",
        "実CredentialやPIIが必要になった",
        "手順が実行可能な侵害手順へ寄り始めた",
        "Authorization条件が不明になった",
        "一つの仮説を最後まで通す記入例",
        "`ART-03`の正本構造は、Templateと合成記入例で共通する次の13節（番号0〜12）である",
        "10. `Assumptions, Unknowns and Gaps`",
        "11. `Evidence Requirements and Actions`",
        "12. `Reassessment and Handoff`",
        "13. `Review and Rubric`",
        "`RUBRIC-TM-YYYY-001` Asset taxonomy",
        "`RUBRIC-TM-YYYY-002` Boundary and flow clarity",
        "`RUBRIC-TM-YYYY-003` Threat usefulness and evidence sufficiency",
        "`RUBRIC-TM-YYYY-004` Safety and authorization",
        "`RUBRIC-TM-YYYY-005` Decision handoff quality",
    )
    messages.extend(require_tokens(label, text, required))

    if text.count("F-04-01") < 2 or text.count("F-04-02") < 2:
        messages.append(f"{label}: both figure IDs must be defined and referenced")
    for table_id in ("T-04-01", "T-04-02", "T-04-03", "T-04-04"):
        if text.count(table_id) != 1:
            messages.append(f"{label}: {table_id} must occur exactly once")

    body, marker, references = text.partition("## 参考資料")
    if not marker:
        messages.append(f"{label}: missing reference section")
    elif source_ids(body) != EXPECTED_SOURCE_IDS:
        messages.append(f"{label}: body source IDs {sorted(source_ids(body))!r} != {sorted(EXPECTED_SOURCE_IDS)!r}")
    if source_ids(references) != EXPECTED_SOURCE_IDS:
        messages.append(f"{label}: chapter-end source IDs {sorted(source_ids(references))!r} != body IDs")

    exercise = section(text, "## 安全な演習")
    if not exercise:
        messages.append(f"{label}: missing bounded safe exercise section")
    else:
        fields = [
            (f"{label} safe exercise line {number}", line)
            for number, line in enumerate(exercise.splitlines(), start=1)
            if re.match(r"\s*(?:[-*]|\d+\.)\s+", line)
        ]
        messages.extend(policy_errors(fields))
    return messages


def template_contract_errors(text: str, label: str) -> list[str]:
    messages = require_order(label, text, EXPECTED_TEMPLATE_HEADINGS)
    required = (
        "ART-03",
        "Model status | Draft / In Review / Approved for Assessment / Needs Evidence / Superseded",
        "Business Outcome / Service / Component / Data / Identity / Control Plane / Evidence",
        "Business Assetは8番目のTypeではない",
        "Unknown / Assumed / Confirmed / Not Applicable",
        "Data / Identity / Control",
        "Evidence statusは Planned / Collected / Rejected / Inconclusive",
        "Identity Authority / Data Ownership / Administrative Control / Tenant / Third-party Responsibility / Control Plane / Network",
        "Candidate / Supported / Partially Supported / Disconfirmed / Inconclusive",
        "Unknown / Documented / Implemented / Observed / Validated",
        "Gap statusは Open / Accepted temporarily / Escalated / Closed",
        "| Attack Path ID | Edge ID | From Asset / State | Condition | Boundary ID | To Asset / State | Affected Asset IDs | Expected impact | Observation point | Required Evidence ID | Knowledge state |",
        "Do not include commands.",
        "Do not include payload strings.",
        "Do not include exploit steps",
        "Do not include credentials, tokens, cookies, or secrets.",
        "Do not include real target identifiers",
        "| Gap ID | Missing information / control / telemetry | Decision affected | Owner | Due date | Status | Evidence Requirement ID | Action ID | Reassessment ID |",
        "| Evidence Requirement ID | Question | Related Threat / Control / Gap | Minimum sufficient evidence | Forbidden / over-collection boundary | Owner | Due date | Status | Resulting Evidence IDs |",
        "| Evidence ID | Related Evidence Requirement IDs | Evidence description | Collection conditions / provenance | Status | Reviewer | Collected at | Limitation |",
        "Evidence RequirementのStatusは Required / Deferred / Replaced / Not Applicable",
        "| Entry Point ID | Related Exposure IDs | Interface class | Description | Owner | Boundary IDs | Required authority | Observation point | Knowledge state | Evidence IDs |",
        "| Dependency ID | From asset | To asset | Why the dependency matters | Failure consequence |",
        "| Rubric ID | Criterion | Meets | Partially meets | Does not meet |",
        "| Limitation ID | Scope / condition | Unsupported claim | Owner | Reassessment trigger |",
        "ACT-TM-YYYY-NNN",
        "REA-TM-YYYY-NNN",
        "| Reassessment ID | Trigger | Scope | Owner | Scheduled date | Inputs required | Closure criteria | Destination chapter / artifact |",
    )
    messages.extend(require_tokens(label, text, required))

    document_rows, document_messages = table_by_header(
        section(text, "## 0. Document Control"), ("Field", "Value"), label
    )
    messages.extend(document_messages)
    document_fields = tuple(row[0] for row in document_rows if len(row) == 2)
    if document_fields != DOCUMENT_CONTROL_FIELDS:
        messages.append(
            f"{label}: Document Control fields/order {document_fields!r} != {DOCUMENT_CONTROL_FIELDS!r}"
        )

    template_flow_header = (
        "Flow ID",
        "Flow type",
        "Source Asset ID",
        "Destination Asset ID",
        "Purpose",
        "Protocol class",
        "Identity / authorization context",
        "Boundary IDs crossed",
        "Data classification",
        "Evidence status",
        "Observation point",
    )
    template_flow_rows, template_flow_messages = table_by_header(text, template_flow_header, label)
    messages.extend(template_flow_messages)
    evidence_status_index = template_flow_header.index("Evidence status")
    for row in template_flow_rows:
        if len(row) != len(template_flow_header):
            continue
        value = row[evidence_status_index]
        if value and value not in COLLECTED_EVIDENCE_STATUSES:
            messages.append(f"{label}: Flow Evidence status outside finite set: {value!r}")

    template_gap_rows, template_gap_messages = table_by_header(text, GAP_HEADER, label)
    messages.extend(template_gap_messages)
    gap_status_index = GAP_HEADER.index("Status")
    for row in template_gap_rows:
        if len(row) != len(GAP_HEADER):
            continue
        value = row[gap_status_index]
        if value and value not in GAP_STATUSES:
            messages.append(f"{label}: Gap status outside finite set: {value!r}")

    template_evidence_rows, template_evidence_messages = table_by_header(
        text, COLLECTED_EVIDENCE_HEADER, label
    )
    messages.extend(template_evidence_messages)
    collected_status_index = COLLECTED_EVIDENCE_HEADER.index("Status")
    for row in template_evidence_rows:
        if len(row) != len(COLLECTED_EVIDENCE_HEADER):
            continue
        value = row[collected_status_index]
        if value and value not in COLLECTED_EVIDENCE_STATUSES:
            messages.append(f"{label}: Collected Evidence status outside finite set: {value!r}")

    fields, adapter_messages = classified_table_fields(text, label, TEMPLATE_TABLE_OCCURRENCES)
    messages.extend(adapter_messages)
    decision_rows, decision_messages = table_by_header(
        section(text, "## 1. Decision Context"), ("Field", "Value"), label
    )
    messages.extend(decision_messages)
    decision_fields = tuple(row[0] for row in decision_rows if len(row) == 2)
    if decision_fields != DECISION_CONTEXT_FIELDS:
        messages.append(
            f"{label}: Decision Context fields/order {decision_fields!r} != {DECISION_CONTEXT_FIELDS!r}"
        )
    messages.extend(policy_errors(fields))
    return messages


def case_contract_errors(text: str, label: str) -> list[str]:
    messages: list[str] = []
    messages.extend(require_order(label, text, EXPECTED_CASE_HEADINGS))
    observed_h2 = tuple(re.findall(r"^## .+$", text, re.MULTILINE))
    if observed_h2 != EXPECTED_CASE_HEADINGS:
        messages.append(f"{label}: top-level headings {observed_h2!r} != {EXPECTED_CASE_HEADINGS!r}")
    required = (
        "ART-03",
        "TM-2026-001",
        "CASE-2026-001",
        "DR-2026-001",
        "AUTH-CASE-2026-001",
        "Proceed with conditions",
        "COND-AUTH-2026-001",
        "COND-AUTH-2026-002",
        "COND-AUTH-2026-003",
        "Telemetry absence is not absence of compromise",
        "Business Assetは8番目のTypeではなく",
        "Evidence Requirement status",
        "Collected Evidence status",
        "同一Evidence IDは原典の取得時刻、取得主体、条件、制約を置換しない",
        "Inherited Negative Finding Register",
        "standaloneの`Collected at`がないため、時刻を創作せず",
        "Gap status",
        "合成Tenant A → 合成Tenant B",
        "Tenant間分離の不確実性",
        "Entry PointはExposureの参照列だけで済ませず",
        "ASSET-2026-001",
        "ASSET-2026-002",
        "ASSET-2026-003",
        "ASSET-2026-004",
        "ASSET-2026-005",
        "ASSET-2026-006",
        "ASSET-2026-007",
        "FLOW-2026-001",
        "TB-2026-001",
        "TB-2026-002",
        "TB-2026-003",
        "TH-2026-001",
        "TH-2026-002",
        "TH-2026-003",
        "MISUSE-2026-001",
        "MISUSE-2026-002",
        "PATH-2026-001",
        "PATH-2026-002",
        "CTRL-2026-001",
        "CTRL-2026-002",
        "CTRL-2026-003",
        "CTRL-2026-004",
        "CTRL-2026-005",
        "ASM-2026-001",
        "ASM-2026-002",
        "ASM-2026-003",
        "GAP-2026-001",
        "GAP-2026-002",
        "GAP-2026-003",
        "EREQ-2026-001",
        "EREQ-2026-002",
        "EREQ-2026-003",
        "ACT-TM-2026-001",
        "REA-TM-2026-001",
    )
    messages.extend(require_tokens(label, text, required))

    field_rows, field_messages = table_by_header(
        section(text, "## 0. Document Control"), ("Field", "Value"), label
    )
    messages.extend(field_messages)
    document_fields = {row[0]: row[1] for row in field_rows if len(row) == 2}
    if document_fields.get("Model status") not in MODEL_STATUSES:
        messages.append(f"{label}: Model status outside finite set: {document_fields.get('Model status')!r}")
    expected_document_fields = {
        "Artifact ID": "`ART-03`",
        "Threat Model ID": "`TM-2026-001`",
        "Parent Case ID": "`CASE-2026-001`",
        "Relation": "`refines`",
        "Decision Requirement ID": "`DR-2026-001`",
        "Authorization Record ID": "`AUTH-CASE-2026-001`",
    }
    for field, expected_value in expected_document_fields.items():
        if document_fields.get(field) != expected_value:
            messages.append(
                f"{label}: Document Control {field!r} {document_fields.get(field)!r} != {expected_value!r}"
            )
    if document_fields.get("Threat Model ID") == document_fields.get("Parent Case ID"):
        messages.append(f"{label}: Threat Model cannot be its own parent")
    observed_document_fields = tuple(row[0] for row in field_rows if len(row) == 2)
    if observed_document_fields != DOCUMENT_CONTROL_FIELDS:
        messages.append(
            f"{label}: Document Control fields/order {observed_document_fields!r} != {DOCUMENT_CONTROL_FIELDS!r}"
        )

    decision_rows, decision_messages = table_by_header(
        section(text, "## 1. Decision Context"), ("Field", "Value"), label
    )
    messages.extend(decision_messages)
    observed_decision_fields = tuple(row[0] for row in decision_rows if len(row) == 2)
    if observed_decision_fields != DECISION_CONTEXT_FIELDS:
        messages.append(
            f"{label}: Decision Context fields/order {observed_decision_fields!r} != {DECISION_CONTEXT_FIELDS!r}"
        )

    table_contracts: tuple[tuple[tuple[str, ...], str, set[str], int], ...] = (
        (("Asset ID", "Type", "Name", "Business role / outcome", "Owner", "Criticality", "Data classification", "Knowledge state", "Evidence IDs", "Dependency IDs"), "Type", ASSET_TYPES, 7),
        (("Flow ID", "Flow type", "Source Asset ID", "Destination Asset ID", "Purpose", "Protocol class", "Identity / authorization context", "Boundary IDs crossed", "Data classification", "Evidence status", "Observation point"), "Flow type", FLOW_TYPES, 3),
        (("Boundary ID", "Boundary type", "From / To", "Owner(s)", "Trust / authority change", "Crossing condition", "Control", "Failure consequence", "Knowledge state", "Evidence IDs"), "Boundary type", BOUNDARY_TYPES, 5),
        (("Hypothesis ID", "Decision Requirement ID", "Related Asset IDs", "Boundary / Flow / Exposure IDs", "Statement", "Preconditions", "Expected impact", "Evidence needed", "Alternative explanation", "Priority", "Hypothesis status"), "Hypothesis status", HYPOTHESIS_STATUSES, 3),
        (("Control ID", "Related Asset / Boundary / Threat / Path IDs", "Control statement", "Owner", "Assurance state", "Evidence IDs", "Limitation", "Gap ID", "Reassessment trigger"), "Assurance state", ASSURANCE_STATES, 5),
    )
    parsed: dict[tuple[str, ...], list[list[str]]] = {}
    for header, finite_column, allowed, minimum_rows in table_contracts:
        rows, table_messages = table_by_header(text, header, label)
        messages.extend(table_messages)
        parsed[header] = rows
        if len(rows) < minimum_rows:
            messages.append(f"{label}: {header[0]} table requires at least {minimum_rows} rows")
        index = header.index(finite_column)
        values = {row[index] for row in rows if len(row) == len(header)}
        if not values <= allowed:
            messages.append(f"{label}: {finite_column} values outside finite set: {sorted(values - allowed)!r}")
        if header[0] in {"Asset ID", "Flow ID"} and values != allowed:
            messages.append(f"{label}: {finite_column} coverage {sorted(values)!r} != {sorted(allowed)!r}")
        for row in rows:
            if len(row) == len(header) and any(not cell for cell in row):
                messages.append(f"{label}: {header[0]} row contains an empty required cell: {row!r}")

    boundary_header = table_contracts[2][0]
    boundary_values = {row[1] for row in parsed.get(boundary_header, []) if len(row) == len(boundary_header)}
    if len(boundary_values) < 5:
        messages.append(f"{label}: requires at least five distinct boundary types")

    flow_header = table_contracts[1][0]
    evidence_status_index = flow_header.index("Evidence status")
    flow_evidence_statuses = {
        row[evidence_status_index]
        for row in parsed.get(flow_header, [])
        if len(row) == len(flow_header)
    }
    if not flow_evidence_statuses <= COLLECTED_EVIDENCE_STATUSES:
        messages.append(
            f"{label}: Flow Evidence status values outside finite set: "
            f"{sorted(flow_evidence_statuses - COLLECTED_EVIDENCE_STATUSES)!r}"
        )

    asset_header = table_contracts[0][0]
    for row in parsed.get(asset_header, []):
        if len(row) != len(asset_header):
            continue
        knowledge_state = row[asset_header.index("Knowledge state")]
        evidence_ids = row[asset_header.index("Evidence IDs")]
        if knowledge_state == "Confirmed" and evidence_ids in {"-", "None", "TBD", "Unknown"}:
            messages.append(
                f"{label}: Confirmed Asset requires an Evidence ID rather than {evidence_ids!r}: {row[0]!r}"
            )

    hypothesis_header = table_contracts[3][0]
    hypothesis_rows = {
        row[hypothesis_header.index("Hypothesis ID")].strip("`"): row
        for row in parsed.get(hypothesis_header, [])
        if len(row) == len(hypothesis_header)
    }
    inherited_th_003 = hypothesis_rows.get("TH-2026-003")
    if inherited_th_003 is not None:
        statement = inherited_th_003[hypothesis_header.index("Statement")]
        if statement != INHERITED_TH_003_PROPOSITION:
            messages.append(
                f"{label}: TH-2026-003 Statement {statement!r} must preserve the inherited proposition "
                f"{INHERITED_TH_003_PROPOSITION!r}"
            )
    chapter1_case = read_text("cases/ch01-integrated-security-case-example.md")
    if INHERITED_TH_003_PROPOSITION not in chapter1_case:
        messages.append(
            f"{label}: Chapter 1 no longer contains the inherited TH-2026-003 proposition "
            f"{INHERITED_TH_003_PROPOSITION!r}"
        )

    count_contracts = (
        (("Exposure ID", "Related Asset / Boundary / Flow IDs", "Entry Point ID", "Reachability class", "External dependency", "Required authority", "Verification status", "Evidence ID", "Gap ID"), 3),
        (("Misuse Case ID", "Goal", "Actor capability class", "Preconditions", "Affected assets", "Boundary crossed", "Expected outcome", "Observation points", "Excluded operational detail"), 2),
        (("Attack Path ID", "Edge ID", "From Asset / State", "Condition", "Boundary ID", "To Asset / State", "Affected Asset IDs", "Expected impact", "Observation point", "Required Evidence ID", "Knowledge state"), 2),
        (("Assumption ID", "Statement", "Owner", "Validation method", "Due date", "Status", "Related IDs"), 3),
        (GAP_HEADER, 3),
        (("Evidence Requirement ID", "Question", "Related Threat / Control / Gap", "Minimum sufficient evidence", "Forbidden / over-collection boundary", "Owner", "Due date", "Status", "Resulting Evidence IDs"), 3),
        (("Reassessment ID", "Trigger", "Scope", "Owner", "Scheduled date", "Inputs required", "Closure criteria", "Destination chapter / artifact"), 3),
    )
    case_tables: dict[tuple[str, ...], list[list[str]]] = {}
    for header, minimum_rows in count_contracts:
        rows, table_messages = table_by_header(text, header, label)
        messages.extend(table_messages)
        case_tables[header] = rows
        if len(rows) < minimum_rows:
            messages.append(f"{label}: {header[0]} table requires at least {minimum_rows} rows")
        for row in rows:
            if len(row) == len(header) and any(not cell for cell in row):
                messages.append(f"{label}: {header[0]} row contains an empty required cell: {row!r}")

    entry_point_header = (
        "Entry Point ID",
        "Related Exposure IDs",
        "Interface class",
        "Description",
        "Owner",
        "Boundary IDs",
        "Required authority",
        "Observation point",
        "Knowledge state",
        "Evidence IDs",
    )
    entry_point_rows, entry_point_messages = table_by_header(text, entry_point_header, label)
    messages.extend(entry_point_messages)
    if len(entry_point_rows) < 3:
        messages.append(f"{label}: Entry Point Detail Register requires at least three rows")
    for row in entry_point_rows:
        if len(row) == len(entry_point_header) and any(not cell for cell in row):
            messages.append(f"{label}: Entry Point row contains an empty required cell: {row!r}")
        if len(row) == len(entry_point_header) and row[8] not in KNOWLEDGE_STATES:
            messages.append(f"{label}: Entry Point Knowledge state outside finite set: {row[8]!r}")

    evidence_requirement_header = count_contracts[5][0]
    evidence_requirement_status_index = evidence_requirement_header.index("Status")
    evidence_requirement_statuses = {
        row[evidence_requirement_status_index]
        for row in case_tables.get(evidence_requirement_header, [])
        if len(row) == len(evidence_requirement_header)
    }
    if not evidence_requirement_statuses <= EVIDENCE_REQUIREMENT_STATUSES:
        messages.append(
            f"{label}: Evidence Requirement status values outside finite set: "
            f"{sorted(evidence_requirement_statuses - EVIDENCE_REQUIREMENT_STATUSES)!r}"
        )

    gap_header = count_contracts[4][0]
    gap_status_index = gap_header.index("Status")
    gap_statuses = {
        row[gap_status_index]
        for row in case_tables.get(gap_header, [])
        if len(row) == len(gap_header)
    }
    if not gap_statuses <= GAP_STATUSES:
        messages.append(f"{label}: Gap status values outside finite set: {sorted(gap_statuses - GAP_STATUSES)!r}")

    collected_rows, collected_messages = table_by_header(text, COLLECTED_EVIDENCE_HEADER, label)
    messages.extend(collected_messages)
    if len(collected_rows) != 5:
        messages.append(f"{label}: Collected Evidence Register must contain exactly five inherited Evidence rows")
    collected_status_index = COLLECTED_EVIDENCE_HEADER.index("Status")
    collected_statuses = {
        row[collected_status_index]
        for row in collected_rows
        if len(row) == len(COLLECTED_EVIDENCE_HEADER)
    }
    if not collected_statuses <= COLLECTED_EVIDENCE_STATUSES:
        messages.append(
            f"{label}: Collected Evidence status values outside finite set: "
            f"{sorted(collected_statuses - COLLECTED_EVIDENCE_STATUSES)!r}"
        )
    collected_ids = {
        row[0].strip("`")
        for row in collected_rows
        if len(row) == len(COLLECTED_EVIDENCE_HEADER)
    }
    if collected_ids != EXPECTED_INHERITED_COLLECTED_EVIDENCE_IDS:
        messages.append(
            f"{label}: Collected Evidence IDs {sorted(collected_ids)!r} "
            f"!= inherited Collected Evidence IDs {sorted(EXPECTED_INHERITED_COLLECTED_EVIDENCE_IDS)!r}"
        )

    chapter1_evidence_header = (
        "Evidence ID",
        "Observation ID",
        "Validation ID",
        "Authority / RoE ID",
        "Question supported",
        "Source / collector",
        "Collected at",
        "Integrity / hash",
        "Limitation",
        "Classification",
    )
    chapter1_case = read_text("cases/ch01-integrated-security-case-example.md")
    chapter1_evidence_rows, source_messages = table_by_header(
        chapter1_case,
        chapter1_evidence_header,
        "cases/ch01-integrated-security-case-example.md",
    )
    messages.extend(source_messages)
    expected_inherited_rows: dict[str, tuple[str, str, str, str, str, str]] = {}
    for row in chapter1_evidence_rows:
        if len(row) != len(chapter1_evidence_header):
            continue
        identifier = row[0].strip("`")
        if identifier not in EXPECTED_INHERITED_COLLECTED_EVIDENCE_IDS:
            continue
        expected_inherited_rows[identifier] = (
            row[4],
            f"第1章継承: {row[5]}; Observation {row[1]}; Validation {row[2]}; "
            f"Authority / RoE {row[3]}; Integrity / hash {row[7]}; Classification {row[9]}",
            "Collected",
            INHERITED_REVIEWER_VALUE,
            row[6],
            row[8],
        )

    chapter2_evidence_header = (
        "Evidence ID",
        "Description",
        "Source / custodian",
        "Collected at",
        "Integrity / reference",
        "Limitation",
    )
    chapter2_case = read_text("cases/ch02-authorization-decision-example.md")
    chapter2_evidence_rows, source_messages = table_by_header(
        chapter2_case,
        chapter2_evidence_header,
        "cases/ch02-authorization-decision-example.md",
    )
    messages.extend(source_messages)
    for row in chapter2_evidence_rows:
        if len(row) != len(chapter2_evidence_header) or row[0].strip("`") != "EVD-AUTH-2026-001":
            continue
        expected_inherited_rows["EVD-AUTH-2026-001"] = (
            row[1],
            f"第2章継承: Source / custodian {row[2]}; Integrity / reference {row[4]}",
            "Collected",
            INHERITED_REVIEWER_VALUE,
            row[3],
            row[5],
        )

    if set(expected_inherited_rows) != EXPECTED_INHERITED_COLLECTED_EVIDENCE_IDS:
        messages.append(
            f"{label}: source-derived inherited Evidence contracts {sorted(expected_inherited_rows)!r} "
            f"!= {sorted(EXPECTED_INHERITED_COLLECTED_EVIDENCE_IDS)!r}"
        )
    observed_inherited_rows = {
        row[0].strip("`"): (row[2], row[3], row[4], row[5], row[6], row[7])
        for row in collected_rows
        if len(row) == len(COLLECTED_EVIDENCE_HEADER)
    }
    requirement_bindings: dict[str, list[str]] = {}
    for row in case_tables.get(evidence_requirement_header, []):
        if len(row) != len(evidence_requirement_header):
            continue
        requirement_id = row[evidence_requirement_header.index("Evidence Requirement ID")].strip("`")
        resulting = row[evidence_requirement_header.index("Resulting Evidence IDs")]
        for identifier in re.findall(r"\b(?:EVD(?:-AUTH)?-2026-\d{3}|NEG-2026-\d{3})\b", resulting):
            requirement_bindings.setdefault(identifier, []).append(requirement_id)
    for row in collected_rows:
        if len(row) != len(COLLECTED_EVIDENCE_HEADER):
            continue
        identifier = row[0].strip("`")
        expected_relation = ", ".join(
            f"`{requirement_id}`" for requirement_id in requirement_bindings.get(identifier, [])
        )
        if row[1] != expected_relation:
            messages.append(
                f"{label}: {identifier} Related Evidence Requirement IDs {row[1]!r} "
                f"!= Resulting Evidence binding {expected_relation!r}"
            )
    for identifier, expected_row in expected_inherited_rows.items():
        if observed_inherited_rows.get(identifier) != expected_row:
            messages.append(
                f"{label}: inherited Evidence metadata drift for {identifier}: "
                f"{observed_inherited_rows.get(identifier)!r} != {expected_row!r}"
            )

    chapter1_negative_rows, source_messages = table_by_header(
        chapter1_case,
        NEGATIVE_FINDING_HEADER,
        "cases/ch01-integrated-security-case-example.md",
    )
    messages.extend(source_messages)
    case_negative_rows, negative_messages = table_by_header(text, NEGATIVE_FINDING_HEADER, label)
    messages.extend(negative_messages)
    inherited_negative = [
        row for row in chapter1_negative_rows if row and row[0].strip("`") == "NEG-2026-001"
    ]
    if len(inherited_negative) != 1 or case_negative_rows != inherited_negative:
        messages.append(
            f"{label}: NEG-2026-001 must preserve the exact Chapter 1 Negative Finding row "
            f"without an invented timestamp"
        )

    control_header = table_contracts[4][0]
    controls_by_id = {
        row[0].strip("`"): row
        for row in parsed.get(control_header, [])
        if len(row) == len(control_header)
    }
    lab_control = controls_by_id.get("CTRL-2026-004")
    if lab_control is None:
        messages.append(f"{label}: missing CTRL-2026-004 assurance contract")
    else:
        assurance = lab_control[control_header.index("Assurance state")]
        evidence_ids = lab_control[control_header.index("Evidence IDs")]
        limitation = lab_control[control_header.index("Limitation")]
        if assurance != "Observed":
            messages.append(
                f"{label}: CTRL-2026-004 must remain Observed until explicit synthetic "
                f"preflight/default-deny/cleanup result Evidence exists; found {assurance!r}"
            )
        if evidence_ids != "`EVD-AUTH-2026-001`, `SYNTH-REV-TM-SAFE-001`":
            messages.append(f"{label}: CTRL-2026-004 review Evidence binding drift: {evidence_ids!r}")
        for marker in ("preflight", "default-deny", "Cleanup", "実施結果は未収集"):
            if marker not in limitation:
                messages.append(f"{label}: CTRL-2026-004 limitation missing {marker!r}")

    assumption_header = count_contracts[3][0]
    for row in case_tables.get(assumption_header, []):
        if len(row) == len(assumption_header) and row[5] not in KNOWLEDGE_STATES:
            messages.append(f"{label}: Assumption status outside finite set: {row[5]!r}")

    path_header = count_contracts[2][0]
    path_rows = case_tables.get(path_header, [])
    if len({row[0] for row in path_rows if row}) != 2:
        messages.append(f"{label}: exactly two Attack Path IDs must own the edge rows")
    operational_pattern = re.compile(r"(?:^|\s)(?:curl|wget|powershell|bash|sh|python|nmap|sqlmap)\s|```(?:bash|sh|powershell)|(?:payload|command)\s*[:=]", re.IGNORECASE)
    for row in path_rows:
        joined = " ".join(row)
        if operational_pattern.search(joined):
            messages.append(f"{label}: Attack Path contains an executable command or payload marker: {joined!r}")
    path_rows_by_edge = {row[1].strip("`"): row for row in path_rows if len(row) == len(path_header)}
    edge004 = path_rows_by_edge.get("EDGE-2026-004")
    edge007 = path_rows_by_edge.get("EDGE-2026-007")
    if edge004 is None or edge004[path_header.index("Boundary ID")] != "`TB-2026-005`":
        messages.append(f"{label}: EDGE-2026-004 must use the Tenant boundary TB-2026-005")
    if edge007 is None or edge007[path_header.index("Boundary ID")] != "`TB-2026-007`":
        messages.append(f"{label}: EDGE-2026-007 must use the third-party responsibility boundary TB-2026-007")

    misuse_header = count_contracts[1][0]
    misuse_rows_by_id = {
        row[0].strip("`"): row
        for row in case_tables.get(misuse_header, [])
        if len(row) == len(misuse_header)
    }
    misuse001 = misuse_rows_by_id.get("MISUSE-2026-001")
    if misuse001 is None or misuse001[misuse_header.index("Boundary crossed")] != "`TB-2026-001`":
        messages.append(f"{label}: MISUSE-2026-001 must remain scoped to administrative boundary TB-2026-001")

    action_header = (
        "Action ID",
        "Related Gap / Control / Threat",
        "Action",
        "Owner",
        "Due date",
        "Success evidence",
        "Status",
    )
    action_rows, action_messages = table_by_header(text, action_header, label)
    messages.extend(action_messages)
    if len(action_rows) < 5:
        messages.append(f"{label}: Action ID table requires at least five rows")

    definition_contracts: tuple[tuple[str, list[list[str]], int, bool], ...] = (
        ("ASSET", parsed.get(asset_header, []), 0, True),
        ("FLOW", parsed.get(table_contracts[1][0], []), 0, True),
        ("TB", parsed.get(boundary_header, []), 0, True),
        ("EXP", case_tables.get(count_contracts[0][0], []), 0, True),
        ("EP", entry_point_rows, 0, True),
        ("TH", parsed.get(table_contracts[3][0], []), 0, True),
        ("MISUSE", case_tables.get(count_contracts[1][0], []), 0, True),
        ("PATH", path_rows, 0, False),
        ("EDGE", path_rows, 1, True),
        ("CTRL", parsed.get(table_contracts[4][0], []), 0, True),
        ("ASM", case_tables.get(count_contracts[3][0], []), 0, True),
        ("GAP", case_tables.get(count_contracts[4][0], []), 0, True),
        ("EREQ", case_tables.get(count_contracts[5][0], []), 0, True),
        ("ACT-TM", action_rows, 0, True),
        ("REA-TM", case_tables.get(count_contracts[6][0], []), 0, True),
    )
    for family, rows, column, unique_definition in definition_contracts:
        identifiers = [
            match.group(1)
            for row in rows
            if len(row) > column
            for match in [re.fullmatch(rf"`?({re.escape(family)}-2026-\d{{3}})`?", row[column])]
            if match
        ]
        if set(identifiers) != EXPECTED_CASE_IDS[family]:
            messages.append(
                f"{label}: defined {family} IDs {sorted(set(identifiers))!r} "
                f"!= {sorted(EXPECTED_CASE_IDS[family])!r}"
            )
        if unique_definition:
            duplicates = sorted(identifier for identifier, count in Counter(identifiers).items() if count != 1)
            if duplicates:
                messages.append(f"{label}: {family} IDs must each be defined exactly once: {duplicates!r}")

    for family, expected in EXPECTED_CASE_IDS.items():
        observed = set(re.findall(rf"\b{family}-2026-\d{{3}}\b", text))
        if observed != expected:
            messages.append(f"{label}: {family} IDs {sorted(observed)!r} != {sorted(expected)!r}")

    auxiliary_definition_contracts = (
        (
            "Dependency",
            ("Dependency ID", "From asset", "To asset", "Why the dependency matters", "Failure consequence"),
            EXPECTED_DEPENDENCY_IDS,
        ),
        (
            "Rubric",
            ("Rubric ID", "Criterion", "Meets", "Partially meets", "Does not meet"),
            EXPECTED_RUBRIC_IDS,
        ),
        (
            "Handoff",
            HANDOFF_HEADER,
            EXPECTED_HANDOFF_IDS,
        ),
    )
    for family, header, expected in auxiliary_definition_contracts:
        rows, table_messages = table_by_header(text, header, label)
        messages.extend(table_messages)
        observed = [cell for row in rows if row for cell in re.findall(r"[A-Z][A-Z0-9-]+-2026-\d{3}", row[0])]
        if set(observed) != expected:
            messages.append(f"{label}: defined {family} IDs {sorted(set(observed))!r} != {sorted(expected)!r}")
        duplicates = sorted(identifier for identifier, count in Counter(observed).items() if count != 1)
        if duplicates:
            messages.append(f"{label}: {family} IDs must each be defined exactly once: {duplicates!r}")

    handoff_rows, handoff_messages = table_by_header(text, HANDOFF_HEADER, label)
    messages.extend(handoff_messages)
    observed_handoffs = {
        row[0].strip("`"): (row[1], row[2])
        for row in handoff_rows
        if len(row) == len(HANDOFF_HEADER)
    }
    if observed_handoffs != EXPECTED_HANDOFF_ROWS:
        messages.append(
            f"{label}: Handoff semantic mapping {observed_handoffs!r} != {EXPECTED_HANDOFF_ROWS!r}"
        )

    inherited_evidence = set(re.findall(r"\b(?:EVD-2026-\d{3}|EVD-AUTH-2026-\d{3}|NEG-2026-\d{3})\b", text))
    if inherited_evidence != EXPECTED_INHERITED_EVIDENCE_IDS:
        messages.append(
            f"{label}: inherited Evidence IDs {sorted(inherited_evidence)!r} "
            f"!= {sorted(EXPECTED_INHERITED_EVIDENCE_IDS)!r}"
        )
    evidence_sources = {
        "cases/ch01-integrated-security-case-example.md": EXPECTED_INHERITED_EVIDENCE_IDS - {"EVD-AUTH-2026-001"},
        "cases/ch02-authorization-decision-example.md": {"EVD-AUTH-2026-001"},
    }
    for relative, expected_ids in evidence_sources.items():
        source_text = (ROOT / relative).read_text(encoding="utf-8") if (ROOT / relative).is_file() else ""
        missing = sorted(identifier for identifier in expected_ids if identifier not in source_text)
        if missing:
            messages.append(f"{label}: inherited Evidence IDs missing from {relative}: {missing!r}")

    fields, adapter_messages = classified_table_fields(text, label, CASE_TABLE_OCCURRENCES)
    messages.extend(adapter_messages)
    fields.extend(
        (f"{label} Limitation line {number}", line)
        for number, line in enumerate(section(text, "### Limitations", 3).splitlines(), start=1)
        if re.match(r"\s*[-*]\s+", line)
    )
    messages.extend(policy_errors(fields))
    return messages


def source_contract_errors(chapter: str, registry: dict, note: str) -> list[str]:
    messages: list[str] = []
    if registry.get("checkedAt") != "2026-07-25":
        messages.append("references/sources.json: registry-level checkedAt must remain 2026-07-25")
    entries = {item.get("id"): item for item in registry.get("sources", []) if isinstance(item, dict)}
    expected = {
        "SRC-CSF-001": {
            "status": "final",
            "version": "2.0",
            "url": "https://www.nist.gov/cyberframework",
            "publishedAt": "2024-02-26",
            "checkedAt": "2026-08-08",
            "nextReviewAt": "2026-11-08",
            "reviewTriggers": [
                "NIST CSF revision or errata",
                "NIST CSF 2.0 resource-center or outcome-taxonomy change used by Chapter 4",
            ],
            "markers": ("高位Outcome taxonomy", "実装方法を規定せず", "完全性"),
        },
        "SRC-NIST-RISK-001": {
            "status": "final",
            "version": "SP 800-30 Rev.1",
            "url": "https://csrc.nist.gov/pubs/sp/800/30/r1/final",
            "publishedAt": "2012-09-17",
            "checkedAt": "2026-08-08",
            "nextReviewAt": "2026-11-08",
            "reviewTriggers": [
                "NIST SP 800-30 revision, withdrawal, successor, or errata",
                "NIST Risk Management publications index status change",
                "Change to a threat source, threat event, vulnerability, predisposing condition, likelihood, impact, or uncertainty concept used by Chapter 4",
            ],
            "markers": ("Federal", "数値Risk score", "後継版"),
        },
        "SRC-OWASP-TM-001": {
            "status": "maintained-project-guidance",
            "version": None,
            "url": "https://owasp.org/www-project-threat-modeling/",
            "publishedAt": None,
            "checkedAt": "2026-08-08",
            "nextReviewAt": "2026-11-08",
            "reviewTriggers": [
                "OWASP project status or methodology-neutral guidance change",
                "OWASP Threat Modeling Project resource, tool, or historical-material classification change",
                "Project URL relocation or retirement",
            ],
            "markers": (
                "Maintained Project Guidance",
                "単一の公式OWASP Threat Modeling methodologyを定義しない",
                "継続更新されるProject pageには固定versionと単一published dateが提示されていない",
                "versionとpublishedAtは推測せずnullとする",
                "checkedAt、nextReviewAt、reviewTriggersで現行pageとProject statusを追跡",
                "公式に固定version、公開日またはreleaseが提示された場合に再監査",
                "方法論中立の補助参照としてのみ用いる",
                "Threat Modelの完全性、Control有効性または評価品質の証明ではない",
            ),
        },
    }
    for source_id, contract in expected.items():
        entry = entries.get(source_id)
        if not entry:
            messages.append(f"references/sources.json: missing {source_id}")
            continue
        for field in ("status", "version", "url", "publishedAt", "checkedAt", "nextReviewAt", "reviewTriggers"):
            if entry.get(field) != contract[field]:
                messages.append(f"references/sources.json: {source_id}.{field} {entry.get(field)!r} != {contract[field]!r}")
        if 4 not in entry.get("chapters", []):
            messages.append(f"references/sources.json: {source_id} does not map Chapter 4")
        notes = entry.get("notes")
        if not isinstance(notes, str):
            messages.append(f"references/sources.json: {source_id}.notes must be a string")
        else:
            for marker in contract["markers"]:
                if marker not in notes:
                    messages.append(f"references/sources.json: {source_id}.notes missing {marker!r}")
    mapped = {source_id for source_id, entry in entries.items() if 4 in entry.get("chapters", [])}
    if mapped != EXPECTED_SOURCE_IDS:
        messages.append(f"references/sources.json: Chapter 4 mapping {sorted(mapped)!r} != {sorted(EXPECTED_SOURCE_IDS)!r}")
    messages.extend(require_tokens(SOURCE_NOTE, note, (
        "Resumed-run workspace search",
        "Direct textual adoption in this PR: なし",
        "Raw predraft tracked files: `0`",
        "SRC-CSF-001",
        "SRC-NIST-RISK-001",
        "SRC-OWASP-TM-001",
        "Historical OWASP `Threat Modeling Process` page",
        "OWASP Threat Dragonは本文の論証に不要",
        "Registry rootの`checkedAt`",
    )))
    return messages


def page_contract_errors(registry: dict, label: str) -> list[str]:
    pages = registry.get("pages", [])
    tuples = Counter((item.get("source"), item.get("destination"), item.get("section"), item.get("order")) for item in pages if isinstance(item, dict))
    routes = Counter((item.get("source"), item.get("destination")) for item in pages if isinstance(item, dict))
    messages: list[str] = []
    for expected in sorted(EXPECTED_PAGES):
        if tuples[expected] != 1:
            messages.append(f"{label}: expected Chapter 4 tuple exactly once: {expected!r}; found {tuples[expected]}")
        if routes[expected[:2]] != 1:
            messages.append(f"{label}: expected Chapter 4 route exactly once: {expected[:2]!r}; found {routes[expected[:2]]}")
    return messages


def registry_rejected(registry: dict, label: str) -> bool:
    try:
        parsed = parse_registry_data(registry, label)
    except SitePageRegistryError:
        return True
    return bool(page_contract_errors(parsed, label))


def publication_contract_errors() -> list[str]:
    messages: list[str] = []
    index_contracts = {
        "artifact-index.md": ("ART-03", "cases/ch04-threat-model-example.md"),
        "figure-index.md": (
            "F-04-01 | Decision RequirementからReassessmentまでのTrace",
            "F-04-02 | 境界、Flow、攻撃面の読み分け",
            "T-04-01 | 資産の型と最小記録項目",
            "T-04-02 | 似て見える用語の違い",
            "T-04-03 | Control assurance states",
            "T-04-04 | Knowledge stateとHypothesis statusの分離",
        ),
        "glossary.md": ("Business Asset", "Data Asset", "Identity", "Control Plane", "Trust Boundary", "Attack Surface", "Exposure", "Entry Point", "Threat Hypothesis", "Misuse Case", "Attack Path", "Evidence Requirement", "Assurance State", "Knowledge State"),
        "cases/index.md": ("ch04-threat-model-example.md", "Threat Model"),
        "index.md": (CHAPTER, TEMPLATE, CASE),
    }
    for relative, tokens in index_contracts.items():
        messages.extend(require_tokens(relative, read_text(relative), tokens))
    try:
        tracked = subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
    except subprocess.CalledProcessError as exc:
        messages.append(f"git ls-files failed: {exc}")
    else:
        forbidden = [path for path in tracked if ".predraft." in path or "parallel-drafts-2026-08-08" in path or path.startswith(".work/")]
        if forbidden:
            messages.append(f"raw Editorial Input must remain untracked: {forbidden!r}")
    return messages


def negative_regressions(
    chapter: str,
    template: str,
    case: str,
    raw_registry: dict,
    sources: dict,
    note: str,
) -> None:
    chapter_mutations = (
        ("missing OWN", chapter.replace("### OWN", "### OWNERSHIP", 1)),
        ("inventory conflation", chapter.replace("Componentを列挙するだけでは", "ComponentはBusiness Assetなので列挙すれば", 1)),
        ("business asset type conflation", chapter.replace("`Business Asset`は8番目のTypeではなく", "`Business Asset`は8番目のTypeであり", 1)),
        ("network-only boundary", chapter.replace("Network segmentはBoundary候補に過ぎない", "Network segmentだけがTrust Boundaryの定義である", 1)),
        ("threat finding conflation", chapter.replace("`Threat`は、望ましくない事象や行為である。", "`Threat`は、`Vulnerability`および`Finding`と同義である。", 1)),
        ("control validation conflation", chapter.replace("文書化されたControlがあるので十分である\n誤りである", "文書化されたControlがあるのでValidatedである\n正しい。", 1)),
        ("mapping completeness", chapter.replace("CSFやOWASPへMappingしたので完全である\n誤りである", "CSFやOWASPへMappingしたので完全である\n正しい。", 1)),
        (
            "ART-03 canonical section drift",
            chapter.replace("10. `Assumptions, Unknowns and Gaps`", "10. `Inventory only`", 1),
        ),
        (
            "rubric mapping drift",
            chapter.replace("`RUBRIC-TM-YYYY-003` Threat usefulness and evidence sufficiency", "`RUBRIC-TM-YYYY-999` Threat count", 1),
        ),
    )
    for name, mutation in chapter_mutations:
        if not chapter_contract_errors(mutation, f"negative chapter {name}"):
            error(f"negative regression accepted Chapter 4 mutation: {name}")

    template_mutations = (
        ("model status", template.replace("Draft / In Review / Approved for Assessment / Needs Evidence / Superseded", "Draft / Complete", 1)),
        ("boundary finite set", template.replace("Identity Authority / Data Ownership / Administrative Control / Tenant / Third-party Responsibility / Control Plane / Network", "Network", 1)),
        ("control assurance", template.replace("Unknown / Documented / Implemented / Observed / Validated", "Mapped / Validated")),
        ("minimum evidence boundary", template.replace("Minimum sufficient evidence | Forbidden / over-collection boundary", "Evidence | Notes", 1)),
        ("Flow Evidence status", template.replace("| Planned |", "| Confirmed |", 1)),
        ("missing Decision owner", template.replace("| Decision owner |  |\n", "", 1)),
        ("Decision Context field drift", template.replace("| Decision deadline | ISO 8601 |", "| Review date | ISO 8601 |", 1)),
        ("Gap status", template.replace("| ISO 8601 date | Open |", "| ISO 8601 date | Confirmed |", 1)),
        (
            "Collected Evidence status",
            template.replace("| Synthetic / Authorized isolated / Inherited | Planned |", "| Synthetic / Authorized isolated / Inherited | Confirmed |", 1),
        ),
        (
            "Threat Hypothesis Evidence needed unsafe external action",
            template.replace(
                "|  |  | `EREQ-YYYY-NNN` |  | High / Medium / Low |",
                "|  |  | `EREQ-YYYY-NNN`。第三者の本番システムへ接続する |  | High / Medium / Low |",
                1,
            ),
        ),
        (
            "Attack Path From Asset State unsafe external action",
            template.replace(
                "| `PATH-YYYY-NNN` | `EDGE-YYYY-NNN` | `ASSET-YYYY-NNN` / state |  |",
                "| `PATH-YYYY-NNN` | `EDGE-YYYY-NNN` | `ASSET-YYYY-NNN` / 第三者の本番システムへ接続する |  |",
                1,
            ),
        ),
        (
            "Attack Path To Asset State unsafe external action",
            template.replace(
                "| `TB-YYYY-NNN` | `ASSET-YYYY-NNN` / state | `ASSET-YYYY-NNN` |",
                "| `TB-YYYY-NNN` | `ASSET-YYYY-NNN` / 第三者の本番システムへ接続する | `ASSET-YYYY-NNN` |",
                1,
            ),
        ),
    )
    for name, mutation in template_mutations:
        if not template_contract_errors(mutation, f"negative template {name}"):
            error(f"negative regression accepted ART-03 mutation: {name}")
    safety_matrix_negative_regressions(template, TEMPLATE, TEMPLATE_TABLE_OCCURRENCES)

    unsafe_samples = (
        "第三者の本番システムへ接続する",
        "実Tokenを取得してEvidenceにする",
        "個人情報を収集する",
        "マルウェアを実行する",
        "C2 infrastructureを運用する",
        "DoSを実行する",
        "システムのログを削除する",
        "persistenceを構築する",
        "https://example.comへ接続する",
        "198.18.0.1へ接続する",
    )
    for sample in unsafe_samples:
        if not policy_errors([("Chapter 4 negative safety mutation", sample)]):
            error(f"Content Safety Policy accepted unsafe Chapter 4 mutation: {sample!r}")
    safe_samples = (
        "第三者の本番システムへ接続しない",
        "合成Token literalをoffline fixtureで記録する",
        "個人情報の収集は禁止する",
        "マルウェア分類の危険性を分析する",
        "DoSを実行しない",
        "https://lab.example/runbook",
        "192.0.2.10",
    )
    for sample in safe_samples:
        findings = policy_errors([("Chapter 4 safe safety mutation", sample)])
        if findings:
            error(f"Content Safety Policy rejected safe Chapter 4 counterpart {sample!r}: {findings!r}")

    if case:
        case_mutations = (
            ("mixed Model status", case.replace("Needs Evidence", "Decision Support", 1)),
            (
                "self-parent relation cycle",
                case.replace("| Parent Case ID | `CASE-2026-001` |", "| Parent Case ID | `TM-2026-001` |", 1),
            ),
            (
                "missing Decision owner",
                case.replace("| Decision owner | Synthetic CTO Decision Owner |\n", "", 1),
            ),
            (
                "Decision Context field drift",
                case.replace("| Decision deadline | 2026-08-19T18:00:00+09:00 |", "| Review date | 2026-08-19T18:00:00+09:00 |", 1),
            ),
            (
                "top-level ART-03 section drift",
                case.replace("## 10. Evidence Requirements and Actions", "## 10. Evidence Inventory", 1),
            ),
            (
                "TH-2026-003 inherited proposition drift",
                case.replace(
                    "既に同型の不正利用が発生した",
                    "TelemetryとRetentionの制約により過去の影響範囲を十分に限定できない",
                    1,
                ),
            ),
            (
                "Confirmed without Evidence",
                case.replace(
                    "| `ASSET-2026-006` | Data | `invoice-sync-manifest` | 実請求書本文を含まない合成の同期要約、状態、再送管理Data | Finance Data Owner | High | Confidential | Assumed | `EVD-2026-002` |",
                    "| `ASSET-2026-006` | Data | `invoice-sync-manifest` | 実請求書本文を含まない合成の同期要約、状態、再送管理Data | Finance Data Owner | High | Confidential | Confirmed | - |",
                    1,
                ),
            ),
            (
                "Attack Path operational marker",
                case.replace(
                    "業務要件変更が承認ticketへ十分反映されない",
                    "command: synthetic-operation",
                    1,
                ),
            ),
            (
                "Path summary unsafe Safety note",
                case.replace(
                    "実Tokenを取得しない。実Dataを参照しない。設定差分と合成metadataだけで評価する。",
                    "実Tokenを取得して確認する。",
                    1,
                ),
            ),
            (
                "Review note unsafe external action",
                case.replace(
                    "Asset type、Boundary、Threat接続を確認",
                    "第三者の本番APIへ接続する。",
                    1,
                ),
            ),
            (
                "Threat Hypothesis unsafe credential handling",
                case.replace(
                    "業務要件を超えるscopeがsummary境界を越える影響へつながる可能性がある",
                    "実Tokenを取得して権限追加を確認する",
                    1,
                ),
            ),
            (
                "Threat Hypothesis Evidence needed unsafe external action",
                case.replace(
                    "| `EREQ-2026-003` | TelemetryとRetentionの制約により、未観測を未発生と判断できない | High | Inconclusive |",
                    "| `EREQ-2026-003`。第三者の本番システムへ接続する | TelemetryとRetentionの制約により、未観測を未発生と判断できない | High | Inconclusive |",
                    1,
                ),
            ),
            (
                "Control unsafe credential handling",
                case.replace(
                    "業務要件とscopeの対応表をReviewする",
                    "実Credentialを取得して監査する",
                    1,
                ),
            ),
            (
                "Exposure unsafe external action",
                case.replace("Isolated configuration surface", "第三者の本番APIへ接続する", 1),
            ),
            (
                "Entry Point unsafe external action",
                case.replace(
                    "合成App registrationとconsent objectのread-only Review接点",
                    "第三者の本番システムへ接続する",
                    1,
                ),
            ),
            (
                "Attack Path From Asset State unsafe external action",
                case.replace(
                    "| `ASSET-2026-004` / scope-review pending | 業務要件変更が承認ticketへ十分反映されない |",
                    "| `ASSET-2026-004` / 第三者の本番システムへ接続する | 業務要件変更が承認ticketへ十分反映されない |",
                    1,
                ),
            ),
            (
                "Attack Path To Asset State unsafe external action",
                case.replace(
                    "| `TB-2026-001` | `ASSET-2026-005` / scope matrix未更新 |",
                    "| `TB-2026-001` | `ASSET-2026-005` / 第三者の本番システムへ接続する |",
                    1,
                ),
            ),
            (
                "Collected Evidence unsafe collection condition",
                case.replace(
                    "第1章継承: App registration export; Observation `OBS-2026-001`; Validation `VAL-2026-001`; Authority / RoE `ROE-2026-001`; Integrity / hash SHA-256をEvidence manifestへ記録; Classification Internal",
                    "実Tokenを取得してEvidenceへ保存する",
                    1,
                ),
            ),
            (
                "inherited Evidence timestamp drift",
                case.replace(
                    "2026-07-20T13:20:00+09:00",
                    "2026-08-08T14:00:00+09:00",
                    1,
                ),
            ),
            (
                "inherited Evidence provenance drift",
                case.replace(
                    "第1章継承: 業務要件とAPI仕様のReview; Observation `OBS-2026-001`; Validation `VAL-2026-001`; Authority / RoE `ROE-2026-001`; Integrity / hash Review承認記録; Classification Internal",
                    "第4章で再作成した要件fixture",
                    1,
                ),
            ),
            (
                "invented Negative Finding timestamp",
                case.replace(
                    "原典にはstandaloneの`Collected at`がないため、時刻を創作せず、原典行をそのまま継承する。",
                    "原典にはstandaloneの`Collected at`がないが、2026-08-08T14:50:00+09:00として記録する。",
                    1,
                ),
            ),
            (
                "CTRL-2026-004 assurance overclaim",
                case.replace(
                    "| Lab Operator | Observed | `EVD-AUTH-2026-001`, `SYNTH-REV-TM-SAFE-001` |",
                    "| Lab Operator | Validated | `EVD-AUTH-2026-001`, `SYNTH-REV-TM-SAFE-001` |",
                    1,
                ),
            ),
            (
                "Flow Evidence status mixed with Knowledge state",
                case.replace("| Internal | Collected | 承認ticket、scope差分、例外理由 |", "| Internal | Confirmed | 承認ticket、scope差分、例外理由 |", 1),
            ),
            (
                "Evidence Requirement status mixed with Model status",
                case.replace("| SOC、Platform | 2026-08-18 | Required |", "| SOC、Platform | 2026-08-18 | Needs Evidence |", 1),
            ),
            (
                "Gap missing owner and due date",
                case.replace(
                    "| `GAP-2026-001` | `TH-2026-003` / `CTRL-2026-005`: API利用Telemetryのresource / operation粒度が不足する | `DR-2026-001`: 既往影響をsummary-only境界までしか限定できない | Platform | 2026-08-18 |",
                    "| `GAP-2026-001` | `TH-2026-003` / `CTRL-2026-005`: API利用Telemetryのresource / operation粒度が不足する | `DR-2026-001`: 既往影響をsummary-only境界までしか限定できない |  |  |",
                    1,
                ),
            ),
            (
                "Gap status mixed with Knowledge state",
                case.replace("| 2026-08-18 | Open | `EREQ-2026-003` |", "| 2026-08-18 | Confirmed | `EREQ-2026-003` |", 1),
            ),
            (
                "Collected Evidence status mixed with Knowledge state",
                case.replace(
                    "| Collected | Not recorded in inherited source | 2026-07-21T15:40:00+09:00 |",
                    "| Confirmed | Not recorded in inherited source | 2026-07-21T15:40:00+09:00 |",
                    1,
                ),
            ),
            (
                "Handoff semantic target drift",
                case.replace("| `HO-TM-2026-012` | 第12章 Identity評価 |", "| `HO-TM-2026-012` | 第27章 AI評価 |", 1),
            ),
        )
        for name, mutation in case_mutations:
            if mutation == case:
                error(f"negative Case mutation fixture did not match canonical text: {name}")
            elif not case_contract_errors(mutation, f"negative Case {name}"):
                error(f"negative regression accepted Chapter 4 Case mutation: {name}")
        safety_matrix_negative_regressions(case, CASE, CASE_TABLE_OCCURRENCES)

    source_mutation = deepcopy(sources)
    source_entry = next(
        (
            item
            for item in source_mutation.get("sources", [])
            if isinstance(item, dict) and item.get("id") == "SRC-OWASP-TM-001"
        ),
        None,
    )
    if source_entry is None:
        error("negative Source Registry mutation cannot find SRC-OWASP-TM-001")
    else:
        source_entry["notes"] = (
            "2026-08-08に公式Project pageを確認した。第4章では補助参照として用いる。"
        )
        if not source_contract_errors(chapter, source_mutation, note):
            error("negative Source Registry mutation accepted missing OWASP null-metadata rationale")

    pages = raw_registry.get("pages", [])
    target = next((item for item in pages if item.get("source") == CHAPTER), None)
    if target:
        mutations: list[tuple[str, dict]] = []
        mutation = deepcopy(raw_registry)
        mutation["schemaVersion"] = "0.0.0"
        mutations.append(("schema drift", mutation))
        for field, value in (("section", "additional"), ("order", 999)):
            mutation = deepcopy(raw_registry)
            next(item for item in mutation["pages"] if item.get("source") == CHAPTER)[field] = value
            mutations.append((f"{field} drift", mutation))
        mutation = deepcopy(raw_registry)
        mutation["pages"].append(deepcopy(target))
        mutations.append(("duplicate page", mutation))
        mutation = deepcopy(raw_registry)
        next(item for item in mutation["pages"] if item.get("source") == CHAPTER)["unexpectedKey"] = True
        mutations.append(("unknown key", mutation))
        mutation = deepcopy(raw_registry)
        next(item for item in mutation["pages"] if item.get("source") == CHAPTER)["destination"] = "../escape.md"
        mutations.append(("path traversal", mutation))
        mutation = deepcopy(raw_registry)
        next(item for item in mutation["pages"] if item.get("source") == CHAPTER)["destination"] = "assets/index.md"
        mutations.append(("reserved path", mutation))
        for name, mutation in mutations:
            if not registry_rejected(mutation, f"negative site registry {name}"):
                error(f"site-pages negative mutation was accepted: {name}")


def main() -> int:
    chapter = read_text(CHAPTER)
    template = read_text(TEMPLATE)
    case = read_text(CASE)
    note = read_text(SOURCE_NOTE)
    raw_registry = load_json("site-pages.json")
    sources = load_json("references/sources.json")

    if CONTENT_SAFETY_POLICY_VERSION != EXPECTED_POLICY_VERSION:
        error(f"Content Safety Policy version {CONTENT_SAFETY_POLICY_VERSION!r} != {EXPECTED_POLICY_VERSION!r}")

    ERRORS.extend(chapter_contract_errors(chapter, CHAPTER))
    ERRORS.extend(template_contract_errors(template, TEMPLATE))
    ERRORS.extend(case_contract_errors(case, CASE))
    ERRORS.extend(source_contract_errors(chapter, sources, note))
    ERRORS.extend(publication_contract_errors())

    try:
        registry = parse_registry_data(raw_registry)
    except SitePageRegistryError as exc:
        error(f"site-pages.json: invalid registry: {exc}")
        registry = {}
    ERRORS.extend(page_contract_errors(registry, "site-pages.json"))

    baseline = read_text("references/reference-baseline.md")
    if baseline and sources and baseline != render_reference_baseline():
        error("references/reference-baseline.md: out of sync with references/sources.json")

    negative_regressions(chapter, template, case, raw_registry, sources, note)

    if ERRORS:
        for message in ERRORS:
            print(f"ERROR: {message}", file=sys.stderr)
        print(f"Chapter 4 contract failed with {len(ERRORS)} error(s).", file=sys.stderr)
        return 1
    print(
        "Chapter 4 contract passed: ART-03, synthetic Case, source registry, "
        "Policy 1.2.0 adapter, exact publication routes, and negative regressions are valid."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
