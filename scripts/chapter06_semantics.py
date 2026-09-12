"""ART-16 Layer A: finite synthetic Signal Flow semantics, no source parser.

Not a product log validator, detector, or permission grant. All receipts are
explicitly synthetic teaching assertions; replay checks their finite linkage.
"""

from __future__ import annotations

from datetime import datetime, timedelta

STAGES = ("Produced", "Collected", "Retained", "Queryable", "Validated")
ROLES = (
    "actor",
    "identity",
    "request",
    "gateway",
    "authorization",
    "effect",
    "producer",
    "collector",
    "normalizer",
    "retention",
    "query",
    "consumer",
)
REQUIRED_FIELDS = [
    "synthetic",
    "eventId",
    "actorId",
    "identityClass",
    "eventTime",
    "tenant",
    "application",
    "requestId",
    "authorizationResult",
]
IDENTITY = {
    "schemaVersion": "1.0.0",
    "synthetic": True,
    "artifactId": "ART-16",
    "mapId": "SFM-2026-001",
    "parentCaseId": "CASE-2026-001",
    "relation": "refines",
    "parentThreatModelId": "TM-2026-001",
    "parentBehaviorMapId": "BMAP-2026-001",
    "decisionRequirementId": "DR-2026-001",
    "authorizationRecordId": "AUTH-CASE-2026-001",
    "scope": "read-only-synthetic-data",
    "parentState": "Independent synthetic teaching supplement; no parent observation, control, gap or decision is changed.",
}
FLOW_TEXT = """flowId parentBehaviorId parentTelemetryId parentGapId actorId identityClass
credentialClass protocolClass plane operationPurpose authenticationResult authorizationResult
effect producerId eventId eventClass collectorId queryEndpoint consumerId telemetryId coverage
eventTime assessmentTime retentionStart retentionEnd queryStart queryEnd clockSource gapId gap allowedConclusion
alternative confidence owner reviewDate reassessment""".split()
FLOW_LIST = "assetIds boundaryIds parentFlowIds correlationKeys requiredFields".split()
FLOW_KEYS = set(
    FLOW_TEXT
    + FLOW_LIST
    + ["detectionId", "clockUncertaintySeconds", "nodes", "edges", "receipts", "test"]
)
RECEIPT_KEYS = set(
    "id synthetic flowId eventId stage recordedAt fieldNames normalizationVersion".split()
)
TEST_KEYS = set("id flowId scope version expected actual result".split())
PARENT_ROWS = [2, 6, 3, 2, 4, 5]
ACTORS = ["Human", "Service", "Workload", "Human", "Human", "Workload"]
ALLOWED_CONCLUSION = (
    "同一Flowの合成受領記録が示す段階だけ。Eventや侵害の不存在は判断しない。"
)


def timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        result = datetime.fromisoformat(value)
        return (
            result
            if result.tzinfo is not None and result.isoformat() == value
            else None
        )
    except ValueError:
        return None


def shape_errors(data: object) -> list[str]:
    """Closed shape before all semantic accesses; values are never executable."""
    if not isinstance(data, dict) or set(data) != set(IDENTITY) | {"flows"}:
        return ["ART16 root shape"]
    if any(type(data[k]) is not type(v) or data[k] != v for k, v in IDENTITY.items()):
        return ["ART16 synthetic identity/parent-state/scope"]
    if not isinstance(data["flows"], list) or len(data["flows"]) != 6:
        return ["ART16 six-flow inventory"]
    for f in data["flows"]:
        if not isinstance(f, dict) or set(f) != FLOW_KEYS:
            return ["ART16 flow closed shape"]
        if any(not isinstance(f[k], str) or not f[k].strip() for k in FLOW_TEXT):
            return ["ART16 flow text shape"]
        for k in FLOW_LIST:
            if (
                not isinstance(f[k], list)
                or not f[k]
                or any(not isinstance(v, str) or not v for v in f[k])
                or len(f[k]) != len(set(f[k]))
            ):
                return ["ART16 unique text list shape"]
        if (
            type(f["clockUncertaintySeconds"]) is not int
            or not 0 <= f["clockUncertaintySeconds"] <= 3600
        ):
            return ["ART16 clock uncertainty shape"]
        if f["detectionId"] is not None and not isinstance(f["detectionId"], str):
            return ["ART16 detection shape"]
        for collection, keys in (
            ("nodes", {"id", "role"}),
            ("edges", {"id", "from", "to"}),
        ):
            if not isinstance(f[collection], list) or not f[collection]:
                return ["ART16 graph shape"]
            if any(
                not isinstance(x, dict)
                or set(x) != keys
                or any(not isinstance(v, str) or not v for v in x.values())
                for x in f[collection]
            ):
                return ["ART16 graph item shape"]
        if not isinstance(f["receipts"], list):
            return ["ART16 receipt list shape"]
        for r in f["receipts"]:
            if (
                not isinstance(r, dict)
                or set(r) != RECEIPT_KEYS
                or r["synthetic"] is not True
            ):
                return ["ART16 synthetic receipt shape"]
            if any(
                not isinstance(r[k], str) or not r[k]
                for k in RECEIPT_KEYS - {"synthetic", "fieldNames"}
            ):
                return ["ART16 receipt text shape"]
            if not isinstance(r["fieldNames"], list) or any(
                not isinstance(x, str) for x in r["fieldNames"]
            ):
                return ["ART16 receipt fields shape"]
        t = f["test"]
        if t is not None:
            if not isinstance(t, dict) or set(t) != TEST_KEYS:
                return ["ART16 test shape"]
            if any(
                not isinstance(t[k], str) or not t[k]
                for k in TEST_KEYS - {"expected", "actual"}
            ):
                return ["ART16 test text shape"]
            if any(
                not isinstance(t[k], list) or any(not isinstance(x, str) for x in t[k])
                for k in ("expected", "actual")
            ):
                return ["ART16 test values shape"]
    return []


