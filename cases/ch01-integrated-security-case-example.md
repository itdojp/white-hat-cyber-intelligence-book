# 第1章 合成記入例：請求書連携OAuthアプリの権限見直し

## この記入例の扱い

この文書は、`Integrated Security Case Map`の記入方法を示すための完全な合成例である。

- 組織名、担当者、サービス、ログ、判断はすべて架空である。
- Domainは予約済みの`.example`を使用する。
- 実Credential、Token、Cookie、個人情報、第三者システムは使用しない。
- 技術的成立性を示すための侵害手順は記載しない。
- Actorや国家への帰属は行わない。

参照する空テンプレートは[Integrated Security Case Map](../templates/integrated-security-case-map.md)である。

## 0. Document Control

| Field | Value |
|---|---|
| Artifact ID | `ART-10` |
| Case ID | `CASE-2026-001` |
| Title | 請求書連携OAuthアプリの権限見直し |
| Status | Reassessment Due |
| Owner | Security Program Lead |
| Contributors | Platform、SOC、CSIRT、CTI、業務システム担当 |
| Classification | Internal |
| Created at | 2026-07-20T09:00:00+09:00 |
| Updated at | 2026-07-30T18:00:00+09:00 |
| Review deadline | 2026-08-21T17:00:00+09:00 |
| Related Issue / Ticket | `SYNTH-SEC-1042` |

## 1. Decision Requirement

| Field | Value |
|---|---|
| Decision Requirement ID | `DR-2026-001` |
| Decision owner | CTO |
| Decision deadline | 2026-07-22T18:00:00+09:00 |
| Decision to make | 請求書連携OAuthアプリを即時停止するか、権限縮小と監視強化で継続するか |
| Available options | 即時停止 / 権限縮小して継続 / 現状維持 |
| Decision criteria | 顧客業務影響、権限範囲、既存Tokenの扱い、観測可能性、代替手段 |
| Maximum acceptable uncertainty | Token利用の完全な過去追跡はできなくても、現在の権限・同意・Credential状態を確認できること |
| Consequence of delay | 過大権限を持つ連携が継続し、問題発生時の影響範囲と調査不能範囲が残る |
| Required approvers | CTO、業務システム責任者、Security Program Lead |

### 判断に不要な問い

今回の48時間以内の判断には、次を必須としない。

- 外部報告で言及された攻撃主体の帰属
- 他社で発生した個別侵害の完全な再現
- 未公開の攻撃コードやCredentialの収集

## 2. Scope, Authority, and Safety

| Field | Value |
|---|---|
| Authority / RoE ID | `ROE-2026-001` |
| In-scope assets | 合成検証Tenant、設定Export、監査ログExport、アプリ登録情報、業務依存関係 |
| Out-of-scope assets | Production顧客Data、実利用者Mailbox、第三者Tenant、外部サービスへの能動操作 |
| Permitted operations | 設定Review、合成Accountによる同意フロー確認、合成Eventの生成、Rule test |
| Prohibited operations | 実Token取得・再利用、第三者への認証試行、権限昇格、永続化、DoS、Data変更 |
| Permitted data | 合成Account、予約Domain、無害化した設定・Log |
| Test window | 2026-07-20T13:00:00+09:00〜2026-07-21T17:00:00+09:00 |
| Stop conditions | 外向き通信、実Data参照、想定外の権限付与、合成Tenant外の操作が発生した場合 |
| Emergency contact | Security Program Lead |
| Cleanup owner | Platform Lead |
| Evidence retention | 90日。判断記録は2年 |

## 3. Business and Technical Context

### 3.1 Assets

| Asset ID | Asset / Service | Business role | Criticality | Data classification | Owner |
|---|---|---|---|---|---|
| `ASSET-2026-001` | `billing-bridge.example` | 請求書Dataを会計処理へ連携 | High | Confidential | Business Systems |
| `ASSET-2026-002` | Identity control plane | OAuth同意、アプリ権限、Credentialを管理 | Critical | Restricted | Platform |
| `ASSET-2026-003` | Audit log store | 同意・設定変更・認証Eventを保持 | High | Internal | SOC |

