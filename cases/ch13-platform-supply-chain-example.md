# 第13章 完全合成記入例：Platform and Supply Chain Assessment

## この記入例の扱い

ART-21 / PSA-2026-013はCASE-2026-001をrefinesする非実行の教材です。全記録・時刻・Digest・Identity・判断は作成者が記述したもので、実Cloud、CI、Registry、Token、Package、Build、Deploymentの測定結果ではありません。Digestは合成ラベル由来で、実Artifactのbyte検証ではありません。

[第13章](../manuscript/13-platform-supply-chain.md)、[空Template](../templates/platform-supply-chain-assessment.md)、[正本JSON](fixtures/ch13-supply-chain.json)、[閉じたSchema](../schemas/ch13-supply-chain.schema.json)を参照します。以下はJSONの全末端Fieldと一対一のField/Value表です。添字は0始まりです。

## 読み方と対比

最初にparents、parentIdentity、safetyを読みます。親RoE Draft / Do not proceed / executionAuthorized=false、失効AUTH、元Window、三Objectを変更しません。第12章のcustomer-summary権限は本章のBuild/Deploy許可ではありません。独立CASE-2026-011のEvidenceも借用しません。

001はexpectationsと同一対象の有限比較が一致、002はmutable source、003はunversioned action、004はRunnerの過大権限、005はProvenance不足、006は宣言だけ、007は観測summaryだけ、008はRuntime Digest差異です。状態はDeclared / Observed / Verified / Rejected / Unknownで、全件をVerifiedに揃えません。

Signed、Trusted、Policy-compliant、Safeと実施許可は分離します。全署名はRecorded-unverified、実署名検証0、実Trustと標準適合は未評価です。001のVerifiedも本書独自summaryの比較だけであり、SPDX/SLSA準拠、実署名や実Buildの成功ではありません。既知の矛盾はRejected、矛盾がなく必要記録が不明ならUnknownです。

確認事実は供給Fieldだけ、分析判断はfinding、仮定はPlatformと時刻、推奨はTreatment計画です。正常な変更、資料遅延、不足を代替説明として保持し、版や資料が変われば再評価します。SourceからRuntimeまでをIDで辿り、Finding / Treatment / Owner / Decision / Reassessmentを読みます。

## 停止条件と評価

実Dataらしい内容、未知入力、外部接続、許可不明なら停止します。実Token、実Credential、実Registry、実CIは使用しません。自分の作業コピーだけを整理し、正本と親Evidenceを保持します。第13章の五観点Rubricを使い、根拠のない状態昇格、親記録変更、実Data混入は点数にかかわらず差し戻します。Handoffはplanned-not-deliveredです。

## schemaVersion

| Field | Value |
|---|---|
| schemaVersion | 1.0.0 |

## synthetic

| Field | Value |
|---|---|
| synthetic | true |

## record

| Field | Value |
|---|---|
| id | PSA-2026-013 |
| artifactId | ART-21 |
| caseId | CASE-2026-001 |
| relation | refines |
| serviceId | SVC-PSA13-001 |
| asOf | 2026-09-15T09:00:00Z |
| revision | PSA13-REV-001 |
| purpose | 供給されたSourceからRuntimeまでの記録の対応と、未確認の条件を区別する。 |
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

## parentIdentity

| Field | Value |
|---|---|
| reviewId | IAR-2026-012 |
| pathId | PTH-IAR12-004 |
| pathState | Validated |
| principalId | PRN-IAR12-004 |
| permission | read-customer-summary |
| signalFlowId | SF-2026-006 |
| threatId | TH-2026-004 |
| boundaryId | TB-2026-004 |
| currentBinding | Unknown |
| coverage | Unknown |
| nonFederationEvaluationId | EVAL-IAR12-005 |
| nonFederationAssertion/0 | null |
| nonFederationAssertion/1 | null |
| nonFederationAssertion/2 | null |
| use | background-gap-only-no-build-or-deploy-permission |

## safety

| Field | Value |
|---|---|
| executionAuthorized | false |
| externalConnections | 0 |
| actualBuilds | 0 |
| actualDeployments | 0 |
| actualSignatureVerifications | 0 |
| actualTrust | Not assessed |
| standardCompliance | Not assessed |
| safeClaim | false |
| secretValuesPresent | false |
| inputKind | authored-summary-only-not-standard-document |
| digestMeaning | sha256-of-authored-label-not-real-artifact |
| nextAction | record-only |
| stop | 実Dataらしい内容、未知の入力、外部接続、許可不明なら停止する。 |
| cleanup | 自分の作業コピーだけを整理し、正本と親Evidenceを保持する。 |
| durationMinutes | 30 |
| retentionHours | 24 |

## platform

| Field | Value |
|---|---|
| id | PLT-PSA13-001 |
| serviceId | SVC-PSA13-001 |
| businessPurpose | 架空の請求書連携の変更根拠を記録する。 |
| controlPlaneId | CP-PSA13-001 |
| dataPlaneId | DP-PSA13-001 |
| buildPlaneId | BP-PSA13-001 |
| runtimeBoundaryId | RB-PSA13-001 |
| saasIntegrationId | SAAS-PSA13-001 |
| saasScope | metadata-only-no-provider-access |
| owner | SYNTH-PLATFORM-OWNER |

## principals HUM-PSA13-001

| Field | Value |
|---|---|
| id | HUM-PSA13-001 |
| class | Human |
| permission | review-promotion-plan |
| secretClass | interactive-authenticator-class |
| owner | SYNTH-REVIEW-OWNER |
| secretClassId | SEC-PSA13-001 |

## principals WRK-PSA13-001

| Field | Value |
|---|---|
| id | WRK-PSA13-001 |
| class | Workload |
| permission | build-summary-only |
| secretClass | workload-authentication-class |
| owner | SYNTH-BUILD-OWNER |
| secretClassId | SEC-PSA13-002 |

## secretClasses SEC-PSA13-001

| Field | Value |
|---|---|
| id | SEC-PSA13-001 |
| principalId | HUM-PSA13-001 |
| secretClass | interactive-authenticator-class |
| valueIncluded | false |
| owner | SYNTH-REVIEW-OWNER |

## secretClasses SEC-PSA13-002

| Field | Value |
|---|---|
| id | SEC-PSA13-002 |
| principalId | WRK-PSA13-001 |
| secretClass | workload-authentication-class |
| valueIncluded | false |
| owner | SYNTH-BUILD-OWNER |

## expectations EXP-PSA13-001

| Field | Value |
|---|---|
| id | EXP-PSA13-001 |
| chainId | CHN-PSA13-001 |
| recordRevision | PSA13-REV-001 |
| sourceRevision | cad8efa6b5af487f26222c95a5f908b5daa8b7b4 |
| lockDigest | 1a85c55f15c449b3294f5e930d53c6dd316d4c80d3a395b84680848443fc7998 |
| artifactDigest | 9efdb1d2979cdb7429c6b0204e7351ac835a19498b7dac316f03503e6e687c87 |
| builderId | BLD-PSA13-001 |
| buildType | finite-summary-v1 |
| parameters | target=synthetic-summary |
| actionRevision | 91296223262f7a7f6d82352e0947f4786b203f6e |
| workloadPrincipalId | WRK-PSA13-001 |
| permission | build-summary-only |
| runnerClass | ephemeral-unprivileged |
| isolation | separate-build-runtime |
| network | deny-external |
| cache | reviewed-no-cross-run-state |
| expectedRuntimeBoundary | RB-PSA13-001 |
| trustBasis | author-supplied-expectation-not-real-root-of-trust |
| secretClassId | SEC-PSA13-002 |

## expectations EXP-PSA13-002

| Field | Value |
|---|---|
| id | EXP-PSA13-002 |
| chainId | CHN-PSA13-002 |
| recordRevision | PSA13-REV-001 |
| sourceRevision | 70b7f0245f128a1368c1758be35300512e5172f1 |
| lockDigest | 8fd6ad965fe15db3b80dcb63edbd05941faa48adab0f8594d73d3da3ef0c8b0f |
| artifactDigest | 28ef2aa48879e820e3f8cb272dbde6ef7421941e91b8cacc3ae9de98869ec543 |
| builderId | BLD-PSA13-001 |
| buildType | finite-summary-v1 |
| parameters | target=synthetic-summary |
| actionRevision | 91296223262f7a7f6d82352e0947f4786b203f6e |
| workloadPrincipalId | WRK-PSA13-001 |
| permission | build-summary-only |
| runnerClass | ephemeral-unprivileged |
| isolation | separate-build-runtime |
| network | deny-external |
| cache | reviewed-no-cross-run-state |
| expectedRuntimeBoundary | RB-PSA13-001 |
| trustBasis | author-supplied-expectation-not-real-root-of-trust |
| secretClassId | SEC-PSA13-002 |

## expectations EXP-PSA13-003

