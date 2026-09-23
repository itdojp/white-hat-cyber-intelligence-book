# 第19章 Incident Action Plan完全合成記入例

[第19章](../manuscript/19-incident-response.md)と[ART-25](../templates/incident-action-plan.md)の記入例である。[供給JSON](fixtures/ch19-incident-response.json)と[Schema](../schemas/ch19-incident-response.schema.json)を正本として照合する。実組織・実User・実PII・実Incidentは使わず、実操作・実通知・実収集は0件である。

## 読み方と境界

十二対比は別々の合成対象・版を使う条件付きSnapshotであり、一連の実対応履歴ではない。最初の七つは七状態の意味を、残り五つは不足や反証を示す。供給EventはOAuth同意変更とWorkload利用を模した独自形式で、製品Schemaではない。宣言基準判定、前状態、承認、保持、復旧検証も教育上の仮定であり、実受領や真正性を認定しない。

親CASE-DET-2026-001をrefinesし、章18Huntを方法参照するが、親のEvidence・権限・未配達を継承しない。各subjectは独立し、同じApp名でも対象版が異なる。四対象の08:00–09:00 UTCだけを扱い、利用可能時刻と判断時刻を区別する。App Aの確認とIdentity Cの除外には供給根拠を置き、Data DはUnknownに残す。

## 十二対比の判断

| Case | 要求 | 結果 | 判断の要点 |
|---|---|---|---|
| ICASE19-001 | Suspected | Suspected / accepted | 候補の確認を続ける。Huntの支持だけでIncidentを宣言しない。 |
| ICASE19-002 | Declared | Declared / accepted | 供給された基準判定と所有者の記録に限ってDeclaredとする。実Incidentの宣言ではない。 |
| ICASE19-003 | Contained | Contained / accepted | 供給された対象と時点に限ってContainedとする。侵害の終結ではない。 |
| ICASE19-004 | Investigating | Investigating / accepted | Investigatingとして因果と影響を問う。攻撃者を確定しない。 |
| ICASE19-005 | Recovering | Recovering / accepted | Recoveringへの条件は揃うが、復旧完了とはしない。 |
| ICASE19-006 | Closed | Closed / accepted | 供給Scopeの復旧検証と残余リスクの担当を条件にClosedとする。改善完了ではない。 |
| ICASE19-007 | Reopened | Reopened / accepted | 閉鎖後に利用可能となった新しい供給EvidenceでReopenedとする。旧閉鎖記録を消さない。 |
| ICASE19-008 | Declared | Suspected / deferred | 宣言根拠が不足するためSuspectedを維持する。 |
| ICASE19-009 | Declared | Suspected / deferred | 正当変更という代替が残り、基準は未確定のためSuspectedを維持する。 |
| ICASE19-010 | Suspected | Suspected / accepted | Log不足をUnknownとして残し、Suspectedを維持する。侵害なしとはしない。 |
| ICASE19-011 | Contained | Declared / deferred | 選択肢の記録だけではContainedに進めず、Declaredを維持する。 |
| ICASE19-012 | Closed | Recovering / deferred | 復旧検証が未確定のためRecoveringを維持する。Closedとしない。 |

## 全欄の読み方

以下はArtifactの全欄である。詳細Evidence配列は供給JSONの同じCaseのinput/evidenceにあり、ID、種別、対象版、対象、Window、利用可能時刻、供給判定を照合する。空配列とnullを完了や承認へ読み替えない。控えに書き写しても、実対応・受領の証拠にはならない。

### record

| Field | Value |
|---|---|
| `id` | `IAP-2026-019-001` |
| `artifactId` | `ART-25` |
| `caseId` | `CASE-IR-2026-001` |
| `parentCaseId` | `CASE-DET-2026-001` |
| `relation` | `refines` |
| `asOf` | `2026-09-23T00:00:00Z` |
| `timeZone` | `UTC` |
| `sourceIds/0` | `SRC-CSF-001` |
| `sourceIds/1` | `SRC-IR-001` |
| `states/0` | `Suspected` |
| `states/1` | `Declared` |
| `states/2` | `Contained` |
| `states/3` | `Investigating` |
| `states/4` | `Recovering` |
| `states/5` | `Closed` |
| `states/6` | `Reopened` |
| `decisionRequirement` | `架空OAuth Appの同意変更とWorkload利用を受け、宣言、限定Scope、選択肢、復旧と再評価をどの根拠で記録できるか。` |
| `actualIncidents` | `0` |
| `actualActions` | `0` |
| `actualNotifications` | `0` |
| `actualCollections` | `0` |

### parents

| Field | Value |
|---|---|
| `telemetryMapId` | `TCM-2026-016` |
| `telemetryRowIds/0` | `ROW-TCM16-003` |
| `telemetryRowIds/1` | `ROW-TCM16-008` |
| `telemetryHandoffId` | `HOF-TCM16-19` |
| `detectionRecordId` | `DVR-2026-017-001` |
| `detectionId` | `DET-2026-017-001` |
| `huntRecordId` | `HUNT-2026-018-001` |
| `huntCaseId` | `CASE-HUNT-2026-001` |
| `huntFindingId` | `FND-HUNT18-001` |
| `huntHandoffId` | `HOF-HUNT18-001-2` |
| `parentHandoffStatus` | `planned-not-delivered` |
| `parentReceiptId` | `null` |
| `evidenceRole` | `method-reference-not-evidence-for-new-subject` |
| `authorityTransferred` | `false` |
| `evidenceTransferred` | `false` |
| `parentHandoffReceived` | `false` |
| `parentStateChanged` | `false` |

### roles

| Field | Value |
|---|---|
| `decisionOwner` | `SYNTH-IR-DECIDER` |
| `incidentCommander` | `SYNTH-IR-COMMANDER` |
| `evidenceLead` | `SYNTH-IR-EVIDENCE` |
| `communicationOwner` | `SYNTH-IR-COMMS` |
| `recoveryOwner` | `SYNTH-IR-RECOVERY` |
| `legalPrivacyReviewer` | `SYNTH-IR-LEGAL` |

### safety

| Field | Value |
|---|---|
| `scope` | `offline-authored-json-reading-only` |
| `authority` | `自分の教材コピーを読む権限だけ。親RoEや実対応の許可ではない。` |
| `stop` | `実Data、外部接続、未知のScope、権限不明が出たら読解を停止しGapを記録する。` |
| `cleanup` | `自分の読解メモを整理するだけ。供給Evidenceと正本は書き換えない。` |
| `dataClassification` | `public-synthetic-only` |
| `personalDataIncluded` | `false` |
| `notificationAutomaticallyDetermined` | `false` |
| `receiptAuthenticityClaimed` | `false` |

### notification

| Field | Value |
|---|---|
| `questionId` | `NQ-IR19-001` |
| `question` | `対象Dataと影響、法域、契約、組織手順を誰が確認し、通知先と期限を判断するか。教材だけで要否や期限は決めない。` |
| `audiences/0` | `内部Incident担当` |
| `audiences/1` | `法務・Privacy担当` |
| `audiences/2` | `顧客担当` |
| `audiences/3` | `Vendor窓口` |
| `escalationOwner` | `SYNTH-IR-LEGAL` |
| `dueAt` | `2026-09-30T00:00:00Z` |
| `status` | `question-only-not-legal-determination` |
| `actualSent` | `false` |

### options

| Field | Value |
|---|---|
| `0/id` | `OPT-IR19-DISABLE` |
| `0/name` | `App停止案` |
| `0/security` | `当該Appの利用を抑える案。別経路の停止までは主張しない。` |
| `0/business` | `合成請求処理が停止する想定。` |
| `0/evidence` | `状態変化前の記録を保持する必要がある。` |
| `0/rollback` | `所有者の再判断と供給復旧条件の照合を要する案。実操作なし。` |
| `1/id` | `OPT-IR19-RESTRICT` |
| `1/name` | `Permission制限案` |
| `1/security` | `問題となる権限の範囲を限定する案。侵害の終結ではない。` |
| `1/business` | `合成Export機能が一時利用不能となる想定。` |
| `1/evidence` | `変更前後の権限Snapshotを別々に保持する。` |
| `1/rollback` | `再拡大は別承認と検証の対象。実操作なし。` |
| `2/id` | `OPT-IR19-MONITOR` |
| `2/name` | `Monitoring強化案` |
| `2/security` | `観測を増やす案であり、それだけでは封じ込めにならない。` |
| `2/business` | `保管量と分析負荷が増える想定。` |
| `2/evidence` | `新規観測と既存記録を区別する。取得済みとはしない。` |
| `2/rollback` | `追加観測の終了条件を別記する案。実操作なし。` |

### ICASE19-001

