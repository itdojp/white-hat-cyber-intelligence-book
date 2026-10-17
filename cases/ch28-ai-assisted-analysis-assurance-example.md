# 第28章 合成AI支援分析の保証記録

## このCaseの境界

この全欄例は著者作成の固定記録であり、実Model/API/原Telemetryの測定、実承認、実観測ではない。親CASE-2026-025を教育上refinesし、第24/27章や独立STIXからEvidenceやAuthorityを継承しない。

[供給JSON](fixtures/ch28-ai-assisted-analysis-assurance.json)と[閉Schema](../schemas/ch28-ai-assisted-analysis-assurance.schema.json)はこの全欄例と同じ固定記録である。書込・API・Model実行を必要としない。

## 七Claimの読み方

| Claim | Status | Human decision | 採用範囲 |
|---|---|---|---|
| AI28-CLAIM-1 | Supported | Accept | quarantine mail was present |
| AI28-CLAIM-2 | Partially supported | Revise | quarantine mail was present |
| AI28-CLAIM-3 | Contradicted | Reject | not-adopted |
| AI28-CLAIM-4 | Rejected | Reject | not-adopted |
| AI28-CLAIM-5 | Unverified | Escalate | not-adopted |
| AI28-CLAIM-6 | Rejected | Reject | not-adopted |
| AI28-CLAIM-7 | Rejected | Reject | not-adopted |

CLAIM2の支持句はmailの存在だけで、成功の不存在や未遂確定を意味しない。CLAIM3は親lineageによる反証、CLAIM4/6/7は不適格・由来喪失・帰属越境による不受理、CLAIM5は未検証を区別する。

Source/Tool/Memory試料はData内の承認自己申告を読解するだけで、防御製品の検出実験ではない。sourceSetのhashはJSON記録、educationalEvidenceHashは親が供給する架空値で、原ログの実測ではない。

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

### realPIIUsed

| Field | Value |
|---|---|
| value | false |

### realSecretUsed

| Field | Value |
|---|---|
| value | false |

### record

| Field | Value |
|---|---|
| id | AAR-2026-028-001 |
| caseId | CASE-2026-025 |
| parentCaseId | CASE-2026-025 |
| relation | refines |
| artifactId | ART-32 |
| parentArtifactId | ART-12 |
| parentDistributionId | CDP-2026-026-001 |
| asOf | 2026-07-29T11:00:00Z |
| cutoff | 2026-07-29T09:00:00Z |
| reviewDeadline | 2026-07-30T01:00:00Z |
| attributionCeiling | L2 |
| setting | author-created offline representation; no historical AI execution |

### task

| Field | Value |
|---|---|
| id | AI28-TASK |
| requirementId | DR-2026-025 |
| intelligenceRequirementId | IR-2026-025 |
| judgmentId | AJ-2026-025 |
| decisionId | DEC-2026-025 |
| ownerId | SYNTH-AI28-OWNER |
| purpose | verify Claim provenance without changing the parent decision |
| successCondition | trace supported wording and unadopted claims to human decisions |

### sourceSet

| Field | Value |
|---|---|
| id | AI28-SOURCESET |
| version | 1.0.0 |
| sourceIds/0 | SN-2026-025-001 |
| sourceIds/1 | SN-2026-025-002 |
| sourceIds/2 | SN-2026-025-003 |
| sourceIds/3 | SN-2026-025-004 |
| sourceIds/4 | SN-2026-025-005 |
| sourceIds/5 | SN-2026-025-006 |
| sourceIds/6 | SN-2026-025-007 |
| sourceIds/7 | SN-2026-025-008 |
| sha256 | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| classification | fully-synthetic |
| hashMeaning | structured educational records, not original telemetry measurement |

### SN-2026-025-001

| Field | Value |
|---|---|
| id | SN-2026-025-001 |
| origin | synthetic-mail-gateway |
| version | parent25-fixed-record |
| independenceGroupId | IG-INT-001 |
| reference | mail-notice.example/message/042 |
| collectedAt | 2026-07-26T23:40:00Z |
| validUntil | 2026-07-30T01:00:00Z |
| evidenceIds/0 | EVD-2026-025-001 |
| educationalEvidenceHash | sha256:1111111111111111111111111111111111111111111111111111111111111111 |
| limitation | Mail bodyは要約保持、archive完全性は別証跡がない。 |
| newObservation | false |

### SN-2026-025-002

| Field | Value |
|---|---|
| id | SN-2026-025-002 |
| origin | synthetic-decoy-proxy |
| version | parent25-fixed-record |
| independenceGroupId | IG-INT-002 |
| reference | signin-bridge.example/log/edge-20260727 |
| collectedAt | 2026-07-27T00:10:00Z |
| validUntil | 2026-07-30T01:00:00Z |
| evidenceIds/0 | EVD-2026-025-002 |
| educationalEvidenceHash | sha256:2222222222222222222222222222222222222222222222222222222222222222 |
| limitation | 後段の成功・失敗はこの観測に含まない。 |
| newObservation | false |

### SN-2026-025-003

| Field | Value |
|---|---|
| id | SN-2026-025-003 |
| origin | synthetic-registrar-export |
| version | parent25-fixed-record |
| independenceGroupId | IG-EXT-001 |
| reference | portal-reset.example/registration/export |
| collectedAt | 2026-07-27T01:05:00Z |
| validUntil | 2026-07-30T01:00:00Z |
| evidenceIds/0 | EVD-2026-025-003 |
| educationalEvidenceHash | sha256:3333333333333333333333333333333333333333333333333333333333333333 |
| limitation | 登録者は判定できない。 |
| newObservation | false |

### SN-2026-025-004

| Field | Value |
|---|---|
| id | SN-2026-025-004 |
| origin | synthetic-vendor-bulletin |
| version | parent25-fixed-record |
| independenceGroupId | IG-EXT-002 |
| reference | blue-quill.example/bulletins/2026-07-28 |
| collectedAt | 2026-07-27T22:50:00Z |
| validUntil | 2026-07-30T01:00:00Z |
| evidenceIds/0 | EVD-2026-025-004 |
| educationalEvidenceHash | sha256:4444444444444444444444444444444444444444444444444444444444444444 |
| limitation | bulletin revision履歴がない。 |
| newObservation | false |

### SN-2026-025-005

| Field | Value |
|---|---|
| id | SN-2026-025-005 |
| origin | synthetic-blog-repost |
| version | parent25-fixed-record |
| independenceGroupId | IG-EXT-002 |
| reference | harbor-signal.example/posts/relay-cluster |
| collectedAt | 2026-07-28T03:00:00Z |
| validUntil | 2026-07-30T01:00:00Z |
| evidenceIds/0 | EVD-2026-025-005 |
| educationalEvidenceHash | sha256:5555555555555555555555555555555555555555555555555555555555555555 |
| limitation | 独自観測のない再掲。 |
| newObservation | false |

### SN-2026-025-006

| Field | Value |
|---|---|
| id | SN-2026-025-006 |
| origin | synthetic-translated-excerpt |
| version | parent25-fixed-record |
| independenceGroupId | IG-EXT-003 |
| reference | chat-excerpt.example/item/17 |
| collectedAt | 2026-07-28T23:20:00Z |
| validUntil | 2026-07-30T01:00:00Z |
| evidenceIds/0 | EVD-2026-025-006 |
| educationalEvidenceHash | sha256:6666666666666666666666666666666666666666666666666666666666666666 |
| limitation | 原文全文・発言者が未確認。 |
| newObservation | false |

### SN-2026-025-007

