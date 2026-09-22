"""Finite ART06 question, evidence and selection counterexamples; no syntax parser."""

from copy import deepcopy
from dataclasses import replace
from itertools import permutations
import ast
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

from scripts.chapter18_model import (
    DATA,
    CORPUS,
    DOCUMENTS,
    INPUTS,
    digest,
    strict,
    read_regular,
    validate_model,
)
from scripts.chapter18_query import RESULTS, LIMIT, VERSION, evaluate, verify_claim
from scripts.check_chapter18_contract import (
    ROOT,
    inventory,
    scan_document,
    document_errors,
    case_errors,
    parent_errors,
)
from scripts.check_editorial_input_manifest import (
    ManifestError,
    validate_schema_instance,
)
from scripts.publication_projection import project_documents, is_policy_scan_field


def run_regressions(data, schema, contract, source, projection):
    checks, errors = [], []

    def check(label, ok):
        if label in checks:
            errors.append("duplicate ART06 regression: " + label)
        checks.append(label)
        if not ok:
            errors.append("failed ART06 regression: " + label)

    def rejected(fn):
        try:
            result = fn()
            return isinstance(result, list) and bool(result)
        except (ValueError, TypeError, KeyError, StopIteration, OSError, ManifestError):
            return True

    def at(obj, path):
        for key in path:
            obj = obj[key]
        return obj

    def containers(obj, path=()):
        if isinstance(obj, dict):
            yield path, obj
            for key, value in obj.items():
                yield from containers(value, path + (key,))
        elif isinstance(obj, list):
            for key, value in enumerate(obj):
                yield from containers(value, path + (key,))

    check("H-HARNESS-BYTES", not rejected(lambda: b"accepted"))
    check("H-HARNESS-OBJECT", not rejected(lambda: {"accepted": True}))
    corpus = strict(read_regular(ROOT, CORPUS))
    cases = corpus["cases"]
    check(
        "H-CORPUS-INVENTORY",
        corpus["caseCount"] == len(cases) == 40
        and [c["id"] for c in cases] == [f"QCASE18-{i:02}" for i in range(1, 41)],
    )
    check(
        "H-CORPUS-VERSION",
        corpus["schemaVersion"] == "1.0.0" and corpus["queryVersion"] == VERSION,
    )
    check(
        "H-CORPUS-OWNERSHIP",
        all(c["requirement"] for c in cases)
        and {c["expected"]["result"] for c in cases} == set(RESULTS),
    )
    # Kernel checks bypass authored digests and schema: expectations were written
    # separately, not populated from evaluate(). Permutations are finite (<=3 rows).
    for case in cases:
        before = deepcopy(case["input"])
        output = evaluate(case["input"])
        check(
            case["id"] + "-EXPECTED",
            {k: output[k] for k in case["expected"]} == case["expected"],
        )
        check(case["id"] + "-NO-MUTATION", case["input"] == before)
        check(
            case["id"] + "-LIMIT",
            output["limit"] == LIMIT
            and all(output[k] for k in ("alternative", "owner", "reassessment")),
        )
        check(
            case["id"] + "-NO-DELIVERY",
            all(
                h["status"] == "planned-not-delivered"
                and h["receipt"] is None
                and h["executionAuthorized"] is False
                for h in output["handoffs"]
            ),
        )
        for result in RESULTS:
            if result == case["expected"]["result"]:
                check(
                    case["id"] + "-CLAIM-" + result,
                    verify_claim(case["input"], result) == output,
                )
            else:
                check(
                    case["id"] + "-CLAIM-" + result,
                    rejected(lambda: verify_claim(case["input"], result)),
                )
        n = 0
        for events in permutations(case["input"]["events"]):
            for receipts in permutations(case["input"]["receipts"]):
                for approvals in permutations(case["input"]["approvals"]):
                    changed = deepcopy(case["input"])
                    changed.update(
                        events=list(events),
                        receipts=list(receipts),
                        approvals=list(approvals),
                    )
                    check(f"{case['id']}-ORDER-{n}", evaluate(changed) == output)
                    n += 1
        check(
            case["id"] + "-KEY-ORDER",
            evaluate(dict(reversed(list(case["input"].items())))) == output,
        )
    base = cases[0]["input"]
    for result in (
        "Partially supported",
        "Limited negative finding",
        "No compromise",
        "Validated",
        "",
    ):
        check("H-K-RESULT-" + result, rejected(lambda: verify_claim(base, result)))
    for zero in (False, True):
        for stream in range(3):
            for field in (
                "producer",
                "collected",
                "retained",
                "queryable",
                "clock",
                "identity",
            ):
                changed = deepcopy(base)
                if zero:
                    changed["events"] = []
                changed["receipts"][stream][field] = False
                result = evaluate(changed)
                check(
                    f"H-K-COVERAGE-{zero}-{stream}-{field}",
                    result["result"] == "Inconclusive"
                    and result["pairs"] == result["evidence"] == [],
                )
    changes = [
        (("executionAuthorized",), True),
        (("parentReceipt",), "EVD-TCM16-005-1"),
        (("syntheticOnly",), 1),
        (("offlineOnly",), False),
        (("plan", "grantStart"), 0.0),
        (("plan", "pivotSeconds"), 3600),
        (("plan", "subject"), "APP-TCM16-001"),
        (("mode",), "live-siem"),
        (("receipts", 0, "producer"), "true"),
        (("receipts", 0, "start"), False),
        (("receipts", 0, "end"), 0),
        (("events", 0, "revision"), "HUNT18-REV-000"),
        (("events", 0, "subject"), "APP-TCM16-001"),
        (("events", 0, "id"), "rec-pos-001"),
        (("events", 0, "eventTime"), True),
        (("events", 0, "ingestTime"), 1),
        (("events", 0, "uncertainty"), -1),
        (("events", 0, "workload"), "real-user"),
        (("events", 0, "scopes"), ["scope-invoice-read", "scope-invoice-read"]),
        (("events", 1, "scopes"), ["scope-invoice-read"]),
    ]
    for i, (path, value) in enumerate(changes):
        changed = deepcopy(base)
        at(changed, path[:-1])[path[-1]] = value
        check(f"H-K-TYPE-BIND-{i}", rejected(lambda: evaluate(changed)))
    for path, obj in containers(base):
        for key in obj:
            changed = deepcopy(base)
            del at(changed, path)[key]
            check("H-K-MISSING-" + str(path) + key, rejected(lambda: evaluate(changed)))
        changed = deepcopy(base)
        at(changed, path)["unreviewedField"] = True
        check("H-K-EXTRA-" + str(path), rejected(lambda: evaluate(changed)))
    for key in ("events", "receipts"):
        changed = deepcopy(base)
        changed[key].append(deepcopy(changed[key][0]))
        check("H-K-DUPLICATE-" + key, rejected(lambda: evaluate(changed)))
    changed = deepcopy(cases[1]["input"])
    extra = deepcopy(changed["approvals"][0])
    extra["id"] = "SYN-APP-02"
    changed["approvals"].append(extra)
    check("H-K-DUPLICATE-TICKET", rejected(lambda: evaluate(changed)))
    output = evaluate(base)
    output["scope"]["population"].append("syn-workload-b")
    check(
        "H-K-RETURN-NOT-SHARED",
        evaluate(base)["scope"]["population"]
        == base["plan"]["population"]
        == ["syn-workload-a"],
    )
    tree = ast.parse((ROOT / "scripts/chapter18_query.py").read_text())
    imports = [
        n.module if isinstance(n, ast.ImportFrom) else a.name
        for n in ast.walk(tree)
        if isinstance(n, (ast.Import, ast.ImportFrom))
        for a in (n.names if isinstance(n, ast.Import) else [None])
    ]
    check("H-K-PURE-DIRECT-IMPORTS", imports == ["copy"])

    # PR150 / discussion_r4072522451: unchanged schema permits these values.
    # Refresh the exact edited top-level digest to isolate semantic enforcement.
    for root, key, value in (
        ("record", "actualCollections", 1),
        ("record", "actualIncidents", 1),
        ("safety", "personalDataIncluded", True),
        ("safety", "productSchemaClaimed", True),
    ):
        changed, checkpoint = deepcopy(data), deepcopy(contract)
        changed[root][key] = value
        checkpoint["authoredInputs"][root] = digest(changed[root])
        check(
            "H-M-SYNTHETIC-" + root + "-" + key,
            validate_model(changed, schema, checkpoint)
            == ["ART06 synthetic-only record claims"],
        )

    # Closed structure at every canonical object, independent of authored hashes.
    for path, obj in containers(data):
        for key in obj:
            changed = deepcopy(data)
            del at(changed, path)[key]
            check(
                "H-S-MISSING-" + str(path) + key,
                rejected(lambda: validate_schema_instance(changed, schema)),
            )
        changed = deepcopy(data)
        at(changed, path)["unreviewedField"] = True
        check(
            "H-S-EXTRA-" + str(path),
            rejected(lambda: validate_schema_instance(changed, schema)),
        )
    for i, row in enumerate(data["contrasts"]):
        matched = next(c for c in cases if c["id"] == row["corpusId"])
        check(
            f"H-M-CORPUS-{i}",
            row["input"] == matched["input"]
            and {k: row["queryResult"][k] for k in matched["expected"]}
            == matched["expected"],
        )
        mutations = [
            (
                ("queryResult", "result"),
                next(r for r in RESULTS if r != row["queryResult"]["result"]),
            ),
            (
                ("judgment", "result"),
                next(r for r in RESULTS if r != row["judgment"]["result"]),
            ),
            (("judgment", "noCompromiseClaim"), True),
            (("judgment", "owner"), ""),
            (("judgment", "gap"), ""),
            (("judgment", "alternative"), ""),
            (("judgment", "reassessment"), ""),
            (("supplyEvidence", "inputDigest"), "0" * 64),
            (("supplyEvidence", "inputId"), "FIX-HUNT18-999"),
            (("supplyEvidence", "queryId"), "QRY-HUNT18-999"),
            (("handoffs", 0, "route"), "unreviewed"),
            (("handoffs", 0, "status"), "delivered"),
            (("handoffs", 0, "targetChapter"), 25),
            (("handoffs", 0, "backlogId"), "unbound"),
            (("handoffs", 0, "owner"), "unbound"),
            (("handoffs", 0, "dueAt"), "2026-09-22T00:00:00Z"),
            (("handoffs", 0, "sourceFindingId"), "unbound"),
            (("handoffs", 0, "sourceSupplyId"), "unbound"),
            (("handoffs", 0, "executionAuthorized"), True),
        ]
        for n, (path, value) in enumerate(mutations):
            changed, checkpoint = deepcopy(data), deepcopy(contract)
            at(changed["contrasts"][i], path[:-1])[path[-1]] = value
            # Remove snapshot-only rejection to prove judgment/binding semantics.
            checkpoint["authoredInputs"]["contrasts"] = digest(changed["contrasts"])
            check(
                f"H-M-SEMANTIC-{i}-{n}",
                rejected(lambda: validate_model(changed, schema, checkpoint)),
            )
        changed = deepcopy(data)
        changed["contrasts"][i]["judgment"]["gap"] = (
            "実在する第三者システムにアクセスする。"
        )
        check(
            f"H-M-POLICY-{i}",
            any(
                "target.real_or_external" in e
                for e in validate_model(changed, schema, contract)
            ),
        )
    for name in (
        "parentStateChanged",
        "authorityTransferred",
        "evidenceTransferred",
        "parentHandoffReceived",
        "chapter17ContractSatisfied",
    ):
        changed = deepcopy(data)
        changed["parents"][name] = True
        check("H-M-NO-INHERIT-" + name, bool(parent_errors(changed, ROOT)))
    for payload in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}', "\ufeff{}"):
        check("H-J-" + payload, rejected(lambda: strict(payload.encode())))

    probes = {}
    for p in DOCUMENTS:
        for position in ("preamble", "body", "tail"):
            unsafe = "\n\n実在する第三者システムにアクセスする。\n\n"
            text = source[p]
            if position == "preamble":
                text = unsafe + text
            elif position == "tail":
                text += unsafe
            else:
                i = text.index("\n## ")
                text = text[:i] + unsafe + text[i:]
            probes[p + "-" + position] = text
    for doc in project_documents(probes).documents:
        check(
            "H-P-ACTION-" + doc.document_id,
            any(
                "target.real_or_external" in e
                for e in scan_document(doc, {"hostProvenance": []})
            ),
        )
    for doc in projection.documents:
        spec = contract["documents"][doc.document_id]
        check("H-P-CANON-" + doc.document_id, not document_errors(doc, spec, data))
        for label, fields in [
            ("missing", doc.fields[:-1]),
            ("duplicate", doc.fields + doc.fields[-1:]),
            ("reverse", tuple(reversed(doc.fields))),
        ]:
            check(
                "H-P-INVENTORY-" + doc.document_id + label,
                bool(document_errors(replace(doc, fields=fields), spec, data)),
            )
        for idx, f in enumerate(doc.fields):
            if f.element_kind == "heading" and is_policy_scan_field(f):
                fields = list(doc.fields)
                fields[idx] = replace(
                    f, text="未審査の節", normalized_text="未審査の節"
                )
                check(
                    "H-P-HEADING-" + f.location,
                    bool(
                        document_errors(replace(doc, fields=tuple(fields)), spec, data)
                    ),
                )
        for item in spec["hostProvenance"]:
            idx = inventory(doc).index(item)
            f = doc.fields[idx]
            for label, text in [
                ("host", "https://outside.invalid/"),
                ("action", "実在する第三者システムにアクセスする。"),
            ]:
                fields = list(doc.fields)
                fields[idx] = replace(f, text=text, normalized_text=text)
                check(
                    "H-P-PROVENANCE-" + f.location + label,
                    bool(scan_document(replace(doc, fields=tuple(fields)), spec)),
                )
            check(
                "H-P-PROVENANCE-DUP-" + f.location,
                bool(scan_document(replace(doc, fields=doc.fields + (f,)), spec)),
            )
    changed = deepcopy(data)
    changed["contrasts"][0]["judgment"]["gap"] = "新しい説明"
    check("H-P-CASE-LEAF", bool(case_errors(projection.documents[2], changed)))
    work = ROOT / ".work"
    work.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ch18-regression-", dir=work) as temp:
        root = Path(temp)
        for p in INPUTS:
            target = root / p
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(b"{}")
            check("H-IO-REGULAR-" + p, read_regular(root, p) == b"{}")
            target.unlink()
            target.symlink_to(ROOT / DATA)
            check("H-IO-SYMLINK-" + p, rejected(lambda: read_regular(root, p)))
            target.unlink()
            target.write_bytes(b"{}")
        target = root / DATA
        for label, value in [("empty", b""), ("large", b"x" * (1024 * 1024 + 1))]:
            target.write_bytes(value)
            check("H-IO-" + label, rejected(lambda: read_regular(root, DATA)))
        target.unlink()
        target.mkdir()
        check("H-IO-DIRECTORY", rejected(lambda: read_regular(root, DATA)))
        target.rmdir()
        os.mkfifo(target)
        check("H-IO-FIFO", rejected(lambda: read_regular(root, DATA)))
        target.unlink()
        target.write_bytes(b"{}")
        for flag in ("O_NOFOLLOW", "O_NONBLOCK"):
            with patch.object(os, flag, create=False):
                delattr(os, flag)
                check(
                    "H-IO-PLATFORM-" + flag, rejected(lambda: read_regular(root, DATA))
                )
        for name in ("../README.md", "/etc/passwd", "cases/../README.md"):
            check("H-IO-INVENTORY-" + name, rejected(lambda: read_regular(root, name)))
    return len(checks), errors
