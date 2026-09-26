"""Finite Chapter22 model regressions; not a Markdown or policy grammar corpus."""

from copy import deepcopy

from scripts.chapter22_model import (
    VERSION,
    digest,
    measure,
    same,
    validate_model,
    validate_semantics,
    validate_dependencies,
)
from scripts.check_editorial_input_manifest import ManifestError


def at(value, path):
    for key in path:
        value = value[key]
    return value


def objects(value, path=()):
    if isinstance(value, dict):
        yield path, value
        for key, child in value.items():
            yield from objects(child, (*path, key))
    elif isinstance(value, list):
        for key, child in enumerate(value):
            yield from objects(child, (*path, key))


def run_model_regressions(data, schema, contract, corpus):
    checks, errors = set(), []

    def check(name, ok):
        if name in checks:
            errors.append("duplicate IMP22 probe: " + name)
        checks.add(name)
        if not ok:
            errors.append("failed IMP22 probe: " + name)

    def rejected(fn):
        try:
            result = fn()
            return isinstance(result, list) and bool(result)
        except (ValueError, KeyError, TypeError, ManifestError):
            return True

    def refreshed(changed):
        result = deepcopy(contract)
        result["authoredInputs"] = {k: digest(v) for k, v in changed.items()}
        return result

    check("harness-nonerror-dict", not rejected(lambda: {"accepted": True}))
    check("harness-nonerror-bytes", not rejected(lambda: b"accepted"))
    check("baseline-model", not validate_model(data, schema, contract))
    check("bool-is-not-one", rejected(lambda: same(True, 1, "typed equality")))
    check(
        "corpus-inventory",
        set(corpus) == {"schemaVersion", "comparisonVersion", "caseCount", "cases"}
        and corpus["schemaVersion"] == corpus["comparisonVersion"] == VERSION
        and type(corpus["caseCount"]) is int
        and corpus["caseCount"] == len(corpus["cases"]) == 42
        and [c["id"] for c in corpus["cases"]]
        == [f"IMPCHECK22-{n:03}" for n in range(1, 43)],
    )
    for case in corpus["cases"]:
        name = case["id"]
        check(
            name + "-owned",
            set(case) == {"id", "owner", "note", "input", "expected", "errorContains"}
            and case["owner"] == "LayerA Chapter22 supplied measurement"
            and isinstance(case["note"], str)
            and bool(case["note"].strip())
            and set(case["input"])
            == {"formula", "population", "selected", "samples", "missing"}
            and ((case["expected"] is None) != (case["errorContains"] is None)),
        )
        try:
            result = measure(**case["input"])
            check(
                name,
                case["errorContains"] is None
                and digest(result) == digest(case["expected"]),
            )
        except ValueError as exc:
            check(
                name,
                isinstance(case["errorContains"], str)
                and case["errorContains"] in str(exc),
            )

    # Closed-object schema failures still reject after an attacker refreshes the
    # data-only digest. No schema/contract regeneration is part of this check.
    for path, node in objects(data):
        name = "/".join(map(str, path)) or "root"
        changed = deepcopy(data)
        at(changed, path)["unreviewed"] = "extra"
        check(
            "unknown-field-" + name,
            rejected(lambda: validate_model(changed, schema, refreshed(changed))),
        )
        for key in node:
            changed = deepcopy(data)
            del at(changed, path)[key]
            check(
                "missing-field-" + name + "/" + key,
                rejected(lambda: validate_model(changed, schema, refreshed(changed))),
            )

    # Deliberately meaningful mutations. Each must fail semantics independent
    # of the snapshot checksum, not merely because its JSON bytes changed.
    mutations = [
        (("synthetic",), False),
        (("readOnly",), False),
        (("networkRequired",), True),
        (("executionAuthorized",), True),
        (("record", "actualOperations"), 1),
        (("record", "actualCollections"), 1),
        (("record", "actualNotifications"), 1),
        (("record", "actualDeployments"), 1),
        (("record", "actualIncidentDeclarations"), 1),
        (("record", "asOf"), "2026-10-02T00:00:00Z"),
        (("parentReferences", "parentReceiptId"), "RECEIVED-IMP22"),
        (("parentReferences", "parentHandoffStatus"), "delivered"),
        (("parentReferences", "parentEvidenceTransferred"), True),
        (("parentReferences", "parentStateChanged"), True),
        (("parentReferences", "authorityTransferred"), True),
        (("parentReferences", "beforeScenarioId"), "SCN-CV21-010"),
        (("parentReferences", "beforeEvidenceId"), "EVD-CV21-010-01"),
        (("authorityBoundary", "parentExpiresAt"), "2027-08-19T09:00:00Z"),
        (("authorityBoundary", "parentRoeStatus"), "Approved"),
        (("authorityBoundary", "parentExecutionAuthorized"), True),
        (("authorityBoundary", "parentLabRuntimeExecuted"), True),
        (("handoff", "receiptId"), "RECEIVED-26"),
        (("handoff", "executionAuthorized"), True),
        (("safety", "individualMonitoring"), True),
        (("safety", "publicRanking"), True),
        (("safety", "punitiveKpi"), True),
    ]
    for i in range(10):
        prefix = ("metrics", i)
        mutations += [
            (prefix + ("id",), "MET-IMP22-OTHER"),
            (prefix + ("definition",), "すべて同じ指標。"),
            (prefix + ("decisionPurpose",), "件数を増やす。"),
            (
                prefix + ("populationMembers",),
                ["OTHER-POPULATION-IMP22"],
            ),
            (
                prefix + ("populationMembers",),
                data["metrics"][i]["populationMembers"][:-1],
            ),
            (prefix + ("unit",), "seconds"),
            (prefix + ("current", "expectedResult"), {"count": 999}),
            (prefix + ("current", "availableAt"), "2026-09-01T09:11:01Z"),
            (prefix + ("current", "subjectRevision"), "INPUT-REV-001"),
            (prefix + ("current", "windowStart"), "2026-09-02T09:00:00Z"),
            (prefix + ("current", "dataSourceId"), "SYNDS-IMP22-OTHER"),
            (
                prefix + ("current", "evidenceId"),
                data["metrics"][i]["baseline"]["evidenceId"],
            ),
        ]
    for i in range(8):
        prefix = ("items", i)
        other = data["items"][(i + 1) % 8]
        mutations += [
            (prefix + ("status",), "Implemented"),
            (prefix + ("metricIds",), other["metricIds"]),
            (prefix + ("dependencyIds",), [data["items"][i]["id"]]),
            (prefix + ("priority", "reason"), other["priority"]["reason"]),
            (prefix + ("priority", "automaticScore"), True),
            (prefix + ("action", "proposal"), other["action"]["proposal"]),
            (prefix + ("action", "acceptance"), other["action"]["acceptance"]),
            (prefix + ("action", "executionAuthorized"), True),
            (prefix + ("action", "actualExecuted"), True),
            (prefix + ("action", "owner"), other["action"]["owner"]),
            (prefix + ("evidenceIds",), other["evidenceIds"]),
            (prefix + ("verification", "itemId"), other["id"]),
            (prefix + ("verification", "subjectRevision"), "INPUT-REV-001"),
            (prefix + ("verification", "realEffectivenessVerified"), True),
            (prefix + ("decision", "executionAuthorized"), True),
            (prefix + ("riskJudgment", "realRiskReductionMeasured"), True),
            (prefix + ("riskJudgment", "riskZero"), True),
            (prefix + ("reassessment", "owner"), other["reassessment"]["owner"]),
            (prefix + ("acceptance", "overridesExecutionAuthority"), True),
            (prefix + ("retirement", "historyRetained"), False),
            (prefix + ("workRecord", "actualOperation"), True),
        ]
    mutations += [
        (("items", 3, "verification", "id"), None),
        (("items", 3, "verification", "evidenceId"), "EVD-IMP22-V005"),
        (
            ("items", 3, "verification", "sourceEvidenceIds"),
            data["items"][4]["evidenceIds"],
        ),
        (("items", 4, "verification", "recordedAt"), "2026-09-01T09:00:00Z"),
        (("items", 4, "verification", "recordedAt"), "2026-10-01T00:00:00Z"),
        (("items", 5, "status"), "Verified"),
        (("items", 6, "status"), "Verified"),
        (("items", 6, "acceptance", "expiresAt"), "2026-09-25T00:00:00Z"),
        (("items", 6, "acceptance", "scope"), "本番Riskと実操作を無期限に受容する。"),
        (("items", 6, "reassessment", "dueAt"), "2026-10-02T00:00:00Z"),
        (("items", 7, "retirement", "replacementMetricIds"), []),
        (("metrics", 8, "current", "missingMembers"), []),
        (
            ("metrics", 5, "current", "selectedMembers"),
            data["metrics"][5]["populationMembers"],
        ),
        (
            ("metrics", 3, "current", "selectedMembers"),
            data["metrics"][2]["current"]["selectedMembers"],
        ),
    ]
    for i, (path, value) in enumerate(mutations):
        changed = deepcopy(data)
        at(changed, path[:-1])[path[-1]] = deepcopy(value)
        check(
            f"semantic-{i:03}-" + "/".join(map(str, path)),
            rejected(lambda: validate_semantics(changed)),
        )
        check(
            f"refreshed-digest-{i:03}",
            rejected(lambda: validate_model(changed, schema, refreshed(changed))),
        )

    cycle = deepcopy(data["items"])
    cycle[0]["dependencyIds"] = [cycle[1]["id"]]
    check("dependency-two-item-cycle", rejected(lambda: validate_dependencies(cycle)))
    unknown = deepcopy(data["items"])
    unknown[0]["dependencyIds"] = ["BLI-IMP22-999"]
    check("dependency-unknown", rejected(lambda: validate_dependencies(unknown)))
    check(
        "dependency-baseline",
        not rejected(lambda: validate_dependencies(data["items"])),
    )
    # Scan fields not restricted to one exact authored sentence: these probes
    # prove shared Policy is reached after a deliberately refreshed digest.
    for path in (
        ("safety", "purpose"),
        ("handoff", "purpose"),
        ("items", 0, "priority", "cost"),
        ("items", 0, "residualRisk", "description"),
    ):
        for text in ("実環境でスキャンを実施する。", "https://example.com/collect"):
            changed = deepcopy(data)
            at(changed, path[:-1])[path[-1]] = text
            check(
                "policy-" + "/".join(map(str, path)) + "-" + text,
                bool(validate_model(changed, schema, refreshed(changed))),
            )
    for value in ("", " " * 4, "a" * 2001):
        changed = deepcopy(data)
        changed["safety"]["purpose"] = value
        check(
            "bounded-string-" + str(len(value)),
            rejected(lambda: validate_model(changed, schema, refreshed(changed))),
        )
    changed_schema = deepcopy(schema)
    changed_schema["unsupported-IMP22-keyword"] = True
    check(
        "unsupported-schema-keyword",
        rejected(lambda: validate_model(data, changed_schema, contract)),
    )
    return errors, len(checks)


