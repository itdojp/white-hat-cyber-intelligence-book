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

### Parent ART-01 Learning Route Plan instance

この合成Caseがrefineする親Planは次の実体である。Job titleや配置判定ではなく、学習TaskとEvidenceを選ぶためのPlanである。

| Learning Route Plan field | Value |
|---|---|
| Artifact ID | `ART-01` |
| Plan ID | `LRP-2026-003` |
| Learner Profile ID | `SYNTH-LEARNER-003` |
| 現在の役割 | 合成学習者。実在の従業員・応募者ではない |
| 目標とするResponsibility | 許可判断支援、offline detection検証、Source評価済み分析判断を、安全境界内で説明する |
| 判断・業務上の目的 | 三Taskの学習優先度と再評価条件を決める。採用・配置・報酬判断には使わない |
| 6か月後の成果物 | `ART-14`と`ART-EVD-CAP-001`〜`003`のReview済み版 |
| 強い前提知識 | 合成Scenarioの読解、表形式Evidenceの記録 |
| 補強が必要な前提知識 | Authority gate、fixture比較、Source lineage |
| 最初に読む章 | 第1章、第2章、第3章 |
| 委譲先の専門書 | Chapter 3のDELEGATE先をTaskごとに使用 |
| 使用する隔離ラボ | `CAP-PACKET-2026-003-R1`。外部Networkなし |
| 禁止する対象・操作 | 実Target、実Secret、個人・従業員・顧客Data、攻撃活動量による評価 |
| 月次レビュー日 | 2026-09-05、2026-10-05、2026-11-05 |
| 学習の証拠 | `ART-EVD-CAP-001`、`ART-EVD-CAP-002`、`ART-EVD-CAP-003` |

## 0. Document Control

| Field | Value |
|---|---|
| Artifact ID | `ART-14` |
| Matrix ID | `CAP-MATRIX-2026-003` |
| Learner Profile ID | `SYNTH-LEARNER-003` |
| Parent Artifact ID | `ART-01` |
| Parent Plan ID | `LRP-2026-003` |
| Relation | `refines` |
| Case ID | `LEARN-CASE-2026-003` |
| Title | Authority、Detection、分析判断のEvidenceを作る合成学習計画 |
| NICE structural publication | `NIST SP 800-181 Rev.1` |
| NICE Components baseline | `v2.2.0` |
| Practice packet | `CAP-PACKET-2026-003-R1` |
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

| Entry ID | Work Role / Responsibility | Task ID / statement | Knowledge reference | Skill reference | NICE Components references（optional） |
|---|---|---|---|---|---|
| `CAP-ENTRY-001` | Security engagementの開始判断を支援する | `TASK-CAP-001`: 合成ScenarioからAuthorization Checklistを作り、停止・Escalation条件を説明する | `KN-CAP-001`: Authority / Scope / Safety / Disclosure | `SK-CAP-001`: 不足条件をGate decisionへ変換する | `v2.2.0`; Not mapped。合成の横断Taskであり、対応identifierを確認していない |
| `CAP-ENTRY-002` | Detection logicの検証可能性を確認する | `TASK-CAP-002`: 本Caseのoffline fixtureを期待結果と照合し、Coverageと限界を記録する | `KN-CAP-002`: Telemetry、fixture、negative finding | `SK-CAP-002`: replay結果を期待値と比較する | `v2.2.0`; Not mapped。学習用Taskを特定Work Roleへ固定しない |
| `CAP-ENTRY-003` | Source評価済みの分析判断を作る | `TASK-CAP-003`: 本Caseの合成Source packetの来歴と独立性を評価し、限定Judgmentを作る | `KN-CAP-003`: Reliability、Credibility、Independence | `SK-CAP-003`: Fact、Assumption、Judgmentを分離する | `v2.2.0`; Not mapped。Components identifierへの対応を推測しない |

Work Role / ResponsibilityはTaskを整理する入口であり、合成学習者のJob titleまたは人物像ではない。Knowledge / Skill referenceは本Case内の識別子であり、NICE identifierとの同一性を主張しない。

三つのTaskはComponents identifierとの意味的対応を確認していないため、推測で割り当てない。一方、確認済みidentifierの記入形式例は`v2.2.0; Work Role OG-WRL-017; local Task / K / S: Not mapped（当該Taskとの対応未確認）`である。これはComponents上のWork Role存在確認を示すだけで、本CaseのTaskやCapability Claimを`OG-WRL-017`へ対応付けない。

### 2.1 完全合成Practice packet

この節だけで三つのTaskを再現できる。第17章または第25章の読了、外部Network、別Datasetを前提にしない。

この節のScenario、Checklist stub、Fixture表、Source Packet表、判定Ruleを、正本Practice packet `CAP-PACKET-2026-003-R1`とする。R1の入力はこの文書内の表そのものであり、外部fileを必要としない。入力またはRuleを変更する場合はpacket版を上げ、旧Review Resultを流用せずReassessmentを行う。

#### Authorization Scenario

