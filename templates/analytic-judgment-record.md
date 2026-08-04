# Analytic Judgment Record

## 目的

このテンプレートは、Decision RequirementまたはIntelligence Requirementに対し、Evidence、Source Note、競合仮説、不確実性、アトリビューション限界、Reassessment条件を一体で記録するために使用する。

本文では、Confirmed Fact、Assumption、Judgment、Forecast、Recommendationを必ず分離する。Technical clusterからOperator、組織、国家への飛躍を防ぐため、Attribution Ladderの適用段と許容表現を明示する。

## 使用条件

- 実在第三者Systemへの追加調査を前提にしない。
- 実在個人、実在組織、実在国家の帰属を記載しない。
- 実Credential、Token、Cookie、個人情報を含めない。
- 同じ原典の再掲を独立裏付けとして数えない。
- false flag、shared tooling、infrastructure reuseの可能性を評価する。

## 0. Document Control

| Field | Value |
|---|---|
| Artifact ID | `ART-12` |
| Case ID | `CASE-YYYY-025` |
| Title |  |
| Status | Draft / Active / Decision Support / Reassessment Due / Closed |
| Analytic cut-off | ISO 8601 |
| Decision owner |  |
| Primary analyst |  |
| Reviewers |  |
| Classification | Public / Internal / Confidential / Restricted |
| Created at | ISO 8601 |
| Updated at | ISO 8601 |

## 1. Decision Requirement and Intelligence Requirement

| Field | Value |
|---|---|
| Decision Requirement ID | `DR-CASE-025` |
| Intelligence Requirement ID | `IR-CASE-025` |
| Decision to support |  |
| Decision deadline | ISO 8601 |
| Consumer / customer |  |
| Key question |  |
| Out-of-scope question |  |
| Maximum acceptable uncertainty |  |
| Decision impact if wrong |  |

## 2. Scope, Safety, and Ownership Boundary

| Field | Value |
|---|---|
| Scope statement |  |
| Allowed data | Synthetic logs / synthetic bulletins / synthetic exports |
| Prohibited data | 実Credential / 個人情報 / 実在第三者Data |
| OWN boundary |  |
| BRIDGE boundary |  |
| DELEGATE boundary |  |
| Stop condition |  |

## 3. Candidate Threat Hypotheses

Threat Hypothesisは、脅威行動、想定対象、前提、観測可能な影響を記録する。Source reliability、independence、lineage、circular reportingの評価をThreat Hypothesisへ混在させない。

| Threat Hypothesis ID | Related Decision Requirement ID | Related Intelligence Requirement ID | Statement | Preconditions | Expected observable | Expected impact | Current assessment |
|---|---|---|---|---|---|---|---|
| `TH-CASE-025-001` | `DR-CASE-025` | `IR-CASE-025` |  |  |  |  | Proposed / Supported / Partially supported / Weakened / Inconclusive / Rejected |
| `TH-CASE-025-002` | `DR-CASE-025` | `IR-CASE-025` |  |  |  |  |  |
| `TH-CASE-025-003` | `DR-CASE-025` | `IR-CASE-025` |  |  |  |  |  |

## 4. Observation Hypotheses and Collection Gaps

### 4.1 Observation Hypotheses

| Observation Hypothesis ID | Related Threat Hypothesis ID | Expected signal | Data source | Time window | Disconfirming observation |
|---|---|---|---|---|---|
| `OBS-CASE-025-001` | `TH-CASE-025-001` |  |  |  |  |

### 4.2 Source-evaluation hypotheses

Source-evaluation hypothesisは、報告の来歴、independence、circular reportingを評価するためだけに用いる。Threat Hypothesis IDへ混在させない。

| Observation Hypothesis ID | Source-evaluation hypothesis ID | Statement | Expected signal | Data source | Disconfirming observation |
|---|---|---|---|---|---|
| `OBS-CASE-025-002` | `SEH-CASE-025-001` |  |  |  |  |

### 4.3 Alternative-hypothesis test observations

