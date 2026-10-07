"""ART-02 finite, non-executing teaching-plan semantics (Layer A only).

This validates declared synthetic conditions, never real permission/signatures.
No Markdown, URL, browser, container, network or operational state machine.
"""

from __future__ import annotations

from datetime import datetime
import json
import os
from pathlib import Path, PurePosixPath
import stat

from scripts.check_editorial_input_manifest import (
    ManifestError,
    _reject_duplicate_keys,
    _reject_constant,
    validate_schema_instance,
    validate_supported_schema_nodes,
)
from scripts.content_safety_policy import scan_action_text, scan_host_policy

MODEL_VERSION = "1.0.0"
DATA_PATH = "cases/fixtures/ch09-engagement-roe.json"
SCHEMA_PATH = "schemas/ch09-engagement-roe.schema.json"
READ_PATHS = (DATA_PATH, SCHEMA_PATH)
PARENT_PATHS = (
    "cases/ch01-integrated-security-case-example.md",
    "cases/ch02-authorization-decision-example.md",
    "cases/ch04-threat-model-example.md",
    "cases/ch05-attack-behavior-example.md",
    "cases/ch06-signal-flow-example.md",
    "cases/fixtures/ch06-signal-flow.json",
    "cases/fixtures/ch05-attack-behavior.json",
    "cases/fixtures/ch07-vulnerability-prioritization.json",
    "cases/ch07-vulnerability-prioritization-example.md",
    "cases/fixtures/ch07-source-snapshot.json",
    "LAB_ARCHITECTURE.md",
    "CONTENT_SAFETY_POLICY.md",
    "scripts/content_safety_policy.py",
    "scripts/publication_projection.py",
    "scripts/_publication_projection_renderer.rb",
    "scripts/publication_text.py",
    "Gemfile.lock",
    "package-lock.json",
    ".book-formatter/revision.json",
    "manuscript/02-law-ethics-authorization.md",
    "templates/authorization-checklist.md",
    "manuscript/08-safe-lab-evidence.md",
    "templates/lab-safety-evidence-plan.md",
    "cases/ch08-lab-evidence-example.md",
    "cases/fixtures/ch08-lab-plan.json",
    "cases/fixtures/ch08-evidence-manifest.json",
    "cases/fixtures/ch08-control-receipts.json",
    "cases/ch11-web-api-assessment-example.md",
    "CROSS_BOOK_MAP.md",
)
DOCUMENT_PATHS = (
    "manuscript/09-engagement-roe.md",
    "templates/rules-of-engagement.md",
    "cases/ch09-engagement-roe-example.md",
    "references/ch09-source-review-2026-09-13.md",
)
REGULAR_PATHS = (*READ_PATHS, *PARENT_PATHS, *DOCUMENT_PATHS)
STATES = (
    "Draft",
    "Under review",
    "Approved",
    "Active",
    "Paused",
    "Revoked",
    "Expired",
    "Completed",
)
OBJECT_IDS = ("OBJ-ROE09-CONFIG", "OBJ-ROE09-EVENT", "OBJ-ROE09-POLICY")
METHODS = ("read-supplied-json", "compare-synthetic-fields", "write-bounded-summary")
PROHIBITED = tuple(
    v + "は禁止する。"
    for v in (
        "external-communication",
        "active-scanning",
        "authentication-attempt",
        "credential-reuse",
        "dos",
        "persistence",
        "evasion",
        "log-deletion",
        "destructive-change",
    )
)
OUTSIDE = (
    "all-unlisted-objects",
    "production-assets",
    "real-identities",
    "third-party-services",
    "credential-material",
    "personal-data",
)
TRIGGERS = (
    "unknown-authority",
    "out-of-scope",
    "unexpected-data",
    "external-communication",
    "budget-exceeded",
    "missing-evidence",
    "unavailable-contact",
    "cleanup-unconfirmed",
)
ROLES = (
    "SYNTH-SPONSOR",
    "SYNTH-AUTHORITY-OWNER",
    "SYNTH-SYSTEM-OWNER",
    "SYNTH-DATA-OWNER",
    "SYNTH-TEST-LEAD",
)
RECOVERY = (
    "stop-new-work",
    "preserve-reference-and-time",
    "notify-primary-or-backup",
    "review-affected-synthetic-copies",
    "verify-cleanup-record",
)
ID_FIELDS = {
    ("record", "artifactId"): "ART-02",
    ("record", "roeId"): "ROE-2026-009",
    ("record", "parentCaseId"): "CASE-2026-001",
    ("record", "relation"): "refines",
    ("parents", "authorizationRecordId"): "AUTH-CASE-2026-001",
    ("parents", "authorizationDecisionId"): "DEC-AUTH-2026-001",
    ("parents", "authorizationDecisionRequirementId"): "DR-AUTH-2026-001",
    ("parents", "threatModelId"): "TM-2026-001",
    ("parents", "threatHypothesisId"): "TH-2026-002",
    ("parents", "labPlanId"): "LABPLAN-2026-001",
    ("parents", "labEvidenceId"): "EVD-LAB08-001",
    ("parents", "parentReassessmentId"): "REA-2026-001",
    ("decision", "requirementId"): "DR-2026-001",
    ("decision", "plannedDecisionId"): "DEC-ROE09-001",
    ("decision", "informationGapId"): "GAP-ROE09-001",
    ("scope", "scopeId"): "SCOPE-ROE09-001",
    ("methods", "methodId"): "METHOD-ROE09-001",
    ("data", "dataId"): "DATA-ROE09-001",
    ("stop", "stopId"): "STOP-ROE09-001",
    ("stop", "cleanupEvidenceId"): "CLEAN-ROE09-001",
    ("evidence", "evidenceId"): "EVD-ROE09-001",
    ("change", "reauthorizationId"): "REA-ROE09-001",
    ("change", "changeRequestId"): "CR-ROE09-001",
    ("change", "retestId"): "RET-ROE09-001",
    ("boundary", "independentCase"): "CASE-2026-011",
    ("boundary", "independentRoe"): "ROE-2026-011",
}


