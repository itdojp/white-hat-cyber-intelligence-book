#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.render_reference_baseline import (  # noqa: E402
    render as render_reference_baseline,
)
from scripts.sync_book_site import (  # noqa: E402
    SitePageRegistryError,
    parse_registry_data,
)

ERRORS: list[str] = []

EXPECTED_CHAPTER03_PAGES = {
    (
        "manuscript/03-capability-evidence.md",
        "chapters/chapter-03/index.md",
        "chapters",
        46,
    ),
    (
        "templates/capability-evidence-matrix.md",
        "templates/capability-evidence-matrix/index.md",
        "additional",
        234,
    ),
    (
        "cases/ch03-capability-evidence-example.md",
        "cases/chapter-03-capability-evidence/index.md",
        "additional",
        236,
    ),
}

CORE_TRACE = """Work Role / Responsibility
→ Task
→ Knowledge / Skill
→ Practice Environment
→ Artifact Evidence
→ Review / Rubric
→ Gap / Learning Action
→ Reassessment"""

STATUS_SET = {
    "Planned",
    "In practice",
    "Evidence submitted",
    "Reviewed",
    "Gap identified",
    "Reassessment due",
    "Complete",
}

EXPECTED_SOURCE = {
    "title": (
        "Workforce Framework for Cybersecurity (NICE Framework) and "
        "NICE Framework Components"
    ),
    "version": "SP 800-181 Rev.1; Components v2.2.0",
    "publishedAt": "2020-11-16",
    "checkedAt": "2026-08-05",
    "nextReviewAt": "2026-11-05",
}

EXPECTED_SOURCE_TRIGGERS = [
    "NIST SP 800-181 revision or errata",
    "NICE Framework Components major or minor release",
    "Changes to Work Role, Competency Area, or TKS identifiers used by Chapter 3",
]

EXPECTED_SOURCE_NOTE_MARKERS = (
    "Structural publication: NIST SP 800-181 Rev.1",
    "final, published 2020-11-16",
    "NICE Framework Components v2.2.0, released 2026-04-28",
    "Current Versions page displayed April 28, 2025",
    "2025 is treated as an apparent page typo",
    "OG-WRL-017",
    "NF-COM-006",
    "NF-COM-008",
    "common vocabulary and decomposition aid",
    "not as standalone proof of individual competence",
)


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


def missing_tokens(text: str, tokens: tuple[str, ...]) -> list[str]:
    return [token for token in tokens if token not in text]


def require_tokens(relative: str, text: str, tokens: tuple[str, ...]) -> None:
    for token in missing_tokens(text, tokens):
        error(f"{relative}: missing required token {token!r}")


def source_ids(text: str) -> set[str]:
    return set(re.findall(r"\bSRC-[A-Z0-9-]+\b", text))


def chapter_body_and_references(text: str) -> tuple[str, str]:
    marker = "## 参考文献・Source Note ID"
    if marker not in text:
        return text, ""
    return tuple(text.split(marker, 1))  # type: ignore[return-value]


