# 第17章 合成記入例：未承認管理者同意変更のDetection Validation

## この記入例の扱い

この文書は、`Detection Validation Record`の記入方法を示すための完全な合成例である。

- 組織名、サービス名、アプリID、ログ、判断はすべて架空である。
- 実Credential、実Tenant ID、個人情報、第三者システムは使用しない。
- 技術的詳細はオフラインfixtureへ固定し、外部通信や本番操作を前提としない。
- ATT&CK mappingはBehaviorの共通語彙に使うが、Coverage proofとして扱わない。
- Detection-as-Codeの表現例は中立形式を含みうるが、形式採用だけで有効性を主張しない。

参照する空テンプレートは[Detection Validation Record](../templates/detection-validation.md)である。

## 0. Document Control

| Field | Value |
|---|---|
| Artifact ID | `ART-05` |
| Detection Validation Record ID | `DVR-2026-017-001` |
| Case ID | `CASE-DET-2026-001` |
| Related Case Map Case ID | `CASE-2026-001` |
| Related Case Map Decision ID | `DEC-2026-001` |
| Related Case Map Detection ID | `DET-2026-001` |
| Detection relationship | `refines`（第17章版は詳細化であり、第1章の合成Ruleを置換または再配備しない） |
| Related Case Map Fixture ID | `FIX-CONSENT-001` |
| Related Case Map Control ID | `CTRL-2026-003` |
| Decision Requirement ID | `DR-DET-2026-001` |
| Response Objective ID | `RO-DET-2026-001` |
| Detection ID | `DET-2026-017-001` |
| Status | Validated |
| Detection owner | SOC Detection Lead |
| Review cadence | 90日ごと、またはSchema変更時 |
| Last validated at | 2026-07-31T15:00:00+09:00 |
| Next review at | 2026-10-29T15:00:00+09:00 |

## 1. Detection Objective and Scope

| Field | Value |
|---|---|
| Business or response objective | 月末処理を止めずに、未承認権限付与を60分以内に遮断 / 承認 / 監視継続へ分類する |
| Protected asset / workflow | `billing-approval.example` の請求処理連携アプリ |
| In scope | 管理者同意変更、承認済みChange参照、同一workloadのfollow-on sign-in |
| Out of scope | 実TenantへのRule投入、Vendor固有UI操作、Credential再利用、Data export実行 |
| OWN / BRIDGE / DELEGATE boundary | OWN: Detection logicとfixture validation、BRIDGE: IR handoff、DELEGATE: 製品固有実装 |
| ATT&CK mapping | T1098 Account Manipulationを参照してBehaviorを表現 |
| ATT&CK mapping is not coverage proof | Yes |

## 2. Hypotheses and Traceability

### 2.1 Threat and observation hypotheses

| Hypothesis ID | Type | Related Decision Requirement ID / Response Objective ID | Statement | Priority | Status |
|---|---|---|---|---|---|
| `TH-DET-2026-001` | Threat | `DR-DET-2026-001`, `RO-DET-2026-001` | 承認済みChangeと一致しない管理者同意変更により、請求処理連携アプリへ業務要件外の権限が追加される | High | Supported |
| `OBS-DET-2026-001` | Observation | `RO-DET-2026-001` | 管理者同意変更Eventにactor、target workload、scope set、change ticket参照、event timeが含まれる | High | Supported |
| `OBS-DET-2026-002` | Observation | `RO-DET-2026-001` | 同一workloadのsign-in Eventを30分以内に相関できる | Medium | Partially supported |

### 2.2 Handoff and response contracts

| ID | Type | Provider | Consumer | Required input | Acceptance criteria |
|---|---|---|---|---|---|
| `TRI-DET-2026-001` | Triage | Detection Engineering | SOC analyst | `DET-2026-017-001` alert、scope差分、ticket状態、target workload、関連Evidence ID | 15分以内に`Escalate` / `Approved change` / `Needs telemetry gap review`を選べる |
| `HO-DET-2026-001` | Incident handoff | SOC analyst | CSIRT | Case ID、Detection ID、Evidence IDs、Coverage、Gap、Permitted conclusion | 60分以内判断に必要なContextが追加照会なしで渡る |

### 2.3 Detection backlog inputs

