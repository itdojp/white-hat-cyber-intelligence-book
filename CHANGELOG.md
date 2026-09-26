# Changelog

## 第III部横断読解（Issue #168）

- 七教材の直接ID参照、方法参照、非継承、未配達、Gapと改善判断を読む補助教材を追加。
- 固定Layer A契約と正負対比を生成前検査へ接続。既存章の原稿・教材・Source・共有構文/安全文法は変更しない。

本書はSemantic Versioningを参考に版を管理します。本文、図表、演習、テンプレート、出版基盤の主要変更を記録します。

## Unreleased

### Added

- [第22章](manuscript/22-measurement-improvement.md)、ART-28、十Metric・八Item・七Statusの完全合成Case、閉Schemaと有限公開前検査を追加。母集団、欠測、時間の統計量、品質、検証とRisk判断を分離し、親の実権限・未配達・旧Failedを保持。五Sourceの用途限定確認を2026-09-26に記録。

- [第21章](manuscript/21-purple-team-validation.md)、ART-27、十Scenario・五層・六Failureの完全合成Case、閉Schemaと有限公開前検査を追加。Expected/Actual、観測された部分充足とUnknown、権限停止、比較可能なRetestを分離し、親のEvidence・実権限・未配達・原因未確定を保持。四Sourceの用途限定確認を2026-09-25に記録。

- [第20章](manuscript/20-dfir-timeline-causality.md)、ART-07拡張とART-26、五Receipt・二Cutoff・六Claimの完全合成Case、閉Schemaと有限公開前検査を追加。原時刻・不確かさ・後着Evidence・代替説明・原因未確定を分け、親19のEvidence・権限・未配達を保持。三Sourceの用途限定確認を2026-09-25に記録。

- [第19章](manuscript/19-incident-response.md)、ART-25、十二の完全合成対比、七状態の有限判断・公開前検査を追加。宣言・Scope・保存・選択肢・復旧検証・残余リスクを分離し、親のEvidence・権限・未配達を変更しない。二NIST Sourceは第19章用途だけを2026-09-23に再確認し、過去の記録を保持。

- [第18章](manuscript/18-threat-hunting.md)、既存ART-06拡張、十二の完全合成対比、閉Schemaと有限Query/読解契約を追加。五Result、Coverage、Negative Finding、代替説明、Backlog、再評価を接続し、親16/17のEvidence・権限・未配達を変更しない。

- [第16章](manuscript/16-telemetry-evidence-readiness.md)、ART-24、十の完全合成対比、閉Schemaと有限読解契約を追加。七状態と時刻・同一性・保持・Privacy・Gapを分け、親5/6/15/17のEvidence・権限・未配達は変更しない。一次資料は限定節のみ再確認。

- [第II部の横断対応表](cases/part-ii-assessment-risk-map.md)と有限検査を追加。直接ID参照と別Case・別対象への方法参照を分け、親Draft・期限・未配達Handoffを保持する。第11章の独立Case、第15章の七つの独立判断例、既存章の正本を変更しない。

- [第12章](manuscript/12-enterprise-identity.md)、ART-20 Identity Attack Path Review、四Principal・六Path stateの完全合成Graphと閉じたSchema・有限Layer A検査を追加。認証の強さ、権限関係、Evidence、評価実施の許可を分け、Federation非該当の比較ではIssuer / Audience / RPをnullで明示する。有限比較の成功を実認証・実行許可・親Gap解消の証拠にしない。

- [第9章](manuscript/09-engagement-roe.md)、既存ART-02の完成、三Objectの完全合成RoE計画・閉じたSchema・有限Layer A検査を追加。期限経過した親Authorizationを更新せずDraft / Do not proceedとし、記録整合性と実行許可を分ける。NIST SP800-115を限定参照し、実使用する法令・IPA・WSTGのみ再監査。既存章のSource版・歴史的記録は保持する。

- [第8章](manuscript/08-safe-lab-evidence.md)、ART-18 Lab Safety and Evidence Plan、三Runの合成Plan・Control receipts・Evidence manifest・閉じたSchemaと読み取り専用Replayを追加。Runningを含む八状態と三判定を分け、失敗後のCleanup成功を正常完了へ置き換えない。実Runtimeは実行せず、親の状態・Authorityを更新しない。

