#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import ipaddress
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.sync_book_site import (  # noqa: E402
    SitePageRegistryError,
    parse_registry_data,
)
import scripts.sync_site_source as base  # noqa: E402

ERRORS: list[str] = []
AUDITED_ARTIFACT_REVISION = "5a31db5a15a7583218b0bd49ca1a285d9348f0b0"
AUDITED_ARTIFACT_SHA256 = {
    "detections/cloud_identity/det_2026_017_001.json": (
        "119694a96b9ac68b4ecbf8a946bbffb1bbd9cda1416720a0c42346961c5f88e8"
    ),
    "scripts/replay_chapter17_detection.py": (
        "e04d0829bc01e46fcb3a15ec05ed83de18c1a7c14139f2dfa6ff0d0ffbc16cfe"
    ),
}
RESERVED_DOMAIN_SUFFIXES = (".example", ".test", ".invalid")
DOCUMENTATION_NETWORKS = tuple(
    ipaddress.ip_network(cidr)
    for cidr in (
        "192.0.2.0/24",
        "198.51.100.0/24",
        "203.0.113.0/24",
        "2001:db8::/32",
    )
)
HOST_RE = re.compile(
    r"^(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}$"
)
URL_RE = re.compile(r"https?://[^\s\"'<>)}]+", re.IGNORECASE)
IPV4_RE = re.compile(r"(?<![0-9.])(?:\d{1,3}\.){3}\d{1,3}(?![0-9.])")
IPV6_RE = re.compile(
    r"(?<![0-9A-Fa-f:.])(?=[0-9A-Fa-f:]*:)[0-9A-Fa-f:]{2,}(?![0-9A-Fa-f:.])"
)
SAFE_DOTTED_VALUES = {"Invoice.Read.All", "Ledger.Export.All"}
SENSITIVE_PATTERNS = (
    re.compile(r"-----BEGIN " + r"(?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"AK" + r"IA[0-9A-Z]{16}"),
    re.compile(r"gh" + r"[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{12,}"),
    re.compile(r"(?i)\b(?:password|client_secret)\s*[:=]\s*\S+"),
    re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE),
    re.compile(r"(?<!\d)\+?\d{1,3}[ -]?\d{2,4}[ -]?\d{3,4}[ -]?\d{4}(?!\d)"),
)


def error(message: str) -> None:
    ERRORS.append(message)


def read_text(relative: str) -> str:
    path = ROOT / relative
    if not path.is_file():
        error(f"missing required file: {relative}")
        return ""
    return path.read_text(encoding="utf-8")


def load_json(relative: str) -> dict:
    text = read_text(relative)
    if not text:
        return {}
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        error(f"{relative}: invalid JSON: {exc}")
        return {}
    if not isinstance(data, dict):
        error(f"{relative}: root must be an object")
        return {}
    return data


def check_audited_artifact_hashes() -> None:
    for relative, expected in AUDITED_ARTIFACT_SHA256.items():
        path = ROOT / relative
        if not path.is_file():
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            error(
                f"{relative}: sha256 {actual} does not match audited revision "
                f"{AUDITED_ARTIFACT_REVISION} ({expected})"
            )


def require_tokens(relative: str, text: str, tokens: tuple[str, ...]) -> None:
    for token in tokens:
        if token not in text:
            error(f"{relative}: missing required token {token!r}")


def iter_strings(value: object):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from iter_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from iter_strings(item)


def is_reserved_host(host: str) -> bool:
    normalized = host.rstrip(".").lower()
    return normalized.endswith(RESERVED_DOMAIN_SUFFIXES)


def is_documentation_ip(raw: str) -> bool:
    try:
        address = ipaddress.ip_address(raw)
    except ValueError:
        return False
    return any(address in network for network in DOCUMENTATION_NETWORKS)


