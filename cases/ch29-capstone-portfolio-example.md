# 第29章 完全合成Case：不足を保持した最終Portfolio

## 読み方と範囲

[第29章](../manuscript/29-capstone-case-study.md) / [空ART-33](../templates/final-security-decision-portfolio-index.md) / [ART-10](../templates/integrated-security-case-map.md)。

全人物Role、時刻、判断は架空。PORT-CAP29-001 / CASE-2026-001 / CAP29-REV-001は、親の履歴を変更しない後日の読解記録である。StatusはDecision ready、推奨はOPT-CAP29-HOLD、承認・受領はnull、実収集・実操作・実Model・実配送は0。四GapとResidual riskは未解消である。

[非実行JSON](fixtures/ch29-capstone-portfolio.json)と[閉Schema](../schemas/ch29-capstone-portfolio.schema.json)を併用する。下の全欄表はJSONの全leafと対応する。nativeStateは元欄の代表値であって全Bundleの状態ではない。integrationOwnerは今回の読解担当であり、親Ownerを変更しない。親Owner、Evidence、Decision、Control、Reassessmentの詳細は次の元記録リンクに保持する。

## 32成果物への戻り先

| Artifact | Record / 関係 | Template / 元記録 |
|---|---|---|
| ART-01 | LRP-2026-003 / independent / independent-comparison | [空Template](../templates/learning-route-plan.md) / [元記録](../cases/ch03-capability-evidence-example.md) |
| ART-02 | ROE-2026-009 / refines / historical-context | [空Template](../templates/rules-of-engagement.md) / [元記録](../cases/ch09-engagement-roe-example.md) |
| ART-03 | TM-2026-001 / refines / method-reference | [空Template](../templates/threat-model.md) / [元記録](../cases/ch04-threat-model-example.md) |
| ART-04 | FRT-2026-015 / refines / method-reference | [空Template](../templates/finding-report.md) / [元記録](../cases/ch15-findings-retest-risk-example.md) |
| ART-05 | DVR-2026-017-001 / refines / method-reference | [空Template](../templates/detection-validation.md) / [元記録](../cases/ch17-detection-validation-example.md) |
| ART-06 | HUNT-2026-018-001 / refines / method-reference | [空Template](../templates/hunt-report.md) / [元記録](../cases/ch18-hunt-plan-example.md) |
| ART-07 | DFIR-2026-020-001 / refines / method-reference | [空Template](../templates/incident-timeline.md) / [元記録](../cases/ch20-dfir-timeline-causality-example.md) |
| ART-08 | PRD-CTI26-TECH / independent / independent-comparison | [空Template](../templates/cti-report.md) / [元記録](../cases/ch26-cti-distribution-example.md) |
| ART-09 | PRD-CTI26-EXEC / independent / independent-comparison | [空Template](../templates/executive-brief.md) / [元記録](../cases/ch26-cti-distribution-example.md) |
| ART-10 | CASE-2026-001 / refines / historical-context | [空Template](../templates/integrated-security-case-map.md) / [元記録](../cases/ch01-integrated-security-case-example.md) |
| ART-11 | CASE-2026-011 / independent / independent-comparison | [空Template](../templates/web-api-assessment-hypothesis-pack.md) / [元記録](../cases/ch11-web-api-assessment-example.md) |
| ART-12 | AJ-2026-025 / independent / independent-comparison | [空Template](../templates/analytic-judgment-record.md) / [元記録](../cases/ch25-structured-analysis-attribution-example.md) |
| ART-13 | AUTH-CASE-2026-001 / refines / historical-context | [空Template](../templates/authorization-checklist.md) / [元記録](../cases/ch02-authorization-decision-example.md) |
| ART-14 | CAP-MATRIX-2026-003 / independent / independent-comparison | [空Template](../templates/capability-evidence-matrix.md) / [元記録](../cases/ch03-capability-evidence-example.md) |
| ART-15 | BMAP-2026-001 / refines / method-reference | [空Template](../templates/attack-behavior-map.md) / [元記録](../cases/ch05-attack-behavior-example.md) |
| ART-16 | SFM-2026-001 / refines / method-reference | [空Template](../templates/signal-flow-diagram.md) / [元記録](../cases/ch06-signal-flow-example.md) |
| ART-17 | VPR-2026-001 / refines / method-reference | [空Template](../templates/vulnerability-prioritization-record.md) / [元記録](../cases/ch07-vulnerability-prioritization-example.md) |
| ART-18 | LABPLAN-2026-001 / refines / method-reference | [空Template](../templates/lab-safety-evidence-plan.md) / [元記録](../cases/ch08-lab-evidence-example.md) |
| ART-19 | ASR-2026-010 / refines / method-reference | [空Template](../templates/attack-surface-register.md) / [元記録](../cases/ch10-attack-surface-example.md) |
| ART-20 | IAR-2026-012 / refines / method-reference | [空Template](../templates/identity-attack-path-review.md) / [元記録](../cases/ch12-identity-path-review-example.md) |
| ART-21 | PSA-2026-013 / refines / method-reference | [空Template](../templates/platform-supply-chain-assessment.md) / [元記録](../cases/ch13-platform-supply-chain-example.md) |
| ART-22 | MIV-2026-014 / refines / method-reference | [空Template](../templates/minimal-impact-validation-record.md) / [元記録](../cases/ch14-minimal-impact-validation-example.md) |
| ART-23 | FRT-2026-015 / refines / method-reference | [空Template](../templates/retest-record.md) / [元記録](../cases/ch15-findings-retest-risk-example.md) |
| ART-24 | TCM-2026-016 / refines / method-reference | [空Template](../templates/telemetry-coverage-map.md) / [元記録](../cases/ch16-telemetry-coverage-example.md) |
| ART-25 | IAP-2026-019-001 / refines / method-reference | [空Template](../templates/incident-action-plan.md) / [元記録](../cases/ch19-incident-action-plan-example.md) |
| ART-26 | DFIR-2026-020-001 / refines / method-reference | [空Template](../templates/root-cause-analysis.md) / [元記録](../cases/ch20-dfir-timeline-causality-example.md) |
| ART-27 | CVP-2026-021-001 / refines / method-reference | [空Template](../templates/control-validation-plan.md) / [元記録](../cases/ch21-control-validation-example.md) |
| ART-28 | SIB-2026-022-001 / refines / method-reference | [空Template](../templates/security-improvement-backlog.md) / [元記録](../cases/ch22-improvement-backlog-example.md) |
| ART-29 | IRCP-2026-023-001 / refines / method-reference | [空Template](../templates/intelligence-requirement-collection-plan.md) / [元記録](../cases/ch23-intelligence-requirements-example.md) |
| ART-30 | EST-2026-024-001 / independent / independent-comparison | [空Template](../templates/evidence-source-evaluation-table.md) / [元記録](../cases/ch24-source-evaluation-example.md) |
| ART-31 | AIM-2026-027 / refines / method-reference | [空Template](../templates/ai-agent-threat-model.md) / [元記録](../cases/ch27-ai-agent-threat-model-example.md) |
| ART-32 | AAR-2026-028-001 / independent / independent-comparison | [空Template](../templates/ai-assisted-analysis-assurance-record.md) / [元記録](../cases/ch28-ai-assisted-analysis-assurance-example.md) |

## 記入結果の自己点検

何を判断するかはrequirement、最初に書く欄はrecord、証拠不足はgaps、停止は実Data・未知入力・版不一致・不明Authority・外部接続要求、次の確認はactions/reassessmentで辿る。DOCは文書読解でありシステム観測ではない。レビュー欄のPass-with-limitsは架空の教材内Reviewで、実際の独立レビュー・法務承認・人間の読者試行ではない。

二Briefは同じAJ・四DOC・四Gapを参照する。Not collectedとInconclusiveを区別し、別Caseの未配達を受領済みにしない。作業メモを整理しても親Evidenceや履歴を削除しない。

## 全欄の読み方

### schemaVersion

| Field | Value |
|---|---|
| value | 1.0.0 |

### synthetic

| Field | Value |
|---|---|
| value | true |

### readOnly

| Field | Value |
|---|---|
| value | true |

### networkRequired

| Field | Value |
|---|---|
| value | false |

### executionAuthorized