| Field | Value |
|---|---|
| id | EXP-PSA13-003 |
| chainId | CHN-PSA13-003 |
| recordRevision | PSA13-REV-001 |
| sourceRevision | fbc0223202a7f096804b1b551b63977abc10d34d |
| lockDigest | 5125dc39778971489248810b241596ad6cc13b9325d4e81aca905b3c5c48f417 |
| artifactDigest | 0ba0c99132d6e945af38d032bd5dd175368bbbe90a5e486dc81833cf48c0ac2b |
| builderId | BLD-PSA13-001 |
| buildType | finite-summary-v1 |
| parameters | target=synthetic-summary |
| actionRevision | 91296223262f7a7f6d82352e0947f4786b203f6e |
| workloadPrincipalId | WRK-PSA13-001 |
| permission | build-summary-only |
| runnerClass | ephemeral-unprivileged |
| isolation | separate-build-runtime |
| network | deny-external |
| cache | reviewed-no-cross-run-state |
| expectedRuntimeBoundary | RB-PSA13-001 |
| trustBasis | author-supplied-expectation-not-real-root-of-trust |
| secretClassId | SEC-PSA13-002 |

## expectations EXP-PSA13-004

| Field | Value |
|---|---|
| id | EXP-PSA13-004 |
| chainId | CHN-PSA13-004 |
| recordRevision | PSA13-REV-001 |
| sourceRevision | f0eb21aecc5bf32ef0d9bdf3c354d64497cf9309 |
| lockDigest | c81c83d998538f2eb1ca390155c1b02d4a4cbbb7998c705a784280d52b9a237e |
| artifactDigest | 9228102d16300a4ec3b9ce86327ed14b05b9ad287a94314a7ecdaac253f0a40b |
| builderId | BLD-PSA13-001 |
| buildType | finite-summary-v1 |
| parameters | target=synthetic-summary |
| actionRevision | 91296223262f7a7f6d82352e0947f4786b203f6e |
| workloadPrincipalId | WRK-PSA13-001 |
| permission | build-summary-only |
| runnerClass | ephemeral-unprivileged |
| isolation | separate-build-runtime |
| network | deny-external |
| cache | reviewed-no-cross-run-state |
| expectedRuntimeBoundary | RB-PSA13-001 |
| trustBasis | author-supplied-expectation-not-real-root-of-trust |
| secretClassId | SEC-PSA13-002 |

## expectations EXP-PSA13-005

| Field | Value |
|---|---|
| id | EXP-PSA13-005 |
| chainId | CHN-PSA13-005 |
| recordRevision | PSA13-REV-001 |
| sourceRevision | a561b92f0034a2fecc2077af920a1ea3b3919146 |
| lockDigest | e96862b409d4bf25394ce710f8e398b2c11806c327fcc219a1fdb1be1c240b7f |
| artifactDigest | 2212905502d5c258c6894da127b8daab0d9a33e41201d4d13faed328ef75ef60 |
| builderId | BLD-PSA13-001 |
| buildType | finite-summary-v1 |
| parameters | target=synthetic-summary |
| actionRevision | 91296223262f7a7f6d82352e0947f4786b203f6e |
| workloadPrincipalId | WRK-PSA13-001 |
| permission | build-summary-only |
| runnerClass | ephemeral-unprivileged |
| isolation | separate-build-runtime |
| network | deny-external |
| cache | reviewed-no-cross-run-state |
| expectedRuntimeBoundary | RB-PSA13-001 |
| trustBasis | author-supplied-expectation-not-real-root-of-trust |
| secretClassId | SEC-PSA13-002 |

## expectations EXP-PSA13-006

| Field | Value |
|---|---|
| id | EXP-PSA13-006 |
| chainId | CHN-PSA13-006 |
| recordRevision | PSA13-REV-001 |
| sourceRevision | 00b4953c634e5d2eaf5e3e7a26ff8308e917c4fb |
| lockDigest | 1193af504a42d1b29c60986036ce6d3b87f9d9afe2b1eda60a6e6f86b64f08de |
| artifactDigest | 098ce0d27fb46e5c96aed75b185169c094eabe243383e5a9b71bc7c7867f8bf4 |
| builderId | BLD-PSA13-001 |
| buildType | finite-summary-v1 |
| parameters | target=synthetic-summary |
| actionRevision | 91296223262f7a7f6d82352e0947f4786b203f6e |
| workloadPrincipalId | WRK-PSA13-001 |
| permission | build-summary-only |
| runnerClass | ephemeral-unprivileged |
| isolation | separate-build-runtime |
| network | deny-external |
| cache | reviewed-no-cross-run-state |
| expectedRuntimeBoundary | RB-PSA13-001 |
| trustBasis | author-supplied-expectation-not-real-root-of-trust |
| secretClassId | SEC-PSA13-002 |

## expectations EXP-PSA13-007

| Field | Value |
|---|---|
| id | EXP-PSA13-007 |
| chainId | CHN-PSA13-007 |
| recordRevision | PSA13-REV-001 |
| sourceRevision | 26addbb641d46ab9166d2f04008ad49bb5e6fd63 |
| lockDigest | c05aee88d88b4b8622008d17e8f2d55f10f9181d107a724e926f2286e2afd25b |
| artifactDigest | f5950ccec365ac9bbf6bf1ea01894cf925732667df4bce3372de095f1f81f028 |
| builderId | BLD-PSA13-001 |
| buildType | finite-summary-v1 |
| parameters | target=synthetic-summary |
| actionRevision | 91296223262f7a7f6d82352e0947f4786b203f6e |
| workloadPrincipalId | WRK-PSA13-001 |
| permission | build-summary-only |
| runnerClass | ephemeral-unprivileged |
| isolation | separate-build-runtime |
| network | deny-external |
| cache | reviewed-no-cross-run-state |
| expectedRuntimeBoundary | RB-PSA13-001 |
| trustBasis | author-supplied-expectation-not-real-root-of-trust |
| secretClassId | SEC-PSA13-002 |

## expectations EXP-PSA13-008

| Field | Value |
|---|---|
| id | EXP-PSA13-008 |
| chainId | CHN-PSA13-008 |
| recordRevision | PSA13-REV-001 |
| sourceRevision | b5e904c240aad31128eef64b478a295fc317d179 |
| lockDigest | 969a8dd26cda281da27b9cb086c7d7edfba9dcd8f866888a42bedca1889ddd02 |
| artifactDigest | 1ca98a80850d87fb76d5f3d751bb343cbe72bd930cbf8147c9d4d1bb8e045ac5 |
| builderId | BLD-PSA13-001 |
| buildType | finite-summary-v1 |
| parameters | target=synthetic-summary |
| actionRevision | 91296223262f7a7f6d82352e0947f4786b203f6e |
| workloadPrincipalId | WRK-PSA13-001 |
| permission | build-summary-only |
| runnerClass | ephemeral-unprivileged |
| isolation | separate-build-runtime |
| network | deny-external |
| cache | reviewed-no-cross-run-state |
| expectedRuntimeBoundary | RB-PSA13-001 |
| trustBasis | author-supplied-expectation-not-real-root-of-trust |
| secretClassId | SEC-PSA13-002 |

## chains CHN-PSA13-001

