#!/usr/bin/env python3
"""Part III finite cross-record/reader contract. No chapter evaluator or parser."""

from __future__ import annotations
import argparse
from copy import deepcopy
from dataclasses import replace
import json
import os
from pathlib import Path
import stat
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.check_editorial_input_manifest import (  # noqa: E402 - direct CLI root bootstrap
    _reject_constant,
    _reject_duplicate_keys,
    ManifestError,
)
from scripts.content_safety_policy import (  # noqa: E402 - direct CLI root bootstrap
    POLICY_VERSION,
    scan_action_text,
    scan_host_policy,
)
from scripts.publication_projection import (  # noqa: E402 - direct CLI root bootstrap
    PROJECTION_VERSION,
    ProjectionRuntimeError,
    project_documents,
    is_policy_scan_field,
    is_absolute_destination,
)

VERSION = "1.0.0"
DOCUMENT = "cases/part-iii-detection-improvement-map.md"
CONTRACT = "tests/fixtures/part03/publication-contract.json"
CORPUS = "tests/fixtures/part03/counterexamples.json"
SOURCES = {
    16: "cases/fixtures/ch16-telemetry-coverage.json",
    17: "cases/fixtures/ch17-detection-engineering-fixture.json",
    18: "cases/fixtures/ch18-threat-hunting.json",
    19: "cases/fixtures/ch19-incident-response.json",
    20: "cases/fixtures/ch20-dfir-timeline-causality.json",
    21: "cases/fixtures/ch21-control-validation.json",
    22: "cases/fixtures/ch22-measurement-improvement.json",
}
INPUTS = (
    *SOURCES.values(),
    DOCUMENT,
    CONTRACT,
    CORPUS,
    "package.json",
    "site-pages.json",
    "cases/index.md",
)
ROUTE = {
    "source": DOCUMENT,
    "destination": "cases/part-iii-detection-improvement-map/index.md",
    "section": "additional",
    "order": 320,
    "title": "第III部 横断読解：観測から改善判断へ",
}
PREFLIGHT = "python3 scripts/check_part03_contract.py --no-regressions"


def read_regular(root, relative):
    """Fixed repository files only; not a hostile concurrent-filesystem sandbox."""
    if relative not in INPUTS or root.is_symlink():
        raise ValueError("P3-fixed-input")
    path = root / relative
    if any(
        p.is_symlink()
        for p in (path, *path.parents)
        if p != root.parent and p.is_relative_to(root)
    ):
        raise ValueError("P3-symlink-input")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError("P3-regular-input")
        raw = stream.read(1048577)
    if len(raw) > 1048576:
        raise ValueError("P3-input-size")
    return raw.decode("utf-8")


def load(root, path):
    return json.loads(
        read_regular(root, path),
        object_pairs_hook=_reject_duplicate_keys,
        parse_constant=_reject_constant,
    )


def same(a, b):
    return json.dumps(
        a, sort_keys=True, ensure_ascii=False, allow_nan=False
    ) == json.dumps(b, sort_keys=True, ensure_ascii=False, allow_nan=False)


def at(value, path):
    for key in path:
        value = value[key]
    return value


