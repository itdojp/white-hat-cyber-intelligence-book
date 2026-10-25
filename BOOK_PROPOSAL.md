# BOOK PROPOSAL

## 1. 基本情報

| 項目 | 内容 |
|---|---|
| リポジトリ | `itdojp/white-hat-cyber-intelligence-book` |
| 書籍名 | ホワイトハッカーとサイバーインテリジェンス実践体系 |
| 副題 | 攻撃者の行動を理解し、検証・検知・対応・経営判断につなげる |
| 著者・発行主体 | ITDO Inc.（株式会社アイティードゥ） |
| 言語 | 日本語 |
| 現在版 | `0.1.0` 公開Draft |
| 次期版 | `v1.0.0` Release準備 |
| 公開範囲 | Public |
| ライセンス | CC BY-NC-SA 4.0（商用利用は別契約） |
| Series UX | Profile B: Practical / Reference |
| 想定本文量 | 420〜520ページ相当。演習データ・テンプレート・更新情報はリポジトリへ分離 |

書籍名と副題は現行の正本名である。名称変更は、URL、Citation、Series catalog、配布物への影響を確認した専用の意思決定を経るまで確定しない。

## 2. 現在地

2026年10月25日時点で、第0章から第29章までの30章と、`ART-33 Final Security Decision Portfolio Index`を`main`へ公開済みである。

本文の主要制作段階は完了したが、次は未完である。

- 付録B、C、E、F、G、I、Jの最終化
- Release前Source freshnessとLicenseの意味確認
- ATT&CK等の更新Triggerへの対応
- 第27〜29章のPart V横断Review
- 専門読者による人間試行
- 配布物、Accessibility、Release Candidateの確認
- `v1.0.0` Release

30章の公開、個別章のCI成功、全書Release完了を同じ状態として扱わない。現在の完了条件と作業順はIssue #17、#25、#212を正とする。

## 3. 問題設定

サイバーセキュリティの実務と学習は、次の領域ごとに分断されやすい。

- ペネトレーションテストと脆弱性診断
- セキュリティ設計と防御運用
- Detection EngineeringとThreat Hunting
- Incident ResponseとDFIR
- OSINTとCyber Threat Intelligence
- AI・AIエージェントのセキュリティ
- 経営層のリスク判断

個別領域を学んでも、攻撃者の行動をどのように仮説化し、許可された環境で検証し、どのログで観測し、どのように検知・対応し、最後に経営判断へ変換するかが接続されていないことが多い。

AIがCode、Finding、分析文、運用候補を大量に生成できるようになっても、候補と確認事実、能力と権限、出力とEvidence、修正案と検証済みControlを区別する必要はなくならない。むしろ、出所、版、判断主体、停止条件、再評価を追跡する重要性は高まる。

本書は、この接続と判断の品質を主題とする。

## 4. 中心命題

> 攻撃手法を知ること自体を目的にせず、脅威を理解し、合法かつ安全に検証し、観測・検知・対応・意思決定へ変換できることを到達点とする。

本書の共通ループは次の通りである。

```text
判断要求を定義する
    ↓
資産・信頼境界・脅威を把握する
    ↓
攻撃経路と観測仮説を立てる
    ↓
許可された隔離環境で最小限に検証する
    ↓
ログ・証拠・痕跡を評価する
    ↓
検知・対応・コントロールを改善する
    ↓
確信度付きのインテリジェンスに変換する
    ↓
技術・運用・経営判断を記録する
    ↓
再評価する
```

## 5. 本書の位置付け

本書は、経験を持つIT・セキュリティ実務者が、攻撃評価、Telemetry、Detection、IR / DFIR、CTI、AI Securityを、Evidenceと意思決定で接続するための専門実務リファレンスである。

### 5.1 主対象

- SOC、CSIRT、Detection Engineering、Threat Hunting、IR、DFIR、CTIの実務者
- Security Architecture、Cloud Security、Identity Security、Platform Securityの担当者
- Pentestや脆弱性管理の成果を、検知、改善、経営判断へ接続する担当者
- セキュリティへ役割を広げる、経験あるインフラ、SRE、DevOps、開発技術者
- CISO室、Security Program責任者、技術リスクを判断するCTO・CISO

