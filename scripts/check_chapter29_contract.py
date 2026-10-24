#!/usr/bin/env python3
"""Chapter 29 finite selection and joins; shared renderer and safety owners only."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.chapter29_model import (  # noqa: E402
    DATA, SCHEMA, BINDINGS, PUBLICATION, DOCUMENTS, SOURCES, case_groups,
    digest, strict, read_regular, model_errors, require,
)
from scripts.check_editorial_input_manifest import ManifestError  # noqa: E402
from scripts.content_safety_policy import (  # noqa: E402
    POLICY_VERSION, scan_action_text, scan_host_policy,
)
from scripts.publication_projection import (  # noqa: E402
    PROJECTION_VERSION, project_documents, is_policy_scan_field,
    is_absolute_destination, ProjectionRuntimeError,
)


def field_identity(field):
    return [field.field_type, field.element_kind, field.attribute,
            field.metadata_value("level"), field.text, field.location]


def projection_digest(document):
    return digest(json.dumps([field_identity(f) for f in document.fields],
                             ensure_ascii=False, separators=(",", ":")).encode())


def document_errors(document, spec, data):
    errors = ["CAP29-projection: " + d.code for d in document.diagnostics]
    # Exact whole-field provenance, never a suffix/host allow-list. Every entry
    # requires identity/cardinality and review; action scanning is never excluded.
    identities = [field_identity(f) for f in document.fields]
    provenance = spec["hostProvenance"]
    counts = Counter(json.dumps(v, ensure_ascii=False) for v in identities)
    if (len({json.dumps(v, ensure_ascii=False) for v in provenance}) != len(provenance)
            or any(counts[json.dumps(v, ensure_ascii=False)] != 1 for v in provenance)):
        errors.append("CAP29-provenance-cardinality")
    for f in document.fields:
        findings = []
        if is_policy_scan_field(f):
            findings += scan_action_text(f.normalized_text, location=f.location)
        if (is_policy_scan_field(f) or (f.field_type == "destination"
                and is_absolute_destination(f.normalized_text))) and field_identity(f) not in provenance:
            findings += scan_host_policy(f.normalized_text, location=f.location)
        errors += ["CAP29-" + x.category + ": " + x.location for x in findings]
    if len(document.fields) != spec["fieldCount"] or projection_digest(document) != spec["sha256"]:
        errors.append("CAP29-finite-reader-fields: " + document.document_id)
    if document.document_id == DOCUMENTS[2]:
        active, rows = False, []
        for f in document.fields:
            if f.element_kind == "heading" and f.metadata_value("level") == 2:
                active = f.text == "全欄の読み方"
            if active and f.element_kind == "table_row" and is_policy_scan_field(f):
                rows.append(f.text)
        expected = [" ".join((group + " Field Value " + key + " " + val).split())
                    for group, pairs in case_groups(data) for key, val in pairs]
        if rows != expected:
            errors.append("CAP29-case-data-parity")
    return errors


def chapter_navigation_errors(site):
    """The final chapter follows Chapter 28, not a contiguous-order guess."""
    chapters = sorted((r for r in site["pages"] if r["section"] == "chapters"),
                      key=lambda r: r["order"])
    expected = ["manuscript/28-ai-assisted-analysis-assurance.md", DOCUMENTS[0]]
    if ([r["source"] for r in chapters[-2:]] != expected
            or chapters[-2]["order"] >= chapters[-1]["order"]):
        return ["CAP29-chapter-navigation: Chapter 29 must follow Chapter 28"]
    return []


ARTIFACT_INDEX = "artifact-index.md"
EXPECTED_INDEX_ROW = (
    "Artifact Index ID 成果物 主な章 テンプレート "
    "ART-33 Final Security Decision Portfolio Index 29 "
    "templates/final-security-decision-portfolio-index.md"
)


def artifact_index_errors(document):
    """Check only Chapter 29's registration, using shared projected table rows.

    A prose mention is not a catalog row. This is not a parser or a substitute
    for a future whole-index safety/catalog contract.
    """
    rows = [field.text for field in document.fields
            if field.element_kind == "table_row"
            and "ART-33" in field.text.split()]
    if document.diagnostics or rows != [EXPECTED_INDEX_ROW]:
        return ["CAP29-artifact-index-registration"]
    return []


def repository_errors(root, data, bindings, pub):
    allowed = set(bindings["parents"]) | set(pub["inputDigests"]) | {
        "site-pages.json", "package.json", "references/sources.json", "book-config.json",
        *DOCUMENTS, BINDINGS, PUBLICATION, DATA, SCHEMA, ARTIFACT_INDEX,
    }
    inputs = {p: read_regular(root, p, allowed) for p in allowed}
    index = project_documents({ARTIFACT_INDEX: inputs[ARTIFACT_INDEX].decode()}).documents[0]
    require(not artifact_index_errors(index), "artifact-index-registration")
    for p, expected in {**bindings["parents"], **pub["inputDigests"]}.items():
        require(digest(inputs[p]) == expected, "reviewed-input-drift: " + p)
    for row in data["artifacts"]:
        lines = inputs[row["canonicalPath"]].decode().splitlines()
        require(lines[row["nativeState"]["line"]-1] == row["nativeState"]["verbatim"],
                "native-state-location")
    for proof in data["documentaryEvidence"]:
        raw = inputs[proof["path"]]
        require(digest(raw) == proof["sourceSha256"]
                and proof["verbatim"] in raw.decode().splitlines()[proof["line"]-1],
                "documentary-location")
    package = strict(inputs["package.json"])["scripts"]
    command = "python3 scripts/check_chapter29_contract.py"
    preflight = package["sync:docs"].split(" && ")
    require(package.get("check:chapter29") == command
            and package["test"].split(" && ").count("npm run check:chapter29") == 1
            and preflight.count(command + " --no-regressions") == 1
            and preflight.index(command + " --no-regressions")
            < preflight.index("python3 scripts/sync_book_site.py --output docs"), "entrypoints")
    site = strict(inputs["site-pages.json"])
    require(not chapter_navigation_errors(site), "chapter-navigation")
    for key, routes in pub["routes"].items():
        for row in routes:
            require(site[key].count(row) == 1 and sum(
                r["source"] == row["source"] or r["destination"] == row["destination"]
                for r in site[key]) == 1, "route")
    sources = strict(inputs["references/sources.json"])
    require(sources["checkedAt"] == "2026-07-25" and {
        s["id"] for s in sources["sources"] if 29 in s["chapters"]} == set(SOURCES), "sources")
    for sid, expected in pub["sourceIdentity"].items():
        s = next(s for s in sources["sources"] if s["id"] == sid)
        require(all(s[k] == v for k, v in expected.items()), "source-version-review")
    chapter = strict(inputs["book-config.json"])["structure"]["chapters"][29]
    require(chapter == pub["chapter"], "chapter-identity")
    return inputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-regressions", action="store_true")
    args = parser.parse_args()
    try:
        initial = (DATA, SCHEMA, BINDINGS, PUBLICATION)
        data, schema, bindings, pub = [strict(read_regular(ROOT, p, initial)) for p in initial]
        require(pub["version"] == "1.0.0" and pub["policy"] == POLICY_VERSION == "1.2.0"
                and pub["projection"] == PROJECTION_VERSION == "1.1.0"
                and list(pub["documents"]) == list(DOCUMENTS), "shared-inventory")
        errors = model_errors(data, schema, bindings)
        inputs = repository_errors(ROOT, data, bindings, pub)
        projection = project_documents({p: inputs[p].decode() for p in DOCUMENTS})
        require([d.document_id for d in projection.documents] == list(DOCUMENTS), "document-inventory")
        for doc in projection.documents:
            errors += document_errors(doc, pub["documents"][doc.document_id], data)
        if errors:
            raise ValueError("; ".join(errors))
        count = 0
        if not args.no_regressions:
            from scripts.chapter29_regressions import run_regressions
            count = run_regressions(data, schema, bindings, pub, projection, ROOT)
        print(f"Chapter29 contract passed: 32 references; 12 stages; 4 DOC; 4 gaps; 8 review areas; {count} regressions; Policy {POLICY_VERSION}; Projection {PROJECTION_VERSION}; offline only")
        return 0
    except (OSError, ValueError, KeyError, TypeError, IndexError, StopIteration,
            ManifestError, ProjectionRuntimeError) as exc:
        print("ERROR: Chapter29 fail closed:", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
