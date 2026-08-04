# Web/API Assessment Hypothesis Pack

## 目的

このテンプレートは、Web ApplicationとAPIの評価を、脆弱性名やTool順ではなく、Decision Requirement、Asset、Boundary、State、Safe Validation、Evidence、Telemetry、Detection、Reassessmentの接続として記録するために使用する。

Assessment結果だけを残すのではなく、次を追跡可能にする。

- 何を判断するための評価か
- どのCase MapのDecisionへ結果を返すか
- どのAsset、Actor、Boundary、Stateを評価するか
- どのThreat Hypothesisを、どのObservationとValidationで支持または反証するか
- どこで停止し、何をCleanupするか
- どのEvidenceでFindingを書くか
- どのTelemetryとDetectionへ引き渡すか
- いつ、何を再評価するか

## 使用条件

- 実在する第三者Systemを対象にしない。
- 実Credential、Token、Cookie、個人情報を記載しない。
- `.example`、`.test`、`.invalid`および合成IDだけを使用する。
- 検証対象は、明示的に許可された自己所有環境または隔離された合成Fixtureに限定する。
- 外向き通信を必要とする操作、横展開、Credential reuse、大量Data取得、DoS相当の操作を含めない。
- Negative Testの不成立をSystem全体の安全性証明として扱わない。

## 0. Document Control

| Field | Value |
|---|---|
| Artifact ID | `ART-11` |
| Case ID | `CASE-YYYY-NNN` |
| Title |  |
| Status | Draft / Active / Validation Complete / Findings Drafted / Detection Handoff / Reassessment Due / Closed |
| Owner |  |
| Contributors |  |
| Classification | Public / Internal / Confidential / Restricted |
| Created at | ISO 8601 |
| Updated at | ISO 8601 |
| Review deadline | ISO 8601 |
| Related Issue / Ticket |  |
| Related Case Map Artifact | `ART-10` |
| Related Case Map Case ID | `CASE-YYYY-NNN` |
| Related Case Map Decision ID | `DEC-CASE-001` |

## 1. Decision Requirement and Scope

| Field | Value |
|---|---|
| Decision Requirement ID | `DR-CASE-001` |
| Decision owner |  |
| Decision deadline |  |
| Decision question |  |
| Decision options |  |
| Decision criteria |  |
| Maximum acceptable uncertainty |  |
| Consequence of delay |  |
| Authority / RoE ID | `ROE-CASE-001` |
| In-scope assets / surfaces |  |
| Out-of-scope assets / surfaces |  |
| Permitted operations |  |
| Prohibited operations |  |
| Permitted data |  |
| Test window |  |
| Stop conditions |  |
| Cleanup owner |  |

### 判断に不要な高リスク操作

今回のDecisionに不要であり、実施しない操作を列挙する。

- （記入）

## 2. Asset, Boundary, and State Context

### 2.1 Assets

| Asset ID | Service / endpoint / job | Business role | Data classification | Owner | Notes |
|---|---|---|---|---|---|
| `ASSET-CASE-001` |  |  |  |  |  |

### 2.2 Actor and Credential Classes

| Actor ID | Role / user class | Credential / session class | Intended scope | Prohibited capability | Notes |
|---|---|---|---|---|---|
| `ACT-CASE-001` |  |  |  |  |  |

### 2.3 Trust, Tenant, and Server-side Boundaries

| Boundary ID | Asset ID | Boundary type | From | To | Control | Failure consequence |
|---|---|---|---|---|---|---|
| `TB-CASE-001` | `ASSET-CASE-001` | Identity / Object / Tenant / Network / Server-side / Queue |  |  |  |  |

### 2.4 Workflow State and Business Rules

| State ID | Asset ID | Triggering action | Required actor / approval | Allowed next state | Forbidden shortcut |
|---|---|---|---|---|---|
| `STATE-CASE-001` | `ASSET-CASE-001` |  |  |  |  |

### 2.5 Inventory, Version, and Deprecation Coverage

