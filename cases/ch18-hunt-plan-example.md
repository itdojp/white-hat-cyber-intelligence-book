# 第18章 完全合成記入例：Hunt Plan and Findings

## 対象と読解の境界

`ART-06` / `HUNT-2026-018-001` / `CASE-HUNT-2026-001`は、[第18章](../manuscript/18-threat-hunting.md)の仮説を十二の独立した対比で説明する。親`CASE-DET-2026-001`をrefinesするが、原DVR/DET/TEL/fixtureは変更しない。新対象SYNTH-HUNT18-001 / HUNT18-REV-001は親の現在実装や実Evidenceではない。

[供給JSON](fixtures/ch18-threat-hunting.json)と[閉じたSchema](../schemas/ch18-threat-hunting.schema.json)は完全合成・オフライン読解用である。実Log、実User、実IP、PII、実Tokenを含まず、実SIEMや外部Targetへの接続を要求しない。親HOF-TCM16-18は未配達のままで、実行権限、受領、証拠を付け替えない。

## 判断例の要約

各例は独立した入力であり、一件のIncidentの進行ではない。高・中・低のConfidenceは合成記録内の判断根拠に限る。Supportedを侵害確定にせず、0件を侵害不存在にしない。

| Case | 対比 | Result | 許容結論 |
|---|---|---|---|
| HCASE18-001 | 限定した行動の組 | Supported | 供給承認で説明できない同意変更と30分以内の同じ対象の利用が、この固定入力で組になった。 |
| HCASE18-002 | 承認による弱化 | Weakened | すべての候補変更が供給承認の対象・Window・Scopeで説明され、当初の仮説は弱まった。 |
| HCASE18-003 | 十分な仮定下の0件 | Negative finding | 供給された三Streamの条件を仮定した限定Windowで該当する組を観測しなかった。 |
| HCASE18-004 | IOC一致だけ | Inconclusive | 合成IOCラベルの一致はあるが、行動仮説を検証していないため判断できない。 |
| HCASE18-005 | 生成根拠不足の0件 | Inconclusive | 一致がなくてもconsentの生成根拠が不足し、仮説の反証にはならない。 |
| HCASE18-006 | 保持根拠不足の0件 | Inconclusive | 保持条件が不足するため、観測なしを限定的な反証としても扱わない。 |
| HCASE18-007 | 判断時点より遅い到着 | Inconclusive | 判断時点までに対象Eventがそろっておらず、結論を保留する。 |
| HCASE18-008 | 時刻の不確かさ | Inconclusive | 時刻誤差により固定Windowや順序を確定できず、組の成立を主張しない。 |
| HCASE18-009 | 同一性不一致 | Inconclusive | 同じWorkload文字列でもNamespaceが異なり、同一対象の組と判断しない。 |
| HCASE18-010 | Scope拡大による停止 | Stopped | 有効なScope拡大の停止理由を優先し、行動の評価を続けない。 |
| HCASE18-011 | Ticketだけでは弱化しない | Supported | Ticketは一致してもScope包含が不足するため、説明できない変更と利用の組が残る。 |
| HCASE18-012 | 別対象のNear-miss | Negative finding | 成功した利用が別Workloadなので、指定Population内の該当組は観測していない。 |

## 入力から判断へ辿る

本文T-18-01の固定WindowとPopulationを先に確認する。Case001/002は承認による代替説明、003/005は0件とCoverage不足、004はIOC-only、007/008/009は到着・時刻・同一性、010は停止、011はScope包含、012は別対象Near-missを比較する。

入力はJSONの各contrasts要素のinputにある。Input IDとSUP-HUNT18-*は対象版、Query ID、入力Digestへ対応する。Digestは固定JSON表現の比較であり、真正性や実Collectorの証拠ではない。receiptsのtrue/falseは教材の供給仮定で、実Coverageの測定ではない。原入力の全Event/Receiptを下表へ重複転載せず、供給JSONを参照する。

Query結果と著者判断を分ける。queryResultは有限算法の出力、judgmentは許容結論・代替説明・Gap・担当・再評価である。handoffsはFindingと供給Evidenceを参照する計画であり、すべて未配達、receiptId null、executionAuthorized falseである。実通知、Incident宣言、実行許可にはならない。

## 全欄の読み方

以下はrecord、parents、safety、planと各対比のArtifact欄を、JSONの格納順で一対一に示す。空配列とnullも意味を持つ。inputは上記JSONの専用欄から読む。スラッシュ区切りはField位置であり、ファイルPathや外部アクセス先ではない。

### record

| Field | Value |
|---|---|
| `id` | `HUNT-2026-018-001` |
| `artifactId` | `ART-06` |
| `revision` | `HUNT18-REV-001` |
| `subjectId` | `SYNTH-HUNT18-001` |
| `caseId` | `CASE-HUNT-2026-001` |
| `parentCaseId` | `CASE-DET-2026-001` |
| `relation` | `refines` |
| `asOf` | `2026-09-22T00:00:00Z` |
| `threatId` | `TH-HUNT18-001` |
| `hypothesisId` | `HYP-HUNT18-001` |
| `queryId` | `QRY-HUNT18-001` |
| `pivotId` | `PIV-HUNT18-001` |
| `decision` | `検知見直し、観測条件修正、IR評価依頼を区別する。` |
| `hypothesis` | `供給承認Snapshotで説明できない成功した同意変更と、同じWorkloadの30分以内の成功した利用が組になる。` |
| `baseline` | `供給承認SnapshotのTicket・対象・Window・Scope包含。正常行動分布の学習ではない。` |
| `timeBasis` | `fictional-integer-seconds-not-wall-clock` |
| `actualCollections` | `0` |
| `actualIncidents` | `0` |
| `sourceIds/0` | `SRC-ATTACK-001` |
| `sourceIds/1` | `SRC-ATTACK-DET-001` |
| `sourceIds/2` | `SRC-IR-001` |
| `resultStates/0` | `Supported` |
| `resultStates/1` | `Weakened` |
| `resultStates/2` | `Negative finding` |
| `resultStates/3` | `Inconclusive` |
| `resultStates/4` | `Stopped` |

### parents

| Field | Value |
|---|---|
| `telemetryMapId` | `TCM-2026-016` |
| `telemetryRowIds/0` | `ROW-TCM16-005` |
| `telemetryRowIds/1` | `ROW-TCM16-006` |
| `telemetryRowIds/2` | `ROW-TCM16-007` |
| `handoffId` | `HOF-TCM16-18` |
| `handoffStatus` | `planned-not-delivered` |
| `handoffReceiptId` | `null` |
| `detectionRecordId` | `DVR-2026-017-001` |
| `detectionId` | `DET-2026-017-001` |
| `fixtureSetId` | `FXSET-2026-017` |
| `threatHypothesisId` | `TH-DET-2026-001` |
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
| `owner` | `SYNTH-HUNT-OWNER` |
| `authority` | `owned-reading-copy-not-parent-RoE` |
| `stop` | `Unknown input, actual data, external connection or unclear scope: stop reading and record the gap.` |
| `cleanup` | `整理するのは自分の読解メモだけ。供給Evidenceと正本は変更しない。` |
| `classification` | `public-synthetic-only` |
| `personalDataIncluded` | `false` |
| `productSchemaClaimed` | `false` |

### plan

| Field | Value |
|---|---|
| `subject` | `SYNTH-HUNT18-001` |
| `revision` | `HUNT18-REV-001` |
| `population/0` | `syn-workload-a` |
| `grantStart` | `0` |
| `grantEnd` | `1800` |
| `dataEnd` | `3600` |
| `asOf` | `4000` |
| `pivotSeconds` | `1800` |
| `namespace` | `syn-tenant-a` |
| `normalizer` | `syn-normalizer-1` |

