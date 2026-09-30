"""Finite authored Claim/Source/review bindings; never evaluates model text or tools."""

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import PurePosixPath
import stat

from scripts.check_editorial_input_manifest import (
    _reject_constant,
    _reject_duplicate_keys,
    validate_schema_instance,
    validate_supported_schema_nodes,
)
from scripts.content_safety_policy import scan_action_text, scan_host_policy

VERSION = "1.0.0"
DATA = "cases/fixtures/ch28-ai-assisted-analysis-assurance.json"
SCHEMA = "schemas/ch28-ai-assisted-analysis-assurance.schema.json"
CONTRACT = "tests/fixtures/chapter28/publication-contract.json"
CORPUS = "tests/fixtures/chapter28/comparison-corpus.json"
DOCUMENTS = (
    "manuscript/28-ai-assisted-analysis-assurance.md",
    "templates/ai-assisted-analysis-assurance-record.md",
    "cases/ch28-ai-assisted-analysis-assurance-example.md",
    "references/ch28-source-review-2026-09-30.md",
)
SOURCES = ("SRC-AIRMF-001", "SRC-AML-001", "SRC-OWASP-LLM-001", "SRC-OWASP-AGENT-001")
STATUSES = (
    "Unverified",
    "Supported",
    "Partially supported",
    "Contradicted",
    "Rejected",
)
PARENT25 = "cases/fixtures/ch25-structured-analysis-attribution-dataset.json"
PARENT26 = "cases/fixtures/ch26-cti-distribution.json"
PARENTS = (
    "WRITING_GUIDE.md",
    "SOURCE_POLICY.md",
    "SAFETY_SCOPE.md",
    "CROSS_BOOK_MAP.md",
    PARENT25,
    PARENT26,
    "cases/fixtures/ch24-source-evaluation.json",
    "cases/fixtures/ch27-ai-agent-threat-model.json",
    "scripts/content_safety_policy.py",
    "CONTENT_SAFETY_POLICY.md",
    "scripts/publication_projection.py",
    "scripts/_publication_projection_renderer.rb",
    "scripts/publication_text.py",
    "scripts/sync_site_source.py",
    "scripts/sync_book_site.py",
    "Gemfile.lock",
    "package-lock.json",
    ".book-formatter/revision.json",
)
INDEX_PATHS = (
    "artifact-index.md",
    "figure-index.md",
    "glossary.md",
    "cases/index.md",
    "cases/fixtures/index.md",
    "README.md",
    "CHANGELOG.md",
    "CANONICAL_SOURCE.md",
)
INPUTS = (
    DATA,
    SCHEMA,
    CONTRACT,
    CORPUS,
    *DOCUMENTS,
    *PARENTS,
    *INDEX_PATHS,
    "package.json",
    "site-pages.json",
    "references/sources.json",
    "book-config.json",
)


def require(condition, code):
    if not condition:
        raise ValueError("AI28 " + code)


def strict(raw):
    return json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=_reject_duplicate_keys,
        parse_constant=_reject_constant,
    )


def digest(value):
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode()
    ).hexdigest()


def text_digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def read_regular(root, relative):
    """Finite POSIX descriptor reader; not a concurrent ancestor-rename sandbox."""
    require(relative in INPUTS and not root.is_symlink(), "fixed input/root")
    root = root.resolve(strict=True)
    path = root
    for part in PurePosixPath(relative).parts:
        path /= part
        require(not path.is_symlink(), "symlink input/ancestor")
    require(path.resolve(strict=True).is_relative_to(root), "input containment")
    require(hasattr(os, "O_NOFOLLOW") and hasattr(os, "O_NONBLOCK"), "POSIX flags")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        require(
            stat.S_ISREG(info.st_mode) and 0 < info.st_size <= 1024 * 1024,
            "bounded regular file",
        )
        raw = stream.read(1024 * 1024 + 1)
    require(len(raw) <= 1024 * 1024, "input size")
    raw.decode("utf-8")
    return raw


