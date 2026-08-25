#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.content_safety_policy import (  # noqa: E402
    POLICY_VERSION as CONTENT_SAFETY_POLICY_VERSION,
    SafetyFinding,
    scan_action_text,
    scan_host_policy,
)
from scripts.publication_projection import (  # noqa: E402
    PROJECTION_VERSION,
    ProjectedDocument,
    ProjectionRuntimeError,
    destination_fields,
    is_absolute_destination,
    is_policy_scan_field,
    project_documents,
)
from scripts.render_reference_baseline import (  # noqa: E402
    render as render_reference_baseline,
)
from scripts.sync_book_site import (  # noqa: E402
    SitePageRegistryError,
    parse_registry_data,
)

ERRORS: list[str] = []
EXPECTED_CONTENT_SAFETY_POLICY_VERSION = "1.2.0"
EXPECTED_PUBLICATION_PROJECTION_VERSION = "1.0.0"

CHAPTER02_DOCUMENTS = (
    "manuscript/02-law-ethics-authorization.md",
    "templates/authorization-checklist.md",
    "cases/ch02-authorization-decision-example.md",
)

# Layer A owns the complete ordered H1/H2 inventory. Layer B decides which source
# constructs are headings, so Setext/indented/fenced precedence is not reimplemented
# here. H3 and deeper content is still projected and scanned but does not define a
# Chapter 2 top-level section boundary.
EXPECTED_CHAPTER02_HEADINGS = {
    "manuscript/02-law-ethics-authorization.md": (
        (1, "第2章　法、倫理、許可、責任ある開示"),
        (2, "この章の位置付け"),
        (2, "本章の責任境界"),
        (2, "学習目標"),
        (2, "前提知識"),
        (2, "導入ケース"),
        (2, "1. 四つのGate"),
        (2, "2. 法、契約、組織権限、倫理を分離する"),
        (2, "3. 書面による許可"),
        (2, "4. Data、Secret、証拠の取扱い"),
        (2, "5. 委託、再委託、Cloud / SaaS"),
        (2, "6. 脆弱性を発見したとき"),
        (2, "7. 四つの視点"),
        (2, "8. Handoff Contract"),
        (2, "9. 安全な演習"),
        (2, "10. 作成する成果物"),
        (2, "11. 評価基準"),
        (2, "12. よくある誤解"),
        (2, "章のまとめ"),
        (2, "次に学ぶこと"),
        (2, "参考文献・Source Note ID"),
    ),
    "templates/authorization-checklist.md": (
        (1, "Authorization Checklist"),
        (2, "目的"),
        (2, "使用条件"),
        (2, "0. Document Control"),
        (2, "1. Decision Requirement"),
        (2, "2. Authority Gate"),
        (2, "3. Scope Gate"),
        (2, "4. Safety Gate"),
        (2, "5. Disclosure Gate"),
        (2, "6. Legal, Contractual, and Policy Questions"),
        (2, "7. Conditions"),
        (2, "8. Decision Record"),
        (2, "9. RoE Handoff"),
        (2, "10. Reassessment"),
        (2, "11. Traceability Check"),
        (2, "12. Review"),
    ),
    "cases/ch02-authorization-decision-example.md": (
        (1, "第2章 合成記入例：OAuth連携評価前のAuthorization判断"),
        (2, "この記入例の扱い"),
        (2, "0. Document Control"),
        (2, "1. Decision Requirement"),
        (2, "2. Authority Gate"),
        (2, "3. Scope Gate"),
        (2, "4. Safety Gate"),
        (2, "5. Disclosure Gate"),
        (2, "6. Legal, Contractual, and Policy Questions"),
        (2, "7. Conditions"),
        (2, "8. Decision Record"),
        (2, "9. RoE Handoff"),
        (2, "10. Reassessment"),
        (2, "11. Traceability Check"),
        (2, "12. Review"),
    ),
}

# Layer A identities are document-scoped exact projected fields.  Absolute source
# lines/ordinals remain diagnostic evidence, but are not semantic identifiers: an
# unrelated safe insertion must not invalidate every later field.  Type, element
# ownership, attribute, exact text, and exactly-once cardinality make moving a
# token into code or duplicating an exemption fail closed.
EXPECTED_CHAPTER02_SEMANTIC_FIELDS = {
    "manuscript/02-law-ethics-authorization.md": frozenset(
        {
            ("reader_visible_text", "heading", None, "1.1 Authority Gate"),
            ("reader_visible_text", "heading", None, "1.2 Scope Gate"),
            ("reader_visible_text", "heading", None, "1.3 Safety Gate"),
            ("reader_visible_text", "heading", None, "1.4 Disclosure Gate"),
            ("reader_visible_text", "heading", None, "BRIDGE"),
            ("reader_visible_text", "heading", None, "DELEGATE"),
            ("reader_visible_text", "heading", None, "OWN"),
            (
                "reader_visible_text",
                "p",
                None,
                "本章の責任境界 本書は、実務上のAuthorization Gateと後続工程へのHandoffに責任を持つ。"
                "本章は法的助言を提供せず、個別事案の法的判断と法令解釈は専門家へ委譲する。"
                "専門領域の詳細は委譲先に残すが、委譲先へのリンクを読まなくても、"
                "第2章の論旨と運用判断は単独で成立する。",
            ),
            (
                "reader_visible_text",
                "list_path",
                None,
                "DELEGATE 個別事案の法的助言と法令解釈は、"
                "適格な法務・契約専門家へ委譲する",
            ),
        }
    ),
    "templates/authorization-checklist.md": frozenset(
        {
            (
                "reader_visible_text",
                "table_row",
                None,
                "0. Document Control Field Value Artifact ID ART-13",
            ),
            (
                "reader_visible_text",
                "table_row",
                None,
                "0. Document Control Field Value Parent Case ID CASE-YYYY-NNN",
            ),
            (
                "reader_visible_text",
                "table_row",
                None,
                "0. Document Control Field Value Relation "
                "refines / supersedes / independent",
            ),
            (
                "reader_visible_text",
                "table_row",
                None,
                "10. Reassessment Field Value Reassessment ID REA-AUTH-001",
            ),
            (
                "reader_visible_text",
                "table_row",
                None,
                "8. Decision Record Field Value Authorization Decision ID DEC-AUTH-001",
            ),
            (
                "reader_visible_text",
                "table_row",
                None,
                "9. RoE Handoff Handoff ID Input to RoE "
                "Acceptance criteria Actual status Reject / "
                "return condition Owner HO-AUTH-001 Decision "
                "Requirement Owner、期限、判断内容がある 抽象目的のみ",
            ),
            (
                "reader_visible_text",
                "table_row",
                None,
                "Authority evidence Evidence ID Description "
                "Source / custodian Collected at Integrity / "
                "reference Limitation EVD-AUTH-001",
            ),
            (
                "reader_visible_text",
                "table_row",
                None,
                "Condition ID Condition Reason Owner Due date "
                "Verification Status COND-AUTH-001 Open / "
                "Satisfied / Waived by authorized owner / "
                "Failed",
            ),
        }
    ),
    "cases/ch02-authorization-decision-example.md": frozenset(
        {
            (
                "reader_visible_text",
                "table_row",
                None,
                "0. Document Control Field Value Artifact ID ART-13",
            ),
            (
                "reader_visible_text",
                "table_row",
                None,
                "0. Document Control Field Value Parent Case ID CASE-2026-001",
            ),
            (
                "reader_visible_text",
                "table_row",
                None,
                "0. Document Control Field Value Relation refines",
            ),
            (
                "reader_visible_text",
                "table_row",
                None,
                "10. Reassessment Field Value Reassessment ID REA-AUTH-2026-001",
            ),
            (
                "reader_visible_text",
                "table_row",
                None,
                "7. Conditions Condition ID Condition "
                "Reason Owner Due date Verification "
                "Status COND-AUTH-2026-001 Production "
                "credentialを操作しない 委託契約とAuthority未確認 "
                "Lab Operator Assessment終了まで Evidence "
                "/ operation log Open",
            ),
            (
                "reader_visible_text",
                "table_row",
                None,
                "8. Decision Record Field Value "
                "Authorization Decision ID "
                "DEC-AUTH-2026-001",
            ),
            (
                "reader_visible_text",
                "table_row",
                None,
                "9. RoE Handoff Handoff ID Input to "
                "RoE Acceptance criteria Actual "
                "status Reject / return condition "
                "Owner HO-AUTH-2026-001 Decision "
                "Requirement Owner、期限、判断内容 Pass "
                "抽象目的のみ CTO",
            ),
            (
                "reader_visible_text",
                "table_row",
                None,
                "Authority evidence Evidence ID "
                "Description Source / custodian "
                "Collected at Integrity / reference "
                "Limitation EVD-AUTH-2026-001 "
                "合成Tenantを対象とした設定Review承認 CTO / "
                "Ticket system "
                "2026-08-05T10:15:00+09:00 "
                "SYNTH-EVD-AUTH-001 "
                "Production、外部API、実Credentialを含まない",
            ),
        }
    ),
}

# These fields close the finite Layer A gaps that raw token checks cannot own:
# core reader-visible Gate meaning and the Authorization/Decision chain IDs.
EXPECTED_CHAPTER02_SEMANTIC_FIELDS[
    "manuscript/02-law-ethics-authorization.md"
] |= frozenset(
    {
        (
            "reader_visible_text",
            "p",
            None,
            "1.1 Authority Gate Authority Gateは、誰がその操作を許可できるかを確認する。",
        ),
        (
            "reader_visible_text",
            "p",
            None,
            "1.2 Scope Gate Scope Gateは、対象を技術的識別子へ変換する。",
        ),
        (
            "reader_visible_text",
            "p",
            None,
            "1.3 Safety Gate Safety Gateは、許可された操作の中から、判断に必要な最小操作を選ぶ。",
        ),
        (
            "reader_visible_text",
            "p",
            None,
            "1.4 Disclosure Gate Disclosure Gateは、発見情報の共有・調整・公開経路を事前に決める。",
        ),
    }
)
EXPECTED_CHAPTER02_SEMANTIC_FIELDS[
    "templates/authorization-checklist.md"
] |= frozenset(
    {
        (
            "reader_visible_text",
            "table_row",
            None,
            "0. Document Control Field Value Authorization Record ID AUTH-YYYY-NNN",
        ),
        (
            "reader_visible_text",
            "table_row",
            None,
            "1. Decision Requirement Field Value Decision Requirement ID DR-AUTH-001",
        ),
    }
)
EXPECTED_CHAPTER02_SEMANTIC_FIELDS[
    "cases/ch02-authorization-decision-example.md"
] |= frozenset(
    {
        (
            "reader_visible_text",
            "table_row",
            None,
            "0. Document Control Field Value Authorization Record ID AUTH-CASE-2026-001",
        ),
        (
            "reader_visible_text",
            "table_row",
            None,
            "1. Decision Requirement Field Value Decision Requirement ID DR-AUTH-2026-001",
        ),
    }
)

