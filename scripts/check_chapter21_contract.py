#!/usr/bin/env python3
"""Chapter21 finite selection/semantics; shared Projection and Policy own syntax."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.chapter21_model import (  # noqa: E402
    VERSION,
    DATA,
    SCHEMA,
    CONTRACT,
    CORPUS,
    DOCUMENTS,
    SOURCES,
    PARENTS,
    INDEX_PATHS,
    strict,
    read_regular,
    digest,
    summary,
    validate_model,
    case_groups,
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
    if len({json.dumps(p, ensure_ascii=False) for p in provenance}) != len(provenance):
        errors.append("CV21 duplicate provenance")
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


def section_rows(document, heading):
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


def reading_table_errors(document, data):
    errors = []
    if document.document_id == DOCUMENTS[2]:
        expected = [
            " ".join((title + " Field Value " + key + " " + value).split())
            for title, rows in case_groups(data)
            for key, value in rows
        ]
        if section_rows(document, "全欄の読み方") != expected:
            errors.append("CV21 all artifact leaves / Case parity")
        expected = [
            f"Scenario Layer Result Failure {s['id']} {r['layer']} {r['result']} "
            + (", ".join(r["failureClasses"]) or "なし")
            for s in data["scenarios"]
            for r in summary(s)
        ]
        if section_rows(document, "層別の供給結果") != expected:
            errors.append("CV21 Case layer summary / evaluated parity")
    if document.document_id == DOCUMENTS[0]:
        notes = (
            "blockedでも監査到達は別の問い",
            "同一Batchで配送失敗根拠がある",
            "Positiveの出力不一致、正常対比は保持",
            "EvidenceだけではOwnerと理由が足りない",
            "案はあっても権限根拠がない",
            "Positive fixture不足を検知失敗にしない",
            "未承認scopeのallowedは期待と矛盾",
            "同一Traceの供給比較だけを支持",
            "Primary到達とSecondary不足を分ける",
            "003を保持し、版を変えた供給Retest",
        )
        expected = []
        for n, (s, note) in enumerate(zip(data["scenarios"], notes), 1):
            evaluated = summary(s)
            layer = "五層" if len(evaluated) == 5 else evaluated[0]["layer"]
            result = (
                "各層Passed"
                if len(evaluated) == 5
                and all(r["result"] == "Passed" for r in evaluated)
                else evaluated[0]["result"]
            )
            expected.append(
                f"Scenario末尾 Type / 選択層 供給結果 読み取る差 {n:03} {s['type']} / {layer} {result} {note}"
            )
        if section_rows(document, "7. 十の供給対比を読む") != expected:
            errors.append("CV21 manuscript comparison table / evaluated parity")
    return errors


def document_errors(document, spec, data):
    errors = scan_document(document, spec) + reading_table_errors(document, data)
    if (
        digest(inventory(document)) != spec["projectionSha256"]
        or headings(document) != spec["headings"]
        or len(document.fields) != spec["fieldCount"]
    ):
        errors.append(document.document_id + ": finite fields/order/locations/headings")
    if document.document_id == DOCUMENTS[0]:
        body, refs, in_refs = set(), set(), False
        for field in document.fields:
            if (
                field.element_kind == "heading"
                and field.text == "参考文献・Source Note ID"
            ):
                in_refs = True
            if is_policy_scan_field(field):
                (refs if in_refs else body).update(SOURCE_ID_RE.findall(field.text))
        if body != set(SOURCES) or refs != set(SOURCES):
            errors.append("CV21 body/end Source set")
    return errors


def repository_errors(data, contract, root=ROOT):
    errors = []
    if list(contract["parentDigests"]) != list(PARENTS):
        errors.append("CV21 fixed parent inventory")
    for path in PARENTS:
        if hashlib.sha256(read_regular(root, path)).hexdigest() != contract[
            "parentDigests"
        ].get(path):
            errors.append("CV21 parent/shared/pin drift: " + path)
    d14 = strict(
        read_regular(root, "cases/fixtures/ch14-minimal-impact-validation.json")
    )
    d16 = strict(read_regular(root, "cases/fixtures/ch16-telemetry-coverage.json"))
    d17 = strict(
        read_regular(root, "cases/fixtures/ch17-detection-engineering-fixture.json")
    )
    d19 = strict(read_regular(root, "cases/fixtures/ch19-incident-response.json"))
    d20 = strict(read_regular(root, "cases/fixtures/ch20-dfir-timeline-causality.json"))
    h20 = next(h for h in d20["handoffs"] if h["targetChapter"] == 21)
    rca = next(
        s["rca"] for s in d20["snapshots"] if s["rca"]["id"] == h20["sourceRcaId"]
    )
    expected = {
        "use": "method-reference-only",
        "decisionRequirementId": d17["decisionRequirementId"],
        "threatHypothesisId": d17["threatHypotheses"][0]["id"],
        "detectionRecordId": d17["detectionValidationRecordId"],
        "detectionId": d17["detectionId"],
        "telemetryIds": [t["id"] for t in d17["telemetryContracts"]],
        "minimalValidationId": d14["record"]["id"],
        "telemetryMapId": d16["record"]["id"],
        "incidentPlanId": d19["record"]["id"],
        "dfirRecordId": d20["record"]["id"],
        "dfirRcaId": rca["id"],
        "dfirControlId": h20["controlId"],
        "dfirControlStatus": rca["controlFailureStatus"],
        "dfirHandoffId": h20["id"],
        "dfirHandoffStatus": h20["status"],
        "receiptId": h20["receiptId"],
        "parentEvidenceTransferred": False,
        "parentStateChanged": False,
        "authorityTransferred": False,
    }
    if (
        data["parentReferences"] != expected
        or h20["executionAuthorized"] is not False
        or h20["status"] != "planned-not-delivered"
        or h20["receiptId"] is not None
        or data["record"]["parentCaseId"] != d17["caseId"]
        or data["threat"]["attackTechniqueId"]
        not in d17["threatHypotheses"][0]["attackMapping"]
    ):
        errors.append("CV21 parent ID/non-inheritance/undelivered boundary")
    b, p14 = data["authorityBoundary"], d14["parents"]
    for ours, parent in (
        ("parentAuthorityId", "authorizationId"),
        ("parentExpiresAt", "authorizationExpiresAt"),
        ("parentRoeId", "roeId"),
        ("parentRoeStatus", "roeStatus"),
        ("parentRoeVersion", "roeVersion"),
        ("parentExecutionAuthorized", "roeExecutionAuthorized"),
    ):
        if b[ours] != p14[parent]:
            errors.append("CV21 exact parent Authority: " + ours)
    package = strict(read_regular(root, "package.json"))["scripts"]
    if (
        package.get("check:chapter21") != "python3 scripts/check_chapter21_contract.py"
        or package["test"].split(" && ").count("npm run check:chapter21") != 1
        or package["sync:docs"].split(" && ") != list(PREFLIGHT)
    ):
        errors.append("CV21 root test/preflight exactly once")
    routes = strict(read_regular(root, "site-pages.json"))
    for kind in ("pages", "staticFiles"):
        for route in contract[kind]:
            if routes[kind].count(route) != 1:
                errors.append("CV21 exact public route: " + route["source"])
    order = [
        p["source"]
        for p in sorted(routes["pages"], key=lambda p: p["order"])
        if p["section"] == "chapters"
    ]
    if not (
        order.index("manuscript/20-dfir-timeline-causality.md")
        < order.index(DOCUMENTS[0])
        < order.index("manuscript/25-structured-analysis-attribution.md")
    ):
        errors.append("CV21 navigation 20/21/25")
    sources = strict(read_regular(root, "references/sources.json"))
    if sources["checkedAt"] != "2026-07-25" or {
        s["id"] for s in sources["sources"] if 21 in s["chapters"]
    } != set(SOURCES):
        errors.append("CV21 scoped Source mapping/baseline")
    if set(contract["sourceIdentity"]) != set(SOURCES):
        errors.append("CV21 frozen Source inventory")
    for sid in SOURCES:
        source = next(s for s in sources["sources"] if s["id"] == sid)
        if any(source[k] != v for k, v in contract["sourceIdentity"][sid].items()):
            errors.append("CV21 reviewed Source identity: " + sid)
        if not meets_audit_baseline(source["checkedAt"], "2026-09-25"):
            errors.append("CV21 scoped Source date: " + sid)
    if list(contract["indices"]) != list(INDEX_PATHS):
        errors.append("CV21 index inventory")
    else:
        for path in INDEX_PATHS:
            text = read_regular(root, path).decode("utf-8")
            if any(marker not in text for marker in contract["indices"][path]):
                errors.append("CV21 index: " + path)
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
            or contract["comparisonVersion"] != VERSION
            or list(contract["documents"]) != list(DOCUMENTS)
            or POLICY_VERSION != "1.2.0"
            or PROJECTION_VERSION != "1.1.0"
            or hashlib.sha256(read_regular(ROOT, SCHEMA)).hexdigest()
            != contract["schemaSha256"]
            or hashlib.sha256(read_regular(ROOT, CORPUS)).hexdigest()
            != contract["corpusSha256"]
        ):
            raise ValueError("CV21 frozen inventory/schema/shared versions")
        errors = validate_model(data, schema, contract) + repository_errors(
            data, contract
        )
        source = {p: read_regular(ROOT, p).decode("utf-8") for p in DOCUMENTS}
        projection = project_documents(source)
        if [d.document_id for d in projection.documents] != list(DOCUMENTS):
            raise ValueError("CV21 complete document order")
        for doc in projection.documents:
            errors += document_errors(doc, contract["documents"][doc.document_id], data)
        count = 0
        if not args.no_regressions:
            from scripts.chapter21_regressions import run_regressions

            count, problems = run_regressions(
                data, schema, contract, source, projection
            )
            errors += problems
        if errors:
            for error in errors:
                print("ERROR:", error)
            return 1
        print(
            f"Chapter 21 contract passed: 4 complete documents; ART-27; 10 scenarios / 5 layers / 6 failure classes; {count} regressions; Policy {POLICY_VERSION}; Projection {PROJECTION_VERSION}; offline record-only / executionAuthorized=false"
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
        print("ERROR: Chapter21 fail closed:", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
