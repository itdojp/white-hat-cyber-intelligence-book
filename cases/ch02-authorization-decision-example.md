# 第2章 合成記入例：OAuth連携評価前のAuthorization判断

## この記入例の扱い

この文書は`Authorization Checklist`の記入方法を示すための完全な合成例である。

- 組織、担当者、契約、Tenant、Domain、判断はすべて架空である。
- Domainは予約済みの`.example`を使用する。
- 実Credential、Token、Cookie、個人情報、第三者Systemを使用しない。
- 具体的な攻撃・侵害手順は記載しない。
- 法的判断の正解例ではなく、不明点を停止・条件・Escalationへ変換する記録例である。

参照する空Templateは[Authorization Checklist](../templates/authorization-checklist.md)である。

## 0. Document Control

| Field | Value |
|---|---|
| Artifact ID | `ART-13` |
| Authorization Record ID | `AUTH-CASE-2026-001` |
| Parent Case ID | `CASE-2026-001` |
| Relation | `refines` |
| Title | 請求書連携OAuthアプリの設定評価を開始できるか |
| Status | Decision Recorded |
| Owner | Security Program Lead |
| Decision owner | CTO |
| Classification | Internal |
| Created at | 2026-08-05T09:00:00+09:00 |
| Updated at | 2026-08-05T15:30:00+09:00 |
| Authorization expires at | 2026-08-19T18:00:00+09:00 |
| Related Issue / Ticket | `SYNTH-AUTH-2001` |

## 1. Decision Requirement

| Field | Value |
|---|---|
| Decision Requirement ID | `DR-AUTH-2026-001` |
| Decision owner | CTO |
| Decision deadline | 2026-08-05T17:00:00+09:00 |
| Decision to make | 合成TenantでOAuth permission設定を評価し、RoE作成へ進めるか |
| Available decisions | Proceed / Proceed with conditions / Do not proceed / Escalate |
| Decision criteria | Authority、Tenant境界、Data、許可操作、Stop、Cleanup、Disclosure routeが再現可能に定義されていること |
| Consequence of delay | 過大権限の可能性を確認できず、改修判断が遅れる。現行Production設定は変更しない |
| Maximum acceptable uncertainty | 委託先が管理するProduction credentialの変更権限は未確定でも、合成Tenantのread-only設定Reviewだけを分離できること |

### 判断に不要な問い

- Production Tokenが現在悪用されているか
- 外部報告のActor attribution
- 実顧客Dataへ到達できるか
- 委託先の全社Security体制

## 2. Authority Gate

| Field | Value |
|---|---|
| Gate status | Conditional |
| System owner | Business Systems Owner |
| Data owner | Finance Data Owner |
| Access administrator | Platform Administrator |
| Contracting party | A社 Procurement / Legal |
| Customer /委託者 | A社 |
| Subcontractor | Synthetic Integrator B |
| Cloud / SaaS provider | Synthetic Identity Cloud |
| Approver | CTO |
| Authority basis | Internal Security Assessment Policy + 合成Tenant利用承認 |
| Written authorization reference | `EVD-AUTH-2026-001` |
| Authorized period | 2026-08-06T09:00:00+09:00〜2026-08-19T18:00:00+09:00 |
| Withdrawal method | CTOまたはSystem ownerがTicketを`Revoked`へ変更しSecurity Program Leadへ連絡 |
| Third-party approval required | No for isolated synthetic Tenant; Unknown for Production credential operation |
| Authority gaps | Production credential変更権限と委託契約上の作業範囲は未確認 |
| Gap owner / due date | Procurement / Legal、2026-08-12 |

### Authority evidence

| Evidence ID | Description | Source / custodian | Collected at | Integrity / reference | Limitation |
|---|---|---|---|---|---|
| `EVD-AUTH-2026-001` | 合成Tenantを対象とした設定Review承認 | CTO / Ticket system | 2026-08-05T10:15:00+09:00 | `SYNTH-EVD-AUTH-001` | Production、外部API、実Credentialを含まない |
| `EVD-AUTH-2026-002` | Business Systems Ownerが対象Appと業務目的を確認 | Business Systems | 2026-08-05T10:40:00+09:00 | `SYNTH-EVD-AUTH-002` | 委託契約の解釈を含まない |

## 3. Scope Gate

| Field | Value |
|---|---|
| Gate status | Pass |
| In-scope target identifiers | `tenant-auth-lab-01.test`、`billing-bridge.example`の合成App registration、設定Export |
| Out-of-scope target identifiers | Production Tenant、顧客Tenant、外部API、Provider管理面、委託先Environment |
| Environment | Isolated Lab |
| Tenant / account / role | 合成Tenant、合成reviewer account、read-only role |
| In-scope data | 合成App metadata、合成permission、合成Audit Event |
| Prohibited data | 顧客Data、実User profile、実Mailbox、Production log、Secret value |
| Allowed methods | Configuration export、read-only comparison、合成Accountでの無害なpermission表示確認 |
| Prohibited methods | Token取得・利用、外部API call、Credential変更、権限昇格、横展開、DoS、Data変更 |
| Time window | 2026-08-06T09:00:00+09:00〜17:00:00+09:00 |
| Rate / volume / concurrency | Manual review、同時1 session、合成Event最大5件 |
| External dependencies | すべてMock。外部Networkはdefault deny |
| Redirect / discovered asset rule | Do not follow。別Target発見時は停止して再承認 |
| Scope gaps | なし |
| Gap owner / due date | Not applicable |

