# A/D/H reference contract

Issue #52。Layer Aは4文書の公開fieldと12親入力の固定版、独立routeと往復リンクを所有する。Markdown/HTML/Liquid/URL/見える内容の解釈は共有Publication Projection 1.1.0、Action/HostはContent Safety Policy 1.2.0が所有する。新たな例外・構文parserはない。

`publication-contract.json`の`documents`は共有Projectionの型付きfield（型、要素、属性、見出しlevel、全文）の順序付き一覧である。章や付録の単語が残っているだけでは受理せず、未知の追記や意味の置換は再レビューを要求する。自動更新CLIは設けない。読者面を変更する場合は、変更理由・親との整合・生成物を確認してfixtureを同じPRで更新する。

`parentDigests`は親章の意味checkerの代わりではなく、本付録が参照した版の結合である。親の変更が正当でも無言で追随しない。全章checkerは引き続きnpm testの独立gateとして実行する。親のStatus/RoE/Caseを付録の都合で変更しない。

## 有限回帰

`npm run check:appendix-adh`で次を確認する。

- 4全文surface、preamble/body/tailの直接unsafeと禁止文、destination、共有unsupported診断。
- 8状態のRunning欠落、実行許可falseの昇格、Unsafe後Cleanupの正常完了化、六種Cleanupの欠落。
- DraftからApproved、過去Authority期限の延長、Not collected / Inconclusiveの置換、Source時点の置換。
- 親入力の変更、文書欠落/追加、route欠落/重複/順序衝突、旧ラボrouteの横取り、戻り先欠落、テスト/公開前gate除去。
- duplicate JSON key、NaN、symlink、非通常file、サイズ上限、UTF-8、固定入力以外の拒否。

## 範囲と限界

本文は供給された合成記録の読み方であり、Runtime・外部接続・現実の許可を検証しない。記入完了はControl検証ではない。検査は版の漂流と有限反例を検出し、任意の自然言語の真偽・法的助言・読者の理解を自動認定しない。

共通の入口`legal-notice.md`と`troubleshooting.md`から新付録へ戻れる。既存`LAB_ARCHITECTURE.md`と`appendices/lab-guide/`の所有権は保持し、新Hは`appendices/lab-operations/`を使う。既存章本文・Template・Caseの書換えは行わない。

初稿のSource節番号（ドット区切りと日本語の隣接）は共有Host検査で3件の誤検知となった。同じ節を章・節・項の日本語表記へ整理した。これは新しいSourceの採用やPolicyの修復・例外追加ではない。既存のfilename等を含む任意の文章が無誤検知であるとは主張しない。

AIによる本文/コードレビュー、CI、ブラウザviewport試験は、人間の読者試行・実機試験・法務承認とは区別する。全書の事前レビューと第29章後の付録最終確定は別gateである。
