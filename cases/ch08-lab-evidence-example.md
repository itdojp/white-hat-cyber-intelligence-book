# 第8章 Lab Safety and Evidence Plan 完全合成記入例

## 読み方と安全境界

ART-18 / LABPLAN-2026-001はCASE-2026-001をrefinesする完全合成の教材である。実Runtimeは実行しない。Control receiptsとOAuth/API/TelemetryのEventは供給された仮定であり、Hostを観測した結果ではない。全RunのexecutionAuthorizedはfalseで、実作業の許可を発行しない。

[第8章](../manuscript/08-safe-lab-evidence.md)、[Template](../templates/lab-safety-evidence-plan.md)、[Source Review Note](../references/ch08-source-review-2026-09-13.md)を対にする。機械可読の正本は[Plan](fixtures/ch08-lab-plan.json)、[Control receipts](fixtures/ch08-control-receipts.json)、[Evidence manifest](fixtures/ch08-evidence-manifest.json)である。下表は全フィールドを表示し、nullと空配列を区別する。ReceiptとEventはIDごとに残りのフィールドをキー付きでまとめる。

AuthorityはAUTH-CASE-2026-001の教材参照、Scopeはread-only-synthetic-dataである。実対象への接続、走査、認証試行、実Credential・実Token・実Cookie・個人情報の入力は行わない。不明なData、ID・Hashの不一致、予期しないエラーでは停止する。Cleanupは自分で保存した報告コピーの整理だけで、親Caseや版管理されたEvidenceは保持する。

親の[Signal Flow](ch06-signal-flow-example.md)のSF-2026-001と[優先順位記録](ch07-vulnerability-prioritization-example.md)のVPR-ITEM-005を直接参照する。CoverageはProduced、GAP-SF-001は維持する。本章のPassで親のControl、観測、優先順位、Authority、期限を更新しない。

## 三Runの判断

SafeはすべてPass、UnsafeはRuntimeのegressがFail、InconclusiveはRuntimeのcollectionとCleanupのcredentialがUnknownである。Unsafeは六種のCleanupを通過してもUnsafeのままで、正常完了はfalseである。InconclusiveはFailed closedで終わり、正常完了もCleanup verifiedもfalseである。

開始前のFailまたはUnknownではRunningへ進まない。Failed closedの後に新規シナリオ操作を再開せず、許可された停止・Evidence export・破棄・残存確認だけを扱う。停止を確認できない場合やEvidence export失敗では、後続段階を未訪問として保持する。提供する三例以外の反証は有限回帰で確認し、任意の実Runtime評価器としては使わない。

同じ表に全receiptを掲載しても、未訪問段階の値を評価に使ったことにはならない。failureReceiptIds、unknownReceiptIds、skippedStagesと履歴を合わせて読む。合成時刻は固定UTCで、現実のHost時計に同期した証拠ではない。

## 完全記入データ

### Document Control

| Field | Value |
|---|---|
| schemaVersion | 1.0.0 |
| synthetic | true |
| artifactId | ART-18 |
| planSetId | LABPLAN-2026-001 |
| parentCaseId | CASE-2026-001 |
| relation | refines |
| decisionRequirementId | DR-2026-001 |
| authorizationRecordId | AUTH-CASE-2026-001 |
| parentThreatModelId | TM-2026-001 |
| parentSignalMapId | SFM-2026-001 |
| parentPrioritySetId | VPR-2026-001 |
| scope | read-only-synthetic-data |
| modelVersion | 1.0.0 |
| executionMode | offline-receipt-replay |
| runtimeExecuted | false |
| parentState | No inherited observation, control, gap, priority or authorization is promoted. |
| legalBoundary | Educational reproducibility only; not legal admissibility or production assurance. |
| states | Planned, Preflight passed, Ready, Running, Stopped, Destroyed, Cleanup verified, Failed closed |

### Lab Architecture

| Field | Value |
|---|---|
| platformModel | WSL2 and rootless Podman equivalent abstract design |
| runtimeVersion | not-executed |
| imageDigest | null |
| rootless | true |
| privileged | false |
| capabilities | 空配列 |
| hostNetwork | false |
| egressPolicy | default-deny |
| allowedEndpointClass | reserved-synthetic-only |
| networkId | NET-LAB08-001 |
| exampleHost | lab.test |
| exampleAddress | 192.0.2.8 |
| exposure | local-only-design-not-opened |
| inputMode | read-only |
| outputMode | ephemeral-design-not-allocated |
| mountScope | dedicated-lab-directory-only |
| credentialMaterial | none |
| classification | synthetic-only |
| limits | bounded-cpu-memory-disk-time-model; no actual runtime measurement |

