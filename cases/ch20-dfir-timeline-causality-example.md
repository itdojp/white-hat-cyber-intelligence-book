# 第20章 TimelineとRoot Cause Analysis完全合成記入例

[第20章](../manuscript/20-dfir-timeline-causality.md)、[ART-07](../templates/incident-timeline.md)、[ART-26](../templates/root-cause-analysis.md)の記入例である。[供給JSON](fixtures/ch20-dfir-timeline-causality.json)と[閉じたSchema](../schemas/ch20-dfir-timeline-causality.schema.json)へ全欄を対応付ける。

## 読み方と境界

CASE-DFIR-2026-001はCASE-IR-2026-001をrefinesするが、親19の未配達Handoffを受領した記録ではない。親の予定TL-IR19-004と本章のTL-DFIR20-A/Bは別IDである。対象・版はSYNTH-DFIR20-001 / REV-DFIR20-001であり、実Incident、実Data、実Clock測定、実収集、実操作、実通知はない。

五つのReceiptは本書独自の供給形式で、製品Schemaではない。Clockのoffset・不確かさ・有効Window・利用可能時点も教育上の仮定である。payloadSha256は供給JSONの表現比較であり、実原本の真正性や実収集のChain of custodyを証明しない。原payloadを保持したまま、作業上の時刻区間を計算する。

## 二つのSnapshot

時刻はすべて2026-09-01 UTCである。原時刻のTimezoneは全欄表へ残す。

| Timeline | Cutoff / Analysis | Receipt / Event | 保守説明と原因 |
|---|---|---|---|
| TL-DFIR20-A | 08:10 / 08:12 | 4 Receipt / 3 Event | EV20-005は後着で不採用。特定Changeの範囲は未確定、原因unresolved |
| TL-DFIR20-B | 08:35 / 08:36 | 5 Receipt / 4 Event | 特定CHG20-001はApp BだけでApp Aを覆わない。別の許可と機構は不明、原因unresolved |

EV20-002/004は同一Source・Event ID・payloadの再送である。Receiptは消さず、一つのEventへ束ねる。EV20-001は07:59:40〜08:00:40、EV20-002は07:59:50〜08:00:50の区間であり、中心値や到着順から前後を確定しない。表示表のSource ID順は時系列ではない。

## Claimの読み取り

| Claim | 問い | A | B |
|---|---|---|---|
| CLM20-001 | 同意変更Before APIか | 未確定・区間重なり | 同じGapを保持 |
| CLM20-002 | 保守予定Before 同意変更か | 供給モデル内で支持 | 支持を保持 |
| CLM20-003 | CHG20-001がAPI利用を覆うか | 後着Evidenceのため未確定 | このChangeについて反証 |
| CLM20-004 | 同意変更が利用を可能にした原因か | 機構と代替の不足 | 同じGapを保持 |
| CLM20-005 | API Before保守予定という主張か | 反証・実際の区間関係はAfter | 反証を保持 |
| CLM20-006 | 同意変更とAPIがConcurrentか | 同時性の独立根拠なし | 同じGapを保持 |

反証は特定の主張に対するものである。CLM20-003の反証は、すべての正当な説明の不存在、実在主体の悪意、Root Causeを証明しない。RCAの低い確信度、Unknown scopeのData D、四つのGapをA/Bの両方に残す。

## 全欄の読み方

以下は原Evidenceも含む全Fieldの記入値である。TemplateのTimeline entriesはsnapshotsのexpected/timelineへ、ClaimとGapはexpected/claimsへ、ART-26は各Snapshotのrcaへ対応する。空配列やnullを完了・受領に読み替えない。JSONのexpectedは独立に記述した教材期待値であり、実観測の証拠ではない。

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
| `id` | `DFIR-2026-020-001` |
| `incidentId` | `null` |
| `incidentReferenceStatus` | `not-declared-in-this-bundle` |
| `timeStandard` | `UTC; original timezone offsets retained` |
| `caseId` | `CASE-DFIR-2026-001` |
| `parentCaseId` | `CASE-IR-2026-001` |
| `relation` | `refines` |
| `artifactIds/0` | `ART-07` |
| `artifactIds/1` | `ART-26` |
| `asOf` | `2026-09-25T00:00:00Z` |
| `sourceIds/0` | `SRC-NIST-DFIR-001` |
| `sourceIds/1` | `SRC-IR-001` |
| `sourceIds/2` | `SRC-BERKELEY-001` |
| `actualIncidents` | `0` |
| `actualCollections` | `0` |
| `actualActions` | `0` |
| `actualNotifications` | `0` |

### parent

