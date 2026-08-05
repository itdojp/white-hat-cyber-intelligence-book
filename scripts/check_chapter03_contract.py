#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.render_reference_baseline import (  # noqa: E402
    render as render_reference_baseline,
)
from scripts.sync_book_site import (  # noqa: E402
    SitePageRegistryError,
    parse_registry_data,
)
from scripts.sync_site_source import PAGES, rewrite_links  # noqa: E402

ERRORS: list[str] = []

EXPECTED_CHAPTER03_PAGES = {
    (
        "manuscript/03-capability-evidence.md",
        "chapters/chapter-03/index.md",
        "chapters",
        46,
        "第3章 能力を分解し、証拠で学習する",
    ),
    (
        "templates/capability-evidence-matrix.md",
        "templates/capability-evidence-matrix/index.md",
        "additional",
        234,
        "Capability Evidence Matrix",
    ),
    (
        "cases/ch03-capability-evidence-example.md",
        "cases/chapter-03-capability-evidence/index.md",
        "additional",
        236,
        "第3章 合成記入例：Capability Evidence Matrix",
    ),
    (
        "references/ch03-source-review-2026-08-05.md",
        "references/chapter-03-source-review/index.md",
        "additional",
        237,
        "第3章 Source Review Note：NICE Framework",
    ),
}

CORE_TRACE = """Work Role / Responsibility
→ Task
→ Knowledge / Skill
→ Practice Environment
→ Artifact Evidence
→ Review / Rubric
→ Gap / Learning Action
→ Reassessment"""

STATUS_SET = {
    "Planned",
    "In practice",
    "Evidence submitted",
    "Reviewed",
    "Gap identified",
    "Reassessment due",
    "Complete",
}

REVIEW_RESULT_SET = {
    "Meets",
    "Partially meets",
    "Does not meet",
    "Inconclusive",
}

CLAIM_RESULT_SET = {
    "Supported",
    "Partially supported",
    "Not supported",
    "Inconclusive",
}

ARTIFACT_RUBRIC_HEADER = (
    "| Rubric ID | Applies to | Meets | Partially meets | Does not meet | Inconclusive |"
)
CLAIM_RUBRIC_HEADER = (
    "| Rubric ID | Applies to | Supported | Partially supported | Not supported | Inconclusive |"
)
CLAIM_JUDGMENT_HEADER = (
    "| Claim ID | Scope | Conditions | Evidence set | Reviewer / Rubric | Result | "
    "Limitations | Expiry | Reassessment Trigger | Reassessment ID |"
)
REASSESSMENT_HEADER = (
    "| Reassessment ID | Scheduled date | Reassessment Trigger | Evidence to recollect | "
    "Task to revisit | Owner | Closure criteria | Status |"
)

EXPECTED_SOURCES = {
    "SRC-NICE-001": {
        "fields": {
            "title": "Workforce Framework for Cybersecurity (NICE Framework)",
            "status": "final",
            "version": "SP 800-181 Rev.1",
            "url": "https://csrc.nist.gov/pubs/sp/800/181/r1/final",
            "publishedAt": "2020-11-16",
            "checkedAt": "2026-08-05",
            "nextReviewAt": "2026-11-05",
            "reviewTriggers": ["NIST SP 800-181 revision or errata"],
            "chapters": [0, 1, 3],
        },
        "noteMarkers": (
            "Structural publication: NIST SP 800-181 Rev.1",
            "final, published 2020-11-16",
            "SRC-NICE-COMP-001",
            "common vocabulary and decomposition aid",
            "not as standalone proof of individual competence",
        ),
    },
    "SRC-NICE-COMP-001": {
        "fields": {
            "title": "NICE Framework Components v2.2.0",
            "status": "current",
            "version": "2.2.0",
            "url": "https://www.nist.gov/news-events/news/2026/04/nice-releases-nice-framework-components-v220",
            "publishedAt": "2026-04-28",
            "checkedAt": "2026-08-05",
            "nextReviewAt": "2026-11-05",
            "reviewTriggers": [
                "NICE Framework Components major or minor release",
                "Changes to Work Role, Competency Area, or TKS identifiers used by Chapter 3",
            ],
            "chapters": [3],
        },
        "noteMarkers": (
            "NICE Framework Components release v2.2.0",
            "released 2026-04-28",
            "Current Versions page displayed April 28, 2025",
            "2025 is treated as an apparent page typo",
            "OG-WRL-017",
            "NF-COM-006",
            "NF-COM-008",
            "common vocabulary and decomposition aid",
            "not as standalone proof of individual competence",
        ),
    },
}


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


def missing_tokens(text: str, tokens: tuple[str, ...]) -> list[str]:
    return [token for token in tokens if token not in text]


def require_tokens(relative: str, text: str, tokens: tuple[str, ...]) -> None:
    for token in missing_tokens(text, tokens):
        error(f"{relative}: missing required token {token!r}")


def source_ids(text: str) -> set[str]:
    return set(re.findall(r"\bSRC-[A-Z0-9-]+\b", text))


def chapter_body_and_references(text: str) -> tuple[str, str]:
    marker = "## 参考文献・Source Note ID"
    if marker not in text:
        return text, ""
    return tuple(text.split(marker, 1))  # type: ignore[return-value]