### RUN-LAB08-SAFE

| Field | Value |
|---|---|
| runId | RUN-LAB08-SAFE |
| synthetic | true |
| planId | LABPLAN-08-001 |
| labId | LAB-08-001 |
| objective | 合成記録だけで開始条件・停止・残存確認を判断する。 |
| scope | read-only-synthetic-data |
| signalFlowId | SF-2026-001 |
| priorityRecordId | VPR-ITEM-005 |
| assetIds | ASSET-2026-002, ASSET-2026-005 |
| boundaryIds | TB-2026-001, TB-2026-003 |
| parentCoverage | Produced |
| parentGapId | GAP-SF-001 |
| startsAt | 2026-09-13T00:00:00Z |
| endsAt | 2026-09-13T00:01:00Z |
| receiptIds | RCP-LAB08-001-001, RCP-LAB08-001-002, RCP-LAB08-001-003, RCP-LAB08-001-004, RCP-LAB08-001-005, RCP-LAB08-001-006, RCP-LAB08-001-007, RCP-LAB08-001-008, RCP-LAB08-001-009, RCP-LAB08-001-010, RCP-LAB08-001-011, RCP-LAB08-001-012, RCP-LAB08-001-013, RCP-LAB08-001-014, RCP-LAB08-001-015, RCP-LAB08-001-016, RCP-LAB08-001-017, RCP-LAB08-001-018, RCP-LAB08-001-019, RCP-LAB08-001-020, RCP-LAB08-001-021, RCP-LAB08-001-022, RCP-LAB08-001-023, RCP-LAB08-001-024 |
| signalIds | EVENT-LAB08-001-001, EVENT-LAB08-001-002, EVENT-LAB08-001-003 |
| evidenceArtifactId | EVD-LAB08-001 |
| stopId | STOP-LAB08-001 |
| cleanupId | CLEAN-LAB08-001 |
| reassessmentId | REASSESS-LAB08-001 |
| owner | SYNTH-LAB-OWNER |
| reviewer | SYNTH-LAB-REVIEWER |
| expectedEvidence | 合成control receiptsとOAuth/API/Telemetry教材の一致。 |
| prohibitedEvidence | 実Credential・実Token・実Cookie・個人情報は収集しない。 |
| stopCondition | FailまたはUnknownなら新規シナリオ操作を停止し、状態とEvidenceを保存する。 |
| rollback | 合成資源台帳の停止・Evidence export・破棄・六種残存検査を順に照合する。 |
| evidenceRetention | EVD-LAB08-001は教材正本として保持し、削除対象の一時資源とは区別する。 |
| gap | 実Runtimeの隔離・停止・残存は未測定。親のGapは不変。 |
| confidence | 低 |
| alternative | 供給された合成receiptが実環境で成立するとは限らない。 |
| reassessmentTrigger | 新Run ID、Authority、境界、実装版、時計、収集状態、残存結果の変更。 |
| nextReviewDate | 2026-09-14 |
| roeReference | not-issued; S0/S1 read-only lesson, no operational RoE |
| emergencyContact | SYNTH-LAB-OWNER |
| executionStepId | STEP-LAB08-001-REPLAY |

### RUN-LAB08-SAFE expected

| Field | Value |
|---|---|
| verdict | Safe |
| statusHistory | Planned, Preflight passed, Ready, Running, Stopped, Destroyed, Cleanup verified |
| finalStatus | Cleanup verified |
| completedNormally | true |
| cleanupVerified | true |
| executionAuthorized | false |
| failureReceiptIds | 空配列 |
| unknownReceiptIds | 空配列 |
| skippedStages | 空配列 |

### RUN-LAB08-UNSAFE

