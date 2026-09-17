# 第15章 完全合成記入例：Finding ReportとRetest Record

## この記入例の扱い

ART-04 / ART-23 / FRT-2026-015はCASE-2026-001をrefinesする非実行の教材である。全ID・値・時刻・判断は作成者が記述した供給記録であり、実サービスの応答、実対策の効果、実許可の発行結果ではない。実操作・実通信・実変更・実届出・実公表は行わない。

[第15章](../manuscript/15-findings-retest-risk.md)、[Finding Report](../templates/finding-report.md)、[Retest Record](../templates/retest-record.md)、[正本JSON](fixtures/ch15-findings-retest-risk.json)、[閉じたSchema](../schemas/ch15-findings-retest-risk.schema.json)を参照する。以下はJSONの全末端Fieldと一対一のField/Value表であり、添字は0始まり、nullと空配列も表示する。

## 親記録と対象の境界

最初にrecord、parents、context、safetyを読む。親RoEのDraft、失効AUTH、元Window、三Objectのfalse、第8章のRunningを含む八状態、独立CASE-2026-011、第12章のUnknown、第13章のVerified=供給summary比較、第14章のSupported/Complete/ResidualのScopeは変えない。

本章のAPP-FRT15-001は第12章のOAuth例から新規作成した教材である。親14のVAL/FNDは方法参照だけであり、新Appの成立性Evidenceではない。各FindingのvalidationとevidenceIdsは新しいsubjectIdとsubjectRevisionへ直接結び付く。第7章のVPR比較もSeverityの自動転用ではない。

## 七つの独立した対比

七Findingは一つの実運用上の状態遷移履歴ではない。同じ設計上の権限差を出発点にした独立した教材の選択肢であり、固定asOfにおける供給判断を比較する。001 Open / Failed、002 Mitigated / Partial、003 Accepted / 明示的Acceptance、004 Retest required / Inconclusive、005 Closed / Passed、006 Reopened / Stoppedと期限切れAcceptance、007 Closed / 明示的Acceptanceを読む。

Mitigatedは供給された一時対策レビューEvidenceがある教材状態であり、implemented=falseの実環境へ対策を実施したという意味ではない。Closedの二つの根拠を混ぜず、AcceptedやClosedでもResidualをゼロにしない。Acceptanceの権限範囲は当該供給シナリオだけで、評価の実行許可を上書きしない。

五Retestはpermissionを主条件、auditReferenceを補助条件とする二条件比較である。停止を最優先し、Method不足・欠測はInconclusive、主条件不一致はFailed、主条件一致かつ補助不一致はPartial、両一致だけPassedとする。Scanner summary onlyは必要Methodを満たさず、再実行の記述だけで完了へ進めない。Retest IDがない二記録はAcceptance経路であり、欠けたRetestを捏造しない。

## 判断・停止・引継ぎ

確認事実は供給Field、分析判断はrootConditionとjudgment、仮定は合成対象と固定時刻、推奨はTreatmentとDecisionの計画に分ける。実事業影響は未測定、別説明と不足情報を残す。残存・Owner・期限・再評価・Audience・調整状況を別々に記入する。

実Data、外部通信、Scope不明、未知入力なら停止する。実Credentialを再利用しない。実システムを変更しない。実システムを削除しない。実許可と実開示の判断が必要なら教材の外で責任者へ確認する。五Handoffはplanned-not-deliveredであり、第16〜22章や第26章の受領や改善効果を主張しない。

本章の六観点Rubricを使い、症状と根本条件、SeverityとPriority、対策と証拠、RetestとAcceptance、ClosedとResidualを区別する。権限不足の上書き、Scannerだけでの完了、Evidenceの対象付替え、期限切れAcceptanceからのClosedは差し戻す。

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
| id | FRT-2026-015 |
| revision | FRT15-REV-001 |
| caseId | CASE-2026-001 |
| relation | refines |
| artifactIds/0 | ART-04 |
| artifactIds/1 | ART-23 |
| asOf | 2026-09-16T23:00:00Z |
| scenarioMeaning | seven-independent-authored-alternatives-not-a-production-timeline |
| actualOperations | 0 |

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
| parentValidationRecord | MIV-2026-014 |
| parentHandoffId | HOF-MIV14-15 |
| parentHandoffStatus | planned-not-delivered |
| parentStateChanged | false |
| parentValidationId | VAL-MIV14-001 |
| parentFindingId | FND-MIV14-001 |
| parentEvidenceRole | method-reference-not-evidence-for-new-subject |
| parentCompleteMeaning | authored-reading-record-only |
| parentSupportedMeaning | supplied-two-criteria-only |
| parentCopyResidualMeaning | current-authored-reading-copy-only |
| parentIdentityApplication | APP-IAR12-001 |
| newApplication | APP-FRT15-001 |
| applicationRelation | authored-variant-not-parent-current-binding |
| parentIdentityBinding | Unknown |
| parentPlatformVerifiedMeaning | authored-summary-comparison-only |
| independentCaseId | CASE-2026-011 |
| independentEvidenceUsed | false |
| labStates/0 | Planned |
| labStates/1 | Preflight passed |
| labStates/2 | Ready |
| labStates/3 | Running |
| labStates/4 | Stopped |
| labStates/5 | Destroyed |
| labStates/6 | Cleanup verified |
| labStates/7 | Failed closed |
| labRuntimeExecuted | false |
| priorityReference | VPR-ITEM-001 |
| priorityReferenceMeaning | contrast-only-no-CVE-rating-transferred |
| findingStatuses/0 | Open |
| findingStatuses/1 | Mitigated |
| findingStatuses/2 | Accepted |
| findingStatuses/3 | Retest required |
| findingStatuses/4 | Closed |
| findingStatuses/5 | Reopened |
| retestResults/0 | Passed |
| retestResults/1 | Partial |
| retestResults/2 | Failed |
| retestResults/3 | Inconclusive |
| retestResults/4 | Stopped |
| sourceIds/0 | SRC-IPA-VDP-001 |
| sourceIds/1 | SRC-WSTG-001 |
| sourceIds/2 | SRC-CVSS-001 |

## safety

| Field | Value |
|---|---|
| actualNetworkConnections | 0 |
| actualSystemChanges | 0 |
| actualScannerRuns | 0 |
| actualNoticesSent | 0 |
| actualPublicDisclosures | 0 |
| realCredentialsPresent | false |
| legalPermissionGranted | false |
| riskAcceptanceOverridesAuthority | false |
| measuredBusinessImpact | false |
| actualCleanupPerformed | false |
| stop | 未知の入力・Scope不一致・追跡不能があれば読解を止め、追加操作を行わない。 |
| cleanup | 作業メモだけを整理し、正本・親資料を保持する。実システムを変更しない。実システムを削除しない。 |

## findings FND-FRT15-001