- [第7章](manuscript/07-vulnerability-prioritization.md)、ART-17 Vulnerability Prioritization Record、六件の合成判断と公開Source Snapshotを追加。導入・到達性・統制・判断は合成、EPSS / KEVは固定公開入力として分離し、CVEの有無にかかわらず未検証の義務適用はUnverifiedに保持する。

- 第6章、ART-16、完全合成Signal Flowと同一Flowの観測段階・時刻・保持・Gap検査を追加。NIST / OAuthの採用範囲を限定し、親Caseの観測結果は更新しない。

- 第5章、ART-15、完全合成Behavior Map、ATT&CK v19.2固定metadataと共有Publication Projectionを使う章契約を追加。
- PublicリポジトリとPhase 0 Runbookを作成
- 最小READMEで`main`を初期化し、以後をPull Request運用へ移行
- 書籍企画、詳細目次、既存書籍との境界、安全方針、ラボ設計を正本化
- `book-config.json`にProfile B、全30章（第0章〜第29章）、10付録を定義
- canonical authoring sourceと非破壊build契約を定義
- 執筆、出典・鮮度、ガバナンス、ライセンス、Security、Contribution方針を追加
- 主要一次資料20件のSource Registry、章対応、更新条件を追加
- 第0章・第1章の初稿を追加
- 9種類の実務成果物テンプレートを追加
- 追跡対象Workflowを含むSecret・Unicode・Markdown・Local link・Source mapping契約検査を追加
- `book-formatter` revision `69eb5c12f5a750b65614bc9bbbc3d7abd5aa6f6c`を固定
- shared component version `3.2.2`のlayout、include、CSS、JavaScript全10ファイルをGit blob SHAで固定
- 正本から一時`docs/`を生成する決定的・非破壊site-source generatorを追加
- Ruby 3.3 / Jekyll依存と`Gemfile.lock`を追加
- 固定SHAのGitHub Actionsだけを許可するWorkflow契約検査を追加
- `Book Contract`、`Book QA`、GitHub Pages deployment workflowを追加
- Jekyll built-site smoke testとPreview artifactを追加
- 第4章「資産、信頼境界、攻撃面、脅威モデル」、ART-03 Threat Model、合成Case、fail-closed Chapter contractを追加
- Editorial InputのPackage identity、Target別Candidate / Disposition、決定的Summary、ZIP安全検証を持つManifest契約を追加

### Changed

- 第12章のSource baselineにNIST SP 800-63-4 / 63A-4 / 63B-4 / 63C-4（2025-07-31 Final）とRFC9700 / BCP240を追加し、既存SP800-207Aの章対応を拡張。読者は自然人のAssuranceをWorkload適合へ一般化せず、MFAと認可、IssuerとAudienceを別に判断する。採用節と限界は[第12章Source Review Note](references/ch12-source-review-2026-09-15.md)で確認できる。既存Sourceの版・親章の意味とRegistry一括監査日は保持する。

- 第8章向けにNIST SP 800-86 / 800-190の限定原則を追加し、Berkeley Protocol 2022 editionの取得・取扱い記録を再確認。Hashの同一性と真実性・法的証拠能力を区別し、日不明の公開日はnullを維持する。第25章の版と意味は不変、Registry一括監査日も据置き。詳細は[第8章Source Review Note](references/ch08-source-review-2026-09-13.md)に記録。

- SRC-EPSS-001をv4 model lineからv5（Model identifier: v2026.06.15）へ意味変更として更新。読者はモデル境界をまたぐScore差を脅威変化だけと解釈せず、Modelと取得時点を対にして扱う。v5運用開始は2026-06-15であり、EPSSを個別組織の侵害確率へ置き換えない。第7章の値は2026-09-11のSnapshotへ限定し、安定本文の現行値としない。
- 第7章のCVSS標準4.0 / 文書1.2、CWE4.20、CVE定義、KEVとCISA告知の採用範囲を[Source Review Note](references/ch07-source-review-2026-09-12.md)に記録。CVSSの教材値は著者の合成評価で、実CVEの公表評価ではない。未取得Directive原文から詳細適用・例外・数値期限を推測せず、第11章のOWASP Awareness用途と既存の親Caseは変更しない。

