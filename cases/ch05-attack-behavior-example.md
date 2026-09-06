# 第5章 合成記入例：ATT&CK Behavior Map

## この記入例の扱い

完全合成の読解教材である。実Target、実Log、実Credentialは使用しない。外部通信、設定変更、Token取得は行わない。
入力は[合成Dataset](./fixtures/ch05-attack-behavior.json)、空欄の書式は[ART-15 Template](../templates/attack-behavior-map.md)である。JSONが機械可読の正本であり、以下の表は同じ値を表示する。

## Document Control

| Field | Value |
|---|---|
| artifactId | ART-15 |
| mapId | BMAP-2026-001 |
| parentCaseId | CASE-2026-001 |
| relation | refines |
| parentThreatModelId | TM-2026-001 |
| decisionRequirementId | DR-2026-001 |
| authorizationRecordId | AUTH-CASE-2026-001 |
| scope | read-only-synthetic-data |
| catalogVersion | 19.2 |
| teachingModel | Office Suite teaching model only; parent product/environment remains unconfirmed. |
| parentState | Chapter 4 source snapshot retained; no parent hypothesis, control, gap or decision is updated. |

[第4章の親Case](./ch04-threat-model-example.md)のTH-2026-001〜006は、同じ命題としてjoinしない。第1章の過去判断期限、REA-2026-001、第4章の各Gap / Control assuranceは元の時点と意味を維持する。本章の2026-09-20は教材Mapの再評価日であり、親Decisionの期限を更新するものではない。

## 継承と条件

AUTH-CASE-2026-001のProceed with conditions、COND-AUTH-2026-001〜003を実行権限の拡張に使わない。教材の作業コピーを読む範囲だけを扱う。新しい環境操作、Snapshot収集、Rule test実行は親Caseの再承認条件へ戻る。
TH-2026-001はhistorical scopeの命題、TH-2026-004はsummary-only境界のrefinementである。TH-2026-002はAdmin consent Event / Rule、TH-2026-005はApp lifecycle / decision summaryを扱う。TH-2026-003の発生有無とTH-2026-006の機会条件・影響範囲は別々に保留する。

Office Suite向けAN1487を選ぶのは、この派生教材で仮置きしたモデルに限る。親Caseの製品・環境がOffice Suiteだと確定したわけではない。AN1488への切替えはSaaSという名称だけで決めず、前提・Data・正常系の差を再Reviewする。

## 既存Controlの参照

親Controlの予防・検知・安全境界に関する状態を参照し、本章のStatusで更新しない。対応する単一Controlを特定しないBM-2026-003はcontrolIdsを「なし」とする。新たな対応・Response Controlが検証されたという意味ではない。

| Control ID | Role | Assurance | Parent Evidence IDs | Limitation |
|---|---|---|---|---|
| CTRL-2026-005 | 業務要件とscopeのReview | Documented | EVD-2026-002 | 人手差分に依存し、実施有効性の証明ではない |
| CTRL-2026-006 | Workload identityの分離と管理 | Documented | EVD-2026-001 | 親EvidenceはApp registration scope Snapshotだけ。bindingと管理手順の実施結果は未収集 |
| CTRL-2026-007 | Admin consent / App lifecycleのAudit coverage | Documented | EVD-2026-003 | 親EvidenceはAdmin consentだけ。App lifecycleと複合ControlのRule testは未収集 |
| CTRL-2026-008 | Labのno outbound / Stop / Cleanup | Documented | EVD-AUTH-2026-001, SYNTH-REV-TM-SAFE-001 | 設計Reviewだけ。default-deny、preflight、Cleanupの実施結果は未収集 |
| CTRL-2026-009 | summary-only Field normalizationの説明 | Unknown | NEG-2026-001 | Vendor内部補正の完全性は直接確認できない |

## BM-2026-001

