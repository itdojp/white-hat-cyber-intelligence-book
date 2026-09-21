"""ART-24 Layer A: bounded authored telemetry records, not a collection engine.

Coverage is calculated for one synthetic question and revision. Parent evidence,
authority, detection effectiveness and real Handoff delivery are never inferred.
"""

from __future__ import annotations

from datetime import datetime, timedelta
import hashlib
import json
import os
from pathlib import PurePosixPath
import stat

from scripts.check_editorial_input_manifest import (
    _reject_constant,
    _reject_duplicate_keys,
    validate_schema_instance,
)
from scripts.content_safety_policy import scan_action_text, scan_host_policy

DATA = "cases/fixtures/ch16-telemetry-coverage.json"
SCHEMA = "schemas/ch16-telemetry-coverage.schema.json"
CONTRACT = "tests/fixtures/chapter16/publication-contract.json"
DOCUMENTS = (
    "manuscript/16-telemetry-evidence-readiness.md",
    "templates/telemetry-coverage-map.md",
    "cases/ch16-telemetry-coverage-example.md",
    "references/ch16-source-review-2026-09-21.md",
)
PARENTS = (
    "WRITING_GUIDE.md",
    "SAFETY_SCOPE.md",
    "CROSS_BOOK_MAP.md",
    "PART_II_RECONCILIATION.md",
    "cases/part-ii-assessment-risk-map.md",
    "manuscript/05-attack-behavior.md",
    "cases/ch05-attack-behavior-example.md",
    "cases/fixtures/ch05-attack-behavior.json",
    "manuscript/06-observable-systems.md",
    "cases/ch06-signal-flow-example.md",
    "cases/fixtures/ch06-signal-flow.json",
    "manuscript/15-findings-retest-risk.md",
    "cases/ch15-findings-retest-risk-example.md",
    "cases/fixtures/ch15-findings-retest-risk.json",
    "manuscript/17-detection-engineering.md",
    "cases/ch17-detection-validation-example.md",
    "cases/fixtures/ch17-detection-engineering-fixture.json",
    "cases/ch02-authorization-decision-example.md",
    "cases/fixtures/ch09-engagement-roe.json",
    "scripts/content_safety_policy.py",
    "CONTENT_SAFETY_POLICY.md",
    "scripts/publication_projection.py",
    "scripts/_publication_projection_renderer.rb",
    "scripts/publication_text.py",
    "Gemfile.lock",
    "package-lock.json",
    ".book-formatter/revision.json",
)
INPUTS = (DATA, SCHEMA, CONTRACT, *DOCUMENTS, *PARENTS)
STAGES = ("Produced", "Collected", "Retained", "Queryable")
STATES = ("Required", *STAGES, "Validated", "Unknown")
SOURCES = (
    "SRC-ATTACK-001",
    "SRC-ATTACK-DET-001",
    "SRC-NIST-LOG-001",
    "SRC-NIST-LOG-DRAFT-001",
    "SRC-IR-001",
)


def strict(raw):
    return json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=_reject_duplicate_keys,
        parse_constant=_reject_constant,
    )


def read_regular(root, relative):
    """Fixed, bounded regular files; static Linux/WSL2 checks, not a race sandbox."""
    if relative not in INPUTS or root.is_symlink():
        raise ValueError("ART24 fixed input inventory/root")
    root = root.resolve(strict=True)
    current = root
    for part in PurePosixPath(relative).parts:
        current /= part
        if current.is_symlink():
            raise ValueError("ART24 symlink input/ancestor")
    if not current.resolve(strict=True).is_relative_to(root):
        raise ValueError("ART24 containment")
    if not all(hasattr(os, flag) for flag in ("O_NOFOLLOW", "O_NONBLOCK")):
        raise ValueError("ART24 Linux/WSL2 descriptor flags required")
    fd = os.open(current, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= 1024 * 1024:
            raise ValueError("ART24 bounded regular input")
        raw = stream.read(1024 * 1024 + 1)
    if len(raw) > 1024 * 1024:
        raise ValueError("ART24 input size")
    return raw


def digest(value):
    """Digest of the documented canonical JSON representation, not a signature."""
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode()
    ).hexdigest()


def utc(value):
    result = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    if result.strftime("%Y-%m-%dT%H:%M:%SZ") != value:
        raise ValueError("ART24 canonical UTC time")
    return result


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
    for group, value in data.items():
        records = value if isinstance(value, list) else [value]
        for item in records:
            title = group + (" " + item["id"] if isinstance(value, list) else "")
            rows = []
            for path, leaf in leaves(item):
                shown = (
                    leaf
                    if isinstance(leaf, str)
                    else json.dumps(leaf, ensure_ascii=False)
                )
                rows.append(("/".join(path) or group, shown))
            yield title, rows


