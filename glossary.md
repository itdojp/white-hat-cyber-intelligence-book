# Glossary

| 用語 | 本書での意味 |
|---|---|
| Assessment | 対象の弱点、成立条件、影響、対策を許可範囲で評価する活動 |
| Authority | 対象、操作、期間、Dataを承認できる法的・契約上・組織上の権限と、その根拠 |
| Authorization | 特定のDecision Requirementについて、Authority、Scope、Safety、Disclosureの条件を満たした操作許可。技術的なAccess control上の認可とは文脈で区別する |
| Artifact Evidence | 明示した条件で作成され、Task、Source、版、限界とともに第三者がReviewできる出力 |
| Assurance State | 本書の`ART-03`で、Controlを`Unknown / Documented / Implemented / Observed / Validated`としてEvidence maturity別に記録する状態。普遍的な成熟度規格ではない |
| Attack Path | 前提条件、境界越え、影響対象、結果、観測点をEdgeとして表す非Operationalな関係。実行可能な侵害手順ではない |
| Attack Surface | Asset、Flow、Boundary、Exposure、Entry Pointの組合せとして、意図しない作用を受け得る面の集合 |
| Business Asset | Business Outcomeに寄与し、停止、毀損、漏えい等が意思決定へ影響する業務上の価値または能力 |
| Capability Judgment | 複数のEvidence itemを基に、Scope、Conditions、Reviewer、Limitations、Expiry、Reassessment Triggerを明示した限定的な能力判断 |
| Collection Gap | 判断や検知に必要なEvent、Field、期間、完全性が不足している状態 |
| Competency Area | NICE Componentsで関連する能力領域をまとめるGrouping。個人が有能であることの証明ではない |
| CTI | サイバー脅威に関する情報を、特定の判断に使える分析へ変えたもの |
| Data Owner | Dataの利用目的、分類、Access、保持、共有、廃棄の判断責任を持つ役割 |
| Decision Requirement | 誰が、何を、いつまでに、どの程度の不確実性で判断するかを定義した問い |
| Data Asset | 目的、Owner、分類、保持、共有条件を持ち、Business Outcomeまたは判断を支えるDataの集合 |
| Evidence | 問いとの関係、取得条件、完全性、限界を説明できる観測記録 |
| Evidence Manifest | EvidenceのID、実ByteのHash、生成元、Time zone、変換履歴、保持、限界を記録する目録。真実性や法的証拠能力の認定ではない |
| Lab Safety State | ART-18の八状態による合成モデルの履歴。Safe / Unsafe / Inconclusiveの判定や実行許可とは別の軸 |
| Evidence Requirement | 判断、Threat Hypothesis、ControlまたはGapを評価するために、最小十分条件と過剰収集禁止境界を定めたEvidenceへの問い |
| Entry Point | Exposureのうち、Request、Identity、DataまたはControl FlowがSystemへ入る具体的な接点 |
| Exposure | Asset、FlowまたはBoundaryが一定条件で作用を受け得る状態。VulnerabilityまたはFindingの存在を自動的に意味しない |
| Handoff Contract | 成果物を渡す側と受け取る側の間で、必須入力、受入条件、差戻し条件、期限、責任を定義した契約 |
| Integrated Security Case Map | Assessment、Detection、Hunting、IR / DFIR、CTI、意思決定、再評価を共通IDと証拠関係で接続する成果物 |
| Intelligence Requirement | 脅威分析の利用者、判断、期限、対象、情報ギャップを定義した問い。Decision RequirementのうちIntelligenceで答える部分 |
| Identity | Human、Workload、Service等を区別し、Authority、Privilege、Lifecycle、Trust sourceを追跡する主体表現 |
| Knowledge State | `Unknown / Assumed / Confirmed / Not Applicable`で個別項目の分かっている範囲を表す状態。Model全体やControl assuranceとは分離する |
| Misuse Case | Actor capability class、前提条件、影響対象、境界、結果、観測点を記録する悪用仮説。実行手順を含めない |
| Negative Finding | 定義した範囲では該当事象を観測しなかったという結果。観測不能点がある場合、事象の不存在を意味しない |
| OSINT | 公開情報を合法かつ再現可能に収集・検証する活動 |
| Provenance | 情報の由来、取得方法、時刻、変換履歴 |
| Reassessment | 時間、Scope、Source、Role、Technology、Rubricの変更または期限到来によって実施する後続Review |
| Reassessment Trigger | 判断、仮説、コントロールを再評価する契機となる期限、変更、兆候、Incident、Source更新 |
| Review Result | 一つのArtifact Evidenceを、宣言済みRubricとReviewer roleで評価した結果 |
| Residual Risk | 対策、検知、移転、受容後にも残る不確実性と損失可能性 |
| Responsible Disclosure | 脆弱性関連情報を、被害抑制、修正、利用者保護、関係者調整を考慮し、適切な窓口・時期・範囲で取り扱うこと |
| Rules of Engagement | 許可されたSecurity engagementについて、対象、手法、時間、Data、停止、連絡、復旧、報告を実施可能な条件へ具体化した規則 |
| Scope | 許可対象と対象外を、System、Tenant、Account、Environment、Data、Method、Time等の識別子で定義した境界 |
| Telemetry | 操作・状態・通信を観測するために収集するEvent、Log、Metric等 |
| Threat Hypothesis | Asset、Flow、Boundary、Exposureへの影響を、成立条件、必要Evidence、代替説明とともに検証可能にした限定仮説 |
| Threat Hunting | 既存Alertだけに依存せず、仮説に基づいて環境を探索する活動 |
| Threat-Informed | 一般論だけでなく、関連する脅威行動と自組織の文脈を判断へ反映すること |
| Trust Boundary | Identity authority、Data ownership、Administrative control、Tenant、Third-party responsibility、Control Plane等のTrustまたは責任が変わる境界。Network Segmentは一つの候補にすぎない |
| Control Plane | Identity、Policy、Configuration、Deployment等を通じてSystemの振る舞いを変更できる管理面 |
| Work Role | NICE Frameworkにおける仕事のGrouping。Job titleまたは個人を意味しない |
| 確信度 | 分析判断を支える証拠品質、整合性、情報ギャップ、代替仮説の強さに対する評価 |

