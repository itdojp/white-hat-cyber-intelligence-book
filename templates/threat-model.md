# Threat Model

## 目的

このテンプレートは、業務判断に必要なAsset、Flow、Trust Boundary、Exposure、Threat Hypothesis、Attack Path、Control、Evidence、Gap、Action、Reassessmentを、同一Artifact内で追跡可能に記録するために使用する。

## 使用条件

- 合成Case、自己所有環境、または明示的に許可された隔離環境だけを前提とする。
- 実在第三者Target、実Credential、実Token、実Cookie、個人情報、実在顧客Dataを記載しない。
- Commands、Payloads、Exploit steps、資格情報、実Target識別子を書かない。
- Attack PathはEdge単位で記録し、再現手順書や侵害手順へ拡張しない。
- Evidenceは判断に必要な最小十分量で止め、過剰収集境界を明示する。
- Unknownを推測でConfirmedにしない。未確認事項はGap、Owner、Action、Reassessment triggerへ落とす。

## 0. Document Control

| Field | Value |
|---|---|
| Artifact ID | `ART-03` |
| Threat Model ID | `TM-YYYY-NNN` |
| Parent Case ID | `CASE-YYYY-NNN` |
| Relation | `refines` / `supersedes` / `independent` |
| Decision Requirement ID | `DR-YYYY-NNN` |
| Authorization Record ID | `AUTH-CASE-YYYY-NNN` |
| Title |  |
| Model status | Draft / In Review / Approved for Assessment / Needs Evidence / Superseded |
| Owner |  |
| Decision owner |  |
| Contributors |  |
| Reviewers |  |
| Classification | Public / Internal / Confidential / Restricted |
| Created | ISO 8601 date |
| Updated | ISO 8601 date |
| Review deadline | ISO 8601 date |
| Reassessment date | ISO 8601 date |
| Related Issue / Ticket |  |

## 1. Decision Context

| Field | Value |
|---|---|
| Decision Requirement ID | `DR-YYYY-NNN` |
| Business process |  |
| Decision to support |  |
| Decision deadline | ISO 8601 |
| In-scope environment | Synthetic Lab / Self-owned Non-production / Other Authorized Isolated Environment |
| Out-of-scope environment | Production / Third-party / Unknown |
| Scope statement |  |
| Non-goals |  |
| Business criticality scale | Mission Critical / High / Moderate / Low |
| Safety boundary | Synthetic-only / Explicitly authorized isolated validation only |
| Minimum sufficient evidence standard |  |
| Overcollection boundary |  |
| Reassessment trigger summary |  |

### Decision notes

- OWN boundary:
- BRIDGE boundary:
- DELEGATE boundary:
- Explicit stop condition:

## 2. Asset Register

Asset typeは、Business Outcome / Service / Component / Data / Identity / Control Plane / Evidence の有限集合だけを使用する。Knowledge stateは Unknown / Assumed / Confirmed / Not Applicable を使用する。

Business Assetは8番目のTypeではない。具体的なService / Component / Data / Identity / Control Plane / Evidence行の`Business role / outcome`に業務能力名を記録し、Business Outcomeへ接続する。Data AssetはType `Data`、Evidence AssetはType `Evidence`で表す。

| Asset ID | Type | Name | Business role / outcome | Owner | Criticality | Data classification | Knowledge state | Evidence IDs | Dependency IDs |
|---|---|---|---|---|---|---|---|---|---|
| `ASSET-YYYY-NNN` |  |  |  |  |  |  |  | `EVD-YYYY-NNN` | `DEP-YYYY-NNN` |
| `ASSET-YYYY-NNN` |  |  |  |  |  |  |  |  |  |

### Asset completion check

- [ ] Business Outcomeが技術Assetと分離されている
- [ ] DataとIdentityが独立Assetとして扱われている
- [ ] Evidence assetが必要な場合だけ登録されている
- [ ] ConfirmedでないAssetに根拠またはGapがある

### Dependency Register

| Dependency ID | From asset | To asset | Why the dependency matters | Failure consequence |
|---|---|---|---|---|
| `DEP-YYYY-NNN` | `ASSET-YYYY-NNN` | `ASSET-YYYY-NNN` |  |  |
| `DEP-YYYY-NNN` |  |  |  |  |

## 3. Flow Register

Flow typeは Data / Identity / Control の有限集合だけを使用する。Evidence statusは Planned / Collected / Rejected / Inconclusive を使用する。FlowはNode間の関係のみを記録し、操作手順や通信内容の再現詳細を書かない。

