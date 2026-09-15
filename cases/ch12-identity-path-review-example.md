# 第12章 完全合成記入例：Identity Attack Path Review

## この記入例の扱い

ART-20 / IAR-2026-012はCASE-2026-001をrefinesする教育用補足です。実Tenant、Directory、Account、Credential、Token、Cookie、実Logは使用しません。すべて作成者が記述した仮定で、実測・実認証・署名・許可の証拠ではありません。

[第12章](../manuscript/12-enterprise-identity.md)、[空Template](../templates/identity-attack-path-review.md)、[正本JSON](fixtures/ch12-identity-paths.json)、[閉じたSchema](../schemas/ch12-identity-paths.schema.json)を参照します。以下のField/Value表はJSONの全末端Fieldと一対一です。数字の添字は0始まりです。

## 読み方と判断

最初にparentsの期限とRoE Draft/falseを読みます。principalsからRole/Permission/Resourceへedgesをたどり、pathsの根拠をconfigEvidence、eventEvidence、evaluationsへ照合します。六つの状態はHypothesized / Config-confirmed / Evidence-supported / Validated / Broken / Unknownです。Unknownは空欄ではなく、不足を保持した判断です。

PTH-IAR12-001は休眠Grantの仮説、002はMFA例外を持つ静的設定、003はAudit readerの合成Event、004は合成Federation条件の有限一致、005は必要な委任承認の否定、006はDevice binding不足です。004のValidatedは実際のWorkload利用や親TB-2026-004/SF-2026-006のUnknownを更新しません。005のBrokenも別経路の不存在を意味しません。

確認事実は教材に含まれるFieldだけ、分析判断は各finding、仮定はGraphと時刻、推奨はTreatment計画です。確信度と代替説明は各Pathへ記録し、新しい資料・版・Owner・権限・許可の変化で再評価します。第11章のCASE-2026-011は独立で、許可やEvidenceを移しません。

## schemaVersion

| Field | Value |
|---|---|
| schemaVersion | 1.0.0 |

## modelVersion

| Field | Value |
|---|---|
| modelVersion | 1.0.0 |

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
| artifactId | ART-20 |
| reviewId | IAR-2026-012 |
| caseId | CASE-2026-001 |
| relation | refines |
| decisionRequirementId | DR-2026-001 |
| asOf | 2026-09-15T09:00:00Z |
| question | 供給された権限関係のどこまでを根拠で説明でき、何の許可と観測が不足するか。 |
| graphRevision | GRAPH-IAR12-001 |
| policyRevision | POLICY-IAR12-001 |
| authoredNotMeasured | true |

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
| threatModelId | TM-2026-001 |
| signalFlowMapId | SFM-2026-001 |
| reconRecordId | ASR-2026-010 |
| reconCandidateId | CAND-ASR10-001 |
| parentAssetId | ASSET-2026-001 |
| parentScopeExpanded | false |
| parentBindingConfirmed | false |
| parentCoverageChanged | false |
| independentChapter11Case | CASE-2026-011 |
| chapter11Relation | conceptual-handoff-only-no-evidence-or-authority-inheritance |

## principals PRN-IAR12-001

| Field | Value |
|---|---|
| id | PRN-IAR12-001 |
| principalClass | Human |
| label | SYNTH-DORMANT-ADMIN |
| owner | SYNTH-IDENTITY-OWNER |
| lifecycle | Dormant |
| credentialClass | interactive-authenticator-class |
| assuranceContext | not-assessed-no-compliance-claim |
| mfaStatus | Enabled |
| mfaException | exception-recorded-not-approved |

## principals PRN-IAR12-002

| Field | Value |
|---|---|
| id | PRN-IAR12-002 |
| principalClass | Device |
| label | SYNTH-DEVICE |
| owner | SYNTH-IDENTITY-OWNER |
| lifecycle | Unknown |
| credentialClass | device-binding-class |
| assuranceContext | not-assessed-no-compliance-claim |
| mfaStatus | Not applicable |
| mfaException | none |

## principals PRN-IAR12-003

| Field | Value |
|---|---|
| id | PRN-IAR12-003 |
| principalClass | Service |
| label | SYNTH-AUDIT-READER |
| owner | SYNTH-IDENTITY-OWNER |
| lifecycle | Active |
| credentialClass | service-authentication-class |
| assuranceContext | not-assessed-no-compliance-claim |
| mfaStatus | Not applicable |
| mfaException | none |

## principals PRN-IAR12-004

