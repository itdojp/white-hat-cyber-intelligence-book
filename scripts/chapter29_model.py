"""Finite authored Portfolio bindings. No parser, network or operational approval.

The only canonical edition is CAP29-REV-001. Parent checkers retain ownership
of their internal semantics; this consumer binds reviewed source bytes and
explicit documentary observations, not a general evidence inference engine.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat

from scripts.check_editorial_input_manifest import (
    _reject_constant, _reject_duplicate_keys, validate_schema_instance,
    validate_supported_schema_nodes,
)
from scripts.content_safety_policy import scan_action_text, scan_host_policy

VERSION = "1.0.0"
DATA = "cases/fixtures/ch29-capstone-portfolio.json"
SCHEMA = "schemas/ch29-capstone-portfolio.schema.json"
BINDINGS = "tests/fixtures/chapter29/parent-contract.json"
PUBLICATION = "tests/fixtures/chapter29/publication-contract.json"
DOCUMENTS = (
    "manuscript/29-capstone-case-study.md",
    "templates/final-security-decision-portfolio-index.md",
    "cases/ch29-capstone-portfolio-example.md",
    "references/ch29-source-review-2026-10-21.md",
)
SOURCES = ("SRC-CSF-001", "SRC-NIST-RISK-001")
STATUSES = ("Assembling", "Reviewable", "Needs evidence", "Decision ready",
            "Approved", "Superseded")
AREAS = ("Technical accuracy", "Safety / legal / ethical boundary",
         "Source quality / freshness", "Analytic quality / uncertainty",
         "Instructional clarity", "Cross-book boundary / traceability",
         "Reproducibility / deterministic build", "Publication / accessibility")


def require(condition, code):
    if not condition:
        raise ValueError("CAP29-" + code)


def strict(raw):
    return json.loads(raw, object_pairs_hook=_reject_duplicate_keys,
                      parse_constant=_reject_constant)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read_regular(root, name, allowed):
    """Finite input identity and POSIX file checks; not a concurrent OS sandbox."""
    require(name in allowed and not root.is_symlink(), "input-inventory")
    p = root / name
    require(not Path(name).is_absolute() and ".." not in Path(name).parts,
            "relative-input")
    require(all(not q.is_symlink() for q in (p, *p.parents)
                if q.is_relative_to(root)), "symlink-input")
    fd = os.open(p, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW)
    with os.fdopen(fd, "rb") as stream:
        require(stat.S_ISREG(os.fstat(stream.fileno()).st_mode), "regular-input")
        raw = stream.read(1_048_577)
    require(0 < len(raw) <= 1_048_576, "input-size")
    raw.decode("utf-8")
    return raw


def leaves(value, prefix=()):
    if isinstance(value, dict):
        for k, v in value.items():
            yield from leaves(v, (*prefix, k))
    elif isinstance(value, list) and value:
        for i, v in enumerate(value):
            yield from leaves(v, (*prefix, str(i)))
    else:
        yield prefix, value


def case_groups(data):
    for key, value in data.items():
        groups = [(f"{key}-{i+1}", r) for i, r in enumerate(value)] if isinstance(value, list) else [(key, value)]
        for name, group in groups:
            yield name, [("/".join(path) or "value", v if isinstance(v, str)
                          else json.dumps(v, ensure_ascii=False, separators=(",", ":")))
                         for path, v in leaves(group)]


def utc(value):
    require(type(value) is str, "date-type")
    d = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    require(d.strftime("%Y-%m-%dT%H:%M:%SZ") == value, "date-form")
    return d


def unique(rows, key="id"):
    result = {r[key]: r for r in rows}
    require(len(result) == len(rows), "duplicate-id")
    return result


def portfolio_state(*, assembled, reviewed, sufficient, approved, superseded):
    """Six bounded comparison cases; booleans are NOT real approval evidence."""
    require(all(type(v) is bool for v in
                (assembled, reviewed, sufficient, approved, superseded)), "state-type")
    require(not reviewed or assembled, "review-before-assembly")
    require(not approved or (assembled and reviewed and sufficient), "unfounded-approval")
    require(not superseded or approved, "superseded-without-previous-approval")
    if superseded:
        return "Superseded"
    if not assembled:
        return "Assembling"
    if not reviewed:
        return "Reviewable"
    if not sufficient:
        return "Needs evidence"
    return "Approved" if approved else "Decision ready"


def model_errors(data, schema, bindings):
    """Validate one authored edition, with explicit cross-record joins."""
    try:
        validate_supported_schema_nodes(schema, "CAP29", schema)
        validate_schema_instance(data, schema)
        require(data["schemaVersion"] == VERSION and bindings["version"] == VERSION,
                "version")
        require(data["synthetic"] is True and data["readOnly"] is True
                and data["networkRequired"] is False and data["executionAuthorized"] is False,
                "safety-boundary")
        require(all(data[k] == 0 for k in
                    ("actualCollections", "actualActions", "actualModelCalls", "actualDeliveries")),
                "actual-effects")
        record = data["record"]
        require((record["id"], record["artifactId"], record["finalCaseId"], record["version"])
                == ("PORT-CAP29-001", "ART-33", "CASE-2026-001", "CAP29-REV-001"), "identity")
        require(record["meaning"] == "later-authored-reading-not-a-historical-case-update"
                and record["classification"] == "Public synthetic teaching record", "record-scope")
        require(utc(record["sourceCutoff"]) == utc(record["asOf"])
                < utc(record["deadline"]) < utc(record["expiry"]), "time-order")
        require(data["sourceIds"] == list(SOURCES), "source-set")
        arts = unique(data["artifacts"], "artifactId")
        require(list(arts) == [f"ART-{i:02}" for i in range(1, 33)], "artifact-inventory")
        # Literal reviewed bindings preserve per-item status scope, native edition,
        # independent cases, two roles per bundle, and no evidence/authority transfer.
        require(data["artifacts"] == bindings["artifacts"], "parent-binding")
        for row in arts.values():
            require(bindings["parents"].get(row["canonicalPath"]) == row["versionSha256"],
                    "parent-version")
        require(data["documentaryEvidence"] == bindings["documentaryEvidence"],
                "documentary-evidence-binding")
        require(data["stages"] == bindings["stages"], "stage-binding")
        stages = unique(data["stages"])
        require(list(stages) == [f"S29-{i:02}" for i in range(1, 13)], "stage-inventory")
        covered = []
        for i, stage in enumerate(stages.values(), 1):
            require(stage["inputIds"] == (["DR-CAP29-001"] if i == 1 else [f"S29-{i-1:02}"]),
                    "reachability")
            covered.extend(stage["artifactIds"])
            for aid in stage["artifactIds"]:
                require(arts[aid]["stageId"] == stage["id"]
                        and arts[aid]["integrationOwner"] == stage["owner"], "artifact-stage-owner")
        require(sorted(covered) == list(arts), "orphan-or-duplicate-artifact")
        proofs, gaps = unique(data["documentaryEvidence"]), unique(data["gaps"])
        require(list(gaps) == [f"GAP-CAP29-{i:02}" for i in range(1, 5)], "gap-inventory")
        require([g["kind"] for g in gaps.values()] ==
                ["Not collected", "Inconclusive", "Residual risk", "Not collected"], "gap-distinction")
        for g in gaps.values():
            require(all(a in arts for a in g["artifactIds"]), "gap-artifact")
            require(utc(g["dueAt"]) == utc(record["deadline"]), "gap-due")
        for p in proofs.values():
            require(p["kind"] == "authored-document-observation" and not p["systemObservation"]
                    and utc(p["availableAt"]) <= utc(record["sourceCutoff"]), "proof-cutoff")
        req, judgment, decision = data["requirement"], data["judgment"], data["decision"]
        require(req["id"] == "DR-CAP29-001" and req["parentId"] == "DR-2026-001"
                and req["deadline"] == record["deadline"], "requirement")
        require(judgment["id"] == "AJ-CAP29-001" and judgment["inputStepId"] == "S29-12"
                and judgment["evidenceIds"] == list(proofs) and judgment["gapIds"] == list(gaps),
                "judgment-join")
        require(judgment["confirmedFacts"] == [p["claim"] for p in proofs.values()], "fact-evidence")
        require(judgment["confidence"] == "高", "bounded-confidence")
        options = unique(data["options"])
        require(list(options) == ["OPT-CAP29-HOLD", "OPT-CAP29-RESUME", "OPT-CAP29-CLOSE"],
                "option-inventory")
        require([o["requiredClosedGaps"] for o in options.values()] ==
                [[], list(gaps)[:2], list(gaps)], "option-conditions")
        require(decision["id"] == "DEC-CAP29-001" and decision["requirementId"] == req["id"]
                and decision["judgmentId"] == judgment["id"]
                and decision["owner"] == req["decisionOwner"]
                and decision["gapIds"] == list(gaps), "decision-join")
        require(decision["approval"] is None and decision["supersededBy"] is None
                and decision["realAuthorization"] is False and decision["receiptId"] is None
                and decision["deliveryStatus"] == "prepared-not-delivered", "approval-receipt-boundary")
        require([r["area"] for r in data["reviews"]] == list(AREAS), "review-inventory")
        unique(data["reviews"])
        for r in data["reviews"]:
            require(r["reviewerRole"].startswith("SYNTH-") and r["date"] == record["asOf"]
                    and r["evidenceIds"] == list(proofs)
                    and r["result"] == "Pass-with-limits", "synthetic-review")
        selected = options[decision["recommendedOption"]]
        state = portfolio_state(assembled=True, reviewed=True,
                                sufficient=not selected["requiredClosedGaps"],
                                approved=False, superseded=False)
        require(state == record["status"] == "Decision ready", "option-status")
        require([b["id"] for b in data["briefs"]] == ["BRIEF-CAP29-TECH", "BRIEF-CAP29-EXEC"],
                "brief-inventory")
        for brief in data["briefs"]:
            require(brief["judgmentId"] == judgment["id"] and brief["evidenceIds"] == list(proofs)
                    and brief["gapIds"] == list(gaps)
                    and brief["deliveryStatus"] == "prepared-not-delivered", "brief-parity")
        actions = unique(data["actions"])
        require(list(actions) == [f"ACT-CAP29-{i:02}" for i in range(1, 5)], "action-inventory")
        for a, g in zip(actions.values(), gaps.values(), strict=True):
            require(a["decisionId"] == decision["id"] and a["gapId"] == g["id"]
                    and a["owner"] == g["owner"] and a["dueAt"] == g["dueAt"]
                    and a["instruction"] == g["nextCheck"]
                    and a["result"] == "Planned" and a["executed"] is False, "action-join")
        reassess = data["reassessment"]
        require(reassess["id"] == "REA-CAP29-001" and reassess["decisionId"] == decision["id"]
                and reassess["actionIds"] == list(actions)
                and reassess["scheduledAt"] == record["deadline"]
                and reassess["expiry"] == record["expiry"], "reassessment-join")
        require(reassess["triggers"] == ["parent-version-change", "case-or-scope-change",
                "source-correction", "new-evidence-or-authority", "receipt-or-review-change", "expiry"],
                "reassessment-triggers")
        for path, value in leaves(data):
            if isinstance(value, str):
                where = "CAP29:" + "/".join(path)
                document_pointer = (
                    (len(path) == 3 and path[0] == "artifacts"
                     and path[2] in ("canonicalPath", "templatePath"))
                    or (len(path) == 3 and path[0] == "documentaryEvidence" and path[2] == "path")
                )
                require(not document_pointer or value in bindings["parents"], "fixed-document-pointer")
                findings = scan_action_text(value, location=where)
                if not document_pointer:
                    findings += scan_host_policy(value, location=where)
                require(not findings, "safety: " + str([(f.category, f.location) for f in findings]))
        return []
    except (ValueError, KeyError, TypeError, IndexError) as exc:
        return [str(exc)]
