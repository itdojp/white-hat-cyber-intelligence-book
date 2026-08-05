# 第3章 合成記入例：Capability Evidence Matrix

## この記入例の扱い

この文書は、`ART-01 Learning Route Plan`を`ART-14 Capability Evidence Matrix`へ具体化するための、完全に独立した合成学習Caseである。

- Learner Profile、Reviewer、日付、Task、Resultはすべて架空である。
- 実在する従業員、応募者、顧客、組織の人事評価ではない。
- 公開ランキング、採用、昇進、報酬、資格認定には使用しない。
- Practiceは合成ScenarioとRepository提供のoffline fixtureだけを使う。
- 実Target、実Credential、Token、Cookie、個人情報、従業員Data、顧客Dataを使用しない。
- 攻撃活動の量をCapability metricにしない。

参照する空Templateは[Capability Evidence Matrix](../templates/capability-evidence-matrix.md)である。

## 0. Document Control

| Field | Value |
|---|---|
| Artifact ID | `ART-14` |
| Matrix ID | `CAP-MATRIX-2026-003` |
| Learner Profile ID | `SYNTH-LEARNER-003` |
| Parent Artifact ID | `ART-01` |
| Relation | `refines` |
| Case ID | `LEARN-CASE-2026-003` |
| Title | Authority、Detection、分析判断のEvidenceを作る合成学習計画 |
| NICE structural publication | `NIST SP 800-181 Rev.1` |
| NICE Components baseline | `v2.2.0` |
| Status | Gap identified |
| Owner | Synthetic Learning Owner |
| Classification | Public |
| Created at | 2026-08-05T09:00:00+09:00 |
| Updated at | 2026-08-05T16:00:00+09:00 |

## 1. Capability Claim Boundary

| Field | Value |
|---|---|
| Capability Claim ID | `CAP-CLAIM-2026-003` |
| Scope | 合成ScenarioでTask 2のoffline detection fixtureをRubricどおり検証できる。Task 1は一部条件を満たし、Task 3は結論不能であることを識別し、両者のGapと再評価を説明できる |
| Conditions | 完全合成資料、Repository提供fixture、Components v2.2.0、Reviewerからの一回の質問機会 |
| Evidence set | `ART-EVD-CAP-001`, `ART-EVD-CAP-002`, `ART-EVD-CAP-003` |
| Reviewer | Synthetic Capability Panel。各Task reviewerとは別の統合Review role |
| Rubric | `RUBRIC-CAP-CLAIM-003` |
| Result | Partially supported |
| Limitations | 実案件の法的判断、実Target操作、製品固有Detection実装、人物・組織への帰属は未評価 |
| Expiry | 2026-11-05T17:00:00+09:00 |
| Reassessment Trigger | NICE Components版、Practice Scope、Reviewer rubric、担当Responsibilityの変更、または期限到来 |

このCapability Judgmentは三つのEvidenceを統合した限定結論である。人物全体の能力、実案件への無条件な配置可否、普遍的な熟達度を示さない。

## 2. Work Decomposition

| Entry ID | Work Role / Responsibility | Task ID / statement | Knowledge reference | Skill reference |
|---|---|---|---|---|
| `CAP-ENTRY-001` | Security engagementの開始判断を支援する | `TASK-CAP-001`: 合成ScenarioからAuthorization Checklistを作り、停止・Escalation条件を説明する | `KN-CAP-001`: Authority / Scope / Safety / Disclosure | `SK-CAP-001`: 不足条件をGate decisionへ変換する |
| `CAP-ENTRY-002` | Detection logicの検証可能性を確認する | `TASK-CAP-002`: Repositoryのoffline fixtureを期待結果と照合し、Coverageと限界を記録する | `KN-CAP-002`: Telemetry、fixture、negative finding | `SK-CAP-002`: replay結果を期待値と比較する |
| `CAP-ENTRY-003` | Source評価済みの分析判断を作る | `TASK-CAP-003`: 合成Sourceの来歴と独立性を評価し、限定Judgmentを作る | `KN-CAP-003`: Reliability、Credibility、Independence | `SK-CAP-003`: Fact、Assumption、Judgmentを分離する |