- Source Note IDと各章の対応をCIで相互検証するように変更
- `package.json`とlockfileのLicense metadataを本文・コードの適用範囲に合わせて更新
- GitHubの編集Linkが生成済み`docs/`ではなくcanonical `source_path`を指すように共有layoutへ決定的変換を適用
- `book-formatter`を監査済みrevision `cf3f75ee9b1e200e4b6cece23501cb9c83170ec7`、shared component version `3.2.3`へ更新
- 第4章の判断要求からThreat ModelへのTrace根拠としてNIST CSF 2.0、NIST SP 800-30 Rev.1、OWASP Threat Modeling Projectを再監査し、Source Registryの章対応、確認日、次回確認条件を更新。Framework mappingは実装、検証、完全性の証明ではないことを明記

### Fixed

- 固定formatterの`js-yaml`依存を修正版3.15.2 / 4.3.2へ更新し、GHSA-2883-xcg3-v3hhの空mapping merge予算回避に対応。書籍本文と共有出版部品は変更なし（Issue #115）。

- `.github/workflows/`がSecret検査から除外される問題を修正
- `node_modules`等の第三者・生成DirectoryがRepository固有検査へ混入する問題を修正
- 第0章・第1章のSource Registry章対応漏れを修正
- 代表章計画の「全29章」を「全30章（第0章〜第29章）」へ修正
- mobile/tablet幅でsidebarが初期表示から本文を覆うCSS cascade回帰を修正

### Pending

- 最新headに対する独立した技術・安全・出典・編集レビュー
- GitHub Pagesの初回deployと公開URL確認
- Repository Rules、merge method、Security settingsの管理者設定
- Phase 1以降のIssue群作成と代表4章の完成

## 0.1.0-draft — 2026-07-25

- 書籍名を「ホワイトハッカーとサイバーインテリジェンス実践体系」に決定
- 副題を「攻撃者の行動を理解し、検証・検知・対応・経営判断につなげる」に決定
- Series UX Profile Bを採用

## 2026-09-15 第13章 Platform / Supply Chain

### Added

- 第13章の本文・ART-21・完全合成記入例、八Chainの供給JSON/閉Schema、有限Layer A、Source Reviewと公開導線を追加。

### Changed

- SourceからRuntimeまでの追跡と五状態を読者向けに明示。署名、Trust、Compliance、Safety、実施許可を分離し、SSDF1.1 Final/SLSA1.2 Approved、SPDX版表記、Container歴史的原則の利用範囲を記録。親の本文・許可・Evidence、共有Policy/Projectionと依存は変更しない。

## 2026-09-16 第14章 最小影響Validation

### Added

- 第14章の本文・ART-22・完全合成記入例、八記録の供給JSON/閉Schema、有限Layer A、Source Reviewと公開導線を追加。

### Changed

- 六Resultと四Method、未実施と停止、Cleanup/Residualによる記録完了を分離。実影響・安全性・許可を主張せず、NIST SP800-115/WSTG4.2の限定採用scopeを過去Source利用記録に追記。親の本文・許可・Evidence、共有Policy/Projection、formatter pinと依存は変更しない。

## 2026-09-17 第15章 Finding・Retest・リスク受容

### Added

- 第15章本文・ART-23・完全合成記入例、七Finding/五Retestの供給JSONと閉Schema、有限Layer A、Source Review、公開導線。

### Changed

- ART-04を既存見出し・URLを保持して拡張。六Status/五ResultとClosedの二経路を分離し、権限不足を受容で上書きしない。IPA2024/WSTG4.2 Reporting/CVSS4.0の限定採用scopeを過去Source notesへ追記。親本文/許可/Evidence、共有Policy/Projection、formatter pin/依存は変更しない。

- 第15章独立レビューの指摘により、受容対象版、独立した供給Delegation、構造化Temporaryレビューを直接参照する。裸のIDや同一欄の自己申告だけでAccepted/Closed/Mitigatedにしない。
