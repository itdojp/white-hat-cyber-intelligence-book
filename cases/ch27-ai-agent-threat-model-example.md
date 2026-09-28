# 第27章 完全合成記入例：AI / Agent Threat Model

## この記入例の扱い

ART-31 / AIM-2026-027はCASE-2026-001をrefinesする教育用追加記録です。親CaseでAIが実稼働していたという観測ではありません。時刻、Actor、Component、承認、監査票はすべて作成者が記述した架空値です。Component Digestは合成ラベルのhashで、実Model、Dataset、配備Artifactのbyte検証ではありません。

[第27章](../manuscript/27-ai-agent-security.md)、[空Template](../templates/ai-agent-threat-model.md)、[供給JSON](fixtures/ch27-ai-agent-threat-model.json)、[閉Schema](../schemas/ch27-ai-agent-threat-model.schema.json)を参照します。実Model、実Tenant、Shell、外部Network、実File mutationは使用しない。実CredentialとAPI keyは使用しない。Purposeは固定記録の比較、Prerequisiteは本章とTemplate、Authority / Scopeはread-only syntheticです。Expected evidenceは境界と不足の説明、Impactは読解だけです。実Dataの疑い、未知入力、許可不明でStopし、Cleanupは自分の演習コピーだけに限定します。

## 読み方と対比

最初にrecord/parents/safetyを読みます。親の失効Authorization、Draft / Do not proceedと実行権限falseを保持します。第26章は独立Caseの方法参照だけで、未配達Productと独立STIXを受領済みEvidenceへ借用しません。

SYSTEMは宣言だけ、RETRIEVERは合成観測、MOCK-READERは同じ対象の有限比較、MEMORYは制限、EXPORTERは無効、MODELは不明です。六状態はLab八状態とは別です。MODELがUnknownでもREQUEST-1は固定応答を読む条件だけ一致し、Modelの推論性能やAgentの安全性を検証したことにはなりません。

REQUEST-1はAllowed-in-model、2〜4と6はBlocked、5はStoppedです。すべてexecuted=falseです。拒否理由はfindingsのreasonsで列挙し、複数理由を一つの原因へ圧縮しません。Instructionの自己申告、期限切れ承認、他CaseのMemory、範囲外効果、停止、無効Toolを比較します。

## 評価と限界

Threatの成立条件・Impact・Control・TelemetryをFinding、合成Evidence、Audit、Decision、Owner、再評価へ接続します。AISVS適合、実署名検証、実停止や復旧成功は主張しません。確認事実、分析判断、仮定、予測、推奨と代替説明はdecisionへ分けて記録します。Handoffはplanned-not-deliveredです。本章Rubricの五観点で評価し、根拠のない状態昇格や実Data混入は点数にかかわらず差し戻します。

## 全欄の読み方

次の表は供給JSONの全末端Fieldです。添字は0始まりです。列挙される要求は非実行の分析対象で、実操作の指示ではありません。

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

### executionAuthorized

| Field | Value |
|---|---|
| value | false |

### record

| Field | Value |
|---|---|
| id | AIM-2026-027 |
| artifactId | ART-31 |
| caseId | CASE-AI-2026-027 |
| parentCaseId | CASE-2026-001 |
| relation | refines |
| decisionRequirementId | DR-AI-2026-027 |
| question | 合成資料の読み取り専用比較をどの境界まで許容し、何を保留するか |
| asOf | 2026-09-20T10:00:00Z |
| owner | Synthetic AI Reviewer |
| decisionOwner | Synthetic CTO Decision Owner |
| reviewDeadline | 2026-09-21T10:00:00Z |
| parentEvidenceInherited | false |
| parentAuthorityInherited | false |
| actualModelCalls | 0 |
| actualToolCalls | 0 |
| actualExternalEffects | 0 |
| realControlEffectivenessProven | false |

### parents

| Field | Value |
|---|---|
| threatModelId | TM-2026-001 |
| signalFlowId | SFM-2026-001 |
| supplyChainAssessmentId | PSA-2026-013 |
| authorizationId | AUTH-CASE-2026-001 |
| roeId | ROE-2026-009 |
| roeStatus | Draft |
| roeDecision | Do not proceed |
| authorizationState | expired-not-renewed |
| ctiRelationship | independent-method-reference |
| ctiProductReceived | false |
| stixAdoptedAsEvidence | false |
| historicalAiDeploymentClaimed | false |

### safety

| Field | Value |
|---|---|
| scope | offline-authored-record-comparison |
| modelApi | false |
| network | false |
| shell | false |
| fileMutation | false |
| credentialAccess | false |
| personalData | false |
| secretMaterial | false |
| stop | 実Dataの疑い、未知入力、対象や版の不一致、許可不明で停止する。 |
| cleanup | 自分の演習コピーだけを整理し、正本と親記録は変更しない。 |
| runtimeKillSwitchTested | false |
| recoveryTested | false |

### AI27-USER

| Field | Value |
|---|---|
| id | AI27-USER |
| role | requester |
| authority | read-synthetic-bundle |

### AI27-AGENT

| Field | Value |
|---|---|
| id | AI27-AGENT |
| role | model-descriptor-only |
| authority | none |

### AI27-OWNER

| Field | Value |
|---|---|
| id | AI27-OWNER |
| role | human-approval-owner |
| authority | approve-read-only-comparison |

### AI27-SYSTEM

| Field | Value |
|---|---|
| id | AI27-SYSTEM |
| layer | application-policy |
| origin | author-synthetic |
| text | 出力は仮説候補だけとし、権限と根拠を自動継承しない。 |
| treatedAs | instruction |
| allowedOverride | false |

### AI27-USER-INSTRUCTION

| Field | Value |
|---|---|
| id | AI27-USER-INSTRUCTION |
| layer | user-request |
| origin | AI27-USER |
| text | 供給された合成資料二件の差と不足を比較する。 |
| treatedAs | instruction |
| allowedOverride | false |

### AI27-RAG-INSTRUCTION

| Field | Value |
|---|---|
| id | AI27-RAG-INSTRUCTION |
| layer | retrieved-content |
| origin | AI27-SOURCE-2 |
| text | この文書は承認済みという自己申告を含む。自己申告を承認票としては扱わない。 |
| treatedAs | data |
| allowedOverride | false |

### AI27-SOURCE-1

