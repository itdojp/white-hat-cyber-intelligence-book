# 第6章 完全合成記入例：Signal Flow Diagram

## 読み方と安全境界

これは完全合成の非実行教材であり、製品Log schemaや実環境の観測結果ではない。SFM-2026-001はCASE-2026-001をrefinesする教育用補足である。第4章・第5章の元記録は保持し、親のControl、Gap、Decisionは変更しない。

Purposeは同一Flowの受領記録をたどること、Prerequisiteは第6章とART-16の読了、Authority / Scopeはread-only-synthetic-dataだけである。実Credential、Token、Cookie、実Logを含めず、外部接続と認証試行は禁止する。Expected evidenceは段階とGapの記入、Impactは教材読み取りだけである。実Dataの疑いと追跡の不一致でStopし、Cleanupは自分の演習コピーの整理だけとする。

[第6章](../manuscript/06-observable-systems.md)、[ART-16](../templates/signal-flow-diagram.md)、[正本JSON](fixtures/ch06-signal-flow.json)を参照する。

## Document Control

| Field | Value |
|---|---|
| schemaVersion | 1.0.0 |
| synthetic | true |
| artifactId | ART-16 |
| mapId | SFM-2026-001 |
| parentCaseId | CASE-2026-001 |
| relation | refines |
| parentThreatModelId | TM-2026-001 |
| parentBehaviorMapId | BMAP-2026-001 |
| decisionRequirementId | DR-2026-001 |
| authorizationRecordId | AUTH-CASE-2026-001 |
| scope | read-only-synthetic-data |
| parentState | Independent synthetic teaching supplement; no parent observation, control, gap or decision is changed. |

Nodeのroleは各Flowの同名Field群を意味する。actorはactorId、identityはidentityClassとcredentialClass、requestはprotocolClassとoperationPurpose、gatewayはplaneとboundaryIds、authorizationはauthenticationResultとauthorizationResult、effectはeffect、producerはproducerIdとeventClass、collectorはcollectorIdとCollected受領票、normalizerは受領票のnormalizationVersionとfieldNames、retentionは保持区間、queryはqueryEndpointとqueryStart / queryEnd、consumerはconsumerIdとdetectionIdへ結び付く。NodeとEdgeのIDを省略せず表でたどる。

受領票のsyntheticは全てtrue。Produced / Collectedは過去の受領を表し、Retained / Queryable / ValidatedのrecordedAtはassessmentTimeと一致する。queryStartは含みqueryEndは含まない。Clock uncertaintyを含むEvent時刻が検索区間内に収まる必要がある。Query用権限Roleは各Flowのownerであり、queryEndpointは名前だけで接続しない。

## SF-2026-001 — Produced

| Field | Value |
|---|---|
| flowId | SF-2026-001 |
| parentBehaviorId | BM-2026-002 |
| assetIds | ASSET-2026-002, ASSET-2026-005 |
| boundaryIds | TB-2026-001, TB-2026-003 |
| parentFlowIds | FLOW-2026-002, FLOW-2026-004 |
| parentTelemetryId | TEL-BM-002 |
| parentGapId | GAP-BM-002 |
| actorId | SYNTH-ACTOR-SF-001 |
| identityClass | Human |
| credentialClass | interactive-authentication |
| protocolClass | HTTPS / OAuth role model only |
| plane | Control |
| operationPurpose | 管理者同意変更の合成記録 |
| authenticationResult | Confirmed in synthetic model |
| authorizationResult | Allow in synthetic model |
| effect | Consent state change |
| producerId | SYNTH-PRODUCER-001 |
| eventId | SYNTH-EVENT-SF-001 |
| eventClass | consent-change |
| collectorId | SYNTH-COLLECTOR-001 |
| queryEndpoint | evidence-query.example |
| consumerId | SYNTH-CONSUMER-001 |
| telemetryId | TEL-SF-001 |
| detectionId | なし |
| coverage | Produced |
| eventTime | 2026-09-01T00:00:00+00:00 |
| assessmentTime | 2026-09-12T00:00:00+00:00 |
| retentionStart | 2026-08-31T00:00:00+00:00 |
| retentionEnd | 2026-10-01T00:00:00+00:00 |
| clockSource | SYNTH-CLOCK-UTC |
| clockUncertaintySeconds | 2 |
| correlationKeys | tenant, application, requestId, eventId |
| requiredFields | synthetic, eventId, actorId, identityClass, eventTime, tenant, application, requestId, authorizationResult |
| gapId | GAP-SF-001 |
| gap | 収集経路の受領票がない |
| allowedConclusion | 同一Flowの合成受領記録が示す段階だけ。Eventや侵害の不存在は判断しない。 |
| alternative | 正常な変更、Collection不備、保持期限切れ、権限不足という別説明を比較する。 |
| confidence | 中 |
| owner | SYNTH-SOC-REVIEWER |
| reviewDate | 2026-09-20 |
| reassessment | 対象期間、Field、Identity binding、変換版または受領記録の変更時に再評価する。 |
| queryStart | 2026-08-31T23:59:58+00:00 |
| queryEnd | 2026-09-01T00:00:03+00:00 |

