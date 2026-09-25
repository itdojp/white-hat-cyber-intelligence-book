# 第21章 Control Validation Plan完全合成記入例

[第21章](../manuscript/21-purple-team-validation.md)と[ART-27](../templates/control-validation-plan.md)の全欄を、[供給JSON](fixtures/ch21-control-validation.json) / [Schema](../schemas/ch21-control-validation.schema.json)へ対応付ける。以下は著者が作成した条件であり、実Controlの測定結果ではない。

## 読み方と境界

CVP-2026-021-001 / CASE-CV-2026-001はCASE-DET-2026-001をrefinesする。新対象SYNTH-CV21-001 / REV-CV21-001は親の対象と別であり、親17の三fixtureを再収集した記録ではない。親14の失効Authority/Draft RoE、親16/17/19/20のEvidenceと状態、親20の原因未確定を保持する。HOF-DFIR20-21は未配達/Receipt null/実権限falseのままである。

五Controlは防止・到達・検知・判定文脈・保留判断の問いに対応する。Atomicは指定した一層だけ、End-to-Endの008は五層を比較する。未選択の層はPassedでも評価済みでもない。供給された時刻は教材内の順序を表す仮定であり、実Clockの精度を測定した記録ではない。

rootのexecutionAuthorizedはfalse、実操作・収集・通知・Deploy・Incident宣言は0である。suppliedAuthorityのtrueも実許可ではない。Stoppedの005にあるrecordedAtは停止条件を記述した供給Recordの時点であり、Response実施時刻ではない。payloadSha256はJSON表現の比較だけで真正性や権限を証明しない。

## 層別の供給結果

この表はJSON内に独立して記述した期待値を示す。Criterionの観測値から計算する結果と一致する必要があり、期待値を変更して成功に合わせてはならない。

| Scenario | Layer | Result | Failure |
|---|---|---|---|
| SCN-CV21-001 | Prevention | Passed | なし |
| SCN-CV21-002 | Telemetry | Failed | Telemetry |
| SCN-CV21-003 | Detection | Failed | Detection logic |
| SCN-CV21-004 | Triage | Partial | Workflow |
| SCN-CV21-005 | Response | Stopped | Authority |
| SCN-CV21-006 | Detection | Indeterminate | Test design |
| SCN-CV21-007 | Prevention | Failed | Control |
| SCN-CV21-008 | Prevention | Passed | なし |
| SCN-CV21-008 | Telemetry | Passed | なし |
| SCN-CV21-008 | Detection | Passed | なし |
| SCN-CV21-008 | Triage | Passed | なし |
| SCN-CV21-008 | Response | Passed | なし |
| SCN-CV21-009 | Telemetry | Partial | Telemetry |
| SCN-CV21-010 | Detection | Passed | なし |

001/002は同じBatchの防止と配送を切り分ける。002のFailedは単なる検索0件ではなく、生成記録と配送失敗を示す供給条件に基づく。003のPositive不一致と006のPositive入力不足も別の問題である。004/009は観測された部分充足であり、nullの言い換えではない。

## Retestと未配達

RT-CV21-003はSCN-CV21-003からSCN-CV21-010への供給比較である。CTLREV-CV21-001とCTLREV-CV21-002を分け、対象・問い・Batch・正常・Near-missの比較条件を保持する。旧Evidenceを新IDへ付け替えず、003のFailedを残す。版名と供給出力の違いは実Ruleの修正・Deploy・測定を示さない。

すべてのActionはproposed-not-executedであり、担当・期限・受入基準・Retest・Reassessmentを持つ。第22章向けHOF-CV21-22はplanned-not-delivered、Receipt null、executionAuthorized=falseである。新しいSource、対象、入力、権限または期待値が必要になれば、旧判断を保持して再評価する。

## 全欄の読み方

以下のFieldはJSONの全leafへ対応する。controlsは期待する目的と条件、scenariosのobservationsは供給されたActual、expectedLayersは独立した教材期待値である。gapとimprovementは不足と次の判断を結ぶ。空配列はその欄に項目がないことを表し、未選択層や実環境に問題がないとは意味しない。

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
| `id` | `CVP-2026-021-001` |
| `caseId` | `CASE-CV-2026-001` |
| `parentCaseId` | `CASE-DET-2026-001` |
| `relation` | `refines` |
| `artifactId` | `ART-27` |
| `asOf` | `2026-09-25T00:00:00Z` |
| `sourceIds/0` | `SRC-ATTACK-001` |
| `sourceIds/1` | `SRC-ATTACK-DET-001` |
| `sourceIds/2` | `SRC-NIST-ASSESS-001` |
| `sourceIds/3` | `SRC-IR-001` |
| `authoring` | `synthetic-authored-not-measured` |
| `actualOperations` | `0` |
| `actualCollections` | `0` |
| `actualNotifications` | `0` |
| `actualDeployments` | `0` |
| `actualIncidentDeclarations` | `0` |

### parentReferences

| Field | Value |
|---|---|
| `use` | `method-reference-only` |
| `decisionRequirementId` | `DR-DET-2026-001` |
| `threatHypothesisId` | `TH-DET-2026-001` |
| `detectionRecordId` | `DVR-2026-017-001` |
| `detectionId` | `DET-2026-017-001` |
| `telemetryIds/0` | `TEL-DET-2026-001` |
| `telemetryIds/1` | `TEL-DET-2026-002` |
| `telemetryIds/2` | `TEL-DET-2026-003` |
| `minimalValidationId` | `MIV-2026-014` |
| `telemetryMapId` | `TCM-2026-016` |
| `incidentPlanId` | `IAP-2026-019-001` |
| `dfirRecordId` | `DFIR-2026-020-001` |
| `dfirRcaId` | `RCA-DFIR20-B` |
| `dfirControlId` | `CTL-DFIR20-001` |
| `dfirControlStatus` | `hypothesis-only` |
| `dfirHandoffId` | `HOF-DFIR20-21` |
| `dfirHandoffStatus` | `planned-not-delivered` |
| `receiptId` | `null` |
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

### threat

| Field | Value |
|---|---|
| `behavior` | `業務上未承認のscope追加という親17の仮説を方法参照する。` |
| `attackTechniqueId` | `T1098` |
| `attackVersion` | `19.2` |
| `mappingBasis` | `parent17-method-reference` |
| `coverageProof` | `false` |
| `actorAttribution` | `not-assessed` |

### roles

| Field | Value |
|---|---|
| `validationOwner` | `SYN-CV-VALIDATION-OWNER` |
| `evidenceReviewer` | `SYN-CV-EVIDENCE-REVIEWER` |
| `residualReviewer` | `SYN-CV-RESIDUAL-REVIEWER` |

### CTL-CV21-001

| Field | Value |
|---|---|
| `id` | `CTL-CV21-001` |
| `objectiveId` | `OBJ-CV21-001` |
| `layer` | `Prevention` |
| `owner` | `SYN-CV-CONTROL-OWNER` |
| `objective` | `未承認の追加scopeを拒否する。` |
| `criteria/0/id` | `CRIT-CV21-01-01` |
| `criteria/0/field` | `scope-outcome` |
| `criteria/0/expected` | `blocked` |
| `criteria/0/partialValues` | `[]` |

