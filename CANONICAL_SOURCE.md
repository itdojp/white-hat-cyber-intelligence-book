# Canonical Authoring Source and Build Contract

## 決定

本リポジトリでは、次を編集元の正本とする。

- 章本文: `manuscript/`
- 付録本文: `appendices/`
- 読者向け入口・モジュール: ルート直下の`index.md`、`title.md`、`preface.md`、`quickstart.md`、`concept-map.md`等
- 企画・編集・安全・出典契約: ルート直下の大文字Markdownと`references/`
- 実務成果物テンプレート: `templates/`
- 演習定義・合成データ: 将来の`lab/`

`docs/`はGitHub Pages向け生成物であり、直接編集しない。

## 非破壊build契約

1. 同期・build前後で正本ファイルのSHA-256が変化してはならない。
2. 生成処理は`docs/`、`_site/`、`dist/`、一時ディレクトリだけへ書き込む。
3. `docs/`の生成対象はmanifestで列挙し、孤立した旧生成物を残さない。
4. `--check`はファイルを書き換えず、期待生成物との差分があれば失敗する。
5. CIは同期確認、リンク、構造、Unicode、出典鮮度、安全文字列、Jekyll buildを分離して表示する。
6. `main`上の公開生成物と正本のdriftを許容しない。

## book-formatter

共通レイアウト、include、asset、schemaは、`.book-formatter/revision.json`に固定したrevisionから同期する。`latest`や可変branchをCIで暗黙参照しない。

Phase 0では固定revisionと編集契約を確定する。共通コンポーネントの実体同期とJekyll buildが完了するまでは、Issue #1をcloseしない。
