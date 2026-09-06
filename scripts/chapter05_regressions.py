"""Bounded Chapter 5 selection/semantic regressions; generic syntax is Layer B's."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace

from scripts.chapter05_semantics import classify_synthetic_event, validate_case
from scripts.source_audit import meets_audit_baseline


def run_regressions(
    case: dict, snapshot: dict, contract: dict, source: dict
) -> tuple[int, list[str]]:
    from scripts.check_chapter05_contract import (
        DOCUMENTS,
        document_errors,
        relations,
        scan_document,
    )
    from scripts.publication_projection import project_documents

    errors, count = [], 0

    def check(condition: bool, label: str) -> None:
        nonlocal count
        count += 1
        if not condition:
            errors.append(f"regression {label}")

    def mutation(collection, index, field, value, expected):
        data = deepcopy(case)
        data[collection][index][field] = value
        result = validate_case(data, snapshot, contract["parentBindings"])
        check(
            any(expected in e for e in result),
            f"{collection}/{index}/{field}={value!r}: {expected}",
        )

    for status in ("Mapped", "Unknown", "Not applicable", "Proposed", "Invalid", None):
        mutation(
            "rows",
            3,
            "status",
            status,
            "status" if status is not None else "expected text",
        )
    for result in ("Fail", "Inconclusive", "Not collected", "pass"):
        mutation("tests", 0, "result", result, "same-row replay")
    for field, value in (
        ("expected", []),
        ("actual", ["benign-change"]),
        ("ruleVersion", "2.0.0"),
        ("scope", "production"),
        ("rowId", "BM-2026-002"),
        ("evidenceId", "EVD-BM-002"),
        ("detectionId", "DET0539"),
    ):
        mutation("tests", 0, field, value, "same-row replay")
    for field, value, expected in (
        ("evidenceIds", [], "validation prerequisites"),
        ("evidenceIds", ["EVD-BM-002"], "same-row evidence"),
        ("validationTestId", None, "validation prerequisites"),
        ("mappingBasis", "Hypothesized", "validation prerequisites"),
        ("subtechniqueId", "T1671.001", "no subtechnique"),
        ("techniqueId", "TA0003", "active technique"),
        ("tacticId", "TA0001", "tactic relation"),
        ("analyticIds", ["AN1488"], "analytic/component relation"),
        ("dataComponentIds", ["DC0038"], "analytic/component relation"),
        ("catalogVersion", "19.1", "catalog version"),
        ("gapId", "GAP-BM-002", "separate gap"),
        ("reviewDate", "2026-08-31", "review date"),
        ("owner", "real-owner", "synthetic owner"),
        ("limitation", "all detections validated", "validation limit"),
    ):
        mutation("rows", 3, field, value, expected)
    for field, value, expected in (
        ("evidenceIds", [], "observed proposition"),
        ("evidenceIds", ["EVD-BM-004"], "same-row evidence"),
        ("observableBehavior", "T1671による侵害が発生した", "observed proposition"),
        ("mappingBasis", "Source-reported", "observed proposition"),
    ):
        mutation("rows", 1, field, value, expected)
    for field, value in (("kind", "public-report"), ("scope", "production")):
        mutation("evidence", 0, field, value, "observed proposition")
    mutation("evidence", 0, "recordIds", ["missing-record"], "same-row evidence")
    mutation("evidence", 1, "recordIds", ["SYNTH-EVENT-BM-001"], "same-row replay")
    for field, value in (
        ("availability", "Not collected"),
        ("availability", "Unknown"),
    ):
        mutation("telemetry", 3, field, value, "observed telemetry")
    for field, value in (
        ("rowId", "BM-2026-003"),
        ("requiredFields", ["eventClass"]),
        ("period", "90 days covered"),
    ):
        mutation("telemetry", 3, field, value, "telemetry ownership")
    mutation("events", 0, "approval", "approved", "same-row replay")
    mutation("events", 0, "synthetic", False, "synthetic event scope")
    mutation("events", 0, "tenant", "live.example", "synthetic event scope")
    for field in ("tenant", "application", "eventClass", "approval", "synthetic"):
        event = deepcopy(case["events"][0])
        del event[field]
        check(
            classify_synthetic_event(event) == "insufficient-data",
            f"missing event {field}",
        )
    check(
        [classify_synthetic_event(e) for e in case["events"]]
        == ["needs-review", "benign-change", "insufficient-data"],
        "safe/near-miss/missing replay",
    )
    for collection in (
        "rows",
        "tests",
        "events",
        "telemetry",
        "evidence",
        "handoffs",
        "controls",
    ):
        data = deepcopy(case)
        data[collection].append(deepcopy(data[collection][0]))
        check(
            bool(validate_case(data, snapshot, contract["parentBindings"])),
            f"duplicate {collection}",
        )
        data = deepcopy(case)
        data[collection][0]["unowned"] = "extra"
        check(
            bool(validate_case(data, snapshot, contract["parentBindings"])),
            f"unknown property {collection}",
        )
    for field in (
        "parentState",
        "scope",
        "relation",
        "sourceSnapshotSha256",
        "synthetic",
    ):
        data = deepcopy(case)
        data[field] = "changed"
        check(
            any(
                "identity" in e
                for e in validate_case(data, snapshot, contract["parentBindings"])
            ),
            f"identity {field}",
        )
    for value, expected in (
        ("2026-08-03", True),
        ("2026-09-06", True),
        ("2026-08-02", False),
        ("20260906", False),
        ("2026-W36-7", False),
        ("2026-09-31", False),
        (None, False),
        (True, False),
        ("2026-09-06T00:00:00Z", False),
    ):
        check(
            meets_audit_baseline(value, "2026-08-03") is expected,
            f"source audit date {value!r}",
        )

    # Mutation sources retain the canonical publication rewrite while using
    # unique document IDs. Tests assert actual Policy rejection, not incidental
    # semantic inventory drift. No generic renderer syntax corpus is duplicated.
    mutations, logical, expectations = {}, {}, {}
    unsafe = "実Credentialを取得する。"
    for i, path in enumerate(DOCUMENTS):
        original = source[path]
        first, rest = original.split("\n", 1)
        variants = {
            "preamble": unsafe + "\n\n" + original,
            "body": first + "\n\n" + unsafe + "\n" + rest,
            "tail": original.rstrip() + "\n\n" + unsafe + "\n",
            "safe": original.rstrip() + "\n\n実Credentialを取得しない。\n",
            "heading": original.rstrip()
            + "\n\n## 未定義の第5章Section\n\n安全な説明。\n",
        }
        for label, text in variants.items():
            docid = f"ch05-probe-{i}-{label}"
            mutations[docid] = text
            logical[docid] = path
            expectations[docid] = label
    projected = project_documents(mutations, publication_sources=logical)
    for document in projected.documents:
        path = logical[document.document_id]
        label = expectations[document.document_id]
        spec = contract["documents"][path]
        found = scan_document(document, spec)
        if label in {"preamble", "body", "tail"}:
            check(
                any("secret.credential" in e for e in found),
                f"{path} {label} Policy forwarding",
            )
        elif label == "safe":
            check(not found, f"{path} safe prohibition")
        else:
            check(
                any(
                    "inventory drift" in e
                    for e in document_errors(document, spec, case)
                ),
                f"{path} section drift",
            )

    from scripts.extract_chapter05_attack_snapshot import extract

    try:
        extract(b'{"objects": []}')
    except ValueError:
        check(True, "source extraction rejects unpinned bytes")
    else:
        check(False, "source extraction rejects unpinned bytes")
    canonical = project_documents(source)
    for doc in canonical.documents:
        spec = contract["documents"][doc.document_id]
        from scripts.publication_projection import is_policy_scan_field

        baseline = next(f for f in doc.fields if is_policy_scan_field(f))
        for field_type, element_kind, attribute, text in (
            ("reader_visible_attribute", "attribute", "title", unsafe),
            ("destination", "a", "href", "https://unapproved.invalid.net/"),
        ):
            forwarded = replace(
                baseline,
                field_type=field_type,
                element_kind=element_kind,
                attribute=attribute,
                text=text,
                normalized_text=text,
                metadata=(),
                ordinal=max(f.ordinal for f in doc.fields) + 1,
            )
            check(
                bool(
                    scan_document(replace(doc, fields=doc.fields + (forwarded,)), spec)
                ),
                f"{doc.document_id} {field_type} Policy forwarding",
            )
        # Chapter-local exemption ownership is tested on projected fields; the
        # shared generic corpus separately proves that source creates them.
        for kind in ("action", "host", "destination"):
            for exemption in spec["exceptions"][kind]:
                pair = next(
                    (f for f, r in relations(doc) if r == exemption["relation"]), None
                )
                check(pair is not None, f"{doc.document_id} owned {kind} exception")
                if pair is None:
                    continue
                duplicate = replace(
                    pair, ordinal=max(f.ordinal for f in doc.fields) + 1
                )
                mutated = replace(doc, fields=doc.fields + (duplicate,))
                check(
                    bool(scan_document(mutated, spec)),
                    f"{doc.document_id} duplicate/moved {kind} rejected",
                )
        # Exact identity changes must not keep a former safe exception active.
        for kind in ("action", "host"):
            for exemption in spec["exceptions"][kind]:
                field = next(f for f, r in relations(doc) if r == exemption["relation"])
                suffix = " " + (
                    unsafe if kind == "action" else "https://unapproved.invalid.net/"
                )
                fields = tuple(
                    replace(
                        f,
                        text=f.text + suffix,
                        normalized_text=f.normalized_text + suffix,
                    )
                    if f.ordinal == field.ordinal
                    else f
                    for f in doc.fields
                )
                check(
                    bool(scan_document(replace(doc, fields=fields), spec)),
                    f"{doc.document_id} {kind} exception cannot expand",
                )
    return count, errors
