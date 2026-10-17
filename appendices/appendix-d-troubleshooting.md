# 付録D 停止・切り分けフロー

## 最初に残す記録

この付録は「失敗をどう回避するか」より先に、「何を止め、何を保持し、誰のどの判断を待つか」を整理する。実環境の復旧コマンドを示すRunbookではない。

[ART-02](../templates/rules-of-engagement.md)のStop / Recoveryと[ART-18](../templates/lab-safety-evidence-plan.md)のStop / Cleanup / Reassessmentを開く。自分の読解メモに対象ID・版・Run、停止理由、確認時刻、確認済みEvidence、未確認事項、連絡する役割を書き分ける。教材の原本や親記録を編集して成功へ揃えない。

OWNは停止と次の確認先の接続、BRIDGEは第2・8・9・14・19・20章である。製品操作、実Incident対応、法的判断は各担当へDELEGATEする。

## 新規操作を止める条件

Authority、Scope、Data所有、予測できる影響、証拠保持、復旧可能性が不明なら、新規操作を始めない。実Dataらしい入力や予期しない外部通信があれば、追加表示・転送・取得を止める。「あと一件」で不足を埋めようとしない。

必要なEvidenceが揃った場合も、追加侵害の確認へ進まず読解を閉じる。不足している場合は不足を残す。第14章の最小十分性は、成功するまで操作を増やす原則ではない。

## 判断順と停止したまま残す場合

1. **新規作業の停止:** Trigger、対象、時刻を記録する。実停止を確認していないなら確認済みにしない。
2. **保全と連絡:** 既定の取扱い内で、参照IDと必要最小限の記録を保持する。実Secretの値や不要なDataは複製しない。Primaryが不明ならBackupと判断責任者へ戻る。
3. **停止確認:** 確認Evidenceがなければ停止未確認と残す。停止できたという仮定で破棄へ進めない。
4. **Evidence exportの確認:** 保持対象と破棄対象を分ける。必要な保持を確認できなければ、Evidenceを失う破棄へ進めない。
5. **事前計画内のDestroyと残存確認:** 所有する一時資源だけを対象にする。DestroyedとCleanup verifiedは別である。
6. **再評価:** 原因、残るGap、再開条件、担当、必要な新しい承認を記録する。Cleanupだけで再開しない。

これは第8章の合成Runに対する読解の順であり、実Incidentで証拠保持より機械的に停止・破棄を優先する指示ではない。現実の封じ込めや復旧の判断は、個別の権限と計画へ戻す。NIST SP 800-115の連絡・停止・再開条件を補助にするが、具体的な実操作の許可は付与しない。［SRC-NIST-TEST-001］

## 「ない」の意味を分ける

| 記録 | 読み方 | 誤った読み替え |
|---|---|---|
| Not collected | 必要な観測を収集していないという取得状況 | 事象が存在しない |
| Inconclusive | 今ある根拠では問いへ結論できない | 安全、無害、失敗の確定 |
| Unknown | そのFieldやチェックの条件が不明 | Passやfalseへの補完 |
| 記入完了 | 不足、担当、次の判断まで記録した | Control有効性を検証した |

各語の所属Fieldと有限語彙は元のArtifactに従う。横断表の語を新しい共通Statusとして各JSONへ追加しない。

## 三つの読み取り専用対比

- [第8章Case](../cases/ch08-lab-evidence-example.md): UnsafeのRunがCleanup verifiedへ達しても、Unsafeと正常完了falseを残す。後片付けの成功は異常を取り消さない。
- [第14章Case](../cases/ch14-minimal-impact-validation-example.md): SupportedでもResidual checkがUnknownなら記録はOpen。Inconclusiveでも不足・制限・担当・期限を記載して記録完了にできる場合とは別である。
- [第19章Case](../cases/ch19-incident-action-plan-example.md): 復旧Actionと復旧検証を分ける。未確認ならClosedへ進めない。通知未送信は、通知不要という法的判断ではない。

期待出力は「支持できる結論、できない結論、不足Evidence、Owner、再評価条件」の五点を含むメモである。新たな収集、通知、実対象への操作は行わない。

## 自己点検と戻り先

親Caseの時点・RoE・未配達Handoffを変えていないか。停止が未確認なのに破棄済みとしていないか。保持原本と自分の一時コピーを区別したか。Hash一致を真実や法的証拠能力と呼んでいないか。再開に必要な根拠と担当を具体化したか。

不明なら[既存の停止フロー](../troubleshooting.md)と[第9章](../manuscript/09-engagement-roe.md)へ戻る。Evidenceの原時刻・来歴・分析時点が不一致なら[第20章](../manuscript/20-dfir-timeline-causality.md)へ戻り、後着Dataで過去の判断を無言で修復しない。

## 参考文献・Source Note ID

- `SRC-NIST-TEST-001`

版・確認日・採用する節と採用しない内容は[付録A/D/Hの限定Source Review](../references/appendix-adh-source-review-2026-10-17.md)を参照する。親Caseの時点とAuthorityは変更しない。

権限の確認は[付録A](appendix-a-legal-safety.md)、六種残存確認は[付録H](appendix-h-lab-operations.md)へ戻る。