| Backlog Item ID | Input type | Related source ID | Requested detection change | Disposition |
|---|---|---|---|---|
| `DBI-DET-2026-001` | Finding | `FIND-2026-002` | 許可List外の管理者同意変更を検知する | Accept |
| `DBI-DET-2026-002` | Hunt | `HUNT-2026-001` | sign-in相関とTelemetry gapを検知・Triageへ返す | Accept |
| `DBI-DET-2026-003` | Incident | —（今回の合成Caseでは入力なし） | 将来のIncident lessonからRule、fixture、Triageを改訂する入口を保持 | Defer |
| `DBI-DET-2026-004` | CTI | —（今回の合成Caseでは入力なし） | 将来のbehavior changeからHypothesisとmappingを改訂する入口を保持 | Defer |

## 3. Data Requirement and Semantics Contract

| Telemetry ID | Source | Event / record | Required fields | Optional enrichment fields | Time contract | Identity contract | Retention | Coverage | Gap |
|---|---|---|---|---|---|---|---|---|---|
| `TEL-DET-2026-001` | Identity control-plane audit | `admin_consent_granted` | event_time、ingest_time、actor_id、target_workload_id、granted_scope_set、change_ticket_id、result | — | 判定はevent_time基準。ingest_timeは遅延監視用 | actor_idは人またはautomation ID、targetは安定workload ID | 180日 | Available | Parser drift監視が必要 |
| `TEL-DET-2026-002` | Change calendar export | `approved_change_snapshot` | change_ticket_id、approved_scope_set、window_start、window_end、owner_id | — | event_timeではなく承認Windowを比較に使用 | owner_idは人の安定ID | 365日 | Available | Ticket連携停止時は判定不能 |
| `TEL-DET-2026-003` | Workload sign-in audit | `workload_sign_in` | event_time、target_workload_id、result | credential_state、source_label | `TEL-DET-2026-001`と30分窓で相関 | target_workload_idを同じ正規化規則で揃える | 90日 | Partial（severity enrichment） | streamまたはenrichment欠落時はHigh判定を維持し、Criticalへ上げない |

### Field semantics notes

- `event_time` meaning: Eventの発生時刻。遅延到着でも相関はevent_timeを使う。
- `ingest_time` meaning: 収集パイプライン到着時刻。SLA監視専用であり、検知判定には使わない。
- `null` and empty-list semantics: `change_ticket_id = null`は「承認情報なし」。`granted_scope_set = []`は無効値としてReplayを失敗扱いにする。
- ID normalization or join rules: `target_workload_id`はDisplay nameではなく`workload-*`形式の安定IDで比較する。
- Sampling, parser drift, or ordering caveats: scopeは集合比較し、順序差を意味差と扱わない。`TEL-DET-2026-003`のsource_label欠落時は緊急度評価を`Partial`へ落とす。

## 4. Detection Logic and Detection-as-Code Lifecycle

| Field | Value |
|---|---|
| Detection logic summary | 未承認scope差分を持つ管理者同意変更を検知し、同一workload sign-inが30分以内にあれば緊急度を上げる |
| Rule / query reference | `detections/cloud_identity/det_2026_017_001.json`（合成fixture専用。実デプロイ対象ではない） |
| Correlation window | 管理者同意変更から30分 |
| Threshold / condition | `granted_scope_set - approved_scope_set != empty` かつ `change_ticket_id` が未承認または欠落 |
| Suppression / allow list | 承認済みticketと一致し、scope差分が空のものは許容 |
| Severity policy | consent変更のみはHigh、follow-on sign-in相関ありはCritical |
| Version / change set | `det-2026-017@v1.2.0-synth` |
| Fixture replay command or procedure | `python3 scripts/replay_chapter17_detection.py`でJSON ruleとfixtureを比較するオフラインReplay |
| Deploy gate | Positive / Negative / Benign-near-missの3種とTelemetry gap replayが一致し、Triage欄が埋まること |
| Maintenance trigger | scope allow list変更、Field名変更、承認フロー変更、保持期間変更 |
| Deprecation trigger | Controlで未承認管理者同意が恒久的に禁止され、代替監視で同等判断ができること |
| Deprecation owner | Detection Engineering Manager |

## 5. Synthetic Fixture Set

