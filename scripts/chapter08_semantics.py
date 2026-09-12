"""ART-18 finite offline receipt model; not a container or legal assurance engine.

Layer A only: eight states and teaching-record ownership/time/evidence contracts.
No network, container operations, host probing, cleanup deletion or syntax parser.
"""

from __future__ import annotations

from datetime import datetime, timedelta
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
STATES = (
    "Planned",
    "Preflight passed",
    "Ready",
    "Running",
    "Stopped",
    "Destroyed",
    "Cleanup verified",
    "Failed closed",
)
RESULTS = ("Pass", "Fail", "Unknown")
STAGES = {
    "preflight": (
        "authority",
        "rootless",
        "privileges",
        "network",
        "egress",
        "mount",
        "data",
        "collection",
    ),
    "runtime": (
        "egress",
        "scope",
        "privileges",
        "data",
        "resources",
        "collection",
        "clock",
    ),
    "stop": ("stopped",),
    "export": ("evidenceExport",),
    "destroy": ("destroyed",),
    "cleanup": ("container", "network", "volume", "file", "credential", "port"),
}
RUN_IDS = ("RUN-LAB08-SAFE", "RUN-LAB08-UNSAFE", "RUN-LAB08-INCONCLUSIVE")
IDENTITY = {
    "schemaVersion": "1.0.0",
    "synthetic": True,
    "artifactId": "ART-18",
    "planSetId": "LABPLAN-2026-001",
    "parentCaseId": "CASE-2026-001",
    "relation": "refines",
    "decisionRequirementId": "DR-2026-001",
    "authorizationRecordId": "AUTH-CASE-2026-001",
    "parentThreatModelId": "TM-2026-001",
    "parentSignalMapId": "SFM-2026-001",
    "parentPrioritySetId": "VPR-2026-001",
    "scope": "read-only-synthetic-data",
    "modelVersion": MODEL_VERSION,
    "executionMode": "offline-receipt-replay",
    "runtimeExecuted": False,
    "parentState": "No inherited observation, control, gap, priority or authorization is promoted.",
    "legalBoundary": "Educational reproducibility only; not legal admissibility or production assurance.",
}
ARCHITECTURE = {
    "platformModel": "WSL2 and rootless Podman equivalent abstract design",
    "runtimeVersion": "not-executed",
    "imageDigest": None,
    "rootless": True,
    "privileged": False,
    "capabilities": [],
    "hostNetwork": False,
    "egressPolicy": "default-deny",
    "allowedEndpointClass": "reserved-synthetic-only",
    "networkId": "NET-LAB08-001",
    "exampleHost": "lab.test",
    "exampleAddress": "192.0.2.8",
    "exposure": "local-only-design-not-opened",
    "inputMode": "read-only",
    "outputMode": "ephemeral-design-not-allocated",
    "mountScope": "dedicated-lab-directory-only",
    "credentialMaterial": "none",
    "classification": "synthetic-only",
    "limits": "bounded-cpu-memory-disk-time-model; no actual runtime measurement",
}
PATHS = (
    "cases/fixtures/ch08-lab-plan.json",
    "cases/fixtures/ch08-control-receipts.json",
    "cases/fixtures/ch08-evidence-manifest.json",
)
EVIDENCE_IDENTITY = {
    "schemaVersion": "1.0.0",
    "synthetic": True,
    "manifestId": "EVM-LAB08-001",
    "artifactId": "EVD-LAB08-001",
    "createdAt": "2026-09-13T00:10:00Z",
    "classification": "synthetic-only",
    "custodian": "SYNTH-EVIDENCE-CUSTODIAN",
    "retention": "versioned teaching artifact; no credential material",
    "limitation": "Hash agreement verifies supplied bytes, not authenticity, legal admissibility or real execution.",
}
# These are the common boundaries of the closed teaching set, not a general
# acceptance grammar for future real labs. A new scope needs a new review.
RUN_BOUNDARIES = {
    "prohibitedEvidence": "実Credential・実Token・実Cookie・個人情報は収集しない。",
    "stopCondition": "FailまたはUnknownなら新規シナリオ操作を停止し、状態とEvidenceを保存する。",
    "rollback": "合成資源台帳の停止・Evidence export・破棄・六種残存検査を順に照合する。",
    "evidenceRetention": "EVD-LAB08-001は教材正本として保持し、削除対象の一時資源とは区別する。",
    "gap": "実Runtimeの隔離・停止・残存は未測定。親のGapは不変。",
    "confidence": "低",
    "alternative": "供給された合成receiptが実環境で成立するとは限らない。",
    "reassessmentTrigger": "新Run ID、Authority、境界、実装版、時計、収集状態、残存結果の変更。",
    "nextReviewDate": "2026-09-14",
    "roeReference": "not-issued; S0/S1 read-only lesson, no operational RoE",
    "emergencyContact": "SYNTH-LAB-OWNER",
}


