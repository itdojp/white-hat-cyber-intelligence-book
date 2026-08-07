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
from urllib.parse import parse_qsl, urlparse


# 1.1.0 expands the bounded structural grammar and protected-data shapes.  This is
# a semantic extension, so it is deliberately a minor rather than a patch release.
POLICY_VERSION = "1.1.0"


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
    r"しかし|ただし|だが|一方で|それでも|その後|そして|なお)[,:、\s]*",
    re.IGNORECASE,
)
_PRONOUN_REFERENCE = re.compile(
    r"\b(?:it|its|them|they|the[ ]same(?:[ ](?:object|item|target|data|material))?)\b|"
    r"(?:これ|それ|その(?:使用|利用|配備|導入|実行|作成|構築)|"
    r"当該(?:対象|情報|値|もの)|同じ(?:対象|もの|情報))(?=[をはもへにがの\s])",
    re.IGNORECASE,
)
_BLOCK_HTML_TAG = re.compile(
    r"</?(?:address|article|aside|blockquote|br|dd|div|dl|dt|fieldset|figcaption|"
    r"figure|footer|form|h[1-6]|header|hr|li|main|nav|ol|p|pre|section|table|"
    r"tbody|td|tfoot|th|thead|tr|ul)\b[^>]*>",
    re.IGNORECASE,
)
_EN_REFERENCE_TO_ACTION_GAP = re.compile(
    r"\s*(?:(?:is|are|was|were|be|been|being|must|should|shall|may|can|could|"
    r"will|would|not|never|also|directly|explicitly|only|ever|immediately|"
    r"forbidden|prohibited|to)\s+)*",
    re.IGNORECASE,
)
_JA_REFERENCE_TO_ACTION_GAP = re.compile(r"[をはもへにがの、\s]*(?:直接|明示的に)?\s*")
_EN_ACTION_TO_REFERENCE_GAP = re.compile(r"^(?:(?:to|with|on|from)\s+)?", re.IGNORECASE)


def _rx(pattern: str) -> Pattern[str]:
    return re.compile(pattern, re.IGNORECASE)


def _mixed_script_action(pattern: str) -> str:
    """Preserve English word bounds and add only a Japanese-suffix form.

    Python treats Japanese letters as word characters, so ``\b`` cannot see the
    boundary in reader-visible forms such as ``deployする``.  The repository's
    bounded mixed-script contract adds that explicit form without widening the
    existing English branch or accepting a suffix inside an ASCII identifier.
    """

    return (
        rf"\b(?:{pattern})\b|"
        rf"(?<![a-z0-9_-])(?:{pattern})"
        r"(?:してください|して(?!ください)|する|した|します|しない|せず)"
        r"(?![a-z0-9_-])"
    )


ACTION_RULES = (
    ActionRule(
        "create",
        _rx(
            _mixed_script_action(
                r"write|code|create|creates|created|creating|creation|"
                r"build|builds|built|building|develop|develops|developed|developing|"
                r"implement|implements|implemented|implementing|"
                r"establish|establishes|established|establishing|automate|automates|"
                r"automated|automating"
            )
            + r"|"
            r"(?:作(?:る|った|って(?:ください)?|ります|らない)|作成|構築|開発|実装)(?:する|した|します|しない|せず)?"
        ),
    ),
    ActionRule(
        "deploy-use",
        _rx(
            _mixed_script_action(
                r"deploy|deploys|deployed|deploying|deployment|install|installs|"
                r"installed|installing|run|runs|ran|running|execute|executes|executed|"
                r"executing|use|uses|used|using|operate|operates|operated|operating|"
                r"log[ -]?in|sign[ -]?in|authenticate|authenticates|authenticated|authenticating"
            )
            + r"|"
            r"(?:配備|導入|実行|使用|利用|運用)(?:する|した|します|しない|せず)?"
        ),
    ),
    ActionRule(
        "access-collect",
        _rx(
            _mixed_script_action(
                r"access|accesses|accessed|accessing|connect|connects|connected|"
                r"connecting|scan|scans|scanned|scanning|probe|probes|probed|probing|"
                r"attack|attacks|attacked|attacking|attempt|attempts|attempted|attempting|"
                r"retrieve|retrieves|retrieved|retrieving|collect|collects|collected|"
                r"collecting|store|stores|stored|storing|share|shares|shared|sharing|"
                r"record|records|recorded|recording|view|views|viewed|viewing|"
                r"send|sends|sent|sending|replace|replaces|replaced|replacing|"
                r"modify|modifies|modified|modifying|encrypt|encrypts|encrypted|encrypting|"
                r"delete|deletes|deleted|deleting|steal|steals|stole|stolen|stealing"
            )
            + r"|"
            r"(?:接続|アクセス|走査|スキャン|攻撃|試行|取得|収集|保存|共有|記録|"
            r"閲覧|観測|参照|変更|改変|暗号化|削除|窃取|送信|置換)(?:する|した|します|しない|せず|行う|実施する)?"
        ),
    ),
    ActionRule(
        "analyze",
        _rx(
            _mixed_script_action(
                r"analy[sz]e|analy[sz]es|analy[sz]ed|analy[sz]ing|analysis"
            )
            + r"|(?:分析|解析)(?:する|した|します|しない|せず|行う|実施する)?"
        ),
    ),
    ActionRule(
        "perform",
        _rx(
            _mixed_script_action(
                r"perform|performs|performed|performing|conduct|conducts|conducted|"
                r"conducting|launch|launches|launched|launching|cause|causes|caused|causing|"
                r"publish|publishes|published|publishing|announce|announces|announced|announcing"
            )
            + r"|"
            r"(?:行う|行わない|実施する|実施しない|仕掛ける|起こす|確立する|自動化する|"
            r"公開(?:する|した|します|しない|せず)|発生させる|公表する|試す|"
            r"ログインする|サインインする|認証する|"
            r"操作(?:する|した|します|しない|せず)|操作(?=なし))"
            r"(?:する|した|します|しない|せず)?"
        ),
    ),
    ActionRule(
        "attribute",
        _rx(
            _mixed_script_action(
                r"attribute|attributes|attributed|attributing|identify|identifies|"
                r"identified|identifying|assert|asserts|asserted|conclude|concludes|"
                r"concluded|claim|claims|claimed"
            )
            + r"|"
            r"(?:帰属|特定|断定|同定)(?:する|した|します|しない|せず)?"
        ),
    ),
)


