"""Finite Chapter21 supplied-record comparison, not a live control validator.

This owns educational IDs, scopes, criteria and result semantics (Layer A).
It neither executes scenarios nor parses publication syntax.
"""

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
)
from scripts.content_safety_policy import scan_action_text, scan_host_policy

VERSION = "1.0.0"
DATA = "cases/fixtures/ch21-control-validation.json"
SCHEMA = "schemas/ch21-control-validation.schema.json"
CONTRACT = "tests/fixtures/chapter21/publication-contract.json"
CORPUS = "tests/fixtures/chapter21/comparison-corpus.json"
DOCUMENTS = (
    "manuscript/21-purple-team-validation.md",
    "templates/control-validation-plan.md",
    "cases/ch21-control-validation-example.md",
    "references/ch21-source-review-2026-09-25.md",
)
SOURCES = ("SRC-ATTACK-001", "SRC-ATTACK-DET-001", "SRC-NIST-ASSESS-001", "SRC-IR-001")
PARENTS = (
    "WRITING_GUIDE.md",
    "SOURCE_POLICY.md",
    "SAFETY_SCOPE.md",
    "CROSS_BOOK_MAP.md",
    "manuscript/14-minimal-impact-validation.md",
    "cases/fixtures/ch14-minimal-impact-validation.json",
    "manuscript/16-telemetry-evidence-readiness.md",
    "cases/fixtures/ch16-telemetry-coverage.json",
    "manuscript/17-detection-engineering.md",
    "cases/fixtures/ch17-detection-engineering-fixture.json",
    "manuscript/19-incident-response.md",
    "cases/fixtures/ch19-incident-response.json",
    "manuscript/20-dfir-timeline-causality.md",
    "cases/fixtures/ch20-dfir-timeline-causality.json",
    "scripts/content_safety_policy.py",
    "CONTENT_SAFETY_POLICY.md",
    "scripts/publication_projection.py",
    "scripts/_publication_projection_renderer.rb",
    "scripts/publication_text.py",
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
)
LAYERS = ("Prevention", "Telemetry", "Detection", "Triage", "Response")
RESULTS = ("Passed", "Failed", "Partial", "Indeterminate", "Stopped")
FAILURES = (
    "Control",
    "Telemetry",
    "Detection logic",
    "Workflow",
    "Authority",
    "Test design",
)
MISMATCH_CLASS = {
    "Prevention": "Control",
    "Telemetry": "Telemetry",
    "Detection": "Detection logic",
    "Triage": "Workflow",
    "Response": "Workflow",
}
# Author-owned criterion roles. Refreshing a JSON digest cannot redefine them.
CRITERIA = {
    "Prevention": (("scope-outcome", "blocked", (), ("blocked", "allowed")),),
    "Telemetry": (
        (
            "signal-coverage",
            "all-required",
            ("primary-only",),
            ("all-required", "primary-only", "missing-confirmed"),
        ),
    ),
    "Detection": (
        ("positive", "alert", (), ("alert", "no-alert")),
        ("negative", "no-alert", (), ("alert", "no-alert")),
        ("benign-near-miss", "no-alert", (), ("alert", "no-alert")),
    ),
    "Triage": (
        (
            "context",
            "evidence-owner-reason",
            ("evidence-only",),
            ("evidence-owner-reason", "evidence-only", "no-context"),
        ),
    ),
    "Response": (
        ("decision", "hold-with-owner", (), ("hold-with-owner", "no-decision")),
    ),
}
# Independent authored teaching roles, not generated from evaluator output.
SCENARIO_ROLES = (
    ("Atomic", ("Prevention",), ("Passed",)),
    ("Atomic", ("Telemetry",), ("Failed",)),
    ("Atomic", ("Detection",), ("Failed",)),
    ("Atomic", ("Triage",), ("Partial",)),
    ("Atomic", ("Response",), ("Stopped",)),
    ("Atomic", ("Detection",), ("Indeterminate",)),
    ("Atomic", ("Prevention",), ("Failed",)),
    ("End-to-End", LAYERS, ("Passed",) * 5),
    ("Atomic", ("Telemetry",), ("Partial",)),
    ("Atomic", ("Detection",), ("Passed",)),
)