| Flow ID | Flow type | Source Asset ID | Destination Asset ID | Purpose | Protocol class | Identity / authorization context | Boundary IDs crossed | Data classification | Evidence status | Observation point |
|---|---|---|---|---|---|---|---|---|---|---|
| `FLOW-YYYY-NNN` |  | `ASSET-YYYY-NNN` | `ASSET-YYYY-NNN` |  |  |  | `TB-YYYY-NNN` |  | Planned |  |
| `FLOW-YYYY-NNN` |  |  |  |  |  |  |  |  |  |  |

## 4. Trust Boundary Register

Boundary typeは Identity Authority / Data Ownership / Administrative Control / Tenant / Third-party Responsibility / Control Plane / Network の有限集合だけを使用する。

| Boundary ID | Boundary type | From / To | Owner(s) | Trust / authority change | Crossing condition | Control | Failure consequence | Knowledge state | Evidence IDs |
|---|---|---|---|---|---|---|---|---|---|
| `TB-YYYY-NNN` |  | `ASSET-YYYY-NNN` → `ASSET-YYYY-NNN` |  |  |  | `CTRL-YYYY-NNN` |  |  | `EVD-YYYY-NNN` |
| `TB-YYYY-NNN` |  |  |  |  |  |  |  |  |  |

### Boundary interpretation notes

- Boundaryは「誰が何を信頼してよいか」を記録する。
- 同一管理者でもData Ownershipが異なる場合は別Boundaryとして扱う。
- Third-party Responsibilityは委託、SaaS、Managed Serviceの責任分界を記録する。

## 5. Exposure and Entry Point Register

ExposureはInterface、Identity path、Administrative surface、Control Plane access、Data ingress / egressを含む。実URL、実IP、実Account名、実Credentialは記載しない。

| Exposure ID | Related Asset / Boundary / Flow IDs | Entry Point ID | Reachability class | External dependency | Required authority | Verification status | Evidence ID | Gap ID |
|---|---|---|---|---|---|---|---|---|
| `EXP-YYYY-NNN` | `ASSET-YYYY-NNN`, `TB-YYYY-NNN`, `FLOW-YYYY-NNN` | `EP-YYYY-NNN` | Isolated / Internal / Partner-mediated / Publicly described |  |  | Unknown / Assumed / Confirmed / Not Applicable | `EVD-YYYY-NNN` | `GAP-YYYY-NNN` |
| `EXP-YYYY-NNN` |  |  |  |  |  |  |  |  |

### Entry Point Detail Register

Entry PointはExposureから独立して定義する。一つのExposureが複数のEntry Pointを持つ場合は、同じExposure IDを複数行から参照する。

| Entry Point ID | Related Exposure IDs | Interface class | Description | Owner | Boundary IDs | Required authority | Observation point | Knowledge state | Evidence IDs |
|---|---|---|---|---|---|---|---|---|---|
| `EP-YYYY-NNN` | `EXP-YYYY-NNN` |  |  |  | `TB-YYYY-NNN` |  |  | Unknown / Assumed / Confirmed / Not Applicable | `EVD-YYYY-NNN` |
| `EP-YYYY-NNN` |  |  |  |  |  |  |  |  |  |

## 6. Threat Hypothesis and Misuse Case

Hypothesis statusは Candidate / Supported / Partially Supported / Disconfirmed / Inconclusive の有限集合だけを使用する。Misuse Caseは望ましくない成立条件と業務影響を記録し、攻撃実行方法の記述へ拡張しない。

| Hypothesis ID | Decision Requirement ID | Related Asset IDs | Boundary / Flow / Exposure IDs | Statement | Preconditions | Expected impact | Evidence needed | Alternative explanation | Priority | Hypothesis status |
|---|---|---|---|---|---|---|---|---|---|---|
| `TH-YYYY-NNN` | `DR-YYYY-NNN` | `ASSET-YYYY-NNN` | `TB-YYYY-NNN`, `FLOW-YYYY-NNN`, `EXP-YYYY-NNN` |  |  |  | `EREQ-YYYY-NNN` |  | High / Medium / Low |  |
| `TH-YYYY-NNN` |  |  |  |  |  |  |  |  |  |  |

### Misuse Case Register

| Misuse Case ID | Goal | Actor capability class | Preconditions | Affected assets | Boundary crossed | Expected outcome | Observation points | Excluded operational detail |
|---|---|---|---|---|---|---|---|---|
| `MISUSE-YYYY-NNN` |  |  |  | `ASSET-YYYY-NNN` | `TB-YYYY-NNN` |  |  | Commands / Payloads / Exploit procedures |
| `MISUSE-YYYY-NNN` |  |  |  |  |  |  |  |  |

### Hypothesis quality checks

- [ ] Asset、Boundary、Exposureが一つ以上接続している
- [ ] PreconditionsとImpactが分離されている
- [ ] Observableがある
- [ ] Unsupportedな断定表現を避けている

## 7. Attack Path Register

