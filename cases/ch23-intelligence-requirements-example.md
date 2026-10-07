# 第23章 完全合成例：Intelligence Requirement and Collection Plan

`ART-29` / `IRCP-2026-023-001` / `CASE-IRP-2026-001`の供給記録である。[第23章](../manuscript/23-intelligence-requirements.md)、[Template](../templates/intelligence-requirement-collection-plan.md)、[JSON](fixtures/ch23-intelligence-requirements.json)、[Schema](../schemas/ch23-intelligence-requirements.schema.json)を照合する。

## 読み方と境界

Purposeは判断要求から不足を辿る読解、Prerequisiteは本章の供給例、Authority / Scopeは教材Dataだけ、Expected evidenceは回答条件とGapの対応、Impactは教材上の記入に限る。実Data・未知の権限・外部接続が必要ならStopし、Cleanupは作業用記入内容の整理だけである。実操作・実収集・実通知は0件、networkRequired/実行権限はfalseである。

親CASE-2026-001を方法上refinesするが、対象・版・Evidence・実許可・Incident宣言・未配達Receiptを継承しない。供給時刻は2026-10-01〜03という架空の教育用条件であり、実観測や未来の実操作予定ではない。

## 判断と五つの問い

判断主体は48時間以内の停止案と制限付き継続案を比較する。R1だけが二条件を回答可能、R2は操作の記載だけで結果が不足、R3〜R5は回答未了である。C1はR1/R2、C3はR2/R3へ関係し、同じCollectionの状態を両Requirementへ機械的に転記しない。

四EvidenceのうちE4はSource品質pendingで、回答の根拠には使わない。C6はAuthority/Terms unknownのBlocked、C8は旧重複案のCancelledを保持する。七Gapと低い確信度を残すことが、この成果物の完成形である。

## 全欄の読み方

各表のFieldはJSON内のpath、Valueは供給値である。null、false、空配列も省略しない。合成SourceのSNOTE-IR23は教科書の一次資料を登録するSRC-*と別の識別子である。

### schemaVersion

| Field | Value |
|---|---|
| `schemaVersion` | `1.0.0` |

### synthetic

| Field | Value |
|---|---|
| `synthetic` | `true` |

### readOnly

| Field | Value |
|---|---|
| `readOnly` | `true` |

### networkRequired

| Field | Value |
|---|---|
| `networkRequired` | `false` |

### executionAuthorized

| Field | Value |
|---|---|
| `executionAuthorized` | `false` |

### record

| Field | Value |
|---|---|
| `id` | `IRCP-2026-023-001` |
| `artifactId` | `ART-29` |
| `caseId` | `CASE-IRP-2026-001` |
| `subjectId` | `APP-IR23-001` |
| `revision` | `IR23-REV-001` |
| `asOf` | `2026-10-02T12:00:00Z` |
| `actualCollections` | `0` |
| `actualActions` | `0` |
| `actualNotifications` | `0` |

### parents

| Field | Value |
|---|---|
| `relation` | `refines` |
| `use` | `method-reference-only` |
| `caseId` | `CASE-2026-001` |
| `threatModelId` | `TM-2026-001` |
| `telemetryRecordId` | `TCM-2026-016` |
| `incidentRecordId` | `IAP-2026-019-001` |
| `subjectInherited` | `false` |
| `evidenceTransferred` | `false` |
| `authorityTransferred` | `false` |
| `incidentDeclared` | `false` |
| `parentStateChanged` | `false` |

### decision

| Field | Value |
|---|---|
| `id` | `DEC-IR23-001` |
| `owner` | `ROLE-IR23-DECISION-OWNER` |
| `question` | `48時間以内に外部連携を停止すべきか` |
| `openedAt` | `2026-10-01T00:00:00Z` |
| `deadline` | `2026-10-03T00:00:00Z` |
| `options/0/id` | `OPT-IR23-STOP` |
| `options/0/text` | `停止を提案する` |
| `options/0/reversibility` | `復旧条件の確認が必要` |
| `options/1/id` | `OPT-IR23-LIMIT` |
| `options/1/text` | `制限付き継続を提案する` |
| `options/1/reversibility` | `制限を再評価する条件が必要` |
| `recommendation` | `未充足の問いを意思決定者へ提示し条件付き案を比較する。実停止は行わない` |
| `judgmentConfidence` | `低` |
| `alternative` | `正常変更または誤設定の説明も未排除` |