_LATIN_LEFT = r"(?<![a-z0-9])"
_LATIN_RIGHT = r"(?![a-z0-9])"


_TARGET = _rx(
    r"(?:real|actual)[ -]?(?:target|system|environment|service|site|tenant|api(?:[ -]endpoint)?)s?|"
    r"(?:third[ -]party|external)[ -]+(?:(?:production|prod|live)[ -]+)?"
    r"(?:targets?|systems?|environments?|data|apis?|api[ -]endpoints?|services?|saas|sites?|tenants?)|"
    r"実(?:在|際)?\s*(?:の\s*)?(?:target|標的|ターゲット|system|システム|環境|tenant|テナント|service|サービス|api)|"
    r"(?:第三者|外部|他社)\s*(?:の\s*)?(?:(?:本番|実運用)\s*[ -]*)?(?:target|標的|system|システム|環境|data|データ|api(?:\s*エンドポイント)?|service|サービス|saas|site|サイト|tenant|テナント)"
)
_SECRET = _rx(
    _LATIN_LEFT + r"(?:credentials?|passwords?|passphrases?|tokens?|cookies?|sessions?|secrets?|"
    r"api[ -]?keys?|private[ -]?keys?|access[ -]?keys?|ssh[ -]?keys?|"
    r"bearer[ -]?(?:tokens?|jwt)|jwts?|session[ -]?ids?)" + _LATIN_RIGHT + r"|"
    r"(?:実)?(?:credential|クレデンシャル|認証情報|資格情報|token|トークン|cookie|クッキー|"
    r"session|セッション|secret|シークレット|password|パスワード|passphrase|パスフレーズ|"
    r"api[ -]?(?:key|キー)|private[ -]?(?:key|キー|鍵)|アクセス[ -]?(?:キー|鍵))"
)
_PII = _rx(
    _LATIN_LEFT + r"(?:pii|personally[ -]identifiable[ -]information|personal[ -](?:data|information|info)|"
    r"employee[ -](?:data|information|info)|customer[ -](?:data|information|info)|"
    r"e[ -]?mail[ -]address|phone[ -]number|date[ -]of[ -]birth|passport[ -]number|"
    r"national[ -]id|social[ -]security[ -]number|payment[ -]card[ -]number|"
    r"bank[ -]account[ -]number|full[ -]name|home[ -]address|credit[ -]card[ -]number)" + _LATIN_RIGHT + r"|"
    r"(?:個人(?:情報|データ)|(?:従業員|顧客)\s*(?:の\s*)?(?:情報|データ)|メールアドレス|"
    r"電話番号|氏名|住所|生年月日|マイナンバー|個人番号|パスポート番号|(?:クレジット\s*)?カード番号|口座番号)"
)
_AUTH_SESSION = _rx(
    _LATIN_LEFT + r"(?:authentication[ -]attempts?|auth[ -]attempts?|login[ -]attempts?|"
    r"(?:login|authentication)[ -]brute[ -]force|brute[ -]force[ -](?:login|authentication)|"
    r"mfa[ -]fatigue|(?:login|sign[ -]in)(?=(?:する|を(?:試す|行う|実施する)))|"
    r"session[ -](?:theft|stealing|hijack(?:ing)?|fixation|replay|reuse|takeover)|"
    r"credential[ -](?:theft|stealing|reuse))" + _LATIN_RIGHT + r"|"
    r"(?:mfa\s*疲労(?:攻撃)?|認証試行|ログイン試行|(?:認証|ログイン|サインイン)(?=(?:を)?(?:試す|行う|実施する|する))|総当たり|ブルート[ -]?フォース(?:ログイン|認証)?|"
    r"セッション(?:窃取|乗っ取り|固定|リプレイ|再利用)|認証情報(?:窃取|再利用))"
)
_MALWARE = _rx(
    _LATIN_LEFT + r"(?:deployable[ -]malware|malware|ransomware|wiper|keyloggers?|rootkits?|spyware|"
    r"info[ -]?stealers?|credential[ -]stealers?|backdoors?|trojans?|stealth[ -]tooling)" + _LATIN_RIGHT + r"|"
    r"(?:マルウェア|ランサムウェア|ワイパー|キーロガー|ルートキット|スパイウェア|"
    r"インフォ[ -]?スティーラー|認証情報窃取(?:型)?マルウェア|バックドア|トロイの木馬|ステルスツール)"
)
_C2_PHISHING = _rx(
    _LATIN_LEFT + r"(?:c2|c[ ]*&[ ]*c|command[ -](?:and|&)[ -]control|phishing)"
    r"(?:[ -](?:infrastructure|server|site|page|channel|operation|campaign))?" + _LATIN_RIGHT + r"|"
    r"(?:c2|c\s*&\s*c|コマンド\s*[ -]?\s*アンド\s*[ -]?\s*コントロール|フィッシング)"
    r"(?:基盤|インフラ|サーバー|サイト|ページ|通信|接続|運用|攻撃)?"
)
_PRIVILEGE_EVASION = _rx(
    _LATIN_LEFT + r"(?:privilege[ -]escalation|lateral[ -]movement|persistence|persistent[ -]access|"
    r"defen[cs]e[ -]evasion|log[ -](?:deletion|erasure|tampering)|"
    r"audit[ -]trail[ -](?:deletion|erasure|tampering))" + _LATIN_RIGHT + r"|"
    r"(?:権限昇格|横展開|ラテラルムーブメント|永続化|永続的アクセス|防御回避|検知回避|"
    r"ログ(?:削除|消去|改ざん)|監査証跡(?:削除|消去|改ざん))"
)
_DISRUPTION = _rx(
    _LATIN_LEFT + r"(?:(?:distributed[ -])?denial[ -]of[ -]service|ddos|dos|resource[ -]exhaustion|"
    r"(?:unauthorized[ -])?data[ -](?:destruction|modification|encryption)|destructive[ -](?:action|operation)|encryption|"
    r"encrypt(?:s|ing)?(?:[ ]+the)?[ ]+data|encrypted[ ]+the[ ]+data)" + _LATIN_RIGHT + r"|"
    r"(?:ddos|dos)(?=[をへにでのはがも、。；;,.!?！？\s]|$)|"
    r"(?:サービス拒否|資源枯渇|データ(?:を)?暗号化(?:する|した|します)?|"
    r"データ(?:破壊|変更|改変|暗号化)|破壊的(?:操作|行為))"
)
_SOCIAL = _rx(
    _LATIN_LEFT + r"(?:social[ -]engineering|doxx(?:ing)?|tracking[ -](?:a[ -])?real[ -]person|"
    r"real[ -]person[ -]tracking|impersonation|anonymi[sz]ation[ -]infrastructure|dark[ -]web[ -]infiltration)" + _LATIN_RIGHT + r"|"
    r"(?:ソーシャルエンジニアリング|ドキシング|晒し|なりすまし|匿名化基盤|ダークウェブ(?:への)?直接潜入|実在人物(?:の)?(?:追跡|位置推定))"
)
_WEAK_ATTRIBUTION = _rx(
    _LATIN_LEFT + r"(?:confident(?:ly)?[ -](?:attribute|attribution)|definitive[ -]attribution)"
    r"(?:[ -](?:from|using))?[ -]weak[ -]evidence" + _LATIN_RIGHT + r"|" +
    _LATIN_LEFT + r"attribute" + _LATIN_RIGHT + r".{0,80}" + _LATIN_LEFT + r"confidently" + _LATIN_RIGHT + r".{0,80}" + _LATIN_LEFT + r"weak[ -]evidence" + _LATIN_RIGHT + r"|"
    + _LATIN_LEFT + r"weak[ -]evidence" + _LATIN_RIGHT
    + r"(?:から(?:の)?|で)(?:断定的(?:に)?(?:帰属|主体|組織|国家)|"
    + r"(?:断定的(?:に)?)?(?:帰属|主体|組織|国家)(?:を)?(?:断定|特定|同定))|"
    r"(?:弱い|不十分な)(?:evidence|証拠|根拠)(?:だけ)?(?:から(?:の)?|で)"
    r"(?:断定的(?:に)?(?:帰属|主体|組織|国家)|(?:断定的(?:に)?)?(?:帰属|主体|組織|国家)(?:を)?(?:断定|特定|同定))"
)


