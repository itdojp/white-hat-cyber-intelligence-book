# 第14章 完全合成記入例：Minimal-Impact Validation Record

## この記入例の扱い

ART-22 / MIV-2026-014はCASE-2026-001をrefinesする非実行の教材です。全ID・観測値・時刻・停止・整理・判断は作成者が記述した供給記録であり、実サービス、実Account、実Data、実操作や実残存影響の測定結果ではありません。

[第14章](../manuscript/14-minimal-impact-validation.md)、[空Template](../templates/minimal-impact-validation-record.md)、[正本JSON](fixtures/ch14-minimal-impact-validation.json)、[閉じたSchema](../schemas/ch14-minimal-impact-validation.schema.json)を参照します。以下はJSONの全末端Fieldと一対一のField/Value表です。添字は0始まりで、空配列も表示します。

## 読み方と対比

最初にparents、context、safetyを読みます。親RoE Draft / executionAuthorized=false、失効AUTH、元Window、三Objectは変えません。第8章のRunningを含む八状態と実行有無、第12章のUnknownとnonFederation三null、第13章のVerifiedと実Build/Deploy/署名検証0を分離します。独立CASE-2026-011のEvidenceや許可を借用しません。

各expectationsは対象Resource IDと監査参照IDという二条件の期待値を持ちます。observationsの合成ID文字列がそれぞれ一致すれば支持、不一致なら反証、present=false/value=nullなら未観測です。空slotにIDがあっても、evidenceIdsには含めません。この比較は実製品の制御や応答を測定するものではありません。

001は二条件支持、002は支持とGap、003は反証とGap、004は二条件反証、005は観測不足です。006はMinimal synthetic operationの計画だけでNot performed / Inconclusive、007は未知入力を表す記号によるStopped、008はSupportedでもResidual UnknownのためOpenです。六Resultと四Methodを全件同じ状態へ揃えません。

Resultは供給された二条件の比較に限定します。停止triggerを最優先し、未実施を別欄へ記録します。Supportedは実影響や安全性ではなく、Completeは記録上の整理・確認が揃った状態です。Gapと制限が記録されていれば005のInconclusiveもCompleteになり得ます。006/007/008はOpenです。

確認事実は供給Field、分析判断はjudgment、仮定は合成対象と時刻、推奨はfindingとdecisionの計画です。実環境との差異や資料不足を代替説明に残し、Hypothesis / Validation / Evidence / Stop / Cleanup / Residual / Finding / Decision / ReassessmentをIDで辿ります。Handoffはplanned-not-deliveredです。

## 停止条件と評価

実Data、未知入力、外部通信、Scope不明なら停止します。実Credentialを再利用しません。横展開、永続化、回避、DoS、破壊は実施しません。全actualOperations=0、stepsAfterStop=0は供給記録の値であり実プロセスの制御ではありません。Cleanup/Residualは今回の読解用作業コピーだけのScopeで、親receiptや正本を整理対象へ付け替えません。

本章の五観点Rubricを使い、十分性と過剰な追加確認、支持と反証、未実施とRejectedを区別します。実Data混入、停止後の追加操作、未確認のResidualからCompleteへの昇格、親許可の改変は点数にかかわらず差し戻します。

## schemaVersion

| Field | Value |
|---|---|
| schemaVersion | 1.0.0 |

## synthetic

| Field | Value |
|---|---|
| synthetic | true |

## executionAuthorized

| Field | Value |
|---|---|
| executionAuthorized | false |

## record

| Field | Value |
|---|---|
| id | MIV-2026-014 |
| artifactId | ART-22 |
| caseId | CASE-2026-001 |
| relation | refines |
| revision | MIV14-REV-001 |
| asOf | 2026-09-16T00:00:00Z |
| authoredNotMeasured | true |
| purpose | 最小限の供給Evidence、停止、未実施、残存確認を区別する。 |

## parents

| Field | Value |
|---|---|
| caseId | CASE-2026-001 |
| relation | refines |
| decisionRequirementId | DR-2026-001 |
| historicalDeadline | 2026-07-22T00:00:00Z |
| authorizationId | AUTH-CASE-2026-001 |
| authorizationExpiresAt | 2026-08-19T09:00:00Z |
| authorizationWindow/0 | 2026-08-06T00:00:00Z |
| authorizationWindow/1 | 2026-08-06T08:00:00Z |
| authorizationConditions/0 | COND-AUTH-2026-001 Open |
| authorizationConditions/1 | COND-AUTH-2026-002 Satisfied |
| authorizationConditions/2 | COND-AUTH-2026-003 Open |
| roeId | ROE-2026-009 |
| roeVersion | 1 |
| roeStatus | Draft |
| roeObjectIds/0 | OBJ-ROE09-CONFIG |
| roeObjectIds/1 | OBJ-ROE09-EVENT |
| roeObjectIds/2 | OBJ-ROE09-POLICY |
| roeExecutionAuthorized | false |
| threatModelId | TM-2026-001 |
| threatModelStatus | Needs Evidence |
| parentReassessmentId | REA-2026-001 |
| independentCaseId | CASE-2026-011 |
| parentStateChanged | false |

## context

| Field | Value |
|---|---|
| assessmentId | PSA-2026-013 |
| parentVerifiedMeaning | authored-summary-comparison-only |
| parentActualBuilds | 0 |
| parentActualDeployments | 0 |
| parentActualSignatureVerifications | 0 |
| identityReviewId | IAR-2026-012 |
| identityBinding | Unknown |
| identityCoverage | Unknown |
| nonFederationAssertion/0 | null |
| nonFederationAssertion/1 | null |
| nonFederationAssertion/2 | null |
| parentPermission | read-customer-summary-not-validation-permission |
| labPlanId | LABPLAN-2026-001 |
| labStates/0 | Planned |
| labStates/1 | Preflight passed |
| labStates/2 | Ready |
| labStates/3 | Running |
| labStates/4 | Stopped |
| labStates/5 | Destroyed |
| labStates/6 | Cleanup verified |
| labStates/7 | Failed closed |
| labRuntimeExecuted | false |
| independentCaseId | CASE-2026-011 |
| independentRoeId | ROE-2026-011 |
| independentUse | comparison-only-not-parent-evidence-or-authorization |
| methods/0 | Static |
| methods/1 | Simulation |
| methods/2 | Offline replay |
| methods/3 | Minimal synthetic operation |
| results/0 | Supported |
| results/1 | Partially supported |
| results/2 | Weakened |
| results/3 | Inconclusive |
| results/4 | Rejected |
| results/5 | Stopped |
| sourceIds/0 | SRC-NIST-TEST-001 |
| sourceIds/1 | SRC-WSTG-001 |

