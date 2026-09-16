# Minimal-Impact Validation Record

## このTemplateの扱い

`ART-22`は最小限のEvidence、停止、Cleanup、Residual checkを判断へ接続する記録です。[第14章](../manuscript/14-minimal-impact-validation.md)と[完全合成例](../cases/ch14-minimal-impact-validation-example.md)を併用します。空欄は承認済みの値ではありません。

## 識別と境界

| Field | 記入する内容 |
|---|---|
| Record / Artifact / Case / Relation | 記録ID・版・ART-22・親Case・refines等の根拠 |
| Hypothesis / Parent Finding | 評価する仮説と親の限定された判断 |
| Authority / RoE / Lab Plan | 対象・期限・状態・許可の根拠、失効やDraftを隠さない |
| Subject / Revision / Owner | 資料対象ID・版・所有者 |
| Data classification / Mode | 合成・非実行などの範囲と実測との差 |
| Independent comparison | 独立Caseは親Evidenceや許可に統合しない |

## 問いと最小十分なEvidence

| Field | 記入する内容 |
|---|---|
| Decision question / Minimum evidence question | 判断に必要な条件と対象範囲 |
| Method / Rationale | Static / Simulation / Offline replay / Minimal synthetic operationから選ぶ理由 |
| Execution disposition | 実施有無、未実施ならその理由と安全な代替 |
| Expected / Disconfirming evidence | 条件ID、期待値、反証、未観測の扱い |
| Evidence ID / Subject / Revision / Time | 証拠と問いの直接対応、空slotを観測済みにしない |
| Observation / Limitation / Alternative | 読めた範囲、Gap、代替説明、結論を変える条件 |
| Claim ceiling / Confidence | 実影響・許可へ一般化しない主張上限と確信度 |

## 停止と残存確認

| Field | 記入する内容 |
|---|---|
| Stop ID / Trigger / Evidence / Reason | 十分なEvidence、不足、想定外入力の停止根拠 |
| Post-stop steps / Next action | 追加操作を続けず、記録と責任者判断へ戻す |
| Cleanup ID / Scope / Owner / Evidence | 自分の作業コピーと正本・親Evidenceを区別する |
| Residual ID / Scope / Reviewer / Evidence | 整理の記入とは別に残存の確認を記録する |
| Actual operation / Actual deletion | 記録上の値と実測の有無を区別する |

## 判断とHandoff

| Field | 記入する内容 |
|---|---|
| Result | Supported / Partially supported / Weakened / Inconclusive / Rejected / Stopped |
| Supported scope / Gap | 支持・反証・未確認を対象条件ごとに分ける |
| Record status | Cleanup・Residual未完了ならOpen、Resultと混同しない |
| Finding / Treatment / Decision | 仮説、Evidence、停止、制限をIDで結ぶ |
| Owner / Reassessment / Due / Reopen | 次の責任者、期限、結論を見直す条件 |
| Handoff | 第15章・第21章への受渡し計画と未完了の区別 |

Not performedは実施有無の欄であり、第七のResultではありません。親の失効AUTH、RoE Draft、Unknown、独立Caseを本Templateの記入だけで昇格させません。実Data取得、Credential再利用、横展開、永続化、回避、DoS、破壊は実施しません。
