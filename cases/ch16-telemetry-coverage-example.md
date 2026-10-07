# 第16章 完全合成記入例：Telemetry Coverage Map

## この記入例の扱い

ART-24 / TCM-2026-016の完全合成・読み取り専用教材である。以下の十行は独立した対比であり、一つの実収集が順に進んだ履歴ではない。対象APP-TCM16-001は親の現在の実装ではない。実Log・実User・実IP・実Token・PIIは使用しない。

[本文](../manuscript/16-telemetry-evidence-readiness.md) / [空Template](../templates/telemetry-coverage-map.md) / [供給JSON](fixtures/ch16-telemetry-coverage.json) / [閉Schema](../schemas/ch16-telemetry-coverage.schema.json)。配布JSONは非実行Dataであり、schemaだけで実権限やEvidenceの真正性を認定しない。

親5/6/15/17への参照は問いと記録方法の参照に限定する。親のEvidence・Authorityは移転せず、HOF-FRT15-16のplanned-not-delivered、既存DVR/DET/TEL/fixtureは保持する。このMapの成立から第17章の検知全体やHandoffの受領を先取りしない。

## 十の判断例

| Row | Consumer / 問い | Coverage | 許される結論 |
|---|---|---|---|
| ROW-TCM16-001 | Detection / 同意変更入力の限定Field検査 | Validated | bounded-input-contract-satisfied |
| ROW-TCM16-002 | Detection / 生成とCollector到着を分ける | Produced | collector-evidence-missing |
| ROW-TCM16-003 | IR / 判断期限までの保持不足 | Collected | retention-gap |
| ROW-TCM16-004 | Audit / 保持済みでも検索根拠がない | Retained | query-evidence-missing |
| ROW-TCM16-005 | Hunt / 相関Windowより時刻誤差が大きい | Queryable | clock-uncertainty |
| ROW-TCM16-006 | Hunt / 同じID文字列でも正規化版が違う | Queryable | identity-normalization-mismatch |
| ROW-TCM16-007 | Hunt / Workload API Eventを必要とするが未生成 | Required | producer-evidence-missing |
| ROW-TCM16-008 | IR / Authentication contextの取扱根拠が未確認 | Unknown | privacy-basis-unknown |
| ROW-TCM16-009 | DFIR / 同意変更の入力はあるが調査用保持が不足 | Collected | retention-gap |
| ROW-TCM16-010 | Detection / 十分な限定Telemetryで一致Eventがない | Validated | not-observed-in-synthetic-window |

Validatedの二行も限定した入力検査だけである。一致Eventがない例は、十分な合成観測範囲の中だけの未観測を示し、実侵害の不存在を意味しない。九行目は一行目と同じ種類のEventでも、DFIRの保持目的には不足する対比である。

供給fixtureの原記録比較は、UTF-8、キー辞書順、空白なしのJSON表現をSHA-256で比較する有限契約である。ファイル全体の空白・改行の同一性や真正性を証明しない。固定した原記録digestと必要条件を観測値に合わせて更新しない。

## 全欄の読み方

以下は供給JSONの全leafを、トップレベルのRecordごとに表示したもの。スラッシュはJSON欄の位置、配列の数字は0始まりの位置であり、検索式や実行命令ではない。Stage receiptは作成者が供給した仮想の記録であり、実Collectorの測定結果ではない。Fixtureの比較用表現はUTF-8、key順序整列、空白なしのJSONである。比較HashはByteの一致に限定し、真正性・取得前の完全性・保管履歴の証明ではない。

### schemaVersion

| Field | Value |
|---|---|
| `schemaVersion` | `1.0.0` |

### synthetic

| Field | Value |
|---|---|
| `synthetic` | `true` |

### executionAuthorized

| Field | Value |
|---|---|
| `executionAuthorized` | `false` |

### readOnly

| Field | Value |
|---|---|
| `readOnly` | `true` |

### networkRequired

| Field | Value |
|---|---|
| `networkRequired` | `false` |

### record

| Field | Value |
|---|---|
| `id` | `TCM-2026-016` |
| `artifactId` | `ART-24` |
| `revision` | `TCM16-REV-001` |
| `subjectId` | `APP-TCM16-001` |
| `caseId` | `CASE-DET-2026-001` |
| `relatedCaseId` | `CASE-2026-001` |
| `relation` | `refines` |
| `asOf` | `2026-09-21T00:00:00Z` |
| `meaning` | `independent-authored-contrasts-not-live-pipeline` |
| `actualCollections` | `0` |
| `actualDeployments` | `0` |
| `sourceIds/0` | `SRC-ATTACK-001` |
| `sourceIds/1` | `SRC-ATTACK-DET-001` |
| `sourceIds/2` | `SRC-NIST-LOG-001` |
| `sourceIds/3` | `SRC-NIST-LOG-DRAFT-001` |
| `sourceIds/4` | `SRC-IR-001` |
| `coverageStates/0` | `Required` |
| `coverageStates/1` | `Produced` |
| `coverageStates/2` | `Collected` |
| `coverageStates/3` | `Retained` |
| `coverageStates/4` | `Queryable` |
| `coverageStates/5` | `Validated` |
| `coverageStates/6` | `Unknown` |

### parents

| Field | Value |
|---|---|
| `behaviorMapId` | `BMAP-2026-001` |
| `behaviorId` | `BM-2026-002` |
| `signalMapId` | `SFM-2026-001` |
| `signalFlowId` | `SF-2026-001` |
| `findingRecordId` | `FRT-2026-015` |
| `findingId` | `FND-FRT15-001` |
| `findingSubjectId` | `APP-FRT15-001` |
| `findingRevision` | `BEFORE-FRT15-001` |
| `handoffId` | `HOF-FRT15-16` |
| `handoffStatus` | `planned-not-delivered` |
| `detectionRecordId` | `DVR-2026-017-001` |
| `detectionId` | `DET-2026-017-001` |
| `telemetryIds/0` | `TEL-DET-2026-001` |
| `telemetryIds/1` | `TEL-DET-2026-002` |
| `telemetryIds/2` | `TEL-DET-2026-003` |
| `evidenceRole` | `method-reference-not-evidence-for-new-subject` |
| `parentStateChanged` | `false` |
| `authorityTransferred` | `false` |
| `evidenceTransferred` | `false` |
| `parentHandoffReceived` | `false` |
| `chapter17ContractSatisfied` | `false` |

### safety

| Field | Value |
|---|---|
| `scope` | `offline-authored-json-reading-only` |
| `owner` | `SYNTH-TCM16-OWNER` |
| `authority` | `owned-reading-copy-not-parent-RoE` |
| `stop` | `Unknown input, actual data, external connection or unclear scope: stop reading and record the gap.` |
| `cleanup` | `整理するのは自分の読解メモだけ。供給Evidenceと正本は変更しない。` |
| `classification` | `public-synthetic-only` |
| `personalDataIncluded` | `false` |
| `productSchemaClaimed` | `false` |

### requirements EQ-TCM16-001

| Field | Value |
|---|---|
| `id` | `EQ-TCM16-001` |
| `rowId` | `ROW-TCM16-001` |
| `question` | `同意変更入力の限定Field検査` |
| `consumer` | `Detection` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `eventType` | `consent-change` |
| `windowStart` | `2026-09-21T00:00:00Z` |
| `windowEnd` | `2026-09-21T00:10:00Z` |
| `decisionDeadline` | `2026-09-21T01:00:00Z` |
| `requiredRetentionDays` | `1` |
| `maximumClockUncertaintySeconds` | `5` |
| `maximumIngestDelaySeconds` | `60` |
| `identityNamespace` | `SYNTH-TCM16` |
| `normalizerVersion` | `NORM-TCM16-1` |
| `classification` | `public-synthetic-only` |
| `requiredFields/0/name` | `event_time` |
| `requiredFields/0/purpose` | `発生時刻による問いの期間照合` |
| `requiredFields/0/consumer` | `Detection` |
| `requiredFields/1/name` | `observed_time` |
| `requiredFields/1/purpose` | `観測側の時刻と不確かさ` |
| `requiredFields/1/consumer` | `Detection` |
| `requiredFields/2/name` | `ingest_time` |
| `requiredFields/2/purpose` | `到着遅延の評価` |
| `requiredFields/2/consumer` | `Detection` |
| `requiredFields/3/name` | `actor_id` |
| `requiredFields/3/purpose` | `合成主体の区別` |
| `requiredFields/3/consumer` | `Detection` |
| `requiredFields/4/name` | `target_workload_id` |
| `requiredFields/4/purpose` | `対象IDの照合` |
| `requiredFields/4/consumer` | `Detection` |
| `requiredFields/5/name` | `event_type` |
| `requiredFields/5/purpose` | `対象とするEvent種別の照合` |
| `requiredFields/5/consumer` | `Detection` |
| `requiredFields/6/name` | `granted_scope_set` |
| `requiredFields/6/purpose` | `同意変更の内容を示す合成分類` |
| `requiredFields/6/consumer` | `Detection` |
| `requiredFields/7/name` | `change_ticket_id` |
| `requiredFields/7/purpose` | `承認参照の有無と意味の分離` |
| `requiredFields/7/consumer` | `Detection` |
| `requiredFields/8/name` | `result` |
| `requiredFields/8/purpose` | `供給Eventの結果表現` |
| `requiredFields/8/consumer` | `Detection` |