### FACT-IR23-1

| Field | Value |
|---|---|
| `id` | `FACT-IR23-1` |
| `evidenceId` | `IR23-E1` |
| `text` | `対象は架空の請求連携一件` |

### FACT-IR23-2

| Field | Value |
|---|---|
| `id` | `FACT-IR23-2` |
| `evidenceId` | `IR23-E2` |
| `text` | `供給記録に同期処理一件が記載される` |

### FACT-IR23-3

| Field | Value |
|---|---|
| `id` | `FACT-IR23-3` |
| `evidenceId` | `IR23-E3` |
| `text` | `供給公開文書例は、教材対象APP-IR23-001/IR23-REV-001の設定上の許可範囲を参照機能だけと定義し、更新機能を含めない` |

### ASSUMP-IR23-001

| Field | Value |
|---|---|
| `id` | `ASSUMP-IR23-001` |
| `text` | `教材上、判断主体は同じ48時間の期限を保つ` |
| `validation` | `期限変更の供給指示で再評価する` |

### IR23-R1

| Field | Value |
|---|---|
| `id` | `IR23-R1` |
| `decisionId` | `DEC-IR23-001` |
| `priority` | `P0 Decision blocking` |
| `timeHorizon` | `Tactical` |
| `question` | `影響対象と権限範囲` |
| `supportingQuestion` | `対象を同定するには何が不足しているか` |
| `criteria/0/id` | `IR23-R1-A` |
| `criteria/0/text` | `対象を同定する` |
| `criteria/1/id` | `IR23-R1-B` |
| `criteria/1/text` | `許可された機能の範囲を区別する` |
| `minimumConfidence` | `中` |
| `status` | `Satisfied` |
| `collectionIds/0` | `COL-IR23-001` |
| `collectionIds/1` | `COL-IR23-002` |
| `answerBindings/0/criterionId` | `IR23-R1-A` |
| `answerBindings/0/evidenceIds/0` | `IR23-E1` |
| `answerBindings/0/confidence` | `中` |
| `answerBindings/1/criterionId` | `IR23-R1-B` |
| `answerBindings/1/evidenceIds/0` | `IR23-E3` |
| `answerBindings/1/confidence` | `中` |
| `gapIds` | `[]` |
| `owner` | `ROLE-IR23-ANALYST-1` |
| `deadline` | `2026-10-02T20:00:00Z` |
| `judgmentConfidence` | `中` |
| `judgment` | `供給された対象・版・Window内の二条件だけ回答可能` |
| `alternative` | `供給例以外の対象や条件では結論が変わり得る` |
| `invalidation` | `対象・版・Scope・Source品質・権限条件が変化したとき` |
| `reassessmentId` | `REASS-IR23-001` |
| `cancellationReason` | `null` |
| `blocker` | `null` |

### IR23-R2

| Field | Value |
|---|---|
| `id` | `IR23-R2` |
| `decisionId` | `DEC-IR23-001` |
| `priority` | `P0 Decision blocking` |
| `timeHorizon` | `Tactical` |
| `question` | `実行された操作のEvidence` |
| `supportingQuestion` | `供給記録内の操作を特定するには何が不足しているか` |
| `criteria/0/id` | `IR23-R2-A` |
| `criteria/0/text` | `供給記録内の操作を特定する` |
| `criteria/1/id` | `IR23-R2-B` |
| `criteria/1/text` | `操作の結果を別の根拠で確認する` |
| `minimumConfidence` | `中` |
| `status` | `Partially satisfied` |
| `collectionIds/0` | `COL-IR23-001` |
| `collectionIds/1` | `COL-IR23-003` |
| `answerBindings/0/criterionId` | `IR23-R2-A` |
| `answerBindings/0/evidenceIds/0` | `IR23-E2` |
| `answerBindings/0/confidence` | `中` |
| `gapIds/0` | `GAP-IR23-R2-B` |
| `owner` | `ROLE-IR23-ANALYST-2` |
| `deadline` | `2026-10-02T20:00:00Z` |
| `judgmentConfidence` | `低` |
| `judgment` | `未充足の問いを残し結論を限定する` |
| `alternative` | `供給例以外の対象や条件では結論が変わり得る` |
| `invalidation` | `対象・版・Scope・Source品質・権限条件が変化したとき` |
| `reassessmentId` | `REASS-IR23-001` |
| `cancellationReason` | `null` |
| `blocker` | `null` |