### CTL-CV21-002

| Field | Value |
|---|---|
| `id` | `CTL-CV21-002` |
| `objectiveId` | `OBJ-CV21-002` |
| `layer` | `Telemetry` |
| `owner` | `SYN-CV-TELEMETRY-OWNER` |
| `objective` | `必要な供給監査が対象Window内でConsumerへ届く。` |
| `criteria/0/id` | `CRIT-CV21-02-01` |
| `criteria/0/field` | `signal-coverage` |
| `criteria/0/expected` | `all-required` |
| `criteria/0/partialValues/0` | `primary-only` |

### CTL-CV21-003

| Field | Value |
|---|---|
| `id` | `CTL-CV21-003` |
| `objectiveId` | `OBJ-CV21-003` |
| `layer` | `Detection` |
| `owner` | `SYN-CV-DETECTION-OWNER` |
| `objective` | `Positiveを検知し正常とBenign-near-missを誤検知しない。` |
| `criteria/0/id` | `CRIT-CV21-03-01` |
| `criteria/0/field` | `positive` |
| `criteria/0/expected` | `alert` |
| `criteria/0/partialValues` | `[]` |
| `criteria/1/id` | `CRIT-CV21-03-02` |
| `criteria/1/field` | `negative` |
| `criteria/1/expected` | `no-alert` |
| `criteria/1/partialValues` | `[]` |
| `criteria/2/id` | `CRIT-CV21-03-03` |
| `criteria/2/field` | `benign-near-miss` |
| `criteria/2/expected` | `no-alert` |
| `criteria/2/partialValues` | `[]` |

### CTL-CV21-004

| Field | Value |
|---|---|
| `id` | `CTL-CV21-004` |
| `objectiveId` | `OBJ-CV21-004` |
| `layer` | `Triage` |
| `owner` | `SYN-CV-TRIAGE-OWNER` |
| `objective` | `Evidence、Owner、理由を含む供給判定を作る。` |
| `criteria/0/id` | `CRIT-CV21-04-01` |
| `criteria/0/field` | `context` |
| `criteria/0/expected` | `evidence-owner-reason` |
| `criteria/0/partialValues/0` | `evidence-only` |

### CTL-CV21-005

| Field | Value |
|---|---|
| `id` | `CTL-CV21-005` |
| `objectiveId` | `OBJ-CV21-005` |
| `layer` | `Response` |
| `owner` | `SYN-CV-RESPONSE-OWNER` |
| `objective` | `与えられた権限と保留判断を記録する。実封じ込めを実施しない。` |
| `criteria/0/id` | `CRIT-CV21-05-01` |
| `criteria/0/field` | `decision` |
| `criteria/0/expected` | `hold-with-owner` |
| `criteria/0/partialValues` | `[]` |

### SCN-CV21-001

| Field | Value |
|---|---|
| `id` | `SCN-CV21-001` |
| `type` | `Atomic` |
| `layers/0` | `Prevention` |
| `traceId` | `TRACE-CV21-001` |
| `batchId` | `BATCH-CV21-PAIR` |
| `subjectId` | `SYNTH-CV21-001` |
| `subjectRevision` | `REV-CV21-001` |
| `controlRevision` | `CTLREV-CV21-001` |
| `windowStart` | `2026-09-01T09:00:00Z` |
| `windowEnd` | `2026-09-01T09:10:00Z` |
| `cutoff` | `2026-09-01T09:11:00Z` |
| `analysisAt` | `2026-09-01T09:12:00Z` |
| `mode` | `supplied-record-comparison` |
| `suppliedAuthority` | `true` |
| `stopReason` | `null` |
| `stepsAfterStop` | `0` |
| `observations/0/id` | `EVD-CV21-001-01` |
| `observations/0/payload/scenarioId` | `SCN-CV21-001` |
| `observations/0/payload/subjectId` | `SYNTH-CV21-001` |
| `observations/0/payload/subjectRevision` | `REV-CV21-001` |
| `observations/0/payload/traceId` | `TRACE-CV21-001` |
| `observations/0/payload/batchId` | `BATCH-CV21-PAIR` |
| `observations/0/payload/layer` | `Prevention` |
| `observations/0/payload/controlId` | `CTL-CV21-001` |
| `observations/0/payload/controlRevision` | `CTLREV-CV21-001` |
| `observations/0/payload/step` | `1` |
| `observations/0/payload/recordedAt` | `2026-09-01T09:01:00Z` |
| `observations/0/payload/availableAt` | `2026-09-01T09:01:30Z` |
| `observations/0/payload/values/scope-outcome` | `blocked` |
| `observations/0/payload/present/scope-outcome` | `true` |
| `observations/0/payload/inputBasis` | `complete-supplied-input` |
| `observations/0/payload/transportBasis` | `not-a-transport-claim` |
| `observations/0/payloadSha256` | `24798ca6201165c9deccc700c3534fd840d8f3086818c0863725ec1a7d7ce819` |
| `expectedLayers/0/layer` | `Prevention` |
| `expectedLayers/0/result` | `Passed` |
| `expectedLayers/0/failureClasses` | `[]` |
| `note` | `同じ供給Batchで防止成功と観測不足を分離する。` |
| `gap/id` | `GAP-CV21-001` |
| `gap/affectedLayers` | `[]` |
| `gap/description` | `供給された対象・版・Windowだけの比較であり、実有効性と未選択層は未評価。` |
| `gap/nextActionId` | `ACT-CV21-001` |
| `improvement/id` | `ACT-CV21-001` |
| `improvement/status` | `proposed-not-executed` |
| `improvement/owner` | `SYN-CV-CONTROL-OWNER` |
| `improvement/dueAt` | `2026-09-30T00:00:00Z` |
| `improvement/action` | `blockedとallowedの対比条件を保持し、防止の問いを変えず再評価する計画。` |
| `improvement/retestId` | `RT-CV21-001` |
| `improvement/acceptance` | `対象・版を固定したscope-outcomeの期待値blockedと反証allowedを保持する。監査到達は別に評価する。` |
| `improvement/reassessmentId` | `REA-CV21-001` |
| `improvement/trigger` | `入力Schema、対象、Rule版、権限条件、Sourceまたは期待値の変更` |
| `permittedConclusion` | `供給記録の限定した層別結果だけ。全Controlの有効性、侵害なし、実操作許可は認定しない。` |

### SCN-CV21-002