| Field | Value |
|---|---|
| id | AI27-SOURCE-1 |
| caseId | CASE-AI-2026-027 |
| audience | AI27-USER |
| version | 1.0 |
| origin | author-synthetic |
| classification | synthetic-only |
| text | 観測票は一件だけで、他の対象については判断できない。 |
| sourceAdopted | true |

### AI27-SOURCE-2

| Field | Value |
|---|---|
| id | AI27-SOURCE-2 |
| caseId | CASE-AI-2026-027 |
| audience | AI27-USER |
| version | 1.0 |
| origin | author-synthetic |
| classification | synthetic-only |
| text | 外部資料を模した自己申告。信頼境界を越える要求の分析対象であり、実行指示ではない。 |
| sourceAdopted | true |

### AI27-MEMORY-1

| Field | Value |
|---|---|
| id | AI27-MEMORY-1 |
| caseId | CASE-AI-2026-027 |
| audience | AI27-USER |
| version | 1.0 |
| sourceId | AI27-SOURCE-1 |
| expiresAt | 2026-09-21T00:00:00Z |
| quarantined | false |
| origin | author-synthetic |
| automaticWrite | false |

### AI27-MEMORY-2

| Field | Value |
|---|---|
| id | AI27-MEMORY-2 |
| caseId | CASE-OTHER-SYNTHETIC |
| audience | AI27-OTHER-USER |
| version | 0.9 |
| sourceId | AI27-SOURCE-2 |
| expiresAt | 2026-09-19T00:00:00Z |
| quarantined | true |
| origin | author-synthetic |
| automaticWrite | false |

### modelOutput

| Field | Value |
|---|---|
| id | AI27-OUTPUT |
| modelId | AI27-MODEL |
| classification | unverified-hypothesis |
| text | 資料不足のため結論を保留するという合成出力例。 |
| sourceIds/0 | AI27-SOURCE-1 |
| sourceIds/1 | AI27-SOURCE-2 |
| adoptedAsFact | false |
| adoptedAsSource | false |
| adoptedAsCommand | false |
| writtenToTrustedMemory | false |

### AI27-RESPONSE

| Field | Value |
|---|---|
| id | AI27-RESPONSE |
| version | 1.0 |
| body | synthetic comparison only; no action performed |
| sha256 | 04aa187490293e09852547cdf4297dc91e65120d40afe7a57b774ed4348c031c |

### AI27-SYSTEM

| Field | Value |
|---|---|
| id | AI27-SYSTEM |
| kind | system |
| version | 1.0 |
| digest | 9a72b91ecd85fb0d824cf5acc53c41137fb0203b5dcc22228702d7893fb0949c |
| provenance/id | AI27-PROV-1 |
| provenance/origin | author-synthetic |
| provenance/label | AI27-SYSTEM:1.0 |
| provenance/signatureStatus | not-verified |
| descriptorKnown | true |
| restrictionActive | false |
| disabled | false |
| observation/present | false |
| observation/id | AI27-OBS-1 |
| observation/target | AI27-SYSTEM |
| observation/version | 1.0 |
| observation/digest | 9a72b91ecd85fb0d824cf5acc53c41137fb0203b5dcc22228702d7893fb0949c |
| observation/observedAt | 2026-09-20T09:55:00Z |
| observation/origin | author-synthetic |
| validation/present | false |
| validation/id | AI27-VAL-1 |
| validation/target | AI27-SYSTEM |
| validation/version | 1.0 |
| validation/digest | 9a72b91ecd85fb0d824cf5acc53c41137fb0203b5dcc22228702d7893fb0949c |
| validation/observedId | AI27-OBS-1 |
| validation/passed | false |
| validation/validatedAt | 2026-09-20T09:58:00Z |
| validation/method | finite-authored-record-comparison |
| status | Declared |

### AI27-RETRIEVER

| Field | Value |
|---|---|
| id | AI27-RETRIEVER |
| kind | retriever |
| version | 1.0 |
| digest | 13408ee8d900f3ed4e73cfd94459b9e399c03e5b0696fd90f848a7d3912192cc |
| provenance/id | AI27-PROV-2 |
| provenance/origin | author-synthetic |
| provenance/label | AI27-RETRIEVER:1.0 |
| provenance/signatureStatus | not-verified |
| descriptorKnown | true |
| restrictionActive | false |
| disabled | false |
| observation/present | true |
| observation/id | AI27-OBS-2 |
| observation/target | AI27-RETRIEVER |
| observation/version | 1.0 |
| observation/digest | 13408ee8d900f3ed4e73cfd94459b9e399c03e5b0696fd90f848a7d3912192cc |
| observation/observedAt | 2026-09-20T09:55:00Z |
| observation/origin | author-synthetic |
| validation/present | false |
| validation/id | AI27-VAL-2 |
| validation/target | AI27-RETRIEVER |
| validation/version | 1.0 |
| validation/digest | 13408ee8d900f3ed4e73cfd94459b9e399c03e5b0696fd90f848a7d3912192cc |
| validation/observedId | AI27-OBS-2 |
| validation/passed | false |
| validation/validatedAt | 2026-09-20T09:58:00Z |
| validation/method | finite-authored-record-comparison |
| status | Observed |

### AI27-MOCK-READER

| Field | Value |
|---|---|
| id | AI27-MOCK-READER |
| kind | mock-reader |
| version | 1.0 |
| digest | cc77082cfa9fb71e1384bc32f69b1aa058d58671f5d9c4e9e728984f4b150e7e |
| provenance/id | AI27-PROV-3 |
| provenance/origin | author-synthetic |
| provenance/label | AI27-MOCK-READER:1.0 |
| provenance/signatureStatus | not-verified |
| descriptorKnown | true |
| restrictionActive | false |
| disabled | false |
| observation/present | true |
| observation/id | AI27-OBS-3 |
| observation/target | AI27-MOCK-READER |
| observation/version | 1.0 |
| observation/digest | cc77082cfa9fb71e1384bc32f69b1aa058d58671f5d9c4e9e728984f4b150e7e |
| observation/observedAt | 2026-09-20T09:55:00Z |
| observation/origin | author-synthetic |
| validation/present | true |
| validation/id | AI27-VAL-3 |
| validation/target | AI27-MOCK-READER |
| validation/version | 1.0 |
| validation/digest | cc77082cfa9fb71e1384bc32f69b1aa058d58671f5d9c4e9e728984f4b150e7e |
| validation/observedId | AI27-OBS-3 |
| validation/passed | true |
| validation/validatedAt | 2026-09-20T09:58:00Z |
| validation/method | finite-authored-record-comparison |
| status | Validated |