### IR23-R3

| Field | Value |
|---|---|
| `id` | `IR23-R3` |
| `decisionId` | `DEC-IR23-001` |
| `priority` | `P1 Required` |
| `timeHorizon` | `Tactical` |
| `question` | `代替説明` |
| `supportingQuestion` | `正常な変更で説明できる条件を示すには何が不足しているか` |
| `criteria/0/id` | `IR23-R3-A` |
| `criteria/0/text` | `正常な変更で説明できる条件を示す` |
| `criteria/1/id` | `IR23-R3-B` |
| `criteria/1/text` | `誤設定で説明できる条件を示す` |
| `minimumConfidence` | `中` |
| `status` | `Collecting` |
| `collectionIds/0` | `COL-IR23-002` |
| `collectionIds/1` | `COL-IR23-003` |
| `collectionIds/2` | `COL-IR23-004` |
| `answerBindings` | `[]` |
| `gapIds/0` | `GAP-IR23-R3-A` |
| `gapIds/1` | `GAP-IR23-R3-B` |
| `owner` | `ROLE-IR23-ANALYST-3` |
| `deadline` | `2026-10-02T20:00:00Z` |
| `judgmentConfidence` | `低` |
| `judgment` | `未充足の問いを残し結論を限定する` |
| `alternative` | `供給例以外の対象や条件では結論が変わり得る` |
| `invalidation` | `対象・版・Scope・Source品質・権限条件が変化したとき` |
| `reassessmentId` | `REASS-IR23-001` |
| `cancellationReason` | `null` |
| `blocker` | `null` |

### IR23-R4

| Field | Value |
|---|---|
| `id` | `IR23-R4` |
| `decisionId` | `DEC-IR23-001` |
| `priority` | `P1 Required` |
| `timeHorizon` | `Tactical` |
| `question` | `Controlの有効性` |
| `supportingQuestion` | `期待する抑止条件を示すには何が不足しているか` |
| `criteria/0/id` | `IR23-R4-A` |
| `criteria/0/text` | `期待する抑止条件を示す` |
| `criteria/1/id` | `IR23-R4-B` |
| `criteria/1/text` | `同じ条件の正常対比を示す` |
| `minimumConfidence` | `中` |
| `status` | `Planned` |
| `collectionIds/0` | `COL-IR23-005` |
| `collectionIds/1` | `COL-IR23-007` |
| `answerBindings` | `[]` |
| `gapIds/0` | `GAP-IR23-R4-A` |
| `gapIds/1` | `GAP-IR23-R4-B` |
| `owner` | `ROLE-IR23-ANALYST-4` |
| `deadline` | `2026-10-02T20:00:00Z` |
| `judgmentConfidence` | `低` |
| `judgment` | `未充足の問いを残し結論を限定する` |
| `alternative` | `供給例以外の対象や条件では結論が変わり得る` |
| `invalidation` | `対象・版・Scope・Source品質・権限条件が変化したとき` |
| `reassessmentId` | `REASS-IR23-001` |
| `cancellationReason` | `null` |
| `blocker` | `null` |

### IR23-R5