# The ten reviewed remedy/acceptance pairs are authored teaching content.
# Updating generated digests alone must not homogenize or swap their meaning.
# Deliberate editorial revisions require reviewing this contract as well.
IMPROVEMENT_CONTENT = (
    (  # SCN-CV21-001
        "blockedとallowedの対比条件を保持し、防止の問いを変えず再評価する計画。",
        "対象・版を固定したscope-outcomeの期待値blockedと反証allowedを保持する。監査到達は別に評価する。",
    ),
    (  # SCN-CV21-002
        "生成記録からConsumerまでの配送失敗箇所と必要channelを供給資料上で照合する計画。実Logは追加収集しない。",
        "produced-and-confirmed-lossの根拠を保持し、新供給版でsignal-coverageがall-requiredかを比較する。",
    ),
    (  # SCN-CV21-003
        "Positiveの入力条件と供給Rule出力の差を切り分け、正常とNear-missを残して再比較する計画。実Ruleは変更しない。",
        "RT-CV21-003でpositive=alert、negativeとbenign-near-miss=no-alertを同一対象・Batch・入力条件で比較する。",
    ),
    (  # SCN-CV21-004
        "不足するOwnerと理由を明示した供給Triage記録を作る計画。実担当への通知は行わない。",
        "context=evidence-owner-reasonを根拠IDと照合し、evidence-onlyという旧Partialを残す。",
    ),
    (  # SCN-CV21-005
        "必要な権限根拠と判断主体を読解資料上で確認する計画。根拠がない間はStoppedを維持し、実許可を推定しない。",
        "供給権限の不足と停止理由を記録し、後続の比較には別途根拠を必要とする。実行権限falseは変えない。",
    ),
    (  # SCN-CV21-006
        "不足するPositive fixtureの必要Fieldと比較条件を定義し直す計画。欠測を成功へ書き換えず、実Dataは使わない。",
        "Positive・Negative・Benign-near-missの入力有無を区別し、足りない間はIndeterminateとNext actionを保持する。",
    ),
    (  # SCN-CV21-007
        "未承認scopeをallowedとした供給条件とControl目的の差を調べる計画。実設定は変更しない。",
        "同じ問いと対象版でblockedとallowedを比較し、元のFailedを保持する。実有効性へ一般化しない。",
    ),
    (  # SCN-CV21-008
        "五層のID・Trace・時刻・比較条件を再評価時にもそろえる計画。別系列の局所成功を寄せ集めない。",
        "全五層の供給根拠を独立に照合し、どの層の不足も総合Passedで隠さない。",
    ),
    (  # SCN-CV21-009
        "Primary到達とSecondary不足を分け、必要channelをそろえる供給検証案を作る。実Collectorは操作しない。",
        "primary-onlyという観測Partialを保持し、all-requiredへ変わったと主張する場合は新しい供給根拠を比較する。",
    ),
    (  # SCN-CV21-010
        "供給新版の正常・Near-miss対比を継続し、入力Schemaや期待値の変更時に再評価する計画。実Deployは行わない。",
        "旧003のFailed、新010の三条件一致と版の差を保持し、追加範囲や実検知率は未評価とする。",
    ),
)


def require(condition, message):
    if not condition:
        raise ValueError("CV21: " + message)


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


def strict(raw):
    return json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=_reject_duplicate_keys,
        parse_constant=_reject_constant,
    )


def instant(value):
    """Only the authored UTC seconds format; no inferred timezone or live clock."""
    require(isinstance(value, str) and len(value) == 20, "UTC seconds format")
    result = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    require(
        2000 <= result.year <= 2099 and result.strftime("%Y-%m-%dT%H:%M:%SZ") == value,
        "canonical UTC seconds",
    )
    return result


def read_regular(root, relative):
    """Bounded fixed inputs on Linux/WSL2; not a hostile-rename sandbox."""
    require(relative in INPUTS and not root.is_symlink(), "fixed input/root")
    root = root.resolve(strict=True)
    path = root
    for part in PurePosixPath(relative).parts:
        path /= part
        require(not path.is_symlink(), "symlink input/ancestor")
    require(path.resolve(strict=True).is_relative_to(root), "input containment")
    require(
        all(hasattr(os, key) for key in ("O_NOFOLLOW", "O_NONBLOCK")),
        "Linux/WSL2 flags",
    )
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        require(
            stat.S_ISREG(info.st_mode) and 0 < info.st_size <= 1024 * 1024,
            "bounded regular input",
        )
        raw = stream.read(1024 * 1024 + 1)
    require(len(raw) <= 1024 * 1024, "input size")
    return raw


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
        groups = [(key, value)]
        if key in ("controls", "scenarios"):
            groups = [(row["id"], row) for row in value]
        for title, group in groups:
            yield (
                title,
                [
                    (
                        "/".join(path) or title,
                        value
                        if isinstance(value, str)
                        else json.dumps(value, ensure_ascii=False),
                    )
                    for path, value in leaves(group)
                ],
            )