| Surface ID | Asset ID | Path / operation / webhook / worker | Version | Discovery source | Deprecated | Security note |
|---|---|---|---|---|---|---|
| `SURF-CASE-001` | `ASSET-CASE-001` |  |  |  | Yes / No |  |

## 3. Hypothesis Register

### 3.1 Threat Hypotheses

| Threat Hypothesis ID | Asset ID | Security property | Actor / credential class | Entry point | Boundary / state | Hypothesis statement | Priority | Status |
|---|---|---|---|---|---|---|---|---|
| `TH-CASE-001` | `ASSET-CASE-001` | Authentication context / Object authz / Function authz / Property authz / State / Input handling / Server-side trust / Resource control |  |  |  | 望ましくない成立条件を書く | High / Medium / Low | Proposed / Testable / Supported / Partially supported / Weakened / Inconclusive / Rejected |

`Authentication context`は、認証後のIdentity、Tenant、Role、Credential classの束縛を指す。認証Protocol実装そのものの詳細評価は、この成果物の中心範囲に含めない。

### 3.2 Observation Hypotheses

| Observation Hypothesis ID | Related Threat Hypothesis ID | Expected authorized result | Expected denied result | Expected side effect | Disconfirming observation |
|---|---|---|---|---|---|
| `OBS-CASE-001` | `TH-CASE-001` |  |  |  |  |

### 3.3 Good / Bad Hypothesis Notes

弱い仮説を残さないため、必要に応じて修正メモを残す。

| Note ID | Before | After | Why the revision matters |
|---|---|---|---|
| `NOTE-CASE-001` |  |  |  |

## 4. Safe Validation Design

| Validation ID | Related Threat Hypothesis ID | Related Observation Hypothesis ID | Minimal authorized operation | Synthetic fixture / dataset | Expected evidence | Stop condition | Cleanup |
|---|---|---|---|---|---|---|---|
| `VAL-CASE-001` | `TH-CASE-001` | `OBS-CASE-001` |  |  |  |  |  |

### 拒否系の確認

| Validation ID | Boundary checked | Low-impact rejected input or action | Expected denied result | Permitted conclusion |
|---|---|---|---|---|
| `VAL-CASE-001` |  |  |  |  |

### 実施しない検証

影響が大きい、権限外、またはDecisionに不要なため実施しない操作を記録する。

- （記入）

## 5. Evidence Register and Findings Handoff

### 5.1 Evidence Register

| Evidence ID | Related Observation ID | Related Validation ID | Authority / RoE ID | Question supported | Source / collector | Collected at | Integrity / location | Limitation |
|---|---|---|---|---|---|---|---|---|
| `EVD-CASE-001` | `OBS-CASE-001` | `VAL-CASE-001` | `ROE-CASE-001` |  |  |  |  |  |

### 5.2 Evidence Handling

Evidenceごとに、公開・共有前の無害化と廃棄責任を定義する。

| Evidence ID | Redaction status | Classification | Access scope | Retention / disposal date | Disposal owner |
|---|---|---|---|---|---|
| `EVD-CASE-001` | Not reviewed / Redacted / No sensitive fields | Public / Internal / Confidential / Restricted |  |  |  |

### 5.3 Negative Findings

| Negative Finding ID | Related Threat Hypothesis ID | Searched behavior | Search window | Available coverage | Remaining gaps | Permitted conclusion |
|---|---|---|---|---|---|---|
| `NEG-CASE-001` | `TH-CASE-001` |  |  |  |  |  |

### 5.4 Findings and Retest Handoff

| Finding ID | Related Threat Hypothesis ID | Root condition | Evidence IDs | Related Telemetry ID | Related Detection ID / planned ID | Business impact | Required remediation | Retest acceptance criteria |
|---|---|---|---|---|---|---|---|---|
| `FIND-CASE-001` | `TH-CASE-001` |  |  | `TEL-CASE-001` | `DET-CASE-001` |  |  |  |

## 6. Telemetry and Detection Handoff

### 6.1 Required Telemetry

