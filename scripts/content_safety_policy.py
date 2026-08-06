#!/usr/bin/env python3
"""Versioned, chapter-independent public-content safety policy.

The scanner is intentionally bounded.  It evaluates reader-visible fields selected by
chapter adapters; it is not a general natural-language safety classifier.
"""

from __future__ import annotations

from dataclasses import dataclass
import html
import ipaddress
import re
from typing import Iterable, Pattern
import unicodedata
from urllib.parse import urlparse


POLICY_VERSION = "1.0.0"


@dataclass(frozen=True)
class SafetyFinding:
    """A deterministic policy finding returned to a chapter adapter."""

    category: str
    location: str
    normalized_excerpt: str
    reason: str
    policy_version: str = POLICY_VERSION


@dataclass(frozen=True)
class ActionRule:
    """A bounded family of action expressions."""

    kind: str
    expression: Pattern[str]


@dataclass(frozen=True)
class ProtectedObjectRule:
    """A protected object/category and the actions that make it operational."""

    category: str
    expression: Pattern[str]
    action_kinds: frozenset[str]
    synthetic_qualifiable: bool = False


@dataclass(frozen=True)
class _Match:
    start: int
    end: int
    text: str
    category: str
    action_kinds: frozenset[str]
    synthetic_qualifiable: bool


_DASHES = "\u058a\u05be\u1400\u1806\u2010\u2011\u2012\u2013\u2014\u2015\u2e17\u2e1a\u2e3a\u2e3b\u2e40\u301c\u3030\u30a0\ufe31\ufe32\ufe58\ufe63\uff0d"
_SEPARATORS = "_・･"
_CONFUSABLE_FOLD = str.maketrans(
    {
        # Bounded high-risk Latin lookalikes, not a complete confusable map.
        "а": "a",  # Cyrillic
        "е": "e",
        "о": "o",
        "р": "p",
        "с": "c",
        "х": "x",
        "у": "y",
        "і": "i",
        "ј": "j",
        "к": "k",
        "м": "m",
        "т": "t",
        "в": "b",
        "н": "h",
        "α": "a",  # Greek
        "ε": "e",
        "ο": "o",
        "ρ": "p",
        "χ": "x",
        "κ": "k",
        "τ": "t",
    }
)
_CLAUSE_SPLIT = re.compile(r"([,;、。；!?！？\n]+|[.:：](?=\s|$))")
_CONTRAST_PREFIX = re.compile(
    r"^\s*(?:(?:but|however|yet|nevertheless|still|then|and)\b|"
    r"しかし|ただし|だが|一方で|それでも|その後|そして)[,:、\s]*",
    re.IGNORECASE,
)
_PRONOUN_REFERENCE = re.compile(
    r"\b(?:it|its|them|they|the[ ]same(?:[ ](?:object|item|target|data|material))?)\b|"
    r"(?:これ|それ|その(?:使用|利用|配備|導入|実行|作成|構築)|"
    r"当該(?:対象|情報|値|もの)|同じ(?:対象|もの|情報))(?=[をはもへにがの\s])",
    re.IGNORECASE,
)


def _rx(pattern: str) -> Pattern[str]:
    return re.compile(pattern, re.IGNORECASE)