| Field | Value |
|---|---|
| value | false |

### actualCollections

| Field | Value |
|---|---|
| value | 0 |

### actualActions

| Field | Value |
|---|---|
| value | 0 |

### actualModelCalls

| Field | Value |
|---|---|
| value | 0 |

### actualDeliveries

| Field | Value |
|---|---|
| value | 0 |

### record

| Field | Value |
|---|---|
| id | PORT-CAP29-001 |
| artifactId | ART-33 |
| finalCaseId | CASE-2026-001 |
| version | CAP29-REV-001 |
| asOf | 2026-10-21T00:00:00Z |
| sourceCutoff | 2026-10-21T00:00:00Z |
| classification | Public synthetic teaching record |
| status | Decision ready |
| owner | SYNTH-PORTFOLIO-OWNER |
| deadline | 2026-10-22T00:00:00Z |
| expiry | 2026-10-28T00:00:00Z |
| meaning | later-authored-reading-not-a-historical-case-update |

### requirement

| Field | Value |
|---|---|
| id | DR-CAP29-001 |
| parentId | DR-2026-001 |
| question | 請求書連携の再評価で、供給資料だけを根拠に実作業再開・全Control完了を提案してよいか。 |
| decisionOwner | SYNTH-CTO |
| deadline | 2026-10-22T00:00:00Z |
| criteria | 今回のAuthority、同対象版のEvidence、未解決Gapを隠さない説明を要する。 |
| maximumUncertainty | 不足を理由に保留する判断は可能。不足を埋めたと仮定して再開・完了を選ばない。 |

### artifacts-1

| Field | Value |
|---|---|
| artifactId | ART-01 |
| recordId | LRP-2026-003 |
| sourceCaseId | LEARN-CASE-2026-003 |
| relationToFinal | independent |
| use | independent-comparison |
| canonicalPath | cases/ch03-capability-evidence-example.md |
| versionSha256 | 90dd67c303c18eefa0a0d3048f97173f215cdc4ac89f1575a116ec18098fc17f |
| templatePath | templates/learning-route-plan.md |
| ownerChapter | 0 |
| nativeState/scope | plan-review-date-not-status |
| nativeState/line | 35 |
| nativeState/verbatim | &#124; 月次レビュー日 &#124; 2026-09-05、2026-10-05、2026-11-05 &#124; |
| integrationOwner | SYNTH-PORTFOLIO-OWNER |
| stageId | S29-01 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | 親Plan→Task/学習Evidence→Review→月次再評価。ART-14の親Planであって業務Caseの侵害・能力認定の根拠ではない。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-2

| Field | Value |
|---|---|
| artifactId | ART-02 |
| recordId | ROE-2026-009 |
| sourceCaseId | CASE-2026-001 |
| relationToFinal | refines |
| use | historical-context |
| canonicalPath | cases/ch09-engagement-roe-example.md |
| versionSha256 | 44cf657c9ad220709c6b026ec4a894d904b1f89d88427e3babd2070e5a11b25a |
| templatePath | templates/rules-of-engagement.md |
| ownerChapter | 9 |
| nativeState/scope | record |
| nativeState/line | 33 |
| nativeState/verbatim | &#124; status &#124; Draft &#124; |
| integrationOwner | SYNTH-AUTHORITY-REVIEWER |
| stageId | S29-02 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | Draft / Do not proceed。decision・approval・evidence・changeを読む。失効AUTHと旧ROE-2026-001を置換せず、承認欄のnullを埋めない。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-3

| Field | Value |
|---|---|
| artifactId | ART-03 |
| recordId | TM-2026-001 |
| sourceCaseId | CASE-2026-001 |
| relationToFinal | refines |
| use | method-reference |
| canonicalPath | cases/ch04-threat-model-example.md |
| versionSha256 | 297e28b6f3437f80fbdacdd02d21fff4f0d00465faad03df5278724ad8f638ac |
| templatePath | templates/threat-model.md |
| ownerChapter | 4 |
| nativeState/scope | record |
| nativeState/line | 27 |
| nativeState/verbatim | &#124; Model status &#124; Needs Evidence &#124; |
| integrationOwner | SYNTH-ASSET-REVIEWER |
| stageId | S29-03 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | Needs Evidence。Threat→Control→Gap→Evidence requirement→Action/Reassessment。必要EvidenceとCollected Evidence、Case関係とControlのsupportsを分離する。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-4

| Field | Value |
|---|---|
| artifactId | ART-04 |
| recordId | FRT-2026-015 |
| sourceCaseId | CASE-2026-001 |
| relationToFinal | refines |
| use | method-reference |
| canonicalPath | cases/ch15-findings-retest-risk-example.md |
| versionSha256 | 1195d3e395e09d25350e903e83f1fe0c782a6ab843dca4ee12252b0485bd83ea |
| templatePath | templates/finding-report.md |
| ownerChapter | 15 |
| nativeState/scope | first-finding |
| nativeState/line | 168 |
| nativeState/verbatim | &#124; status &#124; Open &#124; |
| integrationOwner | SYNTH-RETEST-REVIEWER |
| stageId | S29-05 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | findings→同対象/版のvalidation・evidenceIds→treatments/decision→reassessment。七Findingは独立対比。Closedを修正成功へ一括変換しない。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-5

| Field | Value |
|---|---|
| artifactId | ART-05 |
| recordId | DVR-2026-017-001 |
| sourceCaseId | CASE-DET-2026-001 |
| relationToFinal | refines |
| use | method-reference |
| canonicalPath | cases/ch17-detection-validation-example.md |
| versionSha256 | 579402095d7bb0d35ff6da452220dc748ac0160de577dbbb5756d3633f2afb07 |
| templatePath | templates/detection-validation.md |
| ownerChapter | 17 |
| nativeState/scope | record |
| nativeState/line | 31 |
| nativeState/verbatim | &#124; Status &#124; Validated &#124; |
| integrationOwner | SYNTH-DETECTION-REVIEWER |
| stageId | S29-06 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | Threat/Observation hypothesis→Telemetry contract→三fixture→DVR→triage/handoff/control/reassessment。Mappedやfixture検証を実配備/親Control全合格としない。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-6

| Field | Value |
|---|---|
| artifactId | ART-06 |
| recordId | HUNT-2026-018-001 |
| sourceCaseId | CASE-HUNT-2026-001 |
| relationToFinal | refines |
| use | method-reference |
| canonicalPath | cases/ch18-hunt-plan-example.md |
| versionSha256 | febafef7cc7e68e67afe980f069afa1d445e27f5b0c3e256704fa41c58b7f822 |
| templatePath | templates/hunt-report.md |
| ownerChapter | 18 |
| nativeState/scope | first-contrast |
| nativeState/line | 168 |
| nativeState/verbatim | &#124; &#96;judgment/result&#96; &#124; &#96;Supported&#96; &#124; |
| integrationOwner | SYNTH-INCIDENT-REVIEWER |
| stageId | S29-07 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | 計画と有限対比のEvidence・Coverage・Owner・次判断を読む。SupportedはIncident宣言ではない。負の結果は利用可能な観測範囲に限定する。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-7

| Field | Value |
|---|---|
| artifactId | ART-07 |
| recordId | DFIR-2026-020-001 |
| sourceCaseId | CASE-DFIR-2026-001 |
| relationToFinal | refines |
| use | method-reference |
| canonicalPath | cases/ch20-dfir-timeline-causality-example.md |
| versionSha256 | 5afed2d643b032afa479743eb2f06eb48f19ed080117fb9227f261fa495a7847 |
| templatePath | templates/incident-timeline.md |
| ownerChapter | 20 |
| nativeState/scope | snapshot-A-cause |
| nativeState/line | 484 |
| nativeState/verbatim | &#124; &#96;rca/rootCauseStatus&#96; &#124; &#96;unresolved&#96; &#124; |
| integrationOwner | SYNTH-DFIR-REVIEWER |
| stageId | S29-08 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | TL-DFIR20-A/Bのcutoff・availableAt・Receipt→Event→Claimを読む。親予定TL-IR19-004と別ID。遅着/再送/不確かさを隠さない。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-8