### Nodes

| ID | Role |
|---|---|
| N-SF-001-01 | actor |
| N-SF-001-02 | identity |
| N-SF-001-03 | request |
| N-SF-001-04 | gateway |
| N-SF-001-05 | authorization |
| N-SF-001-06 | effect |
| N-SF-001-07 | producer |
| N-SF-001-08 | collector |
| N-SF-001-09 | normalizer |
| N-SF-001-10 | retention |
| N-SF-001-11 | query |
| N-SF-001-12 | consumer |

### Edges

| ID | From | To |
|---|---|---|
| E-SF-001-01 | N-SF-001-01 | N-SF-001-02 |
| E-SF-001-02 | N-SF-001-02 | N-SF-001-03 |
| E-SF-001-03 | N-SF-001-03 | N-SF-001-04 |
| E-SF-001-04 | N-SF-001-04 | N-SF-001-05 |
| E-SF-001-05 | N-SF-001-05 | N-SF-001-06 |
| E-SF-001-06 | N-SF-001-06 | N-SF-001-07 |
| E-SF-001-07 | N-SF-001-07 | N-SF-001-08 |
| E-SF-001-08 | N-SF-001-08 | N-SF-001-09 |
| E-SF-001-09 | N-SF-001-09 | N-SF-001-10 |
| E-SF-001-10 | N-SF-001-10 | N-SF-001-11 |
| E-SF-001-11 | N-SF-001-11 | N-SF-001-12 |

### Evidence receipts

#### EVD-SF-001-01

| Field | Value |
|---|---|
| id | EVD-SF-001-01 |
| synthetic | true |
| flowId | SF-2026-001 |
| eventId | SYNTH-EVENT-SF-001 |
| stage | Produced |
| recordedAt | 2026-09-01T00:00:01+00:00 |
| fieldNames | synthetic, eventId, actorId, identityClass, eventTime, tenant, application, requestId, authorizationResult |
| normalizationVersion | 1.0.0 |

### Test

Testは未実施。別Flowや親CaseのPassを借用しない。

## SF-2026-002 — Collected

| Field | Value |
|---|---|
| flowId | SF-2026-002 |
| parentBehaviorId | BM-2026-006 |
| assetIds | ASSET-2026-002, ASSET-2026-003, ASSET-2026-004 |
| boundaryIds | TB-2026-003, TB-2026-007 |
| parentFlowIds | FLOW-2026-004, FLOW-2026-005 |
| parentTelemetryId | TEL-BM-006 |
| parentGapId | GAP-BM-006 |
| actorId | SYNTH-ACTOR-SF-002 |
| identityClass | Service |
| credentialClass | service-authentication |
| protocolClass | HTTPS / OAuth role model only |
| plane | Control |
| operationPurpose | Audit exportの合成受領記録 |
| authenticationResult | Confirmed in synthetic model |
| authorizationResult | Allow in synthetic model |
| effect | Export state change |
| producerId | SYNTH-PRODUCER-002 |
| eventId | SYNTH-EVENT-SF-002 |
| eventClass | audit-export |
| collectorId | SYNTH-COLLECTOR-002 |
| queryEndpoint | evidence-query.example |
| consumerId | SYNTH-CONSUMER-002 |
| telemetryId | TEL-SF-002 |
| detectionId | なし |
| coverage | Collected |
| eventTime | 2026-09-01T00:00:00+00:00 |
| assessmentTime | 2026-09-12T00:00:00+00:00 |
| retentionStart | 2026-08-31T00:00:00+00:00 |
| retentionEnd | 2026-09-05T00:00:00+00:00 |
| clockSource | SYNTH-CLOCK-UTC |
| clockUncertaintySeconds | 2 |
| correlationKeys | tenant, application, requestId, eventId |
| requiredFields | synthetic, eventId, actorId, identityClass, eventTime, tenant, application, requestId, authorizationResult |
| gapId | GAP-SF-002 |
| gap | 以前収集した記録が保持期限切れ |
| allowedConclusion | 同一Flowの合成受領記録が示す段階だけ。Eventや侵害の不存在は判断しない。 |
| alternative | 正常な変更、Collection不備、保持期限切れ、権限不足という別説明を比較する。 |
| confidence | 中 |
| owner | SYNTH-PLATFORM-OWNER |
| reviewDate | 2026-09-20 |
| reassessment | 対象期間、Field、Identity binding、変換版または受領記録の変更時に再評価する。 |
| queryStart | 2026-08-31T23:59:58+00:00 |
| queryEnd | 2026-09-01T00:00:03+00:00 |

