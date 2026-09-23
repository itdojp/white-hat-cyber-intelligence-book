"""ART25 supplied records, exact claims and Case parity (chapter semantics only)."""

import hashlib
import json
import os
from pathlib import PurePosixPath
import stat

from scripts.chapter19_decisions import STATES, OPTIONS, evaluate, instant
from scripts.chapter19_judgments import PROFILES
from scripts.check_editorial_input_manifest import (
    _reject_constant,
    _reject_duplicate_keys,
    validate_schema_instance,
)
from scripts.content_safety_policy import scan_action_text, scan_host_policy

DATA = "cases/fixtures/ch19-incident-response.json"
SCHEMA = "schemas/ch19-incident-response.schema.json"
CONTRACT = "tests/fixtures/chapter19/publication-contract.json"
CORPUS = "tests/fixtures/chapter19/decision-corpus.json"
DOCUMENTS = (
    "manuscript/19-incident-response.md",
    "templates/incident-action-plan.md",
    "cases/ch19-incident-action-plan-example.md",
    "references/ch19-source-review-2026-09-23.md",
)
PARENTS = (
    "WRITING_GUIDE.md",
    "SAFETY_SCOPE.md",
    "CROSS_BOOK_MAP.md",
    "manuscript/15-findings-retest-risk.md",
    "manuscript/16-telemetry-evidence-readiness.md",
    "templates/telemetry-coverage-map.md",
    "cases/ch16-telemetry-coverage-example.md",
    "cases/fixtures/ch16-telemetry-coverage.json",
    "manuscript/17-detection-engineering.md",
    "templates/detection-validation.md",
    "cases/ch17-detection-validation-example.md",
    "cases/fixtures/ch17-detection-engineering-fixture.json",
    "detections/cloud_identity/det_2026_017_001.json",
    "scripts/replay_chapter17_detection.py",
    "manuscript/18-threat-hunting.md",
    "templates/hunt-report.md",
    "cases/ch18-hunt-plan-example.md",
    "cases/fixtures/ch18-threat-hunting.json",
    "scripts/content_safety_policy.py",
    "CONTENT_SAFETY_POLICY.md",
    "scripts/publication_projection.py",
    "scripts/_publication_projection_renderer.rb",
    "scripts/publication_text.py",
    "Gemfile.lock",
    "package-lock.json",
    ".book-formatter/revision.json",
)
INPUTS = (DATA, SCHEMA, CONTRACT, CORPUS, *DOCUMENTS, *PARENTS)
SOURCES = ("SRC-CSF-001", "SRC-IR-001")


def strict(raw):
    return json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=_reject_duplicate_keys,
        parse_constant=_reject_constant,
    )


def read_regular(root, relative):
    """Fixed, bounded regular input on Linux/WSL2; not a filesystem sandbox."""
    if relative not in INPUTS or root.is_symlink():
        raise ValueError("ART25 fixed input inventory/root")
    root = root.resolve(strict=True)
    path = root
    for part in PurePosixPath(relative).parts:
        path /= part
        if path.is_symlink():
            raise ValueError("ART25 symlink input/ancestor")
    if not path.resolve(strict=True).is_relative_to(root):
        raise ValueError("ART25 input containment")
    if not all(hasattr(os, flag) for flag in ("O_NOFOLLOW", "O_NONBLOCK")):
        raise ValueError("ART25 Linux/WSL2 descriptor flags required")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= 1024 * 1024:
            raise ValueError("ART25 bounded regular input")
        raw = stream.read(1024 * 1024 + 1)
    if len(raw) > 1024 * 1024:
        raise ValueError("ART25 input size")
    return raw


def digest(value):
    """Representation comparison only, never authenticity or authority."""
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode()
    ).hexdigest()


def leaves(value, path=()):
    if isinstance(value, dict):
        for k, v in value.items():
            yield from leaves(v, path + (k,))
    elif isinstance(value, list) and value:
        for i, v in enumerate(value):
            yield from leaves(v, path + (str(i),))
    else:
        yield path, value


def case_groups(data):
    """Every ART25 field; detailed evidence input is the linked JSON download."""
    groups = [
        (k, data[k])
        for k in ("record", "parents", "roles", "safety", "notification", "options")
    ]
    for row in data["contrasts"]:
        displayed = {k: v for k, v in row.items() if k != "input"}
        displayed["input"] = {k: v for k, v in row["input"].items() if k != "evidence"}
        groups.append((row["id"], displayed))
    for title, value in groups:
        yield (
            title,
            [
                (
                    "/".join(p),
                    v if isinstance(v, str) else json.dumps(v, ensure_ascii=False),
                )
                for p, v in leaves(value)
            ],
        )


def role_references(data):
    """Finite global coordination roles, not record-specific residual-risk owners."""
    yield ("notification", "escalationOwner"), "legalPrivacyReviewer"
    bindings = (
        (("previous", "owner"), "decisionOwner"),
        (("decision", "owner"), "decisionOwner"),
        (("declaration", "owner"), "decisionOwner"),
        (("preservation", "owner"), "evidenceLead"),
        (("containment", "authority", "owner"), "incidentCommander"),
        (("recovery", "owner"), "recoveryOwner"),
        (("closure", "owner"), "decisionOwner"),
        (("previous", "closure", "owner"), "decisionOwner"),
        (("reopening", "owner"), "decisionOwner"),
    )
    for i, row in enumerate(data["contrasts"]):
        for path, role in bindings:
            value = row["input"]
            for key in path:
                if value is None:
                    break
                value = value[key]
            if value is not None:
                yield ("contrasts", i, "input", *path), role
        for j in range(len(row["handoffs"])):
            yield ("contrasts", i, "handoffs", j, "owner"), "incidentCommander"


