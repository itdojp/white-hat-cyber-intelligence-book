"""Bounded Chapter21 semantics, ownership and full-publication selection probes."""

from copy import deepcopy
from dataclasses import replace
import json
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

from scripts.chapter21_model import (
    VERSION,
    DATA,
    CORPUS,
    DOCUMENTS,
    strict,
    read_regular,
    validate_model,
    digest,
    evaluate,
    summary,
    leaves,
)
from scripts.check_chapter21_contract import (
    ROOT,
    identity,
    inventory,
    document_errors,
    scan_document,
    reading_table_errors,
    repository_errors,
)
from scripts.check_editorial_input_manifest import (
    ManifestError,
    validate_schema_instance,
)
from scripts.publication_projection import project_documents, is_policy_scan_field


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


def run_regressions(data, schema, contract, source, projection):
    checks, errors = set(), []

    def check(name, ok):
        if name in checks:
            errors.append("duplicate CV21 probe: " + name)
        checks.add(name)
        if not ok:
            errors.append("failed CV21 probe: " + name)

    def rejected(fn):
        try:
            value = fn()
            return isinstance(value, list) and bool(value)
        except (ValueError, KeyError, TypeError, StopIteration, OSError, ManifestError):
            return True

    def refreshed(changed):
        for s in changed["scenarios"]:
            for observation in s["observations"]:
                observation["payloadSha256"] = digest(observation["payload"])
        c = deepcopy(contract)
        c["authoredInputs"] = {k: digest(v) for k, v in changed.items()}
        return c

    check("harness-nonerror-bytes", not rejected(lambda: b"accepted"))
    check("harness-nonerror-dict", not rejected(lambda: {"accepted": True}))
    check("baseline-model", not validate_model(data, schema, contract))
    corpus = strict(read_regular(ROOT, CORPUS))
    check(
        "corpus-inventory",
        corpus["comparisonVersion"] == VERSION
        and corpus["caseCount"] == len(corpus["cases"]) == 59
        and [c["id"] for c in corpus["cases"]]
        == [f"CVCHECK21-{n:03}" for n in range(1, 60)]
        and all(
            c["owner"] == "LayerA Chapter21 supplied comparison" and c["note"]
            for c in corpus["cases"]
        ),
    )
    for case in corpus["cases"]:
        try:
            actual = evaluate(case["input"])
            ok = case["errorContains"] is None and actual == case["expected"]
        except (ValueError, KeyError, TypeError) as exc:
            ok = case["errorContains"] is not None and case["errorContains"] in str(exc)
        check(case["id"], ok)
    # Every object is closed and every authored field required at publication.
    for path, obj in objects(data):
        changed = deepcopy(data)
        at(changed, path)["unownedField"] = "synthetic-extra"
        check(
            "closed-" + str(path),
            rejected(lambda: validate_schema_instance(changed, schema)),
        )
        for key in obj:
            changed = deepcopy(data)
            del at(changed, path)[key]
            check(
                "required-" + str((*path, key)),
                rejected(lambda: validate_schema_instance(changed, schema)),
            )
    for path, value in leaves(data):
        if isinstance(value, bool):
            changed = deepcopy(data)
            # Schema type and semantic checks must distinguish bool from integer.
            typed_path = tuple(int(k) if k.isdigit() else k for k in path)
            at(changed, typed_path[:-1])[typed_path[-1]] = int(value)
            check(
                "strict-bool-" + str(path),
                rejected(lambda: validate_model(changed, schema, refreshed(changed))),
            )
    for raw in (
        b'{"a":1,"a":2}',
        b'{"x":{"a":1,"a":2}}',
        b'{"x":NaN}',
        b'{"x":Infinity}',
        b'{"x":-Infinity}',
        b"\xff",
    ):
        check("strict-json-" + repr(raw), rejected(lambda: strict(raw)))
    bad_schema = deepcopy(schema)
    bad_schema["maxLength"] = 10
    check(
        "unsupported-schema-keyword",
        rejected(lambda: validate_schema_instance(data, bad_schema)),
    )

    mutations = [
        (["schemaVersion"], "2.0.0"),
        (["record", "asOf"], "2026-08-01T00:00:00Z"),
        (["record", "parentCaseId"], "CASE-IR-2026-001"),
        (["record", "relation"], "independent"),
        (["record", "artifactId"], "ART-26"),
        (["record", "sourceIds"], ["SRC-UNREVIEWED"]),
        (["record", "authoring"], "measured"),
        (["executionAuthorized"], True),
        (["networkRequired"], True),
        (["synthetic"], False),
        (["readOnly"], False),
        (["roles", "evidenceReviewer"], data["roles"]["validationOwner"]),
        (["authorityBoundary", "parentExpiresAt"], "2027-08-19T09:00:00Z"),
        (["authorityBoundary", "parentRoeStatus"], "Approved"),
        (["authorityBoundary", "parentRoeVersion"], True),
        (["authorityBoundary", "parentLabRuntimeExecuted"], True),
        (["authorityBoundary", "parentExecutionAuthorized"], True),
        (["threat", "coverageProof"], True),
        (["threat", "attackVersion"], "19.1"),
        (["threat", "attackTechniqueId"], "T9999"),
        (["threat", "actorAttribution"], "confirmed"),
        (["retest", "beforeRetained"], False),
        (["retest", "actualChangeExecuted"], True),
        (["retest", "beforeScenarioId"], "SCN-CV21-006"),
        (["retest", "afterScenarioId"], "SCN-CV21-008"),
        (["retest", "changedField"], "objective"),
        (["retest", "sourceActionId"], "ACT-CV21-001"),
        (["handoff", "status"], "delivered"),
        (["handoff", "receiptId"], "SYN-RECEIVED"),
        (["handoff", "executionAuthorized"], True),
        (["handoff", "targetChapter"], 25),
        (["handoff", "actionIds"], []),
        (["handoff", "owner"], "SYN-OTHER"),
        (["handoff", "dueAt"], "2026-09-24T00:00:00Z"),
        (["safety", "cleanupDisposition"], "actual-cleanup-complete"),
        (["safety", "residualDisposition"], "verified-clear"),
    ]
    for key in (
        "actualOperations",
        "actualCollections",
        "actualNotifications",
        "actualDeployments",
        "actualIncidentDeclarations",
    ):
        mutations.extend([(["record", key], 1), (["record", key], False)])
    for i in range(5):
        mutations += [
            (["controls", i, "objectiveId"], "OBJ-FOREIGN"),
            (["controls", i, "criteria", 0, "expected"], "always-passed"),
            (["controls", i, "criteria", 0, "partialValues"], [None]),
        ]
    for i in range(10):
        mutations += [
            (["scenarios", i, "subjectId"], "SYNTH-FOREIGN"),
            (["scenarios", i, "traceId"], "TRACE-FOREIGN"),
            (["scenarios", i, "id"], "SCN-FOREIGN"),
            (["scenarios", i, "cutoff"], "2026-09-01T09:11:01Z"),
            (["scenarios", i, "expectedLayers", 0, "result"], "Not tested"),
            (["scenarios", i, "gap", "nextActionId"], "ACT-FOREIGN"),
            (["scenarios", i, "gap", "id"], "GAP-FOREIGN"),
            (["scenarios", i, "improvement", "owner"], "SYN-OTHER"),
            (["scenarios", i, "improvement", "status"], "completed"),
            (["scenarios", i, "improvement", "dueAt"], "2026-09-24T00:00:00Z"),
            (["scenarios", i, "improvement", "retestId"], "RT-FOREIGN"),
            (["scenarios", i, "improvement", "reassessmentId"], "REA-FOREIGN"),
        ]
    for path, value in mutations:
        changed = deepcopy(data)
        at(changed, path[:-1])[path[-1]] = value
        c = refreshed(changed)
        check(
            "semantic-refreshed-" + str(path) + repr(value),
            rejected(lambda: validate_model(changed, schema, c)),
        )
    # Recomputing both expected values and representation digests is not
    # editorial approval to remove a counterexample or swap its teaching role.
    for i, field, value in (
        (2, "positive", "alert"),
        (2, "negative", "alert"),
        (5, "positive", "no-alert"),
        (9, "benign-near-miss", "alert"),
    ):
        changed = deepcopy(data)
        p = changed["scenarios"][i]["observations"][0]["payload"]
        p["values"][field] = value
        p["present"][field] = True
        p["inputBasis"] = "complete-supplied-input"
        c = refreshed(changed)
        for s in changed["scenarios"]:
            s["expectedLayers"] = summary(s)
        c = refreshed(changed)
        check(
            "outcome-and-digest-refresh-" + str((i, field)),
            rejected(lambda: validate_model(changed, schema, c)),
        )
    for key in data["parentReferences"]:
        changed = deepcopy(data)
        changed["parentReferences"][key] = "foreign-parent-binding"
        check("exact-parent-" + key, bool(repository_errors(changed, contract)))

    for path in (
        ["safety", "limitations"],
        ["authorityBoundary", "scope"],
        ["threat", "behavior"],
        ["controls", 0, "objective"],
        ["scenarios", 0, "note"],
        ["scenarios", 0, "gap", "description"],
        ["scenarios", 0, "improvement", "action"],
        ["scenarios", 0, "permittedConclusion"],
        ["retest", "limitation"],
        ["handoff", "question"],
    ):
        changed = deepcopy(data)
        at(changed, path[:-1])[path[-1]] = "第三者の本番システムへ接続する。"
        c = refreshed(changed)
        check(
            "json-shared-scanner-" + str(path),
            any(
                "target.real_or_external" in e
                for e in validate_model(changed, schema, c)
            ),
        )
    # Required root publication preflight exactly once, before output deletion.
    package = strict(read_regular(ROOT, "package.json"))
    command = "python3 scripts/check_chapter21_contract.py --no-regressions && "
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

        with patch("scripts.check_chapter21_contract.read_regular", side_effect=reader):
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
    for doc in project_documents(rendered).documents:
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
            and f.text.startswith("Scenario")
            and "Passed" in f.text
        )
        changed = replace(
            target,
            text=target.text.replace("Passed", "Failed"),
            normalized_text=target.normalized_text.replace("Passed", "Failed"),
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
    with tempfile.TemporaryDirectory(prefix="chapter21-contract-", dir=work) as name:
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
    return len(checks), errors