ACTION_RULES = (
    ActionRule(
        "create",
        _rx(
            r"\b(?:write|code|create|creates|created|creating|creation|"
            r"build|builds|built|building|develop|develops|developed|developing|"
            r"implement|implements|implemented|implementing)\b|"
            r"(?:作(?:る|った|ります|らない)|作成|構築|開発|実装)(?:する|した|します|しない|せず)?"
        ),
    ),
    ActionRule(
        "deploy-use",
        _rx(
            r"\b(?:deploy|deploys|deployed|deploying|deployment|install|installs|"
            r"installed|installing|run|runs|ran|running|execute|executes|executed|"
            r"executing|use|uses|used|using|operate|operates|operated|operating)\b|"
            r"(?:配備|導入|実行|使用|利用|運用)(?:する|した|します|しない|せず)?"
        ),
    ),
    ActionRule(
        "access-collect",
        _rx(
            r"\b(?:access|accesses|accessed|accessing|connect|connects|connected|"
            r"connecting|scan|scans|scanned|scanning|probe|probes|probed|probing|"
            r"attack|attacks|attacked|attacking|attempt|attempts|attempted|attempting|"
            r"retrieve|retrieves|retrieved|retrieving|collect|collects|collected|"
            r"collecting|store|stores|stored|storing|share|shares|shared|sharing|"
            r"record|records|recorded|recording|view|views|viewed|viewing|"
            r"modify|modifies|modified|modifying|encrypt|encrypts|encrypted|encrypting|"
            r"delete|deletes|deleted|deleting|steal|steals|stole|stolen|stealing)\b|"
            r"(?:接続|アクセス|走査|スキャン|攻撃|試行|取得|収集|保存|共有|記録|"
            r"閲覧|観測|参照|変更|改変|暗号化|削除|窃取)(?:する|した|します|しない|せず|行う|実施する)?"
        ),
    ),
    ActionRule(
        "perform",
        _rx(
            r"\b(?:perform|performs|performed|performing|conduct|conducts|conducted|"
            r"conducting|launch|launches|launched|launching|cause|causes|caused|causing)\b|"
            r"(?:行う|行わない|実施する|実施しない|仕掛ける|起こす)"
        ),
    ),
    ActionRule(
        "attribute",
        _rx(
            r"\b(?:attribute|attributes|attributed|attributing|identify|identifies|"
            r"identified|identifying|assert|asserts|asserted|conclude|concludes|"
            r"concluded|claim|claims|claimed)\b|"
            r"(?:帰属|特定|断定|同定)(?:する|した|します|しない|せず)?"
        ),
    ),
)