### 3.2 Trust Boundaries

| Boundary ID | From | To | Identity / protocol | Control | Failure consequence |
|---|---|---|---|---|---|
| `TB-2026-001` | 業務SaaS | Identity control plane | OAuth 2.0 app identity | Admin consent、scope review | 過大権限または不正な同意 |
| `TB-2026-002` | OAuth app | 顧客Data API | Workload credential | App permission、Conditional Access相当の制約 | 顧客Dataへの広範なAccess |
| `TB-2026-003` | Control plane | Audit log store | Audit export | Export設定、保持Policy | 調査に必要なEventの欠落 |

### 3.3 Business Constraints

- Availability requirement: 月末処理以外は4時間停止可能。
- Contractual requirement: 顧客DataのAccess範囲を必要最小限に維持する。
- Privacy requirement: 顧客Dataを合成環境へ複製しない。
- Recovery objective: 4時間以内に手動Importへ切替可能。
- Operational dependency: 経理担当が1日2回の同期結果を確認する。
- Approved compensating control: 手動Importと二者Review。

## 4. Hypotheses

### 4.1 Threat Hypotheses

| Hypothesis ID | Statement | Preconditions | Expected impact | Priority | Status |
|---|---|---|---|---|---|
| `TH-2026-001` | 請求書連携アプリの権限が業務要件を超えており、Credentialが不正利用された場合に顧客Dataへ広範にAccessできる | 過大scope、利用可能なCredential、API到達性 | 顧客Dataの閲覧・変更可能性 | High | Supported |
| `TH-2026-002` | 管理者同意の変更を監視できず、未承認のscope追加を早期検知できない | 同意Eventの未収集またはRule欠落 | 攻撃面拡大の見逃し | High | Partially supported |
| `TH-2026-003` | 既に同型の不正利用が発生した | 過去の不正Credential利用 | 過去侵害 | High | Inconclusive |

### 4.2 Observation Hypotheses

| Observation ID | Related threat hypothesis | Expected signal | Data source | Time window | Disconfirming observation |
|---|---|---|---|---|---|
| `OBS-2026-001` | `TH-2026-001` | 要件外scopeが設定Exportに存在する | App registration export | Current | 必要scopeだけに限定されている |
| `OBS-2026-002` | `TH-2026-002` | Admin consent変更EventがLogへ記録される | Control-plane audit log | 24時間 | 同意変更を再現してもEventが取得されない |
| `OBS-2026-003` | `TH-2026-003` | 不自然なToken利用またはAPI呼出しがある | Sign-in / API audit | 過去90日 | 十分なCoverageで異常がない |

### 4.3 Alternative Explanations

| Alternative ID | Explanation | Supporting evidence | Contradicting evidence | What would distinguish it |
|---|---|---|---|---|
| `ALT-2026-001` | 広いscopeは初期導入時の暫定設定が残っただけで、悪用はない | 変更履歴に導入時の設定がある | 現行要件に不要でありCredentialは有効 | Token利用の完全なTelemetry |
| `ALT-2026-002` | 同意Eventの不足は収集設定ではなく保持期間外である | 90日より前のLogはない | 合成同意Eventは現行Pipelineでも欠落した | Pipeline設定Review |

## 5. Authorized Validation Plan

| Validation ID | Related hypothesis | Minimal operation | Expected evidence | Stop condition | Cleanup |
|---|---|---|---|---|---|
| `VAL-2026-001` | `TH-2026-001` | 設定Exportと業務要件表を比較 | scope差分表 | 実Data参照が必要になった場合 | Export削除、Hash付きEvidenceだけ保持 |
| `VAL-2026-002` | `TH-2026-002` | 合成Tenantで無害な同意変更を1回実行 | Audit EventとRule結果 | 外向き通信または実Tenant参照 | 合成AppとAccountを削除 |
| `VAL-2026-003` | `TH-2026-003` | 保持済みLogを定義済みQueryで検索 | CoverageとNegative Finding | 個人識別情報が必要になった場合 | Query resultを集計・無害化 |