## safety

| Field | Value |
|---|---|
| dataClass | authored-synthetic-only |
| mode | read-only-supplied-records |
| actualOperations | 0 |
| actualNetworkConnections | 0 |
| actualAccountsCreated | 0 |
| realCredentialsPresent | false |
| actualCleanupVerified | false |
| permissionGranted | false |
| impactMeasured | false |
| safeClaim | false |
| limits | 8 supplied records; no service access; no runtime or package execution |
| stop | 実Data、未知の入力、外部通信、Scope不明なら停止する。 |
| cleanup | 自分の読解用作業コピーだけを整理し、親Evidenceと正本を保持する。 |
| notPerformed | 実Dataを取得しない。実Credentialを再利用しない。横展開、永続化、回避、DoS、破壊は実施しない。 |

## expectations EXP-MIV14-001

| Field | Value |
|---|---|
| id | EXP-MIV14-001 |
| validationId | VAL-MIV14-001 |
| subjectId | OBJ-MIV14-001 |
| subjectRevision | SUPPLIED-REV-001 |
| method | Static |
| criterionIds/0 | CRT-MIV14-001-A |
| criterionIds/1 | CRT-MIV14-001-B |
| expectedValues/0 | OBJ-MIV14-001 |
| expectedValues/1 | AUD-MIV14-001 |
| criterionDescriptions/0 | 供給された対象Resource IDが期待した対象と一致する。 |
| criterionDescriptions/1 | 供給された監査参照IDが期待した参照と一致する。 |
| scope | supplied-record-only |

## expectations EXP-MIV14-002

| Field | Value |
|---|---|
| id | EXP-MIV14-002 |
| validationId | VAL-MIV14-002 |
| subjectId | OBJ-MIV14-002 |
| subjectRevision | SUPPLIED-REV-001 |
| method | Simulation |
| criterionIds/0 | CRT-MIV14-002-A |
| criterionIds/1 | CRT-MIV14-002-B |
| expectedValues/0 | OBJ-MIV14-002 |
| expectedValues/1 | AUD-MIV14-002 |
| criterionDescriptions/0 | 供給された対象Resource IDが期待した対象と一致する。 |
| criterionDescriptions/1 | 供給された監査参照IDが期待した参照と一致する。 |
| scope | supplied-record-only |

## expectations EXP-MIV14-003

| Field | Value |
|---|---|
| id | EXP-MIV14-003 |
| validationId | VAL-MIV14-003 |
| subjectId | OBJ-MIV14-003 |
| subjectRevision | SUPPLIED-REV-001 |
| method | Offline replay |
| criterionIds/0 | CRT-MIV14-003-A |
| criterionIds/1 | CRT-MIV14-003-B |
| expectedValues/0 | OBJ-MIV14-003 |
| expectedValues/1 | AUD-MIV14-003 |
| criterionDescriptions/0 | 供給された対象Resource IDが期待した対象と一致する。 |
| criterionDescriptions/1 | 供給された監査参照IDが期待した参照と一致する。 |
| scope | supplied-record-only |

## expectations EXP-MIV14-004

| Field | Value |
|---|---|
| id | EXP-MIV14-004 |
| validationId | VAL-MIV14-004 |
| subjectId | OBJ-MIV14-004 |
| subjectRevision | SUPPLIED-REV-001 |
| method | Offline replay |
| criterionIds/0 | CRT-MIV14-004-A |
| criterionIds/1 | CRT-MIV14-004-B |
| expectedValues/0 | OBJ-MIV14-004 |
| expectedValues/1 | AUD-MIV14-004 |
| criterionDescriptions/0 | 供給された対象Resource IDが期待した対象と一致する。 |
| criterionDescriptions/1 | 供給された監査参照IDが期待した参照と一致する。 |
| scope | supplied-record-only |

## expectations EXP-MIV14-005

| Field | Value |
|---|---|
| id | EXP-MIV14-005 |
| validationId | VAL-MIV14-005 |
| subjectId | OBJ-MIV14-005 |
| subjectRevision | SUPPLIED-REV-001 |
| method | Static |
| criterionIds/0 | CRT-MIV14-005-A |
| criterionIds/1 | CRT-MIV14-005-B |
| expectedValues/0 | OBJ-MIV14-005 |
| expectedValues/1 | AUD-MIV14-005 |
| criterionDescriptions/0 | 供給された対象Resource IDが期待した対象と一致する。 |
| criterionDescriptions/1 | 供給された監査参照IDが期待した参照と一致する。 |
| scope | supplied-record-only |

## expectations EXP-MIV14-006

| Field | Value |
|---|---|
| id | EXP-MIV14-006 |
| validationId | VAL-MIV14-006 |
| subjectId | OBJ-MIV14-006 |
| subjectRevision | SUPPLIED-REV-001 |
| method | Minimal synthetic operation |
| criterionIds/0 | CRT-MIV14-006-A |
| criterionIds/1 | CRT-MIV14-006-B |
| expectedValues/0 | OBJ-MIV14-006 |
| expectedValues/1 | AUD-MIV14-006 |
| criterionDescriptions/0 | 供給された対象Resource IDが期待した対象と一致する。 |
| criterionDescriptions/1 | 供給された監査参照IDが期待した参照と一致する。 |
| scope | supplied-record-only |

## expectations EXP-MIV14-007

