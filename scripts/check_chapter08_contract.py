#!/usr/bin/env python3
"""Chapter 8 Layer A: finite selection, provenance, ART-18 and publication gates.

Layer B owns all syntax/renderer behavior; Layer C owns all safety grammar.
No container, network, host probe, cleanup operation or chapter syntax parser.
"""

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
from scripts.chapter08_semantics import case_groups, validate_bundle  # noqa: E402
from scripts.replay_chapter08_lab import load_bundle  # noqa: E402
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

DOCUMENTS = (
    "manuscript/08-safe-lab-evidence.md",
    "templates/lab-safety-evidence-plan.md",
    "cases/ch08-lab-evidence-example.md",
    "references/ch08-source-review-2026-09-13.md",
)
SOURCE_IDS = ("SRC-NIST-DFIR-001", "SRC-NIST-CONTAINER-001", "SRC-BERKELEY-001")
CONTRACT_PATH = "tests/fixtures/chapter08/publication-contract.json"
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
    "python3 scripts/check_chapter16_contract.py --no-regressions",
    "python3 scripts/check_chapter18_contract.py --no-regressions",
    "python3 scripts/check_chapter19_contract.py --no-regressions",
    "python3 scripts/check_chapter20_contract.py --no-regressions",
    "python3 scripts/check_part02_contract.py --no-regressions",
    "python3 scripts/sync_book_site.py --output docs",
    "npm run copy:notices",
)


def key(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def relations(document):
    """Associate typed fields with Chapter 8 heading/visible link-label owners."""
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
    # Exact provenance and bounded analytic/prohibition false positives only.
    # Section, typed owner, complete field and cardinality all bind. This is not
    # a grammar waiver or permission to operate on any mentioned object.
    exemptions = {key(r) for r in spec["hostProvenance"]}
    analytic_exemptions = {key(r) for r in spec["analyticProvenance"]}
    if require_exceptions:
        for r in sorted(exemptions | analytic_exemptions):
            if counts[r] != 1:
                errors.append(document.document_id + ": exact provenance cardinality")
    for field, relation in pairs:
        findings = []
        if is_policy_scan_field(field):
            if key(relation) not in analytic_exemptions or counts[key(relation)] != 1:
                findings += scan_action_text(
                    field.normalized_text, location=field.location
                )
        if is_policy_scan_field(field) or (
            field.field_type == "destination"
            and is_absolute_destination(field.normalized_text)
        ):
            if key(relation) not in exemptions or counts[key(relation)] != 1:
                findings += scan_host_policy(
                    field.normalized_text, location=field.location
                )
        errors += [f"{field.location}: {f.category}: {f.reason}" for f in findings]
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
    for relation in spec["required"]:
        if counts[key(relation)] != 1:
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
            errors.append("ART18 complete JSON/projected Case parity")
    if document.document_id == DOCUMENTS[0]:
        body, refs = set(), set()
        for field, relation in relations(document):
            if is_policy_scan_field(field):
                for sid in SOURCE_IDS:
                    if sid in field.text:
                        (
                            refs
                            if "参考文献・Source Note ID" in relation["headings"]
                            else body
                        ).add(sid)
        if body != set(SOURCE_IDS) or refs != set(SOURCE_IDS):
            errors.append("Chapter8 body/reference Source ownership")
    return errors


def repository_errors(contract, root=ROOT):
    errors = []
    for p, digest in contract["parentDigests"].items():
        if hashlib.sha256((root / p).read_bytes()).hexdigest() != digest:
            errors.append(p + ": unchanged parent/shared baseline")
    package = load_json_strict(root / "package.json")["scripts"]
    if (
        package.get("check:chapter08") != "python3 scripts/check_chapter08_contract.py"
        or package["test"].split(" && ").count("npm run check:chapter08") != 1
    ):
        errors.append("Chapter8 root invocation exactly once")
    if package.get("sync:docs", "").split(" && ") != list(PREFLIGHT):
        errors.append("Chapter8 safety before publication generation")
    registry = load_json_strict(root / "site-pages.json")
    for kind in ("pages", "staticFiles"):
        for route in contract[kind]:
            if registry[kind].count(route) != 1:
                errors.append("Chapter8 exact publication route " + route["source"])
    order = [
        p["source"]
        for p in sorted(registry["pages"], key=lambda p: p["order"])
        if p["section"] == "chapters"
    ]
    if (
        not order.index("manuscript/07-vulnerability-prioritization.md")
        < order.index(DOCUMENTS[0])
        < order.index("manuscript/11-web-api-hypothesis.md")
    ):
        errors.append("Chapter8 navigation 7 before 8 before 11")
    registry = load_json_strict(root / "references/sources.json")
    if registry["checkedAt"] != "2026-07-25":
        errors.append("Chapter8 scoped audit must not refresh whole Registry")
    sources = registry["sources"]
    if {s["id"] for s in sources if 8 in s["chapters"]} != set(SOURCE_IDS):
        errors.append("Chapter8 Source mapping")
    for sid in SOURCE_IDS:
        source = next((s for s in sources if s["id"] == sid), {})
        if not meets_audit_baseline(
            source.get("checkedAt"), "2026-09-13"
        ) or not meets_audit_baseline(source.get("nextReviewAt"), "2027-09-13"):
            errors.append("Chapter8 dated Source audit " + sid)
        if any(source.get(k) != v for k, v in contract["sourceIdentity"][sid].items()):
            errors.append("Chapter8 Source version/status/date/limited adoption " + sid)
    for path, markers in contract["indices"].items():
        text = (root / path).read_text(encoding="utf-8")
        if any(marker not in text for marker in markers):
            errors.append("Chapter8 index " + path)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-regressions", action="store_true")
    args = parser.parse_args()
    try:
        contract = load_json_strict(ROOT / CONTRACT_PATH)
        if contract["schemaVersion"] != "1.0.0" or list(contract["documents"]) != list(
            DOCUMENTS
        ):
            raise ValueError("Chapter8 finite contract/document inventory")
        if POLICY_VERSION != "1.2.0" or PROJECTION_VERSION != "1.1.0":
            raise ValueError("Chapter8 reviewed shared versions")
        data, raw, schemas, parents = load_bundle()
        errors = validate_bundle(*data, raw, schemas, parents) + repository_errors(
            contract
        )
        source = {p: (ROOT / p).read_text(encoding="utf-8") for p in DOCUMENTS}
        projection = project_documents(source)
        if [d.document_id for d in projection.documents] != list(DOCUMENTS):
            raise ValueError("Chapter8 projected inventory/order")
        for doc in projection.documents:
            errors += document_errors(doc, contract["documents"][doc.document_id], data)
        count = 0
        if not args.no_regressions:
            from scripts.chapter08_regressions import run_regressions

            count, regression_errors = run_regressions(
                data, raw, schemas, parents, contract, source, projection
            )
            errors += regression_errors
        if errors:
            for error in errors:
                print("ERROR:", error)
            return 1
        print(
            f"Chapter 8 contract passed: 4 complete documents; 3 ART-18 runs / 72 checks / 9 signals; {count} regressions; Policy {POLICY_VERSION}; Projection {PROJECTION_VERSION}"
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
        print("ERROR: Chapter8 fail closed:", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