def assess(row, requirement, fixture, receipts, original_digest):
    """Finite semantic kernel, independently tested without editorial snapshots.

    Requirements and original digest are trusted authored inputs, not expectations
    inferred from the observed payload. Return explicit supported state/conclusion.
    Malformed references are rejected, never silently treated as a lower state.
    """
    binding = {
        "rowId": row["id"],
        "questionId": requirement["id"],
        "fixtureId": fixture["id"],
        "subjectId": requirement["subjectId"],
        "revision": requirement["revision"],
    }
    if (
        row["questionId"] != requirement["id"]
        or row["fixtureId"] != fixture["id"]
        or requirement["rowId"] != row["id"]
        or any(
            fixture[k] != binding[k]
            for k in ("rowId", "questionId", "subjectId", "revision")
        )
        or any(row[k] != binding[k] for k in ("subjectId", "revision"))
    ):
        raise ValueError("ART24 question/fixture/subject/revision binding")
    ids = [r["id"] for r in receipts]
    if len(ids) != len(set(ids)) or len(row["receiptIds"]) != len(
        set(row["receiptIds"])
    ):
        raise ValueError("ART24 receipt identity uniqueness")
    stages = []
    for rid in row["receiptIds"]:
        if rid not in ids:
            raise ValueError("ART24 missing receipt")
        proof = receipts[ids.index(rid)]
        if any(proof[k] != v for k, v in binding.items()):
            raise ValueError(
                "ART24 receipt belongs to another question/subject/version"
            )
        stages.append(proof["stage"])
    if stages != list(STAGES[: len(stages)]):
        raise ValueError("ART24 each claimed stage needs its own ordered receipt")
    start, end = utc(requirement["windowStart"]), utc(requirement["windowEnd"])
    deadline = utc(requirement["decisionDeadline"])
    if not start < end <= deadline:
        raise ValueError("ART24 question time bounds")
    # Quality fields remain well-formed even when coverage stops at an earlier stage.
    retention_start, retention_end = (
        utc(row["retentionStart"]),
        utc(row["retentionEnd"]),
    )
    if retention_start >= retention_end:
        raise ValueError("ART24 retention time bounds")
    for name in ("clockUncertaintySeconds", "ingestDelaySeconds"):
        if type(row[name]) is not int or row[name] < 0:
            raise ValueError("ART24 quality field type/range")
    fixed = {
        "producerId": "SYNTH-PRODUCER-TCM16",
        "collectorId": "SYNTH-COLLECTOR-TCM16",
        "transport": "offline-supplied-records",
        "schemaVersion": "TCM16-EVENT-1",
        "clockSource": "SYNTH-UTC-CLOCK",
        "timezone": "UTC",
        "accessRole": "SYNTH-" + requirement["consumer"].upper() + "-READER",
    }
    if any(row[k] != v for k, v in fixed.items()):
        raise ValueError(
            "ART24 supplied producer/collector/schema/clock/access boundary"
        )
    if row["processingBasis"] == "unknown":
        if stages:
            raise ValueError("ART24 unknown processing basis with claimed collection")
        return "Unknown", "privacy-basis-unknown"
    if (
        row["processingBasis"] != "synthetic-reading-only"
        or row["classification"] != requirement["classification"]
        or not row["accessRole"].startswith("SYNTH-")
    ):
        raise ValueError("ART24 bounded data handling")
    if not stages:
        return "Required", "producer-evidence-missing"
    if len(stages) == 1:
        return "Produced", "collector-evidence-missing"
    retention_start, retention_end = (
        utc(row["retentionStart"]),
        utc(row["retentionEnd"]),
    )
    if (
        retention_start > start
        or retention_end < deadline
        or retention_end - start < timedelta(days=requirement["requiredRetentionDays"])
    ):
        return "Collected", "retention-gap"
    if len(stages) == 2:
        return "Collected", "retention-evidence-missing"
    if len(stages) == 3:
        return "Retained", "query-evidence-missing"
    if (
        type(row["clockUncertaintySeconds"]) is not int
        or row["clockUncertaintySeconds"] < 0
        or row["timezone"] != "UTC"
        or not row["clockSource"]
    ):
        raise ValueError("ART24 clock field type/range")
    if row["clockUncertaintySeconds"] > requirement["maximumClockUncertaintySeconds"]:
        return "Queryable", "clock-uncertainty"
    if (
        row["normalizerVersion"] != requirement["normalizerVersion"]
        or row["identityNamespace"] != requirement["identityNamespace"]
    ):
        return "Queryable", "identity-normalization-mismatch"
    if type(row["ingestDelaySeconds"]) is not int or row["ingestDelaySeconds"] < 0:
        raise ValueError("ART24 delay field type/range")
    if row["ingestDelaySeconds"] > requirement["maximumIngestDelaySeconds"]:
        return "Queryable", "ingest-delay"
    if digest(fixture) != original_digest:
        return "Queryable", "original-byte-mismatch"
    required = [f["name"] for f in requirement["requiredFields"]]
    if (
        not required
        or len(required) != len(set(required))
        or any(
            not f["purpose"] or f["consumer"] != requirement["consumer"]
            for f in requirement["requiredFields"]
        )
    ):
        raise ValueError("ART24 field purpose/consumer")
    for event in fixture["records"]:
        if any(k not in event or event[k] is None or event[k] == "" for k in required):
            return "Queryable", "required-field-missing"
        if (
            event["target_workload_id"] != requirement["subjectId"]
            or event["event_type"] != requirement["eventType"]
        ):
            raise ValueError("ART24 event subject/type")
        occurred, observed, ingested = (
            utc(event[k]) for k in ("event_time", "observed_time", "ingest_time")
        )
        if (
            not start <= occurred <= end
            or not occurred <= observed <= ingested <= deadline
        ):
            return "Queryable", "event-time-bounds"
        if (ingested - occurred).total_seconds() > requirement[
            "maximumIngestDelaySeconds"
        ]:
            return "Queryable", "ingest-delay"
    if (
        fixture["eventPresence"] == "absent"
        and not fixture["records"]
        and fixture["observationWindowComplete"] is True
    ):
        return "Validated", "not-observed-in-synthetic-window"
    if fixture["eventPresence"] == "present" and fixture["records"]:
        return "Validated", "bounded-input-contract-satisfied"
    return "Queryable", "observation-coverage-unknown"


