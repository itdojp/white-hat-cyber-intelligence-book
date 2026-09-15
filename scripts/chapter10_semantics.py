"""ART-19's finite synthetic evidence graph, not an acquisition/permission engine.

All source content is supplied and pinned. No real source lookup, Markdown/URL
parser, identity verification, generic PII recognizer or legal determination.
"""

from __future__ import annotations

from datetime import datetime
import hashlib
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
DATA_PATH = "cases/fixtures/ch10-attack-surface.json"
BUNDLE_PATH = "cases/fixtures/ch10-source-bundle.json"
SCHEMA_PATH = "schemas/ch10-attack-surface.schema.json"
CONTRACT_PATH = "tests/fixtures/chapter10/publication-contract.json"
DOCUMENTS = (
    "manuscript/10-recon-osint-boundary.md",
    "templates/attack-surface-register.md",
    "cases/ch10-attack-surface-example.md",
    "references/ch10-source-review-2026-09-14.md",
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
)
INPUTS = (DATA_PATH, BUNDLE_PATH, SCHEMA_PATH, CONTRACT_PATH, *DOCUMENTS, *PARENTS)
CLASSES = ("Passive", "Active", "Authenticated")
STATES = ("Candidate", "Corroborated", "Owner confirmed", "Rejected", "Unknown")
ACTIONS = ("read-supplied-json", "compare-synthetic-fields", "write-bounded-summary")
APPROVALS = (
    "new-current-authorization",
    "exact-asset-operation-time-scope",
    "system-and-data-owner-review",
    "third-party-terms-review",
)