| Field | Value |
|---|---|
| runId | RUN-LAB08-UNSAFE |
| synthetic | true |
| planId | LABPLAN-08-002 |
| labId | LAB-08-002 |
| objective | 合成記録だけで開始条件・停止・残存確認を判断する。 |
| scope | read-only-synthetic-data |
| signalFlowId | SF-2026-001 |
| priorityRecordId | VPR-ITEM-005 |
| assetIds | ASSET-2026-002, ASSET-2026-005 |
| boundaryIds | TB-2026-001, TB-2026-003 |
| parentCoverage | Produced |
| parentGapId | GAP-SF-001 |
| startsAt | 2026-09-13T00:02:00Z |
| endsAt | 2026-09-13T00:03:00Z |
| receiptIds | RCP-LAB08-002-001, RCP-LAB08-002-002, RCP-LAB08-002-003, RCP-LAB08-002-004, RCP-LAB08-002-005, RCP-LAB08-002-006, RCP-LAB08-002-007, RCP-LAB08-002-008, RCP-LAB08-002-009, RCP-LAB08-002-010, RCP-LAB08-002-011, RCP-LAB08-002-012, RCP-LAB08-002-013, RCP-LAB08-002-014, RCP-LAB08-002-015, RCP-LAB08-002-016, RCP-LAB08-002-017, RCP-LAB08-002-018, RCP-LAB08-002-019, RCP-LAB08-002-020, RCP-LAB08-002-021, RCP-LAB08-002-022, RCP-LAB08-002-023, RCP-LAB08-002-024 |
| signalIds | EVENT-LAB08-002-001, EVENT-LAB08-002-002, EVENT-LAB08-002-003 |
| evidenceArtifactId | EVD-LAB08-001 |
| stopId | STOP-LAB08-002 |
| cleanupId | CLEAN-LAB08-002 |
| reassessmentId | REASSESS-LAB08-002 |
| owner | SYNTH-LAB-OWNER |
| reviewer | SYNTH-LAB-REVIEWER |
| expectedEvidence | 合成control receiptsとOAuth/API/Telemetry教材の一致。 |
| prohibitedEvidence | 実Credential・実Token・実Cookie・個人情報は収集しない。 |
| stopCondition | FailまたはUnknownなら新規シナリオ操作を停止し、状態とEvidenceを保存する。 |
| rollback | 合成資源台帳の停止・Evidence export・破棄・六種残存検査を順に照合する。 |
| evidenceRetention | EVD-LAB08-001は教材正本として保持し、削除対象の一時資源とは区別する。 |
| gap | 実Runtimeの隔離・停止・残存は未測定。親のGapは不変。 |
| confidence | 低 |
| alternative | 供給された合成receiptが実環境で成立するとは限らない。 |
| reassessmentTrigger | 新Run ID、Authority、境界、実装版、時計、収集状態、残存結果の変更。 |
| nextReviewDate | 2026-09-14 |
| roeReference | not-issued; S0/S1 read-only lesson, no operational RoE |
| emergencyContact | SYNTH-LAB-OWNER |
| executionStepId | STEP-LAB08-002-REPLAY |

### RUN-LAB08-UNSAFE expected

| Field | Value |
|---|---|
| verdict | Unsafe |
| statusHistory | Planned, Preflight passed, Ready, Running, Failed closed, Stopped, Destroyed, Cleanup verified |
| finalStatus | Cleanup verified |
| completedNormally | false |
| cleanupVerified | true |
| executionAuthorized | false |
| failureReceiptIds | RCP-LAB08-002-009 |
| unknownReceiptIds | 空配列 |
| skippedStages | 空配列 |

### RUN-LAB08-INCONCLUSIVE

