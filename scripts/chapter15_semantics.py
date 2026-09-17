"""Chapter15 Layer A: finite authored Findings, Retests and acceptance decisions.

Not a workflow engine, renderer, live scanner, legal approval or actual remediation.
"""

from __future__ import annotations
from copy import deepcopy
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
DATA_PATH = "cases/fixtures/ch15-findings-retest-risk.json"
SCHEMA_PATH = "schemas/ch15-findings-retest-risk.schema.json"
CONTRACT_PATH = "tests/fixtures/chapter15/publication-contract.json"
DOCUMENTS = (
    "manuscript/15-findings-retest-risk.md",
    "templates/finding-report.md",
    "cases/ch15-findings-retest-risk-example.md",
    "references/ch15-source-review-2026-09-17.md",
    "templates/retest-record.md",
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
    "manuscript/13-platform-supply-chain.md",
    "templates/platform-supply-chain-assessment.md",
    "cases/ch13-platform-supply-chain-example.md",
    "references/ch13-source-review-2026-09-15.md",
    "cases/fixtures/ch13-supply-chain.json",
    "schemas/ch13-supply-chain.schema.json",
    "manuscript/07-vulnerability-prioritization.md",
    "cases/fixtures/ch07-vulnerability-prioritization.json",
    "manuscript/14-minimal-impact-validation.md",
    "templates/minimal-impact-validation-record.md",
    "cases/ch14-minimal-impact-validation-example.md",
    "references/ch14-source-review-2026-09-16.md",
    "cases/fixtures/ch14-minimal-impact-validation.json",
    "schemas/ch14-minimal-impact-validation.schema.json",
)
INPUTS = (DATA_PATH, SCHEMA_PATH, CONTRACT_PATH, *DOCUMENTS, *PARENTS)
STATUSES = ("Open", "Mitigated", "Accepted", "Retest required", "Closed", "Reopened")
RESULTS = ("Passed", "Partial", "Failed", "Inconclusive", "Stopped")


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
        raise ValueError("ART04/23 fixed input inventory/root")
    if any(type(getattr(os, f, None)) is not int for f in ("O_NOFOLLOW", "O_NONBLOCK")):
        raise ValueError(
            "ART04/23 requires Linux/WSL2 no-follow/nonblocking primitives"
        )
    root = root.resolve(strict=True)
    current = root
    for part in PurePosixPath(relative).parts:
        current /= part
        if current.is_symlink():
            raise ValueError("ART04/23 symlink input/ancestor")
    if not current.resolve(strict=True).is_relative_to(root):
        raise ValueError("ART04/23 input containment")
    fd = os.open(current, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= 1024 * 1024:
            raise ValueError("ART04/23 bounded regular input required")
        raw = stream.read(1024 * 1024 + 1)
    if len(raw) > 1024 * 1024:
        raise ValueError("ART04/23 input size")
    return raw


def utc(value):
    parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    if parsed.strftime("%Y-%m-%dT%H:%M:%SZ") != value:
        raise ValueError("ART04/23 canonical UTC time")
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


def retest_result(record):
    """Compare two ordered supplied criteria; never execute the stated Method.

    Stop precedes all results. Missing/insufficient Method is Inconclusive.
    Wrong primary permission is Failed; only secondary disagreement is Partial.
    """
    if record["method"] not in ("Static authored comparison", "Scanner summary only"):
        raise ValueError("unknown Retest Method")
    if record["requiredMethod"] != "Static authored comparison":
        raise ValueError("finite acceptance Method")
    if record["stopTrigger"] not in ("None", "Unexpected-input-symbol"):
        raise ValueError("unknown Stop")
    if type(record["stepsAfterStop"]) is not int or record["stepsAfterStop"] != 0:
        raise ValueError("no continuation after Stop")
    if type(record["actualOperations"]) is not int or record["actualOperations"] != 0:
        raise ValueError("no actual operations")
    if len(record["criteria"]) != 2 or len(record["observations"]) != 2:
        raise ValueError("two criteria and two evidence slots")
    ids = [c["id"] for c in record["criteria"]]
    if len(set(ids)) != 2 or [c["field"] for c in record["criteria"]] != [
        "permission",
        "auditReference",
    ]:
        raise ValueError("distinct ordered acceptance criteria")
    outcomes = []
    for c, o in zip(record["criteria"], record["observations"]):
        if (
            not c["id"]
            or not c["expected"]
            or type(c["expected"]) is not str
            or o["criterionId"] != c["id"]
            or o["subjectId"] != record["subjectId"]
            or o["revision"] != record["changedRevision"]
            or type(o["present"]) is not bool
        ):
            raise ValueError("Retest subject/revision/criterion identity")
        if o["present"]:
            if (
                type(o["value"]) is not str
                or not o["value"]
                or o["basis"] != "authored-supplied-value"
            ):
                raise ValueError("present supplied evidence")
            outcomes.append(o["value"] == c["expected"])
        else:
            if o["value"] is not None or o["basis"] != "missing-not-failed":
                raise ValueError("missing evidence is not a failed observation")
            outcomes.append(None)
    if record["stopTrigger"] != "None":
        return "Stopped"
    if record["method"] != record["requiredMethod"] or None in outcomes:
        return "Inconclusive"
    if not outcomes[0]:
        return "Failed"
    return "Passed" if outcomes[1] else "Partial"


def acceptance_valid(finding, as_of):
    """Finite supplied delegation scope and expiry, not real authority issuance."""
    a = finding["acceptance"]
    if type(a["present"]) is not bool:
        raise ValueError("typed acceptance presence")
    if a["overridesAssessmentAuthority"] is not False:
        raise ValueError("acceptance never grants assessment permission")
    fields = [k for k in a if k not in ("present", "overridesAssessmentAuthority")]
    if not a["present"]:
        if any(a[k] is not None for k in fields):
            raise ValueError("absent acceptance has no borrowed metadata")
        return False
    if any(type(a[k]) is not str or not a[k].strip() for k in fields):
        raise ValueError("complete explicit acceptance")
    if (
        a["findingId"] != finding["id"]
        or a["subjectId"] != finding["subjectId"]
        or a["scope"] != "current-supplied-scenario-only"
        or a["authorityHolder"] != a["decisionOwner"]
        or a["basis"] != "authored-delegation-not-assessment-permission"
        or a["residualRiskId"] != finding["residualRisk"]["id"]
        or a["reassessmentId"] != finding["reassessment"]["id"]
    ):
        raise ValueError("acceptance holder/scope/traceability")
    decided, expiry, now = utc(a["decidedAt"]), utc(a["expiresAt"]), utc(as_of)
    if decided >= expiry or decided > now:
        raise ValueError("acceptance chronology")
    return now < expiry


def finding_status(finding, retest, as_of):
    """Guard an authored workflow decision; severity is never the decision maker."""
    valid = acceptance_valid(finding, as_of)
    result = None
    if retest is not None:
        if (
            retest["id"] != finding["retestId"]
            or retest["findingId"] != finding["id"]
            or retest["subjectId"] != finding["subjectId"]
            or retest["beforeRevision"] != finding["subjectRevision"]
            or retest["residualRiskId"] != finding["residualRisk"]["id"]
            or retest["reassessmentId"] != finding["reassessment"]["id"]
        ):
            raise ValueError("Finding/Retest direct reference")
        result = retest_result(retest)
    elif finding["retestId"] is not None:
        raise ValueError("missing referenced Retest")
    stage = finding["requestedStage"]
    basis = finding["decision"]["basis"]
    if stage in ("Accept", "Close"):
        acceptable = (basis == "acceptance" and valid) or (
            stage == "Close" and basis == "retest" and result == "Passed"
        )
        if not acceptable:
            raise ValueError(
                "Closed/Accepted needs sufficient Retest or valid explicit acceptance"
            )
        return "Accepted" if stage == "Accept" else "Closed"
    if basis != "open-review":
        raise ValueError("nonclosing decision basis")
    if stage == "Report":
        return "Open"
    if stage == "Mitigate":
        if not finding["temporaryReviewEvidenceId"]:
            raise ValueError(
                "Mitigated needs bounded supplied temporary review evidence"
            )
        return "Mitigated"
    if stage == "Retest":
        return "Retest required"
    if stage == "Reopen":
        expired = finding["acceptance"]["present"] and not valid
        if not finding["reassessment"]["reopenReason"] or not (
            expired or result == "Stopped"
        ):
            raise ValueError("Reopened needs a supplied invalidation condition")
        return "Reopened"
    raise ValueError("unknown Finding workflow stage")


def authored_inputs(data):
    """Only supplied inputs are frozen; outputs are independently recomputed."""
    d = deepcopy(data)
    for f in d["findings"]:
        del f["status"]
    for r in d["retests"]:
        del r["result"]
    return d


def validate_model(data, schema, contract):
    errors = []
    if (
        hashlib.sha256(
            json.dumps(schema, ensure_ascii=False, sort_keys=True).encode()
        ).hexdigest()
        != contract["schemaSha256"]
    ):
        return ["ART04/23 frozen closed Schema identity"]
    try:
        validate_supported_schema_nodes(schema, "ART04/23-schema", schema)
        validate_schema_instance(data, schema)
    except (ManifestError, ValueError, TypeError, KeyError) as exc:
        return ["ART04/23 Schema: " + str(exc)]

    def need(ok, label):
        if not ok:
            errors.append("ART04/23 " + label)

    need(
        authored_inputs(data) == contract["authoredInputs"],
        "finite supplied inputs and parent nonexecution baseline",
    )
    findings = data["findings"]
    retests = data["retests"]
    as_of = data["record"]["asOf"]
    need(
        [f["id"] for f in findings] == [f"FND-FRT15-{i:03}" for i in range(1, 8)],
        "seven ordered distinct Findings",
    )
    need(
        [r["id"] for r in retests] == [f"RT-FRT15-{i:03}" for i in (1, 2, 4, 5, 6)],
        "five ordered distinct Retests",
    )
    if errors:
        return errors
    lookup = {r["id"]: r for r in retests}
    for i, f in enumerate(findings, 1):

        def rid(prefix):
            return f"{prefix}-FRT15-{i:03}"

        v = f["validation"]
        need(
            v["id"] == rid("VAL")
            and v["findingId"] == f["id"]
            and v["subjectId"] == f["subjectId"]
            and v["subjectRevision"] == f["subjectRevision"],
            "initial validation binding",
        )
        need(
            f["evidenceIds"] == [v["evidenceId"]] == [rid("EVD")],
            "owned initial evidence",
        )
        need(
            v["requirementPermission"] != v["declaredPermission"]
            and v["basis"] == "authored-supplied-values",
            "bounded design discrepancy, not implementation claim",
        )
        for group, prefix in [
            ("rootCondition", "ROOT"),
            ("residualRisk", "RES"),
            ("decision", "DEC"),
            ("reassessment", "REA"),
        ]:
            need(f[group]["id"] == rid(prefix), "typed direct " + group + " ID")
        need(
            f["decision"]["findingId"] == f["reassessment"]["findingId"] == f["id"],
            "decision/reassessment Finding binding",
        )
        need(
            f["recommendedTreatmentId"] in [t["id"] for t in f["treatments"]],
            "Treatment selection owned",
        )
        need(
            [t["kind"] for t in f["treatments"]]
            == ["Temporary", "Permanent", "Compensating"],
            "three distinct Treatment kinds",
        )
        need(
            f["temporaryReviewEvidenceId"]
            == (rid("TMP-EVD") if f["requestedStage"] == "Mitigate" else None),
            "bounded temporary review identity",
        )
        need(
            not f["priority"]["automaticDecision"]
            and all(
                f["priority"][k] is None
                for k in ("cvssScore", "cvssVector", "cvssNomenclature")
            ),
            "no fabricated rating or automatic acceptance",
        )
        a = f["acceptance"]
        if a["present"]:
            need(
                a["id"] == rid("ACC") and a["authorityReference"] == rid("DELEGATION"),
                "owned acceptance/delegation",
            )
        r = lookup.get(f["retestId"])
        try:
            need(
                utc(as_of) < utc(f["reassessment"]["dueAt"]),
                "reassessment date after fixed supplied snapshot",
            )
            for t in f["treatments"]:
                need(utc(as_of) < utc(t["dueAt"]), "Treatment due date")
            need(
                f["status"] == finding_status(f, r, as_of),
                "recomputed Finding status " + f["id"],
            )
            if r:
                need(
                    r["changeReference"] == rid("CHG")
                    and r["changedRevision"] == rid("AFTER")
                    and r["changedRevision"] != r["beforeRevision"],
                    "Retest changed revision and change reference",
                )
                need(r["scope"] == "current-supplied-scenario-only", "Retest scope")
                need(utc(r["recordedAt"]) <= utc(as_of), "Retest evidence time")
                need(
                    r["result"] == retest_result(r),
                    "recomputed Retest result " + r["id"],
                )
                need(
                    [o["id"] for o in r["observations"]]
                    == [rid("RT-EVD") + "-" + str(j) for j in (1, 2)],
                    "owned Retest observation IDs",
                )
        except (ValueError, KeyError, TypeError) as exc:
            errors.append("ART04/23 decision " + f["id"] + ": " + str(exc))
    for path, value in leaves(data):
        if isinstance(value, str):
            location = "ART04/23/" + "/".join(path)
            need(0 < len(value.strip()) <= 2000, "nonempty bounded leaf " + location)
            errors += [
                location + ": " + f.category
                for f in scan_action_text(value, location=location)
                + scan_host_policy(value, location=location)
            ]
    return errors