CHAPTER02_REVIEWED_ACTION_IDENTITIES = {
    "manuscript/02-law-ethics-authorization.md": frozenset(
        {
            (
                "reader_visible_text",
                "list_path",
                None,
                "初期情報 未確認: 委託先が管理するApp credentialの変更権限",
            ),
            (
                "reader_visible_text",
                "p",
                None,
                "一つの層がPassしても、他の層を自動的にPassさせない。たとえば契約にSecurity "
                "testingの記載があっても、第三者Tenantや実利用者Dataまで対象になるとは限らない。",
            ),
        }
    ),
    "templates/authorization-checklist.md": frozenset(
        {
            (
                "reader_visible_text",
                "list_path",
                None,
                "使用条件 実Credential、Token、Cookie、Personal "
                "Data、Secret valueを記載しない。",
            )
        }
    ),
    "cases/ch02-authorization-decision-example.md": frozenset(
        {
            (
                "reader_visible_text",
                "table_row",
                None,
                "1. Decision Requirement Field Value "
                "Maximum acceptable uncertainty "
                "委託先が管理するProduction "
                "credentialの変更権限は未確定でも、合成Tenantのread-only設定Reviewだけを分離できること",
            ),
            (
                "reader_visible_text",
                "table_row",
                None,
                "2. Authority Gate Field Value "
                "Authority gaps Production "
                "credential変更権限と委託契約上の作業範囲は未確認",
            ),
            (
                "reader_visible_text",
                "table_row",
                None,
                "3. Scope Gate Field Value Prohibited "
                "methods Token取得・利用、外部API "
                "call、Credential変更、権限昇格、横展開、DoS、Data変更",
            ),
            (
                "reader_visible_text",
                "table_row",
                None,
                "6. Legal, Contractual, and Policy "
                "Questions Question ID Question "
                "Applicable source / contract Owner "
                "Status Answer / limitation Recheck "
                "trigger LQ-AUTH-2026-002 "
                "委託契約はProduction credential変更を許容するか "
                "Synthetic contract Procurement / "
                "Legal Escalated "
                "本Decisionでは不要。Production変更前に確認 "
                "Production変更案承認前",
            ),
            (
                "reader_visible_text",
                "table_row",
                None,
                "6. Legal, Contractual, and Policy "
                "Questions Question ID Question "
                "Applicable source / contract Owner "
                "Status Answer / limitation Recheck "
                "trigger LQ-AUTH-2026-004 "
                "許可外の認証試行を行ってよいか "
                "SRC-JP-LAW-001、internal policy Legal "
                "Answered 行わない。合成Tenant・明示許可操作だけに限定 "
                "Scope変更時",
            ),
            (
                "reader_visible_text",
                "table_row",
                None,
                "8. Decision Record Field Value "
                "Information gaps Production "
                "credential変更権限、実Vendor窓口、契約通知期限",
            ),
            (
                "reader_visible_text",
                "table_row",
                None,
                "9. RoE Handoff Handoff ID Input to "
                "RoE Acceptance criteria Actual "
                "status Reject / return condition "
                "Owner HO-AUTH-2026-004 Method "
                "boundary Read-only、禁止操作、Rate Pass "
                "Token利用・外部API追加 Lab Operator",
            ),
        }
    ),
}

CHAPTER02_REVIEWED_HOST_IDENTITIES = {
    "manuscript/02-law-ethics-authorization.md": frozenset(
        {
            (
                "reader_visible_text",
                "list_path",
                None,
                "初期情報 対象: billing-bridge.exampleの合成Tenant",
            )
        }
    ),
    "templates/authorization-checklist.md": frozenset(),
    "cases/ch02-authorization-decision-example.md": frozenset(
        {
            (
                "reader_visible_text",
                "list_path",
                None,
                "Domainは予約済みの.exampleを使用する。",
            ),
            (
                "reader_visible_text",
                "table_row",
                None,
                "3. Scope Gate Field Value In-scope "
                "target identifiers "
                "tenant-auth-lab-01.test、billing-bridge.exampleの合成App "
                "registration、設定Export",
            ),
        }
    ),
}

# A reviewed Policy exemption belongs to one exact projected owner under one
# exact Chapter 2 heading path.  The relational owner prevents identical text
# from inheriting an exemption after it is copied or moved to another section.
CHAPTER02_REVIEWED_ACTION_HEADING_PATHS = {
    "manuscript/02-law-ethics-authorization.md": {
        "初期情報 未確認: 委託先が管理するApp credentialの変更権限": (
            "第2章　法、倫理、許可、責任ある開示",
            "9. 安全な演習",
            "初期情報",
        ),
        (
            "一つの層がPassしても、他の層を自動的にPassさせない。たとえば契約にSecurity "
            "testingの記載があっても、第三者Tenantや実利用者Dataまで対象になるとは限らない。"
        ): (
            "第2章　法、倫理、許可、責任ある開示",
            "2. 法、契約、組織権限、倫理を分離する",
            "T-02-01　許容性判断の層",
        ),
    },
    "templates/authorization-checklist.md": {
        "使用条件 実Credential、Token、Cookie、Personal Data、Secret valueを記載しない。": (
            "Authorization Checklist",
            "使用条件",
        ),
    },
    "cases/ch02-authorization-decision-example.md": {
        "1. Decision Requirement Field Value Maximum acceptable uncertainty "
        "委託先が管理するProduction credentialの変更権限は未確定でも、合成Tenantのread-only設定Reviewだけを分離できること": (
            "第2章 合成記入例：OAuth連携評価前のAuthorization判断",
            "1. Decision Requirement",
        ),
        "2. Authority Gate Field Value Authority gaps Production credential変更権限と委託契約上の作業範囲は未確認": (
            "第2章 合成記入例：OAuth連携評価前のAuthorization判断",
            "2. Authority Gate",
        ),
        "3. Scope Gate Field Value Prohibited methods Token取得・利用、外部API call、Credential変更、権限昇格、横展開、DoS、Data変更": (
            "第2章 合成記入例：OAuth連携評価前のAuthorization判断",
            "3. Scope Gate",
        ),
        "6. Legal, Contractual, and Policy Questions Question ID Question Applicable source / contract Owner Status Answer / limitation Recheck trigger LQ-AUTH-2026-002 委託契約はProduction credential変更を許容するか Synthetic contract Procurement / Legal Escalated 本Decisionでは不要。Production変更前に確認 Production変更案承認前": (
            "第2章 合成記入例：OAuth連携評価前のAuthorization判断",
            "6. Legal, Contractual, and Policy Questions",
        ),
        "6. Legal, Contractual, and Policy Questions Question ID Question Applicable source / contract Owner Status Answer / limitation Recheck trigger LQ-AUTH-2026-004 許可外の認証試行を行ってよいか SRC-JP-LAW-001、internal policy Legal Answered 行わない。合成Tenant・明示許可操作だけに限定 Scope変更時": (
            "第2章 合成記入例：OAuth連携評価前のAuthorization判断",
            "6. Legal, Contractual, and Policy Questions",
        ),
        "8. Decision Record Field Value Information gaps Production credential変更権限、実Vendor窓口、契約通知期限": (
            "第2章 合成記入例：OAuth連携評価前のAuthorization判断",
            "8. Decision Record",
        ),
        "9. RoE Handoff Handoff ID Input to RoE Acceptance criteria Actual status Reject / return condition Owner HO-AUTH-2026-004 Method boundary Read-only、禁止操作、Rate Pass Token利用・外部API追加 Lab Operator": (
            "第2章 合成記入例：OAuth連携評価前のAuthorization判断",
            "9. RoE Handoff",
        ),
    },
}

CHAPTER02_REVIEWED_HOST_HEADING_PATHS = {
    "manuscript/02-law-ethics-authorization.md": {
        "初期情報 対象: billing-bridge.exampleの合成Tenant": (
            "第2章　法、倫理、許可、責任ある開示",
            "9. 安全な演習",
            "初期情報",
        ),
    },
    "templates/authorization-checklist.md": {},
    "cases/ch02-authorization-decision-example.md": {
        "Domainは予約済みの.exampleを使用する。": (
            "第2章 合成記入例：OAuth連携評価前のAuthorization判断",
            "この記入例の扱い",
        ),
        "3. Scope Gate Field Value In-scope target identifiers tenant-auth-lab-01.test、billing-bridge.exampleの合成App registration、設定Export": (
            "第2章 合成記入例：OAuth連携評価前のAuthorization判断",
            "3. Scope Gate",
        ),
    },
}

CHAPTER02_REVIEWED_ACTION_RELATIONS = {
    logical_path: frozenset(
        (identity, CHAPTER02_REVIEWED_ACTION_HEADING_PATHS[logical_path][identity[3]])
        for identity in identities
    )
    for logical_path, identities in CHAPTER02_REVIEWED_ACTION_IDENTITIES.items()
}
CHAPTER02_REVIEWED_HOST_RELATIONS = {
    logical_path: frozenset(
        (identity, CHAPTER02_REVIEWED_HOST_HEADING_PATHS[logical_path][identity[3]])
        for identity in identities
    )
    for logical_path, identities in CHAPTER02_REVIEWED_HOST_IDENTITIES.items()
}

