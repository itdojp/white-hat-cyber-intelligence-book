#!/usr/bin/env python3
"""Validate the generic exact-renderer Publication Projection contract corpus."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.content_safety_policy import (  # noqa: E402
    POLICY_VERSION as CONTENT_SAFETY_POLICY_VERSION,
    SafetyFinding,
    scan_action_text,
    scan_host_policy,
)
from scripts.publication_projection import (  # noqa: E402
    EXPECTED_RENDERER,
    MAX_PRODUCTION_CONFIG_BYTES,
    PROJECTION_VERSION,
    ProjectedDocument,
    ProjectionField,
    ProjectionRuntimeError,
    UNSUPPORTED_SOURCE_CODE,
    _load_bounded_regular_json,
    is_absolute_destination,
    is_policy_scan_field,
    normalize_destination,
    project_documents,
)

CORPUS = ROOT / "tests" / "fixtures" / "publication-projection" / "corpus.json"
EXPECTED_CORPUS_SCHEMA = "1.0.0"
EXPECTED_POLICY_VERSION = "1.2.0"
REQUIRED_ROLES = frozenset(
    {
        "unsafe_direct",
        "safe_counterpart",
        "bounded_explanation",
        "malformed_or_unsupported",
        "near_miss",
    }
)
KNOWN_POLICY_67_FIXTURE = "PP-COV-16-05"


def validate_destination_contract() -> None:
    executable_cases = (
        "javascript:alert(1)",
        "java\tscript:alert(1)",
        "java\nscript:alert(1)",
        "java\rscript:alert(1)",
        "\x01javascript:alert(1)",
        "vbscript:msgbox(1)",
        "file:///etc/passwd",
    )
    for value in executable_cases:
        _, rejection = normalize_destination(value)
        if rejection is None or "executable" not in rejection:
            fail(f"browser-special executable destination was accepted: {value!r}")
    for scheme in ("ftp", "http", "https", "ws", "wss"):
        normalized, rejection = normalize_destination(
            f"{scheme}:\\\\example.com\\runbook"
        )
        if normalized != f"{scheme}://example.com/runbook" or rejection is not None:
            fail(f"{scheme} special-URL backslash normalization changed")
    for value in ("https:example.com", "https:/example.com", r"https:\example.com"):
        normalized, rejection = normalize_destination(value)
        if normalized != value or rejection is None or "authority-less" not in rejection:
            fail(f"same-origin authority-less URL was not rejected: {value!r}")
    normalized, rejection = normalize_destination("//example.com/runbook")
    if normalized != "https://example.com/runbook" or rejection is not None:
        fail("scheme-relative destination normalization changed")
    for value in (r"/\example.com/runbook", r"\/example.com/runbook"):
        normalized, rejection = normalize_destination(value)
        if normalized != "https://example.com/runbook" or rejection is not None:
            fail("mixed-slash scheme-relative normalization changed")
    for value in (
        "http://[::1",
        "http://example.com:bad/",
        "ftp://[::1",
        "ws://example.com:bad/",
        "wss://[::1",
    ):
        _, rejection = normalize_destination(value)
        if rejection is None or "malformed" not in rejection:
            fail(f"malformed special destination was accepted: {value!r}")
    if normalize_destination("../relative/path.md") != (
        "../relative/path.md",
        None,
    ):
        fail("relative destination normalization changed")


def validate_resource_contract() -> None:
    """Prove the renderer's aggregate output budget fails the entire batch closed."""

    header = "H" * 5_000
    source = f"| {header} |\n|---|\n" + "".join(
        f"| row-{index:03d} |\n" for index in range(250)
    )
    projection = project_documents(
        [(f"PP-BATCH-{index}", source) for index in range(4)]
    )
    for document in projection.documents:
        if document.fields or document.rendered_html:
            fail("aggregate renderer budget returned a partial publication surface")
        if len(document.diagnostics) != 1:
            fail("aggregate renderer budget diagnostic count changed")
        diagnostic = document.diagnostics[0]
        if (
            diagnostic.code != UNSUPPORTED_SOURCE_CODE
            or diagnostic.kind != "batch-budget"
        ):
            fail("aggregate renderer budget did not use stable fail-closed diagnostic")

    reference_expansion = (
        "[x][r] " * 10_000
        + "\n\n[r]: # \""
        + ("T" * 4_096)
        + "\"\n"
    )
    document = project_documents(
        {"PP-RESOURCE-REFERENCE-EXPANSION": reference_expansion}
    ).document("PP-RESOURCE-REFERENCE-EXPANSION")
    if document.fields or document.rendered_html or len(document.diagnostics) != 1:
        fail("reference expansion budget returned a partial publication surface")
    diagnostic = document.diagnostics[0]
    if (
        diagnostic.code != UNSUPPORTED_SOURCE_CODE
        or diagnostic.kind != "renderer-error"
        or "pre-render AST expansion budget exceeded" not in diagnostic.reason
    ):
        fail("reference expansion did not fail before exact HTML rendering")

    abbreviation_expansion = (
        "CRED " * 10_000
        + "\n\n*[CRED]: "
        + ("T" * 4_096)
        + "\n"
    )
    document = project_documents(
        {"PP-RESOURCE-ABBREVIATION-EXPANSION": abbreviation_expansion}
    ).document("PP-RESOURCE-ABBREVIATION-EXPANSION")
    if document.fields or document.rendered_html or len(document.diagnostics) != 1:
        fail("abbreviation expansion budget returned a partial publication surface")
    diagnostic = document.diagnostics[0]
    if (
        diagnostic.code != UNSUPPORTED_SOURCE_CODE
        or diagnostic.kind != "renderer-error"
        or "pre-render AST expansion budget exceeded" not in diagnostic.reason
    ):
        fail("abbreviation expansion did not fail before exact HTML rendering")

    option_expansion = (
        "{::options footnote_backlink=\""
        + ("T" * 4_096)
        + "\" /}\n"
        + ("x[^f] " * 10_000)
        + "\n\n[^f]: foot\n"
    )
    document = project_documents(
        {"PP-RESOURCE-KRAMDOWN-OPTIONS": option_expansion}
    ).document("PP-RESOURCE-KRAMDOWN-OPTIONS")
    if document.fields or document.rendered_html or len(document.diagnostics) != 1:
        fail("Kramdown option expansion returned a partial publication surface")
    diagnostic = document.diagnostics[0]
    if (
        diagnostic.code != UNSUPPORTED_SOURCE_CODE
        or diagnostic.kind != "kramdown-extension"
    ):
        fail("interpreted Kramdown options did not fail before exact rendering")

    work_root = ROOT / ".work"
    work_root.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix="publication-config-contract-", dir=work_root
    ) as temporary:
        temporary_root = Path(temporary)
        oversized = temporary_root / "oversized.json"
        oversized.write_bytes(b" " * (MAX_PRODUCTION_CONFIG_BYTES + 1))
        try:
            _load_bounded_regular_json(oversized)
        except ProjectionRuntimeError:
            pass
        else:
            fail("oversized production configuration was accepted")

        regular = temporary_root / "regular.json"
        regular.write_text("{}\n", encoding="utf-8")
        symlink = temporary_root / "symlink.json"
        symlink.symlink_to(regular.name)
        try:
            _load_bounded_regular_json(symlink)
        except ProjectionRuntimeError:
            pass
        else:
            fail("symlink production configuration was accepted")


