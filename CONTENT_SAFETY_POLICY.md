# Public Content Safety Policy

## Status

- Policy version: `1.0.0`
- Scope: chapter adaptersが選択した、読者に見えるbounded field
- Implementation: `scripts/content_safety_policy.py`
- Contract harness: `scripts/check_content_safety_policy.py`
- Generic regression corpus: `tests/fixtures/content-safety/`

本Policyは、公開教材へ危険な実行指示、実在Target、Secret、個人情報、許可外Hostを混入させないための共通contractである。自然言語を完全に理解する分類器ではなく、全章・全文章を自動的に網羅するとも主張しない。各章のadapterは、入力fieldの選択、Artifact/表/JSONの構造検査、章固有の安全要件を引き続き所有する。

## Stable API

`scripts/content_safety_policy.py`は、次の小さなAPIを公開する。

```python
@dataclass(frozen=True)
class SafetyFinding:
    category: str
    location: str
    normalized_excerpt: str
    reason: str
    policy_version: str

normalize_visible_text(text: str) -> str
scan_action_text(text: str, *, location: str) -> list[SafetyFinding]
scan_host_policy(text: str, *, location: str) -> list[SafetyFinding]
scan_fields(fields: Iterable[tuple[str, str]]) -> list[SafetyFinding]
```

Findingは`location / category / normalized_excerpt / reason / policy_version`の順序契約で決定的にsortし、同一Findingをdeduplicateする。型またはfield形状が不正な入力は`policy.malformed_input`としてfail closedにする。

## Structured policy model

共通coreは、無制限の同義語listではなく、次を分離する。

1. protected object/category
2. action expression
3. direct synthetic qualifier
4. local negationまたはprohibition
5. contrast/continuationと、合理的に束縛できるpronoun/ellipsis
6. host/address publication policy
7. diagnostic category

ObjectがActionより前でも後でも検査する。最初の節が禁止・否定でも、`but`、`however`、`しかし`等に続く矛盾Actionを安全扱いしない。`synthetic`、`合成`等は直後のSecret/Credential fixtureだけへ束縛し、`not synthetic`、`non-synthetic`、`非合成`を肯定Qualifierとして扱わない。PIIと危険Operationはsynthetic qualifierの対象外である。

## Normalization contract

`normalize_visible_text`は次の順で決定的に処理する。

1. Unicode NFKC
2. HTML entity decode
3. Markdown link/imageの読者表示label抽出
4. HTML tagとMarkdown emphasis/code delimiterの除去
5. backslash unescape
6. hyphen、underscore、middle-dot variantをASCII hyphenへ統一
7. horizontal whitespaceを単一spaceへ統一し、newlineを保持
8. Unicode case-fold

URL destinationはAction scanの読者表示textから除外する一方、`scan_host_policy`で別途検査する。ASCII word boundaryだけへ依存せず、DoS / DDoSの直後に日本語particleが続く場合も扱う。

## Protected categories

1. `target.real_or_external`
2. `network.host_or_address`
3. `secret.credential`
4. `data.pii`
5. `operation.authentication_or_session`
6. `operation.malware`
7. `operation.c2_or_phishing`
8. `operation.privilege_or_evasion`
9. `operation.disruption_or_destruction`
10. `operation.social_engineering_or_tracking`
11. `analysis.weak_evidence_attribution`

説明または明示的な禁止だけの文は許容する。危険Operationを`synthetic`と呼んでも許容しない。実Target操作量、Malware作成量、認証試行数を学習Evidenceへ変換しない。

## Host and address policy

Repositoryのsynthetic publication policyとして次を許容する。

- DNS suffix: `.example`、`.test`、`.invalid`
- IPv4 documentation range: `192.0.2.0/24`、`198.51.100.0/24`、`203.0.113.0/24`
- IPv6 documentation range: `2001:db8::/32`

`.localhost`は技術的にはreservedだが、このRepositoryの公開Policyでは許容しない。診断は`non-reserved`とは記載せず、技術的reserved statusとRepository permissionを分離する。曖昧なbare host/addressはfail closedにでき、明示的な`.example` / `.test` / `.invalid`、URL形式、IPv6 bracket形式への書換えを案内する。

Chapter 2の既存chapter-specific checkerには`.localhost`を許容する旧suffix listが残るが、現行canonical contentに`.localhost`はない。共通coreをchapter adapterへ導入する際は、Policy `1.0.0`を正本としてこの差を解消し、canonical本文を警告回避だけの目的では変更しない。

## Versioning and re-audit

- patch: 診断文またはfixture訂正。保護Semanticは拡張しない。
- minor: category、normalization、Action/negation/continuation Semanticの追加。
- major: APIまたは既存Policy meaningの破壊的変更。

Policy version変更時は、Policyを利用する全chapter adapterについて、正負fixture、代表canonical field、generated/built driftを再監査する。minor/major変更では、影響する章のexact head、Policy version、再監査結果をPRへ記録する。

## Non-goals

- 自然言語安全性の完全な判定
- 書籍全体の無選別全文scanによる安全保証
- 法的助言または個別Targetの許可判断
- Chapter固有Artifact schema、Source、Publication契約の置換
- 危険Operationの実装、Payload、実Target検証