### HCASE18-001

| Field | Value |
|---|---|
| `id` | `HCASE18-001` |
| `title` | `限定した行動の組` |
| `corpusId` | `QCASE18-01` |
| `supplyEvidence/id` | `SUP-HUNT18-001` |
| `supplyEvidence/inputId` | `FIX-HUNT18-001` |
| `supplyEvidence/queryId` | `QRY-HUNT18-001` |
| `supplyEvidence/subject` | `SYNTH-HUNT18-001` |
| `supplyEvidence/revision` | `HUNT18-REV-001` |
| `supplyEvidence/inputDigest` | `b9187a9c767ba4cb59f9e5119eb653ae764d72e189fbc728373e6f595709ca79` |
| `supplyEvidence/meaning` | `supplied-fixture-comparison-not-authenticity` |
| `queryResult/result` | `Supported` |
| `queryResult/gaps` | `[]` |
| `queryResult/evidence/0` | `SYN-EVT-01` |
| `queryResult/evidence/1` | `SYN-EVT-02` |
| `queryResult/pairs/0/0` | `SYN-EVT-01` |
| `queryResult/pairs/0/1` | `SYN-EVT-02` |
| `queryResult/iocHits` | `[]` |
| `queryResult/limit` | `supplied-synthetic-subject-revision-population-window-query-only` |
| `queryResult/alternative` | `incomplete-change-record-or-unmodeled-benign-context` |
| `queryResult/scope/subject` | `SYNTH-HUNT18-001` |
| `queryResult/scope/revision` | `HUNT18-REV-001` |
| `queryResult/scope/population/0` | `syn-workload-a` |
| `queryResult/scope/grantStart` | `0` |
| `queryResult/scope/grantEnd` | `1800` |
| `queryResult/scope/dataEnd` | `3600` |
| `queryResult/scope/asOf` | `4000` |
| `queryResult/scope/pivotSeconds` | `1800` |
| `queryResult/scope/namespace` | `syn-tenant-a` |
| `queryResult/scope/normalizer` | `syn-normalizer-1` |
| `queryResult/owner` | `SYNTH-HUNT-OWNER` |
| `queryResult/reassessment` | `input-revision-window-query-or-coverage-change` |
| `queryResult/handoffs/0/route` | `detection-review` |
| `queryResult/handoffs/0/status` | `planned-not-delivered` |
| `queryResult/handoffs/0/receipt` | `null` |
| `queryResult/handoffs/0/executionAuthorized` | `false` |
| `queryResult/handoffs/1/route` | `incident-triage-review` |
| `queryResult/handoffs/1/status` | `planned-not-delivered` |
| `queryResult/handoffs/1/receipt` | `null` |
| `queryResult/handoffs/1/executionAuthorized` | `false` |
| `judgment/findingId` | `FND-HUNT18-001` |
| `judgment/result` | `Supported` |
| `judgment/permittedConclusion` | `供給承認で説明できない同意変更と30分以内の同じ対象の利用が、この固定入力で組になった。` |
| `judgment/alternative` | `未記録の正当な変更かもしれない。` |
| `judgment/confidence` | `中` |
| `judgment/confidenceBasis` | `Event二件の対応は明確だが、供給Snapshot外の業務文脈はない。` |
| `judgment/gapId` | `GAP-HUNT18-001` |
| `judgment/gap` | `実業務文脈と原記録の真正性は未評価。` |
| `judgment/nextAction` | `Detection見直し候補とIR評価依頼を別々に記録する。` |
| `judgment/owner` | `SYNTH-HUNT-OWNER` |
| `judgment/dueAt` | `2026-09-30T00:00:00Z` |
| `judgment/reassessmentId` | `REA-HUNT18-001` |
| `judgment/reassessment` | `入力版、Query、Scope、Window、Population、Coverage、承認文脈の変更時に再評価する。` |
| `judgment/noCompromiseClaim` | `false` |
| `handoffs/0/id` | `HOF-HUNT18-001-1` |
| `handoffs/0/route` | `detection-review` |
| `handoffs/0/targetChapter` | `17` |
| `handoffs/0/backlogId` | `BKL-HUNT18-001-1` |
| `handoffs/0/sourceFindingId` | `FND-HUNT18-001` |
| `handoffs/0/sourceSupplyId` | `SUP-HUNT18-001` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/0/owner` | `SYNTH-HUNT-OWNER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/acceptance` | `受け手が対象版、問い、許容結論、代替説明、Gapを別途評価する。` |
| `handoffs/0/limitation` | `記録は実通知、受領、Incident宣言、実行権限を意味しない。` |
| `handoffs/1/id` | `HOF-HUNT18-001-2` |
| `handoffs/1/route` | `incident-triage-review` |
| `handoffs/1/targetChapter` | `19` |
| `handoffs/1/backlogId` | `BKL-HUNT18-001-2` |
| `handoffs/1/sourceFindingId` | `FND-HUNT18-001` |
| `handoffs/1/sourceSupplyId` | `SUP-HUNT18-001` |
| `handoffs/1/status` | `planned-not-delivered` |
| `handoffs/1/receiptId` | `null` |
| `handoffs/1/executionAuthorized` | `false` |
| `handoffs/1/owner` | `SYNTH-HUNT-OWNER` |
| `handoffs/1/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/1/acceptance` | `受け手が対象版、問い、許容結論、代替説明、Gapを別途評価する。` |
| `handoffs/1/limitation` | `記録は実通知、受領、Incident宣言、実行権限を意味しない。` |

### HCASE18-002

| Field | Value |
|---|---|
| `id` | `HCASE18-002` |
| `title` | `承認による弱化` |
| `corpusId` | `QCASE18-02` |
| `supplyEvidence/id` | `SUP-HUNT18-002` |
| `supplyEvidence/inputId` | `FIX-HUNT18-002` |
| `supplyEvidence/queryId` | `QRY-HUNT18-001` |
| `supplyEvidence/subject` | `SYNTH-HUNT18-001` |
| `supplyEvidence/revision` | `HUNT18-REV-001` |
| `supplyEvidence/inputDigest` | `2882993b7d498dd982a47a08db71f31b310606d5787817efdcae01a2ab0a1164` |
| `supplyEvidence/meaning` | `supplied-fixture-comparison-not-authenticity` |
| `queryResult/result` | `Weakened` |
| `queryResult/gaps` | `[]` |
| `queryResult/evidence/0` | `SYN-APP-01` |
| `queryResult/evidence/1` | `SYN-EVT-01` |
| `queryResult/pairs` | `[]` |
| `queryResult/iocHits` | `[]` |
| `queryResult/limit` | `supplied-synthetic-subject-revision-population-window-query-only` |
| `queryResult/alternative` | `incomplete-change-record-or-unmodeled-benign-context` |
| `queryResult/scope/subject` | `SYNTH-HUNT18-001` |
| `queryResult/scope/revision` | `HUNT18-REV-001` |
| `queryResult/scope/population/0` | `syn-workload-a` |
| `queryResult/scope/grantStart` | `0` |
| `queryResult/scope/grantEnd` | `1800` |
| `queryResult/scope/dataEnd` | `3600` |
| `queryResult/scope/asOf` | `4000` |
| `queryResult/scope/pivotSeconds` | `1800` |
| `queryResult/scope/namespace` | `syn-tenant-a` |
| `queryResult/scope/normalizer` | `syn-normalizer-1` |
| `queryResult/owner` | `SYNTH-HUNT-OWNER` |
| `queryResult/reassessment` | `input-revision-window-query-or-coverage-change` |
| `queryResult/handoffs/0/route` | `reassessment` |
| `queryResult/handoffs/0/status` | `planned-not-delivered` |
| `queryResult/handoffs/0/receipt` | `null` |
| `queryResult/handoffs/0/executionAuthorized` | `false` |
| `judgment/findingId` | `FND-HUNT18-002` |
| `judgment/result` | `Weakened` |
| `judgment/permittedConclusion` | `すべての候補変更が供給承認の対象・Window・Scopeで説明され、当初の仮説は弱まった。` |
| `judgment/alternative` | `承認Snapshot自体の誤りは本比較で排除できない。` |
| `judgment/confidence` | `中` |
| `judgment/confidenceBasis` | `候補一件と承認一件を照合したが、現実の承認過程は検査していない。` |
| `judgment/gapId` | `GAP-HUNT18-002` |
| `judgment/gap` | `供給外の承認来歴は不明。` |
| `judgment/nextAction` | `入力版や承認条件が変わった時の再評価を記録する。` |
| `judgment/owner` | `SYNTH-HUNT-OWNER` |
| `judgment/dueAt` | `2026-09-30T00:00:00Z` |
| `judgment/reassessmentId` | `REA-HUNT18-002` |
| `judgment/reassessment` | `入力版、Query、Scope、Window、Population、Coverage、承認文脈の変更時に再評価する。` |
| `judgment/noCompromiseClaim` | `false` |
| `handoffs/0/id` | `HOF-HUNT18-002-1` |
| `handoffs/0/route` | `reassessment` |
| `handoffs/0/targetChapter` | `18` |
| `handoffs/0/backlogId` | `BKL-HUNT18-002-1` |
| `handoffs/0/sourceFindingId` | `FND-HUNT18-002` |
| `handoffs/0/sourceSupplyId` | `SUP-HUNT18-002` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/0/owner` | `SYNTH-HUNT-OWNER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/acceptance` | `受け手が対象版、問い、許容結論、代替説明、Gapを別途評価する。` |
| `handoffs/0/limitation` | `記録は実通知、受領、Incident宣言、実行権限を意味しない。` |