## 4. Safety Gate

| Field | Value |
|---|---|
| Gate status | Pass |
| Purpose of operation | 合成App permissionと業務要件の差分を確認し、Production変更案の要否を判断する |
| Expected evidence | 設定Snapshot、要件表、差分表、操作Log、Cleanup確認 |
| Minimum sufficient evidence | 不要permissionの有無と、read-only roleで設定を取得できること |
| Maximum acceptable impact | 合成Tenant内の合成App・合成Eventだけ。外向き通信0 |
| Stop conditions | 外向き通信、実Domain / Tenant / Account、Secret表示、想定外Role付与、Scope外Redirect |
| Emergency contact | Security Program Lead |
| Rollback owner | Platform Administrator |
| Cleanup owner | Lab Operator |
| Cleanup verification | 合成Account / App / Event削除、Network connection 0、残存Volume 0をChecklistで確認 |
| Personal Data handling | 使用しない。識別子は合成値のみ |
| Secret handling | Secretを作成しない。値が表示された場合は停止して画面保存せずownerへ連絡 |
| Evidence classification | Internal |
| Evidence access control | Case teamのみread |
| Retention / disposal | 90日。Decision Recordは2年。合成Labは当日Destroy |
| Safety gaps | なし |
| Gap owner / due date | Not applicable |

## 5. Disclosure Gate

| Field | Value |
|---|---|
| Gate status | Conditional |
| Discovery owner | Security Program Lead |
| Product developer / site operator contact | 合成Caseでは`security@vendor.example`。実案件では事前確認が必要 |
| Customer /委託者 contact | CTO、Business Systems Owner |
| IPA / JPCERT/CC route applicable | Unknown。製品固有脆弱性と判明した場合に公式Guidelineで再評価 |
| Coordination owner | Security Program Lead |
| Information sharing boundary | 設定差分、再現条件、無害化Evidenceのみ。Secret、顧客Data、契約書を除外 |
| Publication decision owner | CTO + Legal |
| Embargo / non-disclosure condition | 調整中は公開しない。公開判断は別Decision Recordで行う |
| Emergency disclosure condition | 利用者への切迫した影響があり、調整主体が必要と判断した場合にEscalate |
| Reauthorization required for additional validation | Yes |
| Disclosure gaps | 実案件時のVendor窓口と契約上の通知期限は未確認 |
| Gap owner / due date | Vendor Management / Legal、Production評価着手前 |

## 6. Legal, Contractual, and Policy Questions

| Question ID | Question | Applicable source / contract | Owner | Status | Answer / limitation | Recheck trigger |
|---|---|---|---|---|---|---|
| `LQ-AUTH-2026-001` | 合成Tenantのread-only設定Reviewは社内Policyの対象か | Internal Security Assessment Policy | Security Program Lead | Answered | 対象。Productionと外部Serviceは含まない | Policy改定 |
| `LQ-AUTH-2026-002` | 委託契約はProduction credential変更を許容するか | Synthetic contract | Procurement / Legal | Escalated | 本Decisionでは不要。Production変更前に確認 | Production変更案承認前 |
| `LQ-AUTH-2026-003` | 製品固有脆弱性を発見した場合の届出経路は何か | `SRC-IPA-VDP-001`、Vendor policy | Security Program Lead | Open | 発見時に対象種別と現行Guidelineを再確認 | 想定外脆弱性発見時 |
| `LQ-AUTH-2026-004` | 許可外の認証試行を行ってよいか | `SRC-JP-LAW-001`、internal policy | Legal | Answered | 行わない。合成Tenant・明示許可操作だけに限定 | Scope変更時 |

## 7. Conditions

| Condition ID | Condition | Reason | Owner | Due date | Verification | Status |
|---|---|---|---|---|---|---|
| `COND-AUTH-2026-001` | Production credentialを操作しない | 委託契約とAuthority未確認 | Lab Operator | Assessment終了まで | Evidence / operation log | Open |
| `COND-AUTH-2026-002` | 外部Networkをdefault denyにする | Scope外Serviceへの到達を防ぐ | Platform Administrator | 2026-08-06T08:30:00+09:00 | Preflight report | Satisfied |
| `COND-AUTH-2026-003` | 想定外脆弱性発見時は直ちに停止する | Disclosure routeの再評価が必要 | Security Program Lead | Assessment中 | Stop log / escalation ticket | Open |

