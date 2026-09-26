#!/usr/bin/env python3
"""Chapter22 finite selection/semantics; shared Projection and Policy own syntax."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.chapter22_model import (  # noqa: E402
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
        errors.append("IMP22 duplicate provenance")
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
            errors.append("IMP22 all artifact leaves / Case parity")
    if document.document_id == DOCUMENTS[0]:
        expected = [
            "対比 供給された差 許される結論 Rule数と重要範囲 4→8、2/5→2/5 件数増加。重要範囲の検証拡大は未確認",
            "対比 供給された差 許される結論 Mappingと検証 9/10と2/10 対応表の広さを有効性へ変換しない",
            "対比 供給された差 許される結論 時間と根拠品質 平均10→5分、充足5/5→2/5 時間短縮と品質低下を併記する",
            "対比 供給された差 許される結論 TelemetryとHunt Inconclusive4/10→1/10 同じ供給母集団の限定比較だけ",
            "対比 供給された差 許される結論 Control再検証 三条件一致2/3→3/3 旧Failedを保持した供給版の比較だけ",
        ]
        if section_rows(document, "11. 五つの対比から判断を練習する") != expected:
            errors.append("IMP22 manuscript five contrasts")
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
            errors.append("IMP22 body/end Source set")
    return errors


def parent_errors(data, parent):
    errors = []
    before, after = (
        next(s for s in parent["scenarios"] if s["id"] == sid)
        for sid in ("SCN-CV21-003", "SCN-CV21-010")
    )
    h = parent["handoff"]
    expected = {
        "use": "method-reference-only",
        "caseIds": ["CASE-2026-001", "CASE-DET-2026-001"],
        "controlValidationRecordId": parent["record"]["id"],
        "controlRetestId": parent["retest"]["id"],
        "beforeScenarioId": before["id"],
        "afterScenarioId": after["id"],
        "beforeEvidenceId": before["observations"][0]["id"],
        "afterEvidenceId": after["observations"][0]["id"],
        "parentHandoffId": h["id"],
        "parentHandoffStatus": h["status"],
        "parentReceiptId": h["receiptId"],
        "parentEvidenceTransferred": False,
        "parentStateChanged": False,
        "authorityTransferred": False,
    }
    if (
        digest(data["parentReferences"]) != digest(expected)
        or h["status"] != "planned-not-delivered"
        or h["receiptId"] is not None
        or h["executionAuthorized"] is not False
        or h["targetChapter"] != 22
        or digest(data["authorityBoundary"]) != digest(parent["authorityBoundary"])
        or parent["executionAuthorized"] is not False
        or parent["retest"]["beforeRetained"] is not True
        or parent["retest"]["actualChangeExecuted"] is not False
    ):
        errors.append(
            "IMP22 exact parent method reference/non-inheritance/authority boundary"
        )
    for key in (
        "subjectId",
        "subjectRevision",
        "batchId",
        "windowStart",
        "windowEnd",
        "cutoff",
    ):
        if before[key] != after[key]:
            errors.append("IMP22 parent retest same scope/condition: " + key)
    if before["expectedLayers"] != [
        {
            "layer": "Detection",
            "result": "Failed",
            "failureClasses": ["Detection logic"],
        }
    ] or after["expectedLayers"] != [
        {"layer": "Detection", "result": "Passed", "failureClasses": []}
    ]:
        errors.append("IMP22 parent old Failed/new Passed must both remain")
    metric = data["metrics"][7]
    criteria = {
        "positive": "alert",
        "negative": "no-alert",
        "benign-near-miss": "no-alert",
    }
    for name, scenario in (("baseline", before), ("current", after)):
        payload = scenario["observations"][0]["payload"]
        if (
            payload["present"] != {key: True for key in criteria}
            or metric[name]["selectedMembers"]
            != [
                key
                for key, value in criteria.items()
                if payload["values"][key] == value
            ]
            or scenario["improvement"]["status"] != "proposed-not-executed"
            or any(
                metric[name][key] != scenario[key]
                for key in ("windowStart", "windowEnd")
            )
            or metric["cutoff"] != scenario["cutoff"]
        ):
            errors.append(
                "IMP22 parent finite control comparison; no actual action completion"
            )
    return errors


def repository_errors(data, contract, root=ROOT):
    errors = []
    if list(contract["parentDigests"]) != list(PARENTS):
        errors.append("IMP22 fixed parent inventory")
    for path in PARENTS:
        if hashlib.sha256(read_regular(root, path)).hexdigest() != contract[
            "parentDigests"
        ].get(path):
            errors.append("IMP22 parent/shared/pin drift: " + path)
    parent = strict(read_regular(root, "cases/fixtures/ch21-control-validation.json"))
    errors += parent_errors(data, parent)
    package = strict(read_regular(root, "package.json"))["scripts"]
    if (
        package.get("check:chapter22") != "python3 scripts/check_chapter22_contract.py"
        or package["test"].split(" && ").count("npm run check:chapter22") != 1
        or package["sync:docs"].split(" && ") != list(PREFLIGHT)
    ):
        errors.append("IMP22 root test/preflight exactly once")
    routes = strict(read_regular(root, "site-pages.json"))
    for kind in ("pages", "staticFiles"):
        for route in contract[kind]:
            if routes[kind].count(route) != 1:
                errors.append("IMP22 exact public route: " + route["source"])
    order = [
        p["source"]
        for p in sorted(routes["pages"], key=lambda p: p["order"])
        if p["section"] == "chapters"
    ]
    if not (
        order.index("manuscript/21-purple-team-validation.md")
        < order.index(DOCUMENTS[0])
        < order.index("manuscript/25-structured-analysis-attribution.md")
    ):
        errors.append("IMP22 navigation 21/22/25")
    config = strict(read_regular(root, "book-config.json"))
    chapter = {
        "id": "ch22-measurement-improvement",
        "title": "第22章 測定、優先順位、継続改善",
        "description": "Coverage、品質、対応時間、残存リスクを改善Backlogへ変換する",
        "objectives": [
            "有効な測定項目を選べる",
            "見せかけのCoverageを避けられる",
            "Security Improvement Backlogを作成できる",
        ],
    }
    if (
        contract["chapterId"] != chapter["id"]
        or config["structure"]["chapters"][22] != chapter
        or sum(c["id"] == chapter["id"] for c in config["structure"]["chapters"]) != 1
    ):
        errors.append("IMP22 book configuration identity")
    sources = strict(read_regular(root, "references/sources.json"))
    if sources["checkedAt"] != "2026-07-25" or {
        s["id"] for s in sources["sources"] if 22 in s["chapters"]
    } != set(SOURCES):
        errors.append("IMP22 scoped Source mapping/baseline")
    if set(contract["sourceIdentity"]) != set(SOURCES):
        errors.append("IMP22 frozen Source inventory")
    for sid in SOURCES:
        source = next(s for s in sources["sources"] if s["id"] == sid)
        if any(source[k] != v for k, v in contract["sourceIdentity"][sid].items()):
            errors.append("IMP22 reviewed Source identity: " + sid)
        if not meets_audit_baseline(source["checkedAt"], "2026-09-26"):
            errors.append("IMP22 scoped Source date: " + sid)
    if list(contract["indices"]) != list(INDEX_PATHS):
        errors.append("IMP22 index inventory")
    else:
        for path in INDEX_PATHS:
            text = read_regular(root, path).decode("utf-8")
            if any(marker not in text for marker in contract["indices"][path]):
                errors.append("IMP22 index: " + path)
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
            raise ValueError("IMP22 frozen inventory/schema/shared versions")
        errors = validate_model(data, schema, contract) + repository_errors(
            data, contract
        )
        source = {p: read_regular(ROOT, p).decode("utf-8") for p in DOCUMENTS}
        projection = project_documents(source)
        if [d.document_id for d in projection.documents] != list(DOCUMENTS):
            raise ValueError("IMP22 complete document order")
        for doc in projection.documents:
            errors += document_errors(doc, contract["documents"][doc.document_id], data)
        count = 0
        if not args.no_regressions:
            from scripts.chapter22_regressions import run_regressions

            count, problems = run_regressions(
                data, schema, contract, source, projection
            )
            errors += problems
        if errors:
            for error in errors:
                print("ERROR:", error)
            return 1
        print(
            f"Chapter 22 contract passed: 4 complete documents; ART-28; 10 metrics / 8 backlog items / 7 statuses; {count} regressions; Policy {POLICY_VERSION}; Projection {PROJECTION_VERSION}; offline record-only / executionAuthorized=false"
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
        print("ERROR: Chapter22 fail closed:", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