| Field | Value |
|---|---|
| id | PRN-IAR12-004 |
| principalClass | Workload |
| label | SYNTH-INVOICE-SYNC |
| owner | SYNTH-IDENTITY-OWNER |
| lifecycle | Active |
| credentialClass | workload-authentication-class |
| assuranceContext | not-assessed-no-compliance-claim |
| mfaStatus | Not applicable |
| mfaException | none |

## groups GRP-IAR12-001

| Field | Value |
|---|---|
| id | GRP-IAR12-001 |
| label | SYNTH-DORMANT-ADMIN-GROUP |

## roles ROL-IAR12-001

| Field | Value |
|---|---|
| id | ROL-IAR12-001 |
| label | SYNTH-ADMIN |

## roles ROL-IAR12-002

| Field | Value |
|---|---|
| id | ROL-IAR12-002 |
| label | SYNTH-AUDIT-READER |

## roles ROL-IAR12-003

| Field | Value |
|---|---|
| id | ROL-IAR12-003 |
| label | SYNTH-APP-READER |

## permissions PER-IAR12-001

| Field | Value |
|---|---|
| id | PER-IAR12-001 |
| resourceId | RES-IAR12-001 |
| action | review-consent-change |

## permissions PER-IAR12-002

| Field | Value |
|---|---|
| id | PER-IAR12-002 |
| resourceId | RES-IAR12-002 |
| action | read-audit-summary |

## permissions PER-IAR12-003

| Field | Value |
|---|---|
| id | PER-IAR12-003 |
| resourceId | RES-IAR12-003 |
| action | read-customer-summary |

## resources RES-IAR12-001

| Field | Value |
|---|---|
| id | RES-IAR12-001 |
| label | SYNTH-IDENTITY-CONTROL |
| plane | Control |
| controlPlaneId | CP-IAR12-001 |
| relyingPartyId | RP-IAR12-001 |

## resources RES-IAR12-002

| Field | Value |
|---|---|
| id | RES-IAR12-002 |
| label | SYNTH-AUDIT-SUMMARY |
| plane | Data |
| controlPlaneId | CP-IAR12-001 |
| relyingPartyId | RP-IAR12-002 |

## resources RES-IAR12-003

| Field | Value |
|---|---|
| id | RES-IAR12-003 |
| label | SYNTH-CUSTOMER-DATA-API-SUMMARY |
| plane | Data |
| controlPlaneId | CP-IAR12-001 |
| relyingPartyId | RP-IAR12-003 |

## controlPlanes CP-IAR12-001

| Field | Value |
|---|---|
| id | CP-IAR12-001 |
| label | SYNTH-IDENTITY-CONTROL-PLANE |

## issuers ISS-IAR12-001

| Field | Value |
|---|---|
| id | ISS-IAR12-001 |
| label | SYNTH-TRUSTED-ISSUER |

## relyingParties RP-IAR12-001

| Field | Value |
|---|---|
| id | RP-IAR12-001 |
| resourceId | RES-IAR12-001 |

## relyingParties RP-IAR12-002

| Field | Value |
|---|---|
| id | RP-IAR12-002 |
| resourceId | RES-IAR12-002 |

## relyingParties RP-IAR12-003

| Field | Value |
|---|---|
| id | RP-IAR12-003 |
| resourceId | RES-IAR12-003 |

## edges EDG-IAR12-001

| Field | Value |
|---|---|
| id | EDG-IAR12-001 |
| fromId | PRN-IAR12-001 |
| toId | GRP-IAR12-001 |
| kind | Membership |
| condition | True |
| conditionMeaning | authored-binding |
| boundaryId | TB-2026-001 |
| issuerId | null |
| audienceId | null |

## edges EDG-IAR12-002

| Field | Value |
|---|---|
| id | EDG-IAR12-002 |
| fromId | GRP-IAR12-001 |
| toId | ROL-IAR12-001 |
| kind | Membership |
| condition | True |
| conditionMeaning | authored-binding |
| boundaryId | TB-2026-001 |
| issuerId | null |
| audienceId | null |

## edges EDG-IAR12-003

| Field | Value |
|---|---|
| id | EDG-IAR12-003 |
| fromId | ROL-IAR12-001 |
| toId | PER-IAR12-001 |
| kind | Grant |
| condition | True |
| conditionMeaning | authored-binding |
| boundaryId | TB-2026-001 |
| issuerId | null |
| audienceId | null |

## edges EDG-IAR12-004

| Field | Value |
|---|---|
| id | EDG-IAR12-004 |
| fromId | PER-IAR12-001 |
| toId | RES-IAR12-001 |
| kind | Access |
| condition | True |
| conditionMeaning | authored-binding |
| boundaryId | TB-2026-001 |
| issuerId | null |
| audienceId | null |

