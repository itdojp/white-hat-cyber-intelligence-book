#!/usr/bin/env python3
"""Chapter16 finite selection/semantics; shared Projection and Policy own syntax."""

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
from scripts.chapter16_model import (  # noqa: E402
    DATA,
    SCHEMA,
    CONTRACT,
    DOCUMENTS,
    PARENTS,
    SOURCES,
    STATES,
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

PREFLIGHT = tuple(
    f"python3 scripts/check_chapter{n:02}_contract.py --no-regressions"
    for n in (6, 7, 8, 9, 10, 12, 13, 14, 15, 16)
) + (
    "python3 scripts/check_chapter18_contract.py --no-regressions",
    "python3 scripts/check_chapter19_contract.py --no-regressions",
    "python3 scripts/check_chapter20_contract.py --no-regressions",
    "python3 scripts/check_chapter21_contract.py --no-regressions",
    "python3 scripts/check_chapter22_contract.py --no-regressions",
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
    """The dedicated full-leaf section owns exactly one row for every JSON leaf."""
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
    return [] if actual == expected else ["ART24 full JSON leaf / Case field parity"]


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
            errors.append("ART24 body/end-reference Source ownership")
    return errors


def parent_errors(data, root):
    p = data["parents"]
    b, s, f, d = (
        strict(read_regular(root, path))
        for path in (
            "cases/fixtures/ch05-attack-behavior.json",
            "cases/fixtures/ch06-signal-flow.json",
            "cases/fixtures/ch15-findings-retest-risk.json",
            "cases/fixtures/ch17-detection-engineering-fixture.json",
        )
    )
    found = next(x for x in f["findings"] if x["id"] == p["findingId"])
    handoff = next(x for x in f["handoffs"] if x["id"] == p["handoffId"])
    pairs = [
        (p["behaviorMapId"], b["mapId"]),
        (p["signalMapId"], s["mapId"]),
        (p["findingRecordId"], f["record"]["id"]),
        (p["findingSubjectId"], found["subjectId"]),
        (p["findingRevision"], found["subjectRevision"]),
        (p["handoffStatus"], handoff["status"]),
        (p["detectionRecordId"], d["detectionValidationRecordId"]),
        (p["detectionId"], d["detectionId"]),
        (data["record"]["caseId"], d["caseId"]),
        (p["telemetryIds"], [x["id"] for x in d["telemetryContracts"]]),
    ]
    ok = (
        all(a == b for a, b in pairs)
        and p["behaviorId"] in [x["rowId"] for x in b["rows"]]
        and p["signalFlowId"] in [x["flowId"] for x in s["flows"]]
        and data["record"]["subjectId"] != found["subjectId"]
    )
    return [] if ok else ["ART24 direct parent links / subject separation"]


def repository_errors(data, contract, root=ROOT):
    errors = parent_errors(data, root)
    if list(contract["parentDigests"]) != list(PARENTS):
        errors.append("ART24 parent inventory")
    for path, expected in contract["parentDigests"].items():
        if hashlib.sha256(read_regular(root, path)).hexdigest() != expected:
            errors.append(path + ": parent/shared modified")
    package = load_json_strict(root / "package.json")["scripts"]
    if (
        package.get("check:chapter16") != "python3 scripts/check_chapter16_contract.py"
        or package["test"].split(" && ").count("npm run check:chapter16") != 1
        or package["sync:docs"].split(" && ") != list(PREFLIGHT)
    ):
        errors.append("ART24 root test/preflight exactly once before generation")
    routes = load_json_strict(root / "site-pages.json")
    for kind in ("pages", "staticFiles"):
        for route in contract[kind]:
            if routes[kind].count(route) != 1:
                errors.append("ART24 exact route: " + route["source"])
    order = [
        x["source"]
        for x in sorted(routes["pages"], key=lambda x: x["order"])
        if x["section"] == "chapters"
    ]
    if (
        not order.index("manuscript/15-findings-retest-risk.md")
        < order.index(DOCUMENTS[0])
        < order.index("manuscript/17-detection-engineering.md")
    ):
        errors.append("ART24 navigation 15/16/17")
    sources = load_json_strict(root / "references/sources.json")
    if sources["checkedAt"] != "2026-07-25" or {
        s["id"] for s in sources["sources"] if 16 in s["chapters"]
    } != set(SOURCES):
        errors.append("ART24 scoped Source mapping/baseline")
    for sid in SOURCES:
        source = next(s for s in sources["sources"] if s["id"] == sid)
        if any(source[k] != v for k, v in contract["sourceIdentity"][sid].items()):
            errors.append("ART24 reviewed Source identity: " + sid)
        if not meets_audit_baseline(
            source["checkedAt"], "2026-09-21"
        ) or not meets_audit_baseline(source["nextReviewAt"], "2026-12-21"):
            errors.append("ART24 Source review date: " + sid)
    for path, markers in contract["indices"].items():
        text = (root / path).read_text(encoding="utf-8")
        if any(m not in text for m in markers):
            errors.append("ART24 index: " + path)
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
            or list(contract["documents"]) != list(DOCUMENTS)
            or POLICY_VERSION != "1.2.0"
            or PROJECTION_VERSION != "1.1.0"
            or hashlib.sha256(read_regular(ROOT, SCHEMA)).hexdigest()
            != contract["schemaSha256"]
        ):
            raise ValueError("ART24 finite inventory/schema/shared versions")
        errors = validate_model(data, schema, contract)
        errors += repository_errors(data, contract)
        source = {p: read_regular(ROOT, p).decode("utf-8") for p in DOCUMENTS}
        projection = project_documents(source)
        if [d.document_id for d in projection.documents] != list(DOCUMENTS):
            raise ValueError("ART24 complete document projection order")
        for doc in projection.documents:
            errors += document_errors(doc, contract["documents"][doc.document_id], data)
        count = 0
        if not args.no_regressions:
            from scripts.chapter16_regressions import run_regressions

            count, problems = run_regressions(
                data, schema, contract, source, projection
            )
            errors += problems
        if errors:
            for error in errors:
                print("ERROR:", error)
            return 1
        print(
            f"Chapter 16 contract passed: 4 complete documents; 10 ART-24 contrasts / {len(STATES)} states / 24 receipts; {count} regressions; Policy {POLICY_VERSION}; Projection {PROJECTION_VERSION}; offline record-only / executionAuthorized=false"
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
        print("ERROR: Chapter16 fail closed:", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
