"""Layer A: finite ART-15 synthetic data semantics, never Markdown parsing.

This is a teaching-set validator, not an ATT&CK mapper or a production detector.
The only executable classification is the three-record, no-I/O exercise.
"""

from __future__ import annotations

from scripts.source_audit import meets_audit_baseline

SNAPSHOT_SHA256 = "960d0b76b018bdefae3958beaaf3cc2a30d73c034467cbe0941289ded4f4d44a"
IDENTITY = {
    "teachingModel": "Office Suite teaching model only; parent product/environment remains unconfirmed.",
    "schemaVersion": "1.0.0",
    "synthetic": True,
    "artifactId": "ART-15",
    "mapId": "BMAP-2026-001",
    "parentCaseId": "CASE-2026-001",
    "relation": "refines",
    "parentThreatModelId": "TM-2026-001",
    "decisionRequirementId": "DR-2026-001",
    "authorizationRecordId": "AUTH-CASE-2026-001",
    "scope": "read-only-synthetic-data",
    "catalogVersion": "19.2",
    "sourceSnapshotSha256": SNAPSHOT_SHA256,
    "parentState": "Chapter 4 source snapshot retained; no parent hypothesis, control, gap or decision is updated.",
}
ROW_STRINGS = (
    "rowId threatId catalogVersion mappingBasis preconditions observableBehavior telemetryId "
    "status limitation alternativeMapping decisionContribution gapId owner reviewDate reassessmentTrigger"
).split()
ROW_ARRAYS = "assetIds boundaryIds flowIds analyticIds dataComponentIds evidenceIds controlIds".split()
ROW_NULLABLE = (
    "techniqueId tacticId subtechniqueId detectionId validationTestId".split()
)
SCHEMAS = {
    "controls": {
        **dict.fromkeys("controlId role assurance limitation".split(), "text"),
        "parentEvidenceIds": "texts",
    },
    "rows": {
        **dict.fromkeys(ROW_STRINGS, "text"),
        **dict.fromkeys(ROW_ARRAYS, "texts"),
        **dict.fromkeys(ROW_NULLABLE, "nullable"),
    },
    "evidence": {
        **dict.fromkeys("evidenceId rowId kind scope limitation".split(), "text"),
        "recordIds": "texts",
    },
    "telemetry": {
        **dict.fromkeys(
            "telemetryId rowId availability period missing owner".split(), "text"
        ),
        "requiredFields": "texts",
    },
    "events": {
        **dict.fromkeys("id eventClass tenant application".split(), "text"),
        "synthetic": "bool",
        "approval": "nullable",
    },
    "tests": {
        **dict.fromkeys(
            "testId rowId scope ruleVersion detectionId evidenceId result limitations".split(),
            "text",
        ),
        "expected": "texts",
        "actual": "texts",
    },
    "handoffs": {
        **dict.fromkeys("id input acceptance reject owner".split(), "text"),
        "chapters": "ints",
    },
}
IDS = {
    "controls": "controlId",
    "rows": "rowId",
    "evidence": "evidenceId",
    "telemetry": "telemetryId",
    "events": "id",
    "tests": "testId",
    "handoffs": "id",
}
REQUIRED_FIELDS = ["synthetic", "eventClass", "tenant", "application", "approval"]
STATUSES = {"Proposed", "Mapped", "Observed", "Validated", "Not applicable", "Unknown"}
BASES = {"Hypothesized", "Source-reported", "Observed", "Reproduced"}


def classify_synthetic_event(event: dict) -> str:
    """No network or settings changes; missing/unknown inputs never mean benign."""
    if (
        event.get("synthetic") is not True
        or event.get("eventClass") != "consent-change"
        or event.get("tenant") != "tenant-a.example"
        or event.get("application") != "billing-bridge.example"
    ):
        return "insufficient-data"
    return {"unapproved": "needs-review", "approved": "benign-change"}.get(
        event.get("approval") if isinstance(event.get("approval"), str) else None,
        "insufficient-data",
    )