| Field | Value |
|---|---|
| id | CHN-PSA13-001 |
| label | Pinned supplied comparison |
| recordRevision | PSA13-REV-001 |
| platformId | PLT-PSA13-001 |
| source/id | SRC-PSA13-001 |
| source/repository | https://source.psa13.example/synthetic |
| source/refLabel | recorded-release |
| source/revision | cad8efa6b5af487f26222c95a5f908b5daa8b7b4 |
| source/lockId | LCK-PSA13-001 |
| source/lockDigest | 1a85c55f15c449b3294f5e930d53c6dd316d4c80d3a395b84680848443fc7998 |
| dependency/id | DEP-PSA13-001 |
| dependency/name | SYNTH-LIBRARY-NOT-PUBLISHED |
| dependency/version | 1.0.0-synthetic |
| dependency/source | https://dependency.psa13.example/synthetic |
| dependency/review | Reviewed summary |
| dependency/lockId | LCK-PSA13-001 |
| action/id | ACT-PSA13-001 |
| action/source | https://action.psa13.example/synthetic |
| action/version | 1.0.0-synthetic |
| action/revision | 91296223262f7a7f6d82352e0947f4786b203f6e |
| action/review | Reviewed summary |
| build/id | BLR-PSA13-001 |
| build/sourceId | SRC-PSA13-001 |
| build/sourceRevision | cad8efa6b5af487f26222c95a5f908b5daa8b7b4 |
| build/lockId | LCK-PSA13-001 |
| build/lockDigest | 1a85c55f15c449b3294f5e930d53c6dd316d4c80d3a395b84680848443fc7998 |
| build/builderId | BLD-PSA13-001 |
| build/workloadPrincipalId | WRK-PSA13-001 |
| build/permission | build-summary-only |
| build/runnerClass | ephemeral-unprivileged |
| build/isolation | separate-build-runtime |
| build/network | deny-external |
| build/cache | reviewed-no-cross-run-state |
| build/logId | LOG-PSA13-001 |
| build/secretClassId | SEC-PSA13-002 |
| artifact/id | OBJ-PSA13-001 |
| artifact/buildId | BLR-PSA13-001 |
| artifact/digest | 9efdb1d2979cdb7429c6b0204e7351ac835a19498b7dac316f03503e6e687c87 |
| artifact/signatureStatus | Recorded-unverified |
| artifact/sbomId | SBM-PSA13-001 |
| artifact/sbomFormat | book-summary-not-SPDX |
| artifact/sbomDependencyId | DEP-PSA13-001 |
| artifact/sbomCompleteness | Not assessed |
| provenance/id | PROV-PSA13-001 |
| provenance/artifactId | OBJ-PSA13-001 |
| provenance/subjectDigest | 9efdb1d2979cdb7429c6b0204e7351ac835a19498b7dac316f03503e6e687c87 |
| provenance/sourceRevision | cad8efa6b5af487f26222c95a5f908b5daa8b7b4 |
| provenance/lockDigest | 1a85c55f15c449b3294f5e930d53c6dd316d4c80d3a395b84680848443fc7998 |
| provenance/builderId | BLD-PSA13-001 |
| provenance/buildType | finite-summary-v1 |
| provenance/parameters | target=synthetic-summary |
| provenance/format | book-summary-not-SLSA |
| registry/id | REG-PSA13-001 |
| registry/location | https://registry.psa13.example/synthetic |
| registry/artifactId | OBJ-PSA13-001 |
| registry/digest | 9efdb1d2979cdb7429c6b0204e7351ac835a19498b7dac316f03503e6e687c87 |
| registry/tag | release-synthetic |
| registry/trust | Not assessed |
| promotion/id | PROM-PSA13-001 |
| promotion/registryId | REG-PSA13-001 |
| promotion/artifactId | OBJ-PSA13-001 |
| promotion/digest | 9efdb1d2979cdb7429c6b0204e7351ac835a19498b7dac316f03503e6e687c87 |
| promotion/fromEnvironment | Staging |
| promotion/toEnvironment | Production |
| promotion/status | Planned-only |
| promotion/reviewerPrincipalId | HUM-PSA13-001 |
| promotion/approved | false |
| deployment/id | DPL-PSA13-001 |
| deployment/promotionId | PROM-PSA13-001 |
| deployment/digest | 9efdb1d2979cdb7429c6b0204e7351ac835a19498b7dac316f03503e6e687c87 |
| deployment/status | Planned-only |
| deployment/runtimeBoundaryId | RB-PSA13-001 |
| runtime/id | RUN-PSA13-001 |
| runtime/deploymentId | DPL-PSA13-001 |
| runtime/digest | 9efdb1d2979cdb7429c6b0204e7351ac835a19498b7dac316f03503e6e687c87 |
| runtime/controlPlaneId | CP-PSA13-001 |
| runtime/dataPlaneId | DP-PSA13-001 |
| runtime/boundaryId | RB-PSA13-001 |
| runtime/status | Authored-snapshot-not-deployed |
| evidence/id | EVD-PSA13-001 |
| evidence/chainId | CHN-PSA13-001 |
| evidence/recordRevision | PSA13-REV-001 |
| evidence/expectationId | EXP-PSA13-001 |
| evidence/sourceId | SRC-PSA13-001 |
| evidence/buildLogId | LOG-PSA13-001 |
| evidence/artifactId | OBJ-PSA13-001 |
| evidence/runtimeId | RUN-PSA13-001 |
| evidence/recordedAt | 2026-09-15T08:00:00Z |
| evidence/basis | Compared summary |
| evidence/synthetic | true |
| evidence/expectedState | Verified |
| evidence/reason | all-supplied-bindings-match |
| finding/id | FND-PSA13-001 |
| finding/chainId | CHN-PSA13-001 |
| finding/evidenceId | EVD-PSA13-001 |
| finding/threatId | TH-2026-004 |
| finding/signalFlowId | SF-2026-006 |
| finding/status | Verified |
| finding/gap | 実Build、署名、Runtimeの観測と新たな実施許可はない。 |
| finding/alternative | 正常な変更、記録遅延、資料不足を比較する。 |
| finding/confidence | Medium |
| finding/treatment | record-review-question |
| finding/owner | SYNTH-PLATFORM-OWNER |
| finding/dueAt | 2026-09-22T00:00:00Z |
| finding/treatmentId | TRT-PSA13-001 |
| finding/validationQuestion | このChainの必要条件のどれを、同じ版と対象の資料で確認または反証できるか。 |
| finding/telemetryPlanId | TEL-PSA13-001 |
| finding/telemetryStatus | planned-not-tested |
| decision/id | DEC-PSA13-001 |
| decision/findingId | FND-PSA13-001 |
| decision/reassessmentId | REA-PSA13-001 |
| decision/disposition | Record-only |
| decision/executionAuthorized | false |
| decision/trigger | Source、Builder、Digest、権限、観測資料の変更時に再評価する。 |
| decision/treatmentId | TRT-PSA13-001 |

## chains CHN-PSA13-002

| Field | Value |
|---|---|
| id | CHN-PSA13-002 |
| label | Mutable source only |
| recordRevision | PSA13-REV-001 |
| platformId | PLT-PSA13-001 |
| source/id | SRC-PSA13-002 |
| source/repository | https://source.psa13.example/synthetic |
| source/refLabel | mutable-branch-only |
| source/revision | null |
| source/lockId | LCK-PSA13-002 |
| source/lockDigest | 8fd6ad965fe15db3b80dcb63edbd05941faa48adab0f8594d73d3da3ef0c8b0f |
| dependency/id | DEP-PSA13-002 |
| dependency/name | SYNTH-LIBRARY-NOT-PUBLISHED |
| dependency/version | 1.0.0-synthetic |
| dependency/source | https://dependency.psa13.example/synthetic |
| dependency/review | Reviewed summary |
| dependency/lockId | LCK-PSA13-002 |
| action/id | ACT-PSA13-002 |
| action/source | https://action.psa13.example/synthetic |
| action/version | 1.0.0-synthetic |
| action/revision | 91296223262f7a7f6d82352e0947f4786b203f6e |
| action/review | Reviewed summary |
| build/id | BLR-PSA13-002 |
| build/sourceId | SRC-PSA13-002 |
| build/sourceRevision | null |
| build/lockId | LCK-PSA13-002 |
| build/lockDigest | 8fd6ad965fe15db3b80dcb63edbd05941faa48adab0f8594d73d3da3ef0c8b0f |
| build/builderId | BLD-PSA13-001 |
| build/workloadPrincipalId | WRK-PSA13-001 |
| build/permission | build-summary-only |
| build/runnerClass | ephemeral-unprivileged |
| build/isolation | separate-build-runtime |
| build/network | deny-external |
| build/cache | reviewed-no-cross-run-state |
| build/logId | LOG-PSA13-002 |
| build/secretClassId | SEC-PSA13-002 |
| artifact/id | OBJ-PSA13-002 |
| artifact/buildId | BLR-PSA13-002 |
| artifact/digest | 28ef2aa48879e820e3f8cb272dbde6ef7421941e91b8cacc3ae9de98869ec543 |
| artifact/signatureStatus | Recorded-unverified |
| artifact/sbomId | SBM-PSA13-002 |
| artifact/sbomFormat | book-summary-not-SPDX |
| artifact/sbomDependencyId | DEP-PSA13-002 |
| artifact/sbomCompleteness | Not assessed |
| provenance/id | PROV-PSA13-002 |
| provenance/artifactId | OBJ-PSA13-002 |
| provenance/subjectDigest | 28ef2aa48879e820e3f8cb272dbde6ef7421941e91b8cacc3ae9de98869ec543 |
| provenance/sourceRevision | null |
| provenance/lockDigest | 8fd6ad965fe15db3b80dcb63edbd05941faa48adab0f8594d73d3da3ef0c8b0f |
| provenance/builderId | BLD-PSA13-001 |
| provenance/buildType | finite-summary-v1 |
| provenance/parameters | target=synthetic-summary |
| provenance/format | book-summary-not-SLSA |
| registry/id | REG-PSA13-002 |
| registry/location | https://registry.psa13.example/synthetic |
| registry/artifactId | OBJ-PSA13-002 |
| registry/digest | 28ef2aa48879e820e3f8cb272dbde6ef7421941e91b8cacc3ae9de98869ec543 |
| registry/tag | release-synthetic |
| registry/trust | Not assessed |
| promotion/id | PROM-PSA13-002 |
| promotion/registryId | REG-PSA13-002 |
| promotion/artifactId | OBJ-PSA13-002 |
| promotion/digest | 28ef2aa48879e820e3f8cb272dbde6ef7421941e91b8cacc3ae9de98869ec543 |
| promotion/fromEnvironment | Staging |
| promotion/toEnvironment | Production |
| promotion/status | Planned-only |
| promotion/reviewerPrincipalId | HUM-PSA13-001 |
| promotion/approved | false |
| deployment/id | DPL-PSA13-002 |
| deployment/promotionId | PROM-PSA13-002 |
| deployment/digest | 28ef2aa48879e820e3f8cb272dbde6ef7421941e91b8cacc3ae9de98869ec543 |
| deployment/status | Planned-only |
| deployment/runtimeBoundaryId | RB-PSA13-001 |
| runtime/id | RUN-PSA13-002 |
| runtime/deploymentId | DPL-PSA13-002 |
| runtime/digest | 28ef2aa48879e820e3f8cb272dbde6ef7421941e91b8cacc3ae9de98869ec543 |
| runtime/controlPlaneId | CP-PSA13-001 |
| runtime/dataPlaneId | DP-PSA13-001 |
| runtime/boundaryId | RB-PSA13-001 |
| runtime/status | Authored-snapshot-not-deployed |
| evidence/id | EVD-PSA13-002 |
| evidence/chainId | CHN-PSA13-002 |
| evidence/recordRevision | PSA13-REV-001 |
| evidence/expectationId | EXP-PSA13-002 |
| evidence/sourceId | SRC-PSA13-002 |
| evidence/buildLogId | LOG-PSA13-002 |
| evidence/artifactId | OBJ-PSA13-002 |
| evidence/runtimeId | RUN-PSA13-002 |
| evidence/recordedAt | 2026-09-15T08:00:00Z |
| evidence/basis | Compared summary |
| evidence/synthetic | true |
| evidence/expectedState | Rejected |
| evidence/reason | mutable-source-only |
| finding/id | FND-PSA13-002 |
| finding/chainId | CHN-PSA13-002 |
| finding/evidenceId | EVD-PSA13-002 |
| finding/threatId | TH-2026-004 |
| finding/signalFlowId | SF-2026-006 |
| finding/status | Rejected |
| finding/gap | 実Build、署名、Runtimeの観測と新たな実施許可はない。 |
| finding/alternative | 正常な変更、記録遅延、資料不足を比較する。 |
| finding/confidence | Medium |
| finding/treatment | record-review-question |
| finding/owner | SYNTH-PLATFORM-OWNER |
| finding/dueAt | 2026-09-22T00:00:00Z |
| finding/treatmentId | TRT-PSA13-002 |
| finding/validationQuestion | このChainの必要条件のどれを、同じ版と対象の資料で確認または反証できるか。 |
| finding/telemetryPlanId | TEL-PSA13-002 |
| finding/telemetryStatus | planned-not-tested |
| decision/id | DEC-PSA13-002 |
| decision/findingId | FND-PSA13-002 |
| decision/reassessmentId | REA-PSA13-002 |
| decision/disposition | Record-only |
| decision/executionAuthorized | false |
| decision/trigger | Source、Builder、Digest、権限、観測資料の変更時に再評価する。 |
| decision/treatmentId | TRT-PSA13-002 |

