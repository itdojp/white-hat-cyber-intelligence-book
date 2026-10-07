# 測定と改善判断の完全合成例

`CASE-IMP-2026-001` / `SIB-2026-022-001`は、[第22章](../manuscript/22-measurement-improvement.md)の[ART-28](../templates/security-improvement-backlog.md)記入例である。[合成JSON](fixtures/ch22-measurement-improvement.json)と[閉Schema](../schemas/ch22-measurement-improvement.schema.json)が値と構造の正本で、本ページは全欄を読める形で併記する。

## 読み方と実権限の境界

この教材は著者が定義した有限の供給値を計算・比較するための記録である。八つの項目や二つの入力版は、一つの実案件を追跡して観測した時系列ではない。`CASE-2026-001`と`CASE-DET-2026-001`への`refines`は方法参照だけで、親からEvidenceや権限を受け取ったことにはならない。

親21の`HOF-CV21-22`はplanned-not-delivered、Receiptはnullのままである。期限切れの`AUTH-CASE-2026-001`、Draftの`ROE-2026-009`、Runtime未実施の`LABPLAN-2026-001`を保持する。新たな実操作・実収集・実通知・実Deploy・実Incident宣言はすべて0件である。実組織のRisk reductionは未測定で、Verifiedも供給条件の照合に限る。

## 五つの対比

| 問い | 参照Metric | 有限比較と残る限界 |
|---|---|---|
| Rule件数と重要範囲は同じか | MET-IMP22-001 / 002 | 件数4→8、重要行動2/5→2/5。件数だけの増加をCoverage拡大と呼ばない |
| Mappingは検証か | MET-IMP22-003 / 004 | 同じ十仮説のmapping9/10、供給検証2/10。未検証八件が残る |
| 速さは品質を保つか | MET-IMP22-005 / 006 | 平均10→5分、中央値6→3分、nearest-rank p90は25→15分。一方、根拠充足5/5→2/5 |
| Telemetryの供給条件差は何を支持するか | MET-IMP22-007 | 同じ十件でInconclusive4/10→1/10。実侵害率や親Huntの改善を認定しない |
| Control再比較はどこまで一般化できるか | MET-IMP22-008 | SCN-CV21-003の三条件一致2/3と010の3/3を方法参照。旧Failedと正常・Near-missを保持する |

MET-IMP22-005のsamplesはpopulationMembersの順に対応する分単位の供給値である。baselineとcurrentのSubject revisionは別の入力版であり、同じWindow・母集団で比較する。値は有理数の`[分子, 分母]`を保ち、不必要な小数精度を作らない。p90の方式と標本数も明示する。

MET-IMP22-006の三件は、必要Evidenceの不充足が供給記録で既知である。計算入力自体の欠測ではない。一方、MET-IMP22-009は権限根拠の入力が欠けるため`unknown: missing-input`であり、0%へ変換しない。分母0の一般的な計算も`unknown: zero-denominator`として区別する。

## 八項目の状態と次の判断

| Item | Status | 判断の読み方 |
|---|---|---|
| BLI-IMP22-001 | Proposed | 重要行動と検証条件を固定する案。検証未実施 |
| BLI-IMP22-002 | Approved | 供給計画の承認だけ。001への依存は未解消で、実操作を認めない |
| BLI-IMP22-003 | In progress | 供給Workflowの検討記録を作成中。品質低下を時間短縮で隠さない |
| BLI-IMP22-004 | Verified | VAL-IMP22-004 / EVD-IMP22-V004が同じHunt比較の入力根拠を参照する |
| BLI-IMP22-005 | Verified | VAL-IMP22-005 / EVD-IMP22-V005が限定したControl比較を参照する |
| BLI-IMP22-006 | Blocked | 権限根拠の不足をunknownのまま残し、実操作へ進まない |
| BLI-IMP22-007 | Accepted | 知識不足を残す供給判断。Risk ownerと期限があり、検証成功ではない |
| BLI-IMP22-008 | Retired | 活動件数という指標の役割を終了。旧値を残し002と006を代替先にする |

各MetricのreassessmentIdは、その問いを主に担当するItemのReassessmentへ結ぶ。MET-IMP22-002を再利用するAccepted項目には、受容期限に対する別のREA-IMP22-007もある。Risk受容は2026-10-01までで、再評価予定はその前の2026-09-30である。この供給日付は現在の実権限や実組織の有効なRisk受容を表さない。

## 全欄の読み方

以下の見出しがRecord内のObjectまたはMetric / Item IDを表し、FieldはそのObjectからのPathである。空配列、false、nullも省略しない。記録の完成はすべての項目のVerified化を意味しない。

### schemaVersion

| Field | Value |
|---|---|
| `schemaVersion` | `1.0.0` |

### synthetic

| Field | Value |
|---|---|
| `synthetic` | `true` |

### readOnly

| Field | Value |
|---|---|
| `readOnly` | `true` |

### networkRequired

| Field | Value |
|---|---|
| `networkRequired` | `false` |

### executionAuthorized

| Field | Value |
|---|---|
| `executionAuthorized` | `false` |

### record

| Field | Value |
|---|---|
| `id` | `SIB-2026-022-001` |
| `caseId` | `CASE-IMP-2026-001` |
| `artifactId` | `ART-28` |
| `asOf` | `2026-09-26T00:00:00Z` |
| `authoring` | `independent-authored-snapshots-not-a-real-case-timeline` |
| `sourceIds/0` | `SRC-NIST-MEASURE-001` |
| `sourceIds/1` | `SRC-NIST-MEASURE-002` |
| `sourceIds/2` | `SRC-CSF-001` |
| `sourceIds/3` | `SRC-IR-001` |
| `sourceIds/4` | `SRC-KEV-001` |
| `actualOperations` | `0` |
| `actualCollections` | `0` |
| `actualNotifications` | `0` |
| `actualDeployments` | `0` |
| `actualIncidentDeclarations` | `0` |

### parentReferences

| Field | Value |
|---|---|
| `use` | `method-reference-only` |
| `caseIds/0` | `CASE-2026-001` |
| `caseIds/1` | `CASE-DET-2026-001` |
| `controlValidationRecordId` | `CVP-2026-021-001` |
| `controlRetestId` | `RT-CV21-003` |
| `beforeScenarioId` | `SCN-CV21-003` |
| `afterScenarioId` | `SCN-CV21-010` |
| `beforeEvidenceId` | `EVD-CV21-003-01` |
| `afterEvidenceId` | `EVD-CV21-010-01` |
| `parentHandoffId` | `HOF-CV21-22` |
| `parentHandoffStatus` | `planned-not-delivered` |
| `parentReceiptId` | `null` |
| `parentEvidenceTransferred` | `false` |
| `parentStateChanged` | `false` |
| `authorityTransferred` | `false` |

### authorityBoundary

| Field | Value |
|---|---|
| `parentAuthorityId` | `AUTH-CASE-2026-001` |
| `parentExpiresAt` | `2026-08-19T09:00:00Z` |
| `parentRoeId` | `ROE-2026-009` |
| `parentRoeStatus` | `Draft` |
| `parentRoeVersion` | `1` |
| `parentLabId` | `LABPLAN-2026-001` |
| `parentLabRuntimeExecuted` | `false` |
| `parentExecutionAuthorized` | `false` |
| `scope` | `配布JSONの読解と有限比較のみ。実サービスへ接続しない。実Accountは使用しない。実環境で操作しない。` |

### MET-IMP22-001

| Field | Value |
|---|---|
| `id` | `MET-IMP22-001` |
| `type` | `Process` |
| `decisionPurpose` | `重要行動の検証不足に対し、Rule件数だけの増加を区別する。` |
| `definition` | `供給されたRule inventoryのMember数。実製品に導入されたRule数ではない。` |
| `formula` | `count` |
| `unit` | `件` |
| `populationId` | `POP-IMP22-001` |
| `populationRevision` | `POP-REV-001` |
| `populationMembers/0` | `RULE-IMP22-001` |
| `populationMembers/1` | `RULE-IMP22-002` |
| `populationMembers/2` | `RULE-IMP22-003` |
| `populationMembers/3` | `RULE-IMP22-004` |
| `populationMembers/4` | `RULE-IMP22-005` |
| `populationMembers/5` | `RULE-IMP22-006` |
| `populationMembers/6` | `RULE-IMP22-007` |
| `populationMembers/7` | `RULE-IMP22-008` |
| `populationBasis` | `author-selected-finite-teaching-members-not-real-organization` |
| `exclusionReason` | `この著者定義の母集団外は未評価。改善のための事後除外はしない。` |
| `windowStart` | `2026-09-01T09:00:00Z` |
| `windowEnd` | `2026-09-01T09:10:00Z` |
| `cutoff` | `2026-09-01T09:11:00Z` |
| `qualityCriterion` | `供給入力の有無と既知の不一致を区別し、根拠不足をゼロへ置換しない。` |
| `target` | `件数自体の増加を改善目標にしない。` |
| `confidence` | `この供給値の計算は再現可能。実効果の確信度は未評価。` |
| `limitation` | `実測、実組織の分布、因果効果、未選択範囲は評価していない。` |
| `retirementTrigger` | `判断目的の消失、重複、Gaming、Dataの継続取得不能、より適切な代替の出現。` |
| `reassessmentId` | `REA-IMP22-001` |
| `baseline/id` | `SNAP-IMP22-001-baseline` |
| `baseline/evidenceId` | `EVD-IMP22-M001-baseline` |
| `baseline/dataSourceId` | `SYNDS-IMP22-001` |
| `baseline/origin` | `authored-supplied-values-not-measured` |
| `baseline/subjectId` | `SYNTH-IMP22-001` |
| `baseline/subjectRevision` | `INPUT-REV-001` |
| `baseline/populationRevision` | `POP-REV-001` |
| `baseline/windowStart` | `2026-09-01T09:00:00Z` |
| `baseline/windowEnd` | `2026-09-01T09:10:00Z` |
| `baseline/availableAt` | `2026-09-01T09:10:30Z` |
| `baseline/selectedMembers/0` | `RULE-IMP22-001` |
| `baseline/selectedMembers/1` | `RULE-IMP22-002` |
| `baseline/selectedMembers/2` | `RULE-IMP22-003` |
| `baseline/selectedMembers/3` | `RULE-IMP22-004` |
| `baseline/samples` | `[]` |
| `baseline/missingMembers` | `[]` |
| `baseline/expectedResult/count` | `4` |
| `current/id` | `SNAP-IMP22-001-current` |
| `current/evidenceId` | `EVD-IMP22-M001-current` |
| `current/dataSourceId` | `SYNDS-IMP22-001` |
| `current/origin` | `authored-supplied-values-not-measured` |
| `current/subjectId` | `SYNTH-IMP22-001` |
| `current/subjectRevision` | `INPUT-REV-002` |
| `current/populationRevision` | `POP-REV-001` |
| `current/windowStart` | `2026-09-01T09:00:00Z` |
| `current/windowEnd` | `2026-09-01T09:10:00Z` |
| `current/availableAt` | `2026-09-01T09:10:30Z` |
| `current/selectedMembers/0` | `RULE-IMP22-001` |
| `current/selectedMembers/1` | `RULE-IMP22-002` |
| `current/selectedMembers/2` | `RULE-IMP22-003` |
| `current/selectedMembers/3` | `RULE-IMP22-004` |
| `current/selectedMembers/4` | `RULE-IMP22-005` |
| `current/selectedMembers/5` | `RULE-IMP22-006` |
| `current/selectedMembers/6` | `RULE-IMP22-007` |
| `current/selectedMembers/7` | `RULE-IMP22-008` |
| `current/samples` | `[]` |
| `current/missingMembers` | `[]` |
| `current/expectedResult/count` | `8` |