Work Role / ResponsibilityはTaskを整理する入口であり、合成学習者のJob titleまたは人物像ではない。Knowledge / Skill referenceは本Case内の識別子であり、NICE identifierとの同一性を主張しない。

## 3. Practice and Evidence Trace

| Entry ID | Practice ID | Authority / Environment | Artifact / Evidence ID | Reviewer | Rubric | Result | Status | Limitations | Reassessment ID |
|---|---|---|---|---|---|---|---|---|---|
| `CAP-ENTRY-001` | `PRACTICE-CAP-001` | 合成Scenario。外部接続と実Target操作なし | `ART-EVD-CAP-001` | Synthetic Safety Reviewer | `RUBRIC-CAP-001` | Partially meets | Gap identified | 法的助言の正しさと実案件のAuthorityは評価対象外 | `REA-CAP-001` |
| `CAP-ENTRY-002` | `PRACTICE-CAP-002` | Repository提供offline fixture。Network accessなし | `ART-EVD-CAP-002` | Synthetic Detection Reviewer | `RUBRIC-CAP-002` | Meets | Reviewed | Product固有設定、Production scale、未知Telemetryは未評価 | `REA-CAP-002` |
| `CAP-ENTRY-003` | `PRACTICE-CAP-003` | 第25章の完全合成Source / dataset。追加収集なし | `ART-EVD-CAP-003` | Synthetic Analytic Reviewer | `RUBRIC-CAP-003` | Inconclusive | Reassessment due | 独立Sourceが一系統不足し、帰属判断は対象外 | `REA-CAP-003` |

Statusは`Planned / In practice / Evidence submitted / Reviewed / Gap identified / Reassessment due / Complete`の有限集合から選んでいる。`Reviewed`はTask 2のEvidence lifecycleを示すだけで、人物全体のCapabilityがCompleteであることを意味しない。

## 4. Gap and Learning Action

| Entry ID | Gap | Learning Action | Owner | Due date | Expected next evidence |
|---|---|---|---|---|---|
| `CAP-ENTRY-001` | 条件付き許可の再承認Triggerが曖昧 | 第2章TemplateでTarget、Data、期間変更のTriggerを書き直す | Synthetic Learning Owner | 2026-08-12 | `ART-EVD-CAP-001-R2` |
| `CAP-ENTRY-002` | benign near-missに対する説明が一例のみ | 既存fixtureの追加benign recordをofflineで再評価する | Synthetic Learning Owner | 2026-08-19 | `ART-EVD-CAP-002-R2` |
| `CAP-ENTRY-003` | Source independenceを支える別系統が不足 | 既存の合成資料から来歴が独立したSource noteを追加する | Synthetic Learning Owner | 2026-08-26 | `ART-EVD-CAP-003-R2` |

Learning Actionは、実Target調査、実Credential取得、第三者Data収集を要求しない。不足Evidenceを安全な合成入力で作れない場合は、Task Scopeを縮小する。

## 5. Review Result

| Review ID | Artifact / Evidence ID | Artifact version | Reviewer / role | Rubric | Result | Reviewed at | Findings | Disposition |
|---|---|---|---|---|---|---|---|---|
| `REV-CAP-001` | `ART-EVD-CAP-001` | R1 | Synthetic Safety Reviewer | `RUBRIC-CAP-001` | Partially meets | 2026-08-05T13:00:00+09:00 | 四Gateは分離したが再承認Triggerが不足 | GapとしてR2を要求 |
| `REV-CAP-002` | `ART-EVD-CAP-002` | R1 | Synthetic Detection Reviewer | `RUBRIC-CAP-002` | Meets | 2026-08-05T14:00:00+09:00 | 期待検知とnegative findingの限界を再現可能 | 制限付きでEvidence setへ採用 |
| `REV-CAP-003` | `ART-EVD-CAP-003` | R1 | Synthetic Analytic Reviewer | `RUBRIC-CAP-003` | Inconclusive | 2026-08-05T15:00:00+09:00 | Source independence不足 | 追加合成Source後に再評価 |

Rubricの判定軸はTask開始前に固定した。結果に合わせた基準変更は行っていない。

## 6. Bounded Capability Judgment

