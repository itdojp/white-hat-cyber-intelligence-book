# 第11章 合成記入例：マルチテナント受注Export APIとWebhook登録の評価

## この記入例の扱い

この文書は、`Web/API Assessment Hypothesis Pack`の記入方法を示すための完全な合成例である。

- 組織名、担当者、Role、Token、Host名、Request、Response、判断はすべて架空である。
- Domainは予約済みの`.example`、`.test`を使用する。
- 実Credential、実Token、実Cookie、個人情報、第三者Systemは使用しない。
- 外部通信、Data大量取得、負荷試験、横展開、Credential reuseは行わない。
- Webhook先のHost名は合成値であり、実在の内部Serviceを指さない。
- 本文は、攻撃成功手順ではなく、仮説・証拠・Detectionへの接続例を示す。

参照する空テンプレートは[Web/API Assessment Hypothesis Pack](../templates/web-api-assessment-hypothesis-pack.md)である。

Request / ResponseとDetection eventは、外部通信を行わない[読み取り専用の合成Dataset](fixtures/ch11-web-api-assessment-dataset.json)に収録している。

## 悪い仮説から良い仮説へ

| Note ID | Before | After | Why the revision matters |
|---|---|---|---|
| `NOTE-2026-011` | APIに認可不備がないか確認する | `tenant-blue.example`のAnalyst tokenが、他TenantのCompleted export job metadataを取得できる可能性がある | 望ましくない成立条件、Asset、Actor、Tenant boundary、Stateが明確になる |
| `NOTE-2026-012` | WebhookでSSRFできるか試す | `callbackUrl=https://control-plane.service.test/internal-status`が登録され、dispatch taskが作成される可能性がある | 望ましくない成立条件を合成Hostで確認し、Stop pointを明示できる |
| `NOTE-2026-013` | 負荷をかけて落ちるかを見る | 同一`Idempotency-Key`の3回再試行で、job countが1件を超えて増える可能性がある | 高負荷を避け、Resource controlの成立条件だけを確認できる |

## 0. Document Control

| Field | Value |
|---|---|
| Artifact ID | `ART-11` |
| Case ID | `CASE-2026-011` |
| Title | マルチテナント受注Export APIとWebhook登録の評価 |
| Status | Detection Handoff |
| Owner | Security Assessment Lead |
| Contributors | Platform、Backend、SOC、Product Security |
| Classification | Internal |
| Created at | 2026-07-28T09:00:00+09:00 |
| Updated at | 2026-08-02T18:10:00+09:00 |
| Review deadline | 2026-08-05T18:00:00+09:00 |
| Related Issue / Ticket | Feature Gate FG-2026-08 / API Launch Review |
| Related Case Map Artifact | `ART-10` |
| Related Case Map Case ID | `CASE-2026-011` |
| Related Case Map Decision ID | `DEC-2026-011` |

## 1. Decision Requirement and Scope

| Field | Value |
|---|---|
| Decision Requirement ID | `DR-2026-011` |
| Decision owner | VP of Product Engineering |
| Decision deadline | 2026-08-05T18:00:00+09:00 |
| Decision question | Export APIとWebhook self-service機能を、全Tenantへ段階公開してよいか |
| Decision options | 即時公開 / 条件付き公開 / remediation完了まで延期 |
| Decision criteria | Tenant boundary、管理機能保護、Webhook境界保護、最低限のDetection成立 |
| Maximum acceptable uncertainty | 重大なFunction / Property authz gapが未解消でないこと。Telemetry gapはOwnerと期限が必要 |
| Consequence of delay | 8月のPartner onboarding延期、営業計画とサポート工数に影響 |
| Authority / RoE ID | `ROE-2026-011` |
| In-scope assets / surfaces | `api.orders.example` の `/api/v1/admin/report-export`、`/api/v2/exports`、`/api/v2/export-jobs/{jobId}`、`/api/v2/webhooks`、`/api/v2/exports/retry` |
| Out-of-scope assets / surfaces | 本番Tenant data、本番配送Webhook、支払いAPI、第三者SaaS連携、本番DB |
| Permitted operations | ローカル隔離Fixtureでの合成Request再生、設定差分確認、合成Audit log確認、3回以下の再試行確認 |
| Prohibited operations | 実Webhook送信、他Tenant data本文取得、実Token使用、負荷試験、権限昇格、外部通信 |
| Permitted data | 合成Tenant、合成Job metadata、無効な合成Token値、匿名化済み設定抜粋 |
| Test window | 2026-07-29T10:00:00+09:00 〜 2026-08-01T18:00:00+09:00 |
| Stop conditions | 外向き通信発生、実Data混入、3回を超える再試行必要、Cleanup不能なjob生成、権限外操作が必要 |
| Cleanup owner | Platform QA Lead |