| Field | Value |
|---|---|
| `id` | `ICASE19-001` |
| `expected/status` | `Suspected` |
| `expected/decision` | `accepted` |
| `expected/gaps` | `[]` |
| `expected/limit` | `supplied-synthetic-record-only-not-authority-or-authenticity` |
| `expected/executionAuthorized` | `false` |
| `expected/notificationDecided` | `false` |
| `expected/noIncidentClaim` | `false` |
| `expected/improvementComplete` | `false` |
| `judgment/conclusion` | `候補の確認を続ける。Huntの支持だけでIncidentを宣言しない。` |
| `judgment/alternative` | `未記録の正当な管理変更かもしれない。` |
| `judgment/confidence` | `低` |
| `judgment/confidenceBasis` | `供給Signalだけで追加の宣言判断はない。` |
| `judgment/gap` | `業務承認文脈が不足している。` |
| `judgment/nextAction` | `宣言基準に必要な確認事項を記録する。` |
| `judgment/reassessment` | `対象、版、Scope、供給Evidence、承認、正常性、残余リスクが変わったら別Decisionで再評価する。` |
| `timelineId` | `TL-IR19-001` |
| `findingId` | `FND-IR19-001` |
| `controlId` | `CTL-IR19-001` |
| `reassessmentId` | `REA-IR19-001` |
| `handoffs/0/id` | `HOF-IR19-001-20` |
| `handoffs/0/targetChapter` | `20` |
| `handoffs/0/sourceDecisionId` | `DEC-IR19-001` |
| `handoffs/0/questionId` | `EQ-IR19-001-20` |
| `handoffs/0/plannedRecordId` | `TL-IR19-001` |
| `handoffs/0/question` | `同意変更と利用の時系列、代替説明、Unknown scopeをどの追加記録で区別できるか。` |
| `handoffs/0/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/0/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/1/id` | `HOF-IR19-001-22` |
| `handoffs/1/targetChapter` | `22` |
| `handoffs/1/sourceDecisionId` | `DEC-IR19-001` |
| `handoffs/1/questionId` | `EQ-IR19-001-22` |
| `handoffs/1/plannedRecordId` | `BKL-IR19-001` |
| `handoffs/1/question` | `残余リスクと観測GapをどのOwner、期限、検証条件で改善候補にするか。` |
| `handoffs/1/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/1/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/1/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/1/status` | `planned-not-delivered` |
| `handoffs/1/receiptId` | `null` |
| `handoffs/1/executionAuthorized` | `false` |
| `handoffs/2/id` | `HOF-IR19-001-26` |
| `handoffs/2/targetChapter` | `26` |
| `handoffs/2/sourceDecisionId` | `DEC-IR19-001` |
| `handoffs/2/questionId` | `EQ-IR19-001-26` |
| `handoffs/2/plannedRecordId` | `CTI-IR19-001` |
| `handoffs/2/question` | `限定した観測と代替説明をどの判断要求向けに再評価するか。` |
| `handoffs/2/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/2/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/2/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/2/status` | `planned-not-delivered` |
| `handoffs/2/receiptId` | `null` |
| `handoffs/2/executionAuthorized` | `false` |
| `input/context/subject` | `SYNTH-IR19-001` |
| `input/context/revision` | `REV-IR19-001` |
| `input/context/assets/0` | `SYN-APP-A` |
| `input/context/assets/1` | `SYN-APP-B` |
| `input/context/assets/2` | `SYN-ID-C` |
| `input/context/assets/3` | `SYN-DATA-D` |
| `input/context/start` | `2026-09-01T08:00:00Z` |
| `input/context/end` | `2026-09-01T09:00:00Z` |
| `input/previous/id` | `DEC-IR19-001-PREV` |
| `input/previous/status` | `Suspected` |
| `input/previous/at` | `2026-09-01T10:10:00Z` |
| `input/previous/owner` | `SYNTH-IR-DECIDER` |
| `input/previous/reason` | `供給された前提判断。真正性を示す受領記録ではない。` |
| `input/previous/closureValidationId` | `null` |
| `input/previous/closure` | `null` |
| `input/decision/id` | `DEC-IR19-001` |
| `input/decision/requested` | `Suspected` |
| `input/decision/at` | `2026-09-01T11:00:00Z` |
| `input/decision/owner` | `SYNTH-IR-DECIDER` |
| `input/decision/reason` | `供給記録と対象Scopeに限った教育上の判断。` |
| `input/classification` | `suspected-policy-violation` |
| `input/severity` | `medium` |
| `input/priority` | `urgent` |
| `input/scope/hypothesized/0` | `SYN-APP-B` |
| `input/scope/confirmed/0` | `SYN-APP-A` |
| `input/scope/excluded/0` | `SYN-ID-C` |
| `input/scope/unknown/0` | `SYN-DATA-D` |
| `input/declaration` | `null` |
| `input/preservation/id` | `PRV-IR19-001` |
| `input/preservation/owner` | `SYNTH-IR-EVIDENCE` |
| `input/preservation/at` | `2026-09-01T09:25:00Z` |
| `input/preservation/evidenceId` | `EV-IR19-001-SAVE` |
| `input/containment` | `null` |
| `input/analysisId` | `null` |
| `input/recovery` | `null` |
| `input/closure` | `null` |
| `input/reopening` | `null` |
| `input/incidentId` | `INC-IR19-001` |
| `input/threatQuestionId` | `THQ-IR19-001` |
| `input/evidenceQuestion` | `同意変更とWorkload利用の対応を、正当変更・誤設定・侵害仮説からどう区別するか。` |
| `input/collectionGap` | `Data Dの影響は未観測。実収集、原記録の真正性、全組織の範囲は未評価。` |
| `input/classificationBasis` | `供給候補の種類であり、悪意や原因の確定ではない。` |
| `input/severityBasis` | `合成Export機能への限定影響を想定する。Severityは確信度ではない。` |
| `input/priorityBasis` | `次の判断に必要な情報を先に確認する教育上の優先度。実対応の指示ではない。` |
| `input/eradicationQuestion` | `残る権限と再発条件をどのScopeで確認するか。根絶完了は未認定。実操作なし。` |

### ICASE19-002

| Field | Value |
|---|---|
| `id` | `ICASE19-002` |
| `expected/status` | `Declared` |
| `expected/decision` | `accepted` |
| `expected/gaps` | `[]` |
| `expected/limit` | `supplied-synthetic-record-only-not-authority-or-authenticity` |
| `expected/executionAuthorized` | `false` |
| `expected/notificationDecided` | `false` |
| `expected/noIncidentClaim` | `false` |
| `expected/improvementComplete` | `false` |
| `judgment/conclusion` | `供給された基準判定と所有者の記録に限ってDeclaredとする。実Incidentの宣言ではない。` |
| `judgment/alternative` | `誤設定や承認記録不足という説明を残す。` |
| `judgment/confidence` | `中` |
| `judgment/confidenceBasis` | `宣言記録はあるが、組織全体の影響は分からない。` |
| `judgment/gap` | `未観測Dataの影響はUnknownのままである。` |
| `judgment/nextAction` | `Evidence Questionと合成選択肢の比較へ進む。` |
| `judgment/reassessment` | `対象、版、Scope、供給Evidence、承認、正常性、残余リスクが変わったら別Decisionで再評価する。` |
| `timelineId` | `TL-IR19-002` |
| `findingId` | `FND-IR19-002` |
| `controlId` | `CTL-IR19-002` |
| `reassessmentId` | `REA-IR19-002` |
| `handoffs/0/id` | `HOF-IR19-002-20` |
| `handoffs/0/targetChapter` | `20` |
| `handoffs/0/sourceDecisionId` | `DEC-IR19-002` |
| `handoffs/0/questionId` | `EQ-IR19-002-20` |
| `handoffs/0/plannedRecordId` | `TL-IR19-002` |
| `handoffs/0/question` | `同意変更と利用の時系列、代替説明、Unknown scopeをどの追加記録で区別できるか。` |
| `handoffs/0/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/0/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/1/id` | `HOF-IR19-002-22` |
| `handoffs/1/targetChapter` | `22` |
| `handoffs/1/sourceDecisionId` | `DEC-IR19-002` |
| `handoffs/1/questionId` | `EQ-IR19-002-22` |
| `handoffs/1/plannedRecordId` | `BKL-IR19-002` |
| `handoffs/1/question` | `残余リスクと観測GapをどのOwner、期限、検証条件で改善候補にするか。` |
| `handoffs/1/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/1/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/1/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/1/status` | `planned-not-delivered` |
| `handoffs/1/receiptId` | `null` |
| `handoffs/1/executionAuthorized` | `false` |
| `handoffs/2/id` | `HOF-IR19-002-26` |
| `handoffs/2/targetChapter` | `26` |
| `handoffs/2/sourceDecisionId` | `DEC-IR19-002` |
| `handoffs/2/questionId` | `EQ-IR19-002-26` |
| `handoffs/2/plannedRecordId` | `CTI-IR19-002` |
| `handoffs/2/question` | `限定した観測と代替説明をどの判断要求向けに再評価するか。` |
| `handoffs/2/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/2/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/2/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/2/status` | `planned-not-delivered` |
| `handoffs/2/receiptId` | `null` |
| `handoffs/2/executionAuthorized` | `false` |
| `input/context/subject` | `SYNTH-IR19-002` |
| `input/context/revision` | `REV-IR19-002` |
| `input/context/assets/0` | `SYN-APP-A` |
| `input/context/assets/1` | `SYN-APP-B` |
| `input/context/assets/2` | `SYN-ID-C` |
| `input/context/assets/3` | `SYN-DATA-D` |
| `input/context/start` | `2026-09-01T08:00:00Z` |
| `input/context/end` | `2026-09-01T09:00:00Z` |
| `input/previous/id` | `DEC-IR19-002-PREV` |
| `input/previous/status` | `Suspected` |
| `input/previous/at` | `2026-09-01T10:10:00Z` |
| `input/previous/owner` | `SYNTH-IR-DECIDER` |
| `input/previous/reason` | `供給された前提判断。真正性を示す受領記録ではない。` |
| `input/previous/closureValidationId` | `null` |
| `input/previous/closure` | `null` |
| `input/decision/id` | `DEC-IR19-002` |
| `input/decision/requested` | `Declared` |
| `input/decision/at` | `2026-09-01T11:00:00Z` |
| `input/decision/owner` | `SYNTH-IR-DECIDER` |
| `input/decision/reason` | `供給記録と対象Scopeに限った教育上の判断。` |
| `input/classification` | `suspected-policy-violation` |
| `input/severity` | `medium` |
| `input/priority` | `urgent` |
| `input/scope/hypothesized/0` | `SYN-APP-B` |
| `input/scope/confirmed/0` | `SYN-APP-A` |
| `input/scope/excluded/0` | `SYN-ID-C` |
| `input/scope/unknown/0` | `SYN-DATA-D` |
| `input/declaration/id` | `DCL-IR19-002` |
| `input/declaration/owner` | `SYNTH-IR-DECIDER` |
| `input/declaration/reason` | `供給した教育用基準では、承認未確認の権限変化と利用の組が個別確認対象となる。` |
| `input/declaration/at` | `2026-09-01T09:15:00Z` |
| `input/declaration/criteriaId` | `EV-IR19-002-CRITERIA` |
| `input/declaration/asset` | `SYN-APP-A` |
| `input/preservation/id` | `PRV-IR19-002` |
| `input/preservation/owner` | `SYNTH-IR-EVIDENCE` |
| `input/preservation/at` | `2026-09-01T09:25:00Z` |
| `input/preservation/evidenceId` | `EV-IR19-002-SAVE` |
| `input/containment` | `null` |
| `input/analysisId` | `null` |
| `input/recovery` | `null` |
| `input/closure` | `null` |
| `input/reopening` | `null` |
| `input/incidentId` | `INC-IR19-002` |
| `input/threatQuestionId` | `THQ-IR19-002` |
| `input/evidenceQuestion` | `同意変更とWorkload利用の対応を、正当変更・誤設定・侵害仮説からどう区別するか。` |
| `input/collectionGap` | `Data Dの影響は未観測。実収集、原記録の真正性、全組織の範囲は未評価。` |
| `input/classificationBasis` | `供給候補の種類であり、悪意や原因の確定ではない。` |
| `input/severityBasis` | `合成Export機能への限定影響を想定する。Severityは確信度ではない。` |
| `input/priorityBasis` | `次の判断に必要な情報を先に確認する教育上の優先度。実対応の指示ではない。` |
| `input/eradicationQuestion` | `残る権限と再発条件をどのScopeで確認するか。根絶完了は未認定。実操作なし。` |

### ICASE19-003

