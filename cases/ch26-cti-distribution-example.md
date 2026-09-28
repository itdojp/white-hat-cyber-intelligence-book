# 第26章 完全記入例：同じ根拠を技術・経営へ渡す

## この記入例の扱い

ART-08 / ART-09の完全合成例です。`CDP-2026-026-001`は親`CASE-2026-025`をrefinesし、親の限定Block・注意喚起案、L2上限、成功可否の未確認を保持します。実観測、実承認、実操作、実配達は追加していません。7月の記録は親の判断時点を配布面から構成した教材設定で、親の後日のReviewを当時の実承認へ転用しません。

[第26章](../manuscript/26-cti-distribution.md)、[ART-08 Template](../templates/cti-report.md)、[ART-09 Template](../templates/executive-brief.md)、[供給Product JSON](fixtures/ch26-cti-distribution.json)、[閉Schema](../schemas/ch26-cti-distribution.schema.json)を参照してください。

## 二つの教材を結合しない

Productは親25のEvidenceを明示的に参照します。親23/24は方法参照だけで、未配達のHandoffや実権限を受け継ぎません。親25のSource 004/005/007は一原典群、008には期間と詳細Telemetryの欠落があります。

別の`CASE-STIX26-DEMO`は型と関係だけを学ぶ独立の合成例です。[STIX Bundle](fixtures/ch26-stix-bundle.json) / [その閉Schema](../schemas/ch26-stix-bundle.schema.json)、[offline TAXII例](fixtures/ch26-taxii-exchange.json) / [その閉Schema](../schemas/ch26-taxii-exchange.schema.json)は、親の帰属を強める根拠ではありません。Octoberの未来時刻は独立した教材設定です。稼働サービスや実行コードは含まない。

## ART-08：技術・運用向けに読む

読者はSYNTH-SOC Lead、ProductはPRD-CTI26-TECHです。KJ1からEvidence001〜004と帰属上限、KJ2からEvidence008とGap001、KJ3からEvidence004/005/007と同一原典群へ戻ります。検知・Hunt・IRへの案は紙上検討で、過去のArtifactのPassedをこのCaseの有効性として継承しません。

REC-CTI26-001は親の二つの合成Domainだけを扱う限定案、002はTelemetryの欠落、003は原典の不足を記録します。KJと推奨を別欄にし、実行のAuthorityはfalseのままです。

## ART-09：経営判断へ向けて読む

読者はSYNTH-CISO、ProductはPRD-CTI26-EXECです。同じ三KJと確信度を残し、A/B/Cの三OptionのBenefit、Cost、Disruption、Residual risk、Reversibilityを比較します。Aは親Decisionの表現を保つ案で、別の選択へ上書きしません。

業務上の露出は、親の合成Partner administrator向けの誘導と、過少評価・誤通知の両面です。成功可否を未確認のままにすることが残余リスクです。実被害額や確定した費用は与えていないため数値化しません。実行承認・実配送・受領はすべて未取得です。

## 全欄の読み方

以下は供給Product JSONの全leafを順序付きで表示した記入値です。nullは未受領・未配達または該当するIDが未発行、falseは実施や許可を主張しないことを示します。空配列は独立STIX例をEvidenceやProductのObjectとして採用しないことを表します。Hash一致は供給値の識別だけで、分析や合法性の認証ではありません。

### schemaVersion

| Field | Value |
|---|---|
| `value` | `1.0.0` |

### synthetic

| Field | Value |
|---|---|
| `value` | `true` |

### readOnly

| Field | Value |
|---|---|
| `value` | `true` |

### networkRequired

| Field | Value |
|---|---|
| `value` | `false` |

### executionAuthorized

| Field | Value |
|---|---|
| `value` | `false` |

### record

| Field | Value |
|---|---|
| `id` | `CDP-2026-026-001` |
| `caseId` | `CASE-2026-025` |
| `parentCaseId` | `CASE-2026-025` |
| `relation` | `refines` |
| `parentArtifactId` | `ART-12` |
| `parentJudgmentId` | `AJ-2026-025` |
| `parentDecisionId` | `DEC-2026-025` |
| `asOf` | `2026-07-29T11:00:00Z` |
| `cutoff` | `2026-07-29T09:00:00Z` |
| `deadline` | `2026-07-30T01:00:00Z` |
| `attributionCeiling` | `L2` |
| `syntheticSetting` | `第25章の同じ判断時点を配布面から詳細化する教材設定。実観測・実承認・実通知ではない。` |