| Field | Value |
|---|---|
| `id` | `IR23-R5` |
| `decisionId` | `DEC-IR23-001` |
| `priority` | `P0 Decision blocking` |
| `timeHorizon` | `Tactical` |
| `question` | `停止の事業影響` |
| `supportingQuestion` | `停止で中断する業務を特定するには何が不足しているか` |
| `criteria/0/id` | `IR23-R5-A` |
| `criteria/0/text` | `停止で中断する業務を特定する` |
| `criteria/1/id` | `IR23-R5-B` |
| `criteria/1/text` | `復旧可能な時間を確認する` |
| `minimumConfidence` | `中` |
| `status` | `Blocked` |
| `collectionIds/0` | `COL-IR23-006` |
| `collectionIds/1` | `COL-IR23-007` |
| `collectionIds/2` | `COL-IR23-008` |
| `answerBindings` | `[]` |
| `gapIds/0` | `GAP-IR23-R5-A` |
| `gapIds/1` | `GAP-IR23-R5-B` |
| `owner` | `ROLE-IR23-ANALYST-5` |
| `deadline` | `2026-10-02T20:00:00Z` |
| `judgmentConfidence` | `低` |
| `judgment` | `未充足の問いを残し結論を限定する` |
| `alternative` | `供給例以外の対象や条件では結論が変わり得る` |
| `invalidation` | `対象・版・Scope・Source品質・権限条件が変化したとき` |
| `reassessmentId` | `REASS-IR23-001` |
| `cancellationReason` | `null` |
| `blocker` | `架空Owner回答の利用条件が未確認` |

### COL-IR23-001

| Field | Value |
|---|---|
| `id` | `COL-IR23-001` |
| `requirementIds/0` | `IR23-R1` |
| `requirementIds/1` | `IR23-R2` |
| `sourceClass` | `provided-telemetry` |
| `methodClass` | `provided-data-review` |
| `authority` | `provided-synthetic-only` |
| `terms` | `provided-exercise-only` |
| `classification` | `synthetic-public` |
| `privacy` | `no-real-person-data` |
| `retention` | `exercise-record-only` |
| `cost` | `供給資料の読解15分以内という教材上の見積り` |
| `owner` | `ROLE-IR23-COLLECTOR-1` |
| `deadline` | `2026-10-02T16:00:00Z` |
| `status` | `Satisfied` |
| `deliverableIds/0` | `IR23-D1-A` |
| `deliverableIds/1` | `IR23-D1-B` |
| `evidenceIds/0` | `IR23-E1` |
| `evidenceIds/1` | `IR23-E2` |
| `stop` | `Authority・Terms・Classification不明なら停止。外部接続・実Data混入時も停止` |
| `blocker` | `null` |
| `cancellationReason` | `null` |
| `executionAuthorized` | `false` |

### COL-IR23-002

| Field | Value |
|---|---|
| `id` | `COL-IR23-002` |
| `requirementIds/0` | `IR23-R1` |
| `requirementIds/1` | `IR23-R3` |
| `sourceClass` | `provided-public-document` |
| `methodClass` | `provided-data-review` |
| `authority` | `provided-synthetic-only` |
| `terms` | `provided-exercise-only` |
| `classification` | `synthetic-public` |
| `privacy` | `no-real-person-data` |
| `retention` | `exercise-record-only` |
| `cost` | `供給資料の読解15分以内という教材上の見積り` |
| `owner` | `ROLE-IR23-COLLECTOR-2` |
| `deadline` | `2026-10-02T16:00:00Z` |
| `status` | `Satisfied` |
| `deliverableIds/0` | `IR23-D2-A` |
| `evidenceIds/0` | `IR23-E3` |
| `stop` | `Authority・Terms・Classification不明なら停止。外部接続・実Data混入時も停止` |
| `blocker` | `null` |
| `cancellationReason` | `null` |
| `executionAuthorized` | `false` |

### COL-IR23-003

| Field | Value |
|---|---|
| `id` | `COL-IR23-003` |
| `requirementIds/0` | `IR23-R2` |
| `requirementIds/1` | `IR23-R3` |
| `sourceClass` | `provided-owner-confirmation` |
| `methodClass` | `provided-data-review` |
| `authority` | `provided-synthetic-only` |
| `terms` | `provided-exercise-only` |
| `classification` | `synthetic-public` |
| `privacy` | `no-real-person-data` |
| `retention` | `exercise-record-only` |
| `cost` | `供給資料の読解15分以内という教材上の見積り` |
| `owner` | `ROLE-IR23-COLLECTOR-3` |
| `deadline` | `2026-10-02T16:00:00Z` |
| `status` | `Partially satisfied` |
| `deliverableIds/0` | `IR23-D3-A` |
| `deliverableIds/1` | `IR23-D3-B` |
| `evidenceIds/0` | `IR23-E4` |
| `stop` | `Authority・Terms・Classification不明なら停止。外部接続・実Data混入時も停止` |
| `blocker` | `null` |
| `cancellationReason` | `null` |
| `executionAuthorized` | `false` |