| Field | Value |
|---|---|
| `id` | `SCN-CV21-002` |
| `type` | `Atomic` |
| `layers/0` | `Telemetry` |
| `traceId` | `TRACE-CV21-002` |
| `batchId` | `BATCH-CV21-PAIR` |
| `subjectId` | `SYNTH-CV21-001` |
| `subjectRevision` | `REV-CV21-001` |
| `controlRevision` | `CTLREV-CV21-001` |
| `windowStart` | `2026-09-01T09:00:00Z` |
| `windowEnd` | `2026-09-01T09:10:00Z` |
| `cutoff` | `2026-09-01T09:11:00Z` |
| `analysisAt` | `2026-09-01T09:12:00Z` |
| `mode` | `supplied-record-comparison` |
| `suppliedAuthority` | `true` |
| `stopReason` | `null` |
| `stepsAfterStop` | `0` |
| `observations/0/id` | `EVD-CV21-002-01` |
| `observations/0/payload/scenarioId` | `SCN-CV21-002` |
| `observations/0/payload/subjectId` | `SYNTH-CV21-001` |
| `observations/0/payload/subjectRevision` | `REV-CV21-001` |
| `observations/0/payload/traceId` | `TRACE-CV21-002` |
| `observations/0/payload/batchId` | `BATCH-CV21-PAIR` |
| `observations/0/payload/layer` | `Telemetry` |
| `observations/0/payload/controlId` | `CTL-CV21-002` |
| `observations/0/payload/controlRevision` | `CTLREV-CV21-001` |
| `observations/0/payload/step` | `1` |
| `observations/0/payload/recordedAt` | `2026-09-01T09:01:00Z` |
| `observations/0/payload/availableAt` | `2026-09-01T09:01:30Z` |
| `observations/0/payload/values/signal-coverage` | `missing-confirmed` |
| `observations/0/payload/present/signal-coverage` | `true` |
| `observations/0/payload/inputBasis` | `complete-supplied-input` |
| `observations/0/payload/transportBasis` | `produced-and-confirmed-loss` |
| `observations/0/payloadSha256` | `5ca808114c7d74dd24a64e67611016368666fa14b434e11f215c8a8dc4b5f714` |
| `expectedLayers/0/layer` | `Telemetry` |
| `expectedLayers/0/result` | `Failed` |
| `expectedLayers/0/failureClasses/0` | `Telemetry` |
| `note` | `生成記録と供給された配送失敗根拠があり、期待した監査は届かない。` |
| `gap/id` | `GAP-CV21-002` |
| `gap/affectedLayers/0` | `Telemetry` |
| `gap/description` | `生成記録と供給された配送失敗根拠があり、期待した監査は届かない。` |
| `gap/nextActionId` | `ACT-CV21-002` |
| `improvement/id` | `ACT-CV21-002` |
| `improvement/status` | `proposed-not-executed` |
| `improvement/owner` | `SYN-CV-TELEMETRY-OWNER` |
| `improvement/dueAt` | `2026-09-30T00:00:00Z` |
| `improvement/action` | `生成記録からConsumerまでの配送失敗箇所と必要channelを供給資料上で照合する計画。実Logは追加収集しない。` |
| `improvement/retestId` | `RT-CV21-002` |
| `improvement/acceptance` | `produced-and-confirmed-lossの根拠を保持し、新供給版でsignal-coverageがall-requiredかを比較する。` |
| `improvement/reassessmentId` | `REA-CV21-002` |
| `improvement/trigger` | `入力Schema、対象、Rule版、権限条件、Sourceまたは期待値の変更` |
| `permittedConclusion` | `供給記録の限定した層別結果だけ。全Controlの有効性、侵害なし、実操作許可は認定しない。` |

### SCN-CV21-003

| Field | Value |
|---|---|
| `id` | `SCN-CV21-003` |
| `type` | `Atomic` |
| `layers/0` | `Detection` |
| `traceId` | `TRACE-CV21-003` |
| `batchId` | `BATCH-CV21-DETECTION` |
| `subjectId` | `SYNTH-CV21-001` |
| `subjectRevision` | `REV-CV21-001` |
| `controlRevision` | `CTLREV-CV21-001` |
| `windowStart` | `2026-09-01T09:00:00Z` |
| `windowEnd` | `2026-09-01T09:10:00Z` |
| `cutoff` | `2026-09-01T09:11:00Z` |
| `analysisAt` | `2026-09-01T09:12:00Z` |
| `mode` | `supplied-record-comparison` |
| `suppliedAuthority` | `true` |
| `stopReason` | `null` |
| `stepsAfterStop` | `0` |
| `observations/0/id` | `EVD-CV21-003-01` |
| `observations/0/payload/scenarioId` | `SCN-CV21-003` |
| `observations/0/payload/subjectId` | `SYNTH-CV21-001` |
| `observations/0/payload/subjectRevision` | `REV-CV21-001` |
| `observations/0/payload/traceId` | `TRACE-CV21-003` |
| `observations/0/payload/batchId` | `BATCH-CV21-DETECTION` |
| `observations/0/payload/layer` | `Detection` |
| `observations/0/payload/controlId` | `CTL-CV21-003` |
| `observations/0/payload/controlRevision` | `CTLREV-CV21-001` |
| `observations/0/payload/step` | `1` |
| `observations/0/payload/recordedAt` | `2026-09-01T09:01:00Z` |
| `observations/0/payload/availableAt` | `2026-09-01T09:01:30Z` |
| `observations/0/payload/values/positive` | `no-alert` |
| `observations/0/payload/values/negative` | `no-alert` |
| `observations/0/payload/values/benign-near-miss` | `no-alert` |
| `observations/0/payload/present/positive` | `true` |
| `observations/0/payload/present/negative` | `true` |
| `observations/0/payload/present/benign-near-miss` | `true` |
| `observations/0/payload/inputBasis` | `complete-supplied-input` |
| `observations/0/payload/transportBasis` | `not-a-transport-claim` |
| `observations/0/payloadSha256` | `c2212873cf5db70e833715d9d04386e2d27cf4e1bd10c44174e8895c4eec650f` |
| `expectedLayers/0/layer` | `Detection` |
| `expectedLayers/0/result` | `Failed` |
| `expectedLayers/0/failureClasses/0` | `Detection logic` |
| `note` | `三種入力の存在は確認したがPositiveのAlertが出ないという供給記録。` |
| `gap/id` | `GAP-CV21-003` |
| `gap/affectedLayers/0` | `Detection` |
| `gap/description` | `三種入力の存在は確認したがPositiveのAlertが出ないという供給記録。` |
| `gap/nextActionId` | `ACT-CV21-003` |
| `improvement/id` | `ACT-CV21-003` |
| `improvement/status` | `proposed-not-executed` |
| `improvement/owner` | `SYN-CV-DETECTION-OWNER` |
| `improvement/dueAt` | `2026-09-30T00:00:00Z` |
| `improvement/action` | `Positiveの入力条件と供給Rule出力の差を切り分け、正常とNear-missを残して再比較する計画。実Ruleは変更しない。` |
| `improvement/retestId` | `RT-CV21-003` |
| `improvement/acceptance` | `RT-CV21-003でpositive=alert、negativeとbenign-near-miss=no-alertを同一対象・Batch・入力条件で比較する。` |
| `improvement/reassessmentId` | `REA-CV21-003` |
| `improvement/trigger` | `入力Schema、対象、Rule版、権限条件、Sourceまたは期待値の変更` |
| `permittedConclusion` | `供給記録の限定した層別結果だけ。全Controlの有効性、侵害なし、実操作許可は認定しない。` |

