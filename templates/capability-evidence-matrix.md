# Capability Evidence Matrix

## 目的

このTemplateは、Work RoleまたはResponsibilityをTaskへ分解し、Knowledge / Skill、許可されたPractice、Artifact Evidence、Review、Gap、Learning Action、Reassessmentを直接追跡するために使用する。

このTemplateは、人事評価、採用、昇進、報酬、資格認定、公開ランキングには使用しない。Capability Judgmentは、明示したScopeとConditionsにおける限定的な結論であり、人物全体の能力を示すものではない。

## 使用条件

- Practiceは、完全合成環境または明示的に許可された隔離環境だけで行う。
- 実在Targetへの攻撃、実Credential、Token、Cookie、個人情報、従業員Data、顧客DataをEvidenceにしない。
- 攻撃活動の量、取得Account数、Tool数をCapability metricにしない。
- RubricとReviewer roleは、Evidenceを評価する前に定義する。
- Resultが不明な場合は`Inconclusive`とし、推測で`Complete`にしない。

## 0. Document Control

| Field | Value |
|---|---|
| Artifact ID | `ART-14` |
| Matrix ID | `CAP-MATRIX-YYYY-NNN` |
| Learner Profile ID | `SYNTH-LEARNER-NNN` |
| Parent Artifact ID | `ART-01` |
| Relation | `refines` / `supersedes` / `independent` |
| Title |  |
| NICE structural publication | `NIST SP 800-181 Rev.1` |
| NICE Components baseline | `v2.2.0` |
| Status | Planned / In practice / Evidence submitted / Reviewed / Gap identified / Reassessment due / Complete |
| Owner |  |
| Classification | Public / Internal / Confidential / Restricted |
| Created at | ISO 8601 |
| Updated at | ISO 8601 |

## 1. Capability Claim Boundary

| Field | Value |
|---|---|
| Capability Claim ID | `CAP-CLAIM-YYYY-NNN` |
| Scope | 対象Task、対象外、Components版 |
| Conditions | Authority、Practice Environment、入力、利用可能な支援 |
| Evidence set | 複数のArtifact / Evidence ID |
| Reviewer | Role、独立性、必要な専門性 |
| Rubric | 宣言済み評価基準 |
| Result | Supported / Partially supported / Not supported / Inconclusive |
| Limitations | 未観測、未実施、一般化できない範囲 |
| Expiry | ISO 8601 |
| Reassessment Trigger | 時間 / Scope / Source / Role / Technology / Rubricの変更 |

## 2. Work Decomposition

Work Roleは仕事のGroupingであり、Job titleまたは個人ではない。Competency AreaはNICE ComponentsのGroupingであり、個人能力の証明ではない。

| Entry ID | Work Role / Responsibility | Task ID / statement | Knowledge reference | Skill reference |
|---|---|---|---|---|
| `CAP-ENTRY-001` |  | `TASK-CAP-001`:  | `KN-CAP-001` | `SK-CAP-001` |

## 3. Practice and Evidence Trace

| Entry ID | Practice ID | Authority / Environment | Artifact / Evidence ID | Reviewer | Rubric | Result | Status | Limitations | Reassessment ID |
|---|---|---|---|---|---|---|---|---|---|
| `CAP-ENTRY-001` | `PRACTICE-CAP-001` |  | `ART-EVD-CAP-001` |  | `RUBRIC-CAP-001` |  | Planned |  | `REA-CAP-001` |

許容するStatusは次の有限集合だけである。

```text
Planned / In practice / Evidence submitted / Reviewed / Gap identified / Reassessment due / Complete
```

StatusはEvidence lifecycle上の位置を示し、Capabilityの高さを示さない。

## 4. Gap and Learning Action

| Entry ID | Gap | Learning Action | Owner | Due date | Expected next evidence |
|---|---|---|---|---|---|
| `CAP-ENTRY-001` |  |  |  | ISO 8601 |  |

## 5. Review Result

Review Resultは、対象Artifact一つをRubricで評価した結果である。Capability Judgmentと混在させない。

| Review ID | Artifact / Evidence ID | Artifact version | Reviewer / role | Rubric | Result | Reviewed at | Findings | Disposition |
|---|---|---|---|---|---|---|---|---|
| `REV-CAP-001` | `ART-EVD-CAP-001` |  |  | `RUBRIC-CAP-001` | Meets / Partially meets / Does not meet / Inconclusive | ISO 8601 |  |  |

## 6. Bounded Capability Judgment

Capability Judgmentは、一つのReview Resultではなく、複数Evidence itemを対象にする。

| Claim ID | Scope | Conditions | Evidence set | Reviewer | Result | Limitations | Expiry | Trigger | Reassessment ID |
|---|---|---|---|---|---|---|---|---|---|
| `CAP-CLAIM-YYYY-NNN` |  |  |  |  | Supported / Partially supported / Not supported / Inconclusive |  | ISO 8601 |  | `REA-CAP-001` |

## 7. Reassessment

| Reassessment ID | Scheduled date | Trigger | Evidence to recollect | Task to revisit | Owner | Closure criteria | Status |
|---|---|---|---|---|---|---|---|
| `REA-CAP-001` | ISO 8601 |  |  | `TASK-CAP-001` |  |  | Planned / Reassessment due / Complete |

## 8. Traceability Check

- [ ] `ART-01`の学習GoalからTaskへ追跡できる
- [ ] TaskにKnowledge / Skill referenceがある
- [ ] PracticeのAuthorityとEnvironmentが明示されている
- [ ] TaskからArtifact / Evidence IDへ追跡できる
- [ ] Reviewer roleとRubricがEvidence評価前に定義されている
- [ ] Review ResultとCapability Judgmentを分離している
- [ ] Capability Judgmentが複数Evidenceに支えられている
- [ ] Scope、Conditions、Limitations、Expiry、Reassessment Triggerがある
- [ ] GapにLearning Action、Owner、Due dateがある
- [ ] 実Target、実Secret、個人・従業員・顧客Data、公開ランキングを使用していない

## 9. Review

| Review area | Reviewer / role | Result | Date | Evidence reference | Notes |
|---|---|---|---|---|---|
| Technical correctness |  | Pass / Changes required |  |  |  |
| Safety / authorization |  | Pass / Changes required |  |  |  |
| Source quality / freshness |  | Pass / Changes required |  |  |  |
| Evidence / traceability |  | Pass / Changes required |  |  |  |
| Decision usefulness |  | Pass / Changes required |  |  |  |