| Field | Value |
|---|---|
| id | EXP-MIV14-007 |
| validationId | VAL-MIV14-007 |
| subjectId | OBJ-MIV14-007 |
| subjectRevision | SUPPLIED-REV-001 |
| method | Static |
| criterionIds/0 | CRT-MIV14-007-A |
| criterionIds/1 | CRT-MIV14-007-B |
| expectedValues/0 | OBJ-MIV14-007 |
| expectedValues/1 | AUD-MIV14-007 |
| criterionDescriptions/0 | 供給された対象Resource IDが期待した対象と一致する。 |
| criterionDescriptions/1 | 供給された監査参照IDが期待した参照と一致する。 |
| scope | supplied-record-only |

## expectations EXP-MIV14-008

| Field | Value |
|---|---|
| id | EXP-MIV14-008 |
| validationId | VAL-MIV14-008 |
| subjectId | OBJ-MIV14-008 |
| subjectRevision | SUPPLIED-REV-001 |
| method | Static |
| criterionIds/0 | CRT-MIV14-008-A |
| criterionIds/1 | CRT-MIV14-008-B |
| expectedValues/0 | OBJ-MIV14-008 |
| expectedValues/1 | AUD-MIV14-008 |
| criterionDescriptions/0 | 供給された対象Resource IDが期待した対象と一致する。 |
| criterionDescriptions/1 | 供給された監査参照IDが期待した参照と一致する。 |
| scope | supplied-record-only |

## validations VAL-MIV14-001

| Field | Value |
|---|---|
| id | VAL-MIV14-001 |
| revision | MIV14-REV-001 |
| hypothesisId | HYP-MIV14-001 |
| parentFindingId | FND-PSA13-001 |
| authorityId | AUTH-CASE-2026-001 |
| roeId | ROE-2026-009 |
| labPlanId | LABPLAN-2026-001 |
| decisionQuestion | この供給資料の対象Resource IDと監査参照IDは、期待した二条件それぞれに一致するか。 |
| minimumEvidenceQuestion | この対象ID・版の二条件について供給記録だけで支持と反証を区別できるか。 |
| expectationId | EXP-MIV14-001 |
| method | Static |
| methodRationale | 問いに必要な二条件だけを供給記録で読む。手法名は実行許可ではない。 |
| executionDisposition | Authored review only |
| unperformedReason | 実サービスへの操作は全件実施しない。供給記録の読解だけを表す。 |
| subjectId | OBJ-MIV14-001 |
| subjectRevision | SUPPLIED-REV-001 |
| observations/0/id | EVD-MIV14-001-1 |
| observations/0/criterionId | CRT-MIV14-001-A |
| observations/0/subjectId | OBJ-MIV14-001 |
| observations/0/subjectRevision | SUPPLIED-REV-001 |
| observations/0/present | true |
| observations/0/value | OBJ-MIV14-001 |
| observations/0/recordedAt | 2026-09-15T23:00:00Z |
| observations/0/basis | authored-observation |
| observations/1/id | EVD-MIV14-001-2 |
| observations/1/criterionId | CRT-MIV14-001-B |
| observations/1/subjectId | OBJ-MIV14-001 |
| observations/1/subjectRevision | SUPPLIED-REV-001 |
| observations/1/present | true |
| observations/1/value | AUD-MIV14-001 |
| observations/1/recordedAt | 2026-09-15T23:00:00Z |
| observations/1/basis | authored-observation |
| evidenceIds/0 | EVD-MIV14-001-1 |
| evidenceIds/1 | EVD-MIV14-001-2 |
| minimumEvidenceMet | true |
| declaredReadSteps | 1 |
| stepsAfterStop | 0 |
| actualOperations | 0 |
| stop/id | STP-MIV14-001 |
| stop/trigger | None |
| stop/triggerEvidenceId | null |
| stop/reason | Evidence-sufficient |
| stop/nextAction | Record limitation only |
| cleanup/id | CLN-MIV14-001 |
| cleanup/owner | Synthetic learner |
| cleanup/scope | current-authored-reading-copy-only |
| cleanup/action | 作業コピーを整理する設計を記録し、正本と親資料を保持する。 |
| cleanup/status | Recorded complete |
| cleanup/evidenceId | CLN-EVD-MIV14-001 |
| cleanup/actualDeletionPerformed | false |
| residual/id | RES-MIV14-001 |
| residual/owner | Synthetic reviewer |
| residual/scope | current-authored-reading-copy-only |
| residual/status | Recorded clear |
| residual/evidenceId | RES-EVD-MIV14-001 |
| residual/actualSystemAssessed | false |
| judgment/result | Supported |
| judgment/confidence | 中 |
| judgment/supportedScope | 二条件 |
| judgment/gap | 対象の実装と実影響は全件未測定。未観測の条件を推測しない。 |
| judgment/alternative | 供給資料と実システムの状態が異なる可能性がある。 |
| judgment/claimCeiling | 供給Policyの条件だけ。実装・実到達・業務影響は未確認。 |
| finding/id | FND-MIV14-001 |
| finding/validationId | VAL-MIV14-001 |
| finding/evidenceIds/0 | EVD-MIV14-001-1 |
| finding/evidenceIds/1 | EVD-MIV14-001-2 |
| finding/treatment | 未確認条件を記録し、必要なら新しい計画・許可の判断へ戻す。 |
| decision/id | DEC-MIV14-001 |
| decision/findingId | FND-MIV14-001 |
| decision/stopId | STP-MIV14-001 |
| decision/cleanupId | CLN-MIV14-001 |
| decision/residualId | RES-MIV14-001 |
| decision/recordStatus | Complete |
| decision/executionAuthorized | false |
| decision/owner | Synthetic case owner |
| decision/reassessmentId | REA-MIV14-001 |
| decision/dueAt | 2026-09-30T00:00:00Z |
| decision/reopenWhen | 対象版・Scope・Authority・必要Evidenceが変わったとき。 |

## validations VAL-MIV14-002

