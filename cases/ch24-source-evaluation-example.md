# 第24章 完全合成例：Evidence and Source Evaluation Table

`ART-30` / `EST-2026-024-001` / `CASE-OS24-001`の独立した供給記録です。[第24章](../manuscript/24-osint-provenance-sources.md)、[Template](../templates/evidence-source-evaluation-table.md)、[JSON](fixtures/ch24-source-evaluation.json)、[Schema](../schemas/ch24-source-evaluation.schema.json)を照合します。

## 読み方と境界

Purposeは供給資料の来歴と個別Claimの用途を読むこと、Prerequisiteは本書の完全合成教材、Authority / Scopeは記入とオフライン読解だけです。Expected evidenceは原典/変換/評価/Gapの対応、Impactは教材内だけです。未知Data、個人情報、Termsや原典不明、Hash不一致、通信要求ならStopします。Cleanupは自分の演習Copyを確認して終了後24時間以内に除去するだけで、正本と他者Dataを消去しません。実収集・実操作・実通知・外部通信は0、executionAuthorized=falseです。

第10/23/25章はmethod-reference-onlyです。親のEvidence/対象/権限や未配達Handoffを継承しません。2026-10-04〜05の供給日時は未来の実施予定ではなく著者の仮定です。実人物や実Dataで置換しません。

## 原典と主張の対応

五Source、九Item、五Transform、四Claim、十Evaluationです。Vendorの旧v1と訂正v2は同じAdvisoryを別Itemで保持します。BlogとNewsの掲載先は異なっても原典v1は同じです。内容の変換履歴自体はv1→Blog→Newsです。相互引用は取得済みItemの本文ではなく、別の著者供給イベントとして記録します。ITEM-EV24-003は00:20、004は00:35取得のまま保持し、Resource003→004のリンク追加は00:40/記録00:45、逆向きは00:50/記録00:55です（同日UTC）。contextItemIdsはそれ以前の取得物を文脈として参照するだけで、当時の内容に後のリンクがあったとは主張しません。イベントは新しいClaim観測でも実収集の記録でもありません。

現行v2のBatch条件では「可能性がある」までです。供給Labのinteractive二十件で遅延零件という観測は、全sessionで実際に遅延したという全称Claimには反しますが、Batch条件の可能性を反証しません。Postの発行役割を記入したことと、そのClaimを検証したことは別です。

作業訳は原語のmodalityを保ち、元の観測groupへ戻します。意図的な誤AI要約は全称・確定へ強まるためExcluded、Review未完の抽出はLeadです。Hash一致で内容の真実性を認定しません。Source reliabilityと個別credibilityの値は著者の教材設定で、単一Scoreではありません。

## 期待する限定結果

| 項目 | 独立した期待値 | 限界 |
|---|---|---|
| Direct evidence | 四評価 | Vendorと訳は同じgroupで重複する |
| Context | 三評価 | 旧版とその派生を現行根拠へ足さない |
| Lead / Unverified / Excluded | 各一評価 | 不足、未検証、誤変換を隠さない |
| CLM-EV24-002の支持 | OBS-EV24-001一group | Batchの可能性だけ |
| CLM-EV24-003の支持 | OBS-EV24-003一group | 供給二十件内だけ |
| CLM-EV24-004の矛盾 | OBS-EV24-003一group | 同じLab観測を別groupへ数えない |
| 現行判断に用いる観測group総数 | 二 | 件数からConfidenceを自動算出しない |
| 引用循環のedge | 二 | 新観測の追加は零 |
| 実収集 / 配達済みHandoff | 零 / 零 | 予定と実施を区別する |

以下はJSONの全leafを表示します。空欄を推測で埋めるための省略表ではありません。任意の自然言語の真偽、PII完全検出、法的適格性をCheckerが認定するという意味でもありません。

## 全欄の読み方

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
| `id` | `EST-2026-024-001` |
| `artifactId` | `ART-30` |
| `caseId` | `CASE-OS24-001` |
| `relationship` | `independent` |
| `decisionId` | `DR-OS24-001` |
| `decisionOwner` | `SYNTH-DECISION-OWNER` |
| `question` | `供給資料の通知遅延の説明をどの版と条件に限定して判断へ渡せるか。` |
| `asOf` | `2026-10-04T03:00:00Z` |
| `decisionDeadline` | `2026-10-05T03:00:00Z` |
| `actualCollections` | `0` |
| `actualActions` | `0` |
| `actualNotifications` | `0` |
| `parentEvidenceInherited` | `false` |
| `parentAuthorityInherited` | `false` |
| `realWorldTruthCertified` | `false` |
| `retention` | `own working copies within 24 hours after exercise` |
| `custodian` | `SYNTH-CUSTODIAN` |

### REF-EV24-010

| Field | Value |
|---|---|
| `id` | `REF-EV24-010` |
| `chapter` | `10` |
| `recordId` | `ASR-2026-010` |
| `relationship` | `method-reference-only` |
| `received` | `false` |

### REF-EV24-023

| Field | Value |
|---|---|
| `id` | `REF-EV24-023` |
| `chapter` | `23` |
| `recordId` | `IRCP-2026-023-001` |
| `relationship` | `method-reference-only` |
| `received` | `false` |

### REF-EV24-025

| Field | Value |
|---|---|
| `id` | `REF-EV24-025` |
| `chapter` | `25` |
| `recordId` | `ART-12` |
| `relationship` | `method-reference-only` |
| `received` | `false` |

### COL-EV24-001

| Field | Value |
|---|---|
| `id` | `COL-EV24-001` |
| `question` | `訂正版の範囲と供給観測を比較する。` |
| `subject` | `SYNTH-NOTIFY` |
| `currentVersion` | `v2` |
| `owner` | `SYNTH-COLLECTION-OWNER` |
| `deadline` | `2026-10-04T03:00:00Z` |
| `authority` | `supplied-only` |
| `terms` | `supplied-only` |
| `classification` | `synthetic-public` |
| `method` | `supplied-record-reading` |
| `stop` | `未知入力、Terms不明、個人情報、Hash不一致なら追加処理を止める。` |

### COL-EV24-002