def encoded(value):
    """Frozen UTF-8 artifact serialization; explicit input order and LF."""
    return (
        json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    ).encode("utf-8")


def generate_receipts():
    """Regenerate the one finite authored scenario set (seed label 208).

    No randomness or real clock is used. Values are supplied teaching assumptions,
    not measured results. The seed labels this recipe; it is not a runtime option.
    """
    rows, signals = [], []
    for i, rid in enumerate(RUN_IDS, 1):
        start = datetime(2026, 9, 13, 0, (i - 1) * 2)
        for j, (stage, check) in enumerate(
            [(stage, name) for stage, names in STAGES.items() for name in names], 1
        ):
            result = "Pass"
            if i == 2 and (stage, check) == ("runtime", "egress"):
                result = "Fail"
            if i == 3 and (stage, check) in (
                ("runtime", "collection"),
                ("cleanup", "credential"),
            ):
                result = "Unknown"
            rows.append(
                {
                    "receiptId": f"RCP-LAB08-{i:03}-{j:03}",
                    "runId": rid,
                    "synthetic": True,
                    "stage": stage,
                    "check": check,
                    "result": result,
                    "observedAt": (start + timedelta(seconds=j)).strftime(
                        "%Y-%m-%dT%H:%M:%SZ"
                    ),
                    "producerId": "SYNTH-CH08-GENERATOR",
                    "basis": "supplied synthetic control check; not a host observation",
                }
            )
        for j, kind in enumerate(
            (
                "oauth-consent-observation",
                "api-authorization-observation",
                "telemetry-collection-observation",
            ),
            1,
        ):
            signals.append(
                {
                    "eventId": f"EVENT-LAB08-{i:03}-{j:03}",
                    "runId": rid,
                    "synthetic": True,
                    "eventClass": kind,
                    "actorId": f"SYNTH-ACTOR-LAB08-{i:03}",
                    "exampleHost": "identity.lab.test",
                    "credentialMaterial": "none",
                    "recordedAt": (start + timedelta(seconds=10 + j)).strftime(
                        "%Y-%m-%dT%H:%M:%SZ"
                    ),
                    "meaning": "teaching record only; no protocol request was sent",
                }
            )
    return {
        "schemaVersion": "1.0.0",
        "synthetic": True,
        "fixtureId": "FIX-LAB08-001",
        "generatorVersion": MODEL_VERSION,
        "seed": 208,
        "producerId": "SYNTH-CH08-GENERATOR",
        "timeBasis": "fixed synthetic UTC; not synchronized with a real host",
        "receipts": rows,
        "signals": signals,
    }


def strict_bytes(raw):
    return json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=_reject_duplicate_keys,
        parse_constant=_reject_constant,
    )


