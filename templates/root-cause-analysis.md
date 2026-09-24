# Root Cause Analysis

`ART-26`は原因仮説と代替説明を、`ART-07`のTimeline・Evidence・限定した影響へ結ぶ。原因を一つに決めるための穴埋め表ではない。分からない点をGapとして残し、改善案・検証・再評価を区別する。[第20章](../manuscript/20-dfir-timeline-causality.md)と[完全合成記入例](../cases/ch20-dfir-timeline-causality-example.md)を参照する。

## Record and decision requirement

| Field | 記入内容 |
|---|---|
| RCA ID / version | 旧判断を上書きせず、Timeline IDとCutoffへ結ぶ |
| Incident / Case | 完全合成か実事案か、親参照と引き継がない権限 |
| Problem statement | 対象・版・Windowについて説明したいこと |
| Evidence Question | 原因、機構、影響、代替説明を分けた問い |
| Owner / analysis time | 判断主体と判断時点 |
| Known impact / scope | 供給Evidenceで述べられる範囲 |
| Unknown / excluded | 不明と明示根拠による除外を分離 |

## Causal analysis

| Field | 記入内容 |
|---|---|
| Root condition hypothesis | 根底の条件についての仮説。未確定なら未確定と書く |
| Trigger | きっかけとなるEvent。原因と同義にしない |
| Mechanism | どの条件がどの結果を可能にしたか、そのEvidenceと限界 |
| Contributing factor | 機構への寄与と、単なる分析上の障害を分ける |
| Evidence IDs / Claim IDs | Timelineの原Recordと主張へ直接参照 |
| Alternative causal model | 正当な変更、別の許可、Collector・Clock条件、他の説明 |
| Contradicting evidence | どの主張を反証し、何を反証していないか |
| Confidence | 対象となる結論、根拠、Gapと反証条件 |
| Evidence gap | 欠けるData、判断への影響、Owner、期限 |

相関、前後関係、保守予定の存在、一つの代替説明の反証だけでRoot Causeを確定しない。IDから実在人物を同定せず、記録のない範囲を「影響なし」にしない。

## Control and reassessment

| Field | 記入内容 |
|---|---|
| Control failure | 確認した不備か仮説か、支えるEvidenceと範囲 |
| Corrective action | 改善案、Control ID、実施前提、実施と効果の区別 |
| Validation requirement | 同一対象・版・Window、観測と反例、受入基準 |
| Owner / due | 誰が何をいつ確認するか。計画を完了にしない |
| Reassessment ID / trigger | 新Evidence、Clock条件、Scope、代替説明の変化 |
| Recovery / residual | 第19章の判断と区別し、未評価・残余を明示 |
| Handoff | 宛先、Question、送付・受領、Receipt、実行権限 |

## Evidence and safety boundary

原本と作業Copy、Sourceと来歴、変換履歴、Cutoff、Hashの比較対象を記す。Hashは真正性、実権限、法的適格性の証明ではない。本教材は完全合成の読解のみで、実Incident、実収集、実変更、実通知は0件である。追加の実Dataや許可不明の操作が必要なら停止する。

## Review checklist

- 原因、Trigger、寄与要因、影響範囲の欄が別になっている。
- Evidenceと反証・代替説明が同じ対象・版・Cutoffに対応する。
- 確信度を上げた理由が、単に別の説明が弱くなったことだけではない。
- GapとUnknown、Owner、期限、再評価条件が残る。
- 改善案やHandoffを、実施・効果・受領と同一視しない。