### 判断に不要な高リスク操作

- 実Tenant export file本文の取得
- 実在HostへのWebhook到達確認
- 高頻度RequestによるRate / Queue枯渇試験
- 本番認証基盤に対するToken偽造・改変試験

## 2. Asset, Boundary, and State Context

### 2.1 Assets

| Asset ID | Service / endpoint / job | Business role | Data classification | Owner | Notes |
|---|---|---|---|---|---|
| `ASSET-2026-011` | `api.orders.example /api/v2/export-jobs/{jobId}` | Tenant別の受注Export job参照 | Internal business data | Backend Team | 非同期job metadataとdownload準備状態を返す |
| `ASSET-2026-012` | `api.orders.example /api/v1/admin/report-export` | 管理者向けCSV export作成 | Internal business data | Backend Team | Deprecated APIだがlegacy client互換で残存 |
| `ASSET-2026-013` | `api.orders.example /api/v2/exports` | Tenant analystによるExport作成 | Internal business data | Backend Team | `includeInternalNotes`と`status`をRequest bodyに含めうる |
| `ASSET-2026-014` | `api.orders.example /api/v2/webhooks` | 配送Webhook登録 | Integration config | Platform Team | 非同期dispatch workerへ連携 |
| `ASSET-2026-015` | `api.orders.example /api/v2/exports/retry` | 失敗Export job再試行 | Queue workload control | Platform Team | `Idempotency-Key`による重複抑止が要件 |

### 2.2 Actor and Credential Classes

| Actor ID | Role / user class | Credential / session class | Intended scope | Prohibited capability | Notes |
|---|---|---|---|---|---|
| `ACT-2026-011` | Analyst | API token `tok-analyst-invalid` | 自TenantのExport作成と参照 | 管理者Export、内部メモ含むExport、他Tenant job参照 | 合成Token。実環境では無効 |
| `ACT-2026-012` | Tenant Admin | API token `tok-admin-invalid` | Webhook登録、Export管理 | 他Tenant操作、内部運用API呼出し | 合成Token。実環境では無効 |
| `ACT-2026-013` | Worker | Queue service credential | Queueからdispatch task処理 | 未検証Webhook先への送信 | ローカルFixtureでdispatchは無効化 |

### 2.3 Trust, Tenant, and Server-side Boundaries

| Boundary ID | Asset ID | Boundary type | From | To | Control | Failure consequence |
|---|---|---|---|---|---|---|
| `TB-2026-011` | `ASSET-2026-011` | Tenant / Object | Analyst token | Export job metadata | `tenantId == job.ownerTenantId` 判定 | 他Tenantのjob metadata露出 |
| `TB-2026-012` | `ASSET-2026-012` | Function / Role | Analyst token | Admin export作成 | `role == admin` 判定 | 非管理者による管理機能実行 |
| `TB-2026-013` | `ASSET-2026-013` | Property / State | Analyst session | Export request body | allowed fields filter、state machine | 内部メモ露出、状態飛び越し |
| `TB-2026-014` | `ASSET-2026-014` | Server-side / Network | Webhook登録 | Dispatch queue | hostname normalization、allow / deny policy | 内部向け送信試行 |
| `TB-2026-015` | `ASSET-2026-015` | Resource / Idempotency | Retry request | Queue / quota counter | unique idempotency key enforcement | 重複job生成、queue増加 |