| Field | Value |
|---|---|
| `id` | `COL-EV24-002` |
| `question` | `旧版と引用・訂正の来歴を分離する。` |
| `subject` | `SYNTH-NOTIFY` |
| `currentVersion` | `v2` |
| `owner` | `SYNTH-COLLECTION-OWNER` |
| `deadline` | `2026-10-04T03:00:00Z` |
| `authority` | `supplied-only` |
| `terms` | `supplied-only` |
| `classification` | `synthetic-public` |
| `method` | `supplied-record-reading` |
| `stop` | `未知入力、Terms不明、個人情報、Hash不一致なら追加処理を止める。` |

### OSRC-EV24-001

| Field | Value |
|---|---|
| `id` | `OSRC-EV24-001` |
| `publisher` | `SYNTH-VENDOR` |
| `author` | `SYNTH-VENDOR-EDITOR` |
| `kind` | `original` |
| `reliability/value` | `bounded` |
| `reliability/reason` | `教材内の発行系列と訂正を供給。実発行者の認証ではない。` |
| `authority` | `supplied-only` |
| `terms` | `supplied-only` |
| `classification` | `synthetic-public` |
| `allowedUse` | `offline-reading-only` |

### OSRC-EV24-002

| Field | Value |
|---|---|
| `id` | `OSRC-EV24-002` |
| `publisher` | `SYNTH-BLOG` |
| `author` | `SYNTH-BLOG-EDITOR` |
| `kind` | `secondary` |
| `reliability/value` | `limited` |
| `reliability/reason` | `Advisoryの引用だけで独立観測なし。` |
| `authority` | `supplied-only` |
| `terms` | `supplied-only` |
| `classification` | `synthetic-public` |
| `allowedUse` | `offline-reading-only` |

### OSRC-EV24-003

| Field | Value |
|---|---|
| `id` | `OSRC-EV24-003` |
| `publisher` | `SYNTH-NEWS` |
| `author` | `SYNTH-NEWS-EDITOR` |
| `kind` | `aggregator` |
| `reliability/value` | `limited` |
| `reliability/reason` | `Blogの再掲で独立観測なし。` |
| `authority` | `supplied-only` |
| `terms` | `supplied-only` |
| `classification` | `synthetic-public` |
| `allowedUse` | `offline-reading-only` |

### OSRC-EV24-004

| Field | Value |
|---|---|
| `id` | `OSRC-EV24-004` |
| `publisher` | `SYNTH-POST` |
| `author` | `SYNTH-POST-EDITOR` |
| `kind` | `post` |
| `reliability/value` | `unknown` |
| `reliability/reason` | `供給された投稿役割だけが既知で、内容の検証履歴なし。` |
| `authority` | `supplied-only` |
| `terms` | `supplied-only` |
| `classification` | `synthetic-public` |
| `allowedUse` | `offline-reading-only` |

### OSRC-EV24-005

| Field | Value |
|---|---|
| `id` | `OSRC-EV24-005` |
| `publisher` | `SYNTH-LAB` |
| `author` | `SYNTH-LAB-EDITOR` |
| `kind` | `observation` |
| `reliability/value` | `bounded` |
| `reliability/reason` | `二十件の供給観測だけ。実測や完全性を認定しない。` |
| `authority` | `supplied-only` |
| `terms` | `supplied-only` |
| `classification` | `synthetic-public` |
| `allowedUse` | `offline-reading-only` |

### CLM-EV24-001

| Field | Value |
|---|---|
| `id` | `CLM-EV24-001` |
| `collectionId` | `COL-EV24-002` |
| `subject` | `SYNTH-NOTIFY` |
| `version` | `v1` |
| `scope` | `unspecified-load` |
| `text` | `通知遅延が発生する可能性があるという初期説明。` |
| `modality` | `possible` |
| `hypothesisIds/0` | `HYP-EV24-001` |
| `hypothesisIds/1` | `HYP-EV24-002` |

### CLM-EV24-002

| Field | Value |
|---|---|
| `id` | `CLM-EV24-002` |
| `collectionId` | `COL-EV24-001` |
| `subject` | `SYNTH-NOTIFY` |
| `version` | `v2` |
| `scope` | `batch-load` |
| `text` | `Batch条件で通知遅延が発生する可能性がある。` |
| `modality` | `possible` |
| `hypothesisIds/0` | `HYP-EV24-001` |
| `hypothesisIds/1` | `HYP-EV24-002` |

### CLM-EV24-003

| Field | Value |
|---|---|
| `id` | `CLM-EV24-003` |
| `collectionId` | `COL-EV24-001` |
| `subject` | `SYNTH-NOTIFY` |
| `version` | `v2` |
| `scope` | `interactive-20-sample` |
| `text` | `供給されたinteractive二十件では通知遅延が零件。` |
| `modality` | `observed` |
| `hypothesisIds/0` | `HYP-EV24-001` |
| `hypothesisIds/1` | `HYP-EV24-002` |

### CLM-EV24-004

| Field | Value |
|---|---|
| `id` | `CLM-EV24-004` |
| `collectionId` | `COL-EV24-001` |
| `subject` | `SYNTH-NOTIFY` |
| `version` | `v2` |
| `scope` | `all-sessions` |
| `text` | `すべてのsessionで実際に通知遅延が発生したという未検証主張。` |
| `modality` | `confirmed` |
| `hypothesisIds/0` | `HYP-EV24-001` |
| `hypothesisIds/1` | `HYP-EV24-002` |

### ITEM-EV24-001

| Field | Value |
|---|---|
| `id` | `ITEM-EV24-001` |
| `sourceId` | `OSRC-EV24-001` |
| `resourceId` | `advisory` |
| `subject` | `SYNTH-NOTIFY` |
| `version` | `v1` |
| `originKind` | `original` |
| `observationGroup` | `OBS-EV24-001` |
| `parentItemId` | `null` |
| `canonicalUrl` | `https://source-1.example/advisory` |
| `acquiredUrl` | `https://source-1.example/advisory` |
| `publishedAt` | `2026-10-04T00:00:00Z` |
| `acquiredAt` | `2026-10-04T00:05:00Z` |
| `timezone` | `UTC` |
| `acquisitionMethod` | `author-supplied-not-network-acquisition` |
| `archiveRef` | `ARCH-EV24-001` |
| `mediaType` | `text/plain; charset=utf-8` |
| `language` | `en` |
| `content` | `SYNTH advisory v1: Notification delivery may be delayed. Scope is preliminary.` |
| `contentSha256` | `c69a9e4562b636598193d4f00a423b1055e7cff60e93c59914deddd764d95360` |
| `assertions/0/claimId` | `CLM-EV24-001` |
| `assertions/0/relation` | `supports` |
| `assertions/0/modality` | `possible` |