### requirement

| Field | Value |
|---|---|
| `id` | `IR-2026-025` |
| `decisionRequirementId` | `DR-2026-025` |
| `question` | `観測した事象をTechnical clusterとして扱うべきか。CampaignやOperatorを示唆してよいか` |
| `owner` | `SYNTH-CISO` |
| `successCondition` | `二Productから同じKJ・Evidence・Gapを辿れ、実配達や実操作の許可と混同しない。` |

### MREF-CTI26-023

| Field | Value |
|---|---|
| `id` | `MREF-CTI26-023` |
| `chapter` | `23` |
| `artifactId` | `ART-29` |
| `recordId` | `IRCP-2026-023-001` |
| `relation` | `method-only` |
| `evidenceReceived` | `false` |
| `receiptId` | `null` |

### MREF-CTI26-024

| Field | Value |
|---|---|
| `id` | `MREF-CTI26-024` |
| `chapter` | `24` |
| `artifactId` | `ART-30` |
| `recordId` | `EST-2026-024-001` |
| `relation` | `method-only` |
| `evidenceReceived` | `false` |
| `receiptId` | `null` |

### EVD-2026-025-001

| Field | Value |
|---|---|
| `id` | `EVD-2026-025-001` |
| `sourceId` | `SN-2026-025-001` |
| `parentArtifactId` | `ART-12` |
| `independenceGroupId` | `IG-INT-001` |
| `synthetic` | `true` |
| `limitation` | `Mail bodyは要約保持、archive完全性は別証跡がない。` |
| `newObservation` | `false` |

### EVD-2026-025-002

| Field | Value |
|---|---|
| `id` | `EVD-2026-025-002` |
| `sourceId` | `SN-2026-025-002` |
| `parentArtifactId` | `ART-12` |
| `independenceGroupId` | `IG-INT-002` |
| `synthetic` | `true` |
| `limitation` | `後段の成功・失敗はこの観測に含まない。` |
| `newObservation` | `false` |

### EVD-2026-025-003

| Field | Value |
|---|---|
| `id` | `EVD-2026-025-003` |
| `sourceId` | `SN-2026-025-003` |
| `parentArtifactId` | `ART-12` |
| `independenceGroupId` | `IG-EXT-001` |
| `synthetic` | `true` |
| `limitation` | `登録者は判定できない。` |
| `newObservation` | `false` |

### EVD-2026-025-004

| Field | Value |
|---|---|
| `id` | `EVD-2026-025-004` |
| `sourceId` | `SN-2026-025-004` |
| `parentArtifactId` | `ART-12` |
| `independenceGroupId` | `IG-EXT-002` |
| `synthetic` | `true` |
| `limitation` | `bulletin revision履歴がない。` |
| `newObservation` | `false` |

### EVD-2026-025-005

| Field | Value |
|---|---|
| `id` | `EVD-2026-025-005` |
| `sourceId` | `SN-2026-025-005` |
| `parentArtifactId` | `ART-12` |
| `independenceGroupId` | `IG-EXT-002` |
| `synthetic` | `true` |
| `limitation` | `独自観測のない再掲。` |
| `newObservation` | `false` |

### EVD-2026-025-006

| Field | Value |
|---|---|
| `id` | `EVD-2026-025-006` |
| `sourceId` | `SN-2026-025-006` |
| `parentArtifactId` | `ART-12` |
| `independenceGroupId` | `IG-EXT-003` |
| `synthetic` | `true` |
| `limitation` | `原文全文・発言者が未確認。` |
| `newObservation` | `false` |

### EVD-2026-025-007

| Field | Value |
|---|---|
| `id` | `EVD-2026-025-007` |
| `sourceId` | `SN-2026-025-007` |
| `parentArtifactId` | `ART-12` |
| `independenceGroupId` | `IG-EXT-002` |
| `synthetic` | `true` |
| `limitation` | `同じbulletinの再要約。` |
| `newObservation` | `false` |

