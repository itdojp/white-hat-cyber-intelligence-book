# PR #57 Content Safety Adapter Migration Note

## Reference state

- Blocked consumer: PR #57 / Issue #28
- Read-only reference head audited for Issue #59: `9c4f570064372bf8278e0c53cb47709d298e39bb`
- Shared Policy target: `scripts/content_safety_policy.py`, version `1.2.0`

Issue #59ではPR #57のbranch、Chapter 3本文、`ART-14`、Case、NICE Source、index、site-page registryを変更しない。PR #57の`check_chapter03_contract.py`からは、chapter-independentなnormalization、protected category、正負regressionだけをIssue #59のgeneric corpusへ抽出した。

## Chapter 2 adapter status (Issues #65 / #101)

- `scripts/check_chapter02_contract.py`はLayer Aだけを所有し、shared Content Safety Policy `1.2.0`とPublication Projection `1.1.0`へ厳密pinする。
- canonical surfaceは第2章本文、`ART-13 Authorization Checklist`、合成Caseの3文書全体である。Layer Aはordered H1/H2 inventory、Authority / Scope / Safety / Disclosure、Source / Registry / baseline、ART-13 / Case traceability、OWN / BRIDGE / DELEGATE、exact reviewed provenance exemptionを検査する。
- Markdown / Kramdown / HTMLのblock、inline、heading、list、table、blockquote、code、link/image、footnote、abbreviation、definition、entity、render precedenceはChapter 2 checkerで解釈しない。唯一のLayer B ownerは`scripts/publication_projection.py` `1.1.0`であり、private backendからlocked Jekyll `4.4.1` / Kramdown `2.5.2` / GFM parser `1.1.0`のexact projectionを取得する。production site generatorと共有するimmutableなroute contextでbody link rewriteを先に確定し、公開時destinationをtyped fieldとして取得する。設計判断とnon-goalは`adr/0002-publication-projection-owner.md`を正とする。
- Layer Bは`reader_visible_text`、`reader_visible_attribute`、`destination`、`hidden_metadata`を決定的なdocument / line / ordinalで返す。generic corpusは`tests/fixtures/publication-projection/corpus.json`に置き、historical counterexample、全familyの正負/説明/unsupported/near-miss、独立reviewで得たresource/entity/association/URL/production-rewrite regressionを含む184 fixtureとLayer A selection fixture 11件を管理する。PR #100のhistorical Layer B review counterexample 62件とLayer A fixture 8件、およびfresh exact-head Layer B thread 1件を合わせて全71 threadへ一意に対応付ける。
- LiquidはJekyllがMarkdownより前に解釈するため実行せず、raw HTML/comment、IAL / Kramdown extension、renderer warning等のcontract外sourceとともにshared `PP1001`でfail closedとする。executable/data destination等は`PP1002`でfail closedとする。完全なCommonMark / Kramdown / Liquid / HTML / browser / WHATWG URL理解は主張しない。
- canonical `.example` fieldに対する日本語助詞host-token false positiveはLayer CのIssue #67であり、本PRではPolicy grammarを変更しない。現在の3 fieldだけをdocument-scoped exact projected identity、heading path、exactly-once cardinalityで固定し、変更・移動・重複時は通常scanへ戻す。公開済み専門書への3件のDELEGATE destinationはexact reader-visible ownerとのrelationを含むprovenance exemptionとし、URLを別contextへ移動した場合も通常scanへ戻す。
- canonicalのQuestion、Unknown、Prohibited、Reject / return fieldに残る既知の非operative contextはexact projected fieldとheading pathでのみ固定する。absolute lineはdiagnostic evidenceとし、Layer A identityはtype / element / attribute / exact text / cardinality、field order、bounded sectionで構成する。Gate本文とSource ID body/reference occurrenceもreader-visible projection上で固定する。direct unsafe mutation、safe prohibition、preamble/body/tail、unexpected H1/H2 drift、fenced-code heading near-miss、semantic heading relocation、action/host/provenanceの移動・重複、hidden metadata/code literal bypassをChapter 2側の有限regressionで検査する。
- canonical本文、Template、Case、Policy grammar/versionはarchitecture収束のために変更しない。Chapter 4/25のlegacy parser全面移行は本PRの範囲外とし、generic corpusと代表章contractで非回帰を確認する。

## Reference extraction inventory

| Reference concern | Shared core / corpusでの扱い |
|---|---|
| NFKC、HTML entity、Markdown表示text | `normalize_visible_text`とnormalization corpusへ移行 |
| protected objectとAction | typed rule modelとcategory tableへ移行 |
| direct synthetic qualifier | Secret/Credentialだけをqualifiableとする正負fixtureへ移行 |
| PII、Target、危険Operation | syntheticであっても許容しないfixtureへ移行 |
| negated pre-action | standalone prohibitionをsafe counterpartとして固定 |
| contradictory continuation | object memoryとpronoun/ellipsisを六つのblocker phraseで固定 |
| Host/address | `.example` / `.test` / `.invalid`、documentation IP、`.localhost`診断へ移行 |
| dotted identifier / relative link | domainと誤分類しないpositive fixtureへ移行 |
| Chapter 3固有のArtifact/Source/Registry | 共通coreへ移さずfuture adapterに残す |