def strict_bytes(raw):
    return json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=_reject_duplicate_keys,
        parse_constant=_reject_constant,
    )


def read_regular(root: Path, relative: str):
    """Read the fixed data/schema, selected documents and frozen parents.

    Reject static symlinks, special/oversized files and unsupported platforms.
    This is not a sandbox against concurrent hostile filesystem replacement.
    """
    if any(
        type(getattr(os, flag, None)) is not int
        for flag in ("O_NOFOLLOW", "O_NONBLOCK")
    ):
        raise ValueError("ART02 requires Linux/WSL2 no-follow/nonblocking primitives")
    if relative not in REGULAR_PATHS or root.is_symlink():
        raise ValueError("ART02 finite input inventory")
    root = root.resolve(strict=True)
    current = root
    for part in PurePosixPath(relative).parts:
        current /= part
        if current.is_symlink():
            raise ValueError("ART02 symlink input/ancestor")
    if not current.resolve(strict=True).is_relative_to(root):
        raise ValueError("ART02 input containment")
    fd = os.open(current, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= 1024 * 1024:
            raise ValueError("ART02 regular bounded input required")
        raw = stream.read(1024 * 1024 + 1)
    if len(raw) > 1024 * 1024:
        raise ValueError("ART02 input size")
    return raw


def read_input(root: Path, relative: str):
    if relative not in READ_PATHS:
        raise ValueError("ART02 JSON input inventory")
    return strict_bytes(read_regular(root, relative))


def utc(value):
    if not isinstance(value, str):
        raise ValueError("ART02 UTC timestamp type")
    d = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    if d.strftime("%Y-%m-%dT%H:%M:%SZ") != value:
        raise ValueError("ART02 canonical UTC timestamp")
    return d


def leaves(value, path=()):
    """Deterministic authored field paths; not a Markdown projection."""
    if isinstance(value, dict):
        for k, v in value.items():
            yield from leaves(v, path + (k,))
    elif isinstance(value, list) and value:
        for i, v in enumerate(value):
            yield from leaves(v, path + (str(i + 1),))
    else:
        yield path, value


def conditions(data):
    """Evaluate already shape-validated hypothetical declarations at fixed asOf.

    Satisfying these finite conditions never authenticates an authorization or
    signs an approval. The canonical plan is deliberately not eligible.
    """
    r, a, w, c = (data[k] for k in ("record", "approval", "window", "change"))
    now, start, end, afrom, auntil = map(
        utc, (r["asOf"], w["startsAt"], w["endsAt"], a["validFrom"], a["validUntil"])
    )
    blockers = []

    def need(ok, code):
        if not ok:
            blockers.append(code)

    need(r["status"] in ("Approved", "Active"), "ROE-STATUS")
    need(a["authorityStatus"] == "Current", "AUTH-STATUS")
    need(afrom <= now < auntil, "AUTH-TIME")
    need(
        afrom <= start < end <= auntil
        and utc(data["parents"]["authorizationWindowStartsAt"])
        <= start
        < end
        <= utc(data["parents"]["authorizationWindowEndsAt"]),
        "WINDOW-AUTHORITY",
    )
    need(start <= now < end, "WINDOW-NOW")
    need(
        a["writtenEvidenceRef"] == "SYNTH-AUTH-PROOF-ROE09-V" + str(r["version"]),
        "WRITTEN-PROOF",
    )
    need(
        type(a["approvedVersion"]) is int and a["approvedVersion"] == r["version"],
        "APPROVED-VERSION",
    )
    need(a["signoffs"] == list(ROLES), "APPROVAL-ROLES")
    if c["kind"] == "restart":
        need(
            c["stopCleared"] is True
            and c["restartApprovalRef"] == "SYNTH-RESTART-ROE09-V" + str(r["version"]),
            "RESTART-APPROVAL",
        )
    if c["kind"] == "retest":
        need(
            c["retestApprovalRef"] == "SYNTH-RETEST-ROE09-V" + str(r["version"]),
            "RETEST-APPROVAL",
        )
    return blockers


def validate_record(data, schema):
    errors = []
    try:
        validate_supported_schema_nodes(schema, "ART02 schema", schema)
        validate_schema_instance(data, schema)
    except (ManifestError, ValueError, KeyError, TypeError) as exc:
        return ["ART02 schema: " + str(exc)]

    def need(ok, code):
        if not ok:
            errors.append("ART02 " + code)

    need(
        data["schemaVersion"] == data["modelVersion"] == MODEL_VERSION, "model version"
    )
    need(
        data["synthetic"] is True and data["executionAuthorized"] is False,
        "non-executing synthetic boundary",
    )
    for (group, field), expected in ID_FIELDS.items():
        need(data[group][field] == expected, "direct ID " + group + "/" + field)
    r, p, d, s, m, w, lim, dt, stop, a, ev, comp, c, b = (
        data[k]
        for k in (
            "record",
            "parents",
            "decision",
            "scope",
            "methods",
            "window",
            "limits",
            "data",
            "stop",
            "approval",
            "evidence",
            "completion",
            "change",
            "boundary",
        )
    )
    need(
        r["status"] in STATES and r["supersedes"] is None and r["version"] >= 1,
        "record identity/status",
    )
    need(
        p["authorizationHistoricalOutcome"] == "Proceed with conditions"
        and p["authorizationConditions"]
        == [
            "COND-AUTH-2026-001 Open",
            "COND-AUTH-2026-002 Satisfied",
            "COND-AUTH-2026-003 Open",
        ],
        "historical conditions not promoted",
    )
    need(
        p["authorizationExpiresAt"] == "2026-08-19T09:00:00Z"
        and p["threatModelStatus"] == "Needs Evidence"
        and p["labExecutionAuthorized"] is False
        and p["parentStateChanged"] is False,
        "parent state not promoted",
    )
    need(
        p["assetIds"] == ["ASSET-2026-002", "ASSET-2026-003"]
        and p["boundaryIds"] == ["TB-2026-001", "TB-2026-003"]
        and p["flowIds"] == ["FLOW-2026-002", "FLOW-2026-004"],
        "parent selection",
    )
    need(
        d["historicalDeadline"] == "2026-07-22T00:00:00Z"
        and d["decisionUseful"] == "not-assessed",
        "historical DR versus new review",
    )
    need(
        p["authorizationWindowStartsAt"] == "2026-08-06T00:00:00Z"
        and p["authorizationWindowEndsAt"] == "2026-08-06T08:00:00Z",
        "parent test window not broadened",
    )
    need(d["owner"] == "SYNTH-DECISION-OWNER", "decision owner")
    need(
        s["defaultDenied"] is True
        and s["environment"] == "ENV-ROE09-SYNTHETIC"
        and s["identity"] == "IDENTITY-ROE09-SYNTHETIC-READER"
        and s["thirdPartyDependency"] == "none-required",
        "scope boundary",
    )
    need(
        [x["objectId"] for x in s["inScope"]] == list(OBJECT_IDS)
        and s["outOfScope"] == list(OUTSIDE),
        "finite scope/disjointness/default deny",
    )
    need(
        [x["objectId"] for x in data["objects"]] == list(OBJECT_IDS)
        and all(x["synthetic"] is True for x in data["objects"]),
        "supplied object ownership",
    )
    need(
        [x["owner"] for x in s["inScope"]]
        == ["SYNTH-SYSTEM-OWNER", "SYNTH-DATA-OWNER", "SYNTH-SYSTEM-OWNER"]
        and all(
            x["thirdParty"] is False and x["classification"] == "synthetic-only"
            for x in s["inScope"]
        ),
        "scope owner/data",
    )
    need(
        m["permitted"] == list(METHODS)
        and m["conditional"] == []
        and m["prohibited"] == list(PROHIBITED),
        "operation allow/deny finite inventory",
    )
    need(
        w["timezone"] == "UTC" and w["status"] == "proposed-not-authorized",
        "no issued operational window",
    )
    need(
        lim["networkRequests"] == 0
        and lim["concurrency"] == 1
        and lim["retries"] == 0
        and 0 < lim["records"] <= 100
        and 0 < lim["evidenceBytes"] <= 65536
        and 0 < lim["minutes"] <= 30
        and lim["onLimit"] == "stop-and-record-gap",
        "effect budgets",
    )
    need(
        dt["classification"] == "synthetic-only"
        and dt["credentialMaterial"] == "none"
        and dt["storage"] == "SYNTH-DEDICATED-WORK-COPY"
        and dt["custodian"] == "SYNTH-EVIDENCE-CUSTODIAN"
        and dt["destructionOwner"] == "SYNTH-RECOVERY-OWNER"
        and 0 < dt["retentionHours"] <= 24
        and dt["retentionStarts"] == "hypothetical-session-end",
        "data custody/retention",
    )
    need(
        stop["triggers"] == list(TRIGGERS)
        and stop["primaryContact"] == "SYNTH-TEST-LEAD"
        and stop["backupContact"] == "SYNTH-SPONSOR"
        and 0 < stop["acknowledgementSeconds"] <= 60
        and stop["recoveryOwner"] == "SYNTH-RECOVERY-OWNER"
        and stop["recoverySteps"] == list(RECOVERY)
        and stop["cleanupStatus"] == "not-executed"
        and stop["restartAuthority"] == "SYNTH-AUTHORITY-OWNER"
        and stop["automaticRestart"] is False,
        "stop/contact/recovery/cleanup",
    )
    need(
        [
            a[k]
            for k in (
                "sponsor",
                "authorityOwner",
                "systemOwner",
                "dataOwner",
                "testLead",
            )
        ]
        == list(ROLES)
        and a["authorizationId"] == p["authorizationRecordId"],
        "authority identity/roles",
    )
    need(
        ev["type"] == "authored-planning-record-not-observation"
        and ev["requiredFields"]
        == [
            "RoE ID and version",
            "Scope and Method IDs",
            "synthetic object ID",
            "time and custodian",
            "Source and limitation",
            "stop and disposition",
        ],
        "evidence not measured",
    )
    need(
        comp["technicalStatus"] == "not-executed"
        and comp["decisionStatus"] == "not-assessed"
        and comp["technicalCriteria"]
        == [
            "selected-records-accounted",
            "budget-and-stop-record-present",
            "cleanup-reference-present",
        ]
        and comp["decisionCriteria"]
        == [
            "required-question-answered-or-gap-recorded",
            "alternatives-and-confidence-recorded",
            "owner-acceptance-and-reassessment-recorded",
        ],
        "technical/decision completion",
    )
    need(
        c["triggers"]
        == [
            "scope",
            "method",
            "data",
            "time",
            "budget",
            "owner",
            "version",
            "stop",
            "retest",
        ]
        and c["newApprovalRequired"] is True
        and c["resumeAutomatically"] is False,
        "change/reauthorization boundary",
    )
    need(
        [x["handoffId"] for x in data["handoffs"]]
        == ["HOF-ROE09-001", "HOF-ROE09-002", "HOF-ROE09-003"]
        and [x["destination"] for x in data["handoffs"]]
        == ["Chapters10-14", "Chapter15", "Chapter21"]
        and all(x["status"] == "planned-not-delivered" for x in data["handoffs"]),
        "planned handoffs",
    )
    need(
        [x["inputIds"] for x in data["handoffs"]]
        == [
            [
                "ROE-2026-009 v1",
                "SCOPE-ROE09-001",
                "METHOD-ROE09-001",
                "STOP-ROE09-001",
            ],
            ["RET-ROE09-001", "REA-ROE09-001", "CR-ROE09-001"],
            ["ROE-2026-009 v1", "SCOPE-ROE09-001", "METHOD-ROE09-001"],
        ],
        "handoff direct references",
    )
    need(
        b["mode"] == "non-executing-planning-model"
        and b["expectedDisposition"] == "Do not proceed",
        "actual permission never issued",
    )
    try:
        for path in (
            ("record", "asOf"),
            ("parents", "authorizationExpiresAt"),
            ("decision", "historicalDeadline"),
            ("window", "startsAt"),
            ("window", "endsAt"),
            ("approval", "validFrom"),
            ("approval", "validUntil"),
            ("change", "reassessmentAt"),
        ):
            utc(data[path[0]][path[1]])
        start, end = utc(w["startsAt"]), utc(w["endsAt"])
        need(
            0 < (end - start).total_seconds() <= lim["minutes"] * 60,
            "bounded window duration",
        )
        need(
            a["validFrom"] == "2026-08-06T00:00:00Z"
            and a["validUntil"] == p["authorizationExpiresAt"],
            "authority interval not extended",
        )
        need(
            len(set(a["signoffs"])) == len(a["signoffs"])
            and set(a["signoffs"]) <= set(ROLES),
            "finite signoffs",
        )
        if r["status"] in ("Approved", "Active"):
            need(not conditions(data), "unmet declared approval conditions")
    except (ValueError, TypeError):
        errors.append("ART02 fixed UTC time")
    for path, value in leaves(data):
        if isinstance(value, str):
            location = "ART02/" + "/".join(path)
            errors += [
                location + ": " + f.category
                for f in scan_action_text(value, location=location)
                + scan_host_policy(value, location=location)
            ]
    return errors


def case_groups(data):
    """Every public JSON leaf has a reader-facing Case row, in source order."""
    yield (
        "model",
        [
            (k, v if isinstance(v, str) else json.dumps(v, ensure_ascii=False))
            for k, v in data.items()
            if not isinstance(v, (dict, list))
        ],
    )
    for group, value in data.items():
        if not isinstance(value, (dict, list)):
            continue
        rows = []
        for path, v in leaves(value):
            rendered = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
            rows.append((" / ".join(path), rendered))
        yield group, rows
