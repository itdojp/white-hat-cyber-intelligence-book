# 第10章 完全合成記入例：Attack Surface Register

## Caseの位置付け

本記録は`CASE-2026-001`をrefineする`ART-19 / ASR-2026-010`です。九つの合成資料から六つの候補を整理した完全記入例で、実対象の収集・観測・認証・所有確認を実施した記録ではありません。Sourceの時刻、申告者、取得方法も作成者の仮定です。

親`ROE-2026-009 v1`はDraft / Do not proceed、親Authorityは2026-08-19T09:00:00Zで失効しています。元の8月6日Window、RoE三Object、Open条件、TMのNeeds Evidenceを変更しません。新しいAsset候補はRoE Scopeへ追加されず、全候補の次Actionはrecord-only / nextActionAuthorization=falseです。第11章CASE-2026-011は独立のままです。

## 判断と代替説明

- CAND-ASR10-001: billing-bridge.exampleは、供給InventoryとOwner statementが親ASSET-2026-001に一致します。教材内限定でOwner confirmed / Highです。実際の現所有・稼働・実施許可は確認していません。
- CAND-ASR10-002: CTのPrecertificateとそのmirrorは原典が一つです。二資料を独立した裏付けに数えずCandidate / Unverified / Lowとします。最終CertificateやDeploymentの有無は不明です。
- CAND-ASR10-003: 廃止済みと申告された過去DNSの名前です。現在の状態は分からないためUnknown / Historical / Lowとし、名前の再利用も代替説明に残します。
- CAND-ASR10-004: 同名のCodeは別組織の資料です。このCaseへの接続をRejectedとしますが、Source自体を消去しません。
- CAND-ASR10-005: 所有者未記録のSaaSはUnknown / Unverified / Lowです。Shadow ITは仮説であり、承認済みInventoryの登録漏れも考えられます。
- CAND-ASR10-006: Packageの名前を二つの独立した合成申告で補強しても、所有者は未確認です。Corroborated / Unverified / Mediumとし、Dependencyへの許可を発行しません。

確認事実は「提供された文に何が記載されているか」、分析判断は上の限定State、仮定は供給資料の出所・時刻・申告者です。将来の稼働や攻撃を予測する記録ではありません。推奨は不足EvidenceをOwnerへ戻すことだけで、実収集を開始する指示ではありません。全候補にGap、責任者、期限、再評価Triggerを残します。

## 完全Field記録の読み方

以下は[Register JSON](fixtures/ch10-attack-surface.json)と[Source bundle JSON](fixtures/ch10-source-bundle.json)の全末端Fieldです。配列番号は1起点で、各見出しのGroupとField / Valueを合わせて一つのPathを識別します。空配列やnullも省略しません。機械検査は順序と全Fieldの一致を共有Publication Projection経由で確認します。

`contentSha256`の対象は同じSource IDに対応するbundleのcontent文字列をUTF-8化したbyteだけです。囲んだJSON全体、実Sourceの真正性、署名、実施許可のHashではありません。個別ファイルの配布byte一致は出版QAで別に検査します。[Schema](../schemas/ch10-attack-surface.schema.json)は二JSONをregister / bundleに束ねた論理入力の形を定義します。

## register/schemaVersion

このGroupの供給Fieldを省略せず記録します。

| register/schemaVersion Field | Value |
|---|---|
| schemaVersion | `1.0.0` |

## register/modelVersion

このGroupの供給Fieldを省略せず記録します。

| register/modelVersion Field | Value |
|---|---|
| modelVersion | `1.0.0` |

## register/synthetic

このGroupの供給Fieldを省略せず記録します。

| register/synthetic Field | Value |
|---|---|
| synthetic | `true` |

## register/executionAuthorized

このGroupの供給Fieldを省略せず記録します。

| register/executionAuthorized Field | Value |
|---|---|
| executionAuthorized | `false` |

## register/record

このGroupの供給Fieldを省略せず記録します。

| register/record Field | Value |
|---|---|
| artifactId | `ART-19` |
| registerId | `ASR-2026-010` |
| version | `1` |
| asOf | `2026-09-14T01:00:00Z` |
| status | `analysis-complete-with-gaps` |
| collectionRequirementId | `CR-ASR10-001` |
| question | `Which supplied candidates can be linked to the parent asset set, and which evidence or approval remains missing?` |
| owner | `SYNTH-DECISION-OWNER` |
| decisionId | `DEC-ASR10-001` |
| decision | `record-only; Do not proceed with operational actions` |
| decisionUseful | `not-assessed-for-historical-deadline` |

## register/parents

このGroupの供給Fieldを省略せず記録します。