### 実施しない検証

- Production Credentialを利用したAPI Access。
- 顧客Dataの読出しまたは変更。
- Credential窃取、横展開、永続化、回避手法の再現。

## 6. Evidence Register

| Evidence ID | Question supported | Source / collector | Collected at | Integrity / hash | Limitation | Classification |
|---|---|---|---|---|---|---|
| `EVD-2026-001` | 現行scopeは何か | App registration export | 2026-07-20T13:20:00+09:00 | SHA-256をEvidence manifestへ記録 | 取得時点のSnapshot | Internal |
| `EVD-2026-002` | 必要scopeは何か | 業務要件とAPI仕様のReview | 2026-07-20T14:10:00+09:00 | Review承認記録 | 将来要件変更は含まない | Internal |
| `EVD-2026-003` | 同意Eventを観測できるか | 合成Tenant audit export | 2026-07-21T10:05:00+09:00 | SHA-256を記録 | Production Pipelineとの差異がある | Internal |
| `EVD-2026-004` | 過去不正利用を評価できるか | 90日分の無害化Log集計 | 2026-07-21T15:40:00+09:00 | Query versionとHashを記録 | API利用Eventの一部が未収集 | Confidential |

### Negative Finding

| Negative Finding ID | Searched behavior | Search window | Available coverage | Gaps | Permitted conclusion |
|---|---|---|---|---|---|
| `NEG-2026-001` | 未承認同意変更と異常なApp sign-in | 過去90日 | 同意変更とsign-inは72日分。API利用は一部のみ | 18日分の保持不足、API利用Field不足 | 取得できた範囲では該当Eventを確認していない。侵害不存在は断定しない |

## 7. Findings and Control Gaps

| Finding ID | Root condition | Evidence IDs | Business impact | Existing control | Recommended treatment | Status |
|---|---|---|---|---|---|---|
| `FIND-2026-001` | 業務要件を超えるApp permission | `EVD-2026-001`, `EVD-2026-002` | Credential不正利用時の影響範囲拡大 | 手動設定Review | 必要scopeへ縮小、Credential更新、再テスト | Retest Required |
| `FIND-2026-002` | 同意変更の検知Ruleがない | `EVD-2026-003` | scope変更の早期発見が遅れる | Audit logは取得 | RuleとTriage手順を追加 | Open |
| `FIND-2026-003` | API利用Telemetryが不完全 | `EVD-2026-004`, `NEG-2026-001` | 過去調査と影響範囲評価に不確実性 | Sign-in log | API auditの収集・保持を追加 | Open |

## 8. Telemetry, Detection, and Hunting

### 8.1 Telemetry Requirements

| Telemetry ID | Behavior / question | Required event and fields | Retention | Current state | Gap owner |
|---|---|---|---|---|---|
| `TEL-2026-001` | Admin consent変更 | actor、app ID、scope、target tenant、timestamp | 180日 | Available | SOC |
| `TEL-2026-002` | App credential変更 | actor、credential ID、operation、timestamp | 180日 | Available | Platform |
| `TEL-2026-003` | AppによるData API利用 | app ID、resource、operation、result、timestamp | 180日 | Partial | Platform |

### 8.2 Detection Validation

| Detection ID | Related hypothesis | Logic / query reference | Test fixture | Expected result | Actual result | Limitations |
|---|---|---|---|---|---|---|
| `DET-2026-001` | `TH-2026-002` | 許可List外scopeを含むAdmin consent変更 | 合成同意Event `FIX-CONSENT-001` | High severity alert 1件 | Pass | 許可Listの保守が必要 |
| `DET-2026-002` | `TH-2026-001` | App credential変更後の高権限利用 | 合成Event chain `FIX-APP-002` | Correlated alert 1件 | Partial | API利用Telemetry不足 |