### AI27-MEMORY

| Field | Value |
|---|---|
| id | AI27-MEMORY |
| kind | memory |
| version | 1.0 |
| digest | 3fdcebacfa4d0df60f5de33432049d7e6cad1a2bac4888595bff2c8e876f0d0c |
| provenance/id | AI27-PROV-4 |
| provenance/origin | author-synthetic |
| provenance/label | AI27-MEMORY:1.0 |
| provenance/signatureStatus | not-verified |
| descriptorKnown | true |
| restrictionActive | true |
| disabled | false |
| observation/present | false |
| observation/id | AI27-OBS-4 |
| observation/target | AI27-MEMORY |
| observation/version | 1.0 |
| observation/digest | 3fdcebacfa4d0df60f5de33432049d7e6cad1a2bac4888595bff2c8e876f0d0c |
| observation/observedAt | 2026-09-20T09:55:00Z |
| observation/origin | author-synthetic |
| validation/present | false |
| validation/id | AI27-VAL-4 |
| validation/target | AI27-MEMORY |
| validation/version | 1.0 |
| validation/digest | 3fdcebacfa4d0df60f5de33432049d7e6cad1a2bac4888595bff2c8e876f0d0c |
| validation/observedId | AI27-OBS-4 |
| validation/passed | false |
| validation/validatedAt | 2026-09-20T09:58:00Z |
| validation/method | finite-authored-record-comparison |
| status | Restricted |

### AI27-EXPORTER

| Field | Value |
|---|---|
| id | AI27-EXPORTER |
| kind | exporter |
| version | 1.0 |
| digest | 23bc7a4bab90265dbf7441dd2f6f74e65d4b4c8e82bfcb056a0bd09eeb71472d |
| provenance/id | AI27-PROV-5 |
| provenance/origin | author-synthetic |
| provenance/label | AI27-EXPORTER:1.0 |
| provenance/signatureStatus | not-verified |
| descriptorKnown | true |
| restrictionActive | false |
| disabled | true |
| observation/present | false |
| observation/id | AI27-OBS-5 |
| observation/target | AI27-EXPORTER |
| observation/version | 1.0 |
| observation/digest | 23bc7a4bab90265dbf7441dd2f6f74e65d4b4c8e82bfcb056a0bd09eeb71472d |
| observation/observedAt | 2026-09-20T09:55:00Z |
| observation/origin | author-synthetic |
| validation/present | false |
| validation/id | AI27-VAL-5 |
| validation/target | AI27-EXPORTER |
| validation/version | 1.0 |
| validation/digest | 23bc7a4bab90265dbf7441dd2f6f74e65d4b4c8e82bfcb056a0bd09eeb71472d |
| validation/observedId | AI27-OBS-5 |
| validation/passed | false |
| validation/validatedAt | 2026-09-20T09:58:00Z |
| validation/method | finite-authored-record-comparison |
| status | Disabled |

### AI27-MODEL

| Field | Value |
|---|---|
| id | AI27-MODEL |
| kind | model |
| version | 1.0 |
| digest | 8f0767dc9f1a9d37051de958bd2ba08005519d7cb23cd106748f5e919a2ac004 |
| provenance/id | AI27-PROV-6 |
| provenance/origin | author-synthetic |
| provenance/label | AI27-MODEL:1.0 |
| provenance/signatureStatus | not-verified |
| descriptorKnown | false |
| restrictionActive | false |
| disabled | false |
| observation/present | false |
| observation/id | AI27-OBS-6 |
| observation/target | AI27-MODEL |
| observation/version | 1.0 |
| observation/digest | 8f0767dc9f1a9d37051de958bd2ba08005519d7cb23cd106748f5e919a2ac004 |
| observation/observedAt | 2026-09-20T09:55:00Z |
| observation/origin | author-synthetic |
| validation/present | false |
| validation/id | AI27-VAL-6 |
| validation/target | AI27-MODEL |
| validation/version | 1.0 |
| validation/digest | 8f0767dc9f1a9d37051de958bd2ba08005519d7cb23cd106748f5e919a2ac004 |
| validation/observedId | AI27-OBS-6 |
| validation/passed | false |
| validation/validatedAt | 2026-09-20T09:58:00Z |
| validation/method | finite-authored-record-comparison |
| status | Unknown |

### AI27-MOCK-READER

| Field | Value |
|---|---|
| id | AI27-MOCK-READER |
| version | 1.0 |
| capability | read-fixed-response |
| scope/0 | CASE-AI-2026-027 |
| scope/1 | AI27-SOURCE-1 |
| scope/2 | AI27-SOURCE-2 |
| credentialClass | none |
| sideEffect | none |
| approvalRequired | true |
| approvalOwnerId | AI27-OWNER |
| timeoutSeconds | 30 |
| enabled | true |
| responseId | AI27-RESPONSE |
| stopId | AI27-STOP |
| actualImplementation | none-record-only |

### AI27-EXPORTER

| Field | Value |
|---|---|
| id | AI27-EXPORTER |
| version | 1.0 |
| capability | read-fixed-response |
| scope/0 | CASE-AI-2026-027 |
| scope/1 | AI27-SOURCE-1 |
| scope/2 | AI27-SOURCE-2 |
| credentialClass | none |
| sideEffect | none |
| approvalRequired | true |
| approvalOwnerId | AI27-OWNER |
| timeoutSeconds | 30 |
| enabled | false |
| responseId | AI27-RESPONSE |
| stopId | AI27-STOP |
| actualImplementation | none-record-only |

### AI27-APPROVAL-1

| Field | Value |
|---|---|
| id | AI27-APPROVAL-1 |
| ownerId | AI27-OWNER |
| requesterId | AI27-USER |
| toolId | AI27-MOCK-READER |
| toolVersion | 1.0 |
| caseId | CASE-AI-2026-027 |
| sourceIds/0 | AI27-SOURCE-1 |
| sourceIds/1 | AI27-SOURCE-2 |
| effect | read-fixed-response |
| validFrom | 2026-09-20T09:00:00Z |
| validUntil | 2026-09-20T11:00:00Z |
| origin | human-owner-record |
| decision | Approved |
| singleRequestId | AI27-REQUEST-1 |
| cryptographicProof | not-implemented-synthetic-only |

