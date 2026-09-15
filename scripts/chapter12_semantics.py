"""Chapter12 Layer A: supplied ART20 IDs, necessary edges and evidence bounds.

Pure finite record comparison only. No network/authentication/credential parser,
no transitive path search, no IAM/protocol or legal conformance determination.
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
DATA_PATH = "cases/fixtures/ch12-identity-paths.json"
SCHEMA_PATH = "schemas/ch12-identity-paths.schema.json"
CONTRACT_PATH = "tests/fixtures/chapter12/publication-contract.json"
DOCUMENTS = (
    "manuscript/12-enterprise-identity.md",
    "templates/identity-attack-path-review.md",
    "cases/ch12-identity-path-review-example.md",
    "references/ch12-source-review-2026-09-15.md",
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
)
INPUTS = (DATA_PATH, SCHEMA_PATH, CONTRACT_PATH, *DOCUMENTS, *PARENTS)
CLASSES = ("Human", "Device", "Service", "Workload")
STATES = (
    "Hypothesized",
    "Config-confirmed",
    "Evidence-supported",
    "Validated",
    "Broken",
    "Unknown",
)
METHODS = ("Static review", "Policy simulation", "Synthetic replay")


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
        raise ValueError("ART20 fixed input inventory/root")
    if any(type(getattr(os, f, None)) is not int for f in ("O_NOFOLLOW", "O_NONBLOCK")):
        raise ValueError("ART20 requires Linux/WSL2 no-follow/nonblocking primitives")
    root = root.resolve(strict=True)
    current = root
    for part in PurePosixPath(relative).parts:
        current /= part
        if current.is_symlink():
            raise ValueError("ART20 symlink input/ancestor")
    if not current.resolve(strict=True).is_relative_to(root):
        raise ValueError("ART20 input containment")
    fd = os.open(current, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= 1024 * 1024:
            raise ValueError("ART20 bounded regular input required")
        raw = stream.read(1024 * 1024 + 1)
    if len(raw) > 1024 * 1024:
        raise ValueError("ART20 input size")
    return raw


def utc(value):
    parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    if parsed.strftime("%Y-%m-%dT%H:%M:%SZ") != value:
        raise ValueError("ART20 canonical UTC time")
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


def evaluate_path(data, path, request):
    """Compare necessary supplied conditions; never execute a request.

    Returns outcome and the first refuted necessary edge in declared order.
    A known denial refutes this particular conjunction even if another condition
    is unknown. No denial proves that alternative paths do not exist.
    """
    # This kernel consumes a shaped record, not an executable request. Bind
    # the tuple here as well so callers cannot accidentally compare another
    # principal/resource/action or revision under this path's label.
    if (
        any(
            request[k] != path[k]
            for k in (
                "pathId",
                "principalId",
                "resourceId",
                "action",
                "graphRevision",
                "policyRevision",
            )
            if k != "pathId"
        )
        or request["pathId"] != path["id"]
    ):
        raise ValueError("supplied comparison path/tuple/revision mismatch")
    edges = {e["id"]: e for e in data["edges"]}
    resources = {r["id"]: r for r in data["resources"]}
    denied, unknown = [], False
    for eid in path["edgeIds"]:
        edge = edges[eid]
        if edge["condition"] not in ("True", "False", "Unknown"):
            raise ValueError("unsupported necessary condition")
        if edge["condition"] == "False":
            denied.append(eid)
        elif edge["condition"] == "Unknown":
            unknown = True
        if edge["kind"] == "Federation" and (
            request["issuerId"] != edge["issuerId"]
            or request["audienceId"] != edge["audienceId"]
            or request["relyingPartyId"]
            != resources[path["resourceId"]]["relyingPartyId"]
            or request["audienceId"] != request["relyingPartyId"]
        ):
            denied.append(eid)
    if denied:
        return "Deny", denied[0]
    return ("Unknown", None) if unknown else ("Allow", None)


def validate_model(data, schema, contract):
    errors = []
    try:
        validate_supported_schema_nodes(schema, "ART20-schema", schema)
        validate_schema_instance(data, schema)
    except (ManifestError, TypeError, ValueError) as exc:
        return ["ART20 closed supplied-record schema: " + str(exc)]

    def need(condition, message):
        if not condition:
            errors.append("ART20 " + message)

    inventories = {
        "principals": ("PRN", range(1, 5)),
        "groups": ("GRP", range(1, 2)),
        "roles": ("ROL", range(1, 4)),
        "permissions": ("PER", range(1, 4)),
        "resources": ("RES", range(1, 4)),
        "controlPlanes": ("CP", range(1, 2)),
        "issuers": ("ISS", range(1, 2)),
        "relyingParties": ("RP", range(1, 4)),
        "edges": ("EDG", range(1, 15)),
        "paths": ("PTH", range(1, 7)),
        "configEvidence": ("EVD", (2, 3, 4, 5)),
        "eventEvidence": ("EVT", (3,)),
        "evaluations": ("EVAL", (4, 5)),
        "findings": ("FND", range(1, 7)),
        "handoffs": ("HOF", range(1, 6)),
    }
    for group, (prefix, numbers) in inventories.items():
        need(
            [r["id"] for r in data[group]]
            == [f"{prefix}-IAR12-{n:03}" for n in numbers],
            "finite unique ordered inventory " + group,
        )
    need(data["context"] == contract["context"], "unchanged parent-context limitations")
    need(
        all(data["record"].get(k) == v for k, v in contract["recordIdentity"].items()),
        "record identity and authored-not-measured boundary",
    )
    for group, expected in contract["identities"].items():
        for row in data[group]:
            baseline = expected.get(row["id"])
            need(
                baseline is not None
                and all(row.get(k) == v for k, v in baseline.items()),
                "finite identity/provenance " + group + "/" + row["id"],
            )
    need(
        data["schemaVersion"] == data["modelVersion"] == MODEL_VERSION, "model versions"
    )
    need(
        data["synthetic"] is True and data["executionAuthorized"] is False,
        "synthetic non-execution root",
    )
    need(
        data["parents"] == contract["parentSnapshot"],
        "literal unchanged parent authority/time/scope",
    )
    need(
        [p["principalClass"] for p in data["principals"]] == list(CLASSES),
        "four Principal classes",
    )
    if errors:
        return errors
    groups = {g: {r["id"]: r for r in data[g]} for g in inventories}
    node_kind = {
        rid: group
        for group in ("principals", "groups", "roles", "permissions", "resources")
        for rid in groups[group]
    }
    allowed_edges = {
        "Membership": {
            ("principals", "groups"),
            ("principals", "roles"),
            ("groups", "roles"),
        },
        "Grant": {("roles", "permissions")},
        "Access": {("permissions", "resources")},
        "Delegation": {("principals", "principals")},
        "Federation": {("principals", "roles")},
        "Trust": {("principals", "roles")},
    }
    for edge in data["edges"]:
        need(
            (node_kind.get(edge["fromId"]), node_kind.get(edge["toId"]))
            in allowed_edges[edge["kind"]],
            "typed edge " + edge["id"],
        )
        if edge["kind"] == "Federation":
            need(
                edge["issuerId"] in groups["issuers"]
                and edge["audienceId"] in groups["relyingParties"],
                "distinct issuer/audience namespace " + edge["id"],
            )
        else:
            need(
                edge["issuerId"] is None and edge["audienceId"] is None,
                "non-federation has no assertion fields " + edge["id"],
            )
    for resource in data["resources"]:
        need(
            resource["controlPlaneId"] in groups["controlPlanes"]
            and resource["relyingPartyId"] in groups["relyingParties"],
            "resource boundary " + resource["id"],
        )
        if resource["relyingPartyId"] in groups["relyingParties"]:
            need(
                groups["relyingParties"][resource["relyingPartyId"]]["resourceId"]
                == resource["id"],
                "RP/resource binding " + resource["id"],
            )
    for permission in data["permissions"]:
        need(
            permission["resourceId"] in groups["resources"],
            "permission resource " + permission["id"],
        )
    # Check prerequisites before following references or evaluating an expression.
    if errors:
        return errors
    try:
        record = data["record"]
        as_of = utc(record["asOf"])
        need(
            as_of > utc(data["parents"]["authorizationExpiresAt"]),
            "historical authority expired",
        )
        for i, principal in enumerate(data["principals"]):
            need(
                principal["credentialClass"]
                == (
                    "interactive-authenticator-class",
                    "device-binding-class",
                    "service-authentication-class",
                    "workload-authentication-class",
                )[i],
                "credential CLASS binding " + principal["id"],
            )
            if principal["principalClass"] != "Human":
                need(
                    principal["mfaStatus"] == "Not applicable"
                    and principal["mfaException"] == "none",
                    "nonhuman not assigned human MFA " + principal["id"],
                )
        for path in data["paths"]:
            pid = path["id"]
            need(
                path["state"] in STATES and path["validationMethod"] in METHODS,
                "state/method inventory " + pid,
            )
            need(
                path["principalId"] in groups["principals"]
                and path["resourceId"] in groups["resources"]
                and path["requiredPermissionId"] in groups["permissions"],
                "path endpoint/privilege " + pid,
            )
            refs = path["edgeIds"]
            need(
                bool(refs)
                and len(refs) <= 5
                and len(refs) == len(set(refs))
                and all(e in groups["edges"] for e in refs),
                "bounded unique necessary edges " + pid,
            )
            if errors:
                continue
            chain = [groups["edges"][e] for e in refs]
            vertices = [chain[0]["fromId"]] + [e["toId"] for e in chain]
            need(
                vertices[0] == path["principalId"]
                and vertices[-1] == path["resourceId"]
                and len(set(vertices)) == len(vertices)
                and all(a["toId"] == b["fromId"] for a, b in zip(chain, chain[1:])),
                "continuous noncyclic path " + pid,
            )
            permission = groups["permissions"][path["requiredPermissionId"]]
            need(
                path["requiredPermissionId"] == chain[-1]["fromId"]
                and permission["resourceId"] == path["resourceId"]
                and permission["action"] == path["action"],
                "required resource/action permission " + pid,
            )
            need(
                path["graphRevision"] == record["graphRevision"]
                and path["policyRevision"] == record["policyRevision"],
                "path graph/policy revision " + pid,
            )
            need(
                path["executionAuthorized"] is False
                and path["nextAction"] == "record-only",
                "path not permission " + pid,
            )
            need(
                utc(path["dueAt"]) > as_of, "future owner/reassessment deadline " + pid
            )
            config = groups["configEvidence"].get(path["configEvidenceId"])
            event = groups["eventEvidence"].get(path["eventEvidenceId"])
            evaluation = groups["evaluations"].get(path["evaluationId"])
            for name, evidence, ref in (
                ("config", config, path["configEvidenceId"]),
                ("event", event, path["eventEvidenceId"]),
                ("evaluation", evaluation, path["evaluationId"]),
            ):
                need(
                    (ref is None) == (evidence is None),
                    "existing evidence reference " + pid + "/" + name,
                )
                if evidence is not None:
                    need(
                        evidence["pathId"] == pid
                        and evidence["graphRevision"] == path["graphRevision"]
                        and evidence["policyRevision"] == path["policyRevision"]
                        and evidence["synthetic"] is True
                        and utc(evidence["recordedAt"]) <= as_of,
                        "same-path/version authored evidence " + pid + "/" + name,
                    )
            if config:
                need(config["edgeIds"] == refs, "config covers necessary edges " + pid)
            if event:
                need(
                    path["validationMethod"] == "Synthetic replay"
                    and config is not None,
                    "synthetic event method/config " + pid,
                )
                need(
                    all(
                        event[k] == path[k]
                        for k in ("principalId", "resourceId", "action")
                    ),
                    "event tuple binding " + pid,
                )
            if evaluation:
                need(
                    path["validationMethod"] == "Policy simulation"
                    and config is not None,
                    "finite comparison method/config " + pid,
                )
                need(
                    all(
                        evaluation[k] == path[k]
                        for k in ("principalId", "resourceId", "action")
                    ),
                    "evaluation principal/resource/action " + pid,
                )
                need(
                    evaluation["configEvidenceId"] == path["configEvidenceId"],
                    "evaluation source evidence " + pid,
                )
                need(
                    evaluation["conditions"]
                    == [
                        {"edgeId": e["id"], "condition": e["condition"]} for e in chain
                    ],
                    "complete ordered input condition vector " + pid,
                )
                actual, refuted = evaluate_path(data, path, evaluation)
                need(
                    evaluation["expected"] == evaluation["actual"] == actual
                    and evaluation["refutedEdgeId"] == refuted,
                    "recomputed outcome/refuted necessary edge " + pid,
                )
                need(
                    evaluation["networkRequests"]
                    == evaluation["authenticationAttempts"]
                    == 0,
                    "no network or authentication " + pid,
                )
            state = path["state"]
            if path["validationMethod"] == "Static review":
                need(
                    state in ("Hypothesized", "Config-confirmed", "Unknown")
                    and event is None
                    and evaluation is None,
                    "static review cannot validate " + pid,
                )
            if state == "Config-confirmed":
                need(config is not None, "config evidence required " + pid)
            if state == "Evidence-supported":
                need(
                    event is not None and config is not None,
                    "same-path event required " + pid,
                )
            if state in ("Validated", "Broken"):
                need(
                    evaluation is not None and config is not None,
                    "evaluation evidence required " + pid,
                )
                if evaluation:
                    actual, refuted = evaluate_path(data, path, evaluation)
                    need(
                        actual == ("Allow" if state == "Validated" else "Deny")
                        and (refuted is not None) == (state == "Broken"),
                        "state grounded in necessary conditions, not MFA " + pid,
                    )
            if any(e["condition"] == "Unknown" for e in chain) and not any(
                e["condition"] == "False" for e in chain
            ):
                need(state == "Unknown", "missing condition remains Unknown " + pid)
            for field, prefix in (
                ("telemetryId", "TEL"),
                ("detectionId", "DET"),
                ("findingId", "FND"),
                ("gapId", "GAP"),
                ("reassessmentId", "REA"),
            ):
                need(
                    path[field] == f"{prefix}-IAR12-{pid[-3:]}",
                    "direct child traceability " + pid + "/" + field,
                )
        for group, ref in (
            ("configEvidence", "configEvidenceId"),
            ("eventEvidence", "eventEvidenceId"),
            ("evaluations", "evaluationId"),
        ):
            need(
                [p[ref] for p in data["paths"] if p[ref] is not None]
                == list(groups[group]),
                "no unowned/borrowed evidence " + group,
            )
        for finding, path in zip(data["findings"], data["paths"]):
            need(
                finding["pathId"] == path["id"]
                and all(
                    finding[k] == path[k]
                    for k in ("telemetryId", "detectionId", "owner", "reassessmentId")
                ),
                "finding/path accountability " + finding["id"],
            )
        need(
            [h["chapter"] for h in data["handoffs"]] == [11, 13, 14, 16, 17],
            "bounded chapter handoffs",
        )
        for handoff in data["handoffs"]:
            need(
                handoff["pathIds"] == list(groups["paths"])
                and handoff["executionAuthorized"] is False
                and handoff["status"] == "planned-not-delivered",
                "handoff not permission " + handoff["id"],
            )
        limits = data["limits"]
        need(
            limits["networkRequests"] == limits["authenticationAttempts"] == 0
            and 0 < limits["minutes"] <= 30
            and 0 < limits["outputBytes"] <= 65536
            and 0 < limits["retentionHours"] <= 24,
            "finite non-executing budget",
        )
    except (ValueError, TypeError, KeyError, IndexError) as exc:
        errors.append("ART20 graph/evidence/time: " + str(exc))
    for path, value in leaves(data):
        if isinstance(value, str):
            location = "ART20/" + "/".join(path)
            need(len(value) <= 2000, "bounded field " + location)
            errors += [
                location + ": " + f.category
                for f in scan_action_text(value, location=location)
                + scan_host_policy(value, location=location)
            ]
    return errors