| Field | Value |
|---|---|
| runId | RUN-LAB08-INCONCLUSIVE |
| synthetic | true |
| planId | LABPLAN-08-003 |
| labId | LAB-08-003 |
| objective | 合成記録だけで開始条件・停止・残存確認を判断する。 |
| scope | read-only-synthetic-data |
| signalFlowId | SF-2026-001 |
| priorityRecordId | VPR-ITEM-005 |
| assetIds | ASSET-2026-002, ASSET-2026-005 |
| boundaryIds | TB-2026-001, TB-2026-003 |
| parentCoverage | Produced |
| parentGapId | GAP-SF-001 |
| startsAt | 2026-09-13T00:04:00Z |
| endsAt | 2026-09-13T00:05:00Z |
| receiptIds | RCP-LAB08-003-001, RCP-LAB08-003-002, RCP-LAB08-003-003, RCP-LAB08-003-004, RCP-LAB08-003-005, RCP-LAB08-003-006, RCP-LAB08-003-007, RCP-LAB08-003-008, RCP-LAB08-003-009, RCP-LAB08-003-010, RCP-LAB08-003-011, RCP-LAB08-003-012, RCP-LAB08-003-013, RCP-LAB08-003-014, RCP-LAB08-003-015, RCP-LAB08-003-016, RCP-LAB08-003-017, RCP-LAB08-003-018, RCP-LAB08-003-019, RCP-LAB08-003-020, RCP-LAB08-003-021, RCP-LAB08-003-022, RCP-LAB08-003-023, RCP-LAB08-003-024 |
| signalIds | EVENT-LAB08-003-001, EVENT-LAB08-003-002, EVENT-LAB08-003-003 |
| evidenceArtifactId | EVD-LAB08-001 |
| stopId | STOP-LAB08-003 |
| cleanupId | CLEAN-LAB08-003 |
| reassessmentId | REASSESS-LAB08-003 |
| owner | SYNTH-LAB-OWNER |
| reviewer | SYNTH-LAB-REVIEWER |
| expectedEvidence | 合成control receiptsとOAuth/API/Telemetry教材の一致。 |
| prohibitedEvidence | 実Credential・実Token・実Cookie・個人情報は収集しない。 |
| stopCondition | FailまたはUnknownなら新規シナリオ操作を停止し、状態とEvidenceを保存する。 |
| rollback | 合成資源台帳の停止・Evidence export・破棄・六種残存検査を順に照合する。 |
| evidenceRetention | EVD-LAB08-001は教材正本として保持し、削除対象の一時資源とは区別する。 |
| gap | 実Runtimeの隔離・停止・残存は未測定。親のGapは不変。 |
| confidence | 低 |
| alternative | 供給された合成receiptが実環境で成立するとは限らない。 |
| reassessmentTrigger | 新Run ID、Authority、境界、実装版、時計、収集状態、残存結果の変更。 |
| nextReviewDate | 2026-09-14 |
| roeReference | not-issued; S0/S1 read-only lesson, no operational RoE |
| emergencyContact | SYNTH-LAB-OWNER |
| executionStepId | STEP-LAB08-003-REPLAY |

### RUN-LAB08-INCONCLUSIVE expected

| Field | Value |
|---|---|
| verdict | Inconclusive |
| statusHistory | Planned, Preflight passed, Ready, Running, Failed closed, Stopped, Destroyed, Failed closed |
| finalStatus | Failed closed |
| completedNormally | false |
| cleanupVerified | false |
| executionAuthorized | false |
| failureReceiptIds | 空配列 |
| unknownReceiptIds | RCP-LAB08-003-014, RCP-LAB08-003-023 |
| skippedStages | 空配列 |

### Evidence Manifest

| Field | Value |
|---|---|
| schemaVersion | 1.0.0 |
| synthetic | true |
| manifestId | EVM-LAB08-001 |
| artifactId | EVD-LAB08-001 |
| artifactPath | cases/fixtures/ch08-control-receipts.json |
| sha256 | 6a4b7b5b413701cec742d25fd992c88296f54043ef44cddd07d48209fa49e9a2 |
| sourceFixtureId | FIX-LAB08-001 |
| runIds | RUN-LAB08-SAFE, RUN-LAB08-UNSAFE, RUN-LAB08-INCONCLUSIVE |
| producerId | SYNTH-CH08-GENERATOR |
| createdAt | 2026-09-13T00:10:00Z |
| classification | synthetic-only |
| custodian | SYNTH-EVIDENCE-CUSTODIAN |
| retention | versioned teaching artifact; no credential material |
| limitation | Hash agreement verifies supplied bytes, not authenticity, legal admissibility or real execution. |

### Transform 1

| Field | Value |
|---|---|
| operation | synthetic-generation |
| inputIds | 空配列 |
| outputArtifactId | EVD-LAB08-001 |
| producerId | SYNTH-CH08-GENERATOR |
| generatorVersion | 1.0.0 |
| seed | 208 |
| recordedAt | 2026-09-13T00:10:00Z |

### Receipt Control

| Field | Value |
|---|---|
| schemaVersion | 1.0.0 |
| synthetic | true |
| fixtureId | FIX-LAB08-001 |
| generatorVersion | 1.0.0 |
| seed | 208 |
| producerId | SYNTH-CH08-GENERATOR |
| timeBasis | fixed synthetic UTC; not synchronized with a real host |

### Control receipts

