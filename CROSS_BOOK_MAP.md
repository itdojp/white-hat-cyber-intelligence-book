# 既存書籍との役割分担

## 1. 判定記号

| 記号 | 意味 |
|---|---|
| OWN | 新書籍が中心的に詳述する |
| BRIDGE | 新書籍では統合に必要な範囲を説明し、専門書へ接続する |
| DELEGATE | 詳細を既存書籍へ委譲し、新書籍では要約と参照だけを置く |
| OUT | 新書籍の対象外 |

## 2. 書籍別の役割

| 既存リポジトリ | 既存書籍の役割 | 新書籍での扱い |
|---|---|---|
| `itdojp/pentest-learning-book` | Web、API、OAuth/OIDC、モバイル、クラウド、Linux/コンテナのPentest実践 | 方法論と成果物の接続はBRIDGE。個別ツール、脆弱性別手順、詳細ハンズオンはDELEGATE |
| `itdojp/it-infra-security-guide-book` | ネットワーク、OS、クラウド、コンテナの防御設計・実装 | コントロールと検知の接続はBRIDGE。設定・実装詳細はDELEGATE |
| `itdojp/incident-response-basics-book` | 切り分け、状況共有、復旧、ポストモーテムの基本 | サイバー侵害固有の証拠・封じ込め・DFIRはOWN。一般運用フレームはDELEGATE |
| `itdojp/practical-auth-book` | OAuth、OIDC、SAML等の認証・認可設計 | 攻撃面・観測点はBRIDGE。プロトコル詳細と安全な実装はDELEGATE |
| `itdojp/ai-agent-collaboration-book` | AIエージェントの権限、HITL、ログ、セキュリティ、ガバナンス | 脅威モデルと攻撃・検知はBRIDGE。業務導入・協働ガバナンスはDELEGATE |
| `itdojp/genai-repo-auditor` | リポジトリとAIエージェント表面の監査、証跡、分類 | ケーススタディと検査データの候補。製品・CLI手順はDELEGATE |
| `itdojp/security-privacy-literacy-book` | 一般利用者向けのセキュリティ・プライバシー | 読者の前提補強先。本文はDELEGATE |
| `itdojp/IT-infra-book` / `linux-infra-textbook2` | ITインフラ・Linuxの基礎 | 全面的にDELEGATE |
| `itdojp/cloud-infra-book` / `podman-book` | クラウド・コンテナの設計・運用 | 基盤知識と操作はDELEGATE |

## 3. テーマ別責任分担

| テーマ | 新書籍 | Pentest | Infra Security | Incident Basics | Practical Auth | AI Agent |
|---|---:|---:|---:|---:|---:|---:|
| 攻撃・防御・分析の統合モデル | OWN | BRIDGE | BRIDGE | BRIDGE | BRIDGE | BRIDGE |
| 法・倫理・許可・RoE | BRIDGE | OWN | BRIDGE | BRIDGE | OUT | BRIDGE |
| Web/API脆弱性の詳細 | BRIDGE | OWN | BRIDGE | OUT | BRIDGE | OUT |
| 認証プロトコルの詳細 | BRIDGE | BRIDGE | BRIDGE | OUT | OWN | OUT |
| クラウド・コンテナの設定強化 | BRIDGE | BRIDGE | OWN | OUT | OUT | OUT |
| Attack Surface管理 | OWN | BRIDGE | BRIDGE | OUT | BRIDGE | BRIDGE |
| ATT&CKと攻撃者行動モデル | OWN | BRIDGE | BRIDGE | BRIDGE | OUT | BRIDGE |
| Telemetry設計 | OWN | BRIDGE | BRIDGE | BRIDGE | BRIDGE | BRIDGE |
| Detection Engineering | OWN | BRIDGE | BRIDGE | BRIDGE | OUT | BRIDGE |
| Threat Hunting | OWN | OUT | BRIDGE | BRIDGE | OUT | OUT |
| 一般的な障害切り分け | BRIDGE | OUT | BRIDGE | OWN | OUT | OUT |
| サイバーIRとDFIR | OWN | BRIDGE | BRIDGE | BRIDGE | OUT | BRIDGE |
| OSINT収集と証拠管理 | OWN | BRIDGE | OUT | OUT | OUT | OUT |
| CTI、STIX/TAXII | OWN | OUT | BRIDGE | BRIDGE | OUT | OUT |
| 構造化分析、確信度、代替仮説 | OWN | OUT | OUT | BRIDGE | OUT | BRIDGE |
| アトリビューションの限界 | OWN | OUT | OUT | OUT | OUT | OUT |
| AI/LLM/Agent Security | BRIDGE | OUT | BRIDGE | BRIDGE | OUT | OWN |
| AI支援CTIの検証 | OWN | OUT | OUT | OUT | OUT | BRIDGE |
| 経営層向けDecision Brief | OWN | BRIDGE | BRIDGE | BRIDGE | OUT | BRIDGE |
| 統合演習 | OWN | BRIDGE | BRIDGE | BRIDGE | BRIDGE | BRIDGE |

## 4. 新書籍本文へ残す深さ

既存書籍へ委譲するテーマでも、次の最低限は新書籍内に残す。

1. そのテーマが統合ワークフローのどこに位置するか
2. 何を入力として、何を成果物として出すか
3. どの判断が必要か
4. どの証拠を保存するか
5. どの既存書籍・章に進むべきか
6. 新書籍へ戻った後、次にどの成果物へ接続するか

単なる外部リンク集にはしない。

## 5. 重複を許容する条件

次のいずれかを満たす場合に限り、短い重複説明を許容する。

- 読者が安全上の判断を誤る可能性がある
- 章を理解するために即時参照が必要である
- 用語の意味を本書固有の文脈に固定する必要がある
- 既存書籍の内容を、攻撃・防御・CTIの接続へ変換する必要がある

重複部分は原則として概念説明、判断表、データフロー、成果物例に限定し、詳細手順を複製しない。

## 6. 相互参照の実装順

1. 新書籍の章IDと章境界を確定する
2. 新書籍から既存書籍への参照を追加する
3. 参照先の安定URLまたはstable anchorを確認する
4. 既存書籍から新書籍への逆参照は別Issue・別PRで追加する
5. 既存書籍本文の統合・削除は、新書籍公開後の重複再監査で判断する

新書籍立ち上げPRに既存書籍の修正を混在させない。

## 7. 章単位の境界受け入れ条件

各章は、`OWN`、`BRIDGE`、`DELEGATE`を見出しまたは成果物内で明示し、次を満たす。

- OWNは、本書が判断基準、入力、出力、Evidence、責任を説明する
- BRIDGEは、統合に必要な最小概念と本書へ戻るHandoffを説明する
- DELEGATEは、専門書の安定した公開URLを示し、委譲先を読まなくても本章の中心論旨が途切れない
- 製品固有操作、脆弱性別Payload、認証プロトコル実装、一般IR運用、AI Agent業務ガバナンスを不必要に複製しない
- 参照先のHTTP、Route、AnchorをPR時と定期監査で確認する
- 委譲先が非公開、廃止、またはRoute変更となった場合は、Linkだけでなく必要なBRIDGE説明も再評価する

別書籍の内容変更は同じPRへ混在させず、必要な更新をSource Issueとして分離する。
