# Public Content Safety Policy

## Status

- Policy version: `1.2.0`
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

ObjectがActionより前でも後でも検査する。同じbounded clauseでは、Objectの片側にある最短Actionだけへ縮約せず、直接のAction/Object gap、relative predicate、既存のsame-object continuationで束縛できる各Actionを個別に評価する。Action-to-Object gapはEnglish最大7 token / 96文字、Japanese最大32文字の有限modifier grammarとし、gap内に別Action、sentence boundary、またはmodifierとして許可しないcase particleがあれば束縛しない。`but`は原則contrast boundaryだが、後方にProtected Object、前方に関連Actionがあり、その間に別Actionがなく有限modifier grammarを満たす場合だけnoun modifierとして保持する。対照接続の直前節が対応Actionで終わり、直後の局所的に禁止されたActionだけがProtected Objectを明示する場合は、その末尾Objectを直前Actionへも有限に束縛する。ただし直前Actionが`sandbox`等の別Objectを直接導入する場合は再束縛しない。Action後のbounded冠詞句が時間headではなく別Objectを直接導入する場合も、Object-first associationから除外する。冠詞句の末尾が`this week`、`the very next day`等の有限な時間修飾句である場合は、その時間句を除いた後に別Objectが残るかを判定する。これは日本語の完全なdependency parsingを意味せず、別Objectを持つ後続Actionは再束縛しない。最初の節が禁止・否定でも、`but`、`however`、`しかし`等に続く矛盾Actionを安全扱いしない。一つの節で局所的に禁止されたProtected Objectは一件へ縮約せず、合理的に束縛できる各Objectを次の隣接continuation判定へ保持する。複数候補へ束縛可能なgeneric pronounは安全側にfail closedとし、Action kindが適合する各Objectを評価する。`forbidden to`および`prohibited from` / `forbidden from`は同じ句の最初のActionと、句読点や対照接続を挟まない直接の`and / or / nor`協調Actionだけを支配し、comma、sentence boundary、contrast marker、またはcoordinator後の新しいsubject / modalでscopeを終了する。`do not A or/nor B`の局所否定は直接協調Actionへ引き継ぐ一方、`do not A and B`は曖昧なため後続Actionをfail closedに扱う。Actionの後ろにある禁止表現は、その途中と禁止表現後の同一bounded scopeに別Actionがなければ当該Actionへ束縛する。禁止表現後に直接協調された各Actionが自身の禁止表現を持つ場合は、独立した明示的禁止として許容する。`synthetic`、`合成`等は直後のSecret/Credential fixtureだけへ束縛し、`not synthetic`、`non-synthetic`、`非合成`を肯定Qualifierとして扱わない。PIIと危険Operationはsynthetic qualifierの対象外である。`1.1.0`で追加したmixed-script、有限modifier、否定、continuation、versioned identifierの契約は`1.2.0`でも維持する。

### Policy 1.2.0 finite grammar

`1.2.0 finite grammar`は、既存の11 categoryとStable APIを維持したまま、次の三つの有限構造を追加する。

1. `JapaneseParticleFrame`: boundedな名詞句と`の`を任意に持つ`ログ / 監査証跡 / データ + を + 破壊的Action`を検査する。名詞修飾は凍結した`システム / 対象 / 本番 / 顧客 / 無許可`に限定し、`の`を伴う形と直接複合する形を区別せず検査する。`カタログ`、`ブログ`、`メタデータ`のsuffixはProtected Objectにしない。
2. `OperationRule`: theft、exfiltration、reuse、replay、hijack、takeoverと、有限日本語形`窃取 / 持ち出す / 流出させる / 再利用 / リプレイ / 乗っ取る`を、Synthetic qualifierで許容できないOperationとして分類する。Specific Operationのprecedenceはgeneric Secret qualifierより高い。英語Operationへ日本語の`する / しない`等が直接続くmixed-script形式も同じ有限Operationとして扱う。能動否定に加え、`窃取されない`や`再利用されない`の有限受動否定は局所的禁止として扱う。Object-firstの受動表現では、`and are reused`のように主語を省略した有限copula continuationも直前のProtected Objectへ束縛し、先行Actionの局所否定を後続Actionへ伝播させない。
3. `MetaAnalysisFrame`: `meta verb + risk / policy / control等 + relation + PII operation + PII object`の有限英語frameでは、埋め込まれたOperationだけを分析対象として抑制する。直接PII操作、協調Action、矛盾continuation、後続pronoun Actionは抑制しない。特に、frame直前の`collect and analyze ...`のような直接協調Actionは同じPII Objectへ束縛し、meta-analysis suppressionの対象に含めない。

Object classification、Operation classification、qualifier precedence、meta-analysis suppressionは独立した型とfixtureで検証する。English meta-analysis後の`it / the same`は単独または有限Protected Object headのときだけ継続参照とし、`the same report`のように別の明示Objectが続く場合はPIIへ再束縛しない。章名、Artifact ID、固有行番号、無制限の同義語はruleへ持ち込まない。

## Normalization contract

`normalize_visible_text`は次の順で決定的に処理する。

