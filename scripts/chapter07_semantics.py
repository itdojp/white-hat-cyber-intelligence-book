"""ART-17 Layer A: six finite teaching records, not a risk/compliance engine.

CVSS pairs and external signals are frozen audited inputs. This module does not
parse publication syntax, calculate arbitrary CVSS vectors or infer legal scope.
"""

from __future__ import annotations

from datetime import date
import math

IDENTITY = {
    "schemaVersion": "1.0.0",
    "synthetic": True,
    "artifactId": "ART-17",
    "recordSetId": "VPR-2026-001",
    "parentCaseId": "CASE-2026-001",
    "relation": "refines",
    "parentThreatModelId": "TM-2026-001",
    "parentBehaviorMapId": "BMAP-2026-001",
    "parentSignalMapId": "SFM-2026-001",
    "decisionRequirementId": "DR-2026-001",
    "authorizationRecordId": "AUTH-CASE-2026-001",
    "scope": "read-only-synthetic-data",
    "assessmentDate": "2026-09-12",
    "sourceSnapshotId": "SRC-SNAP-CH07-20260911",
    "contextKind": "Synthetic deployments and decisions; external EPSS/KEV values are fixed public-source inputs, not synthetic observations.",
    "parentState": "Independent teaching supplement; no inherited observation, control assurance, gap, decision or deadline is changed.",
    "legalBoundary": "Required-action applicability is unverified; no legal exemption or operational authorization is granted. Catalog dates are not organization deadlines.",
}
TEXT_FIELDS = """recordId title candidateId componentId componentVersion affectedRange
 deploymentStatus affectedStatus reachability exposure precondition attackPathId
 parentThreatId parentBehaviorId signalFlowId parentCoverage parentTelemetryId parentGapId
 cvssAssessment cvssRationale epssMeaning kevStatus requiredActionApplicability governanceOwner
 controlId controlAssurance controlScope assetCriticality businessDependency impactJudgment
 decisionConfidence gapId gap priority treatment decisionReason alternative interimControl
 repairCost owner decisionDate dueDate residualRisk reassessmentTrigger nextReviewDate
 closureCondition handoff""".split()
OPTIONAL_TEXT = """cveId cweId cvssPairId cvssVersion cvssNomenclature cvssVector
 epssModelVersion epssModelIdentifier epssSnapshotDate kevCatalogVersion kevSnapshotDate
 kevCatalogDueDate controlEvidenceId controlValidUntil""".split()
OPTIONAL_NUMBER = ["cvssScore", "epssScore", "epssPercentile"]
LIST_FIELDS = ["assetIds", "boundaryIds", "parentControlIds", "evidenceIds"]
RECORD_KEYS = set(
    TEXT_FIELDS + OPTIONAL_TEXT + OPTIONAL_NUMBER + LIST_FIELDS + ["synthetic"]
)
EVIDENCE_KEYS = {
    "id",
    "recordId",
    "synthetic",
    "kind",
    "scope",
    "recordedDate",
    "claims",
}
CONTEXT_CLAIMS = {
    "componentId",
    "componentVersion",
    "deploymentStatus",
    "affectedStatus",
    "reachability",
    "exposure",
    "impactJudgment",
}
CONTROL_CLAIMS = {"controlId", "controlAssurance", "controlValidUntil"}
# Scenario inventory, not a universal priority rule. New scenarios require review.
SCENARIOS = [
    (
        "CVE-2024-3094",
        "SF-2026-006",
        "Not deployed",
        "Not applicable",
        "Not applicable",
        "Not applicable",
        "Not applicable",
        "Not applicable",
        "Inventory review",
        "Monitor",
    ),
    (
        "CVE-2021-44228",
        "SF-2026-004",
        "Deployed",
        "Affected",
        "Not reachable",
        "Isolated",
        "Validated",
        "Bounded",
        "Planned remediation",
        "Patch",
    ),
    (
        None,
        "SF-2026-006",
        "Deployed",
        "Affected",
        "Possible",
        "Internal",
        "Documented",
        "Bounded",
        "Urgent treatment",
        "Mitigate",
    ),
    (
        "CVE-2021-44228",
        "SF-2026-004",
        "Deployed",
        "Affected",
        "Not reachable",
        "External",
        "Documented",
        "Bounded",
        "Planned remediation",
        "Patch",
    ),
    (
        "CVE-2021-44228",
        "SF-2026-001",
        "Unknown",
        "Unknown",
        "Unknown",
        "External",
        "Unknown",
        "Inconclusive",
        "Evidence first",
        "Investigate",
    ),
    (
        None,
        "SF-2026-006",
        "Deployed",
        "Unknown",
        "Unknown",
        "Unknown",
        "Unknown",
        "Inconclusive",
        "Evidence first",
        "Investigate",
    ),
]
SCENARIO_FIELDS = [
    "cveId",
    "signalFlowId",
    "deploymentStatus",
    "affectedStatus",
    "reachability",
    "exposure",
    "controlAssurance",
    "impactJudgment",
    "priority",
    "treatment",
]
OWNER = "SYNTH-VULNERABILITY-OWNER"
GOVERNANCE_OWNER = "SYNTH-GOVERNANCE-REVIEWER"