| Field | Value |
|---|---|
| `recordId` | `IAP-2026-019-001` |
| `contrastId` | `ICASE19-004` |
| `decisionId` | `DEC-IR19-004` |
| `handoffId` | `HOF-IR19-004-20` |
| `questionId` | `EQ-IR19-004-20` |
| `plannedTimelineId` | `TL-IR19-004` |
| `status` | `planned-not-delivered` |
| `receiptId` | `null` |
| `executionAuthorized` | `false` |
| `use` | `method-reference-only` |

### context

| Field | Value |
|---|---|
| `subjectId` | `SYNTH-DFIR20-001` |
| `revision` | `REV-DFIR20-001` |
| `windowStart` | `2026-09-01T07:50:00Z` |
| `windowEnd` | `2026-09-01T08:10:00Z` |
| `assets/0` | `SYN-DFIR-APP-A` |
| `assets/1` | `SYN-DFIR-APP-B` |
| `assets/2` | `SYN-DFIR-DATA-D` |
| `actors/0` | `SYN-DFIR-ADMIN` |
| `actors/1` | `SYN-DFIR-WORKLOAD` |
| `actors/2` | `SYN-DFIR-REVIEWER` |
| `sessions/0` | `SYN-ADMIN-SESSION` |
| `sessions/1` | `SYN-WORKLOAD-SESSION` |
| `sessions/2` | `SYN-REVIEW-SESSION` |

### roles

| Field | Value |
|---|---|
| `analysisOwner` | `SYN-DFIR-ANALYSIS-OWNER` |
| `evidenceLead` | `SYN-DFIR-EVIDENCE-LEAD` |

### provenance

| Field | Value |
|---|---|
| `id` | `SYN-PRESERVE20-001` |
| `origin` | `synthetic-authored` |
| `custodian` | `SYN-DFIR-EVIDENCE-LEAD` |
| `originalFormat` | `supplied JSON payload` |
| `originalRetained` | `true` |
| `workingCopyOnly` | `true` |
| `transformations/0` | `timezone-to-UTC` |
| `transformations/1` | `subtract-declared-offset` |
| `transformations/2` | `closed-uncertainty-interval` |
| `hashMeaning` | `Canonical JSON payloadの表現比較のみ。真正性・実収集・実権限を証明しない。` |
| `handling` | `全Recordは教材内で創作した仮定であり、実Custodyや実Data保持の完了を表さない。` |

### SYN-SOURCE20-ID

| Field | Value |
|---|---|
| `id` | `SYN-SOURCE20-ID` |
| `purpose` | `同意変更を表す供給Record` |
| `custodyRef` | `SYN-PRESERVE20-001` |
| `limitation` | `Actor IDは実在人物の同定でも操作許可でもない。` |

### SYN-SOURCE20-API

| Field | Value |
|---|---|
| `id` | `SYN-SOURCE20-API` |
| `purpose` | `Workloadの利用を表す供給Record` |
| `custodyRef` | `SYN-PRESERVE20-001` |
| `limitation` | `記録一件は全取得Dataや全影響の証明ではない。` |

### SYN-SOURCE20-ADMIN

| Field | Value |
|---|---|
| `id` | `SYN-SOURCE20-ADMIN` |
| `purpose` | `保守予定を表す供給Record` |
| `custodyRef` | `SYN-PRESERVE20-001` |
| `limitation` | `予定の存在は対象一致や実施確認ではない。` |

### SYN-SOURCE20-CHANGE

| Field | Value |
|---|---|
| `id` | `SYN-SOURCE20-CHANGE` |
| `purpose` | `特定Changeの承認範囲を表す後着Record` |
| `custodyRef` | `SYN-PRESERVE20-001` |
| `limitation` | `CHG20-001以外の許可の存否は分からない。` |

### CLK20-ID

| Field | Value |
|---|---|
| `id` | `CLK20-ID` |
| `sourceId` | `SYN-SOURCE20-ID` |
| `offsetSeconds` | `30` |
| `uncertaintySeconds` | `30` |
| `validFrom` | `2026-09-01T07:50:00Z` |
| `validUntil` | `2026-09-01T08:10:00Z` |
| `availableAt` | `2026-09-01T07:49:00Z` |
| `basis` | `供給された時刻モデルの仮定。量子化・driftを含む総幅であり実測・校正証明ではない。` |

### CLK20-API

| Field | Value |
|---|---|
| `id` | `CLK20-API` |
| `sourceId` | `SYN-SOURCE20-API` |
| `offsetSeconds` | `-10` |
| `uncertaintySeconds` | `30` |
| `validFrom` | `2026-09-01T07:50:00Z` |
| `validUntil` | `2026-09-01T08:10:00Z` |
| `availableAt` | `2026-09-01T07:49:00Z` |
| `basis` | `供給された時刻モデルの仮定。量子化・driftを含む総幅であり実測・校正証明ではない。` |