| Field | Value |
|---|---|
| `id` | `ICASE19-003` |
| `expected/status` | `Contained` |
| `expected/decision` | `accepted` |
| `expected/gaps` | `[]` |
| `expected/limit` | `supplied-synthetic-record-only-not-authority-or-authenticity` |
| `expected/executionAuthorized` | `false` |
| `expected/notificationDecided` | `false` |
| `expected/noIncidentClaim` | `false` |
| `expected/improvementComplete` | `false` |
| `judgment/conclusion` | `供給された対象と時点に限ってContainedとする。侵害の終結ではない。` |
| `judgment/alternative` | `別経路の影響が残る可能性がある。` |
| `judgment/confidence` | `中` |
| `judgment/confidenceBasis` | `事前保持と合成承認、限定した検証記録が揃う。` |
| `judgment/gap` | `未知の対象には封じ込め効果を拡張できない。` |
| `judgment/nextAction` | `調査継続と切戻し条件を別々に記録する。` |
| `judgment/reassessment` | `対象、版、Scope、供給Evidence、承認、正常性、残余リスクが変わったら別Decisionで再評価する。` |
| `timelineId` | `TL-IR19-003` |
| `findingId` | `FND-IR19-003` |
| `controlId` | `CTL-IR19-003` |
| `reassessmentId` | `REA-IR19-003` |
| `handoffs/0/id` | `HOF-IR19-003-20` |
| `handoffs/0/targetChapter` | `20` |
| `handoffs/0/sourceDecisionId` | `DEC-IR19-003` |
| `handoffs/0/questionId` | `EQ-IR19-003-20` |
| `handoffs/0/plannedRecordId` | `TL-IR19-003` |
| `handoffs/0/question` | `同意変更と利用の時系列、代替説明、Unknown scopeをどの追加記録で区別できるか。` |
| `handoffs/0/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/0/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/1/id` | `HOF-IR19-003-22` |
| `handoffs/1/targetChapter` | `22` |
| `handoffs/1/sourceDecisionId` | `DEC-IR19-003` |
| `handoffs/1/questionId` | `EQ-IR19-003-22` |
| `handoffs/1/plannedRecordId` | `BKL-IR19-003` |
| `handoffs/1/question` | `残余リスクと観測GapをどのOwner、期限、検証条件で改善候補にするか。` |
| `handoffs/1/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/1/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/1/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/1/status` | `planned-not-delivered` |
| `handoffs/1/receiptId` | `null` |
| `handoffs/1/executionAuthorized` | `false` |
| `handoffs/2/id` | `HOF-IR19-003-26` |
| `handoffs/2/targetChapter` | `26` |
| `handoffs/2/sourceDecisionId` | `DEC-IR19-003` |
| `handoffs/2/questionId` | `EQ-IR19-003-26` |
| `handoffs/2/plannedRecordId` | `CTI-IR19-003` |
| `handoffs/2/question` | `限定した観測と代替説明をどの判断要求向けに再評価するか。` |
| `handoffs/2/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/2/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/2/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/2/status` | `planned-not-delivered` |
| `handoffs/2/receiptId` | `null` |
| `handoffs/2/executionAuthorized` | `false` |
| `input/context/subject` | `SYNTH-IR19-003` |
| `input/context/revision` | `REV-IR19-003` |
| `input/context/assets/0` | `SYN-APP-A` |
| `input/context/assets/1` | `SYN-APP-B` |
| `input/context/assets/2` | `SYN-ID-C` |
| `input/context/assets/3` | `SYN-DATA-D` |
| `input/context/start` | `2026-09-01T08:00:00Z` |
| `input/context/end` | `2026-09-01T09:00:00Z` |
| `input/previous/id` | `DEC-IR19-003-PREV` |
| `input/previous/status` | `Declared` |
| `input/previous/at` | `2026-09-01T10:10:00Z` |
| `input/previous/owner` | `SYNTH-IR-DECIDER` |
| `input/previous/reason` | `供給された前提判断。真正性を示す受領記録ではない。` |
| `input/previous/closureValidationId` | `null` |
| `input/previous/closure` | `null` |
| `input/decision/id` | `DEC-IR19-003` |
| `input/decision/requested` | `Contained` |
| `input/decision/at` | `2026-09-01T11:00:00Z` |
| `input/decision/owner` | `SYNTH-IR-DECIDER` |
| `input/decision/reason` | `供給記録と対象Scopeに限った教育上の判断。` |
| `input/classification` | `suspected-policy-violation` |
| `input/severity` | `medium` |
| `input/priority` | `urgent` |
| `input/scope/hypothesized/0` | `SYN-APP-B` |
| `input/scope/confirmed/0` | `SYN-APP-A` |
| `input/scope/excluded/0` | `SYN-ID-C` |
| `input/scope/unknown/0` | `SYN-DATA-D` |
| `input/declaration/id` | `DCL-IR19-003` |
| `input/declaration/owner` | `SYNTH-IR-DECIDER` |
| `input/declaration/reason` | `供給した教育用基準では、承認未確認の権限変化と利用の組が個別確認対象となる。` |
| `input/declaration/at` | `2026-09-01T09:15:00Z` |
| `input/declaration/criteriaId` | `EV-IR19-003-CRITERIA` |
| `input/declaration/asset` | `SYN-APP-A` |
| `input/preservation/id` | `PRV-IR19-003` |
| `input/preservation/owner` | `SYNTH-IR-EVIDENCE` |
| `input/preservation/at` | `2026-09-01T09:25:00Z` |
| `input/preservation/evidenceId` | `EV-IR19-003-SAVE` |
| `input/containment/id` | `ACT-IR19-003` |
| `input/containment/optionId` | `OPT-IR19-RESTRICT` |
| `input/containment/asset` | `SYN-APP-A` |
| `input/containment/at` | `2026-09-01T10:15:00Z` |
| `input/containment/expectedImpact` | `合成Export機能が一時利用不能となる想定。` |
| `input/containment/rollback` | `再拡大は別承認と検証の対象。実操作なし。` |
| `input/containment/destructive` | `false` |
| `input/containment/actualExecuted` | `false` |
| `input/containment/validationId` | `EV-IR19-003-CONTAIN` |
| `input/containment/authority/id` | `AUTH-IR19-003` |
| `input/containment/authority/approved` | `true` |
| `input/containment/authority/owner` | `SYNTH-IR-COMMANDER` |
| `input/containment/authority/approvedAt` | `2026-09-01T10:12:00Z` |
| `input/containment/authority/expiresAt` | `2026-09-01T10:45:00Z` |
| `input/containment/authority/subject` | `SYNTH-IR19-003` |
| `input/containment/authority/revision` | `REV-IR19-003` |
| `input/containment/authority/asset` | `SYN-APP-A` |
| `input/containment/authority/realAuthority` | `false` |
| `input/analysisId` | `null` |
| `input/recovery` | `null` |
| `input/closure` | `null` |
| `input/reopening` | `null` |
| `input/incidentId` | `INC-IR19-003` |
| `input/threatQuestionId` | `THQ-IR19-003` |
| `input/evidenceQuestion` | `同意変更とWorkload利用の対応を、正当変更・誤設定・侵害仮説からどう区別するか。` |
| `input/collectionGap` | `Data Dの影響は未観測。実収集、原記録の真正性、全組織の範囲は未評価。` |
| `input/classificationBasis` | `供給候補の種類であり、悪意や原因の確定ではない。` |
| `input/severityBasis` | `合成Export機能への限定影響を想定する。Severityは確信度ではない。` |
| `input/priorityBasis` | `次の判断に必要な情報を先に確認する教育上の優先度。実対応の指示ではない。` |
| `input/eradicationQuestion` | `残る権限と再発条件をどのScopeで確認するか。根絶完了は未認定。実操作なし。` |

### ICASE19-004

| Field | Value |
|---|---|
| `id` | `ICASE19-004` |
| `expected/status` | `Investigating` |
| `expected/decision` | `accepted` |
| `expected/gaps` | `[]` |
| `expected/limit` | `supplied-synthetic-record-only-not-authority-or-authenticity` |
| `expected/executionAuthorized` | `false` |
| `expected/notificationDecided` | `false` |
| `expected/noIncidentClaim` | `false` |
| `expected/improvementComplete` | `false` |
| `judgment/conclusion` | `Investigatingとして因果と影響を問う。攻撃者を確定しない。` |
| `judgment/alternative` | `正当な変更と誤設定も比較対象に残す。` |
| `judgment/confidence` | `低` |
| `judgment/confidenceBasis` | `分析対象は供給記録に限定される。` |
| `judgment/gap` | `Root causeと全影響はまだ確定していない。` |
| `judgment/nextAction` | `第20章向けEvidence Questionを未配達で記録する。` |
| `judgment/reassessment` | `対象、版、Scope、供給Evidence、承認、正常性、残余リスクが変わったら別Decisionで再評価する。` |
| `timelineId` | `TL-IR19-004` |
| `findingId` | `FND-IR19-004` |
| `controlId` | `CTL-IR19-004` |
| `reassessmentId` | `REA-IR19-004` |
| `handoffs/0/id` | `HOF-IR19-004-20` |
| `handoffs/0/targetChapter` | `20` |
| `handoffs/0/sourceDecisionId` | `DEC-IR19-004` |
| `handoffs/0/questionId` | `EQ-IR19-004-20` |
| `handoffs/0/plannedRecordId` | `TL-IR19-004` |
| `handoffs/0/question` | `同意変更と利用の時系列、代替説明、Unknown scopeをどの追加記録で区別できるか。` |
| `handoffs/0/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/0/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/1/id` | `HOF-IR19-004-22` |
| `handoffs/1/targetChapter` | `22` |
| `handoffs/1/sourceDecisionId` | `DEC-IR19-004` |
| `handoffs/1/questionId` | `EQ-IR19-004-22` |
| `handoffs/1/plannedRecordId` | `BKL-IR19-004` |
| `handoffs/1/question` | `残余リスクと観測GapをどのOwner、期限、検証条件で改善候補にするか。` |
| `handoffs/1/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/1/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/1/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/1/status` | `planned-not-delivered` |
| `handoffs/1/receiptId` | `null` |
| `handoffs/1/executionAuthorized` | `false` |
| `handoffs/2/id` | `HOF-IR19-004-26` |
| `handoffs/2/targetChapter` | `26` |
| `handoffs/2/sourceDecisionId` | `DEC-IR19-004` |
| `handoffs/2/questionId` | `EQ-IR19-004-26` |
| `handoffs/2/plannedRecordId` | `CTI-IR19-004` |
| `handoffs/2/question` | `限定した観測と代替説明をどの判断要求向けに再評価するか。` |
| `handoffs/2/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/2/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/2/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/2/status` | `planned-not-delivered` |
| `handoffs/2/receiptId` | `null` |
| `handoffs/2/executionAuthorized` | `false` |
| `input/context/subject` | `SYNTH-IR19-004` |
| `input/context/revision` | `REV-IR19-004` |
| `input/context/assets/0` | `SYN-APP-A` |
| `input/context/assets/1` | `SYN-APP-B` |
| `input/context/assets/2` | `SYN-ID-C` |
| `input/context/assets/3` | `SYN-DATA-D` |
| `input/context/start` | `2026-09-01T08:00:00Z` |
| `input/context/end` | `2026-09-01T09:00:00Z` |
| `input/previous/id` | `DEC-IR19-004-PREV` |
| `input/previous/status` | `Contained` |
| `input/previous/at` | `2026-09-01T10:10:00Z` |
| `input/previous/owner` | `SYNTH-IR-DECIDER` |
| `input/previous/reason` | `供給された前提判断。真正性を示す受領記録ではない。` |
| `input/previous/closureValidationId` | `null` |
| `input/previous/closure` | `null` |
| `input/decision/id` | `DEC-IR19-004` |
| `input/decision/requested` | `Investigating` |
| `input/decision/at` | `2026-09-01T11:00:00Z` |
| `input/decision/owner` | `SYNTH-IR-DECIDER` |
| `input/decision/reason` | `供給記録と対象Scopeに限った教育上の判断。` |
| `input/classification` | `suspected-policy-violation` |
| `input/severity` | `medium` |
| `input/priority` | `urgent` |
| `input/scope/hypothesized/0` | `SYN-APP-B` |
| `input/scope/confirmed/0` | `SYN-APP-A` |
| `input/scope/excluded/0` | `SYN-ID-C` |
| `input/scope/unknown/0` | `SYN-DATA-D` |
| `input/declaration/id` | `DCL-IR19-004` |
| `input/declaration/owner` | `SYNTH-IR-DECIDER` |
| `input/declaration/reason` | `供給した教育用基準では、承認未確認の権限変化と利用の組が個別確認対象となる。` |
| `input/declaration/at` | `2026-09-01T09:15:00Z` |
| `input/declaration/criteriaId` | `EV-IR19-004-CRITERIA` |
| `input/declaration/asset` | `SYN-APP-A` |
| `input/preservation/id` | `PRV-IR19-004` |
| `input/preservation/owner` | `SYNTH-IR-EVIDENCE` |
| `input/preservation/at` | `2026-09-01T09:25:00Z` |
| `input/preservation/evidenceId` | `EV-IR19-004-SAVE` |
| `input/containment` | `null` |
| `input/analysisId` | `EV-IR19-004-ANALYSIS` |
| `input/recovery` | `null` |
| `input/closure` | `null` |
| `input/reopening` | `null` |
| `input/incidentId` | `INC-IR19-004` |
| `input/threatQuestionId` | `THQ-IR19-004` |
| `input/evidenceQuestion` | `同意変更とWorkload利用の対応を、正当変更・誤設定・侵害仮説からどう区別するか。` |
| `input/collectionGap` | `Data Dの影響は未観測。実収集、原記録の真正性、全組織の範囲は未評価。` |
| `input/classificationBasis` | `供給候補の種類であり、悪意や原因の確定ではない。` |
| `input/severityBasis` | `合成Export機能への限定影響を想定する。Severityは確信度ではない。` |
| `input/priorityBasis` | `次の判断に必要な情報を先に確認する教育上の優先度。実対応の指示ではない。` |
| `input/eradicationQuestion` | `残る権限と再発条件をどのScopeで確認するか。根絶完了は未認定。実操作なし。` |

