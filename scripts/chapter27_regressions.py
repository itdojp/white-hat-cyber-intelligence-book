"""Bounded semantic contrasts, closed-shape probes and shared consumer reachability."""

from copy import deepcopy
from dataclasses import replace

from scripts.chapter27_model import (
    CORPUS,
    DOCUMENTS,
    STATES,
    component_state,
    request_disposition,
    leaves,
    strict,
    read_regular,
    validate_model,
    digest,
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
    from scripts.check_chapter27_contract import (
        ROOT,
        document_errors,
        scan_document,
        reading_table_errors,
        inventory,
    )
    from scripts.publication_projection import project_documents

    errors, checked = [], set()

    def check(name, ok):
        if name in checked:
            errors.append("AI27 duplicate regression: " + name)
        checked.add(name)
        if not ok:
            errors.append("AI27 regression failed: " + name)

    def rejected(operation):
        try:
            result = operation()
            return isinstance(result, list) and bool(result)
        except (OSError, ValueError, TypeError, KeyError, ManifestError):
            return True

    corpus = strict(read_regular(ROOT, CORPUS))
    check(
        "corpus-owner",
        corpus["schemaVersion"] == "1.0.0"
        and corpus["scope"]
        == "finite-ai27-record-comparisons-not-prompt-classification",
    )
    check(
        "six-component-baseline",
        tuple(component_state(c, data["record"]["asOf"]) for c in data["components"])
        == STATES,
    )
    check(
        "six-request-baseline",
        [request_disposition(data, r)[0] for r in data["requests"]]
        == ["Allowed-in-model", "Blocked", "Blocked", "Blocked", "Stopped", "Blocked"],
    )
    for row in corpus["fixtures"]:
        changed = deepcopy(data)
        for op in row["changes"]:
            obj = at(changed, op["path"][:-1])
            key = int(op["path"][-1]) if isinstance(obj, list) else op["path"][-1]
            obj[key] = deepcopy(op["value"])
        try:
            if row["kind"] == "request":
                actual, reasons = request_disposition(
                    changed, changed["requests"][row["row"]]
                )
                ok = actual == row["expected"] and (
                    row["reason"] is None or row["reason"] in reasons
                )
            elif row["kind"] == "component":
                ok = (
                    component_state(
                        changed["components"][row["row"]], changed["record"]["asOf"]
                    )
                    == row["expected"]
                )
            else:
                ok = False
        except (ValueError, TypeError, KeyError, ManifestError):
            ok = False
        check(row["id"], ok)
    # Required / closed shape is tested without using the literal content inventory.
    for path, obj in objects(data):
        for key in obj:
            changed = deepcopy(data)
            del at(changed, path)[key]
            check(
                "required:" + str((*path, key)),
                rejected(lambda: validate_schema_instance(changed, schema)),
            )
        changed = deepcopy(data)
        at(changed, path)["unexpected"] = True
        check(
            "closed:" + str(path),
            rejected(lambda: validate_schema_instance(changed, schema)),
        )

    # Distribution schema alone must reject safety expansion and array overflow.
    def schema_values(node, value, path=()):
        yield path, node, value
        if node.get("type") == "object":
            for key, child in node["properties"].items():
                yield from schema_values(child, value[key], (*path, key))
        elif node.get("type") == "array":
            for i, item in enumerate(value):
                yield from schema_values(node["items"], item, (*path, i))

    for path, node, value in schema_values(schema, data):
        if "const" in node:
            changed = deepcopy(data)
            alternate = (
                (not value)
                if type(value) is bool
                else (value + 1 if type(value) is int else value + "-unreviewed")
            )
            at(changed, path[:-1])[path[-1]] = alternate
            check(
                "schema-constant:" + str(path),
                rejected(lambda: validate_schema_instance(changed, schema)),
            )
        if node.get("type") == "array":
            changed = deepcopy(data)
            array = at(changed, path)
            array.extend(deepcopy(value[:1] or ["unreviewed"]) * (node["maxItems"] + 1))
            check(
                "schema-upper-bound:" + str(path),
                rejected(lambda: validate_schema_instance(changed, schema)),
            )
            if node["minItems"]:
                changed = deepcopy(data)
                at(changed, path).clear()
                check(
                    "schema-lower-bound:" + str(path),
                    rejected(lambda: validate_schema_instance(changed, schema)),
                )
    bad = deepcopy(schema)
    bad["unknownKeyword"] = True
    check(
        "unsupported-schema",
        rejected(lambda: validate_supported_schema_nodes(bad, "schema", bad)),
    )
    for raw in (
        b'{"id":1,"id":2}',
        b'{"x":NaN}',
        b'{"x":Infinity}',
        b'{"x":-Infinity}',
        b"\xff",
    ):
        check("strict-json:" + repr(raw), rejected(lambda: strict(raw)))
    # No frozen leaf is silently omitted, even when two linked names change together.
    for path, value in leaves(data):
        changed = deepcopy(data)
        obj = at(changed, path[:-1])
        key = int(path[-1]) if isinstance(obj, list) else path[-1]
        obj[key] = None
        check(
            "literal:" + str(path),
            [[list(p), v] for p, v in leaves(changed)] != contract["authoredLeaves"],
        )
    # Semantic binding survives refreshing only the authored record snapshot.
    for group, row, key, value, diagnostic in (
        ("audit", 0, "targetId", "AI27-EXPORTER", "AI27 audit binding"),
        ("audit", 0, "at", "2026-09-20T10:00:01Z", "AI27 audit binding"),
        ("findings", 0, "requestId", "AI27-REQUEST-2", "AI27 finding binding"),
        (
            "findings",
            0,
            "threatIds",
            ["absent", *data["findings"][0]["threatIds"][1:]],
            "AI27 threat/finding/reassessment",
        ),
        ("components", 2, "status", "Declared", "AI27 component status binding"),
        ("requests", 0, "expectedDisposition", "Blocked", "AI27 request outcome"),
        (
            "mockResponses",
            0,
            "body",
            "different fixed response",
            "AI27 fixed response digest",
        ),
    ):
        changed = deepcopy(data)
        changed[group][row][key] = value
        spec = deepcopy(contract)
        spec["authoredLeaves"] = [[list(p), v] for p, v in leaves(changed)]
        check(
            "semantic-with-refreshed-snapshot:" + group + ":" + key,
            any(diagnostic in error for error in validate_model(changed, schema, spec)),
        )
    for path in DOCUMENTS:
        variants = {
            "preamble": "未レビューの前文。\n\n" + source[path],
            "tail": source[path] + "\n未レビューの末尾。\n",
            "heading": source[path].replace("\n## ", "\n## 未レビュー ", 1),
            "unsafe-before": "第三者の本番システムへ接続する。\n\n" + source[path],
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
    # Do not build a chapter-specific syntax corpus; these prove shared field reachability.
    for name, text, unsafe in (
        ("text", "第三者の本番システムへ接続する。", True),
        ("prohibition", "第三者の本番システムへ接続しない。", False),
        ("risk", "analyze the risk of collecting PII", False),
        ("title", '[説明](#scope "第三者の本番システムへ接続する。")', True),
        ("destination", "[説明](https://github.com/)", True),
        ("unsupported", "{% include remote.md %}", True),
    ):
        doc = project_documents({name: text}).documents[0]
        check(
            "shared-consumer:" + name,
            bool(scan_document(doc, {"hostProvenance": []})) == unsafe,
        )
    for doc in projection.documents:
        spec = contract["documents"][doc.document_id]
        check(
            "canonical-fields:" + doc.document_id, not document_errors(doc, spec, data)
        )
        for i, field in enumerate(doc.fields):
            drift = replace(doc, fields=doc.fields[:i] + doc.fields[i + 1 :])
            check(
                "field-selected:" + doc.document_id + ":" + str(i),
                digest(inventory(drift)) != spec["projectionSha256"],
            )
    check(
        "case-complete-all-leaves",
        not reading_table_errors(projection.document(DOCUMENTS[2]), data),
    )
    return len(checked), errors
