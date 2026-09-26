# Part III finite cross-record contract

Issue #168 / `scripts/check_part03_contract.py`が所有する有限Layer Aのfixture。

- `publication-contract.json`: 第III部横断ページ全体の共有Projection 1.1.0による型付き順序付きfield一覧。正本文の投影snapshotであり、独立した意味判定期待値やrenderer自体の正当性証明ではない。
- `counterexamples.json`: 24件の独立した参照・非継承・Gap・型差の変更例と、12件の共有Projection/Policy到達例。各IDに不変条件を記録する。
- producerのIDは独立literal、consumerはproducerの実欄へ照合する。双方のIDを同時に偽造する対比も含める。
- 208の境界観測には同じproducerを別consumerから参照する重複観測を含む。208の独立した意味判定器ではない。すべてに欄削除と値/型変更の負例がある。
- ページの全field欠落、正本JSONの読取境界（重複key/非有限数/UTF-8/size/symlink/FIFO/未登録path）を検査する。並行した敵対的filesystem変更のsandboxとは主張しない。
- 第17章のreplayや各章の状態・算術・因果判定は再実装しない。既存章checkerが所有する。
- Source本文、章の供給JSON、Policy 1.2.0、共有Projection、formatterや依存は変更しない。

初稿の検査で、consumer側receiptの未宣言を負例が検出し、親側の実status/receiptとの照合を追加した。raw HTMLコメントは共有凍結契約外でPP1001となる。単なる「危険」という語を添えた操作文を包括的に安全と扱わず、安全対比は明示的禁止付きの読解へ限定する。新しい構文や安全文法を本checkerへ追加しない。

`python3 scripts/check_part03_contract.py`で全検査、`--no-regressions`で出版前検査を行う。fixtureや本文を変更する場合は差分と意味をレビューし、検査成功を実行許可・受領・実有効性の証明として扱わない。