### HCASE18-003

| Field | Value |
|---|---|
| `id` | `HCASE18-003` |
| `title` | `十分な仮定下の0件` |
| `corpusId` | `QCASE18-03` |
| `supplyEvidence/id` | `SUP-HUNT18-003` |
| `supplyEvidence/inputId` | `FIX-HUNT18-003` |
| `supplyEvidence/queryId` | `QRY-HUNT18-001` |
| `supplyEvidence/subject` | `SYNTH-HUNT18-001` |
| `supplyEvidence/revision` | `HUNT18-REV-001` |
| `supplyEvidence/inputDigest` | `ae64f39636345f2e95159386acc703080b9155ee4654e4c61686d9d80a6b6e4b` |
| `supplyEvidence/meaning` | `supplied-fixture-comparison-not-authenticity` |
| `queryResult/result` | `Negative finding` |
| `queryResult/gaps` | `[]` |
| `queryResult/evidence` | `[]` |
| `queryResult/pairs` | `[]` |
| `queryResult/iocHits` | `[]` |
| `queryResult/limit` | `supplied-synthetic-subject-revision-population-window-query-only` |
| `queryResult/alternative` | `incomplete-change-record-or-unmodeled-benign-context` |
| `queryResult/scope/subject` | `SYNTH-HUNT18-001` |
| `queryResult/scope/revision` | `HUNT18-REV-001` |
| `queryResult/scope/population/0` | `syn-workload-a` |
| `queryResult/scope/grantStart` | `0` |
| `queryResult/scope/grantEnd` | `1800` |
| `queryResult/scope/dataEnd` | `3600` |
| `queryResult/scope/asOf` | `4000` |
| `queryResult/scope/pivotSeconds` | `1800` |
| `queryResult/scope/namespace` | `syn-tenant-a` |
| `queryResult/scope/normalizer` | `syn-normalizer-1` |
| `queryResult/owner` | `SYNTH-HUNT-OWNER` |
| `queryResult/reassessment` | `input-revision-window-query-or-coverage-change` |
| `queryResult/handoffs/0/route` | `reassessment` |
| `queryResult/handoffs/0/status` | `planned-not-delivered` |
| `queryResult/handoffs/0/receipt` | `null` |
| `queryResult/handoffs/0/executionAuthorized` | `false` |
| `judgment/findingId` | `FND-HUNT18-003` |
| `judgment/result` | `Negative finding` |
| `judgment/permittedConclusion` | `供給された三Streamの条件を仮定した限定Windowで該当する組を観測しなかった。` |
| `judgment/alternative` | `範囲外の期間や別行動は未観測のままである。` |
| `judgment/confidence` | `中` |
| `judgment/confidenceBasis` | `固定Queryと供給Coverageが整合する範囲に限る。` |
| `judgment/gapId` | `GAP-HUNT18-003` |
| `judgment/gap` | `実Coverageと対象外行動は評価していない。` |
| `judgment/nextAction` | `範囲を一般化せず、ScopeやCoverage変更時に再評価する。` |
| `judgment/owner` | `SYNTH-HUNT-OWNER` |
| `judgment/dueAt` | `2026-09-30T00:00:00Z` |
| `judgment/reassessmentId` | `REA-HUNT18-003` |
| `judgment/reassessment` | `入力版、Query、Scope、Window、Population、Coverage、承認文脈の変更時に再評価する。` |
| `judgment/noCompromiseClaim` | `false` |
| `handoffs/0/id` | `HOF-HUNT18-003-1` |
| `handoffs/0/route` | `reassessment` |
| `handoffs/0/targetChapter` | `18` |
| `handoffs/0/backlogId` | `BKL-HUNT18-003-1` |
| `handoffs/0/sourceFindingId` | `FND-HUNT18-003` |
| `handoffs/0/sourceSupplyId` | `SUP-HUNT18-003` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/0/owner` | `SYNTH-HUNT-OWNER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/acceptance` | `受け手が対象版、問い、許容結論、代替説明、Gapを別途評価する。` |
| `handoffs/0/limitation` | `記録は実通知、受領、Incident宣言、実行権限を意味しない。` |

### HCASE18-004

| Field | Value |
|---|---|
| `id` | `HCASE18-004` |
| `title` | `IOC一致だけ` |
| `corpusId` | `QCASE18-04` |
| `supplyEvidence/id` | `SUP-HUNT18-004` |
| `supplyEvidence/inputId` | `FIX-HUNT18-004` |
| `supplyEvidence/queryId` | `QRY-HUNT18-001` |
| `supplyEvidence/subject` | `SYNTH-HUNT18-001` |
| `supplyEvidence/revision` | `HUNT18-REV-001` |
| `supplyEvidence/inputDigest` | `d87e81200abc4abf56a540730792448bdad1e1f9ba142ed0af0df760ffa6cc1e` |
| `supplyEvidence/meaning` | `supplied-fixture-comparison-not-authenticity` |
| `queryResult/result` | `Inconclusive` |
| `queryResult/gaps/0` | `behavior-not-tested` |
| `queryResult/evidence` | `[]` |
| `queryResult/pairs` | `[]` |
| `queryResult/iocHits/0` | `SYN-EVT-01` |
| `queryResult/limit` | `supplied-synthetic-subject-revision-population-window-query-only` |
| `queryResult/alternative` | `incomplete-change-record-or-unmodeled-benign-context` |
| `queryResult/scope/subject` | `SYNTH-HUNT18-001` |
| `queryResult/scope/revision` | `HUNT18-REV-001` |
| `queryResult/scope/population/0` | `syn-workload-a` |
| `queryResult/scope/grantStart` | `0` |
| `queryResult/scope/grantEnd` | `1800` |
| `queryResult/scope/dataEnd` | `3600` |
| `queryResult/scope/asOf` | `4000` |
| `queryResult/scope/pivotSeconds` | `1800` |
| `queryResult/scope/namespace` | `syn-tenant-a` |
| `queryResult/scope/normalizer` | `syn-normalizer-1` |
| `queryResult/owner` | `SYNTH-HUNT-OWNER` |
| `queryResult/reassessment` | `input-revision-window-query-or-coverage-change` |
| `queryResult/handoffs/0/route` | `collection-review` |
| `queryResult/handoffs/0/status` | `planned-not-delivered` |
| `queryResult/handoffs/0/receipt` | `null` |
| `queryResult/handoffs/0/executionAuthorized` | `false` |
| `judgment/findingId` | `FND-HUNT18-004` |
| `judgment/result` | `Inconclusive` |
| `judgment/permittedConclusion` | `合成IOCラベルの一致はあるが、行動仮説を検証していないため判断できない。` |
| `judgment/alternative` | `一致値が正当な利用を指しているかもしれない。` |
| `judgment/confidence` | `低` |
| `judgment/confidenceBasis` | `一致ラベル以外の行動比較を実施していない。` |
| `judgment/gapId` | `GAP-HUNT18-004` |
| `judgment/gap` | `行動仮説の比較が未実施。` |
| `judgment/nextAction` | `同じ供給ScopeでBehavior比較を計画し、実Targetは追加しない。` |
| `judgment/owner` | `SYNTH-HUNT-OWNER` |
| `judgment/dueAt` | `2026-09-30T00:00:00Z` |
| `judgment/reassessmentId` | `REA-HUNT18-004` |
| `judgment/reassessment` | `入力版、Query、Scope、Window、Population、Coverage、承認文脈の変更時に再評価する。` |
| `judgment/noCompromiseClaim` | `false` |
| `handoffs/0/id` | `HOF-HUNT18-004-1` |
| `handoffs/0/route` | `collection-review` |
| `handoffs/0/targetChapter` | `16` |
| `handoffs/0/backlogId` | `BKL-HUNT18-004-1` |
| `handoffs/0/sourceFindingId` | `FND-HUNT18-004` |
| `handoffs/0/sourceSupplyId` | `SUP-HUNT18-004` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/0/owner` | `SYNTH-HUNT-OWNER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/acceptance` | `受け手が対象版、問い、許容結論、代替説明、Gapを別途評価する。` |
| `handoffs/0/limitation` | `記録は実通知、受領、Incident宣言、実行権限を意味しない。` |