### EVD-2026-025-008

| Field | Value |
|---|---|
| `id` | `EVD-2026-025-008` |
| `sourceId` | `SN-2026-025-008` |
| `parentArtifactId` | `ART-12` |
| `independenceGroupId` | `IG-INT-003` |
| `synthetic` | `true` |
| `limitation` | `2026-07-23〜29のsummaryのみ。前半二日と詳細token issuanceは欠落。` |
| `newObservation` | `false` |

### KJ-CTI26-001

| Field | Value |
|---|---|
| `id` | `KJ-CTI26-001` |
| `parentJudgmentId` | `AJ-2026-025` |
| `statement` | `観測事象は技術クラスタと整合する。Campaign・Operator・国家の断定は支持しない。` |
| `confidence` | `中` |
| `evidenceIds/0` | `EVD-2026-025-001` |
| `evidenceIds/1` | `EVD-2026-025-002` |
| `evidenceIds/2` | `EVD-2026-025-003` |
| `evidenceIds/3` | `EVD-2026-025-004` |
| `sourceIds/0` | `SN-2026-025-001` |
| `sourceIds/1` | `SN-2026-025-002` |
| `sourceIds/2` | `SN-2026-025-003` |
| `sourceIds/3` | `SN-2026-025-004` |
| `gapIds/0` | `GAP-2026-025-003` |
| `gapIds/1` | `GAP-2026-025-004` |
| `alternativeIds/0` | `ALT-2026-025-001` |
| `alternativeIds/1` | `ALT-2026-025-002` |
| `alternativeIds/2` | `ALT-2026-025-003` |
| `invalidation` | `承認済みSSO保守が事象全体を説明する、またはshared toolingの説明が強くなる場合。` |
| `attributionLevel` | `L2` |
| `successDetermined` | `false` |
| `stixConfidence` | `null` |
| `independentOrigins` | `4` |

### KJ-CTI26-002

| Field | Value |
|---|---|
| `id` | `KJ-CTI26-002` |
| `parentJudgmentId` | `AJ-2026-025` |
| `statement` | `観測範囲では成功痕跡を確認していないが、保持外と詳細Telemetry欠落のため成功可否は判定できない。` |
| `confidence` | `低` |
| `evidenceIds/0` | `EVD-2026-025-008` |
| `sourceIds/0` | `SN-2026-025-008` |
| `gapIds/0` | `GAP-2026-025-001` |
| `alternativeIds/0` | `ALT-CTI26-SUCCESS` |
| `alternativeIds/1` | `ALT-CTI26-NO-SUCCESS` |
| `invalidation` | `親Gap001に相当する追加の独立観測が得られ、Coverageと成功可否を再評価できる場合。` |
| `attributionLevel` | `L2` |
| `successDetermined` | `false` |
| `stixConfidence` | `null` |
| `independentOrigins` | `1` |

### KJ-CTI26-003

| Field | Value |
|---|---|
| `id` | `KJ-CTI26-003` |
| `parentJudgmentId` | `SEJ-2026-025-001` |
| `statement` | `bulletin・repost・recapの三報告は一つの原典群であり、三件の独立裏付けとは扱わない。` |
| `confidence` | `中` |
| `evidenceIds/0` | `EVD-2026-025-004` |
| `evidenceIds/1` | `EVD-2026-025-005` |
| `evidenceIds/2` | `EVD-2026-025-007` |
| `sourceIds/0` | `SN-2026-025-004` |
| `sourceIds/1` | `SN-2026-025-005` |
| `sourceIds/2` | `SN-2026-025-007` |
| `gapIds/0` | `GAP-2026-025-002` |
| `alternativeIds/0` | `ALT-CTI26-NEW-ORIGIN` |
| `invalidation` | `各報告が別原典や独自観測を持つという来歴が確認される場合。` |
| `attributionLevel` | `L2` |
| `successDetermined` | `false` |
| `stixConfidence` | `null` |
| `independentOrigins` | `1` |

### REC-CTI26-001