### MET-IMP22-002

| Field | Value |
|---|---|
| `id` | `MET-IMP22-002` |
| `type` | `Leading` |
| `decisionPurpose` | `重要な行動の検証範囲を増やす計画を比較する。` |
| `definition` | `著者が選んだ五つの重要行動のうち、供給比較条件を満たしたMemberの割合。` |
| `formula` | `proportion` |
| `unit` | `割合` |
| `populationId` | `POP-IMP22-002` |
| `populationRevision` | `POP-REV-001` |
| `populationMembers/0` | `CRIT-IMP22-001` |
| `populationMembers/1` | `CRIT-IMP22-002` |
| `populationMembers/2` | `CRIT-IMP22-003` |
| `populationMembers/3` | `CRIT-IMP22-004` |
| `populationMembers/4` | `CRIT-IMP22-005` |
| `populationBasis` | `author-selected-finite-teaching-members-not-real-organization` |
| `exclusionReason` | `この著者定義の母集団外は未評価。改善のための事後除外はしない。` |
| `windowStart` | `2026-09-01T09:00:00Z` |
| `windowEnd` | `2026-09-01T09:10:00Z` |
| `cutoff` | `2026-09-01T09:11:00Z` |
| `qualityCriterion` | `供給入力の有無と既知の不一致を区別し、根拠不足をゼロへ置換しない。` |
| `target` | `未検証三行動の必要Evidenceを定める。全攻撃行動への比率とはしない。` |
| `confidence` | `この供給値の計算は再現可能。実効果の確信度は未評価。` |
| `limitation` | `実測、実組織の分布、因果効果、未選択範囲は評価していない。` |
| `retirementTrigger` | `判断目的の消失、重複、Gaming、Dataの継続取得不能、より適切な代替の出現。` |
| `reassessmentId` | `REA-IMP22-001` |
| `baseline/id` | `SNAP-IMP22-002-baseline` |
| `baseline/evidenceId` | `EVD-IMP22-M002-baseline` |
| `baseline/dataSourceId` | `SYNDS-IMP22-002` |
| `baseline/origin` | `authored-supplied-values-not-measured` |
| `baseline/subjectId` | `SYNTH-IMP22-001` |
| `baseline/subjectRevision` | `INPUT-REV-001` |
| `baseline/populationRevision` | `POP-REV-001` |
| `baseline/windowStart` | `2026-09-01T09:00:00Z` |
| `baseline/windowEnd` | `2026-09-01T09:10:00Z` |
| `baseline/availableAt` | `2026-09-01T09:10:30Z` |
| `baseline/selectedMembers/0` | `CRIT-IMP22-001` |
| `baseline/selectedMembers/1` | `CRIT-IMP22-002` |
| `baseline/samples` | `[]` |
| `baseline/missingMembers` | `[]` |
| `baseline/expectedResult/numerator` | `2` |
| `baseline/expectedResult/denominator` | `5` |
| `baseline/expectedResult/ratio/0` | `2` |
| `baseline/expectedResult/ratio/1` | `5` |
| `current/id` | `SNAP-IMP22-002-current` |
| `current/evidenceId` | `EVD-IMP22-M002-current` |
| `current/dataSourceId` | `SYNDS-IMP22-002` |
| `current/origin` | `authored-supplied-values-not-measured` |
| `current/subjectId` | `SYNTH-IMP22-001` |
| `current/subjectRevision` | `INPUT-REV-002` |
| `current/populationRevision` | `POP-REV-001` |
| `current/windowStart` | `2026-09-01T09:00:00Z` |
| `current/windowEnd` | `2026-09-01T09:10:00Z` |
| `current/availableAt` | `2026-09-01T09:10:30Z` |
| `current/selectedMembers/0` | `CRIT-IMP22-001` |
| `current/selectedMembers/1` | `CRIT-IMP22-002` |
| `current/samples` | `[]` |
| `current/missingMembers` | `[]` |
| `current/expectedResult/numerator` | `2` |
| `current/expectedResult/denominator` | `5` |
| `current/expectedResult/ratio/0` | `2` |
| `current/expectedResult/ratio/1` | `5` |

### MET-IMP22-003

| Field | Value |
|---|---|
| `id` | `MET-IMP22-003` |
| `type` | `Leading` |
| `decisionPurpose` | `対応表の広さと検証不足を分離する。` |
| `definition` | `同じ十仮説のうち、対応表に記載のあるMemberの割合。有効性の測定ではない。` |
| `formula` | `proportion` |
| `unit` | `割合` |
| `populationId` | `POP-IMP22-003` |
| `populationRevision` | `POP-REV-001` |
| `populationMembers/0` | `HYP-IMP22-001` |
| `populationMembers/1` | `HYP-IMP22-002` |
| `populationMembers/2` | `HYP-IMP22-003` |
| `populationMembers/3` | `HYP-IMP22-004` |
| `populationMembers/4` | `HYP-IMP22-005` |
| `populationMembers/5` | `HYP-IMP22-006` |
| `populationMembers/6` | `HYP-IMP22-007` |
| `populationMembers/7` | `HYP-IMP22-008` |
| `populationMembers/8` | `HYP-IMP22-009` |
| `populationMembers/9` | `HYP-IMP22-010` |
| `populationBasis` | `author-selected-finite-teaching-members-not-real-organization` |
| `exclusionReason` | `この著者定義の母集団外は未評価。改善のための事後除外はしない。` |
| `windowStart` | `2026-09-01T09:00:00Z` |
| `windowEnd` | `2026-09-01T09:10:00Z` |
| `cutoff` | `2026-09-01T09:11:00Z` |
| `qualityCriterion` | `供給入力の有無と既知の不一致を区別し、根拠不足をゼロへ置換しない。` |
| `target` | `対応表から検証済み割合へ自動変換しない。` |
| `confidence` | `この供給値の計算は再現可能。実効果の確信度は未評価。` |
| `limitation` | `実測、実組織の分布、因果効果、未選択範囲は評価していない。` |
| `retirementTrigger` | `判断目的の消失、重複、Gaming、Dataの継続取得不能、より適切な代替の出現。` |
| `reassessmentId` | `REA-IMP22-002` |
| `baseline/id` | `SNAP-IMP22-003-baseline` |
| `baseline/evidenceId` | `EVD-IMP22-M003-baseline` |
| `baseline/dataSourceId` | `SYNDS-IMP22-003` |
| `baseline/origin` | `authored-supplied-values-not-measured` |
| `baseline/subjectId` | `SYNTH-IMP22-001` |
| `baseline/subjectRevision` | `INPUT-REV-001` |
| `baseline/populationRevision` | `POP-REV-001` |
| `baseline/windowStart` | `2026-09-01T09:00:00Z` |
| `baseline/windowEnd` | `2026-09-01T09:10:00Z` |
| `baseline/availableAt` | `2026-09-01T09:10:30Z` |
| `baseline/selectedMembers/0` | `HYP-IMP22-001` |
| `baseline/selectedMembers/1` | `HYP-IMP22-002` |
| `baseline/selectedMembers/2` | `HYP-IMP22-003` |
| `baseline/selectedMembers/3` | `HYP-IMP22-004` |
| `baseline/selectedMembers/4` | `HYP-IMP22-005` |
| `baseline/selectedMembers/5` | `HYP-IMP22-006` |
| `baseline/selectedMembers/6` | `HYP-IMP22-007` |
| `baseline/selectedMembers/7` | `HYP-IMP22-008` |
| `baseline/selectedMembers/8` | `HYP-IMP22-009` |
| `baseline/samples` | `[]` |
| `baseline/missingMembers` | `[]` |
| `baseline/expectedResult/numerator` | `9` |
| `baseline/expectedResult/denominator` | `10` |
| `baseline/expectedResult/ratio/0` | `9` |
| `baseline/expectedResult/ratio/1` | `10` |
| `current/id` | `SNAP-IMP22-003-current` |
| `current/evidenceId` | `EVD-IMP22-M003-current` |
| `current/dataSourceId` | `SYNDS-IMP22-003` |
| `current/origin` | `authored-supplied-values-not-measured` |
| `current/subjectId` | `SYNTH-IMP22-001` |
| `current/subjectRevision` | `INPUT-REV-002` |
| `current/populationRevision` | `POP-REV-001` |
| `current/windowStart` | `2026-09-01T09:00:00Z` |
| `current/windowEnd` | `2026-09-01T09:10:00Z` |
| `current/availableAt` | `2026-09-01T09:10:30Z` |
| `current/selectedMembers/0` | `HYP-IMP22-001` |
| `current/selectedMembers/1` | `HYP-IMP22-002` |
| `current/selectedMembers/2` | `HYP-IMP22-003` |
| `current/selectedMembers/3` | `HYP-IMP22-004` |
| `current/selectedMembers/4` | `HYP-IMP22-005` |
| `current/selectedMembers/5` | `HYP-IMP22-006` |
| `current/selectedMembers/6` | `HYP-IMP22-007` |
| `current/selectedMembers/7` | `HYP-IMP22-008` |
| `current/selectedMembers/8` | `HYP-IMP22-009` |
| `current/samples` | `[]` |
| `current/missingMembers` | `[]` |
| `current/expectedResult/numerator` | `9` |
| `current/expectedResult/denominator` | `10` |
| `current/expectedResult/ratio/0` | `9` |
| `current/expectedResult/ratio/1` | `10` |

### MET-IMP22-004

| Field | Value |
|---|---|
| `id` | `MET-IMP22-004` |
| `type` | `Outcome` |
| `decisionPurpose` | `同じ仮説の供給検証がどこまで完了したかを問う。` |
| `definition` | `十仮説のうち、供給された正常・異常対比の必須条件を満たしたMemberの割合。` |
| `formula` | `proportion` |
| `unit` | `割合` |
| `populationId` | `POP-IMP22-004` |
| `populationRevision` | `POP-REV-001` |
| `populationMembers/0` | `HYP-IMP22-001` |
| `populationMembers/1` | `HYP-IMP22-002` |
| `populationMembers/2` | `HYP-IMP22-003` |
| `populationMembers/3` | `HYP-IMP22-004` |
| `populationMembers/4` | `HYP-IMP22-005` |
| `populationMembers/5` | `HYP-IMP22-006` |
| `populationMembers/6` | `HYP-IMP22-007` |
| `populationMembers/7` | `HYP-IMP22-008` |
| `populationMembers/8` | `HYP-IMP22-009` |
| `populationMembers/9` | `HYP-IMP22-010` |
| `populationBasis` | `author-selected-finite-teaching-members-not-real-organization` |
| `exclusionReason` | `この著者定義の母集団外は未評価。改善のための事後除外はしない。` |
| `windowStart` | `2026-09-01T09:00:00Z` |
| `windowEnd` | `2026-09-01T09:10:00Z` |
| `cutoff` | `2026-09-01T09:11:00Z` |
| `qualityCriterion` | `供給入力の有無と既知の不一致を区別し、根拠不足をゼロへ置換しない。` |
| `target` | `未検証八仮説を別に保持する。実検知率とは呼ばない。` |
| `confidence` | `この供給値の計算は再現可能。実効果の確信度は未評価。` |
| `limitation` | `実測、実組織の分布、因果効果、未選択範囲は評価していない。` |
| `retirementTrigger` | `判断目的の消失、重複、Gaming、Dataの継続取得不能、より適切な代替の出現。` |
| `reassessmentId` | `REA-IMP22-002` |
| `baseline/id` | `SNAP-IMP22-004-baseline` |
| `baseline/evidenceId` | `EVD-IMP22-M004-baseline` |
| `baseline/dataSourceId` | `SYNDS-IMP22-004` |
| `baseline/origin` | `authored-supplied-values-not-measured` |
| `baseline/subjectId` | `SYNTH-IMP22-001` |
| `baseline/subjectRevision` | `INPUT-REV-001` |
| `baseline/populationRevision` | `POP-REV-001` |
| `baseline/windowStart` | `2026-09-01T09:00:00Z` |
| `baseline/windowEnd` | `2026-09-01T09:10:00Z` |
| `baseline/availableAt` | `2026-09-01T09:10:30Z` |
| `baseline/selectedMembers/0` | `HYP-IMP22-001` |
| `baseline/selectedMembers/1` | `HYP-IMP22-002` |
| `baseline/samples` | `[]` |
| `baseline/missingMembers` | `[]` |
| `baseline/expectedResult/numerator` | `2` |
| `baseline/expectedResult/denominator` | `10` |
| `baseline/expectedResult/ratio/0` | `1` |
| `baseline/expectedResult/ratio/1` | `5` |
| `current/id` | `SNAP-IMP22-004-current` |
| `current/evidenceId` | `EVD-IMP22-M004-current` |
| `current/dataSourceId` | `SYNDS-IMP22-004` |
| `current/origin` | `authored-supplied-values-not-measured` |
| `current/subjectId` | `SYNTH-IMP22-001` |
| `current/subjectRevision` | `INPUT-REV-002` |
| `current/populationRevision` | `POP-REV-001` |
| `current/windowStart` | `2026-09-01T09:00:00Z` |
| `current/windowEnd` | `2026-09-01T09:10:00Z` |
| `current/availableAt` | `2026-09-01T09:10:30Z` |
| `current/selectedMembers/0` | `HYP-IMP22-001` |
| `current/selectedMembers/1` | `HYP-IMP22-002` |
| `current/samples` | `[]` |
| `current/missingMembers` | `[]` |
| `current/expectedResult/numerator` | `2` |
| `current/expectedResult/denominator` | `10` |
| `current/expectedResult/ratio/0` | `1` |
| `current/expectedResult/ratio/1` | `5` |