def normalize_bare_host(value: str) -> str | None:
    candidate = value.strip()
    if candidate in SAFE_DOTTED_VALUES:
        return None
    if ":" in candidate and candidate.rsplit(":", 1)[1].isdigit():
        candidate = candidate.rsplit(":", 1)[0]
    candidate = candidate.rstrip(".").lower()
    return candidate if HOST_RE.fullmatch(candidate) else None


def unsafe_value_reasons(value: str) -> list[str]:
    reasons: list[str] = []
    for pattern in SENSITIVE_PATTERNS:
        if pattern.search(value):
            reasons.append(f"sensitive pattern {pattern.pattern!r}")

    for raw_url in URL_RE.findall(value):
        host = urlparse(raw_url).hostname or ""
        if not is_reserved_host(host):
            reasons.append(f"external URL host {host!r}")

    bare_host = normalize_bare_host(value)
    if bare_host is not None and not is_reserved_host(bare_host):
        reasons.append(f"non-reserved bare host {bare_host!r}")

    for raw_ip in set(IPV4_RE.findall(value) + IPV6_RE.findall(value)):
        try:
            address = ipaddress.ip_address(raw_ip)
        except ValueError:
            continue
        if not is_documentation_ip(str(address)):
            reasons.append(f"non-documentation IP {raw_ip!r}")
    return reasons