### requirements EQ-TCM16-002

| Field | Value |
|---|---|
| `id` | `EQ-TCM16-002` |
| `rowId` | `ROW-TCM16-002` |
| `question` | `生成とCollector到着を分ける` |
| `consumer` | `Detection` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `eventType` | `consent-change` |
| `windowStart` | `2026-09-21T00:00:00Z` |
| `windowEnd` | `2026-09-21T00:10:00Z` |
| `decisionDeadline` | `2026-09-21T01:00:00Z` |
| `requiredRetentionDays` | `1` |
| `maximumClockUncertaintySeconds` | `5` |
| `maximumIngestDelaySeconds` | `60` |
| `identityNamespace` | `SYNTH-TCM16` |
| `normalizerVersion` | `NORM-TCM16-1` |
| `classification` | `public-synthetic-only` |
| `requiredFields/0/name` | `event_time` |
| `requiredFields/0/purpose` | `発生時刻による問いの期間照合` |
| `requiredFields/0/consumer` | `Detection` |
| `requiredFields/1/name` | `observed_time` |
| `requiredFields/1/purpose` | `観測側の時刻と不確かさ` |
| `requiredFields/1/consumer` | `Detection` |
| `requiredFields/2/name` | `ingest_time` |
| `requiredFields/2/purpose` | `到着遅延の評価` |
| `requiredFields/2/consumer` | `Detection` |
| `requiredFields/3/name` | `actor_id` |
| `requiredFields/3/purpose` | `合成主体の区別` |
| `requiredFields/3/consumer` | `Detection` |
| `requiredFields/4/name` | `target_workload_id` |
| `requiredFields/4/purpose` | `対象IDの照合` |
| `requiredFields/4/consumer` | `Detection` |
| `requiredFields/5/name` | `event_type` |
| `requiredFields/5/purpose` | `対象とするEvent種別の照合` |
| `requiredFields/5/consumer` | `Detection` |
| `requiredFields/6/name` | `granted_scope_set` |
| `requiredFields/6/purpose` | `同意変更の内容を示す合成分類` |
| `requiredFields/6/consumer` | `Detection` |
| `requiredFields/7/name` | `change_ticket_id` |
| `requiredFields/7/purpose` | `承認参照の有無と意味の分離` |
| `requiredFields/7/consumer` | `Detection` |
| `requiredFields/8/name` | `result` |
| `requiredFields/8/purpose` | `供給Eventの結果表現` |
| `requiredFields/8/consumer` | `Detection` |

### requirements EQ-TCM16-003

| Field | Value |
|---|---|
| `id` | `EQ-TCM16-003` |
| `rowId` | `ROW-TCM16-003` |
| `question` | `判断期限までの保持不足` |
| `consumer` | `IR` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `eventType` | `consent-change` |
| `windowStart` | `2026-09-21T00:00:00Z` |
| `windowEnd` | `2026-09-21T00:10:00Z` |
| `decisionDeadline` | `2026-09-21T01:00:00Z` |
| `requiredRetentionDays` | `1` |
| `maximumClockUncertaintySeconds` | `5` |
| `maximumIngestDelaySeconds` | `60` |
| `identityNamespace` | `SYNTH-TCM16` |
| `normalizerVersion` | `NORM-TCM16-1` |
| `classification` | `public-synthetic-only` |
| `requiredFields/0/name` | `event_time` |
| `requiredFields/0/purpose` | `発生時刻による問いの期間照合` |
| `requiredFields/0/consumer` | `IR` |
| `requiredFields/1/name` | `observed_time` |
| `requiredFields/1/purpose` | `観測側の時刻と不確かさ` |
| `requiredFields/1/consumer` | `IR` |
| `requiredFields/2/name` | `ingest_time` |
| `requiredFields/2/purpose` | `到着遅延の評価` |
| `requiredFields/2/consumer` | `IR` |
| `requiredFields/3/name` | `actor_id` |
| `requiredFields/3/purpose` | `合成主体の区別` |
| `requiredFields/3/consumer` | `IR` |
| `requiredFields/4/name` | `target_workload_id` |
| `requiredFields/4/purpose` | `対象IDの照合` |
| `requiredFields/4/consumer` | `IR` |
| `requiredFields/5/name` | `event_type` |
| `requiredFields/5/purpose` | `対象とするEvent種別の照合` |
| `requiredFields/5/consumer` | `IR` |
| `requiredFields/6/name` | `granted_scope_set` |
| `requiredFields/6/purpose` | `同意変更の内容を示す合成分類` |
| `requiredFields/6/consumer` | `IR` |
| `requiredFields/7/name` | `change_ticket_id` |
| `requiredFields/7/purpose` | `承認参照の有無と意味の分離` |
| `requiredFields/7/consumer` | `IR` |
| `requiredFields/8/name` | `result` |
| `requiredFields/8/purpose` | `供給Eventの結果表現` |
| `requiredFields/8/consumer` | `IR` |

### requirements EQ-TCM16-004

| Field | Value |
|---|---|
| `id` | `EQ-TCM16-004` |
| `rowId` | `ROW-TCM16-004` |
| `question` | `保持済みでも検索根拠がない` |
| `consumer` | `Audit` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `eventType` | `consent-change` |
| `windowStart` | `2026-09-21T00:00:00Z` |
| `windowEnd` | `2026-09-21T00:10:00Z` |
| `decisionDeadline` | `2026-09-21T01:00:00Z` |
| `requiredRetentionDays` | `1` |
| `maximumClockUncertaintySeconds` | `5` |
| `maximumIngestDelaySeconds` | `60` |
| `identityNamespace` | `SYNTH-TCM16` |
| `normalizerVersion` | `NORM-TCM16-1` |
| `classification` | `public-synthetic-only` |
| `requiredFields/0/name` | `event_time` |
| `requiredFields/0/purpose` | `発生時刻による問いの期間照合` |
| `requiredFields/0/consumer` | `Audit` |
| `requiredFields/1/name` | `observed_time` |
| `requiredFields/1/purpose` | `観測側の時刻と不確かさ` |
| `requiredFields/1/consumer` | `Audit` |
| `requiredFields/2/name` | `ingest_time` |
| `requiredFields/2/purpose` | `到着遅延の評価` |
| `requiredFields/2/consumer` | `Audit` |
| `requiredFields/3/name` | `actor_id` |
| `requiredFields/3/purpose` | `合成主体の区別` |
| `requiredFields/3/consumer` | `Audit` |
| `requiredFields/4/name` | `target_workload_id` |
| `requiredFields/4/purpose` | `対象IDの照合` |
| `requiredFields/4/consumer` | `Audit` |
| `requiredFields/5/name` | `event_type` |
| `requiredFields/5/purpose` | `対象とするEvent種別の照合` |
| `requiredFields/5/consumer` | `Audit` |
| `requiredFields/6/name` | `granted_scope_set` |
| `requiredFields/6/purpose` | `同意変更の内容を示す合成分類` |
| `requiredFields/6/consumer` | `Audit` |
| `requiredFields/7/name` | `change_ticket_id` |
| `requiredFields/7/purpose` | `承認参照の有無と意味の分離` |
| `requiredFields/7/consumer` | `Audit` |
| `requiredFields/8/name` | `result` |
| `requiredFields/8/purpose` | `供給Eventの結果表現` |
| `requiredFields/8/consumer` | `Audit` |

### requirements EQ-TCM16-005

