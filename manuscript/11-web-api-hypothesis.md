---
title: 第11章 Web・APIを仮説駆動で評価する
description: 認証、認可、状態、データ境界、Business Logicを検証可能な仮説として設計する
---

# 第11章　Web・APIを仮説駆動で評価する

## この章の位置付け

Web ApplicationとAPIの評価は、脆弱性名の暗記やTool順の実行だけでは意思決定に接続しにくい。Checklistは観点の取りこぼしを減らすが、**どのAssetに対して、どのActorが、どのBoundaryを、どのStateで越えるのか**を説明しなければ、Finding、Telemetry、Detection、Retestへつながらない。

本章では、Web・API評価を、次の入力から組み立てる。

- Decision Requirement
- AssetとTrust Boundary
- Actor / Credential class
- State transition
- Security property
- Threat Hypothesis
- Safe Validation
- Evidence
- TelemetryとDetection Handoff
- Reassessment Trigger

目的は、脆弱性名を増やすことではない。許可された範囲で、**成立条件、否定条件、最小証拠、必要Telemetry、修正後の再評価条件**を定義し、修正可能なFindingへ変換することである。

本章は、第1章で定義した`ART-10 Integrated Security Case Map`を、第11章向けの`ART-11 Web/API Assessment Hypothesis Pack`へ具体化する。Case ID、Decision Requirement ID、Asset ID、Threat Hypothesis ID、Observation Hypothesis ID、Authority / RoE ID、Validation ID、Evidence ID、Finding ID、Telemetry ID、Detection ID、Reassessment IDの接続を、この章で固定する。

## 学習目標

- Checklistを、そのまま評価計画として使えない理由を説明できる
- AuthenticationとAuthorizationを区別し、Object / Function / Property levelの論点へ分解できる
- Session、Token、Workflow State、Tenant Boundaryを仮説へ落とせる
- Input validation、Injection、SSRF、Webhook、Async処理、Idempotency、Rate limitの論点を安全な検証へ変換できる
- Negative Testの不成立を、安全性証明と混同しないで扱える
- FindingをTelemetry RequirementとDetection Hypothesisへ接続できる
- `Web/API Assessment Hypothesis Pack`を作成できる

## 前提知識

HTTP、Cookie、Session、Token、REST / JSON APIの基本を理解していることを前提とする。OAuth 2.0、OpenID Connect、Browser Security、HTTP仕様の詳細、個別のTool操作は本章では再説明しない。

本章は、脆弱性別の再現手順集ではない。評価の問いを、許可・境界・証拠・Detectionへ接続する方法を扱う。詳細なPentest手順は既存書籍へ委譲する。

## 本章が所有する範囲

### OWN

本章が中心的に説明する。

- Web / API評価仮説の作り方
- AuthenticationとAuthorizationの切り分け
- Object / Function / Property level authorizationの整理
- Session / Token / State transitionの観点
- Business Logic abuseとNegative Testの扱い
- Safe Validation、Stop、Cleanup、Evidence最小化
- FindingからTelemetry / Detection / Retestへ渡す条件
- `ART-11 Web/API Assessment Hypothesis Pack`

### BRIDGE

本章では接続に必要な範囲を説明し、詳細は後続章または専門書へつなぐ。

- Input validationとInjectionの技術的成立条件
- Server-side trust boundaryとしてのSSRF
- OAuth / OIDC、Session管理、Browser security
- Deprecated API、Version、Inventory管理
- Async job、Webhook、Cache、Idempotencyの観測点
- Multi-tenant boundaryとData segregation

### DELEGATE

本章では詳細手順を再録しない。

- 個別Toolを用いたWeb脆弱性の検査手順
- API Endpointごとの再現コマンド集
- OAuth / OIDC / SAMLのプロトコル詳細と安全な実装
- Browser exploit、高度な攻撃Payload、回避手法
- 負荷試験、DoS再現、実運用相当の大量処理検証

詳細を学ぶ先として、次の安定URLを使用する。

