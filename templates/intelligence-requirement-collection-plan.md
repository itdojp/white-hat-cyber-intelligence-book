# Intelligence Requirement and Collection Plan

`ART-29`は判断要求から回答基準、収集要求、Gap、配布、再評価を辿る成果物である。所属章は[第23章](../manuscript/23-intelligence-requirements.md)。[全欄の完全合成例](../cases/ch23-intelligence-requirements-example.md)、[JSON](../cases/fixtures/ch23-intelligence-requirements.json)、[Schema](../schemas/ch23-intelligence-requirements.schema.json)を併用する。

## 利用境界

本教材では供給Dataの読解だけを扱う。Purposeは問いと不足の整理、Prerequisiteは完全合成Case、Authority / Scopeは教材記入のみ、Expected evidenceは回答基準と参照の対応表、Impactは教材内に限る。未知の権限・実Data・外部接続が必要ならStopし、Cleanupは作業用記入内容の整理だけとする。実行権限、実収集、実操作、実通知を成果物から発生させない。

## 記入順序

| 記録 | 必須内容 | 照合する条件 |
|---|---|---|
| Plan / Case | Plan ID、ART-29、Case ID、Subject、版、Cutoff | 親Caseとのrefinesと非継承を明記 |
| Decision | ID、Owner、問い、開始・期限、Options、可逆性 | 何をいつまでに選ぶかを先に固定 |
| Requirement | ID、Decision ID、Priority、Time horizon、Supporting question | 判断に関係する有限の問いへ分解 |
| Answer criteria | 条件ID、条件の意味、Minimum confidence | 回答として認める対象・範囲を定義 |
| Facts / Assumptions | Fact IDとEvidence、Assumption IDと確認方法 | 事実を推測で埋めない |
| Collection | ID、Requirement IDs、Source class、Method class | 多対多を両方向で一致させる |
| Boundary | Authority、Terms、Classification、Privacy、Retention、Stop | 不明ならBlocked、実収集へ進まない |
| Execution plan | Cost、Owner、Deadline、Status、Deliverables | 教材上の計画と実行を区別 |
| Source / Evidence | Source ID、品質と理由、来歴、独立性、Evidence ID | 対象・版・Window・可用時刻・Collectionを結ぶ |
| Answer binding | Criterion ID、Evidence IDs、Confidence | 評価済みSourceと回答条件の一致を照合 |
| Gap | Gap ID、未充足Criterion、Owner、Deadline、Confidence limit | 残る条件を過不足なく保持 |
| Judgment | 許容結論、代替説明、確信度、無効化条件 | Gapを残す場合は結論を限定 |
| Processing / Analysis | 各Owner、期限 | 収集後・配布前の時間を確保 |
| Distribution | Audience、期限、Status、Receipt | 予定と配達済みを混同しない |
| Feedback / Reassessment | 質問、Owner、無効化条件、再評価ID・時刻 | 期限や条件変更を次の問いへ戻す |

## 有限StatusとPriority

Statusは`Planned / Collecting / Satisfied / Partially satisfied / Blocked / Cancelled`の六種類。RequirementとCollectionで同じ名称を使うが、前者は回答条件、後者はDeliverableに対する状態である。Collection完了だけでRequirementを昇格させない。BlockedにはBlocker、Cancelledには取消理由を残す。これらを欠落行やSatisfiedへ置換しない。

Priorityは`P0 Decision blocking / P1 Required / P2 Useful / P3 Deferred / P4 Not collect`。Time horizonは`Tactical / Operational / Strategic`、確信度は`高・中・低`を用いる。いずれも本書の教育用分類であり、法的権限やSource品質を推定する規則ではない。

## 記入例と差戻し

IR23-R2はC1/C3へ結び、E2が一条件だけを満たす。E4はSource品質pendingなので回答へ使わず、GAP-IR23-R2-Bを残す。StatusはPartially satisfied、確信度は低、再評価はREASS-IR23-001である。IDがあるという理由だけで二条件ともSatisfiedにした記録は差し戻す。

C6はAuthorityとTermsがunknownのためBlocked。C8は重複案のCancelledで、どちらも実施済みとは扱わない。停止の事業影響が重要であっても、優先度でこの境界を解除しない。

## Handoff

第24章へSource/Provenance、第25章へ仮説・代替説明・Gap、第26章へAudience・Decision deadlineを渡す予定を記す。本例のStatusはplanned-not-delivered、Receiptはnull、executionAuthorizedはfalseである。計画の記入を受領や実行許可へ変換しない。

## 提出前確認

問い、条件、Evidence、Source、Gap、Owner、期限を両方向に辿る。対象外、異版、Cutoff後、未評価SourceのEvidenceを回答へ結ばない。同じ根拠の複製を独立Sourceとして数えない。全Requirementを充足させるのではなく、未充足の理由と次の判断が説明できる成果物を提出する。