## chains CHN-PSA13-003

| Field | Value |
|---|---|
| id | CHN-PSA13-003 |
| label | Unversioned external action |
| recordRevision | PSA13-REV-001 |
| platformId | PLT-PSA13-001 |
| source/id | SRC-PSA13-003 |
| source/repository | https://source.psa13.example/synthetic |
| source/refLabel | recorded-release |
| source/revision | fbc0223202a7f096804b1b551b63977abc10d34d |
| source/lockId | LCK-PSA13-003 |
| source/lockDigest | 5125dc39778971489248810b241596ad6cc13b9325d4e81aca905b3c5c48f417 |
| dependency/id | DEP-PSA13-003 |
| dependency/name | SYNTH-LIBRARY-NOT-PUBLISHED |
| dependency/version | 1.0.0-synthetic |
| dependency/source | https://dependency.psa13.example/synthetic |
| dependency/review | Reviewed summary |
| dependency/lockId | LCK-PSA13-003 |
| action/id | ACT-PSA13-003 |
| action/source | https://action.psa13.example/synthetic |
| action/version | unversioned |
| action/revision | null |
| action/review | Not reviewed |
| build/id | BLR-PSA13-003 |
| build/sourceId | SRC-PSA13-003 |
| build/sourceRevision | fbc0223202a7f096804b1b551b63977abc10d34d |
| build/lockId | LCK-PSA13-003 |
| build/lockDigest | 5125dc39778971489248810b241596ad6cc13b9325d4e81aca905b3c5c48f417 |
| build/builderId | BLD-PSA13-001 |
| build/workloadPrincipalId | WRK-PSA13-001 |
| build/permission | build-summary-only |
| build/runnerClass | ephemeral-unprivileged |
| build/isolation | separate-build-runtime |
| build/network | deny-external |
| build/cache | reviewed-no-cross-run-state |
| build/logId | LOG-PSA13-003 |
| build/secretClassId | SEC-PSA13-002 |
| artifact/id | OBJ-PSA13-003 |
| artifact/buildId | BLR-PSA13-003 |
| artifact/digest | 0ba0c99132d6e945af38d032bd5dd175368bbbe90a5e486dc81833cf48c0ac2b |
| artifact/signatureStatus | Recorded-unverified |
| artifact/sbomId | SBM-PSA13-003 |
| artifact/sbomFormat | book-summary-not-SPDX |
| artifact/sbomDependencyId | DEP-PSA13-003 |
| artifact/sbomCompleteness | Not assessed |
| provenance/id | PROV-PSA13-003 |
| provenance/artifactId | OBJ-PSA13-003 |
| provenance/subjectDigest | 0ba0c99132d6e945af38d032bd5dd175368bbbe90a5e486dc81833cf48c0ac2b |
| provenance/sourceRevision | fbc0223202a7f096804b1b551b63977abc10d34d |
| provenance/lockDigest | 5125dc39778971489248810b241596ad6cc13b9325d4e81aca905b3c5c48f417 |
| provenance/builderId | BLD-PSA13-001 |
| provenance/buildType | finite-summary-v1 |
| provenance/parameters | target=synthetic-summary |
| provenance/format | book-summary-not-SLSA |
| registry/id | REG-PSA13-003 |
| registry/location | https://registry.psa13.example/synthetic |
| registry/artifactId | OBJ-PSA13-003 |
| registry/digest | 0ba0c99132d6e945af38d032bd5dd175368bbbe90a5e486dc81833cf48c0ac2b |
| registry/tag | release-synthetic |
| registry/trust | Not assessed |
| promotion/id | PROM-PSA13-003 |
| promotion/registryId | REG-PSA13-003 |
| promotion/artifactId | OBJ-PSA13-003 |
| promotion/digest | 0ba0c99132d6e945af38d032bd5dd175368bbbe90a5e486dc81833cf48c0ac2b |
| promotion/fromEnvironment | Staging |
| promotion/toEnvironment | Production |
| promotion/status | Planned-only |
| promotion/reviewerPrincipalId | HUM-PSA13-001 |
| promotion/approved | false |
| deployment/id | DPL-PSA13-003 |
| deployment/promotionId | PROM-PSA13-003 |
| deployment/digest | 0ba0c99132d6e945af38d032bd5dd175368bbbe90a5e486dc81833cf48c0ac2b |
| deployment/status | Planned-only |
| deployment/runtimeBoundaryId | RB-PSA13-001 |
| runtime/id | RUN-PSA13-003 |
| runtime/deploymentId | DPL-PSA13-003 |
| runtime/digest | 0ba0c99132d6e945af38d032bd5dd175368bbbe90a5e486dc81833cf48c0ac2b |
| runtime/controlPlaneId | CP-PSA13-001 |
| runtime/dataPlaneId | DP-PSA13-001 |
| runtime/boundaryId | RB-PSA13-001 |
| runtime/status | Authored-snapshot-not-deployed |
| evidence/id | EVD-PSA13-003 |
| evidence/chainId | CHN-PSA13-003 |
| evidence/recordRevision | PSA13-REV-001 |
| evidence/expectationId | EXP-PSA13-003 |
| evidence/sourceId | SRC-PSA13-003 |
| evidence/buildLogId | LOG-PSA13-003 |
| evidence/artifactId | OBJ-PSA13-003 |
| evidence/runtimeId | RUN-PSA13-003 |
| evidence/recordedAt | 2026-09-15T08:00:00Z |
| evidence/basis | Compared summary |
| evidence/synthetic | true |
| evidence/expectedState | Rejected |
| evidence/reason | unversioned-action |
| finding/id | FND-PSA13-003 |
| finding/chainId | CHN-PSA13-003 |
| finding/evidenceId | EVD-PSA13-003 |
| finding/threatId | TH-2026-004 |
| finding/signalFlowId | SF-2026-006 |
| finding/status | Rejected |
| finding/gap | 実Build、署名、Runtimeの観測と新たな実施許可はない。 |
| finding/alternative | 正常な変更、記録遅延、資料不足を比較する。 |
| finding/confidence | Medium |
| finding/treatment | record-review-question |
| finding/owner | SYNTH-PLATFORM-OWNER |
| finding/dueAt | 2026-09-22T00:00:00Z |
| finding/treatmentId | TRT-PSA13-003 |
| finding/validationQuestion | このChainの必要条件のどれを、同じ版と対象の資料で確認または反証できるか。 |
| finding/telemetryPlanId | TEL-PSA13-003 |
| finding/telemetryStatus | planned-not-tested |
| decision/id | DEC-PSA13-003 |
| decision/findingId | FND-PSA13-003 |
| decision/reassessmentId | REA-PSA13-003 |
| decision/disposition | Record-only |
| decision/executionAuthorized | false |
| decision/trigger | Source、Builder、Digest、権限、観測資料の変更時に再評価する。 |
| decision/treatmentId | TRT-PSA13-003 |