- [Web脆弱性の整理](https://itdojp.github.io/pentest-learning-book/part2_web/24_common_web_vulnerabilities/)
- [APIの基礎とアタックサーフェス](https://itdojp.github.io/pentest-learning-book/part4_api/41_api_basics_and_attack_surface/)
- [典型的なAPI脆弱性](https://itdojp.github.io/pentest-learning-book/part4_api/42_common_api_vulnerabilities/)
- [OAuth 2.0 / OIDCの評価観点](https://itdojp.github.io/pentest-learning-book/part4_api/43_oauth_oidc_testing/)
- [RBAC / ABACの誤実装パターン](https://itdojp.github.io/pentest-learning-book/part4_api/44_rbac_abac_misconfig/)
- [認証・認可プロトコルの設計詳細](https://itdojp.github.io/practical-auth-book/)

## 導入ケース

架空のExample Fulfillment社は、複数Tenantに提供する受注管理SaaSを運用している。新機能として、次の二つを外部公開する予定である。

1. 受注Export API
2. 配送状態通知Webhook

経営会議の判断要求は単純ではない。

- Tenant間のData boundaryは保たれているか
- 非管理者が管理者機能を呼べないか
- Deprecated APIが新UIと違うAuthorization判定を持っていないか
- WebhookがServer-side trust boundaryを越えないか
- Async Export jobのState遷移に抜け道がないか
- もし弱点があれば、現在のTelemetryで検知または追跡できるか

この問いに対して、「OWASP Top 10を一通り確認した」「WSTGの項目を消化した」だけでは判断できない。Decision ownerが必要とするのは、**どの仮説が、どの証拠で、どの程度支持されたか**である。

## 1. Checklistを評価計画と誤解しない

OWASP Top 10やWSTGは重要な共通語彙である。しかし、それ自体は自組織のAsset、State、Boundary、Telemetryを埋めてくれない。OWASP Top 10は主にRisk communicationと優先論点の整理に、WSTGは観点の棚卸しに、OWASP API Security Top 10はAPI特有の論点整理に有用である。これらを、そのまま個別SystemのTest planとみなしてはいけない。`SRC-OWASP-TOP10-001` `SRC-WSTG-001` `SRC-API-001`

### T-11-01　ChecklistとHypothesis Packの違い

| 観点 | Checklist | Hypothesis Pack |
|---|---|---|
| 目的 | 観点の列挙 | 判断要求に必要な仮説と証拠の定義 |
| 主語 | 脆弱性カテゴリ | Asset、Actor、Boundary、State |
| 成果 | 実施済み項目一覧 | Threat / Observation / Validation / Evidence / Finding / Telemetry |
| 否定条件 | 省略されやすい | Expected denied resultとして明示 |
| 安全条件 | 別紙になりやすい | Authority、Stop、Cleanupへ内包 |
| Detection接続 | 後工程に丸投げされやすい | Telemetry ID、Detection IDで接続 |
| 再評価 | 再実施前提が曖昧 | Reassessment Triggerを定義 |

Checklistは捨てなくてよい。Hypothesis Packの観点生成器として利用する。ただし、実施済みチェックの件数を主要成果にしない。

## 2. Decision、Asset、Boundaryから仮説を起こす

Threat Hypothesisは、「脆弱性があるかもしれない」という一般論では弱い。Decision Requirement、Asset、Boundary、State、Security propertyまで落とし込んで初めて、実施価値のある仮説になる。

### F-11-01　DecisionからDetectionまでの接続

```text
Decision Requirement
    ↓
Asset / Actor / Boundary / State
    ↓
Threat Hypothesis (TH)
    ↓
Observation Hypothesis (OBS)
    ↓
Authorized Validation Plan (VAL)
    ↓
Evidence (EVD) and Negative Finding (NEG)
    ↓
Finding (FIND)
    ↓
Telemetry Requirement (TEL)
    ↓
Detection Hypothesis (DET)
    ↓
Reassessment (REA)
```

### 2.1 Threat Hypothesisの最小構成

Threat Hypothesisは、最低限次を含める。

- どのAssetか
- どのActor / Credential classか
- どのBoundaryか
- どのStateまたはWorkflow段階か
- どのSecurity propertyを評価するか
- 期待するAuthorized resultとDenied resultは何か
- 最小証拠は何か
- どこで止めるか
- どのTelemetryが必要か

弱い仮説の例:

- 「APIに認可不備がないか確認する」
- 「Webhookに問題がないか見る」
- 「Injectionできないか試す」

強い仮説の例:

- 「`ASSET-2026-011`の受注Export job取得APIでは、`tenant-blue.example`に属するAnalyst tokenが、Completed stateの他Tenant `jobId`を指定するとMetadataを取得できる可能性がある」
- 「Deprecatedな`/api/v1/admin/report-export`は、UIから到達しなくても、Analyst roleのTokenで202 AcceptedとなりJobを作成できる可能性がある」

Threat Hypothesisは、検証対象となる**望ましくない成立条件**を書く。期待するAuthorized resultとDenied resultはObservation Hypothesisへ分ける。この分離により、`Supported`が弱点の成立、`Rejected`が検証範囲での不成立を一貫して意味する。

### 2.2 ID契約

第1章Case Mapと接続するため、本章では次の識別子を最低限使う。

| 種別 | 例 | 役割 |
|---|---|---|
| Case ID | `CASE-2026-011` | 判断対象のCase単位 |
| Decision Requirement ID | `DR-2026-011` | 何をいつまでに決めるか |
| Asset ID | `ASSET-2026-011` | 対象Asset |
| Threat Hypothesis ID | `TH-2026-011` | 侵害・逸脱の仮説 |
| Observation Hypothesis ID | `OBS-2026-011` | 期待観測・反証条件 |
| Authority / RoE ID | `ROE-2026-011` | 許可、対象外、停止条件 |
| Validation ID | `VAL-2026-011` | 最小影響検証 |
| Evidence ID | `EVD-2026-011` | 収集証拠 |
| Finding ID | `FIND-2026-011` | 修正対象の結論 |
| Telemetry ID | `TEL-2026-011` | 必要な観測要件 |
| Detection ID | `DET-2026-011` | 検知仮説 |
| Reassessment ID | `REA-2026-011` | 再評価計画 |

次は、Asset、仮説、検証を具体化する補助IDである。該当する対象がある場合は省略せず、上表のIDへ接続する。

| 種別 | 例 | 役割 |
|---|---|---|
| Actor ID | `ACT-2026-011` | RoleとCredential class |
| Trust Boundary ID | `TB-2026-011` | 越境を防ぐControl |
| State ID | `STATE-2026-011` | Workflow状態と禁止遷移 |
| Surface ID | `SURF-2026-011` | Endpoint、Version、Deprecated状態 |
| Negative Finding ID | `NEG-2026-011` | 観測範囲と残存Gapを伴う不成立結果 |
| Fixture Event ID | `FIX-2026-011` | Detectionを再現する合成Event |

### 2.3 Hypothesis Statusの判定

| Status | 判定基準 |
|---|---|
| Proposed | 判断要求には接続したが、ObservationまたはValidationが未定義 |
| Testable | Authority、Observation、Validation、Stop、Cleanupが揃い実施可能 |
| Supported | 望ましくない成立条件を、許可された最小Evidenceで確認 |
| Partially supported | 仮説の一部のActor、Property、State、Versionだけが成立 |
| Weakened | 反証方向のEvidenceを得たが、Coverage Gapが残る |
| Inconclusive | Telemetry、Fixture、権限、時間の不足により支持・反証できない |
| Rejected | 定義したActor、State、Version、Time windowでは成立条件を観測しなかった。System全体の安全性は意味しない |

## 3. AuthenticationとAuthorizationを分ける

Loginに成功することと、適切な権限で適切な操作だけを行えることは違う。Web・APIの評価では、Authentication成功後のAuthorization不備、State遷移不備、Boundaryの越境が重要になる。

### 3.1 Authentication

Authenticationで問うのは、誰として扱われるか、どのCredential classか、Session / Tokenがどの文脈に束縛されるかである。

例:

- Browser sessionがTenantとRoleへ束縛されているか
- API tokenがAudience、Scope、Issuer、Expirationへ束縛されているか
- Step-up認証後のStateが、機微操作に反映されているか

ただし本章では、認証プロトコル実装そのものではなく、**認証後にどのAuthorization判断が行われるべきか**を中心に扱う。

### 3.2 Authorization

Authorizationでは、少なくとも次の三層を分ける。

#### Object level

対象Objectそのものへのアクセス可否。典型例は、別Tenantの受注、請求書、Export job、Profile、Documentへの参照である。`SRC-API-001`

#### Function level

呼び出せる機能の可否。管理者Export、Status override、Batch import、Support impersonation、Maintenance endpointなどが該当する。UI上で隠れていても、APIが残っていれば論点になる。`SRC-WSTG-001` `SRC-API-001`

#### Property level

同じObjectでも、変更・参照できる属性の範囲が違う。`discountRate`、`role`、`includeInternalNotes`、`tenantId`、`approvalState`などはProperty level authorizationの論点になる。`SRC-API-001`

### 3.3 State transition

認可不備は、単発のRequestだけでなく、State遷移で起きる。

- Draft → Approved
- Pending export → Completed
- Disabled → Active
- 未検証Webhook → 配信対象

Stateが変わる前提条件、実行者、二重送信、再試行、取消し、再開を明示しないと、Business Logicの弱点を見落としやすい。

## 4. Web / API特有の論点を仮説へ変換する

脆弱性カテゴリを、そのまま「やること一覧」にしない。境界、State、証拠、Telemetryまで含めて仮説へ変換する。

### T-11-02　論点から仮説へ変換する観点

| 論点 | 仮説化するときの問い | 最小証拠の例 | 追加Telemetry |
|---|---|---|---|
| Input validation / Injection | どの入力が、どのInterpreterやData access境界へ到達するか | 正常系と拒否系の応答差分、Safe parser error、Sanitization log | Validation error code、query template ID、exception class |
| SSRF / Server-side trust boundary | Serverが、どのURL / Host / Scheme / Port / Name resolution境界を越えるか | 登録拒否、正規化結果、dispatch queue未作成の証拠 | outbound destination normalization、deny reason |
| Business Logic abuse | 仕様上正しい見た目の操作で、どのStateや承認順序を飛ばせるか | Workflow audit、role差分、state diff | state transition actor、approval reason |
| Error / Cache | エラー時やCache hit時に別ActorのDataが返らないか | key derivation差分、response metadata、cache bypass log | cache key、tenant context、miss / hit reason |
| Async / Webhook / Idempotency | 後続処理や再試行で別Boundaryが開かないか | job queue record、delivery task record、idempotency key reuse差分 | queue name、retry chain、delivery result |
| Inventory / Version / Deprecated API | 同一機能が複数Versionで同じ認可判定を持つか | endpoint inventory、v1 / v2 response差分 | endpoint version、client ID、deprecation path |
| Multi-tenant boundary | Tenant ID、Org ID、Workspace IDがUI、API、DB、Cacheで一貫しているか | tenant mismatch拒否、cross-tenant不成立の証拠 | actor tenant、resource tenant、decision result |
| Rate / Resource consumption | 境界内の低回数操作で、QuotaやIdempotency欠落を示せるか | 少数試行でのqueue増分、quota counter差分 | rate-limit decision、job count、resource class |

### 4.1 Input validationとInjectionの位置付け

Input validationとInjectionは重要だが、単に「Payloadを投げる」ことが本質ではない。評価すべきなのは、入力がどのInterpreter、Template、ORM、検索、変換器、外部呼出し境界へ到達するかである。WSTGは観点整理に有用だが、公開本文では第三者へ転用可能な攻撃Payload集を扱わない。`SRC-WSTG-001`

Hypothesisとしては、次のように書く。

- 対象Asset
- 入力Field
- 到達する解釈境界
- 許可される文字種または構造
- 拒否時の期待挙動
- 収集すべきError / Validation evidence

### 4.2 SSRFとServer-side trust boundary

SSRFは、単に「外へ出られるか」ではなく、**ServerがClientの代わりにどこまで信頼境界を越えられるか**の問題である。Webhook、Import URL、Preview機能、Open Graph fetcher、PDF生成、画像変換、SAML metadata fetch、Outbound integrationが論点になる。`SRC-OWASP-TOP10-001` `SRC-API-001`

安全な公開本文では、実在の内部IPやMetadata Serviceへ到達させる手順を示さない。代わりに、次を評価する。

- 許可されないHost / Scheme / Portが登録時に拒否されるか
- DNS名の正規化とAllow list判定が記録されるか
- 非同期dispatch queueが作成されないか
- Rejection reasonが運用側で追跡できるか

### 4.3 Inventory、Version、Deprecated API

新UIが安全でも、古いEndpoint、Mobile用Version、Partner API、Bulk job、Internal API gateway経由の旧Pathが残っていれば、権限制御が分岐する。`SRC-API-001`

Hypothesis Packには、VersionとDeprecated状態を必ず入れる。

- 同一機能の別Pathがあるか
- UIで非表示でも直接呼べるか
- 旧VersionでRole判定やField制約が緩くないか
- 観測ログにVersionが残るか

### 4.4 Error、Cache、Async、Webhook、Idempotency

Web / APIの問題は、同期Requestだけでは完結しない。Error path、Cache key、Async worker、Webhook retry、Idempotency key、Batch import queueに論点が移る。

たとえば、同期Requestでは403でも、Async workerがQueue消費時に再認可せずに処理すれば、境界は後段で破れる。したがって、HypothesisはRequest単位ではなく、**処理チェーン単位**で設計する。

### 4.5 Rate・Resource consumptionの安全な限界

Rate limitやResource consumptionを評価したいからといって、DoSや大規模負荷試験を公開本文の標準演習にしてはいけない。`SAFETY_SCOPE.md`の範囲では、低回数・低負荷・合成Jobだけで成立条件を確認する。

安全な問いの例:

- 同一Idempotency keyで3回までの再試行でも重複Jobが増えるか
- Tenant quota counterが期待どおりに増減するか
- Queue lengthの増分が設定どおりに抑制されるか

### 4.6 Business Logic abuse

Business Logic abuseでは、単一Fieldの妥当性ではなく、**業務上許される順序、回数、組合せ、承認主体**を問う。正常な形式のRequestでも、別Roleの承認を飛ばす、同じ権利を重複利用する、取消し後に処理を再開する、価格やQuotaの整合しない組合せを作るなら、業務制約は破れている。

仮説には、開始State、許可される次State、禁止されるShortcut、必要Approval、再試行時の不変条件を記録する。証拠はData本文の大量取得ではなく、State diff、Approval record、Job count、Quota counterの最小差分に限定する。

### 4.7 Multi-tenant data boundary

Multi-tenant評価では、URLのTenant IDだけを変更して終わらない。Actor tenant、Resource tenant、Cache key、Queue message、Export object、Audit eventのTenant文脈が一貫しているかを追う。

評価対象は、同期Responseだけでなく、次を含む。

- Error responseのData量や存在推測差分
- Cache hit時のTenant key
- Async workerが再認可するときのActor / Resource tenant
- ExportやWebhook deliveryへ引き継がれるTenant context
- Detection eventに残るActor tenantとResource tenant

### 4.8 RequestからDecisionまでの観測点

### F-11-02　Request・Evidence・Telemetry・Decisionの接続

```text
Decision Requirement
        ↓
Threat / Observation Hypothesis
        ↓
Authorized Validation ── Synthetic Request / State transition
        │                           │
        │                           ├─ Response / Stored state / Queue side effect
        │                           │                 ↓
        │                           │             Evidence (EVD)
        │                           │                 ↓
        │                           │             Finding (FIND)
        │                           │
        │                           └─ Audit / Cache / Queue / Worker event
        │                                             ↓
        │                                      Telemetry (TEL)
        │                                             ↓
        └──────────────────────────────────── Detection (DET)
                                                      ↓
                                         Retest / Reassessment / Decision
```

RequestのResponseだけでは、後段のState変更やQueue投入を判断できない。Evidenceは確認事実を固定し、Telemetryは運用中に同じ逸脱を観測する契約を担う。Findingの根本原因がEvidenceだけでは確定しない場合は、確認事実と分析判断を分け、追加の設定Evidenceまたは第1章Case MapのAnalytic Judgmentへ接続する。

## 5. 良い仮説と悪い仮説

### T-11-03　良い仮説と悪い仮説

| 種別 | 例 | 問題または利点 |
|---|---|---|
| 悪い仮説 | 「BOLAがないか見る」 | Asset、Actor、Boundary、State、期待結果がない |
| 良い仮説 | 「Analyst tokenがCompleted stateの他Tenant export job metadataを取得できる可能性がある」 | 望ましくない成立条件、Object、Actor、State、Boundaryが明確 |
| 悪い仮説 | 「WebhookでSSRFできるか試す」 | 実在環境へ向かう危険があり、停止条件もない |
| 良い仮説 | 「内部向けHost名を含むcallback URLが登録され、dispatch taskが作成される可能性がある」 | 望ましくない成立条件、Server-side boundary、最小証拠、Stop pointが明確 |
| 悪い仮説 | 「重いRequestで落ちるか確認する」 | DoS誘発の危険があり、判断要求にも直結しない |
| 良い仮説 | 「同一Idempotency keyの3回再試行で、重複Jobが1件を超えて増える可能性がある」 | 望ましくない成立条件、安全な上限、期待値、証拠が明確 |

良い仮説は、成功条件よりも**停止条件**が重要である。必要証拠が取れたら止める。追加のData取得、他Tenant dataの閲覧、継続的な高負荷は成功条件にしない。

## 6. Negative TestとEvidence最小化

403、404、400、429などの拒否応答は重要なEvidenceだが、それだけでSystem全体の安全性を証明しない。拒否は、特定のActor、特定のState、特定のPath、特定のVersion、特定のTime windowで観測された結果にすぎない。

Negative Testでは、次を残す。

- どのHypothesisに対する拒否か
- どのBoundaryを確認したか
- どのFixture / synthetic actorを使ったか
- 拒否応答以外にQueue、Audit、Cache、Worker logがどうなったか
- どのCoverage gapが残るか
- 何をもって十分と判断して停止したか

Evidence最小化の原則:

1. 設定、設計、Inventoryから先に成立条件を確認する
2. 無害なRequest差分で挙動差を確認する
3. 合成Objectと合成Tenantだけを対象にする
4. 他のData取得が不要ならそこで止める
5. 追加操作が必要ならAuthority / RoEに戻る

## 7. FindingをTelemetryとDetectionへ変換する

Assessmentの価値は、報告書を出した時点では完結しない。運用で再発を検知できる形に変換して初めて、継続的な防御へ接続できる。

### 7.1 FindingからDetection Hypothesisへの変換

Findingには、少なくとも次を含める。

- Root condition
- どのActor / Role / Token classで成立したか
- どのAsset / Endpoint / Version / Stateか
- どのEvidence IDが支持するか
- どのBusiness impactがあるか
- 修正後に何をRetestするか

そこからDetection Hypothesisを作るときは、次へ翻訳する。

### T-11-04　FindingからDetectionへの変換

| Findingの要素 | Detectionで必要な要素 |
|---|---|
| Root condition | 何を異常または逸脱として捉えるか |
| Actor / Role | subject role、credential type、tenant context |
| Asset / Endpoint / Version | endpoint path、API version、service name |
| State | state before / after、workflow action |
| Evidence差分 | event fields、response code、queue mutation、audit action |
| Business impact | severity、triage priority、escalation threshold |
| Retest条件 | test fixture、expected alert、no-alert条件 |

例:

- Finding: Deprecated admin export endpointがAnalyst roleで202になる
- Detection Hypothesis: `v1/admin/report-export`に対する`actorRole != admin`の成功応答は、Configuration driftまたはAuthorization bypassの候補として検知する
- Required Telemetry: actor role、tenant、endpoint version、response code、job ID、request ID

### 7.2 Detectionに渡せないFindingは未完成である

Findingが「認可不備あり」だけで終わると、SOCやDetection Engineerは何を観測すべきか決められない。最低限、次を渡す。

- 何を成功イベントとして扱うか
- 何を拒否されるべきイベントとして扱うか
- 正常系との区別に必要なFieldは何か
- どのLog sourceで観測できるか
- どのGapがあり、誰が埋めるか

## 8. 安全な演習

演習では、[読み取り専用の合成Request / Response dataset](../cases/fixtures/ch11-web-api-assessment-dataset.json)を使用する。このDatasetはServerを起動せず、外部通信も行わない。記録済みのRequest、Response、side effect、Detection eventを比較し、Hypothesis Packを作成するための教材である。

### 課題

次の合成Datasetを読み、`Web/API Assessment Hypothesis Pack`を作成する。

### 合成Dataset

| Record ID | Asset | Actor / credential | Request or event summary | Observed result |
|---|---|---|---|---|
| `REC-11-001` | `api.orders.example /api/v2/export-jobs/JOB-blue-0007` | Analyst token / tenant-blue.example | 自Tenantの完了済みExport job metadata取得 | 200 / metadataのみ返却 |
| `REC-11-002` | `api.orders.example /api/v2/export-jobs/JOB-red-0003` | Analyst token / tenant-blue.example | 他Tenant job IDを指定 | 404 / queue accessなし |
| `REC-11-003` | `api.orders.example /api/v1/admin/report-export` | Analyst token / tenant-blue.example | Deprecated endpointへCSV export作成 | 202 / job作成あり |
| `REC-11-004` | `api.orders.example /api/v2/exports` | Analyst session / tenant-blue.example | `includeInternalNotes=true`を含むExport作成 | 202 / 応答に拒否なし |
| `REC-11-005` | `api.orders.example /api/v2/webhooks` | Admin token / tenant-blue.example | `callbackUrl=https://control-plane.service.test/internal-status`で登録 | 400 / `internal_host_denied` |
| `REC-11-006` | `api.orders.example /api/v2/exports/retry` | Analyst token / tenant-blue.example | 同一`Idempotency-Key`で3回再試行 | job countが2件増加 |

### 作業

1. Decision questionを一つ定義する
2. Asset、Actor、Boundary、Stateを整理する
3. 3つ以上のThreat Hypothesisを書く
4. 各Threat HypothesisにObservation Hypothesisを付ける
5. Validation IDごとにStop conditionとCleanupを書く
6. Evidence IDとFinding IDを接続する
7. 1つ以上のDetection Hypothesisを作る
8. 1つ以上のNegative Findingを記録する
9. Reassessment Triggerを書く

### 禁止

- 実在Service、実Tenant、実Webhook先を使わない
- 実Token、Cookie、個人情報を含めない
- 第三者Systemへ接続しない
- 大量RequestやDoS相当の検証をしない
- 他Tenant dataの取得を成功条件にしない
- 実在脆弱性の攻撃手順化を行わない

### Stop condition

次のいずれかが起きたら停止する。

- 合成環境外への通信が発生した
- 実Credentialまたは実Dataが混入した
- 低回数確認を超える追加試行が必要になった
- Cleanup不能なJobやWebhookが残る
- Authority / RoEで許可していない操作が必要になった

## 9. 作成する成果物

本章の中心成果物は`ART-11 Web/API Assessment Hypothesis Pack`である。

- [空Template](../templates/web-api-assessment-hypothesis-pack.md)
- [第11章の合成記入例](../cases/ch11-web-api-assessment-example.md)
- [第1章のCase Map](../templates/integrated-security-case-map.md)
- [Finding Report Template](../templates/finding-report.md)
- [Detection Validation Record Template](../templates/detection-validation.md)

Hypothesis Packは、Finding ReportやDetection Validation Recordを置き換えない。第11章では、Assessmentの問いを、それらへ安全に引き渡すための接続面を定義する。

### 最小完成条件

- Decision Requirementが明確である
- Asset、Actor、Boundary、Stateが定義されている
- Threat HypothesisとObservation Hypothesisが対になっている
- Authority / RoE、Stop、Cleanupがある
- 各Validationが、Expected authorized resultとExpected denied resultを持つObservation Hypothesisへ接続している
- FindingがEvidence IDへ追跡できる
- Telemetry IDとDetection IDが定義されている
- Reassessment Triggerがある

## 10. 評価基準

### 技術

- AuthenticationとAuthorizationを混同していない
- Object / Function / Property levelの論点が区別されている
- State、Version、Tenant boundaryが考慮されている
- Business Logic、Async、Webhook、Idempotencyの後段処理が考慮されている

### 安全性

- Authority / RoEが明示されている
- 実在第三者への通信を必要としない
- Stop conditionとCleanupがある
- 高負荷、横展開、大量Data取得を成功条件にしていない

### Evidence

- 何をもって支持または反証とするかが明確である
- Negative Testの不成立を安全性証明としていない
- Evidenceが最小限で、ProvenanceとLimitationがある
- Version、Endpoint、Actor contextが記録されている

### Detection接続

- Telemetry RequirementがFieldレベルで書かれている
- Detection Hypothesisが正常系との差分を持つ
- Gap ownerが明確である
- Retest条件がDetection validationへ渡せる

### 意思決定

- Decision questionに直結している
- 判断に不要な高リスク操作を排除している
- 修正、監視強化、Risk acceptance、再評価へつながる

## よくある誤解

### LoginできればAuthorizationも問題ない

違う。Authentication成功後のObject、Function、Property、Stateの判定が本質である。

### 403や404が返れば、そのカテゴリは安全である

違う。特定条件で拒否されたことを示すだけで、Version差分、Async worker、別Endpoint、別Stateは残りうる。

### Deprecated APIは利用者が少ないので後回しでよい

違う。旧PathはTelemetryやControlが薄く、Policy driftが起きやすい。

### Webhookが拒否されたならTelemetryは不要である

違う。拒否の継続監視、誤判定、Bypass試行の検知にはTelemetryが必要である。

### Rate limitの確認には高負荷試験が必須である

違う。公開本文の標準演習では、低回数・低負荷で成立条件だけを確認する。

## 章のまとめ

- Web / API評価は、Checklist完了ではなく、Decision Requirementに沿ったHypothesis Packとして設計する
- AuthenticationとAuthorizationを分け、Object / Function / Property / Stateで論点を分解する
- Input validation、SSRF、Business Logic、Async、Webhook、Idempotency、Rate limitは、Boundaryと証拠で捉える
- Negative Testの不成立を安全性証明と混同しない
- 必要なEvidenceを最小化し、Authority、Stop、Cleanupを先に定義する
- FindingはTelemetry RequirementとDetection Hypothesisへ翻訳して初めて継続的防御に接続できる
- `ART-11 Web/API Assessment Hypothesis Pack`は、第1章Case MapとFinding / Detection / Reassessmentをつなぐ

## 次に学ぶこと

第12章では、人、端末、Service Account、Workload Identityの権限関係を、Enterprise IdentityとAttack Pathの観点から評価する。

第11章で作成したHypothesis Packは、後続章で次のように展開される。

- 第12章: Identity境界と委任関係の評価
- 第14章: 最小影響Validationの設計
- 第15章: Finding ReportとRetest Record
- 第16章: Telemetry Coverage設計
- 第17章: Detection Validation Record

## 参考文献・Source Note ID

- `SRC-WSTG-001`: OWASP Web Security Testing Guide。安定版WSTG 4.2を、Web評価観点の整理に利用する。5.0開発版をStable版として扱わない
- `SRC-OWASP-TOP10-001`: OWASP Top 10:2025。Risk communicationと主要論点の整理に利用し、個別Systemの完全なTest procedureの代替とはみなさない
- `SRC-API-001`: OWASP API Security Top 10:2023。Object / Function / Property level authorization、Inventory、Multi-tenant boundaryなど、API固有の論点整理に利用する

Version、Status、確認日、次回Review日は[Source Baseline](../references/reference-baseline.md)を参照する。