| Fixture ID | Fixture type | Telemetry presence | Target behavior event presence | Benign-near-miss context | Expected result | Notes |
|---|---|---|---|---|---|---|
| `FIX-2026-017-POS` | Positive | Present | Present | Absent | Alert | 未承認scope差分あり。follow-on sign-inあり |
| `FIX-2026-017-NEG` | Negative | Present | Absent | Absent | No alert | consent変更recordなし。`availableTelemetryIds`で必要Telemetryの利用可能性を別記録 |
| `FIX-2026-017-BNM` | Benign near miss | Present | Present | Present | No alert / Allowed | 承認済みChangeと一致 |
| `GAP-DET-2026-001` | Coverage gap | Missing core telemetry | Unknown | Unknown | Indeterminate | `TEL-DET-2026-002`を除いた派生Replay。Event不存在は結論しない |

### Fixture safety checks

- syntheticOnly: true
- offlineOnly: true
- noMalwareOrC2: true
- noCredentialTheft: true
- noRealCredentialsOrPII: true

## 6. Validation Results and Evidence Register

| Evidence ID | Fixture ID | Telemetry IDs used | Detection ID | Result | Analyst note | Collected at |
|---|---|---|---|---|---|---|
| `EVD-DET-2026-001` | `FIX-2026-017-POS` | `TEL-DET-2026-001`, `TEL-DET-2026-002`, `TEL-DET-2026-003` | `DET-2026-017-001` | Pass | scope差分、ticket欠落、follow-on sign-inの3要素が確認できた | 2026-07-31T14:10:00+09:00 |
| `EVD-DET-2026-002` | `FIX-2026-017-NEG` | `TEL-DET-2026-001`, `TEL-DET-2026-002`, `TEL-DET-2026-003` | `DET-2026-017-001` | Pass | 対象Behaviorがなく、No alertで期待どおり | 2026-07-31T14:20:00+09:00 |
| `EVD-DET-2026-003` | `FIX-2026-017-BNM` | `TEL-DET-2026-001`, `TEL-DET-2026-002`, `TEL-DET-2026-003` | `DET-2026-017-001` | Pass | Eventは存在するが承認済みChangeに一致し、許容判定になった | 2026-07-31T14:32:00+09:00 |
| `EVD-DET-2026-004` | `FIX-2026-017-POS` | `TEL-DET-2026-001`, `TEL-DET-2026-003` | `DET-2026-017-001` | Partial | `TEL-DET-2026-002`を外すと未承認か連携欠落かを区別できない | 2026-07-31T14:40:00+09:00 |
| `EVD-DET-2026-005` | `FIX-2026-017-POS`, `FIX-2026-017-NEG`, `FIX-2026-017-BNM` | `TEL-DET-2026-001`, `TEL-DET-2026-002`, `TEL-DET-2026-003` | `DET-2026-017-001` | Pass | 3種類のfixtureすべてで期待結果が固定化され、Replay証跡を保存した | 2026-07-31T15:00:00+09:00 |

## 7. Negative Finding and Coverage Limits

| Negative Finding ID | Related Evidence IDs | Coverage | Gap | Permitted conclusion |
|---|---|---|---|---|
| `NEG-DET-2026-001` | `EVD-DET-2026-002`, `EVD-DET-2026-004` | `FIX-2026-017-NEG`では`TEL-DET-2026-001`〜`003`が存在し、対象Behaviorなしを確認した | `TEL-DET-2026-002`が欠落すると、未承認変更の不存在ではなく判定不能になる | このfixtureでは対象Behaviorを確認していない。実環境全体で同種行動が存在しないとは結論しない |

**Rule**: Telemetry absenceとEvent absenceを混同しない。`EVD-DET-2026-004`はNo alertの根拠ではなく、Gapの根拠である。

## 8. Quality and Outcome Metrics

