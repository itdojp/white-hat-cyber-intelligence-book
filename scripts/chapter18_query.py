"""ART-06 finite synthetic consent/use question, not a SIEM or log parser.

Integer offsets use a fictional clock. Supplied coverage assertions are teaching
inputs, not actual collector receipts. No I/O, network, arbitrary query language,
production authority, actor attribution or automatic incident declaration.
"""

from copy import deepcopy

VERSION = "1.0.0"
RESULTS = ("Supported", "Weakened", "Negative finding", "Inconclusive", "Stopped")
STREAMS = ("consent", "approval", "use")
SUBJECT = "SYNTH-HUNT18-001"
REVISION = "HUNT18-REV-001"
POPULATION = ("syn-workload-a",)
PLAN = {
    "subject": SUBJECT,
    "revision": REVISION,
    "population": list(POPULATION),
    "grantStart": 0,
    "grantEnd": 1800,
    "dataEnd": 3600,
    "asOf": 4000,
    "pivotSeconds": 1800,
    "namespace": "syn-tenant-a",
    "normalizer": "syn-normalizer-1",
}
LIMIT = "supplied-synthetic-subject-revision-population-window-query-only"
ALTERNATIVE = "incomplete-change-record-or-unmodeled-benign-context"


class HuntInputError(ValueError):
    """Invalid input contract, distinct from a valid Stopped decision."""


def require(condition, code):
    if not condition:
        raise HuntInputError(code)


def keys(value, expected, label):
    require(type(value) is dict and set(value) == set(expected.split()), label)


def integer(value, minimum, maximum, label):
    require(type(value) is int and minimum <= value <= maximum, label)


def tokens(value, allowed, label, nonempty=False):
    require(type(value) is list and (not nonempty or len(value) > 0), label)
    require(all(type(v) is str and v in allowed for v in value), label)
    require(len(value) == len(set(value)), label + ":duplicate")


def scopes(value):
    tokens(
        value, ("scope-invoice-read", "scope-ledger-export"), "scopes", nonempty=True
    )


def validate(data):
    keys(
        data,
        "queryContractId syntheticOnly offlineOnly executionAuthorized parentReceipt plan mode stop receipts events approvals",
        "envelope",
    )
    require(data["queryContractId"] == "QUERY-HUNT18-1", "query-contract")
    require(
        data["syntheticOnly"] is True and data["offlineOnly"] is True,
        "synthetic-offline-only",
    )
    require(
        data["executionAuthorized"] is False and data["parentReceipt"] is None,
        "no-authority-or-receipt-inheritance",
    )
    require(data["plan"] == PLAN, "frozen-plan")
    # Equality alone would accept True for integer 1 and 0.0 for integer 0.
    for k in ("grantStart", "grantEnd", "dataEnd", "asOf", "pivotSeconds"):
        require(type(data["plan"][k]) is int, "plan-integer")
    require(data["mode"] in ("behavior", "ioc-only"), "query-mode")
    require(
        data["stop"] in (None, "scope-expansion", "privacy-risk", "operator-stop"),
        "stop-code",
    )
    require(type(data["receipts"]) is list and len(data["receipts"]) <= 3, "receipts")
    seen = set()
    for r in data["receipts"]:
        keys(
            r,
            "stream subject revision population start end producer collected retained queryable clock identity",
            "receipt-shape",
        )
        require(r["stream"] in STREAMS and r["stream"] not in seen, "receipt-stream")
        seen.add(r["stream"])
        require(r["subject"] in (SUBJECT, "SYNTH-OTHER-SUBJECT"), "receipt-subject")
        require(r["revision"] in (REVISION, "HUNT18-REV-000"), "receipt-revision")
        tokens(
            r["population"],
            ("syn-workload-a", "syn-workload-b"),
            "receipt-population",
            True,
        )
        integer(r["start"], 0, 3600, "receipt-start")
        integer(r["end"], 0, 3600, "receipt-end")
        require(r["start"] < r["end"], "receipt-interval")
        for field in (
            "producer",
            "collected",
            "retained",
            "queryable",
            "clock",
            "identity",
        ):
            require(type(r[field]) is bool, "receipt-boolean")
    require(type(data["events"]) is list and len(data["events"]) <= 12, "events")
    seen = set()
    for e in data["events"]:
        keys(
            e,
            "id kind subject revision workload namespace normalizer eventTime ingestTime uncertainty result scopes ticket iocMatch",
            "event-shape",
        )
        require(
            e["id"] in tuple(f"SYN-EVT-{i:02}" for i in range(1, 13))
            and e["id"] not in seen,
            "event-id",
        )
        seen.add(e["id"])
        require(e["kind"] in ("consent", "use"), "event-kind")
        require(
            e["subject"] == SUBJECT and e["revision"] == REVISION,
            "event-origin-binding",
        )
        require(e["workload"] in ("syn-workload-a", "syn-workload-b"), "event-workload")
        require(e["namespace"] in ("syn-tenant-a", "syn-tenant-b"), "event-namespace")
        require(
            e["normalizer"] in ("syn-normalizer-1", "syn-normalizer-2"),
            "event-normalizer",
        )
        for field in ("eventTime", "ingestTime", "uncertainty"):
            integer(e[field], 0, 5000, "event-time")
        require(e["ingestTime"] >= e["eventTime"], "event-arrival-order")
        require(e["result"] in ("success", "failure"), "event-result")
        require(type(e["iocMatch"]) is bool, "ioc-boolean")
        require(e["ticket"] in (None, "syn-change-01", "syn-change-02"), "event-ticket")
        if e["kind"] == "consent":
            scopes(e["scopes"])
        else:
            require(e["scopes"] == [] and e["ticket"] is None, "use-fields")
    require(
        type(data["approvals"]) is list and len(data["approvals"]) <= 2, "approvals"
    )
    seen = set()
    for a in data["approvals"]:
        keys(
            a,
            "id subject revision workload namespace normalizer ticket start end scopes",
            "approval-shape",
        )
        require(
            a["id"] in ("SYN-APP-01", "SYN-APP-02") and a["id"] not in seen,
            "approval-id",
        )
        seen.add(a["id"])
        require(
            a["subject"] == SUBJECT and a["revision"] == REVISION,
            "approval-origin-binding",
        )
        require(
            a["workload"] in ("syn-workload-a", "syn-workload-b"), "approval-workload"
        )
        require(
            a["namespace"] == PLAN["namespace"]
            and a["normalizer"] == PLAN["normalizer"],
            "approval-identity",
        )
        require(a["ticket"] in ("syn-change-01", "syn-change-02"), "approval-ticket")
        integer(a["start"], 0, 3600, "approval-start")
        integer(a["end"], 0, 3600, "approval-end")
        require(a["start"] < a["end"], "approval-interval")
        scopes(a["scopes"])
    # No first-row-wins interpretation for duplicate change tickets.
    require(
        len({a["ticket"] for a in data["approvals"]}) == len(data["approvals"]),
        "ambiguous-approval-ticket",
    )