| Field | Value |
|---|---|
| id | FND-FRT15-001 |
| scenarioId | SCN-FRT15-001 |
| caseId | CASE-2026-001 |
| assetId | ASSET-2026-005 |
| threatId | TH-2026-004 |
| subjectId | APP-FRT15-001 |
| subjectRevision | BEFORE-FRT15-001 |
| status | Open |
| requestedStage | Report |
| title | 供給OAuth App設計で必要業務より広い権限宣言があるという分析候補。 |
| symptom | 供給設定のpermission欄と業務要件のpermission欄が異なる。 |
| rootCondition/id | ROOT-FRT15-001 |
| rootCondition/claim | 要件と権限宣言の対応を確認する承認条件が供給設計にない。 |
| rootCondition/basis | authored-design-comparison-not-verified-implementation |
| validation/id | VAL-FRT15-001 |
| validation/findingId | FND-FRT15-001 |
| validation/subjectId | APP-FRT15-001 |
| validation/subjectRevision | BEFORE-FRT15-001 |
| validation/method | Static authored comparison |
| validation/requirementPermission | read-summary |
| validation/declaredPermission | read-all-summaries |
| validation/evidenceId | EVD-FRT15-001 |
| validation/basis | authored-supplied-values |
| validation/actualOperation | false |
| evidenceIds/0 | EVD-FRT15-001 |
| scope/confirmed | この供給版の権限宣言文字列だけ。 |
| scope/candidate | 同じ設計条件が実装にもある可能性。実装は未確認。 |
| scope/excluded | 親の別Object、実利用者、第三者環境。 |
| scope/unknown | 実到達、実装、実影響、現在のIdentity binding。 |
| technicalImpact | 供給設計上の権限範囲に差がある。実データへの到達は未確認。 |
| businessImpact | 請求連携の誤処理を懸念する分析仮説。実損害・金額・停止時間は未測定。 |
| limitation | 親や他ScenarioのEvidenceをこの対象・版の実測として利用しない。 |
| confidence | 中 |
| alternative | 供給設計と実装の権限制約が異なる可能性。 |
| priority/severityReference | 第7章の比較方法のみ。新しいScoreは付けない。 |
| priority/cvssScore | null |
| priority/cvssVector | null |
| priority/cvssNomenclature | null |
| priority/automaticDecision | false |
| priority/reason | 業務依存・不足Evidence・変更可能時期をOwnerが別々に比較する。 |
| treatments/0/id | TMP-FRT15-001 |
| treatments/0/kind | Temporary |
| treatments/0/controlId | CTRL-TMP-FRT15-001 |
| treatments/0/proposal | 供給計画の利用Scopeを限定する案。権限宣言自体の修正ではない。 |
| treatments/0/benefit | 判断までの露出を限定する計画。 |
| treatments/0/cost | 必要な連携を制限する可能性。 |
| treatments/0/dependency | 業務Ownerによる対象範囲の確認。 |
| treatments/0/owner | SYNTH-SERVICE-OWNER |
| treatments/0/dueAt | 2026-09-25T00:00:00Z |
| treatments/0/implemented | false |
| treatments/1/id | PERM-FRT15-001 |
| treatments/1/kind | Permanent |
| treatments/1/controlId | CTRL-PERM-FRT15-001 |
| treatments/1/proposal | 供給設計の権限宣言と必要業務を対応付ける改版案。 |
| treatments/1/benefit | 根本条件を変更対象として明示できる。 |
| treatments/1/cost | 連携先との仕様確認が必要。 |
| treatments/1/dependency | 新しい変更計画と別の許可判断。 |
| treatments/1/owner | SYNTH-DESIGN-OWNER |
| treatments/1/dueAt | 2026-09-28T00:00:00Z |
| treatments/1/implemented | false |
| treatments/2/id | COMP-FRT15-001 |
| treatments/2/kind | Compensating |
| treatments/2/controlId | CTRL-COMP-FRT15-001 |
| treatments/2/proposal | 対象・版・判断理由を監査記録へ接続する代替統制案。 |
| treatments/2/benefit | Gapを後続確認へ追跡できる。 |
| treatments/2/cost | 権限宣言の差そのものは残る。 |
| treatments/2/dependency | 必要Telemetryの提供条件。 |
| treatments/2/owner | SYNTH-DETECTION-OWNER |
| treatments/2/dueAt | 2026-09-27T00:00:00Z |
| treatments/2/implemented | false |
| recommendedTreatmentId | PERM-FRT15-001 |
| retestId | RT-FRT15-001 |
| acceptance/present | false |
| acceptance/id | null |
| acceptance/findingId | null |
| acceptance/subjectId | null |
| acceptance/scope | null |
| acceptance/authorityReference | null |
| acceptance/authorityHolder | null |
| acceptance/decisionOwner | null |
| acceptance/basis | null |
| acceptance/decidedAt | null |
| acceptance/expiresAt | null |
| acceptance/residualRiskId | null |
| acceptance/reassessmentId | null |
| acceptance/conditions | null |
| acceptance/overridesAssessmentAuthority | false |
| residualRisk/id | RES-FRT15-001 |
| residualRisk/claim | 実装と業務影響は未確認であり、設計比較の結果からRiskゼロとは言えない。 |
| residualRisk/owner | SYNTH-RISK-OWNER |
| residualRisk/businessRiskZero | false |
| decision/id | DEC-FRT15-001 |
| decision/findingId | FND-FRT15-001 |
| decision/action | Remediate |
| decision/basis | open-review |
| decision/owner | SYNTH-CASE-OWNER |
| decision/reason | 供給資料の差とGapを整理し、実作業とは別に記録の次の担当を決める。 |
| decision/executionAuthorized | false |
| reassessment/id | REA-FRT15-001 |
| reassessment/findingId | FND-FRT15-001 |
| reassessment/owner | SYNTH-CASE-OWNER |
| reassessment/dueAt | 2026-09-20T00:00:00Z |
| reassessment/trigger | Evidence不足・対象版・Scope・受容期限・権限条件の変更。 |
| reassessment/reopenReason | null |
| disclosure/classification | Synthetic teaching only |
| disclosure/audience | Synthetic internal roles |
| disclosure/coordinationStatus | Not initiated |
| disclosure/publicReleaseAuthorized | false |
| disclosure/actualNoticeSent | false |
| temporaryReviewEvidenceId | null |

## findings FND-FRT15-002

| Field | Value |
|---|---|
| id | FND-FRT15-002 |
| scenarioId | SCN-FRT15-002 |
| caseId | CASE-2026-001 |
| assetId | ASSET-2026-005 |
| threatId | TH-2026-004 |
| subjectId | APP-FRT15-001 |
| subjectRevision | BEFORE-FRT15-002 |
| status | Mitigated |
| requestedStage | Mitigate |
| title | 供給OAuth App設計で必要業務より広い権限宣言があるという分析候補。 |
| symptom | 供給設定のpermission欄と業務要件のpermission欄が異なる。 |
| rootCondition/id | ROOT-FRT15-002 |
| rootCondition/claim | 要件と権限宣言の対応を確認する承認条件が供給設計にない。 |
| rootCondition/basis | authored-design-comparison-not-verified-implementation |
| validation/id | VAL-FRT15-002 |
| validation/findingId | FND-FRT15-002 |
| validation/subjectId | APP-FRT15-001 |
| validation/subjectRevision | BEFORE-FRT15-002 |
| validation/method | Static authored comparison |
| validation/requirementPermission | read-summary |
| validation/declaredPermission | read-all-summaries |
| validation/evidenceId | EVD-FRT15-002 |
| validation/basis | authored-supplied-values |
| validation/actualOperation | false |
| evidenceIds/0 | EVD-FRT15-002 |
| scope/confirmed | この供給版の権限宣言文字列だけ。 |
| scope/candidate | 同じ設計条件が実装にもある可能性。実装は未確認。 |
| scope/excluded | 親の別Object、実利用者、第三者環境。 |
| scope/unknown | 実到達、実装、実影響、現在のIdentity binding。 |
| technicalImpact | 供給設計上の権限範囲に差がある。実データへの到達は未確認。 |
| businessImpact | 請求連携の誤処理を懸念する分析仮説。実損害・金額・停止時間は未測定。 |
| limitation | 親や他ScenarioのEvidenceをこの対象・版の実測として利用しない。 |
| confidence | 中 |
| alternative | 供給設計と実装の権限制約が異なる可能性。 |
| priority/severityReference | 第7章の比較方法のみ。新しいScoreは付けない。 |
| priority/cvssScore | null |
| priority/cvssVector | null |
| priority/cvssNomenclature | null |
| priority/automaticDecision | false |
| priority/reason | 業務依存・不足Evidence・変更可能時期をOwnerが別々に比較する。 |
| treatments/0/id | TMP-FRT15-002 |
| treatments/0/kind | Temporary |
| treatments/0/controlId | CTRL-TMP-FRT15-002 |
| treatments/0/proposal | 供給計画の利用Scopeを限定する案。権限宣言自体の修正ではない。 |
| treatments/0/benefit | 判断までの露出を限定する計画。 |
| treatments/0/cost | 必要な連携を制限する可能性。 |
| treatments/0/dependency | 業務Ownerによる対象範囲の確認。 |
| treatments/0/owner | SYNTH-SERVICE-OWNER |
| treatments/0/dueAt | 2026-09-25T00:00:00Z |
| treatments/0/implemented | false |
| treatments/1/id | PERM-FRT15-002 |
| treatments/1/kind | Permanent |
| treatments/1/controlId | CTRL-PERM-FRT15-002 |
| treatments/1/proposal | 供給設計の権限宣言と必要業務を対応付ける改版案。 |
| treatments/1/benefit | 根本条件を変更対象として明示できる。 |
| treatments/1/cost | 連携先との仕様確認が必要。 |
| treatments/1/dependency | 新しい変更計画と別の許可判断。 |
| treatments/1/owner | SYNTH-DESIGN-OWNER |
| treatments/1/dueAt | 2026-09-28T00:00:00Z |
| treatments/1/implemented | false |
| treatments/2/id | COMP-FRT15-002 |
| treatments/2/kind | Compensating |
| treatments/2/controlId | CTRL-COMP-FRT15-002 |
| treatments/2/proposal | 対象・版・判断理由を監査記録へ接続する代替統制案。 |
| treatments/2/benefit | Gapを後続確認へ追跡できる。 |
| treatments/2/cost | 権限宣言の差そのものは残る。 |
| treatments/2/dependency | 必要Telemetryの提供条件。 |
| treatments/2/owner | SYNTH-DETECTION-OWNER |
| treatments/2/dueAt | 2026-09-27T00:00:00Z |
| treatments/2/implemented | false |
| recommendedTreatmentId | PERM-FRT15-002 |
| retestId | RT-FRT15-002 |
| acceptance/present | false |
| acceptance/id | null |
| acceptance/findingId | null |
| acceptance/subjectId | null |
| acceptance/scope | null |
| acceptance/authorityReference | null |
| acceptance/authorityHolder | null |
| acceptance/decisionOwner | null |
| acceptance/basis | null |
| acceptance/decidedAt | null |
| acceptance/expiresAt | null |
| acceptance/residualRiskId | null |
| acceptance/reassessmentId | null |
| acceptance/conditions | null |
| acceptance/overridesAssessmentAuthority | false |
| residualRisk/id | RES-FRT15-002 |
| residualRisk/claim | 実装と業務影響は未確認であり、設計比較の結果からRiskゼロとは言えない。 |
| residualRisk/owner | SYNTH-RISK-OWNER |
| residualRisk/businessRiskZero | false |
| decision/id | DEC-FRT15-002 |
| decision/findingId | FND-FRT15-002 |
| decision/action | Remediate |
| decision/basis | open-review |
| decision/owner | SYNTH-CASE-OWNER |
| decision/reason | 供給資料の差とGapを整理し、実作業とは別に記録の次の担当を決める。 |
| decision/executionAuthorized | false |
| reassessment/id | REA-FRT15-002 |
| reassessment/findingId | FND-FRT15-002 |
| reassessment/owner | SYNTH-CASE-OWNER |
| reassessment/dueAt | 2026-09-20T00:00:00Z |
| reassessment/trigger | Evidence不足・対象版・Scope・受容期限・権限条件の変更。 |
| reassessment/reopenReason | null |
| disclosure/classification | Synthetic teaching only |
| disclosure/audience | Synthetic internal roles |
| disclosure/coordinationStatus | Not initiated |
| disclosure/publicReleaseAuthorized | false |
| disclosure/actualNoticeSent | false |
| temporaryReviewEvidenceId | TMP-EVD-FRT15-002 |