PROTECTED_OBJECT_RULES = (
    ProtectedObjectRule(
        "target.real_or_external",
        _TARGET,
        frozenset({"create", "deploy-use", "access-collect", "perform", "analyze"}),
    ),
    ProtectedObjectRule(
        "secret.credential",
        _SECRET,
        frozenset({"create", "deploy-use", "access-collect", "analyze", "perform"}),
        synthetic_qualifiable=True,
    ),
    ProtectedObjectRule(
        "data.pii",
        _PII,
        frozenset({"create", "deploy-use", "access-collect", "perform", "analyze"}),
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
    # Block tags create a rendered boundary. Inline tags do not: adjacent inline
    # nodes such as ``<span>key</span><span>logger</span>`` render as one token.
    value = _BLOCK_HTML_TAG.sub("\n", value)
    value = re.sub(r"<[^>]+>", "", value)
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


def _action_has_direct_reference(
    text: str,
    action: tuple[int, int, str, str],
) -> bool:
    """Bind a pronoun only when it is the action's direct object or subject."""

    action_start, action_end, _, _ = action
    tail = text[action_end : action_end + 32].lstrip()
    tail = _EN_ACTION_TO_REFERENCE_GAP.sub("", tail, count=1)
    if _PRONOUN_REFERENCE.match(tail):
        return True

    window_start = max(0, action_start - 48)
    window = text[window_start:action_end]
    for reference in _PRONOUN_REFERENCE.finditer(window):
        absolute_start = window_start + reference.start()
        absolute_end = window_start + reference.end()
        if absolute_start <= action_start < absolute_end:
            return True
        if absolute_end > action_start:
            continue
        gap = text[absolute_end:action_start]
        if reference.group(0).isascii():
            if _EN_REFERENCE_TO_ACTION_GAP.fullmatch(gap):
                return True
        elif _JA_REFERENCE_TO_ACTION_GAP.fullmatch(gap):
            return True
    return False


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
    if _pre_action_prohibition_controls_action(clause, action):
        return True
    if re.search(r"(?:しない|せず|行わない|使わない|作らない)$", action_text):
        return True
    # Japanese negative predicates can follow a bare action stem (for example,
    # ``作るべきではない`` and ``実Target操作なし``).  Keep this local: a later
    # action or a clause boundary still ends the negative scope.
    direct_tail = clause[action_end : action_end + 24]
    if re.match(r"\s*(?:べきではない|べからず|なし)(?=$|[、。；;,.!?！？\s])", direct_tail):
        return True
    if _trailing_prohibition_controls_action(clause, action, _TRAILING_EN_PROHIBITION):
        return True
    if _trailing_prohibition_controls_action(clause, action, _TRAILING_JA_PROHIBITION):
        return True
    return False


_PRE_ACTION_PROHIBITION_MARKER = re.compile(
    r"(?:is|are|was|were)\s+"
    r"(?:forbidden\s+to|(?:forbidden|prohibited)\s+from)\b",
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
    r"(?:a\s+)?(?:prohibited|forbidden|not allowed|outside)\b",
    re.IGNORECASE,
)
_TRAILING_JA_PROHIBITION = re.compile(
    r"(?:禁止(?:する|される|している)|対象外(?!ではない)|許可しない|要求しない)|"
    r"(?:しない|せず|行わない|使わない|用いない|含めない|記載しない|"
    r"接続しない|実施しない|作らない|作ることを禁止する|"
    r"はいけない|はならない|(?:処理|操作|機能|方法|手順)(?:は|を)?扱わない)"
)


def _direct_trailing_prohibition_end(
    clause: str,
    action: tuple[int, int, str, str],
) -> int | None:
    """Return a local trailing marker end before any intervening action."""

    action_end = action[1]
    trailing = clause[action_end : action_end + 80]
    ends: list[int] = []
    for expression in (_TRAILING_EN_PROHIBITION, _TRAILING_JA_PROHIBITION):
        marker = expression.search(trailing)
        if marker is None:
            continue
        marker_start = action_end + marker.start()
        if any(
            action_end <= candidate[0] < marker_start
            for candidate in _all_action_matches(clause)
        ):
            continue
        ends.append(action_end + marker.end())
    return min(ends) if ends else None


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
    if any(
        action_end <= candidate[0] < marker_start
        for candidate in _all_action_matches(clause)
    ):
        return False
    marker_end = action_end + marker.end()
    suffix = clause[marker_end:]
    scope_break = _PROHIBITION_SCOPE_BREAK.search(suffix)
    scope_end = marker_end + (scope_break.start() if scope_break else len(suffix))
    later_actions = [
        candidate
        for candidate in _all_action_matches(clause)
        if marker_end <= candidate[0] < scope_end
    ]
    if not later_actions:
        return True

    # A marker complement such as ``prohibited from deployment`` introduces a
    # different action and cannot prohibit the earlier one.  Preserve a bounded
    # list of independently prohibited coordinated actions by requiring each
    # later action to have its own direct marker.
    cursor = marker_end
    for candidate in later_actions:
        if not re.fullmatch(
            r"\s*(?:and|or|nor)\s+(?:(?:its|their|the)\s+)?",
            clause[cursor : candidate[0]],
            re.IGNORECASE,
        ):
            return False
        own_marker_end = _direct_trailing_prohibition_end(clause, candidate)
        if own_marker_end is None:
            return False
        cursor = own_marker_end
    return True


def _coordinated_pre_action_prohibition_controls_action(
    clause: str,
    action: tuple[int, int, str, str],
) -> bool:
    """Carry a local prohibition across a direct action coordination chain."""

    current = action
    preceding_actions = [
        candidate for candidate in _all_action_matches(clause)
        if candidate[0] < action[0]
    ]
    if not preceding_actions:
        return False

    def has_direct_prohibition(candidate: tuple[int, int, str, str]) -> bool:
        before = clause[max(0, candidate[0] - 48) : candidate[0]]
        if re.search(r"(?:do not|don't|never|must not|shall not|should not)\s*$", before):
            return True
        if re.search(
            r"(?:is|are|was|were|must|should|shall|may)\s+not(?:\s+be)?\s*$",
            before,
        ):
            return True
        return bool(re.search(r"(?:しない|せず|行わない|使わない|作らない)$", candidate[3]))

    for previous in reversed(preceding_actions):
        if not _is_direct_action_coordination(
            clause[previous[1] : current[0]],
            coordinator=_NEGATION_COORDINATOR,
        ):
            return False
        current = previous
        # Stop as soon as the directly coordinated chain reaches its local
        # prohibition. Earlier, unrelated actions in the same clause must not
        # absorb or invalidate this bounded scope.
        if has_direct_prohibition(current):
            return True
    return False


def _pre_action_prohibition_controls_action(
    clause: str,
    action: tuple[int, int, str, str],
) -> bool:
    """Return whether a bounded pre-action prohibition governs *action*.

    ``forbidden to`` and ``prohibited/forbidden from`` govern their first action
    and a directly coordinated action in the same punctuation-free phrase. A
    contrast marker, comma, or sentence boundary ends that scope; its mere
    presence earlier in the clause must not suppress a later contradictory
    continuation.
    """

    action_start = action[0]
    markers = list(_PRE_ACTION_PROHIBITION_MARKER.finditer(clause, 0, action_start))
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


_MODIFIER_CONTRAST_SENTINEL = "__bounded_modifier_contrast__"
_CLAUSE_BOUNDARY = re.compile(r"[,;、。；!?！？\n]+|[.:：](?=\s|$)")


def _mask_bounded_modifier_contrasts(text: str) -> str:
    """Keep ``but`` inside a bounded action-to-object modifier span.

    Contrast splitting remains the default.  The exception requires a protected
    object after ``but``, a relevant action before it, no intervening relevant
    action, and a modifier-only gap accepted by the finite gap grammar.
    """

    masked = text
    offset = 0
    for marker in list(re.finditer(r"\bbut\b", text, re.IGNORECASE)):
        preceding_boundaries = list(_CLAUSE_BOUNDARY.finditer(text, 0, marker.start()))
        segment_start = preceding_boundaries[-1].end() if preceding_boundaries else 0
        following_boundary = _CLAUSE_BOUNDARY.search(text, marker.end())
        segment_end = following_boundary.start() if following_boundary else len(text)
        segment = text[segment_start:segment_end]
        local_marker_start = marker.start() - segment_start
        local_marker_end = marker.end() - segment_start

        protect = False
        for protected in _object_matches(segment):
            if protected.start <= local_marker_end:
                continue
            actions = _action_matches(segment, protected.action_kinds)
            if any(
                local_marker_end <= action[0] < protected.start
                for action in actions
            ):
                continue
            for action in reversed(actions):
                if action[1] > local_marker_start:
                    continue
                if _bounded_action_to_object_gap(
                    segment[action[1] : protected.start]
                ):
                    protect = True
                    break
            if protect:
                break
        if not protect:
            continue
        start = marker.start() + offset
        end = marker.end() + offset
        masked = masked[:start] + _MODIFIER_CONTRAST_SENTINEL + masked[end:]
        offset += len(_MODIFIER_CONTRAST_SENTINEL) - (end - start)
    return masked


def _clauses(text: str) -> list[str]:
    text = _mask_bounded_modifier_contrasts(text)
    text = re.sub(
        r"\s+(?=(?:but|however|yet|nevertheless|still|then|and[ ]+then)\b)",
        ",",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"(?<!^)(?=(?:しかし|ただし|だが|一方で|それでも|その後|そして))",
        "、",
        text,
    )
    parts = _CLAUSE_SPLIT.split(text)
    raw = [
        part.strip().replace(_MODIFIER_CONTRAST_SENTINEL, "but")
        for index, part in enumerate(parts)
        if index % 2 == 0 and part.strip()
    ]
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
    # The first relevant action must bind the remembered object directly. A
    # pronoun attached to a later action may refer to a new intervening object.
    pronoun_bound = _action_has_direct_reference(remainder, actions[0])
    new_objects = _object_matches(remainder)
    trailing = remainder[actions[-1][1] :].strip()
    # A punctuation-separated Japanese action stem can omit the already-negated
    # object only when the continuation is itself just that action.  This rejects
    # ``Tokenは使用しない、取得する`` without rebinding benign prose such as
    # ``結果だけを記録する`` to Token.
    bare_ellipsis = (
        not explicit_contrast
        and not new_objects
        and len(actions) == 1
        and not remainder[: actions[0][0]].strip()
        and not trailing
    )
    ellipsis_bound = (explicit_contrast and not new_objects and not trailing) or bare_ellipsis
    if not (pronoun_bound or ellipsis_bound):
        return None
    return remainder, actions


_ACTION_TO_OBJECT_DETERMINERS = frozenset(
    {"a", "an", "the", "this", "that", "these", "those"}
)
_ACTION_TO_OBJECT_COORDINATORS = frozenset({"and", "or", "nor", "but"})
_ACTION_TO_OBJECT_BREAKERS = frozenset(
    {
        "to",
        "because",
        "while",
        "although",
        "though",
        "unless",
        "if",
        "when",
        "where",
        "whose",
        "who",
        "which",
    }
)
_ASCII_MODIFIER = re.compile(r"[a-z][a-z0-9-]*", re.IGNORECASE)
_JA_MODIFIER = re.compile(r"[ぁ-んァ-ヶ一-龯a-z0-9 -]+", re.IGNORECASE)
_JA_STANDALONE_MODIFIERS = frozenset(
    {"この", "その", "当該", "合成", "架空", "ダミー", "模擬", "テスト用"}
)
_EN_OBJECT_TO_ACTION_GAP = re.compile(
    r"\s*(?:(?:that|which|who|we|it|is|are|was|were|be|been|being|must|should|"
    r"shall|may|can|could|will|would|not|never|also|directly|explicitly|only|"
    r"ever|immediately|then)\s+)*",
    re.IGNORECASE,
)
_EN_RELATIVE_PREDICATE_GAP = re.compile(
    r"\s*(?:(?:is|are|was|were|be|been|being|must|should|shall|may|can|could|"
    r"will|would|not|never|also|directly|explicitly|only|ever|immediately|then)\s+)*",
    re.IGNORECASE,
)
_EN_DIRECT_OBJECT_PREFIX = re.compile(
    r"\s+(?:a|an|the|this|that|these|those)\s+",
    re.IGNORECASE,
)
_EN_DIRECT_OBJECT_TOKEN = re.compile(r"[a-z][a-z0-9-]*\b", re.IGNORECASE)
_EN_DIRECT_OBJECT_BREAKERS = frozenset(
    {"to", "in", "on", "at", "for", "from", "with", "without", "by", "because"}
)
_EN_TEMPORAL_HEADS = frozenset(
    {
        "second",
        "minute",
        "hour",
        "day",
        "week",
        "month",
        "quarter",
        "year",
        "morning",
        "afternoon",
        "evening",
        "night",
        "time",
        "moment",
    }
)
_EN_TEMPORAL_QUALIFIERS = frozenset(
    {
        "this",
        "that",
        "these",
        "those",
        "next",
        "last",
        "following",
        "same",
        "each",
        "every",
        "very",
        "business",
        "calendar",
        "working",
        "previous",
        "coming",
        "current",
    }
)
_JA_DIRECT_ACTION_CONTINUATION = re.compile(
    r"^(?:で|て|し|して|せず|つつ|が|けれど|けれども|ものの)\s*$"
)


def _bounded_action_to_object_gap(gap: str) -> bool:
    """Recognize a finite noun-modifier span without parsing a full sentence."""

    stripped = gap.strip()
    if not stripped:
        return True
    if len(stripped) > 96 or re.search(r"[,.;:!?、。；：！？\n]", stripped):
        return False
    if _all_action_matches(stripped):
        return False

    tokens = stripped.casefold().split()
    if tokens and all(_ASCII_MODIFIER.fullmatch(token) for token in tokens):
        if tokens[0] in _ACTION_TO_OBJECT_DETERMINERS:
            tokens = tokens[1:]
        if not tokens:
            return True
        if any(token in _ACTION_TO_OBJECT_DETERMINERS for token in tokens):
            return False
        if len(tokens) > 7 or any(
            token in _ACTION_TO_OBJECT_BREAKERS for token in tokens
        ):
            return False
        for index, token in enumerate(tokens):
            if token not in _ACTION_TO_OBJECT_COORDINATORS:
                continue
            if index == 0 or index == len(tokens) - 1:
                return False
            if tokens[index - 1] in _ACTION_TO_OBJECT_COORDINATORS:
                return False
            if tokens[index + 1] in _ACTION_TO_OBJECT_COORDINATORS:
                return False
        return True

    if not _JA_MODIFIER.fullmatch(stripped) or len(stripped) > 32:
        return False
    if any(particle in stripped for particle in ("を", "へ", "は", "も", "が")):
        return False
    return stripped in _JA_STANDALONE_MODIFIERS or stripped.endswith(
        ("な", "の", "い", "用", "型", "的")
    )


def _action_directly_precedes_object(
    clause: str,
    action: tuple[int, int, str, str],
    protected: _Match,
) -> bool:
    if action[1] > protected.start:
        return action[0] < protected.end
    gap = clause[action[1] : protected.start]
    return _bounded_action_to_object_gap(gap)


def _action_directly_follows_object(
    clause: str,
    protected: _Match,
    action: tuple[int, int, str, str],
) -> bool:
    if action[0] < protected.end:
        return action[1] > protected.start
    if _action_introduces_distinct_english_object(clause, action):
        return False
    gap = clause[protected.end : action[0]]
    return bool(
        _EN_OBJECT_TO_ACTION_GAP.fullmatch(gap)
        or _JA_REFERENCE_TO_ACTION_GAP.fullmatch(gap)
    )


def _action_introduces_distinct_english_object(
    clause: str,
    action: tuple[int, int, str, str],
) -> bool:
    tail = clause[action[1] :]
    prefix = _EN_DIRECT_OBJECT_PREFIX.match(tail)
    if prefix is None:
        return False
    words: list[str] = []
    cursor = prefix.end()
    while len(words) < 4:
        token = _EN_DIRECT_OBJECT_TOKEN.match(tail, cursor)
        if token is None:
            break
        word = token.group(0).casefold()
        if word in _EN_DIRECT_OBJECT_BREAKERS:
            break
        words.append(word)
        cursor = token.end()
        whitespace = re.match(r"\s+", tail[cursor:])
        if whitespace is None:
            break
        cursor += whitespace.end()
    if not words:
        return False
    # A trailing temporal phrase modifies the action; it is not the action's
    # direct object.  Remove that bounded phrase before deciding whether an
    # earlier noun remains (for example, ``the sandbox this week``).
    if words[-1] in _EN_TEMPORAL_HEADS:
        words.pop()
        while words and words[-1] in _EN_TEMPORAL_QUALIFIERS:
            words.pop()
    return bool(words)


def _actions_bound_to_object(
    clause: str,
    protected: _Match,
    actions: list[tuple[int, int, str, str]],
) -> list[tuple[int, int, str, str]]:
    """Select bounded action candidates on both sides of one protected object.

    This is deliberately not a dependency parser.  Direct action/object gaps seed
    the association, then only a bounded relative-predicate or existing
    same-object continuation can extend it.  This keeps an unrelated later action
    (for example, using a sandbox) from rebinding the protected object.
    """

    bound = [
        action
        for action in actions
        if _action_directly_precedes_object(clause, action, protected)
        or _action_directly_follows_object(clause, protected, action)
    ]
    if not bound:
        # Preserve the previous fail-closed behavior for an unusual bounded field
        # that contains an object and action but no recognized direct gap.
        bound.append(
            min(
                actions,
                key=lambda item: min(
                    abs(item[0] - protected.end),
                    abs(protected.start - item[1]),
                ),
            )
        )

    relative_after_object = bool(
        re.search(
            r"\b(?:that|which|who)\b",
            clause[protected.end : max(action[1] for action in bound)],
            re.IGNORECASE,
        )
    )
    changed = True
    while changed:
        changed = False
        for anchor in tuple(sorted(bound)):
            for candidate in actions:
                if candidate in bound or candidate[0] <= anchor[0]:
                    continue
                between = clause[anchor[1] : candidate[0]]
                # A later pronoun can belong to a new object (for example, "use a
                # sandbox because it is isolated") and must not rebind the
                # protected object without direct coordination.
                pronoun_bound = _action_has_direct_reference(clause, candidate)
                direct_english = _is_direct_action_coordination(between) and pronoun_bound
                direct_japanese = bool(_JA_DIRECT_ACTION_CONTINUATION.fullmatch(between)) or (
                    not between and anchor[3].endswith("せず")
                )
                relative_predicate = (
                    relative_after_object
                    and anchor[0] >= protected.end
                    and bool(_EN_RELATIVE_PREDICATE_GAP.fullmatch(between))
                )
                if direct_english or direct_japanese or relative_predicate:
                    bound.append(candidate)
                    changed = True
    return sorted(set(bound))


def _shared_trailing_object_findings(
    previous_clause: str,
    clause: str,
    *,
    location: str,
) -> list[SafetyFinding]:
    """Check an omitted object immediately before a contrasting safe action.

    In a bounded relation such as ``Build but do not deploy a keylogger``, the
    trailing object belongs to both coordinated actions even though contrast
    splitting separates them. Carry it backward only when the prior clause ends
    at a compatible action and does not introduce its own direct object. This
    avoids rebinding ``Use a sandbox, but do not deploy a keylogger``.
    """

    remainder = _CONTRAST_PREFIX.sub("", clause, count=1)
    if remainder == clause or _object_matches(previous_clause):
        return []

    findings: list[SafetyFinding] = []
    for protected in _object_matches(remainder):
        current_actions = _action_matches(remainder, protected.action_kinds)
        if not current_actions or not any(
            action[1] <= protected.start
            and _action_directly_precedes_object(remainder, action, protected)
            for action in current_actions
        ):
            continue
        current_bound = _actions_bound_to_object(
            remainder,
            protected,
            current_actions,
        )
        if not current_bound or not all(
            _locally_prohibited(remainder, protected, action)
            for action in current_bound
        ):
            # The ordinary clause scan reports an affirmative current action.
            continue

        previous_actions = [
            action
            for action in _action_matches(previous_clause, protected.action_kinds)
            if not previous_clause[action[1] :].strip()
            and not _action_introduces_distinct_english_object(previous_clause, action)
        ]
        if not previous_actions or all(
            _action_is_prohibited(
                previous_clause,
                action,
                scope_start=action[0],
            )
            for action in previous_actions
        ):
            continue
        findings.append(
            _finding(
                protected.category,
                location,
                f"{previous_clause} {clause}",
                "an affirmative action shares a trailing protected object with a contrasting locally prohibited action",
            )
        )
    return _ordered_unique(findings)


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
    remembered: tuple[_Match, ...] = ()
    clauses = _clauses(normalized)
    for clause_index, clause in enumerate(clauses):
        if clause_index:
            findings.extend(
                _shared_trailing_object_findings(
                    clauses[clause_index - 1],
                    clause,
                    location=location,
                )
            )
        retained_continuations: list[_Match] = []
        for remembered_object in remembered:
            continuation = _continuation_actions(clause, remembered_object)
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
                            remembered_object.category,
                            location,
                            clause,
                            "a contradictory continuation reuses the protected object after a locally negated or prohibitive clause",
                        )
                    )
                else:
                    # Keep the protected object for one more adjacent continuation
                    # when every action in this clause is prohibited. Still scan
                    # explicit objects in this clause before carrying it forward.
                    retained_continuations.append(remembered_object)

        clause_objects = _object_matches(clause)
        next_remembered: list[_Match] = []
        for protected in clause_objects:
            actions = _action_matches(clause, protected.action_kinds)
            if not actions:
                continue
            bound_actions = _actions_bound_to_object(clause, protected, actions)
            if all(
                _locally_prohibited(clause, protected, action)
                for action in bound_actions
            ):
                next_remembered.append(protected)
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
        remembered = tuple(
            sorted(
                set(next_remembered + retained_continuations),
                key=lambda item: (
                    item.start,
                    item.end,
                    item.category,
                    item.text,
                    tuple(sorted(item.action_kinds)),
                ),
            )
        )
    return _ordered_unique(findings)


