# Source and Freshness Policy

## 1. 原則

- 技術標準、法令、製品仕様、版情報は一次資料を優先する
- 二次資料は探索、比較、論点発見に使い、重要主張は可能な限り原典へ遡る
- AI生成要約を出典にしない
- URLだけでなく、発行主体、文書名、版、公開日、確認日、利用箇所を記録する
- 事実と分析判断を分離する

## 2. Source Noteの必須項目

`references/sources.json`の各項目に次を持たせる。

- `id`
- `publisher`
- `title`
- `kind`
- `status`
- `version`
- `url`
- `publishedAt`
- `checkedAt`
- `nextReviewAt`
- `reviewTriggers`
- `chapters`
- `notes`

日付が不明な場合は推測せず`null`にし、理由を`notes`へ記録する。

Registry直下の`checkedAt`は、全Source Noteを一括監査した最終基準日である。個別Source Noteを章Issueで再確認した場合は、その項目の`checkedAt`だけを更新し、未再確認の項目まで一括監査済みと見なして直下の日付を進めない。読者向けBaselineでは、直下の日付をRegistry-wide baseline、各行の日付を個別Source Noteの確認日として表示する。

## 3. 鮮度分類

| class | 対象 | 通常確認間隔 |
|---|---|---|
| event | 法令改正、標準release、ATT&CK、OWASP、AI guidance | 変更通知時と四半期 |
| continuous | KEV、EPSS、脆弱性・キャンペーン情報 | 値を本文へ固定せず、利用時に確認 |
| annual | NIST等の定期更新文書 | 年1回以上 |
| stable | 基礎理論、長期安定仕様 | 版変更または3年ごと |

`nextReviewAt`を過ぎたSource NoteをCIで警告し、本文の公開判断では章Issueをblockできるようにする。

## 4. 引用と要約

- 引用は必要最小限とし、引用符と出典を付ける
- 原文の意味を変える切り取りをしない
- 翻訳は訳文であることを示し、争点となる語は原語を併記する
- 表や図を転載する場合は、文書ライセンスと帰属条件を確認する

## 5. CTIの情報源評価

情報源そのものの信頼性と、個別情報の確からしさを分ける。複数の記事が同じ原典を参照している場合、独立した裏付けとして数えない。

記録する観点:

- 原典か
- 取得時刻とタイムゾーン
- 改変可能性
- 情報源のアクセス位置
- 技術的観測か自己申告か
- 他の独立情報との整合
- 欺瞞、誤認、翻訳誤差の可能性
- 反証可能性と情報ギャップ

## 6. 更新フロー

1. Source Noteを更新
2. 影響章を列挙
3. 意味変更か表記変更かを分類
4. 本文・図・テンプレート・演習を再監査
5. `CHANGELOG.md`へ読者影響を記録
6. 独立レビュー後にmerge

## 7. 章との双方向Traceability

- 本文で使用する`SRC-*`は、同じ章の`参考文献・Source Note ID`に列挙する
- 章末に列挙したIDは、本文、演習、安全境界、Templateまたはfixtureの説明で実際に使用する
- Registryの`chapters`は、実際にSource Noteを使用する章だけを含める
- 章固有の安全Gateやfixture検査に使うSourceも、読者が用途を確認できる箇所でIDと役割を示す
- Sourceの登録だけを先行して、未使用の章mappingを残さない。将来利用は利用する章のPRで追加する

代表章Gateでは、本文中の使用ID、章末一覧、Registry mappingの集合が一致することをCIで検査する。全章展開時も同じ契約を継承する。

## 8. Source品質の受け入れ条件

- 一次または公式Sourceで重要主張を確認している
- `status`、`checkedAt`、`nextReviewAt`、`reviewTriggers`が空でない
- Versionまたは公開日が`null`の場合、値を特定できない理由と追跡方法が`notes`にある
- Development、Deprecated、SnapshotをStableな現行標準として扱っていない
- 変更検知時に再確認する章、図、Template、fixture、判断基準が分かる
- 引用の独立性を記事数で水増しせず、同一原典を一つの系統として扱う