| register/parents Field | Value |
|---|---|
| caseId | `CASE-2026-001` |
| relation | `refines` |
| decisionRequirementId | `DR-2026-001` |
| historicalDeadline | `2026-07-22T00:00:00Z` |
| authorizationId | `AUTH-CASE-2026-001` |
| authorizationExpiresAt | `2026-08-19T09:00:00Z` |
| authorizationWindow / 1 | `2026-08-06T00:00:00Z` |
| authorizationWindow / 2 | `2026-08-06T08:00:00Z` |
| authorizationConditions / 1 | `COND-AUTH-2026-001 Open` |
| authorizationConditions / 2 | `COND-AUTH-2026-002 Satisfied` |
| authorizationConditions / 3 | `COND-AUTH-2026-003 Open` |
| roeId | `ROE-2026-009` |
| roeVersion | `1` |
| roeStatus | `Draft` |
| roeObjectIds / 1 | `OBJ-ROE09-CONFIG` |
| roeObjectIds / 2 | `OBJ-ROE09-EVENT` |
| roeObjectIds / 3 | `OBJ-ROE09-POLICY` |
| roeExecutionAuthorized | `false` |
| threatModelId | `TM-2026-001` |
| threatModelStatus | `Needs Evidence` |
| parentReassessmentId | `REA-2026-001` |
| independentCaseId | `CASE-2026-011` |
| parentStateChanged | `false` |

## register/learnerPlan

このGroupの供給Fieldを省略せず記録します。

| register/learnerPlan Field | Value |
|---|---|
| collectionClass | `Passive` |
| actions / 1 | `read-supplied-json` |
| actions / 2 | `compare-synthetic-fields` |
| actions / 3 | `write-bounded-summary` |
| networkRequests | `0` |
| authenticationAttempts | `0` |
| rateTests | `0` |
| inputSourceIds / 1 | `OSRC-ASR10-001` |
| inputSourceIds / 2 | `OSRC-ASR10-002` |
| inputSourceIds / 3 | `OSRC-ASR10-003` |
| inputSourceIds / 4 | `OSRC-ASR10-004` |
| inputSourceIds / 5 | `OSRC-ASR10-005` |
| inputSourceIds / 6 | `OSRC-ASR10-006` |
| inputSourceIds / 7 | `OSRC-ASR10-007` |
| inputSourceIds / 8 | `OSRC-ASR10-008` |
| inputSourceIds / 9 | `OSRC-ASR10-009` |
| maximumSources | `9` |
| maximumCandidates | `6` |
| summaryBytes | `65536` |
| minutes | `30` |
| onUnexpectedData | `stop-without-copying-and-record-gap` |
| cleanup | `remove-only-owned-working-copies; retain-canonical-sources` |
| cleanupStatus | `not-executed` |
| retentionHours | `24` |
| retentionStarts | `hypothetical-session-end` |
| cleanupOwner | `SYNTH-EVIDENCE-CUSTODIAN` |

## register/sources

このGroupの供給Fieldを省略せず記録します。

