# 第4章 合成記入例：請求書連携OAuthアプリのAsset / Boundary / Threat Model

## この記入例の扱い

この文書は`Threat Model`の記入方法を示すための完全な合成例である。

- 組織名、担当者、Tenant、サービス、判断、証跡はすべて架空である。
- Domainは予約済みの`.example`と`.test`だけを使用する。
- 実Credential、Token、Cookie、顧客Data、個人情報、第三者Systemは使用しない。
- 外向き通信は行わず、合成Snapshot、無害化した設定差分、既存の監査要約だけを扱う。
- 実運用で再利用可能な攻撃手順、侵害手順、運用手順は記載しない。
- Threat Modelは主体帰属の文書ではなく、Decision、Validation、Detection、Reassessmentの接続文書として扱う。

参照する空Templateは[Threat Model](../templates/threat-model.md)である。

## 0. Document Control

| Field | Value |
|---|---|
| Artifact ID | `ART-03` |
| Threat Model ID | `TM-2026-001` |
| Parent Case ID | `CASE-2026-001` |
| Relation | `refines` |
| Decision Requirement ID | `DR-2026-001` |
| Authorization Record ID | `AUTH-CASE-2026-001` |
| Title | 請求書連携OAuthアプリのAsset / Boundary / Threat Model |
| Model status | Needs Evidence |
| Owner | Security Program Lead |
| Decision owner | Synthetic CTO Decision Owner |
| Contributors | Platform、Business Systems、SOC、CTI、Finance Operations |
| Reviewers | Synthetic Platform Reviewer、Synthetic Safety Reviewer、Synthetic SOC Reviewer、Synthetic CTO Reviewer |
| Classification | Internal |
| Created | 2026-08-06T10:00:00+09:00 |
| Updated | 2026-08-08T16:30:00+09:00 |
| Review deadline | 2026-08-19T18:00:00+09:00 |
| Reassessment date | 2026-08-20 |
| Related Issue / Ticket | `SYNTH-TM-4001` |

## 1. Decision Context

| Field | Value |
|---|---|
| Decision Requirement ID | `DR-2026-001` |
| Business process | 会計連携前の請求書集約、同期、証跡保持 |
| Decision to support | 請求書連携OAuthアプリを即時停止するか、権限縮小と監視強化で継続するか |
| Decision deadline | 2026-07-22T09:00:00+09:00 |
| In-scope environment | Synthetic Lab |
| Out-of-scope environment | Production / Third-party / Unknown |
| Scope statement | 隔離された合成Tenantのread-only設定Review、無害な合成Event、既存Audit export、summary-onlyのData説明 |
| Non-goals | 実証コード、侵害再現、外部接続、主体帰属、Production操作の許可判断 |
| Business criticality scale | High |
| Safety boundary | Synthetic-only |
| Minimum sufficient evidence standard | App設定要約、scope差分、無害化Audit summary、Coverage noteをID付きでReviewできること |
| Overcollection boundary | 実Credential、Token、Cookie、Customer Data、PIIを取得しない。外部APIへ接続しない。 |
| Reassessment trigger summary | Scope、Authorization、Identity binding、Telemetry、retentionまたはOwnerの変更 |

### Decision notes

- Inherited decision boundary: `DR-2026-001`のDecision deadline `2026-07-22T09:00:00+09:00`は、第1章で完了した判断の時点を保持する。Document Controlの`Review deadline`は`TM-2026-001`のReview期限であり、`DR-2026-001`のDecision deadlineを更新しない。第1章の`REA-2026-001`は`2026-08-21`のまま維持し、`REA-TM-2026-001`〜`004`はその判断を置換せず、後続Evidenceを収集するTrigger、Scheduled date、Closure criteriaを管理する。
- OWN boundary: Asset、Flow、Boundary、Threat Hypothesis、非OperationalなAttack Path、Evidence Requirement、Action、Reassessmentを`DR-2026-001`へ接続する。
- BRIDGE boundary: `ART-10`、`AUTH-CASE-2026-001`、Content Safety Policy 1.2.0、後続章の評価・観測・RoEへ引き渡す。
- DELEGATE boundary: 製品固有Hardening、Vulnerability固有Exploit、認証・Cloud・Network・Container実装、AI / Agent固有Modelを専門章へ委譲する。
- Explicit stop condition: Production操作、外部接続、実Data取得、未承認Target追加または実行可能な侵害手順が必要になった時点で停止する。
- Authorization dependency: `AUTH-CASE-2026-001`の`Proceed with conditions`を継承する。
- Conditional authorization: `COND-AUTH-2026-001` Production credentialを操作しない、`COND-AUTH-2026-002` 外部Networkをdefault deny、`COND-AUTH-2026-003` 想定外脆弱性発見時は停止する。
- Related artifacts: `ART-10`、`ART-13`。

### このThreat Modelがやること / やらないこと

- やること: Asset、Flow、Boundary、Exposure、Entry Point、Threat Hypothesis、Misuse Case、Control assurance、Evidence Requirement、Gap、Action、Reassessmentの接続。
- やらないこと: 実証コード、侵害再現、外部接続、主体帰属、Production操作の許可判断。
- 重要原則: `Telemetry absence is not absence of compromise`。Telemetryの不在は侵害不存在を意味しない。

### State separation

自由記述の混在を避けるため、本Caseでは状態集合を分離する。

| State family | Exact finite values | Current usage |
|---|---|---|
| Model status | `Draft / In Review / Approved for Assessment / Needs Evidence / Superseded` | 本Artifactは`Needs Evidence` |
| Knowledge state | `Unknown / Assumed / Confirmed / Not Applicable` | Asset、Boundary、Exposure、Assumptionで使用 |
| Threat hypothesis status | `Candidate / Supported / Partially Supported / Disconfirmed / Inconclusive` | `TH-2026-001`〜`006`で使用 |
| Control assurance | `Unknown / Documented / Implemented / Observed / Validated` | `CTRL-2026-005`〜`009`で使用 |
| Evidence Requirement status | `Required / Deferred / Replaced / Not Applicable` | `EREQ-2026-001`〜`004`で使用 |
| Collected Evidence status | `Planned / Collected / Rejected / Inconclusive` | FlowとCollected Evidence Registerで使用 |
| Gap status | `Open / Accepted temporarily / Escalated / Closed` | `GAP-2026-001`〜`004`で使用 |

## 2. Asset Register

本Caseでは、7種類のAsset typeを`Business Outcome / Service / Component / Data / Identity / Control Plane / Evidence`の有限集合で使い分ける。Business Assetは8番目のTypeではなく、具体的なAsset行の`Business role / outcome`へ記録する。本CaseのBusiness Assetは「請求連携能力」であり、`ASSET-2026-001`がそのService表現を担う。

| Asset ID | Type | Name | Business role / outcome | Owner | Criticality | Data classification | Knowledge state | Evidence IDs | Dependency IDs |
|---|---|---|---|---|---|---|---|---|---|
| `ASSET-2026-004` | Business Outcome | 月末請求締め | 月次収益計上と合成請求処理を4時間以内に完了する | Finance Operations | Critical | Internal | Confirmed | `EVD-2026-002` | `DEP-2026-001`, `DEP-2026-005` |
| `ASSET-2026-001` | Service | `billing-bridge.example` | Business Asset「請求連携能力」を提供する、第1章から継承した請求書Data連携Service | Business Systems | High | Confidential | Confirmed | `EVD-2026-001`, `EVD-2026-002` | `DEP-2026-001`, `DEP-2026-002` |
| `ASSET-2026-005` | Component | `billing-bridge-oauth-app.example` | App registration、consent object、credential metadataを管理する合成Component | Platform | Critical | Restricted | Confirmed | `EVD-2026-001`, `EVD-2026-003` | `DEP-2026-002`, `DEP-2026-003` |
| `ASSET-2026-006` | Data | `invoice-sync-manifest` | 実請求書本文を含まない合成の同期要約、状態、再送管理Data | Finance Data Owner | High | Confidential | Assumed | `EVD-2026-002` | `DEP-2026-005` |
| `ASSET-2026-007` | Identity | `svc-billing-bridge-sync` | 人のIdentityから分離した合成Workload identity | Platform | Critical | Restricted | Confirmed | `EVD-2026-001`, `EVD-2026-003` | `DEP-2026-003` |
| `ASSET-2026-002` | Control Plane | Synthetic Identity Cloud control plane | 第1章から継承したOAuth同意、App権限、Credential lifecycle管理面 | Platform | Critical | Restricted | Confirmed | `EVD-2026-001`, `EVD-2026-003` | `DEP-2026-004` |
| `ASSET-2026-003` | Evidence | Audit log store | 第1章から継承した同意、認証、設定変更、Export結果の証跡 | SOC | High | Internal | Confirmed | `EVD-2026-003`, `EVD-2026-004`, `NEG-2026-001` | `DEP-2026-004`, `DEP-2026-005` |

### Dependency Register

| Dependency ID | From asset | To asset | Why the dependency matters | Failure consequence |
|---|---|---|---|---|
| `DEP-2026-001` | `ASSET-2026-004` | `ASSET-2026-001` | 業務成果は連携Serviceの可用性と整合性に依存する | 月末締め遅延、手動移行コスト増加 |
| `DEP-2026-002` | `ASSET-2026-001` | `ASSET-2026-005` | ServiceはOAuth app componentを通じて許可済み権限を使う | 過大権限または同期不能 |
| `DEP-2026-003` | `ASSET-2026-005` | `ASSET-2026-007` | App componentはworkload identityのbindingに依存する | Identity misuse時の影響拡大 |
| `DEP-2026-004` | `ASSET-2026-002` | `ASSET-2026-003` | Control plane変更を証跡化できるかで検知可能性が変わる | 調査不能、再評価不能 |
| `DEP-2026-005` | `ASSET-2026-006` | `ASSET-2026-003` | Data利用の観測性が不足すると既往影響を限定できない | 影響範囲判断の不確実性 |

