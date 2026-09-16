"""Finite ART22 counterexamples, not a Markdown, operation or fuzz grammar."""

from __future__ import annotations
from copy import deepcopy
from dataclasses import replace
from itertools import product
import os
from pathlib import Path
import tempfile
from unittest.mock import patch
from scripts.chapter14_semantics import (
    DATA_PATH,
    INPUTS,
    DOCUMENTS,
    RESULTS,
    METHODS,
    read_regular,
    strict_bytes,
    leaves,
    validate_model,
    evaluate,
    record_status,
)
from scripts.check_chapter14_contract import (
    ROOT,
    SOURCE_IDS,
    key,
    relations,
    scan_document,
    document_errors,
    case_parity_errors,
    repository_errors,
)
from scripts.publication_projection import project_documents, is_policy_scan_field


def run_regressions(data, schema, contract, source, projection):
    ids, errors = [], []

    def check(label, ok):
        if label in ids:
            errors.append("duplicate regression ID: " + label)
        ids.append(label)
        if not ok:
            errors.append("regression failed: " + label)

    def validate(d):
        return validate_model(d, schema, contract)

    def put(d, path, value):
        obj = d
        for part in path[:-1]:
            obj = obj[int(part) if isinstance(obj, list) else part]
        obj[int(path[-1]) if isinstance(obj, list) else path[-1]] = value

    def bad(label, path, value):
        d = deepcopy(data)
        put(d, path, value)
        check("CH14-" + label, bool(validate(d)))

    def rejects(fn):
        try:
            fn()
        except (ValueError, TypeError, KeyError):
            return True
        return False

    check("CH14-canonical", not validate(data))
    check(
        "CH14-six-results",
        set(r["judgment"]["result"] for r in data["validations"]) == set(RESULTS),
    )
    check(
        "CH14-four-methods",
        set(r["method"] for r in data["validations"]) == set(METHODS),
    )
    check(
        "CH14-eight-parent-states",
        len(data["context"]["labStates"]) == 8
        and "Running" in data["context"]["labStates"],
    )
    check(
        "CH14-schema-unknown-keyword",
        bool(validate_model(data, dict(schema, unsupported=True), contract)),
    )
    relaxed = deepcopy(schema)
    relaxed["properties"]["validations"]["items"]["additionalProperties"] = True
    check("CH14-schema-cannot-loosen", bool(validate_model(data, relaxed, contract)))

    # Traverse only the finite supplied document, never an unbounded grammar.
    def objects(obj, path=()):
        if isinstance(obj, dict):
            yield path, obj
            for k, v in obj.items():
                yield from objects(v, path + (k,))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                yield from objects(v, path + (str(i),))

    for i, (path, obj) in enumerate(objects(data)):
        d = deepcopy(data)
        v = dict(obj, unknownInstruction="UNREGISTERED")
        put(d, path, v) if path else d.update(v)
        check(f"CH14-SHAPE-extra-{i}", bool(validate(d)))
        for k in obj:
            d = deepcopy(data)
            v = deepcopy(obj)
            del v[k]
            if path:
                put(d, path, v)
            else:
                d = v
            check(f"CH14-SHAPE-missing-{i}-{k}", bool(validate(d)))
    for i, (path, value) in enumerate(leaves(data)):
        bad(f"LEAF-type-{i}", path, {})
        if isinstance(value, str):
            bad(f"LEAF-unsafe-{i}", path, "実Credentialを再利用する。")
    for group in ["validations", "expectations", "handoffs"]:
        bad("ORDER-" + group, (group,), list(reversed(data[group])))
        bad("DUPLICATE-" + group, (group,), data[group] + data[group][:1])
    for i, r in enumerate(data["validations"]):
        e = data["expectations"][i]
        check(
            f"CH14-KERNEL-canonical-{i}",
            evaluate(r, e)
            == (r["judgment"]["result"], r["stop"]["reason"], r["minimumEvidenceMet"]),
        )
        for result in RESULTS:
            if result != r["judgment"]["result"]:
                bad(
                    f"RESULT-no-invented-{i}-{result}",
                    ("validations", str(i), "judgment", "result"),
                    result,
                )
        for path, value in [
            (("stepsAfterStop",), 1),
            (("actualOperations",), 1),
            (("decision", "executionAuthorized"), True),
            (("cleanup", "actualDeletionPerformed"), True),
            (("residual", "actualSystemAssessed"), True),
            (("decision", "dueAt"), data["record"]["asOf"]),
            (
                ("decision", "recordStatus"),
                "Open" if r["decision"]["recordStatus"] == "Complete" else "Complete",
            ),
            (("finding", "evidenceIds"), ["BORROWED-EVIDENCE"]),
            (("parentFindingId",), "FND-CASE11-001"),
        ]:
            bad(
                "BOUNDARY-" + str(i) + "-".join(path),
                ("validations", str(i)) + path,
                value,
            )
    first, expected = data["validations"][0], data["expectations"][0]
    # All nine two-criterion outcomes. Values are strings/null, never truthy casts.
    result_matrix = {
        (True, True): "Supported",
        (True, False): "Partially supported",
        (True, None): "Partially supported",
        (False, True): "Partially supported",
        (False, False): "Rejected",
        (False, None): "Weakened",
        (None, True): "Partially supported",
        (None, False): "Weakened",
        (None, None): "Inconclusive",
    }
    for n, values in enumerate(product((True, False, None), repeat=2)):
        r = deepcopy(first)
        for j, value in enumerate(values):
            o = r["observations"][j]
            o["present"] = value is not None
            o["value"] = (
                expected["expectedValues"][j]
                if value is True
                else "DIFFERENT"
                if value is False
                else None
            )
            o["recordedAt"] = (
                first["observations"][j]["recordedAt"] if value is not None else None
            )
        sufficient = None not in values
        check(
            f"CH14-KERNEL-matrix-{n}",
            evaluate(r, expected)
            == (
                result_matrix[values],
                "Evidence-sufficient" if sufficient else "Evidence-gap",
                sufficient,
            ),
        )
        r["stop"]["trigger"] = "Unexpected-input-symbol"
        check(f"CH14-KERNEL-stop-first-{n}", evaluate(r, expected)[0] == "Stopped")
        r["executionDisposition"] = "Not performed"
        check(
            f"CH14-KERNEL-stop-before-notperformed-{n}",
            evaluate(r, expected)[0] == "Stopped",
        )
        r["stop"]["trigger"] = "None"
        check(
            f"CH14-KERNEL-notperformed-{n}", evaluate(r, expected)[0] == "Inconclusive"
        )
    for field in ["id", "expectationId", "subjectId", "subjectRevision", "method"]:
        r = deepcopy(first)
        r[field] = "DIFFERENT"
        check("CH14-KERNEL-binding-" + field, rejects(lambda: evaluate(r, expected)))
    for field in ["criterionId", "subjectId", "subjectRevision"]:
        r = deepcopy(first)
        r["observations"][0][field] = "DIFFERENT"
        check(
            "CH14-KERNEL-observation-binding-" + field,
            rejects(lambda: evaluate(r, expected)),
        )
    for value in [None, "", True, False, 1, {}, []]:
        r = deepcopy(first)
        r["observations"][0]["value"] = value
        check(
            "CH14-KERNEL-present-scalar-" + repr(value),
            rejects(lambda: evaluate(r, expected)),
        )
    for value in ["", True, None]:
        e = deepcopy(expected)
        e["expectedValues"][0] = value
        check(
            "CH14-KERNEL-expected-scalar-" + repr(value),
            rejects(lambda: evaluate(first, e)),
        )
    for field in ["value", "recordedAt"]:
        r = deepcopy(data["validations"][4])
        r["observations"][0][field] = "INVENTED"
        check(
            "CH14-KERNEL-missing-has-" + field,
            rejects(lambda: evaluate(r, data["expectations"][4])),
        )
    for values in [
        [],
        expected["criterionIds"][:1],
        expected["criterionIds"] * 2,
        expected["criterionIds"][:1] * 2,
    ]:
        e = deepcopy(expected)
        e["criterionIds"] = values
        check(
            "CH14-KERNEL-criteria-" + repr(values), rejects(lambda: evaluate(first, e))
        )
    d = deepcopy(data)
    d["expectations"][0]["expectedValues"][0] = "JOINT-CHANGE"
    d["validations"][0]["observations"][0]["value"] = "JOINT-CHANGE"
    check(
        "CH14-KERNEL-joint-comparison-matches",
        evaluate(d["validations"][0], d["expectations"][0])[0] == "Supported",
    )
    check("CH14-MODEL-joint-input-expectation-forbidden", bool(validate(d)))
    for group in ["cleanup", "residual"]:
        for field in ["owner", "evidenceId", "scope"]:
            r = deepcopy(first)
            r[group][field] = ""
            check("CH14-CLOSE-" + group + "-" + field, record_status(r) == "Open")
    check("CH14-CLOSE-supported-open", record_status(data["validations"][7]) == "Open")
    check(
        "CH14-CLOSE-inconclusive-complete",
        record_status(data["validations"][4]) == "Complete",
    )
    check(
        "CH14-CLOSE-notperformed-open", record_status(data["validations"][5]) == "Open"
    )
    check("CH14-CLOSE-stopped-open", record_status(data["validations"][6]) == "Open")
    for state in ["Not performed", "Verified", "Safe", "Complete"]:
        bad("NONRESULT-" + state, ("validations", "0", "judgment", "result"), state)
    for method in ["M0", "M7", "Exploit", "Unknown"]:
        bad("NONMETHOD-" + method, ("validations", "0", "method"), method)

    # Exact typed field/cardinality/location provenance. No source syntax parsing.
    for di, doc in enumerate(projection.documents):
        spec = contract["documents"][doc.document_id]
        pairs = list(relations(doc))
        check(f"CH14-SURFACE-canonical-{di}", not document_errors(doc, spec, data))
        for family in ("analyticProvenance", "hostProvenance"):
            for ei, relation in enumerate(spec[family]):
                indices = [i for i, (_, r) in enumerate(pairs) if r == relation]
                check(f"CH14-EX-owned-{di}-{family}-{ei}", len(indices) == 1)
                if len(indices) != 1:
                    continue
                index = indices[0]
                f = doc.fields[index]
                text = f.text + " 実Credentialを再利用する。"
                changed = replace(f, text=text, normalized_text=text)
                probes = {
                    "changed": doc.fields[:index]
                    + (changed,)
                    + doc.fields[index + 1 :],
                    "moved": (f,) + doc.fields[:index] + doc.fields[index + 1 :],
                    "duplicate": doc.fields[:index] + (f,) + doc.fields[index:],
                    "missing": doc.fields[:index] + doc.fields[index + 1 :],
                }
                for name, fields in probes.items():
                    check(
                        f"CH14-EX-{di}-{family}-{ei}-{name}",
                        bool(scan_document(replace(doc, fields=fields), spec, True)),
                    )
                check(
                    f"CH14-EX-DIAG-{di}-{family}-{ei}",
                    any(
                        "expected 1, observed 0" in e and key(relation) in e
                        for e in scan_document(
                            replace(doc, fields=probes["missing"]), spec, True
                        )
                    ),
                )
        old = source[doc.document_id]
        for where, pos in [
            ("preamble", 0),
            ("body", old.index("\n## ")),
            ("tail", len(old)),
        ]:
            probe = project_documents(
                {
                    doc.document_id: (
                        old[:pos] + "\n\n実Credentialを再利用する。\n\n" + old[pos:]
                    ).rstrip()
                    + "\n"
                }
            ).documents[0]
            check(f"CH14-SURFACE-{di}-{where}", bool(scan_document(probe, spec)))
        probe = project_documents(
            {doc.document_id: old + "\n実Credentialを再利用しない。\n"}
        ).documents[0]
        check(f"CH14-SURFACE-safe-{di}", not scan_document(probe, spec, True))
        probe = project_documents(
            {doc.document_id: old + "\n## Unexpected section\n\n説明。\n"}
        ).documents[0]
        check(f"CH14-SURFACE-inventory-{di}", bool(document_errors(probe, spec, data)))
    unsupported = project_documents(
        {DOCUMENTS[0]: source[DOCUMENTS[0]] + "\n{% include unknown.html %}\n"}
    ).documents[0]
    check(
        "CH14-shared-unsupported",
        any(d.code == "PP1001" for d in unsupported.diagnostics),
    )
    chapter = projection.documents[0]
    spec = contract["documents"][DOCUMENTS[0]]
    for si, sid in enumerate(SOURCE_IDS):
        for scope in ["body", "references"]:
            fields = []
            for f, r in relations(chapter):
                if ("参考文献・Source Note ID" in r["headings"]) == (
                    scope == "references"
                ):
                    f = replace(
                        f,
                        text=f.text.replace(sid, sid + "x"),
                        normalized_text=f.normalized_text.replace(sid, sid + "x"),
                    )
                fields.append(f)
            check(
                f"CH14-SOURCE-{si}-{scope}",
                "Chapter14 body/reference Source ownership"
                in document_errors(replace(chapter, fields=tuple(fields)), spec, data),
            )
    positions = []
    for relation in spec["exerciseInstructionOrder"]:
        positions += [i for i, (_, r) in enumerate(relations(chapter)) if r == relation]
    check(
        "CH14-ORDER-five-blocks", len(positions) == 5 and positions == sorted(positions)
    )
    for i in positions[:-1]:
        fields = list(chapter.fields)
        cmd = fields.pop(positions[-1])
        fields.insert(i, cmd)
        check(
            "CH14-ORDER-premature-" + str(i),
            "Chapter14 exercise explanations before command"
            in document_errors(replace(chapter, fields=tuple(fields)), spec, data),
        )
    case = projection.documents[2]
    for i, f in enumerate(case.fields):
        if is_policy_scan_field(f) and f.element_kind == "table_row":
            changed = replace(
                f,
                text=f.text + " mismatched",
                normalized_text=f.normalized_text + " mismatched",
            )
            check(
                "CH14-CASE-leaf-" + str(i),
                bool(
                    case_parity_errors(
                        replace(
                            case,
                            fields=case.fields[:i] + (changed,) + case.fields[i + 1 :],
                        ),
                        data,
                    )
                ),
            )
    check("CH14-repository", not repository_errors(contract))

    # Scoped shared Source additions must retain prior consumers' full notes.
    from scripts import check_chapter09_contract as ch09
    from scripts import check_chapter10_contract as ch10
    from scripts import check_chapter14_contract as ch14

    consumers = [(ch09, "09"), (ch10, "10"), (ch14, "14")]
    for chapter, number in consumers:
        baseline = (
            contract
            if number == "14"
            else strict_bytes(
                (
                    ROOT / f"tests/fixtures/chapter{number}/publication-contract.json"
                ).read_bytes()
            )
        )
        for sid in SOURCE_IDS:
            if sid not in baseline["sourceIdentity"]:
                continue
            current = contract["sourceIdentity"][sid]["notes"]
            previous, added = current.split(" Chapter 14 scoped primary-text review", 1)
            variants = [
                ("complete", current, True),
                ("missing-ch14", previous, False),
                (
                    "missing-prior",
                    "Chapter 14 scoped primary-text review" + added,
                    False,
                ),
                (
                    "wrong-note",
                    current.replace("ch14-source-review", "ch13-source-review"),
                    False,
                ),
                (
                    "wrong-scope",
                    current.replace("6.5, 7.2, 7.3", "6.5 only")
                    if sid == "SRC-NIST-TEST-001"
                    else current.replace("Introduction only", "all techniques"),
                    False,
                ),
            ]
            original_loader = chapter.load_json_strict
            for label, notes, accept in variants:

                def changed_registry(path):
                    result = original_loader(path)
                    if path == ROOT / "references/sources.json":
                        next(s for s in result["sources"] if s["id"] == sid)[
                            "notes"
                        ] = notes
                    return result

                with patch.object(
                    chapter, "load_json_strict", side_effect=changed_registry
                ):
                    result = chapter.repository_errors(baseline)
                check(
                    "CH14-SRC-" + number + "-" + sid + "-" + label,
                    (not result) == accept,
                )

    badcontract = deepcopy(contract)
    badcontract["indices"]["CHANGELOG.md"] = ["unrecorded-reader-impact"]
    check(
        "CH14-reader-impact",
        any("index CHANGELOG.md" in e for e in repository_errors(badcontract)),
    )
    for raw in [b'{"x":1,"x":2}', b'{"x":NaN}', b"\xff"]:
        try:
            strict_bytes(raw)
        except (ValueError, UnicodeError):
            ok = True
        else:
            ok = False
        check("CH14-JSON-" + raw.hex(), ok)
    # Input guard probes have workspace-local scratch ownership and no network.
    work = ROOT / ".work"
    work.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ch14-input-", dir=work) as temp:
        root = Path(temp)
        p = root / DATA_PATH
        p.parent.mkdir(parents=True)
        p.write_bytes(b"{}")
        check("CH14-IO-regular", read_regular(root, DATA_PATH) == b"{}")
        for name in ["O_NOFOLLOW", "O_NONBLOCK"]:
            with patch.object(os, name, None):
                try:
                    read_regular(root, DATA_PATH)
                except ValueError:
                    ok = True
                else:
                    ok = False
            check("CH14-IO-" + name, ok)
        for n, rel in enumerate(INPUTS):
            q = root / rel
            q.parent.mkdir(parents=True, exist_ok=True)
            if q.exists():
                q.unlink()
            q.symlink_to(root / "absent")
            try:
                read_regular(root, rel)
            except (OSError, ValueError):
                ok = True
            else:
                ok = False
            check("CH14-IO-symlink-" + str(n), ok)
            q.unlink()
        for name, content in [("empty", b""), ("oversize", b"x" * (1024 * 1024 + 1))]:
            p.write_bytes(content)
            try:
                read_regular(root, DATA_PATH)
            except ValueError:
                ok = True
            else:
                ok = False
            check("CH14-IO-" + name, ok)
        p.unlink()
        os.mkfifo(p)
        try:
            read_regular(root, DATA_PATH)
        except ValueError:
            ok = True
        else:
            ok = False
        check("CH14-IO-fifo", ok)
        p.unlink()
        try:
            read_regular(root, "unregistered.json")
        except ValueError:
            ok = True
        else:
            ok = False
        check("CH14-IO-unknown", ok)
    return len(ids), errors