### HCASE18-005

| Field | Value |
|---|---|
| `id` | `HCASE18-005` |
| `title` | `生成根拠不足の0件` |
| `corpusId` | `QCASE18-06` |
| `supplyEvidence/id` | `SUP-HUNT18-005` |
| `supplyEvidence/inputId` | `FIX-HUNT18-005` |
| `supplyEvidence/queryId` | `QRY-HUNT18-001` |
| `supplyEvidence/subject` | `SYNTH-HUNT18-001` |
| `supplyEvidence/revision` | `HUNT18-REV-001` |
| `supplyEvidence/inputDigest` | `10c2c73fbda026a933ef6615b152ad8ed06100f4bebf73aa35f00780113b040f` |
| `supplyEvidence/meaning` | `supplied-fixture-comparison-not-authenticity` |
| `queryResult/result` | `Inconclusive` |
| `queryResult/gaps/0` | `consent:producer-gap` |
| `queryResult/evidence` | `[]` |
| `queryResult/pairs` | `[]` |
| `queryResult/iocHits` | `[]` |
| `queryResult/limit` | `supplied-synthetic-subject-revision-population-window-query-only` |
| `queryResult/alternative` | `incomplete-change-record-or-unmodeled-benign-context` |
| `queryResult/scope/subject` | `SYNTH-HUNT18-001` |
| `queryResult/scope/revision` | `HUNT18-REV-001` |
| `queryResult/scope/population/0` | `syn-workload-a` |
| `queryResult/scope/grantStart` | `0` |
| `queryResult/scope/grantEnd` | `1800` |
| `queryResult/scope/dataEnd` | `3600` |
| `queryResult/scope/asOf` | `4000` |
| `queryResult/scope/pivotSeconds` | `1800` |
| `queryResult/scope/namespace` | `syn-tenant-a` |
| `queryResult/scope/normalizer` | `syn-normalizer-1` |
| `queryResult/owner` | `SYNTH-HUNT-OWNER` |
| `queryResult/reassessment` | `input-revision-window-query-or-coverage-change` |
| `queryResult/handoffs/0/route` | `collection-review` |
| `queryResult/handoffs/0/status` | `planned-not-delivered` |
| `queryResult/handoffs/0/receipt` | `null` |
| `queryResult/handoffs/0/executionAuthorized` | `false` |
| `judgment/findingId` | `FND-HUNT18-005` |
| `judgment/result` | `Inconclusive` |
| `judgment/permittedConclusion` | `一致がなくてもconsentの生成根拠が不足し、仮説の反証にはならない。` |
| `judgment/alternative` | `Eventが生成されていないだけかもしれない。` |
| `judgment/confidence` | `低` |
| `judgment/confidenceBasis` | `不足するProducer条件を0件では補えない。` |
| `judgment/gapId` | `GAP-HUNT18-005` |
| `judgment/gap` | `consent:producer-gap。` |
| `judgment/nextAction` | `生成条件を説明する合成入力の再確認候補を記録する。` |
| `judgment/owner` | `SYNTH-HUNT-OWNER` |
| `judgment/dueAt` | `2026-09-30T00:00:00Z` |
| `judgment/reassessmentId` | `REA-HUNT18-005` |
| `judgment/reassessment` | `入力版、Query、Scope、Window、Population、Coverage、承認文脈の変更時に再評価する。` |
| `judgment/noCompromiseClaim` | `false` |
| `handoffs/0/id` | `HOF-HUNT18-005-1` |
| `handoffs/0/route` | `collection-review` |
| `handoffs/0/targetChapter` | `16` |
| `handoffs/0/backlogId` | `BKL-HUNT18-005-1` |
| `handoffs/0/sourceFindingId` | `FND-HUNT18-005` |
| `handoffs/0/sourceSupplyId` | `SUP-HUNT18-005` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/0/owner` | `SYNTH-HUNT-OWNER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/acceptance` | `受け手が対象版、問い、許容結論、代替説明、Gapを別途評価する。` |
| `handoffs/0/limitation` | `記録は実通知、受領、Incident宣言、実行権限を意味しない。` |

### HCASE18-006

| Field | Value |
|---|---|
| `id` | `HCASE18-006` |
| `title` | `保持根拠不足の0件` |
| `corpusId` | `QCASE18-08` |
| `supplyEvidence/id` | `SUP-HUNT18-006` |
| `supplyEvidence/inputId` | `FIX-HUNT18-006` |
| `supplyEvidence/queryId` | `QRY-HUNT18-001` |
| `supplyEvidence/subject` | `SYNTH-HUNT18-001` |
| `supplyEvidence/revision` | `HUNT18-REV-001` |
| `supplyEvidence/inputDigest` | `d4511aa0310172a684394139e2c8ceb5cd6b298c34e8f293118cd4dbc298878d` |
| `supplyEvidence/meaning` | `supplied-fixture-comparison-not-authenticity` |
| `queryResult/result` | `Inconclusive` |
| `queryResult/gaps/0` | `consent:retained-gap` |
| `queryResult/evidence` | `[]` |
| `queryResult/pairs` | `[]` |
| `queryResult/iocHits` | `[]` |
| `queryResult/limit` | `supplied-synthetic-subject-revision-population-window-query-only` |
| `queryResult/alternative` | `incomplete-change-record-or-unmodeled-benign-context` |
| `queryResult/scope/subject` | `SYNTH-HUNT18-001` |
| `queryResult/scope/revision` | `HUNT18-REV-001` |
| `queryResult/scope/population/0` | `syn-workload-a` |
| `queryResult/scope/grantStart` | `0` |
| `queryResult/scope/grantEnd` | `1800` |
| `queryResult/scope/dataEnd` | `3600` |
| `queryResult/scope/asOf` | `4000` |
| `queryResult/scope/pivotSeconds` | `1800` |
| `queryResult/scope/namespace` | `syn-tenant-a` |
| `queryResult/scope/normalizer` | `syn-normalizer-1` |
| `queryResult/owner` | `SYNTH-HUNT-OWNER` |
| `queryResult/reassessment` | `input-revision-window-query-or-coverage-change` |
| `queryResult/handoffs/0/route` | `collection-review` |
| `queryResult/handoffs/0/status` | `planned-not-delivered` |
| `queryResult/handoffs/0/receipt` | `null` |
| `queryResult/handoffs/0/executionAuthorized` | `false` |
| `judgment/findingId` | `FND-HUNT18-006` |
| `judgment/result` | `Inconclusive` |
| `judgment/permittedConclusion` | `保持条件が不足するため、観測なしを限定的な反証としても扱わない。` |
| `judgment/alternative` | `必要な記録が保持範囲から外れた可能性がある。` |
| `judgment/confidence` | `低` |
| `judgment/confidenceBasis` | `比較対象が残っているという仮定を満たさない。` |
| `judgment/gapId` | `GAP-HUNT18-006` |
| `judgment/gap` | `consent:retained-gap。` |
| `judgment/nextAction` | `必要Windowと保持根拠の確認をCollection候補へ渡す。` |
| `judgment/owner` | `SYNTH-HUNT-OWNER` |
| `judgment/dueAt` | `2026-09-30T00:00:00Z` |
| `judgment/reassessmentId` | `REA-HUNT18-006` |
| `judgment/reassessment` | `入力版、Query、Scope、Window、Population、Coverage、承認文脈の変更時に再評価する。` |
| `judgment/noCompromiseClaim` | `false` |
| `handoffs/0/id` | `HOF-HUNT18-006-1` |
| `handoffs/0/route` | `collection-review` |
| `handoffs/0/targetChapter` | `16` |
| `handoffs/0/backlogId` | `BKL-HUNT18-006-1` |
| `handoffs/0/sourceFindingId` | `FND-HUNT18-006` |
| `handoffs/0/sourceSupplyId` | `SUP-HUNT18-006` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/0/owner` | `SYNTH-HUNT-OWNER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/acceptance` | `受け手が対象版、問い、許容結論、代替説明、Gapを別途評価する。` |
| `handoffs/0/limitation` | `記録は実通知、受領、Incident宣言、実行権限を意味しない。` |