| Field | Value |
|---|---|
| id | SN-2026-025-007 |
| origin | synthetic-newsletter-recap |
| version | parent25-fixed-record |
| independenceGroupId | IG-EXT-002 |
| reference | weekly-brief.example/2026-07-29/relay |
| collectedAt | 2026-07-29T00:45:00Z |
| validUntil | 2026-07-30T01:00:00Z |
| evidenceIds/0 | EVD-2026-025-007 |
| educationalEvidenceHash | sha256:7777777777777777777777777777777777777777777777777777777777777777 |
| limitation | 同じbulletinの再要約。 |
| newObservation | false |

### SN-2026-025-008

| Field | Value |
|---|---|
| id | SN-2026-025-008 |
| origin | synthetic-idp-sign-in-summary |
| version | parent25-fixed-record |
| independenceGroupId | IG-INT-003 |
| reference | `idp-summary.example/reports/2026-07-23--2026-07-29` |
| collectedAt | 2026-07-29T01:15:00Z |
| validUntil | 2026-07-30T01:00:00Z |
| evidenceIds/0 | EVD-2026-025-008 |
| educationalEvidenceHash | sha256:8888888888888888888888888888888888888888888888888888888888888888 |
| limitation | 2026-07-23〜29のsummaryのみ。前半二日と詳細token issuanceは欠落。 |
| newObservation | false |

### AI28-PASSAGE-MAIL

| Field | Value |
|---|---|
| id | AI28-PASSAGE-MAIL |
| text | quarantine mail was present |
| comparedStatement | quarantine mail was present |
| sourceIds/0 | SN-2026-025-001 |
| outcome | supported |
| parentDocument | cases/fixtures/ch25-structured-analysis-attribution-dataset.json |
| parentPaths/0/0 | judgments |
| parentPaths/0/1 | confirmedFacts |
| parentPaths/0/2 | 0 |
| parentPaths/0/3 | statement |
| parentValuesHash | f6a9a2bbc8cbc5526e8310402d6522dc582fc292e2e60f130dc10f1de2b176c7 |
| meaning | author-labelled finite comparison; not a general language classifier |

### AI28-PASSAGE-SUCCESS

| Field | Value |
|---|---|
| id | AI28-PASSAGE-SUCCESS |
| text | successful follow-on access remains unconfirmed |
| comparedStatement | successful follow-on access is established |
| sourceIds/0 | SN-2026-025-008 |
| outcome | unknown |
| parentDocument | cases/fixtures/ch25-structured-analysis-attribution-dataset.json |
| parentPaths/0/0 | collectionGaps |
| parentPaths/0/1 | 0 |
| parentPaths/0/2 | decisionImpact |
| parentPaths/1/0 | negativeFindings |
| parentPaths/1/1 | 0 |
| parentPaths/1/2 | permittedConclusion |
| parentValuesHash | 950da66d60454c38ed5132d381cbd8900c2b155032e2551f1693d43fb85c5acb |
| meaning | author-labelled finite comparison; not a general language classifier |

### AI28-PASSAGE-ORIGINS

| Field | Value |
|---|---|
| id | AI28-PASSAGE-ORIGINS |
| text | vendor bulletin, repost, and recap are not three independent external observations |
| comparedStatement | three reports are three independent observations |
| sourceIds/0 | SN-2026-025-004 |
| sourceIds/1 | SN-2026-025-005 |
| sourceIds/2 | SN-2026-025-007 |
| outcome | contradicted |
| parentDocument | cases/fixtures/ch25-structured-analysis-attribution-dataset.json |
| parentPaths/0/0 | sourceEvaluationJudgments |
| parentPaths/0/1 | 0 |
| parentPaths/0/2 | statement |
| parentPaths/1/0 | lineage |
| parentPaths/1/1 | circularReportingCandidates |
| parentPaths/1/2 | 0 |
| parentValuesHash | 46ff5d5800d970b672a7b58c6fcbe5db464a597aa9d8734db145231173720701 |
| meaning | author-labelled finite comparison; not a general language classifier |

### AI28-PASSAGE-CLUSTER

| Field | Value |
|---|---|
| id | AI28-PASSAGE-CLUSTER |
| text | Technical cluster only; Campaign and Operator are not supported |
| comparedStatement | same operator or state is established with certainty |
| sourceIds/0 | SN-2026-025-001 |
| sourceIds/1 | SN-2026-025-002 |
| sourceIds/2 | SN-2026-025-003 |
| sourceIds/3 | SN-2026-025-004 |
| outcome | unknown |
| parentDocument | cases/fixtures/ch25-structured-analysis-attribution-dataset.json |
| parentPaths/0/0 | attributionAssessment |
| parentPaths/1/0 | judgments |
| parentPaths/1/1 | analyticJudgment |
| parentValuesHash | 7212e1acb7a4b20b593267a12b7c4880cd58e23e0c96dcf1986d1ed8283ab76a |
| meaning | author-labelled finite comparison; not a general language classifier |

### model

| Field | Value |
|---|---|
| id | AI28-MODEL |
| version | author-descriptor-1 |
| runtime | offline-authored-not-model-runtime |
| endpoint | none |
| modelExecuted | false |
| toolCapability | none |
| networkEnabled | false |

### instruction

| Field | Value |
|---|---|
| id | AI28-INSTRUCTION |
| text | Separate source text, Claim verification, and human adoption. No action is authorized. |
| sha256 | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| layer | author-fixed-instruction |

### input

| Field | Value |
|---|---|
| id | AI28-INPUT |
| text | Use the eight synthetic parent records and keep their limitations and common origins. |
| sha256 | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| sourceSetId | AI28-SOURCESET |
| sourceIds/0 | SN-2026-025-001 |
| sourceIds/1 | SN-2026-025-002 |
| sourceIds/2 | SN-2026-025-003 |
| sourceIds/3 | SN-2026-025-004 |
| sourceIds/4 | SN-2026-025-005 |
| sourceIds/5 | SN-2026-025-006 |
| sourceIds/6 | SN-2026-025-007 |
| sourceIds/7 | SN-2026-025-008 |
| classification | fully-synthetic |
| redaction | no real personal or secret data exists |
| transformation | author-created English summaries; parent JSON pointers are retained |
| contaminationSampleIds/0 | AI28-CONT-SOURCE |
| contaminationSampleIds/1 | AI28-CONT-TOOL |
| contaminationSampleIds/2 | AI28-CONT-MEMORY |
| contaminationIncludedInApprovedSources | false |

### output

| Field | Value |
|---|---|
| id | AI28-OUTPUT |
| version | 1.0.0 |
| at | 2026-07-29T09:30:00Z |
| authoredOffline | true |
| modelExecuted | false |
| text | quarantine mail was present / quarantine mail was present; successful follow-on access is established / three reports are three independent observations / the invented citation establishes the conclusion / successful follow-on access is established / quarantine mail was present but its Source ID was lost / same operator or state is established with certainty |
| sha256 | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| claimIds/0 | AI28-CLAIM-1 |
| claimIds/1 | AI28-CLAIM-2 |
| claimIds/2 | AI28-CLAIM-3 |
| claimIds/3 | AI28-CLAIM-4 |
| claimIds/4 | AI28-CLAIM-5 |
| claimIds/5 | AI28-CLAIM-6 |
| claimIds/6 | AI28-CLAIM-7 |

### AI28-CLAIM-1

