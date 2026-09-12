"""Closed ART-17 semantic/selection tests; generic publication grammar is Layer B."""

from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from copy import deepcopy
from dataclasses import replace
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from scripts.chapter07_semantics import (
    validate_case,
    TEXT_FIELDS,
    OPTIONAL_TEXT,
    OPTIONAL_NUMBER,
    LIST_FIELDS,
    SCENARIO_FIELDS,
    iso_date,
)


def run_regressions(
    data, parent, behaviors, snapshot, snapshot_digest, contract, source
):
    from scripts.check_chapter07_contract import (
        ROOT,
        DOCUMENTS,
        CASE_PATH,
        scan_document,
        document_errors,
        json_safety,
        relations,
    )
    from scripts.check_editorial_input_manifest import load_json_strict, ManifestError
    from scripts.publication_projection import project_documents, is_policy_scan_field
    from scripts.verify_chapter07_sources import verified

    count, errors = 0, []

    def check(ok, label):
        nonlocal count
        count += 1
        if not ok:
            errors.append("CH07 regression: " + label)

    def validate(d):
        return validate_case(d, parent, behaviors, snapshot, snapshot_digest)

    def mutation(i, field, value):
        d = deepcopy(data)
        d["records"][i][field] = value
        check(bool(validate(d)), f"record {i + 1}/{field}/{value!r}")

    check(not validate(data), "canonical semantic positive")
    check(not json_safety(data), "canonical JSON safety")
    for val in (None, [], {}, True, 0, "raw"):
        check(bool(validate(val)), f"root malformed {val!r}")
    for field in data:
        d = deepcopy(data)
        del d[field]
        check(bool(validate(d)), "root required " + field)
    for field in data["records"][0]:
        d = deepcopy(data)
        del d["records"][0][field]
        check(bool(validate(d)), "record required " + field)
    for field in TEXT_FIELDS:
        for value in (None, "", [], True):
            mutation(0, field, value)
    for field in OPTIONAL_TEXT:
        mutation(0, field, True)
    for field in OPTIONAL_NUMBER:
        for value in (True, "0.0", float("nan"), float("inf")):
            mutation(0, field, value)
    for field in LIST_FIELDS:
        for value in (None, "ID", [True], ["same", "same"]):
            mutation(0, field, value)
    for i in range(6):
        for field in SCENARIO_FIELDS:
            mutation(i, field, "Unsupported state")
        for field in (
            "recordId",
            "candidateId",
            "componentId",
            "componentVersion",
            "affectedRange",
            "attackPathId",
            "parentThreatId",
            "parentBehaviorId",
            "parentCoverage",
            "parentTelemetryId",
            "parentGapId",
            "cvssAssessment",
            "epssMeaning",
            "owner",
            "governanceOwner",
            "controlScope",
            "controlId",
            "gapId",
            "assetCriticality",
            "decisionConfidence",
            "requiredActionApplicability",
        ):
            mutation(i, field, "SYNTH-UNRELATED")
        for field in LIST_FIELDS:
            mutation(i, field, ["SYNTH-UNRELATED"])
        for field in (
            "cvssPairId",
            "cvssVersion",
            "cvssVector",
            "cvssNomenclature",
            "epssModelVersion",
            "epssModelIdentifier",
            "epssSnapshotDate",
            "kevCatalogVersion",
            "kevSnapshotDate",
            "controlEvidenceId",
        ):
            mutation(i, field, "wrong")
        for field in OPTIONAL_NUMBER:
            mutation(i, field, -1)
        for field in ("decisionDate", "dueDate", "nextReviewDate", "controlValidUntil"):
            mutation(i, field, "2021-12-24")
        d = deepcopy(data)
        d["records"][i]["synthetic"] = False
        check(bool(validate(d)), f"synthetic marker {i}")
    for i, e in enumerate(data["evidence"]):
        for field in e:
            d = deepcopy(data)
            del d["evidence"][i][field]
            check(bool(validate(d)), f"evidence required {i}/{field}")
        for field in ("id", "recordId", "kind", "scope", "recordedDate"):
            d = deepcopy(data)
            d["evidence"][i][field] = "SYNTH-UNRELATED"
            check(bool(validate(d)), f"evidence binding {i}/{field}")
        for field in e["claims"]:
            d = deepcopy(data)
            d["evidence"][i]["claims"][field] = "Unproven"
            check(bool(validate(d)), f"evidence claim {i}/{field}")
    d = deepcopy(data)
    d["evidence"][1] = deepcopy(d["evidence"][0])
    check(bool(validate(d)), "duplicate/borrowed evidence")
    d = deepcopy(data)
    d["records"].reverse()
    check(bool(validate(d)), "stable record order")
    d = deepcopy(data)
    d["sourceSnapshotSha256"] = "0" * 64
    check(bool(validate(d)), "source digest binding")
    for group, field in [("epss", "score"), ("kev", "catalogDueDate")]:
        s = deepcopy(snapshot)
        s[group]["rows"][0][field] = 0 if field == "score" else "2026-09-30"
        check(
            bool(validate_case(data, parent, behaviors, s, snapshot_digest)),
            "source value association " + group,
        )
    # Coherent positives: explanatory prose and a bounded future deadline may
    # evolve; the checker is not merely a whole-JSON hash or priority algorithm.
    d = deepcopy(data)
    d["records"][0]["decisionReason"] = (
        "別の合成Inventory根拠を説明し、導入変更時に再評価する。"
    )
    check(not validate(d) and not json_safety(d), "positive explanation change")
    d = deepcopy(data)
    d["records"][1]["dueDate"] = "2026-09-18"
    check(not validate(d), "positive deadline before verified expiry")
    for value, expected in [
        ("2026-09-12", True),
        ("20260912", False),
        ("2026-W37-6", False),
        ("2026-9-12", False),
        ("2026-02-30", False),
        (True, False),
    ]:
        check(bool(iso_date(value)) == expected, "strict date " + repr(value))
    for field in TEXT_FIELDS + OPTIONAL_TEXT:
        # Every textual record value is a scanner input; no field-level escape.
        d = deepcopy(data)
        d["records"][0][field] = "deploy phishing infrastructure"
        check(bool(json_safety(d)), "unsafe JSON " + field)
    for text in [
        "production.example.com",
        "<b>text</b>",
        "A &amp; B",
        "`code`",
        "back\\slash",
    ]:
        check(
            bool(json_safety(text, CASE_PATH + "/records/0/gap")),
            "closed plain data " + text,
        )
    check(
        not json_safety("Do not deploy phishing infrastructure."),
        "safe direct prohibition",
    )
    # Strict external input/UTF-8 behavior, with no /tmp or canonical mutation.
    scratch = ROOT / ".work"
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ch07-regression-", dir=scratch) as tmp:
        path = Path(tmp) / "input.json"
        for raw in [b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}', b"\xff"]:
            path.write_bytes(raw)
            try:
                load_json_strict(path)
            except (ValueError, ManifestError):
                check(True, "strict JSON negative")
            else:
                check(False, "strict JSON negative")
        path.write_bytes(b"inspected mathematical source")
        check(
            verified(path, hashlib.sha256(path.read_bytes()).hexdigest())
            == path.read_bytes(),
            "source hash positive",
        )
        try:
            verified(path, "0" * 64)
        except ValueError:
            check(True, "changed upstream bytes rejected before execution")
        else:
            check(False, "changed upstream bytes rejected before execution")
    locale_probe = subprocess.run(
        [sys.executable, "scripts/check_chapter07_contract.py", "--no-regressions"],
        cwd=ROOT,
        env={
            **os.environ,
            "LC_ALL": "C",
            "PYTHONUTF8": "0",
            "PYTHONCOERCECLOCALE": "0",
        },
        capture_output=True,
        encoding="utf-8",
        timeout=60,
        check=False,
    )
    check(
        locale_probe.returncode == 0
        and "Chapter 7 contract passed:" in locale_probe.stdout,
        "CH07-IO-001 explicit UTF-8 reads",
    )
    # Integration regression: newer scoped Source audits must not invalidate
    # Chapter11, while old/malformed dates and changed source meaning still fail.
    from scripts import check_chapter11_contract as ch11

    original_loader = ch11.load_json
    for value, expected in [
        ("2026-08-03", True),
        ("2026-09-12", True),
        ("2027-01-01", True),
        ("2026-08-02", False),
        ("20260912", False),
        (True, False),
        (None, False),
    ]:

        def source_override(path):
            result = original_loader(path)
            if path == "references/sources.json":
                next(x for x in result["sources"] if x["id"] == "SRC-OWASP-TOP10-001")[
                    "checkedAt"
                ] = value
            return result

        saved_errors = ch11.ERRORS
        try:
            ch11.ERRORS = []
            with (
                patch.object(ch11, "load_json", side_effect=source_override),
                redirect_stdout(StringIO()),
            ):
                outcome = ch11.main()
            check(
                (outcome == 0) == expected,
                "CH07-SRC-001 Chapter11 audit date " + repr(value),
            )
        finally:
            ch11.ERRORS = saved_errors

    def changed_version(path):
        result = original_loader(path)
        if path == "references/sources.json":
            next(x for x in result["sources"] if x["id"] == "SRC-OWASP-TOP10-001")[
                "version"
            ] = "2021"
        return result

    saved_errors = ch11.ERRORS
    try:
        ch11.ERRORS = []
        with (
            patch.object(ch11, "load_json", side_effect=changed_version),
            redirect_stdout(StringIO()),
        ):
            outcome = ch11.main()
        check(outcome != 0, "CH07-SRC-002 Chapter11 semantic version retained")
    finally:
        ch11.ERRORS = saved_errors
    projected = project_documents(source)
    for doc in projected.documents:
        spec = contract["documents"][doc.document_id]
        check(
            not document_errors(doc, spec, data),
            "canonical document " + doc.document_id,
        )
        # All three source positions reach Layer B and then Policy. No syntax
        # variations are implemented or reproduced by this chapter harness.
        text = source[doc.document_id]
        for place in ("preamble", "body", "tail"):
            for phrase, unsafe in [
                ("deploy phishing infrastructure", True),
                ("Do not deploy phishing infrastructure.", False),
            ]:
                lines = text.splitlines(keepends=True)
                if place == "preamble":
                    mut = phrase + "\n\n" + text
                elif place == "tail":
                    mut = text + "\n\n" + phrase + "\n"
                else:
                    at = (
                        next(
                            i for i, line in enumerate(lines) if line.startswith("## ")
                        )
                        + 1
                    )
                    # This is finite mutation placement, not publication parsing.
                    mut = (
                        "".join(lines[:at])
                        + "\n"
                        + phrase
                        + "\n\n"
                        + "".join(lines[at:])
                    )
                p = project_documents({doc.document_id: mut}).documents[0]
                result = scan_document(p, spec)
                check(
                    any("operation.c2_or_phishing" in e for e in result) == unsafe,
                    f"{doc.document_id} {place} shared scanner {unsafe}",
                )
        p = project_documents(
            {
                doc.document_id: text
                + "\n## Unexpected section\n\nRead the synthetic records.\n"
            }
        ).documents[0]
        check(
            any("finite H1/H2" in e for e in document_errors(p, spec, data)),
            "section drift " + doc.document_id,
        )
        required = spec["required"][0]
        remove = next(f for f, r in relations(doc) if r == required)
        altered = replace(doc, fields=tuple(f for f in doc.fields if f is not remove))
        check(
            bool(document_errors(altered, spec, data)),
            "required semantic removal " + doc.document_id,
        )
        # Every exception is non-expandable: exact cardinality, text and section.
        pairs = relations(doc)
        for kind, items in spec["exceptions"].items():
            for number, item in enumerate(items):
                field = next(f for f, r in pairs if r == item["relation"])
                at = doc.fields.index(field)
                doubled = replace(
                    doc, fields=doc.fields[:at] + (field,) + doc.fields[at:]
                )
                check(
                    bool(scan_document(doubled, spec, True)),
                    f"{kind} duplicate {doc.document_id}/{number}",
                )
                # Remove its section identity while preserving the suspect field.
                solo = replace(doc, fields=(field,))
                check(
                    bool(scan_document(solo, spec)),
                    f"{kind} moved {doc.document_id}/{number}",
                )
                bad_text = field.text + " deploy phishing infrastructure"
                changed_field = replace(field, text=bad_text, normalized_text=bad_text)
                changed_doc = replace(
                    doc,
                    fields=doc.fields[:at] + (changed_field,) + doc.fields[at + 1 :],
                )
                check(
                    bool(scan_document(changed_doc, spec, True)),
                    f"{kind} expanded {number}",
                )
        # Direct typed field evidence proves title/accessibility fields reach
        # Policy without adding a local syntax recognizer.
        f = next(f for f in doc.fields if is_policy_scan_field(f))
        malicious = replace(
            f,
            field_type="reader_visible_attribute",
            element_kind="link",
            attribute="title",
            text="deploy phishing infrastructure",
            normalized_text="deploy phishing infrastructure",
        )
        check(
            bool(scan_document(replace(doc, fields=(malicious,)), spec)),
            "attribute selection " + doc.document_id,
        )
    case_doc = projected.documents[2]
    changed = deepcopy(data)
    changed["records"][0]["gap"] = "別の合成説明"
    check(
        any(
            "JSON/projected" in e
            for e in document_errors(
                case_doc, contract["documents"][DOCUMENTS[2]], changed
            )
        ),
        "reader/JSON parity drift",
    )
    return count, errors