### ICASE19-005

| Field | Value |
|---|---|
| `id` | `ICASE19-005` |
| `expected/status` | `Recovering` |
| `expected/decision` | `accepted` |
| `expected/gaps` | `[]` |
| `expected/limit` | `supplied-synthetic-record-only-not-authority-or-authenticity` |
| `expected/executionAuthorized` | `false` |
| `expected/notificationDecided` | `false` |
| `expected/noIncidentClaim` | `false` |
| `expected/improvementComplete` | `false` |
| `judgment/conclusion` | `Recoveringへの条件は揃うが、復旧完了とはしない。` |
| `judgment/alternative` | `復旧条件の見落としが残る可能性がある。` |
| `judgment/confidence` | `中` |
| `judgment/confidenceBasis` | `入口の基準判定と担当者だけを供給した。` |
| `judgment/gap` | `サービス正常性の別検証が必要である。` |
| `judgment/nextAction` | `Validationと残余リスクの判定を計画する。` |
| `judgment/reassessment` | `対象、版、Scope、供給Evidence、承認、正常性、残余リスクが変わったら別Decisionで再評価する。` |
| `timelineId` | `TL-IR19-005` |
| `findingId` | `FND-IR19-005` |
| `controlId` | `CTL-IR19-005` |
| `reassessmentId` | `REA-IR19-005` |
| `handoffs/0/id` | `HOF-IR19-005-20` |
| `handoffs/0/targetChapter` | `20` |
| `handoffs/0/sourceDecisionId` | `DEC-IR19-005` |
| `handoffs/0/questionId` | `EQ-IR19-005-20` |
| `handoffs/0/plannedRecordId` | `TL-IR19-005` |
| `handoffs/0/question` | `同意変更と利用の時系列、代替説明、Unknown scopeをどの追加記録で区別できるか。` |
| `handoffs/0/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/0/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/1/id` | `HOF-IR19-005-22` |
| `handoffs/1/targetChapter` | `22` |
| `handoffs/1/sourceDecisionId` | `DEC-IR19-005` |
| `handoffs/1/questionId` | `EQ-IR19-005-22` |
| `handoffs/1/plannedRecordId` | `BKL-IR19-005` |
| `handoffs/1/question` | `残余リスクと観測GapをどのOwner、期限、検証条件で改善候補にするか。` |
| `handoffs/1/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/1/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/1/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/1/status` | `planned-not-delivered` |
| `handoffs/1/receiptId` | `null` |
| `handoffs/1/executionAuthorized` | `false` |
| `handoffs/2/id` | `HOF-IR19-005-26` |
| `handoffs/2/targetChapter` | `26` |
| `handoffs/2/sourceDecisionId` | `DEC-IR19-005` |
| `handoffs/2/questionId` | `EQ-IR19-005-26` |
| `handoffs/2/plannedRecordId` | `CTI-IR19-005` |
| `handoffs/2/question` | `限定した観測と代替説明をどの判断要求向けに再評価するか。` |
| `handoffs/2/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/2/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/2/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/2/status` | `planned-not-delivered` |
| `handoffs/2/receiptId` | `null` |
| `handoffs/2/executionAuthorized` | `false` |
| `input/context/subject` | `SYNTH-IR19-005` |
| `input/context/revision` | `REV-IR19-005` |
| `input/context/assets/0` | `SYN-APP-A` |
| `input/context/assets/1` | `SYN-APP-B` |
| `input/context/assets/2` | `SYN-ID-C` |
| `input/context/assets/3` | `SYN-DATA-D` |
| `input/context/start` | `2026-09-01T08:00:00Z` |
| `input/context/end` | `2026-09-01T09:00:00Z` |
| `input/previous/id` | `DEC-IR19-005-PREV` |
| `input/previous/status` | `Investigating` |
| `input/previous/at` | `2026-09-01T10:10:00Z` |
| `input/previous/owner` | `SYNTH-IR-DECIDER` |
| `input/previous/reason` | `供給された前提判断。真正性を示す受領記録ではない。` |
| `input/previous/closureValidationId` | `null` |
| `input/previous/closure` | `null` |
| `input/decision/id` | `DEC-IR19-005` |
| `input/decision/requested` | `Recovering` |
| `input/decision/at` | `2026-09-01T11:00:00Z` |
| `input/decision/owner` | `SYNTH-IR-DECIDER` |
| `input/decision/reason` | `供給記録と対象Scopeに限った教育上の判断。` |
| `input/classification` | `suspected-policy-violation` |
| `input/severity` | `medium` |
| `input/priority` | `urgent` |
| `input/scope/hypothesized/0` | `SYN-APP-B` |
| `input/scope/confirmed/0` | `SYN-APP-A` |
| `input/scope/excluded/0` | `SYN-ID-C` |
| `input/scope/unknown/0` | `SYN-DATA-D` |
| `input/declaration/id` | `DCL-IR19-005` |
| `input/declaration/owner` | `SYNTH-IR-DECIDER` |
| `input/declaration/reason` | `供給した教育用基準では、承認未確認の権限変化と利用の組が個別確認対象となる。` |
| `input/declaration/at` | `2026-09-01T09:15:00Z` |
| `input/declaration/criteriaId` | `EV-IR19-005-CRITERIA` |
| `input/declaration/asset` | `SYN-APP-A` |
| `input/preservation/id` | `PRV-IR19-005` |
| `input/preservation/owner` | `SYNTH-IR-EVIDENCE` |
| `input/preservation/at` | `2026-09-01T09:25:00Z` |
| `input/preservation/evidenceId` | `EV-IR19-005-SAVE` |
| `input/containment` | `null` |
| `input/analysisId` | `null` |
| `input/recovery/id` | `REC-IR19-005` |
| `input/recovery/owner` | `SYNTH-IR-RECOVERY` |
| `input/recovery/criteriaId` | `EV-IR19-005-RECENTRY` |
| `input/recovery/validationId` | `EV-IR19-005-RECVALID` |
| `input/recovery/asset` | `SYN-APP-A` |
| `input/closure` | `null` |
| `input/reopening` | `null` |
| `input/incidentId` | `INC-IR19-005` |
| `input/threatQuestionId` | `THQ-IR19-005` |
| `input/evidenceQuestion` | `同意変更とWorkload利用の対応を、正当変更・誤設定・侵害仮説からどう区別するか。` |
| `input/collectionGap` | `Data Dの影響は未観測。実収集、原記録の真正性、全組織の範囲は未評価。` |
| `input/classificationBasis` | `供給候補の種類であり、悪意や原因の確定ではない。` |
| `input/severityBasis` | `合成Export機能への限定影響を想定する。Severityは確信度ではない。` |
| `input/priorityBasis` | `次の判断に必要な情報を先に確認する教育上の優先度。実対応の指示ではない。` |
| `input/eradicationQuestion` | `残る権限と再発条件をどのScopeで確認するか。根絶完了は未認定。実操作なし。` |

### ICASE19-006

