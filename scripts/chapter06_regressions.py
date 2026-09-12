"""Finite ART16/selection negatives. Generic renderer grammar stays in Layer B."""

from copy import deepcopy
from dataclasses import replace

from scripts.chapter06_semantics import STAGES, validate_case
from scripts.source_audit import meets_audit_baseline


def run_regressions(data, parent, contract, source):
    from scripts.check_chapter06_contract import (
        DOCUMENTS,
        CASE_PATH,
        scan_document,
        document_errors,
        json_safety,
        relations,
    )
    from scripts.publication_projection import project_documents, is_policy_scan_field

    errors = []
    count = 0

    def check(ok, label):
        nonlocal count
        count += 1
        if not ok:
            errors.append("regression " + label)

    def mutation(index, path, value, expected=None):
        d = deepcopy(data)
        target = d["flows"][index]
        for p in path[:-1]:
            target = target[p]
        target[path[-1]] = value
        result = validate_case(d, parent)
        check(
            bool(result) and (expected is None or any(expected in e for e in result)),
            f"SF-{index + 1}/{path}: {expected}",
        )

    check(not validate_case(data, parent), "canonical semantic positive")
    check(not json_safety(data), "canonical JSON safety")
    for key in data:
        d = deepcopy(data)
        del d[key]
        check(bool(validate_case(d, parent)), f"root missing {key}")
    for key in data["flows"][0]:
        d = deepcopy(data)
        del d["flows"][0][key]
        check(bool(validate_case(d, parent)), f"flow missing {key}")
    for val in (None, [], {}, "raw", True, 0):
        check(bool(validate_case(val, parent)), f"root malformed {val!r}")
    for i in range(6):
        for status in (*STAGES, "Unknown", "Normalized", "No compromise", None):
            if status != data["flows"][i]["coverage"]:
                mutation(i, ["coverage"], status)
        for field in (
            "parentBehaviorId",
            "parentTelemetryId",
            "parentGapId",
            "actorId",
            "eventId",
            "producerId",
            "consumerId",
            "gapId",
        ):
            mutation(i, [field], "SYNTH-WRONG-ID")
        for field in ("assetIds", "boundaryIds", "parentFlowIds"):
            mutation(i, [field], ["SYNTH-UNRELATED"])
        mutation(i, ["identityClass"], "Device", "identity/credential")
        mutation(
            i,
            ["credentialClass"],
            "interactive-authentication"
            if i in (1, 2, 5)
            else "workload-authentication",
            "identity/credential",
        )
        mutation(
            i, ["allowedConclusion"], "No log proves no event", "bounded conclusion"
        )
        mutation(i, ["owner"], "named-person", "synthetic owner")
        mutation(i, ["queryEndpoint"], "example.com", "bounded nonexecuting")
        mutation(i, ["correlationKeys"], ["accessToken"], "correlation/required")
        mutation(i, ["requiredFields"], ["synthetic"], "correlation/required")
        mutation(i, ["clockUncertaintySeconds"], True, "uncertainty shape")
        mutation(i, ["clockUncertaintySeconds"], -1, "uncertainty shape")
        mutation(i, ["clockUncertaintySeconds"], 60, "query window/clock")
        mutation(i, ["clockSource"], "unknown", "clock source")
        mutation(i, ["eventTime"], "2026-09-01T00:00:00", "timezone")
        mutation(i, ["queryStart"], "2026-09-01T00:00:00+00:00", "query window/clock")
        mutation(i, ["queryEnd"], "2026-09-01T00:00:02+00:00", "query window/clock")
        mutation(i, ["nodes", 0, "role"], "identity", "node/edge")
        mutation(
            i,
            ["edges", 0, "to"],
            data["flows"][(i + 1) % 6]["nodes"][1]["id"],
            "node/edge",
        )
        mutation(i, ["reviewDate"], "2026-09-01", "review deadline")
        mutation(i, ["reviewDate"], "2026-99-99", "review deadline")
        for j, receipt in enumerate(data["flows"][i]["receipts"]):
            mutation(
                i,
                ["receipts", j, "flowId"],
                data["flows"][(i + 1) % 6]["flowId"],
                "same-flow evidence",
            )
            mutation(i, ["receipts", j, "synthetic"], False, "synthetic receipt")
            mutation(
                i, ["receipts", j, "eventId"], "SYNTH-UNRELATED", "same-flow evidence"
            )
            mutation(
                i, ["receipts", j, "fieldNames"], ["synthetic"], "field/normalization"
            )
            mutation(
                i,
                ["receipts", j, "normalizationVersion"],
                "2.0.0",
                "field/normalization",
            )
            mutation(
                i, ["receipts", j, "recordedAt"], "2026-09-01T00:00:00", "timezone"
            )
        if data["flows"][i]["receipts"]:
            mutation(i, ["receipts"], data["flows"][i]["receipts"][1:])
        if i in (2, 3, 4):
            mutation(
                i, ["retentionEnd"], "2026-09-05T00:00:00+00:00", "retention expired"
            )
            mutation(
                i,
                ["receipts", 2, "recordedAt"],
                "2026-09-01T00:00:03+00:00",
                "current receipt",
            )
    for field, val in [
        ("id", "TEST-SF-004"),
        ("flowId", "SF-2026-004"),
        ("scope", "production"),
        ("version", "2.0.0"),
        ("expected", []),
        ("actual", []),
        ("result", "Inconclusive"),
    ]:
        mutation(4, ["test", field], val, "bounded replay")
    mutation(4, ["test"], None, "test required")
    mutation(3, ["test"], data["flows"][4]["test"], "no borrowed test")
    for idx, val in [
        (0, {"stage": "Unknown"}),
        (1, {"unexpected": "shape"}),
        (2, True),
        (3, []),
    ]:
        mutation(idx, ["test"], val, "test shape")
    for val in (
        "deploy phishing infrastructure",
        "実Tokenを再利用してください",
        "https://example.com",
        "<unsafe>",
        "&lt;unsafe&gt;",
    ):
        check(
            bool(json_safety(val, CASE_PATH + "/flows/2/operationPurpose")),
            f"JSON exemption changed {val}",
        )
    check(
        bool(
            json_safety(
                "Customer Data APIの合成利用記録",
                CASE_PATH + "/flows/1/operationPurpose",
            )
        ),
        "JSON descriptive exception relocated",
    )
    for value, expected in [
        ("2026-09-12", True),
        ("2027-01-01", True),
        ("2026-09-05", False),
        ("2026-9-12", False),
        (True, False),
        (None, False),
    ]:
        check(
            meets_audit_baseline(value, "2026-09-06") == expected,
            "parent audit date " + repr(value),
        )
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
    changed["flows"][0]["gap"] = "別の合成説明"
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