| Field | Value |
|---|---|
| `id` | `EQ-TCM16-005` |
| `rowId` | `ROW-TCM16-005` |
| `question` | `相関Windowより時刻誤差が大きい` |
| `consumer` | `Hunt` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `eventType` | `consent-change` |
| `windowStart` | `2026-09-21T00:00:00Z` |
| `windowEnd` | `2026-09-21T00:10:00Z` |
| `decisionDeadline` | `2026-09-21T01:00:00Z` |
| `requiredRetentionDays` | `1` |
| `maximumClockUncertaintySeconds` | `5` |
| `maximumIngestDelaySeconds` | `60` |
| `identityNamespace` | `SYNTH-TCM16` |
| `normalizerVersion` | `NORM-TCM16-1` |
| `classification` | `public-synthetic-only` |
| `requiredFields/0/name` | `event_time` |
| `requiredFields/0/purpose` | `発生時刻による問いの期間照合` |
| `requiredFields/0/consumer` | `Hunt` |
| `requiredFields/1/name` | `observed_time` |
| `requiredFields/1/purpose` | `観測側の時刻と不確かさ` |
| `requiredFields/1/consumer` | `Hunt` |
| `requiredFields/2/name` | `ingest_time` |
| `requiredFields/2/purpose` | `到着遅延の評価` |
| `requiredFields/2/consumer` | `Hunt` |
| `requiredFields/3/name` | `actor_id` |
| `requiredFields/3/purpose` | `合成主体の区別` |
| `requiredFields/3/consumer` | `Hunt` |
| `requiredFields/4/name` | `target_workload_id` |
| `requiredFields/4/purpose` | `対象IDの照合` |
| `requiredFields/4/consumer` | `Hunt` |
| `requiredFields/5/name` | `event_type` |
| `requiredFields/5/purpose` | `対象とするEvent種別の照合` |
| `requiredFields/5/consumer` | `Hunt` |
| `requiredFields/6/name` | `granted_scope_set` |
| `requiredFields/6/purpose` | `同意変更の内容を示す合成分類` |
| `requiredFields/6/consumer` | `Hunt` |
| `requiredFields/7/name` | `change_ticket_id` |
| `requiredFields/7/purpose` | `承認参照の有無と意味の分離` |
| `requiredFields/7/consumer` | `Hunt` |
| `requiredFields/8/name` | `result` |
| `requiredFields/8/purpose` | `供給Eventの結果表現` |
| `requiredFields/8/consumer` | `Hunt` |

### requirements EQ-TCM16-006

| Field | Value |
|---|---|
| `id` | `EQ-TCM16-006` |
| `rowId` | `ROW-TCM16-006` |
| `question` | `同じID文字列でも正規化版が違う` |
| `consumer` | `Hunt` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `eventType` | `consent-change` |
| `windowStart` | `2026-09-21T00:00:00Z` |
| `windowEnd` | `2026-09-21T00:10:00Z` |
| `decisionDeadline` | `2026-09-21T01:00:00Z` |
| `requiredRetentionDays` | `1` |
| `maximumClockUncertaintySeconds` | `5` |
| `maximumIngestDelaySeconds` | `60` |
| `identityNamespace` | `SYNTH-TCM16` |
| `normalizerVersion` | `NORM-TCM16-1` |
| `classification` | `public-synthetic-only` |
| `requiredFields/0/name` | `event_time` |
| `requiredFields/0/purpose` | `発生時刻による問いの期間照合` |
| `requiredFields/0/consumer` | `Hunt` |
| `requiredFields/1/name` | `observed_time` |
| `requiredFields/1/purpose` | `観測側の時刻と不確かさ` |
| `requiredFields/1/consumer` | `Hunt` |
| `requiredFields/2/name` | `ingest_time` |
| `requiredFields/2/purpose` | `到着遅延の評価` |
| `requiredFields/2/consumer` | `Hunt` |
| `requiredFields/3/name` | `actor_id` |
| `requiredFields/3/purpose` | `合成主体の区別` |
| `requiredFields/3/consumer` | `Hunt` |
| `requiredFields/4/name` | `target_workload_id` |
| `requiredFields/4/purpose` | `対象IDの照合` |
| `requiredFields/4/consumer` | `Hunt` |
| `requiredFields/5/name` | `event_type` |
| `requiredFields/5/purpose` | `対象とするEvent種別の照合` |
| `requiredFields/5/consumer` | `Hunt` |
| `requiredFields/6/name` | `granted_scope_set` |
| `requiredFields/6/purpose` | `同意変更の内容を示す合成分類` |
| `requiredFields/6/consumer` | `Hunt` |
| `requiredFields/7/name` | `change_ticket_id` |
| `requiredFields/7/purpose` | `承認参照の有無と意味の分離` |
| `requiredFields/7/consumer` | `Hunt` |
| `requiredFields/8/name` | `result` |
| `requiredFields/8/purpose` | `供給Eventの結果表現` |
| `requiredFields/8/consumer` | `Hunt` |

### requirements EQ-TCM16-007

| Field | Value |
|---|---|
| `id` | `EQ-TCM16-007` |
| `rowId` | `ROW-TCM16-007` |
| `question` | `Workload API Eventを必要とするが未生成` |
| `consumer` | `Hunt` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `eventType` | `workload-api-access` |
| `windowStart` | `2026-09-21T00:00:00Z` |
| `windowEnd` | `2026-09-21T00:10:00Z` |
| `decisionDeadline` | `2026-09-21T01:00:00Z` |
| `requiredRetentionDays` | `1` |
| `maximumClockUncertaintySeconds` | `5` |
| `maximumIngestDelaySeconds` | `60` |
| `identityNamespace` | `SYNTH-TCM16` |
| `normalizerVersion` | `NORM-TCM16-1` |
| `classification` | `public-synthetic-only` |
| `requiredFields/0/name` | `event_time` |
| `requiredFields/0/purpose` | `発生時刻による問いの期間照合` |
| `requiredFields/0/consumer` | `Hunt` |
| `requiredFields/1/name` | `observed_time` |
| `requiredFields/1/purpose` | `観測側の時刻と不確かさ` |
| `requiredFields/1/consumer` | `Hunt` |
| `requiredFields/2/name` | `ingest_time` |
| `requiredFields/2/purpose` | `到着遅延の評価` |
| `requiredFields/2/consumer` | `Hunt` |
| `requiredFields/3/name` | `actor_id` |
| `requiredFields/3/purpose` | `合成主体の区別` |
| `requiredFields/3/consumer` | `Hunt` |
| `requiredFields/4/name` | `target_workload_id` |
| `requiredFields/4/purpose` | `対象IDの照合` |
| `requiredFields/4/consumer` | `Hunt` |
| `requiredFields/5/name` | `event_type` |
| `requiredFields/5/purpose` | `対象とするEvent種別の照合` |
| `requiredFields/5/consumer` | `Hunt` |
| `requiredFields/6/name` | `granted_scope_set` |
| `requiredFields/6/purpose` | `同意変更の内容を示す合成分類` |
| `requiredFields/6/consumer` | `Hunt` |
| `requiredFields/7/name` | `change_ticket_id` |
| `requiredFields/7/purpose` | `承認参照の有無と意味の分離` |
| `requiredFields/7/consumer` | `Hunt` |
| `requiredFields/8/name` | `result` |
| `requiredFields/8/purpose` | `供給Eventの結果表現` |
| `requiredFields/8/consumer` | `Hunt` |

### requirements EQ-TCM16-008

| Field | Value |
|---|---|
| `id` | `EQ-TCM16-008` |
| `rowId` | `ROW-TCM16-008` |
| `question` | `Authentication contextの取扱根拠が未確認` |
| `consumer` | `IR` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `eventType` | `authentication-context` |
| `windowStart` | `2026-09-21T00:00:00Z` |
| `windowEnd` | `2026-09-21T00:10:00Z` |
| `decisionDeadline` | `2026-09-21T01:00:00Z` |
| `requiredRetentionDays` | `1` |
| `maximumClockUncertaintySeconds` | `5` |
| `maximumIngestDelaySeconds` | `60` |
| `identityNamespace` | `SYNTH-TCM16` |
| `normalizerVersion` | `NORM-TCM16-1` |
| `classification` | `public-synthetic-only` |
| `requiredFields/0/name` | `event_time` |
| `requiredFields/0/purpose` | `発生時刻による問いの期間照合` |
| `requiredFields/0/consumer` | `IR` |
| `requiredFields/1/name` | `observed_time` |
| `requiredFields/1/purpose` | `観測側の時刻と不確かさ` |
| `requiredFields/1/consumer` | `IR` |
| `requiredFields/2/name` | `ingest_time` |
| `requiredFields/2/purpose` | `到着遅延の評価` |
| `requiredFields/2/consumer` | `IR` |
| `requiredFields/3/name` | `actor_id` |
| `requiredFields/3/purpose` | `合成主体の区別` |
| `requiredFields/3/consumer` | `IR` |
| `requiredFields/4/name` | `target_workload_id` |
| `requiredFields/4/purpose` | `対象IDの照合` |
| `requiredFields/4/consumer` | `IR` |
| `requiredFields/5/name` | `event_type` |
| `requiredFields/5/purpose` | `対象とするEvent種別の照合` |
| `requiredFields/5/consumer` | `IR` |
| `requiredFields/6/name` | `granted_scope_set` |
| `requiredFields/6/purpose` | `同意変更の内容を示す合成分類` |
| `requiredFields/6/consumer` | `IR` |
| `requiredFields/7/name` | `change_ticket_id` |
| `requiredFields/7/purpose` | `承認参照の有無と意味の分離` |
| `requiredFields/7/consumer` | `IR` |
| `requiredFields/8/name` | `result` |
| `requiredFields/8/purpose` | `供給Eventの結果表現` |
| `requiredFields/8/consumer` | `IR` |