| Field | Value |
|---|---|
| id | VAL-MIV14-002 |
| revision | MIV14-REV-001 |
| hypothesisId | HYP-MIV14-002 |
| parentFindingId | FND-PSA13-002 |
| authorityId | AUTH-CASE-2026-001 |
| roeId | ROE-2026-009 |
| labPlanId | LABPLAN-2026-001 |
| decisionQuestion | この供給資料の対象Resource IDと監査参照IDは、期待した二条件それぞれに一致するか。 |
| minimumEvidenceQuestion | この対象ID・版の二条件について供給記録だけで支持と反証を区別できるか。 |
| expectationId | EXP-MIV14-002 |
| method | Simulation |
| methodRationale | 問いに必要な二条件だけを供給記録で読む。手法名は実行許可ではない。 |
| executionDisposition | Authored review only |
| unperformedReason | 実サービスへの操作は全件実施しない。供給記録の読解だけを表す。 |
| subjectId | OBJ-MIV14-002 |
| subjectRevision | SUPPLIED-REV-001 |
| observations/0/id | EVD-MIV14-002-1 |
| observations/0/criterionId | CRT-MIV14-002-A |
| observations/0/subjectId | OBJ-MIV14-002 |
| observations/0/subjectRevision | SUPPLIED-REV-001 |
| observations/0/present | true |
| observations/0/value | OBJ-MIV14-002 |
| observations/0/recordedAt | 2026-09-15T23:00:00Z |
| observations/0/basis | authored-observation |
| observations/1/id | EVD-MIV14-002-2 |
| observations/1/criterionId | CRT-MIV14-002-B |
| observations/1/subjectId | OBJ-MIV14-002 |
| observations/1/subjectRevision | SUPPLIED-REV-001 |
| observations/1/present | false |
| observations/1/value | null |
| observations/1/recordedAt | null |
| observations/1/basis | empty-evidence-slot-not-observed |
| evidenceIds/0 | EVD-MIV14-002-1 |
| minimumEvidenceMet | false |
| declaredReadSteps | 1 |
| stepsAfterStop | 0 |
| actualOperations | 0 |
| stop/id | STP-MIV14-002 |
| stop/trigger | None |
| stop/triggerEvidenceId | null |
| stop/reason | Evidence-gap |
| stop/nextAction | Record limitation only |
| cleanup/id | CLN-MIV14-002 |
| cleanup/owner | Synthetic learner |
| cleanup/scope | current-authored-reading-copy-only |
| cleanup/action | 作業コピーを整理する設計を記録し、正本と親資料を保持する。 |
| cleanup/status | Recorded complete |
| cleanup/evidenceId | CLN-EVD-MIV14-002 |
| cleanup/actualDeletionPerformed | false |
| residual/id | RES-MIV14-002 |
| residual/owner | Synthetic reviewer |
| residual/scope | current-authored-reading-copy-only |
| residual/status | Recorded clear |
| residual/evidenceId | RES-EVD-MIV14-002 |
| residual/actualSystemAssessed | false |
| judgment/result | Partially supported |
| judgment/confidence | 低 |
| judgment/supportedScope | 条件Aのみ |
| judgment/gap | 対象の実装と実影響は全件未測定。未観測の条件を推測しない。 |
| judgment/alternative | 供給資料と実システムの状態が異なる可能性がある。 |
| judgment/claimCeiling | 一条件だけ支持。未確認の条件を補完しない。 |
| finding/id | FND-MIV14-002 |
| finding/validationId | VAL-MIV14-002 |
| finding/evidenceIds/0 | EVD-MIV14-002-1 |
| finding/treatment | 未確認条件を記録し、必要なら新しい計画・許可の判断へ戻す。 |
| decision/id | DEC-MIV14-002 |
| decision/findingId | FND-MIV14-002 |
| decision/stopId | STP-MIV14-002 |
| decision/cleanupId | CLN-MIV14-002 |
| decision/residualId | RES-MIV14-002 |
| decision/recordStatus | Complete |
| decision/executionAuthorized | false |
| decision/owner | Synthetic case owner |
| decision/reassessmentId | REA-MIV14-002 |
| decision/dueAt | 2026-09-30T00:00:00Z |
| decision/reopenWhen | 対象版・Scope・Authority・必要Evidenceが変わったとき。 |

## validations VAL-MIV14-003

| Field | Value |
|---|---|
| id | VAL-MIV14-003 |
| revision | MIV14-REV-001 |
| hypothesisId | HYP-MIV14-003 |
| parentFindingId | FND-PSA13-003 |
| authorityId | AUTH-CASE-2026-001 |
| roeId | ROE-2026-009 |
| labPlanId | LABPLAN-2026-001 |
| decisionQuestion | この供給資料の対象Resource IDと監査参照IDは、期待した二条件それぞれに一致するか。 |
| minimumEvidenceQuestion | この対象ID・版の二条件について供給記録だけで支持と反証を区別できるか。 |
| expectationId | EXP-MIV14-003 |
| method | Offline replay |
| methodRationale | 問いに必要な二条件だけを供給記録で読む。手法名は実行許可ではない。 |
| executionDisposition | Authored review only |
| unperformedReason | 実サービスへの操作は全件実施しない。供給記録の読解だけを表す。 |
| subjectId | OBJ-MIV14-003 |
| subjectRevision | SUPPLIED-REV-001 |
| observations/0/id | EVD-MIV14-003-1 |
| observations/0/criterionId | CRT-MIV14-003-A |
| observations/0/subjectId | OBJ-MIV14-003 |
| observations/0/subjectRevision | SUPPLIED-REV-001 |
| observations/0/present | true |
| observations/0/value | OTHER-MIV14-003-1 |
| observations/0/recordedAt | 2026-09-15T23:00:00Z |
| observations/0/basis | authored-observation |
| observations/1/id | EVD-MIV14-003-2 |
| observations/1/criterionId | CRT-MIV14-003-B |
| observations/1/subjectId | OBJ-MIV14-003 |
| observations/1/subjectRevision | SUPPLIED-REV-001 |
| observations/1/present | false |
| observations/1/value | null |
| observations/1/recordedAt | null |
| observations/1/basis | empty-evidence-slot-not-observed |
| evidenceIds/0 | EVD-MIV14-003-1 |
| minimumEvidenceMet | false |
| declaredReadSteps | 1 |
| stepsAfterStop | 0 |
| actualOperations | 0 |
| stop/id | STP-MIV14-003 |
| stop/trigger | None |
| stop/triggerEvidenceId | null |
| stop/reason | Evidence-gap |
| stop/nextAction | Record limitation only |
| cleanup/id | CLN-MIV14-003 |
| cleanup/owner | Synthetic learner |
| cleanup/scope | current-authored-reading-copy-only |
| cleanup/action | 作業コピーを整理する設計を記録し、正本と親資料を保持する。 |
| cleanup/status | Recorded complete |
| cleanup/evidenceId | CLN-EVD-MIV14-003 |
| cleanup/actualDeletionPerformed | false |
| residual/id | RES-MIV14-003 |
| residual/owner | Synthetic reviewer |
| residual/scope | current-authored-reading-copy-only |
| residual/status | Recorded clear |
| residual/evidenceId | RES-EVD-MIV14-003 |
| residual/actualSystemAssessed | false |
| judgment/result | Weakened |
| judgment/confidence | 低 |
| judgment/supportedScope | 支持範囲なし |
| judgment/gap | 対象の実装と実影響は全件未測定。未観測の条件を推測しない。 |
| judgment/alternative | 供給資料と実システムの状態が異なる可能性がある。 |
| judgment/claimCeiling | 一つの反証と一つのGap。仮説の一部を弱めるだけ。 |
| finding/id | FND-MIV14-003 |
| finding/validationId | VAL-MIV14-003 |
| finding/evidenceIds/0 | EVD-MIV14-003-1 |
| finding/treatment | 未確認条件を記録し、必要なら新しい計画・許可の判断へ戻す。 |
| decision/id | DEC-MIV14-003 |
| decision/findingId | FND-MIV14-003 |
| decision/stopId | STP-MIV14-003 |
| decision/cleanupId | CLN-MIV14-003 |
| decision/residualId | RES-MIV14-003 |
| decision/recordStatus | Complete |
| decision/executionAuthorized | false |
| decision/owner | Synthetic case owner |
| decision/reassessmentId | REA-MIV14-003 |
| decision/dueAt | 2026-09-30T00:00:00Z |
| decision/reopenWhen | 対象版・Scope・Authority・必要Evidenceが変わったとき。 |