Attack PathはEdgeのみを記録する。Node列挙、条件、影響、観測点、既存Controlとの関係を記載し、Commands、Payloads、Exploit steps、資格情報、実Target、回避手法の詳細は記載しない。

| Attack Path ID | Edge ID | From Asset / State | Condition | Boundary ID | To Asset / State | Affected Asset IDs | Expected impact | Observation point | Required Evidence ID | Knowledge state |
|---|---|---|---|---|---|---|---|---|---|---|
| `PATH-YYYY-NNN` | `EDGE-YYYY-NNN` | `ASSET-YYYY-NNN` / state |  | `TB-YYYY-NNN` | `ASSET-YYYY-NNN` / state | `ASSET-YYYY-NNN` |  |  | `EREQ-YYYY-NNN` |  |
| `PATH-YYYY-NNN` | `EDGE-YYYY-NNN` |  |  |  |  |  |  |  |  |  |

### Explicit prohibitions for this section

- Do not include commands.
- Do not include payload strings.
- Do not include exploit steps or sequencing instructions.
- Do not include credentials, tokens, cookies, or secrets.
- Do not include real target identifiers or reachable addresses.

## 8. Control Assurance Register

Control statusは Unknown / Documented / Implemented / Observed / Validated の有限集合だけを使用する。Statusは本Artifactで扱うControlごとの局所評価であり、組織全体の成熟度評価として流用しない。

| Control ID | Related Asset / Boundary / Threat / Path IDs | Control statement | Owner | Assurance state | Evidence IDs | Limitation | Gap ID | Reassessment trigger |
|---|---|---|---|---|---|---|---|---|
| `CTRL-YYYY-NNN` | `ASSET-YYYY-NNN`, `TB-YYYY-NNN`, `TH-YYYY-NNN`, `PATH-YYYY-NNN` |  |  | Unknown / Documented / Implemented / Observed / Validated | `EVD-YYYY-NNN` |  | `GAP-YYYY-NNN` |  |
| `CTRL-YYYY-NNN` |  |  |  |  |  |  |  |  |

### Control evidence guidance

- Documented: 承認済み文書または構成基準の存在を確認した状態
- Implemented: 構成または設定が存在すると確認した状態
- Observed: 期待される挙動またはログを観測した状態
- Validated: 本CaseのHypothesisに照らし有効性を確認した状態

## 9. Assumptions, Unknowns and Gaps

Knowledge stateがAssumedまたはUnknownの項目は、この節で回収計画を持たせる。Not Applicableは理由を必ず残す。

### Assumption Register

| Assumption ID | Statement | Owner | Validation method | Due date | Status | Related IDs |
|---|---|---|---|---|---|---|
| `ASM-YYYY-NNN` |  |  |  | ISO 8601 date | Unknown / Assumed / Confirmed / Not Applicable | `ASSET-YYYY-NNN`, `TH-YYYY-NNN` |
| `ASM-YYYY-NNN` |  |  |  |  |  |  |

### Gap Register

Gap statusは Open / Accepted temporarily / Escalated / Closed の有限集合だけを使用する。

| Gap ID | Missing information / control / telemetry | Decision affected | Owner | Due date | Status | Evidence Requirement ID | Action ID | Reassessment ID |
|---|---|---|---|---|---|---|---|---|
| `GAP-YYYY-NNN` |  | `DR-YYYY-NNN` |  | ISO 8601 date | Open | `EREQ-YYYY-NNN` | `ACT-TM-YYYY-NNN` | `REA-TM-YYYY-NNN` |
| `GAP-YYYY-NNN` |  |  |  |  |  |  |  |  |

## 10. Evidence Requirements and Actions

Evidenceは最小十分性と過剰収集境界を同時に定義する。ここでいうEvidenceは、合成Data、構成断面、承認済み文書、スクリーンショット、ログ断片、テスト結果要約などのArtifact-specific evidenceに限定する。Evidence RequirementのStatusは Required / Deferred / Replaced / Not Applicable とし、Collected EvidenceのPlanned / Collected / Rejected / Inconclusiveとは混在させない。

| Evidence Requirement ID | Question | Related Threat / Control / Gap | Minimum sufficient evidence | Forbidden / over-collection boundary | Owner | Due date | Status | Resulting Evidence IDs |
|---|---|---|---|---|---|---|---|---|
| `EREQ-YYYY-NNN` |  | `TH-YYYY-NNN`, `CTRL-YYYY-NNN`, `GAP-YYYY-NNN` |  |  |  | ISO 8601 date | Required / Deferred / Replaced / Not Applicable | `EVD-YYYY-NNN` |
| `EREQ-YYYY-NNN` |  |  |  |  |  |  |  |  |

### Collected Evidence Register

Collected Evidence statusは Planned / Collected / Rejected / Inconclusive の有限集合だけを使用する。Evidence Requirementの状態と混在させない。

