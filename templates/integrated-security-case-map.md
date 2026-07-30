# Integrated Security Case Map

## 目的

このテンプレートは、Security Assessment、Detection Engineering、Threat Hunting、Incident Response / DFIR、Cyber Threat Intelligence、経営判断、再評価を、同一のCaseと証拠関係で接続するために使用する。

ツールの実行履歴を並べるのではなく、次を追跡可能にする。

- 誰が、何を、いつまでに判断するのか
- その判断に必要な仮説と証拠は何か
- どの権限と停止条件で検証したか
- 何を観測でき、何を観測できなかったか
- どの分析判断と代替仮説があるか
- どの措置を選び、いつ再評価するか

## 使用条件

- 実在する第三者システムを対象にしない。
- 実Credential、Token、Cookie、個人情報を記載しない。
- 検証対象は、明示的に許可された自己所有環境または隔離された合成環境に限定する。
- Actorや国家への帰属は、技術的類似だけで断定しない。
- 取得した証拠の分類、保持期限、共有範囲を記録する。

## 0. Document Control

| Field | Value |
|---|---|
| Artifact ID | `ART-10` |
| Case ID | `CASE-YYYY-NNN` |
| Title |  |
| Status | Draft / Active / Decision Recorded / Reassessment Due / Closed |
| Owner |  |
| Contributors |  |
| Classification | Public / Internal / Confidential / Restricted |
| Created at | ISO 8601 |
| Updated at | ISO 8601 |
| Review deadline | ISO 8601 |
| Related Issue / Ticket |  |

## 1. Decision Requirement

| Field | Value |
|---|---|
| Decision Requirement ID | `DR-CASE-001` |
| Decision owner |  |
| Decision deadline |  |
| Decision to make |  |
| Available options |  |
| Decision criteria |  |
| Maximum acceptable uncertainty |  |
| Consequence of delay |  |
| Required approvers |  |

### 判断に不要な問い

今回の期限内に解く必要がない問いを明示する。

- （記入）

## 2. Scope, Authority, and Safety

| Field | Value |
|---|---|
| Authority / RoE ID | `ROE-CASE-001` |
| In-scope assets |  |
| Out-of-scope assets |  |
| Permitted operations |  |
| Prohibited operations |  |
| Permitted data |  |
| Test window |  |
| Stop conditions |  |
| Emergency contact |  |
| Cleanup owner |  |
| Evidence retention |  |

## 3. Business and Technical Context

### 3.1 Assets

| Asset ID | Asset / Service | Business role | Criticality | Data classification | Owner |
|---|---|---|---|---|---|
| `ASSET-CASE-001` |  |  |  |  |  |

### 3.2 Trust Boundaries

| Boundary ID | From | To | Identity / protocol | Control | Failure consequence |
|---|---|---|---|---|---|
| `TB-CASE-001` |  |  |  |  |  |

### 3.3 Business Constraints

- Availability requirement:
- Contractual requirement:
- Privacy / regulatory requirement:
- Recovery objective:
- Operational dependency:
- Approved compensating control:

## 4. Hypotheses

### 4.1 Threat Hypotheses

| Hypothesis ID | Statement | Preconditions | Expected impact | Priority | Status |
|---|---|---|---|---|---|
| `TH-CASE-001` |  |  |  |  | Proposed / Testable / Supported / Weakened / Rejected |

### 4.2 Observation Hypotheses

| Observation ID | Related threat hypothesis | Expected signal | Data source | Time window | Disconfirming observation |
|---|---|---|---|---|---|
| `OBS-CASE-001` | `TH-CASE-001` |  |  |  |  |

### 4.3 Alternative Explanations

| Alternative ID | Explanation | Supporting evidence | Contradicting evidence | What would distinguish it |
|---|---|---|---|---|
| `ALT-CASE-001` |  |  |  |  |

## 5. Authorized Validation Plan

| Validation ID | Related hypothesis | Minimal operation | Expected evidence | Stop condition | Cleanup |
|---|---|---|---|---|---|
| `VAL-CASE-001` | `TH-CASE-001` |  |  |  |  |

### 実施しない検証

影響が大きい、権限外、または判断に不要なため実施しない操作を記録する。

- （記入）

## 6. Evidence Register

| Evidence ID | Question supported | Source / collector | Collected at | Integrity / hash | Limitation | Classification |
|---|---|---|---|---|---|---|
| `EVD-CASE-001` |  |  |  |  |  |  |

### Negative Finding

観測されなかったことを「不存在」と同一視しない。