| register/sources Field | Value |
|---|---|
| 1 / sourceId | `OSRC-ASR10-001` |
| 1 / provenanceId | `PROV-ASR10-001` |
| 1 / candidateId | `CAND-ASR10-001` |
| 1 / sourceClass | `First-party inventory` |
| 1 / originalCollectionClass | `Authenticated` |
| 1 / acquisitionMethod | `authored-inventory-export` |
| 1 / originalOriginId | `ORIGIN-ASR10-001` |
| 1 / derivedFromSourceId | `null` |
| 1 / publisherRole | `SYNTH-SOURCE-PUBLISHER` |
| 1 / observedAt | `2026-09-14T00:00:00Z` |
| 1 / acquiredAt | `2026-09-14T00:30:00Z` |
| 1 / timestampBasis | `authored-synthetic-assumption-not-clock-measurement` |
| 1 / contentSha256 | `92cff8a6cbc3e07ac93830abe41b4098887e39629ba67b9d29dbe6a1a7f1b677` |
| 1 / hashScope | `UTF-8 bytes of matching bundle content string; no normalization` |
| 1 / transformation | `authored-summary; no real acquisition` |
| 1 / termsNote | `supplied synthetic teaching copy only; not external-source permission` |
| 1 / dataClass | `synthetic-only` |
| 1 / credentialMaterial | `none` |
| 1 / personalDataFields | `[]` |
| 1 / custodian | `SYNTH-EVIDENCE-CUSTODIAN` |
| 1 / limitation | `source statement only; no current deployment, ownership or authorization proof` |
| 2 / sourceId | `OSRC-ASR10-002` |
| 2 / provenanceId | `PROV-ASR10-002` |
| 2 / candidateId | `CAND-ASR10-002` |
| 2 / sourceClass | `Certificate Transparency` |
| 2 / originalCollectionClass | `Passive` |
| 2 / acquisitionMethod | `authored-ct-snapshot` |
| 2 / originalOriginId | `ORIGIN-ASR10-002` |
| 2 / derivedFromSourceId | `null` |
| 2 / publisherRole | `SYNTH-SOURCE-PUBLISHER` |
| 2 / observedAt | `2026-09-14T00:00:00Z` |
| 2 / acquiredAt | `2026-09-14T00:30:00Z` |
| 2 / timestampBasis | `authored-synthetic-assumption-not-clock-measurement` |
| 2 / contentSha256 | `21958fbf91a4516b0adfaf1c652fa50c45e0ad78b5f69e7a20b1af70756d375e` |
| 2 / hashScope | `UTF-8 bytes of matching bundle content string; no normalization` |
| 2 / transformation | `authored-summary; no real acquisition` |
| 2 / termsNote | `supplied synthetic teaching copy only; not external-source permission` |
| 2 / dataClass | `synthetic-only` |
| 2 / credentialMaterial | `none` |
| 2 / personalDataFields | `[]` |
| 2 / custodian | `SYNTH-EVIDENCE-CUSTODIAN` |
| 2 / limitation | `source statement only; no current deployment, ownership or authorization proof` |
| 3 / sourceId | `OSRC-ASR10-003` |
| 3 / provenanceId | `PROV-ASR10-003` |
| 3 / candidateId | `CAND-ASR10-003` |
| 3 / sourceClass | `Archived DNS` |
| 3 / originalCollectionClass | `Passive` |
| 3 / acquisitionMethod | `authored-dns-archive` |
| 3 / originalOriginId | `ORIGIN-ASR10-003` |
| 3 / derivedFromSourceId | `null` |
| 3 / publisherRole | `SYNTH-SOURCE-PUBLISHER` |
| 3 / observedAt | `2025-01-10T00:00:00Z` |
| 3 / acquiredAt | `2026-09-14T00:30:00Z` |
| 3 / timestampBasis | `authored-synthetic-assumption-not-clock-measurement` |
| 3 / contentSha256 | `4b4d80595248d9ee4fee2a806ff76e2a6d90c1494cca7dcc40ad2b2031994eab` |
| 3 / hashScope | `UTF-8 bytes of matching bundle content string; no normalization` |
| 3 / transformation | `authored-summary; no real acquisition` |
| 3 / termsNote | `supplied synthetic teaching copy only; not external-source permission` |
| 3 / dataClass | `synthetic-only` |
| 3 / credentialMaterial | `none` |
| 3 / personalDataFields | `[]` |
| 3 / custodian | `SYNTH-EVIDENCE-CUSTODIAN` |
| 3 / limitation | `source statement only; no current deployment, ownership or authorization proof` |
| 4 / sourceId | `OSRC-ASR10-004` |
| 4 / provenanceId | `PROV-ASR10-004` |
| 4 / candidateId | `CAND-ASR10-004` |
| 4 / sourceClass | `Public code` |
| 4 / originalCollectionClass | `Passive` |
| 4 / acquisitionMethod | `authored-code-summary` |
| 4 / originalOriginId | `ORIGIN-ASR10-004` |
| 4 / derivedFromSourceId | `null` |
| 4 / publisherRole | `SYNTH-OTHER-ORG` |
| 4 / observedAt | `2026-09-14T00:00:00Z` |
| 4 / acquiredAt | `2026-09-14T00:30:00Z` |
| 4 / timestampBasis | `authored-synthetic-assumption-not-clock-measurement` |
| 4 / contentSha256 | `21dfdd67b8f926aec5b93bd2f3497c5d0aaf0c260ffd9c051aef4696f5a97434` |
| 4 / hashScope | `UTF-8 bytes of matching bundle content string; no normalization` |
| 4 / transformation | `authored-summary; no real acquisition` |
| 4 / termsNote | `supplied synthetic teaching copy only; not external-source permission` |
| 4 / dataClass | `synthetic-only` |
| 4 / credentialMaterial | `none` |
| 4 / personalDataFields | `[]` |
| 4 / custodian | `SYNTH-EVIDENCE-CUSTODIAN` |
| 4 / limitation | `source statement only; no current deployment, ownership or authorization proof` |
| 5 / sourceId | `OSRC-ASR10-005` |
| 5 / provenanceId | `PROV-ASR10-005` |
| 5 / candidateId | `CAND-ASR10-005` |
| 5 / sourceClass | `SaaS inventory` |
| 5 / originalCollectionClass | `Authenticated` |
| 5 / acquisitionMethod | `authored-saas-export` |
| 5 / originalOriginId | `ORIGIN-ASR10-005` |
| 5 / derivedFromSourceId | `null` |
| 5 / publisherRole | `SYNTH-SOURCE-PUBLISHER` |
| 5 / observedAt | `2026-09-14T00:00:00Z` |
| 5 / acquiredAt | `2026-09-14T00:30:00Z` |
| 5 / timestampBasis | `authored-synthetic-assumption-not-clock-measurement` |
| 5 / contentSha256 | `40476da434b9eeea1b3fb3640d2e39917acb069fa931eaac9862dfa30065902b` |
| 5 / hashScope | `UTF-8 bytes of matching bundle content string; no normalization` |
| 5 / transformation | `authored-summary; no real acquisition` |
| 5 / termsNote | `supplied synthetic teaching copy only; not external-source permission` |
| 5 / dataClass | `synthetic-only` |
| 5 / credentialMaterial | `none` |
| 5 / personalDataFields | `[]` |
| 5 / custodian | `SYNTH-EVIDENCE-CUSTODIAN` |
| 5 / limitation | `source statement only; no current deployment, ownership or authorization proof` |
| 6 / sourceId | `OSRC-ASR10-006` |
| 6 / provenanceId | `PROV-ASR10-006` |
| 6 / candidateId | `CAND-ASR10-006` |
| 6 / sourceClass | `Package metadata` |
| 6 / originalCollectionClass | `Passive` |
| 6 / acquisitionMethod | `authored-package-summary` |
| 6 / originalOriginId | `ORIGIN-ASR10-006` |
| 6 / derivedFromSourceId | `null` |
| 6 / publisherRole | `SYNTH-SOURCE-PUBLISHER` |
| 6 / observedAt | `2026-09-14T00:00:00Z` |
| 6 / acquiredAt | `2026-09-14T00:30:00Z` |
| 6 / timestampBasis | `authored-synthetic-assumption-not-clock-measurement` |
| 6 / contentSha256 | `5387ce2d7cfc0817cfd07e1b40f5c5789e224e4be5710efa36cec010c644b845` |
| 6 / hashScope | `UTF-8 bytes of matching bundle content string; no normalization` |
| 6 / transformation | `authored-summary; no real acquisition` |
| 6 / termsNote | `supplied synthetic teaching copy only; not external-source permission` |
| 6 / dataClass | `synthetic-only` |
| 6 / credentialMaterial | `none` |
| 6 / personalDataFields | `[]` |
| 6 / custodian | `SYNTH-EVIDENCE-CUSTODIAN` |
| 6 / limitation | `source statement only; no current deployment, ownership or authorization proof` |
| 7 / sourceId | `OSRC-ASR10-007` |
| 7 / provenanceId | `PROV-ASR10-007` |
| 7 / candidateId | `CAND-ASR10-006` |
| 7 / sourceClass | `Response metadata` |
| 7 / originalCollectionClass | `Active` |
| 7 / acquisitionMethod | `authored-response-summary` |
| 7 / originalOriginId | `ORIGIN-ASR10-007` |
| 7 / derivedFromSourceId | `null` |
| 7 / publisherRole | `SYNTH-SOURCE-PUBLISHER` |
| 7 / observedAt | `2026-09-14T00:00:00Z` |
| 7 / acquiredAt | `2026-09-14T00:30:00Z` |
| 7 / timestampBasis | `authored-synthetic-assumption-not-clock-measurement` |
| 7 / contentSha256 | `337c5f8a0309ab81794fe3d2ba298a34fb6eb7d90d88513b984edecd4d864e42` |
| 7 / hashScope | `UTF-8 bytes of matching bundle content string; no normalization` |
| 7 / transformation | `authored-summary; no real acquisition` |
| 7 / termsNote | `supplied synthetic teaching copy only; not external-source permission` |
| 7 / dataClass | `synthetic-only` |
| 7 / credentialMaterial | `none` |
| 7 / personalDataFields | `[]` |
| 7 / custodian | `SYNTH-EVIDENCE-CUSTODIAN` |
| 7 / limitation | `source statement only; no current deployment, ownership or authorization proof` |
| 8 / sourceId | `OSRC-ASR10-008` |
| 8 / provenanceId | `PROV-ASR10-008` |
| 8 / candidateId | `CAND-ASR10-001` |
| 8 / sourceClass | `Owner statement` |
| 8 / originalCollectionClass | `Authenticated` |
| 8 / acquisitionMethod | `authored-owner-declaration` |
| 8 / originalOriginId | `ORIGIN-ASR10-008` |
| 8 / derivedFromSourceId | `null` |
| 8 / publisherRole | `SYNTH-SOURCE-PUBLISHER` |
| 8 / observedAt | `2026-09-14T00:00:00Z` |
| 8 / acquiredAt | `2026-09-14T00:30:00Z` |
| 8 / timestampBasis | `authored-synthetic-assumption-not-clock-measurement` |
| 8 / contentSha256 | `43a2fc724d6a718dc735af824bac72521fa0ffde5dfbd67fb715d71259950747` |
| 8 / hashScope | `UTF-8 bytes of matching bundle content string; no normalization` |
| 8 / transformation | `authored-summary; no real acquisition` |
| 8 / termsNote | `supplied synthetic teaching copy only; not external-source permission` |
| 8 / dataClass | `synthetic-only` |
| 8 / credentialMaterial | `none` |
| 8 / personalDataFields | `[]` |
| 8 / custodian | `SYNTH-EVIDENCE-CUSTODIAN` |
| 8 / limitation | `source statement only; no current deployment, ownership or authorization proof` |
| 9 / sourceId | `OSRC-ASR10-009` |
| 9 / provenanceId | `PROV-ASR10-009` |
| 9 / candidateId | `CAND-ASR10-002` |
| 9 / sourceClass | `Third-party aggregator` |
| 9 / originalCollectionClass | `Passive` |
| 9 / acquisitionMethod | `authored-derived-summary` |
| 9 / originalOriginId | `ORIGIN-ASR10-002` |
| 9 / derivedFromSourceId | `OSRC-ASR10-002` |
| 9 / publisherRole | `SYNTH-SOURCE-PUBLISHER` |
| 9 / observedAt | `2026-09-14T00:00:00Z` |
| 9 / acquiredAt | `2026-09-14T00:30:00Z` |
| 9 / timestampBasis | `authored-synthetic-assumption-not-clock-measurement` |
| 9 / contentSha256 | `f64cc77775195657941ca068811501915b55687fe678df3e90201a181ec70b06` |
| 9 / hashScope | `UTF-8 bytes of matching bundle content string; no normalization` |
| 9 / transformation | `authored-summary; no real acquisition` |
| 9 / termsNote | `supplied synthetic teaching copy only; not external-source permission` |
| 9 / dataClass | `synthetic-only` |
| 9 / credentialMaterial | `none` |
| 9 / personalDataFields | `[]` |
| 9 / custodian | `SYNTH-EVIDENCE-CUSTODIAN` |
| 9 / limitation | `source statement only; no current deployment, ownership or authorization proof` |