| Metric | Definition | Baseline | Current result | Target | Notes |
|---|---|---|---|---|---|
| Detectability | 必要Fieldが有効に取得できた割合 | 2 / 3 Telemetry streams fully usable | 3 / 3 in fixture replay、実運用は2.5 / 3相当 | 3 / 3 | `TEL-DET-2026-003`のsource_label欠落が残る |
| Test success | Positive / Negative / Benign-near-miss fixtureとTelemetry gapで期待結果を再現した割合 | 0 / 4 | 4 / 4 | 4 / 4 | `EVD-DET-2026-001`〜`005`とoffline replayで確認 |
| Triageability | 一次判定に必要なContextがAlertに含まれた割合または時間 | 想定: 追加手動照合12分 | 設計目標: 追加手動照合3分 | 5分以内 | scope差分、ticket状態、target、coverage、correlationを出力する。再現可能な時刻証跡を付けていない教材上の想定値 |
| Decision latency contribution | Ruleが遮断 / 承認 / 監視継続の判断時間をどれだけ短縮したか | 想定: 60分判断窓のうち20分を事実確認に使用 | 設計目標: 7分 | 10分以内 | 再現可能な時刻証跡を付けていない教材上の想定値であり、実測結果ではない |
| Precision assumption | 実環境での誤検知見積り前提 | 未評価 | 承認済みChange同期が機能する前提 | 承認済みChangeの誤警報を低位に維持 | Production統計ではない |
| Recall assumption | 重要Behavior取りこぼし見積り前提 | 未評価 | `TEL-DET-2026-001`が完全である前提 | 高リスクscope差分の見落としゼロ | `TEL-DET-2026-001`欠落時は崩れる |
| Base rate note | 低頻度環境での運用負荷前提 | 月5件未満の管理者同意変更 | 低base rateで手動精査可能 | 低頻度維持 | Rule件数やAlert件数を成果指標にしない |

## 9. Control Improvement and Reassessment

| Control ID | Related Detection ID | Improvement | Owner | Due date | Verification method | Status |
|---|---|---|---|---|---|---|
| `CTRL-DET-2026-001` | `DET-2026-017-001` | 承認済みscope allow listを月次レビューし、業務要件表と同期する | IAM Owner | 2026-08-15 | allow list差分レビュー | Open |
| `CTRL-DET-2026-002` | `DET-2026-017-001` | `TEL-DET-2026-003`のsource_label欠落を解消する | Platform Telemetry Owner | 2026-08-22 | Field completeness測定 | Open |

| Reassessment ID | Trigger | Scope to retest | Evidence to recollect | Scheduled date | Exit criteria |
|---|---|---|---|---|---|
| `REA-DET-2026-001` | 承認フロー変更、Field名変更、scope追加、parser更新 | `DET-2026-017-001`、3種類fixture、Triage文面 | `EVD-DET-2026-001`〜`005`を再採取 | 2026-10-29 | 3種類fixture再成功、Gap更新、Deprecation不要と判断 |

## 10. Traceability Check

- Case ID: `CASE-DET-2026-001`
- Related Case Map Case / Decision IDs: `CASE-2026-001` / `DEC-2026-001`
- Related Case Map Detection / Fixture / Control IDs: `DET-2026-001` / `FIX-CONSENT-001` / `CTRL-2026-003`
- Detection relationship: `DET-2026-017-001` `refines` `DET-2026-001`。第1章のRule testを置換せず、Data contract、Triage、Gap replayを詳細化する
- Decision Requirement ID: `DR-DET-2026-001`
- Response Objective ID: `RO-DET-2026-001`
- Threat Hypothesis IDs: `TH-DET-2026-001`
- Observation Hypothesis IDs: `OBS-DET-2026-001`, `OBS-DET-2026-002`
- Telemetry IDs: `TEL-DET-2026-001`, `TEL-DET-2026-002`, `TEL-DET-2026-003`
- Detection ID: `DET-2026-017-001`
- Positive Fixture ID: `FIX-2026-017-POS`
- Negative Fixture ID: `FIX-2026-017-NEG`
- Benign-near-miss Fixture ID: `FIX-2026-017-BNM`
- Evidence IDs: `EVD-DET-2026-001`, `EVD-DET-2026-002`, `EVD-DET-2026-003`, `EVD-DET-2026-004`, `EVD-DET-2026-005`
- Triage / Incident Handoff IDs: `TRI-DET-2026-001`, `HO-DET-2026-001`
- Control IDs: `CTRL-DET-2026-001`, `CTRL-DET-2026-002`
- Reassessment ID: `REA-DET-2026-001`
- Detection backlog input IDs: `DBI-DET-2026-001`〜`DBI-DET-2026-004`
- Source Note IDs: `SRC-ATTACK-001`, `SRC-ATTACK-DET-001`, `SRC-SIGMA-001`, `SRC-IR-001`
