---
title: 第4章 資産、信頼境界、攻撃面、脅威モデル
description: 判断要求から資産、境界、露出、脅威仮説、証拠要件、再評価までを追跡可能に整理する
---
# 第4章 資産、信頼境界、攻撃面、脅威モデル
## この章の位置付け
第1章で定義した`Decision Requirement`とCase中心の追跡性は、そのままでは評価計画にならない。 何を守るのか、誰が責任を持つのか、どこで越境が起きるのか、何が外部へ露出しているのかを明確にしなければ、後続の評価、検知、改善、再評価はすべて場当たり的になる。

本章は、`ART-03 Threat Model`を使って、判断要求を次の順で構造化する。

```text
Decision Requirement
→ Business Outcome / Asset
→ Owner / Criticality / Data Classification
→ Data / Identity / Control Flow
→ Trust Boundary
→ Exposure / Entry Point
→ Threat Hypothesis / Misuse Case
→ Attack Path
→ Existing Control / Assumption / Gap
→ Evidence Requirement / Action / Reassessment
```

この章の役割は、脅威を大量に列挙することではない。 判断に必要な資産、境界、露出、仮説、証拠要件を、後続章へ引き渡せる形へ正規化することである。

本章は単独でも読めるように書いている。 ただし、ここで作るThreat Modelは終点ではなく、Chapter 5以降の評価、観測、改修、再評価へ接続されて初めて業務上の意味を持つ。

NIST CSF 2.0は成果指向であり、特定の単一手法を強制しない非処方的な枠組みである。 したがって、本章のThreat Modelも、CSFへの対応付け自体を完成証明には使わない。`SRC-CSF-001`

NIST SP 800-30 Rev.1は、Threat source、Threat event、Vulnerability、Predisposing condition、不確実性を区別してRisk assessmentを構造化する参考になる。
一方で、連邦機関向けに整理された評価指針を、そのまま普遍的な必須手順や数値判定Gateとして扱わない。`SRC-NIST-RISK-001`

OWASP Threat Modeling Projectは、特定の単一Methodや単一Toolを正本としない、方法論中立の継続保守ガイドである。 本章も同じ立場を取り、図、Threat count、Tool出力を完全性の証拠には使わない。`SRC-OWASP-TM-001`
## 学習目標
この章を終えると、次を実行できる。
- `Business Outcome`と`Business Asset`を区別できる
- `Service`、`Component`、`Data Asset`、`Identity`、`Control Plane`、`Evidence Asset`を混同せずに記述できる
- `Data Flow`、`Identity Flow`、`Control Flow`を分離して書ける
- `Trust Boundary`と`Network Segment`の違いを説明できる
- `Attack Surface`、`Exposure`、`Entry Point`を分けて記録できる
- `Threat`、`Vulnerability`、`Finding`の違いを説明できる
- `Threat Hypothesis`と`Misuse Case`を区別して作成できる
- `Attack Path`を、実行可能な侵害手順へ変えずに表現できる
- `Confirmed`、`Assumed`、`Unknown`、`Not Applicable`を適切に使い分けられる
- `Control Documented`、`Implemented`、`Observed`、`Validated`、`Unknown`を分離して記録できる
- `Evidence Requirement`と`Collected Evidence`を区別できる
- Chapter 5、6、9、11〜15、27へ引き渡せる`ART-03 Threat Model`を作成できる
## 前提知識
第1章の`Case ID`、`Decision Requirement ID`、`Handoff Contract`の考え方を理解していることを前提とする。 第2章の`Authority`、`Scope`、`Safety`、`Disclosure`の四つのGateも前提とする。

ただし、本章は第1章と第2章を読んでいなくても理解できるように、必要な要点を本文中で再説明する。 本章で使うCaseは合成の業務Scenarioであり、実在の組織、顧客、資格情報、個人情報は使用しない。

本章は評価のための構造化を扱う。 実行可能な侵害手順、Payload、回避手法、永続化、横展開、破壊操作は扱わない。 それらが必要になる場合は、本章の責任境界を超えている。
## 導入Case
架空のExample Commerce社は、請求書連携アプリ`billing-bridge.example`を使って、業務SaaSから会計処理へ請求データを連携している。 月末処理を止めずに継続すべきか、権限を縮小した上で監視を追加すべきか、連携自体を停止すべきかを48時間以内に決めなければならない。

判断要求は次のとおりである。
- どの業務成果が守る対象なのか
- どのサービス、どのコンポーネント、どのIdentityがその成果を支えているのか
- どこに信頼境界があり、何が越境すると危険なのか
- どこが外部へ露出しているのか
- どの脅威仮説が優先されるのか
- 既存Controlは文書だけなのか、実装済みなのか、実際に観測できるのか、検証済みなのか
- 何を証拠として集めれば、停止、継続、改修、監視強化の判断に足りるのか
本章では、第1章の`CASE-2026-001`と`DR-2026-001`を継承しつつ、Threat Modelとして詳細化する。 ただし、本章だけで読めるように、Caseの要約をここに持ち込む。