def boundary_checks(data):
    """Independently stated literals bind producers; relations bind consumers."""
    checks = []

    def expected(n, p, v, label):
        checks.append((label, (n, *p), v))

    def link(n, p, parent, q, literal):
        expected(parent, q, literal, f"producer-{len(checks) + 1}")
        expected(n, p, at(data[parent], q), f"consumer-{len(checks) + 1}")

    for n in (16, 18, 19):
        link(
            n,
            ("parents", "detectionRecordId"),
            17,
            ("detectionValidationRecordId",),
            "DVR-2026-017-001",
        )
        link(n, ("parents", "detectionId"), 17, ("detectionId",), "DET-2026-017-001")
    for n, i, prefix in [(18, 1, "handoffId"), (19, 2, "telemetryHandoffId")]:
        link(n, ("parents", "telemetryMapId"), 16, ("record", "id"), "TCM-2026-016")
        link(n, ("parents", prefix), 16, ("handoffs", i, "id"), f"HOF-TCM16-{n}")
        link(
            n,
            ("parents", "telemetryRowIds"),
            16,
            ("handoffs", i, "rowIds"),
            ["ROW-TCM16-005", "ROW-TCM16-006", "ROW-TCM16-007"]
            if n == 18
            else ["ROW-TCM16-003", "ROW-TCM16-008"],
        )
    link(18, ("parents", "fixtureSetId"), 17, ("fixtureSetId",), "FXSET-2026-017")
    link(
        18,
        ("parents", "threatHypothesisId"),
        17,
        ("threatHypotheses", 0, "id"),
        "TH-DET-2026-001",
    )
    for a, b, v in [
        ("huntRecordId", ("record", "id"), "HUNT-2026-018-001"),
        ("huntCaseId", ("record", "caseId"), "CASE-HUNT-2026-001"),
        ("huntFindingId", ("contrasts", 0, "judgment", "findingId"), "FND-HUNT18-001"),
        ("huntHandoffId", ("contrasts", 0, "handoffs", 1, "id"), "HOF-HUNT18-001-2"),
    ]:
        link(19, ("parents", a), 18, b, v)
    for a, b, v in [
        ("recordId", ("record", "id"), "IAP-2026-019-001"),
        ("contrastId", ("contrasts", 3, "id"), "ICASE19-004"),
        ("decisionId", ("contrasts", 3, "input", "decision", "id"), "DEC-IR19-004"),
        ("handoffId", ("contrasts", 3, "handoffs", 0, "id"), "HOF-IR19-004-20"),
        ("questionId", ("contrasts", 3, "handoffs", 0, "questionId"), "EQ-IR19-004-20"),
        (
            "plannedTimelineId",
            ("contrasts", 3, "handoffs", 0, "plannedRecordId"),
            "TL-IR19-004",
        ),
    ]:
        link(20, ("parent", a), 19, b, v)
    for a, b, v in [
        ("dfirRecordId", ("record", "id"), "DFIR-2026-020-001"),
        ("dfirRcaId", ("snapshots", 1, "rca", "id"), "RCA-DFIR20-B"),
        ("dfirControlId", ("handoffs", 0, "controlId"), "CTL-DFIR20-001"),
        ("dfirHandoffId", ("handoffs", 0, "id"), "HOF-DFIR20-21"),
    ]:
        link(21, ("parentReferences", a), 20, b, v)
    for a, b, v in [
        ("controlValidationRecordId", ("record", "id"), "CVP-2026-021-001"),
        ("controlRetestId", ("retest", "id"), "RT-CV21-003"),
        ("beforeScenarioId", ("scenarios", 2, "id"), "SCN-CV21-003"),
        ("afterScenarioId", ("scenarios", 9, "id"), "SCN-CV21-010"),
        (
            "beforeEvidenceId",
            ("scenarios", 2, "observations", 0, "id"),
            "EVD-CV21-003-01",
        ),
        (
            "afterEvidenceId",
            ("scenarios", 9, "observations", 0, "id"),
            "EVD-CV21-010-01",
        ),
        ("parentHandoffId", ("handoff", "id"), "HOF-CV21-22"),
    ]:
        link(22, ("parentReferences", a), 21, b, v)
    for n in (16, 18, 19, 20, 21, 22):
        for key, v in [
            ("synthetic", True),
            ("readOnly", True),
            ("networkRequired", False),
            ("executionAuthorized", False),
        ]:
            expected(n, (key,), v, f"{n}-{key}")
    for n in (16, 18, 19):
        for key in (
            "parentStateChanged",
            "authorityTransferred",
            "evidenceTransferred",
            "parentHandoffReceived",
        ):
            expected(n, ("parents", key), False, f"{n}-{key}")
        expected(
            n,
            ("parents", "evidenceRole"),
            "method-reference-not-evidence-for-new-subject",
            f"{n}-method",
        )
    for n in (21, 22):
        expected(n, ("parentReferences", "use"), "method-reference-only", f"{n}-method")
        for key in (
            "parentEvidenceTransferred",
            "parentStateChanged",
            "authorityTransferred",
        ):
            expected(n, ("parentReferences", key), False, f"{n}-{key}")
        for key, v in [
            ("parentRoeId", "ROE-2026-009"),
            ("parentRoeStatus", "Draft"),
            ("parentRoeVersion", 1),
            ("parentExpiresAt", "2026-08-19T09:00:00Z"),
            ("parentExecutionAuthorized", False),
            ("parentLabRuntimeExecuted", False),
        ]:
            expected(n, ("authorityBoundary", key), v, f"{n}-{key}")
    for n, p in [(16, ("handoffs", i)) for i in range(4)] + [
        (18, ("contrasts", 0, "handoffs", 1)),
        (19, ("contrasts", 3, "handoffs", 0)),
        (20, ("handoffs", 0)),
        (21, ("handoff",)),
        (22, ("handoff",)),
    ]:
        for key, v in [
            ("status", "planned-not-delivered"),
            ("receiptId", None),
            ("executionAuthorized", False),
        ]:
            expected(n, p + (key,), v, f"{n}-{p}-{key}")
    for p, v in [
        (("syntheticOnly",), True),
        (("offlineOnly",), True),
        (("incidentHandoff", "handoffId"), "HO-DET-2026-001"),
        (
            ("incidentHandoff", "requiredFields"),
            [
                "case_id",
                "detection_id",
                "evidence_ids",
                "coverage",
                "gap",
                "permitted_conclusion",
            ],
        ),
        (("coverageGapExample", "expectedOutcome"), "indeterminate"),
        (("coverageGapExample", "targetEventPresence"), "unknown"),
    ]:
        expected(17, p, v, f"17-{p}")
    for n, p, v, label in [
        (
            18,
            ("contrasts", 2, "judgment", "result"),
            "Negative finding",
            "limited-negative",
        ),
        (
            18,
            ("contrasts", 2, "judgment", "noCompromiseClaim"),
            False,
            "not-no-compromise",
        ),
        (18, ("contrasts", 4, "judgment", "result"), "Inconclusive", "producer-gap"),
        (20, ("record", "incidentId"), None, "no-borrowed-incident"),
        (20, ("context", "subjectId"), "SYNTH-DFIR20-001", "separate-subject"),
        (20, ("parent", "use"), "method-reference-only", "method"),
        (
            20,
            ("snapshots", 1, "expected", "claims", "CLM20-004", "status"),
            "undetermined",
            "cause-unknown",
        ),
        (21, ("scenarios", 2, "expectedLayers", 0, "result"), "Failed", "old-failed"),
        (
            21,
            ("scenarios", 9, "expectedLayers", 0, "result"),
            "Passed",
            "new-supplied-passed",
        ),
        (21, ("retest", "actualChangeExecuted"), False, "no-real-change"),
        (22, ("items", 4, "status"), "Verified", "bounded-verified"),
        (
            22,
            ("items", 4, "verification", "realEffectivenessVerified"),
            False,
            "not-effectiveness",
        ),
        (
            22,
            ("items", 4, "riskJudgment", "realRiskReductionMeasured"),
            False,
            "not-risk-reduction",
        ),
    ]:
        expected(n, p, v, f"{n}-{label}")
    expected(
        20,
        ("record", "incidentReferenceStatus"),
        "not-declared-in-this-bundle",
        "20-incident-reference",
    )
    expected(20, ("context", "revision"), "REV-DFIR20-001", "20-revision")
    expected(
        21,
        ("parentReferences", "dfirControlStatus"),
        "hypothesis-only",
        "21-parent-control-hypothesis",
    )
    expected(21, ("retest", "beforeRetained"), True, "21-before-retained")
    for i, ident in (
        (0, "FIX-2026-017-POS"),
        (1, "FIX-2026-017-NEG"),
        (2, "FIX-2026-017-BNM"),
    ):
        expected(17, ("fixtures", i, "fixtureId"), ident, f"17-fixture-{i}")
    for i, revision in ((2, "CTLREV-CV21-001"), (9, "CTLREV-CV21-002")):
        expected(
            21,
            ("scenarios", i, "controlRevision"),
            revision,
            f"21-control-revision-{i}",
        )
    for key, value in [
        ("subjectId", "SYNTH-IMP22-001"),
        ("subjectRevision", "INPUT-REV-002"),
        ("id", "VAL-IMP22-005"),
        ("evidenceId", "EVD-IMP22-V005"),
    ]:
        expected(22, ("items", 4, "verification", key), value, f"22-verification-{key}")
    expected(
        22,
        ("items", 4, "reassessment", "owner"),
        "SYN-IMP22-OWNER-005",
        "22-reassessment-owner",
    )
    expected(
        22,
        ("items", 4, "reassessment", "dueAt"),
        "2026-09-30T00:00:00Z",
        "22-reassessment-due",
    )
    for n, prefix, status_key, receipt_key, producer, producer_path in (
        (18, ("parents",), "handoffStatus", "handoffReceiptId", 16, ("handoffs", 1)),
        (
            19,
            ("parents",),
            "parentHandoffStatus",
            "parentReceiptId",
            18,
            ("contrasts", 0, "handoffs", 1),
        ),
        (20, ("parent",), "status", "receiptId", 19, ("contrasts", 3, "handoffs", 0)),
        (
            21,
            ("parentReferences",),
            "dfirHandoffStatus",
            "receiptId",
            20,
            ("handoffs", 0),
        ),
        (
            22,
            ("parentReferences",),
            "parentHandoffStatus",
            "parentReceiptId",
            21,
            ("handoff",),
        ),
    ):
        link(
            n,
            prefix + (status_key,),
            producer,
            producer_path + ("status",),
            "planned-not-delivered",
        )
        link(n, prefix + (receipt_key,), producer, producer_path + ("receiptId",), None)
    return checks


