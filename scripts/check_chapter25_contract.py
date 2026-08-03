#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import ipaddress
import re
import stringprep
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.sync_book_site import SitePageRegistryError, parse_registry_data  # noqa: E402

IANA_TLD_SNAPSHOT = ROOT / "references/iana-tlds-alpha-by-domain.txt"
IANA_TLD_SNAPSHOT_VERSION = "2026080300"
IANA_TLD_SNAPSHOT_SHA256 = (
    "1a5b42ef79e837556bce63981f79591808237cb42f9fafb1c110783ddf0fcb95"
)


def load_iana_tld_snapshot() -> frozenset[str]:
    raw = IANA_TLD_SNAPSHOT.read_bytes()
    actual_sha256 = hashlib.sha256(raw).hexdigest()
    if actual_sha256 != IANA_TLD_SNAPSHOT_SHA256:
        raise RuntimeError(
            "IANA TLD snapshot digest mismatch: "
            f"expected {IANA_TLD_SNAPSHOT_SHA256}, got {actual_sha256}"
        )
    lines = raw.decode("ascii").splitlines()
    expected_header = f"# Version {IANA_TLD_SNAPSHOT_VERSION},"
    if not lines or not lines[0].startswith(expected_header):
        raise RuntimeError("IANA TLD snapshot version header mismatch")
    entries = lines[1:]
    if not entries or any(
        re.fullmatch(r"(?:[A-Z0-9-]{2,63})", entry) is None for entry in entries
    ):
        raise RuntimeError("IANA TLD snapshot contains an invalid ASCII label")
    normalized = [entry.lower() for entry in entries]
    if len(normalized) != len(set(normalized)):
        raise RuntimeError("IANA TLD snapshot contains duplicate labels")
    return frozenset(normalized)


