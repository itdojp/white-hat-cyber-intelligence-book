# 付録C チェックリスト集

## 使い方と限界

[付録B](appendix-b-templates.md)で成果物を選んだ後、各項目について自分の記録の根拠箇所、確認結果、未確認の理由、担当、期限を残す。既存の状態欄がある場合は元Templateの語彙を使い、この一覧を新しいStatus体系にしない。

Automationは機械が確認する範囲、Limitationは保証しない範囲、Failure actionは不足時の戻り先、Ownerはその確認を担う役割である。Checklistだけで合法・安全・完了を保証しない。担当名の記入も実権限の証明ではない。実Credential・個人情報・実Targetを記入しない。

## 確認の順序

開始条件から根拠、状態、結果、Review、引渡し、整理の順に確認する。該当しない項目を黙って削除せず、今回の問いに不要な理由を記す。不足や停止が見つかったら、後の項目で相殺せずに元欄へ戻す。

生成索引開始（BCI_GENERATED_START）

### BCI-C01 最初の記入先を選ぶ

判断する問いとArtifactを選び、ID・対象・版から記入する。

- Automation: live索引とTemplateの対応、重複・欠落・参照版を検査する。
- Limitation: IDの存在は判断目的の妥当性を保証しない。
- Failure action: 不明なIDや版は推測で埋めず、元章へ戻して訂正する。
- Owner: 記入担当。
- 戻り先: [ART-01](../templates/learning-route-plan.md)、[ART-10](../templates/integrated-security-case-map.md)、[ART-33](../templates/final-security-decision-portfolio-index.md)。

### BCI-C02 開始・停止条件を確かめる

Authority・Scope・Data・停止条件を確認する。

- Automation: 参照版と共有Policyの公開面検査。実権限は自動認定しない。
- Limitation: ChecklistのPASSは合法性や実作業の許可ではない。
- Failure action: 許可・出所・対象範囲が不明、実Dataや外部接続要求があれば停止し、担当へ照会する。
- Owner: 判断担当と安全確認担当。
- 戻り先: [ART-13](../templates/authorization-checklist.md)、[ART-02](../templates/rules-of-engagement.md)、[ART-18](../templates/lab-safety-evidence-plan.md)。

### BCI-C03 根拠と不足を分ける

Evidenceの対象・版・時点・由来と、支持しない結論を記す。

- Automation: 正本参照の存在・版を検査する。
- Limitation: 同じ原典の複製は独立裏付けではない。Hashは真正性を保証しない。
- Failure action: 未収集はNot collected、判断不能はInconclusiveとして区別し、Gap・担当・期限を残す。
- Owner: Evidence確認担当。
- 戻り先: [ART-30](../templates/evidence-source-evaluation-table.md)、[ART-12](../templates/analytic-judgment-record.md)、[ART-10](../templates/integrated-security-case-map.md)。

### BCI-C04 状態の対象を確かめる

Document・Result・Control・配達等のどの欄かを確認する。

- Automation: 元章・Templateの固定版と状態参照を検査する。
- Limitation: 任意の実務記録のStatusをこの索引で承認することはできない。
- Failure action: 語彙や状態遷移が不明なら元章の有限契約へ戻し、独自状態を足さない。
- Owner: 記入担当と元章のReview担当。
- 戻り先: [ART-14](../templates/capability-evidence-matrix.md)、[ART-24](../templates/telemetry-coverage-map.md)、[ART-28](../templates/security-improvement-backlog.md)。

### BCI-C05 期待と結果を照合する

同じ対象版のExpected、Actual、範囲、反例を辿る。

- Automation: 各章の供給Fixture検査を再利用する。
- Limitation: 記入完了・供給Receipt・試験PASSは実Controlの検証ではない。
- Failure action: 不足する観測と次の問いを残し、Expectedを結果へ合わせて変えない。
- Owner: 検証記録のReview担当。
- 戻り先: [ART-22](../templates/minimal-impact-validation-record.md)、[ART-05](../templates/detection-validation.md)、[ART-27](../templates/control-validation-plan.md)。

### BCI-C06 評価と判断を記録する

学習目標・章DoD・八観点を根拠へ結ぶ。

- Automation: 対応表と参照版の欠落を検査する。
- Limitation: 機械検査とAIレビューは人間の読者試行・法務確認・正式承認とは別である。
- Failure action: 根拠不足や重大な境界違反を点数で相殺せず、変更要求と戻り先を記す。
- Owner: Reviewerと判断担当。
- 戻り先: [ART-14](../templates/capability-evidence-matrix.md)、[ART-09](../templates/executive-brief.md)、[ART-33](../templates/final-security-decision-portfolio-index.md)。

### BCI-C07 引渡しと再評価を残す

Owner、期限、受入条件、Receipt、変更時の戻り先を確認する。

- Automation: 参照欄と供給Caseの整合を検査する。
- Limitation: 送付予定は受領でも実行許可でもない。
- Failure action: 未受領・期限切れ・親版変更を未完として保持し、再確認の条件を元欄へ戻す。
- Owner: 引渡し担当と受け手。
- 戻り先: [ART-08](../templates/cti-report.md)、[ART-23](../templates/retest-record.md)、[ART-33](../templates/final-security-decision-portfolio-index.md)。

### BCI-C08 公開と整理の境界を確認する

Template・Example・Fixtureを区別し、自分の作業Copyだけを整理する。

- Automation: リンク、生成一致、構造、共有Policy、built-siteを検査する。
- Limitation: 自動検査は全PIIの検出や実端末・印刷の利用可能性を保証しない。
- Failure action: 実Dataの疑い・公開範囲不明・リンク切れを残したまま共有せず、担当へ戻す。
- Owner: 公開確認担当。
- 戻り先: [ART-13](../templates/authorization-checklist.md)、[ART-18](../templates/lab-safety-evidence-plan.md)、[ART-33](../templates/final-security-decision-portfolio-index.md)。

生成索引終了（BCI_GENERATED_END）

## 確認結果の例

ART-10の読解で必要な観測が供給されていない場合、Evidence欄に観測を創作しない。BCI-C03で未収集と判断不能を分け、Gapと判断への影響を記録する。BCI-C07で次に確認する条件・担当・期限へ結ぶ。これは「記録として不足を説明できた」状態であり、Controlが有効だったという結論ではない。

供給例のHandoffが未配達なら、記入を終えてもReceiptを追加しない。親RoEのDraft、失効したAuthority、過去Windowも更新しない。自分の作業Copyの整理と親のEvidence保持を区別する。

## 自己点検と戻り先

チェックした項目を一つ選び、機械の成功だけでは確認できないことを説明する。不明なら[付録Bの元Template](appendix-b-templates.md)へ戻る。評価は[付録I](appendix-i-rubric.md)、停止時は[付録D](appendix-d-troubleshooting.md)を参照する。実データ収集、実対象への操作、実通知で空欄を埋めない。