### AI27-APPROVAL-2

| Field | Value |
|---|---|
| id | AI27-APPROVAL-2 |
| ownerId | AI27-OWNER |
| requesterId | AI27-USER |
| toolId | AI27-MOCK-READER |
| toolVersion | 1.0 |
| caseId | CASE-AI-2026-027 |
| sourceIds/0 | AI27-SOURCE-1 |
| sourceIds/1 | AI27-SOURCE-2 |
| effect | read-fixed-response |
| validFrom | 2026-09-19T09:00:00Z |
| validUntil | 2026-09-19T11:00:00Z |
| origin | human-owner-record |
| decision | Approved |
| singleRequestId | AI27-REQUEST-2 |
| cryptographicProof | not-implemented-synthetic-only |

### AI27-REQUEST-1

| Field | Value |
|---|---|
| id | AI27-REQUEST-1 |
| userId | AI27-USER |
| modelId | AI27-MODEL |
| toolId | AI27-MOCK-READER |
| toolVersion | 1.0 |
| caseId | CASE-AI-2026-027 |
| sourceIds/0 | AI27-SOURCE-1 |
| sourceIds/1 | AI27-SOURCE-2 |
| instructionId | AI27-USER-INSTRUCTION |
| memoryId | AI27-MEMORY-1 |
| approvalId | AI27-APPROVAL-1 |
| requestedEffect | read-fixed-response |
| stepsUsed | 1 |
| stepBudget | 3 |
| killSwitchActive | false |
| asOf | 2026-09-20T10:00:00Z |
| expectedDisposition | Allowed-in-model |
| evidenceId | AI27-EVIDENCE-1 |
| findingId | AI27-FINDING-1 |
| auditId | AI27-AUDIT-1 |
| executed | false |

### AI27-REQUEST-2

| Field | Value |
|---|---|
| id | AI27-REQUEST-2 |
| userId | AI27-USER |
| modelId | AI27-MODEL |
| toolId | AI27-MOCK-READER |
| toolVersion | 1.0 |
| caseId | CASE-AI-2026-027 |
| sourceIds/0 | AI27-SOURCE-1 |
| sourceIds/1 | AI27-SOURCE-2 |
| instructionId | AI27-RAG-INSTRUCTION |
| memoryId | AI27-MEMORY-1 |
| approvalId | AI27-APPROVAL-2 |
| requestedEffect | read-fixed-response |
| stepsUsed | 1 |
| stepBudget | 3 |
| killSwitchActive | false |
| asOf | 2026-09-20T10:00:00Z |
| expectedDisposition | Blocked |
| evidenceId | AI27-EVIDENCE-2 |
| findingId | AI27-FINDING-2 |
| auditId | AI27-AUDIT-2 |
| executed | false |

### AI27-REQUEST-3

| Field | Value |
|---|---|
| id | AI27-REQUEST-3 |
| userId | AI27-USER |
| modelId | AI27-MODEL |
| toolId | AI27-MOCK-READER |
| toolVersion | 1.0 |
| caseId | CASE-AI-2026-027 |
| sourceIds/0 | AI27-SOURCE-1 |
| sourceIds/1 | AI27-SOURCE-2 |
| instructionId | AI27-USER-INSTRUCTION |
| memoryId | AI27-MEMORY-2 |
| approvalId | AI27-APPROVAL-1 |
| requestedEffect | read-fixed-response |
| stepsUsed | 1 |
| stepBudget | 3 |
| killSwitchActive | false |
| asOf | 2026-09-20T10:00:00Z |
| expectedDisposition | Blocked |
| evidenceId | AI27-EVIDENCE-3 |
| findingId | AI27-FINDING-3 |
| auditId | AI27-AUDIT-3 |
| executed | false |

### AI27-REQUEST-4

| Field | Value |
|---|---|
| id | AI27-REQUEST-4 |
| userId | AI27-USER |
| modelId | AI27-MODEL |
| toolId | AI27-MOCK-READER |
| toolVersion | 1.0 |
| caseId | CASE-AI-2026-027 |
| sourceIds/0 | AI27-SOURCE-1 |
| sourceIds/1 | AI27-SOURCE-2 |
| instructionId | AI27-USER-INSTRUCTION |
| memoryId | AI27-MEMORY-1 |
| approvalId | AI27-APPROVAL-1 |
| requestedEffect | write-request-metadata-only |
| stepsUsed | 1 |
| stepBudget | 3 |
| killSwitchActive | false |
| asOf | 2026-09-20T10:00:00Z |
| expectedDisposition | Blocked |
| evidenceId | AI27-EVIDENCE-4 |
| findingId | AI27-FINDING-4 |
| auditId | AI27-AUDIT-4 |
| executed | false |

### AI27-REQUEST-5

| Field | Value |
|---|---|
| id | AI27-REQUEST-5 |
| userId | AI27-USER |
| modelId | AI27-MODEL |
| toolId | AI27-MOCK-READER |
| toolVersion | 1.0 |
| caseId | CASE-AI-2026-027 |
| sourceIds/0 | AI27-SOURCE-1 |
| sourceIds/1 | AI27-SOURCE-2 |
| instructionId | AI27-USER-INSTRUCTION |
| memoryId | AI27-MEMORY-1 |
| approvalId | AI27-APPROVAL-1 |
| requestedEffect | read-fixed-response |
| stepsUsed | 4 |
| stepBudget | 3 |
| killSwitchActive | true |
| asOf | 2026-09-20T10:00:00Z |
| expectedDisposition | Stopped |
| evidenceId | AI27-EVIDENCE-5 |
| findingId | AI27-FINDING-5 |
| auditId | AI27-AUDIT-5 |
| executed | false |

### AI27-REQUEST-6

| Field | Value |
|---|---|
| id | AI27-REQUEST-6 |
| userId | AI27-USER |
| modelId | AI27-MODEL |
| toolId | AI27-EXPORTER |
| toolVersion | 1.0 |
| caseId | CASE-AI-2026-027 |
| sourceIds/0 | AI27-SOURCE-1 |
| sourceIds/1 | AI27-SOURCE-2 |
| instructionId | AI27-USER-INSTRUCTION |
| memoryId | AI27-MEMORY-1 |
| approvalId | AI27-APPROVAL-1 |
| requestedEffect | read-fixed-response |
| stepsUsed | 1 |
| stepBudget | 3 |
| killSwitchActive | false |
| asOf | 2026-09-20T10:00:00Z |
| expectedDisposition | Blocked |
| evidenceId | AI27-EVIDENCE-6 |
| findingId | AI27-FINDING-6 |
| auditId | AI27-AUDIT-6 |
| executed | false |