_TARGET = _rx(
    r"(?:real|actual)[ -]?(?:target|system|environment|service|site|tenant|api(?:[ -]endpoint)?)s?|"
    r"(?:third[ -]party|external)[ -]+(?:(?:production|prod|live)[ -]+)?"
    r"(?:targets?|systems?|environments?|data|apis?|api[ -]endpoints?|services?|saas|sites?|tenants?)|"
    r"実(?:在|際)?(?:の)?(?:target|標的|ターゲット|system|システム|環境|tenant|テナント|service|サービス|api)|"
    r"第三者(?:の)?(?:(?:本番|実運用)[ -]*)?(?:target|標的|system|システム|環境|data|データ|api|service|サービス|saas|site|サイト|tenant|テナント)|"
    r"外部(?:の)?(?:(?:本番|実運用)[ -]*)?(?:target|標的|system|システム|環境|data|データ|api|service|サービス|saas|site|サイト|tenant|テナント)"
)
_SECRET = _rx(
    r"\b(?:credentials?|passwords?|passphrases?|tokens?|cookies?|sessions?|secrets?|"
    r"api[ -]?keys?|private[ -]?keys?|access[ -]?keys?|ssh[ -]?keys?)\b|"
    r"(?:実)?(?:credential|クレデンシャル|認証情報|資格情報|token|トークン|cookie|クッキー|"
    r"session|セッション|secret|シークレット|password|パスワード|passphrase|パスフレーズ|"
    r"api[ -]?(?:key|キー)|private[ -]?(?:key|キー|鍵)|アクセス[ -]?(?:キー|鍵))"
)
_PII = _rx(
    r"\b(?:pii|personally[ -]identifiable[ -]information|personal[ -](?:data|information)|"
    r"employee[ -](?:data|information)|customer[ -](?:data|information)|"
    r"e[ -]?mail[ -]address|phone[ -]number|date[ -]of[ -]birth|passport[ -]number|"
    r"national[ -]id|social[ -]security[ -]number|payment[ -]card[ -]number|"
    r"bank[ -]account[ -]number)\b|"
    r"(?:個人(?:情報|データ)|従業員(?:情報|データ)|顧客(?:情報|データ)|メールアドレス|"
    r"電話番号|生年月日|マイナンバー|個人番号|パスポート番号|カード番号|口座番号)"
)
_AUTH_SESSION = _rx(
    r"\b(?:authentication[ -]attempts?|login[ -]attempts?|brute[ -]force|"
    r"session[ -](?:theft|stealing|hijack(?:ing)?|fixation|replay|reuse|takeover)|"
    r"credential[ -](?:theft|stealing|reuse))\b|"
    r"(?:認証試行|ログイン試行|総当たり|ブルート[ -]フォース|"
    r"セッション(?:窃取|乗っ取り|固定|リプレイ|再利用)|認証情報(?:窃取|再利用))"
)
_MALWARE = _rx(
    r"(?<![a-z0-9])(?:deployable[ -]malware|malware|ransomware|wiper|keyloggers?|rootkits?|spyware|"
    r"info[ -]?stealers?|credential[ -]stealers?|backdoors?|trojans?)(?![a-z0-9])|"
    r"(?:マルウェア|ランサムウェア|ワイパー|キーロガー|ルートキット|スパイウェア|"
    r"インフォ[ -]スティーラー|認証情報窃取(?:型)?マルウェア|バックドア|トロイの木馬)"
)
_C2_PHISHING = _rx(
    r"\b(?:c2|c[ ]*&[ ]*c|command[ -](?:and|&)[ -]control|phishing)"
    r"(?:[ -](?:infrastructure|server|site|page|channel|operation|campaign))?\b|"
    r"(?:c2|c[ ]*&[ ]*c|コマンド[ -]アンド[ -]コントロール|フィッシング)"
    r"(?:基盤|インフラ|サーバー|サイト|ページ|通信|接続|運用|攻撃)?"
)
_PRIVILEGE_EVASION = _rx(
    r"\b(?:privilege[ -]escalation|lateral[ -]movement|persistence|persistent[ -]access|"
    r"defen[cs]e[ -]evasion|log[ -](?:deletion|erasure|tampering)|"
    r"audit[ -]trail[ -](?:deletion|erasure|tampering))\b|"
    r"(?:権限昇格|横展開|ラテラルムーブメント|永続化|永続的アクセス|防御回避|検知回避|"
    r"ログ(?:削除|消去|改ざん)|監査証跡(?:削除|消去|改ざん))"
)
_DISRUPTION = _rx(
    r"\b(?:(?:distributed[ -])?denial[ -]of[ -]service|ddos|dos|resource[ -]exhaustion|"
    r"data[ -](?:destruction|modification|encryption)|destructive[ -](?:action|operation))\b|"
    r"(?:ddos|dos)(?=[をへにでのはがも、。；;,.!?！？\s]|$)|"
    r"(?:サービス拒否|資源枯渇|データ(?:破壊|変更|改変|暗号化)|破壊的(?:操作|行為))"
)
_SOCIAL = _rx(
    r"\b(?:social[ -]engineering|doxx(?:ing)?|tracking[ -](?:a[ -])?real[ -]person|"
    r"real[ -]person[ -]tracking)\b|"
    r"(?:ソーシャルエンジニアリング|ドキシング|晒し|実在人物(?:の)?(?:追跡|位置推定))"
)
_WEAK_ATTRIBUTION = _rx(
    r"\b(?:confident(?:ly)?[ -](?:attribute|attribution)|definitive[ -]attribution)"
    r"(?:[ -](?:from|using))?[ -]weak[ -]evidence\b|"
    r"\battribute\b.{0,80}\bconfidently\b.{0,80}\bweak[ -]evidence\b|"
    r"(?:弱い|不十分な)(?:evidence|証拠|根拠)(?:だけ)?(?:から|で)"
    r"(?:断定的に)?(?:帰属|主体|組織|国家)(?:を)?(?:断定|特定|同定)"
)