def validate_model(data, schema, contract):
    validate_schema_instance(data, schema)
    errors = []
    if tuple(data["record"]["coverageStates"]) != STATES:
        errors.append("ART24 seven-state vocabulary/order")
    for name, expected in contract["authoredInputs"].items():
        if digest(data[name]) != expected:
            errors.append("ART24 authored input changed: " + name)
    for kind in ("requirements", "fixtures", "receipts", "rows", "handoffs"):
        ids = [r["id"] for r in data[kind]]
        if len(ids) != len(set(ids)):
            errors.append("ART24 duplicate identity: " + kind)
    requirements = {q["id"]: q for q in data["requirements"]}
    for i, row in enumerate(data["rows"], 1):
        req = requirements[row["questionId"]]
        fixture = next(f for f in data["fixtures"] if f["id"] == row["fixtureId"])
        expected = assess(
            row,
            req,
            fixture,
            data["receipts"],
            contract["fixtureDigests"][fixture["id"]],
        )
        if (row["coverage"], row["allowedConclusion"]) != expected:
            errors.append(f"ART24 {row['id']} expected {expected}")
        suffix = f"{i:03}"
        for field, prefix in [
            ("id", "ROW"),
            ("testId", "TEST"),
            ("validationId", "VAL"),
            ("validationEvidenceId", "EVD-TEST"),
            ("gapId", "GAP"),
        ]:
            if row[field] != f"{prefix}-TCM16-{suffix}":
                errors.append("ART24 finite test/evidence/gap identity: " + field)
        if (
            not row["gap"]
            or not row["owner"]
            or not row["reassessment"]
            or utc(row["dueAt"]) <= utc(data["record"]["asOf"])
        ):
            errors.append("ART24 gap/owner/due/reassessment")
        if (
            row["integrityReference"] != "SYNTH-ORIGINAL-TCM16-" + suffix
            or row["integrityMeaning"] != "supplied-byte-comparison-not-authenticity"
        ):
            errors.append("ART24 original reference scope")
    for handoff in data["handoffs"]:
        owned = [
            r["id"]
            for r in data["rows"]
            if requirements[r["questionId"]]["consumer"] == handoff["consumer"]
        ]
        if handoff["rowIds"] != owned:
            errors.append("ART24 handoff consumer ownership")
    for path, value in leaves(data):
        if isinstance(value, str):
            where = DATA + "/" + "/".join(path)
            errors += [
                where + ": " + f.category
                for f in (
                    *scan_action_text(value, location=where),
                    *scan_host_policy(value, location=where),
                )
            ]
    return errors
