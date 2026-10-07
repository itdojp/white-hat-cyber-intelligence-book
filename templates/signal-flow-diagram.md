# Signal Flow Diagram

## Document Control

Artifact IDは`ART-16`。本Templateは操作から観測・判断へ接続する記録であり、認可の付与、製品の監視設定、侵害判定を行うものではない。

| Field | 記入内容 |
|---|---|
| Signal Flow Map ID / Case ID / Relation | 子記録ID、親Case、refines等の関係 |
| Decision Requirement / Parent Behavior | 判断要求、第5章Behavior ID、親Statusを更新しない限定 |
| Authority / Scope | 教材ではread-only-synthetic-dataだけ |
| Owner / Review date | 担当Role、再確認期限 |
| Source / Version | 用いる一次資料と教材契約の版 |

## Flowの記入

一つのFlowには安定したNode IDとEdge IDを付ける。分岐する場合は条件を明示し、同じEventと無関係な経路をEvidenceとして流用しない。

| 記録単位 | 必須項目 |
|---|---|
| Actor / Identity | 主体ID、Human / Workload / Service、binding、Credential classだけ |
| Request / Boundary | Protocol class、目的、Asset ID、Boundary ID |
| Decision / Effect | Authentication、Authorization、Enforcement、State changeまたはData access |
| Event / Collector | Producer、Event class、必須Field、受領先、収集時刻 |
| Normalization / Retention | 変換版、欠落Field、保存先、保持区間 |
| Query / Consumer | 検索時点、対象期間、権限Role、Evidence / Detection consumer |
| Time / Correlation | Clock source、UTC offset、誤差秒数、Token値を含まないkey |
| Gap / Decision | 不足、許容結論、代替説明、確信度、Owner、期限、再評価条件 |

## Coverageと受入条件

Statusは`Produced / Collected / Retained / Queryable / Validated / Unknown`だけを使う。各段階のEvidence IDを独立に持ち、同じFlow、Event、時点、Fieldを参照する。以前収集していても保持期限切れなら、現在検索できるとはしない。Queryableを検証済みへ自動昇格させない。

Validatedには同一FlowのTest ID、Scope、期待値、実際値、版、結果と限界が必要である。No logをNo eventやNo compromiseへ変換しない。UnknownでもGap、Owner、期限、許容結論が揃えば提出可能である。

## Safety / Stop / Cleanup

完全合成の値なしモデルだけを記入する。実Token、Cookie、Secret、実Log、個人情報は含めない。外部接続と認証試行は行わない。実Dataの疑い、許可の不明、追跡の不一致で停止する。自分の演習コピーだけを整理し、正本や親CaseのEvidenceは変更しない。

## HandoffとRubric

第12〜13章へIdentity bindingと境界、第16章へEvent / Field / 期間、第17章へTestのScope、第20章へClock uncertaintyと変換来歴を渡す。受入側が同一FlowのEvidenceを復元できなければ差し戻す。

[第6章](../manuscript/06-observable-systems.md)の5観点Rubricと[完全合成記入例](../cases/ch06-signal-flow-example.md)を用いる。本書はSignal Flow判断をOWNし、Protocolと基盤実装はDELEGATE、検知・DFIRへの受渡しをBRIDGEする。