- System ownerとData ownerは合成人物Roleとして定義済みである。
- 許可対象は隔離済みの合成Tenant設定Exportだけである。
- 許可期間は2026-08-05T09:00:00+09:00から17:00:00+09:00までである。
- Data scope、外部接続禁止、停止、Cleanupは定義済みだが、Target、Data、期間変更時の再承認Triggerが未記入である。

#### Minimum Authorization Checklist stub

Task 1では次の最小stubを使う。第2章の完全なTemplateを参照しなくても、四Gate、停止、Escalation、再承認のEvidenceを作成できる。

| Gate / control | Required record |
|---|---|
| Authority | 承認主体、実施主体、根拠、承認状態 |
| Scope | 対象、対象外、Data、期間、許可Action |
| Safety | 隔離、Rate / load制約、停止条件、Cleanup |
| Disclosure | 連絡先、Evidence取扱い、報告先、開示境界 |
| Stop / Escalation | 誰が、何を検出したら、誰へ引き渡すか |
| Reauthorization | Target、Data、期間、手法、Owner変更時の再承認条件 |

#### Offline Detection Fixture

R1 detector contractは「`operation=admin_change`かつ`actor_authorized=false`かつ`required_fields=complete`なら`Alert`、それ以外は`No alert`」である。各行へこのRuleを適用し、ObservedとExpectedが一致するかをofflineで確認する。

| Fixture ID | Input | Expected observation | Observed in R1 | Coverage limitation |
|---|---|---|---|---|
| `FIX-CAP-002-POS` | `operation=admin_change`, `actor_authorized=false`, `required_fields=complete` | Alert | Alert | 一つのEvent schemaだけを確認 |
| `FIX-CAP-002-NEG` | `operation=admin_change`, `actor_authorized=true`, `required_fields=complete` | No alert | No alert | 許可Listの鮮度は未評価 |
| `FIX-CAP-002-BENIGN` | `operation=view`, `actor_authorized=false`, `required_fields=complete` | No alert | No alert | 類似する別操作は未評価 |

#### Synthetic Source Packet

| Source Note ID | Statement | Lineage | Independence |
|---|---|---|---|
| `SN-CAP-003-A` | 合成技術Cluster `CL-CAP-003`の同一特徴を報告 | 合成一次観測 | Group A |
| `SN-CAP-003-B` | `SN-CAP-003-A`を要約して同じ特徴を報告 | derived-from `SN-CAP-003-A` | Group A |
| `SN-CAP-003-C` | 反対仮説に整合する別特徴を報告 | 合成一次観測だが対象期間外 | Group B / scope mismatch |

`SN-CAP-003-A`と`SN-CAP-003-B`を独立した二件に数えない。`SN-CAP-003-C`は対象期間外であるため、現在の問いを独立に裏付けない。したがって現時点のResultは`Inconclusive`である。

R1 source-evaluation contractは「同じLineage groupの派生Sourceを独立件数へ重複加算せず、対象期間外のSourceを現在の問いの支持・反証へ使わない。独立したin-scope Sourceが二系統未満なら`Inconclusive`」である。

#### R1 replay procedure

1. `CAP-PACKET-2026-003-R1`の表を変更せず入力として使う。
2. Task 1は最小Checklist stubへScenarioを転記し、空欄の再承認条件をGapとして残す。
3. Task 2はdetector contractを三Fixtureへ順に適用し、ExpectedとObservedを比較する。
4. Task 3はsource-evaluation contractを三Sourceへ適用し、Lineage、期間、独立系統数を記録する。
5. Packet ID、Artifact版、Rubric、Reviewer、Result、Limitationsを`ART-14`へ記録する。

#### Artifact Evidence Rubric

| Rubric ID | Applies to | Meets | Partially meets | Does not meet | Inconclusive |
|---|---|---|---|---|---|
| `RUBRIC-CAP-001` | `TASK-CAP-001` / `ART-EVD-CAP-001` | 四Gate、停止、再承認Triggerが再現可能 | 四Gateと停止は分離したが、再承認Triggerの一部が不足 | Authority、Scope、停止条件のいずれかを無視し、安全に開始判断できない | Authority根拠またはScopeが確認不能 |
| `RUBRIC-CAP-002` | `TASK-CAP-002` / `ART-EVD-CAP-002` | 三Fixtureが期待結果と一致し、Coverage limitationを説明 | 一部結果または限界説明が不足 | 期待結果と実測が矛盾するか、offline replayを実施していない | Fixture版、期待結果、必須Fieldが不明 |
| `RUBRIC-CAP-003` | `TASK-CAP-003` / `ART-EVD-CAP-003` | 独立Sourceと反対仮説を評価し限定判断を作成 | 判断は限定したが、結論を反転させない来歴情報が不足 | Fact、Assumption、Judgmentを混在させるか、Source lineageを無視する | 独立Sourceがなく、現在の問いを支持・反証できない |

#### Capability Claim Rubric