## 3. Flow Register

Flow typeは`Data / Identity / Control`の有限集合だけを使用する。Evidence statusは`Planned / Collected / Rejected / Inconclusive`を使用し、Knowledge stateとは分離する。

| Flow ID | Flow type | Source Asset ID | Destination Asset ID | Purpose | Protocol class | Identity / authorization context | Boundary IDs crossed | Data classification | Evidence status | Observation point |
|---|---|---|---|---|---|---|---|---|---|---|
| `FLOW-2026-001` | Control | `ASSET-2026-004` | `ASSET-2026-002` | 業務要件に基づくscope承認・変更判断 | 承認ticket、scope matrix、change workflow | Business approverとPlatform adminの二者Review | `TB-2026-009` | Internal | Collected | 承認ticket、scope差分、例外理由 |
| `FLOW-2026-002` | Identity | `ASSET-2026-002` | `ASSET-2026-005` | OAuth app componentへ許可済み権限を適用する | OAuth 2.0 app identity、consent binding | Admin consent、Conditional Access相当の制約、AUTH条件維持 | `TB-2026-001`, `TB-2026-004` | Restricted | Collected | App registration export、consent audit |
| `FLOW-2026-003` | Data | `ASSET-2026-005` | `ASSET-2026-006` | summary-onlyの請求書同期を実行する | API request / response、summary manifest read/write | `svc-billing-bridge-sync`の最小権限 | `TB-2026-008`, `TB-2026-006` | Confidential | Inconclusive | App permission export、manifest field inventory |
| `FLOW-2026-004` | Control | `ASSET-2026-002` | `ASSET-2026-003` | 同意Event・App identity lifecycle Eventの監査Coverage | Audit export、retention policy | Control plane変更の監査出力 | `TB-2026-003`, `TB-2026-007` | Internal | Inconclusive | 収集済み: `EVD-2026-003`のAdmin consent Event audit export。未収集: App identity lifecycle Event Coverage、両Event classのRule test結果 |
| `FLOW-2026-005` | Data | `ASSET-2026-003` | `ASSET-2026-004` | 月末判断に必要な観測結果を経営判断へ渡す | 無害化summary、evidence handoff | SOC reviewer roleによるread-only参照 | `TB-2026-007` | Internal | Inconclusive | hunt summary、negative finding、coverage note |
| `FLOW-2026-006` | Identity | `ASSET-2026-007` | `ASSET-2026-001` | Workload identityをruntime sessionへ結び付ける | Token issuance metadata、session binding | Workload-only、human admin禁止、Production credential禁止 | `TB-2026-004`, `TB-2026-006` | Restricted | Planned | 収集予定: post-remediation Workload identity binding snapshot、rotation手順Review記録、offline機械的突合結果 |

## 4. Trust Boundary Register

`TB-2026-001`〜`003`は第1章の意味を保ったまま継承する。Boundary typeは`Identity Authority / Data Ownership / Administrative Control / Tenant / Third-party Responsibility / Control Plane / Network`の有限集合だけを使用する。

| Boundary ID | Boundary type | From / To | Owner(s) | Trust / authority change | Crossing condition | Control | Failure consequence | Knowledge state | Evidence IDs |
|---|---|---|---|---|---|---|---|---|---|
| `TB-2026-001` | Identity Authority | 業務SaaS → Identity control plane | Business Systems、Platform | 業務SaaSのOAuth app identityがIdentity control planeの同意・権限管理へ入る | OAuth 2.0 app identity | Admin consent、scope review | 過大権限または不正な同意 | Confirmed | `EVD-2026-001`, `EVD-2026-002` |
| `TB-2026-002` | Data Ownership | OAuth app → 顧客Data API | Finance Data Owner、Platform | App権限がData ownerの許容範囲へ変換される | Workload credential | App permission、Conditional Access相当の制約 | 顧客Dataへの広範なAccess | Confirmed | `EVD-2026-001`, `EVD-2026-002` |
| `TB-2026-003` | Control Plane | Control plane → Audit log store | Platform、SOC | Control plane変更が観測可能なAudit exportへ変換される | Audit export | Export設定、保持Policy | 調査に必要なEventの欠落 | Confirmed | `EVD-2026-003`, `EVD-2026-004` |
| `TB-2026-004` | Identity Authority | Workload identity → OAuth app runtime session | Platform | Service identityの権限主体とruntime execution contextの責任主体を区別する | App componentがidentity bindingを要求 | workload binding、credential inventory、rotation plan | HumanとWorkloadの責任境界が曖昧化 | Unknown | - |
| `TB-2026-005` | Tenant | `billing-bridge.example` の合成Tenant A → 合成Tenant B | Platform、Finance Data Owner | Tenant AのIdentity / Data authorityがTenant Bへ移らないことを要求する | App bindingまたはsummary Dataが別Tenantへ関連付く条件 | Tenant ID binding、scope matrix、fail-closed停止 | Tenant間分離の不確実性と判断遅延 | Assumed | `EVD-2026-001`, `EVD-2026-002` |
| `TB-2026-006` | Network | Synthetic lab runtime → no-outbound boundary | Platform、Lab Operator | local-only評価が外部到達不能という保証へ変換される | runtime sessionやqueryが発生 | default deny、preflight check、cleanup verification | Scope外Serviceへの到達 | Assumed | `EVD-AUTH-2026-001`, `SYNTH-REV-TM-SAFE-001` |
| `TB-2026-007` | Third-party Responsibility | Vendor-managed audit behavior → SOC review and decision use | Platform、SOC、Vendor Management | Vendor管理の内部実装に対する説明責任が内部判断に持ち込まれる | query fieldやnormalization結果へ依存する | 無害化export、role separation、契約前提の確認 | Field欠落や責任境界不明で誤判定 | Unknown | `EVD-2026-003`, `NEG-2026-001` |
| `TB-2026-008` | Data Ownership | OAuth app component → invoice-sync-manifestのsummary Data面 | Finance Data Owner、Platform | App権限がsummary-only Data ownerの許容範囲へ変換される | summary-only endpointに対するread/writeが必要 | App permission、Conditional Access相当の制約、summary-only boundary | 顧客Dataや状態変更への広範なAccess | Assumed | `EVD-2026-001`, `EVD-2026-002` |
| `TB-2026-009` | Administrative Control | 業務要件とscope承認 → Identity control planeのApp設定 | Finance Operations、Platform | 業務上の要件判断が管理者同意へ変換される | scope追加または例外承認が必要 | Admin consent、scope review、二者Review | 過大権限または未承認同意 | Confirmed | `EVD-2026-001`, `EVD-2026-002` |

`TB-2026-004`のcurrent Workload identity bindingは`Unknown`であり、`EVD-2026-001`（historical scope）と`EVD-2026-003`（Admin consent Event）はこのbindingを確認するEvidenceではない。current bindingの確認は`FLOW-2026-006`の`Planned`、`GAP-2026-002`、`EREQ-2026-001`へ渡す。

## 5. Exposure and Entry Point Register

Exposureは成立条件、Entry Pointは観測対象の接点を示す。ここでの`Verification`は許可済みの合成確認に限定する。

| Exposure ID | Related Asset / Boundary / Flow IDs | Entry Point ID | Reachability class | External dependency | Required authority | Verification status | Evidence ID | Gap ID |
|---|---|---|---|---|---|---|---|---|
| `EXP-2026-001` | `ASSET-2026-002`, `ASSET-2026-005`, `TB-2026-001`, `TB-2026-004`, `TB-2026-009`, `FLOW-2026-001`, `FLOW-2026-002` | `EP-2026-001` | Isolated configuration surface | 合成App registrationとconsent object | `AUTH-CASE-2026-001`のread-only設定Review | Confirmed | `EVD-2026-001`, `EVD-2026-002` | `GAP-2026-002` |
| `EXP-2026-002` | `ASSET-2026-002`, `ASSET-2026-003`, `TB-2026-003`, `TB-2026-007`, `FLOW-2026-004`, `FLOW-2026-005` | `EP-2026-002` | Isolated evidence surface | Vendor-managed audit normalizationの説明責任 | `AUTH-CASE-2026-001`のSOC reviewer read-only access | Confirmed | `EVD-2026-003` | `GAP-2026-003` |
| `EXP-2026-003` | `ASSET-2026-005`, `ASSET-2026-006`, `ASSET-2026-007`, `TB-2026-008`, `TB-2026-005`, `TB-2026-006`, `FLOW-2026-003`, `FLOW-2026-006` | `EP-2026-003` | Synthetic offline interface | summary-only manifest fixture | `AUTH-CASE-2026-001`、no outbound、Production credential禁止 | Assumed | `EVD-2026-001`, `EVD-2026-002` | `GAP-2026-001` |

### Entry Point Detail Register

Entry PointはExposureの参照列だけで済ませず、Owner、Boundary、Authority、Observation pointを独立して定義する。

| Entry Point ID | Related Exposure IDs | Interface class | Description | Owner | Boundary IDs | Required authority | Observation point | Knowledge state | Evidence IDs |
|---|---|---|---|---|---|---|---|---|---|
| `EP-2026-001` | `EXP-2026-001` | Isolated configuration surface | 合成App registrationとconsent objectのread-only Review接点 | Platform | `TB-2026-001`, `TB-2026-004`, `TB-2026-009` | `AUTH-CASE-2026-001`のread-only設定Review | App registration export、consent audit | Confirmed | `EVD-2026-001`, `EVD-2026-002` |
| `EP-2026-002` | `EXP-2026-002` | Isolated evidence surface | 無害化したAudit exportとCoverage summaryのReview接点 | SOC | `TB-2026-003`, `TB-2026-007` | `AUTH-CASE-2026-001`のSOC reviewer read-only access | Audit export、retention設定、coverage note | Confirmed | `EVD-2026-003`, `EVD-2026-004` |
| `EP-2026-003` | `EXP-2026-003` | Synthetic offline interface | summary-only manifest fixtureとTenant binding metadataを確認予定の接点 | Platform | `TB-2026-008`, `TB-2026-005`, `TB-2026-006` | `AUTH-CASE-2026-001`、no outbound、Production credential禁止 | 収集予定: manifest field inventory、Tenant binding差分（current結果は未収集） | Assumed | `EVD-2026-001`, `EVD-2026-002` |

