# 詳細目次

## 序部　何を学び、何をしないのか

### 第0章　本書の読み方

- 読者別ルート
- 成果物ベースの学習
- 安全上の境界
- 既存専門書との往復方法
- 学習記録とポートフォリオ

成果物: `Learning Route Plan`

### 第1章　攻撃・防御・インテリジェンスを一つの業務として捉える

- ホワイトハッカーという呼称の限界
- Security Assessment、Pentest、Red Team、Purple Team
- SOC、CSIRT、DFIR、CTI
- 情報、証拠、分析、判断の違い
- Threat-Informed Decision Loop
- 四つの視点: 攻撃者、防御者、分析者、意思決定者

成果物: `Integrated Security Workflow Map`

### 第2章　法、倫理、許可、責任ある開示

- 書面による許可
- 対象、時間、手法、停止条件
- 個人情報・秘密情報・証拠
- 脆弱性発見時の連絡と開示
- 委託、再委託、クラウド共有責任
- 安全性と合法性を事前条件にする

成果物: `Authorization Checklist`

### 第3章　能力を分解し、証拠で学習する

- 職種名ではなくTask、Knowledge、Skillで考える
- 基礎能力、専門能力、統合能力
- 観察、説明、評価、設計、指揮の段階
- 演習スコアではなく成果物で評価する
- 学習バックログ

成果物: `Capability Evidence Matrix`

---

## 第I部　Threat-Informed Securityの共通基盤

### 第4章　資産、信頼境界、攻撃面、脅威モデル

- 業務資産と技術資産
- Identity、Data、Control Plane
- Trust Boundary
- Attack SurfaceとExposure
- Data Flow Diagram
- Misuse CaseとAttack Path

成果物: `Threat Model`

### 第5章　攻撃者の行動をATT&CKで記述する

- Tactic、Technique、Sub-technique
- Group、Software、Campaignの扱い
- ATT&CKは脅威の存在証明ではない
- Detection Strategy、Analytics、Data Component
- Coverage Mapの誤用
- バージョン固定と移行

成果物: `ATT&CK Behavior Map`

### 第6章　通信、Identity、Cloudを観測可能なシステムとして読む

- DNS、TLS、HTTP、API
- Session、Token、Federation
- AD、Entra ID、OAuth、OIDC、SAML
- Cloud IAM、Workload Identity、Secret
- Container、Kubernetes、CI/CD
- 操作とログの対応

成果物: `Signal Flow Diagram`
詳細は既存の認証・インフラ・クラウド書籍へ委譲する。

### 第7章　脆弱性、露出、悪用可能性、事業影響を分ける

- CVE、CWE、CVSSの役割
- EPSS、KEV、実悪用情報
- 資産重要度と外部公開状況
- Attack Pathと代替統制
- 技術深刻度と修正優先度
- リスク受容

成果物: `Vulnerability Prioritization Record`

### 第8章　安全で再現可能なラボと証拠管理

- rootlessコンテナとネットワーク分離
- 合成データ、合成ログ
- 時刻、ハッシュ、実験ノート
- Snapshot、初期化、クリーンアップ
- 失敗時の停止
- 再現性とChain of Custodyの違い

成果物: `Lab Safety and Evidence Plan`

---

## 第II部　安全な攻撃評価

### 第9章　Engagement DesignとRules of Engagement

- 判断目的から検査範囲を決める
- 対象と対象外
- 許可する手法と禁止する手法
- 連絡、時間、停止、復旧
- データ取扱い
- テスト完了と成功の定義

成果物: `Rules of Engagement`

### 第10章　ReconnaissanceとOSINTの境界

- Passive、Active、Authenticatedの区分
- Asset Inventoryと外部公開面
- DNS、証明書、公開コード、SaaS
- Shadow IT
- 第三者情報の取扱い
- 能動検査へ進む承認ゲート

成果物: `Attack Surface Register`

### 第11章　Web・APIを仮説駆動で評価する

- チェックリスト駆動の限界
- 認証、認可、状態、データ境界
- Business LogicとAbuse Case
- API、Webhook、非同期処理
- 証拠の最小化
- 修正可能なFindingへ変換する

成果物: `Web/API Assessment Hypothesis Pack`
脆弱性別の詳細手順は `pentest-learning-book` へ委譲する。

### 第12章　Enterprise Identityとアクセス経路を評価する

- 人、端末、サービス、WorkloadのIdentity
- 権限グラフと委任
- 特権、MFA、Federation
- 認証情報ではなく権限関係を評価する
- 横展開可能性を安全に検証する
- Identityログとの接続

成果物: `Identity Attack Path Review`

### 第13章　Cloud、Container、CI/CD、Software Supply Chainを評価する

- Control PlaneとData Plane
- IAM Policy、Secret、Metadata
- Container境界とHost権限
- CI Token、Artifact、Dependency、Provenance
- SaaS連携
- AI AgentのTool Surface

成果物: `Platform and Supply Chain Assessment`

### 第14章　最小影響で成立性を確認し、止め、戻す

- 発見と侵害の違い
- Proof of VulnerabilityとProof of Impact
- データ取得を避ける確認
- 横展開、永続化、破壊を成功条件にしない
- 停止条件、緊急連絡、復旧
- 証拠の十分性

成果物: `Minimal-Impact Validation Record`

### 第15章　Finding、改修、再評価、リスク受容

- Findingの構造
- 根本原因と症状
- 技術影響と事業影響
- 暫定対策、恒久対策、代替統制
- 再テスト
- 残存リスクと受容判断

成果物: `Finding Report`、`Retest Record`

---

## 第III部　検知、ハンティング、対応

### 第16章　Telemetry ArchitectureとEvidence Readiness

