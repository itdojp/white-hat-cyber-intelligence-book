# Lab Safety and Evidence Plan

## Document Control

Artifact IDはART-18。目的、開始条件、停止、Evidence保持、Cleanup、再評価を一つの計画として記録する。一般Templateは設計のための書式であり、付属の機械契約はレビュー済み三Runの合成モデル1.0.0だけを受理する。

| Field group | 記入する内容 |
|---|---|
| Plan / Case / Relation | Plan Set / Plan / Run / Lab ID、親Case、refines等の関係、親の状態を変更しない限定 |
| Decision / Authority / Scope | 判断要求、許可記録、RoE参照または非発行の理由、対象・時間・手法・Dataの境界。不明なら停止 |
| Owner / Reviewer | 計画と停止を担うRole、証拠・再開条件を審査するRole |
| Asset / Boundary / Parent | 資産、境界、Signal Flow、優先順位記録、親CoverageとGapの直接ID |
| Purpose / Assumptions | 確認したい問い、合成である範囲、未測定の条件、実行の有無 |

## Lab境界と開始条件

| Field group | 記入する内容 |
|---|---|
| Implementation / Version | OS・Runtime・Image digest・設定版。非実行モデルはnot-executedとnullの理由 |
| Privilege / Host | rootless、非特権、追加Capabilitiesなし。host networkと広範なHost mountは禁止 |
| Network / Exposure | 外向き通信は既定拒否、ローカル限定、予約済みHost・文書用Addressだけ |
| Data / Storage / Secret | 合成のみ、入力は読み取り専用、出力専用領域、実Credentialを持ち込まない |
| Resource / Time | CPU・Memory・Disk・時間の上限と確認Evidence。未測定なら未測定 |
| Preflight | Authority、rootless、privileges、network、egress、mount、data、collectionの各receipt |
| Runtime observation | egress、scope、privileges、data、resources、collection、clockの各receipt |
| Expected / Prohibited evidence | 必要な合成観測と、収集しない実Dataを別欄に記録 |

## 八状態と三判定

状態はPlanned / Preflight passed / Ready / Running / Stopped / Destroyed / Cleanup verified / Failed closedの八つ。各receiptの結果はPass / Fail / Unknown、Run判定はSafe / Unsafe / Inconclusiveとする。実行許可と混同しない。

開始前のFailまたはUnknownではRunningへ進まない。実行中の異常では新規シナリオ操作を停止する。Failed closedから同じRunを再開しない。停止・Evidence export・破棄・残存確認の順序と、実施できなかった段階を明記する。

Cleanup verifiedでも以前のFailはUnsafeとして保持し、completedNormallyはfalseとする。全RunのexecutionAuthorizedはfalseである。Safeも実作業の許可ではない。

## Evidence manifest

| Field group | 記入する内容 |
|---|---|
| Identity / Locator | Manifest ID、Evidence Artifact ID、実際に読む相対Path、Fixture ID、対象Run IDs |
| Integrity | 実際のByteから計算したSHA-256、文字コード、改行、照合結果 |
| Origin / Time | Producer、作成日時とTime zone、取得か合成生成か、時計の前提 |
| Transform history | 操作種別、入力ID、出力ID、処理主体、版、日時。変換なしでも生成由来は残す |
| Handling | Classification、Custodian、Retention、作業コピーと保持原本の区別 |
| Limitation | Hash一致は真実性、取扱いの完全性、法的証拠能力、実行成功の証明ではない |

実Credential・実Token・実Cookie・個人情報は収集しない。付属Evidenceは完全合成である。Hashだけを更新して出所・Run・表示の不整合を隠さない。

## Stop / Cleanup / Reassessment

| Field group | 記入する内容 |
|---|---|
| Step / Stop | 合成Replay Step ID、Stop ID、条件、停止確認receipt、緊急連絡Role。予期しない外部影響・実Data・許可不明なら停止 |
| Evidence export | 保持対象、export確認receipt、失敗時に破棄へ進めない理由 |
| Destroy | 事前計画内の破棄確認。停止成功だけで破棄済みとしない |
| Cleanup | Cleanup IDとContainer・Network・Volume・File・Credential・Portの六種receipt |
| Retention boundary | 保持するEvidence正本と、破棄対象の一時資源の区別 |
| Judgment / Gap | 判定、履歴、正常完了、未訪問段階、不明点、根拠、確信度、代替説明 |
| Reassessment | 新Run ID、再審査Trigger、Owner、次回Review日、再開に必要なEvidence |

不明をPassに置換しない。実Runtimeを動かしていないなら、停止・削除・残存を実測したとは記録しない。教材コマンドのCleanupは自分で保存した報告コピーの整理だけで、親Caseや版管理されたEvidenceを削除しない。

## Rubricと完全記入例

[第8章](../manuscript/08-safe-lab-evidence.md)のRubricと[完全合成記入例](../cases/ch08-lab-evidence-example.md)を対にする。Unknownを残しても、必要なEvidence・責任者・再評価まで記録できれば提出できる。根拠のない安全宣言や、親のCoverageの昇格は差戻しとする。