| Negative Finding ID | Searched behavior | Search window | Available coverage | Gaps | Permitted conclusion |
|---|---|---|---|---|---|
| `NEG-CASE-001` |  |  |  |  |  |

## 7. Findings and Control Gaps

| Finding ID | Root condition | Evidence IDs | Business impact | Existing control | Recommended treatment | Status |
|---|---|---|---|---|---|---|
| `FIND-CASE-001` |  |  |  |  |  | Open / Mitigated / Accepted / Retest Required |

## 8. Telemetry, Detection, and Hunting

### 8.1 Telemetry Requirements

| Telemetry ID | Behavior / question | Required event and fields | Retention | Current state | Gap owner |
|---|---|---|---|---|---|
| `TEL-CASE-001` |  |  |  | Available / Partial / Missing |  |

### 8.2 Detection Validation

| Detection ID | Related hypothesis | Logic / query reference | Test fixture | Expected result | Actual result | Limitations |
|---|---|---|---|---|---|---|
| `DET-CASE-001` | `TH-CASE-001` |  |  |  |  |  |

### 8.3 Hunt or Incident Records

| Record ID | Type | Question | Time range | Result | Evidence IDs | Next action |
|---|---|---|---|---|---|---|
| `HUNT-CASE-001` | Hunt / Incident |  |  |  |  |  |

## 9. Analytic Judgment

| Field | Value |
|---|---|
| Analytic Judgment ID | `AJ-CASE-001` |
| Key judgment |  |
| Confidence | High / Moderate / Low |
| Basis for confidence |  |
| Confirmed facts |  |
| Assumptions |  |
| Alternative hypotheses |  |
| Information gaps |  |
| Deception / manipulation risk |  |
| Indicators and signposts |  |
| Conditions that would change the judgment |  |

## 10. Decision Record

| Field | Value |
|---|---|
| Decision ID | `DEC-CASE-001` |
| Decision owner |  |
| Decision time |  |
| Selected option |  |
| Rejected options and reason |  |
| Required actions |  |
| Action owners |  |
| Deadline |  |
| Residual risk |  |
| Risk acceptance authority |  |
| Communication scope |  |

## 11. Control Improvement and Retest

| Control ID | Improvement | Owner | Due date | Verification method | Result |
|---|---|---|---|---|---|
| `CTRL-CASE-001` |  |  |  |  | Planned / Passed / Failed / Partial |

## 12. Reassessment

| Field | Value |
|---|---|
| Reassessment ID | `REA-CASE-001` |
| Scheduled date |  |
| Trigger conditions |  |
| Evidence to recollect |  |
| Hypotheses to retest |  |
| Decision to revisit |  |
| Closure criteria |  |

## 13. Handoff Contracts

| Handoff ID | Provider | Consumer | Required input | Acceptance criteria | Rejection / return condition | Deadline |
|---|---|---|---|---|---|---|
| `HO-CASE-001` |  |  |  |  |  |  |

## 14. Outcome Metrics

件数ではなく、判断とリスク低減の結果を測る。

| Metric ID | Metric | Baseline | Target | Measurement window | Owner |
|---|---|---:|---:|---|---|
| `MET-CASE-001` | Decision latency |  |  |  |  |
| `MET-CASE-002` | Critical hypothesis evidence coverage |  |  |  |  |
| `MET-CASE-003` | Verified control improvement rate |  |  |  |  |
| `MET-CASE-004` | Reassessment completed by due date |  |  |  |  |

## 15. Traceability Check

- [ ] Decision Requirementから各Hypothesisへ追跡できる
- [ ] 各HypothesisにObservationまたは明示的な情報ギャップがある
- [ ] 各FindingにEvidence IDがある
- [ ] 各Detection / Hunt / Incident recordが対象Hypothesisへ接続している
- [ ] Analytic Judgmentが事実、仮定、代替仮説、確信度を分離している
- [ ] Decision Recordが選択肢、残存リスク、責任者、期限を持つ
- [ ] 改善後のRetestとReassessmentが定義されている
- [ ] Handoffの受入条件と差戻し条件が定義されている

## 16. Review

| Review area | Reviewer / role | Result | Date | Notes |
|---|---|---|---|---|
| Technical correctness |  | Pass / Changes required |  |  |
| Safety / authorization |  | Pass / Changes required |  |  |
| Evidence / source quality |  | Pass / Changes required |  |  |
| Analytic quality |  | Pass / Changes required |  |  |
| Decision usefulness |  | Pass / Changes required |  |  |