### CLK20-ADMIN

| Field | Value |
|---|---|
| `id` | `CLK20-ADMIN` |
| `sourceId` | `SYN-SOURCE20-ADMIN` |
| `offsetSeconds` | `0` |
| `uncertaintySeconds` | `1` |
| `validFrom` | `2026-09-01T07:50:00Z` |
| `validUntil` | `2026-09-01T08:10:00Z` |
| `availableAt` | `2026-09-01T07:49:00Z` |
| `basis` | `供給された時刻モデルの仮定。量子化・driftを含む総幅であり実測・校正証明ではない。` |

### CLK20-CHANGE

| Field | Value |
|---|---|
| `id` | `CLK20-CHANGE` |
| `sourceId` | `SYN-SOURCE20-CHANGE` |
| `offsetSeconds` | `0` |
| `uncertaintySeconds` | `1` |
| `validFrom` | `2026-09-01T07:50:00Z` |
| `validUntil` | `2026-09-01T08:10:00Z` |
| `availableAt` | `2026-09-01T07:49:00Z` |
| `basis` | `供給された時刻モデルの仮定。量子化・driftを含む総幅であり実測・校正証明ではない。` |

### EV20-001

| Field | Value |
|---|---|
| `id` | `EV20-001` |
| `sourceId` | `SYN-SOURCE20-ID` |
| `eventId` | `EVENT-ID-001` |
| `payload/subjectId` | `SYNTH-DFIR20-001` |
| `payload/revision` | `REV-DFIR20-001` |
| `payload/assetId` | `SYN-DFIR-APP-A` |
| `payload/actorId` | `SYN-DFIR-ADMIN` |
| `payload/sessionId` | `SYN-ADMIN-SESSION` |
| `payload/operation` | `consent-change` |
| `payload/originalTime` | `2026-09-01T17:00:40+09:00` |
| `payload/clockId` | `CLK20-ID` |
| `payload/detail/permission` | `SYNTH-PERM-READ` |
| `payload/detail/observation` | `同意変更Recordが供給されている。` |
| `payloadSha256` | `2664e85ee2c09c56bc61c415eb897c8a012e81db9b344ab5e495aae76659ef9b` |
| `collectedAt` | `2026-09-01T08:06:00Z` |
| `ingestedAt` | `2026-09-01T08:06:30Z` |
| `availableAt` | `2026-09-01T08:07:00Z` |
| `preservationRef` | `SYN-PRESERVE20-001` |

### EV20-002

| Field | Value |
|---|---|
| `id` | `EV20-002` |
| `sourceId` | `SYN-SOURCE20-API` |
| `eventId` | `EVENT-API-001` |
| `payload/subjectId` | `SYNTH-DFIR20-001` |
| `payload/revision` | `REV-DFIR20-001` |
| `payload/assetId` | `SYN-DFIR-APP-A` |
| `payload/actorId` | `SYN-DFIR-WORKLOAD` |
| `payload/sessionId` | `SYN-WORKLOAD-SESSION` |
| `payload/operation` | `api-read` |
| `payload/originalTime` | `2026-09-01T08:00:10Z` |
| `payload/clockId` | `CLK20-API` |
| `payload/detail/resource` | `SYNTH-RESOURCE-A` |
| `payload/detail/observation` | `一件のAPI利用Recordが供給されている。` |
| `payloadSha256` | `cd80778b1311a95f6d8d4948c2626ac86bd33c45067293deb80aa61dfbd9ceba` |
| `collectedAt` | `2026-09-01T08:03:00Z` |
| `ingestedAt` | `2026-09-01T08:03:30Z` |
| `availableAt` | `2026-09-01T08:04:00Z` |
| `preservationRef` | `SYN-PRESERVE20-001` |

### EV20-003

| Field | Value |
|---|---|
| `id` | `EV20-003` |
| `sourceId` | `SYN-SOURCE20-ADMIN` |
| `eventId` | `EVENT-ADMIN-001` |
| `payload/subjectId` | `SYNTH-DFIR20-001` |
| `payload/revision` | `REV-DFIR20-001` |
| `payload/assetId` | `SYN-DFIR-APP-A` |
| `payload/actorId` | `SYN-DFIR-ADMIN` |
| `payload/sessionId` | `SYN-ADMIN-SESSION` |
| `payload/operation` | `admin-maintenance` |
| `payload/originalTime` | `2026-09-01T07:58:00Z` |
| `payload/clockId` | `CLK20-ADMIN` |
| `payload/detail/changeId` | `CHG20-001` |
| `payload/detail/observation` | `保守予定が記録されている。承認範囲はこのRecordにない。` |
| `payloadSha256` | `30ca714bfc79812d76c5db7e32926ff0ccb6314e3b453cdb7d0cbbd9e5a1f0c9` |
| `collectedAt` | `2026-09-01T08:01:00Z` |
| `ingestedAt` | `2026-09-01T08:01:30Z` |
| `availableAt` | `2026-09-01T08:02:00Z` |
| `preservationRef` | `SYN-PRESERVE20-001` |

