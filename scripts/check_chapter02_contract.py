#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.render_reference_baseline import (  # noqa: E402
    render as render_reference_baseline,
)
from scripts.content_safety_policy import (  # noqa: E402
    POLICY_VERSION as CONTENT_SAFETY_POLICY_VERSION,
    SafetyFinding,
    scan_action_text,
    scan_host_policy,
)
from scripts.sync_book_site import (  # noqa: E402
    SitePageRegistryError,
    parse_registry_data,
)

ERRORS: list[str] = []
EXPECTED_CONTENT_SAFETY_POLICY_VERSION = "1.2.0"

CHAPTER02_POLICY_SECTIONS = {
    "manuscript/02-law-ethics-authorization.md": (
        "## 1. 四つのGate",
        "## 2. 法、契約、組織権限、倫理を分離する",
        "## 3. 書面による許可",
        "## 4. Data、Secret、証拠の取扱い",
        "## 5. 委託、再委託、Cloud / SaaS",
        "## 6. 脆弱性を発見したとき",
        "## 7. 四つの視点",
        "## 8. Handoff Contract",
        "## 9. 安全な演習",
        "## 10. 作成する成果物",
        "## 11. 評価基準",
        "## 12. よくある誤解",
    ),
    "templates/authorization-checklist.md": (
        "## 使用条件",
        "## 0. Document Control",
        "## 1. Decision Requirement",
        "## 2. Authority Gate",
        "## 3. Scope Gate",
        "## 4. Safety Gate",
        "## 5. Disclosure Gate",
        "## 6. Legal, Contractual, and Policy Questions",
        "## 7. Conditions",
        "## 8. Decision Record",
        "## 9. RoE Handoff",
        "## 10. Reassessment",
        "## 11. Traceability Check",
        "## 12. Review",
    ),
    "cases/ch02-authorization-decision-example.md": (
        "## この記入例の扱い",
        "## 0. Document Control",
        "## 1. Decision Requirement",
        "## 2. Authority Gate",
        "## 3. Scope Gate",
        "## 4. Safety Gate",
        "## 5. Disclosure Gate",
        "## 6. Legal, Contractual, and Policy Questions",
        "## 7. Conditions",
        "## 8. Decision Record",
        "## 9. RoE Handoff",
        "## 10. Reassessment",
        "## 11. Traceability Check",
        "## 12. Review",
    ),
}
CHAPTER02_POLICY_PREAMBLE_DOCUMENTS = frozenset(
    {
        "templates/authorization-checklist.md",
        "cases/ch02-authorization-decision-example.md",
    }
)
CHAPTER02_POLICY_TERMINAL_BOUNDARIES = {
    "manuscript/02-law-ethics-authorization.md": "## 章のまとめ",
    "templates/authorization-checklist.md": None,
    "cases/ch02-authorization-decision-example.md": None,
}

# These exact lines are reviewed non-operative context: an uncertainty, question,
# prohibition, or reject/return boundary.  Scanning the fragments without their
# table/paragraph semantics would turn them into affirmative instructions.  Any
# edit removes the exemption and is delegated to Policy 1.2.0 until this finite
# reviewed set is updated deliberately.
CHAPTER02_REVIEWED_ACTION_CONTEXT = {
    "manuscript/02-law-ethics-authorization.md": frozenset(
        {
            "一つの層がPassしても、他の層を自動的にPassさせない。たとえば契約にSecurity testingの記載があっても、第三者Tenantや実利用者Dataまで対象になるとは限らない。",
            "- 未確認: 委託先が管理するApp credentialの変更権限",
        }
    ),
    "templates/authorization-checklist.md": frozenset(),
    "cases/ch02-authorization-decision-example.md": frozenset(
        {
            "| Maximum acceptable uncertainty | 委託先が管理するProduction credentialの変更権限は未確定でも、合成Tenantのread-only設定Reviewだけを分離できること |",
            "| Authority gaps | Production credential変更権限と委託契約上の作業範囲は未確認 |",
            "| Prohibited methods | Token取得・利用、外部API call、Credential変更、権限昇格、横展開、DoS、Data変更 |",
            "| `LQ-AUTH-2026-002` | 委託契約はProduction credential変更を許容するか | Synthetic contract | Procurement / Legal | Escalated | 本Decisionでは不要。Production変更前に確認 | Production変更案承認前 |",
            "| `LQ-AUTH-2026-004` | 許可外の認証試行を行ってよいか | `SRC-JP-LAW-001`、internal policy | Legal | Answered | 行わない。合成Tenant・明示許可操作だけに限定 | Scope変更時 |",
            "| Information gaps | Production credential変更権限、実Vendor窓口、契約通知期限 |",
            "| `HO-AUTH-2026-004` | Method boundary | Read-only、禁止操作、Rate | Pass | Token利用・外部API追加 | Lab Operator |",
        }
    ),
}

# Issue #67 tracks the shared core's Japanese-particle host-token boundary.  Until
# that independent Policy change lands, keep only these exact approved-host lines
# frozen.  A changed line is scanned normally, so .localhost or a real host cannot
# inherit this exemption.
CHAPTER02_REVIEWED_HOST_CONTEXT = {
    "manuscript/02-law-ethics-authorization.md": frozenset(
        {"- 対象: `billing-bridge.example`の合成Tenant"}
    ),
    "templates/authorization-checklist.md": frozenset(),
    "cases/ch02-authorization-decision-example.md": frozenset(
        {
            "- Domainは予約済みの`.example`を使用する。",
            "| In-scope target identifiers | `tenant-auth-lab-01.test`、`billing-bridge.example`の合成App registration、設定Export |",
        }
    ),
}