ERRORS: list[str] = []
ALLOWED_DOMAIN_SUFFIXES = (".example", ".test", ".invalid")
IANA_ASCII_TLDS = load_iana_tld_snapshot()
RESERVED_ASCII_TLDS = frozenset(
    suffix.removeprefix(".") for suffix in ALLOWED_DOMAIN_SUFFIXES
)
SYNTHETIC_NAME_ALLOWLIST: frozenset[str] = frozenset()
FIXTURE_LABEL = "cases/fixtures/ch25-structured-analysis-attribution-dataset.json"
FIXTURE_IDENTITY_COLLECTIONS = {
    "markdownProjection.negativeFindings": "id",
    "markdownProjection.sourceEvaluationJudgments": "id",
    "markdownProjection.attributionAssessments": "id",
    "markdownProjection.judgmentAssumptions": "id",
    "syntheticEntities.organizations": "id",
    "syntheticEntities.media": "id",
    "syntheticEntities.roles": "id",
    "threatHypotheses": "id",
    "observationHypotheses": "id",
    "collectionGaps": "id",
    "alternativeHypotheses": "id",
    "sourceNotes": "id",
    "evidence": "id",
    "negativeFindings": "id",
    "uncertainties": "id",
    "lineage.edges": "id",
    "lineage.circularReportingCandidates": "id",
    "deceptionCandidates": "id",
    "judgments.confirmedFacts": "id",
    "judgments.assumptions": "id",
    "judgments.analyticJudgment.alternativeAssessments": "alternativeHypothesisId",
    "judgments.forecasts": "id",
    "judgments.recommendations": "id",
    "indicators": "id",
    "sourceEvaluationHypotheses": "id",
    "sourceEvaluationJudgments": "id",
}
FIXTURE_IDENTITY_SINGLETONS = {
    "attributionAssessment": "id",
    "judgments.analyticJudgment": "id",
    "decision": "id",
    "reassessment": "id",
}
FIXTURE_IDENTITY_SINGLETON_EXPECTED_IDS = {
    "attributionAssessment": "ATTR-2026-025-001",
    "judgments.analyticJudgment": "AJ-2026-025",
    "decision": "DEC-2026-025",
    "reassessment": "REA-2026-025",
}
FIXTURE_REFERENCE_TARGETS = {
    "sourceNoteId": ("sourceNotes",),
    "sourceNoteIds": ("sourceNotes",),
    "observationHypothesisId": ("observationHypotheses",),
    "relatedThreatHypothesisId": ("threatHypotheses",),
    "relatedSourceEvaluationHypothesisId": ("sourceEvaluationHypotheses",),
    "sourceEvaluationHypothesisId": ("sourceEvaluationHypotheses",),
    "relatedAlternativeHypothesisId": ("alternativeHypotheses",),
    "relatedAlternativeHypothesisIds": ("alternativeHypotheses",),
    "supportedAlternativeHypothesisIds": ("alternativeHypotheses",),
    "alternativeHypothesisId": ("alternativeHypotheses",),
    "relatedEvidenceIds": ("evidence",),
    "evidenceIds": ("evidence",),
    "gapId": ("collectionGaps",),
    "relatedGapIds": ("collectionGaps",),
    "relatedDecisionId": ("decision",),
    "triggeringIndicatorIds": ("indicators",),
    "lineageEdgeIds": ("lineage.edges",),
    "circularReportingCandidateId": ("lineage.circularReportingCandidates",),
    "affectedIds": ("__all_owners__",),
}
FIXTURE_REQUIRED_RECORD_REFERENCE_FIELDS = {
    "markdownProjection.negativeFindings": (
        "relatedEvidenceIds",
        "observationHypothesisId",
    ),
    "markdownProjection.attributionAssessments": (
        "relatedEvidenceIds",
        "relatedAlternativeHypothesisIds",
    ),
    "markdownProjection.judgmentAssumptions": ("relatedGapIds",),
    "evidence": ("sourceNoteId", "observationHypothesisId"),
    "negativeFindings": (
        "relatedEvidenceIds",
        "gapId",
        "observationHypothesisId",
    ),
    "uncertainties": ("affectedIds",),
    "lineage.edges": ("from", "to"),
    "lineage.circularReportingCandidates": ("sourceNoteIds",),
    "deceptionCandidates": (
        "evidenceIds",
        "supportedAlternativeHypothesisIds",
    ),
    "judgments.confirmedFacts": ("evidenceIds",),
    "judgments.assumptions": ("relatedGapIds",),
    "judgments.analyticJudgment.alternativeAssessments": (
        "alternativeHypothesisId",
        "relatedEvidenceIds",
    ),
    "judgments.recommendations": ("relatedDecisionId",),
    "indicators": ("relatedThreatHypothesisId",),
    "sourceEvaluationJudgments": (
        "sourceEvaluationHypothesisId",
        "lineageEdgeIds",
        "circularReportingCandidateId",
    ),
}
FIXTURE_REQUIRED_SINGLETON_REFERENCE_FIELDS = {
    "attributionAssessment": ("relatedAlternativeHypothesisIds",),
    "judgments.analyticJudgment": ("relatedAlternativeHypothesisIds",),
    "reassessment": ("triggeringIndicatorIds",),
}
FIXTURE_REQUIRED_ONE_OF_REFERENCE_FIELDS = {
    "observationHypotheses": (
        "relatedThreatHypothesisId",
        "relatedSourceEvaluationHypothesisId",
        "relatedAlternativeHypothesisId",
    )
}
FIXTURE_REQUIRED_REFERENCE_FIELDS_BY_ID = {
    "GAP-2026-025-001": ("relatedThreatHypothesisId",),
    "GAP-2026-025-004": ("relatedThreatHypothesisId",),
}
IDENTITY_RE = re.compile(r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+\Z")
ANALYTIC_ID_RE = re.compile(
    r"(?<![A-Z0-9-])(?:TH|OBS|SEH|GAP|ALT|SN|EVD|NEG|CR|DECPT|ATTR|CF|ASM|AJ|FOR|REC|IND|DEC|REA|LIN|UNC|SEJ)-2026-025(?:-\d{3})?(?![A-Z0-9-])"
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
DOMAIN_CANDIDATE_RE = re.compile(
    r"(?<![\w@-])(?P<host>(?:[^\W_]|-){1,63}(?:[.。．｡](?:[^\W_]|-){1,63}){1,9})(?![\w-])",
    re.UNICODE,
)
UNICODE_SEPARATOR_ASCII_HOST_RE = re.compile(
    r"(?<![A-Za-z0-9_@-])(?P<host>(?:[A-Za-z0-9-]+[。．｡])+[A-Za-z0-9-]+)"
    r"(?![A-Za-z0-9_-])"
)
DOCUMENTATION_IDN_TLDS = frozenset(
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
        "世界",
        "한국",
        "δοκιμή",
        "시험",
        "परीक्षा",
    }
)
IANA_UNICODE_TLDS = frozenset(
    tld.encode("ascii").decode("idna")
    for tld in IANA_ASCII_TLDS
    if tld.startswith("xn--")
)
DOCUMENTATION_IDN_ASCII_TLDS = frozenset(
    tld.encode("idna").decode("ascii") for tld in DOCUMENTATION_IDN_TLDS
)
RECOGNIZED_IDN_TLDS = IANA_UNICODE_TLDS | DOCUMENTATION_IDN_TLDS
DOCUMENTATION_ONLY_IDN_TLDS = DOCUMENTATION_IDN_TLDS - IANA_UNICODE_TLDS
RECOGNIZED_ASCII_TLDS = (
    IANA_ASCII_TLDS | RESERVED_ASCII_TLDS | DOCUMENTATION_IDN_ASCII_TLDS
)
ASCII_TLD_PATTERN = "|".join(
    re.escape(tld)
    for tld in sorted(RECOGNIZED_ASCII_TLDS, key=len, reverse=True)
)
IANA_UNICODE_TLD_PATTERN = "|".join(
    re.escape(tld) for tld in sorted(IANA_UNICODE_TLDS, key=len, reverse=True)
)
DOCUMENTATION_ONLY_IDN_TLD_PATTERN = "|".join(
    re.escape(tld)
    for tld in sorted(DOCUMENTATION_ONLY_IDN_TLDS, key=len, reverse=True)
)
HOSTNAME_RE = re.compile(
    r"(?<![A-Za-z0-9_@-])(?P<host>(?:[A-Za-z0-9-]{1,63}\.){1,9}(?:"
    + ASCII_TLD_PATTERN
    + r"))(?![A-Za-z0-9_-])",
    re.IGNORECASE,
)
GENERAL_HOST_CANDIDATE_RE = re.compile(
    r"(?P<host>(?:(?:[^\W_@]|-){1,63}[.。．｡]){1,9}(?:"
    + IANA_UNICODE_TLD_PATTERN
    + "|"
    + ASCII_TLD_PATTERN
    + r"))"
    r"(?=$|[^\x00-\x7f]|[/?:#]|[,;:!?)\]])"
    r"|(?P<documentation_host>(?:(?:[^\W_@]|-){1,63}[.。．｡]){1,9}(?:"
    + DOCUMENTATION_ONLY_IDN_TLD_PATTERN
    + r"))"
    r"(?=$|[/?:#]|[。．｡、,;；:：!！?？)\]」』])",
    re.IGNORECASE | re.UNICODE,
)
URL_IPV4_AUTHORITY_RE = re.compile(
    r"(?P<host>(?:\d{1,3}\.){3}\d{1,3})(?=$|[^\x00-\x7f]|[/?:#])"
)
RESERVED_SUFFIX_EXTENSION_RE = re.compile(
    r"(?P<host>(?:(?:[^\W_@]|-){1,63}[.。．｡]){1,9}"
    r"(?:example|test|invalid)(?:\.(?:[A-Za-z0-9-]{1,63}|"
    r"(?:[^\W_@\x00-\x7f]|-){1,63})|"
    r"[。．｡][A-Za-z0-9-]{1,63}))"
    r"(?=$|[^\x00-\x7f]|[/?:#]|[,;:!?)\]])",
    re.IGNORECASE | re.UNICODE,
)
HOST_CONTEXT_VALUE_RE = re.compile(
    r"(?:(?:合成)?(?:接続先|参照先|ドメイン)|\b(?:domain|host|URL)\b)"
    r"(?:\s*(?:は|が|を|[:：=])\s*|\s+)"
    r"(?P<value>[^\s`\"'<>|]{1,160})",
    re.IGNORECASE,
)
HOST_VALUE_TRAILING_PUNCTUATION_RE = re.compile(
    r"[、,;；:：)\]」』]+\Z",
    re.UNICODE,
)
EMAIL_RE = re.compile(
    r"(?<![A-Za-z0-9.!#$%&'*+/=?^_`{|}~-])"
    r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"(?P<host>[\w-]+(?:\.[\w-]+)+)(?![A-Za-z0-9_-])",
    re.UNICODE,
)
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
    r"(?<![\d-])(?:(?!\+81[ .-]?(?:19|20)\d{2}[ .-]?\d{4}[ .-]?\d{4})"
    r"\+\d{1,3}(?:[ .-]\d{1,4}){2,3}|0\d{1,3}[ .-]\d{2,4}[ .-]\d{3,4}|"
    r"\+\d{10,15}|81[1-9]\d{8,9}|1[2-9]\d{2}[2-9]\d{6}|0[1-9]\d{8,9})(?!\d)"
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
    "SRC-IANA-TLD-001",
)
CHAPTER25_SOURCE_CHECKED_AT = {
    "SRC-ATTACK-001": "2026-08-03",
    "SRC-ICD203-001": "2026-08-03",
    "SRC-CIA-SAT-001": "2026-08-03",
    "SRC-BERKELEY-001": "2026-07-25",
    "SRC-IANA-TLD-001": "2026-08-03",
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


def assert_synthetic_host(value: str, label: str) -> None:
    try:
        ipaddress.ip_address(value)
    except ValueError:
        assert_synthetic_domain(value, label)
        return
    assert_doc_ip(value, label)


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


def normalize_for_host_scanning(text: str) -> str:
    """Apply Python IDNA's Stringprep B.1/B.2 mapping before tokenization."""
    separator_sentinels = {
        "。": "\ue000",
        "．": "\ue001",
        "｡": "\ue002",
    }
    protected_text = text.translate(str.maketrans(separator_sentinels))
    mapped = "".join(
        "" if stringprep.in_table_b1(char) else stringprep.map_table_b2(char)
        for char in protected_text
    )
    normalized = unicodedata.normalize("NFKC", mapped)
    return normalized.translate(
        str.maketrans({sentinel: separator for separator, sentinel in separator_sentinels.items()})
    )


def general_host_from_match(match: re.Match[str]) -> str:
    host = match.group("host") or match.group("documentation_host")
    if not host:
        raise ValueError("general host candidate match did not contain a host")
    return host


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
    ascii_final_label = ascii_labels[-1].lower()
    if not has_non_ascii:
        # Unicode full stops are punctuation in ordinary prose too. For all-ASCII
        # labels, only treat an IANA snapshot/reserved TLD as a domain candidate.
        return (
            any(separator in raw for separator in "。．｡")
            and ascii_final_label in RECOGNIZED_ASCII_TLDS
        )

    # Treat an all-Unicode string separated only by a Japanese full stop as
    # prose, not a hostname (for example, "これは。テスト"). A bare IDN such
    # as 例え.テスト still uses an ASCII dot, while real。com is covered by the
    # all-ASCII branch above.
    if "." not in raw and all(
        all(not char.isascii() for char in label if char.isalnum())
        for label in labels
    ):
        if labels[0].endswith(("は", "が", "を", "に", "で", "と", "へ")):
            return False

    # An IANA snapshot/reserved final label distinguishes a bare IDN from
    # ordinary sentence fragments without claiming to be a general PII or
    # public-suffix detector.
    return ascii_final_label in RECOGNIZED_ASCII_TLDS


def url_domain_hosts(text: str):
    """Extract URL hosts without consuming adjacent Japanese prose."""
    for raw_url in URL_RE.findall(text):
        stripped_url = raw_url.rstrip(".,;:")
        parsed_host = urlparse(stripped_url).hostname
        if not parsed_host:
            continue
        ipv4_authority_match = URL_IPV4_AUTHORITY_RE.match(parsed_host)
        if ipv4_authority_match is not None:
            yield ipv4_authority_match.group("host")
            continue
        reserved_extension_match = RESERVED_SUFFIX_EXTENSION_RE.match(parsed_host)
        if reserved_extension_match is not None:
            yield reserved_extension_match.group("host")
            continue
        known_suffix_match = GENERAL_HOST_CANDIDATE_RE.match(parsed_host)
        if known_suffix_match is not None:
            yield general_host_from_match(known_suffix_match)
            continue
        yield parsed_host


def email_domain_hosts(text: str):
    """Extract complete email domains while separating adjacent Japanese prose."""
    for match in EMAIL_RE.finditer(text):
        raw_host = match.group("host")
        reserved_extension_match = RESERVED_SUFFIX_EXTENSION_RE.match(raw_host)
        if reserved_extension_match is not None:
            yield reserved_extension_match.group("host")
            continue
        known_suffix_match = GENERAL_HOST_CANDIDATE_RE.match(raw_host)
        if known_suffix_match is not None:
            yield general_host_from_match(known_suffix_match)
            continue
        yield raw_host


def contextual_domain_hosts(text: str):
    """Extract complete host values from explicit Japanese/English host contexts."""
    for match in HOST_CONTEXT_VALUE_RE.finditer(text):
        value = HOST_VALUE_TRAILING_PUNCTUATION_RE.sub("", match.group("value"))
        if value.lower().startswith(("http://", "https://")):
            extracted_hosts = list(url_domain_hosts(value))
            if extracted_hosts:
                yield extracted_hosts[0]
                continue
        known_suffix_match = GENERAL_HOST_CANDIDATE_RE.search(value)
        if known_suffix_match is not None:
            yield general_host_from_match(known_suffix_match)
            continue
        if any(separator in value for separator in ".。．｡"):
            # An explicitly labelled host with an unknown suffix is still a host
            # candidate. Passing it to the reserved-suffix validator fails closed.
            yield value


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


def normalized_markdown_cell(value: str) -> str:
    return value.strip().replace("`", "")


def subsection_body(markdown: str, heading: str) -> str | None:
    pattern = re.compile(
        rf"^### {re.escape(heading)}\n(?P<body>.*?)(?=^### |^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(markdown)
    return match.group("body") if match is not None else None


def is_valid_identity(value: object) -> bool:
    return isinstance(value, str) and IDENTITY_RE.fullmatch(value) is not None


def require_unique_object_identities(
    items: object,
    label: str,
    identity_key: str,
) -> None:
    if not isinstance(items, list):
        error(f"{label}: must be an array")
        return
    identifiers = [item.get(identity_key) for item in items if isinstance(item, dict)]
    if len(identifiers) != len(items) or any(
        not is_valid_identity(identifier) for identifier in identifiers
    ):
        error(
            f"{label}: every entry must be an object with a canonical ASCII {identity_key}"
        )
        return
    duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
    if duplicates:
        error(
            f"{label}: duplicate {identity_key} values are not allowed: {duplicates}"
        )


def require_declared_identity_collection_paths(dataset: object) -> None:
    """Reject deletion of any collection covered by the identity contract."""
    if not isinstance(dataset, dict):
        error(f"{FIXTURE_LABEL}: fixture root must be an object")
        return
    for relative_path in FIXTURE_IDENTITY_COLLECTIONS:
        current: object = dataset
        for key in relative_path.split("."):
            if not isinstance(current, dict) or key not in current:
                error(
                    f"{FIXTURE_LABEL}.{relative_path}: "
                    "declared identity collection is missing"
                )
                break
            current = current[key]


def declared_identity_key_for_object_path(relative_path: str) -> str | None:
    singleton_key = FIXTURE_IDENTITY_SINGLETONS.get(relative_path)
    if singleton_key is not None:
        return singleton_key
    collection_item = re.fullmatch(r"(?P<collection>.+)\[\d+\]", relative_path)
    if collection_item is None:
        return None
    return FIXTURE_IDENTITY_COLLECTIONS.get(collection_item.group("collection"))


def require_declared_identity_singletons(dataset: object) -> None:
    """Require each canonical singleton owner to be an object with a valid ID."""
    for relative_path, identity_key in FIXTURE_IDENTITY_SINGLETONS.items():
        singleton = nested_value(dataset, relative_path)
        if not isinstance(singleton, dict):
            error(f"{FIXTURE_LABEL}.{relative_path}: identity singleton must be an object")
            continue
        if not is_valid_identity(singleton.get(identity_key)):
            error(
                f"{FIXTURE_LABEL}.{relative_path}.{identity_key}: singleton identity "
                "must use canonical uppercase ASCII hyphenated form"
            )
            continue
        expected_id = FIXTURE_IDENTITY_SINGLETON_EXPECTED_IDS[relative_path]
        if singleton.get(identity_key) != expected_id:
            error(
                f"{FIXTURE_LABEL}.{relative_path}.{identity_key}: singleton identity "
                f"must match canonical reference {expected_id!r}"
            )


def require_unique_ids_recursively(value: object, label: str) -> None:
    """Reject duplicate record identities in every nested fixture collection."""
    prefix = f"{FIXTURE_LABEL}."
    relative_path = label[len(prefix) :] if label.startswith(prefix) else label
    identity_key = FIXTURE_IDENTITY_COLLECTIONS.get(relative_path)
    if identity_key is not None and not isinstance(value, list):
        error(f"{label}: declared identity collection must be an array")
        return
    if isinstance(value, dict):
        object_identity_key = declared_identity_key_for_object_path(relative_path)
        present_identity_keys = {
            key for key in ("id", "alternativeHypothesisId") if key in value
        }
        if present_identity_keys and object_identity_key is None:
            error(
                f"{label}: identity-bearing object path must be declared; "
                f"detected keys={sorted(present_identity_keys)}"
            )
        for record_identity_key in ("id", "alternativeHypothesisId"):
            if record_identity_key in value and not is_valid_identity(
                value[record_identity_key]
            ):
                error(
                    f"{label}.{record_identity_key}: record identity must use "
                    "canonical uppercase ASCII hyphenated form"
                )
        for key, child in value.items():
            require_unique_ids_recursively(child, f"{label}.{key}")
        return
    if not isinstance(value, list):
        return

    objects = [item for item in value if isinstance(item, dict)]
    detected_identity_keys = {
        key
        for key in ("id", "alternativeHypothesisId")
        if any(key in item for item in objects)
    }
    if identity_key is not None:
        require_unique_object_identities(value, label, identity_key)
    elif detected_identity_keys:
        error(
            f"{label}: identity-bearing collection path must be declared; "
            f"detected keys={sorted(detected_identity_keys)}"
        )
    for index, child in enumerate(value):
        require_unique_ids_recursively(child, f"{label}[{index}]")


def nested_value(value: object, relative_path: str) -> object | None:
    current = value
    for key in relative_path.split("."):
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def owner_ids_for_path(dataset: object, relative_path: str) -> set[str]:
    owner = nested_value(dataset, relative_path)
    if relative_path in FIXTURE_IDENTITY_SINGLETONS:
        if not isinstance(owner, dict):
            return set()
        identifier = owner.get(FIXTURE_IDENTITY_SINGLETONS[relative_path])
        return {identifier} if is_valid_identity(identifier) else set()
    identity_key = FIXTURE_IDENTITY_COLLECTIONS.get(relative_path)
    if identity_key != "id" or not isinstance(owner, list):
        return set()
    return {
        item.get(identity_key)
        for item in owner
        if isinstance(item, dict) and is_valid_identity(item.get(identity_key))
    }


def reference_integrity_violations(dataset: object) -> list[str]:
    target_ids = {
        target_path: owner_ids_for_path(dataset, target_path)
        for target_paths in FIXTURE_REFERENCE_TARGETS.values()
        for target_path in target_paths
        if target_path != "__all_owners__"
    }
    all_owner_ids = set().union(
        *(
            owner_ids_for_path(dataset, path)
            for path, identity_key in FIXTURE_IDENTITY_COLLECTIONS.items()
            if not path.startswith("markdownProjection.") and identity_key == "id"
        ),
        *(
            owner_ids_for_path(dataset, path)
            for path in FIXTURE_IDENTITY_SINGLETONS
        ),
    )
    violations: list[str] = []

    for collection_path, required_fields in (
        FIXTURE_REQUIRED_RECORD_REFERENCE_FIELDS.items()
    ):
        collection = nested_value(dataset, collection_path)
        if not isinstance(collection, list):
            continue
        for index, record in enumerate(collection):
            if not isinstance(record, dict):
                continue
            for required_field in required_fields:
                if required_field not in record:
                    violations.append(
                        f"{collection_path}[{index}].{required_field}: "
                        "declared relationship field is missing"
                    )
    for singleton_path, required_fields in (
        FIXTURE_REQUIRED_SINGLETON_REFERENCE_FIELDS.items()
    ):
        singleton = nested_value(dataset, singleton_path)
        if not isinstance(singleton, dict):
            continue
        for required_field in required_fields:
            if required_field not in singleton:
                violations.append(
                    f"{singleton_path}.{required_field}: "
                    "declared relationship field is missing"
                )
    for collection_path, one_of_fields in (
        FIXTURE_REQUIRED_ONE_OF_REFERENCE_FIELDS.items()
    ):
        collection = nested_value(dataset, collection_path)
        if not isinstance(collection, list):
            continue
        for index, record in enumerate(collection):
            if not isinstance(record, dict):
                continue
            present_fields = [field for field in one_of_fields if field in record]
            if len(present_fields) != 1:
                violations.append(
                    f"{collection_path}[{index}]: exactly one declared relationship "
                    f"field is required from {list(one_of_fields)}"
                )
    records_by_id: dict[str, tuple[str, dict]] = {}
    for collection_path, identity_key in FIXTURE_IDENTITY_COLLECTIONS.items():
        if identity_key != "id" or collection_path.startswith("markdownProjection."):
            continue
        collection = nested_value(dataset, collection_path)
        if not isinstance(collection, list):
            continue
        for index, record in enumerate(collection):
            if isinstance(record, dict) and isinstance(record.get("id"), str):
                records_by_id[record["id"]] = (
                    f"{collection_path}[{index}]",
                    record,
                )
    for record_id, required_fields in FIXTURE_REQUIRED_REFERENCE_FIELDS_BY_ID.items():
        record_entry = records_by_id.get(record_id)
        if record_entry is None:
            continue
        record_path, record = record_entry
        for required_field in required_fields:
            if required_field not in record:
                violations.append(
                    f"{record_path}.{required_field}: declared relationship field is missing"
                )

    declared_id_like_fields = {
        "id",
        "datasetId",
        "caseId",
        "artifactId",
        "decisionRequirementId",
        "intelligenceRequirementId",
        "analyticJudgmentId",
        "decisionId",
        "reassessmentId",
        "independenceGroupId",
        *FIXTURE_REFERENCE_TARGETS.keys(),
    }

    def walk(value: object, path: str) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                child_path = f"{path}.{key}" if path else key
                if (
                    re.search(r"(?:Id|Ids|ID|IDs)$", key)
                    and key not in declared_id_like_fields
                ):
                    violations.append(
                        f"{child_path}: undeclared identity/reference-like field"
                    )
                target_paths = FIXTURE_REFERENCE_TARGETS.get(key)
                if target_paths is not None:
                    expected_ids = (
                        all_owner_ids
                        if target_paths == ("__all_owners__",)
                        else set().union(*(target_ids[target] for target in target_paths))
                    )
                    values = child if isinstance(child, list) else [child]
                    expects_list = key.endswith("Ids")
                    if expects_list != isinstance(child, list) or not values or any(
                        not isinstance(item, str) or item not in expected_ids
                        for item in values
                    ):
                        violations.append(
                            f"{child_path}: references must resolve to "
                            f"{list(target_paths)}"
                        )
                if (
                    key in {"from", "to"}
                    and re.fullmatch(r"lineage\.edges\[\d+\]\.(?:from|to)", child_path)
                    and (
                        not isinstance(child, str)
                        or child not in target_ids.get("sourceNotes", set())
                    )
                ):
                    violations.append(
                        f"{child_path}: lineage endpoint must resolve to sourceNotes"
                    )
                walk(child, child_path)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f"{path}[{index}]")

    walk(dataset, "")
    return violations


def require_reference_integrity(dataset: object) -> None:
    for violation in reference_integrity_violations(dataset):
        error(f"{FIXTURE_LABEL}.{violation}")


def global_owner_identity_collisions(dataset: object) -> dict[str, list[str]]:
    """Find IDs reused by distinct canonical owning records.

    Markdown projections and alternativeHypothesisId values are references, not
    identity owners, and are intentionally excluded.
    """
    locations: dict[str, list[str]] = {}
    for relative_path, identity_key in FIXTURE_IDENTITY_COLLECTIONS.items():
        if relative_path.startswith("markdownProjection.") or identity_key != "id":
            continue
        collection = nested_value(dataset, relative_path)
        if not isinstance(collection, list):
            continue
        for index, item in enumerate(collection):
            if not isinstance(item, dict):
                continue
            identifier = item.get(identity_key)
            if not is_valid_identity(identifier):
                continue
            locations.setdefault(identifier, []).append(f"{relative_path}[{index}]")
    for relative_path, identity_key in FIXTURE_IDENTITY_SINGLETONS.items():
        singleton = nested_value(dataset, relative_path)
        if not isinstance(singleton, dict):
            continue
        identifier = singleton.get(identity_key)
        if not is_valid_identity(identifier):
            continue
        locations.setdefault(identifier, []).append(relative_path)
    return {
        identifier: owner_locations
        for identifier, owner_locations in locations.items()
        if len(owner_locations) > 1
    }


def require_globally_unique_owner_ids(dataset: object) -> None:
    collisions = global_owner_identity_collisions(dataset)
    if collisions:
        error(
            f"{FIXTURE_LABEL}: canonical owning-record IDs must be globally unique: "
            f"{collisions}"
        )


def check_synthetic_content_safety(relative: str, text: str) -> None:
    """Check synthetic teaching content only; official Source Note URLs use SOURCE_POLICY."""
    compatibility_text = normalize_for_host_scanning(text)
    for host in url_domain_hosts(compatibility_text):
        assert_synthetic_host(host, f"{relative}: URL")
    for match in HOSTNAME_RE.finditer(compatibility_text):
        host = match.group("host").lower()
        if is_repository_file_reference(host):
            continue
        assert_synthetic_domain(host, f"{relative}: host/URL")
    for match in RESERVED_SUFFIX_EXTENSION_RE.finditer(compatibility_text):
        candidate = normalize_unicode_host(match.group("host")).lower()
        assert_synthetic_domain(
            candidate,
            f"{relative}: reserved suffix followed by another label",
        )
    checked_unicode_hosts: set[str] = set()
    for match in GENERAL_HOST_CANDIDATE_RE.finditer(compatibility_text):
        candidate = general_host_from_match(match)
        if not is_unicode_domain_candidate(candidate):
            continue
        normalized = normalize_unicode_host(candidate).lower()
        checked_unicode_hosts.add(normalized)
        assert_synthetic_domain(normalized, f"{relative}: host/IDN")
    for candidate in contextual_domain_hosts(compatibility_text):
        normalized = normalize_unicode_host(candidate).lower()
        checked_unicode_hosts.add(normalized)
        assert_synthetic_host(normalized, f"{relative}: contextual host/IDN")
    for match in UNICODE_SEPARATOR_ASCII_HOST_RE.finditer(compatibility_text):
        candidate = match.group("host")
        if not is_unicode_domain_candidate(candidate):
            continue
        normalized = normalize_unicode_host(candidate).lower()
        checked_unicode_hosts.add(normalized)
        assert_synthetic_domain(normalized, f"{relative}: Unicode/IDN host")
    for match in DOMAIN_CANDIDATE_RE.finditer(compatibility_text):
        candidate = match.group("host")
        if not is_unicode_domain_candidate(candidate):
            continue
        normalized = normalize_unicode_host(candidate).lower()
        if normalized in checked_unicode_hosts:
            continue
        checked_unicode_hosts.add(normalized)
        assert_synthetic_domain(
            normalized,
            f"{relative}: Unicode/IDN host",
        )
    for host in email_domain_hosts(compatibility_text):
        assert_synthetic_domain(host.lower(), f"{relative}: email")
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
    require_declared_identity_collection_paths(dataset)
    require_declared_identity_singletons(dataset)
    if not isinstance(dataset, dict):
        dataset = {}
    if dataset.get("synthetic") is not True:
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: synthetic must be true")
    require_unique_ids_recursively(
        dataset,
        "cases/fixtures/ch25-structured-analysis-attribution-dataset.json",
    )
    require_globally_unique_owner_ids(dataset)
    require_reference_integrity(dataset)
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
    actual_markdown_source_details = {
        source_note_id: (
            actual_markdown_source_origins.get(source_note_id),
            normalized_markdown_cell(cells[2]) if len(cells) > 2 else None,
            normalized_markdown_cell(cells[3]) if len(cells) > 3 else None,
            normalized_markdown_cell(cells[4]) if len(cells) > 4 else None,
            normalized_markdown_cell(cells[5]) if len(cells) > 5 else None,
        )
        for source_note_id, cells in markdown_source_rows.items()
    }
    expected_markdown_source_details = {
        item.get("id"): (
            item.get("origin"),
            item.get("reliability"),
            item.get("credibility"),
            item.get("independenceGroupId"),
            item.get("collectedAt"),
        )
        for item in dataset.get("sourceNotes", [])
        if isinstance(item, dict)
    }
    if actual_markdown_source_details != expected_markdown_source_details:
        error(
            "cases/ch25-structured-analysis-attribution-example.md: Source Note "
            "reliability/credibility/independence/collection details differ from the canonical fixture"
        )

    markdown_projection = dataset.get("markdownProjection", {})
    if not isinstance(markdown_projection, dict):
        error("cases/fixtures/ch25-structured-analysis-attribution-dataset.json: markdownProjection must be an object")
        markdown_projection = {}

    markdown_negative_rows = markdown_rows_by_id(case, "NEG-2026-025-", case_path)
    actual_markdown_negative_findings = {
        finding_id: {
            "id": finding_id,
            "relatedEvidenceIds": re.findall(r"EVD-2026-025-\d{3}", cells[1]) if len(cells) > 1 else [],
            "observationHypothesisId": normalized_markdown_cell(cells[2]) if len(cells) > 2 else None,
            "searchedBehavior": normalized_markdown_cell(cells[3]) if len(cells) > 3 else None,
            "searchWindow": normalized_markdown_cell(cells[4]) if len(cells) > 4 else None,
            "availableCoverage": normalized_markdown_cell(cells[5]) if len(cells) > 5 else None,
            "gap": normalized_markdown_cell(cells[6]) if len(cells) > 6 else None,
            "permittedConclusion": normalized_markdown_cell(cells[7]) if len(cells) > 7 else None,
        }
        for finding_id, cells in markdown_negative_rows.items()
    }
    expected_markdown_negative_findings = {
        item.get("id"): item
        for item in markdown_projection.get("negativeFindings", [])
        if isinstance(item, dict)
    }
    if actual_markdown_negative_findings != expected_markdown_negative_findings:
        error("cases/ch25-structured-analysis-attribution-example.md: Negative Finding rendering differs from markdownProjection")

    markdown_source_judgment_rows = markdown_rows_by_id(case, "SEJ-2026-025-", case_path)
    actual_markdown_source_judgments = {
        judgment_id: {
            "id": judgment_id,
            "statement": normalized_markdown_cell(cells[1]) if len(cells) > 1 else None,
            "basis": normalized_markdown_cell(cells[2]) if len(cells) > 2 else None,
            "changeCondition": normalized_markdown_cell(cells[3]) if len(cells) > 3 else None,
        }
        for judgment_id, cells in markdown_source_judgment_rows.items()
    }
    expected_markdown_source_judgments = {
        item.get("id"): item
        for item in markdown_projection.get("sourceEvaluationJudgments", [])
        if isinstance(item, dict)
    }
    if actual_markdown_source_judgments != expected_markdown_source_judgments:
        error("cases/ch25-structured-analysis-attribution-example.md: Source-evaluation Judgment rendering differs from markdownProjection")

    markdown_attribution_rows = markdown_rows_by_id(case, "ATTR-2026-025-", case_path)
    actual_markdown_attribution = {
        assessment_id: {
            "id": assessment_id,
            "ladderLevel": normalized_markdown_cell(cells[1]) if len(cells) > 1 else None,
            "evidenceThresholdMet": normalized_markdown_cell(cells[2]) if len(cells) > 2 else None,
            "relatedEvidenceIds": re.findall(r"EVD-2026-025-\d{3}", cells[3]) if len(cells) > 3 else [],
            "relatedAlternativeHypothesisIds": re.findall(r"ALT-2026-025-\d{3}", cells[4]) if len(cells) > 4 else [],
            "permittedLanguage": normalized_markdown_cell(cells[5]) if len(cells) > 5 else None,
            "prohibitedJump": normalized_markdown_cell(cells[6]) if len(cells) > 6 else None,
        }
        for assessment_id, cells in markdown_attribution_rows.items()
    }
    expected_markdown_attribution = {
        item.get("id"): item
        for item in markdown_projection.get("attributionAssessments", [])
        if isinstance(item, dict)
    }
    if actual_markdown_attribution != expected_markdown_attribution:
        error("cases/ch25-structured-analysis-attribution-example.md: Attribution Assessment rendering differs from markdownProjection")

    judgment_assumption_body = subsection_body(case, "10.2 Assumptions")
    if judgment_assumption_body is None:
        error("cases/ch25-structured-analysis-attribution-example.md: missing 10.2 Assumptions subsection")
        markdown_assumption_rows: dict[str, list[str]] = {}
    else:
        markdown_assumption_rows = markdown_rows_by_id(
            judgment_assumption_body,
            "ASM-2026-025-",
            f"{case_path}:10.2 Assumptions",
        )
    actual_markdown_assumptions = {
        assumption_id: {
            "id": assumption_id,
            "statement": normalized_markdown_cell(cells[1]) if len(cells) > 1 else None,
            "whyNeeded": normalized_markdown_cell(cells[2]) if len(cells) > 2 else None,
            "failureTrigger": normalized_markdown_cell(cells[3]) if len(cells) > 3 else None,
            "relatedGapIds": re.findall(r"GAP-2026-025-\d{3}", cells[4]) if len(cells) > 4 else [],
        }
        for assumption_id, cells in markdown_assumption_rows.items()
    }
    expected_markdown_assumptions = {
        item.get("id"): item
        for item in markdown_projection.get("judgmentAssumptions", [])
        if isinstance(item, dict)
    }
    if actual_markdown_assumptions != expected_markdown_assumptions:
        error("cases/ch25-structured-analysis-attribution-example.md: Judgment Assumption rendering differs from markdownProjection")
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

    attribution_value = dataset.get("attributionAssessment", {})
    attribution = attribution_value if isinstance(attribution_value, dict) else {}
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

    judgments_value = dataset.get("judgments", {})
    judgments = judgments_value if isinstance(judgments_value, dict) else {}
    confirmed_facts = judgments.get("confirmedFacts", [])
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
    assumptions = judgments.get("assumptions", [])
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

    analytic_judgment_value = judgments.get("analyticJudgment", {})
    analytic_judgment = (
        analytic_judgment_value
        if isinstance(analytic_judgment_value, dict)
        else {}
    )
    judgment_body = subsection_body(case, "10.3 Judgments")
    if judgment_body is None:
        error("cases/ch25-structured-analysis-attribution-example.md: missing 10.3 Judgments subsection")
        markdown_judgment_rows: dict[str, list[str]] = {}
    else:
        markdown_judgment_rows = markdown_rows_by_id(
            judgment_body,
            "AJ-2026-025",
            f"{case_path}:10.3 Judgments",
        )
    actual_markdown_judgments = {
        judgment_id: {
            "id": judgment_id,
            "statement": normalized_markdown_cell(cells[1]) if len(cells) > 1 else None,
            "confidence": normalized_markdown_cell(cells[2]) if len(cells) > 2 else None,
            "basis": normalized_markdown_cell(cells[3]) if len(cells) > 3 else None,
            "relatedAlternativeHypothesisIds": re.findall(
                r"ALT-2026-025-\d{3}", cells[4]
            ) if len(cells) > 4 else [],
            "changeCondition": normalized_markdown_cell(cells[5]) if len(cells) > 5 else None,
        }
        for judgment_id, cells in markdown_judgment_rows.items()
    }
    expected_markdown_judgments = {
        analytic_judgment.get("id"): {
            key: analytic_judgment.get(key)
            for key in (
                "id",
                "statement",
                "confidence",
                "basis",
                "relatedAlternativeHypothesisIds",
                "changeCondition",
            )
        }
    }
    if actual_markdown_judgments != expected_markdown_judgments:
        error(
            "cases/ch25-structured-analysis-attribution-example.md: central "
            "Analytic Judgment rendering differs from the canonical fixture"
        )
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
    phone_mutations = ("0312345678", "+819012345678", "819012345678", "14155552671")
    for mutation in phone_mutations:
        if not PHONE_RE.search(mutation):
            error(f"fixture safety regression: compact telephone mutation was accepted: {mutation!r}")
    for non_phone in ("20260729101500", "0000000000", "+81-2026-0729-1015"):
        if PHONE_RE.search(non_phone):
            error(f"fixture safety regression: non-telephone numeric value was rejected: {non_phone!r}")
    for mutation in ("例え.テスト", "real。com"):
        if not is_unicode_domain_candidate(mutation):
            error(f"fixture safety regression: Unicode/IDN domain mutation was accepted: {mutation!r}")
    adjacent_match = UNICODE_SEPARATOR_ASCII_HOST_RE.search("接続先はreal。comです")
    if adjacent_match is None or adjacent_match.group("host") != "real。com":
        error("fixture safety regression: adjacent Unicode-separator host was not tokenized")
    adjacent_ascii_match = HOSTNAME_RE.search("接続先はreal.comです")
    if adjacent_ascii_match is None or adjacent_ascii_match.group("host") != "real.com":
        error("fixture safety regression: adjacent ASCII-dot host was not tokenized")
    punycode_match = HOSTNAME_RE.search("接続先はxn--r8jz45g.xn--zckzahです")
    if punycode_match is None or punycode_match.group("host") != "xn--r8jz45g.xn--zckzah":
        error("fixture safety regression: adjacent punycode host was not tokenized")
    contextual_domain_regressions = {
        "接続先は例え.comです": ["例え.com"],
        "接続先は例え。世界です": ["例え。世界"],
        "接続先はпример.РФです": ["пример.РФ"],
        "接続先: 例え。テスト": ["例え。テスト"],
        "ドメインは 例え。テスト": ["例え。テスト"],
        "合成接続先は例え.テスト.exampleです": ["例え.テスト.example"],
        "接続先は例え.exampleを使用する": ["例え.example"],
        "接続先は例え.example/pathです": ["例え.example"],
        "URL: https://例え.example/path": ["例え.example"],
        "参照先はhttps://xn--r8jz45g.example/a?b=1です": [
            "xn--r8jz45g.example"
        ],
        "接続先はhttps://例え.exampleです": ["例え.example"],
        "URL: https://例え.example、確認する": ["例え.example"],
        "URL: http://192.0.2.1/path": ["192.0.2.1"],
        "接続先はhttp://192.0.2.1です": ["192.0.2.1"],
        "URL: http://192.0.2.1、確認する": ["192.0.2.1"],
        "接続先は例え.example。次に確認する": ["例え.example"],
        "URL: https://safe.example名@evil.com/path": ["evil.com"],
    }
    for mutation, expected_hosts in contextual_domain_regressions.items():
        if list(contextual_domain_hosts(mutation)) != expected_hosts:
            error(
                "fixture safety regression: contextual host tokenization drifted: "
                f"{mutation!r}"
            )
    email_domain_regressions = {
        "連絡先はuser@safe.exampleです": ["safe.example"],
        "連絡先はuser@evil.comです": ["evil.com"],
        "連絡先はuser@safe.example.localです": ["safe.example.local"],
    }
    for mutation, expected_hosts in email_domain_regressions.items():
        normalized_mutation = normalize_for_host_scanning(mutation)
        if list(email_domain_hosts(normalized_mutation)) != expected_hosts:
            error(
                "fixture safety regression: email domain tokenization drifted: "
                f"{mutation!r}"
            )
    general_host_regressions = (
        "接続先として例え.comです",
        "通信先は例え.comです",
        "参照先として例え。世界です",
        "ドメイン名は例え.comです",
        "アクセス先は例え。世界です",
        "観測値は例え.comです",
        "URL例は例え.comです",
        "接続先->例え.comです",
        "通信先は例え.aiです",
        "通信先は例え.deです",
        "通信先は例え.frです",
        "観測した例え.comが応答した",
        "観測値は例え.com。次へ進む",
        "観測値は例え.comも応答した",
        "観測値は例え.comより取得した",
        "観測値は例え.comまで到達した",
        "観測値は例え.ｃｏｍ経由で取得した",
        "観測値は例え.c\u200bom経由で取得した",
        "観測値は例え.vermo\u0308gensberater経由で取得した",
        "観測値は例え.preß経由で取得した",
    )
    for mutation in general_host_regressions:
        compatibility_mutation = normalize_for_host_scanning(mutation)
        match = GENERAL_HOST_CANDIDATE_RE.search(compatibility_mutation)
        if match is None or not is_unicode_domain_candidate(
            general_host_from_match(match)
        ):
            error(
                "fixture safety regression: Japanese-adjacent IDN was not tokenized: "
                f"{mutation!r}"
            )
    for mutation in ("例え.テスト", "例え.世界", "例え.ｃｏｍ"):
        if not is_unicode_domain_candidate(mutation):
            error(f"fixture safety regression: bare IDN was not recognized: {mutation!r}")
    if is_unicode_domain_candidate("これは。テスト"):
        error("fixture safety regression: Japanese prose was treated as a Unicode/IDN domain")
    if is_unicode_domain_candidate("検証.テストケースを実施する"):
        error("fixture safety regression: ordinary dotted Japanese prose was treated as an IDN")
    for prose in ("検証.テストを実施する", "検証。テストです"):
        if GENERAL_HOST_CANDIDATE_RE.search(prose):
            error(
                "fixture safety regression: documentation-only IDN tokenization "
                f"treated ordinary prose as a host: {prose!r}"
            )
    for extended_reserved_host in (
        "例え.example.local",
        "例え.example。local",
        "例え.test.internal",
    ):
        match = RESERVED_SUFFIX_EXTENSION_RE.search(extended_reserved_host)
        if match is None or normalize_unicode_host(match.group("host")) != (
            normalize_unicode_host(extended_reserved_host)
        ):
            error(
                "fixture safety regression: reserved suffix extension was not "
                f"tokenized as a complete invalid host: {extended_reserved_host!r}"
            )
    for sentence_terminated_host in (
        "例え.example。次に確認する",
        "例え.example．次に確認する",
        "例え.example｡次に確認する",
    ):
        if RESERVED_SUFFIX_EXTENSION_RE.search(sentence_terminated_host):
            error(
                "fixture safety regression: Japanese sentence text after a "
                f"reserved host was treated as an additional label: {sentence_terminated_host!r}"
            )
    for mutation in ("\u200b", "\ufeff", "ROLE-2026-025-001\u200b", "role-001"):
        if is_valid_identity(mutation):
            error(f"fixture identity regression: unsafe identity was accepted: {mutation!r}")
    for canonical_identity in ("ROLE-2026-025-001", "ALT-2026-025-001"):
        if not is_valid_identity(canonical_identity):
            error(
                "fixture identity regression: canonical identity was rejected: "
                f"{canonical_identity!r}"
            )
    identity_collision_dataset = {
        "syntheticEntities": {
            "organizations": [{"id": "ORG-2026-025-001"}],
            "roles": [{"id": "ORG-2026-025-001"}],
        }
    }
    if global_owner_identity_collisions(identity_collision_dataset) != {
        "ORG-2026-025-001": [
            "syntheticEntities.organizations[0]",
            "syntheticEntities.roles[0]",
        ]
    }:
        error(
            "fixture identity regression: cross-collection owning-record "
            "collision was not detected"
        )
    singleton_collision_dataset = {
        "decision": {"id": "DEC-2026-025"},
        "reassessment": {"id": "DEC-2026-025"},
    }
    if global_owner_identity_collisions(singleton_collision_dataset) != {
        "DEC-2026-025": ["decision", "reassessment"]
    }:
        error(
            "fixture identity regression: singleton owning-record collision "
            "was not detected"
        )
    if declared_identity_key_for_object_path("undeclaredIdentityObject") is not None:
        error("fixture identity regression: undeclared identity object path was accepted")

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
    iana_tlds = source_items.get("SRC-IANA-TLD-001", {})
    if iana_tlds.get("version") != IANA_TLD_SNAPSHOT_VERSION:
        error("references/sources.json: IANA TLD snapshot version drifted")
    if iana_tlds.get("url") != "https://data.iana.org/TLD/tlds-alpha-by-domain.txt":
        error("references/sources.json: IANA TLD snapshot must use the official data URL")
    if IANA_TLD_SNAPSHOT_SHA256 not in iana_tlds.get("notes", ""):
        error("references/sources.json: IANA TLD snapshot digest is missing from notes")
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