CHAPTER02_RESPONSIBILITY_BOUNDARY_RELATIONS = {
    "manuscript/02-law-ethics-authorization.md": frozenset(
        {
            (
                (
                    "reader_visible_text",
                    "p",
                    None,
                    "本章の責任境界 本書は、実務上のAuthorization Gateと後続工程へのHandoffに責任を持つ。"
                    "本章は法的助言を提供せず、個別事案の法的判断と法令解釈は専門家へ委譲する。"
                    "専門領域の詳細は委譲先に残すが、委譲先へのリンクを読まなくても、"
                    "第2章の論旨と運用判断は単独で成立する。",
                ),
                (
                    "第2章　法、倫理、許可、責任ある開示",
                    "本章の責任境界",
                ),
            ),
            (
                (
                    "reader_visible_text",
                    "list_path",
                    None,
                    "DELEGATE 個別事案の法的助言と法令解釈は、"
                    "適格な法務・契約専門家へ委譲する",
                ),
                (
                    "第2章　法、倫理、許可、責任ある開示",
                    "本章の責任境界",
                    "DELEGATE",
                ),
            ),
        }
    ),
    "templates/authorization-checklist.md": frozenset(),
    "cases/ch02-authorization-decision-example.md": frozenset(),
}

CHAPTER02_REVIEWED_PROVENANCE_RELATIONS = {
    "manuscript/02-law-ethics-authorization.md": frozenset(
        {
            (
                (
                    "destination",
                    "link",
                    "href",
                    "https://itdojp.github.io/pentest-learning-book/",
                ),
                (
                    "reader_visible_text",
                    "list_path",
                    None,
                    "DELEGATE 詳細な攻撃技法と脆弱性の悪用は、許可済み評価の専門的な方法、成果物、安全境界を詳述する実務で使えるペネトレーションテスト大全へ委譲する",
                ),
            ),
            (
                (
                    "destination",
                    "link",
                    "href",
                    "https://itdojp.github.io/practical-auth-book/",
                ),
                (
                    "reader_visible_text",
                    "list_path",
                    None,
                    "DELEGATE 認証・認可Protocol内部と安全な実装は、OAuth、OIDC、SAML等の設計と実装を詳述する実践 認証認可システム設計へ委譲する",
                ),
            ),
            (
                (
                    "destination",
                    "link",
                    "href",
                    "https://itdojp.github.io/it-infra-security-guide-book/",
                ),
                (
                    "reader_visible_text",
                    "list_path",
                    None,
                    "DELEGATE Infrastructure Hardeningと防御実装は、Network、OS、Cloud、ContainerのSecurity実装を詳述するインフラエンジニアのための情報セキュリティ実装ガイドへ委譲する",
                ),
            ),
        }
    ),
    "templates/authorization-checklist.md": frozenset(),
    "cases/ch02-authorization-decision-example.md": frozenset(),
}

# Ordered exact-text keys add semantic sequence without coupling the contract to
# absolute line/field ordinals.  The corresponding full identities above still
# enforce projected type, owner element, attribute, and exactly-once cardinality.
EXPECTED_CHAPTER02_SEMANTIC_ORDER = {
    "manuscript/02-law-ethics-authorization.md": (
        "本章の責任境界 本書は、実務上のAuthorization Gateと後続工程へのHandoffに責任を持つ。"
        "本章は法的助言を提供せず、個別事案の法的判断と法令解釈は専門家へ委譲する。"
        "専門領域の詳細は委譲先に残すが、委譲先へのリンクを読まなくても、"
        "第2章の論旨と運用判断は単独で成立する。",
        "OWN",
        "BRIDGE",
        "DELEGATE",
        "DELEGATE 個別事案の法的助言と法令解釈は、適格な法務・契約専門家へ委譲する",
        "1.1 Authority Gate",
        "1.1 Authority Gate Authority Gateは、誰がその操作を許可できるかを確認する。",
        "1.2 Scope Gate",
        "1.2 Scope Gate Scope Gateは、対象を技術的識別子へ変換する。",
        "1.3 Safety Gate",
        "1.3 Safety Gate Safety Gateは、許可された操作の中から、判断に必要な最小操作を選ぶ。",
        "1.4 Disclosure Gate",
        "1.4 Disclosure Gate Disclosure Gateは、発見情報の共有・調整・公開経路を事前に決める。",
    ),
    "templates/authorization-checklist.md": (
        "0. Document Control Field Value Artifact ID ART-13",
        "0. Document Control Field Value Authorization Record ID AUTH-YYYY-NNN",
        "0. Document Control Field Value Parent Case ID CASE-YYYY-NNN",
        "0. Document Control Field Value Relation refines / supersedes / independent",
        "1. Decision Requirement Field Value Decision Requirement ID DR-AUTH-001",
        "Authority evidence Evidence ID Description Source / custodian Collected at Integrity / reference Limitation EVD-AUTH-001",
        "Condition ID Condition Reason Owner Due date Verification Status COND-AUTH-001 Open / Satisfied / Waived by authorized owner / Failed",
        "8. Decision Record Field Value Authorization Decision ID DEC-AUTH-001",
        "9. RoE Handoff Handoff ID Input to RoE Acceptance criteria Actual status Reject / return condition Owner HO-AUTH-001 Decision Requirement Owner、期限、判断内容がある 抽象目的のみ",
        "10. Reassessment Field Value Reassessment ID REA-AUTH-001",
    ),
    "cases/ch02-authorization-decision-example.md": (
        "0. Document Control Field Value Artifact ID ART-13",
        "0. Document Control Field Value Authorization Record ID AUTH-CASE-2026-001",
        "0. Document Control Field Value Parent Case ID CASE-2026-001",
        "0. Document Control Field Value Relation refines",
        "1. Decision Requirement Field Value Decision Requirement ID DR-AUTH-2026-001",
        "Authority evidence Evidence ID Description Source / custodian Collected at Integrity / reference Limitation EVD-AUTH-2026-001 合成Tenantを対象とした設定Review承認 CTO / Ticket system 2026-08-05T10:15:00+09:00 SYNTH-EVD-AUTH-001 Production、外部API、実Credentialを含まない",
        "7. Conditions Condition ID Condition Reason Owner Due date Verification Status COND-AUTH-2026-001 Production credentialを操作しない 委託契約とAuthority未確認 Lab Operator Assessment終了まで Evidence / operation log Open",
        "8. Decision Record Field Value Authorization Decision ID DEC-AUTH-2026-001",
        "9. RoE Handoff Handoff ID Input to RoE Acceptance criteria Actual status Reject / return condition Owner HO-AUTH-2026-001 Decision Requirement Owner、期限、判断内容 Pass 抽象目的のみ CTO",
        "10. Reassessment Field Value Reassessment ID REA-AUTH-2026-001",
    ),
}

CHAPTER02_BOUNDED_HEADING_MEMBERS = {
    "manuscript/02-law-ethics-authorization.md": (
        (
            "本章の責任境界",
            "学習目標",
            ("OWN", "BRIDGE", "DELEGATE"),
        ),
        (
            "1. 四つのGate",
            "2. 法、契約、組織権限、倫理を分離する",
            (
                "1.1 Authority Gate",
                "1.2 Scope Gate",
                "1.3 Safety Gate",
                "1.4 Disclosure Gate",
            ),
        ),
    ),
    "templates/authorization-checklist.md": (),
    "cases/ch02-authorization-decision-example.md": (),
}

# Every Gate body is a finite canonical Layer A surface.  Exact first/last
# projected fields plus the visible field count reject an empty, truncated, or
# structurally relocated Gate without re-parsing Markdown in the chapter checker.
CHAPTER02_GATE_BODY_CONTRACT = {
    "manuscript/02-law-ethics-authorization.md": (
        (
            "1.1 Authority Gate",
            "1.2 Scope Gate",
            21,
            "1.1 Authority Gate Authority Gateは、誰がその操作を許可できるかを確認する。",
            "口頭了解やChatの一文だけでは、対象・期間・手法・Dataの境界が不明な場合がある。形式よりも、後から同じ範囲を再現できる具体性を重視する。",
        ),
        (
            "1.2 Scope Gate",
            "1.3 Safety Gate",
            11,
            "1.2 Scope Gate Scope Gateは、対象を技術的識別子へ変換する。",
            "ScopeはAsset inventoryと一致させる。対象外を明記し、DNSやRedirectで到達した別Domainを自動的に対象へ追加しない。",
        ),
        (
            "1.3 Safety Gate",
            "1.4 Disclosure Gate",
            13,
            "1.3 Safety Gate Safety Gateは、許可された操作の中から、判断に必要な最小操作を選ぶ。",
            "たとえば設定上の過大権限を示すには、実Dataを取得せず、設定Exportと業務要件の差分で十分な場合がある。影響確認が必要でも、合成Data、Canary object、Read-only queryを優先する。",
        ),
        (
            "1.4 Disclosure Gate",
            "2. 法、契約、組織権限、倫理を分離する",
            12,
            "1.4 Disclosure Gate Disclosure Gateは、発見情報の共有・調整・公開経路を事前に決める。",
            "届出や調整を行う場合、発見者、IPA / JPCERT/CC、製品開発者、ウェブサイト運営者等の役割を確認する。独自に公開時期を決める前に、現行の公式Guidelineと対象組織の窓口を確認する。SRC-IPA-VDP-001",
        ),
    ),
    "templates/authorization-checklist.md": (),
    "cases/ch02-authorization-decision-example.md": (),
}

EXPECTED_CHAPTER02_SOURCE_IDS = frozenset(
    {"SRC-JP-LAW-001", "SRC-IPA-VDP-001"}
)
EXPECTED_CHAPTER02_BODY_SOURCE_COUNTS = Counter(
    {"SRC-JP-LAW-001": 1, "SRC-IPA-VDP-001": 4}
)
EXPECTED_CHAPTER02_REFERENCE_SOURCE_COUNTS = Counter(
    {"SRC-JP-LAW-001": 1, "SRC-IPA-VDP-001": 1}
)