| Evidence ID | Related Evidence Requirement IDs | Evidence description | Collection conditions / provenance | Status | Reviewer | Collected at | Limitation |
|---|---|---|---|---|---|---|---|
| `EVD-YYYY-NNN` | `EREQ-YYYY-NNN` |  | Synthetic / Authorized isolated / Inherited | Planned |  | ISO 8601 |  |
| `EVD-YYYY-NNN` |  |  |  |  |  |  |  |

### Action Register

| Action ID | Related Gap / Control / Threat | Action | Owner | Due date | Success evidence | Status |
|---|---|---|---|---|---|---|
| `ACT-TM-YYYY-NNN` | `GAP-YYYY-NNN`, `CTRL-YYYY-NNN`, `TH-YYYY-NNN` |  |  | ISO 8601 | `EVD-YYYY-NNN` | Open / In Progress / Blocked / Done |
| `ACT-TM-YYYY-NNN` |  |  |  |  |  |  |

### Evidence handling rules

- 実Dataが混入した場合は収集、共有、公開を停止し、除去手順とOwnerを記録する。
- 最小十分性を超える追加取得は、Decision ownerまたはAuthorization ownerの再承認を要する。
- Negative findingは「未観測」を示せても「不存在」の証明には使わない。

## 11. Reassessment and Handoff

| Reassessment ID | Trigger | Scope | Owner | Scheduled date | Inputs required | Closure criteria | Destination chapter / artifact |
|---|---|---|---|---|---|---|---|
| `REA-TM-YYYY-NNN` |  | `ASSET-YYYY-NNN`, `TH-YYYY-NNN`, `CTRL-YYYY-NNN` |  | ISO 8601 date | `EVD-YYYY-NNN` |  | Chapter N / `ART-NN` |
| `REA-TM-YYYY-NNN` |  |  |  |  |  |  |  |

### Handoff checklist

- [ ] Decision Requirementへ接続している
- [ ] Asset、Flow、Boundary、Exposureが識別子で追跡できる
- [ ] 各Threat HypothesisにEvidenceまたはGapがある
- [ ] Attack Path edgeがControlへ接続している
- [ ] Unknown / AssumedにOwner、Action、期限がある
- [ ] Reassessment triggerが定義されている

## 12. Review and Rubric

### 12.1 Review Record

| Review area | Reviewer / role | Rubric | Result | Date | Evidence reference | Notes |
|---|---|---|---|---|---|---|
| Decision usefulness |  | `RUBRIC-TM-YYYY-005` | Pass / Changes required | ISO 8601 | `EVD-YYYY-NNN` |  |
| Technical boundary correctness |  | `RUBRIC-TM-YYYY-001`, `RUBRIC-TM-YYYY-002` | Pass / Changes required | ISO 8601 |  |  |
| Safety and authorization |  | `RUBRIC-TM-YYYY-004` | Pass / Changes required | ISO 8601 |  |  |
| Evidence sufficiency |  | `RUBRIC-TM-YYYY-003` | Pass / Changes required | ISO 8601 |  |  |
| Reassessment readiness |  | `RUBRIC-TM-YYYY-005` | Pass / Changes required | ISO 8601 |  |  |

### 12.2 Artifact Rubric

| Rubric ID | Criterion | Meets | Partially meets | Does not meet |
|---|---|---|---|---|
| `RUBRIC-TM-YYYY-001` | Asset taxonomy | Business Outcome、7値Type、Business Asset roleが区別される | 一部を区別するがroleが曖昧 | Component一覧だけで終わる |
| `RUBRIC-TM-YYYY-002` | Boundary and flow clarity | Flow type、Boundary type、Entry PointがIDで追跡できる | 一部のOwnerまたは型が曖昧 | Network境界だけで責任境界が欠落する |
| `RUBRIC-TM-YYYY-003` | Threat usefulness | Hypothesis、Path、Evidence Requirementが接続する | Evidenceまたは反証条件が弱い | 脅威名だけで検証条件がない |
| `RUBRIC-TM-YYYY-004` | Safety and authorization | AUTH条件、非Operational記述、停止条件を保つ | 条件はあるが差戻し条件が弱い | Authorization境界を拡張する |
| `RUBRIC-TM-YYYY-005` | Decision handoff quality | Action、Gap、Reassessment、Handoffが具体的 | Ownerまたは期限が不足する | 後続Artifactへ接続しない |

### 12.3 Limitations

| Limitation ID | Scope / condition | Unsupported claim | Owner | Reassessment trigger |
|---|---|---|---|---|
| `LIM-TM-YYYY-NNN` |  | Threat ModelまたはFramework mappingによる完全性証明 |  | Scope / Source / Control / Evidence change |