### MET-IMP22-005

| Field | Value |
|---|---|
| `id` | `MET-IMP22-005` |
| `type` | `Process` |
| `decisionPurpose` | `判断時間の短縮とEvidence品質の逆行を併せて判断する。` |
| `definition` | `供給された判断開始から判断記録までの五つの時間。個人の作業速度を測らない。` |
| `formula` | `duration-distribution` |
| `unit` | `分` |
| `populationId` | `POP-IMP22-005` |
| `populationRevision` | `POP-REV-001` |
| `populationMembers/0` | `REC-IMP22-001` |
| `populationMembers/1` | `REC-IMP22-002` |
| `populationMembers/2` | `REC-IMP22-003` |
| `populationMembers/3` | `REC-IMP22-004` |
| `populationMembers/4` | `REC-IMP22-005` |
| `populationBasis` | `author-selected-finite-teaching-members-not-real-organization` |
| `exclusionReason` | `この著者定義の母集団外は未評価。改善のための事後除外はしない。` |
| `windowStart` | `2026-09-01T09:00:00Z` |
| `windowEnd` | `2026-09-01T09:10:00Z` |
| `cutoff` | `2026-09-01T09:11:00Z` |
| `qualityCriterion` | `供給入力の有無と既知の不一致を区別し、根拠不足をゼロへ置換しない。` |
| `target` | `品質と安全を保たない時間短縮を合格にしない。` |
| `confidence` | `この供給値の計算は再現可能。実効果の確信度は未評価。` |
| `limitation` | `実測、実組織の分布、因果効果、未選択範囲は評価していない。` |
| `retirementTrigger` | `判断目的の消失、重複、Gaming、Dataの継続取得不能、より適切な代替の出現。` |
| `reassessmentId` | `REA-IMP22-003` |
| `baseline/id` | `SNAP-IMP22-005-baseline` |
| `baseline/evidenceId` | `EVD-IMP22-M005-baseline` |
| `baseline/dataSourceId` | `SYNDS-IMP22-005` |
| `baseline/origin` | `authored-supplied-values-not-measured` |
| `baseline/subjectId` | `SYNTH-IMP22-001` |
| `baseline/subjectRevision` | `INPUT-REV-001` |
| `baseline/populationRevision` | `POP-REV-001` |
| `baseline/windowStart` | `2026-09-01T09:00:00Z` |
| `baseline/windowEnd` | `2026-09-01T09:10:00Z` |
| `baseline/availableAt` | `2026-09-01T09:10:30Z` |
| `baseline/selectedMembers` | `[]` |
| `baseline/samples/0` | `4` |
| `baseline/samples/1` | `5` |
| `baseline/samples/2` | `6` |
| `baseline/samples/3` | `10` |
| `baseline/samples/4` | `25` |
| `baseline/missingMembers` | `[]` |
| `baseline/expectedResult/n` | `5` |
| `baseline/expectedResult/mean/0` | `10` |
| `baseline/expectedResult/mean/1` | `1` |
| `baseline/expectedResult/median/0` | `6` |
| `baseline/expectedResult/median/1` | `1` |
| `baseline/expectedResult/p90` | `25` |
| `baseline/expectedResult/percentileMethod` | `nearest-rank` |
| `current/id` | `SNAP-IMP22-005-current` |
| `current/evidenceId` | `EVD-IMP22-M005-current` |
| `current/dataSourceId` | `SYNDS-IMP22-005` |
| `current/origin` | `authored-supplied-values-not-measured` |
| `current/subjectId` | `SYNTH-IMP22-001` |
| `current/subjectRevision` | `INPUT-REV-002` |
| `current/populationRevision` | `POP-REV-001` |
| `current/windowStart` | `2026-09-01T09:00:00Z` |
| `current/windowEnd` | `2026-09-01T09:10:00Z` |
| `current/availableAt` | `2026-09-01T09:10:30Z` |
| `current/selectedMembers` | `[]` |
| `current/samples/0` | `1` |
| `current/samples/1` | `2` |
| `current/samples/2` | `3` |
| `current/samples/3` | `4` |
| `current/samples/4` | `15` |
| `current/missingMembers` | `[]` |
| `current/expectedResult/n` | `5` |
| `current/expectedResult/mean/0` | `5` |
| `current/expectedResult/mean/1` | `1` |
| `current/expectedResult/median/0` | `3` |
| `current/expectedResult/median/1` | `1` |
| `current/expectedResult/p90` | `15` |
| `current/expectedResult/percentileMethod` | `nearest-rank` |

### MET-IMP22-006

| Field | Value |
|---|---|
| `id` | `MET-IMP22-006` |
| `type` | `Quality` |
| `decisionPurpose` | `判断に必要なEvidenceを失っていないかを確認する。` |
| `definition` | `同じ五判断のうち、必須Evidenceが充足していると供給記録に明示されたMemberの割合。` |
| `formula` | `proportion` |
| `unit` | `割合` |
| `populationId` | `POP-IMP22-006` |
| `populationRevision` | `POP-REV-001` |
| `populationMembers/0` | `REC-IMP22-001` |
| `populationMembers/1` | `REC-IMP22-002` |
| `populationMembers/2` | `REC-IMP22-003` |
| `populationMembers/3` | `REC-IMP22-004` |
| `populationMembers/4` | `REC-IMP22-005` |
| `populationBasis` | `author-selected-finite-teaching-members-not-real-organization` |
| `exclusionReason` | `この著者定義の母集団外は未評価。改善のための事後除外はしない。` |
| `windowStart` | `2026-09-01T09:00:00Z` |
| `windowEnd` | `2026-09-01T09:10:00Z` |
| `cutoff` | `2026-09-01T09:11:00Z` |
| `qualityCriterion` | `供給入力の有無と既知の不一致を区別し、根拠不足をゼロへ置換しない。` |
| `target` | `三記録の不足を隠さず、品質を保つ受入条件を作る。` |
| `confidence` | `この供給値の計算は再現可能。実効果の確信度は未評価。` |
| `limitation` | `実測、実組織の分布、因果効果、未選択範囲は評価していない。` |
| `retirementTrigger` | `判断目的の消失、重複、Gaming、Dataの継続取得不能、より適切な代替の出現。` |
| `reassessmentId` | `REA-IMP22-003` |
| `baseline/id` | `SNAP-IMP22-006-baseline` |
| `baseline/evidenceId` | `EVD-IMP22-M006-baseline` |
| `baseline/dataSourceId` | `SYNDS-IMP22-006` |
| `baseline/origin` | `authored-supplied-values-not-measured` |
| `baseline/subjectId` | `SYNTH-IMP22-001` |
| `baseline/subjectRevision` | `INPUT-REV-001` |
| `baseline/populationRevision` | `POP-REV-001` |
| `baseline/windowStart` | `2026-09-01T09:00:00Z` |
| `baseline/windowEnd` | `2026-09-01T09:10:00Z` |
| `baseline/availableAt` | `2026-09-01T09:10:30Z` |
| `baseline/selectedMembers/0` | `REC-IMP22-001` |
| `baseline/selectedMembers/1` | `REC-IMP22-002` |
| `baseline/selectedMembers/2` | `REC-IMP22-003` |
| `baseline/selectedMembers/3` | `REC-IMP22-004` |
| `baseline/selectedMembers/4` | `REC-IMP22-005` |
| `baseline/samples` | `[]` |
| `baseline/missingMembers` | `[]` |
| `baseline/expectedResult/numerator` | `5` |
| `baseline/expectedResult/denominator` | `5` |
| `baseline/expectedResult/ratio/0` | `1` |
| `baseline/expectedResult/ratio/1` | `1` |
| `current/id` | `SNAP-IMP22-006-current` |
| `current/evidenceId` | `EVD-IMP22-M006-current` |
| `current/dataSourceId` | `SYNDS-IMP22-006` |
| `current/origin` | `authored-supplied-values-not-measured` |
| `current/subjectId` | `SYNTH-IMP22-001` |
| `current/subjectRevision` | `INPUT-REV-002` |
| `current/populationRevision` | `POP-REV-001` |
| `current/windowStart` | `2026-09-01T09:00:00Z` |
| `current/windowEnd` | `2026-09-01T09:10:00Z` |
| `current/availableAt` | `2026-09-01T09:10:30Z` |
| `current/selectedMembers/0` | `REC-IMP22-001` |
| `current/selectedMembers/1` | `REC-IMP22-002` |
| `current/samples` | `[]` |
| `current/missingMembers` | `[]` |
| `current/expectedResult/numerator` | `2` |
| `current/expectedResult/denominator` | `5` |
| `current/expectedResult/ratio/0` | `2` |
| `current/expectedResult/ratio/1` | `5` |

### MET-IMP22-007