EXPECTED_CHAPTER02_PAGES = {
    (
        "manuscript/02-law-ethics-authorization.md",
        "chapters/chapter-02/index.md",
        "chapters",
        45,
    ),
    (
        "templates/authorization-checklist.md",
        "templates/authorization-checklist/index.md",
        "additional",
        232,
    ),
    (
        "cases/ch02-authorization-decision-example.md",
        "cases/chapter-02-authorization-decision/index.md",
        "additional",
        233,
    ),
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


def require_tokens(relative: str, text: str, tokens: tuple[str, ...]) -> None:
    for token in tokens:
        if token not in text:
            error(f"{relative}: missing required token {token!r}")


def chapter02_page_contract_errors(registry: dict, label: str) -> list[str]:
    messages: list[str] = []
    pages = registry.get("pages", [])
    if not isinstance(pages, list):
        return [f"{label}: pages must be an array"]

    actual_tuples = [
        (
            item.get("source"),
            item.get("destination"),
            item.get("section"),
            item.get("order"),
        )
        for item in pages
        if isinstance(item, dict)
    ]
    tuple_counts = Counter(actual_tuples)
    route_counts = Counter(item[:2] for item in actual_tuples)
    for expected in sorted(EXPECTED_CHAPTER02_PAGES):
        tuple_count = tuple_counts[expected]
        if tuple_count != 1:
            messages.append(
                f"{label}: expected Chapter 2 page tuple exactly once: "
                f"{expected!r}; found {tuple_count}"
            )
        route_count = route_counts[expected[:2]]
        if route_count != 1:
            messages.append(
                f"{label}: expected Chapter 2 source/destination exactly once: "
                f"{expected[:2]!r}; found {route_count}"
            )
    return messages


def registry_mutation_is_rejected(registry: dict, label: str) -> bool:
    try:
        parsed = parse_registry_data(registry, label)
    except SitePageRegistryError:
        return True
    return bool(chapter02_page_contract_errors(parsed, label))


def chapter02_heading_inventory_errors(
    document: ProjectedDocument,
    logical_path: str,
) -> list[str]:
    expected = EXPECTED_CHAPTER02_HEADINGS.get(logical_path)
    if expected is None:
        return [f"{logical_path}: is not a canonical Chapter 2 publication surface"]
    actual = tuple(
        (int(field.metadata_value("level")), field.text)
        for field in document.fields
        if field.field_type == "reader_visible_text"
        and field.element_kind == "heading"
        and isinstance(field.metadata_value("level"), int)
        and int(field.metadata_value("level")) <= 2
    )
    if actual == expected:
        return []
    return [
        f"{logical_path}: finite H1/H2 inventory drift; "
        f"expected {expected!r}, got {actual!r}"
    ]


def _field_identity(field) -> tuple[str, str, str | None, str]:
    """Return a document-scoped, relocation-stable Layer A identity."""

    return (
        field.field_type,
        field.element_kind,
        field.attribute,
        field.text,
    )


def _destination_relation(document: ProjectedDocument, field) -> tuple:
    """Bind a destination to its exact same-line projected reader owner."""

    owners = [
        candidate
        for candidate in document.fields
        if candidate.ordinal < field.ordinal
        and candidate.line == field.line
        and candidate.field_type
        in {
            "reader_visible_text",
            "reader_visible_attribute",
        }
    ]
    owner_identity = (
        _field_identity(max(owners, key=lambda item: item.ordinal)) if owners else None
    )
    return _field_identity(field), owner_identity


def _heading_path(document: ProjectedDocument, field) -> tuple[str, ...]:
    """Return the finite H1..H6 path preceding one projected field."""

    levels: dict[int, str] = {}
    for candidate in document.fields:
        if candidate.ordinal >= field.ordinal:
            break
        level = candidate.metadata_value("level")
        if (
            candidate.field_type != "reader_visible_text"
            or candidate.element_kind != "heading"
            or not isinstance(level, int)
            or not 1 <= level <= 6
        ):
            continue
        levels[level] = candidate.text
        for deeper in tuple(value for value in levels if value > level):
            del levels[deeper]
    return tuple(levels[level] for level in sorted(levels))


def _reviewed_text_relation(
    document: ProjectedDocument, field
) -> tuple[tuple[str, str, str | None, str], tuple[str, ...]]:
    return _field_identity(field), _heading_path(document, field)


def chapter02_semantic_projection_errors(
    document: ProjectedDocument,
    logical_path: str,
) -> list[str]:
    errors: list[str] = []
    actual = Counter(_field_identity(field) for field in document.fields)
    for identity in sorted(
        EXPECTED_CHAPTER02_SEMANTIC_FIELDS[logical_path], key=repr
    ):
        field_type, element_kind, attribute, text = identity
        matching = [
            field for field in document.fields if _field_identity(field) == identity
        ]
        if (
            actual[identity] != 1
            or field_type != "reader_visible_text"
            or attribute is not None
            or (
                element_kind == "heading"
                and (not matching or matching[0].metadata_value("level") != 3)
            )
        ):
            errors.append(
                f"{logical_path}: missing exact semantic projection field "
                f"{identity!r}; count={actual[identity]}"
            )

    identities_by_text = {
        identity[3]: identity
        for identity in EXPECTED_CHAPTER02_SEMANTIC_FIELDS[logical_path]
    }
    ordered_fields = []
    for text in EXPECTED_CHAPTER02_SEMANTIC_ORDER[logical_path]:
        identity = identities_by_text[text]
        matches = [
            field for field in document.fields if _field_identity(field) == identity
        ]
        if len(matches) == 1:
            ordered_fields.append(matches[0])
    if len(ordered_fields) == len(EXPECTED_CHAPTER02_SEMANTIC_ORDER[logical_path]):
        ordinals = tuple(field.ordinal for field in ordered_fields)
        if ordinals != tuple(sorted(ordinals)):
            errors.append(
                f"{logical_path}: exact semantic projection field order changed; "
                f"locations={tuple(field.location for field in ordered_fields)!r}"
            )

    headings = [
        field
        for field in document.fields
        if field.field_type == "reader_visible_text" and field.element_kind == "heading"
    ]
    for parent_text, next_text, member_texts in CHAPTER02_BOUNDED_HEADING_MEMBERS[
        logical_path
    ]:
        parents = [
            field
            for field in headings
            if field.text == parent_text and field.metadata_value("level") == 2
        ]
        following = [
            field
            for field in headings
            if field.text == next_text and field.metadata_value("level") == 2
        ]
        if len(parents) != 1 or len(following) != 1:
            # The finite H1/H2 inventory reports the detailed parent error.
            continue
        for member_text in member_texts:
            members = [
                field
                for field in headings
                if field.text == member_text and field.metadata_value("level") == 3
            ]
            if (
                len(members) != 1
                or not parents[0].ordinal < members[0].ordinal < following[0].ordinal
            ):
                errors.append(
                    f"{logical_path}: semantic heading {member_text!r} left "
                    f"bounded section {parent_text!r}"
                )

    for parent_text, next_text, expected_count, first_text, last_text in (
        CHAPTER02_GATE_BODY_CONTRACT[logical_path]
    ):
        parents = [field for field in headings if field.text == parent_text]
        following = [field for field in headings if field.text == next_text]
        if len(parents) != 1 or len(following) != 1:
            continue
        body_fields = [
            field
            for field in document.fields
            if parents[0].ordinal < field.ordinal < following[0].ordinal
            and is_policy_scan_field(field)
        ]
        actual_first = body_fields[0].text if body_fields else None
        actual_last = body_fields[-1].text if body_fields else None
        if (
            len(body_fields) != expected_count
            or actual_first != first_text
            or actual_last != last_text
        ):
            errors.append(
                f"{logical_path}: Gate body projection contract drift for "
                f"{parent_text!r}; count={len(body_fields)}, "
                f"first={actual_first!r}, last={actual_last!r}"
            )

    actual_text_relations = Counter(
        _reviewed_text_relation(document, field)
        for field in document.fields
        if is_policy_scan_field(field)
    )
    for relation in sorted(
        CHAPTER02_RESPONSIBILITY_BOUNDARY_RELATIONS[logical_path], key=repr
    ):
        if actual_text_relations[relation] != 1:
            errors.append(
                f"{logical_path}: responsibility boundary projection relation "
                f"must exist exactly once: {relation!r}; "
                f"count={actual_text_relations[relation]}"
            )
    exemption_sets = (
        ("action", CHAPTER02_REVIEWED_ACTION_RELATIONS[logical_path]),
        ("host", CHAPTER02_REVIEWED_HOST_RELATIONS[logical_path]),
    )
    for owner, relations in exemption_sets:
        for relation in sorted(relations, key=repr):
            if actual_text_relations[relation] != 1:
                errors.append(
                    f"{logical_path}: reviewed {owner} projection relation must "
                    f"exist exactly once: {relation!r}; "
                    f"count={actual_text_relations[relation]}"
                )
    actual_relations = Counter(
        _destination_relation(document, field)
        for field in document.fields
        if field.field_type == "destination"
    )
    for relation in sorted(
        CHAPTER02_REVIEWED_PROVENANCE_RELATIONS[logical_path], key=repr
    ):
        if actual_relations[relation] != 1:
            errors.append(
                f"{logical_path}: reviewed provenance projection relation must "
                f"exist exactly once: {relation!r}; count={actual_relations[relation]}"
            )

    if logical_path == "manuscript/02-law-ethics-authorization.md":
        reference_headings = [
            field
            for field in headings
            if field.text == "参考文献・Source Note ID"
            and field.metadata_value("level") == 2
        ]
        if len(reference_headings) == 1:
            source_pattern = re.compile(r"\bSRC-[A-Z0-9-]+\b")
            visible_fields = [
                field for field in document.fields if is_policy_scan_field(field)
            ]
            body_source_counts = Counter(
                match.group(0)
                for field in visible_fields
                if field.ordinal < reference_headings[0].ordinal
                for match in source_pattern.finditer(field.text)
            )
            reference_source_counts = Counter(
                match.group(0)
                for field in visible_fields
                if field.ordinal > reference_headings[0].ordinal
                for match in source_pattern.finditer(field.text)
            )
            if body_source_counts != EXPECTED_CHAPTER02_BODY_SOURCE_COUNTS:
                errors.append(
                    f"{logical_path}: projected body source ID counts drift; "
                    f"expected={EXPECTED_CHAPTER02_BODY_SOURCE_COUNTS!r}, "
                    f"actual={body_source_counts!r}"
                )
            if (
                reference_source_counts
                != EXPECTED_CHAPTER02_REFERENCE_SOURCE_COUNTS
            ):
                errors.append(
                    f"{logical_path}: projected reference source ID counts drift; "
                    f"expected={EXPECTED_CHAPTER02_REFERENCE_SOURCE_COUNTS!r}, "
                    f"actual={reference_source_counts!r}"
                )
    return errors


def _projection_document_findings(
    document: ProjectedDocument,
    logical_path: str,
) -> list[SafetyFinding]:
    findings: list[SafetyFinding] = []
    reviewed_actions = CHAPTER02_REVIEWED_ACTION_RELATIONS[logical_path]
    reviewed_hosts = CHAPTER02_REVIEWED_HOST_RELATIONS[logical_path]
    reviewed_provenance = CHAPTER02_REVIEWED_PROVENANCE_RELATIONS[logical_path]
    text_relation_counts = Counter(
        _reviewed_text_relation(document, candidate)
        for candidate in document.fields
        if is_policy_scan_field(candidate)
    )
    relation_counts = Counter(
        _destination_relation(document, candidate)
        for candidate in document.fields
        if candidate.field_type == "destination"
    )

    for field in document.fields:
        if is_policy_scan_field(field):
            relation = _reviewed_text_relation(document, field)
            if relation not in reviewed_actions or text_relation_counts[relation] != 1:
                findings.extend(
                    scan_action_text(field.normalized_text, location=field.location)
                )
            if relation not in reviewed_hosts or text_relation_counts[relation] != 1:
                findings.extend(
                    scan_host_policy(field.normalized_text, location=field.location)
                )
        elif field.field_type == "destination":
            relation = _destination_relation(document, field)
            if is_absolute_destination(field.normalized_text) and (
                relation not in reviewed_provenance or relation_counts[relation] != 1
            ):
                findings.extend(
                    scan_host_policy(field.normalized_text, location=field.location)
                )
    return sorted(
        set(findings),
        key=lambda item: (
            item.location,
            item.category,
            item.normalized_excerpt,
            item.reason,
            item.policy_version,
        ),
    )


def chapter02_policy_findings(
    documents: dict[str, str],
) -> tuple[list[SafetyFinding], list[str]]:
    """Run the thin Chapter 2 Layer A → shared Layer B → Layer C flow."""

    if tuple(documents) != CHAPTER02_DOCUMENTS:
        return [], [
            "Chapter 2 publication surface must contain the three canonical "
            f"documents in order: {CHAPTER02_DOCUMENTS!r}"
        ]
    try:
        projection = project_documents(documents)
    except (ProjectionRuntimeError, TypeError, ValueError) as exc:
        return [], [f"shared Publication Projection failed closed: {exc}"]

    errors = [
        f"{diagnostic.location}: {diagnostic.code} "
        f"{diagnostic.kind}: {diagnostic.reason}"
        for diagnostic in projection.diagnostics
    ]
    findings: list[SafetyFinding] = []
    for document, logical_path in zip(
        projection.documents,
        CHAPTER02_DOCUMENTS,
        strict=True,
    ):
        errors.extend(chapter02_heading_inventory_errors(document, logical_path))
        errors.extend(chapter02_semantic_projection_errors(document, logical_path))
        findings.extend(_projection_document_findings(document, logical_path))
    return sorted(
        set(findings),
        key=lambda item: (
            item.location,
            item.category,
            item.normalized_excerpt,
            item.reason,
            item.policy_version,
        ),
    ), errors


def format_policy_finding(finding: SafetyFinding) -> str:
    return (
        f"{finding.location}: [{finding.category}] {finding.reason}; "
        f"excerpt={finding.normalized_excerpt!r}; Policy {finding.policy_version}"
    )


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"{label}: expected one anchor {old!r}")
    return text.replace(old, new, 1)


