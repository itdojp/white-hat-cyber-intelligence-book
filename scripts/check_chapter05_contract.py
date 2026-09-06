#!/usr/bin/env python3
"""Chapter 5 Layer A: select complete documents and check ART-15 semantics.

Publication Projection 1.1.0 exclusively owns syntax/rendering. Content Safety
Policy 1.2.0 owns action/host grammar. No raw Markdown/HTML parsing occurs here.
"""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.chapter05_semantics import SNAPSHOT_SHA256, validate_case  # noqa: E402
from scripts.check_editorial_input_manifest import ManifestError, load_json_strict  # noqa: E402
from scripts.content_safety_policy import (  # noqa: E402
    POLICY_VERSION,
    scan_action_text,
    scan_host_policy,
)  # noqa: E402
from scripts.publication_projection import (  # noqa: E402
    PROJECTION_VERSION,
    ProjectionRuntimeError,
    is_absolute_destination,
    is_policy_scan_field,
    project_documents,
)

DOCUMENTS = (
    "manuscript/05-attack-behavior.md",
    "templates/attack-behavior-map.md",
    "cases/ch05-attack-behavior-example.md",
    "references/ch05-source-review-2026-09-06.md",
)
CASE_PATH = "cases/fixtures/ch05-attack-behavior.json"
SNAPSHOT_PATH = "tests/fixtures/attack/ch05-v19.2.json"
CONTRACT_PATH = "tests/fixtures/chapter05/publication-contract.json"
SOURCE_IDS = (
    "SRC-ATTACK-001",
    "SRC-ATTACK-FAQ-001",
    "SRC-ATTACK-T1671-001",
    "SRC-ATTACK-DET-001",
    "SRC-ATTACK-DS-001",
)


def identity(field) -> list:
    return [field.field_type, field.element_kind, field.attribute, field.text]


def relations(document) -> list[tuple[object, dict]]:
    """Stable semantic locations derived only from Layer B fields."""
    levels, previous, result = {}, {}, []
    for field in document.fields:
        relation = {
            "field": identity(field),
            "headings": [levels[k] for k in sorted(levels)],
        }
        if field.field_type == "destination":
            relation["owner"] = previous.get(field.line)
        result.append((field, relation))
        if field.field_type in {"reader_visible_text", "reader_visible_attribute"}:
            previous[field.line] = identity(field)
        level = field.metadata_value("level")
        if (
            field.element_kind == "heading"
            and field.field_type == "reader_visible_text"
            and type(level) is int
        ):
            levels = {k: v for k, v in levels.items() if k < level}
            levels[level] = field.text
    return result


