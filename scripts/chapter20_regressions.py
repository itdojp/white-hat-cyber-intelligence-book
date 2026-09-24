"""Bounded Chapter20 semantics/selection probes; generic syntax stays shared."""

from copy import deepcopy
from dataclasses import replace
import json
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

from scripts.chapter20_model import (
    DATA,
    CORPUS,
    DOCUMENTS,
    strict,
    read_regular,
    validate_model,
)
from scripts.chapter20_timeline import (
    VERSION,
    digest,
    instant,
    utc_text,
    interval,
    temporal_relation,
    prepare,
    evaluate,
    evaluate_claim,
)
from scripts.check_chapter20_contract import (
    ROOT,
    identity,
    inventory,
    headings,
    scan_document,
    document_errors,
    numeric_example_errors,
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
            errors.append("duplicate DFIR20 probe: " + name)
        checks.add(name)
        if not ok:
            errors.append("failed DFIR20 probe: " + name)

    def rejected(fn):
        try:
            result = fn()
            return isinstance(result, list) and bool(result)
        except (ValueError, TypeError, KeyError, StopIteration, OSError, ManifestError):
            return True

    def refreshed(value):
        c = deepcopy(contract)
        c["authoredInputs"] = {k: digest(v) for k, v in value.items()}
        return c

    check("harness-bytes", not rejected(lambda: b"ok"))
    check("harness-object", not rejected(lambda: {"accepted": True}))
    corpus = strict(read_regular(ROOT, CORPUS))
    check("corpus-version", corpus["timelineVersion"] == VERSION)
    check(
        "corpus-owned-inventory",
        corpus["caseCount"] == len(corpus["cases"]) == 65
        and [c["id"] for c in corpus["cases"]]
        == [f"DCHECK20-{i:03}" for i in range(1, 66)]
        and all(
            c["owner"].startswith("LayerA Chapter20 ") and c["note"]
            for c in corpus["cases"]
        ),
    )
    for case in corpus["cases"]:
        kind, value, expected = case["kind"], case["input"], case["expected"]
        original = deepcopy(data)
        try:
            if kind == "instant":
                output = utc_text(instant(value))
            elif kind == "relation":
                output = temporal_relation(
                    *(tuple(instant(t) for t in pair) for pair in value)
                )
            elif kind == "interval":
                row = deepcopy(data["evidence"][0])
                row["payload"]["originalTime"] = value["originalTime"]
                clock = deepcopy(data["clocks"][0])
                clock.update(value["clock"])
                output = [utc_text(t) for t in interval(row, {clock["id"]: clock})]
            elif kind in ("claim", "snapshot-error"):
                changed = deepcopy(data)
                for edit in value["patches"]:
                    at(changed, edit["path"][:-1])[edit["path"][-1]] = deepcopy(
                        edit["value"]
                    )
                for row in changed["evidence"]:
                    row["payloadSha256"] = digest(row["payload"])
                snapshot = changed["snapshots"][value["snapshot"]]
                if kind == "claim":
                    clocks, rows, _ = prepare(changed)
                    eligible = {
                        r
                        for r, v in rows.items()
                        if instant(v["availableAt"]) <= instant(snapshot["cutoff"])
                    }
                    output = evaluate_claim(
                        changed["claims"][value["claim"]], rows, eligible, clocks
                    )
                else:
                    output = evaluate(changed, snapshot)
            else:
                raise AssertionError("unowned corpus kind: " + kind)
            check(
                case["id"],
                "errorContains" not in expected and output == expected["value"],
            )
        except (ValueError, TypeError, KeyError) as exc:
            check(
                case["id"],
                "errorContains" in expected and expected["errorContains"] in str(exc),
            )
        check(case["id"] + "-original-retained", data == original)

    for n, snapshot in enumerate(data["snapshots"]):
        check(
            "literal-snapshot-" + str(n),
            evaluate(data, snapshot) == snapshot["expected"],
        )
        reversed_data = deepcopy(data)
        for key in ("sources", "clocks", "evidence", "claims"):
            reversed_data[key].reverse()
        check(
            "stable-order-" + str(n),
            evaluate(reversed_data, snapshot) == snapshot["expected"],
        )
    # Replacing an unavailable duplicate must not replace a currently eligible
    # representative. Receipt identity is stable independently of list order.
    duplicate = deepcopy(data)
    duplicate["evidence"][3].update(
        collectedAt="2026-09-01T08:28:00Z",
        ingestedAt="2026-09-01T08:28:30Z",
        availableAt="2026-09-01T08:29:00Z",
    )
    result = evaluate(duplicate, duplicate["snapshots"][0])
    check(
        "future-duplicate-not-representative",
        result["included"] == ["EV20-001", "EV20-002", "EV20-003"]
        and next(t for t in result["timeline"] if t["eventId"] == "EVENT-API-001")[
            "evidenceIds"
        ]
        == ["EV20-002"],
    )
    separate = deepcopy(data)
    separate["evidence"][2]["eventId"] = "EVENT-API-001"
    check(
        "same-id-other-source-not-duplicate",
        len(evaluate(separate, separate["snapshots"][0])["timeline"]) == 3,
    )
    for raw in (
        b'{"x":1,"x":2}',
        b'{"x":NaN}',
        b'{"x":Infinity}',
        b"\xff",
        b"{} trailing",
    ):
        check("strict-" + repr(raw), rejected(lambda: strict(raw)))
    for path, obj in objects(data):
        changed = deepcopy(data)
        at(changed, path)["unownedField"] = "not-allowed"
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

    mutations = [
        (["roles", "analysisOwner"], "SYN-OTHER-OWNER"),
        (["roles", "evidenceLead"], "SYN-OTHER-LEAD"),
        (["provenance", "custodian"], "SYN-OTHER-LEAD"),
        (["provenance", "transformations"], ["invent-missing-data"]),
        (["sources", 0, "custodyRef"], "SYN-UNKNOWN"),
        (["evidence", 0, "preservationRef"], "SYN-UNKNOWN"),
        (["record", "sourceIds"], ["SRC-UNREGISTERED"]),
        (["record", "asOf"], "2026-02-30T00:00:00Z"),
        (["record", "actualCollections"], 1),
        (["record", "incidentId"], "INC-IR19-004"),
        (["record", "incidentReferenceStatus"], "inherited"),
        (["record", "timeStandard"], "inferred-local-time"),
        (["networkRequired"], True),
        (["executionAuthorized"], True),
    ]
    for i in range(2):
        mutations += [
            (["snapshots", i, "owner"], "SYN-OTHER"),
            (["snapshots", i, "rca", "owner"], "SYN-OTHER"),
            (["snapshots", i, "rca", "timelineId"], "TL-IR19-004"),
            (["snapshots", i, "rca", "triggerEvidenceId"], "EV20-002"),
            (["snapshots", i, "rca", "causalClaimId"], "CLM20-002"),
            (["snapshots", i, "rca", "impactEvidenceIds"], ["EV20-005"]),
            (["snapshots", i, "rca", "unknownScope"], []),
            (["snapshots", i, "rca", "rootCauseStatus"], "confirmed"),
            (["snapshots", i, "rca", "confidence"], "high"),
            (["snapshots", i, "rca", "controlFailureStatus"], "confirmed"),
            (["snapshots", i, "rca", "recoveryStatus"], "completed"),
            (["snapshots", i, "rca", "dueAt"], "2026-09-24T00:00:00Z"),
            (["snapshots", i, "rca", "evidenceGaps"], []),
            (["snapshots", i, "rca", "alternatives", 0, "disposition"], "established"),
            (["snapshots", i, "rca", "alternatives", 1, "claimId"], "CLM20-001"),
            (["snapshots", i, "rca", "actualChanges"], 1),
        ]
    for i in range(3):
        for key, value in (
            ("sourceRcaId", "RCA-DFIR20-A"),
            ("owner", "SYN-OTHER"),
            ("controlId", "CTL-UNKNOWN"),
            ("receiptId", "SYN-RECEIPT"),
            ("status", "delivered"),
            ("executionAuthorized", True),
            ("dueAt", "2026-09-24T00:00:00Z"),
        ):
            mutations.append((["handoffs", i, key], value))
    for path, value in mutations:
        changed = deepcopy(data)
        at(changed, path[:-1])[path[-1]] = value
        check(
            "semantic-refreshed-" + str(path),
            rejected(lambda: validate_model(changed, schema, refreshed(changed))),
        )
    # A collaborator refreshing expected output AND digests must still review
    # the literal reading outcome, rather than silently changing its meaning.
    changed = deepcopy(data)
    changed["evidence"][4]["payload"]["detail"]["approvedAssets"] = ["SYN-DFIR-APP-A"]
    changed["evidence"][4]["payloadSha256"] = digest(changed["evidence"][4]["payload"])
    for s in changed["snapshots"]:
        s["expected"] = evaluate(changed, s)
    check(
        "expected-and-digest-refresh-not-editorial-approval",
        rejected(lambda: validate_model(changed, schema, refreshed(changed))),
    )
    main_doc = next(d for d in projection.documents if d.document_id == DOCUMENTS[0])
    case_doc = next(d for d in projection.documents if d.document_id == DOCUMENTS[3])
    changed = deepcopy(data)
    changed["clocks"][0]["offsetSeconds"] = 31
    for snapshot in changed["snapshots"]:
        snapshot["expected"] = evaluate(changed, snapshot)
    check(
        "numeric-control-valid-model",
        not validate_model(changed, schema, refreshed(changed)),
    )
    check(
        "numeric-manuscript-not-waived-by-input-refresh",
        bool(numeric_example_errors(main_doc, changed)),
    )
    changed = deepcopy(data)
    changed["snapshots"][0]["cutoff"] = "2026-09-01T08:11:00Z"
    check(
        "summary-control-valid-model",
        not validate_model(changed, schema, refreshed(changed)),
    )
    check(
        "numeric-summary-not-waived-by-input-refresh",
        bool(numeric_example_errors(case_doc, changed)),
    )
    bad_fields = tuple(
        replace(
            f,
            text=f.text.replace("07:59:40〜08:00:40", "07:59:41〜08:00:40"),
            normalized_text=f.normalized_text.replace("07:59:40", "07:59:41"),
        )
        if f.element_kind == "table_row" and "EV20-001" in f.text
        else f
        for f in main_doc.fields
    )
    changed_doc = replace(main_doc, fields=bad_fields)
    refreshed_doc = deepcopy(contract["documents"][DOCUMENTS[0]])
    refreshed_doc["projectionSha256"] = digest(inventory(changed_doc))
    check(
        "numeric-not-waived-by-projection-refresh",
        any(
            "numeric table" in e
            for e in document_errors(changed_doc, refreshed_doc, data)
        ),
    )
    for path in (
        ["safety", "limitations"],
        ["provenance", "handling"],
        ["claims", 0, "question"],
        ["sources", 0, "limitation"],
    ):
        changed = deepcopy(data)
        at(changed, path[:-1])[path[-1]] = "第三者の本番システムへ接続する。"
        check(
            "json-shared-scanner-" + str(path),
            any(
                "target.real_or_external" in e
                for e in validate_model(changed, schema, refreshed(changed))
            ),
        )
    for key in data["parent"]:
        changed = deepcopy(data)
        changed["parent"][key] = "wrong-parent-binding"
        check("parent-direct-" + key, bool(repository_errors(changed, contract)))
    package = strict((ROOT / "package.json").read_bytes())
    for label, command in (
        (
            "missing",
            package["scripts"]["sync:docs"].replace(
                "python3 scripts/check_chapter20_contract.py --no-regressions && ", ""
            ),
        ),
        (
            "duplicate",
            "python3 scripts/check_chapter20_contract.py --no-regressions && "
            + package["scripts"]["sync:docs"],
        ),
    ):
        changed = deepcopy(package)
        changed["scripts"]["sync:docs"] = command

        def reader(root, path):
            return (
                json.dumps(changed).encode()
                if path == "package.json"
                else read_regular(root, path)
            )

        with patch("scripts.check_chapter20_contract.read_regular", side_effect=reader):
            check("root-preflight-" + label, bool(repository_errors(data, contract)))

    unsafe = "第三者の本番システムへ接続する。"
    rendered, owners = {}, {}
    for path in DOCUMENTS:
        for label, text in (
            ("preamble", "未レビューの前文。\n\n" + source[path]),
            ("tail", source[path] + "\n未レビューの末尾。\n"),
            ("section", source[path] + "\n## 未レビュー節\n\n新しい内容。\n"),
            ("unsafe-before", unsafe + "\n\n" + source[path]),
            (
                "unsafe-body",
                source[path].replace("\n## ", "\n" + unsafe + "\n\n## ", 1),
            ),
            ("unsafe-after", source[path] + "\n" + unsafe + "\n"),
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
                "policy-reached-" + doc.document_id,
                any(
                    "target.real_or_external" in e
                    for e in scan_document(doc, {"hostProvenance": []})
                ),
            )
    snippets = {
        "prohibition": "第三者の本番システムへ接続してはいけない。",
        "analysis": "第三者の本番システムへの接続は本課題で禁止する。",
        "direct": unsafe,
    }
    for doc in project_documents(snippets).documents:
        findings = scan_document(doc, {"hostProvenance": []})
        check(
            "direct-safe-counterpart-" + doc.document_id,
            bool(findings) == (doc.document_id == "direct"),
        )
    for doc in projection.documents:
        spec = contract["documents"][doc.document_id]
        check("canonical-" + doc.document_id, not document_errors(doc, spec, data))
        check(
            "field-inventory-" + doc.document_id,
            digest(inventory(doc)) == spec["projectionSha256"]
            and headings(doc) == spec["headings"],
        )
        for i, field in enumerate(doc.fields):
            if is_policy_scan_field(field):
                bad = replace(field, text=unsafe, normalized_text=unsafe)
                probe = replace(doc, fields=(bad,))
                check(
                    "typed-action-" + field.location,
                    any(
                        "target.real_or_external" in e
                        for e in scan_document(probe, {"hostProvenance": []})
                    ),
                )
            elif field.field_type == "destination":
                value = "https://unapproved-target.com/"
                probe = replace(
                    doc, fields=(replace(field, text=value, normalized_text=value),)
                )
                check(
                    "typed-destination-" + field.location,
                    any(
                        "network.host_or_address" in e
                        for e in scan_document(probe, {"hostProvenance": []})
                    ),
                )
        for i, exemption in enumerate(spec["hostProvenance"]):
            field = next(f for f in doc.fields if identity(f) == exemption)
            for label, mutation in (
                (
                    "text",
                    {
                        "text": field.text + " unapproved-target.com",
                        "normalized_text": field.normalized_text
                        + " unapproved-target.com",
                    },
                ),
                ("location", {"line": field.line + 1}),
                ("type", {"field_type": "reader_visible_attribute"}),
            ):
                probe = replace(doc, fields=(replace(field, **mutation),))
                check(
                    f"provenance-{doc.document_id}-{i}-{label}",
                    bool(scan_document(probe, {"hostProvenance": [exemption]})),
                )
            check(
                f"provenance-{doc.document_id}-{i}-duplicate",
                bool(
                    scan_document(
                        replace(doc, fields=(field, field)),
                        {"hostProvenance": [exemption]},
                    )
                ),
            )
            if is_policy_scan_field(field):
                probe = replace(
                    doc, fields=(replace(field, text=unsafe, normalized_text=unsafe),)
                )
                check(
                    f"provenance-{doc.document_id}-{i}-action-never-waived",
                    any(
                        "target.real_or_external" in e
                        for e in scan_document(probe, {"hostProvenance": [exemption]})
                    ),
                )
    scratch = ROOT / ".work" / "ch20-regressions"
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=scratch) as directory:
        root = Path(directory)
        target = root / DATA
        target.parent.mkdir(parents=True)
        target.write_bytes(b"{}")
        check("regular-input-positive", read_regular(root, DATA) == b"{}")
        check("unknown-input", rejected(lambda: read_regular(root, "unknown.json")))
        for label, raw in (("empty", b""), ("overlong", b"x" * (1024 * 1024 + 1))):
            target.write_bytes(raw)
            check("input-" + label, rejected(lambda: read_regular(root, DATA)))
        target.unlink()
        target.symlink_to(root / "no-such-file")
        check("input-symlink", rejected(lambda: read_regular(root, DATA)))
        target.unlink()
        os.mkfifo(target)
        check("input-fifo-nonblocking", rejected(lambda: read_regular(root, DATA)))
        target.unlink()
        target.parent.rmdir()
        target.parent.symlink_to(root, target_is_directory=True)
        check("input-ancestor-symlink", rejected(lambda: read_regular(root, DATA)))
    check("canonical-model-final", not validate_model(data, schema, contract))
    check("canonical-repository-final", not repository_errors(data, contract))
    return len(checks), errors