| Field | Value |
|---|---|
| `id` | `ICASE19-006` |
| `expected/status` | `Closed` |
| `expected/decision` | `accepted` |
| `expected/gaps` | `[]` |
| `expected/limit` | `supplied-synthetic-record-only-not-authority-or-authenticity` |
| `expected/executionAuthorized` | `false` |
| `expected/notificationDecided` | `false` |
| `expected/noIncidentClaim` | `false` |
| `expected/improvementComplete` | `false` |
| `judgment/conclusion` | `供給Scopeの復旧検証と残余リスクの担当を条件にClosedとする。改善完了ではない。` |
| `judgment/alternative` | `未観測範囲や再発要因が残る可能性がある。` |
| `judgment/confidence` | `中` |
| `judgment/confidenceBasis` | `限定した復旧結果と閉鎖判断を供給した。` |
| `judgment/gap` | `組織全体の安全と再発防止完了は未評価である。` |
| `judgment/nextAction` | `残余リスクと改善Backlogを別期限で追跡する。` |
| `judgment/reassessment` | `対象、版、Scope、供給Evidence、承認、正常性、残余リスクが変わったら別Decisionで再評価する。` |
| `timelineId` | `TL-IR19-006` |
| `findingId` | `FND-IR19-006` |
| `controlId` | `CTL-IR19-006` |
| `reassessmentId` | `REA-IR19-006` |
| `handoffs/0/id` | `HOF-IR19-006-20` |
| `handoffs/0/targetChapter` | `20` |
| `handoffs/0/sourceDecisionId` | `DEC-IR19-006` |
| `handoffs/0/questionId` | `EQ-IR19-006-20` |
| `handoffs/0/plannedRecordId` | `TL-IR19-006` |
| `handoffs/0/question` | `同意変更と利用の時系列、代替説明、Unknown scopeをどの追加記録で区別できるか。` |
| `handoffs/0/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/0/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/1/id` | `HOF-IR19-006-22` |
| `handoffs/1/targetChapter` | `22` |
| `handoffs/1/sourceDecisionId` | `DEC-IR19-006` |
| `handoffs/1/questionId` | `EQ-IR19-006-22` |
| `handoffs/1/plannedRecordId` | `BKL-IR19-006` |
| `handoffs/1/question` | `残余リスクと観測GapをどのOwner、期限、検証条件で改善候補にするか。` |
| `handoffs/1/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/1/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/1/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/1/status` | `planned-not-delivered` |
| `handoffs/1/receiptId` | `null` |
| `handoffs/1/executionAuthorized` | `false` |
| `handoffs/2/id` | `HOF-IR19-006-26` |
| `handoffs/2/targetChapter` | `26` |
| `handoffs/2/sourceDecisionId` | `DEC-IR19-006` |
| `handoffs/2/questionId` | `EQ-IR19-006-26` |
| `handoffs/2/plannedRecordId` | `CTI-IR19-006` |
| `handoffs/2/question` | `限定した観測と代替説明をどの判断要求向けに再評価するか。` |
| `handoffs/2/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/2/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/2/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/2/status` | `planned-not-delivered` |
| `handoffs/2/receiptId` | `null` |
| `handoffs/2/executionAuthorized` | `false` |
| `input/context/subject` | `SYNTH-IR19-006` |
| `input/context/revision` | `REV-IR19-006` |
| `input/context/assets/0` | `SYN-APP-A` |
| `input/context/assets/1` | `SYN-APP-B` |
| `input/context/assets/2` | `SYN-ID-C` |
| `input/context/assets/3` | `SYN-DATA-D` |
| `input/context/start` | `2026-09-01T08:00:00Z` |
| `input/context/end` | `2026-09-01T09:00:00Z` |
| `input/previous/id` | `DEC-IR19-006-PREV` |
| `input/previous/status` | `Recovering` |
| `input/previous/at` | `2026-09-01T10:10:00Z` |
| `input/previous/owner` | `SYNTH-IR-DECIDER` |
| `input/previous/reason` | `供給された前提判断。真正性を示す受領記録ではない。` |
| `input/previous/closureValidationId` | `null` |
| `input/previous/closure` | `null` |
| `input/decision/id` | `DEC-IR19-006` |
| `input/decision/requested` | `Closed` |
| `input/decision/at` | `2026-09-01T11:00:00Z` |
| `input/decision/owner` | `SYNTH-IR-DECIDER` |
| `input/decision/reason` | `供給記録と対象Scopeに限った教育上の判断。` |
| `input/classification` | `suspected-policy-violation` |
| `input/severity` | `medium` |
| `input/priority` | `urgent` |
| `input/scope/hypothesized/0` | `SYN-APP-B` |
| `input/scope/confirmed/0` | `SYN-APP-A` |
| `input/scope/excluded/0` | `SYN-ID-C` |
| `input/scope/unknown/0` | `SYN-DATA-D` |
| `input/declaration/id` | `DCL-IR19-006` |
| `input/declaration/owner` | `SYNTH-IR-DECIDER` |
| `input/declaration/reason` | `供給した教育用基準では、承認未確認の権限変化と利用の組が個別確認対象となる。` |
| `input/declaration/at` | `2026-09-01T09:15:00Z` |
| `input/declaration/criteriaId` | `EV-IR19-006-CRITERIA` |
| `input/declaration/asset` | `SYN-APP-A` |
| `input/preservation/id` | `PRV-IR19-006` |
| `input/preservation/owner` | `SYNTH-IR-EVIDENCE` |
| `input/preservation/at` | `2026-09-01T09:25:00Z` |
| `input/preservation/evidenceId` | `EV-IR19-006-SAVE` |
| `input/containment` | `null` |
| `input/analysisId` | `null` |
| `input/recovery/id` | `REC-IR19-006` |
| `input/recovery/owner` | `SYNTH-IR-RECOVERY` |
| `input/recovery/criteriaId` | `EV-IR19-006-RECENTRY` |
| `input/recovery/validationId` | `EV-IR19-006-RECVALID` |
| `input/recovery/asset` | `SYN-APP-A` |
| `input/closure/owner` | `SYNTH-IR-DECIDER` |
| `input/closure/at` | `2026-09-01T11:00:00Z` |
| `input/closure/residualRisk` | `未観測Dataの影響と再発要因は別担当が追跡する。` |
| `input/closure/riskOwner` | `SYNTH-IR-RISK` |
| `input/closure/dueAt` | `2026-09-30T00:00:00Z` |
| `input/closure/asset` | `SYN-APP-A` |
| `input/reopening` | `null` |
| `input/incidentId` | `INC-IR19-006` |
| `input/threatQuestionId` | `THQ-IR19-006` |
| `input/evidenceQuestion` | `同意変更とWorkload利用の対応を、正当変更・誤設定・侵害仮説からどう区別するか。` |
| `input/collectionGap` | `Data Dの影響は未観測。実収集、原記録の真正性、全組織の範囲は未評価。` |
| `input/classificationBasis` | `供給候補の種類であり、悪意や原因の確定ではない。` |
| `input/severityBasis` | `合成Export機能への限定影響を想定する。Severityは確信度ではない。` |
| `input/priorityBasis` | `次の判断に必要な情報を先に確認する教育上の優先度。実対応の指示ではない。` |
| `input/eradicationQuestion` | `残る権限と再発条件をどのScopeで確認するか。根絶完了は未認定。実操作なし。` |

### ICASE19-007

| Field | Value |
|---|---|
| `id` | `ICASE19-007` |
| `expected/status` | `Reopened` |
| `expected/decision` | `accepted` |
| `expected/gaps` | `[]` |
| `expected/limit` | `supplied-synthetic-record-only-not-authority-or-authenticity` |
| `expected/executionAuthorized` | `false` |
| `expected/notificationDecided` | `false` |
| `expected/noIncidentClaim` | `false` |
| `expected/improvementComplete` | `false` |
| `judgment/conclusion` | `閉鎖後に利用可能となった新しい供給EvidenceでReopenedとする。旧閉鎖記録を消さない。` |
| `judgment/alternative` | `新しい記録が既知事象の遅延情報かもしれない。` |
| `judgment/confidence` | `低` |
| `judgment/confidenceBasis` | `再開理由はあるが新情報の全影響は未分析である。` |
| `judgment/gap` | `新しいEvidenceの解釈を再検討する必要がある。` |
| `judgment/nextAction` | `旧Decision IDを参照した新判断を追記する。` |
| `judgment/reassessment` | `対象、版、Scope、供給Evidence、承認、正常性、残余リスクが変わったら別Decisionで再評価する。` |
| `timelineId` | `TL-IR19-007` |
| `findingId` | `FND-IR19-007` |
| `controlId` | `CTL-IR19-007` |
| `reassessmentId` | `REA-IR19-007` |
| `handoffs/0/id` | `HOF-IR19-007-20` |
| `handoffs/0/targetChapter` | `20` |
| `handoffs/0/sourceDecisionId` | `DEC-IR19-007` |
| `handoffs/0/questionId` | `EQ-IR19-007-20` |
| `handoffs/0/plannedRecordId` | `TL-IR19-007` |
| `handoffs/0/question` | `同意変更と利用の時系列、代替説明、Unknown scopeをどの追加記録で区別できるか。` |
| `handoffs/0/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/0/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/1/id` | `HOF-IR19-007-22` |
| `handoffs/1/targetChapter` | `22` |
| `handoffs/1/sourceDecisionId` | `DEC-IR19-007` |
| `handoffs/1/questionId` | `EQ-IR19-007-22` |
| `handoffs/1/plannedRecordId` | `BKL-IR19-007` |
| `handoffs/1/question` | `残余リスクと観測GapをどのOwner、期限、検証条件で改善候補にするか。` |
| `handoffs/1/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/1/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/1/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/1/status` | `planned-not-delivered` |
| `handoffs/1/receiptId` | `null` |
| `handoffs/1/executionAuthorized` | `false` |
| `handoffs/2/id` | `HOF-IR19-007-26` |
| `handoffs/2/targetChapter` | `26` |
| `handoffs/2/sourceDecisionId` | `DEC-IR19-007` |
| `handoffs/2/questionId` | `EQ-IR19-007-26` |
| `handoffs/2/plannedRecordId` | `CTI-IR19-007` |
| `handoffs/2/question` | `限定した観測と代替説明をどの判断要求向けに再評価するか。` |
| `handoffs/2/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/2/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/2/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/2/status` | `planned-not-delivered` |
| `handoffs/2/receiptId` | `null` |
| `handoffs/2/executionAuthorized` | `false` |
| `input/context/subject` | `SYNTH-IR19-007` |
| `input/context/revision` | `REV-IR19-007` |
| `input/context/assets/0` | `SYN-APP-A` |
| `input/context/assets/1` | `SYN-APP-B` |
| `input/context/assets/2` | `SYN-ID-C` |
| `input/context/assets/3` | `SYN-DATA-D` |
| `input/context/start` | `2026-09-01T08:00:00Z` |
| `input/context/end` | `2026-09-01T09:00:00Z` |
| `input/previous/id` | `DEC-IR19-007-PREV` |
| `input/previous/status` | `Closed` |
| `input/previous/at` | `2026-09-01T10:10:00Z` |
| `input/previous/owner` | `SYNTH-IR-DECIDER` |
| `input/previous/reason` | `供給された前提判断。真正性を示す受領記録ではない。` |
| `input/previous/closureValidationId` | `EV-IR19-007-RECVALID` |
| `input/previous/closure/owner` | `SYNTH-IR-DECIDER` |
| `input/previous/closure/at` | `2026-09-01T10:10:00Z` |
| `input/previous/closure/residualRisk` | `未観測Dataは未解決。` |
| `input/previous/closure/riskOwner` | `SYNTH-IR-RISK` |
| `input/previous/closure/dueAt` | `2026-09-30T00:00:00Z` |
| `input/previous/closure/asset` | `SYN-APP-A` |
| `input/decision/id` | `DEC-IR19-007` |
| `input/decision/requested` | `Reopened` |
| `input/decision/at` | `2026-09-01T11:00:00Z` |
| `input/decision/owner` | `SYNTH-IR-DECIDER` |
| `input/decision/reason` | `供給記録と対象Scopeに限った教育上の判断。` |
| `input/classification` | `suspected-policy-violation` |
| `input/severity` | `medium` |
| `input/priority` | `urgent` |
| `input/scope/hypothesized/0` | `SYN-APP-B` |
| `input/scope/confirmed/0` | `SYN-APP-A` |
| `input/scope/excluded/0` | `SYN-ID-C` |
| `input/scope/unknown/0` | `SYN-DATA-D` |
| `input/declaration/id` | `DCL-IR19-007` |
| `input/declaration/owner` | `SYNTH-IR-DECIDER` |
| `input/declaration/reason` | `供給した教育用基準では、承認未確認の権限変化と利用の組が個別確認対象となる。` |
| `input/declaration/at` | `2026-09-01T09:15:00Z` |
| `input/declaration/criteriaId` | `EV-IR19-007-CRITERIA` |
| `input/declaration/asset` | `SYN-APP-A` |
| `input/preservation/id` | `PRV-IR19-007` |
| `input/preservation/owner` | `SYNTH-IR-EVIDENCE` |
| `input/preservation/at` | `2026-09-01T09:25:00Z` |
| `input/preservation/evidenceId` | `EV-IR19-007-SAVE` |
| `input/containment` | `null` |
| `input/analysisId` | `null` |
| `input/recovery` | `null` |
| `input/closure` | `null` |
| `input/reopening/id` | `REOPEN-IR19-007` |
| `input/reopening/closedDecisionId` | `DEC-IR19-007-PREV` |
| `input/reopening/newEvidenceId` | `EV-IR19-007-NEW` |
| `input/reopening/owner` | `SYNTH-IR-DECIDER` |
| `input/reopening/reason` | `閉鎖後に利用可能となった供給記録の影響を再評価する。` |
| `input/reopening/at` | `2026-09-01T11:00:00Z` |
| `input/incidentId` | `INC-IR19-007` |
| `input/threatQuestionId` | `THQ-IR19-007` |
| `input/evidenceQuestion` | `同意変更とWorkload利用の対応を、正当変更・誤設定・侵害仮説からどう区別するか。` |
| `input/collectionGap` | `Data Dの影響は未観測。実収集、原記録の真正性、全組織の範囲は未評価。` |
| `input/classificationBasis` | `供給候補の種類であり、悪意や原因の確定ではない。` |
| `input/severityBasis` | `合成Export機能への限定影響を想定する。Severityは確信度ではない。` |
| `input/priorityBasis` | `次の判断に必要な情報を先に確認する教育上の優先度。実対応の指示ではない。` |
| `input/eradicationQuestion` | `残る権限と再発条件をどのScopeで確認するか。根絶完了は未認定。実操作なし。` |

### ICASE19-008