### 2.4 Workflow State and Business Rules

| State ID | Asset ID | Triggering action | Required actor / approval | Allowed next state | Forbidden shortcut |
|---|---|---|---|---|---|
| `STATE-2026-011` | `ASSET-2026-011` | Export job作成 | Analyst or Admin / own tenant | `pending` → `completed` or `failed` | 他Tenant jobの直接参照 |
| `STATE-2026-012` | `ASSET-2026-013` | `includeInternalNotes`指定 | Adminのみ | `draft` → `queued` | Analystが内部メモ付きExportを作ること |
| `STATE-2026-013` | `ASSET-2026-014` | Webhook登録 | Adminのみ、Host validation必須 | `submitted` → `validated` → `active` | validation前にdispatch対象化 |
| `STATE-2026-014` | `ASSET-2026-015` | Retry実行 | Analyst / own tenant | failed jobごとに1件だけ再作成 | 同一Idempotency-Keyで複数job生成 |

### 2.5 Inventory, Version, and Deprecation Coverage

| Surface ID | Asset ID | Path / operation / webhook / worker | Version | Discovery source | Deprecated | Security note |
|---|---|---|---|---|---|---|
| `SURF-2026-011` | `ASSET-2026-011` | `GET /api/v2/export-jobs/{jobId}` | v2 | OpenAPI snapshot 2026-07-28 | No | job metadata参照 |
| `SURF-2026-012` | `ASSET-2026-012` | `POST /api/v1/admin/report-export` | v1 | Route inventory export | Yes | UI導線なし。legacy client専用 |
| `SURF-2026-013` | `ASSET-2026-013` | `POST /api/v2/exports` | v2 | OpenAPI snapshot 2026-07-28 | No | property-level制約が必要 |
| `SURF-2026-014` | `ASSET-2026-014` | `POST /api/v2/webhooks` | v2 | OpenAPI snapshot 2026-07-28 | No | server-side dispatch連携 |
| `SURF-2026-015` | `ASSET-2026-015` | `POST /api/v2/exports/retry` | v2 | Worker API inventory | No | idempotency key再利用制御 |

## 3. Hypothesis Register

### 3.1 Threat Hypotheses

| Threat Hypothesis ID | Asset ID | Security property | Actor / credential class | Entry point | Boundary / state | Hypothesis statement | Priority | Status |
|---|---|---|---|---|---|---|---|---|
| `TH-2026-011` | `ASSET-2026-011` | Object authz | `ACT-2026-011` | `GET /api/v2/export-jobs/{jobId}` | `TB-2026-011` / `STATE-2026-011` | Analyst tokenが、他TenantのCompleted export job metadataを取得できる可能性がある | High | Rejected |
| `TH-2026-012` | `ASSET-2026-012` | Function authz | `ACT-2026-011` | `POST /api/v1/admin/report-export` | `TB-2026-012` | Deprecated v1 admin exportが、Analyst tokenで成功しjobを作成できる可能性がある | High | Supported |
| `TH-2026-013` | `ASSET-2026-013` | Property authz / State | `ACT-2026-011` | `POST /api/v2/exports` | `TB-2026-013` / `STATE-2026-012` | Analyst sessionで`includeInternalNotes=true`が保存される、または`status=approved`が受理される可能性がある | High | Partially supported |
| `TH-2026-014` | `ASSET-2026-014` | Server-side trust | `ACT-2026-012` | `POST /api/v2/webhooks` | `TB-2026-014` / `STATE-2026-013` | 内部向けHost名を含むWebhook callbackが登録され、dispatch taskが作成される可能性がある | High | Weakened |
| `TH-2026-015` | `ASSET-2026-015` | Resource control / Idempotency | `ACT-2026-011` | `POST /api/v2/exports/retry` | `TB-2026-015` / `STATE-2026-014` | 同一`Idempotency-Key`の3回再試行で、重複jobが1件を超えて生成される可能性がある | Medium | Supported |

### 3.2 Observation Hypotheses

