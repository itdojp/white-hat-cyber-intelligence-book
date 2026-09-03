#!/usr/bin/env python3
"""Fail-closed contract tests for the shared content safety policy."""

from __future__ import annotations

import argparse
from dataclasses import fields, is_dataclass
from itertools import product
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.content_safety_policy import (  # noqa: E402
    _DIRECT_ACTION_MODIFIERS,
    _DIRECT_COORDINATORS,
    _DIRECT_LOCAL_NEGATIONS,
    _parse_direct_coordination_gap,
    ACTION_RULES,
    JAPANESE_PARTICLE_FRAMES,
    JapaneseParticleFrame,
    META_ANALYSIS_FRAMES,
    MetaAnalysisFrame,
    OPERATION_RULES,
    OperationRule,
    POLICY_VERSION,
    PROTECTED_OBJECT_RULES,
    SafetyFinding,
    normalize_visible_text,
    scan_action_text,
    scan_fields,
    scan_host_policy,
)


EXPECTED_POLICY_VERSION = "1.2.0"
FIXTURE_SCHEMA_VERSION = "1.0.0"
EXPECTED_LEGACY_UNSAFE_COUNT = 249
EXPECTED_LEGACY_SAFE_COUNT = 49
EXPECTED_DIRECT_ACTION_MODIFIERS = (
    "to",
    "also",
    "directly",
    "explicitly",
    "only",
    "ever",
    "immediately",
)
EXPECTED_DIRECT_COORDINATORS = ("and", "or", "but")
EXPECTED_DIRECT_LOCAL_NEGATIONS = ("do not", "never", "must not")
EXPECTED_PUBLICATION_CROSS_PRODUCT_CASES = 30_244
EXPECTED_ACTION_CATEGORIES = {
    "target.real_or_external",
    "secret.credential",
    "data.pii",
    "operation.authentication_or_session",
    "operation.malware",
    "operation.c2_or_phishing",
    "operation.privilege_or_evasion",
    "operation.disruption_or_destruction",
    "operation.social_engineering_or_tracking",
    "analysis.weak_evidence_attribution",
}
EXPECTED_ALL_CATEGORIES = EXPECTED_ACTION_CATEGORIES | {"network.host_or_address"}
EXPECTED_REPRESENTATIVE_IDS = {
    "CH02-MANUSCRIPT-EXTERNAL-API",
    "CH02-TEMPLATE-TARGET",
    "CH02-TEMPLATE-SECRET",
    "CH02-CASE-SAFETY",
    "CH02-CASE-HOST-TEST",
    "CH02-CASE-HOST-EXAMPLE",
    "CH11-MANUSCRIPT-TARGET",
    "CH11-MANUSCRIPT-SECRET",
    "CH11-MANUSCRIPT-THIRD-PARTY",
    "CH11-CASE-SAFETY",
    "CH11-TEMPLATE-SAFETY",
    "CH17-MANUSCRIPT-SCOPE",
    "CH17-MANUSCRIPT-CONNECTION",
    "CH17-CASE-SAFETY",
    "CH17-TEMPLATE-SAFETY",
    "CH25-MANUSCRIPT-SAFETY",
    "CH25-TEMPLATE-TARGET",
    "CH25-TEMPLATE-SECRET",
    "CH25-CASE-SAFETY",
    "CH25-CASE-HOST-SIGNIN",
    "CH25-CASE-HOST-PORTAL",
}
BLOCKER_TEXTS = {
    "do not build a keylogger, but deploy it",
    "never build a keylogger; however, use it",
    "keyloggerを作ることを禁止する、しかしそれを作る",
    "building a keylogger should be prohibited, but it is deployed",
    "write a keylogger",
    "code a rootkit",
}
SAFE_BLOCKER_COUNTERPARTS = {
    "Do not build a keylogger.",
    "Building a keylogger is prohibited.",
    "Keylogger creation is outside this book's scope.",
    "この教材ではkeyloggerを作らない。",
    "keyloggerを作ることを禁止する。",
    "この語はMalware分類の説明としてのみ記録する。",
}
REQUIRED_PUBLICATION_COORDINATION_UNSAFE = {
    "PUBLICATION-GAP-UNSAFE-001": (
        "deploy and immediately publish a phishing report",
        ("operation.c2_or_phishing",),
    ),
    "PUBLICATION-GAP-UNSAFE-002": (
        "build and directly publish a malware report",
        ("operation.malware",),
    ),
    "PUBLICATION-GAP-UNSAFE-003": (
        "use and explicitly announce a phishing analysis",
        ("operation.c2_or_phishing",),
    ),
    "PUBLICATION-GAP-UNSAFE-004": (
        "deploy or immediately publish a phishing report",
        ("operation.c2_or_phishing",),
    ),
    "PUBLICATION-GAP-UNSAFE-005": (
        "deploy but immediately publish a phishing report",
        ("operation.c2_or_phishing",),
    ),
    "PUBLICATION-GAP-UNSAFE-006": (
        "deploy and immediately do not publish a phishing report",
        ("operation.c2_or_phishing",),
    ),
    "PUBLICATION-GAP-UNSAFE-007": (
        "publish a phishing report and then deploy it",
        ("operation.c2_or_phishing",),
    ),
    "PUBLICATION-GAP-UNSAFE-008": (
        "immediately publish a phishing report, then deploy it",
        ("operation.c2_or_phishing",),
    ),
}
REQUIRED_PUBLICATION_COORDINATION_SAFE = {
    "PUBLICATION-GAP-SAFE-001": "immediately publish a phishing report",
    "PUBLICATION-GAP-SAFE-002": "directly announce a malware analysis",
    "PUBLICATION-GAP-SAFE-003": (
        "do not deploy or immediately publish a phishing report"
    ),
    "PUBLICATION-GAP-SAFE-004": (
        "deploy telemetry and immediately publish a phishing report"
    ),
    "PUBLICATION-GAP-SAFE-005": (
        "a sandbox is deployed, and we immediately publish a phishing report"
    ),
    "PUBLICATION-GAP-SAFE-006": (
        "do not deploy; immediately publish a phishing report"
    ),
    "PUBLICATION-GAP-SAFE-007": "publish a report about phishing",
    "PUBLICATION-GAP-SAFE-008": (
        "publish guidance that prohibits phishing deployment"
    ),
    # Issue #62 explicitly freezes the pre-existing ambiguous ``do not A and B``
    # behavior; this task does not introduce a broader negation policy.
    "PUBLICATION-GAP-SAFE-009": (
        "do not deploy and immediately publish a phishing report"
    ),
}
REQUIRED_UNSAFE_PARTICLE_DESTRUCTIVE_ACTIONS = {
    "PARTICLE-LOG-DELETION-JA": "ログを削除する。",
    "PARTICLE-AUDIT-TRAIL-DELETION-JA": "監査証跡を削除する。",
    "PARTICLE-DATA-DESTRUCTION-JA": "データを破壊する。",
    "PARTICLE-DATA-BARE-DESTRUCTION-JA": "本番データを破壊",
}
REQUIRED_SAFE_PARTICLE_DESTRUCTIVE_ACTIONS = {
    "SAFE-076": "ログを削除しない。",
    "SAFE-077": "監査証跡を削除しない。",
    "SAFE-078": "データを破壊しない。",
    "SAFE-079": "ログを削除することを禁止する。",
    "SAFE-080": "データを破壊することを禁止する。",
    "SAFE-081": "ブログを削除する。",
    "SAFE-082": "カタログを削除する。",
    "SAFE-083": "メタデータを変更する。",
    "SAFE-084": "メタデータを暗号化する。",
    "SAFE-096": "本番データを破壊しない",
}
REQUIRED_UNSAFE_BIDIRECTIONAL_ACTIONS = {
    "ACTION-BOTH-SIDES-JA-USE-PRE": "使用しないマルウェアを構築する",
    "ACTION-BOTH-SIDES-JA-CREATE-PRE": "構築しないマルウェアを使用する",
    "ACTION-BOTH-SIDES-MIXED-SCRIPT": "使用しないkeyloggerをdeployする",
    "ACTION-BOTH-SIDES-EN-THEN": "Do not use the keylogger that we then deploy.",
    "ACTION-RELATIVE-EN-SAFE-FIRST": "A keylogger that is not used is deployed.",
    "ACTION-POST-JA-UNSAFE-FIRST": "マルウェアを構築するが使用しない",
    "ACTION-BOTH-SIDES-JA-UNSAFE-PRE": "構築するマルウェアを使用しない",
    "ACTION-RELATIVE-EN-UNSAFE-FIRST": "A keylogger that is built is not deployed.",
    "ACTION-MODIFIER-EN-UNSAFE-PRE": "Build the new keylogger that is not deployed.",
    "ACTION-MODIFIER-JA-UNSAFE-PRE": "構築する危険なマルウェアを使用しない",
    "ACTION-MODIFIER-EN-AND": (
        "Build the new and improved keylogger that is not deployed."
    ),
    "ACTION-MODIFIER-EN-OR": (
        "Build the new or improved keylogger that is not deployed."
    ),
    "ACTION-MODIFIER-EN-BUT": (
        "Build the new but improved keylogger that is not deployed."
    ),
    "ACTION-MODIFIER-JA-COORDINATED": (
        "構築する高度で危険なマルウェアを使用しない"
    ),
    "ACTION-MIXED-CONJUNCTIVE": "キーロガーをdeployして",
    "ACTION-MIXED-POLITE-REQUEST": "キーロガーをdeployしてください",
    "ACTION-SEPARATE-OBJECT-UNSAFE-PRE": (
        "Build a keylogger that we can use a sandbox to analyze."
    ),
    "ACTION-TEMPORAL-NEXT-DAY": (
        "Do not build a keylogger that we deploy the next day."
    ),
    "ACTION-TEMPORAL-THIS-WEEK": (
        "Do not build a keylogger that we deploy this week."
    ),
    "ACTION-SEPARATE-OBJECT-TEMPORAL-UNSAFE": (
        "Build a keylogger that we can use the sandbox this week to analyze."
    ),
    "ACTION-TEMPORAL-VERY-NEXT-DAY": (
        "Do not build a keylogger that we deploy the very next day."
    ),
    "ACTION-TEMPORAL-NEXT-BUSINESS-DAY": (
        "Do not build a keylogger that we deploy the next business day."
    ),
    "JAPANESE-TE-FORM-CREATE": "キーロガーを作って",
    "JAPANESE-TE-FORM-CREATE-REQUEST": "キーロガーを作ってください",
}
REQUIRED_SAFE_BIDIRECTIONAL_ACTIONS = {
    "SAFE-002": "Building a keylogger is prohibited.",
    "SAFE-033": "Do not build or deploy a keylogger.",
    "SAFE-040": "マルウェアを使用しない。",
    "SAFE-041": "マルウェアを構築しない。",
    "SAFE-042": "使用しないマルウェアを説明する。",
    "SAFE-043": "使用しないマルウェアを構築しない。",
    "SAFE-044": "A keylogger that is not used is described.",
    "SAFE-045": "Do not build the new keylogger that is not deployed.",
    "SAFE-046": "構築しない危険なマルウェアを使用しない",
    "SAFE-047": "Use a sandbox to describe a keylogger that is not deployed.",
    "SAFE-048": "predeployするkeyloggerという識別子を説明する。",
    "SAFE-049": "Do not build the new and improved keylogger that is not deployed.",
    "SAFE-050": "Do not build the new or improved keylogger that is not deployed.",
    "SAFE-051": "Do not build the new but improved keylogger that is not deployed.",
    "SAFE-052": "構築しない高度で危険なマルウェアを使用しない",
    "SAFE-053": "Use a sandbox but describe a keylogger that is not deployed.",
    "SAFE-054": "Do not build a keylogger that we can use a sandbox to analyze.",
    "SAFE-055": "predeployしてくださいという識別子とkeyloggerを説明する。",
    "SAFE-056": "deployしてくださいIDという識別子とkeyloggerを説明する。",
    "SAFE-057": "deployしてください_idという識別子とkeyloggerを説明する。",
    "SAFE-059": (
        "Do not build a keylogger that we can use the sandbox this week to analyze."
    ),
    "SAFE-065": "キーロガーを作ってはいけない。",
}
REQUIRED_UNSAFE_PROHIBITION_SCOPE = {
    "CONTINUATION-FORBIDDEN-CONTRAST-MALWARE": (
        "Do not build a keylogger, but it is forbidden to deploy but use it."
    ),
    "CONTINUATION-FORBIDDEN-CONTRAST-TARGET": (
        "Do not access a third-party production API, but it is forbidden to connect "
        "to it but record it."
    ),
    "CONTINUATION-FORBIDDEN-COMMA-MALWARE": (
        "Do not build a keylogger, but it is forbidden to deploy, and use it."
    ),
    "CONTINUATION-FORBIDDEN-SENTENCE-MALWARE": (
        "Do not build a keylogger, but it is forbidden to deploy. Use it."
    ),
    "CONTINUATION-FORBIDDEN-PERIOD-CHAIN-MALWARE": (
        "Do not build a keylogger. It is forbidden to deploy. Use it."
    ),
    "CONTINUATION-FORBIDDEN-PERIOD-CHAIN-TARGET": (
        "Do not access a third-party production API. It is forbidden to connect "
        "to it. Record it."
    ),
    "TRAILING-PROHIBITION-DIFFERENT-ACTION": (
        "Build a keylogger whose deployment is prohibited."
    ),
    "TRAILING-PROHIBITION-LATER-ACTION": (
        "Build a keylogger that is prohibited from deployment."
    ),
    "FORBIDDEN-COORDINATOR-NEW-SUBJECT": (
        "Do not build a keylogger, but it is forbidden to deploy it and you should "
        "use it."
    ),
    "SAME-CLAUSE-AMBIGUOUS-AND-MALWARE": (
        "Do not build a keylogger and use it."
    ),
    "SAME-CLAUSE-AMBIGUOUS-AND-TARGET": (
        "Do not access a third-party production API and scan it."
    ),
    "SAME-CLAUSE-AMBIGUOUS-JA-MALWARE": "keyloggerを作らないで使用する",
    "CONTINUATION-THEN-MALWARE": "Do not build a keylogger then use it.",
    "CONTINUATION-STILL-MALWARE": "Do not build a keylogger still use it.",
    "CONTINUATION-SONOGO-JA-MALWARE": (
        "keyloggerを作らないその後それを使用する"
    ),
    "CONTINUATION-ADDITIONAL-PROTECTED-TARGET": (
        "Do not build a keylogger, but deploy it and access a third-party "
        "production API."
    ),
    "UNBOUND-GENERIC-PROHIBITION": (
        "Describe a prohibited operation and build a keylogger."
    ),
    "SHARED-TRAILING-OBJECT-CONTRAST": (
        "Build but do not deploy a keylogger."
    ),
    "PRE-ACTION-PROHIBITION-CONTRADICTION": (
        "You are prohibited from building a keylogger, but deploy it."
    ),
    "PRE-ACTION-BARE-PROHIBITION-CONTRADICTION": (
        "Forbidden to replay the synthetic session, but reuse it."
    ),
    "PRE-ACTION-BARE-PROHIBITION-NEW-SUBJECT": (
        "Prohibited from replaying the synthetic session and you should reuse it."
    ),
    "PRE-ACTION-BARE-PROHIBITION-NEW-MODAL": (
        "Forbidden from replaying the synthetic session and should reuse it."
    ),
    "PRE-ACTION-BARE-PROHIBITION-PASSIVE-MODAL": (
        "Prohibited from replaying the synthetic session and it should be reused."
    ),
    "OBJECT-FIRST-PROHIBITION-NEW-SUBJECT": (
        "The synthetic session is prohibited from replaying and you should reuse it."
    ),
    "OBJECT-FIRST-NEGATION-NEW-SUBJECT": (
        "Synthetic credentials must not be stolen and you should reuse them."
    ),
    "ACTION-FIRST-BARE-MODAL-PASSIVE": (
        "Forbidden from replaying the synthetic session and should be reused."
    ),
    "OBJECT-FIRST-BARE-MODAL-PASSIVE": (
        "The synthetic session is prohibited from replaying and should be reused."
    ),
    "INLINE-HTML-SPLIT-MALWARE": "<span>key</span><span>logger</span>を作る",
    "CONTINUATION-MULTI-OBJECT-TARGET": (
        "Do not access a third-party production API and do not build a keylogger. "
        "Scan the same target."
    ),
    "CONTINUATION-MULTI-OBJECT-GENERIC-PRONOUN": (
        "Do not access a third-party production API and do not build a keylogger. "
        "Scan it."
    ),
}
REQUIRED_SAFE_PROHIBITION_SCOPE = {
    "SAFE-030": "Do not build a keylogger, but it is forbidden to deploy and use it.",
    "SAFE-031": (
        "Do not access a third-party production API, but it is forbidden to connect "
        "to it and record it."
    ),
    "SAFE-032": (
        "Do not build a keylogger. It is forbidden to deploy. Do not use it."
    ),
    "SAFE-033": "Do not build or deploy a keylogger.",
    "SAFE-034": "Do not access or scan a third-party production API.",
    "SAFE-035": "Use a sandbox and do not build or deploy a keylogger.",
    "SAFE-036": (
        "Do not build a keylogger and use a sandbox because it is isolated."
    ),
    "SAFE-037": (
        "Do not build a keylogger. Use a sandbox because it is isolated."
    ),
    "SAFE-038": "Keylogger creation is a prohibited operation.",
    "SAFE-039": (
        "Do not build a keylogger. Use a sandbox because it is deployed."
    ),
    "SAFE-058": (
        "Do not access a third-party production API and do not build a keylogger. "
        "Do not scan the same target."
    ),
    "SAFE-060": (
        "Building a keylogger is prohibited and deploying it is prohibited."
    ),
    "SAFE-061": (
        "Do not access a third-party production API and do not build a keylogger. "
        "Do not scan it."
    ),
    "SAFE-062": (
        "Building a keylogger is prohibited and its deployment is prohibited."
    ),
    "SAFE-063": "Do not build but do not deploy a keylogger.",
    "SAFE-064": "Use a sandbox, but do not deploy a keylogger.",
    "SAFE-066": "You are prohibited from building a keylogger.",
    "SAFE-067": "You are forbidden from building a keylogger.",
    "SAFE-068": "You are prohibited from building or deploying a keylogger.",
    "SAFE-085": "Forbidden to replay the synthetic session or reuse it.",
    "SAFE-086": "Prohibited from replaying the synthetic session or reusing it.",
    "SAFE-087": "Forbidden from replaying the synthetic session or reusing it.",
    "SAFE-088": (
        "Prohibited from replaying the synthetic session and you should not reuse it."
    ),
    "SAFE-089": (
        "Forbidden from replaying the synthetic session and should not reuse it."
    ),
    "SAFE-090": (
        "Prohibited from replaying the synthetic session and it should not be reused."
    ),
    "SAFE-091": (
        "Prohibited from replaying the synthetic session and it could not be reused."
    ),
    "SAFE-092": (
        "The synthetic session is prohibited from replaying and you should not reuse it."
    ),
    "SAFE-093": (
        "Synthetic credentials must not be stolen and you should not reuse them."
    ),
    "SAFE-094": (
        "Forbidden from replaying the synthetic session and should not be reused."
    ),
    "SAFE-095": (
        "The synthetic session is prohibited from replaying and should not be reused."
    ),
}
REQUIRED_NORMALIZATION_CASES = {
    "INLINE-HTML-ADJACENT": (
        "<span>key</span><span>logger</span>を作る",
        "keyloggerを作る",
    ),
}
REQUIRED_UNSAFE_HOST_CASES = {
    "IPV4-NONDOC-JA-PARTICLE": (
        "10.0.0.1へ接続する",
        "non-documentation IP literal is disallowed",
    ),
    "IPV4-DOC-JA-UNSUPPORTED-PARTICLE": (
        "192.0.2.10から接続する",
        "non-approved bare IDN or punycode host",
    ),
    "IPV4-DOC-JA-IDN-SUFFIX": (
        "192.0.2.10へ例え.テスト",
        "non-approved bare IDN or punycode host",
    ),
    "IPV4-DOC-JA-ASCII-TAIL": (
        "192.0.2.10へconnect",
        "non-approved bare IDN or punycode host",
    ),
    "IPV4-INVALID-JA-PARTICLE": (
        "192.0.2.999へ接続する",
        "non-approved bare IDN or punycode host",
    ),
    "ENTITY-ENCODED-MARKDOWN-URL": (
        "[external](https&#58;&#47;&#47;example&#46;com/runbook)",
        "non-approved host suffix",
    ),
    "HTML-DOUBLE-QUOTED-COM": (
        '<a href="https://example.com">',
        "non-approved host suffix",
    ),
    "HTML-SINGLE-QUOTED-GOV": (
        "<a href='https://agency.gov/path'>",
        "non-approved host suffix",
    ),
    "HTML-ENTITY-ENCODED-COM": (
        '<img src="https&#58;&#47;&#47;example&#46;com/image.png">',
        "non-approved host suffix",
    ),
    "HTML-PROTOCOL-RELATIVE-CO-UK": (
        '<a href="//target.co.uk/runbook">',
        "non-approved host suffix",
    ),
    "HTML-QUOTED-TERMINAL-PERIOD": (
        '<a href="https://example.com/runbook.">',
        "non-approved host suffix",
    ),
    "HTML-QUOTED-TERMINAL-COMMA": (
        '<a href="https://example.com/runbook,">',
        "non-approved host suffix",
    ),
    "HTML-QUOTED-TERMINAL-SEMICOLON": (
        '<a href="https://example.com/runbook;">',
        "non-approved host suffix",
    ),
    "PROSE-TERMINAL-PUNCTUATION": (
        "See https://example.com/runbook.;",
        "non-approved host suffix",
    ),
    "HTML-QUOTED-PARENTHESIS": (
        '<a href="https://example.com/run(book).">',
        "non-approved host suffix",
    ),
    "HTML-QUOTED-LEADING-SPACE": (
        '<a href=" https://example.com/runbook.">',
        "non-approved host suffix",
    ),
    "HTML-MAILTO-DISALLOWED": (
        '<a href="mailto:user@example.com">mail</a>',
        "non-approved host suffix",
    ),
    "HTML-MAILTO-SECOND-RECIPIENT-DISALLOWED": (
        '<a href="mailto:user@lab.example,other@example.com">mail</a>',
        "non-approved host suffix",
    ),
    "HTML-MAILTO-CC-DISALLOWED": (
        '<a href="mailto:user@lab.example?cc=other@example.com">mail</a>',
        "non-approved host suffix",
    ),
    "HTML-MAILTO-TO-DISALLOWED": (
        '<a href="mailto:user@lab.example?to=other@example.com">mail</a>',
        "non-approved host suffix",
    ),
    "HTML-MAILTO-BCC-DISALLOWED": (
        '<a href="mailto:user@lab.example?bcc=other@example.com">mail</a>',
        "non-approved host suffix",
    ),
    "HTML-UNQUOTED-MAILTO-DISALLOWED": (
        "<a href=mailto:user@example.com>mail</a>",
        "non-approved host suffix",
    ),
    "MARKDOWN-AUTOLINK-MAILTO-DISALLOWED": (
        "<mailto:user@example.com>",
        "non-approved host suffix",
    ),
}
REQUIRED_SAFE_HOST_CASES = {
    "IPV4-DOC-JA-PARTICLE-HE": "192.0.2.10へ接続する",
    "IPV4-DOC-JA-PARTICLE-WO": "198.51.100.10を確認する",
    "IPV4-DOC-JA-PARTICLE-DE": "203.0.113.10で検証する",
    "IPV4-DOC-JA-PARTICLE-TOKEN-END": "192.0.2.10へ",
    "HTML-DOUBLE-QUOTED-EXAMPLE": '<a href="https://lab.example">',
    "HTML-SINGLE-QUOTED-TEST": "<a href='https://lab.test/path?q=1#x'>",
    "HTML-DOUBLE-QUOTED-INVALID": '<img src="https://assets.invalid/image.png">',
    "HTML-ENTITY-ENCODED-EXAMPLE": (
        '<a href="https&#58;&#47;&#47;lab&#46;example/runbook">'
    ),
    "HTML-QUOTED-PUNCTUATED-EXAMPLE": (
        '<a href="https://lab.example/runbook;">'
    ),
    "HTML-QUOTED-PARENTHESIS-EXAMPLE": (
        '<a href="https://lab.example/run(book).">'
    ),
    "HTML-QUOTED-LEADING-SPACE-EXAMPLE": (
        '<a href=" https://lab.example/runbook.">'
    ),
    "HTML-MAILTO-EXAMPLE": '<a href="mailto:user@lab.example">mail</a>',
    "HTML-MAILTO-MULTI-EXAMPLE": (
        '<a href="mailto:user@lab.example,other@service.test?to=forward@node.invalid'
        '&cc=copy@assets.invalid&bcc=blind@audit.example">mail</a>'
    ),
    "HTML-UNQUOTED-MAILTO-EXAMPLE": "<a href=mailto:user@lab.example>mail</a>",
    "MARKDOWN-AUTOLINK-MAILTO-EXAMPLE": "<mailto:user@lab.example>",
}
REQUIRED_UNSAFE_HOST_EXCERPTS = {
    "HTML-DOUBLE-QUOTED-COM": "https://example.com",
    "HTML-SINGLE-QUOTED-GOV": "https://agency.gov/path",
    "HTML-ENTITY-ENCODED-COM": "https://example.com/image.png",
    "HTML-PROTOCOL-RELATIVE-CO-UK": "//target.co.uk/runbook",
    "HTML-QUOTED-TERMINAL-PERIOD": "https://example.com/runbook.",
    "HTML-QUOTED-TERMINAL-COMMA": "https://example.com/runbook,",
    "HTML-QUOTED-TERMINAL-SEMICOLON": "https://example.com/runbook;",
    "PROSE-TERMINAL-PUNCTUATION": "https://example.com/runbook",
    "HTML-QUOTED-PARENTHESIS": "https://example.com/run(book).",
    "HTML-QUOTED-LEADING-SPACE": "https://example.com/runbook.",
    "HTML-MAILTO-DISALLOWED": "mailto:user@example.com",
    "HTML-MAILTO-SECOND-RECIPIENT-DISALLOWED": (
        "mailto:user@lab.example,other@example.com"
    ),
    "HTML-MAILTO-CC-DISALLOWED": (
        "mailto:user@lab.example?cc=other@example.com"
    ),
    "HTML-MAILTO-TO-DISALLOWED": (
        "mailto:user@lab.example?to=other@example.com"
    ),
    "HTML-MAILTO-BCC-DISALLOWED": (
        "mailto:user@lab.example?bcc=other@example.com"
    ),
    "HTML-UNQUOTED-MAILTO-DISALLOWED": "mailto:user@example.com",
    "MARKDOWN-AUTOLINK-MAILTO-DISALLOWED": "mailto:user@example.com",
}