### HCASE18-007

| Field | Value |
|---|---|
| `id` | `HCASE18-007` |
| `title` | `判断時点より遅い到着` |
| `corpusId` | `QCASE18-15` |
| `supplyEvidence/id` | `SUP-HUNT18-007` |
| `supplyEvidence/inputId` | `FIX-HUNT18-007` |
| `supplyEvidence/queryId` | `QRY-HUNT18-001` |
| `supplyEvidence/subject` | `SYNTH-HUNT18-001` |
| `supplyEvidence/revision` | `HUNT18-REV-001` |
| `supplyEvidence/inputDigest` | `d7ed700d6d9db6380b2a26c434816dc8b1047413d6aca534007690092efbcd35` |
| `supplyEvidence/meaning` | `supplied-fixture-comparison-not-authenticity` |
| `queryResult/result` | `Inconclusive` |
| `queryResult/gaps/0` | `arrival-incomplete` |
| `queryResult/evidence` | `[]` |
| `queryResult/pairs` | `[]` |
| `queryResult/iocHits` | `[]` |
| `queryResult/limit` | `supplied-synthetic-subject-revision-population-window-query-only` |
| `queryResult/alternative` | `incomplete-change-record-or-unmodeled-benign-context` |
| `queryResult/scope/subject` | `SYNTH-HUNT18-001` |
| `queryResult/scope/revision` | `HUNT18-REV-001` |
| `queryResult/scope/population/0` | `syn-workload-a` |
| `queryResult/scope/grantStart` | `0` |
| `queryResult/scope/grantEnd` | `1800` |
| `queryResult/scope/dataEnd` | `3600` |
| `queryResult/scope/asOf` | `4000` |
| `queryResult/scope/pivotSeconds` | `1800` |
| `queryResult/scope/namespace` | `syn-tenant-a` |
| `queryResult/scope/normalizer` | `syn-normalizer-1` |
| `queryResult/owner` | `SYNTH-HUNT-OWNER` |
| `queryResult/reassessment` | `input-revision-window-query-or-coverage-change` |
| `queryResult/handoffs/0/route` | `collection-review` |
| `queryResult/handoffs/0/status` | `planned-not-delivered` |
| `queryResult/handoffs/0/receipt` | `null` |
| `queryResult/handoffs/0/executionAuthorized` | `false` |
| `judgment/findingId` | `FND-HUNT18-007` |
| `judgment/result` | `Inconclusive` |
| `judgment/permittedConclusion` | `判断時点までに対象Eventがそろっておらず、結論を保留する。` |
| `judgment/alternative` | `単なる到着遅延による欠測かもしれない。` |
| `judgment/confidence` | `低` |
| `judgment/confidenceBasis` | `Event時刻は範囲内でも取り込みがasOfを超える。` |
| `judgment/gapId` | `GAP-HUNT18-007` |
| `judgment/gap` | `arrival-incomplete。` |
| `judgment/nextAction` | `到着条件を更新した新しい入力版で再評価する。` |
| `judgment/owner` | `SYNTH-HUNT-OWNER` |
| `judgment/dueAt` | `2026-09-30T00:00:00Z` |
| `judgment/reassessmentId` | `REA-HUNT18-007` |
| `judgment/reassessment` | `入力版、Query、Scope、Window、Population、Coverage、承認文脈の変更時に再評価する。` |
| `judgment/noCompromiseClaim` | `false` |
| `handoffs/0/id` | `HOF-HUNT18-007-1` |
| `handoffs/0/route` | `collection-review` |
| `handoffs/0/targetChapter` | `16` |
| `handoffs/0/backlogId` | `BKL-HUNT18-007-1` |
| `handoffs/0/sourceFindingId` | `FND-HUNT18-007` |
| `handoffs/0/sourceSupplyId` | `SUP-HUNT18-007` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/0/owner` | `SYNTH-HUNT-OWNER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/acceptance` | `受け手が対象版、問い、許容結論、代替説明、Gapを別途評価する。` |
| `handoffs/0/limitation` | `記録は実通知、受領、Incident宣言、実行権限を意味しない。` |

### HCASE18-008

| Field | Value |
|---|---|
| `id` | `HCASE18-008` |
| `title` | `時刻の不確かさ` |
| `corpusId` | `QCASE18-16` |
| `supplyEvidence/id` | `SUP-HUNT18-008` |
| `supplyEvidence/inputId` | `FIX-HUNT18-008` |
| `supplyEvidence/queryId` | `QRY-HUNT18-001` |
| `supplyEvidence/subject` | `SYNTH-HUNT18-001` |
| `supplyEvidence/revision` | `HUNT18-REV-001` |
| `supplyEvidence/inputDigest` | `823631c047a40621a158a660e8b8a4a120e69273a45431f7dae009c5242eae1c` |
| `supplyEvidence/meaning` | `supplied-fixture-comparison-not-authenticity` |
| `queryResult/result` | `Inconclusive` |
| `queryResult/gaps/0` | `time-uncertainty` |
| `queryResult/evidence` | `[]` |
| `queryResult/pairs` | `[]` |
| `queryResult/iocHits` | `[]` |
| `queryResult/limit` | `supplied-synthetic-subject-revision-population-window-query-only` |
| `queryResult/alternative` | `incomplete-change-record-or-unmodeled-benign-context` |
| `queryResult/scope/subject` | `SYNTH-HUNT18-001` |
| `queryResult/scope/revision` | `HUNT18-REV-001` |
| `queryResult/scope/population/0` | `syn-workload-a` |
| `queryResult/scope/grantStart` | `0` |
| `queryResult/scope/grantEnd` | `1800` |
| `queryResult/scope/dataEnd` | `3600` |
| `queryResult/scope/asOf` | `4000` |
| `queryResult/scope/pivotSeconds` | `1800` |
| `queryResult/scope/namespace` | `syn-tenant-a` |
| `queryResult/scope/normalizer` | `syn-normalizer-1` |
| `queryResult/owner` | `SYNTH-HUNT-OWNER` |
| `queryResult/reassessment` | `input-revision-window-query-or-coverage-change` |
| `queryResult/handoffs/0/route` | `collection-review` |
| `queryResult/handoffs/0/status` | `planned-not-delivered` |
| `queryResult/handoffs/0/receipt` | `null` |
| `queryResult/handoffs/0/executionAuthorized` | `false` |
| `judgment/findingId` | `FND-HUNT18-008` |
| `judgment/result` | `Inconclusive` |
| `judgment/permittedConclusion` | `時刻誤差により固定Windowや順序を確定できず、組の成立を主張しない。` |
| `judgment/alternative` | `見かけの順序が時計誤差で生じた可能性がある。` |
| `judgment/confidence` | `低` |
| `judgment/confidenceBasis` | `時刻品質が本Queryの前提を満たさない。` |
| `judgment/gapId` | `GAP-HUNT18-008` |
| `judgment/gap` | `time-uncertainty。` |
| `judgment/nextAction` | `許容できる時刻根拠を備えた新入力で再評価する。` |
| `judgment/owner` | `SYNTH-HUNT-OWNER` |
| `judgment/dueAt` | `2026-09-30T00:00:00Z` |
| `judgment/reassessmentId` | `REA-HUNT18-008` |
| `judgment/reassessment` | `入力版、Query、Scope、Window、Population、Coverage、承認文脈の変更時に再評価する。` |
| `judgment/noCompromiseClaim` | `false` |
| `handoffs/0/id` | `HOF-HUNT18-008-1` |
| `handoffs/0/route` | `collection-review` |
| `handoffs/0/targetChapter` | `16` |
| `handoffs/0/backlogId` | `BKL-HUNT18-008-1` |
| `handoffs/0/sourceFindingId` | `FND-HUNT18-008` |
| `handoffs/0/sourceSupplyId` | `SUP-HUNT18-008` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/0/owner` | `SYNTH-HUNT-OWNER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/acceptance` | `受け手が対象版、問い、許容結論、代替説明、Gapを別途評価する。` |
| `handoffs/0/limitation` | `記録は実通知、受領、Incident宣言、実行権限を意味しない。` |