### COL-IR23-004

| Field | Value |
|---|---|
| `id` | `COL-IR23-004` |
| `requirementIds/0` | `IR23-R3` |
| `sourceClass` | `provided-telemetry` |
| `methodClass` | `provided-data-review` |
| `authority` | `provided-synthetic-only` |
| `terms` | `provided-exercise-only` |
| `classification` | `synthetic-public` |
| `privacy` | `no-real-person-data` |
| `retention` | `exercise-record-only` |
| `cost` | `供給資料の読解15分以内という教材上の見積り` |
| `owner` | `ROLE-IR23-COLLECTOR-4` |
| `deadline` | `2026-10-02T16:00:00Z` |
| `status` | `Collecting` |
| `deliverableIds/0` | `IR23-D4-A` |
| `evidenceIds` | `[]` |
| `stop` | `Authority・Terms・Classification不明なら停止。外部接続・実Data混入時も停止` |
| `blocker` | `null` |
| `cancellationReason` | `null` |
| `executionAuthorized` | `false` |

### COL-IR23-005

| Field | Value |
|---|---|
| `id` | `COL-IR23-005` |
| `requirementIds/0` | `IR23-R4` |
| `sourceClass` | `provided-telemetry` |
| `methodClass` | `provided-data-review` |
| `authority` | `provided-synthetic-only` |
| `terms` | `provided-exercise-only` |
| `classification` | `synthetic-public` |
| `privacy` | `no-real-person-data` |
| `retention` | `exercise-record-only` |
| `cost` | `供給資料の読解15分以内という教材上の見積り` |
| `owner` | `ROLE-IR23-COLLECTOR-5` |
| `deadline` | `2026-10-02T16:00:00Z` |
| `status` | `Planned` |
| `deliverableIds/0` | `IR23-D5-A` |
| `evidenceIds` | `[]` |
| `stop` | `Authority・Terms・Classification不明なら停止。外部接続・実Data混入時も停止` |
| `blocker` | `null` |
| `cancellationReason` | `null` |
| `executionAuthorized` | `false` |

### COL-IR23-006

| Field | Value |
|---|---|
| `id` | `COL-IR23-006` |
| `requirementIds/0` | `IR23-R5` |
| `sourceClass` | `provided-owner-confirmation` |
| `methodClass` | `provided-data-review` |
| `authority` | `unknown` |
| `terms` | `unknown` |
| `classification` | `synthetic-public` |
| `privacy` | `no-real-person-data` |
| `retention` | `exercise-record-only` |
| `cost` | `供給資料の読解15分以内という教材上の見積り` |
| `owner` | `ROLE-IR23-COLLECTOR-6` |
| `deadline` | `2026-10-02T16:00:00Z` |
| `status` | `Blocked` |
| `deliverableIds/0` | `IR23-D6-A` |
| `evidenceIds` | `[]` |
| `stop` | `Authority・Terms・Classification不明なら停止。外部接続・実Data混入時も停止` |
| `blocker` | `AuthorityとTermsが不明のため読解開始不可` |
| `cancellationReason` | `null` |
| `executionAuthorized` | `false` |

### COL-IR23-007

| Field | Value |
|---|---|
| `id` | `COL-IR23-007` |
| `requirementIds/0` | `IR23-R4` |
| `requirementIds/1` | `IR23-R5` |
| `sourceClass` | `provided-public-document` |
| `methodClass` | `provided-data-review` |
| `authority` | `provided-synthetic-only` |
| `terms` | `provided-exercise-only` |
| `classification` | `synthetic-public` |
| `privacy` | `no-real-person-data` |
| `retention` | `exercise-record-only` |
| `cost` | `供給資料の読解15分以内という教材上の見積り` |
| `owner` | `ROLE-IR23-COLLECTOR-7` |
| `deadline` | `2026-10-02T16:00:00Z` |
| `status` | `Planned` |
| `deliverableIds/0` | `IR23-D7-A` |
| `evidenceIds` | `[]` |
| `stop` | `Authority・Terms・Classification不明なら停止。外部接続・実Data混入時も停止` |
| `blocker` | `null` |
| `cancellationReason` | `null` |
| `executionAuthorized` | `false` |

