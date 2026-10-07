"""Finite independent Chapter24 contrasts; not a renderer or policy corpus."""

from copy import deepcopy
from dataclasses import replace

from scripts.chapter24_model import (
    CORPUS,
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


def run_regressions(data, schema, contract, source, projection):
    from scripts.check_chapter24_contract import (
        ROOT,
        identity,
        document_errors,
        scan_document,
        reading_table_errors,
    )
    from scripts.publication_projection import project_documents

    errors, checked = [], set()

    def check(name, ok):
        if name in checked:
            errors.append("EV24 duplicate regression: " + name)
        checked.add(name)
        if not ok:
            errors.append("EV24 regression failed: " + name)

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
        == "finite-authored-source-evaluation-not-natural-language-truth",
    )
    for row in corpus["fixtures"]:
        changed = deepcopy(data)
        for op in row["changes"]:
            parent = at(changed, op["path"][:-1])
            key = int(op["path"][-1]) if isinstance(parent, list) else op["path"][-1]
            parent[key] = deepcopy(op["value"])
        error, actual = None, None
        try:
            # Refresh only the data snapshot: a rejection must not be a stale hash.
            spec = deepcopy(contract)
            spec["dataSha256"] = digest(changed)
            findings = validate_model(changed, schema, spec)
            if findings:
                raise ValueError("policy: " + "; ".join(findings))
            actual = evaluate(changed)
        except (OSError, ValueError, TypeError, KeyError, ManifestError) as exc:
            error = str(exc)
        if row["expected"] == "rejected":
            check(row["id"], bool(error) and row["errorContains"] in error)
        else:
            check(row["id"], error is None and actual == row["expectedResult"])

    # Required / closed object shape, independently of the content snapshot.
    for path, obj in objects(data):
        for key in obj:
            changed = deepcopy(data)
            del at(changed, path)[key]
            check(
                "missing:" + str((*path, key)),
                rejected(lambda: validate_schema_instance(changed, schema)),
            )
        changed = deepcopy(data)
        at(changed, path)["unexpected"] = True
        check(
            "unknown:" + str(path),
            rejected(lambda: validate_schema_instance(changed, schema)),
        )
    bad_schema = deepcopy(schema)
    bad_schema["unknownKeyword"] = True
    check(
        "unknown-schema-keyword",
        rejected(
            lambda: validate_supported_schema_nodes(bad_schema, "schema", bad_schema)
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
    case = next(d for d in projection.documents if d.document_id == DOCUMENTS[2])
    changed = deepcopy(data)
    changed["record"]["actualCollections"] = 1
    check("all-leaf-parity", bool(reading_table_errors(case, changed)))
    return len(checked), errors