`EXP-2026-003` / `EP-2026-003`の`EVD-2026-001`と`EVD-2026-002`は2026-07-20のhistorical scope / requirement inputだけであり、current Tenant bindingまたはWorkload identity bindingのEvidenceではない。current Tenant binding差分、Workload identity binding snapshot、rotation手順Review記録、offline機械的突合結果は未収集であり、`FLOW-2026-006`の`Planned`、`GAP-2026-002`、`EREQ-2026-001`へ渡す。

## 6. Threat Hypothesis and Misuse Case

### Threat Hypothesis Register

`TH-2026-001`〜`003`は第1章の命題を保持する。第4章で分離した精密化は、継承IDを上書きせず、summary-only境界を`TH-2026-004`、App identity lifecycle Event / decision summary Fieldの観測を`TH-2026-005`、不正利用の機会条件とsummary-only境界までの影響範囲を`TH-2026-006`として記録する。ここでdecision summary Fieldとは、`FLOW-2026-005`でAudit Evidenceを月末判断へ渡す無害化summaryのFieldであり、Admin consent EventやRuleそのものではない。`TH-2026-002`のStatus表記は、本Artifactの有限集合へ大文字小文字だけを正規化した`Partially Supported`とし、命題の意味は変更しない。

| Hypothesis ID | Decision Requirement ID | Related Asset IDs | Boundary / Flow / Exposure IDs | Statement | Preconditions | Expected impact | Evidence needed | Alternative explanation | Priority | Hypothesis status |
|---|---|---|---|---|---|---|---|---|---|---|
| `TH-2026-001` | `DR-2026-001` | `ASSET-2026-001`, `ASSET-2026-002` | `TB-2026-001`, `TB-2026-002`, `TB-2026-004`, `FLOW-2026-002`, `FLOW-2026-006`, `EXP-2026-001` | 請求書連携アプリの業務要件超過権限、Credential misuse、顧客Dataへの広範Access可能性が同時に成立するという第1章の命題 | 過大scope、Credentialの有効性、API到達性を成立条件として評価する | 顧客Dataの閲覧・変更可能性 | `EREQ-2026-001`, `EREQ-2026-003` | 暫定scopeは残るが、Credentialの有効性またはAPI到達性が限定される可能性がある | High | Supported |
| `TH-2026-002` | `DR-2026-001` | `ASSET-2026-002`, `ASSET-2026-003` | `TB-2026-001`, `TB-2026-003`, `FLOW-2026-004`, `EXP-2026-002` | 管理者同意の変更を監視できず、未承認のscope追加を早期検知できない | 同意Eventの未収集またはRule欠落 | 攻撃面拡大の見逃し | `EREQ-2026-002` | 同意Eventは収集済みでもRule欠落により早期検知できない可能性がある | High | Partially Supported |
| `TH-2026-003` | `DR-2026-001` | `ASSET-2026-001`, `ASSET-2026-003` | `TB-2026-002`, `TB-2026-003` | 既に同型の不正利用が発生した | 過去の不正Credential利用 | 過去侵害 | `EREQ-2026-003` | TelemetryとRetentionの制約により、未観測を未発生と判断できない | High | Inconclusive |
| `TH-2026-004` | `DR-2026-001` | `ASSET-2026-001`, `ASSET-2026-005`, `ASSET-2026-006`, `ASSET-2026-007` | `TB-2026-004`, `TB-2026-008`, `TB-2026-009`, `FLOW-2026-001`, `FLOW-2026-002`, `FLOW-2026-003`, `FLOW-2026-006`, `EXP-2026-001`, `EXP-2026-003` | 業務要件を超えるscopeがsummary境界を越える影響へつながる可能性がある | 2026-07-25 remediation後のcurrent scopeとWorkload identity bindingが未確認である | 合成Dataの同期状態と業務判断への影響が拡大する | `EREQ-2026-001`, `EREQ-2026-003` | post-remediation current scopeは必要最小権限で、historical broad scopeが解消済みかもしれない | High | Inconclusive |
| `TH-2026-005` | `DR-2026-001` | `ASSET-2026-002`, `ASSET-2026-003`, `ASSET-2026-004` | `TB-2026-003`, `TB-2026-007`, `FLOW-2026-004`, `FLOW-2026-005`, `EXP-2026-002` | App identity lifecycle Eventまたはdecision summary Fieldの観測不足により、lifecycle変更と月末判断の対応付けが遅れる可能性がある | lifecycle Audit exportまたはdecision summary Fieldが不足する | Decision遅延とControl assuranceの誤判定 | `EREQ-2026-002` | Eventは存在するがsummary Field不足で見えないだけかもしれない | High | Partially Supported |
| `TH-2026-006` | `DR-2026-001` | `ASSET-2026-001`, `ASSET-2026-003`, `ASSET-2026-006` | `TB-2026-002`, `TB-2026-003`, `TB-2026-007`, `TB-2026-008`, `FLOW-2026-003`, `FLOW-2026-004`, `FLOW-2026-005`, `EXP-2026-002`, `EXP-2026-003` | historical scope、Credential metadata、API到達条件とTelemetry不足により、不正利用の機会条件と影響範囲をsummary-only境界まで限定できない可能性がある | historical scope、Credential metadata、API到達条件とTelemetry / Retention Coverageの確認が不十分である | 既往利用可能性と顧客Dataへの影響範囲の判断がInconclusiveのまま残る | `EREQ-2026-003` | 実際の不正利用は発生しておらず、Telemetry / Retention不足だけが判断をInconclusiveにしている可能性がある | High | Inconclusive |

`TH-2026-001`〜`003`の命題とstatusは第1章の評価時点を継承したsource snapshotであり、2026-08-06〜08時点のcurrent状態を自動的に表さない。特に`EVD-2026-001`は2026-07-20のhistorical scope Snapshotであり、第1章`CTRL-2026-001`が2026-07-25にscope縮小`Passed`を記録した後のcurrent scopeは、post-remediation Snapshotを収集するまで`Unknown`としてDecisionへ渡す。

### `TH-2026-002` / `TH-2026-005` Consumer Allocation

同じAudit surfaceを使うことと同じ命題であることを区別する。下表は両IDを直接参照するstructured consumerの有限mapであり、表外のstructured consumerがいずれかのIDへ暗黙にfallbackすることを認めない。

| Allocation | Consumer IDs | Meaning |
|---|---|---|
| Inherited only | `ACT-TM-2026-002` | Admin consent Event / Rule命題だけを扱う |
| Refinement only | `ACT-TM-2026-005` | App identity lifecycle Event / decision summary Field命題とlifecycle Rule testの計画・承認後実行・新Evidence ID付き結果だけを扱う |
| Both | `PATH-2026-002`, `CTRL-2026-007`, `CTRL-2026-008`, `GAP-2026-003`, `EREQ-2026-002`, `EREQ-2026-004`, `ACT-TM-2026-006`, `REA-TM-2026-002` | 共通のAudit surface、Safety gateまたは再評価単位で両命題を明示的に扱う |

### `TH-2026-003` / `TH-2026-006` Consumer Allocation

「同型の不正利用が発生したか」と「不正利用の機会条件および影響範囲をsummary-only境界まで限定できるか」を区別する。下表は両IDを直接参照するstructured consumerの有限mapであり、本表にないstructured consumerが両命題を暗黙に同一視することを認めない。

| Occurrence allocation | Consumer IDs | Meaning |
|---|---|---|
| Refinement only | `CTRL-2026-009`, `ASM-2026-002`, `GAP-2026-001`, `ACT-TM-2026-003` | summary-only Field、機会条件、影響範囲の限定可能性だけを扱い、発生有無を直接判定しない |
| Both | `PATH-2026-002`, `ASM-2026-003`, `GAP-2026-003`, `EREQ-2026-003`, `REA-TM-2026-002` | 共通のTelemetry / Retention Evidenceを使うが、発生命題と機会条件・影響範囲命題を別々に評価する |

### Misuse Case Register

Threat Hypothesisは成立条件を扱い、Misuse Caseは業務・運用上の誤用シナリオを扱う。両者を混在させない。

| Misuse Case ID | Goal | Actor capability class | Preconditions | Affected assets | Boundary crossed | Expected outcome | Observation points | Excluded operational detail |
|---|---|---|---|---|---|---|---|---|
| `MISUSE-2026-001` | 月末遅延を避けるため広いscopeを暫定維持する | 承認Workflowを扱える合成Business approverとPlatform admin | 手動Importの負荷懸念とscope見直し期限の圧迫 | `ASSET-2026-004`, `ASSET-2026-005` | `TB-2026-009` | 要件表と実設定の差分が残る | 承認ticket、scope matrix差分、例外理由 | 実Tokenを取得しない。実設定を変更しない。侵害手順を書かない。 |
| `MISUSE-2026-002` | 判断を急ぐため必要量を超えるEvidence exportを要求する | read-only EvidenceをReviewできる合成SOC role | Telemetry不足と影響範囲確定期限の接近 | `ASSET-2026-003`, `ASSET-2026-006` | `TB-2026-007` | 過剰収集要求が拒否またはEscalateされる | export request、deny reason、retention log | 実Dataをexportしない。PIIを収集しない。外部へ接続しない。 |

## 7. Attack Path Register

Attack Pathは成立しうる関係と観測点を整理する表であり、実行手順ではない。各Edgeは「何を確認すべきか」を示し、再現方法を示さない。

### Path summary

