#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import sys
import unicodedata
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
        "## 章のまとめ",
        "## 次に学ぶこと",
        "## 参考文献・Source Note ID",
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
        "manuscript/02-law-ethics-authorization.md",
        "templates/authorization-checklist.md",
        "cases/ch02-authorization-decision-example.md",
    }
)
CHAPTER02_POLICY_TERMINAL_BOUNDARIES = {
    "manuscript/02-law-ethics-authorization.md": None,
    "templates/authorization-checklist.md": None,
    "cases/ch02-authorization-decision-example.md": None,
}

# Kramdown/Jekyll can publish structures whose rendered relationships differ from
# the source blocks delegated to Policy 1.2.0.  The adapter does not maintain a
# second HTML/Liquid renderer, so it rejects these constructs.  ``br`` is the sole
# raw HTML exception and is projected to whitespace below.
CHAPTER02_RAW_HTML_TAG = re.compile(
    r"</?(?P<tag>[A-Z][A-Z0-9:-]*)\b[^>]*>",
    re.IGNORECASE,
)
CHAPTER02_SAFE_BR_TAG = re.compile(r"<br\s*/?>", re.IGNORECASE)
CHAPTER02_HTML_COMMENT_DELIMITER = re.compile(r"<!--")
CHAPTER02_MARKDOWN_AUTOLINK = re.compile(
    r"<(?:(?:https?://|mailto:)[^<>\x00-\x20]*|"
    r"[A-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Z0-9.-]+\.[A-Z]{2,})>",
    re.IGNORECASE,
)
CHAPTER02_LIQUID_CONSTRUCT = re.compile(r"{{|{%")
CHAPTER02_DEFINITION_ITEM = re.compile(r"(?m)^[ \t]*:[ \t]+\S")
CHAPTER02_BLOCKQUOTE = re.compile(r"^ {0,3}>", re.MULTILINE)
CHAPTER02_KRAMDOWN_IAL = re.compile(r"(?<!\\)\{:")
CHAPTER02_FOOTNOTE = re.compile(r"\[\^[^\]\r\n]+\]")
CHAPTER02_ABBREVIATION_DEFINITION = re.compile(
    r"^ {0,3}\*\[[^\]\r\n]+\]:",
    re.MULTILINE,
)
CHAPTER02_KRAMDOWN_MATH = re.compile(r"(?<!\\)\$\$")
CHAPTER02_INVALID_BACKTICK_FENCE = re.compile(
    r"^ {0,3}`{3,}[^`\r\n]*`",
    re.MULTILINE,
)
CHAPTER02_UNDERSCORE_EMPHASIS = re.compile(
    r"(?<![\w\\])(?P<delimiter>_{1,3})(?=\S)"
    r"(?P<body>[^\r\n]*?\S)(?P=delimiter)(?!\w)"
)
CHAPTER02_REFERENCE_LINK = re.compile(
    r"\[[^\]\r\n]+\]\[[^\]\r\n]*\]|"
    r"^ {0,3}\[[^\]\r\n]+\]:",
    re.MULTILINE,
)
CHAPTER02_TITLED_INLINE_LINK = re.compile(
    r"(?<!\\)\]\("
    r"(?:<[^>\r\n]*>|(?:\\.|[^\s])*)"
    r"[ \t\r\n]+"
    r'(?:"(?:\\.|[^"\\\r\n])*"|'
    r"'(?:\\.|[^'\\\r\n])*'|"
    r"\((?:\\.|[^()\\\r\n])*\))"
    r"[ \t\r\n]*\)"
)
CHAPTER02_SPECIAL_URL = re.compile(
    r"(?:(?:https?:)?[\\/]{2})[^<>\x00-\x20]+",
    re.IGNORECASE,
)
CHAPTER02_INLINE_CODE_DELIMITER = re.compile(r"(?<!`)(`+)(?!`)")
CHAPTER02_ANGLE_TEXT = re.compile(r"<(?P<body>[^<>\r\n]+)>")
CHAPTER02_EXECUTABLE_URL_PREFIXES = (
    "javascript:",
    "vbscript:",
    "data:text/html",
    "data:application/xhtml+xml",
    "data:image/svg+xml",
)

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

# Policy fields normally preserve Markdown block boundaries.  Heading text also
# scopes the body blocks below it, so the adapter scans each body once more with
# its active heading hierarchy.  These three exact composites are reviewed
# non-operative prose that the additional association would otherwise classify
# without their question, list-continuation, or prohibition semantics.
CHAPTER02_REVIEWED_HEADING_ACTION_CONTEXT = {
    "manuscript/02-law-ethics-authorization.md": frozenset(
        {
            (
                "# 第2章　法、倫理、許可、責任ある開示 ## 導入ケース "
                "- SaaS Tenantと外部APIのどこまでがA社の管理範囲か"
            ),
            (
                "# 第2章　法、倫理、許可、責任ある開示 "
                "## 4. Data、Secret、証拠の取扱い ### 4.2 Secret "
                "を記録し、値自体はSecret管理経路で扱う。"
            ),
        }
    ),
    "templates/authorization-checklist.md": frozenset(
        {
            (
                "# Authorization Checklist ## 使用条件 - 実Credential、Token、"
                "Cookie、Personal Data、Secret valueを記載しない。"
            ),
        }
    ),
    "cases/ch02-authorization-decision-example.md": frozenset(),
}