def chapter_contract_errors(text: str, label: str) -> list[str]:
    messages: list[str] = []
    required = (
        "# 第3章　能力を分解し、証拠で学習する",
        "## この章の位置付け",
        "## 本章の責任境界",
        "### OWN",
        "### BRIDGE",
        "### DELEGATE",
        "委譲先を読まなくても、本章の中心論旨と`ART-14`の作成手順は単独で成立する",
        "## 学習目標",
        "## 前提知識",
        "## 導入ケース",
        "ART-01 Learning Route Plan",
        "第1章で整理した業務機能",
        "第2章のAuthority / Scope / Safety / Disclosure",
        "LEARN-CASE-2026-003",
        CORE_TRACE,
        "複数のReview Resultから作る`Capability Judgment`はTraceを上書きせず",
        "F-03-01 Capability Evidence Trace",
        "**Taskは、実行する仕事である。**",
        "**Knowledgeは、Taskに必要な概念または情報である。**",
        "**Skillは、観測可能な行為を実行するCapacityである。**",
        "**Competency Areaは、NICE Componentsにおける関連する能力領域のGroupingであり、個人が有能であることの証明ではない。**",
        "**Work Roleは仕事のGroupingであり、Job titleでも個人でもない。**",
        "**Artifact Evidenceは、明示した条件で作成され、第三者がReviewできる出力である。**",
        "**Review Resultは、一つのArtifact Evidenceを宣言済みRubricで評価した結果である。**",
        "**Capability Judgmentは、複数のEvidence itemに支えられた限定的な結論である。**",
        "**Reassessmentは、時間、Scope、Source、Role、Technology、Rubricの変更によって起動する後続Reviewである。**",
        "NIST SP 800-181 Rev.1",
        "NICE Framework Components v2.2.0",
        "SRC-NICE-COMP-001",
        "NICEを次の用途に限定する",
        "identifierを一つ割り当てただけで個人の能力を証明する",
        "`NICE Components references`欄",
        "`Not mapped`と理由を残す",
        "v2.2.0; Work Role OG-WRL-017; local Task / K / S: Not mapped（当該Taskとの対応未確認）",
        "本章の合成Taskや学習者の能力を当該Work Roleへ対応付けない",
        "正本Practice packet `CAP-PACKET-2026-003-R1`",
        "T-03-01 Evidenceの四分類",
        "良いEvidence",
        "弱いEvidence",
        "危険なEvidence",
        "結論不能なEvidence",
        "Job title、Certification、CTF score、Tool count、Chapter completion",
        "本書固有の学習進行",
        "observe",
        "explain",
        "assess",
        "design",
        "lead",
        "NISTが定めた普遍的なLevel標準ではない",
        "Scope",
        "Conditions",
        "Reviewer",
        "Limitations",
        "Expiry",
        "Reassessment Trigger",
        "実Targetへの攻撃回数",
        "実Target操作が必要になる",
        "ART-14 Capability Evidence Matrix",
        "Planned / In practice / Evidence submitted / Reviewed / Gap identified / Reassessment due / Complete",
        "## 10. 評価基準",
        "## 11. よくある誤解",
        "## 章のまとめ",
        "## 次に学ぶこと",
        "## 参考文献・Source Note ID",
        "SRC-NICE-001",
        "https://itdojp.github.io/pentest-learning-book/",
        "https://itdojp.github.io/practical-auth-book/",
        "https://itdojp.github.io/it-infra-security-guide-book/",
    )
    for token in missing_tokens(text, required):
        messages.append(f"{label}: missing required token {token!r}")
    body, references = chapter_body_and_references(text)
    body_ids = source_ids(body)
    reference_ids = source_ids(references)
    expected_ids = {"SRC-NICE-001", "SRC-NICE-COMP-001"}
    if body_ids != expected_ids:
        messages.append(
            f"{label}: body source IDs {sorted(body_ids)} != {sorted(expected_ids)}"
        )
    if reference_ids != body_ids:
        messages.append(
            f"{label}: chapter-end source IDs {sorted(reference_ids)} "
            f"!= body {sorted(body_ids)}"
        )

    for forbidden in (
        "NISTが定めた普遍的なLevel標準である",
        "NICE identifierが個人の能力を証明する",
        "実Targetへの攻撃を学習証拠にする",
        "無許可の実Target操作をPracticeとする",
        "攻撃活動量が多いほど能力が高い",
        "この章のCapability Judgmentを採用判定に転用できる",
        "従業員をCapabilityで順位付けする",
        "Capability Judgmentを公開ランキングに使用できる",
    ):
        if forbidden in text:
            messages.append(f"{label}: unsafe or unsupported assertion {forbidden!r}")
    if re.search(r"https://github\.com/[^\s)]+/blob/main(?:/|\b)", text):
        messages.append(
            f"{label}: mutable GitHub blob/main URL must not be a delegated target"
        )
    return messages


def template_contract_errors(text: str, label: str) -> list[str]:
    required = (
        "# Capability Evidence Matrix",
        "Artifact ID | `ART-14`",
        "Matrix ID | `CAP-MATRIX-YYYY-NNN`",
        "Learner Profile ID | `SYNTH-LEARNER-NNN`",
        "Parent Artifact ID | `ART-01`",
        "Parent Plan ID | `LRP-YYYY-NNN`",
        "Relation | `refines` / `supersedes` / `independent`",
        "NICE Components baseline | `v2.2.0`",
        "Task ID / statement",
        "Knowledge reference",
        "Skill reference",
        "NICE Components references（optional）",
        "`Not mapped`と理由",
        "v2.2.0; Work Role OG-WRL-017; local Task / K / S: Not mapped（対応未確認）",
        "Practice ID",
        "Authority / Environment",
        "Artifact / Evidence ID",
        "Reviewer",
        "Rubric",
        "Result",
        "Gap",
        "Learning Action",
        "Due date",
        "Reassessment ID",
        "Planned / In practice / Evidence submitted / Reviewed / Gap identified / Reassessment due / Complete",
        "### 2.1 Rubric Definitions",
        "#### Artifact Evidence Rubric",
        ARTIFACT_RUBRIC_HEADER,
        "`RUBRIC-CAP-001` | `TASK-CAP-001` / `ART-EVD-CAP-001`",
        "#### Capability Claim Rubric",
        CLAIM_RUBRIC_HEADER,
        "`RUBRIC-CAP-CLAIM-001` | `CAP-CLAIM-YYYY-NNN`",
        "## 5. Review Result",
        "## 6. Bounded Capability Judgment",
        CLAIM_JUDGMENT_HEADER,
        REASSESSMENT_HEADER,
        "複数Evidence item",
        "Scope",
        "Conditions",
        "Limitations",
        "Expiry",
        "Reassessment Trigger",
        "## 8. Traceability Check",
        "人事評価、採用、昇進、報酬、資格認定、公開ランキングには使用しない",
        "実在Targetへの攻撃、実Credential、Token、Cookie、個人情報、従業員Data、顧客DataをEvidenceにしない",
    )
    messages = [
        f"{label}: missing required token {x!r}"
        for x in missing_tokens(text, required)
    ]
    for forbidden in (
        "このTemplateを採用判定と公開ランキングに使う",
        "このTemplateを従業員の順位付けに使う",
        "Capability Judgmentを報酬決定へ直接使用する",
    ):
        if forbidden in text:
            messages.append(f"{label}: prohibited HR or ranking use {forbidden!r}")
    if text.find("### 2.1 Rubric Definitions") > text.find("## 3. Practice and Evidence Trace"):
        messages.append(f"{label}: Rubric definitions must precede Practice/Evidence trace")
    return messages