| Field | Value |
|---|---|
| `id` | `REC-CTI26-001` |
| `judgmentIds/0` | `KJ-CTI26-001` |
| `purpose` | `tactical` |
| `owner` | `SYNTH-SOC Lead` |
| `statement` | `供給された合成Domain二件に限定する親DecisionのBlock案を、検知仮説・誤通知条件・停止条件の紙上レビューへ渡す。` |
| `executionStatus` | `not-executed` |
| `authorityGranted` | `false` |
| `parentRecommendationId` | `REC-2026-025-001` |

### REC-CTI26-002

| Field | Value |
|---|---|
| `id` | `REC-CTI26-002` |
| `judgmentIds/0` | `KJ-CTI26-002` |
| `purpose` | `operational` |
| `owner` | `SYNTH-Identity Lead` |
| `statement` | `詳細Telemetryの保持不足を優先Gapとして記録し、追加収集には別の承認・Scope審査を要求する。` |
| `executionStatus` | `not-executed` |
| `authorityGranted` | `false` |
| `parentRecommendationId` | `REC-2026-025-002` |

### REC-CTI26-003

| Field | Value |
|---|---|
| `id` | `REC-CTI26-003` |
| `judgmentIds/0` | `KJ-CTI26-003` |
| `purpose` | `strategic` |
| `owner` | `SYNTH-CISO` |
| `statement` | `原典不足と残余リスクを費用判断へ明示し、親の限定通知案を実配達済みとせず再評価期限を設定する。` |
| `executionStatus` | `not-executed` |
| `authorityGranted` | `false` |
| `parentRecommendationId` | `REC-2026-025-003` |

### PRD-CTI26-TECH

| Field | Value |
|---|---|
| `id` | `PRD-CTI26-TECH` |
| `artifactId` | `ART-08` |
| `requirementId` | `IR-2026-025` |
| `audience` | `SYNTH-SOC Lead` |
| `purpose` | `tactical-operational` |
| `version` | `1` |
| `status` | `prepared-not-delivered` |
| `cutoff` | `2026-07-29T09:00:00Z` |
| `preparedAt` | `2026-07-29T10:00:00Z` |
| `deadline` | `2026-07-30T01:00:00Z` |
| `expiresAt` | `2026-07-30T01:00:00Z` |
| `judgmentIds/0` | `KJ-CTI26-001` |
| `judgmentIds/1` | `KJ-CTI26-002` |
| `judgmentIds/2` | `KJ-CTI26-003` |
| `recommendationIds/0` | `REC-CTI26-001` |
| `recommendationIds/1` | `REC-CTI26-002` |
| `recommendationIds/2` | `REC-CTI26-003` |
| `implication` | `Domain対応付けだけで検知の有効性を保証せず、ScopeとCoverageを添えて紙上の検証計画へ渡す。` |
| `classification` | `教育用公開合成資料` |
| `sharingLabel` | `TLP:CLEAR` |
| `license` | `CC BY-NC-SA 4.0; 商用利用は別契約` |
| `encryption` | `offline教材。暗号化や配送を実証しない。` |
| `retention` | `供給資料は教材として保持、演習で作ったCopyのみ終了時に整理。` |
| `actionPermission` | `false` |
| `delivered` | `false` |
| `receiptId` | `null` |
| `feedbackId` | `FDB-CTI26-TECH` |
| `reassessmentId` | `REA-CTI26-001` |
| `supersedes` | `null` |
| `stixObjectIds` | `[]` |

### PRD-CTI26-EXEC