| Path ID | Related Threat IDs | Entry condition | Intermediate condition | Undesired end state | Safety note |
|---|---|---|---|---|---|
| `PATH-2026-001` | `TH-2026-001`, `TH-2026-004` | 2026-07-20のhistorical Snapshotでは要件外scopeが確認されたが、2026-07-25のscope縮小`Passed`後のcurrent scopeはpost-remediation Snapshot未収集で`Unknown`である | current App componentとworkload identityのbindingが必要scopeに収まるか未確認である | Data accessまたは状態変更の影響範囲をcurrent状態として確定できない | 実Tokenを取得しない。実Dataを参照しない。設定差分と合成metadataだけで評価する。 |
| `PATH-2026-002` | `TH-2026-002`, `TH-2026-003`, `TH-2026-005`, `TH-2026-006` | 管理者同意またはApp identity lifecycle Eventが発生する | Audit exportまたはDetection coverageが不足する | 未承認変更が長時間未発見となり、既往影響評価が遅れる | 合成Audit export、保持期間差分、Rule test結果だけで評価する |

### Attack Path edge register

| Attack Path ID | Edge ID | From Asset / State | Condition | Boundary ID | To Asset / State | Affected Asset IDs | Expected impact | Observation point | Required Evidence ID | Knowledge state |
|---|---|---|---|---|---|---|---|---|---|---|
| `PATH-2026-001` | `EDGE-2026-001` | `ASSET-2026-004` / 2026-07-20 historical scope-review | 業務要件を超えるscopeがhistorical Snapshotで確認された | `TB-2026-009` | `ASSET-2026-005` / historical broad-scope snapshot | `ASSET-2026-004`, `ASSET-2026-005` | remediation前に不要scopeが残っていた | 2026-07-20 App registration export、scope差分 | `EREQ-2026-001` | Confirmed |
| `PATH-2026-001` | `EDGE-2026-002` | `ASSET-2026-005` / post-remediation scope unknown | 2026-07-25 scope縮小`Passed`後のcurrent App registration exportが未収集で、current bindingのscopeを確認できない | `TB-2026-004` | `ASSET-2026-007` / current binding scope unknown | `ASSET-2026-005`, `ASSET-2026-007` | Identity misuse時のcurrent影響範囲を確定できない | post-remediation App registration export、Workload identity binding snapshot | `EREQ-2026-001` | Unknown |
| `PATH-2026-001` | `EDGE-2026-003` | `ASSET-2026-007` / binding active | runtime sessionがsummary-only制約と一致しない | `TB-2026-008` | `ASSET-2026-006` / summary boundary uncertain | `ASSET-2026-001`, `ASSET-2026-006`, `ASSET-2026-007` | Data accessまたは状態変更の評価が不十分になる | manifest field inventory、permission diff | `EREQ-2026-003` | Assumed |
| `PATH-2026-001` | `EDGE-2026-004` | `ASSET-2026-006` / Tenant binding assumed | Tenant bindingのEvidenceが不足する | `TB-2026-005` | `ASSET-2026-006` / Tenant isolation inconclusive | `ASSET-2026-001`, `ASSET-2026-006` | 影響範囲をTenant単位で限定できず判断が遅れる | Tenant binding差分、scope matrix | `EREQ-2026-001` | Assumed |
| `PATH-2026-002` | `EDGE-2026-005` | `ASSET-2026-002` / consent change issued | control plane変更が監査exportへ完全に反映されない | `TB-2026-003` | `ASSET-2026-003` / audit coverage partial | `ASSET-2026-002`, `ASSET-2026-003` | 未承認変更の早期検知が遅れる | Audit export、retention設定 | `EREQ-2026-002` | Confirmed |
| `PATH-2026-002` | `EDGE-2026-006` | `ASSET-2026-003` / audit coverage partial | summary exportのFieldがSOC判断に不足する | `TB-2026-007` | `ASSET-2026-004` / decision context incomplete | `ASSET-2026-003`, `ASSET-2026-004` | Coverage誤解によりDecision qualityが低下する | query result、coverage note | `EREQ-2026-002`, `EREQ-2026-003` | Unknown |
| `PATH-2026-002` | `EDGE-2026-007` | `ASSET-2026-003` / historical coverage partial | 保持不足により既往利用を十分否定できない | `TB-2026-007` | `ASSET-2026-004` / residual risk remains | `ASSET-2026-003`, `ASSET-2026-004`, `ASSET-2026-006` | 既往影響の過小評価 | negative finding、retention gap | `EREQ-2026-003` | Confirmed |

## 8. Control Assurance Register

Controlは「あるかどうか」ではなく、どのassurance stateにあるかで記録する。

| Control ID | Related Asset / Boundary / Threat / Path IDs | Control statement | Owner | Assurance state | Evidence IDs | Limitation | Gap ID | Reassessment trigger |
|---|---|---|---|---|---|---|---|---|
| `CTRL-2026-005` | `ASSET-2026-004`, `ASSET-2026-005`, `TB-2026-009`, `TH-2026-001`, `TH-2026-004`, `PATH-2026-001` | 業務要件とscopeの対応表をReviewする | Business Systems | Documented | `EVD-2026-002` | 自動突合がなく人手差分に依存する | `GAP-2026-002` | scopeまたは業務要件変更 |
| `CTRL-2026-006` | `ASSET-2026-005`, `ASSET-2026-007`, `TB-2026-004`, `TH-2026-001`, `TH-2026-004`, `PATH-2026-001` | Workload identityをHuman identityから分離しrotation手順を管理する | Platform | Documented | `EVD-2026-001` | `EVD-2026-001`はApp registration scope Snapshotに限られ、Workload identity binding snapshot、rotation手順Review記録、offline機械的突合結果は未収集である | `GAP-2026-002` | Identity bindingまたはrotation変更 |
| `CTRL-2026-007` | `ASSET-2026-002`, `ASSET-2026-003`, `TB-2026-003`, `TH-2026-002`, `TH-2026-005`, `PATH-2026-002` | Admin consentとApp identity lifecycle EventのAudit coverageを維持する | SOC | Documented | `EVD-2026-003` | `EVD-2026-003`はAdmin consent Eventだけを観測する。App identity lifecycle EventのCoverageとRule test結果は未収集であり、複合Control全体の挙動は未観測である | `GAP-2026-003` | Rule、Fieldまたはretention変更 |
| `CTRL-2026-008` | `ASSET-2026-003`, `TB-2026-006`, `TH-2026-002`, `TH-2026-005`, `PATH-2026-002` | no outbound、停止条件、Cleanupを一体で検証する | Lab Operator | Documented | `EVD-AUTH-2026-001`, `SYNTH-REV-TM-SAFE-001` | 設計とAuthorization条件はReview済みだが、preflight、default-deny、Cleanupの実施結果は未収集であり、Controlの挙動は未観測である | `GAP-2026-004` | AUTH条件、Lab boundaryまたは実施Evidence変更 |
| `CTRL-2026-009` | `ASSET-2026-006`, `TB-2026-007`, `TH-2026-006`, `PATH-2026-002` | Vendor管理のsummary-only Field normalizationを説明可能にする | Vendor Management | Unknown | `NEG-2026-001` | no outbound条件下ではVendor内部補正の完全性を直接確認しない | `GAP-2026-001` | Field仕様またはVendor責任分界変更 |

### Control IDの継承境界

- `CTRL-2026-005`は第1章`CTRL-2026-001`「必要scopeだけへ縮小」（Result: Passed）をsupportsする別Controlであり、正本Controlを置換しない。
- `CTRL-2026-006`は第1章`CTRL-2026-002`「Credential更新と旧Credential失効」（Result: Passed）をsupportsする別Controlであり、正本Controlを置換しない。
- `CTRL-2026-007`は第1章`CTRL-2026-003`「許可List外Admin consent検知」（Result: Passed）をsupportsする別Controlであり、正本Controlを置換しない。
- `CTRL-2026-008`は第4章固有のLab safety Controlであり、第1章Controlからindependentである。
- `CTRL-2026-009`は第1章`CTRL-2026-004`「API利用Telemetry追加」（Result: Partial）をsupportsする別Controlであり、正本Controlを置換しない。

`supports`は同一Controlを意味しない。第1章のControl proposition、Verification、Resultは第1章Caseを正本とし、第4章のassurance stateやEvidenceへ上書きしない。

## 9. Assumptions, Unknowns and Gaps

### Assumption Register

| Assumption ID | Statement | Owner | Validation method | Due date | Status | Related IDs |
|---|---|---|---|---|---|---|
| `ASM-2026-001` | 業務要件表は2026-08-06時点の請求書同期要件を正しく反映している | Finance Operations | 承認ticketとscope matrixの再照合 | 2026-08-12 | Assumed | `TH-2026-001`, `TH-2026-004`, `EREQ-2026-001`, `GAP-2026-002` |
| `ASM-2026-002` | 合成manifest field inventoryはsummary-only境界の最小Data集合を十分代表している | Finance Data Owner | field inventoryとmanual import要件の比較 | 2026-08-15 | Assumed | `TH-2026-004`, `TH-2026-006`, `EREQ-2026-003` |
| `ASM-2026-003` | historical summary exportの欠落期間はDecisionの優先順位を変えるほど大きくない | SOC | retention note、coverage差分、再評価時のsummary再採取 | 2026-08-20 | Assumed | `TH-2026-003`, `TH-2026-006`, `EREQ-2026-003`, `REA-TM-2026-002` |

### Gap Register