SELECTION_FIXTURE_IDS = (
    "CH02-SEL-001",
    "CH02-SEL-003",
    "CH02-SEL-004",
    "CH02-SEL-005",
    "CH02-SEL-025",
    "CH02-SEL-040",
    "CH02-SEL-048",
    "CH02-SEL-059",
    "CH02-SEL-071",
    "CH02-SEL-072",
)


def _selection_fixture_documents(
    fixture_id: str,
    canonical: dict[str, str],
) -> tuple[dict[str, str], str]:
    documents = dict(canonical)
    chapter_path, template_path, case_path = CHAPTER02_DOCUMENTS
    if fixture_id == "CH02-SEL-001":
        documents[case_path] = replace_once(
            documents[case_path],
            "# 第2章 合成記入例：OAuth連携評価前のAuthorization判断",
            "# 第2章 合成記入例：OAuth連携評価前のAuthorization判断\n\nhttps://example.com/runbook",
            fixture_id,
        )
        return documents, "finding:network.host_or_address"
    if fixture_id == "CH02-SEL-003":
        documents[template_path] += (
            "\n## Unclassified trailing operational section\n\n"
            "第三者の本番APIへ接続する\n"
        )
        return documents, "inventory"
    if fixture_id == "CH02-SEL-004":
        documents[chapter_path] = replace_once(
            documents[chapter_path],
            "# 第2章　法、倫理、許可、責任ある開示",
            "# 第2章　法、倫理、許可、責任ある開示\n\nhttps://example.com/runbook",
            fixture_id,
        )
        return documents, "finding:network.host_or_address"
    if fixture_id == "CH02-SEL-005":
        documents[chapter_path] += "\n第三者の本番APIへ接続する\n"
        return documents, "finding:target.real_or_external"
    if fixture_id == "CH02-SEL-025":
        documents[template_path] = replace_once(
            documents[template_path],
            "# Authorization Checklist",
            "# Authorization Checklist\n\n```text\n## Unclassified operational section\n```",
            fixture_id,
        )
        return documents, "accepted-code-heading"
    if fixture_id == "CH02-SEL-040":
        documents[template_path] = replace_once(
            documents[template_path],
            "## 3. Scope Gate",
            "Unclassified operational section\n---\n\n## 3. Scope Gate",
            fixture_id,
        )
        return documents, "inventory"
    if fixture_id == "CH02-SEL-048":
        documents[template_path] = replace_once(
            documents[template_path],
            "## 3. Scope Gate",
            "  ## Unclassified operational section\n\n## 3. Scope Gate",
            fixture_id,
        )
        return documents, "accepted-indented-nonheading"
    if fixture_id == "CH02-SEL-059":
        documents[case_path] = replace_once(
            documents[case_path],
            "# 第2章 合成記入例：OAuth連携評価前のAuthorization判断",
            "# 第2章 合成記入例：OAuth連携評価前のAuthorization判断\n\n## Unclassified operational section",
            fixture_id,
        )
        return documents, "inventory"
    if fixture_id == "CH02-SEL-071":
        documents[template_path] += "\n実Credentialを取得しない。\n"
        return documents, "accepted-safe-counterpart"
    if fixture_id == "CH02-SEL-072":
        documents[template_path] += "\n個人情報の収集リスクを分析する。\n"
        return documents, "accepted-bounded-explanation"
    raise ValueError(f"unknown Chapter 2 selection fixture: {fixture_id}")


def run_selection_fixture(
    fixture_id: str,
    canonical: dict[str, str],
) -> tuple[bool, str]:
    documents, expectation = _selection_fixture_documents(fixture_id, canonical)
    findings, selection_errors = chapter02_policy_findings(documents)
    if expectation.startswith("finding:"):
        category = expectation.split(":", 1)[1]
        passed = any(item.category == category for item in findings)
    elif expectation == "inventory":
        passed = any(
            "finite H1/H2 inventory drift" in item for item in selection_errors
        )
    elif expectation.startswith("accepted-"):
        passed = not findings and not selection_errors
    else:
        raise AssertionError(expectation)
    summary = (
        f"{fixture_id}: expectation={expectation}; "
        f"findings={[item.category for item in findings]!r}; errors={selection_errors!r}"
    )
    return passed, summary