def main() -> int:
    required_files = (
        "manuscript/17-detection-engineering.md",
        "templates/detection-validation.md",
        "cases/ch17-detection-validation-example.md",
        "cases/fixtures/ch17-detection-engineering-fixture.md",
        "cases/fixtures/ch17-detection-engineering-fixture.json",
        "detections/cloud_identity/det_2026_017_001.json",
        "scripts/replay_chapter17_detection.py",
        "site-pages.json",
        "artifact-index.md",
        "figure-index.md",
        "index.md",
        "book-config.json",
        "references/sources.json",
        "package.json",
    )
    for relative in required_files:
        if not (ROOT / relative).is_file():
            error(f"missing required file: {relative}")
    check_audited_artifact_hashes()

    config = load_json("book-config.json")
    chapters = config.get("structure", {}).get("chapters", [])
    chapter_config = next(
        (
            item
            for item in chapters
            if isinstance(item, dict) and item.get("id") == "ch17-detection-engineering"
        ),
        None,
    )
    expected_objectives = [
        "Detection Hypothesisを作成できる",
        "Data Requirementを定義できる",
        "Detection Validation Recordを作成できる",
    ]
    if chapter_config is None:
        error("book-config.json: missing ch17-detection-engineering")
    else:
        objectives = chapter_config.get("objectives", [])
        if objectives != expected_objectives:
            error(
                "book-config.json: chapter 17 objectives must remain exactly the configured three learning objectives"
            )

    chapter_path = "manuscript/17-detection-engineering.md"
    chapter = read_text(chapter_path)
    require_tokens(
        chapter_path,
        chapter,
        (
            "## この章の位置付け",
            "## 学習目標",
            "## 前提知識",
            "### OWN",
            "### BRIDGE",
            "### DELEGATE",
            "Telemetry absenceはEvent absenceではない。",
            "Positive / Negative / Benign-near-miss",
            "Detection-as-Code",
            "precision",
            "recall",
            "base rate",
            "Good example",
            "Bad example",
            "../templates/detection-validation.md",
            "../cases/ch17-detection-validation-example.md",
            "../cases/fixtures/ch17-detection-engineering-fixture.md",
            "../cases/fixtures/ch17-detection-engineering-fixture.json",
            "DR-DET-2026-001",
            "RO-DET-2026-001",
            "DVR-2026-017-001",
            "CASE-2026-001",
            "DEC-2026-001",
            "FIND-2026-002",
            "HUNT-2026-001",
            "TH-DET-2026-001",
            "OBS-DET-2026-001",
            "TEL-DET-2026-001",
            "DET-2026-017-001",
            "FIX-2026-017-POS",
            "FIX-2026-017-NEG",
            "FIX-2026-017-BNM",
            "TRI-DET-2026-001",
            "HO-DET-2026-001",
            "CTRL-DET-2026-001",
            "REA-DET-2026-001",
            "SRC-ATTACK-001",
            "SRC-ATTACK-DS-001",
            "SRC-ATTACK-DET-001",
            "SRC-SIGMA-001",
            "SRC-IR-001",
            "F-17-01",
            "F-17-02",
            "T-17-01",
            f"https://github.com/itdojp/white-hat-cyber-intelligence-book/blob/{AUDITED_ARTIFACT_REVISION}/detections/cloud_identity/det_2026_017_001.json",
            f"https://github.com/itdojp/white-hat-cyber-intelligence-book/blob/{AUDITED_ARTIFACT_REVISION}/scripts/replay_chapter17_detection.py",
        ),
    )
    forbidden_terms = (
        "credential theft",
        "C2",
        "malware sample",
        "実Credentialを使って",
        "第三者Tenantへ",
        "Detection Validation Recordを、`CASE-DET-2026-001`として作成する",
        "/blob/main/detections/cloud_identity/det_2026_017_001.json",
        "/blob/main/scripts/replay_chapter17_detection.py",
    )
    for term in forbidden_terms:
        if term in chapter:
            error(f"{chapter_path}: contains forbidden unsafe term {term!r}")

    template_path = "templates/detection-validation.md"
    template = read_text(template_path)
    require_tokens(
        template_path,
        template,
        (
            "Artifact ID",
            "Detection Validation Record ID",
            "Case ID",
            "Decision Requirement ID",
            "Response Objective ID",
            "Detection ID",
            "Related Case Map Case ID",
            "Related Case Map Decision ID",
            "Related Case Map Detection ID",
            "Detection relationship",
            "Related Case Map Fixture ID",
            "Related Case Map Control ID",
            "ATT&CK mapping is not coverage proof",
            "Telemetry ID",
            "Time contract",
            "Identity contract",
            "Fixture ID",
            "Negative Finding ID",
            "Coverage",
            "Gap",
            "Permitted conclusion",
            "Detectability",
            "Test success",
            "Triageability",
            "Decision latency contribution",
            "Precision assumption",
            "Recall assumption",
            "Base rate note",
            "Control ID",
            "Reassessment ID",
            "Source Note IDs",
            "Detection backlog inputs",
            "Finding / Hunt / Incident / CTI",
            "syntheticOnly",
            "offlineOnly",
        ),
    )

    example_path = "cases/ch17-detection-validation-example.md"
    example = read_text(example_path)
    require_tokens(
        example_path,
        example,
        (
            "CASE-DET-2026-001",
            "| Detection Validation Record ID | `DVR-2026-017-001` |",
            "CASE-2026-001",
            "DEC-2026-001",
            "DET-2026-001",
            "FIX-CONSENT-001",
            "CTRL-2026-003",
            "refines",
            "DR-DET-2026-001",
            "RO-DET-2026-001",
            "TH-DET-2026-001",
            "OBS-DET-2026-001",
            "OBS-DET-2026-002",
            "TEL-DET-2026-001",
            "TEL-DET-2026-002",
            "TEL-DET-2026-003",
            "DET-2026-017-001",
            "FIX-2026-017-POS",
            "FIX-2026-017-NEG",
            "FIX-2026-017-BNM",
            "EVD-DET-2026-001",
            "| `EVD-DET-2026-004` | `GAP-DET-2026-001` |",
            "NEG-DET-2026-001",
            "TRI-DET-2026-001",
            "HO-DET-2026-001",
            "CTRL-DET-2026-001",
            "CTRL-DET-2026-002",
            "REA-DET-2026-001",
            "ATT&CK mapping is not coverage proof | Yes",
            "Telemetry absenceとEvent absenceを混同しない。",
            "No alert",
            "Alert",
            "再現可能な時刻証跡を付けていない教材上の想定値",
            "Rule件数やAlert件数を成果指標にしない",
            "判定不能",
            "実環境全体で同種行動が存在しないとは結論しない",
            "SRC-SIGMA-001",
            "SRC-IR-001",
            "DBI-DET-2026-001",
            "DBI-DET-2026-004",
            "FIND-2026-002",
            "HUNT-2026-001",
            "detections/cloud_identity/det_2026_017_001.json",
            "scripts/replay_chapter17_detection.py",
            "Target behavior event presence",
        ),
    )

    fixture_doc_path = "cases/fixtures/ch17-detection-engineering-fixture.md"
    fixture_doc = read_text(fixture_doc_path)
    require_tokens(
        fixture_doc_path,
        fixture_doc,
        (
            "FIX-2026-017-POS",
            "FIX-2026-017-NEG",
            "FIX-2026-017-BNM",
            "GAP-DET-2026-001",
            "オフライン専用",
            "Telemetry absenceはEvent absenceではない",
            "scripts/check_chapter17_contract.py",
            "scripts/replay_chapter17_detection.py",
            "detections/cloud_identity/det_2026_017_001.json",
            f"https://github.com/itdojp/white-hat-cyber-intelligence-book/blob/{AUDITED_ARTIFACT_REVISION}/detections/cloud_identity/det_2026_017_001.json",
            AUDITED_ARTIFACT_REVISION,
        ),
    )
    for term in (
        "/blob/main/detections/cloud_identity/det_2026_017_001.json",
        "/blob/main/scripts/replay_chapter17_detection.py",
    ):
        if term in fixture_doc:
            error(f"{fixture_doc_path}: contains mutable artifact link {term!r}")

    fixture_path = ROOT / "cases/fixtures/ch17-detection-engineering-fixture.json"
    try:
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        error(f"{fixture_path}: invalid JSON: {exc}")
        fixture = {}

    if fixture.get("caseId") != "CASE-DET-2026-001":
        error("fixture: caseId mismatch")
    if fixture.get("detectionValidationRecordId") != "DVR-2026-017-001":
        error("fixture: detectionValidationRecordId mismatch")
    if fixture.get("relatedCaseMapCaseId") != "CASE-2026-001":
        error("fixture: relatedCaseMapCaseId mismatch")
    if fixture.get("relatedCaseMapDecisionId") != "DEC-2026-001":
        error("fixture: relatedCaseMapDecisionId mismatch")
    if fixture.get("decisionRequirementId") != "DR-DET-2026-001":
        error("fixture: decisionRequirementId mismatch")
    if fixture.get("responseObjectiveId") != "RO-DET-2026-001":
        error("fixture: responseObjectiveId mismatch")
    if fixture.get("detectionId") != "DET-2026-017-001":
        error("fixture: detectionId mismatch")
    expected_case_map = {
        "detectionId": "DET-2026-001",
        "relationship": "refines",
        "fixtureId": "FIX-CONSENT-001",
        "controlId": "CTRL-2026-003",
        "telemetryMap": [
            {
                "caseMapTelemetryId": "TEL-2026-001",
                "chapter17TelemetryId": "TEL-DET-2026-001",
            },
            {
                "caseMapTelemetryId": "TEL-2026-004",
                "chapter17TelemetryId": "TEL-DET-2026-003",
            },
        ],
    }
    if fixture.get("relatedCaseMap") != expected_case_map:
        error("fixture: relatedCaseMap must preserve the Chapter 1 detection/fixture/control refinement")
    if fixture.get("syntheticOnly") is not True or fixture.get("offlineOnly") is not True:
        error("fixture: syntheticOnly and offlineOnly must both be true")
    if fixture.get("attackMappingCoverageProof") is not False:
        error("fixture: attackMappingCoverageProof must be false")
    backlog_inputs = fixture.get("detectionBacklogInputs")
    if backlog_inputs != [
        {
            "backlogItemId": "DBI-DET-2026-001",
            "inputType": "finding",
            "relatedSourceId": "FIND-2026-002",
            "disposition": "accept",
        },
        {
            "backlogItemId": "DBI-DET-2026-002",
            "inputType": "hunt",
            "relatedSourceId": "HUNT-2026-001",
            "disposition": "accept",
        },
        {
            "backlogItemId": "DBI-DET-2026-003",
            "inputType": "incident",
            "relatedSourceId": None,
            "disposition": "defer-no-input-in-synthetic-case",
        },
        {
            "backlogItemId": "DBI-DET-2026-004",
            "inputType": "cti",
            "relatedSourceId": None,
            "disposition": "defer-no-input-in-synthetic-case",
        },
    ]:
        error("fixture: detection backlog inputs must preserve Finding/Hunt inputs and explicit Incident/CTI absence")
    safety = fixture.get("safetyAssertions", {})
    for key in (
        "noMalwareOrC2",
        "noCredentialTheft",
        "noRealCredentials",
        "noPII",
        "noExternalTargets",
    ):
        if safety.get(key) is not True:
            error(f"fixture: safetyAssertions.{key} must be true")
    if safety.get("allowedDomains") != list(RESERVED_DOMAIN_SUFFIXES):
        error(
            "fixture: safetyAssertions.allowedDomains must be exactly "
            f"{list(RESERVED_DOMAIN_SUFFIXES)!r}"
        )

    telemetry_contracts = {
        item.get("id"): item
        for item in fixture.get("telemetryContracts", [])
        if isinstance(item, dict)
    }
    if set(telemetry_contracts) != {
        "TEL-DET-2026-001",
        "TEL-DET-2026-002",
        "TEL-DET-2026-003",
    }:
        error("fixture: telemetryContracts must contain exactly the three configured telemetry IDs")
    sign_in_contract = telemetry_contracts.get("TEL-DET-2026-003", {})
    if sign_in_contract.get("requiredFields") != [
        "event_time",
        "target_workload_id",
        "result",
    ]:
        error("fixture: sign-in core requiredFields mismatch")
    if sign_in_contract.get("optionalEnrichmentFields") != [
        "credential_state",
        "source_label",
    ]:
        error("fixture: sign-in optionalEnrichmentFields mismatch")
    if sign_in_contract.get("coverage") != "partial-optional-enrichment":
        error("fixture: sign-in coverage must identify partial optional enrichment")

    triage_contract = fixture.get("triage", {})
    if triage_contract.get("triageId") != "TRI-DET-2026-001":
        error("fixture: triageId mismatch")
    if triage_contract.get("expectedCategories") != [
        "Escalate",
        "Approved change",
        "Needs telemetry gap review",
    ]:
        error("fixture: triage expectedCategories mismatch")
    if triage_contract.get("mustInclude") != [
        "case_id",
        "detection_id",
        "evidence_ids",
        "scope_delta",
        "change_ticket_status",
        "target_workload_id",
        "coverage_statement",
        "correlation_state",
    ]:
        error("fixture: triage mustInclude contract mismatch")

    fixtures = fixture.get("fixtures", [])
    if not isinstance(fixtures, list) or len(fixtures) != 3:
        error("fixture: must contain exactly three configured fixtures")
        fixtures = []
    fixture_types = {item.get("type"): item for item in fixtures if isinstance(item, dict)}
    positive = fixture_types.get("positive")
    negative = fixture_types.get("negative")
    benign = fixture_types.get("benign_near_miss")
    if positive is None or negative is None or benign is None:
        error("fixture: positive, negative, and benign_near_miss fixtures are all required")
    else:
        expectations = [
            (
                positive,
                "FIX-2026-017-POS",
                "present",
                "present",
                "absent",
                "alert",
                "Escalate",
            ),
            (
                negative,
                "FIX-2026-017-NEG",
                "present",
                "absent",
                "absent",
                "no_alert",
                None,
            ),
            (
                benign,
                "FIX-2026-017-BNM",
                "present",
                "present",
                "present",
                "no_alert",
                "Approved change",
            ),
        ]
        for item, fixture_id, tel, event, benign_ctx, outcome, triage_category in expectations:
            if item.get("fixtureId") != fixture_id:
                error(f"fixture: expected {fixture_id} for type {item.get('type')}")
            if item.get("telemetryPresence") != tel:
                error(f"fixture {fixture_id}: telemetryPresence must be {tel}")
            if item.get("targetEventPresence") != event:
                error(f"fixture {fixture_id}: targetEventPresence must be {event}")
            if item.get("benignNearMissContext") != benign_ctx:
                error(f"fixture {fixture_id}: benignNearMissContext must be {benign_ctx}")
            if item.get("expectedOutcome") != outcome:
                error(f"fixture {fixture_id}: expectedOutcome must be {outcome}")
            expected_severity = {
                "FIX-2026-017-POS": "critical",
                "FIX-2026-017-NEG": "none",
                "FIX-2026-017-BNM": "informational",
            }[fixture_id]
            if item.get("expectedSeverity") != expected_severity:
                error(f"fixture {fixture_id}: expectedSeverity must be {expected_severity}")
            if item.get("expectedTriageCategory") != triage_category:
                error(
                    f"fixture {fixture_id}: expectedTriageCategory must be {triage_category!r}"
                )
            if not isinstance(item.get("records"), list) or not item["records"]:
                error(f"fixture {fixture_id}: records must be a non-empty list")
            if item.get("availableTelemetryIds") != [
                "TEL-DET-2026-001",
                "TEL-DET-2026-002",
                "TEL-DET-2026-003",
            ]:
                error(f"fixture {fixture_id}: availableTelemetryIds mismatch")

        candidate_counts = {}
        for item in (positive, negative, benign):
            candidate_counts[item["fixtureId"]] = sum(
                1
                for record in item.get("records", [])
                if isinstance(record, dict)
                and record.get("telemetryId") == "TEL-DET-2026-001"
                and record.get("eventType") == "admin_consent_granted"
            )
        if candidate_counts != {
            "FIX-2026-017-POS": 1,
            "FIX-2026-017-NEG": 0,
            "FIX-2026-017-BNM": 1,
        }:
            error(
                "fixture: negative must omit the target consent event while the "
                "positive and benign-near-miss fixtures each contain one"
            )

    gap = fixture.get("coverageGapExample", {})
    if gap.get("gapId") != "GAP-DET-2026-001":
        error("fixture: coverageGapExample.gapId mismatch")
    if (
        gap.get("telemetryPresence") != "absent"
        or gap.get("targetEventPresence") != "unknown"
        or gap.get("benignNearMissContext") != "unknown"
    ):
        error("fixture: coverageGapExample must distinguish telemetry absence from unknown event presence")
    permitted = gap.get("permittedConclusion", "")
    expected_gap_conclusion = (
        "Decision is indeterminate; event absence cannot be concluded."
    )
    if permitted != expected_gap_conclusion:
        error(
            "fixture: coverageGapExample permittedConclusion must preserve "
            "indeterminate state and prohibit an event-absence conclusion"
        )
    expected_gap_replay = {
        "sourceFixtureId": "FIX-2026-017-POS",
        "missingTelemetryIds": ["TEL-DET-2026-002"],
        "expectedOutcome": "indeterminate",
        "expectedSeverity": "none",
        "expectedTriageCategory": "Needs telemetry gap review",
    }
    for key, expected in expected_gap_replay.items():
        if gap.get(key) != expected:
            error(f"fixture: coverageGapExample.{key} must be {expected!r}")

    incident_handoff = fixture.get("incidentHandoff", {})
    if incident_handoff.get("handoffId") != "HO-DET-2026-001":
        error("fixture: incidentHandoff.handoffId mismatch")
    if incident_handoff.get("requiredFields") != [
        "case_id",
        "detection_id",
        "evidence_ids",
        "coverage",
        "gap",
        "permitted_conclusion",
    ]:
        error("fixture: incidentHandoff.requiredFields contract mismatch")

    for value in iter_strings(fixture):
        for reason in unsafe_value_reasons(value):
            error(f"fixture: unsafe synthetic value {value!r}: {reason}")

    safety_mutations = (
        "https://public.example.org/path",
        "HTTP://example.com/path",
        "EXAMPLE.COM",
        "example.com:443",
        "example.com.",
        "https://例え.テスト/path",
        "8.8.8.8",
        "2001:4860:4860::8888",
        "AK" + "IAIOSFODNN7EXAMPLE",
        "ghp" + "_abcdefghijklmnopqrstuvwxyz123456",
        "Bearer eyJhbGciOiJIUzI1NiJ9.synthetic",
        "password=not-a-real-password",
        "+81 90 1234 5678",
        "09012345678",
    )
    for mutation in safety_mutations:
        if not unsafe_value_reasons(mutation):
            error(f"fixture safety regression: unsafe mutation was accepted: {mutation!r}")
    safe_mutations = (
        "https://portal.example/path",
        "billing-approval.example.",
        "billing-approval.example:443",
        "192.0.2.10",
        "2001:db8::10",
        "Invoice.Read.All",
    )
    for mutation in safe_mutations:
        reasons = unsafe_value_reasons(mutation)
        if reasons:
            error(f"fixture safety regression: safe mutation {mutation!r} was rejected: {reasons}")

    rule = load_json("detections/cloud_identity/det_2026_017_001.json")
    if rule.get("detectionId") != fixture.get("detectionId"):
        error("detection rule: detectionId must match the fixture set")
    if rule.get("syntheticOnly") is not True or rule.get("offlineOnly") is not True:
        error("detection rule: syntheticOnly and offlineOnly must both be true")
    if rule.get("caseId") != "CASE-DET-2026-001":
        error("detection rule: caseId mismatch")
    expected_rule_case_map = dict(expected_case_map)
    expected_rule_case_map["versionBoundary"] = (
        "Chapter 17 refines the Chapter 1 case-map entry; it does not supersede or "
        "redeploy that synthetic rule."
    )
    if rule.get("relatedCaseMap") != expected_rule_case_map:
        error("detection rule: relatedCaseMap refinement contract mismatch")
    if rule.get("requiredTelemetryIds") != [
        "TEL-DET-2026-001",
        "TEL-DET-2026-002",
    ]:
        error("detection rule: requiredTelemetryIds mismatch")
    if rule.get("optionalTelemetryIds") != ["TEL-DET-2026-003"]:
        error("detection rule: optionalTelemetryIds mismatch")
    if rule.get("candidate", {}).get("eventType") != "admin_consent_granted":
        error("detection rule: candidate event type mismatch")
    if rule.get("severityEscalation", {}).get("withinMinutes") != 30:
        error("detection rule: severity escalation window must remain 30 minutes")
    if rule.get("outcomes") != {
        "unapprovedScopeChange": "alert",
        "approvedScopeChange": "no_alert",
        "noCandidateEvent": "no_alert",
        "telemetryGap": "indeterminate",
    }:
        error("detection rule: outcomes must preserve alert, no-alert, and telemetry-gap states")

    registry = load_json("site-pages.json")
    try:
        registry = parse_registry_data(registry)
    except SitePageRegistryError as exc:
        error(f"site-pages.json: schema contract violation: {exc}")
        registry = {}

    expected_registry_pages = {
        (
            "manuscript/17-detection-engineering.md",
            "chapters/chapter-17/index.md",
        ),
        (
            "cases/ch17-detection-validation-example.md",
            "cases/chapter-17-detection-validation/index.md",
        ),
        (
            "cases/fixtures/ch17-detection-engineering-fixture.md",
            "cases/fixtures/ch17-detection-engineering-fixture/index.md",
        ),
    }
    actual_pages = {
        (item.get("source"), item.get("destination"))
        for item in registry.get("pages", [])
        if isinstance(item, dict)
    }
    missing_pages = expected_registry_pages - actual_pages
    if missing_pages:
        error(f"site-pages.json: missing chapter 17 publication pages: {sorted(missing_pages)}")
    expected_static_files = {
        (
            "cases/fixtures/ch17-detection-engineering-fixture.json",
            "downloads/ch17-detection-engineering-fixture.json",
        )
    }
    actual_static_files = {
        (item.get("source"), item.get("destination"))
        for item in registry.get("staticFiles", [])
        if isinstance(item, dict)
    }
    missing_static_files = expected_static_files - actual_static_files
    if missing_static_files:
        error(
            "site-pages.json: missing chapter 17 static artifact: "
            f"{sorted(missing_static_files)}"
        )
    if "cases" not in registry.get("canonicalDirectories", []):
        error("site-pages.json: canonicalDirectories must include cases for fixture publication")

    base_pages = {(page.source, page.destination) for page in base.PAGES}
    if (
        "templates/detection-validation.md",
        "templates/detection-validation/index.md",
    ) not in base_pages:
        error("sync_site_source.py: base publication for detection-validation template is missing")

    artifact_index = read_text("artifact-index.md")
    require_tokens(
        "artifact-index.md",
        artifact_index,
        (
            "ART-05",
            "Detection Validation Record",
            "templates/detection-validation.md",
            "cases/ch17-detection-validation-example.md",
            "cases/fixtures/ch17-detection-engineering-fixture.json",
        ),
    )

    figure_index = read_text("figure-index.md")
    require_tokens(
        "figure-index.md",
        figure_index,
        (
            "F-17-01",
            "F-17-02",
            "T-17-01",
            "manuscript/17-detection-engineering.md",
        ),
    )

    home = read_text("index.md")
    require_tokens(
        "index.md",
        home,
        (
            "manuscript/17-detection-engineering.md",
            "templates/detection-validation.md",
            "cases/ch17-detection-validation-example.md",
            "cases/fixtures/ch17-detection-engineering-fixture.md",
        ),
    )

    sources = load_json("references/sources.json")
    src_attack = next(
        (
            item
            for item in sources.get("sources", [])
            if isinstance(item, dict) and item.get("id") == "SRC-ATTACK-001"
        ),
        None,
    )
    if src_attack is None:
        error("references/sources.json: missing SRC-ATTACK-001")
    elif 17 not in src_attack.get("chapters", []):
        error("references/sources.json: SRC-ATTACK-001 must map to chapter 17")
    for source_id in ("SRC-ATTACK-DS-001", "SRC-ATTACK-DET-001", "SRC-SIGMA-001", "SRC-IR-001"):
        source = next(
            (
                item
                for item in sources.get("sources", [])
                if isinstance(item, dict) and item.get("id") == source_id
            ),
            None,
        )
        if source is None:
            error(f"references/sources.json: missing {source_id}")
            continue
        if 17 not in source.get("chapters", []):
            error(f"references/sources.json: {source_id} must map to chapter 17")
        if source.get("checkedAt") != "2026-08-03":
            error(f"references/sources.json: {source_id} checkedAt must be 2026-08-03")

    package = load_json("package.json")
    scripts = package.get("scripts", {})
    if scripts.get("check:chapter17") != "python3 scripts/check_chapter17_contract.py":
        error("package.json: check:chapter17 command mismatch")
    if scripts.get("check:chapter17-replay") != "python3 scripts/replay_chapter17_detection.py":
        error("package.json: check:chapter17-replay command mismatch")
    if "npm run check:chapter17" not in scripts.get("test", ""):
        error("package.json: test must run check:chapter17")
    if "npm run check:chapter17-replay" not in scripts.get("test", ""):
        error("package.json: test must run check:chapter17-replay")

    for message in ERRORS:
        print(f"ERROR: {message}")
    if ERRORS:
        return 1

    print(
        "chapter 17 contract passed: direct IDs, synthetic offline fixtures, "
        "safe detection-validation template, registry publication, and fail-closed semantics"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