PROTECTED_OBJECT_RULES = (
    ProtectedObjectRule(
        "target.real_or_external",
        _TARGET,
        frozenset({"create", "deploy-use", "access-collect", "perform"}),
    ),
    ProtectedObjectRule(
        "secret.credential",
        _SECRET,
        frozenset({"create", "deploy-use", "access-collect", "perform"}),
        synthetic_qualifiable=True,
    ),
    ProtectedObjectRule(
        "data.pii",
        _PII,
        frozenset({"create", "deploy-use", "access-collect", "perform"}),
    ),
    ProtectedObjectRule(
        "operation.authentication_or_session",
        _AUTH_SESSION,
        frozenset({"create", "deploy-use", "access-collect", "perform"}),
    ),
    ProtectedObjectRule(
        "operation.malware",
        _MALWARE,
        frozenset({"create", "deploy-use", "perform"}),
    ),
    ProtectedObjectRule(
        "operation.c2_or_phishing",
        _C2_PHISHING,
        frozenset({"create", "deploy-use", "access-collect", "perform"}),
    ),
    ProtectedObjectRule(
        "operation.privilege_or_evasion",
        _PRIVILEGE_EVASION,
        frozenset({"create", "deploy-use", "access-collect", "perform"}),
    ),
    ProtectedObjectRule(
        "operation.disruption_or_destruction",
        _DISRUPTION,
        frozenset({"create", "deploy-use", "access-collect", "perform"}),
    ),
    ProtectedObjectRule(
        "operation.social_engineering_or_tracking",
        _SOCIAL,
        frozenset({"create", "deploy-use", "access-collect", "perform"}),
    ),
    ProtectedObjectRule(
        "analysis.weak_evidence_attribution",
        _WEAK_ATTRIBUTION,
        frozenset({"attribute", "create", "deploy-use", "perform"}),
    ),
)


_SYNTHETIC_PREFIX = re.compile(
    r"(?:^|[\s(（])(?:synthetic|dummy|mock|test[ -]only|reserved|合成|架空|ダミー|模擬|テスト用|予約済み)(?:[\sの-]*)$",
    re.IGNORECASE,
)
_NEGATIVE_SYNTHETIC_PREFIX = re.compile(
    r"(?:not(?:[ ]+a)?[ -]synthetic|non[ -]synthetic|非合成)(?:[\sの-]*)$",
    re.IGNORECASE,
)


def normalize_visible_text(text: str) -> str:
    """Return deterministic normalized reader-visible text.

    NFKC is applied first.  Link destinations and HTML tags are excluded from the
    visible-text action scan; their hosts are evaluated separately.  Separator
    variants are normalized to ASCII hyphen, and case-folding makes matching stable.
    """

    if not isinstance(text, str):
        raise TypeError("text must be str")
    value = html.unescape(unicodedata.normalize("NFKC", text))
    value = "".join(
        character
        for character in value
        if unicodedata.category(character) != "Cf"
    )
    value = re.sub(r"<!--.*?-->", "", value, flags=re.DOTALL)
    value = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"[*~`]", "", value)
    value = value.replace("\\", "")
    value = value.translate(str.maketrans({character: "-" for character in _DASHES}))
    value = value.translate(str.maketrans({character: "-" for character in _SEPARATORS}))
    value = re.sub(r"[\t\r\f\v\u00a0 ]+", " ", value)
    value = re.sub(r" *\n *", "\n", value)
    return value.strip().casefold().translate(_CONFUSABLE_FOLD)


def _finding(category: str, location: str, excerpt: str, reason: str) -> SafetyFinding:
    return SafetyFinding(
        category=category,
        location=location,
        normalized_excerpt=excerpt[:240],
        reason=reason,
    )


def _ordered_unique(findings: Iterable[SafetyFinding]) -> list[SafetyFinding]:
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


def _malformed(location: str, reason: str) -> list[SafetyFinding]:
    return [_finding("policy.malformed_input", location, "<malformed>", reason)]


def _object_matches(clause: str) -> list[_Match]:
    matches: list[_Match] = []
    for rule in PROTECTED_OBJECT_RULES:
        for match in rule.expression.finditer(clause):
            matches.append(
                _Match(
                    start=match.start(),
                    end=match.end(),
                    text=match.group(0),
                    category=rule.category,
                    action_kinds=rule.action_kinds,
                    synthetic_qualifiable=rule.synthetic_qualifiable,
                )
            )
    return sorted(matches, key=lambda item: (item.start, item.end, item.category))


def _action_matches(clause: str, allowed: frozenset[str]) -> list[tuple[int, int, str, str]]:
    matches: list[tuple[int, int, str, str]] = []
    for rule in ACTION_RULES:
        if rule.kind not in allowed:
            continue
        for match in rule.expression.finditer(clause):
            matches.append((match.start(), match.end(), rule.kind, match.group(0)))
    return sorted(matches)