def chapter_contract_errors(text: str, label: str) -> list[str]:
    messages: list[str] = []
    required = (
        "# 第3章　能力を分解し、証拠で学習する",
        "## この章の位置付け",
        "## 本章の責任境界",
        "### OWN",
        "### BRIDGE",
        "### DELEGATE",
        "委譲先を読まなくても、本章の中心論旨と`ART-14`の作成手順は単独で成立する",
        "## 学習目標",
        "## 前提知識",
        "## 導入ケース",
        "ART-01 Learning Route Plan",
        "第1章で整理した業務機能",
        "第2章のAuthority / Scope / Safety / Disclosure",
        "LEARN-CASE-2026-003",
        CORE_TRACE,
        "F-03-01 Capability Evidence Trace",
        "**Taskは、実行する仕事である。**",
        "**Knowledgeは、Taskに必要な概念または情報である。**",
        "**Skillは、観測可能な行為を実行するCapacityである。**",
        "**Competency Areaは、NICE Componentsにおける関連する能力領域のGroupingであり、個人が有能であることの証明ではない。**",
        "**Work Roleは仕事のGroupingであり、Job titleでも個人でもない。**",
        "**Artifact Evidenceは、明示した条件で作成され、第三者がReviewできる出力である。**",
        "**Review Resultは、一つのArtifact Evidenceを宣言済みRubricで評価した結果である。**",
        "**Capability Judgmentは、複数のEvidence itemに支えられた限定的な結論である。**",
        "**Reassessmentは、時間、Scope、Source、Role、Technology、Rubricの変更によって起動する後続Reviewである。**",
        "NIST SP 800-181 Rev.1",
        "NICE Framework Components v2.2.0",
        "NICEを次の用途に限定する",
        "identifierを一つ割り当てただけで個人の能力を証明する",
        "T-03-01 Evidenceの四分類",
        "良いEvidence",
        "弱いEvidence",
        "危険なEvidence",
        "結論不能なEvidence",
        "Job title、Certification、CTF score、Tool count、Chapter completion",
        "本書固有の学習進行",
        "observe",
        "explain",
        "assess",
        "design",
        "lead",
        "NISTが定めた普遍的なLevel標準ではない",
        "Scope",
        "Conditions",
        "Reviewer",
        "Limitations",
        "Expiry",
        "Reassessment Trigger",
        "実Targetへの攻撃回数",
        "実Target操作が必要になる",
        "ART-14 Capability Evidence Matrix",
        "Planned / In practice / Evidence submitted / Reviewed / Gap identified / Reassessment due / Complete",
        "## 10. 評価基準",
        "## 11. よくある誤解",
        "## 章のまとめ",
        "## 次に学ぶこと",
        "## 参考文献・Source Note ID",
        "SRC-NICE-001",
        "https://itdojp.github.io/pentest-learning-book/",
        "https://itdojp.github.io/practical-auth-book/",
        "https://itdojp.github.io/it-infra-security-guide-book/",
    )
    for token in missing_tokens(text, required):
        messages.append(f"{label}: missing required token {token!r}")

    body, references = chapter_body_and_references(text)
    body_ids = source_ids(body)
    reference_ids = source_ids(references)
    expected_ids = {"SRC-NICE-001"}
    if body_ids != expected_ids:
        messages.append(
            f"{label}: body source IDs {sorted(body_ids)} != {sorted(expected_ids)}"
        )
    if reference_ids != body_ids:
        messages.append(
            f"{label}: chapter-end source IDs {sorted(reference_ids)} "
            f"!= body {sorted(body_ids)}"
        )

    for forbidden in (
        "NISTが定めた普遍的なLevel標準である",
        "NICE identifierが個人の能力を証明する",
        "実Targetへの攻撃を学習証拠にする",
        "無許可の実Target操作をPracticeとする",
        "攻撃活動量が多いほど能力が高い",
    ):
        if forbidden in text:
            messages.append(f"{label}: unsafe or unsupported assertion {forbidden!r}")
    if re.search(r"https://github\.com/[^\s)]+/blob/main(?:/|\b)", text):
        messages.append(
            f"{label}: mutable GitHub blob/main URL must not be a delegated target"
        )
    return messages


def template_contract_errors(text: str, label: str) -> list[str]:
    required = (
        "# Capability Evidence Matrix",
        "Artifact ID | `ART-14`",
        "Matrix ID | `CAP-MATRIX-YYYY-NNN`",
        "Learner Profile ID | `SYNTH-LEARNER-NNN`",
        "Parent Artifact ID | `ART-01`",
        "Relation | `refines` / `supersedes` / `independent`",
        "NICE Components baseline | `v2.2.0`",
        "Task ID / statement",
        "Knowledge reference",
        "Skill reference",
        "Practice ID",
        "Authority / Environment",
        "Artifact / Evidence ID",
        "Reviewer",
        "Rubric",
        "Result",
        "Gap",
        "Learning Action",
        "Due date",
        "Reassessment ID",
        "Planned / In practice / Evidence submitted / Reviewed / Gap identified / Reassessment due / Complete",
        "## 5. Review Result",
        "## 6. Bounded Capability Judgment",
        "複数Evidence item",
        "Scope",
        "Conditions",
        "Limitations",
        "Expiry",
        "Reassessment Trigger",
        "## 8. Traceability Check",
        "人事評価、採用、昇進、報酬、資格認定、公開ランキングには使用しない",
        "実在Targetへの攻撃、実Credential、Token、Cookie、個人情報、従業員Data、顧客DataをEvidenceにしない",
    )
    return [f"{label}: missing required token {x!r}" for x in missing_tokens(text, required)]