### 5.2 副対象

- 社内教育や実務標準化のために、成果物と評価基準を設計する担当者
- AI Agentを使ってセキュリティ分析・開発・運用を支援し、出所と権限を管理する担当者

### 5.3 対象外

- コンピュータやネットワーク自体を初めて学ぶための入門書
- CTF解法集、Exploit Development、攻撃コマンドのカタログ
- 特定製品のGUIやCLIを網羅する操作手順書
- 法律相談や個別案件の法的判断の代替
- 実在Actorへの断定を目的とするアトリビューション本

## 6. 初心者向け書籍との分離

初心者向け書籍は、本書から専門用語やFieldを削った短縮版にはしない。別の読者、別のCase、別の成果物を持つ独立書籍として企画する。

初心者向け書籍の対象は、コンピュータ初心者ではなく、IT実務経験はあるがセキュリティ業務の全体像を知らない技術者・管理者とする。

初心者向け書籍がOWNする中心ループは次である。

```text
何を守るか
  → どんな危険があるか
  → 何を観測できるか
  → 何が分からないか
  → 誰が判断するか
  → どの専門家へ引き継ぐか
```

初心者向け書籍とは、次を共有しない。

- Case ID、Artifact ID、Evidence ID
- 本書固有の有限Status
- JSON Schema、fixture、contract、回帰検査
- Authority、Review、受領を示す記録
- 本書の完全合成Caseを簡略化した同一Case

共通化するのは、中心となる意思決定ループと用語上の対応だけである。新しいRepository、URL、正式書名が存在するまで、本書の公開面へ未成立のLinkを置かない。

## 7. 既存書籍との位置付け

本書は既存書籍の統合上位層であり、既存内容を再収録する本ではない。

- `pentest-learning-book`: 攻撃評価技術とTool操作の深掘り
- `it-infra-security-guide-book`: インフラ防御設計と実装
- `incident-response-basics-book`: 障害・Incident運用の基礎
- `practical-auth-book`: 認証・認可Protocolと実装
- `ai-agent-collaboration-book`: AI Agentの権限、HITL、Governance
- `genai-repo-auditor`: AI・Repository surfaceの機械的監査とEvidence

本書が独自に詳述する領域は次である。

1. 攻撃・防御・インテリジェンスの統合Workflow
2. Threat-Informed Defenseの実務化
3. Detection EngineeringとThreat Hunting
4. CTI、OSINT、情報源評価、構造化分析
5. 確信度、不確実性、代替仮説を含む分析文書
6. 技術的事実から経営判断への変換
7. AI Application / AgentのTrust BoundaryとAI支援分析の保証
8. 全工程を接続する安全な統合Caseと最終Portfolio

詳細な境界は`CROSS_BOOK_MAP.md`と付録Jを正とする。

## 8. 前提知識

- Linuxの基本操作
- TCP/IP、DNS、HTTPの基礎
- GitとMarkdownの基礎
- 認証・認可、Cloud、Containerの概念レベルの理解
- インフラ、クラウド、Web、開発、運用のいずれかの実務経験

不足する前提は既存書籍への学習導線で補う。基礎技術を本書内で全面的に再説明しない。

## 9. 読了後の到達目標

読者は、次を一連の成果物として作成できる。

1. 権限、対象、禁止事項、停止条件を含むRules of Engagement
2. 資産・信頼境界・攻撃面を表すThreat Model
3. 攻撃経路と必要Telemetryの対応表
4. 最小影響での検証記録とFinding Report
5. ATT&CKに対応付けたDetection Hypothesis
6. Test可能なDetection RuleとValidation Record
7. Incident Timelineと原因・影響範囲の分析
8. 出典、確信度、代替仮説を含むCTI Report
9. AI / Agent Threat ModelとAI支援分析のAssurance Record
10. 経営層向けDecision Brief
11. 改善後のRetestとReassessment
12. 元のStatusとGapを保持するFinal Security Decision Portfolio

## 10. 三層構造

本書は、読者向け説明と実務記録、機械検査を分離する。

