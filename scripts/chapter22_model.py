"""Chapter22 finite supplied metrics/backlog semantics, not a production KPI engine.

Layer A only: educational identities, arithmetic, evidence bindings and decisions.
Publication syntax and action/host policy remain owned by the shared modules.
"""

from datetime import datetime, timezone
from fractions import Fraction
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
DATA = "cases/fixtures/ch22-measurement-improvement.json"
SCHEMA = "schemas/ch22-measurement-improvement.schema.json"
CONTRACT = "tests/fixtures/chapter22/publication-contract.json"
CORPUS = "tests/fixtures/chapter22/comparison-corpus.json"
DOCUMENTS = (
    "manuscript/22-measurement-improvement.md",
    "templates/security-improvement-backlog.md",
    "cases/ch22-improvement-backlog-example.md",
    "references/ch22-source-review-2026-09-26.md",
)
SOURCES = (
    "SRC-NIST-MEASURE-001",
    "SRC-NIST-MEASURE-002",
    "SRC-CSF-001",
    "SRC-IR-001",
    "SRC-KEV-001",
)
PARENTS = (
    "WRITING_GUIDE.md",
    "SOURCE_POLICY.md",
    "SAFETY_SCOPE.md",
    "CROSS_BOOK_MAP.md",
    "manuscript/07-vulnerability-prioritization.md",
    "cases/fixtures/ch07-vulnerability-prioritization.json",
    "cases/fixtures/ch07-source-snapshot.json",
    "cases/fixtures/ch14-minimal-impact-validation.json",
    "manuscript/15-findings-retest-risk.md",
    "cases/fixtures/ch15-findings-retest-risk.json",
    "manuscript/16-telemetry-evidence-readiness.md",
    "cases/fixtures/ch16-telemetry-coverage.json",
    "manuscript/17-detection-engineering.md",
    "cases/fixtures/ch17-detection-engineering-fixture.json",
    "manuscript/18-threat-hunting.md",
    "cases/fixtures/ch18-threat-hunting.json",
    "manuscript/19-incident-response.md",
    "cases/fixtures/ch19-incident-response.json",
    "manuscript/20-dfir-timeline-causality.md",
    "cases/fixtures/ch20-dfir-timeline-causality.json",
    "manuscript/21-purple-team-validation.md",
    "cases/fixtures/ch21-control-validation.json",
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
    "book-config.json",
)
STATUSES = (
    "Proposed",
    "Approved",
    "In progress",
    "Blocked",
    "Verified",
    "Accepted",
    "Retired",
)


def require(condition, message):
    if not condition:
        raise ValueError("IMP22: " + message)


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
        ).encode("utf-8")
    ).hexdigest()


def instant(value):
    require(isinstance(value, str) and len(value) == 20, "UTC seconds format")
    result = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    require(
        2000 <= result.year <= 2099 and result.strftime("%Y-%m-%dT%H:%M:%SZ") == value,
        "canonical UTC seconds",
    )
    return result


