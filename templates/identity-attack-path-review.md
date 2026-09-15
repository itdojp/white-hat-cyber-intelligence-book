# Identity Attack Path Review

## このTemplateの目的と境界

`ART-20`は、PrincipalからResourceまでの権限関係、必要条件、Evidence、反証、観測不足、Treatmentを判断要求へ結ぶ記録です。[第12章](../manuscript/12-enterprise-identity.md)と[完全合成記入例](../cases/ch12-identity-path-review-example.md)を併用します。

完全合成Graph、供給済みの設定Snapshot、Policy比較、合成Eventだけを用います。実Credential、実Token、実Cookie、実Tenant、実Directory、実Accountは使用しません。入力が不明なら追加の操作をせず停止し、OwnerへGapを返します。Templateを埋めることは実施許可の発行ではありません。

## Document ControlとDecision Requirement

| Field | 記入する内容 |
|---|---|
| Artifact / Review ID | ART-20と一意のReview ID、版、基準時点 |
| Case / Relation | Parent Case ID、refinesまたは独立関係 |
| Decision Requirement | 判断主体、問い、期限、判断を変える条件 |
| RoE / Authorization | ID、版、状態、有効期限、元Window、許可不足 |
| Scope / Stop | 供給資料、対象外、停止条件、連絡先 |
| Data / Cleanup | synthetic-only、Custodian、保持期限、自分の作業コピーだけの整理 |

## Principal Register

| Field | 記入する内容 |
|---|---|
| Principal ID / Class | Human / Device / Service / Workloadの一つ |
| Owner / Lifecycle | 責任者、利用目的、Active/Dormant/Unknown等の根拠 |
| Credential class | 種類だけ。値の欄は作らない |
| Assurance context | 未評価の範囲、認証過程の条件、Humanと非Humanの違い |
| MFA status / Exception | 有効・不明・非適用、例外の対象・期限・承認Evidence |
| Application / Role relation | App名、実行単位、Principal、Roleを同一視しない対応 |

## Role、Permission、Resource、Edge

| Field | 記入する内容 |
|---|---|
| Role ID / Permission ID | Role名と、そのRoleに結び付くPermission |
| Resource ID / Action | 何に何を許すか。用途と必要範囲 |
| Control Plane ID | 管理面の責任者とData面との境界 |
| Edge ID / From / To | 一意の辺、始点と終点、種類 |
| Membership / Delegation | 所属、委任元・先、必要な承認、制限 |
| Federation / Trust | 信頼するIssuer、意図したAudience、受入RP、境界 |
| Condition / Evidence | True / False / Unknownと、その根拠。MFAだけで代用しない |

本TemplateのEdgeは関係の記述です。Credentialを扱う操作や侵害の実行順を記入しません。製品固有のRole名を一般的な権限の意味へ読み替えないでください。

## Path Review

| Field | 記入する内容 |
|---|---|
| Path ID / Principal | 起点と判断対象のPath |
| Required privilege / Target | 必要Permission、Resource、Action |
| Necessary edge IDs | 始点・終点が連続する必要条件。未知の線を確認済みにしない |
| Graph / Policy revision | 比較する同一版、供給元、変換の有無 |
| Preconditions / Alternatives | 成立条件、否定条件、ほかの説明、未列挙経路のGap |
| Validation method | Static review / Policy simulation / Synthetic replay |
| Path state | Hypothesized / Config-confirmed / Evidence-supported / Validated / Broken / Unknown |
| Evidence IDs | 設定、Event、有限比較結果を分離した直接参照 |
| Limits | そのStateから言えないこと、親の状態を変えないこと |

Static reviewはValidatedにしません。Brokenには必要条件の反証が必要であり、MFA Enabledやログ不在だけでは記入できません。Synthetic replayは供給合成Eventの照合であり、実認証要求の再送ではありません。

## 有限比較の記録

| Field | 記入する内容 |
|---|---|
| Comparison ID / Path ID | どのPathの比較か |
| Input bindings | Principal、Resource、Action、Graph版、Policy版、必要条件 |
| Federation bindings | 該当時にIssuer、Audience、受入RPを別欄で示す。非該当の供給JSONでは三欄をnullとする |
| Expected / Actual | 期待値と再計算値、必要条件の照合結果 |
| Refuted necessary edge | Denyならどの必要条件を反証したか |
| Source Evidence / Time | 同一Pathの設定Evidence、作成者による時刻仮定 |
| Effect / Scope | 通信0、認証試行0、非実行。実測・適合保証ではない |

## Telemetry、Finding、Treatment、Reassessment

| Field | 記入する内容 |
|---|---|
| Telemetry / Detection ID | 必要Field、対象期間、相関key、収集・保持・検索の不足 |
| Finding ID / Risk | 確認事実と分析判断、業務上の影響仮説 |
| Treatment / Owner | 最小権限、例外管理、観測改善等の計画と責任者 |
| Confidence / Alternatives | 確信度、根拠、正常変更・資料不足等の代替説明 |
| Gap / Due date | 不足する情報とOwner、今回の期限 |
| Reassessment ID | 新資料・版・主体・権限・Owner・許可の変更時の再確認 |
| Handoff / Receipt | 第11/13/14/16/17章への入力、制限、受領の有無 |

## 提出前の確認

- すべてのIDと参照先が一意で、必要な関係が直接たどれる。
- Credential classだけを記録し、実Dataや値の欄を追加していない。
- 認証、認可、Federation、評価実施の許可を別に扱っている。
- 設定・Event・有限比較を分け、根拠のないState昇格がない。
- 必要条件の否定と不明を区別し、別経路の不存在を断定していない。
- 親RoE、Threat Model、Signal Flowの状態を変更していない。
- Gap、Owner、期限、Treatment、Reassessment、未受領Handoffが明記されている。

評価は第12章の五観点Rubricを用います。Unknownの記録も根拠と不足条件が揃えば有効です。実施許可や資格の認定には使用しません。