EXPECTED_CHAPTER02_PAGES = {
    (
        "manuscript/02-law-ethics-authorization.md",
        "chapters/chapter-02/index.md",
        "chapters",
        45,
    ),
    (
        "templates/authorization-checklist.md",
        "templates/authorization-checklist/index.md",
        "additional",
        232,
    ),
    (
        "cases/ch02-authorization-decision-example.md",
        "cases/chapter-02-authorization-decision/index.md",
        "additional",
        233,
    ),
}


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


def require_tokens(relative: str, text: str, tokens: tuple[str, ...]) -> None:
    for token in tokens:
        if token not in text:
            error(f"{relative}: missing required token {token!r}")


def chapter02_page_contract_errors(registry: dict, label: str) -> list[str]:
    messages: list[str] = []
    pages = registry.get("pages", [])
    if not isinstance(pages, list):
        return [f"{label}: pages must be an array"]

    actual_tuples = [
        (
            item.get("source"),
            item.get("destination"),
            item.get("section"),
            item.get("order"),
        )
        for item in pages
        if isinstance(item, dict)
    ]
    tuple_counts = Counter(actual_tuples)
    route_counts = Counter(item[:2] for item in actual_tuples)
    for expected in sorted(EXPECTED_CHAPTER02_PAGES):
        tuple_count = tuple_counts[expected]
        if tuple_count != 1:
            messages.append(
                f"{label}: expected Chapter 2 page tuple exactly once: "
                f"{expected!r}; found {tuple_count}"
            )
        route_count = route_counts[expected[:2]]
        if route_count != 1:
            messages.append(
                f"{label}: expected Chapter 2 source/destination exactly once: "
                f"{expected[:2]!r}; found {route_count}"
            )
    return messages


def registry_mutation_is_rejected(registry: dict, label: str) -> bool:
    try:
        parsed = parse_registry_data(registry, label)
    except SitePageRegistryError:
        return True
    return bool(chapter02_page_contract_errors(parsed, label))


def source_ids(text: str) -> set[str]:
    return set(re.findall(r"\bSRC-[A-Z0-9-]+\b", text))


def chapter_body_and_references(text: str) -> tuple[str, str]:
    marker = "## 参考文献・Source Note ID"
    if marker not in text:
        return text, ""
    body, references = text.split(marker, 1)
    return body, references