## edges EDG-IAR12-005

| Field | Value |
|---|---|
| id | EDG-IAR12-005 |
| fromId | PRN-IAR12-001 |
| toId | ROL-IAR12-001 |
| kind | Membership |
| condition | True |
| conditionMeaning | authored-binding |
| boundaryId | TB-2026-001 |
| issuerId | null |
| audienceId | null |

## edges EDG-IAR12-006

| Field | Value |
|---|---|
| id | EDG-IAR12-006 |
| fromId | PRN-IAR12-003 |
| toId | ROL-IAR12-002 |
| kind | Membership |
| condition | True |
| conditionMeaning | authored-binding |
| boundaryId | TB-2026-003 |
| issuerId | null |
| audienceId | null |

## edges EDG-IAR12-007

| Field | Value |
|---|---|
| id | EDG-IAR12-007 |
| fromId | ROL-IAR12-002 |
| toId | PER-IAR12-002 |
| kind | Grant |
| condition | True |
| conditionMeaning | authored-binding |
| boundaryId | TB-2026-003 |
| issuerId | null |
| audienceId | null |

## edges EDG-IAR12-008

| Field | Value |
|---|---|
| id | EDG-IAR12-008 |
| fromId | PER-IAR12-002 |
| toId | RES-IAR12-002 |
| kind | Access |
| condition | True |
| conditionMeaning | authored-binding |
| boundaryId | TB-2026-003 |
| issuerId | null |
| audienceId | null |

## edges EDG-IAR12-009

| Field | Value |
|---|---|
| id | EDG-IAR12-009 |
| fromId | PRN-IAR12-004 |
| toId | PRN-IAR12-003 |
| kind | Delegation |
| condition | False |
| conditionMeaning | delegation-approval |
| boundaryId | TB-2026-004 |
| issuerId | null |
| audienceId | null |

## edges EDG-IAR12-010

| Field | Value |
|---|---|
| id | EDG-IAR12-010 |
| fromId | PRN-IAR12-003 |
| toId | ROL-IAR12-003 |
| kind | Membership |
| condition | True |
| conditionMeaning | authored-binding |
| boundaryId | TB-2026-001 |
| issuerId | null |
| audienceId | null |

## edges EDG-IAR12-011

| Field | Value |
|---|---|
| id | EDG-IAR12-011 |
| fromId | ROL-IAR12-003 |
| toId | PER-IAR12-003 |
| kind | Grant |
| condition | True |
| conditionMeaning | authored-binding |
| boundaryId | TB-2026-001 |
| issuerId | null |
| audienceId | null |

## edges EDG-IAR12-012

| Field | Value |
|---|---|
| id | EDG-IAR12-012 |
| fromId | PER-IAR12-003 |
| toId | RES-IAR12-003 |
| kind | Access |
| condition | True |
| conditionMeaning | authored-binding |
| boundaryId | TB-2026-001 |
| issuerId | null |
| audienceId | null |

## edges EDG-IAR12-013

| Field | Value |
|---|---|
| id | EDG-IAR12-013 |
| fromId | PRN-IAR12-004 |
| toId | ROL-IAR12-003 |
| kind | Federation |
| condition | True |
| conditionMeaning | authored-binding |
| boundaryId | TB-2026-004 |
| issuerId | ISS-IAR12-001 |
| audienceId | RP-IAR12-003 |

## edges EDG-IAR12-014

| Field | Value |
|---|---|
| id | EDG-IAR12-014 |
| fromId | PRN-IAR12-002 |
| toId | ROL-IAR12-003 |
| kind | Trust |
| condition | Unknown |
| conditionMeaning | device-binding |
| boundaryId | TB-2026-004 |
| issuerId | null |
| audienceId | null |

## paths PTH-IAR12-001

| Field | Value |
|---|---|
| id | PTH-IAR12-001 |
| label | Dormant grant is a hypothesis |
| principalId | PRN-IAR12-001 |
| requiredPermissionId | PER-IAR12-001 |
| resourceId | RES-IAR12-001 |
| action | review-consent-change |
| edgeIds/0 | EDG-IAR12-001 |
| edgeIds/1 | EDG-IAR12-002 |
| edgeIds/2 | EDG-IAR12-003 |
| edgeIds/3 | EDG-IAR12-004 |
| graphRevision | GRAPH-IAR12-001 |
| policyRevision | POLICY-IAR12-001 |
| state | Hypothesized |
| validationMethod | Static review |
| configEvidenceId | null |
| eventEvidenceId | null |
| evaluationId | null |
| threatId | TH-2026-002 |
| signalFlowId | SF-2026-001 |
| telemetryId | TEL-IAR12-001 |
| detectionId | DET-IAR12-001 |
| findingId | FND-IAR12-001 |
| gapId | GAP-IAR12-001 |
| reassessmentId | REA-IAR12-001 |
| owner | SYNTH-IDENTITY-OWNER |
| dueAt | 2026-09-22T00:00:00Z |
| confidence | Low |
| alternative | 正常な変更または資料不足を比較する。親Caseの実態は未確定。 |
| nextAction | record-only |
| executionAuthorized | false |