| Field | Value |
|---|---|
| RCP-LAB08-001-001 | runId=RUN-LAB08-SAFE; synthetic=true; stage=preflight; check=authority; result=Pass; observedAt=2026-09-13T00:00:01Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-001-002 | runId=RUN-LAB08-SAFE; synthetic=true; stage=preflight; check=rootless; result=Pass; observedAt=2026-09-13T00:00:02Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-001-003 | runId=RUN-LAB08-SAFE; synthetic=true; stage=preflight; check=privileges; result=Pass; observedAt=2026-09-13T00:00:03Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-001-004 | runId=RUN-LAB08-SAFE; synthetic=true; stage=preflight; check=network; result=Pass; observedAt=2026-09-13T00:00:04Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-001-005 | runId=RUN-LAB08-SAFE; synthetic=true; stage=preflight; check=egress; result=Pass; observedAt=2026-09-13T00:00:05Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-001-006 | runId=RUN-LAB08-SAFE; synthetic=true; stage=preflight; check=mount; result=Pass; observedAt=2026-09-13T00:00:06Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-001-007 | runId=RUN-LAB08-SAFE; synthetic=true; stage=preflight; check=data; result=Pass; observedAt=2026-09-13T00:00:07Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-001-008 | runId=RUN-LAB08-SAFE; synthetic=true; stage=preflight; check=collection; result=Pass; observedAt=2026-09-13T00:00:08Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-001-009 | runId=RUN-LAB08-SAFE; synthetic=true; stage=runtime; check=egress; result=Pass; observedAt=2026-09-13T00:00:09Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-001-010 | runId=RUN-LAB08-SAFE; synthetic=true; stage=runtime; check=scope; result=Pass; observedAt=2026-09-13T00:00:10Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-001-011 | runId=RUN-LAB08-SAFE; synthetic=true; stage=runtime; check=privileges; result=Pass; observedAt=2026-09-13T00:00:11Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-001-012 | runId=RUN-LAB08-SAFE; synthetic=true; stage=runtime; check=data; result=Pass; observedAt=2026-09-13T00:00:12Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-001-013 | runId=RUN-LAB08-SAFE; synthetic=true; stage=runtime; check=resources; result=Pass; observedAt=2026-09-13T00:00:13Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-001-014 | runId=RUN-LAB08-SAFE; synthetic=true; stage=runtime; check=collection; result=Pass; observedAt=2026-09-13T00:00:14Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-001-015 | runId=RUN-LAB08-SAFE; synthetic=true; stage=runtime; check=clock; result=Pass; observedAt=2026-09-13T00:00:15Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-001-016 | runId=RUN-LAB08-SAFE; synthetic=true; stage=stop; check=stopped; result=Pass; observedAt=2026-09-13T00:00:16Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-001-017 | runId=RUN-LAB08-SAFE; synthetic=true; stage=export; check=evidenceExport; result=Pass; observedAt=2026-09-13T00:00:17Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-001-018 | runId=RUN-LAB08-SAFE; synthetic=true; stage=destroy; check=destroyed; result=Pass; observedAt=2026-09-13T00:00:18Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-001-019 | runId=RUN-LAB08-SAFE; synthetic=true; stage=cleanup; check=container; result=Pass; observedAt=2026-09-13T00:00:19Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-001-020 | runId=RUN-LAB08-SAFE; synthetic=true; stage=cleanup; check=network; result=Pass; observedAt=2026-09-13T00:00:20Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-001-021 | runId=RUN-LAB08-SAFE; synthetic=true; stage=cleanup; check=volume; result=Pass; observedAt=2026-09-13T00:00:21Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-001-022 | runId=RUN-LAB08-SAFE; synthetic=true; stage=cleanup; check=file; result=Pass; observedAt=2026-09-13T00:00:22Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-001-023 | runId=RUN-LAB08-SAFE; synthetic=true; stage=cleanup; check=credential; result=Pass; observedAt=2026-09-13T00:00:23Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-001-024 | runId=RUN-LAB08-SAFE; synthetic=true; stage=cleanup; check=port; result=Pass; observedAt=2026-09-13T00:00:24Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-001 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=preflight; check=authority; result=Pass; observedAt=2026-09-13T00:02:01Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-002 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=preflight; check=rootless; result=Pass; observedAt=2026-09-13T00:02:02Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-003 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=preflight; check=privileges; result=Pass; observedAt=2026-09-13T00:02:03Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-004 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=preflight; check=network; result=Pass; observedAt=2026-09-13T00:02:04Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-005 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=preflight; check=egress; result=Pass; observedAt=2026-09-13T00:02:05Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-006 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=preflight; check=mount; result=Pass; observedAt=2026-09-13T00:02:06Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-007 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=preflight; check=data; result=Pass; observedAt=2026-09-13T00:02:07Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-008 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=preflight; check=collection; result=Pass; observedAt=2026-09-13T00:02:08Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-009 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=runtime; check=egress; result=Fail; observedAt=2026-09-13T00:02:09Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-010 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=runtime; check=scope; result=Pass; observedAt=2026-09-13T00:02:10Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-011 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=runtime; check=privileges; result=Pass; observedAt=2026-09-13T00:02:11Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-012 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=runtime; check=data; result=Pass; observedAt=2026-09-13T00:02:12Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-013 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=runtime; check=resources; result=Pass; observedAt=2026-09-13T00:02:13Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-014 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=runtime; check=collection; result=Pass; observedAt=2026-09-13T00:02:14Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-015 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=runtime; check=clock; result=Pass; observedAt=2026-09-13T00:02:15Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-016 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=stop; check=stopped; result=Pass; observedAt=2026-09-13T00:02:16Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-017 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=export; check=evidenceExport; result=Pass; observedAt=2026-09-13T00:02:17Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-018 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=destroy; check=destroyed; result=Pass; observedAt=2026-09-13T00:02:18Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-019 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=cleanup; check=container; result=Pass; observedAt=2026-09-13T00:02:19Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-020 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=cleanup; check=network; result=Pass; observedAt=2026-09-13T00:02:20Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-021 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=cleanup; check=volume; result=Pass; observedAt=2026-09-13T00:02:21Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-022 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=cleanup; check=file; result=Pass; observedAt=2026-09-13T00:02:22Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-023 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=cleanup; check=credential; result=Pass; observedAt=2026-09-13T00:02:23Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-002-024 | runId=RUN-LAB08-UNSAFE; synthetic=true; stage=cleanup; check=port; result=Pass; observedAt=2026-09-13T00:02:24Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-001 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=preflight; check=authority; result=Pass; observedAt=2026-09-13T00:04:01Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-002 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=preflight; check=rootless; result=Pass; observedAt=2026-09-13T00:04:02Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-003 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=preflight; check=privileges; result=Pass; observedAt=2026-09-13T00:04:03Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-004 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=preflight; check=network; result=Pass; observedAt=2026-09-13T00:04:04Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-005 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=preflight; check=egress; result=Pass; observedAt=2026-09-13T00:04:05Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-006 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=preflight; check=mount; result=Pass; observedAt=2026-09-13T00:04:06Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-007 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=preflight; check=data; result=Pass; observedAt=2026-09-13T00:04:07Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-008 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=preflight; check=collection; result=Pass; observedAt=2026-09-13T00:04:08Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-009 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=runtime; check=egress; result=Pass; observedAt=2026-09-13T00:04:09Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-010 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=runtime; check=scope; result=Pass; observedAt=2026-09-13T00:04:10Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-011 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=runtime; check=privileges; result=Pass; observedAt=2026-09-13T00:04:11Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-012 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=runtime; check=data; result=Pass; observedAt=2026-09-13T00:04:12Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-013 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=runtime; check=resources; result=Pass; observedAt=2026-09-13T00:04:13Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-014 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=runtime; check=collection; result=Unknown; observedAt=2026-09-13T00:04:14Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-015 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=runtime; check=clock; result=Pass; observedAt=2026-09-13T00:04:15Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-016 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=stop; check=stopped; result=Pass; observedAt=2026-09-13T00:04:16Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-017 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=export; check=evidenceExport; result=Pass; observedAt=2026-09-13T00:04:17Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-018 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=destroy; check=destroyed; result=Pass; observedAt=2026-09-13T00:04:18Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-019 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=cleanup; check=container; result=Pass; observedAt=2026-09-13T00:04:19Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-020 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=cleanup; check=network; result=Pass; observedAt=2026-09-13T00:04:20Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-021 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=cleanup; check=volume; result=Pass; observedAt=2026-09-13T00:04:21Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-022 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=cleanup; check=file; result=Pass; observedAt=2026-09-13T00:04:22Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-023 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=cleanup; check=credential; result=Unknown; observedAt=2026-09-13T00:04:23Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |
| RCP-LAB08-003-024 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; stage=cleanup; check=port; result=Pass; observedAt=2026-09-13T00:04:24Z; producerId=SYNTH-CH08-GENERATOR; basis=supplied synthetic control check; not a host observation |