### ITEM-EV24-002

| Field | Value |
|---|---|
| `id` | `ITEM-EV24-002` |
| `sourceId` | `OSRC-EV24-001` |
| `resourceId` | `advisory` |
| `subject` | `SYNTH-NOTIFY` |
| `version` | `v2` |
| `originKind` | `original` |
| `observationGroup` | `OBS-EV24-001` |
| `parentItemId` | `null` |
| `canonicalUrl` | `https://source-1.example/advisory` |
| `acquiredUrl` | `https://source-1.example/advisory` |
| `publishedAt` | `2026-10-04T01:00:00Z` |
| `acquiredAt` | `2026-10-04T01:05:00Z` |
| `timezone` | `UTC` |
| `acquisitionMethod` | `author-supplied-not-network-acquisition` |
| `archiveRef` | `ARCH-EV24-002` |
| `mediaType` | `text/plain; charset=utf-8` |
| `language` | `en` |
| `content` | `SYNTH advisory v2: Notification delivery may be delayed under batch load. Interactive workload is not established by this advisory.` |
| `contentSha256` | `432658d93cdae4d8c50117d72aa0f38e8915da49d1736632aa61f603bc6c0bab` |
| `assertions/0/claimId` | `CLM-EV24-002` |
| `assertions/0/relation` | `supports` |
| `assertions/0/modality` | `possible` |

### ITEM-EV24-003

| Field | Value |
|---|---|
| `id` | `ITEM-EV24-003` |
| `sourceId` | `OSRC-EV24-002` |
| `resourceId` | `RESOURCE-EV24-003` |
| `subject` | `SYNTH-NOTIFY` |
| `version` | `v1` |
| `originKind` | `derived` |
| `observationGroup` | `OBS-EV24-001` |
| `parentItemId` | `ITEM-EV24-001` |
| `canonicalUrl` | `https://source-2.example/item-3` |
| `acquiredUrl` | `https://source-2.example/item-3` |
| `publishedAt` | `2026-10-04T00:15:00Z` |
| `acquiredAt` | `2026-10-04T00:20:00Z` |
| `timezone` | `UTC` |
| `acquisitionMethod` | `author-supplied-not-network-acquisition` |
| `archiveRef` | `ARCH-EV24-003` |
| `mediaType` | `text/plain; charset=utf-8` |
| `language` | `en` |
| `content` | `SYNTH blog cites advisory v1: Notification delivery may be delayed.` |
| `contentSha256` | `f7261233a7f2c2efc76cc880a13617e0aa9e1c47efb5ad8fe5553a62e6f3b499` |
| `assertions/0/claimId` | `CLM-EV24-001` |
| `assertions/0/relation` | `supports` |
| `assertions/0/modality` | `possible` |

### ITEM-EV24-004

| Field | Value |
|---|---|
| `id` | `ITEM-EV24-004` |
| `sourceId` | `OSRC-EV24-003` |
| `resourceId` | `RESOURCE-EV24-004` |
| `subject` | `SYNTH-NOTIFY` |
| `version` | `v1` |
| `originKind` | `derived` |
| `observationGroup` | `OBS-EV24-001` |
| `parentItemId` | `ITEM-EV24-003` |
| `canonicalUrl` | `https://source-3.example/item-4` |
| `acquiredUrl` | `https://source-3.example/item-4` |
| `publishedAt` | `2026-10-04T00:30:00Z` |
| `acquiredAt` | `2026-10-04T00:35:00Z` |
| `timezone` | `UTC` |
| `acquisitionMethod` | `author-supplied-not-network-acquisition` |
| `archiveRef` | `ARCH-EV24-004` |
| `mediaType` | `text/plain; charset=utf-8` |
| `language` | `en` |
| `content` | `SYNTH news republishes the SYNTH blog statement about advisory v1.` |
| `contentSha256` | `c44bf3da1ad023769f1401b28b590ecd34b184854f05f7c92cd15232dbeeb3da` |
| `assertions/0/claimId` | `CLM-EV24-001` |
| `assertions/0/relation` | `supports` |
| `assertions/0/modality` | `possible` |

### ITEM-EV24-005

| Field | Value |
|---|---|
| `id` | `ITEM-EV24-005` |
| `sourceId` | `OSRC-EV24-004` |
| `resourceId` | `RESOURCE-EV24-005` |
| `subject` | `SYNTH-NOTIFY` |
| `version` | `v2` |
| `originKind` | `original` |
| `observationGroup` | `OBS-EV24-002` |
| `parentItemId` | `null` |
| `canonicalUrl` | `https://source-4.example/item-5` |
| `acquiredUrl` | `https://source-4.example/item-5` |
| `publishedAt` | `2026-10-04T01:15:00Z` |
| `acquiredAt` | `2026-10-04T01:20:00Z` |
| `timezone` | `UTC` |
| `acquisitionMethod` | `author-supplied-not-network-acquisition` |
| `archiveRef` | `ARCH-EV24-005` |
| `mediaType` | `text/plain; charset=utf-8` |
| `language` | `en` |
| `content` | `SYNTH unverified post claims all sessions experienced notification delays. No supporting observations are supplied.` |
| `contentSha256` | `2f32d54ece0d1d106fe917c811c44f01f97c4c2e694061bd85a500d5adf404bc` |
| `assertions/0/claimId` | `CLM-EV24-004` |
| `assertions/0/relation` | `supports` |
| `assertions/0/modality` | `confirmed` |

### ITEM-EV24-006