def _is_markdown_table_delimiter(line: str) -> bool:
    stripped = line.strip().strip("|")
    if not stripped:
        return False
    cells = [cell.strip() for cell in stripped.split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def _is_markdown_policy_block_start(line: str) -> bool:
    stripped = line.lstrip()
    return bool(
        re.match(r"#{1,6}\s+", stripped)
        or stripped.startswith("|")
        or re.match(r"(?:[-+*]|\d+[.)])\s+", stripped)
    )


def _reader_visible_policy_blocks(
    lines: list[str],
    *,
    start: int,
    end: int,
    location_prefix: str,
) -> list[tuple[str, str]]:
    """Project Markdown soft-wrapped source into bounded visible blocks."""

    blocks: list[tuple[str, str]] = []
    pending: list[tuple[int, str]] = []

    def flush() -> None:
        if not pending:
            return
        start_line = pending[0][0] + 1
        end_line = pending[-1][0] + 1
        line_label = (
            f"line {start_line}"
            if start_line == end_line
            else f"lines {start_line}-{end_line}"
        )
        # A normal Markdown source newline inside one paragraph or list item is a
        # soft wrap rendered as whitespace.  Project it to a space before Policy
        # scanning so an object/action pair cannot be split across source lines.
        visible_text = " ".join(value.strip() for _, value in pending)
        blocks.append((f"{location_prefix} {line_label}", visible_text))
        pending.clear()

    for index in range(start, end):
        value = lines[index]
        if not value.strip() or _is_markdown_table_delimiter(value):
            flush()
            continue
        if _is_markdown_policy_block_start(value):
            flush()
            pending.append((index, value))
            if value.lstrip().startswith(("#", "|")):
                flush()
            continue
        pending.append((index, value))
    flush()
    return blocks


def chapter02_reader_visible_policy_fields(
    relative: str,
    text: str,
) -> tuple[list[tuple[str, str]], list[str]]:
    """Select the finite Chapter 2 action/authorization publication surface.

    The adapter owns section and line selection.  Shared Policy 1.2.0 owns
    normalization, protected-action semantics, and host/address classification.
    Public DELEGATE and Source URLs intentionally remain outside this synthetic
    execution surface; their stability is enforced by the existing Chapter 2
    publication/source contracts.
    """

    expected_headings = CHAPTER02_POLICY_SECTIONS.get(relative)
    if expected_headings is None:
        return [], [f"{relative}: no Chapter 2 Policy section contract"]

    lines = text.splitlines()
    headings: list[tuple[int, int, str]] = []
    for index, line in enumerate(lines):
        match = re.fullmatch(r"(#{1,6})\s+(.+?)\s*", line)
        if match:
            headings.append((index, len(match.group(1)), line.rstrip()))

    fields: list[tuple[str, str]] = []
    messages: list[str] = []
    claimed_lines: set[int] = set()
    if relative in CHAPTER02_POLICY_PREAMBLE_DOCUMENTS:
        first_heading_matches = [
            item for item in headings if item[2] == expected_headings[0]
        ]
        if len(first_heading_matches) == 1:
            preamble_end = first_heading_matches[0][0]
            claimed_lines.update(range(0, preamble_end))
            fields.extend(
                _reader_visible_policy_blocks(
                    lines,
                    start=0,
                    end=preamble_end,
                    location_prefix=f"{relative} document preamble",
                )
            )
    for heading_index, expected_heading in enumerate(expected_headings):
        matches = [item for item in headings if item[2] == expected_heading]
        if len(matches) != 1:
            messages.append(
                f"{relative}: expected Policy section exactly once: "
                f"{expected_heading!r}; found {len(matches)}"
            )
            continue
        start, level, _ = matches[0]
        end = len(lines)
        boundary_heading: str | None = None
        for candidate, candidate_level, candidate_heading in headings:
            if candidate > start and candidate_level <= level:
                end = candidate
                boundary_heading = candidate_heading
                break
        expected_boundary = (
            expected_headings[heading_index + 1]
            if heading_index + 1 < len(expected_headings)
            else CHAPTER02_POLICY_TERMINAL_BOUNDARIES[relative]
        )
        if boundary_heading != expected_boundary:
            messages.append(
                f"{relative}: unexpected Policy section boundary after "
                f"{expected_heading!r}: {boundary_heading!r}; expected "
                f"{expected_boundary!r}"
            )
        for index in range(start, end):
            if index in claimed_lines:
                messages.append(
                    f"{relative}: overlapping Policy section selection at line {index + 1}"
                )
            claimed_lines.add(index)
        fields.extend(
            _reader_visible_policy_blocks(
                lines,
                start=start,
                end=end,
                location_prefix=f"{relative} {expected_heading}",
            )
        )
    return fields, messages


def _finding_sort_key(finding: SafetyFinding) -> tuple[str, str, str, str, str]:
    return (
        finding.location,
        finding.category,
        finding.normalized_excerpt,
        finding.reason,
        finding.policy_version,
    )


def chapter02_policy_findings(
    documents: dict[str, str],
) -> tuple[list[SafetyFinding], list[str]]:
    findings: set[SafetyFinding] = set()
    messages: list[str] = []
    for relative in CHAPTER02_POLICY_SECTIONS:
        text = documents.get(relative)
        if text is None:
            messages.append(f"{relative}: missing document for Chapter 2 Policy adapter")
            continue
        fields, selection_errors = chapter02_reader_visible_policy_fields(relative, text)
        messages.extend(selection_errors)
        selected_value_counts = Counter(value for _, value in fields)
        for context_name, reviewed_lines in (
            ("action", CHAPTER02_REVIEWED_ACTION_CONTEXT[relative]),
            ("host", CHAPTER02_REVIEWED_HOST_CONTEXT[relative]),
        ):
            for value in sorted(reviewed_lines):
                count = selected_value_counts[value]
                if count != 1:
                    messages.append(
                        f"{relative}: reviewed {context_name} context must occur "
                        f"exactly once in the bounded Policy surface; found {count}: "
                        f"{value!r}"
                    )

        for location, value in fields:
            if value not in CHAPTER02_REVIEWED_ACTION_CONTEXT[relative]:
                findings.update(scan_action_text(value, location=location))
            if value not in CHAPTER02_REVIEWED_HOST_CONTEXT[relative]:
                findings.update(scan_host_policy(value, location=location))

    return sorted(findings, key=_finding_sort_key), messages


def format_policy_finding(finding: SafetyFinding) -> str:
    return (
        f"{finding.location}: [{finding.category}] {finding.reason}: "
        f"{finding.normalized_excerpt!r} "
        f"(Content Safety Policy {finding.policy_version})"
    )


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        error(f"{label}: mutation anchor must occur exactly once; found {count}")
        return text
    return text.replace(old, new, 1)


def verify_policy_adapter_regressions(
    chapter: str,
    template: str,
    example: str,
) -> None:
    documents = {
        "manuscript/02-law-ethics-authorization.md": chapter,
        "templates/authorization-checklist.md": template,
        "cases/ch02-authorization-decision-example.md": example,
    }
    canonical_findings, selection_errors = chapter02_policy_findings(documents)
    for message in selection_errors:
        error(message)
    for finding in canonical_findings:
        error(format_policy_finding(finding))

    unsafe_case_preamble_mutations = (
        ("leading preamble", "https://example.com/runbook\n" + example),
        (
            "H1 title",
            replace_once(
                example,
                "# 第2章 合成記入例：OAuth連携評価前のAuthorization判断",
                "# 第2章 合成記入例：https://example.com/runbook",
                "Chapter 2 Case H1 regression",
            ),
        ),
    )
    for surface, unsafe_case_preamble in unsafe_case_preamble_mutations:
        unsafe_case_preamble_documents = dict(documents)
        unsafe_case_preamble_documents[
            "cases/ch02-authorization-decision-example.md"
        ] = unsafe_case_preamble
        unsafe_case_preamble_findings, _ = chapter02_policy_findings(
            unsafe_case_preamble_documents
        )
        if not any(
            finding.category == "network.host_or_address"
            and "non-approved host suffix" in finding.reason
            for finding in unsafe_case_preamble_findings
        ):
            error(
                f"Chapter 2 Case {surface} bypassed the host Policy adapter"
            )

    soft_wrap_anchor = "- 不足情報を推測でPassにしない。"
    soft_wrapped_template = replace_once(
        template,
        soft_wrap_anchor,
        soft_wrap_anchor + "\n- 実Credentialを\n  取得する",
        "Chapter 2 Markdown soft-wrap regression",
    )
    soft_wrap_documents = dict(documents)
    soft_wrap_documents["templates/authorization-checklist.md"] = soft_wrapped_template
    soft_wrap_findings, _ = chapter02_policy_findings(soft_wrap_documents)
    if not any(
        finding.category == "secret.credential" for finding in soft_wrap_findings
    ):
        error("Chapter 2 Markdown soft wrap split a protected object from its action")

    unclassified_section_template = replace_once(
        template,
        "## 3. Scope Gate",
        "## Unclassified operational section\n\n第三者の本番APIへ接続する\n\n"
        "## 3. Scope Gate",
        "Chapter 2 unclassified section regression",
    )
    unclassified_documents = dict(documents)
    unclassified_documents["templates/authorization-checklist.md"] = (
        unclassified_section_template
    )
    _, unclassified_errors = chapter02_policy_findings(unclassified_documents)
    if not any("unexpected Policy section boundary" in message for message in unclassified_errors):
        error("Chapter 2 Policy adapter accepted an unclassified section boundary")

    trailing_section_template = template + (
        "\n## Unclassified trailing operational section\n\n"
        "第三者の本番APIへ接続する\n"
    )
    trailing_section_documents = dict(documents)
    trailing_section_documents["templates/authorization-checklist.md"] = (
        trailing_section_template
    )
    _, trailing_section_errors = chapter02_policy_findings(
        trailing_section_documents
    )
    if not any(
        "unexpected Policy section boundary" in message
        for message in trailing_section_errors
    ):
        error("Chapter 2 Policy adapter accepted an unclassified trailing section")

    action_anchor = "| Allowed methods |  |"
    unsafe_actions = (
        ("real target", "第三者の本番APIへ接続する", "target.real_or_external"),
        ("credential", "実Credentialを取得する", "secret.credential"),
        ("token reuse", "Tokenを再利用する", "operation.authentication_or_session"),
        ("cookie", "Cookieを取得する", "secret.credential"),
        ("session", "synthetic sessionをreplayする", "operation.authentication_or_session"),
        ("PII", "個人情報を収集する", "data.pii"),
        ("malware", "keyloggerを作る", "operation.malware"),
        ("C2", "C2 serverを構築する", "operation.c2_or_phishing"),
        ("DoS", "DoSを実行する", "operation.disruption_or_destruction"),
        ("destruction", "本番データを破壊する", "operation.disruption_or_destruction"),
    )
    for name, unsafe_text, expected_category in unsafe_actions:
        mutated_template = replace_once(
            template,
            action_anchor,
            f"| Allowed methods | {unsafe_text} |",
            f"Chapter 2 unsafe {name} regression",
        )
        mutated_documents = dict(documents)
        mutated_documents["templates/authorization-checklist.md"] = mutated_template
        findings, _ = chapter02_policy_findings(mutated_documents)
        if not any(finding.category == expected_category for finding in findings):
            error(
                f"Chapter 2 Policy adapter accepted unsafe {name} mutation; "
                f"expected category {expected_category}"
            )

    unsafe_chapter = replace_once(
        chapter,
        "- 目的: OAuth permissionの設定Review",
        "- 目的: OAuth permissionの設定Review\n- 第三者の本番APIへ接続する",
        "Chapter 2 manuscript action-surface regression",
    )
    unsafe_chapter_documents = dict(documents)
    unsafe_chapter_documents["manuscript/02-law-ethics-authorization.md"] = unsafe_chapter
    chapter_findings, _ = chapter02_policy_findings(unsafe_chapter_documents)
    if not any(
        finding.category == "target.real_or_external" for finding in chapter_findings
    ):
        error("Chapter 2 manuscript action-bearing field bypassed Policy 1.2.0")

    unsafe_case = replace_once(
        example,
        "| `COND-AUTH-2026-001` | Production credentialを操作しない |",
        "| `COND-AUTH-2026-001` | 実Credentialを取得する |",
        "Chapter 2 Case condition-surface regression",
    )
    unsafe_case_documents = dict(documents)
    unsafe_case_documents["cases/ch02-authorization-decision-example.md"] = unsafe_case
    case_findings, _ = chapter02_policy_findings(unsafe_case_documents)
    if not any(finding.category == "secret.credential" for finding in case_findings):
        error("Chapter 2 Case Condition field bypassed Policy 1.2.0")

    reviewed_boundary = (
        "| Prohibited methods | Token取得・利用、外部API call、Credential変更、"
        "権限昇格、横展開、DoS、Data変更 |"
    )
    unsafe_reviewed_boundary_case = replace_once(
        example,
        reviewed_boundary,
        reviewed_boundary[:-1] + "。しかし実Credentialを取得する |",
        "Chapter 2 reviewed-context invalidation regression",
    )
    reviewed_boundary_documents = dict(documents)
    reviewed_boundary_documents["cases/ch02-authorization-decision-example.md"] = (
        unsafe_reviewed_boundary_case
    )
    reviewed_boundary_findings, _ = chapter02_policy_findings(
        reviewed_boundary_documents
    )
    if not any(
        finding.category == "secret.credential"
        for finding in reviewed_boundary_findings
    ):
        error("Chapter 2 reviewed context exemption survived a line mutation")

    safe_explanations = (
        "第三者の本番APIへ接続しない",
        "Tokenを取得しない",
        "個人情報の収集リスクを分析する",
        "keyloggerを作ることを禁止する",
        "DoSを実行しない",
    )
    safe_explanation_anchor = (
        "- `Proceed with conditions`では、Condition、Owner、期限、再確認方法を必須とする。"
    )
    for safe_text in safe_explanations:
        mutated_template = replace_once(
            template,
            safe_explanation_anchor,
            f"{safe_explanation_anchor}\n- {safe_text}",
            "Chapter 2 explicit prohibition regression",
        )
        mutated_documents = dict(documents)
        mutated_documents["templates/authorization-checklist.md"] = mutated_template
        findings, _ = chapter02_policy_findings(mutated_documents)
        action_findings = [
            finding
            for finding in findings
            if finding.category != "network.host_or_address"
        ]
        if action_findings:
            error(
                "Chapter 2 Policy adapter rejected a legal/safety explanation or "
                f"explicit prohibition {safe_text!r}: "
                f"{[format_policy_finding(item) for item in action_findings]!r}"
            )

    host_anchor = "| In-scope target identifiers |  |"
    unsafe_hosts = (
        ("https://lab.localhost/", "technically reserved but disallowed by the synthetic publication policy"),
        ("lab.localhost", "technically reserved but disallowed by the synthetic publication policy"),
        ("8.8.8.8", "non-documentation IP literal is disallowed"),
        ("https://example.com/runbook", "non-approved host suffix"),
    )
    for host, required_reason in unsafe_hosts:
        mutated_template = replace_once(
            template,
            host_anchor,
            f"| In-scope target identifiers | {host} |",
            f"Chapter 2 unsafe host regression {host}",
        )
        mutated_documents = dict(documents)
        mutated_documents["templates/authorization-checklist.md"] = mutated_template
        findings, _ = chapter02_policy_findings(mutated_documents)
        host_findings = [
            finding for finding in findings if finding.category == "network.host_or_address"
        ]
        if not any(required_reason in finding.reason for finding in host_findings):
            error(
                f"Chapter 2 Policy adapter accepted unsafe host {host!r} or emitted "
                f"the wrong diagnostic: {[item.reason for item in host_findings]!r}"
            )
        if host.endswith(".localhost") or ".localhost/" in host:
            if any("non-reserved" in finding.reason for finding in host_findings):
                error(
                    "Chapter 2 Policy adapter misclassified reserved .localhost as "
                    "non-reserved"
                )

    localhost_case = replace_once(
        example,
        "`tenant-auth-lab-01.test`、`billing-bridge.example`の合成App registration、設定Export",
        "`tenant-auth-lab-01.test`、`lab.localhost`の合成App registration、設定Export",
        "Chapter 2 Case .localhost regression",
    )
    localhost_case_documents = dict(documents)
    localhost_case_documents["cases/ch02-authorization-decision-example.md"] = (
        localhost_case
    )
    localhost_case_findings, _ = chapter02_policy_findings(localhost_case_documents)
    localhost_host_findings = [
        finding
        for finding in localhost_case_findings
        if finding.category == "network.host_or_address"
    ]
    if not any(
        "technically reserved but disallowed by the synthetic publication policy"
        in finding.reason
        for finding in localhost_host_findings
    ):
        error("Chapter 2 Case accepted .localhost through its former suffix allowance")
    if any("non-reserved" in finding.reason for finding in localhost_host_findings):
        error("Chapter 2 Case .localhost regression used the obsolete non-reserved diagnostic")

    safe_hosts = (
        "lab.example",
        "https://lab.test/runbook",
        "node.invalid",
        "192.0.2.10",
        "198.51.100.10",
        "203.0.113.10",
        "https://[2001:db8::10]/fixture",
    )
    for host in safe_hosts:
        mutated_template = replace_once(
            template,
            host_anchor,
            f"| In-scope target identifiers | {host} |",
            f"Chapter 2 approved host regression {host}",
        )
        mutated_documents = dict(documents)
        mutated_documents["templates/authorization-checklist.md"] = mutated_template
        findings, _ = chapter02_policy_findings(mutated_documents)
        host_findings = [
            finding for finding in findings if finding.category == "network.host_or_address"
        ]
        if host_findings:
            error(
                f"Chapter 2 Policy adapter rejected approved host/address {host!r}: "
                f"{[format_policy_finding(item) for item in host_findings]!r}"
            )

    chapter_fields, selection_errors = chapter02_reader_visible_policy_fields(
        "manuscript/02-law-ethics-authorization.md",
        chapter,
    )
    if selection_errors:
        for message in selection_errors:
            error(message)
    delegated_urls = (
        "https://itdojp.github.io/pentest-learning-book/",
        "https://itdojp.github.io/practical-auth-book/",
        "https://itdojp.github.io/it-infra-security-guide-book/",
    )
    selected_chapter_text = "\n".join(value for _, value in chapter_fields)
    for delegated_url in delegated_urls:
        if delegated_url in selected_chapter_text:
            error(
                "Chapter 2 Policy adapter incorrectly included a public DELEGATE "
                f"destination in the synthetic host surface: {delegated_url}"
            )


def main() -> int:
    required_files = (
        "manuscript/02-law-ethics-authorization.md",
        "templates/authorization-checklist.md",
        "cases/ch02-authorization-decision-example.md",
        "scripts/check_chapter02_contract.py",
        "site-pages.json",
        "artifact-index.md",
        "figure-index.md",
        "glossary.md",
        "cases/index.md",
        "index.md",
        "book-config.json",
        "references/sources.json",
        "references/reference-baseline.md",
        "references/ch02-source-review-2026-08-05.md",
        "CONTENT_SAFETY_POLICY_MIGRATION.md",
        "package.json",
    )
    for relative in required_files:
        if not (ROOT / relative).is_file():
            error(f"missing required file: {relative}")

    if CONTENT_SAFETY_POLICY_VERSION != EXPECTED_CONTENT_SAFETY_POLICY_VERSION:
        error(
            "scripts/check_chapter02_contract.py: Content Safety Policy version "
            f"{CONTENT_SAFETY_POLICY_VERSION!r} != strict adapter pin "
            f"{EXPECTED_CONTENT_SAFETY_POLICY_VERSION!r}"
        )

    config = load_json("book-config.json")
    chapters = config.get("structure", {}).get("chapters", [])
    chapter_config = next(
        (
            item
            for item in chapters
            if isinstance(item, dict)
            and item.get("id") == "ch02-law-ethics-authorization"
        ),
        None,
    )
    expected_objectives = [
        "許可とスコープを文書化できる",
        "停止条件を定義できる",
        "責任ある開示の流れを説明できる",
    ]
    if chapter_config is None:
        error("book-config.json: missing ch02-law-ethics-authorization")
    elif chapter_config.get("objectives") != expected_objectives:
        error("book-config.json: chapter 2 learning objectives changed unexpectedly")

    chapter_path = "manuscript/02-law-ethics-authorization.md"
    chapter = read_text(chapter_path)
    require_tokens(
        chapter_path,
        chapter,
        (
            "## この章の位置付け",
            "## 学習目標",
            "## 前提知識",
            "## 導入ケース",
            "Authority Gate",
            "Scope Gate",
            "Safety Gate",
            "Disclosure Gate",
            "F-02-01",
            "T-02-01",
            "書面による許可",
            "Data、Secret、証拠の取扱い",
            "委託、再委託、Cloud / SaaS",
            "脆弱性を発見したとき",
            "Stop condition",
            "Cleanup",
            "## 7. 四つの視点",
            "## 8. Handoff Contract",
            "## 9. 安全な演習",
            "ART-13 Authorization Checklist",
            "## 11. 評価基準",
            "## 12. よくある誤解",
            "## 章のまとめ",
            "## 次に学ぶこと",
            "## 参考文献・Source Note ID",
            "SRC-JP-LAW-001",
            "SRC-IPA-VDP-001",
            "Proceed with conditions",
            "Do not proceed",
            "Escalate",
            "## 本章の責任境界",
            "### OWN",
            "### BRIDGE",
            "### DELEGATE",
            "本書は、実務上のAuthorization Gateと後続工程へのHandoffに責任を持つ。",
            "本章は法的助言を提供せず、個別事案の法的判断と法令解釈は専門家へ委譲する。",
            "委譲先へのリンクを読まなくても、第2章の論旨と運用判断は単独で成立する。",
            "個別事案の法的助言と法令解釈は、適格な法務・契約専門家へ委譲する",
            "第8章の安全なLabとEvidence取扱い",
            "第9章のRules of Engagement",
            "第10章のReconnaissance / OSINT境界",
            "第15章のFinding、Remediation、Retest、Responsible Disclosure",
            "第19章のIncidentとPersonal Data対応",
            (
                "詳細な攻撃技法と脆弱性の悪用は、許可済み評価の専門的な方法、"
                "成果物、安全境界を詳述する[実務で使えるペネトレーションテスト大全]"
                "(https://itdojp.github.io/pentest-learning-book/)へ委譲する"
            ),
            (
                "認証・認可Protocol内部と安全な実装は、OAuth、OIDC、SAML等の設計と"
                "実装を詳述する[実践 認証認可システム設計]"
                "(https://itdojp.github.io/practical-auth-book/)へ委譲する"
            ),
            (
                "Infrastructure Hardeningと防御実装は、Network、OS、Cloud、Containerの"
                "Security実装を詳述する[インフラエンジニアのための情報セキュリティ実装ガイド]"
                "(https://itdojp.github.io/it-infra-security-guide-book/)へ委譲する"
            ),
        ),
    )
    if re.search(r"https://github\.com/[^\s)]+/blob/main(?:/|\b)", chapter):
        error(
            f"{chapter_path}: mutable GitHub blob/main URL must not be used as a "
            "delegated publication target"
        )
    for forbidden in (
        "善意の研究であれば明示的な許可は不要である。",
        "管理者権限があれば業務上の承認も不要である。",
        "脆弱性を発見したら影響を最大まで実証する。",
        "届出後は関係者との調整を待たず公開する。",
    ):
        if forbidden in chapter:
            error(f"{chapter_path}: unsafe or unsupported assertion {forbidden!r}")

    body, references = chapter_body_and_references(chapter)
    used_ids = source_ids(body)
    listed_ids = source_ids(references)
    expected_source_ids = {"SRC-JP-LAW-001", "SRC-IPA-VDP-001"}
    if used_ids != expected_source_ids:
        error(
            f"{chapter_path}: body source IDs {sorted(used_ids)} != expected {sorted(expected_source_ids)}"
        )
    if listed_ids != used_ids:
        error(
            f"{chapter_path}: chapter-end source IDs {sorted(listed_ids)} != body {sorted(used_ids)}"
        )

    template_path = "templates/authorization-checklist.md"
    template = read_text(template_path)
    require_tokens(
        template_path,
        template,
        (
            "Artifact ID | `ART-13`",
            "Authorization Record ID",
            "Parent Case ID",
            "Relation | `refines` / `supersedes` / `independent`",
            "Decision Requirement ID",
            "Available decisions | Proceed / Proceed with conditions / Do not proceed / Escalate",
            "## 2. Authority Gate",
            "## 3. Scope Gate",
            "## 4. Safety Gate",
            "## 5. Disclosure Gate",
            "Authority evidence",
            "Legal, Contractual, and Policy Questions",
            "Conditions",
            "Decision Record",
            "RoE Handoff",
            "Reassessment",
            "Traceability Check",
            "Technical correctness",
            "Safety / authorization",
            "Legal / contractual source quality",
            "Evidence / traceability",
            "Decision usefulness",
        ),
    )

    example_path = "cases/ch02-authorization-decision-example.md"
    example = read_text(example_path)
    require_tokens(
        example_path,
        example,
        (
            "ART-13",
            "AUTH-CASE-2026-001",
            "CASE-2026-001",
            "| Relation | `refines` |",
            "DR-AUTH-2026-001",
            "EVD-AUTH-2026-001",
            "COND-AUTH-2026-001",
            "DEC-AUTH-2026-001",
            "HO-AUTH-2026-001",
            "REA-AUTH-2026-001",
            "Proceed with conditions",
            "tenant-auth-lab-01.test",
            "billing-bridge.example",
            "Production credentialを操作しない",
            "外部Networkをdefault denyにする",
            "想定外脆弱性発見時は直ちに停止する",
            "この表は合成Case内の記入例であり、実際の章Gateまたは法的承認の証跡ではない。",
            "SYNTH-REV-AUTH-TECH-001",
            "SYNTH-REV-AUTH-SAFE-001",
            "SYNTH-REV-AUTH-LAW-001",
            "SYNTH-REV-AUTH-EVD-001",
            "SYNTH-REV-AUTH-DEC-001",
        ),
    )
    verify_policy_adapter_regressions(chapter, template, example)

    secret_patterns = (
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
        re.compile(r"(?i)(?:password|api[_-]?key|secret|token)\s*[:=]\s*[A-Za-z0-9+/=_-]{16,}"),
    )
    for pattern in secret_patterns:
        if pattern.search(example):
            error(f"{example_path}: possible real credential or secret pattern detected")

    raw_registry = load_json("site-pages.json")
    try:
        registry = parse_registry_data(raw_registry)
    except SitePageRegistryError as exc:
        error(f"site-pages.json: invalid registry: {exc}")
        registry = {}
    for message in chapter02_page_contract_errors(registry, "site-pages.json"):
        error(message)

    pages = raw_registry.get("pages", [])
    chapter_page = next(
        (
            item
            for item in pages
            if isinstance(item, dict)
            and item.get("source") == "manuscript/02-law-ethics-authorization.md"
        ),
        None,
    ) if isinstance(pages, list) else None
    if chapter_page is None:
        error("site-pages.json: missing Chapter 2 manuscript page for negative regressions")
    else:
        negative_registries: list[tuple[str, dict]] = []

        mutation = deepcopy(raw_registry)
        mutation["schemaVersion"] = "0.0.0"
        negative_registries.append(("schemaVersion drift", mutation))

        mutation = deepcopy(raw_registry)
        next(
            item
            for item in mutation["pages"]
            if item.get("source") == "manuscript/02-law-ethics-authorization.md"
        )["section"] = "additional"
        negative_registries.append(("section drift", mutation))

        mutation = deepcopy(raw_registry)
        next(
            item
            for item in mutation["pages"]
            if item.get("source") == "manuscript/02-law-ethics-authorization.md"
        )["order"] = 46
        negative_registries.append(("order drift", mutation))

        mutation = deepcopy(raw_registry)
        duplicated_page = next(
            item
            for item in mutation["pages"]
            if item.get("source") == "manuscript/02-law-ethics-authorization.md"
        )
        mutation["pages"].append(deepcopy(duplicated_page))
        negative_registries.append(("duplicate page", mutation))

        mutation = deepcopy(raw_registry)
        next(
            item
            for item in mutation["pages"]
            if item.get("source") == "manuscript/02-law-ethics-authorization.md"
        )["unexpectedKey"] = True
        negative_registries.append(("unknown page key", mutation))

        for mutation_name, mutated_registry in negative_registries:
            if not registry_mutation_is_rejected(
                mutated_registry,
                f"site-pages.json negative regression ({mutation_name})",
            ):
                error(
                    "site-pages.json: negative registry mutation was accepted: "
                    f"{mutation_name}"
                )

    artifact_index = read_text("artifact-index.md")
    require_tokens(
        "artifact-index.md",
        artifact_index,
        (
            "| ART-13 | Authorization Checklist | 2, 9 | `templates/authorization-checklist.md` |",
            "cases/ch02-authorization-decision-example.md",
        ),
    )

    figure_index = read_text("figure-index.md")
    require_tokens(
        "figure-index.md",
        figure_index,
        (
            "F-02-01",
            "Authorization Decision Gate",
            "T-02-01",
            "許容性判断の層",
        ),
    )

    glossary = read_text("glossary.md")
    require_tokens(
        "glossary.md",
        glossary,
        (
            "| Authority |",
            "| Authorization |",
            "| Data Owner |",
            "| Responsible Disclosure |",
            "| Rules of Engagement |",
            "| Scope |",
        ),
    )

    cases_index = read_text("cases/index.md")
    index = read_text("index.md")
    require_tokens(
        "cases/index.md",
        cases_index,
        (
            "ch02-authorization-decision-example.md",
            "Authorization Checklist",
        ),
    )
    require_tokens(
        "index.md",
        index,
        (
            "manuscript/02-law-ethics-authorization.md",
            "templates/authorization-checklist.md",
            "cases/ch02-authorization-decision-example.md",
        ),
    )

    sources = load_json("references/sources.json")
    if sources.get("checkedAt") != "2026-07-25":
        error(
            "references/sources.json: registry-level checkedAt must remain 2026-07-25; "
            "only the two Chapter 2 source entries were re-audited"
        )
    source_entries = {
        item.get("id"): item
        for item in sources.get("sources", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    for source_id in sorted(expected_source_ids):
        entry = source_entries.get(source_id)
        if entry is None:
            error(f"references/sources.json: missing {source_id}")
            continue
        chapters = entry.get("chapters", [])
        if 2 not in chapters:
            error(f"references/sources.json: {source_id} does not map chapter 2")

    expected_source_metadata = {
        "SRC-JP-LAW-001": {
            "version": "current display effective 2025-06-01",
            "checkedAt": "2026-08-05",
            "nextReviewAt": "2026-11-05",
            "noteMarkers": (
                "e-Gov current display was rechecked on 2026-08-05",
                "law effective from 2025-06-01",
                "confirm current text before publication",
                "book is not legal advice",
            ),
        },
        "SRC-IPA-VDP-001": {
            "version": "2024 edition",
            "checkedAt": "2026-08-05",
            "nextReviewAt": "2026-11-05",
            "noteMarkers": (
                "official IPA page and linked 2024 edition guideline were rechecked on 2026-08-05",
                "official page showed last update 2026-04-06",
                "current page and linked guideline must be rechecked at publication time",
            ),
        },
    }
    for source_id, expected in expected_source_metadata.items():
        entry = source_entries.get(source_id)
        if entry is None:
            continue
        for field in ("version", "checkedAt", "nextReviewAt"):
            if entry.get(field) != expected[field]:
                error(
                    f"references/sources.json: {source_id}.{field} "
                    f"must be {expected[field]!r}"
                )
        notes = entry.get("notes")
        if not isinstance(notes, str):
            error(f"references/sources.json: {source_id}.notes must be a string")
            continue
        for marker in expected["noteMarkers"]:
            if marker not in notes:
                error(
                    f"references/sources.json: {source_id}.notes missing marker {marker!r}"
                )

    audit_note_path = "references/ch02-source-review-2026-08-05.md"
    audit_note = read_text(audit_note_path)
    require_tokens(
        audit_note_path,
        audit_note,
        (
            "SRC-JP-LAW-001",
            "2025-06-01施行表示",
            "SRC-IPA-VDP-001",
            "2024年版",
            "2026-04-06",
            "Checked at | 2026-08-05",
        ),
    )

    baseline_path = "references/reference-baseline.md"
    baseline = read_text(baseline_path)
    if baseline != render_reference_baseline():
        error(f"{baseline_path}: out of sync with references/sources.json")

    migration_note_path = "CONTENT_SAFETY_POLICY_MIGRATION.md"
    migration_note = read_text(migration_note_path)
    require_tokens(
        migration_note_path,
        migration_note,
        (
            "## Chapter 2 adapter status (Issue #65)",
            "Policy `1.2.0`へ厳密pin",
            "`.localhost`はtechnically reservedだがRepository Policyでdisallowed",
            "Chapter 2固有のAuthority / Scope / Source / Traceability契約は移行しない",
        ),
    )

    package = load_json("package.json")
    scripts = package.get("scripts", {})
    if scripts.get("check:chapter02") != "python3 scripts/check_chapter02_contract.py":
        error("package.json: missing check:chapter02 script")
    if "check:chapter02" not in scripts.get("test", ""):
        error("package.json: npm test does not include check:chapter02")

    for message in ERRORS:
        print(f"ERROR: {message}")
    if ERRORS:
        return 1

    print(
        "chapter 2 contract passed: manuscript, authorization artifact, synthetic case, "
        "source mapping, publication registry, Content Safety Policy 1.2.0 adapter, "
        "and handoff traceability"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