def boundary_errors(data):
    errors = []
    try:
        if set(data) != set(SOURCES):
            return ["P3-source-inventory"]
        for label, path, value in boundary_checks(data):
            try:
                if not same(at(data, path), value):
                    errors.append(label)
            except (KeyError, IndexError, TypeError):
                errors.append(label)
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        errors.append("P3-reference-shape: " + str(exc))
    return errors


def field_inventory(document):
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
        errors.append("P3-reader-fields")
    return errors


def repository_errors(root, contract):
    errors = []
    package = load(root, "package.json")["scripts"]
    steps = package["sync:docs"].split(" && ")
    if (
        package.get("check:part03") != "python3 scripts/check_part03_contract.py"
        or package["test"].split(" && ").count("npm run check:part03") != 1
        or steps.count(PREFLIGHT) != 1
        or steps[-4:]
        != [
            PREFLIGHT,
            "python3 scripts/check_part02_contract.py --no-regressions",
            "python3 scripts/sync_book_site.py --output docs",
            "npm run copy:notices",
        ]
    ):
        errors.append("P3-entrypoints")
    pages = load(root, "site-pages.json")["pages"]
    if (
        pages.count(ROUTE) != 1
        or sum(p["source"] == DOCUMENT for p in pages) != 1
        or sum(p["destination"] == ROUTE["destination"] for p in pages) != 1
    ):
        errors.append("P3-route")
    if f"({DOCUMENT.removeprefix('cases/')})" not in read_regular(
        root, "cases/index.md"
    ):
        errors.append("P3-reader-entry")
    if any(
        contract.get(k) != v
        for k, v in [
            ("version", VERSION),
            ("projection", PROJECTION_VERSION),
            ("policy", POLICY_VERSION),
            ("sourceFiles", list(SOURCES.values())),
        ]
    ):
        errors.append("P3-contract-owner")
    return errors


