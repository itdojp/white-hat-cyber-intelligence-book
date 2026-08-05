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

REASSESSMENT_STATUS_SET = {
    "Planned",
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
        "実Target操作を行わない。必要になった時点で停止する",
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
    exercise_match = re.search(
        r"^## 8\. 安全な演習\s*$\n(?P<body>.*?)(?=^## 9\. )",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if exercise_match is None:
        messages.append(f"{label}: missing bounded safe exercise section")
    else:
        for line_number, line in enumerate(
            exercise_match.group("body").splitlines(), start=1
        ):
            for message in unsafe_operational_field_errors(
                line, f"safe exercise line {line_number}"
            ):
                messages.append(f"{label}: {message}")
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


PROTECTED_PRACTICE_INPUT = re.compile(
    r"(?:実(?:際|在)?の?(?:Target|標的)|現実の(?:Target|標的)|real[- ]target|"
    r"第三者(?:の)?(?:System|システム|環境|Data|データ)|"
    r"third[- ]party[- ]?(?:system|data|environment)|"
    r"実(?:Credential|クレデンシャル|認証情報|資格情報|Token|トークン|Cookie|クッキー)|"
    r"real[- ]?(?:credential|token|cookie)|"
    r"(?:credential|token|cookie|secret|password|passphrase)s?|"
    r"(?:jwt|json[- ]web[- ]token)|"
    r"api[- _]?(?:key|キー)|"
    r"(?:access|private|ssh|session|authentication|auth|signing|encryption)"
    r"[- _]?(?:key|id)|"
    r"アクセス(?:[- _・]?(?:キー|鍵))|"
    r"(?:秘密|SSH|セッション|認証|署名|暗号)"
    r"(?:[- _・]?(?:キー|鍵|ID|識別子))|PII|"
    r"認証情報|資格情報|トークン|クッキー|秘密(?:情報)?|シークレット|"
    r"パスワード|パスフレーズ|個人(?:の)?(?:情報|データ)|"
    r"従業員(?:の)?(?:Data|データ|情報)|"
    r"顧客(?:の)?(?:Data|データ|情報)|"
    r"(?:personal|employee|customer|staff)[- ](?:data|info(?:rmation)?)|"
    r"personally[- ]identifiable[- ]info(?:rmation)?)",
    re.IGNORECASE,
)
SYNTHETIC_QUALIFIABLE_INPUT = re.compile(
    r"(?:(?:credential|token|cookie|secret|password|passphrase)s?|"
    r"(?:jwt|json[- ]web[- ]token)|"
    r"api[- _]?(?:key|キー)|"
    r"(?:access|private|ssh|session|authentication|auth|signing|encryption)"
    r"[- _]?(?:key|id)|"
    r"アクセス(?:[- _・]?(?:キー|鍵))|"
    r"(?:秘密|SSH|セッション|認証|署名|暗号)"
    r"(?:[- _・]?(?:キー|鍵|ID|識別子))|"
    r"認証情報|資格情報|トークン|クッキー|秘密(?:情報)?|シークレット|"
    r"パスワード|パスフレーズ)",
    re.IGNORECASE,
)
EXPLICIT_SYNTHETIC_QUALIFIER = re.compile(
    r"(?:合成|架空|ダミー|模擬|テスト用|予約済み|"
    r"synthetic|dummy|mock|test[- ]only|reserved)(?:の|[- ]+)?$",
    re.IGNORECASE,
)
EXPLICIT_NEGATED_USE = re.compile(
    r"^(?:"
    r"ではなく|ではない|"
    r"(?:を|は|が|へ|に|として|の|も)?"
    r"(?:攻撃|操作|調査|走査|スキャン|観測|閲覧|参照|分析|取得|使用|利用|"
    r"投入|保存|収集|接続|検証|公開|記録)?"
    r"(?:を|は|が|も)?"
    r"(?:なし|しない|せず|禁止|対象外|除外|未使用|非使用|不要|要求しない|"
    r"使わない|使わず|用いない|含めない|含まない|持ち込まない|行わない|"
    r"許可しない)|"
    r"\s*(?:(?:is|are|was|were)\s+not|must\s+not\s+be|not)\s+"
    r"(?:used|allowed|required|included|accessed|collected|stored|retrieved|shared)"
    r")",
    re.IGNORECASE,
)


def unsafe_operational_field_errors(field: str, context: str) -> list[str]:
    """Reject protected inputs unless directly synthetic or explicitly negated."""
    messages: list[str] = []
    matches = list(PROTECTED_PRACTICE_INPUT.finditer(field))
    for index, match in enumerate(matches):
        prefix = field[: match.start()]
        clause_start = max(prefix.rfind(mark) for mark in "、,。;；\n") + 1
        protected_prefix = field[clause_start : match.start()]
        suffix = field[match.end() :]
        clause_tail = re.split(r"[、,。;；\n]", suffix, maxsplit=1)[0]
        if index + 1 < len(matches):
            next_match = matches[index + 1]
            next_relative_start = next_match.start() - match.end()
            if next_relative_start < len(clause_tail):
                clause_tail = clause_tail[:next_relative_start]
        synthetic_qualified = bool(
            SYNTHETIC_QUALIFIABLE_INPUT.fullmatch(match.group(0))
            and EXPLICIT_SYNTHETIC_QUALIFIER.fullmatch(protected_prefix)
        )
        if not (EXPLICIT_NEGATED_USE.fullmatch(clause_tail) or synthetic_qualified):
            messages.append(
                f"unsafe real-target or sensitive-data input in {context}: "
                f"{match.group(0)!r} is neither explicitly synthetic nor negated"
            )
            break
    return messages


def case_contract_errors(text: str, label: str) -> list[str]:
    messages: list[str] = []
    required = (
        "ART-14",
        "CAP-MATRIX-2026-003",
        "SYNTH-LEARNER-003",
        "### Parent ART-01 Learning Route Plan instance",
        "| Plan ID | `LRP-2026-003` |",
        "| 現在の役割 | 合成学習者。実在の従業員・応募者ではない |",
        "| 目標とするResponsibility | 許可判断支援、offline detection検証、Source評価済み分析判断を、安全境界内で説明する |",
        "| 判断・業務上の目的 | 三Taskの学習優先度と再評価条件を決める。採用・配置・報酬判断には使わない |",
        "| 6か月後の成果物 | `ART-14`と`ART-EVD-CAP-001`〜`003`のReview済み版 |",
        "| 使用する隔離ラボ | `CAP-PACKET-2026-003-R1`。外部Networkなし |",
        "| 学習の証拠 | `ART-EVD-CAP-001`、`ART-EVD-CAP-002`、`ART-EVD-CAP-003` |",
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
        "FIX-CAP-002-INCOMPLETE",
        "R1 detector contractは「`operation=admin_change`かつ`actor_authorized=false`かつ`required_fields=complete`なら`Alert`、それ以外は`No alert`」",
        "Observed in R1",
        "`FIX-CAP-002-POS` | `operation=admin_change`, `actor_authorized=false`, `required_fields=complete` | Alert | Alert",
        "`FIX-CAP-002-NEG` | `operation=admin_change`, `actor_authorized=true`, `required_fields=complete` | No alert | No alert",
        "`FIX-CAP-002-BENIGN` | `operation=view`, `actor_authorized=false`, `required_fields=complete` | No alert | No alert",
        "`FIX-CAP-002-INCOMPLETE` | `operation=admin_change`, `actor_authorized=false`, `required_fields=incomplete` | No alert | No alert",
        "detector contractを四Fixtureへ順に適用",
        "四Fixtureが期待結果と一致し",
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
    if text.count("CAP-PACKET-2026-003-R1") != 6:
        messages.append(
            f"{label}: authoritative Practice packet ID must occur exactly 6 times"
        )
    packet_match = re.search(
        r"^### 2\.1 完全合成Practice packet\s*$\n(?P<body>.*?)(?=^## 3\. )",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if packet_match is None:
        messages.append(f"{label}: missing bounded authoritative Practice packet")
    else:
        for line_number, line in enumerate(
            packet_match.group("body").splitlines(), start=1
        ):
            for message in unsafe_operational_field_errors(
                line, f"Practice packet line {line_number}"
            ):
                messages.append(f"{label}: {message}")

    def reject_unsafe_operational_field(field: str, context: str) -> None:
        messages.extend(
            f"{label}: {message}"
            for message in unsafe_operational_field_errors(field, context)
        )

    expected_work_decomposition = {
        "CAP-ENTRY-001": ("TASK-CAP-001", "KN-CAP-001", "SK-CAP-001"),
        "CAP-ENTRY-002": ("TASK-CAP-002", "KN-CAP-002", "SK-CAP-002"),
        "CAP-ENTRY-003": ("TASK-CAP-003", "KN-CAP-003", "SK-CAP-003"),
    }
    work_rows = [
        markdown_row_cells(line)
        for line in text.splitlines()
        if line.startswith("| `CAP-ENTRY-")
        and "TASK-CAP-" in line
        and "KN-CAP-" in line
        and "SK-CAP-" in line
    ]
    work_by_entry: dict[str, tuple[str, str, str]] = {}
    for cells in work_rows:
        if len(cells) != 6:
            messages.append(f"{label}: malformed Work Decomposition row {cells!r}")
            continue
        entry_id = cells[0].strip("`")
        for field_name, field_value in (
            ("Work Role / Responsibility", cells[1]),
            ("Task statement", cells[2]),
            ("Skill reference", cells[4]),
        ):
            reject_unsafe_operational_field(
                field_value, f"{entry_id} {field_name}"
            )
        identifiers: list[str] = []
        for pattern, cell in (
            (r"TASK-CAP-\d{3}", cells[2]),
            (r"KN-CAP-\d{3}", cells[3]),
            (r"SK-CAP-\d{3}", cells[4]),
        ):
            matches = re.findall(pattern, cell)
            identifiers.append(matches[0] if len(matches) == 1 else "")
            if len(matches) != 1:
                messages.append(
                    f"{label}: {entry_id} Work Decomposition requires exactly one {pattern}"
                )
        if entry_id in work_by_entry:
            messages.append(f"{label}: duplicate Work Decomposition entry {entry_id}")
        work_by_entry[entry_id] = tuple(identifiers)  # type: ignore[assignment]
    if set(work_by_entry) != set(expected_work_decomposition):
        messages.append(
            f"{label}: Work Decomposition entries {sorted(work_by_entry)} do not match "
            f"{sorted(expected_work_decomposition)}"
        )
    for entry_id in sorted(set(work_by_entry) & set(expected_work_decomposition)):
        if work_by_entry[entry_id] != expected_work_decomposition[entry_id]:
            messages.append(
                f"{label}: {entry_id} Work Decomposition IDs "
                f"{work_by_entry[entry_id]!r} do not match "
                f"{expected_work_decomposition[entry_id]!r}"
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
    practice_by_entry: dict[str, dict[str, str]] = {}

    for cells in entry_rows:
        if len(cells) != 10:
            messages.append(f"{label}: malformed Practice/Evidence row {cells!r}")
            continue
        evidence_id = cells[3].strip("`")
        reject_unsafe_operational_field(
            cells[2], f"{cells[0].strip('`')} Authority / Environment"
        )
        reject_unsafe_operational_field(
            cells[8], f"{cells[0].strip('`')} Practice Limitations"
        )
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
        entry_id = cells[0].strip("`")
        if entry_id in practice_by_entry:
            messages.append(f"{label}: duplicate Practice entry ID {entry_id}")
        practice_by_entry[entry_id] = practice_by_evidence[evidence_id]
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
        reject_unsafe_operational_field(
            cells[7], f"{cells[0].strip('`')} Review Findings"
        )
        reject_unsafe_operational_field(
            cells[8], f"{cells[0].strip('`')} Review Disposition"
        )
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

    boundary_section_match = re.search(
        r"^## 1\. Capability Claim Boundary\s*$\n(?P<body>.*?)(?=^## 2\. )",
        text,
        re.MULTILINE | re.DOTALL,
    )
    boundary_text = ""
    if boundary_section_match is None:
        messages.append(f"{label}: missing bounded Capability Claim Boundary section")
    else:
        boundary_text = boundary_section_match.group("body")
    for field_name in ("Scope", "Conditions", "Limitations", "Reassessment Trigger"):
        boundary_field_matches = re.findall(
            rf"^\| {re.escape(field_name)} \| (.+) \|$",
            boundary_text,
            re.MULTILINE,
        )
        if len(boundary_field_matches) != 1:
            messages.append(
                f"{label}: Capability Claim Boundary requires exactly one {field_name} field"
            )
            continue
        reject_unsafe_operational_field(
            boundary_field_matches[0], f"Capability Claim Boundary {field_name}"
        )

    claim_reassessment_id = ""
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
            for field_name, field_value in (
                ("Scope", cells[1]),
                ("Conditions", cells[2]),
                ("Limitations", cells[6]),
                ("Reassessment Trigger", cells[8]),
            ):
                reject_unsafe_operational_field(
                    field_value, f"Bounded Capability Judgment {field_name}"
                )
            claim_evidence = set(re.findall(r"ART-EVD-CAP-\d{3}", cells[3]))
            if claim_evidence != set(reviews_by_evidence):
                messages.append(
                    f"{label}: Capability Judgment evidence {sorted(claim_evidence)} "
                    f"must equal reviewed evidence {sorted(reviews_by_evidence)}"
                )
            if len(claim_evidence) < 2:
                messages.append(f"{label}: Capability Judgment requires multiple evidence items")
            boundary_evidence_match = re.search(
                r"^\| Evidence set \| (.+) \|$", text, re.MULTILINE
            )
            if boundary_evidence_match is None:
                messages.append(f"{label}: missing Capability Claim Boundary evidence set")
            else:
                boundary_evidence = set(
                    re.findall(
                        r"ART-EVD-CAP-\d{3}", boundary_evidence_match.group(1)
                    )
                )
                if boundary_evidence != claim_evidence:
                    messages.append(
                        f"{label}: Capability Claim Boundary evidence {sorted(boundary_evidence)} "
                        f"does not match bounded judgment evidence {sorted(claim_evidence)}"
                    )
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
            claim_reassessment_id = cells[9].strip("`")
            if claim_reassessment_id != "REA-CAP-CLAIM-003":
                messages.append(
                    f"{label}: Capability Judgment Reassessment ID "
                    f"{claim_reassessment_id!r} must be 'REA-CAP-CLAIM-003'"
                )

    gap_rows = [
        markdown_row_cells(line)
        for line in text.splitlines()
        if line.startswith("| `CAP-ENTRY-") and re.search(r"2026-08-(?:12|19|26)", line)
    ]
    gap_entries = {cells[0].strip("`") for cells in gap_rows if len(cells) == 6}
    gap_next_evidence: dict[str, str] = {}
    for cells in gap_rows:
        if len(cells) == 6:
            entry_id = cells[0].strip("`")
            next_evidence = re.findall(r"ART-EVD-CAP-\d{3}-R2", cells[5])
            if len(next_evidence) != 1:
                messages.append(
                    f"{label}: {entry_id} Gap row requires exactly one next Evidence ID"
                )
            else:
                if entry_id in gap_next_evidence:
                    messages.append(f"{label}: duplicate Gap entry ID {entry_id}")
                gap_next_evidence[entry_id] = next_evidence[0]
            reject_unsafe_operational_field(
                cells[1], f"{entry_id} Gap"
            )
            reject_unsafe_operational_field(
                cells[2], f"{entry_id} Learning Action"
            )
    for evidence_id, practice in practice_by_evidence.items():
        if practice["result"] in {"Partially meets", "Does not meet", "Inconclusive"}:
            if practice["entry"] not in gap_entries:
                messages.append(
                    f"{label}: {evidence_id} result {practice['result']!r} requires a Gap/Learning Action row"
                )

    expected_reassessments = {
        "REA-CAP-001": ({"ART-EVD-CAP-001-R2"}, {"TASK-CAP-001"}),
        "REA-CAP-002": ({"ART-EVD-CAP-002-R2"}, {"TASK-CAP-002"}),
        "REA-CAP-003": ({"ART-EVD-CAP-003-R2"}, {"TASK-CAP-003"}),
        "REA-CAP-CLAIM-003": (
            {
                "ART-EVD-CAP-001-R2",
                "ART-EVD-CAP-002-R2",
                "ART-EVD-CAP-003-R2",
            },
            {"TASK-CAP-001", "TASK-CAP-002", "TASK-CAP-003"},
        ),
    }
    reassessment_rows = [
        markdown_row_cells(line)
        for line in text.splitlines()
        if line.startswith("| `REA-CAP-")
    ]
    reassessments: dict[str, tuple[set[str], set[str], str]] = {}
    for cells in reassessment_rows:
        if len(cells) != 8:
            messages.append(f"{label}: malformed Reassessment row {cells!r}")
            continue
        reassessment_id = cells[0].strip("`")
        if reassessment_id in reassessments:
            messages.append(f"{label}: duplicate Reassessment ID {reassessment_id}")
        evidence_ids = set(re.findall(r"ART-EVD-CAP-\d{3}-R2", cells[3]))
        task_ids = set(re.findall(r"TASK-CAP-\d{3}", cells[4]))
        status = cells[7]
        reassessments[reassessment_id] = (evidence_ids, task_ids, status)
        if status not in REASSESSMENT_STATUS_SET:
            messages.append(
                f"{label}: Reassessment status outside finite set: {status!r}"
            )
        for field_name, field_value in (
            ("Reassessment Trigger", cells[2]),
            ("Closure criteria", cells[6]),
        ):
            reject_unsafe_operational_field(
                field_value, f"{reassessment_id} {field_name}"
            )
    if set(reassessments) != set(expected_reassessments):
        messages.append(
            f"{label}: Reassessment IDs {sorted(reassessments)} do not match "
            f"{sorted(expected_reassessments)}"
        )
    for reassessment_id in sorted(set(reassessments) & set(expected_reassessments)):
        evidence_ids, task_ids, _ = reassessments[reassessment_id]
        expected_evidence, expected_tasks = expected_reassessments[reassessment_id]
        if evidence_ids != expected_evidence:
            messages.append(
                f"{label}: {reassessment_id} evidence {sorted(evidence_ids)} "
                f"does not match {sorted(expected_evidence)}"
            )
        if task_ids != expected_tasks:
            messages.append(
                f"{label}: {reassessment_id} tasks {sorted(task_ids)} "
                f"do not match {sorted(expected_tasks)}"
            )

    expected_entries = set(expected_work_decomposition)
    if set(practice_by_entry) != expected_entries:
        messages.append(
            f"{label}: Practice entries {sorted(practice_by_entry)} do not match "
            f"Work Decomposition {sorted(expected_entries)}"
        )
    if gap_entries != expected_entries:
        messages.append(
            f"{label}: Gap entries {sorted(gap_entries)} do not match "
            f"Work Decomposition {sorted(expected_entries)}"
        )
    for entry_id in sorted(expected_entries & set(practice_by_entry)):
        suffix = entry_id.rsplit("-", 1)[1]
        expected_reassessment_id = f"REA-CAP-{suffix}"
        expected_next_evidence = f"ART-EVD-CAP-{suffix}-R2"
        if practice_by_entry[entry_id]["reassessment"] != expected_reassessment_id:
            messages.append(
                f"{label}: {entry_id} Practice Reassessment ID "
                f"{practice_by_entry[entry_id]['reassessment']!r} must be "
                f"{expected_reassessment_id!r}"
            )
        if gap_next_evidence.get(entry_id) != expected_next_evidence:
            messages.append(
                f"{label}: {entry_id} Gap next Evidence "
                f"{gap_next_evidence.get(entry_id)!r} must be {expected_next_evidence!r}"
            )
        reassessment = reassessments.get(expected_reassessment_id)
        if reassessment is not None and reassessment[0] != {expected_next_evidence}:
            messages.append(
                f"{label}: {entry_id} Gap next Evidence does not match "
                f"{expected_reassessment_id} recollection Evidence"
            )
    if claim_reassessment_id and claim_reassessment_id not in reassessments:
        messages.append(
            f"{label}: Capability Judgment Reassessment ID "
            f"{claim_reassessment_id!r} is not defined"
        )

    expected_final_review_areas = {
        "Technical correctness",
        "Safety / authorization",
        "Source quality / freshness",
        "Evidence / traceability",
        "Decision usefulness",
    }
    final_review_section_match = re.search(
        r"^## 9\. Review\s*$\n(?P<body>.*)\Z",
        text,
        re.MULTILINE | re.DOTALL,
    )
    final_review_rows: dict[str, list[str]] = {}
    if final_review_section_match is None:
        messages.append(f"{label}: missing bounded final Review section")
    else:
        for line in final_review_section_match.group("body").splitlines():
            if not line.startswith("|"):
                continue
            cells = markdown_row_cells(line)
            if not cells or cells[0] not in expected_final_review_areas:
                continue
            if len(cells) != 6:
                messages.append(f"{label}: malformed final Review row {cells!r}")
                continue
            if cells[0] in final_review_rows:
                messages.append(f"{label}: duplicate final Review area {cells[0]!r}")
            final_review_rows[cells[0]] = cells
            reject_unsafe_operational_field(
                cells[5], f"final Review {cells[0]} Notes"
            )
    if set(final_review_rows) != expected_final_review_areas:
        messages.append(
            f"{label}: final Review areas {sorted(final_review_rows)} do not match "
            f"{sorted(expected_final_review_areas)}"
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

    chapter_with_unsafe_exercise = chapter.replace(
        "合成または明示的許可済みのPractice Environmentを指定する。",
        "第三者Systemを実Targetとして追加走査する。",
        1,
    )
    if not chapter_contract_errors(
        chapter_with_unsafe_exercise, "negative unsafe Chapter exercise"
    ):
        error("negative regression accepted real-target activity in Chapter exercise")

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

    unsafe_practice_environment = case.replace(
        "合成Scenario。外部接続と実Target操作なし",
        "合成Scenario。実Target操作あり",
        1,
    )
    if not case_contract_errors(
        unsafe_practice_environment, "negative unsafe Practice Environment"
    ):
        error("negative regression accepted affirmative real-target Practice wording")

    unsafe_learning_action = case.replace(
        "既存fixtureの追加benign recordをofflineで再評価する",
        "第三者Systemを実Targetとして追加走査する",
        1,
    )
    if not case_contract_errors(
        unsafe_learning_action, "negative unsafe Learning Action"
    ):
        error("negative regression accepted third-party real-target Learning Action")

    for unsafe_field in (
        "第三者Dataを分析する",
        "第三者Systemを観測する",
        "実Targetのログを閲覧する",
        "実Credentialを参照する",
        "従業員データを使用する",
        "real token used",
        "real cookie collected",
        "第三者のシステムを実際の標的として追加走査する",
        "Tokenを取得して追加benign recordを作る",
        "Cookieを保存する",
        "production credentials used",
        "PIIを収集する",
        "Synthetic lab uses production credentials to add a benign record",
        "Tokenを取得してCookieを使用しない追加benign recordを作る",
        "passwordを取得して追加benign recordを作る",
        "パスワードを取得して追加benign recordを作る",
        "個人情報を収集するが公開しない",
        "実Targetを走査するが記録しない",
        "第三者Systemへ接続するが保存しない",
        "シークレットを取得する",
        "個人データを収集する",
        "個人情報は収集しないが保存する",
        "実Targetを走査しないが観測する",
        "第三者Systemへ接続しないが閲覧する",
        "シークレットは未使用だが参照する",
        "個人データを含めないが分析する",
        "Tokenを取得せず保存する",
        "Cookieを使用しないが収集する",
        "実Credentialを持ち込まないが閲覧する",
        "PII not collected but stored",
        "secret not shared but retrieved",
        "not synthetic token used for additional benign record",
        "非合成Tokenを使用する",
        "personal information collected for additional benign record",
        "customer information collected for additional benign record",
        "employee information collected for additional benign record",
        "synthetic personally identifiable information used",
        "合成個人情報を使用する",
        "API keyを取得して追加benign recordを作る",
        "APIキーを取得する",
        "API キーを取得する",
        "access-key retrieved for replay",
        "アクセスキーを取得する",
        "顧客情報を収集する",
        "従業員情報を収集する",
        "顧客の情報を収集する",
        "従業員の情報を収集する",
        "personal info collected for additional benign record",
        "private key retrieved for additional benign record",
        "SSH keyを取得して追加benign recordを作る",
        "session IDを取得して追加benign recordを作る",
        "JWTを取得して追加benign recordを作る",
        "Bearer JWT retrieved for replay",
    ):
        if not unsafe_operational_field_errors(
            unsafe_field, "negative broad protected-input wording"
        ):
            error(f"negative regression accepted protected Practice input: {unsafe_field}")

    for explicitly_negated_field in (
        "合成Scenario。外部接続と実Target操作なし",
        "個人情報を使用しない",
        "第三者Systemへ接続しない",
        "実Targetではない",
        "個人情報を含まない",
        "合成Tokenを使用する",
        "Synthetic Cookie fixtureを使用する",
        "合成APIキーを使用する",
        "合成API キーを使用する",
        "Synthetic access-key fixture used",
        "Synthetic private key fixture used",
        "Synthetic session ID fixture used",
        "Synthetic JWT fixture used",
        "Tokenを使用しない",
    ):
        if unsafe_operational_field_errors(
            explicitly_negated_field, "negative-form safety statement"
        ):
            error(
                "negative regression rejected an explicitly negated safety statement: "
                f"{explicitly_negated_field}"
            )

    unsafe_gap = case.replace(
        "Source independenceを支える別系統が不足",
        "第三者Dataを収集する必要がある",
        1,
    )
    if not case_contract_errors(unsafe_gap, "negative unsafe Gap wording"):
        error("negative regression accepted protected input in a Gap cell")

    work_entry_drift = case.replace(
        "| `CAP-ENTRY-001` | Security engagementの開始判断を支援する |",
        "| `CAP-ENTRY-999` | Security engagementの開始判断を支援する |",
        1,
    )
    if not case_contract_errors(
        work_entry_drift, "negative Work Decomposition entry drift"
    ):
        error("negative regression accepted Work Decomposition entry drift")

    work_task_drift = case.replace(
        "`TASK-CAP-001`: 合成ScenarioからAuthorization Checklistを作り、停止・Escalation条件を説明する",
        "`TASK-CAP-999`: 合成ScenarioからAuthorization Checklistを作り、停止・Escalation条件を説明する",
        1,
    )
    if not case_contract_errors(
        work_task_drift, "negative Work Decomposition Task drift"
    ):
        error("negative regression accepted Work Decomposition Task drift")

    practice_reassessment_drift = case.replace(
        "法的助言の正しさと実案件のAuthorityは評価対象外 | `REA-CAP-001` |",
        "法的助言の正しさと実案件のAuthorityは評価対象外 | `REA-CAP-003` |",
        1,
    )
    if not case_contract_errors(
        practice_reassessment_drift, "negative Practice Reassessment drift"
    ):
        error("negative regression accepted a mismatched Practice Reassessment ID")

    claim_reassessment_drift = case.replace(
        "Components、Scope、Role、Rubric、期限の変更 | `REA-CAP-CLAIM-003` |",
        "Components、Scope、Role、Rubric、期限の変更 | `REA-CAP-001` |",
        1,
    )
    if not case_contract_errors(
        claim_reassessment_drift, "negative Claim Reassessment drift"
    ):
        error("negative regression accepted a mismatched Claim Reassessment ID")

    gap_next_evidence_drift = case.replace(
        "2026-08-12 | `ART-EVD-CAP-001-R2` |",
        "2026-08-12 | `ART-EVD-CAP-999-R2` |",
        1,
    )
    if not case_contract_errors(
        gap_next_evidence_drift, "negative Gap next Evidence drift"
    ):
        error("negative regression accepted a mismatched Gap next Evidence ID")

    invalid_reassessment_status = case.replace(
        "| `REA-CAP-003` | 2026-08-27 | 独立合成Source追加 | `ART-EVD-CAP-003-R2` | `TASK-CAP-003` | Synthetic Analytic Reviewer | 来歴と独立性を分離して再判定 | Reassessment due |",
        "| `REA-CAP-003` | 2026-08-27 | 独立合成Source追加 | `ART-EVD-CAP-003-R2` | `TASK-CAP-003` | Synthetic Analytic Reviewer | 来歴と独立性を分離して再判定 | Ranked |",
        1,
    )
    if not case_contract_errors(
        invalid_reassessment_status, "negative invalid Reassessment status"
    ):
        error("negative regression accepted Reassessment status outside finite set")

    practice_status_in_reassessment = case.replace(
        "| `REA-CAP-001` | 2026-08-13 | 再承認Triggerの修正完了 | `ART-EVD-CAP-001-R2` | `TASK-CAP-001` | Synthetic Safety Reviewer | Scope変更時の停止・再承認が一意 | Planned |",
        "| `REA-CAP-001` | 2026-08-13 | 再承認Triggerの修正完了 | `ART-EVD-CAP-001-R2` | `TASK-CAP-001` | Synthetic Safety Reviewer | Scope変更時の停止・再承認が一意 | Reviewed |",
        1,
    )
    if not case_contract_errors(
        practice_status_in_reassessment,
        "negative Practice status in Reassessment row",
    ):
        error("negative regression accepted Practice-only status in Reassessment row")

    unsafe_reassessment_trigger = case.replace(
        "再承認Triggerの修正完了",
        "Tokenを取得して再評価",
        1,
    )
    if not case_contract_errors(
        unsafe_reassessment_trigger, "negative unsafe Reassessment Trigger"
    ):
        error("negative regression accepted protected input in Reassessment Trigger")

    unsafe_reassessment_closure = case.replace(
        "来歴と独立性を分離して再判定",
        "第三者Dataを収集して確認",
        1,
    )
    if not case_contract_errors(
        unsafe_reassessment_closure, "negative unsafe Reassessment Closure"
    ):
        error("negative regression accepted protected input in Reassessment Closure")

    unsafe_review_disposition = case.replace(
        "GapとしてR2を要求",
        "Tokenを取得して再評価",
        1,
    )
    if not case_contract_errors(
        unsafe_review_disposition, "negative unsafe Review Disposition"
    ):
        error("negative regression accepted protected input in Review Disposition")

    unsafe_boundary_trigger = case.replace(
        "NICE Components版、Practice Scope、Reviewer rubric、担当Responsibilityの変更、または期限到来",
        "Tokenを取得してCapabilityを再評価する",
        1,
    )
    if not case_contract_errors(
        unsafe_boundary_trigger, "negative unsafe Claim Boundary Trigger"
    ):
        error("negative regression accepted protected input in Claim Boundary Trigger")

    unsafe_judgment_trigger = case.replace(
        "Components、Scope、Role、Rubric、期限の変更",
        "Tokenを取得してCapabilityを再評価する",
        1,
    )
    if not case_contract_errors(
        unsafe_judgment_trigger, "negative unsafe Judgment Trigger"
    ):
        error("negative regression accepted protected input in Judgment Trigger")

    unsafe_action_field_mutations = (
        (
            "Claim Boundary Scope",
            "合成ScenarioでTask 2のoffline detection fixtureをRubricどおり検証できる。Task 1は一部条件を満たし、Task 3は結論不能であることを識別し、両者のGapと再評価を説明できる",
            "合成ScenarioでTask 2のoffline detection fixtureをRubricどおり検証できる。Task 1は一部条件を満たし、Task 3は結論不能であることを識別し、両者のGapと再評価を説明できる。Tokenを取得して検証する",
        ),
        (
            "Claim Boundary Conditions",
            "完全合成資料、Repository提供fixture、Components v2.2.0、Reviewerからの一回の質問機会",
            "完全合成資料、Repository提供fixture、Components v2.2.0、Reviewerからの一回の質問機会、API keyを取得する",
        ),
        (
            "Claim Boundary Limitations",
            "実案件の法的判断は未評価、実Targetは操作しない、製品固有Detection実装は未評価、人物・組織への帰属は未評価",
            "実案件の法的判断は未評価、実Targetは操作しない、製品固有Detection実装は未評価、人物・組織への帰属は未評価。個人情報を収集する",
        ),
        (
            "Work Responsibility",
            "Security engagementの開始判断を支援する",
            "Security engagementの開始判断を支援する。API keyを取得する",
        ),
        (
            "Task statement",
            "`TASK-CAP-002`: 本Caseのoffline fixtureを期待結果と照合し、Coverageと限界を記録する",
            "`TASK-CAP-002`: 本Caseのoffline fixtureを期待結果と照合し、Coverageと限界を記録する。実Targetを走査する",
        ),
        (
            "Skill reference",
            "`SK-CAP-003`: Fact、Assumption、Judgmentを分離する",
            "`SK-CAP-003`: Fact、Assumption、Judgmentを分離する。個人情報を収集する",
        ),
        (
            "Practice Limitations",
            "Product固有設定、Production scale、未知Telemetryは未評価",
            "Product固有設定、Production scale、未知Telemetryは未評価。API keyを取得する",
        ),
        (
            "Review Findings",
            "四Gateは分離したが再承認Triggerが不足",
            "四Gateは分離したが再承認Triggerが不足。Tokenを取得して確認した",
        ),
        (
            "Judgment Scope",
            "Task 2のoffline detection fixture検証、およびTask 1 / 3の未達・結論不能の識別と再評価設計",
            "Task 2のoffline detection fixture検証、およびTask 1 / 3の未達・結論不能の識別と再評価設計。access-keyを取得する",
        ),
        (
            "Judgment Conditions",
            "合成資料、offline fixture、v2.2.0、宣言済みRubric",
            "合成資料、offline fixture、v2.2.0、宣言済みRubric、APIキーを取得する",
        ),
        (
            "Judgment Limitations",
            "Task 1は条件不足、Task 3は結論不能。実案件と人物評価へ一般化しない",
            "Task 1は条件不足、Task 3は結論不能。実案件と人物評価へ一般化しない。顧客情報を収集する",
        ),
    )
    for field_name, safe_value, unsafe_value in unsafe_action_field_mutations:
        mutated_case = case.replace(safe_value, unsafe_value, 1)
        if mutated_case == case:
            error(f"negative regression fixture missing for {field_name}")
        if not case_contract_errors(
            mutated_case, f"negative unsafe {field_name}"
        ):
            error(f"negative regression accepted protected input in {field_name}")

    unsafe_final_review_notes = case.replace(
        "合成・offline条件と停止条件を確認",
        "合成・offline条件と停止条件を確認。Tokenを取得して確認",
        1,
    )
    if not case_contract_errors(
        unsafe_final_review_notes, "negative unsafe final Review Notes"
    ):
        error("negative regression accepted protected input in final Review Notes")

    fixture_without_required_field_negative = case.replace(
        "| `FIX-CAP-002-INCOMPLETE` | `operation=admin_change`, `actor_authorized=false`, `required_fields=incomplete` | No alert | No alert | 欠損Fieldの補完処理は未評価 |\n",
        "",
        1,
    )
    if not case_contract_errors(
        fixture_without_required_field_negative,
        "negative missing required-fields fixture",
    ):
        error("negative regression accepted detector fixtures without required_fields gate coverage")

    unsafe_replay_step = case.replace(
        "3. Task 2はdetector contractを四Fixtureへ順に適用し、ExpectedとObservedを比較する。",
        "3. Task 2はdetector contractを四Fixtureへ順に適用し、ExpectedとObservedを比較する。第三者Systemを実Targetとして追加走査する。",
        1,
    )
    if not case_contract_errors(unsafe_replay_step, "negative unsafe replay step"):
        error("negative regression accepted real-target activity in R1 replay procedure")

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

    missing_parent_plan = case.replace(
        "### Parent ART-01 Learning Route Plan instance",
        "### Parent plan omitted",
        1,
    )
    if not case_contract_errors(missing_parent_plan, "negative missing parent Plan"):
        error("negative regression accepted ART-14 without its parent LRP instance")

    boundary_evidence_drift = case.replace(
        "| Evidence set | `ART-EVD-CAP-001`, `ART-EVD-CAP-002`, `ART-EVD-CAP-003` |",
        "| Evidence set | `ART-EVD-CAP-002` |",
        1,
    )
    if not case_contract_errors(
        boundary_evidence_drift, "negative Capability Claim Boundary evidence drift"
    ):
        error("negative regression accepted conflicting Boundary and Judgment evidence sets")

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