## paths PTH-IAR12-002

| Field | Value |
|---|---|
| id | PTH-IAR12-002 |
| label | MFA exception does not close permission path |
| principalId | PRN-IAR12-001 |
| requiredPermissionId | PER-IAR12-001 |
| resourceId | RES-IAR12-001 |
| action | review-consent-change |
| edgeIds/0 | EDG-IAR12-005 |
| edgeIds/1 | EDG-IAR12-003 |
| edgeIds/2 | EDG-IAR12-004 |
| graphRevision | GRAPH-IAR12-001 |
| policyRevision | POLICY-IAR12-001 |
| state | Config-confirmed |
| validationMethod | Static review |
| configEvidenceId | EVD-IAR12-002 |
| eventEvidenceId | null |
| evaluationId | null |
| threatId | TH-2026-002 |
| signalFlowId | SF-2026-004 |
| telemetryId | TEL-IAR12-002 |
| detectionId | DET-IAR12-002 |
| findingId | FND-IAR12-002 |
| gapId | GAP-IAR12-002 |
| reassessmentId | REA-IAR12-002 |
| owner | SYNTH-IDENTITY-OWNER |
| dueAt | 2026-09-22T00:00:00Z |
| confidence | Medium |
| alternative | 正常な変更または資料不足を比較する。親Caseの実態は未確定。 |
| nextAction | record-only |
| executionAuthorized | false |

## paths PTH-IAR12-003

| Field | Value |
|---|---|
| id | PTH-IAR12-003 |
| label | Audit-reader authored event supports limited relation |
| principalId | PRN-IAR12-003 |
| requiredPermissionId | PER-IAR12-002 |
| resourceId | RES-IAR12-002 |
| action | read-audit-summary |
| edgeIds/0 | EDG-IAR12-006 |
| edgeIds/1 | EDG-IAR12-007 |
| edgeIds/2 | EDG-IAR12-008 |
| graphRevision | GRAPH-IAR12-001 |
| policyRevision | POLICY-IAR12-001 |
| state | Evidence-supported |
| validationMethod | Synthetic replay |
| configEvidenceId | EVD-IAR12-003 |
| eventEvidenceId | EVT-IAR12-003 |
| evaluationId | null |
| threatId | TH-2026-003 |
| signalFlowId | SF-2026-002 |
| telemetryId | TEL-IAR12-003 |
| detectionId | DET-IAR12-003 |
| findingId | FND-IAR12-003 |
| gapId | GAP-IAR12-003 |
| reassessmentId | REA-IAR12-003 |
| owner | SYNTH-IDENTITY-OWNER |
| dueAt | 2026-09-22T00:00:00Z |
| confidence | Medium |
| alternative | 正常な変更または資料不足を比較する。親Caseの実態は未確定。 |
| nextAction | record-only |
| executionAuthorized | false |

## paths PTH-IAR12-004

| Field | Value |
|---|---|
| id | PTH-IAR12-004 |
| label | Synthetic federation tuple matches |
| principalId | PRN-IAR12-004 |
| requiredPermissionId | PER-IAR12-003 |
| resourceId | RES-IAR12-003 |
| action | read-customer-summary |
| edgeIds/0 | EDG-IAR12-013 |
| edgeIds/1 | EDG-IAR12-011 |
| edgeIds/2 | EDG-IAR12-012 |
| graphRevision | GRAPH-IAR12-001 |
| policyRevision | POLICY-IAR12-001 |
| state | Validated |
| validationMethod | Policy simulation |
| configEvidenceId | EVD-IAR12-004 |
| eventEvidenceId | null |
| evaluationId | EVAL-IAR12-004 |
| threatId | TH-2026-004 |
| signalFlowId | SF-2026-006 |
| telemetryId | TEL-IAR12-004 |
| detectionId | DET-IAR12-004 |
| findingId | FND-IAR12-004 |
| gapId | GAP-IAR12-004 |
| reassessmentId | REA-IAR12-004 |
| owner | SYNTH-IDENTITY-OWNER |
| dueAt | 2026-09-22T00:00:00Z |
| confidence | Medium |
| alternative | 正常な変更または資料不足を比較する。親Caseの実態は未確定。 |
| nextAction | record-only |
| executionAuthorized | false |