## Future adapter steps after Policy core is on `main`

1. PR #57を最新`main`へ通常の方法で取り込む。
2. Chapter 3 checkerは、Artifact/table/sectionからbounded reader-visible fieldを選択し、`scan_fields`へ`(stable location, text)`を渡す。
3. Chapter 3固有のART-14 referential integrity、NICE Source、Source Registry、Case、site-page、Publication契約はchapter checkerに残す。
4. 既存のchapter-independent regex/corpusを削除し、generic fixtureと同じSemanticを二重実装しない。
5. PR #57の現在の六つのblocker phraseを、共通Policy `1.2.0`がunsafeと判定することをadapter regressionで固定する。
6. `.localhost`は「reservedだがRepository Policyでdisallowed」と診断し、`non-reserved`と誤記しない。
7. full local QA、exact-head Book Contract / Book QA、fresh review、unresolved thread 0を再取得する。

Adapterは書籍全体の自由文を無選別にscanしない。Chapter 3が所有するAction-bearing fieldとreader-visible safe-boundary fieldを明示し、locationをArtifact ID、section、row ID等へ固定する。

## 1.2.0 finite grammar re-audit

Policy `1.2.0`はstable APIと11 categoryを維持したminor updateである。`1.1.0`のmixed-script境界、日本語空白、bounded action chain、bare ellipsis、standalone prohibition、versioned identifierを維持し、Issue #61で凍結した次の三つの有限構造を追加する。

- Japanese modifier + particle + destructive action
- Synthetic qualifierより優先するtheft / reuse / replay / hijack / takeover / exfiltration Operation
- 埋め込みOperationだけを抑制するEnglish PII risk / policy / control analysis

Chapter 3 adapterはPolicy `1.2.0`へ厳密pinする。旧Chapter 3のread-only safety corpusをPolicy inputやChapter固有denylistにはせず、249 unsafe / 49 explicitly negated fieldとoriginal blocker 6 / safe counterpart 6をChapter contractで照合する。`finite-grammar-1.2-corpus.json`はA/B/Cごとにunsafe、safe、near-miss、continuationのexact inventoryを持つ。代表Chapter 2 / 11 / 17 / 25はmain `a1dfadae153bfe36b88f72e503f5a5be9c64bddf`をbaselineとして再監査する。Chapter名、`ART-14`、固有行番号、無制限の同義語をshared ruleへ持ち込まない。

新adapterはbounded Chapter 3 fieldに対して、`合成Scenario。外部接続と実Target操作なし`、`keyloggerを作るべきではない`、`rootkitを実装するべきではない`をPolicy由来で0 findingとする。Case全体をhost scanする場合も、`確認済みIdentifierの記入形式例はv2.2.0`をhost/IDNと誤認しない。ambiguous labelled IPv6とbare `artifact.json`は既存のfail-closed contractどおり許容へ緩和しない。

## Issue #62 Publication coordination correction

Issue #62はPolicy versionを`1.2.0`のまま維持し、防御文書Publication exceptionに既存のdirect modifierを挟むと先行Actionを見落とす実装欠陥を修正する。Coordinator、modifier、local negationは一つの有限source-of-truthから生成し、Chapter 3 adapterに独自gap grammarを追加しない。Publication Actionとdocument headだけを抑制し、同じProtected Objectへ束縛された先行Actionおよび後続continuationは共通Policyで独立評価する。別Object、新subject、句読点を越えた再束縛は行わず、`do not deploy and immediately publish a phishing report`の既存結果は変更しない。

## Issue #67 IPv4 Japanese prose boundary correction

Issue #67は、main `a129c14bd15a1ee2101cd531aba7d226e02dd011`で再現したdocumentation IPv4直後の日本語助詞によるfalse positiveを修正する。IPv4の前に連続する日本語script、`へ / を / で`、およびその後ろのtoken終端または日本語scriptだけを有限なprose境界としてIDN scannerからIP scannerへ委譲する。documentation rangeの許可、non-documentation IPv4のreject、既存のURL / bare domain / IDN / punycode / `.localhost`判定は変更しない。

この修正は既存のhost token ownershipを訂正するpatchであり、category、Stable API、Policy meaningを追加・変更しないため、Policy versionは`1.2.0`を維持する。shared host corpusは三つの受け入れ例、token終端、non-documentation IPv4、未知助詞、ASCII tail、IDN suffix、無効IPv4を固定する。Policy利用章はChapter 2 / 11 / 17 / 25とChapter 4 canonicalを再監査し、canonical prose、Publication Projection、formatter pin、generated/built siteに変更を加えない。