REQUIRED_STRUCTURAL_GAP_UNSAFE = {
    "TARGET-JA-WHITESPACE-ANALYSIS": "第三者 の APIを分析する",
    "TARGET-OTHER-ORGANIZATION": "他社サービスへ接続する",
    "PII-LATIN-JAPANESE-BOUNDARY": "PIIを収集する",
    "PII-GENERIC-FIELD-SHAPE": "credit card number collected",
    "PII-CUSTOMER-INFO-MIXED-SCRIPT": "customer infoを分析する",
    "PII-EMPLOYEE-INFO-MIXED-SCRIPT": "employee infoを収集する",
    "SECRET-ANALYSIS": "Tokenを分析する",
    "NEGATED-FIRST-ACTION-JA-CHAIN": "Tokenを取得せず保存する",
    "NEGATED-OBJECT-BARE-ELLIPSIS": "Tokenは使用しない、取得する",
    "PRIVILEGE-MIXED-SCRIPT": "lateral movementを実施する",
    "AUTH-LOGIN-MIXED-SCRIPT": "sign-inする",
    "WEAK-EVIDENCE-PUBLICATION": "弱いEvidenceからの断定的帰属を公表する",
    "WEAK-EVIDENCE-EN-JA-PUBLICATION": "weak evidenceからの断定的帰属を公表する",
    "WEAK-EVIDENCE-EN-JA-IDENTIFICATION": "weak evidenceから断定的に国家を特定する",
    "DISRUPTION-ENCRYPT-DATA-EN": "encrypt data",
    "DISRUPTION-ENCRYPT-DATA-JA": "データを暗号化する",
}
REQUIRED_STRUCTURAL_GAP_SAFE = {
    "TARGET-NO-OPERATION-STATEMENT": "合成Scenario。外部接続と実Target操作なし",
    "JAPANESE-NORMATIVE-NEGATION-CREATE": "keyloggerを作るべきではない",
    "JAPANESE-NORMATIVE-NEGATION-IMPLEMENT": "rootkitを実装するべきではない",
    "RESULT-RECORD-NOT-SECRET-ELLIPSIS": "Tokenを使用しない、結果だけを記録する",
    "SECRET-NEGATED-ANALYSIS": "Tokenを分析しない",
    "SECRET-SYNTHETIC-ANALYSIS": "合成Tokenを分析する",
    "AUTH-EXPLANATORY-OUT-OF-SCOPE": "サインインする処理は扱わない",
}