| Gap ID | Missing information / control / telemetry | Decision affected | Owner | Due date | Status | Evidence Requirement ID | Action ID | Reassessment ID |
|---|---|---|---|---|---|---|---|---|
| `GAP-2026-001` | `TH-2026-006` / `CTRL-2026-009`: API利用Telemetryのresource / operation粒度が不足する | `DR-2026-001`: 既往影響をsummary-only境界までしか限定できない | Platform | 2026-08-18 | Open | `EREQ-2026-003` | `ACT-TM-2026-003` | `REA-TM-2026-002` |
| `GAP-2026-002` | `TH-2026-001` / `TH-2026-004` / `CTRL-2026-005` / `CTRL-2026-006`: 2026-07-25 scope縮小`Passed`後のcurrent App registration export、Workload identity binding snapshot、Tenant binding差分、rotation手順Review記録、scope matrixのoffline機械的突合結果が未収集である | `DR-2026-001`: current scopeを`Confirmed`にできず、過大権限とIdentity lifecycle不整合の再発防止が人手依存になる | Business Systems | 2026-08-21 | Accepted temporarily | `EREQ-2026-001` | `ACT-TM-2026-001`, `ACT-TM-2026-004` | `REA-TM-2026-001` |
| `GAP-2026-003` | `TH-2026-002` / `TH-2026-003` / `TH-2026-005` / `TH-2026-006` / `CTRL-2026-007`: 90日窓の完全Coverageと保持証跡が不足する | `DR-2026-001`: 未観測を未発生と誤解しやすい | SOC | 2026-08-20 | Escalated | `EREQ-2026-002`, `EREQ-2026-003` | `ACT-TM-2026-002`, `ACT-TM-2026-005` | `REA-TM-2026-002` |
| `GAP-2026-004` | `CTRL-2026-008`: 合成Labのpreflight、default-deny、Cleanup実施結果が未収集である | `DR-2026-001`: 安全境界の挙動を確認できるまでLab検証を開始できない | Lab Operator | 2026-08-18 | Open | `EREQ-2026-004` | `ACT-TM-2026-006` | `REA-TM-2026-004` |

### Decision handoff summary for `DR-2026-001`

| Field | Value |
|---|---|
| Supported option | 権限縮小と監視強化で継続 |
| Confidence | 低。これは推奨の確からしさでありseverityではない。2026-07-25のhistorical scope縮小`Passed`はあるが、post-remediation current scope Snapshotが未収集で、`GAP-2026-001` / `GAP-2026-003`がOpen / Escalatedのため、再評価前の確信は限定される |
| Why not immediate unrestricted continuation | `TH-2026-001`、継承命題`TH-2026-002`、summary-only refinementの`TH-2026-004`、lifecycle / summary Field refinementの`TH-2026-005`が残る。発生有無を問う`TH-2026-003`と、機会条件およびsummary-only境界までの影響範囲を問う`TH-2026-006`はTelemetry / Retention Gapで別々に閉じていない |
| Why not direct production validation here | `AUTH-CASE-2026-001`の条件付き許可は合成Tenantのread-only評価に限定される |
| Strongest confirmed point | 2026-07-20のhistorical SnapshotではApp scopeと業務要件の差分が確認され、2026-07-25にscope縮小`Passed`が記録された |
| Strongest uncertainty | post-remediation current scope Snapshotが未収集であり、過去利用の完全追跡もできない |
| Permitted conclusion | 最小scope化、観測改善、再評価条件を付けた継続判断は支持できる |
| Prohibited conclusion | Telemetry不足のまま「侵害はなかった」「影響はゼロ」と断定すること |

## 10. Evidence Requirements and Actions

### Evidence Requirement Register

| Evidence Requirement ID | Question | Related Threat / Control / Gap | Minimum sufficient evidence | Forbidden / over-collection boundary | Owner | Due date | Status | Resulting Evidence IDs |
|---|---|---|---|---|---|---|---|---|
| `EREQ-2026-001` | 2026-07-25 remediation後のcurrent scope、Workload identity binding、Tenant binding、rotation手順は業務要件と一致するか | `TH-2026-001`, `TH-2026-004`, `CTRL-2026-005`, `CTRL-2026-006`, `GAP-2026-002` | post-remediation App registration export、要件表、scope差分表、Workload identity binding snapshot、Tenant binding差分、rotation手順Review記録、source Evidence IDを記録したWorkload-only binding check結果、source Evidence IDを記録したRotation-management check結果、Reviewer sign-off | 実Tokenを取得しない。実Dataを取得しない。Productionを変更しない。 | Platform | 2026-08-15 | Required | Historical inputs only（current resultではない）: `EVD-2026-001`, `EVD-2026-002`（いずれも2026-07-20）; New post-remediation result: current-scope snapshot、Workload identity binding snapshot、Tenant binding差分、rotation手順Review記録、offline機械的突合結果、新Evidence ID付き・source Evidence IDを記録したWorkload-only binding check結果、新Evidence ID付き・source Evidence IDを記録したRotation-management check結果、新Evidence ID付きReviewer sign-offは未収集（承認後にそれぞれ新Evidence IDを割り当てる） |
| `EREQ-2026-002` | 同意EventとApp identity lifecycle Eventの監査Coverageは十分か | `TH-2026-002`, `TH-2026-005`, `CTRL-2026-007`, `GAP-2026-003` | 合成同意Event、合成App identity lifecycle Event、Audit export、両Event classのRule test結果 | 無害化summaryを超える追加Data exportを要求しない。新Authorization Record / RoE承認前にRule testを再実施しない。 | SOC | 2026-08-18 | Required | Coverage result: `EVD-2026-003`（Admin consent Eventのみ）; App identity lifecycle EventのCoverageと両Event classのRule test結果は未収集（承認後に新Evidence IDを割り当てる） |
| `EREQ-2026-003` | 保持範囲内で既往影響をどこまで評価でき、resource / operation Field補正後にControlを検証できるか | `TH-2026-001`, `TH-2026-003`, `TH-2026-004`, `TH-2026-006`, `CTRL-2026-009`, `GAP-2026-001`, `GAP-2026-003` | 90日窓のTelemetry summary、Coverage表、negative finding、retention note、resource / operation Field contract、承認後のpost-change telemetry result | PIIを収集しない。実Tenantへ接続しない。scope外Targetを追跡しない。Production変更や実Dataが必要な工程を第4章内で実行しない。 | SOC、Platform | 2026-08-18 | Required | Historical inputs only: `EVD-2026-004`, `NEG-2026-001`; resource / operation Fieldの実装記録とpost-change telemetry resultは未収集（承認済み運用工程後に新Evidence IDを割り当てる） |
| `EREQ-2026-004` | 合成Labはno outbound、停止条件、Cleanupを実施結果で示せるか | `TH-2026-002`, `TH-2026-005`, `CTRL-2026-008`, `GAP-2026-004` | 署名済みpreflight report、default-deny dry-run結果、Cleanup verification | 新Authorization Record / RoE承認前に実行しない。実Target、実Credential、実Data、外向き通信を使用しない。 | Lab Operator | 2026-08-18 | Required | 未収集（承認後に新Evidence IDを割り当てる） |

### Evidence Requirement supplier schedule

`Requirement due`は、`Minimum sufficient evidence`を供給する全Actionが完了可能になる最終日以降に置く。表にないActionを暗黙のsupplierとして扱わず、Gapの期限は関連supplierの完了日以降、post-collection ReassessmentはRequirementとsupplierの完了日より後に置く。

| Evidence Requirement ID | Supplier Action IDs | Latest supplier completion | Requirement due | Gap IDs | Consuming Reassessment ID |
|---|---|---|---|---|---|
| `EREQ-2026-001` | `ACT-TM-2026-001`, `ACT-TM-2026-004` | 2026-08-15 | 2026-08-15 | `GAP-2026-002` | `REA-TM-2026-001` |
| `EREQ-2026-002` | `ACT-TM-2026-002`, `ACT-TM-2026-005` | 2026-08-18 | 2026-08-18 | `GAP-2026-003` | `REA-TM-2026-002` |
| `EREQ-2026-003` | `ACT-TM-2026-002`, `ACT-TM-2026-003`, `ACT-TM-2026-005` | 2026-08-18 | 2026-08-18 | `GAP-2026-001`, `GAP-2026-003` | `REA-TM-2026-002` |
| `EREQ-2026-004` | `ACT-TM-2026-006` | 2026-08-18 | 2026-08-18 | `GAP-2026-004` | `REA-TM-2026-004` |

`EVD-AUTH-2026-001`はread-only configuration reviewのAuthorization provenanceであり、Rule testを承認しない。`EREQ-2026-002`のResulting Evidenceではなく、新しいRule testには別の新Authorization Record / RoE承認が必要である。

### Collected Evidence Register

Collected Evidence statusは `Planned / Collected / Rejected / Inconclusive` の有限集合だけを使用する。Evidence Requirementの状態と混在させない。

| Evidence ID | Related Evidence Requirement IDs | Evidence description | Collection conditions / provenance | Status | Reviewer | Collected at | Limitation |
|---|---|---|---|---|---|---|---|
| `EVD-2026-001` | `EREQ-2026-001` | 現行scopeは何か | 第1章継承: App registration export; Observation `OBS-2026-001`; Validation `VAL-2026-001`; Authority / RoE `ROE-2026-001`; Integrity / hash SHA-256をEvidence manifestへ記録; Classification Internal | Collected | Not recorded in inherited source | 2026-07-20T13:20:00+09:00 | 取得時点のSnapshot |
| `EVD-2026-002` | `EREQ-2026-001` | 必要scopeは何か | 第1章継承: 業務要件とAPI仕様のReview; Observation `OBS-2026-001`; Validation `VAL-2026-001`; Authority / RoE `ROE-2026-001`; Integrity / hash Review承認記録; Classification Internal | Collected | Not recorded in inherited source | 2026-07-20T14:10:00+09:00 | 将来要件変更は含まない |
| `EVD-2026-003` | `EREQ-2026-002` | 同意Eventを観測できるか | 第1章継承: 合成Tenant audit export; Observation `OBS-2026-002`; Validation `VAL-2026-002`; Authority / RoE `ROE-2026-001`; Integrity / hash SHA-256を記録; Classification Internal | Collected | Not recorded in inherited source | 2026-07-21T10:05:00+09:00 | Production Pipelineとの差異がある |
| `EVD-2026-004` | `EREQ-2026-003` | 過去不正利用を評価できるか | 第1章継承: 90日分の無害化Log集計; Observation `OBS-2026-003`; Validation `VAL-2026-003`; Authority / RoE `ROE-2026-001`; Integrity / hash Query versionとHashを記録; Classification Confidential | Collected | Not recorded in inherited source | 2026-07-21T15:40:00+09:00 | API利用Eventの一部が未収集 |
| `EVD-AUTH-2026-001` | - | 合成Tenantを対象とした設定Review承認 | 第2章継承: Source / custodian CTO / Ticket system; Integrity / reference `SYNTH-EVD-AUTH-001` | Collected | Not recorded in inherited source | 2026-08-05T10:15:00+09:00 | Production、外部API、実Credentialを含まない |