### COL-IR23-008

| Field | Value |
|---|---|
| `id` | `COL-IR23-008` |
| `requirementIds/0` | `IR23-R5` |
| `sourceClass` | `provided-owner-confirmation` |
| `methodClass` | `provided-data-review` |
| `authority` | `provided-synthetic-only` |
| `terms` | `provided-exercise-only` |
| `classification` | `synthetic-public` |
| `privacy` | `no-real-person-data` |
| `retention` | `exercise-record-only` |
| `cost` | `供給資料の読解15分以内という教材上の見積り` |
| `owner` | `ROLE-IR23-COLLECTOR-8` |
| `deadline` | `2026-10-02T16:00:00Z` |
| `status` | `Cancelled` |
| `deliverableIds/0` | `IR23-D8-A` |
| `evidenceIds` | `[]` |
| `stop` | `Authority・Terms・Classification不明なら停止。外部接続・実Data混入時も停止` |
| `blocker` | `null` |
| `cancellationReason` | `別のCollectionと目的が重複した旧案。未実施のまま保持` |
| `executionAuthorized` | `false` |

### SNOTE-IR23-1

| Field | Value |
|---|---|
| `id` | `SNOTE-IR23-1` |
| `sourceClass` | `provided-telemetry` |
| `quality` | `reviewed` |
| `qualityReason` | `供給範囲・版・来歴を教材内で照合` |
| `origin` | `PROVIDED-IR23-1` |
| `synthetic` | `true` |
| `independentGroup` | `GROUP-IR23-1` |

### SNOTE-IR23-2

| Field | Value |
|---|---|
| `id` | `SNOTE-IR23-2` |
| `sourceClass` | `provided-public-document` |
| `quality` | `reviewed` |
| `qualityReason` | `供給範囲・版・来歴を教材内で照合` |
| `origin` | `PROVIDED-IR23-2` |
| `synthetic` | `true` |
| `independentGroup` | `GROUP-IR23-2` |

### SNOTE-IR23-3

| Field | Value |
|---|---|
| `id` | `SNOTE-IR23-3` |
| `sourceClass` | `provided-owner-confirmation` |
| `quality` | `pending` |
| `qualityReason` | `架空回答の独立確認が未了` |
| `origin` | `PROVIDED-IR23-3` |
| `synthetic` | `true` |
| `independentGroup` | `GROUP-IR23-3` |

### IR23-E1

| Field | Value |
|---|---|
| `id` | `IR23-E1` |
| `collectionId` | `COL-IR23-001` |
| `deliverableId` | `IR23-D1-A` |
| `sourceId` | `SNOTE-IR23-1` |
| `subjectId` | `APP-IR23-001` |
| `revision` | `IR23-REV-001` |
| `windowStart` | `2026-10-01T00:00:00Z` |
| `windowEnd` | `2026-10-02T10:00:00Z` |
| `availableAt` | `2026-10-02T11:00:00Z` |
| `criterionIds/0` | `IR23-R1-A` |
| `observation` | `対象は架空の請求連携一件` |

### IR23-E2

| Field | Value |
|---|---|
| `id` | `IR23-E2` |
| `collectionId` | `COL-IR23-001` |
| `deliverableId` | `IR23-D1-B` |
| `sourceId` | `SNOTE-IR23-1` |
| `subjectId` | `APP-IR23-001` |
| `revision` | `IR23-REV-001` |
| `windowStart` | `2026-10-01T00:00:00Z` |
| `windowEnd` | `2026-10-02T10:00:00Z` |
| `availableAt` | `2026-10-02T11:00:00Z` |
| `criterionIds/0` | `IR23-R2-A` |
| `observation` | `供給記録に同期処理一件が記載される` |

### IR23-E3

| Field | Value |
|---|---|
| `id` | `IR23-E3` |
| `collectionId` | `COL-IR23-002` |
| `deliverableId` | `IR23-D2-A` |
| `sourceId` | `SNOTE-IR23-2` |
| `subjectId` | `APP-IR23-001` |
| `revision` | `IR23-REV-001` |
| `windowStart` | `2026-10-01T00:00:00Z` |
| `windowEnd` | `2026-10-02T10:00:00Z` |
| `availableAt` | `2026-10-02T11:00:00Z` |
| `criterionIds/0` | `IR23-R1-B` |
| `observation` | `供給公開文書例は、教材対象APP-IR23-001/IR23-REV-001の設定上の許可範囲を参照機能だけと定義し、更新機能を含めない` |