| Field | Value |
|---|---|
| artifactId | ART-08 |
| recordId | PRD-CTI26-TECH |
| sourceCaseId | CASE-2026-025 |
| relationToFinal | independent |
| use | independent-comparison |
| canonicalPath | cases/ch26-cti-distribution-example.md |
| versionSha256 | 35d8a3b7342ba589e095fbd7b91e057c1e5194d332c55823fc35b731e612312e |
| templatePath | templates/cti-report.md |
| ownerChapter | 26 |
| nativeState/scope | technical-product |
| nativeState/line | 325 |
| nativeState/verbatim | &#124; &#96;status&#96; &#124; &#96;prepared-not-delivered&#96; &#124; |
| integrationOwner | SYNTH-ANALYSIS-REVIEWER |
| stageId | S29-11 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | products&#91;0&#93;→三KJ→親25のEvidence/原典群→recommendations/decision/reassessment。prepared-not-delivered、L2上限、成功未確認を保持する。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-9

| Field | Value |
|---|---|
| artifactId | ART-09 |
| recordId | PRD-CTI26-EXEC |
| sourceCaseId | CASE-2026-025 |
| relationToFinal | independent |
| use | independent-comparison |
| canonicalPath | cases/ch26-cti-distribution-example.md |
| versionSha256 | 35d8a3b7342ba589e095fbd7b91e057c1e5194d332c55823fc35b731e612312e |
| templatePath | templates/executive-brief.md |
| ownerChapter | 26 |
| nativeState/scope | executive-product |
| nativeState/line | 360 |
| nativeState/verbatim | &#124; &#96;status&#96; &#124; &#96;prepared-not-delivered&#96; &#124; |
| integrationOwner | SYNTH-ANALYSIS-REVIEWER |
| stageId | S29-11 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | products&#91;1&#93;も同じKJを使う。Audience/選択肢/残余リスクの表現を変えてもEvidence・確信度・実権限を増やさない。未配達を保持する。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-10

| Field | Value |
|---|---|
| artifactId | ART-10 |
| recordId | CASE-2026-001 |
| sourceCaseId | CASE-2026-001 |
| relationToFinal | refines |
| use | historical-context |
| canonicalPath | cases/ch01-integrated-security-case-example.md |
| versionSha256 | c72c0d149321a24f2b6901db381c069cff86a8536b5578eba285b9d17eb329b2 |
| templatePath | templates/integrated-security-case-map.md |
| ownerChapter | 1 |
| nativeState/scope | record |
| nativeState/line | 22 |
| nativeState/verbatim | &#124; Status &#124; Reassessment Due &#124; |
| integrationOwner | SYNTH-PORTFOLIO-OWNER |
| stageId | S29-01 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | DR→ROE→Hypothesis→Evidence→Finding/Control→DEC-2026-001→REA-2026-001。Reassessment DueのDocument状態と個別Finding/Control結果を分離する。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-11

| Field | Value |
|---|---|
| artifactId | ART-11 |
| recordId | CASE-2026-011 |
| sourceCaseId | CASE-2026-011 |
| relationToFinal | independent |
| use | independent-comparison |
| canonicalPath | cases/ch11-web-api-assessment-example.md |
| versionSha256 | 170f4d66d10aa2b2090018b610002b23a226db43b86b473af2216525ddca182f |
| templatePath | templates/web-api-assessment-hypothesis-pack.md |
| ownerChapter | 11 |
| nativeState/scope | record |
| nativeState/line | 33 |
| nativeState/verbatim | &#124; Status &#124; Detection Handoff &#124; |
| integrationOwner | SYNTH-ASSESSMENT-REVIEWER |
| stageId | S29-04 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | Hypothesis Pack→VAL/OBS/EVD→Finding・Detection handoff→再評価。別対象のExport/Webhook教材であり、CASE-2026-001へEvidence/許可を借用しない。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-12

| Field | Value |
|---|---|
| artifactId | ART-12 |
| recordId | AJ-2026-025 |
| sourceCaseId | CASE-2026-025 |
| relationToFinal | independent |
| use | independent-comparison |
| canonicalPath | cases/ch25-structured-analysis-attribution-example.md |
| versionSha256 | cd78f9a491106b458b41291986c92085b8ab04886070e8ba9e8dc59336a20b49 |
| templatePath | templates/analytic-judgment-record.md |
| ownerChapter | 25 |
| nativeState/scope | record |
| nativeState/line | 22 |
| nativeState/verbatim | &#124; Status &#124; Decision Support &#124; |
| integrationOwner | SYNTH-ANALYSIS-REVIEWER |
| stageId | S29-11 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | DR/IR→Source Note/lineage/Evidence→代替説明/判断→DEC/REA。同原典の再掲を独立観測に数えず、限定非観測を成功不存在にしない。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-13

| Field | Value |
|---|---|
| artifactId | ART-13 |
| recordId | AUTH-CASE-2026-001 |
| sourceCaseId | CASE-2026-001 |
| relationToFinal | refines |
| use | historical-context |
| canonicalPath | cases/ch02-authorization-decision-example.md |
| versionSha256 | 74d1aa7a802525ee5f465ccbdc1404e26a974ed60e264b65978612bef8026f4a |
| templatePath | templates/authorization-checklist.md |
| ownerChapter | 2 |
| nativeState/scope | record |
| nativeState/line | 24 |
| nativeState/verbatim | &#124; Status &#124; Decision Recorded &#124; |
| integrationOwner | SYNTH-AUTHORITY-REVIEWER |
| stageId | S29-02 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | Decision RecordedとGate Conditionalを分離。Authority/Scope/Safety/Disclosure→Decision→条件/担当/期限。後日のSource確認は過去権限を延長しない。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-14

| Field | Value |
|---|---|
| artifactId | ART-14 |
| recordId | CAP-MATRIX-2026-003 |
| sourceCaseId | LEARN-CASE-2026-003 |
| relationToFinal | independent |
| use | independent-comparison |
| canonicalPath | cases/ch03-capability-evidence-example.md |
| versionSha256 | 90dd67c303c18eefa0a0d3048f97173f215cdc4ac89f1575a116ec18098fc17f |
| templatePath | templates/capability-evidence-matrix.md |
| ownerChapter | 3 |
| nativeState/scope | matrix-not-person |
| nativeState/line | 53 |
| nativeState/verbatim | &#124; Status &#124; Gap identified &#124; |
| integrationOwner | SYNTH-PORTFOLIO-OWNER |
| stageId | S29-01 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | LRP-2026-003→Task/Practice→Artifact Evidence/Review→Capability Judgment→Gap/再評価。Gap identifiedとPartially supportedは別軸。人事評価へ転用しない。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-15

| Field | Value |
|---|---|
| artifactId | ART-15 |
| recordId | BMAP-2026-001 |
| sourceCaseId | CASE-2026-001 |
| relationToFinal | refines |
| use | method-reference |
| canonicalPath | cases/ch05-attack-behavior-example.md |
| versionSha256 | 9bc5004441f6a7911106da6cba263297bf115814d7c644c80f776c7f0e7098ac |
| templatePath | templates/attack-behavior-map.md |
| ownerChapter | 5 |
| nativeState/scope | first-row |
| nativeState/line | 66 |
| nativeState/verbatim | &#124; status &#124; Mapped &#124; |
| integrationOwner | SYNTH-ASSET-REVIEWER |
| stageId | S29-03 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | rowsのThreat/Asset/Boundary→ATT&amp;CK版/関係→Evidence/test→Gap/Owner/reviewDate。Not collected、対応付けと検証、教育用製品モデルと親実態を分離する。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-16

| Field | Value |
|---|---|
| artifactId | ART-16 |
| recordId | SFM-2026-001 |
| sourceCaseId | CASE-2026-001 |
| relationToFinal | refines |
| use | method-reference |
| canonicalPath | cases/ch06-signal-flow-example.md |
| versionSha256 | a062ba22f4f0e1eb28a08342b0173a02473e995062410986b51d1a6a4af7cf0a |
| templatePath | templates/signal-flow-diagram.md |
| ownerChapter | 6 |
| nativeState/scope | first-flow |
| nativeState/line | 60 |
| nativeState/verbatim | &#124; coverage &#124; Produced &#124; |
| integrationOwner | SYNTH-ASSET-REVIEWER |
| stageId | S29-03 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | flowsの親ID→receipt/test→coverage/gap→allowedConclusion/owner/reassessment。六Coverageを第16章のRequired込み七状態へ暗黙変換しない。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-17