def evaluate(scenario):
    """Compare only supplied premises, preserving every unknown criterion.

    Foreign scope/trace/revision and malformed premises are rejected. A well-
    formed but late or absent input remains Indeterminate, never Partial.
    """
    kind, layers = scenario["type"], scenario["layers"]
    require(kind in ("Atomic", "End-to-End"), "Scenario type")
    require(
        layers and layers == [layer for layer in LAYERS if layer in layers],
        "layer inventory/order",
    )
    require(
        (kind == "Atomic" and len(layers) == 1)
        or (kind == "End-to-End" and tuple(layers) == LAYERS),
        "type/layer scope",
    )
    start, end, cutoff, analysis = (
        instant(scenario[k])
        for k in ("windowStart", "windowEnd", "cutoff", "analysisAt")
    )
    require(start < end <= cutoff <= analysis, "window/cutoff/analysis")
    require(type(scenario["suppliedAuthority"]) is bool, "supplied authority type")
    reason = scenario["stopReason"]
    require(reason in (None, "authority-gap", "unexpected-input"), "stop reason")
    require(
        scenario["suppliedAuthority"] or reason == "authority-gap", "authority stop"
    )
    require(
        reason != "authority-gap" or not scenario["suppliedAuthority"],
        "authority reason",
    )
    require(
        type(scenario["stepsAfterStop"]) is int and scenario["stepsAfterStop"] == 0,
        "no continuation",
    )
    require(scenario["mode"] == "supplied-record-comparison", "non-execution mode")
    observations = scenario["observations"]
    require(len(observations) == len(layers), "one observation per selected layer")
    require(
        len({o["id"] for o in observations}) == len(observations), "unique evidence"
    )
    output, previous_time, previous_available = [], None, None
    for index, (layer, observation) in enumerate(zip(layers, observations), 1):
        p = observation["payload"]
        require(observation["payloadSha256"] == digest(p), "payload representation")
        for key in (
            "subjectId",
            "subjectRevision",
            "traceId",
            "batchId",
            "controlRevision",
        ):
            require(p[key] == scenario[key], "evidence binding " + key)
        require(
            p["scenarioId"] == scenario["id"] and p["layer"] == layer,
            "scenario/layer evidence binding",
        )
        number = LAYERS.index(layer) + 1
        require(p["controlId"] == f"CTL-CV21-{number:03}", "Control/layer role")
        require(type(p["step"]) is int and p["step"] == index, "supplied step order")
        recorded, available = instant(p["recordedAt"]), instant(p["availableAt"])
        require(
            start <= recorded <= end and recorded <= available,
            "supplied record chronology",
        )
        require(
            previous_time is None or previous_time < recorded,
            "same-trace supplied order",
        )
        previous_time = recorded
        # A batch receipt can make consecutive layers available together.
        # This finite supplied chain cannot reverse availability order;
        # it is not a claim about every real-world telemetry pipeline.
        require(
            previous_available is None or previous_available <= available,
            "same-trace supplied availability order",
        )
        previous_available = available
        spec = CRITERIA[layer]
        keys = {row[0] for row in spec}
        require(
            set(p["values"]) == set(p["present"]) == keys, "criterion field inventory"
        )
        require(
            p["inputBasis"]
            in (
                "complete-supplied-input",
                "fixture-missing",
                "authority-not-supplied",
                "stopped-not-compared",
            ),
            "input basis",
        )
        require(
            p["transportBasis"]
            in (
                "not-a-transport-claim",
                "produced-and-confirmed-loss",
                "primary-present-secondary-missing",
            ),
            "transport basis",
        )
        if layer == "Telemetry":
            expected_basis = {
                "missing-confirmed": "produced-and-confirmed-loss",
                "primary-only": "primary-present-secondary-missing",
            }.get(p["values"]["signal-coverage"], "not-a-transport-claim")
            require(p["transportBasis"] == expected_basis, "transport claim evidence")
        else:
            require(
                p["transportBasis"] == "not-a-transport-claim",
                "no foreign transport claim",
            )
        missing = []
        for field in keys:
            present, actual = p["present"][field], p["values"][field]
            require(
                type(present) is bool and present == (actual is not None),
                "presence/value",
            )
            if not present:
                missing.append(field)
        require(
            (not missing and p["inputBasis"] == "complete-supplied-input")
            or (
                missing
                and p["inputBasis"]
                == (
                    "authority-not-supplied"
                    if reason == "authority-gap"
                    else "stopped-not-compared"
                    if reason
                    else "fixture-missing"
                )
            ),
            "missing input basis",
        )
        if reason:
            require(len(missing) == len(keys), "no observed execution after stop")
        results, classes, gaps = [], [], []
        for j, (field, wanted, partial, allowed) in enumerate(spec, 1):
            actual = p["values"][field]
            require(
                actual is None or (isinstance(actual, str) and actual in allowed),
                "finite actual value",
            )
            cid, gap = f"CRIT-CV21-{number:02}-{j:02}", None
            if reason:
                result, failure, gap = (
                    "Stopped",
                    "Authority" if reason == "authority-gap" else "Test design",
                    reason,
                )
            elif available > cutoff or actual is None:
                result, failure = "Indeterminate", "Test design"
                gap = "after-cutoff" if available > cutoff else "missing-input"
            elif actual == wanted:
                result, failure = "Passed", None
            elif actual in partial:
                result, failure, gap = (
                    "Partial",
                    MISMATCH_CLASS[layer],
                    "observed-partial",
                )
            else:
                result, failure, gap = (
                    "Failed",
                    MISMATCH_CLASS[layer],
                    "observed-mismatch",
                )
            results.append(
                {
                    "id": cid,
                    "result": result,
                    "evidenceId": observation["id"]
                    if not reason and available <= cutoff and actual is not None
                    else None,
                    "gapCode": gap,
                }
            )
            if failure and failure not in classes:
                classes.append(failure)
            if gap:
                gaps.append({"criterionId": cid, "reason": gap})
        statuses = {r["result"] for r in results}
        aggregate = next(
            s
            for s in ("Stopped", "Failed", "Indeterminate", "Partial", "Passed")
            if s in statuses
        )
        output.append(
            {
                "layer": layer,
                "result": aggregate,
                "failureClasses": [f for f in FAILURES if f in classes],
                "criteria": results,
                "gaps": gaps,
            }
        )
    return output