### IR23-E4

| Field | Value |
|---|---|
| `id` | `IR23-E4` |
| `collectionId` | `COL-IR23-003` |
| `deliverableId` | `IR23-D3-A` |
| `sourceId` | `SNOTE-IR23-3` |
| `subjectId` | `APP-IR23-001` |
| `revision` | `IR23-REV-001` |
| `windowStart` | `2026-10-01T00:00:00Z` |
| `windowEnd` | `2026-10-02T10:00:00Z` |
| `availableAt` | `2026-10-02T11:00:00Z` |
| `criterionIds/0` | `IR23-R2-B` |
| `observation` | `架空Owner回答案だけでは操作結果を確定できない` |

### GAP-IR23-R2-B

| Field | Value |
|---|---|
| `id` | `GAP-IR23-R2-B` |
| `requirementId` | `IR23-R2` |
| `criterionId` | `IR23-R2-B` |
| `reason` | `回答条件を満たす評価済みSourceのEvidenceが未供給` |
| `owner` | `ROLE-IR23-ANALYST-2` |
| `deadline` | `2026-10-02T20:00:00Z` |
| `confidenceLimit` | `低` |
| `reassessmentId` | `REASS-IR23-001` |

### GAP-IR23-R3-A

| Field | Value |
|---|---|
| `id` | `GAP-IR23-R3-A` |
| `requirementId` | `IR23-R3` |
| `criterionId` | `IR23-R3-A` |
| `reason` | `回答条件を満たす評価済みSourceのEvidenceが未供給` |
| `owner` | `ROLE-IR23-ANALYST-3` |
| `deadline` | `2026-10-02T20:00:00Z` |
| `confidenceLimit` | `低` |
| `reassessmentId` | `REASS-IR23-001` |

### GAP-IR23-R3-B

| Field | Value |
|---|---|
| `id` | `GAP-IR23-R3-B` |
| `requirementId` | `IR23-R3` |
| `criterionId` | `IR23-R3-B` |
| `reason` | `回答条件を満たす評価済みSourceのEvidenceが未供給` |
| `owner` | `ROLE-IR23-ANALYST-3` |
| `deadline` | `2026-10-02T20:00:00Z` |
| `confidenceLimit` | `低` |
| `reassessmentId` | `REASS-IR23-001` |

### GAP-IR23-R4-A

| Field | Value |
|---|---|
| `id` | `GAP-IR23-R4-A` |
| `requirementId` | `IR23-R4` |
| `criterionId` | `IR23-R4-A` |
| `reason` | `回答条件を満たす評価済みSourceのEvidenceが未供給` |
| `owner` | `ROLE-IR23-ANALYST-4` |
| `deadline` | `2026-10-02T20:00:00Z` |
| `confidenceLimit` | `低` |
| `reassessmentId` | `REASS-IR23-001` |

### GAP-IR23-R4-B

| Field | Value |
|---|---|
| `id` | `GAP-IR23-R4-B` |
| `requirementId` | `IR23-R4` |
| `criterionId` | `IR23-R4-B` |
| `reason` | `回答条件を満たす評価済みSourceのEvidenceが未供給` |
| `owner` | `ROLE-IR23-ANALYST-4` |
| `deadline` | `2026-10-02T20:00:00Z` |
| `confidenceLimit` | `低` |
| `reassessmentId` | `REASS-IR23-001` |

### GAP-IR23-R5-A

| Field | Value |
|---|---|
| `id` | `GAP-IR23-R5-A` |
| `requirementId` | `IR23-R5` |
| `criterionId` | `IR23-R5-A` |
| `reason` | `回答条件を満たす評価済みSourceのEvidenceが未供給` |
| `owner` | `ROLE-IR23-ANALYST-5` |
| `deadline` | `2026-10-02T20:00:00Z` |
| `confidenceLimit` | `低` |
| `reassessmentId` | `REASS-IR23-001` |

### GAP-IR23-R5-B