### Nodes

| ID | Role |
|---|---|
| N-SF-002-01 | actor |
| N-SF-002-02 | identity |
| N-SF-002-03 | request |
| N-SF-002-04 | gateway |
| N-SF-002-05 | authorization |
| N-SF-002-06 | effect |
| N-SF-002-07 | producer |
| N-SF-002-08 | collector |
| N-SF-002-09 | normalizer |
| N-SF-002-10 | retention |
| N-SF-002-11 | query |
| N-SF-002-12 | consumer |

### Edges

| ID | From | To |
|---|---|---|
| E-SF-002-01 | N-SF-002-01 | N-SF-002-02 |
| E-SF-002-02 | N-SF-002-02 | N-SF-002-03 |
| E-SF-002-03 | N-SF-002-03 | N-SF-002-04 |
| E-SF-002-04 | N-SF-002-04 | N-SF-002-05 |
| E-SF-002-05 | N-SF-002-05 | N-SF-002-06 |
| E-SF-002-06 | N-SF-002-06 | N-SF-002-07 |
| E-SF-002-07 | N-SF-002-07 | N-SF-002-08 |
| E-SF-002-08 | N-SF-002-08 | N-SF-002-09 |
| E-SF-002-09 | N-SF-002-09 | N-SF-002-10 |
| E-SF-002-10 | N-SF-002-10 | N-SF-002-11 |
| E-SF-002-11 | N-SF-002-11 | N-SF-002-12 |

### Evidence receipts

#### EVD-SF-002-01

| Field | Value |
|---|---|
| id | EVD-SF-002-01 |
| synthetic | true |
| flowId | SF-2026-002 |
| eventId | SYNTH-EVENT-SF-002 |
| stage | Produced |
| recordedAt | 2026-09-01T00:00:01+00:00 |
| fieldNames | synthetic, eventId, actorId, identityClass, eventTime, tenant, application, requestId, authorizationResult |
| normalizationVersion | 1.0.0 |

#### EVD-SF-002-02

| Field | Value |
|---|---|
| id | EVD-SF-002-02 |
| synthetic | true |
| flowId | SF-2026-002 |
| eventId | SYNTH-EVENT-SF-002 |
| stage | Collected |
| recordedAt | 2026-09-01T00:00:02+00:00 |
| fieldNames | synthetic, eventId, actorId, identityClass, eventTime, tenant, application, requestId, authorizationResult |
| normalizationVersion | 1.0.0 |

### Test

Testは未実施。別Flowや親CaseのPassを借用しない。

## SF-2026-003 — Retained