## findings FND-FRT15-003

| Field | Value |
|---|---|
| id | FND-FRT15-003 |
| scenarioId | SCN-FRT15-003 |
| caseId | CASE-2026-001 |
| assetId | ASSET-2026-005 |
| threatId | TH-2026-004 |
| subjectId | APP-FRT15-001 |
| subjectRevision | BEFORE-FRT15-003 |
| status | Accepted |
| requestedStage | Accept |
| title | 供給OAuth App設計で必要業務より広い権限宣言があるという分析候補。 |
| symptom | 供給設定のpermission欄と業務要件のpermission欄が異なる。 |
| rootCondition/id | ROOT-FRT15-003 |
| rootCondition/claim | 要件と権限宣言の対応を確認する承認条件が供給設計にない。 |
| rootCondition/basis | authored-design-comparison-not-verified-implementation |
| validation/id | VAL-FRT15-003 |
| validation/findingId | FND-FRT15-003 |
| validation/subjectId | APP-FRT15-001 |
| validation/subjectRevision | BEFORE-FRT15-003 |
| validation/method | Static authored comparison |
| validation/requirementPermission | read-summary |
| validation/declaredPermission | read-all-summaries |
| validation/evidenceId | EVD-FRT15-003 |
| validation/basis | authored-supplied-values |
| validation/actualOperation | false |
| evidenceIds/0 | EVD-FRT15-003 |
| scope/confirmed | この供給版の権限宣言文字列だけ。 |
| scope/candidate | 同じ設計条件が実装にもある可能性。実装は未確認。 |
| scope/excluded | 親の別Object、実利用者、第三者環境。 |
| scope/unknown | 実到達、実装、実影響、現在のIdentity binding。 |
| technicalImpact | 供給設計上の権限範囲に差がある。実データへの到達は未確認。 |
| businessImpact | 請求連携の誤処理を懸念する分析仮説。実損害・金額・停止時間は未測定。 |
| limitation | 親や他ScenarioのEvidenceをこの対象・版の実測として利用しない。 |
| confidence | 中 |
| alternative | 供給設計と実装の権限制約が異なる可能性。 |
| priority/severityReference | 第7章の比較方法のみ。新しいScoreは付けない。 |
| priority/cvssScore | null |
| priority/cvssVector | null |
| priority/cvssNomenclature | null |
| priority/automaticDecision | false |
| priority/reason | 業務依存・不足Evidence・変更可能時期をOwnerが別々に比較する。 |
| treatments/0/id | TMP-FRT15-003 |
| treatments/0/kind | Temporary |
| treatments/0/controlId | CTRL-TMP-FRT15-003 |
| treatments/0/proposal | 供給計画の利用Scopeを限定する案。権限宣言自体の修正ではない。 |
| treatments/0/benefit | 判断までの露出を限定する計画。 |
| treatments/0/cost | 必要な連携を制限する可能性。 |
| treatments/0/dependency | 業務Ownerによる対象範囲の確認。 |
| treatments/0/owner | SYNTH-SERVICE-OWNER |
| treatments/0/dueAt | 2026-09-25T00:00:00Z |
| treatments/0/implemented | false |
| treatments/1/id | PERM-FRT15-003 |
| treatments/1/kind | Permanent |
| treatments/1/controlId | CTRL-PERM-FRT15-003 |
| treatments/1/proposal | 供給設計の権限宣言と必要業務を対応付ける改版案。 |
| treatments/1/benefit | 根本条件を変更対象として明示できる。 |
| treatments/1/cost | 連携先との仕様確認が必要。 |
| treatments/1/dependency | 新しい変更計画と別の許可判断。 |
| treatments/1/owner | SYNTH-DESIGN-OWNER |
| treatments/1/dueAt | 2026-09-28T00:00:00Z |
| treatments/1/implemented | false |
| treatments/2/id | COMP-FRT15-003 |
| treatments/2/kind | Compensating |
| treatments/2/controlId | CTRL-COMP-FRT15-003 |
| treatments/2/proposal | 対象・版・判断理由を監査記録へ接続する代替統制案。 |
| treatments/2/benefit | Gapを後続確認へ追跡できる。 |
| treatments/2/cost | 権限宣言の差そのものは残る。 |
| treatments/2/dependency | 必要Telemetryの提供条件。 |
| treatments/2/owner | SYNTH-DETECTION-OWNER |
| treatments/2/dueAt | 2026-09-27T00:00:00Z |
| treatments/2/implemented | false |
| recommendedTreatmentId | PERM-FRT15-003 |
| retestId | null |
| acceptance/present | true |
| acceptance/id | ACC-FRT15-003 |
| acceptance/findingId | FND-FRT15-003 |
| acceptance/subjectId | APP-FRT15-001 |
| acceptance/scope | current-supplied-scenario-only |
| acceptance/authorityReference | DELEGATION-FRT15-003 |
| acceptance/authorityHolder | SYNTH-RISK-OWNER |
| acceptance/decisionOwner | SYNTH-RISK-OWNER |
| acceptance/basis | authored-delegation-not-assessment-permission |
| acceptance/decidedAt | 2026-09-14T00:00:00Z |
| acceptance/expiresAt | 2026-09-30T00:00:00Z |
| acceptance/residualRiskId | RES-FRT15-003 |
| acceptance/reassessmentId | REA-FRT15-003 |
| acceptance/conditions | 対象版・Scope・Evidence・担当が変われば受容判断を再開する。 |
| acceptance/overridesAssessmentAuthority | false |
| residualRisk/id | RES-FRT15-003 |
| residualRisk/claim | 実装と業務影響は未確認であり、設計比較の結果からRiskゼロとは言えない。 |
| residualRisk/owner | SYNTH-RISK-OWNER |
| residualRisk/businessRiskZero | false |
| decision/id | DEC-FRT15-003 |
| decision/findingId | FND-FRT15-003 |
| decision/action | Accept |
| decision/basis | acceptance |
| decision/owner | SYNTH-CASE-OWNER |
| decision/reason | 供給資料の差とGapを整理し、実作業とは別に記録の次の担当を決める。 |
| decision/executionAuthorized | false |
| reassessment/id | REA-FRT15-003 |
| reassessment/findingId | FND-FRT15-003 |
| reassessment/owner | SYNTH-CASE-OWNER |
| reassessment/dueAt | 2026-09-20T00:00:00Z |
| reassessment/trigger | Evidence不足・対象版・Scope・受容期限・権限条件の変更。 |
| reassessment/reopenReason | null |
| disclosure/classification | Synthetic teaching only |
| disclosure/audience | Synthetic internal roles |
| disclosure/coordinationStatus | Not initiated |
| disclosure/publicReleaseAuthorized | false |
| disclosure/actualNoticeSent | false |
| temporaryReviewEvidenceId | null |

