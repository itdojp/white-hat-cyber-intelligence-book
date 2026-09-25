# Control Validation Plan

`ART-27`はControlの目的、試験条件、層別の期待とActual、改善と再評価を結ぶ。[第21章](../manuscript/21-purple-team-validation.md)と[完全合成記入例](../cases/ch21-control-validation-example.md)を参照する。Templateを埋めたことは、実操作の許可やControlの有効性の証明ではない。

## Plan and decision requirement

| Field | 記入内容 |
|---|---|
| Plan ID / version / Case | 判断対象、親Caseとrefines等の関係、旧版の保持 |
| Decision / Threat behavior | 何を判断するか、正常・Near-missと区別する条件 |
| Source / mapping basis | Source版と利用箇所。mappingと有効性を分ける |
| Subject / revision / window | 対象の同一性、設定版、観測範囲、Cutoff |
| Owner / reviewer | 検証担当、Evidence確認者、残存確認者 |
| Parent references | 親記録のID、用途、受領していないEvidence・権限・状態 |

## Authority, scope and safety

| Field | 記入内容 |
|---|---|
| RoE / Lab / Authority | 出所、版、期限、Scope、許可不足を明記 |
| Method / execution disposition | 供給記録比較と実操作を分離。本教材の実操作は0 |
| Preconditions | 対象版、必要入力、正常系、時間基準、担当 |
| Prohibited operation | 実Target・実Credential・実Dataは使わず、外部接続を行わない |
| Impact / stop | 許可不明や想定外入力で停止し、追加操作を続けない |
| Cleanup / residual | 解答Copyの整理計画と残存確認。実Runtime未作成と実影響未測定を区別 |

本教材の`suppliedAuthority`は読解用の条件であり、実権限を与えない。rootの`executionAuthorized=false`を保持する。親RoEの失効やDraftを、成果物の出来栄えで補わない。

## Control objective and scenario

| Field | 記入内容 |
|---|---|
| Control / objective / owner | 期待する機能、対象版、責任者 |
| Scenario ID / type | AtomicまたはEnd-to-End。方法の名前と混同しない |
| Selected layers | Prevention、Telemetry、Detection、Triage、Responseの評価対象を明示 |
| Trace / batch | 同一供給系列と対比条件。別Traceの寄せ集めをしない |
| Criterion / expected / partial | 比較Field、期待値、事前に定義した部分充足。nullは部分充足ではない |
| Normal / disconfirming case | Negative、Benign-near-miss、反証、入力不足の対比 |
| Expected evidence | 何の根拠が必要か、何がなければ結論できないか |

Atomicで未選択の層は暗黙のPassedではない。End-to-Endでも、五つの局所結果を一つの実安全性の証明へ潰さない。

## Evidence and actual by layer

| Field | 記入内容 |
|---|---|
| Evidence ID / origin | 完全合成の供給か実観測かを区別。本教材は前者のみ |
| Subject / scenario / control binding | 同じ対象・版・Scenario・Trace・Controlか |
| Recorded / available / cut-off | 供給時点、利用可能時点と判断締切。後着で旧結果を上書きしない |
| Actual / present / input basis | 期待値と別欄の値、入力有無、確認根拠 |
| Hash / preservation | 比較した表現と保持参照。真正性や権限を認定しない |
| Layer result | Passed / Failed / Partial / Indeterminate / Stopped |
| Failure class | Control / Telemetry / Detection logic / Workflow / Authority / Test design |
| Gap / permitted conclusion | 不足、反証範囲、限定結果、結論できない範囲 |

一つの層のFailedは全条件の失敗という意味ではない。不明条件のGapを併記する。部分充足は観測された範囲を示し、入力不足をPartialへ丸めない。

## Improvement, retest and handoff

| Field | 記入内容 |
|---|---|
| Action / source result | 改善案と元Failure・Gap・Evidenceの参照 |
| Owner / due / acceptance | 誰が何をいつまでに、何をもって確認するか |
| Retest ID / before / after | 旧失敗と旧版を保持し、新版のEvidenceを別IDへ結ぶ |
| Comparability | 同じ問い・対象・入力契約・正常系を保持。変える条件を明示 |
| Actual change disposition | 提案・供給版比較・実変更・効果確認を分離 |
| Reassessment / trigger | 入力、Schema、対象、Rule、権限、Source変更時の見直し |
| Handoff / receipt | 宛先、Action ID、Status、Receipt、実権限。予定は受領ではない |

本例の第22章向けHandoffはplanned-not-delivered、Receipt null、実行権限falseである。ControlのFailedやIndeterminateが残っても、Gap・担当・期限・次の判断を埋めた教材は完成し得る。

## Review checklist

- Control objectiveとExpectedをActualへ合わせて変えていない。
- 正常・異常・Near-miss・入力不足を必要な範囲で対比した。
- 層別の根拠と結果を、対象・版・Trace・Cutoffへ結んだ。
- 停止、部分充足、Unknown、未選択を区別した。
- 改善案、供給Retest、実変更、Handoff受領を混同していない。
- 親のEvidence・失効Authority・Draft・未配達・原因未確定を更新していない。