同一Evidence IDは原典の取得時刻、取得主体、条件、制約を置換しない。第4章固有の要約をEvidenceとして保存する場合は、新しい派生IDと`Derived from`関係を割り当てる。本Caseでは派生Evidenceを作らず、原典metadataをそのまま継承する。

### Inherited Negative Finding Register

`NEG-2026-001`はCollected Evidenceではなく、第1章で定義されたNegative Findingである。原典にはstandaloneの`Collected at`がないため、時刻を創作せず、原典行をそのまま継承する。

| Negative Finding ID | Related Evidence IDs | Searched behavior | Search window | Available coverage | Gaps | Permitted conclusion |
|---|---|---|---|---|---|---|
| `NEG-2026-001` | `EVD-2026-004` | 未承認同意変更、異常なApp sign-in、Data API利用 | 過去90日 | 同意変更とsign-inは72日分。API利用は一部のみ | 18日分の保持不足、API利用Field不足 | 取得できた範囲では3つの対象Behaviorに該当するEventを確認していない。侵害不存在は断定しない |

### Negative findingの原則

- `EREQ-2026-003`が不足している場合、`確認できなかった`と`存在しない`を混同しない。
- Telemetryが欠けるときは、Caseの不備ではなく、観測系のGapとして別管理する。
- 本Caseでは「観測範囲では異常を確認していない」が許される結論であり、「侵害はなかった」は許されない結論である。

### Action Register

| Action ID | Related Gap / Control / Threat | Action | Owner | Due date | Success evidence | Status |
|---|---|---|---|---|---|---|
| `ACT-TM-2026-001` | `TH-2026-001`, `TH-2026-004`, `CTRL-2026-005`, `GAP-2026-002` | 2026-07-25 remediation後のcurrent scope Snapshot収集計画と要求、App permissionの必要最小scope案、scope matrix更新案を作成する。exportの取得と実設定変更は新Authorization Record / RoE承認後の別工程とする | Platform | 2026-08-12 | post-remediation App registration export収集要求ticket、収集計画、最小scope案、要件との差分表、新Authorization Record / RoE申請ticket（export未収集。実設定変更なし。未収集Evidenceを収集済みと扱わない） | Open |
| `ACT-TM-2026-002` | `TH-2026-002`, `CTRL-2026-007`, `GAP-2026-003` | Phase AではAdmin consent change Eventの合成Rule test計画を第17章の形式で更新し、新Authorization Record / RoE申請を作成する。Phase Bでは対象・method・time windowの承認と`ACT-TM-2026-006` Phase B-entryの新Evidence ID付き署名済みpreflight report / default-deny結果の成功を開始条件とし、no-outboundの合成LabでAdmin consent change Eventの合成Rule testを実行してDetection test結果へ新Evidence IDを割り当て、query version、Coverageとともに`REA-TM-2026-002`へ供給する。両Event classのRule test終了または停止後は`ACT-TM-2026-006` Phase CのCleanup verificationを完了するまで本Actionを完了扱いにしない。entry gate失敗、外向き通信、実Target、実Credential、実Dataが必要な場合は開始しない | SOC | 2026-08-18 | Phase A: consent Rule test計画、新Authorization Record / RoE申請ticket。Phase B: approval ticket、承認済みの新Authorization Record / RoE、`ACT-TM-2026-006` Phase B-entryの新Evidence ID付き署名済みpreflight report / default-deny結果、新Evidence ID付きAdmin consent Detection test結果、query version、Coverage、Phase Cの新Evidence ID付きCleanup verification、`REA-TM-2026-002`への供給。Phase B / C未実施の間は結果未収集 | Open |
| `ACT-TM-2026-003` | `TH-2026-006`, `CTRL-2026-009`, `GAP-2026-001` | Phase AではAPI利用Telemetryのresource / operation Field contract、合成sample summary、change proposal、新Authorization Record / change approval申請を作成する。Phase Bでは対象・method・time window・実施Ownerを新Authorization Record / change approvalで承認した後に限り、Field実装とpost-change collectionを承認済み運用工程へhandoffする。第4章内ではProduction Pipelineを変更せず実Dataを収集しない。承認済み運用工程は最小十分なField境界でresource / operation Fieldを実装し、合成probeを用いたpost-change telemetry resultを収集して新Evidence IDを割り当て、query / version、Coverage、retention、review sign-offとともに`REA-TM-2026-002`へ供給する。未承認、過剰収集、scope外変更が必要な場合は停止する | Platform、Vendor Management | 2026-08-18 | Phase A: Field contract、合成sample summary、change proposal、新Authorization Record / change approval申請ticket（Production変更なし）。Phase B: approval ticket、承認済みの新Authorization Record / change approval、実装記録、新Evidence ID付きpost-change API telemetry result、query / version、resource / operation Coverage、retention note、review sign-off、`REA-TM-2026-002`への供給。Phase B未実施の間はpost-change result未収集 | Open |
| `ACT-TM-2026-004` | `TH-2026-001`, `TH-2026-004`, `CTRL-2026-005`, `CTRL-2026-006`, `GAP-2026-002` | Phase Aでは合成Tenant bindingのBoundary owner、停止条件、fallback判断、rotation手順Review fieldをscope matrixへ構造化し、収集計画と新Authorization Record / RoE申請を作成する。Phase Bでは対象・method・time windowを新Authorization Record / RoEで承認した後に限り、合成Tenantのread-only configuration exportとしてpost-remediation App registration export、Workload identity binding snapshot、Tenant binding snapshot、rotation手順Review記録を収集し、新Evidence IDを割り当ててoffline機械的突合を行う。Platformはsource Evidence IDをWorkload-only binding check結果とRotation-management check結果へ記録し、Identity Assurance Reviewerは有限閾値に対するresultとlimitationをsign-offする。両check結果とReviewer sign-offへ別々の新Evidence IDを割り当てて`REA-TM-2026-001`へ供給する。承認前、live Tenant、実Credential、実Dataが必要な場合は停止する | Platform、Finance Operations | 2026-08-15 | Phase A: 更新scope matrix、収集計画、新Authorization Record / RoE申請ticket、承認runbook。Phase B: approval ticket、承認済みの新Authorization Record / RoE、新Evidence ID付きpost-remediation App registration export、Workload identity binding snapshot、Tenant binding snapshot、rotation手順Review記録、Tenant binding差分、offline機械的突合結果、新Evidence ID付き・source Evidence IDを記録したWorkload-only binding check結果、新Evidence ID付き・source Evidence IDを記録したRotation-management check結果、新Evidence ID付きIdentity Assurance Reviewer sign-off、`REA-TM-2026-001`への供給。Phase B未実施の間は未収集 | Open |
| `ACT-TM-2026-005` | `TH-2026-005`, `CTRL-2026-007`, `GAP-2026-003` | Phase AではSOC query申請templateへApp identity lifecycle Eventとdecision summary FieldのCoverage、90日retention証跡の必須Field、欠損時のdeny条件を文書化し、App identity lifecycle Eventの合成Rule test計画と新Authorization Record / RoE申請を作成する。Phase Bでは対象・method・time windowの承認と`ACT-TM-2026-006` Phase B-entryの新Evidence ID付き署名済みpreflight report / default-deny結果の成功を開始条件とし、no-outboundの合成LabでApp identity lifecycle Eventの合成Rule testを実行し、Detection test結果を収集して新Evidence IDを割り当て、query version、Coverage、90日retention証跡、review sign-offとともに`REA-TM-2026-002`へ供給する。Admin consent change Event側は`ACT-TM-2026-002`が扱い、本ActionはApp identity lifecycle Event側だけを扱う。両Event classのRule test終了または停止後は`ACT-TM-2026-006` Phase CのCleanup verificationを完了するまで本Actionを完了扱いにしない。entry gate失敗、外向き通信、実Target、実Credential、実Data、Production変更が必要な場合は開始または継続しない | SOC | 2026-08-18 | Phase A: query approval template、lifecycle Rule test計画、新Authorization Record / RoE申請ticket、Coverage表、retention record、deny例。Phase B: approval ticket、承認済みの新Authorization Record / RoE、`ACT-TM-2026-006` Phase B-entryの新Evidence ID付き署名済みpreflight report / default-deny結果、新Evidence ID付きApp identity lifecycle Event Detection test結果、query version、Coverage表、retention record、review sign-off、Phase Cの新Evidence ID付きCleanup verification、`REA-TM-2026-002`への供給。Phase B / C未実施の間はApp identity lifecycle EventのDetection test結果とCleanup結果は未収集 | Open |
| `ACT-TM-2026-006` | `TH-2026-002`, `TH-2026-005`, `CTRL-2026-008`, `GAP-2026-004` | Phase Aでは合成Labのpreflight、default-deny、Cleanup実施計画と新Authorization Record / RoE申請を作成する。Phase B-entryでは対象・method・time windowを承認した後、`ACT-TM-2026-002` / `ACT-TM-2026-005`のRule test開始前に署名済みpreflightとdefault-deny検証を実行し、成功結果へ新Evidence IDを割り当ててentry Evidenceとして供給する。失敗時はRule testを開始しない。Phase Cでは両Event classのRule test終了または停止直後にCleanup verificationを実行し、新Evidence IDを割り当てて`REA-TM-2026-004`へ供給する。外向き通信、実Target、実Credential、実Data、Production変更が必要な場合は開始または継続しない | Lab Operator | 2026-08-18 | Phase A: Lab実施計画、新Authorization Record / RoE申請ticket。Phase B-entry: approval ticket、承認済みの新Authorization Record / RoE、新Evidence ID付き署名済みpreflight report / default-deny結果、entry-gate sign-off。Phase C: 新Evidence ID付きCleanup verification、`REA-TM-2026-004`への供給。各Phase未実施の間はpreflight / default-deny / Cleanup結果未収集 | Open |

