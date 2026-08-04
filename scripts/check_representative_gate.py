#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []

CHAPTERS = {
    1: ROOT / "manuscript/01-integrated-discipline.md",
    11: ROOT / "manuscript/11-web-api-hypothesis.md",
    17: ROOT / "manuscript/17-detection-engineering.md",
    25: ROOT / "manuscript/25-structured-analysis-attribution.md",
}
SOURCE_ID_RE = re.compile(r"\bSRC-[A-Z0-9-]+\b")
EXPECTED_REVIEW_BASELINE = "b56af680863a43017475b046ed7f9280f759844f"
EXPECTED_REVIEW_DATE = date(2026, 8, 4)
EXPECTED_REVIEW_EVIDENCE_URL = (
    "https://github.com/itdojp/white-hat-cyber-intelligence-book/"
    "issues/8#issuecomment-5181087925"
)
ARTIFACT_ROW_RE = re.compile(
    r"^\| (ART-\d{2}) \| ([^|]+?) \| ([^|]+?) \| `([^`]+)` \|$",
    re.MULTILINE,
)
REVIEW_HEADER = (
    "| Review area | Reviewer / role | Result | Date | Evidence reference | Notes |"
)
REVIEW_SEPARATOR = "|---|---|---|---|---|---|"
SYNTH_REVIEW_DISCLAIMER = (
    "以下は合成Case内のReview記入例であり、実際のGate reviewまたは本番承認の"
    "証跡ではない。Evidence referenceも合成IDである。"
)
FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
RAW_HTML_DELIMITERS = (
    (re.compile(r"^ {0,3}<\?"), "?>", "processing instruction"),
    (re.compile(r"^ {0,3}<!\[CDATA\[", re.IGNORECASE), "]]>", "CDATA block"),
    (re.compile(r"^ {0,3}<![A-Z]"), ">", "declaration"),
)
LIQUID_TAG_RE = re.compile(r"{%-?\s*([A-Za-z_][A-Za-z0-9_-]*)\b.*?-?%}")
LIQUID_BLOCK_ENDS = {
    "capture": "endcapture",
    "case": "endcase",
    "comment": "endcomment",
    "for": "endfor",
    "highlight": "endhighlight",
    "if": "endif",
    "tablerow": "endtablerow",
    "unless": "endunless",
}
KRAMDOWN_HIDDEN_OPEN_RE = re.compile(
    r"^ {0,3}\{::(comment|nomarkdown)\b", re.IGNORECASE
)
KRAMDOWN_EXTENSION_CLOSE_RE = re.compile(
    r"^ {0,3}\{:/([A-Za-z][A-Za-z0-9_-]*)\}", re.IGNORECASE
)
KRAMDOWN_IAL_OPEN_RE = re.compile(r"\{:")
ACTIVE_RAW_HTML_RE = re.compile(
    r"<(style|script|link)(?=[\s/>])", re.IGNORECASE
)
VOID_HTML_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}
FOREIGN_ROOT_TAGS = {"math", "svg"}
ACTIVE_RAW_HTML_TAGS = {"link", "script", "style"}
SCRIPT_URL_ATTRIBUTES = {
    "action",
    "data",
    "formaction",
    "href",
    "poster",
    "src",
    "xlink:href",
}
SCRIPT_URL_PREFIXES = (
    "javascript:",
    "vbscript:",
    "data:text/html",
    "data:application/xhtml+xml",
    "data:image/svg+xml",
)
URL_ASCII_TAB_OR_NEWLINE_RE = re.compile(r"[\t\r\n]")


def normalize_url_for_scheme_check(value: str | None) -> str:
    """Apply the browser URL parser's ASCII-tab/newline preprocessing."""
    return URL_ASCII_TAB_OR_NEWLINE_RE.sub("", value or "").strip().lower()