# Issue #67 tracks the shared core's Japanese-particle host-token boundary.  Until
# that independent Policy change lands, keep only these exact approved-host lines
# frozen.  A changed line is scanned normally, so .localhost or a real host cannot
# inherit this exemption.
CHAPTER02_REVIEWED_HOST_CONTEXT = {
    "manuscript/02-law-ethics-authorization.md": frozenset(
        {
            "- 詳細な攻撃技法と脆弱性の悪用は、許可済み評価の専門的な方法、成果物、安全境界を詳述する[実務で使えるペネトレーションテスト大全](https://itdojp.github.io/pentest-learning-book/)へ委譲する",
            "- 認証・認可Protocol内部と安全な実装は、OAuth、OIDC、SAML等の設計と実装を詳述する[実践 認証認可システム設計](https://itdojp.github.io/practical-auth-book/)へ委譲する",
            "- Infrastructure Hardeningと防御実装は、Network、OS、Cloud、ContainerのSecurity実装を詳述する[インフラエンジニアのための情報セキュリティ実装ガイド](https://itdojp.github.io/it-infra-security-guide-book/)へ委譲する",
            "- 対象: `billing-bridge.example`の合成Tenant",
        }
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
        or re.match(r"(?:[-+*]|\d+[.)])\s+", stripped)
    )


def _markdown_table_row_indexes(
    lines: list[str],
    *,
    start: int,
    end: int,
) -> set[int]:
    """Return rows belonging to a table confirmed by its delimiter row."""

    indexes: set[int] = set()
    for delimiter_index in range(max(start + 1, 1), end):
        if not _is_markdown_table_delimiter(lines[delimiter_index]):
            continue
        header_index = delimiter_index - 1
        if header_index < start or not _is_markdown_table_row(lines[header_index]):
            continue
        indexes.update({header_index, delimiter_index})
        body_index = delimiter_index + 1
        while body_index < end and _is_markdown_table_row(lines[body_index]):
            indexes.add(body_index)
            body_index += 1
    return indexes


def _project_in_field_whitespace(value: str) -> str:
    """Project rendered in-field whitespace to Policy-safe spaces."""

    value = re.sub(r"[\t\r\n\f\v]+", " ", html.unescape(value))
    return CHAPTER02_SAFE_BR_TAG.sub(" ", value)


def _join_markdown_policy_lines(
    pending: list[tuple[int, str]],
    *,
    field_kind: str | None,
) -> str:
    """Join source lines using their Markdown reader-visible boundaries."""

    if field_kind == "fenced code":
        return " ".join(value.strip() for _, value in pending)

    visible_text = ""
    for offset, (_, source_line) in enumerate(pending):
        projected_line = source_line.strip()
        separator = " "
        if len(source_line) - len(source_line.rstrip(" ")) >= 2:
            # Markdown's two-space hard break does not insert a text token
            # between adjacent reader-visible characters.
            separator = ""
        elif projected_line.endswith("\\"):
            # The terminal backslash is the alternative Markdown hard-break
            # marker and is not part of the rendered text.
            projected_line = projected_line[:-1]
            separator = ""
        visible_text += projected_line
        if offset + 1 < len(pending):
            visible_text += separator
    return visible_text


def _opening_fence_marker(line: str) -> str | None:
    match = re.fullmatch(
        r"[ ]{0,3}(?P<marker>`{3,}|~{3,})(?P<info>.*)",
        line,
    )
    if match is None:
        return None
    marker = match.group("marker")
    if marker.startswith("`") and "`" in match.group("info"):
        return None
    return marker


def _is_closing_fence(line: str, marker: str) -> bool:
    match = re.fullmatch(r"[ ]{0,3}([`~]+)[ \t]*", line)
    return bool(
        match is not None
        and match.group(1)[0] == marker[0]
        and len(match.group(1)) >= len(marker)
    )


def _literal_indented_code_line_indexes(lines: list[str]) -> set[int]:
    """Select finite root/list indented code using source-column thresholds."""

    indexes: set[int] = set()
    list_item = re.compile(
        r"^(?P<prefix>[ \t]*(?:[-+*]|\d+[.)])[ \t]+)"
    )
    index = 0
    while index < len(lines):
        line = lines[index]
        if not re.match(r"(?: {4}|\t)", line):
            index += 1
            continue
        # Pinned Kramdown does not let an indented code block interrupt an
        # active paragraph.  Require a document/block boundary for its opener.
        if index > 0 and lines[index - 1].strip():
            index += 1
            continue

        owner_prefixes: list[str] = []
        cursor = index - 1
        while cursor >= 0:
            candidate = lines[cursor]
            if not candidate.strip():
                cursor -= 1
                continue
            owner = list_item.match(candidate)
            if owner is not None:
                owner_prefixes.append(owner.group("prefix"))
                cursor -= 1
                continue
            if candidate.startswith((" ", "\t")):
                cursor -= 1
                continue
            break

        opening_indent = re.match(r"^[ \t]*", line).group(0)
        opening_column = _markdown_indent_width(opening_indent)
        owner_prefix = next(
            (
                prefix
                for prefix in owner_prefixes
                if opening_column >= len(prefix.expandtabs(4))
            ),
            None,
        )
        required_column = 4
        if owner_prefix is not None:
            # Ambiguous tabbed list ownership fails closed as rendered list
            # content rather than being hidden from render-time guards.
            if "\t" in owner_prefix or "\t" in opening_indent:
                index += 1
                continue
            content_column = len(owner_prefix.expandtabs(4))
            if opening_column < content_column:
                required_column = 4
            else:
                required_column = content_column + 4
            if opening_column < required_column:
                index += 1
                continue

        cursor = index
        while cursor < len(lines):
            candidate = lines[cursor]
            if not candidate.strip():
                cursor += 1
                continue
            indentation = re.match(r"^[ \t]*", candidate).group(0)
            if "\t" in indentation and owner_prefix is not None:
                break
            if _markdown_indent_width(indentation) < required_column:
                break
            indexes.add(cursor)
            cursor += 1
        index = max(index + 1, cursor)
    return indexes


def _markdown_character_is_escaped(value: str, position: int) -> bool:
    backslashes = 0
    cursor = position - 1
    while cursor >= 0 and value[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


def _inline_code_spans(value: str) -> list[tuple[int, int, str]]:
    """Return finite code spans with unescaped, equal-length delimiters."""

    spans: list[tuple[int, int, str]] = []
    search_start = 0
    while True:
        opening = CHAPTER02_INLINE_CODE_DELIMITER.search(value, search_start)
        if opening is None:
            break
        if _markdown_character_is_escaped(value, opening.start()):
            search_start = opening.end()
            continue
        marker = opening.group(1)
        closing_start = opening.end()
        closing = None
        while True:
            candidate = CHAPTER02_INLINE_CODE_DELIMITER.search(
                value,
                closing_start,
            )
            if candidate is None:
                break
            if candidate.group(1) == marker:
                closing = candidate
                break
            closing_start = candidate.end()
        if closing is None:
            search_start = opening.end()
            continue
        spans.append(
            (
                opening.start(),
                closing.end(),
                value[opening.end() : closing.start()],
            )
        )
        search_start = closing.end()
    return spans


def _mask_markdown_literal_code(text: str) -> str:
    """Mask code syntax for render guards while preserving line offsets."""

    masked = list(text)

    def mask(start: int, end: int) -> None:
        for position in range(start, end):
            if masked[position] not in "\r\n":
                masked[position] = " "

    source_lines = text.splitlines()
    indented_code_indexes = _literal_indented_code_line_indexes(source_lines)
    offset = 0
    fence_marker: str | None = None
    for line_index, line in enumerate(text.splitlines(keepends=True)):
        source_line = line.rstrip("\r\n")
        line_end = offset + len(line)
        if fence_marker is not None:
            mask(offset, line_end)
            if _is_closing_fence(source_line, fence_marker):
                fence_marker = None
        else:
            opening_fence = _opening_fence_marker(source_line)
            if opening_fence is not None:
                fence_marker = opening_fence
                mask(offset, line_end)
            elif line_index in indented_code_indexes:
                mask(offset, line_end)
        offset = line_end

    block_masked = "".join(masked)
    for start, end, _ in _inline_code_spans(block_masked):
        mask(start, end)
    return "".join(masked)


def _project_literal_code_for_policy(value: str) -> str:
    """Preserve literal code text that Policy would otherwise treat as HTML."""

    projected = re.sub(r"[\t\r\n\f\v]+", " ", value)
    projected = projected.replace("<!--", "").replace("-->", "")
    return projected.replace("<", " ").replace(">", " ")


def _literal_code_policy_fields(
    relative: str,
    text: str,
) -> list[tuple[str, str]]:
    """Select reader-visible fenced, indented, and inline code payloads."""

    lines = text.splitlines()
    indented_indexes = _literal_indented_code_line_indexes(lines)
    fields: list[tuple[str, str]] = []
    fence_marker: str | None = None
    fence_start = 0
    fence_payload: list[str] = []
    for index, line in enumerate(lines):
        if fence_marker is not None:
            if _is_closing_fence(line, fence_marker):
                projected = _project_literal_code_for_policy(
                    "\n".join(fence_payload)
                )
                if projected.strip():
                    fields.append(
                        (
                            f"{relative} literal fenced code lines "
                            f"{fence_start + 1}-{index + 1}",
                            projected,
                        )
                    )
                fence_marker = None
                fence_payload = []
            else:
                fence_payload.append(line)
            continue
        opening_fence = _opening_fence_marker(line)
        if opening_fence is not None:
            fence_marker = opening_fence
            fence_start = index
            fence_payload = []
            continue
        if index in indented_indexes:
            projected = _project_literal_code_for_policy(line.strip())
            if projected.strip():
                fields.append(
                    (f"{relative} literal indented code line {index + 1}", projected)
                )
            continue
        for occurrence, (_, _, body) in enumerate(
            _inline_code_spans(line),
            start=1,
        ):
            projected = _project_literal_code_for_policy(body)
            if projected.strip():
                fields.append(
                    (
                        f"{relative} literal inline code line {index + 1} "
                        f"occurrence {occurrence}",
                        projected,
                    )
                )
    if fence_marker is not None and fence_payload:
        projected = _project_literal_code_for_policy("\n".join(fence_payload))
        if projected.strip():
            fields.append(
                (
                    f"{relative} literal unclosed fenced code from line "
                    f"{fence_start + 1}",
                    projected,
                )
            )
    return fields


def _bare_angle_policy_fields(
    relative: str,
    render_guard_source: str,
) -> list[tuple[str, str]]:
    """Select non-tag angle bodies that pinned Kramdown renders literally."""

    fields: list[tuple[str, str]] = []
    for occurrence, match in enumerate(
        CHAPTER02_ANGLE_TEXT.finditer(render_guard_source),
        start=1,
    ):
        token = match.group(0)
        if (
            CHAPTER02_RAW_HTML_TAG.fullmatch(token) is not None
            or CHAPTER02_SAFE_BR_TAG.fullmatch(token) is not None
            or CHAPTER02_MARKDOWN_AUTOLINK.fullmatch(token) is not None
            or token.startswith("<!--")
        ):
            continue
        visible = unicodedata.normalize("NFKC", html.unescape(match.group("body")))
        if visible.strip():
            line = render_guard_source.count("\n", 0, match.start()) + 1
            fields.append(
                (
                    f"{relative} bare-angle text line {line} occurrence {occurrence}",
                    visible,
                )
            )
    return fields


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
    fence_marker: str | None = None
    frontmatter_delimiters: set[int] = set()
    if start == 0 and lines and lines[0].strip() == "---":
        frontmatter_delimiters.add(0)
        for index in range(1, len(lines)):
            if lines[index].strip() in {"---", "..."}:
                frontmatter_delimiters.add(index)
                break
    table_row_indexes = _markdown_table_row_indexes(lines, start=start, end=end)

    def flush(
        *,
        heading_level: int | None = None,
        field_kind: str | None = None,
    ) -> None:
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
        visible_text = _join_markdown_policy_lines(
            pending,
            field_kind=field_kind,
        )
        # An HTML ``br`` is a reader-visible hard break inside the same field.
        # Shared Policy treats block tags as clause boundaries, so project only
        # this in-field line-break tag to whitespace before delegating.  This
        # prevents an object/action pair from being split inside one table cell.
        visible_text = _project_in_field_whitespace(visible_text)
        if heading_level is not None:
            visible_text = f"{'#' * heading_level} {visible_text}"
        kind_label = f" {field_kind}" if field_kind is not None else ""
        blocks.append((f"{location_prefix}{kind_label} {line_label}", visible_text))
        pending.clear()

    for index in range(start, end):
        value = lines[index]
        if fence_marker is not None:
            if _is_closing_fence(value, fence_marker):
                flush(field_kind="fenced code")
                fence_marker = None
            else:
                # Blank source lines remain inside the same rendered code block.
                pending.append((index, value))
            continue
        opening_fence = _opening_fence_marker(value)
        if opening_fence is not None:
            flush()
            fence_marker = opening_fence
            continue
        if not value.strip():
            flush()
            continue
        setext_match = re.fullmatch(r"\s*(=+|-+)\s*", value)
        if (
            setext_match is not None
            and index not in frontmatter_delimiters
            and pending
            and not _is_markdown_policy_block_start(pending[0][1])
        ):
            heading_level = 1 if setext_match.group(1).startswith("=") else 2
            flush(heading_level=heading_level)
            continue
        if index in table_row_indexes and _is_markdown_table_delimiter(value):
            flush()
            continue
        if _is_markdown_policy_block_start(value) or index in table_row_indexes:
            flush()
            pending.append((index, value))
            if value.lstrip().startswith("#") or index in table_row_indexes:
                flush()
            continue
        pending.append((index, value))
    flush(field_kind="fenced code" if fence_marker is not None else None)
    return blocks


def chapter02_reader_visible_policy_fields(
    relative: str,
    text: str,
) -> tuple[list[tuple[str, str]], list[str]]:
    """Select the finite Chapter 2 action/authorization publication surface.

    The adapter owns section and line selection.  Shared Policy 1.2.0 owns
    normalization, protected-action semantics, and host/address classification.
    Reader-visible DELEGATE URLs remain in this surface.  The three canonical
    publication links are exact reviewed host contexts; an edited line returns
    to normal Policy scanning.  The final Source-note section remains inside the
    bounded surface and its relative references also retain the existing Chapter
    2 publication/source contracts.
    """

    expected_headings = CHAPTER02_POLICY_SECTIONS.get(relative)
    if expected_headings is None:
        return [], [f"{relative}: no Chapter 2 Policy section contract"]

    lines = text.splitlines()
    headings: list[tuple[int, int, str]] = []
    frontmatter_delimiters: set[int] = set()
    if lines and lines[0].strip() == "---":
        frontmatter_delimiters.add(0)
        for index in range(1, len(lines)):
            if lines[index].strip() in {"---", "..."}:
                frontmatter_delimiters.add(index)
                break
    fence_marker: str | None = None
    for index, line in enumerate(lines):
        if fence_marker is not None:
            if _is_closing_fence(line, fence_marker):
                fence_marker = None
            continue
        opening_fence = _opening_fence_marker(line)
        if opening_fence is not None:
            fence_marker = opening_fence
            continue
        match = re.fullmatch(r"(#{1,6})\s+(.+?)\s*", line)
        if match:
            headings.append((index, len(match.group(1)), line.rstrip()))
            continue
        setext = re.fullmatch(r" {0,3}(=+|-+)[ \t]*", line)
        if (
            setext is not None
            and index not in frontmatter_delimiters
            and index > 0
            and lines[index - 1].strip()
            and not _is_markdown_policy_block_start(lines[index - 1])
        ):
            level = 1 if setext.group(1).startswith("=") else 2
            title = lines[index - 1].strip()
            headings.append((index - 1, level, f"{'#' * level} {title}"))

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


def _heading_associated_action_fields(
    fields: list[tuple[str, str]],
) -> list[tuple[str, str, str]]:
    """Associate each visible body block with its active ATX heading hierarchy."""

    heading_stack: list[tuple[int, str]] = []
    associated: list[tuple[str, str, str]] = []
    for location, value in fields:
        match = (
            None
            if " fenced code " in location
            else re.match(r"^(#{1,6})\s+", value)
        )
        if match:
            level = len(match.group(1))
            heading_stack = [
                item for item in heading_stack if item[0] < level
            ]
            heading_stack.append((level, value))
            continue
        if not heading_stack:
            continue
        heading_context = " ".join(heading for _, heading in heading_stack)
        composite = f"{heading_context} {value}"
        associated.append((f"{location} heading association", composite, value))
    return associated


_MARKDOWN_LIST_ITEM = re.compile(
    r"^(?P<indent>[ \t]*)(?:[-+*]|\d+[.)])\s+(?P<body>.+?)\s*$"
)


def _markdown_indent_width(line: str) -> int:
    prefix_length = len(line) - len(line.lstrip(" \t"))
    return len(line[:prefix_length].expandtabs(4))


def _nested_list_action_fields(
    relative: str,
    text: str,
) -> list[tuple[str, str, str]]:
    """Associate each nested list item with its visible ancestor items."""

    lines = text.splitlines()
    records: list[tuple[int, int, int, str, str]] = []
    for index, line in enumerate(lines):
        match = _MARKDOWN_LIST_ITEM.match(line)
        if match is None:
            continue
        continuation: list[str] = []
        end = index + 1
        while end < len(lines):
            candidate = lines[end]
            if not candidate.strip() or _is_markdown_policy_block_start(candidate):
                break
            continuation.append(candidate.strip())
            end += 1
        raw_value = _project_in_field_whitespace(
            " ".join([line.strip(), *continuation])
        )
        # List markers are layout, not reader-visible clause punctuation.  Drop
        # them in the association so numbered markers cannot split object/action.
        visible_value = _project_in_field_whitespace(
            " ".join([match.group("body").strip(), *continuation])
        )
        indentation = len(match.group("indent").expandtabs(4))
        records.append((index, end, indentation, visible_value, raw_value))

    stack: list[tuple[int, list[str]]] = []
    associated: list[tuple[str, str, str]] = []

    def associate_with_ancestors(
        context_stack: list[tuple[int, list[str]]],
        *,
        location: str,
        value: str,
        raw_value: str,
    ) -> None:
        for _, ancestor_contexts in context_stack:
            for ancestor_context in ancestor_contexts:
                associated.append(
                    (location, f"{ancestor_context} {value}", raw_value)
                )

    previous_end = 0
    for start, end, indentation, value, raw_value in records:
        gap_lines = lines[previous_end:start]
        first_continuation = next(
            (line for line in gap_lines if line.strip()),
            None,
        )
        if first_continuation is not None:
            continuation_indent = _markdown_indent_width(first_continuation)
            owner_stack = [
                item for item in stack if item[0] < continuation_indent
            ]
            continuation_lines: list[str] = []
            reached_outer_block = False
            if owner_stack:
                for line in gap_lines:
                    if not line.strip():
                        continue
                    if _markdown_indent_width(line) <= owner_stack[-1][0]:
                        reached_outer_block = True
                        break
                    continuation_lines.append(line)
            if owner_stack and continuation_lines:
                continuation_text = _project_in_field_whitespace(
                    " ".join(line.strip() for line in continuation_lines)
                )
                associate_with_ancestors(
                    owner_stack,
                    location=f"{relative} list continuation before line {start + 1}",
                    value=continuation_text,
                    raw_value=continuation_text,
                )
                owner_stack[-1][1].append(continuation_text)
            stack = [] if reached_outer_block else owner_stack
        stack = [item for item in stack if item[0] < indentation]
        if stack:
            associate_with_ancestors(
                stack,
                location=f"{relative} nested list line {start + 1}",
                value=value,
                raw_value=raw_value,
            )
        stack.append((indentation, [value]))
        previous_end = end

    if stack:
        paragraph: list[str] = []

        def flush_terminal_continuation() -> None:
            if not paragraph:
                return
            continuation_text = _project_in_field_whitespace(
                " ".join(line.strip() for line in paragraph)
            )
            associate_with_ancestors(
                stack,
                location=f"{relative} terminal list continuation",
                value=continuation_text,
                raw_value=continuation_text,
            )
            paragraph.clear()

        for line in lines[previous_end:]:
            if not line.strip():
                flush_terminal_continuation()
                continue
            if _markdown_indent_width(line) <= stack[-1][0]:
                break
            paragraph.append(line)
        flush_terminal_continuation()
    return associated


def _is_markdown_table_row(line: str) -> bool:
    stripped = line.strip()
    return bool(stripped and "|" in stripped and not _is_markdown_table_delimiter(line))


def _table_header_action_fields(
    relative: str,
    text: str,
) -> list[tuple[str, str, str]]:
    """Associate each pipe-table body row with its reader-visible header row."""

    lines = text.splitlines()
    associated: list[tuple[str, str, str]] = []
    for delimiter_index, delimiter in enumerate(lines):
        if not _is_markdown_table_delimiter(delimiter) or delimiter_index == 0:
            continue
        header = lines[delimiter_index - 1]
        if not _is_markdown_table_row(header):
            continue
        header_value = _project_in_field_whitespace(header.strip())
        body_index = delimiter_index + 1
        while body_index < len(lines) and _is_markdown_table_row(lines[body_index]):
            body_value = _project_in_field_whitespace(lines[body_index].strip())
            associated.append(
                (
                    f"{relative} table row line {body_index + 1}",
                    f"{header_value} {body_value}",
                    body_value,
                )
            )
            body_index += 1
    return associated


def _indented_code_action_fields(
    relative: str,
    text: str,
) -> list[tuple[str, str, str]]:
    """Keep blank-separated four-space/tab code payloads in one Policy field."""

    lines = text.splitlines()
    associated: list[tuple[str, str, str]] = []
    index = 0
    while index < len(lines):
        if not re.match(r"(?: {4}|\t)", lines[index]):
            index += 1
            continue
        start = index
        payload: list[str] = []
        while index < len(lines):
            line = lines[index]
            if not line.strip():
                payload.append("")
                index += 1
                continue
            if line.startswith("\t"):
                payload.append(line[1:])
                index += 1
                continue
            if line.startswith("    "):
                payload.append(line[4:])
                index += 1
                continue
            break
        visible_value = _project_in_field_whitespace(
            " ".join(item.strip() for item in payload)
        )
        associated.append(
            (
                f"{relative} indented code lines {start + 1}-{index}",
                visible_value,
                visible_value,
            )
        )
    return associated


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
        render_guard_source = _mask_markdown_literal_code(text)
        raw_html_source = CHAPTER02_MARKDOWN_AUTOLINK.sub("", render_guard_source)
        raw_html_tags = sorted(
            {
                match.group("tag").casefold()
                for match in CHAPTER02_RAW_HTML_TAG.finditer(raw_html_source)
                if CHAPTER02_SAFE_BR_TAG.fullmatch(match.group(0)) is None
            }
        )
        if raw_html_tags:
            messages.append(
                f"{relative}: raw HTML other than attribute-free br is "
                "unsupported in the "
                "bounded Policy surface; use equivalent Markdown: "
                f"{raw_html_tags!r}"
            )
        # Jekyll evaluates Liquid before Markdown, including source that later
        # becomes fenced, indented, or inline code.  Inspect the unmasked source.
        if CHAPTER02_LIQUID_CONSTRUCT.search(text):
            messages.append(
                f"{relative}: interpreted Liquid is unsupported in the bounded "
                "Policy surface"
            )
        if CHAPTER02_INVALID_BACKTICK_FENCE.search(text):
            messages.append(
                f"{relative}: backtick in a backtick-fence info string is "
                "unsupported in the bounded Policy surface"
            )
        if CHAPTER02_HTML_COMMENT_DELIMITER.search(render_guard_source):
            messages.append(
                f"{relative}: HTML comments are unsupported in the bounded "
                "Policy surface"
            )
        if CHAPTER02_DEFINITION_ITEM.search(render_guard_source):
            messages.append(
                f"{relative}: Kramdown definition-list syntax is unsupported in "
                "the bounded Policy surface"
            )
        if CHAPTER02_BLOCKQUOTE.search(render_guard_source):
            messages.append(
                f"{relative}: Markdown blockquote syntax is unsupported in the "
                "bounded Policy surface"
            )
        if CHAPTER02_KRAMDOWN_IAL.search(render_guard_source):
            messages.append(
                f"{relative}: Kramdown IAL syntax is unsupported in the bounded "
                "Policy surface"
            )
        if CHAPTER02_FOOTNOTE.search(render_guard_source):
            messages.append(
                f"{relative}: Kramdown footnote syntax is unsupported in the "
                "bounded Policy surface"
            )
        if CHAPTER02_ABBREVIATION_DEFINITION.search(render_guard_source):
            messages.append(
                f"{relative}: Kramdown abbreviation syntax is unsupported in "
                "the bounded Policy surface"
            )
        if CHAPTER02_KRAMDOWN_MATH.search(render_guard_source):
            messages.append(
                f"{relative}: Kramdown math syntax is unsupported in the "
                "bounded Policy surface"
            )
        if CHAPTER02_UNDERSCORE_EMPHASIS.search(render_guard_source):
            messages.append(
                f"{relative}: Markdown underscore-emphasis syntax is "
                "unsupported in the bounded Policy surface"
            )
        if CHAPTER02_REFERENCE_LINK.search(render_guard_source):
            messages.append(
                f"{relative}: Markdown reference-link syntax is unsupported in "
                "the bounded Policy surface"
            )
        if CHAPTER02_TITLED_INLINE_LINK.search(render_guard_source):
            messages.append(
                f"{relative}: Markdown link/image titles are unsupported in "
                "the bounded Policy surface"
            )
        rendered_text = unicodedata.normalize(
            "NFKC",
            html.unescape(render_guard_source),
        )
        if any(
            "\\" in match.group(0)
            for match in CHAPTER02_SPECIAL_URL.finditer(rendered_text)
        ):
            messages.append(
                f"{relative}: HTTP(S) or scheme-relative special URL containing "
                "backslash is unsupported in the bounded Policy surface"
            )
        executable_scheme_view = re.sub(
            r"[\t\r\n\f]",
            "",
            rendered_text,
        ).casefold()
        executable_prefixes = [
            prefix
            for prefix in CHAPTER02_EXECUTABLE_URL_PREFIXES
            if prefix in executable_scheme_view
        ]
        if executable_prefixes:
            messages.append(
                f"{relative}: executable URL scheme is unsupported in the "
                f"bounded Policy surface: {executable_prefixes!r}"
            )
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

        heading_action_fields = _heading_associated_action_fields(fields)
        selected_heading_action_counts = Counter(
            value for _, value, _ in heading_action_fields
        )
        for value in sorted(
            CHAPTER02_REVIEWED_HEADING_ACTION_CONTEXT[relative]
        ):
            count = selected_heading_action_counts[value]
            if count != 1:
                messages.append(
                    f"{relative}: reviewed heading/action context must occur "
                    f"exactly once in the bounded Policy surface; found {count}: "
                    f"{value!r}"
                )

        for location, value in fields:
            if value not in CHAPTER02_REVIEWED_ACTION_CONTEXT[relative]:
                findings.update(scan_action_text(value, location=location))
            if value not in CHAPTER02_REVIEWED_HOST_CONTEXT[relative]:
                findings.update(scan_host_policy(value, location=location))
        for location, value, body_value in heading_action_fields:
            # A reviewed body remains a question, uncertainty, prohibition, or
            # reject/return record when its unchanged heading hierarchy is added.
            if body_value in CHAPTER02_REVIEWED_ACTION_CONTEXT[relative]:
                continue
            if value in CHAPTER02_REVIEWED_HEADING_ACTION_CONTEXT[relative]:
                continue
            findings.update(scan_action_text(value, location=location))
        for structural_fields in (
            _nested_list_action_fields(relative, text),
            _table_header_action_fields(relative, text),
            _indented_code_action_fields(relative, text),
        ):
            for location, value, body_value in structural_fields:
                if body_value in CHAPTER02_REVIEWED_ACTION_CONTEXT[relative]:
                    continue
                findings.update(scan_action_text(value, location=location))
        for location, value in (
            _literal_code_policy_fields(relative, text)
            + _bare_angle_policy_fields(relative, render_guard_source)
        ):
            findings.update(scan_action_text(value, location=location))
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

    unsafe_manuscript_preamble_mutations = (
        (
            "introductory action",
            replace_once(
                chapter,
                "- 誰が検証を承認できるか",
                "- 第三者の本番APIへ接続する",
                "Chapter 2 manuscript introductory action regression",
            ),
            "target.real_or_external",
        ),
        (
            "leading host",
            "https://example.com/runbook\n" + chapter,
            "network.host_or_address",
        ),
    )
    for surface, unsafe_manuscript_preamble, expected_category in (
        unsafe_manuscript_preamble_mutations
    ):
        unsafe_manuscript_preamble_documents = dict(documents)
        unsafe_manuscript_preamble_documents[
            "manuscript/02-law-ethics-authorization.md"
        ] = unsafe_manuscript_preamble
        unsafe_manuscript_preamble_findings, _ = chapter02_policy_findings(
            unsafe_manuscript_preamble_documents
        )
        if not any(
            finding.category == expected_category
            for finding in unsafe_manuscript_preamble_findings
        ):
            error(
                f"Chapter 2 manuscript {surface} bypassed the Policy adapter"
            )

    for tail_heading in (
        "## 章のまとめ",
        "## 次に学ぶこと",
        "## 参考文献・Source Note ID",
    ):
        unsafe_manuscript_tail = replace_once(
            chapter,
            tail_heading,
            tail_heading + "\n\n第三者の本番APIへ接続する",
            f"Chapter 2 manuscript tail regression {tail_heading}",
        )
        unsafe_manuscript_tail_documents = dict(documents)
        unsafe_manuscript_tail_documents[
            "manuscript/02-law-ethics-authorization.md"
        ] = unsafe_manuscript_tail
        unsafe_manuscript_tail_findings, _ = chapter02_policy_findings(
            unsafe_manuscript_tail_documents
        )
        if not any(
            finding.category == "target.real_or_external"
            for finding in unsafe_manuscript_tail_findings
        ):
            error(
                "Chapter 2 manuscript tail bypassed the Policy adapter after "
                f"{tail_heading!r}"
            )

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

    pipe_prose_template = replace_once(
        template,
        soft_wrap_anchor,
        soft_wrap_anchor + "\n\n| 実Credentialを\n取得する",
        "Chapter 2 pipe-prefixed prose regression",
    )
    pipe_prose_documents = dict(documents)
    pipe_prose_documents["templates/authorization-checklist.md"] = (
        pipe_prose_template
    )
    pipe_prose_findings, _ = chapter02_policy_findings(pipe_prose_documents)
    if not any(
        finding.category == "secret.credential"
        for finding in pipe_prose_findings
    ):
        error(
            "Chapter 2 pipe-prefixed prose was treated as an unconfirmed table"
        )

    for source_hard_break in ("  \n", "\\\n"):
        hard_wrapped_template = replace_once(
            template,
            soft_wrap_anchor,
            (
                soft_wrap_anchor
                + "\n\n実Credentialを取"
                + source_hard_break
                + "得する"
            ),
            "Chapter 2 Markdown source hard-break regression",
        )
        hard_wrapped_documents = dict(documents)
        hard_wrapped_documents["templates/authorization-checklist.md"] = (
            hard_wrapped_template
        )
        hard_wrapped_findings, _ = chapter02_policy_findings(
            hard_wrapped_documents
        )
        if not any(
            finding.category == "secret.credential"
            for finding in hard_wrapped_findings
        ):
            error(
                "Chapter 2 Markdown source hard break split a protected token: "
                f"{source_hard_break!r}"
            )

    hard_break_anchor = "| Allowed methods |  |"
    for hard_break in (
        "<br>",
        "<br/>",
        "<br />",
        "<BR>",
        "&#10;",
        "&#x0A;",
        "&NewLine;",
        "&Tab;",
    ):
        hard_break_template = replace_once(
            template,
            hard_break_anchor,
            f"| Allowed methods | 実Credentialを{hard_break}取得する |",
            f"Chapter 2 Markdown hard-break regression {hard_break}",
        )
        hard_break_documents = dict(documents)
        hard_break_documents["templates/authorization-checklist.md"] = (
            hard_break_template
        )
        hard_break_findings, _ = chapter02_policy_findings(hard_break_documents)
        if not any(
            finding.category == "secret.credential"
            for finding in hard_break_findings
        ):
            error(
                "Chapter 2 Markdown hard break split a protected object from "
                f"its action: {hard_break!r}"
            )

    heading_association_anchor = "## 3. Scope Gate"
    unsafe_heading_associations = (
        ("### 実Credentialを\n\n取得する\n\n", "secret.credential"),
        (
            "### 実Credentialを\n\n#### 操作\n\n取得する\n\n",
            "secret.credential",
        ),
        (
            "### 実Credentialを\n\n前提を確認する。\n\n取得する\n\n",
            "secret.credential",
        ),
        (
            "Tokenを\n---\n\n再利用する\n\n",
            "operation.authentication_or_session",
        ),
        ("実Credentialを\n===\n\n取得する\n\n", "secret.credential"),
    )
    for unsafe_heading_association, expected_category in (
        unsafe_heading_associations
    ):
        heading_association_template = replace_once(
            template,
            heading_association_anchor,
            unsafe_heading_association + heading_association_anchor,
            "Chapter 2 heading/body association regression",
        )
        heading_association_documents = dict(documents)
        heading_association_documents[
            "templates/authorization-checklist.md"
        ] = heading_association_template
        heading_association_findings, heading_association_messages = (
            chapter02_policy_findings(
                heading_association_documents
            )
        )
        expected_finding = any(
            finding.category == expected_category
            for finding in heading_association_findings
        )
        rejected_setext_boundary = "\n---" in unsafe_heading_association or (
            "\n===" in unsafe_heading_association
        )
        rejected_setext_boundary = rejected_setext_boundary and any(
            "unexpected Policy section boundary" in message
            for message in heading_association_messages
        )
        if not expected_finding and not rejected_setext_boundary:
            error(
                "Chapter 2 Markdown heading split a protected object from its "
                f"associated action: {unsafe_heading_association!r}"
            )

    unsafe_nested_lists = (
        "- 実Credentialを\n  - 取得する\n\n",
        "- 実Credentialを\n  - 前提\n    - 取得する\n\n",
        "1. 実Credentialを\n   1. 取得する\n\n",
        (
            "- 実Credentialを\n\n  前提を確認する。\n\n"
            "  - 取得する\n\n"
        ),
        (
            "- 前提\n\n  実Credentialを\n\n"
            "  - 取得する\n\n"
        ),
        "- 実Credentialを\n\n  取得する\n\n",
        "- 実Credentialを\n\n    取得する\n\n",
    )
    for unsafe_nested_list in unsafe_nested_lists:
        nested_list_template = replace_once(
            template,
            heading_association_anchor,
            unsafe_nested_list + heading_association_anchor,
            "Chapter 2 nested-list association regression",
        )
        nested_list_documents = dict(documents)
        nested_list_documents["templates/authorization-checklist.md"] = (
            nested_list_template
        )
        nested_list_findings, _ = chapter02_policy_findings(
            nested_list_documents
        )
        if not any(
            finding.category == "secret.credential"
            for finding in nested_list_findings
        ):
            error(
                "Chapter 2 Markdown nested list split a protected object from "
                f"its associated action: {unsafe_nested_list!r}"
            )

    unsafe_header_tables = (
        "| 実Credentialを |\n|---|\n| 取得する |\n\n",
        (
            "| Field | 実Credentialを |\n"
            "|---|---|\n"
            "| Value | 取得する |\n\n"
        ),
    )
    for unsafe_header_table in unsafe_header_tables:
        header_table_template = replace_once(
            template,
            heading_association_anchor,
            unsafe_header_table + heading_association_anchor,
            "Chapter 2 table-header association regression",
        )
        header_table_documents = dict(documents)
        header_table_documents["templates/authorization-checklist.md"] = (
            header_table_template
        )
        header_table_findings, _ = chapter02_policy_findings(
            header_table_documents
        )
        if not any(
            finding.category == "secret.credential"
            for finding in header_table_findings
        ):
            error(
                "Chapter 2 Markdown table header split a protected object from "
                f"its associated body cell: {unsafe_header_table!r}"
            )

    unsafe_raw_html_structures = (
        (
            "<table><tr><th>実Credentialを</th></tr>"
            "<tr><td>取得する</td></tr></table>\n\n"
        ),
        "<h3>実Credentialを</h3>\n\n取得する\n\n",
        (
            "<ul><li>実Credentialを<ul><li>取得する</li></ul>"
            "</li></ul>\n\n"
        ),
        (
            "<details><summary>実Credentialを</summary>\n\n"
            "取得する\n\n</details>\n\n"
        ),
        "- safe\n\n    <script>alert(1)</script>\n\n",
        (
            "- outer\n    - inner\n\n"
            '    <span onmouseover="alert(1)">safe</span>\n\n'
        ),
        '\\`<span onmouseover="alert(1)">safe</span>`\n\n',
        "<javascript:alert(document.domain)>\n\n",
        '<br onmouseover="alert(document.domain)">\n\n',
    )
    for unsafe_raw_html_structure in unsafe_raw_html_structures:
        raw_html_template = replace_once(
            template,
            heading_association_anchor,
            unsafe_raw_html_structure + heading_association_anchor,
            "Chapter 2 raw-HTML structure regression",
        )
        raw_html_documents = dict(documents)
        raw_html_documents["templates/authorization-checklist.md"] = (
            raw_html_template
        )
        _, raw_html_messages = chapter02_policy_findings(raw_html_documents)
        if not any(
            "raw HTML other than attribute-free br is unsupported" in message
            for message in raw_html_messages
        ):
            error(
                "Chapter 2 adapter accepted unsupported raw HTML: "
                f"{unsafe_raw_html_structure!r}"
            )

    unsafe_fenced_blocks = (
        "```text\n実Credentialを\n\n取得する\n```\n\n",
        "~~~~text\n実Credentialを\n\n取得する\n~~~~\n\n",
    )
    for unsafe_fenced_block in unsafe_fenced_blocks:
        fenced_template = replace_once(
            template,
            heading_association_anchor,
            unsafe_fenced_block + heading_association_anchor,
            "Chapter 2 fenced-code association regression",
        )
        fenced_documents = dict(documents)
        fenced_documents["templates/authorization-checklist.md"] = fenced_template
        fenced_findings, _ = chapter02_policy_findings(fenced_documents)
        if not any(
            finding.category == "secret.credential"
            for finding in fenced_findings
        ):
            error(
                "Chapter 2 fenced code split a protected object from its action: "
                f"{unsafe_fenced_block!r}"
            )

    safe_fenced_heading = "```markdown\n## Example\n\nSafe text.\n```\n\n"
    safe_fenced_heading_template = replace_once(
        template,
        heading_association_anchor,
        safe_fenced_heading + heading_association_anchor,
        "Chapter 2 fenced-heading boundary regression",
    )
    safe_fenced_heading_documents = dict(documents)
    safe_fenced_heading_documents[
        "templates/authorization-checklist.md"
    ] = safe_fenced_heading_template
    _, safe_fenced_heading_messages = chapter02_policy_findings(
        safe_fenced_heading_documents
    )
    if any(
        "unexpected Policy section boundary" in message
        for message in safe_fenced_heading_messages
    ):
        error("Chapter 2 treated a fenced-code heading as a section boundary")

    literal_code_examples = (
        "```html\n<div>safe example</div>\n```\n\n",
        "    <div>safe example</div>\n\n",
        "- safe\n\n      <div>safe example</div>\n\n",
        "`<div>safe example</div>`\n\n",
        "`<div>safe example</div>\\`\n\n",
    )
    for literal_code_example in literal_code_examples:
        literal_code_template = replace_once(
            template,
            heading_association_anchor,
            literal_code_example + heading_association_anchor,
            "Chapter 2 literal-code render-guard regression",
        )
        literal_code_documents = dict(documents)
        literal_code_documents["templates/authorization-checklist.md"] = (
            literal_code_template
        )
        _, literal_code_messages = chapter02_policy_findings(
            literal_code_documents
        )
        if any(
            "raw HTML other than attribute-free br is unsupported" in message
            for message in literal_code_messages
        ):
            error(
                "Chapter 2 render guard interpreted literal code as raw HTML: "
                f"{literal_code_example!r}"
            )

    liquid_code_examples = (
        '```text\n実Credentialを取{{ "得" }}する\n```\n\n',
        '    実Credentialを取{{ "得" }}する\n\n',
        '`実Credentialを取{{ "得" }}する`\n\n',
    )
    for liquid_code_example in liquid_code_examples:
        liquid_code_template = replace_once(
            template,
            heading_association_anchor,
            liquid_code_example + heading_association_anchor,
            "Chapter 2 Liquid-in-code render-order regression",
        )
        liquid_code_documents = dict(documents)
        liquid_code_documents["templates/authorization-checklist.md"] = (
            liquid_code_template
        )
        _, liquid_code_messages = chapter02_policy_findings(
            liquid_code_documents
        )
        if not any(
            "interpreted Liquid is unsupported" in message
            for message in liquid_code_messages
        ):
            error(
                "Chapter 2 render guard masked pre-Markdown Liquid in code: "
                f"{liquid_code_example!r}"
            )

    unsafe_indented_blocks = (
        "    実Credentialを\n\n    取得する\n\n",
        "\t実Credentialを\n\n\t取得する\n\n",
    )
    for unsafe_indented_block in unsafe_indented_blocks:
        indented_template = replace_once(
            template,
            heading_association_anchor,
            unsafe_indented_block + heading_association_anchor,
            "Chapter 2 indented-code association regression",
        )
        indented_documents = dict(documents)
        indented_documents["templates/authorization-checklist.md"] = (
            indented_template
        )
        indented_findings, _ = chapter02_policy_findings(indented_documents)
        if not any(
            finding.category == "secret.credential"
            for finding in indented_findings
        ):
            error(
                "Chapter 2 indented code split a protected object from its "
                f"action: {unsafe_indented_block!r}"
            )

    unsupported_render_constructs = (
        (
            '| Allowed methods | 実Credentialを取{{ "得" }}する |',
            "interpreted Liquid is unsupported",
        ),
        (
            '{% assign operation = "実Credentialを取得する" %}\n'
            "{{ operation }}\n\n",
            "interpreted Liquid is unsupported",
        ),
        (
            "実Credentialを\n: 取得する\n\n",
            "Kramdown definition-list syntax is unsupported",
        ),
        (
            "> 実Credentialを\n>\n> 取得する\n\n",
            "Markdown blockquote syntax is unsupported",
        ),
        (
            '[safe](#){: href="javascript:alert(1)" }\n\n',
            "Kramdown IAL syntax is unsupported",
        ),
        (
            "実Credentialを[^x]\n\n[^x]: 取得する\n\n",
            "Kramdown footnote syntax is unsupported",
        ),
        (
            "実CredentialをCRED\n\n*[CRED]: 取得する\n\n",
            "Kramdown abbreviation syntax is unsupported",
        ),
        (
            "実Credentialを取$$得$$する\n\n",
            "Kramdown math syntax is unsupported",
        ),
        (
            "```text`bad\n"
            '<span onmouseover="alert(1)">safe</span>\n'
            "```\n\n",
            "backtick in a backtick-fence info string is unsupported",
        ),
        (
            "第三者の _本番_ システムへ接続する\n\n",
            "Markdown underscore-emphasis syntax is unsupported",
        ),
        (
            "第三者の __本番__ システムへ接続する\n\n",
            "Markdown underscore-emphasis syntax is unsupported",
        ),
        (
            "第三者の ___本番___ システムへ接続する\n\n",
            "Markdown underscore-emphasis syntax is unsupported",
        ),
        (
            "実Credentialを取[得][x]する\n\n[x]: #safe\n\n",
            "Markdown reference-link syntax is unsupported",
        ),
        (
            '[safe](# "実Credentialを取得する")\n\n',
            "Markdown link/image titles are unsupported",
        ),
        (
            "![safe](# '実Credentialを取得する')\n\n",
            "Markdown link/image titles are unsupported",
        ),
        (
            "[safe](# (実Credentialを取得する))\n\n",
            "Markdown link/image titles are unsupported",
        ),
        (
            "[safe](javascript:alert(1))\n\n",
            "executable URL scheme is unsupported",
        ),
        (
            "[safe][unsafe-ref]\n\n"
            "[unsafe-ref]: vbscript:msgbox(1)\n\n",
            "executable URL scheme is unsupported",
        ),
        (
            "[safe](data:text/html,<script>alert(1)</script>)\n\n",
            "executable URL scheme is unsupported",
        ),
        (
            "[safe](https://example.com\\\\@lab.test/)\n\n",
            "special URL containing backslash is unsupported",
        ),
        (
            "[safe](https://example.com&#92;&#92;@lab.test/)\n\n",
            "special URL containing backslash is unsupported",
        ),
        (
            "[safe](//attacker.com\\\\@lab.test/)\n\n",
            "special URL containing backslash is unsupported",
        ),
        (
            "[safe](//attacker.com&#92;&#92;@lab.test/)\n\n",
            "special URL containing backslash is unsupported",
        ),
        (
            "[safe](\\\\attacker.com\\@lab.test/)\n\n",
            "special URL containing backslash is unsupported",
        ),
        (
            "実Credentialを取<!--\n- hidden\n-->得する\n\n",
            "HTML comments are unsupported",
        ),
    )
    for unsupported_construct, expected_message in unsupported_render_constructs:
        if unsupported_construct.startswith("| Allowed methods"):
            unsupported_template = replace_once(
                template,
                hard_break_anchor,
                unsupported_construct,
                "Chapter 2 unsupported render construct regression",
            )
        else:
            unsupported_template = replace_once(
                template,
                heading_association_anchor,
                unsupported_construct + heading_association_anchor,
                "Chapter 2 unsupported render construct regression",
            )
        unsupported_documents = dict(documents)
        unsupported_documents["templates/authorization-checklist.md"] = (
            unsupported_template
        )
        _, unsupported_messages = chapter02_policy_findings(
            unsupported_documents
        )
        if not any(
            expected_message in message for message in unsupported_messages
        ):
            error(
                "Chapter 2 adapter accepted an unsupported rendered construct: "
                f"{unsupported_construct!r}"
            )

    literal_projection_mutations = (
        "`<!--第三者の本番システムへ接続する-->`\n\n",
        "<第三者の本番システムへ接続する>\n\n",
        "<&#31532;三者の本番システムへ接続する>\n\n",
    )
    for literal_projection in literal_projection_mutations:
        literal_projection_template = replace_once(
            template,
            heading_association_anchor,
            literal_projection + heading_association_anchor,
            "Chapter 2 literal reader-visible projection regression",
        )
        literal_projection_documents = dict(documents)
        literal_projection_documents["templates/authorization-checklist.md"] = (
            literal_projection_template
        )
        literal_projection_findings, _ = chapter02_policy_findings(
            literal_projection_documents
        )
        if not any(
            finding.category == "target.real_or_external"
            for finding in literal_projection_findings
        ):
            error(
                "Chapter 2 adapter discarded reader-visible literal text: "
                f"{literal_projection!r}"
            )

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

    unclassified_setext_template = replace_once(
        template,
        "## 3. Scope Gate",
        "Unclassified operational section\n---\n\n"
        "第三者の本番APIへ接続する\n\n## 3. Scope Gate",
        "Chapter 2 unclassified Setext section regression",
    )
    unclassified_setext_documents = dict(documents)
    unclassified_setext_documents["templates/authorization-checklist.md"] = (
        unclassified_setext_template
    )
    _, unclassified_setext_errors = chapter02_policy_findings(
        unclassified_setext_documents
    )
    if not any(
        "unexpected Policy section boundary" in message
        for message in unclassified_setext_errors
    ):
        error(
            "Chapter 2 Policy adapter accepted an unclassified Setext boundary"
        )

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
        "<https://lab.test/runbook>",
        "<security@example.test>",
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
        if delegated_url not in selected_chapter_text:
            error(
                "Chapter 2 Policy adapter omitted a reviewed public DELEGATE "
                f"destination from its reader-visible surface: {delegated_url}"
            )

    delegated_line = next(
        value
        for value in CHAPTER02_REVIEWED_HOST_CONTEXT[
            "manuscript/02-law-ethics-authorization.md"
        ]
        if "pentest-learning-book" in value
    )
    unsafe_delegate_chapter = replace_once(
        chapter,
        delegated_line,
        delegated_line + "。追加参照: https://example.com/runbook",
        "Chapter 2 DELEGATE host exemption regression",
    )
    unsafe_delegate_documents = dict(documents)
    unsafe_delegate_documents[
        "manuscript/02-law-ethics-authorization.md"
    ] = unsafe_delegate_chapter
    unsafe_delegate_findings, _ = chapter02_policy_findings(
        unsafe_delegate_documents
    )
    if not any(
        finding.category == "network.host_or_address"
        and "non-approved host suffix" in finding.reason
        for finding in unsafe_delegate_findings
    ):
        error("Chapter 2 public DELEGATE exemption survived a line mutation")


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