### EV20-004

| Field | Value |
|---|---|
| `id` | `EV20-004` |
| `sourceId` | `SYN-SOURCE20-API` |
| `eventId` | `EVENT-API-001` |
| `payload/subjectId` | `SYNTH-DFIR20-001` |
| `payload/revision` | `REV-DFIR20-001` |
| `payload/assetId` | `SYN-DFIR-APP-A` |
| `payload/actorId` | `SYN-DFIR-WORKLOAD` |
| `payload/sessionId` | `SYN-WORKLOAD-SESSION` |
| `payload/operation` | `api-read` |
| `payload/originalTime` | `2026-09-01T08:00:10Z` |
| `payload/clockId` | `CLK20-API` |
| `payload/detail/resource` | `SYNTH-RESOURCE-A` |
| `payload/detail/observation` | `一件のAPI利用Recordが供給されている。` |
| `payloadSha256` | `cd80778b1311a95f6d8d4948c2626ac86bd33c45067293deb80aa61dfbd9ceba` |
| `collectedAt` | `2026-09-01T08:08:00Z` |
| `ingestedAt` | `2026-09-01T08:08:30Z` |
| `availableAt` | `2026-09-01T08:09:00Z` |
| `preservationRef` | `SYN-PRESERVE20-001` |

### EV20-005

| Field | Value |
|---|---|
| `id` | `EV20-005` |
| `sourceId` | `SYN-SOURCE20-CHANGE` |
| `eventId` | `EVENT-CHANGE-001` |
| `payload/subjectId` | `SYNTH-DFIR20-001` |
| `payload/revision` | `REV-DFIR20-001` |
| `payload/assetId` | `SYN-DFIR-APP-B` |
| `payload/actorId` | `SYN-DFIR-REVIEWER` |
| `payload/sessionId` | `SYN-REVIEW-SESSION` |
| `payload/operation` | `change-scope` |
| `payload/originalTime` | `2026-09-01T07:55:00Z` |
| `payload/clockId` | `CLK20-CHANGE` |
| `payload/detail/changeId` | `CHG20-001` |
| `payload/detail/approvedAssets/0` | `SYN-DFIR-APP-B` |
| `payload/detail/windowStart` | `2026-09-01T07:50:00Z` |
| `payload/detail/windowEnd` | `2026-09-01T08:10:00Z` |
| `payload/detail/observation` | `この供給Changeの対象はApp Bだけである。` |
| `payloadSha256` | `3f85f8ebf263ec0dace6b328260fa9bdb93a2d03ecdde7159ccc14ea6e4d23df` |
| `collectedAt` | `2026-09-01T08:29:00Z` |
| `ingestedAt` | `2026-09-01T08:29:30Z` |
| `availableAt` | `2026-09-01T08:30:00Z` |
| `preservationRef` | `SYN-PRESERVE20-001` |

### CLM20-001

| Field | Value |
|---|---|
| `id` | `CLM20-001` |
| `questionId` | `EQ20-001` |
| `kind` | `order` |
| `evidenceIds/0` | `EV20-001` |
| `evidenceIds/1` | `EV20-002` |
| `assertedRelation` | `Before` |
| `changeId` | `null` |
| `question` | `同意変更はAPI利用より前か。` |

### CLM20-002

| Field | Value |
|---|---|
| `id` | `CLM20-002` |
| `questionId` | `EQ20-002` |
| `kind` | `order` |
| `evidenceIds/0` | `EV20-003` |
| `evidenceIds/1` | `EV20-001` |
| `assertedRelation` | `Before` |
| `changeId` | `null` |
| `question` | `保守予定Recordは同意変更より前か。` |

### CLM20-003

| Field | Value |
|---|---|
| `id` | `CLM20-003` |
| `questionId` | `EQ20-003` |
| `kind` | `change-covers` |
| `evidenceIds/0` | `EV20-005` |
| `evidenceIds/1` | `EV20-002` |
| `assertedRelation` | `null` |
| `changeId` | `CHG20-001` |
| `question` | `このAPI利用のAssetと時刻幅は、特定CHG20-001の対象資産・時間窓に含まれるか。操作の実行許可とは別である。` |