## paths PTH-IAR12-005

| Field | Value |
|---|---|
| id | PTH-IAR12-005 |
| label | Necessary delegation approval is denied |
| principalId | PRN-IAR12-004 |
| requiredPermissionId | PER-IAR12-003 |
| resourceId | RES-IAR12-003 |
| action | read-customer-summary |
| edgeIds/0 | EDG-IAR12-009 |
| edgeIds/1 | EDG-IAR12-010 |
| edgeIds/2 | EDG-IAR12-011 |
| edgeIds/3 | EDG-IAR12-012 |
| graphRevision | GRAPH-IAR12-001 |
| policyRevision | POLICY-IAR12-001 |
| state | Broken |
| validationMethod | Policy simulation |
| configEvidenceId | EVD-IAR12-005 |
| eventEvidenceId | null |
| evaluationId | EVAL-IAR12-005 |
| threatId | TH-2026-004 |
| signalFlowId | SF-2026-006 |
| telemetryId | TEL-IAR12-005 |
| detectionId | DET-IAR12-005 |
| findingId | FND-IAR12-005 |
| gapId | GAP-IAR12-005 |
| reassessmentId | REA-IAR12-005 |
| owner | SYNTH-IDENTITY-OWNER |
| dueAt | 2026-09-22T00:00:00Z |
| confidence | Medium |
| alternative | 正常な変更または資料不足を比較する。親Caseの実態は未確定。 |
| nextAction | record-only |
| executionAuthorized | false |

## paths PTH-IAR12-006

| Field | Value |
|---|---|
| id | PTH-IAR12-006 |
| label | Device binding condition is absent |
| principalId | PRN-IAR12-002 |
| requiredPermissionId | PER-IAR12-003 |
| resourceId | RES-IAR12-003 |
| action | read-customer-summary |
| edgeIds/0 | EDG-IAR12-014 |
| edgeIds/1 | EDG-IAR12-011 |
| edgeIds/2 | EDG-IAR12-012 |
| graphRevision | GRAPH-IAR12-001 |
| policyRevision | POLICY-IAR12-001 |
| state | Unknown |
| validationMethod | Static review |
| configEvidenceId | null |
| eventEvidenceId | null |
| evaluationId | null |
| threatId | TH-2026-004 |
| signalFlowId | SF-2026-006 |
| telemetryId | TEL-IAR12-006 |
| detectionId | DET-IAR12-006 |
| findingId | FND-IAR12-006 |
| gapId | GAP-IAR12-006 |
| reassessmentId | REA-IAR12-006 |
| owner | SYNTH-IDENTITY-OWNER |
| dueAt | 2026-09-22T00:00:00Z |
| confidence | Low |
| alternative | 正常な変更または資料不足を比較する。親Caseの実態は未確定。 |
| nextAction | record-only |
| executionAuthorized | false |

## configEvidence EVD-IAR12-002

| Field | Value |
|---|---|
| id | EVD-IAR12-002 |
| pathId | PTH-IAR12-002 |
| graphRevision | GRAPH-IAR12-001 |
| policyRevision | POLICY-IAR12-001 |
| edgeIds/0 | EDG-IAR12-005 |
| edgeIds/1 | EDG-IAR12-003 |
| edgeIds/2 | EDG-IAR12-004 |
| recordedAt | 2026-09-15T00:00:00Z |
| basis | authored-synthetic-snapshot-not-observation |
| synthetic | true |

## configEvidence EVD-IAR12-003

| Field | Value |
|---|---|
| id | EVD-IAR12-003 |
| pathId | PTH-IAR12-003 |
| graphRevision | GRAPH-IAR12-001 |
| policyRevision | POLICY-IAR12-001 |
| edgeIds/0 | EDG-IAR12-006 |
| edgeIds/1 | EDG-IAR12-007 |
| edgeIds/2 | EDG-IAR12-008 |
| recordedAt | 2026-09-15T00:00:00Z |
| basis | authored-synthetic-snapshot-not-observation |
| synthetic | true |

## configEvidence EVD-IAR12-004

| Field | Value |
|---|---|
| id | EVD-IAR12-004 |
| pathId | PTH-IAR12-004 |
| graphRevision | GRAPH-IAR12-001 |
| policyRevision | POLICY-IAR12-001 |
| edgeIds/0 | EDG-IAR12-013 |
| edgeIds/1 | EDG-IAR12-011 |
| edgeIds/2 | EDG-IAR12-012 |
| recordedAt | 2026-09-15T00:00:00Z |
| basis | authored-synthetic-snapshot-not-observation |
| synthetic | true |

