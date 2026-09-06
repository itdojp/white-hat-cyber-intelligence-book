# Canonical Authoring Source and Build Contract

## 決定

本リポジトリでは、次を編集元の正本とする。

- 章本文: `manuscript/`
- 付録本文: `appendices/`
- 読者向け入口・モジュール: ルート直下の`index.md`、`title.md`、`preface.md`、`quickstart.md`、`concept-map.md`等
- 企画・編集・安全・出典契約: ルート直下の大文字Markdownと`references/`
- 実務成果物テンプレート: `templates/`
- 合成Caseと記入例: `cases/`
- 演習定義・合成データ: 将来の`lab/`
- 機械可読Schema: `schemas/`
- 機械可読な書籍構造: `book-config.json`
- Editorial InputのPackage / Target / Candidate / Disposition: `editorial-input-manifest.json`
- Editorial Input ManifestのSchema: `schemas/editorial-input-manifest.schema.json`
- 公開ページ追加Registry: `site-pages.json`
- 共通出版部品の固定情報: `.book-formatter/revision.json`

`docs/`はGitHub Pages向けの一時生成物であり、直接編集もGit管理もしない。CIとローカルbuildは、正本から毎回`docs/`を再生成する。

`EDITORIAL_INPUT_MANIFEST.md`は`editorial-input-manifest.json`から生成する人間向け索引であり、直接編集しない。外部のZIP、`.predraft.md`、Codex Goal Packageは正本ではなく、Repositoryへcommitしない。

## 生成コマンド

```bash
npm ci
npm run check:docs-sync
npm run sync:docs
bundle install
npm run build
```

- `npm run check:docs-sync`: `scripts/sync_book_site.py`を使用して一時ディレクトリへ2回生成し、全生成ファイルのSHA-256一致と全追跡ファイルの非変更を確認する
- `npm run sync:docs`: 許可された生成先`docs/`だけを削除し、正本と`site-pages.json`から再生成する
- `npm run build`: `docs/`を生成し、Jekyllで`_site/`へbuildする

固定済み`book-formatter` checkoutを使う場合は、`BOOK_FORMATTER_DIR`へpathを指定する。

```bash
BOOK_FORMATTER_DIR=../book-formatter npm run check:docs-sync
BOOK_FORMATTER_DIR=../book-formatter npm run build
```

未指定時は、固定commitの個別ファイルを取得し、Git blob SHAを検証してから使用する。可変branchや`latest`は参照しない。

## 公開ページRegistry

`scripts/sync_site_source.py`は、Phase 0で監査した共通生成器である。`scripts/sync_book_site.py`は、この生成器を置換せず、`site-pages.json`に登録した追加ページとCanonical Directoryを検証して注入する薄い拡張層である。

`site-pages.json`には次だけを置く。

- Canonical Directoryの追加
- 正本Sourceと生成先Destinationの対応
- Navigation sectionとorder
- Directory route
- JSON形式の非実行・読み取り専用教材と`downloads/`配下の公開先

RegistryのSchemaは`schemas/site-pages.schema.json`で管理する。新しい章や成果物を公開するPRは、本文、TemplateまたはCase、Registry、検査を同じPRで更新する。

`staticFiles`は、許可されたCanonical Directory内にある1 MiB以下のUTF-8 JSONだけを対象とし、`.json`のまま`downloads/`配下へbyte-for-byteで生成する。JSONはobjectまたはarrayをrootとする厳密な形式とし、重複keyや`NaN`等の非標準値を拒否する。生成器はMarkdown内の正本リンクを公開先への相対リンクに変換し、正本と公開物のSHA-256をbuild manifestへ記録する。symlink、path traversal、hidden path、実行形式、共有`assets/`への上書きは拒否する。

## 非破壊build契約

1. 同期・build前後で追跡ファイルのSHA-256が変化してはならない。
2. Site-source生成処理の出力先はRepository直下の`docs/`だけとし、それ以外のpathやsymlinkを拒否する。
3. Jekyll buildは`_site/`、その他の将来の配布処理は明示された生成Directoryだけへ書き込む。
4. `docs/`は毎回作り直し、孤立した旧生成物を残さない。
5. `--check`はRepository内のファイルを書き換えず、同じ入力から異なる出力が生じた場合に失敗する。
6. 生成物の`_data/build-manifest.json`は、正本SHA-256、`site-pages.json`のSHA-256、formatter commit、上流Git blob SHA、適用した局所変換を記録する。
7. CIは契約、出典、決定性、リンク、構造、Unicode、文章、layout risk、Jekyll build、built-site smoke testを分離して表示する。
8. 同じ本文を`manuscript/`、`cases/`、`templates/`と`docs/`の両方で手編集しない。

## book-formatter

共通layout、include、asset、schemaは、`.book-formatter/revision.json`に固定したrevisionから同期する。全対象ファイルについてGit blob SHAを検証する。

共有`book.html`には、次の3つの決定的な局所変換を適用する。

1. 「GitHubで編集」リンクを生成済み`docs/`ではなく`page.source_path`の正本へ向け、`site.show_edit_link`で表示制御する。
2. 実際には外部Fontを読み込んでいないため、不要なGoogle Fontsのpreconnect hintを除去する。
3. Repository所有のfaviconをまだ配置していないため、404になるfaviconとapple-touch-iconのLinkを除去する。

`.book-formatter/revision.json`を局所変換一覧の機械可読な正本とし、変換前の上流Git blob SHA、変換名、変換後SHA-256を生成時の`_data/build-manifest.json`へ記録する。局所変換を追加・変更する場合は、本契約、revision manifest、generator、Book QA、第三者通知を同じPRで更新する。

## 公開方式

- Pull Request: `Book Contract`と`Book QA`で生成、静的検査、Jekyll build、smoke testを実行する
- `main`: 同じ工程でPages artifactを生成する
- GitHub Pages: `.github/workflows/pages.yml`がartifactをdeployする
- Repositoryには`docs/`や`_site/`をcommitしない

Phase 0は、Review Thread、Contract、Book QA、Pages workflow、管理者設定の状態を確認した上で完了判定する。代表章はPhase 0完了前にDraftとして開始できるが、mergeはPhase 0のOperator Gate完了後とする。