| Claim ID | Scope | Conditions | Evidence set | Reviewer | Result | Limitations | Expiry | Trigger | Reassessment ID |
|---|---|---|---|---|---|---|---|---|---|
| `CAP-CLAIM-2026-003` | Task 2のoffline detection fixture検証、およびTask 1 / 3の未達・結論不能の識別と再評価設計 | 合成資料、offline fixture、v2.2.0、宣言済みRubric | `ART-EVD-CAP-001`, `ART-EVD-CAP-002`, `ART-EVD-CAP-003` | Synthetic Capability Panel | Partially supported | Task 1は条件不足、Task 3は結論不能。実案件と人物評価へ一般化しない | 2026-11-05T17:00:00+09:00 | Components、Scope、Role、Rubric、期限の変更 | `REA-CAP-CLAIM-003` |

判断根拠は、Task 2が`Meets`、Task 1が`Partially meets`、Task 3が`Inconclusive`であることによる。資格、CTF得点、Tool数、章完了はこの結論のEvidence setに含めていない。

## 7. Reassessment

| Reassessment ID | Scheduled date | Trigger | Evidence to recollect | Task to revisit | Owner | Closure criteria | Status |
|---|---|---|---|---|---|---|---|
| `REA-CAP-001` | 2026-08-13 | 再承認Triggerの修正完了 | `ART-EVD-CAP-001-R2` | `TASK-CAP-001` | Synthetic Safety Reviewer | Scope変更時の停止・再承認が一意 | Planned |
| `REA-CAP-002` | 2026-08-20 | benign fixture追加 | `ART-EVD-CAP-002-R2` | `TASK-CAP-002` | Synthetic Detection Reviewer | 期待検知と非検知限界を再現可能 | Planned |
| `REA-CAP-003` | 2026-08-27 | 独立合成Source追加 | `ART-EVD-CAP-003-R2` | `TASK-CAP-003` | Synthetic Analytic Reviewer | 来歴と独立性を分離して再判定 | Reassessment due |
| `REA-CAP-CLAIM-003` | 2026-11-05 | 最短の個別再評価またはCapability expiry | R2 Evidence一式 | `TASK-CAP-001` / `TASK-CAP-002` / `TASK-CAP-003` | Synthetic Capability Panel | Scope、Limitations、Expiryを含む新しい限定結論 | Planned |

## 8. Traceability Check

- [x] `ART-01`の合成学習Goalから三つのTaskへ追跡できる
- [x] 各TaskにKnowledge / Skill referenceがある
- [x] PracticeのAuthorityとEnvironmentを明示している
- [x] 各TaskからArtifact / Evidence IDへ追跡できる
- [x] Reviewer roleとRubricをResultより先に定義している
- [x] Review ResultとCapability Judgmentを分離している
- [x] Capability Judgmentが三つのEvidenceに支えられている
- [x] Scope、Conditions、Limitations、Expiry、Reassessment Triggerがある
- [x] GapにLearning Action、Owner、Due dateがある
- [x] 実Target、実Secret、個人・従業員・顧客Data、公開ランキングを使用していない

## 9. Review

以下は合成Case内のReview記入例であり、実際の章Gate、人事評価、Repository merge承認の証跡ではない。Evidence referenceも合成IDである。

| Review area | Reviewer / role | Result | Date | Evidence reference | Notes |
|---|---|---|---|---|---|
| Technical correctness | Synthetic technical reviewer | Pass | 2026-08-05 | `SYNTH-REV-CAP-TECH-001` | 用語とTask traceを確認 |
| Safety / authorization | Synthetic safety reviewer | Pass | 2026-08-05 | `SYNTH-REV-CAP-SAFE-001` | 合成・offline条件と停止条件を確認 |
| Source quality / freshness | Synthetic source reviewer | Pass | 2026-08-05 | `SYNTH-REV-CAP-SOURCE-001` | NICE structural publicationとComponents版を分離 |
| Evidence / traceability | Synthetic trace reviewer | Pass | 2026-08-05 | `SYNTH-REV-CAP-TRACE-001` | Taskから再評価までのIDを確認 |
| Decision usefulness | Synthetic decision reviewer | Pass | 2026-08-05 | `SYNTH-REV-CAP-DEC-001` | 限定結論、限界、期限を確認 |