### SCN-CV21-004

| Field | Value |
|---|---|
| `id` | `SCN-CV21-004` |
| `type` | `Atomic` |
| `layers/0` | `Triage` |
| `traceId` | `TRACE-CV21-004` |
| `batchId` | `BATCH-CV21-004` |
| `subjectId` | `SYNTH-CV21-001` |
| `subjectRevision` | `REV-CV21-001` |
| `controlRevision` | `CTLREV-CV21-001` |
| `windowStart` | `2026-09-01T09:00:00Z` |
| `windowEnd` | `2026-09-01T09:10:00Z` |
| `cutoff` | `2026-09-01T09:11:00Z` |
| `analysisAt` | `2026-09-01T09:12:00Z` |
| `mode` | `supplied-record-comparison` |
| `suppliedAuthority` | `true` |
| `stopReason` | `null` |
| `stepsAfterStop` | `0` |
| `observations/0/id` | `EVD-CV21-004-01` |
| `observations/0/payload/scenarioId` | `SCN-CV21-004` |
| `observations/0/payload/subjectId` | `SYNTH-CV21-001` |
| `observations/0/payload/subjectRevision` | `REV-CV21-001` |
| `observations/0/payload/traceId` | `TRACE-CV21-004` |
| `observations/0/payload/batchId` | `BATCH-CV21-004` |
| `observations/0/payload/layer` | `Triage` |
| `observations/0/payload/controlId` | `CTL-CV21-004` |
| `observations/0/payload/controlRevision` | `CTLREV-CV21-001` |
| `observations/0/payload/step` | `1` |
| `observations/0/payload/recordedAt` | `2026-09-01T09:01:00Z` |
| `observations/0/payload/availableAt` | `2026-09-01T09:01:30Z` |
| `observations/0/payload/values/context` | `evidence-only` |
| `observations/0/payload/present/context` | `true` |
| `observations/0/payload/inputBasis` | `complete-supplied-input` |
| `observations/0/payload/transportBasis` | `not-a-transport-claim` |
| `observations/0/payloadSha256` | `468352cfcdf838551a443a77c874eccee375140d0ec996b20b323512e355f9aa` |
| `expectedLayers/0/layer` | `Triage` |
| `expectedLayers/0/result` | `Partial` |
| `expectedLayers/0/failureClasses/0` | `Workflow` |
| `note` | `Evidence参照はあるがOwnerと理由が欠けることが記録されている。` |
| `gap/id` | `GAP-CV21-004` |
| `gap/affectedLayers/0` | `Triage` |
| `gap/description` | `Evidence参照はあるがOwnerと理由が欠けることが記録されている。` |
| `gap/nextActionId` | `ACT-CV21-004` |
| `improvement/id` | `ACT-CV21-004` |
| `improvement/status` | `proposed-not-executed` |
| `improvement/owner` | `SYN-CV-TRIAGE-OWNER` |
| `improvement/dueAt` | `2026-09-30T00:00:00Z` |
| `improvement/action` | `不足するOwnerと理由を明示した供給Triage記録を作る計画。実担当への通知は行わない。` |
| `improvement/retestId` | `RT-CV21-004` |
| `improvement/acceptance` | `context=evidence-owner-reasonを根拠IDと照合し、evidence-onlyという旧Partialを残す。` |
| `improvement/reassessmentId` | `REA-CV21-004` |
| `improvement/trigger` | `入力Schema、対象、Rule版、権限条件、Sourceまたは期待値の変更` |
| `permittedConclusion` | `供給記録の限定した層別結果だけ。全Controlの有効性、侵害なし、実操作許可は認定しない。` |

### SCN-CV21-005

| Field | Value |
|---|---|
| `id` | `SCN-CV21-005` |
| `type` | `Atomic` |
| `layers/0` | `Response` |
| `traceId` | `TRACE-CV21-005` |
| `batchId` | `BATCH-CV21-005` |
| `subjectId` | `SYNTH-CV21-001` |
| `subjectRevision` | `REV-CV21-001` |
| `controlRevision` | `CTLREV-CV21-001` |
| `windowStart` | `2026-09-01T09:00:00Z` |
| `windowEnd` | `2026-09-01T09:10:00Z` |
| `cutoff` | `2026-09-01T09:11:00Z` |
| `analysisAt` | `2026-09-01T09:12:00Z` |
| `mode` | `supplied-record-comparison` |
| `suppliedAuthority` | `false` |
| `stopReason` | `authority-gap` |
| `stepsAfterStop` | `0` |
| `observations/0/id` | `EVD-CV21-005-01` |
| `observations/0/payload/scenarioId` | `SCN-CV21-005` |
| `observations/0/payload/subjectId` | `SYNTH-CV21-001` |
| `observations/0/payload/subjectRevision` | `REV-CV21-001` |
| `observations/0/payload/traceId` | `TRACE-CV21-005` |
| `observations/0/payload/batchId` | `BATCH-CV21-005` |
| `observations/0/payload/layer` | `Response` |
| `observations/0/payload/controlId` | `CTL-CV21-005` |
| `observations/0/payload/controlRevision` | `CTLREV-CV21-001` |
| `observations/0/payload/step` | `1` |
| `observations/0/payload/recordedAt` | `2026-09-01T09:01:00Z` |
| `observations/0/payload/availableAt` | `2026-09-01T09:01:30Z` |
| `observations/0/payload/values/decision` | `null` |
| `observations/0/payload/present/decision` | `false` |
| `observations/0/payload/inputBasis` | `authority-not-supplied` |
| `observations/0/payload/transportBasis` | `not-a-transport-claim` |
| `observations/0/payloadSha256` | `034808d8d4e6e9cc40563a1031cf95947dfd85b2c701b6f63196474ab341dbe7` |
| `expectedLayers/0/layer` | `Response` |
| `expectedLayers/0/result` | `Stopped` |
| `expectedLayers/0/failureClasses/0` | `Authority` |
| `note` | `対応案はあるが供給モデルの権限条件が満たされず停止する。` |
| `gap/id` | `GAP-CV21-005` |
| `gap/affectedLayers/0` | `Response` |
| `gap/description` | `対応案はあるが供給モデルの権限条件が満たされず停止する。` |
| `gap/nextActionId` | `ACT-CV21-005` |
| `improvement/id` | `ACT-CV21-005` |
| `improvement/status` | `proposed-not-executed` |
| `improvement/owner` | `SYN-CV-RESPONSE-OWNER` |
| `improvement/dueAt` | `2026-09-30T00:00:00Z` |
| `improvement/action` | `必要な権限根拠と判断主体を読解資料上で確認する計画。根拠がない間はStoppedを維持し、実許可を推定しない。` |
| `improvement/retestId` | `RT-CV21-005` |
| `improvement/acceptance` | `供給権限の不足と停止理由を記録し、後続の比較には別途根拠を必要とする。実行権限falseは変えない。` |
| `improvement/reassessmentId` | `REA-CV21-005` |
| `improvement/trigger` | `入力Schema、対象、Rule版、権限条件、Sourceまたは期待値の変更` |
| `permittedConclusion` | `供給記録の限定した層別結果だけ。全Controlの有効性、侵害なし、実操作許可は認定しない。` |