| Field | Value |
|---|---|
| `id` | `MET-IMP22-007` |
| `type` | `Quality` |
| `decisionPurpose` | `Telemetry条件の違いが供給Huntの結論保留とどう関係するかを比較する。` |
| `definition` | `同じ十件の供給Huntのうち、Inconclusiveと記録されたMemberの割合。実侵害率ではない。` |
| `formula` | `proportion` |
| `unit` | `割合` |
| `populationId` | `POP-IMP22-007` |
| `populationRevision` | `POP-REV-001` |
| `populationMembers/0` | `HUNT-IMP22-001` |
| `populationMembers/1` | `HUNT-IMP22-002` |
| `populationMembers/2` | `HUNT-IMP22-003` |
| `populationMembers/3` | `HUNT-IMP22-004` |
| `populationMembers/4` | `HUNT-IMP22-005` |
| `populationMembers/5` | `HUNT-IMP22-006` |
| `populationMembers/6` | `HUNT-IMP22-007` |
| `populationMembers/7` | `HUNT-IMP22-008` |
| `populationMembers/8` | `HUNT-IMP22-009` |
| `populationMembers/9` | `HUNT-IMP22-010` |
| `populationBasis` | `author-selected-finite-teaching-members-not-real-organization` |
| `exclusionReason` | `この著者定義の母集団外は未評価。改善のための事後除外はしない。` |
| `windowStart` | `2026-09-01T09:00:00Z` |
| `windowEnd` | `2026-09-01T09:10:00Z` |
| `cutoff` | `2026-09-01T09:11:00Z` |
| `qualityCriterion` | `供給入力の有無と既知の不一致を区別し、根拠不足をゼロへ置換しない。` |
| `target` | `供給比較のInconclusive減少だけを検証し、親Huntの結果を書き換えない。` |
| `confidence` | `この供給値の計算は再現可能。実効果の確信度は未評価。` |
| `limitation` | `実測、実組織の分布、因果効果、未選択範囲は評価していない。` |
| `retirementTrigger` | `判断目的の消失、重複、Gaming、Dataの継続取得不能、より適切な代替の出現。` |
| `reassessmentId` | `REA-IMP22-004` |
| `baseline/id` | `SNAP-IMP22-007-baseline` |
| `baseline/evidenceId` | `EVD-IMP22-M007-baseline` |
| `baseline/dataSourceId` | `SYNDS-IMP22-007` |
| `baseline/origin` | `authored-supplied-values-not-measured` |
| `baseline/subjectId` | `SYNTH-IMP22-001` |
| `baseline/subjectRevision` | `INPUT-REV-001` |
| `baseline/populationRevision` | `POP-REV-001` |
| `baseline/windowStart` | `2026-09-01T09:00:00Z` |
| `baseline/windowEnd` | `2026-09-01T09:10:00Z` |
| `baseline/availableAt` | `2026-09-01T09:10:30Z` |
| `baseline/selectedMembers/0` | `HUNT-IMP22-001` |
| `baseline/selectedMembers/1` | `HUNT-IMP22-002` |
| `baseline/selectedMembers/2` | `HUNT-IMP22-003` |
| `baseline/selectedMembers/3` | `HUNT-IMP22-004` |
| `baseline/samples` | `[]` |
| `baseline/missingMembers` | `[]` |
| `baseline/expectedResult/numerator` | `4` |
| `baseline/expectedResult/denominator` | `10` |
| `baseline/expectedResult/ratio/0` | `2` |
| `baseline/expectedResult/ratio/1` | `5` |
| `current/id` | `SNAP-IMP22-007-current` |
| `current/evidenceId` | `EVD-IMP22-M007-current` |
| `current/dataSourceId` | `SYNDS-IMP22-007` |
| `current/origin` | `authored-supplied-values-not-measured` |
| `current/subjectId` | `SYNTH-IMP22-001` |
| `current/subjectRevision` | `INPUT-REV-002` |
| `current/populationRevision` | `POP-REV-001` |
| `current/windowStart` | `2026-09-01T09:00:00Z` |
| `current/windowEnd` | `2026-09-01T09:10:00Z` |
| `current/availableAt` | `2026-09-01T09:10:30Z` |
| `current/selectedMembers/0` | `HUNT-IMP22-001` |
| `current/samples` | `[]` |
| `current/missingMembers` | `[]` |
| `current/expectedResult/numerator` | `1` |
| `current/expectedResult/denominator` | `10` |
| `current/expectedResult/ratio/0` | `1` |
| `current/expectedResult/ratio/1` | `10` |

### MET-IMP22-008

| Field | Value |
|---|---|
| `id` | `MET-IMP22-008` |
| `type` | `Outcome` |
| `decisionPurpose` | `親21の同一条件の供給Retestを、限定した改善判断へ接続する。` |
| `definition` | `SCN-CV21-003と010で、三つの供給検知出力がControl期待値に一致する割合。` |
| `formula` | `proportion` |
| `unit` | `割合` |
| `populationId` | `POP-IMP22-008` |
| `populationRevision` | `POP-REV-001` |
| `populationMembers/0` | `positive` |
| `populationMembers/1` | `negative` |
| `populationMembers/2` | `benign-near-miss` |
| `populationBasis` | `author-selected-finite-teaching-members-not-real-organization` |
| `exclusionReason` | `この著者定義の母集団外は未評価。改善のための事後除外はしない。` |
| `windowStart` | `2026-09-01T09:00:00Z` |
| `windowEnd` | `2026-09-01T09:10:00Z` |
| `cutoff` | `2026-09-01T09:11:00Z` |
| `qualityCriterion` | `供給入力の有無と既知の不一致を区別し、根拠不足をゼロへ置換しない。` |
| `target` | `旧Failedと正常・Near-missを保持した三条件一致。実RuleのDeployは未実施。` |
| `confidence` | `この供給値の計算は再現可能。実効果の確信度は未評価。` |
| `limitation` | `実測、実組織の分布、因果効果、未選択範囲は評価していない。` |
| `retirementTrigger` | `判断目的の消失、重複、Gaming、Dataの継続取得不能、より適切な代替の出現。` |
| `reassessmentId` | `REA-IMP22-005` |
| `baseline/id` | `SNAP-IMP22-008-baseline` |
| `baseline/evidenceId` | `EVD-IMP22-M008-baseline` |
| `baseline/dataSourceId` | `SYNDS-IMP22-008` |
| `baseline/origin` | `authored-supplied-values-not-measured` |
| `baseline/subjectId` | `SYNTH-IMP22-001` |
| `baseline/subjectRevision` | `INPUT-REV-001` |
| `baseline/populationRevision` | `POP-REV-001` |
| `baseline/windowStart` | `2026-09-01T09:00:00Z` |
| `baseline/windowEnd` | `2026-09-01T09:10:00Z` |
| `baseline/availableAt` | `2026-09-01T09:10:30Z` |
| `baseline/selectedMembers/0` | `negative` |
| `baseline/selectedMembers/1` | `benign-near-miss` |
| `baseline/samples` | `[]` |
| `baseline/missingMembers` | `[]` |
| `baseline/expectedResult/numerator` | `2` |
| `baseline/expectedResult/denominator` | `3` |
| `baseline/expectedResult/ratio/0` | `2` |
| `baseline/expectedResult/ratio/1` | `3` |
| `current/id` | `SNAP-IMP22-008-current` |
| `current/evidenceId` | `EVD-IMP22-M008-current` |
| `current/dataSourceId` | `SYNDS-IMP22-008` |
| `current/origin` | `authored-supplied-values-not-measured` |
| `current/subjectId` | `SYNTH-IMP22-001` |
| `current/subjectRevision` | `INPUT-REV-002` |
| `current/populationRevision` | `POP-REV-001` |
| `current/windowStart` | `2026-09-01T09:00:00Z` |
| `current/windowEnd` | `2026-09-01T09:10:00Z` |
| `current/availableAt` | `2026-09-01T09:10:30Z` |
| `current/selectedMembers/0` | `positive` |
| `current/selectedMembers/1` | `negative` |
| `current/selectedMembers/2` | `benign-near-miss` |
| `current/samples` | `[]` |
| `current/missingMembers` | `[]` |
| `current/expectedResult/numerator` | `3` |
| `current/expectedResult/denominator` | `3` |
| `current/expectedResult/ratio/0` | `1` |
| `current/expectedResult/ratio/1` | `1` |

### MET-IMP22-009

| Field | Value |
|---|---|
| `id` | `MET-IMP22-009` |
| `type` | `Leading` |
| `decisionPurpose` | `権限根拠がない条件を、他の数値で補わず停止する。` |
| `definition` | `教材内の必要な権限根拠の供給有無。実権限を判定したり付与したりしない。` |
| `formula` | `proportion` |
| `unit` | `割合` |
| `populationId` | `POP-IMP22-009` |
| `populationRevision` | `POP-REV-001` |
| `populationMembers/0` | `AUTHORITY-IMP22-001` |
| `populationBasis` | `author-selected-finite-teaching-members-not-real-organization` |
| `exclusionReason` | `この著者定義の母集団外は未評価。改善のための事後除外はしない。` |
| `windowStart` | `2026-09-01T09:00:00Z` |
| `windowEnd` | `2026-09-01T09:10:00Z` |
| `cutoff` | `2026-09-01T09:11:00Z` |
| `qualityCriterion` | `供給入力の有無と既知の不一致を区別し、根拠不足をゼロへ置換しない。` |
| `target` | `根拠がない間はBlocked。実操作を行わない。` |
| `confidence` | `この供給値の計算は再現可能。実効果の確信度は未評価。` |
| `limitation` | `実測、実組織の分布、因果効果、未選択範囲は評価していない。` |
| `retirementTrigger` | `判断目的の消失、重複、Gaming、Dataの継続取得不能、より適切な代替の出現。` |
| `reassessmentId` | `REA-IMP22-006` |
| `baseline/id` | `SNAP-IMP22-009-baseline` |
| `baseline/evidenceId` | `EVD-IMP22-M009-baseline` |
| `baseline/dataSourceId` | `SYNDS-IMP22-009` |
| `baseline/origin` | `authored-supplied-values-not-measured` |
| `baseline/subjectId` | `SYNTH-IMP22-001` |
| `baseline/subjectRevision` | `INPUT-REV-001` |
| `baseline/populationRevision` | `POP-REV-001` |
| `baseline/windowStart` | `2026-09-01T09:00:00Z` |
| `baseline/windowEnd` | `2026-09-01T09:10:00Z` |
| `baseline/availableAt` | `2026-09-01T09:10:30Z` |
| `baseline/selectedMembers` | `[]` |
| `baseline/samples` | `[]` |
| `baseline/missingMembers/0` | `AUTHORITY-IMP22-001` |
| `baseline/expectedResult/unknown` | `missing-input` |
| `current/id` | `SNAP-IMP22-009-current` |
| `current/evidenceId` | `EVD-IMP22-M009-current` |
| `current/dataSourceId` | `SYNDS-IMP22-009` |
| `current/origin` | `authored-supplied-values-not-measured` |
| `current/subjectId` | `SYNTH-IMP22-001` |
| `current/subjectRevision` | `INPUT-REV-002` |
| `current/populationRevision` | `POP-REV-001` |
| `current/windowStart` | `2026-09-01T09:00:00Z` |
| `current/windowEnd` | `2026-09-01T09:10:00Z` |
| `current/availableAt` | `2026-09-01T09:10:30Z` |
| `current/selectedMembers` | `[]` |
| `current/samples` | `[]` |
| `current/missingMembers/0` | `AUTHORITY-IMP22-001` |
| `current/expectedResult/unknown` | `missing-input` |

### MET-IMP22-010