| Field | Value |
|---|---|
| artifactId | ART-17 |
| recordId | VPR-2026-001 |
| sourceCaseId | CASE-2026-001 |
| relationToFinal | refines |
| use | method-reference |
| canonicalPath | cases/ch07-vulnerability-prioritization-example.md |
| versionSha256 | 868840e8ee6fdb66b2645f0a954d11107d286b1c63c81a7cdb4be072d5061c3f |
| templatePath | templates/vulnerability-prioritization-record.md |
| ownerChapter | 7 |
| nativeState/scope | first-candidate |
| nativeState/line | 58 |
| nativeState/verbatim | &#124; exposure &#124; Not applicable &#124; |
| integrationOwner | SYNTH-ASSESSMENT-REVIEWER |
| stageId | S29-04 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | recordsの版・到達条件→固定Source snapshotと合成Evidence→priority/treatment→owner/期限/再評価。公開EPSS/KEV値と合成Deployment、Catalog期日と組織期限は別。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-18

| Field | Value |
|---|---|
| artifactId | ART-18 |
| recordId | LABPLAN-2026-001 |
| sourceCaseId | CASE-2026-001 |
| relationToFinal | refines |
| use | method-reference |
| canonicalPath | cases/ch08-lab-evidence-example.md |
| versionSha256 | 715859aea7c9ee8e939ff080447d34916a4f4b582d737719f272b394b9f17e0d |
| templatePath | templates/lab-safety-evidence-plan.md |
| ownerChapter | 8 |
| nativeState/scope | first-run |
| nativeState/line | 116 |
| nativeState/verbatim | &#124; finalStatus &#124; Cleanup verified &#124; |
| integrationOwner | SYNTH-AUTHORITY-REVIEWER |
| stageId | S29-02 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | runs→receiptIds/signalIds→八状態/三結果→export/cleanup/再評価。Runningを含む状態、正常完了、実行許可は別。Cleanup成功で過去Failを消さない。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-19

| Field | Value |
|---|---|
| artifactId | ART-19 |
| recordId | ASR-2026-010 |
| sourceCaseId | CASE-2026-001 |
| relationToFinal | refines |
| use | method-reference |
| canonicalPath | cases/ch10-attack-surface-example.md |
| versionSha256 | 7409da76004a7c32489d620691684054cb60e486dfb7dd8a7f7dabb012ed46fa |
| templatePath | templates/attack-surface-register.md |
| ownerChapter | 10 |
| nativeState/scope | record |
| nativeState/line | 68 |
| nativeState/verbatim | &#124; status &#124; &#96;analysis-complete-with-gaps&#96; &#124; |
| integrationOwner | SYNTH-ASSET-REVIEWER |
| stageId | S29-03 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | candidate→source/provenance/origin→所有/検証状態→gapOwner/期限/再評価。候補発見はRoE Scope追加でなく、所有確信度は操作許可ではない。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-20

| Field | Value |
|---|---|
| artifactId | ART-20 |
| recordId | IAR-2026-012 |
| sourceCaseId | CASE-2026-001 |
| relationToFinal | refines |
| use | method-reference |
| canonicalPath | cases/ch12-identity-path-review-example.md |
| versionSha256 | 0caa79dcb448212f08f5d6d44c5af705bf850be7b60bd610fab93a5e6ffc1bd3 |
| templatePath | templates/identity-attack-path-review.md |
| ownerChapter | 12 |
| nativeState/scope | first-finding |
| nativeState/line | 834 |
| nativeState/verbatim | &#124; status &#124; teaching-analysis-not-production-finding &#124; |
| integrationOwner | SYNTH-ASSESSMENT-REVIEWER |
| stageId | S29-04 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | pathのprincipal/resource/action/graph・policy版→config/event/evaluation→finding/owner/reassessment。静的経路はValidatedでなく、Brokenには反証が必要。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-21

| Field | Value |
|---|---|
| artifactId | ART-21 |
| recordId | PSA-2026-013 |
| sourceCaseId | CASE-2026-001 |
| relationToFinal | refines |
| use | method-reference |
| canonicalPath | cases/ch13-platform-supply-chain-example.md |
| versionSha256 | 2b7f65bbeb4d66f9f8f9eed58ecb54cd69ed458891a666f6a27158bc92dff876 |
| templatePath | templates/platform-supply-chain-assessment.md |
| ownerChapter | 13 |
| nativeState/scope | first-finding |
| nativeState/line | 468 |
| nativeState/verbatim | &#124; finding/status &#124; Verified &#124; |
| integrationOwner | SYNTH-ASSESSMENT-REVIEWER |
| stageId | S29-04 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | 同recordRevisionのexpectations→chains/evidence→finding/decision。Verifiedは供給summary比較に限定。Signed/Trusted/準拠/Safe/Build許可へ昇格しない。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-22

| Field | Value |
|---|---|
| artifactId | ART-22 |
| recordId | MIV-2026-014 |
| sourceCaseId | CASE-2026-001 |
| relationToFinal | refines |
| use | method-reference |
| canonicalPath | cases/ch14-minimal-impact-validation-example.md |
| versionSha256 | 920e50b2b94152bf8c93bd640de1bec9dc61e2fcf3deb8bfacc682ada9764aa2 |
| templatePath | templates/minimal-impact-validation-record.md |
| ownerChapter | 14 |
| nativeState/scope | first-validation |
| nativeState/line | 343 |
| nativeState/verbatim | &#124; judgment/result &#124; Supported &#124; |
| integrationOwner | SYNTH-ASSESSMENT-REVIEWER |
| stageId | S29-04 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | 同対象/版の二条件→observations/evidenceIds→stop/cleanup/residual→judgment/finding/decision。Not performedは別欄。Inconclusiveでも記録Completeはあり得る。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-23

| Field | Value |
|---|---|
| artifactId | ART-23 |
| recordId | FRT-2026-015 |
| sourceCaseId | CASE-2026-001 |
| relationToFinal | refines |
| use | method-reference |
| canonicalPath | cases/ch15-findings-retest-risk-example.md |
| versionSha256 | 1195d3e395e09d25350e903e83f1fe0c782a6ab843dca4ee12252b0485bd83ea |
| templatePath | templates/retest-record.md |
| ownerChapter | 15 |
| nativeState/scope | first-retest |
| nativeState/line | 1003 |
| nativeState/verbatim | &#124; result &#124; Failed &#124; |
| integrationOwner | SYNTH-RETEST-REVIEWER |
| stageId | S29-05 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | retestsをfindingId・対象・before/after版で結ぶ。Passed、受容経由Closed、期限付き受容、残余リスクを分離。親14のEvidenceを新Appへ移さない。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-24

| Field | Value |
|---|---|
| artifactId | ART-24 |
| recordId | TCM-2026-016 |
| sourceCaseId | CASE-DET-2026-001 |
| relationToFinal | refines |
| use | method-reference |
| canonicalPath | cases/ch16-telemetry-coverage-example.md |
| versionSha256 | c6feb2d518321779dbdc32d9245b26553ee619813dfbc9f50e8a28d2610914fe |
| templatePath | templates/telemetry-coverage-map.md |
| ownerChapter | 16 |
| nativeState/scope | first-coverage-row |
| nativeState/line | 1149 |
| nativeState/verbatim | &#124; &#96;coverage&#96; &#124; &#96;Validated&#96; &#124; |
| integrationOwner | SYNTH-DETECTION-REVIEWER |
| stageId | S29-06 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | requirements→fixtures/receipts→rows/七Coverage→Gap/Owner/期限→handoffs。Mapの存在だけで第17章入力契約を満たしたことにしない。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-25

| Field | Value |
|---|---|
| artifactId | ART-25 |
| recordId | IAP-2026-019-001 |
| sourceCaseId | CASE-IR-2026-001 |
| relationToFinal | refines |
| use | method-reference |
| canonicalPath | cases/ch19-incident-action-plan-example.md |
| versionSha256 | f72b0311c2acc075063b05003d55ecb323d767b27f449e6ab019d1a5de2118b0 |
| templatePath | templates/incident-action-plan.md |
| ownerChapter | 19 |
| nativeState/scope | first-contrast |
| nativeState/line | 147 |
| nativeState/verbatim | &#124; &#96;expected/status&#96; &#124; &#96;Suspected&#96; &#124; |
| integrationOwner | SYNTH-INCIDENT-REVIEWER |
| stageId | S29-07 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | 十二対比の利用可能Evidence・Scope・判断権者→宣言/対応/復旧/再評価。Hunt SupportedからDeclaredへ自動昇格せず、Closedを全改善完了にしない。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-26

