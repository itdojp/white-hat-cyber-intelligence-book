# Part IIのCase独立性と横断Traceability

## 変更の根拠と採用方法

根拠は[Issue #145](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/145)と[実装前の裁定提案](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/145#issuecomment-5740785599)である。本変更の採用判断は、対応PRの独立レビューと利用者による通常mergeで行う。文書の作成やCI成功を人間承認とは扱わない。

[Issue #20](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/20)の旧Artifact計画は「CASE-2026-001をrefineし、第11章のAssessment結果から第15章のRisk decisionまで直接IDで接続する」としていた。一方、凍結[WRITING_GUIDE](WRITING_GUIDE.md)§10は、第11章のCASE-2026-011を独立Caseとする。第15章も、親14のEvidenceを別対象へ移さず方法参照だけに限定している。

旧文言を証拠や許可の継承と解釈すると、既存契約と衝突する。章を一つの実施時系列へ改変せず、旧計画の「接続」を次のように明確化する。

> 既存レコード内・章間の直接参照IDを追跡する。ただし、CASE-2026-011は独立Caseとして比較・方法参照に限定する。CASE-2026-001内でも別対象・版・Scopeの教材へEvidence/Authorityを継承せず、Finding→Retest→Decisionは同じ判断例の記録へ直接結ぶ。未配達Handoffは未配達のまま、Gap・担当・受領条件を示す。

## 影響範囲と移行

- 読者向けには[Part II横断対応表](cases/part-ii-assessment-risk-map.md)を追加し、Case索引から案内する。新CaseやArtifact IDを発行しない。
- 第9〜15章の本文、Template、Case、JSON、Schema、Source Note、既存ID、Status、許可、Evidenceは変更しない。
- WRITING_GUIDE、安全契約、共有Policy・Projection、Formatter pin、Editorial Input Manifestは変更しない。外部草稿の採用はない。
- 公開後、Issue #20の旧Artifact計画を削除して履歴を失わせず、本裁定と通常mergeの証跡を付けて解釈を整合する。
- 六章のmerge件数だけでPart完了にしない。横断の技術・安全・教育設計レビュー、有限検査、全QA、actual-main公開確認を行い、残DoDを個別に判定する。

別の選択肢として同一対象の新しい統合教材を作ることは可能だが、新scope・版・根拠・許可条件の設計と独立レビューを要する。既存教材の遡及統合や、第16章の先行実装には置き換えない。

## 検査の所有範囲

`scripts/check_part02_contract.py`は、七章の固定教材間の直接参照、独立Case、親Draft/期限/Scope、未配達、別対象への非継承、および横断ページの有限公開面だけを検査する。供給JSONの意味判定やSchema全体は、既存の各章checkerが引き続き所有する。

新ページの構文処理はPublication Projection 1.1.0、危険な操作・Hostの判定はContent Safety Policy 1.2.0を使用する。新しい構文parserや章限定の構文regex、一般化した安全除外は追加しない。公開fieldの順序と内容を有限fixtureに固定し、正本変更時はfixture差分もレビューする。

この検査は実環境の権限、同一性、法的適合性、コントロールの有効性、Handoffの配送を認定しない。CI成功は教材の整合性の証拠であって、実運用の許可ではない。