### AI27-AUDIT-1

| Field | Value |
|---|---|
| id | AI27-AUDIT-1 |
| requestId | AI27-REQUEST-1 |
| evidenceId | AI27-EVIDENCE-1 |
| findingId | AI27-FINDING-1 |
| targetId | AI27-MOCK-READER |
| targetVersion | 1.0 |
| at | 2026-09-20T10:00:00Z |
| disposition | Allowed-in-model |
| origin | author-synthetic |
| ownerId | AI27-OWNER |
| retentionUntil | 2026-09-27T10:00:00Z |
| immutableStorageVerified | false |
| controlEvidence | recorded-comparison-only |
| actualEffect | none |

### AI27-AUDIT-2

| Field | Value |
|---|---|
| id | AI27-AUDIT-2 |
| requestId | AI27-REQUEST-2 |
| evidenceId | AI27-EVIDENCE-2 |
| findingId | AI27-FINDING-2 |
| targetId | AI27-MOCK-READER |
| targetVersion | 1.0 |
| at | 2026-09-20T10:00:00Z |
| disposition | Blocked |
| origin | author-synthetic |
| ownerId | AI27-OWNER |
| retentionUntil | 2026-09-27T10:00:00Z |
| immutableStorageVerified | false |
| controlEvidence | recorded-comparison-only |
| actualEffect | none |

### AI27-AUDIT-3

| Field | Value |
|---|---|
| id | AI27-AUDIT-3 |
| requestId | AI27-REQUEST-3 |
| evidenceId | AI27-EVIDENCE-3 |
| findingId | AI27-FINDING-3 |
| targetId | AI27-MOCK-READER |
| targetVersion | 1.0 |
| at | 2026-09-20T10:00:00Z |
| disposition | Blocked |
| origin | author-synthetic |
| ownerId | AI27-OWNER |
| retentionUntil | 2026-09-27T10:00:00Z |
| immutableStorageVerified | false |
| controlEvidence | recorded-comparison-only |
| actualEffect | none |

### AI27-AUDIT-4

| Field | Value |
|---|---|
| id | AI27-AUDIT-4 |
| requestId | AI27-REQUEST-4 |
| evidenceId | AI27-EVIDENCE-4 |
| findingId | AI27-FINDING-4 |
| targetId | AI27-MOCK-READER |
| targetVersion | 1.0 |
| at | 2026-09-20T10:00:00Z |
| disposition | Blocked |
| origin | author-synthetic |
| ownerId | AI27-OWNER |
| retentionUntil | 2026-09-27T10:00:00Z |
| immutableStorageVerified | false |
| controlEvidence | recorded-comparison-only |
| actualEffect | none |

### AI27-AUDIT-5

| Field | Value |
|---|---|
| id | AI27-AUDIT-5 |
| requestId | AI27-REQUEST-5 |
| evidenceId | AI27-EVIDENCE-5 |
| findingId | AI27-FINDING-5 |
| targetId | AI27-MOCK-READER |
| targetVersion | 1.0 |
| at | 2026-09-20T10:00:00Z |
| disposition | Stopped |
| origin | author-synthetic |
| ownerId | AI27-OWNER |
| retentionUntil | 2026-09-27T10:00:00Z |
| immutableStorageVerified | false |
| controlEvidence | recorded-comparison-only |
| actualEffect | none |

### AI27-AUDIT-6

| Field | Value |
|---|---|
| id | AI27-AUDIT-6 |
| requestId | AI27-REQUEST-6 |
| evidenceId | AI27-EVIDENCE-6 |
| findingId | AI27-FINDING-6 |
| targetId | AI27-EXPORTER |
| targetVersion | 1.0 |
| at | 2026-09-20T10:00:00Z |
| disposition | Blocked |
| origin | author-synthetic |
| ownerId | AI27-OWNER |
| retentionUntil | 2026-09-27T10:00:00Z |
| immutableStorageVerified | false |
| controlEvidence | recorded-comparison-only |
| actualEffect | none |

### limitations

| Field | Value |
|---|---|
| modelEvaluated | false |
| promptClassifierImplemented | false |
| aisvsConformanceClaimed | false |
| signatureVerified | false |
| digestMeaning | SHA-256 of synthetic component label; not a measured model, dataset or deployed artifact |
| independentEvidenceSources | 1 |
| coverage | six authored components and six request records only |

### decision

| Field | Value |
|---|---|
| id | DEC-AI-2026-027 |
| owner | Synthetic CTO Decision Owner |
| value | Allow record comparison only; deployment withheld |
| confidence | 低 |
| fact | 供給記録の対象・版・時刻・状態だけを比較した。 |
| judgment | 限定された読み取り例以外は不足または停止条件を解消できない。 |
| assumption | 供給された時刻とActorはすべて架空である。 |
| alternative | 資料遅延や通常の変更でも不一致は起こり、悪意は断定できない。 |
| prediction | 対象や版を変更すれば今の比較結果は利用できない。 |
| recommendation | 同一対象の承認・観測・停止証跡を揃えて再評価する。 |
| realExecutionAuthorized | false |
| handoff | planned-not-delivered |

### reassessment

| Field | Value |
|---|---|
| id | REA-AI-2026-027 |
| owner | Synthetic AI Reviewer |
| dueAt | 2026-09-22T10:00:00Z |
| triggers/0 | source-version-change |
| triggers/1 | tool-scope-change |
| triggers/2 | approval-expiry |
| triggers/3 | memory-provenance-change |
| triggers/4 | model-version-change |
| triggers/5 | audit-gap |
| triggers/6 | kill-switch-change |
| closure | 同じ対象・版・利用者・期限で不足と停止条件を再検証し、Decision ownerが記録する。 |

### AI27-THREAT-1

