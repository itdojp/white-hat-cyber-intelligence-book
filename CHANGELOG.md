# Changelog

本書はSemantic Versioningを参考に版を管理します。本文、図表、演習、テンプレート、出版基盤の主要変更を記録します。

## Unreleased

### Added

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

### Changed

- Source Note IDと各章の対応をCIで相互検証するように変更
- `package.json`とlockfileのLicense metadataを本文・コードの適用範囲に合わせて更新
- GitHubの編集Linkが生成済み`docs/`ではなくcanonical `source_path`を指すように共有layoutへ決定的変換を適用
- `book-formatter`を監査済みrevision `764f644850c21983c96919d0e13706413d59c089`、shared component version `3.2.3`へ更新

### Fixed

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