## findings FND-FRT15-004

| Field | Value |
|---|---|
| id | FND-FRT15-004 |
| scenarioId | SCN-FRT15-004 |
| caseId | CASE-2026-001 |
| assetId | ASSET-2026-005 |
| threatId | TH-2026-004 |
| subjectId | APP-FRT15-001 |
| subjectRevision | BEFORE-FRT15-004 |
| status | Retest required |
| requestedStage | Retest |
| title | 供給OAuth App設計で必要業務より広い権限宣言があるという分析候補。 |
| symptom | 供給設定のpermission欄と業務要件のpermission欄が異なる。 |
| rootCondition/id | ROOT-FRT15-004 |
| rootCondition/claim | 要件と権限宣言の対応を確認する承認条件が供給設計にない。 |
| rootCondition/basis | authored-design-comparison-not-verified-implementation |
| validation/id | VAL-FRT15-004 |
| validation/findingId | FND-FRT15-004 |
| validation/subjectId | APP-FRT15-001 |
| validation/subjectRevision | BEFORE-FRT15-004 |
| validation/method | Static authored comparison |
| validation/requirementPermission | read-summary |
| validation/declaredPermission | read-all-summaries |
| validation/evidenceId | EVD-FRT15-004 |
| validation/basis | authored-supplied-values |
| validation/actualOperation | false |
| evidenceIds/0 | EVD-FRT15-004 |
| scope/confirmed | この供給版の権限宣言文字列だけ。 |
| scope/candidate | 同じ設計条件が実装にもある可能性。実装は未確認。 |
| scope/excluded | 親の別Object、実利用者、第三者環境。 |
| scope/unknown | 実到達、実装、実影響、現在のIdentity binding。 |
| technicalImpact | 供給設計上の権限範囲に差がある。実データへの到達は未確認。 |
| businessImpact | 請求連携の誤処理を懸念する分析仮説。実損害・金額・停止時間は未測定。 |
| limitation | 親や他ScenarioのEvidenceをこの対象・版の実測として利用しない。 |
| confidence | 中 |
| alternative | 供給設計と実装の権限制約が異なる可能性。 |
| priority/severityReference | 第7章の比較方法のみ。新しいScoreは付けない。 |
| priority/cvssScore | null |
| priority/cvssVector | null |
| priority/cvssNomenclature | null |
| priority/automaticDecision | false |
| priority/reason | 業務依存・不足Evidence・変更可能時期をOwnerが別々に比較する。 |
| treatments/0/id | TMP-FRT15-004 |
| treatments/0/kind | Temporary |
| treatments/0/controlId | CTRL-TMP-FRT15-004 |
| treatments/0/proposal | 供給計画の利用Scopeを限定する案。権限宣言自体の修正ではない。 |
| treatments/0/benefit | 判断までの露出を限定する計画。 |
| treatments/0/cost | 必要な連携を制限する可能性。 |
| treatments/0/dependency | 業務Ownerによる対象範囲の確認。 |
| treatments/0/owner | SYNTH-SERVICE-OWNER |
| treatments/0/dueAt | 2026-09-25T00:00:00Z |
| treatments/0/implemented | false |
| treatments/1/id | PERM-FRT15-004 |
| treatments/1/kind | Permanent |
| treatments/1/controlId | CTRL-PERM-FRT15-004 |
| treatments/1/proposal | 供給設計の権限宣言と必要業務を対応付ける改版案。 |
| treatments/1/benefit | 根本条件を変更対象として明示できる。 |
| treatments/1/cost | 連携先との仕様確認が必要。 |
| treatments/1/dependency | 新しい変更計画と別の許可判断。 |
| treatments/1/owner | SYNTH-DESIGN-OWNER |
| treatments/1/dueAt | 2026-09-28T00:00:00Z |
| treatments/1/implemented | false |
| treatments/2/id | COMP-FRT15-004 |
| treatments/2/kind | Compensating |
| treatments/2/controlId | CTRL-COMP-FRT15-004 |
| treatments/2/proposal | 対象・版・判断理由を監査記録へ接続する代替統制案。 |
| treatments/2/benefit | Gapを後続確認へ追跡できる。 |
| treatments/2/cost | 権限宣言の差そのものは残る。 |
| treatments/2/dependency | 必要Telemetryの提供条件。 |
| treatments/2/owner | SYNTH-DETECTION-OWNER |
| treatments/2/dueAt | 2026-09-27T00:00:00Z |
| treatments/2/implemented | false |
| recommendedTreatmentId | PERM-FRT15-004 |
| retestId | RT-FRT15-004 |
| acceptance/present | false |
| acceptance/id | null |
| acceptance/findingId | null |
| acceptance/subjectId | null |
| acceptance/scope | null |
| acceptance/authorityReference | null |
| acceptance/authorityHolder | null |
| acceptance/decisionOwner | null |
| acceptance/basis | null |
| acceptance/decidedAt | null |
| acceptance/expiresAt | null |
| acceptance/residualRiskId | null |
| acceptance/reassessmentId | null |
| acceptance/conditions | null |
| acceptance/overridesAssessmentAuthority | false |
| residualRisk/id | RES-FRT15-004 |
| residualRisk/claim | 実装と業務影響は未確認であり、設計比較の結果からRiskゼロとは言えない。 |
| residualRisk/owner | SYNTH-RISK-OWNER |
| residualRisk/businessRiskZero | false |
| decision/id | DEC-FRT15-004 |
| decision/findingId | FND-FRT15-004 |
| decision/action | Remediate |
| decision/basis | open-review |
| decision/owner | SYNTH-CASE-OWNER |
| decision/reason | 供給資料の差とGapを整理し、実作業とは別に記録の次の担当を決める。 |
| decision/executionAuthorized | false |
| reassessment/id | REA-FRT15-004 |
| reassessment/findingId | FND-FRT15-004 |
| reassessment/owner | SYNTH-CASE-OWNER |
| reassessment/dueAt | 2026-09-20T00:00:00Z |
| reassessment/trigger | Evidence不足・対象版・Scope・受容期限・権限条件の変更。 |
| reassessment/reopenReason | null |
| disclosure/classification | Synthetic teaching only |
| disclosure/audience | Synthetic internal roles |
| disclosure/coordinationStatus | Not initiated |
| disclosure/publicReleaseAuthorized | false |
| disclosure/actualNoticeSent | false |
| temporaryReviewEvidenceId | null |

## findings FND-FRT15-005