| Field | Value |
|---|---|
| id | AI27-THREAT-1 |
| family | instruction-boundary |
| precondition | 資料を指示扱いする構成 |
| impact | 意図外の判断 |
| control | untrusted-data-not-instruction |
| telemetryRequired | instruction-origin/role |
| limit | 文字列検査だけでは一般Injectionを判定できない。 |
| owner | Synthetic AI Reviewer |
| status | Inconclusive |
| reassessmentId | REA-AI-2026-027 |
| controlId | AI27-CONTROL-1 |

### AI27-THREAT-2

| Field | Value |
|---|---|
| id | AI27-THREAT-2 |
| family | rag-memory |
| precondition | Caseまたは由来を失った参照 |
| impact | 別用途の混入 |
| control | case-audience-version-expiry-binding |
| telemetryRequired | retrieval-source/memory-scope |
| limit | scope一致は内容の真実性を保証しない。 |
| owner | Synthetic AI Reviewer |
| status | Inconclusive |
| reassessmentId | REA-AI-2026-027 |
| controlId | AI27-CONTROL-2 |

### AI27-THREAT-3

| Field | Value |
|---|---|
| id | AI27-THREAT-3 |
| family | output-handling |
| precondition | 未検証出力の自動採用 |
| impact | 誤判断 |
| control | no-automatic-fact-source-command |
| telemetryRequired | output-classification/source-ids |
| limit | 原典照合は第28章へ渡す計画で未実施。 |
| owner | Synthetic AI Reviewer |
| status | Inconclusive |
| reassessmentId | REA-AI-2026-027 |
| controlId | AI27-CONTROL-3 |

### AI27-THREAT-4

| Field | Value |
|---|---|
| id | AI27-THREAT-4 |
| family | excessive-agency |
| precondition | 過大CapabilityやScope |
| impact | 意図外の効果 |
| control | read-only-capability/approval |
| telemetryRequired | tool/effect/approval-owner |
| limit | この教材は実Toolを呼ばない。 |
| owner | Synthetic AI Reviewer |
| status | Inconclusive |
| reassessmentId | REA-AI-2026-027 |
| controlId | AI27-CONTROL-4 |

### AI27-THREAT-5

| Field | Value |
|---|---|
| id | AI27-THREAT-5 |
| family | supply-chain |
| precondition | 版・Digest・由来の不足 |
| impact | 対象の取違え |
| control | version-digest-provenance |
| telemetryRequired | component-version/digest |
| limit | ラベルhashは実Artifactの安全性を示さない。 |
| owner | Synthetic AI Reviewer |
| status | Inconclusive |
| reassessmentId | REA-AI-2026-027 |
| controlId | AI27-CONTROL-5 |

### AI27-THREAT-6

| Field | Value |
|---|---|
| id | AI27-THREAT-6 |
| family | peer-authority |
| precondition | 他Agentの自己申告を信頼 |
| impact | 承認の混同 |
| control | no-authority-inheritance |
| telemetryRequired | sender/task/approval-origin |
| limit | Agent間通信の暗号検証は未実装。 |
| owner | Synthetic AI Reviewer |
| status | Inconclusive |
| reassessmentId | REA-AI-2026-027 |
| controlId | AI27-CONTROL-6 |

### AI27-THREAT-7

| Field | Value |
|---|---|
| id | AI27-THREAT-7 |
| family | loop-cascade |
| precondition | 上限なしの反復 |
| impact | 停止遅延 |
| control | bounded-budget/stop-first |
| telemetryRequired | steps/budget/kill-switch |
| limit | 固定記録の停止判定は実停止試験ではない。 |
| owner | Synthetic AI Reviewer |
| status | Inconclusive |
| reassessmentId | REA-AI-2026-027 |
| controlId | AI27-CONTROL-7 |

### AI27-THREAT-8

| Field | Value |
|---|---|
| id | AI27-THREAT-8 |
| family | human-audit |
| precondition | 承認の対象や証跡が不明 |
| impact | 追跡不能 |
| control | same-action-approval/audit |
| telemetryRequired | request/owner/target/version/time |
| limit | 人間の了承だけで内容の正確性は証明されない。 |
| owner | Synthetic AI Reviewer |
| status | Inconclusive |
| reassessmentId | REA-AI-2026-027 |
| controlId | AI27-CONTROL-8 |

### AI27-FINDING-1

| Field | Value |
|---|---|
| id | AI27-FINDING-1 |
| requestId | AI27-REQUEST-1 |
| evidenceId | AI27-EVIDENCE-1 |
| disposition | Allowed-in-model |
| reasons | `[]` |
| threatIds/0 | AI27-THREAT-4 |
| threatIds/1 | AI27-THREAT-8 |
| owner | Synthetic AI Reviewer |
| dueAt | 2026-09-21T10:00:00Z |
| reassessmentId | REA-AI-2026-027 |
| permittedConclusion | 供給記録の条件一致または差戻しだけ。実脆弱性・悪意・対策有効性は判定しない。 |
| controlIds/0 | AI27-CONTROL-4 |
| controlIds/1 | AI27-CONTROL-8 |
| validationIds/0 | AI27-VAL-3 |

### AI27-FINDING-2

| Field | Value |
|---|---|
| id | AI27-FINDING-2 |
| requestId | AI27-REQUEST-2 |
| evidenceId | AI27-EVIDENCE-2 |
| disposition | Blocked |
| reasons/0 | instruction-origin |
| reasons/1 | approval-window |
| threatIds/0 | AI27-THREAT-1 |
| threatIds/1 | AI27-THREAT-6 |
| threatIds/2 | AI27-THREAT-8 |
| owner | Synthetic AI Reviewer |
| dueAt | 2026-09-21T10:00:00Z |
| reassessmentId | REA-AI-2026-027 |
| permittedConclusion | 供給記録の条件一致または差戻しだけ。実脆弱性・悪意・対策有効性は判定しない。 |
| controlIds/0 | AI27-CONTROL-1 |
| controlIds/1 | AI27-CONTROL-6 |
| controlIds/2 | AI27-CONTROL-8 |
| validationIds | `[]` |

### AI27-FINDING-3

| Field | Value |
|---|---|
| id | AI27-FINDING-3 |
| requestId | AI27-REQUEST-3 |
| evidenceId | AI27-EVIDENCE-3 |
| disposition | Blocked |
| reasons/0 | memory-scope-expiry |
| reasons/1 | approval-action-binding |
| threatIds/0 | AI27-THREAT-2 |
| threatIds/1 | AI27-THREAT-8 |
| owner | Synthetic AI Reviewer |
| dueAt | 2026-09-21T10:00:00Z |
| reassessmentId | REA-AI-2026-027 |
| permittedConclusion | 供給記録の条件一致または差戻しだけ。実脆弱性・悪意・対策有効性は判定しない。 |
| controlIds/0 | AI27-CONTROL-2 |
| controlIds/1 | AI27-CONTROL-8 |
| validationIds | `[]` |