def iso_date(value):
    if not isinstance(value, str):
        return None
    try:
        parsed = date.fromisoformat(value)
        return parsed if parsed.isoformat() == value else None
    except ValueError:
        return None


def shape_errors(data):
    if not isinstance(data, dict) or set(data) != set(IDENTITY) | {
        "sourceSnapshotSha256",
        "records",
        "evidence",
    }:
        return ["ART17 root closed shape"]
    if any(type(data[k]) is not type(v) or data[k] != v for k, v in IDENTITY.items()):
        return ["ART17 synthetic identity/authority/parent-state"]
    if not isinstance(data["sourceSnapshotSha256"], str):
        return ["ART17 source digest shape"]
    if not isinstance(data["records"], list) or len(data["records"]) != 6:
        return ["ART17 six-record inventory"]
    for r in data["records"]:
        if (
            not isinstance(r, dict)
            or set(r) != RECORD_KEYS
            or r["synthetic"] is not True
        ):
            return ["ART17 record closed shape/synthetic marker"]
        if any(not isinstance(r[k], str) or not r[k].strip() for k in TEXT_FIELDS):
            return ["ART17 required text shape"]
        if any(
            r[k] is not None and (not isinstance(r[k], str) or not r[k])
            for k in OPTIONAL_TEXT
        ):
            return ["ART17 nullable text shape"]
        for k in OPTIONAL_NUMBER:
            if r[k] is not None and (
                type(r[k]) not in (int, float) or not math.isfinite(r[k])
            ):
                return ["ART17 finite numeric shape"]
        for k in LIST_FIELDS:
            if (
                not isinstance(r[k], list)
                or any(not isinstance(x, str) or not x for x in r[k])
                or len(set(r[k])) != len(r[k])
            ):
                return ["ART17 unique reference list shape"]
            if k != "parentControlIds" and not r[k]:
                return ["ART17 nonempty reference list"]
    if not isinstance(data["evidence"], list) or len(data["evidence"]) != 7:
        return ["ART17 evidence inventory"]
    for e in data["evidence"]:
        if (
            not isinstance(e, dict)
            or set(e) != EVIDENCE_KEYS
            or e["synthetic"] is not True
        ):
            return ["ART17 synthetic evidence shape"]
        if any(
            not isinstance(e[k], str) or not e[k]
            for k in EVIDENCE_KEYS - {"claims", "synthetic"}
        ):
            return ["ART17 evidence text shape"]
        if not isinstance(e["claims"], dict) or set(e["claims"]) not in (
            CONTEXT_CLAIMS,
            CONTROL_CLAIMS,
        ):
            return ["ART17 evidence claim shape"]
        if any(not isinstance(v, str) or not v for v in e["claims"].values()):
            return ["ART17 evidence claim values"]
    return []