## chains CHN-PSA13-004

| Field | Value |
|---|---|
| id | CHN-PSA13-004 |
| label | Excess runner privilege |
| recordRevision | PSA13-REV-001 |
| platformId | PLT-PSA13-001 |
| source/id | SRC-PSA13-004 |
| source/repository | https://source.psa13.example/synthetic |
| source/refLabel | recorded-release |
| source/revision | f0eb21aecc5bf32ef0d9bdf3c354d64497cf9309 |
| source/lockId | LCK-PSA13-004 |
| source/lockDigest | c81c83d998538f2eb1ca390155c1b02d4a4cbbb7998c705a784280d52b9a237e |
| dependency/id | DEP-PSA13-004 |
| dependency/name | SYNTH-LIBRARY-NOT-PUBLISHED |
| dependency/version | 1.0.0-synthetic |
| dependency/source | https://dependency.psa13.example/synthetic |
| dependency/review | Reviewed summary |
| dependency/lockId | LCK-PSA13-004 |
| action/id | ACT-PSA13-004 |
| action/source | https://action.psa13.example/synthetic |
| action/version | 1.0.0-synthetic |
| action/revision | 91296223262f7a7f6d82352e0947f4786b203f6e |
| action/review | Reviewed summary |
| build/id | BLR-PSA13-004 |
| build/sourceId | SRC-PSA13-004 |
| build/sourceRevision | f0eb21aecc5bf32ef0d9bdf3c354d64497cf9309 |
| build/lockId | LCK-PSA13-004 |
| build/lockDigest | c81c83d998538f2eb1ca390155c1b02d4a4cbbb7998c705a784280d52b9a237e |
| build/builderId | BLD-PSA13-001 |
| build/workloadPrincipalId | WRK-PSA13-001 |
| build/permission | runtime-write-excess |
| build/runnerClass | ephemeral-unprivileged |
| build/isolation | separate-build-runtime |
| build/network | deny-external |
| build/cache | reviewed-no-cross-run-state |
| build/logId | LOG-PSA13-004 |
| build/secretClassId | SEC-PSA13-002 |
| artifact/id | OBJ-PSA13-004 |
| artifact/buildId | BLR-PSA13-004 |
| artifact/digest | 9228102d16300a4ec3b9ce86327ed14b05b9ad287a94314a7ecdaac253f0a40b |
| artifact/signatureStatus | Recorded-unverified |
| artifact/sbomId | SBM-PSA13-004 |
| artifact/sbomFormat | book-summary-not-SPDX |
| artifact/sbomDependencyId | DEP-PSA13-004 |
| artifact/sbomCompleteness | Not assessed |
| provenance/id | PROV-PSA13-004 |
| provenance/artifactId | OBJ-PSA13-004 |
| provenance/subjectDigest | 9228102d16300a4ec3b9ce86327ed14b05b9ad287a94314a7ecdaac253f0a40b |
| provenance/sourceRevision | f0eb21aecc5bf32ef0d9bdf3c354d64497cf9309 |
| provenance/lockDigest | c81c83d998538f2eb1ca390155c1b02d4a4cbbb7998c705a784280d52b9a237e |
| provenance/builderId | BLD-PSA13-001 |
| provenance/buildType | finite-summary-v1 |
| provenance/parameters | target=synthetic-summary |
| provenance/format | book-summary-not-SLSA |
| registry/id | REG-PSA13-004 |
| registry/location | https://registry.psa13.example/synthetic |
| registry/artifactId | OBJ-PSA13-004 |
| registry/digest | 9228102d16300a4ec3b9ce86327ed14b05b9ad287a94314a7ecdaac253f0a40b |
| registry/tag | release-synthetic |
| registry/trust | Not assessed |
| promotion/id | PROM-PSA13-004 |
| promotion/registryId | REG-PSA13-004 |
| promotion/artifactId | OBJ-PSA13-004 |
| promotion/digest | 9228102d16300a4ec3b9ce86327ed14b05b9ad287a94314a7ecdaac253f0a40b |
| promotion/fromEnvironment | Staging |
| promotion/toEnvironment | Production |
| promotion/status | Planned-only |
| promotion/reviewerPrincipalId | HUM-PSA13-001 |
| promotion/approved | false |
| deployment/id | DPL-PSA13-004 |
| deployment/promotionId | PROM-PSA13-004 |
| deployment/digest | 9228102d16300a4ec3b9ce86327ed14b05b9ad287a94314a7ecdaac253f0a40b |
| deployment/status | Planned-only |
| deployment/runtimeBoundaryId | RB-PSA13-001 |
| runtime/id | RUN-PSA13-004 |
| runtime/deploymentId | DPL-PSA13-004 |
| runtime/digest | 9228102d16300a4ec3b9ce86327ed14b05b9ad287a94314a7ecdaac253f0a40b |
| runtime/controlPlaneId | CP-PSA13-001 |
| runtime/dataPlaneId | DP-PSA13-001 |
| runtime/boundaryId | RB-PSA13-001 |
| runtime/status | Authored-snapshot-not-deployed |
| evidence/id | EVD-PSA13-004 |
| evidence/chainId | CHN-PSA13-004 |
| evidence/recordRevision | PSA13-REV-001 |
| evidence/expectationId | EXP-PSA13-004 |
| evidence/sourceId | SRC-PSA13-004 |
| evidence/buildLogId | LOG-PSA13-004 |
| evidence/artifactId | OBJ-PSA13-004 |
| evidence/runtimeId | RUN-PSA13-004 |
| evidence/recordedAt | 2026-09-15T08:00:00Z |
| evidence/basis | Compared summary |
| evidence/synthetic | true |
| evidence/expectedState | Rejected |
| evidence/reason | runner-permission-mismatch |
| finding/id | FND-PSA13-004 |
| finding/chainId | CHN-PSA13-004 |
| finding/evidenceId | EVD-PSA13-004 |
| finding/threatId | TH-2026-004 |
| finding/signalFlowId | SF-2026-006 |
| finding/status | Rejected |
| finding/gap | 実Build、署名、Runtimeの観測と新たな実施許可はない。 |
| finding/alternative | 正常な変更、記録遅延、資料不足を比較する。 |
| finding/confidence | Medium |
| finding/treatment | record-review-question |
| finding/owner | SYNTH-PLATFORM-OWNER |
| finding/dueAt | 2026-09-22T00:00:00Z |
| finding/treatmentId | TRT-PSA13-004 |
| finding/validationQuestion | このChainの必要条件のどれを、同じ版と対象の資料で確認または反証できるか。 |
| finding/telemetryPlanId | TEL-PSA13-004 |
| finding/telemetryStatus | planned-not-tested |
| decision/id | DEC-PSA13-004 |
| decision/findingId | FND-PSA13-004 |
| decision/reassessmentId | REA-PSA13-004 |
| decision/disposition | Record-only |
| decision/executionAuthorized | false |
| decision/trigger | Source、Builder、Digest、権限、観測資料の変更時に再評価する。 |
| decision/treatmentId | TRT-PSA13-004 |

## chains CHN-PSA13-005