- 観測目的からログを設計する
- Endpoint、Identity、Network、Cloud、Application
- 正規化、時刻、保持、完全性
- 収集不能と未観測の区別
- プライバシーとデータ最小化
- Incident Readiness

成果物: `Telemetry Coverage Map`

### 第17章　Detection Engineering

- Detection Hypothesis
- ATT&CK BehaviorからSignalへ落とす
- Data RequirementとCollection Gap
- Rule、Query、Threshold、Correlation
- False PositiveとFalse Negative
- Unit Test、Replay、Regression
- Detection as Code

成果物: `Detection Validation Record`

### 第18章　Threat Hunting

- IOC検索とTTP探索の違い
- 仮説、ベースライン、探索範囲
- Query、Pivot、Evidence Table
- 悪意と異常の区別
- Negative Findingの価値
- Detection Backlogへの還元

成果物: `Hunt Plan and Findings`

### 第19章　CSF 2.0に接続したIncident Response

- Govern、Identify、Protect、Detect、Respond、Recover
- 準備と役割
- 初動、トリアージ、封じ込め
- 根絶、復旧、再発防止
- 法務、顧客、経営との連携
- 事後学習

成果物: `Incident Action Plan`
一般的な連絡・復旧運用は `incident-response-basics-book` へ委譲する。

### 第20章　DFIRとタイムライン・因果再構成

- Evidence Question
- Disk、Memory、Network、Cloud、SaaS
- Timeline、Session、Identity、Process
- 原因、侵入経路、影響範囲
- 欠落証拠と不確実性
- Root CauseとContributing Factor

成果物: `Incident Timeline`、`Root Cause Analysis`

### 第21章　Purple TeamとControl Validation

- 脅威シナリオ
- 攻撃操作、観測、検知、対応
- Atomic TestとEnd-to-End Scenario
- 防止、検知、対応の分離評価
- 失敗の分類
- コントロール改善

成果物: `Control Validation Plan`

### 第22章　測定、優先順位、継続改善

- Coverage率の誤解
- Mean Time指標の限界
- Evidence Quality
- Detection Debt、Telemetry Debt
- Risk Reductionと投資判断
- 改善バックログと再検証

成果物: `Security Improvement Backlog`

---

## 第IV部　OSINTとCyber Threat Intelligence

### 第23章　Intelligence Requirementsと収集計画

- 誰が何をいつ判断するのか
- Priority Intelligence Requirements
- 既知事項、仮定、情報ギャップ
- Collection Requirement
- 収集、処理、分析、配布、フィードバック
- 技術・運用・戦略の時間軸

成果物: `Intelligence Requirement and Collection Plan`

### 第24章　OSINT、Provenance、情報源評価

- 一次情報と二次情報
- 公的機関、ベンダー、研究者、報道、SNS
- DNS、証明書、コード、企業情報
- 保存日時、原本、ハッシュ、翻訳
- 情報源の信頼性と内容の確からしさ
- 独立した裏付けと循環参照
- 偽情報、攪乱、削除・改変

成果物: `Evidence and Source Evaluation Table`

### 第25章　構造化分析、不確実性、アトリビューション

- 事実、仮定、判断、予測
- Analysis of Competing Hypotheses
- Key Assumptions Check
- Indicators and Signposts
- ベースレートと更新
- 確信度表現
- 技術クラスタ、組織、国家関与を分離する
- False FlagとDeception

成果物: `Structured Analytic Note`

### 第26章　CTIを構造化し、技術・経営へ配布する

- Actor、Campaign、Malware、Infrastructure、TTP、Victimology
- IOCの寿命とTTPの抽象度
- ATT&CK Mapping
- STIX/TAXII
- Tactical、Operational、Strategic Intelligence
- Key Judgments
- 技術勧告と経営含意

成果物: `CTI Report`、`Executive Brief`

---

## 第V部　AI時代の統合実践

### 第27章　AI・LLM・Agent Security

- Prompt InjectionとIndirect Prompt Injection
- RAG、Memory、Dataset、Model Supply Chain
- Tool CallingとExcessive Agency
- Secret、Privacy、Output Handling
- Agent間の信頼境界
- Approval、Audit、Kill Switch
- AI Security Verification Requirements

成果物: `AI/Agent Threat Model`

### 第28章　AIを使って分析するときの検証と汚染対策

- ログ要約、コード分析、OSINT、CTI支援
- 出典の消失と架空引用
- Prompt Injectionによる分析汚染
- 誤帰属と過剰確信
- Cross-check、Reproduction、Human Review
- AI利用記録と監査

成果物: `AI-Assisted Analysis Assurance Record`

### 第29章　統合ケーススタディ

- 架空組織と合成インシデント
- Intelligence Requirement
- RoEとThreat Model
- AssessmentとMinimal-Impact Validation
- Telemetry、Detection、Hunt
- Incident TimelineとRCA
- CTI ReportとExecutive Brief
- 改善、再テスト、Risk Acceptance

最終成果物:

- Rules of Engagement
- Threat Model
- Attack Surface Register
- Finding Report
- ATT&CK Behavior Map
- Telemetry Coverage Map
- Detection RuleとValidation Record
- Hunt Report
- Incident TimelineとRCA
- CTI Report
- Executive Brief
- Improvement Backlog

---

## 付録

- 付録A　安全・法的注意と責任ある開示
- 付録B　成果物テンプレート集
- 付録C　チェックリスト集
- 付録D　トラブルシューティングと停止フロー
- 付録E　用語集
- 付録F　図表索引
- 付録G　参考文献とSource Baseline
- 付録H　既存書籍への学習導線
- 付録I　演習データセットと再現手順
- 付録J　評価ルーブリック