def key(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def scan_document(
    document, spec: dict, *, require_exceptions: bool = False
) -> list[str]:
    errors = [f"{document.document_id}: {item}" for item in document.diagnostics]
    pairs = relations(document)
    counts = Counter(key(relation) for _, relation in pairs)
    exemptions = {
        kind: {key(x["relation"]) for x in spec["exceptions"][kind]}
        for kind in ("action", "host", "destination")
    }
    if require_exceptions:
        for kind, values in exemptions.items():
            for value in sorted(values):
                if counts[value] != 1:
                    errors.append(
                        f"{document.document_id}: {kind} exact exception cardinality"
                    )
    for field, relation in pairs:
        relation_key = key(relation)

        def exempt(kind: str) -> bool:
            return relation_key in exemptions[kind] and counts[relation_key] == 1

        findings = []
        if is_policy_scan_field(field):
            if not exempt("action"):
                findings.extend(
                    scan_action_text(field.normalized_text, location=field.location)
                )
            if not exempt("host"):
                findings.extend(
                    scan_host_policy(field.normalized_text, location=field.location)
                )
        elif (
            field.field_type == "destination"
            and is_absolute_destination(field.normalized_text)
            and not exempt("destination")
        ):
            findings.extend(
                scan_host_policy(field.normalized_text, location=field.location)
            )
        errors.extend(f"{f.location}: {f.category}: {f.reason}" for f in findings)
    return errors


def display(value: object) -> str:
    if value is None or value == []:
        return "なし"
    return ", ".join(value) if isinstance(value, list) else str(value)


def document_errors(document, spec: dict, case: dict) -> list[str]:
    errors = scan_document(document, spec, require_exceptions=True)
    headings = [
        [f.metadata_value("level"), f.text]
        for f in document.fields
        if f.field_type == "reader_visible_text"
        and f.element_kind == "heading"
        and type(f.metadata_value("level")) is int
        and f.metadata_value("level") <= 2
    ]
    if headings != spec["headings"]:
        errors.append(f"{document.document_id}: finite H1/H2 inventory drift")
    counts = Counter(key(relation) for _, relation in relations(document))
    for requirement in spec["required"]:
        if counts[key(requirement)] != 1:
            errors.append(
                f"{document.document_id}: semantic field missing/duplicate: {requirement['field'][3]}"
            )
    if document.document_id == DOCUMENTS[2]:
        expected = []
        for row in case["rows"]:
            expected.extend(
                f"{row['rowId']} Field Value {k} {display(v)}" for k, v in row.items()
            )
        controls = (
            "artifactId mapId parentCaseId relation parentThreatModelId decisionRequirementId "
            "authorizationRecordId scope catalogVersion teachingModel parentState"
        ).split()
        expected = (
            [f"Document Control Field Value {k} {display(case[k])}" for k in controls]
            + [
                "Control ID Role Assurance Parent Evidence IDs Limitation "
                + " ".join(
                    display(c[k])
                    for k in (
                        "controlId",
                        "role",
                        "assurance",
                        "parentEvidenceIds",
                        "limitation",
                    )
                )
                for c in case["controls"]
            ]
            + expected
        )
        actual = [
            f.text
            for f in document.fields
            if f.field_type == "reader_visible_text" and f.element_kind == "table_row"
        ]
        if actual != expected:
            errors.append("ART-15 JSON/projected case table parity")
    return errors


def json_safety(value: object, location: str = CASE_PATH) -> list[str]:
    """Scan every synthetic data string; no destination/provenance exceptions."""
    if isinstance(value, dict):
        return [e for k, v in value.items() for e in json_safety(v, f"{location}/{k}")]
    if isinstance(value, list):
        return [
            e for i, v in enumerate(value) for e in json_safety(v, f"{location}/{i}")
        ]
    if isinstance(value, str):
        return [
            f"{f.location}: {f.category}: {f.reason}"
            for f in scan_action_text(value, location=location)
            + scan_host_policy(value, location=location)
        ]
    return []


def repository_errors(contract: dict) -> list[str]:
    errors = []
    package = load_json_strict(ROOT / "package.json")
    if (
        package["scripts"].get("check:chapter05")
        != "python3 scripts/check_chapter05_contract.py"
        or package["scripts"]["test"].split(" && ").count("npm run check:chapter05")
        != 1
    ):
        errors.append("root test must invoke Chapter 5 exactly once")
    sources = load_json_strict(ROOT / "references/sources.json")
    sources = {item["id"]: item for item in sources["sources"]}
    for sid in SOURCE_IDS:
        source = sources.get(sid, {})
        if (
            source.get("checkedAt") != "2026-09-06"
            or source.get("nextReviewAt") != "2026-12-06"
            or 5 not in source.get("chapters", [])
        ):
            errors.append(f"{sid}: scoped source audit")
    if sources["SRC-ATTACK-001"].get("version") != "19.2":
        errors.append("ATT&CK current catalog version")
    registry = load_json_strict(ROOT / "site-pages.json")
    for expected in contract["pages"]:
        if sum(page == expected for page in registry["pages"]) != 1:
            errors.append(f"Chapter 5 publication route: {expected['source']}")
    for expected in contract["staticArtifacts"]:
        if sum(page == expected for page in registry["staticFiles"]) != 1:
            errors.append("Chapter 5 static dataset route")
    return errors


def main() -> int:
    try:
        contract = load_json_strict(ROOT / CONTRACT_PATH)
        case = load_json_strict(ROOT / CASE_PATH)
        snapshot = load_json_strict(ROOT / SNAPSHOT_PATH)
        if (
            hashlib.sha256((ROOT / SNAPSHOT_PATH).read_bytes()).hexdigest()
            != SNAPSHOT_SHA256
        ):
            raise ValueError("pinned minimal ATT&CK metadata digest mismatch")
        if POLICY_VERSION != "1.2.0" or PROJECTION_VERSION != "1.1.0":
            raise ValueError("Chapter 5 reviewed Policy/Projection version mismatch")
        if list(contract["documents"]) != list(DOCUMENTS):
            raise ValueError("Chapter 5 finite document contract inventory")
        errors = (
            validate_case(case, snapshot, contract["parentBindings"])
            + json_safety(case)
            + repository_errors(contract)
        )
        if case["controls"] != contract["parentControls"]:
            errors.append("retained parent Control state/evidence")
        source = {path: (ROOT / path).read_text(encoding="utf-8") for path in DOCUMENTS}
        projected = project_documents(source)
        if [d.document_id for d in projected.documents] != list(DOCUMENTS):
            # Layer B retains the explicitly selected document order.
            raise ValueError("projected document inventory/order")
        for document in projected.documents:
            errors.extend(
                document_errors(
                    document, contract["documents"][document.document_id], case
                )
            )
        from scripts.chapter05_regressions import run_regressions

        count, regression_errors = run_regressions(case, snapshot, contract, source)
        errors.extend(regression_errors)
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        print(
            f"Chapter 5 contract passed: 4 complete documents; 7 ART-15 rows; 8 source objects; {count} regressions; Policy {POLICY_VERSION}; Projection {PROJECTION_VERSION}"
        )
        return 0
    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        ManifestError,
        ProjectionRuntimeError,
    ) as exc:
        print(f"ERROR: Chapter 5 contract: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