### 8.3 Hunt or Incident Records

| Record ID | Type | Related hypothesis | Question | Time range | Result | Evidence IDs | Next action |
|---|---|---|---|---|---|---|---|
| `HUNT-2026-001` | Hunt | `TH-2026-003` | 未承認同意変更または不自然なApp sign-inはあるか | 過去90日 | 確認範囲では該当なし | `EVD-2026-004`, `NEG-2026-001` | Telemetry Gap解消後に再実施 |

## 9. Analytic Judgment

| Field | Value |
|---|---|
| Analytic Judgment ID | `AJ-2026-001` |
| Related Evidence / Negative Finding IDs | `EVD-2026-001`, `EVD-2026-002`, `EVD-2026-003`, `EVD-2026-004`, `NEG-2026-001` |
| Related Finding IDs | `FIND-2026-001`, `FIND-2026-002`, `FIND-2026-003` |
| Related Detection / Hunt / Incident IDs | `DET-2026-001`, `DET-2026-002`, `HUNT-2026-001` |
| Key judgment | 外部報告の攻撃Campaignが当社を直接標的にしている証拠はない。一方、報告された行動と同型の過大権限経路が存在し、現在のTelemetryでは過去利用を完全に評価できない。標的判断とは独立に権限縮小と観測改善が必要である |
| Confidence | 中 |
| Basis for confidence | 現行設定と業務要件の差分は直接確認した。過去利用はTelemetry Gapにより限定的である |
| Confirmed facts | 過大scope、Credential有効、同意Event取得可能、API利用Telemetry不完全 |
| Assumptions | 業務要件表が現行運用を正しく反映している |
| Alternative hypotheses | 初期導入時の暫定設定が残っただけで悪用はない |
| Information gaps | 一部API利用Event、保持期間外の履歴 |
| Deception / manipulation risk | 外部報告のActor帰属やCampaign名に依存しない判断とした |
| Indicators and signposts | scope追加、Credential追加、許可List外同意、異常なAPI利用 |
| Conditions that would change the judgment | 十分なTelemetryで過去悪用を示すEventが見つかる、または業務上広いscopeが不可欠と確認される |

## 10. Decision Record

| Field | Value |
|---|---|
| Decision ID | `DEC-2026-001` |
| Decision owner | CTO |
| Decision time | 2026-07-22T16:30:00+09:00 |
| Selected option | 権限縮小と監視強化で継続。縮小完了まで新規同意を停止 |
| Rejected options and reason | 即時全面停止は月末業務影響が大きい。現状維持は過大権限とTelemetry Gapを受容できない |
| Required actions | scope縮小、Credential更新、同意Rule導入、API audit収集、Retest |
| Action owners | Platform、SOC、Business Systems |
| Deadline | 2026-07-29T18:00:00+09:00 |
| Residual risk | 過去90日より前とTelemetry欠落期間の利用は完全に評価できない |
| Risk acceptance authority | CTO |
| Communication scope | 経営会議、Security、業務システム担当 |

## 11. Control Improvement and Retest

| Control ID | Improvement | Owner | Due date | Verification method | Result |
|---|---|---|---|---|---|
| `CTRL-2026-001` | 必要scopeだけへ縮小 | Platform | 2026-07-25 | 設定Export差分と合成業務テスト | Passed |
| `CTRL-2026-002` | Credential更新と旧Credential失効 | Platform | 2026-07-25 | Credential inventoryと利用確認 | Passed |
| `CTRL-2026-003` | 許可List外Admin consent検知 | SOC | 2026-07-27 | `FIX-CONSENT-001`でRule test | Passed |
| `CTRL-2026-004` | API利用Telemetry追加 | Platform | 2026-07-29 | Required fieldの欠落率測定 | Partial |

## 12. Reassessment