| Field | Value |
|---|---|
| `id` | `MET-IMP22-010` |
| `type` | `Process` |
| `decisionPurpose` | `判断目的を失った活動件数の指標を廃止する理由を記録する。` |
| `definition` | `供給された活動記録の件数。数を増やすだけの誘因を点検する旧指標。` |
| `formula` | `count` |
| `unit` | `件` |
| `populationId` | `POP-IMP22-010` |
| `populationRevision` | `POP-REV-001` |
| `populationMembers/0` | `ACTIVITY-IMP22-001` |
| `populationMembers/1` | `ACTIVITY-IMP22-002` |
| `populationMembers/2` | `ACTIVITY-IMP22-003` |
| `populationMembers/3` | `ACTIVITY-IMP22-004` |
| `populationMembers/4` | `ACTIVITY-IMP22-005` |
| `populationMembers/5` | `ACTIVITY-IMP22-006` |
| `populationMembers/6` | `ACTIVITY-IMP22-007` |
| `populationMembers/7` | `ACTIVITY-IMP22-008` |
| `populationBasis` | `author-selected-finite-teaching-members-not-real-organization` |
| `exclusionReason` | `この著者定義の母集団外は未評価。改善のための事後除外はしない。` |
| `windowStart` | `2026-09-01T09:00:00Z` |
| `windowEnd` | `2026-09-01T09:10:00Z` |
| `cutoff` | `2026-09-01T09:11:00Z` |
| `qualityCriterion` | `供給入力の有無と既知の不一致を区別し、根拠不足をゼロへ置換しない。` |
| `target` | `指標をRetiredとし、重要行動とQualityの問いへ戻る。` |
| `confidence` | `この供給値の計算は再現可能。実効果の確信度は未評価。` |
| `limitation` | `実測、実組織の分布、因果効果、未選択範囲は評価していない。` |
| `retirementTrigger` | `判断目的の消失、重複、Gaming、Dataの継続取得不能、より適切な代替の出現。` |
| `reassessmentId` | `REA-IMP22-008` |
| `baseline/id` | `SNAP-IMP22-010-baseline` |
| `baseline/evidenceId` | `EVD-IMP22-M010-baseline` |
| `baseline/dataSourceId` | `SYNDS-IMP22-010` |
| `baseline/origin` | `authored-supplied-values-not-measured` |
| `baseline/subjectId` | `SYNTH-IMP22-001` |
| `baseline/subjectRevision` | `INPUT-REV-001` |
| `baseline/populationRevision` | `POP-REV-001` |
| `baseline/windowStart` | `2026-09-01T09:00:00Z` |
| `baseline/windowEnd` | `2026-09-01T09:10:00Z` |
| `baseline/availableAt` | `2026-09-01T09:10:30Z` |
| `baseline/selectedMembers/0` | `ACTIVITY-IMP22-001` |
| `baseline/selectedMembers/1` | `ACTIVITY-IMP22-002` |
| `baseline/selectedMembers/2` | `ACTIVITY-IMP22-003` |
| `baseline/selectedMembers/3` | `ACTIVITY-IMP22-004` |
| `baseline/samples` | `[]` |
| `baseline/missingMembers` | `[]` |
| `baseline/expectedResult/count` | `4` |
| `current/id` | `SNAP-IMP22-010-current` |
| `current/evidenceId` | `EVD-IMP22-M010-current` |
| `current/dataSourceId` | `SYNDS-IMP22-010` |
| `current/origin` | `authored-supplied-values-not-measured` |
| `current/subjectId` | `SYNTH-IMP22-001` |
| `current/subjectRevision` | `INPUT-REV-002` |
| `current/populationRevision` | `POP-REV-001` |
| `current/windowStart` | `2026-09-01T09:00:00Z` |
| `current/windowEnd` | `2026-09-01T09:10:00Z` |
| `current/availableAt` | `2026-09-01T09:10:30Z` |
| `current/selectedMembers/0` | `ACTIVITY-IMP22-001` |
| `current/selectedMembers/1` | `ACTIVITY-IMP22-002` |
| `current/selectedMembers/2` | `ACTIVITY-IMP22-003` |
| `current/selectedMembers/3` | `ACTIVITY-IMP22-004` |
| `current/selectedMembers/4` | `ACTIVITY-IMP22-005` |
| `current/selectedMembers/5` | `ACTIVITY-IMP22-006` |
| `current/selectedMembers/6` | `ACTIVITY-IMP22-007` |
| `current/selectedMembers/7` | `ACTIVITY-IMP22-008` |
| `current/samples` | `[]` |
| `current/missingMembers` | `[]` |
| `current/expectedResult/count` | `8` |

### BLI-IMP22-001

| Field | Value |
|---|---|
| `id` | `BLI-IMP22-001` |
| `caseId` | `CASE-IMP-2026-001` |
| `refines/0` | `CASE-2026-001` |
| `refines/1` | `CASE-DET-2026-001` |
| `riskObjectiveId` | `ROBJ-IMP22-001` |
| `findingId` | `FND-IMP22-001` |
| `gapId` | `GAP-IMP22-001` |
| `controlId` | `CTL-IMP22-001` |
| `metricIds/0` | `MET-IMP22-001` |
| `metricIds/1` | `MET-IMP22-002` |
| `debt` | `Detection` |
| `status` | `Proposed` |
| `priority/label` | `供給案を比較` |
| `priority/reason` | `重要行動の未検証が残り、Rule追加を先に成功と数えられない。` |
| `priority/automaticScore` | `false` |
| `priority/cost` | `教材の定性的な負荷想定だけ。実費用は未見積り。` |
| `dependencyIds` | `[]` |
| `action/id` | `ACT-IMP22-001` |
| `action/owner` | `SYN-IMP22-OWNER-001` |
| `action/dueAt` | `2026-09-30T00:00:00Z` |
| `action/proposal` | `五行動の母集団と三つの未検証条件を固定し、必要Evidenceを列挙する案。` |
| `action/acceptance` | `Rule件数とは別に各行動の正常・異常比較と未検証理由を示す。` |
| `action/executionAuthorized` | `false` |
| `action/actualExecuted` | `false` |
| `evidenceIds/0` | `EVD-IMP22-M001-baseline` |
| `evidenceIds/1` | `EVD-IMP22-M001-current` |
| `evidenceIds/2` | `EVD-IMP22-M002-baseline` |
| `evidenceIds/3` | `EVD-IMP22-M002-current` |
| `verification/id` | `null` |
| `verification/evidenceId` | `null` |
| `verification/itemId` | `BLI-IMP22-001` |
| `verification/metricIds/0` | `MET-IMP22-001` |
| `verification/metricIds/1` | `MET-IMP22-002` |
| `verification/sourceEvidenceIds` | `[]` |
| `verification/subjectId` | `SYNTH-IMP22-001` |
| `verification/subjectRevision` | `INPUT-REV-002` |
| `verification/windowStart` | `2026-09-01T09:00:00Z` |
| `verification/windowEnd` | `2026-09-01T09:10:00Z` |
| `verification/cutoff` | `2026-09-01T09:11:00Z` |
| `verification/recordedAt` | `null` |
| `verification/method` | `finite-supplied-comparison` |
| `verification/result` | `not-verified` |
| `verification/realEffectivenessVerified` | `false` |
| `decision/id` | `DEC-IMP22-001` |
| `decision/owner` | `SYN-IMP22-DECISION-OWNER` |
| `decision/basis` | `重要行動の未検証が残り、Rule追加を先に成功と数えられない。` |
| `decision/recordedAt` | `2026-09-26T00:00:00Z` |
| `decision/executionAuthorized` | `false` |
| `riskJudgment/claim` | `Rule件数とは別に各行動の正常・異常比較と未検証理由を示す。` |
| `riskJudgment/confidence` | `供給記録の限定解釈。実効果は未評価。` |
| `riskJudgment/alternative` | `実環境では母集団、観測条件、運用、権限が供給設定と異なる可能性。` |
| `riskJudgment/gap` | `実影響、実効果、未選択範囲は未測定。` |
| `riskJudgment/invalidation` | `対象版・母集団・定義・Data source・入力品質・権限条件の変更。` |
| `riskJudgment/realRiskReductionMeasured` | `false` |
| `riskJudgment/riskZero` | `false` |
| `residualRisk/id` | `RES-IMP22-001` |
| `residualRisk/owner` | `SYN-IMP22-RISK-OWNER` |
| `residualRisk/description` | `供給範囲外と実影響は未知のままであり、無条件の安全とは言えない。` |
| `acceptance/present` | `false` |
| `acceptance/id` | `null` |
| `acceptance/owner` | `null` |
| `acceptance/scope` | `null` |
| `acceptance/authorityReference` | `null` |
| `acceptance/decidedAt` | `null` |
| `acceptance/expiresAt` | `null` |
| `acceptance/overridesExecutionAuthority` | `false` |
| `retirement/present` | `false` |
| `retirement/reason` | `null` |
| `retirement/replacementMetricIds` | `[]` |
| `retirement/historyRetained` | `true` |
| `reassessment/id` | `REA-IMP22-001` |
| `reassessment/owner` | `SYN-IMP22-OWNER-001` |
| `reassessment/dueAt` | `2026-09-30T00:00:00Z` |
| `reassessment/trigger` | `対象版・母集団・Schema・Source・品質・依存・権限・受容期限・指標目的の変更。` |
| `workRecord/stage` | `plan-proposed` |
| `workRecord/recordedAt` | `2026-09-26T00:00:00Z` |
| `workRecord/note` | `計画案だけ。検証は未実施。` |
| `workRecord/actualOperation` | `false` |

### BLI-IMP22-002

| Field | Value |
|---|---|
| `id` | `BLI-IMP22-002` |
| `caseId` | `CASE-IMP-2026-001` |
| `refines/0` | `CASE-2026-001` |
| `refines/1` | `CASE-DET-2026-001` |
| `riskObjectiveId` | `ROBJ-IMP22-002` |
| `findingId` | `FND-IMP22-002` |
| `gapId` | `GAP-IMP22-002` |
| `controlId` | `CTL-IMP22-002` |
| `metricIds/0` | `MET-IMP22-003` |
| `metricIds/1` | `MET-IMP22-004` |
| `debt` | `Detection` |
| `status` | `Approved` |
| `priority/label` | `供給案を比較` |
| `priority/reason` | `対応表の9/10と供給検証の2/10の差を可視化する必要がある。` |
| `priority/automaticScore` | `false` |
| `priority/cost` | `教材の定性的な負荷想定だけ。実費用は未見積り。` |
| `dependencyIds/0` | `BLI-IMP22-001` |
| `action/id` | `ACT-IMP22-002` |
| `action/owner` | `SYN-IMP22-OWNER-002` |
| `action/dueAt` | `2026-09-30T00:00:00Z` |
| `action/proposal` | `対応付けだけの仮説を分け、正常系を伴う供給検証計画を比較する案。` |
| `action/acceptance` | `同じ十仮説でmappingと検証の集合を別々に追跡し、未検証八件を残す。` |
| `action/executionAuthorized` | `false` |
| `action/actualExecuted` | `false` |
| `evidenceIds/0` | `EVD-IMP22-M003-baseline` |
| `evidenceIds/1` | `EVD-IMP22-M003-current` |
| `evidenceIds/2` | `EVD-IMP22-M004-baseline` |
| `evidenceIds/3` | `EVD-IMP22-M004-current` |
| `verification/id` | `null` |
| `verification/evidenceId` | `null` |
| `verification/itemId` | `BLI-IMP22-002` |
| `verification/metricIds/0` | `MET-IMP22-003` |
| `verification/metricIds/1` | `MET-IMP22-004` |
| `verification/sourceEvidenceIds` | `[]` |
| `verification/subjectId` | `SYNTH-IMP22-001` |
| `verification/subjectRevision` | `INPUT-REV-002` |
| `verification/windowStart` | `2026-09-01T09:00:00Z` |
| `verification/windowEnd` | `2026-09-01T09:10:00Z` |
| `verification/cutoff` | `2026-09-01T09:11:00Z` |
| `verification/recordedAt` | `null` |
| `verification/method` | `finite-supplied-comparison` |
| `verification/result` | `not-verified` |
| `verification/realEffectivenessVerified` | `false` |
| `decision/id` | `DEC-IMP22-002` |
| `decision/owner` | `SYN-IMP22-DECISION-OWNER` |
| `decision/basis` | `対応表の9/10と供給検証の2/10の差を可視化する必要がある。` |
| `decision/recordedAt` | `2026-09-26T00:00:00Z` |
| `decision/executionAuthorized` | `false` |
| `riskJudgment/claim` | `同じ十仮説でmappingと検証の集合を別々に追跡し、未検証八件を残す。` |
| `riskJudgment/confidence` | `供給記録の限定解釈。実効果は未評価。` |
| `riskJudgment/alternative` | `実環境では母集団、観測条件、運用、権限が供給設定と異なる可能性。` |
| `riskJudgment/gap` | `実影響、実効果、未選択範囲は未測定。` |
| `riskJudgment/invalidation` | `対象版・母集団・定義・Data source・入力品質・権限条件の変更。` |
| `riskJudgment/realRiskReductionMeasured` | `false` |
| `riskJudgment/riskZero` | `false` |
| `residualRisk/id` | `RES-IMP22-002` |
| `residualRisk/owner` | `SYN-IMP22-RISK-OWNER` |
| `residualRisk/description` | `供給範囲外と実影響は未知のままであり、無条件の安全とは言えない。` |
| `acceptance/present` | `false` |
| `acceptance/id` | `null` |
| `acceptance/owner` | `null` |
| `acceptance/scope` | `null` |
| `acceptance/authorityReference` | `null` |
| `acceptance/decidedAt` | `null` |
| `acceptance/expiresAt` | `null` |
| `acceptance/overridesExecutionAuthority` | `false` |
| `retirement/present` | `false` |
| `retirement/reason` | `null` |
| `retirement/replacementMetricIds` | `[]` |
| `retirement/historyRetained` | `true` |
| `reassessment/id` | `REA-IMP22-002` |
| `reassessment/owner` | `SYN-IMP22-OWNER-002` |
| `reassessment/dueAt` | `2026-09-30T00:00:00Z` |
| `reassessment/trigger` | `対象版・母集団・Schema・Source・品質・依存・権限・受容期限・指標目的の変更。` |
| `workRecord/stage` | `plan-approved` |
| `workRecord/recordedAt` | `2026-09-26T00:00:00Z` |
| `workRecord/note` | `供給計画の条件確認のみ。実操作は承認していない。` |
| `workRecord/actualOperation` | `false` |

