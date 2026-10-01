# 全体レビュー: 書籍完成へ向けた編集・品質・進行の整理

## 1. 監査の位置付け

- 確認日: 2026-09-06
- 基準commit: `518ea8579439a2c29cfc0e4fbea4086995ada1c0`
- 所有Issue: [#108](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/108)
- 対象: 書籍企画、目次、収録状況、編集・安全・出典契約、共有出版基盤、章Checkerの構成、Issue計画。
- 方法: GitHub上の固定commitのファイル、tree metadata、Issue/PR記録の確認。

本記録は横断的な編集レビューであり、全8章の逐語的な技術再承認、全Sourceの最新版監査、読者試行、侵入試験、依存関係の新規監査ではない。観測と提案を区別し、ここに記載した提案だけで凍結契約を変更しない。

今回の並行作業は新規review branchに限定する。進行中Codexのworktree、章branch、review thread、Canonical本文、Manifest、Schema、CI、formatter pinを変更しない。Open PRがないことも、別セッションの未push作業が存在しない証拠にはしない。

## 2. 結論

書籍の中心設計は維持する。攻撃評価、観測、検知、対応、インテリジェンス、経営判断をEvidenceと成果物で接続する構成には一貫性がある。合成Case、許可・停止・再評価、生成物と正本の分離も継続する。

次の優先課題は、共有基盤をさらに一般化することではなく、現在の基盤を使って未収録章を完成させることである。保守・出典・可読性の改善は必要だが、未実証の将来要件を全章共通の新しいブロッカーにしない。

参照: [BOOK_PROPOSAL](../BOOK_PROPOSAL.md)、[書籍設定](../book-config.json)、[安全範囲](../SAFETY_SCOPE.md)、[正本と生成契約](../CANONICAL_SOURCE.md)。

## 3. 基準commitの状態

| 項目 | 観測 | 読み違えてはいけないこと |
|---|---|---|
| Canonical章本文 | 第0・1・2・3・4・11・17・25章の8章 | 本レビューが8章を新たに検証済みとしたわけではない |
| 計画章数 | 第0章から第29章まで30章 | 8/30は収録数であって品質・工数の進捗率ではない |
| 未収録章 | 22章 | 登録済みの外部草稿を本文完成へ加算しない |
| 付録 | 基準treeに`appendices/`配下の正本はない | Manifest登録、Blueprint、Templateの存在は付録完成と同じではない |
| formatter pin | `198935ff8f60653c40e513343dc5f02573d9968e`、確認記録2026-09-04 | 旧pinのadvisoryを現在の検出結果として引用しない |
| Editorial Input | PR #107でManifest基盤がmerge済み | 登録hash、ファイル実在、検証、採用、merge後のconsumedは別状態 |
| README | `Phase 0 in progress`が残存 | 出版基盤は既にその段階を通過している |
| Roadmap #17 | 5/30章・旧baselineの現在地表示が残存 | 歴史的baselineと現在の状態を分けて表示する |

根拠: [固定tree](https://github.com/itdojp/white-hat-cyber-intelligence-book/tree/518ea8579439a2c29cfc0e4fbea4086995ada1c0)、[formatter固定情報](../.book-formatter/revision.json)、[Manifest](../editorial-input-manifest.json)、[PR #107](https://github.com/itdojp/white-hat-cyber-intelligence-book/pull/107)。

## 4. 維持する設計

### 4.1 判断とEvidenceの分離

Mapped、Observed、Validatedや、Assumed、Confirmed、Not collectedを混同しない設計を維持する。成果物の完成は、全Controlが合格した状態を意味しない。未収集・不明・不一致を、Owner、期限、必要Evidence、再評価へ接続すること自体が正当な学習成果である。

### 4.2 共有基盤の再利用

共有Publication ProjectionとContent Safety Policyを新しい章から利用し、章CheckerがMarkdown/Kramdownや自然言語grammarを再実装しない。既存の固定rendererを根拠にすることと、任意の自然言語の安全性を完全に証明することは別である。

### 4.3 非正本草稿の扱い

外部草稿はcurrent mainに優先しない。複数Candidateの自動選択、hash未確認の採用、Package不在時の内容推測、過去履歴の書換えをしない。Manifestの次状態は、実際の採用・PR・公開証跡に対応させる。

参照: [WRITING_GUIDE](../WRITING_GUIDE.md)、[Publication ADR](../adr/0002-publication-projection-owner.md)、[CONTENT_SAFETY_POLICY](../CONTENT_SAFETY_POLICY.md)。

## 5. 改善項目

### R1: Sourceの実使用と参照計画を分離する

**観測:** `SOURCE_POLICY.md` §7は実使用章だけのmappingを要求する。一方、`SRC-ATTACK-001`には未収録の5・16・21・26章、`SRC-CSF-001`には未収録の19・22章等が含まれる。全体Checkerは存在する本文からRegistryへの参照を検査するが、未作成章への余剰mappingを一般には検出しない。

**影響:** 読者や編集Agentが、採用予定と引用済みを区別できない。章固有の検査成功を全章双方向一致の保証として扱えない。

**対応:** [#109](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/109)。実使用はRegistry、将来採用は章Issueの計画へ分離する。新フィールドを導入する場合はSchema/Policy/生成Baselineを同時に移行する。意味再確認をしていないSourceの`checkedAt`を進めない。作業中のChapter 5等のSource変更と競合する場合は、その後へ直列化する。

根拠: [SOURCE_POLICY](../SOURCE_POLICY.md)、[sources.json](../references/sources.json)、[check_contract.py](../scripts/check_contract.py)。

### R2: 最小例から実務版へ進む学習導線を作る

**観測:** Quick Startは4成果物を作成する入口を示すが、最小の記入済み一式、具体的な自己点検、完全Caseへ段階的に進む導線は補強できる。第4章は本文55,546 bytes、Template16,077 bytes、Case97,022 bytesである。値はUTF-8ファイルサイズであり、語数や読書時間ではない。

**判断:** 情報の多さを削るより、初回学習と実務参照で必要な粒度を分ける方が安全条件と可読性を両立できる。

**対応:** [#110](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/110)。一つの判断要求・脅威仮説・観測計画・Evidence gap・次の判断から始め、既存Template、完全Caseへ接続する。新しい二重正本を作らず、既存IDの意味と未収集状態を維持する。想定読者による課題試行はコード検査と別に記録する。

根拠: [Quick Start](../quickstart.md)、[第4章](../manuscript/04-assets-boundaries-threat-model.md)、[ART-03](../templates/threat-model.md)、[第4章Case](../cases/ch04-threat-model-example.md)。

### R3: 章Checkerの責任とレビュー終了条件を限定する

**観測:** 第4章Checkerは710,777 bytes、第25章は235,823 bytes、第3章は146,606 bytes、第2章は91,017 bytesである。サイズ自体は欠陥の証明ではないが、意味契約、共有処理、Fixture、Test harnessの分類と、実際の実行時間の計測が必要である。

**対応:** [#111](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/111)。まず測定し、実害のある一箇所だけを独立保守PRで改善する。行数削減、テスト削除、全章一括Refactorを目的にしない。

レビューでは、CI成功、コメントが増えない時間、Reaction、独立レビューの実施証跡を区別する。新しい仕様要望と、現在受理する入力による実際の危険な公開・意味不整合を分ける。後者を「特殊構文」という理由だけで除外しない。前者の無制限な列挙で執筆を止めない。

根拠: 固定treeの各Checker metadata、[共有Projection](../scripts/publication_projection.py)、[ADR](../adr/0002-publication-projection-owner.md)。

### R4: OWN / BRIDGE / DELEGATEの分類粒度を合わせる

**観測:** CROSS_BOOK_MAPの「法・倫理・許可・RoE」は本書BRIDGEだが、第2章および第9章計画は実務上のAuthorization Gate/RoEをOWNとしている。「AI/LLM/Agent Security」も、全体の分類と第27章の具体的成果物の粒度が異なる。

**対応:** 既存の[#55](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/55)へ追記する。実務上の判断・成果物、個別法的助言、製品実装、AI Agent業務ガバナンスを別の行にすることを検討する。新しい分類は既存書籍と実際の章責任を確認して決める。凍結表を本レビューPRで直接変更しない。

根拠: [CROSS_BOOK_MAP](../CROSS_BOOK_MAP.md)、[第2章](../manuscript/02-law-ethics-authorization.md)、[第9章Issue](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/34)、[第27章Issue](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/49)。

### R5: 完成判定を出版基盤・本文・学習・配布へ分ける

**観測:** 機械検査と公開手順は充実している。一方、CI greenは、全章完成、初心者が課題を遂行できること、印刷版が読めること、引用内容が現時点でも正しいことの証明ではない。

**対応:** 既存の[#25](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/25)へ追記する。現行章を使い、通常本文・広い表・図・Template・Source Noteを含む小さな配布サンプルで先に出力方式を確認する。完成後に初めてPDF/EPUBの可読性問題を発見する順序を避ける。配布サンプルは正式版でも全書完成の主張でもない。

技術レビュー、読者試行、Source鮮度、配布検証を別の欄で管理する。実施していないものは未実施とする。

## 6. 実行順と並行作業

| トラック | 次の作業 | 他トラックとの境界 |
|---|---|---|
| 本文制作 | 現在Codexが所有する作業を完了し、既存の章Issue順でCanonical化する | このレビューの全Issue完了を新規前提にしない |
| 出典整合 | 次のSource編集時に#109を同期する | 実行中章branchのRegistryを並行書換えしない |
| 教育・可読性 | 第I部の横断編集で#110を実施する | 現行安全条件、完全Case、IDを弱めない |
| 保守・レビュー | #111の分類・実測から始める | 全章refactorや新しいrendererを開始しない |
| 境界・配布 | #55と#25の既存作業へ追加確認を統合する | 重複した親Issueや新しい全章ブロッカーを作らない |

新しい章を開始する際は、実行時のmain、既存branch/PR、章の前提、ManifestのCandidate/Intake状態を再確認する。Package登録順やIssue comment順を自動選択の根拠にしない。

## 7. 本レビューで行っていない検証

- 全30章の本文精査。基準commitには22章が未収録である。
- 全Sourceの現行版・法令・製品仕様の再調査。
- 実際の想定読者による学習課題試行。
- 新しいdependency audit、全ローカルテスト、公開Webサイトの全ルート再検証。
- 大きなCheckerの完全な関数別・性能・脆弱性監査。
- 別セッションの未push作業の確認。

このチャット実行環境からのリポジトリ取得はDNS解決に失敗したため、ローカルの全テスト実行を報告しない。新規文書PRのGitHub Actions結果はPR側で別途記録する。

## 8. この文書PRの受入範囲

変更は本記録とREADMEの進捗表示に限定する。本文、Source、Manifest、生成索引、凍結契約、CI、依存関係は変更しない。本記録の提案は対応Issueで根拠・影響・移行をレビューした後に採用する。Draft PRのmergeはOperatorが判断する。