| Field | Value |
|---|---|
| `id` | `ICASE19-008` |
| `expected/status` | `Suspected` |
| `expected/decision` | `deferred` |
| `expected/gaps/0` | `declaration-owner-reason-time-criteria` |
| `expected/limit` | `supplied-synthetic-record-only-not-authority-or-authenticity` |
| `expected/executionAuthorized` | `false` |
| `expected/notificationDecided` | `false` |
| `expected/noIncidentClaim` | `false` |
| `expected/improvementComplete` | `false` |
| `judgment/conclusion` | `宣言根拠が不足するためSuspectedを維持する。` |
| `judgment/alternative` | `Event不足で判断材料が揃っていない。` |
| `judgment/confidence` | `低` |
| `judgment/confidenceBasis` | `Huntの支持を追加の宣言基準に代用できない。` |
| `judgment/gap` | `判断主体と供給基準の確認が必要である。` |
| `judgment/nextAction` | `不足根拠のOwnerと次回確認を記録する。` |
| `judgment/reassessment` | `対象、版、Scope、供給Evidence、承認、正常性、残余リスクが変わったら別Decisionで再評価する。` |
| `timelineId` | `TL-IR19-008` |
| `findingId` | `FND-IR19-008` |
| `controlId` | `CTL-IR19-008` |
| `reassessmentId` | `REA-IR19-008` |
| `handoffs/0/id` | `HOF-IR19-008-20` |
| `handoffs/0/targetChapter` | `20` |
| `handoffs/0/sourceDecisionId` | `DEC-IR19-008` |
| `handoffs/0/questionId` | `EQ-IR19-008-20` |
| `handoffs/0/plannedRecordId` | `TL-IR19-008` |
| `handoffs/0/question` | `同意変更と利用の時系列、代替説明、Unknown scopeをどの追加記録で区別できるか。` |
| `handoffs/0/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/0/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/1/id` | `HOF-IR19-008-22` |
| `handoffs/1/targetChapter` | `22` |
| `handoffs/1/sourceDecisionId` | `DEC-IR19-008` |
| `handoffs/1/questionId` | `EQ-IR19-008-22` |
| `handoffs/1/plannedRecordId` | `BKL-IR19-008` |
| `handoffs/1/question` | `残余リスクと観測GapをどのOwner、期限、検証条件で改善候補にするか。` |
| `handoffs/1/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/1/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/1/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/1/status` | `planned-not-delivered` |
| `handoffs/1/receiptId` | `null` |
| `handoffs/1/executionAuthorized` | `false` |
| `handoffs/2/id` | `HOF-IR19-008-26` |
| `handoffs/2/targetChapter` | `26` |
| `handoffs/2/sourceDecisionId` | `DEC-IR19-008` |
| `handoffs/2/questionId` | `EQ-IR19-008-26` |
| `handoffs/2/plannedRecordId` | `CTI-IR19-008` |
| `handoffs/2/question` | `限定した観測と代替説明をどの判断要求向けに再評価するか。` |
| `handoffs/2/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/2/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/2/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/2/status` | `planned-not-delivered` |
| `handoffs/2/receiptId` | `null` |
| `handoffs/2/executionAuthorized` | `false` |
| `input/context/subject` | `SYNTH-IR19-008` |
| `input/context/revision` | `REV-IR19-008` |
| `input/context/assets/0` | `SYN-APP-A` |
| `input/context/assets/1` | `SYN-APP-B` |
| `input/context/assets/2` | `SYN-ID-C` |
| `input/context/assets/3` | `SYN-DATA-D` |
| `input/context/start` | `2026-09-01T08:00:00Z` |
| `input/context/end` | `2026-09-01T09:00:00Z` |
| `input/previous/id` | `DEC-IR19-008-PREV` |
| `input/previous/status` | `Suspected` |
| `input/previous/at` | `2026-09-01T10:10:00Z` |
| `input/previous/owner` | `SYNTH-IR-DECIDER` |
| `input/previous/reason` | `供給された前提判断。真正性を示す受領記録ではない。` |
| `input/previous/closureValidationId` | `null` |
| `input/previous/closure` | `null` |
| `input/decision/id` | `DEC-IR19-008` |
| `input/decision/requested` | `Declared` |
| `input/decision/at` | `2026-09-01T11:00:00Z` |
| `input/decision/owner` | `SYNTH-IR-DECIDER` |
| `input/decision/reason` | `供給記録と対象Scopeに限った教育上の判断。` |
| `input/classification` | `suspected-policy-violation` |
| `input/severity` | `medium` |
| `input/priority` | `urgent` |
| `input/scope/hypothesized/0` | `SYN-APP-B` |
| `input/scope/confirmed/0` | `SYN-APP-A` |
| `input/scope/excluded/0` | `SYN-ID-C` |
| `input/scope/unknown/0` | `SYN-DATA-D` |
| `input/declaration` | `null` |
| `input/preservation/id` | `PRV-IR19-008` |
| `input/preservation/owner` | `SYNTH-IR-EVIDENCE` |
| `input/preservation/at` | `2026-09-01T09:25:00Z` |
| `input/preservation/evidenceId` | `EV-IR19-008-SAVE` |
| `input/containment` | `null` |
| `input/analysisId` | `null` |
| `input/recovery` | `null` |
| `input/closure` | `null` |
| `input/reopening` | `null` |
| `input/incidentId` | `INC-IR19-008` |
| `input/threatQuestionId` | `THQ-IR19-008` |
| `input/evidenceQuestion` | `同意変更とWorkload利用の対応を、正当変更・誤設定・侵害仮説からどう区別するか。` |
| `input/collectionGap` | `Data Dの影響は未観測。実収集、原記録の真正性、全組織の範囲は未評価。` |
| `input/classificationBasis` | `供給候補の種類であり、悪意や原因の確定ではない。` |
| `input/severityBasis` | `合成Export機能への限定影響を想定する。Severityは確信度ではない。` |
| `input/priorityBasis` | `次の判断に必要な情報を先に確認する教育上の優先度。実対応の指示ではない。` |
| `input/eradicationQuestion` | `残る権限と再発条件をどのScopeで確認するか。根絶完了は未認定。実操作なし。` |

### ICASE19-009

| Field | Value |
|---|---|
| `id` | `ICASE19-009` |
| `expected/status` | `Suspected` |
| `expected/decision` | `deferred` |
| `expected/gaps/0` | `declaration-owner-reason-time-criteria` |
| `expected/limit` | `supplied-synthetic-record-only-not-authority-or-authenticity` |
| `expected/executionAuthorized` | `false` |
| `expected/notificationDecided` | `false` |
| `expected/noIncidentClaim` | `false` |
| `expected/improvementComplete` | `false` |
| `judgment/conclusion` | `正当変更という代替が残り、基準は未確定のためSuspectedを維持する。` |
| `judgment/alternative` | `誤設定の可能性も残す。` |
| `judgment/confidence` | `低` |
| `judgment/confidenceBasis` | `部分的な承認文脈だけでは宣言基準を満たさない。` |
| `judgment/gap` | `正当変更の対象と時点の追加確認が必要である。` |
| `judgment/nextAction` | `承認の不足を照会する計画だけを記録する。` |
| `judgment/reassessment` | `対象、版、Scope、供給Evidence、承認、正常性、残余リスクが変わったら別Decisionで再評価する。` |
| `timelineId` | `TL-IR19-009` |
| `findingId` | `FND-IR19-009` |
| `controlId` | `CTL-IR19-009` |
| `reassessmentId` | `REA-IR19-009` |
| `handoffs/0/id` | `HOF-IR19-009-20` |
| `handoffs/0/targetChapter` | `20` |
| `handoffs/0/sourceDecisionId` | `DEC-IR19-009` |
| `handoffs/0/questionId` | `EQ-IR19-009-20` |
| `handoffs/0/plannedRecordId` | `TL-IR19-009` |
| `handoffs/0/question` | `同意変更と利用の時系列、代替説明、Unknown scopeをどの追加記録で区別できるか。` |
| `handoffs/0/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/0/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/1/id` | `HOF-IR19-009-22` |
| `handoffs/1/targetChapter` | `22` |
| `handoffs/1/sourceDecisionId` | `DEC-IR19-009` |
| `handoffs/1/questionId` | `EQ-IR19-009-22` |
| `handoffs/1/plannedRecordId` | `BKL-IR19-009` |
| `handoffs/1/question` | `残余リスクと観測GapをどのOwner、期限、検証条件で改善候補にするか。` |
| `handoffs/1/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/1/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/1/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/1/status` | `planned-not-delivered` |
| `handoffs/1/receiptId` | `null` |
| `handoffs/1/executionAuthorized` | `false` |
| `handoffs/2/id` | `HOF-IR19-009-26` |
| `handoffs/2/targetChapter` | `26` |
| `handoffs/2/sourceDecisionId` | `DEC-IR19-009` |
| `handoffs/2/questionId` | `EQ-IR19-009-26` |
| `handoffs/2/plannedRecordId` | `CTI-IR19-009` |
| `handoffs/2/question` | `限定した観測と代替説明をどの判断要求向けに再評価するか。` |
| `handoffs/2/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/2/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/2/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/2/status` | `planned-not-delivered` |
| `handoffs/2/receiptId` | `null` |
| `handoffs/2/executionAuthorized` | `false` |
| `input/context/subject` | `SYNTH-IR19-009` |
| `input/context/revision` | `REV-IR19-009` |
| `input/context/assets/0` | `SYN-APP-A` |
| `input/context/assets/1` | `SYN-APP-B` |
| `input/context/assets/2` | `SYN-ID-C` |
| `input/context/assets/3` | `SYN-DATA-D` |
| `input/context/start` | `2026-09-01T08:00:00Z` |
| `input/context/end` | `2026-09-01T09:00:00Z` |
| `input/previous/id` | `DEC-IR19-009-PREV` |
| `input/previous/status` | `Suspected` |
| `input/previous/at` | `2026-09-01T10:10:00Z` |
| `input/previous/owner` | `SYNTH-IR-DECIDER` |
| `input/previous/reason` | `供給された前提判断。真正性を示す受領記録ではない。` |
| `input/previous/closureValidationId` | `null` |
| `input/previous/closure` | `null` |
| `input/decision/id` | `DEC-IR19-009` |
| `input/decision/requested` | `Declared` |
| `input/decision/at` | `2026-09-01T11:00:00Z` |
| `input/decision/owner` | `SYNTH-IR-DECIDER` |
| `input/decision/reason` | `供給記録と対象Scopeに限った教育上の判断。` |
| `input/classification` | `legitimate-change-possible` |
| `input/severity` | `medium` |
| `input/priority` | `urgent` |
| `input/scope/hypothesized/0` | `SYN-APP-B` |
| `input/scope/confirmed/0` | `SYN-APP-A` |
| `input/scope/excluded/0` | `SYN-ID-C` |
| `input/scope/unknown/0` | `SYN-DATA-D` |
| `input/declaration/id` | `DCL-IR19-009` |
| `input/declaration/owner` | `SYNTH-IR-DECIDER` |
| `input/declaration/reason` | `供給した教育用基準では、承認未確認の権限変化と利用の組が個別確認対象となる。` |
| `input/declaration/at` | `2026-09-01T09:15:00Z` |
| `input/declaration/criteriaId` | `EV-IR19-009-CRITERIA` |
| `input/declaration/asset` | `SYN-APP-A` |
| `input/preservation/id` | `PRV-IR19-009` |
| `input/preservation/owner` | `SYNTH-IR-EVIDENCE` |
| `input/preservation/at` | `2026-09-01T09:25:00Z` |
| `input/preservation/evidenceId` | `EV-IR19-009-SAVE` |
| `input/containment` | `null` |
| `input/analysisId` | `null` |
| `input/recovery` | `null` |
| `input/closure` | `null` |
| `input/reopening` | `null` |
| `input/incidentId` | `INC-IR19-009` |
| `input/threatQuestionId` | `THQ-IR19-009` |
| `input/evidenceQuestion` | `同意変更とWorkload利用の対応を、正当変更・誤設定・侵害仮説からどう区別するか。` |
| `input/collectionGap` | `Data Dの影響は未観測。実収集、原記録の真正性、全組織の範囲は未評価。` |
| `input/classificationBasis` | `供給候補の種類であり、悪意や原因の確定ではない。` |
| `input/severityBasis` | `合成Export機能への限定影響を想定する。Severityは確信度ではない。` |
| `input/priorityBasis` | `次の判断に必要な情報を先に確認する教育上の優先度。実対応の指示ではない。` |
| `input/eradicationQuestion` | `残る権限と再発条件をどのScopeで確認するか。根絶完了は未認定。実操作なし。` |