## 第5章の用語

| 用語 | 本書での意味 |
|---|---|
| ATT&CK Behavior Map | ART-15。条件付きBehavior、根拠、版、Data、Evidence、GapをDecisionへ渡す記録 |
| Mapping basis | Hypothesized / Source-reported / Observed / Reproducedの根拠分類。自組織観測と公開報告を区別する |
| Catalog coverage | 選定した行動候補に対する対応付けの範囲。Detection有効性ではない |
| Observable coverage | 指定Event・Field・期間について観測できる範囲 |
| Validated coverage | 指定した条件・版・Testで期待Evidenceを確認した範囲 |
| Detection Strategy | 特定Techniqueに対する高位の検知方針。プラットフォーム向けAnalyticを束ねる |

定義の出典、Statusの有限契約、限界は[第5章](manuscript/05-attack-behavior.md)を参照する。

## 第6章の用語

| 用語 | 本書での意味 |
|---|---|
| Signal Flow | 操作、認可、状態変化、Event、収集、Evidenceを判断へ結ぶ追跡構造 |
| Event lifecycle | 生成、収集、保持、検索、検証を別の根拠で確認する観測経路 |
| Clock uncertainty | 表示時刻から真の時刻がずれ得る範囲。UTC表記への統一では解消しない |
| Queryable | 指定時点・期間・必須Fieldで検索した根拠があること。検知有効性ではない |

六Statusの有限契約と限界は[第6章](manuscript/06-observable-systems.md)を参照する。

## 第7章の用語

| 用語 | 本書での意味 |
|---|---|
| Technical severity | 脆弱性の技術的な性質と重大度。事業上の修正順位とは別 |
| Deployment / Affected | 導入有無と、版・条件が影響範囲に該当するかの別々の判断 |
| Reachability | 指定したPath・前提条件における到達性。露出面だけでは確定しない |
| Probability signal | 定義された対象・期間に関する推定入力。EPSSを個別組織の侵害確率に置き換えない |
| Compensating control | リスクを抑える代替統制。存在、検証範囲、有効期限を分離する |
| Required action applicability | 公開要請・義務が当該環境に適用されるかの確認状態。Catalog掲載とは別 |
| Residual risk | 処置後または判断待ちに残るリスク。Ownerと再評価条件を伴う |

指標の一次資料、固定Snapshot、有限教材と実務への転用限界は[第7章](manuscript/07-vulnerability-prioritization.md)を参照する。

## 第9章の用語

| 用語 | 本書での意味 |
|---|---|
| RoE | 確認済みの許可をScope・Method・Time・Data・Stop等の実施条件へ具体化する記録。権限の発生源ではない |
| Excluded by default | 未記載の対象・作用は許可せず、追加時に再審査する原則 |
| Technical completion | 対象件数、予算、停止、Cleanup等の作業記録がそろった状態 |
| Decision completion | 必要EvidenceまたはGap、代替説明、責任者の受入と再評価がそろった状態 |
| Restart authority | 停止原因の解消と残存リスクを確認し、同じ版の再開を判断する責任。Cleanupとは別 |

[第9章](manuscript/09-engagement-roe.md)の有限教材は実署名・通知・隔離・法的承認を検証しない。

## 第10章の用語

| 用語 | 本書での意味 |
|---|---|
| Attack Surface Register | Sourceから候補・所有Confidence・次Actionの不足条件まで追跡する判断記録。脆弱性一覧ではない |
| Collection class | Passive / Active / Authenticatedの三つ。Source classと実際の学習操作を別に記録 |
| Provenance | 原典、派生、取得方法、時点、変換、Hash対象、取扱いと限界の記録 |
| Owner confirmed | 対象IDと所有者の根拠を限定して照合した検証状態。実行許可ではない |
| Unverified | 所有未確認を示す属性。五Verification statesとは別 |

[第10章](manuscript/10-recon-osint-boundary.md)は完全合成・offlineで、Source真正性・法的承認・実稼働を保証しない。

## 第12章の用語