## validations VAL-MIV14-004

| Field | Value |
|---|---|
| id | VAL-MIV14-004 |
| revision | MIV14-REV-001 |
| hypothesisId | HYP-MIV14-004 |
| parentFindingId | FND-PSA13-004 |
| authorityId | AUTH-CASE-2026-001 |
| roeId | ROE-2026-009 |
| labPlanId | LABPLAN-2026-001 |
| decisionQuestion | この供給資料の対象Resource IDと監査参照IDは、期待した二条件それぞれに一致するか。 |
| minimumEvidenceQuestion | この対象ID・版の二条件について供給記録だけで支持と反証を区別できるか。 |
| expectationId | EXP-MIV14-004 |
| method | Offline replay |
| methodRationale | 問いに必要な二条件だけを供給記録で読む。手法名は実行許可ではない。 |
| executionDisposition | Authored review only |
| unperformedReason | 実サービスへの操作は全件実施しない。供給記録の読解だけを表す。 |
| subjectId | OBJ-MIV14-004 |
| subjectRevision | SUPPLIED-REV-001 |
| observations/0/id | EVD-MIV14-004-1 |
| observations/0/criterionId | CRT-MIV14-004-A |
| observations/0/subjectId | OBJ-MIV14-004 |
| observations/0/subjectRevision | SUPPLIED-REV-001 |
| observations/0/present | true |
| observations/0/value | OTHER-MIV14-004-1 |
| observations/0/recordedAt | 2026-09-15T23:00:00Z |
| observations/0/basis | authored-observation |
| observations/1/id | EVD-MIV14-004-2 |
| observations/1/criterionId | CRT-MIV14-004-B |
| observations/1/subjectId | OBJ-MIV14-004 |
| observations/1/subjectRevision | SUPPLIED-REV-001 |
| observations/1/present | true |
| observations/1/value | OTHER-MIV14-004-2 |
| observations/1/recordedAt | 2026-09-15T23:00:00Z |
| observations/1/basis | authored-observation |
| evidenceIds/0 | EVD-MIV14-004-1 |
| evidenceIds/1 | EVD-MIV14-004-2 |
| minimumEvidenceMet | true |
| declaredReadSteps | 1 |
| stepsAfterStop | 0 |
| actualOperations | 0 |
| stop/id | STP-MIV14-004 |
| stop/trigger | None |
| stop/triggerEvidenceId | null |
| stop/reason | Evidence-sufficient |
| stop/nextAction | Record limitation only |
| cleanup/id | CLN-MIV14-004 |
| cleanup/owner | Synthetic learner |
| cleanup/scope | current-authored-reading-copy-only |
| cleanup/action | 作業コピーを整理する設計を記録し、正本と親資料を保持する。 |
| cleanup/status | Recorded complete |
| cleanup/evidenceId | CLN-EVD-MIV14-004 |
| cleanup/actualDeletionPerformed | false |
| residual/id | RES-MIV14-004 |
| residual/owner | Synthetic reviewer |
| residual/scope | current-authored-reading-copy-only |
| residual/status | Recorded clear |
| residual/evidenceId | RES-EVD-MIV14-004 |
| residual/actualSystemAssessed | false |
| judgment/result | Rejected |
| judgment/confidence | 中 |
| judgment/supportedScope | 支持範囲なし |
| judgment/gap | 対象の実装と実影響は全件未測定。未観測の条件を推測しない。 |
| judgment/alternative | 供給資料と実システムの状態が異なる可能性がある。 |
| judgment/claimCeiling | この供給資料での二条件は反証。実環境全体の否定ではない。 |
| finding/id | FND-MIV14-004 |
| finding/validationId | VAL-MIV14-004 |
| finding/evidenceIds/0 | EVD-MIV14-004-1 |
| finding/evidenceIds/1 | EVD-MIV14-004-2 |
| finding/treatment | 未確認条件を記録し、必要なら新しい計画・許可の判断へ戻す。 |
| decision/id | DEC-MIV14-004 |
| decision/findingId | FND-MIV14-004 |
| decision/stopId | STP-MIV14-004 |
| decision/cleanupId | CLN-MIV14-004 |
| decision/residualId | RES-MIV14-004 |
| decision/recordStatus | Complete |
| decision/executionAuthorized | false |
| decision/owner | Synthetic case owner |
| decision/reassessmentId | REA-MIV14-004 |
| decision/dueAt | 2026-09-30T00:00:00Z |
| decision/reopenWhen | 対象版・Scope・Authority・必要Evidenceが変わったとき。 |