### 合成Lab Rule testの実行順序

日付の前後だけに依存せず、次の有限順序で`ACT-TM-2026-002` / `005` / `006`を実行する。前段のexit evidenceがない場合は次段へ進まない。

| Sequence | Owner Action | Entry gate | Operation / scope | Exit evidence / consumer |
|---|---|---|---|---|
| 1. Safety entry | `ACT-TM-2026-006` Phase B-entry | 対象・method・time windowを承認した新Authorization Record / RoE | Rule test前にno-outbound合成Labのpreflightとdefault-denyを検証する。失敗時は開始しない | 新Evidence ID付き署名済みpreflight report / default-deny結果を`ACT-TM-2026-002` / `005`へ供給 |
| 2. Event-class tests | `ACT-TM-2026-002` / `ACT-TM-2026-005` Phase B | Sequence 1の両Evidenceが成功しentry-gate sign-offがある | Admin consentとApp identity lifecycleを別の合成Rule testとして実行する | 各Detection test結果へ新Evidence IDを割り当て`REA-TM-2026-002`へ供給 |
| 3. Cleanup | `ACT-TM-2026-006` Phase C | Sequence 2が終了または停止した | 直後にCleanup verificationを実行する。失敗時は完了扱いにせずEscalateする | 新Evidence ID付きCleanup verificationを`REA-TM-2026-004`へ供給 |
| 4. Separate closure | `REA-TM-2026-002` / `REA-TM-2026-004` | Sequence 1〜3の対応Evidenceがある | Detection assuranceとLab-safety assuranceを別々に評価する | `CTRL-2026-007`と`CTRL-2026-008`をEvidence範囲内で別々に更新する |

## 11. Reassessment and Handoff

### `REA-TM-2026-001`のIdentity assurance判定閾値

- `Workload-only binding check: Passed`は、Workload identity binding snapshotとTenant binding差分に記録されたactive bindingのHuman identityが0件で、すべてが承認済みWorkload identity、Owner、Tenant、scope matrixへ一致する場合だけ記録する。不一致、分類不能または未収集は`Failed / Inconclusive / Not collected`とする。
- `Rotation-management check: Passed`は、rotation手順Review記録にOwner、review interval / trigger、last review result、next review date、exception / failure escalationがあり、未管理または期限超過のactive bindingが0件である場合だけ記録する。欠落、不合格または未収集は`Failed / Inconclusive / Not collected`とする。
- `CTRL-2026-006`は両checkが`Passed`で、対応する新Evidence IDとReviewer sign-offがそろう場合だけ`Observed`へ進める。どちらか一方でも`Failed / Inconclusive / Not collected`なら`Documented`に維持し、`GAP-2026-002`を閉じない。`CTRL-2026-005`のscope判定はこのIdentity判定と分離する。

### Reassessment Register

| Reassessment ID | Trigger | Scope | Owner | Scheduled date | Inputs required | Closure criteria | Destination chapter / artifact |
|---|---|---|---|---|---|---|---|
| `REA-TM-2026-001` | scope、Identity binding、rotationまたは承認ticket変更 | `TH-2026-001`, `TH-2026-004`, `CTRL-2026-005`, `CTRL-2026-006`, `GAP-2026-002` | Platform | 2026-08-19 | 2026-07-25 remediation後のApp registration export、scope matrix、Tenant binding差分、Workload identity binding snapshot、rotation手順Review記録、新Evidence ID付き・source Evidence IDを記録したWorkload-only binding check結果、新Evidence ID付き・source Evidence IDを記録したRotation-management check結果、新Evidence ID付きReviewer sign-off、approval ticket、新Authorization Record / RoE | post-remediation current scopeがEvidenceで`Confirmed`となり、最小scope案と要件の差分がゼロである。新Authorization Record / RoE承認後にのみ変更し、scope条件が満たされた場合だけ`CTRL-2026-005`を少なくともImplementedとする。`Workload-only binding check`と`Rotation-management check`の両方が`Passed`で、新Evidence ID付き・source Evidence IDを記録した各check結果と新Evidence ID付きReviewer sign-offがそろう場合だけ`CTRL-2026-006`を少なくともObservedとする。どちらかが`Failed / Inconclusive / Not collected`なら`CTRL-2026-006`を`Documented`に維持し、`GAP-2026-002`を閉じない | 第15章 `Finding Report` / `Retest Record` |
| `REA-TM-2026-002` | Rule導入、Field追加、retention変更 | `TH-2026-002`, `TH-2026-003`, `TH-2026-005`, `TH-2026-006`, `CTRL-2026-007`, `CTRL-2026-009` | SOC、Platform、Vendor Management | 2026-08-20 | Admin consent EventとApp identity lifecycle EventのAudit export、Rule test計画、新Authorization Record / RoE、両Event classのDetection test結果、query version、coverage表、retention note、Field contract、合成sample summary、change proposal、Telemetry Field change approval、Field実装記録、新Evidence ID付きpost-change API telemetry result、resource / operation Coverage、review sign-off | 新Authorization Record / RoE承認後にのみ両Event classの合成Rule testを再実施し、Detection test結果に新Evidence IDを割り当てる。両Event classのEvidenceで`CTRL-2026-007`をValidatedとする。API telemetryは新Authorization Record / change approval後の承認済み運用工程でのみ変更・収集し、post-change Evidenceがrequired API Eventのresource / operation Field、Coverage、retention、過剰収集なしを示す場合に限り`CTRL-2026-009`を承認scope内でValidatedとし`GAP-2026-001`を閉じる。`CTRL-2026-007`のEvidenceを`CTRL-2026-009`へ流用しない。`TH-2026-003`の発生有無と`TH-2026-006`の機会条件・影響範囲は同じEvidenceから別々に再評価する。未達時は各Gap ownerと期限を更新する | 第6章 観測設計、第17章 Detection Validation |
| `REA-TM-2026-003` | AUTH条件変更、Target追加、Production操作要請 | 全仮説、全Boundary、全Exposure | Security Program Lead | 条件発生時に即時 | 新Authorization Record、更新Scope、RoE案 | `AUTH-CASE-2026-001`からの逸脱が閉じ、新条件で再承認済み | 第9章 `Rules of Engagement` |
| `REA-TM-2026-004` | 新Authorization / RoE承認、Lab boundary変更、preflight / default-deny / Cleanup結果収集 | `CTRL-2026-008`, `GAP-2026-004`, `EREQ-2026-004` | Synthetic Safety Reviewer | 2026-08-19 | 新Authorization Record、RoE、Rule test開始前の新Evidence ID付き署名済みpreflight report / default-deny結果、Rule test終了または停止後の新Evidence ID付きCleanup verification | preflight / default-denyがRule test開始前に成功し、終了または停止直後のCleanup verificationを含む全結果が収集された場合に限り`CTRL-2026-008`を少なくともObservedとする。失敗時は検証を開始または継続せず、完了扱いにしない | 第2章 `Authorization Checklist` / 第9章 `Rules of Engagement` |

### 再承認が必要な変更

- Production Tenant、実Credential、実Customer Data、外部API callを追加する場合。
- 合成TenantであってもApp permission、consent、Identity bindingなどの設定変更を行う場合。
- RoEのmethod / time windowを越えて合成Rule testを再実施する場合。
- post-remediation configuration / identity binding Snapshotを収集し、新Evidence IDを割り当てる場合。
- Telemetryの収集設定またはProduction Pipelineを変更する場合。
- 追加Boundaryを越えるValidationが必要になった場合。
- 想定外脆弱性を発見し、Disclosure routeを実運用へ接続する場合。

### Handoff Contracts to Later Chapters