| Field | Value |
|---|---|
| artifactId | ART-26 |
| recordId | DFIR-2026-020-001 |
| sourceCaseId | CASE-DFIR-2026-001 |
| relationToFinal | refines |
| use | method-reference |
| canonicalPath | cases/ch20-dfir-timeline-causality-example.md |
| versionSha256 | 5afed2d643b032afa479743eb2f06eb48f19ed080117fb9227f261fa495a7847 |
| templatePath | templates/root-cause-analysis.md |
| ownerChapter | 20 |
| nativeState/scope | snapshot-A-cause |
| nativeState/line | 484 |
| nativeState/verbatim | &#124; &#96;rca/rootCauseStatus&#96; &#124; &#96;unresolved&#96; &#124; |
| integrationOwner | SYNTH-DFIR-REVIEWER |
| stageId | S29-08 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | Timelineと同じrecord内の六Claim・仮説・Gap→担当/再評価。相関・一つの保守説明への反証を原因確定にしない。両Snapshotの原因unresolvedを保持。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-27

| Field | Value |
|---|---|
| artifactId | ART-27 |
| recordId | CVP-2026-021-001 |
| sourceCaseId | CASE-CV-2026-001 |
| relationToFinal | refines |
| use | method-reference |
| canonicalPath | cases/ch21-control-validation-example.md |
| versionSha256 | 38d80638db23e8218a19dd718a19fb8196b1d06138e653af5da573352bb6ae5d |
| templatePath | templates/control-validation-plan.md |
| ownerChapter | 21 |
| nativeState/scope | first-scenario |
| nativeState/line | 272 |
| nativeState/verbatim | &#124; &#96;expectedLayers/0/result&#96; &#124; &#96;Passed&#96; &#124; |
| integrationOwner | SYNTH-CONTROL-REVIEWER |
| stageId | S29-09 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | 新対象/版の五層・十Scenario→Evidence/判定→Retest/Action/未配達。IndeterminateをPartialやPassedへ丸めず、非選択層は未評価のまま。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-28

| Field | Value |
|---|---|
| artifactId | ART-28 |
| recordId | SIB-2026-022-001 |
| sourceCaseId | CASE-IMP-2026-001 |
| relationToFinal | refines |
| use | method-reference |
| canonicalPath | cases/ch22-improvement-backlog-example.md |
| versionSha256 | 44072e9adc67982f5811058d2f9d99000b3cb831cd49abc89267392a9d495dd7 |
| templatePath | templates/security-improvement-backlog.md |
| ownerChapter | 22 |
| nativeState/scope | first-item |
| nativeState/line | 835 |
| nativeState/verbatim | &#124; &#96;status&#96; &#124; &#96;Proposed&#96; &#124; |
| integrationOwner | SYNTH-CONTROL-REVIEWER |
| stageId | S29-09 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | metricsの母集団/版/品質→items/evidence/verification→decision/acceptance/reassessment。Accepted/Retiredは修正成功ではなく、二版・八項目は実時系列ではない。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-29

| Field | Value |
|---|---|
| artifactId | ART-29 |
| recordId | IRCP-2026-023-001 |
| sourceCaseId | CASE-IRP-2026-001 |
| relationToFinal | refines |
| use | method-reference |
| canonicalPath | cases/ch23-intelligence-requirements-example.md |
| versionSha256 | a9dd034c0a9a70097a06d066be79023122a4c180aee1117d7c3c388cb680b759 |
| templatePath | templates/intelligence-requirement-collection-plan.md |
| ownerChapter | 23 |
| nativeState/scope | first-requirement |
| nativeState/line | 147 |
| nativeState/verbatim | &#124; &#96;status&#96; &#124; &#96;Satisfied&#96; &#124; |
| integrationOwner | SYNTH-SOURCE-REVIEWER |
| stageId | S29-10 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | decision→requirementsとcollections多対多→Evidence/Gap→owner/deadline/feedback。両者の同名六Statusを転記しない。第25章IRとは別要求。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-30

| Field | Value |
|---|---|
| artifactId | ART-30 |
| recordId | EST-2026-024-001 |
| sourceCaseId | CASE-OS24-001 |
| relationToFinal | independent |
| use | independent-comparison |
| canonicalPath | cases/ch24-source-evaluation-example.md |
| versionSha256 | 523c91b93ba4a17c769cb9fc44eeebc4e1ee14e7ee2465746e20a414b9c90b7a |
| templatePath | templates/evidence-source-evaluation-table.md |
| ownerChapter | 24 |
| nativeState/scope | first-evaluation |
| nativeState/line | 684 |
| nativeState/verbatim | &#124; &#96;use&#96; &#124; &#96;Context&#96; &#124; |
| integrationOwner | SYNTH-SOURCE-REVIEWER |
| stageId | S29-10 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | Source→版付きItem/Transform→Claim別Evaluation→Gap/Handoff。用途の五分類は法的区分でなく、同Itemの別Claim評価を複写しない。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-31

| Field | Value |
|---|---|
| artifactId | ART-31 |
| recordId | AIM-2026-027 |
| sourceCaseId | CASE-AI-2026-027 |
| relationToFinal | refines |
| use | method-reference |
| canonicalPath | cases/ch27-ai-agent-threat-model-example.md |
| versionSha256 | 490c04794f76ce762ca25c348bed8b9ceec879482ade126780e15f628d682ca0 |
| templatePath | templates/ai-agent-threat-model.md |
| ownerChapter | 27 |
| nativeState/scope | first-component |
| nativeState/line | 271 |
| nativeState/verbatim | &#124; status &#124; Declared &#124; |
| integrationOwner | SYNTH-AI-REVIEWER |
| stageId | S29-12 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | component/tool/version/approval/request→audit/evidence/finding→decision/reassessment。Allowed-in-modelでもexecuted=false、親Evidence/Authority非継承。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### artifacts-32

| Field | Value |
|---|---|
| artifactId | ART-32 |
| recordId | AAR-2026-028-001 |
| sourceCaseId | CASE-2026-025 |
| relationToFinal | independent |
| use | independent-comparison |
| canonicalPath | cases/ch28-ai-assisted-analysis-assurance-example.md |
| versionSha256 | ebe6d15331e30df48539a85fcc8ec67d5231833bf3fdf60138a7874c4bc9eb1d |
| templatePath | templates/ai-assisted-analysis-assurance-record.md |
| ownerChapter | 28 |
| nativeState/scope | first-claim |
| nativeState/line | 405 |
| nativeState/verbatim | &#124; status &#124; Supported &#124; |
| integrationOwner | SYNTH-AI-REVIEWER |
| stageId | S29-12 |
| evidenceTransfer | false |
| authorityTransfer | false |
| parentChanged | false |
| receiptCreated | false |
| readingBoundary | sourceSet/版→Claim/part/citation→verification→humanDecision/audit→reassessment/handoff。合成Acceptは実承認でなく、acceptedDecisionIdsは第29章の受領証拠ではない。 |
| reassessment | 親の版・対象・時点・参照関係が変われば本行を再照合する。親期限は更新しない。 |

### stages-1

| Field | Value |
|---|---|
| id | S29-01 |
| title | 目的と学習境界 |
| inputIds/0 | DR-CAP29-001 |
| artifactIds/0 | ART-01 |
| artifactIds/1 | ART-10 |
| artifactIds/2 | ART-14 |
| owner | SYNTH-PORTFOLIO-OWNER |
| result | 親ART-10の判断要求と独立学習Planを区別し、新しい判断期限を置く。 |
| gapId | GAP-CAP29-01 |

### stages-2