### CLM20-004

| Field | Value |
|---|---|
| `id` | `CLM20-004` |
| `questionId` | `EQ20-004` |
| `kind` | `causal-link` |
| `evidenceIds/0` | `EV20-001` |
| `evidenceIds/1` | `EV20-002` |
| `assertedRelation` | `null` |
| `changeId` | `null` |
| `question` | `同意変更がAPI利用を可能にした原因といえるか。` |

### CLM20-005

| Field | Value |
|---|---|
| `id` | `CLM20-005` |
| `questionId` | `EQ20-005` |
| `kind` | `order` |
| `evidenceIds/0` | `EV20-002` |
| `evidenceIds/1` | `EV20-003` |
| `assertedRelation` | `Before` |
| `changeId` | `null` |
| `question` | `API利用は保守予定Recordより前という主張を支持できるか。` |

### CLM20-006

| Field | Value |
|---|---|
| `id` | `CLM20-006` |
| `questionId` | `EQ20-006` |
| `kind` | `order` |
| `evidenceIds/0` | `EV20-001` |
| `evidenceIds/1` | `EV20-002` |
| `assertedRelation` | `Concurrent` |
| `changeId` | `null` |
| `question` | `同意変更とAPI利用の同時性を確定できるか。` |

### TL-DFIR20-A

