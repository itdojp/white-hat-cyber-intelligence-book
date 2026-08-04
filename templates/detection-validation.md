# Detection Validation Record

## 0. Document Control

| Field | Value |
|---|---|
| Artifact ID | `ART-05` |
| Detection Validation Record ID | |
| Case ID | |
| Related Case Map Case ID | |
| Related Case Map Decision ID | |
| Related Case Map Detection ID | |
| Detection relationship | refines / supersedes / independent |
| Related Case Map Fixture ID | |
| Related Case Map Control ID | |
| Decision Requirement ID | |
| Response Objective ID | |
| Detection ID | |
| Status | Draft / Validated / Needs Review / Deprecated |
| Detection owner | |
| Review cadence | |
| Last validated at | |
| Next review at | |

## 1. Detection Objective and Scope

| Field | Value |
|---|---|
| Business or response objective | |
| Protected asset / workflow | |
| In scope | |
| Out of scope | |
| OWN / BRIDGE / DELEGATE boundary | |
| ATT&CK mapping | |
| ATT&CK mapping is not coverage proof | Yes / No |

## 2. Hypotheses and Traceability

### 2.1 Threat and observation hypotheses

| Hypothesis ID | Type | Related Decision Requirement ID / Response Objective ID | Statement | Priority | Status |
|---|---|---|---|---|---|
| `TH-*` | Threat | | | | |
| `OBS-*` | Observation | | | | |

### 2.2 Handoff and response contracts

| ID | Type | Provider | Consumer | Required input | Acceptance criteria |
|---|---|---|---|---|---|
| `TRI-*` | Triage | | | | |
| `HO-*` | Incident handoff | | | | |

### 2.3 Detection backlog inputs

| Backlog Item ID | Input type | Related source ID | Requested detection change | Disposition |
|---|---|---|---|---|
| `DBI-*` | Finding / Hunt / Incident / CTI | | | Accept / Defer / Reject |

## 3. Data Requirement and Semantics Contract

| Telemetry ID | Source | Event / record | Required fields | Optional enrichment fields | Time contract | Identity contract | Retention | Coverage | Gap |
|---|---|---|---|---|---|---|---|---|---|
| `TEL-*` | | | | | | | | Available / Partial / Missing | |

### Field semantics notes

- `event_time` meaning:
- `ingest_time` meaning:
- `null` and empty-list semantics:
- ID normalization or join rules:
- Sampling, parser drift, or ordering caveats:

## 4. Detection Logic and Detection-as-Code Lifecycle

| Field | Value |
|---|---|
| Detection logic summary | |
| Rule / query reference | |
| Correlation window | |
| Threshold / condition | |
| Suppression / allow list | |
| Severity policy | |
| Version / change set | |
| Fixture replay command or procedure | |
| Deploy gate | |
| Maintenance trigger | |
| Deprecation trigger | |
| Deprecation owner | |

## 5. Synthetic Fixture Set

| Fixture ID | Fixture type | Telemetry presence | Target behavior event presence | Benign-near-miss context | Expected result | Notes |
|---|---|---|---|---|---|---|
| `FIX-*` | Positive | Present | Present | Absent | Alert | |
| `FIX-*` | Negative | Present | Absent | Absent | No alert | |
| `FIX-*` | Benign near miss | Present | Present | Present | No alert / Allowed | |

### Fixture safety checks

- syntheticOnly:
- offlineOnly:
- noMalwareOrC2:
- noCredentialTheft:
- noRealCredentialsOrPII:

## 6. Validation Results and Evidence Register

| Evidence ID | Fixture ID | Telemetry IDs used | Detection ID | Result | Analyst note | Collected at |
|---|---|---|---|---|---|---|
| `EVD-*` | | | | Pass / Fail / Partial | | |

## 7. Negative Finding and Coverage Limits

| Negative Finding ID | Related Evidence IDs | Coverage | Gap | Permitted conclusion |
|---|---|---|---|---|
| `NEG-*` | | | | |

**Rule**: Telemetry absenceとEvent absenceを混同しない。Gapが残る場合は、`侵害不存在`や`行動不存在`を断定しない。

## 8. Quality and Outcome Metrics

| Metric | Definition | Baseline | Current result | Target | Notes |
|---|---|---|---|---|---|
| Detectability | 必要Fieldが有効に取得できた割合 | | | | |
| Test success | Positive / Negative / Benign-near-miss fixtureで期待結果を再現した割合 | | | | |
| Triageability | 一次判定に必要なContextがAlertに含まれた割合または時間 | | | | |
| Decision latency contribution | Ruleが遮断 / 承認 / 監視継続の判断時間をどれだけ短縮したか | | | | |
| Precision assumption | 実環境での誤検知見積り前提 | | | | |
| Recall assumption | 重要Behavior取りこぼし見積り前提 | | | | |
| Base rate note | 低頻度環境での運用負荷前提 | | | | |

## 9. Control Improvement and Reassessment

| Control ID | Related Detection ID | Improvement | Owner | Due date | Verification method | Status |
|---|---|---|---|---|---|---|
| `CTRL-*` | | | | | | |

| Reassessment ID | Trigger | Scope to retest | Evidence to recollect | Scheduled date | Exit criteria |
|---|---|---|---|---|---|
| `REA-*` | | | | | |

## 10. Traceability Check

- Case ID:
- Related Case Map Case / Decision IDs:
- Related Case Map Detection / Fixture / Control IDs:
- Detection relationship:
- Decision Requirement ID:
- Response Objective ID:
- Threat Hypothesis IDs:
- Observation Hypothesis IDs:
- Telemetry IDs:
- Detection ID:
- Positive Fixture ID:
- Negative Fixture ID:
- Benign-near-miss Fixture ID:
- Evidence IDs:
- Triage / Incident Handoff IDs:
- Control IDs:
- Reassessment ID:
- Detection backlog input IDs:
- Source Note IDs:

## 11. Review

| Review area | Reviewer / role | Result | Date | Evidence reference | Notes |
|---|---|---|---|---|---|
| Technical correctness |  | Pass / Changes required |  |  |  |
| Safety / authorization |  | Pass / Changes required |  |  |  |
| Evidence / source quality |  | Pass / Changes required |  |  |  |
| Coverage and analytic quality |  | Pass / Changes required |  |  |  |
| Decision usefulness |  | Pass / Changes required |  |  |  |