| Observation Hypothesis ID | Related Threat Hypothesis ID | Expected authorized result | Expected denied result | Expected side effect | Disconfirming observation |
|---|---|---|---|---|---|
| `OBS-2026-011` | `TH-2026-011` | 自Tenant jobは200でmetadataのみ返る | 他Tenant jobは404または403で、download準備情報を返さない | queue access eventなし | 他Tenant job参照で200またはmetadata差分がある |
| `OBS-2026-012` | `TH-2026-012` | Admin tokenだけが202でjob作成される | Analyst tokenは403でjob作成されない | audit logに`authorization_denied` | Analyst tokenで202かつjob IDが発行される |
| `OBS-2026-013` | `TH-2026-013` | Admin sessionでは`includeInternalNotes=true`を許可できるが、client指定の`status=approved`は別の承認条件を満たさない限り受理しない | Analyst sessionでは`includeInternalNotes`を除去し、client指定stateにかかわらずqueued stateだけを許可する | auditにactor role、property filter、state normalizationが残る | Analyst sessionで内部メモが残る、またはapproved stateでqueue投入される |
| `OBS-2026-014` | `TH-2026-014` | Public allowlist hostだけが登録可能 | `control-plane.service.test`は400で拒否 | dispatch task未作成、deny reason記録 | 400でもdispatch taskが作成される、またはactive状態になる |
| `OBS-2026-015` | `TH-2026-015` | 1回目だけが新規job作成、残りは同一job再利用または429 | 重複job countが増えない | quota counterは1件分だけ増える | 2件以上のjob IDが作成される |

### 3.3 Good / Bad Hypothesis Notes

| Note ID | Before | After | Why the revision matters |
|---|---|---|---|
| `NOTE-2026-014` | Deprecated APIを一応確認する | Deprecated v1 admin exportがAnalyst tokenで成功しjobを作成できる可能性がある | Version差分、Actor、望ましくない成立条件を明確にできる |
| `NOTE-2026-015` | Retryで変なことが起きないか見る | 同一Idempotency-Key再試行で重複job countが1件を超えて増える可能性がある | Resource controlを安全な低回数試行へ変換できる |

## 4. Safe Validation Design

以下の表は、合成Datasetを作成した隔離Capture時の設計と完了記録である。本章の演習では記録済みJSONを読み取るだけで、Requestの再送、Job作成、Webhook登録、retryを実行しない。Stop conditionとCleanupはCapture時に適用済みであり、演習時の追加Cleanupは不要である。

| Validation ID | Related Threat Hypothesis ID | Related Observation Hypothesis ID | Recorded low-impact operation | Synthetic fixture / dataset | Expected evidence | Capture-time stop condition | Capture-time cleanup record |
|---|---|---|---|---|---|---|---|
| `VAL-2026-011` | `TH-2026-011` | `OBS-2026-011` | Capture時に合成Analyst tokenで自Tenant / 他Tenant job metadataを比較 | 読み取り専用の合成Dataset | response code差分、job metadata redaction、queue accessなし | 他Tenant本文取得が必要になった時点 | 完了済み。比較用job snapshotを破棄 |
| `VAL-2026-012` | `TH-2026-012` | `OBS-2026-012` | Capture時にv1 endpointへのexport作成Requestを1回記録 | 合成Route inventoryとread-only replay dataset | 202または403、job ID生成有無、route middleware設定 | 1件目でjob IDが作成された時点 | 完了済み。生成された合成jobを削除 |
| `VAL-2026-013` | `TH-2026-013` | `OBS-2026-013` | Capture時にAdmin / Analystの合成field付きExport作成を各1回記録 | 合成request/response dataset | role別応答、保存済みjob property、workflow audit | 内部メモ本文取得が必要になった時点 | 完了済み。2件の合成jobとqueue entryを削除 |
| `VAL-2026-014` | `TH-2026-014` | `OBS-2026-014` | Capture時に内部向け合成Host名を含むWebhook登録を1回記録 | egress無効の読み取り専用合成Dataset | 400、deny reason、dispatch task未作成 | 送信workerが起動しそうになった時点 | 完了済み。登録候補を削除 |
| `VAL-2026-015` | `TH-2026-015` | `OBS-2026-015` | Capture時に同一`Idempotency-Key`の最大3回再試行を記録 | 読み取り専用の合成Dataset | job count差分、quota counter差分 | 2件目の重複jobが作成された時点 | 完了済み。合成retry jobを削除 |