| Field | Value |
|---|---|
| Reassessment ID | `REA-2026-001` |
| Scheduled date | 2026-08-21 |
| Trigger conditions | scope変更、Credential追加、Vendor仕様変更、関連Alert、重大な外部報告 |
| Evidence to recollect | 設定Export、Rule test、Telemetry Coverage、30日Hunt結果 |
| Hypotheses to retest | `TH-2026-001`, `TH-2026-002`, `TH-2026-003` |
| Decision to revisit | 連携継続、追加制限、停止 |
| Closure criteria | 必要scopeだけで業務成立、重要Event取得、Rule test成功、残存Risk承認 |

## 13. Handoff Contracts

| Handoff ID | Provider | Consumer | Required input | Acceptance criteria | Rejection / return condition | Deadline |
|---|---|---|---|---|---|---|
| `HO-2026-001` | Assessment | SOC | Attack / Observation Hypothesis、Evidence ID、必要Event | Data sourceとFieldが特定されている | 「不審なActivityを監視」のように検証不能 | 2026-07-21 12:00 |
| `HO-2026-002` | SOC | CSIRT | Alert context、Query version、Coverage、Gap | Case IDとEvidence IDへ追跡できる | Coverage不明、時刻範囲不明 | Alert後30分 |
| `HO-2026-003` | CTI | CTO | Key Judgment、Confidence、Alternatives、Decision options | 事実と判断が分離されている | Actor名だけで推奨を正当化 | 2026-07-22 15:00 |
| `HO-2026-004` | CTO | Control owners | Decision、期限、残存Risk、Retest条件 | OwnerとDue dateがある | 「監視強化」だけで具体策なし | 2026-07-22 18:00 |

## 14. Outcome Metrics

| Metric ID | Metric | Baseline | Target | Measurement window | Owner |
|---|---|---:|---:|---|---|
| `MET-2026-001` | Decision latency | 55時間 | 48時間以内 | Case開始からDecisionまで | Security Program Lead |
| `MET-2026-002` | Critical hypothesis evidence coverage | 2 / 3 | 3 / 3、またはGapの責任者と期限を明示 | Reassessment時 | Case owner |
| `MET-2026-003` | Verified control improvement rate | 0 / 4 | 4 / 4 | 30日 | Control owners |
| `MET-2026-004` | Reassessment completed by due date | 未計測 | 100% | 四半期 | Security Program Lead |

### 件数指標を主要成果にしない理由

このCaseでは、Finding数、Alert数、Rule数、IOC数の増加は成果を意味しない。重要なのは、判断時間が短縮され、過大権限が縮小され、観測不能点が減り、再評価が期限内に行われることである。

## 15. Traceability Check

- [x] `DR-2026-001`から3つのThreat Hypothesisへ追跡できる
- [x] 各Threat HypothesisにObservationまたは情報ギャップがある
- [x] 各FindingにEvidence IDがある
- [x] DetectionとHuntが対象Hypothesisへ接続している
- [x] Analytic Judgmentが関連Evidence、Finding、Detection / Hunt / Incident IDへ直接接続している
- [x] Analytic Judgmentが事実、仮定、代替仮説、確信度を分離している
- [x] Decision Recordが選択肢、残存Risk、責任者、期限を持つ
- [x] RetestとReassessmentが定義されている
- [x] Handoffの受入条件と差戻し条件が定義されている

## 16. Review

| Review area | Reviewer / role | Result | Date | Notes |
|---|---|---|---|---|
| Technical correctness | Platform reviewer | Pass | 2026-07-30 | scopeとTelemetryの関係を確認 |
| Safety / authorization | Engagement owner | Pass | 2026-07-30 | 合成環境・最小操作を確認 |
| Evidence / source quality | Evidence reviewer | Pass | 2026-07-30 | Negative Findingの限界を確認 |
| Analytic quality | CTI reviewer | Pass | 2026-07-30 | Actor帰属へ依存しない判断を確認 |
| Decision usefulness | CTO delegate | Pass | 2026-07-30 | 選択肢、期限、残存Riskを確認 |
