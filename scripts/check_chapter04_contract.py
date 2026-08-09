#!/usr/bin/env python3
"""Fail-closed Chapter 4 publication, traceability, and safety contract."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.content_safety_policy import (  # noqa: E402
    POLICY_VERSION as CONTENT_SAFETY_POLICY_VERSION,
    SafetyFinding,
    normalize_visible_text,
    scan_action_text,
    scan_fields,
    scan_host_policy,
)
from scripts.render_reference_baseline import render as render_reference_baseline  # noqa: E402
from scripts.sync_book_site import (  # noqa: E402
    SitePageRegistryError,
    parse_registry_data,
    published_page_title_findings,
)

ERRORS: list[str] = []
EXPECTED_POLICY_VERSION = "1.2.0"

CHAPTER = "manuscript/04-assets-boundaries-threat-model.md"
TEMPLATE = "templates/threat-model.md"
CASE = "cases/ch04-threat-model-example.md"
SOURCE_NOTE = "references/ch04-source-review-2026-08-08.md"
CHANGELOG = "CHANGELOG.md"

CHANGELOG_CH04_SOURCE_NAMES = (
    "NIST CSF 2.0",
    "NIST SP 800-30 Rev.1",
    "OWASP Threat Modeling Project",
)

EXPECTED_PAGES = {
    (CHAPTER, "chapters/chapter-04/index.md", "chapters", 47),
    (TEMPLATE, "templates/threat-model/index.md", "additional", 150),
    (CASE, "cases/chapter-04-threat-model/index.md", "additional", 241),
    (SOURCE_NOTE, "references/chapter-04-source-review/index.md", "additional", 242),
}

EXPECTED_PAGE_TITLES = {
    CHAPTER: "第4章 資産、信頼境界、攻撃面、脅威モデル",
    TEMPLATE: "Threat Model",
    CASE: "第4章 合成記入例：資産・信頼境界・脅威モデル",
    SOURCE_NOTE: "第4章 Source Review Note：Threat Model",
}

EXPECTED_CHAPTER_MARKDOWN_TABLE_HEADINGS = (
    "T-04-01 資産の型と最小記録項目",
    "T-04-02 似て見える用語の違い",
    "T-04-03 Control assurance states",
    "T-04-04 Knowledge stateとHypothesis statusの分離",
)

UNSAFE_PAGE_TITLES = (
    "第三者の本番システムへ接続する",
    "実Tokenを取得してEvidenceにする",
    "個人情報を収集する",
    "マルウェアを実行する",
    "https://example.comへ接続する",
    "第三者の本番システムへ\n接続する",
    "実Tokenを\r取得してEvidenceにする",
    "個人情報を\u2028収集する",
    "マルウェアを\u2029実行する",
    "\u2800",
    "\u115f",
    "\u3164",
    "\uffa0",
)

SAFE_PAGE_TITLES = (
    "第4章 資産、信頼境界、攻撃面、脅威モデル",
    "ART-03 Threat Model",
    "第4章 合成記入例：請求書連携OAuthアプリのAsset / Boundary / Threat Model",
    "第4章 Source Review",
    "第三者の本番システムへ接続しない",
    "マルウェア分類の危険性を分析する",
    "e\u0301vidence title",
    "क\u093f",
    "か\u3099",
    "𐀀\U000101fd",
    "😀\ufe0f",
    "Visible\u2800title",
    "Visible\u115ftitle",
    "Visible\u3164title",
    "Visible\uffa0title",
)

MODEL_STATUSES = {
    "Draft",
    "In Review",
    "Approved for Assessment",
    "Needs Evidence",
    "Superseded",
}
ASSET_TYPES = {
    "Business Outcome",
    "Service",
    "Component",
    "Data",
    "Identity",
    "Control Plane",
    "Evidence",
}
KNOWLEDGE_STATES = {"Unknown", "Assumed", "Confirmed", "Not Applicable"}
FLOW_TYPES = {"Data", "Identity", "Control"}
COLLECTED_EVIDENCE_STATUSES = {"Planned", "Collected", "Rejected", "Inconclusive"}
GAP_STATUSES = {"Open", "Accepted temporarily", "Escalated", "Closed"}
BOUNDARY_TYPES = {
    "Identity Authority",
    "Data Ownership",
    "Administrative Control",
    "Tenant",
    "Third-party Responsibility",
    "Control Plane",
    "Network",
}
HYPOTHESIS_STATUSES = {
    "Candidate",
    "Supported",
    "Partially Supported",
    "Disconfirmed",
    "Inconclusive",
}
ASSURANCE_STATES = {"Unknown", "Documented", "Implemented", "Observed", "Validated"}
EVIDENCE_REQUIREMENT_STATUSES = {"Required", "Deferred", "Replaced", "Not Applicable"}
EXPECTED_SOURCE_IDS = {"SRC-CSF-001", "SRC-NIST-RISK-001", "SRC-OWASP-TM-001"}
EXPECTED_INHERITED_CONTROL_IDS = {
    f"CTRL-2026-{number:03d}" for number in range(1, 5)
}

EXPECTED_CASE_IDS: dict[str, set[str]] = {
    "ASSET": {f"ASSET-2026-{number:03d}" for number in range(1, 8)},
    "FLOW": {f"FLOW-2026-{number:03d}" for number in range(1, 7)},
    "TB": {f"TB-2026-{number:03d}" for number in range(1, 10)},
    "EXP": {f"EXP-2026-{number:03d}" for number in range(1, 4)},
    "EP": {f"EP-2026-{number:03d}" for number in range(1, 4)},
    "TH": {f"TH-2026-{number:03d}" for number in range(1, 7)},
    "MISUSE": {f"MISUSE-2026-{number:03d}" for number in range(1, 3)},
    "PATH": {f"PATH-2026-{number:03d}" for number in range(1, 3)},
    "EDGE": {f"EDGE-2026-{number:03d}" for number in range(1, 8)},
    "CTRL": {f"CTRL-2026-{number:03d}" for number in range(5, 10)},
    "ASM": {f"ASM-2026-{number:03d}" for number in range(1, 4)},
    "GAP": {f"GAP-2026-{number:03d}" for number in range(1, 5)},
    "EREQ": {f"EREQ-2026-{number:03d}" for number in range(1, 5)},
    "ACT-TM": {f"ACT-TM-2026-{number:03d}" for number in range(1, 7)},
    "REA-TM": {f"REA-TM-2026-{number:03d}" for number in range(1, 5)},
}
EXPECTED_CASE_REFERENCE_IDS = {
    family: set(identifiers) for family, identifiers in EXPECTED_CASE_IDS.items()
}
EXPECTED_CASE_REFERENCE_IDS["CTRL"] |= EXPECTED_INHERITED_CONTROL_IDS

CHAPTER4_CONTROL_RELATIONS: dict[str, tuple[str, str | None]] = {
    "CTRL-2026-005": ("supports", "CTRL-2026-001"),
    "CTRL-2026-006": ("supports", "CTRL-2026-002"),
    "CTRL-2026-007": ("supports", "CTRL-2026-003"),
    "CTRL-2026-008": ("independent", None),
    "CTRL-2026-009": ("supports", "CTRL-2026-004"),
}

EXPECTED_DEPENDENCY_IDS = {f"DEP-2026-{number:03d}" for number in range(1, 6)}
EXPECTED_RUBRIC_IDS = {f"RUBRIC-TM-2026-{number:03d}" for number in range(1, 6)}
EXPECTED_INHERITED_EVIDENCE_IDS = {
    "EVD-2026-001",
    "EVD-2026-002",
    "EVD-2026-003",
    "EVD-2026-004",
    "EVD-AUTH-2026-001",
    "NEG-2026-001",
}
EXPECTED_INHERITED_COLLECTED_EVIDENCE_IDS = EXPECTED_INHERITED_EVIDENCE_IDS - {"NEG-2026-001"}
INHERITED_REVIEWER_VALUE = "Not recorded in inherited source"
INHERITED_TH_001_PROPOSITION = (
    "請求書連携アプリの権限が業務要件を超えており、Credentialが不正利用された場合に"
    "顧客Dataへ広範にAccessできる"
)
INHERITED_TH_001_CASE_PROPOSITION = (
    "請求書連携アプリの業務要件超過権限、Credential misuse、顧客Dataへの"
    "広範Access可能性が同時に成立するという第1章の命題"
)
INHERITED_TH_001_CASE_PRECONDITIONS = (
    "過大scope、Credentialの有効性、API到達性を成立条件として評価する"
)
INHERITED_TH_002_PROPOSITION = (
    "管理者同意の変更を監視できず、未承認のscope追加を早期検知できない"
)
INHERITED_TH_002_PRECONDITIONS = "同意Eventの未収集またはRule欠落"
INHERITED_TH_002_IMPACT = "攻撃面拡大の見逃し"
INHERITED_TH_002_CASE_RELATIONS = (
    "`TB-2026-001`, `TB-2026-003`, `FLOW-2026-004`, `EXP-2026-002`"
)
INHERITED_TH_002_ALTERNATIVE = (
    "同意Eventは収集済みでもRule欠落により早期検知できない可能性がある"
)
INHERITED_TH_003_PROPOSITION = "既に同型の不正利用が発生した"
INHERITED_TH_003_PRECONDITIONS = "過去の不正Credential利用"
INHERITED_TH_003_IMPACT = "過去侵害"
INHERITED_TH_003_ASSETS = "`ASSET-2026-001`, `ASSET-2026-003`"
INHERITED_TH_003_RELATIONS = "`TB-2026-002`, `TB-2026-003`"
INHERITED_TH_003_ALTERNATIVE = (
    "TelemetryとRetentionの制約により、未観測を未発生と判断できない"
)
OPPORTUNITY_TH_006_PROPOSITION = (
    "historical scope、Credential metadata、API到達条件とTelemetry不足により、"
    "不正利用の機会条件と影響範囲をsummary-only境界まで限定できない可能性がある"
)
OPPORTUNITY_TH_006_PRECONDITIONS = (
    "historical scope、Credential metadata、API到達条件とTelemetry / Retention Coverageの"
    "確認が不十分である"
)
OPPORTUNITY_TH_006_IMPACT = (
    "既往利用可能性と顧客Dataへの影響範囲の判断がInconclusiveのまま残る"
)
OPPORTUNITY_TH_006_RELATIONS = (
    "`TB-2026-002`, `TB-2026-003`, `TB-2026-007`, `TB-2026-008`, "
    "`FLOW-2026-003`, `FLOW-2026-004`, `FLOW-2026-005`, `EXP-2026-002`, "
    "`EXP-2026-003`"
)
OPPORTUNITY_TH_006_ALTERNATIVE = (
    "実際の不正利用は発生しておらず、Telemetry / Retention不足だけが判断を"
    "Inconclusiveにしている可能性がある"
)
SUMMARY_TH_004_PROPOSITION = (
    "業務要件を超えるscopeがsummary境界を越える影響へつながる可能性がある"
)
CHAPTER_WALKTHROUGH_TRACE = (
    "完成例を読む前に、一つの仮説だけをTemplateへ通す。`DR-2026-001`の継続判断に対し、"
    "Business Asset「請求連携能力」を担う`ASSET-2026-001`とOAuth component "
    "`ASSET-2026-005`を置く。承認からApp設定へ進むControl Flowを`FLOW-2026-001`、"
    "Administrative Controlの変化を第4章固有の`TB-2026-009`、read-only Review接点を"
    "`EXP-2026-001` / `EP-2026-001`とする。第1章から継承する`TB-2026-001`は"
    "業務SaaSからIdentity control planeへOAuth app identityが入る境界のまま変更しない。"
    "そこから「"
    f"{SUMMARY_TH_004_PROPOSITION}」を`TH-2026-004`として記録し、"
    "2026-07-20のhistorical broad scopeを`EDGE-2026-001`、2026-07-25 remediation後の"
    "current scope / binding未確認を`EDGE-2026-002`、summary-only境界への影響条件と"
    "観測点を`EDGE-2026-003`、Tenant binding Evidence不足を`EDGE-2026-004`へ分けて"
    "`PATH-2026-001`として書く。`CTRL-2026-005`と"
    "`CTRL-2026-006`がDocumentedに留まるなら`GAP-2026-002`を開き、"
    "`EREQ-2026-001`、`ACT-TM-2026-001` / `ACT-TM-2026-004`、"
    "`REA-TM-2026-001`へつなぐ。"
)
DECISION_CONFIDENCE_VALUE = (
    "低。これは推奨の確からしさでありseverityではない。2026-07-25のhistorical "
    "scope縮小`Passed`はあるが、post-remediation current scope Snapshotが未収集で、"
    "`GAP-2026-001` / `GAP-2026-003`がOpen / Escalatedのため、再評価前の確信は限定される"
)
DECISION_CONFIDENCE_ROW = f"| Confidence | {DECISION_CONFIDENCE_VALUE} |"
IDENTITY_ASSURANCE_THRESHOLD_SECTION = """### `REA-TM-2026-001`のIdentity assurance判定閾値

- `Workload-only binding check: Passed`は、Workload identity binding snapshotとTenant binding差分に記録されたactive bindingのHuman identityが0件で、すべてが承認済みWorkload identity、Owner、Tenant、scope matrixへ一致する場合だけ記録する。不一致、分類不能または未収集は`Failed / Inconclusive / Not collected`とする。
- `Rotation-management check: Passed`は、rotation手順Review記録にOwner、review interval / trigger、last review result、next review date、exception / failure escalationがあり、未管理または期限超過のactive bindingが0件である場合だけ記録する。欠落、不合格または未収集は`Failed / Inconclusive / Not collected`とする。
- `CTRL-2026-006`は両checkが`Passed`で、対応する新Evidence IDとReviewer sign-offがそろう場合だけ`Observed`へ進める。どちらか一方でも`Failed / Inconclusive / Not collected`なら`Documented`に維持し、`GAP-2026-002`を閉じない。`CTRL-2026-005`のscope判定はこのIdentity判定と分離する。
"""
REA_TM_001_INPUTS_REQUIRED = (
    "2026-07-25 remediation後のApp registration export、scope matrix、"
    "Tenant binding差分、Workload identity binding snapshot、rotation手順Review記録、"
    "新Evidence ID付き・source Evidence IDを記録したWorkload-only binding check結果、"
    "新Evidence ID付き・source Evidence IDを記録したRotation-management check結果、"
    "新Evidence ID付きReviewer sign-off、approval ticket、新Authorization Record / RoE"
)
REA_TM_001_CLOSURE_CRITERIA = (
    "post-remediation current scopeがEvidenceで`Confirmed`となり、最小scope案と"
    "要件の差分がゼロである。新Authorization Record / RoE承認後にのみ変更し、"
    "scope条件が満たされた場合だけ`CTRL-2026-005`を少なくともImplementedとする。"
    "`Workload-only binding check`と`Rotation-management check`の両方が"
    "`Passed`で、新Evidence ID付き・source Evidence IDを記録した各check結果と"
    "新Evidence ID付きReviewer sign-offがそろう場合だけ`CTRL-2026-006`を"
    "少なくともObservedとする。どちらかが"
    "`Failed / Inconclusive / Not collected`なら`CTRL-2026-006`を"
    "`Documented`に維持し、`GAP-2026-002`を閉じない"
)
FLOW_006_EVIDENCE_STATUS = "Planned"
FLOW_006_OBSERVATION_POINT = (
    "収集予定: post-remediation Workload identity binding snapshot、"
    "rotation手順Review記録、offline機械的突合結果"
)
FLOW_004_EVIDENCE_STATUS = "Inconclusive"
FLOW_004_OBSERVATION_POINT = (
    "収集済み: `EVD-2026-003`のAdmin consent Event audit export。未収集: "
    "App identity lifecycle Event Coverage、両Event classのRule test結果"
)
EP_003_CURRENT_EVIDENCE_BOUNDARY = (
    "`EXP-2026-003` / `EP-2026-003`の`EVD-2026-001`と`EVD-2026-002`は"
    "2026-07-20のhistorical scope / requirement inputだけであり、current Tenant binding"
    "またはWorkload identity bindingのEvidenceではない。current Tenant binding差分、"
    "Workload identity binding snapshot、rotation手順Review記録、"
    "offline機械的突合結果は未収集であり、"
    "`FLOW-2026-006`の`Planned`、`GAP-2026-002`、"
    "`EREQ-2026-001`へ渡す。"
)
TB_004_CURRENT_BINDING_BOUNDARY = (
    "`TB-2026-004`のcurrent Workload identity bindingは`Unknown`であり、"
    "`EVD-2026-001`（historical scope）と`EVD-2026-003`（Admin consent Event）は"
    "このbindingを確認するEvidenceではない。current bindingの確認は"
    "`FLOW-2026-006`の`Planned`、`GAP-2026-002`、`EREQ-2026-001`へ渡す。"
)
RULE_TEST_AUTHORIZATION_PROVENANCE_BOUNDARY = (
    "`EVD-AUTH-2026-001`はread-only configuration reviewのAuthorization provenanceであり、"
    "Rule testを承認しない。`EREQ-2026-002`のResulting Evidenceではなく、新しいRule testには"
    "別の新Authorization Record / RoE承認が必要である。"
)
LIFECYCLE_TH_005_PROPOSITION = (
    "App identity lifecycle Eventまたはdecision summary Fieldの観測不足により、"
    "lifecycle変更と月末判断の対応付けが遅れる可能性がある"
)
LIFECYCLE_TH_005_PRECONDITIONS = (
    "lifecycle Audit exportまたはdecision summary Fieldが不足する"
)
LIFECYCLE_TH_005_IMPACT = "Decision遅延とControl assuranceの誤判定"
LIFECYCLE_TH_005_RELATIONS = (
    "`TB-2026-003`, `TB-2026-007`, `FLOW-2026-004`, `FLOW-2026-005`, "
    "`EXP-2026-002`"
)
FRESH_CHAPTER4_HYPOTHESIS_IDS = {
    "TH-2026-004",
    "TH-2026-005",
    "TH-2026-006",
}
EXPECTED_HANDOFF_ROWS = {
    "HO-TM-2026-005": (
        "第5章 ATT&CK",
        "Behavior記述",
        "`TH-2026-001`〜`006`の成立条件、Flow、Boundary、Exposure、観測点",
    ),
    "HO-TM-2026-006": (
        "第6章 観測可能性",
        "Telemetry / logging設計",
        "`CTRL-2026-007` / `CTRL-2026-009`、`EREQ-2026-001`〜`004`、"
        "`GAP-2026-001`〜`004`、Negative finding原則",
    ),
    "HO-TM-2026-009": (
        "第9章 RoE",
        "Rules of Engagement",
        "`CTRL-2026-008`、`AUTH-CASE-2026-001`継承条件、`ACT-TM-2026-001` / "
        "`ACT-TM-2026-002` / `ACT-TM-2026-003` / `ACT-TM-2026-004` / "
        "`ACT-TM-2026-005` / `ACT-TM-2026-006`の"
        "再Authorization依存、停止条件、no outbound、対象外一覧",
    ),
    "HO-TM-2026-011": (
        "第11章 Web/API評価",
        "Web/API Assessment Hypothesis Pack",
        "`CTRL-2026-005`、`TH-2026-001` / `TH-2026-004`、`TB-2026-002` / "
        "`TB-2026-008`、`FLOW-2026-003`、`PATH-2026-001`",
    ),
    "HO-TM-2026-012": (
        "第12章 Identity評価",
        "Identity Attack Path Review",
        "`CTRL-2026-006`、`ASSET-2026-007`、`TB-2026-004`、"
        "`FLOW-2026-002`、`FLOW-2026-006`",
    ),
    "HO-TM-2026-013": (
        "第13章 Platform / Supply Chain",
        "Platform and Supply Chain Assessment",
        "`CTRL-2026-006`、`ASSET-2026-002`、`ASSET-2026-005`、"
        "Credential lifecycle、control plane依存",
    ),
    "HO-TM-2026-014": (
        "第14章 最小影響Validation",
        "Minimal-Impact Validation Record",
        "`CTRL-2026-008`、`EREQ-2026-001`〜`004`、特に`EREQ-2026-004`の"
        "preflight / default-deny / Cleanup証拠、禁止操作、stop条件、fallback",
    ),
    "HO-TM-2026-015": (
        "第15章 Finding / Retest",
        "Finding Report、Retest Record",
        "`CTRL-2026-005` / `CTRL-2026-006` / `CTRL-2026-007` / "
        "`CTRL-2026-008` / `CTRL-2026-009`、`GAP-2026-001`〜`004`、"
        "`ACT-TM-2026-001`〜`006`、`REA-TM-2026-001`〜`004`",
    ),
    "HO-TM-2026-027": (
        "第27章 AI / Agent固有Threat Model",
        "AI / Agent Threat Model拡張",
        "本CaseではN/A。AI / Agent component追加時に再利用するAsset、Flow、Boundary、Threat、Gap ID",
    ),
}
EXPECTED_HANDOFF_IDS = set(EXPECTED_HANDOFF_ROWS)

HANDOFF_INTERPRETATION_BOUNDARY = (
    "以下は上表のHandoffを読解するための焦点であり、入力の完全列挙ではない。"
    "各後続章へ渡す正確な全入力は、上表の`What this artifact provides`を正本とする。"
)

EXPECTED_HANDOFF_INTERPRETATION_LINES = (
    "- 第5章では、継承命題`TH-2026-001`〜`003`、summary-only refinement "
    "`TH-2026-004`、lifecycle / summary Field refinement `TH-2026-005`、"
    "機会条件・影響範囲 refinement `TH-2026-006`を区別してATT&CKの行動言語へ"
    "変換する。",
    "- 第6章では、`CTRL-2026-007` / `CTRL-2026-009`、`EREQ-2026-003` / "
    "`EREQ-2026-004`を主要な観測入力とする。上表の正本どおり"
    "`EREQ-2026-001`〜`004`と`GAP-2026-001`〜`004`を併記して渡すのは、"
    "観測点をDecision、scope、Identity contextから切り離さないためである。",
    "- 第9章では、Lab safetyの`CTRL-2026-008`、`AUTH-CASE-2026-001`継承条件と"
    "`ACT-TM-2026-001` / `ACT-TM-2026-002` / `ACT-TM-2026-003` / "
    "`ACT-TM-2026-004` / `ACT-TM-2026-005` / `ACT-TM-2026-006`の"
    "再Authorization依存をRoEへ具体化する。",
    "- 第11章では、scope assuranceの`CTRL-2026-005`、継承命題`TH-2026-001`と"
    "summary-only refinement `TH-2026-004`、継承した`TB-2026-002`とsummary-only "
    "refinementの`TB-2026-008`、`PATH-2026-001`をWeb/APIの仮説パックへ分解する。",
    "- 第12章では、Identity assuranceの`CTRL-2026-006`、`ASSET-2026-007`と"
    "`TB-2026-004`をIdentity attack pathとして再評価する。",
    "- 第13章では、`CTRL-2026-006`、`ASSET-2026-002`と`ASSET-2026-005`の"
    "control plane依存をPlatform評価へ渡す。",
    "- 第14章では、Lab safetyの`CTRL-2026-008`と`EREQ-2026-004`を含む"
    "最小影響で必要Evidenceだけを集めるValidation設計へ接続する。",
    "- 第15章では、`CTRL-2026-005`〜`009`と`GAP-2026-004`を含むGapを"
    "Finding、Action、Retest、Residual riskへ変換する。",
)

DOCUMENT_CONTROL_FIELDS = (
    "Artifact ID",
    "Threat Model ID",
    "Parent Case ID",
    "Relation",
    "Decision Requirement ID",
    "Authorization Record ID",
    "Title",
    "Model status",
    "Owner",
    "Decision owner",
    "Contributors",
    "Reviewers",
    "Classification",
    "Created",
    "Updated",
    "Review deadline",
    "Reassessment date",
    "Related Issue / Ticket",
)

DECISION_CONTEXT_FIELDS = (
    "Decision Requirement ID",
    "Business process",
    "Decision to support",
    "Decision deadline",
    "In-scope environment",
    "Out-of-scope environment",
    "Scope statement",
    "Non-goals",
    "Business criticality scale",
    "Safety boundary",
    "Minimum sufficient evidence standard",
    "Overcollection boundary",
    "Reassessment trigger summary",
)

GAP_HEADER = (
    "Gap ID",
    "Missing information / control / telemetry",
    "Decision affected",
    "Owner",
    "Due date",
    "Status",
    "Evidence Requirement ID",
    "Action ID",
    "Reassessment ID",
)

COLLECTED_EVIDENCE_HEADER = (
    "Evidence ID",
    "Related Evidence Requirement IDs",
    "Evidence description",
    "Collection conditions / provenance",
    "Status",
    "Reviewer",
    "Collected at",
    "Limitation",
)

HANDOFF_HEADER = (
    "Handoff ID",
    "Target chapter",
    "Deliverable / consumer",
    "What this artifact provides",
    "Acceptance criteria",
    "Reject / return condition",
)

FIELD_VALUE_HEADER = ("Field", "Value")
STATE_FAMILY_HEADER = ("State family", "Exact finite values", "Current usage")
ASSET_HEADER = (
    "Asset ID",
    "Type",
    "Name",
    "Business role / outcome",
    "Owner",
    "Criticality",
    "Data classification",
    "Knowledge state",
    "Evidence IDs",
    "Dependency IDs",
)
DEPENDENCY_HEADER = (
    "Dependency ID",
    "From asset",
    "To asset",
    "Why the dependency matters",
    "Failure consequence",
)
FLOW_HEADER = (
    "Flow ID",
    "Flow type",
    "Source Asset ID",
    "Destination Asset ID",
    "Purpose",
    "Protocol class",
    "Identity / authorization context",
    "Boundary IDs crossed",
    "Data classification",
    "Evidence status",
    "Observation point",
)
BOUNDARY_HEADER = (
    "Boundary ID",
    "Boundary type",
    "From / To",
    "Owner(s)",
    "Trust / authority change",
    "Crossing condition",
    "Control",
    "Failure consequence",
    "Knowledge state",
    "Evidence IDs",
)
EXPOSURE_HEADER = (
    "Exposure ID",
    "Related Asset / Boundary / Flow IDs",
    "Entry Point ID",
    "Reachability class",
    "External dependency",
    "Required authority",
    "Verification status",
    "Evidence ID",
    "Gap ID",
)
ENTRY_POINT_HEADER = (
    "Entry Point ID",
    "Related Exposure IDs",
    "Interface class",
    "Description",
    "Owner",
    "Boundary IDs",
    "Required authority",
    "Observation point",
    "Knowledge state",
    "Evidence IDs",
)
HYPOTHESIS_HEADER = (
    "Hypothesis ID",
    "Decision Requirement ID",
    "Related Asset IDs",
    "Boundary / Flow / Exposure IDs",
    "Statement",
    "Preconditions",
    "Expected impact",
    "Evidence needed",
    "Alternative explanation",
    "Priority",
    "Hypothesis status",
)
MISUSE_HEADER = (
    "Misuse Case ID",
    "Goal",
    "Actor capability class",
    "Preconditions",
    "Affected assets",
    "Boundary crossed",
    "Expected outcome",
    "Observation points",
    "Excluded operational detail",
)
PATH_SUMMARY_HEADER = (
    "Path ID",
    "Related Threat IDs",
    "Entry condition",
    "Intermediate condition",
    "Undesired end state",
    "Safety note",
)
TH_002_005_ALLOCATION_HEADER = ("Allocation", "Consumer IDs", "Meaning")
EXPECTED_TH_002_005_ALLOCATION_ROWS = (
    (
        "Inherited only",
        "`ACT-TM-2026-002`",
        "Admin consent Event / Rule命題だけを扱う",
    ),
    (
        "Refinement only",
        "`ACT-TM-2026-005`",
        "App identity lifecycle Event / decision summary Field命題とlifecycle Rule testの"
        "計画・承認後実行・新Evidence ID付き結果だけを扱う",
    ),
    (
        "Both",
        "`PATH-2026-002`, `CTRL-2026-007`, `CTRL-2026-008`, `GAP-2026-003`, "
        "`EREQ-2026-002`, `EREQ-2026-004`, `ACT-TM-2026-006`, `REA-TM-2026-002`",
        "共通のAudit surface、Safety gateまたは再評価単位で両命題を明示的に扱う",
    ),
)
TH_003_006_ALLOCATION_HEADER = (
    "Occurrence allocation",
    "Consumer IDs",
    "Meaning",
)
EXPECTED_TH_003_006_ALLOCATION_ROWS = (
    (
        "Refinement only",
        "`CTRL-2026-009`, `ASM-2026-002`, `GAP-2026-001`, `ACT-TM-2026-003`",
        "summary-only Field、機会条件、影響範囲の限定可能性だけを扱い、"
        "発生有無を直接判定しない",
    ),
    (
        "Both",
        "`PATH-2026-002`, `ASM-2026-003`, `GAP-2026-003`, `EREQ-2026-003`, "
        "`REA-TM-2026-002`",
        "共通のTelemetry / Retention Evidenceを使うが、発生命題と"
        "機会条件・影響範囲命題を別々に評価する",
    ),
)
ATTACK_PATH_HEADER = (
    "Attack Path ID",
    "Edge ID",
    "From Asset / State",
    "Condition",
    "Boundary ID",
    "To Asset / State",
    "Affected Asset IDs",
    "Expected impact",
    "Observation point",
    "Required Evidence ID",
    "Knowledge state",
)
CONTROL_HEADER = (
    "Control ID",
    "Related Asset / Boundary / Threat / Path IDs",
    "Control statement",
    "Owner",
    "Assurance state",
    "Evidence IDs",
    "Limitation",
    "Gap ID",
    "Reassessment trigger",
)
CHAPTER1_CONTROL_HEADER = (
    "Control ID",
    "Related Decision ID",
    "Related Finding IDs",
    "Improvement",
    "Owner",
    "Due date",
    "Verification method",
    "Result",
)
ASSUMPTION_HEADER = (
    "Assumption ID",
    "Statement",
    "Owner",
    "Validation method",
    "Due date",
    "Status",
    "Related IDs",
)
EVIDENCE_REQUIREMENT_HEADER = (
    "Evidence Requirement ID",
    "Question",
    "Related Threat / Control / Gap",
    "Minimum sufficient evidence",
    "Forbidden / over-collection boundary",
    "Owner",
    "Due date",
    "Status",
    "Resulting Evidence IDs",
)
ACTION_HEADER = (
    "Action ID",
    "Related Gap / Control / Threat",
    "Action",
    "Owner",
    "Due date",
    "Success evidence",
    "Status",
)
LAB_SEQUENCE_HEADER = (
    "Sequence",
    "Owner Action",
    "Entry gate",
    "Operation / scope",
    "Exit evidence / consumer",
)
EXPECTED_LAB_SEQUENCE_ROWS = (
    (
        "1. Safety entry",
        "`ACT-TM-2026-006` Phase B-entry",
        "対象・method・time windowを承認した新Authorization Record / RoE",
        "Rule test前にno-outbound合成Labのpreflightとdefault-denyを検証する。失敗時は開始しない",
        "新Evidence ID付き署名済みpreflight report / default-deny結果を"
        "`ACT-TM-2026-002` / `005`へ供給",
    ),
    (
        "2. Event-class tests",
        "`ACT-TM-2026-002` / `ACT-TM-2026-005` Phase B",
        "Sequence 1の両Evidenceが成功しentry-gate sign-offがある",
        "Admin consentとApp identity lifecycleを別の合成Rule testとして実行する",
        "各Detection test結果へ新Evidence IDを割り当て`REA-TM-2026-002`へ供給",
    ),
    (
        "3. Cleanup",
        "`ACT-TM-2026-006` Phase C",
        "Sequence 2が終了または停止した",
        "直後にCleanup verificationを実行する。失敗時は完了扱いにせずEscalateする",
        "新Evidence ID付きCleanup verificationを`REA-TM-2026-004`へ供給",
    ),
    (
        "4. Separate closure",
        "`REA-TM-2026-002` / `REA-TM-2026-004`",
        "Sequence 1〜3の対応Evidenceがある",
        "Detection assuranceとLab-safety assuranceを別々に評価する",
        "`CTRL-2026-007`と`CTRL-2026-008`をEvidence範囲内で別々に更新する",
    ),
)
LAB_SEQUENCE_COMPLETION_DATE = "2026-08-18"
LAB_SEQUENCE_REASSESSMENT_DATE = "2026-08-19"
EVIDENCE_SUPPLIER_SCHEDULE_HEADER = (
    "Evidence Requirement ID",
    "Supplier Action IDs",
    "Latest supplier completion",
    "Requirement due",
    "Gap IDs",
    "Consuming Reassessment ID",
)
EXPECTED_EVIDENCE_SUPPLIER_SCHEDULE_ROWS = (
    (
        "`EREQ-2026-001`",
        "`ACT-TM-2026-001`, `ACT-TM-2026-004`",
        "2026-08-15",
        "2026-08-15",
        "`GAP-2026-002`",
        "`REA-TM-2026-001`",
    ),
    (
        "`EREQ-2026-002`",
        "`ACT-TM-2026-002`, `ACT-TM-2026-005`",
        "2026-08-18",
        "2026-08-18",
        "`GAP-2026-003`",
        "`REA-TM-2026-002`",
    ),
    (
        "`EREQ-2026-003`",
        "`ACT-TM-2026-002`, `ACT-TM-2026-003`, `ACT-TM-2026-005`",
        "2026-08-18",
        "2026-08-18",
        "`GAP-2026-001`, `GAP-2026-003`",
        "`REA-TM-2026-002`",
    ),
    (
        "`EREQ-2026-004`",
        "`ACT-TM-2026-006`",
        "2026-08-18",
        "2026-08-18",
        "`GAP-2026-004`",
        "`REA-TM-2026-004`",
    ),
)
EXPECTED_ACTION_DUE_DATES = {
    "ACT-TM-2026-001": "2026-08-12",
    "ACT-TM-2026-002": "2026-08-18",
    "ACT-TM-2026-003": "2026-08-18",
    "ACT-TM-2026-004": "2026-08-15",
    "ACT-TM-2026-005": "2026-08-18",
    "ACT-TM-2026-006": "2026-08-18",
}
EXPECTED_EVIDENCE_REQUIREMENT_DUE_DATES = {
    "EREQ-2026-001": "2026-08-15",
    "EREQ-2026-002": "2026-08-18",
    "EREQ-2026-003": "2026-08-18",
    "EREQ-2026-004": "2026-08-18",
}
EXPECTED_GAP_DUE_DATES = {
    "GAP-2026-001": "2026-08-18",
    "GAP-2026-002": "2026-08-21",
    "GAP-2026-003": "2026-08-20",
    "GAP-2026-004": "2026-08-18",
}
EXPECTED_POST_COLLECTION_REASSESSMENT_DATES = {
    "REA-TM-2026-001": "2026-08-19",
    "REA-TM-2026-002": "2026-08-20",
    "REA-TM-2026-004": "2026-08-19",
}
REASSESSMENT_HEADER = (
    "Reassessment ID",
    "Trigger",
    "Scope",
    "Owner",
    "Scheduled date",
    "Inputs required",
    "Closure criteria",
    "Destination chapter / artifact",
)
REVIEW_HEADER = (
    "Review area",
    "Reviewer / role",
    "Rubric",
    "Result",
    "Date",
    "Evidence reference",
    "Notes",
)
RUBRIC_HEADER = ("Rubric ID", "Criterion", "Meets", "Partially meets", "Does not meet")
LIMITATION_HEADER = (
    "Limitation ID",
    "Scope / condition",
    "Unsupported claim",
    "Owner",
    "Reassessment trigger",
)
NEGATIVE_FINDING_HEADER = (
    "Negative Finding ID",
    "Related Evidence IDs",
    "Searched behavior",
    "Search window",
    "Available coverage",
    "Gaps",
    "Permitted conclusion",
)

FIELD_STRUCTURAL = "structural identifier/reference"
FIELD_FINITE = "finite enum/date/metadata"
FIELD_READER_VISIBLE = "reader-visible descriptive/action-bearing"
FIELD_CLASSES = {FIELD_STRUCTURAL, FIELD_FINITE, FIELD_READER_VISIBLE}


@dataclass(frozen=True)
class TableSafetyPolicy:
    """Finite field classification for one public ART-03 Markdown table."""

    header: tuple[str, ...]
    classifications: tuple[tuple[str, str], ...]

    @property
    def reader_visible(self) -> tuple[str, ...]:
        return tuple(name for name, classification in self.classifications if classification == FIELD_READER_VISIBLE)

    @property
    def scan_required(self) -> tuple[str, ...]:
        # Every table cell is public. Structural and finite fields are also
        # scanned as defense in depth so an identifier or date with appended
        # action prose cannot bypass the adapter before structural validation.
        return tuple(name for name, _ in self.classifications)


@dataclass(frozen=True)
class MarkdownTable:
    header: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]
    line: int
    end_line: int


CHAPTER_ASSET_TAXONOMY_HEADER = (
    "型",
    "何を表すか",
    "典型例",
    "最低限の記録項目",
    "混同しやすい対象",
    "誤りの例",
)
CHAPTER_DISTINCTION_HEADER = (
    "用語対",
    "前者",
    "後者",
    "実務上の違い",
    "典型的な誤り",
)
CHAPTER_ASSURANCE_HEADER = (
    "Assurance state",
    "本章での意味",
    "次へ進むためのEvidence",
    "誤った読み方",
)
CHAPTER_STATE_DISTINCTION_HEADER = (
    "対象",
    "何の状態か",
    "有限集合",
    "使い方",
    "してはいけないこと",
)
CHAPTER_HANDOFF_HEADER = (
    "行先",
    "本章から渡すもの",
    "最低限必要なIDまたは情報",
    "渡した先で何に使うか",
    "差戻し条件",
)


def table_safety_policy(
    header: tuple[str, ...],
    *,
    structural: tuple[str, ...],
    finite: tuple[str, ...],
    reader_visible: tuple[str, ...],
) -> TableSafetyPolicy:
    classified = structural + finite + reader_visible
    if len(classified) != len(set(classified)) or set(classified) != set(header):
        raise RuntimeError(f"invalid Chapter 4 table safety classification for {header!r}: {classified!r}")
    classes = {
        **{name: FIELD_STRUCTURAL for name in structural},
        **{name: FIELD_FINITE for name in finite},
        **{name: FIELD_READER_VISIBLE for name in reader_visible},
    }
    classifications = tuple((name, classes[name]) for name in header)
    if {classification for _, classification in classifications} - FIELD_CLASSES:
        raise RuntimeError(f"unknown Chapter 4 safety field class for {header!r}")
    return TableSafetyPolicy(header=header, classifications=classifications)


TABLE_SAFETY_POLICIES = {
    policy.header: policy
    for policy in (
        table_safety_policy(
            FIELD_VALUE_HEADER,
            structural=("Field",),
            finite=(),
            reader_visible=("Value",),
        ),
        table_safety_policy(
            STATE_FAMILY_HEADER,
            structural=("State family",),
            finite=("Exact finite values",),
            reader_visible=("Current usage",),
        ),
        table_safety_policy(
            ASSET_HEADER,
            structural=("Asset ID", "Evidence IDs", "Dependency IDs"),
            finite=("Type", "Criticality", "Data classification", "Knowledge state"),
            reader_visible=("Name", "Business role / outcome", "Owner"),
        ),
        table_safety_policy(
            DEPENDENCY_HEADER,
            structural=("Dependency ID", "From asset", "To asset"),
            finite=(),
            reader_visible=("Why the dependency matters", "Failure consequence"),
        ),
        table_safety_policy(
            FLOW_HEADER,
            structural=("Flow ID", "Source Asset ID", "Destination Asset ID", "Boundary IDs crossed"),
            finite=("Flow type", "Data classification", "Evidence status"),
            reader_visible=("Purpose", "Protocol class", "Identity / authorization context", "Observation point"),
        ),
        table_safety_policy(
            BOUNDARY_HEADER,
            structural=("Boundary ID", "Evidence IDs"),
            finite=("Boundary type", "Knowledge state"),
            reader_visible=(
                "From / To",
                "Owner(s)",
                "Trust / authority change",
                "Crossing condition",
                "Control",
                "Failure consequence",
            ),
        ),
        table_safety_policy(
            EXPOSURE_HEADER,
            structural=(
                "Exposure ID",
                "Related Asset / Boundary / Flow IDs",
                "Entry Point ID",
                "Evidence ID",
                "Gap ID",
            ),
            finite=("Verification status",),
            reader_visible=("Reachability class", "External dependency", "Required authority"),
        ),
        table_safety_policy(
            ENTRY_POINT_HEADER,
            structural=("Entry Point ID", "Related Exposure IDs", "Boundary IDs", "Evidence IDs"),
            finite=("Knowledge state",),
            reader_visible=("Interface class", "Description", "Owner", "Required authority", "Observation point"),
        ),
        table_safety_policy(
            HYPOTHESIS_HEADER,
            structural=("Hypothesis ID", "Decision Requirement ID", "Related Asset IDs", "Boundary / Flow / Exposure IDs"),
            finite=("Priority", "Hypothesis status"),
            reader_visible=("Statement", "Preconditions", "Expected impact", "Evidence needed", "Alternative explanation"),
        ),
        table_safety_policy(
            MISUSE_HEADER,
            structural=("Misuse Case ID", "Affected assets", "Boundary crossed"),
            finite=(),
            reader_visible=(
                "Goal",
                "Actor capability class",
                "Preconditions",
                "Expected outcome",
                "Observation points",
                "Excluded operational detail",
            ),
        ),
        table_safety_policy(
            PATH_SUMMARY_HEADER,
            structural=("Path ID", "Related Threat IDs"),
            finite=(),
            reader_visible=("Entry condition", "Intermediate condition", "Undesired end state", "Safety note"),
        ),
        table_safety_policy(
            TH_002_005_ALLOCATION_HEADER,
            structural=("Allocation", "Consumer IDs"),
            finite=(),
            reader_visible=("Meaning",),
        ),
        table_safety_policy(
            TH_003_006_ALLOCATION_HEADER,
            structural=("Occurrence allocation", "Consumer IDs"),
            finite=(),
            reader_visible=("Meaning",),
        ),
        table_safety_policy(
            ATTACK_PATH_HEADER,
            structural=("Attack Path ID", "Edge ID", "Boundary ID", "Affected Asset IDs", "Required Evidence ID"),
            finite=("Knowledge state",),
            reader_visible=("From Asset / State", "Condition", "To Asset / State", "Expected impact", "Observation point"),
        ),
        table_safety_policy(
            CONTROL_HEADER,
            structural=("Control ID", "Related Asset / Boundary / Threat / Path IDs", "Evidence IDs", "Gap ID"),
            finite=("Assurance state",),
            reader_visible=("Control statement", "Owner", "Limitation", "Reassessment trigger"),
        ),
        table_safety_policy(
            ASSUMPTION_HEADER,
            structural=("Assumption ID", "Related IDs"),
            finite=("Due date", "Status"),
            reader_visible=("Statement", "Owner", "Validation method"),
        ),
        table_safety_policy(
            GAP_HEADER,
            structural=("Gap ID", "Evidence Requirement ID", "Action ID", "Reassessment ID"),
            finite=("Due date", "Status"),
            reader_visible=("Missing information / control / telemetry", "Decision affected", "Owner"),
        ),
        table_safety_policy(
            EVIDENCE_REQUIREMENT_HEADER,
            structural=("Evidence Requirement ID", "Related Threat / Control / Gap", "Resulting Evidence IDs"),
            finite=("Due date", "Status"),
            reader_visible=("Question", "Minimum sufficient evidence", "Forbidden / over-collection boundary", "Owner"),
        ),
        table_safety_policy(
            EVIDENCE_SUPPLIER_SCHEDULE_HEADER,
            structural=(
                "Evidence Requirement ID",
                "Supplier Action IDs",
                "Gap IDs",
                "Consuming Reassessment ID",
            ),
            finite=("Latest supplier completion", "Requirement due"),
            reader_visible=(),
        ),
        table_safety_policy(
            COLLECTED_EVIDENCE_HEADER,
            structural=("Evidence ID", "Related Evidence Requirement IDs"),
            finite=("Status", "Collected at"),
            reader_visible=("Evidence description", "Collection conditions / provenance", "Reviewer", "Limitation"),
        ),
        table_safety_policy(
            NEGATIVE_FINDING_HEADER,
            structural=("Negative Finding ID", "Related Evidence IDs"),
            finite=(),
            reader_visible=("Searched behavior", "Search window", "Available coverage", "Gaps", "Permitted conclusion"),
        ),
        table_safety_policy(
            ACTION_HEADER,
            structural=("Action ID", "Related Gap / Control / Threat"),
            finite=("Due date", "Status"),
            reader_visible=("Action", "Owner", "Success evidence"),
        ),
        table_safety_policy(
            LAB_SEQUENCE_HEADER,
            structural=("Sequence", "Owner Action"),
            finite=(),
            reader_visible=("Entry gate", "Operation / scope", "Exit evidence / consumer"),
        ),
        table_safety_policy(
            REASSESSMENT_HEADER,
            structural=("Reassessment ID",),
            finite=("Scheduled date",),
            reader_visible=("Trigger", "Scope", "Owner", "Inputs required", "Closure criteria", "Destination chapter / artifact"),
        ),
        table_safety_policy(
            HANDOFF_HEADER,
            structural=("Handoff ID",),
            finite=(),
            reader_visible=("Target chapter", "Deliverable / consumer", "What this artifact provides", "Acceptance criteria", "Reject / return condition"),
        ),
        table_safety_policy(
            REVIEW_HEADER,
            structural=("Evidence reference",),
            finite=("Result", "Date"),
            reader_visible=("Review area", "Reviewer / role", "Rubric", "Notes"),
        ),
        table_safety_policy(
            RUBRIC_HEADER,
            structural=("Rubric ID",),
            finite=(),
            reader_visible=("Criterion", "Meets", "Partially meets", "Does not meet"),
        ),
        table_safety_policy(
            LIMITATION_HEADER,
            structural=("Limitation ID",),
            finite=(),
            reader_visible=("Scope / condition", "Unsupported claim", "Owner", "Reassessment trigger"),
        ),
        *(
            table_safety_policy(
                header,
                structural=(),
                finite=(),
                reader_visible=header,
            )
            for header in (
                CHAPTER_ASSET_TAXONOMY_HEADER,
                CHAPTER_DISTINCTION_HEADER,
                CHAPTER_ASSURANCE_HEADER,
                CHAPTER_STATE_DISTINCTION_HEADER,
                CHAPTER_HANDOFF_HEADER,
            )
        ),
    )
}

CHAPTER_TABLE_OCCURRENCES = {
    header: 1
    for header in (
        CHAPTER_ASSET_TAXONOMY_HEADER,
        CHAPTER_DISTINCTION_HEADER,
        CHAPTER_ASSURANCE_HEADER,
        CHAPTER_STATE_DISTINCTION_HEADER,
        CHAPTER_HANDOFF_HEADER,
    )
}

TEMPLATE_TABLE_OCCURRENCES = {
    header: (2 if header == FIELD_VALUE_HEADER else 1)
    for header in (
        FIELD_VALUE_HEADER,
        ASSET_HEADER,
        DEPENDENCY_HEADER,
        FLOW_HEADER,
        BOUNDARY_HEADER,
        EXPOSURE_HEADER,
        ENTRY_POINT_HEADER,
        HYPOTHESIS_HEADER,
        MISUSE_HEADER,
        ATTACK_PATH_HEADER,
        CONTROL_HEADER,
        ASSUMPTION_HEADER,
        GAP_HEADER,
        EVIDENCE_REQUIREMENT_HEADER,
        COLLECTED_EVIDENCE_HEADER,
        ACTION_HEADER,
        REASSESSMENT_HEADER,
        REVIEW_HEADER,
        RUBRIC_HEADER,
        LIMITATION_HEADER,
    )
}

CASE_TABLE_OCCURRENCES = {
    header: (3 if header == FIELD_VALUE_HEADER else 1)
    for header in (
        FIELD_VALUE_HEADER,
        STATE_FAMILY_HEADER,
        ASSET_HEADER,
        DEPENDENCY_HEADER,
        FLOW_HEADER,
        BOUNDARY_HEADER,
        EXPOSURE_HEADER,
        ENTRY_POINT_HEADER,
        HYPOTHESIS_HEADER,
        TH_002_005_ALLOCATION_HEADER,
        TH_003_006_ALLOCATION_HEADER,
        MISUSE_HEADER,
        PATH_SUMMARY_HEADER,
        ATTACK_PATH_HEADER,
        CONTROL_HEADER,
        ASSUMPTION_HEADER,
        GAP_HEADER,
        EVIDENCE_REQUIREMENT_HEADER,
        EVIDENCE_SUPPLIER_SCHEDULE_HEADER,
        COLLECTED_EVIDENCE_HEADER,
        NEGATIVE_FINDING_HEADER,
        ACTION_HEADER,
        LAB_SEQUENCE_HEADER,
        REASSESSMENT_HEADER,
        HANDOFF_HEADER,
        RUBRIC_HEADER,
        REVIEW_HEADER,
    )
}

EXPECTED_HEADINGS = (
    "# 第4章 資産、信頼境界、攻撃面、脅威モデル",
    "## この章の位置付け",
    "## 学習目標",
    "## 前提知識",
    "## 導入Case",
    "## 本章の責任境界",
    "### OWN",
    "### BRIDGE",
    "### DELEGATE",
    "## 安全な演習",
    "## 作成する成果物",
    "## 評価基準",
    "## よくある誤解",
    "## 章のまとめ",
    "## 次に学ぶこと",
    "## 参考資料",
)

EXPECTED_TEMPLATE_HEADINGS = tuple(
    f"## {number}. {title}"
    for number, title in enumerate(
        (
            "Document Control",
            "Decision Context",
            "Asset Register",
            "Flow Register",
            "Trust Boundary Register",
            "Exposure and Entry Point Register",
            "Threat Hypothesis and Misuse Case",
            "Attack Path Register",
            "Control Assurance Register",
            "Assumptions, Unknowns and Gaps",
            "Evidence Requirements and Actions",
            "Reassessment and Handoff",
            "Review and Rubric",
        )
    )
)

EXPECTED_CASE_HEADINGS = ("## この記入例の扱い",) + EXPECTED_TEMPLATE_HEADINGS


def error(message: str) -> None:
    ERRORS.append(message)


def read_text(relative: str) -> str:
    path = ROOT / relative
    if not path.is_file():
        error(f"missing required file: {relative}")
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        error(f"{relative}: not valid UTF-8: {exc}")
        return ""


def load_json(relative: str) -> dict:
    text = read_text(relative)
    if not text:
        return {}
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        error(f"{relative}: invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        error(f"{relative}: root must be an object")
        return {}
    return value


def require_tokens(label: str, text: str, tokens: tuple[str, ...]) -> list[str]:
    return [f"{label}: missing required token {token!r}" for token in tokens if token not in text]


def require_order(label: str, text: str, tokens: tuple[str, ...]) -> list[str]:
    positions: list[int] = []
    messages: list[str] = []
    for token in tokens:
        matches = list(re.finditer(rf"^{re.escape(token)}\s*$", text, re.MULTILINE))
        if len(matches) != 1:
            messages.append(f"{label}: missing ordered token {token!r}")
        positions.append(matches[0].start() if matches else -1)
    present = [position for position in positions if position >= 0]
    if present != sorted(present):
        messages.append(f"{label}: required headings are out of order")
    return messages


def source_ids(text: str) -> set[str]:
    return set(re.findall(r"\bSRC-[A-Z0-9-]+\b", text))


def markdown_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def table_by_header(text: str, header: tuple[str, ...], label: str) -> tuple[list[list[str]], list[str]]:
    messages: list[str] = []
    expected = "| " + " | ".join(header) + " |"
    lines = text.splitlines()
    indexes = [index for index, line in enumerate(lines) if line.strip() == expected]
    if len(indexes) != 1:
        messages.append(f"{label}: expected table header exactly once: {expected!r}; found {len(indexes)}")
        return [], messages
    index = indexes[0]
    if index + 1 >= len(lines):
        messages.append(f"{label}: missing table separator after {expected!r}")
        return [], messages
    separator = markdown_cells(lines[index + 1])
    if len(separator) != len(header) or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator):
        messages.append(f"{label}: invalid table separator after {expected!r}")
    rows: list[list[str]] = []
    for line in lines[index + 2 :]:
        if not line.strip().startswith("|"):
            break
        cells = markdown_cells(line)
        if len(cells) != len(header):
            messages.append(f"{label}: malformed row for {expected!r}: {cells!r}")
        else:
            rows.append(cells)
    return rows, messages


def section(text: str, heading: str, next_heading_level: int = 2) -> str:
    match = re.search(
        rf"^{re.escape(heading)}\s*$\n(?P<body>.*?)(?=^{'#' * next_heading_level} |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group("body") if match else ""


def format_finding(finding: SafetyFinding) -> str:
    return (
        f"{finding.location}: [{finding.category}] {finding.reason}: "
        f"{finding.normalized_excerpt!r} (Policy {finding.policy_version})"
    )


def policy_errors(fields: list[tuple[str, str]]) -> list[str]:
    return [format_finding(finding) for finding in scan_fields(fields)]


_MARKDOWN_LIST_ITEM = re.compile(r"^\s*(?:[-+*]|\d+[.)])\s+(?P<body>.*)$")
_MARKDOWN_HEADING = re.compile(r"^\s{0,3}#{1,6}(?:[ \t]+|$)(?P<body>.*)$")
_MARKDOWN_FENCE = re.compile(
    r"^(?P<indent> {0,3})(?P<marker>`{3,}|~{3,})(?P<info>[^\r\n]*)$"
)
_FENCED_HTML_COMMENT = re.compile(r"<!--(?P<body>.*?)-->", re.DOTALL)
_FENCED_INLINE_LINK = re.compile(
    r"!?\[(?P<label>[^\]\n]*)\]\((?P<destination>[^)\n]+)\)"
)
_FENCED_REFERENCE_LINK = re.compile(
    r"!?\[(?P<label>[^\]\n]*)\]\[(?P<reference>[^\]\n]*)\]"
)
_FENCED_SHORTCUT_LINK = re.compile(r"!?\[(?P<label>[^\]\n]*)\]")
_SAME_LINE_LIST_FENCE = re.compile(
    r"^ {0,3}(?:[-+*]|\d+[.)])[ \t]+(?:`{3,}|~{3,})"
)
_MAX_FENCE_QUOTE_DEPTH = 3
_MAX_FENCE_CONTAINER_INDENT = 12
# Chapter 4 publishes only non-executable textual, structured-data, and diagram
# fences.  Every listed surface is reader-visible and is scanned.  A new or
# executable language fails closed until this finite adapter contract is
# reviewed; unknown languages never become an implicit safety bypass.
_READER_VISIBLE_FENCE_LANGUAGES = {
    "": "plain-text",
    "text": "plain-text",
    "plaintext": "plain-text",
    "md": "markup-source",
    "markdown": "markup-source",
    "json": "structured-data",
    "yaml": "structured-data",
    "yml": "structured-data",
    "mermaid": "diagram-source",
}
_MARKDOWN_LINK_TITLE_TOKEN = r'(?:"[^"\r\n]*"|\'[^\'\r\n]*\'|\([^()\r\n]*\))'
_MARKDOWN_LINK_TITLE = rf"(?P<title>{_MARKDOWN_LINK_TITLE_TOKEN})"
_MARKDOWN_LINK_DESTINATION = r"(?:<[^>\r\n]*>|[^\s()\r\n]+)"
_MARKDOWN_INLINE_LINK_OPENING = re.compile(r"\]\(")
_MARKDOWN_INLINE_LINK = re.compile(
    r"\]\("
    rf"[ \t]*(?P<destination>{_MARKDOWN_LINK_DESTINATION})"
    rf"(?:[ \t]+{_MARKDOWN_LINK_TITLE})?[ \t]*\)"
)
_MARKDOWN_DIRECT_LABEL_BEFORE_TAIL = re.compile(
    r"(?P<image>!)?\[(?P<label>[^\]\r\n]*)\]$"
)
_MARKDOWN_NESTED_IMAGE_LABEL_BEFORE_TAIL = re.compile(
    r"\[!\[(?P<label>[^\]\r\n]*)\]\("
    rf"[ \t]*{_MARKDOWN_LINK_DESTINATION}"
    rf"(?:[ \t]+{_MARKDOWN_LINK_TITLE_TOKEN})?[ \t]*\)\]$"
)
_MARKDOWN_ESCAPED_NESTED_IMAGE_LINK = re.compile(
    r"(?<!\\)\[\\!\[[^\]\r\n]*\]\([^\r\n]*?\)\]\("
)
_MARKDOWN_REFERENCE_DEFINITION_PREFIX = re.compile(r"^\s{0,3}\[[^]\r\n]+\]:")
_MARKDOWN_REFERENCE_DEFINITION = re.compile(
    r"^\s{0,3}\[(?P<reference>[^]\r\n]+)\]:[ \t]*"
    r"(?P<destination><[^>\r\n]+>|[^\s\r\n]+)"
    rf"(?:[ \t]+{_MARKDOWN_LINK_TITLE})?[ \t]*$"
)
_MARKDOWN_REFERENCE_LINK = re.compile(
    r"!?\[(?P<label>[^\]\r\n]+)\]\[(?P<reference>[^\]\r\n]*)\]"
)
_MARKDOWN_NESTED_IMAGE_REFERENCE_LINK = re.compile(
    r"\[!\[(?P<label>[^\]\r\n]+)\]"
    r"\[(?P<image_reference>[^\]\r\n]*)\]\]"
    r"\[(?P<outer_reference>[^\]\r\n]*)\]"
)
_MARKDOWN_NESTED_INLINE_IMAGE_BASE = (
    r"\[!\[(?P<label>[^\]\r\n]+)\]\("
    rf"[ \t]*{_MARKDOWN_LINK_DESTINATION}"
    rf"(?:[ \t]+{_MARKDOWN_LINK_TITLE_TOKEN})?[ \t]*\)\]"
)
_MARKDOWN_NESTED_INLINE_IMAGE_INLINE_LINK = re.compile(
    _MARKDOWN_NESTED_INLINE_IMAGE_BASE
    + r"\("
    + rf"[ \t]*{_MARKDOWN_LINK_DESTINATION}"
    + rf"(?:[ \t]+{_MARKDOWN_LINK_TITLE_TOKEN})?[ \t]*\)"
)
_MARKDOWN_NESTED_INLINE_IMAGE_REFERENCE_LINK = re.compile(
    _MARKDOWN_NESTED_INLINE_IMAGE_BASE
    + r"\[(?P<outer_reference>[^\]\r\n]+)\]"
)
_MARKDOWN_NESTED_INLINE_IMAGE_COLLAPSED = re.compile(
    _MARKDOWN_NESTED_INLINE_IMAGE_BASE + r"\[\]"
)
_MARKDOWN_NESTED_INLINE_IMAGE_SHORTCUT = re.compile(
    _MARKDOWN_NESTED_INLINE_IMAGE_BASE + r"(?![\[(])"
)
_MARKDOWN_SHORTCUT_REFERENCE_LINK = re.compile(
    r"!?\[(?P<label>[^\]\r\n]+)\]"
)
_KRAMDOWN_IAL_START = re.compile(r"\{:")
_KRAMDOWN_IAL_CLASS = r"\.[^\s.#]+"
_KRAMDOWN_IAL_ID = r"#[A-Za-z][A-Za-z0-9_:-]*"
_KRAMDOWN_SAFE_CLASS_ID_IAL_BODY = re.compile(
    rf"[ \t]*(?:{_KRAMDOWN_IAL_ID}|{_KRAMDOWN_IAL_CLASS})+"
    rf"(?:[ \t]+(?:{_KRAMDOWN_IAL_ID}|{_KRAMDOWN_IAL_CLASS})+)*[ \t]*"
)
_KRAMDOWN_BLOCK_IAL_PREFIX = re.compile(
    r"^[ \t]*(?:(?:>[ \t]*){0,3})"
    r"(?:(?:[-+*]|\d+[.)])[ \t]+)?$"
)
_KRAMDOWN_FOOTNOTE_MARKER_TAIL = re.compile(r"\[\^[^\]\r\n]+\]$")
_KRAMDOWN_ENTITY_TAIL = re.compile(
    r"&(?:#[0-9]+|#[xX][0-9A-Fa-f]+|[A-Za-z][A-Za-z0-9]+);$"
)
_KRAMDOWN_DOUBLE_ENCODED_ENTITY_LITERAL_TAIL = re.compile(
    r"&amp;(?:#[0-9]+|#[xX][0-9A-Fa-f]+|[A-Za-z][A-Za-z0-9]+);$"
)
_MARKDOWN_FOOTNOTE_DEFINITION_PREFIX = re.compile(
    r"^\s{0,3}\[\^(?!\^)[^]\r\n]+\]:"
)
_MARKDOWN_FOOTNOTE_DEFINITION = re.compile(
    r"^\s{0,3}\[\^(?!\^)(?P<reference>[^]\r\n]+)\]:[ \t]*(?P<body>.*)$"
)
_MARKDOWN_CONTINUED_LINK_TITLE = re.compile(
    r"^[ \t]+(?:\"[^\"\r\n]*\"|'[^'\r\n]*'|\([^()\r\n]*\))[ \t]*$"
)
_MARKDOWN_AUTOLINK_URL = re.compile(
    r"<(?P<url>(?:(?:https?):)?//[^<>\s]+)>",
    re.IGNORECASE,
)
# Chapter 4 deliberately rejects interpreted raw HTML instead of attempting a
# second, partial HTML attribute parser.  Comments are removed before this
# check, rendered fenced/indented code is selected as literal source, and
# finite same-line code spans are masked.  Autolinks do not match because a
# tag name must end at whitespace, ``/``, ``>``, or end-of-line.
_RAW_HTML_TAG_OPENING = re.compile(
    r"<\/?[A-Za-z][A-Za-z0-9-]*(?=[\t >]|/(?=[\t ]*>)|$)"
    r"|<\?(?=\S)|<!\[(?:CDATA)\[|<![A-Z]",
    re.IGNORECASE,
)
# Pinned Kramdown/GFM renders semicolon-terminated angle references as HTML
# character references, but escapes semicolonless references as reader-visible
# entity-like source.  Python ``html.unescape()`` accepts both forms.  Neutralize
# this finite vocabulary before shared Policy normalization so that its decoded
# ``<...>`` shape cannot be mistaken for non-visible HTML and discard the body.
#
# Numeric references require a code-point boundary: ``&#601`` and ``&#x3c0``
# are different characters, not an angle reference followed by a suffix.  The
# legacy named references ``lt``/``gt`` and ``LT``/``GT`` deliberately accept
# an immediate suffix because Python's decoder consumes those finite prefixes
# without a semicolon (for example, ``&ltfoo`` becomes ``<foo``).  Named
# prefixes need decoder-aware handling: ``&gtcc;`` is a distinct complete HTML5
# entity and must not be truncated to ``cc;``.
_HTML_NUMERIC_ANGLE_ENTITY = re.compile(
    r"&(?:"
    r"#0*(?:60|62)(?:;|(?![0-9]))"
    r"|#x0*(?:3c|3e)(?:;|(?![0-9a-f]))"
    r")",
    re.IGNORECASE,
)
_HTML_NAMED_ANGLE_PREFIX = re.compile(r"&(?:lt|gt|LT|GT);?")
_HTML_NAMED_ENTITY_TOKEN = re.compile(r"&[A-Za-z][A-Za-z0-9]*;?")


def _neutralize_html_angle_entities(value: str) -> str:
    """Blank only finite angle-reference delimiters, preserving their body."""

    spans: list[tuple[int, int]] = []
    for match in _HTML_NUMERIC_ANGLE_ENTITY.finditer(value):
        spans.append(match.span())
    for match in _HTML_NAMED_ANGLE_PREFIX.finditer(value):
        token_match = _HTML_NAMED_ENTITY_TOKEN.match(value, match.start())
        if token_match is None:
            continue
        token = token_match.group(0)
        prefix = match.group(0)
        # Consume the finite legacy prefix only when Python's actual decoder
        # treats that prefix—not a longer complete entity—as the angle.  This
        # preserves distinct names such as ``&ltcc;`` and mixed-case ``&Lt;``.
        if html.unescape(token) != html.unescape(prefix) + token[len(prefix) :]:
            continue
        spans.append(match.span())
    if not spans:
        return value
    projected: list[str] = []
    cursor = 0
    for start, end in sorted(spans):
        if start < cursor:
            continue
        projected.extend((value[cursor:start], " "))
        cursor = end
    projected.append(value[cursor:])
    return "".join(projected)


_VISIBLE_URL_TOKEN = re.compile(r"(?:(?:https?):)?//[^\s<>'\"\])}]+", re.IGNORECASE)
_VISIBLE_ASCII_DOMAIN_TOKEN = re.compile(
    r"(?<![A-Za-z0-9-])"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"
    r"(?:[A-Za-z]{2,63}|xn--[A-Za-z0-9-]{1,59})"
    r"(?![A-Za-z0-9-])",
    re.IGNORECASE,
)
_VISIBLE_IP_TOKEN = re.compile(
    r"(?<![A-Za-z0-9_.:])(?:"
    r"\[(?:[0-9A-Fa-f:.]+)\](?::\d+)?|"
    r"(?:\d{1,3}\.){3}\d{1,3}(?::\d+)?|"
    r"[0-9A-Fa-f]{0,4}:[0-9A-Fa-f:.]+"
    r")(?![A-Za-z0-9_.:])"
)
_VISIBLE_IDN_COARSE_TOKEN = re.compile(r"[^\s`<>\"'()\[\]{}、。！？,;]+")
_VISIBLE_IDN_TRAILING_JAPANESE = re.compile(
    r"(?:です|である|でした|を|は|が|に|へ|と|から|まで|のみ|だけ)+$"
)
_VISIBLE_IDN_LEADING_JAPANESE = re.compile(
    r"^.*(?:は|が|を|に|へ|で|と|:|：)(?=[^.]+\.)"
)
_VISIBLE_IDN_HOST = re.compile(r"(?:[\w-]+\.)+[\w-]+", re.UNICODE)
_VISIBLE_DOTTED_VERSION = re.compile(
    r"v?\d+\.\d+\.\d+(?:-[0-9A-Za-z]+(?:\.[0-9A-Za-z-]+)*)?",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class MarkdownFenceOpening:
    marker: str
    language: str
    surface: str
    quote_depth: int
    container_indent: int


@dataclass(frozen=True)
class MarkdownFenceSpan:
    opening_index: int
    closing_index: int
    opening: MarkdownFenceOpening
    content: tuple[str, ...]


@dataclass(frozen=True)
class MarkdownIndentedCodeSpan:
    opening_index: int
    closing_index: int
    indentation: str
    content: tuple[str, ...]


@dataclass(frozen=True)
class MarkdownFootnoteSpan:
    opening_index: int
    closing_index: int
    reference: str
    content: tuple[str, ...]


@dataclass(frozen=True)
class MarkdownInlineLink:
    """One finite same-line inline link/image and its rendered label."""

    source_start: int
    source_end: int
    label: str
    destination_span: tuple[int, int]
    title: str | None
    title_span: tuple[int, int] | None


def _next_unescaped_backtick_run(
    value: str,
    start: int,
    *,
    required_width: int | None = None,
) -> tuple[int, int] | None:
    """Return the next finite unescaped backtick run."""

    candidate = value.find("`", start)
    while candidate >= 0:
        if _markdown_character_is_escaped(value, candidate):
            candidate = value.find("`", candidate + 1)
            continue
        end = candidate + 1
        while end < len(value) and value[end] == "`":
            end += 1
        width = end - candidate
        if required_width is None or width == required_width:
            return candidate, width
        candidate = value.find("`", end)
    return None


def _reject_comment_shaped_multiline_code_spans(
    lines: list[tuple[int, str]],
) -> None:
    """Fail closed when a multiline code span could be stripped as a comment.

    The Chapter 4 adapter supports finite same-line code spans directly.
    Kramdown/GFM also permits a code span to cross a source newline.  Rather
    than duplicating that renderer's multiline projection, this bounded pass
    rejects a *closed* multiline span when it contains ``<!--``.  Actual HTML
    comments encountered before a backtick opening retain precedence, and a
    normal multiline code span without a comment-shaped token remains valid.
    """

    in_comment = False
    code_width: int | None = None
    code_start_line = 0
    code_crossed_line = False
    code_contains_comment = False

    for line_number, line in lines:
        cursor = 0
        while cursor < len(line):
            if in_comment:
                closing_comment = line.find("-->", cursor)
                if closing_comment < 0:
                    break
                in_comment = False
                cursor = closing_comment + 3
                continue

            if code_width is not None:
                comment = line.find("<!--", cursor)
                closing_code = _next_unescaped_backtick_run(
                    line,
                    cursor,
                    required_width=code_width,
                )
                closing_index = closing_code[0] if closing_code is not None else -1
                if comment >= 0 and (
                    closing_index < 0 or comment < closing_index
                ):
                    code_contains_comment = True
                    cursor = comment + 4
                    continue
                if closing_code is None:
                    break
                if code_crossed_line and code_contains_comment:
                    raise ValueError(
                        f"lines {code_start_line}-{line_number}: unsupported or "
                        "multiline Markdown inline-code span contains an "
                        "HTML-comment-shaped literal"
                    )
                cursor = closing_index + closing_code[1]
                code_width = None
                code_start_line = 0
                code_crossed_line = False
                code_contains_comment = False
                continue

            comment = line.find("<!--", cursor)
            opening_code = _next_unescaped_backtick_run(line, cursor)
            opening_index = opening_code[0] if opening_code is not None else -1
            if comment >= 0 and (
                opening_index < 0 or comment < opening_index
            ):
                in_comment = True
                cursor = comment + 4
                continue
            if opening_code is None:
                break
            code_width = opening_code[1]
            code_start_line = line_number
            code_crossed_line = False
            code_contains_comment = False
            cursor = opening_index + code_width

        if code_width is not None:
            code_crossed_line = True


def _strip_html_comments(lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Remove non-rendered comments while preserving visible same-line text.

    Comment-only physical lines are omitted so a comment embedded between two
    wrapped prose lines cannot split the action/object context.  An unclosed
    comment fails closed instead of hiding the remaining publication surface.
    """

    _reject_comment_shaped_multiline_code_spans(lines)

    visible_lines: list[tuple[int, str]] = []
    in_comment = False
    for line_number, line in lines:
        # Kramdown/GFM renders Markdown titles as tooltip text even when the
        # title literal is shaped like an HTML comment.  Protect the same
        # finite destination/title ranges that the link adapter classifies as
        # metadata, as well as literal inline-code spans, before deciding
        # whether ``<!--`` starts an actual non-rendered HTML comment.  Titles
        # are projected into their own Policy field later; destinations remain
        # hidden from reader-action scanning.
        protected_spans = tuple(
            sorted(
                set(
                    _finite_same_line_code_spans(line)
                    + _finite_markdown_link_noncontent_spans(line)
                )
            )
        )

        def opening_outside_protected_span(start: int) -> int:
            candidate = line.find("<!--", start)
            while candidate >= 0:
                if not any(
                    span_start <= candidate
                    and candidate + len("<!--") <= span_end
                    for span_start, span_end in protected_spans
                ):
                    return candidate
                candidate = line.find("<!--", candidate + 1)
            return -1

        cursor = 0
        visible_parts: list[str] = []
        had_comment = in_comment
        while cursor < len(line):
            if in_comment:
                # Once an actual comment starts, Markdown code-span syntax is
                # not interpreted inside it; the first raw close delimiter
                # therefore ends the non-rendered comment.
                close = line.find("-->", cursor)
                if close < 0:
                    cursor = len(line)
                    break
                in_comment = False
                had_comment = True
                cursor = close + 3
                continue
            opening = opening_outside_protected_span(cursor)
            if opening < 0:
                visible_parts.append(line[cursor:])
                cursor = len(line)
                break
            visible_parts.append(line[cursor:opening])
            in_comment = True
            had_comment = True
            cursor = opening + 4
        visible = "".join(visible_parts)
        if visible or not had_comment:
            visible_lines.append((line_number, visible))
    if in_comment:
        raise ValueError("unclosed HTML comment hides reader-visible prose")
    return visible_lines


def _fence_language(info: str, *, marker: str, line_number: int) -> tuple[str, str]:
    """Classify one top-level rendered fence from the finite Chapter 4 set."""

    normalized = info.strip().casefold()
    if marker.startswith("`") and "`" in normalized:
        raise ValueError(f"line {line_number}: backtick fence info contains a backtick")
    if normalized and not re.fullmatch(r"[a-z0-9_-]+", normalized):
        raise ValueError(f"line {line_number}: unsupported Markdown fence info {info.strip()!r}")
    surface = _READER_VISIBLE_FENCE_LANGUAGES.get(normalized)
    if surface is None:
        raise ValueError(
            f"line {line_number}: unclassified reader-visible Markdown fence language "
            f"{normalized!r}"
        )
    return normalized, surface


def _front_matter_content_start(lines: list[str]) -> int:
    """Return the first content-line index, rejecting unclosed YAML metadata."""

    if not lines or lines[0].strip() != "---":
        return 0
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return index + 1
    raise ValueError("unclosed YAML front matter hides reader-visible Markdown")


def _parse_fence_opening(line: str, *, line_number: int) -> MarkdownFenceOpening | None:
    """Parse the finite top-level/blockquote/indented fence placement set."""

    remainder = line
    quote_depth = 0
    while quote_depth < _MAX_FENCE_QUOTE_DEPTH:
        quote = re.match(r"^ {0,3}>[ \t]?", remainder)
        if not quote:
            break
        remainder = remainder[quote.end() :]
        quote_depth += 1
    if re.match(r"^ {0,3}>", remainder) and re.search(r"(?:`{3,}|~{3,})", remainder):
        raise ValueError(
            f"line {line_number}: Markdown fence exceeds finite blockquote depth "
            f"{_MAX_FENCE_QUOTE_DEPTH}"
        )
    if _SAME_LINE_LIST_FENCE.match(remainder):
        raise ValueError(
            f"line {line_number}: same-line list fences are unsupported; "
            "use a finite indented fence block"
        )
    if remainder.startswith("\t") and re.match(r"^\t+(?:`{3,}|~{3,})", remainder):
        raise ValueError(f"line {line_number}: tab-indented Markdown fence is unsupported")

    leading_spaces = len(remainder) - len(remainder.lstrip(" "))
    candidate = remainder[leading_spaces:]
    if not re.match(r"^(?:`{3,}|~{3,})", candidate):
        return None
    maximum_indent = _MAX_FENCE_CONTAINER_INDENT + 3
    if leading_spaces > maximum_indent:
        raise ValueError(
            f"line {line_number}: Markdown fence indent {leading_spaces} exceeds "
            f"finite maximum {maximum_indent}"
        )
    container_indent = (leading_spaces // 4) * 4
    relative_indent = leading_spaces - container_indent
    normalized_line = f"{' ' * relative_indent}{candidate}"
    fence = _MARKDOWN_FENCE.fullmatch(normalized_line)
    if not fence:
        return None
    marker = fence.group("marker")
    language, surface = _fence_language(
        fence.group("info"), marker=marker, line_number=line_number
    )
    return MarkdownFenceOpening(
        marker=marker,
        language=language,
        surface=surface,
        quote_depth=quote_depth,
        container_indent=container_indent,
    )


def _fence_container_content(
    line: str,
    *,
    opening: MarkdownFenceOpening,
    line_number: int,
) -> str:
    """Remove the finite container prefix from one fence body/closing line."""

    remainder = line
    for _ in range(opening.quote_depth):
        quote = re.match(r"^ {0,3}>[ \t]?", remainder)
        if not quote:
            if not remainder.strip():
                return ""
            raise ValueError(
                f"line {line_number}: rendered fence escaped its blockquote container"
            )
        remainder = remainder[quote.end() :]
    if opening.container_indent:
        if not remainder.strip():
            return ""
        prefix = " " * opening.container_indent
        if not remainder.startswith(prefix):
            raise ValueError(
                f"line {line_number}: rendered fence escaped its indented container"
            )
        remainder = remainder[opening.container_indent :]
    return remainder


def _rendered_fence_spans(lines: list[str], *, start_index: int) -> list[MarkdownFenceSpan]:
    """Parse all finite rendered fences and fail closed on boundary drift."""

    spans: list[MarkdownFenceSpan] = []
    index = start_index
    while index < len(lines):
        opening = _parse_fence_opening(lines[index], line_number=index + 1)
        if opening is None:
            index += 1
            continue
        content: list[str] = []
        closing_index = index + 1
        while closing_index < len(lines):
            visible_line = _fence_container_content(
                lines[closing_index],
                opening=opening,
                line_number=closing_index + 1,
            )
            if re.fullmatch(
                rf" {{0,3}}{re.escape(opening.marker[0])}"
                rf"{{{len(opening.marker)},}}[ \t]*",
                visible_line,
            ):
                break
            content.append(visible_line)
            closing_index += 1
        if closing_index >= len(lines):
            raise ValueError(
                f"line {index + 1}: unclosed Markdown fence hides reader-visible content"
            )
        spans.append(
            MarkdownFenceSpan(
                opening_index=index,
                closing_index=closing_index,
                opening=opening,
                content=tuple(content),
            )
        )
        index = closing_index + 1
    return spans


def _rendered_indented_code_spans(
    lines: list[str],
    *,
    start_index: int,
    excluded_lines: set[int],
) -> list[MarkdownIndentedCodeSpan]:
    """Select finite four-space/tab reader-visible code blocks.

    This is deliberately a bounded publication adapter rather than a complete
    CommonMark block parser.  Every nonblank line beginning with four spaces or
    one tab outside a parsed fenced block is treated as reader-visible literal
    code.  Blank continuation lines stay inside a span only when another
    indented line follows, so ordinary paragraph boundaries remain stable.
    """

    spans: list[MarkdownIndentedCodeSpan] = []
    index = start_index
    while index < len(lines):
        if index in excluded_lines:
            index += 1
            continue
        line = lines[index]
        if line.startswith("    "):
            indentation = "spaces"
        elif line.startswith("\t"):
            indentation = "tab"
        else:
            index += 1
            continue

        content: list[str] = []
        indentation_kinds: set[str] = set()
        closing_index = index
        while closing_index < len(lines) and closing_index not in excluded_lines:
            candidate = lines[closing_index]
            if candidate.startswith("    "):
                indentation_kinds.add("spaces")
                content.append(candidate[4:])
                closing_index += 1
                continue
            if candidate.startswith("\t"):
                indentation_kinds.add("tab")
                content.append(candidate[1:])
                closing_index += 1
                continue
            if not candidate.strip():
                lookahead = closing_index + 1
                while (
                    lookahead < len(lines)
                    and lookahead not in excluded_lines
                    and not lines[lookahead].strip()
                ):
                    lookahead += 1
                if (
                    lookahead < len(lines)
                    and lookahead not in excluded_lines
                    and (
                        lines[lookahead].startswith("    ")
                        or lines[lookahead].startswith("\t")
                    )
                ):
                    content.append("")
                    closing_index += 1
                    continue
            break
        indentation = (
            next(iter(indentation_kinds))
            if len(indentation_kinds) == 1
            else "mixed"
        )
        spans.append(
            MarkdownIndentedCodeSpan(
                opening_index=index,
                closing_index=closing_index - 1,
                indentation=indentation,
                content=tuple(content),
            )
        )
        index = closing_index
    return spans


def _rendered_footnote_spans(
    lines: list[str],
    *,
    start_index: int,
    excluded_lines: set[int],
) -> list[MarkdownFootnoteSpan]:
    """Select finite Kramdown/GFM footnote definitions as visible prose.

    A footnote definition is not link metadata: its body is rendered in the
    document footnote list.  This bounded parser owns a same-line body plus
    four-space/tab continuations, including blank lines only when another
    indented continuation follows.  Fenced blocks are excluded by the caller;
    unsupported block shapes remain visible to the ordinary fail-closed
    adapters instead of being silently discarded.
    """

    spans: list[MarkdownFootnoteSpan] = []
    index = start_index
    while index < len(lines):
        if index in excluded_lines:
            index += 1
            continue
        line = lines[index]
        prefix = _MARKDOWN_FOOTNOTE_DEFINITION_PREFIX.match(line)
        if prefix is None:
            index += 1
            continue
        definition = _MARKDOWN_FOOTNOTE_DEFINITION.fullmatch(line)
        if definition is None:
            raise ValueError(f"line {index + 1}: malformed Markdown footnote definition")

        content = [definition.group("body")]
        closing_index = index
        cursor = index + 1
        while cursor < len(lines) and cursor not in excluded_lines:
            candidate = lines[cursor]
            if candidate.startswith("    "):
                content.append(candidate[4:])
                closing_index = cursor
                cursor += 1
                continue
            if candidate.startswith("\t"):
                content.append(candidate[1:])
                closing_index = cursor
                cursor += 1
                continue
            if not candidate.strip():
                lookahead = cursor + 1
                while (
                    lookahead < len(lines)
                    and lookahead not in excluded_lines
                    and not lines[lookahead].strip()
                ):
                    lookahead += 1
                if (
                    lookahead < len(lines)
                    and lookahead not in excluded_lines
                    and (
                        lines[lookahead].startswith("    ")
                        or lines[lookahead].startswith("\t")
                    )
                ):
                    content.append("")
                    closing_index = cursor
                    cursor += 1
                    continue
            break
        spans.append(
            MarkdownFootnoteSpan(
                opening_index=index,
                closing_index=closing_index,
                reference=definition.group("reference"),
                content=tuple(content),
            )
        )
        index = cursor
    return spans


def _literal_fence_visible_fields(
    text: str,
    *,
    location: str,
) -> list[tuple[str, str]]:
    """Project finite literal-source forms into Policy-visible fields.

    Markdown/HTML syntax inside a fence is displayed literally rather than
    interpreted.  The main projection removes complete comment spans and keeps
    inline-link labels so syntax cannot split an object, action, or negation.
    Comment bodies and link destinations are scanned as separate visible fields,
    so the projection does not hide dangerous text or non-approved hosts.  This
    is source-surface selection only; all safety semantics stay in shared Policy
    1.2.0.
    """

    decoded = html.unescape(text)
    # Literal blocks undergo one adapter decode before shared normalization.
    # A source such as ``&amp;#60`` therefore reaches this point as ``&#60``;
    # neutralize the same finite delimiter vocabulary at this layer as well.
    decoded = _neutralize_html_angle_entities(decoded)
    comments: list[str] = []

    def drop_comment(match: re.Match[str]) -> str:
        comments.append(match.group("body"))
        return ""

    projected = _FENCED_HTML_COMMENT.sub(drop_comment, decoded)
    if "<!--" in projected or "-->" in projected:
        raise ValueError(f"{location}: unbalanced literal HTML comment in rendered fence")

    def project_link_syntax(value: str) -> tuple[str, list[str]]:
        destinations: list[str] = []

        def project_inline_link(match: re.Match[str]) -> str:
            destinations.append(match.group("destination"))
            return match.group("label")

        value = _FENCED_INLINE_LINK.sub(project_inline_link, value)
        if re.search(r"\]\s*\(", value):
            raise ValueError(f"{location}: unsupported literal Markdown inline-link shape")
        value = _FENCED_REFERENCE_LINK.sub(lambda match: match.group("label"), value)
        value = _FENCED_SHORTCUT_LINK.sub(lambda match: match.group("label"), value)
        # A truncated image opener is still displayed literally.  Remove its
        # finite delimiter pair together so the remaining ``!`` cannot split an
        # object or local negation after square delimiters are projected out.
        value = value.replace("![", "[")
        # Any unmatched square delimiters are still literal reader-visible source.
        # Removing the delimiters rather than inserting spaces prevents an
        # unmatched form from splitting a protected object or local negation.
        value = value.replace("[", "").replace("]", "")
        return value, destinations

    projected, destinations = project_link_syntax(projected)
    # In a rendered literal block, tag delimiters are visible source rather
    # than interpreted HTML.  Neutralize only the delimiters so attribute
    # names and values remain Policy-visible instead of being discarded by
    # generic Markdown/HTML normalization.
    projected = projected.replace("<", " ").replace(">", " ")

    fields: list[tuple[str, str]] = []
    main = projected.strip()
    if main:
        fields.append((location, main))
    for index, body in enumerate(comments, start=1):
        comment_location = f"{location}/html-comment[{index}]"
        visible_comment, comment_destinations = project_link_syntax(body)
        visible_comment = visible_comment.replace("<", " ").replace(">", " ")
        if visible_comment.strip():
            fields.append((comment_location, visible_comment.strip()))
        fields.extend(
            (
                f"{comment_location}/link-destination[{destination_index}]",
                destination.strip(),
            )
            for destination_index, destination in enumerate(
                comment_destinations, start=1
            )
            if destination.strip()
        )
    fields.extend(
        (f"{location}/link-destination[{index}]", destination.strip())
        for index, destination in enumerate(destinations, start=1)
        if destination.strip()
    )
    return fields


def _markdown_title_value(token: str) -> str:
    """Remove one finite Markdown title delimiter pair."""

    if len(token) < 2 or (token[0], token[-1]) not in {
        ('"', '"'),
        ("'", "'"),
        ("(", ")"),
    }:
        raise ValueError(f"unsupported Markdown link title token: {token!r}")
    return token[1:-1]


def _markdown_character_is_escaped(value: str, index: int) -> bool:
    """Return whether a Markdown delimiter has an odd backslash prefix."""

    backslashes = 0
    cursor = index - 1
    while cursor >= 0 and value[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


@dataclass(frozen=True)
class _MarkdownUnderscoreDelimiter:
    """One finite underscore delimiter run in pinned Kramdown/GFM prose."""

    start: int
    end: int
    width: int
    can_open: bool
    can_close: bool


_KRAMDOWN_UNDERSCORE_EMPHASIS_WIDTHS = frozenset({1, 2, 3})


def _markdown_punctuation_or_symbol(character: str) -> bool:
    """Use CommonMark's Unicode punctuation/symbol class for flank tests."""

    return bool(character) and unicodedata.category(character)[0] in {"P", "S"}


def _kramdown_underscore_delimiters(
    value: str,
    *,
    protected: tuple[tuple[int, int], ...],
) -> tuple[_MarkdownUnderscoreDelimiter, ...]:
    """Classify a bounded same-line underscore delimiter corpus.

    Pinned Kramdown 2.5.2 with kramdown-parser-gfm 1.1.0 follows the
    CommonMark left/right-flanking rules for underscore emphasis.  This
    adapter owns only unescaped runs of width 1, 2, or 3 on one source line.
    Wider, multiline, malformed, intraword, code, destination, and title forms
    remain literal source instead of being guessed into rendered emphasis.
    """

    def overlaps(start: int, end: int) -> bool:
        return any(
            start < span_end and span_start < end
            for span_start, span_end in protected
        )

    delimiters: list[_MarkdownUnderscoreDelimiter] = []
    for match in re.finditer(r"_+", value):
        start, end = match.span()
        width = end - start
        if (
            width not in _KRAMDOWN_UNDERSCORE_EMPHASIS_WIDTHS
            or overlaps(start, end)
            or _markdown_character_is_escaped(value, start)
            or "\n" in value[start:end]
        ):
            continue

        before = value[start - 1] if start else "\n"
        after = value[end] if end < len(value) else "\n"
        before_whitespace = before.isspace()
        after_whitespace = after.isspace()
        before_punctuation = _markdown_punctuation_or_symbol(before)
        after_punctuation = _markdown_punctuation_or_symbol(after)
        left_flanking = not after_whitespace and (
            not after_punctuation or before_whitespace or before_punctuation
        )
        right_flanking = not before_whitespace and (
            not before_punctuation or after_whitespace or after_punctuation
        )
        delimiters.append(
            _MarkdownUnderscoreDelimiter(
                start=start,
                end=end,
                width=width,
                can_open=left_flanking
                and (not right_flanking or before_punctuation),
                can_close=right_flanking
                and (not left_flanking or after_punctuation),
            )
        )
    return tuple(delimiters)


def _project_kramdown_underscore_emphasis(value: str) -> str:
    """Project finite rendered underscore emphasis to its visible text.

    The delimiter stack consumes underscore units nearest the emphasized
    content first.  This projects both same-width pairs and mixed-width forms
    that Kramdown decomposes into nested emphasis/strong nodes, while refusing
    crossing or whitespace-only pairs.  This is deliberately a finite renderer
    adapter for runs of width 1--3, not a complete Markdown emphasis parser.
    """

    protected = tuple(
        sorted(
            set(_finite_same_line_code_spans(value))
            | set(_finite_markdown_link_noncontent_spans(value))
        )
    )
    delimiters = _kramdown_underscore_delimiters(value, protected=protected)
    # Each opener unit carries the end of its source run.  The latter prevents
    # underscores in a delimiter run from making a whitespace-only body appear
    # non-empty when a mixed-width closer is considered.
    stack: list[tuple[int, int]] = []
    pairs: list[tuple[int, int]] = []
    for delimiter in delimiters:
        consumed_closers = 0
        if delimiter.can_close:
            for closer_index in range(delimiter.start, delimiter.end):
                if not stack:
                    break
                opener_index, content_start = stack[-1]
                if not any(
                    not character.isspace()
                    for character in value[content_start : delimiter.start]
                ):
                    break
                stack.pop()
                pairs.append((opener_index, closer_index))
                consumed_closers += 1
        if delimiter.can_open:
            stack.extend(
                (opener_index, delimiter.end)
                for opener_index in range(
                    delimiter.start + consumed_closers,
                    delimiter.end,
                )
            )

    if not pairs:
        return value
    projected = list(value)
    for opener_index, closer_index in pairs:
        projected[opener_index] = ""
        projected[closer_index] = ""
    return "".join(projected)


def _finite_same_line_code_spans(value: str) -> tuple[tuple[int, int], ...]:
    """Return finite same-line Markdown code-span ranges.

    This bounded scanner owns exact-length, unescaped backtick pairs on one
    line.  An unmatched delimiter remains ordinary source; the cross-line
    prepass separately rejects a closed multiline span when it could hide a
    comment-shaped Policy surface.
    """

    spans: list[tuple[int, int]] = []
    index = 0
    while index < len(value):
        if value[index] != "`" or _markdown_character_is_escaped(value, index):
            index += 1
            continue
        opening = index
        while index < len(value) and value[index] == "`":
            index += 1
        width = index - opening
        closing = index
        matched = False
        while closing < len(value):
            if value[closing] != "`" or _markdown_character_is_escaped(value, closing):
                closing += 1
                continue
            end = closing
            while end < len(value) and value[end] == "`":
                end += 1
            if end - closing == width:
                spans.append((opening, end))
                index = end
                matched = True
                break
            closing = end
        if not matched:
            # A valid matching delimiter may occur on a later source line;
            # otherwise Kramdown/GFM renders this as an ordinary literal.
            index = opening + width
    return tuple(spans)


def _mask_finite_same_line_code_spans(value: str) -> str:
    """Mask finite code spans for interpreted-raw-HTML classification."""

    masked = list(value)
    for start, end in _finite_same_line_code_spans(value):
        masked[start:end] = " " * (end - start)
    return "".join(masked)


def _finite_markdown_inline_links(
    value: str,
    *,
    location: str = "reader-visible Markdown",
) -> tuple[MarkdownInlineLink, ...]:
    """Parse the finite same-line inline links/images interpreted by Kramdown.

    This is the single recognition source for rendered-label projection,
    destination/title ownership, tooltip extraction, and IAL attachment.  A
    recognized label followed by an unsupported tail fails closed.  Link-like
    source inside a finite same-line code span remains literal.
    """

    code_spans = _finite_same_line_code_spans(value)
    literal_surface = _mask_finite_same_line_code_spans(value)
    if _MARKDOWN_ESCAPED_NESTED_IMAGE_LINK.search(literal_surface):
        # Pinned Kramdown treats the escaped inner image source as literal text
        # owned by the outer link label.  That would make the inner destination
        # reader-visible rather than metadata.  The finite Chapter 4 adapter
        # does not recursively reinterpret that shape, so reject it instead of
        # partially projecting it and hiding visible source.
        raise ValueError(
            f"{location}: escaped nested-image link is outside the finite "
            "renderer contract"
        )
    links: list[MarkdownInlineLink] = []
    for opening in _MARKDOWN_INLINE_LINK_OPENING.finditer(value):
        if any(start <= opening.start() < end for start, end in code_spans):
            continue
        label = _finite_inline_label_before_tail(value, opening.start())
        if label is None:
            continue
        source_start, rendered_label = label
        tail = _MARKDOWN_INLINE_LINK.match(value, opening.start())
        if tail is None:
            raise ValueError(
                f"{location}: unsupported or multiline Markdown inline-link shape"
            )
        source_end = tail.end()
        if any(
            source_start < code_end and code_start < source_end
            for code_start, code_end in code_spans
        ):
            continue
        title_span = tail.span("title") if tail.group("title") is not None else None
        links.append(
            MarkdownInlineLink(
                source_start=source_start,
                source_end=source_end,
                label=rendered_label,
                destination_span=tail.span("destination"),
                title=tail.group("title"),
                title_span=title_span,
            )
        )
    return tuple(
        sorted(
            set(links),
            key=lambda link: (link.source_start, -link.source_end, link.label),
        )
    )


def _project_markdown_inline_link_labels(
    value: str,
    *,
    location: str = "reader-visible Markdown",
) -> str:
    """Project finite inline links/images to exactly their rendered label.

    Pinned Kramdown/GFM emits an empty link as a zero-text anchor and an empty
    image alt as no text.  The complete source span must therefore disappear;
    a non-empty label/alt replaces the span exactly.  For a supported nested
    image link, the outermost span owns the rendered alt.  Crossing spans are
    outside the finite contract and fail closed.
    """

    selected: list[MarkdownInlineLink] = []
    for candidate in _finite_markdown_inline_links(value, location=location):
        overlaps = [
            link
            for link in selected
            if candidate.source_start < link.source_end
            and link.source_start < candidate.source_end
        ]
        if not overlaps:
            selected.append(candidate)
            continue
        if all(
            link.source_start <= candidate.source_start
            and candidate.source_end <= link.source_end
            for link in overlaps
        ):
            # An already selected outer nested-image link owns the rendered alt.
            continue
        raise ValueError(
            f"{location}: crossing Markdown inline-link spans are outside the "
            "finite renderer contract"
        )

    if not selected:
        return value
    parts: list[str] = []
    cursor = 0
    for link in selected:
        if link.source_start < cursor:
            raise ValueError(
                f"{location}: overlapping Markdown inline-link projection"
            )
        parts.extend((value[cursor : link.source_start], link.label))
        cursor = link.source_end
    parts.append(value[cursor:])
    return "".join(parts)


def _finite_markdown_link_noncontent_spans(value: str) -> tuple[tuple[int, int], ...]:
    """Return exact finite destination/title ranges on one source line.

    Destinations are link metadata rather than interpreted HTML or
    reader-visible prose.  Titles are selected separately as rendered
    tooltips.  Labels remain unmasked because inline HTML in a rendered label
    is still subject to the Chapter 4 raw-HTML prohibition.
    """

    spans: list[tuple[int, int]] = []
    definition = _MARKDOWN_REFERENCE_DEFINITION.fullmatch(value)
    if definition is not None:
        spans.append(definition.span("destination"))
        if definition.group("title") is not None:
            spans.append(definition.span("title"))
    for link in _finite_markdown_inline_links(value):
        spans.append(link.destination_span)
        if link.title_span is not None:
            spans.append(link.title_span)
    return tuple(sorted(set(spans)))


def _normalized_markdown_reference_label(value: str) -> str:
    """Return the bounded case/whitespace key used by local link references."""

    return " ".join(value.split()).casefold()


def _markdown_reference_definition_labels(text: str) -> frozenset[str]:
    """Return valid non-footnote local reference labels in one document."""

    source_lines = text.splitlines()
    content_start = _front_matter_content_start(source_lines)
    fenced_spans = _rendered_fence_spans(source_lines, start_index=content_start)
    excluded_lines = {
        index
        for span in fenced_spans
        for index in range(span.opening_index, span.closing_index + 1)
    }
    footnote_spans = _rendered_footnote_spans(
        source_lines,
        start_index=content_start,
        excluded_lines=excluded_lines,
    )
    excluded_lines |= {
        index
        for span in footnote_spans
        for index in range(span.opening_index, span.closing_index + 1)
    }
    indented_spans = _rendered_indented_code_spans(
        source_lines,
        start_index=content_start,
        excluded_lines=excluded_lines,
    )
    excluded_lines |= {
        index
        for span in indented_spans
        for index in range(span.opening_index, span.closing_index + 1)
    }
    visible_lines = _strip_html_comments(
        [
            (index + 1, "" if index in excluded_lines else line)
            for index, line in enumerate(source_lines)
            if index >= content_start
        ]
    )
    labels: set[str] = set()
    for _, line in visible_lines:
        definition = _MARKDOWN_REFERENCE_DEFINITION.fullmatch(line)
        if definition is None or definition.group("reference").startswith("^"):
            continue
        labels.add(_normalized_markdown_reference_label(definition.group("reference")))
    return frozenset(labels)


def _project_markdown_reference_link_labels(
    value: str,
    *,
    reference_labels: frozenset[str],
) -> str:
    """Project defined reference links to rendered labels, not hidden IDs.

    Full, collapsed, shortcut, and finite nested-image forms are reduced only
    when a valid local definition exists.  Undefined forms remain literal
    source.  Inline-code spans are reader-visible literal Markdown and are not
    interpreted as links.
    """

    def project_once(current: str) -> str:
        protected = _finite_same_line_code_spans(current)
        occupied: list[tuple[int, int]] = []
        replacements: list[tuple[int, int, str]] = []

        def overlaps(
            spans: list[tuple[int, int]] | tuple[tuple[int, int], ...],
            start: int,
            end: int,
        ) -> bool:
            return any(start < span_end and span_start < end for span_start, span_end in spans)

        for match in _MARKDOWN_NESTED_INLINE_IMAGE_INLINE_LINK.finditer(current):
            start, end = match.span()
            occupied.append((start, end))
            if not overlaps(protected, start, end):
                # Both image and outer destinations are hidden metadata.  Only
                # the rendered image alt participates in Policy scanning.
                replacements.append((start, end, match.group("label")))

        for match in _MARKDOWN_NESTED_INLINE_IMAGE_REFERENCE_LINK.finditer(current):
            start, end = match.span()
            occupied.append((start, end))
            if overlaps(protected, start, end):
                continue
            if (
                _normalized_markdown_reference_label(match.group("outer_reference"))
                in reference_labels
            ):
                replacements.append((start, end, match.group("label")))

        # Pinned Kramdown renders these two near-misses as an inline image with
        # literal outer brackets rather than as a reference link.  The image
        # alt remains reader-visible; reduce only the finite wrappers so they
        # cannot split a protected phrase.
        for pattern in (
            _MARKDOWN_NESTED_INLINE_IMAGE_COLLAPSED,
            _MARKDOWN_NESTED_INLINE_IMAGE_SHORTCUT,
        ):
            for match in pattern.finditer(current):
                start, end = match.span()
                if overlaps(occupied, start, end):
                    continue
                occupied.append((start, end))
                if not overlaps(protected, start, end):
                    replacements.append((start, end, match.group("label")))

        for match in _MARKDOWN_NESTED_IMAGE_REFERENCE_LINK.finditer(current):
            start, end = match.span()
            occupied.append((start, end))
            if overlaps(protected, start, end):
                continue
            image_reference = match.group("image_reference") or match.group("label")
            outer_reference = match.group("outer_reference") or match.group("label")
            if all(
                _normalized_markdown_reference_label(reference) in reference_labels
                for reference in (image_reference, outer_reference)
            ):
                replacements.append((start, end, match.group("label")))

        for match in _MARKDOWN_REFERENCE_LINK.finditer(current):
            start, end = match.span()
            if overlaps(occupied, start, end):
                continue
            occupied.append((start, end))
            if overlaps(protected, start, end):
                continue
            reference = match.group("reference") or match.group("label")
            if _normalized_markdown_reference_label(reference) in reference_labels:
                replacements.append((start, end, match.group("label")))

        for match in _MARKDOWN_SHORTCUT_REFERENCE_LINK.finditer(current):
            start, end = match.span()
            if overlaps(protected, start, end) or overlaps(occupied, start, end):
                continue
            if (
                _normalized_markdown_reference_label(match.group("label"))
                in reference_labels
            ):
                replacements.append((start, end, match.group("label")))

        if not replacements:
            return current
        parts: list[str] = []
        cursor = 0
        for start, end, label in sorted(replacements):
            if start < cursor:
                continue
            parts.extend((current[cursor:start], label))
            cursor = end
        parts.append(current[cursor:])
        return "".join(parts)

    projected = value
    # Two levels cover a finite nested-image label followed by its outer
    # reference link.  A third pass must be stable; otherwise fail closed.
    for _ in range(2):
        updated = project_once(projected)
        if updated == projected:
            return projected
        projected = updated
    final = project_once(projected)
    if final != projected:
        raise ValueError("reference-link nesting exceeds the finite projection contract")
    return projected


def _kramdown_ial_attachment_kind(
    value: str,
    *,
    start: int,
    end: int,
    reference_labels: frozenset[str],
) -> str | None:
    """Return the finite rendered element that owns an adjacent IAL."""

    prefix = value[:start]
    suffix = value[end + 1 :]
    if _KRAMDOWN_BLOCK_IAL_PREFIX.fullmatch(prefix) and not suffix.strip():
        return "block"

    for code_start, code_end in _finite_same_line_code_spans(value):
        if code_end == start:
            return "code-span"

    for link in _finite_markdown_inline_links(
        value, location="Kramdown IAL attachment"
    ):
        if link.source_end == start:
            return "inline-link-or-image"

    for pattern in (
        _MARKDOWN_NESTED_INLINE_IMAGE_REFERENCE_LINK,
        _MARKDOWN_NESTED_IMAGE_REFERENCE_LINK,
        _MARKDOWN_REFERENCE_LINK,
    ):
        for match in pattern.finditer(value):
            if match.end() != start:
                continue
            references: list[str] = []
            for group_name in (
                "reference",
                "image_reference",
                "outer_reference",
            ):
                if group_name in match.re.groupindex:
                    references.append(match.group(group_name) or match.group("label"))
            if all(
                _normalized_markdown_reference_label(reference)
                in reference_labels
                for reference in references
            ):
                return "reference-link-or-image"

    for match in _MARKDOWN_SHORTCUT_REFERENCE_LINK.finditer(value):
        if match.end() == start and (
            _normalized_markdown_reference_label(match.group("label"))
            in reference_labels
        ):
            return "shortcut-reference-link-or-image"

    if _KRAMDOWN_FOOTNOTE_MARKER_TAIL.search(prefix):
        return "footnote-marker"
    if any(match.end() == start for match in _MARKDOWN_AUTOLINK_URL.finditer(value)):
        return "autolink"
    if _KRAMDOWN_ENTITY_TAIL.search(prefix):
        return "entity"

    if start:
        delimiter = value[start - 1]
        if delimiter in "*_" and not _markdown_character_is_escaped(value, start - 1):
            run_start = start - 1
            while run_start > 0 and value[run_start - 1] == delimiter:
                run_start -= 1
            width = start - run_start
            opening = delimiter * width
            candidate = value[:run_start]
            opening_index = candidate.rfind(opening)
            if (
                opening_index >= 0
                and not _markdown_character_is_escaped(candidate, opening_index)
                and candidate[opening_index + width :].strip()
            ):
                return "emphasis"
    return None


def _project_kramdown_attribute_lists(
    value: str,
    *,
    location: str,
    reference_labels: frozenset[str],
) -> str:
    """Project a finite, inert Kramdown IAL to its rendered text boundary.

    Pinned Kramdown 2.5.2 / GFM 1.1.0 removes a same-line ``{:...}``
    attribute list after a rendered span, and removes a block IAL line.  Such
    metadata must not split the text sent to Policy 1.2.0.  Chapter 4 permits
    only class/id shorthand aligned with the pinned parser; named attributes,
    ALD references, and generic extensions fail closed when they are attached
    to a rendered element or occupy a block IAL line.

    Inline code and Markdown destination/title spans are literal or separately
    owned metadata, so IAL-looking source inside them is not interpreted here.
    Text-adjacent and malformed shapes that pinned Kramdown leaves literal stay
    reader-visible.  Unknown attachment punctuation fails closed instead of
    being silently projected.  This is a finite renderer adapter, not a claim
    to implement the complete Kramdown parser.
    """

    protected = tuple(
        sorted(
            set(_finite_same_line_code_spans(value))
            | set(_finite_markdown_link_noncontent_spans(value))
        )
    )

    def protected_at(position: int) -> bool:
        return any(start <= position < end for start, end in protected)

    projected = list(value)
    cursor = 0
    while True:
        match = _KRAMDOWN_IAL_START.search(value, cursor)
        if match is None:
            break
        start = match.start()
        cursor = start + 2
        if protected_at(start) or _markdown_character_is_escaped(value, start):
            continue

        end = cursor
        while end < len(value) and value[end] not in "\r\n":
            if value[end] == "\\" and end + 1 < len(value) and value[end + 1] == "}":
                end += 2
                continue
            if value[end] == "}":
                break
            end += 1
        if end >= len(value) or value[end] != "}":
            # An unclosed shape is rendered literally and therefore is not
            # hidden metadata.  Leave it visible for the ordinary Policy path.
            continue

        body = value[start + 2 : end]
        attachment = _kramdown_ial_attachment_kind(
            value,
            start=start,
            end=end,
            reference_labels=reference_labels,
        )
        if attachment is None:
            # Kramdown warns and renders a span IAL literally when its previous
            # child is ordinary text.  A double-encoded entity is an entity
            # token followed by literal entity-name text, so its trailing
            # semicolon belongs to the same ordinary-text boundary.  Preserve
            # those exact reader-visible forms instead of treating the IAL as
            # hidden metadata.
            if start and (
                value[start - 1].isalnum()
                or ord(value[start - 1]) > 127
                or _KRAMDOWN_DOUBLE_ENCODED_ENTITY_LITERAL_TAIL.search(
                    value[:start]
                )
            ):
                cursor = end + 1
                continue
            raise ValueError(
                f"{location}: Kramdown attribute-list attachment is outside "
                "the finite Chapter 4 renderer contract"
            )
        if not _KRAMDOWN_SAFE_CLASS_ID_IAL_BODY.fullmatch(body):
            raise ValueError(
                f"{location}: Kramdown attribute lists are limited to finite "
                "class/id shorthand; named attributes, references, and "
                "extensions are disallowed"
            )
        projected[start : end + 1] = [""] * (end + 1 - start)
        cursor = end + 1
    return "".join(projected)


def _project_literal_inline_code(
    value: str,
    *,
    reference_labels: frozenset[str] = frozenset(),
    location: str = "reader-visible Markdown",
) -> str:
    """Keep reader-visible literal angle content Policy-visible.

    Actual raw HTML is rejected before this projection.  Finite Markdown link
    destinations and titles are blanked from the main field because they are
    metadata: destinations stay hidden and titles are selected separately.
    Every other literal angle delimiter is neutralized so the shared
    normalizer cannot discard the reader-visible content between it, including
    balanced and unbalanced bare prose and autolinks.  Host extraction still
    owns visible autolinks after masking finite Markdown link metadata.
    """

    ial_projected = _project_kramdown_attribute_lists(
        value,
        location=location,
        reference_labels=reference_labels,
    )
    reference_projected = _project_markdown_reference_link_labels(
        ial_projected,
        reference_labels=reference_labels,
    )
    inline_projected = _project_markdown_inline_link_labels(
        reference_projected,
        location=location,
    )
    emphasis_projected = _project_kramdown_underscore_emphasis(inline_projected)
    projected = list(emphasis_projected)
    for start, end in _finite_markdown_link_noncontent_spans(emphasis_projected):
        projected[start:end] = " " * (end - start)

    for start, end in _finite_same_line_code_spans(emphasis_projected):
        for position in range(start, end):
            if projected[position] in "<>":
                projected[position] = " "
    # Markdown-escaped angle brackets and encoded ``&lt;``/``&gt;`` forms are
    # reader-visible literal source.  Neutralize only their delimiters so a
    # displayed attribute value cannot be discarded by HTML normalization.
    index = 0
    while index + 1 < len(projected):
        if projected[index] == "\\" and projected[index + 1] in "<>":
            projected[index] = " "
            projected[index + 1] = " "
            index += 2
            continue
        index += 1
    for position, character in enumerate(projected):
        if character in "<>":
            projected[position] = " "
    return _neutralize_html_angle_entities("".join(projected))


def _project_literal_markdown_title(value: str) -> str:
    """Keep a rendered Markdown tooltip's literal tag-shaped text visible."""

    decoded = _neutralize_html_angle_entities(html.unescape(value))
    return decoded.replace("<", " ").replace(">", " ")


def _reject_interpreted_raw_html(value: str, *, location: str) -> None:
    """Reject raw HTML in an interpreted Chapter 4 Markdown surface.

    Raw HTML attributes can be rendered or accessibility-visible while the
    existing Markdown projection discards them.  The Chapter 4 publication
    contract therefore permits Markdown but no interpreted raw HTML.  This is
    fail-closed surface ownership, not a claim to parse arbitrary HTML.
    """

    candidate = list(_mask_finite_same_line_code_spans(value))
    for start, end in _finite_markdown_link_noncontent_spans(value):
        candidate[start:end] = " " * (end - start)
    candidate_text = "".join(candidate)
    for match in _RAW_HTML_TAG_OPENING.finditer(candidate_text):
        if _markdown_character_is_escaped(candidate_text, match.start()):
            continue
        raise ValueError(
            f"{location}: interpreted raw HTML is disallowed; use Markdown or "
            "reader-visible literal code"
        )


def _finite_inline_label_before_tail(
    value: str, closing_index: int
) -> tuple[int, str] | None:
    """Return source start/rendered label before one finite ``](`` tail."""

    if _markdown_character_is_escaped(value, closing_index):
        return None
    label_prefix = value[: closing_index + 1]
    direct = _MARKDOWN_DIRECT_LABEL_BEFORE_TAIL.search(label_prefix)
    if direct is not None:
        bracket_index = direct.start() + (1 if direct.group(0).startswith("!") else 0)
        if not _markdown_character_is_escaped(value, bracket_index):
            source_start = direct.start()
            rendered_label = direct.group("label")
            if direct.group("image") and _markdown_character_is_escaped(
                value, source_start
            ):
                # ``\![label](...)`` renders as a literal ``!`` followed by a
                # normal link.  Consume the escape and emit that rendered
                # prefix with the link label instead of leaking ``\``.
                source_start -= 1
                rendered_label = f"!{rendered_label}"
            return source_start, rendered_label
    nested = _MARKDOWN_NESTED_IMAGE_LABEL_BEFORE_TAIL.search(label_prefix)
    if nested is None or _markdown_character_is_escaped(value, nested.start()):
        return None
    return nested.start(), nested.group("label")


def _inline_link_title_fields(value: str, *, location: str) -> list[tuple[str, str]]:
    """Select same-line finite inline/image-link titles as rendered tooltips."""

    fields: list[tuple[str, str]] = []
    occurrence = 0
    for link in _finite_markdown_inline_links(value, location=location):
        occurrence += 1
        title = link.title
        if title is not None:
            visible_title = _project_literal_markdown_title(
                _markdown_title_value(title)
            )
            if visible_title:
                fields.append(
                    (f"{location}/inline-link-title[{occurrence}]", visible_title)
                )
    return fields


_INTERPRETED_LIQUID_OPENING = re.compile(r"\{\{|\{%")


def _reject_interpreted_liquid(value: str, *, location: str) -> None:
    """Reject Liquid before any Markdown projection or masking.

    Jekyll evaluates Liquid before Kramdown renders Markdown.  A Liquid tag can
    therefore remove source text and join two otherwise separated fragments,
    including inside a fence, Markdown table, or HTML comment.  Chapter 4 does
    not need executable Liquid, so the finite publication contract rejects both
    output and tag openers instead of attempting to emulate the Liquid runtime.
    Entity-encoded braces remain ordinary reader-visible text because Jekyll
    does not interpret them as Liquid delimiters.
    """

    match = _INTERPRETED_LIQUID_OPENING.search(value)
    if match is None:
        return
    line = value.count("\n", 0, match.start()) + 1
    line_start = value.rfind("\n", 0, match.start()) + 1
    column = match.start() - line_start + 1
    raise ValueError(
        f"{location}:{line}:{column}: interpreted Liquid syntax "
        f"{match.group(0)!r} is disallowed before Markdown publication"
    )


def reader_visible_markdown_fields(text: str, label: str) -> list[tuple[str, str]]:
    """Select rendered headings, prose, lists, and finite code-block contents.

    Table cells are owned by the finite table manifest.  A document contract
    that calls this adapter must therefore also call ``classified_table_fields``
    with its complete table manifest.  This adapter owns the remaining
    heading/prose/list/code surface without treating front matter, ordinary
    Markdown comments, link destinations, or ordinary link-reference definitions
    as reader instructions.  Footnote-definition bodies are selected because
    Kramdown/GFM renders them as reader-visible prose.  Fenced and
    four-space/tab-indented code are literal rendered source, so their delimiters
    are neutralized and their full contents are sent to shared Policy 1.2.0.
    Wrapped lines remain one field so action/object and negation context is not
    split at an authoring line break.
    """

    _reject_interpreted_liquid(text, location=label)
    source_lines = text.splitlines()
    selected: list[tuple[int, tuple[str, str]]] = []
    content_start = _front_matter_content_start(source_lines)
    reference_labels = _markdown_reference_definition_labels(
        "\n".join(source_lines[content_start:])
    )
    spans = _rendered_fence_spans(source_lines, start_index=content_start)
    fenced_lines = {
        index
        for span in spans
        for index in range(span.opening_index, span.closing_index + 1)
    }
    footnote_spans = _rendered_footnote_spans(
        source_lines,
        start_index=content_start,
        excluded_lines=fenced_lines,
    )
    footnote_lines = {
        index
        for span in footnote_spans
        for index in range(span.opening_index, span.closing_index + 1)
    }
    indented_spans = _rendered_indented_code_spans(
        source_lines,
        start_index=content_start,
        excluded_lines=fenced_lines | footnote_lines,
    )
    covered_lines = fenced_lines | footnote_lines | {
        index
        for span in indented_spans
        for index in range(span.opening_index, span.closing_index + 1)
    }
    tables, table_messages = markdown_tables(text, label)
    if table_messages:
        raise ValueError("; ".join(table_messages))
    table_lines = {
        index
        for table in tables
        for index in range(table.line - 1, table.end_line)
    }
    covered_lines |= table_lines
    renderable_lines = [
        (index + 1, "" if index in covered_lines else line)
        for index, line in enumerate(source_lines)
        if index >= content_start
    ]
    for span in spans:
        opening = span.opening
        language_label = opening.language or "plain"
        container = ""
        if opening.quote_depth or opening.container_indent:
            container = (
                f";quote={opening.quote_depth};indent={opening.container_indent}"
            )
        location = (
            f"{label}:{span.opening_index + 1}-{span.closing_index + 1} "
            f"fence[{language_label}/{opening.surface}{container}]"
        )
        for field in _literal_fence_visible_fields(
            "\n".join(span.content), location=location
        ):
            selected.append((span.opening_index + 1, field))
    for span in indented_spans:
        location = (
            f"{label}:{span.opening_index + 1}-{span.closing_index + 1} "
            f"indented-code[{span.indentation}]"
        )
        for field in _literal_fence_visible_fields(
            "\n".join(span.content), location=location
        ):
            selected.append((span.opening_index + 1, field))
    for span in footnote_spans:
        location = (
            f"{label}:{span.opening_index + 1}-{span.closing_index + 1} "
            f"footnote[{span.reference}]"
        )
        nested_code_spans = _rendered_indented_code_spans(
            list(span.content),
            start_index=0,
            excluded_lines=set(),
        )
        nested_code_lines = {
            index
            for code_span in nested_code_spans
            for index in range(code_span.opening_index, code_span.closing_index + 1)
        }
        footnote_table_source = "\n".join(
            "" if index in nested_code_lines else content_line
            for index, content_line in enumerate(span.content)
        )
        footnote_tables, footnote_table_messages = markdown_tables(
            footnote_table_source, location
        )
        if footnote_table_messages or footnote_tables:
            detail = (
                "; ".join(footnote_table_messages)
                if footnote_table_messages
                else "Markdown tables inside footnotes are outside the finite adapter contract"
            )
            raise ValueError(f"{location}: {detail}")

        for code_span in nested_code_spans:
            code_location = (
                f"{location}/indented-code[{code_span.indentation}]"
            )
            for field in _literal_fence_visible_fields(
                "\n".join(code_span.content), location=code_location
            ):
                selected.append(
                    (span.opening_index + code_span.opening_index + 1, field)
                )

        rendered_parts: list[str] = []
        visible_content_lines = _strip_html_comments(
            [
                (
                    span.opening_index + offset + 1,
                    "" if offset in nested_code_lines else content_line,
                )
                for offset, content_line in enumerate(span.content)
            ]
        )
        for physical_line, content_line in visible_content_lines:
            content_location = f"{location}/line[{physical_line}]"
            _reject_interpreted_raw_html(content_line, location=content_location)
            for field in _inline_link_title_fields(
                content_line, location=content_location
            ):
                selected.append((physical_line, field))
            projected = _project_literal_inline_code(
                content_line,
                reference_labels=reference_labels,
                location=content_location,
            ).strip()
            if projected:
                rendered_parts.append(projected)
        rendered = " ".join(rendered_parts).strip()
        if rendered:
            selected.append(
                (
                    span.opening_index + 1,
                    (location, rendered),
                )
            )

    lines = _strip_html_comments(renderable_lines)
    policy_lines: list[tuple[int, str]] = []
    for line_number, line in lines:
        _reject_interpreted_raw_html(
            line, location=f"{label}:{line_number}-{line_number}"
        )
        reference_prefix = _MARKDOWN_REFERENCE_DEFINITION_PREFIX.match(line)
        if reference_prefix:
            definition = _MARKDOWN_REFERENCE_DEFINITION.fullmatch(line)
            if definition is None:
                raise ValueError(
                    f"{label}:{line_number}: malformed Markdown reference definition"
                )
            title = definition.group("title")
            if title is not None:
                visible_title = _project_literal_markdown_title(
                    _markdown_title_value(title)
                )
                if visible_title:
                    selected.append(
                        (
                            line_number,
                            (
                                f"{label}:{line_number}-{line_number} reference-link-title",
                                visible_title,
                            ),
                        )
                    )
            elif line_number < len(source_lines):
                next_line = source_lines[line_number]
                if _MARKDOWN_CONTINUED_LINK_TITLE.fullmatch(next_line):
                    raise ValueError(
                        f"{label}:{line_number}-{line_number + 1}: multiline "
                        "Markdown reference title is outside the finite contract"
                    )
            policy_lines.append((line_number, line))
            continue
        for field in _inline_link_title_fields(
            line, location=f"{label}:{line_number}-{line_number}"
        ):
            selected.append((line_number, field))
        policy_lines.append(
            (
                line_number,
                _project_literal_inline_code(
                    line,
                    reference_labels=reference_labels,
                    location=f"{label}:{line_number}-{line_number}",
                ),
            )
        )
    lines = policy_lines
    index = 0

    def structural(line: str) -> bool:
        stripped = line.strip()
        return bool(
            not stripped
            or _MARKDOWN_HEADING.match(stripped)
            or _MARKDOWN_FENCE.match(line)
            or _MARKDOWN_REFERENCE_DEFINITION.fullmatch(line)
            or stripped in {"---", "***", "___"}
        )

    while index < len(lines):
        line_number, line = lines[index]
        stripped = line.strip()
        if line.startswith("    ") or line.startswith("\t"):
            index += 1
            continue
        heading_match = _MARKDOWN_HEADING.match(line)
        if heading_match:
            heading = re.sub(r"[ \t]+#+[ \t]*$", "", heading_match.group("body")).strip()
            if heading:
                selected.append(
                    (
                        line_number,
                        (f"{label}:{line_number}-{line_number} heading", heading),
                    )
                )
            index += 1
            continue
        if structural(line):
            index += 1
            continue

        list_match = _MARKDOWN_LIST_ITEM.match(line)
        kind = "list" if list_match else "paragraph"
        parts = [list_match.group("body").strip() if list_match else stripped]
        index += 1
        while index < len(lines):
            _, continuation = lines[index]
            if structural(continuation) or _MARKDOWN_LIST_ITEM.match(continuation):
                break
            if continuation.startswith("    ") and kind != "list":
                break
            parts.append(continuation.strip())
            index += 1
        end_line = lines[index - 1][0]
        rendered = " ".join(part for part in parts if part).strip()
        if rendered:
            selected.append(
                (
                    line_number,
                    (f"{label}:{line_number}-{end_line} {kind}", rendered),
                )
            )
    return [field for _, field in sorted(selected, key=lambda item: item[0])]


def _visible_idn_tokens(text: str) -> set[str]:
    """Extract bounded visible IDN candidates without scanning dotted prose.

    The shared Policy remains the authority for allow/deny decisions.  This
    adapter only selects an isolated token, or a token bounded by the finite
    Japanese topic/case-particle and sentence-ending forms used in reader
    prose.  It intentionally does not attempt general natural-language host
    parsing.
    """

    tokens: set[str] = set()
    for coarse_match in _VISIBLE_IDN_COARSE_TOKEN.finditer(text):
        candidate = coarse_match.group(0).rstrip(".:：")
        if "." not in candidate or not any(ord(character) > 127 for character in candidate):
            continue
        if _VISIBLE_ASCII_DOMAIN_TOKEN.search(candidate) or _VISIBLE_IP_TOKEN.search(candidate):
            continue
        if any(suffix in candidate.casefold() for suffix in (".example", ".test", ".invalid")):
            continue
        candidate = _VISIBLE_IDN_LEADING_JAPANESE.sub("", candidate)
        candidate = _VISIBLE_IDN_TRAILING_JAPANESE.sub("", candidate)
        if not candidate or _VISIBLE_DOTTED_VERSION.fullmatch(candidate):
            continue
        if not _VISIBLE_IDN_HOST.fullmatch(candidate):
            continue
        labels = candidate.split(".")
        if labels[-1][0].isdigit():
            continue
        if ord(labels[-1][0]) < 128 and (
            len(labels) != 2
            or not any(ord(character) > 127 for character in labels[0])
            or any(ord(character) > 127 for character in labels[-1])
        ):
            continue
        tokens.add(candidate)
    return tokens


def visible_host_tokens(text: str) -> tuple[str, ...]:
    """Return bounded visible URL/domain/IP tokens for the shared host Policy.

    ``normalize_visible_text`` removes Markdown link destinations before this
    extraction.  The separate autolink pass masks the same finite destination
    and title spans so an angle-bracket destination cannot masquerade as a
    visible autolink.  Scanning explicit tokens avoids treating dotted prose
    such as ``SP 800-30 Rev.1`` as a hostname while preserving visible bare
    hosts, URLs, and documentation/non-documentation address literals.
    """

    autolink_source = list(text)
    for start, end in _finite_markdown_link_noncontent_spans(text):
        autolink_source[start:end] = " " * (end - start)
    autolinks = {
        match.group("url")
        for match in _MARKDOWN_AUTOLINK_URL.finditer("".join(autolink_source))
    }
    visible = normalize_visible_text(text)
    tokens = {
        match.group(0).rstrip(".,;、。")
        for pattern in (_VISIBLE_URL_TOKEN, _VISIBLE_ASCII_DOMAIN_TOKEN, _VISIBLE_IP_TOKEN)
        for match in pattern.finditer(visible)
    }
    tokens.update(autolinks)
    tokens.update(_visible_idn_tokens(visible))
    return tuple(sorted(token for token in tokens if token))


def prose_policy_findings(fields: list[tuple[str, str]]) -> list[SafetyFinding]:
    findings: set[SafetyFinding] = set()
    for location, value in fields:
        findings.update(scan_action_text(value, location=location))
        for token in visible_host_tokens(value):
            findings.update(scan_host_policy(token, location=location))
    return sorted(
        findings,
        key=lambda finding: (
            finding.location,
            finding.category,
            finding.normalized_excerpt,
            finding.reason,
        ),
    )


def prose_policy_errors(fields: list[tuple[str, str]]) -> list[str]:
    return [format_finding(finding) for finding in prose_policy_findings(fields)]


def document_reader_visible_policy_errors(text: str, label: str) -> list[str]:
    try:
        fields = reader_visible_markdown_fields(text, label)
        return prose_policy_errors(fields)
    except (TypeError, ValueError, UnicodeError) as exc:
        return [f"{label}: reader-visible Markdown adapter failed closed: {exc}"]


def markdown_tables(text: str, label: str) -> tuple[list[MarkdownTable], list[str]]:
    """Parse every Markdown table in document order without guessing its semantics."""

    lines = text.splitlines()
    tables: list[MarkdownTable] = []
    messages: list[str] = []
    for index, line in enumerate(lines[:-1]):
        if not line.strip().startswith("|"):
            continue
        header = tuple(markdown_cells(line))
        separator = tuple(markdown_cells(lines[index + 1]))
        separator_candidate = bool(separator) and all(
            re.fullmatch(r":?-+:?", cell) for cell in separator
        )
        if not separator_candidate:
            continue
        if len(separator) != len(header) or not all(
            re.fullmatch(r":?-{3,}:?", cell) for cell in separator
        ):
            messages.append(
                f"{label}:{index + 1}: malformed Markdown table separator: "
                f"header={header!r}, separator={separator!r}"
            )
            continue
        if not header or any(not cell for cell in header) or len(header) != len(set(header)):
            messages.append(
                f"{label}:{index + 1}: malformed Markdown table header: {header!r}"
            )
            continue
        rows: list[tuple[str, ...]] = []
        end_index = index + 1
        for row_index, row_line in enumerate(lines[index + 2 :], start=index + 2):
            if not row_line.strip().startswith("|"):
                break
            end_index = row_index
            row = tuple(markdown_cells(row_line))
            if len(row) != len(header):
                messages.append(
                    f"{label}:{index + 1}: malformed safety-adapter row for {header!r}: {row!r}"
                )
                continue
            rows.append(row)
        tables.append(
            MarkdownTable(
                header=header,
                rows=tuple(rows),
                line=index + 1,
                end_line=end_index + 1,
            )
        )
    return tables, messages


def adapter_field_location(
    label: str,
    table: MarkdownTable,
    occurrence: int,
    column: str,
    row: int,
) -> str:
    return f"{label}:{table.line} {table.header[0]}[{occurrence}] {column} row {row}"


def is_frozen_inherited_nominal_descriptor(
    header: tuple[str, ...], row: tuple[str, ...], column: str, value: str
) -> bool:
    """Identify a source-exact, non-instructional inherited descriptor.

    Chapter 1 freezes TH-2026-003 Preconditions as the nominal historical
    phrase ``過去の不正Credential利用``.  The shared Policy correctly treats
    an unbounded ``Credential利用`` action as unsafe, but this exact table cell
    is source provenance rather than a reader action.  Keep the exception in
    this thin Chapter 4 adapter: any changed/appended value remains selected
    for Policy 1.2.0, and the source-derived structural contract independently
    requires the exact phrase.
    """

    return (
        header == HYPOTHESIS_HEADER
        and column == "Preconditions"
        and len(row) == len(header)
        and row[header.index("Hypothesis ID")].strip("`") == "TH-2026-003"
        and value == INHERITED_TH_003_PRECONDITIONS
    )


def classified_table_fields(
    text: str,
    label: str,
    expected_occurrences: dict[tuple[str, ...], int],
) -> tuple[list[tuple[str, str]], list[str]]:
    """Select all public fields through one finite Template/Case manifest.

    A new or renamed table/column cannot silently bypass Policy 1.2.0: the
    complete observed header inventory and its occurrence count must match the
    document-specific contract, and every column is explicitly classified.
    """

    tables, messages = markdown_tables(text, label)
    try:
        reference_labels = _markdown_reference_definition_labels(text)
    except (TypeError, ValueError, UnicodeError) as exc:
        messages.append(
            f"{label}: reference-definition adapter failed closed: {exc}"
        )
        reference_labels = frozenset()
    counts = Counter(table.header for table in tables)
    observed_headers = set(counts)
    expected_headers = set(expected_occurrences)
    for header in sorted(observed_headers - expected_headers):
        messages.append(f"{label}: unclassified public table header: {header!r}")
    for header in sorted(expected_headers - observed_headers):
        messages.append(f"{label}: missing classified public table header: {header!r}")
    for header, expected_count in expected_occurrences.items():
        if counts[header] != expected_count:
            messages.append(
                f"{label}: classified table occurrence count for {header!r} "
                f"is {counts[header]}, expected {expected_count}"
            )

    fields: list[tuple[str, str]] = []
    occurrences: Counter[tuple[str, ...]] = Counter()
    for table in tables:
        occurrences[table.header] += 1
        policy = TABLE_SAFETY_POLICIES.get(table.header)
        if policy is None or table.header not in expected_occurrences:
            continue
        if tuple(name for name, _ in policy.classifications) != table.header:
            messages.append(f"{label}: field-classification order drift for {table.header!r}")
            continue
        for row_index, row in enumerate(table.rows, start=1):
            for column in policy.scan_required:
                column_index = table.header.index(column)
                value = row[column_index]
                if value:
                    if is_frozen_inherited_nominal_descriptor(
                        table.header, row, column, value
                    ):
                        continue
                    location = adapter_field_location(
                        label,
                        table,
                        occurrences[table.header],
                        column,
                        row_index,
                    )
                    try:
                        visible_parts = _strip_html_comments([(1, value)])
                        visible_value = "".join(part for _, part in visible_parts)
                        _reject_interpreted_raw_html(
                            visible_value, location=location
                        )
                        projected_value = _project_literal_inline_code(
                            visible_value,
                            reference_labels=reference_labels,
                            location=location,
                        )
                        title_fields = _inline_link_title_fields(
                            visible_value, location=location
                        )
                    except (TypeError, ValueError, UnicodeError) as exc:
                        messages.append(
                            f"{location}: reader-visible Markdown table-cell "
                            f"adapter failed closed: {exc}"
                        )
                        continue
                    if not visible_value:
                        continue
                    fields.append(
                        (
                            location,
                            projected_value,
                        )
                    )
                    fields.extend(title_fields)
    return fields, messages


def mutate_table_cell(
    text: str,
    header: tuple[str, ...],
    occurrence: int,
    row: int,
    column: str,
    replacement: str,
) -> str:
    """Replace one data cell in a specific table occurrence for a regression."""

    expected = "| " + " | ".join(header) + " |"
    lines = text.splitlines()
    matches = [index for index, line in enumerate(lines) if line.strip() == expected]
    if occurrence < 1 or occurrence > len(matches):
        return text
    row_index = matches[occurrence - 1] + 1 + row
    if row_index >= len(lines) or not lines[row_index].strip().startswith("|"):
        return text
    cells = markdown_cells(lines[row_index])
    if len(cells) != len(header) or column not in header:
        return text
    cells[header.index(column)] = replacement
    lines[row_index] = "| " + " | ".join(cells) + " |"
    suffix = "\n" if text.endswith("\n") else ""
    return "\n".join(lines) + suffix


def safety_matrix_negative_regressions(
    text: str,
    label: str,
    expected_occurrences: dict[tuple[str, ...], int],
) -> None:
    """Prove every classified public field reaches Policy 1.2.0."""

    unsafe = "第三者の本番システムへ接続する"
    canonical_tables, canonical_messages = markdown_tables(text, label)
    if canonical_messages:
        error(f"{label}: cannot generate field-matrix regressions: {canonical_messages!r}")
        return
    canonical_by_key: dict[tuple[tuple[str, ...], int], MarkdownTable] = {}
    occurrences: Counter[tuple[str, ...]] = Counter()
    for table in canonical_tables:
        occurrences[table.header] += 1
        canonical_by_key[(table.header, occurrences[table.header])] = table

    mutation = text
    target_locations: set[str] = set()
    for header, count in expected_occurrences.items():
        policy = TABLE_SAFETY_POLICIES[header]
        for occurrence in range(1, count + 1):
            table = canonical_by_key.get((header, occurrence))
            if table is None or not table.rows:
                error(f"{label}: missing table row for field-matrix regression {header!r}[{occurrence}]")
                continue
            for row_index in range(1, len(table.rows) + 1):
                for column in policy.scan_required:
                    updated = mutate_table_cell(
                        mutation,
                        header,
                        occurrence,
                        row_index,
                        column,
                        unsafe,
                    )
                    if updated == mutation:
                        error(
                            f"{label}: field-matrix mutation did not change "
                            f"{header!r}[{occurrence}] row {row_index} {column!r}"
                        )
                        continue
                    mutation = updated
                    target_locations.add(
                        adapter_field_location(
                            f"negative {label}", table, occurrence, column, row_index
                        )
                    )
    fields, adapter_messages = classified_table_fields(
        mutation, f"negative {label}", expected_occurrences
    )
    if adapter_messages:
        error(f"{label}: field-matrix mutation invalidated adapter structure: {adapter_messages!r}")
        return
    finding_locations = {finding.location for finding in scan_fields(fields)}
    missing = sorted(target_locations - finding_locations)
    if missing:
        error(f"{label}: public fields bypassed Policy 1.2.0: {missing!r}")


def prose_surface_negative_regressions(
    text: str,
    label: str,
    targets: tuple[tuple[str, str], ...],
) -> None:
    """Prove representative paragraph/list locations reach the shared Policy."""

    unsafe = "第三者の本番システムへ接続する。"
    safe = "第三者の本番システムへ接続しない。"
    for name, needle in targets:
        if text.count(needle) != 1:
            error(f"{label}: prose regression target {name!r} must occur exactly once")
            continue
        unsafe_text = text.replace(needle, f"{needle} {unsafe}", 1)
        unsafe_fields = reader_visible_markdown_fields(unsafe_text, f"negative {label} {name}")
        unsafe_findings = prose_policy_findings(unsafe_fields)
        if not any(
            finding.category == "target.real_or_external"
            and "第三者の本番システムへ接続する" in finding.normalized_excerpt
            for finding in unsafe_findings
        ):
            error(f"{label}: prose/list location bypassed Policy 1.2.0: {name}")

        safe_text = text.replace(needle, f"{needle} {safe}", 1)
        safe_fields = reader_visible_markdown_fields(safe_text, f"safe {label} {name}")
        safe_findings = prose_policy_findings(safe_fields)
        if safe_findings:
            error(
                f"{label}: safe prose/list counterpart produced findings for {name}: "
                f"{[format_finding(finding) for finding in safe_findings]!r}"
            )


def pipe_prefixed_prose_surface_regressions(
    text: str,
    label: str,
    contract_errors: Callable[[str, str], list[str]],
) -> None:
    """Prove a pipe-prefixed non-table line cannot bypass Policy 1.2.0."""

    suffix = "" if not text or text.endswith("\n") else "\n"
    unsafe = f"{text}{suffix}\n| 第三者の本番システムへ接続する。\n"
    unsafe_errors = contract_errors(unsafe, f"negative {label} pipe-prefixed prose")
    if not any(
        "[target.real_or_external]" in message
        and "第三者の本番システムへ接続する" in message
        for message in unsafe_errors
    ):
        error(f"{label}: pipe-prefixed reader prose bypassed Policy 1.2.0")

    safe = f"{text}{suffix}\n| 第三者の本番システムへ接続しない。\n"
    safe_errors = contract_errors(safe, f"safe {label} pipe-prefixed prose")
    if safe_errors:
        error(
            f"{label}: safe pipe-prefixed reader prose was rejected: {safe_errors!r}"
        )


def liquid_surface_regressions(
    text: str,
    label: str,
    contract_errors: Callable[[str, str], list[str]],
) -> None:
    """Prove Liquid cannot alter a Chapter 4 publication before Policy scan."""

    suffix = "" if not text or text.endswith("\n") else "\n"
    probes = (
        (
            "comment splice in prose",
            "第三者の{% comment %}hidden{% endcomment %}本番システムへ接続する。",
            "{%",
        ),
        (
            "whitespace-control tag in a table cell",
            "| Probe | 第三者の{%- comment -%}hidden{%- endcomment -%}本番システムへ接続する。 |",
            "{%",
        ),
        (
            "output splice in prose",
            '第三者の{{ "本番" }}システムへ接続する。',
            "{{",
        ),
        (
            "whitespace-control output in fenced source",
            '```text\n第三者の{{- "本番" -}}システムへ接続する。\n```',
            "{{",
        ),
        (
            "output inside an HTML comment",
            '<!-- 第三者の{{ "本番" }}システムへ接続する。 -->',
            "{{",
        ),
    )
    for name, probe, opener in probes:
        failures = contract_errors(
            f"{text}{suffix}\n{probe}\n",
            f"negative {label} Liquid {name}",
        )
        if not any(
            "interpreted Liquid syntax" in failure
            and repr(opener) in failure
            for failure in failures
        ):
            error(f"{label}: interpreted Liquid {name} did not fail closed")

    # Entity-encoded braces are emitted as ordinary reader-visible text and do
    # not form a Liquid delimiter during Jekyll's pre-Markdown Liquid pass.
    encoded_literal = (
        "Liquid delimiter example: &#123;&#123; value &#125;&#125; and "
        "&#123;% comment %&#125;."
    )
    failures = contract_errors(
        f"{text}{suffix}\n{encoded_literal}\n",
        f"safe {label} entity-encoded Liquid delimiter",
    )
    if failures:
        error(
            f"{label}: entity-encoded Liquid near-miss was rejected: {failures!r}"
        )


def raw_html_surface_regressions(
    text: str,
    label: str,
    contract_errors: Callable[[str, str], list[str]],
) -> None:
    """Prove Chapter 4 rejects interpreted raw HTML on every document surface."""

    suffix = "" if not text or text.endswith("\n") else "\n"
    for name, probe in (
        (
            "unsafe title attribute",
            '<span title="第三者の本番システムへ接続する">safe</span>',
        ),
        (
            "safe title attribute",
            "<span title='第三者の本番システムへ接続しない'>safe</span>",
        ),
        (
            "accessibility label",
            '<span aria-label="第三者の本番システムへ接続する">safe</span>',
        ),
        (
            "malformed unquoted attribute",
            "<span title=第三者の本番システムへ接続する",
        ),
    ):
        failures = contract_errors(
            f"{text}{suffix}\n{probe}\n",
            f"negative {label} raw HTML {name}",
        )
        if not any("interpreted raw HTML is disallowed" in failure for failure in failures):
            error(f"{label}: interpreted raw HTML {name} did not fail closed")

    for name, probe in (
        (
            "escaped literal attribute",
            '\\<span title="第三者の本番システムへ接続する"\\>safe\\</span\\>',
        ),
        (
            "entity-encoded literal attribute",
            '&lt;span title="第三者の本番システムへ接続する"&gt;safe&lt;/span&gt;',
        ),
    ):
        failures = contract_errors(
            f"{text}{suffix}\n{probe}\n",
            f"negative {label} {name}",
        )
        if not any(
            "[target.real_or_external]" in failure
            and "第三者の本番システムへ接続する" in failure
            for failure in failures
        ):
            error(f"{label}: {name} bypassed Policy 1.2.0")

    # Escaped tag syntax and finite inline code are literal reader content, not
    # interpreted HTML.  A locally prohibited phrase must remain safe.
    for name, probe in (
        (
            "escaped literal",
            '\\<span title="第三者の本番システムへ接続しない"\\>safe\\</span\\>',
        ),
        (
            "inline-code literal",
            '`<span title="第三者の本番システムへ接続しない">safe</span>`',
        ),
        (
            "entity-encoded literal",
            '&lt;span title="第三者の本番システムへ接続しない"&gt;safe&lt;/span&gt;',
        ),
        ("approved autolink", "<https://lab.example/runbook>"),
        ("angle-bracket Markdown destination", "[runbook](<local/path>)"),
        ("tag-like Markdown destination", "[runbook](<note>)"),
        (
            "tag-like reference destination",
            "[runbook][ref]\n\n[ref]: <foo-bar>",
        ),
    ):
        failures = contract_errors(
            f"{text}{suffix}\n{name}: {probe}\n",
            f"safe {label} raw HTML near-miss {name}",
        )
        if failures:
            error(f"{label}: raw HTML near-miss {name} was rejected: {failures!r}")


def bare_angle_surface_regressions(
    text: str,
    label: str,
    contract_errors: Callable[[str, str], list[str]],
) -> None:
    """Fix the finite reader-visible bare-angle projection contract.

    Kramdown/GFM preserves non-tag, non-autolink angle-bracket source for the
    reader.  Balanced and malformed literal delimiters must therefore not let
    the shared HTML-aware normalizer discard the enclosed instruction.  Link
    destinations remain metadata, while autolink hosts retain their dedicated
    host-policy handling.
    """

    suffix = "" if not text or text.endswith("\n") else "\n"
    for name, probe in (
        ("balanced literal", "<第三者の本番システムへ接続する>"),
        ("unclosed opening literal", "<第三者の本番システムへ接続する"),
        ("unmatched closing literal", "第三者の本番システムへ接続する>"),
    ):
        failures = contract_errors(
            f"{text}{suffix}\n{probe}\n",
            f"negative {label} bare angle {name}",
        )
        if not any(
            "[target.real_or_external]" in failure
            and "第三者の本番システムへ接続する" in failure
            for failure in failures
        ):
            error(f"{label}: unsafe bare angle {name} bypassed Policy 1.2.0")

    for name, probe in (
        (
            "explicit prohibition",
            "<第三者の本番システムへ接続することを禁止する>",
        ),
        ("explicit negative", "<第三者の本番システムへ接続しない>"),
        (
            "literal explanation",
            "この記号列 <表示用literal> は表示形式の説明である。",
        ),
        ("ordinary comparison", "値 < threshold > lower boundを比較する。"),
        ("approved autolink", "<https://lab.example/runbook>"),
        (
            "hidden angle destination",
            "[runbook](<第三者の本番システムへ接続する>)",
        ),
        (
            "hidden angle URL destination",
            "[runbook](<https://example.com/runbook>)",
        ),
        (
            "unclosed safe literal",
            "<第三者の本番システムへ接続しない",
        ),
        (
            "unmatched safe closing literal",
            "第三者の本番システムへ接続しない>",
        ),
    ):
        failures = contract_errors(
            f"{text}{suffix}\n{probe}\n",
            f"safe {label} bare angle {name}",
        )
        if failures:
            error(f"{label}: safe bare angle {name} was rejected: {failures!r}")

    disallowed_autolink = contract_errors(
        f"{text}{suffix}\n<https://example.com/runbook>\n",
        f"negative {label} disallowed autolink host",
    )
    if not any(
        "[network.host_or_address]" in failure
        and "non-approved host suffix" in failure
        for failure in disallowed_autolink
    ):
        error(f"{label}: non-approved autolink host bypassed Policy 1.2.0")


def angle_entity_surface_regressions(
    text: str,
    label: str,
    contract_errors: Callable[[str, str], list[str]],
) -> None:
    """Keep finite semicolonless angle-reference bodies Policy-visible.

    Pinned Kramdown/GFM leaves the semicolonless forms below as escaped,
    reader-visible entity-like source, while Python ``html.unescape()`` accepts
    them as angle delimiters.  Every canonical Chapter 4 document adapter must
    preserve the body through that renderer/decoder difference.
    """

    suffix = "" if not text or text.endswith("\n") else "\n"
    unsafe = "第三者の本番システムへ接続する"
    safe = "第三者の本番システムへ接続しない"
    for name, opening, closing in (
        ("decimal", "&#60", "&#62"),
        ("hex lowercase", "&#x3c", "&#x3e"),
        ("hex uppercase", "&#X3C", "&#X3E"),
        ("named", "&lt", "&gt"),
        ("named uppercase", "&LT", "&GT"),
    ):
        failures = contract_errors(
            f"{text}{suffix}\n{opening}{unsafe}{closing}\n",
            f"negative {label} semicolonless angle entity {name}",
        )
        if not any(
            "[target.real_or_external]" in failure and unsafe in failure
            for failure in failures
        ):
            error(
                f"{label}: unsafe semicolonless angle entity {name} bypassed "
                "Policy 1.2.0"
            )

        safe_failures = contract_errors(
            f"{text}{suffix}\n{opening}{safe}{closing}\n",
            f"safe {label} semicolonless angle entity {name}",
        )
        if safe_failures:
            error(
                f"{label}: safe semicolonless angle entity {name} was rejected: "
                f"{safe_failures!r}"
            )


def reference_link_label_surface_regressions(
    text: str,
    label: str,
    contract_errors: Callable[[str, str], list[str]],
) -> None:
    """Bind rendered reference links to labels, not hidden identifiers."""

    suffix = "" if not text or text.endswith("\n") else "\n"
    unsafe = "第三者の本番システムへ接続する"
    safe = "第三者の本番システムへ接続しない"
    for name, unsafe_link, safe_link, definition in (
        (
            "full",
            "第三者の[本番][ch04-full-ref]システムへ接続する",
            "第三者の[本番][ch04-full-ref]システムへ接続しない",
            "[ch04-full-ref]: /local",
        ),
        (
            "collapsed",
            "第三者の[本番][]システムへ接続する",
            "第三者の[本番][]システムへ接続しない",
            "[本番]: /local",
        ),
        (
            "shortcut",
            "第三者の[本番]システムへ接続する",
            "第三者の[本番]システムへ接続しない",
            "[本番]: /local",
        ),
        (
            "image alt",
            "第三者の![本番][ch04-image-ref]システムへ接続する",
            "第三者の![本番][ch04-image-ref]システムへ接続しない",
            "[ch04-image-ref]: /local",
        ),
        (
            "mixed inline-image outer reference",
            "第三者の[![本番](/asset)][ch04-outer-ref]システムへ接続する",
            "第三者の[![本番](/asset)][ch04-outer-ref]システムへ接続しない",
            "[ch04-outer-ref]: /local",
        ),
        (
            "mixed inline-image outer inline link",
            "第三者の[![本番](/asset)](/local)システムへ接続する",
            "第三者の[![本番](/asset)](/local)システムへ接続しない",
            "[unrelated-inline-ref]: /elsewhere",
        ),
        (
            "mixed inline-image collapsed near-miss",
            "第三者の[![本番](/asset)][]システムへ接続する",
            "第三者の[![本番](/asset)][]システムへ接続しない",
            "[unrelated-collapsed-ref]: /local",
        ),
        (
            "mixed inline-image shortcut near-miss",
            "第三者の[![本番](/asset)]システムへ接続する",
            "第三者の[![本番](/asset)]システムへ接続しない",
            "[unrelated-shortcut-ref]: /local",
        ),
    ):
        failures = contract_errors(
            f"{text}{suffix}\n{unsafe_link}\n\n{definition}\n",
            f"negative {label} rendered reference-link label {name}",
        )
        if not any(
            "[target.real_or_external]" in failure and unsafe in failure
            for failure in failures
        ):
            error(
                f"{label}: unsafe rendered reference-link label {name} "
                "bypassed Policy 1.2.0"
            )

        safe_failures = contract_errors(
            f"{text}{suffix}\n{safe_link}\n\n{definition}\n",
            f"safe {label} rendered reference-link label {name}",
        )
        if safe_failures:
            error(
                f"{label}: safe rendered reference-link label {name} was "
                f"rejected: {safe_failures!r}"
            )

    hidden_identifier = "第三者の本番システムへ接続する"
    hidden_failures = contract_errors(
        f"{text}{suffix}\n[安全な表示][{hidden_identifier}]\n\n"
        f"[{hidden_identifier}]: /local\n",
        f"safe {label} hidden reference identifier",
    )
    if hidden_failures:
        error(
            f"{label}: hidden reference identifier became Policy-visible: "
            f"{hidden_failures!r}"
        )


def inline_link_label_surface_regressions(
    text: str,
    label: str,
    contract_errors: Callable[[str, str], list[str]],
) -> None:
    """Bind finite inline links/images to pinned Kramdown rendered labels.

    A zero-text anchor or empty image alt disappears from the reader-visible
    surface.  A non-empty label/alt remains exactly once.  This prevents link
    metadata from separating protected prose that the published renderer joins.
    """

    suffix = "" if not text or text.endswith("\n") else "\n"
    unsafe_rendered = "第三者の本番システムへ接続する"
    unsafe_cases = (
        ("empty link", "第三者の[](/local)本番システムへ接続する"),
        (
            "empty link with destination whitespace",
            "第三者の[](  /local  )本番システムへ接続する",
        ),
        (
            "empty link with angle destination",
            "第三者の[](<local/path>)本番システムへ接続する",
        ),
        (
            "empty link with title",
            '第三者の[](/local "tooltip")本番システムへ接続する',
        ),
        ("non-empty link", "第三者の[本番](/local)システムへ接続する"),
        ("empty image alt", "第三者の![](/asset)本番システムへ接続する"),
        (
            "non-empty image alt",
            "第三者の![本番](/asset)システムへ接続する",
        ),
        (
            "nested empty image alt",
            "第三者の[![](/asset)](/local)本番システムへ接続する",
        ),
        (
            "nested non-empty image alt",
            "第三者の[![本番](/asset)](/local)システムへ接続する",
        ),
    )
    # Bind each canonical Chapter/Template/Case contract to the repaired
    # projection once.  The full finite shape matrix is tested below through
    # the shared reader-visible adapter so this regression remains bounded.
    contract_unsafe = unsafe_cases[0][1]
    contract_failures = contract_errors(
        f"{text}{suffix}\n{contract_unsafe}\n",
        f"negative {label} rendered inline-link label",
    )
    if not any(
        "[target.real_or_external]" in failure
        and unsafe_rendered in re.sub(r"\s+", "", failure)
        for failure in contract_failures
    ):
        error(
            f"{label}: canonical contract did not scan joined empty-link text: "
            f"{contract_failures!r}"
        )
    contract_safe_failures = contract_errors(
        f"{text}{suffix}\n{contract_unsafe.replace('接続する', '接続しない')}\n",
        f"safe {label} rendered inline-link label",
    )
    if contract_safe_failures:
        error(
            f"{label}: canonical contract rejected safe joined empty-link text: "
            f"{contract_safe_failures!r}"
        )

    for name, unsafe_source in unsafe_cases:
        failures = document_reader_visible_policy_errors(
            f"{unsafe_source}\n",
            f"negative {label} rendered inline-link label {name}",
        )
        if not any(
            "[target.real_or_external]" in failure
            and unsafe_rendered in re.sub(r"\s+", "", failure)
            for failure in failures
        ):
            error(
                f"{label}: unsafe rendered inline-link label {name} bypassed "
                f"Policy 1.2.0: {failures!r}"
            )

        safe_failures = document_reader_visible_policy_errors(
            f"{unsafe_source.replace('接続する', '接続しない')}\n",
            f"safe {label} rendered inline-link label {name}",
        )
        if safe_failures:
            error(
                f"{label}: safe rendered inline-link label {name} was "
                f"rejected: {safe_failures!r}"
            )

    projection_cases = (
        ("[](/local)", ""),
        ("[](  /local  )", ""),
        ("[](<local/path>)", ""),
        ('[](/local "tooltip")', ""),
        ("[本番](/local)", "本番"),
        ("![](/asset)", ""),
        ("![本番](/asset)", "本番"),
        (r"\![](/asset)", "!"),
        (r"\![本番](/asset)", "!本番"),
        ("[![](/asset)](/local)", ""),
        ("[![本番](/asset)](/local)", "本番"),
    )
    for source, expected in projection_cases:
        projected = _project_markdown_inline_link_labels(
            source,
            location=f"{label} direct inline-link projection",
        )
        if projected != expected:
            error(
                f"{label}: inline-link rendered-label projection drifted: "
                f"{source!r} -> {projected!r} != {expected!r}"
            )

    escaped_and_code_safe = (
        r"第三者の\[](/local)本番システムへ接続しない",
        r"第三者の[本番\](/local)システムへ接続しない",
        "第三者の`[](/local)`本番システムへ接続しない",
    )
    for source in escaped_and_code_safe:
        projected = _project_markdown_inline_link_labels(
            source,
            location=f"{label} literal inline-link near-miss",
        )
        if projected != source:
            error(
                f"{label}: escaped/code inline-link near-miss was projected: "
                f"{source!r} -> {projected!r}"
            )
        failures = document_reader_visible_policy_errors(
            f"{source}\n",
            f"safe {label} literal inline-link near-miss",
        )
        if failures:
            error(
                f"{label}: escaped/code inline-link near-miss was rejected: "
                f"{source!r} / {failures!r}"
            )

    for source in (
        r"第三者の\![](/asset)本番システムへ接続しない",
        r"第三者の\![本番](/asset)システムへ接続しない",
    ):
        failures = document_reader_visible_policy_errors(
            f"{source}\n",
            f"safe {label} escaped image opener",
        )
        if failures:
            error(
                f"{label}: pinned-renderer escaped image opener was rejected: "
                f"{source!r} / {failures!r}"
            )

    try:
        _project_markdown_inline_link_labels(
            "第三者の[](/local本番システムへ接続しない",
            location=f"{label} malformed inline-link shape",
        )
    except ValueError:
        pass
    else:
        error(f"{label}: malformed inline-link shape did not fail closed")

    for source in (
        r"[\![](/asset)](/local)",
        r"[\![本番](/asset)](/local)",
    ):
        try:
            _project_markdown_inline_link_labels(
                source,
                location=f"{label} escaped nested-image near-miss",
            )
        except ValueError:
            pass
        else:
            error(
                f"{label}: escaped nested-image shape was partially projected "
                f"instead of failing closed: {source!r}"
            )

    title_failures = document_reader_visible_policy_errors(
        f'[安全な表示](/local "{unsafe_rendered}")\n',
        f"negative {label} inline-link title",
    )
    if not any(
        "[target.real_or_external]" in failure
        and "inline-link-title" in failure
        for failure in title_failures
    ):
        error(
            f"{label}: unsafe inline-link title was not selected separately: "
            f"{title_failures!r}"
        )

    hidden_destination_failures = document_reader_visible_policy_errors(
        "[安全な表示](/第三者の本番システムへ接続する)\n",
        f"safe {label} hidden inline-link destination",
    )
    if hidden_destination_failures:
        error(
            f"{label}: hidden inline-link destination became Policy-visible: "
            f"{hidden_destination_failures!r}"
        )

    rendered_table = (
        "| Field | Value |\n|---|---|\n"
        "| row | 第三者の[](/local)本番システムへ接続する |\n"
    )
    table_fields, table_messages = classified_table_fields(
        rendered_table,
        f"negative {label} rendered empty-link table fixture",
        {FIELD_VALUE_HEADER: 1},
    )
    table_findings = policy_errors(table_fields)
    if table_messages or len(
        [
            finding
            for finding in table_findings
            if "[target.real_or_external]" in finding
            and unsafe_rendered in re.sub(r"\s+", "", finding)
        ]
    ) != 1:
        error(
            f"{label}: rendered empty-link table text was not scanned exactly "
            f"once: {table_messages!r} / {table_findings!r}"
        )


def kramdown_underscore_emphasis_surface_regressions(
    text: str,
    label: str,
    contract_errors: Callable[[str, str], list[str]],
) -> None:
    """Bind finite underscore emphasis to its pinned rendered text."""

    suffix = "" if not text or text.endswith("\n") else "\n"
    unsafe = "第三者の本番システムへ接続する"
    for name, unsafe_source, safe_source in (
        (
            "emphasis",
            "第三者の _本番_ システムへ接続する",
            "第三者の _本番_ システムへ接続しない",
        ),
        (
            "strong",
            "第三者の __本番__ システムへ接続する",
            "第三者の __本番__ システムへ接続しない",
        ),
        (
            "strong-emphasis",
            "第三者の ___本番___ システムへ接続する",
            "第三者の ___本番___ システムへ接続しない",
        ),
        (
            "mixed-width strong/emphasis",
            "第三者の ___本番__ システムへ接続する_",
            "第三者の ___本番__ システムへ接続しない_",
        ),
    ):
        failures = contract_errors(
            f"{text}{suffix}\n{unsafe_source}\n",
            f"negative {label} rendered underscore {name}",
        )
        if not any(
            "[target.real_or_external]" in failure
            and unsafe in re.sub(r"\s+", "", failure)
            for failure in failures
        ):
            error(
                f"{label}: unsafe rendered underscore {name} bypassed "
                "Policy 1.2.0"
            )

        safe_failures = contract_errors(
            f"{text}{suffix}\n{safe_source}\n",
            f"safe {label} rendered underscore {name}",
        )
        if safe_failures:
            error(
                f"{label}: safe rendered underscore {name} was rejected: "
                f"{safe_failures!r}"
            )


def kramdown_ial_surface_regressions(
    text: str,
    label: str,
    contract_errors: Callable[[str, str], list[str]],
) -> None:
    """Keep inert Kramdown class/id metadata from splitting rendered prose."""

    suffix = "" if not text or text.endswith("\n") else "\n"
    unsafe = "第三者の本番システムへ接続する"
    for name, unsafe_source, safe_source, tail in (
        (
            "emphasis",
            "第三者の*本番*{:.ch04-probe}システムへ接続する",
            "第三者の*本番*{:.ch04-probe}システムへ接続しない",
            "",
        ),
        (
            "strong",
            "第三者の**本番**{:#foo:bar}システムへ接続する",
            "第三者の**本番**{:#foo:bar}システムへ接続しない",
            "",
        ),
        (
            "code",
            "第三者の`本番`{:.1probe}システムへ接続する",
            "第三者の`本番`{:.1probe}システムへ接続しない",
            "",
        ),
        (
            "inline link",
            "第三者の[本番](/local){:.ch04-probe}システムへ接続する",
            "第三者の[本番](/local){:.ch04-probe}システムへ接続しない",
            "",
        ),
        (
            "reference link",
            "第三者の[本番][ch04-ial-ref]{:.ch04-probe}システムへ接続する",
            "第三者の[本番][ch04-ial-ref]{:.ch04-probe}システムへ接続しない",
            "\n[ch04-ial-ref]: /local",
        ),
        (
            "image alt",
            "第三者の![本番](/asset){:.ch04-probe}システムへ接続する",
            "第三者の![本番](/asset){:.ch04-probe}システムへ接続しない",
            "",
        ),
        (
            "footnote",
            "Reader note[^ial].\n\n[^ial]: 第三者の*本番*{:.ch04-probe}システムへ接続する",
            "Reader note[^ial].\n\n[^ial]: 第三者の*本番*{:.ch04-probe}システムへ接続しない",
            "",
        ),
        (
            "block IAL",
            "第三者の本番システムへ接続する\n{: .ch04-probe}",
            "第三者の本番システムへ接続しない\n{: .ch04-probe}",
            "",
        ),
        (
            "blockquote block IAL",
            "> 第三者の本番システムへ接続する\n> {: .ch04-probe}",
            "> 第三者の本番システムへ接続しない\n> {: .ch04-probe}",
            "",
        ),
        (
            "list-item block IAL",
            "- 第三者の本番システムへ接続する\n  {: .ch04-probe}",
            "- 第三者の本番システムへ接続しない\n  {: .ch04-probe}",
            "",
        ),
    ):
        failures = contract_errors(
            f"{text}{suffix}\n{unsafe_source}{tail}\n",
            f"negative {label} Kramdown IAL {name}",
        )
        if not any(
            "[target.real_or_external]" in failure and unsafe in failure
            for failure in failures
        ):
            error(
                f"{label}: unsafe rendered Kramdown IAL {name} bypassed "
                "Policy 1.2.0"
            )

        safe_failures = contract_errors(
            f"{text}{suffix}\n{safe_source}{tail}\n",
            f"safe {label} Kramdown IAL {name}",
        )
        if safe_failures:
            error(
                f"{label}: safe rendered Kramdown IAL {name} was rejected: "
                f"{safe_failures!r}"
            )


def inline_code_comment_surface_regressions(
    text: str,
    label: str,
    contract_errors: Callable[[str, str], list[str]],
) -> None:
    """Keep HTML-comment-shaped source inside inline code reader-visible."""

    suffix = "" if not text or text.endswith("\n") else "\n"
    for name, probe in (
        (
            "balanced comment literal",
            "`<!--第三者の本番システムへ接続する。-->`",
        ),
        (
            "unclosed comment literal",
            "`<!--第三者の本番システムへ接続する。`",
        ),
    ):
        failures = contract_errors(
            f"{text}{suffix}\n{probe}\n",
            f"negative {label} inline-code {name}",
        )
        if not any(
            "[target.real_or_external]" in failure
            and "第三者の本番システムへ接続する" in failure
            for failure in failures
        ):
            error(
                f"{label}: HTML-comment-shaped {name} bypassed Policy 1.2.0"
            )

    for name, probe in (
        (
            "safe comment literal",
            "`<!--第三者の本番システムへ接続しない。-->`",
        ),
        (
            "actual non-rendered comment",
            "<!-- `第三者の本番システムへ接続する。` -->",
        ),
    ):
        failures = contract_errors(
            f"{text}{suffix}\n{probe}\n",
            f"safe {label} inline-code {name}",
        )
        if failures:
            error(
                f"{label}: inline-code/comment precedence rejected {name}: "
                f"{failures!r}"
            )


def markdown_title_comment_surface_regressions(
    text: str,
    label: str,
    contract_errors: Callable[[str, str], list[str]],
) -> None:
    """Keep comment-shaped rendered Markdown titles Policy-visible.

    Kramdown/GFM emits the finite title literal as escaped tooltip text.  The
    document-level adapters must therefore reject an unsafe title while actual
    comments and hidden destinations remain outside reader-action scanning.
    """

    suffix = "" if not text or text.endswith("\n") else "\n"
    unsafe = '[safe](/local "<!--第三者の本番システムへ接続する。-->")'
    failures = contract_errors(
        f"{text}{suffix}\n{unsafe}\n",
        f"negative {label} comment-shaped Markdown title",
    )
    if not any(
        "[target.real_or_external]" in failure
        and "inline-link-title" in failure
        and "第三者の本番システムへ接続する" in failure
        for failure in failures
    ):
        error(
            f"{label}: unsafe comment-shaped Markdown title bypassed "
            "Policy 1.2.0"
        )

    for name, probe in (
        (
            "explicit prohibition title",
            '[safe](/local "<!--第三者の本番システムへ接続することを禁止する。-->")',
        ),
        (
            "actual non-rendered comment",
            '<!-- [safe](/local "第三者の本番システムへ接続する。") -->',
        ),
        (
            "hidden destination",
            '[safe](https://example.com/runbook "<!--表示用tooltip。-->")',
        ),
    ):
        safe_failures = contract_errors(
            f"{text}{suffix}\n{probe}\n",
            f"safe {label} comment-shaped Markdown title {name}",
        )
        if safe_failures:
            error(
                f"{label}: Markdown title/comment precedence rejected "
                f"{name}: {safe_failures!r}"
            )


def multiline_inline_code_surface_regressions(
    text: str,
    label: str,
    contract_errors: Callable[[str, str], list[str]],
) -> None:
    """Reject unsupported multiline code spans before comment removal."""

    suffix = "" if not text or text.endswith("\n") else "\n"
    failures = contract_errors(
        f"{text}{suffix}\n`<!--第三者の本番システムへ接続する。\n-->`\n",
        f"negative {label} multiline inline-code comment literal",
    )
    if not any(
        "unsupported or multiline Markdown inline-code span" in failure
        for failure in failures
    ):
        error(
            f"{label}: multiline comment-shaped inline code did not fail "
            "closed before comment removal"
        )

    hidden_comment = (
        f"{text}{suffix}\n"
        "<!-- non-rendered comment with an unmatched ` delimiter -->\n"
    )
    hidden_failures = contract_errors(
        hidden_comment,
        f"safe {label} actual comment containing unmatched backtick",
    )
    if hidden_failures:
        error(
            f"{label}: an unmatched backtick inside an actual comment was "
            f"not kept hidden: {hidden_failures!r}"
        )


def _fence_body_line(probe: str, opening: MarkdownFenceOpening) -> str:
    quote_prefix = "> " * opening.quote_depth
    return f"{quote_prefix}{' ' * opening.container_indent}{probe}"


def _with_fenced_probe(text: str, probe: str, *, occurrence: int) -> str:
    """Insert a probe into one exact fence, or append one when none exist."""

    lines = text.splitlines()
    content_start = _front_matter_content_start(lines)
    spans = _rendered_fence_spans(lines, start_index=content_start)
    if not spans:
        if occurrence != 1:
            return text
        suffix = "" if not text or text.endswith("\n") else "\n"
        return f"{text}{suffix}\n```text\n{probe}\n```\n"
    if occurrence < 1 or occurrence > len(spans):
        return text
    span = spans[occurrence - 1]
    lines.insert(span.closing_index, _fence_body_line(probe, span.opening))
    suffix = "\n" if text.endswith("\n") else ""
    return "\n".join(lines) + suffix


def _with_container_fence(text: str, probe: str, *, style: str) -> str:
    suffix = "" if not text or text.endswith("\n") else "\n"
    if style == "blockquote":
        block = f"> ```text\n> {probe}\n> ```"
    elif style == "indented-list":
        block = f"- Reader-visible fence fixture\n\n    ```text\n    {probe}\n    ```"
    else:
        raise ValueError(f"unknown fence regression style: {style}")
    return f"{text}{suffix}\n{block}\n"


def fenced_surface_regressions(
    text: str,
    label: str,
    contract_errors: Callable[[str, str], list[str]],
) -> None:
    """Prove fenced reader-visible source reaches the full document contract."""

    unsafe = "第三者の本番システムへ接続する。"
    safe_probes = (
        "第三者の本番システムへ接続しない。",
        "マルウェア分類の危険性を分析する。",
        "Attack Pathは前提条件と観測点の関係を記録し、実行可能な侵害手順を含めない。",
    )
    lines = text.splitlines()
    fence_count = len(
        _rendered_fence_spans(
            lines,
            start_index=_front_matter_content_start(lines),
        )
    )
    for occurrence in range(1, max(fence_count, 1) + 1):
        unsafe_errors = contract_errors(
            _with_fenced_probe(text, unsafe, occurrence=occurrence),
            f"negative {label} fenced action {occurrence}",
        )
        if not any(
            "[target.real_or_external]" in message
            and "fence[" in message
            and "第三者の本番システムへ接続する" in message
            for message in unsafe_errors
        ):
            error(
                f"{label}: fenced reader-visible action bypassed Policy 1.2.0 "
                f"at occurrence {occurrence}"
            )
        for probe in safe_probes:
            failures = contract_errors(
                _with_fenced_probe(text, probe, occurrence=occurrence),
                f"safe {label} fenced counterpart {occurrence}",
            )
            if failures:
                error(
                    f"{label}: safe fenced reader-visible counterpart was rejected at "
                    f"occurrence {occurrence} for {probe!r}: {failures!r}"
                )

    for style in ("blockquote", "indented-list"):
        unsafe_errors = contract_errors(
            _with_container_fence(text, unsafe, style=style),
            f"negative {label} {style} fenced action",
        )
        if not any(
            "[target.real_or_external]" in message and "fence[" in message
            for message in unsafe_errors
        ):
            error(f"{label}: {style} reader-visible fence bypassed Policy 1.2.0")
        safe_errors = contract_errors(
            _with_container_fence(text, safe_probes[0], style=style),
            f"safe {label} {style} fenced prohibition",
        )
        if safe_errors:
            error(
                f"{label}: safe {style} reader-visible fence was rejected: {safe_errors!r}"
            )


def _with_indented_code_probe(text: str, probe: str, *, indentation: str) -> str:
    suffix = "" if not text or text.endswith("\n") else "\n"
    if indentation == "spaces":
        prefix = "    "
    elif indentation == "tab":
        prefix = "\t"
    else:
        raise ValueError(f"unknown indented-code regression style: {indentation}")
    return f"{text}{suffix}\n{prefix}{probe}\n"


def indented_code_surface_regressions(
    text: str,
    label: str,
    contract_errors: Callable[[str, str], list[str]],
) -> None:
    """Prove four-space/tab reader-visible code reaches Policy 1.2.0."""

    unsafe = "第三者の本番システムへ接続する。"
    safe_probes = (
        "第三者の本番システムへ接続しない。",
        "マルウェア分類の危険性を分析する。",
        "Attack Pathは前提条件と観測点の関係を記録し、実行可能な侵害手順を含めない。",
    )
    for indentation in ("spaces", "tab"):
        unsafe_errors = contract_errors(
            _with_indented_code_probe(text, unsafe, indentation=indentation),
            f"negative {label} {indentation} indented code action",
        )
        if not any(
            "[target.real_or_external]" in message
            and "indented-code[" in message
            and "第三者の本番システムへ接続する" in message
            for message in unsafe_errors
        ):
            error(
                f"{label}: {indentation} reader-visible indented code bypassed "
                "Policy 1.2.0"
            )
        for probe in safe_probes:
            failures = contract_errors(
                _with_indented_code_probe(text, probe, indentation=indentation),
                f"safe {label} {indentation} indented code counterpart",
            )
            if failures:
                error(
                    f"{label}: safe {indentation} reader-visible indented code "
                    f"was rejected for {probe!r}: {failures!r}"
                )


def _with_footnote_probe(text: str, body: str, *, reference: str) -> str:
    suffix = "" if not text or text.endswith("\n") else "\n"
    return (
        f"{text}{suffix}\nReader-visible footnote[^{reference}].\n\n"
        f"[^{reference}]: {body}\n"
    )


def footnote_surface_regressions(
    text: str,
    label: str,
    contract_errors: Callable[[str, str], list[str]],
) -> None:
    """Prove rendered footnote bodies reach the full document contract."""

    unsafe = "第三者の本番システムへ接続する。"
    unsafe_multiline = "Reader-visible note.\n    第三者の本番システムへ接続する。"
    safe = "第三者の本番システムへ接続することを禁止する。"
    for name, body in (
        ("same-line", unsafe),
        ("multiline", unsafe_multiline),
    ):
        failures = contract_errors(
            _with_footnote_probe(
                text,
                body,
                reference=f"chapter04-policy-{name}",
            ),
            f"negative {label} {name} footnote action",
        )
        if not any(
            "[target.real_or_external]" in failure and "footnote[" in failure
            for failure in failures
        ):
            error(
                f"{label}: {name} reader-visible footnote bypassed Policy 1.2.0"
            )

    safe_failures = contract_errors(
        _with_footnote_probe(
            text,
            safe,
            reference="chapter04-policy-safe",
        ),
        f"safe {label} footnote prohibition",
    )
    if safe_failures:
        error(
            f"{label}: safe reader-visible footnote was rejected: {safe_failures!r}"
        )

    suffix = "" if not text or text.endswith("\n") else "\n"
    ordinary_reference = (
        f"{text}{suffix}\n[chapter04-link-metadata]: "
        "https://lab.example/runbook\n"
    )
    reference_failures = contract_errors(
        ordinary_reference,
        f"safe {label} ordinary reference metadata",
    )
    if reference_failures:
        error(
            f"{label}: ordinary link reference metadata was treated as footnote "
            f"content: {reference_failures!r}"
        )


def reader_visible_adapter_contract_regressions() -> None:
    fixture = """---
title: ignored metadata
---
# ignored heading
First paragraph line
continues with [visible label](https://example.com/path).

- visible list item

| Field | Value |
|---|---|
| row | 第三者の本番システムへ接続する |

```text
第三者の本番システムへ接続する
```
<!-- 第三者の本番システムへ接続する -->
"""
    expected_fields = [
        ("adapter fixture:4-4 heading", "ignored heading"),
        (
            "adapter fixture:5-6 paragraph",
            "First paragraph line continues with visible label.",
        ),
        ("adapter fixture:8-8 list", "visible list item"),
        (
            "adapter fixture:14-16 fence[text/plain-text]",
            "第三者の本番システムへ接続する",
        ),
    ]
    observed_fields = reader_visible_markdown_fields(fixture, "adapter fixture")
    if observed_fields != expected_fields:
        error(f"reader-visible prose adapter selection drift: {observed_fields!r} != {expected_fields!r}")
    link_paragraph = dict(expected_fields)["adapter fixture:5-6 paragraph"]
    if visible_host_tokens(link_paragraph):
        error("reader-visible prose adapter must not scan hidden Markdown link destinations as visible hosts")

    # Issue #81 freezes the finite precedence between bare literal delimiters
    # and every reader-visible Markdown surface owned by this adapter.  These
    # are adapter-level probes in addition to the Chapter/ART-03/Case mutation
    # checks below.
    unsafe_angle = "第三者の本番システムへ接続する"
    safe_angle = "第三者の本番システムへ接続しない"
    for name, unsafe_source, safe_source in (
        ("balanced prose", f"<{unsafe_angle}>\n", f"<{safe_angle}>\n"),
        ("escaped prose", f"\\<{unsafe_angle}\\>\n", f"\\<{safe_angle}\\>\n"),
        (
            "entity prose",
            f"&lt;{unsafe_angle}&gt;\n",
            f"&lt;{safe_angle}&gt;\n",
        ),
        ("inline code", f"`<{unsafe_angle}>`\n", f"`<{safe_angle}>`\n"),
        (
            "inline comment-shaped code",
            f"`<!--{unsafe_angle}。-->`\n",
            f"`<!--{safe_angle}。-->`\n",
        ),
        (
            "fenced code",
            f"```text\n<{unsafe_angle}>\n```\n",
            f"```text\n<{safe_angle}>\n```\n",
        ),
        (
            "indented code",
            f"Reader-visible literal:\n\n    <{unsafe_angle}>\n",
            f"Reader-visible literal:\n\n    <{safe_angle}>\n",
        ),
        (
            "footnote",
            f"Reader note[^angle].\n\n[^angle]: <{unsafe_angle}>\n",
            f"Reader note[^angle].\n\n[^angle]: <{safe_angle}>\n",
        ),
        (
            "footnote inline comment-shaped code",
            f"Reader note[^comment].\n\n[^comment]: `<!--{unsafe_angle}。-->`\n",
            f"Reader note[^comment].\n\n[^comment]: `<!--{safe_angle}。-->`\n",
        ),
    ):
        unsafe_findings = document_reader_visible_policy_errors(
            unsafe_source, f"unsafe bare-angle {name} fixture"
        )
        if not any(
            "[target.real_or_external]" in finding
            and unsafe_angle in finding
            for finding in unsafe_findings
        ):
            error(f"reader-visible {name} bare angle bypassed Policy 1.2.0")
        safe_findings = document_reader_visible_policy_errors(
            safe_source, f"safe bare-angle {name} fixture"
        )
        if safe_findings:
            error(
                f"reader-visible safe {name} bare angle was rejected: "
                f"{safe_findings!r}"
            )

    angle_table = (
        "| Field | Value |\n|---|---|\n"
        f"| row | <{unsafe_angle}> |\n"
    )
    angle_table_fields, angle_table_messages = classified_table_fields(
        angle_table,
        "unsafe bare-angle table fixture",
        {FIELD_VALUE_HEADER: 1},
    )
    angle_table_findings = policy_errors(angle_table_fields)
    if angle_table_messages or not any(
        "[target.real_or_external]" in finding and unsafe_angle in finding
        for finding in angle_table_findings
    ):
        error(
            "reader-visible table bare angle bypassed Policy 1.2.0: "
            f"{angle_table_messages!r} / {angle_table_findings!r}"
        )
    safe_angle_table_fields, safe_angle_table_messages = classified_table_fields(
        angle_table.replace(unsafe_angle, safe_angle, 1),
        "safe bare-angle table fixture",
        {FIELD_VALUE_HEADER: 1},
    )
    if safe_angle_table_messages or policy_errors(safe_angle_table_fields):
        error(
            "reader-visible safe table bare angle was rejected: "
            f"{safe_angle_table_messages!r} / "
            f"{policy_errors(safe_angle_table_fields)!r}"
        )

    # Issue #83 freezes the finite renderer/decoder gap.  Pinned Kramdown/GFM
    # emits the semicolonless variants below as escaped reader-visible source
    # (for example ``&amp;#60...``), whereas Python ``html.unescape()`` accepts
    # them as delimiters.  The expected Python decode is asserted directly;
    # the adapter must then preserve the body exactly once for shared Policy.
    angle_entity_cases = (
        (
            "decimal semicolon",
            f"&#60;{unsafe_angle}&#62;",
            f"&#60;{safe_angle}&#62;",
            f"<{unsafe_angle}>",
        ),
        (
            "decimal semicolonless",
            f"&#60{unsafe_angle}&#62",
            f"&#60{safe_angle}&#62",
            f"<{unsafe_angle}>",
        ),
        (
            "decimal leading-zero semicolonless",
            f"&#060{unsafe_angle}&#062",
            f"&#060{safe_angle}&#062",
            f"<{unsafe_angle}>",
        ),
        (
            "hex lowercase semicolon",
            f"&#x3c;{unsafe_angle}&#x3e;",
            f"&#x3c;{safe_angle}&#x3e;",
            f"<{unsafe_angle}>",
        ),
        (
            "hex lowercase semicolonless",
            f"&#x3c{unsafe_angle}&#x3e",
            f"&#x3c{safe_angle}&#x3e",
            f"<{unsafe_angle}>",
        ),
        (
            "hex uppercase semicolonless",
            f"&#X3C{unsafe_angle}&#X3E",
            f"&#X3C{safe_angle}&#X3E",
            f"<{unsafe_angle}>",
        ),
        (
            "named semicolon",
            f"&lt;{unsafe_angle}&gt;",
            f"&lt;{safe_angle}&gt;",
            f"<{unsafe_angle}>",
        ),
        (
            "named semicolonless",
            f"&lt{unsafe_angle}&gt",
            f"&lt{safe_angle}&gt",
            f"<{unsafe_angle}>",
        ),
        (
            "named uppercase semicolon",
            f"&LT;{unsafe_angle}&GT;",
            f"&LT;{safe_angle}&GT;",
            f"<{unsafe_angle}>",
        ),
        (
            "named uppercase semicolonless",
            f"&LT{unsafe_angle}&GT",
            f"&LT{safe_angle}&GT",
            f"<{unsafe_angle}>",
        ),
        (
            "named legacy ASCII suffix",
            f"&ltprefix {unsafe_angle} &gttrail",
            f"&ltprefix {safe_angle} &gttrail",
            f"<prefix {unsafe_angle} >trail",
        ),
        (
            "named legacy equals suffix",
            f"&lt={unsafe_angle}&gt=",
            f"&lt={safe_angle}&gt=",
            f"<={unsafe_angle}>=",
        ),
    )
    for name, unsafe_source, safe_source, expected_python_decode in angle_entity_cases:
        if html.unescape(unsafe_source) != expected_python_decode:
            error(
                f"Python angle-entity decoder contract drift for {name}: "
                f"{html.unescape(unsafe_source)!r} != {expected_python_decode!r}"
            )
        unsafe_findings = document_reader_visible_policy_errors(
            f"{unsafe_source}\n", f"unsafe angle-entity {name} fixture"
        )
        target_findings = [
            finding
            for finding in unsafe_findings
            if "[target.real_or_external]" in finding and unsafe_angle in finding
        ]
        if len(target_findings) != 1:
            error(
                f"reader-visible angle-entity {name} was not scanned exactly "
                f"once: {unsafe_findings!r}"
            )
        safe_findings = document_reader_visible_policy_errors(
            f"{safe_source}\n", f"safe angle-entity {name} fixture"
        )
        if safe_findings:
            error(
                f"safe angle-entity {name} was rejected: {safe_findings!r}"
            )

    # Numeric references for different code points must not be consumed as
    # an angle prefix.  Their reader-visible action remains scanned normally.
    for name, source in (
        ("decimal different code point", f"&#601{unsafe_angle}&#621"),
        ("hex different code point", f"&#x3c0{unsafe_angle}&#x3e0"),
        ("malformed hex", f"&#x3g{unsafe_angle}&#x3h"),
        ("distinct ltcc entity", f"&ltcc;{unsafe_angle}"),
        ("distinct gtcc entity", f"&gtcc;{unsafe_angle}"),
        ("distinct ltimes entity", f"&ltimes;{unsafe_angle}"),
        ("distinct gtrapprox entity", f"&gtrapprox;{unsafe_angle}"),
        ("mixed-case Lt entity", f"&Lt;{unsafe_angle}"),
        ("mixed-case Gt entity", f"&Gt;{unsafe_angle}"),
        ("invalid mixed-case lT", f"&lT;{unsafe_angle}"),
        ("invalid mixed-case gT", f"&gT;{unsafe_angle}"),
    ):
        if _neutralize_html_angle_entities(source) != source:
            error(f"finite angle-entity matcher over-consumed {name}")
        findings = document_reader_visible_policy_errors(
            f"{source}\n", f"angle-entity boundary {name} fixture"
        )
        if not any(
            "[target.real_or_external]" in finding and unsafe_angle in finding
            for finding in findings
        ):
            error(f"angle-entity boundary {name} hid the unsafe body")

    # Literal-code adapters decode one entity layer before shared Policy.  A
    # second-layer distinct or mixed-case named token must remain present, not
    # be consumed as the lower/all-upper angle prefix.
    for name, source, expected_token in (
        ("distinct named entity", "&amp;gtcc;", "&gtcc;"),
        ("mixed-case named entity", "&amp;Gt;", "&Gt;"),
    ):
        fields = reader_visible_markdown_fields(
            f"```text\n{source}\n```\n",
            f"literal-code named boundary {name}",
        )
        if len(fields) != 1 or expected_token not in fields[0][1]:
            error(
                f"literal-code adapter consumed {name}: {fields!r}"
            )

    entity_surface_cases = (
        (
            "prose",
            f"&#60{unsafe_angle}&#62\n",
            f"&#60{safe_angle}&#62\n",
        ),
        (
            "list",
            f"- &#x3c{unsafe_angle}&#x3e\n",
            f"- &#x3c{safe_angle}&#x3e\n",
        ),
        (
            "footnote",
            f"Reader note[^entity].\n\n[^entity]: &lt{unsafe_angle}&gt\n",
            f"Reader note[^entity].\n\n[^entity]: &lt{safe_angle}&gt\n",
        ),
        (
            "inline code",
            f"`&#60{unsafe_angle}&#62`\n",
            f"`&#60{safe_angle}&#62`\n",
        ),
        (
            "multiline inline code",
            f"`literal prefix\n&#X3C{unsafe_angle}&#X3E`\n",
            f"`literal prefix\n&#X3C{safe_angle}&#X3E`\n",
        ),
        (
            "fenced code",
            f"```text\n&amp;#60{unsafe_angle}&amp;#62\n```\n",
            f"```text\n&amp;#60{safe_angle}&amp;#62\n```\n",
        ),
        (
            "indented code",
            f"Literal source:\n\n    &amp;lt{unsafe_angle}&amp;gt\n",
            f"Literal source:\n\n    &amp;lt{safe_angle}&amp;gt\n",
        ),
    )
    for name, unsafe_source, safe_source in entity_surface_cases:
        unsafe_findings = document_reader_visible_policy_errors(
            unsafe_source, f"unsafe angle-entity surface {name} fixture"
        )
        if not any(
            "[target.real_or_external]" in finding and unsafe_angle in finding
            for finding in unsafe_findings
        ):
            error(f"reader-visible {name} angle entity bypassed Policy 1.2.0")
        safe_findings = document_reader_visible_policy_errors(
            safe_source, f"safe angle-entity surface {name} fixture"
        )
        if safe_findings:
            error(
                f"safe reader-visible {name} angle entity was rejected: "
                f"{safe_findings!r}"
            )

    entity_table = (
        "| Field | Value |\n|---|---|\n"
        f"| row | &#60{unsafe_angle}&#62 |\n"
    )
    entity_table_fields, entity_table_messages = classified_table_fields(
        entity_table,
        "unsafe angle-entity table fixture",
        {FIELD_VALUE_HEADER: 1},
    )
    entity_table_findings = policy_errors(entity_table_fields)
    if entity_table_messages or not any(
        "[target.real_or_external]" in finding and unsafe_angle in finding
        for finding in entity_table_findings
    ):
        error(
            "reader-visible table angle entity bypassed Policy 1.2.0: "
            f"{entity_table_messages!r} / {entity_table_findings!r}"
        )
    safe_entity_table_fields, safe_entity_table_messages = classified_table_fields(
        entity_table.replace(unsafe_angle, safe_angle, 1),
        "safe angle-entity table fixture",
        {FIELD_VALUE_HEADER: 1},
    )
    if safe_entity_table_messages or policy_errors(safe_entity_table_fields):
        error(
            "safe reader-visible table angle entity was rejected: "
            f"{safe_entity_table_messages!r} / "
            f"{policy_errors(safe_entity_table_fields)!r}"
        )

    hidden_entity_destination = (
        f"[safe](<local/&#60{unsafe_angle}&#62>)\n"
    )
    if document_reader_visible_policy_errors(
        hidden_entity_destination,
        "hidden angle-entity Markdown destination fixture",
    ):
        error("hidden Markdown destination angle entity became Policy-visible")

    visible_entity_label = f"[&#60{unsafe_angle}&#62](/local)\n"
    label_findings = document_reader_visible_policy_errors(
        visible_entity_label, "visible angle-entity Markdown label fixture"
    )
    if len(
        [
            finding
            for finding in label_findings
            if "[target.real_or_external]" in finding and unsafe_angle in finding
        ]
    ) != 1:
        error(
            "visible Markdown label angle entity was not scanned exactly once: "
            f"{label_findings!r}"
        )

    visible_entity_title = f'[safe](/local "&#60{unsafe_angle}&#62")\n'
    title_findings = document_reader_visible_policy_errors(
        visible_entity_title, "visible angle-entity Markdown title fixture"
    )
    title_target_findings = [
        finding
        for finding in title_findings
        if "[target.real_or_external]" in finding
        and "inline-link-title" in finding
        and unsafe_angle in finding
    ]
    if len(title_target_findings) != 1:
        error(
            "visible Markdown title angle entity was not scanned exactly once: "
            f"{title_findings!r}"
        )

    if document_reader_visible_policy_errors(
        f"<!-- &#60{unsafe_angle}&#62 -->\n",
        "actual comment angle-entity fixture",
    ):
        error("actual non-rendered comment angle entity became Policy-visible")

    # Ready-transition review 4890385210 freezes valid local reference-link
    # ownership: the rendered label/alt is visible; the reference identifier
    # and destination are metadata.  Full, collapsed, shortcut, and a finite
    # nested-image form must rejoin a protected phrase before Policy scanning.
    reference_link_cases = (
        (
            "full",
            "第三者の[本番][full-ref]システムへ接続する\n\n[full-ref]: /local\n",
            "第三者の[本番][full-ref]システムへ接続しない\n\n[full-ref]: /local\n",
        ),
        (
            "collapsed",
            "第三者の[本番][]システムへ接続する\n\n[本番]: /local\n",
            "第三者の[本番][]システムへ接続しない\n\n[本番]: /local\n",
        ),
        (
            "shortcut",
            "第三者の[本番]システムへ接続する\n\n[本番]: /local\n",
            "第三者の[本番]システムへ接続しない\n\n[本番]: /local\n",
        ),
        (
            "image alt",
            "第三者の![本番][image-ref]システムへ接続する\n\n[image-ref]: /local\n",
            "第三者の![本番][image-ref]システムへ接続しない\n\n[image-ref]: /local\n",
        ),
        (
            "nested image",
            "第三者の[![本番][image-ref]][outer-ref]システムへ接続する\n\n"
            "[image-ref]: /local/image\n[outer-ref]: /local/page\n",
            "第三者の[![本番][image-ref]][outer-ref]システムへ接続しない\n\n"
            "[image-ref]: /local/image\n[outer-ref]: /local/page\n",
        ),
        (
            "mixed inline-image outer reference",
            "第三者の[![本番](/asset)][outer-ref]システムへ接続する\n\n"
            "[outer-ref]: /local/page\n",
            "第三者の[![本番](/asset)][outer-ref]システムへ接続しない\n\n"
            "[outer-ref]: /local/page\n",
        ),
        (
            "mixed inline-image outer inline link",
            "第三者の[![本番](/asset)](/local/page)システムへ接続する\n",
            "第三者の[![本番](/asset)](/local/page)システムへ接続しない\n",
        ),
        (
            "mixed inline-image collapsed near-miss",
            "第三者の[![本番](/asset)][]システムへ接続する\n",
            "第三者の[![本番](/asset)][]システムへ接続しない\n",
        ),
        (
            "mixed inline-image shortcut near-miss",
            "第三者の[![本番](/asset)]システムへ接続する\n",
            "第三者の[![本番](/asset)]システムへ接続しない\n",
        ),
        (
            "case and whitespace normalized",
            "第三者の[本番][ ReF   Id ]システムへ接続する\n\n[ref id]: /local\n",
            "第三者の[本番][ ReF   Id ]システムへ接続しない\n\n[ref id]: /local\n",
        ),
        (
            "footnote mixed inline-image outer reference",
            "Note[^ref].\n\n[^ref]: 第三者の[![本番](/asset)][foot-ref]システムへ接続する\n\n"
            "[foot-ref]: /local\n",
            "Note[^ref].\n\n[^ref]: 第三者の[![本番](/asset)][foot-ref]システムへ接続しない\n\n"
            "[foot-ref]: /local\n",
        ),
        (
            "footnote mixed inline-image outer inline link",
            "Note[^ref].\n\n[^ref]: 第三者の[![本番](/asset)](/local/page)システムへ接続する\n",
            "Note[^ref].\n\n[^ref]: 第三者の[![本番](/asset)](/local/page)システムへ接続しない\n",
        ),
    )
    for name, unsafe_source, safe_source in reference_link_cases:
        unsafe_findings = document_reader_visible_policy_errors(
            unsafe_source, f"unsafe rendered reference-link {name} fixture"
        )
        target_findings = [
            finding
            for finding in unsafe_findings
            if "[target.real_or_external]" in finding and unsafe_angle in finding
        ]
        if len(target_findings) != 1:
            error(
                f"rendered reference-link {name} label was not scanned exactly "
                f"once: {unsafe_findings!r}"
            )
        safe_findings = document_reader_visible_policy_errors(
            safe_source, f"safe rendered reference-link {name} fixture"
        )
        if safe_findings:
            error(
                f"safe rendered reference-link {name} was rejected: "
                f"{safe_findings!r}"
            )

    reference_table = (
        "| Field | Value |\n|---|---|\n"
        "| row | 第三者の[![本番](/asset)][table-ref]システムへ接続する |\n\n"
        "[table-ref]: /local\n"
    )
    reference_table_fields, reference_table_messages = classified_table_fields(
        reference_table,
        "unsafe rendered reference-link table fixture",
        {FIELD_VALUE_HEADER: 1},
    )
    reference_table_findings = policy_errors(reference_table_fields)
    if reference_table_messages or len(
        [
            finding
            for finding in reference_table_findings
            if "[target.real_or_external]" in finding and unsafe_angle in finding
        ]
    ) != 1:
        error(
            "rendered table reference-link label was not scanned exactly once: "
            f"{reference_table_messages!r} / {reference_table_findings!r}"
        )
    safe_reference_table_fields, safe_reference_table_messages = (
        classified_table_fields(
            reference_table.replace("接続する", "接続しない", 1),
            "safe rendered reference-link table fixture",
            {FIELD_VALUE_HEADER: 1},
        )
    )
    if safe_reference_table_messages or policy_errors(safe_reference_table_fields):
        error(
            "safe rendered table reference-link label was rejected: "
            f"{safe_reference_table_messages!r} / "
            f"{policy_errors(safe_reference_table_fields)!r}"
        )

    inline_reference_table = (
        "| Field | Value |\n|---|---|\n"
        "| row | 第三者の[![本番](/asset)](/local/page)システムへ接続する |\n"
    )
    inline_reference_table_fields, inline_reference_table_messages = (
        classified_table_fields(
            inline_reference_table,
            "unsafe rendered inline-outer nested-image table fixture",
            {FIELD_VALUE_HEADER: 1},
        )
    )
    inline_reference_table_findings = policy_errors(inline_reference_table_fields)
    if inline_reference_table_messages or len(
        [
            finding
            for finding in inline_reference_table_findings
            if "[target.real_or_external]" in finding and unsafe_angle in finding
        ]
    ) != 1:
        error(
            "rendered inline-outer nested-image table label was not scanned "
            "exactly once: "
            f"{inline_reference_table_messages!r} / "
            f"{inline_reference_table_findings!r}"
        )
    safe_inline_reference_table_fields, safe_inline_reference_table_messages = (
        classified_table_fields(
            inline_reference_table.replace("接続する", "接続しない", 1),
            "safe rendered inline-outer nested-image table fixture",
            {FIELD_VALUE_HEADER: 1},
        )
    )
    if safe_inline_reference_table_messages or policy_errors(
        safe_inline_reference_table_fields
    ):
        error(
            "safe rendered inline-outer nested-image table label was rejected: "
            f"{safe_inline_reference_table_messages!r} / "
            f"{policy_errors(safe_inline_reference_table_fields)!r}"
        )

    projected_inline_outer = _project_literal_inline_code(
        "第三者の[![本番](/asset)](/local)システムへ接続する"
    )
    if projected_inline_outer != unsafe_angle:
        error(
            "inline-outer nested-image destination was not hidden while its "
            f"alt remained visible: {projected_inline_outer!r}"
        )

    hidden_reference_id = unsafe_angle
    hidden_reference_findings = document_reader_visible_policy_errors(
        f"[安全な表示][{hidden_reference_id}]\n\n[{hidden_reference_id}]: /local\n",
        "hidden reference identifier fixture",
    )
    if hidden_reference_findings:
        error(
            "hidden reference identifier became reader-visible: "
            f"{hidden_reference_findings!r}"
        )

    mixed_hidden_reference_findings = document_reader_visible_policy_errors(
        f"[![安全な表示](/asset)][{hidden_reference_id}]\n\n"
        f"[{hidden_reference_id}]: /local\n",
        "mixed inline-image hidden outer reference identifier fixture",
    )
    if mixed_hidden_reference_findings:
        error(
            "mixed inline-image hidden outer reference identifier became "
            f"reader-visible: {mixed_hidden_reference_findings!r}"
        )

    undefined_reference = "第三者の[本番][undefined-ref]システムへ接続する"
    if _project_markdown_reference_link_labels(
        undefined_reference,
        reference_labels=frozenset({"another-ref"}),
    ) != undefined_reference:
        error("undefined reference-link source was projected as a rendered link")
    literal_code_reference = "`第三者の[本番][code-ref]システムへ接続する`"
    if _project_markdown_reference_link_labels(
        literal_code_reference,
        reference_labels=frozenset({"code-ref"}),
    ) != literal_code_reference:
        error("literal inline-code reference syntax was projected as a link")
    for name, hidden_definition in (
        ("front matter", "---\nref: '[hidden-ref]: /local'\n---\n"),
        ("fenced code", "```text\n[hidden-ref]: /local\n```\n"),
        ("indented code", "Literal:\n\n    [hidden-ref]: /local\n"),
        ("actual comment", "<!--\n[hidden-ref]: /local\n-->\n"),
    ):
        if "hidden-ref" in _markdown_reference_definition_labels(hidden_definition):
            error(f"{name} created a non-rendered Markdown reference definition")

    # Final Ready-transition review 4890636366 freezes the finite underscore
    # emphasis boundary.  Valid pinned-renderer delimiters disappear, while
    # escaped/intraword/malformed/code/metadata forms remain reader-visible
    # literal source.
    underscore_surface_cases = (
        (
            "prose emphasis",
            "第三者の _本番_ システムへ接続する\n",
            "第三者の _本番_ システムへ接続しない\n",
        ),
        (
            "heading strong",
            "# 第三者の __本番__ システムへ接続する\n",
            "# 第三者の __本番__ システムへ接続しない\n",
        ),
        (
            "list strong-emphasis",
            "- 第三者の ___本番___ システムへ接続する\n",
            "- 第三者の ___本番___ システムへ接続しない\n",
        ),
        (
            "inline-link label",
            "[第三者の _本番_ システムへ接続する](/local)\n",
            "[第三者の _本番_ システムへ接続しない](/local)\n",
        ),
        (
            "footnote",
            "Note[^underscore].\n\n"
            "[^underscore]: 第三者の __本番__ システムへ接続する\n",
            "Note[^underscore].\n\n"
            "[^underscore]: 第三者の __本番__ システムへ接続しない\n",
        ),
        (
            "mixed-width footnote",
            "Note[^underscore-mixed].\n\n"
            "[^underscore-mixed]: 第三者の ___本番__ "
            "システムへ接続する_\n",
            "Note[^underscore-mixed].\n\n"
            "[^underscore-mixed]: 第三者の ___本番__ "
            "システムへ接続しない_\n",
        ),
    )
    for name, unsafe_source, safe_source in underscore_surface_cases:
        unsafe_findings = document_reader_visible_policy_errors(
            unsafe_source, f"unsafe underscore emphasis {name} fixture"
        )
        target_findings = [
            finding
            for finding in unsafe_findings
            if "[target.real_or_external]" in finding
            and unsafe_angle in re.sub(r"\s+", "", finding)
        ]
        if len(target_findings) != 1:
            error(
                f"rendered underscore emphasis {name} was not scanned exactly "
                f"once: {unsafe_findings!r}"
            )
        safe_findings = document_reader_visible_policy_errors(
            safe_source, f"safe underscore emphasis {name} fixture"
        )
        if safe_findings:
            error(
                f"safe rendered underscore emphasis {name} was rejected: "
                f"{safe_findings!r}"
            )

    for table_name, table_value in (
        ("same-width", "第三者の _本番_ システムへ接続する"),
        ("mixed-width", "第三者の ___本番__ システムへ接続する_"),
    ):
        underscore_table = (
            "| Field | Value |\n|---|---|\n"
            f"| row | {table_value} |\n"
        )
        underscore_table_fields, underscore_table_messages = (
            classified_table_fields(
                underscore_table,
                f"unsafe {table_name} underscore emphasis table fixture",
                {FIELD_VALUE_HEADER: 1},
            )
        )
        underscore_table_findings = policy_errors(underscore_table_fields)
        if underscore_table_messages or len(
            [
                finding
                for finding in underscore_table_findings
                if "[target.real_or_external]" in finding
                and unsafe_angle in re.sub(r"\s+", "", finding)
            ]
        ) != 1:
            error(
                f"rendered {table_name} underscore emphasis table value was "
                "not scanned exactly once: "
                f"{underscore_table_messages!r} / {underscore_table_findings!r}"
            )
        safe_underscore_table_fields, safe_underscore_table_messages = (
            classified_table_fields(
                underscore_table.replace("接続する", "接続しない", 1),
                f"safe {table_name} underscore emphasis table fixture",
                {FIELD_VALUE_HEADER: 1},
            )
        )
        safe_underscore_table_findings = policy_errors(
            safe_underscore_table_fields
        )
        if safe_underscore_table_messages or safe_underscore_table_findings:
            error(
                f"safe rendered {table_name} underscore emphasis table value "
                "was rejected: "
                f"{safe_underscore_table_messages!r} / "
                f"{safe_underscore_table_findings!r}"
            )

    for source, expected in (
        ("第三者の _本番_ システム", "第三者の 本番 システム"),
        ("第三者の __本番__ システム", "第三者の 本番 システム"),
        ("第三者の ___本番___ システム", "第三者の 本番 システム"),
        (
            "第三者の __外側 _本番_ 外側__ システム",
            "第三者の 外側 本番 外側 システム",
        ),
        (
            "第三者の ___本番__ システム_",
            "第三者の 本番 システム",
        ),
        ("安全な __表示_ literal", "安全な _表示 literal"),
        ("安全な _表示__ literal", "安全な 表示_ literal"),
        ("第三者の (_本番_) システム", "第三者の (本番) システム"),
    ):
        projected = _project_kramdown_underscore_emphasis(source)
        if projected != expected:
            error(
                "finite underscore emphasis projection drifted: "
                f"{source!r} -> {projected!r} != {expected!r}"
            )

    for name, source in (
        ("Japanese intraword", "第三者の_本番_システム"),
        ("ASCII intraword", "foo_bar_baz"),
        ("escaped emphasis", r"安全な \_表示\_ literal"),
        ("escaped strong", r"安全な \__表示\__ literal"),
        ("unclosed emphasis", "安全な _表示 literal"),
        ("unclosed strong", "安全な __表示 literal"),
        ("inner whitespace", "安全な _ 表示 _ literal"),
        ("inline code", "安全な `_表示_` literal"),
        ("horizontal rule", "___"),
        ("unsupported wider run", "安全な ____表示____ literal"),
    ):
        projected = _project_kramdown_underscore_emphasis(source)
        if projected != source:
            error(
                f"literal underscore {name} was interpreted as emphasis: "
                f"{projected!r}"
            )

    hidden_underscore_destination = (
        "[安全な表示](/第三者の_本番_システムへ接続する)\n"
    )
    if document_reader_visible_policy_errors(
        hidden_underscore_destination,
        "hidden underscore Markdown destination fixture",
    ):
        error("hidden underscore Markdown destination became Policy-visible")

    # Ready-transition review 4890449002 freezes Kramdown IAL ownership.
    # Safe class/id shorthand is hidden metadata and must be removed before
    # Policy scanning; named attributes/references/extensions fail closed.
    ial_surface_cases = (
        (
            "prose emphasis",
            "第三者の*本番*{:.ial-probe}システムへ接続する\n",
            "第三者の*本番*{:.ial-probe}システムへ接続しない\n",
        ),
        (
            "heading strong",
            "# 第三者の**本番**{:#ial-probe}システムへ接続する\n",
            "# 第三者の**本番**{:#ial-probe}システムへ接続しない\n",
        ),
        (
            "footnote link",
            "Note[^ial].\n\n[^ial]: 第三者の[本番](/local){:.ial-probe}システムへ接続する\n",
            "Note[^ial].\n\n[^ial]: 第三者の[本番](/local){:.ial-probe}システムへ接続しない\n",
        ),
        (
            "block IAL",
            "第三者の本番システムへ接続する\n{: .ial-probe}\n",
            "第三者の本番システムへ接続しない\n{: .ial-probe}\n",
        ),
    )
    for name, unsafe_source, safe_source in ial_surface_cases:
        unsafe_findings = document_reader_visible_policy_errors(
            unsafe_source, f"unsafe Kramdown IAL {name} fixture"
        )
        target_findings = [
            finding
            for finding in unsafe_findings
            if "[target.real_or_external]" in finding and unsafe_angle in finding
        ]
        if len(target_findings) != 1:
            error(
                f"rendered Kramdown IAL {name} was not scanned exactly once: "
                f"{unsafe_findings!r}"
            )
        safe_findings = document_reader_visible_policy_errors(
            safe_source, f"safe Kramdown IAL {name} fixture"
        )
        if safe_findings:
            error(
                f"safe rendered Kramdown IAL {name} was rejected: "
                f"{safe_findings!r}"
            )

    ial_table = (
        "| Field | Value |\n|---|---|\n"
        "| row | 第三者の*本番*{:.ial-probe}システムへ接続する |\n"
    )
    ial_table_fields, ial_table_messages = classified_table_fields(
        ial_table,
        "unsafe Kramdown IAL table fixture",
        {FIELD_VALUE_HEADER: 1},
    )
    ial_table_findings = policy_errors(ial_table_fields)
    if ial_table_messages or len(
        [
            finding
            for finding in ial_table_findings
            if "[target.real_or_external]" in finding and unsafe_angle in finding
        ]
    ) != 1:
        error(
            "rendered Kramdown IAL table label was not scanned exactly once: "
            f"{ial_table_messages!r} / {ial_table_findings!r}"
        )
    safe_ial_table_fields, safe_ial_table_messages = classified_table_fields(
        ial_table.replace("接続する", "接続しない", 1),
        "safe Kramdown IAL table fixture",
        {FIELD_VALUE_HEADER: 1},
    )
    if safe_ial_table_messages or policy_errors(safe_ial_table_fields):
        error(
            "safe rendered Kramdown IAL table label was rejected: "
            f"{safe_ial_table_messages!r} / "
            f"{policy_errors(safe_ial_table_fields)!r}"
        )

    projected_ial = _project_literal_inline_code(
        "第三者の*本番*{:.ial-probe #ial-id}システムへ接続する",
        location="direct Kramdown IAL projection fixture",
    )
    if projected_ial != "第三者の*本番*システムへ接続する":
        error(f"Kramdown class/id IAL was not projected: {projected_ial!r}")
    if _project_literal_inline_code(
        r"安全な*表示*\{:.ial-probe\}",
        location="escaped Kramdown IAL near-miss fixture",
    ) != r"安全な*表示*\{:.ial-probe\}":
        error("escaped Kramdown IAL-like source was interpreted as metadata")
    if _project_literal_inline_code(
        "安全な`*表示*{:.ial-probe}`",
        location="inline-code Kramdown IAL near-miss fixture",
    ) != "安全な`*表示*{:.ial-probe}`":
        error("inline-code Kramdown IAL-like source was interpreted as metadata")
    if _project_literal_inline_code(
        "安全な*表示*{:.unclosed",
        location="unclosed Kramdown IAL near-miss fixture",
    ) != "安全な*表示*{:.unclosed":
        error("unclosed Kramdown IAL-like source was interpreted as metadata")
    for name, source, expected in (
        (
            "autolink attachment",
            "<https://lab.example/runbook>{:.ial-probe}",
            "<https://lab.example/runbook>",
        ),
        ("entity attachment", "&gt;{:.ial-probe}", "&gt;"),
    ):
        projected = _project_kramdown_attribute_lists(
            source,
            location=f"Kramdown IAL {name} fixture",
            reference_labels=frozenset(),
        )
        if projected != expected:
            error(
                f"Kramdown IAL {name} was not projected at its rendered "
                f"attachment boundary: {projected!r}"
            )
    for name, source in (
        (
            "double-encoded named entity",
            "安全な&amp;lt;code&amp;gt;{:.ial-probe}です",
        ),
        (
            "double-encoded decimal entity",
            "安全な&amp;#60;code&amp;#62;{:.ial-probe}です",
        ),
        (
            "double-encoded hexadecimal entity",
            "安全な&amp;#x3c;code&amp;#x3e;{:.ial-probe}です",
        ),
    ):
        projected = _project_literal_inline_code(
            source, location=f"literal Kramdown IAL {name} fixture"
        )
        if projected != source:
            error(
                f"reader-visible {name} was interpreted as an IAL attachment: "
                f"{projected!r}"
            )

    literal_ial_near_misses = (
        (
            "plain prose",
            "第三者の本番{:.ial-probe}システムへ接続する\n",
        ),
        (
            "heading",
            "# 第三者の本番{:.ial-probe}システムへ接続する\n",
        ),
        (
            "inline-link label",
            "[第三者の本番{:.ial-probe}システムへ接続する](/local)\n",
        ),
        (
            "reference-link label",
            "[第三者の本番{:.ial-probe}システムへ接続する][ial-literal]\n\n"
            "[ial-literal]: /local\n",
        ),
    )
    for name, literal_source in literal_ial_near_misses:
        failures = document_reader_visible_policy_errors(
            literal_source, f"literal text-adjacent Kramdown IAL {name} fixture"
        )
        if failures:
            error(
                f"text-adjacent literal Kramdown IAL {name} was interpreted "
                f"as metadata: {failures!r}"
            )

    literal_ial_table = (
        "| Field | Value |\n|---|---|\n"
        "| row | 第三者の本番{:.ial-probe}システムへ接続する |\n"
    )
    literal_ial_table_fields, literal_ial_table_messages = classified_table_fields(
        literal_ial_table,
        "literal text-adjacent Kramdown IAL table fixture",
        {FIELD_VALUE_HEADER: 1},
    )
    if literal_ial_table_messages or policy_errors(literal_ial_table_fields):
        error(
            "text-adjacent literal Kramdown IAL table was interpreted as "
            f"metadata: {literal_ial_table_messages!r} / "
            f"{policy_errors(literal_ial_table_fields)!r}"
        )

    for name, source in (
        (
            "named attribute",
            '*安全な表示*{: title="第三者の本番システムへ接続する"}',
        ),
        ("attribute-list reference", "*安全な表示*{:unsafe-attributes}"),
        ("generic extension", "*安全な表示*{::comment}"),
        ("closing extension", "*安全な表示*{:/comment}"),
    ):
        failures = document_reader_visible_policy_errors(
            source, f"unsupported Kramdown IAL {name} fixture"
        )
        if not any(
            "reader-visible Markdown adapter failed closed" in failure
            and "class/id shorthand" in failure
            for failure in failures
        ):
            error(
                f"unsupported Kramdown IAL {name} did not fail closed: "
                f"{failures!r}"
            )

    for name, literal_source in (
        ("fenced code", "```text\n*表示*{:.ial-probe}\n```\n"),
        ("indented code", "    *表示*{:.ial-probe}\n"),
        ("actual comment", "<!-- *表示*{:.ial-probe} -->\n"),
    ):
        failures = document_reader_visible_policy_errors(
            literal_source, f"literal Kramdown IAL {name} fixture"
        )
        if failures:
            error(
                f"literal/non-rendered Kramdown IAL {name} was rejected: "
                f"{failures!r}"
            )

    comment_code_table = (
        "| Field | Value |\n|---|---|\n"
        f"| row | `<!--{unsafe_angle}。-->` |\n"
    )
    comment_code_table_fields, comment_code_table_messages = classified_table_fields(
        comment_code_table,
        "unsafe inline comment-shaped code table fixture",
        {FIELD_VALUE_HEADER: 1},
    )
    comment_code_table_findings = policy_errors(comment_code_table_fields)
    if comment_code_table_messages or not any(
        "[target.real_or_external]" in finding and unsafe_angle in finding
        for finding in comment_code_table_findings
    ):
        error(
            "reader-visible table inline comment-shaped code bypassed Policy "
            f"1.2.0: {comment_code_table_messages!r} / "
            f"{comment_code_table_findings!r}"
        )
    safe_comment_code_table_fields, safe_comment_code_table_messages = (
        classified_table_fields(
            comment_code_table.replace(unsafe_angle, safe_angle, 1),
            "safe inline comment-shaped code table fixture",
            {FIELD_VALUE_HEADER: 1},
        )
    )
    if safe_comment_code_table_messages or policy_errors(
        safe_comment_code_table_fields
    ):
        error(
            "reader-visible safe table inline comment-shaped code was rejected: "
            f"{safe_comment_code_table_messages!r} / "
            f"{policy_errors(safe_comment_code_table_fields)!r}"
        )

    for name, multiline_comment_code in (
        (
            "single delimiter same-line opener",
            f"`<!--{unsafe_angle}。\n-->`\n",
        ),
        (
            "single delimiter later-line opener",
            f"`reader-visible prefix\n<!--{unsafe_angle}。-->`\n",
        ),
        (
            "double delimiter later-line opener",
            f"``reader-visible prefix\n<!--{unsafe_angle}。-->``\n",
        ),
    ):
        multiline_comment_code_failures = document_reader_visible_policy_errors(
            multiline_comment_code,
            f"unsupported multiline inline-code comment fixture {name}",
        )
        if not any(
            "unsupported or multiline Markdown inline-code span" in failure
            for failure in multiline_comment_code_failures
        ):
            error(
                "reader-visible adapter accepted a multiline comment-shaped "
                f"inline-code span ({name})"
            )

    for name, safe_multiline_code in (
        ("single delimiter", "`Entry\nPoint`\n"),
        ("double delimiter", "``Entry\nPoint``\n"),
        (
            "unclosed literal before actual comment",
            "`<!-- actual non-rendered comment -->\n",
        ),
        (
            "actual multiline comment containing backticks",
            "<!-- `\nnon-rendered comment\n` -->\n",
        ),
    ):
        safe_multiline_failures = document_reader_visible_policy_errors(
            safe_multiline_code,
            f"safe multiline inline-code/comment fixture {name}",
        )
        if safe_multiline_failures:
            error(
                f"reader-visible adapter rejected {name}: "
                f"{safe_multiline_failures!r}"
            )

    unclosed_comment_code_table = (
        "| Field | Value |\n|---|---|\n"
        f"| row | `<!--{unsafe_angle}。--> |\n"
    )
    unclosed_comment_code_table_fields, unclosed_comment_code_table_messages = (
        classified_table_fields(
            unclosed_comment_code_table,
            "unclosed inline-code comment table fixture",
            {FIELD_VALUE_HEADER: 1},
        )
    )
    if unclosed_comment_code_table_messages or policy_errors(
        unclosed_comment_code_table_fields
    ):
        error(
            "reader-visible table adapter did not keep an unmatched literal "
            "backtick and following actual comment safe: "
            f"{unclosed_comment_code_table_messages!r} / "
            f"{policy_errors(unclosed_comment_code_table_fields)!r}"
        )

    actual_comment_unmatched_code_findings = document_reader_visible_policy_errors(
        "<!-- non-rendered comment with an unmatched ` delimiter -->\n",
        "actual comment unmatched inline-code delimiter fixture",
    )
    if actual_comment_unmatched_code_findings:
        error(
            "an unmatched backtick inside an actual HTML comment became "
            f"reader-visible: {actual_comment_unmatched_code_findings!r}"
        )

    for title in ("", ' "visible title"'):
        hidden_url_table = (
            "| Field | Value |\n|---|---|\n"
            f"| row | [runbook](<https://example.com/runbook>{title}) |\n"
        )
        hidden_url_table_fields, hidden_url_table_messages = classified_table_fields(
            hidden_url_table,
            "hidden angle URL table destination fixture",
            {FIELD_VALUE_HEADER: 1},
        )
        hidden_url_table_findings = policy_errors(hidden_url_table_fields)
        if hidden_url_table_messages or hidden_url_table_findings:
            error(
                "hidden angle-bracket table destination became a visible field: "
                f"{hidden_url_table_messages!r} / {hidden_url_table_findings!r}"
            )

    for hidden_destination in (
        "[runbook](<https://example.com/runbook>)",
        '[runbook](<https://example.com/runbook> "visible title")',
    ):
        findings = document_reader_visible_policy_errors(
            hidden_destination,
            "hidden angle URL destination fixture",
        )
        if findings:
            error(
                "hidden angle-bracket Markdown destination became a visible "
                f"host: {findings!r}"
            )
    visible_autolink_findings = document_reader_visible_policy_errors(
        "<https://example.com/runbook>",
        "visible disallowed autolink fixture",
    )
    if not any(
        "[network.host_or_address]" in finding
        and "non-approved host suffix" in finding
        for finding in visible_autolink_findings
    ):
        error("visible non-approved autolink bypassed the host Policy")

    footnote_fixture = (
        "Reader note[^unsafe].\n\n"
        "[^unsafe]: Reader-visible first line.\n"
        "    第三者の本番システムへ接続する。\n"
    )
    footnote_fields = reader_visible_markdown_fields(
        footnote_fixture, "footnote adapter fixture"
    )
    expected_footnote = (
        "footnote adapter fixture:3-4 footnote[unsafe]",
        "Reader-visible first line. 第三者の本番システムへ接続する。",
    )
    if expected_footnote not in footnote_fields:
        error(
            "reader-visible adapter did not select the complete footnote body: "
            f"{footnote_fields!r}"
        )
    footnote_findings = prose_policy_errors(footnote_fields)
    if not any(
        "[target.real_or_external]" in finding and "footnote[unsafe]" in finding
        for finding in footnote_findings
    ):
        error("reader-visible footnote body bypassed Policy 1.2.0")
    safe_footnote_findings = document_reader_visible_policy_errors(
        "Reader note[^safe].\n\n"
        "[^safe]: 第三者の本番システムへ接続することを禁止する。\n",
        "safe footnote adapter fixture",
    )
    if safe_footnote_findings:
        error(
            "reader-visible adapter rejected a safe footnote prohibition: "
            f"{safe_footnote_findings!r}"
        )
    for name, safe_footnote in (
        (
            "hidden link destination",
            "Reader note[^safe].\n\n[^safe]: [runbook](https://example.com/path)\n",
        ),
        (
            "non-rendered comment",
            "Reader note[^safe].\n\n"
            "[^safe]: <!-- 第三者の本番システムへ接続する。 --> safe note.\n",
        ),
    ):
        findings = document_reader_visible_policy_errors(
            safe_footnote, f"safe footnote {name} fixture"
        )
        if findings:
            error(
                f"reader-visible adapter rejected safe footnote {name}: {findings!r}"
            )

    safe_footnote_code = (
        "Reader note[^safe].\n\n"
        "[^safe]: Reader-visible note.\n\n"
        "        <span title=\"第三者の本番システムへ接続しない\">safe</span>\n"
    )
    safe_footnote_code_findings = document_reader_visible_policy_errors(
        safe_footnote_code, "safe footnote indented-code fixture"
    )
    if safe_footnote_code_findings:
        error(
            "footnote indented code was misclassified as interpreted prose: "
            f"{safe_footnote_code_findings!r}"
        )
    unsafe_footnote_code_findings = document_reader_visible_policy_errors(
        safe_footnote_code.replace("接続しない", "接続する", 1),
        "unsafe footnote indented-code fixture",
    )
    if not any(
        "[target.real_or_external]" in finding
        and "footnote[safe]/indented-code[spaces]" in finding
        for finding in unsafe_footnote_code_findings
    ):
        error("reader-visible footnote indented code bypassed Policy 1.2.0")

    safe_footnote_code_table = (
        "Reader note[^safe].\n\n"
        "[^safe]: Reader-visible note.\n\n"
        "        | Field | Value |\n"
        "        |---|---|\n"
        "        | row | 第三者の本番システムへ接続しない |\n"
    )
    safe_code_table_findings = document_reader_visible_policy_errors(
        safe_footnote_code_table,
        "safe footnote indented-code table-like fixture",
    )
    if safe_code_table_findings:
        error(
            "table-like literal inside footnote indented code was misclassified: "
            f"{safe_code_table_findings!r}"
        )
    unsafe_code_table_findings = document_reader_visible_policy_errors(
        safe_footnote_code_table.replace("接続しない", "接続する", 1),
        "unsafe footnote indented-code table-like fixture",
    )
    if not any(
        "[target.real_or_external]" in finding
        and "footnote[safe]/indented-code[spaces]" in finding
        for finding in unsafe_code_table_findings
    ):
        error(
            "table-like literal inside footnote indented code bypassed Policy 1.2.0"
        )

    invalid_footnote = (
        "Reader note[x][^a].\n\n"
        "[^^a]: 第三者の本番システムへ接続する。\n"
    )
    invalid_footnote_fields = reader_visible_markdown_fields(
        invalid_footnote, "invalid double-caret footnote fixture"
    )
    if any("footnote[" in location for location, _ in invalid_footnote_fields):
        error("double-caret link definition was misclassified as a footnote")
    if document_reader_visible_policy_errors(
        invalid_footnote, "invalid double-caret footnote fixture"
    ):
        error("non-rendered double-caret link metadata became Policy-visible")

    footnote_table = (
        "Reader note[^table].\n\n"
        "[^table]: | Field | Value |\n"
        "    |---|---|\n"
        "    | row | safe |\n"
    )
    footnote_table_failures = document_reader_visible_policy_errors(
        footnote_table, "footnote table fixture"
    )
    if not any(
        "Markdown tables inside footnotes are outside the finite adapter contract"
        in failure
        for failure in footnote_table_failures
    ):
        error("footnote table escaped the finite fail-closed adapter boundary")

    for name, raw_html in (
        ("double-quoted title", '<span title="第三者の本番システムへ接続する">safe</span>'),
        ("single-quoted title", "<span title='第三者の本番システムへ接続する'>safe</span>"),
        ("unquoted title", "<span title=第三者の本番システムへ接続する>safe</span>"),
        ("ARIA label", '<span aria-label="第三者の本番システムへ接続する">safe</span>'),
        ("image alt", '<img alt="第三者の本番システムへ接続する">'),
        ("malformed tag", '<span title="第三者の本番システムへ接続する"'),
    ):
        failures = document_reader_visible_policy_errors(
            raw_html, f"raw HTML {name} fixture"
        )
        if not any("interpreted raw HTML is disallowed" in failure for failure in failures):
            error(f"reader-visible adapter accepted interpreted raw HTML {name}")

    raw_html_table = (
        "| Field | Value |\n|---|---|\n"
        '| row | <span title="第三者の本番システムへ接続する">safe</span> |\n'
    )
    _, raw_html_table_messages = classified_table_fields(
        raw_html_table,
        "raw HTML table fixture",
        {FIELD_VALUE_HEADER: 1},
    )
    if not any(
        "table-cell adapter failed closed" in message
        and "interpreted raw HTML is disallowed" in message
        for message in raw_html_table_messages
    ):
        error("reader-visible table adapter accepted interpreted raw HTML")
    tag_destination_table = (
        "| Field | Value |\n|---|---|\n| row | [runbook](<note>) |\n"
    )
    tag_destination_fields, tag_destination_messages = classified_table_fields(
        tag_destination_table,
        "tag-like table link-destination fixture",
        {FIELD_VALUE_HEADER: 1},
    )
    if tag_destination_messages or policy_errors(tag_destination_fields):
        error(
            "tag-like angle-bracket table link destination was treated as raw HTML: "
            f"{tag_destination_messages!r} / {policy_errors(tag_destination_fields)!r}"
        )
    comment_table = (
        "| Field | Value |\n|---|---|\n"
        '| row | safe <!-- <span title="第三者の本番システムへ接続する"> --> text |\n'
    )
    comment_table_fields, comment_table_messages = classified_table_fields(
        comment_table,
        "non-rendered table comment fixture",
        {FIELD_VALUE_HEADER: 1},
    )
    if comment_table_messages or policy_errors(comment_table_fields):
        error(
            "non-rendered table comment affected the reader-visible contract: "
            f"{comment_table_messages!r} / {policy_errors(comment_table_fields)!r}"
        )
    unclosed_comment_table = (
        "| Field | Value |\n|---|---|\n"
        '| row | safe <!-- <span title="hidden"> |\n'
    )
    _, unclosed_comment_messages = classified_table_fields(
        unclosed_comment_table,
        "unclosed table comment fixture",
        {FIELD_VALUE_HEADER: 1},
    )
    if not any(
        "table-cell adapter failed closed" in message
        and "unclosed HTML comment" in message
        for message in unclosed_comment_messages
    ):
        error("reader-visible table adapter accepted an unclosed HTML comment")

    literal_raw_html = (
        '`<span title="第三者の本番システムへ接続する">safe</span>`\n'
    )
    literal_raw_html_findings = document_reader_visible_policy_errors(
        literal_raw_html, "literal inline-code HTML fixture"
    )
    if not any(
        "[target.real_or_external]" in finding
        and "interpreted raw HTML is disallowed" not in finding
        for finding in literal_raw_html_findings
    ):
        error("literal inline-code HTML attribute bypassed Policy 1.2.0")
    for name, literal_source in (
        (
            "escaped tag",
            '\\<span title="第三者の本番システムへ接続する"\\>safe\\</span\\>',
        ),
        (
            "entity-encoded tag",
            '&lt;span title="第三者の本番システムへ接続する"&gt;safe&lt;/span&gt;',
        ),
    ):
        findings = document_reader_visible_policy_errors(
            literal_source, f"unsafe literal {name} fixture"
        )
        if not any("[target.real_or_external]" in finding for finding in findings):
            error(f"reader-visible literal {name} attribute bypassed Policy 1.2.0")
    for name, safe_literal in (
        (
            "inline code",
            '`<span title="第三者の本番システムへ接続しない">safe</span>`',
        ),
        (
            "escaped tag",
            '\\<span title="第三者の本番システムへ接続しない"\\>safe\\</span\\>',
        ),
        (
            "entity-encoded tag",
            '&lt;span title="第三者の本番システムへ接続しない"&gt;safe&lt;/span&gt;',
        ),
        ("approved autolink", "<https://lab.example/runbook>"),
        ("angle-bracket Markdown destination", "[runbook](<local/path>)"),
        ("tag-like Markdown destination", "[runbook](<note>)"),
        (
            "tag-like reference destination",
            "[runbook][ref]\n\n[ref]: <foo-bar>",
        ),
        ("non-rendered comment", '<!-- <span title="第三者の本番システムへ接続する"> -->'),
    ):
        failures = document_reader_visible_policy_errors(
            safe_literal, f"safe raw HTML near-miss {name} fixture"
        )
        if failures:
            error(f"reader-visible adapter rejected raw HTML near-miss {name}: {failures!r}")

    for syntax, unsafe_link, safe_link in (
        (
            "reference double-quoted title",
            '[safe]: /local "第三者の本番システムへ接続する。"\n\n[safe]\n',
            '[safe]: /local "第三者の本番システムへ接続しない。"\n\n[safe]\n',
        ),
        (
            "reference literal-tag title",
            '[safe]: /local "<span title=\'第三者の本番システムへ接続する。\'>safe</span>"\n\n[safe]\n',
            '[safe]: /local "<span title=\'第三者の本番システムへ接続しない。\'>safe</span>"\n\n[safe]\n',
        ),
        (
            "reference comment-shaped title",
            '[safe]: /local "<!--第三者の本番システムへ接続する。-->"\n\n[safe]\n',
            '[safe]: /local "<!--第三者の本番システムへ接続しない。-->"\n\n[safe]\n',
        ),
        (
            "reference single-quoted title",
            "[safe]: /local '第三者の本番システムへ接続する。'\n\n[safe]\n",
            "[safe]: /local '第三者の本番システムへ接続しない。'\n\n[safe]\n",
        ),
        (
            "reference parenthesized title",
            "[safe]: /local (第三者の本番システムへ接続する。)\n\n[safe]\n",
            "[safe]: /local (第三者の本番システムへ接続しない。)\n\n[safe]\n",
        ),
        (
            "inline double-quoted title",
            '[safe](/local "第三者の本番システムへ接続する。")\n',
            '[safe](/local "第三者の本番システムへ接続しない。")\n',
        ),
        (
            "inline literal-tag title",
            '[safe](/local "<span title=\'第三者の本番システムへ接続する。\'>safe</span>")\n',
            '[safe](/local "<span title=\'第三者の本番システムへ接続しない。\'>safe</span>")\n',
        ),
        (
            "inline comment-shaped title",
            '[safe](/local "<!--第三者の本番システムへ接続する。-->")\n',
            '[safe](/local "<!--第三者の本番システムへ接続しない。-->")\n',
        ),
        (
            "inline single-quoted title",
            "[safe](/local '第三者の本番システムへ接続する。')\n",
            "[safe](/local '第三者の本番システムへ接続しない。')\n",
        ),
        (
            "inline parenthesized title",
            "[safe](/local (第三者の本番システムへ接続する。))\n",
            "[safe](/local (第三者の本番システムへ接続しない。))\n",
        ),
        (
            "inline image title",
            '![diagram](/local "第三者の本番システムへ接続する。")\n',
            '![diagram](/local "第三者の本番システムへ接続しない。")\n',
        ),
        (
            "inline image comment-shaped title",
            '![diagram](/local "<!--第三者の本番システムへ接続する。-->")\n',
            '![diagram](/local "<!--第三者の本番システムへ接続しない。-->")\n',
        ),
        (
            "nested-image outer-link title",
            '[![diagram](/assets/diagram.svg)](/local "第三者の本番システムへ接続する。")\n',
            '[![diagram](/assets/diagram.svg)](/local "第三者の本番システムへ接続しない。")\n',
        ),
        (
            "nested-image outer-link comment-shaped title",
            '[![diagram](/assets/diagram.svg)](/local "<!--第三者の本番システムへ接続する。-->")\n',
            '[![diagram](/assets/diagram.svg)](/local "<!--第三者の本番システムへ接続しない。-->")\n',
        ),
    ):
        unsafe_findings = document_reader_visible_policy_errors(
            unsafe_link, f"unsafe {syntax}"
        )
        if not any(
            "[target.real_or_external]" in finding
            and "link-title" in finding
            for finding in unsafe_findings
        ):
            error(f"reader-visible Markdown adapter did not scan {syntax}")
        safe_findings = document_reader_visible_policy_errors(
            safe_link, f"safe {syntax}"
        )
        if safe_findings:
            error(
                f"reader-visible Markdown adapter rejected safe {syntax}: "
                f"{safe_findings!r}"
            )

    for disposition, title, expect_finding in (
        ("unsafe", "第三者の本番システムへ接続する。", True),
        ("safe", "第三者の本番システムへ接続しない。", False),
        (
            "unsafe literal-tag",
            "<span title='第三者の本番システムへ接続する。'>safe</span>",
            True,
        ),
        (
            "safe literal-tag",
            "<span title='第三者の本番システムへ接続しない。'>safe</span>",
            False,
        ),
        (
            "unsafe comment-shaped",
            "<!--第三者の本番システムへ接続する。-->",
            True,
        ),
        (
            "safe comment-shaped",
            "<!--第三者の本番システムへ接続しない。-->",
            False,
        ),
    ):
        table_with_title = (
            "| Field | Value |\n|---|---|\n"
            f'| Link | [safe](/local "{title}") |\n'
        )
        table_fields, table_messages = classified_table_fields(
            table_with_title,
            f"{disposition} table link-title fixture",
            {FIELD_VALUE_HEADER: 1},
        )
        if table_messages:
            error(
                f"{disposition} table link-title fixture invalidated the table "
                f"adapter: {table_messages!r}"
            )
            continue
        table_findings = policy_errors(table_fields)
        observed = any(
            "[target.real_or_external]" in finding and "link-title" in finding
            for finding in table_findings
        )
        if observed != expect_finding:
            error(
                f"{disposition} table link-title Policy result {observed} "
                f"!= {expect_finding}: {table_findings!r}"
            )

    for disposition, title, expect_finding in (
        (
            "unsafe",
            "<!--第三者の本番システムへ接続する。-->",
            True,
        ),
        (
            "safe",
            "<!--第三者の本番システムへ接続しない。-->",
            False,
        ),
    ):
        footnote_with_title = (
            "Reader note.[^title]\n\n"
            f'[^title]: [safe](/local "{title}")\n'
        )
        footnote_findings = document_reader_visible_policy_errors(
            footnote_with_title,
            f"{disposition} footnote comment-shaped link-title fixture",
        )
        observed = any(
            "[target.real_or_external]" in finding
            and "link-title" in finding
            for finding in footnote_findings
        )
        if observed != expect_finding:
            error(
                f"{disposition} footnote comment-shaped link-title result "
                f"{observed} != {expect_finding}: {footnote_findings!r}"
            )

    title_only_findings = document_reader_visible_policy_errors(
        '[safe](https://example.com/runbook "<!--第三者の本番システムへ接続する。-->")\n',
        "comment-shaped visible title with hidden destination fixture",
    )
    title_action_findings = [
        finding
        for finding in title_only_findings
        if "[target.real_or_external]" in finding
    ]
    if len(title_action_findings) != 1 or not all(
        "inline-link-title" in finding for finding in title_action_findings
    ):
        error(
            "comment-shaped Markdown title was not scanned exactly once as "
            f"title metadata: {title_only_findings!r}"
        )
    if any("[network.host_or_address]" in finding for finding in title_only_findings):
        error(
            "hidden Markdown destination leaked into host Policy scanning: "
            f"{title_only_findings!r}"
        )

    actual_comment_with_link = (
        '<!-- [safe](/local "第三者の本番システムへ接続する。") -->\n'
    )
    actual_comment_findings = document_reader_visible_policy_errors(
        actual_comment_with_link,
        "actual comment containing Markdown link-title fixture",
    )
    if actual_comment_findings:
        error(
            "actual non-rendered HTML comment leaked a Markdown title into "
            f"Policy scanning: {actual_comment_findings!r}"
        )

    malformed_table_title = (
        "| Field | Value |\n|---|---|\n"
        '| Link | [safe](/local "unterminated) |\n'
    )
    _, malformed_table_messages = classified_table_fields(
        malformed_table_title,
        "malformed table link-title fixture",
        {FIELD_VALUE_HEADER: 1},
    )
    if not any(
        "table-cell adapter failed closed" in message
        for message in malformed_table_messages
    ):
        error("reader-visible table adapter accepted a malformed inline link title")

    literal_tail = (
        'これはリンクではなく ](/local "第三者の本番システムへ接続する。") '
        "というreader-visible文字列です。\n"
    )
    literal_fields = reader_visible_markdown_fields(
        literal_tail, "literal non-link tail fixture"
    )
    if any("inline-link-title" in location for location, _ in literal_fields):
        error("reader-visible adapter treated a literal ](...) tail as a link title")
    literal_findings = document_reader_visible_policy_errors(
        literal_tail, "literal non-link tail fixture"
    )
    if not any(
        "paragraph" in finding and "[target.real_or_external]" in finding
        for finding in literal_findings
    ) or any("inline-link-title" in finding for finding in literal_findings):
        error(
            "literal ](...) tail did not remain ordinary reader-visible prose: "
            f"{literal_findings!r}"
        )

    for escaped_name, escaped_link in (
        (
            "opening bracket",
            '\\[safe](/local "第三者の本番システムへ接続する。")\n',
        ),
        (
            "closing bracket",
            '[safe\\](/local "第三者の本番システムへ接続する。")\n',
        ),
    ):
        escaped_fields = reader_visible_markdown_fields(
            escaped_link, f"escaped {escaped_name} non-link fixture"
        )
        if any("inline-link-title" in location for location, _ in escaped_fields):
            error(
                f"reader-visible adapter treated an escaped {escaped_name} "
                "literal as a link title"
            )

    literal_table_tail = (
        "| Field | Value |\n|---|---|\n"
        '| Note | 文字列 ](/local "第三者の本番システムへ接続する。") |\n'
    )
    literal_table_fields, literal_table_messages = classified_table_fields(
        literal_table_tail,
        "literal table non-link tail fixture",
        {FIELD_VALUE_HEADER: 1},
    )
    if literal_table_messages:
        error(
            "literal table non-link tail invalidated the finite table adapter: "
            f"{literal_table_messages!r}"
        )
    if any("inline-link-title" in location for location, _ in literal_table_fields):
        error("table adapter treated a literal ](...) tail as a link title")
    literal_table_findings = policy_errors(literal_table_fields)
    if not any(
        " Value row 1:" in finding and "[target.real_or_external]" in finding
        for finding in literal_table_findings
    ) or any("inline-link-title" in finding for finding in literal_table_findings):
        error(
            "literal table ](...) tail did not remain an ordinary scanned cell: "
            f"{literal_table_findings!r}"
        )

    for name, malformed_link in (
        ("unterminated reference title", '[safe]: /local "unterminated\n'),
        (
            "unterminated comment-shaped reference title",
            '[safe]: /local "<!--第三者の本番システムへ接続する。\n',
        ),
        ("multiline reference title", '[safe]: /local\n    "title"\n'),
        ("unterminated inline title", '[safe](/local "unterminated)\n'),
        (
            "unterminated comment-shaped inline title",
            '[safe](/local "<!--第三者の本番システムへ接続する。)\n',
        ),
        ("multiline inline link", '[safe](/local\n "title")\n'),
    ):
        failures = document_reader_visible_policy_errors(
            malformed_link, f"malformed {name}"
        )
        if not any("failed closed" in failure for failure in failures):
            error(f"reader-visible Markdown adapter accepted {name}")

    table = "| Field | Value |\n|---|---|\n| row | ordinary table value |"
    separated_fields = reader_visible_markdown_fields(
        f"Before table.\n\n{table}\n\nAfter table.\n",
        "table boundary fixture",
    )
    if separated_fields != [
        ("table boundary fixture:1-1 paragraph", "Before table."),
        ("table boundary fixture:7-7 paragraph", "After table."),
    ]:
        error(
            "recognized table lines did not preserve the surrounding prose "
            f"block boundary: {separated_fields!r}"
        )
    for position, unsafe_fixture, safe_fixture in (
        (
            "before",
            f"| 第三者の本番システムへ接続する。\n\n{table}\n",
            f"| 第三者の本番システムへ接続しない。\n\n{table}\n",
        ),
        (
            "after",
            f"{table}\n\n| 第三者の本番システムへ接続する。\n",
            f"{table}\n\n| 第三者の本番システムへ接続しない。\n",
        ),
    ):
        unsafe_findings = document_reader_visible_policy_errors(
            unsafe_fixture, f"pipe prose {position} table"
        )
        if not any(
            "[target.real_or_external]" in finding
            and "第三者の本番システムへ接続する" in finding
            for finding in unsafe_findings
        ):
            error(f"pipe-prefixed prose {position} a table bypassed Policy 1.2.0")
        safe_findings = document_reader_visible_policy_errors(
            safe_fixture, f"safe pipe prose {position} table"
        )
        if safe_findings:
            error(
                f"safe pipe-prefixed prose {position} a table was rejected: "
                f"{safe_findings!r}"
            )

    malformed_tables = (
        ("row", "| Field | Value |\n|---|---|\n| malformed row |\n"),
        ("separator", "| Field | Value |\n|--|---|\n| safe | text |\n"),
        ("empty header", "| Field |  |\n|---|---|\n| safe | text |\n"),
        ("duplicate header", "| Field | Field |\n|---|---|\n| safe | text |\n"),
    )
    for name, malformed_table in malformed_tables:
        malformed_failures = document_reader_visible_policy_errors(
            malformed_table, f"malformed {name} table adapter fixture"
        )
        if not any("failed closed" in failure for failure in malformed_failures):
            error(
                "reader-visible prose adapter did not fail closed on a malformed "
                f"table {name}"
            )

    for language, surface in sorted(_READER_VISIBLE_FENCE_LANGUAGES.items()):
        for marker in ("```", "~~~"):
            opener = f"{marker}{language}" if language else marker
            unsafe_fence = f"{opener}\n第三者の本番システムへ接続する\n{marker}\n"
            unsafe_findings = document_reader_visible_policy_errors(
                unsafe_fence, f"fence-language {language or 'plain'} {marker[0]}"
            )
            if not any("[target.real_or_external]" in finding for finding in unsafe_findings):
                error(
                    f"reader-visible fence language {language!r}/{surface!r} with "
                    f"{marker[0]!r} marker bypassed Policy 1.2.0"
                )
            safe_fence = f"{opener}\n第三者の本番システムへ接続しない\n{marker}\n"
            safe_findings = document_reader_visible_policy_errors(
                safe_fence, f"safe fence-language {language or 'plain'} {marker[0]}"
            )
            if safe_findings:
                error(
                    f"reader-visible fence language {language!r}/{surface!r} with "
                    f"{marker[0]!r} marker rejected a safe prohibition: {safe_findings!r}"
                )

    literal_unsafe = (
        '```text\n<span title="第三者の本番システムへ接続する">safe</span>\n```',
        "```text\n<!-- 第三者の本番システムへ接続する -->\n```",
        "```text\n第三者の本番<!--x-->システムへ接続する\n```",
        "```text\n第三者の本番&lt;!--x--&gt;システムへ接続する\n```",
        "```markdown\n第三者の[本番](https://lab.example)システムへ接続する\n```",
        "```markdown\n第三者の[本番][x]システムへ接続する\n[x]: https://lab.example/path\n```",
        "```markdown\n第三者の[本番][]システムへ接続する\n[本番]: https://lab.example/path\n```",
        "```markdown\n第三者の[本番]システムへ接続する\n```",
        "```markdown\n第三者の![本番][x]システムへ接続する\n[x]: https://lab.example/ref\n```",
        "```markdown\n第三者の![本番]システムへ接続する\n```",
        "```markdown\n第三者の![本番システムへ接続する\n```",
        "```markdown\n<!-- 第三者の![本番システムへ接続する -->\n```",
        "```markdown\n[runbook](https://example.com/path)\n```",
    )
    for sample in literal_unsafe:
        findings = document_reader_visible_policy_errors(sample, "literal fenced fixture")
        if not findings:
            error(f"literal fenced source bypassed the shared Policy: {sample!r}")
    literal_safe = (
        '```text\n<span title="第三者の本番システムへ接続しない">safe</span>\n```',
        "```text\n<!-- 第三者の本番システムへ接続しない -->\n```",
        "```text\n第三者の本番システムへ接続し<!--x-->ない\n```",
        "```markdown\n第三者の本番システムへ接続し[ない](https://lab.example)\n```",
        "```markdown\n第三者の本番システムへ接続し[ない][x]\n[x]: https://lab.example/path\n```",
        "```markdown\n第三者の本番システムへ接続し![ない][x]\n[x]: https://lab.example/ref\n```",
        "```markdown\n第三者の本番システムへ接続し![ない]\n```",
        "```markdown\n第三者の本番システムへ接続し![ない\n```",
        "```markdown\n<!-- 第三者の本番システムへ接続し![ない -->\n```",
        "```markdown\n[runbook](https://lab.example/path)\n```",
    )
    for sample in literal_safe:
        findings = document_reader_visible_policy_errors(sample, "safe literal fenced fixture")
        if findings:
            error(f"safe literal fenced source produced findings: {sample!r}: {findings!r}")
    host_probes = {
        "SP 800-30 Rev.1を参照する": (),
        "billing-bridge.exampleへ接続しない": ("billing-bridge.example",),
        "example.comへ接続しない": ("example.com",),
        "192.0.2.10を記録する": ("192.0.2.10",),
        "<https://example.com/path>": ("https://example.com/path",),
        "接続先は例え.localhostです": ("例え.localhost",),
        "URL: https://例え.example/path": ("https://例え.example/path",),
    }
    for sample, expected in host_probes.items():
        observed = visible_host_tokens(sample)
        if observed != expected:
            error(f"visible host-token extraction drift for {sample!r}: {observed!r} != {expected!r}")

    comment_unsafe = (
        "説明 <!-- hidden --> 第三者の本番システムへ接続する",
        "第三者の本番システムへ接続する <!-- hidden -->",
        "<!-- hidden --> 第三者の本番システムへ接続する",
        "第三者の本番<!-- hidden\n-->システムへ接続する",
    )
    for sample in comment_unsafe:
        findings = document_reader_visible_policy_errors(sample, "inline-comment fixture")
        if not any("[target.real_or_external]" in finding for finding in findings):
            error(f"reader-visible prose adapter hid unsafe text beside an HTML comment: {sample!r}")
    if document_reader_visible_policy_errors(
        "説明 <!-- hidden --> 第三者の本番システムへ接続しない",
        "safe inline-comment fixture",
    ):
        error("reader-visible prose adapter rejected a locally prohibited action beside an HTML comment")

    unsafe_host_samples = (
        "<https://example.com/path>",
        "接続先は例え.localhostです",
    )
    for sample in unsafe_host_samples:
        findings = prose_policy_findings([("visible-host fixture", sample)])
        if not any(finding.category == "network.host_or_address" for finding in findings):
            error(f"reader-visible prose adapter accepted a non-approved visible host: {sample!r}")
    safe_host_samples = (
        "<https://lab.example/path>",
        "URL: https://例え.example/path",
    )
    for sample in safe_host_samples:
        findings = prose_policy_findings([("safe visible-host fixture", sample)])
        if findings:
            error(
                f"reader-visible prose adapter rejected an approved visible host: {sample!r}: "
                f"{[format_finding(finding) for finding in findings]!r}"
            )
    malformed = (
        "---\ntitle: unclosed",
        "```text\nhidden remainder",
        "```python\nprint('reader-visible but unclassified')\n```",
        "```text {.unsafe}\nreader-visible\n```",
        "````text\nreader-visible\n```",
        "- ```text\n  reader-visible\n  ```",
        "> > > > ```text\n> > > > reader-visible\n> > > > ```",
        "\t```text\n\treader-visible\n\t```",
        "<!-- hidden remainder",
    )
    for sample in malformed:
        failures = document_reader_visible_policy_errors(sample, "malformed prose fixture")
        if not any("failed closed" in failure for failure in failures):
            error(f"reader-visible prose adapter accepted malformed Markdown boundary: {sample!r}")


def chapter_contract_errors(text: str, label: str) -> list[str]:
    messages: list[str] = []
    messages.extend(require_order(label, text, EXPECTED_HEADINGS))
    required = (
        "Decision Requirement\n→ Business Outcome / Asset",
        "→ Evidence Requirement / Action / Reassessment",
        "Componentを列挙するだけでは",
        "`Business Asset`は8番目のTypeではなく",
        "Network segmentはBoundary候補に過ぎない",
        "Threat、Vulnerability、Finding",
        "`Threat`は、望ましくない事象や行為である。",
        "`Vulnerability`は、そのThreatを成立させやすい弱点や条件である。",
        "`Finding`は、許可された範囲でEvidenceに支えられて確認した環境固有の結論である。",
        "Attack Path`と実行可能な侵害手順",
        "権限拡大の仮説 → Token scope過大の状態 → Data APIへの到達可能性 → 監査欠落による検知遅延",
        "Unknown / Assumed / Confirmed / Not Applicable",
        "Draft / In Review / Approved for Assessment / Needs Evidence / Superseded",
        "Candidate / Supported / Partially Supported / Disconfirmed / Inconclusive",
        "Unknown / Documented / Implemented / Observed / Validated",
        "Gap statusは Open / Accepted temporarily / Escalated / Closed",
        "Evidence Requirement`と`Collected Evidence",
        "Unknown`がGapへ変換",
        "文書化されたControlがあるので十分である\n誤りである",
        "CSFやOWASPへMappingしたので完全である\n誤りである",
        "Threat countの多さではない",
        "本章の成果物は、Capabilityの証拠候補にはなるが、Review、Rubric、再評価なしに能力証明にはならない",
        "[Threat Model](../templates/threat-model.md)",
        "[第4章 合成記入例](../cases/ch04-threat-model-example.md)",
        "https://itdojp.github.io/pentest-learning-book/",
        "https://itdojp.github.io/practical-auth-book/",
        "https://itdojp.github.io/it-infra-security-guide-book/",
        "委譲先を読まなくても、本章の中心論旨は切れない",
        "CASE-2026-001",
        "DR-2026-001",
        "AUTH-CASE-2026-001",
        "Chapter 5",
        "Chapter 6",
        "Chapter 9",
        "Chapter 11",
        "第15章",
        "Chapter 27",
        "F-04-01",
        "F-04-02",
        "T-04-01",
        "T-04-02",
        "T-04-03",
        "T-04-04",
        "実在Targetが必要になった",
        "実CredentialやPIIが必要になった",
        "手順が実行可能な侵害手順へ寄り始めた",
        "Authorization条件が不明になった",
        "一つの仮説を最後まで通す記入例",
        "`ART-03`の正本構造は、Templateと合成記入例で共通する次の13節（番号0〜12）である",
        "10. `Assumptions, Unknowns and Gaps`",
        "11. `Evidence Requirements and Actions`",
        "12. `Reassessment and Handoff`",
        "13. `Review and Rubric`",
        "`RUBRIC-TM-YYYY-001` Asset taxonomy",
        "`RUBRIC-TM-YYYY-002` Boundary and flow clarity",
        "`RUBRIC-TM-YYYY-003` Threat usefulness and evidence sufficiency",
        "`RUBRIC-TM-YYYY-004` Safety and authorization",
        "`RUBRIC-TM-YYYY-005` Decision handoff quality",
    )
    messages.extend(require_tokens(label, text, required))

    if text.count(CHAPTER_WALKTHROUGH_TRACE) != 1:
        messages.append(
            f"{label}: Chapter 4 walkthrough must contain exactly one frozen "
            "TH-2026-004 / PATH-2026-001 historical-current-summary trace"
        )
    walkthrough_match = re.search(
        r"^#### 一つの仮説を最後まで通す記入例\s*$\n"
        r"(?P<body>.*?)(?=^#{1,4} |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if walkthrough_match is None:
        messages.append(f"{label}: missing bounded Chapter 4 walkthrough section")
    else:
        walkthrough = walkthrough_match.group("body")
        if "`TH-2026-001`" in walkthrough:
            messages.append(
                f"{label}: walkthrough must not assign the summary-only refinement "
                "to inherited composite TH-2026-001"
            )

    if text.count("F-04-01") < 2 or text.count("F-04-02") < 2:
        messages.append(f"{label}: both figure IDs must be defined and referenced")
    for table_id in ("T-04-01", "T-04-02", "T-04-03", "T-04-04"):
        if text.count(table_id) != 1:
            messages.append(f"{label}: {table_id} must occur exactly once")
    for heading in EXPECTED_CHAPTER_MARKDOWN_TABLE_HEADINGS:
        rendered_table_pattern = re.compile(
            rf"^### {re.escape(heading)}\n\n(?:\|[^\n]*\|\n)+\n(?=\S)",
            re.MULTILINE,
        )
        if len(rendered_table_pattern.findall(text)) != 1:
            messages.append(
                f"{label}: {heading} must have blank lines before and after its "
                "Markdown table so the published page renders one semantic table"
            )

    body, marker, references = text.partition("## 参考資料")
    if not marker:
        messages.append(f"{label}: missing reference section")
    elif source_ids(body) != EXPECTED_SOURCE_IDS:
        messages.append(f"{label}: body source IDs {sorted(source_ids(body))!r} != {sorted(EXPECTED_SOURCE_IDS)!r}")
    if source_ids(references) != EXPECTED_SOURCE_IDS:
        messages.append(f"{label}: chapter-end source IDs {sorted(source_ids(references))!r} != body IDs")

    exercise = section(text, "## 安全な演習")
    if not exercise:
        messages.append(f"{label}: missing bounded safe exercise section")
    chapter_control_ids = set(re.findall(r"\bCTRL-2026-\d{3}\b", text))
    if chapter_control_ids != {"CTRL-2026-005", "CTRL-2026-006"}:
        messages.append(
            f"{label}: introductory Control trace must use the paired fresh Chapter 4 "
            f"scope/identity Controls CTRL-2026-005 and CTRL-2026-006; "
            f"found {sorted(chapter_control_ids)!r}"
        )
    fields, adapter_messages = classified_table_fields(
        text, label, CHAPTER_TABLE_OCCURRENCES
    )
    messages.extend(adapter_messages)
    messages.extend(policy_errors(fields))
    messages.extend(document_reader_visible_policy_errors(text, label))
    return messages


def template_contract_errors(text: str, label: str) -> list[str]:
    messages = require_order(label, text, EXPECTED_TEMPLATE_HEADINGS)
    required = (
        "ART-03",
        "Model status | Draft / In Review / Approved for Assessment / Needs Evidence / Superseded",
        "Business Outcome / Service / Component / Data / Identity / Control Plane / Evidence",
        "Business Assetは8番目のTypeではない",
        "Unknown / Assumed / Confirmed / Not Applicable",
        "Data / Identity / Control",
        "Evidence statusは Planned / Collected / Rejected / Inconclusive",
        "Identity Authority / Data Ownership / Administrative Control / Tenant / Third-party Responsibility / Control Plane / Network",
        "Candidate / Supported / Partially Supported / Disconfirmed / Inconclusive",
        "Unknown / Documented / Implemented / Observed / Validated",
        "Gap statusは Open / Accepted temporarily / Escalated / Closed",
        "| Attack Path ID | Edge ID | From Asset / State | Condition | Boundary ID | To Asset / State | Affected Asset IDs | Expected impact | Observation point | Required Evidence ID | Knowledge state |",
        "Do not include commands.",
        "Do not include payload strings.",
        "Do not include exploit steps",
        "Do not include credentials, tokens, cookies, or secrets.",
        "Do not include real target identifiers",
        "| Gap ID | Missing information / control / telemetry | Decision affected | Owner | Due date | Status | Evidence Requirement ID | Action ID | Reassessment ID |",
        "| Evidence Requirement ID | Question | Related Threat / Control / Gap | Minimum sufficient evidence | Forbidden / over-collection boundary | Owner | Due date | Status | Resulting Evidence IDs |",
        "| Evidence ID | Related Evidence Requirement IDs | Evidence description | Collection conditions / provenance | Status | Reviewer | Collected at | Limitation |",
        "Evidence RequirementのStatusは Required / Deferred / Replaced / Not Applicable",
        "| Entry Point ID | Related Exposure IDs | Interface class | Description | Owner | Boundary IDs | Required authority | Observation point | Knowledge state | Evidence IDs |",
        "| Dependency ID | From asset | To asset | Why the dependency matters | Failure consequence |",
        "| Rubric ID | Criterion | Meets | Partially meets | Does not meet |",
        "| Limitation ID | Scope / condition | Unsupported claim | Owner | Reassessment trigger |",
        "ACT-TM-YYYY-NNN",
        "REA-TM-YYYY-NNN",
        "| Reassessment ID | Trigger | Scope | Owner | Scheduled date | Inputs required | Closure criteria | Destination chapter / artifact |",
    )
    messages.extend(require_tokens(label, text, required))

    document_rows, document_messages = table_by_header(
        section(text, "## 0. Document Control"), ("Field", "Value"), label
    )
    messages.extend(document_messages)
    document_fields = tuple(row[0] for row in document_rows if len(row) == 2)
    if document_fields != DOCUMENT_CONTROL_FIELDS:
        messages.append(
            f"{label}: Document Control fields/order {document_fields!r} != {DOCUMENT_CONTROL_FIELDS!r}"
        )

    template_flow_header = (
        "Flow ID",
        "Flow type",
        "Source Asset ID",
        "Destination Asset ID",
        "Purpose",
        "Protocol class",
        "Identity / authorization context",
        "Boundary IDs crossed",
        "Data classification",
        "Evidence status",
        "Observation point",
    )
    template_flow_rows, template_flow_messages = table_by_header(text, template_flow_header, label)
    messages.extend(template_flow_messages)
    evidence_status_index = template_flow_header.index("Evidence status")
    for row in template_flow_rows:
        if len(row) != len(template_flow_header):
            continue
        value = row[evidence_status_index]
        if value and value not in COLLECTED_EVIDENCE_STATUSES:
            messages.append(f"{label}: Flow Evidence status outside finite set: {value!r}")

    template_gap_rows, template_gap_messages = table_by_header(text, GAP_HEADER, label)
    messages.extend(template_gap_messages)
    gap_status_index = GAP_HEADER.index("Status")
    for row in template_gap_rows:
        if len(row) != len(GAP_HEADER):
            continue
        value = row[gap_status_index]
        if value and value not in GAP_STATUSES:
            messages.append(f"{label}: Gap status outside finite set: {value!r}")

    template_evidence_rows, template_evidence_messages = table_by_header(
        text, COLLECTED_EVIDENCE_HEADER, label
    )
    messages.extend(template_evidence_messages)
    collected_status_index = COLLECTED_EVIDENCE_HEADER.index("Status")
    for row in template_evidence_rows:
        if len(row) != len(COLLECTED_EVIDENCE_HEADER):
            continue
        value = row[collected_status_index]
        if value and value not in COLLECTED_EVIDENCE_STATUSES:
            messages.append(f"{label}: Collected Evidence status outside finite set: {value!r}")

    fields, adapter_messages = classified_table_fields(text, label, TEMPLATE_TABLE_OCCURRENCES)
    messages.extend(adapter_messages)
    decision_rows, decision_messages = table_by_header(
        section(text, "## 1. Decision Context"), ("Field", "Value"), label
    )
    messages.extend(decision_messages)
    decision_fields = tuple(row[0] for row in decision_rows if len(row) == 2)
    if decision_fields != DECISION_CONTEXT_FIELDS:
        messages.append(
            f"{label}: Decision Context fields/order {decision_fields!r} != {DECISION_CONTEXT_FIELDS!r}"
        )
    messages.extend(policy_errors(fields))
    messages.extend(document_reader_visible_policy_errors(text, label))
    return messages


def case_contract_errors(text: str, label: str) -> list[str]:
    messages: list[str] = []
    messages.extend(require_order(label, text, EXPECTED_CASE_HEADINGS))
    observed_h2 = tuple(re.findall(r"^## .+$", text, re.MULTILINE))
    if observed_h2 != EXPECTED_CASE_HEADINGS:
        messages.append(f"{label}: top-level headings {observed_h2!r} != {EXPECTED_CASE_HEADINGS!r}")
    required = (
        "ART-03",
        "TM-2026-001",
        "CASE-2026-001",
        "DR-2026-001",
        "AUTH-CASE-2026-001",
        "Proceed with conditions",
        "COND-AUTH-2026-001",
        "COND-AUTH-2026-002",
        "COND-AUTH-2026-003",
        "Telemetry absence is not absence of compromise",
        "Business Assetは8番目のTypeではなく",
        "Evidence Requirement status",
        "Collected Evidence status",
        "同一Evidence IDは原典の取得時刻、取得主体、条件、制約を置換しない",
        "Inherited Negative Finding Register",
        "standaloneの`Collected at`がないため、時刻を創作せず",
        "Gap status",
        "合成Tenant A → 合成Tenant B",
        "Tenant間分離の不確実性",
        "Entry PointはExposureの参照列だけで済ませず",
        "ASSET-2026-001",
        "ASSET-2026-002",
        "ASSET-2026-003",
        "ASSET-2026-004",
        "ASSET-2026-005",
        "ASSET-2026-006",
        "ASSET-2026-007",
        "FLOW-2026-001",
        "TB-2026-001",
        "TB-2026-002",
        "TB-2026-003",
        "TH-2026-001",
        "TH-2026-002",
        "TH-2026-003",
        "TH-2026-004",
        "TH-2026-005",
        "MISUSE-2026-001",
        "MISUSE-2026-002",
        "PATH-2026-001",
        "PATH-2026-002",
        "CTRL-2026-005",
        "CTRL-2026-006",
        "CTRL-2026-007",
        "CTRL-2026-008",
        "CTRL-2026-009",
        "ASM-2026-001",
        "ASM-2026-002",
        "ASM-2026-003",
        "GAP-2026-001",
        "GAP-2026-002",
        "GAP-2026-003",
        "GAP-2026-004",
        "EREQ-2026-001",
        "EREQ-2026-002",
        "EREQ-2026-003",
        "EREQ-2026-004",
        "ACT-TM-2026-001",
        "ACT-TM-2026-006",
        "REA-TM-2026-001",
        "REA-TM-2026-004",
    )
    messages.extend(require_tokens(label, text, required))

    field_rows, field_messages = table_by_header(
        section(text, "## 0. Document Control"), ("Field", "Value"), label
    )
    messages.extend(field_messages)
    document_fields = {row[0]: row[1] for row in field_rows if len(row) == 2}
    if document_fields.get("Model status") not in MODEL_STATUSES:
        messages.append(f"{label}: Model status outside finite set: {document_fields.get('Model status')!r}")
    expected_document_fields = {
        "Artifact ID": "`ART-03`",
        "Threat Model ID": "`TM-2026-001`",
        "Parent Case ID": "`CASE-2026-001`",
        "Relation": "`refines`",
        "Decision Requirement ID": "`DR-2026-001`",
        "Authorization Record ID": "`AUTH-CASE-2026-001`",
    }
    for field, expected_value in expected_document_fields.items():
        if document_fields.get(field) != expected_value:
            messages.append(
                f"{label}: Document Control {field!r} {document_fields.get(field)!r} != {expected_value!r}"
            )
    if document_fields.get("Threat Model ID") == document_fields.get("Parent Case ID"):
        messages.append(f"{label}: Threat Model cannot be its own parent")
    observed_document_fields = tuple(row[0] for row in field_rows if len(row) == 2)
    if observed_document_fields != DOCUMENT_CONTROL_FIELDS:
        messages.append(
            f"{label}: Document Control fields/order {observed_document_fields!r} != {DOCUMENT_CONTROL_FIELDS!r}"
        )

    decision_rows, decision_messages = table_by_header(
        section(text, "## 1. Decision Context"), ("Field", "Value"), label
    )
    messages.extend(decision_messages)
    observed_decision_fields = tuple(row[0] for row in decision_rows if len(row) == 2)
    if observed_decision_fields != DECISION_CONTEXT_FIELDS:
        messages.append(
            f"{label}: Decision Context fields/order {observed_decision_fields!r} != {DECISION_CONTEXT_FIELDS!r}"
        )

    table_contracts: tuple[tuple[tuple[str, ...], str, set[str], int], ...] = (
        (("Asset ID", "Type", "Name", "Business role / outcome", "Owner", "Criticality", "Data classification", "Knowledge state", "Evidence IDs", "Dependency IDs"), "Type", ASSET_TYPES, 7),
        (("Flow ID", "Flow type", "Source Asset ID", "Destination Asset ID", "Purpose", "Protocol class", "Identity / authorization context", "Boundary IDs crossed", "Data classification", "Evidence status", "Observation point"), "Flow type", FLOW_TYPES, 3),
        (("Boundary ID", "Boundary type", "From / To", "Owner(s)", "Trust / authority change", "Crossing condition", "Control", "Failure consequence", "Knowledge state", "Evidence IDs"), "Boundary type", BOUNDARY_TYPES, 5),
        (("Hypothesis ID", "Decision Requirement ID", "Related Asset IDs", "Boundary / Flow / Exposure IDs", "Statement", "Preconditions", "Expected impact", "Evidence needed", "Alternative explanation", "Priority", "Hypothesis status"), "Hypothesis status", HYPOTHESIS_STATUSES, 3),
        (("Control ID", "Related Asset / Boundary / Threat / Path IDs", "Control statement", "Owner", "Assurance state", "Evidence IDs", "Limitation", "Gap ID", "Reassessment trigger"), "Assurance state", ASSURANCE_STATES, 5),
    )
    parsed: dict[tuple[str, ...], list[list[str]]] = {}
    for header, finite_column, allowed, minimum_rows in table_contracts:
        rows, table_messages = table_by_header(text, header, label)
        messages.extend(table_messages)
        parsed[header] = rows
        if len(rows) < minimum_rows:
            messages.append(f"{label}: {header[0]} table requires at least {minimum_rows} rows")
        index = header.index(finite_column)
        values = {row[index] for row in rows if len(row) == len(header)}
        if not values <= allowed:
            messages.append(f"{label}: {finite_column} values outside finite set: {sorted(values - allowed)!r}")
        if header[0] in {"Asset ID", "Flow ID"} and values != allowed:
            messages.append(f"{label}: {finite_column} coverage {sorted(values)!r} != {sorted(allowed)!r}")
        for row in rows:
            if len(row) == len(header) and any(not cell for cell in row):
                messages.append(f"{label}: {header[0]} row contains an empty required cell: {row!r}")

    boundary_header = table_contracts[2][0]
    boundary_values = {row[1] for row in parsed.get(boundary_header, []) if len(row) == len(boundary_header)}
    if len(boundary_values) < 5:
        messages.append(f"{label}: requires at least five distinct boundary types")

    chapter1_boundary_header = (
        "Boundary ID",
        "From",
        "To",
        "Identity / protocol",
        "Control",
        "Failure consequence",
    )
    chapter1_case = read_text("cases/ch01-integrated-security-case-example.md")
    chapter1_boundary_rows, chapter1_boundary_messages = table_by_header(
        chapter1_case,
        chapter1_boundary_header,
        "cases/ch01-integrated-security-case-example.md",
    )
    messages.extend(chapter1_boundary_messages)
    boundary_rows_by_id = {
        row[0].strip("`"): row
        for row in parsed.get(boundary_header, [])
        if len(row) == len(boundary_header)
    }
    expected_inherited_boundary_ids = {
        "TB-2026-001",
        "TB-2026-002",
        "TB-2026-003",
    }
    chapter1_boundary_ids = [
        row[0].strip("`")
        for row in chapter1_boundary_rows
        if len(row) == len(chapter1_boundary_header)
    ]
    for inherited_id in sorted(expected_inherited_boundary_ids):
        source_matches = [
            row
            for row in chapter1_boundary_rows
            if len(row) == len(chapter1_boundary_header)
            and row[0].strip("`") == inherited_id
        ]
        if len(source_matches) != 1:
            messages.append(
                f"{label}: Chapter 1 must define inherited boundary {inherited_id} "
                f"exactly once; found {chapter1_boundary_ids.count(inherited_id)}"
            )
            continue
        chapter4_inherited_boundary = boundary_rows_by_id.get(inherited_id)
        if chapter4_inherited_boundary is None:
            messages.append(f"{label}: missing inherited boundary {inherited_id}")
            continue
        source_boundary = source_matches[0]
        inherited_contract = {
            "From / To": f"{source_boundary[1]} → {source_boundary[2]}",
            "Crossing condition": source_boundary[3],
            "Control": source_boundary[4],
            "Failure consequence": source_boundary[5],
        }
        for field, expected in inherited_contract.items():
            observed = chapter4_inherited_boundary[boundary_header.index(field)]
            if observed != expected:
                messages.append(
                    f"{label}: {inherited_id} {field} {observed!r} must preserve "
                    f"Chapter 1 value {expected!r}"
                )

    requirement_configuration_boundary = boundary_rows_by_id.get("TB-2026-009")
    if requirement_configuration_boundary is None:
        messages.append(
            f"{label}: missing Chapter 4 requirement-to-configuration boundary TB-2026-009"
        )
    else:
        expected_requirement_configuration_fields = {
            "Boundary type": "Administrative Control",
            "From / To": "業務要件とscope承認 → Identity control planeのApp設定",
            "Trust / authority change": "業務上の要件判断が管理者同意へ変換される",
            "Crossing condition": "scope追加または例外承認が必要",
            "Control": "Admin consent、scope review、二者Review",
            "Failure consequence": "過大権限または未承認同意",
        }
        for field, expected in expected_requirement_configuration_fields.items():
            observed = requirement_configuration_boundary[boundary_header.index(field)]
            if observed != expected:
                messages.append(
                    f"{label}: TB-2026-009 {field} {observed!r} != "
                    f"requirement-to-configuration contract {expected!r}"
                )

    refinement_boundary = boundary_rows_by_id.get("TB-2026-008")
    if refinement_boundary is None:
        messages.append(f"{label}: missing summary-only refinement boundary TB-2026-008")
    else:
        refinement_text = " ".join(refinement_boundary)
        for marker in ("invoice-sync-manifest", "summary-only"):
            if marker not in refinement_text:
                messages.append(f"{label}: TB-2026-008 summary-only refinement missing {marker!r}")

    lab_boundary = boundary_rows_by_id.get("TB-2026-006")
    if lab_boundary is None:
        messages.append(f"{label}: missing synthetic lab boundary TB-2026-006")
    else:
        knowledge_state = lab_boundary[boundary_header.index("Knowledge state")]
        if knowledge_state != "Assumed":
            messages.append(
                f"{label}: TB-2026-006 must remain Assumed until preflight/default-deny/"
                f"cleanup behavior Evidence is collected; found {knowledge_state!r}"
            )

    identity_boundary = boundary_rows_by_id.get("TB-2026-004")
    if identity_boundary is None:
        messages.append(f"{label}: missing current identity boundary TB-2026-004")
    else:
        expected_identity_boundary_fields = {
            "Boundary type": "Identity Authority",
            "From / To": "Workload identity → OAuth app runtime session",
            "Knowledge state": "Unknown",
            "Evidence IDs": "-",
        }
        for field, expected in expected_identity_boundary_fields.items():
            observed = identity_boundary[boundary_header.index(field)]
            if observed != expected:
                messages.append(
                    f"{label}: TB-2026-004 {field} {observed!r} != current-binding "
                    f"contract {expected!r}"
                )
    if text.count(TB_004_CURRENT_BINDING_BOUNDARY) != 1:
        messages.append(
            f"{label}: requires one exact TB-2026-004 historical/current Evidence boundary"
        )

    flow_header = table_contracts[1][0]
    evidence_status_index = flow_header.index("Evidence status")
    flow_evidence_statuses = {
        row[evidence_status_index]
        for row in parsed.get(flow_header, [])
        if len(row) == len(flow_header)
    }
    if not flow_evidence_statuses <= COLLECTED_EVIDENCE_STATUSES:
        messages.append(
            f"{label}: Flow Evidence status values outside finite set: "
            f"{sorted(flow_evidence_statuses - COLLECTED_EVIDENCE_STATUSES)!r}"
        )

    asset_header = table_contracts[0][0]
    for row in parsed.get(asset_header, []):
        if len(row) != len(asset_header):
            continue
        knowledge_state = row[asset_header.index("Knowledge state")]
        evidence_ids = row[asset_header.index("Evidence IDs")]
        if knowledge_state == "Confirmed" and evidence_ids in {"-", "None", "TBD", "Unknown"}:
            messages.append(
                f"{label}: Confirmed Asset requires an Evidence ID rather than {evidence_ids!r}: {row[0]!r}"
            )

    hypothesis_header = table_contracts[3][0]
    hypothesis_rows = {
        row[hypothesis_header.index("Hypothesis ID")].strip("`"): row
        for row in parsed.get(hypothesis_header, [])
        if len(row) == len(hypothesis_header)
    }
    chapter1_hypothesis_header = (
        "Hypothesis ID",
        "Related Decision Requirement ID",
        "Related Asset IDs",
        "Related Boundary IDs",
        "Statement",
        "Preconditions",
        "Expected impact",
        "Priority",
        "Status",
    )
    chapter1_hypothesis_rows, chapter1_hypothesis_messages = table_by_header(
        chapter1_case,
        chapter1_hypothesis_header,
        "cases/ch01-integrated-security-case-example.md",
    )
    messages.extend(chapter1_hypothesis_messages)
    source_th_001 = next(
        (
            row
            for row in chapter1_hypothesis_rows
            if len(row) == len(chapter1_hypothesis_header)
            and row[0].strip("`") == "TH-2026-001"
        ),
        None,
    )
    inherited_th_001 = hypothesis_rows.get("TH-2026-001")
    if source_th_001 is None:
        messages.append(f"{label}: Chapter 1 must define inherited hypothesis TH-2026-001")
    elif inherited_th_001 is None:
        messages.append(f"{label}: missing inherited hypothesis TH-2026-001")
    else:
        exact_fields = {
            "Decision Requirement ID": source_th_001[1],
            "Related Asset IDs": source_th_001[2],
            # The Chapter 1 action-bearing prose is preserved semantically in a
            # non-operational nominal proposition so the public-content Policy
            # does not mistake a threat statement for an instruction.
            "Statement": INHERITED_TH_001_CASE_PROPOSITION,
            "Preconditions": INHERITED_TH_001_CASE_PRECONDITIONS,
            "Expected impact": source_th_001[6],
            "Priority": source_th_001[7],
            "Hypothesis status": source_th_001[8],
        }
        for field, expected in exact_fields.items():
            observed = inherited_th_001[hypothesis_header.index(field)]
            if observed != expected:
                messages.append(
                    f"{label}: TH-2026-001 {field} {observed!r} must match "
                    f"the inherited semantic contract {expected!r}"
                )
        inherited_boundaries = set(re.findall(r"\bTB-2026-\d{3}\b", source_th_001[3]))
        chapter4_boundaries = set(
            re.findall(
                r"\bTB-2026-\d{3}\b",
                inherited_th_001[hypothesis_header.index("Boundary / Flow / Exposure IDs")],
            )
        )
        if not inherited_boundaries <= chapter4_boundaries:
            messages.append(
                f"{label}: TH-2026-001 dropped inherited boundary IDs "
                f"{sorted(inherited_boundaries - chapter4_boundaries)!r}"
            )
        if source_th_001[4] != INHERITED_TH_001_PROPOSITION:
            messages.append(
                f"{label}: Chapter 1 TH-2026-001 proposition drifted from the frozen "
                f"contract {INHERITED_TH_001_PROPOSITION!r}"
            )

    source_th_002 = next(
        (
            row
            for row in chapter1_hypothesis_rows
            if len(row) == len(chapter1_hypothesis_header)
            and row[0].strip("`") == "TH-2026-002"
        ),
        None,
    )
    inherited_th_002 = hypothesis_rows.get("TH-2026-002")
    if source_th_002 is None:
        messages.append(f"{label}: Chapter 1 must define inherited hypothesis TH-2026-002")
    elif inherited_th_002 is None:
        messages.append(f"{label}: missing inherited hypothesis TH-2026-002")
    else:
        frozen_source_fields = {
            "Decision Requirement ID": source_th_002[1],
            "Related Asset IDs": source_th_002[2],
            "Statement": source_th_002[4],
            "Preconditions": source_th_002[5],
            "Expected impact": source_th_002[6],
            "Priority": source_th_002[7],
        }
        for field, expected in frozen_source_fields.items():
            observed = inherited_th_002[hypothesis_header.index(field)]
            if observed != expected:
                messages.append(
                    f"{label}: TH-2026-002 {field} {observed!r} must preserve "
                    f"the Chapter 1 source-derived value {expected!r}"
                )
        exact_chapter4_fields = {
            "Boundary / Flow / Exposure IDs": INHERITED_TH_002_CASE_RELATIONS,
            "Evidence needed": "`EREQ-2026-002`",
            "Alternative explanation": INHERITED_TH_002_ALTERNATIVE,
            # Chapter 1 uses ``Partially supported``. ART-03 normalizes only
            # capitalization to its finite status vocabulary; the proposition
            # and evaluation meaning remain unchanged.
            "Hypothesis status": "Partially Supported",
        }
        for field, expected in exact_chapter4_fields.items():
            observed = inherited_th_002[hypothesis_header.index(field)]
            if observed != expected:
                messages.append(
                    f"{label}: TH-2026-002 {field} {observed!r} != frozen "
                    f"Chapter 4 inherited value {expected!r}"
                )
        source_contract = {
            "Statement": INHERITED_TH_002_PROPOSITION,
            "Preconditions": INHERITED_TH_002_PRECONDITIONS,
            "Expected impact": INHERITED_TH_002_IMPACT,
            "Priority": "High",
            "Status": "Partially supported",
        }
        for field, expected in source_contract.items():
            observed = source_th_002[chapter1_hypothesis_header.index(field)]
            if observed != expected:
                messages.append(
                    f"{label}: Chapter 1 TH-2026-002 {field} {observed!r} drifted "
                    f"from frozen source value {expected!r}"
                )
        inherited_boundaries = set(re.findall(r"\bTB-2026-\d{3}\b", source_th_002[3]))
        chapter4_boundaries = set(
            re.findall(
                r"\bTB-2026-\d{3}\b",
                inherited_th_002[
                    hypothesis_header.index("Boundary / Flow / Exposure IDs")
                ],
            )
        )
        if not inherited_boundaries <= chapter4_boundaries:
            messages.append(
                f"{label}: TH-2026-002 dropped inherited boundary IDs "
                f"{sorted(inherited_boundaries - chapter4_boundaries)!r}"
            )

    summary_th_004 = hypothesis_rows.get("TH-2026-004")
    if summary_th_004 is None:
        messages.append(f"{label}: missing summary-only refinement hypothesis TH-2026-004")
    else:
        summary_contract = {
            "Decision Requirement ID": "`DR-2026-001`",
            "Related Asset IDs": (
                "`ASSET-2026-001`, `ASSET-2026-005`, `ASSET-2026-006`, "
                "`ASSET-2026-007`"
            ),
            "Boundary / Flow / Exposure IDs": (
                "`TB-2026-004`, `TB-2026-008`, `TB-2026-009`, `FLOW-2026-001`, "
                "`FLOW-2026-002`, `FLOW-2026-003`, `FLOW-2026-006`, "
                "`EXP-2026-001`, `EXP-2026-003`"
            ),
            "Statement": SUMMARY_TH_004_PROPOSITION,
            "Preconditions": (
                "2026-07-25 remediation後のcurrent scopeとWorkload identity bindingが未確認である"
            ),
            "Expected impact": "合成Dataの同期状態と業務判断への影響が拡大する",
            "Evidence needed": "`EREQ-2026-001`, `EREQ-2026-003`",
            "Alternative explanation": (
                "post-remediation current scopeは必要最小権限で、historical broad scopeが"
                "解消済みかもしれない"
            ),
            "Priority": "High",
            "Hypothesis status": "Inconclusive",
        }
        for field, expected in summary_contract.items():
            observed = summary_th_004[hypothesis_header.index(field)]
            if observed != expected:
                messages.append(
                    f"{label}: TH-2026-004 {field} {observed!r} != frozen "
                    f"summary-only value {expected!r}"
                )
        statement = summary_th_004[hypothesis_header.index("Statement")]
        relations = summary_th_004[hypothesis_header.index("Boundary / Flow / Exposure IDs")]
        if "TB-2026-008" not in relations or "TB-2026-002" in relations:
            messages.append(
                f"{label}: TH-2026-004 must bind summary-only TB-2026-008 without "
                f"overwriting inherited customer-data TB-2026-002: {relations!r}"
            )
        if statement == INHERITED_TH_001_PROPOSITION:
            messages.append(
                f"{label}: TH-2026-004 must remain a distinct summary-only proposition"
            )

    lifecycle_th_005 = hypothesis_rows.get("TH-2026-005")
    if lifecycle_th_005 is None:
        messages.append(
            f"{label}: missing App lifecycle / decision-summary refinement TH-2026-005"
        )
    else:
        lifecycle_contract = {
            "Decision Requirement ID": "`DR-2026-001`",
            "Related Asset IDs": (
                "`ASSET-2026-002`, `ASSET-2026-003`, `ASSET-2026-004`"
            ),
            "Boundary / Flow / Exposure IDs": LIFECYCLE_TH_005_RELATIONS,
            "Statement": LIFECYCLE_TH_005_PROPOSITION,
            "Preconditions": LIFECYCLE_TH_005_PRECONDITIONS,
            "Expected impact": LIFECYCLE_TH_005_IMPACT,
            "Evidence needed": "`EREQ-2026-002`",
            "Alternative explanation": (
                "Eventは存在するがsummary Field不足で見えないだけかもしれない"
            ),
            "Priority": "High",
            "Hypothesis status": "Partially Supported",
        }
        for field, expected in lifecycle_contract.items():
            observed = lifecycle_th_005[hypothesis_header.index(field)]
            if observed != expected:
                messages.append(
                    f"{label}: TH-2026-005 {field} {observed!r} != frozen "
                    f"lifecycle / decision-summary value {expected!r}"
                )
        if lifecycle_th_005[hypothesis_header.index("Statement")] == INHERITED_TH_002_PROPOSITION:
            messages.append(
                f"{label}: TH-2026-005 must remain distinct from inherited TH-2026-002"
            )
    decision_summary_definition = (
        "ここでdecision summary Fieldとは、`FLOW-2026-005`でAudit Evidenceを"
        "月末判断へ渡す無害化summaryのFieldであり、Admin consent EventやRule"
        "そのものではない。"
    )
    if text.count(decision_summary_definition) != 1:
        messages.append(
            f"{label}: decision summary Field must have exactly one reader-visible "
            f"FLOW-2026-005 definition distinct from TH-2026-002"
        )

    source_th_003 = next(
        (
            row
            for row in chapter1_hypothesis_rows
            if len(row) == len(chapter1_hypothesis_header)
            and row[0].strip("`") == "TH-2026-003"
        ),
        None,
    )
    inherited_th_003 = hypothesis_rows.get("TH-2026-003")
    if source_th_003 is None:
        messages.append(f"{label}: Chapter 1 must define inherited hypothesis TH-2026-003")
    elif inherited_th_003 is None:
        messages.append(f"{label}: missing inherited hypothesis TH-2026-003")
    else:
        source_frozen_contract = {
            "Related Decision Requirement ID": "`DR-2026-001`",
            "Related Asset IDs": INHERITED_TH_003_ASSETS,
            "Related Boundary IDs": INHERITED_TH_003_RELATIONS,
            "Statement": INHERITED_TH_003_PROPOSITION,
            "Preconditions": INHERITED_TH_003_PRECONDITIONS,
            "Expected impact": INHERITED_TH_003_IMPACT,
            "Priority": "High",
            "Status": "Inconclusive",
        }
        for field, expected in source_frozen_contract.items():
            observed = source_th_003[chapter1_hypothesis_header.index(field)]
            if observed != expected:
                messages.append(
                    f"{label}: Chapter 1 TH-2026-003 {field} {observed!r} drifted "
                    f"from frozen source value {expected!r}"
                )

        inherited_source_fields = {
            "Decision Requirement ID": source_th_003[1],
            "Related Asset IDs": source_th_003[2],
            "Boundary / Flow / Exposure IDs": source_th_003[3],
            "Statement": source_th_003[4],
            "Preconditions": source_th_003[5],
            "Expected impact": source_th_003[6],
            "Priority": source_th_003[7],
            "Hypothesis status": source_th_003[8],
            "Evidence needed": "`EREQ-2026-003`",
            "Alternative explanation": INHERITED_TH_003_ALTERNATIVE,
        }
        for field, expected in inherited_source_fields.items():
            observed = inherited_th_003[hypothesis_header.index(field)]
            if observed != expected:
                messages.append(
                    f"{label}: TH-2026-003 {field} {observed!r} must preserve "
                    f"the Chapter 1 source-derived contract {expected!r}"
                )

    opportunity_th_006 = hypothesis_rows.get("TH-2026-006")
    if opportunity_th_006 is None:
        messages.append(
            f"{label}: missing opportunity / summary-only refinement hypothesis TH-2026-006"
        )
    else:
        opportunity_contract = {
            "Decision Requirement ID": "`DR-2026-001`",
            "Related Asset IDs": (
                "`ASSET-2026-001`, `ASSET-2026-003`, `ASSET-2026-006`"
            ),
            "Boundary / Flow / Exposure IDs": OPPORTUNITY_TH_006_RELATIONS,
            "Statement": OPPORTUNITY_TH_006_PROPOSITION,
            "Preconditions": OPPORTUNITY_TH_006_PRECONDITIONS,
            "Expected impact": OPPORTUNITY_TH_006_IMPACT,
            "Evidence needed": "`EREQ-2026-003`",
            "Alternative explanation": OPPORTUNITY_TH_006_ALTERNATIVE,
            "Priority": "High",
            "Hypothesis status": "Inconclusive",
        }
        for field, expected in opportunity_contract.items():
            observed = opportunity_th_006[hypothesis_header.index(field)]
            if observed != expected:
                messages.append(
                    f"{label}: TH-2026-006 {field} {observed!r} != frozen "
                    f"opportunity / summary-only value {expected!r}"
                )
        if opportunity_th_006[hypothesis_header.index("Statement")] == INHERITED_TH_003_PROPOSITION:
            messages.append(
                f"{label}: TH-2026-006 must remain distinct from inherited TH-2026-003"
            )

    count_contracts = (
        (("Exposure ID", "Related Asset / Boundary / Flow IDs", "Entry Point ID", "Reachability class", "External dependency", "Required authority", "Verification status", "Evidence ID", "Gap ID"), 3),
        (("Misuse Case ID", "Goal", "Actor capability class", "Preconditions", "Affected assets", "Boundary crossed", "Expected outcome", "Observation points", "Excluded operational detail"), 2),
        (("Attack Path ID", "Edge ID", "From Asset / State", "Condition", "Boundary ID", "To Asset / State", "Affected Asset IDs", "Expected impact", "Observation point", "Required Evidence ID", "Knowledge state"), 2),
        (("Assumption ID", "Statement", "Owner", "Validation method", "Due date", "Status", "Related IDs"), 3),
        (GAP_HEADER, 3),
        (("Evidence Requirement ID", "Question", "Related Threat / Control / Gap", "Minimum sufficient evidence", "Forbidden / over-collection boundary", "Owner", "Due date", "Status", "Resulting Evidence IDs"), 3),
        (("Reassessment ID", "Trigger", "Scope", "Owner", "Scheduled date", "Inputs required", "Closure criteria", "Destination chapter / artifact"), 3),
    )
    case_tables: dict[tuple[str, ...], list[list[str]]] = {}
    for header, minimum_rows in count_contracts:
        rows, table_messages = table_by_header(text, header, label)
        messages.extend(table_messages)
        case_tables[header] = rows
        if len(rows) < minimum_rows:
            messages.append(f"{label}: {header[0]} table requires at least {minimum_rows} rows")
        for row in rows:
            if len(row) == len(header) and any(not cell for cell in row):
                messages.append(f"{label}: {header[0]} row contains an empty required cell: {row!r}")

    entry_point_header = (
        "Entry Point ID",
        "Related Exposure IDs",
        "Interface class",
        "Description",
        "Owner",
        "Boundary IDs",
        "Required authority",
        "Observation point",
        "Knowledge state",
        "Evidence IDs",
    )
    entry_point_rows, entry_point_messages = table_by_header(text, entry_point_header, label)
    messages.extend(entry_point_messages)
    if len(entry_point_rows) < 3:
        messages.append(f"{label}: Entry Point Detail Register requires at least three rows")
    for row in entry_point_rows:
        if len(row) == len(entry_point_header) and any(not cell for cell in row):
            messages.append(f"{label}: Entry Point row contains an empty required cell: {row!r}")
        if len(row) == len(entry_point_header) and row[8] not in KNOWLEDGE_STATES:
            messages.append(f"{label}: Entry Point Knowledge state outside finite set: {row[8]!r}")

    evidence_requirement_header = count_contracts[5][0]
    evidence_requirement_status_index = evidence_requirement_header.index("Status")
    evidence_requirement_statuses = {
        row[evidence_requirement_status_index]
        for row in case_tables.get(evidence_requirement_header, [])
        if len(row) == len(evidence_requirement_header)
    }
    if not evidence_requirement_statuses <= EVIDENCE_REQUIREMENT_STATUSES:
        messages.append(
            f"{label}: Evidence Requirement status values outside finite set: "
            f"{sorted(evidence_requirement_statuses - EVIDENCE_REQUIREMENT_STATUSES)!r}"
        )

    gap_header = count_contracts[4][0]
    gap_status_index = gap_header.index("Status")
    gap_statuses = {
        row[gap_status_index]
        for row in case_tables.get(gap_header, [])
        if len(row) == len(gap_header)
    }
    if not gap_statuses <= GAP_STATUSES:
        messages.append(f"{label}: Gap status values outside finite set: {sorted(gap_statuses - GAP_STATUSES)!r}")

    collected_rows, collected_messages = table_by_header(text, COLLECTED_EVIDENCE_HEADER, label)
    messages.extend(collected_messages)
    if len(collected_rows) != 5:
        messages.append(f"{label}: Collected Evidence Register must contain exactly five inherited Evidence rows")
    collected_status_index = COLLECTED_EVIDENCE_HEADER.index("Status")
    collected_statuses = {
        row[collected_status_index]
        for row in collected_rows
        if len(row) == len(COLLECTED_EVIDENCE_HEADER)
    }
    if not collected_statuses <= COLLECTED_EVIDENCE_STATUSES:
        messages.append(
            f"{label}: Collected Evidence status values outside finite set: "
            f"{sorted(collected_statuses - COLLECTED_EVIDENCE_STATUSES)!r}"
        )
    collected_ids = {
        row[0].strip("`")
        for row in collected_rows
        if len(row) == len(COLLECTED_EVIDENCE_HEADER)
    }
    if collected_ids != EXPECTED_INHERITED_COLLECTED_EVIDENCE_IDS:
        messages.append(
            f"{label}: Collected Evidence IDs {sorted(collected_ids)!r} "
            f"!= inherited Collected Evidence IDs {sorted(EXPECTED_INHERITED_COLLECTED_EVIDENCE_IDS)!r}"
        )

    chapter1_evidence_header = (
        "Evidence ID",
        "Observation ID",
        "Validation ID",
        "Authority / RoE ID",
        "Question supported",
        "Source / collector",
        "Collected at",
        "Integrity / hash",
        "Limitation",
        "Classification",
    )
    chapter1_case = read_text("cases/ch01-integrated-security-case-example.md")
    chapter1_evidence_rows, source_messages = table_by_header(
        chapter1_case,
        chapter1_evidence_header,
        "cases/ch01-integrated-security-case-example.md",
    )
    messages.extend(source_messages)
    expected_inherited_rows: dict[str, tuple[str, str, str, str, str, str]] = {}
    for row in chapter1_evidence_rows:
        if len(row) != len(chapter1_evidence_header):
            continue
        identifier = row[0].strip("`")
        if identifier not in EXPECTED_INHERITED_COLLECTED_EVIDENCE_IDS:
            continue
        expected_inherited_rows[identifier] = (
            row[4],
            f"第1章継承: {row[5]}; Observation {row[1]}; Validation {row[2]}; "
            f"Authority / RoE {row[3]}; Integrity / hash {row[7]}; Classification {row[9]}",
            "Collected",
            INHERITED_REVIEWER_VALUE,
            row[6],
            row[8],
        )

    chapter2_evidence_header = (
        "Evidence ID",
        "Description",
        "Source / custodian",
        "Collected at",
        "Integrity / reference",
        "Limitation",
    )
    chapter2_case = read_text("cases/ch02-authorization-decision-example.md")
    chapter2_evidence_rows, source_messages = table_by_header(
        chapter2_case,
        chapter2_evidence_header,
        "cases/ch02-authorization-decision-example.md",
    )
    messages.extend(source_messages)
    for row in chapter2_evidence_rows:
        if len(row) != len(chapter2_evidence_header) or row[0].strip("`") != "EVD-AUTH-2026-001":
            continue
        expected_inherited_rows["EVD-AUTH-2026-001"] = (
            row[1],
            f"第2章継承: Source / custodian {row[2]}; Integrity / reference {row[4]}",
            "Collected",
            INHERITED_REVIEWER_VALUE,
            row[3],
            row[5],
        )

    if set(expected_inherited_rows) != EXPECTED_INHERITED_COLLECTED_EVIDENCE_IDS:
        messages.append(
            f"{label}: source-derived inherited Evidence contracts {sorted(expected_inherited_rows)!r} "
            f"!= {sorted(EXPECTED_INHERITED_COLLECTED_EVIDENCE_IDS)!r}"
        )
    observed_inherited_rows = {
        row[0].strip("`"): (row[2], row[3], row[4], row[5], row[6], row[7])
        for row in collected_rows
        if len(row) == len(COLLECTED_EVIDENCE_HEADER)
    }
    requirement_bindings: dict[str, list[str]] = {}
    for row in case_tables.get(evidence_requirement_header, []):
        if len(row) != len(evidence_requirement_header):
            continue
        requirement_id = row[evidence_requirement_header.index("Evidence Requirement ID")].strip("`")
        resulting = row[evidence_requirement_header.index("Resulting Evidence IDs")]
        for identifier in re.findall(r"\b(?:EVD(?:-AUTH)?-2026-\d{3}|NEG-2026-\d{3})\b", resulting):
            requirement_bindings.setdefault(identifier, []).append(requirement_id)
    for row in collected_rows:
        if len(row) != len(COLLECTED_EVIDENCE_HEADER):
            continue
        identifier = row[0].strip("`")
        expected_relation = ", ".join(
            f"`{requirement_id}`" for requirement_id in requirement_bindings.get(identifier, [])
        ) or "-"
        if row[1] != expected_relation:
            messages.append(
                f"{label}: {identifier} Related Evidence Requirement IDs {row[1]!r} "
                f"!= Resulting Evidence binding {expected_relation!r}"
            )
    for identifier, expected_row in expected_inherited_rows.items():
        if observed_inherited_rows.get(identifier) != expected_row:
            messages.append(
                f"{label}: inherited Evidence metadata drift for {identifier}: "
                f"{observed_inherited_rows.get(identifier)!r} != {expected_row!r}"
            )

    chapter1_negative_rows, source_messages = table_by_header(
        chapter1_case,
        NEGATIVE_FINDING_HEADER,
        "cases/ch01-integrated-security-case-example.md",
    )
    messages.extend(source_messages)
    case_negative_rows, negative_messages = table_by_header(text, NEGATIVE_FINDING_HEADER, label)
    messages.extend(negative_messages)
    inherited_negative = [
        row for row in chapter1_negative_rows if row and row[0].strip("`") == "NEG-2026-001"
    ]
    if len(inherited_negative) != 1 or case_negative_rows != inherited_negative:
        messages.append(
            f"{label}: NEG-2026-001 must preserve the exact Chapter 1 Negative Finding row "
            f"without an invented timestamp"
        )

    control_header = table_contracts[4][0]
    controls_by_id = {
        row[0].strip("`"): row
        for row in parsed.get(control_header, [])
        if len(row) == len(control_header)
    }
    chapter1_control_rows, source_control_messages = table_by_header(
        chapter1_case,
        CHAPTER1_CONTROL_HEADER,
        "cases/ch01-integrated-security-case-example.md",
    )
    messages.extend(source_control_messages)
    source_control_ids = [
        row[0].strip("`")
        for row in chapter1_control_rows
        if len(row) == len(CHAPTER1_CONTROL_HEADER)
    ]
    if set(source_control_ids) != EXPECTED_INHERITED_CONTROL_IDS:
        messages.append(
            f"{label}: Chapter 1 inherited Control IDs {sorted(set(source_control_ids))!r} "
            f"!= {sorted(EXPECTED_INHERITED_CONTROL_IDS)!r}"
        )
    duplicate_source_controls = sorted(
        identifier for identifier, count in Counter(source_control_ids).items() if count != 1
    )
    if duplicate_source_controls:
        messages.append(
            f"{label}: Chapter 1 inherited Control IDs must be defined exactly once: "
            f"{duplicate_source_controls!r}"
        )
    source_controls_by_id = {
        row[0].strip("`"): row
        for row in chapter1_control_rows
        if len(row) == len(CHAPTER1_CONTROL_HEADER)
    }
    for identifier, row in source_controls_by_id.items():
        if any(not cell for cell in row):
            messages.append(
                f"{label}: Chapter 1 inherited Control {identifier} has an empty "
                f"meaning/Evidence/Result field: {row!r}"
            )

    reused_inherited_ids = sorted(set(controls_by_id) & EXPECTED_INHERITED_CONTROL_IDS)
    if reused_inherited_ids:
        messages.append(
            f"{label}: Chapter 4 must not redefine inherited Chapter 1 Control IDs: "
            f"{reused_inherited_ids!r}"
        )
    if set(controls_by_id) != set(CHAPTER4_CONTROL_RELATIONS):
        messages.append(
            f"{label}: Chapter 4 Control definitions {sorted(controls_by_id)!r} != "
            f"fresh Control relation IDs {sorted(CHAPTER4_CONTROL_RELATIONS)!r}"
        )
    requirement_configuration_control = controls_by_id.get("CTRL-2026-005")
    if requirement_configuration_control is None:
        messages.append(f"{label}: missing requirement-to-configuration Control CTRL-2026-005")
    else:
        control_boundary_ids = set(
            re.findall(
                r"\bTB-2026-\d{3}\b",
                requirement_configuration_control[
                    control_header.index("Related Asset / Boundary / Threat / Path IDs")
                ],
            )
        )
        if control_boundary_ids != {"TB-2026-009"}:
            messages.append(
                f"{label}: CTRL-2026-005 boundary references "
                f"{sorted(control_boundary_ids)!r} != ['TB-2026-009']"
            )

    if text.count("### Control IDの継承境界") != 1:
        messages.append(f"{label}: requires exactly one Control ID inheritance boundary heading")
    for chapter4_id, (relation, inherited_id) in CHAPTER4_CONTROL_RELATIONS.items():
        if relation == "independent":
            expected_line = (
                f"- `{chapter4_id}`は第4章固有のLab safety Controlであり、"
                "第1章Controlからindependentである。"
            )
        else:
            source_row = source_controls_by_id.get(inherited_id or "")
            if source_row is None:
                messages.append(
                    f"{label}: {chapter4_id} cannot derive {relation} relation from "
                    f"missing Chapter 1 Control {inherited_id!r}"
                )
                continue
            improvement = source_row[CHAPTER1_CONTROL_HEADER.index("Improvement")]
            result = source_row[CHAPTER1_CONTROL_HEADER.index("Result")]
            expected_line = (
                f"- `{chapter4_id}`は第1章`{inherited_id}`「{improvement}」"
                f"（Result: {result}）をsupportsする別Controlであり、正本Controlを置換しない。"
            )
        if text.count(expected_line) != 1:
            messages.append(
                f"{label}: {chapter4_id} must record exactly one source-derived "
                f"Control identity relation: {expected_line!r}"
            )
    inheritance_boundary = (
        "`supports`は同一Controlを意味しない。第1章のControl proposition、Verification、"
        "Resultは第1章Caseを正本とし、第4章のassurance stateやEvidenceへ上書きしない。"
    )
    if text.count(inheritance_boundary) != 1:
        messages.append(
            f"{label}: missing exact Control identity non-replacement boundary "
            f"{inheritance_boundary!r}"
        )

    # The current-state decision must reconcile the source chronology rather
    # than treating a pre-remediation snapshot as if it described the model's
    # August timestamp.  Both values are derived from the Chapter 1 source so
    # a later edit cannot silently move the dates or manufacture a newer
    # observation in Chapter 4.
    source_scope_evidence = expected_inherited_rows.get("EVD-2026-001")
    if source_scope_evidence is None or source_scope_evidence[4] != "2026-07-20T13:20:00+09:00":
        messages.append(
            f"{label}: Chapter 1 EVD-2026-001 must remain the 2026-07-20 scope snapshot"
        )
    source_scope_control = source_controls_by_id.get("CTRL-2026-001")
    if source_scope_control is None:
        messages.append(f"{label}: missing Chapter 1 CTRL-2026-001 remediation source")
    else:
        expected_scope_control = {
            "Improvement": "必要scopeだけへ縮小",
            "Due date": "2026-07-25",
            "Result": "Passed",
        }
        for field, expected in expected_scope_control.items():
            observed = source_scope_control[CHAPTER1_CONTROL_HEADER.index(field)]
            if observed != expected:
                messages.append(
                    f"{label}: Chapter 1 CTRL-2026-001 {field} {observed!r} != {expected!r}"
                )
    temporal_boundary = (
        "`EVD-2026-001`は2026-07-20のhistorical scope Snapshotであり、"
        "第1章`CTRL-2026-001`が2026-07-25にscope縮小`Passed`を記録した後の"
        "current scopeは、post-remediation Snapshotを収集するまで`Unknown`としてDecisionへ渡す。"
    )
    if text.count(temporal_boundary) != 1:
        messages.append(
            f"{label}: requires one exact historical/current scope boundary: "
            f"{temporal_boundary!r}"
        )

    lab_control = controls_by_id.get("CTRL-2026-008")
    if lab_control is None:
        messages.append(f"{label}: missing CTRL-2026-008 assurance contract")
    else:
        assurance = lab_control[control_header.index("Assurance state")]
        evidence_ids = lab_control[control_header.index("Evidence IDs")]
        limitation = lab_control[control_header.index("Limitation")]
        gap_id = lab_control[control_header.index("Gap ID")]
        if assurance != "Documented":
            messages.append(
                f"{label}: CTRL-2026-008 must remain Documented until explicit synthetic "
                f"preflight/default-deny/cleanup behavior Evidence exists; found {assurance!r}"
            )
        if evidence_ids != "`EVD-AUTH-2026-001`, `SYNTH-REV-TM-SAFE-001`":
            messages.append(f"{label}: CTRL-2026-008 review Evidence binding drift: {evidence_ids!r}")
        if gap_id != "`GAP-2026-004`":
            messages.append(
                f"{label}: CTRL-2026-008 must link to its dedicated lab-safety Gap "
                f"GAP-2026-004; found {gap_id!r}"
            )
        for marker in (
            "preflight",
            "default-deny",
            "Cleanup",
            "実施結果は未収集",
            "Controlの挙動は未観測",
        ):
            if marker not in limitation:
                messages.append(f"{label}: CTRL-2026-008 limitation missing {marker!r}")

    identity_control = controls_by_id.get("CTRL-2026-006")
    if identity_control is None:
        messages.append(f"{label}: missing CTRL-2026-006 identity-assurance contract")
    else:
        expected_identity_fields = {
            "Assurance state": "Documented",
            "Evidence IDs": "`EVD-2026-001`",
            "Gap ID": "`GAP-2026-002`",
        }
        for field, expected in expected_identity_fields.items():
            observed = identity_control[control_header.index(field)]
            if observed != expected:
                messages.append(
                    f"{label}: CTRL-2026-006 {field} {observed!r} != {expected!r}"
                )
        identity_limitation = identity_control[control_header.index("Limitation")]
        for marker in (
            "App registration scope Snapshotに限られ",
            "Workload identity binding snapshot",
            "rotation手順Review記録",
            "offline機械的突合結果",
            "未収集",
        ):
            if marker not in identity_limitation:
                messages.append(
                    f"{label}: CTRL-2026-006 limitation missing {marker!r}"
                )

    audit_control = controls_by_id.get("CTRL-2026-007")
    if audit_control is None:
        messages.append(f"{label}: missing CTRL-2026-007 composite audit-assurance contract")
    else:
        expected_audit_fields = {
            "Control statement": (
                "Admin consentとApp identity lifecycle EventのAudit coverageを維持する"
            ),
            "Assurance state": "Documented",
            "Evidence IDs": "`EVD-2026-003`",
            "Gap ID": "`GAP-2026-003`",
        }
        for field, expected in expected_audit_fields.items():
            observed = audit_control[control_header.index(field)]
            if observed != expected:
                messages.append(
                    f"{label}: CTRL-2026-007 {field} {observed!r} != {expected!r}"
                )
        audit_limitation = audit_control[control_header.index("Limitation")]
        for marker in (
            "EVD-2026-003",
            "Admin consent Eventだけを観測",
            "App identity lifecycle EventのCoverage",
            "Rule test結果は未収集",
            "複合Control全体の挙動は未観測",
        ):
            if marker not in audit_limitation:
                messages.append(f"{label}: CTRL-2026-007 limitation missing {marker!r}")

    assumption_header = count_contracts[3][0]
    for row in case_tables.get(assumption_header, []):
        if len(row) == len(assumption_header) and row[5] not in KNOWLEDGE_STATES:
            messages.append(f"{label}: Assumption status outside finite set: {row[5]!r}")

    path_header = count_contracts[2][0]
    path_rows = case_tables.get(path_header, [])
    if len({row[0] for row in path_rows if row}) != 2:
        messages.append(f"{label}: exactly two Attack Path IDs must own the edge rows")
    operational_pattern = re.compile(r"(?:^|\s)(?:curl|wget|powershell|bash|sh|python|nmap|sqlmap)\s|```(?:bash|sh|powershell)|(?:payload|command)\s*[:=]", re.IGNORECASE)
    for row in path_rows:
        joined = " ".join(row)
        if operational_pattern.search(joined):
            messages.append(f"{label}: Attack Path contains an executable command or payload marker: {joined!r}")
    path_rows_by_edge = {row[1].strip("`"): row for row in path_rows if len(row) == len(path_header)}
    edge001 = path_rows_by_edge.get("EDGE-2026-001")
    edge002 = path_rows_by_edge.get("EDGE-2026-002")
    edge004 = path_rows_by_edge.get("EDGE-2026-004")
    edge007 = path_rows_by_edge.get("EDGE-2026-007")
    if edge001 is None:
        messages.append(f"{label}: missing historical scope edge EDGE-2026-001")
    else:
        expected_historical_edge_markers = {
            "From Asset / State": ("2026-07-20", "historical"),
            "Condition": ("historical Snapshot",),
            "To Asset / State": ("historical broad-scope snapshot",),
            "Observation point": ("2026-07-20 App registration export",),
        }
        for field, markers in expected_historical_edge_markers.items():
            value = edge001[path_header.index(field)]
            for marker in markers:
                if marker not in value:
                    messages.append(f"{label}: EDGE-2026-001 {field} missing {marker!r}")
        if edge001[path_header.index("Knowledge state")] != "Confirmed":
            messages.append(
                f"{label}: EDGE-2026-001 historical snapshot must remain Confirmed"
            )
        if edge001[path_header.index("Boundary ID")] != "`TB-2026-009`":
            messages.append(
                f"{label}: EDGE-2026-001 must use fresh requirement-to-configuration "
                "boundary TB-2026-009"
            )
    if edge002 is None:
        messages.append(f"{label}: missing current-scope edge EDGE-2026-002")
    else:
        expected_current_edge_markers = {
            "From Asset / State": ("post-remediation scope unknown",),
            "Condition": ("2026-07-25", "Passed", "current App registration exportが未収集"),
            "To Asset / State": ("current binding scope unknown",),
            "Expected impact": ("current影響範囲を確定できない",),
            "Observation point": (
                "post-remediation App registration export",
                "Workload identity binding snapshot",
            ),
        }
        for field, markers in expected_current_edge_markers.items():
            value = edge002[path_header.index(field)]
            for marker in markers:
                if marker not in value:
                    messages.append(f"{label}: EDGE-2026-002 {field} missing {marker!r}")
        if edge002[path_header.index("Knowledge state")] != "Unknown":
            messages.append(
                f"{label}: EDGE-2026-002 current post-remediation scope must remain Unknown"
            )
    if edge004 is None or edge004[path_header.index("Boundary ID")] != "`TB-2026-005`":
        messages.append(f"{label}: EDGE-2026-004 must use the Tenant boundary TB-2026-005")
    if edge007 is None or edge007[path_header.index("Boundary ID")] != "`TB-2026-007`":
        messages.append(f"{label}: EDGE-2026-007 must use the third-party responsibility boundary TB-2026-007")

    flow_rows_by_id = {
        row[0].strip("`"): row
        for row in parsed.get(flow_header, [])
        if len(row) == len(flow_header)
    }
    requirement_configuration_flow = flow_rows_by_id.get("FLOW-2026-001")
    if requirement_configuration_flow is None:
        messages.append(f"{label}: missing requirement-to-configuration flow FLOW-2026-001")
    elif requirement_configuration_flow[flow_header.index("Boundary IDs crossed")] != "`TB-2026-009`":
        messages.append(
            f"{label}: FLOW-2026-001 must use fresh requirement-to-configuration "
            "boundary TB-2026-009 without redefining inherited TB-2026-001"
        )
    identity_flow = flow_rows_by_id.get("FLOW-2026-006")
    if identity_flow is None:
        messages.append(f"{label}: missing current workload-identity flow FLOW-2026-006")
    else:
        expected_identity_flow_fields = {
            "Flow type": "Identity",
            "Source Asset ID": "`ASSET-2026-007`",
            "Destination Asset ID": "`ASSET-2026-001`",
            "Evidence status": FLOW_006_EVIDENCE_STATUS,
            "Observation point": FLOW_006_OBSERVATION_POINT,
        }
        for field, expected in expected_identity_flow_fields.items():
            observed = identity_flow[flow_header.index(field)]
            if observed != expected:
                messages.append(
                    f"{label}: FLOW-2026-006 {field} {observed!r} != "
                    f"uncollected current-binding contract {expected!r}"
                )
    composite_audit_flow = flow_rows_by_id.get("FLOW-2026-004")
    if composite_audit_flow is None:
        messages.append(f"{label}: missing composite audit flow FLOW-2026-004")
    else:
        expected_composite_audit_flow_fields = {
            "Purpose": "同意Event・App identity lifecycle Eventの監査Coverage",
            "Evidence status": FLOW_004_EVIDENCE_STATUS,
            "Observation point": FLOW_004_OBSERVATION_POINT,
        }
        for field, expected in expected_composite_audit_flow_fields.items():
            observed = composite_audit_flow[flow_header.index(field)]
            if observed != expected:
                messages.append(
                    f"{label}: FLOW-2026-004 {field} {observed!r} != "
                    f"composite partial-Evidence contract {expected!r}"
                )
    exposure_header = count_contracts[0][0]
    exposure_rows_by_id = {
        row[0].strip("`"): row
        for row in case_tables.get(exposure_header, [])
        if len(row) == len(exposure_header)
    }
    entry_point_rows_by_id = {
        row[0].strip("`"): row
        for row in entry_point_rows
        if len(row) == len(entry_point_header)
    }
    offline_entry_point = entry_point_rows_by_id.get("EP-2026-003")
    if offline_entry_point is None:
        messages.append(f"{label}: missing current-binding review entry point EP-2026-003")
    else:
        expected_offline_entry_fields = {
            "Description": (
                "summary-only manifest fixtureとTenant binding metadataを確認予定の接点"
            ),
            "Observation point": (
                "収集予定: manifest field inventory、Tenant binding差分（current結果は未収集）"
            ),
            "Knowledge state": "Assumed",
            "Evidence IDs": "`EVD-2026-001`, `EVD-2026-002`",
        }
        for field, expected in expected_offline_entry_fields.items():
            observed = offline_entry_point[entry_point_header.index(field)]
            if observed != expected:
                messages.append(
                    f"{label}: EP-2026-003 {field} {observed!r} != "
                    f"bounded uncollected-entry contract {expected!r}"
                )
    if text.count(EP_003_CURRENT_EVIDENCE_BOUNDARY) != 1:
        messages.append(
            f"{label}: requires one exact historical/current EP-2026-003 Evidence boundary"
        )
    summary_boundary_bindings = (
        (
            "EXP-2026-001",
            exposure_rows_by_id.get("EXP-2026-001"),
            exposure_header,
            "Related Asset / Boundary / Flow IDs",
            {"TB-2026-001", "TB-2026-004", "TB-2026-009"},
        ),
        (
            "EP-2026-001",
            entry_point_rows_by_id.get("EP-2026-001"),
            entry_point_header,
            "Boundary IDs",
            {"TB-2026-001", "TB-2026-004", "TB-2026-009"},
        ),
        (
            "FLOW-2026-003",
            flow_rows_by_id.get("FLOW-2026-003"),
            flow_header,
            "Boundary IDs crossed",
            {"TB-2026-006", "TB-2026-008"},
        ),
        (
            "EXP-2026-003",
            exposure_rows_by_id.get("EXP-2026-003"),
            exposure_header,
            "Related Asset / Boundary / Flow IDs",
            {"TB-2026-005", "TB-2026-006", "TB-2026-008"},
        ),
        (
            "EP-2026-003",
            entry_point_rows_by_id.get("EP-2026-003"),
            entry_point_header,
            "Boundary IDs",
            {"TB-2026-005", "TB-2026-006", "TB-2026-008"},
        ),
        (
            "EDGE-2026-003",
            path_rows_by_edge.get("EDGE-2026-003"),
            path_header,
            "Boundary ID",
            {"TB-2026-008"},
        ),
        (
            "TH-2026-001",
            hypothesis_rows.get("TH-2026-001"),
            hypothesis_header,
            "Boundary / Flow / Exposure IDs",
            {"TB-2026-001", "TB-2026-002", "TB-2026-004"},
        ),
        (
            "TH-2026-004",
            hypothesis_rows.get("TH-2026-004"),
            hypothesis_header,
            "Boundary / Flow / Exposure IDs",
            {"TB-2026-004", "TB-2026-008", "TB-2026-009"},
        ),
        (
            "TH-2026-002",
            hypothesis_rows.get("TH-2026-002"),
            hypothesis_header,
            "Boundary / Flow / Exposure IDs",
            {"TB-2026-001", "TB-2026-003"},
        ),
        (
            "TH-2026-005",
            hypothesis_rows.get("TH-2026-005"),
            hypothesis_header,
            "Boundary / Flow / Exposure IDs",
            {"TB-2026-003", "TB-2026-007"},
        ),
        (
            "TH-2026-003",
            hypothesis_rows.get("TH-2026-003"),
            hypothesis_header,
            "Boundary / Flow / Exposure IDs",
            {"TB-2026-002", "TB-2026-003"},
        ),
        (
            "TH-2026-006",
            hypothesis_rows.get("TH-2026-006"),
            hypothesis_header,
            "Boundary / Flow / Exposure IDs",
            {"TB-2026-002", "TB-2026-003", "TB-2026-007", "TB-2026-008"},
        ),
    )
    for identifier, row, header, field, expected_tb_ids in summary_boundary_bindings:
        if row is None:
            messages.append(f"{label}: missing summary-boundary consumer {identifier}")
            continue
        observed_tb_ids = set(re.findall(r"\bTB-2026-\d{3}\b", row[header.index(field)]))
        if observed_tb_ids != expected_tb_ids:
            messages.append(
                f"{label}: {identifier} {field} TB references {sorted(observed_tb_ids)!r} "
                f"!= {sorted(expected_tb_ids)!r}"
            )

    misuse_header = count_contracts[1][0]
    misuse_rows_by_id = {
        row[0].strip("`"): row
        for row in case_tables.get(misuse_header, [])
        if len(row) == len(misuse_header)
    }
    misuse001 = misuse_rows_by_id.get("MISUSE-2026-001")
    if misuse001 is None or misuse001[misuse_header.index("Boundary crossed")] != "`TB-2026-009`":
        messages.append(
            f"{label}: MISUSE-2026-001 must use fresh administrative boundary "
            "TB-2026-009 without redefining inherited TB-2026-001"
        )

    action_header = (
        "Action ID",
        "Related Gap / Control / Threat",
        "Action",
        "Owner",
        "Due date",
        "Success evidence",
        "Status",
    )
    action_rows, action_messages = table_by_header(text, action_header, label)
    messages.extend(action_messages)
    if len(action_rows) < 5:
        messages.append(f"{label}: Action ID table requires at least five rows")

    expected_action_relations = {
        "ACT-TM-2026-001": "`TH-2026-001`, `TH-2026-004`, `CTRL-2026-005`, `GAP-2026-002`",
        "ACT-TM-2026-002": "`TH-2026-002`, `CTRL-2026-007`, `GAP-2026-003`",
        "ACT-TM-2026-003": "`TH-2026-006`, `CTRL-2026-009`, `GAP-2026-001`",
        "ACT-TM-2026-004": "`TH-2026-001`, `TH-2026-004`, `CTRL-2026-005`, `CTRL-2026-006`, `GAP-2026-002`",
        "ACT-TM-2026-005": "`TH-2026-005`, `CTRL-2026-007`, `GAP-2026-003`",
        "ACT-TM-2026-006": (
            "`TH-2026-002`, `TH-2026-005`, `CTRL-2026-008`, `GAP-2026-004`"
        ),
    }
    action_relation_index = action_header.index("Related Gap / Control / Threat")
    observed_action_relations = {
        row[0].strip("`"): row[action_relation_index]
        for row in action_rows
        if len(row) == len(action_header)
    }
    if observed_action_relations != expected_action_relations:
        messages.append(
            f"{label}: Action source trace {observed_action_relations!r} "
            f"!= {expected_action_relations!r}"
        )

    allowed_action_source_ids = (
        EXPECTED_CASE_IDS["TH"] | EXPECTED_CASE_IDS["CTRL"] | EXPECTED_CASE_IDS["GAP"]
    )
    for action_id, relation in observed_action_relations.items():
        related_ids = set(re.findall(r"\b[A-Z][A-Z-]*-2026-\d{3}\b", relation))
        if not related_ids or not related_ids <= allowed_action_source_ids:
            messages.append(
                f"{label}: {action_id} Related Gap / Control / Threat must contain only "
                f"declared TH/CTRL/GAP IDs: {sorted(related_ids)!r}"
            )

    expected_gap_actions = {
        "GAP-2026-001": "`ACT-TM-2026-003`",
        "GAP-2026-002": "`ACT-TM-2026-001`, `ACT-TM-2026-004`",
        "GAP-2026-003": "`ACT-TM-2026-002`, `ACT-TM-2026-005`",
        "GAP-2026-004": "`ACT-TM-2026-006`",
    }
    gap_action_index = gap_header.index("Action ID")
    observed_gap_actions = {
        row[0].strip("`"): row[gap_action_index]
        for row in case_tables.get(gap_header, [])
        if len(row) == len(gap_header)
    }
    if observed_gap_actions != expected_gap_actions:
        messages.append(
            f"{label}: Gap-to-Action reverse trace {observed_gap_actions!r} "
            f"!= {expected_gap_actions!r}"
        )

    action_rows_by_id = {
        row[0].strip("`"): row for row in action_rows if len(row) == len(action_header)
    }
    action_text_index = action_header.index("Action")
    success_evidence_index = action_header.index("Success evidence")
    expected_action_semantics = {
        "ACT-TM-2026-001": {
            "action": (
                "2026-07-25 remediation後",
                "current scope Snapshot収集計画と要求",
                "必要最小scope案",
                "exportの取得",
                "実設定変更",
                "新Authorization Record / RoE承認後の別工程",
            ),
            "success": (
                "post-remediation App registration export収集要求ticket",
                "収集計画",
                "最小scope案",
                "新Authorization Record / RoE申請ticket",
                "export未収集",
                "実設定変更なし",
                "未収集Evidenceを収集済みと扱わない",
            ),
        },
        "ACT-TM-2026-002": {
            "action": (
                "Phase A",
                "Admin consent change Event",
                "合成Rule test計画",
                "新Authorization Record / RoE申請",
                "Phase B",
                "`ACT-TM-2026-006` Phase B-entry",
                "新Evidence ID付き署名済みpreflight report / default-deny結果の成功を開始条件",
                "no-outboundの合成Lab",
                "新Evidence IDを割り当て",
                "`REA-TM-2026-002`へ供給",
                "Phase CのCleanup verificationを完了するまで本Actionを完了扱いにしない",
                "entry gate失敗",
                "開始しない",
            ),
            "success": (
                "Phase A",
                "consent Rule test計画",
                "新Authorization Record / RoE申請ticket",
                "Phase B",
                "approval ticket",
                "Phase B-entryの新Evidence ID付き署名済みpreflight report / default-deny結果",
                "新Evidence ID付きAdmin consent Detection test結果",
                "query version",
                "Coverage",
                "Phase Cの新Evidence ID付きCleanup verification",
                "`REA-TM-2026-002`への供給",
                "Phase B / C未実施の間は結果未収集",
            ),
        },
        "ACT-TM-2026-003": {
            "action": (
                "Phase A",
                "resource / operation Field contract",
                "合成sample summary",
                "change proposal",
                "新Authorization Record / change approval申請",
                "Phase B",
                "対象・method・time window・実施Owner",
                "新Authorization Record / change approvalで承認した後に限り",
                "承認済み運用工程へhandoff",
                "第4章内ではProduction Pipelineを変更せず実Dataを収集しない",
                "post-change telemetry result",
                "新Evidence IDを割り当て",
                "query / version",
                "Coverage",
                "retention",
                "review sign-off",
                "`REA-TM-2026-002`へ供給",
                "未承認、過剰収集、scope外変更が必要な場合は停止する",
            ),
            "success": (
                "Phase A",
                "Field contract",
                "合成sample summary",
                "change proposal",
                "新Authorization Record / change approval申請ticket",
                "Production変更なし",
                "Phase B",
                "approval ticket",
                "承認済みの新Authorization Record / change approval",
                "実装記録",
                "新Evidence ID付きpost-change API telemetry result",
                "query / version",
                "resource / operation Coverage",
                "retention note",
                "review sign-off",
                "`REA-TM-2026-002`への供給",
                "Phase B未実施の間はpost-change result未収集",
            ),
        },
        "ACT-TM-2026-004": {
            "action": (
                "Phase A",
                "Boundary owner",
                "rotation手順Review field",
                "scope matrix",
                "収集計画",
                "新Authorization Record / RoE申請",
                "Phase B",
                "承認した後に限り",
                "合成Tenant",
                "read-only configuration export",
                "post-remediation App registration export",
                "Workload identity binding snapshot",
                "Tenant binding snapshot",
                "rotation手順Review記録",
                "rotation手順Review記録を収集し、新Evidence IDを割り当てて"
                "offline機械的突合",
                "新Evidence ID",
                "offline機械的突合",
                "source Evidence ID",
                "Workload-only binding check結果",
                "Rotation-management check結果",
                "Identity Assurance Reviewer",
                "resultとlimitation",
                "sign-off",
                "別々の新Evidence ID",
                "`REA-TM-2026-001`へ供給",
                "承認前",
                "live Tenant",
                "実Credential",
                "実Data",
                "停止する",
            ),
            "success": (
                "Phase A",
                "scope matrix",
                "収集計画",
                "新Authorization Record / RoE申請ticket",
                "Phase B",
                "approval ticket",
                "承認済みの新Authorization Record / RoE",
                "新Evidence ID付きpost-remediation App registration export",
                "Tenant binding差分",
                "Workload identity binding snapshot",
                "Tenant binding snapshot",
                "rotation手順Review記録",
                "offline機械的突合結果",
                "新Evidence ID付き・source Evidence IDを記録した"
                "Workload-only binding check結果",
                "新Evidence ID付き・source Evidence IDを記録した"
                "Rotation-management check結果",
                "新Evidence ID付きIdentity Assurance Reviewer sign-off",
                "`REA-TM-2026-001`への供給",
                "承認runbook",
                "Phase B未実施の間は未収集",
            ),
        },
        "ACT-TM-2026-005": {
            "action": (
                "Phase A",
                "query申請template",
                "App identity lifecycle Event",
                "decision summary Field",
                "90日retention証跡",
                "deny条件",
                "文書化",
                "合成Rule test計画",
                "新Authorization Record / RoE申請",
                "Phase B",
                "対象・method・time window",
                "`ACT-TM-2026-006` Phase B-entry",
                "新Evidence ID付き署名済みpreflight report / default-deny結果の成功を開始条件",
                "no-outboundの合成Lab",
                "no-outboundの合成LabでApp identity lifecycle Eventの合成Rule testを実行",
                "合成Rule testを実行",
                "Detection test結果を収集",
                "新Evidence IDを割り当て",
                "query version",
                "review sign-off",
                "query version、Coverage、90日retention証跡、review sign-offとともに"
                "`REA-TM-2026-002`へ供給する",
                "`REA-TM-2026-002`へ供給",
                "Admin consent change Event側は`ACT-TM-2026-002`が扱い",
                "App identity lifecycle Event側だけを扱う",
                "Phase CのCleanup verificationを完了するまで本Actionを完了扱いにしない",
                "entry gate失敗",
                "外向き通信",
                "実Target",
                "実Credential",
                "実Data",
                "Production変更",
                "開始または継続しない",
            ),
            "success": (
                "Phase A",
                "lifecycle Rule test計画",
                "新Authorization Record / RoE申請ticket",
                "Coverage表",
                "retention record",
                "deny例",
                "Phase B",
                "approval ticket",
                "承認済みの新Authorization Record / RoE",
                "Phase B-entryの新Evidence ID付き署名済みpreflight report / default-deny結果",
                "新Evidence ID付きApp identity lifecycle Event Detection test結果",
                "query version",
                "review sign-off",
                "Phase Cの新Evidence ID付きCleanup verification",
                "新Evidence ID付きApp identity lifecycle Event Detection test結果、query version、"
                "Coverage表、retention record、review sign-off、Phase Cの新Evidence ID付き"
                "Cleanup verification、`REA-TM-2026-002`への供給",
                "`REA-TM-2026-002`への供給",
                "Phase B / C未実施の間はApp identity lifecycle EventのDetection test結果とCleanup結果は未収集",
            ),
        },
        "ACT-TM-2026-006": {
            "action": (
                "Phase A",
                "preflight",
                "default-deny",
                "Cleanup実施計画",
                "新Authorization Record / RoE申請",
                "Phase B-entry",
                "対象・method・time windowを承認した後",
                "Rule test開始前",
                "新Evidence ID",
                "entry Evidence",
                "失敗時はRule testを開始しない",
                "Phase C",
                "Rule test終了または停止直後",
                "Cleanup verification",
                "`REA-TM-2026-004`へ供給",
                "開始または継続しない",
            ),
            "success": (
                "Phase A",
                "Lab実施計画",
                "新Authorization Record / RoE申請ticket",
                "Phase B-entry",
                "approval ticket",
                "承認済みの新Authorization Record / RoE",
                "新Evidence ID付き署名済みpreflight report / default-deny結果",
                "entry-gate sign-off",
                "Phase C",
                "新Evidence ID付きCleanup verification",
                "`REA-TM-2026-004`への供給",
                "各Phase未実施の間はpreflight / default-deny / Cleanup結果未収集",
            ),
        },
    }
    for action_id, requirements in expected_action_semantics.items():
        row = action_rows_by_id.get(action_id)
        if row is None:
            messages.append(f"{label}: missing semantic Action contract for {action_id}")
            continue
        for marker in requirements["action"]:
            if marker not in row[action_text_index]:
                messages.append(f"{label}: {action_id} Action missing Gap-remediation marker {marker!r}")
        for marker in requirements["success"]:
            if marker not in row[success_evidence_index]:
                messages.append(f"{label}: {action_id} Success evidence missing marker {marker!r}")

    lab_sequence_action_ids = (
        "ACT-TM-2026-002",
        "ACT-TM-2026-005",
        "ACT-TM-2026-006",
    )
    lab_sequence_action_due_dates: dict[str, str] = {}
    action_due_date_index = action_header.index("Due date")
    for action_id in lab_sequence_action_ids:
        row = action_rows_by_id.get(action_id)
        if row is None:
            continue
        due_date = row[action_due_date_index]
        lab_sequence_action_due_dates[action_id] = due_date
        if due_date != LAB_SEQUENCE_COMPLETION_DATE:
            messages.append(
                f"{label}: {action_id} Due date {due_date!r} != "
                f"coordinated completion {LAB_SEQUENCE_COMPLETION_DATE!r}"
            )

    lab_sequence_rows, lab_sequence_messages = table_by_header(
        text, LAB_SEQUENCE_HEADER, label
    )
    messages.extend(lab_sequence_messages)
    if tuple(tuple(row) for row in lab_sequence_rows) != EXPECTED_LAB_SEQUENCE_ROWS:
        messages.append(
            f"{label}: Lab Rule-test execution order {tuple(tuple(row) for row in lab_sequence_rows)!r} "
            f"!= {EXPECTED_LAB_SEQUENCE_ROWS!r}"
        )

    gap_rows_by_id = {
        row[0].strip("`"): row
        for row in case_tables.get(gap_header, [])
        if len(row) == len(gap_header)
    }
    scope_gap = gap_rows_by_id.get("GAP-2026-002")
    if scope_gap is None:
        messages.append(f"{label}: missing post-remediation scope Gap GAP-2026-002")
    else:
        scope_gap_markers = {
            "Missing information / control / telemetry": (
                "2026-07-25",
                "Passed",
                "current App registration export",
                "Workload identity binding snapshot",
                "Tenant binding差分",
                "rotation手順Review記録",
                "offline機械的突合結果",
                "未収集",
            ),
            "Decision affected": ("current scope", "Confirmed", "人手依存"),
        }
        for field, markers in scope_gap_markers.items():
            value = scope_gap[gap_header.index(field)]
            for marker in markers:
                if marker not in value:
                    messages.append(f"{label}: GAP-2026-002 {field} missing {marker!r}")
    lab_gap = gap_rows_by_id.get("GAP-2026-004")
    if lab_gap is None:
        messages.append(f"{label}: missing dedicated lab-safety Gap GAP-2026-004")
    else:
        expected_lab_gap_fields = {
            "Owner": "Lab Operator",
            "Due date": LAB_SEQUENCE_COMPLETION_DATE,
            "Evidence Requirement ID": "`EREQ-2026-004`",
            "Action ID": "`ACT-TM-2026-006`",
            "Reassessment ID": "`REA-TM-2026-004`",
        }
        for field, expected in expected_lab_gap_fields.items():
            actual = lab_gap[gap_header.index(field)]
            if actual != expected:
                messages.append(f"{label}: GAP-2026-004 {field} {actual!r} != {expected!r}")
        missing_information = lab_gap[gap_header.index("Missing information / control / telemetry")]
        for marker in ("CTRL-2026-008", "preflight", "default-deny", "Cleanup", "未収集"):
            if marker not in missing_information:
                messages.append(f"{label}: GAP-2026-004 missing lab-safety marker {marker!r}")

    evidence_rows_by_id = {
        row[0].strip("`"): row
        for row in case_tables.get(evidence_requirement_header, [])
        if len(row) == len(evidence_requirement_header)
    }
    scope_requirement = evidence_rows_by_id.get("EREQ-2026-001")
    if scope_requirement is None:
        messages.append(f"{label}: missing post-remediation scope requirement EREQ-2026-001")
    else:
        expected_scope_requirement_markers = {
            "Question": (
                "2026-07-25 remediation後",
                "current scope",
                "Workload identity binding",
                "Tenant binding",
                "rotation手順",
            ),
            "Minimum sufficient evidence": (
                "post-remediation App registration export",
                "scope差分表",
                "Workload identity binding snapshot",
                "Tenant binding差分",
                "rotation手順Review記録",
                "source Evidence IDを記録したWorkload-only binding check結果",
                "source Evidence IDを記録したRotation-management check結果",
                "Reviewer sign-off",
            ),
            "Resulting Evidence IDs": (
                "EVD-2026-001",
                "EVD-2026-002",
                "Historical inputs only",
                "current resultではない",
                "いずれも2026-07-20",
                "New post-remediation result",
                "current-scope snapshot",
                "Workload identity binding snapshot",
                "Tenant binding差分",
                "rotation手順Review記録",
                "offline機械的突合結果",
                "新Evidence ID付き・source Evidence IDを記録した"
                "Workload-only binding check結果",
                "新Evidence ID付き・source Evidence IDを記録した"
                "Rotation-management check結果",
                "新Evidence ID付きReviewer sign-off",
                "未収集",
                "承認後にそれぞれ新Evidence IDを割り当てる",
            ),
        }
        for field, markers in expected_scope_requirement_markers.items():
            value = scope_requirement[evidence_requirement_header.index(field)]
            for marker in markers:
                if marker not in value:
                    messages.append(f"{label}: EREQ-2026-001 {field} missing {marker!r}")
    rule_test_requirement = evidence_rows_by_id.get("EREQ-2026-002")
    if rule_test_requirement is None:
        messages.append(f"{label}: missing Rule-test Evidence Requirement EREQ-2026-002")
    else:
        rule_test_forbidden = rule_test_requirement[
            evidence_requirement_header.index("Forbidden / over-collection boundary")
        ]
        for marker in (
            "無害化summaryを超える追加Data exportを要求しない",
            "新Authorization Record / RoE承認前にRule testを再実施しない",
        ):
            if marker not in rule_test_forbidden:
                messages.append(f"{label}: EREQ-2026-002 safety boundary missing {marker!r}")
        rule_test_resulting = rule_test_requirement[
            evidence_requirement_header.index("Resulting Evidence IDs")
        ]
        for marker in (
            "Coverage result",
            "EVD-2026-003",
            "Admin consent Eventのみ",
            "App identity lifecycle EventのCoverage",
            "両Event classのRule test結果は未収集",
            "承認後に新Evidence IDを割り当てる",
        ):
            if marker not in rule_test_resulting:
                messages.append(f"{label}: EREQ-2026-002 Resulting Evidence IDs missing {marker!r}")
        if "EVD-AUTH-2026-001" in rule_test_resulting:
            messages.append(
                f"{label}: EREQ-2026-002 must not count Authorization provenance as Resulting Evidence"
            )
        if text.count(RULE_TEST_AUTHORIZATION_PROVENANCE_BOUNDARY) != 1:
            messages.append(
                f"{label}: Rule-test Authorization provenance boundary must occur exactly once"
            )
        rule_test_minimum = rule_test_requirement[
            evidence_requirement_header.index("Minimum sufficient evidence")
        ]
        for marker in (
            "合成同意Event",
            "合成App identity lifecycle Event",
            "両Event classのRule test結果",
        ):
            if marker not in rule_test_minimum:
                messages.append(f"{label}: EREQ-2026-002 minimum evidence missing {marker!r}")

    telemetry_requirement = evidence_rows_by_id.get("EREQ-2026-003")
    if telemetry_requirement is None:
        messages.append(f"{label}: missing API telemetry Evidence Requirement EREQ-2026-003")
    else:
        telemetry_minimum = telemetry_requirement[
            evidence_requirement_header.index("Minimum sufficient evidence")
        ]
        telemetry_forbidden = telemetry_requirement[
            evidence_requirement_header.index("Forbidden / over-collection boundary")
        ]
        telemetry_resulting = telemetry_requirement[
            evidence_requirement_header.index("Resulting Evidence IDs")
        ]
        for marker in (
            "resource / operation Field contract",
            "承認後のpost-change telemetry result",
        ):
            if marker not in telemetry_minimum:
                messages.append(f"{label}: EREQ-2026-003 minimum evidence missing {marker!r}")
        for marker in (
            "Production変更や実Dataが必要な工程を第4章内で実行しない",
            "PIIを収集しない",
            "実Tenantへ接続しない",
        ):
            if marker not in telemetry_forbidden:
                messages.append(f"{label}: EREQ-2026-003 safety boundary missing {marker!r}")
        for marker in (
            "Historical inputs only",
            "EVD-2026-004",
            "NEG-2026-001",
            "resource / operation Fieldの実装記録とpost-change telemetry resultは未収集",
            "承認済み運用工程後に新Evidence IDを割り当てる",
        ):
            if marker not in telemetry_resulting:
                messages.append(
                    f"{label}: EREQ-2026-003 Resulting Evidence IDs missing {marker!r}"
                )

    lab_requirement = evidence_rows_by_id.get("EREQ-2026-004")
    if lab_requirement is None:
        messages.append(f"{label}: missing lab-safety Evidence Requirement EREQ-2026-004")
    else:
        relation = lab_requirement[evidence_requirement_header.index("Related Threat / Control / Gap")]
        if relation != (
            "`TH-2026-002`, `TH-2026-005`, `CTRL-2026-008`, `GAP-2026-004`"
        ):
            messages.append(f"{label}: EREQ-2026-004 source trace drift: {relation!r}")
        minimum = lab_requirement[evidence_requirement_header.index("Minimum sufficient evidence")]
        forbidden = lab_requirement[evidence_requirement_header.index("Forbidden / over-collection boundary")]
        resulting = lab_requirement[evidence_requirement_header.index("Resulting Evidence IDs")]
        due_date = lab_requirement[evidence_requirement_header.index("Due date")]
        if due_date != LAB_SEQUENCE_COMPLETION_DATE:
            messages.append(
                f"{label}: EREQ-2026-004 Due date {due_date!r} != "
                f"coordinated completion {LAB_SEQUENCE_COMPLETION_DATE!r}"
            )
        for marker in ("preflight report", "default-deny", "Cleanup verification"):
            if marker not in minimum:
                messages.append(f"{label}: EREQ-2026-004 minimum evidence missing {marker!r}")
        for marker in ("新Authorization Record / RoE承認前に実行しない", "実Target", "実Credential", "外向き通信"):
            if marker not in forbidden:
                messages.append(f"{label}: EREQ-2026-004 safety boundary missing {marker!r}")
        if resulting != "未収集（承認後に新Evidence IDを割り当てる）":
            messages.append(f"{label}: EREQ-2026-004 must not invent collected Evidence: {resulting!r}")

    threshold_occurrences = text.count(IDENTITY_ASSURANCE_THRESHOLD_SECTION)
    if threshold_occurrences != 1:
        messages.append(
            f"{label}: REA-TM-2026-001 identity closure threshold section "
            f"count {threshold_occurrences} != 1"
        )

    reassessment_header = count_contracts[6][0]
    reassessment_rows_by_id = {
        row[0].strip("`"): row
        for row in case_tables.get(reassessment_header, [])
        if len(row) == len(reassessment_header)
    }

    supplier_schedule_rows, supplier_schedule_messages = table_by_header(
        text, EVIDENCE_SUPPLIER_SCHEDULE_HEADER, label
    )
    messages.extend(supplier_schedule_messages)
    observed_supplier_schedule_rows = tuple(
        tuple(row) for row in supplier_schedule_rows
    )
    if observed_supplier_schedule_rows != EXPECTED_EVIDENCE_SUPPLIER_SCHEDULE_ROWS:
        messages.append(
            f"{label}: Evidence Requirement supplier schedule "
            f"{observed_supplier_schedule_rows!r} != "
            f"{EXPECTED_EVIDENCE_SUPPLIER_SCHEDULE_ROWS!r}"
        )

    action_due_date_index = action_header.index("Due date")
    evidence_due_date_index = evidence_requirement_header.index("Due date")
    gap_due_date_index = gap_header.index("Due date")
    reassessment_date_index = reassessment_header.index("Scheduled date")
    observed_action_due_dates = {
        action_id: row[action_due_date_index]
        for action_id, row in action_rows_by_id.items()
    }
    observed_evidence_due_dates = {
        requirement_id: row[evidence_due_date_index]
        for requirement_id, row in evidence_rows_by_id.items()
    }
    observed_gap_due_dates = {
        gap_id: row[gap_due_date_index] for gap_id, row in gap_rows_by_id.items()
    }
    observed_reassessment_dates = {
        reassessment_id: reassessment_rows_by_id[reassessment_id][
            reassessment_date_index
        ]
        for reassessment_id in EXPECTED_POST_COLLECTION_REASSESSMENT_DATES
        if reassessment_id in reassessment_rows_by_id
    }
    for family, observed, expected in (
        ("Action", observed_action_due_dates, EXPECTED_ACTION_DUE_DATES),
        (
            "Evidence Requirement",
            observed_evidence_due_dates,
            EXPECTED_EVIDENCE_REQUIREMENT_DUE_DATES,
        ),
        ("Gap", observed_gap_due_dates, EXPECTED_GAP_DUE_DATES),
        (
            "post-collection Reassessment",
            observed_reassessment_dates,
            EXPECTED_POST_COLLECTION_REASSESSMENT_DATES,
        ),
    ):
        if observed != expected:
            messages.append(
                f"{label}: exact {family} schedule {observed!r} != {expected!r}"
            )

    parsed_schedule_dates: dict[tuple[str, str], date] = {}
    for family, schedule in (
        ("Action", observed_action_due_dates),
        ("Evidence Requirement", observed_evidence_due_dates),
        ("Gap", observed_gap_due_dates),
        ("Reassessment", observed_reassessment_dates),
    ):
        for identifier, raw_date in schedule.items():
            try:
                parsed_date = date.fromisoformat(raw_date)
            except ValueError as exc:
                messages.append(
                    f"{label}: {family} {identifier} date {raw_date!r} "
                    f"is not ISO-8601: {exc}"
                )
                continue
            if parsed_date.isoformat() != raw_date:
                messages.append(
                    f"{label}: {family} {identifier} date {raw_date!r} is not "
                    "canonical YYYY-MM-DD"
                )
                continue
            parsed_schedule_dates[(family, identifier)] = parsed_date

    supplier_schedule_by_id = {
        row[0].strip("`"): row
        for row in supplier_schedule_rows
        if len(row) == len(EVIDENCE_SUPPLIER_SCHEDULE_HEADER)
    }
    supplier_union: set[str] = set()
    for requirement_id in EXPECTED_EVIDENCE_REQUIREMENT_DUE_DATES:
        row = supplier_schedule_by_id.get(requirement_id)
        if row is None:
            messages.append(
                f"{label}: supplier schedule missing {requirement_id}"
            )
            continue
        supplier_ids = set(
            re.findall(
                r"\bACT-TM-2026-\d{3}\b",
                row[EVIDENCE_SUPPLIER_SCHEDULE_HEADER.index("Supplier Action IDs")],
            )
        )
        gap_ids = set(
            re.findall(
                r"\bGAP-2026-\d{3}\b",
                row[EVIDENCE_SUPPLIER_SCHEDULE_HEADER.index("Gap IDs")],
            )
        )
        reassessment_ids = set(
            re.findall(
                r"\bREA-TM-2026-\d{3}\b",
                row[
                    EVIDENCE_SUPPLIER_SCHEDULE_HEADER.index(
                        "Consuming Reassessment ID"
                    )
                ],
            )
        )
        supplier_union.update(supplier_ids)
        unknown_suppliers = supplier_ids - set(observed_action_due_dates)
        if unknown_suppliers:
            messages.append(
                f"{label}: {requirement_id} has unknown supplier Actions "
                f"{sorted(unknown_suppliers)!r}"
            )
        unknown_gaps = gap_ids - set(observed_gap_due_dates)
        if unknown_gaps:
            messages.append(
                f"{label}: {requirement_id} has unknown Gaps "
                f"{sorted(unknown_gaps)!r}"
            )
        if len(reassessment_ids) != 1:
            messages.append(
                f"{label}: {requirement_id} must have exactly one consuming "
                f"Reassessment, found {sorted(reassessment_ids)!r}"
            )

        supplier_days = {
            supplier_id: parsed_schedule_dates.get(("Action", supplier_id))
            for supplier_id in supplier_ids
        }
        supplier_days = {
            supplier_id: supplier_day
            for supplier_id, supplier_day in supplier_days.items()
            if supplier_day is not None
        }
        if supplier_ids and len(supplier_days) == len(supplier_ids):
            latest_supplier_day = max(supplier_days.values())
            recorded_latest = row[
                EVIDENCE_SUPPLIER_SCHEDULE_HEADER.index(
                    "Latest supplier completion"
                )
            ]
            try:
                recorded_latest_day = date.fromisoformat(recorded_latest)
            except ValueError as exc:
                messages.append(
                    f"{label}: {requirement_id} latest supplier completion "
                    f"{recorded_latest!r} is not ISO-8601: {exc}"
                )
            else:
                if recorded_latest_day != latest_supplier_day:
                    messages.append(
                        f"{label}: {requirement_id} latest supplier completion "
                        f"{recorded_latest!r} != computed "
                        f"{latest_supplier_day.isoformat()!r}"
                    )

            requirement_day = parsed_schedule_dates.get(
                ("Evidence Requirement", requirement_id)
            )
            recorded_requirement_due = row[
                EVIDENCE_SUPPLIER_SCHEDULE_HEADER.index("Requirement due")
            ]
            if (
                requirement_day is not None
                and recorded_requirement_due != requirement_day.isoformat()
            ):
                messages.append(
                    f"{label}: {requirement_id} supplier schedule due "
                    f"{recorded_requirement_due!r} != register due "
                    f"{requirement_day.isoformat()!r}"
                )
            if requirement_day is not None and requirement_day < latest_supplier_day:
                messages.append(
                    f"{label}: {requirement_id} due "
                    f"{requirement_day.isoformat()!r} precedes suppliers "
                    f"{ {key: supplier_days[key].isoformat() for key in sorted(supplier_days)}!r}"
                )

            for gap_id in sorted(gap_ids):
                gap_day = parsed_schedule_dates.get(("Gap", gap_id))
                if gap_day is not None and gap_day < latest_supplier_day:
                    messages.append(
                        f"{label}: {gap_id} due {gap_day.isoformat()!r} precedes "
                        f"{requirement_id} supplier completion "
                        f"{latest_supplier_day.isoformat()!r}"
                    )

            for reassessment_id in sorted(reassessment_ids):
                reassessment_day = parsed_schedule_dates.get(
                    ("Reassessment", reassessment_id)
                )
                if reassessment_day is None or requirement_day is None:
                    continue
                prerequisite_day = max(requirement_day, latest_supplier_day)
                if reassessment_day <= prerequisite_day:
                    messages.append(
                        f"{label}: {reassessment_id} must run after "
                        f"{requirement_id} and all supplier Actions: "
                        f"{reassessment_day.isoformat()!r} <= "
                        f"{prerequisite_day.isoformat()!r}"
                    )

        reverse_gap_ids = {
            gap_id
            for gap_id, gap_row in gap_rows_by_id.items()
            if requirement_id
            in set(
                re.findall(
                    r"\bEREQ-2026-\d{3}\b",
                    gap_row[gap_header.index("Evidence Requirement ID")],
                )
            )
        }
        if reverse_gap_ids != gap_ids:
            messages.append(
                f"{label}: {requirement_id} Gap set {sorted(gap_ids)!r} != "
                f"reverse trace {sorted(reverse_gap_ids)!r}"
            )

        gap_action_union: set[str] = set()
        gap_reassessment_union: set[str] = set()
        for gap_id in sorted(gap_ids):
            gap_row = gap_rows_by_id.get(gap_id)
            if gap_row is None:
                continue
            gap_requirement_ids = set(
                re.findall(
                    r"\bEREQ-2026-\d{3}\b",
                    gap_row[gap_header.index("Evidence Requirement ID")],
                )
            )
            if requirement_id not in gap_requirement_ids:
                messages.append(
                    f"{label}: {gap_id} does not reference {requirement_id}"
                )
            gap_action_union.update(
                re.findall(
                    r"\bACT-TM-2026-\d{3}\b",
                    gap_row[gap_header.index("Action ID")],
                )
            )
            gap_reassessment_union.update(
                re.findall(
                    r"\bREA-TM-2026-\d{3}\b",
                    gap_row[gap_header.index("Reassessment ID")],
                )
            )
        if gap_action_union != supplier_ids:
            messages.append(
                f"{label}: {requirement_id} supplier Actions "
                f"{sorted(supplier_ids)!r} != Action union from Gaps "
                f"{sorted(gap_action_union)!r}"
            )
        if gap_reassessment_union != reassessment_ids:
            messages.append(
                f"{label}: {requirement_id} consuming Reassessments "
                f"{sorted(reassessment_ids)!r} != Gap reverse trace "
                f"{sorted(gap_reassessment_union)!r}"
            )

    if supplier_union != set(EXPECTED_ACTION_DUE_DATES):
        messages.append(
            f"{label}: supplier schedule Action coverage "
            f"{sorted(supplier_union)!r} != "
            f"{sorted(EXPECTED_ACTION_DUE_DATES)!r}"
        )

    identity_reassessment = reassessment_rows_by_id.get("REA-TM-2026-001")
    if identity_reassessment is None:
        messages.append(f"{label}: missing REA-TM-2026-001 exact identity contract")
    else:
        for field, expected in (
            ("Inputs required", REA_TM_001_INPUTS_REQUIRED),
            ("Closure criteria", REA_TM_001_CLOSURE_CRITERIA),
        ):
            actual = identity_reassessment[reassessment_header.index(field)]
            if actual != expected:
                messages.append(
                    f"{label}: REA-TM-2026-001 {field} {actual!r} != "
                    f"exact identity contract {expected!r}"
                )
    expected_reassessment_markers = {
        "REA-TM-2026-001": {
            "Inputs required": (
                "2026-07-25 remediation後のApp registration export",
                "Tenant binding差分",
                "Workload identity binding snapshot",
                "rotation手順Review記録",
                "Workload-only binding check結果",
                "Rotation-management check結果",
                "Reviewer sign-off",
                "新Authorization Record / RoE",
            ),
            "Closure criteria": (
                "post-remediation current scopeがEvidenceで`Confirmed`",
                "新Authorization Record / RoE承認後にのみ変更",
                "CTRL-2026-005",
                "Implemented",
                "Workload-only binding check",
                "Rotation-management check",
                "両方が`Passed`",
                "新Evidence ID付き・source Evidence IDを記録した各check結果",
                "新Evidence ID付きReviewer sign-off",
                "そろう場合だけ",
                "CTRL-2026-006",
                "Observed",
                "Failed / Inconclusive / Not collected",
                "`Documented`に維持",
                "`GAP-2026-002`を閉じない",
            ),
        },
        "REA-TM-2026-002": {
            "Inputs required": (
                "Admin consent Event",
                "App identity lifecycle Event",
                "Rule test計画",
                "新Authorization Record / RoE",
                "両Event classのDetection test結果",
                "query version",
                "Field contract",
                "合成sample summary",
                "change proposal",
                "Telemetry Field change approval",
                "Field実装記録",
                "新Evidence ID付きpost-change API telemetry result",
                "resource / operation Coverage",
                "review sign-off",
            ),
            "Closure criteria": (
                "新Authorization Record / RoE承認後にのみ両Event classの合成Rule testを再実施",
                "Detection test結果に新Evidence IDを割り当てる",
                "両Event classのEvidence",
                "CTRL-2026-007",
                "Validated",
                "新Authorization Record / change approval後の承認済み運用工程",
                "post-change Evidence",
                "required API Eventのresource / operation Field",
                "Coverage",
                "retention",
                "過剰収集なし",
                "CTRL-2026-009",
                "GAP-2026-001",
                "CTRL-2026-007`のEvidenceを`CTRL-2026-009`へ流用しない",
            ),
        },
        "REA-TM-2026-004": {
            "Scope": ("CTRL-2026-008", "GAP-2026-004", "EREQ-2026-004"),
            "Inputs required": (
                "新Authorization Record",
                "RoE",
                "Rule test開始前",
                "新Evidence ID付き署名済みpreflight report / default-deny結果",
                "Rule test終了または停止後",
                "新Evidence ID付きCleanup verification",
            ),
            "Closure criteria": (
                "preflight / default-denyがRule test開始前に成功",
                "終了または停止直後のCleanup verification",
                "CTRL-2026-008",
                "Observed",
                "開始または継続せず",
                "完了扱いにしない",
            ),
        },
    }
    for reassessment_id, fields in expected_reassessment_markers.items():
        row = reassessment_rows_by_id.get(reassessment_id)
        if row is None:
            messages.append(f"{label}: missing Reassessment contract {reassessment_id}")
            continue
        for field, markers in fields.items():
            value = row[reassessment_header.index(field)]
            for marker in markers:
                if marker not in value:
                    messages.append(f"{label}: {reassessment_id} {field} missing {marker!r}")

    lab_reassessment = reassessment_rows_by_id.get("REA-TM-2026-004")
    if lab_reassessment is not None:
        scheduled_date = lab_reassessment[
            reassessment_header.index("Scheduled date")
        ]
        if scheduled_date != LAB_SEQUENCE_REASSESSMENT_DATE:
            messages.append(
                f"{label}: REA-TM-2026-004 Scheduled date "
                f"{scheduled_date!r} != post-cleanup reassessment "
                f"{LAB_SEQUENCE_REASSESSMENT_DATE!r}"
            )

        prerequisite_due_dates = dict(lab_sequence_action_due_dates)
        if lab_gap is not None:
            prerequisite_due_dates["GAP-2026-004"] = lab_gap[
                gap_header.index("Due date")
            ]
        if lab_requirement is not None:
            prerequisite_due_dates["EREQ-2026-004"] = lab_requirement[
                evidence_requirement_header.index("Due date")
            ]
        try:
            reassessment_day = date.fromisoformat(scheduled_date)
            completion_days = {
                identifier: date.fromisoformat(due_date)
                for identifier, due_date in prerequisite_due_dates.items()
            }
        except ValueError as exc:
            messages.append(f"{label}: Lab sequence date is not ISO-8601: {exc}")
        else:
            late_or_equal = {
                identifier: due_day.isoformat()
                for identifier, due_day in completion_days.items()
                if due_day >= reassessment_day
            }
            if late_or_equal:
                messages.append(
                    f"{label}: Lab prerequisites must complete before "
                    f"REA-TM-2026-004: {late_or_equal!r} >= "
                    f"{scheduled_date!r}"
                )

    path_summary_rows, path_summary_messages = table_by_header(
        text, PATH_SUMMARY_HEADER, label
    )
    messages.extend(path_summary_messages)
    path_summaries_by_id = {
        row[0].strip("`"): row
        for row in path_summary_rows
        if len(row) == len(PATH_SUMMARY_HEADER)
    }
    path001_summary = path_summaries_by_id.get("PATH-2026-001")
    if path001_summary is None:
        messages.append(f"{label}: missing PATH-2026-001 temporal summary")
    else:
        temporal_summary_markers = {
            "Entry condition": (
                "2026-07-20",
                "historical Snapshot",
                "2026-07-25",
                "Passed",
                "post-remediation Snapshot未収集",
                "`Unknown`",
            ),
            "Intermediate condition": ("current", "未確認"),
            "Undesired end state": ("current状態として確定できない",),
        }
        for field, markers in temporal_summary_markers.items():
            value = path001_summary[PATH_SUMMARY_HEADER.index(field)]
            for marker in markers:
                if marker not in value:
                    messages.append(f"{label}: PATH-2026-001 {field} missing {marker!r}")
    assumption_header = count_contracts[3][0]
    assumptions_by_id = {
        row[0].strip("`"): row
        for row in case_tables.get(assumption_header, [])
        if len(row) == len(assumption_header)
    }
    refinement_consumer_contracts = (
        (
            "PATH-2026-001",
            path_summaries_by_id.get("PATH-2026-001"),
            PATH_SUMMARY_HEADER,
            "Related Threat IDs",
            {"TH-2026-001", "TH-2026-004"},
        ),
        (
            "CTRL-2026-005",
            controls_by_id.get("CTRL-2026-005"),
            control_header,
            "Related Asset / Boundary / Threat / Path IDs",
            {"TH-2026-001", "TH-2026-004"},
        ),
        (
            "CTRL-2026-006",
            controls_by_id.get("CTRL-2026-006"),
            control_header,
            "Related Asset / Boundary / Threat / Path IDs",
            {"TH-2026-001", "TH-2026-004"},
        ),
        (
            "ASM-2026-001",
            assumptions_by_id.get("ASM-2026-001"),
            assumption_header,
            "Related IDs",
            {"TH-2026-001", "TH-2026-004"},
        ),
        (
            "ASM-2026-002",
            assumptions_by_id.get("ASM-2026-002"),
            assumption_header,
            "Related IDs",
            {"TH-2026-004", "TH-2026-006"},
        ),
        (
            "GAP-2026-002",
            gap_rows_by_id.get("GAP-2026-002"),
            gap_header,
            "Missing information / control / telemetry",
            {"TH-2026-001", "TH-2026-004"},
        ),
        (
            "EREQ-2026-001",
            evidence_rows_by_id.get("EREQ-2026-001"),
            evidence_requirement_header,
            "Related Threat / Control / Gap",
            {"TH-2026-001", "TH-2026-004"},
        ),
        (
            "EREQ-2026-003",
            evidence_rows_by_id.get("EREQ-2026-003"),
            evidence_requirement_header,
            "Related Threat / Control / Gap",
            {"TH-2026-001", "TH-2026-003", "TH-2026-004", "TH-2026-006"},
        ),
        (
            "REA-TM-2026-001",
            reassessment_rows_by_id.get("REA-TM-2026-001"),
            reassessment_header,
            "Scope",
            {"TH-2026-001", "TH-2026-004"},
        ),
    )
    for identifier, row, header, field, expected_th_ids in refinement_consumer_contracts:
        if row is None:
            messages.append(f"{label}: missing TH-2026-004 refinement consumer {identifier}")
            continue
        observed_th_ids = set(
            re.findall(r"\bTH-2026-\d{3}\b", row[header.index(field)])
        )
        if observed_th_ids != expected_th_ids:
            messages.append(
                f"{label}: {identifier} {field} Threat references "
                f"{sorted(observed_th_ids)!r} != {sorted(expected_th_ids)!r}"
            )

    # Freeze every structured consumer of the inherited consent/Rule
    # proposition (TH-2026-002) and the Chapter 4 lifecycle/summary-field
    # refinement (TH-2026-005).  The finite map makes inherited-only,
    # refinement-only, both, and neither explicit; a consumer cannot silently
    # fall back to the inherited ID after the two propositions are separated.
    th_002_005 = {"TH-2026-002", "TH-2026-005"}
    th_002_005_consumer_maps = (
        (
            "Path summary",
            path_summaries_by_id,
            PATH_SUMMARY_HEADER,
            "Related Threat IDs",
            {
                "PATH-2026-001": set(),
                "PATH-2026-002": {"TH-2026-002", "TH-2026-005"},
            },
        ),
        (
            "Control",
            controls_by_id,
            control_header,
            "Related Asset / Boundary / Threat / Path IDs",
            {
                "CTRL-2026-005": set(),
                "CTRL-2026-006": set(),
                "CTRL-2026-007": {"TH-2026-002", "TH-2026-005"},
                "CTRL-2026-008": {"TH-2026-002", "TH-2026-005"},
                "CTRL-2026-009": set(),
            },
        ),
        (
            "Assumption",
            assumptions_by_id,
            assumption_header,
            "Related IDs",
            {
                "ASM-2026-001": set(),
                "ASM-2026-002": set(),
                "ASM-2026-003": set(),
            },
        ),
        (
            "Gap",
            gap_rows_by_id,
            gap_header,
            "Missing information / control / telemetry",
            {
                "GAP-2026-001": set(),
                "GAP-2026-002": set(),
                "GAP-2026-003": {"TH-2026-002", "TH-2026-005"},
                "GAP-2026-004": set(),
            },
        ),
        (
            "Evidence Requirement",
            evidence_rows_by_id,
            evidence_requirement_header,
            "Related Threat / Control / Gap",
            {
                "EREQ-2026-001": set(),
                "EREQ-2026-002": {"TH-2026-002", "TH-2026-005"},
                "EREQ-2026-003": set(),
                "EREQ-2026-004": {"TH-2026-002", "TH-2026-005"},
            },
        ),
        (
            "Action",
            action_rows_by_id,
            action_header,
            "Related Gap / Control / Threat",
            {
                "ACT-TM-2026-001": set(),
                "ACT-TM-2026-002": {"TH-2026-002"},
                "ACT-TM-2026-003": set(),
                "ACT-TM-2026-004": set(),
                "ACT-TM-2026-005": {"TH-2026-005"},
                "ACT-TM-2026-006": {"TH-2026-002", "TH-2026-005"},
            },
        ),
        (
            "Reassessment",
            reassessment_rows_by_id,
            reassessment_header,
            "Scope",
            {
                "REA-TM-2026-001": set(),
                "REA-TM-2026-002": {"TH-2026-002", "TH-2026-005"},
                "REA-TM-2026-003": set(),
                "REA-TM-2026-004": set(),
            },
        ),
    )
    for map_name, rows_by_id, header, field, expected_map in th_002_005_consumer_maps:
        if set(rows_by_id) != set(expected_map):
            messages.append(
                f"{label}: {map_name} TH-2026-002/005 consumer-map row coverage "
                f"{sorted(rows_by_id)!r} != {sorted(expected_map)!r}"
            )
        for identifier, expected_th_ids in expected_map.items():
            row = rows_by_id.get(identifier)
            if row is None:
                continue
            observed_th_ids = set(
                re.findall(r"\bTH-2026-\d{3}\b", row[header.index(field)])
            ) & th_002_005
            if observed_th_ids != expected_th_ids:
                messages.append(
                    f"{label}: {identifier} {field} inherited/refinement Threat map "
                    f"{sorted(observed_th_ids)!r} != {sorted(expected_th_ids)!r}"
                )

    # Freeze every structured consumer of the inherited occurrence
    # proposition (TH-2026-003) and the Chapter 4 opportunity/summary-only
    # refinement (TH-2026-006). A shared Telemetry source does not make these
    # the same proposition: each consumer must explicitly select one or both.
    th_003_006 = {"TH-2026-003", "TH-2026-006"}
    th_003_006_consumer_maps = (
        (
            "Path summary",
            path_summaries_by_id,
            PATH_SUMMARY_HEADER,
            "Related Threat IDs",
            {
                "PATH-2026-001": set(),
                "PATH-2026-002": {"TH-2026-003", "TH-2026-006"},
            },
        ),
        (
            "Control",
            controls_by_id,
            control_header,
            "Related Asset / Boundary / Threat / Path IDs",
            {
                "CTRL-2026-005": set(),
                "CTRL-2026-006": set(),
                "CTRL-2026-007": set(),
                "CTRL-2026-008": set(),
                "CTRL-2026-009": {"TH-2026-006"},
            },
        ),
        (
            "Assumption",
            assumptions_by_id,
            assumption_header,
            "Related IDs",
            {
                "ASM-2026-001": set(),
                "ASM-2026-002": {"TH-2026-006"},
                "ASM-2026-003": {"TH-2026-003", "TH-2026-006"},
            },
        ),
        (
            "Gap",
            gap_rows_by_id,
            gap_header,
            "Missing information / control / telemetry",
            {
                "GAP-2026-001": {"TH-2026-006"},
                "GAP-2026-002": set(),
                "GAP-2026-003": {"TH-2026-003", "TH-2026-006"},
                "GAP-2026-004": set(),
            },
        ),
        (
            "Evidence Requirement",
            evidence_rows_by_id,
            evidence_requirement_header,
            "Related Threat / Control / Gap",
            {
                "EREQ-2026-001": set(),
                "EREQ-2026-002": set(),
                "EREQ-2026-003": {"TH-2026-003", "TH-2026-006"},
                "EREQ-2026-004": set(),
            },
        ),
        (
            "Action",
            action_rows_by_id,
            action_header,
            "Related Gap / Control / Threat",
            {
                "ACT-TM-2026-001": set(),
                "ACT-TM-2026-002": set(),
                "ACT-TM-2026-003": {"TH-2026-006"},
                "ACT-TM-2026-004": set(),
                "ACT-TM-2026-005": set(),
                "ACT-TM-2026-006": set(),
            },
        ),
        (
            "Reassessment",
            reassessment_rows_by_id,
            reassessment_header,
            "Scope",
            {
                "REA-TM-2026-001": set(),
                "REA-TM-2026-002": {"TH-2026-003", "TH-2026-006"},
                "REA-TM-2026-003": set(),
                "REA-TM-2026-004": set(),
            },
        ),
    )
    for map_name, rows_by_id, header, field, expected_map in th_003_006_consumer_maps:
        if set(rows_by_id) != set(expected_map):
            messages.append(
                f"{label}: {map_name} TH-2026-003/006 consumer-map row coverage "
                f"{sorted(rows_by_id)!r} != {sorted(expected_map)!r}"
            )
        for identifier, expected_th_ids in expected_map.items():
            row = rows_by_id.get(identifier)
            if row is None:
                continue
            observed_th_ids = set(
                re.findall(r"\bTH-2026-\d{3}\b", row[header.index(field)])
            ) & th_003_006
            if observed_th_ids != expected_th_ids:
                messages.append(
                    f"{label}: {identifier} {field} occurrence/refinement Threat map "
                    f"{sorted(observed_th_ids)!r} != {sorted(expected_th_ids)!r}"
                )

    allocation_rows, allocation_messages = table_by_header(
        text, TH_002_005_ALLOCATION_HEADER, label
    )
    messages.extend(allocation_messages)
    observed_allocation_rows = tuple(
        tuple(row)
        for row in allocation_rows
        if len(row) == len(TH_002_005_ALLOCATION_HEADER)
    )
    if observed_allocation_rows != EXPECTED_TH_002_005_ALLOCATION_ROWS:
        messages.append(
            f"{label}: TH-2026-002/005 reader-visible consumer allocation "
            f"{observed_allocation_rows!r} != {EXPECTED_TH_002_005_ALLOCATION_ROWS!r}"
        )
    allocation_boundary = (
        "表外のstructured consumerがいずれかのIDへ暗黙にfallbackすることを認めない"
    )
    if text.count(allocation_boundary) != 1:
        messages.append(
            f"{label}: TH-2026-002/005 allocation boundary must occur exactly once"
        )

    occurrence_allocation_rows, occurrence_allocation_messages = table_by_header(
        text, TH_003_006_ALLOCATION_HEADER, label
    )
    messages.extend(occurrence_allocation_messages)
    observed_occurrence_allocation_rows = tuple(
        tuple(row)
        for row in occurrence_allocation_rows
        if len(row) == len(TH_003_006_ALLOCATION_HEADER)
    )
    if observed_occurrence_allocation_rows != EXPECTED_TH_003_006_ALLOCATION_ROWS:
        messages.append(
            f"{label}: TH-2026-003/006 reader-visible consumer allocation "
            f"{observed_occurrence_allocation_rows!r} != "
            f"{EXPECTED_TH_003_006_ALLOCATION_ROWS!r}"
        )
    occurrence_allocation_boundary = (
        "発生命題と機会条件・影響範囲命題を別々に評価する"
    )
    if text.count(occurrence_allocation_boundary) != 1:
        messages.append(
            f"{label}: TH-2026-003/006 allocation boundary must occur exactly once"
        )

    decision_summary = section(text, "### Decision handoff summary for `DR-2026-001`")
    for marker in (
        "継承命題`TH-2026-002`",
        "lifecycle / summary Field refinementの`TH-2026-005`",
        "発生有無を問う`TH-2026-003`",
        "機会条件およびsummary-only境界までの影響範囲を問う`TH-2026-006`",
        "2026-07-20のhistorical Snapshot",
        "2026-07-25にscope縮小`Passed`",
        "post-remediation current scope Snapshotが未収集",
    ):
        if marker not in decision_summary:
            messages.append(
                f"{label}: Decision handoff summary does not distinguish {marker!r}"
            )
    decision_rows, decision_messages = table_by_header(
        decision_summary, FIELD_VALUE_HEADER, label
    )
    messages.extend(decision_messages)
    expected_decision_fields = (
        "Supported option",
        "Confidence",
        "Why not immediate unrestricted continuation",
        "Why not direct production validation here",
        "Strongest confirmed point",
        "Strongest uncertainty",
        "Permitted conclusion",
        "Prohibited conclusion",
    )
    observed_decision_fields = tuple(
        row[0] for row in decision_rows if len(row) == len(FIELD_VALUE_HEADER)
    )
    if observed_decision_fields != expected_decision_fields:
        messages.append(
            f"{label}: Decision handoff fields/order {observed_decision_fields!r} "
            f"!= {expected_decision_fields!r}"
        )
    decision_values = {
        row[0]: row[1]
        for row in decision_rows
        if len(row) == len(FIELD_VALUE_HEADER)
    }
    confidence = decision_values.get("Confidence", "")
    for marker in (
        "低。",
        "推奨の確からしさ",
        "severityではない",
        "2026-07-25",
        "post-remediation current scope Snapshotが未収集",
        "GAP-2026-001",
        "GAP-2026-003",
        "Open / Escalated",
        "再評価前",
    ):
        if marker not in confidence:
            messages.append(
                f"{label}: Decision handoff Confidence missing bounded marker {marker!r}"
            )
    if confidence.startswith("高") or "不確実性はない" in confidence:
        messages.append(
            f"{label}: Decision handoff Confidence overclaims uncollected current Evidence"
        )
    if confidence != DECISION_CONFIDENCE_VALUE:
        messages.append(
            f"{label}: Decision handoff Confidence drifted from the bounded "
            "evidence/limitation contract"
        )

    control_consumer_contracts = (
        (
            "GAP-2026-001",
            gap_rows_by_id.get("GAP-2026-001"),
            gap_header,
            "Missing information / control / telemetry",
            {"CTRL-2026-009"},
        ),
        (
            "GAP-2026-002",
            gap_rows_by_id.get("GAP-2026-002"),
            gap_header,
            "Missing information / control / telemetry",
            {"CTRL-2026-005", "CTRL-2026-006"},
        ),
        (
            "GAP-2026-003",
            gap_rows_by_id.get("GAP-2026-003"),
            gap_header,
            "Missing information / control / telemetry",
            {"CTRL-2026-007"},
        ),
        (
            "GAP-2026-004",
            gap_rows_by_id.get("GAP-2026-004"),
            gap_header,
            "Missing information / control / telemetry",
            {"CTRL-2026-008"},
        ),
        (
            "EREQ-2026-001",
            evidence_rows_by_id.get("EREQ-2026-001"),
            evidence_requirement_header,
            "Related Threat / Control / Gap",
            {"CTRL-2026-005", "CTRL-2026-006"},
        ),
        (
            "EREQ-2026-002",
            evidence_rows_by_id.get("EREQ-2026-002"),
            evidence_requirement_header,
            "Related Threat / Control / Gap",
            {"CTRL-2026-007"},
        ),
        (
            "EREQ-2026-003",
            evidence_rows_by_id.get("EREQ-2026-003"),
            evidence_requirement_header,
            "Related Threat / Control / Gap",
            {"CTRL-2026-009"},
        ),
        (
            "EREQ-2026-004",
            evidence_rows_by_id.get("EREQ-2026-004"),
            evidence_requirement_header,
            "Related Threat / Control / Gap",
            {"CTRL-2026-008"},
        ),
        (
            "ACT-TM-2026-001",
            action_rows_by_id.get("ACT-TM-2026-001"),
            action_header,
            "Related Gap / Control / Threat",
            {"CTRL-2026-005"},
        ),
        (
            "ACT-TM-2026-002",
            action_rows_by_id.get("ACT-TM-2026-002"),
            action_header,
            "Related Gap / Control / Threat",
            {"CTRL-2026-007"},
        ),
        (
            "ACT-TM-2026-003",
            action_rows_by_id.get("ACT-TM-2026-003"),
            action_header,
            "Related Gap / Control / Threat",
            {"CTRL-2026-009"},
        ),
        (
            "ACT-TM-2026-004",
            action_rows_by_id.get("ACT-TM-2026-004"),
            action_header,
            "Related Gap / Control / Threat",
            {"CTRL-2026-005", "CTRL-2026-006"},
        ),
        (
            "ACT-TM-2026-005",
            action_rows_by_id.get("ACT-TM-2026-005"),
            action_header,
            "Related Gap / Control / Threat",
            {"CTRL-2026-007"},
        ),
        (
            "ACT-TM-2026-006",
            action_rows_by_id.get("ACT-TM-2026-006"),
            action_header,
            "Related Gap / Control / Threat",
            {"CTRL-2026-008"},
        ),
        (
            "REA-TM-2026-001 Scope",
            reassessment_rows_by_id.get("REA-TM-2026-001"),
            reassessment_header,
            "Scope",
            {"CTRL-2026-005", "CTRL-2026-006"},
        ),
        (
            "REA-TM-2026-001 Closure",
            reassessment_rows_by_id.get("REA-TM-2026-001"),
            reassessment_header,
            "Closure criteria",
            {"CTRL-2026-005", "CTRL-2026-006"},
        ),
        (
            "REA-TM-2026-002 Scope",
            reassessment_rows_by_id.get("REA-TM-2026-002"),
            reassessment_header,
            "Scope",
            {"CTRL-2026-007", "CTRL-2026-009"},
        ),
        (
            "REA-TM-2026-002 Closure",
            reassessment_rows_by_id.get("REA-TM-2026-002"),
            reassessment_header,
            "Closure criteria",
            {"CTRL-2026-007", "CTRL-2026-009"},
        ),
        (
            "REA-TM-2026-003 Scope",
            reassessment_rows_by_id.get("REA-TM-2026-003"),
            reassessment_header,
            "Scope",
            set(),
        ),
        (
            "REA-TM-2026-003 Closure",
            reassessment_rows_by_id.get("REA-TM-2026-003"),
            reassessment_header,
            "Closure criteria",
            set(),
        ),
        (
            "REA-TM-2026-004 Scope",
            reassessment_rows_by_id.get("REA-TM-2026-004"),
            reassessment_header,
            "Scope",
            {"CTRL-2026-008"},
        ),
        (
            "REA-TM-2026-004 Closure",
            reassessment_rows_by_id.get("REA-TM-2026-004"),
            reassessment_header,
            "Closure criteria",
            {"CTRL-2026-008"},
        ),
    )
    for identifier, row, header, field, expected_control_ids in control_consumer_contracts:
        if row is None:
            messages.append(f"{label}: missing Control consumer {identifier}")
            continue
        observed_control_ids = set(
            re.findall(r"\bCTRL-2026-\d{3}\b", row[header.index(field)])
        )
        if observed_control_ids != expected_control_ids:
            messages.append(
                f"{label}: {identifier} {field} Control references "
                f"{sorted(observed_control_ids)!r} != {sorted(expected_control_ids)!r}"
            )

    reauthorization_markers = (
        "合成TenantであってもApp permission、consent、Identity bindingなどの設定変更を行う場合。",
        "RoEのmethod / time windowを越えて合成Rule testを再実施する場合。",
        "Telemetryの収集設定またはProduction Pipelineを変更する場合。",
    )
    for marker in reauthorization_markers:
        if marker not in text:
            messages.append(f"{label}: missing reauthorization gate {marker!r}")

    expected_traceability_assertions = (
        f"- [x] {len(EXPECTED_CASE_IDS['EREQ'])}つのEvidence Requirementがある",
        f"- [x] {len(EXPECTED_CASE_IDS['ASM'])}つのAssumptionと"
        f"{len(EXPECTED_CASE_IDS['GAP'])}つのGapがある",
    )
    for assertion in expected_traceability_assertions:
        if text.count(assertion) != 1:
            messages.append(
                f"{label}: traceability assertion must occur exactly once and derive from finite ID sets: "
                f"{assertion!r}"
            )

    definition_contracts: tuple[tuple[str, list[list[str]], int, bool], ...] = (
        ("ASSET", parsed.get(asset_header, []), 0, True),
        ("FLOW", parsed.get(table_contracts[1][0], []), 0, True),
        ("TB", parsed.get(boundary_header, []), 0, True),
        ("EXP", case_tables.get(count_contracts[0][0], []), 0, True),
        ("EP", entry_point_rows, 0, True),
        ("TH", parsed.get(table_contracts[3][0], []), 0, True),
        ("MISUSE", case_tables.get(count_contracts[1][0], []), 0, True),
        ("PATH", path_rows, 0, False),
        ("EDGE", path_rows, 1, True),
        ("CTRL", parsed.get(table_contracts[4][0], []), 0, True),
        ("ASM", case_tables.get(count_contracts[3][0], []), 0, True),
        ("GAP", case_tables.get(count_contracts[4][0], []), 0, True),
        ("EREQ", case_tables.get(count_contracts[5][0], []), 0, True),
        ("ACT-TM", action_rows, 0, True),
        ("REA-TM", case_tables.get(count_contracts[6][0], []), 0, True),
    )
    for family, rows, column, unique_definition in definition_contracts:
        identifiers = [
            match.group(1)
            for row in rows
            if len(row) > column
            for match in [re.fullmatch(rf"`?({re.escape(family)}-2026-\d{{3}})`?", row[column])]
            if match
        ]
        if set(identifiers) != EXPECTED_CASE_IDS[family]:
            messages.append(
                f"{label}: defined {family} IDs {sorted(set(identifiers))!r} "
                f"!= {sorted(EXPECTED_CASE_IDS[family])!r}"
            )
        if unique_definition:
            duplicates = sorted(identifier for identifier, count in Counter(identifiers).items() if count != 1)
            if duplicates:
                messages.append(f"{label}: {family} IDs must each be defined exactly once: {duplicates!r}")

    for family, expected in EXPECTED_CASE_IDS.items():
        observed = set(re.findall(rf"\b{family}-2026-\d{{3}}\b", text))
        expected_references = EXPECTED_CASE_REFERENCE_IDS[family]
        if observed != expected_references:
            messages.append(
                f"{label}: {family} reference IDs {sorted(observed)!r} != "
                f"{sorted(expected_references)!r}"
            )

    auxiliary_definition_contracts = (
        (
            "Dependency",
            ("Dependency ID", "From asset", "To asset", "Why the dependency matters", "Failure consequence"),
            EXPECTED_DEPENDENCY_IDS,
        ),
        (
            "Rubric",
            ("Rubric ID", "Criterion", "Meets", "Partially meets", "Does not meet"),
            EXPECTED_RUBRIC_IDS,
        ),
        (
            "Handoff",
            HANDOFF_HEADER,
            EXPECTED_HANDOFF_IDS,
        ),
    )
    for family, header, expected in auxiliary_definition_contracts:
        rows, table_messages = table_by_header(text, header, label)
        messages.extend(table_messages)
        observed = [cell for row in rows if row for cell in re.findall(r"[A-Z][A-Z0-9-]+-2026-\d{3}", row[0])]
        if set(observed) != expected:
            messages.append(f"{label}: defined {family} IDs {sorted(set(observed))!r} != {sorted(expected)!r}")
        duplicates = sorted(identifier for identifier, count in Counter(observed).items() if count != 1)
        if duplicates:
            messages.append(f"{label}: {family} IDs must each be defined exactly once: {duplicates!r}")

    handoff_rows, handoff_messages = table_by_header(text, HANDOFF_HEADER, label)
    messages.extend(handoff_messages)
    observed_handoffs = {
        row[0].strip("`"): (row[1], row[2], row[3])
        for row in handoff_rows
        if len(row) == len(HANDOFF_HEADER)
    }
    if observed_handoffs != EXPECTED_HANDOFF_ROWS:
        messages.append(
            f"{label}: Handoff semantic mapping {observed_handoffs!r} != {EXPECTED_HANDOFF_ROWS!r}"
        )
    expected_handoff_controls = {
        "HO-TM-2026-005": set(),
        "HO-TM-2026-006": {"CTRL-2026-007", "CTRL-2026-009"},
        "HO-TM-2026-009": {"CTRL-2026-008"},
        "HO-TM-2026-011": {"CTRL-2026-005"},
        "HO-TM-2026-012": {"CTRL-2026-006"},
        "HO-TM-2026-013": {"CTRL-2026-006"},
        "HO-TM-2026-014": {"CTRL-2026-008"},
        "HO-TM-2026-015": set(CHAPTER4_CONTROL_RELATIONS),
        "HO-TM-2026-027": set(),
    }
    handoff_rows_by_id = {
        row[0].strip("`"): row
        for row in handoff_rows
        if len(row) == len(HANDOFF_HEADER)
    }
    for handoff_id, expected_control_ids in expected_handoff_controls.items():
        row = handoff_rows_by_id.get(handoff_id)
        if row is None:
            messages.append(f"{label}: missing Control handoff consumer {handoff_id}")
            continue
        provided = row[HANDOFF_HEADER.index("What this artifact provides")]
        observed_control_ids = set(re.findall(r"\bCTRL-2026-\d{3}\b", provided))
        if observed_control_ids != expected_control_ids:
            messages.append(
                f"{label}: {handoff_id} Control references "
                f"{sorted(observed_control_ids)!r} != {sorted(expected_control_ids)!r}"
            )
    for line in EXPECTED_HANDOFF_INTERPRETATION_LINES:
        if text.count(line) != 1:
            messages.append(
                f"{label}: Handoff interpretation Control trace must occur exactly once: "
                f"{line!r}"
            )
    if text.count(HANDOFF_INTERPRETATION_BOUNDARY) != 1:
        messages.append(
            f"{label}: Handoff interpretation must identify itself as a non-exhaustive "
            f"reader aid and keep the table as canonical: {HANDOFF_INTERPRETATION_BOUNDARY!r}"
        )

    downstream_control_references = {
        "Evidence Requirement": [
            row[evidence_requirement_header.index("Related Threat / Control / Gap")]
            for row in evidence_rows_by_id.values()
        ],
        "Action": [
            row[action_header.index("Related Gap / Control / Threat")]
            for row in action_rows_by_id.values()
        ],
        "Reassessment": [
            " ".join(
                (
                    row[reassessment_header.index("Scope")],
                    row[reassessment_header.index("Closure criteria")],
                )
            )
            for row in reassessment_rows_by_id.values()
        ],
        "Handoff": [
            row[HANDOFF_HEADER.index("What this artifact provides")]
            for row in handoff_rows_by_id.values()
        ],
    }
    for control_id, control_row in controls_by_id.items():
        gap_ids = set(
            re.findall(
                r"\bGAP-2026-\d{3}\b",
                control_row[control_header.index("Gap ID")],
            )
        )
        if len(gap_ids) != 1:
            messages.append(
                f"{label}: {control_id} must identify exactly one reverse-trace Gap; "
                f"found {sorted(gap_ids)!r}"
            )
        else:
            gap_id = next(iter(gap_ids))
            gap_row = gap_rows_by_id.get(gap_id)
            if gap_row is None or control_id not in gap_row[gap_header.index("Missing information / control / telemetry")]:
                messages.append(
                    f"{label}: {control_id} -> {gap_id} is not reversed by the Gap row"
                )
        for consumer_kind, values in downstream_control_references.items():
            if not any(control_id in value for value in values):
                messages.append(
                    f"{label}: {control_id} has no finite {consumer_kind} consumer"
                )

    inherited_evidence = set(re.findall(r"\b(?:EVD-2026-\d{3}|EVD-AUTH-2026-\d{3}|NEG-2026-\d{3})\b", text))
    if inherited_evidence != EXPECTED_INHERITED_EVIDENCE_IDS:
        messages.append(
            f"{label}: inherited Evidence IDs {sorted(inherited_evidence)!r} "
            f"!= {sorted(EXPECTED_INHERITED_EVIDENCE_IDS)!r}"
        )
    evidence_sources = {
        "cases/ch01-integrated-security-case-example.md": EXPECTED_INHERITED_EVIDENCE_IDS - {"EVD-AUTH-2026-001"},
        "cases/ch02-authorization-decision-example.md": {"EVD-AUTH-2026-001"},
    }
    for relative, expected_ids in evidence_sources.items():
        source_text = (ROOT / relative).read_text(encoding="utf-8") if (ROOT / relative).is_file() else ""
        missing = sorted(identifier for identifier in expected_ids if identifier not in source_text)
        if missing:
            messages.append(f"{label}: inherited Evidence IDs missing from {relative}: {missing!r}")

    fields, adapter_messages = classified_table_fields(text, label, CASE_TABLE_OCCURRENCES)
    messages.extend(adapter_messages)
    messages.extend(policy_errors(fields))
    messages.extend(document_reader_visible_policy_errors(text, label))
    return messages


def source_contract_errors(chapter: str, registry: dict, note: str) -> list[str]:
    messages: list[str] = []
    if registry.get("checkedAt") != "2026-07-25":
        messages.append("references/sources.json: registry-level checkedAt must remain 2026-07-25")
    entries = {item.get("id"): item for item in registry.get("sources", []) if isinstance(item, dict)}
    expected = {
        "SRC-CSF-001": {
            "status": "final",
            "version": "2.0",
            "url": "https://www.nist.gov/cyberframework",
            "publishedAt": "2024-02-26",
            "checkedAt": "2026-08-08",
            "nextReviewAt": "2026-11-08",
            "reviewTriggers": [
                "NIST CSF revision or errata",
                "NIST CSF 2.0 resource-center or outcome-taxonomy change used by Chapter 4",
            ],
            "markers": ("高位Outcome taxonomy", "実装方法を規定せず", "完全性"),
        },
        "SRC-NIST-RISK-001": {
            "status": "final",
            "version": "SP 800-30 Rev.1",
            "url": "https://csrc.nist.gov/pubs/sp/800/30/r1/final",
            "publishedAt": "2012-09-17",
            "checkedAt": "2026-08-08",
            "nextReviewAt": "2026-11-08",
            "reviewTriggers": [
                "NIST SP 800-30 revision, withdrawal, successor, or errata",
                "NIST Risk Management publications index status change",
                "Change to a threat source, threat event, vulnerability, predisposing condition, likelihood, impact, or uncertainty concept used by Chapter 4",
            ],
            "markers": ("Federal", "数値Risk score", "後継版"),
        },
        "SRC-OWASP-TM-001": {
            "status": "maintained-project-guidance",
            "version": None,
            "url": "https://owasp.org/www-project-threat-modeling/",
            "publishedAt": None,
            "checkedAt": "2026-08-08",
            "nextReviewAt": "2026-11-08",
            "reviewTriggers": [
                "OWASP project status or methodology-neutral guidance change",
                "OWASP Threat Modeling Project resource, tool, or historical-material classification change",
                "Project URL relocation or retirement",
            ],
            "markers": (
                "Maintained Project Guidance",
                "単一の公式OWASP Threat Modeling methodologyを定義しない",
                "継続更新されるProject pageには固定versionと単一published dateが提示されていない",
                "versionとpublishedAtは推測せずnullとする",
                "checkedAt、nextReviewAt、reviewTriggersで現行pageとProject statusを追跡",
                "公式に固定version、公開日またはreleaseが提示された場合に再監査",
                "方法論中立の補助参照としてのみ用いる",
                "Threat Modelの完全性、Control有効性または評価品質の証明ではない",
            ),
        },
    }
    for source_id, contract in expected.items():
        entry = entries.get(source_id)
        if not entry:
            messages.append(f"references/sources.json: missing {source_id}")
            continue
        for field in ("status", "version", "url", "publishedAt", "checkedAt", "nextReviewAt", "reviewTriggers"):
            if entry.get(field) != contract[field]:
                messages.append(f"references/sources.json: {source_id}.{field} {entry.get(field)!r} != {contract[field]!r}")
        if 4 not in entry.get("chapters", []):
            messages.append(f"references/sources.json: {source_id} does not map Chapter 4")
        notes = entry.get("notes")
        if not isinstance(notes, str):
            messages.append(f"references/sources.json: {source_id}.notes must be a string")
        else:
            for marker in contract["markers"]:
                if marker not in notes:
                    messages.append(f"references/sources.json: {source_id}.notes missing {marker!r}")
    mapped = {source_id for source_id, entry in entries.items() if 4 in entry.get("chapters", [])}
    if mapped != EXPECTED_SOURCE_IDS:
        messages.append(f"references/sources.json: Chapter 4 mapping {sorted(mapped)!r} != {sorted(EXPECTED_SOURCE_IDS)!r}")
    messages.extend(require_tokens(SOURCE_NOTE, note, (
        "Resumed-run workspace search",
        "Direct textual adoption in this PR: なし",
        "Raw predraft tracked files: `0`",
        "SRC-CSF-001",
        "SRC-NIST-RISK-001",
        "SRC-OWASP-TM-001",
        "Historical OWASP `Threat Modeling Process` page",
        "OWASP Threat Dragonは本文の論証に不要",
        "Registry rootの`checkedAt`",
    )))
    return messages


def control_definition_collision_errors(
    documents: tuple[tuple[str, str], ...],
) -> list[str]:
    """Reject Chapter 4 Control IDs defined by a different canonical document."""

    messages: list[str] = []
    for relative, text in documents:
        if relative == CASE:
            continue
        definitions = set(
            re.findall(
                r"^\|\s*`(CTRL-2026-\d{3})`\s*\|",
                text,
                re.MULTILINE,
            )
        )
        collisions = sorted(definitions & set(CHAPTER4_CONTROL_RELATIONS))
        if collisions:
            messages.append(
                f"{relative}: fresh Chapter 4 Control IDs already defined outside "
                f"{CASE}: {collisions!r}"
            )
    return messages


def fresh_control_definition_errors() -> list[str]:
    """Check every tracked Markdown definition against the fresh Chapter 4 IDs."""

    result = subprocess.run(
        ["git", "ls-files", "-z", "--", "*.md"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    documents: list[tuple[str, str]] = []
    for raw_relative in result.stdout.decode("utf-8").split("\0"):
        if not raw_relative:
            continue
        path = ROOT / raw_relative
        if not path.is_file():
            continue
        documents.append((raw_relative, path.read_text(encoding="utf-8")))
    return control_definition_collision_errors(tuple(documents))


def hypothesis_definition_collision_errors(
    documents: tuple[tuple[str, str], ...],
) -> list[str]:
    """Reject fresh Chapter 4 Hypothesis IDs defined by another document."""

    messages: list[str] = []
    for relative, text in documents:
        if relative == CASE:
            continue
        definitions = set(
            re.findall(
                r"^\|\s*`(TH-2026-\d{3})`\s*\|",
                text,
                re.MULTILINE,
            )
        )
        collisions = sorted(definitions & FRESH_CHAPTER4_HYPOTHESIS_IDS)
        if collisions:
            messages.append(
                f"{relative}: fresh Chapter 4 Hypothesis IDs already defined outside "
                f"{CASE}: {collisions!r}"
            )
    return messages


def fresh_hypothesis_definition_errors() -> list[str]:
    """Check every tracked Markdown definition against fresh Chapter 4 IDs."""

    result = subprocess.run(
        ["git", "ls-files", "-z", "--", "*.md"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    documents: list[tuple[str, str]] = []
    for raw_relative in result.stdout.decode("utf-8").split("\0"):
        if not raw_relative:
            continue
        path = ROOT / raw_relative
        if not path.is_file():
            continue
        documents.append((raw_relative, path.read_text(encoding="utf-8")))
    return hypothesis_definition_collision_errors(tuple(documents))


def page_contract_errors(registry: dict, label: str) -> list[str]:
    pages = registry.get("pages", [])
    tuples = Counter((item.get("source"), item.get("destination"), item.get("section"), item.get("order")) for item in pages if isinstance(item, dict))
    routes = Counter((item.get("source"), item.get("destination")) for item in pages if isinstance(item, dict))
    messages: list[str] = []
    for expected in sorted(EXPECTED_PAGES):
        if tuples[expected] != 1:
            messages.append(f"{label}: expected Chapter 4 tuple exactly once: {expected!r}; found {tuples[expected]}")
        if routes[expected[:2]] != 1:
            messages.append(f"{label}: expected Chapter 4 route exactly once: {expected[:2]!r}; found {routes[expected[:2]]}")
    return messages


def page_title_contract_errors(registry: dict, label: str) -> list[str]:
    """Bind Chapter 4 titles without conflating them with route identity."""

    pages = registry.get("pages", [])
    messages: list[str] = []
    for source, expected_title in sorted(EXPECTED_PAGE_TITLES.items()):
        actual_titles = [
            item.get("title")
            for item in pages
            if isinstance(item, dict) and item.get("source") == source
        ]
        if actual_titles != [expected_title]:
            messages.append(
                f"{label}: expected Chapter 4 title for {source!r} exactly once as "
                f"{expected_title!r}; found {actual_titles!r}"
            )
    return messages


def registry_rejected(registry: dict, label: str) -> bool:
    try:
        parsed = parse_registry_data(registry, label)
    except SitePageRegistryError:
        return True
    return bool(
        page_contract_errors(parsed, label)
        or page_title_contract_errors(parsed, label)
    )


def publication_contract_errors() -> list[str]:
    messages: list[str] = []
    index_contracts = {
        "artifact-index.md": ("ART-03", "cases/ch04-threat-model-example.md"),
        "figure-index.md": (
            "F-04-01 | Decision RequirementからReassessmentまでのTrace",
            "F-04-02 | 境界、Flow、攻撃面の読み分け",
            "T-04-01 | 資産の型と最小記録項目",
            "T-04-02 | 似て見える用語の違い",
            "T-04-03 | Control assurance states",
            "T-04-04 | Knowledge stateとHypothesis statusの分離",
        ),
        "glossary.md": ("Business Asset", "Data Asset", "Identity", "Control Plane", "Trust Boundary", "Attack Surface", "Exposure", "Entry Point", "Threat Hypothesis", "Misuse Case", "Attack Path", "Evidence Requirement", "Assurance State", "Knowledge State"),
        "cases/index.md": ("ch04-threat-model-example.md", "Threat Model"),
        "index.md": (CHAPTER, TEMPLATE, CASE),
    }
    for relative, tokens in index_contracts.items():
        messages.extend(require_tokens(relative, read_text(relative), tokens))
    try:
        tracked = subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
    except subprocess.CalledProcessError as exc:
        messages.append(f"git ls-files failed: {exc}")
    else:
        forbidden = [path for path in tracked if ".predraft." in path or "parallel-drafts-2026-08-08" in path or path.startswith(".work/")]
        if forbidden:
            messages.append(f"raw Editorial Input must remain untracked: {forbidden!r}")
    return messages


def changelog_contract_errors(text: str, label: str) -> list[str]:
    """Require Chapter 4 reader impact in the current Unreleased section."""

    unreleased_match = re.search(
        r"^## Unreleased\s*$\n(?P<body>.*?)(?=^## (?!Unreleased\s*$)|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not unreleased_match:
        return [f"{label}: missing Unreleased section"]
    unreleased = unreleased_match.group("body")
    added_match = re.search(
        r"^### Added\s*$\n(?P<body>.*?)(?=^### |\Z)",
        unreleased,
        re.MULTILINE | re.DOTALL,
    )
    changed_match = re.search(
        r"^### Changed\s*$\n(?P<body>.*?)(?=^### |\Z)",
        unreleased,
        re.MULTILINE | re.DOTALL,
    )
    messages: list[str] = []
    if not added_match:
        messages.append(f"{label}: Unreleased missing Added subsection")
    else:
        added_lines = [line for line in added_match.group("body").splitlines() if line.startswith("- ")]
        chapter4_added = next((line for line in added_lines if "ART-03" in line), "")
        if not chapter4_added:
            messages.append(f"{label}: Unreleased Added missing Chapter 4 / ART-03 reader impact")
        else:
            messages.extend(
                require_tokens(
                    f"{label}: Chapter 4 Added entry",
                    chapter4_added,
                    ("第4章", "ART-03", "合成Case", "contract"),
                )
            )
    if not changed_match:
        messages.append(f"{label}: Unreleased missing Changed subsection")
        return messages

    changed_lines = [line for line in changed_match.group("body").splitlines() if line.startswith("- ")]
    source_change = next((line for line in changed_lines if "NIST CSF 2.0" in line), "")
    if not source_change:
        messages.append(f"{label}: Unreleased Changed missing Chapter 4 Source reader impact")
        return messages
    messages.extend(
        require_tokens(
            f"{label}: Chapter 4 Source impact",
            source_change,
            CHANGELOG_CH04_SOURCE_NAMES
            + ("Source Registry", "章対応", "確認日", "次回確認", "Framework mapping"),
        )
    )
    if not re.search(
        r"Framework mapping.*実装.*検証.*完全性.*(?:証明ではない|証明しない|保証しない)",
        source_change,
    ):
        messages.append(
            f"{label}: Chapter 4 Source impact must state that Framework mapping does not "
            "prove or guarantee implementation, validation, or completeness"
        )
    return messages


def negative_regressions(
    chapter: str,
    template: str,
    case: str,
    raw_registry: dict,
    sources: dict,
    note: str,
    changelog: str,
) -> None:
    reader_visible_adapter_contract_regressions()
    chapter_mutations = (
        ("missing OWN", chapter.replace("### OWN", "### OWNERSHIP", 1)),
        ("inventory conflation", chapter.replace("Componentを列挙するだけでは", "ComponentはBusiness Assetなので列挙すれば", 1)),
        ("business asset type conflation", chapter.replace("`Business Asset`は8番目のTypeではなく", "`Business Asset`は8番目のTypeであり", 1)),
        ("network-only boundary", chapter.replace("Network segmentはBoundary候補に過ぎない", "Network segmentだけがTrust Boundaryの定義である", 1)),
        ("threat finding conflation", chapter.replace("`Threat`は、望ましくない事象や行為である。", "`Threat`は、`Vulnerability`および`Finding`と同義である。", 1)),
        ("control validation conflation", chapter.replace("文書化されたControlがあるので十分である\n誤りである", "文書化されたControlがあるのでValidatedである\n正しい。", 1)),
        ("mapping completeness", chapter.replace("CSFやOWASPへMappingしたので完全である\n誤りである", "CSFやOWASPへMappingしたので完全である\n正しい。", 1)),
        (
            "ART-03 canonical section drift",
            chapter.replace("10. `Assumptions, Unknowns and Gaps`", "10. `Inventory only`", 1),
        ),
        (
            "rubric mapping drift",
            chapter.replace("`RUBRIC-TM-YYYY-003` Threat usefulness and evidence sufficiency", "`RUBRIC-TM-YYYY-999` Threat count", 1),
        ),
        (
            "walkthrough falls back to inherited TH-2026-001",
            chapter.replace(
                f"「{SUMMARY_TH_004_PROPOSITION}」を`TH-2026-004`として記録し",
                f"「{SUMMARY_TH_004_PROPOSITION}」を`TH-2026-001`として記録し",
                1,
            ),
        ),
        (
            "walkthrough omits current EDGE-2026-002",
            chapter.replace(
                "2026-07-25 remediation後のcurrent scope / binding未確認を`EDGE-2026-002`、",
                "2026-07-25 remediation後のcurrent scope / binding未確認を記録せず、",
                1,
            ),
        ),
        (
            "walkthrough omits Tenant EDGE-2026-004",
            chapter.replace(
                "、Tenant binding Evidence不足を`EDGE-2026-004`へ分けて",
                "へ分けて",
                1,
            ),
        ),
        (
            "walkthrough omits identity Control",
            chapter.replace(
                "`CTRL-2026-005`と`CTRL-2026-006`がDocumentedに留まるなら",
                "`CTRL-2026-005`がDocumentedに留まるなら",
                1,
            ),
        ),
        (
            "walkthrough omits identity Action",
            chapter.replace(
                "`ACT-TM-2026-001` / `ACT-TM-2026-004`",
                "`ACT-TM-2026-001`",
                1,
            ),
        ),
        *(
            (
                f"{heading.split()[0]} rendered-table opening boundary",
                chapter.replace(f"### {heading}\n\n|", f"### {heading}\n|", 1),
            )
            for heading in EXPECTED_CHAPTER_MARKDOWN_TABLE_HEADINGS
        ),
        *(
            (
                f"{heading.split()[0]} rendered-table closing boundary",
                re.sub(
                    rf"(^### {re.escape(heading)}\n\n(?:\|[^\n]*\|\n)+)\n(?=\S)",
                    r"\1",
                    chapter,
                    count=1,
                    flags=re.MULTILINE,
                ),
            )
            for heading in EXPECTED_CHAPTER_MARKDOWN_TABLE_HEADINGS
        ),
    )
    for name, mutation in chapter_mutations:
        if not chapter_contract_errors(mutation, f"negative chapter {name}"):
            error(f"negative regression accepted Chapter 4 mutation: {name}")
    prose_surface_negative_regressions(
        chapter,
        CHAPTER,
        (
            (
                "chapter ATX heading",
                "# 第4章 資産、信頼境界、攻撃面、脅威モデル",
            ),
            (
                "ordinary chapter prose",
                "Threat Modelは、図を描く作業ではなく、判断要求をレビュー可能な記録へ変換する作業である。",
            ),
        ),
    )
    safety_matrix_negative_regressions(chapter, CHAPTER, CHAPTER_TABLE_OCCURRENCES)
    pipe_prefixed_prose_surface_regressions(
        chapter, CHAPTER, chapter_contract_errors
    )
    liquid_surface_regressions(chapter, CHAPTER, chapter_contract_errors)
    raw_html_surface_regressions(chapter, CHAPTER, chapter_contract_errors)
    bare_angle_surface_regressions(chapter, CHAPTER, chapter_contract_errors)
    angle_entity_surface_regressions(chapter, CHAPTER, chapter_contract_errors)
    reference_link_label_surface_regressions(
        chapter, CHAPTER, chapter_contract_errors
    )
    inline_link_label_surface_regressions(
        chapter, CHAPTER, chapter_contract_errors
    )
    kramdown_underscore_emphasis_surface_regressions(
        chapter, CHAPTER, chapter_contract_errors
    )
    kramdown_ial_surface_regressions(
        chapter, CHAPTER, chapter_contract_errors
    )
    inline_code_comment_surface_regressions(
        chapter, CHAPTER, chapter_contract_errors
    )
    markdown_title_comment_surface_regressions(
        chapter, CHAPTER, chapter_contract_errors
    )
    multiline_inline_code_surface_regressions(
        chapter, CHAPTER, chapter_contract_errors
    )
    fenced_surface_regressions(chapter, CHAPTER, chapter_contract_errors)
    indented_code_surface_regressions(chapter, CHAPTER, chapter_contract_errors)
    footnote_surface_regressions(chapter, CHAPTER, chapter_contract_errors)

    template_mutations = (
        ("model status", template.replace("Draft / In Review / Approved for Assessment / Needs Evidence / Superseded", "Draft / Complete", 1)),
        ("boundary finite set", template.replace("Identity Authority / Data Ownership / Administrative Control / Tenant / Third-party Responsibility / Control Plane / Network", "Network", 1)),
        ("control assurance", template.replace("Unknown / Documented / Implemented / Observed / Validated", "Mapped / Validated")),
        ("minimum evidence boundary", template.replace("Minimum sufficient evidence | Forbidden / over-collection boundary", "Evidence | Notes", 1)),
        ("Flow Evidence status", template.replace("| Planned |", "| Confirmed |", 1)),
        ("missing Decision owner", template.replace("| Decision owner |  |\n", "", 1)),
        ("Decision Context field drift", template.replace("| Decision deadline | ISO 8601 |", "| Review date | ISO 8601 |", 1)),
        ("Gap status", template.replace("| ISO 8601 date | Open |", "| ISO 8601 date | Confirmed |", 1)),
        (
            "Collected Evidence status",
            template.replace("| Synthetic / Authorized isolated / Inherited | Planned |", "| Synthetic / Authorized isolated / Inherited | Confirmed |", 1),
        ),
        (
            "Threat Hypothesis Evidence needed unsafe external action",
            template.replace(
                "|  |  | `EREQ-YYYY-NNN` |  | High / Medium / Low |",
                "|  |  | `EREQ-YYYY-NNN`。第三者の本番システムへ接続する |  | High / Medium / Low |",
                1,
            ),
        ),
        (
            "Attack Path From Asset State unsafe external action",
            template.replace(
                "| `PATH-YYYY-NNN` | `EDGE-YYYY-NNN` | `ASSET-YYYY-NNN` / state |  |",
                "| `PATH-YYYY-NNN` | `EDGE-YYYY-NNN` | `ASSET-YYYY-NNN` / 第三者の本番システムへ接続する |  |",
                1,
            ),
        ),
        (
            "Attack Path To Asset State unsafe external action",
            template.replace(
                "| `TB-YYYY-NNN` | `ASSET-YYYY-NNN` / state | `ASSET-YYYY-NNN` |",
                "| `TB-YYYY-NNN` | `ASSET-YYYY-NNN` / 第三者の本番システムへ接続する | `ASSET-YYYY-NNN` |",
                1,
            ),
        ),
    )
    for name, mutation in template_mutations:
        if not template_contract_errors(mutation, f"negative template {name}"):
            error(f"negative regression accepted ART-03 mutation: {name}")
    safety_matrix_negative_regressions(template, TEMPLATE, TEMPLATE_TABLE_OCCURRENCES)
    prose_surface_negative_regressions(
        template,
        TEMPLATE,
        (
            (
                "ART-03 ATX heading",
                "# Threat Model",
            ),
            (
                "usage-condition list item",
                "合成Case、自己所有環境、または明示的に許可された隔離環境だけを前提とする。",
            ),
        ),
    )
    pipe_prefixed_prose_surface_regressions(
        template, TEMPLATE, template_contract_errors
    )
    liquid_surface_regressions(template, TEMPLATE, template_contract_errors)
    raw_html_surface_regressions(template, TEMPLATE, template_contract_errors)
    bare_angle_surface_regressions(template, TEMPLATE, template_contract_errors)
    angle_entity_surface_regressions(template, TEMPLATE, template_contract_errors)
    reference_link_label_surface_regressions(
        template, TEMPLATE, template_contract_errors
    )
    inline_link_label_surface_regressions(
        template, TEMPLATE, template_contract_errors
    )
    kramdown_underscore_emphasis_surface_regressions(
        template, TEMPLATE, template_contract_errors
    )
    kramdown_ial_surface_regressions(
        template, TEMPLATE, template_contract_errors
    )
    inline_code_comment_surface_regressions(
        template, TEMPLATE, template_contract_errors
    )
    markdown_title_comment_surface_regressions(
        template, TEMPLATE, template_contract_errors
    )
    multiline_inline_code_surface_regressions(
        template, TEMPLATE, template_contract_errors
    )
    fenced_surface_regressions(template, TEMPLATE, template_contract_errors)
    indented_code_surface_regressions(template, TEMPLATE, template_contract_errors)
    footnote_surface_regressions(template, TEMPLATE, template_contract_errors)

    unsafe_samples = (
        "第三者の本番システムへ接続する",
        "実Tokenを取得してEvidenceにする",
        "個人情報を収集する",
        "マルウェアを実行する",
        "C2 infrastructureを運用する",
        "DoSを実行する",
        "システムのログを削除する",
        "persistenceを構築する",
        "https://example.comへ接続する",
        "198.18.0.1へ接続する",
    )
    for sample in unsafe_samples:
        if not policy_errors([("Chapter 4 negative safety mutation", sample)]):
            error(f"Content Safety Policy accepted unsafe Chapter 4 mutation: {sample!r}")
    safe_samples = (
        "第三者の本番システムへ接続しない",
        "合成Token literalをoffline fixtureで記録する",
        "個人情報の収集は禁止する",
        "マルウェア分類の危険性を分析する",
        "DoSを実行しない",
        "https://lab.example/runbook",
        "192.0.2.10",
    )
    for sample in safe_samples:
        findings = policy_errors([("Chapter 4 safe safety mutation", sample)])
        if findings:
            error(f"Content Safety Policy rejected safe Chapter 4 counterpart {sample!r}: {findings!r}")

    if case:
        case_mutations = (
            ("mixed Model status", case.replace("Needs Evidence", "Decision Support", 1)),
            (
                "self-parent relation cycle",
                case.replace("| Parent Case ID | `CASE-2026-001` |", "| Parent Case ID | `TM-2026-001` |", 1),
            ),
            (
                "missing Decision owner",
                case.replace("| Decision owner | Synthetic CTO Decision Owner |\n", "", 1),
            ),
            (
                "Decision Context field drift",
                case.replace("| Decision deadline | 2026-08-19T18:00:00+09:00 |", "| Review date | 2026-08-19T18:00:00+09:00 |", 1),
            ),
            (
                "Decision handoff Confidence missing",
                case.replace(f"{DECISION_CONFIDENCE_ROW}\n", "", 1),
            ),
            (
                "Decision handoff Confidence unsupported overclaim",
                case.replace(
                    DECISION_CONFIDENCE_ROW,
                    "| Confidence | 高。既存のhistorical Evidenceだけで不確実性はない |",
                    1,
                ),
            ),
            (
                "top-level ART-03 section drift",
                case.replace("## 10. Evidence Requirements and Actions", "## 10. Evidence Inventory", 1),
            ),
            (
                "inherited Chapter 1 Control ID redefined",
                case.replace(
                    "| `CTRL-2026-005` | `ASSET-2026-004`, `ASSET-2026-005`",
                    "| `CTRL-2026-001` | `ASSET-2026-004`, `ASSET-2026-005`",
                    1,
                ),
            ),
            (
                "fresh Chapter 4 Control ID duplicated",
                case.replace(
                    "| `CTRL-2026-006` | `ASSET-2026-005`, `ASSET-2026-007`",
                    "| `CTRL-2026-005` | `ASSET-2026-005`, `ASSET-2026-007`",
                    1,
                ),
            ),
            (
                "Control inheritance relation drift",
                case.replace(
                    "- `CTRL-2026-005`は第1章`CTRL-2026-001`「必要scopeだけへ縮小」",
                    "- `CTRL-2026-005`は第1章`CTRL-2026-002`「必要scopeだけへ縮小」",
                    1,
                ),
            ),
            (
                "Control consumer falls back to inherited ID",
                case.replace(
                    "`TH-2026-001` / `TH-2026-004` / `CTRL-2026-005` / `CTRL-2026-006`: "
                    "2026-07-25 scope縮小`Passed`後のcurrent App registration export",
                    "`TH-2026-001` / `TH-2026-004` / `CTRL-2026-001` / `CTRL-2026-006`: "
                    "2026-07-25 scope縮小`Passed`後のcurrent App registration export",
                    1,
                ),
            ),
            (
                "CTRL-2026-006 identity assurance overclaimed",
                case.replace(
                    "| Platform | Documented | `EVD-2026-001` | "
                    "`EVD-2026-001`はApp registration scope Snapshotに限られ",
                    "| Platform | Implemented | `EVD-2026-001` | "
                    "`EVD-2026-001`はApp registration scope Snapshotに限られ",
                    1,
                ),
            ),
            (
                "FLOW-2026-006 current identity Evidence overclaimed",
                case.replace(
                    f"| Restricted | {FLOW_006_EVIDENCE_STATUS} | "
                    f"{FLOW_006_OBSERVATION_POINT} |",
                    f"| Restricted | Collected | {FLOW_006_OBSERVATION_POINT} |",
                    1,
                ),
            ),
            (
                "FLOW-2026-006 current identity Evidence fabricated",
                case.replace(
                    FLOW_006_OBSERVATION_POINT,
                    "identity binding、usage observation、rotation結果を収集済み",
                    1,
                ),
            ),
            (
                "FLOW-2026-006 planned artifact terminology drift",
                case.replace(
                    "post-remediation Workload identity binding snapshot",
                    "identity inventory",
                    1,
                ),
            ),
            (
                "FLOW-2026-004 composite audit Evidence overclaimed",
                case.replace(
                    f"| Internal | {FLOW_004_EVIDENCE_STATUS} | "
                    f"{FLOW_004_OBSERVATION_POINT} |",
                    f"| Internal | Collected | {FLOW_004_OBSERVATION_POINT} |",
                    1,
                ),
            ),
            (
                "FLOW-2026-004 lifecycle Evidence gap hidden",
                case.replace(
                    FLOW_004_OBSERVATION_POINT,
                    "Admin consent EventとApp identity lifecycle Eventの監査Coverage、"
                    "両Event classのRule test結果を収集済み",
                    1,
                ),
            ),
            (
                "TB-2026-004 current binding assurance overclaimed",
                case.replace(
                    "| HumanとWorkloadの責任境界が曖昧化 | Unknown | - |",
                    "| HumanとWorkloadの責任境界が曖昧化 | Confirmed | - |",
                    1,
                ),
            ),
            (
                "TB-2026-004 historical Evidence reused for current binding",
                case.replace(
                    "| HumanとWorkloadの責任境界が曖昧化 | Unknown | - |",
                    "| HumanとWorkloadの責任境界が曖昧化 | Unknown | "
                    "`EVD-2026-001`, `EVD-2026-003` |",
                    1,
                ),
            ),
            (
                "TB-2026-004 historical/current Evidence boundary omitted",
                case.replace(
                    TB_004_CURRENT_BINDING_BOUNDARY,
                    "`EVD-2026-001`と`EVD-2026-003`でcurrent bindingを確認済みである。",
                    1,
                ),
            ),
            (
                "EP-2026-003 current Evidence overclaim",
                case.replace(
                    "Tenant binding metadataを確認予定の接点",
                    "Tenant binding metadataを確認済みの接点",
                    1,
                ),
            ),
            (
                "CTRL-2026-006 unstructured Evidence scope drift",
                case.replace(
                    "Workload identity binding snapshot、rotation手順Review記録、"
                    "offline機械的突合結果は未収集である | `GAP-2026-002`",
                    "Workload identity binding snapshot、利用観測、rotation実施結果は"
                    "未収集である | `GAP-2026-002`",
                    1,
                ),
            ),
            (
                "EP-2026-003 historical/current Evidence boundary omitted",
                case.replace(
                    EP_003_CURRENT_EVIDENCE_BOUNDARY,
                    "`EVD-2026-001`と`EVD-2026-002`でcurrent bindingを確認済みである。",
                    1,
                ),
            ),
            (
                "EDGE-2026-002 binding observation falls back to inventory",
                case.replace(
                    "post-remediation App registration export、Workload identity binding snapshot",
                    "post-remediation App registration export、identity inventory",
                    1,
                ),
            ),
            (
                "CTRL-2026-006 reverse Gap reference omitted",
                case.replace(
                    "`TH-2026-001` / `TH-2026-004` / `CTRL-2026-005` / `CTRL-2026-006`: "
                    "2026-07-25 scope縮小`Passed`後のcurrent App registration export",
                    "`TH-2026-001` / `TH-2026-004` / `CTRL-2026-005`: "
                    "2026-07-25 scope縮小`Passed`後のcurrent App registration export",
                    1,
                ),
            ),
            (
                "historical/current scope boundary omitted",
                case.replace(
                    "`EVD-2026-001`は2026-07-20のhistorical scope Snapshotであり、"
                    "第1章`CTRL-2026-001`が2026-07-25にscope縮小`Passed`を記録した後の"
                    "current scopeは、post-remediation Snapshotを収集するまで`Unknown`としてDecisionへ渡す。",
                    "`EVD-2026-001`でcurrent scopeはConfirmedである。",
                    1,
                ),
            ),
            (
                "post-remediation EDGE-2026-002 assurance overclaim",
                case.replace(
                    "| `EREQ-2026-001` | Unknown |\n| `PATH-2026-001` | `EDGE-2026-003` |",
                    "| `EREQ-2026-001` | Confirmed |\n| `PATH-2026-001` | `EDGE-2026-003` |",
                    1,
                ),
            ),
            (
                "PATH-2026-001 temporal split omitted",
                case.replace(
                    "2026-07-20のhistorical Snapshotでは要件外scopeが確認されたが、2026-07-25のscope縮小`Passed`後のcurrent scopeはpost-remediation Snapshot未収集で`Unknown`である",
                    "要件外scopeがcurrent状態としてConfirmedである",
                    1,
                ),
            ),
            (
                "GAP-2026-002 omits post-remediation snapshot",
                case.replace(
                    "2026-07-25 scope縮小`Passed`後のcurrent App registration export、"
                    "Workload identity binding snapshot、Tenant binding差分、"
                    "rotation手順Review記録、scope matrixのoffline機械的突合結果が未収集である",
                    "scope matrix、Identity binding、rotation手順を確認する",
                    1,
                ),
            ),
            (
                "EREQ-2026-001 invents post-remediation evidence",
                case.replace(
                    "New post-remediation result: current-scope snapshot、"
                    "Workload identity binding snapshot、Tenant binding差分、"
                    "rotation手順Review記録、offline機械的突合結果、"
                    "新Evidence ID付き・source Evidence IDを記録した"
                    "Workload-only binding check結果、"
                    "新Evidence ID付き・source Evidence IDを記録した"
                    "Rotation-management check結果、"
                    "新Evidence ID付きReviewer sign-offは未収集"
                    "（承認後にそれぞれ新Evidence IDを割り当てる）",
                    "New post-remediation result: current-scope snapshotは収集済み",
                    1,
                ),
            ),
            (
                "EREQ-2026-001 omits Tenant binding evidence",
                case.replace(
                    "Workload identity binding snapshot、Tenant binding差分、"
                    "rotation手順Review記録、source Evidence IDを記録した"
                    "Workload-only binding check結果、source Evidence IDを記録した"
                    "Rotation-management check結果、Reviewer sign-off | "
                    "実Tokenを取得しない。",
                    "Workload identity binding snapshot、rotation手順Review記録、"
                    "source Evidence IDを記録したWorkload-only binding check結果、"
                    "source Evidence IDを記録したRotation-management check結果、"
                    "Reviewer sign-off | "
                    "実Tokenを取得しない。",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-004 omits Tenant binding evidence",
                case.replace(
                    "Workload identity binding snapshot、Tenant binding snapshot、"
                    "rotation手順Review記録、Tenant binding差分",
                    "Workload identity binding snapshot、rotation手順Review記録",
                    1,
                ),
            ),
            (
                "REA-TM-2026-001 omits Tenant binding evidence",
                case.replace(
                    "App registration export、scope matrix、Tenant binding差分、"
                    "Workload identity binding snapshot",
                    "App registration export、scope matrix、Workload identity binding snapshot",
                    1,
                ),
            ),
            (
                "CTRL-2026-007 composite assurance overclaim",
                case.replace(
                    "| SOC | Documented | `EVD-2026-003` | `EVD-2026-003`はAdmin consent Eventだけを観測する。",
                    "| SOC | Observed | `EVD-2026-003` | `EVD-2026-003`はAdmin consent Eventだけを観測する。",
                    1,
                ),
            ),
            (
                "CTRL-2026-007 composite statement narrows to consent only",
                case.replace(
                    "Admin consentとApp identity lifecycle EventのAudit coverageを維持する",
                    "Admin consent EventのAudit coverageを維持する",
                    1,
                ),
            ),
            (
                "CTRL-2026-007 invents lifecycle observation",
                case.replace(
                    "App identity lifecycle EventのCoverageとRule test結果は未収集であり、複合Control全体の挙動は未観測である",
                    "App identity lifecycle EventのCoverageもEVD-2026-003で観測済みである",
                    1,
                ),
            ),
            (
                "EREQ-2026-002 omits lifecycle evidence class",
                case.replace(
                    "合成同意Event、合成App identity lifecycle Event、Audit export、両Event classのRule test結果",
                    "合成同意Event、Audit export、Rule test結果",
                    1,
                ),
            ),
            (
                "REA-TM-2026-002 closes on consent-only evidence",
                case.replace(
                    "新Authorization Record / RoE承認後にのみ両Event classの合成Rule testを再実施し、"
                    "Detection test結果に新Evidence IDを割り当てる。両Event classのEvidence",
                    "Admin consent Eventだけの合成Rule testを再実施し、Detection test結果に"
                    "新Evidence IDを割り当てる。Admin consent EventのEvidence",
                    1,
                ),
            ),
            (
                "lab safety Control reuses inherited API Telemetry ID",
                case.replace(
                    "| `CTRL-2026-008` | `ASSET-2026-003`, `TB-2026-006`",
                    "| `CTRL-2026-004` | `ASSET-2026-003`, `TB-2026-006`",
                    1,
                ),
            ),
            (
                "Control Handoff consumer omitted",
                case.replace(
                    "`CTRL-2026-005` / `CTRL-2026-006` / `CTRL-2026-007` / `CTRL-2026-008` / `CTRL-2026-009`、`GAP-2026-001`〜`004`",
                    "`GAP-2026-001`〜`004`",
                    1,
                ),
            ),
            (
                "TH-2026-001 inherited proposition drift",
                case.replace(
                    INHERITED_TH_001_CASE_PROPOSITION,
                    SUMMARY_TH_004_PROPOSITION,
                    1,
                ),
            ),
            (
                "TH-2026-001 inherited precondition drift",
                case.replace(
                    INHERITED_TH_001_CASE_PRECONDITIONS,
                    "2026-07-25 remediation後のcurrent scopeとWorkload identity bindingが未確認である",
                    1,
                ),
            ),
            (
                "TH-2026-001 inherited impact drift",
                case.replace(
                    "顧客Dataの閲覧・変更可能性",
                    "合成Dataの同期状態と業務判断への影響が拡大する",
                    1,
                ),
            ),
            (
                "TH-2026-002 inherited proposition overwritten by refinement",
                case.replace(
                    INHERITED_TH_002_PROPOSITION,
                    LIFECYCLE_TH_005_PROPOSITION,
                    1,
                ),
            ),
            (
                "TH-2026-002 inherited precondition drift",
                case.replace(
                    INHERITED_TH_002_PRECONDITIONS,
                    LIFECYCLE_TH_005_PRECONDITIONS,
                    1,
                ),
            ),
            (
                "TH-2026-002 inherited impact drift",
                case.replace(
                    INHERITED_TH_002_IMPACT,
                    LIFECYCLE_TH_005_IMPACT,
                    1,
                ),
            ),
            (
                "TH-2026-002 inherited status drift",
                case.replace(
                    f"{INHERITED_TH_002_ALTERNATIVE} | High | Partially Supported |",
                    f"{INHERITED_TH_002_ALTERNATIVE} | High | Supported |",
                    1,
                ),
            ),
            (
                "fresh TH-2026-005 definition duplicated",
                case.replace(
                    "| `TH-2026-005` | `DR-2026-001` |",
                    "| `TH-2026-004` | `DR-2026-001` |",
                    1,
                ),
            ),
            (
                "TH-2026-005 lifecycle proposition drift",
                case.replace(
                    LIFECYCLE_TH_005_PROPOSITION,
                    INHERITED_TH_002_PROPOSITION,
                    1,
                ),
            ),
            (
                "TH-2026-005 relation drift",
                case.replace(
                    LIFECYCLE_TH_005_RELATIONS,
                    "`TB-2026-001`, `TB-2026-003`, `FLOW-2026-004`, "
                    "`FLOW-2026-005`, `EXP-2026-002`",
                    1,
                ),
            ),
            (
                "PATH-2026-002 falls back from refinement to inherited ID",
                case.replace(
                    "| `PATH-2026-002` | `TH-2026-002`, `TH-2026-003`, `TH-2026-005`, `TH-2026-006` |",
                    "| `PATH-2026-002` | `TH-2026-002`, `TH-2026-003`, `TH-2026-006` |",
                    1,
                ),
            ),
            (
                "EREQ-2026-002 omits lifecycle refinement consumer",
                case.replace(
                    "| `EREQ-2026-002` | 同意EventとApp identity lifecycle Eventの監査Coverageは十分か | "
                    "`TH-2026-002`, `TH-2026-005`, `CTRL-2026-007`, `GAP-2026-003` |",
                    "| `EREQ-2026-002` | 同意EventとApp identity lifecycle Eventの監査Coverageは十分か | "
                    "`TH-2026-002`, `CTRL-2026-007`, `GAP-2026-003` |",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-005 falls back to inherited consent hypothesis",
                case.replace(
                    "| `ACT-TM-2026-005` | `TH-2026-005`, `CTRL-2026-007`, `GAP-2026-003` |",
                    "| `ACT-TM-2026-005` | `TH-2026-002`, `CTRL-2026-007`, `GAP-2026-003` |",
                    1,
                ),
            ),
            (
                "TH-2026-002/005 reader allocation drift",
                case.replace(
                    "| Refinement only | `ACT-TM-2026-005` |",
                    "| Refinement only | `ACT-TM-2026-002` |",
                    1,
                ),
            ),
            (
                "TH-2026-003 inherited proposition drift",
                case.replace(
                    INHERITED_TH_003_PROPOSITION,
                    OPPORTUNITY_TH_006_PROPOSITION,
                    1,
                ),
            ),
            (
                "TH-2026-003 inherited precondition drift",
                case.replace(
                    INHERITED_TH_003_PRECONDITIONS,
                    OPPORTUNITY_TH_006_PRECONDITIONS,
                    1,
                ),
            ),
            (
                "TH-2026-003 inherited impact drift",
                case.replace(
                    INHERITED_TH_003_IMPACT,
                    OPPORTUNITY_TH_006_IMPACT,
                    1,
                ),
            ),
            (
                "TH-2026-003 inherited Asset set drift",
                case.replace(
                    f"| `TH-2026-003` | `DR-2026-001` | {INHERITED_TH_003_ASSETS} |",
                    "| `TH-2026-003` | `DR-2026-001` | `ASSET-2026-001`, "
                    "`ASSET-2026-003`, `ASSET-2026-006` |",
                    1,
                ),
            ),
            (
                "TH-2026-003 inherited Boundary set drift",
                case.replace(
                    f"{INHERITED_TH_003_ASSETS} | {INHERITED_TH_003_RELATIONS} | "
                    f"{INHERITED_TH_003_PROPOSITION}",
                    f"{INHERITED_TH_003_ASSETS} | `TB-2026-002`, `TB-2026-003`, "
                    f"`TB-2026-008` | {INHERITED_TH_003_PROPOSITION}",
                    1,
                ),
            ),
            (
                "fresh TH-2026-006 definition duplicated",
                case.replace(
                    "| `TH-2026-006` | `DR-2026-001` |",
                    "| `TH-2026-003` | `DR-2026-001` |",
                    1,
                ),
            ),
            (
                "TH-2026-006 opportunity proposition falls back to occurrence",
                case.replace(
                    OPPORTUNITY_TH_006_PROPOSITION,
                    INHERITED_TH_003_PROPOSITION,
                    1,
                ),
            ),
            (
                "TH-2026-006 precondition drift",
                case.replace(
                    OPPORTUNITY_TH_006_PRECONDITIONS,
                    INHERITED_TH_003_PRECONDITIONS,
                    1,
                ),
            ),
            (
                "TH-2026-006 impact drift",
                case.replace(
                    OPPORTUNITY_TH_006_IMPACT,
                    INHERITED_TH_003_IMPACT,
                    1,
                ),
            ),
            (
                "PATH-2026-002 drops opportunity refinement",
                case.replace(
                    "| `PATH-2026-002` | `TH-2026-002`, `TH-2026-003`, `TH-2026-005`, `TH-2026-006` |",
                    "| `PATH-2026-002` | `TH-2026-002`, `TH-2026-003`, `TH-2026-005` |",
                    1,
                ),
            ),
            (
                "CTRL-2026-009 falls back to inherited occurrence",
                case.replace(
                    "`ASSET-2026-006`, `TB-2026-007`, `TH-2026-006`, `PATH-2026-002`",
                    "`ASSET-2026-006`, `TB-2026-007`, `TH-2026-003`, `PATH-2026-002`",
                    1,
                ),
            ),
            (
                "ASM-2026-002 falls back to inherited occurrence",
                case.replace(
                    "`TH-2026-004`, `TH-2026-006`, `EREQ-2026-003`",
                    "`TH-2026-003`, `TH-2026-004`, `EREQ-2026-003`",
                    1,
                ),
            ),
            (
                "ASM-2026-003 drops opportunity refinement",
                case.replace(
                    "`TH-2026-003`, `TH-2026-006`, `EREQ-2026-003`, `REA-TM-2026-002`",
                    "`TH-2026-003`, `EREQ-2026-003`, `REA-TM-2026-002`",
                    1,
                ),
            ),
            (
                "GAP-2026-001 falls back to inherited occurrence",
                case.replace(
                    "`TH-2026-006` / `CTRL-2026-009`: API利用Telemetryのresource / operation粒度が不足する",
                    "`TH-2026-003` / `CTRL-2026-009`: API利用Telemetryのresource / operation粒度が不足する",
                    1,
                ),
            ),
            (
                "GAP-2026-003 drops opportunity refinement",
                case.replace(
                    "`TH-2026-002` / `TH-2026-003` / `TH-2026-005` / `TH-2026-006` / `CTRL-2026-007`",
                    "`TH-2026-002` / `TH-2026-003` / `TH-2026-005` / `CTRL-2026-007`",
                    1,
                ),
            ),
            (
                "EREQ-2026-003 drops opportunity refinement",
                case.replace(
                    "`TH-2026-001`, `TH-2026-003`, `TH-2026-004`, `TH-2026-006`, "
                    "`CTRL-2026-009`, `GAP-2026-001`, `GAP-2026-003`",
                    "`TH-2026-001`, `TH-2026-003`, `TH-2026-004`, `CTRL-2026-009`, "
                    "`GAP-2026-001`, `GAP-2026-003`",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-003 falls back to inherited occurrence",
                case.replace(
                    "| `ACT-TM-2026-003` | `TH-2026-006`, `CTRL-2026-009`, `GAP-2026-001` |",
                    "| `ACT-TM-2026-003` | `TH-2026-003`, `CTRL-2026-009`, `GAP-2026-001` |",
                    1,
                ),
            ),
            (
                "REA-TM-2026-002 drops opportunity refinement",
                case.replace(
                    "| `REA-TM-2026-002` | Rule導入、Field追加、retention変更 | "
                    "`TH-2026-002`, `TH-2026-003`, `TH-2026-005`, `TH-2026-006`, "
                    "`CTRL-2026-007`, `CTRL-2026-009` |",
                    "| `REA-TM-2026-002` | Rule導入、Field追加、retention変更 | "
                    "`TH-2026-002`, `TH-2026-003`, `TH-2026-005`, "
                    "`CTRL-2026-007`, `CTRL-2026-009` |",
                    1,
                ),
            ),
            (
                "TH-2026-003/006 reader allocation drift",
                case.replace(
                    "| Refinement only | `CTRL-2026-009`, `ASM-2026-002`, "
                    "`GAP-2026-001`, `ACT-TM-2026-003` |",
                    "| Refinement only | `CTRL-2026-009`, `ASM-2026-002`, "
                    "`GAP-2026-001` |",
                    1,
                ),
            ),
            (
                "TH-2026-003/006 Decision handoff conflation",
                case.replace(
                    "発生有無を問う`TH-2026-003`と、機会条件およびsummary-only境界までの"
                    "影響範囲を問う`TH-2026-006`",
                    "発生有無と機会条件を問う`TH-2026-003`",
                    1,
                ),
            ),
            (
                "Chapter 5 handoff omits TH-2026-006",
                case.replace(
                    "`TH-2026-001`〜`006`の成立条件、Flow、Boundary、Exposure、観測点",
                    "`TH-2026-001`〜`005`の成立条件、Flow、Boundary、Exposure、観測点",
                    1,
                ),
            ),
            (
                "TB-2026-002 inherited endpoint drift",
                case.replace(
                    "OAuth app → 顧客Data API",
                    "OAuth app component → invoice-sync-manifestのsummary Data面",
                    1,
                ),
            ),
            (
                "TB-2026-001 inherited endpoint drift",
                case.replace(
                    "業務SaaS → Identity control plane",
                    "業務要件とscope承認 → Identity control planeのApp設定",
                    1,
                ),
            ),
            (
                "TB-2026-001 inherited crossing context drift",
                case.replace(
                    "| OAuth 2.0 app identity | Admin consent、scope review | 過大権限または不正な同意 |",
                    "| scope追加または例外承認が必要 | Admin consent、scope review | 過大権限または不正な同意 |",
                    1,
                ),
            ),
            (
                "fresh TB-2026-009 collapsed into inherited TB-2026-001",
                case.replace(
                    "| `TB-2026-009` | Administrative Control |",
                    "| `TB-2026-001` | Administrative Control |",
                    1,
                ),
            ),
            (
                "TB-2026-009 trust-authority meaning drift",
                case.replace(
                    "業務上の要件判断が管理者同意へ変換される",
                    "OAuth app identityが同意へ入る",
                    1,
                ),
            ),
            (
                "FLOW-2026-001 reuses inherited boundary",
                case.replace(
                    "Business approverとPlatform adminの二者Review | `TB-2026-009` | Internal |",
                    "Business approverとPlatform adminの二者Review | `TB-2026-001` | Internal |",
                    1,
                ),
            ),
            (
                "MISUSE-2026-001 reuses inherited boundary",
                case.replace(
                    "`ASSET-2026-004`, `ASSET-2026-005` | `TB-2026-009` | 要件表と実設定の差分が残る",
                    "`ASSET-2026-004`, `ASSET-2026-005` | `TB-2026-001` | 要件表と実設定の差分が残る",
                    1,
                ),
            ),
            (
                "EDGE-2026-001 reuses inherited boundary",
                case.replace(
                    "historical Snapshotで確認された | `TB-2026-009` | `ASSET-2026-005` / historical broad-scope snapshot",
                    "historical Snapshotで確認された | `TB-2026-001` | `ASSET-2026-005` / historical broad-scope snapshot",
                    1,
                ),
            ),
            (
                "CTRL-2026-005 reuses inherited boundary",
                case.replace(
                    "`ASSET-2026-004`, `ASSET-2026-005`, `TB-2026-009`, `TH-2026-001`",
                    "`ASSET-2026-004`, `ASSET-2026-005`, `TB-2026-001`, `TH-2026-001`",
                    1,
                ),
            ),
            (
                "TB-2026-006 evidence-state overclaim",
                case.replace(
                    "| Scope外Serviceへの到達 | Assumed | `EVD-AUTH-2026-001`, `SYNTH-REV-TM-SAFE-001` |",
                    "| Scope外Serviceへの到達 | Confirmed | `EVD-AUTH-2026-001`, `SYNTH-REV-TM-SAFE-001` |",
                    1,
                ),
            ),
            (
                "FLOW-2026-003 summary-boundary reference drift",
                case.replace(
                    "`TB-2026-008`, `TB-2026-006`",
                    "`TB-2026-002`, `TB-2026-006`",
                    1,
                ),
            ),
            (
                "EXP-2026-003 summary-boundary reference drift",
                case.replace(
                    "`TB-2026-008`, `TB-2026-005`, `TB-2026-006`, `FLOW-2026-003`",
                    "`TB-2026-002`, `TB-2026-005`, `TB-2026-006`, `FLOW-2026-003`",
                    1,
                ),
            ),
            (
                "EP-2026-003 summary-boundary reference drift",
                case.replace(
                    "`TB-2026-008`, `TB-2026-005`, `TB-2026-006` | `AUTH-CASE-2026-001`",
                    "`TB-2026-002`, `TB-2026-005`, `TB-2026-006` | `AUTH-CASE-2026-001`",
                    1,
                ),
            ),
            (
                "EDGE-2026-003 summary-boundary reference drift",
                case.replace(
                    "runtime sessionがsummary-only制約と一致しない | `TB-2026-008` |",
                    "runtime sessionがsummary-only制約と一致しない | `TB-2026-002` |",
                    1,
                ),
            ),
            (
                "TH-2026-004 summary-boundary reference drift",
                case.replace(
                    "`TB-2026-004`, `TB-2026-008`, `TB-2026-009`, `FLOW-2026-001`",
                    "`TB-2026-004`, `TB-2026-002`, `TB-2026-009`, `FLOW-2026-001`",
                    1,
                ),
            ),
            (
                "TH-2026-004 related-asset drift",
                case.replace(
                    "`ASSET-2026-001`, `ASSET-2026-005`, `ASSET-2026-006`, `ASSET-2026-007` | `TB-2026-004`, `TB-2026-008`, `TB-2026-009`",
                    "`ASSET-2026-001`, `ASSET-2026-005`, `ASSET-2026-006` | `TB-2026-004`, `TB-2026-008`, `TB-2026-009`",
                    1,
                ),
            ),
            (
                "TH-2026-004 evidence-requirement drift",
                case.replace(
                    "合成Dataの同期状態と業務判断への影響が拡大する | `EREQ-2026-001`, `EREQ-2026-003` | post-remediation current scopeは必要最小権限で、historical broad scopeが解消済みかもしれない",
                    "合成Dataの同期状態と業務判断への影響が拡大する | `EREQ-2026-001` | post-remediation current scopeは必要最小権限で、historical broad scopeが解消済みかもしれない",
                    1,
                ),
            ),
            (
                "TH-2026-004 current-state assurance overclaim",
                case.replace(
                    "post-remediation current scopeは必要最小権限で、historical broad scopeが解消済みかもしれない | High | Inconclusive |",
                    "post-remediation current scopeは必要最小権限で、historical broad scopeが解消済みかもしれない | High | Supported |",
                    1,
                ),
            ),
            (
                "TH-2026-006 summary-boundary reference drift",
                case.replace(
                    OPPORTUNITY_TH_006_RELATIONS,
                    "`TB-2026-002`, `TB-2026-003`, `TB-2026-007`, `FLOW-2026-003`, "
                    "`FLOW-2026-004`, `FLOW-2026-005`, `EXP-2026-002`, `EXP-2026-003`",
                    1,
                ),
            ),
            (
                "PATH-2026-001 drops summary refinement hypothesis",
                case.replace(
                    "| `PATH-2026-001` | `TH-2026-001`, `TH-2026-004` |",
                    "| `PATH-2026-001` | `TH-2026-001` |",
                    1,
                ),
            ),
            (
                "EREQ-2026-001 drops summary refinement hypothesis",
                case.replace(
                    "| `EREQ-2026-001` | 2026-07-25 remediation後のcurrent scope、Workload identity binding、Tenant binding、rotation手順は業務要件と一致するか | "
                    "`TH-2026-001`, `TH-2026-004`, `CTRL-2026-005`, `CTRL-2026-006`, `GAP-2026-002` |",
                    "| `EREQ-2026-001` | 2026-07-25 remediation後のcurrent scope、Workload identity binding、Tenant binding、rotation手順は業務要件と一致するか | "
                    "`TH-2026-001`, `CTRL-2026-005`, `CTRL-2026-006`, `GAP-2026-002` |",
                    1,
                ),
            ),
            (
                "REA-TM-2026-001 drops summary refinement hypothesis",
                case.replace(
                    "| `REA-TM-2026-001` | scope、Identity binding、rotationまたは承認ticket変更 | "
                    "`TH-2026-001`, `TH-2026-004`, `CTRL-2026-005`, `CTRL-2026-006`, `GAP-2026-002` |",
                    "| `REA-TM-2026-001` | scope、Identity binding、rotationまたは承認ticket変更 | "
                    "`TH-2026-001`, `CTRL-2026-005`, `CTRL-2026-006`, `GAP-2026-002` |",
                    1,
                ),
            ),
            (
                "REA-TM-2026-001 workload-only pass threshold removed",
                case.replace(
                    "active bindingのHuman identityが0件で、すべてが承認済み"
                    "Workload identity、Owner、Tenant、scope matrixへ一致",
                    "binding snapshotが存在",
                    1,
                ),
            ),
            (
                "REA-TM-2026-001 workload failure misclassified as Passed",
                case.replace(
                    "不一致、分類不能または未収集は"
                    "`Failed / Inconclusive / Not collected`とする",
                    "不一致、分類不能または未収集も`Passed`とする",
                    1,
                ),
            ),
            (
                "REA-TM-2026-001 identity check results omitted from inputs",
                case.replace(
                    REA_TM_001_INPUTS_REQUIRED,
                    REA_TM_001_INPUTS_REQUIRED.replace(
                        "新Evidence ID付き・source Evidence IDを記録した"
                        "Workload-only binding check結果、新Evidence ID付き・"
                        "source Evidence IDを記録した"
                        "Rotation-management check結果、新Evidence ID付き"
                        "Reviewer sign-off、",
                        "",
                    ),
                    1,
                ),
            ),
            (
                "EREQ-2026-001 identity check producer evidence omitted",
                case.replace(
                    "rotation手順Review記録、source Evidence IDを記録した"
                    "Workload-only binding check結果、source Evidence IDを記録した"
                    "Rotation-management check結果、Reviewer sign-off",
                    "rotation手順Review記録",
                    1,
                ),
            ),
            (
                "REA-TM-2026-001 rotation-management pass threshold removed",
                case.replace(
                    "Owner、review interval / trigger、last review result、"
                    "next review date、exception / failure escalationがあり、"
                    "未管理または期限超過のactive bindingが0件",
                    "rotation手順Review記録が存在",
                    1,
                ),
            ),
            (
                "REA-TM-2026-001 rotation failure misclassified as Passed",
                case.replace(
                    "欠落、不合格または未収集は"
                    "`Failed / Inconclusive / Not collected`とする",
                    "欠落、不合格または未収集も`Passed`とする",
                    1,
                ),
            ),
            (
                "REA-TM-2026-001 positive gate weakened to either-or",
                case.replace(
                    "両checkが`Passed`で、対応する新Evidence IDと"
                    "Reviewer sign-offがそろう場合だけ",
                    "どちらかのcheckが`Passed`で、対応する新Evidence ID"
                    "またはReviewer sign-offがあれば",
                    1,
                ),
            ),
            (
                "REA-TM-2026-001 row accepts non-Passed identity checks",
                case.replace(
                    REA_TM_001_CLOSURE_CRITERIA,
                    REA_TM_001_CLOSURE_CRITERIA.replace(
                        "両方が`Passed`で",
                        "両方が`Passed`でなくても",
                    ),
                    1,
                ),
            ),
            (
                "REA-TM-2026-001 row weakens Evidence and sign-off to OR",
                case.replace(
                    REA_TM_001_CLOSURE_CRITERIA,
                    REA_TM_001_CLOSURE_CRITERIA.replace(
                        "新Evidence ID付き・source Evidence IDを記録した"
                        "各check結果と新Evidence ID付きReviewer sign-offが"
                        "そろう場合だけ",
                        "新Evidence ID付き・source Evidence IDを記録した"
                        "各check結果と新Evidence ID付きReviewer sign-offの"
                        "どちらかがある場合",
                    ),
                    1,
                ),
            ),
            (
                "REA-TM-2026-001 row drops only-if gate",
                case.replace(
                    REA_TM_001_CLOSURE_CRITERIA,
                    REA_TM_001_CLOSURE_CRITERIA.replace(
                        "そろう場合だけ",
                        "そろわなくても",
                    ),
                    1,
                ),
            ),
            (
                "REA-TM-2026-001 row drops non-Passed retention",
                case.replace(
                    REA_TM_001_CLOSURE_CRITERIA,
                    REA_TM_001_CLOSURE_CRITERIA.replace(
                        "どちらかが`Failed / Inconclusive / Not collected`なら"
                        "`CTRL-2026-006`を`Documented`に維持し、"
                        "`GAP-2026-002`を閉じない",
                        "非Passed結果でも`CTRL-2026-006`を`Observed`とする",
                    ),
                    1,
                ),
            ),
            (
                "REA-TM-2026-001 input drops new Evidence ID qualifier",
                case.replace(
                    REA_TM_001_INPUTS_REQUIRED,
                    REA_TM_001_INPUTS_REQUIRED.replace(
                        "新Evidence ID付き・source Evidence IDを記録した"
                        "Workload-only binding check結果",
                        "source Evidence IDを記録した"
                        "Workload-only binding check結果",
                    ),
                    1,
                ),
            ),
            (
                "ACT-TM-2026-004 identity result handoff omitted",
                case.replace(
                    "Platformはsource Evidence IDをWorkload-only binding check結果と"
                    "Rotation-management check結果へ記録し、Identity Assurance Reviewerは"
                    "有限閾値に対するresultとlimitationをsign-offする。両check結果と"
                    "Reviewer sign-offへ別々の新Evidence IDを割り当てて"
                    "`REA-TM-2026-001`へ供給する。",
                    "Platformはoffline機械的突合結果を保存する。",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-004 success drops check result new Evidence ID",
                case.replace(
                    "offline機械的突合結果、新Evidence ID付き・source Evidence IDを"
                    "記録したWorkload-only binding check結果、"
                    "新Evidence ID付き・source Evidence IDを記録した"
                    "Rotation-management check結果、新Evidence ID付き"
                    "Identity Assurance Reviewer sign-off、"
                    "`REA-TM-2026-001`への供給",
                    "offline機械的突合結果、source Evidence IDを記録した"
                    "Workload-only binding check結果、新Evidence ID付き・"
                    "source Evidence IDを記録したRotation-management check結果、"
                    "新Evidence ID付きIdentity Assurance Reviewer sign-off、"
                    "`REA-TM-2026-001`への供給",
                    1,
                ),
            ),
            (
                "REA-TM-2026-001 failed identity check overclaims Observed",
                case.replace(
                    "なら`CTRL-2026-006`を`Documented`に維持し、"
                    "`GAP-2026-002`を閉じない",
                    "でも`CTRL-2026-006`を`Observed`とする",
                ),
            ),
            (
                "Confirmed without Evidence",
                case.replace(
                    "| `ASSET-2026-006` | Data | `invoice-sync-manifest` | 実請求書本文を含まない合成の同期要約、状態、再送管理Data | Finance Data Owner | High | Confidential | Assumed | `EVD-2026-002` |",
                    "| `ASSET-2026-006` | Data | `invoice-sync-manifest` | 実請求書本文を含まない合成の同期要約、状態、再送管理Data | Finance Data Owner | High | Confidential | Confirmed | - |",
                    1,
                ),
            ),
            (
                "Attack Path operational marker",
                case.replace(
                    "業務要件を超えるscopeがhistorical Snapshotで確認された",
                    "command: synthetic-operation",
                    1,
                ),
            ),
            (
                "Path summary unsafe Safety note",
                case.replace(
                    "実Tokenを取得しない。実Dataを参照しない。設定差分と合成metadataだけで評価する。",
                    "実Tokenを取得して確認する。",
                    1,
                ),
            ),
            (
                "Review note unsafe external action",
                case.replace(
                    "Asset type、Boundary、Threat接続を確認",
                    "第三者の本番APIへ接続する。",
                    1,
                ),
            ),
            (
                "Threat Hypothesis unsafe credential handling",
                case.replace(
                    "業務要件を超えるscopeがsummary境界を越える影響へつながる可能性がある",
                    "実Tokenを取得して権限追加を確認する",
                    1,
                ),
            ),
            (
                "Threat Hypothesis Evidence needed unsafe external action",
                case.replace(
                    "| `EREQ-2026-003` | TelemetryとRetentionの制約により、未観測を未発生と判断できない | High | Inconclusive |",
                    "| `EREQ-2026-003`。第三者の本番システムへ接続する | TelemetryとRetentionの制約により、未観測を未発生と判断できない | High | Inconclusive |",
                    1,
                ),
            ),
            (
                "Control unsafe credential handling",
                case.replace(
                    "業務要件とscopeの対応表をReviewする",
                    "実Credentialを取得して監査する",
                    1,
                ),
            ),
            (
                "Exposure unsafe external action",
                case.replace("Isolated configuration surface", "第三者の本番APIへ接続する", 1),
            ),
            (
                "Entry Point unsafe external action",
                case.replace(
                    "合成App registrationとconsent objectのread-only Review接点",
                    "第三者の本番システムへ接続する",
                    1,
                ),
            ),
            (
                "Attack Path From Asset State unsafe external action",
                case.replace(
                    "| `ASSET-2026-004` / 2026-07-20 historical scope-review | 業務要件を超えるscopeがhistorical Snapshotで確認された |",
                    "| `ASSET-2026-004` / 第三者の本番システムへ接続する | 業務要件を超えるscopeがhistorical Snapshotで確認された |",
                    1,
                ),
            ),
            (
                "Attack Path To Asset State unsafe external action",
                case.replace(
                    "| `TB-2026-009` | `ASSET-2026-005` / historical broad-scope snapshot |",
                    "| `TB-2026-009` | `ASSET-2026-005` / 第三者の本番システムへ接続する |",
                    1,
                ),
            ),
            (
                "Collected Evidence unsafe collection condition",
                case.replace(
                    "第1章継承: App registration export; Observation `OBS-2026-001`; Validation `VAL-2026-001`; Authority / RoE `ROE-2026-001`; Integrity / hash SHA-256をEvidence manifestへ記録; Classification Internal",
                    "実Tokenを取得してEvidenceへ保存する",
                    1,
                ),
            ),
            (
                "inherited Evidence timestamp drift",
                case.replace(
                    "2026-07-20T13:20:00+09:00",
                    "2026-08-08T14:00:00+09:00",
                    1,
                ),
            ),
            (
                "inherited Evidence provenance drift",
                case.replace(
                    "第1章継承: 業務要件とAPI仕様のReview; Observation `OBS-2026-001`; Validation `VAL-2026-001`; Authority / RoE `ROE-2026-001`; Integrity / hash Review承認記録; Classification Internal",
                    "第4章で再作成した要件fixture",
                    1,
                ),
            ),
            (
                "invented Negative Finding timestamp",
                case.replace(
                    "原典にはstandaloneの`Collected at`がないため、時刻を創作せず、原典行をそのまま継承する。",
                    "原典にはstandaloneの`Collected at`がないが、2026-08-08T14:50:00+09:00として記録する。",
                    1,
                ),
            ),
            (
                "CTRL-2026-008 assurance overclaim",
                case.replace(
                    "| Lab Operator | Documented | `EVD-AUTH-2026-001`, `SYNTH-REV-TM-SAFE-001` |",
                    "| Lab Operator | Observed | `EVD-AUTH-2026-001`, `SYNTH-REV-TM-SAFE-001` |",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-001 bypasses reauthorization",
                case.replace(
                    "2026-07-25 remediation後のcurrent scope Snapshot収集計画と要求、App permissionの必要最小scope案、scope matrix更新案を作成する。exportの取得と実設定変更は新Authorization Record / RoE承認後の別工程とする",
                    "App permissionを必要最小限へ縮小し、scope matrixとの差分をゼロにする",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-001 claims export collection instead of request completion",
                case.replace(
                    "post-remediation App registration export収集要求ticket、収集計画",
                    "post-remediation App registration export収集済み",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-002 bypasses renewed Authorization and RoE",
                case.replace(
                    "Phase Bでは対象・method・time windowの承認と`ACT-TM-2026-006` "
                    "Phase B-entryの新Evidence ID付き署名済みpreflight report / default-deny結果の"
                    "成功を開始条件とし、no-outboundの合成LabでAdmin consent change Eventの"
                    "合成Rule testを実行",
                    "Phase Bでは直ちにno-outboundの合成LabでAdmin consent change Eventの"
                    "合成Rule testを実行",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-005 bypasses renewed Authorization and RoE",
                case.replace(
                    "Phase Bでは対象・method・time windowの承認と`ACT-TM-2026-006` "
                    "Phase B-entryの新Evidence ID付き署名済みpreflight report / default-deny結果の"
                    "成功を開始条件とし、no-outboundの合成LabでApp identity lifecycle Eventの"
                    "合成Rule testを実行",
                    "Phase Bでは直ちにno-outboundの合成LabでApp identity lifecycle Eventの"
                    "合成Rule testを実行",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-005 omits default-deny Phase B entry evidence",
                case.replace(
                    "Phase Bでは対象・method・time windowの承認と`ACT-TM-2026-006` "
                    "Phase B-entryの新Evidence ID付き署名済みpreflight report / default-deny結果の"
                    "成功を開始条件とし、no-outboundの合成LabでApp identity lifecycle Event",
                    "Phase Bでは対象・method・time windowの承認と`ACT-TM-2026-006` "
                    "Phase B-entryの新Evidence ID付き署名済みpreflight reportの成功を開始条件とし、"
                    "no-outboundの合成LabでApp identity lifecycle Event",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-005 omits signed preflight success evidence",
                case.replace(
                    "承認済みの新Authorization Record / RoE、`ACT-TM-2026-006` Phase B-entryの"
                    "新Evidence ID付き署名済みpreflight report / default-deny結果、新Evidence ID付き"
                    "App identity lifecycle Event Detection test結果",
                    "承認済みの新Authorization Record / RoE、新Evidence ID付きApp identity "
                    "lifecycle Event Detection test結果",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-005 lifecycle result omits new Evidence ID",
                case.replace(
                    "Detection test結果を収集して新Evidence IDを割り当て",
                    "Detection test結果を収集して",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-005 lifecycle result overclaims collection before execution",
                case.replace(
                    "Phase B / C未実施の間はApp identity lifecycle EventのDetection test結果とCleanup結果は未収集",
                    "Phase B / C実施前からApp identity lifecycle EventのDetection test結果とCleanup結果は収集済み",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-005 omits post-test Cleanup completion gate",
                case.replace(
                    "本ActionはApp identity lifecycle Event側だけを扱う。両Event classのRule test"
                    "終了または停止後は`ACT-TM-2026-006` Phase CのCleanup verificationを完了するまで"
                    "本Actionを完了扱いにしない。",
                    "本ActionはApp identity lifecycle Event側だけを扱う。",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-005 omits lifecycle event class",
                case.replace(
                    "no-outboundの合成LabでApp identity lifecycle Eventの合成Rule testを実行し",
                    "no-outboundの合成Labで合成Rule testを実行し",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-005 does not supply lifecycle result to reassessment",
                case.replace(
                    "review sign-offとともに`REA-TM-2026-002`へ供給する",
                    "review sign-offとともに保管する",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-005 Phase B omits coverage and retention handoff",
                case.replace(
                    "query version、Coverage、90日retention証跡、review sign-offとともに"
                    "`REA-TM-2026-002`へ供給する",
                    "query version、review sign-offとともに`REA-TM-2026-002`へ供給する",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-005 Phase B success omits coverage and retention evidence",
                case.replace(
                    "新Evidence ID付きApp identity lifecycle Event Detection test結果、query version、"
                    "Coverage表、retention record、review sign-off、Phase Cの新Evidence ID付き"
                    "Cleanup verification、`REA-TM-2026-002`への供給",
                    "新Evidence ID付きApp identity lifecycle Event Detection test結果、query version、"
                    "review sign-off、Phase Cの新Evidence ID付きCleanup verification、"
                    "`REA-TM-2026-002`への供給",
                    1,
                ),
            ),
            (
                "EREQ-2026-002 permits pre-authorization Rule test",
                case.replace(
                    "無害化summaryを超える追加Data exportを要求しない。新Authorization Record / RoE承認前にRule testを再実施しない。",
                    "無害化summaryを超える追加Data exportを要求しない。",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-003 bypasses change authorization",
                case.replace(
                    "Phase AではAPI利用Telemetryのresource / operation Field contract、合成sample summary、"
                    "change proposal、新Authorization Record / change approval申請を作成する。Phase Bでは"
                    "対象・method・time window・実施Ownerを新Authorization Record / change approvalで"
                    "承認した後に限り、Field実装とpost-change collectionを承認済み運用工程へhandoffする",
                    "API利用Telemetryにresource / operation粒度を直ちに追加する",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-003 post-change result omits new Evidence ID",
                case.replace(
                    "post-change telemetry resultを収集して新Evidence IDを割り当て",
                    "post-change telemetry resultを収集して",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-003 success omits post-change telemetry result",
                case.replace(
                    "実装記録、新Evidence ID付きpost-change API telemetry result、query / version、"
                    "resource / operation Coverage、retention note、review sign-off",
                    "実装記録、query / version、resource / operation Coverage、retention note、review sign-off",
                    1,
                ),
            ),
            (
                "EREQ-2026-003 invents collected post-change Evidence",
                case.replace(
                    "resource / operation Fieldの実装記録とpost-change telemetry resultは未収集"
                    "（承認済み運用工程後に新Evidence IDを割り当てる）",
                    "resource / operation Fieldの実装記録とpost-change telemetry resultは"
                    "EVD-2026-005として収集済み",
                    1,
                ),
            ),
            (
                "EREQ-2026-002 omits uncollected Rule-test result handoff",
                case.replace(
                    "Coverage result: `EVD-2026-003`（Admin consent Eventのみ）; App identity lifecycle EventのCoverageと両Event classのRule test結果は未収集（承認後に新Evidence IDを割り当てる）",
                    "`EVD-2026-003`, `EVD-AUTH-2026-001`",
                    1,
                ),
            ),
            (
                "EREQ-2026-002 counts Authorization provenance as coverage result",
                case.replace(
                    "Coverage result: `EVD-2026-003`（Admin consent Eventのみ）;",
                    "Coverage result: `EVD-2026-003`（Admin consent Eventのみ）, "
                    "`EVD-AUTH-2026-001`;",
                    1,
                ),
            ),
            (
                "Authorization provenance is rebound to EREQ-2026-002",
                case.replace(
                    "| `EVD-AUTH-2026-001` | - | 合成Tenantを対象とした設定Review承認 |",
                    "| `EVD-AUTH-2026-001` | `EREQ-2026-002` | 合成Tenantを対象とした設定Review承認 |",
                    1,
                ),
            ),
            (
                "Rule-test Authorization provenance overclaims authorization",
                case.replace(
                    RULE_TEST_AUTHORIZATION_PROVENANCE_BOUNDARY,
                    "`EVD-AUTH-2026-001`はRule testを承認し、`EREQ-2026-002`の"
                    "Resulting EvidenceとしてCoverageを証明する。",
                    1,
                ),
            ),
            (
                "Rule-test Authorization provenance boundary omitted",
                case.replace(f"{RULE_TEST_AUTHORIZATION_PROVENANCE_BOUNDARY}\n\n", "", 1),
            ),
            (
                "REA-TM-2026-002 omits Action result inputs",
                case.replace(
                    "Admin consent EventとApp identity lifecycle EventのAudit export、Rule test計画、"
                    "新Authorization Record / RoE、両Event classのDetection test結果、query version、"
                    "coverage表、retention note、Field contract、合成sample summary、change proposal、"
                    "Telemetry Field change approval、Field実装記録、新Evidence ID付きpost-change "
                    "API telemetry result、resource / operation Coverage、review sign-off",
                    "Audit export、Rule test計画、新Authorization Record / RoE、coverage表、retention note、Telemetry Field change approval",
                    1,
                ),
            ),
            (
                "REA-TM-2026-002 omits renewed authorization gate",
                case.replace(
                    "新Authorization Record / RoE承認後にのみ両Event classの合成Rule testを再実施し、"
                    "Detection test結果に新Evidence IDを割り当てる。両Event classのEvidenceで"
                    "`CTRL-2026-007`をValidatedとする。API telemetryは新Authorization Record / "
                    "change approval後の承認済み運用工程でのみ変更・収集し",
                    "両Event classのEvidenceで`CTRL-2026-007`をValidatedとする。API telemetryを変更・収集し",
                    1,
                ),
            ),
            (
                "REA-TM-2026-002 omits CTRL-2026-009 post-change closure threshold",
                case.replace(
                    "post-change Evidenceがrequired API Eventのresource / operation Field、Coverage、"
                    "retention、過剰収集なしを示す場合に限り`CTRL-2026-009`を承認scope内でValidatedとし"
                    "`GAP-2026-001`を閉じる",
                    "`CTRL-2026-009`をValidatedとし`GAP-2026-001`を閉じる",
                    1,
                ),
            ),
            (
                "REA-TM-2026-002 reuses Detection evidence for API telemetry closure",
                case.replace(
                    "`CTRL-2026-007`のEvidenceを`CTRL-2026-009`へ流用しない",
                    "`CTRL-2026-007`のEvidenceを`CTRL-2026-009`へ流用する",
                    1,
                ),
            ),
            (
                "CTRL-2026-008 orphaned from lab-safety Gap",
                case.replace(
                    "| `GAP-2026-004` | AUTH条件、Lab boundaryまたは実施Evidence変更 |",
                    "| `GAP-2026-003` | AUTH条件、Lab boundaryまたは実施Evidence変更 |",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-006 executes before authorization",
                case.replace(
                    "Phase B-entryでは対象・method・time windowを承認した後、"
                    "`ACT-TM-2026-002` / `ACT-TM-2026-005`のRule test開始前に署名済みpreflightと"
                    "default-deny検証を実行し",
                    "Phase B-entryでは直ちにRule test前のpreflightとdefault-deny検証を実行し",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-006 omits post-test Cleanup handoff",
                case.replace(
                    "Phase Cでは両Event classのRule test終了または停止直後にCleanup verificationを実行し、"
                    "新Evidence IDを割り当てて`REA-TM-2026-004`へ供給する。",
                    "Phase CではRule test終了後に記録を確認する。",
                    1,
                ),
            ),
            (
                "Lab sequence starts Event-class tests before Safety entry",
                case.replace(
                    "| 2. Event-class tests | `ACT-TM-2026-002` / `ACT-TM-2026-005` Phase B | "
                    "Sequence 1の両Evidenceが成功しentry-gate sign-offがある |",
                    "| 1. Event-class tests | `ACT-TM-2026-002` / `ACT-TM-2026-005` Phase B | "
                    "任意の開始判断 |",
                    1,
                ),
            ),
            (
                "EREQ-2026-001 is due before ACT-TM-2026-004 can supply current evidence",
                mutate_table_cell(
                    case,
                    EVIDENCE_REQUIREMENT_HEADER,
                    1,
                    1,
                    "Due date",
                    "2026-08-12",
                ),
            ),
            (
                "EREQ-2026-002 is due before both Rule-test suppliers complete",
                mutate_table_cell(
                    case,
                    EVIDENCE_REQUIREMENT_HEADER,
                    1,
                    2,
                    "Due date",
                    "2026-08-14",
                ),
            ),
            (
                "supplier schedule drops ACT-TM-2026-004 from EREQ-2026-001",
                mutate_table_cell(
                    case,
                    EVIDENCE_SUPPLIER_SCHEDULE_HEADER,
                    1,
                    1,
                    "Supplier Action IDs",
                    "`ACT-TM-2026-001`",
                ),
            ),
            (
                "supplier schedule drops ACT-TM-2026-003 from EREQ-2026-003",
                mutate_table_cell(
                    case,
                    EVIDENCE_SUPPLIER_SCHEDULE_HEADER,
                    1,
                    3,
                    "Supplier Action IDs",
                    "`ACT-TM-2026-002`, `ACT-TM-2026-005`",
                ),
            ),
            (
                "supplier schedule omits EREQ-2026-004",
                mutate_table_cell(
                    case,
                    EVIDENCE_SUPPLIER_SCHEDULE_HEADER,
                    1,
                    4,
                    "Evidence Requirement ID",
                    "`EREQ-2026-003`",
                ),
            ),
            (
                "supplier schedule records a stale latest completion",
                mutate_table_cell(
                    case,
                    EVIDENCE_SUPPLIER_SCHEDULE_HEADER,
                    1,
                    1,
                    "Latest supplier completion",
                    "2026-08-14",
                ),
            ),
            (
                "supplier Action due date is not ISO-8601",
                mutate_table_cell(
                    case,
                    ACTION_HEADER,
                    1,
                    4,
                    "Due date",
                    "2026-08-XX",
                ),
            ),
            (
                "GAP-2026-001 is due before its complete supplier set",
                mutate_table_cell(
                    case,
                    GAP_HEADER,
                    1,
                    1,
                    "Due date",
                    "2026-08-17",
                ),
            ),
            (
                "REA-TM-2026-001 is not strictly after evidence collection",
                mutate_table_cell(
                    case,
                    REASSESSMENT_HEADER,
                    1,
                    1,
                    "Scheduled date",
                    "2026-08-15",
                ),
            ),
            (
                "ACT-TM-2026-006 cleanup completion is scheduled before the coordinated sequence",
                mutate_table_cell(
                    case,
                    ACTION_HEADER,
                    1,
                    6,
                    "Due date",
                    "2026-08-17",
                ),
            ),
            (
                "EREQ-2026-004 remains due on the reassessment date",
                mutate_table_cell(
                    case,
                    EVIDENCE_REQUIREMENT_HEADER,
                    1,
                    4,
                    "Due date",
                    LAB_SEQUENCE_REASSESSMENT_DATE,
                ),
            ),
            (
                "REA-TM-2026-004 runs before cleanup completion evidence can close",
                mutate_table_cell(
                    case,
                    REASSESSMENT_HEADER,
                    1,
                    4,
                    "Scheduled date",
                    LAB_SEQUENCE_COMPLETION_DATE,
                ),
            ),
            (
                "REA-TM-2026-004 omits post-stop Cleanup closure",
                case.replace(
                    "終了または停止直後のCleanup verificationを含む全結果が収集された場合に限り",
                    "preflight結果が収集された場合に限り",
                    1,
                ),
            ),
            (
                "synthetic configuration reauthorization gate omitted",
                case.replace(
                    "- 合成TenantであってもApp permission、consent、Identity bindingなどの設定変更を行う場合。\n",
                    "",
                    1,
                ),
            ),
            (
                "Rule test reauthorization gate omitted",
                case.replace(
                    "- RoEのmethod / time windowを越えて合成Rule testを再実施する場合。\n",
                    "",
                    1,
                ),
            ),
            (
                "Telemetry change reauthorization gate omitted",
                case.replace(
                    "- Telemetryの収集設定またはProduction Pipelineを変更する場合。\n",
                    "",
                    1,
                ),
            ),
            (
                "Action source type drift",
                case.replace(
                    "| `ACT-TM-2026-004` | `TH-2026-001`, `TH-2026-004`, `CTRL-2026-005`, "
                    "`CTRL-2026-006`, `GAP-2026-002` |",
                    "| `ACT-TM-2026-004` | `TB-2026-005`, `MISUSE-2026-001` |",
                    1,
                ),
            ),
            (
                "Gap-to-Action reverse trace drift",
                case.replace(
                    "| `EREQ-2026-001` | `ACT-TM-2026-001`, `ACT-TM-2026-004` | `REA-TM-2026-001` |",
                    "| `EREQ-2026-001` | `ACT-TM-2026-001` | `REA-TM-2026-001` |",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-004 does not remediate its Gap",
                case.replace(
                    "Phase Aでは合成Tenant bindingのBoundary owner、停止条件、fallback判断、"
                    "rotation手順Review fieldをscope matrixへ構造化し、収集計画と"
                    "新Authorization Record / RoE申請を作成する。",
                    "合成Tenant bindingのBoundary owner、停止条件、fallback判断をscope matrixへ構造化し、live Tenantへ接続して機械的突合する",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-004 collection phase bypasses renewed authorization",
                case.replace(
                    "Phase Bでは対象・method・time windowを新Authorization Record / RoEで"
                    "承認した後に限り",
                    "Phase Bでは直ちに",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-004 collection phase omits new Evidence IDs",
                case.replace(
                    "rotation手順Review記録を収集し、新Evidence IDを割り当てて",
                    "rotation手順Review記録を収集して",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-004 success overclaims unexecuted collection phase",
                case.replace("Phase B未実施の間は未収集", "Phase BのEvidenceは収集済み", 1),
            ),
            (
                "ACT-TM-2026-004 does not supply reassessment approval ticket",
                case.replace(
                    "Phase B: approval ticket、承認済みの新Authorization Record / RoE",
                    "Phase B: 承認済みの新Authorization Record / RoE",
                    1,
                ),
            ),
            (
                "RoE handoff omits ACT-TM-2026-004 collection authorization",
                case.replace(
                    "`ACT-TM-2026-003` / `ACT-TM-2026-004` / `ACT-TM-2026-005` / "
                    "`ACT-TM-2026-006`の"
                    "再Authorization依存",
                    "`ACT-TM-2026-003` / `ACT-TM-2026-005` / `ACT-TM-2026-006`の"
                    "再Authorization依存",
                    1,
                ),
            ),
            (
                "RoE handoff omits ACT-TM-2026-005 lifecycle execution authorization",
                case.replace(
                    "`ACT-TM-2026-004` / `ACT-TM-2026-005` / `ACT-TM-2026-006`の"
                    "再Authorization依存",
                    "`ACT-TM-2026-004` / `ACT-TM-2026-006`の再Authorization依存",
                    1,
                ),
            ),
            (
                "ACT-TM-2026-005 success evidence does not close its Gap",
                case.replace(
                    "Phase A: query approval template、lifecycle Rule test計画、新Authorization Record / "
                    "RoE申請ticket、Coverage表、retention record、deny例。Phase B: approval ticket、"
                    "承認済みの新Authorization Record / RoE、`ACT-TM-2026-006` Phase B-entryの"
                    "新Evidence ID付き署名済みpreflight report / default-deny結果、新Evidence ID付き"
                    "App identity lifecycle Event Detection test結果、query version、Coverage表、"
                    "retention record、review sign-off、Phase Cの新Evidence ID付きCleanup verification、"
                    "`REA-TM-2026-002`への供給。Phase B / C未実施の間はApp identity lifecycle Eventの"
                    "Detection test結果とCleanup結果は未収集",
                    "query approval template、deny例、review sign-off",
                    1,
                ),
            ),
            (
                "Flow Evidence status mixed with Knowledge state",
                case.replace("| Internal | Collected | 承認ticket、scope差分、例外理由 |", "| Internal | Confirmed | 承認ticket、scope差分、例外理由 |", 1),
            ),
            (
                "Evidence Requirement status mixed with Model status",
                case.replace("| SOC、Platform | 2026-08-18 | Required |", "| SOC、Platform | 2026-08-18 | Needs Evidence |", 1),
            ),
            (
                "Gap missing owner and due date",
                case.replace(
                    "| `GAP-2026-001` | `TH-2026-006` / `CTRL-2026-009`: API利用Telemetryのresource / operation粒度が不足する | `DR-2026-001`: 既往影響をsummary-only境界までしか限定できない | Platform | 2026-08-18 |",
                    "| `GAP-2026-001` | `TH-2026-006` / `CTRL-2026-009`: API利用Telemetryのresource / operation粒度が不足する | `DR-2026-001`: 既往影響をsummary-only境界までしか限定できない |  |  |",
                    1,
                ),
            ),
            (
                "Gap status mixed with Knowledge state",
                case.replace("| 2026-08-18 | Open | `EREQ-2026-003` |", "| 2026-08-18 | Confirmed | `EREQ-2026-003` |", 1),
            ),
            (
                "Collected Evidence status mixed with Knowledge state",
                case.replace(
                    "| Collected | Not recorded in inherited source | 2026-07-21T15:40:00+09:00 |",
                    "| Confirmed | Not recorded in inherited source | 2026-07-21T15:40:00+09:00 |",
                    1,
                ),
            ),
            (
                "Handoff semantic target drift",
                case.replace("| `HO-TM-2026-012` | 第12章 Identity評価 |", "| `HO-TM-2026-012` | 第27章 AI評価 |", 1),
            ),
            (
                "Handoff interpretation canonical-table boundary omitted",
                case.replace(f"{HANDOFF_INTERPRETATION_BOUNDARY}\n\n", "", 1),
            ),
            (
                "Chapter 14 lab-safety Evidence handoff drift",
                case.replace(
                    "`EREQ-2026-001`〜`004`、特に`EREQ-2026-004`のpreflight / default-deny / Cleanup証拠、禁止操作、stop条件、fallback",
                    "`EREQ-2026-001`〜`003`、禁止操作、stop条件、fallback",
                    1,
                ),
            ),
            (
                "Chapter 15 lab-safety trace handoff drift",
                case.replace(
                    "`GAP-2026-001`〜`004`、`ACT-TM-2026-001`〜`006`、`REA-TM-2026-001`〜`004`",
                    "`GAP-2026-001`〜`003`、`ACT-TM-2026-001`〜`005`、`REA-TM-2026-001`〜`003`",
                    1,
                ),
            ),
            (
                "Evidence Requirement traceability count drift",
                case.replace(
                    "- [x] 4つのEvidence Requirementがある",
                    "- [x] 3つのEvidence Requirementがある",
                    1,
                ),
            ),
            (
                "Assumption and Gap traceability count drift",
                case.replace(
                    "- [x] 3つのAssumptionと4つのGapがある",
                    "- [x] 3つのAssumptionと3つのGapがある",
                    1,
                ),
            ),
        )
        for name, mutation in case_mutations:
            if mutation == case:
                error(f"negative Case mutation fixture did not match canonical text: {name}")
            elif not case_contract_errors(mutation, f"negative Case {name}"):
                error(f"negative regression accepted Chapter 4 Case mutation: {name}")
        for control_id in sorted(CHAPTER4_CONTROL_RELATIONS):
            collision = control_definition_collision_errors(
                (
                    (
                        "cases/foreign-control-definition.md",
                        "| Control ID | Statement |\n"
                        "|---|---|\n"
                        f"| `{control_id}` | unrelated definition |\n",
                    ),
                )
            )
            if not collision:
                error(
                    f"negative external-artifact Control collision was accepted: {control_id}"
                )
        for hypothesis_id in sorted(FRESH_CHAPTER4_HYPOTHESIS_IDS):
            collision = hypothesis_definition_collision_errors(
                (
                    (
                        "cases/foreign-hypothesis-definition.md",
                        "| Hypothesis ID | Statement |\n"
                        "|---|---|\n"
                        f"| `{hypothesis_id}` | unrelated definition |\n",
                    ),
                )
            )
            if not collision:
                error(
                    "negative external-artifact Hypothesis collision was accepted: "
                    f"{hypothesis_id}"
                )
        safety_matrix_negative_regressions(case, CASE, CASE_TABLE_OCCURRENCES)
        prose_surface_negative_regressions(
            case,
            CASE,
            (
                (
                    "Case ATX heading",
                    "# 第4章 合成記入例：請求書連携OAuthアプリのAsset / Boundary / Threat Model",
                ),
                (
                    "Decision-note list item",
                    "OWN boundary: Asset、Flow、Boundary、Threat Hypothesis、非OperationalなAttack Path、Evidence Requirement、Action、Reassessmentを`DR-2026-001`へ接続する。",
                ),
            ),
        )
        pipe_prefixed_prose_surface_regressions(
            case, CASE, case_contract_errors
        )
        liquid_surface_regressions(case, CASE, case_contract_errors)
        raw_html_surface_regressions(case, CASE, case_contract_errors)
        bare_angle_surface_regressions(case, CASE, case_contract_errors)
        angle_entity_surface_regressions(case, CASE, case_contract_errors)
        reference_link_label_surface_regressions(
            case, CASE, case_contract_errors
        )
        inline_link_label_surface_regressions(
            case, CASE, case_contract_errors
        )
        kramdown_underscore_emphasis_surface_regressions(
            case, CASE, case_contract_errors
        )
        kramdown_ial_surface_regressions(
            case, CASE, case_contract_errors
        )
        inline_code_comment_surface_regressions(case, CASE, case_contract_errors)
        markdown_title_comment_surface_regressions(
            case, CASE, case_contract_errors
        )
        multiline_inline_code_surface_regressions(
            case, CASE, case_contract_errors
        )
        fenced_surface_regressions(case, CASE, case_contract_errors)
        indented_code_surface_regressions(case, CASE, case_contract_errors)
        footnote_surface_regressions(case, CASE, case_contract_errors)

    changelog_lines = changelog.splitlines()
    added_line = next((line for line in changelog_lines if line.startswith("- ") and "ART-03" in line), "")
    source_line = next(
        (line for line in changelog_lines if line.startswith("- ") and "NIST CSF 2.0" in line),
        "",
    )
    changelog_mutations: list[tuple[str, str]] = []
    if added_line:
        changelog_mutations.append(
            ("missing Added reader impact", changelog.replace(added_line, "- 第4章を更新", 1))
        )
    else:
        error("negative CHANGELOG mutation cannot find Chapter 4 Added entry")
    if source_line:
        for marker in CHANGELOG_CH04_SOURCE_NAMES + (
            "Source Registry",
            "章対応",
            "確認日",
            "次回確認",
        ):
            changelog_mutations.append(
                (
                    f"missing Source impact {marker}",
                    changelog.replace(source_line, source_line.replace(marker, "omitted", 1), 1),
                )
            )
        no_limitation = re.sub(r"Framework mapping.*$", "Framework mappingを利用", source_line)
        changelog_mutations.append(
            ("missing Framework mapping limitation", changelog.replace(source_line, no_limitation, 1))
        )
    else:
        error("negative CHANGELOG mutation cannot find Chapter 4 Source impact entry")
    for name, mutation in changelog_mutations:
        if mutation == changelog:
            error(f"negative CHANGELOG mutation fixture did not change text: {name}")
        elif not changelog_contract_errors(mutation, f"negative {CHANGELOG} {name}"):
            error(f"negative regression accepted Chapter 4 CHANGELOG mutation: {name}")
    if source_line:
        equivalent_source = re.sub(
            r"Framework mapping.*$",
            "Framework mappingは実装、検証、完全性を保証しないことを記録",
            source_line,
        )
        equivalent_changelog = changelog.replace(source_line, equivalent_source, 1)
        equivalent_errors = changelog_contract_errors(equivalent_changelog, f"equivalent {CHANGELOG}")
        if equivalent_errors:
            error(
                "Chapter 4 CHANGELOG contract rejected a semantically equivalent limitation: "
                f"{equivalent_errors!r}"
            )

    source_mutation = deepcopy(sources)
    source_entry = next(
        (
            item
            for item in source_mutation.get("sources", [])
            if isinstance(item, dict) and item.get("id") == "SRC-OWASP-TM-001"
        ),
        None,
    )
    if source_entry is None:
        error("negative Source Registry mutation cannot find SRC-OWASP-TM-001")
    else:
        source_entry["notes"] = (
            "2026-08-08に公式Project pageを確認した。第4章では補助参照として用いる。"
        )
        if not source_contract_errors(chapter, source_mutation, note):
            error("negative Source Registry mutation accepted missing OWASP null-metadata rationale")

    pages = raw_registry.get("pages", [])
    target = next((item for item in pages if item.get("source") == CHAPTER), None)
    if target:
        mutations: list[tuple[str, dict]] = []
        mutation = deepcopy(raw_registry)
        mutation["schemaVersion"] = "0.0.0"
        mutations.append(("schema drift", mutation))
        for field, value in (("section", "additional"), ("order", 999)):
            mutation = deepcopy(raw_registry)
            next(item for item in mutation["pages"] if item.get("source") == CHAPTER)[field] = value
            mutations.append((f"{field} drift", mutation))
        mutation = deepcopy(raw_registry)
        mutation["pages"].append(deepcopy(target))
        mutations.append(("duplicate page", mutation))
        mutation = deepcopy(raw_registry)
        next(item for item in mutation["pages"] if item.get("source") == CHAPTER)["unexpectedKey"] = True
        mutations.append(("unknown key", mutation))
        mutation = deepcopy(raw_registry)
        next(item for item in mutation["pages"] if item.get("source") == CHAPTER)["destination"] = "../escape.md"
        mutations.append(("path traversal", mutation))
        mutation = deepcopy(raw_registry)
        next(item for item in mutation["pages"] if item.get("source") == CHAPTER)["destination"] = "assets/index.md"
        mutations.append(("reserved path", mutation))
        mutation = deepcopy(raw_registry)
        next(item for item in mutation["pages"] if item.get("source") == CHAPTER)["title"] = "第4章 Threat Model 改訂"
        mutations.append(("canonical title drift", mutation))
        mutation = deepcopy(raw_registry)
        del next(
            item for item in mutation["pages"] if item.get("source") == CHAPTER
        )["title"]
        mutations.append(("missing canonical title", mutation))
        for name, mutation in mutations:
            if not registry_rejected(mutation, f"negative site registry {name}"):
                error(f"site-pages negative mutation was accepted: {name}")

        # Exercise the generic parser directly.  The Chapter 4 exact-title
        # comparator would also reject these values and could otherwise mask
        # a parser/schema regression.
        for title_name, invalid_title in (
            ("spaces", "   "),
            ("tabs", "\t\t"),
            ("Unicode spaces", "\u3000\u00a0"),
            ("C0 separator whitespace", "\u001c\u001d\u001e\u001f"),
            ("NEXT LINE whitespace", "\u0085"),
            ("NUL Cc", "\u0000"),
            ("BELL Cc", "\u0007"),
            ("DELETE Cc", "\u007f"),
            ("APPLICATION PROGRAM COMMAND Cc", "\u009f"),
            ("mixed Cc", "Visible\u0007 title"),
            ("unpaired high surrogate Cs", "\ud800"),
            ("mixed unpaired high surrogate Cs", "Visible\ud800 title"),
            ("zero-width format controls", "\u200b\u2060"),
            ("variation selector Mark", "\ufe0f"),
            ("combining grapheme joiner Mark", "\u034f"),
            ("combining acute Mark", "\u0301"),
            ("Mongolian variation selector Mark", "\u180b"),
            ("BRAILLE PATTERN BLANK invisible base", "\u2800"),
            ("HANGUL CHOSEONG FILLER invisible base", "\u115f"),
            ("HANGUL FILLER invisible base", "\u3164"),
            ("HALFWIDTH HANGUL FILLER invisible base", "\uffa0"),
            ("raw HTML", "<span>Visible title</span>"),
        ):
            invalid_title_registry = {
                "schemaVersion": "1.1.0",
                "canonicalDirectories": [],
                "pages": [
                    {
                        "source": "cases/whitespace-title.md",
                        "destination": "cases/whitespace-title/index.md",
                        "section": "additional",
                        "order": 1,
                        "title": invalid_title,
                    }
                ],
                "directoryRoutes": {},
            }
            try:
                parse_registry_data(
                    invalid_title_registry,
                    f"negative Chapter 4 {title_name}-only page title",
                )
            except SitePageRegistryError:
                pass
            else:
                error(
                    f"generic registry parser accepted {title_name}-only page title"
                )

        for safe_index, safe_title in enumerate(SAFE_PAGE_TITLES, start=1):
            safe_title_registry = {
                "schemaVersion": "1.1.0",
                "canonicalDirectories": [],
                "pages": [
                    {
                        "source": f"cases/safe-title-{safe_index}.md",
                        "destination": f"cases/safe-title-{safe_index}/index.md",
                        "section": "additional",
                        "order": safe_index,
                        "title": safe_title,
                    }
                ],
                "directoryRoutes": {},
            }
            try:
                parse_registry_data(
                    safe_title_registry,
                    f"safe Chapter 4 page title {safe_index}",
                )
            except SitePageRegistryError as exc:
                error(
                    "generic registry parser rejected a safe base/Mark title: "
                    f"{safe_title!r}: {exc}"
                )
            try:
                safe_title.encode("utf-8", errors="strict").decode(
                    "utf-8", errors="strict"
                )
            except UnicodeError as exc:
                error(
                    "safe Chapter 4 page title did not round-trip as strict UTF-8: "
                    f"{safe_title!r}: {exc}"
                )

        # The generic registry parser owns title safety. Exercise every current
        # registry page dynamically so a future page cannot bypass that owner.
        for page_index, page in enumerate(pages):
            mutation = deepcopy(raw_registry)
            mutation["pages"][page_index]["title"] = UNSAFE_PAGE_TITLES[
                page_index % len(UNSAFE_PAGE_TITLES)
            ]
            if not registry_rejected(
                mutation,
                f"negative site registry published title coverage {page_index}",
            ):
                error(
                    "site-pages published title escaped shared Policy scan: "
                    f"pages[{page_index}] {page.get('source')!r}"
                )

        # Bind every required unsafe class to every Chapter 4 publication route.
        for source in sorted(EXPECTED_PAGE_TITLES):
            for unsafe_index, unsafe_title in enumerate(UNSAFE_PAGE_TITLES, start=1):
                mutation = deepcopy(raw_registry)
                page = next(
                    item for item in mutation["pages"] if item.get("source") == source
                )
                page["title"] = unsafe_title
                if not registry_rejected(
                    mutation,
                    f"negative Chapter 4 title {source} class {unsafe_index}",
                ):
                    error(
                        "Chapter 4 published title mutation escaped shared Policy: "
                        f"{source!r} / {unsafe_title!r}"
                    )

        safe_registry = {
            "pages": [
                {
                    "source": f"cases/safe-title-{index}.md",
                    "destination": f"cases/safe-title-{index}/index.md",
                    "title": safe_title,
                }
                for index, safe_title in enumerate(SAFE_PAGE_TITLES, start=1)
            ]
        }
        safe_findings = published_page_title_findings(
            safe_registry,
            "Chapter 4 safe published title fixtures",
        )
        if safe_findings:
            error(
                "shared Policy rejected safe published title fixtures: "
                f"{[format_finding(finding) for finding in safe_findings]!r}"
            )
    else:
        error("negative site registry mutation cannot find Chapter 4 page")


def main() -> int:
    chapter = read_text(CHAPTER)
    template = read_text(TEMPLATE)
    case = read_text(CASE)
    note = read_text(SOURCE_NOTE)
    changelog = read_text(CHANGELOG)
    raw_registry = load_json("site-pages.json")
    sources = load_json("references/sources.json")

    if CONTENT_SAFETY_POLICY_VERSION != EXPECTED_POLICY_VERSION:
        error(f"Content Safety Policy version {CONTENT_SAFETY_POLICY_VERSION!r} != {EXPECTED_POLICY_VERSION!r}")

    ERRORS.extend(chapter_contract_errors(chapter, CHAPTER))
    ERRORS.extend(template_contract_errors(template, TEMPLATE))
    ERRORS.extend(case_contract_errors(case, CASE))
    ERRORS.extend(fresh_control_definition_errors())
    ERRORS.extend(fresh_hypothesis_definition_errors())
    ERRORS.extend(source_contract_errors(chapter, sources, note))
    ERRORS.extend(publication_contract_errors())
    ERRORS.extend(changelog_contract_errors(changelog, CHANGELOG))

    try:
        registry = parse_registry_data(raw_registry)
    except SitePageRegistryError as exc:
        error(f"site-pages.json: invalid registry: {exc}")
        registry = {}
    ERRORS.extend(page_contract_errors(registry, "site-pages.json"))
    ERRORS.extend(page_title_contract_errors(registry, "site-pages.json"))

    baseline = read_text("references/reference-baseline.md")
    if baseline and sources and baseline != render_reference_baseline():
        error("references/reference-baseline.md: out of sync with references/sources.json")

    negative_regressions(chapter, template, case, raw_registry, sources, note, changelog)

    if ERRORS:
        for message in ERRORS:
            print(f"ERROR: {message}", file=sys.stderr)
        print(f"Chapter 4 contract failed with {len(ERRORS)} error(s).", file=sys.stderr)
        return 1
    print(
        "Chapter 4 contract passed: ART-03, synthetic Case, source registry, "
        "Policy 1.2.0 adapter, exact publication routes, and negative regressions are valid."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
