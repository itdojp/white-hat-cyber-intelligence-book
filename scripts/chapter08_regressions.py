"""Finite ART-18 counterexamples. Generic syntax fixtures remain in Layer B.

Families: schema/identity, state/stop, evidence/lineage, path/IO,
selection/provenance/JSON parity, source/preflight/navigation compatibility.
Each bounded probe has an ID; no unbounded fuzz grammar or runtime operation.
"""

from contextlib import redirect_stdout
from copy import deepcopy
from dataclasses import replace
import hashlib
from io import StringIO
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

from scripts.chapter08_semantics import (
    PATHS,
    STATES,
    RUN_IDS,
    IDENTITY,
    ARCHITECTURE,
    EVIDENCE_IDENTITY,
    RUN_BOUNDARIES,
    encoded,
    generate_receipts,
    strict_bytes,
    read_artifact,
    evaluate,
    utc,
    json_safety,
    validate_bundle,
)
from scripts.check_editorial_input_manifest import (
    ManifestError,
    validate_schema_instance,
    validate_supported_schema_nodes,
)


def run_regressions(data, raw, schemas, parents, contract, source, projection):
    from scripts import check_chapter08_contract as chapter
    from scripts.publication_projection import project_documents, is_policy_scan_field

    root, documents = chapter.ROOT, chapter.DOCUMENTS
    count, errors = 0, []

    def check(ok, label):
        nonlocal count
        count += 1
        if not ok:
            errors.append("CH08 regression " + label)

    def rejects(call):
        try:
            call()
        except (ValueError, TypeError, KeyError, OSError, UnicodeError, ManifestError):
            return True
        return False

    def validate(values, *, byte_data=raw, parent_data=parents):
        return validate_bundle(*values, byte_data, schemas, parent_data)

    def change(index, path, value):
        values = deepcopy(data)
        node = values[index]
        for part in path[:-1]:
            node = node[part]
        node[path[-1]] = value
        check(bool(validate(values)), f"CH08-DATA {index}/{path!r}/{value!r}")

    check(not validate(data), "CH08-POS canonical complete bundle")
    check(
        tuple(data[0]["states"]) == STATES and len(STATES) == 8,
        "CH08-STATE-001 eight states incl Running",
    )
    for i, value in enumerate(data):
        check(not json_safety(value, manifest=i == 2), f"CH08-JSON-POS-{i}")
        for invalid in (None, [], True, 0, "raw"):
            values = deepcopy(data)
            values[i] = invalid
            check(bool(validate(values)), f"CH08-SCHEMA-ROOT-{i}-{invalid!r}")

        # All required closed object fields, including every repeated record.
        def schema_objects(node, spec, path=()):
            if isinstance(node, dict):
                for field in node:
                    variant = deepcopy(node)
                    del variant[field]
                    check(
                        rejects(lambda: validate_schema_instance(variant, spec)),
                        f"CH08-REQUIRED-{i}-{path!r}-{field}",
                    )
                variant = deepcopy(node)
                variant["unownedField"] = "SYNTH-UNOWNED"
                check(
                    rejects(lambda: validate_schema_instance(variant, spec)),
                    f"CH08-CLOSED-{i}-{path!r}",
                )
                for field in node:
                    yield from schema_objects(
                        node[field], spec["properties"][field], path + (field,)
                    )
            elif isinstance(node, list):
                for j, item in enumerate(node):
                    yield from schema_objects(item, spec["items"], path + (j,))
            yield None

        list(schema_objects(value, schemas[i]))
    for schema in schemas:
        unknown = deepcopy(schema)
        unknown["allOf"] = []
        check(
            rejects(lambda: validate_supported_schema_nodes(unknown, "ART18", unknown)),
            "CH08-SCHEMA unsupported keyword",
        )
    for text in (
        '{"a":1,"a":2}',
        '{"v":NaN}',
        '{"v":Infinity}',
        '{"v":-Infinity}',
        "{",
        "\ufeff{}",
    ):
        check(
            rejects(lambda: strict_bytes(text.encode("utf-8"))),
            "CH08-STRICT " + repr(text),
        )
    check(rejects(lambda: strict_bytes(b"\xff")), "CH08-STRICT non UTF8")
    for value in (
        "2026-09-13T00:00:00",
        "2026-09-13T00:00:00+00:00",
        "2026-9-13T00:00:00Z",
        "2026-02-30T00:00:00Z",
        None,
        True,
    ):
        check(rejects(lambda: utc(value)), "CH08-TIME " + repr(value))
    for k in IDENTITY:
        change(0, (k,), "SYNTH-WRONG")
    for k, value in ARCHITECTURE.items():
        change(
            0,
            ("architecture", k),
            (not value) if isinstance(value, bool) else "SYNTH-WRONG",
        )
    for k in EVIDENCE_IDENTITY:
        change(2, (k,), "SYNTH-WRONG")
    for i in range(3):
        for k in RUN_BOUNDARIES:
            change(0, ("runs", i, k), "SYNTH-WRONG")
        for k in (
            "runId",
            "planId",
            "labId",
            "executionStepId",
            "signalFlowId",
            "priorityRecordId",
            "stopId",
            "cleanupId",
            "reassessmentId",
            "evidenceArtifactId",
            "owner",
            "reviewer",
            "parentCoverage",
            "parentGapId",
            "scope",
        ):
            change(0, ("runs", i, k), "SYNTH-UNRELATED")
        for k in ("receiptIds", "signalIds", "assetIds", "boundaryIds"):
            change(0, ("runs", i, k), ["SYNTH-UNRELATED"])
        for k in ("executionAuthorized", "completedNormally", "cleanupVerified"):
            change(0, ("runs", i, "expected", k), not data[0]["runs"][i]["expected"][k])
        for k in ("verdict", "finalStatus"):
            change(0, ("runs", i, "expected", k), "Unowned state")
        change(
            0,
            ("runs", i, "expected", "statusHistory"),
            ["Planned", "Running", "Cleanup verified"],
        )
        change(0, ("runs", i, "startsAt"), "2027-09-13T00:00:00Z")
        change(0, ("runs", i, "endsAt"), "2026-09-13T00:00:00Z")
    for k in ("synthetic", "runtimeExecuted"):
        change(0, (k,), int(data[0][k]))
    for parent_i, field in (
        (0, "mapId"),
        (1, "recordSetId"),
        (0, "authorizationRecordId"),
        (1, "scope"),
    ):
        p = deepcopy(parents)
        p[parent_i][field] = "SYNTH-UNRELATED"
        check(bool(validate(data, parent_data=p)), f"CH08-PARENT-{parent_i}-{field}")
    # Every check has a bounded Fail and Unknown counterpart. No expected table
    # is used as the oracle for these transition assertions.
    safe = [r for r in data[1]["receipts"] if r["runId"] == RUN_IDS[0]]
    for n, original in enumerate(safe):
        for result in ("Fail", "Unknown"):
            rows = deepcopy(safe)
            rows[n]["result"] = result
            verdict = evaluate(rows)
            check(
                verdict["verdict"]
                == ("Unsafe" if result == "Fail" else "Inconclusive"),
                f"CH08-STATE-RESULT-{n}-{result}",
            )
            check(
                not verdict["completedNormally"] and not verdict["executionAuthorized"],
                f"CH08-STATE-NORMAL-{n}-{result}",
            )
            check(
                "Failed closed" in verdict["statusHistory"],
                f"CH08-STATE-CLOSED-{n}-{result}",
            )
            history = verdict["statusHistory"]
            failure = history.index("Failed closed")
            check(
                "Running" not in history[failure:], f"CH08-STATE-NO-RESUME-{n}-{result}"
            )
            stage = original["stage"]
            if stage == "preflight":
                check(
                    "Running" not in history
                    and verdict["skippedStages"] == ["runtime"],
                    f"CH08-PREFLIGHT-{n}-{result}",
                )
            elif stage == "runtime":
                check(
                    history.index("Running") < failure < history.index("Stopped")
                    and verdict["cleanupVerified"],
                    f"CH08-RUNTIME-{n}-{result}",
                )
            elif stage in ("stop", "export", "destroy"):
                expected_skip = {
                    "stop": ["export", "destroy", "cleanup"],
                    "export": ["destroy", "cleanup"],
                    "destroy": ["cleanup"],
                }[stage]
                check(
                    verdict["skippedStages"] == expected_skip
                    and not verdict["cleanupVerified"]
                    and verdict["finalStatus"] == "Failed closed",
                    f"CH08-STOP-ORDER-{n}-{result}",
                )
            else:
                check(
                    not verdict["cleanupVerified"]
                    and verdict["finalStatus"] == "Failed closed",
                    f"CH08-CLEANUP-{n}-{result}",
                )
    mixed = deepcopy(safe)
    mixed[8]["result"] = "Fail"
    mixed[-1]["result"] = "Unknown"
    report = evaluate(mixed)
    check(
        report["verdict"] == "Unsafe"
        and report["failureReceiptIds"] == [mixed[8]["receiptId"]]
        and report["unknownReceiptIds"] == [mixed[-1]["receiptId"]]
        and not report["cleanupVerified"],
        "CH08-STATE-PRIORITY Fail retained across Unknown cleanup",
    )
    # Unvisited future failures cannot become observations or make a verdict.
    rows = deepcopy(safe)
    rows[0]["result"] = "Unknown"
    rows[8]["result"] = "Fail"
    report = evaluate(rows)
    check(
        report["verdict"] == "Inconclusive"
        and report["failureReceiptIds"] == []
        and report["skippedStages"] == ["runtime"],
        "CH08-STATE-SKIPPED no synthetic Pass/Fail inference",
    )
    for rows in (safe[:-1], safe + [safe[-1]], list(reversed(safe))):
        check(rejects(lambda: evaluate(rows)), "CH08-STATE missing/duplicate/order")
    for field, value in (
        ("runId", RUN_IDS[1]),
        ("receiptId", safe[1]["receiptId"]),
        ("result", "Absent"),
        ("stage", "unowned"),
    ):
        rows = deepcopy(safe)
        rows[0][field] = value
        check(rejects(lambda: evaluate(rows)), f"CH08-STATE-INVENTORY-{field}")
    # Actual bytes AND fixed recipe, not self-asserted hashes or equivalent JSON.
    for bad_raw in (raw + b"\n", raw.replace(b"\n", b"\r\n"), b"{}\n"):
        values = deepcopy(data)
        values[2]["sha256"] = hashlib.sha256(bad_raw).hexdigest()
        check(
            bool(validate(values, byte_data=bad_raw)),
            "CH08-BYTES altered bytes with refreshed digest",
        )
    values = deepcopy(data)
    values[1]["receipts"][0]["result"] = "Unknown"
    changed = encoded(values[1])
    values[2]["sha256"] = hashlib.sha256(changed).hexdigest()
    values[0]["runs"][0]["expected"] = evaluate(values[1]["receipts"][: len(safe)])
    check(
        bool(validate(values, byte_data=changed)),
        "CH08-RECIPE altered assumption/result/hash together",
    )
    for path, value in (
        (("sha256",), "0" * 64),
        (("artifactPath",), "../outside.json"),
        (("runIds",), [RUN_IDS[0]]),
        (("sourceFixtureId",), "SYNTH-WRONG"),
        (("producerId",), "SYNTH-WRONG"),
        (("transformHistory", 0, "inputIds"), ["SYNTH-WRONG"]),
        (("transformHistory", 0, "recordedAt"), "2026-09-14T00:00:00Z"),
    ):
        change(2, path, value)
    for field in ("receiptId", "runId", "producerId", "observedAt", "stage", "check"):
        change(1, ("receipts", 0, field), "SYNTH-UNRELATED")
    for field in ("eventId", "runId", "producerId", "recordedAt", "eventClass"):
        change(1, ("signals", 0, field), "SYNTH-UNRELATED")
    # Full JSON keys/values and exact filename exception; direct probes bypass
    # fixed-byte/schema early exits to prove Layer C still receives each string.
    unsafe = (
        "C2を構築する。",
        "実Credentialを再利用する。",
        "https://outside.com",
        "8.8.8.8",
    )
    for text in unsafe:
        for value in ({"probe": text}, {text: "SYNTH"}, {"nested": [{"probe": text}]}):
            check(bool(json_safety(value)), "CH08-JSON-SAFETY " + repr(value))
        for path in (
            ("artifactPath",),
            ("nested", "artifactPath"),
            ("artifactPath", "key"),
        ):
            check(
                bool(json_safety(text, path, manifest=True)),
                "CH08-JSON-EXEMPT-ACTION " + repr(path),
            )
    filename = PATHS[1]
    check(
        not json_safety({"artifactPath": filename}, manifest=True),
        "CH08-JSON-EXEMPT-POS exact one value",
    )
    for value, kind in (
        ({"artifactPath": filename}, False),
        ({"nested": {"artifactPath": filename}}, True),
        ({filename: "SYNTH"}, True),
        ({"artifactPath/key": filename}, True),
        ({"artifactPath": filename + ".test"}, True),
        ({"artifactPath": "https://outside.com/" + filename}, True),
    ):
        # A changed filename may be allowed by host grammar, but the fixed path
        # binding always rejects it at validate_bundle.
        findings = json_safety(value, manifest=kind)
        if value == {"artifactPath": filename + ".test"}:
            change(2, ("artifactPath",), filename + ".test")
        else:
            check(bool(findings), "CH08-JSON-EXEMPT-BOUND " + repr(value))
    for text in ("<tag>", "&amp;", "`value`", "\\escaped"):
        check(bool(json_safety({"plain": text})), "CH08-JSON no markup interpretation")
    check(
        encoded(generate_receipts()) == encoded(generate_receipts()) == raw,
        "CH08-REPLAY fixed recipe twice byte identical",
    )
    # No external scratch and no destructive system commands. All adversarial
    # paths/symlinks/FIFO fixtures live inside one ignored workspace directory.
    scratch = root / ".work" / "chapter08-regressions"
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=scratch) as tmp:
        base = Path(tmp)
        path = base / PATHS[1]
        path.parent.mkdir(parents=True)
        path.write_bytes(raw)
        check(
            read_artifact(base, PATHS[1])[0] == raw, "CH08-PATH positive regular UTF8"
        )
        for candidate in (
            "../outside.json",
            str(path),
            "./" + PATHS[1],
            PATHS[1].replace("/", "\\"),
            "cases/fixtures/unowned.json",
        ):
            check(
                rejects(lambda: read_artifact(base, candidate)),
                "CH08-PATH finite inventory " + candidate,
            )
        path.unlink()
        path.symlink_to(base / "not-present")
        check(rejects(lambda: read_artifact(base, PATHS[1])), "CH08-PATH leaf symlink")
        path.unlink()
        path.parent.rmdir()
        path.parent.symlink_to(base)
        check(
            rejects(lambda: read_artifact(base, PATHS[1])), "CH08-PATH ancestor symlink"
        )
        path.parent.unlink()
        path.parent.mkdir()
        for raw_variant in (b"", b"x" * (1024 * 1024 + 1), b"\xff", b'{"a":1,"a":2}'):
            path.write_bytes(raw_variant)
            check(
                rejects(lambda: read_artifact(base, PATHS[1])),
                "CH08-PATH invalid bytes/size",
            )
        path.unlink()
        path.mkdir()
        check(rejects(lambda: read_artifact(base, PATHS[1])), "CH08-PATH directory")
        path.rmdir()
        os.mkfifo(path)
        check(
            rejects(lambda: read_artifact(base, PATHS[1])),
            "CH08-PATH FIFO rejected nonblocking",
        )
        path.unlink()
        path.write_bytes(raw)
        alias = base / "alias"
        alias.symlink_to(base, target_is_directory=True)
        check(rejects(lambda: read_artifact(alias, PATHS[1])), "CH08-PATH root symlink")
    # Unsupported OS primitives must fail closed with a useful diagnostic,
    # not an unhandled AttributeError or a weaker fallback file reader.
    for flag in ("O_NOFOLLOW", "O_NONBLOCK"):
        with patch.dict(os.__dict__):
            delattr(os, flag)
            try:
                read_artifact(root, PATHS[1])
            except ValueError as exc:
                check("requires Linux/WSL2" in str(exc), "CH08-IO-006 missing " + flag)
            else:
                check(False, "CH08-IO-006 missing " + flag)
    check(
        "LinuxまたはWSL2のLinux環境上のPython 3.11以上" in source[documents[0]],
        "CH08-IO-007 supported environment prerequisite",
    )
    # Explicit encoding under ASCII process locale; production replay is read-only.
    before = {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in PATHS}
    env = {
        **os.environ,
        "LC_ALL": "C",
        "LANG": "C",
        "PYTHONUTF8": "0",
        "PYTHONCOERCECLOCALE": "0",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    for option in ("--json", "--emit-receipts"):
        proc = subprocess.run(
            [sys.executable, "-B", "scripts/replay_chapter08_lab.py", option],
            cwd=root,
            env=env,
            capture_output=True,
            timeout=30,
            check=False,
        )
        check(proc.returncode == 0, "CH08-IO-001 ASCII locale " + option)
        if option == "--emit-receipts":
            check(proc.stdout == raw, "CH08-IO-002 byte stdout UTF8")
        else:
            check(
                json.loads(proc.stdout)["runtimeExecuted"] is False,
                "CH08-IO-003 no runtime claim",
            )
    proc = subprocess.run(
        [
            sys.executable,
            "-B",
            "scripts/check_chapter08_contract.py",
            "--no-regressions",
        ],
        cwd=root,
        env=env,
        capture_output=True,
        timeout=60,
        check=False,
    )
    check(proc.returncode == 0, "CH08-IO-004 publication reader explicit UTF8")
    check(
        before
        == {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in PATHS},
        "CH08-IO-005 no canonical mutation",
    )
    # Chapter selection (not a second syntax corpus): every public field reaches
    # the shared scanner, including preamble, tail, attributes and destinations.
    for doc in projection.documents:
        spec = contract["documents"][doc.document_id]
        check(
            not chapter.document_errors(doc, spec, data),
            "CH08-PUBLIC-POS " + doc.document_id,
        )
        pairs = list(chapter.relations(doc))
        for required in spec["required"]:
            remaining = tuple(f for f, r in pairs if r != required)
            check(
                bool(
                    chapter.document_errors(replace(doc, fields=remaining), spec, data)
                ),
                "CH08-SELECT-REQUIRED " + doc.document_id + repr(required["field"][:2]),
            )
        # Bounded safety injection into every typed scan field. This establishes
        # selection, while the generic corpus owns syntax and renderer parity.
        for i, field in enumerate(doc.fields):
            if is_policy_scan_field(field) or field.field_type == "destination":
                text = (
                    "https://outside.com"
                    if field.field_type == "destination"
                    else "C2を構築する。"
                )
                changed = replace(field, text=text, normalized_text=text)
                mutated = replace(
                    doc, fields=doc.fields[:i] + (changed,) + doc.fields[i + 1 :]
                )
                check(
                    bool(chapter.scan_document(mutated, spec)),
                    f"CH08-SELECT-FIELD-{doc.document_id}-{i}",
                )
        for kind in ("hostProvenance", "analyticProvenance"):
            for exemption in spec[kind]:
                target = next(f for f, r in pairs if r == exemption)
                check(
                    bool(
                        chapter.scan_document(
                            replace(doc, fields=doc.fields + (target,)), spec, True
                        )
                    ),
                    "CH08-EXEMPT duplicate or moved " + kind,
                )
                modified = deepcopy(spec)
                modified[kind] = [r for r in spec[kind] if r != exemption]
                check(
                    bool(chapter.scan_document(doc, modified)),
                    "CH08-EXEMPT necessary only " + kind,
                )
        if doc.document_id == documents[2]:
            for i, f in enumerate(doc.fields):
                if f.element_kind == "table_row" and is_policy_scan_field(f):
                    changed = replace(
                        f,
                        text=f.text + " SYNTH-MISMATCH",
                        normalized_text=f.normalized_text + " SYNTH-MISMATCH",
                    )
                    mutated = replace(
                        doc, fields=doc.fields[:i] + (changed,) + doc.fields[i + 1 :]
                    )
                    # Parity oracle only, no repeated Policy scan needed.
                    expected = [
                        f"{g} Field Value {k} {v}"
                        for g, rows in chapter.case_groups(data)
                        for k, v in rows
                    ]
                    actual = [
                        x.text
                        for x in mutated.fields
                        if x.element_kind == "table_row" and is_policy_scan_field(x)
                    ]
                    check(actual != expected, "CH08-PARITY all Case rows " + str(i))
    # Actual source-to-projection checks, bounded to Layer A placement and one
    # unsupported shared diagnostic. No Chapter 8 renderer regex is introduced.
    for path in documents:
        original = source[path]
        for label, text in (
            ("preamble", "C2を構築する。\n\n" + original),
            ("tail", original + "\n\nC2を構築する。\n"),
            ("section", original + "\n\n## 未審査の追加区画\n\n合成Data。\n"),
            ("unsupported", original + "\n\n{% include outside.html %}\n"),
        ):
            doc = project_documents({path: text}).documents[0]
            check(
                bool(chapter.document_errors(doc, contract["documents"][path], data)),
                "CH08-SOURCE-" + label + "-" + path,
            )
    # Exact current consumer compatibility is exercised, not only the shared
    # date helper. Keep Chapter 25 historical baseline and null-date guard.
    from scripts import check_chapter25_contract as ch25

    original_loader = ch25.load_json
    for field, value, accept in [
        ("checkedAt", "2026-07-25", True),
        ("checkedAt", "2026-09-13", True),
        ("checkedAt", "2027-01-01", True),
        ("checkedAt", "2026-07-24", False),
        ("checkedAt", "20260913", False),
        ("checkedAt", True, False),
        ("publishedAt", "2022-01-01", False),
    ]:

        def changed_source(path):
            result = original_loader(path)
            if path == "references/sources.json":
                next(s for s in result["sources"] if s["id"] == "SRC-BERKELEY-001")[
                    field
                ] = value
            return result

        saved = ch25.ERRORS
        try:
            ch25.ERRORS = []
            with (
                patch.object(ch25, "load_json", side_effect=changed_source),
                redirect_stdout(StringIO()),
            ):
                result = ch25.main()
            check((result == 0) == accept, f"CH08-SRC-COMPAT-{field}-{value!r}")
        finally:
            ch25.ERRORS = saved
    original_loader = chapter.load_json_strict
    for i in range(3):
        for mode in ("remove", "after-generator", "duplicate"):

            def changed_package(path):
                result = original_loader(path)
                if path == root / "package.json":
                    steps = result["scripts"]["sync:docs"].split(" && ")
                    step = steps.pop(i)
                    if mode == "after-generator":
                        steps.append(step)
                    elif mode == "duplicate":
                        steps.insert(i, step)
                        steps.insert(i, step)
                    result["scripts"]["sync:docs"] = " && ".join(steps)
                return result

            with patch.object(chapter, "load_json_strict", side_effect=changed_package):
                check(
                    any(
                        "safety before publication" in e
                        for e in chapter.repository_errors(contract)
                    ),
                    f"CH08-PREFLIGHT-COMPAT-{i}-{mode}",
                )

    def wrong_navigation(path):
        result = original_loader(path)
        if path == root / "site-pages.json":
            next(p for p in result["pages"] if p["source"] == documents[0])["order"] = (
                60
            )
        return result

    with patch.object(chapter, "load_json_strict", side_effect=wrong_navigation):
        check(
            any("navigation" in e for e in chapter.repository_errors(contract)),
            "CH08-NAV-COMPAT 7 before 8 before 11",
        )
    return count, errors