class RawHtmlContainerTracker(HTMLParser):
    """Track a strict raw-HTML container that cannot satisfy Markdown gates."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.stack: list[str] = []
        self.malformed = ""
        self.active_content_tag = ""
        self.unsafe_attribute = ""
        self.saw_tag = False

    def inspect_attributes(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        http_equiv_values: list[str] = []
        for name, value in attrs:
            attribute = name.lower()
            normalized_value = normalize_url_for_scheme_check(value)
            if attribute.startswith("on") or attribute in {"srcdoc", "style"}:
                self.unsafe_attribute = attribute
                return
            if attribute in SCRIPT_URL_ATTRIBUTES and normalized_value.startswith(
                SCRIPT_URL_PREFIXES
            ):
                self.unsafe_attribute = attribute
                return
            if attribute == "http-equiv":
                http_equiv_values.append(normalized_value)
        if tag == "meta" and "refresh" in http_equiv_values:
            self.unsafe_attribute = "http-equiv=refresh"

    def register_tag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self.saw_tag = True
        if tag in ACTIVE_RAW_HTML_TAGS and not self.active_content_tag:
            self.active_content_tag = tag
        self.inspect_attributes(tag, attrs)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        normalized = tag.lower()
        if normalized.endswith(":"):
            return
        self.register_tag(normalized, attrs)
        if normalized not in VOID_HTML_TAGS:
            self.stack.append(normalized)

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        # HTML browsers ignore the self-closing flag on non-void HTML elements.
        # SVG / MathML and their descendants use foreign-content semantics,
        # where the self-closing flag is honored.
        normalized = tag.lower()
        if normalized.endswith(":"):
            return
        self.register_tag(normalized, attrs)
        if normalized in FOREIGN_ROOT_TAGS or any(
            ancestor in FOREIGN_ROOT_TAGS for ancestor in self.stack
        ):
            return
        if normalized not in VOID_HTML_TAGS:
            self.stack.append(normalized)

    def handle_endtag(self, tag: str) -> None:
        normalized = tag.lower()
        if normalized.endswith(":"):
            return
        self.saw_tag = True
        if not self.stack:
            self.malformed = f"unexpected closing tag </{normalized}>"
            return
        if self.stack[-1] != normalized:
            self.malformed = (
                f"mismatched closing tag </{normalized}> for <{self.stack[-1]}>"
            )
            return
        self.stack.pop()


def error(message: str) -> None:
    ERRORS.append(message)


def check_raw_html_attribute_regressions() -> None:
    unsafe_markup = {
        "character-reference tab in javascript URL": (
            '<iframe src="java&#x09;script:alert(1)"></iframe>'
        ),
        "literal CR/LF in javascript URL": (
            '<iframe src="java\r\nscript:alert(1)"></iframe>'
        ),
        "meta refresh": (
            '<meta http-equiv="refresh" content="0;url=data:text/html,synthetic">'
        ),
        "object executable data URL": (
            '<object data="data:application/xhtml+xml,synthetic"></object>'
        ),
    }
    for label, markup in unsafe_markup.items():
        tracker = RawHtmlContainerTracker()
        tracker.feed(markup)
        tracker.close()
        if not tracker.unsafe_attribute:
            error(f"raw HTML safety regression accepted {label}")

    safe_markup = {
        "synthetic image": '<img src="synthetic.png" alt="synthetic fixture">',
        "inert data URL": '<a href="data:text/plain,synthetic">sample</a>',
        "description metadata": (
            '<meta name="description" content="synthetic fixture">'
        ),
        "local object": '<object data="synthetic.pdf"></object>',
    }
    for label, markup in safe_markup.items():
        tracker = RawHtmlContainerTracker()
        tracker.feed(markup)
        tracker.close()
        if tracker.unsafe_attribute or tracker.active_content_tag or tracker.malformed:
            error(f"raw HTML safety regression rejected {label}")


def read_text(relative: str) -> str:
    path = ROOT / relative
    if not path.is_file():
        error(f"missing required file: {relative}")
        return ""
    return path.read_text(encoding="utf-8")


def load_json(relative: str) -> dict:
    raw = read_text(relative)
    if not raw:
        return {}
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        error(f"{relative}: invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        error(f"{relative}: root must be an object")
        return {}
    return value


def require_tokens(relative: str, content: str, tokens: tuple[str, ...]) -> None:
    for token in tokens:
        if token not in content:
            error(f"{relative}: missing required token {token!r}")


def strip_html_comments(line: str, in_comment: bool) -> tuple[str, bool]:
    """Remove Markdown HTML comments while preserving visible text around them."""
    visible: list[str] = []
    cursor = 0
    while cursor < len(line):
        if in_comment:
            end = line.find("-->", cursor)
            if end == -1:
                return "".join(visible), True
            cursor = end + len("-->")
            in_comment = False
            continue

        start = line.find("<!--", cursor)
        if start == -1:
            visible.append(line[cursor:])
            break
        visible.append(line[cursor:start])
        cursor = start + len("<!--")
        in_comment = True
    return "".join(visible), in_comment


def mask_inline_code_and_escapes(line: str) -> str:
    """Mask inline code spans and escaped contract syntax."""
    masked = list(line)
    cursor = 0
    while True:
        opener = re.search(r"`+", line[cursor:])
        if opener is None:
            break
        start = cursor + opener.start()
        end = cursor + opener.end()
        ticks = line[start:end]
        closer = re.search(
            rf"(?<!`){re.escape(ticks)}(?!`)",
            line[end:],
        )
        if closer is None:
            cursor = end
            continue
        close_end = end + closer.end()
        masked[start:close_end] = " " * (close_end - start)
        cursor = close_end

    for index, character in enumerate(masked):
        if character not in "<{":
            continue
        backslashes = 0
        previous = index - 1
        while previous >= 0 and masked[previous] == "\\":
            backslashes += 1
            previous -= 1
        if backslashes % 2:
            masked[index] = " "
    return "".join(masked)


def strip_markdown_container_prefixes(line: str) -> str:
    """Strip blockquote and list markers before block-level contract checks."""
    remaining = line
    while True:
        blockquote = re.match(r"^ {0,3}>[ \t]?", remaining)
        if blockquote:
            remaining = remaining[blockquote.end() :]
            continue
        list_item = re.match(
            r"^ {0,3}(?:[-+*]|\d{1,9}[.)])[ \t]+",
            remaining,
        )
        if list_item:
            remaining = remaining[list_item.end() :]
            continue
        return remaining


def liquid_block_line_is_hidden(
    relative: str, line: str, stack: list[str]
) -> bool:
    """Track Liquid blocks whose body is conditional, captured, or non-Markdown."""
    tags = [match.group(1).lower() for match in LIQUID_TAG_RE.finditer(line)]
    was_hidden = bool(stack)

    if stack and stack[-1] == "comment":
        if LIQUID_BLOCK_ENDS["comment"] in tags:
            stack.pop()
        return True

    block_tag_seen = False
    for tag in tags:
        if tag in LIQUID_BLOCK_ENDS:
            stack.append(tag)
            block_tag_seen = True
            continue
        if tag not in LIQUID_BLOCK_ENDS.values():
            continue
        block_tag_seen = True
        if not stack:
            error(f"{relative}: unexpected Liquid closing tag {tag!r}")
            continue
        expected = LIQUID_BLOCK_ENDS[stack[-1]]
        if tag != expected:
            error(
                f"{relative}: Liquid closing tag {tag!r} does not match "
                f"{expected!r}"
            )
            continue
        stack.pop()
    return was_hidden or block_tag_seen or bool(stack)


def visible_markdown_lines(relative: str, content: str) -> list[str]:
    """Return contract-eligible Markdown outside code, comments, and raw HTML."""
    visible: list[str] = []
    in_comment = False
    fence_char = ""
    fence_length = 0
    html_tracker: RawHtmlContainerTracker | None = None
    html_delimiter_end = ""
    html_delimiter_name = ""
    liquid_stack: list[str] = []
    kramdown_hidden_stack: list[str] = []

    for raw_line in content.splitlines():
        if fence_char:
            fence_line = strip_markdown_container_prefixes(raw_line)
            if re.fullmatch(
                rf" {{0,3}}{re.escape(fence_char)}{{{fence_length},}}[ \t]*",
                fence_line,
            ):
                fence_char = ""
                fence_length = 0
            continue

        line, in_comment = strip_html_comments(raw_line, in_comment)
        if liquid_block_line_is_hidden(relative, line, liquid_stack):
            continue
        block_line = strip_markdown_container_prefixes(line)
        kramdown_open = KRAMDOWN_HIDDEN_OPEN_RE.match(block_line)
        kramdown_close = KRAMDOWN_EXTENSION_CLOSE_RE.match(block_line)
        if kramdown_hidden_stack:
            if kramdown_open:
                kramdown_hidden_stack.append(kramdown_open.group(1).lower())
            elif kramdown_close:
                actual = kramdown_close.group(1).lower()
                expected = kramdown_hidden_stack[-1]
                if actual != expected:
                    error(
                        f"{relative}: Kramdown closing extension {actual!r} "
                        f"does not match {expected!r}"
                    )
                else:
                    kramdown_hidden_stack.pop()
            continue
        if kramdown_open:
            kramdown_hidden_stack.append(kramdown_open.group(1).lower())
            continue
        if kramdown_close:
            error(
                f"{relative}: unexpected Kramdown closing extension "
                f"{kramdown_close.group(1).lower()!r}"
            )
            continue
        if html_delimiter_end:
            if html_delimiter_end in line:
                html_delimiter_end = ""
                html_delimiter_name = ""
            continue
        if html_tracker is not None:
            html_tracker.feed(line + "\n")
            if html_tracker.active_content_tag:
                error(
                    f"{relative}: active raw HTML <{html_tracker.active_content_tag}> "
                    "is not allowed in representative content"
                )
                html_tracker = None
            elif html_tracker.unsafe_attribute:
                error(
                    f"{relative}: unsafe raw HTML attribute "
                    f"{html_tracker.unsafe_attribute!r} is not allowed"
                )
                html_tracker = None
            elif html_tracker.malformed:
                error(f"{relative}: malformed raw HTML: {html_tracker.malformed}")
                html_tracker = None
            elif not html_tracker.stack:
                html_tracker.close()
                html_tracker = None
            continue

        fence_match = FENCE_OPEN_RE.match(block_line)
        if fence_match:
            fence = fence_match.group(1)
            fence_char = fence[0]
            fence_length = len(fence)
            continue

        contract_line = mask_inline_code_and_escapes(line)
        if KRAMDOWN_IAL_OPEN_RE.search(contract_line):
            error(f"{relative}: Kramdown IAL is not allowed")
            continue

        active_html = ACTIVE_RAW_HTML_RE.search(contract_line)
        if active_html:
            error(
                f"{relative}: active raw HTML <{active_html.group(1).lower()}> "
                "is not allowed in representative content"
            )
            continue

        delimited_html = False
        for opener, closer, name in RAW_HTML_DELIMITERS:
            match = opener.match(block_line)
            if match is None:
                continue
            if closer not in block_line[match.end() :]:
                html_delimiter_end = closer
                html_delimiter_name = name
            delimited_html = True
            break
        if delimited_html:
            continue

        candidate_tracker = RawHtmlContainerTracker()
        candidate_tracker.feed(contract_line + "\n")
        if candidate_tracker.saw_tag:
            if candidate_tracker.active_content_tag:
                error(
                    f"{relative}: active raw HTML "
                    f"<{candidate_tracker.active_content_tag}> "
                    "is not allowed in representative content"
                )
            elif candidate_tracker.unsafe_attribute:
                error(
                    f"{relative}: unsafe raw HTML attribute "
                    f"{candidate_tracker.unsafe_attribute!r} is not allowed"
                )
            elif candidate_tracker.malformed:
                error(
                    f"{relative}: malformed raw HTML: "
                    f"{candidate_tracker.malformed}"
                )
            elif candidate_tracker.stack:
                html_tracker = candidate_tracker
            else:
                candidate_tracker.close()
            continue
        visible.append(line)

    if fence_char:
        error(f"{relative}: unclosed fenced code block")
    if in_comment:
        error(f"{relative}: unclosed HTML comment")
    if html_delimiter_end:
        error(f"{relative}: unclosed raw HTML {html_delimiter_name}")
    if html_tracker is not None:
        open_tags = ", ".join(f"<{tag}>" for tag in html_tracker.stack)
        error(f"{relative}: unclosed raw HTML container(s): {open_tags}")
    if liquid_stack:
        open_tags = ", ".join(f"{{% {tag} %}}" for tag in liquid_stack)
        error(f"{relative}: unclosed Liquid block(s): {open_tags}")
    if kramdown_hidden_stack:
        open_tags = ", ".join(
            f"{{::{name}}}" for name in kramdown_hidden_stack
        )
        error(f"{relative}: unclosed Kramdown hidden extension(s): {open_tags}")
    return visible


def review_table_rows(
    relative: str,
    content: str,
    heading: str,
    *,
    require_synthetic_disclaimer: bool = False,
) -> dict[str, list[str]]:
    lines = visible_markdown_lines(relative, content)
    heading_indexes = [index for index, line in enumerate(lines) if line == heading]
    if not heading_indexes:
        error(f"{relative}: missing visible exact heading {heading!r}")
        return {}
    if len(heading_indexes) != 1:
        error(
            f"{relative}: visible exact heading {heading!r} must occur once, "
            f"got {len(heading_indexes)}"
        )
        return {}
    heading_index = heading_indexes[0]

    index = heading_index + 1
    while index < len(lines) and not lines[index].strip():
        index += 1
    if require_synthetic_disclaimer:
        if index >= len(lines) or lines[index] != SYNTH_REVIEW_DISCLAIMER:
            error(
                f"{relative}: Review table beneath {heading!r} must carry the "
                "exact synthetic-review disclaimer"
            )
            return {}
        index += 1
        while index < len(lines) and not lines[index].strip():
            index += 1
    if index >= len(lines) or lines[index] != REVIEW_HEADER:
        error(f"{relative}: Review table beneath {heading!r} has an invalid header")
        return {}
    if index + 1 >= len(lines) or lines[index + 1] != REVIEW_SEPARATOR:
        error(f"{relative}: Review table beneath {heading!r} has an invalid separator")
        return {}

    rows: dict[str, list[str]] = {}
    row_index = index + 2
    while row_index < len(lines):
        line = lines[row_index]
        if not line.startswith("|"):
            break
        row_index += 1
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 6:
            error(f"{relative}: Review table row must contain six cells: {line}")
            continue
        area = cells[0]
        if area in rows:
            error(f"{relative}: duplicate Review area {area!r}")
        else:
            rows[area] = cells

    return rows


def check_review_tables() -> None:
    templates = {
        "templates/integrated-security-case-map.md": (
            "## 16. Review",
            {
                "Technical correctness",
                "Safety / authorization",
                "Evidence / source quality",
                "Analytic quality",
                "Decision usefulness",
            },
        ),
        "templates/web-api-assessment-hypothesis-pack.md": (
            "## 11. Review",
            {
                "Technical correctness",
                "Safety / authorization",
                "Evidence / source quality",
                "Detection handoff",
                "Decision usefulness",
            },
        ),
        "templates/detection-validation.md": (
            "## 11. Review",
            {
                "Technical correctness",
                "Safety / authorization",
                "Evidence / source quality",
                "Coverage and analytic quality",
                "Decision usefulness",
            },
        ),
        "templates/analytic-judgment-record.md": (
            "## 15. Review",
            {
                "Technical correctness",
                "Safety / authorization",
                "Evidence / source quality",
                "Analytic quality",
                "Decision usefulness",
            },
        ),
    }
    for relative, (heading, expected_areas) in templates.items():
        rows = review_table_rows(relative, read_text(relative), heading)
        if set(rows) != expected_areas:
            error(
                f"{relative}: Review areas differ; "
                f"missing={sorted(expected_areas - set(rows))}, "
                f"extra={sorted(set(rows) - expected_areas)}"
            )

    cases = {
        "cases/ch01-integrated-security-case-example.md": (
            "## 16. Review",
            {
                "Technical correctness": "SYNTH-REV-01-TECH-001",
                "Safety / authorization": "SYNTH-REV-01-SAFE-001",
                "Evidence / source quality": "SYNTH-REV-01-EVID-001",
                "Analytic quality": "SYNTH-REV-01-ANALYTIC-001",
                "Decision usefulness": "SYNTH-REV-01-DEC-001",
            },
        ),
        "cases/ch11-web-api-assessment-example.md": (
            "## 11. Review",
            {
                "Technical correctness": "SYNTH-REV-11-TECH-001",
                "Safety / authorization": "SYNTH-REV-11-SAFE-001",
                "Evidence / source quality": "SYNTH-REV-11-EVID-001",
                "Detection handoff": "SYNTH-REV-11-DET-001",
                "Decision usefulness": "SYNTH-REV-11-DEC-001",
            },
        ),
        "cases/ch17-detection-validation-example.md": (
            "## 11. Review",
            {
                "Technical correctness": "SYNTH-REV-17-TECH-001",
                "Safety / authorization": "SYNTH-REV-17-SAFE-001",
                "Evidence / source quality": "SYNTH-REV-17-EVID-001",
                "Coverage and analytic quality": "SYNTH-REV-17-DET-001",
                "Decision usefulness": "SYNTH-REV-17-DEC-001",
            },
        ),
        "cases/ch25-structured-analysis-attribution-example.md": (
            "## 15. Review",
            {
                "Technical correctness": "SYNTH-REV-25-TECH-001",
                "Safety / authorization": "SYNTH-REV-25-SAFE-001",
                "Evidence / source quality": "SYNTH-REV-25-EVID-001",
                "Analytic quality": "SYNTH-REV-25-ANALYTIC-001",
                "Decision usefulness": "SYNTH-REV-25-DEC-001",
            },
        ),
    }
    for relative, (heading, expected) in cases.items():
        rows = review_table_rows(
            relative,
            read_text(relative),
            heading,
            require_synthetic_disclaimer=True,
        )
        if set(rows) != set(expected):
            error(
                f"{relative}: Review areas differ; "
                f"missing={sorted(set(expected) - set(rows))}, "
                f"extra={sorted(set(rows) - set(expected))}"
            )
        for area, evidence_id in expected.items():
            row = rows.get(area)
            if row is None:
                continue
            actual = row[4].strip("`")
            if actual != evidence_id:
                error(
                    f"{relative}: {area!r} must reference {evidence_id}, "
                    f"got {row[4]!r}"
                )


def split_source_ids(relative: str, content: str) -> tuple[set[str], set[str]]:
    marker = "## 参考文献・Source Note ID"
    visible_content = "\n".join(visible_markdown_lines(relative, content))
    if visible_content.count(marker) != 1:
        error(f"{relative}: missing reference section")
        return set(), set()
    body, section = visible_content.split(marker, 1)
    return set(SOURCE_ID_RE.findall(body)), set(SOURCE_ID_RE.findall(section))


def check_source_traceability() -> None:
    registry = load_json("references/sources.json")
    sources = registry.get("sources", [])
    if not isinstance(sources, list):
        error("references/sources.json: sources must be an array")
        return

    by_id: dict[str, dict] = {}
    mapped: dict[int, set[str]] = {number: set() for number in CHAPTERS}
    for item in sources:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            error("references/sources.json: every source must be an object with an id")
            continue
        source_id = item["id"]
        if source_id in by_id:
            error(f"references/sources.json: duplicate source id {source_id}")
            continue
        by_id[source_id] = item
        chapters = item.get("chapters", [])
        if isinstance(chapters, list):
            for number in CHAPTERS:
                if number in chapters:
                    mapped[number].add(source_id)

    for number, path in CHAPTERS.items():
        relative = path.relative_to(ROOT).as_posix()
        content = read_text(relative)
        used, referenced = split_source_ids(relative, content)
        if used != referenced:
            error(
                f"{relative}: used Source IDs and reference-section IDs differ; "
                f"only-used={sorted(used - referenced)}, "
                f"only-reference={sorted(referenced - used)}"
            )
        if used != mapped[number]:
            error(
                f"{relative}: used Source IDs and registry chapter mapping differ; "
                f"only-used={sorted(used - mapped[number])}, "
                f"only-mapped={sorted(mapped[number] - used)}"
            )
        for source_id in used:
            source = by_id.get(source_id)
            if source is None:
                error(f"{relative}: unknown Source Note ID {source_id}")
                continue
            for field in (
                "publisher",
                "title",
                "kind",
                "status",
                "url",
                "checkedAt",
                "nextReviewAt",
                "reviewTriggers",
            ):
                if source.get(field) in (None, "", []):
                    error(f"{source_id}: required representative-source field is empty: {field}")
            if "notes" not in source:
                error(f"{source_id}: required representative-source field is missing: notes")
            for field in ("checkedAt", "nextReviewAt"):
                try:
                    date.fromisoformat(str(source.get(field)))
                except ValueError:
                    error(f"{source_id}: {field} must be an ISO date")
            null_metadata = [
                field for field in ("version", "publishedAt") if source.get(field) is None
            ]
            notes = str(source.get("notes", "")).lower()
            if null_metadata and not any(
                phrase in notes
                for phrase in ("exact", "does not publish", "not recorded", "unknown")
            ):
                error(
                    f"{source_id}: null {', '.join(null_metadata)} "
                    "requires an explicit reason in notes"
                )


def check_artifacts_and_cases() -> None:
    artifact_text = read_text("artifact-index.md")
    rows = ARTIFACT_ROW_RE.findall(artifact_text)
    ids = [row[0] for row in rows]
    if len(ids) != len(set(ids)):
        error("artifact-index.md: duplicate Artifact ID")
    expected = {
        "ART-05": ("templates/detection-validation.md", "## 11. Review"),
        "ART-10": ("templates/integrated-security-case-map.md", "## 16. Review"),
        "ART-11": ("templates/web-api-assessment-hypothesis-pack.md", "## 11. Review"),
        "ART-12": ("templates/analytic-judgment-record.md", "## 15. Review"),
    }
    actual = {artifact_id: template for artifact_id, _, _, template in rows}
    for artifact_id, (template, review_heading) in expected.items():
        if actual.get(artifact_id) != template:
            error(
                f"artifact-index.md: {artifact_id} must map to {template}, "
                f"got {actual.get(artifact_id)!r}"
            )
        template_text = read_text(template)
        require_tokens(
            template,
            template_text,
            (
                artifact_id,
                REVIEW_HEADER,
            ),
        )
    relationships = {
        "cases/ch01-integrated-security-case-example.md": (
            "ART-10",
            "CASE-2026-001",
            "DR-2026-001",
            "ROE-2026-001",
            "FIND-2026-001",
            "TEL-2026-001",
            "DET-2026-001",
            "EVD-2026-001",
            "AJ-2026-001",
            "DEC-2026-001",
            "REA-2026-001",
            "## 16. Review",
            "合成Case内のReview記入例",
            "SYNTH-REV-01-TECH-001",
            "SYNTH-REV-01-SAFE-001",
            "SYNTH-REV-01-EVID-001",
            "SYNTH-REV-01-ANALYTIC-001",
            "SYNTH-REV-01-DEC-001",
        ),
        "cases/ch11-web-api-assessment-example.md": (
            "ART-11",
            "CASE-2026-011",
            "DR-2026-011",
            "ROE-2026-011",
            "FIND-2026-011",
            "TEL-2026-011",
            "DET-2026-011",
            "EVD-2026-011",
            "DEC-2026-011",
            "REA-2026-011",
            "## 11. Review",
            "Artifact completeness",
            "合成Case内のReview記入例",
            "SYNTH-REV-11-TECH-001",
            "SYNTH-REV-11-SAFE-001",
            "SYNTH-REV-11-EVID-001",
            "SYNTH-REV-11-DET-001",
            "SYNTH-REV-11-DEC-001",
        ),
        "cases/ch17-detection-validation-example.md": (
            "ART-05",
            "CASE-DET-2026-001",
            "CASE-2026-001",
            "DEC-2026-001",
            "DET-2026-001",
            "DET-2026-017-001",
            "refines",
            "EVD-DET-2026-001",
            "REA-DET-2026-001",
            "## 11. Review",
            "合成Case内のReview記入例",
            "SYNTH-REV-17-TECH-001",
            "SYNTH-REV-17-SAFE-001",
            "SYNTH-REV-17-EVID-001",
            "SYNTH-REV-17-DET-001",
            "SYNTH-REV-17-DEC-001",
        ),
        "cases/ch25-structured-analysis-attribution-example.md": (
            "ART-12",
            "CASE-2026-025",
            "DR-2026-025",
            "EVD-2026-025-001",
            "AJ-2026-025",
            "DEC-2026-025",
            "REA-2026-025",
            "## 15. Review",
            "合成Case内のReview記入例",
            "SYNTH-REV-25-TECH-001",
            "SYNTH-REV-25-SAFE-001",
            "SYNTH-REV-25-EVID-001",
            "SYNTH-REV-25-ANALYTIC-001",
            "SYNTH-REV-25-DEC-001",
        ),
    }
    for relative, tokens in relationships.items():
        require_tokens(relative, read_text(relative), tokens)


def check_frozen_contract() -> None:
    require_tokens(
        "WRITING_GUIDE.md",
        read_text("WRITING_GUIDE.md"),
        (
            "契約状態:",
            "代表章Gateで凍結",
            "Case・成果物・識別子の契約",
            "Source Noteと主張の契約",
            "Chapter Definition of Done",
            "Part単位の執筆運用",
            "refines",
            "supersedes",
            "independent",
            "P0 / P1が0件",
            "成果物の完成",
        ),
    )
    require_tokens(
        "SOURCE_POLICY.md",
        read_text("SOURCE_POLICY.md"),
        ("章との双方向Traceability", "本文中の使用ID", "Registry mapping"),
    )
    require_tokens(
        "SAFETY_SCOPE.md",
        read_text("SAFETY_SCOPE.md"),
        (
            "合成Caseとfixtureの公開契約",
            "fail-closed",
            "Secret、実Credential、Token、Cookie",
            "安全レビューの証跡",
        ),
    )
    require_tokens(
        "CROSS_BOOK_MAP.md",
        read_text("CROSS_BOOK_MAP.md"),
        (
            "章単位の境界受け入れ条件",
            "OWN",
            "BRIDGE",
            "DELEGATE",
            "安定した公開URL",
        ),
    )
    require_tokens(
        "TOC.md",
        read_text("TOC.md"),
        (
            "付録H　ラボ運用ガイド",
            "付録I　成果物評価ルーブリック",
            "付録J　既存書籍との学習導線",
        ),
    )
    package = load_json("package.json")
    scripts = package.get("scripts", {})
    if not isinstance(scripts, dict) or scripts.get("check:book-qa") != (
        "bash scripts/run_book_qa.sh"
    ):
        error("package.json: check:book-qa must run scripts/run_book_qa.sh")
    require_tokens(
        "scripts/run_book_qa.sh",
        read_text("scripts/run_book_qa.sh"),
        (
            "BOOK_FORMATTER_DIR",
            "npm test",
            "validate-config",
            "check-unicode.js",
            "check-textlint.js",
            "check-links.js",
            "check-layout-risk.js",
            "check-markdown-structure.js",
            "jekyll build",
            "check_built_site.py",
        ),
    )


def check_issue_template_and_gate_record() -> None:
    template = read_text(".github/ISSUE_TEMPLATE/part-writing.yml")
    require_tokens(
        ".github/ISSUE_TEMPLATE/part-writing.yml",
        template,
        (
            "name: Part writing",
            "id: part",
            "id: prerequisites",
            "id: source_plan",
            "id: artifact_plan",
            "id: safety",
            "id: pr_plan",
            "id: review_evidence",
            "id: publication_evidence",
            "独立Review Pass",
            "Command and lab reproducibility",
            "P0 / P1と未解決Review Threadが0件",
        ),
    )

    record = read_text("REPRESENTATIVE_CHAPTER_GATE.md")
    require_tokens(
        "REPRESENTATIVE_CHAPTER_GATE.md",
        record,
        (
            "判定: **GO**",
            "Open P0: **0**",
            "Open P1: **0**",
            "Open P2: **0**",
            "Technical accuracy",
            "Safety and legal boundary",
            "Source quality",
            "Analytic quality",
            "Instructional design",
            "Cross-book boundary",
            "Artifact traceability",
            "Publication quality",
            "Command and lab reproducibility",
            "manual editorial decision",
            "issues/8#issuecomment-5181087925",
            "Repository checker does not validate GitHub live state",
            "GATE-001",
            "GATE-046",
            "CASE-2026-001",
            "CASE-DET-2026-001",
        ),
    )
    if re.search(r"Open P[012]: \*\*[1-9]\d*\*\*", record):
        error("REPRESENTATIVE_CHAPTER_GATE.md: open findings must be zero for GO")

    baseline_match = re.search(
        r"^- Review baseline: `([0-9a-f]{40})`$", record, re.MULTILINE
    )
    if baseline_match is None:
        error(
            "REPRESENTATIVE_CHAPTER_GATE.md: Review baseline must be a "
            "lowercase 40-hex commit SHA"
        )
    else:
        baseline = baseline_match.group(1)
        if baseline != EXPECTED_REVIEW_BASELINE:
            error(
                "REPRESENTATIVE_CHAPTER_GATE.md: Review baseline differs from "
                f"the audited pin: {baseline}"
            )
        exists = subprocess.run(
            ["git", "cat-file", "-e", f"{baseline}^{{commit}}"],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if exists.returncode != 0:
            shallow = subprocess.run(
                ["git", "rev-parse", "--is-shallow-repository"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            if shallow.returncode != 0 or shallow.stdout.strip() != "true":
                error(
                    "REPRESENTATIVE_CHAPTER_GATE.md: Review baseline is not a "
                    f"commit in this repository: {baseline}"
                )
        else:
            ancestor = subprocess.run(
                ["git", "merge-base", "--is-ancestor", baseline, "HEAD"],
                cwd=ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            if ancestor.returncode != 0:
                error(
                    "REPRESENTATIVE_CHAPTER_GATE.md: Review baseline must be "
                    f"an ancestor of HEAD: {baseline}"
                )

    review_date_match = re.search(
        r"^- Review日: (\d{4}-\d{2}-\d{2})$", record, re.MULTILINE
    )
    if review_date_match is None:
        error("REPRESENTATIVE_CHAPTER_GATE.md: Review日 must be an ISO date")
    else:
        try:
            review_date = date.fromisoformat(review_date_match.group(1))
        except ValueError:
            error("REPRESENTATIVE_CHAPTER_GATE.md: Review日 is not a valid date")
        else:
            if review_date > date.today():
                error("REPRESENTATIVE_CHAPTER_GATE.md: Review日 must not be in the future")
            if review_date != EXPECTED_REVIEW_DATE:
                error(
                    "REPRESENTATIVE_CHAPTER_GATE.md: Review日 differs from the "
                    f"audited date: {review_date.isoformat()}"
                )

    evidence_match = re.search(
        r"^- 独立Review evidence: \[[^\]]+\]\("
        r"https://github\.com/itdojp/white-hat-cyber-intelligence-book/"
        r"issues/8#issuecomment-(\d+)\)$",
        record,
        re.MULTILINE,
    )
    if evidence_match is None:
        error(
            "REPRESENTATIVE_CHAPTER_GATE.md: independent review evidence must "
            "reference an Issue #8 comment"
        )
    else:
        evidence_url = (
            "https://github.com/itdojp/white-hat-cyber-intelligence-book/"
            f"issues/8#issuecomment-{evidence_match.group(1)}"
        )
        if evidence_url != EXPECTED_REVIEW_EVIDENCE_URL:
            error(
                "REPRESENTATIVE_CHAPTER_GATE.md: independent review evidence "
                f"differs from the audited comment: {evidence_url}"
            )


def main() -> int:
    check_raw_html_attribute_regressions()
    check_source_traceability()
    check_artifacts_and_cases()
    check_review_tables()
    check_frozen_contract()
    check_issue_template_and_gate_record()

    if ERRORS:
        for message in ERRORS:
            print(f"ERROR: {message}", file=sys.stderr)
        print(f"FAIL: {len(ERRORS)} representative-gate error(s)", file=sys.stderr)
        return 1

    print(
        "representative gate passed: 4 chapters, exact Source mapping, "
        "4 artifact contracts, separated reviews, frozen Chapter DoD, "
        "Part Issue template, and commit-bound structured manual GO record; "
        "GitHub reviews, CI, Pages, HTTP, and visual evidence remain external gates"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
