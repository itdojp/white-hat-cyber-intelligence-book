# Retest Record

ART-23は[ART-04 Finding Report](finding-report.md)に対する再確認記録である。実作業の許可や一般のRisk判定器ではない。[第15章](../manuscript/15-findings-retest-risk.md)の必修課題は供給された完全合成記録の読解だけで完結する。

## この記録の境界

Purposeは変更後の問い・条件・Evidenceを対応付けること。Prerequisite / Authority / Scopeは対象と版を限定した供給資料であり、親の許可状態を変更しない。Expected evidenceは各条件を支持・反証・未観測として説明できる記録である。Impactはローカルの読解に限定し、実Scannerや実System変更を行わない。

Stopは未知入力・Scope不一致・追跡不能である。追加操作をせず、理由と次の担当を記録する。Cleanupは作業メモの整理に限定し、正本と親資料を保持する。

## T-15-07 Retestの記入欄

| 欄 | 記入するもの | 確認点 |
|---|---|---|
| Retest ID / Finding ID | ART-04の対象との直接参照 | 別Findingへ付け替えない |
| Subject / before revision | 変更前の対象と版 | 元Validationとの一致 |
| Change reference / changed revision | 供給された変更記録と変更後版 | 実改修と混同しない |
| Scope / Method | 必要な条件を確認できる方法 | Scanner要約だけで十分としない |
| Acceptance criteria | 条件ID、期待値、対象版 | 期待値を観測から逆算しない |
| Observation / Evidence | Evidence ID、条件ID、対象、版、present、value、basis | 欠測をfalseに変換しない |
| Stop / continuation | trigger、理由、停止後追加操作0 | 停止を最優先にする |
| Result | Passed / Partial / Failed / Inconclusive / Stopped | 支持した範囲と限界を併記 |
| Regression scope | 再確認した範囲と未確認範囲 | 全System非回帰を主張しない |
| Residual / Decision | Residual risk ID、判断Owner、理由 | PassedでもRiskゼロとしない |
| Expiry / Reassessment | 受容期限、再評価ID、担当、期限、条件 | 記録を永久受容にしない |

## 判断を残す

第一の権限条件と第二の監査参照を、同じ対象・変更後版で比較する。停止ならStopped、欠測やMethod不足ならInconclusive、第一条件が不一致ならFailed、第一のみ一致ならPartial、両条件一致ならPassedとする。この優先順は二条件を持つ本教材だけの契約である。

Closedへ進める場合、十分なRetestを根拠にしたのか、有効な明示的受容を根拠にしたのかをART-04に戻して記録する。受容記録にはAuthority reference、Holder、Scope、Expiry、Residual、Reassessmentが必要である。実行許可や公表許可は付与しない。

## 完全合成例と読み取り専用データ

- [七Finding・五Retestの全Field表示](../cases/ch15-findings-retest-risk-example.md)
- [供給JSON](../cases/fixtures/ch15-findings-retest-risk.json)
- [閉じたSchema](../schemas/ch15-findings-retest-risk.schema.json)

実データ、実Credential、実連絡先は使用しない。結果は供給値の比較であり、実脆弱性や実改修の成立を証明しない。