| Observation Hypothesis ID | Related Alternative Hypothesis ID | Expected signal | Data source | Disconfirming observation |
|---|---|---|---|---|
| `OBS-CASE-025-003` | `ALT-CASE-025-001` |  |  |  |

### 4.4 Collection Gaps

| Collection Gap ID | Related hypothesis or question | Missing evidence | Why it is missing | Decision impact | Priority |
|---|---|---|---|---|---|
| `GAP-CASE-025-001` |  |  |  |  | 高 / 中 / 低 |

## 5. Alternative Hypotheses and Key Assumptions

### 5.1 Alternative Hypotheses

| Alternative Hypothesis ID | Explanation | Supporting evidence | Contradicting evidence | What would weaken it |
|---|---|---|---|---|
| `ALT-CASE-025-001` |  |  |  |  |

| Alternative Hypothesis ID | Focus question | Relationship to primary judgment | Current disposition | Related Evidence IDs |
|---|---|---|---|---|
| `ALT-CASE-025-001` |  | directly competing / attribution boundary |  |  |

### 5.2 Key Assumptions

| Assumption ID | Statement | Why needed | Failure trigger | Related Gap IDs |
|---|---|---|---|---|
| `ASM-CASE-025-001` |  |  |  | `GAP-CASE-025-001` |

## 6. Source Notes and Evidence Register

### 6.1 Source Notes

| Source Note ID | Origin | Reliability | Credibility | Independence group | Collected at | Provenance note | Limitation |
|---|---|---|---|---|---|---|---|
| `SN-CASE-025-001` |  |  |  |  | ISO 8601 |  |  |

### 6.2 Evidence Register

| Evidence ID | Source Note ID | Related Observation / Source-evaluation hypothesis ID | Question supported | Collected at | Integrity / hash | Limitation | Synthetic confirmation |
|---|---|---|---|---|---|---|---|
| `EVD-CASE-025-001` | `SN-CASE-025-001` | `OBS-CASE-025-001` |  | ISO 8601 |  |  | yes |

### 6.3 Negative Finding

Missing evidenceとevidence of absenceを分離する。

| Negative Finding ID | Related Evidence IDs | Related Observation Hypothesis ID | Searched behavior | Search window | Available coverage | Gap | Permitted conclusion |
|---|---|---|---|---|---|---|---|
| `NEG-CASE-025-001` | `EVD-CASE-025-001` | `OBS-CASE-025-001` |  |  |  |  |  |

## 7. Uncertainty Register

| Uncertainty ID | Type | Description | Affected IDs | Mitigation | Residual effect |
|---|---|---|---|---|---|
| `UNC-CASE-025-001` | translation / timestamp / entity / provenance |  |  |  |  |

## 8. Lineage, Circular Reporting, and Deception

### 8.1 Lineage Register

| Lineage Edge ID | From Source Note ID | To Source Note ID | Relationship | Independence effect |
|---|---|---|---|---|
| `LIN-CASE-025-001` | `SN-CASE-025-001` | `SN-CASE-025-002` | cites / republishes / derived-from | counts-as-same / independent / unknown |

### 8.2 Circular Reporting Candidates

| Circular Reporting ID | Related Source Note IDs | Why it is circular or same-origin | Do not count as independent corroboration |
|---|---|---|---|
| `CR-CASE-025-001` | `SN-CASE-025-002`, `SN-CASE-025-003` |  | yes |

### 8.3 Source-evaluation judgments

Source-evaluation judgmentは、independenceやcorroborationの評価を記録する。Confirmed Factへは直接観測したEventだけを置く。

| Source-evaluation Judgment ID | Statement | Basis | What would change it |
|---|---|---|---|
| `SEJ-CASE-025-001` |  | `SEH-CASE-025-001`, `LIN-CASE-025-001` |  |

### 8.4 Deception / False Flag / Shared Tooling / Infrastructure Reuse

| Deception Candidate ID | Category | Description | Evidence IDs | Alternative explanation supported | Analyst note |
|---|---|---|---|---|---|
| `DECPT-CASE-025-001` | false flag / shared tooling / infrastructure reuse |  | `EVD-CASE-025-001` | `ALT-CASE-025-001` |  |