## configEvidence EVD-IAR12-005

| Field | Value |
|---|---|
| id | EVD-IAR12-005 |
| pathId | PTH-IAR12-005 |
| graphRevision | GRAPH-IAR12-001 |
| policyRevision | POLICY-IAR12-001 |
| edgeIds/0 | EDG-IAR12-009 |
| edgeIds/1 | EDG-IAR12-010 |
| edgeIds/2 | EDG-IAR12-011 |
| edgeIds/3 | EDG-IAR12-012 |
| recordedAt | 2026-09-15T00:00:00Z |
| basis | authored-synthetic-snapshot-not-observation |
| synthetic | true |

## eventEvidence EVT-IAR12-003

| Field | Value |
|---|---|
| id | EVT-IAR12-003 |
| pathId | PTH-IAR12-003 |
| graphRevision | GRAPH-IAR12-001 |
| policyRevision | POLICY-IAR12-001 |
| principalId | PRN-IAR12-003 |
| resourceId | RES-IAR12-002 |
| action | read-audit-summary |
| outcome | Allow |
| recordedAt | 2026-09-15T00:00:00Z |
| basis | authored-synthetic-event-not-request |
| synthetic | true |

## evaluations EVAL-IAR12-004

| Field | Value |
|---|---|
| id | EVAL-IAR12-004 |
| pathId | PTH-IAR12-004 |
| graphRevision | GRAPH-IAR12-001 |
| policyRevision | POLICY-IAR12-001 |
| principalId | PRN-IAR12-004 |
| resourceId | RES-IAR12-003 |
| action | read-customer-summary |
| issuerId | ISS-IAR12-001 |
| audienceId | RP-IAR12-003 |
| relyingPartyId | RP-IAR12-003 |
| conditions/0/edgeId | EDG-IAR12-013 |
| conditions/0/condition | True |
| conditions/1/edgeId | EDG-IAR12-011 |
| conditions/1/condition | True |
| conditions/2/edgeId | EDG-IAR12-012 |
| conditions/2/condition | True |
| expected | Allow |
| actual | Allow |
| refutedEdgeId | null |
| configEvidenceId | EVD-IAR12-004 |
| recordedAt | 2026-09-15T00:00:00Z |
| basis | authored-input-and-result-for-finite-offline-comparison |
| networkRequests | 0 |
| authenticationAttempts | 0 |
| synthetic | true |

## evaluations EVAL-IAR12-005

| Field | Value |
|---|---|
| id | EVAL-IAR12-005 |
| pathId | PTH-IAR12-005 |
| graphRevision | GRAPH-IAR12-001 |
| policyRevision | POLICY-IAR12-001 |
| principalId | PRN-IAR12-004 |
| resourceId | RES-IAR12-003 |
| action | read-customer-summary |
| issuerId | ISS-IAR12-001 |
| audienceId | RP-IAR12-003 |
| relyingPartyId | RP-IAR12-003 |
| conditions/0/edgeId | EDG-IAR12-009 |
| conditions/0/condition | False |
| conditions/1/edgeId | EDG-IAR12-010 |
| conditions/1/condition | True |
| conditions/2/edgeId | EDG-IAR12-011 |
| conditions/2/condition | True |
| conditions/3/edgeId | EDG-IAR12-012 |
| conditions/3/condition | True |
| expected | Deny |
| actual | Deny |
| refutedEdgeId | EDG-IAR12-009 |
| configEvidenceId | EVD-IAR12-005 |
| recordedAt | 2026-09-15T00:00:00Z |
| basis | authored-input-and-result-for-finite-offline-comparison |
| networkRequests | 0 |
| authenticationAttempts | 0 |
| synthetic | true |

## findings FND-IAR12-001

| Field | Value |
|---|---|
| id | FND-IAR12-001 |
| pathId | PTH-IAR12-001 |
| status | teaching-analysis-not-production-finding |
| risk | 休眠Roleの残存による将来権限集中の仮説。現利用は未確認。 |
| treatment | Ownerと必要業務を再確認する計画。 |
| telemetryId | TEL-IAR12-001 |
| detectionId | DET-IAR12-001 |
| requiredFields/0 | principalId |
| requiredFields/1 | resourceId |
| requiredFields/2 | action |
| requiredFields/3 | policyRevision |
| requiredFields/4 | graphRevision |
| requiredFields/5 | outcome |
| requiredFields/6 | eventTime |
| requiredFields/7 | correlationId |
| detectionStatus | planned-not-tested |
| owner | SYNTH-IDENTITY-OWNER |
| reassessmentId | REA-IAR12-001 |