| Field | Value |
|---|---|
| flowId | SF-2026-003 |
| parentBehaviorId | BM-2026-003 |
| assetIds | ASSET-2026-001, ASSET-2026-003 |
| boundaryIds | TB-2026-002, TB-2026-003 |
| parentFlowIds | FLOW-2026-004 |
| parentTelemetryId | TEL-BM-003 |
| parentGapId | GAP-BM-003 |
| actorId | SYNTH-ACTOR-SF-003 |
| identityClass | Workload |
| credentialClass | workload-authentication |
| protocolClass | HTTPS / OAuth role model only |
| plane | Data |
| operationPurpose | Customer Data APIの合成利用記録 |
| authenticationResult | Confirmed in synthetic model |
| authorizationResult | Allow in synthetic model |
| effect | Data access summary |
| producerId | SYNTH-PRODUCER-003 |
| eventId | SYNTH-EVENT-SF-003 |
| eventClass | api-access |
| collectorId | SYNTH-COLLECTOR-003 |
| queryEndpoint | evidence-query.example |
| consumerId | SYNTH-CONSUMER-003 |
| telemetryId | TEL-SF-003 |
| detectionId | なし |
| coverage | Retained |
| eventTime | 2026-09-01T00:00:00+00:00 |
| assessmentTime | 2026-09-12T00:00:00+00:00 |
| retentionStart | 2026-08-31T00:00:00+00:00 |
| retentionEnd | 2026-10-01T00:00:00+00:00 |
| clockSource | SYNTH-CLOCK-UTC |
| clockUncertaintySeconds | 2 |
| correlationKeys | tenant, application, requestId, eventId |
| requiredFields | synthetic, eventId, actorId, identityClass, eventTime, tenant, application, requestId, authorizationResult |
| gapId | GAP-SF-003 |
| gap | 保存しているが検索権限を確認していない |
| allowedConclusion | 同一Flowの合成受領記録が示す段階だけ。Eventや侵害の不存在は判断しない。 |
| alternative | 正常な変更、Collection不備、保持期限切れ、権限不足という別説明を比較する。 |
| confidence | 中 |
| owner | SYNTH-PLATFORM-OWNER |
| reviewDate | 2026-09-20 |
| reassessment | 対象期間、Field、Identity binding、変換版または受領記録の変更時に再評価する。 |
| queryStart | 2026-08-31T23:59:58+00:00 |
| queryEnd | 2026-09-01T00:00:03+00:00 |

### Nodes

| ID | Role |
|---|---|
| N-SF-003-01 | actor |
| N-SF-003-02 | identity |
| N-SF-003-03 | request |
| N-SF-003-04 | gateway |
| N-SF-003-05 | authorization |
| N-SF-003-06 | effect |
| N-SF-003-07 | producer |
| N-SF-003-08 | collector |
| N-SF-003-09 | normalizer |
| N-SF-003-10 | retention |
| N-SF-003-11 | query |
| N-SF-003-12 | consumer |

### Edges

| ID | From | To |
|---|---|---|
| E-SF-003-01 | N-SF-003-01 | N-SF-003-02 |
| E-SF-003-02 | N-SF-003-02 | N-SF-003-03 |
| E-SF-003-03 | N-SF-003-03 | N-SF-003-04 |
| E-SF-003-04 | N-SF-003-04 | N-SF-003-05 |
| E-SF-003-05 | N-SF-003-05 | N-SF-003-06 |
| E-SF-003-06 | N-SF-003-06 | N-SF-003-07 |
| E-SF-003-07 | N-SF-003-07 | N-SF-003-08 |
| E-SF-003-08 | N-SF-003-08 | N-SF-003-09 |
| E-SF-003-09 | N-SF-003-09 | N-SF-003-10 |
| E-SF-003-10 | N-SF-003-10 | N-SF-003-11 |
| E-SF-003-11 | N-SF-003-11 | N-SF-003-12 |

### Evidence receipts

#### EVD-SF-003-01

| Field | Value |
|---|---|
| id | EVD-SF-003-01 |
| synthetic | true |
| flowId | SF-2026-003 |
| eventId | SYNTH-EVENT-SF-003 |
| stage | Produced |
| recordedAt | 2026-09-01T00:00:01+00:00 |
| fieldNames | synthetic, eventId, actorId, identityClass, eventTime, tenant, application, requestId, authorizationResult |
| normalizationVersion | 1.0.0 |

#### EVD-SF-003-02

| Field | Value |
|---|---|
| id | EVD-SF-003-02 |
| synthetic | true |
| flowId | SF-2026-003 |
| eventId | SYNTH-EVENT-SF-003 |
| stage | Collected |
| recordedAt | 2026-09-01T00:00:02+00:00 |
| fieldNames | synthetic, eventId, actorId, identityClass, eventTime, tenant, application, requestId, authorizationResult |
| normalizationVersion | 1.0.0 |

#### EVD-SF-003-03

| Field | Value |
|---|---|
| id | EVD-SF-003-03 |
| synthetic | true |
| flowId | SF-2026-003 |
| eventId | SYNTH-EVENT-SF-003 |
| stage | Retained |
| recordedAt | 2026-09-12T00:00:00+00:00 |
| fieldNames | synthetic, eventId, actorId, identityClass, eventTime, tenant, application, requestId, authorizationResult |
| normalizationVersion | 1.0.0 |

### Test

Testは未実施。別Flowや親CaseのPassを借用しない。

## SF-2026-004 — Queryable

