#!/usr/bin/env python3
from __future__ import annotations

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

ERRORS: list[str] = []


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


def main() -> int:
    required_files = (
        "manuscript/11-web-api-hypothesis.md",
        "templates/web-api-assessment-hypothesis-pack.md",
        "cases/ch11-web-api-assessment-example.md",
        "cases/fixtures/ch11-web-api-assessment-dataset.json",
        "scripts/check_chapter11_contract.py",
        "site-pages.json",
        "artifact-index.md",
        "figure-index.md",
        "index.md",
        "book-config.json",
        "references/sources.json",
        "references/reference-baseline.md",
        "package.json",
    )
    for relative in required_files:
        if not (ROOT / relative).is_file():
            error(f"missing required file: {relative}")

    config = load_json("book-config.json")
    chapters = config.get("structure", {}).get("chapters", [])
    chapter_config = next(
        (
            item
            for item in chapters
            if isinstance(item, dict)
            and item.get("id") == "ch11-web-api-hypothesis"
        ),
        None,
    )
    expected_objectives = [
        "評価仮説を作成できる",
        "証拠を最小化できる",
        "Web/API Assessment Hypothesis Packを作成できる",
    ]
    if chapter_config is None:
        error("book-config.json: missing ch11-web-api-hypothesis")
    elif chapter_config.get("objectives") != expected_objectives:
        error("book-config.json: chapter 11 learning objectives changed unexpectedly")

    chapter_path = "manuscript/11-web-api-hypothesis.md"
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
            "AuthenticationとAuthorization",
            "Object level",
            "Function level",
            "Property level",
            "Session / Token / State transition",
            "Input validationとInjection",
            "SSRFとServer-side trust boundary",
            "Rate・Resource consumption",
            "Inventory、Version、Deprecated API",
            "Business Logic",
            "Error、Cache、Async、Webhook、Idempotency",
            "Multi-tenant",
            "Negative Test",
            "FindingをTelemetryとDetectionへ変換する",
            "Stop condition",
            "Cleanup",
            "ART-11 Web/API Assessment Hypothesis Pack",
            "F-11-01",
            "F-11-02",
            "T-11-01",
            "T-11-02",
            "T-11-03",
            "T-11-04",
            "SRC-WSTG-001",
            "SRC-OWASP-TOP10-001",
            "SRC-API-001",
            "https://itdojp.github.io/pentest-learning-book/part4_api/41_api_basics_and_attack_surface/",
            "https://itdojp.github.io/practical-auth-book/",
            "## 章のまとめ",
            "## 次に学ぶこと",
            "## 参考文献・Source Note ID",
        ),
    )
    for forbidden in (
        "WSTG 5.0を安定版",
        "Negative Testに失敗しなければ安全",
        "外部ServiceへRequestを送る",
    ):
        if forbidden in chapter:
            error(f"{chapter_path}: unsafe or unsupported statement {forbidden!r}")

    template_path = "templates/web-api-assessment-hypothesis-pack.md"
    template = read_text(template_path)
    require_tokens(
        template_path,
        template,
        (
            "Artifact ID | `ART-11`",
            "Case ID",
            "Decision Requirement ID",
            "Asset ID",
            "Actor and Credential Classes",
            "Trust, Tenant, and Server-side Boundaries",
            "Threat Hypothesis ID",
            "Observation Hypothesis ID",
            "Authority / RoE ID",
            "Validation ID",
            "Expected authorized result",
            "Expected denied result",
            "Expected evidence",
            "Stop condition",
            "Cleanup",
            "Evidence ID",
            "Related Observation ID",
            "Related Validation ID",
            "Related Observation Hypothesis ID",
            "Related Telemetry ID",
            "Related Detection ID / planned ID",
            "Telemetry ID",
            "Detection ID",
            "Reassessment ID",
            "Related Finding IDs",
            "Related Detection IDs",
            "Evidence Handling",
            "Redaction status",
            "Retention / disposal date",
            "Disposal owner",
            "Negative Testの不成立をSystem全体の安全性証明として扱わない",
        ),
    )

    example_path = "cases/ch11-web-api-assessment-example.md"
    example = read_text(example_path)
    require_tokens(
        example_path,
        example,
        (
            "CASE-2026-011",
            "DR-2026-011",
            "ROE-2026-011",
            "ASSET-2026-011",
            "TH-2026-011",
            "OBS-2026-011",
            "VAL-2026-011",
            "EVD-2026-011",
            "FIND-2026-011",
            "TEL-2026-011",
            "DET-2026-011",
            "REA-2026-011",
            "悪い仮説から良い仮説へ",
            "| `EVD-2026-012` | `OBS-2026-012` | `VAL-2026-012` | `ROE-2026-011` |",
            "| `VAL-2026-012` | `TH-2026-012` | `OBS-2026-012` |",
            "| `FIND-2026-011` | `TH-2026-012` |",
            "| `TEL-2026-011` | `DET-2026-011` |",
            "| `REA-2026-011` | `FIND-2026-011`, `FIND-2026-012`, `FIND-2026-013` |",
            "この条件ではcross-tenant参照を観測しなかった",
            "全Bypass不在は証明しない",
            "外部通信、Data大量取得、負荷試験、横展開、Credential reuseは行わない",
            "3回以下の再試行確認",
            "tok-analyst-invalid",
            "tenant-blue.example",
            "control-plane.service.test",
            "fixtures/ch11-web-api-assessment-dataset.json",
            "### 5.2 Evidence Handling",
        ),
    )
    if "CASE-2026-001" in example:
        error(f"{example_path}: chapter 11 must not reuse the chapter 1 Case ID")

    secret_patterns = (
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
        re.compile(r"(?:10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}"),
        re.compile(r"192\.168\.\d{1,3}\.\d{1,3}"),
    )
    for pattern in secret_patterns:
        if pattern.search(example):
            error(f"{example_path}: possible real target or secret pattern detected")
    for raw_url in re.findall(r"https?://[^\s`)]+", example):
        host = (urlparse(raw_url).hostname or "").lower()
        if not host.endswith((".example", ".test", ".invalid")):
            error(f"{example_path}: non-reserved URL in synthetic case: {raw_url}")

    fixture_path = "cases/fixtures/ch11-web-api-assessment-dataset.json"
    fixture = load_json(fixture_path)
    for key, expected in (
        ("schemaVersion", "1.0.0"),
        ("fixtureId", "FIXTURE-CH11-001"),
        ("synthetic", True),
        ("readOnly", True),
        ("networkRequired", False),
    ):
        if fixture.get(key) != expected:
            error(f"{fixture_path}: {key} must be {expected!r}")
    authority = fixture.get("authority", {})
    domains = authority.get("permittedDomains", [])
    if not domains or any(
        not isinstance(host, str)
        or not host.endswith((".example", ".test", ".invalid"))
        for host in domains
    ):
        error(f"{fixture_path}: permittedDomains must contain reserved domains only")
    capture_provenance = fixture.get("captureProvenance", {})
    if capture_provenance != {
        "captureComplete": True,
        "exerciseAction": "inspect-recorded-data-only",
        "externalNetworkUsed": False,
        "cleanupComplete": True,
    }:
        error(f"{fixture_path}: capture provenance must make the exercise read-only")
    exercise_records = fixture.get("exerciseRecords", [])
    validations = fixture.get("validations", [])
    record_ids = {
        item.get("recordId")
        for item in exercise_records
        if isinstance(item, dict)
    }
    expected_record_ids = {f"REC-11-{number:03d}" for number in range(1, 7)}
    if record_ids != expected_record_ids:
        error(f"{fixture_path}: expected REC-11-001 through REC-11-006")
    expected_record_validation = {
        "REC-11-001": "VAL-2026-011",
        "REC-11-002": "VAL-2026-011",
        "REC-11-003": "VAL-2026-012",
        "REC-11-004": "VAL-2026-013",
        "REC-11-005": "VAL-2026-014",
        "REC-11-006": "VAL-2026-015",
    }
    records_by_id = {
        item.get("recordId"): item
        for item in exercise_records
        if isinstance(item, dict)
    }
    for record_id, validation_id in expected_record_validation.items():
        record = records_by_id.get(record_id, {})
        if record.get("validationId") != validation_id:
            error(f"{fixture_path}: {record_id} must map to {validation_id}")
        for key in ("request", "expectedResult", "observedResult"):
            if not isinstance(record.get(key), dict):
                error(f"{fixture_path}: {record_id} must contain structured {key}")
        observed = record.get("observedResult", {})
        if isinstance(observed, dict) and observed.get("status") != record.get(
            "observedStatus"
        ):
            error(f"{fixture_path}: {record_id} observed status fields must agree")
        request = record.get("request", {})
        host = request.get("host") if isinstance(request, dict) else None
        if not isinstance(host, str) or not host.endswith(
            (".example", ".test", ".invalid")
        ):
            error(f"{fixture_path}: {record_id} request host must be reserved")
    own_tenant_record = records_by_id.get("REC-11-001", {})
    denied_tenant_record = records_by_id.get("REC-11-002", {})
    if own_tenant_record.get("expectedResult") != own_tenant_record.get(
        "observedResult"
    ) or own_tenant_record.get("observedStatus") != 200:
        error(f"{fixture_path}: REC-11-001 must directly record the authorized result")
    if denied_tenant_record.get("expectedResult") != denied_tenant_record.get(
        "observedResult"
    ) or denied_tenant_record.get("observedStatus") != 404:
        error(f"{fixture_path}: REC-11-002 must directly record the denied result")
    validation_ids = {
        item.get("validationId")
        for item in validations
        if isinstance(item, dict)
    }
    if validation_ids != {f"VAL-2026-{number:03d}" for number in range(11, 16)}:
        error(f"{fixture_path}: expected five chapter 11 validation records")
    for item in validations:
        if not isinstance(item, dict):
            error(f"{fixture_path}: validation records must be objects")
            continue
        suffix = str(item.get("validationId", "")).removeprefix("VAL-")
        if item.get("observationId") != f"OBS-{suffix}":
            error(f"{fixture_path}: validation/observation ID mismatch for {suffix}")
        if item.get("evidenceId") != f"EVD-{suffix}":
            error(f"{fixture_path}: validation/evidence ID mismatch for {suffix}")
        if not isinstance(item.get("limitation"), str) or not item["limitation"].strip():
            error(f"{fixture_path}: missing validation limitation for {suffix}")
    record_mapping = {
        item.get("validationId"): item.get("recordIds")
        for item in validations
        if isinstance(item, dict)
    }
    if record_mapping != {
        "VAL-2026-011": ["REC-11-001", "REC-11-002"],
        "VAL-2026-012": ["REC-11-003"],
        "VAL-2026-013": ["REC-11-004"],
        "VAL-2026-014": ["REC-11-005"],
        "VAL-2026-015": ["REC-11-006"],
    }:
        error(f"{fixture_path}: exercise records must map directly to validations")
    mapped_record_ids = {
        record_id
        for item_record_ids in record_mapping.values()
        if isinstance(item_record_ids, list)
        for record_id in item_record_ids
    }
    if mapped_record_ids != expected_record_ids:
        error(f"{fixture_path}: every exercise record must be referenced by a validation")
    event_ids = {
        item.get("fixtureEventId")
        for item in fixture.get("detectionEvents", [])
        if isinstance(item, dict)
    }
    if event_ids != {f"FIX-2026-{number:03d}" for number in range(11, 15)}:
        error(f"{fixture_path}: expected four synthetic detection events")
    detection_mapping = {
        item.get("fixtureEventId"): (
            item.get("detectionId"),
            item.get("validationId"),
            item.get("recordIds"),
        )
        for item in fixture.get("detectionEvents", [])
        if isinstance(item, dict)
    }
    if detection_mapping != {
        "FIX-2026-011": ("DET-2026-011", "VAL-2026-012", ["REC-11-003"]),
        "FIX-2026-012": ("DET-2026-012", "VAL-2026-013", ["REC-11-004"]),
        "FIX-2026-013": ("DET-2026-013", "VAL-2026-015", ["REC-11-006"]),
        "FIX-2026-014": ("DET-2026-014", "VAL-2026-014", ["REC-11-005"]),
    }:
        error(f"{fixture_path}: detection events must map to validation records")
    fixture_text = json.dumps(fixture, ensure_ascii=False)
    for pattern in secret_patterns:
        if pattern.search(fixture_text):
            error(f"{fixture_path}: possible real target or secret pattern detected")
    for raw_url in re.findall(r"https?://[^\s\"}]+", fixture_text):
        host = (urlparse(raw_url).hostname or "").lower()
        if not host.endswith((".example", ".test", ".invalid")):
            error(f"{fixture_path}: non-reserved URL in synthetic fixture: {raw_url}")

    sources = load_json("references/sources.json")
    sources_by_id = {
        item.get("id"): item
        for item in sources.get("sources", [])
        if isinstance(item, dict)
    }
    for source_id in (
        "SRC-WSTG-001",
        "SRC-OWASP-TOP10-001",
        "SRC-API-001",
    ):
        source = sources_by_id.get(source_id)
        if source is None:
            error(f"references/sources.json: missing {source_id}")
            continue
        if 11 not in source.get("chapters", []):
            error(f"references/sources.json: {source_id} must map to chapter 11")
        if source.get("checkedAt") != "2026-08-03":
            error(f"references/sources.json: {source_id} must be rechecked on 2026-08-03")
    wstg = sources_by_id.get("SRC-WSTG-001", {})
    if wstg.get("version") != "4.2; 5.0 under development" or wstg.get("status") != "stable":
        error("references/sources.json: WSTG stable/development distinction changed")
    if sources_by_id.get("SRC-OWASP-TOP10-001", {}).get("version") != "2025":
        error("references/sources.json: OWASP Top 10 version must be 2025")
    if sources_by_id.get("SRC-API-001", {}).get("version") != "2023":
        error("references/sources.json: OWASP API Security Top 10 version must be 2023")

    registry = load_json("site-pages.json")
    try:
        registry = parse_registry_data(registry)
    except SitePageRegistryError as exc:
        error(f"site-pages.json: schema contract violation: {exc}")
        registry = {}
    expected_pages = {
        (
            "manuscript/11-web-api-hypothesis.md",
            "chapters/chapter-11/index.md",
            "chapters",
            50,
        ),
        (
            "templates/web-api-assessment-hypothesis-pack.md",
            "templates/web-api-assessment-hypothesis-pack/index.md",
            "additional",
            240,
        ),
        (
            "cases/ch11-web-api-assessment-example.md",
            "cases/chapter-11-web-api-assessment/index.md",
            "additional",
            250,
        ),
    }
    actual_pages = {
        (
            item.get("source"),
            item.get("destination"),
            item.get("section"),
            item.get("order"),
        )
        for item in registry.get("pages", [])
        if isinstance(item, dict)
    }
    missing_pages = expected_pages - actual_pages
    if missing_pages:
        error(f"site-pages.json: missing chapter 11 pages: {sorted(missing_pages)}")

    artifact_index = read_text("artifact-index.md")
    require_tokens(
        "artifact-index.md",
        artifact_index,
        (
            "ART-11",
            "Web/API Assessment Hypothesis Pack",
            "templates/web-api-assessment-hypothesis-pack.md",
            "cases/ch11-web-api-assessment-example.md",
            "cases/fixtures/ch11-web-api-assessment-dataset.json",
        ),
    )
    figure_index = read_text("figure-index.md")
    require_tokens(
        "figure-index.md",
        figure_index,
        ("F-11-01", "F-11-02", "T-11-01", "T-11-02", "T-11-03", "T-11-04"),
    )
    landing = read_text("index.md")
    require_tokens(
        "index.md",
        landing,
        (
            "manuscript/11-web-api-hypothesis.md",
            "templates/web-api-assessment-hypothesis-pack.md",
            "cases/ch11-web-api-assessment-example.md",
            "cases/fixtures/ch11-web-api-assessment-dataset.json",
        ),
    )

    package = load_json("package.json")
    scripts = package.get("scripts", {})
    if scripts.get("check:chapter11") != "python3 scripts/check_chapter11_contract.py":
        error("package.json: missing check:chapter11 script")
    if "npm run check:chapter11" not in scripts.get("test", ""):
        error("package.json: test must run check:chapter11")

    for item in ERRORS:
        print(f"ERROR: {item}")
    if ERRORS:
        return 1
    print(
        "chapter 11 contract passed: hypothesis-driven Web/API assessment, "
        "safe synthetic case, direct evidence/detection traceability, source "
        "baseline, and registry publication"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
