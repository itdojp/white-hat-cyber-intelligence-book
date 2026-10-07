# Incident Action Plan

`ART-25`は[第19章](../manuscript/19-incident-response.md)の判断を、[完全合成Case](../cases/ch19-incident-action-plan-example.md)のように記録するためのTemplateである。空欄を推測で埋めない。不明ならGap、Owner、期限、次のQuestionを残す。

## Identity and roles

- Incident / Case / Parent Case ID / relation / Record revision:
- Signal / Report / Hunt ID / Finding ID / Detection ID / Telemetry Map ID:
- Decision Requirement / Decision ID / Owner / Reason / Timestamp / Timezone:
- Incident commander / Evidence lead / Communication owner / Recovery owner:
- 法務・Privacy照会担当 / 判断期限:
- 親記録のStatus / Handoff未配達 / Evidenceと権限の非継承:

本書の課題は完全合成JSONの読解だけである。実Incident、実組織、実User、実PII、実Credential、外部接続、実収集、実通知、実封じ込めは対象外とする。実Dataや不明な権限が出たら停止する。自分のメモだけを整理し、供給Evidenceや親記録は変更しない。

## Classification and scope

- Classification / 代替説明:
- Severity / 影響の根拠 / Priority / 緊急性と資源の理由:
- Status: Suspected / Declared / Contained / Investigating / Recovering / Closed / Reopened
- Previous Decision ID / Status / 時刻 / 今回要求するStatus:
- 宣言基準 / 判定Evidence ID / 宣言Owner / Reason / Timestamp:
- Subject / Revision / Asset / Identity / Data classification:
- Scope hypothesis / Confirmed scope / Excluded scope / Unknown scope:
- Observation window / 利用可能時刻 / Collection gap:

Scopeごとに限定根拠を残す。UnknownをExcludedへ、HuntのSupportedをDeclaredへ自動変換しない。四つの判断軸と七状態は本書の有限記録契約であり、全組織の固定直列手順ではない。

## Evidence and options

- Evidence Question ID / Evidence ID / 種類 / 対象版 / 範囲 / 時点:
- Evidence Preservation ID / Owner / 保持時刻 / 来歴と取扱いの制限:
- Option ID / Security effect / Business impact / Evidence impact / Reversibility:
- Authority ID / 合成承認の主体・対象・有効時間 / Expected impact / Rollback:
- Action ID / 計画か供給仮定か / 実施の有無 / Validation ID / Scope:
- 調査Question / 仮説 / 確認事実 / Alternative / Confidence / 根拠 / Gap:

App停止、Permission制限、Monitoring強化は比較する案であり、製品操作手順ではない。供給Receiptは教育上の仮定で、真正性や実権限を示さない。保持前のAction、破壊的Action、選択肢だけによる効果認定は受け入れない。実行した操作は0件である。

## Communication and recovery

- Notification Question ID / Data・影響・法域・契約の確認事項:
- Audience候補 / 法務・Privacy照会Owner / 期限 / 未判断事項 / 実送信の有無:
- Eradicationに向けたQuestion / 残る要因 / 対応計画の制限:
- Recovery ID / Owner / 入口基準 / Validation ID / 正常性・完全性の範囲:
- Closure Owner / Timestamp / Residual risk / Risk owner / 再確認期限:
- Reopen ID / Closed Decision ID / 新Evidence / 利用可能時刻 / Owner / Reason:

通知の要否・期限を教材で自動決定しない。復旧開始、復旧検証、閉鎖、改善完了を同義にしない。再開では旧閉鎖の記録を保持する。

## Traceability and reassessment

- Decision Log / Timeline ID / Finding ID / Control ID / Reassessment ID:
- 許される結論 / 代替説明 / Confidence / 根拠 / Gap / Next action:
- 第20章Evidence QuestionとScope / 予定Timeline・RCAの問い:
- 第22章Improvement item / 予定Backlog / Owner / 期限:
- 第26章Operational CTI Question / 予定Record / 判断要求:
- Handoff ID / sourceDecisionId / targetChapter / status / Receipt / 実権限:
- 再評価Trigger / 引渡し時の受入条件 / 未完了事項:

Handoffはplanned-not-delivered、Receiptはnull、実権限はfalseとする。後続章の調査完了・受領・改善効果は認定しない。Scope、版、Evidence、承認、復旧検証、残余リスクが変わったら新Decisionを追加する。
