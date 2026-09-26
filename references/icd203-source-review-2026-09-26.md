# ICD 203 Source Review — 2026-09-26

## 確認範囲

`SRC-ICD203-001`の版情報を補完する限定監査である。[Issue #171](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/171)に基づき、[第1章](../manuscript/01-integrated-discipline.md)と[第25章](../manuscript/25-structured-analysis-attribution.md)が参照する分析基準を再確認した。Registry全件や将来章の監査ではない。

## 一次資料と確認精度

- [ODNI公式PDF](https://www.dni.gov/files/documents/ICD/ICD-203.pdf): web readerで8ページを確認。2015-01-02署名の本文、旧改訂頁の2022-01-21という記載、先頭の年次研修に関する改訂頁を区別する。旧頁内部の日付順序を推測で修正しない。
- [IC公式Objectivity](https://www.intelligence.gov/mission/our-values/objectivity): 2015年1月に加え、2023年6月の改訂・再承認を明示する。今回はこの月精度までを版情報に補う。
- 2023年改訂の正確な署名日は未確認（null扱い）。検索索引の候補日を確定値にせず、月初の日付も補わない。Registryの`publishedAt: 2015-01-02`は元本文の日付であり、最新改訂の公開日ではない。
- PDFの直接取得はHTTP403だった。今回の確認は公式PDFをweb readerで取得した抽出本文と公式説明による。署名画像の目視、取得PDFのbyte同一性やSHA-256確認は主張しない。

## 既存章への影響

本文D.6で、適時性、情報源の品質、不確実性、情報と仮定・判断の区別、代替分析、顧客関連性、論理的説明を確認した。第1章のDecision Loopと第25章の分析品質の引用用途を維持できる。第25章の確信度、代替仮説、帰属の段階、Template、合成Caseを変更する根拠にはしない。

これは米国ICの分析基準を品質の参考とする用途であり、民間の収集権限、個別の法的適格性、分析結果の正しさを認定するものではない。年次研修の組織義務を本書の読者へ直接適用しない。

版情報の補完は出典記録の変更であり、既存章の分析手順の意味変更ではない。2015本文と旧2022改訂の記録を保持し、個別`checkedAt`だけを2026-09-26へ進める。既存の`nextReviewAt: 2027-08-03`は延長しない。Registry直下の一括監査日、他Source、章mappingは据え置く。将来章のmapping整理は[Issue #109](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/109)の別課題であり、今回の監査済み章に数えない。

## 検査と次回確認

第25章checkerは過去の2026-08-03基準日を保持し、ICD203についても既存の共有日付helperで後日の限定監査を許容する。過去への巻戻し、不正な日付や型は拒否し、CIA SATとIANA snapshotの完全一致条件は変更しない。日付だけを進めても版・適用範囲の確認や独立レビューの代わりにはならない。

次回は公式改訂・置換告知、2023年署名日の原資料確認、または2027-08-03以前を再確認の契機とする。第23章以降へ採用する際は、その章の主張と適用範囲を別に監査する。OSINT StrategyやCAI Policyの現行状態は本監査の対象外である。