def markdown_row_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def case_contract_errors(text: str, label: str) -> list[str]:
    messages: list[str] = []
    required = (
        "ART-14",
        "CAP-MATRIX-2026-003",
        "SYNTH-LEARNER-003",
        "Parent Artifact ID | `ART-01`",
        "Parent Plan ID | `LRP-2026-003`",
        "Relation | `refines`",
        "LEARN-CASE-2026-003",
        "NICE Components baseline | `v2.2.0`",
        "Practice packet | `CAP-PACKET-2026-003-R1`",
        "CAP-CLAIM-2026-003",
        "TASK-CAP-001",
        "TASK-CAP-002",
        "TASK-CAP-003",
        "KN-CAP-001",
        "KN-CAP-002",
        "KN-CAP-003",
        "SK-CAP-001",
        "SK-CAP-002",
        "SK-CAP-003",
        "PRACTICE-CAP-001",
        "PRACTICE-CAP-002",
        "PRACTICE-CAP-003",
        "ART-EVD-CAP-001",
        "ART-EVD-CAP-002",
        "ART-EVD-CAP-003",
        "RUBRIC-CAP-001",
        "RUBRIC-CAP-002",
        "RUBRIC-CAP-003",
        "RUBRIC-CAP-CLAIM-003",
        "REV-CAP-001",
        "REV-CAP-002",
        "REV-CAP-003",
        "REA-CAP-001",
        "REA-CAP-002",
        "REA-CAP-003",
        "Authorization Checklistを作り",
        "offline detection fixture",
        "Source評価済みの分析判断",
        "### 2.1 完全合成Practice packet",
        "第17章または第25章の読了、外部Network、別Datasetを前提にしない",
        "#### Minimum Authorization Checklist stub",
        "第2章の完全なTemplateを参照しなくても、四Gate、停止、Escalation、再承認のEvidenceを作成できる",
        "| Authority | 承認主体、実施主体、根拠、承認状態 |",
        "| Scope | 対象、対象外、Data、期間、許可Action |",
        "| Safety | 隔離、Rate / load制約、停止条件、Cleanup |",
        "| Disclosure | 連絡先、Evidence取扱い、報告先、開示境界 |",
        "| Stop / Escalation | 誰が、何を検出したら、誰へ引き渡すか |",
        "| Reauthorization | Target、Data、期間、手法、Owner変更時の再承認条件 |",
        "FIX-CAP-002-POS",
        "FIX-CAP-002-NEG",
        "FIX-CAP-002-BENIGN",
        "R1 detector contractは「`operation=admin_change`かつ`actor_authorized=false`かつ`required_fields=complete`なら`Alert`、それ以外は`No alert`」",
        "Observed in R1",
        "`FIX-CAP-002-POS` | `operation=admin_change`, `actor_authorized=false`, `required_fields=complete` | Alert | Alert",
        "`FIX-CAP-002-NEG` | `operation=admin_change`, `actor_authorized=true`, `required_fields=complete` | No alert | No alert",
        "`FIX-CAP-002-BENIGN` | `operation=view`, `actor_authorized=false`, `required_fields=complete` | No alert | No alert",
        "SN-CAP-003-A",
        "SN-CAP-003-B",
        "SN-CAP-003-C",
        "`SN-CAP-003-A` | 合成技術Cluster `CL-CAP-003`の同一特徴を報告 | 合成一次観測 | Group A",
        "`SN-CAP-003-B` | `SN-CAP-003-A`を要約して同じ特徴を報告 | derived-from `SN-CAP-003-A` | Group A",
        "`SN-CAP-003-C` | 反対仮説に整合する別特徴を報告 | 合成一次観測だが対象期間外 | Group B / scope mismatch",
        "R1 source-evaluation contract",
        "独立したin-scope Sourceが二系統未満なら`Inconclusive`",
        "#### R1 replay procedure",
        "Packet ID、Artifact版、Rubric、Reviewer、Result、Limitationsを`ART-14`へ記録する",
        "正本Practice packet `CAP-PACKET-2026-003-R1`",
        "#### Artifact Evidence Rubric",
        ARTIFACT_RUBRIC_HEADER,
        "#### Capability Claim Rubric",
        CLAIM_RUBRIC_HEADER,
        "三TaskがすべてMeetsで、宣言ScopeとLimitationsが矛盾しない",
        "一つ以上のTaskがDoes not meet、またはEvidence setが宣言Scopeを支持しない",
        "必須EvidenceまたはReview Resultが不足・矛盾し、限定結論も作れない",
        CLAIM_JUDGMENT_HEADER,
        REASSESSMENT_HEADER,
        "NICE Components references（optional）",
        "Not mapped。合成の横断Task",
        "Not mapped。学習用Task",
        "Not mapped。Components identifierへの対応を推測しない",
        "v2.2.0; Work Role OG-WRL-017; local Task / K / S: Not mapped（当該Taskとの対応未確認）",
        "本CaseのTaskやCapability Claimを`OG-WRL-017`へ対応付けない",
        "本節の最小Checklist stubでTarget、Data、期間変更のTriggerを書き直す",
        "Synthetic Safety Reviewer",
        "Synthetic Detection Reviewer",
        "Synthetic Analytic Reviewer",
        "Result | Partially supported",
        "Task 2のoffline detection fixtureをRubricどおり検証できる",
        "Task 1は一部条件を満たし、Task 3は結論不能",
        "Limitations",
        "Expiry | 2026-11-05T17:00:00+09:00",
        "Reassessment Trigger",
        "人物全体の能力",
        "実在する従業員、応募者、顧客、組織の人事評価ではない",
        "公開ランキング、採用、昇進、報酬、資格認定には使用しない",
        "実Target、実Credential、Token、Cookie、個人情報、従業員Data、顧客Dataを使用しない",
        "SYNTH-REV-CAP-TECH-001",
        "SYNTH-REV-CAP-SAFE-001",
        "SYNTH-REV-CAP-SOURCE-001",
        "SYNTH-REV-CAP-TRACE-001",
        "SYNTH-REV-CAP-DEC-001",
        "`LRP-2026-003`でrefine対象のLearning Route Plan instanceを特定できる",
    )
    for token in missing_tokens(text, required):
        messages.append(f"{label}: missing required token {token!r}")
    if re.search(r"(?:非)?Critical", text):
        messages.append(
            f"{label}: rubric must use explicit conditions instead of undefined Critical labels"
        )
    if text.count("CAP-PACKET-2026-003-R1") != 5:
        messages.append(
            f"{label}: authoritative Practice packet ID must occur exactly 5 times"
        )

    artifact_rubric_rows = [
        markdown_row_cells(line)
        for line in text.splitlines()
        if line.startswith("| `RUBRIC-CAP-")
        and not line.startswith("| `RUBRIC-CAP-CLAIM-")
    ]
    if len(artifact_rubric_rows) != 3:
        messages.append(f"{label}: expected exactly 3 Artifact Evidence rubric rows")
    artifact_rubrics: dict[str, str] = {}
    for cells in artifact_rubric_rows:
        if len(cells) != 6 or any(not cell for cell in cells[1:]):
            messages.append(
                f"{label}: Artifact Evidence rubric must define Applies to and all four results: {cells!r}"
            )
            continue
        rubric_id = cells[0].strip("`")
        if rubric_id in artifact_rubrics:
            messages.append(f"{label}: duplicate Artifact Evidence rubric ID {rubric_id}")
        artifact_rubrics[rubric_id] = cells[1]

    claim_rubric_rows = [
        markdown_row_cells(line)
        for line in text.splitlines()
        if line.startswith("| `RUBRIC-CAP-CLAIM-")
    ]
    if len(claim_rubric_rows) != 1:
        messages.append(f"{label}: expected exactly one Capability Claim rubric row")
    claim_rubrics: dict[str, str] = {}
    for cells in claim_rubric_rows:
        if len(cells) != 6 or any(not cell for cell in cells[1:]):
            messages.append(
                f"{label}: Capability Claim rubric must define Applies to and all four results: {cells!r}"
            )
            continue
        rubric_id = cells[0].strip("`")
        if rubric_id in claim_rubrics:
            messages.append(f"{label}: duplicate Capability Claim rubric ID {rubric_id}")
        claim_rubrics[rubric_id] = cells[1]

    entry_rows = [
        markdown_row_cells(line)
        for line in text.splitlines()
        if line.startswith("| `CAP-ENTRY-") and "PRACTICE-CAP-" in line
    ]
    if len(entry_rows) != 3:
        messages.append(f"{label}: expected exactly 3 Practice/Evidence entry rows")
    practice_by_evidence: dict[str, dict[str, str]] = {}
    for cells in entry_rows:
        if len(cells) != 10:
            messages.append(f"{label}: malformed Practice/Evidence row {cells!r}")
            continue
        evidence_id = cells[3].strip("`")
        if evidence_id in practice_by_evidence:
            messages.append(f"{label}: duplicate Practice evidence ID {evidence_id}")
        practice_by_evidence[evidence_id] = {
            "entry": cells[0].strip("`"),
            "reviewer": cells[4],
            "rubric": cells[5].strip("`"),
            "result": cells[6],
            "status": cells[7],
            "limitations": cells[8],
            "reassessment": cells[9].strip("`"),
        }
        status = cells[7]
        if status not in STATUS_SET:
            messages.append(f"{label}: status outside finite set: {status!r}")
        if cells[6] not in REVIEW_RESULT_SET:
            messages.append(f"{label}: Practice result outside finite set: {cells[6]!r}")
        if cells[5].strip("`") not in artifact_rubrics:
            messages.append(
                f"{label}: Practice references undefined Artifact Evidence rubric {cells[5]!r}"
            )
        elif evidence_id not in artifact_rubrics[cells[5].strip("`")]:
            messages.append(
                f"{label}: rubric {cells[5]!r} does not apply to {evidence_id}"
            )

    review_rows = [
        markdown_row_cells(line)
        for line in text.splitlines()
        if line.startswith("| `REV-CAP-")
    ]
    if len(review_rows) != 3:
        messages.append(f"{label}: expected exactly 3 Review Result rows")
    reviews_by_evidence: dict[str, dict[str, str]] = {}
    for cells in review_rows:
        if len(cells) != 9:
            messages.append(f"{label}: malformed Review Result row {cells!r}")
            continue
        evidence_id = cells[1].strip("`")
        if evidence_id in reviews_by_evidence:
            messages.append(f"{label}: duplicate reviewed evidence ID {evidence_id}")
        reviews_by_evidence[evidence_id] = {
            "reviewer": cells[3],
            "rubric": cells[4].strip("`"),
            "result": cells[5],
            "findings": cells[7],
            "disposition": cells[8],
        }
        if cells[5] not in REVIEW_RESULT_SET:
            messages.append(f"{label}: Review Result outside finite set: {cells[5]!r}")
        if cells[4].strip("`") not in artifact_rubrics:
            messages.append(
                f"{label}: Review references undefined Artifact Evidence rubric {cells[4]!r}"
            )

    if set(practice_by_evidence) != set(reviews_by_evidence):
        messages.append(
            f"{label}: Practice evidence IDs {sorted(practice_by_evidence)} do not "
            f"match reviewed evidence IDs {sorted(reviews_by_evidence)}"
        )
    for evidence_id in sorted(set(practice_by_evidence) & set(reviews_by_evidence)):
        practice = practice_by_evidence[evidence_id]
        review = reviews_by_evidence[evidence_id]
        for field in ("reviewer", "rubric", "result"):
            if practice[field] != review[field]:
                messages.append(
                    f"{label}: {evidence_id} Practice/Review {field} mismatch: "
                    f"{practice[field]!r} != {review[field]!r}"
                )
        if review["result"] == "Inconclusive":
            if practice["status"] not in {"Gap identified", "Reassessment due"}:
                messages.append(
                    f"{label}: inconclusive {evidence_id} must remain in a Gap or Reassessment status"
                )
            if not practice["limitations"] or not practice["reassessment"]:
                messages.append(
                    f"{label}: inconclusive {evidence_id} requires limitations and reassessment"
                )

    claim_rows = [
        markdown_row_cells(line)
        for line in text.splitlines()
        if line.startswith("| `CAP-CLAIM-2026-003`")
    ]
    if len(claim_rows) != 1:
        messages.append(f"{label}: expected exactly one bounded Capability Judgment row")
    else:
        cells = claim_rows[0]
        if len(cells) != 10:
            messages.append(f"{label}: malformed Capability Judgment row {cells!r}")
        else:
            claim_evidence = set(re.findall(r"ART-EVD-CAP-\d{3}", cells[3]))
            if claim_evidence != set(reviews_by_evidence):
                messages.append(
                    f"{label}: Capability Judgment evidence {sorted(claim_evidence)} "
                    f"must equal reviewed evidence {sorted(reviews_by_evidence)}"
                )
            if len(claim_evidence) < 2:
                messages.append(f"{label}: Capability Judgment requires multiple evidence items")
            claim_rubric_match = re.search(r"RUBRIC-CAP-CLAIM-\d{3}", cells[4])
            claim_rubric = claim_rubric_match.group(0) if claim_rubric_match else ""
            if claim_rubric not in claim_rubrics:
                messages.append(
                    f"{label}: Capability Judgment references undefined rubric in {cells[4]!r}"
                )
            elif "CAP-CLAIM-2026-003" not in claim_rubrics[claim_rubric]:
                messages.append(
                    f"{label}: rubric {claim_rubric!r} does not apply to CAP-CLAIM-2026-003"
                )
            boundary_match = re.search(
                r"^\| Rubric \| `([^`]+)` \|$", text, re.MULTILINE
            )
            if boundary_match is None or boundary_match.group(1) != claim_rubric:
                messages.append(
                    f"{label}: Capability Claim Boundary rubric must match {claim_rubric!r}"
                )
            if cells[5] not in CLAIM_RESULT_SET:
                messages.append(f"{label}: Capability Judgment result outside finite set: {cells[5]!r}")
            boundary_result_match = re.search(
                r"^\| Result \| (Supported|Partially supported|Not supported|Inconclusive) \|$",
                text,
                re.MULTILINE,
            )
            if boundary_result_match is None:
                messages.append(f"{label}: missing finite Capability Claim Boundary result")
            elif boundary_result_match.group(1) != cells[5]:
                messages.append(
                    f"{label}: Capability Claim Boundary result {boundary_result_match.group(1)!r} "
                    f"does not match bounded judgment result {cells[5]!r}"
                )

            review_results = [item["result"] for item in reviews_by_evidence.values()]
            if any(result == "Does not meet" for result in review_results):
                expected_claim_result = "Not supported"
            elif review_results and all(result == "Meets" for result in review_results):
                expected_claim_result = "Supported"
            elif review_results and all(
                result == "Inconclusive" for result in review_results
            ):
                expected_claim_result = "Inconclusive"
            else:
                expected_claim_result = "Partially supported"
            if cells[5] != expected_claim_result:
                messages.append(
                    f"{label}: Capability Judgment result {cells[5]!r} is inconsistent "
                    f"with Review Results {review_results!r}; expected {expected_claim_result!r}"
                )

    gap_rows = [
        markdown_row_cells(line)
        for line in text.splitlines()
        if line.startswith("| `CAP-ENTRY-") and re.search(r"2026-08-(?:12|19|26)", line)
    ]
    gap_entries = {cells[0].strip("`") for cells in gap_rows if len(cells) == 6}
    for evidence_id, practice in practice_by_evidence.items():
        if practice["result"] in {"Partially meets", "Does not meet", "Inconclusive"}:
            if practice["entry"] not in gap_entries:
                messages.append(
                    f"{label}: {evidence_id} result {practice['result']!r} requires a Gap/Learning Action row"
                )

    for date in ("2026-08-12", "2026-08-19", "2026-08-26"):
        if date not in text:
            messages.append(f"{label}: missing bounded Learning Action due date {date}")

    forbidden = (
        "実Targetへの攻撃を実施する",
        "実Credentialを取得する",
        "従業員を順位付けする",
        "公開ランキングへ掲載する",
    )
    for assertion in forbidden:
        if assertion in text:
            messages.append(f"{label}: unsafe synthetic example {assertion!r}")
    return messages