| Field | Value |
|---|---|
| id | FND-FRT15-005 |
| scenarioId | SCN-FRT15-005 |
| caseId | CASE-2026-001 |
| assetId | ASSET-2026-005 |
| threatId | TH-2026-004 |
| subjectId | APP-FRT15-001 |
| subjectRevision | BEFORE-FRT15-005 |
| status | Closed |
| requestedStage | Close |
| title | 供給OAuth App設計で必要業務より広い権限宣言があるという分析候補。 |
| symptom | 供給設定のpermission欄と業務要件のpermission欄が異なる。 |
| rootCondition/id | ROOT-FRT15-005 |
| rootCondition/claim | 要件と権限宣言の対応を確認する承認条件が供給設計にない。 |
| rootCondition/basis | authored-design-comparison-not-verified-implementation |
| validation/id | VAL-FRT15-005 |
| validation/findingId | FND-FRT15-005 |
| validation/subjectId | APP-FRT15-001 |
| validation/subjectRevision | BEFORE-FRT15-005 |
| validation/method | Static authored comparison |
| validation/requirementPermission | read-summary |
| validation/declaredPermission | read-all-summaries |
| validation/evidenceId | EVD-FRT15-005 |
| validation/basis | authored-supplied-values |
| validation/actualOperation | false |
| evidenceIds/0 | EVD-FRT15-005 |
| scope/confirmed | この供給版の権限宣言文字列だけ。 |
| scope/candidate | 同じ設計条件が実装にもある可能性。実装は未確認。 |
| scope/excluded | 親の別Object、実利用者、第三者環境。 |
| scope/unknown | 実到達、実装、実影響、現在のIdentity binding。 |
| technicalImpact | 供給設計上の権限範囲に差がある。実データへの到達は未確認。 |
| businessImpact | 請求連携の誤処理を懸念する分析仮説。実損害・金額・停止時間は未測定。 |
| limitation | 親や他ScenarioのEvidenceをこの対象・版の実測として利用しない。 |
| confidence | 中 |
| alternative | 供給設計と実装の権限制約が異なる可能性。 |
| priority/severityReference | 第7章の比較方法のみ。新しいScoreは付けない。 |
| priority/cvssScore | null |
| priority/cvssVector | null |
| priority/cvssNomenclature | null |
| priority/automaticDecision | false |
| priority/reason | 業務依存・不足Evidence・変更可能時期をOwnerが別々に比較する。 |
| treatments/0/id | TMP-FRT15-005 |
| treatments/0/kind | Temporary |
| treatments/0/controlId | CTRL-TMP-FRT15-005 |
| treatments/0/proposal | 供給計画の利用Scopeを限定する案。権限宣言自体の修正ではない。 |
| treatments/0/benefit | 判断までの露出を限定する計画。 |
| treatments/0/cost | 必要な連携を制限する可能性。 |
| treatments/0/dependency | 業務Ownerによる対象範囲の確認。 |
| treatments/0/owner | SYNTH-SERVICE-OWNER |
| treatments/0/dueAt | 2026-09-25T00:00:00Z |
| treatments/0/implemented | false |
| treatments/1/id | PERM-FRT15-005 |
| treatments/1/kind | Permanent |
| treatments/1/controlId | CTRL-PERM-FRT15-005 |
| treatments/1/proposal | 供給設計の権限宣言と必要業務を対応付ける改版案。 |
| treatments/1/benefit | 根本条件を変更対象として明示できる。 |
| treatments/1/cost | 連携先との仕様確認が必要。 |
| treatments/1/dependency | 新しい変更計画と別の許可判断。 |
| treatments/1/owner | SYNTH-DESIGN-OWNER |
| treatments/1/dueAt | 2026-09-28T00:00:00Z |
| treatments/1/implemented | false |
| treatments/2/id | COMP-FRT15-005 |
| treatments/2/kind | Compensating |
| treatments/2/controlId | CTRL-COMP-FRT15-005 |
| treatments/2/proposal | 対象・版・判断理由を監査記録へ接続する代替統制案。 |
| treatments/2/benefit | Gapを後続確認へ追跡できる。 |
| treatments/2/cost | 権限宣言の差そのものは残る。 |
| treatments/2/dependency | 必要Telemetryの提供条件。 |
| treatments/2/owner | SYNTH-DETECTION-OWNER |
| treatments/2/dueAt | 2026-09-27T00:00:00Z |
| treatments/2/implemented | false |
| recommendedTreatmentId | PERM-FRT15-005 |
| retestId | RT-FRT15-005 |
| acceptance/present | false |
| acceptance/id | null |
| acceptance/findingId | null |
| acceptance/subjectId | null |
| acceptance/scope | null |
| acceptance/authorityReference | null |
| acceptance/authorityHolder | null |
| acceptance/decisionOwner | null |
| acceptance/basis | null |
| acceptance/decidedAt | null |
| acceptance/expiresAt | null |
| acceptance/residualRiskId | null |
| acceptance/reassessmentId | null |
| acceptance/conditions | null |
| acceptance/overridesAssessmentAuthority | false |
| residualRisk/id | RES-FRT15-005 |
| residualRisk/claim | 実装と業務影響は未確認であり、設計比較の結果からRiskゼロとは言えない。 |
| residualRisk/owner | SYNTH-RISK-OWNER |
| residualRisk/businessRiskZero | false |
| decision/id | DEC-FRT15-005 |
| decision/findingId | FND-FRT15-005 |
| decision/action | Remediate |
| decision/basis | retest |
| decision/owner | SYNTH-CASE-OWNER |
| decision/reason | 供給資料の差とGapを整理し、実作業とは別に記録の次の担当を決める。 |
| decision/executionAuthorized | false |
| reassessment/id | REA-FRT15-005 |
| reassessment/findingId | FND-FRT15-005 |
| reassessment/owner | SYNTH-CASE-OWNER |
| reassessment/dueAt | 2026-09-20T00:00:00Z |
| reassessment/trigger | Evidence不足・対象版・Scope・受容期限・権限条件の変更。 |
| reassessment/reopenReason | null |
| disclosure/classification | Synthetic teaching only |
| disclosure/audience | Synthetic internal roles |
| disclosure/coordinationStatus | Not initiated |
| disclosure/publicReleaseAuthorized | false |
| disclosure/actualNoticeSent | false |
| temporaryReviewEvidenceId | null |

## findings FND-FRT15-006