| Field | Value |
|---|---|
| `id` | `ITEM-EV24-006` |
| `sourceId` | `OSRC-EV24-005` |
| `resourceId` | `RESOURCE-EV24-006` |
| `subject` | `SYNTH-NOTIFY` |
| `version` | `v2` |
| `originKind` | `original` |
| `observationGroup` | `OBS-EV24-003` |
| `parentItemId` | `null` |
| `canonicalUrl` | `https://source-5.example/item-6` |
| `acquiredUrl` | `https://source-5.example/item-6` |
| `publishedAt` | `2026-10-04T01:30:00Z` |
| `acquiredAt` | `2026-10-04T01:35:00Z` |
| `timezone` | `UTC` |
| `acquisitionMethod` | `author-supplied-not-network-acquisition` |
| `archiveRef` | `ARCH-EV24-006` |
| `mediaType` | `text/plain; charset=utf-8` |
| `language` | `en` |
| `content` | `SYNTH supplied observation: 0 delayed notifications in 20 interactive sessions. No observation of batch workload is supplied.` |
| `contentSha256` | `42bd1d32a8646267ac2543d7cbe9bde26af54f61cb23a68b2d3ebb0cf3b092e9` |
| `assertions/0/claimId` | `CLM-EV24-003` |
| `assertions/0/relation` | `supports` |
| `assertions/0/modality` | `observed` |
| `assertions/1/claimId` | `CLM-EV24-004` |
| `assertions/1/relation` | `contradicts` |
| `assertions/1/modality` | `observed` |

### ITEM-EV24-007

| Field | Value |
|---|---|
| `id` | `ITEM-EV24-007` |
| `sourceId` | `OSRC-EV24-001` |
| `resourceId` | `RESOURCE-EV24-007` |
| `subject` | `SYNTH-NOTIFY` |
| `version` | `v2` |
| `originKind` | `derived` |
| `observationGroup` | `OBS-EV24-001` |
| `parentItemId` | `ITEM-EV24-002` |
| `canonicalUrl` | `https://source-1.example/item-7` |
| `acquiredUrl` | `https://source-1.example/item-7` |
| `publishedAt` | `2026-10-04T01:40:00Z` |
| `acquiredAt` | `2026-10-04T01:45:00Z` |
| `timezone` | `UTC` |
| `acquisitionMethod` | `author-supplied-not-network-acquisition` |
| `archiveRef` | `ARCH-EV24-007` |
| `mediaType` | `text/plain; charset=utf-8` |
| `language` | `ja` |
| `content` | `合成Advisory v2の作業訳: Batch条件で通知遅延が発生する可能性がある。interactiveについて、このAdvisoryでは確認していない。` |
| `contentSha256` | `e161581e00ee9e9cdbd90431e5964fb6f72490a89842c1134a509d2fd2243a62` |
| `assertions/0/claimId` | `CLM-EV24-002` |
| `assertions/0/relation` | `supports` |
| `assertions/0/modality` | `possible` |

### ITEM-EV24-008

| Field | Value |
|---|---|
| `id` | `ITEM-EV24-008` |
| `sourceId` | `OSRC-EV24-001` |
| `resourceId` | `RESOURCE-EV24-008` |
| `subject` | `SYNTH-NOTIFY` |
| `version` | `v2` |
| `originKind` | `derived` |
| `observationGroup` | `OBS-EV24-001` |
| `parentItemId` | `ITEM-EV24-002` |
| `canonicalUrl` | `https://source-1.example/item-8` |
| `acquiredUrl` | `https://source-1.example/item-8` |
| `publishedAt` | `2026-10-04T01:50:00Z` |
| `acquiredAt` | `2026-10-04T01:55:00Z` |
| `timezone` | `UTC` |
| `acquisitionMethod` | `author-supplied-not-network-acquisition` |
| `archiveRef` | `ARCH-EV24-008` |
| `mediaType` | `text/plain; charset=utf-8` |
| `language` | `en` |
| `content` | `SYNTH intentionally incorrect AI summary: all sessions experienced notification delays.` |
| `contentSha256` | `1a3c2c08a4947a4072a1c4889c36b759b8a76d07bc9e499d100ba3e5f7bc3610` |
| `assertions/0/claimId` | `CLM-EV24-004` |
| `assertions/0/relation` | `supports` |
| `assertions/0/modality` | `confirmed` |

### ITEM-EV24-009

| Field | Value |
|---|---|
| `id` | `ITEM-EV24-009` |
| `sourceId` | `OSRC-EV24-005` |
| `resourceId` | `RESOURCE-EV24-009` |
| `subject` | `SYNTH-NOTIFY` |
| `version` | `v2` |
| `originKind` | `derived` |
| `observationGroup` | `OBS-EV24-003` |
| `parentItemId` | `ITEM-EV24-006` |
| `canonicalUrl` | `https://source-5.example/item-9` |
| `acquiredUrl` | `https://source-5.example/item-9` |
| `publishedAt` | `2026-10-04T02:00:00Z` |
| `acquiredAt` | `2026-10-04T02:05:00Z` |
| `timezone` | `UTC` |
| `acquisitionMethod` | `author-supplied-not-network-acquisition` |
| `archiveRef` | `ARCH-EV24-009` |
| `mediaType` | `text/plain; charset=utf-8` |
| `language` | `en` |
| `content` | `SYNTH working extraction, review pending: 0 delayed notifications in 20 supplied interactive sessions.` |
| `contentSha256` | `7f7b276db5cdca039d60b50125955c8612e775d75621b8e1c33c74b81ef549f4` |
| `assertions/0/claimId` | `CLM-EV24-003` |
| `assertions/0/relation` | `supports` |
| `assertions/0/modality` | `observed` |
| `assertions/1/claimId` | `CLM-EV24-004` |
| `assertions/1/relation` | `contradicts` |
| `assertions/1/modality` | `observed` |

### TRF-EV24-001

| Field | Value |
|---|---|
| `id` | `TRF-EV24-001` |
| `kind` | `republication` |
| `inputItemId` | `ITEM-EV24-001` |
| `outputItemId` | `ITEM-EV24-003` |
| `inputSha256` | `c69a9e4562b636598193d4f00a423b1055e7cff60e93c59914deddd764d95360` |
| `outputSha256` | `f7261233a7f2c2efc76cc880a13617e0aa9e1c47efb5ad8fe5553a62e6f3b499` |
| `agent` | `SYNTH-EDITOR` |
| `toolVersion` | `authored-fixture-1` |
| `performedAt` | `2026-10-04T00:15:00Z` |
| `originalLanguage` | `en` |
| `outputLanguage` | `en` |
| `reviewer` | `SYNTH-REVIEWER` |
| `reviewState` | `reviewed` |
| `meaning` | `preserved` |
| `ambiguousTerm` | `not-applicable` |
| `limitations` | `作業Copyだけ。原本の上書きなし。意味対応は著者の有限供給条件。` |