| Field | Value |
|---|---|
| id | AI28-CLAIM-1 |
| text | quarantine mail was present |
| textHash | 459e90e224fb554a318c87f32acf53f70cb580525fa8cb652076c79f92c6f0ea |
| claimType | confirmed-fact |
| grounding | Direct |
| citations/0 | SN-2026-025-001 |
| parts/0/statement | quarantine mail was present |
| parts/0/sourceText | quarantine mail was present |
| parts/0/passageId | AI28-PASSAGE-MAIL |
| parts/0/sourceIds/0 | SN-2026-025-001 |
| parts/0/outcome | supported |
| contaminated | false |
| proposedAttribution | L0 |
| modelSelfConfidence | 99 |
| verificationId | AI28-VERIFY-1 |
| decisionId | AI28-HUMAN-1 |
| status | Supported |

### AI28-CLAIM-2

| Field | Value |
|---|---|
| id | AI28-CLAIM-2 |
| text | quarantine mail was present; successful follow-on access is established |
| textHash | 0f68c6f89fd1f6a3ce36214c1cff269ac6afe615d75faf1e808cd57da3cbc459 |
| claimType | judgment |
| grounding | Composite |
| citations/0 | SN-2026-025-001 |
| citations/1 | SN-2026-025-008 |
| parts/0/statement | quarantine mail was present |
| parts/0/sourceText | quarantine mail was present |
| parts/0/passageId | AI28-PASSAGE-MAIL |
| parts/0/sourceIds/0 | SN-2026-025-001 |
| parts/0/outcome | supported |
| parts/1/statement | successful follow-on access is established |
| parts/1/sourceText | successful follow-on access remains unconfirmed |
| parts/1/passageId | AI28-PASSAGE-SUCCESS |
| parts/1/sourceIds/0 | SN-2026-025-008 |
| parts/1/outcome | unknown |
| contaminated | false |
| proposedAttribution | L2 |
| modelSelfConfidence | 99 |
| verificationId | AI28-VERIFY-2 |
| decisionId | AI28-HUMAN-2 |
| status | Partially supported |

### AI28-CLAIM-3

| Field | Value |
|---|---|
| id | AI28-CLAIM-3 |
| text | three reports are three independent observations |
| textHash | 2a9f2626283568d85bd253d6b254dcb4ed1215876242e57bf5a672525e5fbded |
| claimType | judgment |
| grounding | Direct |
| citations/0 | SN-2026-025-004 |
| citations/1 | SN-2026-025-005 |
| citations/2 | SN-2026-025-007 |
| parts/0/statement | three reports are three independent observations |
| parts/0/sourceText | vendor bulletin, repost, and recap are not three independent external observations |
| parts/0/passageId | AI28-PASSAGE-ORIGINS |
| parts/0/sourceIds/0 | SN-2026-025-004 |
| parts/0/sourceIds/1 | SN-2026-025-005 |
| parts/0/sourceIds/2 | SN-2026-025-007 |
| parts/0/outcome | contradicted |
| contaminated | false |
| proposedAttribution | L2 |
| modelSelfConfidence | 99 |
| verificationId | AI28-VERIFY-3 |
| decisionId | AI28-HUMAN-3 |
| status | Contradicted |

### AI28-CLAIM-4

| Field | Value |
|---|---|
| id | AI28-CLAIM-4 |
| text | the invented citation establishes the conclusion |
| textHash | b1e6029cfde8ad24ea6cf1f6ef27e5a2afe81f159ee88ef8dd92f797cacb1cf5 |
| claimType | judgment |
| grounding | Inference |
| citations/0 | SN-FAKE-028 |
| parts/0/statement | the invented citation establishes the conclusion |
| parts/0/sourceText | not-found |
| parts/0/passageId | null |
| parts/0/sourceIds | `[]` |
| parts/0/outcome | unknown |
| contaminated | false |
| proposedAttribution | L2 |
| modelSelfConfidence | 99 |
| verificationId | AI28-VERIFY-4 |
| decisionId | AI28-HUMAN-4 |
| status | Rejected |

### AI28-CLAIM-5

| Field | Value |
|---|---|
| id | AI28-CLAIM-5 |
| text | successful follow-on access is established |
| textHash | 97ab1dd89c0fd4ab674b0b8361c1cd6cce04a7a0aee963d19c52541cd6d61a8b |
| claimType | judgment |
| grounding | Inference |
| citations/0 | SN-2026-025-008 |
| parts/0/statement | successful follow-on access is established |
| parts/0/sourceText | successful follow-on access remains unconfirmed |
| parts/0/passageId | AI28-PASSAGE-SUCCESS |
| parts/0/sourceIds/0 | SN-2026-025-008 |
| parts/0/outcome | unknown |
| contaminated | false |
| proposedAttribution | L2 |
| modelSelfConfidence | 99 |
| verificationId | AI28-VERIFY-5 |
| decisionId | AI28-HUMAN-5 |
| status | Unverified |

### AI28-CLAIM-6

| Field | Value |
|---|---|
| id | AI28-CLAIM-6 |
| text | quarantine mail was present but its Source ID was lost |
| textHash | cb8f6ed1b7d9d2a62e9d440460e3bca4c72e0692c05860a230a760604940869d |
| claimType | confirmed-fact |
| grounding | Direct |
| citations | `[]` |
| parts/0/statement | quarantine mail was present but its Source ID was lost |
| parts/0/sourceText | not-found |
| parts/0/passageId | null |
| parts/0/sourceIds | `[]` |
| parts/0/outcome | unknown |
| contaminated | false |
| proposedAttribution | L0 |
| modelSelfConfidence | 99 |
| verificationId | AI28-VERIFY-6 |
| decisionId | AI28-HUMAN-6 |
| status | Rejected |

### AI28-CLAIM-7

| Field | Value |
|---|---|
| id | AI28-CLAIM-7 |
| text | same operator or state is established with certainty |
| textHash | 809e7611e379656a90c87baae504496a7f912f65be1aca46173799980cc7c24a |
| claimType | judgment |
| grounding | Inference |
| citations/0 | SN-2026-025-001 |
| citations/1 | SN-2026-025-002 |
| citations/2 | SN-2026-025-003 |
| citations/3 | SN-2026-025-004 |
| parts/0/statement | same operator or state is established with certainty |
| parts/0/sourceText | Technical cluster only; Campaign and Operator are not supported |
| parts/0/passageId | AI28-PASSAGE-CLUSTER |
| parts/0/sourceIds/0 | SN-2026-025-001 |
| parts/0/sourceIds/1 | SN-2026-025-002 |
| parts/0/sourceIds/2 | SN-2026-025-003 |
| parts/0/sourceIds/3 | SN-2026-025-004 |
| parts/0/outcome | unknown |
| contaminated | false |
| proposedAttribution | L4 |
| modelSelfConfidence | 99 |
| verificationId | AI28-VERIFY-7 |
| decisionId | AI28-HUMAN-7 |
| status | Rejected |

### AI28-VERIFY-1

| Field | Value |
|---|---|
| id | AI28-VERIFY-1 |
| target/claimId | AI28-CLAIM-1 |
| target/claimHash | 459e90e224fb554a318c87f32acf53f70cb580525fa8cb652076c79f92c6f0ea |
| target/sourceSetId | AI28-SOURCESET |
| target/sourceSetVersion | 1.0.0 |
| target/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| target/modelId | AI28-MODEL |
| target/modelVersion | author-descriptor-1 |
| target/runtime | offline-authored-not-model-runtime |
| target/instructionId | AI28-INSTRUCTION |
| target/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| target/inputId | AI28-INPUT |
| target/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| target/outputId | AI28-OUTPUT |
| target/outputVersion | 1.0.0 |
| target/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| complete | true |
| at | 2026-07-29T10:00:00Z |
| originGroups/0 | IG-INT-001 |
| independentOriginCount | 1 |
| crossCheck | parent-structured-record-and-lineage |
| independentObservationAdded | false |
| reasons/0 | bounded-passages-supported |