| Field | Value |
|---|---|
| flowId | SF-2026-004 |
| parentBehaviorId | BM-2026-002 |
| assetIds | ASSET-2026-002, ASSET-2026-005 |
| boundaryIds | TB-2026-001, TB-2026-003 |
| parentFlowIds | FLOW-2026-002, FLOW-2026-004 |
| parentTelemetryId | TEL-BM-002 |
| parentGapId | GAP-BM-002 |
| actorId | SYNTH-ACTOR-SF-004 |
| identityClass | Human |
| credentialClass | interactive-authentication |
| protocolClass | HTTPS / OAuth role model only |
| plane | Control |
| operationPurpose | 正常な同意変更の合成検索記録 |
| authenticationResult | Confirmed in synthetic model |
| authorizationResult | Allow in synthetic model |
| effect | Consent state change |
| producerId | SYNTH-PRODUCER-004 |
| eventId | SYNTH-EVENT-SF-004 |
| eventClass | consent-change |
| collectorId | SYNTH-COLLECTOR-004 |
| queryEndpoint | evidence-query.example |
| consumerId | SYNTH-CONSUMER-004 |
| telemetryId | TEL-SF-004 |
| detectionId | なし |
| coverage | Queryable |
| eventTime | 2026-09-01T00:00:00+00:00 |
| assessmentTime | 2026-09-12T00:00:00+00:00 |
| retentionStart | 2026-08-31T00:00:00+00:00 |
| retentionEnd | 2026-10-01T00:00:00+00:00 |
| clockSource | SYNTH-CLOCK-UTC |
| clockUncertaintySeconds | 2 |
| correlationKeys | tenant, application, requestId, eventId |
| requiredFields | synthetic, eventId, actorId, identityClass, eventTime, tenant, application, requestId, authorizationResult |
| gapId | GAP-SF-004 |
| gap | 判定条件のTestは未実施 |
| allowedConclusion | 同一Flowの合成受領記録が示す段階だけ。Eventや侵害の不存在は判断しない。 |
| alternative | 正常な変更、Collection不備、保持期限切れ、権限不足という別説明を比較する。 |
| confidence | 中 |
| owner | SYNTH-SOC-REVIEWER |
| reviewDate | 2026-09-20 |
| reassessment | 対象期間、Field、Identity binding、変換版または受領記録の変更時に再評価する。 |
| queryStart | 2026-08-31T23:59:58+00:00 |
| queryEnd | 2026-09-01T00:00:03+00:00 |

### Nodes

| ID | Role |
|---|---|
| N-SF-004-01 | actor |
| N-SF-004-02 | identity |
| N-SF-004-03 | request |
| N-SF-004-04 | gateway |
| N-SF-004-05 | authorization |
| N-SF-004-06 | effect |
| N-SF-004-07 | producer |
| N-SF-004-08 | collector |
| N-SF-004-09 | normalizer |
| N-SF-004-10 | retention |
| N-SF-004-11 | query |
| N-SF-004-12 | consumer |

### Edges

| ID | From | To |
|---|---|---|
| E-SF-004-01 | N-SF-004-01 | N-SF-004-02 |
| E-SF-004-02 | N-SF-004-02 | N-SF-004-03 |
| E-SF-004-03 | N-SF-004-03 | N-SF-004-04 |
| E-SF-004-04 | N-SF-004-04 | N-SF-004-05 |
| E-SF-004-05 | N-SF-004-05 | N-SF-004-06 |
| E-SF-004-06 | N-SF-004-06 | N-SF-004-07 |
| E-SF-004-07 | N-SF-004-07 | N-SF-004-08 |
| E-SF-004-08 | N-SF-004-08 | N-SF-004-09 |
| E-SF-004-09 | N-SF-004-09 | N-SF-004-10 |
| E-SF-004-10 | N-SF-004-10 | N-SF-004-11 |
| E-SF-004-11 | N-SF-004-11 | N-SF-004-12 |

### Evidence receipts

#### EVD-SF-004-01

| Field | Value |
|---|---|
| id | EVD-SF-004-01 |
| synthetic | true |
| flowId | SF-2026-004 |
| eventId | SYNTH-EVENT-SF-004 |
| stage | Produced |
| recordedAt | 2026-09-01T00:00:01+00:00 |
| fieldNames | synthetic, eventId, actorId, identityClass, eventTime, tenant, application, requestId, authorizationResult |
| normalizationVersion | 1.0.0 |

#### EVD-SF-004-02