### TRF-EV24-002

| Field | Value |
|---|---|
| `id` | `TRF-EV24-002` |
| `kind` | `republication` |
| `inputItemId` | `ITEM-EV24-003` |
| `outputItemId` | `ITEM-EV24-004` |
| `inputSha256` | `f7261233a7f2c2efc76cc880a13617e0aa9e1c47efb5ad8fe5553a62e6f3b499` |
| `outputSha256` | `c44bf3da1ad023769f1401b28b590ecd34b184854f05f7c92cd15232dbeeb3da` |
| `agent` | `SYNTH-EDITOR` |
| `toolVersion` | `authored-fixture-1` |
| `performedAt` | `2026-10-04T00:30:00Z` |
| `originalLanguage` | `en` |
| `outputLanguage` | `en` |
| `reviewer` | `SYNTH-REVIEWER` |
| `reviewState` | `reviewed` |
| `meaning` | `preserved` |
| `ambiguousTerm` | `not-applicable` |
| `limitations` | `作業Copyだけ。原本の上書きなし。意味対応は著者の有限供給条件。` |

### TRF-EV24-003

| Field | Value |
|---|---|
| `id` | `TRF-EV24-003` |
| `kind` | `translation` |
| `inputItemId` | `ITEM-EV24-002` |
| `outputItemId` | `ITEM-EV24-007` |
| `inputSha256` | `432658d93cdae4d8c50117d72aa0f38e8915da49d1736632aa61f603bc6c0bab` |
| `outputSha256` | `e161581e00ee9e9cdbd90431e5964fb6f72490a89842c1134a509d2fd2243a62` |
| `agent` | `SYNTH-EDITOR` |
| `toolVersion` | `authored-fixture-1` |
| `performedAt` | `2026-10-04T01:40:00Z` |
| `originalLanguage` | `en` |
| `outputLanguage` | `ja` |
| `reviewer` | `SYNTH-REVIEWER` |
| `reviewState` | `reviewed` |
| `meaning` | `preserved` |
| `ambiguousTerm` | `may / 可能性。発生の断定へ強めない。` |
| `limitations` | `作業Copyだけ。原本の上書きなし。意味対応は著者の有限供給条件。` |

### TRF-EV24-004

| Field | Value |
|---|---|
| `id` | `TRF-EV24-004` |
| `kind` | `ai-summary` |
| `inputItemId` | `ITEM-EV24-002` |
| `outputItemId` | `ITEM-EV24-008` |
| `inputSha256` | `432658d93cdae4d8c50117d72aa0f38e8915da49d1736632aa61f603bc6c0bab` |
| `outputSha256` | `1a3c2c08a4947a4072a1c4889c36b759b8a76d07bc9e499d100ba3e5f7bc3610` |
| `agent` | `SYNTH-AI-ILLUSTRATION` |
| `toolVersion` | `authored-fixture-1` |
| `performedAt` | `2026-10-04T01:50:00Z` |
| `originalLanguage` | `en` |
| `outputLanguage` | `en` |
| `reviewer` | `SYNTH-REVIEWER` |
| `reviewState` | `rejected` |
| `meaning` | `changed` |
| `ambiguousTerm` | `not-applicable` |
| `limitations` | `作業Copyだけ。原本の上書きなし。意味対応は著者の有限供給条件。` |

### TRF-EV24-005

| Field | Value |
|---|---|
| `id` | `TRF-EV24-005` |
| `kind` | `extraction` |
| `inputItemId` | `ITEM-EV24-006` |
| `outputItemId` | `ITEM-EV24-009` |
| `inputSha256` | `42bd1d32a8646267ac2543d7cbe9bde26af54f61cb23a68b2d3ebb0cf3b092e9` |
| `outputSha256` | `7f7b276db5cdca039d60b50125955c8612e775d75621b8e1c33c74b81ef549f4` |
| `agent` | `SYNTH-EDITOR` |
| `toolVersion` | `authored-fixture-1` |
| `performedAt` | `2026-10-04T02:00:00Z` |
| `originalLanguage` | `en` |
| `outputLanguage` | `en` |
| `reviewer` | `SYNTH-REVIEWER` |
| `reviewState` | `pending` |
| `meaning` | `preserved` |
| `ambiguousTerm` | `not-applicable` |
| `limitations` | `作業Copyだけ。原本の上書きなし。意味対応は著者の有限供給条件。` |

### CITE-EV24-001

| Field | Value |
|---|---|
| `id` | `CITE-EV24-001` |
| `kind` | `later-citation-event` |
| `fromResourceId` | `RESOURCE-EV24-003` |
| `toResourceId` | `RESOURCE-EV24-004` |
| `contextItemIds/0` | `ITEM-EV24-003` |
| `contextItemIds/1` | `ITEM-EV24-004` |
| `occurredAt` | `2026-10-04T00:40:00Z` |
| `recordedAt` | `2026-10-04T00:45:00Z` |
| `recordingMethod` | `author-supplied-not-network-observation` |
| `meaning` | `later-mutual-reference-no-new-observation` |

### CITE-EV24-002

| Field | Value |
|---|---|
| `id` | `CITE-EV24-002` |
| `kind` | `later-citation-event` |
| `fromResourceId` | `RESOURCE-EV24-004` |
| `toResourceId` | `RESOURCE-EV24-003` |
| `contextItemIds/0` | `ITEM-EV24-003` |
| `contextItemIds/1` | `ITEM-EV24-004` |
| `occurredAt` | `2026-10-04T00:50:00Z` |
| `recordedAt` | `2026-10-04T00:55:00Z` |
| `recordingMethod` | `author-supplied-not-network-observation` |
| `meaning` | `later-mutual-reference-no-new-observation` |

### VER-EV24-001

| Field | Value |
|---|---|
| `id` | `VER-EV24-001` |
| `previousItemId` | `ITEM-EV24-001` |
| `currentItemId` | `ITEM-EV24-002` |
| `reason` | `同じAdvisoryの供給訂正。原本を保持して対象条件を限定する。` |

### EV-EV24-001

