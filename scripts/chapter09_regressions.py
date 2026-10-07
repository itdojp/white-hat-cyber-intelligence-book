"""Finite ART-02 counterexamples; generic syntax tests remain Layer B-owned."""

from copy import deepcopy
from dataclasses import replace
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

from scripts.chapter09_semantics import (
    DATA_PATH,
    REGULAR_PATHS,
    read_regular,
    STATES,
    ROLES,
    validate_record,
    conditions,
    read_input,
    strict_bytes,
    utc,
)
from scripts.check_chapter09_contract import (
    ROOT,
    DOCUMENTS,
    relations,
    document_errors,
    scan_document,
    canonical_errors,
    key,
)
from scripts.publication_projection import project_documents, is_policy_scan_field
from scripts.check_editorial_input_manifest import ManifestError
from scripts.source_audit import meets_audit_baseline


def set_value(data, path, value):
    target = data
    for k in path[:-1]:
        target = target[k]
    target[path[-1]] = value


def containers(value, path=()):
    if isinstance(value, dict):
        yield path, value
        for k, v in value.items():
            yield from containers(v, path + (k,))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from containers(v, path + (i,))


def run_regressions(data, schema, contract, source, projection):
    errors = []
    ids = set()

    def check(ident, ok):
        if ident in ids:
            errors.append("duplicate regression ID " + ident)
        ids.add(ident)
        if not ok:
            errors.append(ident + ": counterexample not rejected or positive rejected")

    def bad(ident, path, value, base=data):
        probe = deepcopy(base)
        set_value(probe, path, value)
        check(ident, bool(validate_record(probe, schema)))

    check(
        "CH09-POS-001", not validate_record(data, schema) and not canonical_errors(data)
    )
    check(
        "CH09-POS-002",
        len(conditions(data)) == 8 and data["executionAuthorized"] is False,
    )
    # Manufactured positive within the retained parent's original August 6 window.
    # Not an actual past approval or a backdated canonical record; no parent
    # interval is extended, and real executionAuthorized remains false.
    good = deepcopy(data)
    good["record"].update(status="Approved", asOf="2026-08-06T00:05:00Z")
    good["window"].update(
        startsAt="2026-08-06T00:00:00Z", endsAt="2026-08-06T00:30:00Z"
    )
    good["approval"].update(
        authorityStatus="Current",
        writtenEvidenceRef="SYNTH-AUTH-PROOF-ROE09-V1",
        approvedVersion=1,
        signoffs=list(ROLES),
    )
    check(
        "CH09-POS-003",
        not validate_record(good, schema)
        and not conditions(good)
        and good["executionAuthorized"] is False,
    )
    check("CH09-POS-004", bool(canonical_errors(good)))
    for status in STATES:
        probe = deepcopy(good)
        probe["record"]["status"] = status
        check(
            "CH09-STATE-" + status.replace(" ", "-"),
            not validate_record(probe, schema)
            and (not conditions(probe)) == (status in ("Approved", "Active")),
        )
    bad("CH09-AUTH-001", ("approval", "authorizationId"), "")
    for i, (path, value) in enumerate(
        [
            (("approval", "writtenEvidenceRef"), None),
            (("approval", "approvedVersion"), None),
            (("approval", "approvedVersion"), 2),
            (("approval", "approvedVersion"), True),
            (("approval", "signoffs"), list(ROLES)[:-1]),
            (("approval", "authorityStatus"), "Unknown"),
            (("approval", "authorityStatus"), "Expired"),
            (("approval", "authorityStatus"), "Revoked"),
            (("approval", "validUntil"), "2026-09-19T09:00:00Z"),
            (("window", "startsAt"), "2026-08-05T00:00:00Z"),
            (("window", "endsAt"), "2026-08-19T09:01:00Z"),
            (("record", "asOf"), "2026-08-06T00:30:00Z"),
            (("record", "asOf"), "2026-08-17T23:59:59Z"),
            (("record", "asOf"), "2026-08-19T09:00:00Z"),
            (("record", "version"), 2),
        ],
        1,
    ):
        bad(f"CH09-AUTH-{i + 1:03}", path, value, good)
    for i, kind in enumerate(("restart", "retest"), 1):
        p = deepcopy(good)
        p["change"]["kind"] = kind
        check(f"CH09-REAUTH-{i}-missing", bool(validate_record(p, schema)))
        if kind == "restart":
            p["change"].update(
                stopCleared=True, restartApprovalRef="SYNTH-RESTART-ROE09-V1"
            )
        else:
            p["change"]["retestApprovalRef"] = "SYNTH-RETEST-ROE09-V1"
        check(
            f"CH09-REAUTH-{i}-positive",
            not validate_record(p, schema) and not conditions(p),
        )
        p["record"]["version"] = 2
        check(f"CH09-REAUTH-{i}-stale", bool(validate_record(p, schema)))
    later = deepcopy(good)
    later["record"]["asOf"] = "2026-08-18T00:05:00Z"
    later["window"].update(
        startsAt="2026-08-18T00:00:00Z", endsAt="2026-08-18T00:30:00Z"
    )
    check(
        "CH09-AUTH-parent-test-window",
        bool(validate_record(later, schema))
        and "WINDOW-AUTHORITY" in conditions(later),
    )
    bad(
        "CH09-AUTH-parent-window-extension",
        ("parents", "authorizationWindowEndsAt"),
        "2026-08-19T09:00:00Z",
        good,
    )
    # Each object property is required and each object shape is closed.
    for i, (path, obj) in enumerate(containers(data), 1):
        for name in obj:
            p = deepcopy(data)
            target = p
            for k in path:
                target = target[k]
            del target[name]
            check(
                f"CH09-SCHEMA-{i:03}-missing-{name}", bool(validate_record(p, schema))
            )
        p = deepcopy(data)
        target = p
        for k in path:
            target = target[k]
        target["unowned-field"] = "sentinel"
        check(f"CH09-SCHEMA-{i:03}-extra", bool(validate_record(p, schema)))
    negatives = [
        (("synthetic",), False),
        (("executionAuthorized",), True),
        (("record", "status"), "Running"),
        (("record", "supersedes"), "ROE-2026-001"),
        (("record", "parentCaseId"), "CASE-2026-011"),
        (("parents", "authorizationRecordId"), "AUTH-OTHER"),
        (("parents", "authorizationConditions"), ["Satisfied"] * 3),
        (("parents", "authorizationExpiresAt"), "2027-08-19T09:00:00Z"),
        (("parents", "threatModelStatus"), "Approved"),
        (("parents", "parentStateChanged"), True),
        (("parents", "labExecutionAuthorized"), True),
        (("decision", "historicalDeadline"), "2026-09-13T00:00:00Z"),
        (("scope", "defaultDenied"), False),
        (("scope", "inScope", 0, "objectId"), "*"),
        (("scope", "inScope", 0, "owner"), "Unknown"),
        (("scope", "inScope", 0, "classification"), "Unknown"),
        (("scope", "inScope", 0, "thirdParty"), True),
        (("scope", "outOfScope"), data["scope"]["outOfScope"] + ["OBJ-ROE09-CONFIG"]),
        (
            ("scope", "inScope"),
            data["scope"]["inScope"] + [data["scope"]["inScope"][0]],
        ),
        (
            ("methods", "permitted"),
            data["methods"]["permitted"] + ["authentication-attempt"],
        ),
        (("methods", "prohibited"), data["methods"]["prohibited"][1:]),
        (("methods", "conditional"), ["undeclared-method"]),
        (("limits", "networkRequests"), 1),
        (("limits", "concurrency"), 2),
        (("limits", "retries"), 1),
        (("limits", "records"), 0),
        (("limits", "records"), 101),
        (("limits", "evidenceBytes"), 65537),
        (("limits", "minutes"), 31),
        (("limits", "minutes"), True),
        (("window", "timezone"), "Unknown"),
        (("data", "classification"), "Unknown"),
        (("data", "credentialMaterial"), "real"),
        (("data", "retentionHours"), 25),
        (("data", "custodian"), "Unknown"),
        (("stop", "primaryContact"), "Unknown"),
        (("stop", "backupContact"), "Unknown"),
        (("stop", "recoveryOwner"), "Unknown"),
        (("stop", "recoverySteps"), []),
        (("stop", "triggers"), data["stop"]["triggers"][:-1]),
        (("stop", "automaticRestart"), True),
        (("stop", "acknowledgementSeconds"), 0),
        (("stop", "cleanupStatus"), "verified"),
        (("evidence", "type"), "real-observation"),
        (("completion", "technicalStatus"), "completed"),
        (("completion", "decisionStatus"), "accepted"),
        (("change", "newApprovalRequired"), False),
        (("change", "resumeAutomatically"), True),
        (("handoffs", 0, "status"), "delivered"),
        (("handoffs", 0, "inputIds"), ["ROE-2026-011"]),
        (("boundary", "independentCase"), "CASE-2026-001"),
        (("objects", 0, "synthetic"), False),
        (("objects", 0, "value"), "実Credentialを再利用する。"),
        (("objects", 0, "value"), "https://production.example.com/"),
    ]
    for i, (path, value) in enumerate(negatives, 1):
        bad(f"CH09-SEM-{i:03}", path, value)
    # JSON strings use shared Policy, not filename/field-name safety waivers.
    p = deepcopy(data)
    p["objects"][0]["value"] = "供給された合成記録だけを読む。"
    check("CH09-POLICY-safe", not validate_record(p, schema))
    for i, raw in enumerate(
        (b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}', b"\xff", b"{"), 1
    ):
        try:
            strict_bytes(raw)
            rejected = False
        except (ValueError, UnicodeError, ManifestError):
            rejected = True
        check(f"CH09-JSON-{i}", rejected)
    for i, value in enumerate(
        (
            "20260818T000000Z",
            "2026-8-18T00:00:00Z",
            "2026-08-18T00:00:00",
            "2026-08-18T00:00:00+00:00",
            True,
        ),
        1,
    ):
        try:
            utc(value)
            rejected = False
        except (ValueError, TypeError):
            rejected = True
        check(f"CH09-TIME-{i}", rejected)
    # Typed output association: every required semantic field and exception
    # has one owner; removal, duplication and changed unsafe text fail closed.
    for di, doc in enumerate(projection.documents, 1):
        spec = contract["documents"][doc.document_id]
        check(f"CH09-DOC-{di}-canonical", not document_errors(doc, spec, data))
        pairs = list(relations(doc))
        for ri, relation in enumerate(spec["required"], 1):
            index = next(i for i, (_, r) in enumerate(pairs) if r == relation)
            removed = replace(doc, fields=doc.fields[:index] + doc.fields[index + 1 :])
            check(
                f"CH09-DOC-{di}-required-{ri}",
                bool(document_errors(removed, spec, data)),
            )
        for family in ("hostProvenance", "analyticProvenance"):
            for ei, relation in enumerate(spec[family], 1):
                index = next(i for i, (_, r) in enumerate(pairs) if r == relation)
                field = doc.fields[index]
                text = (
                    field.text + " 実Credentialを再利用する。"
                    if family == "analyticProvenance"
                    else (field.text + " https://production.example.com/")
                )
                changed = replace(field, text=text, normalized_text=text)
                mutated = replace(
                    doc,
                    fields=doc.fields[:index] + (changed,) + doc.fields[index + 1 :],
                )
                check(
                    f"CH09-EX-{di}-{family}-{ei}-changed",
                    bool(scan_document(mutated, spec)),
                )
                relocated = replace(
                    doc, fields=(field,) + doc.fields[:index] + doc.fields[index + 1 :]
                )
                check(
                    f"CH09-EX-{di}-{family}-{ei}-moved",
                    bool(scan_document(relocated, spec)),
                )
                duplicate = replace(
                    doc, fields=doc.fields[:index] + (field,) + doc.fields[index:]
                )
                check(
                    f"CH09-EX-{di}-{family}-{ei}-duplicate",
                    bool(scan_document(duplicate, spec)),
                )
                if di == 1 and ei == 1:
                    missing = replace(
                        doc, fields=doc.fields[:index] + doc.fields[index + 1 :]
                    )
                    for label, probe, count in (
                        ("missing", missing, 0), ("duplicate", duplicate, 2)
                    ):
                        expected = (
                            f"{doc.document_id}: exact provenance cardinality: "
                            f"expected 1, observed {count}; entry={key(relation)}"
                        )
                        check(
                            f"CH09-DIAG-{family}-{label}",
                            expected in scan_document(probe, spec, True),
                        )
    # Chapter-specific exercise order, using actual shared renderer output.
    # Keep source literals here only to mutate the one finite local exercise.
    path = DOCUMENTS[0]
    start = source[path].index("### ローカル検査\n\n") + len("### ローカル検査\n\n")
    end = source[path].index("### 成果物とRubric", start)
    blocks = source[path][start:end].strip().split("\n\n")
    check("CH09-BUILD-ORDER-inventory", len(blocks) == 4)
    if len(blocks) == 4:
        orders = {
            "historical": [0, 3, 1, 2],
            "prerequisites-late": [1, 2, 3, 0],
            "evidence-stop-late": [0, 2, 3, 1],
            "impact-cleanup-late": [0, 1, 3, 2],
        }
        for label, order in orders.items():
            text = (
                source[path][:start]
                + "\n\n".join(blocks[i] for i in order)
                + "\n\n"
                + source[path][end:]
            )
            doc = project_documents({path: text}).documents[0]
            check(
                "CH09-BUILD-ORDER-" + label,
                "Chapter9 exercise explanations before command"
                in document_errors(doc, contract["documents"][path], data),
            )
    # Direct source mutations prove preamble/body/tail really reach Layer B/C.
    for di, path in enumerate(DOCUMENTS, 1):
        for where in ("preamble", "body", "tail"):
            old = source[path]
            unsafe = "\n\n実Credentialを再利用する。\n\n"
            if where == "preamble":
                text = unsafe.lstrip() + old
            elif where == "tail":
                text = old.rstrip() + unsafe.rstrip() + "\n"
            else:
                pos = old.index("\n## ")
                text = old[:pos] + unsafe + old[pos:]
            doc = project_documents({path: text}).documents[0]
            check(
                f"CH09-SURFACE-{di}-{where}",
                bool(scan_document(doc, contract["documents"][path])),
            )
        doc = project_documents(
            {path: source[path] + "\n## Unexpected Chapter9 section\n\n説明。\n"}
        ).documents[0]
        check(
            f"CH09-SURFACE-{di}-section",
            bool(document_errors(doc, contract["documents"][path], data)),
        )
    # No parser variants here: one unsupported marker delegates fail-closed to B.
    doc = project_documents(
        {DOCUMENTS[0]: source[DOCUMENTS[0]] + "\n{% include unknown.html %}\n"}
    ).documents[0]
    check("CH09-SURFACE-unsupported", bool(doc.diagnostics))
    # Exact Case-to-JSON parity covers every serialized scalar/empty array.
    case = projection.documents[2]
    rows = [
        (i, f)
        for i, f in enumerate(case.fields)
        if is_policy_scan_field(f) and f.element_kind == "table_row"
    ]
    for ri, (index, f) in enumerate(rows, 1):
        p = replace(
            case,
            fields=case.fields[:index]
            + (
                replace(
                    f,
                    text=f.text + " changed",
                    normalized_text=f.normalized_text + " changed",
                ),
            )
            + case.fields[index + 1 :],
        )
        check(
            f"CH09-PARITY-{ri:03}",
            "ART02 complete JSON/projected Case parity"
            in document_errors(p, contract["documents"][DOCUMENTS[2]], data),
        )
    # IO tests stay in the repository's ignored workspace, never /tmp.
    scratch = ROOT / ".work"
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ch09-tests-", dir=scratch) as directory:
        base = Path(directory)
        for relative in REGULAR_PATHS:
            p = base / relative
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes((ROOT / relative).read_bytes())
        for relative in REGULAR_PATHS:
            check(
                "CH09-IO-positive-" + relative,
                read_regular(base, relative) == read_regular(ROOT, relative),
            )
            p = base / relative
            raw = p.read_bytes()
            p.unlink()
            p.symlink_to(ROOT / relative)
            try:
                read_regular(base, relative)
                rejected = False
            except (OSError, ValueError):
                rejected = True
            check("CH09-IO-symlink-" + relative, rejected)
            p.unlink()
            p.write_bytes(raw)
        p = base / DATA_PATH
        raw = p.read_bytes()
        for label, content in (("empty", b""), ("oversize", b" " * (1024 * 1024 + 1))):
            p.write_bytes(content)
            try:
                read_input(base, DATA_PATH)
                rejected = False
            except (OSError, ValueError):
                rejected = True
            check("CH09-IO-" + label, rejected)
        p.write_bytes(raw)
        p.unlink()
        os.mkfifo(p)
        try:
            read_regular(base, DATA_PATH)
            rejected = False
        except (OSError, ValueError):
            rejected = True
        check("CH09-IO-fifo", rejected)
        p.unlink()
        p.write_bytes(raw)
        ancestor = base / "cases" / "fixtures"
        moved = base / "saved-fixtures"
        ancestor.rename(moved)
        ancestor.symlink_to(moved, target_is_directory=True)
        try:
            read_regular(base, DATA_PATH)
            rejected = False
        except (OSError, ValueError):
            rejected = True
        check("CH09-IO-ancestor", rejected)
        ancestor.unlink()
        moved.rename(ancestor)
        for name in ("O_NOFOLLOW", "O_NONBLOCK"):
            with patch.object(os, name, None):
                try:
                    read_input(base, DATA_PATH)
                    rejected = False
                except ValueError:
                    rejected = True
            check("CH09-IO-platform-" + name, rejected)
        try:
            read_input(base, "../outside.json")
            rejected = False
        except ValueError:
            rejected = True
        check("CH09-IO-inventory", rejected)
    for i, (value, expected) in enumerate(
        (
            ("2026-08-05", True),
            ("2026-09-13", True),
            ("2026-08-04", False),
            ("20260805", False),
            ("2026-8-05", False),
            (True, False),
        ),
        1,
    ):
        check(
            f"CH09-SOURCE-DATE-{i}",
            meets_audit_baseline(value, "2026-08-05") is expected,
        )
    return len(ids), errors