| Field | Value |
|---|---|
| `id` | `TL-DFIR20-A` |
| `cutoff` | `2026-09-01T08:10:00Z` |
| `analysisAt` | `2026-09-01T08:12:00Z` |
| `owner` | `SYN-DFIR-ANALYSIS-OWNER` |
| `expected/included/0` | `EV20-001` |
| `expected/included/1` | `EV20-002` |
| `expected/included/2` | `EV20-003` |
| `expected/included/3` | `EV20-004` |
| `expected/excluded/0` | `EV20-005` |
| `expected/timeline/0/sourceId` | `SYN-SOURCE20-ADMIN` |
| `expected/timeline/0/eventId` | `EVENT-ADMIN-001` |
| `expected/timeline/0/evidenceIds/0` | `EV20-003` |
| `expected/timeline/0/intervalStart` | `2026-09-01T07:57:59Z` |
| `expected/timeline/0/intervalEnd` | `2026-09-01T07:58:01Z` |
| `expected/timeline/1/sourceId` | `SYN-SOURCE20-API` |
| `expected/timeline/1/eventId` | `EVENT-API-001` |
| `expected/timeline/1/evidenceIds/0` | `EV20-002` |
| `expected/timeline/1/evidenceIds/1` | `EV20-004` |
| `expected/timeline/1/intervalStart` | `2026-09-01T07:59:50Z` |
| `expected/timeline/1/intervalEnd` | `2026-09-01T08:00:50Z` |
| `expected/timeline/2/sourceId` | `SYN-SOURCE20-ID` |
| `expected/timeline/2/eventId` | `EVENT-ID-001` |
| `expected/timeline/2/evidenceIds/0` | `EV20-001` |
| `expected/timeline/2/intervalStart` | `2026-09-01T07:59:40Z` |
| `expected/timeline/2/intervalEnd` | `2026-09-01T08:00:40Z` |
| `expected/claims/CLM20-001/status` | `undetermined` |
| `expected/claims/CLM20-001/relation` | `Possibly related` |
| `expected/claims/CLM20-001/gaps/0` | `clock-order-uncertain` |
| `expected/claims/CLM20-002/status` | `supported` |
| `expected/claims/CLM20-002/relation` | `Before` |
| `expected/claims/CLM20-002/gaps` | `[]` |
| `expected/claims/CLM20-003/status` | `undetermined` |
| `expected/claims/CLM20-003/relation` | `null` |
| `expected/claims/CLM20-003/gaps/0` | `not-available:EV20-005` |
| `expected/claims/CLM20-004/status` | `undetermined` |
| `expected/claims/CLM20-004/relation` | `null` |
| `expected/claims/CLM20-004/gaps/0` | `mechanism-not-supplied` |
| `expected/claims/CLM20-004/gaps/1` | `alternative-not-eliminated` |
| `expected/claims/CLM20-005/status` | `contradicted` |
| `expected/claims/CLM20-005/relation` | `After` |
| `expected/claims/CLM20-005/gaps` | `[]` |
| `expected/claims/CLM20-006/status` | `undetermined` |
| `expected/claims/CLM20-006/relation` | `Possibly related` |
| `expected/claims/CLM20-006/gaps/0` | `independent-simultaneity-evidence` |
| `rca/id` | `RCA-DFIR20-A` |
| `rca/timelineId` | `TL-DFIR20-A` |
| `rca/problemStatement` | `同意変更とAPI利用の関係、限定影響、保守による説明の可否を区別する。` |
| `rca/triggerEvidenceId` | `EV20-001` |
| `rca/rootConditionHypothesis` | `認可条件の欠落という仮説はあるが機構を示す記録がない。` |
| `rca/rootCauseStatus` | `unresolved` |
| `rca/causalClaimId` | `CLM20-004` |
| `rca/contributingEvidenceIds/0` | `EV20-001` |
| `rca/contributingEvidenceIds/1` | `EV20-002` |
| `rca/contributingFactor` | `同意変更のreceiptはAPIより後着した。分析順序への寄与と事案の原因は別である。` |
| `rca/impactEvidenceIds/0` | `EV20-002` |
| `rca/observedScope/0` | `SYN-DFIR-APP-A` |
| `rca/unknownScope/0` | `SYN-DFIR-DATA-D` |
| `rca/confidence` | `low` |
| `rca/confidenceReason` | `時刻幅が重なり、認可機構と他の許可・操作目的が未供給である。` |
| `rca/alternatives/0/id` | `HYP20-MAINT` |
| `rca/alternatives/0/claimId` | `CLM20-003` |
| `rca/alternatives/0/disposition` | `not-yet-testable` |
| `rca/alternatives/0/remainingGap` | `特定CHG20-001以外の許可や保守の存否は不明。` |
| `rca/alternatives/1/id` | `HYP20-MISUSE` |
| `rca/alternatives/1/claimId` | `CLM20-004` |
| `rca/alternatives/1/disposition` | `not-established` |
| `rca/alternatives/1/remainingGap` | `Actorの目的と利用可能化の機構は未供給。` |
| `rca/alternatives/2/id` | `HYP20-ORDER` |
| `rca/alternatives/2/claimId` | `CLM20-001` |
| `rca/alternatives/2/disposition` | `order-uncertain` |
| `rca/alternatives/2/remainingGap` | `Collector到着順とEvent順は一致するとは限らない。` |
| `rca/evidenceGaps/0` | `GAP20-MECHANISM` |
| `rca/evidenceGaps/1` | `GAP20-OTHER-AUTHORITY` |
| `rca/evidenceGaps/2` | `GAP20-UNKNOWN-SCOPE` |
| `rca/evidenceGaps/3` | `GAP20-CLOCK-ORDER` |
| `rca/controlFailureStatus` | `hypothesis-only` |
| `rca/correctiveAction` | `認可判定根拠と変更対象の対応を検証する計画を作る。実変更は行わない。` |
| `rca/controlId` | `CTL-DFIR20-001` |
| `rca/validationRequirement` | `同一対象・版・Windowにおける判定根拠、変更前後と反例を別記する。` |
| `rca/owner` | `SYN-DFIR-ANALYSIS-OWNER` |
| `rca/dueAt` | `2026-09-30T00:00:00Z` |
| `rca/reassessmentId` | `REA-DFIR20-A` |
| `rca/invalidation` | `別の許可、機構を示す記録、Clock条件または対象版が変われば旧判断を残して新しいSnapshotを作る。` |
| `rca/recoveryStatus` | `not-assessed` |
| `rca/actualChanges` | `0` |

### TL-DFIR20-B