| Field | Value |
|---|---|
| `id` | `PRD-CTI26-EXEC` |
| `artifactId` | `ART-09` |
| `requirementId` | `IR-2026-025` |
| `audience` | `SYNTH-CISO` |
| `purpose` | `strategic` |
| `version` | `1` |
| `status` | `prepared-not-delivered` |
| `cutoff` | `2026-07-29T09:00:00Z` |
| `preparedAt` | `2026-07-29T10:00:00Z` |
| `deadline` | `2026-07-30T01:00:00Z` |
| `expiresAt` | `2026-07-30T01:00:00Z` |
| `judgmentIds/0` | `KJ-CTI26-001` |
| `judgmentIds/1` | `KJ-CTI26-002` |
| `judgmentIds/2` | `KJ-CTI26-003` |
| `recommendationIds/0` | `REC-CTI26-001` |
| `recommendationIds/1` | `REC-CTI26-002` |
| `recommendationIds/2` | `REC-CTI26-003` |
| `implication` | `過小評価と過剰な範囲拡大の両方を避け、業務影響・費用・残余リスク・可逆性を比較する。` |
| `classification` | `教育用公開合成資料` |
| `sharingLabel` | `TLP:CLEAR` |
| `license` | `CC BY-NC-SA 4.0; 商用利用は別契約` |
| `encryption` | `offline教材。暗号化や配送を実証しない。` |
| `retention` | `供給資料は教材として保持、演習で作ったCopyのみ終了時に整理。` |
| `actionPermission` | `false` |
| `delivered` | `false` |
| `receiptId` | `null` |
| `feedbackId` | `FDB-CTI26-EXEC` |
| `reassessmentId` | `REA-CTI26-001` |
| `supersedes` | `null` |
| `stixObjectIds` | `[]` |

### OPT-CTI26-A

| Field | Value |
|---|---|
| `id` | `OPT-CTI26-A` |
| `label` | `親Decisionの限定案を説明する` |
| `benefit` | `二つの合成Domainだけを対象とする案とL2表現を保持できる。` |
| `cost` | `SYNTH-SOC/Identityによる確認と誤通知審査の時間が必要。` |
| `disruption` | `紙上案では停止なし。実施時の影響評価・承認は別途未取得。` |
| `residualRisk` | `成功したfollow-on accessは未確認のまま。` |
| `reversibility` | `紙上案の訂正は可能。実通知の回収や実Blockの解除を実証したわけではない。` |
| `parentDecisionPreserved` | `true` |

### OPT-CTI26-B

| Field | Value |
|---|---|
| `id` | `OPT-CTI26-B` |
| `label` | `広い対象を一括で扱う案を棄却する` |
| `benefit` | `実効性は未検証で、広い範囲が有効という証拠はない。` |
| `cost` | `許可・Scope・誤検知の追加審査が必要。` |
| `disruption` | `第三者や無関係な業務へ影響する懸念がある。` |
| `residualRisk` | `帰属や成功可否のGapは解消しない。` |
| `reversibility` | `誤通知の影響を完全には戻せない。` |
| `parentDecisionPreserved` | `false` |

### OPT-CTI26-C

| Field | Value |
|---|---|
| `id` | `OPT-CTI26-C` |
| `label` | `不確実性を理由に全説明を保留する案を棄却する` |
| `benefit` | `断定の誤りは避けやすい。` |
| `cost` | `判断期限を逃す。` |
| `disruption` | `本教材では実操作なしだが、担当者への情報提供も遅れる。` |
| `residualRisk` | `限定的に言える事実とGapが意思決定へ渡らない。` |
| `reversibility` | `失われた判断時間は回復できない。` |
| `parentDecisionPreserved` | `false` |

### decision

| Field | Value |
|---|---|
| `id` | `DEC-CTI26-001` |
| `parentDecisionId` | `DEC-2026-025` |
| `status` | `synthetic-representation` |
| `selectedOptionId` | `OPT-CTI26-A` |
| `owner` | `SYNTH-CISO` |
| `productId` | `PRD-CTI26-EXEC` |
| `authorityGranted` | `false` |
| `executed` | `false` |
| `rationale` | `親Decisionを別の選択へ上書きせず、限定案・非帰属・未確定の成功可否を二Productで同じ意味に保つ。` |

### FDB-CTI26-TECH

| Field | Value |
|---|---|
| `id` | `FDB-CTI26-TECH` |
| `productId` | `PRD-CTI26-TECH` |
| `audience` | `SYNTH-SOC Lead` |
| `status` | `planned-not-received` |
| `question` | `Coverageの欠落と、検知対応付けが有効性の証明でないことを読者が区別できるか。` |
| `answer` | `null` |
| `receiptId` | `null` |

### FDB-CTI26-EXEC