### SCN-CV21-006

| Field | Value |
|---|---|
| `id` | `SCN-CV21-006` |
| `type` | `Atomic` |
| `layers/0` | `Detection` |
| `traceId` | `TRACE-CV21-006` |
| `batchId` | `BATCH-CV21-006` |
| `subjectId` | `SYNTH-CV21-001` |
| `subjectRevision` | `REV-CV21-001` |
| `controlRevision` | `CTLREV-CV21-001` |
| `windowStart` | `2026-09-01T09:00:00Z` |
| `windowEnd` | `2026-09-01T09:10:00Z` |
| `cutoff` | `2026-09-01T09:11:00Z` |
| `analysisAt` | `2026-09-01T09:12:00Z` |
| `mode` | `supplied-record-comparison` |
| `suppliedAuthority` | `true` |
| `stopReason` | `null` |
| `stepsAfterStop` | `0` |
| `observations/0/id` | `EVD-CV21-006-01` |
| `observations/0/payload/scenarioId` | `SCN-CV21-006` |
| `observations/0/payload/subjectId` | `SYNTH-CV21-001` |
| `observations/0/payload/subjectRevision` | `REV-CV21-001` |
| `observations/0/payload/traceId` | `TRACE-CV21-006` |
| `observations/0/payload/batchId` | `BATCH-CV21-006` |
| `observations/0/payload/layer` | `Detection` |
| `observations/0/payload/controlId` | `CTL-CV21-003` |
| `observations/0/payload/controlRevision` | `CTLREV-CV21-001` |
| `observations/0/payload/step` | `1` |
| `observations/0/payload/recordedAt` | `2026-09-01T09:01:00Z` |
| `observations/0/payload/availableAt` | `2026-09-01T09:01:30Z` |
| `observations/0/payload/values/positive` | `null` |
| `observations/0/payload/values/negative` | `no-alert` |
| `observations/0/payload/values/benign-near-miss` | `no-alert` |
| `observations/0/payload/present/positive` | `false` |
| `observations/0/payload/present/negative` | `true` |
| `observations/0/payload/present/benign-near-miss` | `true` |
| `observations/0/payload/inputBasis` | `fixture-missing` |
| `observations/0/payload/transportBasis` | `not-a-transport-claim` |
| `observations/0/payloadSha256` | `af37a6e86660d71814dde990010d73f96975ea4a16572c951d0473bf5d7e5a7e` |
| `expectedLayers/0/layer` | `Detection` |
| `expectedLayers/0/result` | `Indeterminate` |
| `expectedLayers/0/failureClasses/0` | `Test design` |
| `note` | `Positive fixture自体が不足し、検知失敗かどうかを評価できない。` |
| `gap/id` | `GAP-CV21-006` |
| `gap/affectedLayers/0` | `Detection` |
| `gap/description` | `Positive fixture自体が不足し、検知失敗かどうかを評価できない。` |
| `gap/nextActionId` | `ACT-CV21-006` |
| `improvement/id` | `ACT-CV21-006` |
| `improvement/status` | `proposed-not-executed` |
| `improvement/owner` | `SYN-CV-VALIDATION-OWNER` |
| `improvement/dueAt` | `2026-09-30T00:00:00Z` |
| `improvement/action` | `不足するPositive fixtureの必要Fieldと比較条件を定義し直す計画。欠測を成功へ書き換えず、実Dataは使わない。` |
| `improvement/retestId` | `RT-CV21-006` |
| `improvement/acceptance` | `Positive・Negative・Benign-near-missの入力有無を区別し、足りない間はIndeterminateとNext actionを保持する。` |
| `improvement/reassessmentId` | `REA-CV21-006` |
| `improvement/trigger` | `入力Schema、対象、Rule版、権限条件、Sourceまたは期待値の変更` |
| `permittedConclusion` | `供給記録の限定した層別結果だけ。全Controlの有効性、侵害なし、実操作許可は認定しない。` |

### SCN-CV21-007

| Field | Value |
|---|---|
| `id` | `SCN-CV21-007` |
| `type` | `Atomic` |
| `layers/0` | `Prevention` |
| `traceId` | `TRACE-CV21-007` |
| `batchId` | `BATCH-CV21-007` |
| `subjectId` | `SYNTH-CV21-001` |
| `subjectRevision` | `REV-CV21-001` |
| `controlRevision` | `CTLREV-CV21-001` |
| `windowStart` | `2026-09-01T09:00:00Z` |
| `windowEnd` | `2026-09-01T09:10:00Z` |
| `cutoff` | `2026-09-01T09:11:00Z` |
| `analysisAt` | `2026-09-01T09:12:00Z` |
| `mode` | `supplied-record-comparison` |
| `suppliedAuthority` | `true` |
| `stopReason` | `null` |
| `stepsAfterStop` | `0` |
| `observations/0/id` | `EVD-CV21-007-01` |
| `observations/0/payload/scenarioId` | `SCN-CV21-007` |
| `observations/0/payload/subjectId` | `SYNTH-CV21-001` |
| `observations/0/payload/subjectRevision` | `REV-CV21-001` |
| `observations/0/payload/traceId` | `TRACE-CV21-007` |
| `observations/0/payload/batchId` | `BATCH-CV21-007` |
| `observations/0/payload/layer` | `Prevention` |
| `observations/0/payload/controlId` | `CTL-CV21-001` |
| `observations/0/payload/controlRevision` | `CTLREV-CV21-001` |
| `observations/0/payload/step` | `1` |
| `observations/0/payload/recordedAt` | `2026-09-01T09:01:00Z` |
| `observations/0/payload/availableAt` | `2026-09-01T09:01:30Z` |
| `observations/0/payload/values/scope-outcome` | `allowed` |
| `observations/0/payload/present/scope-outcome` | `true` |
| `observations/0/payload/inputBasis` | `complete-supplied-input` |
| `observations/0/payload/transportBasis` | `not-a-transport-claim` |
| `observations/0/payloadSha256` | `0a49d668ad28f6692851f4090584f14f5daa80e086de8d8125d95cfd543dda13` |
| `expectedLayers/0/layer` | `Prevention` |
| `expectedLayers/0/result` | `Failed` |
| `expectedLayers/0/failureClasses/0` | `Control` |
| `note` | `未承認scopeを許容したという供給記録で、防止の期待と矛盾する。` |
| `gap/id` | `GAP-CV21-007` |
| `gap/affectedLayers/0` | `Prevention` |
| `gap/description` | `未承認scopeを許容したという供給記録で、防止の期待と矛盾する。` |
| `gap/nextActionId` | `ACT-CV21-007` |
| `improvement/id` | `ACT-CV21-007` |
| `improvement/status` | `proposed-not-executed` |
| `improvement/owner` | `SYN-CV-CONTROL-OWNER` |
| `improvement/dueAt` | `2026-09-30T00:00:00Z` |
| `improvement/action` | `未承認scopeをallowedとした供給条件とControl目的の差を調べる計画。実設定は変更しない。` |
| `improvement/retestId` | `RT-CV21-007` |
| `improvement/acceptance` | `同じ問いと対象版でblockedとallowedを比較し、元のFailedを保持する。実有効性へ一般化しない。` |
| `improvement/reassessmentId` | `REA-CV21-007` |
| `improvement/trigger` | `入力Schema、対象、Rule版、権限条件、Sourceまたは期待値の変更` |
| `permittedConclusion` | `供給記録の限定した層別結果だけ。全Controlの有効性、侵害なし、実操作許可は認定しない。` |