## register/candidates

このGroupの供給Fieldを省略せず記録します。

| register/candidates Field | Value |
|---|---|
| 1 / candidateId | `CAND-ASR10-001` |
| 1 / type | `Service` |
| 1 / locator | `billing-bridge.example` |
| 1 / sourceIds / 1 | `OSRC-ASR10-001` |
| 1 / sourceIds / 2 | `OSRC-ASR10-008` |
| 1 / candidateOwner | `SYNTH-BUSINESS-SYSTEMS` |
| 1 / ownershipStatus | `Confirmed owned` |
| 1 / ownershipConfidence | `High` |
| 1 / verificationStatus | `Owner confirmed` |
| 1 / ownerEvidenceSourceIds / 1 | `OSRC-ASR10-001` |
| 1 / ownerEvidenceSourceIds / 2 | `OSRC-ASR10-008` |
| 1 / parentAssetId | `ASSET-2026-001` |
| 1 / exposure | `not-measured` |
| 1 / dependency | `not-established` |
| 1 / thirdPartyStatus | `not-indicated-in-supplied-case` |
| 1 / evidenceId | `EVD-ASR10-001` |
| 1 / evidenceBasis | `authored-source-comparison-not-observation` |
| 1 / judgment | `supplied inventory and owner statement agree within the authored case` |
| 1 / alternative | `owner statement may be outdated outside the fixed exercise` |
| 1 / gapId | `GAP-ASR10-001` |
| 1 / gap | `current authority and scope remain missing` |
| 1 / gapOwner | `SYNTH-ASSET-REVIEW-OWNER` |
| 1 / dueAt | `2026-09-15T00:00:00Z` |
| 1 / reassessmentId | `REA-ASR10-001` |
| 1 / reassessmentTrigger | `source, owner, time or authority evidence changes` |
| 1 / nextAction | `record-only` |
| 1 / nextActionAuthorization | `false` |
| 1 / requiredApproval / 1 | `new-current-authorization` |
| 1 / requiredApproval / 2 | `exact-asset-operation-time-scope` |
| 1 / requiredApproval / 3 | `system-and-data-owner-review` |
| 1 / requiredApproval / 4 | `third-party-terms-review` |
| 1 / stopReason | `parent authority expired; no operational scope for new candidate` |
| 2 / candidateId | `CAND-ASR10-002` |
| 2 / type | `Domain` |
| 2 / locator | `preview.billing-bridge.example` |
| 2 / sourceIds / 1 | `OSRC-ASR10-002` |
| 2 / sourceIds / 2 | `OSRC-ASR10-009` |
| 2 / candidateOwner | `Unknown` |
| 2 / ownershipStatus | `Unverified` |
| 2 / ownershipConfidence | `Low` |
| 2 / verificationStatus | `Candidate` |
| 2 / ownerEvidenceSourceIds | `[]` |
| 2 / parentAssetId | `null` |
| 2 / exposure | `not-measured` |
| 2 / dependency | `not-established` |
| 2 / thirdPartyStatus | `possible-unverified` |
| 2 / evidenceId | `EVD-ASR10-002` |
| 2 / evidenceBasis | `authored-source-comparison-not-observation` |
| 2 / judgment | `CT intent remains a candidate; mirror is not corroboration` |
| 2 / alternative | `precertificate may never lead to deployment` |
| 2 / gapId | `GAP-ASR10-002` |
| 2 / gap | `ownership and deployment remain unknown` |
| 2 / gapOwner | `SYNTH-ASSET-REVIEW-OWNER` |
| 2 / dueAt | `2026-09-15T00:00:00Z` |
| 2 / reassessmentId | `REA-ASR10-002` |
| 2 / reassessmentTrigger | `source, owner, time or authority evidence changes` |
| 2 / nextAction | `record-only` |
| 2 / nextActionAuthorization | `false` |
| 2 / requiredApproval / 1 | `new-current-authorization` |
| 2 / requiredApproval / 2 | `exact-asset-operation-time-scope` |
| 2 / requiredApproval / 3 | `system-and-data-owner-review` |
| 2 / requiredApproval / 4 | `third-party-terms-review` |
| 2 / stopReason | `parent authority expired; no operational scope for new candidate` |
| 3 / candidateId | `CAND-ASR10-003` |
| 3 / type | `Domain` |
| 3 / locator | `retired.billing-bridge.example` |
| 3 / sourceIds / 1 | `OSRC-ASR10-003` |
| 3 / candidateOwner | `Unknown` |
| 3 / ownershipStatus | `Historical` |
| 3 / ownershipConfidence | `Low` |
| 3 / verificationStatus | `Unknown` |
| 3 / ownerEvidenceSourceIds | `[]` |
| 3 / parentAssetId | `null` |
| 3 / exposure | `not-measured` |
| 3 / dependency | `not-established` |
| 3 / thirdPartyStatus | `possible-unverified` |
| 3 / evidenceId | `EVD-ASR10-003` |
| 3 / evidenceBasis | `authored-source-comparison-not-observation` |
| 3 / judgment | `historical record cannot settle present ownership or operation` |
| 3 / alternative | `retired service name may have been reassigned` |
| 3 / gapId | `GAP-ASR10-003` |
| 3 / gap | `current ownership and service state remain unknown` |
| 3 / gapOwner | `SYNTH-ASSET-REVIEW-OWNER` |
| 3 / dueAt | `2026-09-15T00:00:00Z` |
| 3 / reassessmentId | `REA-ASR10-003` |
| 3 / reassessmentTrigger | `source, owner, time or authority evidence changes` |
| 3 / nextAction | `record-only` |
| 3 / nextActionAuthorization | `false` |
| 3 / requiredApproval / 1 | `new-current-authorization` |
| 3 / requiredApproval / 2 | `exact-asset-operation-time-scope` |
| 3 / requiredApproval / 3 | `system-and-data-owner-review` |
| 3 / requiredApproval / 4 | `third-party-terms-review` |
| 3 / stopReason | `parent authority expired; no operational scope for new candidate` |
| 4 / candidateId | `CAND-ASR10-004` |
| 4 / type | `Repository` |
| 4 / locator | `code.other-org.example/billing-bridge` |
| 4 / sourceIds / 1 | `OSRC-ASR10-004` |
| 4 / candidateOwner | `SYNTH-OTHER-ORG` |
| 4 / ownershipStatus | `Third party` |
| 4 / ownershipConfidence | `High` |
| 4 / verificationStatus | `Rejected` |
| 4 / ownerEvidenceSourceIds | `[]` |
| 4 / parentAssetId | `null` |
| 4 / exposure | `not-measured` |
| 4 / dependency | `not-established` |
| 4 / thirdPartyStatus | `confirmed-third-party` |
| 4 / evidenceId | `EVD-ASR10-004` |
| 4 / evidenceBasis | `authored-source-comparison-not-observation` |
| 4 / judgment | `same-name other organization is excluded from this parent asset set` |
| 4 / alternative | `name similarity may be coincidental` |
| 4 / gapId | `GAP-ASR10-004` |
| 4 / gap | `no evidence of relationship to this parent case` |
| 4 / gapOwner | `SYNTH-ASSET-REVIEW-OWNER` |
| 4 / dueAt | `2026-09-15T00:00:00Z` |
| 4 / reassessmentId | `REA-ASR10-004` |
| 4 / reassessmentTrigger | `source, owner, time or authority evidence changes` |
| 4 / nextAction | `record-only` |
| 4 / nextActionAuthorization | `false` |
| 4 / requiredApproval / 1 | `new-current-authorization` |
| 4 / requiredApproval / 2 | `exact-asset-operation-time-scope` |
| 4 / requiredApproval / 3 | `system-and-data-owner-review` |
| 4 / requiredApproval / 4 | `third-party-terms-review` |
| 4 / stopReason | `parent authority expired; no operational scope for new candidate` |
| 5 / candidateId | `CAND-ASR10-005` |
| 5 / type | `SaaS` |
| 5 / locator | `shadow-workspace.example` |
| 5 / sourceIds / 1 | `OSRC-ASR10-005` |
| 5 / candidateOwner | `Unknown` |
| 5 / ownershipStatus | `Unverified` |
| 5 / ownershipConfidence | `Low` |
| 5 / verificationStatus | `Unknown` |
| 5 / ownerEvidenceSourceIds | `[]` |
| 5 / parentAssetId | `null` |
| 5 / exposure | `not-measured` |
| 5 / dependency | `not-established` |
| 5 / thirdPartyStatus | `possible-unverified` |
| 5 / evidenceId | `EVD-ASR10-005` |
| 5 / evidenceBasis | `authored-source-comparison-not-observation` |
| 5 / judgment | `Shadow IT is a hypothesis, not a finding of unauthorized use` |
| 5 / alternative | `sanctioned but incomplete inventory is also possible` |
| 5 / gapId | `GAP-ASR10-005` |
| 5 / gap | `approved inventory and accountable owner remain unknown` |
| 5 / gapOwner | `SYNTH-ASSET-REVIEW-OWNER` |
| 5 / dueAt | `2026-09-15T00:00:00Z` |
| 5 / reassessmentId | `REA-ASR10-005` |
| 5 / reassessmentTrigger | `source, owner, time or authority evidence changes` |
| 5 / nextAction | `record-only` |
| 5 / nextActionAuthorization | `false` |
| 5 / requiredApproval / 1 | `new-current-authorization` |
| 5 / requiredApproval / 2 | `exact-asset-operation-time-scope` |
| 5 / requiredApproval / 3 | `system-and-data-owner-review` |
| 5 / requiredApproval / 4 | `third-party-terms-review` |
| 5 / stopReason | `parent authority expired; no operational scope for new candidate` |
| 6 / candidateId | `CAND-ASR10-006` |
| 6 / type | `Package` |
| 6 / locator | `registry.packages.example/billing-helper` |
| 6 / sourceIds / 1 | `OSRC-ASR10-006` |
| 6 / sourceIds / 2 | `OSRC-ASR10-007` |
| 6 / candidateOwner | `Unknown` |
| 6 / ownershipStatus | `Unverified` |
| 6 / ownershipConfidence | `Medium` |
| 6 / verificationStatus | `Corroborated` |
| 6 / ownerEvidenceSourceIds | `[]` |
| 6 / parentAssetId | `null` |
| 6 / exposure | `not-measured` |
| 6 / dependency | `supplier-sdk.example` |
| 6 / thirdPartyStatus | `possible-unverified` |
| 6 / evidenceId | `EVD-ASR10-006` |
| 6 / evidenceBasis | `authored-source-comparison-not-observation` |
| 6 / judgment | `two independent authored statements agree on package label, not ownership` |
| 6 / alternative | `both statements may rely on incomplete publisher claims` |
| 6 / gapId | `GAP-ASR10-006` |
| 6 / gap | `package ownership and dependency permission remain unknown` |
| 6 / gapOwner | `SYNTH-ASSET-REVIEW-OWNER` |
| 6 / dueAt | `2026-09-15T00:00:00Z` |
| 6 / reassessmentId | `REA-ASR10-006` |
| 6 / reassessmentTrigger | `source, owner, time or authority evidence changes` |
| 6 / nextAction | `record-only` |
| 6 / nextActionAuthorization | `false` |
| 6 / requiredApproval / 1 | `new-current-authorization` |
| 6 / requiredApproval / 2 | `exact-asset-operation-time-scope` |
| 6 / requiredApproval / 3 | `system-and-data-owner-review` |
| 6 / requiredApproval / 4 | `third-party-terms-review` |
| 6 / stopReason | `parent authority expired; no operational scope for new candidate` |

