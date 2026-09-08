# 第5章 攻撃者の行動をATT&CKで記述する

## この章の位置付け

第4章のThreat Modelは、何が重要で、どの境界で、どの条件が未確認かを表した。本章では、その条件付きのThreat Hypothesisを、他の担当者が同じ意味で扱えるBehaviorへ変換する。成果物は`ART-15 ATT&CK Behavior Map`である。

MITRE ATT&CK®は行動の共通語彙として参照する。Techniqueを付ける作業と、自組織でその行動を観測・検証する作業は別である。Tacticは目的、Techniqueは行動の方法、Sub-techniqueはより具体的な分類を表す。Tacticの列を必ず順番に通る侵入工程として読まない。`SRC-ATTACK-FAQ-001`

本章はS0〜S1の読解課題で完結する。実Target、実Log、実Credentialは使用しない。連携設定の変更、Token取得、侵害再現、外部への能動通信は行わない。

## 本章の責任境界

- **OWN**: 行動のMapping basis、版、Evidence threshold、Gap、Decisionへの接続を定義する。
- **BRIDGE**: 第4章のThreat Modelを入力とし、第6章のSignal Flow、第16〜18章の観測・検知・Hunting、第21章のControl Validation、第26章のCTI配布へ渡す。
- **DELEGATE**: 個別Techniqueの実行方法や製品固有Ruleの実装は扱わない。認証・認可の詳細は[実践認証認可設計](https://itdojp.github.io/practical-auth-book/)、評価技法の深掘りは[ペネトレーションテスト学習ガイド](https://itdojp.github.io/pentest-learning-book/)へ委譲する。戻る際は操作手順ではなく、前提、観測点、検証範囲をBehavior Mapへ記録する。

委譲先を読まなくても、本章の課題、状態判定、成果物の作成は完結する。

## 学習目標

- ATT&CKのオブジェクトを区別できる。
- Coverageの限界を説明できる。
- ATT&CK Behavior Mapを作成できる。

## 前提知識

- 第1章の`CASE-2026-001`、Decision Requirement、Evidenceの区別
- 第2章のAuthority / Scope / Stop条件
- 第4章のAsset、Threat Hypothesis、Trust Boundary、Control assurance
- OAuth連携とWorkload identityの概念。製品の管理権限や実環境は不要

## 導入ケース

請求書連携アプリの権限が広いと分かった担当者が、ATT&CKの多数のTechniqueを塗り、「この範囲は検知可能」と報告した。しかし、同意変更のAudit summaryがあっても、現在のscope、Workload identity binding、Rule test結果は未確認だった。

ここには二つの飛躍がある。過大権限という設計上の条件から具体的な行動の発生へ進む飛躍と、カタログ上の対応付けからDetectionの有効性へ進む飛躍である。さらに、類似するGroup名を添えても、そのGroupが関与した証拠にはならない。

本章では第4章の`TM-2026-001`を読み、未確認事項を残したまま次の問いに答える。

1. どの行動なら候補Techniqueの説明に合うか。
2. 何を観測できれば、候補という判断を一段進められるか。
3. 何が不足している間は、継続判断を強めてはならないか。

## 1. ThreatからBehaviorへ変換する

**F-05-01: Behavior Mapの追跡構造**

```text
Threat Hypothesis → Adversary objective → Tactic
→ Technique / Sub-technique → Preconditions / Asset / Boundary
→ Observable behavior → Required data / Detection strategy
→ Existing control → Evidence / Gap / Status
→ Decision contribution → Reassessment
```

図の読み方は左から右の変換である。上流の仮説が下流の結果を保証する矢印ではない。各矢印に根拠と差戻し条件が必要であり、入力条件が変わればMappingも戻して再検討する。

例えば「広いscopeが残る」は前提条件であって、行動の記述ではない。「SaaSの連携アプリを介したアクセス関係が、正規の承認や利用者の状態と整合せず残る可能性」は、観測する対象と比較条件を含むBehavior仮説になる。ここからT1671を検討できるが、仮説文を書いただけでは発生を主張できない。T1671の公開説明が扱う対象はCloud Application Integrationであり、カタログ上のTacticはPersistenceである。`SRC-ATTACK-T1671-001`

記入時は「対象Asset」「前提」「期待される差分」「正常な代替説明」を一組にする。未確認の前提はそのまま記録し、Technique名で埋めない。

## 2. ATT&CKオブジェクトを混同しない

**T-05-01: オブジェクトと判断上の役割**

| オブジェクト | 本章で問うこと | 単独では分からないこと |
|---|---|---|
| Tactic | どの戦術的目的を仮説に置くか | その目的を持つ主体が実在するか |
| Technique | どの行動の方法に対応するか | 自組織で実行されたか |
| Sub-technique | 分類をさらに具体化できるか | 根拠のない詳細を補ってよいか |
| Group | 公開報告で追跡される活動集合は何か | 現在の事案の実行主体か |
| Software | 行動と関連付けられたソフトウェアは何か | その製品名だけで悪意があるか |
| Campaign | ある期間・対象・目的を持つ活動群は何か | 類似する事案が同一Campaignか |
| Procedure example | 公開報告の具体例はどの対応付けを支えるか | 本書の演習として実行してよいか |
| Mitigation | 行動の成立性を下げる対策候補は何か | 自組織で実装・検証済みか |

Tactic、Technique、Sub-technique、Procedureの区別は公式FAQに従う。Group / Software / CampaignはカタログのCTIオブジェクトとして扱い、組織内のEvidenceと結合せずに帰属判断へ転用しない。`SRC-ATTACK-FAQ-001` `SRC-ATTACK-001`

T1671には、本章が固定した版でSub-techniqueがない。細かく見せる目的で小数付きIDを作らず、Sub-technique欄は「なし」とする。ATT&CK catalogの`19.2`、T1671 objectの`1.0`、教材fixtureの`1.0.0`は別の版である。`SRC-ATTACK-T1671-001`

## 3. Detection Strategyを自組織のDataへ接続する

Detection Strategyは高位の検知方針であり、複数のプラットフォーム向けAnalyticを束ねる。存在していることと、自組織で必要Dataを収集できることは異なる。`SRC-ATTACK-DET-001`

本章の例は`DET0539`を参照する。`AN1487`はOffice Suite向け、`AN1488`はSaaS向けの候補である。二つを両方採用すれば強くなるのではなく、対象環境と利用可能なDataの説明に合う方を選ぶ。`SRC-ATTACK-T1671-001`

**T-05-02: 本章で使うDetectionの参照関係**

| Analytic | Data Component | 本書側で具体化するData要件 |
|---|---|---|
| AN1487 | DC0066 / DC0069 | App・同意・権限変更の時刻、対象、変更主体、承認記録への参照 |
| AN1488 | DC0069 / DC0038 | 連携変更、承認状態、連携に関連する活動を突合するための識別子 |

表のData要件は本書の教材設計であり、製品のEvent schemaの転載ではない。公式のComponentとAnalyticの関係は固定STIX bundleで照合する。`SRC-ATTACK-T1671-001`

実務へ渡すときは、Telemetry IDごとにEvent class、必須Field、取得点、時刻の意味、保持期間、欠落期間、完全性の限界、Ownerを定める。例えばApp IDが一致してもTenantが欠けていれば、別Tenantの同名アプリを誤って結び付けるおそれがある。承認記録がない場合も、未承認だったのか、記録だけが欠けたのかを分ける。

Mutable elementは環境に合わせる判断点であり、固定値をコピーする欄ではない。承認済みアプリの範囲、同意できる役割、許容scopeの基準にOwnerと版を付ける。変更した際は正常系のnear-missも再評価する。

Data Sourcesはv18でdeprecatedとなり、歴史的な参照として残されている。本章では移行説明以外に旧分類を新しい検知設計の正本として使わない。Data Sourcesのdeprecatedと、現在利用するData Componentの有効性を一括して判定しない。`SRC-ATTACK-DS-001`

## 4. Mapping basisとStatusの証拠閾値

以下は`ART-15`固有の有限状態であり、MITREが定めた成熟度尺度ではない。証拠の追加で自動昇格するのではなく、対象行の命題をどこまで支えるかをReviewする。

**T-05-03: Statusと受入条件**

| Status | 受入条件 | 許容しない飛躍 |
|---|---|---|
| Proposed | 行動候補と調べる理由がある | Objectを選定済みとする |
| Mapped | Object、前提、Mapping basis、代替説明が対応する | 観測済み・検知有効とする |
| Observed | 同じ行のObservable behaviorに対応するEvidence IDと観測範囲がある | 合成観測を実侵害や主体の証明とする |
| Validated | 同じ行に結び付くTest ID、Expected / Actual、Result、Evidence、条件・版がありPassである | 教材テストを実製品のDetection有効性へ拡張する |
| Not applicable | 対象環境に適用しない理由がある | データ不足を対象外にする |
| Unknown | 判断に必要な情報が足りず、Gap / Owner / 再評価条件がある | 不存在または安全を主張する |

Mapping basisは`Hypothesized / Source-reported / Observed / Reproduced`から選ぶ。自組織を観測していない公開報告はSource-reportedであり、自組織のObservedではない。原典が同じ報告を複数読んでも独立Evidenceは増えない。

Observedの対象は必ず限定する。本章の合成Consent変更をObservedと記録しても、「合成記録上で変更があった」という命題だけである。悪意、Persistenceの達成、過去侵害は別の命題として未確認に残す。

ValidatedのResultは`Pass / Fail / Inconclusive / Not collected`で記録する。Pass以外、必要Evidenceの欠落、対象行・版・期待結果の不一致があればValidatedを受理しない。既存のControl assuranceや親CaseのGapは、別の検証条件を持つため自動更新しない。

## 5. 良いMappingと過剰Mappingを比較する

| 比較 | 記入例 | 判定と修正 |
|---|---|---|
| 良いMapping | 連携アプリの承認と活動の不整合を仮説化し、T1671、前提、必要Dataを記録する | Mapped。現在の発生を主張せず不足Evidenceを渡す |
| 過剰Mapping | OAuthという名称から多数のTechniqueをまとめて付ける | 不受理。行動、対象、根拠を一行ずつ対応させる |
| 根拠なしMapping | Groupとの類似だけで、合成Caseの実行主体を確定する | 不受理。AttributionのEvidenceと代替仮説がない |
| 正常系near-miss | 承認済みの連携変更が、申請と時刻・対象の両方で一致する | 変更の観測は残る。悪意とする根拠は弱まる |
| 情報不足 | 変更記録はあるが承認参照とTenantが欠ける | Unknown。未承認だったと補完しない |

悪い例は編集上の反例であり、許容される分析結論ではない。Techniqueを削除することも適切な成果である。説明できない行を残してCoverageの見かけだけを増やすより、差戻し理由と再評価条件を明記する方が後続判断に役立つ。

## 6. Coverageは分母と証拠を分ける

本章のCoverageは次の三種類に分ける。

- **Catalog coverage**: 自分たちが選定した行動候補のうち、根拠付きMappingがある範囲
- **Observable coverage**: 同じ行動候補のうち、必要なEvent・Field・期間を実際に扱える範囲
- **Validated coverage**: 明示したTest条件と版で、期待Evidenceを確認できた範囲

集計には、対象Asset、Behaviorの選び方、ATT&CK版、対象期間、除外理由、Unknown数を添える。分母の違う比率は直接比較しない。同じTechniqueへ三行を対応付けても、三つの異なるTechniqueを覆ったことにはならない。

教材の少数行がPassでも、カタログ全体、自組織の侵入経路全体、製品Coverage、Control effectivenessを保証しない。MITREの利用条件でも、カタログの分類を覆うだけで完全な防御Coverageが保証されるわけではないと説明している。`SRC-ATTACK-001`

Telemetry不足は侵害不存在ではない。Response coverageを論じるなら、検知後に誰が、いつ、どの許可で対処できるかも別に検証する。Mapping率だけを経営向けの安全性指標に置き換えない。

## 7. 版固定とMigration記録

本章は2026-09-06に確認したATT&CK catalog v19.2を使用する。Updatesページの開始日は2026-08-06、GitHub releaseの公開時刻は2026-08-05T22:57:35Zである。Version HistoryにはApril 28の表示が残るため、それをv19.2固有の公開日と読み替えない。`SRC-ATTACK-001`

固定したEnterprise bundleから8 Objectと関連を最小抽出し、CIは保存済みfixtureだけを検査する。WebsiteのVersion Permalinkはv19単位なので、minor releaseの完全な固定はSTIXのcommitとbundle hashで補う。取得方法、Objectごとのmodified、revoked / deprecated、利用条件は[Source Review Note](../references/ch05-source-review-2026-09-06.md)へ記録した。`SRC-ATTACK-T1671-001`

Migration時は旧版を上書きして終わらせず、次を記録する。

1. 旧・新catalog版、bundle hash、Object ID、Object version、modified
2. 名称、Tactic、platform、Sub-technique、Detection / Analytic / Data Component関係の差分
3. revoked / deprecatedの状態と後継Object。名前の類似だけで自動移行しない
4. 影響するBehavior Map、Telemetry、Test、判定、Owner
5. Mappingを維持・変更・保留する理由と再評価Evidence

IDが同じでも意味や関係が変わり得る。Objectが無効になれば、過去のEvidenceを削除せず、当時の版を保存したうえで新規利用を再審査する。

## 8. 四つの視点とHandoff

| 視点 | 本章で作る情報 | 次の担当者への受入条件 |
|---|---|---|
| 攻撃者行動の理解 | 目的、前提、対象、Observable behavior | 手順ではなく条件付きの行動命題である |
| 防御 | Required data、Control、検知方針候補 | Dataの有無とControl assuranceを分離する |
| 分析 | Mapping basis、Evidence、代替説明、確信度 | 合成・公開報告・自組織観測を混同しない |
| 意思決定 | 支持できる結論、Gap、Owner、期限 | 比率ではなく継続・差戻し・再評価条件を示す |

第6章にはFieldと観測点、第16〜18章にはData取得の制約と検知仮説、第21章には未検証条件、第26章には出典・版・共有範囲付きのBehavior表現を渡す。受け手が対象、版、Evidence scopeを復元できない場合は差し戻す。

## 9. 安全な演習

**目的**: `ART-15`で、対応候補と証拠の強さを区別する。

**前提・許可・範囲**: 自分の作業用コピーで、配布された完全合成JSONとMarkdownを読む。第4章の`AUTH-CASE-2026-001`を実環境の操作許可へ転用しない。新しいTenant、Data収集、Rule実行の許可は付与しない。

**入力**: [第5章合成Case](../cases/ch05-attack-behavior-example.md)、[合成Dataset](../cases/fixtures/ch05-attack-behavior.json)、[ART-15 Template](../templates/attack-behavior-map.md)。

1. `BM-2026-001`の条件とT1671を対応付け、発生を示さない理由を説明する。
2. `BM-2026-002`の合成観測が示す事実と、示さない結論を二つずつ記録する。
3. `BM-2026-003`の不足Fieldを補完せず、Gap、Owner、再評価日を維持する。
4. Templateに正常系near-missと過剰Mappingの差戻し理由を記入する。
5. `BM-2026-004`のテスト範囲を読み、親ControlをValidatedへ変更できない理由を記録する。

**期待Evidence**: ID、Mapping basis、Status、根拠、代替説明、Data gap、Decision contribution、Reassessmentを持つ記入済みMap。正解はTechnique数では評価しない。

**影響**: 作業コピーの編集だけであり、外部通信や実環境の変更はない。

**停止条件**: 実Log、実Credential、個人情報、Scope外の対象、出典不明の入力が混入した場合は追加作業を止め、隔離して教材管理者へ確認する。

**Cleanup**: 作業コピーと自分の出力だけを整理し、正本の配布ファイルを変更していないことを確認する。原典や親CaseのEvidenceを削除しない。

## 10. 作成する成果物

[ATT&CK Behavior Map](../templates/attack-behavior-map.md)は次を一つの判断記録へ接続する。

- Map / Case / Decision / Threat / Asset / Boundary ID
- Catalog / Object / fixtureの版と原典
- Mapping basis、Preconditions、Observable behavior、必要Data
- Evidence / Telemetry / Detection / Test ID、Statusと許容結論
- Existing control、Gap、Alternative mapping、Owner、Review date
- Decision contribution、Handoff、Reassessment trigger

`ART-15`は`ART-03`の仮説を置換せず、`ART-05`のDetection Validationを先取りしない。

## 11. 評価基準

| 観点 | Meets | 差戻し |
|---|---|---|
| Objectと版 | ID・Type・版・有効性・関係を原典へ追跡できる | 名称だけ、架空Sub-technique、旧版をcurrent扱い |
| 根拠と状態 | 同じ命題のEvidenceとStatusが一致する | MappedをObserved / Validatedへ読み替える |
| 観測可能性 | Field、期間、欠落、Ownerがある | Logの存在だけで検知可能とする |
| 分析 | 代替説明、Unknown、許容結論を残す | 類似から侵害や主体を確定する |
| 安全な引渡し | Scope、停止、期限、再評価を記録する | 次章への移行を操作許可とする |

## 12. よくある誤解

- **多くのTechniqueが付けば良い成果物になる**: 数ではなく、各行の対応理由と判断への寄与を評価する。
- **Observedは攻撃を確認した意味である**: 観測したのは定義したBehaviorであり、悪意や主体は別の命題である。
- **AnalyticがあるならRuleを有効化できる**: 製品schema、正常系、Data品質、権限、性能、運用条件の検証が別に必要である。
- **UnknownはNot applicableへ移せる**: 不足情報と適用対象外は異なり、情報不足を分母から消してはならない。
- **教材のPassで親CaseのGapが閉じる**: Testの目的・対象・版・条件が異なるEvidenceを流用してはならない。

## 章のまとめ

ATT&CKはBehaviorの表現を揃えるために使い、Evidenceや判断の代わりにはしない。`ART-15`では版、前提、Mapping basis、Status、観測要件、限界を固定し、次の担当者へ渡す。適切に残されたUnknownとGapも、判断に使える成果物の一部である。

## 次に学ぶこと

第6章では、Behaviorを通信・Identity・Cloudの観測点へ変換する。先に検知の検証構造を確認する場合は[第17章](./17-detection-engineering.md)へ進み、Telemetry、Test、Evidence、運用Handoffの条件を比較する。本章のMapだけでは実行権限を増やさない。

## 参考文献・Source Note ID

- `SRC-ATTACK-001`: catalog v19.2、releaseの追跡、Coverageの限界
- `SRC-ATTACK-FAQ-001`: Tactic / Technique / Sub-technique / Procedureの定義
- `SRC-ATTACK-T1671-001`: T1671、DET0539、Analytics、Data Componentsの固定metadata
- `SRC-ATTACK-DET-001`: Detection Strategyの役割
- `SRC-ATTACK-DS-001`: deprecated Data Sourcesの歴史的・移行上の扱い

版、checkedAt、固定commit、採用範囲は[Source Review Note](../references/ch05-source-review-2026-09-06.md)を参照する。
