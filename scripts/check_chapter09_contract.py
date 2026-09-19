#!/usr/bin/env python3
"""Chapter 9 Layer A: ART-02 selection, provenance and finite publication gates."""

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
from scripts.chapter09_semantics import (  # noqa: E402
    DATA_PATH,
    PARENT_PATHS,
    DOCUMENT_PATHS,
    read_regular,
    SCHEMA_PATH,
    read_input,
    validate_record,
    conditions,
    case_groups,
)
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
from scripts.source_audit import meets_audit_baseline  # noqa: E402

DOCUMENTS = DOCUMENT_PATHS

SOURCE_IDS = ("SRC-NIST-TEST-001", "SRC-JP-LAW-001", "SRC-IPA-VDP-001", "SRC-WSTG-001")
CONTRACT_PATH = "tests/fixtures/chapter09/publication-contract.json"
PREFLIGHT = (
    "python3 scripts/check_chapter06_contract.py --no-regressions",
    "python3 scripts/check_chapter07_contract.py --no-regressions",
    "python3 scripts/check_chapter08_contract.py --no-regressions",
    "python3 scripts/check_chapter09_contract.py --no-regressions",
    "python3 scripts/check_chapter10_contract.py --no-regressions",
    "python3 scripts/check_chapter12_contract.py --no-regressions",
    "python3 scripts/check_chapter13_contract.py --no-regressions",
    "python3 scripts/check_chapter14_contract.py --no-regressions",
    "python3 scripts/check_chapter15_contract.py --no-regressions",
    "python3 scripts/sync_book_site.py --output docs",
    "npm run copy:notices",
)