| Field | Value |
|---|---|
| `id` | `EV-EV24-001` |
| `itemId` | `ITEM-EV24-001` |
| `claimId` | `CLM-EV24-001` |
| `relation` | `supports` |
| `use` | `Context` |
| `credibility/value` | `limited` |
| `credibility/reason` | `旧版の初期説明で現行v2の直接裏付けではない。` |
| `independence/value` | `independent-in-supplied-model` |
| `independence/observationGroups/0` | `OBS-EV24-001` |
| `independence/reason` | `供給された内容の親子関係をたどる。別URLや記事数から独立性を推定しない。` |
| `limitations` | `旧版の初期説明で現行v2の直接裏付けではない。` |
| `hypothesisIds/0` | `HYP-EV24-001` |
| `hypothesisIds/1` | `HYP-EV24-002` |
| `gapId` | `GAP-EV24-001` |
| `reassessmentId` | `REV-EV24-001` |

### EV-EV24-002

| Field | Value |
|---|---|
| `id` | `EV-EV24-002` |
| `itemId` | `ITEM-EV24-002` |
| `claimId` | `CLM-EV24-002` |
| `relation` | `supports` |
| `use` | `Direct evidence` |
| `credibility/value` | `supported` |
| `credibility/reason` | `供給v2のBatch条件の可能性だけ。発生確定ではない。` |
| `independence/value` | `independent-in-supplied-model` |
| `independence/observationGroups/0` | `OBS-EV24-001` |
| `independence/reason` | `供給された内容の親子関係をたどる。別URLや記事数から独立性を推定しない。` |
| `limitations` | `供給v2のBatch条件の可能性だけ。発生確定ではない。` |
| `hypothesisIds/0` | `HYP-EV24-001` |
| `hypothesisIds/1` | `HYP-EV24-002` |
| `gapId` | `GAP-EV24-002` |
| `reassessmentId` | `REV-EV24-002` |

### EV-EV24-003

| Field | Value |
|---|---|
| `id` | `EV-EV24-003` |
| `itemId` | `ITEM-EV24-003` |
| `claimId` | `CLM-EV24-001` |
| `relation` | `supports` |
| `use` | `Context` |
| `credibility/value` | `limited` |
| `credibility/reason` | `旧Advisoryの引用で追加の独立観測なし。` |
| `independence/value` | `same-origin` |
| `independence/observationGroups/0` | `OBS-EV24-001` |
| `independence/reason` | `供給された内容の親子関係をたどる。別URLや記事数から独立性を推定しない。` |
| `limitations` | `旧Advisoryの引用で追加の独立観測なし。` |
| `hypothesisIds/0` | `HYP-EV24-001` |
| `hypothesisIds/1` | `HYP-EV24-002` |
| `gapId` | `GAP-EV24-003` |
| `reassessmentId` | `REV-EV24-003` |

### EV-EV24-004

| Field | Value |
|---|---|
| `id` | `EV-EV24-004` |
| `itemId` | `ITEM-EV24-004` |
| `claimId` | `CLM-EV24-001` |
| `relation` | `supports` |
| `use` | `Context` |
| `credibility/value` | `limited` |
| `credibility/reason` | `同じ旧原典の転載。相互引用を新根拠にしない。` |
| `independence/value` | `same-origin` |
| `independence/observationGroups/0` | `OBS-EV24-001` |
| `independence/reason` | `供給された内容の親子関係をたどる。別URLや記事数から独立性を推定しない。` |
| `limitations` | `同じ旧原典の転載。相互引用を新根拠にしない。` |
| `hypothesisIds/0` | `HYP-EV24-001` |
| `hypothesisIds/1` | `HYP-EV24-002` |
| `gapId` | `GAP-EV24-004` |
| `reassessmentId` | `REV-EV24-004` |

### EV-EV24-005

| Field | Value |
|---|---|
| `id` | `EV-EV24-005` |
| `itemId` | `ITEM-EV24-005` |
| `claimId` | `CLM-EV24-004` |
| `relation` | `supports` |
| `use` | `Unverified` |
| `credibility/value` | `unverified` |
| `credibility/reason` | `記入済みの発行役割と個別Claimの裏付けを区別する。` |
| `independence/value` | `unknown` |
| `independence/observationGroups/0` | `OBS-EV24-002` |
| `independence/reason` | `供給された内容の親子関係をたどる。別URLや記事数から独立性を推定しない。` |
| `limitations` | `記入済みの発行役割と個別Claimの裏付けを区別する。` |
| `hypothesisIds/0` | `HYP-EV24-001` |
| `hypothesisIds/1` | `HYP-EV24-002` |
| `gapId` | `GAP-EV24-005` |
| `reassessmentId` | `REV-EV24-005` |

### EV-EV24-006

| Field | Value |
|---|---|
| `id` | `EV-EV24-006` |
| `itemId` | `ITEM-EV24-006` |
| `claimId` | `CLM-EV24-003` |
| `relation` | `supports` |
| `use` | `Direct evidence` |
| `credibility/value` | `supported` |
| `credibility/reason` | `供給20件内の零件だけ。全体やBatchの不存在は示さない。` |
| `independence/value` | `independent-in-supplied-model` |
| `independence/observationGroups/0` | `OBS-EV24-003` |
| `independence/reason` | `供給された内容の親子関係をたどる。別URLや記事数から独立性を推定しない。` |
| `limitations` | `供給20件内の零件だけ。全体やBatchの不存在は示さない。` |
| `hypothesisIds/0` | `HYP-EV24-001` |
| `hypothesisIds/1` | `HYP-EV24-002` |
| `gapId` | `GAP-EV24-006` |
| `reassessmentId` | `REV-EV24-006` |

### EV-EV24-007

| Field | Value |
|---|---|
| `id` | `EV-EV24-007` |
| `itemId` | `ITEM-EV24-007` |
| `claimId` | `CLM-EV24-002` |
| `relation` | `supports` |
| `use` | `Direct evidence` |
| `credibility/value` | `supported` |
| `credibility/reason` | `可能性のまま訳し、元と同じ観測group一件に束ねる。` |
| `independence/value` | `same-origin` |
| `independence/observationGroups/0` | `OBS-EV24-001` |
| `independence/reason` | `供給された内容の親子関係をたどる。別URLや記事数から独立性を推定しない。` |
| `limitations` | `可能性のまま訳し、元と同じ観測group一件に束ねる。` |
| `hypothesisIds/0` | `HYP-EV24-001` |
| `hypothesisIds/1` | `HYP-EV24-002` |
| `gapId` | `GAP-EV24-007` |
| `reassessmentId` | `REV-EV24-007` |

