# 付録H ラボ運用ガイド

## このガイドで行うこと

ラボが起動したこと、分析が終わったこと、残存物を確認したことは別である。本付録では[第8章](../manuscript/08-safe-lab-evidence.md)の供給された合成記録を読み、開始できない条件と終了を主張できない条件を説明する。実コンテナを起動しない。NetworkやPortを開かない。実Credentialを作成しない。

OWNはART-18の記入と確認先への導線、BRIDGEは第2・8・9・20章、DELEGATEは製品固有の構築方法である。本付録は供給教材の読解だけに限定する。実Dataを取得しない。[演習環境アーキテクチャ](../LAB_ARCHITECTURE.md)と[安全・公開範囲](../SAFETY_SCOPE.md)は設計の正本のまま保持し、運用メモで上書きしない。

## 最初にどこへ記入するか

[ART-18 Lab Safety and Evidence Plan](../templates/lab-safety-evidence-plan.md)のDocument Controlから始める。自分の読解メモへPlan / Case / Relation、Decision / Authority / Scope、Owner / Reviewer、Purpose / Assumptionsを記入する。実装していない版・Image digestは、教材で定義されたnot-executedとnullの理由を保持する。数値やreceiptを創作して空欄を埋めない。

次に[完全合成記入例](../cases/ch08-lab-evidence-example.md)を読み、同じRunの開始条件、停止記録、Evidence、Cleanup、Gapを対応付ける。他RunのPassを借りて完了にしない。

## 八状態、三判定、実行許可は別の軸

状態は次の八つに固定されている。

`Planned / Preflight passed / Ready / Running / Stopped / Destroyed / Cleanup verified / Failed closed`

Run判定は`Safe / Unsafe / Inconclusive`、各receiptは`Pass / Fail / Unknown`である。実行許可は全Runで`executionAuthorized=false`。Ready、Running、Safeのいずれも実作業の承認ではない。安全Tier、作業段階、Run状態を一つの一覧へ統合しない。

PreflightのFailまたはUnknownではRunningに入らない。実行中の異常では新規シナリオ操作を止め、定義済みの停止、Evidence保持、破棄、残存確認だけを扱う。Failed closedから同じRunを再開せず、再審査と新Run IDを必要とする。

## 開始前に確認する根拠

| 観点 | ART-18で照合するもの | 不明時の扱い |
|---|---|---|
| 権限と対象 | Authority、Scope、Case、Run | 開始しない |
| Hostと権限 | rootless、非特権、Mount、Capabilities | 設定名だけでPassにしない |
| Network | 境界、外向き既定拒否、Exposure | 実通信で勝手に補完しない |
| Data | 合成入力、読取り専用、実Secret不在の前提 | 実Dataを混ぜない |
| 観測 | 必要な収集、時計、期待Evidence | 欠けた観測を「異常なし」にしない |
| 資源 | CPU・Memory・Disk・時間の計画 | 実測していなければ未測定と残す |

この表は第8章の読み方であり、任意の環境に安全を認定する検査ではない。実Runtimeの設定・到達性・残存を本付録で測定したとは記録しない。

## 保持するものと破棄するもの

Evidence manifestのID、相対Path、SHA-256、Producer、時刻、Run、由来、変換履歴、Custodian、Retentionを照合する。収集、検査、分析、報告を分けるNIST SP 800-86の考え方を限定参照し、古い製品操作やHash方式の推奨を引き継がない。［SRC-NIST-DFIR-001］

Hash一致は指定Byteの同一性であり、内容の真実、許可、取得前の完全性、法的証拠能力を単独では証明しない。親Case、供給JSON、保持原本はCleanup対象の一時資源と区別する。

第8章では、停止確認、Evidence export、Destroy、Cleanupの順を守る。保持が確認できなければ、Evidenceを失う破棄へ進めない。Container・Network・Volume・File・Credential・Portの六種を別々に照合し、CredentialがUnknownなら残り五種がPassでもCleanup verifiedにしない。

## 三Runの期待出力を読む

| Run | 判定 | 最終状態 | 正常完了 |
|---|---|---|---|
| RUN-LAB08-SAFE | Safe | Cleanup verified | true |
| RUN-LAB08-UNSAFE | Unsafe | Cleanup verified | false |
| RUN-LAB08-INCONCLUSIVE | Inconclusive | Failed closed | false |

Unsafeの後でCleanupが完了しても、そのFailを消さない。FailがあればUnknownより優先し、未訪問の段階はPassへ補完しない。構造欠損や未知の状態を検証エラーで拒否したことと、RunをInconclusiveと判定したことも別である。

## 自己点検と次の確認

次の五点を自分のメモだけから説明できれば、読解の提出物になる。

1. 対象Runと判断する問い。
2. 開始条件を支えるreceiptと不足しているもの。
3. 新規操作を止める条件と停止確認の有無。
4. 保持対象、破棄対象、六種Cleanupの各結果。
5. 残るGap、Owner、新Runに向けた再審査条件。

記入が完成しても実Controlが検証されたことにはならない。許可は[第2章](../manuscript/02-law-ethics-authorization.md)、RoEの期限と再開条件は[第9章](../manuscript/09-engagement-roe.md)、時点と証拠の意味は[第20章](../manuscript/20-dfir-timeline-causality.md)へ戻る。実Dataや権限不明を見つけたら停止し、読解課題を実操作へ拡張しない。

## 参考文献・Source Note ID

- `SRC-NIST-DFIR-001`

版・確認日・採用する節と採用しない内容は[付録A/D/Hの限定Source Review](../references/appendix-adh-source-review-2026-10-17.md)を参照する。親Caseの時点とAuthorityは変更しない。

停止したまま保留する場合は[付録D](appendix-d-troubleshooting.md)、許可の根拠は[付録A](appendix-a-legal-safety.md)へ戻る。