### 拒否系の確認

| Validation ID | Boundary checked | Low-impact rejected input or action | Expected denied result | Permitted conclusion |
|---|---|---|---|---|
| `VAL-2026-011` | Tenant / Object | 他Tenant `jobId`参照 | 404または403、queue accessなし | 確認したStateとVersionではcross-tenant参照を観測しなかった |
| `VAL-2026-014` | Server-side / Network | `control-plane.service.test` callback登録 | 400 / `internal_host_denied` | 登録時validationは機能している可能性が高いが、別Bypass pathは未評価 |

### 実施しない検証

- 実在の配送Webhook先への到達確認
- 他Tenant export本文の取得
- 10回超のretryまたは長時間queue枯渇試験
- Browser sessionの盗用やToken改変

## 5. Evidence Register and Findings Handoff

### 5.1 Evidence Register

| Evidence ID | Related Observation ID | Related Validation ID | Authority / RoE ID | Question supported | Source / collector | Collected at | Integrity / location | Limitation |
|---|---|---|---|---|---|---|---|---|
| `EVD-2026-011` | `OBS-2026-011` | `VAL-2026-011` | `ROE-2026-011` | 他Tenant job参照が拒否されるか | Fixture response pair collector | 2026-07-29T11:10:00+09:00 | 合成Dataset record `EVD-2026-011`（Gitで版管理） | Completed stateのv2 pathだけを確認 |
| `EVD-2026-012` | `OBS-2026-012` | `VAL-2026-012` | `ROE-2026-011` | Deprecated admin exportがAnalystで成功しないか | Route replay collector | 2026-07-29T14:20:00+09:00 | 合成Dataset record `EVD-2026-012`（Gitで版管理） | v1 endpoint以外のlegacy pathは未確認 |
| `EVD-2026-013` | `OBS-2026-013` | `VAL-2026-013` | `ROE-2026-011` | Adminの許可結果とAnalystの拒否結果をrole境界として比較できるか | Fixture response pair + stored job diff | 2026-07-30T10:05:00+09:00 | 合成Dataset records `REC-11-004`, `REC-11-007`（Gitで版管理） | 実本文は取得せずproperty flagのみ確認 |
| `EVD-2026-014` | `OBS-2026-014` | `VAL-2026-014` | `ROE-2026-011` | 内部向けWebhook hostが拒否されるか | Validation log collector | 2026-07-30T15:30:00+09:00 | 合成Dataset record `EVD-2026-014`（Gitで版管理） | 登録時validationだけを確認 |
| `EVD-2026-015` | `OBS-2026-015` | `VAL-2026-015` | `ROE-2026-011` | Retry pathで重複jobが生成されないか | Queue counter collector | 2026-07-31T09:40:00+09:00 | 合成Dataset record `EVD-2026-015`（Gitで版管理） | 3回までの低回数確認のみ |

### 5.2 Evidence Handling

| Evidence ID | Redaction status | Classification | Access scope | Retention / disposal date | Disposal owner |
|---|---|---|---|---|---|
| `EVD-2026-011` | No sensitive fields | Internal | Product Security、Backend | 2026-10-29 | Product Security Manager |
| `EVD-2026-012` | No sensitive fields | Internal | Product Security、Backend | 2026-10-29 | Product Security Manager |
| `EVD-2026-013` | Redacted | Confidential | Product Security、Platform | 2026-10-30 | Product Security Manager |
| `EVD-2026-014` | No sensitive fields | Internal | Product Security、Platform | 2026-10-30 | Product Security Manager |
| `EVD-2026-015` | No sensitive fields | Internal | Product Security、Platform | 2026-10-31 | Product Security Manager |

### 5.3 Negative Findings