| Field | Value |
|---|---|
| rowId | BM-2026-001 |
| threatId | TH-2026-001 |
| assetIds | ASSET-2026-002, ASSET-2026-005 |
| boundaryIds | TB-2026-001, TB-2026-003 |
| flowIds | FLOW-2026-002, FLOW-2026-004 |
| catalogVersion | 19.2 |
| techniqueId | T1671 |
| tacticId | TA0003 |
| subtechniqueId | なし |
| mappingBasis | Hypothesized |
| preconditions | 承認状態と連携変更の対応、現在の設定は未確認を含む |
| observableBehavior | SaaS連携の承認と活動の関係が正規の利用条件と整合せず残るという仮説 |
| analyticIds | AN1487 |
| dataComponentIds | DC0066, DC0069 |
| telemetryId | TEL-BM-001 |
| detectionId | なし |
| evidenceIds | なし |
| status | Mapped |
| validationTestId | なし |
| limitation | 過大scopeだけでは行動の発生を示さない。historical scopeはcurrent scopeではない |
| alternativeMapping | 正常な承認変更、または観測Data不足による見かけの不整合 |
| decisionContribution | T1671の候補対応を保持し、現在の前提を確認するまで結論を進めない |
| gapId | GAP-BM-001 |
| owner | SYNTH-SOC-REVIEWER |
| reviewDate | 2026-09-20 |
| reassessmentTrigger | 必要Field、承認記録、ScopeまたはATT&CK Objectの変更 |
| controlIds | CTRL-2026-005, CTRL-2026-006 |

## BM-2026-002

| Field | Value |
|---|---|
| rowId | BM-2026-002 |
| threatId | TH-2026-002 |
| assetIds | ASSET-2026-002, ASSET-2026-005 |
| boundaryIds | TB-2026-001, TB-2026-003 |
| flowIds | FLOW-2026-002, FLOW-2026-004 |
| catalogVersion | 19.2 |
| techniqueId | T1671 |
| tacticId | TA0003 |
| subtechniqueId | なし |
| mappingBasis | Observed |
| preconditions | 承認状態と連携変更の対応、現在の設定は未確認を含む |
| observableBehavior | 合成記録で同意変更が記録された |
| analyticIds | AN1487 |
| dataComponentIds | DC0066, DC0069 |
| telemetryId | TEL-BM-002 |
| detectionId | なし |
| evidenceIds | EVD-BM-002 |
| status | Observed |
| validationTestId | なし |
| limitation | 合成変更の観測だけで悪意、早期検知、有効なControlを主張しない |
| alternativeMapping | 正常な承認変更、または観測Data不足による見かけの不整合 |
| decisionContribution | TH-2026-002のEventとRuleの問題を分離して引き渡す |
| gapId | GAP-BM-002 |
| owner | SYNTH-SOC-REVIEWER |
| reviewDate | 2026-09-20 |
| reassessmentTrigger | 必要Field、承認記録、ScopeまたはATT&CK Objectの変更 |
| controlIds | CTRL-2026-007, CTRL-2026-008 |

## BM-2026-003

| Field | Value |
|---|---|
| rowId | BM-2026-003 |
| threatId | TH-2026-003 |
| assetIds | ASSET-2026-001, ASSET-2026-003 |
| boundaryIds | TB-2026-002, TB-2026-003 |
| flowIds | FLOW-2026-004 |
| catalogVersion | 19.2 |
| techniqueId | なし |
| tacticId | なし |
| subtechniqueId | なし |
| mappingBasis | Hypothesized |
| preconditions | 承認状態と連携変更の対応、現在の設定は未確認を含む |
| observableBehavior | 既往の不正利用を判断するための観測範囲が不足している |
| analyticIds | なし |
| dataComponentIds | なし |
| telemetryId | TEL-BM-003 |
| detectionId | なし |
| evidenceIds | なし |
| status | Unknown |
| validationTestId | なし |
| limitation | Telemetry欠落は不正利用の不存在を意味しない |
| alternativeMapping | 正常な承認変更、または観測Data不足による見かけの不整合 |
| decisionContribution | 発生有無はUnknownとして維持し、TH-2026-006と統合しない |
| gapId | GAP-BM-003 |
| owner | SYNTH-SOC-REVIEWER |
| reviewDate | 2026-09-20 |
| reassessmentTrigger | 必要Field、承認記録、ScopeまたはATT&CK Objectの変更 |
| controlIds | なし |

## BM-2026-004

