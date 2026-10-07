# Security Improvement Backlog

`ART-28`は、測定値を改善担当・検証・残存Riskの判断へ接続する記録である。[第22章](../manuscript/22-measurement-improvement.md)と[完全合成記入例](../cases/ch22-improvement-backlog-example.md)を併せて読む。記入済みであることは、実操作の許可、根拠の真正性、実組織のRisk reductionの認定ではない。

## Record and decision purpose

| Field | 記入内容 |
|---|---|
| Backlog / Item ID / revision | 記録全体と改善項目のID、版、旧記録への参照 |
| Case / relation | 親Caseとのrefines等の関係、方法参照と受領済みEvidenceを区別 |
| Risk Objective / Decision Requirement | 何の判断を支え、何を避けたいか |
| Finding / Gap / Control | 元の不足、Control目的、未確認範囲のID |
| Parent boundary | 親のUnknown、未配達、期限切れ、権限falseを保持する条件 |
| Source / scope | Source版と採用箇所。分類・mappingを有効性の証明にしない |

## Metric specification

| Field | 記入内容 |
|---|---|
| Metric ID / type / decision purpose | Outcome / Leading / Process / Qualityの役割と利用する判断 |
| Definition / formula / unit | 数える対象、計算式、単位。件数と率、時間の統計量を区別 |
| Population / revision / exclusions | 母集団のMember ID、選定理由、対象版、除外とその理由 |
| Numerator / denominator | 率の分子と分母、重複と包含関係。0・不明分母は率を出さない |
| Window / cutoff / available at | 観測の範囲、情報利用の締切、根拠が利用可能になった時刻 |
| Data source / provenance | 根拠ID、供給記録か実測か、同一原典の重複を避ける識別 |
| Aggregation / sample size | Mean / Median / Percentile等の方式と件数。未完了・欠測の扱い |
| Baseline / target / actual | 同じ条件の旧値、目標、現在値。未定義や未測定はnullと理由 |
| Quality / bias / missingness | 完全性、選択Bias、欠測、比較できない条件 |
| Confidence / limitation | 支持する範囲、代替説明、情報Gap、無効化条件 |

値を精密に表示しても、元のEvidenceが完全になるわけではない。Metricの目的・定義を変えた場合は旧値を保持し、同じ系列の改善と呼べるかを再判断する。

## Priority and action

| Field | 記入内容 |
|---|---|
| Debt / finding | Telemetry、Detection、Evidenceのどこが判断を妨げるか |
| Priority / rationale | 業務への関係、根拠の強さ、緊急性、依存。単一Scoreへ潰さない |
| Dependency / acceptance | 先行するItem ID、必要な根拠、循環や未充足の扱い |
| Cost / trade-off | 費用・負荷・副作用の仮定。実見積りと教材の値を区別 |
| Action ID / proposal | 何を改善する計画か。提案と実施記録を分ける |
| Owner / due date | 役割としての担当、期限、判断不能時の照会先 |
| Expected evidence / criterion | どの対象・版・Metricで何が得られれば受け入れられるか |

## Verification and risk decision

| Field | 記入内容 |
|---|---|
| Validation ID / method | 同じ対象・範囲でどの条件を照合したか |
| Evidence ID / binding | Item・Metric・対象版・Window・Cutoffに結び付く根拠 |
| Actual / result | 期待との一致・不一致・部分充足・不足を区別 |
| Before / after / retained evidence | 変更したものと固定したもの、旧失敗・正常・反証例を保持 |
| Risk reduction judgment | 支持する限定結論、代替説明、確信度、実影響の未確認事項 |
| Residual risk / owner | 残るGap、評価責任者。VerifiedをRiskゼロと呼ばない |
| Decision ID / basis | 改善、保留、限定受容、廃止等の理由と参照先 |
| Acceptance / expiry | 受容の対象・条件・Risk owner・判断時刻・期限。実操作許可とは別 |

## Seven statuses

| Status | 記録上の意味 |
|---|---|
| Proposed | 目的とGapに対応する改善案がある |
| Approved | 条件と担当を伴う供給計画の承認がある |
| In progress | 供給記録の作業は進行中だが検証完了ではない |
| Blocked | 必要条件が不足し、解除に必要な根拠を待つ |
| Verified | 結び付いたValidationとEvidenceで受入条件を照合した |
| Accepted | 残存Riskについて期限・条件付きの供給判断を残す |
| Retired | 役割を終えた理由、代替先、旧履歴を保持する |

ImplementedやVerification pendingを正式Statusへ追加しない。必要な進捗はActionとVerificationの欄で説明する。Approvedは実権限を付与せず、AcceptedとRetiredを修正成功へ算入しない。

## Reassessment and metric retirement

| Field | 記入内容 |
|---|---|
| Reassessment ID / owner / due | 次に誰がいつ何を再判断するか |
| Trigger / invalidation | 母集団、Schema、Rule、Source、品質、権限、受容期限の変化 |
| Retire / revise / retain condition | 判断目的の喪失、重複、Gaming、Data不足、代替の有無 |
| Replacement / history | 代替Metric、旧定義・値・廃止理由の保持 |
| Executive handoff | 判断要求、選択肢、費用・限界。予定とReceiptを区別 |

## Authority, scope and safety

| Field | 記入内容 |
|---|---|
| Purpose / prerequisite | 判断目的と必要な方法知識。本教材は供給記録の読解だけ |
| Authority / scope | 許可、範囲、期限の出所。不明なら停止。本教材の実行権限はfalse |
| Expected evidence / impact | 解答と照合記録のみ。親正本や実設定を変更しない |
| Prohibited use | 実Dataを使わず、個人監視・公開Ranking・懲罰KPIに転用しない |
| Stop | 実Data混入、意味・品質・範囲・権限不明で停止し、追加実操作をしない |
| Cleanup / residual | 解答Copyの整理計画と残存確認。実Runtime未作成と復旧完了を混同しない |

Templateを埋めることと、すべてのGapを解消することは別である。未知のままの欄も、理由・Owner・次の判断を伴えば隠さず残せる。