## register/handoffs

このGroupの供給Fieldを省略せず記録します。

| register/handoffs Field | Value |
|---|---|
| 1 / handoffId | `HOF-ASR10-001` |
| 1 / destination | `Chapters12-13` |
| 1 / candidateIds / 1 | `CAND-ASR10-001` |
| 1 / provenanceIds / 1 | `PROV-ASR10-001` |
| 1 / provenanceIds / 2 | `PROV-ASR10-008` |
| 1 / inputIds / 1 | `ASR-2026-010` |
| 1 / inputIds / 2 | `TM-2026-001` |
| 1 / inputIds / 3 | `ROE-2026-009 v1` |
| 1 / scope | `owner-confirmed teaching candidate only; not operational scope` |
| 1 / status | `planned-not-delivered` |
| 1 / executionAuthorized | `false` |
| 2 / handoffId | `HOF-ASR10-002` |
| 2 / destination | `Chapters23-24` |
| 2 / candidateIds / 1 | `CAND-ASR10-001` |
| 2 / candidateIds / 2 | `CAND-ASR10-002` |
| 2 / candidateIds / 3 | `CAND-ASR10-003` |
| 2 / candidateIds / 4 | `CAND-ASR10-004` |
| 2 / candidateIds / 5 | `CAND-ASR10-005` |
| 2 / candidateIds / 6 | `CAND-ASR10-006` |
| 2 / provenanceIds / 1 | `PROV-ASR10-001` |
| 2 / provenanceIds / 2 | `PROV-ASR10-002` |
| 2 / provenanceIds / 3 | `PROV-ASR10-003` |
| 2 / provenanceIds / 4 | `PROV-ASR10-004` |
| 2 / provenanceIds / 5 | `PROV-ASR10-005` |
| 2 / provenanceIds / 6 | `PROV-ASR10-006` |
| 2 / provenanceIds / 7 | `PROV-ASR10-007` |
| 2 / provenanceIds / 8 | `PROV-ASR10-008` |
| 2 / provenanceIds / 9 | `PROV-ASR10-009` |
| 2 / inputIds / 1 | `CR-ASR10-001` |
| 2 / inputIds / 2 | `ASR-2026-010` |
| 2 / scope | `source lineage, transformations, uncertainties and gaps; no new collection` |
| 2 / status | `planned-not-delivered` |
| 2 / executionAuthorized | `false` |