| Field | Value |
|---|---|
| id | EVD-SF-004-02 |
| synthetic | true |
| flowId | SF-2026-004 |
| eventId | SYNTH-EVENT-SF-004 |
| stage | Collected |
| recordedAt | 2026-09-01T00:00:02+00:00 |
| fieldNames | synthetic, eventId, actorId, identityClass, eventTime, tenant, application, requestId, authorizationResult |
| normalizationVersion | 1.0.0 |

#### EVD-SF-004-03

| Field | Value |
|---|---|
| id | EVD-SF-004-03 |
| synthetic | true |
| flowId | SF-2026-004 |
| eventId | SYNTH-EVENT-SF-004 |
| stage | Retained |
| recordedAt | 2026-09-12T00:00:00+00:00 |
| fieldNames | synthetic, eventId, actorId, identityClass, eventTime, tenant, application, requestId, authorizationResult |
| normalizationVersion | 1.0.0 |

#### EVD-SF-004-04

| Field | Value |
|---|---|
| id | EVD-SF-004-04 |
| synthetic | true |
| flowId | SF-2026-004 |
| eventId | SYNTH-EVENT-SF-004 |
| stage | Queryable |
| recordedAt | 2026-09-12T00:00:00+00:00 |
| fieldNames | synthetic, eventId, actorId, identityClass, eventTime, tenant, application, requestId, authorizationResult |
| normalizationVersion | 1.0.0 |

### Test

Testは未実施。別Flowや親CaseのPassを借用しない。

## SF-2026-005 — Validated

| Field | Value |
|---|---|
| flowId | SF-2026-005 |
| parentBehaviorId | BM-2026-004 |
| assetIds | ASSET-2026-002, ASSET-2026-005 |
| boundaryIds | TB-2026-001, TB-2026-003 |
| parentFlowIds | FLOW-2026-002, FLOW-2026-004 |
| parentTelemetryId | TEL-BM-004 |
| parentGapId | GAP-BM-004 |
| actorId | SYNTH-ACTOR-SF-005 |
| identityClass | Human |
| credentialClass | interactive-authentication |
| protocolClass | HTTPS / OAuth role model only |
| plane | Control |
| operationPurpose | 同意Eventの合成経路検査 |
| authenticationResult | Confirmed in synthetic model |
| authorizationResult | Allow in synthetic model |
| effect | Consent state change |
| producerId | SYNTH-PRODUCER-005 |
| eventId | SYNTH-EVENT-SF-005 |
| eventClass | consent-change |
| collectorId | SYNTH-COLLECTOR-005 |
| queryEndpoint | evidence-query.example |
| consumerId | SYNTH-CONSUMER-005 |
| telemetryId | TEL-SF-005 |
| detectionId | DET-SF-005 |
| coverage | Validated |
| eventTime | 2026-09-01T00:00:00+00:00 |
| assessmentTime | 2026-09-12T00:00:00+00:00 |
| retentionStart | 2026-08-31T00:00:00+00:00 |
| retentionEnd | 2026-10-01T00:00:00+00:00 |
| clockSource | SYNTH-CLOCK-UTC |
| clockUncertaintySeconds | 2 |
| correlationKeys | tenant, application, requestId, eventId |
| requiredFields | synthetic, eventId, actorId, identityClass, eventTime, tenant, application, requestId, authorizationResult |
| gapId | GAP-SF-005 |
| gap | 教材の同一Flow突合だけ。親Controlや実製品の検証ではない |
| allowedConclusion | 同一Flowの合成受領記録が示す段階だけ。Eventや侵害の不存在は判断しない。 |
| alternative | 正常な変更、Collection不備、保持期限切れ、権限不足という別説明を比較する。 |
| confidence | 中 |
| owner | SYNTH-SOC-REVIEWER |
| reviewDate | 2026-09-20 |
| reassessment | 対象期間、Field、Identity binding、変換版または受領記録の変更時に再評価する。 |
| queryStart | 2026-08-31T23:59:58+00:00 |
| queryEnd | 2026-09-01T00:00:03+00:00 |

### Nodes

| ID | Role |
|---|---|
| N-SF-005-01 | actor |
| N-SF-005-02 | identity |
| N-SF-005-03 | request |
| N-SF-005-04 | gateway |
| N-SF-005-05 | authorization |
| N-SF-005-06 | effect |
| N-SF-005-07 | producer |
| N-SF-005-08 | collector |
| N-SF-005-09 | normalizer |
| N-SF-005-10 | retention |
| N-SF-005-11 | query |
| N-SF-005-12 | consumer |