| Field | Value |
|---|---|
| id | CHN-PSA13-005 |
| label | Unknown artifact origin |
| recordRevision | PSA13-REV-001 |
| platformId | PLT-PSA13-001 |
| source/id | SRC-PSA13-005 |
| source/repository | https://source.psa13.example/synthetic |
| source/refLabel | recorded-release |
| source/revision | a561b92f0034a2fecc2077af920a1ea3b3919146 |
| source/lockId | LCK-PSA13-005 |
| source/lockDigest | e96862b409d4bf25394ce710f8e398b2c11806c327fcc219a1fdb1be1c240b7f |
| dependency/id | DEP-PSA13-005 |
| dependency/name | SYNTH-LIBRARY-NOT-PUBLISHED |
| dependency/version | 1.0.0-synthetic |
| dependency/source | https://dependency.psa13.example/synthetic |
| dependency/review | Reviewed summary |
| dependency/lockId | LCK-PSA13-005 |
| action/id | ACT-PSA13-005 |
| action/source | https://action.psa13.example/synthetic |
| action/version | 1.0.0-synthetic |
| action/revision | 91296223262f7a7f6d82352e0947f4786b203f6e |
| action/review | Reviewed summary |
| build/id | BLR-PSA13-005 |
| build/sourceId | SRC-PSA13-005 |
| build/sourceRevision | a561b92f0034a2fecc2077af920a1ea3b3919146 |
| build/lockId | LCK-PSA13-005 |
| build/lockDigest | e96862b409d4bf25394ce710f8e398b2c11806c327fcc219a1fdb1be1c240b7f |
| build/builderId | BLD-PSA13-001 |
| build/workloadPrincipalId | WRK-PSA13-001 |
| build/permission | build-summary-only |
| build/runnerClass | ephemeral-unprivileged |
| build/isolation | separate-build-runtime |
| build/network | deny-external |
| build/cache | reviewed-no-cross-run-state |
| build/logId | LOG-PSA13-005 |
| build/secretClassId | SEC-PSA13-002 |
| artifact/id | OBJ-PSA13-005 |
| artifact/buildId | BLR-PSA13-005 |
| artifact/digest | 2212905502d5c258c6894da127b8daab0d9a33e41201d4d13faed328ef75ef60 |
| artifact/signatureStatus | Recorded-unverified |
| artifact/sbomId | SBM-PSA13-005 |
| artifact/sbomFormat | book-summary-not-SPDX |
| artifact/sbomDependencyId | DEP-PSA13-005 |
| artifact/sbomCompleteness | Not assessed |
| provenance/id | PROV-PSA13-005 |
| provenance/artifactId | null |
| provenance/subjectDigest | null |
| provenance/sourceRevision | null |
| provenance/lockDigest | null |
| provenance/builderId | null |
| provenance/buildType | null |
| provenance/parameters | null |
| provenance/format | book-summary-not-SLSA |
| registry/id | REG-PSA13-005 |
| registry/location | https://registry.psa13.example/synthetic |
| registry/artifactId | OBJ-PSA13-005 |
| registry/digest | 2212905502d5c258c6894da127b8daab0d9a33e41201d4d13faed328ef75ef60 |
| registry/tag | release-synthetic |
| registry/trust | Not assessed |
| promotion/id | PROM-PSA13-005 |
| promotion/registryId | REG-PSA13-005 |
| promotion/artifactId | OBJ-PSA13-005 |
| promotion/digest | 2212905502d5c258c6894da127b8daab0d9a33e41201d4d13faed328ef75ef60 |
| promotion/fromEnvironment | Staging |
| promotion/toEnvironment | Production |
| promotion/status | Planned-only |
| promotion/reviewerPrincipalId | HUM-PSA13-001 |
| promotion/approved | false |
| deployment/id | DPL-PSA13-005 |
| deployment/promotionId | PROM-PSA13-005 |
| deployment/digest | 2212905502d5c258c6894da127b8daab0d9a33e41201d4d13faed328ef75ef60 |
| deployment/status | Planned-only |
| deployment/runtimeBoundaryId | RB-PSA13-001 |
| runtime/id | RUN-PSA13-005 |
| runtime/deploymentId | DPL-PSA13-005 |
| runtime/digest | 2212905502d5c258c6894da127b8daab0d9a33e41201d4d13faed328ef75ef60 |
| runtime/controlPlaneId | CP-PSA13-001 |
| runtime/dataPlaneId | DP-PSA13-001 |
| runtime/boundaryId | RB-PSA13-001 |
| runtime/status | Authored-snapshot-not-deployed |
| evidence/id | EVD-PSA13-005 |
| evidence/chainId | CHN-PSA13-005 |
| evidence/recordRevision | PSA13-REV-001 |
| evidence/expectationId | EXP-PSA13-005 |
| evidence/sourceId | SRC-PSA13-005 |
| evidence/buildLogId | LOG-PSA13-005 |
| evidence/artifactId | OBJ-PSA13-005 |
| evidence/runtimeId | RUN-PSA13-005 |
| evidence/recordedAt | 2026-09-15T08:00:00Z |
| evidence/basis | Compared summary |
| evidence/synthetic | true |
| evidence/expectedState | Unknown |
| evidence/reason | provenance-missing |
| finding/id | FND-PSA13-005 |
| finding/chainId | CHN-PSA13-005 |
| finding/evidenceId | EVD-PSA13-005 |
| finding/threatId | TH-2026-004 |
| finding/signalFlowId | SF-2026-006 |
| finding/status | Unknown |
| finding/gap | 実Build、署名、Runtimeの観測と新たな実施許可はない。 |
| finding/alternative | 正常な変更、記録遅延、資料不足を比較する。 |
| finding/confidence | Low |
| finding/treatment | record-review-question |
| finding/owner | SYNTH-PLATFORM-OWNER |
| finding/dueAt | 2026-09-22T00:00:00Z |
| finding/treatmentId | TRT-PSA13-005 |
| finding/validationQuestion | このChainの必要条件のどれを、同じ版と対象の資料で確認または反証できるか。 |
| finding/telemetryPlanId | TEL-PSA13-005 |
| finding/telemetryStatus | planned-not-tested |
| decision/id | DEC-PSA13-005 |
| decision/findingId | FND-PSA13-005 |
| decision/reassessmentId | REA-PSA13-005 |
| decision/disposition | Record-only |
| decision/executionAuthorized | false |
| decision/trigger | Source、Builder、Digest、権限、観測資料の変更時に再評価する。 |
| decision/treatmentId | TRT-PSA13-005 |

## chains CHN-PSA13-006

| Field | Value |
|---|---|
| id | CHN-PSA13-006 |
| label | Declaration only |
| recordRevision | PSA13-REV-001 |
| platformId | PLT-PSA13-001 |
| source/id | SRC-PSA13-006 |
| source/repository | https://source.psa13.example/synthetic |
| source/refLabel | recorded-release |
| source/revision | 00b4953c634e5d2eaf5e3e7a26ff8308e917c4fb |
| source/lockId | LCK-PSA13-006 |
| source/lockDigest | 1193af504a42d1b29c60986036ce6d3b87f9d9afe2b1eda60a6e6f86b64f08de |
| dependency/id | DEP-PSA13-006 |
| dependency/name | SYNTH-LIBRARY-NOT-PUBLISHED |
| dependency/version | 1.0.0-synthetic |
| dependency/source | https://dependency.psa13.example/synthetic |
| dependency/review | Reviewed summary |
| dependency/lockId | LCK-PSA13-006 |
| action/id | ACT-PSA13-006 |
| action/source | https://action.psa13.example/synthetic |
| action/version | 1.0.0-synthetic |
| action/revision | 91296223262f7a7f6d82352e0947f4786b203f6e |
| action/review | Reviewed summary |
| build/id | BLR-PSA13-006 |
| build/sourceId | SRC-PSA13-006 |
| build/sourceRevision | 00b4953c634e5d2eaf5e3e7a26ff8308e917c4fb |
| build/lockId | LCK-PSA13-006 |
| build/lockDigest | 1193af504a42d1b29c60986036ce6d3b87f9d9afe2b1eda60a6e6f86b64f08de |
| build/builderId | BLD-PSA13-001 |
| build/workloadPrincipalId | WRK-PSA13-001 |
| build/permission | build-summary-only |
| build/runnerClass | ephemeral-unprivileged |
| build/isolation | separate-build-runtime |
| build/network | deny-external |
| build/cache | reviewed-no-cross-run-state |
| build/logId | LOG-PSA13-006 |
| build/secretClassId | SEC-PSA13-002 |
| artifact/id | OBJ-PSA13-006 |
| artifact/buildId | BLR-PSA13-006 |
| artifact/digest | 098ce0d27fb46e5c96aed75b185169c094eabe243383e5a9b71bc7c7867f8bf4 |
| artifact/signatureStatus | Recorded-unverified |
| artifact/sbomId | SBM-PSA13-006 |
| artifact/sbomFormat | book-summary-not-SPDX |
| artifact/sbomDependencyId | DEP-PSA13-006 |
| artifact/sbomCompleteness | Not assessed |
| provenance/id | PROV-PSA13-006 |
| provenance/artifactId | OBJ-PSA13-006 |
| provenance/subjectDigest | 098ce0d27fb46e5c96aed75b185169c094eabe243383e5a9b71bc7c7867f8bf4 |
| provenance/sourceRevision | 00b4953c634e5d2eaf5e3e7a26ff8308e917c4fb |
| provenance/lockDigest | 1193af504a42d1b29c60986036ce6d3b87f9d9afe2b1eda60a6e6f86b64f08de |
| provenance/builderId | BLD-PSA13-001 |
| provenance/buildType | finite-summary-v1 |
| provenance/parameters | target=synthetic-summary |
| provenance/format | book-summary-not-SLSA |
| registry/id | REG-PSA13-006 |
| registry/location | https://registry.psa13.example/synthetic |
| registry/artifactId | OBJ-PSA13-006 |
| registry/digest | 098ce0d27fb46e5c96aed75b185169c094eabe243383e5a9b71bc7c7867f8bf4 |
| registry/tag | release-synthetic |
| registry/trust | Not assessed |
| promotion/id | PROM-PSA13-006 |
| promotion/registryId | REG-PSA13-006 |
| promotion/artifactId | OBJ-PSA13-006 |
| promotion/digest | 098ce0d27fb46e5c96aed75b185169c094eabe243383e5a9b71bc7c7867f8bf4 |
| promotion/fromEnvironment | Staging |
| promotion/toEnvironment | Production |
| promotion/status | Planned-only |
| promotion/reviewerPrincipalId | HUM-PSA13-001 |
| promotion/approved | false |
| deployment/id | DPL-PSA13-006 |
| deployment/promotionId | PROM-PSA13-006 |
| deployment/digest | 098ce0d27fb46e5c96aed75b185169c094eabe243383e5a9b71bc7c7867f8bf4 |
| deployment/status | Planned-only |
| deployment/runtimeBoundaryId | RB-PSA13-001 |
| runtime/id | RUN-PSA13-006 |
| runtime/deploymentId | DPL-PSA13-006 |
| runtime/digest | 098ce0d27fb46e5c96aed75b185169c094eabe243383e5a9b71bc7c7867f8bf4 |
| runtime/controlPlaneId | CP-PSA13-001 |
| runtime/dataPlaneId | DP-PSA13-001 |
| runtime/boundaryId | RB-PSA13-001 |
| runtime/status | Authored-snapshot-not-deployed |
| evidence/id | EVD-PSA13-006 |
| evidence/chainId | CHN-PSA13-006 |
| evidence/recordRevision | PSA13-REV-001 |
| evidence/expectationId | EXP-PSA13-006 |
| evidence/sourceId | SRC-PSA13-006 |
| evidence/buildLogId | LOG-PSA13-006 |
| evidence/artifactId | OBJ-PSA13-006 |
| evidence/runtimeId | RUN-PSA13-006 |
| evidence/recordedAt | 2026-09-15T08:00:00Z |
| evidence/basis | Declared summary |
| evidence/synthetic | true |
| evidence/expectedState | Declared |
| evidence/reason | declaration-only |
| finding/id | FND-PSA13-006 |
| finding/chainId | CHN-PSA13-006 |
| finding/evidenceId | EVD-PSA13-006 |
| finding/threatId | TH-2026-004 |
| finding/signalFlowId | SF-2026-006 |
| finding/status | Declared |
| finding/gap | 実Build、署名、Runtimeの観測と新たな実施許可はない。 |
| finding/alternative | 正常な変更、記録遅延、資料不足を比較する。 |
| finding/confidence | Medium |
| finding/treatment | record-review-question |
| finding/owner | SYNTH-PLATFORM-OWNER |
| finding/dueAt | 2026-09-22T00:00:00Z |
| finding/treatmentId | TRT-PSA13-006 |
| finding/validationQuestion | このChainの必要条件のどれを、同じ版と対象の資料で確認または反証できるか。 |
| finding/telemetryPlanId | TEL-PSA13-006 |
| finding/telemetryStatus | planned-not-tested |
| decision/id | DEC-PSA13-006 |
| decision/findingId | FND-PSA13-006 |
| decision/reassessmentId | REA-PSA13-006 |
| decision/disposition | Record-only |
| decision/executionAuthorized | false |
| decision/trigger | Source、Builder、Digest、権限、観測資料の変更時に再評価する。 |
| decision/treatmentId | TRT-PSA13-006 |