| Field | Value |
|---|---|
| id | FND-FRT15-006 |
| scenarioId | SCN-FRT15-006 |
| caseId | CASE-2026-001 |
| assetId | ASSET-2026-005 |
| threatId | TH-2026-004 |
| subjectId | APP-FRT15-001 |
| subjectRevision | BEFORE-FRT15-006 |
| status | Reopened |
| requestedStage | Reopen |
| title | 供給OAuth App設計で必要業務より広い権限宣言があるという分析候補。 |
| symptom | 供給設定のpermission欄と業務要件のpermission欄が異なる。 |
| rootCondition/id | ROOT-FRT15-006 |
| rootCondition/claim | 要件と権限宣言の対応を確認する承認条件が供給設計にない。 |
| rootCondition/basis | authored-design-comparison-not-verified-implementation |
| validation/id | VAL-FRT15-006 |
| validation/findingId | FND-FRT15-006 |
| validation/subjectId | APP-FRT15-001 |
| validation/subjectRevision | BEFORE-FRT15-006 |
| validation/method | Static authored comparison |
| validation/requirementPermission | read-summary |
| validation/declaredPermission | read-all-summaries |
| validation/evidenceId | EVD-FRT15-006 |
| validation/basis | authored-supplied-values |
| validation/actualOperation | false |
| evidenceIds/0 | EVD-FRT15-006 |
| scope/confirmed | この供給版の権限宣言文字列だけ。 |
| scope/candidate | 同じ設計条件が実装にもある可能性。実装は未確認。 |
| scope/excluded | 親の別Object、実利用者、第三者環境。 |
| scope/unknown | 実到達、実装、実影響、現在のIdentity binding。 |
| technicalImpact | 供給設計上の権限範囲に差がある。実データへの到達は未確認。 |
| businessImpact | 請求連携の誤処理を懸念する分析仮説。実損害・金額・停止時間は未測定。 |
| limitation | 親や他ScenarioのEvidenceをこの対象・版の実測として利用しない。 |
| confidence | 中 |
| alternative | 供給設計と実装の権限制約が異なる可能性。 |
| priority/severityReference | 第7章の比較方法のみ。新しいScoreは付けない。 |
| priority/cvssScore | null |
| priority/cvssVector | null |
| priority/cvssNomenclature | null |
| priority/automaticDecision | false |
| priority/reason | 業務依存・不足Evidence・変更可能時期をOwnerが別々に比較する。 |
| treatments/0/id | TMP-FRT15-006 |
| treatments/0/kind | Temporary |
| treatments/0/controlId | CTRL-TMP-FRT15-006 |
| treatments/0/proposal | 供給計画の利用Scopeを限定する案。権限宣言自体の修正ではない。 |
| treatments/0/benefit | 判断までの露出を限定する計画。 |
| treatments/0/cost | 必要な連携を制限する可能性。 |
| treatments/0/dependency | 業務Ownerによる対象範囲の確認。 |
| treatments/0/owner | SYNTH-SERVICE-OWNER |
| treatments/0/dueAt | 2026-09-25T00:00:00Z |
| treatments/0/implemented | false |
| treatments/1/id | PERM-FRT15-006 |
| treatments/1/kind | Permanent |
| treatments/1/controlId | CTRL-PERM-FRT15-006 |
| treatments/1/proposal | 供給設計の権限宣言と必要業務を対応付ける改版案。 |
| treatments/1/benefit | 根本条件を変更対象として明示できる。 |
| treatments/1/cost | 連携先との仕様確認が必要。 |
| treatments/1/dependency | 新しい変更計画と別の許可判断。 |
| treatments/1/owner | SYNTH-DESIGN-OWNER |
| treatments/1/dueAt | 2026-09-28T00:00:00Z |
| treatments/1/implemented | false |
| treatments/2/id | COMP-FRT15-006 |
| treatments/2/kind | Compensating |
| treatments/2/controlId | CTRL-COMP-FRT15-006 |
| treatments/2/proposal | 対象・版・判断理由を監査記録へ接続する代替統制案。 |
| treatments/2/benefit | Gapを後続確認へ追跡できる。 |
| treatments/2/cost | 権限宣言の差そのものは残る。 |
| treatments/2/dependency | 必要Telemetryの提供条件。 |
| treatments/2/owner | SYNTH-DETECTION-OWNER |
| treatments/2/dueAt | 2026-09-27T00:00:00Z |
| treatments/2/implemented | false |
| recommendedTreatmentId | PERM-FRT15-006 |
| retestId | RT-FRT15-006 |
| acceptance/present | true |
| acceptance/id | ACC-FRT15-006 |
| acceptance/findingId | FND-FRT15-006 |
| acceptance/subjectId | APP-FRT15-001 |
| acceptance/scope | current-supplied-scenario-only |
| acceptance/authorityReference | DELEGATION-FRT15-006 |
| acceptance/authorityHolder | SYNTH-RISK-OWNER |
| acceptance/decisionOwner | SYNTH-RISK-OWNER |
| acceptance/basis | authored-delegation-not-assessment-permission |
| acceptance/decidedAt | 2026-09-14T00:00:00Z |
| acceptance/expiresAt | 2026-09-15T00:00:00Z |
| acceptance/residualRiskId | RES-FRT15-006 |
| acceptance/reassessmentId | REA-FRT15-006 |
| acceptance/conditions | 対象版・Scope・Evidence・担当が変われば受容判断を再開する。 |
| acceptance/overridesAssessmentAuthority | false |
| residualRisk/id | RES-FRT15-006 |
| residualRisk/claim | 実装と業務影響は未確認であり、設計比較の結果からRiskゼロとは言えない。 |
| residualRisk/owner | SYNTH-RISK-OWNER |
| residualRisk/businessRiskZero | false |
| decision/id | DEC-FRT15-006 |
| decision/findingId | FND-FRT15-006 |
| decision/action | Remediate |
| decision/basis | open-review |
| decision/owner | SYNTH-CASE-OWNER |
| decision/reason | 供給資料の差とGapを整理し、実作業とは別に記録の次の担当を決める。 |
| decision/executionAuthorized | false |
| reassessment/id | REA-FRT15-006 |
| reassessment/findingId | FND-FRT15-006 |
| reassessment/owner | SYNTH-CASE-OWNER |
| reassessment/dueAt | 2026-09-20T00:00:00Z |
| reassessment/trigger | Evidence不足・対象版・Scope・受容期限・権限条件の変更。 |
| reassessment/reopenReason | 停止と過去受容の期限切れを供給記録から確認した。 |
| disclosure/classification | Synthetic teaching only |
| disclosure/audience | Synthetic internal roles |
| disclosure/coordinationStatus | Not initiated |
| disclosure/publicReleaseAuthorized | false |
| disclosure/actualNoticeSent | false |
| temporaryReviewEvidenceId | null |

## findings FND-FRT15-007

| Field | Value |
|---|---|
| id | FND-FRT15-007 |
| scenarioId | SCN-FRT15-007 |
| caseId | CASE-2026-001 |
| assetId | ASSET-2026-005 |
| threatId | TH-2026-004 |
| subjectId | APP-FRT15-001 |
| subjectRevision | BEFORE-FRT15-007 |
| status | Closed |
| requestedStage | Close |
| title | 供給OAuth App設計で必要業務より広い権限宣言があるという分析候補。 |
| symptom | 供給設定のpermission欄と業務要件のpermission欄が異なる。 |
| rootCondition/id | ROOT-FRT15-007 |
| rootCondition/claim | 要件と権限宣言の対応を確認する承認条件が供給設計にない。 |
| rootCondition/basis | authored-design-comparison-not-verified-implementation |
| validation/id | VAL-FRT15-007 |
| validation/findingId | FND-FRT15-007 |
| validation/subjectId | APP-FRT15-001 |
| validation/subjectRevision | BEFORE-FRT15-007 |
| validation/method | Static authored comparison |
| validation/requirementPermission | read-summary |
| validation/declaredPermission | read-all-summaries |
| validation/evidenceId | EVD-FRT15-007 |
| validation/basis | authored-supplied-values |
| validation/actualOperation | false |
| evidenceIds/0 | EVD-FRT15-007 |
| scope/confirmed | この供給版の権限宣言文字列だけ。 |
| scope/candidate | 同じ設計条件が実装にもある可能性。実装は未確認。 |
| scope/excluded | 親の別Object、実利用者、第三者環境。 |
| scope/unknown | 実到達、実装、実影響、現在のIdentity binding。 |
| technicalImpact | 供給設計上の権限範囲に差がある。実データへの到達は未確認。 |
| businessImpact | 請求連携の誤処理を懸念する分析仮説。実損害・金額・停止時間は未測定。 |
| limitation | 親や他ScenarioのEvidenceをこの対象・版の実測として利用しない。 |
| confidence | 中 |
| alternative | 供給設計と実装の権限制約が異なる可能性。 |
| priority/severityReference | 第7章の比較方法のみ。新しいScoreは付けない。 |
| priority/cvssScore | null |
| priority/cvssVector | null |
| priority/cvssNomenclature | null |
| priority/automaticDecision | false |
| priority/reason | 業務依存・不足Evidence・変更可能時期をOwnerが別々に比較する。 |
| treatments/0/id | TMP-FRT15-007 |
| treatments/0/kind | Temporary |
| treatments/0/controlId | CTRL-TMP-FRT15-007 |
| treatments/0/proposal | 供給計画の利用Scopeを限定する案。権限宣言自体の修正ではない。 |
| treatments/0/benefit | 判断までの露出を限定する計画。 |
| treatments/0/cost | 必要な連携を制限する可能性。 |
| treatments/0/dependency | 業務Ownerによる対象範囲の確認。 |
| treatments/0/owner | SYNTH-SERVICE-OWNER |
| treatments/0/dueAt | 2026-09-25T00:00:00Z |
| treatments/0/implemented | false |
| treatments/1/id | PERM-FRT15-007 |
| treatments/1/kind | Permanent |
| treatments/1/controlId | CTRL-PERM-FRT15-007 |
| treatments/1/proposal | 供給設計の権限宣言と必要業務を対応付ける改版案。 |
| treatments/1/benefit | 根本条件を変更対象として明示できる。 |
| treatments/1/cost | 連携先との仕様確認が必要。 |
| treatments/1/dependency | 新しい変更計画と別の許可判断。 |
| treatments/1/owner | SYNTH-DESIGN-OWNER |
| treatments/1/dueAt | 2026-09-28T00:00:00Z |
| treatments/1/implemented | false |
| treatments/2/id | COMP-FRT15-007 |
| treatments/2/kind | Compensating |
| treatments/2/controlId | CTRL-COMP-FRT15-007 |
| treatments/2/proposal | 対象・版・判断理由を監査記録へ接続する代替統制案。 |
| treatments/2/benefit | Gapを後続確認へ追跡できる。 |
| treatments/2/cost | 権限宣言の差そのものは残る。 |
| treatments/2/dependency | 必要Telemetryの提供条件。 |
| treatments/2/owner | SYNTH-DETECTION-OWNER |
| treatments/2/dueAt | 2026-09-27T00:00:00Z |
| treatments/2/implemented | false |
| recommendedTreatmentId | PERM-FRT15-007 |
| retestId | null |
| acceptance/present | true |
| acceptance/id | ACC-FRT15-007 |
| acceptance/findingId | FND-FRT15-007 |
| acceptance/subjectId | APP-FRT15-001 |
| acceptance/scope | current-supplied-scenario-only |
| acceptance/authorityReference | DELEGATION-FRT15-007 |
| acceptance/authorityHolder | SYNTH-RISK-OWNER |
| acceptance/decisionOwner | SYNTH-RISK-OWNER |
| acceptance/basis | authored-delegation-not-assessment-permission |
| acceptance/decidedAt | 2026-09-14T00:00:00Z |
| acceptance/expiresAt | 2026-09-30T00:00:00Z |
| acceptance/residualRiskId | RES-FRT15-007 |
| acceptance/reassessmentId | REA-FRT15-007 |
| acceptance/conditions | 対象版・Scope・Evidence・担当が変われば受容判断を再開する。 |
| acceptance/overridesAssessmentAuthority | false |
| residualRisk/id | RES-FRT15-007 |
| residualRisk/claim | 実装と業務影響は未確認であり、設計比較の結果からRiskゼロとは言えない。 |
| residualRisk/owner | SYNTH-RISK-OWNER |
| residualRisk/businessRiskZero | false |
| decision/id | DEC-FRT15-007 |
| decision/findingId | FND-FRT15-007 |
| decision/action | Accept |
| decision/basis | acceptance |
| decision/owner | SYNTH-CASE-OWNER |
| decision/reason | 供給資料の差とGapを整理し、実作業とは別に記録の次の担当を決める。 |
| decision/executionAuthorized | false |
| reassessment/id | REA-FRT15-007 |
| reassessment/findingId | FND-FRT15-007 |
| reassessment/owner | SYNTH-CASE-OWNER |
| reassessment/dueAt | 2026-09-20T00:00:00Z |
| reassessment/trigger | Evidence不足・対象版・Scope・受容期限・権限条件の変更。 |
| reassessment/reopenReason | null |
| disclosure/classification | Synthetic teaching only |
| disclosure/audience | Synthetic internal roles |
| disclosure/coordinationStatus | Not initiated |
| disclosure/publicReleaseAuthorized | false |
| disclosure/actualNoticeSent | false |
| temporaryReviewEvidenceId | null |

