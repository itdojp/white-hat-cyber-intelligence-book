# ART-21 Platform and Supply Chain Assessment

## 目的と使用範囲

SourceからRuntimeまでの変更可能点、必要条件、Evidence、判断の上限を記録するTemplateです。[第13章](../manuscript/13-platform-supply-chain.md)と[完全合成記入例](../cases/ch13-platform-supply-chain-example.md)を使います。本Templateの完成は、実Cloud、CI、Registry、Package、Tokenへの操作許可ではありません。

## Authority / Scope / Safety

Assessment ID、Case ID、Service ID、RoE IDと版、対象、期限、Stop、Ownerを最初に記入します。CASE-2026-001の補足ならrefinesを明示し、親RoE Draft / Do not proceed / executionAuthorized=false、失効したAUTHと元Window、三Objectを変更しません。独立CASE-2026-011の許可やEvidenceは借用しません。

合成Policy、SBOM summary、Provenance summary、Build log summary、Artifact metadataだけを用います。Secretはclassのみで、実値、Token、Cookie、Credentialは使用しません。実Cloud、実Registry、実CIへ接続せず、実Build、実Deploy、署名検証を実施しません。

## 記入欄

表T-13-05: 一つのAssessmentについて、同じ対象と版を直接IDで接続する。

| Field group | 必須欄 | 差し戻す条件 |
|---|---|---|
| Identity | Assessment / Case / Service / RoE / revision / asOf | 別Caseや失効記録から許可を借用 |
| Platform | Control / Build / Data Plane、Runtime boundary、SaaS scope | 境界とOwnerが不明 |
| Source | Repository / revision / Lock ID / Lock digest | branch名やtagだけを不変根拠にする |
| Dependency / Action | ID / version / Source / review / revision | 未審査やunversionedをVerifiedへ昇格 |
| Principal / Secret | Human / Workload ID、Permission、Owner、Secret class IDと分類 | 主体の混同、Secret値の入力 |
| Build | ID / Source ID / revision / Lock / Builder / Runner / Isolation / Network / Cache / log ID | 別Sourceや過大権限を見落とす |
| Artifact | ID / Build ID / Digest / Signature status / SBOM ID | 署名やSBOMの存在を安全保証にする |
| Provenance | ID / subject digest / Source / Lock / Builder / build type / parameters | 対象や信頼する主体が別 |
| Promotion / Runtime | Registry / Digest / environment / Promotion / Deployment / Runtime IDsと各状態 | 同名tagで差替えを見落とす |
| Evidence / State | 同じChain / version / expectation / basis / 五状態 / 反証またはGap | 別対象のEvidence、根拠のない昇格 |
| Decision | Finding / Treatment / Owner / 期限 / Decision / Reassessment | 次の問いと責任が不明 |

## Stateと判断の規則

状態はDeclared / Observed / Verified / Rejected / Unknownの五つだけです。これは本書の記録契約で、SLSA levelでも標準適合証明でもありません。

必要条件の既知の矛盾があればRejected、矛盾がなく必要な情報が不明ならUnknownです。条件が一致しても宣言summaryだけならDeclared、観測summaryだけならObservedです。同一Chain、版、期待値、Evidenceを使った有限比較が一致するときだけVerifiedとします。実測がない本Caseでは、Observedという語も作成者が記述した観測summaryの範囲です。

Signed、Trusted、Policy-compliant、Safeと実施許可は別の問いです。期待するBuilderを、未検証のProvenance自身の主張から採用しません。Recorded-unverifiedな署名、未評価のTrustやComplianceを、有限Verifiedで上書きしません。

## 親と次工程への接続

ART-21→第12章Identity Path→第6章Signal Flow→第4章Threat Modelを直接IDで結びます。ただし背景のGapを参照するだけなら、その用途を明示します。customer summaryへのPermissionをBuild/Deployへ転用しません。非FederationのIssuer / Audience / RPがnullであることと、不足資料のUnknownも区別します。

第14章へValidation question、第16章へBuild/Deployの相関Field、第27章へModel/Data供給過程の境界を渡す計画を残します。現在はplanned-not-deliveredで、親の状態やCoverageを更新しません。

## Stop / Cleanup / Rubric

未知の入力、実Dataらしい内容、外部接続の必要性、許可・境界の不一致があれば停止します。自分の作業コピーだけを整理し、正本と親Evidenceを保持します。合成ラベルのDigestを実Artifactの検証結果として記入しません。

第13章の五観点Rubricを用い、各0〜2点、8点以上を教材の目安にします。実Data混入、根拠のないVerified、実行許可への昇格、親記録変更があれば点数にかかわらず差し戻します。Unknownでも根拠・Owner・期限があれば有効な成果物です。
