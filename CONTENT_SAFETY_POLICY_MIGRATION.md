# PR #57 Content Safety Adapter Migration Note

## Reference state

- Blocked consumer: PR #57 / Issue #28
- Read-only reference head audited for Issue #59: `9c4f570064372bf8278e0c53cb47709d298e39bb`
- Shared Policy target: `scripts/content_safety_policy.py`, version `1.2.0`

Issue #59ではPR #57のbranch、Chapter 3本文、`ART-14`、Case、NICE Source、index、site-page registryを変更しない。PR #57の`check_chapter03_contract.py`からは、chapter-independentなnormalization、protected category、正負regressionだけをIssue #59のgeneric corpusへ抽出した。

## Chapter 2 adapter status (Issue #65)

- `scripts/check_chapter02_contract.py`をshared Policy `1.2.0`へ厳密pinする。
- Chapter 2本文、`ART-13 Authorization Checklist`、合成CaseのH1 / document preambleから全Record sectionまでを、有限なreader-visible fieldとして選択する。Markdown paragraph / list item内のsoft wrapは表示上のspaceへ投影してから検査する。
- 選択したfieldは`scan_action_text()`と`scan_host_policy()`へ渡し、実Target、Credential / Token / Cookie / Session、PII、Malware / C2、DoS / 破壊操作、非承認Hostを共有Policyへ委譲する。
- `.localhost`はtechnically reservedだがRepository Policyでdisallowedとし、non-reservedとは診断しない。
- `.example` / `.test` / `.invalid`、IPv4 documentation range、`2001:db8::/32`を維持する。公開済み専門書への3件のDELEGATE URLはreader-visible surfaceへ含めつつ、既存のChapter 2 publication contractと同じ完全一致行だけをreviewed host contextとして固定し、行変更時は通常のPolicy scanへ戻す。
- Policyの構造を欠くfragmentとなる既存のQuestion、Unknown、Prohibited、Reject / return fieldは、有限のreviewed contextとして完全一致で保持する。変更時は自動的に通常のPolicy scanへ戻す。
- Chapter 2固有のAuthority / Scope / Source / Traceability契約は移行しない。Canonical本文、Template、Caseの意味内容もPolicy適合だけを目的には変更しない。

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