def summary(scenario):
    return [
        {k: row[k] for k in ("layer", "result", "failureClasses")}
        for row in evaluate(scenario)
    ]


def validate_semantics(data):
    require(data["schemaVersion"] == VERSION, "data version")
    record = data["record"]
    require(record["asOf"] == "2026-09-25T00:00:00Z", "authored asOf")
    require(
        (
            record["id"],
            record["caseId"],
            record["parentCaseId"],
            record["relation"],
            record["artifactId"],
        )
        == (
            "CVP-2026-021-001",
            "CASE-CV-2026-001",
            "CASE-DET-2026-001",
            "refines",
            "ART-27",
        ),
        "plan/case/artifact ownership",
    )
    require(
        record["sourceIds"] == list(SOURCES)
        and record["authoring"] == "synthetic-authored-not-measured",
        "source/authorship",
    )
    for key in (
        "actualOperations",
        "actualCollections",
        "actualNotifications",
        "actualDeployments",
        "actualIncidentDeclarations",
    ):
        require(type(record[key]) is int and record[key] == 0, "no actual activity")
    require(
        data["synthetic"] is True
        and data["readOnly"] is True
        and data["networkRequired"] is False
        and data["executionAuthorized"] is False,
        "read-only safety",
    )
    roles = data["roles"]
    require(
        len(set(roles.values())) == 3
        and all(v.startswith("SYN-CV-") for v in roles.values()),
        "separate synthetic roles",
    )
    require(len(data["controls"]) == 5, "five control objectives")
    control_owners = (
        "SYN-CV-CONTROL-OWNER",
        "SYN-CV-TELEMETRY-OWNER",
        "SYN-CV-DETECTION-OWNER",
        "SYN-CV-TRIAGE-OWNER",
        "SYN-CV-RESPONSE-OWNER",
    )
    for i, (control, layer) in enumerate(zip(data["controls"], LAYERS), 1):
        require(
            control["id"] == f"CTL-CV21-{i:03}"
            and control["objectiveId"] == f"OBJ-CV21-{i:03}"
            and control["layer"] == layer
            and control["owner"] == control_owners[i - 1],
            "control/objective/layer ownership",
        )
        expected = [
            {
                "id": f"CRIT-CV21-{i:02}-{j:02}",
                "field": field,
                "expected": value,
                "partialValues": list(partial),
            }
            for j, (field, value, partial, _) in enumerate(CRITERIA[layer], 1)
        ]
        require(control["criteria"] == expected, "authored criterion meaning")
    require(len(data["scenarios"]) == 10, "ten authored scenarios")
    # Missing test-design input (006) and cross-layer reassessment (008)
    # belong to the coordinator; each other proposal belongs to its Control.
    action_owner_layers = (0, 1, 2, 3, 4, None, 0, None, 1, 2)
    all_evidence, actions = [], []
    for n, (scenario, role) in enumerate(zip(data["scenarios"], SCENARIO_ROLES), 1):
        require(
            scenario["id"] == f"SCN-CV21-{n:03}"
            and scenario["traceId"] == f"TRACE-CV21-{n:03}",
            "scenario identity",
        )
        require(
            scenario["subjectId"] == "SYNTH-CV21-001"
            and scenario["subjectRevision"] == "REV-CV21-001",
            "new subject scope",
        )
        require(
            (scenario["type"], tuple(scenario["layers"])) == role[:2],
            "authored scenario role",
        )
        require(
            [scenario[k] for k in ("windowStart", "windowEnd", "cutoff", "analysisAt")]
            == [
                "2026-09-01T09:00:00Z",
                "2026-09-01T09:10:00Z",
                "2026-09-01T09:11:00Z",
                "2026-09-01T09:12:00Z",
            ],
            "authored time basis",
        )
        actual = summary(scenario)
        require(
            tuple(r["result"] for r in actual) == role[2]
            and actual == scenario["expectedLayers"],
            "literal teaching outcome",
        )
        require(
            scenario["suppliedAuthority"] is (n != 5), "authored authority contrast"
        )
        require(
            scenario["stopReason"] == ("authority-gap" if n == 5 else None),
            "authored stop role",
        )
        require(
            scenario["controlRevision"]
            == ("CTLREV-CV21-002" if n == 10 else "CTLREV-CV21-001"),
            "authored revision",
        )
        batch = (
            "BATCH-CV21-PAIR"
            if n in (1, 2)
            else "BATCH-CV21-DETECTION"
            if n in (3, 10)
            else f"BATCH-CV21-{n:03}"
        )
        require(scenario["batchId"] == batch, "paired comparison batch")
        for j, o in enumerate(scenario["observations"], 1):
            require(o["id"] == f"EVD-CV21-{n:03}-{j:02}", "authored evidence identity")
            all_evidence.append(o["id"])
        # The detection counterexample must remain the Positive, not a swapped normal case.
        if n in (3, 6, 10):
            values = scenario["observations"][0]["payload"]["values"]
            require(
                values
                == {
                    "positive": {3: "no-alert", 6: None, 10: "alert"}[n],
                    "negative": "no-alert",
                    "benign-near-miss": "no-alert",
                },
                "normal/positive role preservation",
            )
        gap, action = scenario["gap"], scenario["improvement"]
        require(
            gap["id"] == f"GAP-CV21-{n:03}"
            and gap["affectedLayers"]
            == [r["layer"] for r in actual if r["result"] != "Passed"],
            "gap/result association",
        )
        require(
            action["id"] == gap["nextActionId"] == f"ACT-CV21-{n:03}", "Gap/Next action"
        )
        require(
            (action["action"], action["acceptance"]) == IMPROVEMENT_CONTENT[n - 1],
            "authored scenario improvement content",
        )
        owner_layer = action_owner_layers[n - 1]
        action_owner = (
            roles["validationOwner"]
            if owner_layer is None
            else control_owners[owner_layer]
        )
        require(
            action["owner"] == action_owner
            and action["status"] == "proposed-not-executed",
            "proposed action owner",
        )
        require(instant(action["dueAt"]) > instant(record["asOf"]), "action due date")
        require(
            action["retestId"] == f"RT-CV21-{n:03}"
            and action["reassessmentId"] == f"REA-CV21-{n:03}",
            "retest/reassessment ID",
        )
        actions.append(action["id"])
    require(len(set(all_evidence)) == len(all_evidence), "global evidence ownership")
    retest = data["retest"]
    require(
        retest
        == {
            "id": "RT-CV21-003",
            "beforeScenarioId": "SCN-CV21-003",
            "afterScenarioId": "SCN-CV21-010",
            "changedField": "controlRevision",
            "beforeRevision": "CTLREV-CV21-001",
            "afterRevision": "CTLREV-CV21-002",
            "sourceActionId": "ACT-CV21-003",
            "result": "recorded-comparison-only",
            "beforeRetained": True,
            "actualChangeExecuted": False,
            "limitation": retest["limitation"],
        },
        "bounded retest identity/non-execution",
    )
    before, after = data["scenarios"][2], data["scenarios"][9]
    for key in (
        "type",
        "layers",
        "subjectId",
        "subjectRevision",
        "batchId",
        "windowStart",
        "windowEnd",
        "cutoff",
        "analysisAt",
        "mode",
        "suppliedAuthority",
    ):
        require(before[key] == after[key], "retest comparability " + key)
    for old_observation, new_observation in zip(
        before["observations"], after["observations"]
    ):
        for key in ("recordedAt", "availableAt"):
            require(
                old_observation["payload"][key] == new_observation["payload"][key],
                "retest observation timing " + key,
            )
    h = data["handoff"]
    require(
        h["id"] == "HOF-CV21-22"
        and type(h["targetChapter"]) is int
        and h["targetChapter"] == 22
        and h["sourcePlanId"] == record["id"]
        and h["actionIds"] == actions,
        "handoff traceability",
    )
    require(
        h["status"] == "planned-not-delivered"
        and h["receiptId"] is None
        and h["executionAuthorized"] is False
        and h["owner"] == roles["validationOwner"],
        "handoff non-receipt",
    )
    require(instant(h["dueAt"]) > instant(record["asOf"]), "handoff due date")
    boundary = data["authorityBoundary"]
    require(
        boundary["parentAuthorityId"] == "AUTH-CASE-2026-001"
        and boundary["parentExpiresAt"] == "2026-08-19T09:00:00Z"
        and boundary["parentRoeId"] == "ROE-2026-009"
        and boundary["parentRoeStatus"] == "Draft"
        and type(boundary["parentRoeVersion"]) is int
        and boundary["parentRoeVersion"] == 1
        and boundary["parentLabId"] == "LABPLAN-2026-001"
        and boundary["parentLabRuntimeExecuted"] is False
        and boundary["parentExecutionAuthorized"] is False,
        "parent authority remains expired/Draft",
    )
    require(
        data["threat"]["attackTechniqueId"] == "T1098"
        and data["threat"]["attackVersion"] == "19.2"
        and data["threat"]["coverageProof"] is False
        and data["threat"]["actorAttribution"] == "not-assessed",
        "mapping is not effectiveness or attribution",
    )
    safety = data["safety"]
    require(
        safety["mode"] == "offline-record-only"
        and safety["cleanupDisposition"] == "reading-copy-plan-only"
        and safety["residualDisposition"] == "not-measured",
        "cleanup/residual boundary",
    )


def validate_model(data, schema, contract):
    validate_schema_instance(data, schema)
    validate_semantics(data)
    errors = []
    for path, value in leaves(data):
        if isinstance(value, str):
            if not value.strip() or len(value) > 2000:
                errors.append("CV21 bounded nonempty field: " + "/".join(path))
            for finding in (
                *scan_action_text(value, location="/".join(path)),
                *scan_host_policy(value, location="/".join(path)),
            ):
                errors.append("CV21 " + "/".join(path) + ": " + finding.category)
    if {k: digest(v) for k, v in data.items()} != contract["authoredInputs"]:
        errors.append("CV21 authored input snapshot")
    return errors