### BLI-IMP22-003

| Field | Value |
|---|---|
| `id` | `BLI-IMP22-003` |
| `caseId` | `CASE-IMP-2026-001` |
| `refines/0` | `CASE-2026-001` |
| `refines/1` | `CASE-DET-2026-001` |
| `riskObjectiveId` | `ROBJ-IMP22-003` |
| `findingId` | `FND-IMP22-003` |
| `gapId` | `GAP-IMP22-003` |
| `controlId` | `CTL-IMP22-003` |
| `metricIds/0` | `MET-IMP22-005` |
| `metricIds/1` | `MET-IMP22-006` |
| `debt` | `Evidence` |
| `status` | `In progress` |
| `priority/label` | `条件を先に確認` |
| `priority/reason` | `平均時間短縮と根拠充足の悪化が同時に起きている。` |
| `priority/automaticScore` | `false` |
| `priority/cost` | `教材の定性的な負荷想定だけ。実費用は未見積り。` |
| `dependencyIds` | `[]` |
| `action/id` | `ACT-IMP22-003` |
| `action/owner` | `SYN-IMP22-OWNER-003` |
| `action/dueAt` | `2026-09-30T00:00:00Z` |
| `action/proposal` | `必須Evidenceを失うWorkflowを供給資料上で見直す計画。実担当への通知は行わない。` |
| `action/acceptance` | `時間の三統計量と同じ五判断の品質を併記し、品質低下を時間目標で正当化しない。` |
| `action/executionAuthorized` | `false` |
| `action/actualExecuted` | `false` |
| `evidenceIds/0` | `EVD-IMP22-M005-baseline` |
| `evidenceIds/1` | `EVD-IMP22-M005-current` |
| `evidenceIds/2` | `EVD-IMP22-M006-baseline` |
| `evidenceIds/3` | `EVD-IMP22-M006-current` |
| `verification/id` | `null` |
| `verification/evidenceId` | `null` |
| `verification/itemId` | `BLI-IMP22-003` |
| `verification/metricIds/0` | `MET-IMP22-005` |
| `verification/metricIds/1` | `MET-IMP22-006` |
| `verification/sourceEvidenceIds` | `[]` |
| `verification/subjectId` | `SYNTH-IMP22-001` |
| `verification/subjectRevision` | `INPUT-REV-002` |
| `verification/windowStart` | `2026-09-01T09:00:00Z` |
| `verification/windowEnd` | `2026-09-01T09:10:00Z` |
| `verification/cutoff` | `2026-09-01T09:11:00Z` |
| `verification/recordedAt` | `null` |
| `verification/method` | `finite-supplied-comparison` |
| `verification/result` | `not-verified` |
| `verification/realEffectivenessVerified` | `false` |
| `decision/id` | `DEC-IMP22-003` |
| `decision/owner` | `SYN-IMP22-DECISION-OWNER` |
| `decision/basis` | `平均時間短縮と根拠充足の悪化が同時に起きている。` |
| `decision/recordedAt` | `2026-09-26T00:00:00Z` |
| `decision/executionAuthorized` | `false` |
| `riskJudgment/claim` | `時間の三統計量と同じ五判断の品質を併記し、品質低下を時間目標で正当化しない。` |
| `riskJudgment/confidence` | `供給記録の限定解釈。実効果は未評価。` |
| `riskJudgment/alternative` | `実環境では母集団、観測条件、運用、権限が供給設定と異なる可能性。` |
| `riskJudgment/gap` | `実影響、実効果、未選択範囲は未測定。` |
| `riskJudgment/invalidation` | `対象版・母集団・定義・Data source・入力品質・権限条件の変更。` |
| `riskJudgment/realRiskReductionMeasured` | `false` |
| `riskJudgment/riskZero` | `false` |
| `residualRisk/id` | `RES-IMP22-003` |
| `residualRisk/owner` | `SYN-IMP22-RISK-OWNER` |
| `residualRisk/description` | `供給範囲外と実影響は未知のままであり、無条件の安全とは言えない。` |
| `acceptance/present` | `false` |
| `acceptance/id` | `null` |
| `acceptance/owner` | `null` |
| `acceptance/scope` | `null` |
| `acceptance/authorityReference` | `null` |
| `acceptance/decidedAt` | `null` |
| `acceptance/expiresAt` | `null` |
| `acceptance/overridesExecutionAuthority` | `false` |
| `retirement/present` | `false` |
| `retirement/reason` | `null` |
| `retirement/replacementMetricIds` | `[]` |
| `retirement/historyRetained` | `true` |
| `reassessment/id` | `REA-IMP22-003` |
| `reassessment/owner` | `SYN-IMP22-OWNER-003` |
| `reassessment/dueAt` | `2026-09-30T00:00:00Z` |
| `reassessment/trigger` | `対象版・母集団・Schema・Source・品質・依存・権限・受容期限・指標目的の変更。` |
| `workRecord/stage` | `record-draft-in-progress` |
| `workRecord/recordedAt` | `2026-09-26T00:00:00Z` |
| `workRecord/note` | `供給Workflowの検討用記録が作成途中。品質条件は未充足。` |
| `workRecord/actualOperation` | `false` |

### BLI-IMP22-004

| Field | Value |
|---|---|
| `id` | `BLI-IMP22-004` |
| `caseId` | `CASE-IMP-2026-001` |
| `refines/0` | `CASE-2026-001` |
| `refines/1` | `CASE-DET-2026-001` |
| `riskObjectiveId` | `ROBJ-IMP22-004` |
| `findingId` | `FND-IMP22-004` |
| `gapId` | `GAP-IMP22-004` |
| `controlId` | `CTL-IMP22-004` |
| `metricIds/0` | `MET-IMP22-007` |
| `debt` | `Telemetry` |
| `status` | `Verified` |
| `priority/label` | `供給案を比較` |
| `priority/reason` | `同じ供給Huntの条件差を比較し、結論保留が残る一件も追跡する。` |
| `priority/automaticScore` | `false` |
| `priority/cost` | `教材の定性的な負荷想定だけ。実費用は未見積り。` |
| `dependencyIds` | `[]` |
| `action/id` | `ACT-IMP22-004` |
| `action/owner` | `SYN-IMP22-OWNER-004` |
| `action/dueAt` | `2026-09-30T00:00:00Z` |
| `action/proposal` | `十件の供給HuntでTelemetry条件とInconclusiveの前後を比較する。実Collectorは操作しない。` |
| `action/acceptance` | `同じ十件で4/10と1/10を照合し、未確定一件と親Huntの未変更を保持する。` |
| `action/executionAuthorized` | `false` |
| `action/actualExecuted` | `false` |
| `evidenceIds/0` | `EVD-IMP22-M007-baseline` |
| `evidenceIds/1` | `EVD-IMP22-M007-current` |
| `verification/id` | `VAL-IMP22-004` |
| `verification/evidenceId` | `EVD-IMP22-V004` |
| `verification/itemId` | `BLI-IMP22-004` |
| `verification/metricIds/0` | `MET-IMP22-007` |
| `verification/sourceEvidenceIds/0` | `EVD-IMP22-M007-baseline` |
| `verification/sourceEvidenceIds/1` | `EVD-IMP22-M007-current` |
| `verification/subjectId` | `SYNTH-IMP22-001` |
| `verification/subjectRevision` | `INPUT-REV-002` |
| `verification/windowStart` | `2026-09-01T09:00:00Z` |
| `verification/windowEnd` | `2026-09-01T09:10:00Z` |
| `verification/cutoff` | `2026-09-01T09:11:00Z` |
| `verification/recordedAt` | `2026-09-26T00:00:00Z` |
| `verification/method` | `finite-supplied-comparison` |
| `verification/result` | `bounded-supplied-match` |
| `verification/realEffectivenessVerified` | `false` |
| `decision/id` | `DEC-IMP22-004` |
| `decision/owner` | `SYN-IMP22-DECISION-OWNER` |
| `decision/basis` | `同じ供給Huntの条件差を比較し、結論保留が残る一件も追跡する。` |
| `decision/recordedAt` | `2026-09-26T00:00:00Z` |
| `decision/executionAuthorized` | `false` |
| `riskJudgment/claim` | `同じ十件で4/10と1/10を照合し、未確定一件と親Huntの未変更を保持する。` |
| `riskJudgment/confidence` | `供給記録の限定解釈。実効果は未評価。` |
| `riskJudgment/alternative` | `実環境では母集団、観測条件、運用、権限が供給設定と異なる可能性。` |
| `riskJudgment/gap` | `実影響、実効果、未選択範囲は未測定。` |
| `riskJudgment/invalidation` | `対象版・母集団・定義・Data source・入力品質・権限条件の変更。` |
| `riskJudgment/realRiskReductionMeasured` | `false` |
| `riskJudgment/riskZero` | `false` |
| `residualRisk/id` | `RES-IMP22-004` |
| `residualRisk/owner` | `SYN-IMP22-RISK-OWNER` |
| `residualRisk/description` | `供給範囲外と実影響は未知のままであり、無条件の安全とは言えない。` |
| `acceptance/present` | `false` |
| `acceptance/id` | `null` |
| `acceptance/owner` | `null` |
| `acceptance/scope` | `null` |
| `acceptance/authorityReference` | `null` |
| `acceptance/decidedAt` | `null` |
| `acceptance/expiresAt` | `null` |
| `acceptance/overridesExecutionAuthority` | `false` |
| `retirement/present` | `false` |
| `retirement/reason` | `null` |
| `retirement/replacementMetricIds` | `[]` |
| `retirement/historyRetained` | `true` |
| `reassessment/id` | `REA-IMP22-004` |
| `reassessment/owner` | `SYN-IMP22-OWNER-004` |
| `reassessment/dueAt` | `2026-09-30T00:00:00Z` |
| `reassessment/trigger` | `対象版・母集団・Schema・Source・品質・依存・権限・受容期限・指標目的の変更。` |
| `workRecord/stage` | `supplied-comparison-complete` |
| `workRecord/recordedAt` | `2026-09-26T00:00:00Z` |
| `workRecord/note` | `供給Huntの前後照合記録がそろった。実Collectorや親Huntは未変更。` |
| `workRecord/actualOperation` | `false` |