## findings FND-IAR12-002

| Field | Value |
|---|---|
| id | FND-IAR12-002 |
| pathId | PTH-IAR12-002 |
| status | teaching-analysis-not-production-finding |
| risk | MFA例外と管理権限の併存。認可の正しさは未検証。 |
| treatment | 例外の期限・承認とRole縮小案を別々にReviewする計画。 |
| telemetryId | TEL-IAR12-002 |
| detectionId | DET-IAR12-002 |
| requiredFields/0 | principalId |
| requiredFields/1 | resourceId |
| requiredFields/2 | action |
| requiredFields/3 | policyRevision |
| requiredFields/4 | graphRevision |
| requiredFields/5 | outcome |
| requiredFields/6 | eventTime |
| requiredFields/7 | correlationId |
| detectionStatus | planned-not-tested |
| owner | SYNTH-IDENTITY-OWNER |
| reassessmentId | REA-IAR12-002 |

## findings FND-IAR12-003

| Field | Value |
|---|---|
| id | FND-IAR12-003 |
| pathId | PTH-IAR12-003 |
| status | teaching-analysis-not-production-finding |
| risk | Audit参照の記録はあるが全期間の観測性は不明。 |
| treatment | 収集・保持・検索のGapを第16章へ渡す計画。 |
| telemetryId | TEL-IAR12-003 |
| detectionId | DET-IAR12-003 |
| requiredFields/0 | principalId |
| requiredFields/1 | resourceId |
| requiredFields/2 | action |
| requiredFields/3 | policyRevision |
| requiredFields/4 | graphRevision |
| requiredFields/5 | outcome |
| requiredFields/6 | eventTime |
| requiredFields/7 | correlationId |
| detectionStatus | planned-not-tested |
| owner | SYNTH-IDENTITY-OWNER |
| reassessmentId | REA-IAR12-003 |

## findings FND-IAR12-004

| Field | Value |
|---|---|
| id | FND-IAR12-004 |
| pathId | PTH-IAR12-004 |
| status | teaching-analysis-not-production-finding |
| risk | 合成許可条件は一致するが実環境のbindingは未確認。 |
| treatment | 必要ResourceとActionの最小性を確認する計画。 |
| telemetryId | TEL-IAR12-004 |
| detectionId | DET-IAR12-004 |
| requiredFields/0 | principalId |
| requiredFields/1 | resourceId |
| requiredFields/2 | action |
| requiredFields/3 | policyRevision |
| requiredFields/4 | graphRevision |
| requiredFields/5 | outcome |
| requiredFields/6 | eventTime |
| requiredFields/7 | correlationId |
| detectionStatus | planned-not-tested |
| owner | SYNTH-IDENTITY-OWNER |
| reassessmentId | REA-IAR12-004 |

## findings FND-IAR12-005

| Field | Value |
|---|---|
| id | FND-IAR12-005 |
| pathId | PTH-IAR12-005 |
| status | teaching-analysis-not-production-finding |
| risk | 特定の必要委任条件が不成立。他経路の不存在は不明。 |
| treatment | 否定条件の版と代替経路のGapを保持する。 |
| telemetryId | TEL-IAR12-005 |
| detectionId | DET-IAR12-005 |
| requiredFields/0 | principalId |
| requiredFields/1 | resourceId |
| requiredFields/2 | action |
| requiredFields/3 | policyRevision |
| requiredFields/4 | graphRevision |
| requiredFields/5 | outcome |
| requiredFields/6 | eventTime |
| requiredFields/7 | correlationId |
| detectionStatus | planned-not-tested |
| owner | SYNTH-IDENTITY-OWNER |
| reassessmentId | REA-IAR12-005 |

## findings FND-IAR12-006

| Field | Value |
|---|---|
| id | FND-IAR12-006 |
| pathId | PTH-IAR12-006 |
| status | teaching-analysis-not-production-finding |
| risk | Deviceのbinding不足。許可にも安全にも昇格しない。 |
| treatment | 追加資料と責任者を要求しUnknownを保持する。 |
| telemetryId | TEL-IAR12-006 |
| detectionId | DET-IAR12-006 |
| requiredFields/0 | principalId |
| requiredFields/1 | resourceId |
| requiredFields/2 | action |
| requiredFields/3 | policyRevision |
| requiredFields/4 | graphRevision |
| requiredFields/5 | outcome |
| requiredFields/6 | eventTime |
| requiredFields/7 | correlationId |
| detectionStatus | planned-not-tested |
| owner | SYNTH-IDENTITY-OWNER |
| reassessmentId | REA-IAR12-006 |