## retests RT-FRT15-001

| Field | Value |
|---|---|
| id | RT-FRT15-001 |
| findingId | FND-FRT15-001 |
| subjectId | APP-FRT15-001 |
| beforeRevision | BEFORE-FRT15-001 |
| changeReference | CHG-FRT15-001 |
| changedRevision | AFTER-FRT15-001 |
| changeMeaning | authored-change-summary-not-real-change |
| scope | current-supplied-scenario-only |
| method | Static authored comparison |
| requiredMethod | Static authored comparison |
| criteria/0/id | CRT-FRT15-001-1 |
| criteria/0/field | permission |
| criteria/0/expected | read-summary |
| criteria/1/id | CRT-FRT15-001-2 |
| criteria/1/field | auditReference |
| criteria/1/expected | AUD-FRT15-EXPECTED |
| observations/0/id | RT-EVD-FRT15-001-1 |
| observations/0/criterionId | CRT-FRT15-001-1 |
| observations/0/subjectId | APP-FRT15-001 |
| observations/0/revision | AFTER-FRT15-001 |
| observations/0/present | true |
| observations/0/value | read-all-summaries |
| observations/0/basis | authored-supplied-value |
| observations/1/id | RT-EVD-FRT15-001-2 |
| observations/1/criterionId | CRT-FRT15-001-2 |
| observations/1/subjectId | APP-FRT15-001 |
| observations/1/revision | AFTER-FRT15-001 |
| observations/1/present | true |
| observations/1/value | AUD-FRT15-EXPECTED |
| observations/1/basis | authored-supplied-value |
| result | Failed |
| stopTrigger | None |
| stepsAfterStop | 0 |
| actualOperations | 0 |
| owner | SYNTH-RETEST-REVIEWER |
| recordedAt | 2026-09-16T22:00:00Z |
| limitation | 二つの供給欄だけを比較。実ScannerやBusiness Logicの動作試験は行っていない。 |
| regressionScope | 同じ供給Scenarioの二条件だけ。全System非回帰ではない。 |
| residualRiskId | RES-FRT15-001 |
| reassessmentId | REA-FRT15-001 |

## retests RT-FRT15-002

| Field | Value |
|---|---|
| id | RT-FRT15-002 |
| findingId | FND-FRT15-002 |
| subjectId | APP-FRT15-001 |
| beforeRevision | BEFORE-FRT15-002 |
| changeReference | CHG-FRT15-002 |
| changedRevision | AFTER-FRT15-002 |
| changeMeaning | authored-change-summary-not-real-change |
| scope | current-supplied-scenario-only |
| method | Static authored comparison |
| requiredMethod | Static authored comparison |
| criteria/0/id | CRT-FRT15-002-1 |
| criteria/0/field | permission |
| criteria/0/expected | read-summary |
| criteria/1/id | CRT-FRT15-002-2 |
| criteria/1/field | auditReference |
| criteria/1/expected | AUD-FRT15-EXPECTED |
| observations/0/id | RT-EVD-FRT15-002-1 |
| observations/0/criterionId | CRT-FRT15-002-1 |
| observations/0/subjectId | APP-FRT15-001 |
| observations/0/revision | AFTER-FRT15-002 |
| observations/0/present | true |
| observations/0/value | read-summary |
| observations/0/basis | authored-supplied-value |
| observations/1/id | RT-EVD-FRT15-002-2 |
| observations/1/criterionId | CRT-FRT15-002-2 |
| observations/1/subjectId | APP-FRT15-001 |
| observations/1/revision | AFTER-FRT15-002 |
| observations/1/present | true |
| observations/1/value | AUD-FRT15-OTHER |
| observations/1/basis | authored-supplied-value |
| result | Partial |
| stopTrigger | None |
| stepsAfterStop | 0 |
| actualOperations | 0 |
| owner | SYNTH-RETEST-REVIEWER |
| recordedAt | 2026-09-16T22:00:00Z |
| limitation | 二つの供給欄だけを比較。実ScannerやBusiness Logicの動作試験は行っていない。 |
| regressionScope | 同じ供給Scenarioの二条件だけ。全System非回帰ではない。 |
| residualRiskId | RES-FRT15-002 |
| reassessmentId | REA-FRT15-002 |

## retests RT-FRT15-004

| Field | Value |
|---|---|
| id | RT-FRT15-004 |
| findingId | FND-FRT15-004 |
| subjectId | APP-FRT15-001 |
| beforeRevision | BEFORE-FRT15-004 |
| changeReference | CHG-FRT15-004 |
| changedRevision | AFTER-FRT15-004 |
| changeMeaning | authored-change-summary-not-real-change |
| scope | current-supplied-scenario-only |
| method | Scanner summary only |
| requiredMethod | Static authored comparison |
| criteria/0/id | CRT-FRT15-004-1 |
| criteria/0/field | permission |
| criteria/0/expected | read-summary |
| criteria/1/id | CRT-FRT15-004-2 |
| criteria/1/field | auditReference |
| criteria/1/expected | AUD-FRT15-EXPECTED |
| observations/0/id | RT-EVD-FRT15-004-1 |
| observations/0/criterionId | CRT-FRT15-004-1 |
| observations/0/subjectId | APP-FRT15-001 |
| observations/0/revision | AFTER-FRT15-004 |
| observations/0/present | false |
| observations/0/value | null |
| observations/0/basis | missing-not-failed |
| observations/1/id | RT-EVD-FRT15-004-2 |
| observations/1/criterionId | CRT-FRT15-004-2 |
| observations/1/subjectId | APP-FRT15-001 |
| observations/1/revision | AFTER-FRT15-004 |
| observations/1/present | false |
| observations/1/value | null |
| observations/1/basis | missing-not-failed |
| result | Inconclusive |
| stopTrigger | None |
| stepsAfterStop | 0 |
| actualOperations | 0 |
| owner | SYNTH-RETEST-REVIEWER |
| recordedAt | 2026-09-16T22:00:00Z |
| limitation | 二つの供給欄だけを比較。実ScannerやBusiness Logicの動作試験は行っていない。 |
| regressionScope | 同じ供給Scenarioの二条件だけ。全System非回帰ではない。 |
| residualRiskId | RES-FRT15-004 |
| reassessmentId | REA-FRT15-004 |