### BLI-IMP22-005

| Field | Value |
|---|---|
| `id` | `BLI-IMP22-005` |
| `caseId` | `CASE-IMP-2026-001` |
| `refines/0` | `CASE-2026-001` |
| `refines/1` | `CASE-DET-2026-001` |
| `riskObjectiveId` | `ROBJ-IMP22-005` |
| `findingId` | `FND-IMP22-005` |
| `gapId` | `GAP-IMP22-005` |
| `controlId` | `CTL-IMP22-005` |
| `metricIds/0` | `MET-IMP22-008` |
| `debt` | `Detection` |
| `status` | `Verified` |
| `priority/label` | `供給案を比較` |
| `priority/reason` | `供給Rule版の差を正常・Near-miss対比を失わず再確認する。` |
| `priority/automaticScore` | `false` |
| `priority/cost` | `教材の定性的な負荷想定だけ。実費用は未見積り。` |
| `dependencyIds` | `[]` |
| `action/id` | `ACT-IMP22-005` |
| `action/owner` | `SYN-IMP22-OWNER-005` |
| `action/dueAt` | `2026-09-30T00:00:00Z` |
| `action/proposal` | `親21の003と010を方法参照として照合し、旧Failedと供給新版の一致を両方残す。` |
| `action/acceptance` | `同一対象・Batch・時間条件で三出力を比較し、2/3から3/3の限定差だけを支持する。` |
| `action/executionAuthorized` | `false` |
| `action/actualExecuted` | `false` |
| `evidenceIds/0` | `EVD-IMP22-M008-baseline` |
| `evidenceIds/1` | `EVD-IMP22-M008-current` |
| `verification/id` | `VAL-IMP22-005` |
| `verification/evidenceId` | `EVD-IMP22-V005` |
| `verification/itemId` | `BLI-IMP22-005` |
| `verification/metricIds/0` | `MET-IMP22-008` |
| `verification/sourceEvidenceIds/0` | `EVD-IMP22-M008-baseline` |
| `verification/sourceEvidenceIds/1` | `EVD-IMP22-M008-current` |
| `verification/subjectId` | `SYNTH-IMP22-001` |
| `verification/subjectRevision` | `INPUT-REV-002` |
| `verification/windowStart` | `2026-09-01T09:00:00Z` |
| `verification/windowEnd` | `2026-09-01T09:10:00Z` |
| `verification/cutoff` | `2026-09-01T09:11:00Z` |
| `verification/recordedAt` | `2026-09-26T00:00:00Z` |
| `verification/method` | `finite-supplied-comparison` |
| `verification/result` | `bounded-supplied-match` |
| `verification/realEffectivenessVerified` | `false` |
| `decision/id` | `DEC-IMP22-005` |
| `decision/owner` | `SYN-IMP22-DECISION-OWNER` |
| `decision/basis` | `供給Rule版の差を正常・Near-miss対比を失わず再確認する。` |
| `decision/recordedAt` | `2026-09-26T00:00:00Z` |
| `decision/executionAuthorized` | `false` |
| `riskJudgment/claim` | `同一対象・Batch・時間条件で三出力を比較し、2/3から3/3の限定差だけを支持する。` |
| `riskJudgment/confidence` | `供給記録の限定解釈。実効果は未評価。` |
| `riskJudgment/alternative` | `実環境では母集団、観測条件、運用、権限が供給設定と異なる可能性。` |
| `riskJudgment/gap` | `実影響、実効果、未選択範囲は未測定。` |
| `riskJudgment/invalidation` | `対象版・母集団・定義・Data source・入力品質・権限条件の変更。` |
| `riskJudgment/realRiskReductionMeasured` | `false` |
| `riskJudgment/riskZero` | `false` |
| `residualRisk/id` | `RES-IMP22-005` |
| `residualRisk/owner` | `SYN-IMP22-RISK-OWNER` |
| `residualRisk/description` | `供給範囲外と実影響は未知のままであり、無条件の安全とは言えない。` |
| `acceptance/present` | `false` |
| `acceptance/id` | `null` |
| `acceptance/owner` | `null` |
| `acceptance/scope` | `null` |
| `acceptance/authorityReference` | `null` |
| `acceptance/decidedAt` | `null` |
| `acceptance/expiresAt` | `null` |
| `acceptance/overridesExecutionAuthority` | `false` |
| `retirement/present` | `false` |
| `retirement/reason` | `null` |
| `retirement/replacementMetricIds` | `[]` |
| `retirement/historyRetained` | `true` |
| `reassessment/id` | `REA-IMP22-005` |
| `reassessment/owner` | `SYN-IMP22-OWNER-005` |
| `reassessment/dueAt` | `2026-09-30T00:00:00Z` |
| `reassessment/trigger` | `対象版・母集団・Schema・Source・品質・依存・権限・受容期限・指標目的の変更。` |
| `workRecord/stage` | `supplied-comparison-complete` |
| `workRecord/recordedAt` | `2026-09-26T00:00:00Z` |
| `workRecord/note` | `親21の供給Retestを照合した記録だけ。親Actionを実施済みにしない。` |
| `workRecord/actualOperation` | `false` |

### BLI-IMP22-006

| Field | Value |
|---|---|
| `id` | `BLI-IMP22-006` |
| `caseId` | `CASE-IMP-2026-001` |
| `refines/0` | `CASE-2026-001` |
| `refines/1` | `CASE-DET-2026-001` |
| `riskObjectiveId` | `ROBJ-IMP22-006` |
| `findingId` | `FND-IMP22-006` |
| `gapId` | `GAP-IMP22-006` |
| `controlId` | `CTL-IMP22-006` |
| `metricIds/0` | `MET-IMP22-009` |
| `debt` | `Authority` |
| `status` | `Blocked` |
| `priority/label` | `条件を先に確認` |
| `priority/reason` | `権限根拠不足は、品質や件数の良さで補えない。` |
| `priority/automaticScore` | `false` |
| `priority/cost` | `教材の定性的な負荷想定だけ。実費用は未見積り。` |
| `dependencyIds` | `[]` |
| `action/id` | `ACT-IMP22-006` |
| `action/owner` | `SYN-IMP22-OWNER-006` |
| `action/dueAt` | `2026-09-30T00:00:00Z` |
| `action/proposal` | `必要な権限根拠と判断主体を資料上で明示する案。根拠不足の間は停止を保持する。` |
| `action/acceptance` | `供給不足をunknownとBlockedで残し、親の期限切れ権限やDraft RoEを実許可に変えない。` |
| `action/executionAuthorized` | `false` |
| `action/actualExecuted` | `false` |
| `evidenceIds/0` | `EVD-IMP22-M009-baseline` |
| `evidenceIds/1` | `EVD-IMP22-M009-current` |
| `verification/id` | `null` |
| `verification/evidenceId` | `null` |
| `verification/itemId` | `BLI-IMP22-006` |
| `verification/metricIds/0` | `MET-IMP22-009` |
| `verification/sourceEvidenceIds` | `[]` |
| `verification/subjectId` | `SYNTH-IMP22-001` |
| `verification/subjectRevision` | `INPUT-REV-002` |
| `verification/windowStart` | `2026-09-01T09:00:00Z` |
| `verification/windowEnd` | `2026-09-01T09:10:00Z` |
| `verification/cutoff` | `2026-09-01T09:11:00Z` |
| `verification/recordedAt` | `null` |
| `verification/method` | `finite-supplied-comparison` |
| `verification/result` | `not-verified` |
| `verification/realEffectivenessVerified` | `false` |
| `decision/id` | `DEC-IMP22-006` |
| `decision/owner` | `SYN-IMP22-DECISION-OWNER` |
| `decision/basis` | `権限根拠不足は、品質や件数の良さで補えない。` |
| `decision/recordedAt` | `2026-09-26T00:00:00Z` |
| `decision/executionAuthorized` | `false` |
| `riskJudgment/claim` | `供給不足をunknownとBlockedで残し、親の期限切れ権限やDraft RoEを実許可に変えない。` |
| `riskJudgment/confidence` | `供給記録の限定解釈。実効果は未評価。` |
| `riskJudgment/alternative` | `実環境では母集団、観測条件、運用、権限が供給設定と異なる可能性。` |
| `riskJudgment/gap` | `実影響、実効果、未選択範囲は未測定。` |
| `riskJudgment/invalidation` | `対象版・母集団・定義・Data source・入力品質・権限条件の変更。` |
| `riskJudgment/realRiskReductionMeasured` | `false` |
| `riskJudgment/riskZero` | `false` |
| `residualRisk/id` | `RES-IMP22-006` |
| `residualRisk/owner` | `SYN-IMP22-RISK-OWNER` |
| `residualRisk/description` | `供給範囲外と実影響は未知のままであり、無条件の安全とは言えない。` |
| `acceptance/present` | `false` |
| `acceptance/id` | `null` |
| `acceptance/owner` | `null` |
| `acceptance/scope` | `null` |
| `acceptance/authorityReference` | `null` |
| `acceptance/decidedAt` | `null` |
| `acceptance/expiresAt` | `null` |
| `acceptance/overridesExecutionAuthority` | `false` |
| `retirement/present` | `false` |
| `retirement/reason` | `null` |
| `retirement/replacementMetricIds` | `[]` |
| `retirement/historyRetained` | `true` |
| `reassessment/id` | `REA-IMP22-006` |
| `reassessment/owner` | `SYN-IMP22-OWNER-006` |
| `reassessment/dueAt` | `2026-09-30T00:00:00Z` |
| `reassessment/trigger` | `対象版・母集団・Schema・Source・品質・依存・権限・受容期限・指標目的の変更。` |
| `workRecord/stage` | `blocked` |
| `workRecord/recordedAt` | `2026-09-26T00:00:00Z` |
| `workRecord/note` | `供給権限根拠が不足し、後続の実操作は0。` |
| `workRecord/actualOperation` | `false` |

### BLI-IMP22-007