| Field | Value |
|---|---|
| id | S29-02 |
| title | AuthorityとScope |
| inputIds/0 | S29-01 |
| artifactIds/0 | ART-02 |
| artifactIds/1 | ART-13 |
| artifactIds/2 | ART-18 |
| owner | SYNTH-AUTHORITY-REVIEWER |
| result | Draft、過去のConditional、Lab八状態を同時に読んでも新しい実施許可にはならない。 |
| gapId | GAP-CAP29-01 |

### stages-3

| Field | Value |
|---|---|
| id | S29-03 |
| title | 資産と観測仮説 |
| inputIds/0 | S29-02 |
| artifactIds/0 | ART-03 |
| artifactIds/1 | ART-15 |
| artifactIds/2 | ART-16 |
| artifactIds/3 | ART-19 |
| owner | SYNTH-ASSET-REVIEWER |
| result | Threat、Behavior、Signal、Candidateを結び、Not collectedと観測後のInconclusiveを分ける。 |
| gapId | GAP-CAP29-01 |

### stages-4

| Field | Value |
|---|---|
| id | S29-04 |
| title | 優先度と評価 |
| inputIds/0 | S29-03 |
| artifactIds/0 | ART-11 |
| artifactIds/1 | ART-17 |
| artifactIds/2 | ART-20 |
| artifactIds/3 | ART-21 |
| artifactIds/4 | ART-22 |
| owner | SYNTH-ASSESSMENT-REVIEWER |
| result | 公開Snapshot、別Case、別App、対象版の違いを保持して評価の問いを選ぶ。 |
| gapId | GAP-CAP29-02 |

### stages-5

| Field | Value |
|---|---|
| id | S29-05 |
| title | FindingとRetest |
| inputIds/0 | S29-04 |
| artifactIds/0 | ART-04 |
| artifactIds/1 | ART-23 |
| owner | SYNTH-RETEST-REVIEWER |
| result | 同じBundleの二成果物を保持し、七対比を時系列や一括修正成功にしない。 |
| gapId | GAP-CAP29-02 |

### stages-6

| Field | Value |
|---|---|
| id | S29-06 |
| title | TelemetryとDetection |
| inputIds/0 | S29-05 |
| artifactIds/0 | ART-05 |
| artifactIds/1 | ART-24 |
| owner | SYNTH-DETECTION-REVIEWER |
| result | 有限fixtureのValidatedを実配備へ転用せず、Coverage欠落を残す。 |
| gapId | GAP-CAP29-02 |

### stages-7

| Field | Value |
|---|---|
| id | S29-07 |
| title | HuntとIncident |
| inputIds/0 | S29-06 |
| artifactIds/0 | ART-06 |
| artifactIds/1 | ART-25 |
| owner | SYNTH-INCIDENT-REVIEWER |
| result | SupportedからIncident宣言へ自動遷移せず、実宣言や対応を行わない。 |
| gapId | GAP-CAP29-03 |

### stages-8

| Field | Value |
|---|---|
| id | S29-08 |
| title | Timelineと原因 |
| inputIds/0 | S29-07 |
| artifactIds/0 | ART-07 |
| artifactIds/1 | ART-26 |
| owner | SYNTH-DFIR-REVIEWER |
| result | 同BundleのTimelineとRCAを別役割で読み、遅着と原因unresolvedを残す。 |
| gapId | GAP-CAP29-03 |

### stages-9

| Field | Value |
|---|---|
| id | S29-09 |
| title | Controlと改善 |
| inputIds/0 | S29-08 |
| artifactIds/0 | ART-27 |
| artifactIds/1 | ART-28 |
| owner | SYNTH-CONTROL-REVIEWER |
| result | Indeterminate、Partial、Accepted、Retiredを全Control合格へ変換しない。 |
| gapId | GAP-CAP29-03 |

### stages-10

| Field | Value |
|---|---|
| id | S29-10 |
| title | 要求とSource評価 |
| inputIds/0 | S29-09 |
| artifactIds/0 | ART-29 |
| artifactIds/1 | ART-30 |
| owner | SYNTH-SOURCE-REVIEWER |
| result | 方法参照と独立Caseを分け、取得予定と利用可能な根拠を混ぜない。 |
| gapId | GAP-CAP29-04 |

### stages-11

| Field | Value |
|---|---|
| id | S29-11 |
| title | 分析と二つのBrief |
| inputIds/0 | S29-10 |
| artifactIds/0 | ART-08 |
| artifactIds/1 | ART-09 |
| artifactIds/2 | ART-12 |
| owner | SYNTH-ANALYSIS-REVIEWER |
| result | CASE025のL2上限と未配達を保ち、同じ限定根拠から読者別の文面を作る。 |
| gapId | GAP-CAP29-04 |

### stages-12

| Field | Value |
|---|---|
| id | S29-12 |
| title | AI保証と再評価 |
| inputIds/0 | S29-11 |
| artifactIds/0 | ART-31 |
| artifactIds/1 | ART-32 |
| owner | SYNTH-AI-REVIEWER |
| result | モデル内許容と実効果を分け、AI採用判断を新Portfolioの受領証拠にしない。 |
| gapId | GAP-CAP29-04 |

### documentaryEvidence-1

| Field | Value |
|---|---|
| id | DOC-CAP29-01 |
| artifactId | ART-10 |
| path | cases/ch01-integrated-security-case-example.md |
| line | 22 |
| verbatim | Reassessment Due |
| sourceSha256 | c72c0d149321a24f2b6901db381c069cff86a8536b5578eba285b9d17eb329b2 |
| kind | authored-document-observation |
| claim | 親CaseはReassessment Dueの記録である。 |
| systemObservation | false |
| availableAt | 2026-10-21T00:00:00Z |

### documentaryEvidence-2

| Field | Value |
|---|---|
| id | DOC-CAP29-02 |
| artifactId | ART-02 |
| path | cases/ch09-engagement-roe-example.md |
| line | 33 |
| verbatim | Draft |
| sourceSha256 | 44cf657c9ad220709c6b026ec4a894d904b1f89d88427e3babd2070e5a11b25a |
| kind | authored-document-observation |
| claim | 後続RoEはDraftのままである。 |
| systemObservation | false |
| availableAt | 2026-10-21T00:00:00Z |

### documentaryEvidence-3

| Field | Value |
|---|---|
| id | DOC-CAP29-03 |
| artifactId | ART-10 |
| path | cases/ch01-integrated-security-case-example.md |
| line | 104 |
| verbatim | Inconclusive |
| sourceSha256 | c72c0d149321a24f2b6901db381c069cff86a8536b5578eba285b9d17eb329b2 |
| kind | authored-document-observation |
| claim | 過去侵害の仮説にはInconclusiveが残る。 |
| systemObservation | false |
| availableAt | 2026-10-21T00:00:00Z |

### documentaryEvidence-4

| Field | Value |
|---|---|
| id | DOC-CAP29-04 |
| artifactId | ART-09 |
| path | cases/ch26-cti-distribution-example.md |
| line | 360 |
| verbatim | prepared-not-delivered |
| sourceSha256 | 35d8a3b7342ba589e095fbd7b91e057c1e5194d332c55823fc35b731e612312e |
| kind | authored-document-observation |
| claim | 独立CASE025のExecutive Productは未配達である。 |
| systemObservation | false |
| availableAt | 2026-10-21T00:00:00Z |

### gaps-1

| Field | Value |
|---|---|
| id | GAP-CAP29-01 |
| kind | Not collected |
| question | 今回の再開を認める新しい許可・Scope・期間はあるか。 |
| artifactIds/0 | ART-02 |
| artifactIds/1 | ART-13 |
| artifactIds/2 | ART-18 |
| answer | 供給記録にはない。過去の許可を延長しない。 |
| owner | SYNTH-AUTHORITY-REVIEWER |
| dueAt | 2026-10-22T00:00:00Z |
| nextCheck | 第2/9章の許可条件へ戻り、新計画に必要な欄を紙上で列挙する。実申請・実収集は行わない。 |

### gaps-2

| Field | Value |
|---|---|
| id | GAP-CAP29-02 |
| kind | Inconclusive |
| question | 過去の侵害不存在、現在の実装と対策の全有効性を説明できるか。 |
| artifactIds/0 | ART-10 |
| artifactIds/1 | ART-03 |
| artifactIds/2 | ART-22 |
| artifactIds/3 | ART-24 |
| answer | 歴史的TH-2026-003はInconclusive。新しい実装・実効果は未観測で、別教材のPassedで埋めない。 |
| owner | SYNTH-ASSESSMENT-REVIEWER |
| dueAt | 2026-10-22T00:00:00Z |
| nextCheck | 第1/4/14/16章で既存Evidenceと未収集欄を区別し、同じ対象版に必要な確認をメモする。 |