def reserved_name_contract_errors(relative: str, text: str) -> list[str]:
    messages: list[str] = []
    allowed_suffixes = (".example", ".test", ".invalid")
    for raw_url in re.findall(r"https?://[^\s`)\]>]+", text):
        host = (urlparse(raw_url).hostname or "").lower()
        if host and not host.endswith(allowed_suffixes):
            messages.append(f"{relative}: non-reserved URL in synthetic content: {raw_url}")
    domain_pattern = re.compile(
        r"(?<![A-Za-z0-9_-])(?:[A-Za-z0-9-]+\.)+(?:com|net|org|jp|io|dev|app|cloud)(?![A-Za-z0-9_-])",
        re.IGNORECASE,
    )
    for domain in domain_pattern.findall(text):
        messages.append(f"{relative}: possible real domain in synthetic content: {domain}")
    return messages


def sensitive_content_errors(relative: str, text: str) -> list[str]:
    messages: list[str] = []
    secret_patterns = (
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
        re.compile(
            r"(?i)(?:password|api[_-]?key|secret|token)\s*[:=]\s*[A-Za-z0-9+/=_-]{16,}"
        ),
    )
    for pattern in secret_patterns:
        if pattern.search(text):
            messages.append(f"{relative}: possible real credential or secret pattern detected")
    for email in re.findall(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})", text):
        domain = email.lower()
        if not domain.endswith((".example", ".test", ".invalid")):
            messages.append(f"{relative}: possible real personal email address detected")
    return messages