| Field | Value |
|---|---|
| `id` | `FDB-CTI26-EXEC` |
| `productId` | `PRD-CTI26-EXEC` |
| `audience` | `SYNTH-CISO` |
| `status` | `planned-not-received` |
| `question` | `残余リスクと可逆性を踏まえて、親Decisionの案と実行承認が別であると理解できるか。` |
| `answer` | `null` |
| `receiptId` | `null` |

### reassessment

| Field | Value |
|---|---|
| `id` | `REA-CTI26-001` |
| `parentReassessmentId` | `REA-2026-025` |
| `at` | `2026-07-30T00:30:00Z` |
| `triggerGapIds/0` | `GAP-2026-025-001` |
| `triggerGapIds/1` | `GAP-2026-025-002` |
| `triggerGapIds/2` | `GAP-2026-025-003` |
| `triggerGapIds/3` | `GAP-2026-025-004` |
| `invalidation` | `独立した追加観測、Source訂正、Coverage欠落の拡大、翻訳の原文確認が判断を変える場合は再評価する。` |
| `onChange` | `旧版を配布対象から外し、訂正理由と影響KJを記録して新Product版を審査する。` |
| `supersedingProductId` | `null` |
| `stixObjectRevoked` | `false` |

### handoff

| Field | Value |
|---|---|
| `id` | `HOF-CTI26-029` |
| `chapter` | `29` |
| `audience` | `SYNTH-Capstone coordinator` |
| `productIds/0` | `PRD-CTI26-TECH` |
| `productIds/1` | `PRD-CTI26-EXEC` |
| `status` | `planned-not-delivered` |
| `receiptId` | `null` |
| `authorityGranted` | `false` |

### exchangeExample

| Field | Value |
|---|---|
| `id` | `CASE-STIX26-DEMO` |
| `relation` | `independent` |
| `purpose` | `structure-only-not-evidence` |
| `adoptedEvidenceIds` | `[]` |
| `contributesToJudgment` | `false` |
| `networkExecuted` | `false` |
| `bundleProfile` | `STIX21-STRUCTURE-ONLY` |
| `taxiiProfile` | `TAXII21-OFFLINE-ONLY` |

### ALT-CTI26-SUCCESS

| Field | Value |
|---|---|
| `id` | `ALT-CTI26-SUCCESS` |
| `focusQuestion` | `Q-CTI26-FOLLOWON` |
| `parentHypothesisId` | `TH-2026-025-003` |
| `statement` | `実際には成功したが、保持外または詳細Telemetryの欠落により確認できていない可能性。` |
| `evidenceIds/0` | `EVD-2026-025-008` |
| `gapIds/0` | `GAP-2026-025-001` |
| `disposition` | `unresolved` |

### ALT-CTI26-NO-SUCCESS

| Field | Value |
|---|---|
| `id` | `ALT-CTI26-NO-SUCCESS` |
| `focusQuestion` | `Q-CTI26-FOLLOWON` |
| `parentHypothesisId` | `TH-2026-025-003` |
| `statement` | `実際には成功していなかった可能性。供給summaryの不検出だけで確定しない。` |
| `evidenceIds/0` | `EVD-2026-025-008` |
| `gapIds/0` | `GAP-2026-025-001` |
| `disposition` | `unresolved` |

### ALT-CTI26-NEW-ORIGIN

| Field | Value |
|---|---|
| `id` | `ALT-CTI26-NEW-ORIGIN` |
| `focusQuestion` | `Q-CTI26-ORIGINS` |
| `parentHypothesisId` | `SEH-2026-025-001` |
| `statement` | `各報告に別原典や独自観測が存在する可能性を再評価条件として残す。供給lineageでは未支持。` |
| `evidenceIds/0` | `EVD-2026-025-004` |
| `evidenceIds/1` | `EVD-2026-025-005` |
| `evidenceIds/2` | `EVD-2026-025-007` |
| `gapIds/0` | `GAP-2026-025-002` |
| `disposition` | `not-supported-by-supplied-lineage` |

## 独立STIX構造例のObject一覧

この表のObjectはすべてCASE-STIX26-DEMOの設定であり、上のEvidence欄へ採用しません。型が表現するものと、個別主張の真偽を分ける練習です。Artifactは非実行JSONで、実在Actor・国家・被害者を含みません。