### EV-EV24-008

| Field | Value |
|---|---|
| `id` | `EV-EV24-008` |
| `itemId` | `ITEM-EV24-008` |
| `claimId` | `CLM-EV24-004` |
| `relation` | `supports` |
| `use` | `Excluded` |
| `credibility/value` | `unverified` |
| `credibility/reason` | `原典にない全sessionの確定へ強まった誤要約。` |
| `independence/value` | `same-origin` |
| `independence/observationGroups/0` | `OBS-EV24-001` |
| `independence/reason` | `供給された内容の親子関係をたどる。別URLや記事数から独立性を推定しない。` |
| `limitations` | `原典にない全sessionの確定へ強まった誤要約。` |
| `hypothesisIds/0` | `HYP-EV24-001` |
| `hypothesisIds/1` | `HYP-EV24-002` |
| `gapId` | `GAP-EV24-008` |
| `reassessmentId` | `REV-EV24-008` |

### EV-EV24-009

| Field | Value |
|---|---|
| `id` | `EV-EV24-009` |
| `itemId` | `ITEM-EV24-009` |
| `claimId` | `CLM-EV24-003` |
| `relation` | `supports` |
| `use` | `Lead` |
| `credibility/value` | `limited` |
| `credibility/reason` | `作業抽出のreview未完。判断根拠へ追加しない。` |
| `independence/value` | `same-origin` |
| `independence/observationGroups/0` | `OBS-EV24-003` |
| `independence/reason` | `供給された内容の親子関係をたどる。別URLや記事数から独立性を推定しない。` |
| `limitations` | `作業抽出のreview未完。判断根拠へ追加しない。` |
| `hypothesisIds/0` | `HYP-EV24-001` |
| `hypothesisIds/1` | `HYP-EV24-002` |
| `gapId` | `GAP-EV24-009` |
| `reassessmentId` | `REV-EV24-009` |

### EV-EV24-010

| Field | Value |
|---|---|
| `id` | `EV-EV24-010` |
| `itemId` | `ITEM-EV24-006` |
| `claimId` | `CLM-EV24-004` |
| `relation` | `contradicts` |
| `use` | `Direct evidence` |
| `credibility/value` | `supported` |
| `credibility/reason` | `供給二十件の値は、教材の全称Claimと矛盾する。Batch条件は未観測。` |
| `independence/value` | `independent-in-supplied-model` |
| `independence/observationGroups/0` | `OBS-EV24-003` |
| `independence/reason` | `供給された内容の親子関係をたどる。別URLや記事数から独立性を推定しない。` |
| `limitations` | `供給二十件の値は、教材の全称Claimと矛盾する。Batch条件は未観測。` |
| `hypothesisIds/0` | `HYP-EV24-001` |
| `hypothesisIds/1` | `HYP-EV24-002` |
| `gapId` | `GAP-EV24-010` |
| `reassessmentId` | `REV-EV24-010` |

### GAP-EV24-001

| Field | Value |
|---|---|
| `id` | `GAP-EV24-001` |
| `evaluationId` | `EV-EV24-001` |
| `owner` | `SYNTH-ANALYSIS-OWNER` |
| `deadline` | `2026-10-05T00:00:00Z` |
| `reason` | `旧版の初期説明で現行v2の直接裏付けではない。` |
| `invalidation` | `新しい版、独立観測、訳語、Terms変更を受けたら根拠と用途を再評価する。` |
| `reassessmentId` | `REV-EV24-001` |

### GAP-EV24-002

| Field | Value |
|---|---|
| `id` | `GAP-EV24-002` |
| `evaluationId` | `EV-EV24-002` |
| `owner` | `SYNTH-ANALYSIS-OWNER` |
| `deadline` | `2026-10-05T00:00:00Z` |
| `reason` | `供給v2のBatch条件の可能性だけ。発生確定ではない。` |
| `invalidation` | `新しい版、独立観測、訳語、Terms変更を受けたら根拠と用途を再評価する。` |
| `reassessmentId` | `REV-EV24-002` |

### GAP-EV24-003

| Field | Value |
|---|---|
| `id` | `GAP-EV24-003` |
| `evaluationId` | `EV-EV24-003` |
| `owner` | `SYNTH-ANALYSIS-OWNER` |
| `deadline` | `2026-10-05T00:00:00Z` |
| `reason` | `旧Advisoryの引用で追加の独立観測なし。` |
| `invalidation` | `新しい版、独立観測、訳語、Terms変更を受けたら根拠と用途を再評価する。` |
| `reassessmentId` | `REV-EV24-003` |

### GAP-EV24-004

| Field | Value |
|---|---|
| `id` | `GAP-EV24-004` |
| `evaluationId` | `EV-EV24-004` |
| `owner` | `SYNTH-ANALYSIS-OWNER` |
| `deadline` | `2026-10-05T00:00:00Z` |
| `reason` | `同じ旧原典の転載。相互引用を新根拠にしない。` |
| `invalidation` | `新しい版、独立観測、訳語、Terms変更を受けたら根拠と用途を再評価する。` |
| `reassessmentId` | `REV-EV24-004` |

### GAP-EV24-005

| Field | Value |
|---|---|
| `id` | `GAP-EV24-005` |
| `evaluationId` | `EV-EV24-005` |
| `owner` | `SYNTH-ANALYSIS-OWNER` |
| `deadline` | `2026-10-05T00:00:00Z` |
| `reason` | `記入済みの発行役割と個別Claimの裏付けを区別する。` |
| `invalidation` | `新しい版、独立観測、訳語、Terms変更を受けたら根拠と用途を再評価する。` |
| `reassessmentId` | `REV-EV24-005` |

### GAP-EV24-006

| Field | Value |
|---|---|
| `id` | `GAP-EV24-006` |
| `evaluationId` | `EV-EV24-006` |
| `owner` | `SYNTH-ANALYSIS-OWNER` |
| `deadline` | `2026-10-05T00:00:00Z` |
| `reason` | `供給20件内の零件だけ。全体やBatchの不存在は示さない。` |
| `invalidation` | `新しい版、独立観測、訳語、Terms変更を受けたら根拠と用途を再評価する。` |
| `reassessmentId` | `REV-EV24-006` |

### GAP-EV24-007