## handoffs HOF-IAR12-001

| Field | Value |
|---|---|
| id | HOF-IAR12-001 |
| chapter | 11 |
| status | planned-not-delivered |
| pathIds/0 | PTH-IAR12-001 |
| pathIds/1 | PTH-IAR12-002 |
| pathIds/2 | PTH-IAR12-003 |
| pathIds/3 | PTH-IAR12-004 |
| pathIds/4 | PTH-IAR12-005 |
| pathIds/5 | PTH-IAR12-006 |
| inputRequirement | AuthN/AuthZ/resource/action/conditionsの概念対応。独立CaseのEvidenceは流用しない。 |
| executionAuthorized | false |

## handoffs HOF-IAR12-002

| Field | Value |
|---|---|
| id | HOF-IAR12-002 |
| chapter | 13 |
| status | planned-not-delivered |
| pathIds/0 | PTH-IAR12-001 |
| pathIds/1 | PTH-IAR12-002 |
| pathIds/2 | PTH-IAR12-003 |
| pathIds/3 | PTH-IAR12-004 |
| pathIds/4 | PTH-IAR12-005 |
| pathIds/5 | PTH-IAR12-006 |
| inputRequirement | WorkloadとControl planeのOwnerとbindingの不足条件。 |
| executionAuthorized | false |

## handoffs HOF-IAR12-003

| Field | Value |
|---|---|
| id | HOF-IAR12-003 |
| chapter | 14 |
| status | planned-not-delivered |
| pathIds/0 | PTH-IAR12-001 |
| pathIds/1 | PTH-IAR12-002 |
| pathIds/2 | PTH-IAR12-003 |
| pathIds/3 | PTH-IAR12-004 |
| pathIds/4 | PTH-IAR12-005 |
| pathIds/5 | PTH-IAR12-006 |
| inputRequirement | 必要条件一つに限定した問い、否定条件、最小Evidenceと停止。 |
| executionAuthorized | false |

## handoffs HOF-IAR12-004

| Field | Value |
|---|---|
| id | HOF-IAR12-004 |
| chapter | 16 |
| status | planned-not-delivered |
| pathIds/0 | PTH-IAR12-001 |
| pathIds/1 | PTH-IAR12-002 |
| pathIds/2 | PTH-IAR12-003 |
| pathIds/3 | PTH-IAR12-004 |
| pathIds/4 | PTH-IAR12-005 |
| pathIds/5 | PTH-IAR12-006 |
| inputRequirement | Principal/Resource/Action/版/期間/相関keyと収集・保持のGap。 |
| executionAuthorized | false |

## handoffs HOF-IAR12-005

| Field | Value |
|---|---|
| id | HOF-IAR12-005 |
| chapter | 17 |
| status | planned-not-delivered |
| pathIds/0 | PTH-IAR12-001 |
| pathIds/1 | PTH-IAR12-002 |
| pathIds/2 | PTH-IAR12-003 |
| pathIds/3 | PTH-IAR12-004 |
| pathIds/4 | PTH-IAR12-005 |
| pathIds/5 | PTH-IAR12-006 |
| inputRequirement | 許容結論と未観測範囲を持つ合成Test計画。実検知率は未測定。 |
| executionAuthorized | false |

## limits

| Field | Value |
|---|---|
| mode | non-executing-synthetic-record-review |
| credentialMaterial | none |
| networkRequests | 0 |
| authenticationAttempts | 0 |
| minutes | 30 |
| outputBytes | 65536 |
| stop | unknown-authority-or-input-or-boundary; stop-and-record-gap |
| cleanup | remove-only-owned-working-copies; retain-canonical-sources |
| cleanupStatus | not-executed |
| custodian | SYNTH-EVIDENCE-CUSTODIAN |
| retentionHours | 24 |
| retentionStarts | hypothetical-session-end |
| assurance | no-real-authentication-or-measurement-or-legal-assurance |
| pathCoverage | six-supplied-paths-only; no-global-reachability-claim |
| parentDisposition | Do not proceed |

## 終了とHandoff

これは授業用の記録比較で、親RoEはDo not proceedのままです。六つのPath、必要条件、Evidence参照、反証またはGap、Owner、期限を記入できれば教材上の提出物になります。実行許可の不足を埋めたことにはなりません。

第11/13/14/16/17章へのHandoffはplanned-not-delivered、Detectionはplanned-not-testedです。実施・受領・改修・検知率を捏造しません。自分の作業コピーだけを整理し、正本と親記録を変更しません。評価は第12章の五観点Rubricを使い、根拠のない状態昇格や実Data混入は得点にかかわらず差し戻します。