REQUIRED_FINITE_GRAMMAR_1_2 = {
    "A": {
        "unsafe": {
            "A-UNSAFE-001": ("システムのログを削除する", ("operation.privilege_or_evasion",)),
            "A-UNSAFE-002": ("対象の監査証跡を消去する", ("operation.privilege_or_evasion",)),
            "A-UNSAFE-003": ("本番データを破壊する", ("operation.disruption_or_destruction",)),
            "A-UNSAFE-004": (
                "顧客のデータを暗号化する",
                ("data.pii", "operation.disruption_or_destruction"),
            ),
            "A-UNSAFE-005": ("監査ログを改ざんする", ("operation.privilege_or_evasion",)),
            "A-UNSAFE-006": ("本番データを破壊", ("operation.disruption_or_destruction",)),
            "A-UNSAFE-007": ("対象ログを削除する", ("operation.privilege_or_evasion",)),
            "A-UNSAFE-008": ("本番ログを削除する", ("operation.privilege_or_evasion",)),
        },
        "safe": {
            "A-SAFE-001": "システムのログを削除しない",
            "A-SAFE-002": "本番データを破壊することを禁止する",
            "A-SAFE-003": "監査ログを改ざんしない",
            "A-SAFE-004": "システムのログを削除しない。しかし監査ログを改ざんしない",
            "A-SAFE-005": "システムのログを削除しない。しかし監査証跡を消去しない",
            "A-SAFE-006": "本番データを破壊しない",
            "A-SAFE-007": "対象ログを削除しない",
            "A-SAFE-008": "本番ログを削除しない",
        },
        "nearMiss": {
            "A-NEAR-001": "ログ削除の危険性を分析する",
            "A-NEAR-002": "カタログを削除する",
            "A-NEAR-003": "ブログを削除する",
            "A-NEAR-004": "メタデータの取扱いを説明する",
            "A-NEAR-005": "対象カタログを削除する",
            "A-NEAR-006": "本番ブログを削除する",
        },
        "continuation": {
            "A-CONT-001": (
                "システムのログを削除して監査証跡を消去する",
                ("operation.privilege_or_evasion",),
            ),
            "A-CONT-002": (
                "システムのログを削除しない。しかし監査ログを改ざんする",
                ("operation.privilege_or_evasion",),
            ),
            "A-CONT-003": (
                "システムのログを削除しない。しかし監査証跡を消去する",
                ("operation.privilege_or_evasion",),
            ),
        },
    },
    "B": {
        "unsafe": {
            "B-UNSAFE-001": ("合成認証情報を窃取する", ("operation.authentication_or_session",)),
            "B-UNSAFE-002": ("合成セッションを再利用する", ("operation.authentication_or_session",)),
            "B-UNSAFE-003": ("synthetic sessionを再利用する", ("operation.authentication_or_session",)),
            "B-UNSAFE-004": ("mock tokenをリプレイする", ("operation.authentication_or_session",)),
            "B-UNSAFE-005": ("test cookieを乗っ取る", ("operation.authentication_or_session",)),
            "B-UNSAFE-006": ("synthetic credentials are stolen", ("operation.authentication_or_session",)),
            "B-UNSAFE-007": ("synthetic JWT is replayed", ("operation.authentication_or_session",)),
            "B-UNSAFE-008": ("合成認証情報を持ち出す", ("operation.authentication_or_session",)),
            "B-UNSAFE-009": ("合成認証情報を流出させる", ("operation.authentication_or_session",)),
            "B-UNSAFE-010": (
                "synthetic credentialsをexfiltrateする",
                ("operation.authentication_or_session",),
            ),
            "B-UNSAFE-011": (
                "synthetic sessionをreplayする",
                ("operation.authentication_or_session",),
            ),
        },
        "safe": {
            "B-SAFE-001": "合成認証情報を窃取しない",
            "B-SAFE-002": "Session reuseは禁止される",
            "B-SAFE-003": "synthetic session replay is prohibited",
            "B-SAFE-004": "合成認証情報は窃取されない",
            "B-SAFE-005": "合成セッションは再利用されない",
            "B-SAFE-006": "合成認証情報を持ち出さない",
            "B-SAFE-007": "合成認証情報を流出させない",
            "B-SAFE-008": "synthetic credentialsをexfiltrateしない",
            "B-SAFE-009": "synthetic sessionをreplayしない",
            "B-SAFE-010": (
                "Synthetic credentials must not be stolen and are not reused"
            ),
        },
        "nearMiss": {
            "B-NEAR-001": "合成Tokenをoffline fixtureで使用する",
            "B-NEAR-002": "mock Cookieの分類結果を記録する",
            "B-NEAR-003": "認証情報の窃取を検知する",
            "B-NEAR-004": "The fixture records a synthetic JWT literal.",
        },
        "continuation": {
            "B-CONT-001": (
                "Do not replay the synthetic session, but reuse it.",
                ("operation.authentication_or_session",),
            ),
            "B-CONT-002": (
                "合成認証情報を窃取しない。しかし再利用する",
                ("operation.authentication_or_session",),
            ),
            "B-CONT-003": (
                "合成認証情報を持ち出さない。しかし再利用する",
                ("operation.authentication_or_session",),
            ),
            "B-CONT-004": (
                "Synthetic credentials must not be stolen and are reused",
                ("operation.authentication_or_session",),
            ),
        },
    },
    "C": {
        "safe": {
            "C-SAFE-001": "analyze the risk of collecting PII",
            "C-SAFE-002": "assess the privacy impact of storing personal information",
            "C-SAFE-003": "evaluate safeguards against sharing customer information",
            "C-SAFE-004": "review whether collecting PII is necessary",
            "C-SAFE-005": "document the consequences of exposing employee information",
            "C-SAFE-006": "discuss controls related to processing personal data",
            "C-SAFE-007": "do not collect and analyze the risk of storing PII",
        },
        "unsafe": {
            "C-UNSAFE-001": ("analyze PII", ("data.pii",)),
            "C-UNSAFE-002": ("collect PII for analysis", ("data.pii",)),
            "C-UNSAFE-003": ("analyze and collect PII", ("data.pii",)),
            "C-UNSAFE-004": ("analyze the risk, then collect PII", ("data.pii",)),
            "C-UNSAFE-005": ("review PII and share it", ("data.pii",)),
            "C-UNSAFE-006": (
                "assess the impact and retain customer information",
                ("data.pii",),
            ),
            "C-UNSAFE-007": (
                "collect and analyze the risk of storing PII",
                ("data.pii",),
            ),
        },
        "nearMiss": {
            "C-NEAR-001": "analyze the risk of collecting telemetry",
            "C-NEAR-002": "review whether storing fixture output is necessary",
            "C-NEAR-003": (
                "analyze the risk of collecting PII and store the same report"
            ),
            "C-NEAR-004": (
                "collect telemetry and analyze the risk of storing PII"
            ),
        },
        "continuation": {
            "C-CONT-001": (
                "analyze the risk of collecting PII, then store it",
                ("data.pii",),
            ),
            "C-CONT-002": (
                "analyze the risk of collecting PII and use it",
                ("data.pii",),
            ),
        },
    },
}


