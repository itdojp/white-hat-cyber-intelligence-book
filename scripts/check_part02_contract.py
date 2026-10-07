#!/usr/bin/env python3
"""Part II Layer A: finite cross-record references, not a new chapter evaluator.

Existing chapter checkers retain JSON Schema and judgment semantics. This owner
checks only the links and boundaries described by the supplemental reader map.
The shared production projection and Policy own all syntax and safety grammar.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.check_editorial_input_manifest import load_json_strict, ManifestError  # noqa: E402
from scripts.content_safety_policy import (  # noqa: E402
    POLICY_VERSION,
    scan_action_text,
    scan_host_policy,
)
from scripts.publication_projection import (  # noqa: E402
    PROJECTION_VERSION,
    ProjectionRuntimeError,
    project_documents,
    is_policy_scan_field,
    is_absolute_destination,
)

VERSION = "1.0.0"
DOCUMENT = "cases/part-ii-assessment-risk-map.md"
CONTRACT = "tests/fixtures/part02/publication-contract.json"
PROBES = "tests/fixtures/part02/counterexamples.json"
SOURCES = {
    9: "cases/fixtures/ch09-engagement-roe.json",
    10: "cases/fixtures/ch10-attack-surface.json",
    11: "cases/fixtures/ch11-web-api-assessment-dataset.json",
    12: "cases/fixtures/ch12-identity-paths.json",
    13: "cases/fixtures/ch13-supply-chain.json",
    14: "cases/fixtures/ch14-minimal-impact-validation.json",
    15: "cases/fixtures/ch15-findings-retest-risk.json",
}
ROUTE = {
    "source": DOCUMENT,
    "destination": "cases/part-ii-assessment-risk-map/index.md",
    "section": "additional",
    "order": 319,
    "title": "第II部 横断読解：AssessmentからRisk判断へ",
}
PREFLIGHT = "python3 scripts/check_part02_contract.py --no-regressions"


def same(left, right):
    """JSON equality must not equate false with 0, or true with 1."""
    return json.dumps(
        left, sort_keys=True, ensure_ascii=False, allow_nan=False
    ) == json.dumps(right, sort_keys=True, ensure_ascii=False, allow_nan=False)


def at(data, path):
    value = data
    for part in path:
        value = value[part]
    return value


def boundary_checks(data):
    """Return stable (claim, source path, expected value) observations.

    Paths are fixed Python tuples, not a user-controlled query language. Reference
    RHS values come from their actual parent records; missing parents fail closed.
    """
    checks = []

    def expect(label, chapter, path, expected):
        checks.append((label, (chapter, *path), expected))

    def link(label, chapter, path, parent, parent_path):
        expect(label, chapter, path, at(data[parent], parent_path))

    expect("P2-source-inventory", 9, ("record", "roeId"), "ROE-2026-009")
    expect("P2-roe-version", 9, ("record", "version"), 1)
    expect("P2-roe-draft", 9, ("record", "status"), "Draft")
    expect("P2-case", 9, ("record", "parentCaseId"), "CASE-2026-001")
    expect(
        "P2-expiry", 9, ("parents", "authorizationExpiresAt"), "2026-08-19T09:00:00Z"
    )
    expect(
        "P2-window-start",
        9,
        ("parents", "authorizationWindowStartsAt"),
        "2026-08-06T00:00:00Z",
    )
    expect(
        "P2-window-end",
        9,
        ("parents", "authorizationWindowEndsAt"),
        "2026-08-06T08:00:00Z",
    )
    expect("P2-independent-roe", 11, ("authority", "id"), "ROE-2026-011")
    expect("P2-read-only", 11, ("readOnly",), True)
    expect("P2-no-network", 11, ("networkRequired",), False)
    if len(data[9]["objects"]) != 3:
        raise ValueError("P2-roe-object-inventory")
    for index, object_id in enumerate(
        ("OBJ-ROE09-CONFIG", "OBJ-ROE09-EVENT", "OBJ-ROE09-POLICY")
    ):
        expect(f"P2-roe-object-{index}", 9, ("objects", index, "objectId"), object_id)
    for chapter in SOURCES:
        expect(f"P2-synthetic-{chapter}", chapter, ("synthetic",), True)
        if chapter != 11:
            path = (
                ("safety", "executionAuthorized")
                if chapter == 13
                else ("executionAuthorized",)
            )
            expect(f"P2-no-execution-{chapter}", chapter, path, False)
    for chapter in (10, 12, 13, 14, 15):
        prefix = f"P2-parent-{chapter}"
        for name, expected in (
            ("caseId", "CASE-2026-001"),
            ("relation", "refines"),
            ("authorizationId", "AUTH-CASE-2026-001"),
            ("independentCaseId", "CASE-2026-011"),
            ("parentStateChanged", False),
            (
                "roeObjectIds",
                ["OBJ-ROE09-CONFIG", "OBJ-ROE09-EVENT", "OBJ-ROE09-POLICY"],
            ),
        ):
            expect(prefix + "-" + name, chapter, ("parents", name), expected)
        for target, source in (
            ("roeId", "roeId"),
            ("roeVersion", "version"),
            ("roeStatus", "status"),
        ):
            link(
                prefix + "-" + target,
                chapter,
                ("parents", target),
                9,
                ("record", source),
            )
        link(
            prefix + "-permission",
            chapter,
            ("parents", "roeExecutionAuthorized"),
            9,
            ("executionAuthorized",),
        )
        link(
            prefix + "-expiry",
            chapter,
            ("parents", "authorizationExpiresAt"),
            9,
            ("parents", "authorizationExpiresAt"),
        )
        expect(
            prefix + "-window",
            chapter,
            ("parents", "authorizationWindow"),
            [
                data[9]["parents"]["authorizationWindowStartsAt"],
                data[9]["parents"]["authorizationWindowEndsAt"],
            ],
        )
    link(
        "P2-recon-record",
        12,
        ("context", "reconRecordId"),
        10,
        ("record", "registerId"),
    )
    link(
        "P2-recon-candidate",
        12,
        ("context", "reconCandidateId"),
        10,
        ("candidates", 0, "candidateId"),
    )
    link(
        "P2-recon-asset",
        12,
        ("context", "parentAssetId"),
        10,
        ("candidates", 0, "parentAssetId"),
    )
    expect(
        "P2-recon-no-approval", 10, ("candidates", 0, "nextActionAuthorization"), False
    )
    link(
        "P2-identity-review",
        13,
        ("parentIdentity", "reviewId"),
        12,
        ("record", "reviewId"),
    )
    link("P2-identity-path", 13, ("parentIdentity", "pathId"), 12, ("paths", 3, "id"))
    expect("P2-binding", 13, ("parentIdentity", "currentBinding"), "Unknown")
    expect("P2-coverage", 13, ("parentIdentity", "coverage"), "Unknown")
    link("P2-assessment", 14, ("context", "assessmentId"), 13, ("record", "id"))
    link(
        "P2-platform-finding",
        14,
        ("validations", 0, "parentFindingId"),
        13,
        ("chains", 0, "finding", "id"),
    )
    for name in ("actualBuilds", "actualDeployments", "actualSignatureVerifications"):
        expect("P2-platform-" + name, 13, ("safety", name), 0)
    for target, source in (
        ("parentValidationRecord", ("record", "id")),
        ("parentHandoffId", ("handoffs", 0, "id")),
        ("parentHandoffStatus", ("handoffs", 0, "status")),
        ("parentValidationId", ("validations", 0, "id")),
        ("parentFindingId", ("validations", 0, "finding", "id")),
    ):
        link("P2-validation-" + target, 15, ("context", target), 14, source)
    for name, expected in (
        ("parentEvidenceRole", "method-reference-not-evidence-for-new-subject"),
        ("parentCompleteMeaning", "authored-reading-record-only"),
        ("parentSupportedMeaning", "supplied-two-criteria-only"),
        ("applicationRelation", "authored-variant-not-parent-current-binding"),
        ("parentIdentityBinding", "Unknown"),
        ("newApplication", "APP-FRT15-001"),
        ("independentEvidenceUsed", False),
        ("parentStateChanged", False),
    ):
        expect("P2-new-subject-" + name, 15, ("context", name), expected)
    link(
        "P2-parent-application",
        15,
        ("context", "parentIdentityApplication"),
        12,
        ("application", "appId"),
    )
    expect(
        "P2-alternatives",
        15,
        ("record", "scenarioMeaning"),
        "seven-independent-authored-alternatives-not-a-production-timeline",
    )
    for chapter, length in ((9, 3), (10, 2), (12, 5), (13, 3), (14, 2), (15, 5)):
        handoffs = data[chapter]["handoffs"]
        if type(handoffs) is not list or len(handoffs) != length:
            raise ValueError(f"P2-handoff-inventory-{chapter}")
        for index in range(length):
            name = "state" if chapter == 13 else "status"
            expect(
                f"P2-undelivered-{chapter}-{index}",
                chapter,
                ("handoffs", index, name),
                "planned-not-delivered",
            )
    findings, retests = data[15]["findings"], data[15]["retests"]
    if len(findings) != 7 or len(retests) != 5 or len({r["id"] for r in retests}) != 5:
        raise ValueError("P2-finding-retest-inventory")
    for index, finding in enumerate(findings):
        fp = ("findings", index)
        for name in ("validation", "decision", "reassessment"):
            link(
                f"P2-{index}-{name}-finding",
                15,
                (*fp, name, "findingId"),
                15,
                (*fp, "id"),
            )
        expect(
            f"P2-{index}-decision-not-permission",
            15,
            (*fp, "decision", "executionAuthorized"),
            False,
        )
        if finding["retestId"] is None:
            continue
        matches = [i for i, r in enumerate(retests) if r["id"] == finding["retestId"]]
        if len(matches) != 1:
            raise ValueError(f"P2-{index}-retest-reference")
        rp = ("retests", matches[0])
        for name, target in (
            ("findingId", "id"),
            ("subjectId", "subjectId"),
            ("beforeRevision", "subjectRevision"),
        ):
            link(f"P2-{index}-retest-{name}", 15, (*rp, name), 15, (*fp, target))
        link(
            f"P2-{index}-original-requirement",
            15,
            (*rp, "criteria", 0, "expected"),
            15,
            (*fp, "validation", "requirementPermission"),
        )
    return checks


def boundary_errors(data):
    errors = []
    try:
        if set(data) != set(SOURCES):
            return ["P2-source-inventory"]
        for label, path, expected in boundary_checks(data):
            try:
                if not same(at(data, path), expected):
                    errors.append(label + ": " + str(path))
            except (KeyError, IndexError, TypeError):
                errors.append(label + ": missing/invalid " + str(path))
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        errors.append("P2-reference-shape: " + str(exc))
    return errors


def field_inventory(document):
    # Full typed order binds headings/body/links without parsing source syntax.
    return [
        [f.field_type, f.element_kind, f.attribute, f.metadata_value("level"), f.text]
        for f in document.fields
    ]


def scan_errors(document):
    errors = [f"{d.location}: {d.code}" for d in document.diagnostics]
    for field in document.fields:
        findings = []
        if is_policy_scan_field(field):
            findings += scan_action_text(field.normalized_text, location=field.location)
        if is_policy_scan_field(field) or (
            field.field_type == "destination"
            and is_absolute_destination(field.normalized_text)
        ):
            findings += scan_host_policy(field.normalized_text, location=field.location)
        errors += [f"{f.location}: {f.category}" for f in findings]
    return errors


def document_errors(document, contract):
    errors = scan_errors(document)
    if field_inventory(document) != contract["fields"]:
        errors.append("P2-finite-reader-fields")
    return errors


def repository_errors(root, contract):
    package = load_json_strict(root / "package.json")["scripts"]
    steps = package["sync:docs"].split(" && ")
    errors = []
    if (
        package.get("check:part02") != "python3 scripts/check_part02_contract.py"
        or package["test"].split(" && ").count("npm run check:part02") != 1
        or steps[-3:]
        != [
            PREFLIGHT,
            "python3 scripts/sync_book_site.py --output docs",
            "npm run copy:notices",
        ]
        or steps.count(PREFLIGHT) != 1
    ):
        errors.append("P2-test-publication-entrypoints")
    if load_json_strict(root / "site-pages.json")["pages"].count(ROUTE) != 1:
        errors.append("P2-exact-route")
    if (
        contract.get("version") != VERSION
        or contract.get("projection") != PROJECTION_VERSION
        or contract.get("policy") != POLICY_VERSION
    ):
        errors.append("P2-versions")
    if contract.get("sourceFiles") != list(SOURCES.values()):
        errors.append("P2-source-files")
    return errors


def regressions(data, document, contract, probes):
    passed, errors = [], []

    def check(label, condition):
        (passed if condition else errors).append(label)

    check(
        "P2-positive-canonical",
        not boundary_errors(data) and not document_errors(document, contract),
    )
    check(
        "P2-positive-source-order",
        not boundary_errors(dict(reversed(list(data.items())))),
    )
    check("P2-json-bool-not-number", not same(False, 0) and not same(True, 1))
    # Every declared boundary has a missing-field counterexample. This finite
    # coverage does not claim an unbounded grammar or independent judgment test.
    for label, path, _ in boundary_checks(data):
        altered = deepcopy(data)
        del at(altered, path[:-1])[path[-1]]
        check(label + "-missing", bool(boundary_errors(altered)))
    for probe in probes["records"]:
        altered = deepcopy(data)
        path = (probe["chapter"], *probe["path"])
        at(altered, path[:-1])[path[-1]] = probe["value"]
        result = boundary_errors(altered)
        check(probe["id"], any(e.startswith(probe["error"]) for e in result))
    for i in range(len(document.fields)):
        altered = replace(
            document, fields=document.fields[:i] + document.fields[i + 1 :]
        )
        check(
            f"P2-field-{i}-missing",
            "P2-finite-reader-fields" in document_errors(altered, contract),
        )
    source_probes = probes["publication"]
    result = project_documents([(p["id"], p["source"]) for p in source_probes])
    for probe in source_probes:
        # Isolate shared safety from the immutable page inventory, so a failing
        # snapshot cannot masquerade as proof that unsafe prose was detected.
        errors_found = scan_errors(result.document(probe["id"]))
        check(probe["id"], bool(errors_found) == probe["unsafe"])
    check(
        "P2-frozen-counterexample-count",
        len(probes["records"]) == 18 and len(source_probes) == 10,
    )
    ids = [p["id"] for p in probes["records"] + source_probes]
    check(
        "P2-probe-ownership",
        len(ids) == len(set(ids))
        and all(p.get("invariant") for p in probes["records"] + source_probes),
    )
    return passed, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-regressions", action="store_true")
    args = parser.parse_args()
    try:
        data = {n: load_json_strict(ROOT / p) for n, p in SOURCES.items()}
        contract = load_json_strict(ROOT / CONTRACT)
        document = project_documents(
            {DOCUMENT: (ROOT / DOCUMENT).read_text(encoding="utf-8")}
        ).document(DOCUMENT)
        errors = (
            boundary_errors(data)
            + document_errors(document, contract)
            + repository_errors(ROOT, contract)
        )
        passed = []
        if not errors and not args.no_regressions:
            passed, failures = regressions(
                data, document, contract, load_json_strict(ROOT / PROBES)
            )
            errors += failures
        if errors:
            print("Part II contract failed:\n" + "\n".join(errors), file=sys.stderr)
            return 1
        print(
            f"Part II contract passed: {len(boundary_checks(data))} boundary observations, "
            f"{len(document.fields)} typed fields, {len(passed)} finite regressions; "
            f"Projection {PROJECTION_VERSION} / Policy {POLICY_VERSION}."
        )
        return 0
    except (
        OSError,
        ValueError,
        TypeError,
        KeyError,
        ManifestError,
        ProjectionRuntimeError,
    ) as exc:
        print(f"Part II contract failed closed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
