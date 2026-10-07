# 第13章 Cloud、Container、CI/CD、Software Supply Chainを評価する

## この章の位置付け

同じrelease tagを指すArtifactに署名とSBOMが付いていれば、そのまま本番へ進めてよいでしょうか。確認すべきなのは資料の数ではなく、誰が何を変更でき、その資料がどのSource、Build、Artifact、Deploymentを指すかです。

本章は[ART-21 Platform and Supply Chain Assessment](../templates/platform-supply-chain-assessment.md)へ判断を残します。Cloud、Container、CI/CD、Dependency、SaaSを個別の製品手順にせず、SourceからRuntimeまでの信頼境界として扱います。供給された合成summaryの比較だけで課題が完結します。

### OWN / BRIDGE / DELEGATE

- **OWN:** 三Plane、HumanとWorkloadの責任、変更可能点、出所の根拠、五状態、Findingと再評価を直接IDで接続します。
- **BRIDGE:** 第4章Threat Model、第6章Signal Flow、第9章RoE、第12章Identityを使い、第14章へ検証の問い、第16章へTelemetry、第27章へAIの供給過程に関する未確認条件を渡します。
- **DELEGATE:** Provider CLI、KubernetesやContainerの設定強化、CI製品とPackage managerの操作は[ITインフラセキュリティ](https://itdojp.github.io/it-infra-security-guide-book/)と[Podmanによるコンテナ運用](https://itdojp.github.io/podman-book/)へ委譲します。戻ったら設定コマンドではなく、必要条件、Owner、Evidence、停止条件をART-21へ記入します。Supply-chain exploitの実演は含めません。

## 学習目標

1. Platformの信頼境界を識別できる。
2. Supply Chainの攻撃面を整理できる。
3. Platform and Supply Chain Assessmentを作成できる。

## 前提知識

[第4章](04-assets-boundaries-threat-model.md)のAssetとBoundary、[第6章](06-observable-systems.md)の観測条件、[第9章](09-engagement-roe.md)の許可、[第12章](12-enterprise-identity.md)の主体と権限の区別を前提にします。実Cloud account、実CI、実Registry、実Tokenは不要です。

[完全合成Case](../cases/ch13-platform-supply-chain-example.md)は`CASE-2026-001`をrefinesする`PSA-2026-013`です。ここでBuild、Promotion、Runtimeと呼ぶものも、作成者が記述した非実行の記録です。実Packageの取得やビルドを行ったという意味ではありません。

## 13.1 判断要求と親の境界

問いは「供給記録のどこまでが同じ対象に結び付き、何が未確認か」です。**確認事実（教材内）**は八ChainのFieldと参照関係です。**仮定**として架空の請求書連携サービスを置きます。**分析判断**は、tagや署名の存在から許可を導かず、変更可能点と観測不足を管理することです。代替説明は正常な変更、記録遅延、資料不足で、確信度は中、出所不明の記録は低とします。実環境への一般化はしません。

親`DR-2026-001`の歴史的期限2026-07-22T00:00:00Z、`TM-2026-001`のNeeds Evidenceを保持します。`AUTH-CASE-2026-001`は2026-08-19T09:00:00Zで失効し、元のTest windowは2026-08-06T00:00:00Z〜08:00:00Zです。基準時点2026-09-15の`ROE-2026-009 v1`は **Draft / Do not proceed / executionAuthorized=false** のままです。

第12章の`PTH-IAR12-004`はcustomer summaryへの権限条件の比較であり、本章のBuildやDeployへの権限ではありません。新しいHuman / Workload IDは架空の役割記述で、親の三RoE Objectへ追加しません。`TB-2026-004` / `SF-2026-006`のcurrent bindingとCoverageはUnknownのままです。独立した`CASE-2026-011`のEvidenceや許可も借用しません。

## 13.2 三つのPlaneと変更可能点

表T-13-01: 本章の判断用分類。Providerの実装モデルを統一する分類ではありません。

| Plane | 主な問い | 記録するEvidence |
|---|---|---|
| Control Plane | 誰がPolicy、Role、配置先を変更できるか | 変更要求、主体、承認、Policy版 |
| Build Plane | 誰のSourceとDependencyを、どのBuilderで処理するか | Revision、Lock、Runner条件、Build log |
| Data Plane | 業務DataがどのRuntime境界を通るか | DeploymentとRuntimeの対応、Dataの区分 |

Buildが終わってもControl PlaneとData Planeの責任は終わりません。SaaS連携も、外部サービスという名前だけで一つの箱にせず、誰が連携設定を変更でき、WorkloadがどのDataを扱う予定かを分けます。本CaseのSaaSはmetadata-onlyで、実Providerへの接続はありません。

図F-13-01: Sourceから判断までの記録の対応（本書独自図）。

```text
Decision Requirement / RoE / service
  → Source revision / Dependency lock / Action revision
  → Builder / Workload / Runner / Build log
  → Artifact digest / SBOM summary / Provenance summary
  → Registry digest / Promotion plan / Deployment plan
  → Runtime snapshot / Control plane / Data plane
  → Evidence / five-state assessment
  → Finding / Treatment / Owner / Decision / Reassessment
```

入力は完全合成の記録、出力は条件付きの判断です。矢印は実行順の指示ではなく参照IDの対応を示します。途中で同名tagに頼り、Digestや版の対応を失ったら、その先を同じ対象として扱いません。

## 13.3 Source、Dependency、外部Action

Branchやtagは便利な名前ですが、その名前だけを変更不能な対象識別子として使いません。Source revision、Dependency lock、Actionの版・Source・Review状態を別欄に残します。Lockがあることと、内容が審査済みであることも別です。

SSDF 1.1のPS.1.1はSource等への最小権限、PS.2.1はreleaseの完全性検証情報、PS.3はreleaseと出所情報の保持、PW.4.4は第三者Componentの継続的評価を扱います。本章はこれらを根拠に、取得元・版・変更履歴・審査の問いを分けます。特定のPackageが安全であるとの判定はしません。`SRC-NIST-SSDF-001`

**悪い例**はmutable branchだけを記録し、それをVerifiedとする判断です。八Chainの002はこの問題をRejectedとして残します。003はunversioned actionと未審査の記録です。公開Package名や実リポジトリを脆弱な対象例にせず、合成の名前と予約済みDomainだけを使います。

## 13.4 Human、Workload、Runner、Secret class

HumanはPromotion計画をレビューする役割、WorkloadはBuild summaryの役割として別IDとPermissionを持ちます。Humanの承認という記載だけでWorkloadへ広い権限を与えず、Workloadの技術的な成功からHumanの承認を推定しません。

RunnerはIsolation、Network、Cache、実行権限を分けて読みます。ephemeralというラベルだけでは、状態の残存や他のBuildからの影響がない証拠になりません。004のruntime-write-excessは、期待するbuild-summary-onlyとの矛盾です。実際の権限行使は行わず、資料上の不一致としてRejectedにします。

Secretはclassだけを記録し、値、Cookie、Tokenを教材へ含めません。SP 800-190の§4.1.4はImageへのSecret埋込みを避ける考え方、§3.5.2は共有Kernelの残余リスクを扱います。2017年の原則を用いるもので、現在のContainer製品や隔離の保証ではありません。`SRC-NIST-CONTAINER-001`

## 13.5 Digest、署名、Provenance、SBOM

表T-13-02: 異なる問いを同じ「確認済み」へ畳み込まない。

| 記録 | 答える問い | それだけでは言えないこと |
|---|---|---|
| Digest | 期待するbyte列と同じ対象か | 出所の信頼、安全性、許可 |
| Signature | 指定した検証条件で署名が有効か | 署名者を信頼してよい、内容が安全 |
| Provenance | 誰が何を入力にどの過程で作ったか | 記録が真正、全依存が安全 |
| SBOM | どのComponentを記述しているか | 完全性、脆弱性なし、実Deploy一致 |

SLSA 1.2ではSource TrackとBuild Trackを区別します。前者はSource revisionの作成過程、後者はArtifactとBuildの出所情報を扱います。本書の五状態とSLSA levelを対応させません。`SRC-SLSA-001`

Artifact検証では、対象Digest、信頼するBuilderと署名の検証、Source、Build type、想定Parameterを分けます。Provenanceを持つだけでは確認が終わらず、Build L3もBuild platform自体の侵害を保証範囲へ含めません。未知のexternalParametersを拒否する規範上の推奨と、任意の外側拡張Fieldの扱いは同一ではありません。`SRC-SLSA-001`

本Caseのexpectationsは作成者が別に与えた比較条件です。chainが自称するBuilderから期待値を作りません。ただし実際のroot of trustではなく、署名状態はRecorded-unverified、実署名検証回数は0です。Verifiedは供給summaryの有限照合だけを意味し、実際のTrusted / Policy-compliant / Safeはすべて未評価です。

SPDX公式一覧のCurrent Versionは3.0、版別HTMLは3.0.1です。本章では所在と版を区別する参照に限定します。供給する簡略SBOMは本書独自のsummaryで、SPDX JSON-LDやSLSA Attestationの標準適合文書ではありません。`SRC-SPDX-001`

## 13.6 Registry、Promotion、Deployment、Runtime

Registryの同じtagでも、記録時点が違えば指す内容が異なる可能性があります。Artifact IDとDigestをRegistry、Promotion、Deployment、Runtimeへ直接結びます。008はRuntimeの記録Digestだけが異なる対比で、他の資料が整っていてもRejectedです。差異は侵害の断定ではなく、同一対象という必要条件への反証です。

StagingからProductionへのPromotionは本CaseではPlanned-only、approved=falseです。DeploymentもPlanned-only、RuntimeはAuthored-snapshot-not-deployedです。架空の将来構成の対応を調べることと、変更を実施した記録は別です。Deployment成功や復旧成功を捏造しません。

## 13.7 五状態とEvidenceの上限

表T-13-03: ART-21の有限状態。標準認証や五段階の成熟度ではありません。

| State | 本教材で必要な根拠 | 保持する限界 |
|---|---|---|
| Declared | 条件を満たすと記述したsummary | 観測・比較の実施なし |
| Observed | 同じ対象を指す観測summaryの記述 | 比較の完了なし、実測ではない |
| Verified | 同一Chain・版・期待値・Evidenceの有限比較が一致 | 実署名、実環境、安全、許可は未評価 |
| Rejected | 同じ対象の必要条件に明示的な矛盾 | 別経路や悪意の断定ではない |
| Unknown | 必要な記録やbindingが不明 | 記録不足を安全や否定へ変換しない |

既知の矛盾は他の不足より優先します。矛盾がなく必要な記録がnullならUnknownです。すべて既知でも、EvidenceのbasisがDeclared summaryならDeclared、Observed summaryならObservedに留めます。Compared summaryと同一の期待値があって初めてVerifiedとします。

001は有限一致、002〜004は前述の悪い記録、005は出所不足、006は宣言だけ、007は観測summaryだけ、008はRuntime差異です。全件をVerifiedへ直すことが課題ではありません。UnknownやRejectedに根拠、Owner、期限を付けられれば有効な成果物です。

## 13.8 観測、検証、判断へ渡す

攻撃者視点では変更可能点を仮説化し、防御者視点ではVersion、Builder、Permission、Digestの差異を観測候補にします。分析者は正常な変更や資料遅延を代替説明として比較し、意思決定者は追加資料、境界の見直し、保留を選びます。実環境での動作や侵害を推測で断定しません。

各ChainのFindingはEvidenceを直接参照し、Treatment、Owner、期限、Decision、Reassessmentへ続きます。第14章には一つの必要条件と最小Evidence、第16章にはSource revision / Builder / Artifact digest / Deployment ID / Event time、第27章にはModel・Dataの供給過程でも再検討すべき境界を渡します。

Handoffはplanned-not-deliveredです。第6章の観測状態や第12章のPath stateを、この五状態で更新しません。後続担当者の受領と新たな許可がないまま実施計画へ昇格させません。

## 13.9 安全な分析課題

**Purpose:** 八ChainをART-21へ整理し、署名・SBOM・tagがあるだけでVerifiedへ進めるかを、Caseを見る前に予想します。

**Prerequisite / Authority / Scope:** [Case](../cases/ch13-platform-supply-chain-example.md)、[合成JSON](../cases/fixtures/ch13-supply-chain.json)、[閉じたSchema](../schemas/ch13-supply-chain.schema.json)だけを使います。実Cloud、CI、Registry、Token、Package installは使用しません。任意検査はLinux/WSL2と[出版基盤](../CANONICAL_SOURCE.md)の固定依存が導入済みの本Repositoryでだけ行います。依存取得は演習に含めません。

**Expected evidence / Impact:** 出力はChain ID、必要条件、Evidence ID、五状態、反証またはGap、Owner、再評価条件です。任意コマンドはローカル教材の整合性だけを検査します。実Build、実Deploy、実署名検証、実許可発行は0です。

**Stop / Cleanup:** 未知の入力、実Dataらしい内容、外部接続の必要性、親の許可・範囲との不一致があれば停止します。失敗時は公開を止めます。自分の作業コピーだけを整理し、正本と親Evidenceを保持します。課題は30分、作業summaryは65,536byte以内、保持は終了後24時間以内を目安とし、削除や隔離の実施成功を検査結果から推定しません。

```bash
python3 scripts/check_chapter13_contract.py
```

1. Platform、三Plane、HumanとWorkloadのPermissionを分けます。
2. Source revisionとLockをBuildへ、Artifact IDとDigestをRuntimeへたどります。
3. expectationsとEvidenceが同じChainと版を指すことを確認します。
4. 002〜005と008で、矛盾と資料不足の違いを説明します。
5. 006と007を、署名やSBOMの存在だけで昇格できない理由を書きます。
6. Finding、Treatment、Owner、Decision、再評価の問いを記入します。

Schemaは供給教材だけの閉じたFieldと語彙を定義します。未知Fieldや値を拒否する契約であり、任意の実Secretを識別する検知器、標準適合validator、学習者の任意Artifactを採点する製品ではありません。表示されるDigestは合成ラベルから作成した値で、実Artifactのbyteを検証した証拠ではありません。

## 作成する成果物と評価基準

[ART-21 Template](../templates/platform-supply-chain-assessment.md)はJSONなしでも記入できます。実データではなく本Caseの記録だけで判断の筋道を説明してください。

表T-13-04: 各観点0点（欠落）、1点（曖昧）、2点（直接追跡できる）のRubric。

| 観点 | 2点の条件 |
|---|---|
| 境界と主体 | 三Plane、Human、Workload、Secret classを分ける |
| 同一対象 | Source、Lock、Build、Artifact、Runtimeを版とIDで結ぶ |
| 根拠の上限 | 署名、Trust、Compliance、Safety、許可を分離する |
| 状態と反証 | 五状態、矛盾と不足、代替説明を区別する |
| 判断への接続 | Evidence、Finding、Treatment、Owner、Decision、再評価が辿れる |

8点以上を教材の目安とします。ただし実Data混入、根拠のないVerified、実行許可への昇格、親記録の変更は点数にかかわらず差し戻します。資格や実務能力の認定ではありません。

## よくある誤解

- 固定Digestは出所の信頼や脆弱性不存在の保証ではありません。
- ProvenanceとSBOMの存在は、その真正性、完全性、評価完了の証明ではありません。
- Build Planeの権限はRuntimeやSaaS設定変更の許可ではありません。
- Containerという分類だけでは隔離成功を保証しません。
- Unknownは失敗を隠す空欄ではなく、追加の問いと責任を残した判断です。

## 章のまとめ

SourceからRuntimeまで、同じ対象・版・主体・期待値を追跡して初めて、記録の一致と不足を分けられます。ART-21は製品チェック数ではなく、その根拠と判断の上限を残す成果物です。有限一致を実際の安全性や実行許可へ一般化しません。

## 次に学ぶこと

第14章の検証設計へ、反証できる必要条件、最小Evidence、停止条件を渡します。現時点ではplanned-not-deliveredで、[目次](../TOC.md)から今後の構成を確認できます。第16章へ観測Field、第27章へAIの供給過程の境界を引き継ぐ計画も残します。

## 参考文献・Source Note ID

確認日は2026-09-15です。SSDF 1.1はFinal、1.2はInitial Public Draftとして分離し、SLSAは1.2 Approvedを採用します。採用節、版、限界、再確認条件は[Source Review Note](../references/ch13-source-review-2026-09-15.md)に記録します。

- `SRC-NIST-SSDF-001`: SSDF 1.1、CodeとRelease完全性・出所・第三者Componentの原則。
- `SRC-SLSA-001`: SLSA 1.2、Source / Build TrackとArtifact検証の前提。
- `SRC-NIST-CONTAINER-001`: SP 800-190、共有KernelとSecretの境界に限る歴史的原則。
- `SRC-SPDX-001`: SPDXの公式版の所在。供給summaryの標準適合は主張しない。