def _direct_synthetic(clause: str, protected: _Match) -> bool:
    if not protected.synthetic_qualifiable:
        return False
    prefix = clause[max(0, protected.start - 32) : protected.start]
    if _NEGATIVE_SYNTHETIC_PREFIX.search(prefix):
        return False
    return bool(_SYNTHETIC_PREFIX.search(prefix))


def _action_is_prohibited(
    clause: str,
    action: tuple[int, int, str, str],
    *,
    scope_start: int,
) -> bool:
    action_start, action_end, _, action_text = action
    before = clause[max(0, scope_start - 48) : scope_start]
    whole = clause.strip()
    action_before = clause[max(0, action_start - 48) : action_start]

    if re.search(r"(?:do not|don't|never|must not|shall not|should not)\s*$", before):
        return True
    if re.search(
        r"(?:is|are|was|were|must|should|shall|may)\s+not(?:\s+be)?\s*$",
        action_before,
    ):
        return True
    if re.search(r"(?:is|are|was|were)\s+forbidden\s+to\s*$", action_before):
        return True
    if _coordinated_pre_action_prohibition_controls_action(clause, action):
        return True
    if _forbidden_to_controls_action(clause, action):
        return True
    if re.search(r"(?:しない|せず|行わない|使わない|作らない)$", action_text):
        return True
    if _trailing_prohibition_controls_action(clause, action, _TRAILING_EN_PROHIBITION):
        return True
    if _trailing_prohibition_controls_action(clause, action, _TRAILING_JA_PROHIBITION):
        return True
    if re.search(r"(?:禁止する対象|prohibited (?:operation|method|data))", before + whole):
        return True
    return False


_FORBIDDEN_TO_MARKER = re.compile(
    r"(?:is|are|was|were)\s+forbidden\s+to\b",
    re.IGNORECASE,
)
_PROHIBITION_SCOPE_BREAK = re.compile(
    r"[,.;:!?、。；：！？]|\b(?:but|however|yet|nevertheless|still|then)\b",
    re.IGNORECASE,
)
_PROHIBITION_COORDINATOR = re.compile(r"\b(?:and|or|nor)\b", re.IGNORECASE)
_NEGATION_COORDINATOR = re.compile(r"\b(?:or|nor)\b", re.IGNORECASE)
_DIRECT_ACTION_PREFIX = re.compile(
    r"\s*(?:(?:to|also|directly|explicitly|only|ever|immediately)\s+)*",
    re.IGNORECASE,
)
_TRAILING_EN_PROHIBITION = re.compile(
    r"\b(?:is|are|was|were|should be|must be)\s+"
    r"(?:prohibited|forbidden|not allowed|outside)\b",
    re.IGNORECASE,
)
_TRAILING_JA_PROHIBITION = re.compile(
    r"(?:禁止(?:する|される|している)|対象外(?!ではない)|許可しない|要求しない)|"
    r"(?:しない|せず|行わない|使わない|用いない|含めない|記載しない|"
    r"接続しない|実施しない|作らない|作ることを禁止する)"
)


def _all_action_matches(clause: str) -> list[tuple[int, int, str, str]]:
    return _action_matches(clause, frozenset(rule.kind for rule in ACTION_RULES))


def _is_direct_action_coordination(
    text: str,
    *,
    coordinator: Pattern[str] = _PROHIBITION_COORDINATOR,
) -> bool:
    """Recognize a bounded coordinator that leads directly to another action."""

    if _PROHIBITION_SCOPE_BREAK.search(text):
        return False
    coordinators = list(coordinator.finditer(text))
    if not coordinators:
        return False
    tail = text[coordinators[-1].end() :]
    return bool(_DIRECT_ACTION_PREFIX.fullmatch(tail))


def _trailing_prohibition_controls_action(
    clause: str,
    action: tuple[int, int, str, str],
    expression: Pattern[str],
) -> bool:
    """Bind a trailing prohibition to this action, not a later action."""

    action_end = action[1]
    trailing = clause[action_end : action_end + 80]
    marker = expression.search(trailing)
    if marker is None:
        return False
    marker_start = action_end + marker.start()
    return not any(
        action_end <= candidate[0] < marker_start
        for candidate in _all_action_matches(clause)
    )