| Field | Value |
|---|---|
| rowId | BM-2026-004 |
| threatId | TH-2026-002 |
| assetIds | ASSET-2026-002, ASSET-2026-005 |
| boundaryIds | TB-2026-001, TB-2026-003 |
| flowIds | FLOW-2026-002, FLOW-2026-004 |
| catalogVersion | 19.2 |
| techniqueId | T1671 |
| tacticId | TA0003 |
| subtechniqueId | なし |
| mappingBasis | Reproduced |
| preconditions | 承認状態と連携変更の対応、現在の設定は未確認を含む |
| observableBehavior | 3件の合成Consent記録を承認状態で分類した |
| analyticIds | AN1487 |
| dataComponentIds | DC0066, DC0069 |
| telemetryId | TEL-BM-004 |
| detectionId | DET-BM-004 |
| evidenceIds | EVD-BM-004 |
| status | Validated |
| validationTestId | TEST-BM-004 |
| limitation | synthetic-field-classificationだけのPass。T1671の再現、DET0539の製品有効性、親Controlの検証ではない |
| alternativeMapping | 正常な承認変更、または観測Data不足による見かけの不整合 |
| decisionContribution | 教材内の判定手続きを確認した。CTRL-2026-007と親Gapは変更しない |
| gapId | GAP-BM-004 |
| owner | SYNTH-SOC-REVIEWER |
| reviewDate | 2026-09-20 |
| reassessmentTrigger | 必要Field、承認記録、ScopeまたはATT&CK Objectの変更 |
| controlIds | CTRL-2026-007, CTRL-2026-008 |

## BM-2026-005

| Field | Value |
|---|---|
| rowId | BM-2026-005 |
| threatId | TH-2026-004 |
| assetIds | ASSET-2026-005, ASSET-2026-006, ASSET-2026-007 |
| boundaryIds | TB-2026-004, TB-2026-008 |
| flowIds | FLOW-2026-003, FLOW-2026-006 |
| catalogVersion | 19.2 |
| techniqueId | なし |
| tacticId | なし |
| subtechniqueId | なし |
| mappingBasis | Hypothesized |
| preconditions | 承認状態と連携変更の対応、現在の設定は未確認を含む |
| observableBehavior | post-remediationのscopeとWorkload identity bindingの現状を読めない |
| analyticIds | なし |
| dataComponentIds | なし |
| telemetryId | TEL-BM-005 |
| detectionId | なし |
| evidenceIds | なし |
| status | Unknown |
| validationTestId | なし |
| limitation | 第1章の改修Passedからcurrent Snapshotの内容を推定しない |
| alternativeMapping | 正常な承認変更、または観測Data不足による見かけの不整合 |
| decisionContribution | summary-only refinementの判断を留保する |
| gapId | GAP-BM-005 |
| owner | SYNTH-SOC-REVIEWER |
| reviewDate | 2026-09-20 |
| reassessmentTrigger | 必要Field、承認記録、ScopeまたはATT&CK Objectの変更 |
| controlIds | CTRL-2026-005, CTRL-2026-006 |

## BM-2026-006

| Field | Value |
|---|---|
| rowId | BM-2026-006 |
| threatId | TH-2026-005 |
| assetIds | ASSET-2026-002, ASSET-2026-003, ASSET-2026-004 |
| boundaryIds | TB-2026-003, TB-2026-007 |
| flowIds | FLOW-2026-004, FLOW-2026-005 |
| catalogVersion | 19.2 |
| techniqueId | なし |
| tacticId | なし |
| subtechniqueId | なし |
| mappingBasis | Hypothesized |
| preconditions | 承認状態と連携変更の対応、現在の設定は未確認を含む |
| observableBehavior | App identity lifecycle変更とdecision summaryの対応を観測対象として提案する |
| analyticIds | なし |
| dataComponentIds | なし |
| telemetryId | TEL-BM-006 |
| detectionId | なし |
| evidenceIds | なし |
| status | Proposed |
| validationTestId | なし |
| limitation | Defenderの観測不足それ自体はAdversary Techniqueではない |
| alternativeMapping | 正常な承認変更、または観測Data不足による見かけの不整合 |
| decisionContribution | 行動条件が具体化するまでTechniqueを割り当てない |
| gapId | GAP-BM-006 |
| owner | SYNTH-SOC-REVIEWER |
| reviewDate | 2026-09-20 |
| reassessmentTrigger | 必要Field、承認記録、ScopeまたはATT&CK Objectの変更 |
| controlIds | CTRL-2026-007, CTRL-2026-008 |

