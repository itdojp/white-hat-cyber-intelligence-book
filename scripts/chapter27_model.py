"""Finite authored AI boundary comparisons; no model/tool execution or prompt parser."""

from datetime import datetime
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
DATA = "cases/fixtures/ch27-ai-agent-threat-model.json"
SCHEMA = "schemas/ch27-ai-agent-threat-model.schema.json"
CONTRACT = "tests/fixtures/chapter27/publication-contract.json"
CORPUS = "tests/fixtures/chapter27/comparison-corpus.json"
DOCUMENTS = (
    "manuscript/27-ai-agent-security.md",
    "templates/ai-agent-threat-model.md",
    "cases/ch27-ai-agent-threat-model-example.md",
    "references/ch27-source-review-2026-09-29.md",
)
SOURCES = (
    "SRC-AIRMF-001",
    "SRC-AML-001",
    "SRC-OWASP-LLM-001",
    "SRC-OWASP-AGENT-001",
    "SRC-AISVS-001",
)
STATES = ("Declared", "Observed", "Validated", "Restricted", "Disabled", "Unknown")
PARENTS = (
    "WRITING_GUIDE.md",
    "SOURCE_POLICY.md",
    "SAFETY_SCOPE.md",
    "CROSS_BOOK_MAP.md",
    "cases/ch01-integrated-security-case-example.md",
    "cases/ch04-threat-model-example.md",
    "cases/fixtures/ch06-signal-flow.json",
    "cases/fixtures/ch09-engagement-roe.json",
    "cases/fixtures/ch13-supply-chain.json",
    "cases/fixtures/ch26-cti-distribution.json",
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
        raise ValueError("AI27 " + code)


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


def read_regular(root, relative):
    """Only bounded known input files; not an adversarial concurrent-rename sandbox."""
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
    result = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
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


def component_state(component, as_of):
    """Precedence is about six authored component records, not runtime assurance."""
    c = component
    if c["disabled"]:
        return "Disabled"
    if c["restrictionActive"]:
        return "Restricted"
    if not c["descriptorKnown"]:
        return "Unknown"
    expected = (c["id"], c["version"], c["digest"])
    o, v = c["observation"], c["validation"]
    if v["present"] and not o["present"]:
        return "Restricted"
    if not o["present"]:
        return "Declared"
    if (o["target"], o["version"], o["digest"]) != expected or instant(
        o["observedAt"]
    ) > instant(as_of):
        return "Restricted"
    if not v["present"]:
        return "Observed"
    if (
        (v["target"], v["version"], v["digest"]) != expected
        or v["observedId"] != o["id"]
        or not v["passed"]
        or not instant(o["observedAt"]) <= instant(v["validatedAt"]) <= instant(as_of)
    ):
        return "Restricted"
    return "Validated"


def request_disposition(data, request):
    """Return ordered reasons only. Never execute, connect, evaluate a prompt or write."""
    r = request
    if r["killSwitchActive"] or r["stepsUsed"] > 3:
        return "Stopped", ["stop-or-budget"]
    reasons = []
    if r["stepBudget"] != 3:
        reasons.append("fixed-budget")

    def check(condition, code):
        if not condition:
            reasons.append(code)

    tools, components = index(data["tools"]), index(data["components"])
    instructions, memories = index(data["instructions"]), index(data["memory"])
    approvals, sources = index(data["approvals"]), index(data["sources"])
    check(
        r["userId"] == "AI27-USER" and r["caseId"] == "CASE-AI-2026-027",
        "request-scope",
    )
    check(r["modelId"] == "AI27-MODEL", "model-binding")
    check(r["asOf"] == data["record"]["asOf"], "comparison-time")
    t, c = tools.get(r["toolId"]), components.get(r["toolId"])
    check(t is not None and c is not None, "known-tool")
    if t and c:
        check(
            t["enabled"] and component_state(c, r["asOf"]) == "Validated",
            "tool-availability",
        )
        check(t["version"] == c["version"] == r["toolVersion"], "tool-version")
        check(
            r["requestedEffect"] == t["capability"] == "read-fixed-response"
            and t["sideEffect"] == "none",
            "tool-effect",
        )
        check(set(t["scope"]) == {r["caseId"], *r["sourceIds"]}, "tool-scope")
    instruction = instructions.get(r["instructionId"])
    check(
        instruction is not None
        and instruction["layer"] == "user-request"
        and instruction["origin"] == r["userId"]
        and instruction["treatedAs"] == "instruction"
        and not instruction["allowedOverride"],
        "instruction-origin",
    )
    check(r["sourceIds"] == ["AI27-SOURCE-1", "AI27-SOURCE-2"], "source-inventory")
    for sid in r["sourceIds"]:
        s = sources.get(sid)
        check(
            s is not None
            and s["caseId"] == r["caseId"]
            and s["audience"] == r["userId"]
            and s["version"] == "1.0"
            and s["origin"] == "author-synthetic",
            "source-scope",
        )
    m = memories.get(r["memoryId"])
    check(
        m is not None
        and not m["quarantined"]
        and m["caseId"] == r["caseId"]
        and m["audience"] == r["userId"]
        and m["version"] == "1.0"
        and m["sourceId"] in r["sourceIds"]
        and instant(r["asOf"]) < instant(m["expiresAt"]),
        "memory-scope-expiry",
    )
    a = approvals.get(r["approvalId"])
    check(a is not None, "approval-present")
    if a:
        check(
            a["ownerId"] == "AI27-OWNER"
            and a["ownerId"] != r["userId"]
            and a["requesterId"] == r["userId"]
            and a["origin"] == "human-owner-record"
            and a["decision"] == "Approved",
            "approval-owner",
        )
        check(
            a["singleRequestId"] == r["id"]
            and a["toolId"] == r["toolId"]
            and a["toolVersion"] == r["toolVersion"]
            and a["caseId"] == r["caseId"]
            and a["sourceIds"] == r["sourceIds"]
            and a["effect"] == r["requestedEffect"],
            "approval-action-binding",
        )
        check(
            instant(a["validFrom"]) <= instant(r["asOf"]) < instant(a["validUntil"]),
            "approval-window",
        )
    check(
        r["executed"] is False and data["executionAuthorized"] is False, "no-execution"
    )
    return ("Blocked" if reasons else "Allowed-in-model"), list(dict.fromkeys(reasons))


def validate_model(data, schema, contract):
    """Semantic outcomes and immutable authored literals are separate checks."""
    errors = []
    try:
        validate_supported_schema_nodes(schema, "schema", schema)
        validate_schema_instance(data, schema)
        require(
            data["synthetic"] is True
            and data["readOnly"] is True
            and data["executionAuthorized"] is False,
            "synthetic nonexecution boundary",
        )
        for key in (
            "modelApi",
            "network",
            "shell",
            "fileMutation",
            "credentialAccess",
            "personalData",
            "secretMaterial",
            "runtimeKillSwitchTested",
            "recoveryTested",
        ):
            require(
                data["safety"][key] is False,
                "no live capability or unobserved assurance",
            )
        require(
            data["safety"]["scope"] == "offline-authored-record-comparison",
            "fixed scope",
        )
        for key in (
            "adoptedAsFact",
            "adoptedAsSource",
            "adoptedAsCommand",
            "writtenToTrustedMemory",
        ):
            require(data["modelOutput"][key] is False, "no automatic output promotion")
        for memory in data["memory"]:
            require(memory["automaticWrite"] is False, "no automatic memory write")
        for tool in data["tools"]:
            require(
                tool["credentialClass"] == "none"
                and tool["actualImplementation"] == "none-record-only"
                and tool["approvalRequired"] is True
                and tool["approvalOwnerId"] == "AI27-OWNER"
                and tool["stopId"] == "AI27-STOP"
                and tool["timeoutSeconds"] == 30,
                "tool authority/stop boundary",
            )
        for key in (
            "parentEvidenceInherited",
            "parentAuthorityInherited",
            "realControlEffectivenessProven",
        ):
            require(data["record"][key] is False, "no parent/assurance inheritance")
        for key in ("actualModelCalls", "actualToolCalls", "actualExternalEffects"):
            require(
                type(data["record"][key]) is int and data["record"][key] == 0,
                "actual execution count zero",
            )
        require(
            data["parents"]["roeStatus"] == "Draft"
            and data["parents"]["roeDecision"] == "Do not proceed"
            and data["parents"]["authorizationState"] == "expired-not-renewed",
            "parent authorization unchanged",
        )
        # An independent fixed leaf inventory prevents correlated renaming or safety expansion.
        literal_rows = [[list(p), v] for p, v in leaves(data)]
        if literal_rows != contract["authoredLeaves"]:
            errors.append("AI27 authored literal inventory")
        for path, value in leaves(data):
            if type(value) is str:
                findings = scan_action_text(
                    value, location="/".join(path)
                ) + scan_host_policy(value, location="/".join(path))
                errors += [
                    "AI27 " + f.category + ": " + "/".join(path) for f in findings
                ]
        for group in (
            "actors",
            "instructions",
            "sources",
            "memory",
            "components",
            "tools",
            "approvals",
            "requests",
            "audit",
            "threats",
            "findings",
            "controls",
            "evidence",
            "gaps",
        ):
            index(data[group])
        if tuple(c["status"] for c in data["components"]) != STATES:
            errors.append("AI27 six-state inventory")
        for c in data["components"]:
            if c["status"] != component_state(c, data["record"]["asOf"]):
                errors.append("AI27 component status binding")
            if (
                c["digest"]
                != hashlib.sha256(c["provenance"]["label"].encode()).hexdigest()
            ):
                errors.append("AI27 synthetic label digest")
        for response in data["mockResponses"]:
            if (
                response["sha256"]
                != hashlib.sha256(response["body"].encode()).hexdigest()
            ):
                errors.append("AI27 fixed response digest")
        audit, findings, threats = (
            index(data[k]) for k in ("audit", "findings", "threats")
        )
        evidence, controls, gaps = (
            index(data[k]) for k in ("evidence", "controls", "gaps")
        )
        require(
            data["stop"]["id"] == "AI27-STOP"
            and data["stop"]["stepBudget"] == 3
            and data["stop"]["ownerId"] == "AI27-OWNER"
            and data["stop"]["runtimeTested"] is False
            and data["stop"]["auditRequired"] is True,
            "stop ownership/budget/audit",
        )
        for threat in data["threats"]:
            control = controls[threat["controlId"]]
            gap = gaps[control["gapId"]]
            require(
                control["threatId"] == threat["id"]
                and gap["controlId"] == control["id"]
                and control["runtimeValidated"] is False,
                "threat/control/gap binding",
            )
        for r in data["requests"]:
            state, reasons = request_disposition(data, r)
            if state != r["expectedDisposition"]:
                errors.append("AI27 request outcome")
            a, f = audit[r["auditId"]], findings[r["findingId"]]
            e = evidence[r["evidenceId"]]
            require(
                (
                    e["requestId"],
                    e["auditId"],
                    e["targetId"],
                    e["targetVersion"],
                    e["at"],
                )
                == (r["id"], r["auditId"], r["toolId"], r["toolVersion"], r["asOf"]),
                "evidence binding",
            )
            require(
                e["origin"] == "author-synthetic" and e["modelOutputAdopted"] is False,
                "evidence not model output",
            )
            require(
                bool(f["threatIds"]) and set(f["threatIds"]) <= set(threats),
                "threat/finding/reassessment",
            )
            require(
                f["controlIds"] == [threats[x]["controlId"] for x in f["threatIds"]],
                "finding controls",
            )
            require(
                f["validationIds"]
                == (["AI27-VAL-3"] if r["id"] == "AI27-REQUEST-1" else []),
                "finding validation limit",
            )
            if (
                a["requestId"],
                a["targetId"],
                a["targetVersion"],
                a["evidenceId"],
                a["findingId"],
                a["at"],
                a["disposition"],
            ) != (
                r["id"],
                r["toolId"],
                r["toolVersion"],
                r["evidenceId"],
                r["findingId"],
                r["asOf"],
                state,
            ):
                errors.append("AI27 audit binding")
            if (f["requestId"], f["evidenceId"], f["disposition"], f["reasons"]) != (
                r["id"],
                r["evidenceId"],
                state,
                reasons,
            ):
                errors.append("AI27 finding binding")
            if (
                not set(f["threatIds"]) <= set(threats)
                or not f["threatIds"]
                or f["reassessmentId"] != data["reassessment"]["id"]
            ):
                errors.append("AI27 threat/finding/reassessment")
            if not instant(a["at"]) < instant(a["retentionUntil"]):
                errors.append("AI27 audit retention")
        if (
            not instant(data["record"]["asOf"])
            < instant(data["record"]["reviewDeadline"])
            < instant(data["reassessment"]["dueAt"])
        ):
            errors.append("AI27 decision timeline")
    except (ValueError, KeyError, TypeError) as exc:
        errors.append("AI27 fail closed: " + str(exc))
    return errors