| Field | Value |
|---|---|
| `id` | `GAP-IR23-R5-B` |
| `requirementId` | `IR23-R5` |
| `criterionId` | `IR23-R5-B` |
| `reason` | `回答条件を満たす評価済みSourceのEvidenceが未供給` |
| `owner` | `ROLE-IR23-ANALYST-5` |
| `deadline` | `2026-10-02T20:00:00Z` |
| `confidenceLimit` | `低` |
| `reassessmentId` | `REASS-IR23-001` |

### pipeline

| Field | Value |
|---|---|
| `processingOwner` | `ROLE-IR23-PROCESSOR` |
| `processingDeadline` | `2026-10-02T18:00:00Z` |
| `analysisOwner` | `ROLE-IR23-ANALYSIS` |
| `analysisDeadline` | `2026-10-02T21:00:00Z` |
| `distributionAudience` | `ROLE-IR23-DECISION-OWNER` |
| `distributionDeadline` | `2026-10-02T22:00:00Z` |
| `deliveryStatus` | `planned-not-delivered` |
| `receiptId` | `null` |

### feedback

| Field | Value |
|---|---|
| `id` | `FB-IR23-001` |
| `question` | `回答が選択肢の比較に使えるか。期限と不足は伝わったか` |
| `owner` | `ROLE-IR23-DECISION-OWNER` |
| `invalidation/0` | `対象または版の変更` |
| `invalidation/1` | `Source品質または利用条件の変更` |
| `invalidation/2` | `期限または選択肢の変更` |
| `reassessmentId` | `REASS-IR23-001` |
| `reassessmentAt` | `2026-10-03T00:00:00Z` |
| `stop` | `未確認の権限を優先度や期限で上書きしない` |

### HOF-IR23-24

| Field | Value |
|---|---|
| `id` | `HOF-IR23-24` |
| `targetChapter` | `24` |
| `purpose` | `Sourceと来歴・品質の確認条件` |
| `refs/0` | `SNOTE-IR23-1` |
| `refs/1` | `SNOTE-IR23-2` |
| `refs/2` | `SNOTE-IR23-3` |
| `owner` | `ROLE-IR23-ANALYSIS` |
| `audience` | `ROLE-CH24-READER` |
| `deadline` | `2026-10-02T22:00:00Z` |
| `status` | `planned-not-delivered` |
| `receiptId` | `null` |
| `executionAuthorized` | `false` |

### HOF-IR23-25

| Field | Value |
|---|---|
| `id` | `HOF-IR23-25` |
| `targetChapter` | `25` |
| `purpose` | `代替説明・仮説・未充足の問い` |
| `refs/0` | `IR23-R2` |
| `refs/1` | `IR23-R3` |
| `refs/2` | `IR23-R4` |
| `refs/3` | `IR23-R5` |
| `owner` | `ROLE-IR23-ANALYSIS` |
| `audience` | `ROLE-CH25-READER` |
| `deadline` | `2026-10-02T22:00:00Z` |
| `status` | `planned-not-delivered` |
| `receiptId` | `null` |
| `executionAuthorized` | `false` |

### HOF-IR23-26

| Field | Value |
|---|---|
| `id` | `HOF-IR23-26` |
| `targetChapter` | `26` |
| `purpose` | `判断主体・選択肢・期限` |
| `refs/0` | `DEC-IR23-001` |
| `owner` | `ROLE-IR23-ANALYSIS` |
| `audience` | `ROLE-CH26-READER` |
| `deadline` | `2026-10-02T22:00:00Z` |
| `status` | `planned-not-delivered` |
| `receiptId` | `null` |
| `executionAuthorized` | `false` |

## 失敗例と再評価

E4を回答Bindingへ加える、異版のEvidenceを使う、Cutoff後の資料を遡及して使う、Gapを削除してSatisfiedにする、未配達HandoffへReceiptを作る、といった変更は拒否する。担当を整合的に変更する、Source品質を確認済みにしても回答条件との照合までは自動充足させない、といった対比も確認する。

HOF-IR23-24/25/26は予定のままで、Receiptはnull、実行権限はfalseである。実業務の受入済み成果物や親Incidentの続報ではない。REASS-IR23-001では判断主体、期限、Source品質、対象・版・利用境界を見直す。