## BM-2026-007

| Field | Value |
|---|---|
| rowId | BM-2026-007 |
| threatId | TH-2026-006 |
| assetIds | ASSET-2026-001, ASSET-2026-003, ASSET-2026-006 |
| boundaryIds | TB-2026-002, TB-2026-003, TB-2026-007, TB-2026-008 |
| flowIds | FLOW-2026-003, FLOW-2026-004, FLOW-2026-005 |
| catalogVersion | 19.2 |
| techniqueId | なし |
| tacticId | なし |
| subtechniqueId | なし |
| mappingBasis | Hypothesized |
| preconditions | 承認状態と連携変更の対応、現在の設定は未確認を含む |
| observableBehavior | historicalな機会条件とsummary-only境界の影響範囲を限定できない |
| analyticIds | なし |
| dataComponentIds | なし |
| telemetryId | TEL-BM-007 |
| detectionId | なし |
| evidenceIds | なし |
| status | Unknown |
| validationTestId | なし |
| limitation | 機会条件の不確実性は発生の証拠ではない |
| alternativeMapping | 正常な承認変更、または観測Data不足による見かけの不整合 |
| decisionContribution | TH-2026-003の発生有無とは別の情報ギャップとして渡す |
| gapId | GAP-BM-007 |
| owner | SYNTH-SOC-REVIEWER |
| reviewDate | 2026-09-20 |
| reassessmentTrigger | 必要Field、承認記録、ScopeまたはATT&CK Objectの変更 |
| controlIds | CTRL-2026-009 |

## EvidenceとTest

EVD-BM-002はSYNTH-EVENT-BM-001にある合成同意変更を示すだけである。TH-2026-002のRule欠落が解決したとは解釈しない。
EVD-BM-004 / TEST-BM-004 / DET-BM-004はsynthetic-field-classificationに限定した教材結果である。承認状態がunapprovedならneeds-review、approvedならbenign-change、欠落ならinsufficient-dataと分類する。予測した3件の結果と実際の分類結果が一致することを章contractで再計算する。
needs-reviewは悪意確定ではなく、benign-changeもシステム全体の侵害不存在ではない。Rule versionは1.0.0。DET0539を実製品に実装・試験した結果ではない。

## DataとGap

TEL-BM-001〜007は行ごとに定義する。必須FieldはeventClass、tenant、application、approvalである。TEL-BM-002 / TEL-BM-004は合成Dataだけがあり、他はNot collectedである。親Caseの90日Coverage、retention、API resource / operation Field、App lifecycle結果は未検証のままとする。
GAP-BM-001〜007は各行の限界を保持する本章の情報ギャップであり、第4章GAP-2026-001〜004を閉じる記録ではない。OwnerはSYNTH-SOC-REVIEWER、Review dateは2026-09-20、必要Field・承認記録・Scope・ATT&CK Objectの変更を再評価Triggerとする。

## DecisionとHandoff

判断はT1671の条件付き候補を維持し、観測不足は留保することである。Catalog coverageの分母はこの7行、Objectの種類はT1671のみであり、製品Coverage率として使わない。Mapped / Observed / Validatedは異なる軸の証拠閾値を持ち、同じTechniqueへ対応する行を重複集計しない。
HO-BM-006は第6・16章へField、観測点、欠落とOwnerを渡す。HO-BM-017は第17・18・21章へ条件付き候補と有限教材結果を渡す。HO-BM-026は第26章へ出典・版・代替説明・共有範囲を渡す。受入条件と差戻し条件は合成Datasetに固定する。
OWNはBehavior Map、BRIDGEは親Threat Modelと後続Detection、DELEGATEは製品実装である。実用Ruleや侵害手順を本章の成果物へ追加しない。

## 安全と評価

Scopeはread-only-synthetic-data。実Log、実Credential、個人情報、出典不明Data、Scope外の対象を認めたら停止し、追加取得せず教材管理者へ確認する。Cleanupは自分の作業コピーだけを整理する。原典や親CaseのEvidenceを削除しない。
評価はIDの追跡、Statusの証拠閾値、代替説明、Gap、Handoff、安全境界で行う。この記入例のPassはRepositoryの独立Review承認や実務のAuthorizationを意味しない。