## retests RT-FRT15-005

| Field | Value |
|---|---|
| id | RT-FRT15-005 |
| findingId | FND-FRT15-005 |
| subjectId | APP-FRT15-001 |
| beforeRevision | BEFORE-FRT15-005 |
| changeReference | CHG-FRT15-005 |
| changedRevision | AFTER-FRT15-005 |
| changeMeaning | authored-change-summary-not-real-change |
| scope | current-supplied-scenario-only |
| method | Static authored comparison |
| requiredMethod | Static authored comparison |
| criteria/0/id | CRT-FRT15-005-1 |
| criteria/0/field | permission |
| criteria/0/expected | read-summary |
| criteria/1/id | CRT-FRT15-005-2 |
| criteria/1/field | auditReference |
| criteria/1/expected | AUD-FRT15-EXPECTED |
| observations/0/id | RT-EVD-FRT15-005-1 |
| observations/0/criterionId | CRT-FRT15-005-1 |
| observations/0/subjectId | APP-FRT15-001 |
| observations/0/revision | AFTER-FRT15-005 |
| observations/0/present | true |
| observations/0/value | read-summary |
| observations/0/basis | authored-supplied-value |
| observations/1/id | RT-EVD-FRT15-005-2 |
| observations/1/criterionId | CRT-FRT15-005-2 |
| observations/1/subjectId | APP-FRT15-001 |
| observations/1/revision | AFTER-FRT15-005 |
| observations/1/present | true |
| observations/1/value | AUD-FRT15-EXPECTED |
| observations/1/basis | authored-supplied-value |
| result | Passed |
| stopTrigger | None |
| stepsAfterStop | 0 |
| actualOperations | 0 |
| owner | SYNTH-RETEST-REVIEWER |
| recordedAt | 2026-09-16T22:00:00Z |
| limitation | 二つの供給欄だけを比較。実ScannerやBusiness Logicの動作試験は行っていない。 |
| regressionScope | 同じ供給Scenarioの二条件だけ。全System非回帰ではない。 |
| residualRiskId | RES-FRT15-005 |
| reassessmentId | REA-FRT15-005 |

## retests RT-FRT15-006

| Field | Value |
|---|---|
| id | RT-FRT15-006 |
| findingId | FND-FRT15-006 |
| subjectId | APP-FRT15-001 |
| beforeRevision | BEFORE-FRT15-006 |
| changeReference | CHG-FRT15-006 |
| changedRevision | AFTER-FRT15-006 |
| changeMeaning | authored-change-summary-not-real-change |
| scope | current-supplied-scenario-only |
| method | Static authored comparison |
| requiredMethod | Static authored comparison |
| criteria/0/id | CRT-FRT15-006-1 |
| criteria/0/field | permission |
| criteria/0/expected | read-summary |
| criteria/1/id | CRT-FRT15-006-2 |
| criteria/1/field | auditReference |
| criteria/1/expected | AUD-FRT15-EXPECTED |
| observations/0/id | RT-EVD-FRT15-006-1 |
| observations/0/criterionId | CRT-FRT15-006-1 |
| observations/0/subjectId | APP-FRT15-001 |
| observations/0/revision | AFTER-FRT15-006 |
| observations/0/present | true |
| observations/0/value | read-summary |
| observations/0/basis | authored-supplied-value |
| observations/1/id | RT-EVD-FRT15-006-2 |
| observations/1/criterionId | CRT-FRT15-006-2 |
| observations/1/subjectId | APP-FRT15-001 |
| observations/1/revision | AFTER-FRT15-006 |
| observations/1/present | true |
| observations/1/value | AUD-FRT15-EXPECTED |
| observations/1/basis | authored-supplied-value |
| result | Stopped |
| stopTrigger | Unexpected-input-symbol |
| stepsAfterStop | 0 |
| actualOperations | 0 |
| owner | SYNTH-RETEST-REVIEWER |
| recordedAt | 2026-09-16T22:00:00Z |
| limitation | 二つの供給欄だけを比較。実ScannerやBusiness Logicの動作試験は行っていない。 |
| regressionScope | 同じ供給Scenarioの二条件だけ。全System非回帰ではない。 |
| residualRiskId | RES-FRT15-006 |
| reassessmentId | REA-FRT15-006 |

## handoffs HOF-FRT15-16

| Field | Value |
|---|---|
| id | HOF-FRT15-16 |
| targetChapter | 16 |
| findingIds/0 | FND-FRT15-001 |
| findingIds/1 | FND-FRT15-002 |
| findingIds/2 | FND-FRT15-003 |
| findingIds/3 | FND-FRT15-004 |
| findingIds/4 | FND-FRT15-005 |
| findingIds/5 | FND-FRT15-006 |
| findingIds/6 | FND-FRT15-007 |
| recordId | FRT-2026-015 |
| purpose | 対象・版・時刻・判断の必須Fieldと未観測Gap。 |
| status | planned-not-delivered |
| executionAuthorized | false |

## handoffs HOF-FRT15-17

| Field | Value |
|---|---|
| id | HOF-FRT15-17 |
| targetChapter | 17 |
| findingIds/0 | FND-FRT15-001 |
| findingIds/1 | FND-FRT15-002 |
| findingIds/2 | FND-FRT15-003 |
| findingIds/3 | FND-FRT15-004 |
| findingIds/4 | FND-FRT15-005 |
| findingIds/5 | FND-FRT15-006 |
| findingIds/6 | FND-FRT15-007 |
| recordId | FRT-2026-015 |
| purpose | 検知の仮説と必要Evidence。検知成功の証明ではない。 |
| status | planned-not-delivered |
| executionAuthorized | false |

## handoffs HOF-FRT15-21

| Field | Value |
|---|---|
| id | HOF-FRT15-21 |
| targetChapter | 21 |
| findingIds/0 | FND-FRT15-001 |
| findingIds/1 | FND-FRT15-002 |
| findingIds/2 | FND-FRT15-003 |
| findingIds/3 | FND-FRT15-004 |
| findingIds/4 | FND-FRT15-005 |
| findingIds/5 | FND-FRT15-006 |
| findingIds/6 | FND-FRT15-007 |
| recordId | FRT-2026-015 |
| purpose | 統制の受入条件と反証条件。 |
| status | planned-not-delivered |
| executionAuthorized | false |

## handoffs HOF-FRT15-22

| Field | Value |
|---|---|
| id | HOF-FRT15-22 |
| targetChapter | 22 |
| findingIds/0 | FND-FRT15-001 |
| findingIds/1 | FND-FRT15-002 |
| findingIds/2 | FND-FRT15-003 |
| findingIds/3 | FND-FRT15-004 |
| findingIds/4 | FND-FRT15-005 |
| findingIds/5 | FND-FRT15-006 |
| findingIds/6 | FND-FRT15-007 |
| recordId | FRT-2026-015 |
| purpose | 改修BacklogのOwner・期限・依存。 |
| status | planned-not-delivered |
| executionAuthorized | false |

## handoffs HOF-FRT15-26

| Field | Value |
|---|---|
| id | HOF-FRT15-26 |
| targetChapter | 26 |
| findingIds/0 | FND-FRT15-001 |
| findingIds/1 | FND-FRT15-002 |
| findingIds/2 | FND-FRT15-003 |
| findingIds/3 | FND-FRT15-004 |
| findingIds/4 | FND-FRT15-005 |
| findingIds/5 | FND-FRT15-006 |
| findingIds/6 | FND-FRT15-007 |
| recordId | FRT-2026-015 |
| purpose | 残存Riskと判断Owner、次の再評価条件。 |
| status | planned-not-delivered |
| executionAuthorized | false |
