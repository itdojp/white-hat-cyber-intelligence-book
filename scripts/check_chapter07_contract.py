#!/usr/bin/env python3
"""Chapter7 Layer A selection/provenance/parity. Rendering belongs to Layer B."""

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
from scripts.chapter07_semantics import validate_case  # noqa: E402
from scripts.check_editorial_input_manifest import load_json_strict, ManifestError  # noqa: E402
from scripts.content_safety_policy import (  # noqa: E402
    POLICY_VERSION,
    scan_action_text,
    scan_host_policy,
)  # noqa: E402
from scripts.publication_projection import (  # noqa: E402
    PROJECTION_VERSION,
    ProjectionRuntimeError,
    project_documents,
    is_policy_scan_field,
    is_absolute_destination,
)
from scripts.source_audit import meets_audit_baseline  # noqa: E402

DOCUMENTS = (
    "manuscript/07-vulnerability-prioritization.md",
    "templates/vulnerability-prioritization-record.md",
    "cases/ch07-vulnerability-prioritization-example.md",
    "references/ch07-source-review-2026-09-12.md",
)
CASE_PATH = "cases/fixtures/ch07-vulnerability-prioritization.json"
PARENT_PATH = "cases/fixtures/ch06-signal-flow.json"
BEHAVIOR_PATH = "cases/fixtures/ch05-attack-behavior.json"
SNAPSHOT_PATH = "cases/fixtures/ch07-source-snapshot.json"
CONTRACT_PATH = "tests/fixtures/chapter07/publication-contract.json"
SOURCE_IDS = (
    "SRC-CVE-001",
    "SRC-CWE-001",
    "SRC-CVSS-001",
    "SRC-EPSS-001",
    "SRC-KEV-001",
    "SRC-CISA-VRM-001",
    "SRC-OWASP-TOP10-001",
)