### Edges

| ID | From | To |
|---|---|---|
| E-SF-005-01 | N-SF-005-01 | N-SF-005-02 |
| E-SF-005-02 | N-SF-005-02 | N-SF-005-03 |
| E-SF-005-03 | N-SF-005-03 | N-SF-005-04 |
| E-SF-005-04 | N-SF-005-04 | N-SF-005-05 |
| E-SF-005-05 | N-SF-005-05 | N-SF-005-06 |
| E-SF-005-06 | N-SF-005-06 | N-SF-005-07 |
| E-SF-005-07 | N-SF-005-07 | N-SF-005-08 |
| E-SF-005-08 | N-SF-005-08 | N-SF-005-09 |
| E-SF-005-09 | N-SF-005-09 | N-SF-005-10 |
| E-SF-005-10 | N-SF-005-10 | N-SF-005-11 |
| E-SF-005-11 | N-SF-005-11 | N-SF-005-12 |

### Evidence receipts

#### EVD-SF-005-01

| Field | Value |
|---|---|
| id | EVD-SF-005-01 |
| synthetic | true |
| flowId | SF-2026-005 |
| eventId | SYNTH-EVENT-SF-005 |
| stage | Produced |
| recordedAt | 2026-09-01T00:00:01+00:00 |
| fieldNames | synthetic, eventId, actorId, identityClass, eventTime, tenant, application, requestId, authorizationResult |
| normalizationVersion | 1.0.0 |

#### EVD-SF-005-02

| Field | Value |
|---|---|
| id | EVD-SF-005-02 |
| synthetic | true |
| flowId | SF-2026-005 |
| eventId | SYNTH-EVENT-SF-005 |
| stage | Collected |
| recordedAt | 2026-09-01T00:00:02+00:00 |
| fieldNames | synthetic, eventId, actorId, identityClass, eventTime, tenant, application, requestId, authorizationResult |
| normalizationVersion | 1.0.0 |

#### EVD-SF-005-03

| Field | Value |
|---|---|
| id | EVD-SF-005-03 |
| synthetic | true |
| flowId | SF-2026-005 |
| eventId | SYNTH-EVENT-SF-005 |
| stage | Retained |
| recordedAt | 2026-09-12T00:00:00+00:00 |
| fieldNames | synthetic, eventId, actorId, identityClass, eventTime, tenant, application, requestId, authorizationResult |
| normalizationVersion | 1.0.0 |

#### EVD-SF-005-04

| Field | Value |
|---|---|
| id | EVD-SF-005-04 |
| synthetic | true |
| flowId | SF-2026-005 |
| eventId | SYNTH-EVENT-SF-005 |
| stage | Queryable |
| recordedAt | 2026-09-12T00:00:00+00:00 |
| fieldNames | synthetic, eventId, actorId, identityClass, eventTime, tenant, application, requestId, authorizationResult |
| normalizationVersion | 1.0.0 |

#### EVD-SF-005-05

| Field | Value |
|---|---|
| id | EVD-SF-005-05 |
| synthetic | true |
| flowId | SF-2026-005 |
| eventId | SYNTH-EVENT-SF-005 |
| stage | Validated |
| recordedAt | 2026-09-12T00:00:00+00:00 |
| fieldNames | synthetic, eventId, actorId, identityClass, eventTime, tenant, application, requestId, authorizationResult |
| normalizationVersion | 1.0.0 |

### Test

| Field | Value |
|---|---|
| id | TEST-SF-005 |
| flowId | SF-2026-005 |
| scope | synthetic-flow-receipt-chain |
| version | 1.0.0 |
| expected | Produced, Collected, Retained, Queryable |
| actual | Produced, Collected, Retained, Queryable |
| result | Pass |

## SF-2026-006 — Unknown

