#!/usr/bin/env python3
from __future__ import annotations

import json
import ipaddress
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.sync_book_site import SitePageRegistryError, parse_registry_data  # noqa: E402

ERRORS: list[str] = []
ALLOWED_DOMAIN_SUFFIXES = (".example", ".test", ".invalid")
SYNTHETIC_NAME_ALLOWLIST: frozenset[str] = frozenset()
ANALYTIC_ID_RE = re.compile(
    r"\b(?:TH|OBS|SEH|GAP|ALT|SN|EVD|NEG|CR|DECPT|ATTR|CF|ASM|AJ|FOR|REC|IND|DEC|REA|LIN|UNC|SEJ)-2026-025(?:-\d{3})?\b"
)
INDEPENDENCE_EVALUATION_TOKENS = (
    "independence",
    "independent",
    "corroboration",
    "same-origin",
    "circular reporting",
    "lineage",
    "独立",
    "裏付け",
)
URL_RE = re.compile(r"https?://[^\s<>()\]\[\"']+", re.IGNORECASE)
HOSTNAME_RE = re.compile(
    r"(?<![\w@-])(?P<host>(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,63})(?![\w-])",
)
DOMAIN_CANDIDATE_RE = re.compile(
    r"(?<![\w@-])(?P<host>(?:[^\W_]|-)+(?:[.。．｡](?:[^\W_]|-)+)+)(?![\w-])",
    re.UNICODE,
)
COMMON_PUBLIC_TLDS = frozenset(
    {
        "app",
        "biz",
        "cloud",
        "co",
        "com",
        "dev",
        "edu",
        "gov",
        "info",
        "io",
        "jp",
        "me",
        "mil",
        "net",
        "org",
        "site",
        "tech",
        "uk",
        "us",
        "xyz",
    }
)
RECOGNIZED_IDN_TLDS = frozenset(
    {
        "भारत",
        "испытание",
        "рф",
        "テスト",
        "みんな",
        "中国",
        "中國",
        "公司",
        "测试",
        "測試",
        "网络",
        "網絡",
        "한국",
        "δοκιμή",
        "시험",
        "परीक्षा",
    }
)
EMAIL_RE = re.compile(r"\b[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@(?P<host>[\w-]+(?:\.[\w-]+)+)\b", re.UNICODE)
IPV4_RE = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
IPV6_RE = re.compile(r"(?<![\w:])(?:[0-9A-Fa-f]{0,4}:){2,}[0-9A-Fa-f]{0,4}(?![\w:])")
SECRET_VALUE_RE = re.compile(
    r"(?i)\b(?:api[_ -]?key|secret|client[_ -]?secret|password|passwd|token|private[_ -]?key)\b\s*(?:=|:)\s*['\"]?[A-Za-z0-9_./+=-]{8,}"
)
PRIVATE_KEY_RE = re.compile(r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----")
KNOWN_SECRET_RE = re.compile(
    r"(?:AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9_]{20,}|"
    r"AWS_SECRET_ACCESS_KEY\s*=\s*[A-Za-z0-9/+=]{20,}|"
    r"xox[baprs]-[A-Za-z0-9-]{16,}|"
    r"eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}|"
    r"\bBearer\s+[A-Za-z0-9._~+/=-]{16,})"
)
PHONE_RE = re.compile(
    r"(?<![\d-])(?:\+\d{1,3}(?:[ .-]\d{1,4}){2,3}|0\d{1,3}[ .-]\d{2,4}[ .-]\d{3,4}|"
    r"\+\d{10,15}|1[2-9]\d{2}[2-9]\d{6}|0[1-9]\d{8,9})(?!\d)"
)
SYNTHETIC_CONTENT_FILES = (
    "manuscript/25-structured-analysis-attribution.md",
    "templates/analytic-judgment-record.md",
    "cases/ch25-structured-analysis-attribution-example.md",
    "cases/index.md",
    "cases/fixtures/index.md",
    "cases/fixtures/ch25-structured-analysis-attribution-dataset.json",
)
FORBIDDEN_CONFIDENCE_TOKENS = (
    "High confidence",
    "high confidence",
    "Moderate confidence",
    "moderate confidence",
    "Low confidence",
    "low confidence",
)
REQUIRED_SOURCE_IDS = (
    "SRC-ICD203-001",
    "SRC-CIA-SAT-001",
    "SRC-ATTACK-001",
    "SRC-BERKELEY-001",
)
CHAPTER25_SOURCE_CHECKED_AT = {
    "SRC-ATTACK-001": "2026-08-03",
    "SRC-ICD203-001": "2026-08-03",
    "SRC-CIA-SAT-001": "2026-08-03",
    "SRC-BERKELEY-001": "2026-07-25",
}


def error(message: str) -> None:
    ERRORS.append(message)



def read_text(relative: str) -> str:
    path = ROOT / relative
    if not path.is_file():
        error(f"missing required file: {relative}")
        return ""
    return path.read_text(encoding="utf-8")



def load_json(relative: str):
    text = read_text(relative)
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        error(f"{relative}: invalid JSON: {exc}")
        return {}



def require_tokens(relative: str, text: str, tokens: tuple[str, ...]) -> None:
    for token in tokens:
        if token not in text:
            error(f"{relative}: missing required token {token!r}")



def section_body(markdown: str, heading: str) -> str | None:
    pattern = re.compile(
        rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(markdown)
    if match is None:
        return None
    return match.group("body")



def check_learning_objectives(chapter: str, expected: list[str]) -> None:
    body = section_body(chapter, "学習目標")
    if body is None:
        error("manuscript/25-structured-analysis-attribution.md: missing 学習目標 section")
        return
    bullets = [
        line[2:].strip()
        for line in body.splitlines()
        if line.startswith("- ")
    ]
    if bullets != expected:
        error(
            "manuscript/25-structured-analysis-attribution.md: learning objectives "
            f"must exactly match book-config.json: {expected!r} != {bullets!r}"
        )



def recursive_confidence_values(value, label: str = "root") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            child_label = f"{label}.{key}"
            if "confidence" in key.lower():
                if isinstance(child, str):
                    if child not in {"高", "中", "低"}:
                        error(f"cases/fixtures/ch25-structured-analysis-attribution-dataset.json: {child_label} must be 高 / 中 / 低")
                elif isinstance(child, list):
                    for idx, item in enumerate(child):
                        if item not in {"高", "中", "低"}:
                            error(f"cases/fixtures/ch25-structured-analysis-attribution-dataset.json: {child_label}[{idx}] must be 高 / 中 / 低")
            recursive_confidence_values(child, child_label)
    elif isinstance(value, list):
        for idx, item in enumerate(value):
            recursive_confidence_values(item, f"{label}[{idx}]")



def assert_doc_ip(value: str, label: str) -> None:
    try:
        ip = ipaddress.ip_address(value)
    except ValueError as exc:
        error(f"{label}: invalid IP address: {exc}")
        return
    documentation_networks = (
        ipaddress.ip_network("192.0.2.0/24"),
        ipaddress.ip_network("198.51.100.0/24"),
        ipaddress.ip_network("203.0.113.0/24"),
        ipaddress.ip_network("2001:db8::/32"),
    )
    if not any(ip in network for network in documentation_networks):
        error(f"{label}: IP must be from documentation ranges")



def assert_synthetic_domain(value: str, label: str) -> None:
    host = value.rstrip(".").lower()
    try:
        ascii_host = host.encode("idna").decode("ascii")
    except UnicodeError:
        error(f"{label}: invalid IDN host: {value!r}")
        return
    if not any(ascii_host.endswith(suffix) for suffix in ALLOWED_DOMAIN_SUFFIXES):
        error(f"{label}: domain must use a reserved synthetic suffix: {value!r}")


def assert_synthetic_name(value: str, label: str) -> None:
    if value not in SYNTHETIC_NAME_ALLOWLIST and not value.startswith("SYNTH-"):
        error(f"{label}: synthetic named entity must use SYNTH- prefix or the explicit allowlist")


def collect_analytic_ids(value) -> set[str]:
    if isinstance(value, str):
        return set(ANALYTIC_ID_RE.findall(value))
    if isinstance(value, dict):
        return set().union(*(collect_analytic_ids(child) for child in value.values())) if value else set()
    if isinstance(value, list):
        return set().union(*(collect_analytic_ids(child) for child in value)) if value else set()
    return set()


def is_repository_file_reference(host: str) -> bool:
    if not host.endswith((".md", ".json", ".pdf", ".py", ".yml", ".yaml")):
        return False
    return any(path.is_file() for path in ROOT.rglob(host))


def normalize_unicode_host(raw: str) -> str:
    return raw.translate(str.maketrans({"。": ".", "．": ".", "｡": "."}))


def is_unicode_domain_candidate(raw: str) -> bool:
    """Recognize bare IDN or Unicode-separator hosts without treating prose as a host."""
    normalized = normalize_unicode_host(raw).rstrip(".")
    labels = normalized.split(".")
    if len(labels) < 2 or any(not label or "_" in label for label in labels):
        return False
    try:
        ascii_labels = [label.encode("idna").decode("ascii") for label in labels]
    except UnicodeError:
        return False
    if any(len(label) > 63 for label in ascii_labels):
        return False

    has_non_ascii = any(any(ord(char) > 127 for char in label) for label in labels)
    final_label = labels[-1].lower()
    if not has_non_ascii:
        # Unicode full stops are punctuation in ordinary prose too. For all-ASCII
        # labels, only treat a common public/reserved TLD as a domain candidate.
        return any(separator in raw for separator in "。．｡") and (
            final_label in COMMON_PUBLIC_TLDS
            or f".{final_label}" in ALLOWED_DOMAIN_SUFFIXES
        )

    # Treat an all-Unicode string separated only by a Japanese full stop as
    # prose, not a hostname (for example, "これは。テスト"). A bare IDN such
    # as 例え.テスト still uses an ASCII dot, while real。com is covered by the
    # all-ASCII branch above.
    if "." not in raw and all(
        all(not char.isascii() for char in label if char.isalnum())
        for label in labels
    ):
        return False

    # A recognized public/reserved final label distinguishes a bare IDN from
    # ordinary sentence fragments without claiming to be a general PII or
    # public-suffix detector.
    return (
        final_label in COMMON_PUBLIC_TLDS
        or f".{final_label}" in ALLOWED_DOMAIN_SUFFIXES
        or final_label in RECOGNIZED_IDN_TLDS
    )


def markdown_rows_by_id(markdown: str, prefix: str, label: str) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    for line in markdown.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if not cells:
            continue
        row_id = cells[0].strip("`")
        if not row_id.startswith(prefix):
            continue
        if row_id in rows:
            error(f"{label}: duplicate Markdown row ID {row_id}")
            continue
        rows[row_id] = cells
    return rows


def require_unique_object_ids(items: object, label: str) -> None:
    if not isinstance(items, list):
        error(f"{label}: must be an array")
        return
    identifiers = [item.get("id") for item in items if isinstance(item, dict)]
    if len(identifiers) != len(items) or any(not identifier for identifier in identifiers):
        error(f"{label}: every entry must be an object with a non-empty ID")
        return
    duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
    if duplicates:
        error(f"{label}: duplicate IDs are not allowed: {duplicates}")


def check_synthetic_content_safety(relative: str, text: str) -> None:
    """Check synthetic teaching content only; official Source Note URLs use SOURCE_POLICY."""
    for raw_url in URL_RE.findall(text):
        host = urlparse(raw_url.rstrip(".,;:")).hostname or ""
        assert_synthetic_domain(host, f"{relative}: URL")
    for match in HOSTNAME_RE.finditer(text):
        host = match.group("host").lower()
        if is_repository_file_reference(host):
            continue
        assert_synthetic_domain(host, f"{relative}: host/URL")
    for match in DOMAIN_CANDIDATE_RE.finditer(text):
        candidate = match.group("host")
        if not is_unicode_domain_candidate(candidate):
            continue
        assert_synthetic_domain(
            normalize_unicode_host(candidate).lower(),
            f"{relative}: Unicode/IDN host",
        )
    for match in EMAIL_RE.finditer(text):
        assert_synthetic_domain(match.group("host").lower(), f"{relative}: email")
    for match in IPV4_RE.finditer(text):
        assert_doc_ip(match.group(0), f"{relative}: IP")
    for match in IPV6_RE.finditer(text):
        assert_doc_ip(match.group(0), f"{relative}: IPv6")
    if SECRET_VALUE_RE.search(text):
        error(f"{relative}: contains a secret/token/private-key value assignment")
    if KNOWN_SECRET_RE.search(text):
        error(f"{relative}: contains a known secret/token format")
    if PRIVATE_KEY_RE.search(text):
        error(f"{relative}: contains a private-key block")
    if PHONE_RE.search(text):
        error(f"{relative}: contains a telephone-number-like value")


def check_structured_synthetic_people(relative: str, text: str) -> None:
    fields = (
        "Decision owner",
        "Primary analyst",
        "Reviewers",
        "Consumer / customer",
        "Communication scope",
    )
    for field in fields:
        match = re.search(
            rf"^\| {re.escape(field)} \| (?P<value>.*?) \|$",
            text,
            re.MULTILINE,
        )
        if match is None:
            error(f"{relative}: missing structured synthetic-name field {field!r}")
            continue
        for value in re.split(r"、|,", match.group("value")):
            normalized = value.strip().strip("`")
            if normalized and not normalized.startswith("SYNTH-"):
                error(
                    f"{relative}: {field} must contain SYNTH-prefixed names only: "
                    f"{normalized!r}"
                )
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        headers = [cell.strip() for cell in line.strip("|").split("|")]
        if "Owner" not in headers:
            continue
        owner_index = headers.index("Owner")
        for row in lines[index + 2 :]:
            if not row.startswith("|"):
                break
            cells = [cell.strip() for cell in row.strip("|").split("|")]
            if len(cells) <= owner_index:
                error(f"{relative}: malformed table row below Owner column")
                continue
            owner = cells[owner_index].strip("`")
            if owner and not owner.startswith("SYNTH-"):
                error(f"{relative}: Owner column must use a SYNTH-prefixed name: {owner!r}")



def check_no_forbidden_confidence(relative: str, text: str) -> None:
    for token in FORBIDDEN_CONFIDENCE_TOKENS:
        if token in text:
            error(f"{relative}: forbidden confidence token {token!r}")



def main() -> int:
    required_files = (
        "manuscript/25-structured-analysis-attribution.md",
        "templates/analytic-judgment-record.md",
        "cases/ch25-structured-analysis-attribution-example.md",
        "cases/index.md",
        "cases/fixtures/index.md",
        "cases/fixtures/ch25-structured-analysis-attribution-dataset.json",
        "site-pages.json",
        "artifact-index.md",
        "figure-index.md",
        "index.md",
        "references/sources.json",
        "references/reference-baseline.md",
        "SOURCE_POLICY.md",
        "scripts/render_reference_baseline.py",
        "package.json",
    )
    for relative in required_files:
        if not (ROOT / relative).is_file():
            error(f"missing required file: {relative}")

    config = load_json("book-config.json")
    chapter_config = None
    for item in config.get("structure", {}).get("chapters", []):
        if isinstance(item, dict) and item.get("id") == "ch25-structured-analysis-attribution":
            chapter_config = item
            break
    if chapter_config is None:
        error("book-config.json: missing ch25-structured-analysis-attribution")
        expected_objectives: list[str] = []
    else:
        expected_objectives = chapter_config.get("objectives", [])
        if expected_objectives != [
            "事実と判断を分離できる",
            "競合仮説を比較できる",
            "Analytic Judgment Recordを作成できる",
        ]:
            error("book-config.json: chapter 25 objectives must remain exactly the configured three objectives")

    chapter_path = "manuscript/25-structured-analysis-attribution.md"
    chapter = read_text(chapter_path)
    check_learning_objectives(chapter, expected_objectives)
    check_no_forbidden_confidence(chapter_path, chapter)
    require_tokens(
        chapter_path,
        chapter,
        (
            "## この章の位置付け",
            "### OWN",
            "### BRIDGE",
            "### DELEGATE",
            "情報（information）",
            "Source reliability、credibility、independence",
            "ACH",
            "Base rate",
            "Bayesian",
            "translation、timestamp、entity uncertainty",
            "missing evidence",
            "evidence of absence",
            "Attribution Ladder",
            "circular reporting",
            "same-origin republication",
            "false flag",
            "shared tooling",
            "infrastructure reuse",
            "Decision impactとCollection Priority",
            "F-25-01",
            "T-25-01",
            "T-25-02",
            "T-25-03",
            "F-25-02",
            "F-25-03",
            "../templates/analytic-judgment-record.md",
            "../cases/ch25-structured-analysis-attribution-example.md",
            "../cases/fixtures/index.md",
            "../cases/fixtures/ch25-structured-analysis-attribution-dataset.json",
            "SRC-ICD203-001",
            "SRC-CIA-SAT-001",
            "SRC-ATTACK-001",
            "SRC-BERKELEY-001",
            "帰属証拠ではない",
        ),
    )

    template_path = "templates/analytic-judgment-record.md"
    template = read_text(template_path)
    check_no_forbidden_confidence(template_path, template)
    require_tokens(
        template_path,
        template,
        (
            "Artifact ID | `ART-11`",
            "Case ID",
            "Decision Requirement ID",
            "Intelligence Requirement ID",
            "Threat Hypothesis ID",
            "Observation Hypothesis ID",
            "Source-evaluation hypothesis ID",
            "Related Alternative Hypothesis ID",
            "Relationship to primary judgment",
            "Collection Gap ID",
            "Alternative Hypothesis ID",
            "Source Note ID",
            "Evidence ID",
            "Negative Finding",
            "Attribution Ladder Assessment",
            "Permitted language",
            "Confirmed Facts",
            "Assumptions",
            "Judgments",
            "Forecasts",
            "Recommendations",
            "Indicators and Signposts",
            "Decision ID",
            "Reassessment ID",
            "Invalidation condition",
            "Circular Reporting",
            "Source-evaluation judgments",
            "same-origin",
            "false flag / shared tooling / infrastructure reuse",
            "Confidence | Basis",
            "高 / 中 / 低",
        ),
    )

    case_path = "cases/ch25-structured-analysis-attribution-example.md"
    case = read_text(case_path)
    check_no_forbidden_confidence(case_path, case)
    check_structured_synthetic_people(case_path, case)
    require_tokens(
        case_path,
        case,
        (
            "CASE-2026-025",
            "DR-2026-025",
            "IR-2026-025",
            "TH-2026-025-001",
            "TH-2026-025-002",
            "TH-2026-025-003",
            "OBS-2026-025-001",
            "OBS-2026-025-004",
            "OBS-2026-025-005",
            "SEH-2026-025-001",
            "GAP-2026-025-001",
            "GAP-2026-025-004",
            "ALT-2026-025-001",
            "SN-2026-025-001",
            "SN-2026-025-008",
            "EVD-2026-025-001",
            "EVD-2026-025-008",
            "NEG-2026-025-001",
            "CR-2026-025-001",
            "DECPT-2026-025-001",
            "ATTR-2026-025-001",
            "CF-2026-025-001",
            "SEJ-2026-025-001",
            "ASM-2026-025-001",
            "ASM-2026-025-004",
            "AJ-2026-025",
            "FOR-2026-025-001",
            "REC-2026-025-001",
            "IND-2026-025-001",
            "DEC-2026-025",
            "REA-2026-025",
            "観測範囲では成功痕跡を確認していない。侵害不存在や未遂確定は断定しない",
            "CampaignやOperatorまでの表現は支持しない",
            "同一Technical clusterの可能性がある",
            "same-origin republication",
            "異なる焦点質問の仮説を、一つの相互排他的なACH集合へ混在させない",
            "`ALT-2026-025-001`は外部誘導かSSO保守かを直接競合させ",
            "`SN-2026-025-001`〜`008`の合成Mail gateway",
            "`synthetic-idp-sign-in-summary`",
            "translated excerptはTechnical clusterと無関係な第三者が既知報告の用語を模倣して作成したfalse flag",
            "| `NEG-2026-025-001` | `EVD-2026-025-008` | `OBS-2026-025-004` |",
            "| `DECPT-2026-025-002` | false flag |",
            "| `EVD-2026-025-006` | `ALT-2026-025-002` |",
            "| `EVD-2026-025-006` | `SN-2026-025-006` | `OBS-2026-025-005` |",
            "| `OBS-2026-025-005` | `ALT-2026-025-002` |",
            "| `ASM-2026-025-001` | quarantine exportは対象期間の誘導mail評価に対して実質的に完全である",
            "| `ASM-2026-025-004` | IdP sign-in summaryは明示した2026-07-23〜2026-07-29のCoverage内で実質的に完全である",
            "| `GAP-2026-025-004` | `TH-2026-025-001`のmail Coverage |",
            "| `ALT-2026-025-001`, `ALT-2026-025-002`, `ALT-2026-025-003` |",
            ".example",
        ),
    )

    cases_index = read_text("cases/index.md")
    require_tokens(
        "cases/index.md",
        cases_index,
        (
            "合成Case索引",
            "ch01-integrated-security-case-example.md",
            "ch25-structured-analysis-attribution-example.md",
            "fixtures/index.md",
        ),
    )

    fixture_index = read_text("cases/fixtures/index.md")
    require_tokens(
        "cases/fixtures/index.md",
        fixture_index,
        (
            "Fixture Catalog",
            "ch25-structured-analysis-attribution-dataset.json",
            "synthetic data",
            "Lineage",
            "JSON fixtureを機械可読の正本",
            "一般的な人名・住所PII検出器ではない",
            "circular reporting",
        ),
    )

    dataset = load_json("cases/fixtures/ch25-structured-analysis-attribution-dataset.json")
    if dataset.get("synthetic") is not True:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: synthetic must be true")
    for collection_name in (
        "threatHypotheses",
        "sourceEvaluationHypotheses",
        "alternativeHypotheses",
        "observationHypotheses",
        "sourceNotes",
        "evidence",
        "collectionGaps",
    ):
        require_unique_object_ids(
            dataset.get(collection_name),
            f"cases/fixtures/ch25-structured-analysis-attribution-dataset.json:{collection_name}",
        )
    for key, expected in (
        ("artifactId", "ART-11"),
        ("caseId", "CASE-2026-025"),
        ("decisionRequirementId", "DR-2026-025"),
        ("intelligenceRequirementId", "IR-2026-025"),
        ("analyticJudgmentId", "AJ-2026-025"),
        ("decisionId", "DEC-2026-025"),
        ("reassessmentId", "REA-2026-025"),
    ):
        if dataset.get(key) != expected:
            error(f"cases/fixtures/ch25-structured-analysis-attribution-dataset.json: {key} must be {expected!r}")

    expected_allowed_data = [
        "synthetic-mail-gateway",
        "synthetic-decoy-proxy",
        "synthetic-registrar-export",
        "synthetic-vendor-bulletin",
        "synthetic-blog-repost",
        "synthetic-translated-excerpt",
        "synthetic-newsletter-recap",
        "synthetic-idp-sign-in-summary",
    ]
    if dataset.get("scope", {}).get("allowedData") != expected_allowed_data:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: scope.allowedData must cover exactly the eight synthetic Source Note origins")

    threat_hypotheses = dataset.get("threatHypotheses", [])
    if len(threat_hypotheses) < 3:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: requires at least three threat hypotheses")
    source_evaluation_hypotheses = dataset.get("sourceEvaluationHypotheses", [])
    if not source_evaluation_hypotheses:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: requires sourceEvaluationHypotheses")
    threat_ids = {item.get("id") for item in threat_hypotheses if isinstance(item, dict)}
    source_evaluation_ids = {item.get("id") for item in source_evaluation_hypotheses if isinstance(item, dict)}
    if "OBS-2026-025-004" not in {item.get("id") for item in dataset.get("observationHypotheses", []) if isinstance(item, dict)}:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: OBS-2026-025-004 must be present for the follow-on-access negative finding")
    alternative_ids = {
        item.get("id") for item in dataset.get("alternativeHypotheses", []) if isinstance(item, dict)
    }
    for item in threat_hypotheses:
        if not isinstance(item, dict):
            error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: threat hypothesis must be an object")
            continue
        statement = str(item.get("statement", "")).lower()
        if any(token in statement for token in INDEPENDENCE_EVALUATION_TOKENS):
            error(f"cases/fixtures/ch25-structured-analysis-attribution-dataset.json: {item.get('id')} mixes source evaluation into a threat hypothesis")
    if threat_ids & alternative_ids:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: threat and alternative hypothesis IDs must not overlap")
    threat_statements = {str(item.get("statement", "")).strip().lower() for item in threat_hypotheses if isinstance(item, dict)}
    alternative_statements = {
        str(item.get("statement", "")).strip().lower()
        for item in dataset.get("alternativeHypotheses", [])
        if isinstance(item, dict)
    }
    if threat_statements & alternative_statements:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: threat and alternative hypothesis statements must not duplicate")
    expected_alternatives = {
        "ALT-2026-025-001": "SSO maintenance side effect rather than external lure",
        "ALT-2026-025-002": "translated excerpt is a planted false flag by an unrelated third party and does not identify the operator behind the technical events",
        "ALT-2026-025-003": "shared phishing kit reuse rather than same operator or sponsor",
    }
    actual_alternatives = {
        item.get("id"): item.get("statement")
        for item in dataset.get("alternativeHypotheses", [])
        if isinstance(item, dict)
    }
    if actual_alternatives != expected_alternatives:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: alternative hypothesis semantics changed unexpectedly")
    expected_alternative_focus = {
        "ALT-2026-025-001": (
            "Were the observed technical events an external lure or an authorized SSO maintenance side effect?",
            "directly_competing",
        ),
        "ALT-2026-025-002": (
            "Does the translated excerpt identify the operator behind the technical events?",
            "attribution_boundary",
        ),
        "ALT-2026-025-003": (
            "Do shared artifacts identify one operator or sponsor?",
            "attribution_boundary",
        ),
    }
    actual_alternative_focus = {
        item.get("id"): (item.get("focusQuestion"), item.get("relationshipToPrimaryJudgment"))
        for item in dataset.get("alternativeHypotheses", [])
        if isinstance(item, dict)
    }
    if actual_alternative_focus != expected_alternative_focus:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: alternative focus-question grouping drifted")
    for alternative_id, statement in actual_alternatives.items():
        if any(token in str(statement).lower() for token in INDEPENDENCE_EVALUATION_TOKENS):
            error(
                "cases/fixtures/ch25-structured-analysis-attribution-dataset.json: "
                f"{alternative_id} mixes source evaluation into a competing alternative"
            )
    observation_ids: set[str] = set()
    for observation in dataset.get("observationHypotheses", []):
        if not isinstance(observation, dict):
            error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: observation hypothesis must be an object")
            continue
        observation_id = observation.get("id")
        observation_ids.add(observation_id)
        related_threat = observation.get("relatedThreatHypothesisId")
        related_source_evaluation = observation.get("relatedSourceEvaluationHypothesisId")
        related_alternative = observation.get("relatedAlternativeHypothesisId")
        if sum(bool(item) for item in (related_threat, related_source_evaluation, related_alternative)) != 1:
            error(f"cases/fixtures/ch25-structured-analysis-attribution-dataset.json: {observation_id} must reference exactly one hypothesis type")
        if related_threat and related_threat not in threat_ids:
            error(f"cases/fixtures/ch25-structured-analysis-attribution-dataset.json: {observation_id} references unknown threat hypothesis")
        if related_source_evaluation and related_source_evaluation not in source_evaluation_ids:
            error(f"cases/fixtures/ch25-structured-analysis-attribution-dataset.json: {observation_id} references unknown source-evaluation hypothesis")
        if related_alternative and related_alternative not in alternative_ids:
            error(f"cases/fixtures/ch25-structured-analysis-attribution-dataset.json: {observation_id} references unknown alternative hypothesis")
    alternative_observation = next(
        (
            item
            for item in dataset.get("observationHypotheses", [])
            if isinstance(item, dict) and item.get("id") == "OBS-2026-025-005"
        ),
        {},
    )
    if alternative_observation != {
        "id": "OBS-2026-025-005",
        "relatedAlternativeHypothesisId": "ALT-2026-025-002",
        "expectedSignal": "verifiable original-language context, speaker provenance, and collection path for the translated excerpt",
        "dataSource": ["SN-2026-025-006"],
    }:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: false-flag alternative observation contract drifted")
    if len(dataset.get("sourceNotes", [])) < 8:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: requires multiple source notes")
    if len(dataset.get("evidence", [])) < 8:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: requires multiple evidence records")
    if len(dataset.get("deceptionCandidates", [])) < 2:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: requires deception candidates")

    source_note_ids = {
        item.get("id") for item in dataset.get("sourceNotes", []) if isinstance(item, dict)
    }
    source_note_origins = {
        item.get("origin") for item in dataset.get("sourceNotes", []) if isinstance(item, dict)
    }
    if source_note_origins != set(expected_allowed_data):
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: Source Note origins must equal scope.allowedData")
    observation_by_id = {
        item.get("id"): item
        for item in dataset.get("observationHypotheses", [])
        if isinstance(item, dict)
    }
    markdown_observation_rows = markdown_rows_by_id(case, "OBS-2026-025-", case_path)
    expected_markdown_observation_relations = {
        observation_id: (
            observation.get("relatedThreatHypothesisId")
            or observation.get("relatedSourceEvaluationHypothesisId")
            or observation.get("relatedAlternativeHypothesisId")
        )
        for observation_id, observation in observation_by_id.items()
    }
    actual_markdown_observation_relations = {
        observation_id: cells[1].strip("`") if len(cells) > 1 else None
        for observation_id, cells in markdown_observation_rows.items()
    }
    if actual_markdown_observation_relations != expected_markdown_observation_relations:
        error("cases/ch25-structured-analysis-attribution-example.md: Observation-to-hypothesis mappings differ from the canonical fixture")
    expected_markdown_observation_sources = {
        observation_id: observation.get("dataSource", [])
        for observation_id, observation in observation_by_id.items()
    }
    actual_markdown_observation_sources = {
        observation_id: re.findall(r"SN-2026-025-\d{3}", " | ".join(cells))
        for observation_id, cells in markdown_observation_rows.items()
    }
    if actual_markdown_observation_sources != expected_markdown_observation_sources:
        error("cases/ch25-structured-analysis-attribution-example.md: Observation data-source mappings differ from the canonical fixture")

    markdown_source_rows = markdown_rows_by_id(case, "SN-2026-025-", case_path)
    actual_markdown_source_origins: dict[str, str | None] = {}
    for source_note_id, cells in markdown_source_rows.items():
        origin_match = re.search(r"`([^`]+)`", cells[1]) if len(cells) > 1 else None
        actual_markdown_source_origins[source_note_id] = origin_match.group(1) if origin_match else None
    expected_markdown_source_origins = {
        item.get("id"): item.get("origin")
        for item in dataset.get("sourceNotes", [])
        if isinstance(item, dict)
    }
    if actual_markdown_source_origins != expected_markdown_source_origins:
        error("cases/ch25-structured-analysis-attribution-example.md: Source Note origin mappings differ from the canonical fixture")
    for observation in dataset.get("observationHypotheses", []):
        if not isinstance(observation, dict):
            continue
        data_sources = observation.get("dataSource", [])
        if not isinstance(data_sources, list) or not data_sources:
            error(
                "cases/fixtures/ch25-structured-analysis-attribution-dataset.json: "
                f"{observation.get('id')} must reference at least one Source Note"
            )
        elif not set(data_sources) <= source_note_ids:
            error(
                "cases/fixtures/ch25-structured-analysis-attribution-dataset.json: "
                f"{observation.get('id')} references an unknown Source Note"
            )
    evidence_by_id = {
        item.get("id"): item for item in dataset.get("evidence", []) if isinstance(item, dict)
    }
    expected_evidence_links = {
        "EVD-2026-025-001": ("SN-2026-025-001", "OBS-2026-025-001"),
        "EVD-2026-025-002": ("SN-2026-025-002", "OBS-2026-025-001"),
        "EVD-2026-025-003": ("SN-2026-025-003", "OBS-2026-025-002"),
        "EVD-2026-025-004": ("SN-2026-025-004", "OBS-2026-025-003"),
        "EVD-2026-025-005": ("SN-2026-025-005", "OBS-2026-025-003"),
        "EVD-2026-025-006": ("SN-2026-025-006", "OBS-2026-025-005"),
        "EVD-2026-025-007": ("SN-2026-025-007", "OBS-2026-025-003"),
        "EVD-2026-025-008": ("SN-2026-025-008", "OBS-2026-025-004"),
    }
    actual_evidence_links = {
        evidence_id: (
            item.get("sourceNoteId"),
            item.get("observationHypothesisId"),
        )
        for evidence_id, item in evidence_by_id.items()
    }
    if actual_evidence_links != expected_evidence_links:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: Evidence to Source Note / Observation links drifted")
    markdown_evidence_rows = markdown_rows_by_id(case, "EVD-2026-025-", case_path)
    actual_markdown_evidence_links = {
        evidence_id: (
            cells[1].strip("`") if len(cells) > 1 else None,
            cells[2].strip("`") if len(cells) > 2 else None,
        )
        for evidence_id, cells in markdown_evidence_rows.items()
    }
    if actual_markdown_evidence_links != actual_evidence_links:
        error("cases/ch25-structured-analysis-attribution-example.md: Evidence mappings differ from the canonical fixture")
    if not all(source_id in source_note_ids for source_id, _ in actual_evidence_links.values()):
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: Evidence references an unknown Source Note")
    for evidence_id, (source_note_id, observation_id) in actual_evidence_links.items():
        observation = observation_by_id.get(observation_id, {})
        if source_note_id not in observation.get("dataSource", []):
            error(
                "cases/fixtures/ch25-structured-analysis-attribution-dataset.json: "
                f"{evidence_id} sourceNoteId is not declared by {observation_id}.dataSource"
            )

    for finding in dataset.get("negativeFindings", []):
        if not isinstance(finding, dict):
            error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: negative finding must be an object")
            continue
        observation_id = finding.get("observationHypothesisId")
        if not observation_id:
            error(f"cases/fixtures/ch25-structured-analysis-attribution-dataset.json: {finding.get('id')} must reference an observation hypothesis")
        elif observation_id not in observation_ids:
            error(f"cases/fixtures/ch25-structured-analysis-attribution-dataset.json: {finding.get('id')} references unknown observation hypothesis {observation_id!r}")
        for evidence_id in finding.get("relatedEvidenceIds", []):
            evidence = evidence_by_id.get(evidence_id)
            if evidence is None:
                error(f"cases/fixtures/ch25-structured-analysis-attribution-dataset.json: {finding.get('id')} references unknown Evidence {evidence_id!r}")
            elif evidence.get("observationHypothesisId") != observation_id:
                error(f"cases/fixtures/ch25-structured-analysis-attribution-dataset.json: {finding.get('id')} Evidence does not evaluate {observation_id}")
    if dataset.get("negativeFindings") != [
        {
            "id": "NEG-2026-025-001",
            "relatedEvidenceIds": ["EVD-2026-025-008"],
            "availableCoverage": "IdP sign-in summary for 2026-07-23 through 2026-07-29",
            "gapId": "GAP-2026-025-001",
            "permittedConclusion": "no successful follow-on access observed within available coverage; absence cannot be concluded",
            "observationHypothesisId": "OBS-2026-025-004",
        }
    ]:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: Negative Finding coverage/evidence contract drifted")

    gap_by_id = {
        item.get("id"): item for item in dataset.get("collectionGaps", []) if isinstance(item, dict)
    }
    if gap_by_id.get("GAP-2026-025-001", {}).get("relatedThreatHypothesisId") != "TH-2026-025-003":
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: GAP-2026-025-001 must qualify the follow-on-access hypothesis")
    if gap_by_id.get("GAP-2026-025-004") != {
        "id": "GAP-2026-025-004",
        "missingEvidence": "mail archive completeness and filter-bypass accounting for the quarantine export",
        "decisionImpact": "lure frequency could be underestimated if the export is incomplete",
        "priority": "中",
        "relatedThreatHypothesisId": "TH-2026-025-001",
    }:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: mail coverage gap contract drifted")

    categories = {item.get("category") for item in dataset.get("deceptionCandidates", [])}
    for category in ("false flag", "shared tooling", "infrastructure reuse"):
        if category not in categories:
            error(f"cases/fixtures/ch25-structured-analysis-attribution-dataset.json: missing deception category {category!r}")
    deception_links = {
        item.get("id"): item.get("supportedAlternativeHypothesisIds")
        for item in dataset.get("deceptionCandidates", [])
        if isinstance(item, dict)
    }
    if deception_links != {
        "DECPT-2026-025-001": ["ALT-2026-025-003"],
        "DECPT-2026-025-002": ["ALT-2026-025-002"],
        "DECPT-2026-025-003": ["ALT-2026-025-003"],
    }:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: deception-to-alternative links drifted")
    if any(
        alternative_id not in alternative_ids
        for links in deception_links.values()
        for alternative_id in (links or [])
    ):
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: deception candidate references an unknown alternative")

    lineage = dataset.get("lineage", {})
    if not lineage.get("edges"):
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: lineage.edges must be present")
    circular = lineage.get("circularReportingCandidates", [])
    if not circular:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: circularReportingCandidates must be present")
    else:
        if not any(item.get("sameOriginRepublication") and item.get("doNotCountAsIndependent") for item in circular):
            error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: same-origin republication must be marked as non-independent corroboration")

    attribution = dataset.get("attributionAssessment", {})
    if attribution.get("ladderLevel") != "L2":
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: expected L2 attribution stopping point")
    if "Technical cluster" not in " ".join(attribution.get("permittedLanguage", [])):
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: permittedLanguage must preserve technical-cluster wording")
    if "Campaign" not in attribution.get("prohibitedJump", ""):
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: prohibitedJump must block over-attribution")
    expected_judgment_alternatives = [
        "ALT-2026-025-001",
        "ALT-2026-025-002",
        "ALT-2026-025-003",
    ]
    if attribution.get("relatedAlternativeHypothesisIds") != expected_judgment_alternatives:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: attribution alternative links drifted")

    recursive_confidence_values(dataset)

    fixture_ids = collect_analytic_ids(dataset)
    markdown_ids = collect_analytic_ids(case)
    if fixture_ids != markdown_ids:
        missing_from_markdown = sorted(fixture_ids - markdown_ids)
        missing_from_fixture = sorted(markdown_ids - fixture_ids)
        error(
            "Chapter 25 Markdown/fixture analytic ID parity failed: "
            f"missing_from_markdown={missing_from_markdown}, missing_from_fixture={missing_from_fixture}"
        )

    confirmed_facts = dataset.get("judgments", {}).get("confirmedFacts", [])
    if any(isinstance(fact, dict) and fact.get("id") == "CF-2026-025-004" for fact in confirmed_facts):
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: CF-2026-025-004 must be a source-evaluation judgment, not a Confirmed Fact")
    for fact in confirmed_facts:
        statement = str(fact.get("statement", "")).lower() if isinstance(fact, dict) else ""
        if any(token in statement for token in INDEPENDENCE_EVALUATION_TOKENS):
            error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: Confirmed Fact must not contain independence/corroboration evaluation")
    confirmed_facts_case = re.search(r"^### 10\.1 Confirmed Facts\n(?P<body>.*?)(?=^### |\Z)", case, re.MULTILINE | re.DOTALL)
    if confirmed_facts_case and any(token in confirmed_facts_case.group("body").lower() for token in INDEPENDENCE_EVALUATION_TOKENS):
        error("cases/ch25-structured-analysis-attribution-example.md: Confirmed Facts must not contain independence/corroboration evaluation")
    source_evaluation_judgments = dataset.get("sourceEvaluationJudgments", [])
    if not source_evaluation_judgments:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: source-evaluation judgment is required for the circular-reporting assessment")
    else:
        lineage_ids = {item.get("id") for item in lineage.get("edges", []) if isinstance(item, dict)}
        circular_ids = {item.get("id") for item in circular if isinstance(item, dict)}
        for judgment in source_evaluation_judgments:
            if not isinstance(judgment, dict):
                error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: source-evaluation judgment must be an object")
                continue
            if judgment.get("sourceEvaluationHypothesisId") not in source_evaluation_ids:
                error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: source-evaluation judgment references an unknown source-evaluation hypothesis")
            if judgment.get("circularReportingCandidateId") not in circular_ids:
                error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: source-evaluation judgment must reference a circular-reporting candidate")
            if not set(judgment.get("lineageEdgeIds", [])) <= lineage_ids:
                error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: source-evaluation judgment references an unknown lineage edge")

    expected_assumptions = {
        "ASM-2026-025-001": ["GAP-2026-025-004"],
        "ASM-2026-025-002": ["GAP-2026-025-002"],
        "ASM-2026-025-003": ["GAP-2026-025-003"],
        "ASM-2026-025-004": ["GAP-2026-025-001"],
    }
    assumptions = dataset.get("judgments", {}).get("assumptions", [])
    actual_assumptions = {
        item.get("id"): item.get("relatedGapIds")
        for item in assumptions
        if isinstance(item, dict)
    }
    if actual_assumptions != expected_assumptions:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: Assumption-to-Gap links drifted")
    if any(
        not isinstance(item.get("whyNeeded"), str)
        or not item.get("whyNeeded")
        or not isinstance(item.get("failureTrigger"), str)
        or not item.get("failureTrigger")
        for item in assumptions
        if isinstance(item, dict)
    ):
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: assumptions require whyNeeded and failureTrigger")

    analytic_judgment = dataset.get("judgments", {}).get("analyticJudgment", {})
    if analytic_judgment.get("relatedAlternativeHypothesisIds") != expected_judgment_alternatives:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: central judgment must assess all three alternative hypotheses")
    expected_alternative_assessments = {
        "ALT-2026-025-001": ("weakened", ["EVD-2026-025-001", "EVD-2026-025-002", "EVD-2026-025-003"]),
        "ALT-2026-025-002": ("plausible-for-excerpt-only", ["EVD-2026-025-006"]),
        "ALT-2026-025-003": ("plausible-attribution-boundary", ["EVD-2026-025-002", "EVD-2026-025-003", "EVD-2026-025-004"]),
    }
    actual_alternative_assessments = {
        item.get("alternativeHypothesisId"): (item.get("disposition"), item.get("relatedEvidenceIds"))
        for item in analytic_judgment.get("alternativeAssessments", [])
        if isinstance(item, dict)
    }
    if actual_alternative_assessments != expected_alternative_assessments:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: alternative assessment dispositions/evidence drifted")
    if any(
        evidence_id not in evidence_by_id
        for _, evidence_ids in actual_alternative_assessments.values()
        for evidence_id in evidence_ids
    ):
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: alternative assessment references unknown Evidence")

    synthetic_entities = dataset.get("syntheticEntities", {})
    for entity_kind in ("organizations", "media", "roles"):
        entities = synthetic_entities.get(entity_kind, [])
        if not entities:
            error(f"cases/fixtures/ch25-structured-analysis-attribution-dataset.json: syntheticEntities.{entity_kind} must be present")
        for entity in entities:
            if not isinstance(entity, dict) or entity.get("synthetic") is not True:
                error(f"cases/fixtures/ch25-structured-analysis-attribution-dataset.json: syntheticEntities.{entity_kind} entries must be marked synthetic")
                continue
            assert_synthetic_name(str(entity.get("name", "")), f"cases/fixtures/ch25-structured-analysis-attribution-dataset.json:syntheticEntities.{entity_kind}")
    for domain in synthetic_entities.get("domains", []):
        assert_synthetic_domain(domain, "cases/fixtures/ch25-structured-analysis-attribution-dataset.json:syntheticEntities.domains")
    for source_note in dataset.get("sourceNotes", []):
        reference = source_note.get("reference")
        if isinstance(reference, str) and "." in reference:
            domain = reference.split("/", 1)[0]
            assert_synthetic_domain(domain, f"cases/fixtures/ch25-structured-analysis-attribution-dataset.json:sourceNotes.{source_note.get('id')}.reference")
    for ip in synthetic_entities.get("ips", []):
        assert_doc_ip(ip, "cases/fixtures/ch25-structured-analysis-attribution-dataset.json:syntheticEntities.ips")

    for relative in SYNTHETIC_CONTENT_FILES:
        check_synthetic_content_safety(relative, read_text(relative))

    if is_repository_file_reference("evil.md"):
        error("fixture safety regression: a non-existent .md basename was treated as a local file")
    if not is_repository_file_reference("analytic-judgment-record.md"):
        error("fixture safety regression: the tracked template basename was not recognized as a local file")
    secret_mutations = (
        "AWS_SECRET_ACCESS_KEY=" + "A" * 40,
        "xoxb-" + "1234567890-abcdefghijklmnop",
        "eyJhbGciOiJIUzI1NiJ9" + ".eyJzdWIiOiJzeW50aGV0aWMifQ.signature123",
    )
    for mutation in secret_mutations:
        if not KNOWN_SECRET_RE.search(mutation):
            error(f"fixture safety regression: known secret mutation was accepted: {mutation[:12]!r}")
    phone_mutations = ("0312345678", "+819012345678", "14155552671")
    for mutation in phone_mutations:
        if not PHONE_RE.search(mutation):
            error(f"fixture safety regression: compact telephone mutation was accepted: {mutation!r}")
    for non_phone in ("20260729101500", "0000000000"):
        if PHONE_RE.search(non_phone):
            error(f"fixture safety regression: non-telephone numeric value was rejected: {non_phone!r}")
    for mutation in ("例え.テスト", "real。com"):
        if not is_unicode_domain_candidate(mutation):
            error(f"fixture safety regression: Unicode/IDN domain mutation was accepted: {mutation!r}")
    if is_unicode_domain_candidate("これは。テスト"):
        error("fixture safety regression: Japanese prose was treated as a Unicode/IDN domain")

    package = load_json("package.json")
    scripts = package.get("scripts", {})
    if scripts.get("check:chapter25") != "python3 scripts/check_chapter25_contract.py":
        error("package.json: missing check:chapter25 script")
    if "check:chapter25" not in scripts.get("test", ""):
        error("package.json: test script must invoke check:chapter25")

    artifact_index = read_text("artifact-index.md")
    require_tokens(
        "artifact-index.md",
        artifact_index,
        (
            "ART-11",
            "Analytic Judgment Record",
            "templates/analytic-judgment-record.md",
            "Decision Requirement",
            "Lineage",
            "Reassessment",
        ),
    )

    figure_index = read_text("figure-index.md")
    require_tokens(
        "figure-index.md",
        figure_index,
        (
            "F-25-01",
            "T-25-01",
            "T-25-02",
            "T-25-03",
            "F-25-02",
            "F-25-03",
            "manuscript/25-structured-analysis-attribution.md",
        ),
    )

    index_md = read_text("index.md")
    require_tokens(
        "index.md",
        index_md,
        (
            "Analytic Judgment Record",
            "manuscript/25-structured-analysis-attribution.md",
            "templates/analytic-judgment-record.md",
            "cases/ch25-structured-analysis-attribution-example.md",
            "cases/index.md",
            "cases/fixtures/index.md",
        ),
    )

    sources = load_json("references/sources.json")
    if sources.get("checkedAt") != "2026-07-25":
        error("references/sources.json: root checkedAt must remain 2026-07-25; it is not a claim that every source was checked on 2026-08-03")
    source_items = {item.get("id"): item for item in sources.get("sources", []) if isinstance(item, dict)}
    for source_id in REQUIRED_SOURCE_IDS:
        if source_id not in source_items:
            error(f"references/sources.json: missing {source_id}")
    if source_items.get("SRC-BERKELEY-001", {}).get("publishedAt", "MISSING") is not None:
        error("references/sources.json: SRC-BERKELEY-001 publishedAt must remain null when the exact date is uncertain")
    for source_id, checked_at in CHAPTER25_SOURCE_CHECKED_AT.items():
        source = source_items.get(source_id, {})
        if source.get("checkedAt") != checked_at:
            error(f"references/sources.json: {source_id} checkedAt must be {checked_at} for its Chapter 25 Source Note")
        if 25 not in source.get("chapters", []):
            error(f"references/sources.json: {source_id} must map to chapter 25 when cited")
    attack = source_items.get("SRC-ATTACK-001", {})
    if "not as attribution proof" not in attack.get("notes", ""):
        error("references/sources.json: SRC-ATTACK-001 notes must state that ATT&CK is not attribution proof")
    icd = source_items.get("SRC-ICD203-001", {})
    if icd.get("url") != "https://www.dni.gov/files/documents/ICD/ICD-203.pdf":
        error("references/sources.json: SRC-ICD203-001 must use the official DNI PDF URL")
    if icd.get("publishedAt") != "2015-01-02":
        error("references/sources.json: SRC-ICD203-001 publishedAt must be 2015-01-02")
    if "2022-01-21" not in (icd.get("version") or "") and "2022-01-21" not in icd.get("notes", ""):
        error("references/sources.json: SRC-ICD203-001 must record the 2022-01-21 technical amendment")
    cia = source_items.get("SRC-CIA-SAT-001", {})
    if cia.get("publishedAt") is not None:
        error("references/sources.json: SRC-CIA-SAT-001 publishedAt should be null when only March 2009 is known")
    if "does not guarantee analytic correctness" not in cia.get("notes", ""):
        error("references/sources.json: SRC-CIA-SAT-001 notes must bound SAT usage")

    baseline = read_text("references/reference-baseline.md")
    require_tokens(
        "references/reference-baseline.md",
        baseline,
        (
            f"Registry全体の最終一括監査日: **{sources.get('checkedAt')}**",
            "各行の確認日は個別Source Noteの最終確認日",
            "SRC-CIA-SAT-001",
            "signed 2015-01-02; technical amendment effective 2022-01-21",
        ),
    )
    source_policy = read_text("SOURCE_POLICY.md")
    require_tokens(
        "SOURCE_POLICY.md",
        source_policy,
        (
            "Registry直下の`checkedAt`は、全Source Noteを一括監査した最終基準日",
            "個別Source Noteを章Issueで再確認した場合は、その項目の`checkedAt`だけを更新",
        ),
    )

    registry_data = load_json("site-pages.json")
    try:
        registry = parse_registry_data(registry_data)
    except SitePageRegistryError as exc:
        error(f"site-pages.json: invalid registry: {exc}")
        registry = {"pages": [], "directoryRoutes": {}}

    page_sources = {item.get("source"): item for item in registry.get("pages", []) if isinstance(item, dict)}
    required_routes = {
        "cases/index.md": "cases/index.md",
        "templates/analytic-judgment-record.md": "templates/analytic-judgment-record/index.md",
        "cases/fixtures/index.md": "cases/fixtures/index.md",
        "cases/ch25-structured-analysis-attribution-example.md": "cases/chapter-25-structured-analysis-attribution/index.md",
        "manuscript/25-structured-analysis-attribution.md": "chapters/chapter-25/index.md",
    }
    for source, destination in required_routes.items():
        item = page_sources.get(source)
        if item is None:
            error(f"site-pages.json: missing page for {source}")
        elif item.get("destination") != destination:
            error(f"site-pages.json: {source} destination must be {destination!r}")
    if registry.get("directoryRoutes", {}).get("cases") != "cases/index.md":
        error("site-pages.json: directoryRoutes.cases must target cases/index.md")

    for message in ERRORS:
        print(f"ERROR: {message}")
    if ERRORS:
        return 1

    print(
        "chapter 25 contract passed: manuscript, template, case, fixtures, source registry, "
        "registry routes, and confidence/safety semantics verified"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
