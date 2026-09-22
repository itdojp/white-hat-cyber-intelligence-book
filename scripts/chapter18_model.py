"""ART-06 authored input, evidence binding and judgment contract (Layer A)."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import PurePosixPath
import stat

from scripts.chapter18_query import PLAN, RESULTS, evaluate
from scripts.check_editorial_input_manifest import (
    _reject_constant,
    _reject_duplicate_keys,
    validate_schema_instance,
)
from scripts.content_safety_policy import scan_action_text, scan_host_policy

DATA = "cases/fixtures/ch18-threat-hunting.json"
SCHEMA = "schemas/ch18-threat-hunting.schema.json"
CONTRACT = "tests/fixtures/chapter18/publication-contract.json"
CORPUS = "tests/fixtures/chapter18/query-corpus.json"
DOCUMENTS = (
    "manuscript/18-threat-hunting.md",
    "templates/hunt-report.md",
    "cases/ch18-hunt-plan-example.md",
    "references/ch18-source-review-2026-09-22.md",
)
PARENTS = (
    "WRITING_GUIDE.md",
    "SAFETY_SCOPE.md",
    "CROSS_BOOK_MAP.md",
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
SOURCES = ("SRC-ATTACK-001", "SRC-ATTACK-DET-001", "SRC-IR-001")


def strict(raw):
    return json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=_reject_duplicate_keys,
        parse_constant=_reject_constant,
    )


def read_regular(root, relative):
    """Bounded authored regular files; static Linux/WSL2 checks, not a sandbox."""
    if relative not in INPUTS or root.is_symlink():
        raise ValueError("ART06 fixed input inventory/root")
    root = root.resolve(strict=True)
    current = root
    for part in PurePosixPath(relative).parts:
        current /= part
        if current.is_symlink():
            raise ValueError("ART06 symlink input/ancestor")
    if not current.resolve(strict=True).is_relative_to(root):
        raise ValueError("ART06 containment")
    if not all(hasattr(os, flag) for flag in ("O_NOFOLLOW", "O_NONBLOCK")):
        raise ValueError("ART06 Linux/WSL2 descriptor flags required")
    fd = os.open(current, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= 1024 * 1024:
            raise ValueError("ART06 bounded regular input")
        raw = stream.read(1024 * 1024 + 1)
    if len(raw) > 1024 * 1024:
        raise ValueError("ART06 input size")
    return raw


def digest(value):
    """Hash fixed JSON representation; neither a signature nor authenticity proof."""
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
    """Artifact fields in the Case; raw query inputs are linked JSON, not prose."""
    groups = [(k, data[k]) for k in ("record", "parents", "safety", "plan")]
    for row in data["contrasts"]:
        groups.append((row["id"], {k: v for k, v in row.items() if k != "input"}))
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


def validate_model(data, schema, contract):
    validate_schema_instance(data, schema)
    errors = []
    # These safety claims are semantic invariants, not editorial snapshot values.
    # Refreshing authored hashes or projected Case fields cannot authorize them.
    if (
        data["record"]["actualCollections"] != 0
        or data["record"]["actualIncidents"] != 0
        or data["safety"]["personalDataIncluded"] is not False
        or data["safety"]["productSchemaClaimed"] is not False
    ):
        errors.append("ART06 synthetic-only record claims")
    if tuple(data["record"]["resultStates"]) != RESULTS or data["plan"] != PLAN:
        errors.append("ART06 frozen query plan / five results")
    for key, expected in contract["authoredInputs"].items():
        if digest(data[key]) != expected:
            errors.append("ART06 authored input changed: " + key)
    ids = [row["id"] for row in data["contrasts"]]
    if ids != [f"HCASE18-{i:03}" for i in range(1, 13)]:
        errors.append("ART06 finite contrast inventory/order")
    for index, row in enumerate(data["contrasts"], 1):
        suffix = f"{index:03}"
        actual = evaluate(row["input"])
        if actual != row["queryResult"]:
            errors.append(row["id"] + ": result is not supported by the supplied input")
        supply = row["supplyEvidence"]
        if (
            supply["id"] != "SUP-HUNT18-" + suffix
            or supply["inputId"] != "FIX-HUNT18-" + suffix
            or supply["queryId"] != "QRY-HUNT18-001"
            or supply["subject"] != PLAN["subject"]
            or supply["revision"] != PLAN["revision"]
            or supply["inputDigest"] != digest(row["input"])
            or supply["inputDigest"] != contract["inputDigests"][row["id"]]
            or supply["meaning"] != "supplied-fixture-comparison-not-authenticity"
        ):
            errors.append(row["id"] + ": supplied evidence binding/digest")
        judgment = row["judgment"]
        if (
            judgment["result"] != actual["result"]
            or judgment["findingId"] != "FND-HUNT18-" + suffix
            or judgment["gapId"] != "GAP-HUNT18-" + suffix
            or judgment["reassessmentId"] != "REA-HUNT18-" + suffix
            or judgment["confidence"] not in ("高", "中", "低")
            or judgment["noCompromiseClaim"] is not False
            or judgment["dueAt"] != "2026-09-30T00:00:00Z"
            or any(
                not judgment[k]
                for k in (
                    "permittedConclusion",
                    "alternative",
                    "confidenceBasis",
                    "gap",
                    "nextAction",
                    "owner",
                    "reassessment",
                )
            )
        ):
            errors.append(row["id"] + ": judgment/owner/gap/reassessment boundary")
        expected_routes = [h["route"] for h in actual["handoffs"]]
        if [h["route"] for h in row["handoffs"]] != expected_routes:
            errors.append(row["id"] + ": handoff purpose ownership")
        for n, h in enumerate(row["handoffs"], 1):
            if (
                h["id"] != f"HOF-HUNT18-{suffix}-{n}"
                or h["backlogId"] != f"BKL-HUNT18-{suffix}-{n}"
                or h["targetChapter"]
                != {
                    "detection-review": 17,
                    "incident-triage-review": 19,
                    "collection-review": 16,
                    "scope-review": 18,
                    "reassessment": 18,
                }.get(h["route"])
                or h["owner"] != judgment["owner"]
                or h["dueAt"] != judgment["dueAt"]
                or h["sourceFindingId"] != judgment["findingId"]
                or h["sourceSupplyId"] != supply["id"]
                or h["status"] != "planned-not-delivered"
                or h["receiptId"] is not None
                or h["executionAuthorized"] is not False
            ):
                errors.append(row["id"] + ": handoff binding/no delivery/no authority")
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