def markdown_row_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def case_contract_errors(text: str, label: str) -> list[str]:
    messages: list[str] = []
    required = (
        "ART-14",
        "CAP-MATRIX-2026-003",
        "SYNTH-LEARNER-003",
        "Parent Artifact ID | `ART-01`",
        "Relation | `refines`",
        "LEARN-CASE-2026-003",
        "NICE Components baseline | `v2.2.0`",
        "CAP-CLAIM-2026-003",
        "TASK-CAP-001",
        "TASK-CAP-002",
        "TASK-CAP-003",
        "KN-CAP-001",
        "KN-CAP-002",
        "KN-CAP-003",
        "SK-CAP-001",
        "SK-CAP-002",
        "SK-CAP-003",
        "PRACTICE-CAP-001",
        "PRACTICE-CAP-002",
        "PRACTICE-CAP-003",
        "ART-EVD-CAP-001",
        "ART-EVD-CAP-002",
        "ART-EVD-CAP-003",
        "RUBRIC-CAP-001",
        "RUBRIC-CAP-002",
        "RUBRIC-CAP-003",
        "REV-CAP-001",
        "REV-CAP-002",
        "REV-CAP-003",
        "REA-CAP-001",
        "REA-CAP-002",
        "REA-CAP-003",
        "Authorization Checklistを作り",
        "offline detection fixture",
        "Source評価済みの分析判断",
        "Synthetic Safety Reviewer",
        "Synthetic Detection Reviewer",
        "Synthetic Analytic Reviewer",
        "Result | Partially supported",
        "Limitations",
        "Expiry | 2026-11-05T17:00:00+09:00",
        "Reassessment Trigger",
        "人物全体の能力",
        "実在する従業員、応募者、顧客、組織の人事評価ではない",
        "公開ランキング、採用、昇進、報酬、資格認定には使用しない",
        "実Target、実Credential、Token、Cookie、個人情報、従業員Data、顧客Dataを使用しない",
        "SYNTH-REV-CAP-TECH-001",
        "SYNTH-REV-CAP-SAFE-001",
        "SYNTH-REV-CAP-SOURCE-001",
        "SYNTH-REV-CAP-TRACE-001",
        "SYNTH-REV-CAP-DEC-001",
    )
    for token in missing_tokens(text, required):
        messages.append(f"{label}: missing required token {token!r}")

    entry_rows = [
        markdown_row_cells(line)
        for line in text.splitlines()
        if line.startswith("| `CAP-ENTRY-") and "PRACTICE-CAP-" in line
    ]
    if len(entry_rows) != 3:
        messages.append(f"{label}: expected exactly 3 Practice/Evidence entry rows")
    for cells in entry_rows:
        if len(cells) != 10:
            messages.append(f"{label}: malformed Practice/Evidence row {cells!r}")
            continue
        status = cells[7]
        if status not in STATUS_SET:
            messages.append(f"{label}: status outside finite set: {status!r}")

    for date in ("2026-08-12", "2026-08-19", "2026-08-26"):
        if date not in text:
            messages.append(f"{label}: missing bounded Learning Action due date {date}")

    forbidden = (
        "実Targetへの攻撃を実施する",
        "実Credentialを取得する",
        "従業員を順位付けする",
        "公開ランキングへ掲載する",
    )
    for assertion in forbidden:
        if assertion in text:
            messages.append(f"{label}: unsafe synthetic example {assertion!r}")
    return messages


def check_reserved_names(relative: str, text: str) -> None:
    allowed_suffixes = (".example", ".test", ".invalid", ".localhost")
    for raw_url in re.findall(r"https?://[^\s`)\]>]+", text):
        host = (urlparse(raw_url).hostname or "").lower()
        if host and not host.endswith(allowed_suffixes):
            error(f"{relative}: non-reserved URL in synthetic content: {raw_url}")
    domain_pattern = re.compile(
        r"(?<![A-Za-z0-9_-])(?:[A-Za-z0-9-]+\.)+(?:com|net|org|jp|io|dev|app|cloud)(?![A-Za-z0-9_-])",
        re.IGNORECASE,
    )
    for domain in domain_pattern.findall(text):
        error(f"{relative}: possible real domain in synthetic content: {domain}")