### SCN-CV21-008

| Field | Value |
|---|---|
| `id` | `SCN-CV21-008` |
| `type` | `End-to-End` |
| `layers/0` | `Prevention` |
| `layers/1` | `Telemetry` |
| `layers/2` | `Detection` |
| `layers/3` | `Triage` |
| `layers/4` | `Response` |
| `traceId` | `TRACE-CV21-008` |
| `batchId` | `BATCH-CV21-008` |
| `subjectId` | `SYNTH-CV21-001` |
| `subjectRevision` | `REV-CV21-001` |
| `controlRevision` | `CTLREV-CV21-001` |
| `windowStart` | `2026-09-01T09:00:00Z` |
| `windowEnd` | `2026-09-01T09:10:00Z` |
| `cutoff` | `2026-09-01T09:11:00Z` |
| `analysisAt` | `2026-09-01T09:12:00Z` |
| `mode` | `supplied-record-comparison` |
| `suppliedAuthority` | `true` |
| `stopReason` | `null` |
| `stepsAfterStop` | `0` |
| `observations/0/id` | `EVD-CV21-008-01` |
| `observations/0/payload/scenarioId` | `SCN-CV21-008` |
| `observations/0/payload/subjectId` | `SYNTH-CV21-001` |
| `observations/0/payload/subjectRevision` | `REV-CV21-001` |
| `observations/0/payload/traceId` | `TRACE-CV21-008` |
| `observations/0/payload/batchId` | `BATCH-CV21-008` |
| `observations/0/payload/layer` | `Prevention` |
| `observations/0/payload/controlId` | `CTL-CV21-001` |
| `observations/0/payload/controlRevision` | `CTLREV-CV21-001` |
| `observations/0/payload/step` | `1` |
| `observations/0/payload/recordedAt` | `2026-09-01T09:01:00Z` |
| `observations/0/payload/availableAt` | `2026-09-01T09:01:30Z` |
| `observations/0/payload/values/scope-outcome` | `blocked` |
| `observations/0/payload/present/scope-outcome` | `true` |
| `observations/0/payload/inputBasis` | `complete-supplied-input` |
| `observations/0/payload/transportBasis` | `not-a-transport-claim` |
| `observations/0/payloadSha256` | `3d2a20f9483516df9827a4b6427b4a3ac98c9864713b8833e6968f8f5a50407e` |
| `observations/1/id` | `EVD-CV21-008-02` |
| `observations/1/payload/scenarioId` | `SCN-CV21-008` |
| `observations/1/payload/subjectId` | `SYNTH-CV21-001` |
| `observations/1/payload/subjectRevision` | `REV-CV21-001` |
| `observations/1/payload/traceId` | `TRACE-CV21-008` |
| `observations/1/payload/batchId` | `BATCH-CV21-008` |
| `observations/1/payload/layer` | `Telemetry` |
| `observations/1/payload/controlId` | `CTL-CV21-002` |
| `observations/1/payload/controlRevision` | `CTLREV-CV21-001` |
| `observations/1/payload/step` | `2` |
| `observations/1/payload/recordedAt` | `2026-09-01T09:02:00Z` |
| `observations/1/payload/availableAt` | `2026-09-01T09:02:30Z` |
| `observations/1/payload/values/signal-coverage` | `all-required` |
| `observations/1/payload/present/signal-coverage` | `true` |
| `observations/1/payload/inputBasis` | `complete-supplied-input` |
| `observations/1/payload/transportBasis` | `not-a-transport-claim` |
| `observations/1/payloadSha256` | `95fd8a87945acb9aa917d51fbf71cbbab0ca238b7ebb33a86a69e377d7e5dc26` |
| `observations/2/id` | `EVD-CV21-008-03` |
| `observations/2/payload/scenarioId` | `SCN-CV21-008` |
| `observations/2/payload/subjectId` | `SYNTH-CV21-001` |
| `observations/2/payload/subjectRevision` | `REV-CV21-001` |
| `observations/2/payload/traceId` | `TRACE-CV21-008` |
| `observations/2/payload/batchId` | `BATCH-CV21-008` |
| `observations/2/payload/layer` | `Detection` |
| `observations/2/payload/controlId` | `CTL-CV21-003` |
| `observations/2/payload/controlRevision` | `CTLREV-CV21-001` |
| `observations/2/payload/step` | `3` |
| `observations/2/payload/recordedAt` | `2026-09-01T09:03:00Z` |
| `observations/2/payload/availableAt` | `2026-09-01T09:03:30Z` |
| `observations/2/payload/values/positive` | `alert` |
| `observations/2/payload/values/negative` | `no-alert` |
| `observations/2/payload/values/benign-near-miss` | `no-alert` |
| `observations/2/payload/present/positive` | `true` |
| `observations/2/payload/present/negative` | `true` |
| `observations/2/payload/present/benign-near-miss` | `true` |
| `observations/2/payload/inputBasis` | `complete-supplied-input` |
| `observations/2/payload/transportBasis` | `not-a-transport-claim` |
| `observations/2/payloadSha256` | `d2a46936a0749a073dd2f8111db1767ef1c69f09547d408830a51ca2b268726a` |
| `observations/3/id` | `EVD-CV21-008-04` |
| `observations/3/payload/scenarioId` | `SCN-CV21-008` |
| `observations/3/payload/subjectId` | `SYNTH-CV21-001` |
| `observations/3/payload/subjectRevision` | `REV-CV21-001` |
| `observations/3/payload/traceId` | `TRACE-CV21-008` |
| `observations/3/payload/batchId` | `BATCH-CV21-008` |
| `observations/3/payload/layer` | `Triage` |
| `observations/3/payload/controlId` | `CTL-CV21-004` |
| `observations/3/payload/controlRevision` | `CTLREV-CV21-001` |
| `observations/3/payload/step` | `4` |
| `observations/3/payload/recordedAt` | `2026-09-01T09:04:00Z` |
| `observations/3/payload/availableAt` | `2026-09-01T09:04:30Z` |
| `observations/3/payload/values/context` | `evidence-owner-reason` |
| `observations/3/payload/present/context` | `true` |
| `observations/3/payload/inputBasis` | `complete-supplied-input` |
| `observations/3/payload/transportBasis` | `not-a-transport-claim` |
| `observations/3/payloadSha256` | `50f2c76469b54817ae3b45c4d0991a36408649f21610843cbfa519c9fb9b3eb8` |
| `observations/4/id` | `EVD-CV21-008-05` |
| `observations/4/payload/scenarioId` | `SCN-CV21-008` |
| `observations/4/payload/subjectId` | `SYNTH-CV21-001` |
| `observations/4/payload/subjectRevision` | `REV-CV21-001` |
| `observations/4/payload/traceId` | `TRACE-CV21-008` |
| `observations/4/payload/batchId` | `BATCH-CV21-008` |
| `observations/4/payload/layer` | `Response` |
| `observations/4/payload/controlId` | `CTL-CV21-005` |
| `observations/4/payload/controlRevision` | `CTLREV-CV21-001` |
| `observations/4/payload/step` | `5` |
| `observations/4/payload/recordedAt` | `2026-09-01T09:05:00Z` |
| `observations/4/payload/availableAt` | `2026-09-01T09:05:30Z` |
| `observations/4/payload/values/decision` | `hold-with-owner` |
| `observations/4/payload/present/decision` | `true` |
| `observations/4/payload/inputBasis` | `complete-supplied-input` |
| `observations/4/payload/transportBasis` | `not-a-transport-claim` |
| `observations/4/payloadSha256` | `e1671a27b5248698cd54b14c82a046e5fb3a9db3f4d790a94adc5c3c1a3d146c` |
| `expectedLayers/0/layer` | `Prevention` |
| `expectedLayers/0/result` | `Passed` |
| `expectedLayers/0/failureClasses` | `[]` |
| `expectedLayers/1/layer` | `Telemetry` |
| `expectedLayers/1/result` | `Passed` |
| `expectedLayers/1/failureClasses` | `[]` |
| `expectedLayers/2/layer` | `Detection` |
| `expectedLayers/2/result` | `Passed` |
| `expectedLayers/2/failureClasses` | `[]` |
| `expectedLayers/3/layer` | `Triage` |
| `expectedLayers/3/result` | `Passed` |
| `expectedLayers/3/failureClasses` | `[]` |
| `expectedLayers/4/layer` | `Response` |
| `expectedLayers/4/result` | `Passed` |
| `expectedLayers/4/failureClasses` | `[]` |
| `note` | `同一Traceの供給記録を五層で照合する。実攻撃も実IRも行っていない。` |
| `gap/id` | `GAP-CV21-008` |
| `gap/affectedLayers` | `[]` |
| `gap/description` | `供給された対象・版・Windowだけの比較であり、実有効性と未選択層は未評価。` |
| `gap/nextActionId` | `ACT-CV21-008` |
| `improvement/id` | `ACT-CV21-008` |
| `improvement/status` | `proposed-not-executed` |
| `improvement/owner` | `SYN-CV-VALIDATION-OWNER` |
| `improvement/dueAt` | `2026-09-30T00:00:00Z` |
| `improvement/action` | `五層のID・Trace・時刻・比較条件を再評価時にもそろえる計画。別系列の局所成功を寄せ集めない。` |
| `improvement/retestId` | `RT-CV21-008` |
| `improvement/acceptance` | `全五層の供給根拠を独立に照合し、どの層の不足も総合Passedで隠さない。` |
| `improvement/reassessmentId` | `REA-CV21-008` |
| `improvement/trigger` | `入力Schema、対象、Rule版、権限条件、Sourceまたは期待値の変更` |
| `permittedConclusion` | `供給記録の限定した層別結果だけ。全Controlの有効性、侵害なし、実操作許可は認定しない。` |