def evaluate(data):
    """Return an evidence-limited educational judgment without mutating input."""
    validate(data)
    gaps = []
    evidence = []
    pairs = []
    ioc_hits = []
    if data["stop"]:
        result = "Stopped"
        gaps.append(data["stop"])
    else:
        receipts = {r["stream"]: r for r in data["receipts"]}
        for stream in STREAMS:
            r = receipts.get(stream)
            if r is None:
                gaps.append(stream + ":receipt-missing")
                continue
            if (r["subject"], r["revision"], sorted(r["population"])) != (
                SUBJECT,
                REVISION,
                list(POPULATION),
            ):
                gaps.append(stream + ":context-mismatch")
            if r["start"] != 0 or r["end"] != 3600:
                gaps.append(stream + ":window-gap")
            for field in (
                "producer",
                "collected",
                "retained",
                "queryable",
                "clock",
                "identity",
            ):
                if not r[field]:
                    gaps.append(stream + ":" + field + "-gap")
        events = []
        for e in data["events"]:
            # Workload-b is a known out-of-population near-miss, not a pivot.
            if e["workload"] not in POPULATION:
                continue
            overlaps = (
                e["eventTime"] + e["uncertainty"] >= 0
                and e["eventTime"] - e["uncertainty"] < PLAN["dataEnd"]
            )
            if overlaps and e["uncertainty"]:
                gaps.append("time-uncertainty")
            if not 0 <= e["eventTime"] < PLAN["dataEnd"]:
                continue
            if (
                e["namespace"] != PLAN["namespace"]
                or e["normalizer"] != PLAN["normalizer"]
            ):
                gaps.append("identity-unjoinable")
                continue
            if e["ingestTime"] > PLAN["asOf"]:
                gaps.append("arrival-incomplete")
                continue
            events.append(e)
        ioc_hits = sorted(e["id"] for e in events if e["iocMatch"])
        if data["mode"] == "ioc-only":
            gaps.append("behavior-not-tested")
        if gaps:
            result = "Inconclusive"
        else:
            grants = [
                e
                for e in events
                if e["kind"] == "consent"
                and e["result"] == "success"
                and PLAN["grantStart"] <= e["eventTime"] < PLAN["grantEnd"]
            ]
            uses = [
                e for e in events if e["kind"] == "use" and e["result"] == "success"
            ]
            approved = []
            approved_grants = set()
            for grant in grants:
                matches = [
                    a
                    for a in data["approvals"]
                    if a["ticket"] == grant["ticket"]
                    and a["workload"] == grant["workload"]
                    and a["start"] <= grant["eventTime"] < a["end"]
                    and set(grant["scopes"]) <= set(a["scopes"])
                ]
                if matches:
                    approved_grants.add(grant["id"])
                    approved.extend((grant["id"], matches[0]["id"]))
                    continue
                for use in uses:
                    if (
                        use["workload"] == grant["workload"]
                        and 0
                        <= use["eventTime"] - grant["eventTime"]
                        <= PLAN["pivotSeconds"]
                    ):
                        pairs.append((grant["id"], use["id"]))
            if pairs:
                result = "Supported"
                evidence = sorted({v for pair in pairs for v in pair})
            elif grants and len(approved_grants) == len(grants):
                result = "Weakened"
                evidence = sorted(set(approved))
            else:
                result = "Negative finding"
    if result == "Stopped":
        routes = ["scope-review"]
    elif result == "Inconclusive":
        routes = ["collection-review"]
    elif result == "Supported":
        routes = ["detection-review", "incident-triage-review"]
    else:
        routes = ["reassessment"]
    return {
        "result": result,
        "gaps": sorted(set(gaps)),
        "evidence": sorted(evidence),
        "pairs": [list(pair) for pair in sorted(set(pairs))],
        "iocHits": ioc_hits,
        "limit": LIMIT,
        "alternative": ALTERNATIVE,
        "scope": deepcopy(PLAN),
        "owner": "SYNTH-HUNT-OWNER",
        "reassessment": "input-revision-window-query-or-coverage-change",
        "handoffs": [
            {
                "route": route,
                "status": "planned-not-delivered",
                "receipt": None,
                "executionAuthorized": False,
            }
            for route in routes
        ],
    }


def verify_claim(data, claimed_result):
    require(claimed_result in RESULTS, "unknown-result")
    output = evaluate(data)
    require(output["result"] == claimed_result, "result-not-supported")
    return output