## validations VAL-MIV14-005

| Field | Value |
|---|---|
| id | VAL-MIV14-005 |
| revision | MIV14-REV-001 |
| hypothesisId | HYP-MIV14-005 |
| parentFindingId | FND-PSA13-005 |
| authorityId | AUTH-CASE-2026-001 |
| roeId | ROE-2026-009 |
| labPlanId | LABPLAN-2026-001 |
| decisionQuestion | この供給資料の対象Resource IDと監査参照IDは、期待した二条件それぞれに一致するか。 |
| minimumEvidenceQuestion | この対象ID・版の二条件について供給記録だけで支持と反証を区別できるか。 |
| expectationId | EXP-MIV14-005 |
| method | Static |
| methodRationale | 問いに必要な二条件だけを供給記録で読む。手法名は実行許可ではない。 |
| executionDisposition | Authored review only |
| unperformedReason | 実サービスへの操作は全件実施しない。供給記録の読解だけを表す。 |
| subjectId | OBJ-MIV14-005 |
| subjectRevision | SUPPLIED-REV-001 |
| observations/0/id | EVD-MIV14-005-1 |
| observations/0/criterionId | CRT-MIV14-005-A |
| observations/0/subjectId | OBJ-MIV14-005 |
| observations/0/subjectRevision | SUPPLIED-REV-001 |
| observations/0/present | false |
| observations/0/value | null |
| observations/0/recordedAt | null |
| observations/0/basis | empty-evidence-slot-not-observed |
| observations/1/id | EVD-MIV14-005-2 |
| observations/1/criterionId | CRT-MIV14-005-B |
| observations/1/subjectId | OBJ-MIV14-005 |
| observations/1/subjectRevision | SUPPLIED-REV-001 |
| observations/1/present | false |
| observations/1/value | null |
| observations/1/recordedAt | null |
| observations/1/basis | empty-evidence-slot-not-observed |
| evidenceIds | `[]` |
| minimumEvidenceMet | false |
| declaredReadSteps | 1 |
| stepsAfterStop | 0 |
| actualOperations | 0 |
| stop/id | STP-MIV14-005 |
| stop/trigger | None |
| stop/triggerEvidenceId | null |
| stop/reason | Evidence-gap |
| stop/nextAction | Record limitation only |
| cleanup/id | CLN-MIV14-005 |
| cleanup/owner | Synthetic learner |
| cleanup/scope | current-authored-reading-copy-only |
| cleanup/action | 作業コピーを整理する設計を記録し、正本と親資料を保持する。 |
| cleanup/status | Recorded complete |
| cleanup/evidenceId | CLN-EVD-MIV14-005 |
| cleanup/actualDeletionPerformed | false |
| residual/id | RES-MIV14-005 |
| residual/owner | Synthetic reviewer |
| residual/scope | current-authored-reading-copy-only |
| residual/status | Recorded clear |
| residual/evidenceId | RES-EVD-MIV14-005 |
| residual/actualSystemAssessed | false |
| judgment/result | Inconclusive |
| judgment/confidence | 低 |
| judgment/supportedScope | 支持範囲なし |
| judgment/gap | 対象の実装と実影響は全件未測定。未観測の条件を推測しない。 |
| judgment/alternative | 供給資料と実システムの状態が異なる可能性がある。 |
| judgment/claimCeiling | 必要な観測がなく、支持も反証も確定できない。 |
| finding/id | FND-MIV14-005 |
| finding/validationId | VAL-MIV14-005 |
| finding/evidenceIds | `[]` |
| finding/treatment | 未確認条件を記録し、必要なら新しい計画・許可の判断へ戻す。 |
| decision/id | DEC-MIV14-005 |
| decision/findingId | FND-MIV14-005 |
| decision/stopId | STP-MIV14-005 |
| decision/cleanupId | CLN-MIV14-005 |
| decision/residualId | RES-MIV14-005 |
| decision/recordStatus | Complete |
| decision/executionAuthorized | false |
| decision/owner | Synthetic case owner |
| decision/reassessmentId | REA-MIV14-005 |
| decision/dueAt | 2026-09-30T00:00:00Z |
| decision/reopenWhen | 対象版・Scope・Authority・必要Evidenceが変わったとき。 |

## validations VAL-MIV14-006