### gaps-3

| Field | Value |
|---|---|
| id | GAP-CAP29-03 |
| kind | Residual risk |
| question | 原因確定、修正完了、受容と検証の責任を一本化してよいか。 |
| artifactIds/0 | ART-07 |
| artifactIds/1 | ART-23 |
| artifactIds/2 | ART-26 |
| artifactIds/3 | ART-27 |
| artifactIds/4 | ART-28 |
| answer | 原因unresolved、受容、Retest、未評価層が別々に残る。実務側の残余リスクはこの教材で解消しない。 |
| owner | SYNTH-CONTROL-REVIEWER |
| dueAt | 2026-10-22T00:00:00Z |
| nextCheck | 第15/20/21/22章で対象版・検証・受容期限を分けて読み直す。 |

### gaps-4

| Field | Value |
|---|---|
| id | GAP-CAP29-04 |
| kind | Not collected |
| question | CASE025のProductやAI判断をCASE001の実証根拠として受領したか。 |
| artifactIds/0 | ART-08 |
| artifactIds/1 | ART-09 |
| artifactIds/2 | ART-12 |
| artifactIds/3 | ART-29 |
| artifactIds/4 | ART-30 |
| artifactIds/5 | ART-31 |
| artifactIds/6 | ART-32 |
| answer | 受領していない。方法の参照であり、別CaseのEvidence・実権限・配送履歴は移さない。 |
| owner | SYNTH-ANALYSIS-REVIEWER |
| dueAt | 2026-10-22T00:00:00Z |
| nextCheck | 第23〜28章の来歴、独立原典、未配達、Claim採否へ戻る。外部照会・モデル呼出しは行わない。 |

### judgment

| Field | Value |
|---|---|
| id | AJ-CAP29-001 |
| inputStepId | S29-12 |
| evidenceIds/0 | DOC-CAP29-01 |
| evidenceIds/1 | DOC-CAP29-02 |
| evidenceIds/2 | DOC-CAP29-03 |
| evidenceIds/3 | DOC-CAP29-04 |
| gapIds/0 | GAP-CAP29-01 |
| gapIds/1 | GAP-CAP29-02 |
| gapIds/2 | GAP-CAP29-03 |
| gapIds/3 | GAP-CAP29-04 |
| confirmedFacts/0 | 親CaseはReassessment Dueの記録である。 |
| confirmedFacts/1 | 後続RoEはDraftのままである。 |
| confirmedFacts/2 | 過去侵害の仮説にはInconclusiveが残る。 |
| confirmedFacts/3 | 独立CASE025のExecutive Productは未配達である。 |
| assessment | 今回の資料だけでは再開・全Control完了を提案できない。 |
| confidence | 高 |
| confidenceScope | 供給文書の不足条件に限定。現在の実システムの安全性や侵害有無の確信度ではない。 |
| assumption | 全記録は架空で、取り込む版は固定されている。 |
| alternative | 新しい許可や同対象版の観測が別途存在する可能性はあるが、供給例には含まれない。 |
| prediction | 必要な版付き根拠が追加されれば再開可否の判断が変わり得る。 |
| recommendation | 保留案を提示し、Gapの担当・期限・再評価条件を返す。 |

### options-1

| Field | Value |
|---|---|
| id | OPT-CAP29-HOLD |
| label | 再開と完了宣言を保留し、不足条件を返す |
| requiredClosedGaps | &#91;&#93; |
| benefit | 不確実性と権限不足を隠さず次の判断条件を渡す。 |
| cost | 再評価の準備と判断遅延が残る。 |
| reversible | 新しい対象版のEvidence・Authority・独立レビューが揃えば新Portfolio版で見直す。 |

### options-2

| Field | Value |
|---|---|
| id | OPT-CAP29-RESUME |
| label | 今回の資料だけで実作業再開を提案する |
| requiredClosedGaps/0 | GAP-CAP29-01 |
| requiredClosedGaps/1 | GAP-CAP29-02 |
| benefit | 仮に成立すれば判断待ちを短縮する。 |
| cost | 必要な許可と観測が不足するため、この供給例では選べない。 |
| reversible | 実行しない。条件を満たした新計画の判断へ戻す。 |

### options-3

| Field | Value |
|---|---|
| id | OPT-CAP29-CLOSE |
| label | 全Control検証完了として閉じる |
| requiredClosedGaps/0 | GAP-CAP29-01 |
| requiredClosedGaps/1 | GAP-CAP29-02 |
| requiredClosedGaps/2 | GAP-CAP29-03 |
| requiredClosedGaps/3 | GAP-CAP29-04 |
| benefit | 成立すれば終了判断を明確化できる。 |
| cost | 別対象の結果や未配達を借用する誤りが必要になるため選べない。 |
| reversible | 誤った完了記録を作らず、元のGapへ戻す。 |

### reviews-1

| Field | Value |
|---|---|
| id | REV-CAP29-01 |
| area | Technical accuracy |
| reviewerRole | SYNTH-TECH-REVIEWER |
| result | Pass-with-limits |
| date | 2026-10-21T00:00:00Z |
| evidenceIds/0 | DOC-CAP29-01 |
| evidenceIds/1 | DOC-CAP29-02 |
| evidenceIds/2 | DOC-CAP29-03 |
| evidenceIds/3 | DOC-CAP29-04 |
| limitation | 供給記入例の架空レビュー。書籍PRの独立レビュー、人間承認、実システム検査ではない。 |

### reviews-2

| Field | Value |
|---|---|
| id | REV-CAP29-02 |
| area | Safety / legal / ethical boundary |
| reviewerRole | SYNTH-SAFETY-REVIEWER |
| result | Pass-with-limits |
| date | 2026-10-21T00:00:00Z |
| evidenceIds/0 | DOC-CAP29-01 |
| evidenceIds/1 | DOC-CAP29-02 |
| evidenceIds/2 | DOC-CAP29-03 |
| evidenceIds/3 | DOC-CAP29-04 |
| limitation | 供給記入例の架空レビュー。書籍PRの独立レビュー、人間承認、実システム検査ではない。 |

### reviews-3

| Field | Value |
|---|---|
| id | REV-CAP29-03 |
| area | Source quality / freshness |
| reviewerRole | SYNTH-SOURCE-REVIEWER |
| result | Pass-with-limits |
| date | 2026-10-21T00:00:00Z |
| evidenceIds/0 | DOC-CAP29-01 |
| evidenceIds/1 | DOC-CAP29-02 |
| evidenceIds/2 | DOC-CAP29-03 |
| evidenceIds/3 | DOC-CAP29-04 |
| limitation | 供給記入例の架空レビュー。書籍PRの独立レビュー、人間承認、実システム検査ではない。 |

### reviews-4

| Field | Value |
|---|---|
| id | REV-CAP29-04 |
| area | Analytic quality / uncertainty |
| reviewerRole | SYNTH-ANALYSIS-REVIEWER |
| result | Pass-with-limits |
| date | 2026-10-21T00:00:00Z |
| evidenceIds/0 | DOC-CAP29-01 |
| evidenceIds/1 | DOC-CAP29-02 |
| evidenceIds/2 | DOC-CAP29-03 |
| evidenceIds/3 | DOC-CAP29-04 |
| limitation | 供給記入例の架空レビュー。書籍PRの独立レビュー、人間承認、実システム検査ではない。 |

### reviews-5

| Field | Value |
|---|---|
| id | REV-CAP29-05 |
| area | Instructional clarity |
| reviewerRole | SYNTH-LEARNING-REVIEWER |
| result | Pass-with-limits |
| date | 2026-10-21T00:00:00Z |
| evidenceIds/0 | DOC-CAP29-01 |
| evidenceIds/1 | DOC-CAP29-02 |
| evidenceIds/2 | DOC-CAP29-03 |
| evidenceIds/3 | DOC-CAP29-04 |
| limitation | 供給記入例の架空レビュー。書籍PRの独立レビュー、人間承認、実システム検査ではない。 |