| Field | Value |
|---|---|
| `id` | `TL-DFIR20-B` |
| `cutoff` | `2026-09-01T08:35:00Z` |
| `analysisAt` | `2026-09-01T08:36:00Z` |
| `owner` | `SYN-DFIR-ANALYSIS-OWNER` |
| `expected/included/0` | `EV20-001` |
| `expected/included/1` | `EV20-002` |
| `expected/included/2` | `EV20-003` |
| `expected/included/3` | `EV20-004` |
| `expected/included/4` | `EV20-005` |
| `expected/excluded` | `[]` |
| `expected/timeline/0/sourceId` | `SYN-SOURCE20-ADMIN` |
| `expected/timeline/0/eventId` | `EVENT-ADMIN-001` |
| `expected/timeline/0/evidenceIds/0` | `EV20-003` |
| `expected/timeline/0/intervalStart` | `2026-09-01T07:57:59Z` |
| `expected/timeline/0/intervalEnd` | `2026-09-01T07:58:01Z` |
| `expected/timeline/1/sourceId` | `SYN-SOURCE20-API` |
| `expected/timeline/1/eventId` | `EVENT-API-001` |
| `expected/timeline/1/evidenceIds/0` | `EV20-002` |
| `expected/timeline/1/evidenceIds/1` | `EV20-004` |
| `expected/timeline/1/intervalStart` | `2026-09-01T07:59:50Z` |
| `expected/timeline/1/intervalEnd` | `2026-09-01T08:00:50Z` |
| `expected/timeline/2/sourceId` | `SYN-SOURCE20-CHANGE` |
| `expected/timeline/2/eventId` | `EVENT-CHANGE-001` |
| `expected/timeline/2/evidenceIds/0` | `EV20-005` |
| `expected/timeline/2/intervalStart` | `2026-09-01T07:54:59Z` |
| `expected/timeline/2/intervalEnd` | `2026-09-01T07:55:01Z` |
| `expected/timeline/3/sourceId` | `SYN-SOURCE20-ID` |
| `expected/timeline/3/eventId` | `EVENT-ID-001` |
| `expected/timeline/3/evidenceIds/0` | `EV20-001` |
| `expected/timeline/3/intervalStart` | `2026-09-01T07:59:40Z` |
| `expected/timeline/3/intervalEnd` | `2026-09-01T08:00:40Z` |
| `expected/claims/CLM20-001/status` | `undetermined` |
| `expected/claims/CLM20-001/relation` | `Possibly related` |
| `expected/claims/CLM20-001/gaps/0` | `clock-order-uncertain` |
| `expected/claims/CLM20-002/status` | `supported` |
| `expected/claims/CLM20-002/relation` | `Before` |
| `expected/claims/CLM20-002/gaps` | `[]` |
| `expected/claims/CLM20-003/status` | `contradicted` |
| `expected/claims/CLM20-003/relation` | `null` |
| `expected/claims/CLM20-003/gaps` | `[]` |
| `expected/claims/CLM20-004/status` | `undetermined` |
| `expected/claims/CLM20-004/relation` | `null` |
| `expected/claims/CLM20-004/gaps/0` | `mechanism-not-supplied` |
| `expected/claims/CLM20-004/gaps/1` | `alternative-not-eliminated` |
| `expected/claims/CLM20-005/status` | `contradicted` |
| `expected/claims/CLM20-005/relation` | `After` |
| `expected/claims/CLM20-005/gaps` | `[]` |
| `expected/claims/CLM20-006/status` | `undetermined` |
| `expected/claims/CLM20-006/relation` | `Possibly related` |
| `expected/claims/CLM20-006/gaps/0` | `independent-simultaneity-evidence` |
| `rca/id` | `RCA-DFIR20-B` |
| `rca/timelineId` | `TL-DFIR20-B` |
| `rca/problemStatement` | `同意変更とAPI利用の関係、限定影響、保守による説明の可否を区別する。` |
| `rca/triggerEvidenceId` | `EV20-001` |
| `rca/rootConditionHypothesis` | `認可条件の欠落という仮説はあるが機構を示す記録がない。` |
| `rca/rootCauseStatus` | `unresolved` |
| `rca/causalClaimId` | `CLM20-004` |
| `rca/contributingEvidenceIds/0` | `EV20-001` |
| `rca/contributingEvidenceIds/1` | `EV20-002` |
| `rca/contributingFactor` | `同意変更のreceiptはAPIより後着した。分析順序への寄与と事案の原因は別である。` |
| `rca/impactEvidenceIds/0` | `EV20-002` |
| `rca/observedScope/0` | `SYN-DFIR-APP-A` |
| `rca/unknownScope/0` | `SYN-DFIR-DATA-D` |
| `rca/confidence` | `low` |
| `rca/confidenceReason` | `時刻幅が重なり、認可機構と他の許可・操作目的が未供給である。` |
| `rca/alternatives/0/id` | `HYP20-MAINT` |
| `rca/alternatives/0/claimId` | `CLM20-003` |
| `rca/alternatives/0/disposition` | `contradicted-for-this-change` |
| `rca/alternatives/0/remainingGap` | `特定CHG20-001以外の許可や保守の存否は不明。` |
| `rca/alternatives/1/id` | `HYP20-MISUSE` |
| `rca/alternatives/1/claimId` | `CLM20-004` |
| `rca/alternatives/1/disposition` | `not-established` |
| `rca/alternatives/1/remainingGap` | `Actorの目的と利用可能化の機構は未供給。` |
| `rca/alternatives/2/id` | `HYP20-ORDER` |
| `rca/alternatives/2/claimId` | `CLM20-001` |
| `rca/alternatives/2/disposition` | `order-uncertain` |
| `rca/alternatives/2/remainingGap` | `Collector到着順とEvent順は一致するとは限らない。` |
| `rca/evidenceGaps/0` | `GAP20-MECHANISM` |
| `rca/evidenceGaps/1` | `GAP20-OTHER-AUTHORITY` |
| `rca/evidenceGaps/2` | `GAP20-UNKNOWN-SCOPE` |
| `rca/evidenceGaps/3` | `GAP20-CLOCK-ORDER` |
| `rca/controlFailureStatus` | `hypothesis-only` |
| `rca/correctiveAction` | `認可判定根拠と変更対象の対応を検証する計画を作る。実変更は行わない。` |
| `rca/controlId` | `CTL-DFIR20-001` |
| `rca/validationRequirement` | `同一対象・版・Windowにおける判定根拠、変更前後と反例を別記する。` |
| `rca/owner` | `SYN-DFIR-ANALYSIS-OWNER` |
| `rca/dueAt` | `2026-09-30T00:00:00Z` |
| `rca/reassessmentId` | `REA-DFIR20-B` |
| `rca/invalidation` | `別の許可、機構を示す記録、Clock条件または対象版が変われば旧判断を残して新しいSnapshotを作る。` |
| `rca/recoveryStatus` | `not-assessed` |
| `rca/actualChanges` | `0` |

