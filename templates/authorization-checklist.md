# Authorization Checklist

## 目的

このTemplateは、Security Assessment、OSINT、Lab、Incident調査を開始する前に、Authority、Scope、Safety、Disclosureの四つのGateを評価し、Rules of Engagementへ渡せる条件を記録するために使用する。

このTemplateは法的助言ではない。法令・契約の適用判断が必要な場合は、法務、Privacy、契約責任者、System / Data ownerへEscalateする。

## 使用条件

- 実在する第三者Targetを無断で対象にしない。
- 実Credential、Token、Cookie、Personal Data、Secret valueを記載しない。
- 不足情報を推測でPassにしない。
- 一つでもCritical gateが`Unknown`または`Fail`なら、Tool実行へ進まない。
- `Proceed with conditions`では、Condition、Owner、期限、再確認方法を必須とする。

## 0. Document Control

| Field | Value |
|---|---|
| Artifact ID | `ART-13` |
| Authorization Record ID | `AUTH-YYYY-NNN` |
| Parent Case ID | `CASE-YYYY-NNN` |
| Relation | `refines` / `supersedes` / `independent` |
| Title |  |
| Status | Draft / Review Required / Decision Recorded / Expired / Superseded / Closed |
| Owner |  |
| Decision owner |  |
| Classification | Public / Internal / Confidential / Restricted |
| Created at | ISO 8601 |
| Updated at | ISO 8601 |
| Authorization expires at | ISO 8601 |
| Related Issue / Ticket |  |

## 1. Decision Requirement

| Field | Value |
|---|---|
| Decision Requirement ID | `DR-AUTH-001` |
| Decision owner |  |
| Decision deadline |  |
| Decision to make |  |
| Available decisions | Proceed / Proceed with conditions / Do not proceed / Escalate |
| Decision criteria |  |
| Consequence of delay |  |
| Maximum acceptable uncertainty |  |

### 判断に不要な問い

- （記入）

## 2. Authority Gate

| Field | Value |
|---|---|
| Gate status | Pass / Conditional / Fail / Unknown |
| System owner |  |
| Data owner |  |
| Access administrator |  |
| Contracting party |  |
| Customer /委託者 |  |
| Subcontractor |  |
| Cloud / SaaS provider |  |
| Approver |  |
| Authority basis | Contract / Statement of Work / Policy / Delegation / Other |
| Written authorization reference |  |
| Authorized period |  |
| Withdrawal method |  |
| Third-party approval required | Yes / No / Unknown |
| Authority gaps |  |
| Gap owner / due date |  |

### Authority evidence

| Evidence ID | Description | Source / custodian | Collected at | Integrity / reference | Limitation |
|---|---|---|---|---|---|
| `EVD-AUTH-001` |  |  |  |  |  |

## 3. Scope Gate

| Field | Value |
|---|---|
| Gate status | Pass / Conditional / Fail / Unknown |
| In-scope target identifiers |  |
| Out-of-scope target identifiers |  |
| Environment | Production / Staging / Isolated Lab / Other |
| Tenant / account / role |  |
| In-scope data |  |
| Prohibited data |  |
| Allowed methods |  |
| Prohibited methods |  |
| Time window |  |
| Rate / volume / concurrency |  |
| External dependencies |  |
| Redirect / discovered asset rule | Do not follow / Reauthorize / Other |
| Scope gaps |  |
| Gap owner / due date |  |

## 4. Safety Gate

| Field | Value |
|---|---|
| Gate status | Pass / Conditional / Fail / Unknown |
| Purpose of operation |  |
| Expected evidence |  |
| Minimum sufficient evidence |  |
| Maximum acceptable impact |  |
| Stop conditions |  |
| Emergency contact |  |
| Rollback owner |  |
| Cleanup owner |  |
| Cleanup verification |  |
| Personal Data handling |  |
| Secret handling |  |
| Evidence classification |  |
| Evidence access control |  |
| Retention / disposal |  |
| Safety gaps |  |
| Gap owner / due date |  |

## 5. Disclosure Gate

