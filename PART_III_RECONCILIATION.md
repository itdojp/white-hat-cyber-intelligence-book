# 第III部の直接参照と非継承の整理

## 根拠と採用判断

根拠は[Issue #168](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/168)と、[Issue #21](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/21)のPart横断確認である。本提案の採用判断は、対応PRの独立レビューと利用者による通常mergeで行う。文書作成、検査成功、PRのReady状態を人間承認とは扱わない。

Issue #21の旧Artifact計画は「第17章CASE-DET-2026-001をrefineし、Hunt / Incident / Control / Improvementを直接IDで接続する」としていた。一方、[WRITING_GUIDE](WRITING_GUIDE.md)§10は別判断対象の見かけ上の統合を禁止し、現行の第16〜22章は方法参照、別対象・版、未配達、権限とEvidenceの非継承を明記している。

旧計画の接続を、一件の実施済みIncidentや受領済みEvidenceの継承と解釈すると既存契約に衝突する。既存教材を遡及的に書き換えず、次の読み方へ明確化する。

> 供給記録の定義と参照を直接IDで追跡する。参照が解決しても、対象・版・Scope、根拠の用途、受領条件は別に確認する。方法上のrefinesは元Evidence・許可・実施結果の継承ではない。未配達Handoff、親の旧結果、Gapを保持し、章ごとの限定結論と再評価を読む。

第17章のDetection/DVR/fixture/Handoff必須欄は共通の比較基準として保持する。第16章のTelemetry Mapが存在するだけで第17章の入力契約を満たしたとは扱わない。第19章のIncident IDを第20章へ借用せず、第21章の供給比較を第22章で実リスク低下へ昇格させない。

## 影響範囲と移行

- [第III部横断読解](cases/part-iii-detection-improvement-map.md)を補助教材として追加する。新Case、Artifact、実施履歴を作らない。
- 第16〜22章の本文、Template、Case、供給JSON、Schema、Source Note、既存ID/Status/Evidence/許可は変更しない。
- WRITING_GUIDE、安全契約、共有Policy・Projection、formatter pin、依存、Editorial Inputは変更しない。外部草稿の採用はない。
- 公開後、Issue #21の旧計画を削除せず、本整理と通常mergeの証跡を付けて解釈を整合する。
- 六章mergeだけでPart完了とはせず、七教材の横断レビュー、全QA、actual-main/Pages確認と各DoDの判定を行う。未解決の契約問題を次Partへ持ち越さない。

一つの対象を最後まで追う新規統合教材は別の選択肢である。ただし新Scope・版・根拠・許可条件の設計と独立レビューが必要で、既存記録を同じ実施時系列へ改変する方法では代替しない。

## 検査の所有範囲

`scripts/check_part03_contract.py`は固定七教材間の参照、非継承、未配達、限定結論と新ページの有限公開面を検査するLayer Aである。各章のJSON Schema、Hunt/IR状態判定、DFIR因果評価、Control判定、Metric計算は既存章checkerが引き続き所有する。

新ページ全体の構文処理はPublication Projection 1.1.0、Action/Host判定はContent Safety Policy 1.2.0へ委譲する。新構文parser、章限定構文regex、一般化したprovenance除外は追加しない。供給教材の参照が実在することと、実際の配送・実行許可・真正性・検知成功は別の命題である。