def regressions(data, document, contract, corpus):
    passed = []

    def check(label, condition):
        if not condition:
            raise ValueError("P3-regression: " + label)
        passed.append(label)

    check(
        "canonical",
        not boundary_errors(data) and not document_errors(document, contract),
    )
    check("source-order", not boundary_errors(dict(reversed(list(data.items())))))
    check("typed-json", not same(False, 0) and not same(True, 1))
    # Every declared boundary has a deletion and a wrong-type/value counterexample.
    for label, path, value in boundary_checks(data):
        changed = deepcopy(data)
        del at(changed, path[:-1])[path[-1]]
        check(label + "-missing", bool(boundary_errors(changed)))
        changed = deepcopy(data)
        at(changed, path[:-1])[path[-1]] = "not-the-supplied-value"
        check(label + "-changed", bool(boundary_errors(changed)))
    for probe in corpus["records"]:
        changed = deepcopy(data)
        for m in probe["mutations"]:
            at(changed, (m["chapter"], *m["path"][:-1]))[m["path"][-1]] = m["value"]
        check(probe["id"], bool(boundary_errors(changed)))
    for i in range(len(document.fields)):
        changed = replace(
            document, fields=document.fields[:i] + document.fields[i + 1 :]
        )
        check(f"field-{i}-missing", field_inventory(changed) != contract["fields"])
    projection = project_documents(
        [(p["id"], p["source"]) for p in corpus["publication"]]
    )
    for probe in corpus["publication"]:
        # Scan safety separately from the frozen reader inventory.
        projected = projection.document(probe["id"])
        findings = scan_errors(projected)
        check(probe["id"], bool(findings) == probe["unsafe"])
        check(
            probe["id"] + "-diagnostics",
            [d.code for d in projected.diagnostics] == probe["diagnosticCodes"],
        )
        if probe["findingCategory"] is not None:
            check(
                probe["id"] + "-policy-category",
                any(e.endswith(": " + probe["findingCategory"]) for e in findings),
            )
    ids = [p["id"] for p in corpus["records"] + corpus["publication"]]
    check(
        "corpus-owner",
        corpus["version"] == VERSION
        and len(ids) == len(set(ids))
        and all(p.get("invariant") for p in corpus["records"] + corpus["publication"]),
    )
    check(
        "corpus-count",
        len(corpus["records"]) == 27 and len(corpus["publication"]) == 12,
    )
    check("boundary-count", len(boundary_checks(data)) == 210)
    # Fixed-file reader failures are tested under this worktree, never in /tmp.
    scratch = ROOT / ".tmp"
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="part03-input-", dir=scratch) as directory:
        root = Path(directory)
        path = root / SOURCES[16]
        path.parent.mkdir(parents=True)

        def rejected(label, operation):
            try:
                operation()
            except (OSError, ValueError, ManifestError):
                check(label, True)
            else:
                check(label, False)

        for label, raw in (
            ("duplicate-key", b'{"a":1,"a":2}'),
            ("non-finite", b'{"a":NaN}'),
            ("invalid-utf8", b"\xff"),
            ("oversize", b" " * 1048577),
        ):
            path.write_bytes(raw)
            rejected(label, lambda: load(root, SOURCES[16]))
        path.unlink()
        rejected("missing-file", lambda: read_regular(root, SOURCES[16]))
        path.symlink_to(root / "absent")
        rejected("symlink", lambda: read_regular(root, SOURCES[16]))
        path.unlink()
        os.mkfifo(path)
        rejected("fifo", lambda: read_regular(root, SOURCES[16]))
        path.unlink()
        rejected("unowned-path", lambda: read_regular(root, "../outside.json"))
        path.write_text('{"ok":true}', encoding="utf-8")
        check("valid-input", load(root, SOURCES[16]) == {"ok": True})
    return passed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-regressions", action="store_true")
    args = parser.parse_args()
    try:
        data = {n: load(ROOT, p) for n, p in SOURCES.items()}
        contract = load(ROOT, CONTRACT)
        document = project_documents({DOCUMENT: read_regular(ROOT, DOCUMENT)}).document(
            DOCUMENT
        )
        errors = (
            boundary_errors(data)
            + document_errors(document, contract)
            + repository_errors(ROOT, contract)
        )
        if errors:
            raise ValueError("; ".join(errors))
        passed = (
            []
            if args.no_regressions
            else regressions(data, document, contract, load(ROOT, CORPUS))
        )
        print(
            f"Part III contract passed: {len(boundary_checks(data))} boundary observations; {len(document.fields)} typed fields; {len(passed)} finite regressions; Policy {POLICY_VERSION}; Projection {PROJECTION_VERSION}; references are not delivery or authority."
        )
        return 0
    except (
        OSError,
        ValueError,
        TypeError,
        KeyError,
        IndexError,
        ManifestError,
        ProjectionRuntimeError,
    ) as exc:
        print(f"Part III contract failed closed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