errors: list[str] = []


def error(message: str) -> None:
    errors.append(message)


def load_json(relative: str) -> dict[str, Any]:
    path = ROOT / relative
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        error(f"{relative}: cannot load strict UTF-8 JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        error(f"{relative}: root must be an object")
        return {}
    return value


def exact_keys(value: dict[str, Any], expected: set[str], context: str) -> bool:
    actual = set(value)
    if actual != expected:
        error(f"{context}: keys {sorted(actual)!r} do not match {sorted(expected)!r}")
        return False
    return True


def checked_entries(
    value: Any,
    *,
    expected_keys: set[str],
    context: str,
) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        error(f"{context}: must be an array")
        return []
    result: list[dict[str, Any]] = []
    ids: set[str] = set()
    for index, item in enumerate(value):
        item_context = f"{context}[{index}]"
        if not isinstance(item, dict):
            error(f"{item_context}: must be an object")
            continue
        exact_keys(item, expected_keys, item_context)
        identifier = item.get("id")
        if not isinstance(identifier, str) or not identifier:
            error(f"{item_context}: id must be a non-empty string")
        elif identifier in ids:
            error(f"{item_context}: duplicate id {identifier!r}")
        else:
            ids.add(identifier)
        if not isinstance(item.get("text"), str) or not item.get("text"):
            error(f"{item_context}: text must be a non-empty string")
        result.append(item)
    return result


def check_public_api() -> None:
    if POLICY_VERSION != EXPECTED_POLICY_VERSION:
        error(f"policy version {POLICY_VERSION!r} is not {EXPECTED_POLICY_VERSION!r}")
    if not is_dataclass(SafetyFinding):
        error("SafetyFinding must be a dataclass")
    actual_fields = tuple(field.name for field in fields(SafetyFinding))
    expected_fields = (
        "category",
        "location",
        "normalized_excerpt",
        "reason",
        "policy_version",
    )
    if actual_fields != expected_fields:
        error(f"SafetyFinding fields {actual_fields!r} do not match {expected_fields!r}")
    if not SafetyFinding.__dataclass_params__.frozen:
        error("SafetyFinding must remain frozen")
    for function in (normalize_visible_text, scan_action_text, scan_host_policy, scan_fields):
        if not callable(function):
            error(f"stable API member {function!r} is not callable")

    model_categories = {rule.category for rule in PROTECTED_OBJECT_RULES}
    if model_categories != EXPECTED_ACTION_CATEGORIES:
        error(
            f"protected object categories {sorted(model_categories)!r} do not match "
            f"{sorted(EXPECTED_ACTION_CATEGORIES)!r}"
        )
    required_action_kinds = {
        "create", "deploy-use", "access-collect", "analyze", "perform", "attribute"
    }
    action_kinds = {rule.kind for rule in ACTION_RULES}
    if action_kinds != required_action_kinds:
        error(f"action kinds {sorted(action_kinds)!r} do not match {sorted(required_action_kinds)!r}")

    for model in (JapaneseParticleFrame, OperationRule, MetaAnalysisFrame):
        if not is_dataclass(model) or not model.__dataclass_params__.frozen:
            error(f"{model.__name__} must remain a frozen dataclass")
    if {frame.category for frame in JAPANESE_PARTICLE_FRAMES} != {
        "operation.privilege_or_evasion",
        "operation.disruption_or_destruction",
    }:
        error("Japanese particle frame categories drifted")
    if {frame.action_kind for frame in JAPANESE_PARTICLE_FRAMES} != {"access-collect"}:
        error("Japanese particle frame action kinds drifted")
    if len(OPERATION_RULES) != 1:
        error("finite non-qualifiable operation inventory drifted")
    else:
        operation = OPERATION_RULES[0]
        if (
            operation.kind != "theft-reuse"
            or operation.category != "operation.authentication_or_session"
            or operation.synthetic_qualifiable
            or operation.precedence <= 0
        ):
            error("theft/reuse operation precedence contract drifted")
    if len(META_ANALYSIS_FRAMES) != 1:
        error("finite PII meta-analysis frame inventory drifted")
    else:
        frame = META_ANALYSIS_FRAMES[0]
        expected_frame = (
            (
                "analyze", "assess", "evaluate", "review", "examine", "model",
                "discuss", "document",
            ),
            (
                "risk", "risks", "impact", "impacts", "implications", "policy",
                "policies", "control", "controls", "safeguard", "safeguards",
                "necessity", "consequences",
            ),
            ("of", "associated with", "related to", "against", "whether"),
            ("collecting", "storing", "sharing", "using", "processing", "exposing", "retaining"),
            (
                "pii", "personal information", "personal data", "employee information",
                "employee data", "customer information", "customer data",
            ),
        )
        actual_frame = (
            frame.meta_verbs,
            frame.meta_heads,
            frame.relations,
            frame.embedded_operations,
            frame.protected_objects,
        )
        if actual_frame != expected_frame:
            error("finite PII meta-analysis vocabulary drifted")


def check_action_corpus() -> list[tuple[str, str]]:
    relative = "tests/fixtures/content-safety/action-corpus.json"
    corpus = load_json(relative)
    exact_keys(corpus, {"schemaVersion", "policyVersion", "unsafe", "safe"}, relative)
    if corpus.get("schemaVersion") != FIXTURE_SCHEMA_VERSION or corpus.get("policyVersion") != POLICY_VERSION:
        error(f"{relative}: schemaVersion/policyVersion mismatch")

    unsafe = checked_entries(
        corpus.get("unsafe"),
        expected_keys={"id", "text", "expectedCategories"},
        context=f"{relative}.unsafe",
    )
    safe = checked_entries(
        corpus.get("safe"),
        expected_keys={"id", "text"},
        context=f"{relative}.safe",
    )

    unsafe_texts = {item.get("text") for item in unsafe}
    safe_texts = {item.get("text") for item in safe}
    if not BLOCKER_TEXTS <= unsafe_texts:
        error(f"{relative}: missing blocker phrases {sorted(BLOCKER_TEXTS - unsafe_texts)!r}")
    if not SAFE_BLOCKER_COUNTERPARTS <= safe_texts:
        error(
            f"{relative}: missing safe blocker counterparts "
            f"{sorted(SAFE_BLOCKER_COUNTERPARTS - safe_texts)!r}"
        )

    covered_categories: set[str] = set()
    deterministic_fields: list[tuple[str, str]] = []
    for item in unsafe:
        identifier = item.get("id")
        text = item.get("text")
        expected = item.get("expectedCategories")
        if not isinstance(identifier, str) or not isinstance(text, str):
            continue
        if (
            not isinstance(expected, list)
            or not expected
            or not all(isinstance(category, str) for category in expected)
        ):
            error(f"{relative}.{identifier}: expectedCategories must be a non-empty string array")
            continue
        if not set(expected) <= EXPECTED_ACTION_CATEGORIES:
            error(f"{relative}.{identifier}: unknown expected category")
        findings = scan_action_text(text, location=identifier)
        actual = {finding.category for finding in findings}
        if not set(expected) <= actual:
            error(
                f"{relative}.{identifier}: expected {sorted(expected)!r}, got {sorted(actual)!r}"
            )
        if any(finding.location != identifier for finding in findings):
            error(f"{relative}.{identifier}: finding location drift")
        if any(finding.policy_version != POLICY_VERSION for finding in findings):
            error(f"{relative}.{identifier}: finding policy version drift")
        covered_categories.update(expected)
        deterministic_fields.append((identifier, text))

    if covered_categories != EXPECTED_ACTION_CATEGORIES:
        error(
            f"{relative}: category coverage {sorted(covered_categories)!r} does not match "
            f"{sorted(EXPECTED_ACTION_CATEGORIES)!r}"
        )
    required_pair_ids = {"TARGET-OBJECT-FIRST", "TARGET-ACTION-FIRST"}
    unsafe_by_id = {item.get("id"): item.get("text") for item in unsafe}
    safe_by_id = {item.get("id"): item.get("text") for item in safe}
    unsafe_ids = set(unsafe_by_id)
    if not required_pair_ids <= unsafe_ids:
        error(f"{relative}: action-before/object-before regressions are incomplete")
    for identifier, expected_text in REQUIRED_UNSAFE_PROHIBITION_SCOPE.items():
        if unsafe_by_id.get(identifier) != expected_text:
            error(f"{relative}: unsafe prohibition-scope regression {identifier!r} drifted")
    for identifier, expected_text in REQUIRED_UNSAFE_BIDIRECTIONAL_ACTIONS.items():
        if unsafe_by_id.get(identifier) != expected_text:
            error(f"{relative}: bidirectional unsafe regression {identifier!r} drifted")
    for identifier, expected_text in REQUIRED_UNSAFE_PARTICLE_DESTRUCTIVE_ACTIONS.items():
        if unsafe_by_id.get(identifier) != expected_text:
            error(f"{relative}: particle destructive unsafe regression {identifier!r} drifted")
    for identifier, expected_text in REQUIRED_SAFE_PROHIBITION_SCOPE.items():
        if safe_by_id.get(identifier) != expected_text:
            error(f"{relative}: safe prohibition-scope regression {identifier!r} drifted")
    for identifier, expected_text in REQUIRED_SAFE_BIDIRECTIONAL_ACTIONS.items():
        if safe_by_id.get(identifier) != expected_text:
            error(f"{relative}: bidirectional safe regression {identifier!r} drifted")
    for identifier, expected_text in REQUIRED_SAFE_PARTICLE_DESTRUCTIVE_ACTIONS.items():
        if safe_by_id.get(identifier) != expected_text:
            error(f"{relative}: particle destructive safe regression {identifier!r} drifted")

    for item in safe:
        identifier = item.get("id")
        text = item.get("text")
        if not isinstance(identifier, str) or not isinstance(text, str):
            continue
        findings = scan_action_text(text, location=identifier)
        if findings:
            error(f"{relative}.{identifier}: safe text produced findings {findings!r}")
        deterministic_fields.append((identifier, text))

    for coordinator in ("or", "nor"):
        long_coordination = (
            "Do not build" + f" {coordinator} use" * 1200 + " a keylogger."
        )
        try:
            long_findings = scan_action_text(
                long_coordination,
                location=f"LONG-{coordinator.upper()}-COORDINATION",
            )
        except RecursionError:
            error(
                f"{relative}: long {coordinator} coordination depends on "
                "Python recursion depth"
            )
        else:
            if long_findings:
                error(
                    f"{relative}: explicitly negated long {coordinator} "
                    f"coordination produced {long_findings!r}"
                )
    return deterministic_fields


def check_publication_coordination_corpus() -> list[tuple[str, str]]:
    """Freeze Issue #62's exact Publication coordination examples."""

    relative = (
        "tests/fixtures/content-safety/"
        "publication-coordination-1.2-corpus.json"
    )
    corpus = load_json(relative)
    exact_keys(corpus, {"schemaVersion", "policyVersion", "unsafe", "safe"}, relative)
    if (
        corpus.get("schemaVersion") != FIXTURE_SCHEMA_VERSION
        or corpus.get("policyVersion") != POLICY_VERSION
    ):
        error(f"{relative}: schemaVersion/policyVersion mismatch")
    unsafe = checked_entries(
        corpus.get("unsafe"),
        expected_keys={"id", "text", "expectedCategories"},
        context=f"{relative}.unsafe",
    )
    safe = checked_entries(
        corpus.get("safe"),
        expected_keys={"id", "text"},
        context=f"{relative}.safe",
    )
    actual_unsafe = {
        item.get("id"): (
            item.get("text"),
            tuple(item.get("expectedCategories", [])),
        )
        for item in unsafe
    }
    actual_safe = {item.get("id"): item.get("text") for item in safe}
    if actual_unsafe != REQUIRED_PUBLICATION_COORDINATION_UNSAFE:
        error(f"{relative}: unsafe Issue #62 inventory drifted")
    if actual_safe != REQUIRED_PUBLICATION_COORDINATION_SAFE:
        error(f"{relative}: safe Issue #62 inventory drifted")

    deterministic_fields: list[tuple[str, str]] = []
    for item in unsafe:
        identifier = item.get("id")
        text = item.get("text")
        expected = item.get("expectedCategories")
        if not (
            isinstance(identifier, str)
            and isinstance(text, str)
            and isinstance(expected, list)
            and all(isinstance(category, str) for category in expected)
        ):
            continue
        actual = sorted(
            {finding.category for finding in scan_action_text(text, location=identifier)}
        )
        if actual != sorted(expected):
            error(
                f"{relative}.{identifier}: expected exactly {sorted(expected)!r}, "
                f"got {actual!r}"
            )
        deterministic_fields.append((identifier, text))
    for item in safe:
        identifier = item.get("id")
        text = item.get("text")
        if not isinstance(identifier, str) or not isinstance(text, str):
            continue
        findings = scan_action_text(text, location=identifier)
        if findings:
            error(f"{relative}.{identifier}: safe text produced {findings!r}")
        deterministic_fields.append((identifier, text))
    return deterministic_fields


def _publication_document(protected: str, head: str) -> str:
    article = "a " if head != "guidance" else ""
    return f"{article}{protected} {head}"


def _publication_lead(
    modifier: str | None,
    local_negation: str | None,
    publication: str,
) -> str:
    return " ".join(
        value
        for value in (modifier, local_negation, publication)
        if value is not None
    )


def check_publication_coordination_cross_product() -> int:
    """Generate Issue #62's finite matrix from the Policy source constants."""

    if _DIRECT_ACTION_MODIFIERS != EXPECTED_DIRECT_ACTION_MODIFIERS:
        error("direct Action modifier source-of-truth drifted without fixture audit")
    if _DIRECT_COORDINATORS != EXPECTED_DIRECT_COORDINATORS:
        error("direct coordinator source-of-truth drifted without fixture audit")
    if _DIRECT_LOCAL_NEGATIONS != EXPECTED_DIRECT_LOCAL_NEGATIONS:
        error("direct local-negation source-of-truth drifted without fixture audit")

    modifiers: tuple[str | None, ...] = (None, *_DIRECT_ACTION_MODIFIERS)
    local_negations: tuple[str | None, ...] = (None, *_DIRECT_LOCAL_NEGATIONS)
    prior_actions = ("build", "deploy", "install", "run", "use", "operate", "access")
    publications = ("publish", "announce")
    protected_objects = (
        ("phishing", "operation.c2_or_phishing"),
        ("malware", "operation.malware"),
    )
    document_heads = ("report", "analysis", "guidance")
    relations = ("shared", "distinct-object", "new-subject")
    mismatches: list[str] = []
    case_count = 0

    def categories(text: str) -> set[str]:
        return {
            finding.category
            for finding in scan_action_text(text, location="PUBLICATION-CROSS-PRODUCT")
        }

    def require(text: str, category: str, expected: bool) -> None:
        nonlocal case_count
        case_count += 1
        actual = category in categories(text)
        if actual != expected and len(mismatches) < 12:
            mismatches.append(
                f"expected finding={expected}, actual categories={sorted(categories(text))!r}: "
                f"{text!r}"
            )

    # Main relation matrix.  Publication-local negation never suppresses an
    # affirmative prior Action.  A distinct Object or explicit subject prevents
    # rebinding across the coordinator.
    for (
        prior,
        coordinator,
        modifier,
        publication,
        (protected, category),
        head,
        local_negation,
        relation,
    ) in product(
        prior_actions,
        _DIRECT_COORDINATORS,
        modifiers,
        publications,
        protected_objects,
        document_heads,
        local_negations,
        relations,
    ):
        publication_phrase = _publication_lead(
            modifier,
            local_negation,
            publication,
        )
        document = _publication_document(protected, head)
        if relation == "shared":
            text = f"{prior} {coordinator} {publication_phrase} {document}"
            expected = True
        elif relation == "distinct-object":
            text = (
                f"{prior} telemetry {coordinator} {publication_phrase} {document}"
            )
            expected = False
        else:
            text = (
                f"{prior} telemetry, {coordinator} we {publication_phrase} {document}"
            )
            expected = False
        require(text, category, expected)

    # Existing local-negation semantics for a prior Action remain unchanged.
    for (
        prior,
        coordinator,
        modifier,
        publication,
        (protected, category),
        head,
    ) in product(
        prior_actions,
        _DIRECT_COORDINATORS,
        modifiers,
        publications,
        protected_objects,
        document_heads,
    ):
        text = (
            f"do not {prior} {coordinator} "
            f"{_publication_lead(modifier, None, publication)} "
            f"{_publication_document(protected, head)}"
        )
        require(text, category, False)

    # Publication-only frames remain defensive prose for every frozen modifier
    # and supported local-negation form.
    for (
        modifier,
        publication,
        (protected, category),
        head,
        local_negation,
    ) in product(
        modifiers,
        publications,
        protected_objects,
        document_heads,
        local_negations,
    ):
        text = (
            f"{_publication_lead(modifier, local_negation, publication)} "
            f"{_publication_document(protected, head)}"
        )
        require(text, category, False)

    # A later affirmative continuation must not inherit Publication suppression.
    for (
        modifier,
        publication,
        (protected, category),
        head,
        prior,
    ) in product(
        modifiers,
        publications,
        protected_objects,
        document_heads,
        prior_actions,
    ):
        text = (
            f"{_publication_lead(modifier, None, publication)} "
            f"{_publication_document(protected, head)}, then {prior} it"
        )
        require(text, category, True)

    # Prove backward traversal across a two-Action finite chain.  The nearest
    # Action is locally prohibited so the finding must come from the older
    # affirmative Action; the companion matrix prohibits both Actions.
    for (
        first_coordinator,
        second_coordinator,
        modifier,
        publication,
        (protected, category),
        head,
    ) in product(
        _DIRECT_COORDINATORS,
        _DIRECT_COORDINATORS,
        modifiers,
        publications,
        protected_objects,
        document_heads,
    ):
        publication_phrase = _publication_lead(modifier, None, publication)
        document = _publication_document(protected, head)
        require(
            f"build {first_coordinator} do not deploy {second_coordinator} "
            f"{publication_phrase} {document}",
            category,
            True,
        )
        require(
            f"do not build {first_coordinator} do not deploy "
            f"{second_coordinator} {publication_phrase} {document}",
            category,
            False,
        )

    # A new explicit subject before the current-clause chain severs the previous
    # bare Action, including when Publication itself has a finite local negation.
    for (
        second_coordinator,
        modifier,
        publication,
        (protected, category),
        head,
        publication_local_negation,
    ) in product(
        _DIRECT_COORDINATORS,
        modifiers,
        publications,
        protected_objects,
        document_heads,
        local_negations,
    ):
        publication_phrase = _publication_lead(
            modifier,
            publication_local_negation,
            publication,
        )
        require(
            f"build but we do not deploy {second_coordinator} "
            f"{publication_phrase} {_publication_document(protected, head)}",
            category,
            False,
        )

    # Directly exercise the structured whole-gap parser.  Coverage is generated
    # from the same constants, so adding one modifier without updating the
    # frozen expected tuple cannot silently skip the new grammar branch.
    covered_modifiers: set[str] = set()
    for coordinator, modifier, local_negation in product(
        _DIRECT_COORDINATORS,
        modifiers,
        local_negations,
    ):
        gap = " ".join(
            value
            for value in (coordinator, modifier, local_negation)
            if value is not None
        )
        parsed = _parse_direct_coordination_gap(
            gap,
            allow_local_negation=True,
            coordinators=frozenset(_DIRECT_COORDINATORS),
        )
        case_count += 1
        if parsed is None:
            if len(mismatches) < 12:
                mismatches.append(f"direct coordination gap did not parse: {gap!r}")
            continue
        if (
            parsed.coordinator != coordinator
            or parsed.local_negation != local_negation
            or parsed.modifiers != (() if modifier is None else (modifier,))
        ):
            if len(mismatches) < 12:
                mismatches.append(f"direct coordination gap parsed incorrectly: {gap!r}")
        if modifier is not None:
            covered_modifiers.add(modifier)
    if covered_modifiers != set(_DIRECT_ACTION_MODIFIERS):
        error("generated Publication matrix does not cover every direct modifier")

    invalid_gaps = (
        "and, immediately",
        "and we immediately",
        "and telemetry immediately",
        "and immediately;",
    )
    for gap in invalid_gaps:
        case_count += 1
        if _parse_direct_coordination_gap(
            gap,
            allow_local_negation=True,
            coordinators=frozenset(_DIRECT_COORDINATORS),
        ) is not None:
            if len(mismatches) < 12:
                mismatches.append(f"invalid direct coordination gap parsed: {gap!r}")

    if mismatches:
        error(
            "Publication coordination cross-product failed; examples: "
            + " | ".join(mismatches)
        )
    if case_count != EXPECTED_PUBLICATION_CROSS_PRODUCT_CASES:
        error(
            "Publication coordination cross-product count drifted: "
            f"expected {EXPECTED_PUBLICATION_CROSS_PRODUCT_CASES}, got {case_count}"
        )
    return case_count


def check_structural_gap_corpus() -> list[tuple[str, str]]:
    """Exercise finite grammar shapes added by the 1.1 minor re-audit.

    These are category- and language-structure regressions, not chapter fields or
    a per-chapter exception list.  The external legacy parity corpus is accepted
    only by the explicit probe below.
    """

    relative = "tests/fixtures/content-safety/structural-gap-corpus.json"
    corpus = load_json(relative)
    exact_keys(corpus, {"schemaVersion", "policyVersion", "unsafe", "safe"}, relative)
    if corpus.get("schemaVersion") != FIXTURE_SCHEMA_VERSION or corpus.get("policyVersion") != POLICY_VERSION:
        error(f"{relative}: schemaVersion/policyVersion mismatch")
    unsafe = checked_entries(
        corpus.get("unsafe"),
        expected_keys={"id", "text", "expectedCategories"},
        context=f"{relative}.unsafe",
    )
    safe = checked_entries(
        corpus.get("safe"),
        expected_keys={"id", "text"},
        context=f"{relative}.safe",
    )
    unsafe_by_id = {item.get("id"): item.get("text") for item in unsafe}
    safe_by_id = {item.get("id"): item.get("text") for item in safe}
    if unsafe_by_id != REQUIRED_STRUCTURAL_GAP_UNSAFE:
        error(f"{relative}: unsafe structural regression inventory drifted")
    if safe_by_id != REQUIRED_STRUCTURAL_GAP_SAFE:
        error(f"{relative}: safe structural regression inventory drifted")

    deterministic_fields: list[tuple[str, str]] = []
    for item in unsafe:
        identifier, text, expected = item.get("id"), item.get("text"), item.get("expectedCategories")
        if not isinstance(identifier, str) or not isinstance(text, str) or not isinstance(expected, list):
            continue
        findings = scan_action_text(text, location=identifier)
        actual = {finding.category for finding in findings}
        if not set(expected) <= actual:
            error(f"{relative}.{identifier}: expected {expected!r}, got {sorted(actual)!r}")
        deterministic_fields.append((identifier, text))
    for item in safe:
        identifier, text = item.get("id"), item.get("text")
        if not isinstance(identifier, str) or not isinstance(text, str):
            continue
        findings = scan_action_text(text, location=identifier)
        if findings:
            error(f"{relative}.{identifier}: safe text produced findings {findings!r}")
        deterministic_fields.append((identifier, text))
    return deterministic_fields


def check_finite_grammar_1_2_corpus() -> list[tuple[str, str]]:
    """Freeze Issue #61's three semantic classes as exact table inventories."""

    relative = "tests/fixtures/content-safety/finite-grammar-1.2-corpus.json"
    corpus = load_json(relative)
    exact_keys(corpus, {"schemaVersion", "policyVersion", "clusters"}, relative)
    if (
        corpus.get("schemaVersion") != FIXTURE_SCHEMA_VERSION
        or corpus.get("policyVersion") != POLICY_VERSION
    ):
        error(f"{relative}: schemaVersion/policyVersion mismatch")
    clusters = corpus.get("clusters")
    if not isinstance(clusters, dict):
        error(f"{relative}.clusters: must be an object")
        return []
    exact_keys(clusters, set(REQUIRED_FINITE_GRAMMAR_1_2), f"{relative}.clusters")

    deterministic_fields: list[tuple[str, str]] = []
    seen_ids: set[str] = set()
    for cluster_name, required_groups in REQUIRED_FINITE_GRAMMAR_1_2.items():
        cluster = clusters.get(cluster_name)
        if not isinstance(cluster, dict):
            error(f"{relative}.clusters.{cluster_name}: must be an object")
            continue
        exact_keys(
            cluster,
            set(required_groups),
            f"{relative}.clusters.{cluster_name}",
        )
        for group_name, required_inventory in required_groups.items():
            unsafe_group = group_name in {"unsafe", "continuation"}
            entries = checked_entries(
                cluster.get(group_name),
                expected_keys=(
                    {"id", "text", "expectedCategories"}
                    if unsafe_group
                    else {"id", "text"}
                ),
                context=f"{relative}.clusters.{cluster_name}.{group_name}",
            )
            duplicates = seen_ids & {str(item.get("id")) for item in entries}
            if duplicates:
                error(f"{relative}: duplicate IDs across clusters {sorted(duplicates)!r}")
            seen_ids.update(str(item.get("id")) for item in entries)

            if unsafe_group:
                actual_inventory = {
                    item.get("id"): (
                        item.get("text"),
                        tuple(item.get("expectedCategories", [])),
                    )
                    for item in entries
                }
            else:
                actual_inventory = {
                    item.get("id"): item.get("text")
                    for item in entries
                }
            if actual_inventory != required_inventory:
                error(
                    f"{relative}.{cluster_name}.{group_name}: finite inventory drifted"
                )

            for item in entries:
                identifier, text = item.get("id"), item.get("text")
                if not isinstance(identifier, str) or not isinstance(text, str):
                    continue
                findings = scan_action_text(text, location=identifier)
                if unsafe_group:
                    expected = item.get("expectedCategories")
                    if not isinstance(expected, list) or not all(
                        isinstance(category, str) for category in expected
                    ):
                        error(f"{relative}.{identifier}: invalid expectedCategories")
                    else:
                        actual = sorted({finding.category for finding in findings})
                        if actual != sorted(expected):
                            error(
                                f"{relative}.{identifier}: expected exactly "
                                f"{sorted(expected)!r}, got {actual!r}"
                            )
                elif findings:
                    error(
                        f"{relative}.{identifier}: safe/near-miss text produced "
                        f"findings {findings!r}"
                    )
                deterministic_fields.append((identifier, text))
    return deterministic_fields


def check_normalization_corpus() -> None:
    relative = "tests/fixtures/content-safety/normalization-corpus.json"
    corpus = load_json(relative)
    exact_keys(corpus, {"schemaVersion", "policyVersion", "cases"}, relative)
    if corpus.get("schemaVersion") != FIXTURE_SCHEMA_VERSION or corpus.get("policyVersion") != POLICY_VERSION:
        error(f"{relative}: schemaVersion/policyVersion mismatch")
    cases = corpus.get("cases")
    if not isinstance(cases, list):
        error(f"{relative}.cases: must be an array")
        return
    ids: set[str] = set()
    observed: dict[str, tuple[str, str]] = {}
    for index, item in enumerate(cases):
        context = f"{relative}.cases[{index}]"
        if not isinstance(item, dict):
            error(f"{context}: must be an object")
            continue
        exact_keys(item, {"id", "input", "expected"}, context)
        identifier, text, expected = item.get("id"), item.get("input"), item.get("expected")
        if not all(isinstance(value, str) for value in (identifier, text, expected)):
            error(f"{context}: id/input/expected must be strings")
            continue
        if identifier in ids:
            error(f"{context}: duplicate id {identifier!r}")
        ids.add(identifier)
        observed[identifier] = (text, expected)
        actual = normalize_visible_text(text)
        if actual != expected:
            error(f"{context}: normalized value {actual!r} does not match {expected!r}")
    for identifier, expected_case in REQUIRED_NORMALIZATION_CASES.items():
        if observed.get(identifier) != expected_case:
            error(f"{relative}: required normalization regression {identifier!r} drifted")


def check_host_corpus() -> list[tuple[str, str]]:
    relative = "tests/fixtures/content-safety/host-corpus.json"
    corpus = load_json(relative)
    exact_keys(corpus, {"schemaVersion", "policyVersion", "safe", "unsafe"}, relative)
    if corpus.get("schemaVersion") != FIXTURE_SCHEMA_VERSION or corpus.get("policyVersion") != POLICY_VERSION:
        error(f"{relative}: schemaVersion/policyVersion mismatch")
    safe = checked_entries(
        corpus.get("safe"),
        expected_keys={"id", "text"},
        context=f"{relative}.safe",
    )
    unsafe = checked_entries(
        corpus.get("unsafe"),
        expected_keys={"id", "text", "requiredReason", "forbiddenReason"},
        context=f"{relative}.unsafe",
    )
    unsafe_by_id = {
        item.get("id"): (item.get("text"), item.get("requiredReason"))
        for item in unsafe
    }
    safe_by_id = {item.get("id"): item.get("text") for item in safe}
    for identifier, expected_text in REQUIRED_SAFE_HOST_CASES.items():
        if safe_by_id.get(identifier) != expected_text:
            error(f"{relative}: required safe host regression {identifier!r} drifted")
    for identifier, expected_case in REQUIRED_UNSAFE_HOST_CASES.items():
        if unsafe_by_id.get(identifier) != expected_case:
            error(f"{relative}: required host regression {identifier!r} drifted")
    deterministic_fields: list[tuple[str, str]] = []
    for item in safe:
        identifier, text = item.get("id"), item.get("text")
        if not isinstance(identifier, str) or not isinstance(text, str):
            continue
        findings = scan_host_policy(text, location=identifier)
        if findings:
            error(f"{relative}.{identifier}: safe host/address produced findings {findings!r}")
        deterministic_fields.append((identifier, text))
    for item in unsafe:
        identifier, text = item.get("id"), item.get("text")
        required, forbidden = item.get("requiredReason"), item.get("forbiddenReason")
        if not all(isinstance(value, str) for value in (identifier, text, required, forbidden)):
            error(f"{relative}: unsafe host fields must be strings")
            continue
        findings = scan_host_policy(text, location=identifier)
        reasons = "\n".join(finding.reason for finding in findings)
        if not findings or required not in reasons:
            error(f"{relative}.{identifier}: required diagnostic {required!r} missing")
        if forbidden and forbidden in reasons:
            error(f"{relative}.{identifier}: forbidden diagnostic {forbidden!r} was used")
        if any(finding.category != "network.host_or_address" for finding in findings):
            error(f"{relative}.{identifier}: host finding category drift")
        required_excerpt = REQUIRED_UNSAFE_HOST_EXCERPTS.get(identifier)
        if required_excerpt is not None and not any(
            finding.normalized_excerpt == required_excerpt for finding in findings
        ):
            error(
                f"{relative}.{identifier}: quoted URL excerpt was not preserved as "
                f"{required_excerpt!r}"
            )
        deterministic_fields.append((identifier, text))
    return deterministic_fields


def check_legacy_parity_corpus(path: Path) -> tuple[int, int]:
    """Probe an explicitly supplied historical corpus without making it Policy data."""

    try:
        corpus = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        error(f"{path}: cannot load legacy parity corpus: {exc}")
        return (0, 0)
    if not isinstance(corpus, dict) or set(corpus) != {"unsafe_field", "explicitly_negated_field"}:
        error(f"{path}: legacy parity corpus must contain unsafe_field and explicitly_negated_field")
        return (0, 0)
    unsafe = corpus["unsafe_field"]
    safe = corpus["explicitly_negated_field"]
    if not isinstance(unsafe, list) or not isinstance(safe, list) or not all(
        isinstance(text, str) and text for text in unsafe + safe
    ):
        error(f"{path}: legacy parity entries must be non-empty strings")
        return (0, 0)
    if len(unsafe) != EXPECTED_LEGACY_UNSAFE_COUNT:
        error(
            f"{path}: legacy unsafe count {len(unsafe)} does not match "
            f"{EXPECTED_LEGACY_UNSAFE_COUNT}"
        )
    if len(safe) != EXPECTED_LEGACY_SAFE_COUNT:
        error(
            f"{path}: legacy safe count {len(safe)} does not match "
            f"{EXPECTED_LEGACY_SAFE_COUNT}"
        )
    misses = [text for text in unsafe if not scan_action_text(text, location="legacy-unsafe")]
    false_positives = [text for text in safe if scan_action_text(text, location="legacy-safe")]
    if misses:
        error(f"{path}: legacy unsafe misses={len(misses)} examples={misses[:3]!r}")
    if false_positives:
        error(f"{path}: legacy safe false_positives={len(false_positives)} examples={false_positives[:3]!r}")
    return (len(unsafe), len(safe))


def check_representative_main_fields() -> list[tuple[str, str]]:
    relative = "tests/fixtures/content-safety/representative-main-fields.json"
    corpus = load_json(relative)
    exact_keys(
        corpus,
        {"schemaVersion", "policyVersion", "baselineMain", "scope", "fields"},
        relative,
    )
    if corpus.get("schemaVersion") != FIXTURE_SCHEMA_VERSION or corpus.get("policyVersion") != POLICY_VERSION:
        error(f"{relative}: schemaVersion/policyVersion mismatch")
    if corpus.get("baselineMain") != "a1dfadae153bfe36b88f72e503f5a5be9c64bddf":
        error(f"{relative}: reference baseline main changed without explicit audit")
    if "not whole-book natural-language coverage" not in str(corpus.get("scope", "")):
        error(f"{relative}: bounded-scope disclaimer is missing")
    entries = checked_entries(
        corpus.get("fields"),
        expected_keys={"id", "source", "text"},
        context=f"{relative}.fields",
    )
    actual_ids = {item.get("id") for item in entries}
    if actual_ids != EXPECTED_REPRESENTATIVE_IDS:
        error(
            f"{relative}: representative field inventory drifted: "
            f"expected {len(EXPECTED_REPRESENTATIVE_IDS)}, got {len(actual_ids)}"
        )
    expected_chapters = {"CH02", "CH11", "CH17", "CH25"}
    seen_chapters: set[str] = set()
    seen_source_kinds: dict[str, set[str]] = {chapter: set() for chapter in expected_chapters}
    fields_to_scan: list[tuple[str, str]] = []
    for item in entries:
        identifier, source, text = item.get("id"), item.get("source"), item.get("text")
        if not all(isinstance(value, str) for value in (identifier, source, text)):
            error(f"{relative}: representative fields must use string id/source/text")
            continue
        chapter = identifier.split("-", 1)[0]
        if chapter not in expected_chapters:
            error(f"{relative}.{identifier}: unexpected representative chapter")
        else:
            seen_chapters.add(chapter)
            source_kind = source.split("/", 1)[0]
            seen_source_kinds[chapter].add(source_kind)
        source_path = ROOT / source
        try:
            source_text = source_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            error(f"{relative}.{identifier}: cannot read {source}: {exc}")
            continue
        if text not in source_text:
            error(f"{relative}.{identifier}: selected field is not present verbatim in {source}")
        findings = scan_fields([(identifier, text)])
        if findings:
            error(f"{relative}.{identifier}: canonical field produced false positives {findings!r}")
        fields_to_scan.append((identifier, text))
    if seen_chapters != expected_chapters:
        error(f"{relative}: representative chapters {sorted(seen_chapters)!r} incomplete")
    for chapter in expected_chapters:
        required = {"manuscript", "templates", "cases"}
        if not required <= seen_source_kinds[chapter]:
            error(
                f"{relative}: {chapter} source kinds {sorted(seen_source_kinds[chapter])!r} "
                f"do not include {sorted(required)!r}"
            )
    return fields_to_scan


def check_determinism_and_malformed(fields_to_scan: list[tuple[str, str]]) -> None:
    forward = scan_fields(fields_to_scan)
    reverse = scan_fields(reversed(fields_to_scan))
    if forward != reverse:
        error("scan_fields ordering depends on input order")
    if scan_fields(fields_to_scan + fields_to_scan) != forward:
        error("scan_fields does not deduplicate identical findings deterministically")
    if scan_fields(fields_to_scan) != scan_fields(fields_to_scan):
        error("scan_fields repeated execution is not deterministic")

    malformed_cases: list[Any] = [
        "not-a-field-list",
        [("valid-location", 7)],
        [("only-one-element",)],
        [("", "text")],
        [None],
    ]
    for index, malformed in enumerate(malformed_cases):
        findings = scan_fields(malformed)
        if not findings or not all(f.category == "policy.malformed_input" for f in findings):
            error(f"malformed case {index} did not fail closed: {findings!r}")
    if scan_action_text(None, location="bad-action")[0].category != "policy.malformed_input":  # type: ignore[arg-type]
        error("scan_action_text non-string input did not fail closed")
    if scan_host_policy(None, location="bad-host")[0].category != "policy.malformed_input":  # type: ignore[arg-type]
        error("scan_host_policy non-string input did not fail closed")


def check_documentation() -> None:
    required_files = {
        "CONTENT_SAFETY_POLICY.md": (
            "Policy version: `1.2.0`",
            "## Stable API",
            "## Structured policy model",
            "## Normalization contract",
            "## Protected categories",
            "## Host and address policy",
            "`.localhost`は技術的にはreserved",
            "## Versioning and re-audit",
            "patch:",
            "minor:",
            "1.2.0 finite grammar",
            "Issue #62 Publication coordination correction",
            "## Finite review acceptance contract",
            "Blocking",
            "Non-blocking backlog",
            "major:",
            "## Non-goals",
            "自然言語安全性の完全な判定",
        ),
        "CONTENT_SAFETY_POLICY_MIGRATION.md": (
            "PR #57 / Issue #28",
            "9c4f570064372bf8278e0c53cb47709d298e39bb",
            "Issue #59ではPR #57のbranch",
            "Chapter 3固有のART-14",
            "六つのblocker phrase",
            "`.localhost`",
            "unresolved thread 0",
            "1.2.0 finite grammar re-audit",
            "Issue #62 Publication coordination correction",
            "Issue #67 IPv4 Japanese prose boundary correction",
        ),
    }
    for relative, markers in required_files.items():
        try:
            text = (ROOT / relative).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            error(f"{relative}: cannot read policy documentation: {exc}")
            continue
        for marker in markers:
            if marker not in text:
                error(f"{relative}: missing required marker {marker!r}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--legacy-parity-corpus",
        type=Path,
        help="read-only historical unsafe/safe corpus to probe; not Policy input",
    )
    args = parser.parse_args(argv)
    check_public_api()
    deterministic_fields = check_action_corpus()
    publication_coordination_fields = check_publication_coordination_corpus()
    deterministic_fields.extend(publication_coordination_fields)
    publication_cross_product_cases = check_publication_coordination_cross_product()
    deterministic_fields.extend(check_structural_gap_corpus())
    finite_grammar_fields = check_finite_grammar_1_2_corpus()
    deterministic_fields.extend(finite_grammar_fields)
    check_normalization_corpus()
    deterministic_fields.extend(check_host_corpus())
    representative_fields = check_representative_main_fields()
    deterministic_fields.extend(representative_fields)
    check_determinism_and_malformed(deterministic_fields)
    check_documentation()
    parity_counts: tuple[int, int] | None = None
    if args.legacy_parity_corpus is not None:
        parity_counts = check_legacy_parity_corpus(args.legacy_parity_corpus)
    if errors:
        for message in errors:
            print(f"ERROR: {message}", file=sys.stderr)
        print(f"content safety policy contract failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    summary = (
        "content safety policy contract passed: "
        f"version={POLICY_VERSION}, categories={len(EXPECTED_ALL_CATEGORIES)}, "
        f"blockers={len(BLOCKER_TEXTS)}, finite_grammar_cases={len(finite_grammar_fields)}, "
        f"publication_fixtures={len(publication_coordination_fields)}, "
        f"publication_cross_product_cases={publication_cross_product_cases}, "
        f"representative_fields={len(representative_fields)}"
    )
    if parity_counts is not None:
        summary += (
            "; legacy parity passed: "
            f"unsafe={parity_counts[0]}, explicitly_negated={parity_counts[1]}, "
            "misses=0, false_positives=0"
        )
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