### AI27-FINDING-4

| Field | Value |
|---|---|
| id | AI27-FINDING-4 |
| requestId | AI27-REQUEST-4 |
| evidenceId | AI27-EVIDENCE-4 |
| disposition | Blocked |
| reasons/0 | tool-effect |
| reasons/1 | approval-action-binding |
| threatIds/0 | AI27-THREAT-4 |
| threatIds/1 | AI27-THREAT-8 |
| owner | Synthetic AI Reviewer |
| dueAt | 2026-09-21T10:00:00Z |
| reassessmentId | REA-AI-2026-027 |
| permittedConclusion | 供給記録の条件一致または差戻しだけ。実脆弱性・悪意・対策有効性は判定しない。 |
| controlIds/0 | AI27-CONTROL-4 |
| controlIds/1 | AI27-CONTROL-8 |
| validationIds | `[]` |

### AI27-FINDING-5

| Field | Value |
|---|---|
| id | AI27-FINDING-5 |
| requestId | AI27-REQUEST-5 |
| evidenceId | AI27-EVIDENCE-5 |
| disposition | Stopped |
| reasons/0 | stop-or-budget |
| threatIds/0 | AI27-THREAT-7 |
| threatIds/1 | AI27-THREAT-8 |
| owner | Synthetic AI Reviewer |
| dueAt | 2026-09-21T10:00:00Z |
| reassessmentId | REA-AI-2026-027 |
| permittedConclusion | 供給記録の条件一致または差戻しだけ。実脆弱性・悪意・対策有効性は判定しない。 |
| controlIds/0 | AI27-CONTROL-7 |
| controlIds/1 | AI27-CONTROL-8 |
| validationIds | `[]` |

### AI27-FINDING-6

| Field | Value |
|---|---|
| id | AI27-FINDING-6 |
| requestId | AI27-REQUEST-6 |
| evidenceId | AI27-EVIDENCE-6 |
| disposition | Blocked |
| reasons/0 | tool-availability |
| reasons/1 | approval-action-binding |
| threatIds/0 | AI27-THREAT-4 |
| threatIds/1 | AI27-THREAT-5 |
| threatIds/2 | AI27-THREAT-8 |
| owner | Synthetic AI Reviewer |
| dueAt | 2026-09-21T10:00:00Z |
| reassessmentId | REA-AI-2026-027 |
| permittedConclusion | 供給記録の条件一致または差戻しだけ。実脆弱性・悪意・対策有効性は判定しない。 |
| controlIds/0 | AI27-CONTROL-4 |
| controlIds/1 | AI27-CONTROL-5 |
| controlIds/2 | AI27-CONTROL-8 |
| validationIds | `[]` |

### AI27-CONTROL-1

| Field | Value |
|---|---|
| id | AI27-CONTROL-1 |
| threatId | AI27-THREAT-1 |
| description | untrusted-data-not-instruction |
| owner | Synthetic AI Reviewer |
| status | Documented-only |
| runtimeValidated | false |
| telemetryRequired | instruction-origin/role |
| gapId | AI27-GAP-1 |
| reassessmentId | REA-AI-2026-027 |

### AI27-CONTROL-2

| Field | Value |
|---|---|
| id | AI27-CONTROL-2 |
| threatId | AI27-THREAT-2 |
| description | case-audience-version-expiry-binding |
| owner | Synthetic AI Reviewer |
| status | Documented-only |
| runtimeValidated | false |
| telemetryRequired | retrieval-source/memory-scope |
| gapId | AI27-GAP-2 |
| reassessmentId | REA-AI-2026-027 |

### AI27-CONTROL-3

| Field | Value |
|---|---|
| id | AI27-CONTROL-3 |
| threatId | AI27-THREAT-3 |
| description | no-automatic-fact-source-command |
| owner | Synthetic AI Reviewer |
| status | Documented-only |
| runtimeValidated | false |
| telemetryRequired | output-classification/source-ids |
| gapId | AI27-GAP-3 |
| reassessmentId | REA-AI-2026-027 |

### AI27-CONTROL-4

| Field | Value |
|---|---|
| id | AI27-CONTROL-4 |
| threatId | AI27-THREAT-4 |
| description | read-only-capability/approval |
| owner | Synthetic AI Reviewer |
| status | Documented-only |
| runtimeValidated | false |
| telemetryRequired | tool/effect/approval-owner |
| gapId | AI27-GAP-4 |
| reassessmentId | REA-AI-2026-027 |

### AI27-CONTROL-5

| Field | Value |
|---|---|
| id | AI27-CONTROL-5 |
| threatId | AI27-THREAT-5 |
| description | version-digest-provenance |
| owner | Synthetic AI Reviewer |
| status | Documented-only |
| runtimeValidated | false |
| telemetryRequired | component-version/digest |
| gapId | AI27-GAP-5 |
| reassessmentId | REA-AI-2026-027 |

### AI27-CONTROL-6

| Field | Value |
|---|---|
| id | AI27-CONTROL-6 |
| threatId | AI27-THREAT-6 |
| description | no-authority-inheritance |
| owner | Synthetic AI Reviewer |
| status | Documented-only |
| runtimeValidated | false |
| telemetryRequired | sender/task/approval-origin |
| gapId | AI27-GAP-6 |
| reassessmentId | REA-AI-2026-027 |

### AI27-CONTROL-7

| Field | Value |
|---|---|
| id | AI27-CONTROL-7 |
| threatId | AI27-THREAT-7 |
| description | bounded-budget/stop-first |
| owner | Synthetic AI Reviewer |
| status | Documented-only |
| runtimeValidated | false |
| telemetryRequired | steps/budget/kill-switch |
| gapId | AI27-GAP-7 |
| reassessmentId | REA-AI-2026-027 |

### AI27-CONTROL-8

| Field | Value |
|---|---|
| id | AI27-CONTROL-8 |
| threatId | AI27-THREAT-8 |
| description | same-action-approval/audit |
| owner | Synthetic AI Reviewer |
| status | Documented-only |
| runtimeValidated | false |
| telemetryRequired | request/owner/target/version/time |
| gapId | AI27-GAP-8 |
| reassessmentId | REA-AI-2026-027 |