## chains CHN-PSA13-007

| Field | Value |
|---|---|
| id | CHN-PSA13-007 |
| label | Observation without comparison |
| recordRevision | PSA13-REV-001 |
| platformId | PLT-PSA13-001 |
| source/id | SRC-PSA13-007 |
| source/repository | https://source.psa13.example/synthetic |
| source/refLabel | recorded-release |
| source/revision | 26addbb641d46ab9166d2f04008ad49bb5e6fd63 |
| source/lockId | LCK-PSA13-007 |
| source/lockDigest | c05aee88d88b4b8622008d17e8f2d55f10f9181d107a724e926f2286e2afd25b |
| dependency/id | DEP-PSA13-007 |
| dependency/name | SYNTH-LIBRARY-NOT-PUBLISHED |
| dependency/version | 1.0.0-synthetic |
| dependency/source | https://dependency.psa13.example/synthetic |
| dependency/review | Reviewed summary |
| dependency/lockId | LCK-PSA13-007 |
| action/id | ACT-PSA13-007 |
| action/source | https://action.psa13.example/synthetic |
| action/version | 1.0.0-synthetic |
| action/revision | 91296223262f7a7f6d82352e0947f4786b203f6e |
| action/review | Reviewed summary |
| build/id | BLR-PSA13-007 |
| build/sourceId | SRC-PSA13-007 |
| build/sourceRevision | 26addbb641d46ab9166d2f04008ad49bb5e6fd63 |
| build/lockId | LCK-PSA13-007 |
| build/lockDigest | c05aee88d88b4b8622008d17e8f2d55f10f9181d107a724e926f2286e2afd25b |
| build/builderId | BLD-PSA13-001 |
| build/workloadPrincipalId | WRK-PSA13-001 |
| build/permission | build-summary-only |
| build/runnerClass | ephemeral-unprivileged |
| build/isolation | separate-build-runtime |
| build/network | deny-external |
| build/cache | reviewed-no-cross-run-state |
| build/logId | LOG-PSA13-007 |
| build/secretClassId | SEC-PSA13-002 |
| artifact/id | OBJ-PSA13-007 |
| artifact/buildId | BLR-PSA13-007 |
| artifact/digest | f5950ccec365ac9bbf6bf1ea01894cf925732667df4bce3372de095f1f81f028 |
| artifact/signatureStatus | Recorded-unverified |
| artifact/sbomId | SBM-PSA13-007 |
| artifact/sbomFormat | book-summary-not-SPDX |
| artifact/sbomDependencyId | DEP-PSA13-007 |
| artifact/sbomCompleteness | Not assessed |
| provenance/id | PROV-PSA13-007 |
| provenance/artifactId | OBJ-PSA13-007 |
| provenance/subjectDigest | f5950ccec365ac9bbf6bf1ea01894cf925732667df4bce3372de095f1f81f028 |
| provenance/sourceRevision | 26addbb641d46ab9166d2f04008ad49bb5e6fd63 |
| provenance/lockDigest | c05aee88d88b4b8622008d17e8f2d55f10f9181d107a724e926f2286e2afd25b |
| provenance/builderId | BLD-PSA13-001 |
| provenance/buildType | finite-summary-v1 |
| provenance/parameters | target=synthetic-summary |
| provenance/format | book-summary-not-SLSA |
| registry/id | REG-PSA13-007 |
| registry/location | https://registry.psa13.example/synthetic |
| registry/artifactId | OBJ-PSA13-007 |
| registry/digest | f5950ccec365ac9bbf6bf1ea01894cf925732667df4bce3372de095f1f81f028 |
| registry/tag | release-synthetic |
| registry/trust | Not assessed |
| promotion/id | PROM-PSA13-007 |
| promotion/registryId | REG-PSA13-007 |
| promotion/artifactId | OBJ-PSA13-007 |
| promotion/digest | f5950ccec365ac9bbf6bf1ea01894cf925732667df4bce3372de095f1f81f028 |
| promotion/fromEnvironment | Staging |
| promotion/toEnvironment | Production |
| promotion/status | Planned-only |
| promotion/reviewerPrincipalId | HUM-PSA13-001 |
| promotion/approved | false |
| deployment/id | DPL-PSA13-007 |
| deployment/promotionId | PROM-PSA13-007 |
| deployment/digest | f5950ccec365ac9bbf6bf1ea01894cf925732667df4bce3372de095f1f81f028 |
| deployment/status | Planned-only |
| deployment/runtimeBoundaryId | RB-PSA13-001 |
| runtime/id | RUN-PSA13-007 |
| runtime/deploymentId | DPL-PSA13-007 |
| runtime/digest | f5950ccec365ac9bbf6bf1ea01894cf925732667df4bce3372de095f1f81f028 |
| runtime/controlPlaneId | CP-PSA13-001 |
| runtime/dataPlaneId | DP-PSA13-001 |
| runtime/boundaryId | RB-PSA13-001 |
| runtime/status | Authored-snapshot-not-deployed |
| evidence/id | EVD-PSA13-007 |
| evidence/chainId | CHN-PSA13-007 |
| evidence/recordRevision | PSA13-REV-001 |
| evidence/expectationId | EXP-PSA13-007 |
| evidence/sourceId | SRC-PSA13-007 |
| evidence/buildLogId | LOG-PSA13-007 |
| evidence/artifactId | OBJ-PSA13-007 |
| evidence/runtimeId | RUN-PSA13-007 |
| evidence/recordedAt | 2026-09-15T08:00:00Z |
| evidence/basis | Observed summary |
| evidence/synthetic | true |
| evidence/expectedState | Observed |
| evidence/reason | observation-only |
| finding/id | FND-PSA13-007 |
| finding/chainId | CHN-PSA13-007 |
| finding/evidenceId | EVD-PSA13-007 |
| finding/threatId | TH-2026-004 |
| finding/signalFlowId | SF-2026-006 |
| finding/status | Observed |
| finding/gap | 実Build、署名、Runtimeの観測と新たな実施許可はない。 |
| finding/alternative | 正常な変更、記録遅延、資料不足を比較する。 |
| finding/confidence | Medium |
| finding/treatment | record-review-question |
| finding/owner | SYNTH-PLATFORM-OWNER |
| finding/dueAt | 2026-09-22T00:00:00Z |
| finding/treatmentId | TRT-PSA13-007 |
| finding/validationQuestion | このChainの必要条件のどれを、同じ版と対象の資料で確認または反証できるか。 |
| finding/telemetryPlanId | TEL-PSA13-007 |
| finding/telemetryStatus | planned-not-tested |
| decision/id | DEC-PSA13-007 |
| decision/findingId | FND-PSA13-007 |
| decision/reassessmentId | REA-PSA13-007 |
| decision/disposition | Record-only |
| decision/executionAuthorized | false |
| decision/trigger | Source、Builder、Digest、権限、観測資料の変更時に再評価する。 |
| decision/treatmentId | TRT-PSA13-007 |

