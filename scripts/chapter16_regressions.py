"""Finite ART24 semantic and selection counterexamples; no syntax grammar."""

from copy import deepcopy
from dataclasses import replace
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

from scripts.chapter16_model import (
    DATA,
    DOCUMENTS,
    INPUTS,
    assess,
    digest,
    strict,
    read_regular,
    validate_model,
)
from scripts.check_editorial_input_manifest import (
    ManifestError,
    validate_schema_instance,
)
from scripts.check_chapter16_contract import (
    ROOT,
    inventory,
    scan_document,
    document_errors,
    case_errors,
)
from scripts.publication_projection import project_documents, is_policy_scan_field


def run_regressions(data, schema, contract, source, projection):
    checks, errors = [], []

    def check(label, ok):
        if label in checks:
            errors.append("duplicate ART24 regression: " + label)
        checks.append(label)
        if not ok:
            errors.append("failed ART24 regression: " + label)

    def rejected(fn):
        try:
            result = fn()
            return isinstance(result, list) and bool(result)
        except (ValueError, TypeError, KeyError, StopIteration, OSError, ManifestError):
            return True

    def outcome(row, req, fixture, receipts, original):
        try:
            return assess(row, req, fixture, receipts, original)
        except (ValueError, TypeError, KeyError):
            return "Rejected"

    check("TCM-H-NONEMPTY-BYTES-ARE-NOT-REJECTION", not rejected(lambda: b"accepted"))
    check(
        "TCM-H-NONEMPTY-JSON-IS-NOT-REJECTION", not rejected(lambda: {"accepted": True})
    )

    # Kernel tests deliberately do not invoke schema or frozen authored-input hashes.
    for i, row in enumerate(data["rows"]):
        q, f = data["requirements"][i], data["fixtures"][i]
        expected = row["coverage"], row["allowedConclusion"]
        check(
            f"TCM-K-BASE-{i:03}",
            outcome(row, q, f, data["receipts"], digest(f)) == expected,
        )
        for key in ("subjectId", "revision", "questionId", "fixtureId"):
            r = deepcopy(row)
            r[key] = "unbound"
            check(
                f"TCM-K-BIND-{i:03}-{key}",
                outcome(r, q, f, data["receipts"], digest(f)) == "Rejected",
            )
        for key, value in [
            ("timezone", "local"),
            ("clockSource", ""),
            ("clockUncertaintySeconds", -1),
            ("clockUncertaintySeconds", True),
            ("ingestDelaySeconds", -1),
            ("ingestDelaySeconds", True),
            ("schemaVersion", "unreviewed"),
            ("accessRole", "SYNTH-OTHER"),
            ("retentionEnd", row["retentionStart"]),
            ("retentionStart", "20260921T000000Z"),
        ]:
            r = deepcopy(row)
            r[key] = value
            check(
                f"TCM-K-QUALITY-{i:03}-{key}-{value}",
                outcome(r, q, f, data["receipts"], digest(f)) == "Rejected",
            )
    row, req, fixture = (
        deepcopy(data[k][0]) for k in ("rows", "requirements", "fixtures")
    )
    original = digest(fixture)
    expected_stages = [
        ("Required", "producer-evidence-missing"),
        ("Produced", "collector-evidence-missing"),
        ("Collected", "retention-evidence-missing"),
        ("Retained", "query-evidence-missing"),
        ("Validated", "bounded-input-contract-satisfied"),
    ]
    for n, expected in enumerate(expected_stages):
        r = deepcopy(row)
        r["receiptIds"] = r["receiptIds"][:n]
        check(
            f"TCM-K-STAGE-{n}",
            outcome(r, req, fixture, data["receipts"], original) == expected,
        )
    for n in range(4):
        r = deepcopy(row)
        r["receiptIds"].pop(n)
        actual = outcome(r, req, fixture, data["receipts"], original)
        check(
            f"TCM-K-MISSING-STAGE-{n}",
            actual == ("Retained", "query-evidence-missing")
            if n == 3
            else actual == "Rejected",
        )
    for field in ("rowId", "questionId", "fixtureId", "subjectId", "revision"):
        receipts = deepcopy(data["receipts"])
        receipts[0][field] = "another-record"
        check(
            "TCM-K-RECEIPT-" + field,
            outcome(row, req, fixture, receipts, original) == "Rejected",
        )
    for label, ids in [
        ("duplicate", [row["receiptIds"][0]] * 2),
        ("unknown", ["missing"]),
        ("reordered", list(reversed(row["receiptIds"]))),
        ("cross-row", data["rows"][1]["receiptIds"]),
    ]:
        r = deepcopy(row)
        r["receiptIds"] = ids
        check(
            "TCM-K-RECEIPTS-" + label,
            outcome(r, req, fixture, data["receipts"], original) == "Rejected",
        )
    for name, value, expected in [
        ("retentionEnd", "2026-09-21T00:30:00Z", ("Collected", "retention-gap")),
        ("retentionStart", "2026-09-21T00:01:00Z", ("Collected", "retention-gap")),
        ("clockUncertaintySeconds", 6, ("Queryable", "clock-uncertainty")),
        (
            "normalizerVersion",
            "NORM-TCM16-2",
            ("Queryable", "identity-normalization-mismatch"),
        ),
        (
            "identityNamespace",
            "SYNTH-OTHER",
            ("Queryable", "identity-normalization-mismatch"),
        ),
        ("ingestDelaySeconds", 61, ("Queryable", "ingest-delay")),
        ("processingBasis", "unknown", "Rejected"),
    ]:
        r = deepcopy(row)
        r[name] = value
        check(
            "TCM-K-STATE-" + name,
            outcome(r, req, fixture, data["receipts"], original) == expected,
        )
    # Boundary equality and stricter Consumer requirements are independent of receipts.
    for key, value in [
        ("clockUncertaintySeconds", 5),
        ("ingestDelaySeconds", 60),
        ("retentionEnd", "2026-09-22T00:00:00Z"),
    ]:
        r = deepcopy(row)
        r[key] = value
        check(
            "TCM-K-BOUNDARY-" + key,
            outcome(r, req, fixture, data["receipts"], original) == expected_stages[4],
        )
    q = deepcopy(req)
    q["requiredRetentionDays"] = 30
    check(
        "TCM-K-CONSUMER-RETENTION",
        outcome(row, q, fixture, data["receipts"], original)
        == ("Collected", "retention-gap"),
    )
    f = deepcopy(fixture)
    f["records"][0]["result"] = "changed"
    check(
        "TCM-K-ORIGINAL",
        outcome(row, req, f, data["receipts"], original)
        == ("Queryable", "original-byte-mismatch"),
    )
    # A trusted malformed original still cannot pass required-field/time semantics.
    for field in req["requiredFields"]:
        name = field["name"]
        for mode in ("missing", "null", "empty"):
            f = deepcopy(fixture)
            if mode == "missing":
                del f["records"][0][name]
            else:
                f["records"][0][name] = None if mode == "null" else ""
            check(
                f"TCM-K-FIELD-{name}-{mode}",
                outcome(row, req, f, data["receipts"], digest(f))
                == ("Queryable", "required-field-missing"),
            )
    for key, value, expected in [
        ("event_time", "2026-09-20T23:59:59Z", ("Queryable", "event-time-bounds")),
        ("observed_time", "2026-09-21T00:04:59Z", ("Queryable", "event-time-bounds")),
        ("ingest_time", "2026-09-21T00:06:01Z", ("Queryable", "ingest-delay")),
        ("ingest_time", "2026-09-21T01:00:01Z", ("Queryable", "event-time-bounds")),
        ("event_time", "20260921T000500Z", "Rejected"),
        ("target_workload_id", "APP-OTHER", "Rejected"),
        ("event_type", "unrelated", "Rejected"),
    ]:
        f = deepcopy(fixture)
        f["records"][0][key] = value
        check(
            "TCM-K-EVENT-" + key + "-" + value,
            outcome(row, req, f, data["receipts"], digest(f)) == expected,
        )
    for presence, records, complete, expected in [
        ("absent", [], True, ("Validated", "not-observed-in-synthetic-window")),
        ("absent", [], False, ("Queryable", "observation-coverage-unknown")),
        ("present", [], True, ("Queryable", "observation-coverage-unknown")),
        (
            "absent",
            fixture["records"],
            True,
            ("Queryable", "observation-coverage-unknown"),
        ),
    ]:
        f = deepcopy(fixture)
        f.update(
            eventPresence=presence, records=records, observationWindowComplete=complete
        )
        check(
            f"TCM-K-ABSENCE-{presence}-{bool(records)}-{complete}",
            outcome(row, req, f, data["receipts"], digest(f)) == expected,
        )

    # Closed shape: every authored object requires every field, at every array element.
    def walk(value, path=()):
        if isinstance(value, dict):
            yield path, value
            for k, v in value.items():
                yield from walk(v, path + (k,))
        elif isinstance(value, list):
            for i, v in enumerate(value):
                yield from walk(v, path + (i,))

    def at(value, path):
        for k in path:
            value = value[k]
        return value

    for path, obj in walk(data):
        label = "/".join(map(str, path)) or "root"
        for key in obj:
            d = deepcopy(data)
            del at(d, path)[key]
            check(
                "TCM-S-MISSING-" + label + "/" + key,
                rejected(lambda: validate_schema_instance(d, schema)),
            )
        d = deepcopy(data)
        at(d, path)["unreviewedField"] = True
        check(
            "TCM-S-EXTRA-" + label,
            rejected(lambda: validate_schema_instance(d, schema)),
        )
    for name in ("synthetic", "executionAuthorized", "readOnly", "networkRequired"):
        d = deepcopy(data)
        d[name] = not d[name]
        check(
            "TCM-M-SAFETY-" + name,
            rejected(lambda: validate_model(d, schema, contract)),
        )
    for i in range(10):
        for name, value in [
            ("coverage", "Validated"),
            ("allowedConclusion", "bounded-input-contract-satisfied"),
            ("validationEvidenceId", "EVD-UNBOUND"),
            ("gap", ""),
            ("owner", ""),
            ("dueAt", "2026-09-20T00:00:00Z"),
            ("reassessment", ""),
            ("integrityReference", "SYNTH-OTHER"),
        ]:
            if data["rows"][i][name] == value:
                continue
            d = deepcopy(data)
            d["rows"][i][name] = value
            check(
                f"TCM-M-CLAIM-{i}-{name}",
                rejected(lambda: validate_model(d, schema, contract)),
            )
    for i, handoff in enumerate(data["handoffs"]):
        for name, value in [
            ("status", "delivered"),
            ("receiptId", "EVD-UNBOUND"),
            ("rowIds", []),
            ("executionAuthorized", True),
        ]:
            d = deepcopy(data)
            d["handoffs"][i][name] = value
            check(
                f"TCM-M-HANDOFF-{i}-{name}",
                rejected(lambda: validate_model(d, schema, contract)),
            )
    for payload in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}', "\ufeff{}"):
        check("TCM-J-" + payload, rejected(lambda: strict(payload.encode())))

    # Complete preamble/body/tail, heading association, field order and host exclusions.
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
    projected = project_documents(probes)
    for doc in projected.documents:
        findings = scan_document(doc, {"hostProvenance": []})
        check(
            "TCM-P-ACTION-" + doc.document_id,
            any("target.real_or_external" in e for e in findings),
        )
    for doc in projection.documents:
        spec = contract["documents"][doc.document_id]
        check("TCM-P-CANON-" + doc.document_id, not document_errors(doc, spec, data))
        for label, fields in [
            ("missing", doc.fields[:-1]),
            ("duplicate", doc.fields + doc.fields[-1:]),
            ("reverse", tuple(reversed(doc.fields))),
        ]:
            changed = replace(doc, fields=fields)
            check(
                "TCM-P-INVENTORY-" + doc.document_id + "-" + label,
                bool(document_errors(changed, spec, data)),
            )
        for idx, f in enumerate(doc.fields):
            if f.element_kind == "heading" and is_policy_scan_field(f):
                fs = list(doc.fields)
                fs[idx] = replace(f, text="未審査の節", normalized_text="未審査の節")
                check(
                    "TCM-P-HEADING-" + f.location,
                    bool(document_errors(replace(doc, fields=tuple(fs)), spec, data)),
                )
        for item in spec["hostProvenance"]:
            idx = inventory(doc).index(item)
            f = doc.fields[idx]
            changed = replace(
                f,
                text="https://outside.invalid/",
                normalized_text="https://outside.invalid/",
            )
            fs = list(doc.fields)
            fs[idx] = changed
            check(
                "TCM-P-PROVENANCE-" + f.location,
                bool(scan_document(replace(doc, fields=tuple(fs)), spec)),
            )
    case = projection.documents[2]
    d = deepcopy(data)
    d["rows"][0]["gap"] = "新しい説明"
    check("TCM-P-LEAF-CHANGED", bool(case_errors(case, d)))
    for i, row in enumerate(data["rows"]):
        d = deepcopy(data)
        d["rows"][i]["gap"] = "実在する第三者システムにアクセスする。"
        check(
            f"TCM-P-JSON-ACTION-{i}",
            any(
                "target.real_or_external" in e
                for e in validate_model(d, schema, contract)
            ),
        )

    # Static bounded input IO, no arbitrary file/network/command parameter.
    work = ROOT / ".work"
    work.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ch16-regression-", dir=work) as temp:
        root = Path(temp)
        for p in INPUTS:
            target = root / p
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(b"{}")
            check("TCM-IO-REGULAR-" + p, read_regular(root, p) == b"{}")
            target.unlink()
            target.symlink_to(ROOT / DATA)
            check("TCM-IO-SYMLINK-" + p, rejected(lambda: read_regular(root, p)))
            target.unlink()
            target.write_bytes(b"{}")
        target = root / DATA
        for label, value in [("empty", b""), ("large", b"x" * (1024 * 1024 + 1))]:
            target.write_bytes(value)
            check("TCM-IO-" + label, rejected(lambda: read_regular(root, DATA)))
        target.unlink()
        target.mkdir()
        check("TCM-IO-DIRECTORY", rejected(lambda: read_regular(root, DATA)))
        target.rmdir()
        os.mkfifo(target)
        check("TCM-IO-FIFO", rejected(lambda: read_regular(root, DATA)))
        target.unlink()
        target.write_bytes(b"{}")
        for flag in ("O_NOFOLLOW", "O_NONBLOCK"):
            with patch.object(os, flag, create=False):
                delattr(os, flag)
                check(
                    "TCM-IO-PLATFORM-" + flag,
                    rejected(lambda: read_regular(root, DATA)),
                )
        for name in ("../README.md", "/etc/passwd", "cases/../README.md"):
            check(
                "TCM-IO-INVENTORY-" + name, rejected(lambda: read_regular(root, name))
            )
    return len(checks), errors
