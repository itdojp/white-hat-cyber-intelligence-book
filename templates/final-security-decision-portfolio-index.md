# Final Security Decision Portfolio Index

## 目的と使用境界

`ART-33`は`ART-10`を中心に成果物の参照、判断、Gap、担当、再評価をまとめる索引である。本文は[第29章](../manuscript/29-capstone-case-study.md)、[全欄合成Case](../cases/ch29-capstone-portfolio-example.md)を併用する。

記入対象は合成資料と自分の読解メモだけ。実対象、実Credential、個人情報、外部Network、実Model APIは使わない。版不一致、由来不明、Scope不明、外部接続要求、未配達の受領化で停止する。自分のメモだけを整理し、元資料は保持する。

## 0. Portfolio identity

| Field | Value |
|---|---|
| Artifact ID | ART-33 |
| Portfolio ID / Version | 記入 |
| Final Case ID | 記入 |
| Owner / Decision owner | 作成担当と判断担当を別に記入 |
| As-of / Source cutoff | 親の観測時点と今回の読解時点を区別 |
| Deadline / Portfolio expiry | 時刻・タイムゾーンを記入 |
| Classification | 公開可能な合成資料だけ |
| Portfolio Status | Assembling / Reviewable / Needs evidence / Decision ready / Approved / Superseded |

Statusは親Artifactの状態ではない。独立した承認記録がなければApprovedにしない。記入完了やApprovedから実操作許可を導かない。

## 1. Decision Requirement

| Field | Value |
|---|---|
| Decision Requirement ID / Parent requirement | 同じIDを上書きせず新旧関係を記入 |
| Question / Owner / deadline | 誰が何をいつまでに判断するか |
| Criteria / maximum uncertainty | 選べるOptionに必要な根拠と、許容できない不足 |
| Not required | 今回判断しない問い |

## 2. ART-01〜32の参照

次の欄をArtifact種別ごとに32行記入する。同BundleのART-04/23、ART-07/26を一行へ消さない。Artifactの全欄を本索引へ複製せず、正しい版の元記録へ戻る。

| Field | Value |
|---|---|
| Artifact ID / Record ID | 種別と記録Instanceを区別 |
| Canonical path / version / hash | 固定入力を識別。hashは真正性の保証ではない |
| Source Case / subject / as-of | 元資料の対象・版・時点を保持 |
| Relation to final Case | refines / supports / contradicts / supersedes / independent、関係の対象を明示 |
| Use / native Status scope | historical-context / method-reference / independent-comparison。状態が記録全体か個別項目かを記入 |
| Native owner / Evidence / Decision / Reassessment reference | 元記録の欄へ戻る参照。不明なら推測せず明記 |
| Integration owner / step | 今回の読解担当。元Ownerの交代ではない |
| Non-inheritance / next review | Evidence、Authority、未配達、親状態を変更しない境界 |

## 3. Evidence inventoryとGap

| Field | Value |
|---|---|
| Evidence ID / kind | 文書読解の記録とシステム観測を分ける |
| Source / location / version / cutoff | 出典、根拠箇所、hash、利用可能時点 |
| Claim supported / limitation | 何を支持し、何を支持しないか |
| Gap ID / kind / question | Not collected、Inconclusive、Residual riskを混ぜない |
| Owner / due / next check | 不足を解く確認条件と元章への戻り先 |

同原典の再掲は独立裏付けに数えない。別Caseや未受領ProductをEvidence inventoryへ転用しない。

## 4. Judgmentと二つのBrief

| Field | Value |
|---|---|
| Judgment ID / Evidence IDs / Gap IDs | 根拠と不足を直接参照 |
| Confirmed facts / assessment | 確認事実と分析判断を分ける |
| Assumption / alternative / prediction | 未確認条件、別説明、判断が変わる条件 |
| Confidence / scope / basis | 実システム全体の確信度へ拡張しない |
| Recommendation | 目的に対する行動案。実操作命令ではない |
| Technical brief / Executive brief | 同じ判断・根拠・Gapを別の読者へ説明 |
| Delivery / receipt | 未配達・未受領を記入、受領証拠を捏造しない |

## 5. Option、Review、Decision

| Field | Value |
|---|---|
| Option / required evidence | 不足がどの選択肢を妨げるか |
| Benefit / cost / residual / reversibility | 保留や拒否を含め比較 |
| Review pass / reviewer role / result / date | 八観点を区別。架空例と実レビューを混ぜない |
| Decision ID / version / owner | 同じCase・版・判断への参照 |
| Recommendation / approval | 推奨と承認を別欄にする |
| Approval scope / limitations | 不在はnull相当で残す。過去許可を延長しない |
| Supersedes / successor | 置換しても旧版の不足を削除しない |

## 6. ActionとReassessment

| Field | Value |
|---|---|
| Action ID / Decision ID / Gap ID | 対応する不足と判断 |
| Owner / due / verification | 次に何をどう確認するか |
| Result / executed | 計画と実施・実検証を区別 |
| Reassessment ID / trigger / expiry | 版、対象、Source訂正、新Evidence・許可、受領、レビュー、期限の変更 |
| Closure / return route | 終了条件と元Artifactの欄への戻り先 |

## 7. 最終自己点検

- [ ] 何を判断し、どの条件が不足するかを本文だけから説明できる。
- [ ] 32種の参照、版、独立Case、同Bundle二役割を保持した。
- [ ] 親のOwner、Evidence、Decision、Control、期限、未配達を変更していない。
- [ ] 記入完了とControl有効性、提案と承認、承認と実許可を分けた。
- [ ] 八観点のRubric、不足の担当・期限・次確認を記録した。
- [ ] [第29章](../manuscript/29-capstone-case-study.md)と[ART-10](integrated-security-case-map.md)へ戻れる。