| Term | 本書での意味 |
|---|---|
| Principal | 権限評価の主体。本教材はHuman/Device/Service/Workloadの四分類を使う |
| Identity Attack Path Review | 必要条件とEvidenceを持つ権限関係の判断記録。侵害手順ではない |
| Delegation | 委任元・先・対象・Action・制限を持つ関係。任意権限の付与ではない |
| Issuer / Audience / Relying party | 発行者、意図した受入先、実際に検証・利用する受入側を分離する欄 |
| Dormant grant | 利用されていないという仮定と残るGrant。取消済みや悪意を意味しない |
| Broken path | 特定Pathに必要な条件の反証。未知の別経路の不存在ではない |
| Synthetic replay | 第12章では供給合成EventのField照合だけ。認証要求の再送はしない |

[第12章](manuscript/12-enterprise-identity.md)の六状態と観測経路のCoverageを混同しない。

## 第13章の用語

| Term | 本書での意味 |
|---|---|
| Build Plane | SourceとDependencyをArtifactへ結ぶ処理と権限の境界 |
| Provenance | Artifactの作成主体・過程・入力についての記録。存在だけでは真正性を保証しない |
| SBOM summary | 本章ではComponentの供給要約。SPDX適合や完全性を主張しない |
| Promotion plan | 環境間のArtifact移行計画。本CaseはPlanned-onlyで未承認 |
| ART21 Verified | 同一Chainと版の有限summary比較の一致。実署名・実安全・実許可ではない |

[第13章](manuscript/13-platform-supply-chain.md)の五状態をSLSA levelや親の観測状態へ読み替えない。

## 第14章の用語

| Term | 本書での意味 |
|---|---|
| Minimum evidence question | 対象ID・版と必要条件を限定し、十分性と不足を先に定める問い |
| ART22 Supported | 供給資料の二条件が支持された結果。実影響・安全性・許可とは別 |
| Not performed | 実施有無の欄。本章ではResultをInconclusiveとし、第七Resultにしない |
| Residual check | Cleanupとは別のScope・確認者・Evidenceによる残存確認。本教材の値は実測でない |
| ART22 Complete | 読解記録の整理と確認が揃うこと。業務上の問題の解決とは別 |

[第14章](manuscript/14-minimal-impact-validation.md)ではResult、実施有無、記録完了を分ける。

## 第15章の用語

| Term | 本書での意味 |
|---|---|
| Finding | 対象・条件・根拠・判断を追跡できる報告単位 |
| Retest | 変更後の対象版で受入条件を再確認する記録。Scannerの要約だけでは完了しない |
| Risk acceptance | 権限・Scope・期限・条件を持つ残存リスクの受容。評価の実行許可とは別 |
| Compensating control | 残る条件を別の手段で扱う統制。恒久改修と同一視しない |
| ART04 Closed | 十分なRetestまたは明示的な有効な受容を根拠にした記録の終了。修正済みやリスクゼロとは別 |

[第15章](manuscript/15-findings-retest-risk.md)ではStatusとResult、SeverityとPriority、受容と実施許可を分ける。

## 第16章の用語

| Term | 本書での意味 |
|---|---|
| Telemetry Coverage | 特定の対象・版・問いに必要な観測の根拠と不足 |
| Evidence Readiness | 判断に必要なデータと取扱条件の準備。法的適格性の認定ではない |
| Clock uncertainty | 時刻比較で考慮する不確かさ。到着順を発生順にしない |
| ART24 Validated | 供給合成入力の限定比較の成功。実収集・検知・権限とは別 |
| Not observed | 根拠がある限定観測Window内の未観測。侵害の不存在ではない |

[第16章](manuscript/16-telemetry-evidence-readiness.md)では七状態と相関品質、親参照とEvidence受領を分ける。

## 第18章の用語

| Term | 本書での意味 |
|---|---|
| Hunt Hypothesis | 対象と観測、支持・反証条件を持つ探索の問い |
| Negative Finding | 根拠あるCoverageと固定した対象・期間・Queryに限る未観測 |
| Pivot | 次の問いへ進む条件付き接続。無断のScope拡大ではない |
| ART06 Supported | 供給合成入力が限定仮説と整合する判断。侵害確定ではない |
| ART06 Inconclusive | 観測条件や比較目的の不足による判断保留 |

[第18章](manuscript/18-threat-hunting.md)で五ResultとCoverage、代替説明、再評価を接続する。

## 第19章の用語

| Term | 本書での意味 |
|---|---|
| Incident Candidate | 判断主体が宣言基準と比較すべき候補 |
| Incident Declaration | Owner・Reason・Timestampと基準に結び付く宣言判断 |
| Confirmed Scope | 指定対象・版・Windowの供給Evidenceで確認した範囲 |
| Unknown Scope | 観測不足などにより結論を出せない範囲。除外ではない |
| ART25 Closed | 限定した復旧検証と残余リスクの担当付き閉鎖。改善完了ではない |
| Reopened | 旧閉鎖を保持し、新Evidenceに基づいて再開する判断 |

[第19章](manuscript/19-incident-response.md)では分類・重大度・優先度・状態を分離する。
