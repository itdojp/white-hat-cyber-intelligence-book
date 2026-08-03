#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

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
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        error(f"{relative}: invalid JSON: {exc}")
        return {}
    if not isinstance(data, dict):
        error(f"{relative}: root must be an object")
        return {}
    return data


def require_tokens(relative: str, text: str, tokens: tuple[str, ...]) -> None:
    for token in tokens:
        if token not in text:
            error(f"{relative}: missing required token {token!r}")


def main() -> int:
    required_files = (
        "manuscript/01-integrated-discipline.md",
        "templates/integrated-security-case-map.md",
        "cases/ch01-integrated-security-case-example.md",
        "site-pages.json",
        "schemas/site-pages.schema.json",
        "scripts/sync_book_site.py",
        "scripts/check_site_pages_security.py",
        "artifact-index.md",
        "figure-index.md",
        "glossary.md",
        "book-config.json",
        "CANONICAL_SOURCE.md",
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
            and item.get("id") == "ch01-integrated-discipline"
        ),
        None,
    )
    if chapter_config is None:
        error("book-config.json: missing ch01-integrated-discipline")
    else:
        objectives = chapter_config.get("objectives", [])
        if "Integrated Security Workflow Mapを作成できる" not in objectives:
            error(
                "book-config.json: chapter 1 must retain the configured "
                "Integrated Security Workflow Map learning objective"
            )

    chapter_path = "manuscript/01-integrated-discipline.md"
    chapter = read_text(chapter_path)
    require_tokens(
        chapter_path,
        chapter,
        (
            "Integrated Security Case Map",
            "Integrated Security Workflow Map",
            "OWN",
            "BRIDGE",
            "DELEGATE",
            "Case ID",
            "Decision Requirement",
            "Handoff Contract",
            "Outcome metric",
            "Negative Finding",
            "F-01-01",
            "F-01-02",
            "F-01-03",
            "T-01-01",
            "T-01-02",
            "T-01-03",
            "../templates/integrated-security-case-map.md",
            "../cases/ch01-integrated-security-case-example.md",
        ),
    )
    for forbidden in (
        "High confidence",
        "Low confidence",
        "Moderate confidence",
        "LowまたはModerate confidence",
    ):
        if forbidden in chapter:
            error(
                f"{chapter_path}: confidence vocabulary must use 高 / 中 / 低; "
                f"found {forbidden!r}"
            )
    for source_id in (
        "SRC-NICE-001",
        "SRC-ATTACK-001",
        "SRC-CSF-001",
        "SRC-IR-001",
        "SRC-ICD203-001",
    ):
        if source_id not in chapter:
            error(f"{chapter_path}: missing Source Note ID {source_id}")

    template_path = "templates/integrated-security-case-map.md"
    template = read_text(template_path)
    require_tokens(
        template_path,
        template,
        (
            "Artifact ID",
            "Case ID",
            "Decision Requirement ID",
            "Related Decision Requirement ID",
            "Related Asset IDs",
            "Related Boundary IDs",
            "Authority / RoE ID",
            "Threat Hypotheses",
            "Observation Hypotheses",
            "Alternative Explanations",
            "Evidence Register",
            "Observation ID",
            "Validation ID",
            "Authority / RoE ID",
            "Negative Finding",
            "Related Evidence IDs",
            "Telemetry Requirements",
            "Detection Validation",
            "Related hypothesis",
            "Analytic Judgment",
            "Related Evidence / Negative Finding IDs",
            "Related Finding IDs",
            "Related Detection / Hunt / Incident IDs",
            "Related Telemetry IDs",
            "Confidence | 高 / 中 / 低",
            "Decision Record",
            "Related Analytic Judgment ID",
            "Related Decision ID",
            "Related Control IDs",
            "Reassessment",
            "Handoff Contracts",
            "Outcome Metrics",
            "Traceability Check",
        ),
    )
    if "Confidence | High / Moderate / Low" in template:
        error(f"{template_path}: confidence vocabulary must use 高 / 中 / 低")

    example_path = "cases/ch01-integrated-security-case-example.md"
    example = read_text(example_path)
    require_tokens(
        example_path,
        example,
        (
            "CASE-2026-001",
            "DR-2026-001",
            "ROE-2026-001",
            "TH-2026-001",
            "OBS-2026-001",
            "EVD-2026-001",
            "FIND-2026-001",
            "TEL-2026-001",
            "DET-2026-001",
            "HUNT-2026-001",
            "AJ-2026-001",
            "DEC-2026-001",
            "CTRL-2026-001",
            "REA-2026-001",
            "HO-2026-001",
            "MET-2026-001",
            "billing-bridge.example",
            "侵害不存在は断定しない",
            "| Status | Reassessment Due |",
            "| Confidence | 中 |",
            "| `HUNT-2026-001` | Hunt | `TH-2026-003` |",
            "| Related Evidence / Negative Finding IDs | `EVD-2026-001`, `EVD-2026-002`, `EVD-2026-003`, `EVD-2026-004`, `NEG-2026-001` |",
            "| Related Finding IDs | `FIND-2026-001`, `FIND-2026-002`, `FIND-2026-003` |",
            "| Related Detection / Hunt / Incident IDs | `DET-2026-001`, `DET-2026-002`, `HUNT-2026-001` |",
            "| Related Analytic Judgment ID | `AJ-2026-001` |",
            "| Related Control IDs | `CTRL-2026-001`, `CTRL-2026-002`, `CTRL-2026-003`, `CTRL-2026-004` |",
            "| Related Decision Requirement ID | `DR-2026-001` |",
            "| `TH-2026-002` | `DR-2026-001` | `ASSET-2026-002`, `ASSET-2026-003` | `TB-2026-001`, `TB-2026-003` |",
            "| `NEG-2026-001` | `EVD-2026-004` |",
            "| `TEL-2026-003` | `EVD-2026-004` |",
            "| `DET-2026-002` | `TH-2026-001` | `TEL-2026-002`, `TEL-2026-003` |",
            "| `EVD-2026-003` | `OBS-2026-002` | `VAL-2026-002` | `ROE-2026-001` |",
            "| `CTRL-2026-003` | `DEC-2026-001` | `FIND-2026-002` |",
            "合成同意Eventは現行Pipelineで取得でき、Rule testも成功した",
        ),
    )
    if "合成同意Eventは現行Pipelineでも欠落した" in example:
        error(f"{example_path}: alternative evidence contradicts validated telemetry")
    if re.search(r"^\| Confidence \| (?:High|Moderate|Low) \|$", example, re.MULTILINE):
        error(f"{example_path}: confidence vocabulary must use 高 / 中 / 低")

    secret_patterns = (
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    )
    for pattern in secret_patterns:
        if pattern.search(example):
            error(f"{example_path}: possible secret pattern detected")

    registry = load_json("site-pages.json")
    try:
        registry = parse_registry_data(registry)
    except SitePageRegistryError as exc:
        error(f"site-pages.json: schema contract violation: {exc}")
        registry = {}

    expected_pages = {
        (
            "templates/integrated-security-case-map.md",
            "templates/integrated-security-case-map/index.md",
        ),
        (
            "cases/ch01-integrated-security-case-example.md",
            "cases/chapter-01-integrated-security-case/index.md",
        ),
    }
    actual_pages = {
        (item.get("source"), item.get("destination"))
        for item in registry.get("pages", [])
        if isinstance(item, dict)
    }
    missing_pages = expected_pages - actual_pages
    if missing_pages:
        error(f"site-pages.json: missing registered pages: {sorted(missing_pages)}")
    directories = registry.get("canonicalDirectories", [])
    for directory in ("cases", "schemas"):
        if directory not in directories:
            error(f"site-pages.json: canonicalDirectories missing {directory}")
    if registry.get("directoryRoutes", {}).get("cases") != (
        "cases/chapter-01-integrated-security-case/index.md"
    ):
        error("site-pages.json: cases directory route mismatch")

    schema = load_json("schemas/site-pages.schema.json")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        error("schemas/site-pages.schema.json: unexpected JSON Schema dialect")
    route_names = (
        schema.get("properties", {})
        .get("directoryRoutes", {})
        .get("propertyNames", {})
        .get("enum")
    )
    if route_names != ["cases", "schemas"]:
        error(
            "schemas/site-pages.schema.json: directoryRoutes must allow only "
            "the approved canonical roots"
        )
    route_dependencies = {
        (
            item.get("if", {})
            .get("properties", {})
            .get("directoryRoutes", {})
            .get("required", [None])[0]
        ): (
            item.get("then", {})
            .get("properties", {})
            .get("canonicalDirectories", {})
            .get("contains", {})
            .get("const")
        )
        for item in schema.get("allOf", [])
        if isinstance(item, dict)
    }
    if route_dependencies != {"cases": "cases", "schemas": "schemas"}:
        error(
            "schemas/site-pages.schema.json: each directory route must require "
            "its matching canonicalDirectories declaration"
        )

    artifact_index = read_text("artifact-index.md")
    require_tokens(
        "artifact-index.md",
        artifact_index,
        (
            "ART-10",
            "Integrated Security Case Map",
            "templates/integrated-security-case-map.md",
        ),
    )

    figure_index = read_text("figure-index.md")
    require_tokens(
        "figure-index.md",
        figure_index,
        (
            "F-01-01",
            "F-01-02",
            "F-01-03",
            "T-01-01",
            "T-01-02",
            "T-01-03",
        ),
    )

    glossary = read_text("glossary.md")
    require_tokens(
        "glossary.md",
        glossary,
        (
            "Decision Requirement",
            "Handoff Contract",
            "Integrated Security Case Map",
            "Negative Finding",
            "Residual Risk",
            "Reassessment Trigger",
        ),
    )

    canonical = read_text("CANONICAL_SOURCE.md")
    require_tokens(
        "CANONICAL_SOURCE.md",
        canonical,
        (
            "cases/",
            "site-pages.json",
            "sync_book_site.py",
        ),
    )

    package = load_json("package.json")
    scripts = package.get("scripts", {})
    if scripts.get("check:chapter1") != "python3 scripts/check_chapter1_contract.py":
        error("package.json: check:chapter1 command mismatch")
    if scripts.get("check:site-pages-security") != (
        "python3 scripts/check_site_pages_security.py"
    ):
        error("package.json: check:site-pages-security command mismatch")
    if "scripts/sync_book_site.py" not in scripts.get("sync:docs", ""):
        error("package.json: sync:docs must use sync_book_site.py")
    if "scripts/sync_book_site.py" not in scripts.get("check:docs-sync", ""):
        error("package.json: check:docs-sync must use sync_book_site.py")
    if "npm run check:chapter1" not in scripts.get("test", ""):
        error("package.json: test must run check:chapter1")
    if "npm run check:site-pages-security" not in scripts.get("test", ""):
        error("package.json: test must run check:site-pages-security")

    for message in ERRORS:
        print(f"ERROR: {message}")
    if ERRORS:
        return 1

    print(
        "chapter 1 contract passed: integrated case template, synthetic example, "
        "direct judgment traceability, source IDs, schema-enforced page registry, "
        "and publication extension"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
