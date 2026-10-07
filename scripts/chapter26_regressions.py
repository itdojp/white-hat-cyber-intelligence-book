"""Finite independent Chapter26 contrasts; not a renderer or policy corpus."""

from copy import deepcopy
from dataclasses import replace
from unittest.mock import patch
import os

from scripts.chapter26_model import (
    CORPUS,
    DATA,
    BUNDLE,
    TAXII,
    DOCUMENTS,
    digest,
    strict,
    read_regular,
    evaluate,
    validate_model,
)
from scripts.check_editorial_input_manifest import (
    ManifestError,
    validate_schema_instance,
    validate_supported_schema_nodes,
)


def at(value, path):
    for key in path:
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def objects(value, path=()):
    if isinstance(value, dict):
        yield path, value
        for key, child in value.items():
            yield from objects(child, (*path, key))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            yield from objects(child, (*path, i))


def run_regressions(data, bundle, taxii, schemas, contract, source, projection):
    from scripts.check_chapter26_contract import (
        ROOT,
        STIX_REVIEW_TRIGGERS,
        TAXII_REVIEW_TRIGGERS,
        standard_source_errors,
        chapter_order_errors,
        identity,
        document_errors,
        scan_document,
        reading_table_errors,
    )
    from scripts.publication_projection import project_documents

    errors, checked = [], set()

    def check(name, ok):
        if name in checked:
            errors.append("CTI26 duplicate regression: " + name)
        checked.add(name)
        if not ok:
            errors.append("CTI26 regression failed: " + name)

    def rejected(fn):
        try:
            value = fn()
            return isinstance(value, list) and bool(value)
        except (OSError, ValueError, TypeError, KeyError, ManifestError):
            return True

    corpus = strict(read_regular(ROOT, CORPUS))
    check(
        "corpus-owner",
        corpus["schemaVersion"] == "1.0.0"
        and corpus["scope"]
        == "finite-authored-product-and-independent-exchange-not-general-standard-or-truth",
    )
    values = {"data": data, "bundle": bundle, "taxii": taxii}
    names = {"data": DATA, "bundle": BUNDLE, "taxii": TAXII}
    for row in corpus["fixtures"]:
        changed = deepcopy(values)
        for op in row["changes"]:
            parent = at(changed[op["target"]], op["path"][:-1])
            key = int(op["path"][-1]) if isinstance(parent, list) else op["path"][-1]
            parent[key] = deepcopy(op["value"])
        error, actual = None, None
        try:
            # Refresh all three snapshots: semantics, not stale hashes, must reject.
            spec = deepcopy(contract)
            spec["dataDigests"] = {p: digest(changed[k]) for k, p in names.items()}
            findings = validate_model(
                changed["data"], changed["bundle"], changed["taxii"], schemas, spec
            )
            if findings:
                raise ValueError("policy: " + "; ".join(findings))
            actual = evaluate(changed["data"])
        except (OSError, ValueError, TypeError, KeyError, ManifestError) as exc:
            error = str(exc)
        if row["expected"] == "rejected":
            check(row["id"], bool(error) and row["errorContains"] in error)
        else:
            check(row["id"], error is None and actual == row["expectedResult"])
        check(
            row["id"] + ":owned",
            bool(row["invariant"])
            and row["owner"] == "Chapter26 finite product/exchange profile",
        )

    # Required and closed object shapes, independent of the content snapshots.
    for (label, value), schema in zip(values.items(), schemas, strict=True):
        for path, obj in objects(value):
            for key in obj:
                changed = deepcopy(value)
                del at(changed, path)[key]
                check(
                    label + ":missing:" + str((*path, key)),
                    rejected(lambda: validate_schema_instance(changed, schema)),
                )
            changed = deepcopy(value)
            at(changed, path)["unexpected"] = True
            check(
                label + ":unknown:" + str(path),
                rejected(lambda: validate_schema_instance(changed, schema)),
            )
        bad_schema = deepcopy(schema)
        bad_schema["unknownKeyword"] = True
        check(
            label + ":unknown-schema-keyword",
            rejected(
                lambda: validate_supported_schema_nodes(
                    bad_schema, "schema", bad_schema
                )
            ),
        )
    for raw in (
        b'{"id":1,"id":2}',
        b'{"x":NaN}',
        b'{"x":Infinity}',
        b'{"x":-Infinity}',
    ):
        check("strict-json:" + repr(raw), rejected(lambda: strict(raw)))
    for path in ("../Gemfile", "/etc/passwd"):
        check("fixed-input:" + path, rejected(lambda: read_regular(ROOT, path)))
    for flag in ("O_NOFOLLOW", "O_NONBLOCK"):
        with patch.object(os, flag, create=True):
            delattr(os, flag)
            check("platform:" + flag, rejected(lambda: read_regular(ROOT, DATA)))
    pages = strict(read_regular(ROOT, "site-pages.json"))["pages"]
    check("navigation:canonical", not chapter_order_errors(pages))
    check(
        "navigation:registry-order-independent",
        not chapter_order_errors(list(reversed(pages))),
    )
    for value in (208, 210):
        changed = deepcopy(pages)
        next(p for p in changed if p["source"] == DOCUMENTS[0])["order"] = value
        check(
            "navigation:before-or-equal-25:" + str(value),
            bool(chapter_order_errors(changed)),
        )
    # Reviews 4117146440 / 4117288138 / 4117295893: the two scoped
    # standards retain stage/property revalidation and clean new note prefixes.
    for standard, required in (
        ("STIX", STIX_REVIEW_TRIGGERS),
        ("TAXII", TAXII_REVIEW_TRIGGERS),
    ):
        for label, triggers, accepted in (
            ("canonical", list(required), True),
            ("reordered", list(reversed(required)), True),
            ("extended", [*required, "additional scoped review"], True),
            ("standard-only", ["new OASIS Standard"], False),
            ("not-list", None, False),
            ("not-text", [*required, 1], False),
            *(
                (
                    "missing-" + str(i),
                    [t for j, t in enumerate(required) if j != i],
                    False,
                )
                for i in range(len(required))
            ),
        ):
            check(
                "source-" + standard.lower() + "-trigger:" + label,
                (
                    not standard_source_errors(
                        {
                            "reviewTriggers": triggers,
                            "notes": "Chapter26 scoped review",
                        },
                        standard,
                    )
                )
                is accepted,
            )
        for label, prefix in (("space", " "), ("tab", "\t")):
            check(
                "source-" + standard.lower() + "-notes:" + label,
                bool(
                    standard_source_errors(
                        {
                            "reviewTriggers": list(required),
                            "notes": prefix + "Chapter26 scoped review",
                        },
                        standard,
                    )
                ),
            )
    # Shared scanner reachability, full preamble/body/tail and heading selection.
    for path in DOCUMENTS:
        variants = {
            "preamble": "未レビューの前文。\n\n" + source[path],
            "tail": source[path] + "\n未レビューの末尾。\n",
            "heading": source[path].replace("\n## ", "\n## 未レビュー ", 1),
            "unsafe-before": "第三者の本番システムへ接続する。\n\n" + source[path],
            "unsafe-body": source[path].replace(
                "\n## ", "\n第三者の本番システムへ接続する。\n\n## ", 1
            ),
            "unsafe-after": source[path] + "\n第三者の本番システムへ接続する。\n",
        }
        for label, text in variants.items():
            doc = project_documents({path: text}).documents[0]
            check(
                "selection:" + path + ":" + label,
                bool(document_errors(doc, contract["documents"][path], data)),
            )
            if label.startswith("unsafe"):
                check(
                    "shared-action:" + path + ":" + label,
                    any(
                        "target.real_or_external" in e
                        for e in scan_document(doc, {"hostProvenance": []})
                    ),
                )
    for doc in project_documents(
        {
            "prohibition": "第三者の本番システムへ接続しない。",
            "risk": "analyze the risk of collecting PII",
        }
    ).documents:
        check("safe:" + doc.document_id, not scan_document(doc, {"hostProvenance": []}))
    for doc in projection.documents:
        spec = contract["documents"][doc.document_id]
        check("canonical:" + doc.document_id, not document_errors(doc, spec, data))
        for i, entry in enumerate(spec["hostProvenance"]):
            wrong = deepcopy(spec)
            wrong["hostProvenance"][i][-1] = "unreviewed-location"
            check(
                "provenance-location:" + doc.document_id + str(i),
                bool(scan_document(doc, wrong)),
            )
            doubled = deepcopy(spec)
            doubled["hostProvenance"].append(entry)
            check(
                "provenance-duplicate:" + doc.document_id + str(i),
                bool(scan_document(doc, doubled)),
            )
        # Directly mutate projected text at the same reviewed location: action
        # policy is never exempt, even if host provenance is explicitly allowed.
        if spec["hostProvenance"]:
            f = next(f for f in doc.fields if identity(f) == spec["hostProvenance"][0])
            changed = replace(
                f,
                text="第三者の本番システムへ接続する。",
                normalized_text="第三者の本番システムへ接続する。",
                field_type="reader_visible_text",
            )
            changed_doc = replace(doc, fields=(changed,))
            check(
                "provenance-action-not-exempt:" + doc.document_id,
                bool(
                    scan_document(changed_doc, {"hostProvenance": [identity(changed)]})
                ),
            )
    case = next(d for d in projection.documents if d.document_id == DOCUMENTS[3])
    changed = deepcopy(data)
    changed["record"]["asOf"] = "2026-07-29T11:00:01Z"
    check("all-leaf-parity", bool(reading_table_errors(case, changed)))
    return len(checked), errors