### AI28-VERIFY-2

| Field | Value |
|---|---|
| id | AI28-VERIFY-2 |
| target/claimId | AI28-CLAIM-2 |
| target/claimHash | 0f68c6f89fd1f6a3ce36214c1cff269ac6afe615d75faf1e808cd57da3cbc459 |
| target/sourceSetId | AI28-SOURCESET |
| target/sourceSetVersion | 1.0.0 |
| target/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| target/modelId | AI28-MODEL |
| target/modelVersion | author-descriptor-1 |
| target/runtime | offline-authored-not-model-runtime |
| target/instructionId | AI28-INSTRUCTION |
| target/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| target/inputId | AI28-INPUT |
| target/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| target/outputId | AI28-OUTPUT |
| target/outputVersion | 1.0.0 |
| target/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| complete | true |
| at | 2026-07-29T10:00:00Z |
| originGroups/0 | IG-INT-001 |
| originGroups/1 | IG-INT-003 |
| independentOriginCount | 2 |
| crossCheck | parent-structured-record-and-lineage |
| independentObservationAdded | false |
| reasons/0 | supported-and-unknown-parts |

### AI28-VERIFY-3

| Field | Value |
|---|---|
| id | AI28-VERIFY-3 |
| target/claimId | AI28-CLAIM-3 |
| target/claimHash | 2a9f2626283568d85bd253d6b254dcb4ed1215876242e57bf5a672525e5fbded |
| target/sourceSetId | AI28-SOURCESET |
| target/sourceSetVersion | 1.0.0 |
| target/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| target/modelId | AI28-MODEL |
| target/modelVersion | author-descriptor-1 |
| target/runtime | offline-authored-not-model-runtime |
| target/instructionId | AI28-INSTRUCTION |
| target/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| target/inputId | AI28-INPUT |
| target/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| target/outputId | AI28-OUTPUT |
| target/outputVersion | 1.0.0 |
| target/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| complete | true |
| at | 2026-07-29T10:00:00Z |
| originGroups/0 | IG-EXT-002 |
| independentOriginCount | 1 |
| crossCheck | parent-structured-record-and-lineage |
| independentObservationAdded | false |
| reasons/0 | authored-counterevidence |

### AI28-VERIFY-4

| Field | Value |
|---|---|
| id | AI28-VERIFY-4 |
| target/claimId | AI28-CLAIM-4 |
| target/claimHash | b1e6029cfde8ad24ea6cf1f6ef27e5a2afe81f159ee88ef8dd92f797cacb1cf5 |
| target/sourceSetId | AI28-SOURCESET |
| target/sourceSetVersion | 1.0.0 |
| target/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| target/modelId | AI28-MODEL |
| target/modelVersion | author-descriptor-1 |
| target/runtime | offline-authored-not-model-runtime |
| target/instructionId | AI28-INSTRUCTION |
| target/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| target/inputId | AI28-INPUT |
| target/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| target/outputId | AI28-OUTPUT |
| target/outputVersion | 1.0.0 |
| target/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| complete | true |
| at | 2026-07-29T10:00:00Z |
| originGroups | `[]` |
| independentOriginCount | 0 |
| crossCheck | parent-structured-record-and-lineage |
| independentObservationAdded | false |
| reasons/0 | ineligible-provenance-or-boundary |

### AI28-VERIFY-5

| Field | Value |
|---|---|
| id | AI28-VERIFY-5 |
| target/claimId | AI28-CLAIM-5 |
| target/claimHash | 97ab1dd89c0fd4ab674b0b8361c1cd6cce04a7a0aee963d19c52541cd6d61a8b |
| target/sourceSetId | AI28-SOURCESET |
| target/sourceSetVersion | 1.0.0 |
| target/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| target/modelId | AI28-MODEL |
| target/modelVersion | author-descriptor-1 |
| target/runtime | offline-authored-not-model-runtime |
| target/instructionId | AI28-INSTRUCTION |
| target/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| target/inputId | AI28-INPUT |
| target/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| target/outputId | AI28-OUTPUT |
| target/outputVersion | 1.0.0 |
| target/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| complete | false |
| at | 2026-07-29T10:00:00Z |
| originGroups/0 | IG-INT-003 |
| independentOriginCount | 1 |
| crossCheck | parent-structured-record-and-lineage |
| independentObservationAdded | false |
| reasons/0 | verification-incomplete |

### AI28-VERIFY-6

| Field | Value |
|---|---|
| id | AI28-VERIFY-6 |
| target/claimId | AI28-CLAIM-6 |
| target/claimHash | cb8f6ed1b7d9d2a62e9d440460e3bca4c72e0692c05860a230a760604940869d |
| target/sourceSetId | AI28-SOURCESET |
| target/sourceSetVersion | 1.0.0 |
| target/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| target/modelId | AI28-MODEL |
| target/modelVersion | author-descriptor-1 |
| target/runtime | offline-authored-not-model-runtime |
| target/instructionId | AI28-INSTRUCTION |
| target/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| target/inputId | AI28-INPUT |
| target/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| target/outputId | AI28-OUTPUT |
| target/outputVersion | 1.0.0 |
| target/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| complete | true |
| at | 2026-07-29T10:00:00Z |
| originGroups | `[]` |
| independentOriginCount | 0 |
| crossCheck | parent-structured-record-and-lineage |
| independentObservationAdded | false |
| reasons/0 | ineligible-provenance-or-boundary |

### AI28-VERIFY-7

| Field | Value |
|---|---|
| id | AI28-VERIFY-7 |
| target/claimId | AI28-CLAIM-7 |
| target/claimHash | 809e7611e379656a90c87baae504496a7f912f65be1aca46173799980cc7c24a |
| target/sourceSetId | AI28-SOURCESET |
| target/sourceSetVersion | 1.0.0 |
| target/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| target/modelId | AI28-MODEL |
| target/modelVersion | author-descriptor-1 |
| target/runtime | offline-authored-not-model-runtime |
| target/instructionId | AI28-INSTRUCTION |
| target/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| target/inputId | AI28-INPUT |
| target/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| target/outputId | AI28-OUTPUT |
| target/outputVersion | 1.0.0 |
| target/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| complete | true |
| at | 2026-07-29T10:00:00Z |
| originGroups/0 | IG-INT-001 |
| originGroups/1 | IG-INT-002 |
| originGroups/2 | IG-EXT-001 |
| originGroups/3 | IG-EXT-002 |
| independentOriginCount | 4 |
| crossCheck | parent-structured-record-and-lineage |
| independentObservationAdded | false |
| reasons/0 | ineligible-provenance-or-boundary |

### AI28-HUMAN-1

| Field | Value |
|---|---|
| id | AI28-HUMAN-1 |
| target/claimId | AI28-CLAIM-1 |
| target/claimHash | 459e90e224fb554a318c87f32acf53f70cb580525fa8cb652076c79f92c6f0ea |
| target/sourceSetId | AI28-SOURCESET |
| target/sourceSetVersion | 1.0.0 |
| target/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| target/modelId | AI28-MODEL |
| target/modelVersion | author-descriptor-1 |
| target/runtime | offline-authored-not-model-runtime |
| target/instructionId | AI28-INSTRUCTION |
| target/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| target/inputId | AI28-INPUT |
| target/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| target/outputId | AI28-OUTPUT |
| target/outputVersion | 1.0.0 |
| target/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| verificationId | AI28-VERIFY-1 |
| reviewerId | SYNTH-AI28-REVIEWER |
| reviewedAt | 2026-07-29T10:30:00Z |
| validUntil | 2026-07-30T01:00:00Z |
| disposition | Accept |
| acceptedWording | quarantine mail was present |
| rationale | retain parent scope; do not adopt unverified output |
| analyticConfidence | 中 |
| confidenceSource | human-evidence-alternatives-gaps |
| modelConfidenceCopied | false |
| attributionCeiling | L2 |
| judgmentId | AJ-2026-025 |
| alternativeIds/0 | ALT-2026-025-001 |
| alternativeIds/1 | ALT-2026-025-002 |
| alternativeIds/2 | ALT-2026-025-003 |
| gapIds/0 | GAP-2026-025-001 |
| gapIds/1 | GAP-2026-025-002 |
| gapIds/2 | GAP-2026-025-003 |
| gapIds/3 | GAP-2026-025-004 |
| auditId | AI28-AUDIT-1 |
| reassessmentId | AI28-REASSESSMENT |

