# 第9章 完全合成記入例：Rules of Engagement

## 読み方とDecision Context

この記録は供給された三つの合成Objectを読むための計画例です。実Tenant・実Credential・実Log・実在担当者・実署名は含みません。`ART-02` / `ROE-2026-009` v1は`CASE-2026-001`をrefinesし、過去の`ROE-2026-001`を置換しません。

基準時点は2026-09-13T09:00:00Zです。親`AUTH-CASE-2026-001`は2026-08-19T09:00:00Z（日本時間18:00）に期限を過ぎているため、現状態は **Draft / Do not proceed** です。書面参照、承認版、署名欄のnullまたは空配列は未確認を明示する値であり、承認済みという意味ではありません。機械検査の成功は実施許可でも権限の真正性確認でもありません。

OWNは本書固有の計画・判断・Evidence・Handoffの直接IDです。BRIDGEは第2・4・8章の入力と後続Assessmentの形式、DELEGATEは[Pentest専門書](https://itdojp.github.io/pentest-learning-book/)等の方法論詳細と個別担当者の法的/契約判断です。一般的なRoEテーマの責任分担はCROSS_BOOK_MAPのままです。

以下の表は[計画JSON](fixtures/ch09-engagement-roe.json)の全Fieldを、各groupのField / Valueとして表示します。配列の番号は1から、nullは未確定、`[]`は空集合です。[閉じたSchema](../schemas/ch09-engagement-roe.schema.json)と章固有検査が型・ID・条件を照合します。これは帳票データであり、実行手順を自動起動する設定ファイルではありません。

## model

全体の版と、常にfalseである実行許可の境界です。

| model Field | Value |
|---|---|
| schemaVersion | 1.0.0 |
| modelVersion | 1.0.0 |
| synthetic | true |
| executionAuthorized | false |

## record

Document Controlです。作成基準時点と版を記録します。

| record Field | Value |
|---|---|
| artifactId | ART-02 |
| roeId | ROE-2026-009 |
| version | 1 |
| status | Draft |
| asOf | 2026-09-13T09:00:00Z |
| relation | refines |
| parentCaseId | CASE-2026-001 |
| supersedes | null |

## parents

親の記録と歴史的状態の参照です。列挙した親Asset/Flowを無条件にScopeへ含めるものではありません。

| parents Field | Value |
|---|---|
| authorizationRecordId | AUTH-CASE-2026-001 |
| authorizationDecisionId | DEC-AUTH-2026-001 |
| authorizationDecisionRequirementId | DR-AUTH-2026-001 |
| authorizationHistoricalOutcome | Proceed with conditions |
| authorizationExpiresAt | 2026-08-19T09:00:00Z |
| authorizationConditions / 1 | COND-AUTH-2026-001 Open |
| authorizationConditions / 2 | COND-AUTH-2026-002 Satisfied |
| authorizationConditions / 3 | COND-AUTH-2026-003 Open |
| threatModelId | TM-2026-001 |
| threatModelStatus | Needs Evidence |
| threatHypothesisId | TH-2026-002 |
| assetIds / 1 | ASSET-2026-002 |
| assetIds / 2 | ASSET-2026-003 |
| boundaryIds / 1 | TB-2026-001 |
| boundaryIds / 2 | TB-2026-003 |
| flowIds / 1 | FLOW-2026-002 |
| flowIds / 2 | FLOW-2026-004 |
| labPlanId | LABPLAN-2026-001 |
| labExecutionAuthorized | false |
| labEvidenceId | EVD-LAB08-001 |
| parentReassessmentId | REA-2026-001 |
| parentStateChanged | false |
| authorizationWindowStartsAt | 2026-08-06T00:00:00Z |
| authorizationWindowEndsAt | 2026-08-06T08:00:00Z |

## decision

親の過去の判断期限と、新しい計画のGapを分けます。

| decision Field | Value |
|---|---|
| requirementId | DR-2026-001 |
| owner | SYNTH-DECISION-OWNER |
| historicalDeadline | 2026-07-22T00:00:00Z |
| question | 合成OAuth設定とEventの矛盾を検討するため、許可・範囲・停止・Evidenceの計画はそろうか。 |
| plannedDecisionId | DEC-ROE09-001 |
| informationGapId | GAP-ROE09-001 |
| gap | 親Authorizationの期限経過。新しい判断期限・Authorization・実施承認は未確定。 |
| decisionUseful | not-assessed |

## scope

対象は供給された三Objectだけです。所有不明、第三者依存、未記載対象は許可しません。

| scope Field | Value |
|---|---|
| scopeId | SCOPE-ROE09-001 |
| defaultDenied | true |
| environment | ENV-ROE09-SYNTHETIC |
| identity | IDENTITY-ROE09-SYNTHETIC-READER |
| inScope / 1 / objectId | OBJ-ROE09-CONFIG |
| inScope / 1 / kind | OAuth configuration |
| inScope / 1 / owner | SYNTH-SYSTEM-OWNER |
| inScope / 1 / classification | synthetic-only |
| inScope / 1 / thirdParty | false |
| inScope / 2 / objectId | OBJ-ROE09-EVENT |
| inScope / 2 / kind | Authored event |
| inScope / 2 / owner | SYNTH-DATA-OWNER |
| inScope / 2 / classification | synthetic-only |
| inScope / 2 / thirdParty | false |
| inScope / 3 / objectId | OBJ-ROE09-POLICY |
| inScope / 3 / kind | Policy snapshot |
| inScope / 3 / owner | SYNTH-SYSTEM-OWNER |
| inScope / 3 / classification | synthetic-only |
| inScope / 3 / thirdParty | false |
| outOfScope / 1 | all-unlisted-objects |
| outOfScope / 2 | production-assets |
| outOfScope / 3 | real-identities |
| outOfScope / 4 | third-party-services |
| outOfScope / 5 | credential-material |
| outOfScope / 6 | personal-data |
| thirdPartyDependency | none-required |

## objects

作成者が書いた三つの合成値です。Eventの文章は実測ではなく、実Credentialの値はありません。

| objects Field | Value |
|---|---|
| 1 / objectId | OBJ-ROE09-CONFIG |
| 1 / synthetic | true |
| 1 / value | App label billing-bridge; requested permission read-fixture-summary; approval record absent. |
| 2 / objectId | OBJ-ROE09-EVENT |
| 2 / synthetic | true |
| 2 / value | Authored event: consent-record absent; no real request or observation occurred. |
| 3 / objectId | OBJ-ROE09-POLICY |
| 3 / synthetic | true |
| 3 / value | Author policy: only supplied synthetic records; all unlisted operations denied. |

## methods

供給記録の読解と比較だけを候補化します。全体の承認条件が未充足なので、実作業の許可は出ません。

| methods Field | Value |
|---|---|
| methodId | METHOD-ROE09-001 |
| permitted / 1 | read-supplied-json |
| permitted / 2 | compare-synthetic-fields |
| permitted / 3 | write-bounded-summary |
| conditional | `[]` |
| prohibited / 1 | external-communicationは禁止する。 |
| prohibited / 2 | active-scanningは禁止する。 |
| prohibited / 3 | authentication-attemptは禁止する。 |
| prohibited / 4 | credential-reuseは禁止する。 |
| prohibited / 5 | dosは禁止する。 |
| prohibited / 6 | persistenceは禁止する。 |
| prohibited / 7 | evasionは禁止する。 |
| prohibited / 8 | log-deletionは禁止する。 |
| prohibited / 9 | destructive-changeは禁止する。 |

## window

将来の提案Windowであり、親許可の期限外です。開始・終了を記入しても有効にはなりません。

| window Field | Value |
|---|---|
| timezone | UTC |
| startsAt | 2026-09-14T00:00:00Z |
| endsAt | 2026-09-14T00:30:00Z |
| status | proposed-not-authorized |

## limits

教材で定義した予算値です。実環境で制限を適用した証拠ではありません。

| limits Field | Value |
|---|---|
| networkRequests | 0 |
| records | 100 |
| evidenceBytes | 65536 |
| concurrency | 1 |
| retries | 0 |
| minutes | 30 |
| onLimit | stop-and-record-gap |

## data

保持・廃棄は仮想の作業コピーに対する計画です。教材正本・承認記録は別に保持し、本検査は削除しません。

| data Field | Value |
|---|---|
| dataId | DATA-ROE09-001 |
| classification | synthetic-only |
| credentialMaterial | none |
| storage | SYNTH-DEDICATED-WORK-COPY |
| custodian | SYNTH-EVIDENCE-CUSTODIAN |
| retentionHours | 24 |
| retentionStarts | hypothetical-session-end |
| destructionOwner | SYNTH-RECOVERY-OWNER |
| destructionPlan | 一時作業コピーだけを削除対象として台帳化し、正本・承認記録・教材を除外する。実際の削除は本検査では行わない。 |
| unexpectedData | 内容を追加表示・転送せず新規作業を停止し、参照IDだけで責任者へ通知する。 |

## stop

SYNTH役割は記入例であり、稼働中の連絡網ではありません。停止・Recovery・再開の権限を分けます。

| stop Field | Value |
|---|---|
| stopId | STOP-ROE09-001 |
| triggers / 1 | unknown-authority |
| triggers / 2 | out-of-scope |
| triggers / 3 | unexpected-data |
| triggers / 4 | external-communication |
| triggers / 5 | budget-exceeded |
| triggers / 6 | missing-evidence |
| triggers / 7 | unavailable-contact |
| triggers / 8 | cleanup-unconfirmed |
| primaryContact | SYNTH-TEST-LEAD |
| backupContact | SYNTH-SPONSOR |
| acknowledgementSeconds | 60 |
| recoveryOwner | SYNTH-RECOVERY-OWNER |
| recoverySteps / 1 | stop-new-work |
| recoverySteps / 2 | preserve-reference-and-time |
| recoverySteps / 3 | notify-primary-or-backup |
| recoverySteps / 4 | review-affected-synthetic-copies |
| recoverySteps / 5 | verify-cleanup-record |
| cleanupEvidenceId | CLEAN-ROE09-001 |
| cleanupStatus | not-executed |
| restartAuthority | SYNTH-AUTHORITY-OWNER |
| automaticRestart | false |

## approval

失効した親を保持した未承認記録です。新しい許可の発行や更新を表しません。

| approval Field | Value |
|---|---|
| sponsor | SYNTH-SPONSOR |
| authorityOwner | SYNTH-AUTHORITY-OWNER |
| systemOwner | SYNTH-SYSTEM-OWNER |
| dataOwner | SYNTH-DATA-OWNER |
| testLead | SYNTH-TEST-LEAD |
| authorizationId | AUTH-CASE-2026-001 |
| authorityStatus | Expired |
| writtenEvidenceRef | null |
| approvedVersion | null |
| validFrom | 2026-08-06T00:00:00Z |
| validUntil | 2026-08-19T09:00:00Z |
| signoffs | `[]` |

## evidence

EVD-ROE09-001は計画記録のIDであり、実作業結果ではありません。

| evidence Field | Value |
|---|---|
| evidenceId | EVD-ROE09-001 |
| type | authored-planning-record-not-observation |
| requiredFields / 1 | RoE ID and version |
| requiredFields / 2 | Scope and Method IDs |
| requiredFields / 3 | synthetic object ID |
| requiredFields / 4 | time and custodian |
| requiredFields / 5 | Source and limitation |
| requiredFields / 6 | stop and disposition |
| integrity | 正本JSONのbyte hashは取扱いの照合用。真正性・法的証拠能力・実行成功の証明ではない。 |
| prohibited | 実Credential・実Token・実Cookie・個人情報は収集しない。 |

## completion

作業もDecisionの受入も未実施です。TechnicalとDecisionの条件を別に記入しています。

| completion Field | Value |
|---|---|
| technicalStatus | not-executed |
| decisionStatus | not-assessed |
| technicalCriteria / 1 | selected-records-accounted |
| technicalCriteria / 2 | budget-and-stop-record-present |
| technicalCriteria / 3 | cleanup-reference-present |
| decisionCriteria / 1 | required-question-answered-or-gap-recorded |
| decisionCriteria / 2 | alternatives-and-confidence-recorded |
| decisionCriteria / 3 | owner-acceptance-and-reassessment-recorded |
| inconclusive | Required evidenceが不足したらInconclusiveとしてGapと再評価条件を残す。成功や不存在と表現しない。 |

## change

再評価予定は親REA-2026-001とは別です。変更・再開・Retestの承認は未取得です。

| change Field | Value |
|---|---|
| reauthorizationId | REA-ROE09-001 |
| changeRequestId | CR-ROE09-001 |
| kind | initial-plan |
| triggers / 1 | scope |
| triggers / 2 | method |
| triggers / 3 | data |
| triggers / 4 | time |
| triggers / 5 | budget |
| triggers / 6 | owner |
| triggers / 7 | version |
| triggers / 8 | stop |
| triggers / 9 | retest |
| newApprovalRequired | true |
| stopCleared | false |
| restartApprovalRef | null |
| retestId | RET-ROE09-001 |
| retestApprovalRef | null |
| reassessmentAt | 2026-09-14T00:00:00Z |
| resumeAutomatically | false |

## handoffs

後続に渡すべき入力と期待する返却形式の計画です。まだ引渡しや後続Validationを実施していません。

| handoffs Field | Value |
|---|---|
| 1 / handoffId | HOF-ROE09-001 |
| 1 / destination | Chapters10-14 |
| 1 / status | planned-not-delivered |
| 1 / inputIds / 1 | ROE-2026-009 v1 |
| 1 / inputIds / 2 | SCOPE-ROE09-001 |
| 1 / inputIds / 3 | METHOD-ROE09-001 |
| 1 / inputIds / 4 | STOP-ROE09-001 |
| 1 / returnContract | HypothesisとValidationをScope・Methodへ結び、Evidence参照またはGapを返す。現記録では開始不可。 |
| 2 / handoffId | HOF-ROE09-002 |
| 2 / destination | Chapter15 |
| 2 / status | planned-not-delivered |
| 2 / inputIds / 1 | RET-ROE09-001 |
| 2 / inputIds / 2 | REA-ROE09-001 |
| 2 / inputIds / 3 | CR-ROE09-001 |
| 2 / returnContract | 修正対象とRetest条件を新しい版・許可・Evidenceへ結ぶ。旧RoEの再利用ではない。 |
| 3 / handoffId | HOF-ROE09-003 |
| 3 / destination | Chapter21 |
| 3 / status | planned-not-delivered |
| 3 / inputIds / 1 | ROE-2026-009 v1 |
| 3 / inputIds / 2 | SCOPE-ROE09-001 |
| 3 / inputIds / 3 | METHOD-ROE09-001 |
| 3 / returnContract | Control Validationも独立のScope・Method・停止・許可確認を要する。Lab Safeから許可を導かない。 |

## boundary

第11章の独立CaseとRoEを同一視せず、権限・Evidenceを転用しません。

| boundary Field | Value |
|---|---|
| mode | non-executing-planning-model |
| independentCase | CASE-2026-011 |
| independentRoe | ROE-2026-011 |
| limitation | 授業用仮定。承認署名・実測・法的判断は存在しない。親の期限・Gap・Coverageを変更しない。 |
| expectedDisposition | Do not proceed |

## 判断と代替説明

確認済みの事実は、教材JSONの記録、親の期限、未承認欄、提案Windowが期限外であることです。分析判断は、現在の記録のままでは開始条件が整わないというDo not proceedです。信頼度はこの限定判断について高、実環境の権限・通知・隔離・削除の成立については未評価です。

代替説明として、新しい許可が別途存在する可能性はあります。しかし参照と責任者の確認がないため、それを仮定して実施可能とはしません。必要な追加Evidenceは新しい判断要求・期限、正確なScope/Method/期間に結び付いたAuthorization、同じ版の役割別承認、連絡・Recoveryの確認です。

条件が整った新記録を作る場合も、親の歴史的期限やOutcomeを修正して整合させません。新しいIDとRelationを審査し、別の教材版として記録します。現在の第4章Needs Evidence、第8章の非実行Lab、第11章の独立Caseは不変です。

## 負例と受入

Authority IDを消したApproved、Wildcard対象、対象外との重複、所有者Unknown、Permittedへの禁止作用追加、Data分類Unknown、連絡先・Recovery・Cleanup欠落は拒否します。Expired / Revoked / Paused / Completedは開始条件を満たしません。別版の署名、範囲外Window、停止原因未解消の再開、未承認Retestも差戻します。

[第9章の分析課題とRubric](../manuscript/09-engagement-roe.md)で、停止理由、必要なEvidence、再承認、後続Handoffを説明してください。[ART-02 Template](../templates/rules-of-engagement.md) / [Source Review Note](../references/ch09-source-review-2026-09-13.md)も同じ境界を適用します。