### HCASE18-009

| Field | Value |
|---|---|
| `id` | `HCASE18-009` |
| `title` | `同一性不一致` |
| `corpusId` | `QCASE18-17` |
| `supplyEvidence/id` | `SUP-HUNT18-009` |
| `supplyEvidence/inputId` | `FIX-HUNT18-009` |
| `supplyEvidence/queryId` | `QRY-HUNT18-001` |
| `supplyEvidence/subject` | `SYNTH-HUNT18-001` |
| `supplyEvidence/revision` | `HUNT18-REV-001` |
| `supplyEvidence/inputDigest` | `9962b628a36e9b0651db5ce2473d88180cb96099cecab8a92847602b1bd12346` |
| `supplyEvidence/meaning` | `supplied-fixture-comparison-not-authenticity` |
| `queryResult/result` | `Inconclusive` |
| `queryResult/gaps/0` | `identity-unjoinable` |
| `queryResult/evidence` | `[]` |
| `queryResult/pairs` | `[]` |
| `queryResult/iocHits` | `[]` |
| `queryResult/limit` | `supplied-synthetic-subject-revision-population-window-query-only` |
| `queryResult/alternative` | `incomplete-change-record-or-unmodeled-benign-context` |
| `queryResult/scope/subject` | `SYNTH-HUNT18-001` |
| `queryResult/scope/revision` | `HUNT18-REV-001` |
| `queryResult/scope/population/0` | `syn-workload-a` |
| `queryResult/scope/grantStart` | `0` |
| `queryResult/scope/grantEnd` | `1800` |
| `queryResult/scope/dataEnd` | `3600` |
| `queryResult/scope/asOf` | `4000` |
| `queryResult/scope/pivotSeconds` | `1800` |
| `queryResult/scope/namespace` | `syn-tenant-a` |
| `queryResult/scope/normalizer` | `syn-normalizer-1` |
| `queryResult/owner` | `SYNTH-HUNT-OWNER` |
| `queryResult/reassessment` | `input-revision-window-query-or-coverage-change` |
| `queryResult/handoffs/0/route` | `collection-review` |
| `queryResult/handoffs/0/status` | `planned-not-delivered` |
| `queryResult/handoffs/0/receipt` | `null` |
| `queryResult/handoffs/0/executionAuthorized` | `false` |
| `judgment/findingId` | `FND-HUNT18-009` |
| `judgment/result` | `Inconclusive` |
| `judgment/permittedConclusion` | `同じWorkload文字列でもNamespaceが異なり、同一対象の組と判断しない。` |
| `judgment/alternative` | `異なる対象が同じ表示名を使っているかもしれない。` |
| `judgment/confidence` | `低` |
| `judgment/confidenceBasis` | `NamespaceとNormalizerの一致が必要である。` |
| `judgment/gapId` | `GAP-HUNT18-009` |
| `judgment/gap` | `identity-unjoinable。` |
| `judgment/nextAction` | `合成Identity対応の確認をCollection候補へ残す。` |
| `judgment/owner` | `SYNTH-HUNT-OWNER` |
| `judgment/dueAt` | `2026-09-30T00:00:00Z` |
| `judgment/reassessmentId` | `REA-HUNT18-009` |
| `judgment/reassessment` | `入力版、Query、Scope、Window、Population、Coverage、承認文脈の変更時に再評価する。` |
| `judgment/noCompromiseClaim` | `false` |
| `handoffs/0/id` | `HOF-HUNT18-009-1` |
| `handoffs/0/route` | `collection-review` |
| `handoffs/0/targetChapter` | `16` |
| `handoffs/0/backlogId` | `BKL-HUNT18-009-1` |
| `handoffs/0/sourceFindingId` | `FND-HUNT18-009` |
| `handoffs/0/sourceSupplyId` | `SUP-HUNT18-009` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/0/owner` | `SYNTH-HUNT-OWNER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/acceptance` | `受け手が対象版、問い、許容結論、代替説明、Gapを別途評価する。` |
| `handoffs/0/limitation` | `記録は実通知、受領、Incident宣言、実行権限を意味しない。` |

### HCASE18-010

| Field | Value |
|---|---|
| `id` | `HCASE18-010` |
| `title` | `Scope拡大による停止` |
| `corpusId` | `QCASE18-24` |
| `supplyEvidence/id` | `SUP-HUNT18-010` |
| `supplyEvidence/inputId` | `FIX-HUNT18-010` |
| `supplyEvidence/queryId` | `QRY-HUNT18-001` |
| `supplyEvidence/subject` | `SYNTH-HUNT18-001` |
| `supplyEvidence/revision` | `HUNT18-REV-001` |
| `supplyEvidence/inputDigest` | `73ec0cfb970cc2cc5b1a235e28c1930126d94ff96baa4557d7624597f89b7ab9` |
| `supplyEvidence/meaning` | `supplied-fixture-comparison-not-authenticity` |
| `queryResult/result` | `Stopped` |
| `queryResult/gaps/0` | `scope-expansion` |
| `queryResult/evidence` | `[]` |
| `queryResult/pairs` | `[]` |
| `queryResult/iocHits` | `[]` |
| `queryResult/limit` | `supplied-synthetic-subject-revision-population-window-query-only` |
| `queryResult/alternative` | `incomplete-change-record-or-unmodeled-benign-context` |
| `queryResult/scope/subject` | `SYNTH-HUNT18-001` |
| `queryResult/scope/revision` | `HUNT18-REV-001` |
| `queryResult/scope/population/0` | `syn-workload-a` |
| `queryResult/scope/grantStart` | `0` |
| `queryResult/scope/grantEnd` | `1800` |
| `queryResult/scope/dataEnd` | `3600` |
| `queryResult/scope/asOf` | `4000` |
| `queryResult/scope/pivotSeconds` | `1800` |
| `queryResult/scope/namespace` | `syn-tenant-a` |
| `queryResult/scope/normalizer` | `syn-normalizer-1` |
| `queryResult/owner` | `SYNTH-HUNT-OWNER` |
| `queryResult/reassessment` | `input-revision-window-query-or-coverage-change` |
| `queryResult/handoffs/0/route` | `scope-review` |
| `queryResult/handoffs/0/status` | `planned-not-delivered` |
| `queryResult/handoffs/0/receipt` | `null` |
| `queryResult/handoffs/0/executionAuthorized` | `false` |
| `judgment/findingId` | `FND-HUNT18-010` |
| `judgment/result` | `Stopped` |
| `judgment/permittedConclusion` | `有効なScope拡大の停止理由を優先し、行動の評価を続けない。` |
| `judgment/alternative` | `停止していない場合のResultはこの記録の主張ではない。` |
| `judgment/confidence` | `高` |
| `judgment/confidenceBasis` | `指定された停止理由の適用だけは入力から確認できる。` |
| `judgment/gapId` | `GAP-HUNT18-010` |
| `judgment/gap` | `scope-expansion。` |
| `judgment/nextAction` | `Scope確認へ戻し、実権限を追加せず計画を再評価する。` |
| `judgment/owner` | `SYNTH-HUNT-OWNER` |
| `judgment/dueAt` | `2026-09-30T00:00:00Z` |
| `judgment/reassessmentId` | `REA-HUNT18-010` |
| `judgment/reassessment` | `入力版、Query、Scope、Window、Population、Coverage、承認文脈の変更時に再評価する。` |
| `judgment/noCompromiseClaim` | `false` |
| `handoffs/0/id` | `HOF-HUNT18-010-1` |
| `handoffs/0/route` | `scope-review` |
| `handoffs/0/targetChapter` | `18` |
| `handoffs/0/backlogId` | `BKL-HUNT18-010-1` |
| `handoffs/0/sourceFindingId` | `FND-HUNT18-010` |
| `handoffs/0/sourceSupplyId` | `SUP-HUNT18-010` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/0/owner` | `SYNTH-HUNT-OWNER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/acceptance` | `受け手が対象版、問い、許容結論、代替説明、Gapを別途評価する。` |
| `handoffs/0/limitation` | `記録は実通知、受領、Incident宣言、実行権限を意味しない。` |

