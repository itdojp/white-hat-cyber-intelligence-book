"""Finite ART21 counterexamples; no chapter-owned renderer or secret grammar."""

from __future__ import annotations
from copy import deepcopy
from dataclasses import replace
import os
from pathlib import Path
import tempfile
from unittest.mock import patch
from scripts.chapter13_semantics import (
    DATA_PATH,
    INPUTS,
    DOCUMENTS,
    STATES,
    read_regular,
    strict_bytes,
    leaves,
    validate_model,
    compare,
)
from scripts.check_chapter13_contract import (
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
        check("CH13-" + label, bool(validate(d)))

    check("CH13-canonical", not validate(data))
    check(
        "CH13-state-inventory",
        set(c["finding"]["status"] for c in data["chains"]) == set(STATES),
    )
    check("CH13-context-readonly", data["safety"]["executionAuthorized"] is False)

    # Bounded traversal of this supplied record, not a generated language grammar.
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
        v = deepcopy(obj)
        v["unregisteredSecretValue"] = "NOT-ALLOWED"
        put(d, path, v) if path else d.update(v)
        check(f"CH13-SHAPE-extra-{i}", bool(validate(d)))
        for k in obj:
            d = deepcopy(data)
            v = deepcopy(obj)
            del v[k]
            if path:
                put(d, path, v)
            else:
                d = v
            check(f"CH13-SHAPE-missing-{i}-{k}", bool(validate(d)))
    for i, (path, value) in enumerate(leaves(data)):
        bad(f"LEAF-type-{i}", path, {} if not isinstance(value, dict) else [])
        if isinstance(value, str):
            bad(f"LEAF-unsafe-{i}", path, "実Credentialを再利用する。")
    for group in ["chains", "expectations", "principals", "handoffs"]:
        bad("ORDER-" + group, (group,), list(reversed(data[group])))
        bad("DUPLICATE-" + group, (group,), data[group] + data[group][:1])
    # Direct evaluator contrasts distinguish data defects from state outcomes.
    for i, c in enumerate(data["chains"]):
        e = data["expectations"][i]
        check(
            f"CH13-KERNEL-canonical-{i}",
            compare(c, e) == (c["evidence"]["expectedState"], c["evidence"]["reason"]),
        )
    first = data["chains"][0]
    expected = data["expectations"][0]
    comparison_fields = {
        "source": ["revision", "lockDigest"],
        "action": ["revision"],
        "build": [
            "sourceRevision",
            "lockDigest",
            "builderId",
            "runnerClass",
            "isolation",
            "network",
            "cache",
            "workloadPrincipalId",
            "secretClassId",
            "permission",
        ],
        "artifact": ["digest"],
        "provenance": [
            "artifactId",
            "subjectDigest",
            "sourceRevision",
            "lockDigest",
            "builderId",
            "buildType",
            "parameters",
        ],
        "registry": ["digest"],
        "promotion": ["digest"],
        "deployment": ["digest"],
        "runtime": ["digest", "boundaryId"],
        "dependency": ["review"],
    }
    for group, keys in comparison_fields.items():
        for k in keys:
            c = deepcopy(first)
            c[group][k] = "DIFFERENT-SUPPLIED-VALUE"
            check(
                f"CH13-KERNEL-mismatch-{group}-{k}",
                compare(c, expected)[0] == "Rejected",
            )
            c = deepcopy(first)
            c[group][k] = None
            check(
                f"CH13-KERNEL-missing-{group}-{k}", compare(c, expected)[0] == "Unknown"
            )
    for changed in ("chain", "expectation", "revision"):
        c = deepcopy(first)
        e = deepcopy(expected)
        if changed == "chain":
            c["id"] = "CHN-PSA13-002"
        if changed == "expectation":
            c["evidence"]["expectationId"] = "EXP-PSA13-002"
        if changed == "revision":
            e["recordRevision"] = "DIFFERENT"
        try:
            compare(c, e)
        except ValueError:
            ok = True
        else:
            ok = False
        check("CH13-KERNEL-binding-" + changed, ok)
    # A known false necessary condition wins over another missing condition.
    c = deepcopy(first)
    c["provenance"]["subjectDigest"] = None
    c["runtime"]["digest"] = "DIFFERENT"
    check(
        "CH13-KERNEL-refutation-before-unknown", compare(c, expected)[0] == "Rejected"
    )
    for basis, state, reason in [
        ("Declared summary", "Declared", "declaration-only"),
        ("Observed summary", "Observed", "observation-only"),
        ("Compared summary", "Verified", "all-supplied-bindings-match"),
    ]:
        d = deepcopy(data)
        c = d["chains"][0]
        c["evidence"].update(basis=basis, expectedState=state, reason=reason)
        c["finding"]["status"] = state
        check("CH13-positive-basis-" + state, not validate(d))
    for i in range(8):
        for state in STATES:
            if state == data["chains"][i]["finding"]["status"]:
                continue
            d = deepcopy(data)
            d["chains"][i]["evidence"]["expectedState"] = state
            d["chains"][i]["finding"]["status"] = state
            check(f"CH13-STATE-no-invented-{i}-{state}", bool(validate(d)))
    # Exact typed field/cardinality/location provenance. No source syntax parsing.
    for di, doc in enumerate(projection.documents):
        spec = contract["documents"][doc.document_id]
        pairs = list(relations(doc))
        check(f"CH13-SURFACE-canonical-{di}", not document_errors(doc, spec, data))
        for family in ("analyticProvenance", "hostProvenance"):
            for ei, relation in enumerate(spec[family]):
                indices = [i for i, (_, r) in enumerate(pairs) if r == relation]
                check(f"CH13-EX-owned-{di}-{family}-{ei}", len(indices) == 1)
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
                        f"CH13-EX-{di}-{family}-{ei}-{name}",
                        bool(scan_document(replace(doc, fields=fields), spec, True)),
                    )
                check(
                    f"CH13-EX-DIAG-{di}-{family}-{ei}",
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
            check(f"CH13-SURFACE-{di}-{where}", bool(scan_document(probe, spec)))
        probe = project_documents(
            {doc.document_id: old + "\n実Credentialを再利用しない。\n"}
        ).documents[0]
        check(f"CH13-SURFACE-safe-{di}", not scan_document(probe, spec, True))
        probe = project_documents(
            {doc.document_id: old + "\n## Unexpected section\n\n説明。\n"}
        ).documents[0]
        check(f"CH13-SURFACE-inventory-{di}", bool(document_errors(probe, spec, data)))
    unsupported = project_documents(
        {DOCUMENTS[0]: source[DOCUMENTS[0]] + "\n{% include unknown.html %}\n"}
    ).documents[0]
    check(
        "CH13-shared-unsupported",
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
                f"CH13-SOURCE-{si}-{scope}",
                "Chapter13 body/reference Source ownership"
                in document_errors(replace(chapter, fields=tuple(fields)), spec, data),
            )
    positions = []
    for relation in spec["exerciseInstructionOrder"]:
        positions += [i for i, (_, r) in enumerate(relations(chapter)) if r == relation]
    check(
        "CH13-ORDER-five-blocks", len(positions) == 5 and positions == sorted(positions)
    )
    for i in positions[:-1]:
        fields = list(chapter.fields)
        cmd = fields.pop(positions[-1])
        fields.insert(i, cmd)
        check(
            "CH13-ORDER-premature-" + str(i),
            "Chapter13 exercise explanations before command"
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
                "CH13-CASE-leaf-" + str(i),
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
    check("CH13-repository", not repository_errors(contract))
    badcontract = deepcopy(contract)
    badcontract["indices"]["CHANGELOG.md"] = ["unrecorded-reader-impact"]
    check(
        "CH13-reader-impact",
        any("index CHANGELOG.md" in e for e in repository_errors(badcontract)),
    )
    for raw in [b'{"x":1,"x":2}', b'{"x":NaN}', b"\xff"]:
        try:
            strict_bytes(raw)
        except (ValueError, UnicodeError):
            ok = True
        else:
            ok = False
        check("CH13-JSON-" + raw.hex(), ok)
    # Input guard probes have workspace-local scratch ownership and no network.
    work = ROOT / ".work"
    work.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ch13-input-", dir=work) as temp:
        root = Path(temp)
        p = root / DATA_PATH
        p.parent.mkdir(parents=True)
        p.write_bytes(b"{}")
        check("CH13-IO-regular", read_regular(root, DATA_PATH) == b"{}")
        for name in ["O_NOFOLLOW", "O_NONBLOCK"]:
            with patch.object(os, name, None):
                try:
                    read_regular(root, DATA_PATH)
                except ValueError:
                    ok = True
                else:
                    ok = False
            check("CH13-IO-" + name, ok)
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
            check("CH13-IO-symlink-" + str(n), ok)
            q.unlink()
        for name, content in [("empty", b""), ("oversize", b"x" * (1024 * 1024 + 1))]:
            p.write_bytes(content)
            try:
                read_regular(root, DATA_PATH)
            except ValueError:
                ok = True
            else:
                ok = False
            check("CH13-IO-" + name, ok)
        p.unlink()
        os.mkfifo(p)
        try:
            read_regular(root, DATA_PATH)
        except ValueError:
            ok = True
        else:
            ok = False
        check("CH13-IO-fifo", ok)
        p.unlink()
        try:
            read_regular(root, "unregistered.json")
        except ValueError:
            ok = True
        else:
            ok = False
        check("CH13-IO-unknown", ok)
    return len(ids), errors
