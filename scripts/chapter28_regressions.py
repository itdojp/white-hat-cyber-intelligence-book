"""Bounded Chapter28 semantic/shape/selection probes, not a renderer syntax corpus."""

from copy import deepcopy
from dataclasses import replace
from scripts.chapter28_model import (
    CORPUS,
    DOCUMENTS,
    strict,
    read_regular,
    leaves,
    digest,
    resolve,
    validate_model,
)
from scripts.check_editorial_input_manifest import (
    ManifestError,
    validate_schema_instance,
    validate_supported_schema_nodes,
)


def objects(value, path=()):
    if isinstance(value, dict):
        yield path, value
        for k, v in value.items():
            yield from objects(v, (*path, k))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from objects(v, (*path, i))


def run_regressions(data, schema, contract, source, projection, parent25, parent26):
    from scripts.check_chapter28_contract import (
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
            errors.append("AI28 duplicate probe: " + name)
        checked.add(name)
        if not ok:
            errors.append("AI28 failed probe: " + name)

    def rejected(operation):
        try:
            return bool(operation())
        except (ValueError, OSError, TypeError, KeyError, ManifestError):
            return True

    corpus = strict(read_regular(ROOT, CORPUS))
    check(
        "corpus-owner",
        corpus["schemaVersion"] == "1.0.0"
        and corpus["scope"]
        == "finite-ai28-source-claim-human-comparisons-not-model-evaluation"
        and len(corpus["families"]) == len(set(corpus["families"])) == 16,
    )
    check(
        "family-completeness",
        {r["family"] for r in corpus["fixtures"]} == set(corpus["families"])
        and all(
            any(r["family"] == f and r["expectedAccepted"] for r in corpus["fixtures"])
            and any(
                r["family"] == f and not r["expectedAccepted"]
                for r in corpus["fixtures"]
            )
            for f in corpus["families"]
        ),
    )
    for row in corpus["fixtures"]:
        changed, spec = deepcopy(data), deepcopy(contract)
        for op in row["changes"]:
            obj = resolve(changed, op["path"][:-1])
            key = op["path"][-1]
            obj[int(key) if isinstance(obj, list) else key] = deepcopy(op["value"])
        spec["authoredLeaves"] = [[list(p), v] for p, v in leaves(changed)]
        result = validate_model(changed, schema, spec, parent25, parent26)
        check(
            row["id"],
            bool(result) != row["expectedAccepted"]
            and (
                row["diagnostic"] is None or any(row["diagnostic"] in e for e in result)
            )
            and row["owner"] == "Chapter28 Layer A"
            and row["snapshotRefreshed"] is True,
        )
    # Every object is required and closed independently of frozen literal content.
    for path, obj in objects(data):
        for key in obj:
            changed = deepcopy(data)
            del resolve(changed, path)[key]
            check(
                "required:" + str((*path, key)),
                rejected(lambda: validate_schema_instance(changed, schema)),
            )
        changed = deepcopy(data)
        resolve(changed, path)["unexpected"] = True
        check(
            "closed:" + str(path),
            rejected(lambda: validate_schema_instance(changed, schema)),
        )

    # Explicit null, booleans, integers, constants and every array bound use the shared validator.
    def nodes(node, value, path=()):
        yield path, node, value
        if node.get("type") == "object":
            for k, child in node["properties"].items():
                yield from nodes(child, value[k], (*path, k))
        elif node.get("type") == "array":
            for i, child in enumerate(value):
                yield from nodes(node["items"], child, (*path, i))

    for path, node, value in nodes(schema, data):
        if "const" in node:
            changed = deepcopy(data)
            resolve(changed, path[:-1])[path[-1]] = (
                not value if type(value) is bool else str(value) + "-unreviewed"
            )
            check(
                "constant:" + str(path),
                rejected(lambda: validate_schema_instance(changed, schema)),
            )
        if node.get("type") == "array":
            changed = deepcopy(data)
            array = resolve(changed, path)
            array.extend(deepcopy(value[:1] or ["unreviewed"]) * (node["maxItems"] + 1))
            check(
                "upper:" + str(path),
                rejected(lambda: validate_schema_instance(changed, schema)),
            )
            if node["minItems"]:
                changed = deepcopy(data)
                resolve(changed, path).clear()
                check(
                    "lower:" + str(path),
                    rejected(lambda: validate_schema_instance(changed, schema)),
                )
    for path, value in leaves(data):
        changed = deepcopy(data)
        obj = resolve(changed, path[:-1])
        key = int(path[-1]) if isinstance(obj, list) else path[-1]
        obj[key] = "changed-null" if value is None else None
        check(
            "leaf:" + str(path),
            [[list(p), v] for p, v in leaves(changed)] != contract["authoredLeaves"],
        )
    for raw in (
        b'{"a":1,"a":2}',
        b'{"a":NaN}',
        b'{"a":Infinity}',
        b'{"a":-Infinity}',
        b"\xff",
    ):
        check("strict:" + repr(raw), rejected(lambda: strict(raw)))
    bad = deepcopy(schema)
    bad["unknownKeyword"] = True
    check(
        "unsupported-schema",
        rejected(lambda: validate_supported_schema_nodes(bad, "schema", bad)),
    )
    # Duplicate IDs are checked semantically with refreshed inventory, not only by shape.
    for group in (
        "approvedSources",
        "passages",
        "claims",
        "verifications",
        "humanDecisions",
        "audit",
        "contaminationSamples",
    ):
        changed, spec = deepcopy(data), deepcopy(contract)
        changed[group][1]["id"] = changed[group][0]["id"]
        spec["authoredLeaves"] = [[list(p), v] for p, v in leaves(changed)]
        check(
            "duplicate:" + group,
            bool(validate_model(changed, schema, spec, parent25, parent26)),
        )
    for path in DOCUMENTS:
        for label, text in {
            "preamble": "未レビューの前文。\n\n" + source[path],
            "tail": source[path] + "\n未レビューの末尾。\n",
            "heading": source[path].replace("\n## ", "\n## 未レビュー ", 1),
            "unsafe-before": "第三者の本番システムへ接続する。\n\n" + source[path],
            "unsafe-after": source[path] + "\n第三者の本番システムへ接続する。\n",
        }.items():
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
    for name, text, unsafe in (
        ("direct", "第三者の本番システムへ接続する。", True),
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
        check("canonical:" + doc.document_id, not document_errors(doc, spec, data))
        for i in range(len(doc.fields)):
            changed = replace(doc, fields=doc.fields[:i] + doc.fields[i + 1 :])
            check(
                "field:" + doc.document_id + ":" + str(i),
                digest(inventory(changed)) != spec["projectionSha256"],
            )
        for i, item in enumerate(spec["hostProvenance"]):
            field = next(
                f
                for f in doc.fields
                if [
                    f.field_type,
                    f.element_kind,
                    f.attribute,
                    f.metadata_value("level"),
                    f.text,
                    f.location,
                ]
                == item
            )
            changed = replace(
                field, text="https://github.com/", normalized_text="https://github.com/"
            )
            probe = replace(
                doc, fields=tuple(changed if f is field else f for f in doc.fields)
            )
            check(
                "provenance-non-expansion:" + doc.document_id + ":" + str(i),
                any("network.host_or_address" in e for e in scan_document(probe, spec)),
            )
    check(
        "Case-complete",
        not reading_table_errors(projection.document(DOCUMENTS[2]), data),
    )
    return len(checked), errors