_ALLOWED_HOST_SUFFIXES = (".example", ".test", ".invalid")
_POLICY_DISALLOWED_RESERVED_SUFFIXES = (".localhost",)
_DOCUMENTATION_NETWORKS = (
    ipaddress.ip_network("192.0.2.0/24"),
    ipaddress.ip_network("198.51.100.0/24"),
    ipaddress.ip_network("203.0.113.0/24"),
    ipaddress.ip_network("2001:db8::/32"),
)
_URL_PATTERN = re.compile(
    r"(?:(?:(?:[a-z][a-z0-9+.-]*:)?//)[^\s`\"'<>)]+|"
    r"(?<![a-z0-9+.-])mailto:[^\s`\"'<>)]+)",
    re.IGNORECASE,
)
_QUOTED_URL_ATTRIBUTE = re.compile(
    r"(?:href|src|action|formaction|poster|cite)\s*=\s*"
    r"(?P<quote>['\"])(?P<value>.*?)(?P=quote)",
    re.IGNORECASE | re.DOTALL,
)
_ATTRIBUTE_URL_PATTERN = re.compile(
    r"(?:(?:(?:[a-z][a-z0-9+.-]*:)?//)[^\s<>]+|mailto:[^\s<>]+)",
    re.IGNORECASE,
)
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