| Rubric ID | Applies to | Supported | Partially supported | Not supported | Inconclusive |
|---|---|---|---|---|---|
| `RUBRIC-CAP-CLAIM-003` | `CAP-CLAIM-2026-003` | 三TaskがすべてMeetsで、宣言ScopeとLimitationsが矛盾しない | 複数EvidenceをReview済みで、未達または結論不能をLimitations、Gap、Reassessmentへ閉じている | 一つ以上のTaskがDoes not meet、またはEvidence setが宣言Scopeを支持しない | 必須EvidenceまたはReview Resultが不足・矛盾し、限定結論も作れない |

## 3. Practice and Evidence Trace

| Entry ID | Practice ID | Authority / Environment | Artifact / Evidence ID | Reviewer | Rubric | Result | Status | Limitations | Reassessment ID |
|---|---|---|---|---|---|---|---|---|---|
| `CAP-ENTRY-001` | `PRACTICE-CAP-001` | 合成Scenario。外部接続と実Target操作なし | `ART-EVD-CAP-001` | Synthetic Safety Reviewer | `RUBRIC-CAP-001` | Partially meets | Gap identified | 法的助言の正しさと実案件のAuthorityは評価対象外 | `REA-CAP-001` |
| `CAP-ENTRY-002` | `PRACTICE-CAP-002` | `CAP-PACKET-2026-003-R1`のoffline fixture。Network accessなし | `ART-EVD-CAP-002` | Synthetic Detection Reviewer | `RUBRIC-CAP-002` | Meets | Reviewed | Product固有設定、Production scale、未知Telemetryは未評価 | `REA-CAP-002` |
| `CAP-ENTRY-003` | `PRACTICE-CAP-003` | `CAP-PACKET-2026-003-R1`の合成Source packet。追加収集なし | `ART-EVD-CAP-003` | Synthetic Analytic Reviewer | `RUBRIC-CAP-003` | Inconclusive | Reassessment due | 独立Sourceが一系統不足し、帰属判断は対象外 | `REA-CAP-003` |

Statusは`Planned / In practice / Evidence submitted / Reviewed / Gap identified / Reassessment due / Complete`の有限集合から選んでいる。`Reviewed`はTask 2のEvidence lifecycleを示すだけで、人物全体のCapabilityがCompleteであることを意味しない。

## 4. Gap and Learning Action

| Entry ID | Gap | Learning Action | Owner | Due date | Expected next evidence |
|---|---|---|---|---|---|
| `CAP-ENTRY-001` | 条件付き許可の再承認Triggerが曖昧 | 本節の最小Checklist stubでTarget、Data、期間変更のTriggerを書き直す | Synthetic Learning Owner | 2026-08-12 | `ART-EVD-CAP-001-R2` |
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

| Claim ID | Scope | Conditions | Evidence set | Reviewer / Rubric | Result | Limitations | Expiry | Reassessment Trigger | Reassessment ID |
|---|---|---|---|---|---|---|---|---|---|
| `CAP-CLAIM-2026-003` | Task 2のoffline detection fixture検証、およびTask 1 / 3の未達・結論不能の識別と再評価設計 | 合成資料、offline fixture、v2.2.0、宣言済みRubric | `ART-EVD-CAP-001`, `ART-EVD-CAP-002`, `ART-EVD-CAP-003` | Synthetic Capability Panel / `RUBRIC-CAP-CLAIM-003` | Partially supported | Task 1は条件不足、Task 3は結論不能。実案件と人物評価へ一般化しない | 2026-11-05T17:00:00+09:00 | Components、Scope、Role、Rubric、期限の変更 | `REA-CAP-CLAIM-003` |

判断根拠は、Task 2が`Meets`、Task 1が`Partially meets`、Task 3が`Inconclusive`であることによる。資格、CTF得点、Tool数、章完了はこの結論のEvidence setに含めていない。

## 7. Reassessment

| Reassessment ID | Scheduled date | Reassessment Trigger | Evidence to recollect | Task to revisit | Owner | Closure criteria | Status |
|---|---|---|---|---|---|---|---|
| `REA-CAP-001` | 2026-08-13 | 再承認Triggerの修正完了 | `ART-EVD-CAP-001-R2` | `TASK-CAP-001` | Synthetic Safety Reviewer | Scope変更時の停止・再承認が一意 | Planned |
| `REA-CAP-002` | 2026-08-20 | benign fixture追加 | `ART-EVD-CAP-002-R2` | `TASK-CAP-002` | Synthetic Detection Reviewer | 期待検知と非検知限界を再現可能 | Planned |
| `REA-CAP-003` | 2026-08-27 | 独立合成Source追加 | `ART-EVD-CAP-003-R2` | `TASK-CAP-003` | Synthetic Analytic Reviewer | 来歴と独立性を分離して再判定 | Reassessment due |
| `REA-CAP-CLAIM-003` | 2026-11-05 | 最短の個別再評価またはCapability expiry | R2 Evidence一式 | `TASK-CAP-001` / `TASK-CAP-002` / `TASK-CAP-003` | Synthetic Capability Panel | Scope、Limitations、Expiryを含む新しい限定結論 | Planned |

## 8. Traceability Check

- [x] `ART-01`の合成学習Goalから三つのTaskへ追跡できる
- [x] `LRP-2026-003`でrefine対象のLearning Route Plan instanceを特定できる
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