def source_contract_errors(registry: dict, label: str) -> list[str]:
    messages: list[str] = []
    if registry.get("checkedAt") != "2026-07-25":
        messages.append(
            f"{label}: registry-level checkedAt must remain 2026-07-25"
        )
    sources = registry.get("sources", [])
    if not isinstance(sources, list):
        return messages + [f"{label}: sources must be an array"]
    entries = {
        item.get("id"): item
        for item in sources
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    for source_id, expected in EXPECTED_SOURCES.items():
        entry = entries.get(source_id)
        if entry is None:
            messages.append(f"{label}: missing {source_id}")
            continue
        for field, expected_value in expected["fields"].items():
            if entry.get(field) != expected_value:
                messages.append(
                    f"{label}: {source_id}.{field} must be {expected_value!r}"
                )
        notes = entry.get("notes")
        if not isinstance(notes, str):
            messages.append(f"{label}: {source_id}.notes must be a string")
        else:
            for marker in expected["noteMarkers"]:
                if marker not in notes:
                    messages.append(
                        f"{label}: {source_id}.notes missing marker {marker!r}"
                    )
    chapter3_entries = {
        source_id
        for source_id, item in entries.items()
        if 3 in item.get("chapters", [])
    }
    expected_chapter3_entries = {"SRC-NICE-001", "SRC-NICE-COMP-001"}
    if chapter3_entries != expected_chapter3_entries:
        messages.append(
            f"{label}: Chapter 3 source mapping {sorted(chapter3_entries)} "
            f"must match body source IDs {sorted(expected_chapter3_entries)}"
        )
    return messages


def chapter03_page_contract_errors(registry: dict, label: str) -> list[str]:
    messages: list[str] = []
    pages = registry.get("pages", [])
    if not isinstance(pages, list):
        return [f"{label}: pages must be an array"]
    actual = [
        (
            item.get("source"),
            item.get("destination"),
            item.get("section"),
            item.get("order"),
            item.get("title"),
        )
        for item in pages
        if isinstance(item, dict)
    ]
    tuple_counts = Counter(actual)
    route_counts = Counter(item[:2] for item in actual)
    for expected in sorted(EXPECTED_CHAPTER03_PAGES):
        if tuple_counts[expected] != 1:
            messages.append(
                f"{label}: expected Chapter 3 tuple exactly once: {expected!r}; "
                f"found {tuple_counts[expected]}"
            )
        if route_counts[expected[:2]] != 1:
            messages.append(
                f"{label}: expected Chapter 3 route exactly once: {expected[:2]!r}; "
                f"found {route_counts[expected[:2]]}"
            )
    return messages


def registry_mutation_is_rejected(registry: dict, label: str) -> bool:
    try:
        parsed = parse_registry_data(registry, label)
    except SitePageRegistryError:
        return True
    return bool(chapter03_page_contract_errors(parsed, label))


def verify_negative_regressions(
    chapter: str,
    template: str,
    case: str,
    sources: dict,
    raw_registry: dict,
    audit_note: str,
) -> None:
    chapter_without_trace = chapter.replace(CORE_TRACE, "Task → Evidence")
    if not chapter_contract_errors(chapter_without_trace, "negative chapter core trace"):
        error("negative regression accepted Chapter 3 without the core trace")

    chapter_with_false_standard = chapter.replace(
        "NISTが定めた普遍的なLevel標準ではない",
        "NISTが定めた普遍的なLevel標準である",
    )
    if not chapter_contract_errors(
        chapter_with_false_standard, "negative universal level assertion"
    ):
        error("negative regression accepted a false universal NICE level assertion")

    chapter_with_hr_use = chapter + "\nこの章のCapability Judgmentを採用判定に転用できる。\n"
    if not chapter_contract_errors(chapter_with_hr_use, "negative Chapter HR use"):
        error("negative regression accepted Chapter 3 Capability Judgment for hiring")

    template_status_drift = template.replace(
        "Planned / In practice / Evidence submitted / Reviewed / Gap identified / Reassessment due / Complete",
        "Planned / In practice / Ranked / Complete",
    )
    if not template_contract_errors(template_status_drift, "negative status drift"):
        error("negative regression accepted Capability Evidence status drift")

    template_with_hr_use = template + "\nこのTemplateを採用判定と公開ランキングに使う。\n"
    if not template_contract_errors(template_with_hr_use, "negative Template HR use"):
        error("negative regression accepted ART-14 for hiring or public ranking")

    unsafe_case = case + "\n実Targetへの攻撃を実施する\n"
    if not case_contract_errors(unsafe_case, "negative real-target practice"):
        error("negative regression accepted real-target activity as learning evidence")

    evidence_shrink = case.replace(
        "`ART-EVD-CAP-001`, `ART-EVD-CAP-002`, `ART-EVD-CAP-003` | Synthetic Capability Panel / `RUBRIC-CAP-CLAIM-003` | Partially supported",
        "`ART-EVD-CAP-002` | Synthetic Capability Panel / `RUBRIC-CAP-CLAIM-003` | Partially supported",
    )
    if not case_contract_errors(evidence_shrink, "negative single-evidence claim"):
        error("negative regression accepted a single-evidence Capability Judgment")

    result_mismatch = case.replace(
        "`ART-EVD-CAP-001` | Synthetic Safety Reviewer | `RUBRIC-CAP-001` | Partially meets | Gap identified",
        "`ART-EVD-CAP-001` | Synthetic Safety Reviewer | `RUBRIC-CAP-001` | Meets | Gap identified",
        1,
    )
    if not case_contract_errors(result_mismatch, "negative Practice/Review mismatch"):
        error("negative regression accepted a Practice/Review Result mismatch")

    invalid_result = case.replace(
        "`RUBRIC-CAP-003` | Inconclusive | 2026-08-05T15:00:00+09:00",
        "`RUBRIC-CAP-003` | Pass | 2026-08-05T15:00:00+09:00",
    )
    if not case_contract_errors(invalid_result, "negative invalid Review Result"):
        error("negative regression accepted a Review Result outside the finite set")

    missing_claim_rubric = "\n".join(
        line
        for line in case.splitlines()
        if not line.startswith("| `RUBRIC-CAP-CLAIM-003`")
    )
    if not case_contract_errors(
        missing_claim_rubric, "negative missing Capability Claim rubric"
    ):
        error("negative regression accepted an undefined Capability Claim rubric")

    incomplete_artifact_rubric = case.replace(
        ARTIFACT_RUBRIC_HEADER,
        "| Rubric ID | Applies to | Meets | Partially meets | Inconclusive |",
        1,
    )
    if not case_contract_errors(
        incomplete_artifact_rubric, "negative incomplete Artifact Evidence rubric"
    ):
        error("negative regression accepted an Artifact rubric without Does not meet")

    trigger_header_drift = case.replace(
        CLAIM_JUDGMENT_HEADER,
        CLAIM_JUDGMENT_HEADER.replace("Reassessment Trigger", "Trigger"),
        1,
    )
    if not case_contract_errors(
        trigger_header_drift, "negative Capability Judgment header drift"
    ):
        error("negative regression accepted Trigger in place of Reassessment Trigger")

    overstated_claim = case.replace(
        "| Result | Partially supported |",
        "| Result | Supported |",
        1,
    ).replace(
        "Synthetic Capability Panel / `RUBRIC-CAP-CLAIM-003` | Partially supported |",
        "Synthetic Capability Panel / `RUBRIC-CAP-CLAIM-003` | Supported |",
        1,
    )
    if not case_contract_errors(overstated_claim, "negative overstated Capability Claim"):
        error("negative regression accepted Supported with partial/inconclusive reviews")

    degraded_review = case.replace(
        "`RUBRIC-CAP-003` | Inconclusive | Reassessment due",
        "`RUBRIC-CAP-003` | Does not meet | Reassessment due",
        1,
    ).replace(
        "`RUBRIC-CAP-003` | Inconclusive | 2026-08-05T15:00:00+09:00",
        "`RUBRIC-CAP-003` | Does not meet | 2026-08-05T15:00:00+09:00",
        1,
    )
    if not case_contract_errors(degraded_review, "negative degraded Review Result"):
        error("negative regression accepted a partial Claim with Does not meet evidence")

    boundary_result_drift = case.replace(
        "| Result | Partially supported |",
        "| Result | Supported |",
        1,
    )
    if not case_contract_errors(
        boundary_result_drift, "negative Capability Claim Boundary result drift"
    ):
        error("negative regression accepted mismatched Claim Boundary and Judgment results")

    missing_authorization_stub = case.replace(
        "#### Minimum Authorization Checklist stub",
        "#### Authorization input omitted",
        1,
    )
    if not case_contract_errors(
        missing_authorization_stub, "negative missing Authorization Checklist stub"
    ):
        error("negative regression accepted a non-self-contained Task 1 exercise")

    if not reserved_name_contract_errors(
        "negative synthetic domain", "https://admin.localhost/runbook"
    ):
        error("negative regression accepted .localhost outside the Case domain policy")

    leaked_audit = audit_note + "\napi_key=0123456789abcdef0123456789abcdef\n"
    if not sensitive_content_errors("negative source audit secret", leaked_audit):
        error("negative regression accepted a secret-like value in the source audit")
    pii_audit = audit_note + "\nreviewer=person@real-company.com\n"
    if not sensitive_content_errors("negative source audit PII", pii_audit):
        error("negative regression accepted a real-domain email in the source audit")

    source_mutations: list[tuple[str, str, dict]] = []
    for source_id in EXPECTED_SOURCES:
        for field, value in (
            ("version", "latest"),
            ("checkedAt", "2026-07-25"),
            ("nextReviewAt", "2027-01-01"),
            ("notes", "NICE proves competence"),
        ):
            mutation = deepcopy(sources)
            entry = next(
                item for item in mutation["sources"] if item.get("id") == source_id
            )
            entry[field] = value
            source_mutations.append((source_id, field, mutation))
    for source_id, field, mutation in source_mutations:
        if not source_contract_errors(
            mutation, f"negative source {source_id}.{field}"
        ):
            error(f"negative regression accepted {source_id} {field} drift")

    page_source = "manuscript/03-capability-evidence.md"
    page_mutations: list[tuple[str, dict]] = []
    mutation = deepcopy(raw_registry)
    mutation["schemaVersion"] = "0.0.0"
    page_mutations.append(("schemaVersion drift", mutation))
    mutation = deepcopy(raw_registry)
    next(item for item in mutation["pages"] if item.get("source") == page_source)["section"] = "additional"
    page_mutations.append(("section drift", mutation))
    mutation = deepcopy(raw_registry)
    next(item for item in mutation["pages"] if item.get("source") == page_source)["order"] = 47
    page_mutations.append(("order drift", mutation))
    mutation = deepcopy(raw_registry)
    next(item for item in mutation["pages"] if item.get("source") == page_source)["title"] = "Changed Chapter Title"
    page_mutations.append(("title drift", mutation))
    mutation = deepcopy(raw_registry)
    page = next(item for item in mutation["pages"] if item.get("source") == page_source)
    mutation["pages"].append(deepcopy(page))
    page_mutations.append(("duplicate page", mutation))
    mutation = deepcopy(raw_registry)
    next(item for item in mutation["pages"] if item.get("source") == page_source)["unexpectedKey"] = True
    page_mutations.append(("unknown page key", mutation))
    for name, mutation in page_mutations:
        if not registry_mutation_is_rejected(
            mutation, f"site-pages.json negative regression ({name})"
        ):
            error(f"site-pages.json: negative mutation was accepted: {name}")


def main() -> int:
    required_files = (
        "manuscript/03-capability-evidence.md",
        "templates/capability-evidence-matrix.md",
        "templates/learning-route-plan.md",
        "cases/ch03-capability-evidence-example.md",
        "scripts/check_chapter03_contract.py",
        "site-pages.json",
        "artifact-index.md",
        "figure-index.md",
        "glossary.md",
        "cases/index.md",
        "index.md",
        "book-config.json",
        "references/sources.json",
        "references/reference-baseline.md",
        "references/ch03-source-review-2026-08-05.md",
        "package.json",
    )
    for relative in required_files:
        if not (ROOT / relative).is_file():
            error(f"missing required file: {relative}")

    config = load_json("book-config.json")
    chapter_config = next(
        (
            item
            for item in config.get("structure", {}).get("chapters", [])
            if isinstance(item, dict) and item.get("id") == "ch03-capability-evidence"
        ),
        None,
    )
    expected_objectives = [
        "能力を分解できる",
        "学習証拠を定義できる",
        "Capability Evidence Matrixを作成できる",
    ]
    if chapter_config is None:
        error("book-config.json: missing ch03-capability-evidence")
    elif chapter_config.get("objectives") != expected_objectives:
        error("book-config.json: chapter 3 learning objectives changed unexpectedly")

    chapter_path = "manuscript/03-capability-evidence.md"
    template_path = "templates/capability-evidence-matrix.md"
    case_path = "cases/ch03-capability-evidence-example.md"
    chapter = read_text(chapter_path)
    template = read_text(template_path)
    case = read_text(case_path)
    for message in chapter_contract_errors(chapter, chapter_path):
        error(message)
    for message in template_contract_errors(template, template_path):
        error(message)
    for message in case_contract_errors(case, case_path):
        error(message)
    for message in reserved_name_contract_errors(case_path, case):
        error(message)

    safety_scan_files = (
        chapter_path,
        template_path,
        case_path,
        "templates/learning-route-plan.md",
        "references/ch03-source-review-2026-08-05.md",
        "references/sources.json",
        "references/reference-baseline.md",
        "artifact-index.md",
        "cases/index.md",
        "figure-index.md",
        "glossary.md",
        "index.md",
        "site-pages.json",
        "package.json",
    )
    for relative in safety_scan_files:
        for message in sensitive_content_errors(relative, read_text(relative)):
            error(message)

    raw_registry = load_json("site-pages.json")
    try:
        registry = parse_registry_data(raw_registry)
    except SitePageRegistryError as exc:
        error(f"site-pages.json: invalid registry: {exc}")
        registry = {}
    for message in chapter03_page_contract_errors(registry, "site-pages.json"):
        error(message)

    if registry:
        source_to_destination = {page.source: page.destination for page in PAGES}
        source_to_destination.update({
            item["source"]: item["destination"]
            for item in registry.get("pages", [])
            if isinstance(item, dict)
        })
        rewritten_chapter = rewrite_links(
            chapter,
            chapter_path,
            "chapters/chapter-03/index.md",
            source_to_destination,
        )
        if "/blob/main/references/" in rewritten_chapter:
            error(
                "generated Chapter 3 source links must not fall back to mutable blob/main"
            )
        require_tokens(
            "generated Chapter 3 links",
            rewritten_chapter,
            (
                "../../source-notes/",
                "../../references/chapter-03-source-review/",
            ),
        )

    require_tokens(
        "templates/learning-route-plan.md",
        read_text("templates/learning-route-plan.md"),
        (
            "Artifact ID: `ART-01`",
            "Plan ID: `LRP-YYYY-NNN`",
            "Learner Profile ID: `SYNTH-LEARNER-NNN`",
        ),
    )

    require_tokens(
        "artifact-index.md",
        read_text("artifact-index.md"),
        (
            "| ART-14 | Capability Evidence Matrix | 3, 29 | `templates/capability-evidence-matrix.md` |",
            "cases/ch03-capability-evidence-example.md",
        ),
    )
    require_tokens(
        "figure-index.md",
        read_text("figure-index.md"),
        ("F-03-01", "T-03-01", "T-03-02", "manuscript/03-capability-evidence.md"),
    )
    require_tokens(
        "glossary.md",
        read_text("glossary.md"),
        (
            "| Artifact Evidence |",
            "| Capability Judgment |",
            "| Competency Area |",
            "| Reassessment |",
            "| Review Result |",
            "| Work Role |",
        ),
    )
    require_tokens(
        "cases/index.md",
        read_text("cases/index.md"),
        ("ch03-capability-evidence-example.md", "Capability Evidence Matrix"),
    )
    require_tokens(
        "index.md",
        read_text("index.md"),
        (
            "manuscript/03-capability-evidence.md",
            "templates/capability-evidence-matrix.md",
            "cases/ch03-capability-evidence-example.md",
        ),
    )

    sources = load_json("references/sources.json")
    for message in source_contract_errors(sources, "references/sources.json"):
        error(message)

    audit_note_path = "references/ch03-source-review-2026-08-05.md"
    audit_note = read_text(audit_note_path)
    require_tokens(
        audit_note_path,
        audit_note,
        (
            "Checked at | 2026-08-05",
            "対象章 | 第3章（`SRC-NICE-001`の既存mappingとして第0章・第1章も監査）",
            "NIST SP 800-181 Rev.1",
            "SRC-NICE-001",
            "SRC-NICE-COMP-001",
            "2020-11-16",
            "NICE Framework Components v2.2.0",
            "2026-04-28",
            "OG-WRL-017",
            "NF-COM-006",
            "NF-COM-008",
            "administrative changes",
            "CURRENT VERSION: 2.2.0 (April 28, 2025)",
            "見かけ上のページ誤記",
            "Certification vendorの資料は、標準や能力証明の根拠として採用していない",
            "個人の能力を証明しない",
            "本書固有の学習進行表現",
        ),
    )
    official_urls = (
        "https://csrc.nist.gov/pubs/sp/800/181/r1/final",
        "https://www.nist.gov/news-events/news/2026/04/nice-releases-nice-framework-components-v220",
        "https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center/current-version/change-logs",
        "https://www.nist.gov/itl/applied-cybersecurity/nice/nice-framework-resource-center/nice-framework-current-versions",
        "https://csrc.nist.gov/projects/cprt/catalog",
    )
    require_tokens(audit_note_path, audit_note, official_urls)

    baseline_path = "references/reference-baseline.md"
    if read_text(baseline_path) != render_reference_baseline():
        error(f"{baseline_path}: out of sync with references/sources.json")

    package = load_json("package.json")
    scripts = package.get("scripts", {})
    if scripts.get("check:chapter03") != "python3 scripts/check_chapter03_contract.py":
        error("package.json: missing check:chapter03 script")
    if "check:chapter03" not in scripts.get("test", ""):
        error("package.json: npm test does not include check:chapter03")

    if chapter and template and case and sources and raw_registry:
        verify_negative_regressions(
            chapter, template, case, sources, raw_registry, audit_note
        )

    for message in ERRORS:
        print(f"ERROR: {message}")
    if ERRORS:
        return 1

    print(
        "chapter 3 contract passed: manuscript, ART-14, synthetic learner case, "
        "NICE source state, publication registry, safety boundary, and fail-closed regressions"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