def key(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def relations(document):
    """Attach selected typed fields to chapter-specific heading/label owners."""
    headings, owner = {}, None
    for field in document.fields:
        identity = [field.field_type, field.element_kind, field.attribute, field.text]
        relation = {
            "field": identity,
            "headings": [headings[k] for k in sorted(headings)],
        }
        if field.field_type == "destination":
            relation["owner"] = owner
        yield field, relation
        if field.field_type in ("reader_visible_text", "reader_visible_attribute"):
            owner = identity
        level = field.metadata_value("level")
        if (
            field.element_kind == "heading"
            and field.field_type == "reader_visible_text"
            and type(level) is int
        ):
            headings = {k: v for k, v in headings.items() if k < level}
            headings[level] = field.text


def scan_document(document, spec, require_exceptions=False):
    pairs = list(relations(document))
    counts = Counter(key(r) for _, r in pairs)
    errors = [f"{d.location}: {d.code}: {d.reason}" for d in document.diagnostics]
    host = {key(r) for r in spec["hostProvenance"]}
    analytic = {key(r) for r in spec["analyticProvenance"]}
    if require_exceptions:
        for r in sorted(host | analytic):
            if counts[r] != 1:
                errors.append(
                    f"{document.document_id}: exact provenance cardinality: "
                    f"expected 1, observed {counts[r]}; entry={r}"
                )
    for field, relation in pairs:
        found = []
        identity = key(relation)
        if is_policy_scan_field(field) and (
            identity not in analytic or counts[identity] != 1
        ):
            found += scan_action_text(field.normalized_text, location=field.location)
        if (
            is_policy_scan_field(field)
            or (
                field.field_type == "destination"
                and is_absolute_destination(field.normalized_text)
            )
        ) and (identity not in host or counts[identity] != 1):
            found += scan_host_policy(field.normalized_text, location=field.location)
        errors += [f"{field.location}: {f.category}: {f.reason}" for f in found]
    return errors


def document_errors(document, spec, data):
    errors = scan_document(document, spec, True)
    headings = [
        [f.metadata_value("level"), f.text]
        for f in document.fields
        if f.field_type == "reader_visible_text"
        and f.element_kind == "heading"
        and type(f.metadata_value("level")) is int
        and f.metadata_value("level") <= 2
    ]
    if headings != spec["headings"]:
        errors.append(document.document_id + ": finite H1/H2 inventory")
    counts = Counter(key(r) for _, r in relations(document))
    for r in spec["required"]:
        if counts[key(r)] != 1:
            errors.append(
                document.document_id + ": required semantic field missing/duplicate"
            )
    if document.document_id == DOCUMENTS[2]:
        actual = [
            f.text
            for f in document.fields
            if is_policy_scan_field(f) and f.element_kind == "table_row"
        ]
        expected = [
            f"{group} Field Value {k} {v}"
            for group, rows in case_groups(data)
            for k, v in rows
        ]
        if actual != expected:
            errors.append("ART02 complete JSON/projected Case parity")
    if document.document_id == DOCUMENTS[0]:
        # The chapter's local exercise must explain its purpose, prerequisites,
        # expected evidence, stop conditions and cleanup before its command.
        # Ordering uses Layer B fields, not a chapter-specific Markdown parser.
        pairs = list(relations(document))
        positions = [
            [i for i, (_, relation) in enumerate(pairs) if relation == expected]
            for expected in spec["exerciseInstructionOrder"]
        ]
        if any(len(p) != 1 for p in positions) or positions != sorted(positions):
            errors.append("Chapter9 exercise explanations before command")
        body, refs = set(), set()
        for f, r in relations(document):
            if is_policy_scan_field(f):
                for sid in SOURCE_IDS:
                    if sid in f.text:
                        (
                            refs
                            if "参考文献・Source Note ID" in r["headings"]
                            else body
                        ).add(sid)
        if body != set(SOURCE_IDS) or refs != set(SOURCE_IDS):
            errors.append("Chapter9 body/reference Source ownership")
    return errors


def repository_errors(contract, root=ROOT):
    errors = []
    if list(contract["parentDigests"]) != list(PARENT_PATHS):
        errors.append("Chapter9 fixed parent inventory")
    for path, digest in contract["parentDigests"].items():
        if hashlib.sha256(read_regular(root, path)).hexdigest() != digest:
            errors.append(path + ": unchanged parent/shared baseline")
    package = load_json_strict(root / "package.json")["scripts"]
    if (
        package.get("check:chapter09") != "python3 scripts/check_chapter09_contract.py"
        or package["test"].split(" && ").count("npm run check:chapter09") != 1
    ):
        errors.append("Chapter9 root invocation exactly once")
    if package.get("sync:docs", "").split(" && ") != list(PREFLIGHT):
        errors.append("Chapter9 safety before publication generation")
    registry = load_json_strict(root / "site-pages.json")
    for kind in ("pages", "staticFiles"):
        for route in contract[kind]:
            if registry[kind].count(route) != 1:
                errors.append("Chapter9 exact route " + route["source"])
    order = [
        p["source"]
        for p in sorted(registry["pages"], key=lambda x: x["order"])
        if p["section"] == "chapters"
    ]
    if (
        not order.index("manuscript/08-safe-lab-evidence.md")
        < order.index(DOCUMENTS[0])
        < order.index("manuscript/11-web-api-hypothesis.md")
    ):
        errors.append("Chapter9 navigation 8 before 9 before 11")
    registry = load_json_strict(root / "references/sources.json")
    sources = registry["sources"]
    if registry["checkedAt"] != "2026-07-25" or {
        s["id"] for s in sources if 9 in s["chapters"]
    } != set(SOURCE_IDS):
        errors.append("Chapter9 scoped Source mapping/date")
    for sid in SOURCE_IDS:
        source = next((s for s in sources if s["id"] == sid), {})
        review = "2027-09-13" if sid == "SRC-NIST-TEST-001" else "2026-12-13"
        if not meets_audit_baseline(
            source.get("checkedAt"), "2026-09-13"
        ) or not meets_audit_baseline(source.get("nextReviewAt"), review):
            errors.append("Chapter9 dated Source audit " + sid)
        if any(source.get(k) != v for k, v in contract["sourceIdentity"][sid].items()):
            errors.append("Chapter9 Source version/status/date/limited adoption " + sid)
    for path, markers in contract["indices"].items():
        if any(
            marker not in (root / path).read_text(encoding="utf-8")
            for marker in markers
        ):
            errors.append("Chapter9 index " + path)
    return errors


def canonical_errors(data):
    if (
        data["record"]["status"] != "Draft"
        or data["record"]["asOf"] != "2026-09-13T09:00:00Z"
        or data["record"]["version"] != 1
        or data["approval"]["authorityStatus"] != "Expired"
        or data["approval"]["signoffs"] != []
        or data["approval"]["writtenEvidenceRef"] is not None
        or data["approval"]["approvedVersion"] is not None
    ):
        return [
            "ART02 canonical dated Draft and missing authorization must be retained"
        ]
    if conditions(data) != [
        "ROE-STATUS",
        "AUTH-STATUS",
        "AUTH-TIME",
        "WINDOW-AUTHORITY",
        "WINDOW-NOW",
        "WRITTEN-PROOF",
        "APPROVED-VERSION",
        "APPROVAL-ROLES",
    ]:
        return ["ART02 canonical Do not proceed reasons"]
    return []


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-regressions", action="store_true")
    args = parser.parse_args()
    try:
        contract = load_json_strict(ROOT / CONTRACT_PATH)
        if (
            contract["schemaVersion"] != "1.0.0"
            or list(contract["documents"]) != list(DOCUMENTS)
            or POLICY_VERSION != "1.2.0"
            or PROJECTION_VERSION != "1.1.0"
        ):
            raise ValueError("Chapter9 finite inventory/shared versions")
        data, schema = (read_input(ROOT, p) for p in (DATA_PATH, SCHEMA_PATH))
        errors = validate_record(data, schema)
        if errors:
            raise ValueError("; ".join(errors))
        errors += canonical_errors(data) + repository_errors(contract)
        source = {p: read_regular(ROOT, p).decode("utf-8") for p in DOCUMENTS}
        projection = project_documents(source)
        if [d.document_id for d in projection.documents] != list(DOCUMENTS):
            raise ValueError("Chapter9 projection selection/order")
        for doc in projection.documents:
            errors += document_errors(doc, contract["documents"][doc.document_id], data)
        count = 0
        if not args.no_regressions:
            from scripts.chapter09_regressions import run_regressions

            count, regression_errors = run_regressions(
                data, schema, contract, source, projection
            )
            errors += regression_errors
        if errors:
            for error in errors:
                print("ERROR:", error)
            return 1
        print(
            f"Chapter 9 contract passed: 4 complete documents; ART-02 Draft / Do not proceed; {count} regressions; Policy {POLICY_VERSION}; Projection {PROJECTION_VERSION}; executionAuthorized=false"
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
        print("ERROR: Chapter9 fail closed:", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