| Field | Value |
|---|---|
| Gate status | Pass / Conditional / Fail / Unknown |
| Discovery owner |  |
| Product developer / site operator contact |  |
| Customer /委託者 contact |  |
| IPA / JPCERT/CC route applicable | Yes / No / Unknown |
| Coordination owner |  |
| Information sharing boundary |  |
| Publication decision owner |  |
| Embargo / non-disclosure condition |  |
| Emergency disclosure condition |  |
| Reauthorization required for additional validation | Yes / No |
| Disclosure gaps |  |
| Gap owner / due date |  |

## 6. Legal, Contractual, and Policy Questions

この節では結論を捏造しない。法務等へ確認する問いを記録する。

| Question ID | Question | Applicable source / contract | Owner | Status | Answer / limitation | Recheck trigger |
|---|---|---|---|---|---|---|
| `LQ-AUTH-001` |  |  |  | Open / Answered / Escalated / Not applicable |  |  |

## 7. Conditions

`Proceed with conditions`の場合に使用する。

| Condition ID | Condition | Reason | Owner | Due date | Verification | Status |
|---|---|---|---|---|---|---|
| `COND-AUTH-001` |  |  |  |  |  | Open / Satisfied / Waived by authorized owner / Failed |

## 8. Decision Record

| Field | Value |
|---|---|
| Authorization Decision ID | `DEC-AUTH-001` |
| Selected decision | Proceed / Proceed with conditions / Do not proceed / Escalate |
| Decision owner |  |
| Decision time |  |
| Related evidence IDs |  |
| Related condition IDs |  |
| Confirmed facts |  |
| Assumptions |  |
| Information gaps |  |
| Reasoning |  |
| Residual risk |  |
| Required approvers |  |
| Reauthorization triggers |  |

## 9. RoE Handoff

| Handoff ID | Input to RoE | Acceptance criteria | Actual status | Reject / return condition | Owner |
|---|---|---|---|---|---|
| `HO-AUTH-001` | Decision Requirement | Owner、期限、判断内容がある |  | 抽象目的のみ |  |
| `HO-AUTH-002` | Authority evidence | 承認者、根拠、期間、対象がある |  | 承認権限不明 |  |
| `HO-AUTH-003` | Target / Data scope | 技術識別子、対象外、Data境界がある |  | 外部依存・Tenant境界不明 |  |
| `HO-AUTH-004` | Method boundary | 許可・禁止、Rate、Volumeがある |  | Tool名だけで操作不明 |  |
| `HO-AUTH-005` | Safety plan | Evidence、Stop、Contact、Cleanupがある |  | Stop / Cleanup owner不在 |  |
| `HO-AUTH-006` | Disclosure route | 連絡、調整、公開判断者がある |  | 発見後の経路不明 |  |

## 10. Reassessment

| Field | Value |
|---|---|
| Reassessment ID | `REA-AUTH-001` |
| Scheduled date |  |
| Trigger conditions | Target / owner / method / data / time / provider / contract change |
| Evidence to recollect |  |
| Decision to revisit |  |
| Closure criteria |  |

## 11. Traceability Check

- [ ] Decision Requirementから四つのGateへ追跡できる
- [ ] Authority evidenceが承認対象、期間、操作へ接続している
- [ ] Target、Account、Environment、Data、対象外が技術識別子で定義されている
- [ ] Expected evidence、Stop、Emergency contact、Cleanupがある
- [ ] Personal DataとSecretの取扱条件がある
- [ ] Disclosure routeと追加検証の再承認条件がある
- [ ] `Unknown` / `Conditional`にOwnerと期限がある
- [ ] Decision RecordとRoE Handoffが一致する
- [ ] Reauthorization triggerがある

## 12. Review

| Review area | Reviewer / role | Result | Date | Evidence reference | Notes |
|---|---|---|---|---|---|
| Technical correctness |  | Pass / Changes required |  |  |  |
| Safety / authorization |  | Pass / Changes required |  |  |  |
| Legal / contractual source quality |  | Pass / Changes required |  |  |  |
| Evidence / traceability |  | Pass / Changes required |  |  |  |
| Decision usefulness |  | Pass / Changes required |  |  |  |