| Telemetry ID | Related Threat Hypothesis ID | Required event / fields | Retention | Current state | Gap owner |
|---|---|---|---|---|---|
| `TEL-CASE-001` | `TH-CASE-001` |  |  | Available / Partial / Missing |  |

### 6.2 Detection Handoff

| Detection ID | Related Threat Hypothesis ID | Related Telemetry ID | Detection hypothesis | Test fixture | Expected result | Limitations |
|---|---|---|---|---|---|---|
| `DET-CASE-001` | `TH-CASE-001` | `TEL-CASE-001` |  |  |  |  |

## 7. Reassessment Plan

| Reassessment ID | Related Decision ID | Related Finding IDs | Related Detection IDs | Trigger conditions | Hypotheses to retest | Evidence to recollect | Owner | Due date |
|---|---|---|---|---|---|---|---|---|
| `REA-CASE-001` | `DEC-CASE-001` | `FIND-CASE-001` | `DET-CASE-001` |  |  |  |  |  |

## 8. Traceability Check

- [ ] Case ID、Decision Requirement ID、関連Case MapのDecision IDが明記されている
- [ ] 各AssetにActor、Boundary、Stateの説明がある
- [ ] 各Threat HypothesisにObservation Hypothesisがある
- [ ] 各Threat HypothesisにValidation IDがある
- [ ] 各ValidationがObservation IDへ接続し、Expected evidence、Stop、Cleanupがある
- [ ] 各FindingがEvidence IDへ追跡できる
- [ ] 各FindingにTelemetry IDまたはGap ownerがある
- [ ] 各Detection IDがThreat HypothesisまたはTelemetry IDへ接続している
- [ ] Negative FindingがCoverageとGapを持つ
- [ ] EvidenceのRedaction、Classification、Access、Retention / disposal、Ownerが定義されている
- [ ] Reassessment IDがDecision IDへ接続している

## 9. Artifact Rubric

| 評価軸 | Pass条件 | よくある不足 |
|---|---|---|
| Decision alignment | Decision questionとHypothesisが直接対応している | 「何となく重要そう」な論点が混在する |
| Boundary clarity | Asset、Actor、Tenant / trust boundary、Stateが明示されている | 認証済みかどうかだけで終わる |
| Safe validation | Authority、Stop、Cleanup、最小証拠がある | 追加Data取得や高負荷が前提になる |
| Evidence quality | 支持・反証条件、時刻、制約がある | 403 / 404だけで結論する |
| Detection handoff | Telemetry field、Detection hypothesis、Gap ownerがある | 「監視強化する」で終わる |
| Reassessment | TriggerとRetest対象がある | 修正後確認の条件がない |

## 10. Delegated Reading

詳細手順や実装詳細は、このテンプレートへコピーせず、必要に応じて次を参照する。

- [Web脆弱性の整理](https://itdojp.github.io/pentest-learning-book/part2_web/24_common_web_vulnerabilities/)
- [APIの基礎とアタックサーフェス](https://itdojp.github.io/pentest-learning-book/part4_api/41_api_basics_and_attack_surface/)
- [典型的なAPI脆弱性](https://itdojp.github.io/pentest-learning-book/part4_api/42_common_api_vulnerabilities/)
- [OAuth 2.0 / OIDCの評価観点](https://itdojp.github.io/pentest-learning-book/part4_api/43_oauth_oidc_testing/)
- [RBAC / ABACの誤実装パターン](https://itdojp.github.io/pentest-learning-book/part4_api/44_rbac_abac_misconfig/)
- [認証・認可プロトコルの設計詳細](https://itdojp.github.io/practical-auth-book/)

## 11. Review

| Review area | Reviewer / role | Result | Date | Evidence reference | Notes |
|---|---|---|---|---|---|
| Technical correctness |  | Pass / Changes required |  |  |  |
| Safety / authorization |  | Pass / Changes required |  |  |  |
| Evidence / source quality |  | Pass / Changes required |  |  |  |
| Detection handoff |  | Pass / Changes required |  |  |  |
| Decision usefulness |  | Pass / Changes required |  |  |  |