def fail(message: str) -> None:
    raise ValueError(message)


def load_corpus() -> dict:
    try:
        value = json.loads(CORPUS.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"publication projection corpus cannot be read: {exc}")
    if not isinstance(value, dict):
        fail("publication projection corpus root must be an object")
    expected_keys = {
        "schema_version",
        "projection_version",
        "renderer",
        "required_roles",
        "required_families",
        "historical_review_thread_ids",
        "external_chapter_selection_fixtures",
        "fixtures",
        "non_goals",
    }
    if set(value) != expected_keys:
        fail("publication projection corpus root keys changed")
    return value


def string_list(value: object, label: str) -> list[str]:
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item for item in value
    ):
        fail(f"{label} must be an array of non-empty strings")
    return value


def validate_manifest(corpus: dict) -> None:
    if corpus["schema_version"] != EXPECTED_CORPUS_SCHEMA:
        fail("publication projection corpus schema version changed")
    if corpus["projection_version"] != PROJECTION_VERSION:
        fail("publication projection corpus version is not the shared module version")
    if corpus["renderer"] != EXPECTED_RENDERER:
        fail("publication projection corpus renderer pin changed")
    if CONTENT_SAFETY_POLICY_VERSION != EXPECTED_POLICY_VERSION:
        fail(
            "generic corpus must retain Content Safety Policy 1.2.0; "
            f"got {CONTENT_SAFETY_POLICY_VERSION!r}"
        )
    roles = frozenset(string_list(corpus["required_roles"], "required_roles"))
    if roles != REQUIRED_ROLES:
        fail(f"required fixture roles changed: {sorted(roles)!r}")
    families = string_list(corpus["required_families"], "required_families")
    if len(families) != len(set(families)):
        fail("required_families contains duplicates")
    historical_ids = string_list(
        corpus["historical_review_thread_ids"],
        "historical_review_thread_ids",
    )
    if len(historical_ids) != 70 or len(set(historical_ids)) != 70:
        fail("historical review thread inventory must contain exactly 70 unique IDs")
    if not all(item.startswith("PRRT_") for item in historical_ids):
        fail("historical review thread inventory contains an invalid GraphQL ID")
    string_list(corpus["non_goals"], "non_goals")

    fixtures = corpus["fixtures"]
    external = corpus["external_chapter_selection_fixtures"]
    if not isinstance(fixtures, list) or not isinstance(external, list):
        fail("fixtures and external selection fixtures must be arrays")
    fixture_ids: set[str] = set()
    mapped_threads: list[str] = []
    family_roles: dict[str, set[str]] = {family: set() for family in families}

    for index, fixture in enumerate(fixtures):
        label = f"fixtures[{index}]"
        if not isinstance(fixture, dict):
            fail(f"{label} must be an object")
        fixture_id = fixture.get("fixture_id")
        if not isinstance(fixture_id, str) or not fixture_id.startswith("PP-"):
            fail(f"{label}.fixture_id must be generic and start with PP-")
        if fixture_id in fixture_ids:
            fail(f"duplicate fixture ID: {fixture_id}")
        fixture_ids.add(fixture_id)
        family = fixture.get("family")
        if family not in family_roles:
            fail(f"{fixture_id}: unowned semantic family {family!r}")
        roles_for_fixture = string_list(fixture.get("roles"), f"{fixture_id}.roles")
        unknown_roles = set(roles_for_fixture) - (
            REQUIRED_ROLES | {"originating_counterexample"}
        )
        if unknown_roles:
            fail(f"{fixture_id}: unknown roles {sorted(unknown_roles)!r}")
        family_roles[family].update(set(roles_for_fixture) & REQUIRED_ROLES)
        secondary = string_list(
            fixture.get("secondary_families"),
            f"{fixture_id}.secondary_families",
        )
        if set(secondary) - set(families):
            fail(f"{fixture_id}: unowned secondary family")
        for secondary_family in secondary:
            # Counterexamples may own an overlapping invariant without satisfying
            # the five explicit coverage roles for that family.
            family_roles[secondary_family].update(
                set(roles_for_fixture) & REQUIRED_ROLES
            )
        threads = string_list(
            fixture.get("originating_thread_ids"),
            f"{fixture_id}.originating_thread_ids",
        )
        mapped_threads.extend(threads)
        if not isinstance(fixture.get("source_markdown"), str):
            fail(f"{fixture_id}: source_markdown must be a string")
        if "chapter02" in fixture["source_markdown"].casefold():
            fail(f"{fixture_id}: generic fixture contains Chapter 2 ownership")
        if not isinstance(fixture.get("notes"), str) or not fixture["notes"]:
            fail(f"{fixture_id}: notes are required")
        if (
            not isinstance(fixture.get("limitations"), str)
            or not fixture["limitations"]
        ):
            fail(f"{fixture_id}: limitations are required")

    for index, fixture in enumerate(external):
        label = f"external_chapter_selection_fixtures[{index}]"
        if not isinstance(fixture, dict):
            fail(f"{label} must be an object")
        expected_keys = {
            "fixture_id",
            "family",
            "also_covers",
            "roles",
            "originating_thread_ids",
            "owner",
            "command",
        }
        if set(fixture) != expected_keys:
            fail(f"{label}: schema changed")
        fixture_id = fixture["fixture_id"]
        if not isinstance(fixture_id, str) or not fixture_id.startswith("CH02-SEL-"):
            fail(f"{label}: invalid external selection fixture ID")
        if fixture_id in fixture_ids:
            fail(f"duplicate fixture ID: {fixture_id}")
        fixture_ids.add(fixture_id)
        covered = [fixture["family"]] + string_list(
            fixture["also_covers"], f"{fixture_id}.also_covers"
        )
        if set(covered) - set(families):
            fail(f"{fixture_id}: external fixture has an unowned family")
        fixture_roles = set(string_list(fixture["roles"], f"{fixture_id}.roles"))
        if fixture_roles - REQUIRED_ROLES:
            fail(f"{fixture_id}: external fixture has an unknown role")
        for family in covered:
            family_roles[family].update(fixture_roles)
        mapped_threads.extend(
            string_list(
                fixture["originating_thread_ids"],
                f"{fixture_id}.originating_thread_ids",
            )
        )
        if fixture["owner"] != "scripts/check_chapter02_contract.py":
            fail(f"{fixture_id}: Layer A owner changed")
        if fixture_id not in fixture["command"]:
            fail(f"{fixture_id}: reproduction command does not name the fixture")

    if len(mapped_threads) != 70 or len(set(mapped_threads)) != 70:
        fail("each historical review thread must be mapped exactly once")
    if set(mapped_threads) != set(historical_ids):
        missing = sorted(set(historical_ids) - set(mapped_threads))
        extra = sorted(set(mapped_threads) - set(historical_ids))
        fail(f"review mapping mismatch; missing={missing!r}; extra={extra!r}")
    for family, covered_roles in family_roles.items():
        if covered_roles != REQUIRED_ROLES:
            fail(
                f"semantic family {family!r} does not cover every required role; "
                f"got {sorted(covered_roles)!r}"
            )