### HCASE18-011

| Field | Value |
|---|---|
| `id` | `HCASE18-011` |
| `title` | `Ticketだけでは弱化しない` |
| `corpusId` | `QCASE18-27` |
| `supplyEvidence/id` | `SUP-HUNT18-011` |
| `supplyEvidence/inputId` | `FIX-HUNT18-011` |
| `supplyEvidence/queryId` | `QRY-HUNT18-001` |
| `supplyEvidence/subject` | `SYNTH-HUNT18-001` |
| `supplyEvidence/revision` | `HUNT18-REV-001` |
| `supplyEvidence/inputDigest` | `571b656a4ca0a29006da10c31a7d440772492ea95f845706ff9eb39044f3fcbd` |
| `supplyEvidence/meaning` | `supplied-fixture-comparison-not-authenticity` |
| `queryResult/result` | `Supported` |
| `queryResult/gaps` | `[]` |
| `queryResult/evidence/0` | `SYN-EVT-01` |
| `queryResult/evidence/1` | `SYN-EVT-02` |
| `queryResult/pairs/0/0` | `SYN-EVT-01` |
| `queryResult/pairs/0/1` | `SYN-EVT-02` |
| `queryResult/iocHits` | `[]` |
| `queryResult/limit` | `supplied-synthetic-subject-revision-population-window-query-only` |
| `queryResult/alternative` | `incomplete-change-record-or-unmodeled-benign-context` |
| `queryResult/scope/subject` | `SYNTH-HUNT18-001` |
| `queryResult/scope/revision` | `HUNT18-REV-001` |
| `queryResult/scope/population/0` | `syn-workload-a` |
| `queryResult/scope/grantStart` | `0` |
| `queryResult/scope/grantEnd` | `1800` |
| `queryResult/scope/dataEnd` | `3600` |
| `queryResult/scope/asOf` | `4000` |
| `queryResult/scope/pivotSeconds` | `1800` |
| `queryResult/scope/namespace` | `syn-tenant-a` |
| `queryResult/scope/normalizer` | `syn-normalizer-1` |
| `queryResult/owner` | `SYNTH-HUNT-OWNER` |
| `queryResult/reassessment` | `input-revision-window-query-or-coverage-change` |
| `queryResult/handoffs/0/route` | `detection-review` |
| `queryResult/handoffs/0/status` | `planned-not-delivered` |
| `queryResult/handoffs/0/receipt` | `null` |
| `queryResult/handoffs/0/executionAuthorized` | `false` |
| `queryResult/handoffs/1/route` | `incident-triage-review` |
| `queryResult/handoffs/1/status` | `planned-not-delivered` |
| `queryResult/handoffs/1/receipt` | `null` |
| `queryResult/handoffs/1/executionAuthorized` | `false` |
| `judgment/findingId` | `FND-HUNT18-011` |
| `judgment/result` | `Supported` |
| `judgment/permittedConclusion` | `Ticketは一致してもScope包含が不足するため、説明できない変更と利用の組が残る。` |
| `judgment/alternative` | `未記録の追加承認があるかもしれない。` |
| `judgment/confidence` | `中` |
| `judgment/confidenceBasis` | `TicketだけでなくScope集合を比較している。` |
| `judgment/gapId` | `GAP-HUNT18-011` |
| `judgment/gap` | `供給Snapshot以外の承認は不明。` |
| `judgment/nextAction` | `不足する承認文脈を明示して検知候補と評価依頼を分ける。` |
| `judgment/owner` | `SYNTH-HUNT-OWNER` |
| `judgment/dueAt` | `2026-09-30T00:00:00Z` |
| `judgment/reassessmentId` | `REA-HUNT18-011` |
| `judgment/reassessment` | `入力版、Query、Scope、Window、Population、Coverage、承認文脈の変更時に再評価する。` |
| `judgment/noCompromiseClaim` | `false` |
| `handoffs/0/id` | `HOF-HUNT18-011-1` |
| `handoffs/0/route` | `detection-review` |
| `handoffs/0/targetChapter` | `17` |
| `handoffs/0/backlogId` | `BKL-HUNT18-011-1` |
| `handoffs/0/sourceFindingId` | `FND-HUNT18-011` |
| `handoffs/0/sourceSupplyId` | `SUP-HUNT18-011` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/0/owner` | `SYNTH-HUNT-OWNER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/acceptance` | `受け手が対象版、問い、許容結論、代替説明、Gapを別途評価する。` |
| `handoffs/0/limitation` | `記録は実通知、受領、Incident宣言、実行権限を意味しない。` |
| `handoffs/1/id` | `HOF-HUNT18-011-2` |
| `handoffs/1/route` | `incident-triage-review` |
| `handoffs/1/targetChapter` | `19` |
| `handoffs/1/backlogId` | `BKL-HUNT18-011-2` |
| `handoffs/1/sourceFindingId` | `FND-HUNT18-011` |
| `handoffs/1/sourceSupplyId` | `SUP-HUNT18-011` |
| `handoffs/1/status` | `planned-not-delivered` |
| `handoffs/1/receiptId` | `null` |
| `handoffs/1/executionAuthorized` | `false` |
| `handoffs/1/owner` | `SYNTH-HUNT-OWNER` |
| `handoffs/1/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/1/acceptance` | `受け手が対象版、問い、許容結論、代替説明、Gapを別途評価する。` |
| `handoffs/1/limitation` | `記録は実通知、受領、Incident宣言、実行権限を意味しない。` |

### HCASE18-012

| Field | Value |
|---|---|
| `id` | `HCASE18-012` |
| `title` | `別対象のNear-miss` |
| `corpusId` | `QCASE18-19` |
| `supplyEvidence/id` | `SUP-HUNT18-012` |
| `supplyEvidence/inputId` | `FIX-HUNT18-012` |
| `supplyEvidence/queryId` | `QRY-HUNT18-001` |
| `supplyEvidence/subject` | `SYNTH-HUNT18-001` |
| `supplyEvidence/revision` | `HUNT18-REV-001` |
| `supplyEvidence/inputDigest` | `c1a1034855568e5202ca0c39c10db7d984a830aaa7900f808fed2a182d9d9311` |
| `supplyEvidence/meaning` | `supplied-fixture-comparison-not-authenticity` |
| `queryResult/result` | `Negative finding` |
| `queryResult/gaps` | `[]` |
| `queryResult/evidence` | `[]` |
| `queryResult/pairs` | `[]` |
| `queryResult/iocHits` | `[]` |
| `queryResult/limit` | `supplied-synthetic-subject-revision-population-window-query-only` |
| `queryResult/alternative` | `incomplete-change-record-or-unmodeled-benign-context` |
| `queryResult/scope/subject` | `SYNTH-HUNT18-001` |
| `queryResult/scope/revision` | `HUNT18-REV-001` |
| `queryResult/scope/population/0` | `syn-workload-a` |
| `queryResult/scope/grantStart` | `0` |
| `queryResult/scope/grantEnd` | `1800` |
| `queryResult/scope/dataEnd` | `3600` |
| `queryResult/scope/asOf` | `4000` |
| `queryResult/scope/pivotSeconds` | `1800` |
| `queryResult/scope/namespace` | `syn-tenant-a` |
| `queryResult/scope/normalizer` | `syn-normalizer-1` |
| `queryResult/owner` | `SYNTH-HUNT-OWNER` |
| `queryResult/reassessment` | `input-revision-window-query-or-coverage-change` |
| `queryResult/handoffs/0/route` | `reassessment` |
| `queryResult/handoffs/0/status` | `planned-not-delivered` |
| `queryResult/handoffs/0/receipt` | `null` |
| `queryResult/handoffs/0/executionAuthorized` | `false` |
| `judgment/findingId` | `FND-HUNT18-012` |
| `judgment/result` | `Negative finding` |
| `judgment/permittedConclusion` | `成功した利用が別Workloadなので、指定Population内の該当組は観測していない。` |
| `judgment/alternative` | `別Workloadの活動は本仮説の反証にも支持にも使わない。` |
| `judgment/confidence` | `中` |
| `judgment/confidenceBasis` | `対象固定の結合条件に限った比較である。` |
| `judgment/gapId` | `GAP-HUNT18-012` |
| `judgment/gap` | `範囲外の対象は未評価。` |
| `judgment/nextAction` | `Populationを無断で広げず、条件変更時の再評価を残す。` |
| `judgment/owner` | `SYNTH-HUNT-OWNER` |
| `judgment/dueAt` | `2026-09-30T00:00:00Z` |
| `judgment/reassessmentId` | `REA-HUNT18-012` |
| `judgment/reassessment` | `入力版、Query、Scope、Window、Population、Coverage、承認文脈の変更時に再評価する。` |
| `judgment/noCompromiseClaim` | `false` |
| `handoffs/0/id` | `HOF-HUNT18-012-1` |
| `handoffs/0/route` | `reassessment` |
| `handoffs/0/targetChapter` | `18` |
| `handoffs/0/backlogId` | `BKL-HUNT18-012-1` |
| `handoffs/0/sourceFindingId` | `FND-HUNT18-012` |
| `handoffs/0/sourceSupplyId` | `SUP-HUNT18-012` |
| `handoffs/0/status` | `planned-not-delivered` |
| `handoffs/0/receiptId` | `null` |
| `handoffs/0/executionAuthorized` | `false` |
| `handoffs/0/owner` | `SYNTH-HUNT-OWNER` |
| `handoffs/0/dueAt` | `2026-09-30T00:00:00Z` |
| `handoffs/0/acceptance` | `受け手が対象版、問い、許容結論、代替説明、Gapを別途評価する。` |
| `handoffs/0/limitation` | `記録は実通知、受領、Incident宣言、実行権限を意味しない。` |

## 読解後の確認

入力ID→Query ID→Supply Evidence→Finding→Gap→未配達Handoff→Reassessmentを一行ずつ辿る。Rootlessな製品実行やRuntime起動すら不要で、読解だけでよい。未知入力、実データ、外部接続要求、Scope不明では停止し、追加取得しない。整理するのは自分のメモだけであり、供給Evidenceや正本を変更しない。

[空のART-06](../templates/hunt-report.md)へ戻り、自分の許容結論と再評価条件を記す。Sourceの採用範囲は[第18章Source Review](../references/ch18-source-review-2026-09-22.md)を参照する。