## 8. Decision Record

| Field | Value |
|---|---|
| Authorization Decision ID | `DEC-AUTH-2026-001` |
| Selected decision | Proceed with conditions |
| Decision owner | CTO |
| Decision time | 2026-08-05T15:00:00+09:00 |
| Related evidence IDs | `EVD-AUTH-2026-001`, `EVD-AUTH-2026-002` |
| Related condition IDs | `COND-AUTH-2026-001`〜`003` |
| Confirmed facts | 合成Tenant、read-only設定Review、外部通信禁止、合成Dataだけが承認された |
| Assumptions | Mock endpointが外部通信を必要としない |
| Information gaps | Production credential変更権限、実Vendor窓口、契約通知期限 |
| Reasoning | 今回の判断にProduction操作は不要で、合成TenantへScopeを限定すれば必要Evidenceを安全に取得できる。未確認事項を条件と将来Gateへ分離した |
| Residual risk | Lab設定誤りによる外向き通信。PreflightとStop conditionで管理する |
| Required approvers | CTO、System owner、Security Program Lead |
| Reauthorization triggers | Target、Tenant、Data、Method、Provider、Time window、Production操作の追加 |

## 9. RoE Handoff

| Handoff ID | Input to RoE | Acceptance criteria | Actual status | Reject / return condition | Owner |
|---|---|---|---|---|---|
| `HO-AUTH-2026-001` | Decision Requirement | Owner、期限、判断内容 | Pass | 抽象目的のみ | CTO |
| `HO-AUTH-2026-002` | Authority evidence | 合成Tenantと期間の承認 | Pass | Productionを含める場合 | Security Program Lead |
| `HO-AUTH-2026-003` | Target / Data scope | 技術識別子、対象外、合成Data | Pass | 外部依存・実Data追加 | Platform Administrator |
| `HO-AUTH-2026-004` | Method boundary | Read-only、禁止操作、Rate | Pass | Token利用・外部API追加 | Lab Operator |
| `HO-AUTH-2026-005` | Safety plan | Evidence、Stop、Contact、Cleanup | Pass | Preflight未完了 | Security Program Lead |
| `HO-AUTH-2026-006` | Disclosure route | 停止、owner、再承認 | Conditional | 実案件の公開判断へ進む場合 | Legal / Security Program Lead |

RoEは合成Tenantの設定Reviewだけを対象に作成する。Production operationは別Authorization Recordを必要とする。

## 10. Reassessment

| Field | Value |
|---|---|
| Reassessment ID | `REA-AUTH-2026-001` |
| Scheduled date | 2026-08-06T17:30:00+09:00 |
| Trigger conditions | 外向き通信、Secret表示、Scope外Target、Production変更要求、想定外脆弱性 |
| Evidence to recollect | Preflight、operation log、configuration snapshot、cleanup report |
| Decision to revisit | 条件付き許可をClosedにできるか。追加検証が必要か |
| Closure criteria | Scope内完了、Condition違反0、Cleanup完了、未解決発見のHandoff完了 |

## 11. Traceability Check

- [x] Decision Requirementから四つのGateへ追跡できる
- [x] Authority evidenceが承認対象、期間、操作へ接続している
- [x] Target、Account、Environment、Data、対象外が技術識別子で定義されている
- [x] Expected evidence、Stop、Emergency contact、Cleanupがある
- [x] Personal DataとSecretの取扱条件がある
- [x] Disclosure routeと追加検証の再承認条件がある
- [x] `Unknown` / `Conditional`にOwnerと期限がある
- [x] Decision RecordとRoE Handoffが一致する
- [x] Reauthorization triggerがある

## 12. Review

この表は合成Case内の記入例であり、実際の章Gateまたは法的承認の証跡ではない。

| Review area | Reviewer / role | Result | Date | Evidence reference | Notes |
|---|---|---|---|---|---|
| Technical correctness | Synthetic Platform Reviewer | Pass | 2026-08-05 | `SYNTH-REV-AUTH-TECH-001` | Target / method / dataが技術識別子で定義されている |
| Safety / authorization | Synthetic Safety Reviewer | Pass | 2026-08-05 | `SYNTH-REV-AUTH-SAFE-001` | Production操作と外部通信を除外した |
| Legal / contractual source quality | Synthetic Legal Source Reviewer | Pass | 2026-08-05 | `SYNTH-REV-AUTH-LAW-001` | 法的結論を断定せず、未確認事項をEscalateした |
| Evidence / traceability | Synthetic Evidence Reviewer | Pass | 2026-08-05 | `SYNTH-REV-AUTH-EVD-001` | Evidence、Condition、Decision、Handoffを追跡できる |
| Decision usefulness | Synthetic CTO Reviewer | Pass | 2026-08-05 | `SYNTH-REV-AUTH-DEC-001` | 条件付き許可と再承認条件が明確 |
