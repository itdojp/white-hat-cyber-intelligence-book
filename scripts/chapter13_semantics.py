"""Chapter13 Layer A: finite supplied ART21 references and evidence ceilings.

No real build/deploy/crypto or network. Not a generic attestation/schema parser.
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
DATA_PATH = "cases/fixtures/ch13-supply-chain.json"
SCHEMA_PATH = "schemas/ch13-supply-chain.schema.json"
CONTRACT_PATH = "tests/fixtures/chapter13/publication-contract.json"
DOCUMENTS = (
    "manuscript/13-platform-supply-chain.md",
    "templates/platform-supply-chain-assessment.md",
    "cases/ch13-platform-supply-chain-example.md",
    "references/ch13-source-review-2026-09-15.md",
)
PARENTS = (
    "cases/ch01-integrated-security-case-example.md",
    "cases/ch02-authorization-decision-example.md",
    "cases/ch04-threat-model-example.md",
    "cases/ch08-lab-evidence-example.md",
    "cases/fixtures/ch08-lab-plan.json",
    "manuscript/09-engagement-roe.md",
    "templates/rules-of-engagement.md",
    "cases/ch09-engagement-roe-example.md",
    "cases/fixtures/ch09-engagement-roe.json",
    "schemas/ch09-engagement-roe.schema.json",
    "references/ch09-source-review-2026-09-13.md",
    "cases/ch11-web-api-assessment-example.md",
    "CONTENT_SAFETY_POLICY.md",
    "scripts/content_safety_policy.py",
    "scripts/publication_projection.py",
    "scripts/_publication_projection_renderer.rb",
    "scripts/publication_text.py",
    "Gemfile.lock",
    "package-lock.json",
    ".book-formatter/revision.json",
    "CROSS_BOOK_MAP.md",
    "manuscript/04-assets-boundaries-threat-model.md",
    "manuscript/06-observable-systems.md",
    "cases/ch06-signal-flow-example.md",
    "cases/fixtures/ch06-signal-flow.json",
    "manuscript/10-recon-osint-boundary.md",
    "templates/attack-surface-register.md",
    "cases/ch10-attack-surface-example.md",
    "cases/fixtures/ch10-attack-surface.json",
    "cases/fixtures/ch10-source-bundle.json",
    "schemas/ch10-attack-surface.schema.json",
    "references/ch10-source-review-2026-09-14.md",
    "manuscript/11-web-api-hypothesis.md",
    "cases/fixtures/ch11-web-api-assessment-dataset.json",
    "manuscript/12-enterprise-identity.md",
    "templates/identity-attack-path-review.md",
    "cases/ch12-identity-path-review-example.md",
    "references/ch12-source-review-2026-09-15.md",
    "cases/fixtures/ch12-identity-paths.json",
    "schemas/ch12-identity-paths.schema.json",
)
INPUTS = (DATA_PATH, SCHEMA_PATH, CONTRACT_PATH, *DOCUMENTS, *PARENTS)
STATES = ("Declared", "Observed", "Verified", "Rejected", "Unknown")


def strict_bytes(raw):
    return json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=_reject_duplicate_keys,
        parse_constant=_reject_constant,
    )


def read_regular(root: Path, relative: str):
    """Fixed publication inputs only; static symlink/special/size rejection.

    Requires Linux/WSL2. Not a concurrent hostile-filesystem sandbox.
    """
    if relative not in INPUTS or root.is_symlink():
        raise ValueError("ART21 fixed input inventory/root")
    if any(type(getattr(os, f, None)) is not int for f in ("O_NOFOLLOW", "O_NONBLOCK")):
        raise ValueError("ART21 requires Linux/WSL2 no-follow/nonblocking primitives")
    root = root.resolve(strict=True)
    current = root
    for part in PurePosixPath(relative).parts:
        current /= part
        if current.is_symlink():
            raise ValueError("ART21 symlink input/ancestor")
    if not current.resolve(strict=True).is_relative_to(root):
        raise ValueError("ART21 input containment")
    fd = os.open(current, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= 1024 * 1024:
            raise ValueError("ART21 bounded regular input required")
        raw = stream.read(1024 * 1024 + 1)
    if len(raw) > 1024 * 1024:
        raise ValueError("ART21 input size")
    return raw


def utc(value):
    parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    if parsed.strftime("%Y-%m-%dT%H:%M:%SZ") != value:
        raise ValueError("ART21 canonical UTC time")
    return parsed


def leaves(value, path=()):
    """Structured JSON paths, not reader projection or renderer syntax."""
    if isinstance(value, dict):
        for k, v in value.items():
            yield from leaves(v, path + (k,))
    elif isinstance(value, list) and value:
        for i, v in enumerate(value):
            yield from leaves(v, path + (str(i),))
    else:
        yield path, value


def case_groups(data):
    """Every JSON leaf has a visible Field/Value row, grouped by owned record."""
    for group, value in data.items():
        records = (
            list(enumerate(value, 1)) if isinstance(value, list) else [(None, value)]
        )
        for number, record in records:
            title = group if number is None else f"{group} {record['id']}"
            rows = []
            for path, item in leaves(record):
                label = "/".join(path) or group
                shown = (
                    item
                    if isinstance(item, str)
                    else json.dumps(item, ensure_ascii=False)
                )
                rows.append((label, shown))
            yield title, rows


"""Finite authored comparison; noncanonical spike, no parsing or execution."""


def compare(chain, expected):
    if (
        chain["id"] != expected["chainId"]
        or chain["recordRevision"] != expected["recordRevision"]
        or chain["evidence"]["expectationId"] != expected["id"]
    ):
        raise ValueError("assessment/expectation/version binding")
    # Structural references are checked by the shaped-input owner before this
    # pure kernel. Contradictions win over missing evidence for this conjunction.
    checks = []

    def match(name, a, b):
        checks.append((name, None if a is None or b is None else a == b))

    s, b, a, p, r, u = [
        chain[k]
        for k in ["source", "build", "artifact", "provenance", "registry", "runtime"]
    ]
    checks.append(("mutable-source-only", s["refLabel"] != "mutable-branch-only"))
    checks.append(
        (
            "unversioned-action",
            chain["action"]["version"] != "unversioned"
            and chain["action"]["review"] == "Reviewed summary",
        )
    )
    match("runner-permission-mismatch", b["permission"], expected["permission"])
    for key in [
        "sourceRevision",
        "lockDigest",
        "builderId",
        "runnerClass",
        "isolation",
        "network",
        "cache",
        "workloadPrincipalId",
        "secretClassId",
    ]:
        match("build-" + key + "-mismatch", b[key], expected[key])
    match("source-revision-mismatch", s["revision"], expected["sourceRevision"])
    match("source-lock-mismatch", s["lockDigest"], expected["lockDigest"])
    match(
        "action-revision-mismatch",
        chain["action"]["revision"],
        expected["actionRevision"],
    )
    match("artifact-digest-mismatch", a["digest"], expected["artifactDigest"])
    for key, value in [
        ("artifactId", a["id"]),
        ("subjectDigest", a["digest"]),
        ("sourceRevision", s["revision"]),
        ("lockDigest", s["lockDigest"]),
        ("builderId", expected["builderId"]),
        ("buildType", expected["buildType"]),
        ("parameters", expected["parameters"]),
    ]:
        match("provenance-" + key + "-mismatch", p[key], value)
    for key in ["registry", "promotion", "deployment", "runtime"]:
        match(
            key + "-digest-mismatch", chain[key]["digest"], expected["artifactDigest"]
        )
    match(
        "runtime-boundary-mismatch",
        u["boundaryId"],
        expected["expectedRuntimeBoundary"],
    )
    match(
        "dependency-review-mismatch", chain["dependency"]["review"], "Reviewed summary"
    )
    for reason, value in checks:
        if value is False:
            return "Rejected", reason
    if any(v is None for _, v in checks):
        return "Unknown", "provenance-missing" if p[
            "artifactId"
        ] is None else "necessary-record-missing"
    basis = chain["evidence"]["basis"]
    if basis == "Declared summary":
        return "Declared", "declaration-only"
    if basis == "Observed summary":
        return "Observed", "observation-only"
    if basis == "Compared summary":
        return "Verified", "all-supplied-bindings-match"
    raise ValueError("unknown evidence basis")


def validate_model(data, schema, contract):
    """Validate the supplied finite teaching record, not arbitrary attestations."""
    errors = []

    def need(ok, message):
        if not ok:
            errors.append("ART21 " + message)

    try:
        validate_supported_schema_nodes(schema, "ART21-schema", schema)
        validate_schema_instance(data, schema)
    except (ManifestError, ValueError, TypeError, KeyError) as exc:
        return ["ART21 closed supplied schema: " + str(exc)]
    for k, value in contract["fixedContext"].items():
        need(data[k] == value, "unchanged fixed context " + k)
    need(
        data["expectations"] == contract["expectations"], "separate frozen expectations"
    )
    need(
        [c["id"] for c in data["chains"]] == [f"CHN-PSA13-{i:03}" for i in range(1, 9)],
        "finite unique ordered chains",
    )
    if errors:
        return errors
    prefixes = {
        "source": "SRC",
        "dependency": "DEP",
        "action": "ACT",
        "build": "BLR",
        "artifact": "OBJ",
        "provenance": "PROV",
        "registry": "REG",
        "promotion": "PROM",
        "deployment": "DPL",
        "runtime": "RUN",
        "evidence": "EVD",
        "finding": "FND",
        "decision": "DEC",
    }
    for i, (c, e) in enumerate(zip(data["chains"], data["expectations"]), 1):

        def rid(kind):
            return f"{kind}-PSA13-{i:03}"

        need(
            c["recordRevision"] == data["record"]["revision"]
            and c["platformId"] == data["platform"]["id"],
            "chain revision/platform " + c["id"],
        )
        for group, prefix in prefixes.items():
            need(
                c[group]["id"] == rid(prefix),
                "owned record ID " + c["id"] + "/" + group,
            )
        s, b, a, p, r, m, d, u, v, f, z = [
            c[k]
            for k in [
                "source",
                "build",
                "artifact",
                "provenance",
                "registry",
                "promotion",
                "deployment",
                "runtime",
                "evidence",
                "finding",
                "decision",
            ]
        ]
        bindings = [
            (s["lockId"], rid("LCK")),
            (c["dependency"]["lockId"], s["lockId"]),
            (b["sourceId"], s["id"]),
            (b["lockId"], s["lockId"]),
            (b["logId"], rid("LOG")),
            (a["buildId"], b["id"]),
            (a["sbomId"], rid("SBM")),
            (a["sbomDependencyId"], c["dependency"]["id"]),
            (r["artifactId"], a["id"]),
            (m["registryId"], r["id"]),
            (m["artifactId"], a["id"]),
            (m["reviewerPrincipalId"], data["principals"][0]["id"]),
            (d["promotionId"], m["id"]),
            (d["runtimeBoundaryId"], data["platform"]["runtimeBoundaryId"]),
            (u["deploymentId"], d["id"]),
            (u["controlPlaneId"], data["platform"]["controlPlaneId"]),
            (u["dataPlaneId"], data["platform"]["dataPlaneId"]),
            (v["chainId"], c["id"]),
            (v["recordRevision"], c["recordRevision"]),
            (v["expectationId"], e["id"]),
            (v["sourceId"], s["id"]),
            (v["buildLogId"], b["logId"]),
            (v["artifactId"], a["id"]),
            (v["runtimeId"], u["id"]),
            (f["chainId"], c["id"]),
            (f["evidenceId"], v["id"]),
            (f["threatId"], data["parentIdentity"]["threatId"]),
            (f["signalFlowId"], data["parentIdentity"]["signalFlowId"]),
            (z["findingId"], f["id"]),
            (z["reassessmentId"], rid("REA")),
            (f["treatmentId"], rid("TRT")),
            (z["treatmentId"], f["treatmentId"]),
            (f["telemetryPlanId"], rid("TEL")),
            (b["secretClassId"], data["principals"][1]["secretClassId"]),
        ]
        for j, (actual, expected) in enumerate(bindings):
            need(actual == expected, "direct binding " + c["id"] + "/" + str(j))
        need(
            m["status"] == "Planned-only"
            and m["approved"] is False
            and d["status"] == "Planned-only"
            and u["status"] == "Authored-snapshot-not-deployed",
            "no operational promotion " + c["id"],
        )
        need(
            z["executionAuthorized"] is False and z["disposition"] == "Record-only",
            "decision not authorization " + c["id"],
        )
        need(
            a["signatureStatus"] == "Recorded-unverified"
            and a["sbomFormat"] == "book-summary-not-SPDX"
            and a["sbomCompleteness"] == "Not assessed"
            and p["format"] == "book-summary-not-SLSA"
            and r["trust"] == "Not assessed",
            "no signature/standard/safety claim " + c["id"],
        )
        need(v["synthetic"] is True, "authored evidence " + c["id"])
        try:
            need(
                utc(v["recordedAt"]) <= utc(data["record"]["asOf"]) < utc(f["dueAt"]),
                "evidence/reassessment time " + c["id"],
            )
            actual, reason = compare(c, e)
            need(
                actual == v["expectedState"] == f["status"] and reason == v["reason"],
                "recomputed evidence/state/reason " + c["id"],
            )
        except (ValueError, TypeError, KeyError) as exc:
            errors.append("ART21 comparison " + c["id"] + ": " + str(exc))
    for path, value in leaves(data):
        if isinstance(value, str):
            loc = "ART21/" + "/".join(path)
            need(len(value) <= 2000, "bounded field " + loc)
            errors += [
                loc + ": " + f.category
                for f in scan_action_text(value, location=loc)
                + scan_host_policy(value, location=loc)
            ]
    return errors