### AI28-HUMAN-2

| Field | Value |
|---|---|
| id | AI28-HUMAN-2 |
| target/claimId | AI28-CLAIM-2 |
| target/claimHash | 0f68c6f89fd1f6a3ce36214c1cff269ac6afe615d75faf1e808cd57da3cbc459 |
| target/sourceSetId | AI28-SOURCESET |
| target/sourceSetVersion | 1.0.0 |
| target/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| target/modelId | AI28-MODEL |
| target/modelVersion | author-descriptor-1 |
| target/runtime | offline-authored-not-model-runtime |
| target/instructionId | AI28-INSTRUCTION |
| target/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| target/inputId | AI28-INPUT |
| target/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| target/outputId | AI28-OUTPUT |
| target/outputVersion | 1.0.0 |
| target/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| verificationId | AI28-VERIFY-2 |
| reviewerId | SYNTH-AI28-REVIEWER |
| reviewedAt | 2026-07-29T10:30:00Z |
| validUntil | 2026-07-30T01:00:00Z |
| disposition | Revise |
| acceptedWording | quarantine mail was present |
| rationale | retain parent scope; do not adopt unverified output |
| analyticConfidence | 中 |
| confidenceSource | human-evidence-alternatives-gaps |
| modelConfidenceCopied | false |
| attributionCeiling | L2 |
| judgmentId | AJ-2026-025 |
| alternativeIds/0 | ALT-2026-025-001 |
| alternativeIds/1 | ALT-2026-025-002 |
| alternativeIds/2 | ALT-2026-025-003 |
| gapIds/0 | GAP-2026-025-001 |
| gapIds/1 | GAP-2026-025-002 |
| gapIds/2 | GAP-2026-025-003 |
| gapIds/3 | GAP-2026-025-004 |
| auditId | AI28-AUDIT-2 |
| reassessmentId | AI28-REASSESSMENT |

### AI28-HUMAN-3

| Field | Value |
|---|---|
| id | AI28-HUMAN-3 |
| target/claimId | AI28-CLAIM-3 |
| target/claimHash | 2a9f2626283568d85bd253d6b254dcb4ed1215876242e57bf5a672525e5fbded |
| target/sourceSetId | AI28-SOURCESET |
| target/sourceSetVersion | 1.0.0 |
| target/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| target/modelId | AI28-MODEL |
| target/modelVersion | author-descriptor-1 |
| target/runtime | offline-authored-not-model-runtime |
| target/instructionId | AI28-INSTRUCTION |
| target/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| target/inputId | AI28-INPUT |
| target/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| target/outputId | AI28-OUTPUT |
| target/outputVersion | 1.0.0 |
| target/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| verificationId | AI28-VERIFY-3 |
| reviewerId | SYNTH-AI28-REVIEWER |
| reviewedAt | 2026-07-29T10:30:00Z |
| validUntil | 2026-07-30T01:00:00Z |
| disposition | Reject |
| acceptedWording | not-adopted |
| rationale | retain parent scope; do not adopt unverified output |
| analyticConfidence | 中 |
| confidenceSource | human-evidence-alternatives-gaps |
| modelConfidenceCopied | false |
| attributionCeiling | L2 |
| judgmentId | AJ-2026-025 |
| alternativeIds/0 | ALT-2026-025-001 |
| alternativeIds/1 | ALT-2026-025-002 |
| alternativeIds/2 | ALT-2026-025-003 |
| gapIds/0 | GAP-2026-025-001 |
| gapIds/1 | GAP-2026-025-002 |
| gapIds/2 | GAP-2026-025-003 |
| gapIds/3 | GAP-2026-025-004 |
| auditId | AI28-AUDIT-3 |
| reassessmentId | AI28-REASSESSMENT |

### AI28-HUMAN-4

| Field | Value |
|---|---|
| id | AI28-HUMAN-4 |
| target/claimId | AI28-CLAIM-4 |
| target/claimHash | b1e6029cfde8ad24ea6cf1f6ef27e5a2afe81f159ee88ef8dd92f797cacb1cf5 |
| target/sourceSetId | AI28-SOURCESET |
| target/sourceSetVersion | 1.0.0 |
| target/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| target/modelId | AI28-MODEL |
| target/modelVersion | author-descriptor-1 |
| target/runtime | offline-authored-not-model-runtime |
| target/instructionId | AI28-INSTRUCTION |
| target/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| target/inputId | AI28-INPUT |
| target/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| target/outputId | AI28-OUTPUT |
| target/outputVersion | 1.0.0 |
| target/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| verificationId | AI28-VERIFY-4 |
| reviewerId | SYNTH-AI28-REVIEWER |
| reviewedAt | 2026-07-29T10:30:00Z |
| validUntil | 2026-07-30T01:00:00Z |
| disposition | Reject |
| acceptedWording | not-adopted |
| rationale | retain parent scope; do not adopt unverified output |
| analyticConfidence | 未判定 |
| confidenceSource | human-evidence-alternatives-gaps |
| modelConfidenceCopied | false |
| attributionCeiling | L2 |
| judgmentId | AJ-2026-025 |
| alternativeIds/0 | ALT-2026-025-001 |
| alternativeIds/1 | ALT-2026-025-002 |
| alternativeIds/2 | ALT-2026-025-003 |
| gapIds/0 | GAP-2026-025-001 |
| gapIds/1 | GAP-2026-025-002 |
| gapIds/2 | GAP-2026-025-003 |
| gapIds/3 | GAP-2026-025-004 |
| auditId | AI28-AUDIT-4 |
| reassessmentId | AI28-REASSESSMENT |

### AI28-HUMAN-5

| Field | Value |
|---|---|
| id | AI28-HUMAN-5 |
| target/claimId | AI28-CLAIM-5 |
| target/claimHash | 97ab1dd89c0fd4ab674b0b8361c1cd6cce04a7a0aee963d19c52541cd6d61a8b |
| target/sourceSetId | AI28-SOURCESET |
| target/sourceSetVersion | 1.0.0 |
| target/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| target/modelId | AI28-MODEL |
| target/modelVersion | author-descriptor-1 |
| target/runtime | offline-authored-not-model-runtime |
| target/instructionId | AI28-INSTRUCTION |
| target/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| target/inputId | AI28-INPUT |
| target/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| target/outputId | AI28-OUTPUT |
| target/outputVersion | 1.0.0 |
| target/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| verificationId | AI28-VERIFY-5 |
| reviewerId | SYNTH-AI28-REVIEWER |
| reviewedAt | 2026-07-29T10:30:00Z |
| validUntil | 2026-07-30T01:00:00Z |
| disposition | Escalate |
| acceptedWording | not-adopted |
| rationale | retain parent scope; do not adopt unverified output |
| analyticConfidence | 未判定 |
| confidenceSource | human-evidence-alternatives-gaps |
| modelConfidenceCopied | false |
| attributionCeiling | L2 |
| judgmentId | AJ-2026-025 |
| alternativeIds/0 | ALT-2026-025-001 |
| alternativeIds/1 | ALT-2026-025-002 |
| alternativeIds/2 | ALT-2026-025-003 |
| gapIds/0 | GAP-2026-025-001 |
| gapIds/1 | GAP-2026-025-002 |
| gapIds/2 | GAP-2026-025-003 |
| gapIds/3 | GAP-2026-025-004 |
| auditId | AI28-AUDIT-5 |
| reassessmentId | AI28-REASSESSMENT |