また、第2章で作成した`AUTH-CASE-2026-001`が未承認、条件未達、または期限切れである場合、本章のThreat Modelは「実行計画」へ進まない。 Threat Modelは、許可境界の外で進めてよい免罪符ではない。
## 本章の責任境界
本章は、判断要求を、資産、境界、露出、脅威仮説、証拠要件へ変換する責任を持つ。 一方で、個別技術の詳細手順、侵害確認の実施、認証Protocolの設計詳細、Hardening手順は本章の責任ではない。
### OWN
- `ART-03 Threat Model`の構造と記入順
- `Business Outcome`、`Business Asset`、`Service`、`Component`、`Data Asset`、`Identity`、`Control Plane`、`Evidence Asset`の区別
- `Data Flow`、`Identity Flow`、`Control Flow`の区別
- `Trust Boundary`、`Attack Surface`、`Exposure`、`Entry Point`の定義
- `Threat`、`Vulnerability`、`Finding`、`Threat Hypothesis`、`Misuse Case`、`Attack Path`の分離
- `Confirmed`、`Assumed`、`Unknown`、`Not Applicable`の使い方
- `Control Documented`、`Implemented`、`Observed`、`Validated`、`Unknown`の使い方
- `Evidence Requirement`、`Gap`、`Action`、`Reassessment`の設計
- Chapter 5、6、9、11〜15、27へ渡す最小Handoff条件
### BRIDGE
- 第1章の`CASE-2026-001`、`DR-2026-001`、各種IDを本章のModelへ継承すること
- 第2章の`AUTH-CASE-2026-001`とAuthorization条件を、本章の前提条件として確認すること
- 第3章の`Capability Evidence Matrix`と接続し、「章を読んだ」ことをCapability完了の証拠にしないこと
- 第5章のATT&CK記述へ、Threat HypothesisとAsset IDを受け渡すこと
- 第6章の`Signal Flow Diagram`へ、Flow、Boundary、Observation pointを受け渡すこと
- 第9章の`Rules of Engagement`へ、Scope、Gap、停止条件の候補を受け渡すこと
- 第11章〜第15章へ、仮説、最小影響確認、Finding、改修、再評価の入力を渡すこと
- 第27章へ、AI・LLM・Agent固有の資産、境界、Tool Surfaceが存在する場合の拡張点を渡すこと
### DELEGATE
- Web、API、Identity、Cloud、Container、Supply Chainの詳細な攻撃評価手順は、[実務で使えるペネトレーションテスト大全](https://itdojp.github.io/pentest-learning-book/)へ委譲する
- OAuth、OIDC、SAML、Federation、権限委任、認証・認可の安全な設計詳細は、[実践 認証認可システム設計](https://itdojp.github.io/practical-auth-book/)へ委譲する
- OS、Network、Cloud、ContainerのHardening、Control plane保護、監査設定、運用実装は、[インフラエンジニアのための情報セキュリティ実装ガイド](https://itdojp.github.io/it-infra-security-guide-book/)へ委譲する
委譲の意味は、「本章で説明しない」ではない。 本章では、何を判断材料として渡すか、なぜその専門書が必要か、戻ってきた成果物をどこへ接続するかまでは説明する。 したがって、委譲先を読まなくても、本章の中心論旨は切れない。
## 1. 判断要求からThreat ModelへTraceを作る
Threat Modelは、図を描く作業ではなく、判断要求をレビュー可能な記録へ変換する作業である。 最初に決めるべきことは、「何のためにModelを作るのか」である。

悪い始め方は次である。
- とりあえずInventoryを一覧化する
- Diagram toolに全Nodeを置く
- 外部公開Endpointを数える
- STRIDEやChecklistの項目数を増やす
- Control frameworkへのMappingを先に埋める
これらは補助情報にはなるが、判断要求を定義しない限り、Threat Modelの完成条件にはならない。 CSFのFunctionやCategoryは、Threat Modelがどの業務成果へ接続するかを整理するには有用である。 しかし、対応付けだけで完全性や妥当性を証明しない。`SRC-CSF-001`
### F-04-01 Decision RequirementからReassessmentまでのTrace
`F-04-01`は、本章で扱う最小Traceを文章で表した図である。

```text
1. Decision Requirement
   例: 月末請求を止めずに、連携アプリを停止・継続・縮小のどれにするかを48時間以内に決める
2. Business Outcome / Business Asset
   例: 月末請求を期限どおり完了する / 請求連携能力を維持する
3. Asset typing
   例: Service、Component、Data Asset、Identity、Control Plane、Evidence Assetを分ける
4. Flow modeling
   例: Data Flow、Identity Flow、Control Flowを分ける
5. Trust Boundary
   例: Tenant境界、Identity authority境界、第三者SaaS境界、Control plane境界
6. Exposure / Entry Point
   例: 公開Webhook、管理者同意画面、外部連携設定画面、API endpoint
7. Threat Hypothesis / Misuse Case
   例: 未承認権限追加、他Tenant Data参照、監査欠落、第三者管理面経由の誤設定
8. Attack Path
   例: 権限拡大の仮説 → Token scope過大の状態 → Data APIへの到達可能性 → 監査欠落による検知遅延
9. Existing Control / Assumption / Gap
   例: 変更承認Policyはあるが、実装状態と観測状態が未確認
10. Evidence Requirement / Action / Reassessment
    例: 設定Snapshot、監査Log、承認記録、合成Event、再確認期限
```

このTraceは、NIST SP 800-30 Rev.1が整理するThreat source、Threat event、Vulnerability、Predisposing condition、不確実性の考え方と整合する。 ただし、本章では定量Risk計算を完成条件にしない。`SRC-NIST-RISK-001`

#### 一つの仮説を最後まで通す記入例

完成例を読む前に、一つの仮説だけをTemplateへ通す。`DR-2026-001`の継続判断に対し、Business Asset「請求連携能力」を担う`ASSET-2026-001`とOAuth component `ASSET-2026-005`を置く。承認からApp設定へ進むControl Flowを`FLOW-2026-001`、Administrative Controlの変化を`TB-2026-001`、read-only Review接点を`EXP-2026-001` / `EP-2026-001`とする。そこから「業務要件を超えるscopeが残る可能性」を`TH-2026-001`として記録し、成立条件と観測点だけを`EDGE-2026-001`へ書く。`CTRL-2026-001`がDocumentedに留まるなら`GAP-2026-002`を開き、`EREQ-2026-001`、`ACT-TM-2026-001`、`REA-TM-2026-001`へつなぐ。

この一連の記入では、侵害を再現していない。仮説、Controlの状態、必要Evidence、Owner、期限をDecisionへつないだだけである。各IDの全行は合成記入例で確認できる。

重要なのは、どの矢印も省略しないことである。 たとえば、`Exposure`を列挙しても、それがどの`Business Outcome`を脅かすかにつながらなければ、優先順位を決められない。 逆に、`Business Outcome`だけを書いても、どの`Entry
Point`から成立し得るかが分からなければ、観測と改善へ進めない。
## 2. 資産を「数える対象」ではなく「守る対象」として定義する
Threat Modelで最初に崩れやすいのは、「Asset」という語を一つにまとめてしまうことである。 業務成果、システム、サーバ、DB、Token、監査Log、運用手順は、すべて重要かもしれない。 しかし、同じ種類のAssetではない。

Asset inventoryは、存在する項目の一覧である。 Asset modelは、何が、誰にとって、どの結果のために、どの境界で、どの状態で重要かを記述したものである。 InventoryだけではThreat Modelにならない。
### T-04-01 資産の型と最小記録項目
| 型 | 何を表すか | 典型例 | 最低限の記録項目 | 混同しやすい対象 | 誤りの例 |
|---|---|---|---|---|---|
| `Business Outcome` | 守りたい業務結果 | 月末請求を期限どおり完了する | 判断要求、期限、失敗時影響 | Service availability | 「サーバが動いている」をOutcomeと書く |
| `Business Asset`（ART-03では具体的な`Service / Component / Data / Identity / Control Plane / Evidence`へ型付け） | Outcomeを支える業務能力や機能 | 請求連携能力、顧客向け注文Export機能 | Owner、Criticality、依存関係 | 個別Component | 単一ContainerをBusiness Assetと書く |
| `Service` | 外部または内部へ提供される機能単位 | `billing-bridge.example`、Export API | Interface、利用者、依存Control | Business Asset | Service名だけで事業影響を説明した気になる |
| `Component` | Serviceを構成する技術要素 | Scheduler、Worker、Queue、Log exporter | 実行環境、依存先、運用Owner | Service | Component一覧だけで攻撃面が分かったとみなす |
| `Data Asset`（ART-03 Typeは`Data`） | 保護対象となるData集合 | 請求データ、顧客ID、承認記録 | 分類、保存先、保有者、流通先 | DB製品名 | DBインスタンス名だけでData分類を省略する |
| `Identity` | 人、Service、Workload、Role、Tokenなどの主体 | Service principal、admin role、reviewer account | 発行元、権限、ライフサイクルOwner | User table | Identityと利用者アカウントを同一視する |
| `Control Plane` | 他のAssetの設定や権限を変更できる管理面 | IAM、同意管理、CI設定面 | 管理権限、監査可否、変更経路 | Data Plane | 管理APIを通常APIと同じ境界で扱う |
| `Evidence Asset`（ART-03 Typeは`Evidence`） | 判断と再評価に必要な証跡 | 監査Log、設定Snapshot、承認Ticket、図面 | 完全性、保持期間、Access制御 | 監視用Data source | 「本番サービスではないので重要ではない」と軽視する |
`Business Outcome`は、組織が期限内に守りたい結果である。 本章のCaseでは、「月末請求を止めない」がこれにあたる。 これはシステム名ではない。

`Business Asset`は、その結果を支える能力である。 本章のCaseでは、「請求連携能力」や「請求Export承認能力」が該当する。 これはサーバ名やAPI名より一段上の概念である。

`ART-03`の`Type`は、`Business Outcome / Service / Component / Data / Identity / Control Plane / Evidence`の7値に固定する。`Business Asset`は8番目のTypeではなく、具体的なAsset行が業務上どの能力を支えるかという意味上のRoleである。したがって、`Business role / outcome`欄に`Business Asset`名を明示し、具体的なTypeと`Business Outcome`の双方へ接続する。

`Service`は、機能の提供単位である。 利用者や他Systemから見える境界であり、`billing-bridge.example`やExport APIのような単位で表すと扱いやすい。 しかし、ServiceとBusiness Assetは同一ではない。 単一Serviceが複数のBusiness
Assetを支える場合も、その逆もある。

`Component`は、Serviceを実現するための技術構成要素である。 Queue、Scheduler、Worker、Webhook handler、Audit exporterなどが該当する。 Componentを列挙するだけでは、どれが重要かは分からない。 `Business
Outcome`との接続が必要である。

`Data Asset`は、DBやBucketそのものではなく、その中にある保護対象Dataの集合である。 同じDBに、顧客Data、監査Data、合成Test dataが混在するなら、Data Assetとしては分けて記録した方がよい。 Data classificationは組織既存の分類体系を使う。
もし分類体系が未整備なら、Threat Model内で仮分類を置き、`Assumed`としてOwnerと見直し期限を記録する。

`Identity`は、人間利用者だけではない。 Service account、Workload identity、Federated principal、admin role、承認者Role、短命Tokenも対象である。 Identityを`Data Asset`の一部として埋め込むと、権限経路を見落としやすい。

`Control Plane`は、他のAssetの振る舞いを変えられる管理面である。 同意設定、Role付与、Key rotation、CI/CD secret設定、監査出力設定は、Data planeと分けて扱うべきである。 Control planeの侵害や誤設定は、個々のData
accessより影響が広いことがある。

`Evidence Asset`は軽視されやすいが、意思決定に必須である。 監査Log、設定Export、変更承認Ticket、Architecture図、Rule test結果が欠けると、侵害がなくても「判断不能」という重大な状態になる。 本番Dataを守れていても、Evidence
Assetの完全性が失われれば、後続のDetection、IR、Auditに支障が出る。

Asset記述では、少なくとも次をセットで残す。
- `Owner`
- `Criticality`
- `Data Classification`
- 依存する`Business Outcome`
- 関連する`Flow`
- 関連する`Trust Boundary`
- 観測可能性とEvidence source
ここでいう`Criticality`は、脆弱性深刻度と同義ではない。 業務上の停止許容時間、代替運用、法務・契約影響、依存先の有無などで決まる。 `Critical`や`High`のような質的区分は使ってよいが、本章では数値Risk scoreを完成条件にしない。`SRC-NIST-RISK-001`
## 3. Flowを分ける
多くのThreat Modelが弱くなる理由は、「通信」を一つの矢印で済ませるからである。 同じ矢印に、Data、Identity、Controlが混ざると、どの越境を守りたいのかが曖昧になる。

本章では、少なくとも次の三種類を分ける。
- `Data Flow`
- `Identity Flow`
- `Control Flow`
`Data Flow`は、請求データ、監査データ、承認記録、設定Exportなど、保護対象Dataの移動である。 問題は、何が、どこからどこへ、どの形式で、どのOwnerの権限で流れるかである。

`Identity Flow`は、認証、認可、Token発行、Role引受け、Federation、Service-to-service trustなどの流れである。 問題は、誰が誰として扱われ、どの権限がどの条件で成立するかである。

`Control Flow`は、設定変更、権限変更、承認、同意、Secret rotation、監査設定変更の流れである。 問題は、誰がどの管理面を通じて、何の振る舞いを変えられるかである。

同じ通信路でも、三つのFlowが重なることがある。 たとえば、管理者同意画面は`Identity Flow`であり、同時に`Control Flow`でもある。 一方、Export APIの応答は主に`Data Flow`である。

Flowを分ける利点は次である。
- Data segregationの問題を、認証問題と混同しにくい
- TokenやRole委任の問題を、単なるNetwork pathと誤解しにくい
- 管理面の誤設定を、通常の利用面と分けて高優先で扱える
- どのEventをLogで取るべきかをChapter 6へ受け渡しやすい
Flowの本数やDiagramの複雑さは、Threat Modelの品質を保証しない。 重要なのは、判断に必要な越境を十分に説明できるかである。
## 4. 信頼境界をNetwork Segmentと混同しない
`Trust Boundary`は、単に別Subnet、別VPC、別コンテナであることを意味しない。 逆に、同一Network segment内でも強いBoundaryが存在することがある。

Boundaryを定義する基準は、技術的な線ではなく、「信頼している前提が切り替わる場所」である。 本章では、少なくとも次のBoundary候補を確認する。
- `Identity authority boundary`
- `Data ownership boundary`
- `Administrative boundary`
- `Tenant boundary`
- `Third-party boundary`
- `Control-plane boundary`
`Identity authority boundary`は、ある主体の身元と権限を誰が保証するかが変わる境界である。 自社IdPから第三者SaaSへFederationする点や、Service principalが外部Tokenを受け取る点が典型例である。

`Data ownership boundary`は、Dataの保有・利用責任が切り替わる境界である。 顧客Data、委託先Data、監査Data、社内運用Dataが同じStorageにあっても、Ownershipが違えばBoundary候補になる。

`Administrative boundary`は、設定変更権限の保有者が変わる境界である。 Platform team、委託先、SaaS provider、顧客管理者のいずれが変更できるかが変わる場所である。

`Tenant boundary`は、Multi-tenant環境で顧客、部門、環境、テスト領域の分離が求められる境界である。 同じApplication codeでも、Tenant separationは独立したBoundaryである。

`Third-party boundary`は、自組織が直接統制しないProvider、連携SaaS、外部API、外部CI/CD、外部監査基盤との境界である。 契約上の責任と技術的到達性を分けて記録する必要がある。

`Control-plane boundary`は、設定や権限を変更できる管理面と、通常利用面の境界である。 Data planeだけを見るModelでは、このBoundaryを見落としやすい。
### F-04-02 境界、Flow、攻撃面の読み分け
`F-04-02`は、合成SaaS連携を文章で分解した図である。

```text
Business Outcome:
  月末請求を期限どおり完了する

Business Asset:
  請求連携能力

Service:
  billing-bridge.example

Components:
  export worker / scheduler / audit exporter / consent review job

Data Assets:
  請求データ / 承認記録 / 監査Log / 設定Snapshot

Identities:
  finance-operator role / workload identity / admin approver role

Control Plane:
  app consent management / IAM role assignment / audit export setting

Data Flow:
  業務SaaS → 請求Export → billing-bridge.example → 会計処理

Identity Flow:
  workload identity → token issuance → API authorization

Control Flow:
  admin approver role → consent management → scope change

Trust Boundaries:
  tenant boundary / identity authority boundary / control-plane boundary / third-party SaaS boundary

Exposure:
  admin consent UI / export API / webhook callback / audit export configuration interface
```

この図で重要なのは、Network pathだけではBoundaryが説明できないことである。 たとえば、admin consent UIとexport APIが同じDomain配下でも、前者は`Control-plane boundary`、後者は主に`Data Flow`のEntry Pointである。
### T-04-02 似て見える用語の違い
| 用語対 | 前者 | 後者 | 実務上の違い | 典型的な誤り |
|---|---|---|---|---|
| `Trust Boundary` / `Network Segment` | 信頼前提が切り替わる場所 | 通信経路の分割単位 | Boundaryは権限、Ownership、統制主体の切替を表せる | VLANが違うからBoundary、同じVPCだからBoundaryなしと決める |
| `Attack Surface` / `Exposure` | 攻撃者が作用し得る面の集合 | その時点で実際に露出している要素 | Surfaceは潜在的、Exposureは現在状態 | Inventoryにある全EndpointをExposureと書く |
| `Exposure` / `Entry Point` | 到達可能な対象や機能の露出状態 | 攻撃経路の起点となる具体的接点 | 一つのExposureに複数Entry Pointがあり得る | 公開Domain名だけをEntry Pointと書く |
| `Threat` / `Vulnerability` | 望ましくない事象や行為 | それを成立させやすい弱点 | Threatは起こり得る事象、Vulnerabilityは条件 | CWE名だけでThreatを書いた気になる |
| `Vulnerability` / `Finding` | 一般的または環境依存の弱点 | その環境で確認した記録 | FindingはEvidenceに支えられる | Scanner結果をそのままFinding確定とみなす |
| `Threat Hypothesis` / `Misuse Case` | 検証可能な仮説文 | 利用機能の悪用シナリオ記述 | 前者は状態管理、後者は説明補助 | 物語だけ書いて反証条件を持たない |
| `Attack Path` / 実行可能な侵害手順 | 境界越えの抽象経路 | コマンド、Payload、操作列 | 公開教材では前者まで | Pathを再現手順へ展開してしまう |
Boundaryを定義するときの注意点は三つある。

第一に、Network segmentはBoundary候補に過ぎない。 同じSegmentでも、別Tenant、別権限、別OwnerならBoundaryがある。

第二に、Boundaryは「境界線の本数」では評価しない。 多く引けば安全というものではなく、誤って引けば分析の焦点を外す。

第三に、Boundaryは後続章の観測点と一致する必要がある。 Chapter 6では、各Boundaryで何を観測できるか、どのFlowがどのLogへ現れるかを詳しく扱う。
## 5. Attack Surface、Exposure、Entry Pointを分ける
`Attack Surface`は、攻撃者が作用し得る面の集合である。 公開API、管理画面、Webhook、外部連携、Federation、CI/CD、監査設定、Support運用、供給Chainなどが含まれる。

`Exposure`は、そのSurfaceのうち、いま実際に利用可能、到達可能、設定可能、公開中、委任済みの状態である。 Surfaceが存在しても、無効化されている、Firewallで遮断されている、Roleが未割当である、機能Flagが無効であるなら、現在のExposureではない場合がある。

`Entry Point`は、Attack Pathの起点になる具体的な接点である。 URL、Webhook endpoint、admin consent画面、Role assignment API、artifact upload口、support request workflowなどが該当する。

三者を分ける利点は次である。
- 将来有効化される潜在面を`Attack Surface`として保持できる
- 現在の到達可能性を`Exposure`として判断できる
- 実際の確認や監視の対象を`Entry Point`として明示できる
誤りやすい例を示す。
- 「公開Domainが一つある」だけでは`Attack Surface`しか分からない
- 「API endpointが200本ある」だけでは、どれが`Exposure`か分からない
- 「Scannerが0件だった」だけでは、`Entry Point`の見落としを否定できない
- 「ATT&CKへMappingした」だけでは、どの`Entry Point`に対する仮説か分からない
OWASP Threat Modeling Projectは、単一Methodよりも、問い、System model、Threat identification、Mitigation、Reviewの接続を重視する。 したがって、本章でもSurface countやTool countを完成条件にしない。`SRC-OWASP-TM-001`

`Attack Surface Register`を別章で作る場合でも、本章のThreat Modelはそれを置き換えない。 Registerは列挙に強いが、判断要求、Business Asset、Boundary、Evidence Requirementとの接続は本章の責任である。

ここでの完成条件は、「全部見つけたと断言すること」ではない。 次を説明できることである。
- 何を見たか
- 何をまだ見ていないか
- なぜ優先したか
- 何が`Unknown`として残るか
- その`Unknown`を誰が、いつ、何を契機に再確認するか
## 6. Threat、Vulnerability、Finding、Hypothesisを分離する
Threat Modelで最も混ざりやすいのが、Threat、Vulnerability、Findingである。 NIST SP 800-30 Rev.1は、Threat source / eventとVulnerability / Predisposing conditionを分けてRisk
assessmentを組み立てる。 本章でも、この分離を維持する。`SRC-NIST-RISK-001`

`Threat`は、望ましくない事象や行為である。 例として、未承認の権限追加、他Tenant Dataへの到達、監査停止、第三者管理面からの誤設定、承認経路を迂回した変更などがある。

`Vulnerability`は、そのThreatを成立させやすい弱点や条件である。 例として、過大権限、境界チェック欠落、監査保持不足、Approval連携欠落、Tenant分離不備、Role設計の曖昧さがある。

`Finding`は、許可された範囲でEvidenceに支えられて確認した環境固有の結論である。 一般論としての弱点が知られていても、自組織環境で確認できなければFindingではない。 逆に、業界標準のCWE名が付かなくても、自組織の設定差分や監査欠落をFindingとして扱える。

`Threat Hypothesis`は、Threat Modelの中心である。 「何が起こり得るか」を、対象Asset、Boundary、成立条件、影響、否定条件とともに検証可能な文へしたものである。 例として、次のように書く。
- 請求連携アプリの管理権限変更が承認記録なしに成立し、月末処理のData access範囲が業務要件を超える可能性がある
- Multi-tenant Export APIで、他Tenant job identifierに対する認可判定が不十分で、Metadataが露出する可能性がある
- Audit export設定がControl plane変更に追随できず、必要な変更EventがEvidence Assetへ残らない可能性がある
`Misuse Case`は、利用可能な正規機能がどのように悪用されるかを、関係者が理解しやすいNarrativeで示すものである。 たとえば、「運用担当が通常の承認画面を使って、意図せず広い権限を付与し、その後の監査差分で検出できない」という形で書ける。

両者の違いは次である。
- `Threat Hypothesis`は状態管理の対象である
- `Misuse Case`は説明補助であり、単独では検証条件にならない
- `Threat Hypothesis`は反証条件を持つ
- `Misuse Case`は業務側や管理者との合意形成に有効である
`Attack Path`は、Asset、Boundary、Exposure、Threat Hypothesisをつないだ抽象経路である。 ここでは、「どの順で越境が重なるとBusiness Outcomeへ届くか」を示す。

重要なのは、`Attack Path`を実行可能な侵害手順に変えないことである。 公開教材で必要なのは、境界越えの論理、必要なEvidence、観測点、停止条件である。 コマンド列、Payload、再現細部は本章および公開本編の範囲外である。Chapter 11〜15へは、許可条件に従う評価仮説とEvidence Requirementだけを引き渡す。

良い`Attack Path`の例は次である。
- 要件外scopeが承認済み設定として残る
- Workload identityとApp componentのbindingが最小権限要件から外れる
- Summary-only Boundaryを越える影響範囲が生じ得る
- 必要な監査Eventの欠落または保持不足で観測範囲が限定される
- その結果、停止・継続判断が遅延する
悪い`Attack Path`の例は次である。
- 脆弱性名だけを並べる
- 実行手順を詳細化する
- 影響先のBusiness Outcomeを書かない
- Entry Pointを示さない
- 既存ControlとEvidence Requirementを書かない
Threat countを増やしても、良いModelにはならない。 OWASP Threat Modeling Projectも、単一の公式MethodやToolを完全性証明として位置付けていない。`SRC-OWASP-TM-001`
## 7. 状態を混ぜない
Threat Modelでは、ひとつの`Status`欄へ何でも入れた瞬間に運用が崩れる。 Model全体の状態、各項目の確からしさ、仮説の進捗、Controlの成熟度、Evidenceの収集状態は別物である。
### T-04-03 Control assurance states
| Assurance state | 本章での意味 | 次へ進むためのEvidence | 誤った読み方 |
|---|---|---|---|
| Unknown | Controlの存在または状態を確認できていない | Owner、設計、設定、観測点の確認 | 未確認なのでControlが存在しない |
| Documented | Policy、Runbook、設計書または標準に記載されている | 実装された設定またはCodeの確認 | 文書があるので有効である |
| Implemented | 設定、Codeまたは製品機能として存在する | 期待挙動またはEventの観測 | 実装があるので動作している |
| Observed | 期待挙動またはEventを観測できる | 宣言したThreat Hypothesisと条件に対する検証 | 観測できたので全条件で有効である |
| Validated | 本Caseの限定条件で防止または検知への寄与を確認した | Reassessment triggerと有効期限の管理 | 組織全体の普遍的成熟度である |

### T-04-04 Knowledge stateとHypothesis statusの分離
| 対象 | 何の状態か | 有限集合 | 使い方 | してはいけないこと |
|---|---|---|---|---|
| Model全体 | 文書としての準備状態 | Draft / In Review / Approved for Assessment / Needs Evidence / Superseded | Threat Model全体のReviewと見直し管理 | 個別仮説の成立可否をここへ混ぜる |
| Item knowledge | Asset、Boundary、Flow等の事実確度 | Unknown / Assumed / Confirmed / Not Applicable | 一つひとつの項目にEvidenceまたはGapを付ける | Unknownを空欄で放置する |
| Threat Hypothesis | 仮説の検証状態 | Candidate / Supported / Partially Supported / Disconfirmed / Inconclusive | 後続章の評価対象として使う | Supportedを「危険度High」と同義にする |
| Evidence Requirement | 必要Evidenceの定義状態 | Required / Deferred / Replaced / Not Applicable | 何を集めるべきかを先に定義する | 手元にあるDataを後付けで十分とみなす |
| Collected Evidence | 実際のEvidence収集状態 | Planned / Collected / Rejected / Inconclusive | 収集時刻、完全性、限界を記録する | Requirementと同じ欄で管理する |
| Gap | 未解決事項の管理状態 | Open / Accepted temporarily / Escalated / Closed | Owner、Due date、Triggerを持たせる | UnknownとGapを区別しない |

Gap statusは Open / Accepted temporarily / Escalated / Closed の有限集合だけを使用する。これはKnowledge stateやEvidence Requirement statusとは別の状態である。
`Confirmed`は、一次資料、直接観測、承認済み図面、設定Snapshot、Logなどで裏付けできる状態である。 `Assumed`は、現時点でそう置かないと判断が進まないが、まだ確認していない状態である。 `Unknown`は、確認できていないことが明らかな状態である。 `Not
Applicable`は、対象判断に本当に関係がない場合だけ使う。

`Assumed`と`Unknown`の違いは重要である。
- `Assumed`は暫定前提であり、無効化条件を持つ
- `Unknown`は不足そのものであり、Ownerと期限を持つGapへ変換する
- `Not Applicable`は「今は見ない」の言い換えではない
たとえば、組織のData classificationが未整備で、本章の判断に仮分類が必要なら`Assumed`で置ける。 一方、第三者SaaS側の監査保持期間が分からないなら、それは`Unknown`である。 そして`Unknown`は、`Gap owner`、`Due date`、`Reassessment
trigger`を必ず持つ。

Control状態の分離も同じくらい重要である。
本章で用いる有限集合は`Unknown / Documented / Implemented / Observed / Validated`である。
- `Documented`: Policy、Runbook、設計書、標準が存在する
- `Implemented`: 設定、Code、製品機能として存在する
- `Observed`: 実際のEvent、設定差分、挙動として観測できる
- `Validated`: 定義したThreat Hypothesisに対して、定義した条件で防止または検知に効くと確認した
- `Unknown`: どこまで成立しているか未確認
この順序は、成熟の段階を示すが、自動進行ではない。 `Documented`だから`Implemented`とは限らず、`Implemented`だから`Observed`とも限らず、`Observed`だから`Validated`でもない。
「文書化されているControl」を「有効なControl」と読み替えるのは典型的な誤りである。

`Evidence Requirement`と`Collected Evidence`も分ける。 `Evidence Requirement`は、判断に何が必要かを事前に定義したものである。 `Collected Evidence`は、実際に得られたものとその限界である。

この順序を逆にすると、手元にたまたまあったLogや図面で結論を正当化しやすくなる。 本章では、必ず「何が必要か」を先に定義し、その後で「実際に何が集まったか」を比較する。

CSF 2.0の観点でも、Govern、Identify、Protect、Detect、Respond、Recoverは、Controlの存在、観測、改善を連続的に扱う。 しかし、Categoryへ対応付けただけで、Controlが観測済みまたは検証済みとは言えない。`SRC-CSF-001`

`Unknown`は恥ではない。 問題は、`Unknown`を無言で隠すことである。 Threat Modelの良し悪しは、空欄の少なさではなく、`Unknown`を判断可能なGapへ変換できているかで決まる。
## 8. Handoffを前提にThreat Modelを書く
Threat Modelは、その章で閉じる成果物ではない。 Chapter 5、6、9、11〜15、27へ渡す入力である。 そのため、本章の記述は、後続章が受け取れる粒度でなければならない。
### 章間Handoffの最小契約
| 行先 | 本章から渡すもの | 最低限必要なIDまたは情報 | 渡した先で何に使うか | 差戻し条件 |
|---|---|---|---|---|
| 第1章 | `CASE-2026-001`、`DR-2026-001`との整合 | Case ID、Decision Requirement ID、Asset ID、Boundary ID | Case Mapの追跡性維持 | 新しいCaseなのに既存Caseへ無理に統合している |
| 第2章 | `AUTH-CASE-2026-001`の条件反映 | Authority条件、対象外、停止条件、期限 | 実行可否と再承認判断 | Authorizationが失効、条件未達、対象追加 |
| 第3章 | Capability上の注意書き | どのTaskを想定した成果物か | `ART-14`で学習Evidenceへ接続 | 章読了だけをCapability完了扱いしている |
| 第5章 | Threat HypothesisとAsset / Boundary | Threat ID、Asset ID、Boundary ID、想定Actor | ATT&CK Behavior記述とCoverage議論 | AssetやBoundaryが抽象的すぎる |
| 第6章 | FlowとObservation point | Data / Identity / Control Flow、Boundary、Entry Point | `Signal Flow Diagram`とTelemetry候補 | どこを観測したいか不明 |
| 第9章 | Scope候補とGap | In-scope候補、Out-of-scope候補、禁止事項、Gap | `Rules of Engagement`設計 | Threat Modelが実行手順に流れ込みすぎている |
| 第11章〜第15章 | TestableなThreat Hypothesis | Threat Hypothesis、Misuse Case、Attack Path、Evidence Requirement、Control state | 仮説駆動評価、最小影響確認、Finding、改修、再評価 | 仮説が反証不能、Evidence要件が未定義 |
| 第27章 | AI固有拡張点 | Model provider、Prompt source、Tool scope、Memory、Approval path | AI / Agent固有のBoundaryとControl評価 | AI固有のIdentityやTool Surfaceを一般Web資産へ埋没させる |
第1章との接続では、ID継承が重要である。 別の判断対象ではない限り、Case IDをむやみに増やさない。 一方で、単に話がつながって見えるからといって、独立した判断要求を同じCaseへ統合しない。

第2章との接続では、`AUTH-CASE-2026-001`の条件をThreat Modelへ反映する。 たとえば、Production credentialが対象外なら、本章の`Entry Point`候補へ書けても、後続のValidation対象にはそのまま入れない。

第3章との接続では、`ART-03`を作れたことと、Threat Modelingを実務で安定運用できることを同一視しない。 本章の成果物は、Capabilityの証拠候補にはなるが、Review、Rubric、再評価なしに能力証明にはならない。

第5章では、Threat HypothesisをATT&CKのBehavior表現へつなぐ。 ただし、Technique mapping自体がThreatの存在証明にならないのと同じく、本章のAsset listだけでもThreat Modelの完成証明にはならない。

第6章では、各BoundaryとFlowを、観測可能なSignalへ分解する。 本章で`Data Flow`と`Identity Flow`を混同していると、後続のTelemetry設計が破綻する。

第9章では、本章のGapを無視してRoEを書かない。 `Unknown`があるなら、そのまま許可手順へ進まず、対象外化、条件付きProceed、再承認のいずれかへ変換する。

第11章〜第15章では、本章の`Threat Hypothesis`が評価計画、最小影響確認、Finding、改修、再評価へ接続される。 したがって、ここでの仮説は「面白そう」ではなく、「判断に必要」でなければならない。

第27章では、AI・LLM・Agent特有の追加論点を扱う。 たとえば、Prompt source、Tool calling範囲、Memory、Model provider、Approval path、output handlingは、本章でいう`Data Asset`、`Identity`、`Control
Plane`、`Third-party boundary`の拡張として扱える。 ただし、AI固有の脅威は第27章で詳述する。
## 9. Threat Modelの最小完成条件
本章のThreat Modelは、すべての脅威を見つけた状態を意味しない。 最低限、次が追跡できる状態を完成とみなす。
- `Decision Requirement`が明記されている
- 少なくとも一つの`Business Outcome`と`Business Asset`が定義されている
- 重要Assetに`Owner`、`Criticality`、`Data Classification`がある
- `Data Flow`、`Identity Flow`、`Control Flow`の少なくとも一つずつが記載されている
- `Trust Boundary`が、Network segment以外の観点も含めて定義されている
- `Exposure`と`Entry Point`が区別されている
- 少なくとも一つの`Threat Hypothesis`と一つの`Misuse Case`がある
- `Attack Path`が、実行可能手順ではなく、越境の論理として記述されている
- 既存Controlが`Documented`、`Implemented`、`Observed`、`Validated`、`Unknown`のどれかで整理されている
- `Evidence Requirement`と`Collected Evidence`が分離されている、またはCollected前であることが明記されている
- `Unknown`がGapへ変換され、Owner、Due date、Reassessment triggerを持つ
逆に、次は完成条件ではない。
- Assetの件数
- Boundaryの本数
- Threatの件数
- Tool出力の件数
- Framework mappingの件数
- 数値Risk scoreの有無
- Diagramの見た目の複雑さ
NIST CSF 2.0は、組織が成果に向けてRisk managementを整えるための枠組みであり、単一の完全性指標を与えるものではない。`SRC-CSF-001` Threat Modelの完成も同様である。
## 安全な演習
### 目的
完全オフラインの合成Scenarioから、`ART-03 Threat Model`の最小版を作成する。 外部接続、実Credential、実在組織、実在Tenantは使わない。
### 使用する材料
- ローカルにある[Threat Model](../templates/threat-model.md)
- 本章本文
- 合成Case要約メモ
- 任意で、後日参照するための[第4章 合成記入例](../cases/ch04-threat-model-example.md)
### 合成Scenario
次の完全合成Scenarioを使う。
- 組織: `SYNTH-ORG-BILLING`
- 業務成果: 月末請求を期限内に完了する
- Business Asset: 請求連携能力
- Service: `billing-bridge.example`
- Data Asset: 合成請求データ、承認記録、監査Log
- Identity: 合成workload identity、合成approver role、合成reviewer account
- Control Plane: 合成同意管理画面、合成監査設定画面
- Evidence Asset: 合成設定Snapshot、合成承認Ticket、合成監査Export
### 作業
1. `Decision Requirement`を一文で書く
2. `Business Outcome`と`Business Asset`を分けて書く
3. `Service`、`Component`、`Data Asset`、`Identity`、`Control Plane`、`Evidence Asset`を最低一つずつ書き、`Business Asset`は該当行の`Business role / outcome`へ明示する
4. `Data Flow`、`Identity Flow`、`Control Flow`を最低一つずつ書く
5. `Trust Boundary`を三つ以上書く。ただし、少なくとも一つはNetwork segment以外のBoundaryにする
6. `Exposure`と`Entry Point`を分けて書く
7. `Threat Hypothesis`を二つ、`Misuse Case`を一つ書く
8. 既存Controlを`Documented`、`Implemented`、`Observed`、`Validated`、`Unknown`のいずれかで記録する
9. `Unknown`を最低一つGapへ変換し、Owner、Due date、Reassessment triggerを付ける
10. `Evidence Requirement`を先に書き、Collected Evidence欄は空欄または`Planned`のままにする
### 禁止
- 実在Domain、実在IP、実在Tenantを書かない
- 実Credential、Token、Cookie、個人情報を書かない
- 侵害手順、Payload、運用可能な攻撃経路を書かない
- 外部サイトや本番環境へ接続しない
- `Unknown`を空欄で隠さない
### Stop condition
次のいずれかが起きたら、Threat Model作成を中断する。
- 実在Targetが必要になった
- 実CredentialやPIIが必要になった
- 手順が実行可能な侵害手順へ寄り始めた
- Authorization条件が不明になった
- どのBoundaryが判断に関係するか説明できなくなった
### 期待する学習成果
演習の合格条件は、Threat countの多さではない。 判断要求からGapまでを追跡でき、どこが未確認かを隠していないことである。
## 作成する成果物
本章で作成する成果物は`ART-03 Threat Model`である。 空Templateは[Threat Model](../templates/threat-model.md)を参照する。 合成記入例は[第4章 合成記入例](../cases/ch04-threat-model-example.md)を参照する。

`ART-03`の正本構造は、Templateと合成記入例で共通する次の13節（番号0〜12）である。

1. `Document Control`
2. `Decision Context`
3. `Asset Register`
4. `Flow Register`
5. `Trust Boundary Register`
6. `Exposure and Entry Point Register`
7. `Threat Hypothesis and Misuse Case`
8. `Attack Path Register`
9. `Control Assurance Register`
10. `Assumptions, Unknowns and Gaps`
11. `Evidence Requirements and Actions`
12. `Reassessment and Handoff`
13. `Review and Rubric`

演習では各表の全行を埋める必要はないが、節、有限状態、ID関係は削らない。Templateの各節と合成記入例の同名節を一対一で参照し、途中成果でも`Unknown`や空のCollected Evidenceを隠さずに残す。

本章で重視するのは、行数を増やすことではない。次を追跡できることである。
- Decision Requirementとの接続
- Asset typeの区別
- Boundaryの根拠
- Flowの種類
- HypothesisとMisuse Caseの分離
- Evidence RequirementとGap
- Reassessment trigger
## 評価基準

正式な自己評価には、Templateと合成記入例で共通する`RUBRIC-TM-YYYY-NNN`の5項目を使う。本節はその読み方を示し、別の評価体系を追加しない。

### `RUBRIC-TM-YYYY-001` Asset taxonomy
- `Business Outcome`、`Business Asset`、`Service`、`Component`、`Data Asset`、`Identity`、`Control Plane`、`Evidence Asset`を混同していない
- Component一覧で終わらず、DecisionへのBusiness roleを説明できる

### `RUBRIC-TM-YYYY-002` Boundary and flow clarity
- `Data Flow`、`Identity Flow`、`Control Flow`が分離されている
- `Trust Boundary`をNetwork segmentだけで決めていない
- `Attack Surface`、`Exposure`、`Entry Point`が分離されている

### `RUBRIC-TM-YYYY-003` Threat usefulness and evidence sufficiency
- `Threat`、`Vulnerability`、`Finding`、`Threat Hypothesis`、`Misuse Case`、`Attack Path`が分離されている
- `Decision Requirement`から`Evidence Requirement`、`Gap`、`Action / Reassessment`まで辿れる
- Model、Knowledge、Hypothesis、Control、Evidence Requirement、Collected Evidence、Gapの状態を混ぜていない

### `RUBRIC-TM-YYYY-004` Safety and authorization
- 実在Target、実Credential、PII、外部接続を含まない
- `Attack Path`が実行可能な侵害手順へ変質していない
- `AUTH-CASE-2026-001`などAuthorization条件に反する内容を入れていない
- 実施が必要な場合でも、Chapter 9以降のGateへ正しく差し戻している

### `RUBRIC-TM-YYYY-005` Decision handoff quality
- Decision ownerが、何を守りたいのかを理解できる
- どこが未確認で、何を追加で確認すべきかが分かる
- Chapter 5、6、9、11〜15、27へ渡す入力として十分である
- Threat、Asset、Toolの件数ではなく、判断寄与で品質を説明できる

章を読了した事実だけをCapability完了と扱わない。演習結果を第3章の`ART-14`へ戻す場合は、Review、限定条件、Expiry、再評価条件を別途定義する。
## よくある誤解
### InventoryがあればThreat Modelもできている
誤りである。 Inventoryは一覧であり、Threat Modelは判断要求との接続である。 Assetの件数やComponentの件数だけでは、どのBoundaryが重要か分からない。
### 別Subnet、別VPCなら自動的にTrust Boundaryである
誤りである。 Network分離はBoundaryの一根拠に過ぎない。 同一Network内でも、Tenant、Identity authority、Control plane、Data ownershipが違えばBoundaryになり得る。
### Management画面は通常APIと同じAttack Surfaceでよい
誤りである。 Control planeはData planeより影響が大きい場合がある。 管理面、同意、Role付与、監査設定変更は、別Boundaryとして扱うべきである。
### 文書化されたControlがあるので十分である
誤りである。 `Documented`は`Validated`ではない。 Policyが存在しても、設定が存在するとは限らず、設定が存在しても観測できるとは限らず、観測できても有効とは限らない。
### Unknownは未熟さなので書かない方がよい
誤りである。 Unknownを隠すと、後続章で誤った前提が固定される。 Threat Modelでは、UnknownをGapへ変換し、Owner、期限、Triggerを付ける方が成熟している。
### CSFやOWASPへMappingしたので完全である
誤りである。 CSFは非処方的な成果指向フレームワークであり、OWASP Threat Modeling Projectも単一Methodや単一Toolを完成証明にしない。`SRC-CSF-001` `SRC-OWASP-TM-001`
### Threatをたくさん書くほど良いModelである
誤りである。 重要なのは件数ではなく、判断要求、Business Asset、Boundary、Evidence Requirementとの接続である。 後続章へ渡せないThreat listは、長くても弱い。
### 数値Risk scoreを入れないとThreat Modelは完成しない
誤りである。 本章は、数値Risk scoreを否定しないが、完成条件にはしない。 NIST SP 800-30 Rev.1も、不確実性や前提条件を伴う評価を重視しており、単一の数値GateでModel完成を定義していない。`SRC-NIST-RISK-001`
## 章のまとめ
本章では、Threat Modelを「脅威を数える文書」ではなく、「判断要求を、資産、境界、露出、仮説、証拠要件、再評価へ変換する文書」として定義した。

重要な区別は次のとおりである。
- `Business Outcome`と`Business Asset`
- `Service`と`Component`
- `Data Asset`、`Identity`、`Control Plane`、`Evidence Asset`
- `Data Flow`、`Identity Flow`、`Control Flow`
- `Trust Boundary`と`Network Segment`
- `Attack Surface`、`Exposure`、`Entry Point`
- `Threat`、`Vulnerability`、`Finding`
- `Threat Hypothesis`と`Misuse Case`
- `Attack Path`と実行可能な侵害手順
- `Confirmed`、`Assumed`、`Unknown`、`Not Applicable`
- `Control Documented`、`Implemented`、`Observed`、`Validated`、`Unknown`
- `Evidence Requirement`と`Collected Evidence`
また、Threat Modelの品質は、件数やTool outputではなく、Decision RequirementからReassessmentまでの追跡性で評価すべきことを確認した。 `Unknown`は隠す対象ではなく、Owner、期限、Triggerを持つGapとして扱う。 `Documented`
controlは`Validated` controlではない。

本章で作った`ART-03 Threat Model`は、Chapter 5のBehavior記述、Chapter 6の観測設計、Chapter 9のRoE、Chapter 11〜15の評価・改修、Chapter 27のAI固有論点へ接続する起点になる。
## 次に学ぶこと
次は第5章で、ここで作成したThreat HypothesisとAsset / Boundary情報を、ATT&CKのBehavior記述へ接続する。 そのときも、Technique mappingだけで脅威の存在やCoverage完全性を主張しないことが重要である。

第6章では、本章で分けた`Data Flow`、`Identity Flow`、`Control Flow`を、観測可能なSignalとLogへ落とし込む。 本章でBoundaryを曖昧にしたままでは、後続のTelemetry設計が弱くなる。

第9章では、Threat Modelで見つかったGap、対象外、停止条件候補を、`Rules of Engagement`へ変換する。 Chapter 11〜15では、本章のThreat Hypothesisを、最小影響の確認、Finding、改修、再評価へ進める。
AI・LLM・Agent固有のBoundaryやTool Surfaceがある場合は、第27章で追加拡張する。
## 参考資料

以下のSource Note IDは、本文で採用した主張と一次情報の対応を示す。

### 参考文献・Source Note ID

- `SRC-CSF-001`: NIST Cybersecurity Framework 2.0。成果指向、非処方的、Governを含むRisk management接続。本章ではFramework mappingを完全性証明に使わない前提として参照した
- `SRC-NIST-RISK-001`: NIST SP 800-30 Rev.1 Guide for Conducting Risk Assessments。Threat source / event、Vulnerability、Predisposing condition、不確実性、数値Gate非依存の整理に参照した
- `SRC-OWASP-TM-001`: OWASP Threat Modeling Project。継続保守される方法論中立のThreat Modeling guidanceとして参照し、単一Method、Threat count、Tool outputを完全性証明にしない前提に使った