| 層 | 内容 | 責任 |
|---|---|---|
| Human-readable manuscript | 概念、判断、根拠、反例、実務上の含意 | 読者が中心論旨を理解できること |
| Professional artifacts | Template、完全合成Case、Checklist、Rubric | 実務記録とReview条件を作れること |
| Machine-verifiable knowledge layer | JSON、Schema、fixture、contract、回帰検査 | 参照、版、状態、安全境界、公開面の漂流を検出すること |

機械検証層は削除しない。ただし、機械検査の成功を、実環境の安全性、人間の承認、Controlの有効性、未知入力への一般化へ拡張しない。

## 11. 差別化

### 11.1 Tool catalogにしない

Commandや製品UIは更新が速い。本文は、問い、判断、Evidence、失敗条件、成果物を中心にする。Tool固有の手順は演習READMEまたは既存専門書へ委譲する。

### 11.2 攻撃と検知を対にする

攻撃技法を紹介する場合、最低限次を同じ章または相互参照先で扱う。

- 成立条件
- 業務上の影響
- 観測可能な痕跡
- 必要なLog source
- Detection hypothesis
- 防止・緩和策
- 安全な再現範囲

### 11.3 インテリジェンスを情報収集で終わらせない

OSINT、IOC、News、脆弱性情報を集めただけでは完成としない。判断要求、Source評価、代替仮説、確信度、情報Gap、含意、推奨措置までを成果物とする。

### 11.4 経営判断へ変換する

技術的な深刻度と、事業上の優先度を分離する。修正、監視強化、代替Control、Risk acceptance、Service停止、通知などの選択肢を比較する。

### 11.5 AI出力をEvidenceやAuthorityへ自動昇格させない

AIが生成したCode、Finding、要約、推奨、Tool選択を、Source、確認事実、人間の承認、実行許可として扱わない。入力、Model、Memory、Tool、Authority、Approval、Stop、Auditを別々に記録する。

## 12. 書籍構造

| 部 | 主題 | 主要成果物 |
|---|---|---|
| 序部 | 学び方、役割、法・倫理、能力評価 | 学習計画、権限境界 |
| 第I部 | 資産、脅威、ATT&CK、脆弱性優先度、Lab | Threat Model、Evidence Plan |
| 第II部 | 安全な攻撃評価と報告 | RoE、Finding、Retest Record |
| 第III部 | Telemetry、Detection、Hunting、IR、DFIR | Detection Rule、Timeline、RCA |
| 第IV部 | OSINT、CTI、構造化分析、戦略判断 | Evidence Table、CTI Report |
| 第V部 | AI Security、AI支援分析、統合演習 | AI Threat Model、Assurance Record、最終Portfolio |

詳細は`TOC.md`を正とする。

## 13. 学習設計

- 章単位ではなく成果物単位で進める
- 読者の役割と判断要求に応じた複数のRouteを第0章で定義する
- 各章に攻撃者、防御者、分析者、意思決定者の接続を示す
- 各部の横断Mapと最終PortfolioでHandoffと非継承を確認する
- 演習は隔離された自己所有環境または合成データのみを使用する
- 解答は単一の正解ではなく、Evidence、Assumption、Judgment、Gap、再評価の妥当性をRubricで評価する
- Quick Startは、専門実務書の記録体系へ最小単位から入るためのOnboardingとする

## 14. Series UX設定

Profile Bを採用する。実務参照性を主目的とし、学習導線を追加Moduleで補う。

有効化するModule:

- `quickStart`
- `readingGuide`
- `checklistPack`
- `troubleshootingFlow`
- `conceptMap`
- `figureIndex`
- `legalNotice`
- `glossary`

設定の正本は`book-config.json`とする。未定義Moduleを追加しない。

## 15. 安全性と公開範囲

本書は、防御・教育目的であっても、そのまま第三者への侵害に転用しやすい手順を無制限に掲載しない。

- 実在第三者へのScan、認証試行、Access、追跡を演習対象にしない
- 本番環境を標準演習対象にしない
- 実Data、実Account、実Tokenを使用しない
- 破壊、Persistence、隠蔽、Evasion、Credential窃取の実装手順を掲載しない
- MalwareやC2の実運用を演習に含めない
- 脆弱性確認は最小影響で停止し、Data取得や横展開を成功条件にしない
- 公開Levelは`SAFETY_SCOPE.md`に従う

## 16. 出典と鮮度