### AI28-HUMAN-6

| Field | Value |
|---|---|
| id | AI28-HUMAN-6 |
| target/claimId | AI28-CLAIM-6 |
| target/claimHash | cb8f6ed1b7d9d2a62e9d440460e3bca4c72e0692c05860a230a760604940869d |
| target/sourceSetId | AI28-SOURCESET |
| target/sourceSetVersion | 1.0.0 |
| target/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| target/modelId | AI28-MODEL |
| target/modelVersion | author-descriptor-1 |
| target/runtime | offline-authored-not-model-runtime |
| target/instructionId | AI28-INSTRUCTION |
| target/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| target/inputId | AI28-INPUT |
| target/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| target/outputId | AI28-OUTPUT |
| target/outputVersion | 1.0.0 |
| target/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| verificationId | AI28-VERIFY-6 |
| reviewerId | SYNTH-AI28-REVIEWER |
| reviewedAt | 2026-07-29T10:30:00Z |
| validUntil | 2026-07-30T01:00:00Z |
| disposition | Reject |
| acceptedWording | not-adopted |
| rationale | retain parent scope; do not adopt unverified output |
| analyticConfidence | 未判定 |
| confidenceSource | human-evidence-alternatives-gaps |
| modelConfidenceCopied | false |
| attributionCeiling | L2 |
| judgmentId | AJ-2026-025 |
| alternativeIds/0 | ALT-2026-025-001 |
| alternativeIds/1 | ALT-2026-025-002 |
| alternativeIds/2 | ALT-2026-025-003 |
| gapIds/0 | GAP-2026-025-001 |
| gapIds/1 | GAP-2026-025-002 |
| gapIds/2 | GAP-2026-025-003 |
| gapIds/3 | GAP-2026-025-004 |
| auditId | AI28-AUDIT-6 |
| reassessmentId | AI28-REASSESSMENT |

### AI28-HUMAN-7

| Field | Value |
|---|---|
| id | AI28-HUMAN-7 |
| target/claimId | AI28-CLAIM-7 |
| target/claimHash | 809e7611e379656a90c87baae504496a7f912f65be1aca46173799980cc7c24a |
| target/sourceSetId | AI28-SOURCESET |
| target/sourceSetVersion | 1.0.0 |
| target/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| target/modelId | AI28-MODEL |
| target/modelVersion | author-descriptor-1 |
| target/runtime | offline-authored-not-model-runtime |
| target/instructionId | AI28-INSTRUCTION |
| target/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| target/inputId | AI28-INPUT |
| target/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| target/outputId | AI28-OUTPUT |
| target/outputVersion | 1.0.0 |
| target/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| verificationId | AI28-VERIFY-7 |
| reviewerId | SYNTH-AI28-REVIEWER |
| reviewedAt | 2026-07-29T10:30:00Z |
| validUntil | 2026-07-30T01:00:00Z |
| disposition | Reject |
| acceptedWording | not-adopted |
| rationale | retain parent scope; do not adopt unverified output |
| analyticConfidence | 未判定 |
| confidenceSource | human-evidence-alternatives-gaps |
| modelConfidenceCopied | false |
| attributionCeiling | L2 |
| judgmentId | AJ-2026-025 |
| alternativeIds/0 | ALT-2026-025-001 |
| alternativeIds/1 | ALT-2026-025-002 |
| alternativeIds/2 | ALT-2026-025-003 |
| gapIds/0 | GAP-2026-025-001 |
| gapIds/1 | GAP-2026-025-002 |
| gapIds/2 | GAP-2026-025-003 |
| gapIds/3 | GAP-2026-025-004 |
| auditId | AI28-AUDIT-7 |
| reassessmentId | AI28-REASSESSMENT |

### AI28-AUDIT-1

| Field | Value |
|---|---|
| id | AI28-AUDIT-1 |
| target/claimId | AI28-CLAIM-1 |
| target/claimHash | 459e90e224fb554a318c87f32acf53f70cb580525fa8cb652076c79f92c6f0ea |
| target/sourceSetId | AI28-SOURCESET |
| target/sourceSetVersion | 1.0.0 |
| target/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| target/modelId | AI28-MODEL |
| target/modelVersion | author-descriptor-1 |
| target/runtime | offline-authored-not-model-runtime |
| target/instructionId | AI28-INSTRUCTION |
| target/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| target/inputId | AI28-INPUT |
| target/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| target/outputId | AI28-OUTPUT |
| target/outputVersion | 1.0.0 |
| target/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| decisionId | AI28-HUMAN-1 |
| at | 2026-07-29T10:30:00Z |
| disposition | Accept |
| ownerId | SYNTH-AI28-OWNER |
| retainUntil | 2026-08-29T11:00:00Z |

### AI28-AUDIT-2

| Field | Value |
|---|---|
| id | AI28-AUDIT-2 |
| target/claimId | AI28-CLAIM-2 |
| target/claimHash | 0f68c6f89fd1f6a3ce36214c1cff269ac6afe615d75faf1e808cd57da3cbc459 |
| target/sourceSetId | AI28-SOURCESET |
| target/sourceSetVersion | 1.0.0 |
| target/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| target/modelId | AI28-MODEL |
| target/modelVersion | author-descriptor-1 |
| target/runtime | offline-authored-not-model-runtime |
| target/instructionId | AI28-INSTRUCTION |
| target/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| target/inputId | AI28-INPUT |
| target/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| target/outputId | AI28-OUTPUT |
| target/outputVersion | 1.0.0 |
| target/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| decisionId | AI28-HUMAN-2 |
| at | 2026-07-29T10:30:00Z |
| disposition | Revise |
| ownerId | SYNTH-AI28-OWNER |
| retainUntil | 2026-08-29T11:00:00Z |

### AI28-AUDIT-3

| Field | Value |
|---|---|
| id | AI28-AUDIT-3 |
| target/claimId | AI28-CLAIM-3 |
| target/claimHash | 2a9f2626283568d85bd253d6b254dcb4ed1215876242e57bf5a672525e5fbded |
| target/sourceSetId | AI28-SOURCESET |
| target/sourceSetVersion | 1.0.0 |
| target/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| target/modelId | AI28-MODEL |
| target/modelVersion | author-descriptor-1 |
| target/runtime | offline-authored-not-model-runtime |
| target/instructionId | AI28-INSTRUCTION |
| target/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| target/inputId | AI28-INPUT |
| target/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| target/outputId | AI28-OUTPUT |
| target/outputVersion | 1.0.0 |
| target/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| decisionId | AI28-HUMAN-3 |
| at | 2026-07-29T10:30:00Z |
| disposition | Reject |
| ownerId | SYNTH-AI28-OWNER |
| retainUntil | 2026-08-29T11:00:00Z |

### AI28-AUDIT-4