### HOF-DFIR20-21

| Field | Value |
|---|---|
| `id` | `HOF-DFIR20-21` |
| `targetChapter` | `21` |
| `sourceRcaId` | `RCA-DFIR20-B` |
| `sourceTimelineId` | `TL-DFIR20-B` |
| `controlId` | `CTL-DFIR20-001` |
| `questionId` | `EQ-DFIR20-H21` |
| `question` | `Control不備の仮説をどの安全な供給反例で比較するか。` |
| `scope` | `SYNTH-DFIR20-001 / REV-DFIR20-001のみ。親のEvidenceを移送しない。` |
| `owner` | `SYN-DFIR-ANALYSIS-OWNER` |
| `dueAt` | `2026-09-30T00:00:00Z` |
| `status` | `planned-not-delivered` |
| `receiptId` | `null` |
| `executionAuthorized` | `false` |

### HOF-DFIR20-22

| Field | Value |
|---|---|
| `id` | `HOF-DFIR20-22` |
| `targetChapter` | `22` |
| `sourceRcaId` | `RCA-DFIR20-B` |
| `sourceTimelineId` | `TL-DFIR20-B` |
| `controlId` | `CTL-DFIR20-001` |
| `questionId` | `EQ-DFIR20-H22` |
| `question` | `改善案のOwner、受入基準、再評価をどう管理するか。` |
| `scope` | `SYNTH-DFIR20-001 / REV-DFIR20-001のみ。親のEvidenceを移送しない。` |
| `owner` | `SYN-DFIR-ANALYSIS-OWNER` |
| `dueAt` | `2026-09-30T00:00:00Z` |
| `status` | `planned-not-delivered` |
| `receiptId` | `null` |
| `executionAuthorized` | `false` |

### HOF-DFIR20-25

| Field | Value |
|---|---|
| `id` | `HOF-DFIR20-25` |
| `targetChapter` | `25` |
| `sourceRcaId` | `RCA-DFIR20-B` |
| `sourceTimelineId` | `TL-DFIR20-B` |
| `controlId` | `CTL-DFIR20-001` |
| `questionId` | `EQ-DFIR20-H25` |
| `question` | `残る代替説明とUnknown scopeをどの根拠で更新するか。` |
| `scope` | `SYNTH-DFIR20-001 / REV-DFIR20-001のみ。親のEvidenceを移送しない。` |
| `owner` | `SYN-DFIR-ANALYSIS-OWNER` |
| `dueAt` | `2026-09-30T00:00:00Z` |
| `status` | `planned-not-delivered` |
| `receiptId` | `null` |
| `executionAuthorized` | `false` |

### safety

| Field | Value |
|---|---|
| `mode` | `offline-record-only` |
| `stop` | `実Data、個人情報、実Credential、外部対象、許可不明の追加収集を要する場合は停止する。` |
| `cleanup` | `配布資料の読解だけなので実Runtimeの停止・破棄はない。自分の解答Copyを保持条件に従い整理し、配布原本は変更しない。` |
| `limitations` | `有限の教材検査であり、真正性・完全性・裁判上の適格性・原因・実在主体の同定を自動認定しない。` |

## 提出時の確認

原時刻とClock条件、Cutoff、来歴、重複の保持、Relationの根拠、原因未確定の理由を指し示す。Controlは仮説・改善案、復旧は未評価で、全三Handoffは未配達/null/実権限falseである。第21・22・25章の成果や親19の状態を先取りしない。自分の解答Copyだけを整理し、配布原本・親Evidence・実ログを変更しない。