### SCN-CV21-009

| Field | Value |
|---|---|
| `id` | `SCN-CV21-009` |
| `type` | `Atomic` |
| `layers/0` | `Telemetry` |
| `traceId` | `TRACE-CV21-009` |
| `batchId` | `BATCH-CV21-009` |
| `subjectId` | `SYNTH-CV21-001` |
| `subjectRevision` | `REV-CV21-001` |
| `controlRevision` | `CTLREV-CV21-001` |
| `windowStart` | `2026-09-01T09:00:00Z` |
| `windowEnd` | `2026-09-01T09:10:00Z` |
| `cutoff` | `2026-09-01T09:11:00Z` |
| `analysisAt` | `2026-09-01T09:12:00Z` |
| `mode` | `supplied-record-comparison` |
| `suppliedAuthority` | `true` |
| `stopReason` | `null` |
| `stepsAfterStop` | `0` |
| `observations/0/id` | `EVD-CV21-009-01` |
| `observations/0/payload/scenarioId` | `SCN-CV21-009` |
| `observations/0/payload/subjectId` | `SYNTH-CV21-001` |
| `observations/0/payload/subjectRevision` | `REV-CV21-001` |
| `observations/0/payload/traceId` | `TRACE-CV21-009` |
| `observations/0/payload/batchId` | `BATCH-CV21-009` |
| `observations/0/payload/layer` | `Telemetry` |
| `observations/0/payload/controlId` | `CTL-CV21-002` |
| `observations/0/payload/controlRevision` | `CTLREV-CV21-001` |
| `observations/0/payload/step` | `1` |
| `observations/0/payload/recordedAt` | `2026-09-01T09:01:00Z` |
| `observations/0/payload/availableAt` | `2026-09-01T09:01:30Z` |
| `observations/0/payload/values/signal-coverage` | `primary-only` |
| `observations/0/payload/present/signal-coverage` | `true` |
| `observations/0/payload/inputBasis` | `complete-supplied-input` |
| `observations/0/payload/transportBasis` | `primary-present-secondary-missing` |
| `observations/0/payloadSha256` | `1e0d6834c1ba1e2da1094a7ea83b688139e3b55be61514fb6dffbdef4b6c9a0e` |
| `expectedLayers/0/layer` | `Telemetry` |
| `expectedLayers/0/result` | `Partial` |
| `expectedLayers/0/failureClasses/0` | `Telemetry` |
| `note` | `Primary channelは届くがSecondary channel不足が明示された限定到達。` |
| `gap/id` | `GAP-CV21-009` |
| `gap/affectedLayers/0` | `Telemetry` |
| `gap/description` | `Primary channelは届くがSecondary channel不足が明示された限定到達。` |
| `gap/nextActionId` | `ACT-CV21-009` |
| `improvement/id` | `ACT-CV21-009` |
| `improvement/status` | `proposed-not-executed` |
| `improvement/owner` | `SYN-CV-TELEMETRY-OWNER` |
| `improvement/dueAt` | `2026-09-30T00:00:00Z` |
| `improvement/action` | `Primary到達とSecondary不足を分け、必要channelをそろえる供給検証案を作る。実Collectorは操作しない。` |
| `improvement/retestId` | `RT-CV21-009` |
| `improvement/acceptance` | `primary-onlyという観測Partialを保持し、all-requiredへ変わったと主張する場合は新しい供給根拠を比較する。` |
| `improvement/reassessmentId` | `REA-CV21-009` |
| `improvement/trigger` | `入力Schema、対象、Rule版、権限条件、Sourceまたは期待値の変更` |
| `permittedConclusion` | `供給記録の限定した層別結果だけ。全Controlの有効性、侵害なし、実操作許可は認定しない。` |