def validate_model(data, schema, contract):
    validate_schema_instance(data, schema)
    errors = []
    roles = data["roles"]
    if any(not value.strip() for value in roles.values()):
        errors.append("ART25 nonempty coordination role registry")
    for path, role in role_references(data):
        value = data
        for key in path:
            value = value[key]
        if value != roles[role]:
            errors.append("ART25 role-owner binding: " + "/".join(map(str, path)))
    timestamp_fields = {
        "asOf",
        "at",
        "dueAt",
        "start",
        "end",
        "windowStart",
        "windowEnd",
        "availableAt",
        "approvedAt",
        "expiresAt",
    }
    for path, value in leaves(data):
        if path[-1] in timestamp_fields and isinstance(value, str):
            instant(value)
    if tuple(data["record"]["sourceIds"]) != SOURCES:
        errors.append("ART25 Source identity traceability")
    if tuple(data["record"]["states"]) != STATES:
        errors.append("ART25 seven-state inventory/order")
    # Keep safety assertions meaningful even after authored snapshots are refreshed.
    if any(
        data["record"][k] != 0
        for k in (
            "actualIncidents",
            "actualActions",
            "actualNotifications",
            "actualCollections",
        )
    ) or any(
        data["safety"][k] is not False
        for k in (
            "personalDataIncluded",
            "notificationAutomaticallyDetermined",
            "receiptAuthenticityClaimed",
        )
    ):
        errors.append("ART25 synthetic-only claims")
    if data["options"] != [{"id": k, **v} for k, v in OPTIONS.items()]:
        errors.append("ART25 reviewed option/impact/rollback profiles")
    if set(contract["authoredInputs"]) != set(data):
        errors.append("ART25 complete authored input inventory")
    for key, expected in contract["authoredInputs"].items():
        if digest(data[key]) != expected:
            errors.append("ART25 authored input changed: " + key)
    if [r["id"] for r in data["contrasts"]] != [
        f"ICASE19-{i:03}" for i in range(1, 13)
    ]:
        errors.append("ART25 finite contrast inventory/order")
    for i, row in enumerate(data["contrasts"], 1):
        suf = f"{i:03}"
        inp = row["input"]
        if instant(inp["decision"]["at"]) > instant(data["record"]["asOf"]):
            errors.append("ART25 decision after record as-of")
        if (
            inp["incidentId"] != "INC-IR19-" + suf
            or inp["threatQuestionId"] != "THQ-IR19-" + suf
        ):
            errors.append("ART25 incident/threat question identity")
        result = evaluate(inp)
        if row["expected"] != result:
            errors.append(row["id"] + ": supplied decision does not support claim")
        if row["judgment"] != PROFILES.get(row["id"]):
            errors.append(row["id"] + ": reviewed finite judgment profile")
        profile = PROFILES.get(row["id"])
        if profile is None or inp["decision"]["reason"] != profile["conclusion"]:
            errors.append(row["id"] + ": reviewed decision reason profile")
        action = inp["containment"]
        if action is not None:
            option = OPTIONS[action["optionId"]]
            if (
                action["expectedImpact"] != option["business"]
                or action["rollback"] != option["rollback"]
            ):
                errors.append(
                    row["id"] + ": reviewed containment impact/rollback profile"
                )
        if (
            inp["context"]["subject"] != "SYNTH-IR19-" + suf
            or inp["context"]["revision"] != "REV-IR19-" + suf
            or inp["decision"]["id"] != "DEC-IR19-" + suf
        ):
            errors.append("ART25 synthetic subject/revision/decision identity")
        if any(
            row[k] != prefix + suf
            for k, prefix in (
                ("timelineId", "TL-IR19-"),
                ("findingId", "FND-IR19-"),
                ("controlId", "CTL-IR19-"),
                ("reassessmentId", "REA-IR19-"),
            )
        ):
            errors.append("ART25 direct traceability IDs")
        if [h["targetChapter"] for h in row["handoffs"]] != [20, 22, 26]:
            errors.append("ART25 finite handoff routes/order")
        for h, prefix in zip(row["handoffs"], ("TL", "BKL", "CTI")):
            ch = h["targetChapter"]
            if instant(h["dueAt"]) < instant(inp["decision"]["at"]):
                errors.append("ART25 handoff deadline before source decision")
            if (
                h["id"] != f"HOF-IR19-{suf}-{ch}"
                or h["questionId"] != f"EQ-IR19-{suf}-{ch}"
                or h["plannedRecordId"] != f"{prefix}-IR19-{suf}"
                or h["sourceDecisionId"] != inp["decision"]["id"]
                or h["status"] != "planned-not-delivered"
                or h["receiptId"] is not None
                or h["executionAuthorized"] is not False
            ):
                errors.append("ART25 undelivered direct handoff identity")
    for path, value in leaves(data):
        if isinstance(value, str):
            location = DATA + ":" + "/".join(path)
            for finding in (
                *scan_action_text(value, location=location),
                *scan_host_policy(value, location=location),
            ):
                errors.append(f"{location}: {finding.category}: {finding.reason}")
    return errors