def validate_case(data: object, parent: dict) -> list[str]:
    errors = shape_errors(data)
    if errors:
        return errors
    rows = {r["rowId"]: r for r in parent["rows"]}
    all_ids = []

    def need(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    for index, f in enumerate(data["flows"], 1):
        fid = f"SF-2026-{index:03}"
        prefix = f"{fid}: "
        p = rows[f"BM-2026-{PARENT_ROWS[index - 1]:03}"]
        need(f["flowId"] == fid, prefix + "flow ID/order")
        for child_key, parent_key in [
            ("parentBehaviorId", "rowId"),
            ("assetIds", "assetIds"),
            ("boundaryIds", "boundaryIds"),
            ("parentFlowIds", "flowIds"),
            ("parentTelemetryId", "telemetryId"),
            ("parentGapId", "gapId"),
        ]:
            need(
                f[child_key] == p[parent_key],
                prefix + "parent association " + child_key,
            )
        ident = ACTORS[index - 1]
        need(
            f["identityClass"] == ident
            and f["credentialClass"]
            == {
                "Human": "interactive-authentication",
                "Workload": "workload-authentication",
                "Service": "service-authentication",
            }[ident],
            prefix + "identity/credential role",
        )
        need(
            f["actorId"] == f"SYNTH-ACTOR-SF-{index:03}"
            and f["eventId"] == f"SYNTH-EVENT-SF-{index:03}",
            prefix + "synthetic actor/event",
        )
        for k, stem in [
            ("producerId", "SYNTH-PRODUCER"),
            ("collectorId", "SYNTH-COLLECTOR"),
            ("consumerId", "SYNTH-CONSUMER"),
            ("telemetryId", "TEL-SF"),
            ("gapId", "GAP-SF"),
        ]:
            need(f[k] == f"{stem}-{index:03}", prefix + "owned identifier " + k)
        need(
            f["owner"] in {"SYNTH-PLATFORM-OWNER", "SYNTH-SOC-REVIEWER"},
            prefix + "synthetic owner",
        )
        need(f["plane"] == ("Data" if index in (3, 6) else "Control"), prefix + "plane")
        need(
            f["protocolClass"] == "HTTPS / OAuth role model only"
            and f["queryEndpoint"] == "evidence-query.example",
            prefix + "bounded nonexecuting protocol",
        )
        need(
            f["eventClass"]
            == {2: "audit-export", 3: "api-access", 6: "workload-binding"}.get(
                index, "consent-change"
            ),
            prefix + "event class",
        )
        need(
            f["correlationKeys"] == ["tenant", "application", "requestId", "eventId"]
            and f["requiredFields"] == REQUIRED_FIELDS,
            prefix + "correlation/required fields",
        )
        need(f["clockSource"] == "SYNTH-CLOCK-UTC", prefix + "clock source")
        expected_nodes = [
            {"id": f"N-SF-{index:03}-{j:02}", "role": role}
            for j, role in enumerate(ROLES, 1)
        ]
        expected_edges = [
            {
                "id": f"E-SF-{index:03}-{j:02}",
                "from": expected_nodes[j - 1]["id"],
                "to": expected_nodes[j]["id"],
            }
            for j in range(1, 12)
        ]
        need(
            f["nodes"] == expected_nodes and f["edges"] == expected_edges,
            prefix + "node/edge ownership and continuity",
        )
        dates = {
            k: timestamp(f[k])
            for k in [
                "eventTime",
                "assessmentTime",
                "retentionStart",
                "retentionEnd",
                "queryStart",
                "queryEnd",
            ]
        }
        need(
            all(v is not None for v in dates.values()),
            prefix + "timestamp timezone/canonical format",
        )
        if all(v is not None for v in dates.values()):
            need(
                dates["retentionStart"] <= dates["eventTime"] <= dates["assessmentTime"]
                and dates["retentionStart"] < dates["retentionEnd"],
                prefix + "time ordering",
            )
        if all(v is not None for v in dates.values()):
            delta = timedelta(seconds=f["clockUncertaintySeconds"])
            need(
                dates["retentionStart"]
                <= dates["queryStart"]
                <= dates["eventTime"] - delta
                and dates["eventTime"] + delta
                < dates["queryEnd"]
                <= dates["assessmentTime"],
                prefix + "query window/clock uncertainty",
            )
        stages = [r["stage"] for r in f["receipts"]]
        need(
            stages == list(STAGES[: len(stages)]),
            prefix + "receipt stage prefix/no skipped stage",
        )
        need(f["coverage"] in (*STAGES, "Unknown"), prefix + "finite coverage")
        inferred = stages[-1] if stages else "Unknown"
        need(f["coverage"] == inferred, prefix + "no implicit coverage promotion")
        need(
            f["coverage"] == (*STAGES, "Unknown")[index - 1],
            prefix + "six contrasting teaching scenarios",
        )
        expected_result = "Unknown" if index == 6 else "Allow in synthetic model"
        need(
            f["authorizationResult"] == expected_result
            and f["authenticationResult"]
            == ("Unknown" if index == 6 else "Confirmed in synthetic model"),
            prefix + "authentication/authorization scope",
        )
        prior = dates["eventTime"]
        for j, r in enumerate(f["receipts"], 1):
            need(
                r["id"] == f"EVD-SF-{index:03}-{j:02}"
                and r["flowId"] == fid
                and r["eventId"] == f["eventId"],
                prefix + "same-flow evidence",
            )
            need(
                r["fieldNames"] == REQUIRED_FIELDS
                and r["normalizationVersion"] == "1.0.0",
                prefix + "receipt field/normalization contract",
            )
            at = timestamp(r["recordedAt"])
            need(at is not None, prefix + "receipt timezone")
            if (
                at is not None
                and prior is not None
                and dates["assessmentTime"] is not None
            ):
                need(
                    prior <= at <= dates["assessmentTime"],
                    prefix + "receipt time order",
                )
            prior = at
            if r["stage"] in ("Retained", "Queryable", "Validated") and all(
                v is not None for v in dates.values()
            ):
                need(
                    dates["retentionStart"]
                    <= dates["assessmentTime"]
                    < dates["retentionEnd"],
                    prefix + "current retention expired",
                )
                need(
                    at == dates["assessmentTime"],
                    prefix + "current receipt assessment time",
                )
            all_ids.append(r["id"])
        if index == 2 and all(v is not None for v in dates.values()):
            need(
                dates["retentionEnd"] <= dates["assessmentTime"],
                prefix + "expired teaching counterexample",
            )
        if f["coverage"] == "Validated":
            t = f["test"]
            replay = [r["stage"] for r in f["receipts"] if r["stage"] != "Validated"]
            need(t is not None, prefix + "test required")
            if t is not None:
                need(
                    t
                    == {
                        "id": "TEST-SF-005",
                        "flowId": fid,
                        "scope": "synthetic-flow-receipt-chain",
                        "version": "1.0.0",
                        "expected": replay,
                        "actual": replay,
                        "result": "Pass",
                    }
                    and replay == list(STAGES[:4])
                    and f["detectionId"] == "DET-SF-005",
                    prefix + "same-flow bounded replay",
                )
                all_ids.append(t["id"])
        else:
            need(
                f["test"] is None and f["detectionId"] is None,
                prefix + "no borrowed test",
            )
        need(
            f["allowedConclusion"] == ALLOWED_CONCLUSION
            and f["confidence"] in ("高", "中", "低"),
            prefix + "bounded conclusion/confidence",
        )
        need(
            timestamp(f["reviewDate"] + "T00:00:00+00:00") is not None
            and "2026-09-12" <= f["reviewDate"] <= "2026-12-12",
            prefix + "review deadline",
        )
        all_ids.extend(
            [fid, f["eventId"], f["gapId"], f["telemetryId"]]
            + [n["id"] for n in f["nodes"]]
            + [e["id"] for e in f["edges"]]
        )
    need(len(all_ids) == len(set(all_ids)), "ART16 unique ID ownership")
    return errors