def read_artifact(root: Path, relative: str):
    """Read only the three fixed, regular canonical files, before interpreting data.

    This guards a stable authoring worktree, not a concurrently hostile filesystem.
    No caller-controlled general file access or symlink traversal is supported.
    """
    if relative not in PATHS or root.is_symlink():
        raise ValueError("ART18 artifact path outside finite inventory")
    root = root.resolve(strict=True)
    current = root
    for part in PurePosixPath(relative).parts:
        current /= part
        if current.is_symlink():
            raise ValueError("ART18 symlink artifact/ancestor forbidden")
    if not current.resolve(strict=True).is_relative_to(root):
        raise ValueError("ART18 artifact containment")
    fd = os.open(current, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= 1024 * 1024:
            raise ValueError("ART18 regular bounded artifact required")
        raw = stream.read(1024 * 1024 + 1)
    if len(raw) > 1024 * 1024:
        raise ValueError("ART18 artifact size")
    return raw, strict_bytes(raw)


def utc(value):
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError("ART18 explicit UTC timestamp required")
    try:
        d = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise ValueError("ART18 canonical UTC timestamp") from exc
    if d.strftime("%Y-%m-%dT%H:%M:%SZ") != value:
        raise ValueError("ART18 noncanonical UTC timestamp")
    return d


def evaluate(receipts):
    """Evaluate validated, same-run synthetic receipts without executing a lab.

    A terminal cleanup state never erases earlier failures. Failed/unknown preflight
    cannot enter Running. After failure only preservation/stop/destroy/cleanup remain.
    """
    by_stage = {stage: [r for r in receipts if r["stage"] == stage] for stage in STAGES}
    for stage, names in STAGES.items():
        if [r["check"] for r in by_stage[stage]] != list(names):
            raise ValueError("ART18 missing/duplicate/out-of-order check " + stage)
    if len(receipts) != sum(map(len, STAGES.values())):
        raise ValueError("ART18 unowned check")
    if (
        [(r["stage"], r["check"]) for r in receipts]
        != [(stage, name) for stage, names in STAGES.items() for name in names]
        or len({r["runId"] for r in receipts}) != 1
        or len({r["receiptId"] for r in receipts}) != len(receipts)
    ):
        raise ValueError("ART18 same-run check order/identity")
    if any(r["result"] not in RESULTS for r in receipts):
        raise ValueError("ART18 unknown check result")
    history, visited, skipped = ["Planned"], [], []

    def passed(stage):
        visited.extend(by_stage[stage])
        return all(r["result"] == "Pass" for r in by_stage[stage])

    def failed():
        if history[-1] != "Failed closed":
            history.append("Failed closed")

    if passed("preflight"):
        history.extend(("Preflight passed", "Ready", "Running"))
        normal = passed("runtime")
        if not normal:
            failed()
    else:
        normal = False
        skipped.append("runtime")
        failed()
    stopped = passed("stop")
    exported = destroyed = cleaned = False
    if stopped:
        history.append("Stopped")
        exported = passed("export")
        if exported:
            destroyed = passed("destroy")
            if destroyed:
                history.append("Destroyed")
                cleaned = passed("cleanup")
                if cleaned:
                    history.append("Cleanup verified")
                else:
                    failed()
            else:
                failed()
                skipped.append("cleanup")
        else:
            failed()
            skipped.extend(("destroy", "cleanup"))
    else:
        failed()
        skipped.extend(("export", "destroy", "cleanup"))
    bad = [r["receiptId"] for r in visited if r["result"] == "Fail"]
    unknown = [r["receiptId"] for r in visited if r["result"] == "Unknown"]
    return {
        "verdict": "Unsafe" if bad else "Inconclusive" if unknown else "Safe",
        "statusHistory": history,
        "finalStatus": history[-1],
        "completedNormally": normal and stopped and exported and destroyed and cleaned,
        "cleanupVerified": cleaned,
        "executionAuthorized": False,
        "failureReceiptIds": bad,
        "unknownReceiptIds": unknown,
        "skippedStages": skipped,
    }


def json_safety(value, path=(), *, manifest=False):
    """All JSON values AND keys are plain data; shared Policy owns grammar."""
    out = []
    if isinstance(value, dict):
        for k, v in value.items():
            out += json_safety(k, path + (k, "key"), manifest=manifest) + json_safety(
                v, path + (k,), manifest=manifest
            )
    elif isinstance(value, list):
        for i, v in enumerate(value):
            out += json_safety(v, path + (i,), manifest=manifest)
    elif isinstance(value, str):
        location = "ART18:" + repr(path)
        if any(c in value for c in "<>&`\\"):
            out.append(location + ": plain-text data only")
        # One local filename is classified as a possible host by Layer C.
        # Exact document kind + tuple path + value only; never exempt actions.
        # validate_bundle separately binds this path to EVD-LAB08-001 and the
        # bytes actually read. This is not a filename/domain/suffix allowlist.
        findings = scan_action_text(value, location=location)
        if not (manifest and path == ("artifactPath",) and value == PATHS[1]):
            findings += scan_host_policy(value, location=location)
        out += [location + ": " + f.category for f in findings]
    return out


def validate_bundle(plan, receipts, manifest, raw_receipts, schemas, parents):
    errors = []
    try:
        for index, (value, schema) in enumerate(
            zip((plan, receipts, manifest), schemas, strict=True)
        ):
            validate_supported_schema_nodes(schema, "ART18 schema", schema)
            validate_schema_instance(value, schema)
            errors += json_safety(value, manifest=index == 2)
        if any(
            type(plan.get(k)) is not type(v) or plan[k] != v
            for k, v in IDENTITY.items()
        ):
            raise ValueError("ART18 identity/authority/parent-state")
        if plan["architecture"] != ARCHITECTURE:
            raise ValueError("ART18 requested safe architecture")
        if any(manifest.get(k) != v for k, v in EVIDENCE_IDENTITY.items()):
            raise ValueError("ART18 evidence identity/retention/limitation")
        for parent, id_key, expected_id in (
            (parents[0], "mapId", IDENTITY["parentSignalMapId"]),
            (parents[1], "recordSetId", IDENTITY["parentPrioritySetId"]),
        ):
            if parent.get(id_key) != expected_id or any(
                parent.get(k) != IDENTITY[k]
                for k in (
                    "synthetic",
                    "parentCaseId",
                    "relation",
                    "parentThreatModelId",
                    "decisionRequirementId",
                    "authorizationRecordId",
                    "scope",
                )
            ):
                raise ValueError("ART18 actual parent root identity/authority")
        if plan["states"] != list(STATES) or [r["runId"] for r in plan["runs"]] != list(
            RUN_IDS
        ):
            raise ValueError("ART18 finite state/run inventory")
        if (
            receipts["generatorVersion"] != MODEL_VERSION
            or receipts["seed"] != 208
            or receipts["synthetic"] is not True
        ):
            raise ValueError("ART18 synthetic receipt identity")
        if (
            manifest["artifactPath"] != PATHS[1]
            or hashlib.sha256(raw_receipts).hexdigest() != manifest["sha256"]
        ):
            raise ValueError("ART18 actual artifact/hash mismatch")
        if raw_receipts != encoded(receipts) or raw_receipts != encoded(
            generate_receipts()
        ):
            raise ValueError("ART18 canonical UTF-8 LF serialization")
        if (
            manifest["runIds"] != list(RUN_IDS)
            or manifest["producerId"] != receipts["producerId"]
        ):
            raise ValueError("ART18 evidence run/producer binding")
        if (
            manifest["artifactId"] != "EVD-LAB08-001"
            or manifest["sourceFixtureId"] != receipts["fixtureId"]
        ):
            raise ValueError("ART18 evidence identity/lineage")
        if manifest["transformHistory"] != [
            {
                "operation": "synthetic-generation",
                "inputIds": [],
                "outputArtifactId": "EVD-LAB08-001",
                "producerId": receipts["producerId"],
                "generatorVersion": MODEL_VERSION,
                "seed": 208,
                "recordedAt": "2026-09-13T00:10:00Z",
            }
        ]:
            raise ValueError("ART18 finite synthetic creation lineage")
        ids = [r["receiptId"] for r in receipts["receipts"]]
        if len(ids) != len(set(ids)):
            raise ValueError("ART18 duplicate receipt identity")
        owned = []
        for i, run in enumerate(plan["runs"], 1):
            if any(run.get(k) != v for k, v in RUN_BOUNDARIES.items()):
                raise ValueError("ART18 run boundary/retention/reassessment")
            if (
                run["scope"] != IDENTITY["scope"]
                or run["signalFlowId"] != "SF-2026-001"
                or run["priorityRecordId"] != "VPR-ITEM-005"
            ):
                raise ValueError("ART18 closed read-only lesson/parent selection")
            if run["expected"]["verdict"] != ("Safe", "Unsafe", "Inconclusive")[i - 1]:
                raise ValueError("ART18 Safe/Unsafe/Inconclusive lesson inventory")
            signal_ids = [
                r["eventId"] for r in receipts["signals"] if r["runId"] == run["runId"]
            ]
            if run["signalIds"] != signal_ids or len(signal_ids) != 3:
                raise ValueError("ART18 synthetic signal ownership")
            rows = [r for r in receipts["receipts"] if r["runId"] == run["runId"]]
            if run["receiptIds"] != [r["receiptId"] for r in rows]:
                raise ValueError("ART18 receipt ownership")
            owned.extend(run["receiptIds"])
            expected_order = [
                (stage, check) for stage, names in STAGES.items() for check in names
            ]
            if [(r["stage"], r["check"]) for r in rows] != expected_order:
                raise ValueError("ART18 receipt stage/order inventory")
            times = [utc(r["observedAt"]) for r in rows]
            if times != sorted(set(times)) or not utc(run["startsAt"]) <= times[
                0
            ] <= times[-1] <= utc(run["endsAt"]) < utc(manifest["createdAt"]):
                raise ValueError("ART18 receipt time/run/export sequence")
            if any(
                r["producerId"] != receipts["producerId"] or r["synthetic"] is not True
                for r in rows
            ):
                raise ValueError("ART18 receipt producer/synthetic")
            if run["expected"] != evaluate(rows):
                raise ValueError("ART18 derived state/verdict mismatch")
            parent_flow = next(
                f for f in parents[0]["flows"] if f["flowId"] == run["signalFlowId"]
            )
            priority = next(
                r
                for r in parents[1]["records"]
                if r["recordId"] == run["priorityRecordId"]
            )
            if (
                run["signalFlowId"] != priority["signalFlowId"]
                or run["parentCoverage"] != parent_flow["coverage"]
                or run["parentGapId"] != parent_flow["gapId"]
            ):
                raise ValueError("ART18 parent row/coverage/gap binding")
            if (
                run["assetIds"] != parent_flow["assetIds"]
                or run["boundaryIds"] != parent_flow["boundaryIds"]
            ):
                raise ValueError("ART18 asset/boundary linkage")
            expected_ids = {
                "planId": f"LABPLAN-08-{i:03}",
                "labId": f"LAB-08-{i:03}",
                "executionStepId": f"STEP-LAB08-{i:03}-REPLAY",
                "stopId": f"STOP-LAB08-{i:03}",
                "cleanupId": f"CLEAN-LAB08-{i:03}",
                "reassessmentId": f"REASSESS-LAB08-{i:03}",
                "evidenceArtifactId": "EVD-LAB08-001",
                "owner": "SYNTH-LAB-OWNER",
                "reviewer": "SYNTH-LAB-REVIEWER",
            }
            if any(run[k] != v for k, v in expected_ids.items()):
                raise ValueError("ART18 direct control ID/owner binding")
        if owned != ids:
            raise ValueError("ART18 unowned receipt")
    except (ValueError, TypeError, KeyError, StopIteration, ManifestError) as exc:
        errors.append("ART18: " + str(exc))
    return errors


def display(value):
    """ART-18 reader table values; JSON null and empty arrays stay distinct."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        return ", ".join(display(v) for v in value) if value else "空配列"
    return str(value)


def case_groups(data):
    """Finite ART-18 view model, not Markdown or renderer syntax parsing.

    Plan/manifest fields are individual rows. Receipts and signals use one row
    per identity, with every remaining key/value in input order. No value is
    hidden merely because its check is Unknown or its stage was skipped.
    """
    plan, receipts, manifest = data
    groups = [
        (
            "Document Control",
            [
                (k, display(v))
                for k, v in plan.items()
                if k not in ("architecture", "runs")
            ],
        ),
        (
            "Lab Architecture",
            [(k, display(v)) for k, v in plan["architecture"].items()],
        ),
    ]
    for run in plan["runs"]:
        groups.append(
            (run["runId"], [(k, display(v)) for k, v in run.items() if k != "expected"])
        )
        groups.append(
            (
                run["runId"] + " expected",
                [(k, display(v)) for k, v in run["expected"].items()],
            )
        )
    groups.append(
        (
            "Evidence Manifest",
            [(k, display(v)) for k, v in manifest.items() if k != "transformHistory"],
        )
    )
    for i, transform in enumerate(manifest["transformHistory"], 1):
        groups.append(
            (f"Transform {i}", [(k, display(v)) for k, v in transform.items()])
        )
    groups.append(
        (
            "Receipt Control",
            [
                (k, display(v))
                for k, v in receipts.items()
                if k not in ("receipts", "signals")
            ],
        )
    )
    for name, items, identity in (
        ("Control receipts", receipts["receipts"], "receiptId"),
        ("Synthetic signals", receipts["signals"], "eventId"),
    ):
        groups.append(
            (
                name,
                [
                    (
                        item[identity],
                        "; ".join(
                            f"{k}={display(v)}"
                            for k, v in item.items()
                            if k != identity
                        ),
                    )
                    for item in items
                ],
            )
        )
    return groups
