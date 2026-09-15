"""Finite Chapter12 selection/model tests; generic syntax belongs to Layer B."""

from __future__ import annotations
import ast
from copy import deepcopy
from dataclasses import replace
import json
import os
from pathlib import Path
import tempfile
from unittest.mock import patch
from scripts.chapter12_semantics import (
    DATA_PATH,
    DOCUMENTS,
    INPUTS,
    CLASSES,
    STATES,
    METHODS,
    validate_model,
    evaluate_path,
    leaves,
    read_regular,
    strict_bytes,
    utc,
)
from scripts.check_chapter12_contract import (
    ROOT,
    SOURCE_IDS,
    key,
    relations,
    scan_document,
    document_errors,
    repository_errors,
    case_parity_errors,
)
from scripts.check_editorial_input_manifest import ManifestError
from scripts.publication_projection import project_documents, is_policy_scan_field


def run_regressions(data, schema, contract, source, projection):
    ids, errors = [], []

    def check(label, passed):
        if label in ids:
            errors.append("duplicate regression ID: " + label)
        ids.append(label)
        if not passed:
            errors.append("regression failed: " + label)

    def validate(d=data, s=schema):
        return validate_model(d, s, contract)

    def put(d, path, value):
        p = d
        for k in path[:-1]:
            p = p[int(k) if isinstance(p, list) else k]
        p[int(path[-1]) if isinstance(p, list) else path[-1]] = value

    def bad(label, path, value):
        d = deepcopy(data)
        put(d, path, value)
        check("CH12-SEM-" + label, bool(validate(d)))

    check("CH12-positive-canonical", not validate())
    check(
        "CH12-positive-six-states", tuple(p["state"] for p in data["paths"]) == STATES
    )
    check(
        "CH12-positive-four-classes",
        tuple(p["principalClass"] for p in data["principals"]) == CLASSES,
    )
    check(
        "CH12-positive-three-methods",
        set(p["validationMethod"] for p in data["paths"]) == set(METHODS),
    )
    for mfa in ("Enabled", "Disabled", "Unknown"):
        d = deepcopy(data)
        d["principals"][0]["mfaStatus"] = mfa
        check("CH12-positive-MFA-not-path-state-" + mfa, not validate(d))
    d = deepcopy(data)
    d["limits"].update(minutes=10, outputBytes=4096, retentionHours=1)
    check("CH12-positive-tighter-budgets", not validate(d))
    # A reader may withhold a stronger conclusion; existing evidence must remain
    # explicitly owned and does not automatically require a promotion.
    d = deepcopy(data)
    d["paths"][2]["state"] = "Config-confirmed"
    check("CH12-positive-withheld-event-conclusion", not validate(d))
    # Independently test the finite evaluator's declared conjunction, including
    # safe counterexamples, without pretending it is a general policy engine.
    p, e = data["paths"][3], data["evaluations"][0]
    check("CH12-EVAL-allow", evaluate_path(data, p, e) == ("Allow", None))
    check(
        "CH12-EVAL-necessary-deny",
        evaluate_path(data, data["paths"][4], data["evaluations"][1])
        == ("Deny", "EDG-IAR12-009"),
    )
    for field, wrong in (
        ("issuerId", "RP-IAR12-003"),
        ("audienceId", "RP-IAR12-002"),
        ("relyingPartyId", "RP-IAR12-002"),
        ("issuerId", None),
        ("audienceId", None),
    ):
        request = deepcopy(e)
        request[field] = wrong
        check(
            "CH12-EVAL-binding-" + field + "-" + str(wrong),
            evaluate_path(data, p, request) == ("Deny", "EDG-IAR12-013"),
        )
    d = deepcopy(data)
    d["edges"][12]["condition"] = "Unknown"
    check("CH12-EVAL-unknown-not-safe", evaluate_path(d, p, e) == ("Unknown", None))
    d["edges"][10]["condition"] = "False"
    check(
        "CH12-EVAL-known-necessary-deny-with-unknown",
        evaluate_path(d, p, e) == ("Deny", "EDG-IAR12-011"),
    )
    d = deepcopy(data)
    d["edges"][0]["condition"] = "False"
    check(
        "CH12-EVAL-unrelated-edge-not-refutation",
        evaluate_path(d, p, e) == ("Allow", None),
    )
    for field in (
        "pathId",
        "principalId",
        "resourceId",
        "action",
        "graphRevision",
        "policyRevision",
    ):
        request = deepcopy(e)
        request[field] = "SYNTH-WRONG-BINDING"
        try:
            evaluate_path(data, p, request)
            rejected = False
        except ValueError:
            rejected = True
        check("CH12-EVAL-kernel-tuple-" + field, rejected)
    d = deepcopy(data)
    d["edges"][12]["condition"] = "unsupported"
    try:
        evaluate_path(d, p, e)
        rejected = False
    except ValueError:
        rejected = True
    check("CH12-EVAL-kernel-condition", rejected)

    # Closed schema: finite traversal of the supplied record, not a fuzz grammar.
    def objects(value, path=()):
        if isinstance(value, dict):
            yield path, value
            for k, v in value.items():
                yield from objects(v, path + (k,))
        elif isinstance(value, list):
            for i, v in enumerate(value):
                yield from objects(v, path + (i,))

    for oi, (path, obj) in enumerate(objects(data), 1):
        for extra in ("credentialValue", "token", "cookie", "secret"):
            d = deepcopy(data)
            target = d
            for k in path:
                target = target[k]
            target[extra] = "SYNTH-UNOWNED-VALUE"
            check(f"CH12-CLOSED-{oi}-extra-{extra}", bool(validate(d)))
        for ki, k in enumerate(obj, 1):
            d = deepcopy(data)
            target = d
            for part in path:
                target = target[part]
            del target[k]
            check(f"CH12-CLOSED-{oi}-missing-{ki}", bool(validate(d)))
    for li, (path, value) in enumerate(leaves(data), 1):
        if isinstance(value, str):
            d = deepcopy(data)
            put(d, path, "SYNTH-UNREGISTERED-OPAQUE-MATERIAL")
            check(f"CH12-VOCAB-{li}-unregistered-value", bool(validate(d)))
    negatives = [
        ("root-execution", ("executionAuthorized",), True),
        ("root-nonsynthetic", ("synthetic",), False),
        (
            "parent-expiry",
            ("parents", "authorizationExpiresAt"),
            "2026-12-31T00:00:00Z",
        ),
        (
            "parent-window",
            ("parents", "authorizationWindow", 0),
            "2026-09-15T00:00:00Z",
        ),
        ("parent-approval", ("parents", "roeStatus"), "Approved"),
        (
            "parent-object",
            ("parents", "roeObjectIds"),
            data["parents"]["roeObjectIds"] + ["PRN-IAR12-004"],
        ),
        ("parent-binding", ("context", "parentBindingConfirmed"), True),
        ("parent-coverage", ("context", "parentCoverageChanged"), True),
        ("parent-scope", ("context", "parentScopeExpanded"), True),
        ("independent-case", ("context", "independentChapter11Case"), "CASE-2026-001"),
        ("principal-class", ("principals", 0, "principalClass"), "Workload"),
        ("principal-duplicate", ("principals", 1, "id"), "PRN-IAR12-001"),
        ("human-mfa-to-workload", ("principals", 3, "mfaStatus"), "Enabled"),
        (
            "class-as-value",
            ("principals", 0, "credentialClass"),
            "Bearer SYNTH-INVALID",
        ),
        ("edge-type", ("edges", 0, "kind"), "Access"),
        ("edge-endpoint", ("edges", 0, "toId"), "RES-IAR12-001"),
        ("issuer-RP", ("edges", 12, "issuerId"), "RP-IAR12-003"),
        ("audience-other-RP", ("edges", 12, "audienceId"), "RP-IAR12-002"),
        ("resource-RP", ("resources", 2, "relyingPartyId"), "RP-IAR12-002"),
        ("permission-resource", ("permissions", 2, "resourceId"), "RES-IAR12-002"),
        ("path-duplicate", ("paths", 1, "id"), "PTH-IAR12-001"),
        ("path-dangling", ("paths", 3, "principalId"), "PRN-IAR12-999"),
        ("path-chain", ("paths", 3, "edgeIds"), ["EDG-IAR12-013", "EDG-IAR12-012"]),
        (
            "path-cycle",
            ("paths", 3, "edgeIds"),
            ["EDG-IAR12-013", "EDG-IAR12-011", "EDG-IAR12-011", "EDG-IAR12-012"],
        ),
        ("path-empty", ("paths", 0, "edgeIds"), []),
        ("path-privilege", ("paths", 3, "requiredPermissionId"), "PER-IAR12-001"),
        ("path-wrong-action", ("paths", 3, "action"), "read-audit-summary"),
        ("static-promoted", ("paths", 1, "state"), "Validated"),
        ("MFA-only-broken", ("paths", 1, "state"), "Broken"),
        ("missing-condition-promoted", ("paths", 5, "state"), "Config-confirmed"),
        ("unknown-treated-safe", ("paths", 5, "state"), "Broken"),
        ("borrowed-config", ("paths", 3, "configEvidenceId"), "EVD-IAR12-002"),
        ("borrowed-event", ("paths", 3, "eventEvidenceId"), "EVT-IAR12-003"),
        ("missing-eval", ("paths", 3, "evaluationId"), None),
        ("real-method", ("paths", 3, "validationMethod"), "Real authentication"),
        ("graph-version", ("evaluations", 0, "graphRevision"), "GRAPH-IAR12-002"),
        ("policy-version", ("evaluations", 0, "policyRevision"), "POLICY-IAR12-002"),
        ("wrong-principal", ("evaluations", 0, "principalId"), "PRN-IAR12-003"),
        ("wrong-resource", ("evaluations", 0, "resourceId"), "RES-IAR12-002"),
        ("wrong-action", ("evaluations", 0, "action"), "read-audit-summary"),
        ("wrong-RP", ("evaluations", 0, "relyingPartyId"), "RP-IAR12-002"),
        ("wrong-issuer", ("evaluations", 0, "issuerId"), "RP-IAR12-003"),
        ("input-vector", ("evaluations", 0, "conditions"), []),
        ("actual-not-expected", ("evaluations", 0, "actual"), "Deny"),
        ("wrong-refutation", ("evaluations", 1, "refutedEdgeId"), None),
        ("no-denial-for-broken", ("edges", 8, "condition"), "True"),
        ("network", ("evaluations", 0, "networkRequests"), 1),
        ("authentication", ("evaluations", 0, "authenticationAttempts"), 1),
        ("event-unrelated", ("eventEvidence", 0, "pathId"), "PTH-IAR12-004"),
        ("source-evidence", ("evaluations", 0, "configEvidenceId"), "EVD-IAR12-005"),
        ("unowned-evidence", ("configEvidence",), data["configEvidence"][:-1]),
        ("finding-borrowed", ("findings", 0, "pathId"), "PTH-IAR12-002"),
        ("handoff-delivered", ("handoffs", 0, "status"), "delivered"),
        ("handoff-execution", ("handoffs", 1, "executionAuthorized"), True),
        ("record-real-claim", ("record", "authoredNotMeasured"), False),
        ("unbounded-minutes", ("limits", "minutes"), 31),
        ("empty-budget", ("limits", "outputBytes"), 0),
        ("retention", ("limits", "retentionHours"), 25),
        ("unsafe-statement", ("record", "question"), "実Credentialを再利用する。"),
        ("external-host", ("record", "question"), "https://production.example.com/"),
    ]
    for label, path, value in negatives:
        bad(label, path, value)
    # Two coordinated edits cannot turn a guessed result into a true comparison.
    d = deepcopy(data)
    d["evaluations"][0].update(expected="Deny", actual="Deny")
    check("CH12-EVAL-coordinated-result-not-proof", bool(validate(d)))
    for i, raw in enumerate(
        (b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}', b"\xff", b"{"), 1
    ):
        try:
            strict_bytes(raw)
            rejected = False
        except (ValueError, UnicodeError, ManifestError):
            rejected = True
        check(f"CH12-JSON-{i}", rejected)
    for i, value in enumerate(
        ("20260915T000000Z", "2026-9-15T00:00:00Z", "2026-09-15T00:00:00+00:00", True),
        1,
    ):
        try:
            utc(value)
            rejected = False
        except (ValueError, TypeError):
            rejected = True
        check(f"CH12-TIME-{i}", rejected)
    s = deepcopy(schema)
    s["unevaluatedProperties"] = False
    check("CH12-SCHEMA-unsupported-keyword", bool(validate(s=s)))
    for path in (
        "scripts/chapter12_semantics.py",
        "scripts/check_chapter12_contract.py",
        "scripts/chapter12_regressions.py",
    ):
        tree = ast.parse((ROOT / path).read_text(encoding="utf-8"))
        calls = [
            n
            for n in ast.walk(tree)
            if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute)
            and n.func.attr in ("read_text", "write_text")
        ]
        check(
            "CH12-UTF8-" + path,
            all(
                any(
                    k.arg == "encoding"
                    and isinstance(k.value, ast.Constant)
                    and k.value.value == "utf-8"
                    for k in n.keywords
                )
                for n in calls
            ),
        )
    for di, doc in enumerate(projection.documents, 1):
        spec = contract["documents"][doc.document_id]
        check(f"CH12-DOC-{di}-canonical", not document_errors(doc, spec, data))
        pairs = list(relations(doc))
        for ri, required in enumerate(spec["required"], 1):
            index = next(i for i, (_, r) in enumerate(pairs) if r == required)
            removed = replace(doc, fields=doc.fields[:index] + doc.fields[index + 1 :])
            check(
                f"CH12-DOC-{di}-required-{ri}",
                bool(document_errors(removed, spec, data)),
            )
        for family in ("hostProvenance", "analyticProvenance"):
            for ei, relation in enumerate(spec[family], 1):
                index = next(i for i, (_, r) in enumerate(pairs) if r == relation)
                f = doc.fields[index]
                text = f.text + (
                    " 実Credentialを再利用する。"
                    if family == "analyticProvenance"
                    else " https://production.example.com/"
                )
                changed = replace(f, text=text, normalized_text=text)
                probes = {
                    "changed": replace(
                        doc,
                        fields=doc.fields[:index]
                        + (changed,)
                        + doc.fields[index + 1 :],
                    ),
                    "moved": replace(
                        doc, fields=(f,) + doc.fields[:index] + doc.fields[index + 1 :]
                    ),
                    "duplicate": replace(
                        doc, fields=doc.fields[:index] + (f,) + doc.fields[index:]
                    ),
                    "missing": replace(
                        doc, fields=doc.fields[:index] + doc.fields[index + 1 :]
                    ),
                }
                for label, probe in probes.items():
                    check(
                        f"CH12-EX-{di}-{family}-{ei}-{label}",
                        bool(scan_document(probe, spec, True)),
                    )
                expected = (
                    f"{doc.document_id}: exact provenance cardinality: expected 1, observed 0; "
                    f"entry={key(relation)}"
                )
                check(
                    f"CH12-DIAG-{di}-{family}-{ei}",
                    expected in scan_document(probes["missing"], spec, True),
                )
        # Complete whole-document selection, not per-chapter syntax variants.
        path = doc.document_id
        old = source[path]
        for where, pos in (
            ("preamble", 0),
            ("body", old.index("\n## ")),
            ("tail", len(old)),
        ):
            mutated = (
                old[:pos] + "\n\n実Credentialを再利用する。\n\n" + old[pos:]
            ).rstrip() + "\n"
            probe = project_documents({path: mutated}).documents[0]
            check(f"CH12-SURFACE-{di}-{where}", bool(scan_document(probe, spec)))
        safe = project_documents(
            {path: old + "\n実Credentialを再利用しない。\n"}
        ).documents[0]
        check(f"CH12-SURFACE-{di}-prohibition", not scan_document(safe, spec, True))
        drift = project_documents(
            {path: old + "\n## Unexpected Chapter12 section\n\n説明。\n"}
        ).documents[0]
        check(f"CH12-SURFACE-{di}-drift", bool(document_errors(drift, spec, data)))
    unsupported = project_documents(
        {DOCUMENTS[0]: source[DOCUMENTS[0]] + "\n{% include unknown.html %}\n"}
    ).documents[0]
    check("CH12-SURFACE-shared-failclosed", bool(unsupported.diagnostics))
    # Validate source identity on the existing token vocabulary, not substring.
    chapter = projection.documents[0]
    spec = contract["documents"][DOCUMENTS[0]]
    for si, sid in enumerate(SOURCE_IDS, 1):
        for scope in ("body", "references", "both"):
            for suffix in ("x", "X", "2", "_x"):
                fields = []
                for f, relation in relations(chapter):
                    in_refs = "参考文献・Source Note ID" in relation["headings"]
                    if scope == "both" or (scope == "references") == in_refs:
                        f = replace(
                            f,
                            text=f.text.replace(sid, sid + suffix),
                            normalized_text=f.normalized_text.replace(
                                sid, sid + suffix
                            ),
                        )
                    fields.append(f)
                check(
                    f"CH12-SOURCE-{si}-{scope}-{suffix}",
                    "Chapter12 body/reference Source ownership"
                    in document_errors(
                        replace(chapter, fields=tuple(fields)), spec, data
                    ),
                )
        fields = tuple(
            replace(
                f,
                text=f.text.replace(sid, "(" + sid + ")"),
                normalized_text=f.normalized_text.replace(sid, "(" + sid + ")"),
            )
            for f in chapter.fields
        )
        check(
            f"CH12-SOURCE-{si}-punctuation",
            "Chapter12 body/reference Source ownership"
            not in document_errors(replace(chapter, fields=fields), spec, data),
        )
    text = source[DOCUMENTS[0]]
    start, end = text.index("**Purpose:**"), text.index("\n1. Caseを見る前")
    blocks = text[start:end].strip().split("\n\n")
    check("CH12-ORDER-five-owned-blocks", len(blocks) == 5)
    if len(blocks) == 5:
        for late in range(4):
            order = [i for i in range(5) if i != late] + [late]
            changed = (
                text[:start] + "\n\n".join(blocks[i] for i in order) + "\n" + text[end:]
            )
            doc = project_documents({DOCUMENTS[0]: changed}).documents[0]
            check(
                f"CH12-ORDER-{late}-after-command",
                "Chapter12 exercise explanations before command"
                in document_errors(doc, spec, data),
            )
    # Exhaustively compare every owned displayed leaf. Use the parity component
    # directly to avoid quadratic repeated Policy scanning of unchanged fields.
    case = projection.documents[2]
    rows = [
        (i, f)
        for i, f in enumerate(case.fields)
        if is_policy_scan_field(f) and f.element_kind == "table_row"
    ]
    for ri, (i, f) in enumerate(rows, 1):
        changed = replace(
            f, text=f.text + " changed", normalized_text=f.normalized_text + " changed"
        )
        doc = replace(case, fields=case.fields[:i] + (changed,) + case.fields[i + 1 :])
        check(f"CH12-PARITY-{ri}", bool(case_parity_errors(doc, data)))
        if ri == 1:
            check(
                "CH12-PARITY-integrated",
                "ART20 complete JSON/projected Case parity"
                in document_errors(doc, contract["documents"][DOCUMENTS[2]], data),
            )
    scratch = ROOT / ".work"
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ch12-tests-", dir=scratch) as directory:
        root = Path(directory)
        for relative in INPUTS:
            p = root / relative
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes((ROOT / relative).read_bytes())
        for relative in INPUTS:
            p = root / relative
            raw = p.read_bytes()
            check("CH12-IO-positive-" + relative, read_regular(root, relative) == raw)
            p.unlink()
            p.symlink_to(ROOT / relative)
            try:
                read_regular(root, relative)
                rejected = False
            except (ValueError, OSError):
                rejected = True
            check("CH12-IO-symlink-" + relative, rejected)
            p.unlink()
            p.write_bytes(raw)
        p = root / DATA_PATH
        original = p.read_bytes()
        for label, raw in (("empty", b""), ("oversize", b" " * (1024 * 1024 + 1))):
            p.write_bytes(raw)
            try:
                read_regular(root, DATA_PATH)
                rejected = False
            except (ValueError, OSError):
                rejected = True
            check("CH12-IO-" + label, rejected)
        p.unlink()
        os.mkfifo(p)
        try:
            read_regular(root, DATA_PATH)
            rejected = False
        except (ValueError, OSError):
            rejected = True
        check("CH12-IO-fifo", rejected)
        p.unlink()
        p.write_bytes(original)
        ancestor, saved = root / "cases/fixtures", root / "saved-fixtures"
        ancestor.rename(saved)
        ancestor.symlink_to(saved, target_is_directory=True)
        try:
            read_regular(root, DATA_PATH)
            rejected = False
        except (ValueError, OSError):
            rejected = True
        check("CH12-IO-ancestor", rejected)
        ancestor.unlink()
        saved.rename(ancestor)
        for name in ("O_NOFOLLOW", "O_NONBLOCK"):
            with patch.object(os, name, None):
                try:
                    read_regular(root, DATA_PATH)
                    rejected = False
                except ValueError:
                    rejected = True
            check("CH12-IO-platform-" + name, rejected)
        for value in (
            "../outside.json",
            "/absolute.json",
            "cases/fixtures/unowned.json",
        ):
            try:
                read_regular(root, value)
                rejected = False
            except ValueError:
                rejected = True
            check("CH12-IO-inventory-" + value, rejected)
        for relative in (
            "package.json",
            "site-pages.json",
            "references/sources.json",
            *contract["indices"],
        ):
            p = root / relative
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes((ROOT / relative).read_bytes())
        check("CH12-REPO-positive", not repository_errors(contract, root))
        p = root / "package.json"
        baseline = json.loads(p.read_text(encoding="utf-8"))
        for mode in ("missing", "after-generator"):
            d = deepcopy(baseline)
            cmd = "python3 scripts/check_chapter12_contract.py --no-regressions"
            d["scripts"]["sync:docs"] = d["scripts"]["sync:docs"].replace(
                cmd + " && ", ""
            )
            if mode == "after-generator":
                d["scripts"]["sync:docs"] += " && " + cmd
            p.write_text(json.dumps(d), encoding="utf-8")
            check(
                "CH12-REPO-preflight-" + mode, bool(repository_errors(contract, root))
            )
        p.write_text(json.dumps(baseline), encoding="utf-8")
    return len(ids), errors
