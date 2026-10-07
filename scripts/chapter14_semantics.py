"""Chapter14 Layer A: finite supplied ART22 criteria, stop and reading-record completeness.

No real build/deploy/crypto or network. Not a generic validation/schema parser.
"""

from __future__ import annotations
from datetime import datetime
import json
import hashlib
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
DATA_PATH = "cases/fixtures/ch14-minimal-impact-validation.json"
SCHEMA_PATH = "schemas/ch14-minimal-impact-validation.schema.json"
CONTRACT_PATH = "tests/fixtures/chapter14/publication-contract.json"
DOCUMENTS = (
    "manuscript/14-minimal-impact-validation.md",
    "templates/minimal-impact-validation-record.md",
    "cases/ch14-minimal-impact-validation-example.md",
    "references/ch14-source-review-2026-09-16.md",
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
)
INPUTS = (DATA_PATH, SCHEMA_PATH, CONTRACT_PATH, *DOCUMENTS, *PARENTS)
METHODS = ("Static", "Simulation", "Offline replay", "Minimal synthetic operation")
RESULTS = (
    "Supported",
    "Partially supported",
    "Weakened",
    "Inconclusive",
    "Rejected",
    "Stopped",
)


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
        raise ValueError("ART22 fixed input inventory/root")
    if any(type(getattr(os, f, None)) is not int for f in ("O_NOFOLLOW", "O_NONBLOCK")):
        raise ValueError("ART22 requires Linux/WSL2 no-follow/nonblocking primitives")
    root = root.resolve(strict=True)
    current = root
    for part in PurePosixPath(relative).parts:
        current /= part
        if current.is_symlink():
            raise ValueError("ART22 symlink input/ancestor")
    if not current.resolve(strict=True).is_relative_to(root):
        raise ValueError("ART22 input containment")
    fd = os.open(current, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= 1024 * 1024:
            raise ValueError("ART22 bounded regular input required")
        raw = stream.read(1024 * 1024 + 1)
    if len(raw) > 1024 * 1024:
        raise ValueError("ART22 input size")
    return raw


def utc(value):
    parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    if parsed.strftime("%Y-%m-%dT%H:%M:%SZ") != value:
        raise ValueError("ART22 canonical UTC time")
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


def evaluate(record, expected):
    """Compare two supplied scalar criteria; never replay or execute a Method.

    Shaped inputs are the caller's responsibility, but identity, unknown values,
    missing observations and precedence are enforced here as well.
    """
    for actual, wanted in (
        (record["id"], expected["validationId"]),
        (record["expectationId"], expected["id"]),
        (record["subjectId"], expected["subjectId"]),
        (record["subjectRevision"], expected["subjectRevision"]),
        (record["method"], expected["method"]),
    ):
        if not actual or actual != wanted:
            raise ValueError("validation/expectation/subject/revision/method binding")
    if record["method"] not in METHODS:
        raise ValueError("unknown Method")
    if (
        len(expected["criterionIds"]) != 2
        or len(set(expected["criterionIds"])) != 2
        or len(expected["expectedValues"]) != 2
        or len(record["observations"]) != 2
    ):
        raise ValueError("two distinct criteria and two observations required")
    outcomes = []
    for observation, criterion, wanted in zip(
        record["observations"], expected["criterionIds"], expected["expectedValues"]
    ):
        if (
            observation["criterionId"] != criterion
            or observation["subjectId"] != expected["subjectId"]
            or observation["subjectRevision"] != expected["subjectRevision"]
            or type(observation["present"]) is not bool
            or type(wanted) is not str
            or not wanted
        ):
            raise ValueError("bound, typed criterion/observation required")
        if observation["present"]:
            if type(observation["value"]) is not str or not observation["value"]:
                raise ValueError("present observation requires nonempty scalar value")
            outcomes.append(observation["value"] == wanted)
        else:
            if (
                observation["value"] is not None
                or observation["recordedAt"] is not None
            ):
                raise ValueError("absent observation cannot carry value or timestamp")
            outcomes.append(None)
    trigger = record["stop"]["trigger"]
    disposition = record["executionDisposition"]
    if trigger not in ("None", "Unexpected-input-symbol"):
        raise ValueError("unknown stop trigger")
    if disposition not in ("Authored review only", "Not performed"):
        raise ValueError("unknown execution disposition")
    sufficient = all(value is not None for value in outcomes)
    if trigger != "None":
        return "Stopped", "Unexpected-input-symbol", sufficient
    if disposition == "Not performed":
        return "Inconclusive", "Not-performed", sufficient
    reason = "Evidence-sufficient" if sufficient else "Evidence-gap"
    if all(value is True for value in outcomes):
        result = "Supported"
    elif all(value is False for value in outcomes):
        result = "Rejected"
    elif any(value is True for value in outcomes):
        result = "Partially supported"
    elif any(value is False for value in outcomes):
        result = "Weakened"
    else:
        result = "Inconclusive"
    return result, reason, sufficient


def record_status(record):
    """Authored reading-record completeness, not operational remediation."""
    cleanup, residual = record["cleanup"], record["residual"]
    if cleanup["status"] not in ("Not started", "Recorded complete") or residual[
        "status"
    ] not in ("Unknown", "Recorded clear"):
        raise ValueError("unknown cleanup/residual status")
    complete = (
        cleanup["status"] == "Recorded complete"
        and residual["status"] == "Recorded clear"
        and all(
            type(group[k]) is str and bool(group[k].strip())
            for group in (cleanup, residual)
            for k in ("owner", "evidenceId")
        )
        and all(
            group["scope"] == "current-authored-reading-copy-only"
            for group in (cleanup, residual)
        )
        and all(
            type(record["judgment"][k]) is str and bool(record["judgment"][k].strip())
            for k in ("gap", "alternative", "claimCeiling")
        )
        and all(
            type(record["decision"][k]) is str and bool(record["decision"][k].strip())
            for k in ("owner", "dueAt", "reassessmentId", "reopenWhen")
        )
        and record["actualOperations"] == 0
        and record["decision"]["executionAuthorized"] is False
    )
    return "Complete" if complete else "Open"


def authored_input(record):
    """Freeze observations/questions separately from recomputed conclusions."""
    return {
        **{
            k: record[k]
            for k in (
                "decisionQuestion",
                "minimumEvidenceQuestion",
                "methodRationale",
                "unperformedReason",
                "observations",
            )
        },
        "judgment": {k: v for k, v in record["judgment"].items() if k != "result"},
        "treatment": record["finding"]["treatment"],
        "cleanupAction": record["cleanup"]["action"],
    }


def validate_model(data, schema, contract):
    errors = []
    if (
        hashlib.sha256(
            json.dumps(schema, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest()
        != contract["schemaSha256"]
    ):
        return ["ART22 frozen closed schema identity"]

    def need(ok, message):
        if not ok:
            errors.append("ART22 " + message)

    try:
        validate_supported_schema_nodes(schema, "ART22-schema", schema)
        validate_schema_instance(data, schema)
    except (ManifestError, ValueError, TypeError, KeyError) as exc:
        return ["ART22 closed supplied schema: " + str(exc)]
    for k, value in contract["fixedContext"].items():
        need(data[k] == value, "unchanged fixed context " + k)
    need(
        data["expectations"] == contract["expectations"], "separate frozen expectations"
    )
    need(
        [r["id"] for r in data["validations"]]
        == [f"VAL-MIV14-{i:03}" for i in range(1, 9)],
        "finite unique ordered validations",
    )
    if errors:
        return errors
    for i, (r, e, supplied) in enumerate(
        zip(data["validations"], data["expectations"], contract["authoredInputs"]), 1
    ):

        def rid(prefix):
            return f"{prefix}-MIV14-{i:03}"

        need(
            authored_input(r) == supplied,
            "authored questions/observations/ceilings " + r["id"],
        )
        bindings = [
            (r["revision"], data["record"]["revision"]),
            (r["hypothesisId"], rid("HYP")),
            (r["parentFindingId"], f"FND-PSA13-{i:03}"),
            (r["authorityId"], data["parents"]["authorizationId"]),
            (r["roeId"], data["parents"]["roeId"]),
            (r["labPlanId"], data["context"]["labPlanId"]),
            (r["subjectId"], rid("OBJ")),
            (r["subjectRevision"], "SUPPLIED-REV-001"),
            (r["stop"]["id"], rid("STP")),
            (r["cleanup"]["id"], rid("CLN")),
            (r["residual"]["id"], rid("RES")),
            (r["finding"]["id"], rid("FND")),
            (r["finding"]["validationId"], r["id"]),
            (r["decision"]["id"], rid("DEC")),
            (r["decision"]["findingId"], r["finding"]["id"]),
            (r["decision"]["stopId"], r["stop"]["id"]),
            (r["decision"]["cleanupId"], r["cleanup"]["id"]),
            (r["decision"]["residualId"], r["residual"]["id"]),
            (r["decision"]["reassessmentId"], rid("REA")),
        ]
        for j, (actual, wanted) in enumerate(bindings):
            need(actual == wanted, "direct binding " + r["id"] + "/" + str(j))
        observed = [o["id"] for o in r["observations"] if o["present"]]
        need(
            r["evidenceIds"] == r["finding"]["evidenceIds"] == observed,
            "exact observed evidence IDs " + r["id"],
        )
        not_performed = r["executionDisposition"] == "Not performed"
        need(
            r["method"] != "Minimal synthetic operation" or not_performed,
            "minimal operation stays unperformed " + r["id"],
        )
        need(
            not not_performed or not observed,
            "unperformed observations absent " + r["id"],
        )
        need(
            type(r["actualOperations"]) is int
            and r["actualOperations"] == 0
            and type(r["stepsAfterStop"]) is int
            and r["stepsAfterStop"] == 0
            and type(r["declaredReadSteps"]) is int
            and r["declaredReadSteps"] == (0 if not_performed else 1),
            "bounded reading/no operations or continuation " + r["id"],
        )
        stop = r["stop"]
        need(
            stop["triggerEvidenceId"]
            == (
                rid("STOP-EVD")
                if stop["trigger"] == "Unexpected-input-symbol"
                else None
            )
            and stop["nextAction"] == "Record limitation only",
            "stop record only " + r["id"],
        )
        for group, owner, complete, prefix in [
            ("cleanup", "Synthetic learner", "Recorded complete", "CLN-EVD"),
            ("residual", "Synthetic reviewer", "Recorded clear", "RES-EVD"),
        ]:
            value = r[group]
            need(
                value["scope"] == "current-authored-reading-copy-only"
                and value["owner"] == owner,
                "current reading-copy ownership " + r["id"] + "/" + group,
            )
            need(
                value["evidenceId"]
                == (rid(prefix) if value["status"] == complete else None),
                "cleanup/residual evidence " + r["id"] + "/" + group,
            )
        need(
            r["cleanup"]["actualDeletionPerformed"] is False
            and r["residual"]["actualSystemAssessed"] is False
            and r["decision"]["executionAuthorized"] is False,
            "not operational cleanup/authorization " + r["id"],
        )
        need(
            r["decision"]["owner"] == "Synthetic case owner"
            and bool(r["decision"]["reopenWhen"].strip()),
            "decision owner/reopen " + r["id"],
        )
        try:
            for j, o in enumerate(r["observations"], 1):
                need(
                    o["id"] == rid("EVD") + "-" + str(j),
                    "owned observation ID " + r["id"],
                )
                need(
                    o["basis"]
                    == (
                        "authored-observation"
                        if o["present"]
                        else "empty-evidence-slot-not-observed"
                    ),
                    "observation basis " + r["id"],
                )
                if o["present"]:
                    need(
                        utc(o["recordedAt"]) <= utc(data["record"]["asOf"]),
                        "observation time " + r["id"],
                    )
            need(
                utc(data["record"]["asOf"]) < utc(r["decision"]["dueAt"]),
                "reassessment time " + r["id"],
            )
            result, reason, sufficient = evaluate(r, e)
            need(
                r["judgment"]["result"] == result
                and stop["reason"] == reason
                and r["minimumEvidenceMet"] is sufficient,
                "recomputed Result/Stop/sufficiency " + r["id"],
            )
            need(
                r["decision"]["recordStatus"] == record_status(r),
                "recomputed completeness " + r["id"],
            )
        except (ValueError, TypeError, KeyError) as exc:
            errors.append("ART22 comparison " + r["id"] + ": " + str(exc))
    for path, value in leaves(data):
        if isinstance(value, str):
            location = "ART22/" + "/".join(path)
            need(0 < len(value) <= 2000, "bounded nonempty field " + location)
            errors += [
                location + ": " + f.category
                for f in scan_action_text(value, location=location)
                + scan_host_policy(value, location=location)
            ]
    return errors