## chains CHN-PSA13-008

| Field | Value |
|---|---|
| id | CHN-PSA13-008 |
| label | Runtime digest drift |
| recordRevision | PSA13-REV-001 |
| platformId | PLT-PSA13-001 |
| source/id | SRC-PSA13-008 |
| source/repository | https://source.psa13.example/synthetic |
| source/refLabel | recorded-release |
| source/revision | b5e904c240aad31128eef64b478a295fc317d179 |
| source/lockId | LCK-PSA13-008 |
| source/lockDigest | 969a8dd26cda281da27b9cb086c7d7edfba9dcd8f866888a42bedca1889ddd02 |
| dependency/id | DEP-PSA13-008 |
| dependency/name | SYNTH-LIBRARY-NOT-PUBLISHED |
| dependency/version | 1.0.0-synthetic |
| dependency/source | https://dependency.psa13.example/synthetic |
| dependency/review | Reviewed summary |
| dependency/lockId | LCK-PSA13-008 |
| action/id | ACT-PSA13-008 |
| action/source | https://action.psa13.example/synthetic |
| action/version | 1.0.0-synthetic |
| action/revision | 91296223262f7a7f6d82352e0947f4786b203f6e |
| action/review | Reviewed summary |
| build/id | BLR-PSA13-008 |
| build/sourceId | SRC-PSA13-008 |
| build/sourceRevision | b5e904c240aad31128eef64b478a295fc317d179 |
| build/lockId | LCK-PSA13-008 |
| build/lockDigest | 969a8dd26cda281da27b9cb086c7d7edfba9dcd8f866888a42bedca1889ddd02 |
| build/builderId | BLD-PSA13-001 |
| build/workloadPrincipalId | WRK-PSA13-001 |
| build/permission | build-summary-only |
| build/runnerClass | ephemeral-unprivileged |
| build/isolation | separate-build-runtime |
| build/network | deny-external |
| build/cache | reviewed-no-cross-run-state |
| build/logId | LOG-PSA13-008 |
| build/secretClassId | SEC-PSA13-002 |
| artifact/id | OBJ-PSA13-008 |
| artifact/buildId | BLR-PSA13-008 |
| artifact/digest | 1ca98a80850d87fb76d5f3d751bb343cbe72bd930cbf8147c9d4d1bb8e045ac5 |
| artifact/signatureStatus | Recorded-unverified |
| artifact/sbomId | SBM-PSA13-008 |
| artifact/sbomFormat | book-summary-not-SPDX |
| artifact/sbomDependencyId | DEP-PSA13-008 |
| artifact/sbomCompleteness | Not assessed |
| provenance/id | PROV-PSA13-008 |
| provenance/artifactId | OBJ-PSA13-008 |
| provenance/subjectDigest | 1ca98a80850d87fb76d5f3d751bb343cbe72bd930cbf8147c9d4d1bb8e045ac5 |
| provenance/sourceRevision | b5e904c240aad31128eef64b478a295fc317d179 |
| provenance/lockDigest | 969a8dd26cda281da27b9cb086c7d7edfba9dcd8f866888a42bedca1889ddd02 |
| provenance/builderId | BLD-PSA13-001 |
| provenance/buildType | finite-summary-v1 |
| provenance/parameters | target=synthetic-summary |
| provenance/format | book-summary-not-SLSA |
| registry/id | REG-PSA13-008 |
| registry/location | https://registry.psa13.example/synthetic |
| registry/artifactId | OBJ-PSA13-008 |
| registry/digest | 1ca98a80850d87fb76d5f3d751bb343cbe72bd930cbf8147c9d4d1bb8e045ac5 |
| registry/tag | release-synthetic |
| registry/trust | Not assessed |
| promotion/id | PROM-PSA13-008 |
| promotion/registryId | REG-PSA13-008 |
| promotion/artifactId | OBJ-PSA13-008 |
| promotion/digest | 1ca98a80850d87fb76d5f3d751bb343cbe72bd930cbf8147c9d4d1bb8e045ac5 |
| promotion/fromEnvironment | Staging |
| promotion/toEnvironment | Production |
| promotion/status | Planned-only |
| promotion/reviewerPrincipalId | HUM-PSA13-001 |
| promotion/approved | false |
| deployment/id | DPL-PSA13-008 |
| deployment/promotionId | PROM-PSA13-008 |
| deployment/digest | 1ca98a80850d87fb76d5f3d751bb343cbe72bd930cbf8147c9d4d1bb8e045ac5 |
| deployment/status | Planned-only |
| deployment/runtimeBoundaryId | RB-PSA13-001 |
| runtime/id | RUN-PSA13-008 |
| runtime/deploymentId | DPL-PSA13-008 |
| runtime/digest | f2b79473fd5ea4a0f7b538e68b1210041c72feb664ae01fcfef0efc1619da902 |
| runtime/controlPlaneId | CP-PSA13-001 |
| runtime/dataPlaneId | DP-PSA13-001 |
| runtime/boundaryId | RB-PSA13-001 |
| runtime/status | Authored-snapshot-not-deployed |
| evidence/id | EVD-PSA13-008 |
| evidence/chainId | CHN-PSA13-008 |
| evidence/recordRevision | PSA13-REV-001 |
| evidence/expectationId | EXP-PSA13-008 |
| evidence/sourceId | SRC-PSA13-008 |
| evidence/buildLogId | LOG-PSA13-008 |
| evidence/artifactId | OBJ-PSA13-008 |
| evidence/runtimeId | RUN-PSA13-008 |
| evidence/recordedAt | 2026-09-15T08:00:00Z |
| evidence/basis | Compared summary |
| evidence/synthetic | true |
| evidence/expectedState | Rejected |
| evidence/reason | runtime-digest-mismatch |
| finding/id | FND-PSA13-008 |
| finding/chainId | CHN-PSA13-008 |
| finding/evidenceId | EVD-PSA13-008 |
| finding/threatId | TH-2026-004 |
| finding/signalFlowId | SF-2026-006 |
| finding/status | Rejected |
| finding/gap | 実Build、署名、Runtimeの観測と新たな実施許可はない。 |
| finding/alternative | 正常な変更、記録遅延、資料不足を比較する。 |
| finding/confidence | Medium |
| finding/treatment | record-review-question |
| finding/owner | SYNTH-PLATFORM-OWNER |
| finding/dueAt | 2026-09-22T00:00:00Z |
| finding/treatmentId | TRT-PSA13-008 |
| finding/validationQuestion | このChainの必要条件のどれを、同じ版と対象の資料で確認または反証できるか。 |
| finding/telemetryPlanId | TEL-PSA13-008 |
| finding/telemetryStatus | planned-not-tested |
| decision/id | DEC-PSA13-008 |
| decision/findingId | FND-PSA13-008 |
| decision/reassessmentId | REA-PSA13-008 |
| decision/disposition | Record-only |
| decision/executionAuthorized | false |
| decision/trigger | Source、Builder、Digest、権限、観測資料の変更時に再評価する。 |
| decision/treatmentId | TRT-PSA13-008 |

## handoffs HOF-PSA13-014

| Field | Value |
|---|---|
| id | HOF-PSA13-014 |
| chapter | 14 |
| assessmentId | PSA-2026-013 |
| input | Validation question / Build-Deploy correlation / supply-chain boundary |
| state | planned-not-delivered |
| owner | SYNTH-PLATFORM-OWNER |
| parentStateChanged | false |

## handoffs HOF-PSA13-016

| Field | Value |
|---|---|
| id | HOF-PSA13-016 |
| chapter | 16 |
| assessmentId | PSA-2026-013 |
| input | Validation question / Build-Deploy correlation / supply-chain boundary |
| state | planned-not-delivered |
| owner | SYNTH-PLATFORM-OWNER |
| parentStateChanged | false |

## handoffs HOF-PSA13-027

| Field | Value |
|---|---|
| id | HOF-PSA13-027 |
| chapter | 27 |
| assessmentId | PSA-2026-013 |
| input | Validation question / Build-Deploy correlation / supply-chain boundary |
| state | planned-not-delivered |
| owner | SYNTH-PLATFORM-OWNER |
| parentStateChanged | false |
