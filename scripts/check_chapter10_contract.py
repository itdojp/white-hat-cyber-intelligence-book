#!/usr/bin/env python3
"""Chapter 10 Layer A: finite ART-19 surfaces and evidence/approval semantics."""

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
from scripts.chapter10_semantics import (  # noqa: E402
    DATA_PATH,
    BUNDLE_PATH,
    SCHEMA_PATH,
    CONTRACT_PATH,
    DOCUMENTS,
    PARENTS,
    read_regular,
    strict_bytes,
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

SOURCE_IDS = (
    "SRC-BERKELEY-001",
    "SRC-WSTG-001",
    "SRC-CT-001",
    "SRC-SECURITYTXT-001",
    "SRC-DNS-TERM-001",
    "SRC-DNS-STALE-001",
)
PREFLIGHT = tuple(
    f"python3 scripts/check_chapter{n:02}_contract.py --no-regressions"
    for n in (6, 7, 8, 9, 10, 12, 13, 14, 15)
) + (
    "python3 scripts/check_chapter16_contract.py --no-regressions",
    "python3 scripts/check_chapter18_contract.py --no-regressions",
    "python3 scripts/check_chapter19_contract.py --no-regressions",
    "python3 scripts/check_part02_contract.py --no-regressions",
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


def document_errors(document, spec, data, bundle):
    errors = scan_document(document, spec, True)
    pairs = list(relations(document))
    headings = [
        [f.metadata_value("level"), f.text]
        for f, _ in pairs
        if f.field_type == "reader_visible_text"
        and f.element_kind == "heading"
        and type(f.metadata_value("level")) is int
        and f.metadata_value("level") <= 2
    ]
    if headings != spec["headings"]:
        errors.append(document.document_id + ": finite H1/H2 inventory")
    counts = Counter(key(r) for _, r in pairs)
    for required in spec["required"]:
        if counts[key(required)] != 1:
            errors.append(
                document.document_id
                + ": required semantic field missing/duplicate: "
                + key(required)
            )
    if document.document_id == DOCUMENTS[2]:
        actual = [
            f.text
            for f, _ in pairs
            if is_policy_scan_field(f) and f.element_kind == "table_row"
        ]
        expected = [
            f"{group} Field Value {k} {v}"
            for group, rows in case_groups(data, bundle)
            for k, v in rows
        ]
        if actual != expected:
            errors.append("ART19 complete two-JSON/projected Case parity")
    if document.document_id == DOCUMENTS[0]:
        positions = [
            [i for i, (_, r) in enumerate(pairs) if r == expected]
            for expected in spec["exerciseInstructionOrder"]
        ]
        if any(len(p) != 1 for p in positions) or positions != sorted(positions):
            errors.append("Chapter10 exercise explanations before command")
        body, refs = set(), set()
        for f, r in pairs:
            if is_policy_scan_field(f):
                # Reuse the repository's Source-ID token vocabulary, not
                # substring membership or a chapter-specific syntax parser.
                (refs if "参考文献・Source Note ID" in r["headings"] else body).update(
                    SOURCE_ID_RE.findall(f.text)
                )
        if body != set(SOURCE_IDS) or refs != set(SOURCE_IDS):
            errors.append("Chapter10 body/reference Source ownership")
    return errors


def repository_errors(contract, root=ROOT):
    errors = []
    if list(contract["parentDigests"]) != list(PARENTS):
        errors.append("Chapter10 frozen parent inventory")
    for p, digest in contract["parentDigests"].items():
        if hashlib.sha256(read_regular(root, p)).hexdigest() != digest:
            errors.append(p + ": unchanged parent/shared baseline")
    package = load_json_strict(root / "package.json")["scripts"]
    if (
        package.get("check:chapter10") != "python3 scripts/check_chapter10_contract.py"
        or package["test"].split(" && ").count("npm run check:chapter10") != 1
    ):
        errors.append("Chapter10 root invocation exactly once")
    if package.get("sync:docs", "").split(" && ") != list(PREFLIGHT):
        errors.append("Chapter10 safety before publication generation")
    pages = load_json_strict(root / "site-pages.json")
    for kind in ("pages", "staticFiles"):
        for route in contract[kind]:
            if pages[kind].count(route) != 1:
                errors.append("Chapter10 exact route " + route["source"])
    order = [
        p["source"]
        for p in sorted(pages["pages"], key=lambda x: x["order"])
        if p["section"] == "chapters"
    ]
    if (
        not order.index("manuscript/09-engagement-roe.md")
        < order.index(DOCUMENTS[0])
        < order.index("manuscript/11-web-api-hypothesis.md")
    ):
        errors.append("Chapter10 navigation 9 before 10 before 11")
    sources = load_json_strict(root / "references/sources.json")
    if sources["checkedAt"] != "2026-07-25" or {
        s["id"] for s in sources["sources"] if 10 in s["chapters"]
    } != set(SOURCE_IDS):
        errors.append("Chapter10 scoped Source mapping/date")
    for sid in SOURCE_IDS:
        source = next((s for s in sources["sources"] if s["id"] == sid), {})
        review = "2026-12-14" if sid == "SRC-WSTG-001" else "2027-09-14"
        if not meets_audit_baseline(
            source.get("checkedAt"), "2026-09-14"
        ) or not meets_audit_baseline(source.get("nextReviewAt"), review):
            errors.append("Chapter10 Source audit " + sid)
        if any(source.get(k) != v for k, v in contract["sourceIdentity"][sid].items()):
            errors.append("Chapter10 fixed Source version/status/scope " + sid)
    for p, markers in contract["indices"].items():
        text = (root / p).read_text(encoding="utf-8")
        if any(m not in text for m in markers):
            errors.append("Chapter10 index " + p)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-regressions", action="store_true")
    args = parser.parse_args()
    try:
        data, bundle, schema, contract = (
            strict_bytes(read_regular(ROOT, p))
            for p in (DATA_PATH, BUNDLE_PATH, SCHEMA_PATH, CONTRACT_PATH)
        )
        if (
            contract["schemaVersion"] != "1.0.0"
            or list(contract["documents"]) != list(DOCUMENTS)
            or POLICY_VERSION != "1.2.0"
            or PROJECTION_VERSION != "1.1.0"
        ):
            raise ValueError("Chapter10 finite inventory/shared versions")
        errors = validate_model(data, bundle, schema, contract)
        if errors:
            raise ValueError("; ".join(errors))
        errors += repository_errors(contract)
        source = {p: read_regular(ROOT, p).decode("utf-8") for p in DOCUMENTS}
        projection = project_documents(source)
        if [d.document_id for d in projection.documents] != list(DOCUMENTS):
            raise ValueError("Chapter10 projection selection/order")
        for doc in projection.documents:
            errors += document_errors(
                doc, contract["documents"][doc.document_id], data, bundle
            )
        count = 0
        if not args.no_regressions:
            from scripts.chapter10_regressions import run_regressions

            count, regression_errors = run_regressions(
                data, bundle, schema, contract, source, projection
            )
            errors += regression_errors
        if errors:
            for error in errors:
                print("ERROR:", error)
            return 1
        print(
            f"Chapter 10 contract passed: 4 complete documents; 9 sources / 6 candidates; {count} regressions; Policy {POLICY_VERSION}; Projection {PROJECTION_VERSION}; record-only / executionAuthorized=false"
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
        print("ERROR: Chapter10 fail closed:", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