def _coordinated_pre_action_prohibition_controls_action(
    clause: str,
    action: tuple[int, int, str, str],
) -> bool:
    """Carry a local prohibition across a direct action coordination chain."""

    action_start = action[0]
    preceding_actions = [
        candidate for candidate in _all_action_matches(clause)
        if candidate[0] < action_start
    ]
    if not preceding_actions:
        return False
    previous = preceding_actions[-1]
    if not _is_direct_action_coordination(
        clause[previous[1] : action_start],
        coordinator=_NEGATION_COORDINATOR,
    ):
        return False
    return _action_is_prohibited(clause, previous, scope_start=previous[0])


def _forbidden_to_controls_action(
    clause: str,
    action: tuple[int, int, str, str],
) -> bool:
    """Return whether a bounded ``forbidden to`` phrase governs *action*.

    The marker governs its first action and a directly coordinated action in the
    same punctuation-free phrase. A contrast marker, comma, or sentence boundary
    ends that scope; its mere presence earlier in the clause must not suppress a
    later contradictory continuation.
    """

    action_start = action[0]
    markers = list(_FORBIDDEN_TO_MARKER.finditer(clause, 0, action_start))
    if not markers:
        return False
    marker = markers[-1]
    governed_prefix = clause[marker.end() : action_start]
    if _PROHIBITION_SCOPE_BREAK.search(governed_prefix):
        return False

    preceding_actions = [
        match for match in _all_action_matches(clause)
        if marker.end() <= match[0] < action_start
    ]
    if not preceding_actions:
        return bool(_DIRECT_ACTION_PREFIX.fullmatch(governed_prefix))

    coordination = clause[preceding_actions[-1][1] : action_start]
    return _is_direct_action_coordination(coordination)


def _locally_prohibited(clause: str, protected: _Match, action: tuple[int, int, str, str]) -> bool:
    return _action_is_prohibited(
        clause,
        action,
        scope_start=min(protected.start, action[0]),
    )


def _clauses(text: str) -> list[str]:
    text = re.sub(
        r"\s+(?=(?:but|however|yet|nevertheless|and[ ]+then)\b)",
        ",",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"(?<!^)(?=(?:しかし|ただし|だが|一方で|それでも|そして))",
        "、",
        text,
    )
    parts = _CLAUSE_SPLIT.split(text)
    raw = [part.strip() for index, part in enumerate(parts) if index % 2 == 0 and part.strip()]
    clauses: list[str] = []
    index = 0
    while index < len(raw):
        clause = raw[index]
        if _CONTRAST_PREFIX.fullmatch(clause) and index + 1 < len(raw):
            clauses.append(f"{clause} {raw[index + 1]}")
            index += 2
        else:
            clauses.append(clause)
            index += 1
    return clauses


def _continuation_actions(
    clause: str,
    remembered: _Match,
) -> tuple[str, list[tuple[int, int, str, str]]] | None:
    remainder = _CONTRAST_PREFIX.sub("", clause, count=1)
    explicit_contrast = remainder != clause
    actions = _action_matches(remainder, remembered.action_kinds)
    if not actions:
        return None
    pronoun_bound = bool(_PRONOUN_REFERENCE.search(remainder))
    new_objects = _object_matches(remainder)
    trailing = remainder[actions[-1][1] :].strip()
    ellipsis_bound = explicit_contrast and not new_objects and not trailing
    if not (pronoun_bound or ellipsis_bound):
        return None
    return remainder, actions


