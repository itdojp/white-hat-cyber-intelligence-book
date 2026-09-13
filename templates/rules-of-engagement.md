# Rules of Engagement

`ART-02`は、確認済みAuthorizationを実施条件へ具体化する記録です。空欄、Unknown、矛盾、期限経過を包括許可へ読み替えません。本書の記入例は完全合成・非実行の計画であり、署名や実施許可を発行しません。

## 1. Document ControlとDecision

| Field | 記入内容 |
|---|---|
| Artifact / RoE ID / Version | ART-02、既存記録と衝突しないRoE ID、審査対象の版 |
| Status / As of | Draft / Under review / Approved / Active / Paused / Revoked / Expired / Completedのいずれか、基準時点 |
| Case / Relation | Parent Case ID、refinesまたは別Caseとのindependent。置換なら根拠を明示 |
| Decision Requirement / Owner | 必要な問い、責任者、判断期限と計画レビュー期限の区別 |
| Success / Information gap | 何が分かれば判断できるか、未確定事項、停止中でも残すGap |

## 2. Authorization evidenceと役割

| Field | 記入内容 |
|---|---|
| Authority record / Decision ID | 根拠と判断の直接ID。親のOutcomeと現在の有効性を分ける |
| Scope of authority / Validity | 許可者の権限範囲、有効開始・終了、Timezone、取消し確認 |
| Sponsor / Authority owner | 目的・予算の責任と許可根拠の確認責任を分ける |
| System / Data owner | 対象・Dataの権限、第三者条件、未確認事項 |
| Test lead / Emergency role | 実施統括と停止連絡、代替担当 |
| Written evidence / Signoff | 同じRoE ID・版・対象に結び付いた署名または変更不能な参照 |

Source、Tool、CI、LabのPassをAuthorizationの代替にしません。根拠の真正性や法的適用を機械検査で承認したとは扱いません。期限経過、取消し、役割不明ならDo not proceedです。

## 3. ScopeとDependency

| Field | 記入内容 |
|---|---|
| Scope ID / In scope | Asset、Identity、Environment、Data、Objectの正確なIDと所有者 |
| Out of scope | 明示的対象外。未記載は既定拒否 |
| Dependency / Third party | 必要な共有基盤・第三者条件、権限確認者。不要なら不要と記入 |
| Ambiguity / Overlap | Wildcard、所有不明、対象/対象外の重複は解消まで開始不可 |

## 4. Permitted、Conditional、Prohibited methods

| Field | 記入内容 |
|---|---|
| Method ID / Purpose | Tool名ではなく目的、入力、出力、作用のクラス |
| Permitted | Scope内の必要最小限の作用だけを列挙 |
| Conditional | 追加条件・確認者・Evidenceが明確なものだけ。未確定なら許可しない |
| Prohibited | 対象外への作用と禁止事項を明記。Permittedと重複させない |

標準教材では実TargetへのScan・認証試行を行いません。実Credentialの取得・再利用、第三者への通信、DoS、Persistence、Evasion、Log deletion、破壊的変更を許可しません。

## 5. Window、Rate、Volume、Resource budget

開始・終了・Timezoneを指定し、Authorization期間内に収めます。Request数、対象件数、Evidence量、Concurrency、Retry、Durationなどは単位と計測方法を記入します。上限超過時の停止先を決め、後付けで予算を増やしません。数値を記入しても実装済み制限や実測保証にはなりません。

## 6. Data、Evidence、Retention

| Field | 記入内容 |
|---|---|
| Data ID / Classification | 許可Data、所有者、禁止Data、Credentialの参照と値の分離 |
| Evidence ID / Required fields | RoE ID/版、Scope/Method、対象、時刻、Custodian、Source/限界、Stop/処置 |
| Storage / Access / Custodian | 保存先、読取権限、責任者、原本と作業コピーの区別 |
| Retention / Destruction | 保持期間と起点、廃棄対象・除外対象・責任者・確認Evidence |
| Unexpected data / Disclosure | 追加取得・表示・転送を止め、参照IDで通知。公表は別判断 |

実Credential・Token・Cookie・PIIを標準Evidenceとして取得しません。Hash一致はbyteの確認であって、真正性・法的証拠能力・実行成功の保証ではありません。

## 7. StopとEmergency contact

Authority不明、Scope drift、予期しないData、通信、量超過、Evidence欠落、連絡不能、Cleanup未確認を停止候補として検討します。Stop ID、Primary/Backup、応答待ち時間、時刻記録、Escalation先を記入します。UnknownをPassへ置き換えません。

## 8. Recovery、Cleanup、Restart

Recovery owner、影響確認、保存すべき参照、復旧順序、Cleanup対象と除外対象、残存確認、Evidence IDを記入します。Cleanup完了と再開承認を分離します。停止原因の解消確認と同じRoE版に結び付いたRestart authorityの承認がなければ、自動再開しません。

## 9. Completion、Success、Inconclusive

Technical completionには対象件数・予算・停止・Cleanupの記録を、Decision completionには必要Evidence・Gap・代替説明・Confidence・受入責任者・再評価を記入します。作業完了を判断完了に読み替えず、Evidence不足はInconclusiveとして残します。何も観測しなかったことだけで不存在とは結論しません。

## 10. Change、Reauthorization、Retest

Change request ID、変更前後の版、Scope/Method/Data/Time/Budget/Owner/Stopの変更、Reauthorization ID、確認者、承認参照を記入します。Retestには対象・修正内容・方法・期間・新しいEvidenceの条件を付けます。旧版の承認を新しい版や別Caseへ自動継承しません。

## 11. HandoffとReturn

後続AssessmentへRoE ID/版、Scope、Method、Stop、許可根拠を渡し、Hypothesis→Validation→EvidenceまたはGapを返してもらいます。RetestとControl Validationも独立の範囲・期間・承認を確認します。必要な入力が欠ければ開始せず、承認者への差戻しを記録します。

## 12. Approval checklist

- 根拠の許可者と対象権限、有効期間、第三者条件が確認できる。
- 同じRoE版をSponsor、Authority owner、System owner、Data owner、Test leadが担当範囲ごとに確認している。
- Scopeと対象外、Method、時間と量、Data、Stop/連絡、Recovery/残存確認が一意である。
- Technical/Decisionの完了条件、Inconclusive、Retestと再承認が明確である。
- 不明・失効・取消し・矛盾があればDo not proceedを記録する。

[第9章](../manuscript/09-engagement-roe.md)と[完全合成記入例](../cases/ch09-engagement-roe-example.md)はこのTemplateの入力・判断・引渡しを説明します。旧`ROE-2026-001`や独立`ROE-2026-011`の権限を更新するTemplateではありません。