### requirements EQ-TCM16-009

| Field | Value |
|---|---|
| `id` | `EQ-TCM16-009` |
| `rowId` | `ROW-TCM16-009` |
| `question` | `同意変更の入力はあるが調査用保持が不足` |
| `consumer` | `DFIR` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `eventType` | `consent-change` |
| `windowStart` | `2026-09-21T00:00:00Z` |
| `windowEnd` | `2026-09-21T00:10:00Z` |
| `decisionDeadline` | `2026-09-21T01:00:00Z` |
| `requiredRetentionDays` | `30` |
| `maximumClockUncertaintySeconds` | `5` |
| `maximumIngestDelaySeconds` | `60` |
| `identityNamespace` | `SYNTH-TCM16` |
| `normalizerVersion` | `NORM-TCM16-1` |
| `classification` | `public-synthetic-only` |
| `requiredFields/0/name` | `event_time` |
| `requiredFields/0/purpose` | `発生時刻による問いの期間照合` |
| `requiredFields/0/consumer` | `DFIR` |
| `requiredFields/1/name` | `observed_time` |
| `requiredFields/1/purpose` | `観測側の時刻と不確かさ` |
| `requiredFields/1/consumer` | `DFIR` |
| `requiredFields/2/name` | `ingest_time` |
| `requiredFields/2/purpose` | `到着遅延の評価` |
| `requiredFields/2/consumer` | `DFIR` |
| `requiredFields/3/name` | `actor_id` |
| `requiredFields/3/purpose` | `合成主体の区別` |
| `requiredFields/3/consumer` | `DFIR` |
| `requiredFields/4/name` | `target_workload_id` |
| `requiredFields/4/purpose` | `対象IDの照合` |
| `requiredFields/4/consumer` | `DFIR` |
| `requiredFields/5/name` | `event_type` |
| `requiredFields/5/purpose` | `対象とするEvent種別の照合` |
| `requiredFields/5/consumer` | `DFIR` |
| `requiredFields/6/name` | `granted_scope_set` |
| `requiredFields/6/purpose` | `同意変更の内容を示す合成分類` |
| `requiredFields/6/consumer` | `DFIR` |
| `requiredFields/7/name` | `change_ticket_id` |
| `requiredFields/7/purpose` | `承認参照の有無と意味の分離` |
| `requiredFields/7/consumer` | `DFIR` |
| `requiredFields/8/name` | `result` |
| `requiredFields/8/purpose` | `供給Eventの結果表現` |
| `requiredFields/8/consumer` | `DFIR` |

### requirements EQ-TCM16-010

| Field | Value |
|---|---|
| `id` | `EQ-TCM16-010` |
| `rowId` | `ROW-TCM16-010` |
| `question` | `十分な限定Telemetryで一致Eventがない` |
| `consumer` | `Detection` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `eventType` | `consent-change` |
| `windowStart` | `2026-09-21T00:00:00Z` |
| `windowEnd` | `2026-09-21T00:10:00Z` |
| `decisionDeadline` | `2026-09-21T01:00:00Z` |
| `requiredRetentionDays` | `1` |
| `maximumClockUncertaintySeconds` | `5` |
| `maximumIngestDelaySeconds` | `60` |
| `identityNamespace` | `SYNTH-TCM16` |
| `normalizerVersion` | `NORM-TCM16-1` |
| `classification` | `public-synthetic-only` |
| `requiredFields/0/name` | `event_time` |
| `requiredFields/0/purpose` | `発生時刻による問いの期間照合` |
| `requiredFields/0/consumer` | `Detection` |
| `requiredFields/1/name` | `observed_time` |
| `requiredFields/1/purpose` | `観測側の時刻と不確かさ` |
| `requiredFields/1/consumer` | `Detection` |
| `requiredFields/2/name` | `ingest_time` |
| `requiredFields/2/purpose` | `到着遅延の評価` |
| `requiredFields/2/consumer` | `Detection` |
| `requiredFields/3/name` | `actor_id` |
| `requiredFields/3/purpose` | `合成主体の区別` |
| `requiredFields/3/consumer` | `Detection` |
| `requiredFields/4/name` | `target_workload_id` |
| `requiredFields/4/purpose` | `対象IDの照合` |
| `requiredFields/4/consumer` | `Detection` |
| `requiredFields/5/name` | `event_type` |
| `requiredFields/5/purpose` | `対象とするEvent種別の照合` |
| `requiredFields/5/consumer` | `Detection` |
| `requiredFields/6/name` | `granted_scope_set` |
| `requiredFields/6/purpose` | `同意変更の内容を示す合成分類` |
| `requiredFields/6/consumer` | `Detection` |
| `requiredFields/7/name` | `change_ticket_id` |
| `requiredFields/7/purpose` | `承認参照の有無と意味の分離` |
| `requiredFields/7/consumer` | `Detection` |
| `requiredFields/8/name` | `result` |
| `requiredFields/8/purpose` | `供給Eventの結果表現` |
| `requiredFields/8/consumer` | `Detection` |

### fixtures FIX-TCM16-001

| Field | Value |
|---|---|
| `id` | `FIX-TCM16-001` |
| `rowId` | `ROW-TCM16-001` |
| `questionId` | `EQ-TCM16-001` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `synthetic` | `true` |
| `eventPresence` | `present` |
| `observationWindowComplete` | `false` |
| `records/0/event_time` | `2026-09-21T00:05:00Z` |
| `records/0/observed_time` | `2026-09-21T00:05:01Z` |
| `records/0/ingest_time` | `2026-09-21T00:05:02Z` |
| `records/0/actor_id` | `SYNTH-ACTOR-TCM16-001` |
| `records/0/target_workload_id` | `APP-TCM16-001` |
| `records/0/event_type` | `consent-change` |
| `records/0/granted_scope_set/0` | `read-summary` |
| `records/0/change_ticket_id` | `SYNTH-CHANGE-TCM16-001` |
| `records/0/result` | `synthetic-recorded` |

### fixtures FIX-TCM16-002

| Field | Value |
|---|---|
| `id` | `FIX-TCM16-002` |
| `rowId` | `ROW-TCM16-002` |
| `questionId` | `EQ-TCM16-002` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `synthetic` | `true` |
| `eventPresence` | `present` |
| `observationWindowComplete` | `false` |
| `records/0/event_time` | `2026-09-21T00:05:00Z` |
| `records/0/observed_time` | `2026-09-21T00:05:01Z` |
| `records/0/ingest_time` | `2026-09-21T00:05:02Z` |
| `records/0/actor_id` | `SYNTH-ACTOR-TCM16-001` |
| `records/0/target_workload_id` | `APP-TCM16-001` |
| `records/0/event_type` | `consent-change` |
| `records/0/granted_scope_set/0` | `read-summary` |
| `records/0/change_ticket_id` | `SYNTH-CHANGE-TCM16-001` |
| `records/0/result` | `synthetic-recorded` |

### fixtures FIX-TCM16-003

| Field | Value |
|---|---|
| `id` | `FIX-TCM16-003` |
| `rowId` | `ROW-TCM16-003` |
| `questionId` | `EQ-TCM16-003` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `synthetic` | `true` |
| `eventPresence` | `present` |
| `observationWindowComplete` | `false` |
| `records/0/event_time` | `2026-09-21T00:05:00Z` |
| `records/0/observed_time` | `2026-09-21T00:05:01Z` |
| `records/0/ingest_time` | `2026-09-21T00:05:02Z` |
| `records/0/actor_id` | `SYNTH-ACTOR-TCM16-001` |
| `records/0/target_workload_id` | `APP-TCM16-001` |
| `records/0/event_type` | `consent-change` |
| `records/0/granted_scope_set/0` | `read-summary` |
| `records/0/change_ticket_id` | `SYNTH-CHANGE-TCM16-001` |
| `records/0/result` | `synthetic-recorded` |

### fixtures FIX-TCM16-004

| Field | Value |
|---|---|
| `id` | `FIX-TCM16-004` |
| `rowId` | `ROW-TCM16-004` |
| `questionId` | `EQ-TCM16-004` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `synthetic` | `true` |
| `eventPresence` | `present` |
| `observationWindowComplete` | `false` |
| `records/0/event_time` | `2026-09-21T00:05:00Z` |
| `records/0/observed_time` | `2026-09-21T00:05:01Z` |
| `records/0/ingest_time` | `2026-09-21T00:05:02Z` |
| `records/0/actor_id` | `SYNTH-ACTOR-TCM16-001` |
| `records/0/target_workload_id` | `APP-TCM16-001` |
| `records/0/event_type` | `consent-change` |
| `records/0/granted_scope_set/0` | `read-summary` |
| `records/0/change_ticket_id` | `SYNTH-CHANGE-TCM16-001` |
| `records/0/result` | `synthetic-recorded` |