def scan_action_text(text: str, *, location: str) -> list[SafetyFinding]:
    """Scan one bounded reader-visible field for action-bearing unsafe semantics."""

    if not isinstance(location, str) or not location.strip():
        return _malformed("<unknown>", "location must be a non-empty string")
    if not isinstance(text, str):
        return _malformed(location, "text must be a string")
    try:
        normalized = normalize_visible_text(text)
    except (TypeError, ValueError, UnicodeError) as exc:
        return _malformed(location, f"normalization failed: {type(exc).__name__}")
    if not normalized:
        return []

    findings: list[SafetyFinding] = []
    remembered: _Match | None = None
    for clause in _clauses(normalized):
        if remembered is not None:
            continuation = _continuation_actions(clause, remembered)
            if continuation is not None:
                continuation_text, continuation_matches = continuation
                has_unprohibited_action = any(
                    not _action_is_prohibited(
                        continuation_text,
                        action,
                        scope_start=action[0],
                    )
                    for action in continuation_matches
                )
                if has_unprohibited_action:
                    findings.append(
                        _finding(
                            remembered.category,
                            location,
                            clause,
                            "a contradictory continuation reuses the protected object after a locally negated or prohibitive clause",
                        )
                    )
                    remembered = None
                # Keep the protected object for one more adjacent continuation
                # when every action in this clause is prohibited. This prevents
                # a later contrast or sentence from escaping the local scope.
                continue

        clause_objects = _object_matches(clause)
        next_remembered: _Match | None = None
        for protected in clause_objects:
            actions = _action_matches(clause, protected.action_kinds)
            if not actions:
                continue
            nearest = min(
                actions,
                key=lambda item: min(abs(item[0] - protected.end), abs(protected.start - item[1])),
            )
            if _locally_prohibited(clause, protected, nearest):
                next_remembered = protected
                continue
            if _direct_synthetic(clause, protected):
                continue
            findings.append(
                _finding(
                    protected.category,
                    location,
                    clause,
                    "protected object is paired with an action without a local prohibition or permitted direct synthetic qualifier",
                )
            )
        remembered = next_remembered
    return _ordered_unique(findings)


_ALLOWED_HOST_SUFFIXES = (".example", ".test", ".invalid")
_POLICY_DISALLOWED_RESERVED_SUFFIXES = (".localhost",)
_DOCUMENTATION_NETWORKS = (
    ipaddress.ip_network("192.0.2.0/24"),
    ipaddress.ip_network("198.51.100.0/24"),
    ipaddress.ip_network("203.0.113.0/24"),
    ipaddress.ip_network("2001:db8::/32"),
)
_URL_PATTERN = re.compile(r"(?:(?:[a-z][a-z0-9+.-]*:)?//)[^\s`)>)]+", re.IGNORECASE)
_DOMAIN_PATTERN = re.compile(
    r"(?<![a-z0-9_-])(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}(?![a-z0-9_-])",
    re.IGNORECASE,
)
_IDN_DOMAIN_PATTERN = re.compile(
    r"(?<![\w-])(?:[\w-]+\.)+[\w-]+(?![\w-])",
    re.IGNORECASE,
)


def _parse_ip(value: str) -> ipaddress.IPv4Address | ipaddress.IPv6Address | None:
    try:
        return ipaddress.ip_address(value.strip("[]"))
    except ValueError:
        return None