def ident(prefix, number):
    return f"{prefix}-ASR10-{number:03}"


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
        raise ValueError("ART19 fixed input inventory/root")
    if any(type(getattr(os, f, None)) is not int for f in ("O_NOFOLLOW", "O_NONBLOCK")):
        raise ValueError("ART19 requires Linux/WSL2 no-follow/nonblocking primitives")
    root = root.resolve(strict=True)
    current = root
    for part in PurePosixPath(relative).parts:
        current /= part
        if current.is_symlink():
            raise ValueError("ART19 symlink input/ancestor")
    if not current.resolve(strict=True).is_relative_to(root):
        raise ValueError("ART19 input containment")
    fd = os.open(current, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= 1024 * 1024:
            raise ValueError("ART19 bounded regular input required")
        raw = stream.read(1024 * 1024 + 1)
    if len(raw) > 1024 * 1024:
        raise ValueError("ART19 input size")
    return raw


def utc(value):
    parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    if parsed.strftime("%Y-%m-%dT%H:%M:%SZ") != value:
        raise ValueError("ART19 canonical UTC time")
    return parsed


def leaves(value, path=()):
    """Structured JSON paths, not reader projection or renderer syntax."""
    if isinstance(value, dict):
        for k, v in value.items():
            yield from leaves(v, path + (k,))
    elif isinstance(value, list) and value:
        for i, v in enumerate(value, 1):
            yield from leaves(v, path + (str(i),))
    else:
        yield path, value


def case_groups(data, bundle):
    for label, document in (("register", data), ("bundle", bundle)):
        for group, value in document.items():
            rows = [
                (
                    " / ".join(path) or group,
                    v if isinstance(v, str) else json.dumps(v, ensure_ascii=False),
                )
                for path, v in leaves(value)
            ]
            yield label + "/" + group, rows


def validate_model(data, bundle, schema, contract):
    errors = []
    try:
        validate_supported_schema_nodes(schema, "ART19 schema", schema)
        validate_schema_instance({"register": data, "bundle": bundle}, schema)
    except (ManifestError, ValueError, KeyError, TypeError) as exc:
        return ["ART19 schema: " + str(exc)]

    def need(ok, code):
        if not ok:
            errors.append("ART19 " + code)

    need(
        data["schemaVersion"]
        == data["modelVersion"]
        == bundle["schemaVersion"]
        == MODEL_VERSION,
        "model version",
    )
    need(
        data["synthetic"] is True
        and bundle["synthetic"] is True
        and data["executionAuthorized"] is False
        and bundle["acquisitionOccurred"] is False,
        "synthetic non-execution",
    )
    need(bundle["bundleId"] == "BUNDLE-ASR10-001", "bundle identity")
    need(
        data["parents"] == contract["parentSnapshot"],
        "parent IDs/time/scope/state unchanged",
    )
    r, plan = data["record"], data["learnerPlan"]
    for k, v in {
        "artifactId": "ART-19",
        "registerId": "ASR-2026-010",
        "version": 1,
        "asOf": "2026-09-14T01:00:00Z",
        "status": "analysis-complete-with-gaps",
        "collectionRequirementId": "CR-ASR10-001",
        "owner": "SYNTH-DECISION-OWNER",
        "decisionId": "DEC-ASR10-001",
        "decision": "record-only; Do not proceed with operational actions",
        "decisionUseful": "not-assessed-for-historical-deadline",
    }.items():
        need(r[k] == v, "record " + k)
    need(
        plan["collectionClass"] == "Passive"
        and plan["actions"] == list(ACTIONS)
        and plan["networkRequests"]
        == plan["authenticationAttempts"]
        == plan["rateTests"]
        == 0,
        "offline learner class/action boundary",
    )
    need(
        plan["inputSourceIds"] == [ident("OSRC", i) for i in range(1, 10)],
        "learner supplied input coverage",
    )
    need(
        plan["maximumSources"] == 9
        and plan["maximumCandidates"] == 6
        and 0 < plan["summaryBytes"] <= 65536
        and 0 < plan["minutes"] <= 30,
        "finite budgets",
    )
    for k, v in {
        "onUnexpectedData": "stop-without-copying-and-record-gap",
        "cleanup": "remove-only-owned-working-copies; retain-canonical-sources",
        "cleanupStatus": "not-executed",
        "retentionStarts": "hypothetical-session-end",
        "cleanupOwner": "SYNTH-EVIDENCE-CUSTODIAN",
    }.items():
        need(plan[k] == v, "data/cleanup " + k)
    need(0 < plan["retentionHours"] <= 24, "bounded retention")
    source_ids = [ident("OSRC", i) for i in range(1, 10)]
    candidate_ids = [ident("CAND", i) for i in range(1, 7)]
    need(
        [x["sourceId"] for x in data["sources"]] == source_ids
        and [x["sourceId"] for x in bundle["sources"]] == source_ids,
        "finite source IDs/order/uniqueness",
    )
    need(
        [x["candidateId"] for x in data["candidates"]] == candidate_ids,
        "finite candidate IDs/order/uniqueness",
    )
    # Do not build lookup dictionaries until duplicates, omissions and dangling
    # inventory entries have failed closed.
    if errors:
        return errors
    sources = {x["sourceId"]: x for x in data["sources"]}
    contents = {x["sourceId"]: x["content"] for x in bundle["sources"]}
    try:
        for i, (sid, source) in enumerate(sources.items(), 1):
            need(source["provenanceId"] == ident("PROV", i), "direct provenance " + sid)
            need(
                all(source[k] == v for k, v in contract["sourceRoles"][sid].items()),
                "source role/lineage/interaction " + sid,
            )
            digest = hashlib.sha256(contents[sid].encode("utf-8")).hexdigest()
            need(
                digest
                == source["contentSha256"]
                == contract["sourceContentDigests"][sid],
                "pinned supplied content/hash " + sid,
            )
            need(
                source["hashScope"]
                == "UTF-8 bytes of matching bundle content string; no normalization",
                "hash scope " + sid,
            )
            need(
                source["timestampBasis"]
                == "authored-synthetic-assumption-not-clock-measurement"
                and source["transformation"] == "authored-summary; no real acquisition",
                "authored provenance " + sid,
            )
            need(
                source["termsNote"]
                == "supplied synthetic teaching copy only; not external-source permission"
                and source["dataClass"] == "synthetic-only"
                and source["credentialMaterial"] == "none"
                and source["personalDataFields"] == []
                and source["custodian"] == "SYNTH-EVIDENCE-CUSTODIAN",
                "terms/data/custody " + sid,
            )
            need(
                utc(source["observedAt"])
                <= utc(source["acquiredAt"])
                <= utc(r["asOf"]),
                "source time ordering " + sid,
            )
        for i, c in enumerate(data["candidates"], 1):
            cid, refs = c["candidateId"], c["sourceIds"]
            expected = [sid for sid, s in sources.items() if s["candidateId"] == cid]
            need(refs == expected, "candidate source ownership/order " + cid)
            if refs != expected:
                continue
            need(
                all(c[k] == v for k, v in contract["candidateIdentity"][cid].items()),
                "candidate identity/dependency/third-party source binding " + cid,
            )
            origins = {sources[sid]["originalOriginId"] for sid in refs}
            if c["verificationStatus"] == "Corroborated":
                need(len(origins) >= 2, "independent origins for corroboration " + cid)
            confirmed = c["verificationStatus"] == "Owner confirmed"
            need(
                confirmed == (c["ownershipStatus"] == "Confirmed owned"),
                "verification/ownership not conflated " + cid,
            )
            if confirmed:
                need(
                    i == 1
                    and c["ownershipConfidence"] == "High"
                    and c["candidateOwner"] == "SYNTH-BUSINESS-SYSTEMS"
                    and c["ownerEvidenceSourceIds"]
                    == [ident("OSRC", 1), ident("OSRC", 8)]
                    and c["parentAssetId"] == "ASSET-2026-001",
                    "bounded owner confirmation evidence " + cid,
                )
            else:
                need(
                    c["ownerEvidenceSourceIds"] == [] and c["parentAssetId"] is None,
                    "unconfirmed asset not parent membership " + cid,
                )
                need(
                    c["candidateOwner"] == ("SYNTH-OTHER-ORG" if i == 4 else "Unknown"),
                    "candidate owner uncertainty " + cid,
                )
            if i == 2:
                need(
                    c["verificationStatus"] in ("Candidate", "Unknown")
                    and c["ownershipStatus"] == "Unverified"
                    and c["ownershipConfidence"] == "Low",
                    "CT intent and mirror not ownership/current service",
                )
            if i == 3:
                need(
                    c["verificationStatus"] == "Unknown"
                    and c["ownershipStatus"] == "Historical"
                    and c["ownershipConfidence"] == "Low",
                    "historical DNS not current evidence",
                )
            if i == 4:
                need(
                    c["verificationStatus"] == "Rejected"
                    and c["ownershipStatus"] == "Third party"
                    and c["thirdPartyStatus"] == "confirmed-third-party",
                    "same-name third party excluded",
                )
            if i in (5, 6):
                need(
                    c["ownershipStatus"] == "Unverified"
                    and c["verificationStatus"] != "Owner confirmed",
                    "SaaS/package ownership remains unverified " + cid,
                )
                expected_confidence = (
                    "Medium" if c["verificationStatus"] == "Corroborated" else "Low"
                )
                need(
                    c["ownershipConfidence"] == expected_confidence,
                    "confidence bounded by supplied support " + cid,
                )
            need(
                c["exposure"] == "not-measured"
                and c["evidenceBasis"] == "authored-source-comparison-not-observation",
                "source statements not real measurements " + cid,
            )
            need(
                c["nextAction"] == "record-only"
                and c["nextActionAuthorization"] is False
                and c["requiredApproval"] == list(APPROVALS)
                and c["stopReason"]
                == "parent authority expired; no operational scope for new candidate",
                "next action cannot inherit ownership/parent permission " + cid,
            )
            for field, prefix in (
                ("evidenceId", "EVD"),
                ("gapId", "GAP"),
                ("reassessmentId", "REA"),
            ):
                need(c[field] == ident(prefix, i), "direct " + field + " " + cid)
            need(
                c["gapOwner"] == "SYNTH-ASSET-REVIEW-OWNER"
                and utc(c["dueAt"]) > utc(r["asOf"]),
                "gap accountability/time " + cid,
            )
    except (ValueError, TypeError, KeyError) as exc:
        errors.append("ART19 evidence graph/time: " + str(exc))
    need(data["handoffs"] == contract["handoffs"], "bounded nonoperational handoffs")
    confirmed_ids = [
        c["candidateId"]
        for c in data["candidates"]
        if c["verificationStatus"] == "Owner confirmed"
    ]
    need(
        bool(data["handoffs"]) and data["handoffs"][0]["candidateIds"] == confirmed_ids,
        "only owner-confirmed candidates in Chapters12-13 handoff",
    )
    need(data["limits"] == contract["limits"], "coverage/nonmeasurement limits")
    for label, doc in (("register", data), ("bundle", bundle)):
        for path, value in leaves(doc):
            if isinstance(value, str):
                location = "ART19/" + label + "/" + "/".join(path)
                need(len(value) <= 2000, "bounded string " + location)
                errors += [
                    location + ": " + f.category
                    for f in scan_action_text(value, location=location)
                    + scan_host_policy(value, location=location)
                ]
    return errors
