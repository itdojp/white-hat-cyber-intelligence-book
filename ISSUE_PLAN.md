# GitHub Issue計画

## 運用原則

- 親Issueを新規書籍立ち上げの正本Runbookとする
- 新規リポジトリ作成後は、実装Issueを原則として新規リポジトリ側へ作成する
- Issue → branch → Draft PR → 独立レビュー → CI → merge の順を守る
- 既存書籍の変更を新書籍PRへ混在させない
- mainへの直接pushを行わない
- 章本文、演習、出版基盤、既存書籍相互参照を別PRへ分ける

## Phase 0　リポジトリを立ち上げる

**Issue title**
`[Phase 0][Bootstrap] white-hat-cyber-intelligence-book の公開リポジトリと出版基盤を作成する`

### 作業

- `itdojp/white-hat-cyber-intelligence-book` をpublicで作成
- `it-engineer-knowledge-architecture/templates/book/` と `book-formatter` を使用
- `book-config.json` を現行スキーマに合わせて正本化
- Profile Bと8つの定義済みmoduleを設定
- README、LICENSE、CHANGELOG、SECURITY、CONTRIBUTINGを整備
- GitHub Pages、Book QA、dependency review等を既存標準へ合わせる
- 新規書籍は最初は `planned` または `draft` とし、ポータルcatalog登録は公開導線が成立してから行う

### 完了条件

- ローカルbuildと標準テストが成功
- canonical authoring sourceが一つに決まっている
- buildがcanonical sourceを破壊しない
- public URL、repository URL、licenseが整合
- mainへの直接pushなし

## Phase 1　企画・境界・出典を正本化する

**Issue title**
`[Phase 1][Editorial Contract] 企画、目次、既存書籍境界、安全方針、出典方針を正本化する`

### 投入ファイル

- `BOOK_PROPOSAL.md`
- `TOC.md`
- `CROSS_BOOK_MAP.md`
- `WRITING_GUIDE.md`
- `SOURCE_POLICY.md`
- `SAFETY_SCOPE.md`
- `LAB_ARCHITECTURE.md`
- `references/reference-baseline.md`

### 完了条件

- 章ID、Part、主要成果物が固定
- OWN / BRIDGE / DELEGATEがレビュー済み
- 危険な公開範囲が除外されている
- 一次資料の初期Baselineが確認されている

## Phase 2　代表4章を執筆する

**Issue title**
`[Phase 2][Representative Chapters] 統合・攻撃評価・検知・分析の代表4章を完成させる`

### 対象

- 第1章
- 第11章
- 第17章
- 第25章

### 完了条件

- 章契約に準拠
- 各章に成果物例がある
- 出典・安全・技術・編集レビューが別に完了
- 四章の用語と抽象度が一致

## Phase 3　成果物テンプレートを確立する

**Issue title**
`[Phase 3][Artifact Pack] RoE、Finding、Detection、CTI、Executive Briefのテンプレートを検証する`

### 対象

- Rules of Engagement
- Threat Model
- Finding Report
- Retest Record
- Detection Validation Record
- Hunt Report
- Incident Timeline
- CTI Report
- Executive Brief

### 完了条件

- 架空ケースで全テンプレートを記入できる
- 同じ事実から技術版と経営版を作成できる
- 事実、分析、仮定、確信度が分離される

## Phase 4　安全なラボ基盤を作る

**Issue title**
`[Phase 4][Lab Foundation] rootless・外向き通信既定拒否・合成データのラボ基盤を実装する`

### 完了条件

- Preflight、Initialize、Export、Destroyが自動化
- rootlessを検査
- 外向き通信の既定拒否を検査
- ManifestとHashを生成
- Tier 1の観測演習が再現できる
- 実Secretや第三者接続先がない

## Phase 5　Source RegistryとFreshness Gateを実装する

**Issue title**
`[Phase 5][Source Quality] 版・確認日・再確認条件を追跡するSource Registryを実装する`

### 完了条件

- Source Note Schemaがある
- 重要フレームワークの版が追跡される
- 期限切れSourceをCIまたはレポートで検知する
- AI生成URLを未確認のまま登録できない運用契約がある

## Phase 6　第0部・第I部を完成する

**Issue title**
`[Phase 6][Manuscript] 序部とThreat-Informed Security基盤を完成させる`

対象: 第0〜8章

## Phase 7　第II部を完成する

**Issue title**
`[Phase 7][Manuscript] 安全な攻撃評価編を完成させる`

対象: 第9〜15章

## Phase 8　第III部を完成する

**Issue title**
`[Phase 8][Manuscript] 検知・ハンティング・対応編を完成させる`

対象: 第16〜22章

## Phase 9　第IV部を完成する

**Issue title**
`[Phase 9][Manuscript] OSINT・CTI・構造化分析編を完成させる`

対象: 第23〜26章

## Phase 10　第V部と統合ケースを完成する

**Issue title**
`[Phase 10][Capstone] AIセキュリティと統合ケーススタディを完成させる`

対象: 第27〜29章

### 完了条件

- 架空組織と合成データのみで完結
- 第9〜28章の成果物を一つのケースへ統合
- 技術・CTI・経営の三種類の出力が一致
- 改善後の再検証まで実行可能

## Phase 11　既存書籍との相互参照を追加する

**Issue title**
`[Phase 11][Cross-Book Links] 安定章IDに基づき既存書籍との双方向導線を追加する`

### 注意

- 書籍ごとに別Issue・別PR
- 既存本文の大規模再編は行わない
- stable anchorとリンク検査を追加
- 重複削除は公開後の別監査

## Phase 12　独立レビューと公開判定

**Issue title**
`[Phase 12][Release Readiness] 技術・安全・出典・教育・出版の独立レビューを完了する`

### レビュー軸

- 技術的正確性
- 法務・倫理・安全性
- 出典と鮮度
- CTI分析基準
- 教育設計
- 再現性
- Series UX
- Accessibility
- ライセンス

### 完了条件

- P0/P1指摘が0
- 全演習がclean環境から再現
- 全リンク・図・メタデータ・buildが成功
- 実Secret・個人情報・第三者ターゲットが0
- 公開版のVersionとChangelogが確定

## Codex CLI向け停止条件

- orgリポジトリ作成権限がない
- Series UXまたはbook-formatterの現行契約が不明
- 既存の同名リポジトリまたは重複Issueを発見
- mainへ直接pushする必要がある
- 外部ターゲットへの通信が必要
- 実Secretを必要とする
- 高リスクな攻撃手順を公開しなければ演習が成立しない
- 法令・ライセンス・出典の扱いを判断できない

停止時は、完了扱いにせず、確認済み証跡、未解決事項、必要なoperator actionをIssueへ記録する。