def verify_chapter02_adapter(
    chapter: str,
    template: str,
    example: str,
) -> None:
    canonical = dict(
        zip(CHAPTER02_DOCUMENTS, (chapter, template, example), strict=True)
    )
    findings, selection_errors = chapter02_policy_findings(canonical)
    for message in selection_errors:
        error(message)
    for finding in findings:
        error(format_policy_finding(finding))

    for fixture_id in SELECTION_FIXTURE_IDS:
        passed, summary = run_selection_fixture(fixture_id, canonical)
        if not passed:
            error(f"Chapter 2 selection regression failed: {summary}")

    direct_mutations = (
        ("target.real_or_external", "| Allowed methods | 第三者の本番APIへ接続する |"),
        ("secret.credential", "| Allowed methods | 実Credentialを取得する |"),
        ("data.pii", "| Allowed methods | 個人情報を収集する |"),
        ("operation.malware", "| Allowed methods | keyloggerを作る |"),
    )
    for category, mutation in direct_mutations:
        mutated = replace_once(
            template,
            "| Allowed methods |  |",
            mutation,
            f"Chapter 2 direct {category}",
        )
        try:
            document = project_documents(
                {"templates/authorization-checklist.md": mutated}
            ).document("templates/authorization-checklist.md")
        except (ProjectionRuntimeError, TypeError, ValueError) as exc:
            error(f"Chapter 2 direct mutation projection failed closed: {exc}")
            continue
        mutation_findings = _projection_document_findings(
            document, "templates/authorization-checklist.md"
        )
        if not any(item.category == category for item in mutation_findings):
            error(
                "Chapter 2 direct unsafe mutation bypassed shared "
                f"projection/Policy: {category}"
            )

    safe_mutations = (
        "第三者の本番APIへ接続しない",
        "Tokenを取得しない",
        "個人情報の収集リスクを分析する",
        "keyloggerを作ることを禁止する",
    )
    safe_block = "\n".join(f"- {text}" for text in safe_mutations)
    safe_source = replace_once(
        template,
        "- `Proceed with conditions`では、Condition、Owner、期限、再確認方法を必須とする。",
        "- `Proceed with conditions`では、Condition、Owner、期限、再確認方法を必須とする。\n"
        + safe_block,
        "Chapter 2 safe counterparts",
    )
    try:
        safe_document = project_documents(
            {"templates/authorization-checklist.md": safe_source}
        ).document("templates/authorization-checklist.md")
    except (ProjectionRuntimeError, TypeError, ValueError) as exc:
        error(f"Chapter 2 safe mutation projection failed closed: {exc}")
    else:
        safe_findings = _projection_document_findings(
            safe_document, "templates/authorization-checklist.md"
        )
        if safe_findings:
            error(
                "Chapter 2 safe counterparts produced findings: "
                f"{[format_policy_finding(item) for item in safe_findings]!r}"
            )

    reviewed_action_mutation = replace_once(
        example,
        "| Information gaps | Production credential変更権限、実Vendor窓口、契約通知期限 |",
        "| Information gaps | Production credential変更権限、実Vendor窓口、契約通知期限。"
        "しかし実Credentialを取得する |",
        "Chapter 2 reviewed action mutation",
    )
    provenance_mutation = replace_once(
        chapter,
        "https://itdojp.github.io/pentest-learning-book/",
        "https://example.com/runbook",
        "Chapter 2 reviewed provenance mutation",
    )
    host_mutation = replace_once(
        example,
        "`billing-bridge.example`の合成App registration",
        "`lab.localhost`の合成App registration",
        "Chapter 2 Issue #67 exact host exemption mutation",
    )
    exemption_probes = (
        (
            "cases/ch02-authorization-decision-example.md",
            reviewed_action_mutation,
            "secret.credential",
            "L160",
            "reviewed action",
        ),
        (
            "manuscript/02-law-ethics-authorization.md",
            provenance_mutation,
            "network.host_or_address",
            "L41",
            "reviewed provenance",
        ),
        (
            "cases/ch02-authorization-decision-example.md",
            host_mutation,
            "network.host_or_address",
            "L83",
            "Issue #67 host",
        ),
    )
    for logical_path, source, category, line_marker, label in exemption_probes:
        try:
            document = project_documents({logical_path: source}).document(logical_path)
        except (ProjectionRuntimeError, TypeError, ValueError) as exc:
            error(f"Chapter 2 exact {label} mutation projection failed: {exc}")
            continue
        probe_findings = _projection_document_findings(document, logical_path)
        if not any(
            item.category == category and line_marker in item.location
            for item in probe_findings
        ):
            error(f"Chapter 2 exact {label} exemption survived its field mutation")

    relocated_provenance = replace_once(
        chapter,
        "https://itdojp.github.io/pentest-learning-book/",
        "../safe-local-reference",
        "Chapter 2 reviewed provenance relocation source",
    ) + (
        "\nOperational target: [target]"
        "(https://itdojp.github.io/pentest-learning-book/)\n"
    )
    relocated_document = project_documents(
        {"manuscript/02-law-ethics-authorization.md": relocated_provenance}
    ).document("manuscript/02-law-ethics-authorization.md")
    relocated_findings = _projection_document_findings(
        relocated_document, "manuscript/02-law-ethics-authorization.md"
    )
    relocated_errors = chapter02_semantic_projection_errors(
        relocated_document, "manuscript/02-law-ethics-authorization.md"
    )
    if not any(
        item.category == "network.host_or_address" for item in relocated_findings
    ) or not any(
        "reviewed provenance projection relation" in item for item in relocated_errors
    ):
        error("Chapter 2 provenance exemption followed a URL into a new owner")

    duplicate_host = replace_once(
        example,
        "- Domainは予約済みの`.example`を使用する。",
        "- Domainは予約済みの`.example`を使用する。\n"
        "- Domainは予約済みの`.example`を使用する。",
        "Chapter 2 exact host exemption duplicate",
    )
    duplicate_document = project_documents(
        {"cases/ch02-authorization-decision-example.md": duplicate_host}
    ).document("cases/ch02-authorization-decision-example.md")
    duplicate_findings = _projection_document_findings(
        duplicate_document, "cases/ch02-authorization-decision-example.md"
    )
    if not any(
        item.category == "network.host_or_address" for item in duplicate_findings
    ):
        error("Chapter 2 host exemption expanded to an unreviewed duplicate location")

    ownership_mutation = replace_once(
        chapter, "### OWN", "`### OWN`", "Chapter 2 OWN semantic mutation"
    )
    _, ownership_errors = chapter02_policy_findings(
        {
            "manuscript/02-law-ethics-authorization.md": ownership_mutation,
            "templates/authorization-checklist.md": template,
            "cases/ch02-authorization-decision-example.md": example,
        }
    )
    if not any(
        "missing exact semantic projection field" in item for item in ownership_errors
    ):
        error("Chapter 2 OWN raw token satisfied the projected semantic contract")

    relocated_ownership = (
        replace_once(
            chapter,
            "### OWN\n",
            "",
            "Chapter 2 OWN bounded-section relocation source",
        )
        + "\n### OWN\n"
    )
    _, relocation_errors = chapter02_policy_findings(
        {
            "manuscript/02-law-ethics-authorization.md": relocated_ownership,
            "templates/authorization-checklist.md": template,
            "cases/ch02-authorization-decision-example.md": example,
        }
    )
    if not any(
        "semantic heading 'OWN' left bounded section" in item
        for item in relocation_errors
    ):
        error("Chapter 2 OWN relocation preserved the bounded semantic contract")

    responsibility_paragraph = (
        "本書は、実務上のAuthorization Gateと後続工程へのHandoffに責任を持つ。"
        "本章は法的助言を提供せず、個別事案の法的判断と法令解釈は専門家へ委譲する。"
        "専門領域の詳細は委譲先に残すが、委譲先へのリンクを読まなくても、"
        "第2章の論旨と運用判断は単独で成立する。"
    )
    legal_delegate = (
        "- 個別事案の法的助言と法令解釈は、適格な法務・契約専門家へ委譲する"
    )
    responsibility_mutations = (
        (
            "responsibility paragraph",
            responsibility_paragraph,
        ),
        (
            "legal DELEGATE item",
            legal_delegate,
        ),
    )
    for label, source_owner in responsibility_mutations:
        relocated_to_code = replace_once(
            chapter,
            source_owner + "\n",
            "",
            f"Chapter 2 {label} code relocation",
        ) + f"\n```text\n{source_owner}\n```\n"
        _, responsibility_errors = chapter02_policy_findings(
            {
                "manuscript/02-law-ethics-authorization.md": relocated_to_code,
                "templates/authorization-checklist.md": template,
                "cases/ch02-authorization-decision-example.md": example,
            }
        )
        if not any(
            "responsibility boundary projection relation" in item
            for item in responsibility_errors
        ) or not any(
            "missing exact semantic projection field" in item
            for item in responsibility_errors
        ):
            error(
                f"Chapter 2 {label} code literal satisfied the responsibility boundary"
            )

    artifact_mutation = (
        replace_once(
            template,
            "| Artifact ID | `ART-13` |",
            "| Identifier | NONE |",
            "Chapter 2 ART-13 semantic mutation",
        )
        + "\n```text\n| Artifact ID | `ART-13` |\n```\n"
    )
    _, artifact_errors = chapter02_policy_findings(
        {
            "manuscript/02-law-ethics-authorization.md": chapter,
            "templates/authorization-checklist.md": artifact_mutation,
            "cases/ch02-authorization-decision-example.md": example,
        }
    )
    if not any(
        "missing exact semantic projection field" in item for item in artifact_errors
    ):
        error("Chapter 2 ART-13 code literal satisfied the projected table contract")

    gate_start = chapter.index("### 1.1 Authority Gate")
    gate_body_start = chapter.index("\n", gate_start) + 1
    next_gate_start = chapter.index("### 1.2 Scope Gate", gate_body_start)
    empty_authority_gate = (
        chapter[:gate_body_start] + "\n" + chapter[next_gate_start:]
    )
    _, gate_errors = chapter02_policy_findings(
        {
            "manuscript/02-law-ethics-authorization.md": empty_authority_gate,
            "templates/authorization-checklist.md": template,
            "cases/ch02-authorization-decision-example.md": example,
        }
    )
    if not any("Gate body projection contract drift" in item for item in gate_errors):
        error("Chapter 2 empty Authority Gate body satisfied the finite surface")

    major_id_mutations = (
        (
            "Authorization Record ID",
            "| Authorization Record ID | `AUTH-CASE-2026-001` |",
            "| Authorization Record ID | NONE |",
        ),
        (
            "Decision Requirement ID",
            "| Decision Requirement ID | `DR-AUTH-2026-001` |",
            "| Decision Requirement ID | NONE |",
        ),
    )
    for label, source_row, replacement_row in major_id_mutations:
        mutated_example = replace_once(
            example,
            source_row,
            replacement_row,
            f"Chapter 2 {label} semantic mutation",
        ) + f"\n```text\n{source_row}\n```\n"
        _, identifier_errors = chapter02_policy_findings(
            {
                "manuscript/02-law-ethics-authorization.md": chapter,
                "templates/authorization-checklist.md": template,
                "cases/ch02-authorization-decision-example.md": mutated_example,
            }
        )
        if not any(
            "missing exact semantic projection field" in item
            for item in identifier_errors
        ):
            error(f"Chapter 2 {label} code literal satisfied its table contract")

    reference_marker = chapter.index("## 参考文献・Source Note ID")
    source_id_body = replace_once(
            chapter[:reference_marker],
            "`SRC-JP-LAW-001`",
            "`SOURCE-ID-REMOVED`",
            "Chapter 2 projected source ID removal",
        ) + chapter[reference_marker:]
    hidden_source_id = replace_once(
        source_id_body,
        "\n---\n\n# 第2章",
        "\nsource-id: SRC-JP-LAW-001\n---\n\n# 第2章",
        "Chapter 2 hidden source ID insertion",
    )
    _, source_id_errors = chapter02_policy_findings(
        {
            "manuscript/02-law-ethics-authorization.md": hidden_source_id,
            "templates/authorization-checklist.md": template,
            "cases/ch02-authorization-decision-example.md": example,
        }
    )
    if not any(
        "projected body source ID counts drift" in item
        for item in source_id_errors
    ):
        error("Chapter 2 hidden metadata satisfied a reader-visible source ID")

    action_owner = (
        "一つの層がPassしても、他の層を自動的にPassさせない。たとえば契約にSecurity "
        "testingの記載があっても、第三者Tenantや実利用者Dataまで対象になるとは限らない。"
    )
    action_relocation = replace_once(
        chapter,
        action_owner + "\n",
        "",
        "Chapter 2 action relation relocation",
    ) + f"\n{action_owner}\n"
    action_duplicate = replace_once(
        chapter,
        action_owner,
        action_owner + "\n\n" + action_owner,
        "Chapter 2 action relation duplicate",
    )
    host_owner = "- Domainは予約済みの`.example`を使用する。"
    host_relocation = replace_once(
        example,
        host_owner + "\n",
        "",
        "Chapter 2 host relation relocation",
    ) + f"\n{host_owner}\n"
    provenance_owner = (
        "- 詳細な攻撃技法と脆弱性の悪用は、許可済み評価の専門的な方法、成果物、安全境界を詳述する"
        "[実務で使えるペネトレーションテスト大全]"
        "(https://itdojp.github.io/pentest-learning-book/)へ委譲する"
    )
    provenance_duplicate = replace_once(
        chapter,
        provenance_owner,
        provenance_owner + "\n" + provenance_owner,
        "Chapter 2 provenance relation duplicate",
    )
    relation_mutations = (
        (
            "action relocation",
            "manuscript/02-law-ethics-authorization.md",
            action_relocation,
            "reviewed action projection relation",
            "target.real_or_external",
        ),
        (
            "action duplicate",
            "manuscript/02-law-ethics-authorization.md",
            action_duplicate,
            "reviewed action projection relation",
            "target.real_or_external",
        ),
        (
            "host relocation",
            "cases/ch02-authorization-decision-example.md",
            host_relocation,
            "reviewed host projection relation",
            "network.host_or_address",
        ),
        (
            "provenance duplicate",
            "manuscript/02-law-ethics-authorization.md",
            provenance_duplicate,
            "reviewed provenance projection relation",
            "network.host_or_address",
        ),
    )
    for label, logical_path, source, error_marker, category in relation_mutations:
        relation_document = project_documents({logical_path: source}).document(
            logical_path
        )
        relation_errors = chapter02_semantic_projection_errors(
            relation_document, logical_path
        )
        relation_findings = _projection_document_findings(
            relation_document, logical_path
        )
        if not any(error_marker in item for item in relation_errors) or not any(
            item.category == category for item in relation_findings
        ):
            error(
                f"Chapter 2 reviewed {label} retained an expandable exemption"
            )

    delegated = {
        relation[0][3]
        for relation in CHAPTER02_REVIEWED_PROVENANCE_RELATIONS[
            "manuscript/02-law-ethics-authorization.md"
        ]
    }
    canonical_projection = project_documents(canonical)
    projected_destinations = {
        field.text
        for field in destination_fields(canonical_projection)
        if field.document_id == "manuscript/02-law-ethics-authorization.md"
    }
    if not delegated <= projected_destinations:
        error(
            "Chapter 2 shared projection omitted reviewed DELEGATE destinations: "
            f"{sorted(delegated - projected_destinations)!r}"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the Chapter 2 contract")
    parser.add_argument("--selection-fixture", choices=SELECTION_FIXTURE_IDS)
    args = parser.parse_args(argv)

    required_files = (
        "manuscript/02-law-ethics-authorization.md",
        "templates/authorization-checklist.md",
        "cases/ch02-authorization-decision-example.md",
        "scripts/check_chapter02_contract.py",
        "scripts/publication_projection.py",
        "scripts/_publication_projection_renderer.rb",
        "scripts/check_publication_projection.py",
        "tests/fixtures/publication-projection/corpus.json",
        "adr/0002-publication-projection-owner.md",
        "CONTENT_SAFETY_POLICY_MIGRATION.md",
        "site-pages.json",
        "artifact-index.md",
        "figure-index.md",
        "glossary.md",
        "cases/index.md",
        "index.md",
        "book-config.json",
        "references/sources.json",
        "references/reference-baseline.md",
        "references/ch02-source-review-2026-08-05.md",
        "package.json",
    )
    for relative in required_files:
        if not (ROOT / relative).is_file():
            error(f"missing required file: {relative}")

    if CONTENT_SAFETY_POLICY_VERSION != EXPECTED_CONTENT_SAFETY_POLICY_VERSION:
        error(
            "Chapter 2 Content Safety Policy pin changed: "
            f"{CONTENT_SAFETY_POLICY_VERSION!r} != {EXPECTED_CONTENT_SAFETY_POLICY_VERSION!r}"
        )
    if PROJECTION_VERSION != EXPECTED_PUBLICATION_PROJECTION_VERSION:
        error(
            "Chapter 2 Publication Projection pin changed: "
            f"{PROJECTION_VERSION!r} != {EXPECTED_PUBLICATION_PROJECTION_VERSION!r}"
        )

    if args.selection_fixture:
        canonical = {path: read_text(path) for path in CHAPTER02_DOCUMENTS}
        passed, summary = run_selection_fixture(args.selection_fixture, canonical)
        print(("PASS: " if passed else "ERROR: ") + summary)
        return 0 if passed else 1

    config = load_json("book-config.json")
    chapters = config.get("structure", {}).get("chapters", [])
    chapter_config = next(
        (
            item
            for item in chapters
            if isinstance(item, dict)
            and item.get("id") == "ch02-law-ethics-authorization"
        ),
        None,
    )
    expected_objectives = [
        "許可とスコープを文書化できる",
        "停止条件を定義できる",
        "責任ある開示の流れを説明できる",
    ]
    if chapter_config is None:
        error("book-config.json: missing ch02-law-ethics-authorization")
    elif chapter_config.get("objectives") != expected_objectives:
        error("book-config.json: chapter 2 learning objectives changed unexpectedly")

    chapter_path = "manuscript/02-law-ethics-authorization.md"
    chapter = read_text(chapter_path)
    require_tokens(
        chapter_path,
        chapter,
        (
            "## この章の位置付け",
            "## 学習目標",
            "## 前提知識",
            "## 導入ケース",
            "Authority Gate",
            "Scope Gate",
            "Safety Gate",
            "Disclosure Gate",
            "F-02-01",
            "T-02-01",
            "書面による許可",
            "Data、Secret、証拠の取扱い",
            "委託、再委託、Cloud / SaaS",
            "脆弱性を発見したとき",
            "Stop condition",
            "Cleanup",
            "## 7. 四つの視点",
            "## 8. Handoff Contract",
            "## 9. 安全な演習",
            "ART-13 Authorization Checklist",
            "## 11. 評価基準",
            "## 12. よくある誤解",
            "## 章のまとめ",
            "## 次に学ぶこと",
            "## 参考文献・Source Note ID",
            "SRC-JP-LAW-001",
            "SRC-IPA-VDP-001",
            "Proceed with conditions",
            "Do not proceed",
            "Escalate",
            "## 本章の責任境界",
            "### OWN",
            "### BRIDGE",
            "### DELEGATE",
            "本書は、実務上のAuthorization Gateと後続工程へのHandoffに責任を持つ。",
            "本章は法的助言を提供せず、個別事案の法的判断と法令解釈は専門家へ委譲する。",
            "委譲先へのリンクを読まなくても、第2章の論旨と運用判断は単独で成立する。",
            "個別事案の法的助言と法令解釈は、適格な法務・契約専門家へ委譲する",
            "第8章の安全なLabとEvidence取扱い",
            "第9章のRules of Engagement",
            "第10章のReconnaissance / OSINT境界",
            "第15章のFinding、Remediation、Retest、Responsible Disclosure",
            "第19章のIncidentとPersonal Data対応",
            (
                "詳細な攻撃技法と脆弱性の悪用は、許可済み評価の専門的な方法、"
                "成果物、安全境界を詳述する[実務で使えるペネトレーションテスト大全]"
                "(https://itdojp.github.io/pentest-learning-book/)へ委譲する"
            ),
            (
                "認証・認可Protocol内部と安全な実装は、OAuth、OIDC、SAML等の設計と"
                "実装を詳述する[実践 認証認可システム設計]"
                "(https://itdojp.github.io/practical-auth-book/)へ委譲する"
            ),
            (
                "Infrastructure Hardeningと防御実装は、Network、OS、Cloud、Containerの"
                "Security実装を詳述する[インフラエンジニアのための情報セキュリティ実装ガイド]"
                "(https://itdojp.github.io/it-infra-security-guide-book/)へ委譲する"
            ),
        ),
    )
    if re.search(r"https://github\.com/[^\s)]+/blob/main(?:/|\b)", chapter):
        error(
            f"{chapter_path}: mutable GitHub blob/main URL must not be used as a "
            "delegated publication target"
        )
    for forbidden in (
        "善意の研究であれば明示的な許可は不要である。",
        "管理者権限があれば業務上の承認も不要である。",
        "脆弱性を発見したら影響を最大まで実証する。",
        "届出後は関係者との調整を待たず公開する。",
    ):
        if forbidden in chapter:
            error(f"{chapter_path}: unsafe or unsupported assertion {forbidden!r}")

    # Exact body/reference occurrence checks run over Layer B reader-visible
    # fields in chapter02_semantic_projection_errors(). Hidden front matter and
    # source-only code cannot satisfy the Chapter 2 citation contract.
    expected_source_ids = EXPECTED_CHAPTER02_SOURCE_IDS

    template_path = "templates/authorization-checklist.md"
    template = read_text(template_path)
    require_tokens(
        template_path,
        template,
        (
            "Artifact ID | `ART-13`",
            "Authorization Record ID",
            "Parent Case ID",
            "Relation | `refines` / `supersedes` / `independent`",
            "Decision Requirement ID",
            "Available decisions | Proceed / Proceed with conditions / Do not proceed / Escalate",
            "## 2. Authority Gate",
            "## 3. Scope Gate",
            "## 4. Safety Gate",
            "## 5. Disclosure Gate",
            "Authority evidence",
            "Legal, Contractual, and Policy Questions",
            "Conditions",
            "Decision Record",
            "RoE Handoff",
            "Reassessment",
            "Traceability Check",
            "Technical correctness",
            "Safety / authorization",
            "Legal / contractual source quality",
            "Evidence / traceability",
            "Decision usefulness",
        ),
    )

    example_path = "cases/ch02-authorization-decision-example.md"
    example = read_text(example_path)
    require_tokens(
        example_path,
        example,
        (
            "ART-13",
            "AUTH-CASE-2026-001",
            "CASE-2026-001",
            "| Relation | `refines` |",
            "DR-AUTH-2026-001",
            "EVD-AUTH-2026-001",
            "COND-AUTH-2026-001",
            "DEC-AUTH-2026-001",
            "HO-AUTH-2026-001",
            "REA-AUTH-2026-001",
            "Proceed with conditions",
            "tenant-auth-lab-01.test",
            "billing-bridge.example",
            "Production credentialを操作しない",
            "外部Networkをdefault denyにする",
            "想定外脆弱性発見時は直ちに停止する",
            "この表は合成Case内の記入例であり、実際の章Gateまたは法的承認の証跡ではない。",
            "SYNTH-REV-AUTH-TECH-001",
            "SYNTH-REV-AUTH-SAFE-001",
            "SYNTH-REV-AUTH-LAW-001",
            "SYNTH-REV-AUTH-EVD-001",
            "SYNTH-REV-AUTH-DEC-001",
        ),
    )
    verify_chapter02_adapter(chapter, template, example)

    secret_patterns = (
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
        re.compile(
            r"(?i)(?:password|api[_-]?key|secret|token)\s*[:=]\s*[A-Za-z0-9+/=_-]{16,}"
        ),
    )
    for pattern in secret_patterns:
        if pattern.search(example):
            error(
                f"{example_path}: possible real credential or secret pattern detected"
            )

    raw_registry = load_json("site-pages.json")
    try:
        registry = parse_registry_data(raw_registry)
    except SitePageRegistryError as exc:
        error(f"site-pages.json: invalid registry: {exc}")
        registry = {}
    for message in chapter02_page_contract_errors(registry, "site-pages.json"):
        error(message)

    pages = raw_registry.get("pages", [])
    chapter_page = (
        next(
            (
                item
                for item in pages
                if isinstance(item, dict)
                and item.get("source") == "manuscript/02-law-ethics-authorization.md"
            ),
            None,
        )
        if isinstance(pages, list)
        else None
    )
    if chapter_page is None:
        error(
            "site-pages.json: missing Chapter 2 manuscript page for negative regressions"
        )
    else:
        negative_registries: list[tuple[str, dict]] = []

        mutation = deepcopy(raw_registry)
        mutation["schemaVersion"] = "0.0.0"
        negative_registries.append(("schemaVersion drift", mutation))

        mutation = deepcopy(raw_registry)
        next(
            item
            for item in mutation["pages"]
            if item.get("source") == "manuscript/02-law-ethics-authorization.md"
        )["section"] = "additional"
        negative_registries.append(("section drift", mutation))

        mutation = deepcopy(raw_registry)
        next(
            item
            for item in mutation["pages"]
            if item.get("source") == "manuscript/02-law-ethics-authorization.md"
        )["order"] = 46
        negative_registries.append(("order drift", mutation))

        mutation = deepcopy(raw_registry)
        duplicated_page = next(
            item
            for item in mutation["pages"]
            if item.get("source") == "manuscript/02-law-ethics-authorization.md"
        )
        mutation["pages"].append(deepcopy(duplicated_page))
        negative_registries.append(("duplicate page", mutation))

        mutation = deepcopy(raw_registry)
        next(
            item
            for item in mutation["pages"]
            if item.get("source") == "manuscript/02-law-ethics-authorization.md"
        )["unexpectedKey"] = True
        negative_registries.append(("unknown page key", mutation))

        for mutation_name, mutated_registry in negative_registries:
            if not registry_mutation_is_rejected(
                mutated_registry,
                f"site-pages.json negative regression ({mutation_name})",
            ):
                error(
                    "site-pages.json: negative registry mutation was accepted: "
                    f"{mutation_name}"
                )

    artifact_index = read_text("artifact-index.md")
    require_tokens(
        "artifact-index.md",
        artifact_index,
        (
            "| ART-13 | Authorization Checklist | 2, 9 | `templates/authorization-checklist.md` |",
            "cases/ch02-authorization-decision-example.md",
        ),
    )

    figure_index = read_text("figure-index.md")
    require_tokens(
        "figure-index.md",
        figure_index,
        (
            "F-02-01",
            "Authorization Decision Gate",
            "T-02-01",
            "許容性判断の層",
        ),
    )

    glossary = read_text("glossary.md")
    require_tokens(
        "glossary.md",
        glossary,
        (
            "| Authority |",
            "| Authorization |",
            "| Data Owner |",
            "| Responsible Disclosure |",
            "| Rules of Engagement |",
            "| Scope |",
        ),
    )

    cases_index = read_text("cases/index.md")
    index = read_text("index.md")
    require_tokens(
        "cases/index.md",
        cases_index,
        (
            "ch02-authorization-decision-example.md",
            "Authorization Checklist",
        ),
    )
    require_tokens(
        "index.md",
        index,
        (
            "manuscript/02-law-ethics-authorization.md",
            "templates/authorization-checklist.md",
            "cases/ch02-authorization-decision-example.md",
        ),
    )

    sources = load_json("references/sources.json")
    if sources.get("checkedAt") != "2026-07-25":
        error(
            "references/sources.json: registry-level checkedAt must remain 2026-07-25; "
            "only the two Chapter 2 source entries were re-audited"
        )
    source_entries = {
        item.get("id"): item
        for item in sources.get("sources", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    for source_id in sorted(expected_source_ids):
        entry = source_entries.get(source_id)
        if entry is None:
            error(f"references/sources.json: missing {source_id}")
            continue
        chapters = entry.get("chapters", [])
        if 2 not in chapters:
            error(f"references/sources.json: {source_id} does not map chapter 2")

    expected_source_metadata = {
        "SRC-JP-LAW-001": {
            "version": "current display effective 2025-06-01",
            "checkedAt": "2026-08-05",
            "nextReviewAt": "2026-11-05",
            "noteMarkers": (
                "e-Gov current display was rechecked on 2026-08-05",
                "law effective from 2025-06-01",
                "confirm current text before publication",
                "book is not legal advice",
            ),
        },
        "SRC-IPA-VDP-001": {
            "version": "2024 edition",
            "checkedAt": "2026-08-05",
            "nextReviewAt": "2026-11-05",
            "noteMarkers": (
                "official IPA page and linked 2024 edition guideline were rechecked on 2026-08-05",
                "official page showed last update 2026-04-06",
                "current page and linked guideline must be rechecked at publication time",
            ),
        },
    }
    for source_id, expected in expected_source_metadata.items():
        entry = source_entries.get(source_id)
        if entry is None:
            continue
        for field in ("version", "checkedAt", "nextReviewAt"):
            if entry.get(field) != expected[field]:
                error(
                    f"references/sources.json: {source_id}.{field} "
                    f"must be {expected[field]!r}"
                )
        notes = entry.get("notes")
        if not isinstance(notes, str):
            error(f"references/sources.json: {source_id}.notes must be a string")
            continue
        for marker in expected["noteMarkers"]:
            if marker not in notes:
                error(
                    f"references/sources.json: {source_id}.notes missing marker {marker!r}"
                )

    audit_note_path = "references/ch02-source-review-2026-08-05.md"
    audit_note = read_text(audit_note_path)
    require_tokens(
        audit_note_path,
        audit_note,
        (
            "SRC-JP-LAW-001",
            "2025-06-01施行表示",
            "SRC-IPA-VDP-001",
            "2024年版",
            "2026-04-06",
            "Checked at | 2026-08-05",
        ),
    )

    baseline_path = "references/reference-baseline.md"
    baseline = read_text(baseline_path)
    if baseline != render_reference_baseline():
        error(f"{baseline_path}: out of sync with references/sources.json")

    package = load_json("package.json")
    scripts = package.get("scripts", {})
    if scripts.get("check:chapter02") != "python3 scripts/check_chapter02_contract.py":
        error("package.json: missing check:chapter02 script")
    if scripts.get("check:publication-projection") != (
        "python3 scripts/check_publication_projection.py"
    ):
        error("package.json: missing check:publication-projection script")
    if "check:chapter02" not in scripts.get("test", ""):
        error("package.json: npm test does not include check:chapter02")
    if "check:publication-projection" not in scripts.get("test", ""):
        error("package.json: npm test does not include check:publication-projection")

    for message in ERRORS:
        print(f"ERROR: {message}")
    if ERRORS:
        return 1

    print(
        "chapter 2 contract passed: manuscript, authorization artifact, synthetic case, "
        "source mapping, publication registry, shared Publication Projection "
        f"{PROJECTION_VERSION}, Content Safety Policy {CONTENT_SAFETY_POLICY_VERSION}, "
        "and handoff traceability"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