def _typed(value: object, kind: str) -> bool:
    if kind == "text":
        return isinstance(value, str) and bool(value.strip())
    if kind == "nullable":
        return value is None or _typed(value, "text")
    if kind == "bool":
        return type(value) is bool
    if not isinstance(value, list):
        return False
    item_type = str if kind == "texts" else int
    return (
        all(type(item) is item_type for item in value)
        and len(value) == len(set(value))
        and (kind != "texts" or all(item.strip() for item in value))
    )


def structure_errors(data: object) -> list[str]:
    errors = []
    if not isinstance(data, dict) or set(data) != set(IDENTITY) | set(SCHEMAS):
        return ["ART-15 root property inventory"]
    for key, expected in IDENTITY.items():
        if type(data[key]) is not type(expected) or data[key] != expected:
            errors.append(f"identity {key}")
    for collection, schema in SCHEMAS.items():
        items = data[collection]
        if not isinstance(items, list) or not items:
            errors.append(f"{collection}: nonempty array required")
            continue
        for i, item in enumerate(items):
            if not isinstance(item, dict) or set(item) != set(schema):
                errors.append(f"{collection}[{i}]: property inventory")
                continue
            for key, kind in schema.items():
                if not _typed(item[key], kind):
                    errors.append(f"{collection}[{i}].{key}: expected {kind}")
        if not errors:
            values = [item[IDS[collection]] for item in items]
            if len(set(values)) != len(values):
                errors.append(f"{collection}: duplicate identifier")
    return errors