### fixtures FIX-TCM16-005

| Field | Value |
|---|---|
| `id` | `FIX-TCM16-005` |
| `rowId` | `ROW-TCM16-005` |
| `questionId` | `EQ-TCM16-005` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `synthetic` | `true` |
| `eventPresence` | `present` |
| `observationWindowComplete` | `false` |
| `records/0/event_time` | `2026-09-21T00:05:00Z` |
| `records/0/observed_time` | `2026-09-21T00:05:01Z` |
| `records/0/ingest_time` | `2026-09-21T00:05:02Z` |
| `records/0/actor_id` | `SYNTH-ACTOR-TCM16-001` |
| `records/0/target_workload_id` | `APP-TCM16-001` |
| `records/0/event_type` | `consent-change` |
| `records/0/granted_scope_set/0` | `read-summary` |
| `records/0/change_ticket_id` | `SYNTH-CHANGE-TCM16-001` |
| `records/0/result` | `synthetic-recorded` |

### fixtures FIX-TCM16-006

| Field | Value |
|---|---|
| `id` | `FIX-TCM16-006` |
| `rowId` | `ROW-TCM16-006` |
| `questionId` | `EQ-TCM16-006` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `synthetic` | `true` |
| `eventPresence` | `present` |
| `observationWindowComplete` | `false` |
| `records/0/event_time` | `2026-09-21T00:05:00Z` |
| `records/0/observed_time` | `2026-09-21T00:05:01Z` |
| `records/0/ingest_time` | `2026-09-21T00:05:02Z` |
| `records/0/actor_id` | `SYNTH-ACTOR-TCM16-001` |
| `records/0/target_workload_id` | `APP-TCM16-001` |
| `records/0/event_type` | `consent-change` |
| `records/0/granted_scope_set/0` | `read-summary` |
| `records/0/change_ticket_id` | `SYNTH-CHANGE-TCM16-001` |
| `records/0/result` | `synthetic-recorded` |

### fixtures FIX-TCM16-007

| Field | Value |
|---|---|
| `id` | `FIX-TCM16-007` |
| `rowId` | `ROW-TCM16-007` |
| `questionId` | `EQ-TCM16-007` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `synthetic` | `true` |
| `eventPresence` | `unknown` |
| `observationWindowComplete` | `false` |
| `records` | `[]` |

### fixtures FIX-TCM16-008

| Field | Value |
|---|---|
| `id` | `FIX-TCM16-008` |
| `rowId` | `ROW-TCM16-008` |
| `questionId` | `EQ-TCM16-008` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `synthetic` | `true` |
| `eventPresence` | `unknown` |
| `observationWindowComplete` | `false` |
| `records` | `[]` |

### fixtures FIX-TCM16-009

| Field | Value |
|---|---|
| `id` | `FIX-TCM16-009` |
| `rowId` | `ROW-TCM16-009` |
| `questionId` | `EQ-TCM16-009` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `synthetic` | `true` |
| `eventPresence` | `present` |
| `observationWindowComplete` | `false` |
| `records/0/event_time` | `2026-09-21T00:05:00Z` |
| `records/0/observed_time` | `2026-09-21T00:05:01Z` |
| `records/0/ingest_time` | `2026-09-21T00:05:02Z` |
| `records/0/actor_id` | `SYNTH-ACTOR-TCM16-001` |
| `records/0/target_workload_id` | `APP-TCM16-001` |
| `records/0/event_type` | `consent-change` |
| `records/0/granted_scope_set/0` | `read-summary` |
| `records/0/change_ticket_id` | `SYNTH-CHANGE-TCM16-001` |
| `records/0/result` | `synthetic-recorded` |

### fixtures FIX-TCM16-010

| Field | Value |
|---|---|
| `id` | `FIX-TCM16-010` |
| `rowId` | `ROW-TCM16-010` |
| `questionId` | `EQ-TCM16-010` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `synthetic` | `true` |
| `eventPresence` | `absent` |
| `observationWindowComplete` | `true` |
| `records` | `[]` |