def source_contract_errors(registry: dict, label: str) -> list[str]:
    messages: list[str] = []
    if registry.get("checkedAt") != "2026-07-25":
        messages.append(
            f"{label}: registry-level checkedAt must remain 2026-07-25"
        )
    sources = registry.get("sources", [])
    if not isinstance(sources, list):
        return messages + [f"{label}: sources must be an array"]
    entries = {
        item.get("id"): item
        for item in sources
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    entry = entries.get("SRC-NICE-001")
    if entry is None:
        return messages + [f"{label}: missing SRC-NICE-001"]
    for field, expected in EXPECTED_SOURCE.items():
        if entry.get(field) != expected:
            messages.append(
                f"{label}: SRC-NICE-001.{field} must be {expected!r}"
            )
    if entry.get("status") != "final":
        messages.append(f"{label}: SRC-NICE-001.status must remain 'final'")
    if entry.get("reviewTriggers") != EXPECTED_SOURCE_TRIGGERS:
        messages.append(f"{label}: SRC-NICE-001.reviewTriggers changed")
    if entry.get("chapters") != [0, 1, 3]:
        messages.append(f"{label}: SRC-NICE-001.chapters must be [0, 1, 3]")
    chapter3_entries = {
        source_id
        for source_id, item in entries.items()
        if 3 in item.get("chapters", [])
    }
    if chapter3_entries != {"SRC-NICE-001"}:
        messages.append(
            f"{label}: Chapter 3 source mapping {sorted(chapter3_entries)} "
            "must match body source IDs ['SRC-NICE-001']"
        )
    notes = entry.get("notes")
    if not isinstance(notes, str):
        messages.append(f"{label}: SRC-NICE-001.notes must be a string")
    else:
        for marker in EXPECTED_SOURCE_NOTE_MARKERS:
            if marker not in notes:
                messages.append(
                    f"{label}: SRC-NICE-001.notes missing marker {marker!r}"
                )
    return messages


def chapter03_page_contract_errors(registry: dict, label: str) -> list[str]:
    messages: list[str] = []
    pages = registry.get("pages", [])
    if not isinstance(pages, list):
        return [f"{label}: pages must be an array"]
    actual = [
        (
            item.get("source"),
            item.get("destination"),
            item.get("section"),
            item.get("order"),
        )
        for item in pages
        if isinstance(item, dict)
    ]
    tuple_counts = Counter(actual)
    route_counts = Counter(item[:2] for item in actual)
    for expected in sorted(EXPECTED_CHAPTER03_PAGES):
        if tuple_counts[expected] != 1:
            messages.append(
                f"{label}: expected Chapter 3 tuple exactly once: {expected!r}; "
                f"found {tuple_counts[expected]}"
            )
        if route_counts[expected[:2]] != 1:
            messages.append(
                f"{label}: expected Chapter 3 route exactly once: {expected[:2]!r}; "
                f"found {route_counts[expected[:2]]}"
            )
    return messages


def registry_mutation_is_rejected(registry: dict, label: str) -> bool:
    try:
        parsed = parse_registry_data(registry, label)
    except SitePageRegistryError:
        return True
    return bool(chapter03_page_contract_errors(parsed, label))


def verify_negative_regressions(
    chapter: str,
    template: str,
    case: str,
    sources: dict,
    raw_registry: dict,
) -> None:
    chapter_without_trace = chapter.replace(CORE_TRACE, "Task → Evidence")
    if not chapter_contract_errors(chapter_without_trace, "negative chapter core trace"):
        error("negative regression accepted Chapter 3 without the core trace")

    chapter_with_false_standard = chapter.replace(
        "NISTが定めた普遍的なLevel標準ではない",
        "NISTが定めた普遍的なLevel標準である",
    )
    if not chapter_contract_errors(
        chapter_with_false_standard, "negative universal level assertion"
    ):
        error("negative regression accepted a false universal NICE level assertion")

    template_status_drift = template.replace(
        "Planned / In practice / Evidence submitted / Reviewed / Gap identified / Reassessment due / Complete",
        "Planned / In practice / Ranked / Complete",
    )
    if not template_contract_errors(template_status_drift, "negative status drift"):
        error("negative regression accepted Capability Evidence status drift")

    unsafe_case = case + "\n実Targetへの攻撃を実施する\n"
    if not case_contract_errors(unsafe_case, "negative real-target practice"):
        error("negative regression accepted real-target activity as learning evidence")

    source_mutations: list[tuple[str, dict]] = []
    for field, value in (
        ("version", "Components latest"),
        ("checkedAt", "2026-07-25"),
        ("nextReviewAt", "2027-01-01"),
        ("notes", "NICE proves competence"),
    ):
        mutation = deepcopy(sources)
        entry = next(item for item in mutation["sources"] if item.get("id") == "SRC-NICE-001")
        entry[field] = value
        source_mutations.append((field, mutation))
    for field, mutation in source_mutations:
        if not source_contract_errors(mutation, f"negative source {field}"):
            error(f"negative regression accepted SRC-NICE-001 {field} drift")

    page_source = "manuscript/03-capability-evidence.md"
    page_mutations: list[tuple[str, dict]] = []
    mutation = deepcopy(raw_registry)
    mutation["schemaVersion"] = "0.0.0"
    page_mutations.append(("schemaVersion drift", mutation))
    mutation = deepcopy(raw_registry)
    next(item for item in mutation["pages"] if item.get("source") == page_source)["section"] = "additional"
    page_mutations.append(("section drift", mutation))
    mutation = deepcopy(raw_registry)
    next(item for item in mutation["pages"] if item.get("source") == page_source)["order"] = 47
    page_mutations.append(("order drift", mutation))
    mutation = deepcopy(raw_registry)
    page = next(item for item in mutation["pages"] if item.get("source") == page_source)
    mutation["pages"].append(deepcopy(page))
    page_mutations.append(("duplicate page", mutation))
    mutation = deepcopy(raw_registry)
    next(item for item in mutation["pages"] if item.get("source") == page_source)["unexpectedKey"] = True
    page_mutations.append(("unknown page key", mutation))
    for name, mutation in page_mutations:
        if not registry_mutation_is_rejected(
            mutation, f"site-pages.json negative regression ({name})"
        ):
            error(f"site-pages.json: negative mutation was accepted: {name}")


def main() -> int:
    required_files = (
        "manuscript/03-capability-evidence.md",
        "templates/capability-evidence-matrix.md",
        "cases/ch03-capability-evidence-example.md",
        "scripts/check_chapter03_contract.py",
        "site-pages.json",
        "artifact-index.md",
        "figure-index.md",
        "glossary.md",
        "cases/index.md",
        "index.md",
        "book-config.json",
        "references/sources.json",
        "references/reference-baseline.md",
        "references/ch03-source-review-2026-08-05.md",
        "package.json",
    )
    for relative in required_files:
        if not (ROOT / relative).is_file():
            error(f"missing required file: {relative}")

    config = load_json("book-config.json")
    chapter_config = next(
        (
            item
            for item in config.get("structure", {}).get("chapters", [])
            if isinstance(item, dict) and item.get("id") == "ch03-capability-evidence"
        ),
        None,
    )
    expected_objectives = [
        "能力を分解できる",
        "学習証拠を定義できる",
        "Capability Evidence Matrixを作成できる",
    ]
    if chapter_config is None:
        error("book-config.json: missing ch03-capability-evidence")
    elif chapter_config.get("objectives") != expected_objectives:
        error("book-config.json: chapter 3 learning objectives changed unexpectedly")

    chapter_path = "manuscript/03-capability-evidence.md"
    template_path = "templates/capability-evidence-matrix.md"
    case_path = "cases/ch03-capability-evidence-example.md"
    chapter = read_text(chapter_path)
    template = read_text(template_path)
    case = read_text(case_path)
    for message in chapter_contract_errors(chapter, chapter_path):
        error(message)
    for message in template_contract_errors(template, template_path):
        error(message)
    for message in case_contract_errors(case, case_path):
        error(message)
    check_reserved_names(case_path, case)

    secret_patterns = (
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
        re.compile(
            r"(?i)(?:password|api[_-]?key|secret|token)\s*[:=]\s*[A-Za-z0-9+/=_-]{16,}"
        ),
    )
    for relative, text in ((chapter_path, chapter), (template_path, template), (case_path, case)):
        for pattern in secret_patterns:
            if pattern.search(text):
                error(f"{relative}: possible real credential or secret pattern detected")

    raw_registry = load_json("site-pages.json")
    try:
        registry = parse_registry_data(raw_registry)
    except SitePageRegistryError as exc:
        error(f"site-pages.json: invalid registry: {exc}")
        registry = {}
    for message in chapter03_page_contract_errors(registry, "site-pages.json"):
        error(message)

    require_tokens(
        "artifact-index.md",
        read_text("artifact-index.md"),
        (
            "| ART-14 | Capability Evidence Matrix | 3, 29 | `templates/capability-evidence-matrix.md` |",
            "cases/ch03-capability-evidence-example.md",
        ),
    )
    require_tokens(
        "figure-index.md",
        read_text("figure-index.md"),
        ("F-03-01", "T-03-01", "T-03-02", "manuscript/03-capability-evidence.md"),
    )
    require_tokens(
        "glossary.md",
        read_text("glossary.md"),
        (
            "| Artifact Evidence |",
            "| Capability Judgment |",
            "| Competency Area |",
            "| Reassessment |",
            "| Review Result |",
            "| Work Role |",
        ),
    )
    require_tokens(
        "cases/index.md",
        read_text("cases/index.md"),
        ("ch03-capability-evidence-example.md", "Capability Evidence Matrix"),
    )
    require_tokens(
        "index.md",
        read_text("index.md"),
        (
            "manuscript/03-capability-evidence.md",
            "templates/capability-evidence-matrix.md",
            "cases/ch03-capability-evidence-example.md",
        ),
    )

    sources = load_json("references/sources.json")
    for message in source_contract_errors(sources, "references/sources.json"):
        error(message)

    audit_note_path = "references/ch03-source-review-2026-08-05.md"
    audit_note = read_text(audit_note_path)
    require_tokens(
        audit_note_path,
        audit_note,
        (
            "Checked at | 2026-08-05",
            "NIST SP 800-181 Rev.1",
            "2020-11-16",
            "NICE Framework Components v2.2.0",
            "2026-04-28",
            "OG-WRL-017",
            "NF-COM-006",
            "NF-COM-008",
            "administrative changes",
            "CURRENT VERSION: 2.2.0 (April 28, 2025)",
            "見かけ上のページ誤記",
            "Certification vendorの資料は、標準や能力証明の根拠として採用していない",
            "個人の能力を証明しない",
            "本書固有の学習進行表現",
        ),
    )
    official_urls = (
        "https://csrc.nist.gov/pubs/sp/800/181/r1/final",
        "https://www.nist.gov/news-events/news/2026/04/nice-releases-nice-framework-components-v220",
        "https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center/current-version/change-logs",
        "https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center/nice-framework-current-versions",
        "https://csrc.nist.gov/projects/cprt/catalog",
    )
    require_tokens(audit_note_path, audit_note, official_urls)

    baseline_path = "references/reference-baseline.md"
    if read_text(baseline_path) != render_reference_baseline():
        error(f"{baseline_path}: out of sync with references/sources.json")

    package = load_json("package.json")
    scripts = package.get("scripts", {})
    if scripts.get("check:chapter03") != "python3 scripts/check_chapter03_contract.py":
        error("package.json: missing check:chapter03 script")
    if "check:chapter03" not in scripts.get("test", ""):
        error("package.json: npm test does not include check:chapter03")

    if chapter and template and case and sources and raw_registry:
        verify_negative_regressions(chapter, template, case, sources, raw_registry)

    for message in ERRORS:
        print(f"ERROR: {message}")
    if ERRORS:
        return 1

    print(
        "chapter 3 contract passed: manuscript, ART-14, synthetic learner case, "
        "NICE source state, publication registry, safety boundary, and fail-closed regressions"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