| Negative Finding ID | Related Threat Hypothesis ID | Searched behavior | Search window | Available coverage | Remaining gaps | Permitted conclusion |
|---|---|---|---|---|---|---|
| `NEG-2026-011` | `TH-2026-011` | Completed stateの他Tenant export job metadata参照 | 2026-07-29T11:00:00+09:00 〜 11:15:00+09:00 | v2 path、completed state、Analyst token | draft state、別Version、cache pathは未確認 | この条件ではcross-tenant参照を観測しなかった |
| `NEG-2026-012` | `TH-2026-014` | 内部向けHost名Webhookの登録成功とdispatch task作成 | 2026-07-30T15:20:00+09:00 〜 15:35:00+09:00 | 合成Host入力1件、登録API、deny reason、dispatch queue不作成 | 別encoding、scheme、port、redirect、hostname normalization、DNS rebinding、別worker pathは未確認 | この合成Host入力は400で拒否され、dispatch taskも作成されなかった。登録時validation全体や別Bypass pathの有効性は結論しない |

### 5.4 Findings and Retest Handoff

| Finding ID | Related Threat Hypothesis ID | Root condition | Evidence IDs | Related Telemetry ID | Related Detection ID / planned ID | Business impact | Required remediation | Retest acceptance criteria |
|---|---|---|---|---|---|---|---|---|
| `FIND-2026-011` | `TH-2026-012` | Analyst tokenへの合成Requestが202となり、job IDが発行された。Route inventoryでは共通Authorization middlewareが未設定 | `EVD-2026-012` | `TEL-2026-011` | `DET-2026-011` | 非管理者が管理者向け大量Exportを起動しうる。監査上もv1 path利用を見落とす可能性 | v1 endpointを停止、または共通Authorization middlewareへ統合。legacy client移行計画を確定 | Analyst tokenで403、job ID未発行、admin tokenのみ202 |
| `FIND-2026-012` | `TH-2026-013` | Analyst sessionの`includeInternalNotes`がserver側で除去されず保存される。`status=approved`は拒否された | `EVD-2026-013` | `TEL-2026-012` | `DET-2026-012` | 内部メモがExport対象へ混入する恐れ。State shortcutは未成立だがproperty controlは不十分 | allowlistベースのproperty filter追加、internal note fieldのserver-side強制除外 | Analyst sessionで内部メモflagが保存されず、workflow auditにfield normalizationが残る |
| `FIND-2026-013` | `TH-2026-015` | Retry pathで同一`Idempotency-Key`にもかかわらず2件のjobが作成された | `EVD-2026-015` | `TEL-2026-014` | `DET-2026-013` | Queue増加、Tenant quota超過、重複通知、運用コスト増加 | retry pathを共通idempotency storeへ統合、quota counter再計算 | 同一Keyで1件のみ維持、quota counter増分1件 |

## 6. Telemetry and Detection Handoff

### 6.1 Required Telemetry

| Telemetry ID | Related Threat Hypothesis ID | Required event / fields | Retention | Current state | Gap owner |
|---|---|---|---|---|---|
| `TEL-2026-011` | `TH-2026-012` | endpoint path、version、actor role、tenant ID、response code、job ID、request ID | 180日 | Partial | Backend Team |
| `TEL-2026-012` | `TH-2026-013` | request field normalization、actor role、saved property diff、workflow state before / after | 180日 | Missing | Platform Team |
| `TEL-2026-013` | `TH-2026-014` | normalized hostname、scheme、deny reason、dispatch task created flag | 180日 | Available | Platform Team |
| `TEL-2026-014` | `TH-2026-015` | idempotency key、retry count、job count delta、quota counter delta | 180日 | Partial | Platform Team |

### 6.2 Detection Handoff