## register/limits

このGroupの供給Fieldを省略せず記録します。

| register/limits Field | Value |
|---|---|
| coverage | `nine supplied source summaries only; absence is not nonexistence` |
| verification | `finite authored evidence relationships; not source authenticity or legal judgment` |
| negativeFinding | `no global negative finding from this bounded bundle` |
| runtime | `no real acquisition, lookup, authentication, contact or observation` |

## bundle/schemaVersion

このGroupの供給Fieldを省略せず記録します。

| bundle/schemaVersion Field | Value |
|---|---|
| schemaVersion | `1.0.0` |

## bundle/bundleId

このGroupの供給Fieldを省略せず記録します。

| bundle/bundleId Field | Value |
|---|---|
| bundleId | `BUNDLE-ASR10-001` |

## bundle/synthetic

このGroupの供給Fieldを省略せず記録します。

| bundle/synthetic Field | Value |
|---|---|
| synthetic | `true` |

## bundle/acquisitionOccurred

このGroupの供給Fieldを省略せず記録します。

| bundle/acquisitionOccurred Field | Value |
|---|---|
| acquisitionOccurred | `false` |

## bundle/sources

このGroupの供給Fieldを省略せず記録します。

| bundle/sources Field | Value |
|---|---|
| 1 / sourceId | `OSRC-ASR10-001` |
| 1 / content | `Authored inventory: billing-bridge.example; parent ASSET-2026-001; declared owner SYNTH-BUSINESS-SYSTEMS; status listed.` |
| 2 / sourceId | `OSRC-ASR10-002` |
| 2 / content | `Authored CT metadata: precertificate for preview.billing-bridge.example; issuer intent only; final certificate issuance unknown.` |
| 3 / sourceId | `OSRC-ASR10-003` |
| 3 / content | `Authored archived DNS: RR owner retired.billing-bridge.example; CNAME legacy.supplier.example; observed 2025-01-10; current resolution unknown; inventory says retired.` |
| 4 / sourceId | `OSRC-ASR10-004` |
| 4 / content | `Authored public code summary: code.other-org.example/billing-bridge; owner SYNTH-OTHER-ORG; same name only; no relation to CASE-2026-001.` |
| 5 / sourceId | `OSRC-ASR10-005` |
| 5 / content | `Authored SaaS export summary: workspace shadow-workspace.example; owner not recorded; inventory membership unknown; no account or personal fields.` |
| 6 / sourceId | `OSRC-ASR10-006` |
| 6 / content | `Authored package metadata: registry.packages.example/billing-helper; dependency supplier-sdk.example; publisher ownership not verified.` |
| 7 / sourceId | `OSRC-ASR10-007` |
| 7 / content | `Authored response summary: package label billing-helper at packages-view.example; no real request or observation occurred.` |
| 8 / sourceId | `OSRC-ASR10-008` |
| 8 / content | `Authored owner statement: SYNTH-BUSINESS-SYSTEMS declares billing-bridge.example corresponds to ASSET-2026-001; limited to this supplied teaching record.` |
| 9 / sourceId | `OSRC-ASR10-009` |
| 9 / content | `Authored CT mirror summary: same precertificate as OSRC-ASR10-002; derived copy, not an independent origin.` |

## 受入と残る制限

記入はanalysis-complete-with-gapsですが、親の過去のDecision deadlineに間に合うかはnot-assessed-for-historical-deadlineです。第12〜13章への一候補、第23〜24章へのProvenanceのHandoffはいずれもplanned-not-deliveredで、実際に送付した証跡ではありません。

UnknownやRejectedを隠さず記録し、所有の根拠が変われば再評価します。九資料の外側の不存在や網羅性は主張しません。実環境、法的権限、Data真正性、隔離・削除・PII完全検出の保証は行いません。

[第10章](../manuscript/10-recon-osint-boundary.md)の安全条件とRubric、[ART-19 Template](../templates/attack-surface-register.md)、[Source Review Note](../references/ch10-source-review-2026-09-14.md)を併用してください。