| Field | Value |
|---|---|
| id | AI28-AUDIT-4 |
| target/claimId | AI28-CLAIM-4 |
| target/claimHash | b1e6029cfde8ad24ea6cf1f6ef27e5a2afe81f159ee88ef8dd92f797cacb1cf5 |
| target/sourceSetId | AI28-SOURCESET |
| target/sourceSetVersion | 1.0.0 |
| target/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| target/modelId | AI28-MODEL |
| target/modelVersion | author-descriptor-1 |
| target/runtime | offline-authored-not-model-runtime |
| target/instructionId | AI28-INSTRUCTION |
| target/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| target/inputId | AI28-INPUT |
| target/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| target/outputId | AI28-OUTPUT |
| target/outputVersion | 1.0.0 |
| target/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| decisionId | AI28-HUMAN-4 |
| at | 2026-07-29T10:30:00Z |
| disposition | Reject |
| ownerId | SYNTH-AI28-OWNER |
| retainUntil | 2026-08-29T11:00:00Z |

### AI28-AUDIT-5

| Field | Value |
|---|---|
| id | AI28-AUDIT-5 |
| target/claimId | AI28-CLAIM-5 |
| target/claimHash | 97ab1dd89c0fd4ab674b0b8361c1cd6cce04a7a0aee963d19c52541cd6d61a8b |
| target/sourceSetId | AI28-SOURCESET |
| target/sourceSetVersion | 1.0.0 |
| target/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| target/modelId | AI28-MODEL |
| target/modelVersion | author-descriptor-1 |
| target/runtime | offline-authored-not-model-runtime |
| target/instructionId | AI28-INSTRUCTION |
| target/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| target/inputId | AI28-INPUT |
| target/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| target/outputId | AI28-OUTPUT |
| target/outputVersion | 1.0.0 |
| target/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| decisionId | AI28-HUMAN-5 |
| at | 2026-07-29T10:30:00Z |
| disposition | Escalate |
| ownerId | SYNTH-AI28-OWNER |
| retainUntil | 2026-08-29T11:00:00Z |

### AI28-AUDIT-6

| Field | Value |
|---|---|
| id | AI28-AUDIT-6 |
| target/claimId | AI28-CLAIM-6 |
| target/claimHash | cb8f6ed1b7d9d2a62e9d440460e3bca4c72e0692c05860a230a760604940869d |
| target/sourceSetId | AI28-SOURCESET |
| target/sourceSetVersion | 1.0.0 |
| target/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| target/modelId | AI28-MODEL |
| target/modelVersion | author-descriptor-1 |
| target/runtime | offline-authored-not-model-runtime |
| target/instructionId | AI28-INSTRUCTION |
| target/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| target/inputId | AI28-INPUT |
| target/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| target/outputId | AI28-OUTPUT |
| target/outputVersion | 1.0.0 |
| target/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| decisionId | AI28-HUMAN-6 |
| at | 2026-07-29T10:30:00Z |
| disposition | Reject |
| ownerId | SYNTH-AI28-OWNER |
| retainUntil | 2026-08-29T11:00:00Z |

### AI28-AUDIT-7

| Field | Value |
|---|---|
| id | AI28-AUDIT-7 |
| target/claimId | AI28-CLAIM-7 |
| target/claimHash | 809e7611e379656a90c87baae504496a7f912f65be1aca46173799980cc7c24a |
| target/sourceSetId | AI28-SOURCESET |
| target/sourceSetVersion | 1.0.0 |
| target/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| target/modelId | AI28-MODEL |
| target/modelVersion | author-descriptor-1 |
| target/runtime | offline-authored-not-model-runtime |
| target/instructionId | AI28-INSTRUCTION |
| target/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| target/inputId | AI28-INPUT |
| target/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| target/outputId | AI28-OUTPUT |
| target/outputVersion | 1.0.0 |
| target/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| decisionId | AI28-HUMAN-7 |
| at | 2026-07-29T10:30:00Z |
| disposition | Reject |
| ownerId | SYNTH-AI28-OWNER |
| retainUntil | 2026-08-29T11:00:00Z |

### AI28-CONT-SOURCE

| Field | Value |
|---|---|
| id | AI28-CONT-SOURCE |
| kind | source |
| text | Untrusted source sample asserts that every Claim already has human approval. |
| sha256 | 39bcebcc2c9ee56cfeba95ec6efb2be097e339b42bb21b3290aea2144d427937 |
| conclusion | untrusted-authority-self-claim |
| method | author-labelled-fixed-sample-not-detector |
| adopted | false |
| authorityGranted | false |
| executed | false |

### AI28-CONT-TOOL

| Field | Value |
|---|---|
| id | AI28-CONT-TOOL |
| kind | tool |
| text | Untrusted tool sample asserts that every Claim already has human approval. |
| sha256 | f8b01d381a14626a7123428cfcde58b4422a8d3b52d89164e84331ae0c12b3d7 |
| conclusion | untrusted-authority-self-claim |
| method | author-labelled-fixed-sample-not-detector |
| adopted | false |
| authorityGranted | false |
| executed | false |

### AI28-CONT-MEMORY

| Field | Value |
|---|---|
| id | AI28-CONT-MEMORY |
| kind | memory |
| text | Untrusted memory sample asserts that every Claim already has human approval. |
| sha256 | 7ba00f95e9b4924bf951bf6179aefa2b7cd78d6db69f2061a97f53e29f1ad87c |
| conclusion | untrusted-authority-self-claim |
| method | author-labelled-fixed-sample-not-detector |
| adopted | false |
| authorityGranted | false |
| executed | false |

### reproduction