| Detection ID | Related Threat Hypothesis ID | Related Telemetry ID | Detection hypothesis | Test fixture | Expected result | Limitations |
|---|---|---|---|---|---|---|
| `DET-2026-011` | `TH-2026-012` | `TEL-2026-011` | `POST /api/v1/admin/report-export`が`actorRole != admin`かつ202を返した場合、Authorization driftとして検知する | 合成event chain `FIX-2026-011` | High severity alert 1件 | v1 pathの廃止後はRuleを停止または再利用が必要 |
| `DET-2026-012` | `TH-2026-013` | `TEL-2026-012` | 非admin actorが`includeInternalNotes=true`または保存後property diffを発生させた場合、Property authz gap候補として検知する | 合成event `FIX-2026-012` | Medium severity alert 1件 | field diff logが未収集だと成立しない |
| `DET-2026-013` | `TH-2026-015` | `TEL-2026-014` | 同一Idempotency-Keyでjob count deltaが2以上の場合、queue duplicationとして検知する | 合成retry sequence `FIX-2026-013` | Medium severity alert 1件 | 長期Queue蓄積の相関は別Ruleが必要 |
| `DET-2026-014` | `TH-2026-014` | `TEL-2026-013` | 内部向けHost名Webhook登録試行をaudit eventとして記録し、一定閾値で運用注意喚起する | 合成event `FIX-2026-014` | Info alert 1件 | 攻撃の成立ではなく拒否イベントの監視 |

## 7. Reassessment Plan

| Reassessment ID | Related Decision ID | Related Finding IDs | Related Detection IDs | Trigger conditions | Hypotheses to retest | Evidence to recollect | Owner | Due date |
|---|---|---|---|---|---|---|---|---|
| `REA-2026-011` | `DEC-2026-011` | `FIND-2026-011`, `FIND-2026-012`, `FIND-2026-013` | `DET-2026-011`, `DET-2026-012`, `DET-2026-013`, `DET-2026-014` | v1 endpoint停止、property filter実装、idempotency store改修、Webhook validator変更、新規Tenant 20社追加 | `TH-2026-012`, `TH-2026-013`, `TH-2026-015`, `TH-2026-014` | route inventory、property diff log、retry counter、detection test結果 | Product Security Manager | 2026-08-26 |

## 8. Traceability Check

- [x] Case ID、Decision Requirement ID、関連Case MapのDecision IDが明記されている
- [x] 各AssetにActor、Boundary、Stateの説明がある
- [x] 各Threat HypothesisにObservation Hypothesisがある
- [x] 各Threat HypothesisにValidation IDがある
- [x] 各ValidationがObservation IDへ接続し、Expected evidence、Stop、Cleanupがある
- [x] 各FindingがEvidence IDへ追跡できる
- [x] 各FindingにTelemetry IDまたはGap ownerがある
- [x] 各Detection IDがThreat HypothesisまたはTelemetry IDへ接続している
- [x] Negative FindingがCoverageとGapを持つ
- [x] EvidenceのRedaction、Classification、Access、Retention / disposal、Ownerが定義されている
- [x] Reassessment IDが`DEC-2026-011`へ接続している

## 9. Artifact Rubric

| 評価軸 | Pass条件 | この例での状態 |
|---|---|---|
| Decision alignment | 公開可否の判断に直接つながる仮説になっている | Pass |
| Boundary clarity | Tenant / function / property / server-side / idempotency境界が明示されている | Pass |
| Safe validation | 低回数、synthetic data、stop / cleanupが定義されている | Pass |
| Evidence quality | 各FindingにEvidence IDと制約がある | Pass |
| Detection handoff | Telemetry fieldとDetection hypothesisがある | Partial（`TEL-2026-012`がMissing） |
| Reassessment | Trigger、再収集証拠、Owner、Due dateがある | Pass |

## 10. 補足判断

- `TH-2026-011`はRejectedだが、「安全である」とは書かない。v2 completed stateに限定したNegative Findingである。
- `TH-2026-014`はWeakenedであり、確認した合成Host入力が拒否されdispatch taskも作成されなかったことだけを示す。別encoding、scheme、port、redirect、hostname normalization、DNS rebinding、別worker pathは未評価である。
- 主要な公開阻害要因は、Deprecated APIのFunction authz gap、Property authz gap、Retry pathのIdempotency gapである。
- 条件付き公開を選ぶなら、少なくとも`FIND-2026-011`と`FIND-2026-013`の解消と`DET-2026-011`の有効化が先行条件になる。