def serialize_field(field: ProjectionField) -> dict:
    return {
        "type": field.field_type,
        "text": field.text,
        "normalized_text": field.normalized_text,
        "line": field.line,
        "ordinal": field.ordinal,
        "element_kind": field.element_kind,
        "attribute": field.attribute,
        "metadata": dict(field.metadata),
        "location": field.location,
    }


def serialize_diagnostics(document: ProjectedDocument) -> list[dict]:
    return [
        {
            "code": item.code,
            "line": item.line,
            "kind": item.kind,
            "reason": item.reason,
            "location": item.location,
        }
        for item in document.diagnostics
    ]


def policy_findings(document: ProjectedDocument) -> list[SafetyFinding]:
    findings: list[SafetyFinding] = []
    for field in document.fields:
        if is_policy_scan_field(field):
            findings.extend(
                scan_action_text(field.normalized_text, location=field.location)
            )
            findings.extend(
                scan_host_policy(field.normalized_text, location=field.location)
            )
        elif field.field_type == "destination" and is_absolute_destination(
            field.normalized_text
        ):
            findings.extend(
                scan_host_policy(field.normalized_text, location=field.location)
            )
    return sorted(
        set(findings),
        key=lambda item: (
            item.location,
            item.category,
            item.normalized_excerpt,
            item.reason,
            item.policy_version,
        ),
    )


