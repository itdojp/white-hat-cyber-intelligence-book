#!/usr/bin/env python3
"""Chapter20 selection/semantics; shared Projection and Policy own all syntax."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.chapter20_model import (  # noqa: E402
    DATA,
    SCHEMA,
    CONTRACT,
    CORPUS,
    DOCUMENTS,
    PARENTS,
    SOURCES,
    INDEX_PATHS,
    strict,
    read_regular,
    validate_model,
    case_groups,
)
from scripts.chapter20_timeline import (  # noqa: E402
    VERSION,
    digest,
    evaluate,
    instant,
    interval,
    utc_text,
)
from scripts.check_editorial_input_manifest import ManifestError  # noqa: E402
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
from scripts.sync_book_site import BASE_PAGES  # noqa: E402

PREFLIGHT = tuple(
    f"python3 scripts/check_chapter{n:02}_contract.py --no-regressions"
    for n in (6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 18, 19, 20)
) + (
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


def headings(document):
    return [
        [f.metadata_value("level"), f.text]
        for f in document.fields
        if f.field_type == "reader_visible_text" and f.element_kind == "heading"
    ]


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
            findings += scan_action_text(field.normalized_text, location=field.location)
        if (
            is_policy_scan_field(field)
            or (
                field.field_type == "destination"
                and is_absolute_destination(field.normalized_text)
            )
        ) and identity(field) not in provenance:
            findings += scan_host_policy(field.normalized_text, location=field.location)
        errors += [f"{field.location}: {f.category}: {f.reason}" for f in findings]
    return errors


def section_table_rows(document, heading):
    """Select an authored Chapter20 H2 surface from shared projected fields."""
    active, rows = False, []
    for field in document.fields:
        if (
            field.field_type == "reader_visible_text"
            and field.element_kind == "heading"
            and field.metadata_value("level") == 2
        ):
            active = field.text == heading
        if active and is_policy_scan_field(field) and field.element_kind == "table_row":
            rows.append(field.text)
    return rows


def numeric_example_errors(document, data):
    """Bind the short numeric reading tables, not just the full Artifact leaves."""
    errors, expected = [], []
    if document.document_id == DOCUMENTS[0]:
        clocks = {c["id"]: c for c in data["clocks"]}
        rows = {r["id"]: r for r in data["evidence"]}
        for eid in ("EV20-001", "EV20-002", "EV20-003", "EV20-005"):
            row = rows[eid]
            raw = row["payload"]["originalTime"]
            clock = clocks[row["payload"]["clockId"]]
            low, high = (utc_text(t) for t in interval(row, clocks))
            if {raw[:10], low[:10], high[:10]} != {"2026-09-01"}:
                errors.append("DFIR20 numeric example date scope")
            offset = f"{clock['offsetSeconds']:+d}" if clock["offsetSeconds"] else "0"
            expected.append(
                f"Evidence 原時刻 offset / 不確かさ 正規化区間 UTC {eid} {raw[11:]} "
                f"{offset}秒 / ±{clock['uncertaintySeconds']}秒 {low[11:19]}〜{high[11:19]}"
            )
        if section_table_rows(document, "3. 原時刻を幅のあるUTCへ変換する") != expected:
            errors.append("DFIR20 manuscript numeric table / supplied time parity")
    if document.document_id == DOCUMENTS[3]:
        judgments = {
            "TL-DFIR20-A": "EV20-005は後着で不採用。特定Changeの範囲は未確定、原因unresolved",
            "TL-DFIR20-B": "特定CHG20-001はApp BだけでApp Aを覆わない。別の許可と機構は不明、原因unresolved",
        }
        for snapshot in data["snapshots"]:
            result = evaluate(data, snapshot)
            cutoff, analysis = (
                utc_text(instant(snapshot[k])) for k in ("cutoff", "analysisAt")
            )
            if {cutoff[:10], analysis[:10]} != {"2026-09-01"}:
                errors.append("DFIR20 summary snapshot date scope")
            expected.append(
                f"Timeline Cutoff / Analysis Receipt / Event 保守説明と原因 {snapshot['id']} "
                f"{cutoff[11:16]} / {analysis[11:16]} {len(result['included'])} Receipt / "
                f"{len(result['timeline'])} Event {judgments[snapshot['id']]}"
            )
        if section_table_rows(document, "二つのSnapshot") != expected:
            errors.append("DFIR20 Case snapshot summary / input parity")
    return errors


def document_errors(document, spec, data):
    errors = scan_document(document, spec) + numeric_example_errors(document, data)
    if (
        digest(inventory(document)) != spec["projectionSha256"]
        or headings(document) != spec["headings"]
        or len(document.fields) != spec["fieldCount"]
    ):
        errors.append(document.document_id + ": finite fields/order/locations/headings")
    if document.document_id == DOCUMENTS[3]:
        actual, active = [], False
        for field in document.fields:
            if (
                field.field_type == "reader_visible_text"
                and field.element_kind == "heading"
            ):
                if field.metadata_value("level") == 2:
                    active = field.text == "全欄の読み方"
            if (
                active
                and is_policy_scan_field(field)
                and field.element_kind == "table_row"
            ):
                actual.append(field.text)
        expected = [
            " ".join((title + " Field Value " + k + " " + v).split())
            for title, rows in case_groups(data)
            for k, v in rows
        ]
        if actual != expected:
            errors.append("DFIR20 all artifact/evidence leaves / Case parity")
    if document.document_id == DOCUMENTS[0]:
        body, refs, in_refs = set(), set(), False
        for field in document.fields:
            if field.element_kind == "heading" and field.metadata_value("level") == 2:
                in_refs = field.text == "参考文献・Source Note ID"
            if is_policy_scan_field(field):
                (refs if in_refs else body).update(SOURCE_ID_RE.findall(field.text))
        if body != set(SOURCES) or refs != set(SOURCES):
            errors.append("DFIR20 body/end-reference Source ownership")
    return errors


def repository_errors(data, contract, root=ROOT):
    errors = []
    if list(contract["parentDigests"]) != list(PARENTS):
        errors.append("DFIR20 fixed parent/shared inventory")
    else:
        for path in PARENTS:
            if (
                hashlib.sha256(read_regular(root, path)).hexdigest()
                != contract["parentDigests"][path]
            ):
                errors.append(path + ": parent/shared modified")
    parent = strict(read_regular(root, "cases/fixtures/ch19-incident-response.json"))
    contrast = next(r for r in parent["contrasts"] if r["id"] == "ICASE19-004")
    handoff = next(h for h in contrast["handoffs"] if h["targetChapter"] == 20)
    p = data["parent"]
    actual = {
        "recordId": parent["record"]["id"],
        "contrastId": contrast["id"],
        "decisionId": handoff["sourceDecisionId"],
        "handoffId": handoff["id"],
        "questionId": handoff["questionId"],
        "plannedTimelineId": handoff["plannedRecordId"],
        "status": handoff["status"],
        "receiptId": handoff["receiptId"],
        "executionAuthorized": handoff["executionAuthorized"],
        "use": "method-reference-only",
    }
    if (
        p != actual
        or p["status"] != "planned-not-delivered"
        or p["receiptId"] is not None
        or p["executionAuthorized"] is not False
        or data["record"]["parentCaseId"] != parent["record"]["caseId"]
        or data["record"]["relation"] != "refines"
        or data["context"]["subjectId"]
        in {r["input"]["context"]["subject"] for r in parent["contrasts"]}
        or p["plannedTimelineId"] in {s["id"] for s in data["snapshots"]}
    ):
        errors.append("DFIR20 direct parent IDs / non-inheritance / undelivered")
    package = strict(read_regular(root, "package.json"))["scripts"]
    if (
        package.get("check:chapter20") != "python3 scripts/check_chapter20_contract.py"
        or package["test"].split(" && ").count("npm run check:chapter20") != 1
        or package["sync:docs"].split(" && ") != list(PREFLIGHT)
    ):
        errors.append("DFIR20 root test/preflight exactly once")
    routes = strict(read_regular(root, "site-pages.json"))
    if (
        sum(
            p.source == DOCUMENTS[1]
            and p.destination == "templates/incident-timeline/index.md"
            for p in BASE_PAGES
        )
        != 1
    ):
        errors.append("DFIR20 legacy ART07 public URL")
    for kind in ("pages", "staticFiles"):
        for route in contract[kind]:
            if routes[kind].count(route) != 1:
                errors.append("DFIR20 exact route: " + route["source"])
    order = [
        p["source"]
        for p in sorted(routes["pages"], key=lambda p: p["order"])
        if p["section"] == "chapters"
    ]
    if not (
        order.index("manuscript/19-incident-response.md")
        < order.index(DOCUMENTS[0])
        < order.index("manuscript/25-structured-analysis-attribution.md")
    ):
        errors.append("DFIR20 navigation 19/20/25")
    sources = strict(read_regular(root, "references/sources.json"))
    if sources["checkedAt"] != "2026-07-25" or {
        s["id"] for s in sources["sources"] if 20 in s["chapters"]
    } != set(SOURCES):
        errors.append("DFIR20 scoped Source mapping/baseline")
    for sid in SOURCES:
        source = next(s for s in sources["sources"] if s["id"] == sid)
        if any(source[k] != v for k, v in contract["sourceIdentity"][sid].items()):
            errors.append("DFIR20 reviewed Source identity: " + sid)
        if not meets_audit_baseline(source["checkedAt"], "2026-09-25"):
            errors.append("DFIR20 scoped Source date: " + sid)
    if list(contract["indices"]) != list(INDEX_PATHS):
        errors.append("DFIR20 index inventory")
    else:
        for path in INDEX_PATHS:
            text = read_regular(root, path).decode("utf-8")
            if any(m not in text for m in contract["indices"][path]):
                errors.append("DFIR20 index: " + path)
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
            or contract["timelineVersion"] != VERSION
            or list(contract["documents"]) != list(DOCUMENTS)
            or POLICY_VERSION != "1.2.0"
            or PROJECTION_VERSION != "1.1.0"
            or hashlib.sha256(read_regular(ROOT, SCHEMA)).hexdigest()
            != contract["schemaSha256"]
            or hashlib.sha256(read_regular(ROOT, CORPUS)).hexdigest()
            != contract["corpusSha256"]
        ):
            raise ValueError("DFIR20 frozen inventory/schema/shared versions")
        errors = validate_model(data, schema, contract) + repository_errors(
            data, contract
        )
        source = {p: read_regular(ROOT, p).decode("utf-8") for p in DOCUMENTS}
        projection = project_documents(source)
        if [d.document_id for d in projection.documents] != list(DOCUMENTS):
            raise ValueError("DFIR20 full document projection order")
        for doc in projection.documents:
            errors += document_errors(doc, contract["documents"][doc.document_id], data)
        count = 0
        if not args.no_regressions:
            from scripts.chapter20_regressions import run_regressions

            count, problems = run_regressions(
                data, schema, contract, source, projection
            )
            errors += problems
        if errors:
            for error in errors:
                print("ERROR:", error)
            return 1
        print(
            f"Chapter 20 contract passed: 5 complete documents; ART-07/26; 5 receipts / 2 cutoffs / 6 claims; {count} regressions; Policy {POLICY_VERSION}; Projection {PROJECTION_VERSION}; offline record-only / executionAuthorized=false"
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
        print("ERROR: Chapter20 fail closed:", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