| Field | Value |
|---|---|
| id | VAL-MIV14-006 |
| revision | MIV14-REV-001 |
| hypothesisId | HYP-MIV14-006 |
| parentFindingId | FND-PSA13-006 |
| authorityId | AUTH-CASE-2026-001 |
| roeId | ROE-2026-009 |
| labPlanId | LABPLAN-2026-001 |
| decisionQuestion | この供給資料の対象Resource IDと監査参照IDは、期待した二条件それぞれに一致するか。 |
| minimumEvidenceQuestion | この対象ID・版の二条件について供給記録だけで支持と反証を区別できるか。 |
| expectationId | EXP-MIV14-006 |
| method | Minimal synthetic operation |
| methodRationale | 問いに必要な二条件だけを供給記録で読む。手法名は実行許可ではない。 |
| executionDisposition | Not performed |
| unperformedReason | 親RoEはDraftで許可は失効。本教材は実操作を行わず、合成Account作成も実施しない。 |
| subjectId | OBJ-MIV14-006 |
| subjectRevision | SUPPLIED-REV-001 |
| observations/0/id | EVD-MIV14-006-1 |
| observations/0/criterionId | CRT-MIV14-006-A |
| observations/0/subjectId | OBJ-MIV14-006 |
| observations/0/subjectRevision | SUPPLIED-REV-001 |
| observations/0/present | false |
| observations/0/value | null |
| observations/0/recordedAt | null |
| observations/0/basis | empty-evidence-slot-not-observed |
| observations/1/id | EVD-MIV14-006-2 |
| observations/1/criterionId | CRT-MIV14-006-B |
| observations/1/subjectId | OBJ-MIV14-006 |
| observations/1/subjectRevision | SUPPLIED-REV-001 |
| observations/1/present | false |
| observations/1/value | null |
| observations/1/recordedAt | null |
| observations/1/basis | empty-evidence-slot-not-observed |
| evidenceIds | `[]` |
| minimumEvidenceMet | false |
| declaredReadSteps | 0 |
| stepsAfterStop | 0 |
| actualOperations | 0 |
| stop/id | STP-MIV14-006 |
| stop/trigger | None |
| stop/triggerEvidenceId | null |
| stop/reason | Not-performed |
| stop/nextAction | Record limitation only |
| cleanup/id | CLN-MIV14-006 |
| cleanup/owner | Synthetic learner |
| cleanup/scope | current-authored-reading-copy-only |
| cleanup/action | 作業コピーを整理する設計を記録し、正本と親資料を保持する。 |
| cleanup/status | Not started |
| cleanup/evidenceId | null |
| cleanup/actualDeletionPerformed | false |
| residual/id | RES-MIV14-006 |
| residual/owner | Synthetic reviewer |
| residual/scope | current-authored-reading-copy-only |
| residual/status | Unknown |
| residual/evidenceId | null |
| residual/actualSystemAssessed | false |
| judgment/result | Inconclusive |
| judgment/confidence | 低 |
| judgment/supportedScope | 支持範囲なし |
| judgment/gap | 対象の実装と実影響は全件未測定。未観測の条件を推測しない。 |
| judgment/alternative | 供給資料と実システムの状態が異なる可能性がある。 |
| judgment/claimCeiling | 実施しない。資料だけでは問いの結論は確定できない。 |
| finding/id | FND-MIV14-006 |
| finding/validationId | VAL-MIV14-006 |
| finding/evidenceIds | `[]` |
| finding/treatment | 未確認条件を記録し、必要なら新しい計画・許可の判断へ戻す。 |
| decision/id | DEC-MIV14-006 |
| decision/findingId | FND-MIV14-006 |
| decision/stopId | STP-MIV14-006 |
| decision/cleanupId | CLN-MIV14-006 |
| decision/residualId | RES-MIV14-006 |
| decision/recordStatus | Open |
| decision/executionAuthorized | false |
| decision/owner | Synthetic case owner |
| decision/reassessmentId | REA-MIV14-006 |
| decision/dueAt | 2026-09-30T00:00:00Z |
| decision/reopenWhen | 対象版・Scope・Authority・必要Evidenceが変わったとき。 |

## validations VAL-MIV14-007

| Field | Value |
|---|---|
| id | VAL-MIV14-007 |
| revision | MIV14-REV-001 |
| hypothesisId | HYP-MIV14-007 |
| parentFindingId | FND-PSA13-007 |
| authorityId | AUTH-CASE-2026-001 |
| roeId | ROE-2026-009 |
| labPlanId | LABPLAN-2026-001 |
| decisionQuestion | この供給資料の対象Resource IDと監査参照IDは、期待した二条件それぞれに一致するか。 |
| minimumEvidenceQuestion | この対象ID・版の二条件について供給記録だけで支持と反証を区別できるか。 |
| expectationId | EXP-MIV14-007 |
| method | Static |
| methodRationale | 問いに必要な二条件だけを供給記録で読む。手法名は実行許可ではない。 |
| executionDisposition | Authored review only |
| unperformedReason | 実サービスへの操作は全件実施しない。供給記録の読解だけを表す。 |
| subjectId | OBJ-MIV14-007 |
| subjectRevision | SUPPLIED-REV-001 |
| observations/0/id | EVD-MIV14-007-1 |
| observations/0/criterionId | CRT-MIV14-007-A |
| observations/0/subjectId | OBJ-MIV14-007 |
| observations/0/subjectRevision | SUPPLIED-REV-001 |
| observations/0/present | false |
| observations/0/value | null |
| observations/0/recordedAt | null |
| observations/0/basis | empty-evidence-slot-not-observed |
| observations/1/id | EVD-MIV14-007-2 |
| observations/1/criterionId | CRT-MIV14-007-B |
| observations/1/subjectId | OBJ-MIV14-007 |
| observations/1/subjectRevision | SUPPLIED-REV-001 |
| observations/1/present | false |
| observations/1/value | null |
| observations/1/recordedAt | null |
| observations/1/basis | empty-evidence-slot-not-observed |
| evidenceIds | `[]` |
| minimumEvidenceMet | false |
| declaredReadSteps | 1 |
| stepsAfterStop | 0 |
| actualOperations | 0 |
| stop/id | STP-MIV14-007 |
| stop/trigger | Unexpected-input-symbol |
| stop/triggerEvidenceId | STOP-EVD-MIV14-007 |
| stop/reason | Unexpected-input-symbol |
| stop/nextAction | Record limitation only |
| cleanup/id | CLN-MIV14-007 |
| cleanup/owner | Synthetic learner |
| cleanup/scope | current-authored-reading-copy-only |
| cleanup/action | 作業コピーを整理する設計を記録し、正本と親資料を保持する。 |
| cleanup/status | Recorded complete |
| cleanup/evidenceId | CLN-EVD-MIV14-007 |
| cleanup/actualDeletionPerformed | false |
| residual/id | RES-MIV14-007 |
| residual/owner | Synthetic reviewer |
| residual/scope | current-authored-reading-copy-only |
| residual/status | Unknown |
| residual/evidenceId | null |
| residual/actualSystemAssessed | false |
| judgment/result | Stopped |
| judgment/confidence | 低 |
| judgment/supportedScope | 支持範囲なし |
| judgment/gap | 対象の実装と実影響は全件未測定。未観測の条件を推測しない。 |
| judgment/alternative | 供給資料と実システムの状態が異なる可能性がある。 |
| judgment/claimCeiling | 停止の記録だけ。実Dataの検出や実プロセス停止の測定ではない。 |
| finding/id | FND-MIV14-007 |
| finding/validationId | VAL-MIV14-007 |
| finding/evidenceIds | `[]` |
| finding/treatment | 未確認条件を記録し、必要なら新しい計画・許可の判断へ戻す。 |
| decision/id | DEC-MIV14-007 |
| decision/findingId | FND-MIV14-007 |
| decision/stopId | STP-MIV14-007 |
| decision/cleanupId | CLN-MIV14-007 |
| decision/residualId | RES-MIV14-007 |
| decision/recordStatus | Open |
| decision/executionAuthorized | false |
| decision/owner | Synthetic case owner |
| decision/reassessmentId | REA-MIV14-007 |
| decision/dueAt | 2026-09-30T00:00:00Z |
| decision/reopenWhen | 対象版・Scope・Authority・必要Evidenceが変わったとき。 |