### SCN-CV21-010

| Field | Value |
|---|---|
| `id` | `SCN-CV21-010` |
| `type` | `Atomic` |
| `layers/0` | `Detection` |
| `traceId` | `TRACE-CV21-010` |
| `batchId` | `BATCH-CV21-DETECTION` |
| `subjectId` | `SYNTH-CV21-001` |
| `subjectRevision` | `REV-CV21-001` |
| `controlRevision` | `CTLREV-CV21-002` |
| `windowStart` | `2026-09-01T09:00:00Z` |
| `windowEnd` | `2026-09-01T09:10:00Z` |
| `cutoff` | `2026-09-01T09:11:00Z` |
| `analysisAt` | `2026-09-01T09:12:00Z` |
| `mode` | `supplied-record-comparison` |
| `suppliedAuthority` | `true` |
| `stopReason` | `null` |
| `stepsAfterStop` | `0` |
| `observations/0/id` | `EVD-CV21-010-01` |
| `observations/0/payload/scenarioId` | `SCN-CV21-010` |
| `observations/0/payload/subjectId` | `SYNTH-CV21-001` |
| `observations/0/payload/subjectRevision` | `REV-CV21-001` |
| `observations/0/payload/traceId` | `TRACE-CV21-010` |
| `observations/0/payload/batchId` | `BATCH-CV21-DETECTION` |
| `observations/0/payload/layer` | `Detection` |
| `observations/0/payload/controlId` | `CTL-CV21-003` |
| `observations/0/payload/controlRevision` | `CTLREV-CV21-002` |
| `observations/0/payload/step` | `1` |
| `observations/0/payload/recordedAt` | `2026-09-01T09:01:00Z` |
| `observations/0/payload/availableAt` | `2026-09-01T09:01:30Z` |
| `observations/0/payload/values/positive` | `alert` |
| `observations/0/payload/values/negative` | `no-alert` |
| `observations/0/payload/values/benign-near-miss` | `no-alert` |
| `observations/0/payload/present/positive` | `true` |
| `observations/0/payload/present/negative` | `true` |
| `observations/0/payload/present/benign-near-miss` | `true` |
| `observations/0/payload/inputBasis` | `complete-supplied-input` |
| `observations/0/payload/transportBasis` | `not-a-transport-claim` |
| `observations/0/payloadSha256` | `d0aa603dc0eb47a3bbf6b2a4683a98f5ac28e38e5ab3d3c48c68f9f6590ea200` |
| `expectedLayers/0/layer` | `Detection` |
| `expectedLayers/0/result` | `Passed` |
| `expectedLayers/0/failureClasses` | `[]` |
| `note` | `S03と同一条件で供給Rule版だけを変えたRetest。正常とNear-missも残す。` |
| `gap/id` | `GAP-CV21-010` |
| `gap/affectedLayers` | `[]` |
| `gap/description` | `供給された対象・版・Windowだけの比較であり、実有効性と未選択層は未評価。` |
| `gap/nextActionId` | `ACT-CV21-010` |
| `improvement/id` | `ACT-CV21-010` |
| `improvement/status` | `proposed-not-executed` |
| `improvement/owner` | `SYN-CV-DETECTION-OWNER` |
| `improvement/dueAt` | `2026-09-30T00:00:00Z` |
| `improvement/action` | `供給新版の正常・Near-miss対比を継続し、入力Schemaや期待値の変更時に再評価する計画。実Deployは行わない。` |
| `improvement/retestId` | `RT-CV21-010` |
| `improvement/acceptance` | `旧003のFailed、新010の三条件一致と版の差を保持し、追加範囲や実検知率は未評価とする。` |
| `improvement/reassessmentId` | `REA-CV21-010` |
| `improvement/trigger` | `入力Schema、対象、Rule版、権限条件、Sourceまたは期待値の変更` |
| `permittedConclusion` | `供給記録の限定した層別結果だけ。全Controlの有効性、侵害なし、実操作許可は認定しない。` |

### retest

| Field | Value |
|---|---|
| `id` | `RT-CV21-003` |
| `beforeScenarioId` | `SCN-CV21-003` |
| `afterScenarioId` | `SCN-CV21-010` |
| `changedField` | `controlRevision` |
| `beforeRevision` | `CTLREV-CV21-001` |
| `afterRevision` | `CTLREV-CV21-002` |
| `sourceActionId` | `ACT-CV21-003` |
| `result` | `recorded-comparison-only` |
| `beforeRetained` | `true` |
| `actualChangeExecuted` | `false` |
| `limitation` | `供給Rule版名と出力記録の比較であり、Rule実装を変更・Deploy・実測した証明ではない。` |

### handoff

| Field | Value |
|---|---|
| `id` | `HOF-CV21-22` |
| `targetChapter` | `22` |
| `sourcePlanId` | `CVP-2026-021-001` |
| `actionIds/0` | `ACT-CV21-001` |
| `actionIds/1` | `ACT-CV21-002` |
| `actionIds/2` | `ACT-CV21-003` |
| `actionIds/3` | `ACT-CV21-004` |
| `actionIds/4` | `ACT-CV21-005` |
| `actionIds/5` | `ACT-CV21-006` |
| `actionIds/6` | `ACT-CV21-007` |
| `actionIds/7` | `ACT-CV21-008` |
| `actionIds/8` | `ACT-CV21-009` |
| `actionIds/9` | `ACT-CV21-010` |
| `status` | `planned-not-delivered` |
| `receiptId` | `null` |
| `executionAuthorized` | `false` |
| `owner` | `SYN-CV-VALIDATION-OWNER` |
| `dueAt` | `2026-09-30T00:00:00Z` |
| `question` | `層別の失敗・不足・限定結果をOwnerと受入基準付きの改善管理へどう接続するか。` |

### safety

| Field | Value |
|---|---|
| `mode` | `offline-record-only` |
| `stop` | `実Target、実Credential、実Data、外部接続、許可不明の入力が必要なら停止する。` |
| `cleanup` | `配布原本は変えず、自分の解答Copyだけを保持条件に従い整理する。実Runtimeは作らない。` |
| `cleanupDisposition` | `reading-copy-plan-only` |
| `residualCheck` | `実Runtime未作成。実システムの残存影響は測定していない。` |
| `residualDisposition` | `not-measured` |
| `limitations` | `有限な教材比較であり、実証拠の認証、一般的攻撃Emulation、実IR、NIST適合、全組織の安全性は評価しない。` |

## 提出時の確認

問い、Expected/Actual、Criterion ID、対象・版・Trace・Cutoff、層別Result、FailureとGapを指し示す。正常対比、停止後継続0、旧失敗、十Action、Owner、期限、未配達を残す。解答Copyだけを整理し、配布原本や親Evidenceを変更しない。実Runtimeの残存影響は未測定であり、成果物の完成を実Control成功へ置き換えない。