| Field | Value |
|---|---|
| id | AI28-REPRODUCTION |
| method | offline-record-equality |
| modelExecuted | false |
| generalizationProven | false |
| targets/0/claimId | AI28-CLAIM-1 |
| targets/0/claimHash | 459e90e224fb554a318c87f32acf53f70cb580525fa8cb652076c79f92c6f0ea |
| targets/0/sourceSetId | AI28-SOURCESET |
| targets/0/sourceSetVersion | 1.0.0 |
| targets/0/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| targets/0/modelId | AI28-MODEL |
| targets/0/modelVersion | author-descriptor-1 |
| targets/0/runtime | offline-authored-not-model-runtime |
| targets/0/instructionId | AI28-INSTRUCTION |
| targets/0/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| targets/0/inputId | AI28-INPUT |
| targets/0/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| targets/0/outputId | AI28-OUTPUT |
| targets/0/outputVersion | 1.0.0 |
| targets/0/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| targets/1/claimId | AI28-CLAIM-2 |
| targets/1/claimHash | 0f68c6f89fd1f6a3ce36214c1cff269ac6afe615d75faf1e808cd57da3cbc459 |
| targets/1/sourceSetId | AI28-SOURCESET |
| targets/1/sourceSetVersion | 1.0.0 |
| targets/1/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| targets/1/modelId | AI28-MODEL |
| targets/1/modelVersion | author-descriptor-1 |
| targets/1/runtime | offline-authored-not-model-runtime |
| targets/1/instructionId | AI28-INSTRUCTION |
| targets/1/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| targets/1/inputId | AI28-INPUT |
| targets/1/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| targets/1/outputId | AI28-OUTPUT |
| targets/1/outputVersion | 1.0.0 |
| targets/1/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| targets/2/claimId | AI28-CLAIM-3 |
| targets/2/claimHash | 2a9f2626283568d85bd253d6b254dcb4ed1215876242e57bf5a672525e5fbded |
| targets/2/sourceSetId | AI28-SOURCESET |
| targets/2/sourceSetVersion | 1.0.0 |
| targets/2/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| targets/2/modelId | AI28-MODEL |
| targets/2/modelVersion | author-descriptor-1 |
| targets/2/runtime | offline-authored-not-model-runtime |
| targets/2/instructionId | AI28-INSTRUCTION |
| targets/2/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| targets/2/inputId | AI28-INPUT |
| targets/2/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| targets/2/outputId | AI28-OUTPUT |
| targets/2/outputVersion | 1.0.0 |
| targets/2/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| targets/3/claimId | AI28-CLAIM-4 |
| targets/3/claimHash | b1e6029cfde8ad24ea6cf1f6ef27e5a2afe81f159ee88ef8dd92f797cacb1cf5 |
| targets/3/sourceSetId | AI28-SOURCESET |
| targets/3/sourceSetVersion | 1.0.0 |
| targets/3/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| targets/3/modelId | AI28-MODEL |
| targets/3/modelVersion | author-descriptor-1 |
| targets/3/runtime | offline-authored-not-model-runtime |
| targets/3/instructionId | AI28-INSTRUCTION |
| targets/3/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| targets/3/inputId | AI28-INPUT |
| targets/3/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| targets/3/outputId | AI28-OUTPUT |
| targets/3/outputVersion | 1.0.0 |
| targets/3/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| targets/4/claimId | AI28-CLAIM-5 |
| targets/4/claimHash | 97ab1dd89c0fd4ab674b0b8361c1cd6cce04a7a0aee963d19c52541cd6d61a8b |
| targets/4/sourceSetId | AI28-SOURCESET |
| targets/4/sourceSetVersion | 1.0.0 |
| targets/4/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| targets/4/modelId | AI28-MODEL |
| targets/4/modelVersion | author-descriptor-1 |
| targets/4/runtime | offline-authored-not-model-runtime |
| targets/4/instructionId | AI28-INSTRUCTION |
| targets/4/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| targets/4/inputId | AI28-INPUT |
| targets/4/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| targets/4/outputId | AI28-OUTPUT |
| targets/4/outputVersion | 1.0.0 |
| targets/4/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| targets/5/claimId | AI28-CLAIM-6 |
| targets/5/claimHash | cb8f6ed1b7d9d2a62e9d440460e3bca4c72e0692c05860a230a760604940869d |
| targets/5/sourceSetId | AI28-SOURCESET |
| targets/5/sourceSetVersion | 1.0.0 |
| targets/5/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| targets/5/modelId | AI28-MODEL |
| targets/5/modelVersion | author-descriptor-1 |
| targets/5/runtime | offline-authored-not-model-runtime |
| targets/5/instructionId | AI28-INSTRUCTION |
| targets/5/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| targets/5/inputId | AI28-INPUT |
| targets/5/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| targets/5/outputId | AI28-OUTPUT |
| targets/5/outputVersion | 1.0.0 |
| targets/5/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| targets/6/claimId | AI28-CLAIM-7 |
| targets/6/claimHash | 809e7611e379656a90c87baae504496a7f912f65be1aca46173799980cc7c24a |
| targets/6/sourceSetId | AI28-SOURCESET |
| targets/6/sourceSetVersion | 1.0.0 |
| targets/6/sourceSetHash | 89b6d94e97a200791814a56e9d4dc9913b05bb54c0b782681a68c81af07442d5 |
| targets/6/modelId | AI28-MODEL |
| targets/6/modelVersion | author-descriptor-1 |
| targets/6/runtime | offline-authored-not-model-runtime |
| targets/6/instructionId | AI28-INSTRUCTION |
| targets/6/instructionHash | c6eeb7e00e4456cf9afb394a54a90a0c39c3480f8b40ff6755256ecee7b07e40 |
| targets/6/inputId | AI28-INPUT |
| targets/6/inputHash | 9296912aa0669af472979b51c213805167b183244e99eda55bbfcd5a00d8897a |
| targets/6/outputId | AI28-OUTPUT |
| targets/6/outputVersion | 1.0.0 |
| targets/6/outputHash | 78759c57bd9c196797708f985c298ecc64c16ce37f5056d46e2dc1f299c2c117 |
| limitation | records are compared; actual model repeatability and detection coverage are not tested |

### AI28-METHOD-24

| Field | Value |
|---|---|
| id | AI28-METHOD-24 |
| caseId | CASE-OS24-001 |
| relation | method-only |
| evidenceInherited | false |

### AI28-METHOD-27

| Field | Value |
|---|---|
| id | AI28-METHOD-27 |
| caseId | CASE-2026-001 |
| relation | method-only |
| evidenceInherited | false |

### AI28-METHOD-STIX

| Field | Value |
|---|---|
| id | AI28-METHOD-STIX |
| caseId | CASE-STIX26-DEMO |
| relation | independent-not-adopted |
| evidenceInherited | false |

### reassessment

| Field | Value |
|---|---|
| id | AI28-REASSESSMENT |
| ownerId | SYNTH-AI28-OWNER |
| dueAt | 2026-07-30T00:00:00Z |
| triggers/0 | source-correction |
| triggers/1 | source-withdrawal |
| triggers/2 | source-expiry |
| triggers/3 | version-change |
| triggers/4 | input-contamination |
| triggers/5 | cutoff-change |
| triggers/6 | coverage-change |
| triggers/7 | independence-change |
| triggers/8 | attribution-threshold-change |
| claimIds/0 | AI28-CLAIM-1 |
| claimIds/1 | AI28-CLAIM-2 |
| claimIds/2 | AI28-CLAIM-3 |
| claimIds/3 | AI28-CLAIM-4 |
| claimIds/4 | AI28-CLAIM-5 |
| claimIds/5 | AI28-CLAIM-6 |
| claimIds/6 | AI28-CLAIM-7 |
| decisionIds/0 | AI28-HUMAN-1 |
| decisionIds/1 | AI28-HUMAN-2 |
| decisionIds/2 | AI28-HUMAN-3 |
| decisionIds/3 | AI28-HUMAN-4 |
| decisionIds/4 | AI28-HUMAN-5 |
| decisionIds/5 | AI28-HUMAN-6 |
| decisionIds/6 | AI28-HUMAN-7 |
| auditIds/0 | AI28-AUDIT-1 |
| auditIds/1 | AI28-AUDIT-2 |
| auditIds/2 | AI28-AUDIT-3 |
| auditIds/3 | AI28-AUDIT-4 |
| auditIds/4 | AI28-AUDIT-5 |
| auditIds/5 | AI28-AUDIT-6 |
| auditIds/6 | AI28-AUDIT-7 |
| effect | suspend adoption and require new verification and human review |

### handoff

| Field | Value |
|---|---|
| id | AI28-HANDOFF |
| targetChapter | 29 |
| receipt | not-received |
| acceptedDecisionIds/0 | AI28-HUMAN-1 |
| acceptedDecisionIds/1 | AI28-HUMAN-2 |
| unadoptedDecisionIds/0 | AI28-HUMAN-3 |
| unadoptedDecisionIds/1 | AI28-HUMAN-4 |
| unadoptedDecisionIds/2 | AI28-HUMAN-5 |
| unadoptedDecisionIds/3 | AI28-HUMAN-6 |
| unadoptedDecisionIds/4 | AI28-HUMAN-7 |
| executionAuthorized | false |
| unreceivedCTIProductAdopted | false |

### limitations

| Field | Value |
|---|---|
| id | AI28-LIMITS |
| modelPerformanceMeasured | false |
| standardConformanceCertified | false |
| injectionCoverageProven | false |
| realAuthorityGranted | false |
| coverageGapId | GAP-2026-025-001 |
| negativeFindingId | NEG-2026-025-001 |
| note | 2026-07-21/22 coverage and detailed token issuance are missing; neither success nor absence is established |