### Synthetic signals

| Field | Value |
|---|---|
| EVENT-LAB08-001-001 | runId=RUN-LAB08-SAFE; synthetic=true; eventClass=oauth-consent-observation; actorId=SYNTH-ACTOR-LAB08-001; exampleHost=identity.lab.test; credentialMaterial=none; recordedAt=2026-09-13T00:00:11Z; meaning=teaching record only; no protocol request was sent |
| EVENT-LAB08-001-002 | runId=RUN-LAB08-SAFE; synthetic=true; eventClass=api-authorization-observation; actorId=SYNTH-ACTOR-LAB08-001; exampleHost=identity.lab.test; credentialMaterial=none; recordedAt=2026-09-13T00:00:12Z; meaning=teaching record only; no protocol request was sent |
| EVENT-LAB08-001-003 | runId=RUN-LAB08-SAFE; synthetic=true; eventClass=telemetry-collection-observation; actorId=SYNTH-ACTOR-LAB08-001; exampleHost=identity.lab.test; credentialMaterial=none; recordedAt=2026-09-13T00:00:13Z; meaning=teaching record only; no protocol request was sent |
| EVENT-LAB08-002-001 | runId=RUN-LAB08-UNSAFE; synthetic=true; eventClass=oauth-consent-observation; actorId=SYNTH-ACTOR-LAB08-002; exampleHost=identity.lab.test; credentialMaterial=none; recordedAt=2026-09-13T00:02:11Z; meaning=teaching record only; no protocol request was sent |
| EVENT-LAB08-002-002 | runId=RUN-LAB08-UNSAFE; synthetic=true; eventClass=api-authorization-observation; actorId=SYNTH-ACTOR-LAB08-002; exampleHost=identity.lab.test; credentialMaterial=none; recordedAt=2026-09-13T00:02:12Z; meaning=teaching record only; no protocol request was sent |
| EVENT-LAB08-002-003 | runId=RUN-LAB08-UNSAFE; synthetic=true; eventClass=telemetry-collection-observation; actorId=SYNTH-ACTOR-LAB08-002; exampleHost=identity.lab.test; credentialMaterial=none; recordedAt=2026-09-13T00:02:13Z; meaning=teaching record only; no protocol request was sent |
| EVENT-LAB08-003-001 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; eventClass=oauth-consent-observation; actorId=SYNTH-ACTOR-LAB08-003; exampleHost=identity.lab.test; credentialMaterial=none; recordedAt=2026-09-13T00:04:11Z; meaning=teaching record only; no protocol request was sent |
| EVENT-LAB08-003-002 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; eventClass=api-authorization-observation; actorId=SYNTH-ACTOR-LAB08-003; exampleHost=identity.lab.test; credentialMaterial=none; recordedAt=2026-09-13T00:04:12Z; meaning=teaching record only; no protocol request was sent |
| EVENT-LAB08-003-003 | runId=RUN-LAB08-INCONCLUSIVE; synthetic=true; eventClass=telemetry-collection-observation; actorId=SYNTH-ACTOR-LAB08-003; exampleHost=identity.lab.test; credentialMaterial=none; recordedAt=2026-09-13T00:04:13Z; meaning=teaching record only; no protocol request was sent |

## Evidenceと再評価の結論

EVD-LAB08-001は、実際の供給ファイルのSHA-256と照合する。Transformは合成生成一回であり、元の実Logや実Credentialがあるという意味ではない。Hash一致は指定Byteとの同一性であり、真実性、法的証拠能力、完全なChain of custody、実Runtimeの成功の証明ではない。

保持する教材正本と破棄対象の一時資源を区別する。Container・Network・Volume・File・Credential・Portの各Passはモデルの仮定であり、実Hostの残存を測定した記録ではない。Evidence exportが確認できなければ破棄へ進まない。

分析の確信度は低。実装版、Hostの境界、時計、収集経路がモデルと異なる可能性が残る。各REASSESS-LAB08 IDのOwnerはSYNTH-LAB-OWNER、ReviewerはSYNTH-LAB-REVIEWER、次回Reviewは2026-09-14とする。実務の再開には新Run IDと独立したAuthority確認が必要であり、この教材から自動昇格しない。