## validations VAL-MIV14-008

| Field | Value |
|---|---|
| id | VAL-MIV14-008 |
| revision | MIV14-REV-001 |
| hypothesisId | HYP-MIV14-008 |
| parentFindingId | FND-PSA13-008 |
| authorityId | AUTH-CASE-2026-001 |
| roeId | ROE-2026-009 |
| labPlanId | LABPLAN-2026-001 |
| decisionQuestion | この供給資料の対象Resource IDと監査参照IDは、期待した二条件それぞれに一致するか。 |
| minimumEvidenceQuestion | この対象ID・版の二条件について供給記録だけで支持と反証を区別できるか。 |
| expectationId | EXP-MIV14-008 |
| method | Static |
| methodRationale | 問いに必要な二条件だけを供給記録で読む。手法名は実行許可ではない。 |
| executionDisposition | Authored review only |
| unperformedReason | 実サービスへの操作は全件実施しない。供給記録の読解だけを表す。 |
| subjectId | OBJ-MIV14-008 |
| subjectRevision | SUPPLIED-REV-001 |
| observations/0/id | EVD-MIV14-008-1 |
| observations/0/criterionId | CRT-MIV14-008-A |
| observations/0/subjectId | OBJ-MIV14-008 |
| observations/0/subjectRevision | SUPPLIED-REV-001 |
| observations/0/present | true |
| observations/0/value | OBJ-MIV14-008 |
| observations/0/recordedAt | 2026-09-15T23:00:00Z |
| observations/0/basis | authored-observation |
| observations/1/id | EVD-MIV14-008-2 |
| observations/1/criterionId | CRT-MIV14-008-B |
| observations/1/subjectId | OBJ-MIV14-008 |
| observations/1/subjectRevision | SUPPLIED-REV-001 |
| observations/1/present | true |
| observations/1/value | AUD-MIV14-008 |
| observations/1/recordedAt | 2026-09-15T23:00:00Z |
| observations/1/basis | authored-observation |
| evidenceIds/0 | EVD-MIV14-008-1 |
| evidenceIds/1 | EVD-MIV14-008-2 |
| minimumEvidenceMet | true |
| declaredReadSteps | 1 |
| stepsAfterStop | 0 |
| actualOperations | 0 |
| stop/id | STP-MIV14-008 |
| stop/trigger | None |
| stop/triggerEvidenceId | null |
| stop/reason | Evidence-sufficient |
| stop/nextAction | Record limitation only |
| cleanup/id | CLN-MIV14-008 |
| cleanup/owner | Synthetic learner |
| cleanup/scope | current-authored-reading-copy-only |
| cleanup/action | 作業コピーを整理する設計を記録し、正本と親資料を保持する。 |
| cleanup/status | Recorded complete |
| cleanup/evidenceId | CLN-EVD-MIV14-008 |
| cleanup/actualDeletionPerformed | false |
| residual/id | RES-MIV14-008 |
| residual/owner | Synthetic reviewer |
| residual/scope | current-authored-reading-copy-only |
| residual/status | Unknown |
| residual/evidenceId | null |
| residual/actualSystemAssessed | false |
| judgment/result | Supported |
| judgment/confidence | 低 |
| judgment/supportedScope | 二条件 |
| judgment/gap | 対象の実装と実影響は全件未測定。未観測の条件を推測しない。 |
| judgment/alternative | 供給資料と実システムの状態が異なる可能性がある。 |
| judgment/claimCeiling | 問いは支持されても、残存確認が不足し記録はOpen。 |
| finding/id | FND-MIV14-008 |
| finding/validationId | VAL-MIV14-008 |
| finding/evidenceIds/0 | EVD-MIV14-008-1 |
| finding/evidenceIds/1 | EVD-MIV14-008-2 |
| finding/treatment | 未確認条件を記録し、必要なら新しい計画・許可の判断へ戻す。 |
| decision/id | DEC-MIV14-008 |
| decision/findingId | FND-MIV14-008 |
| decision/stopId | STP-MIV14-008 |
| decision/cleanupId | CLN-MIV14-008 |
| decision/residualId | RES-MIV14-008 |
| decision/recordStatus | Open |
| decision/executionAuthorized | false |
| decision/owner | Synthetic case owner |
| decision/reassessmentId | REA-MIV14-008 |
| decision/dueAt | 2026-09-30T00:00:00Z |
| decision/reopenWhen | 対象版・Scope・Authority・必要Evidenceが変わったとき。 |

## handoffs HOF-MIV14-15

| Field | Value |
|---|---|
| id | HOF-MIV14-15 |
| caseId | CASE-2026-001 |
| recordId | MIV-2026-014 |
| targetChapter | 15 |
| status | planned-not-delivered |
| purpose | FindingとEvidence limitationを渡す計画。実施許可や検知成功は渡さない。 |
| executionAuthorized | false |

## handoffs HOF-MIV14-21

| Field | Value |
|---|---|
| id | HOF-MIV14-21 |
| caseId | CASE-2026-001 |
| recordId | MIV-2026-014 |
| targetChapter | 21 |
| status | planned-not-delivered |
| purpose | FindingとEvidence limitationを渡す計画。実施許可や検知成功は渡さない。 |
| executionAuthorized | false |