### ICASE19-010

| Field | Value |
|---|---|
| `id` | `ICASE19-010` |
| `expected/status` | `Suspected` |
| `expected/decision` | `accepted` |
| `expected/gaps` | `[]` |
| `expected/limit` | `supplied-synthetic-record-only-not-authority-or-authenticity` |
| `expected/executionAuthorized` | `false` |
| `expected/notificationDecided` | `false` |
| `expected/noIncidentClaim` | `false` |
| `expected/improvementComplete` | `false` |
| `judgment/conclusion` | `Log不足をUnknownとして残し、Suspectedを維持する。侵害なしとはしない。` |
| `judgment/alternative` | `未観測の影響も無害な変更もあり得る。` |
| `judgment/confidence` | `低` |
| `judgment/confidenceBasis` | `供給Scopeの一部が未観測である。` |
| `judgment/gap` | `未知の範囲を除外範囲に置換できない。` |
| `judgment/nextAction` | `Collection gapとEvidence Questionを渡す計画を記録する。` |
| `judgment/reassessment` | `対象、版、Scope、供給Evidence、承認、正常性、残余リスクが変わったら別Decisionで再評価する。` |
| `timelineId` | `TL-IR19-010` |
| `findingId` | `FND-IR19-010` |
| `controlId` | `CTL-IR19-010` |
| `reassessmentId` | `REA-IR19-010` |
| `handoffs/0/id` | `HOF-IR19-010-20` |
| `handoffs/0/targetChapter` | `20` |
| `handoffs/0/sourceDecisionId` | `DEC-IR19-010` |
| `handoffs/0/questionId` | `EQ-IR19-010-20` |
| `handoffs/0/plannedRecordId` | `TL-IR19-010` |
| `handoffs/0/question` | `同意変更と利用の時系列、代替説明、Unknown scopeをどの追加記録で区別できるか。` |
| `handoffs/0/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/0/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/1/id` | `HOF-IR19-010-22` |
| `handoffs/1/targetChapter` | `22` |
| `handoffs/1/sourceDecisionId` | `DEC-IR19-010` |
| `handoffs/1/questionId` | `EQ-IR19-010-22` |
| `handoffs/1/plannedRecordId` | `BKL-IR19-010` |
| `handoffs/1/question` | `残余リスクと観測GapをどのOwner、期限、検証条件で改善候補にするか。` |
| `handoffs/1/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/1/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/1/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/1/status` | `planned-not-delivered` |
| `handoffs/1/receiptId` | `null` |
| `handoffs/1/executionAuthorized` | `false` |
| `handoffs/2/id` | `HOF-IR19-010-26` |
| `handoffs/2/targetChapter` | `26` |
| `handoffs/2/sourceDecisionId` | `DEC-IR19-010` |
| `handoffs/2/questionId` | `EQ-IR19-010-26` |
| `handoffs/2/plannedRecordId` | `CTI-IR19-010` |
| `handoffs/2/question` | `限定した観測と代替説明をどの判断要求向けに再評価するか。` |
| `handoffs/2/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/2/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/2/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/2/status` | `planned-not-delivered` |
| `handoffs/2/receiptId` | `null` |
| `handoffs/2/executionAuthorized` | `false` |
| `input/context/subject` | `SYNTH-IR19-010` |
| `input/context/revision` | `REV-IR19-010` |
| `input/context/assets/0` | `SYN-APP-A` |
| `input/context/assets/1` | `SYN-APP-B` |
| `input/context/assets/2` | `SYN-ID-C` |
| `input/context/assets/3` | `SYN-DATA-D` |
| `input/context/start` | `2026-09-01T08:00:00Z` |
| `input/context/end` | `2026-09-01T09:00:00Z` |
| `input/previous/id` | `DEC-IR19-010-PREV` |
| `input/previous/status` | `Suspected` |
| `input/previous/at` | `2026-09-01T10:10:00Z` |
| `input/previous/owner` | `SYNTH-IR-DECIDER` |
| `input/previous/reason` | `供給された前提判断。真正性を示す受領記録ではない。` |
| `input/previous/closureValidationId` | `null` |
| `input/previous/closure` | `null` |
| `input/decision/id` | `DEC-IR19-010` |
| `input/decision/requested` | `Suspected` |
| `input/decision/at` | `2026-09-01T11:00:00Z` |
| `input/decision/owner` | `SYNTH-IR-DECIDER` |
| `input/decision/reason` | `供給記録と対象Scopeに限った教育上の判断。` |
| `input/classification` | `suspected-policy-violation` |
| `input/severity` | `medium` |
| `input/priority` | `urgent` |
| `input/scope/hypothesized` | `[]` |
| `input/scope/confirmed/0` | `SYN-APP-A` |
| `input/scope/excluded/0` | `SYN-ID-C` |
| `input/scope/unknown/0` | `SYN-APP-B` |
| `input/scope/unknown/1` | `SYN-DATA-D` |
| `input/declaration` | `null` |
| `input/preservation/id` | `PRV-IR19-010` |
| `input/preservation/owner` | `SYNTH-IR-EVIDENCE` |
| `input/preservation/at` | `2026-09-01T09:25:00Z` |
| `input/preservation/evidenceId` | `EV-IR19-010-SAVE` |
| `input/containment` | `null` |
| `input/analysisId` | `null` |
| `input/recovery` | `null` |
| `input/closure` | `null` |
| `input/reopening` | `null` |
| `input/incidentId` | `INC-IR19-010` |
| `input/threatQuestionId` | `THQ-IR19-010` |
| `input/evidenceQuestion` | `同意変更とWorkload利用の対応を、正当変更・誤設定・侵害仮説からどう区別するか。` |
| `input/collectionGap` | `Data Dの影響は未観測。実収集、原記録の真正性、全組織の範囲は未評価。` |
| `input/classificationBasis` | `供給候補の種類であり、悪意や原因の確定ではない。` |
| `input/severityBasis` | `合成Export機能への限定影響を想定する。Severityは確信度ではない。` |
| `input/priorityBasis` | `次の判断に必要な情報を先に確認する教育上の優先度。実対応の指示ではない。` |
| `input/eradicationQuestion` | `残る権限と再発条件をどのScopeで確認するか。根絶完了は未認定。実操作なし。` |

### ICASE19-011

| Field | Value |
|---|---|
| `id` | `ICASE19-011` |
| `expected/status` | `Declared` |
| `expected/decision` | `deferred` |
| `expected/gaps/0` | `containment-not-validated` |
| `expected/limit` | `supplied-synthetic-record-only-not-authority-or-authenticity` |
| `expected/executionAuthorized` | `false` |
| `expected/notificationDecided` | `false` |
| `expected/noIncidentClaim` | `false` |
| `expected/improvementComplete` | `false` |
| `judgment/conclusion` | `選択肢の記録だけではContainedに進めず、Declaredを維持する。` |
| `judgment/alternative` | `Monitoringだけでは拡大が続く可能性がある。` |
| `judgment/confidence` | `低` |
| `judgment/confidenceBasis` | `封じ込め効果を示す供給検証がない。` |
| `judgment/gap` | `実行済みとも効果確認済みともいえない。` |
| `judgment/nextAction` | `効果の検証条件を再設計する計画を記録する。` |
| `judgment/reassessment` | `対象、版、Scope、供給Evidence、承認、正常性、残余リスクが変わったら別Decisionで再評価する。` |
| `timelineId` | `TL-IR19-011` |
| `findingId` | `FND-IR19-011` |
| `controlId` | `CTL-IR19-011` |
| `reassessmentId` | `REA-IR19-011` |
| `handoffs/0/id` | `HOF-IR19-011-20` |
| `handoffs/0/targetChapter` | `20` |
| `handoffs/0/sourceDecisionId` | `DEC-IR19-011` |
| `handoffs/0/questionId` | `EQ-IR19-011-20` |
| `handoffs/0/plannedRecordId` | `TL-IR19-011` |
| `handoffs/0/question` | `同意変更と利用の時系列、代替説明、Unknown scopeをどの追加記録で区別できるか。` |
| `handoffs/0/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/0/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/1/id` | `HOF-IR19-011-22` |
| `handoffs/1/targetChapter` | `22` |
| `handoffs/1/sourceDecisionId` | `DEC-IR19-011` |
| `handoffs/1/questionId` | `EQ-IR19-011-22` |
| `handoffs/1/plannedRecordId` | `BKL-IR19-011` |
| `handoffs/1/question` | `残余リスクと観測GapをどのOwner、期限、検証条件で改善候補にするか。` |
| `handoffs/1/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/1/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/1/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/1/status` | `planned-not-delivered` |
| `handoffs/1/receiptId` | `null` |
| `handoffs/1/executionAuthorized` | `false` |
| `handoffs/2/id` | `HOF-IR19-011-26` |
| `handoffs/2/targetChapter` | `26` |
| `handoffs/2/sourceDecisionId` | `DEC-IR19-011` |
| `handoffs/2/questionId` | `EQ-IR19-011-26` |
| `handoffs/2/plannedRecordId` | `CTI-IR19-011` |
| `handoffs/2/question` | `限定した観測と代替説明をどの判断要求向けに再評価するか。` |
| `handoffs/2/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/2/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/2/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/2/status` | `planned-not-delivered` |
| `handoffs/2/receiptId` | `null` |
| `handoffs/2/executionAuthorized` | `false` |
| `input/context/subject` | `SYNTH-IR19-011` |
| `input/context/revision` | `REV-IR19-011` |
| `input/context/assets/0` | `SYN-APP-A` |
| `input/context/assets/1` | `SYN-APP-B` |
| `input/context/assets/2` | `SYN-ID-C` |
| `input/context/assets/3` | `SYN-DATA-D` |
| `input/context/start` | `2026-09-01T08:00:00Z` |
| `input/context/end` | `2026-09-01T09:00:00Z` |
| `input/previous/id` | `DEC-IR19-011-PREV` |
| `input/previous/status` | `Declared` |
| `input/previous/at` | `2026-09-01T10:10:00Z` |
| `input/previous/owner` | `SYNTH-IR-DECIDER` |
| `input/previous/reason` | `供給された前提判断。真正性を示す受領記録ではない。` |
| `input/previous/closureValidationId` | `null` |
| `input/previous/closure` | `null` |
| `input/decision/id` | `DEC-IR19-011` |
| `input/decision/requested` | `Contained` |
| `input/decision/at` | `2026-09-01T11:00:00Z` |
| `input/decision/owner` | `SYNTH-IR-DECIDER` |
| `input/decision/reason` | `供給記録と対象Scopeに限った教育上の判断。` |
| `input/classification` | `suspected-policy-violation` |
| `input/severity` | `medium` |
| `input/priority` | `urgent` |
| `input/scope/hypothesized/0` | `SYN-APP-B` |
| `input/scope/confirmed/0` | `SYN-APP-A` |
| `input/scope/excluded/0` | `SYN-ID-C` |
| `input/scope/unknown/0` | `SYN-DATA-D` |
| `input/declaration/id` | `DCL-IR19-011` |
| `input/declaration/owner` | `SYNTH-IR-DECIDER` |
| `input/declaration/reason` | `供給した教育用基準では、承認未確認の権限変化と利用の組が個別確認対象となる。` |
| `input/declaration/at` | `2026-09-01T09:15:00Z` |
| `input/declaration/criteriaId` | `EV-IR19-011-CRITERIA` |
| `input/declaration/asset` | `SYN-APP-A` |
| `input/preservation/id` | `PRV-IR19-011` |
| `input/preservation/owner` | `SYNTH-IR-EVIDENCE` |
| `input/preservation/at` | `2026-09-01T09:25:00Z` |
| `input/preservation/evidenceId` | `EV-IR19-011-SAVE` |
| `input/containment/id` | `ACT-IR19-011` |
| `input/containment/optionId` | `OPT-IR19-MONITOR` |
| `input/containment/asset` | `SYN-APP-A` |
| `input/containment/at` | `2026-09-01T10:15:00Z` |
| `input/containment/expectedImpact` | `保管量と分析負荷が増える想定。` |
| `input/containment/rollback` | `追加観測の終了条件を別記する案。実操作なし。` |
| `input/containment/destructive` | `false` |
| `input/containment/actualExecuted` | `false` |
| `input/containment/validationId` | `null` |
| `input/containment/authority/id` | `AUTH-IR19-011` |
| `input/containment/authority/approved` | `true` |
| `input/containment/authority/owner` | `SYNTH-IR-COMMANDER` |
| `input/containment/authority/approvedAt` | `2026-09-01T10:12:00Z` |
| `input/containment/authority/expiresAt` | `2026-09-01T10:45:00Z` |
| `input/containment/authority/subject` | `SYNTH-IR19-011` |
| `input/containment/authority/revision` | `REV-IR19-011` |
| `input/containment/authority/asset` | `SYN-APP-A` |
| `input/containment/authority/realAuthority` | `false` |
| `input/analysisId` | `null` |
| `input/recovery` | `null` |
| `input/closure` | `null` |
| `input/reopening` | `null` |
| `input/incidentId` | `INC-IR19-011` |
| `input/threatQuestionId` | `THQ-IR19-011` |
| `input/evidenceQuestion` | `同意変更とWorkload利用の対応を、正当変更・誤設定・侵害仮説からどう区別するか。` |
| `input/collectionGap` | `Data Dの影響は未観測。実収集、原記録の真正性、全組織の範囲は未評価。` |
| `input/classificationBasis` | `供給候補の種類であり、悪意や原因の確定ではない。` |
| `input/severityBasis` | `合成Export機能への限定影響を想定する。Severityは確信度ではない。` |
| `input/priorityBasis` | `次の判断に必要な情報を先に確認する教育上の優先度。実対応の指示ではない。` |
| `input/eradicationQuestion` | `残る権限と再発条件をどのScopeで確認するか。根絶完了は未認定。実操作なし。` |