## 9. Attribution Ladder Assessment

| Attribution Assessment ID | Ladder level | Evidence threshold met | Related Evidence IDs | Related Alternative Hypothesis IDs | Permitted language | Prohibited jump |
|---|---|---|---|---|---|---|
| `ATTR-CASE-025-001` | L1 / L2 / L3 / L4 / L5 / L6 |  |  |  |  |  |

## 10. Structured Analytic Judgment

### 10.1 Confirmed Facts

Confirmed Factには、直接観測したEventのみを記録する。independence、corroboration、lineageの評価はSource-evaluation judgmentまたはLineage Registerへ置く。

| Confirmed Fact ID | Statement | Evidence IDs |
|---|---|---|
| `CF-CASE-025-001` |  | `EVD-CASE-025-001` |

### 10.2 Assumptions

| Assumption ID | Statement | Why needed | Failure trigger | Related Gap IDs |
|---|---|---|---|---|
| `ASM-CASE-025-001` |  |  |  | `GAP-CASE-025-001` |

### 10.3 Judgments

| Analytic Judgment ID | Statement | Confidence | Basis | Related Alternative Hypothesis IDs | What would change the judgment |
|---|---|---|---|---|---|
| `AJ-CASE-025` |  | 高 / 中 / 低 |  | `ALT-CASE-025-001` |  |

### 10.4 Forecasts

| Forecast ID | Statement | Time horizon | Confidence | Indicators / Signposts |
|---|---|---|---|---|
| `FOR-CASE-025-001` |  | 7日 / 30日 / 90日 | 高 / 中 / 低 | `IND-CASE-025-001` |

### 10.5 Recommendations

| Recommendation ID | Statement | Owner | Priority | Related Decision ID |
|---|---|---|---|---|
| `REC-CASE-025-001` |  |  | 高 / 中 / 低 | `DEC-CASE-025` |

## 11. Indicators and Signposts

| Indicator / Signpost ID | Statement | Related hypothesis | Monitoring source | Escalation trigger |
|---|---|---|---|---|
| `IND-CASE-025-001` |  | `TH-CASE-025-001` |  |  |

## 12. Decision Record and Collection Priority

### 12.1 Decision Record

| Field | Value |
|---|---|
| Decision ID | `DEC-CASE-025` |
| Related Analytic Judgment ID | `AJ-CASE-025` |
| Selected option |  |
| Rejected options and reason |  |
| Residual risk |  |
| Communication scope |  |

### 12.2 Collection Priority

| Collection Gap ID | Priority | Why it matters to the decision | Owner | Due date |
|---|---|---|---|---|
| `GAP-CASE-025-001` | 高 / 中 / 低 |  |  | ISO 8601 |

## 13. Reassessment and Invalidation

| Field | Value |
|---|---|
| Reassessment ID | `REA-CASE-025` |
| Review date | ISO 8601 |
| Triggering indicators / signposts | `IND-CASE-025-001` |
| Invalidation condition |  |
| Next action if invalidated |  |

## 14. Traceability Check

- Case ID、Decision Requirement ID、Intelligence Requirement IDが全表に一貫している
- Threat Hypothesis IDが三つ以上ある
- Evidence IDがSource Note IDへ遡れる
- Negative FindingがCoverageとGapを分離している
- Confidence表現は`高 / 中 / 低`だけを使っている
- Technical clusterからSponsorへの飛躍がない
- Circular reporting候補を独立裏付けに数えていない

## 15. Review

| Review area | Reviewer / role | Result | Date | Evidence reference | Notes |
|---|---|---|---|---|---|
| Technical correctness |  | Pass / Changes required |  |  |  |
| Safety / authorization |  | Pass / Changes required |  |  |  |
| Evidence / source quality |  | Pass / Changes required |  |  |  |
| Analytic quality |  | Pass / Changes required |  |  |  |
| Decision usefulness |  | Pass / Changes required |  |  |  |