| Field | Value |
|---|---|
| flowId | SF-2026-006 |
| parentBehaviorId | BM-2026-005 |
| assetIds | ASSET-2026-005, ASSET-2026-006, ASSET-2026-007 |
| boundaryIds | TB-2026-004, TB-2026-008 |
| parentFlowIds | FLOW-2026-003, FLOW-2026-006 |
| parentTelemetryId | TEL-BM-005 |
| parentGapId | GAP-BM-005 |
| actorId | SYNTH-ACTOR-SF-006 |
| identityClass | Workload |
| credentialClass | workload-authentication |
| protocolClass | HTTPS / OAuth role model only |
| plane | Data |
| operationPurpose | 現在のWorkload bindingの確認要求 |
| authenticationResult | Unknown |
| authorizationResult | Unknown |
| effect | Binding state unknown |
| producerId | SYNTH-PRODUCER-006 |
| eventId | SYNTH-EVENT-SF-006 |
| eventClass | workload-binding |
| collectorId | SYNTH-COLLECTOR-006 |
| queryEndpoint | evidence-query.example |
| consumerId | SYNTH-CONSUMER-006 |
| telemetryId | TEL-SF-006 |
| detectionId | なし |
| coverage | Unknown |
| eventTime | 2026-09-01T00:00:00+00:00 |
| assessmentTime | 2026-09-12T00:00:00+00:00 |
| retentionStart | 2026-08-31T00:00:00+00:00 |
| retentionEnd | 2026-10-01T00:00:00+00:00 |
| clockSource | SYNTH-CLOCK-UTC |
| clockUncertaintySeconds | 2 |
| correlationKeys | tenant, application, requestId, eventId |
| requiredFields | synthetic, eventId, actorId, identityClass, eventTime, tenant, application, requestId, authorizationResult |
| gapId | GAP-SF-006 |
| gap | 現在のbindingと生成記録を確定できない |
| allowedConclusion | 同一Flowの合成受領記録が示す段階だけ。Eventや侵害の不存在は判断しない。 |
| alternative | 正常な変更、Collection不備、保持期限切れ、権限不足という別説明を比較する。 |
| confidence | 中 |
| owner | SYNTH-PLATFORM-OWNER |
| reviewDate | 2026-09-20 |
| reassessment | 対象期間、Field、Identity binding、変換版または受領記録の変更時に再評価する。 |
| queryStart | 2026-08-31T23:59:58+00:00 |
| queryEnd | 2026-09-01T00:00:03+00:00 |

### Nodes

| ID | Role |
|---|---|
| N-SF-006-01 | actor |
| N-SF-006-02 | identity |
| N-SF-006-03 | request |
| N-SF-006-04 | gateway |
| N-SF-006-05 | authorization |
| N-SF-006-06 | effect |
| N-SF-006-07 | producer |
| N-SF-006-08 | collector |
| N-SF-006-09 | normalizer |
| N-SF-006-10 | retention |
| N-SF-006-11 | query |
| N-SF-006-12 | consumer |

### Edges

| ID | From | To |
|---|---|---|
| E-SF-006-01 | N-SF-006-01 | N-SF-006-02 |
| E-SF-006-02 | N-SF-006-02 | N-SF-006-03 |
| E-SF-006-03 | N-SF-006-03 | N-SF-006-04 |
| E-SF-006-04 | N-SF-006-04 | N-SF-006-05 |
| E-SF-006-05 | N-SF-006-05 | N-SF-006-06 |
| E-SF-006-06 | N-SF-006-06 | N-SF-006-07 |
| E-SF-006-07 | N-SF-006-07 | N-SF-006-08 |
| E-SF-006-08 | N-SF-006-08 | N-SF-006-09 |
| E-SF-006-09 | N-SF-006-09 | N-SF-006-10 |
| E-SF-006-10 | N-SF-006-10 | N-SF-006-11 |
| E-SF-006-11 | N-SF-006-11 | N-SF-006-12 |

### Evidence receipts

受領記録なし。Unknownのまま扱う。

### Test

Testは未実施。別Flowや親CaseのPassを借用しない。

## Decision / Reassessment / Handoff

SYNTH-PLATFORM-OWNERとSYNTH-SOC-REVIEWERは2026-09-20までに各GAP-SFを見直す。第12〜13章へIdentity bindingとPlane、第16章へEventとField・保持期間、第17章へ有限TestのScope、第20章へClock uncertaintyと変換来歴を渡す。受領票のない範囲を不足として明示することを受入条件とする。

OWNは観測経路と許容結論、BRIDGEは検知・DFIRへのHandoff、DELEGATEはProtocolと基盤の実装である。分析判断の確信度は中、代替説明は正常変更とCollection・保持・権限の不足である。新しい受領票、対象期間、Field、Identity binding、変換版が得られた場合に再評価する。

教材のValidatedは受領票の連続性を再計算した結果だけであり、親Behaviorの発生、実製品の検知率、悪意、主体帰属、侵害不存在の証明ではない。