def validate_case(data, parent_signals, parent_behaviors, snapshot, snapshot_digest):
    errors = shape_errors(data)
    if errors:
        return errors

    def need(ok, message):
        if not ok:
            errors.append("ART17 " + message)

    need(data["sourceSnapshotSha256"] == snapshot_digest, "source snapshot digest")
    need(data["sourceSnapshotId"] == snapshot["snapshotId"], "source snapshot identity")
    flows = {f["flowId"]: f for f in parent_signals["flows"]}
    behaviors = {r["rowId"]: r for r in parent_behaviors["rows"]}
    evidence = {e["id"]: e for e in data["evidence"]}
    need(len(evidence) == len(data["evidence"]), "duplicate evidence identity")
    used = []
    for i, r in enumerate(data["records"], 1):
        rid = f"VPR-ITEM-{i:03}"
        need(
            r["recordId"] == rid and r["candidateId"] == f"SYNTH-CANDIDATE-{i:03}",
            "record/candidate identity/order",
        )
        need(
            tuple(r[k] for k in SCENARIO_FIELDS) == SCENARIOS[i - 1],
            "finite scenario semantics " + rid,
        )
        # Resolve the audited association, never trust a mutated link as the owner.
        f = flows[SCENARIOS[i - 1][1]]
        b = behaviors[f["parentBehaviorId"]]
        for k, parentkey in [
            ("parentCoverage", "coverage"),
            ("parentTelemetryId", "telemetryId"),
            ("parentGapId", "gapId"),
        ]:
            need(r[k] == f[parentkey], "retained parent Flow/Gap " + k)
        for k, parentkey in [
            ("assetIds", "assetIds"),
            ("boundaryIds", "boundaryIds"),
            ("parentControlIds", "controlIds"),
            ("parentBehaviorId", "rowId"),
            ("parentThreatId", "threatId"),
        ]:
            need(r[k] == b[parentkey], "parent association " + k)
        path = (
            "PATH-2026-001"
            if b["threatId"] in ("TH-2026-001", "TH-2026-004")
            else "PATH-2026-002"
        )
        need(r["attackPathId"] == path, "Threat/Attack Path relation")
        need(
            r["componentId"] == f"SYNTH-COMPONENT-{i:03}"
            and r["componentVersion"] == "0.0.0-synthetic"
            and r["affectedRange"]
            == "synthetic teaching range only; not vendor version advice",
            "synthetic component/version boundary",
        )
        need(r["gapId"] == f"GAP-VPR-{i:03}", "new gap identity")
        # No rating is inferred for the evidence-deficient sixth case.
        pair = snapshot["cvss"]["pairs"][1 if i == 3 else 0] if i != 6 else None
        for k, pk in [
            ("cvssPairId", "id"),
            ("cvssVersion", "version"),
            ("cvssNomenclature", "nomenclature"),
            ("cvssVector", "vector"),
            ("cvssScore", "score"),
        ]:
            need(
                r[k] == (pair[pk] if pair else None),
                "finite CVSS vector/score/nomenclature " + k,
            )
        need(
            r["cvssAssessment"]
            == (
                "synthetic-author-assessment-not-a-vendor-CVE-rating"
                if pair
                else "Not assessed: missing impact evidence"
            ),
            "CVSS rating provenance",
        )
        if r["cveId"]:
            s = next(
                (s for s in snapshot["epss"]["rows"] if s["cveId"] == r["cveId"]), None
            )
            k = next(
                (s for s in snapshot["kev"]["rows"] if s["cveId"] == r["cveId"]), None
            )
            if s is None or k is None:
                need(False, "CVE source selection")
                continue
            expected = {
                "epssModelVersion": snapshot["epss"]["modelVersion"],
                "epssModelIdentifier": snapshot["epss"]["modelIdentifier"],
                "epssSnapshotDate": snapshot["epss"]["scoreDate"],
                "epssScore": s["score"],
                "epssPercentile": s["percentile"],
                "epssMeaning": "30-day CVE exploitation signal, not organization compromise probability",
                "kevStatus": "Listed" if k["listed"] else "Not listed in snapshot",
                "kevCatalogVersion": snapshot["kev"]["catalogVersion"],
                "kevSnapshotDate": snapshot["kev"]["dateReleased"][:10],
                "kevCatalogDueDate": k["catalogDueDate"],
                "cweId": None,
            }
        else:
            expected = {
                k: None
                for k in [
                    "epssModelVersion",
                    "epssModelIdentifier",
                    "epssSnapshotDate",
                    "epssScore",
                    "epssPercentile",
                    "kevCatalogVersion",
                    "kevSnapshotDate",
                    "kevCatalogDueDate",
                ]
            }
            expected.update(
                epssMeaning="Not applicable: no CVE identifier",
                kevStatus="Not applicable",
                cweId="CWE-639",
            )
        # Missing CVE prevents a keyed EPSS/KEV lookup, not legal applicability.
        expected["requiredActionApplicability"] = "Unverified"
        for k, v in expected.items():
            need(
                type(r[k]) is type(v) and r[k] == v,
                "CVE/snapshot/meaning/applicability " + k,
            )
        need(
            r["owner"] == OWNER and r["governanceOwner"] == GOVERNANCE_OWNER,
            "synthetic accountable owners",
        )
        need(r["assetCriticality"] == "Critical", "business context")
        need(
            r["controlId"] == f"SYNTH-CTRL-VPR-{i:03}"
            and r["controlScope"]
            == "same-record synthetic path only; not inherited control validation",
            "local control ownership",
        )
        decision, due, review = (
            iso_date(r[k]) for k in ("decisionDate", "dueDate", "nextReviewDate")
        )
        need(decision == iso_date(data["assessmentDate"]), "decision snapshot date")
        need(
            bool(
                decision
                and due
                and review
                and decision < review <= due <= date(2026, 10, 12)
            ),
            "owner deadline/reassessment order",
        )
        if r["kevCatalogDueDate"]:
            need(
                r["dueDate"] != r["kevCatalogDueDate"],
                "catalog date is not organization deadline",
            )
        need(r["decisionConfidence"] in ["高", "中", "低"], "confidence finite status")
        uncertain = any(
            r[k] in ["Unknown", "Inconclusive"]
            for k in [
                "deploymentStatus",
                "affectedStatus",
                "reachability",
                "exposure",
                "controlAssurance",
                "impactJudgment",
            ]
        )
        need(
            r["decisionConfidence"] == ("低" if uncertain else "中"),
            "bounded decision confidence",
        )
        if uncertain:
            need(
                r["priority"] == "Evidence first" and r["treatment"] == "Investigate",
                "unknown evidence treatment",
            )
        if r["deploymentStatus"] == "Not deployed":
            need(
                r["affectedStatus"] == "Not applicable" and r["treatment"] == "Monitor",
                "non-deployed is not affected",
            )
        expected_ids = [f"EVD-VPR-{i:03}-CONTEXT"]
        if r["controlAssurance"] == "Validated":
            expected_ids.append(f"EVD-VPR-{i:03}-CONTROL")
            need(
                r["controlEvidenceId"] == expected_ids[-1], "validated control evidence"
            )
            until = iso_date(r["controlValidUntil"])
            need(
                bool(until and due and due < until <= date(2026, 10, 12)),
                "control validity after treatment deadline",
            )
        else:
            need(
                r["controlEvidenceId"] is None and r["controlValidUntil"] is None,
                "no invented validation",
            )
        need(r["evidenceIds"] == expected_ids, "same-record evidence list")
        for eid in r["evidenceIds"]:
            used.append(eid)
            e = evidence.get(eid)
            if e is None:
                need(False, "missing evidence " + eid)
                continue
            need(
                e["recordId"] == rid
                and e["kind"] == "supplied-teaching-assumption"
                and e["scope"]
                == "same-record synthetic path only; not production or parent assurance",
                "evidence provenance/association",
            )
            need(e["recordedDate"] == data["assessmentDate"], "evidence date")
            keys = CONTROL_CLAIMS if eid.endswith("-CONTROL") else CONTEXT_CLAIMS
            need(
                set(e["claims"]) == keys
                and all(e["claims"].get(k) == r[k] for k in keys),
                "evidence claim/record parity",
            )
    need(
        len(used) == len(set(used)) and set(used) == set(evidence),
        "no borrowed or unowned evidence",
    )
    return errors