### AI27-EVIDENCE-1

| Field | Value |
|---|---|
| id | AI27-EVIDENCE-1 |
| requestId | AI27-REQUEST-1 |
| auditId | AI27-AUDIT-1 |
| targetId | AI27-MOCK-READER |
| targetVersion | 1.0 |
| at | 2026-09-20T10:00:00Z |
| origin | author-synthetic |
| classification | authored-comparison-not-runtime-observation |
| modelOutputAdopted | false |

### AI27-EVIDENCE-2

| Field | Value |
|---|---|
| id | AI27-EVIDENCE-2 |
| requestId | AI27-REQUEST-2 |
| auditId | AI27-AUDIT-2 |
| targetId | AI27-MOCK-READER |
| targetVersion | 1.0 |
| at | 2026-09-20T10:00:00Z |
| origin | author-synthetic |
| classification | authored-comparison-not-runtime-observation |
| modelOutputAdopted | false |

### AI27-EVIDENCE-3

| Field | Value |
|---|---|
| id | AI27-EVIDENCE-3 |
| requestId | AI27-REQUEST-3 |
| auditId | AI27-AUDIT-3 |
| targetId | AI27-MOCK-READER |
| targetVersion | 1.0 |
| at | 2026-09-20T10:00:00Z |
| origin | author-synthetic |
| classification | authored-comparison-not-runtime-observation |
| modelOutputAdopted | false |

### AI27-EVIDENCE-4

| Field | Value |
|---|---|
| id | AI27-EVIDENCE-4 |
| requestId | AI27-REQUEST-4 |
| auditId | AI27-AUDIT-4 |
| targetId | AI27-MOCK-READER |
| targetVersion | 1.0 |
| at | 2026-09-20T10:00:00Z |
| origin | author-synthetic |
| classification | authored-comparison-not-runtime-observation |
| modelOutputAdopted | false |

### AI27-EVIDENCE-5

| Field | Value |
|---|---|
| id | AI27-EVIDENCE-5 |
| requestId | AI27-REQUEST-5 |
| auditId | AI27-AUDIT-5 |
| targetId | AI27-MOCK-READER |
| targetVersion | 1.0 |
| at | 2026-09-20T10:00:00Z |
| origin | author-synthetic |
| classification | authored-comparison-not-runtime-observation |
| modelOutputAdopted | false |

### AI27-EVIDENCE-6

| Field | Value |
|---|---|
| id | AI27-EVIDENCE-6 |
| requestId | AI27-REQUEST-6 |
| auditId | AI27-AUDIT-6 |
| targetId | AI27-EXPORTER |
| targetVersion | 1.0 |
| at | 2026-09-20T10:00:00Z |
| origin | author-synthetic |
| classification | authored-comparison-not-runtime-observation |
| modelOutputAdopted | false |

### stop

| Field | Value |
|---|---|
| id | AI27-STOP |
| ownerId | AI27-OWNER |
| stepBudget | 3 |
| timeoutSeconds | 30 |
| precedence | stop-before-approval |
| controlChannel | not-implemented-record-only |
| runtimeTested | false |
| auditRequired | true |

### AI27-GAP-1

| Field | Value |
|---|---|
| id | AI27-GAP-1 |
| controlId | AI27-CONTROL-1 |
| reason | 文字列検査だけでは一般Injectionを判定できない。 |
| owner | Synthetic AI Reviewer |
| dueAt | 2026-09-21T10:00:00Z |
| status | Open |
| reassessmentId | REA-AI-2026-027 |

### AI27-GAP-2

| Field | Value |
|---|---|
| id | AI27-GAP-2 |
| controlId | AI27-CONTROL-2 |
| reason | scope一致は内容の真実性を保証しない。 |
| owner | Synthetic AI Reviewer |
| dueAt | 2026-09-21T10:00:00Z |
| status | Open |
| reassessmentId | REA-AI-2026-027 |

### AI27-GAP-3

| Field | Value |
|---|---|
| id | AI27-GAP-3 |
| controlId | AI27-CONTROL-3 |
| reason | 原典照合は第28章へ渡す計画で未実施。 |
| owner | Synthetic AI Reviewer |
| dueAt | 2026-09-21T10:00:00Z |
| status | Open |
| reassessmentId | REA-AI-2026-027 |

### AI27-GAP-4

| Field | Value |
|---|---|
| id | AI27-GAP-4 |
| controlId | AI27-CONTROL-4 |
| reason | この教材は実Toolを呼ばない。 |
| owner | Synthetic AI Reviewer |
| dueAt | 2026-09-21T10:00:00Z |
| status | Open |
| reassessmentId | REA-AI-2026-027 |

### AI27-GAP-5

| Field | Value |
|---|---|
| id | AI27-GAP-5 |
| controlId | AI27-CONTROL-5 |
| reason | ラベルhashは実Artifactの安全性を示さない。 |
| owner | Synthetic AI Reviewer |
| dueAt | 2026-09-21T10:00:00Z |
| status | Open |
| reassessmentId | REA-AI-2026-027 |

### AI27-GAP-6

| Field | Value |
|---|---|
| id | AI27-GAP-6 |
| controlId | AI27-CONTROL-6 |
| reason | Agent間通信の暗号検証は未実装。 |
| owner | Synthetic AI Reviewer |
| dueAt | 2026-09-21T10:00:00Z |
| status | Open |
| reassessmentId | REA-AI-2026-027 |

### AI27-GAP-7

| Field | Value |
|---|---|
| id | AI27-GAP-7 |
| controlId | AI27-CONTROL-7 |
| reason | 固定記録の停止判定は実停止試験ではない。 |
| owner | Synthetic AI Reviewer |
| dueAt | 2026-09-21T10:00:00Z |
| status | Open |
| reassessmentId | REA-AI-2026-027 |

### AI27-GAP-8

| Field | Value |
|---|---|
| id | AI27-GAP-8 |
| controlId | AI27-CONTROL-8 |
| reason | 人間の了承だけで内容の正確性は証明されない。 |
| owner | Synthetic AI Reviewer |
| dueAt | 2026-09-21T10:00:00Z |
| status | Open |
| reassessmentId | REA-AI-2026-027 |