def validate_case(data: object, snapshot: dict, bindings: list[dict]) -> list[str]:
    """Check typed relationships before evaluating same-row status thresholds."""
    errors = structure_errors(data)
    if errors:
        return errors

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    indexes = {name: {item[IDS[name]]: item for item in data[name]} for name in SCHEMAS}
    objects = {item["externalId"]: item for item in snapshot["objects"]}
    require(len(data["rows"]) == len(bindings), "row inventory")
    for row, binding in zip(data["rows"], bindings):
        require(
            all(row[key] == value for key, value in binding.items()),
            f"{row['rowId']}: retained parent binding/status",
        )
    require(
        set(indexes["events"]) == {f"SYNTH-EVENT-BM-{i:03}" for i in range(1, 4)},
        "three synthetic record IDs",
    )
    for event in data["events"]:
        require(
            event["synthetic"] is True
            and event["eventClass"] == "consent-change"
            and event["tenant"] == "tenant-a.example"
            and event["application"] == "billing-bridge.example"
            and event["approval"] in ("approved", "unapproved", None),
            f"{event['id']}: synthetic event scope",
        )
    used_evidence, used_tests, used_telemetry = set(), set(), set()
    for row in data["rows"]:
        rid = row["rowId"]
        require(
            row["status"] in STATUSES and row["mappingBasis"] in BASES,
            f"{rid}: status/basis enum",
        )
        require(row["catalogVersion"] == "19.2", f"{rid}: catalog version")
        require(
            meets_audit_baseline(row["reviewDate"], "2026-09-06"), f"{rid}: review date"
        )
        require(row["owner"].startswith("SYNTH-"), f"{rid}: synthetic owner")
        require(row["gapId"] == "GAP-BM-" + rid[-3:], f"{rid}: separate gap")
        require(
            all(cid in indexes["controls"] for cid in row["controlIds"]),
            f"{rid}: parent control link",
        )
        technique = objects.get(row["techniqueId"])
        if row["techniqueId"] is not None:
            require(
                technique is not None
                and technique["type"] == "attack-pattern"
                and technique["deprecated"] is False
                and technique["revoked"] is False,
                f"{rid}: active technique",
            )
            tactic = objects.get(row["tacticId"])
            require(
                tactic is not None
                and tactic["type"] == "x-mitre-tactic"
                and technique is not None
                and tactic.get("shortname") in technique.get("tactics", []),
                f"{rid}: tactic relation",
            )
            require(row["subtechniqueId"] is None, f"{rid}: T1671 has no subtechnique")
            require(
                bool(row["analyticIds"])
                and all(
                    a in objects["DET0539"]["analyticIds"] for a in row["analyticIds"]
                ),
                f"{rid}: strategy/analytic relation",
            )
            components = sorted(
                {
                    c
                    for a in row["analyticIds"]
                    if a in objects
                    for c in objects[a].get("dataComponentIds", [])
                }
            )
            require(
                row["dataComponentIds"] == components,
                f"{rid}: analytic/component relation",
            )
        else:
            require(
                row["tacticId"] is None
                and row["subtechniqueId"] is None
                and not row["analyticIds"]
                and not row["dataComponentIds"]
                and row["status"] in {"Proposed", "Unknown", "Not applicable"},
                f"{rid}: no invented mapping",
            )
        tel = indexes["telemetry"].get(row["telemetryId"])
        used_telemetry.add(row["telemetryId"])
        require(
            tel is not None
            and tel["rowId"] == rid
            and tel["requiredFields"] == REQUIRED_FIELDS
            and tel["owner"] == row["owner"]
            and tel["period"]
            == "3-record teaching set only; no historical retention claim",
            f"{rid}: telemetry ownership/period/fields",
        )
        evidence = [indexes["evidence"].get(eid) for eid in row["evidenceIds"]]
        used_evidence.update(row["evidenceIds"])
        require(
            all(
                e is not None
                and e["rowId"] == rid
                and e["recordIds"]
                and all(r in indexes["events"] for r in e["recordIds"])
                for e in evidence
            ),
            f"{rid}: same-row evidence",
        )
        if row["status"] == "Observed":
            require(
                row["mappingBasis"] == "Observed"
                and bool(evidence)
                and all(
                    e is not None
                    and e["kind"] == "synthetic-observation"
                    and e["scope"] == "synthetic-consent-change-only"
                    for e in evidence
                )
                and row["observableBehavior"] == "合成記録で同意変更が記録された",
                f"{rid}: observed proposition/evidence",
            )
        if row["status"] in {"Observed", "Validated"}:
            require(
                tel is not None and tel["availability"] == "Synthetic only",
                f"{rid}: observed telemetry",
            )
        else:
            require(
                not evidence
                and tel is not None
                and tel["availability"] == "Not collected",
                f"{rid}: unobserved evidence/data",
            )
        if row["status"] == "Validated":
            test = indexes["tests"].get(row["validationTestId"])
            used_tests.add(row["validationTestId"])
            require(
                row["mappingBasis"] == "Reproduced"
                and len(evidence) == 1
                and test is not None,
                f"{rid}: validation prerequisites",
            )
            if test is not None and len(evidence) == 1 and evidence[0] is not None:
                ev = evidence[0]
                result = [
                    classify_synthetic_event(indexes["events"][eid])
                    for eid in ev["recordIds"]
                    if eid in indexes["events"]
                ]
                require(
                    test["rowId"] == rid
                    and test["scope"] == ev["scope"] == "synthetic-field-classification"
                    and test["evidenceId"] == ev["evidenceId"]
                    and ev["kind"] == "synthetic-test-result"
                    and test["ruleVersion"] == "1.0.0"
                    and test["detectionId"] == row["detectionId"] == "DET-BM-004"
                    and test["result"] == "Pass"
                    and test["expected"] == test["actual"] == result
                    and result
                    == ["needs-review", "benign-change", "insufficient-data"],
                    f"{rid}: same-row replay/Pass/conditions",
                )
                require(
                    "synthetic-field-classification" in row["limitation"]
                    and "親Control" in row["limitation"],
                    f"{rid}: validation limit",
                )
        else:
            require(
                row["validationTestId"] is None and row["detectionId"] is None,
                f"{rid}: no validation promotion",
            )
    for collection, used in (
        ("evidence", used_evidence),
        ("tests", used_tests),
        ("telemetry", used_telemetry),
    ):
        require(set(indexes[collection]) == used, f"{collection}: no unowned records")
    require(
        [(h["id"], h["chapters"]) for h in data["handoffs"]]
        == [("HO-BM-006", [6, 16]), ("HO-BM-017", [17, 18, 21]), ("HO-BM-026", [26])],
        "finite handoff inventory",
    )
    return errors