### reviews-6

| Field | Value |
|---|---|
| id | REV-CAP29-06 |
| area | Cross-book boundary / traceability |
| reviewerRole | SYNTH-BOUNDARY-REVIEWER |
| result | Pass-with-limits |
| date | 2026-10-21T00:00:00Z |
| evidenceIds/0 | DOC-CAP29-01 |
| evidenceIds/1 | DOC-CAP29-02 |
| evidenceIds/2 | DOC-CAP29-03 |
| evidenceIds/3 | DOC-CAP29-04 |
| limitation | 供給記入例の架空レビュー。書籍PRの独立レビュー、人間承認、実システム検査ではない。 |

### reviews-7

| Field | Value |
|---|---|
| id | REV-CAP29-07 |
| area | Reproducibility / deterministic build |
| reviewerRole | SYNTH-REPRO-REVIEWER |
| result | Pass-with-limits |
| date | 2026-10-21T00:00:00Z |
| evidenceIds/0 | DOC-CAP29-01 |
| evidenceIds/1 | DOC-CAP29-02 |
| evidenceIds/2 | DOC-CAP29-03 |
| evidenceIds/3 | DOC-CAP29-04 |
| limitation | 供給記入例の架空レビュー。書籍PRの独立レビュー、人間承認、実システム検査ではない。 |

### reviews-8

| Field | Value |
|---|---|
| id | REV-CAP29-08 |
| area | Publication / accessibility |
| reviewerRole | SYNTH-PUBLICATION-REVIEWER |
| result | Pass-with-limits |
| date | 2026-10-21T00:00:00Z |
| evidenceIds/0 | DOC-CAP29-01 |
| evidenceIds/1 | DOC-CAP29-02 |
| evidenceIds/2 | DOC-CAP29-03 |
| evidenceIds/3 | DOC-CAP29-04 |
| limitation | 供給記入例の架空レビュー。書籍PRの独立レビュー、人間承認、実システム検査ではない。 |

### decision

| Field | Value |
|---|---|
| id | DEC-CAP29-001 |
| requirementId | DR-CAP29-001 |
| judgmentId | AJ-CAP29-001 |
| owner | SYNTH-CTO |
| recommendedOption | OPT-CAP29-HOLD |
| approval | null |
| supersededBy | null |
| gapIds/0 | GAP-CAP29-01 |
| gapIds/1 | GAP-CAP29-02 |
| gapIds/2 | GAP-CAP29-03 |
| gapIds/3 | GAP-CAP29-04 |
| statusMeaning | ready-for-a-fictional-decision-not-approved-or-executed |
| residualRisk | 実務対象の未観測、過去期間の欠測、原因不確実性、未配達は残る。 |
| deliveryStatus | prepared-not-delivered |
| receiptId | null |
| realAuthorization | false |

### briefs-1

| Field | Value |
|---|---|
| id | BRIEF-CAP29-TECH |
| audience | Synthetic technical reviewer |
| judgmentId | AJ-CAP29-001 |
| evidenceIds/0 | DOC-CAP29-01 |
| evidenceIds/1 | DOC-CAP29-02 |
| evidenceIds/2 | DOC-CAP29-03 |
| evidenceIds/3 | DOC-CAP29-04 |
| gapIds/0 | GAP-CAP29-01 |
| gapIds/1 | GAP-CAP29-02 |
| gapIds/2 | GAP-CAP29-03 |
| gapIds/3 | GAP-CAP29-04 |
| text | 親のReassessment Due、RoE Draft、過去仮説Inconclusive、独立Product未配達を確認。版と対象を合わせずに結果を結合しない。次はGAP01〜04の元章の確認条件を記入する。 |
| deliveryStatus | prepared-not-delivered |

### briefs-2

| Field | Value |
|---|---|
| id | BRIEF-CAP29-EXEC |
| audience | Synthetic decision owner |
| judgmentId | AJ-CAP29-001 |
| evidenceIds/0 | DOC-CAP29-01 |
| evidenceIds/1 | DOC-CAP29-02 |
| evidenceIds/2 | DOC-CAP29-03 |
| evidenceIds/3 | DOC-CAP29-04 |
| gapIds/0 | GAP-CAP29-01 |
| gapIds/1 | GAP-CAP29-02 |
| gapIds/2 | GAP-CAP29-03 |
| gapIds/3 | GAP-CAP29-04 |
| text | 再開・完了の根拠が不足するため保留を推奨する。判断遅延と未観測の残余リスクを明示し、担当と期限を付けて再評価条件を返す。実承認や配送は行わない。 |
| deliveryStatus | prepared-not-delivered |

### actions-1

| Field | Value |
|---|---|
| id | ACT-CAP29-01 |
| decisionId | DEC-CAP29-001 |
| gapId | GAP-CAP29-01 |
| owner | SYNTH-AUTHORITY-REVIEWER |
| dueAt | 2026-10-22T00:00:00Z |
| instruction | 第2/9章の許可条件へ戻り、新計画に必要な欄を紙上で列挙する。実申請・実収集は行わない。 |
| verification | 元章のID・版・不足・停止条件を説明した作業メモをレビューする。実Control合格は判定しない。 |
| result | Planned |
| executed | false |

### actions-2

| Field | Value |
|---|---|
| id | ACT-CAP29-02 |
| decisionId | DEC-CAP29-001 |
| gapId | GAP-CAP29-02 |
| owner | SYNTH-ASSESSMENT-REVIEWER |
| dueAt | 2026-10-22T00:00:00Z |
| instruction | 第1/4/14/16章で既存Evidenceと未収集欄を区別し、同じ対象版に必要な確認をメモする。 |
| verification | 元章のID・版・不足・停止条件を説明した作業メモをレビューする。実Control合格は判定しない。 |
| result | Planned |
| executed | false |

### actions-3

| Field | Value |
|---|---|
| id | ACT-CAP29-03 |
| decisionId | DEC-CAP29-001 |
| gapId | GAP-CAP29-03 |
| owner | SYNTH-CONTROL-REVIEWER |
| dueAt | 2026-10-22T00:00:00Z |
| instruction | 第15/20/21/22章で対象版・検証・受容期限を分けて読み直す。 |
| verification | 元章のID・版・不足・停止条件を説明した作業メモをレビューする。実Control合格は判定しない。 |
| result | Planned |
| executed | false |

### actions-4

| Field | Value |
|---|---|
| id | ACT-CAP29-04 |
| decisionId | DEC-CAP29-001 |
| gapId | GAP-CAP29-04 |
| owner | SYNTH-ANALYSIS-REVIEWER |
| dueAt | 2026-10-22T00:00:00Z |
| instruction | 第23〜28章の来歴、独立原典、未配達、Claim採否へ戻る。外部照会・モデル呼出しは行わない。 |
| verification | 元章のID・版・不足・停止条件を説明した作業メモをレビューする。実Control合格は判定しない。 |
| result | Planned |
| executed | false |

### reassessment

| Field | Value |
|---|---|
| id | REA-CAP29-001 |
| decisionId | DEC-CAP29-001 |
| actionIds/0 | ACT-CAP29-01 |
| actionIds/1 | ACT-CAP29-02 |
| actionIds/2 | ACT-CAP29-03 |
| actionIds/3 | ACT-CAP29-04 |
| scheduledAt | 2026-10-22T00:00:00Z |
| expiry | 2026-10-28T00:00:00Z |
| triggers/0 | parent-version-change |
| triggers/1 | case-or-scope-change |
| triggers/2 | source-correction |
| triggers/3 | new-evidence-or-authority |
| triggers/4 | receipt-or-review-change |
| triggers/5 | expiry |
| closure | 必要な同対象版の根拠を独立レビューし、新版で判断する。旧版の不足を遡及削除しない。 |

### sourceIds-1

| Field | Value |
|---|---|
| value | SRC-CSF-001 |

### sourceIds-2

| Field | Value |
|---|---|
| value | SRC-NIST-RISK-001 |

## 次の確認

保留の理由、四Action、期限と再評価Triggerを説明できるか確認し、[第29章の自己点検](../manuscript/29-capstone-case-study.md)へ戻る。実収集でGapを埋める演習ではない。