| Type | Object ID | 教材上の値・関係 |
|---|---|---|
| threat-actor | `threat-actor--f5b949d5-668a-4c36-a938-fbd5e8ba9dd4` | `SYNTH-Training Actor` |
| campaign | `campaign--40efeb2d-c0a1-4573-a953-aaf1abeab51b` | `SYNTH-Training Campaign` |
| malware | `malware--6b504777-6bcb-424b-870a-73e28d981fad` | `SYNTH-Training Malware Label` |
| infrastructure | `infrastructure--2d5912eb-2462-48a0-92e3-1c1f65f110fc` | `SYNTH-Training Infrastructure` |
| domain-name | `domain-name--7471572f-90bd-5053-9550-edb807c1ab17` | `relay-demo.example` |
| observed-data | `observed-data--907457b7-b097-45dc-8bf8-df7ba74f1ebc` | `1 supplied observation` |
| indicator | `indicator--0ac09c72-7c9c-450f-a789-0389c726ba10` | `SYNTH-Training Pattern` |
| attack-pattern | `attack-pattern--79fb7e3f-8a2c-4678-9eab-e27daedcbd6c` | `SYNTH-Training Behavior` |
| relationship | `relationship--71fbba92-c181-45aa-9ae8-6be9310f509a` | `合成関係の説明: source_ref=campaign--40efeb2d-c0a1-4573-a953-aaf1abeab51b; relationship_type=attributed-to; target_ref=threat-actor--f5b949d5-668a-4c36-a938-fbd5e8ba9dd4` |
| relationship | `relationship--fdaba7d7-b877-4d25-95af-3bcf1ce03087` | `合成関係の説明: source_ref=threat-actor--f5b949d5-668a-4c36-a938-fbd5e8ba9dd4; relationship_type=uses; target_ref=malware--6b504777-6bcb-424b-870a-73e28d981fad` |
| relationship | `relationship--b4332286-4ab9-4647-91b8-596a3729d743` | `合成関係の説明: source_ref=campaign--40efeb2d-c0a1-4573-a953-aaf1abeab51b; relationship_type=uses; target_ref=infrastructure--2d5912eb-2462-48a0-92e3-1c1f65f110fc` |
| relationship | `relationship--8637a454-e325-4b02-8916-5c277fda42d9` | `合成関係の説明: source_ref=campaign--40efeb2d-c0a1-4573-a953-aaf1abeab51b; relationship_type=uses; target_ref=attack-pattern--79fb7e3f-8a2c-4678-9eab-e27daedcbd6c` |
| relationship | `relationship--b65f4f93-74b5-470c-9510-2612246218ab` | `合成関係の説明: source_ref=indicator--0ac09c72-7c9c-450f-a789-0389c726ba10; relationship_type=indicates; target_ref=attack-pattern--79fb7e3f-8a2c-4678-9eab-e27daedcbd6c` |

## 検査結果の意味と安全な対比

`npm run check:chapter26`は供給13Object、TAXII envelope、Productの必須欄と有限意味を検査します。任意STIXの準拠認証、Pattern engine、実サーバー検査、権限認定ではありません。実APIへ接続しない。

- 良い対比: Productの表示順を入れ替えても、IDで結ぶKJ / Audience / Artifact / Feedbackは同じにする。
- 悪い対比: TECHとEXECのAudienceを協調して入れ替える、同じ原典を別観測にする、独立BundleのActorをEvidenceへ採用する。
- 失敗・反証: 期限より後に作ったProduct、存在しないObject参照、逆転した観測期間、BundleをObjects envelopeの一件として入れる例を拒否する。

全て合成の比較であり、実Dataが必要になれば停止します。終了時は自分の演習Copyと出力だけを整理し、供給資料や親Recordを上書きしません。

## Handoffと再評価

第29章向けHOF-CTI26-029はplanned-not-delivered、Receiptはnullです。Feedbackもplanned-not-receivedで、回答や受領証跡を作っていません。新しいSource、Coverage、訂正があれば旧Productをそのまま正しいとせず、影響KJとGapを明示して再審査します。Productの差替えとSTIX Objectのrevocationは別の処理です。