| Field | Value |
|---|---|
| `id` | `BLI-IMP22-007` |
| `caseId` | `CASE-IMP-2026-001` |
| `refines/0` | `CASE-2026-001` |
| `refines/1` | `CASE-DET-2026-001` |
| `riskObjectiveId` | `ROBJ-IMP22-007` |
| `findingId` | `FND-IMP22-007` |
| `gapId` | `GAP-IMP22-007` |
| `controlId` | `CTL-IMP22-007` |
| `metricIds/0` | `MET-IMP22-002` |
| `debt` | `Evidence` |
| `status` | `Accepted` |
| `priority/label` | `供給案を比較` |
| `priority/reason` | `未検証範囲の知識不足を、実Riskゼロとせず期限付きの供給判断へ残す。` |
| `priority/automaticScore` | `false` |
| `priority/cost` | `教材の定性的な負荷想定だけ。実費用は未見積り。` |
| `dependencyIds` | `[]` |
| `action/id` | `ACT-IMP22-007` |
| `action/owner` | `SYN-IMP22-OWNER-007` |
| `action/dueAt` | `2026-09-30T00:00:00Z` |
| `action/proposal` | `限定した供給計画の残存不確実性を、Risk ownerと期限付きで再評価する案。` |
| `action/acceptance` | `受容の範囲・理由・担当・期限・再評価を残す。実操作許可や検証成功にはしない。` |
| `action/executionAuthorized` | `false` |
| `action/actualExecuted` | `false` |
| `evidenceIds/0` | `EVD-IMP22-M002-baseline` |
| `evidenceIds/1` | `EVD-IMP22-M002-current` |
| `verification/id` | `null` |
| `verification/evidenceId` | `null` |
| `verification/itemId` | `BLI-IMP22-007` |
| `verification/metricIds/0` | `MET-IMP22-002` |
| `verification/sourceEvidenceIds` | `[]` |
| `verification/subjectId` | `SYNTH-IMP22-001` |
| `verification/subjectRevision` | `INPUT-REV-002` |
| `verification/windowStart` | `2026-09-01T09:00:00Z` |
| `verification/windowEnd` | `2026-09-01T09:10:00Z` |
| `verification/cutoff` | `2026-09-01T09:11:00Z` |
| `verification/recordedAt` | `null` |
| `verification/method` | `finite-supplied-comparison` |
| `verification/result` | `not-verified` |
| `verification/realEffectivenessVerified` | `false` |
| `decision/id` | `DEC-IMP22-007` |
| `decision/owner` | `SYN-IMP22-DECISION-OWNER` |
| `decision/basis` | `未検証範囲の知識不足を、実Riskゼロとせず期限付きの供給判断へ残す。` |
| `decision/recordedAt` | `2026-09-26T00:00:00Z` |
| `decision/executionAuthorized` | `false` |
| `riskJudgment/claim` | `受容の範囲・理由・担当・期限・再評価を残す。実操作許可や検証成功にはしない。` |
| `riskJudgment/confidence` | `供給記録の限定解釈。実効果は未評価。` |
| `riskJudgment/alternative` | `実環境では母集団、観測条件、運用、権限が供給設定と異なる可能性。` |
| `riskJudgment/gap` | `実影響、実効果、未選択範囲は未測定。` |
| `riskJudgment/invalidation` | `対象版・母集団・定義・Data source・入力品質・権限条件の変更。` |
| `riskJudgment/realRiskReductionMeasured` | `false` |
| `riskJudgment/riskZero` | `false` |
| `residualRisk/id` | `RES-IMP22-007` |
| `residualRisk/owner` | `SYN-IMP22-RISK-OWNER` |
| `residualRisk/description` | `供給範囲外と実影響は未知のままであり、無条件の安全とは言えない。` |
| `acceptance/present` | `true` |
| `acceptance/id` | `ACC-IMP22-007` |
| `acceptance/owner` | `SYN-IMP22-RISK-OWNER` |
| `acceptance/scope` | `この供給計画の未検証範囲に関する知識不足だけ。実事業Riskや実作業の許可ではない。` |
| `acceptance/authorityReference` | `SYN-RISK-MANDATE-IMP22` |
| `acceptance/decidedAt` | `2026-09-26T00:00:00Z` |
| `acceptance/expiresAt` | `2026-10-01T00:00:00Z` |
| `acceptance/overridesExecutionAuthority` | `false` |
| `retirement/present` | `false` |
| `retirement/reason` | `null` |
| `retirement/replacementMetricIds` | `[]` |
| `retirement/historyRetained` | `true` |
| `reassessment/id` | `REA-IMP22-007` |
| `reassessment/owner` | `SYN-IMP22-OWNER-007` |
| `reassessment/dueAt` | `2026-09-30T00:00:00Z` |
| `reassessment/trigger` | `対象版・母集団・Schema・Source・品質・依存・権限・受容期限・指標目的の変更。` |
| `workRecord/stage` | `risk-decision-recorded` |
| `workRecord/recordedAt` | `2026-09-26T00:00:00Z` |
| `workRecord/note` | `知識不足を残す供給判断のみ。修正や検証の完了ではない。` |
| `workRecord/actualOperation` | `false` |

### BLI-IMP22-008

| Field | Value |
|---|---|
| `id` | `BLI-IMP22-008` |
| `caseId` | `CASE-IMP-2026-001` |
| `refines/0` | `CASE-2026-001` |
| `refines/1` | `CASE-DET-2026-001` |
| `riskObjectiveId` | `ROBJ-IMP22-008` |
| `findingId` | `FND-IMP22-008` |
| `gapId` | `GAP-IMP22-008` |
| `controlId` | `CTL-IMP22-008` |
| `metricIds/0` | `MET-IMP22-010` |
| `debt` | `Evidence` |
| `status` | `Retired` |
| `priority/label` | `供給案を比較` |
| `priority/reason` | `活動件数だけを増やす指標は現在の判断目的を失っている。` |
| `priority/automaticScore` | `false` |
| `priority/cost` | `教材の定性的な負荷想定だけ。実費用は未見積り。` |
| `dependencyIds` | `[]` |
| `action/id` | `ACT-IMP22-008` |
| `action/owner` | `SYN-IMP22-OWNER-008` |
| `action/dueAt` | `2026-09-30T00:00:00Z` |
| `action/proposal` | `旧活動件数の定義と値を保持して廃止し、重要行動と根拠品質の問いへ置き換える。` |
| `action/acceptance` | `旧値を削除せず、廃止理由とMET-IMP22-002/006への代替参照を残す。` |
| `action/executionAuthorized` | `false` |
| `action/actualExecuted` | `false` |
| `evidenceIds/0` | `EVD-IMP22-M010-baseline` |
| `evidenceIds/1` | `EVD-IMP22-M010-current` |
| `verification/id` | `null` |
| `verification/evidenceId` | `null` |
| `verification/itemId` | `BLI-IMP22-008` |
| `verification/metricIds/0` | `MET-IMP22-010` |
| `verification/sourceEvidenceIds` | `[]` |
| `verification/subjectId` | `SYNTH-IMP22-001` |
| `verification/subjectRevision` | `INPUT-REV-002` |
| `verification/windowStart` | `2026-09-01T09:00:00Z` |
| `verification/windowEnd` | `2026-09-01T09:10:00Z` |
| `verification/cutoff` | `2026-09-01T09:11:00Z` |
| `verification/recordedAt` | `null` |
| `verification/method` | `finite-supplied-comparison` |
| `verification/result` | `not-verified` |
| `verification/realEffectivenessVerified` | `false` |
| `decision/id` | `DEC-IMP22-008` |
| `decision/owner` | `SYN-IMP22-DECISION-OWNER` |
| `decision/basis` | `活動件数だけを増やす指標は現在の判断目的を失っている。` |
| `decision/recordedAt` | `2026-09-26T00:00:00Z` |
| `decision/executionAuthorized` | `false` |
| `riskJudgment/claim` | `旧値を削除せず、廃止理由とMET-IMP22-002/006への代替参照を残す。` |
| `riskJudgment/confidence` | `供給記録の限定解釈。実効果は未評価。` |
| `riskJudgment/alternative` | `実環境では母集団、観測条件、運用、権限が供給設定と異なる可能性。` |
| `riskJudgment/gap` | `実影響、実効果、未選択範囲は未測定。` |
| `riskJudgment/invalidation` | `対象版・母集団・定義・Data source・入力品質・権限条件の変更。` |
| `riskJudgment/realRiskReductionMeasured` | `false` |
| `riskJudgment/riskZero` | `false` |
| `residualRisk/id` | `RES-IMP22-008` |
| `residualRisk/owner` | `SYN-IMP22-RISK-OWNER` |
| `residualRisk/description` | `供給範囲外と実影響は未知のままであり、無条件の安全とは言えない。` |
| `acceptance/present` | `false` |
| `acceptance/id` | `null` |
| `acceptance/owner` | `null` |
| `acceptance/scope` | `null` |
| `acceptance/authorityReference` | `null` |
| `acceptance/decidedAt` | `null` |
| `acceptance/expiresAt` | `null` |
| `acceptance/overridesExecutionAuthority` | `false` |
| `retirement/present` | `true` |
| `retirement/reason` | `活動件数だけの目標が判断目的を失い、Gamingを招く。旧記録を保持する。` |
| `retirement/replacementMetricIds/0` | `MET-IMP22-002` |
| `retirement/replacementMetricIds/1` | `MET-IMP22-006` |
| `retirement/historyRetained` | `true` |
| `reassessment/id` | `REA-IMP22-008` |
| `reassessment/owner` | `SYN-IMP22-OWNER-008` |
| `reassessment/dueAt` | `2026-09-30T00:00:00Z` |
| `reassessment/trigger` | `対象版・母集団・Schema・Source・品質・依存・権限・受容期限・指標目的の変更。` |
| `workRecord/stage` | `metric-retired-in-record` |
| `workRecord/recordedAt` | `2026-09-26T00:00:00Z` |
| `workRecord/note` | `指標の役割終了を記録した。旧値と根拠は削除していない。` |
| `workRecord/actualOperation` | `false` |

### handoff

| Field | Value |
|---|---|
| `id` | `HOF-IMP22-26` |
| `targetChapter` | `26` |
| `itemIds/0` | `BLI-IMP22-001` |
| `itemIds/1` | `BLI-IMP22-002` |
| `itemIds/2` | `BLI-IMP22-003` |
| `itemIds/3` | `BLI-IMP22-004` |
| `itemIds/4` | `BLI-IMP22-005` |
| `itemIds/5` | `BLI-IMP22-006` |
| `itemIds/6` | `BLI-IMP22-007` |
| `itemIds/7` | `BLI-IMP22-008` |
| `status` | `planned-not-delivered` |
| `receiptId` | `null` |
| `owner` | `SYN-IMP22-DECISION-OWNER` |
| `dueAt` | `2026-09-30T00:00:00Z` |
| `executionAuthorized` | `false` |
| `purpose` | `選択肢、費用仮定、依存、根拠と限界を比較する計画。実受領や判断を認定しない。` |

### safety

| Field | Value |
|---|---|
| `purpose` | `完全合成記録の計算と改善判断を学ぶ。` |
| `prerequisite` | `章内の定義と親章の方法参照のみ。` |
| `authorityAndScope` | `供給記録の読解とローカルCopyだけ。実操作の許可は含まない。` |
| `expectedEvidence` | `分母、統計量、品質、IDの照合と限界を記した解答。` |
| `impact` | `解答Copyのみ。親正本・実設定・実担当を変更しない。` |
| `stop` | `実Data混入、意味・品質・範囲・権限不明で停止し、外部接続や追加実操作をしない。` |
| `cleanup` | `解答Copyの整理計画と残存確認。実Runtimeは作っていない。` |
| `individualMonitoring` | `false` |
| `publicRanking` | `false` |
| `punitiveKpi` | `false` |


## 安全な分析と終了条件

Purposeは判断目的、分母、入力品質、状態の根拠を確認することである。Prerequisiteは本章の表と供給JSONだけで、外部環境を用意しない。Authority / Scopeは教材の読解とローカルCopyの計算に限る。Expected evidenceは五つの対比、IDの対応、未知の範囲を記した解答である。

Impactは解答Copyだけに限定し、正本・親Case・実設定を変更しない。実Data混入、範囲・権限・意味・品質が不明なら停止し、追加の実操作や外部接続をしない。個人監視、公開Ranking、懲罰KPIへの転用は禁止する。

Cleanupは解答Copyの整理計画と残存確認である。Runtimeを作っていないため、実環境の復旧完了とは主張しない。第26章へのHOF-IMP22-26は予定だけで、Receiptはnullのまま残す。
