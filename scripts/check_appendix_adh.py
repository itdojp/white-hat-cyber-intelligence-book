#!/usr/bin/env python3
"""Finite A/D/H reference consumer; no new syntax or safety grammar.

Reviewed projected fields and fixed parent bytes bound the reference edition.
Parent checkers still own their semantic judgments. Any reader-field change
requires review and an explicit fixture update, not a new exception or parser.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_editorial_input_manifest import (  # noqa: E402
    _reject_constant, _reject_duplicate_keys,
)
from scripts.content_safety_policy import (  # noqa: E402
    POLICY_VERSION, scan_action_text, scan_host_policy,
)
from scripts.publication_projection import (  # noqa: E402
    PROJECTION_VERSION, project_documents, is_policy_scan_field,
    is_absolute_destination,
)

DOCUMENTS = (
    "appendices/appendix-a-legal-safety.md",
    "appendices/appendix-d-troubleshooting.md",
    "appendices/appendix-h-lab-operations.md",
    "references/appendix-adh-source-review-2026-10-17.md",
)
ENTRIES = ("legal-notice.md", "troubleshooting.md")
CONTRACT = "tests/fixtures/appendix-adh/publication-contract.json"
PARENTS = (
    "templates/authorization-checklist.md",
    "templates/rules-of-engagement.md",
    "templates/lab-safety-evidence-plan.md",
    "cases/fixtures/ch08-lab-plan.json",
    "cases/fixtures/ch08-control-receipts.json",
    "cases/fixtures/ch08-evidence-manifest.json",
    "cases/fixtures/ch09-engagement-roe.json",
    "cases/fixtures/ch14-minimal-impact-validation.json",
    "cases/fixtures/ch19-incident-response.json",
    "cases/fixtures/ch20-dfir-timeline-causality.json",
    "LAB_ARCHITECTURE.md",
    "SAFETY_SCOPE.md",
)
SOURCE_IDS = (
    "SRC-JP-LAW-001", "SRC-IPA-VDP-001", "SRC-SECURITYTXT-001",
    "SRC-NIST-TEST-001", "SRC-NIST-DFIR-001",
)
INPUTS = (*DOCUMENTS, *ENTRIES, *PARENTS, CONTRACT, "site-pages.json", "package.json",
          "references/sources.json")
PREFLIGHT = "python3 scripts/check_appendix_adh.py"


def read_input(root, name):
    if name not in INPUTS or root.is_symlink():
        raise ValueError("ADH-fixed-input")
    path = root / name
    if any(p.is_symlink() for p in (path, *path.parents) if p.is_relative_to(root)):
        raise ValueError("ADH-symlink-input")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError("ADH-regular-input")
        raw = stream.read(1_048_577)
    if len(raw) > 1_048_576:
        raise ValueError("ADH-input-size")
    return raw.decode("utf-8")


def strict(text):
    return json.loads(text, object_pairs_hook=_reject_duplicate_keys,
                      parse_constant=_reject_constant)


def fields(document):
    return [[f.field_type, f.element_kind, f.attribute, f.metadata_value("level"), f.text]
            for f in document.fields]


def document_errors(documents, contract):
    if tuple(documents) != DOCUMENTS or tuple(contract["documents"]) != DOCUMENTS:
        return ["ADH-document-inventory"]
    projection = project_documents(documents)
    errors = [f"ADH-projection: {d.code}: {d.location}" for d in projection.diagnostics]
    for document in projection.documents:
        for field in document.fields:
            findings = []
            if is_policy_scan_field(field):
                findings += scan_action_text(field.normalized_text, location=field.location)
            if is_policy_scan_field(field) or (
                field.field_type == "destination" and is_absolute_destination(field.normalized_text)
            ):
                findings += scan_host_policy(field.normalized_text, location=field.location)
            errors += [f"ADH-safety: {f.category}: {f.location}" for f in findings]
        if fields(document) != contract["documents"][document.document_id]:
            errors.append("ADH-reader-fields: " + document.document_id)
    return errors


def repository_errors(inputs, contract):
    errors = []
    if (contract["version"] != "1.0.0"
            or contract["projection"] != PROJECTION_VERSION
            or contract["policy"] != POLICY_VERSION
            or tuple(contract["parentDigests"]) != PARENTS):
        errors.append("ADH-contract-identity")
    for name in PARENTS:
        if hashlib.sha256(inputs[name].encode()).hexdigest() != contract["parentDigests"][name]:
            errors.append("ADH-parent-review-required: " + name)
    sources = strict(inputs["references/sources.json"])["sources"]
    if tuple(contract["sourceIdentity"]) != SOURCE_IDS:
        errors.append("ADH-source-inventory")
    for identifier in SOURCE_IDS:
        matches = [s for s in sources if s["id"] == identifier]
        expected = contract["sourceIdentity"][identifier]
        if len(matches) != 1 or any(matches[0].get(k) != v for k, v in expected.items()):
            errors.append("ADH-source-identity: " + identifier)
    registry, package = (strict(inputs[p]) for p in ("site-pages.json", "package.json"))
    pages = registry["pages"]
    if [p["source"] for p in contract["routes"]] != list(DOCUMENTS):
        errors.append("ADH-route-inventory")
    for route in contract["routes"]:
        if (pages.count(route) != 1
                or sum(p["source"] == route["source"] for p in pages) != 1
                or sum(p["destination"] == route["destination"] for p in pages) != 1
                or sum((p["section"], p["order"]) == (route["section"], route["order"])
                       for p in pages) != 1):
            errors.append("ADH-route: " + route["source"])
    # The existing architecture route is not moved or shadowed by H.
    if any(p["destination"] == "appendices/lab-guide/index.md" for p in pages):
        errors.append("ADH-legacy-route-owner")
    scripts = package["scripts"]
    steps = scripts["sync:docs"].split(" && ")
    if (scripts.get("check:appendix-adh") != PREFLIGHT + " && python3 tests/test_appendix_adh.py"
            or scripts["test"].split(" && ").count("npm run check:appendix-adh") != 1
            or steps.count(PREFLIGHT) != 1
            or steps.index(PREFLIGHT) >= steps.index("python3 scripts/sync_book_site.py --output docs")):
        errors.append("ADH-entrypoints")
    projection = project_documents({name: inputs[name] for name in ENTRIES})
    errors += ["ADH-entry-projection: " + d.code for d in projection.diagnostics]
    if tuple(contract["entryLinks"]) != ENTRIES:
        errors.append("ADH-entry-inventory")
    for name in ENTRIES:
        destinations = [f.text for f in projection.document(name).fields
                        if f.field_type == "destination"]
        for target in contract["entryLinks"][name]:
            if destinations.count(target) != 1:
                errors.append("ADH-return-link: " + name)
    return errors


def main():
    try:
        inputs = {name: read_input(ROOT, name) for name in INPUTS}
        contract = strict(inputs[CONTRACT])
        errors = repository_errors(inputs, contract)
        errors += document_errors({name: inputs[name] for name in DOCUMENTS}, contract)
    except (OSError, ValueError, TypeError, KeyError, RuntimeError) as exc:
        print(f"Appendix A/D/H failed closed: {exc}", file=sys.stderr)
        return 1
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    print(f"Appendix A/D/H passed: 4 full surfaces / 12 parent bindings; "
          f"Policy {POLICY_VERSION}; Projection {PROJECTION_VERSION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