def key(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def relations(document):
    """Map typed projected fields to chapter section/owner, without syntax parsing."""
    headings, previous, result = {}, None, []
    for f in document.fields:
        ident = [f.field_type, f.element_kind, f.attribute, f.text]
        relation = {"field": ident, "headings": [headings[k] for k in sorted(headings)]}
        if f.field_type == "destination":
            relation["owner"] = previous
        result.append((f, relation))
        if f.field_type in ("reader_visible_text", "reader_visible_attribute"):
            previous = ident
        level = f.metadata_value("level")
        if (
            f.field_type == "reader_visible_text"
            and f.element_kind == "heading"
            and type(level) is int
        ):
            headings = {k: v for k, v in headings.items() if k < level}
            headings[level] = f.text
    return result


def scan_document(document, spec, require_exceptions=False):
    errors = [str(x) for x in document.diagnostics]
    pairs = relations(document)
    counts = Counter(key(r) for _, r in pairs)
    exclusions = {
        kind: {key(x["relation"]) for x in spec["exceptions"][kind]}
        for kind in ("action", "host", "destination")
    }
    if require_exceptions:
        for kind in exclusions:
            for r in sorted(exclusions[kind]):
                if counts[r] != 1:
                    errors.append(
                        f"{document.document_id}: exact {kind} provenance cardinality"
                    )
    for f, r in pairs:

        def exempt(kind):
            return key(r) in exclusions[kind] and counts[key(r)] == 1

        findings = []
        if is_policy_scan_field(f):
            if not exempt("action"):
                findings += scan_action_text(f.normalized_text, location=f.location)
            if not exempt("host"):
                findings += scan_host_policy(f.normalized_text, location=f.location)
        elif (
            f.field_type == "destination"
            and is_absolute_destination(f.normalized_text)
            and not exempt("destination")
        ):
            findings += scan_host_policy(f.normalized_text, location=f.location)
        errors.extend(f"{f.location}: {x.category}: {x.reason}" for x in findings)
    return errors


def display(value):
    if value is None:
        return "なし"
    if value is True:
        return "true"
    if isinstance(value, list):
        return ", ".join(value)
    return str(value)


def case_rows(data):
    """All closed ART-17 data values must be visible, not only favorable fields."""
    expected = [
        f"Document Control Field Value {k} {display(v)}"
        for k, v in data.items()
        if k not in ("records", "evidence")
    ]
    for r in data["records"]:
        expected += [
            f"{r['recordId']} Field Value {k} {display(v)}" for k, v in r.items()
        ]
    for e in data["evidence"]:
        expected += [
            f"{e['id']} Field Value {k} {display(v)}"
            for k, v in e.items()
            if k != "claims"
        ]
        expected += [
            f"{e['id']} claims Field Value {k} {display(v)}"
            for k, v in e["claims"].items()
        ]
    return expected


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
        errors.append(f"{document.document_id}: finite H1/H2 inventory")
    counts = Counter(key(r) for _, r in relations(document))
    for r in spec["required"]:
        if counts[key(r)] != 1:
            errors.append(
                f"{document.document_id}: required semantic field missing/duplicate"
            )
    if document.document_id == DOCUMENTS[2]:
        actual = [
            f.text
            for f in document.fields
            if f.field_type == "reader_visible_text" and f.element_kind == "table_row"
        ]
        if actual != case_rows(data):
            errors.append("ART17 JSON/projected case parity")
    if document.document_id == DOCUMENTS[0]:
        # Source IDs must be visible in body AND in the final references section.
        body, refs = set(), set()
        for f, r in relations(document):
            if not is_policy_scan_field(f):
                continue
            for sid in SOURCE_IDS:
                if sid in f.text:
                    (refs if "参考文献・Source Note ID" in r["headings"] else body).add(
                        sid
                    )
        if body != set(SOURCE_IDS) or refs != set(SOURCE_IDS):
            errors.append("Chapter7 visible Source body/reference inventory")
    return errors


def json_safety(value, location=CASE_PATH):
    if isinstance(value, dict):
        return [e for k, v in value.items() for e in json_safety(v, f"{location}/{k}")]
    if isinstance(value, list):
        return [
            e for i, v in enumerate(value) for e in json_safety(v, f"{location}/{i}")
        ]
    if isinstance(value, str):
        # This data schema is plain text, not a markup surface. Reject markup
        # delimiters instead of attempting to interpret or strip them as syntax.
        if any(c in value for c in "<>&`\\"):
            return [f"{location}: ART17 plain-text data only"]
        return [
            f"{location}: {f.category}"
            for f in scan_action_text(value, location=location)
            + scan_host_policy(value, location=location)
        ]
    return []


def repository_errors(contract):
    errors = []
    for path, digest in contract["parentDigests"].items():
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != digest:
            errors.append(f"{path}: retained parent baseline")
    package = load_json_strict(ROOT / "package.json")["scripts"]
    if (
        package.get("check:chapter07") != "python3 scripts/check_chapter07_contract.py"
        or package["test"].split(" && ").count("npm run check:chapter07") != 1
    ):
        errors.append("root Chapter7 invocation")
    if not package["sync:docs"].startswith(
        "python3 scripts/check_chapter06_contract.py --no-regressions && "
        "python3 scripts/check_chapter07_contract.py --no-regressions && "
        "python3 scripts/sync_book_site.py "
    ):
        errors.append("Chapter7 publication preflight")
    registry = load_json_strict(ROOT / "site-pages.json")
    for k in ("pages", "staticFiles"):
        for item in contract[k]:
            if registry[k].count(item) != 1:
                errors.append("Chapter7 publication route " + item["source"])
    sources = load_json_strict(ROOT / "references/sources.json")["sources"]
    if {s["id"] for s in sources if 7 in s["chapters"]} != set(SOURCE_IDS):
        errors.append("Chapter7 Source mapping")
    for sid in SOURCE_IDS:
        s = next((s for s in sources if s["id"] == sid), {})
        if not meets_audit_baseline(
            s.get("checkedAt"), "2026-09-12"
        ) or not meets_audit_baseline(s.get("nextReviewAt"), "2026-12-12"):
            errors.append("Chapter7 scoped Source audit " + sid)
        for k, v in contract["sourceIdentity"][sid].items():
            if s.get(k) != v:
                errors.append("Chapter7 Source identity/status " + sid)
    for path, markers in contract["indices"].items():
        text = (ROOT / path).read_text(encoding="utf-8")
        if any(m not in text for m in markers):
            errors.append("Chapter7 index " + path)
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-regressions", action="store_true")
    args = parser.parse_args()
    try:
        contract = load_json_strict(ROOT / CONTRACT_PATH)
        data = load_json_strict(ROOT / CASE_PATH)
        parent = load_json_strict(ROOT / PARENT_PATH)
        behaviors = load_json_strict(ROOT / BEHAVIOR_PATH)
        snapshot = load_json_strict(ROOT / SNAPSHOT_PATH)
        snapshot_digest = hashlib.sha256(
            (ROOT / SNAPSHOT_PATH).read_bytes()
        ).hexdigest()
        if snapshot_digest != contract["sourceSnapshotSha256"]:
            raise ValueError(
                "audited public Source snapshot changed; review/re-extraction required"
            )
        if POLICY_VERSION != "1.2.0" or PROJECTION_VERSION != "1.1.0":
            raise ValueError("reviewed shared versions")
        if list(contract["documents"]) != list(DOCUMENTS):
            raise ValueError("finite complete document inventory")
        errors = (
            validate_case(data, parent, behaviors, snapshot, snapshot_digest)
            + json_safety(data)
            + repository_errors(contract)
        )
        source = {p: (ROOT / p).read_text(encoding="utf-8") for p in DOCUMENTS}
        projection = project_documents(source)
        if [d.document_id for d in projection.documents] != list(DOCUMENTS):
            raise ValueError("projected document inventory/order")
        for doc in projection.documents:
            errors += document_errors(doc, contract["documents"][doc.document_id], data)
        count = 0
        if not args.no_regressions:
            from scripts.chapter07_regressions import run_regressions

            count, tests = run_regressions(
                data, parent, behaviors, snapshot, snapshot_digest, contract, source
            )
            errors += tests
        if errors:
            for e in errors:
                print("ERROR:", e)
            return 1
        print(
            f"Chapter 7 contract passed: 4 complete documents; 6 ART-17 records; {count} regressions; Policy {POLICY_VERSION}; Projection {PROJECTION_VERSION}"
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
        print("ERROR: Chapter7 contract:", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