### receipts EVD-TCM16-001-1

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-001-1` |
| `stage` | `Produced` |
| `rowId` | `ROW-TCM16-001` |
| `questionId` | `EQ-TCM16-001` |
| `fixtureId` | `FIX-TCM16-001` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### receipts EVD-TCM16-001-2

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-001-2` |
| `stage` | `Collected` |
| `rowId` | `ROW-TCM16-001` |
| `questionId` | `EQ-TCM16-001` |
| `fixtureId` | `FIX-TCM16-001` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### receipts EVD-TCM16-001-3

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-001-3` |
| `stage` | `Retained` |
| `rowId` | `ROW-TCM16-001` |
| `questionId` | `EQ-TCM16-001` |
| `fixtureId` | `FIX-TCM16-001` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### receipts EVD-TCM16-001-4

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-001-4` |
| `stage` | `Queryable` |
| `rowId` | `ROW-TCM16-001` |
| `questionId` | `EQ-TCM16-001` |
| `fixtureId` | `FIX-TCM16-001` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### receipts EVD-TCM16-002-1

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-002-1` |
| `stage` | `Produced` |
| `rowId` | `ROW-TCM16-002` |
| `questionId` | `EQ-TCM16-002` |
| `fixtureId` | `FIX-TCM16-002` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### receipts EVD-TCM16-003-1

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-003-1` |
| `stage` | `Produced` |
| `rowId` | `ROW-TCM16-003` |
| `questionId` | `EQ-TCM16-003` |
| `fixtureId` | `FIX-TCM16-003` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### receipts EVD-TCM16-003-2

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-003-2` |
| `stage` | `Collected` |
| `rowId` | `ROW-TCM16-003` |
| `questionId` | `EQ-TCM16-003` |
| `fixtureId` | `FIX-TCM16-003` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### receipts EVD-TCM16-004-1

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-004-1` |
| `stage` | `Produced` |
| `rowId` | `ROW-TCM16-004` |
| `questionId` | `EQ-TCM16-004` |
| `fixtureId` | `FIX-TCM16-004` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### receipts EVD-TCM16-004-2

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-004-2` |
| `stage` | `Collected` |
| `rowId` | `ROW-TCM16-004` |
| `questionId` | `EQ-TCM16-004` |
| `fixtureId` | `FIX-TCM16-004` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### receipts EVD-TCM16-004-3

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-004-3` |
| `stage` | `Retained` |
| `rowId` | `ROW-TCM16-004` |
| `questionId` | `EQ-TCM16-004` |
| `fixtureId` | `FIX-TCM16-004` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### receipts EVD-TCM16-005-1

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-005-1` |
| `stage` | `Produced` |
| `rowId` | `ROW-TCM16-005` |
| `questionId` | `EQ-TCM16-005` |
| `fixtureId` | `FIX-TCM16-005` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### receipts EVD-TCM16-005-2

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-005-2` |
| `stage` | `Collected` |
| `rowId` | `ROW-TCM16-005` |
| `questionId` | `EQ-TCM16-005` |
| `fixtureId` | `FIX-TCM16-005` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### receipts EVD-TCM16-005-3

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-005-3` |
| `stage` | `Retained` |
| `rowId` | `ROW-TCM16-005` |
| `questionId` | `EQ-TCM16-005` |
| `fixtureId` | `FIX-TCM16-005` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### receipts EVD-TCM16-005-4

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-005-4` |
| `stage` | `Queryable` |
| `rowId` | `ROW-TCM16-005` |
| `questionId` | `EQ-TCM16-005` |
| `fixtureId` | `FIX-TCM16-005` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### receipts EVD-TCM16-006-1

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-006-1` |
| `stage` | `Produced` |
| `rowId` | `ROW-TCM16-006` |
| `questionId` | `EQ-TCM16-006` |
| `fixtureId` | `FIX-TCM16-006` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### receipts EVD-TCM16-006-2

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-006-2` |
| `stage` | `Collected` |
| `rowId` | `ROW-TCM16-006` |
| `questionId` | `EQ-TCM16-006` |
| `fixtureId` | `FIX-TCM16-006` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### receipts EVD-TCM16-006-3

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-006-3` |
| `stage` | `Retained` |
| `rowId` | `ROW-TCM16-006` |
| `questionId` | `EQ-TCM16-006` |
| `fixtureId` | `FIX-TCM16-006` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### receipts EVD-TCM16-006-4

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-006-4` |
| `stage` | `Queryable` |
| `rowId` | `ROW-TCM16-006` |
| `questionId` | `EQ-TCM16-006` |
| `fixtureId` | `FIX-TCM16-006` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### receipts EVD-TCM16-009-1

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-009-1` |
| `stage` | `Produced` |
| `rowId` | `ROW-TCM16-009` |
| `questionId` | `EQ-TCM16-009` |
| `fixtureId` | `FIX-TCM16-009` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### receipts EVD-TCM16-009-2

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-009-2` |
| `stage` | `Collected` |
| `rowId` | `ROW-TCM16-009` |
| `questionId` | `EQ-TCM16-009` |
| `fixtureId` | `FIX-TCM16-009` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### receipts EVD-TCM16-010-1

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-010-1` |
| `stage` | `Produced` |
| `rowId` | `ROW-TCM16-010` |
| `questionId` | `EQ-TCM16-010` |
| `fixtureId` | `FIX-TCM16-010` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### receipts EVD-TCM16-010-2

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-010-2` |
| `stage` | `Collected` |
| `rowId` | `ROW-TCM16-010` |
| `questionId` | `EQ-TCM16-010` |
| `fixtureId` | `FIX-TCM16-010` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### receipts EVD-TCM16-010-3

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-010-3` |
| `stage` | `Retained` |
| `rowId` | `ROW-TCM16-010` |
| `questionId` | `EQ-TCM16-010` |
| `fixtureId` | `FIX-TCM16-010` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### receipts EVD-TCM16-010-4

| Field | Value |
|---|---|
| `id` | `EVD-TCM16-010-4` |
| `stage` | `Queryable` |
| `rowId` | `ROW-TCM16-010` |
| `questionId` | `EQ-TCM16-010` |
| `fixtureId` | `FIX-TCM16-010` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `meaning` | `authored-stage-receipt-not-live-measurement` |

### rows ROW-TCM16-001

| Field | Value |
|---|---|
| `id` | `ROW-TCM16-001` |
| `questionId` | `EQ-TCM16-001` |
| `fixtureId` | `FIX-TCM16-001` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `producerId` | `SYNTH-PRODUCER-TCM16` |
| `collectorId` | `SYNTH-COLLECTOR-TCM16` |
| `transport` | `offline-supplied-records` |
| `schemaVersion` | `TCM16-EVENT-1` |
| `normalizerVersion` | `NORM-TCM16-1` |
| `identityNamespace` | `SYNTH-TCM16` |
| `clockSource` | `SYNTH-UTC-CLOCK` |
| `timezone` | `UTC` |
| `clockUncertaintySeconds` | `2` |
| `ingestDelaySeconds` | `2` |
| `retentionStart` | `2026-09-21T00:00:00Z` |
| `retentionEnd` | `2026-09-23T00:00:00Z` |
| `integrityReference` | `SYNTH-ORIGINAL-TCM16-001` |
| `integrityMeaning` | `supplied-byte-comparison-not-authenticity` |
| `classification` | `public-synthetic-only` |
| `processingBasis` | `synthetic-reading-only` |
| `accessRole` | `SYNTH-DETECTION-READER` |
| `receiptIds/0` | `EVD-TCM16-001-1` |
| `receiptIds/1` | `EVD-TCM16-001-2` |
| `receiptIds/2` | `EVD-TCM16-001-3` |
| `receiptIds/3` | `EVD-TCM16-001-4` |
| `coverage` | `Validated` |
| `testId` | `TEST-TCM16-001` |
| `validationId` | `VAL-TCM16-001` |
| `validationEvidenceId` | `EVD-TEST-TCM16-001` |
| `allowedConclusion` | `bounded-input-contract-satisfied` |
| `gapId` | `GAP-TCM16-001` |
| `gap` | `限定入力検査だけであり親17の検知全体は未評価。` |
| `owner` | `SYNTH-TCM16-OWNER` |
| `dueAt` | `2026-09-22T00:00:00Z` |
| `reassessment` | `Schema、対象版、時間精度、保持、Identity、Consumer目的が変われば再比較。` |

### rows ROW-TCM16-002

| Field | Value |
|---|---|
| `id` | `ROW-TCM16-002` |
| `questionId` | `EQ-TCM16-002` |
| `fixtureId` | `FIX-TCM16-002` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `producerId` | `SYNTH-PRODUCER-TCM16` |
| `collectorId` | `SYNTH-COLLECTOR-TCM16` |
| `transport` | `offline-supplied-records` |
| `schemaVersion` | `TCM16-EVENT-1` |
| `normalizerVersion` | `NORM-TCM16-1` |
| `identityNamespace` | `SYNTH-TCM16` |
| `clockSource` | `SYNTH-UTC-CLOCK` |
| `timezone` | `UTC` |
| `clockUncertaintySeconds` | `2` |
| `ingestDelaySeconds` | `120` |
| `retentionStart` | `2026-09-21T00:00:00Z` |
| `retentionEnd` | `2026-09-23T00:00:00Z` |
| `integrityReference` | `SYNTH-ORIGINAL-TCM16-002` |
| `integrityMeaning` | `supplied-byte-comparison-not-authenticity` |
| `classification` | `public-synthetic-only` |
| `processingBasis` | `synthetic-reading-only` |
| `accessRole` | `SYNTH-DETECTION-READER` |
| `receiptIds/0` | `EVD-TCM16-002-1` |
| `coverage` | `Produced` |
| `testId` | `TEST-TCM16-002` |
| `validationId` | `VAL-TCM16-002` |
| `validationEvidenceId` | `EVD-TEST-TCM16-002` |
| `allowedConclusion` | `collector-evidence-missing` |
| `gapId` | `GAP-TCM16-002` |
| `gap` | `生成とCollector到着を分ける` |
| `owner` | `SYNTH-TCM16-OWNER` |
| `dueAt` | `2026-09-22T00:00:00Z` |
| `reassessment` | `Schema、対象版、時間精度、保持、Identity、Consumer目的が変われば再比較。` |

### rows ROW-TCM16-003

| Field | Value |
|---|---|
| `id` | `ROW-TCM16-003` |
| `questionId` | `EQ-TCM16-003` |
| `fixtureId` | `FIX-TCM16-003` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `producerId` | `SYNTH-PRODUCER-TCM16` |
| `collectorId` | `SYNTH-COLLECTOR-TCM16` |
| `transport` | `offline-supplied-records` |
| `schemaVersion` | `TCM16-EVENT-1` |
| `normalizerVersion` | `NORM-TCM16-1` |
| `identityNamespace` | `SYNTH-TCM16` |
| `clockSource` | `SYNTH-UTC-CLOCK` |
| `timezone` | `UTC` |
| `clockUncertaintySeconds` | `2` |
| `ingestDelaySeconds` | `2` |
| `retentionStart` | `2026-09-21T00:00:00Z` |
| `retentionEnd` | `2026-09-21T00:30:00Z` |
| `integrityReference` | `SYNTH-ORIGINAL-TCM16-003` |
| `integrityMeaning` | `supplied-byte-comparison-not-authenticity` |
| `classification` | `public-synthetic-only` |
| `processingBasis` | `synthetic-reading-only` |
| `accessRole` | `SYNTH-IR-READER` |
| `receiptIds/0` | `EVD-TCM16-003-1` |
| `receiptIds/1` | `EVD-TCM16-003-2` |
| `coverage` | `Collected` |
| `testId` | `TEST-TCM16-003` |
| `validationId` | `VAL-TCM16-003` |
| `validationEvidenceId` | `EVD-TEST-TCM16-003` |
| `allowedConclusion` | `retention-gap` |
| `gapId` | `GAP-TCM16-003` |
| `gap` | `判断期限までの保持不足` |
| `owner` | `SYNTH-TCM16-OWNER` |
| `dueAt` | `2026-09-22T00:00:00Z` |
| `reassessment` | `Schema、対象版、時間精度、保持、Identity、Consumer目的が変われば再比較。` |

### rows ROW-TCM16-004

| Field | Value |
|---|---|
| `id` | `ROW-TCM16-004` |
| `questionId` | `EQ-TCM16-004` |
| `fixtureId` | `FIX-TCM16-004` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `producerId` | `SYNTH-PRODUCER-TCM16` |
| `collectorId` | `SYNTH-COLLECTOR-TCM16` |
| `transport` | `offline-supplied-records` |
| `schemaVersion` | `TCM16-EVENT-1` |
| `normalizerVersion` | `NORM-TCM16-1` |
| `identityNamespace` | `SYNTH-TCM16` |
| `clockSource` | `SYNTH-UTC-CLOCK` |
| `timezone` | `UTC` |
| `clockUncertaintySeconds` | `2` |
| `ingestDelaySeconds` | `2` |
| `retentionStart` | `2026-09-21T00:00:00Z` |
| `retentionEnd` | `2026-09-23T00:00:00Z` |
| `integrityReference` | `SYNTH-ORIGINAL-TCM16-004` |
| `integrityMeaning` | `supplied-byte-comparison-not-authenticity` |
| `classification` | `public-synthetic-only` |
| `processingBasis` | `synthetic-reading-only` |
| `accessRole` | `SYNTH-AUDIT-READER` |
| `receiptIds/0` | `EVD-TCM16-004-1` |
| `receiptIds/1` | `EVD-TCM16-004-2` |
| `receiptIds/2` | `EVD-TCM16-004-3` |
| `coverage` | `Retained` |
| `testId` | `TEST-TCM16-004` |
| `validationId` | `VAL-TCM16-004` |
| `validationEvidenceId` | `EVD-TEST-TCM16-004` |
| `allowedConclusion` | `query-evidence-missing` |
| `gapId` | `GAP-TCM16-004` |
| `gap` | `保持済みでも検索根拠がない` |
| `owner` | `SYNTH-TCM16-OWNER` |
| `dueAt` | `2026-09-22T00:00:00Z` |
| `reassessment` | `Schema、対象版、時間精度、保持、Identity、Consumer目的が変われば再比較。` |

### rows ROW-TCM16-005

| Field | Value |
|---|---|
| `id` | `ROW-TCM16-005` |
| `questionId` | `EQ-TCM16-005` |
| `fixtureId` | `FIX-TCM16-005` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `producerId` | `SYNTH-PRODUCER-TCM16` |
| `collectorId` | `SYNTH-COLLECTOR-TCM16` |
| `transport` | `offline-supplied-records` |
| `schemaVersion` | `TCM16-EVENT-1` |
| `normalizerVersion` | `NORM-TCM16-1` |
| `identityNamespace` | `SYNTH-TCM16` |
| `clockSource` | `SYNTH-UTC-CLOCK` |
| `timezone` | `UTC` |
| `clockUncertaintySeconds` | `120` |
| `ingestDelaySeconds` | `2` |
| `retentionStart` | `2026-09-21T00:00:00Z` |
| `retentionEnd` | `2026-09-23T00:00:00Z` |
| `integrityReference` | `SYNTH-ORIGINAL-TCM16-005` |
| `integrityMeaning` | `supplied-byte-comparison-not-authenticity` |
| `classification` | `public-synthetic-only` |
| `processingBasis` | `synthetic-reading-only` |
| `accessRole` | `SYNTH-HUNT-READER` |
| `receiptIds/0` | `EVD-TCM16-005-1` |
| `receiptIds/1` | `EVD-TCM16-005-2` |
| `receiptIds/2` | `EVD-TCM16-005-3` |
| `receiptIds/3` | `EVD-TCM16-005-4` |
| `coverage` | `Queryable` |
| `testId` | `TEST-TCM16-005` |
| `validationId` | `VAL-TCM16-005` |
| `validationEvidenceId` | `EVD-TEST-TCM16-005` |
| `allowedConclusion` | `clock-uncertainty` |
| `gapId` | `GAP-TCM16-005` |
| `gap` | `相関Windowより時刻誤差が大きい` |
| `owner` | `SYNTH-TCM16-OWNER` |
| `dueAt` | `2026-09-22T00:00:00Z` |
| `reassessment` | `Schema、対象版、時間精度、保持、Identity、Consumer目的が変われば再比較。` |

### rows ROW-TCM16-006

| Field | Value |
|---|---|
| `id` | `ROW-TCM16-006` |
| `questionId` | `EQ-TCM16-006` |
| `fixtureId` | `FIX-TCM16-006` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `producerId` | `SYNTH-PRODUCER-TCM16` |
| `collectorId` | `SYNTH-COLLECTOR-TCM16` |
| `transport` | `offline-supplied-records` |
| `schemaVersion` | `TCM16-EVENT-1` |
| `normalizerVersion` | `NORM-TCM16-2` |
| `identityNamespace` | `SYNTH-TCM16` |
| `clockSource` | `SYNTH-UTC-CLOCK` |
| `timezone` | `UTC` |
| `clockUncertaintySeconds` | `2` |
| `ingestDelaySeconds` | `2` |
| `retentionStart` | `2026-09-21T00:00:00Z` |
| `retentionEnd` | `2026-09-23T00:00:00Z` |
| `integrityReference` | `SYNTH-ORIGINAL-TCM16-006` |
| `integrityMeaning` | `supplied-byte-comparison-not-authenticity` |
| `classification` | `public-synthetic-only` |
| `processingBasis` | `synthetic-reading-only` |
| `accessRole` | `SYNTH-HUNT-READER` |
| `receiptIds/0` | `EVD-TCM16-006-1` |
| `receiptIds/1` | `EVD-TCM16-006-2` |
| `receiptIds/2` | `EVD-TCM16-006-3` |
| `receiptIds/3` | `EVD-TCM16-006-4` |
| `coverage` | `Queryable` |
| `testId` | `TEST-TCM16-006` |
| `validationId` | `VAL-TCM16-006` |
| `validationEvidenceId` | `EVD-TEST-TCM16-006` |
| `allowedConclusion` | `identity-normalization-mismatch` |
| `gapId` | `GAP-TCM16-006` |
| `gap` | `同じID文字列でも正規化版が違う` |
| `owner` | `SYNTH-TCM16-OWNER` |
| `dueAt` | `2026-09-22T00:00:00Z` |
| `reassessment` | `Schema、対象版、時間精度、保持、Identity、Consumer目的が変われば再比較。` |

### rows ROW-TCM16-007

| Field | Value |
|---|---|
| `id` | `ROW-TCM16-007` |
| `questionId` | `EQ-TCM16-007` |
| `fixtureId` | `FIX-TCM16-007` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `producerId` | `SYNTH-PRODUCER-TCM16` |
| `collectorId` | `SYNTH-COLLECTOR-TCM16` |
| `transport` | `offline-supplied-records` |
| `schemaVersion` | `TCM16-EVENT-1` |
| `normalizerVersion` | `NORM-TCM16-1` |
| `identityNamespace` | `SYNTH-TCM16` |
| `clockSource` | `SYNTH-UTC-CLOCK` |
| `timezone` | `UTC` |
| `clockUncertaintySeconds` | `2` |
| `ingestDelaySeconds` | `2` |
| `retentionStart` | `2026-09-21T00:00:00Z` |
| `retentionEnd` | `2026-09-23T00:00:00Z` |
| `integrityReference` | `SYNTH-ORIGINAL-TCM16-007` |
| `integrityMeaning` | `supplied-byte-comparison-not-authenticity` |
| `classification` | `public-synthetic-only` |
| `processingBasis` | `synthetic-reading-only` |
| `accessRole` | `SYNTH-HUNT-READER` |
| `receiptIds` | `[]` |
| `coverage` | `Required` |
| `testId` | `TEST-TCM16-007` |
| `validationId` | `VAL-TCM16-007` |
| `validationEvidenceId` | `EVD-TEST-TCM16-007` |
| `allowedConclusion` | `producer-evidence-missing` |
| `gapId` | `GAP-TCM16-007` |
| `gap` | `Workload API Eventを必要とするが未生成` |
| `owner` | `SYNTH-TCM16-OWNER` |
| `dueAt` | `2026-09-22T00:00:00Z` |
| `reassessment` | `Schema、対象版、時間精度、保持、Identity、Consumer目的が変われば再比較。` |

### rows ROW-TCM16-008

| Field | Value |
|---|---|
| `id` | `ROW-TCM16-008` |
| `questionId` | `EQ-TCM16-008` |
| `fixtureId` | `FIX-TCM16-008` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `producerId` | `SYNTH-PRODUCER-TCM16` |
| `collectorId` | `SYNTH-COLLECTOR-TCM16` |
| `transport` | `offline-supplied-records` |
| `schemaVersion` | `TCM16-EVENT-1` |
| `normalizerVersion` | `NORM-TCM16-1` |
| `identityNamespace` | `SYNTH-TCM16` |
| `clockSource` | `SYNTH-UTC-CLOCK` |
| `timezone` | `UTC` |
| `clockUncertaintySeconds` | `2` |
| `ingestDelaySeconds` | `2` |
| `retentionStart` | `2026-09-21T00:00:00Z` |
| `retentionEnd` | `2026-09-23T00:00:00Z` |
| `integrityReference` | `SYNTH-ORIGINAL-TCM16-008` |
| `integrityMeaning` | `supplied-byte-comparison-not-authenticity` |
| `classification` | `public-synthetic-only` |
| `processingBasis` | `unknown` |
| `accessRole` | `SYNTH-IR-READER` |
| `receiptIds` | `[]` |
| `coverage` | `Unknown` |
| `testId` | `TEST-TCM16-008` |
| `validationId` | `VAL-TCM16-008` |
| `validationEvidenceId` | `EVD-TEST-TCM16-008` |
| `allowedConclusion` | `privacy-basis-unknown` |
| `gapId` | `GAP-TCM16-008` |
| `gap` | `Authentication contextの取扱根拠が未確認` |
| `owner` | `SYNTH-TCM16-OWNER` |
| `dueAt` | `2026-09-22T00:00:00Z` |
| `reassessment` | `Schema、対象版、時間精度、保持、Identity、Consumer目的が変われば再比較。` |

### rows ROW-TCM16-009

| Field | Value |
|---|---|
| `id` | `ROW-TCM16-009` |
| `questionId` | `EQ-TCM16-009` |
| `fixtureId` | `FIX-TCM16-009` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `producerId` | `SYNTH-PRODUCER-TCM16` |
| `collectorId` | `SYNTH-COLLECTOR-TCM16` |
| `transport` | `offline-supplied-records` |
| `schemaVersion` | `TCM16-EVENT-1` |
| `normalizerVersion` | `NORM-TCM16-1` |
| `identityNamespace` | `SYNTH-TCM16` |
| `clockSource` | `SYNTH-UTC-CLOCK` |
| `timezone` | `UTC` |
| `clockUncertaintySeconds` | `2` |
| `ingestDelaySeconds` | `2` |
| `retentionStart` | `2026-09-21T00:00:00Z` |
| `retentionEnd` | `2026-09-23T00:00:00Z` |
| `integrityReference` | `SYNTH-ORIGINAL-TCM16-009` |
| `integrityMeaning` | `supplied-byte-comparison-not-authenticity` |
| `classification` | `public-synthetic-only` |
| `processingBasis` | `synthetic-reading-only` |
| `accessRole` | `SYNTH-DFIR-READER` |
| `receiptIds/0` | `EVD-TCM16-009-1` |
| `receiptIds/1` | `EVD-TCM16-009-2` |
| `coverage` | `Collected` |
| `testId` | `TEST-TCM16-009` |
| `validationId` | `VAL-TCM16-009` |
| `validationEvidenceId` | `EVD-TEST-TCM16-009` |
| `allowedConclusion` | `retention-gap` |
| `gapId` | `GAP-TCM16-009` |
| `gap` | `同意変更の入力はあるが調査用保持が不足` |
| `owner` | `SYNTH-TCM16-OWNER` |
| `dueAt` | `2026-09-22T00:00:00Z` |
| `reassessment` | `Schema、対象版、時間精度、保持、Identity、Consumer目的が変われば再比較。` |

### rows ROW-TCM16-010

| Field | Value |
|---|---|
| `id` | `ROW-TCM16-010` |
| `questionId` | `EQ-TCM16-010` |
| `fixtureId` | `FIX-TCM16-010` |
| `subjectId` | `APP-TCM16-001` |
| `revision` | `TCM16-REV-001` |
| `producerId` | `SYNTH-PRODUCER-TCM16` |
| `collectorId` | `SYNTH-COLLECTOR-TCM16` |
| `transport` | `offline-supplied-records` |
| `schemaVersion` | `TCM16-EVENT-1` |
| `normalizerVersion` | `NORM-TCM16-1` |
| `identityNamespace` | `SYNTH-TCM16` |
| `clockSource` | `SYNTH-UTC-CLOCK` |
| `timezone` | `UTC` |
| `clockUncertaintySeconds` | `2` |
| `ingestDelaySeconds` | `2` |
| `retentionStart` | `2026-09-21T00:00:00Z` |
| `retentionEnd` | `2026-09-23T00:00:00Z` |
| `integrityReference` | `SYNTH-ORIGINAL-TCM16-010` |
| `integrityMeaning` | `supplied-byte-comparison-not-authenticity` |
| `classification` | `public-synthetic-only` |
| `processingBasis` | `synthetic-reading-only` |
| `accessRole` | `SYNTH-DETECTION-READER` |
| `receiptIds/0` | `EVD-TCM16-010-1` |
| `receiptIds/1` | `EVD-TCM16-010-2` |
| `receiptIds/2` | `EVD-TCM16-010-3` |
| `receiptIds/3` | `EVD-TCM16-010-4` |
| `coverage` | `Validated` |
| `testId` | `TEST-TCM16-010` |
| `validationId` | `VAL-TCM16-010` |
| `validationEvidenceId` | `EVD-TEST-TCM16-010` |
| `allowedConclusion` | `not-observed-in-synthetic-window` |
| `gapId` | `GAP-TCM16-010` |
| `gap` | `限定合成Windowだけの未観測。実侵害の不存在ではない。` |
| `owner` | `SYNTH-TCM16-OWNER` |
| `dueAt` | `2026-09-22T00:00:00Z` |
| `reassessment` | `Schema、対象版、時間精度、保持、Identity、Consumer目的が変われば再比較。` |

### handoffs HOF-TCM16-17

| Field | Value |
|---|---|
| `id` | `HOF-TCM16-17` |
| `targetChapter` | `17` |
| `consumer` | `Detection` |
| `recordId` | `TCM-2026-016` |
| `rowIds/0` | `ROW-TCM16-001` |
| `rowIds/1` | `ROW-TCM16-002` |
| `rowIds/2` | `ROW-TCM16-010` |
| `status` | `planned-not-delivered` |
| `receiptId` | `null` |
| `executionAuthorized` | `false` |
| `owner` | `SYNTH-DETECTION-OWNER` |
| `dueAt` | `2026-09-22T00:00:00Z` |
| `acceptance` | `受け手が対象版、問い、必要Field、許される結論、Gap、再評価条件を別途照合する。` |
| `limitation` | `参照IDは受領・実行許可・検知成功の証拠ではない。` |

### handoffs HOF-TCM16-18

| Field | Value |
|---|---|
| `id` | `HOF-TCM16-18` |
| `targetChapter` | `18` |
| `consumer` | `Hunt` |
| `recordId` | `TCM-2026-016` |
| `rowIds/0` | `ROW-TCM16-005` |
| `rowIds/1` | `ROW-TCM16-006` |
| `rowIds/2` | `ROW-TCM16-007` |
| `status` | `planned-not-delivered` |
| `receiptId` | `null` |
| `executionAuthorized` | `false` |
| `owner` | `SYNTH-HUNT-OWNER` |
| `dueAt` | `2026-09-22T00:00:00Z` |
| `acceptance` | `受け手が対象版、問い、必要Field、許される結論、Gap、再評価条件を別途照合する。` |
| `limitation` | `参照IDは受領・実行許可・検知成功の証拠ではない。` |

### handoffs HOF-TCM16-19

| Field | Value |
|---|---|
| `id` | `HOF-TCM16-19` |
| `targetChapter` | `19` |
| `consumer` | `IR` |
| `recordId` | `TCM-2026-016` |
| `rowIds/0` | `ROW-TCM16-003` |
| `rowIds/1` | `ROW-TCM16-008` |
| `status` | `planned-not-delivered` |
| `receiptId` | `null` |
| `executionAuthorized` | `false` |
| `owner` | `SYNTH-IR-OWNER` |
| `dueAt` | `2026-09-22T00:00:00Z` |
| `acceptance` | `受け手が対象版、問い、必要Field、許される結論、Gap、再評価条件を別途照合する。` |
| `limitation` | `参照IDは受領・実行許可・検知成功の証拠ではない。` |

### handoffs HOF-TCM16-20

| Field | Value |
|---|---|
| `id` | `HOF-TCM16-20` |
| `targetChapter` | `20` |
| `consumer` | `DFIR` |
| `recordId` | `TCM-2026-016` |
| `rowIds/0` | `ROW-TCM16-009` |
| `status` | `planned-not-delivered` |
| `receiptId` | `null` |
| `executionAuthorized` | `false` |
| `owner` | `SYNTH-DFIR-OWNER` |
| `dueAt` | `2026-09-22T00:00:00Z` |
| `acceptance` | `受け手が対象版、問い、必要Field、許される結論、Gap、再評価条件を別途照合する。` |
| `limitation` | `参照IDは受領・実行許可・検知成功の証拠ではない。` |

## 読解課題・停止・Cleanup

各Rowの問い、段階のEvidence、時刻・同一性・保持条件、結論、Gap/Owner/期限を記す。未知入力や実データらしい内容、外部接続、Scope不明を見つけたら停止し、追加取得しない。自分のメモだけを整理し、供給Recordや正本は変更しない。

判断不能は不合格ではない。根拠の不足を明示し、Consumerごとの次の確認へ結べることが成果である。Handoffは別途の受領記録がない限り未配達のままである。