def instant(value):
    require(type(value) is str, "UTC string")
    result = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    require(result.strftime("%Y-%m-%dT%H:%M:%SZ") == value, "canonical UTC")
    return result


def index(rows):
    require(
        type(rows) is list
        and all(type(r) is dict and type(r.get("id")) is str for r in rows),
        "ID rows",
    )
    ids = [r["id"] for r in rows]
    require(len(ids) == len(set(ids)), "unique IDs")
    return dict(zip(ids, rows, strict=True))


def leaves(value, path=()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from leaves(child, (*path, key))
    elif isinstance(value, list) and value:
        for i, child in enumerate(value):
            yield from leaves(child, (*path, str(i)))
    else:
        yield path, value


def case_groups(data):
    for key, value in data.items():
        groups = (
            [(r["id"], r) for r in value] if isinstance(value, list) else [(key, value)]
        )
        for title, group in groups:
            yield (
                title,
                [
                    (
                        "/".join(p) or "value",
                        v
                        if isinstance(v, str)
                        else json.dumps(v, ensure_ascii=False, separators=(",", ":")),
                    )
                    for p, v in leaves(group)
                ],
            )


def resolve(value, path):
    for key in path:
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def binding(data, claim):
    """All verification/review targets refer to the same finite offline conditions."""
    return {
        "claimId": claim["id"],
        "claimHash": text_digest(claim["text"]),
        "sourceSetId": data["sourceSet"]["id"],
        "sourceSetVersion": data["sourceSet"]["version"],
        "sourceSetHash": data["sourceSet"]["sha256"],
        "modelId": data["model"]["id"],
        "modelVersion": data["model"]["version"],
        "runtime": data["model"]["runtime"],
        "instructionId": data["instruction"]["id"],
        "instructionHash": data["instruction"]["sha256"],
        "inputId": data["input"]["id"],
        "inputHash": data["input"]["sha256"],
        "outputId": data["output"]["id"],
        "outputVersion": data["output"]["version"],
        "outputHash": data["output"]["sha256"],
    }


def claim_status(data, claim):
    """Compare authored passage pointers, not arbitrary natural-language semantics."""
    source, passages = index(data["approvedSources"]), index(data["passages"])
    v = index(data["verifications"])[claim["verificationId"]]
    require(v["target"] == binding(data, claim), "verification target/version/hash")
    require(claim["textHash"] == text_digest(claim["text"]), "claim text hash")
    require(
        claim["text"] == "; ".join(p["statement"] for p in claim["parts"]),
        "original Claim part coverage",
    )
    require(
        len(claim["citations"]) == len(set(claim["citations"])), "duplicate citation"
    )
    groups = list(
        dict.fromkeys(
            source[s]["independenceGroupId"] for s in claim["citations"] if s in source
        )
    )
    require(
        v["originGroups"] == groups and v["independentOriginCount"] == len(groups),
        "independent origins not report count",
    )
    require(
        v["crossCheck"] == "parent-structured-record-and-lineage"
        and v["independentObservationAdded"] is False,
        "cross-check scope",
    )
    if (
        not claim["citations"]
        or any(s not in source for s in claim["citations"])
        or claim["contaminated"]
        or claim["proposedAttribution"] not in ("L0", "L1", "L2")
    ):
        return "Rejected", ["ineligible-provenance-or-boundary"]
    require(
        all(
            instant(source[s]["collectedAt"]) <= instant(data["record"]["cutoff"])
            for s in claim["citations"]
        ),
        "source cutoff",
    )
    require(
        claim["grounding"] in ("Direct", "Composite", "Inference"), "grounding mode"
    )
    require(
        (claim["grounding"] == "Composite") == (len(claim["parts"]) > 1),
        "composite part coverage",
    )
    outcomes, covered = [], []
    for part in claim["parts"]:
        require(
            part["outcome"] in ("supported", "unknown", "contradicted"), "part outcome"
        )
        if part["passageId"] is None:
            require(
                part["outcome"] == "unknown"
                and part["sourceIds"] == []
                and part["sourceText"] == "not-found",
                "ungrounded part",
            )
        else:
            p = passages.get(part["passageId"])
            require(
                p is not None
                and part["sourceIds"] == p["sourceIds"]
                and part["statement"] == p["comparedStatement"]
                and part["sourceText"] == p["text"]
                and part["outcome"] == p["outcome"],
                "passage existence/content/support",
            )
            covered.extend(p["sourceIds"])
        outcomes.append(part["outcome"])
    require(
        list(dict.fromkeys(covered)) == claim["citations"], "claim Source preservation"
    )
    if not v["complete"]:
        return "Unverified", ["verification-incomplete"]
    if "contradicted" in outcomes:
        return "Contradicted", ["authored-counterevidence"]
    if outcomes and all(o == "supported" for o in outcomes):
        return "Supported", ["bounded-passages-supported"]
    if "supported" in outcomes:
        return "Partially supported", ["supported-and-unknown-parts"]
    return "Unverified", ["no-complete-support"]


def validate_model(data, schema, contract, parent25, parent26):
    errors = []
    try:
        validate_supported_schema_nodes(schema, "schema", schema)
        validate_schema_instance(data, schema)
        require(
            [[list(p), v] for p, v in leaves(data)] == contract["authoredLeaves"],
            "authored all-leaf inventory",
        )
        for path, value in leaves(data):
            if isinstance(value, str):
                # Four fixed relative parent-document pointers, not URL/host grants.
                # Action scanning still applies. No pattern or new pointer is exempt.
                local_pointer = (
                    path
                    in (
                        ("passages", "0", "parentDocument"),
                        ("passages", "1", "parentDocument"),
                        ("passages", "2", "parentDocument"),
                        ("passages", "3", "parentDocument"),
                    )
                    and value == PARENT25
                )
                errors += [
                    "AI28 " + f.category + ": " + "/".join(path)
                    for f in (
                        *scan_action_text(value, location="/".join(path)),
                        *(
                            scan_host_policy(value, location="/".join(path))
                            if not local_pointer
                            else []
                        ),
                    )
                ]
        r, task = data["record"], data["task"]
        require(
            (r["caseId"], r["parentCaseId"], r["relation"], r["attributionCeiling"])
            == (parent25["caseId"], parent26["record"]["caseId"], "refines", "L2"),
            "parent Case/non-inheritance",
        )
        require(
            (r["artifactId"], r["parentArtifactId"], r["parentDistributionId"])
            == ("ART-32", "ART-12", parent26["record"]["id"]),
            "Artifact/distribution binding",
        )
        for key in ("asOf", "cutoff", "attributionCeiling"):
            require(r[key] == parent26["record"][key], "parent time/ceiling")
        require(
            (
                task["requirementId"],
                task["intelligenceRequirementId"],
                task["judgmentId"],
                task["decisionId"],
            )
            == tuple(
                parent25[k]
                for k in (
                    "decisionRequirementId",
                    "intelligenceRequirementId",
                    "analyticJudgmentId",
                    "decisionId",
                )
            ),
            "task parent IDs",
        )
        require(
            instant(r["cutoff"])
            <= instant(data["output"]["at"])
            <= instant(r["asOf"])
            < instant(r["reviewDeadline"]),
            "record timeline",
        )
        source, evidence = index(parent25["sourceNotes"]), index(parent25["evidence"])
        approved = index(data["approvedSources"])
        require(list(approved) == list(source), "approved parent Source inventory")
        for s in approved.values():
            p = source[s["id"]]
            collected = datetime.fromisoformat(p["collectedAt"]).astimezone(
                timezone.utc
            )
            require(
                (
                    s["origin"],
                    s["independenceGroupId"],
                    s["reference"],
                    instant(s["collectedAt"]),
                )
                == (p["origin"], p["independenceGroupId"], p["reference"], collected),
                "parent Source identity",
            )
            require(
                instant(s["collectedAt"])
                <= instant(r["cutoff"])
                <= instant(r["asOf"])
                < instant(s["validUntil"]),
                "approved Source cutoff/validity",
            )
            require(
                all(
                    e in evidence and evidence[e]["sourceNoteId"] == s["id"]
                    for e in s["evidenceIds"]
                ),
                "Source Evidence binding",
            )
            require(
                len(s["evidenceIds"]) == 1
                and s["educationalEvidenceHash"]
                == evidence[s["evidenceIds"][0]]["hash"],
                "parent Evidence descriptor",
            )
            parent_e = next(e for e in parent26["evidence"] if e["sourceId"] == s["id"])
            require(
                s["limitation"] == parent_e["limitation"]
                and s["newObservation"] is False,
                "parent limitation/no new observation",
            )
        require(
            data["sourceSet"]["sourceIds"] == list(approved)
            and data["sourceSet"]["sha256"] == digest(data["approvedSources"]),
            "Source Set hash/order",
        )
        for p in data["passages"]:
            require(
                p["parentDocument"] == PARENT25 and bool(p["parentPaths"]),
                "passage parent",
            )
            parent_values = [resolve(parent25, path) for path in p["parentPaths"]]
            require(
                p["parentValuesHash"] == digest(parent_values), "parent passage hash"
            )
            require(
                p["text"] == contract["passageIdentity"][p["id"]]["text"]
                and p["comparedStatement"]
                == contract["passageIdentity"][p["id"]]["comparedStatement"]
                and p["outcome"] == contract["passageIdentity"][p["id"]]["outcome"]
                and p["parentPaths"]
                == contract["passageIdentity"][p["id"]]["parentPaths"]
                and p["sourceIds"] == contract["passageIdentity"][p["id"]]["sourceIds"],
                "finite authored passage meaning",
            )
        for obj in (data["instruction"], data["input"]):
            require(obj["sha256"] == text_digest(obj["text"]), "Instruction/Input hash")
        require(
            data["input"]["sourceIds"] == list(approved)
            and data["input"]["sourceSetId"] == data["sourceSet"]["id"],
            "input approved Source binding",
        )
        claims, verifications, decisions, audit = (
            index(data[k])
            for k in ("claims", "verifications", "humanDecisions", "audit")
        )
        require(
            data["output"]["claimIds"] == list(claims)
            and data["output"]["text"] == " / ".join(c["text"] for c in claims.values())
            and data["output"]["sha256"] == text_digest(data["output"]["text"]),
            "output Claim/hash/order",
        )
        require(
            len(verifications) == len(decisions) == len(audit) == len(claims),
            "one-to-one review inventory",
        )
        require(
            len({c["verificationId"] for c in claims.values()}) == len(claims)
            and len({c["decisionId"] for c in claims.values()}) == len(claims),
            "unique Claim review links",
        )
        for c in claims.values():
            status, reasons = claim_status(data, c)
            require(
                c["status"] == status
                and verifications[c["verificationId"]]["reasons"] == reasons,
                "Claim status/reason",
            )
            v, h = verifications[c["verificationId"]], decisions[c["decisionId"]]
            require(
                instant(data["output"]["at"])
                <= instant(v["at"])
                <= instant(h["reviewedAt"])
                <= instant(r["asOf"])
                < instant(h["validUntil"]),
                "verification/human review timeline",
            )
            require(
                h["target"] == binding(data, c)
                and h["verificationId"] == v["id"]
                and h["reviewerId"] == "SYNTH-AI28-REVIEWER"
                and h["judgmentId"] == task["judgmentId"],
                "human Claim/Verification binding",
            )
            disposition = {
                "Supported": "Accept",
                "Partially supported": "Revise",
                "Contradicted": "Reject",
                "Rejected": "Reject",
                "Unverified": "Escalate",
            }[status]
            expected_text = " / ".join(
                p["statement"] for p in c["parts"] if p["outcome"] == "supported"
            )
            require(
                h["disposition"] == disposition
                and h["acceptedWording"]
                == (
                    expected_text
                    if status in ("Supported", "Partially supported")
                    else "not-adopted"
                ),
                "partial-only limited adoption",
            )
            require(
                h["analyticConfidence"] in ("中", "低", "未判定")
                and h["confidenceSource"] == "human-evidence-alternatives-gaps"
                and h["modelConfidenceCopied"] is False
                and h["attributionCeiling"] == "L2",
                "human confidence/attribution boundary",
            )
            require(
                h["alternativeIds"]
                == [a["id"] for a in parent25["alternativeHypotheses"]]
                and h["gapIds"] == [g["id"] for g in parent25["collectionGaps"]],
                "alternatives/gaps preserved",
            )
            a = audit[h["auditId"]]
            require(
                a["decisionId"] == h["id"]
                and a["target"] == binding(data, c)
                and a["at"] == h["reviewedAt"]
                and a["disposition"] == disposition
                and a["ownerId"] == "SYNTH-AI28-OWNER"
                and instant(a["at"]) < instant(a["retainUntil"]),
                "audit binding/retention",
            )
            require(
                h["reassessmentId"] == data["reassessment"]["id"],
                "human reassessment binding",
            )
        samples = index(data["contaminationSamples"])
        require(
            list(samples) == ["AI28-CONT-SOURCE", "AI28-CONT-TOOL", "AI28-CONT-MEMORY"],
            "three fixed contamination samples",
        )
        require(
            data["input"]["contaminationSampleIds"] == list(samples),
            "input contamination inventory",
        )
        for s in samples.values():
            require(
                s["sha256"] == text_digest(s["text"])
                and s["adopted"] is False
                and s["authorityGranted"] is False
                and s["executed"] is False
                and s["conclusion"] == "untrusted-authority-self-claim"
                and s["method"] == "author-labelled-fixed-sample-not-detector",
                "contamination non-promotion",
            )
        rep = data["reproduction"]
        require(
            rep["targets"] == [binding(data, c) for c in claims.values()]
            and rep["method"] == "offline-record-equality"
            and rep["modelExecuted"] is False
            and rep["generalizationProven"] is False,
            "reproduction target/limits",
        )
        re = data["reassessment"]
        require(
            re["claimIds"] == list(claims)
            and re["decisionIds"] == list(decisions)
            and re["auditIds"] == list(audit)
            and re["ownerId"] == "SYNTH-AI28-OWNER"
            and instant(r["asOf"])
            < instant(re["dueAt"])
            <= instant(r["reviewDeadline"])
            and re["triggers"]
            == [
                "source-correction",
                "source-withdrawal",
                "source-expiry",
                "version-change",
                "input-contamination",
                "cutoff-change",
                "coverage-change",
                "independence-change",
                "attribution-threshold-change",
            ],
            "reassessment reachability/owner/triggers",
        )
        require(
            data["methodReferences"] == contract["methodReferences"],
            "method-only/non-inheritance",
        )
        require(
            data["handoff"]["acceptedDecisionIds"]
            == [
                h["id"]
                for h in decisions.values()
                if h["disposition"] in ("Accept", "Revise")
            ]
            and data["handoff"]["unadoptedDecisionIds"]
            == [
                h["id"]
                for h in decisions.values()
                if h["disposition"] in ("Reject", "Escalate")
            ]
            and data["handoff"]["receipt"] == "not-received"
            and data["handoff"]["executionAuthorized"] is False,
            "handoff selective/not received",
        )
    except (ValueError, KeyError, TypeError, StopIteration) as exc:
        errors.append("AI28 fail closed: " + str(exc))
    return errors