| Field | Value |
|---|---|
| `id` | `GAP-EV24-007` |
| `evaluationId` | `EV-EV24-007` |
| `owner` | `SYNTH-ANALYSIS-OWNER` |
| `deadline` | `2026-10-05T00:00:00Z` |
| `reason` | `可能性のまま訳し、元と同じ観測group一件に束ねる。` |
| `invalidation` | `新しい版、独立観測、訳語、Terms変更を受けたら根拠と用途を再評価する。` |
| `reassessmentId` | `REV-EV24-007` |

### GAP-EV24-008

| Field | Value |
|---|---|
| `id` | `GAP-EV24-008` |
| `evaluationId` | `EV-EV24-008` |
| `owner` | `SYNTH-ANALYSIS-OWNER` |
| `deadline` | `2026-10-05T00:00:00Z` |
| `reason` | `原典にない全sessionの確定へ強まった誤要約。` |
| `invalidation` | `新しい版、独立観測、訳語、Terms変更を受けたら根拠と用途を再評価する。` |
| `reassessmentId` | `REV-EV24-008` |

### GAP-EV24-009

| Field | Value |
|---|---|
| `id` | `GAP-EV24-009` |
| `evaluationId` | `EV-EV24-009` |
| `owner` | `SYNTH-ANALYSIS-OWNER` |
| `deadline` | `2026-10-05T00:00:00Z` |
| `reason` | `作業抽出のreview未完。判断根拠へ追加しない。` |
| `invalidation` | `新しい版、独立観測、訳語、Terms変更を受けたら根拠と用途を再評価する。` |
| `reassessmentId` | `REV-EV24-009` |

### GAP-EV24-010

| Field | Value |
|---|---|
| `id` | `GAP-EV24-010` |
| `evaluationId` | `EV-EV24-010` |
| `owner` | `SYNTH-ANALYSIS-OWNER` |
| `deadline` | `2026-10-05T00:00:00Z` |
| `reason` | `供給二十件の値は、教材の全称Claimと矛盾する。Batch条件は未観測。` |
| `invalidation` | `新しい版、独立観測、訳語、Terms変更を受けたら根拠と用途を再評価する。` |
| `reassessmentId` | `REV-EV24-010` |

### HYP-EV24-001

| Field | Value |
|---|---|
| `id` | `HYP-EV24-001` |
| `text` | `Batchに限定した条件で説明できる可能性。` |
| `decision` | `not-concluded` |

### HYP-EV24-002

| Field | Value |
|---|---|
| `id` | `HYP-EV24-002` |
| `text` | `供給資料にない条件が残る可能性。` |
| `decision` | `not-concluded` |

### HOF-EV24-25

| Field | Value |
|---|---|
| `id` | `HOF-EV24-25` |
| `chapter` | `25` |
| `audience` | `SYNTH-ANALYSIS-READER` |
| `status` | `planned-not-delivered` |
| `receipt` | `null` |
| `executionAuthorized` | `false` |
| `evidenceIds/0` | `EV-EV24-001` |
| `evidenceIds/1` | `EV-EV24-002` |
| `evidenceIds/2` | `EV-EV24-003` |
| `evidenceIds/3` | `EV-EV24-004` |
| `evidenceIds/4` | `EV-EV24-005` |
| `evidenceIds/5` | `EV-EV24-006` |
| `evidenceIds/6` | `EV-EV24-007` |
| `evidenceIds/7` | `EV-EV24-008` |
| `evidenceIds/8` | `EV-EV24-009` |
| `evidenceIds/9` | `EV-EV24-010` |
| `gapIds/0` | `GAP-EV24-001` |
| `gapIds/1` | `GAP-EV24-002` |
| `gapIds/2` | `GAP-EV24-003` |
| `gapIds/3` | `GAP-EV24-004` |
| `gapIds/4` | `GAP-EV24-005` |
| `gapIds/5` | `GAP-EV24-006` |
| `gapIds/6` | `GAP-EV24-007` |
| `gapIds/7` | `GAP-EV24-008` |
| `gapIds/8` | `GAP-EV24-009` |
| `gapIds/9` | `GAP-EV24-010` |
| `deadline` | `2026-10-05T01:00:00Z` |
| `limitation` | `制約と除外も記録として渡す予定。既存Caseへ根拠を自動投入せず実配布しない。` |

### HOF-EV24-26

| Field | Value |
|---|---|
| `id` | `HOF-EV24-26` |
| `chapter` | `26` |
| `audience` | `SYNTH-DISTRIBUTION-READER` |
| `status` | `planned-not-delivered` |
| `receipt` | `null` |
| `executionAuthorized` | `false` |
| `evidenceIds/0` | `EV-EV24-001` |
| `evidenceIds/1` | `EV-EV24-002` |
| `evidenceIds/2` | `EV-EV24-003` |
| `evidenceIds/3` | `EV-EV24-004` |
| `evidenceIds/4` | `EV-EV24-005` |
| `evidenceIds/5` | `EV-EV24-006` |
| `evidenceIds/6` | `EV-EV24-007` |
| `evidenceIds/7` | `EV-EV24-008` |
| `evidenceIds/8` | `EV-EV24-009` |
| `evidenceIds/9` | `EV-EV24-010` |
| `gapIds/0` | `GAP-EV24-001` |
| `gapIds/1` | `GAP-EV24-002` |
| `gapIds/2` | `GAP-EV24-003` |
| `gapIds/3` | `GAP-EV24-004` |
| `gapIds/4` | `GAP-EV24-005` |
| `gapIds/5` | `GAP-EV24-006` |
| `gapIds/6` | `GAP-EV24-007` |
| `gapIds/7` | `GAP-EV24-008` |
| `gapIds/8` | `GAP-EV24-009` |
| `gapIds/9` | `GAP-EV24-010` |
| `deadline` | `2026-10-05T01:00:00Z` |
| `limitation` | `制約と除外も記録として渡す予定。既存Caseへ根拠を自動投入せず実配布しない。` |

## 再評価と提出

入力の対象・版・利用条件・変換・独立観測が変わったら、以前の評価を残して再評価します。根拠が増えなくてもGapとOwner、期限を説明できれば記入成果物を完成できます。第25/26章へは全評価と制限を渡す予定であり、Excludedを判断根拠として推薦する配布ではありません。receipt nullと実行権限falseを保持します。
