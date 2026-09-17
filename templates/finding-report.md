# Finding Report

ART-04はFindingの条件・根拠・影響・対策・Decisionをつなぐ記録である。既存の見出しを維持し、[第15章](../manuscript/15-findings-retest-risk.md)で対象版と受容の欄を補う。空欄を推測で埋めず、Unknownとその理由・担当・期限を残す。

- Finding ID:
- Title:
- Status: Open / Mitigated / Accepted / Retest required / Closed / Reopened
- Scope: Confirmed / Candidate / Excluded / Unknownを分ける。
- Evidence timestamp / time zone:
- Case ID / refinesまたはindependent:
- Asset / Threat / Subject ID / Revision:
- Decision Requirement / Authority / RoE reference:

## Summary

SymptomとRoot conditionを別々に書く。確認事実、分析判断、仮定を区別し、確信度・代替説明・結論を変える条件を添える。

## Preconditions

対象、版、Scope、許可の状態、使用する供給資料を限定する。本書の合成課題では実操作を行わない。別Caseの許可やEvidenceを借用しない。

## Minimal-impact validation

- Validation ID / Finding ID / same subject and revision:
- Authorized operation: 本教材は供給記録の読解のみ。実施許可を発行しない。
- Expected result:
- Observed result / evidence basis:
- Stop point:
- Cleanup: 作業メモを整理し、正本・親資料を保持する。

## Evidence

| Evidence ID | Description | Hash / location | Limitations |
|---|---|---|---|
| 記入するEvidence ID | 同じ対象版の供給根拠 | 読み取り専用の参照 | 未確認の範囲 |

対象と版をlocationまたは説明で追跡する。供給値、観測、解釈を分け、実Credential・実個人情報を記入しない。

## Impact

- Technical impact:
- Business impact: 実測・仮説・未測定を区別する。
- Affected assets / identities: Confirmed / Candidate / Excluded / Unknown。

## Root cause

Root condition ID、主張、Evidence、代替説明、未確認範囲を記載する。症状の言い換えや、根拠のない組織・個人の責任断定にしない。

## Risk context

- Severity inputs: CVSSを記載する場合はScore / Vector / Nomenclatureを第7章の契約に従って併記する。未評価なら新たな値を作らない。
- Exposure:
- Exploitation evidence:
- Compensating controls:
- Priority rationale: 業務依存、Evidence不足、Owner、Urgency、Due dateを分ける。

## Remediation

- Immediate containment: Temporary案のTreatment ID / Control ID。
- Permanent correction: Permanent案のTreatment ID / Control ID。
- Alternative control: Compensating案のTreatment ID / Control ID。
- 各案の便益 / 負担 / Dependency / Owner / Due date:
- Recommended Treatment IDと選択理由:

案を実装済みと混同しない。一時的な緩和や監査の追加を、根本条件の解消と同じ意味で表示しない。

## Retest acceptance criteria

[ART-23](retest-record.md)へRetest ID、Finding ID、Change reference、対象・変更前後版、Scope、期待Evidence、Method、限界を接続する。Scanner要約だけでRetest完了としない。

## Residual risk and owner

- Residual risk ID / 未確認条件 / Owner:
- Decision ID / Finding ID / Action / 判断理由:
- Acceptance ID / Authority reference / Holder / Decision owner / Scope:
- Decision time / Expiry / Conditions:
- Reassessment ID / Owner / Due date / Reopen trigger:
- Disclosure classification / Audience / Coordination status:

Closedには十分なRetestまたは明示的で有効なRisk acceptanceの根拠を記す。受容で閉じた場合は「修正済み」と表示しない。受容権限は評価作業のAuthorityを上書きしない。教材のAudienceはSynthetic internal roles、coordinationStatusはNot initiatedで、実届出・実公表は行わない。

[完全合成記入例](../cases/ch15-findings-retest-risk-example.md)で、記録の完了と業務課題の解決を区別する。