### ICASE19-012

| Field | Value |
|---|---|
| `id` | `ICASE19-012` |
| `expected/status` | `Recovering` |
| `expected/decision` | `deferred` |
| `expected/gaps/0` | `recovery-not-validated` |
| `expected/limit` | `supplied-synthetic-record-only-not-authority-or-authenticity` |
| `expected/executionAuthorized` | `false` |
| `expected/notificationDecided` | `false` |
| `expected/noIncidentClaim` | `false` |
| `expected/improvementComplete` | `false` |
| `judgment/conclusion` | `復旧検証が未確定のためRecoveringを維持する。Closedとしない。` |
| `judgment/alternative` | `限定した正常性確認が不足している。` |
| `judgment/confidence` | `低` |
| `judgment/confidenceBasis` | `入口基準だけでは復旧完了を示せない。` |
| `judgment/gap` | `復旧後の完全性と正常性の確認が必要である。` |
| `judgment/nextAction` | `復旧検証と残余リスクの見直しを記録する。` |
| `judgment/reassessment` | `対象、版、Scope、供給Evidence、承認、正常性、残余リスクが変わったら別Decisionで再評価する。` |
| `timelineId` | `TL-IR19-012` |
| `findingId` | `FND-IR19-012` |
| `controlId` | `CTL-IR19-012` |
| `reassessmentId` | `REA-IR19-012` |
| `handoffs/0/id` | `HOF-IR19-012-20` |
| `handoffs/0/targetChapter` | `20` |
| `handoffs/0/sourceDecisionId` | `DEC-IR19-012` |
| `handoffs/0/questionId` | `EQ-IR19-012-20` |
| `handoffs/0/plannedRecordId` | `TL-IR19-012` |
| `handoffs/0/question` | `同意変更と利用の時系列、代替説明、Unknown scopeをどの追加記録で区別できるか。` |
| `handoffs/0/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/0/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/1/id` | `HOF-IR19-012-22` |
| `handoffs/1/targetChapter` | `22` |
| `handoffs/1/sourceDecisionId` | `DEC-IR19-012` |
| `handoffs/1/questionId` | `EQ-IR19-012-22` |
| `handoffs/1/plannedRecordId` | `BKL-IR19-012` |
| `handoffs/1/question` | `残余リスクと観測GapをどのOwner、期限、検証条件で改善候補にするか。` |
| `handoffs/1/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/1/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/1/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/1/status` | `planned-not-delivered` |
| `handoffs/1/receiptId` | `null` |
| `handoffs/1/executionAuthorized` | `false` |
| `handoffs/2/id` | `HOF-IR19-012-26` |
| `handoffs/2/targetChapter` | `26` |
| `handoffs/2/sourceDecisionId` | `DEC-IR19-012` |
| `handoffs/2/questionId` | `EQ-IR19-012-26` |
| `handoffs/2/plannedRecordId` | `CTI-IR19-012` |
| `handoffs/2/question` | `限定した観測と代替説明をどの判断要求向けに再評価するか。` |
| `handoffs/2/scope` | `供給subject/revisionの四対象と08:00–09:00 UTCだけ。親Evidenceの移送ではない。` |
| `handoffs/2/owner` | `SYNTH-IR-COMMANDER` |
| `handoffs/2/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/2/status` | `planned-not-delivered` |
| `handoffs/2/receiptId` | `null` |
| `handoffs/2/executionAuthorized` | `false` |
| `input/context/subject` | `SYNTH-IR19-012` |
| `input/context/revision` | `REV-IR19-012` |
| `input/context/assets/0` | `SYN-APP-A` |
| `input/context/assets/1` | `SYN-APP-B` |
| `input/context/assets/2` | `SYN-ID-C` |
| `input/context/assets/3` | `SYN-DATA-D` |
| `input/context/start` | `2026-09-01T08:00:00Z` |
| `input/context/end` | `2026-09-01T09:00:00Z` |
| `input/previous/id` | `DEC-IR19-012-PREV` |
| `input/previous/status` | `Recovering` |
| `input/previous/at` | `2026-09-01T10:10:00Z` |
| `input/previous/owner` | `SYNTH-IR-DECIDER` |
| `input/previous/reason` | `供給された前提判断。真正性を示す受領記録ではない。` |
| `input/previous/closureValidationId` | `null` |
| `input/previous/closure` | `null` |
| `input/decision/id` | `DEC-IR19-012` |
| `input/decision/requested` | `Closed` |
| `input/decision/at` | `2026-09-01T11:00:00Z` |
| `input/decision/owner` | `SYNTH-IR-DECIDER` |
| `input/decision/reason` | `供給記録と対象Scopeに限った教育上の判断。` |
| `input/classification` | `suspected-policy-violation` |
| `input/severity` | `medium` |
| `input/priority` | `urgent` |
| `input/scope/hypothesized/0` | `SYN-APP-B` |
| `input/scope/confirmed/0` | `SYN-APP-A` |
| `input/scope/excluded/0` | `SYN-ID-C` |
| `input/scope/unknown/0` | `SYN-DATA-D` |
| `input/declaration/id` | `DCL-IR19-012` |
| `input/declaration/owner` | `SYNTH-IR-DECIDER` |
| `input/declaration/reason` | `供給した教育用基準では、承認未確認の権限変化と利用の組が個別確認対象となる。` |
| `input/declaration/at` | `2026-09-01T09:15:00Z` |
| `input/declaration/criteriaId` | `EV-IR19-012-CRITERIA` |
| `input/declaration/asset` | `SYN-APP-A` |
| `input/preservation/id` | `PRV-IR19-012` |
| `input/preservation/owner` | `SYNTH-IR-EVIDENCE` |
| `input/preservation/at` | `2026-09-01T09:25:00Z` |
| `input/preservation/evidenceId` | `EV-IR19-012-SAVE` |
| `input/containment` | `null` |
| `input/analysisId` | `null` |
| `input/recovery/id` | `REC-IR19-012` |
| `input/recovery/owner` | `SYNTH-IR-RECOVERY` |
| `input/recovery/criteriaId` | `EV-IR19-012-RECENTRY` |
| `input/recovery/validationId` | `EV-IR19-012-RECVALID` |
| `input/recovery/asset` | `SYN-APP-A` |
| `input/closure/owner` | `SYNTH-IR-DECIDER` |
| `input/closure/at` | `2026-09-01T11:00:00Z` |
| `input/closure/residualRisk` | `未観測Dataの影響と再発要因は別担当が追跡する。` |
| `input/closure/riskOwner` | `SYNTH-IR-RISK` |
| `input/closure/dueAt` | `2026-09-30T00:00:00Z` |
| `input/closure/asset` | `SYN-APP-A` |
| `input/reopening` | `null` |
| `input/incidentId` | `INC-IR19-012` |
| `input/threatQuestionId` | `THQ-IR19-012` |
| `input/evidenceQuestion` | `同意変更とWorkload利用の対応を、正当変更・誤設定・侵害仮説からどう区別するか。` |
| `input/collectionGap` | `Data Dの影響は未観測。実収集、原記録の真正性、全組織の範囲は未評価。` |
| `input/classificationBasis` | `供給候補の種類であり、悪意や原因の確定ではない。` |
| `input/severityBasis` | `合成Export機能への限定影響を想定する。Severityは確信度ではない。` |
| `input/priorityBasis` | `次の判断に必要な情報を先に確認する教育上の優先度。実対応の指示ではない。` |
| `input/eradicationQuestion` | `残る権限と再発条件をどのScopeで確認するか。根絶完了は未認定。実操作なし。` |

## 提出時の確認

宣言の主体・理由・時刻、限定Scope、保持と選択肢、復旧検証、残余リスク、再開の新Evidenceを指し示す。全Handoffは未配達、Receiptはnull、実権限はfalseであり、第20・22・26章の成果を先取りしない。法的通知の要否・期限は本教材で決めない。自分の読解メモだけを整理し、正本と親Evidenceは変更しない。