def read_regular(root, relative):
    """Fixed bounded publication inputs; not a hostile concurrent-rename sandbox."""
    require(relative in INPUTS and not root.is_symlink(), "fixed input/root")
    root = root.resolve(strict=True)
    path = root
    for part in PurePosixPath(relative).parts:
        path /= part
        require(not path.is_symlink(), "symlink input/ancestor")
    require(path.resolve(strict=True).is_relative_to(root), "input containment")
    require(
        all(hasattr(os, k) for k in ("O_NOFOLLOW", "O_NONBLOCK")), "Linux/WSL2 flags"
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
        if key in ("metrics", "items"):
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


def rational(value):
    return [value.numerator, value.denominator]


def unique_ids(value, label):
    require(isinstance(value, list) and len(value) <= 100, label + " bounded list")
    require(
        all(isinstance(x, str) and x and len(x) <= 100 for x in value), label + " IDs"
    )
    require(len(value) == len(set(value)), label + " duplicates")
    return set(value)


def measure(formula, population, selected, samples, missing):
    """Three finite authored calculation forms; no runtime data collection.

    All membership facts are supplied. A known false result is not missing data.
    Missing/zero-denominator results are explicit unknowns, never zero percent.
    """
    require(formula in ("count", "proportion", "duration-distribution"), "formula")
    members = unique_ids(population, "population")
    numerator = unique_ids(selected, "selected")
    absent = unique_ids(missing, "missing")
    require(numerator <= members and absent <= members, "population membership")
    require(not numerator & absent, "selected/missing overlap")
    require(isinstance(samples, list) and len(samples) <= 100, "bounded samples")
    require(
        all(type(v) is int and 0 <= v <= 1000000 for v in samples), "integer samples"
    )
    if formula == "duration-distribution":
        require(not selected, "duration is not a selected-set count")
        require(
            len(samples) + len(missing) == len(population),
            "one sample per known member",
        )
    else:
        require(not samples, "count/proportion have no duration samples")
    if missing:
        return {"unknown": "missing-input"}
    if formula == "count":
        return {"count": len(selected)}
    if not population:
        return {"unknown": "zero-denominator"}
    if formula == "proportion":
        return {
            "numerator": len(selected),
            "denominator": len(population),
            "ratio": rational(Fraction(len(selected), len(population))),
        }
    ordered = sorted(samples)
    n = len(ordered)
    middle = (
        Fraction(ordered[n // 2])
        if n % 2
        else Fraction(ordered[n // 2 - 1] + ordered[n // 2], 2)
    )
    rank = (9 * n + 9) // 10
    return {
        "n": n,
        "mean": rational(Fraction(sum(ordered), n)),
        "median": rational(middle),
        "p90": ordered[rank - 1],
        "percentileMethod": "nearest-rank",
    }


def metric_result(metric, name):
    snapshot = metric[name]
    return measure(
        metric["formula"],
        metric["populationMembers"],
        snapshot["selectedMembers"],
        snapshot["samples"],
        snapshot["missingMembers"],
    )


def same(actual, expected, label):
    """Exact typed JSON equality: Python's True == 1 is not a semantic match."""
    require(digest(actual) == digest(expected), label)


def numbered(prefix, count):
    return [f"{prefix}-{i:03}" for i in range(1, count + 1)]


# Finite authored inventories and roles, not inferred from a mutable snapshot.
# Deliberate teaching revisions must review these contracts, not only digests.
METRIC_ROLES = (
    ("Process", "count", "件", "RULE-IMP22", 8, 4, 8),
    ("Leading", "proportion", "割合", "CRIT-IMP22", 5, 2, 2),
    ("Leading", "proportion", "割合", "HYP-IMP22", 10, 9, 9),
    ("Outcome", "proportion", "割合", "HYP-IMP22", 10, 2, 2),
    ("Process", "duration-distribution", "分", "REC-IMP22", 5, 0, 0),
    ("Quality", "proportion", "割合", "REC-IMP22", 5, 5, 2),
    ("Quality", "proportion", "割合", "HUNT-IMP22", 10, 4, 1),
    ("Outcome", "proportion", "割合", None, 3, 2, 3),
    ("Leading", "proportion", "割合", "AUTHORITY-IMP22", 1, 0, 0),
    ("Process", "count", "件", "ACTIVITY-IMP22", 8, 4, 8),
)
ITEM_ROLES = (
    ("Proposed", "Detection", (1, 2), "plan-proposed"),
    ("Approved", "Detection", (3, 4), "plan-approved"),
    ("In progress", "Evidence", (5, 6), "record-draft-in-progress"),
    ("Verified", "Telemetry", (7,), "supplied-comparison-complete"),
    ("Verified", "Detection", (8,), "supplied-comparison-complete"),
    ("Blocked", "Authority", (9,), "blocked"),
    ("Accepted", "Evidence", (2,), "risk-decision-recorded"),
    ("Retired", "Evidence", (10,), "metric-retired-in-record"),
)
WINDOW = ("2026-09-01T09:00:00Z", "2026-09-01T09:10:00Z", "2026-09-01T09:11:00Z")
AS_OF = "2026-09-26T00:00:00Z"
DUE = "2026-09-30T00:00:00Z"
REFINES = ["CASE-2026-001", "CASE-DET-2026-001"]


# Reviewed editorial roles, transcribed from the first authored draft.
# Changing only a publication digest cannot homogenize these explanations.
METRIC_TEXT_FIELDS = (
    "decisionPurpose",
    "definition",
    "target",
    "exclusionReason",
    "qualityCriterion",
    "confidence",
    "limitation",
    "retirementTrigger",
)
METRIC_CONTENT = (
    (
        "重要行動の検証不足に対し、Rule件数だけの増加を区別する。",
        "供給されたRule inventoryのMember数。実製品に導入されたRule数ではない。",
        "件数自体の増加を改善目標にしない。",
        "この著者定義の母集団外は未評価。改善のための事後除外はしない。",
        "供給入力の有無と既知の不一致を区別し、根拠不足をゼロへ置換しない。",
        "この供給値の計算は再現可能。実効果の確信度は未評価。",
        "実測、実組織の分布、因果効果、未選択範囲は評価していない。",
        "判断目的の消失、重複、Gaming、Dataの継続取得不能、より適切な代替の出現。",
    ),
    (
        "重要な行動の検証範囲を増やす計画を比較する。",
        "著者が選んだ五つの重要行動のうち、供給比較条件を満たしたMemberの割合。",
        "未検証三行動の必要Evidenceを定める。全攻撃行動への比率とはしない。",
        "この著者定義の母集団外は未評価。改善のための事後除外はしない。",
        "供給入力の有無と既知の不一致を区別し、根拠不足をゼロへ置換しない。",
        "この供給値の計算は再現可能。実効果の確信度は未評価。",
        "実測、実組織の分布、因果効果、未選択範囲は評価していない。",
        "判断目的の消失、重複、Gaming、Dataの継続取得不能、より適切な代替の出現。",
    ),
    (
        "対応表の広さと検証不足を分離する。",
        "同じ十仮説のうち、対応表に記載のあるMemberの割合。有効性の測定ではない。",
        "対応表から検証済み割合へ自動変換しない。",
        "この著者定義の母集団外は未評価。改善のための事後除外はしない。",
        "供給入力の有無と既知の不一致を区別し、根拠不足をゼロへ置換しない。",
        "この供給値の計算は再現可能。実効果の確信度は未評価。",
        "実測、実組織の分布、因果効果、未選択範囲は評価していない。",
        "判断目的の消失、重複、Gaming、Dataの継続取得不能、より適切な代替の出現。",
    ),
    (
        "同じ仮説の供給検証がどこまで完了したかを問う。",
        "十仮説のうち、供給された正常・異常対比の必須条件を満たしたMemberの割合。",
        "未検証八仮説を別に保持する。実検知率とは呼ばない。",
        "この著者定義の母集団外は未評価。改善のための事後除外はしない。",
        "供給入力の有無と既知の不一致を区別し、根拠不足をゼロへ置換しない。",
        "この供給値の計算は再現可能。実効果の確信度は未評価。",
        "実測、実組織の分布、因果効果、未選択範囲は評価していない。",
        "判断目的の消失、重複、Gaming、Dataの継続取得不能、より適切な代替の出現。",
    ),
    (
        "判断時間の短縮とEvidence品質の逆行を併せて判断する。",
        "供給された判断開始から判断記録までの五つの時間。個人の作業速度を測らない。",
        "品質と安全を保たない時間短縮を合格にしない。",
        "この著者定義の母集団外は未評価。改善のための事後除外はしない。",
        "供給入力の有無と既知の不一致を区別し、根拠不足をゼロへ置換しない。",
        "この供給値の計算は再現可能。実効果の確信度は未評価。",
        "実測、実組織の分布、因果効果、未選択範囲は評価していない。",
        "判断目的の消失、重複、Gaming、Dataの継続取得不能、より適切な代替の出現。",
    ),
    (
        "判断に必要なEvidenceを失っていないかを確認する。",
        "同じ五判断のうち、必須Evidenceが充足していると供給記録に明示されたMemberの割合。",
        "三記録の不足を隠さず、品質を保つ受入条件を作る。",
        "この著者定義の母集団外は未評価。改善のための事後除外はしない。",
        "供給入力の有無と既知の不一致を区別し、根拠不足をゼロへ置換しない。",
        "この供給値の計算は再現可能。実効果の確信度は未評価。",
        "実測、実組織の分布、因果効果、未選択範囲は評価していない。",
        "判断目的の消失、重複、Gaming、Dataの継続取得不能、より適切な代替の出現。",
    ),
    (
        "Telemetry条件の違いが供給Huntの結論保留とどう関係するかを比較する。",
        "同じ十件の供給Huntのうち、Inconclusiveと記録されたMemberの割合。実侵害率ではない。",
        "供給比較のInconclusive減少だけを検証し、親Huntの結果を書き換えない。",
        "この著者定義の母集団外は未評価。改善のための事後除外はしない。",
        "供給入力の有無と既知の不一致を区別し、根拠不足をゼロへ置換しない。",
        "この供給値の計算は再現可能。実効果の確信度は未評価。",
        "実測、実組織の分布、因果効果、未選択範囲は評価していない。",
        "判断目的の消失、重複、Gaming、Dataの継続取得不能、より適切な代替の出現。",
    ),
    (
        "親21の同一条件の供給Retestを、限定した改善判断へ接続する。",
        "SCN-CV21-003と010で、三つの供給検知出力がControl期待値に一致する割合。",
        "旧Failedと正常・Near-missを保持した三条件一致。実RuleのDeployは未実施。",
        "この著者定義の母集団外は未評価。改善のための事後除外はしない。",
        "供給入力の有無と既知の不一致を区別し、根拠不足をゼロへ置換しない。",
        "この供給値の計算は再現可能。実効果の確信度は未評価。",
        "実測、実組織の分布、因果効果、未選択範囲は評価していない。",
        "判断目的の消失、重複、Gaming、Dataの継続取得不能、より適切な代替の出現。",
    ),
    (
        "権限根拠がない条件を、他の数値で補わず停止する。",
        "教材内の必要な権限根拠の供給有無。実権限を判定したり付与したりしない。",
        "根拠がない間はBlocked。実操作を行わない。",
        "この著者定義の母集団外は未評価。改善のための事後除外はしない。",
        "供給入力の有無と既知の不一致を区別し、根拠不足をゼロへ置換しない。",
        "この供給値の計算は再現可能。実効果の確信度は未評価。",
        "実測、実組織の分布、因果効果、未選択範囲は評価していない。",
        "判断目的の消失、重複、Gaming、Dataの継続取得不能、より適切な代替の出現。",
    ),
    (
        "判断目的を失った活動件数の指標を廃止する理由を記録する。",
        "供給された活動記録の件数。数を増やすだけの誘因を点検する旧指標。",
        "指標をRetiredとし、重要行動とQualityの問いへ戻る。",
        "この著者定義の母集団外は未評価。改善のための事後除外はしない。",
        "供給入力の有無と既知の不一致を区別し、根拠不足をゼロへ置換しない。",
        "この供給値の計算は再現可能。実効果の確信度は未評価。",
        "実測、実組織の分布、因果効果、未選択範囲は評価していない。",
        "判断目的の消失、重複、Gaming、Dataの継続取得不能、より適切な代替の出現。",
    ),
)
ITEM_CONTENT = (
    (
        "重要行動の未検証が残り、Rule追加を先に成功と数えられない。",
        "五行動の母集団と三つの未検証条件を固定し、必要Evidenceを列挙する案。",
        "Rule件数とは別に各行動の正常・異常比較と未検証理由を示す。",
        "計画案だけ。検証は未実施。",
    ),
    (
        "対応表の9/10と供給検証の2/10の差を可視化する必要がある。",
        "対応付けだけの仮説を分け、正常系を伴う供給検証計画を比較する案。",
        "同じ十仮説でmappingと検証の集合を別々に追跡し、未検証八件を残す。",
        "供給計画の条件確認のみ。実操作は承認していない。",
    ),
    (
        "平均時間短縮と根拠充足の悪化が同時に起きている。",
        "必須Evidenceを失うWorkflowを供給資料上で見直す計画。実担当への通知は行わない。",
        "時間の三統計量と同じ五判断の品質を併記し、品質低下を時間目標で正当化しない。",
        "供給Workflowの検討用記録が作成途中。品質条件は未充足。",
    ),
    (
        "同じ供給Huntの条件差を比較し、結論保留が残る一件も追跡する。",
        "十件の供給HuntでTelemetry条件とInconclusiveの前後を比較する。実Collectorは操作しない。",
        "同じ十件で4/10と1/10を照合し、未確定一件と親Huntの未変更を保持する。",
        "供給Huntの前後照合記録がそろった。実Collectorや親Huntは未変更。",
    ),
    (
        "供給Rule版の差を正常・Near-miss対比を失わず再確認する。",
        "親21の003と010を方法参照として照合し、旧Failedと供給新版の一致を両方残す。",
        "同一対象・Batch・時間条件で三出力を比較し、2/3から3/3の限定差だけを支持する。",
        "親21の供給Retestを照合した記録だけ。親Actionを実施済みにしない。",
    ),
    (
        "権限根拠不足は、品質や件数の良さで補えない。",
        "必要な権限根拠と判断主体を資料上で明示する案。根拠不足の間は停止を保持する。",
        "供給不足をunknownとBlockedで残し、親の期限切れ権限やDraft RoEを実許可に変えない。",
        "供給権限根拠が不足し、後続の実操作は0。",
    ),
    (
        "未検証範囲の知識不足を、実Riskゼロとせず期限付きの供給判断へ残す。",
        "限定した供給計画の残存不確実性を、Risk ownerと期限付きで再評価する案。",
        "受容の範囲・理由・担当・期限・再評価を残す。実操作許可や検証成功にはしない。",
        "知識不足を残す供給判断のみ。修正や検証の完了ではない。",
    ),
    (
        "活動件数だけを増やす指標は現在の判断目的を失っている。",
        "旧活動件数の定義と値を保持して廃止し、重要行動と根拠品質の問いへ置き換える。",
        "旧値を削除せず、廃止理由とMET-IMP22-002/006への代替参照を残す。",
        "指標の役割終了を記録した。旧値と根拠は削除していない。",
    ),
)


def validate_metrics(metrics, as_of):
    same([m["id"] for m in metrics], numbered("MET-IMP22", 10), "metric order/identity")
    for i, (metric, role) in enumerate(zip(metrics, METRIC_ROLES, strict=True), 1):
        typ, formula, unit, prefix, count, before, after = role
        same(
            [metric[k] for k in ("type", "formula", "unit")],
            [typ, formula, unit],
            "metric type/formula/unit role",
        )
        members = (
            numbered(prefix, count)
            if prefix
            else ["positive", "negative", "benign-near-miss"]
        )
        same(
            metric["populationMembers"],
            members,
            "authored population; no denominator removal",
        )
        same(metric["populationId"], f"POP-IMP22-{i:03}", "population identity")
        same(metric["populationRevision"], "POP-REV-001", "population revision")
        same(
            metric["populationBasis"],
            "author-selected-finite-teaching-members-not-real-organization",
            "population provenance",
        )
        same(
            metric["reassessmentId"],
            f"REA-IMP22-{(1, 1, 2, 2, 3, 3, 4, 5, 6, 8)[i - 1]:03}",
            "metric reassessment identity",
        )
        same(
            [metric[k] for k in ("windowStart", "windowEnd", "cutoff")],
            list(WINDOW),
            "authored common observation window/cutoff",
        )
        start, end, cutoff = (
            instant(metric[k]) for k in ("windowStart", "windowEnd", "cutoff")
        )
        require(start < end <= cutoff <= as_of, "metric time ordering")
        same(
            [metric[k] for k in METRIC_TEXT_FIELDS],
            list(METRIC_CONTENT[i - 1]),
            "authored metric purpose/definition/target; digest refresh is not editorial approval",
        )
        for name, n, revision in (
            ("baseline", before, "INPUT-REV-001"),
            ("current", after, "INPUT-REV-002"),
        ):
            snap = metric[name]
            same(
                [snap[k] for k in ("id", "evidenceId", "dataSourceId")],
                [
                    f"SNAP-IMP22-{i:03}-{name}",
                    f"EVD-IMP22-M{i:03}-{name}",
                    f"SYNDS-IMP22-{i:03}",
                ],
                "snapshot/evidence/source identity",
            )
            same(
                [
                    snap[k]
                    for k in (
                        "origin",
                        "subjectId",
                        "subjectRevision",
                        "populationRevision",
                    )
                ],
                [
                    "authored-supplied-values-not-measured",
                    "SYNTH-IMP22-001",
                    revision,
                    "POP-REV-001",
                ],
                "snapshot provenance/subject/revisions",
            )
            same(
                [snap[k] for k in ("windowStart", "windowEnd")],
                list(WINDOW[:2]),
                "snapshot window binding",
            )
            same(snap["availableAt"], "2026-09-01T09:10:30Z", "authored availability")
            require(
                end <= instant(snap["availableAt"]) <= cutoff,
                "available evidence before cutoff",
            )
            selected = members[:n]
            if i == 8 and name == "baseline":
                selected = ["negative", "benign-near-miss"]
            samples = []
            if i == 5:
                samples = [4, 5, 6, 10, 25] if name == "baseline" else [1, 2, 3, 4, 15]
            same(
                snap["selectedMembers"], selected, "supplied membership by metric role"
            )
            same(snap["samples"], samples, "supplied duration samples in member order")
            same(
                snap["missingMembers"],
                members if i == 9 else [],
                "missing input is distinct from known evidence noncompliance",
            )
            same(
                snap["expectedResult"],
                metric_result(metric, name),
                "independently authored arithmetic result",
            )
    # These paired comparisons have the same denominator but distinct questions.
    for left, right in ((2, 3), (4, 5)):
        same(
            metrics[left]["populationMembers"],
            metrics[right]["populationMembers"],
            "paired comparison population",
        )


def validate_dependencies(items):
    graph = {
        item["id"]: unique_ids(item["dependencyIds"], "dependencies") for item in items
    }
    require(len(graph) == len(items), "duplicate item identity")
    for item, deps in graph.items():
        require(
            deps <= graph.keys() and item not in deps, "dependency reference/self-cycle"
        )
    done, visiting = set(), set()

    def visit(item):
        require(item not in visiting, "dependency cycle")
        if item in done:
            return
        visiting.add(item)
        for dependency in sorted(graph[item]):
            visit(dependency)
        visiting.remove(item)
        done.add(item)

    for item in graph:
        visit(item)


def validate_items(items, metrics, as_of):
    same(
        [item["id"] for item in items], numbered("BLI-IMP22", 8), "item order/identity"
    )
    validate_dependencies(items)
    by_id = {m["id"]: m for m in metrics}
    for i, (item, role) in enumerate(zip(items, ITEM_ROLES, strict=True), 1):
        status, debt, numbers, stage = role
        metric_ids = [f"MET-IMP22-{n:03}" for n in numbers]
        same(
            [item["status"], item["debt"], item["metricIds"]],
            [status, debt, metric_ids],
            "authored item role/status/debt/metrics",
        )
        same(item["caseId"], "CASE-IMP-2026-001", "item case")
        same(item["refines"], REFINES, "item refines method references")
        for key, prefix in (
            ("riskObjectiveId", "ROBJ"),
            ("findingId", "FND"),
            ("gapId", "GAP"),
            ("controlId", "CTL"),
        ):
            same(
                item[key],
                f"{prefix}-IMP22-{i:03}",
                "objective/finding/gap/control binding",
            )
        same(
            item["dependencyIds"],
            ["BLI-IMP22-001"] if i == 2 else [],
            "authored prerequisites",
        )
        priority, action = item["priority"], item["action"]
        same(
            priority["label"],
            "条件を先に確認" if i in (3, 6) else "供給案を比較",
            "priority role",
        )
        same(priority["automaticScore"], False, "no automatic risk score")
        same(
            [
                priority["reason"],
                action["proposal"],
                action["acceptance"],
                item["workRecord"]["note"],
            ],
            list(ITEM_CONTENT[i - 1]),
            "authored distinct priority/remedy/acceptance/progress meaning",
        )
        same(
            [
                action[k]
                for k in (
                    "id",
                    "owner",
                    "dueAt",
                    "executionAuthorized",
                    "actualExecuted",
                )
            ],
            [f"ACT-IMP22-{i:03}", f"SYN-IMP22-OWNER-{i:03}", DUE, False, False],
            "action identity/owner/due/no execution",
        )
        require(as_of < instant(action["dueAt"]), "action future due")
        evidence = [
            by_id[mid][name]["evidenceId"]
            for mid in metric_ids
            for name in ("baseline", "current")
        ]
        same(
            item["evidenceIds"],
            evidence,
            "item evidence must bind both snapshots of its metrics",
        )
        verification = item["verification"]
        verified = status == "Verified"
        same(
            [
                verification[k]
                for k in (
                    "id",
                    "evidenceId",
                    "itemId",
                    "metricIds",
                    "sourceEvidenceIds",
                )
            ],
            [
                f"VAL-IMP22-{i:03}" if verified else None,
                f"EVD-IMP22-V{i:03}" if verified else None,
                item["id"],
                metric_ids,
                evidence if verified else [],
            ],
            "validation/evidence binding",
        )
        same(
            [
                verification[k]
                for k in (
                    "subjectId",
                    "subjectRevision",
                    "windowStart",
                    "windowEnd",
                    "cutoff",
                )
            ],
            ["SYNTH-IMP22-001", "INPUT-REV-002", *WINDOW],
            "validation scope/revision/window/cutoff binding",
        )
        same(
            [
                verification[k]
                for k in ("recordedAt", "method", "result", "realEffectivenessVerified")
            ],
            [
                AS_OF if verified else None,
                "finite-supplied-comparison",
                "bounded-supplied-match" if verified else "not-verified",
                False,
            ],
            "bounded verification, not real effectiveness",
        )
        if verified:
            require(
                instant(WINDOW[2]) <= instant(verification["recordedAt"]) <= as_of,
                "verification uses available inputs, not future record",
            )
            require(
                all(
                    "unknown" not in metric_result(by_id[mid], name)
                    for mid in metric_ids
                    for name in ("baseline", "current")
                ),
                "verified needs complete evidence",
            )
        decision = item["decision"]
        same(
            decision,
            {
                "id": f"DEC-IMP22-{i:03}",
                "owner": "SYN-IMP22-DECISION-OWNER",
                "basis": priority["reason"],
                "recordedAt": AS_OF,
                "executionAuthorized": False,
            },
            "decision binding/basis/no authorization",
        )
        risk = item["riskJudgment"]
        same(
            risk["claim"],
            action["acceptance"],
            "bounded judgment must retain the distinct teaching conclusion",
        )
        same(
            [risk["realRiskReductionMeasured"], risk["riskZero"]],
            [False, False],
            "no real risk reduction or risk zero",
        )
        same(
            [item["residualRisk"][k] for k in ("id", "owner")],
            [f"RES-IMP22-{i:03}", "SYN-IMP22-RISK-OWNER"],
            "residual risk owner/identity",
        )
        reassessment = item["reassessment"]
        same(
            [reassessment[k] for k in ("id", "owner", "dueAt")],
            [f"REA-IMP22-{i:03}", action["owner"], DUE],
            "reassessment owner/due binding",
        )
        acceptance = item["acceptance"]
        present = status == "Accepted"
        same(
            [
                acceptance[k]
                for k in (
                    "present",
                    "id",
                    "owner",
                    "authorityReference",
                    "decidedAt",
                    "expiresAt",
                    "overridesExecutionAuthority",
                )
            ],
            [
                present,
                "ACC-IMP22-007" if present else None,
                "SYN-IMP22-RISK-OWNER" if present else None,
                "SYN-RISK-MANDATE-IMP22" if present else None,
                AS_OF if present else None,
                "2026-10-01T00:00:00Z" if present else None,
                False,
            ],
            "acceptance is a bounded risk decision, not execution authority",
        )
        same(
            acceptance["scope"],
            "この供給計画の未検証範囲に関する知識不足だけ。実事業Riskや実作業の許可ではない。"
            if present
            else None,
            "acceptance scope",
        )
        if present:
            require(
                instant(acceptance["decidedAt"])
                <= as_of
                < instant(acceptance["expiresAt"]),
                "unexpired acceptance",
            )
            require(
                as_of
                < instant(reassessment["dueAt"])
                <= instant(acceptance["expiresAt"]),
                "reassessment before acceptance expiry",
            )
        retirement = item["retirement"]
        retired = status == "Retired"
        same(
            retirement,
            {
                "present": retired,
                "reason": "活動件数だけの目標が判断目的を失い、Gamingを招く。旧記録を保持する。"
                if retired
                else None,
                "replacementMetricIds": ["MET-IMP22-002", "MET-IMP22-006"]
                if retired
                else [],
                "historyRetained": True,
            },
            "retirement retains old evidence and replacement purpose",
        )
        same(
            [item["workRecord"][k] for k in ("stage", "recordedAt", "actualOperation")],
            [stage, AS_OF, False],
            "progress is a record, not actual operation",
        )


def validate_semantics(data):
    same(
        [
            data[k]
            for k in (
                "schemaVersion",
                "synthetic",
                "readOnly",
                "networkRequired",
                "executionAuthorized",
            )
        ],
        [VERSION, True, True, False, False],
        "synthetic offline read-only boundary",
    )
    record = data["record"]
    same(
        [
            record[k]
            for k in ("id", "caseId", "artifactId", "asOf", "authoring", "sourceIds")
        ],
        [
            "SIB-2026-022-001",
            "CASE-IMP-2026-001",
            "ART-28",
            AS_OF,
            "independent-authored-snapshots-not-a-real-case-timeline",
            list(SOURCES),
        ],
        "record identity/provenance",
    )
    for field in (
        "actualOperations",
        "actualCollections",
        "actualNotifications",
        "actualDeployments",
        "actualIncidentDeclarations",
    ):
        same(
            record[field],
            0,
            "no actual operation/collection/notification/deployment/declaration",
        )
    same(
        data["parentReferences"],
        {
            "use": "method-reference-only",
            "caseIds": REFINES,
            "controlValidationRecordId": "CVP-2026-021-001",
            "controlRetestId": "RT-CV21-003",
            "beforeScenarioId": "SCN-CV21-003",
            "afterScenarioId": "SCN-CV21-010",
            "beforeEvidenceId": "EVD-CV21-003-01",
            "afterEvidenceId": "EVD-CV21-010-01",
            "parentHandoffId": "HOF-CV21-22",
            "parentHandoffStatus": "planned-not-delivered",
            "parentReceiptId": None,
            "parentEvidenceTransferred": False,
            "parentStateChanged": False,
            "authorityTransferred": False,
        },
        "parent method reference only: no delivery/evidence/state/authority inheritance",
    )
    same(
        data["authorityBoundary"],
        {
            "parentAuthorityId": "AUTH-CASE-2026-001",
            "parentExpiresAt": "2026-08-19T09:00:00Z",
            "parentRoeId": "ROE-2026-009",
            "parentRoeStatus": "Draft",
            "parentRoeVersion": 1,
            "parentLabId": "LABPLAN-2026-001",
            "parentLabRuntimeExecuted": False,
            "parentExecutionAuthorized": False,
            "scope": "配布JSONの読解と有限比較のみ。実サービスへ接続しない。実Accountは使用しない。実環境で操作しない。",
        },
        "parent expired authority/Draft RoE/read-only scope retained",
    )
    as_of = instant(record["asOf"])
    require(
        instant(data["authorityBoundary"]["parentExpiresAt"]) < as_of,
        "parent authority expired",
    )
    validate_metrics(data["metrics"], as_of)
    validate_items(data["items"], data["metrics"], as_of)
    handoff = data["handoff"]
    same(
        [
            handoff[k]
            for k in (
                "id",
                "targetChapter",
                "itemIds",
                "status",
                "receiptId",
                "owner",
                "dueAt",
                "executionAuthorized",
            )
        ],
        [
            "HOF-IMP22-26",
            26,
            numbered("BLI-IMP22", 8),
            "planned-not-delivered",
            None,
            "SYN-IMP22-DECISION-OWNER",
            DUE,
            False,
        ],
        "handoff remains a plan, not a receipt/authorization",
    )
    same(
        [
            data["safety"][k]
            for k in ("individualMonitoring", "publicRanking", "punitiveKpi")
        ],
        [False, False, False],
        "no individual surveillance/ranking/punitive KPI",
    )


def validate_model(data, schema, contract):
    validate_supported_schema_nodes(schema, "IMP22 schema", schema)
    validate_schema_instance(data, schema)
    validate_semantics(data)
    errors = []
    for path, value in leaves(data):
        if isinstance(value, str):
            location = "/".join(path)
            if not value.strip() or len(value) > 2000:
                errors.append("IMP22 bounded nonempty field: " + location)
            for finding in (
                *scan_action_text(value, location=location),
                *scan_host_policy(value, location=location),
            ):
                errors.append("IMP22 " + location + ": " + finding.category)
    if {k: digest(v) for k, v in data.items()} != contract["authoredInputs"]:
        errors.append("IMP22 authored input snapshot")
    return errors