def run_regressions(data, schema, contract, source, projection):
    from dataclasses import replace
    import json
    import os
    from pathlib import Path
    import tempfile
    from unittest.mock import patch
    from scripts.chapter22_model import DATA, CORPUS, DOCUMENTS, strict, read_regular
    from scripts.check_chapter22_contract import (
        ROOT,
        identity,
        inventory,
        document_errors,
        scan_document,
        reading_table_errors,
        repository_errors,
        parent_errors,
    )
    from scripts.publication_projection import project_documents, is_policy_scan_field

    errors, model_count = run_model_regressions(
        data, schema, contract, strict(read_regular(ROOT, CORPUS))
    )
    checks = set()

    def check(name, ok):
        if name in checks:
            errors.append("duplicate IMP22 publication probe: " + name)
        checks.add(name)
        if not ok:
            errors.append("failed IMP22 publication probe: " + name)

    def rejected(fn):
        try:
            value = fn()
            return isinstance(value, list) and bool(value)
        except (OSError, ValueError, KeyError, TypeError, ManifestError):
            return True

    parent = strict(read_regular(ROOT, "cases/fixtures/ch21-control-validation.json"))
    check("parent-positive", not parent_errors(data, parent))
    for path, value in (
        (("handoff", "receiptId"), "RECEIVED"),
        (("handoff", "status"), "delivered"),
        (("handoff", "executionAuthorized"), True),
        (("authorityBoundary", "parentRoeStatus"), "Approved"),
        (("retest", "beforeRetained"), False),
        (("retest", "actualChangeExecuted"), True),
        (("scenarios", 2, "expectedLayers", 0, "result"), "Passed"),
        (("scenarios", 9, "batchId"), "BATCH-OTHER"),
        (("scenarios", 9, "observations", 0, "payload", "values", "negative"), "alert"),
        (("scenarios", 9, "improvement", "status"), "completed"),
    ):
        changed = deepcopy(parent)
        at(changed, path[:-1])[path[-1]] = value
        check("parent-boundary-" + str(path), bool(parent_errors(data, changed)))
    for text in (b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}', b"\xff"):
        check("strict-json-" + repr(text), rejected(lambda: strict(text)))
    # Even an unsupported node in a non-selected union arm is a schema error.
    changed = deepcopy(schema)
    branch = next(node for _, node in objects(changed) if "oneOf" in node)
    branch["oneOf"][-1]["unsupported-in-unselected-arm"] = True
    check(
        "unused-schema-arm-fail-closed",
        rejected(lambda: validate_model(data, changed, contract)),
    )
    # Required root publication preflight exactly once, before output deletion.
    package = strict(read_regular(ROOT, "package.json"))
    command = "python3 scripts/check_chapter22_contract.py --no-regressions && "
    for label, value in (
        ("missing", package["scripts"]["sync:docs"].replace(command, "")),
        ("duplicate", command + package["scripts"]["sync:docs"]),
    ):
        changed = deepcopy(package)
        changed["scripts"]["sync:docs"] = value

        def reader(root, path):
            return (
                json.dumps(changed).encode()
                if path == "package.json"
                else read_regular(root, path)
            )

        with patch("scripts.check_chapter22_contract.read_regular", side_effect=reader):
            check("root-preflight-" + label, bool(repository_errors(data, contract)))

    rendered, owners = {}, {}
    for path in DOCUMENTS:
        for label, text in (
            ("preamble", "未レビューの前文。\n\n" + source[path]),
            ("tail", source[path] + "\n未レビューの末尾。\n"),
            ("heading", source[path].replace("\n## ", "\n## 未レビュー ", 1)),
            ("unsafe-before", "第三者の本番システムへ接続する。\n\n" + source[path]),
            (
                "unsafe-body",
                source[path].replace(
                    "\n## ", "\n第三者の本番システムへ接続する。\n\n## ", 1
                ),
            ),
            ("unsafe-after", source[path] + "\n第三者の本番システムへ接続する。\n"),
        ):
            key = path + "#" + label
            rendered[key], owners[key] = text, path
    # Six full copies of the all-leaf Case exceed the shared field budget.
    # Keep each renderer call bounded; never weaken the shared fail-closed cap.
    keys = list(rendered)
    projected = []
    for offset in range(0, len(keys), 2):
        batch = {key: rendered[key] for key in keys[offset : offset + 2]}
        projected.extend(project_documents(batch).documents)
    for doc in projected:
        path = owners[doc.document_id]
        check(
            "selection-" + doc.document_id,
            bool(
                document_errors(
                    replace(doc, document_id=path), contract["documents"][path], data
                )
            ),
        )
        if "#unsafe-" in doc.document_id:
            check(
                "shared-action-" + doc.document_id,
                any(
                    "target.real_or_external" in e
                    for e in scan_document(doc, {"hostProvenance": []})
                ),
            )
    counterparts = project_documents(
        {
            "prohibition": "第三者の本番システムへ接続しない。",
            "risk": "analyze the risk of collecting PII",
        }
    )
    for doc in counterparts.documents:
        check(
            "safe-counterpart-" + doc.document_id,
            not scan_document(doc, {"hostProvenance": []}),
        )
    for doc in projection.documents:
        spec = contract["documents"][doc.document_id]
        check(
            "canonical-false-positive-zero-" + doc.document_id,
            not scan_document(doc, spec),
        )
        for f in doc.fields:
            if identity(f) in spec["hostProvenance"]:
                key = f.location
                duplicate = replace(doc, fields=(*doc.fields, f))
                check("provenance-once-" + key, bool(scan_document(duplicate, spec)))
                changed = replace(
                    f,
                    text=f.text + " unreviewed",
                    normalized_text=f.normalized_text + " unreviewed",
                )
                altered = replace(
                    doc, fields=tuple(changed if x is f else x for x in doc.fields)
                )
                check("provenance-exact-" + key, bool(scan_document(altered, spec)))
                # Same exact allowed host field, but malicious projected action.
                # This proves the adapter never skips Layer C action scanning.
                changed = replace(f, normalized_text="第三者の本番システムへ接続する。")
                altered = replace(
                    doc, fields=tuple(changed if x is f else x for x in doc.fields)
                )
                if is_policy_scan_field(f):
                    check(
                        "provenance-action-always-" + key,
                        any(
                            "target.real_or_external" in e
                            for e in scan_document(altered, spec)
                        ),
                    )
    for doc in projection.documents:
        if doc.document_id not in (DOCUMENTS[0], DOCUMENTS[2]):
            continue
        target = next(
            f
            for f in doc.fields
            if f.element_kind == "table_row"
            and (
                "4→8" in f.text
                if doc.document_id == DOCUMENTS[0]
                else "SIB-2026-022-001" in f.text
            )
        )
        changed = replace(
            target,
            text=target.text + " unreviewed",
            normalized_text=target.normalized_text + " unreviewed",
        )
        altered = replace(
            doc, fields=tuple(changed if f is target else f for f in doc.fields)
        )
        spec = deepcopy(contract["documents"][doc.document_id])
        spec["projectionSha256"] = digest(inventory(altered))
        check(
            "table-not-waived-by-projection-refresh-" + doc.document_id,
            bool(reading_table_errors(altered, data)),
        )

    work = ROOT / ".work"
    work.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="chapter22-contract-", dir=work) as name:
        root = Path(name)
        path = root / DATA
        path.parent.mkdir(parents=True)
        path.write_bytes(b"{}")
        check("bounded-regular-positive", read_regular(root, DATA) == b"{}")
        check("unowned-path", rejected(lambda: read_regular(root, "unowned.json")))
        path.write_bytes(b"")
        check("empty-input", rejected(lambda: read_regular(root, DATA)))
        path.write_bytes(b"x" * (1024 * 1024 + 1))
        check("oversize-input", rejected(lambda: read_regular(root, DATA)))
        path.unlink()
        path.mkdir()
        check("directory-input", rejected(lambda: read_regular(root, DATA)))
        path.rmdir()
        os.mkfifo(path)
        check("fifo-nonblocking", rejected(lambda: read_regular(root, DATA)))
        path.unlink()
        target = root / "target.json"
        target.write_bytes(b"{}")
        path.symlink_to(target)
        check("symlink-input", rejected(lambda: read_regular(root, DATA)))
        path.unlink()
        path.parent.rmdir()
        path.parent.symlink_to(root, target_is_directory=True)
        check("symlink-ancestor", rejected(lambda: read_regular(root, DATA)))
        path.parent.unlink()
        link = root / "root-link"
        link.symlink_to(root, target_is_directory=True)
        check("symlink-root", rejected(lambda: read_regular(link, DATA)))
    return model_count + len(checks), errors