def _is_documentation_address(address: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    return any(address in network for network in _DOCUMENTATION_NETWORKS)


def _host_finding(location: str, excerpt: str, reason: str) -> SafetyFinding:
    return _finding("network.host_or_address", location, excerpt, reason)


def scan_host_policy(text: str, *, location: str) -> list[SafetyFinding]:
    """Enforce the repository's synthetic host/address publication policy."""

    if not isinstance(location, str) or not location.strip():
        return _malformed("<unknown>", "location must be a non-empty string")
    if not isinstance(text, str):
        return _malformed(location, "text must be a string")
    try:
        normalized = normalize_visible_text(text)
    except (TypeError, ValueError, UnicodeError) as exc:
        return _malformed(location, f"normalization failed: {type(exc).__name__}")

    findings: list[SafetyFinding] = []
    url_hosts: set[str] = set()
    url_addresses: set[str] = set()
    for match in _URL_PATTERN.finditer(unicodedata.normalize("NFKC", text)):
        raw_url = match.group(0).rstrip(".,;、。")
        try:
            host = (urlparse(raw_url).hostname or "").casefold()
        except ValueError:
            findings.append(_host_finding(location, raw_url, "malformed URL in synthetic content"))
            continue
        if not host:
            findings.append(_host_finding(location, raw_url, "URL does not expose a parseable host"))
            continue
        url_hosts.add(host)
        address = _parse_ip(host)
        if address is not None:
            url_addresses.add(str(address))
            if not _is_documentation_address(address):
                findings.append(_host_finding(location, raw_url, "non-documentation IP URL is disallowed"))
        elif host.endswith(_POLICY_DISALLOWED_RESERVED_SUFFIXES):
            findings.append(
                _host_finding(
                    location,
                    raw_url,
                    "host suffix is technically reserved but disallowed by the synthetic publication policy",
                )
            )
        elif not host.endswith(_ALLOWED_HOST_SUFFIXES):
            findings.append(_host_finding(location, raw_url, "non-approved host suffix in synthetic content"))

    for match in _DOMAIN_PATTERN.finditer(normalized):
        domain = match.group(0).casefold()
        if domain in url_hosts:
            continue
        if domain.endswith(_POLICY_DISALLOWED_RESERVED_SUFFIXES):
            findings.append(
                _host_finding(
                    location,
                    domain,
                    "host suffix is technically reserved but disallowed by the synthetic publication policy",
                )
            )
        elif not domain.endswith(_ALLOWED_HOST_SUFFIXES):
            findings.append(_host_finding(location, domain, "possible real domain in synthetic content"))

    for match in _IDN_DOMAIN_PATTERN.finditer(normalized):
        domain = match.group(0).casefold()
        if domain in url_hosts or _DOMAIN_PATTERN.fullmatch(domain):
            continue
        if domain.endswith(_ALLOWED_HOST_SUFFIXES):
            continue
        if not (any(ord(character) > 127 for character in domain) or "xn--" in domain):
            continue
        findings.append(
            _host_finding(
                location,
                domain,
                "non-approved bare IDN or punycode host in synthetic content",
            )
        )

    detected_addresses: dict[str, ipaddress.IPv4Address | ipaddress.IPv6Address] = {}
    raw_normalized = unicodedata.normalize("NFKC", text)
    for raw_token in re.findall(r"[A-Za-z0-9_.:\[\]-]+", raw_normalized):
        token = raw_token.rstrip(".,;")
        forms = {token}
        if token.startswith(":") and not token.startswith("::"):
            forms.add(token[1:])
        labelled = re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.-]*:(.+)", token)
        if labelled:
            forms.add(labelled.group(1))
        for form in forms:
            if "." not in form and ":" not in form:
                continue
            bracketed = re.fullmatch(r"\[([0-9A-Fa-f:.]+)\](?::\d+)?", form)
            ipv4_with_port = re.fullmatch(r"((?:\d{1,3}\.){3}\d{1,3})(?::\d*)?", form)
            candidate = bracketed.group(1) if bracketed else ipv4_with_port.group(1) if ipv4_with_port else form
            address = _parse_ip(candidate)
            if address is not None:
                detected_addresses[str(address)] = address
    for address_text, address in sorted(detected_addresses.items()):
        if address_text in url_addresses:
            continue
        if not _is_documentation_address(address):
            findings.append(_host_finding(location, address_text, "non-documentation IP literal is disallowed"))
    return _ordered_unique(findings)


def scan_fields(fields: Iterable[tuple[str, str]]) -> list[SafetyFinding]:
    """Scan selected fields with deterministic ordering and fail-closed input checks."""

    if isinstance(fields, (str, bytes)):
        return _malformed("<fields>", "fields must be an iterable of (location, text) pairs")
    try:
        materialized = list(fields)
    except Exception:  # fail closed for iterators that raise while materializing
        return _malformed("<fields>", "fields must be iterable")

    findings: list[SafetyFinding] = []
    for index, item in enumerate(materialized):
        if not isinstance(item, (tuple, list)) or len(item) != 2:
            findings.extend(_malformed(f"<fields[{index}]>", "field must contain location and text"))
            continue
        location, text = item
        if not isinstance(location, str) or not location.strip():
            findings.extend(_malformed(f"<fields[{index}]>", "location must be a non-empty string"))
            continue
        if not isinstance(text, str):
            findings.extend(_malformed(location, "text must be a string"))
            continue
        findings.extend(scan_action_text(text, location=location))
        findings.extend(scan_host_policy(text, location=location))
    return _ordered_unique(findings)


__all__ = (
    "POLICY_VERSION",
    "SafetyFinding",
    "normalize_visible_text",
    "scan_action_text",
    "scan_host_policy",
    "scan_fields",
)