- 一次情報を優先する
- Version、公開日、確認日を記録する
- 時点依存情報は本文から更新Registryへ分離する
- ATT&CK、NIST、OWASP、OASIS、FIRST、CISA、IPA、e-Gov等の基準文書を追跡する
- CTIではSource reliabilityと情報内容のcredibilityを分離する
- AI生成要約を原典の代替にしない
- 更新Trigger成立時は、意味を確認せず`checkedAt`だけを進めない

詳細は`SOURCE_POLICY.md`と`references/reference-baseline.md`を正とする。

## 17. 代表章Gateの履歴

全章執筆前には、次の4章を代表章として完成し、統合概念、攻撃評価、防御、分析の粒度を固定した。

1. 第1章: 攻撃・防御・インテリジェンスを一つの業務として捉える
2. 第11章: Web・APIを仮説駆動で評価する
3. 第17章: Detection Engineering
4. 第25章: 構造化分析、不確実性、アトリビューション

これは完了済みの歴史的Gateであり、現在の作業状態ではない。現在は30章公開後の付録、横断Review、Source freshness、人間読者試行、Release工程にある。代表章Gateの詳細は`REPRESENTATIVE_CHAPTER_PLAN.md`と`REPRESENTATIVE_CHAPTER_GATE.md`を参照する。

## 18. v1.0完成条件

### 内容

- 第0〜29章と付録A〜Jが正本へ登録されている
- 全章に学習目標、前提、本文、成果物、まとめ、次章への接続がある
- 既存書籍との重複が`CROSS_BOOK_MAP.md`と付録Jに沿って制御されている
- 全ての時点依存記述にVersionまたは確認日がある
- Fact、Judgment、Assumption、Forecast、Recommendationが区別されている
- 第27〜29章のPart V横断Reviewが完了している

### 演習

- 標準Labがrootlessかつ隔離可能である
- 初期状態へ戻せる
- 外部への能動通信を標準で必要としない
- 合成Log・合成Dataで必修課題を完結できる
- 各演習に停止条件、Cleanup、Evidence一覧がある

### 品質

- Markdown、Link、Metadata、出版Buildが成功する
- 技術、編集、安全、Source、CTI分析、教育設計、配布のReviewを分離して実施する
- 専門読者による人間試行を行い、P0/P1を解消する
- 公開前に第三者Systemへ向く文字列、実Token、PIIが含まれないことを検査する
- Source freshness、License、Third-party notice、依存監査、Accessibilityを確認する
- `v1.0.0-rc.1`を経て`v1.0.0`を公開する

## 19. v1.0前の変更方針

- 新章を追加しない
- 全章の大規模な再構成を行わない
- 本文の専門性を初心者向けに薄めない
- Releaseに必要な位置付け、Source freshness、付録、横断Review、Reader trial、配布整備へ集中する
- AI能力評価、Agent-scale開発、Formal Verification、SCS評価制度等の詳細Caseは、原則としてv1.1以降へ送る
- 初心者向け書籍は企画と代表章の試作までを並行可能とし、全章執筆は本書v1.0を優先する

## 20. 非目標

- ゼロデイ発見やExploit Developmentの専門書
- Malware開発・C2運用の手引き
- Kali Linuxや各種Toolの網羅的Manual
- CTF解法集
- 法律相談の代替
- 実在する攻撃主体の断定を目的とするAttribution本
- 製品選定Ranking
- 資格試験対策書
- AIが自律的に実務判断・実行許可を確定するSystem

## 21. 現在のReleaseマイルストーン

1. 付録B/C/Iを通常Review・採用する
2. 付録E/F/Gの用語、図表、Source Baselineを完成する
3. 付録Jで既存専門書と将来の初心者向け書籍との責任境界を確定する
4. Release前Source freshnessとATT&CK更新Triggerを処理する
5. 第27〜29章のPart V横断Reviewを完了する
6. 専門読者による人間試行を完了する
7. 依存、License、配布物、AccessibilityのRelease blockerを解消する
8. `v1.0.0-rc.1`を公開して独立Reviewする
9. `v1.0.0`を公開し、継続更新へ移行する

実行単位は`ISSUE_PLAN.md`、Issue #17、#25、#212に定義する。
