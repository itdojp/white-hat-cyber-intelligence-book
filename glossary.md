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