def _record_url_policy(
    raw_url: str,
    *,
    location: str,
    findings: list[SafetyFinding],
    url_hosts: set[str],
    url_addresses: set[str],
) -> None:
    try:
        parsed = urlparse(raw_url)
    except ValueError:
        findings.append(_host_finding(location, raw_url, "malformed URL in synthetic content"))
        return

    hosts: list[str] = []
    malformed_mailto = False
    if parsed.scheme.casefold() == "mailto":
        # Check every direct recipient and the standard recipient-bearing query
        # fields, while leaving non-recipient fields such as subject/body opaque.
        recipients = parsed.path.split(",")
        for key, value in parse_qsl(parsed.query, keep_blank_values=True):
            if key.casefold() in {"to", "cc", "bcc"}:
                recipients.extend(value.split(","))
        for recipient in recipients:
            address = recipient.strip()
            if not address:
                continue
            if "@" not in address or not address.rsplit("@", 1)[1]:
                malformed_mailto = True
                continue
            hosts.append(address.rsplit("@", 1)[1].casefold())
    else:
        host = (parsed.hostname or "").casefold()
        if host:
            hosts.append(host)

    if malformed_mailto:
        findings.append(_host_finding(location, raw_url, "malformed URL in synthetic content"))
    if not hosts:
        findings.append(_host_finding(location, raw_url, "URL does not expose a parseable host"))
        return
    for host in sorted(set(hosts)):
        url_hosts.add(host)
        address = _parse_ip(host)
        if address is not None:
            url_addresses.add(str(address))
            if not _is_documentation_address(address):
                findings.append(
                    _host_finding(
                        location,
                        raw_url,
                        "non-documentation IP URL is disallowed",
                    )
                )
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
    decoded_source = html.unescape(unicodedata.normalize("NFKC", text))
    quoted_url_spans: list[tuple[int, int]] = []
    for attribute in _QUOTED_URL_ATTRIBUTE.finditer(decoded_source):
        value = attribute.group("value")
        value_start = attribute.start("value")
        for url_match in _ATTRIBUTE_URL_PATTERN.finditer(value):
            start = value_start + url_match.start()
            end = value_start + url_match.end()
            quoted_url_spans.append((start, end))
            _record_url_policy(
                url_match.group(0),
                location=location,
                findings=findings,
                url_hosts=url_hosts,
                url_addresses=url_addresses,
            )
    for match in _URL_PATTERN.finditer(decoded_source):
        if any(start <= match.start() < end for start, end in quoted_url_spans):
            continue
        _record_url_policy(
            match.group(0).rstrip(".,;、。"),
            location=location,
            findings=findings,
            url_hosts=url_hosts,
            url_addresses=url_addresses,
        )

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
        # A dotted version/identifier can contain non-ASCII prose before a
        # numeric terminal component (for example, ``Identifier...v2.2.0``).
        # DNS TLDs are not numeric-only, so retain fail-closed IDN handling only
        # when the final label has at least one letter.
        if not any(character.isalpha() for character in domain.rsplit(".", 1)[-1]):
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
    raw_normalized = decoded_source
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