1. Unicode NFKC
2. HTML entity decode
3. Unicode category `Cf`のzero-width format characterを除去
4. HTML commentを空文字へ変換し、commentで分断された読者表示tokenを再結合
5. Markdown link/imageの読者表示label抽出
6. HTML tagとMarkdown emphasis/code delimiterの除去
7. backslash unescape
8. hyphen、underscore、middle-dot variantをASCII hyphenへ統一
9. horizontal whitespaceを単一spaceへ統一し、newlineを保持
10. Unicode case-fold
11. protected vocabularyの回避に使われやすいGreek / Cyrillic Latin-lookalikeのbounded fold

URL destinationはAction scanの読者表示textから除外する一方、`scan_host_policy`で別途検査する。HTML attribute内のURL tokenはdecode後もsingle/double quote、whitespace、angle bracket等のdelimiter手前で終了し、path/query/fragmentとquoted value内の末尾punctuationはdelimiterまで保持する。Hierarchical URLに加えて、quoted/unquoted HTML attributeおよびMarkdown autolinkの`mailto:`について、direct recipientと`to` / `cc` / `bcc` query fieldにある全address domainを有限に検査し、任意のopaque URI schemeや`subject` / `body`をhost-bearing URLとはみなさない。Prose URLの外側にある末尾punctuationだけをtrimする。ASCII word boundaryだけへ依存せず、DoS / DDoSの直後に日本語particleが続く場合と、英語Actionへ日本語suffixが続くmixed-script形式、`作って` / `作ってください`のbounded creation requestを扱う。Confusable foldはUnicode全体の同形異字判定を主張せず、Policy corpusに固定したbounded mappingだけを適用する。

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

説明または明示的な禁止だけの文は許容する。`publish / announce + phishing / malware + report / analysis / guidance`および`フィッシング / マルウェア + 報告 / 分析 / ガイダンス / 指針 + 公開 / 公表`は、節全体がこの有限な防御文書Publication frameで完結する場合だけ説明文として許容する。`infrastructure / server / site / page / channel / operation / campaign`または対応する日本語の実運用対象語、bare Operation、PII、弱いEvidenceによる断定的帰属、同じ節の追加Operation、`deployable malware`はこの例外に含めない。危険Operationを`synthetic`と呼んでも許容しない。実Target操作量、Malware作成量、認証試行数を学習Evidenceへ変換しない。

## Host and address policy

Repositoryのsynthetic publication policyとして次を許容する。

- DNS suffix: `.example`、`.test`、`.invalid`
- IPv4 documentation range: `192.0.2.0/24`、`198.51.100.0/24`、`203.0.113.0/24`
- IPv6 documentation range: `2001:db8::/32`

`.localhost`は技術的にはreservedだが、このRepositoryの公開Policyでは許容しない。診断は`non-reserved`とは記載せず、技術的reserved statusとRepository permissionを分離する。bare IDN / punycode hostも検査し、明示的な`.example` / `.test` / `.invalid` suffixだけを許容する。ただしnumeric-only terminal labelを持つdotted version/identifierはDNS TLDではないためhost候補から除外する（例: Unicode proseに続く`v2.2.0`）。曖昧なbare host/addressはfail closedにでき、許容suffix、URL形式、IPv6 bracket形式への書換えを案内する。

Chapter 2の既存chapter-specific checkerには`.localhost`を許容する旧suffix listが残るが、現行canonical contentに`.localhost`はない。共通coreをchapter adapterへ導入する際は、Policy `1.2.0`を正本としてこの差を解消し、canonical本文を警告回避だけの目的では変更しない。

## Versioning and re-audit

- patch: 診断文またはfixture訂正。保護Semanticは拡張しない。
- minor: category、normalization、Action/negation/continuation Semanticの追加。
- major: APIまたは既存Policy meaningの破壊的変更。

`1.2.0 finite grammar`はminorである。Stable APIと11 categoryを維持する一方、1.1.0が検出しなかった三つのbounded semantic classを追加し、Operation qualifier precedenceと有限Meta-analysis suppressionをPolicy meaningとして明示するためである。Policy version変更時は、Policyを利用する全chapter adapterについて、正負fixture、代表canonical field、generated/built driftを再監査する。minor/major変更では、影響する章のexact head、Policy version、再監査結果をPRへ記録する。

## Finite review acceptance contract

### Blocking

- P0またはP1
- `1.2.0`で宣言したJapanese particle frame、non-qualifiable theft/reuse Operation、English PII meta-analysis frameのinvariantを破る最小反例
- 既存Policy category、Host、negation、continuation、deterministic ordering/deduplication、canonical/generated/build契約のregression

### Non-blocking backlog

- 凍結した有限Vocabulary外の新しい単語または同義語だけを追加する提案
- 完全な自然言語理解または書籍全体の無選別全文scanを要求する提案
- 本文書で明示したNon-goalに属し、既存categoryまたは`1.2.0` invariantの破壊を示さない表現

Non-blocking指摘は、該当するbounded non-goalをReviewへ返信し、将来Coverageの集約Issueへ記録できる。同じPRで無制限の語彙追加を再開しない。

## Non-goals

- 自然言語安全性の完全な判定
- 書籍全体の無選別全文scanによる安全保証
- 法的助言または個別Targetの許可判断
- Chapter固有Artifact schema、Source、Publication契約の置換
- 危険Operationの実装、Payload、実Target検証
