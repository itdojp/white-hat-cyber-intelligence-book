#!/usr/bin/env python3
"""Chapter19 finite selection/semantics; shared Projection and Policy own syntax."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.chapter19_model import (  # noqa: E402
    DATA,
    SCHEMA,
    CONTRACT,
    CORPUS,
    DOCUMENTS,
    PARENTS,
    SOURCES,
    strict,
    read_regular,
    validate_model,
    case_groups,
)
from scripts.check_editorial_input_manifest import ManifestError, load_json_strict  # noqa: E402
from scripts.check_representative_gate import SOURCE_ID_RE  # noqa: E402
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
from scripts.source_audit import meets_audit_baseline  # noqa: E402
from scripts.chapter19_decisions import VERSION as DECISION_VERSION  # noqa: E402

PREFLIGHT = tuple(
    f"python3 scripts/check_chapter{n:02}_contract.py --no-regressions"
    for n in (6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22)
) + (
    "python3 scripts/check_part03_contract.py --no-regressions",
    "python3 scripts/check_part02_contract.py --no-regressions",
    "python3 scripts/sync_book_site.py --output docs",
    "npm run copy:notices",
)


def identity(field):
    return [
        field.field_type,
        field.element_kind,
        field.attribute,
        field.metadata_value("level"),
        field.text,
        field.location,
    ]


def inventory(document):
    return [identity(f) for f in document.fields]


def scan_document(document, spec):
    errors = [f"{d.location}: {d.code}: {d.reason}" for d in document.diagnostics]
    provenance = spec["hostProvenance"]
    counts = Counter(
        json.dumps(identity(f), ensure_ascii=False) for f in document.fields
    )
    for item in provenance:
        if counts[json.dumps(item, ensure_ascii=False)] != 1:
            errors.append(document.document_id + ": exact provenance cardinality")
    for field in document.fields:
        findings = []
        if is_policy_scan_field(field):
            findings.extend(
                scan_action_text(field.normalized_text, location=field.location)
            )
        if (
            is_policy_scan_field(field)
            or (
                field.field_type == "destination"
                and is_absolute_destination(field.normalized_text)
            )
        ) and identity(field) not in provenance:
            findings.extend(
                scan_host_policy(field.normalized_text, location=field.location)
            )
        errors += [f"{field.location}: {f.category}: {f.reason}" for f in findings]
    return errors


def case_errors(document, data):
    """The dedicated artifact-leaf section owns exactly one row for every displayed artifact leaf."""
    actual, active = [], False
    for field in document.fields:
        if (
            field.field_type == "reader_visible_text"
            and field.element_kind == "heading"
        ):
            if field.metadata_value("level") == 2:
                active = field.text == "全欄の読み方"
        if active and is_policy_scan_field(field) and field.element_kind == "table_row":
            actual.append(field.text)
    expected = []
    for title, rows in case_groups(data):
        expected += [
            " ".join((title + " Field Value " + k + " " + v).split()) for k, v in rows
        ]
    return [] if actual == expected else ["ART25 artifact leaf / Case field parity"]


def document_errors(document, spec, data):
    errors = scan_document(document, spec)
    if inventory(document) != spec["fields"]:
        errors.append(
            document.document_id + ": finite publication fields/order/locations"
        )
    if document.document_id == DOCUMENTS[2]:
        errors += case_errors(document, data)
    if document.document_id == DOCUMENTS[0]:
        body, refs, in_refs = set(), set(), False
        for f in document.fields:
            if f.element_kind == "heading" and f.metadata_value("level") == 2:
                in_refs = f.text == "参考文献・Source Note ID"
            if is_policy_scan_field(f):
                (refs if in_refs else body).update(SOURCE_ID_RE.findall(f.text))
        if body != set(SOURCES) or refs != set(SOURCES):
            errors.append("ART25 body/end-reference Source ownership")
    return errors


def parent_errors(data, root):
    p = data["parents"]
    t = strict(read_regular(root, "cases/fixtures/ch16-telemetry-coverage.json"))
    d = strict(
        read_regular(root, "cases/fixtures/ch17-detection-engineering-fixture.json")
    )
    h = strict(read_regular(root, "cases/fixtures/ch18-threat-hunting.json"))
    th = next(x for x in t["handoffs"] if x["id"] == p["telemetryHandoffId"])
    hh = next(x for x in h["contrasts"][0]["handoffs"] if x["id"] == p["huntHandoffId"])
    pairs = [
        (p["telemetryMapId"], t["record"]["id"]),
        (p["telemetryRowIds"], th["rowIds"]),
        (p["detectionRecordId"], d["detectionValidationRecordId"]),
        (p["detectionId"], d["detectionId"]),
        (data["record"]["parentCaseId"], d["caseId"]),
        (p["huntRecordId"], h["record"]["id"]),
        (p["huntCaseId"], h["record"]["caseId"]),
        (p["huntFindingId"], h["contrasts"][0]["judgment"]["findingId"]),
    ]
    ok = all(a == b for a, b in pairs)
    ok = ok and all(
        x["targetChapter"] == 19
        and x["status"] == "planned-not-delivered"
        and x["receiptId"] is None
        and x["executionAuthorized"] is False
        for x in (th, hh)
    )
    ok = (
        ok
        and p["parentHandoffStatus"] == "planned-not-delivered"
        and p["parentReceiptId"] is None
    )
    ok = ok and all(
        p[k] is False
        for k in (
            "authorityTransferred",
            "evidenceTransferred",
            "parentHandoffReceived",
            "parentStateChanged",
        )
    )
    subjects = [r["input"]["context"]["subject"] for r in data["contrasts"]]
    ok = ok and not set(subjects) & {t["record"]["subjectId"], h["record"]["subjectId"]}
    return [] if ok else ["ART25 parent direct IDs / undelivered / non-inheritance"]


def repository_errors(data, contract, root=ROOT):
    errors = parent_errors(data, root)
    if list(contract["parentDigests"]) != list(PARENTS):
        errors.append("ART25 parent inventory")
    for path, expected in contract["parentDigests"].items():
        if hashlib.sha256(read_regular(root, path)).hexdigest() != expected:
            errors.append(path + ": parent/shared modified")
    package = load_json_strict(root / "package.json")["scripts"]
    if (
        package.get("check:chapter19") != "python3 scripts/check_chapter19_contract.py"
        or package["test"].split(" && ").count("npm run check:chapter19") != 1
        or package["sync:docs"].split(" && ") != list(PREFLIGHT)
    ):
        errors.append("ART25 root test/preflight exactly once before generation")
    routes = load_json_strict(root / "site-pages.json")
    for kind in ("pages", "staticFiles"):
        for route in contract[kind]:
            if routes[kind].count(route) != 1:
                errors.append("ART25 exact route: " + route["source"])
    order = [
        p["source"]
        for p in sorted(routes["pages"], key=lambda p: p["order"])
        if p["section"] == "chapters"
    ]
    if (
        not order.index("manuscript/18-threat-hunting.md")
        < order.index(DOCUMENTS[0])
        < order.index("manuscript/25-structured-analysis-attribution.md")
    ):
        errors.append("ART25 navigation 18/19/25")
    sources = load_json_strict(root / "references/sources.json")
    if sources["checkedAt"] != "2026-07-25" or {
        s["id"] for s in sources["sources"] if 19 in s["chapters"]
    } != set(SOURCES):
        errors.append("ART25 scoped Source mapping/baseline")
    for sid in SOURCES:
        source = next(s for s in sources["sources"] if s["id"] == sid)
        if any(source[k] != v for k, v in contract["sourceIdentity"][sid].items()):
            errors.append("ART25 reviewed Source identity: " + sid)
        if not meets_audit_baseline(
            source["checkedAt"], "2026-09-23"
        ) or not meets_audit_baseline(source["nextReviewAt"], "2026-11-08"):
            errors.append("ART25 Source review date: " + sid)
    for path, markers in contract["indices"].items():
        text = (root / path).read_text(encoding="utf-8")
        if any(m not in text for m in markers):
            errors.append("ART25 index: " + path)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-regressions", action="store_true")
    args = parser.parse_args()
    try:
        data, schema, contract = (
            strict(read_regular(ROOT, p)) for p in (DATA, SCHEMA, CONTRACT)
        )
        if (
            contract["schemaVersion"] != "1.0.0"
            or contract["decisionVersion"] != DECISION_VERSION
            or list(contract["documents"]) != list(DOCUMENTS)
            or POLICY_VERSION != "1.2.0"
            or PROJECTION_VERSION != "1.1.0"
            or hashlib.sha256(read_regular(ROOT, SCHEMA)).hexdigest()
            != contract["schemaSha256"]
            or hashlib.sha256(read_regular(ROOT, CORPUS)).hexdigest()
            != contract["corpusSha256"]
        ):
            raise ValueError("ART25 finite inventory/schema/shared versions")
        errors = validate_model(data, schema, contract)
        errors += repository_errors(data, contract)
        source = {p: read_regular(ROOT, p).decode("utf-8") for p in DOCUMENTS}
        projection = project_documents(source)
        if [d.document_id for d in projection.documents] != list(DOCUMENTS):
            raise ValueError("ART25 complete document projection order")
        for doc in projection.documents:
            errors += document_errors(doc, contract["documents"][doc.document_id], data)
        count = 0
        if not args.no_regressions:
            from scripts.chapter19_regressions import run_regressions

            count, problems = run_regressions(
                data, schema, contract, source, projection
            )
            errors += problems
        if errors:
            for error in errors:
                print("ERROR:", error)
            return 1
        print(
            f"Chapter 19 contract passed: 4 complete documents; 12 ART-25 contrasts / 7 states; {count} regressions; Policy {POLICY_VERSION}; Projection {PROJECTION_VERSION}; offline record-only / executionAuthorized=false"
        )
        return 0
    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        StopIteration,
        ManifestError,
        ProjectionRuntimeError,
    ) as exc:
        print("ERROR: Chapter19 fail closed:", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