| Handoff ID | Target chapter | Deliverable / consumer | What this artifact provides | Acceptance criteria | Reject / return condition |
|---|---|---|---|---|---|
| `HO-TM-2026-005` | 第5章 ATT&CK | Behavior記述 | `TH-2026-001`〜`006`の成立条件、Flow、Boundary、Exposure、観測点 | Technique名ではなく行動条件へ落とせる | Campaign名や主体帰属だけで具体性がない |
| `HO-TM-2026-006` | 第6章 観測可能性 | Telemetry / logging設計 | `CTRL-2026-007` / `CTRL-2026-009`、`EREQ-2026-001`〜`004`、`GAP-2026-001`〜`004`、Negative finding原則 | Field、retention、coverage、Lab safety Evidence、Gap ownerがある | 「ログを増やす」だけでField contractがない |
| `HO-TM-2026-009` | 第9章 RoE | Rules of Engagement | `CTRL-2026-008`、`AUTH-CASE-2026-001`継承条件、`ACT-TM-2026-001` / `ACT-TM-2026-002` / `ACT-TM-2026-003` / `ACT-TM-2026-004` / `ACT-TM-2026-005` / `ACT-TM-2026-006`の再Authorization依存、停止条件、no outbound、対象外一覧 | Allowed / prohibited / stop / cleanupと設定変更・Snapshot収集・Rule test・Telemetry変更・Lab実行の再Authorization gateが明示される | Production操作、外部通信、期限外Rule testまたは未承認の設定変更・Snapshot収集が紛れ込む |
| `HO-TM-2026-011` | 第11章 Web/API評価 | Web/API Assessment Hypothesis Pack | `CTRL-2026-005`、`TH-2026-001` / `TH-2026-004`、`TB-2026-002` / `TB-2026-008`、`FLOW-2026-003`、`PATH-2026-001` | Entry point、state、property境界へ変換できる | endpointやstateが曖昧 |
| `HO-TM-2026-012` | 第12章 Identity評価 | Identity Attack Path Review | `CTRL-2026-006`、`ASSET-2026-007`、`TB-2026-004`、`FLOW-2026-002`、`FLOW-2026-006` | 人・サービス・workloadの委任関係が追跡できる | 人とworkload identityが混在したまま |
| `HO-TM-2026-013` | 第13章 Platform / Supply Chain | Platform and Supply Chain Assessment | `CTRL-2026-006`、`ASSET-2026-002`、`ASSET-2026-005`、Credential lifecycle、control plane依存 | Control planeとruntimeの境界が整理される | SaaS連携の境界が説明不能 |
| `HO-TM-2026-014` | 第14章 最小影響Validation | Minimal-Impact Validation Record | `CTRL-2026-008`、`EREQ-2026-001`〜`004`、特に`EREQ-2026-004`のpreflight / default-deny / Cleanup証拠、禁止操作、stop条件、fallback | 最小証拠、再Authorization、停止、Cleanupが一致する | 証拠のためにData取得または未承認実行を要求する |
| `HO-TM-2026-015` | 第15章 Finding / Retest | Finding Report、Retest Record | `CTRL-2026-005` / `CTRL-2026-006` / `CTRL-2026-007` / `CTRL-2026-008` / `CTRL-2026-009`、`GAP-2026-001`〜`004`、`ACT-TM-2026-001`〜`006`、`REA-TM-2026-001`〜`004` | 根本原因、暫定対策、恒久対策、再Authorization、再評価が追跡できる | 影響、Owner、再テスト条件またはAuthorization gateがない |
| `HO-TM-2026-027` | 第27章 AI / Agent固有Threat Model | AI / Agent Threat Model拡張 | 本CaseではN/A。AI / Agent component追加時に再利用するAsset、Flow、Boundary、Threat、Gap ID | AI / Agent固有Surfaceを既存IDへ接続し、本章の一般Modelを置換しない | AI / Agent固有論点を一般Threat Modelだけで完了扱いにする |

### Handoff interpretation

以下は上表のHandoffを読解するための焦点であり、入力の完全列挙ではない。各後続章へ渡す正確な全入力は、上表の`What this artifact provides`を正本とする。

- 第5章では、継承命題`TH-2026-001`〜`003`、summary-only refinement `TH-2026-004`、lifecycle / summary Field refinement `TH-2026-005`、機会条件・影響範囲 refinement `TH-2026-006`を区別してATT&CKの行動言語へ変換する。
- 第6章では、`CTRL-2026-007` / `CTRL-2026-009`、`EREQ-2026-003` / `EREQ-2026-004`を主要な観測入力とする。上表の正本どおり`EREQ-2026-001`〜`004`と`GAP-2026-001`〜`004`を併記して渡すのは、観測点をDecision、scope、Identity contextから切り離さないためである。
- 第9章では、Lab safetyの`CTRL-2026-008`、`AUTH-CASE-2026-001`継承条件と`ACT-TM-2026-001` / `ACT-TM-2026-002` / `ACT-TM-2026-003` / `ACT-TM-2026-004` / `ACT-TM-2026-005` / `ACT-TM-2026-006`の再Authorization依存をRoEへ具体化する。
- 第11章では、scope assuranceの`CTRL-2026-005`、継承命題`TH-2026-001`とsummary-only refinement `TH-2026-004`、継承した`TB-2026-002`とsummary-only refinementの`TB-2026-008`、`PATH-2026-001`をWeb/APIの仮説パックへ分解する。
- 第12章では、Identity assuranceの`CTRL-2026-006`、`ASSET-2026-007`と`TB-2026-004`をIdentity attack pathとして再評価する。
- 第13章では、`CTRL-2026-006`、`ASSET-2026-002`と`ASSET-2026-005`のcontrol plane依存をPlatform評価へ渡す。
- 第14章では、Lab safetyの`CTRL-2026-008`と`EREQ-2026-004`を含む最小影響で必要Evidenceだけを集めるValidation設計へ接続する。
- 第15章では、`CTRL-2026-005`〜`009`と`GAP-2026-004`を含むGapをFinding、Action、Retest、Residual riskへ変換する。

## 12. Review and Rubric

### Traceability Check

- [x] `TM-2026-001`が`CASE-2026-001`を`refines`している
- [x] `DR-2026-001`への意思決定支援目的が明示されている
- [x] `AUTH-CASE-2026-001`の条件付き許可を拡張せず継承している
- [x] 7種類のAsset typeがすべて登場する
- [x] `Data / Identity / Control`の全Flow typeが登場する
- [x] 5種類以上のBoundary typeが登場する
- [x] `EXP-2026-001`〜`003`と`EP-2026-001`〜`003`がある
- [x] `TH-2026-001`〜`003`を第1章の意味を保って再利用し、summary-only refinementを`TH-2026-004`、lifecycle / summary Field refinementを`TH-2026-005`、機会条件・影響範囲 refinementを`TH-2026-006`へ分離している
- [x] Misuse CaseとThreat Hypothesisを分離している
- [x] `PATH-2026-001`〜`002`とEdge tableがある
- [x] 5つのControlがassurance stateで管理されている
- [x] 4つのEvidence Requirementがある
- [x] 3つのAssumptionと4つのGapがある
- [x] Telemetry不足を侵害不存在と混同しない原則を明示している
- [x] Action、Reassessment、後続章へのHandoffがある

### Artifact Rubric

このRubricは、Threat Modelの完成度ではなく、後続判断へ安全に引き渡せるかを評価する。

| Rubric ID | Criterion | Meets | Partially meets | Does not meet |
|---|---|---|---|---|
| `RUBRIC-TM-2026-001` | Asset taxonomy | 7種類のAsset typeが区別され、Decisionとの関係が説明される | Assetはあるがtypeが混在する | Assetが列挙だけで終わる |
| `RUBRIC-TM-2026-002` | Boundary and flow clarity | Flow typeとBoundary typeが固定語彙で追跡できる | 一部は追跡できるが型が曖昧 | FlowとBoundaryが混同される |
| `RUBRIC-TM-2026-003` | Threat usefulness | Hypothesisが成立条件、Exposure、Evidence requirementへ接続する | HypothesisはあるがEvidenceや影響が弱い | 抽象的な脅威列挙に留まる |
| `RUBRIC-TM-2026-004` | Safety and authorization | AUTH条件、禁止操作、再承認Triggerが保たれる | 条件はあるが逸脱時の扱いが弱い | Authorization境界を拡張している |
| `RUBRIC-TM-2026-005` | Decision handoff quality | Action、Gap、Reassessment、Chapter handoffが具体的 | 一部具体だがOwnerや期限が不足 | 後続章が何を受け取るか不明 |

### Review Record

以下は合成Case内のReview記入例であり、実際のRepository gateや運用承認の証跡ではない。

| Review area | Reviewer / role | Rubric | Result | Date | Evidence reference | Notes |
|---|---|---|---|---|---|---|
| Technical correctness | Synthetic Platform Reviewer | `RUBRIC-TM-2026-001`〜`003` | Pass | 2026-08-08 | `SYNTH-REV-TM-TECH-001` | Asset type、Boundary、Threat接続を確認 |
| Safety / authorization | Synthetic Safety Reviewer | `RUBRIC-TM-2026-004` | Pass | 2026-08-08 | `SYNTH-REV-TM-SAFE-001` | `AUTH-CASE-2026-001`の条件を拡張していない |
| Evidence / telemetry quality | Synthetic SOC Reviewer | `RUBRIC-TM-2026-003`、`005` | Pass | 2026-08-08 | `SYNTH-REV-TM-EVD-001` | Negative findingとGapの分離を確認 |
| Decision usefulness | Synthetic CTO Reviewer | `RUBRIC-TM-2026-005` | Pass | 2026-08-08 | `SYNTH-REV-TM-DEC-001` | 継続判断、停止条件、再評価条件が明確 |

### Limitations

- 本文は合成Caseであり、Vendor固有仕様や実Tenantの例外実装を代表しない。
- `TH-2026-001`は第1章の顧客Data Access命題を保持し、summary-only境界だけの精密化は`TH-2026-004`へ分離する。両IDを同一命題として集計しない。
- `TH-2026-002`は第1章の同意Event / Rule命題を保持し、App identity lifecycle Event / decision summary Fieldの精密化は`TH-2026-005`へ分離する。両IDのconsumerは「継承のみ / refinementのみ / 両方」の有限mapで管理し、同一命題としてjoinしない。
- `TH-2026-003`は第1章の「既に同型の不正利用が発生した」という命題を維持する。TelemetryとRetentionの制約により`Inconclusive`であり、既往影響の不存在証明には使えない。
- `TH-2026-006`は機会条件とsummary-only境界までの影響範囲を扱い、`TH-2026-003`の発生有無を代替しない。両IDを同一命題としてjoinしない。
- `CTRL-2026-009`は`Unknown`であり、Controlの不存在を意味しない。AUTH条件とno outboundの範囲では直接確認しないだけである。
- `ASSET-2026-006`と`FLOW-2026-003`の一部はsummary-onlyの構造前提に基づく`Assumed`であり、実Data取得を伴わずに扱う。
- Attack Pathは関係と観測点の説明であり、侵害手順、Tool選定、実行手順、再現レシピではない。
- 本Threat Modelだけで第15章のFinding確定やRisk受容を代替しない。後続章のValidation、Detection、Retestが必要である。