def validate_fixture(fixture: dict, document: ProjectedDocument) -> str:
    fixture_id = fixture["fixture_id"]
    if document.document_id != fixture_id:
        fail(f"{fixture_id}: projected document ID/order changed")
    renderer = fixture.get("renderer_expectation")
    if not isinstance(renderer, dict):
        fail(f"{fixture_id}: renderer_expectation must be an object")
    expected_renderer = {
        **EXPECTED_RENDERER,
        "rendered_html": document.rendered_html,
    }
    if renderer != expected_renderer:
        fail(f"{fixture_id}: exact pinned rendered HTML/version parity changed")

    actual_visible = [
        serialize_field(field)
        for field in document.fields
        if field.field_type in {"reader_visible_text", "reader_visible_attribute"}
    ]
    actual_destinations = [
        serialize_field(field)
        for field in document.fields
        if field.field_type == "destination"
    ]
    actual_hidden = [
        serialize_field(field)
        for field in document.fields
        if field.field_type == "hidden_metadata"
    ]
    comparisons = (
        (
            "projected_reader_visible_fields",
            actual_visible,
        ),
        ("projected_destination_fields", actual_destinations),
        ("projected_hidden_metadata_fields", actual_hidden),
        (
            "unsupported_fail_closed_expectation",
            serialize_diagnostics(document),
        ),
    )
    for name, actual in comparisons:
        if fixture.get(name) != actual:
            fail(f"{fixture_id}: {name} changed")

    locations = [field.location for field in document.fields]
    if fixture.get("stable_location_order") != locations:
        fail(f"{fixture_id}: stable field location/order changed")
    if fixture.get("exactly_once") is not True:
        fail(f"{fixture_id}: exactly_once must be true")
    unique_fields = {
        (
            field.field_type,
            field.text,
            field.normalized_text,
            field.line,
            field.element_kind,
            field.attribute,
            field.metadata,
        )
        for field in document.fields
    }
    if len(unique_fields) != len(document.fields):
        fail(f"{fixture_id}: projected field is not exactly once")

    findings = policy_findings(document)
    category_counts = dict(sorted(Counter(item.category for item in findings).items()))
    expected_policy = fixture.get("policy_expectation")
    if not isinstance(expected_policy, dict) or set(expected_policy) != {
        "expected_category_counts",
        "expected_total_findings",
        "expected_safe_finding_count",
    }:
        fail(f"{fixture_id}: policy_expectation schema changed")
    if expected_policy["expected_category_counts"] != category_counts:
        fail(
            f"{fixture_id}: Policy categories changed; "
            f"expected={expected_policy['expected_category_counts']!r}; actual={category_counts!r}"
        )
    if expected_policy["expected_total_findings"] != len(findings):
        fail(f"{fixture_id}: Policy finding count changed")
    if expected_policy["expected_safe_finding_count"] != 0:
        fail(f"{fixture_id}: safe finding count must remain zero")

    safe_roles = {"safe_counterpart", "bounded_explanation", "near_miss"}
    if set(fixture["roles"]) & safe_roles and findings:
        if fixture_id != KNOWN_POLICY_67_FIXTURE:
            fail(f"{fixture_id}: safe/explanation/near-miss fixture produced findings")
        if fixture["family"] != "shared Policy issue #67":
            fail(f"{fixture_id}: only the separately tracked Issue #67 may be known")
    return (
        f"{fixture_id}: fields={len(document.fields)}; "
        f"diagnostics={len(document.diagnostics)}; findings={len(findings)}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate the shared Publication Projection fixture corpus"
    )
    parser.add_argument(
        "--fixture",
        action="append",
        help="run one generic fixture ID (repeatable)",
    )
    args = parser.parse_args(argv)

    try:
        corpus = load_corpus()
        validate_manifest(corpus)
        validate_destination_contract()
        validate_resource_contract()
        fixtures = corpus["fixtures"]
        if args.fixture:
            requested = set(args.fixture)
            available = {item["fixture_id"] for item in fixtures}
            missing = sorted(requested - available)
            if missing:
                fail(f"unknown generic fixture IDs: {missing!r}")
            fixtures = [item for item in fixtures if item["fixture_id"] in requested]
        projection = project_documents(
            [(item["fixture_id"], item["source_markdown"]) for item in fixtures]
        )
        summaries = [
            validate_fixture(fixture, document)
            for fixture, document in zip(
                fixtures,
                projection.documents,
                strict=True,
            )
        ]
    except (OSError, TypeError, ValueError, ProjectionRuntimeError) as exc:
        print(f"ERROR: {exc}")
        return 1

    for summary in summaries:
        print(f"PASS: {summary}")
    print(
        "publication projection contract passed: "
        f"version {PROJECTION_VERSION}, fixtures={len(fixtures)}, "
        "review-thread mapping=70/70, exact renderer parity and deterministic "
        "typed fields verified"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
