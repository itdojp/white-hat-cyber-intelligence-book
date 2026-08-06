# PR #57 Content Safety Adapter Migration Note

## Reference state

- Blocked consumer: PR #57 / Issue #28
- Read-only reference head audited for Issue #59: `9c4f570064372bf8278e0c53cb47709d298e39bb`
- Shared Policy target: `scripts/content_safety_policy.py`, version `1.0.0`

Issue #59ではPR #57のbranch、Chapter 3本文、`ART-14`、Case、NICE Source、index、site-page registryを変更しない。PR #57の`check_chapter03_contract.py`からは、chapter-independentなnormalization、protected category、正負regressionだけをIssue #59のgeneric corpusへ抽出した。

## Reference extraction inventory

| Reference concern | Shared core / corpusでの扱い |
|---|---|
| NFKC、HTML entity、Markdown表示text | `normalize_visible_text`とnormalization corpusへ移行 |
| protected objectとAction | typed rule modelとcategory tableへ移行 |
| direct synthetic qualifier | Secret/Credentialだけをqualifiableとする正負fixtureへ移行 |
| PII、Target、危険Operation | syntheticであっても許容しないfixtureへ移行 |
| negated pre-action | standalone prohibitionをsafe counterpartとして固定 |
| contradictory continuation | object memoryとpronoun/ellipsisをsix blocker phraseで固定 |
| Host/address | `.example` / `.test` / `.invalid`、documentation IP、`.localhost`診断へ移行 |
| dotted identifier / relative link | domainと誤分類しないpositive fixtureへ移行 |
| Chapter 3固有のArtifact/Source/Registry | 共通coreへ移さずfuture adapterに残す |

## Future adapter steps after Policy core is on `main`

1. PR #57を最新`main`へ通常の方法で取り込む。
2. Chapter 3 checkerは、Artifact/table/sectionからbounded reader-visible fieldを選択し、`scan_fields`へ`(stable location, text)`を渡す。
3. Chapter 3固有のART-14 referential integrity、NICE Source、Source Registry、Case、site-page、Publication契約はchapter checkerに残す。
4. 既存のchapter-independent regex/corpusを削除し、generic fixtureと同じSemanticを二重実装しない。
5. PR #57の現在の三つのblocker phraseを、共通Policy `1.0.0`がunsafeと判定することをadapter regressionで固定する。
6. `.localhost`は「reservedだがRepository Policyでdisallowed」と診断し、`non-reserved`と誤記しない。
7. full local QA、exact-head Book Contract / Book QA、fresh review、unresolved thread 0を再取得する。

Adapterは書籍全体の自由文を無選別にscanしない。Chapter 3が所有するAction-bearing fieldとreader-visible safe-boundary fieldを明示し、locationをArtifact ID、section、row ID等へ固定する。
