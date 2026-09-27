#!/usr/bin/env python3
"""Chapter26 finite selection/semantics; shared Projection and Policy own syntax."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.chapter26_model import (  # noqa: E402
    VERSION,
    DATA,
    BUNDLE,
    TAXII,
    SCHEMAS,
    PARENT_DATA,
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
    for n in (6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 26)
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
        errors.append("CTI26 duplicate provenance")
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
    if document.document_id != DOCUMENTS[3]:
        return []
    expected = [
        " ".join((title + " Field Value " + key + " " + value).split())
        for title, rows in case_groups(data)
        for key, value in rows
    ]
    return (
        []
        if section_rows(document, "全欄の読み方") == expected
        else ["CTI26 all artifact leaves / Case parity"]
    )


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
            errors.append("CTI26 body/end Source set")
    return errors


def chapter_order_errors(pages):
    """Finite reading sequence, independent of the frozen route snapshot."""
    names = (
        "manuscript/24-osint-provenance-sources.md",
        "manuscript/25-structured-analysis-attribution.md",
        DOCUMENTS[0],
    )
    selected = [p for p in pages if p["source"] in names]
    orders = {p["source"]: p["order"] for p in selected}
    if (
        len(selected) != 3
        or len(orders) != 3
        or not orders[names[0]] < orders[names[1]] < orders[names[2]]
    ):
        return ["CTI26 reading order must be Chapter24 < Chapter25 < Chapter26"]
    return []


def repository_errors(data, contract, root=ROOT):
    errors = []
    if list(contract["parentDigests"]) != list(PARENTS):
        errors.append("CTI26 fixed parent inventory")
    for path in PARENTS:
        if hashlib.sha256(read_regular(root, path)).hexdigest() != contract[
            "parentDigests"
        ].get(path):
            errors.append("CTI26 parent/shared/pin drift: " + path)
    parent = strict(read_regular(root, PARENT_DATA))
    if (
        parent["caseId"] != data["record"]["caseId"]
        or parent["analyticJudgmentId"] != data["record"]["parentJudgmentId"]
        or parent["decisionId"] != data["decision"]["parentDecisionId"]
        or parent["synthetic"] is not True
    ):
        errors.append("CTI26 parent identity")
    for e in data["evidence"]:
        pe = next(x for x in parent["evidence"] if x["id"] == e["id"])
        sn = next(x for x in parent["sourceNotes"] if x["id"] == pe["sourceNoteId"])
        if (
            e["sourceId"] != pe["sourceNoteId"]
            or e["independenceGroupId"] != sn["independenceGroupId"]
        ):
            errors.append("CTI26 parent evidence/source exact binding")
    package = strict(read_regular(root, "package.json"))["scripts"]
    if (
        package.get("check:chapter26") != "python3 scripts/check_chapter26_contract.py"
        or package["test"].split(" && ").count("npm run check:chapter26") != 1
        or package["sync:docs"].split(" && ") != list(PREFLIGHT)
    ):
        errors.append("CTI26 test/preflight entrypoint")
    site = strict(read_regular(root, "site-pages.json"))
    errors += chapter_order_errors(site["pages"])
    for key in ("pages", "staticFiles"):
        for row in contract["routes"][key]:
            if (
                site[key].count(row) != 1
                or sum(
                    r["source"] == row["source"]
                    or r["destination"] == row["destination"]
                    for r in site[key]
                )
                != 1
            ):
                errors.append("CTI26 canonical publication route")
    from dataclasses import asdict
    from scripts.sync_site_source import PAGES

    legacy = [asdict(p) for p in PAGES if p.source in DOCUMENTS[1:3]]
    if legacy != contract["legacyTemplateRoutes"]:
        errors.append("CTI26 existing template route identity")
    config = strict(read_regular(root, "book-config.json"))
    chapter = {
        "id": "ch26-cti-structure-distribution",
        "title": "第26章 CTIを構造化し、技術・経営へ配布する",
        "description": "STIX/TAXIIと分析文書を用途別成果物へ変換する",
        "objectives": [
            "CTIオブジェクトを関係付けられる",
            "対象読者別に配布物を作れる",
            "CTI Reportを作成できる",
        ],
    }
    if (
        config["structure"]["chapters"][26] != chapter
        or contract["chapterId"] != chapter["id"]
    ):
        errors.append("CTI26 chapter identity")
    sources = strict(read_regular(root, "references/sources.json"))
    if sources["checkedAt"] != "2026-07-25" or {
        s["id"] for s in sources["sources"] if 26 in s["chapters"]
    } != set(SOURCES):
        errors.append("CTI26 scoped Source mapping/baseline")
    if set(contract["sourceIdentity"]) != set(SOURCES):
        errors.append("CTI26 frozen source inventory")
    for sid in SOURCES:
        s = next(s for s in sources["sources"] if s["id"] == sid)
        if any(
            s[k] != v for k, v in contract["sourceIdentity"][sid].items()
        ) or not meets_audit_baseline(s["checkedAt"], "2026-09-28"):
            errors.append("CTI26 scoped source identity/date: " + sid)
    if list(contract["indices"]) != list(INDEX_PATHS):
        errors.append("CTI26 index inventory")
    else:
        for path, markers in contract["indices"].items():
            text = read_regular(root, path).decode("utf-8")
            if any(marker not in text for marker in markers):
                errors.append("CTI26 index: " + path)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-regressions", action="store_true")
    args = parser.parse_args()
    try:
        data, bundle, taxii, contract = (
            strict(read_regular(ROOT, p)) for p in (DATA, BUNDLE, TAXII, CONTRACT)
        )
        schemas = [strict(read_regular(ROOT, p)) for p in SCHEMAS]
        if (
            contract["schemaVersion"] != "1.0.0"
            or contract["comparisonVersion"] != VERSION
            or list(contract["documents"]) != list(DOCUMENTS)
            or POLICY_VERSION != "1.2.0"
            or PROJECTION_VERSION != "1.1.0"
            or {p: hashlib.sha256(read_regular(ROOT, p)).hexdigest() for p in SCHEMAS}
            != contract["schemaDigests"]
            or hashlib.sha256(read_regular(ROOT, CORPUS)).hexdigest()
            != contract["corpusSha256"]
        ):
            raise ValueError("CTI26 frozen inventory/schema/shared versions")
        errors = validate_model(
            data, bundle, taxii, schemas, contract
        ) + repository_errors(data, contract)
        source = {p: read_regular(ROOT, p).decode("utf-8") for p in DOCUMENTS}
        projection = project_documents(source)
        if [d.document_id for d in projection.documents] != list(DOCUMENTS):
            raise ValueError("CTI26 complete document order")
        for doc in projection.documents:
            errors += document_errors(doc, contract["documents"][doc.document_id], data)
        count = 0
        if not args.no_regressions:
            from scripts.chapter26_regressions import run_regressions

            count, problems = run_regressions(
                data, bundle, taxii, schemas, contract, source, projection
            )
            errors += problems
        if errors:
            for error in errors:
                print("ERROR:", error)
            return 1
        print(
            f"Chapter 26 contract passed: 5 complete documents; ART-08 / ART-09; 3 judgments / 2 products / 13 independent STIX objects; {count} regressions; Policy {POLICY_VERSION}; Projection {PROJECTION_VERSION}; offline record-only / executionAuthorized=false"
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
        print("ERROR: Chapter26 fail closed:", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
