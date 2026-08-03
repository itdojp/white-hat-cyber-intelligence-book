# 第25章 合成記入例：共同報告に埋もれた技術クラスタの判断

## この記入例の扱い

この文書は、`Analytic Judgment Record`の記入方法を示すための完全な合成例である。

- 組織名、報告、分析者、判断、Domain、IP Addressはすべて架空である。
- Domainは予約済みの`.example`のみを使用する。
- 実在のActor、組織、国家、個人への帰属は行わない。
- 実Credential、Token、Cookie、個人情報、第三者Systemは使用しない。
- 外部報告はすべて合成であり、分析構造だけを学ぶ。

参照する空テンプレートは[Analytic Judgment Record](../templates/analytic-judgment-record.md)である。機械可読datasetは[chapter 25 dataset](../cases/fixtures/ch25-structured-analysis-attribution-dataset.json)を参照する。

## 0. Document Control

| Field | Value |
|---|---|
| Artifact ID | `ART-11` |
| Case ID | `CASE-2026-025` |
| Title | 共同報告に埋もれた技術クラスタの判断 |
| Status | Decision Support |
| Analytic cut-off | 2026-07-29T18:00:00+09:00 |
| Decision owner | SYNTH-CISO |
| Primary analyst | SYNTH-CTI Lead |
| Reviewers | SYNTH-SOC Lead、SYNTH-Identity Lead、SYNTH-Risk Manager |
| Classification | Internal |
| Created at | 2026-07-27T09:30:00+09:00 |
| Updated at | 2026-07-29T17:40:00+09:00 |

## 1. Decision Requirement and Intelligence Requirement

| Field | Value |
|---|---|
| Decision Requirement ID | `DR-2026-025` |
| Intelligence Requirement ID | `IR-2026-025` |
| Decision to support | Partner向け注意喚起、即時Block、追加収集優先度をどう設定するか |
| Decision deadline | 2026-07-30T10:00:00+09:00 |
| Consumer / customer | SYNTH-CISO、SYNTH-Partner Operations Owner |
| Key question | 観測した事象をTechnical clusterとして扱うべきか。CampaignやOperatorを示唆してよいか |
| Out-of-scope question | 実在国家または実在組織の支援有無 |
| Maximum acceptable uncertainty | 成功したfollow-on accessの有無は未確定でも、Partner通知とBlock判断に必要な表現境界が定まること |
| Decision impact if wrong | 過小評価すると再発防止が遅れる。過大評価すると誤通知と不要な停止を招く |

## 2. Scope, Safety, and Ownership Boundary

| Field | Value |
|---|---|
| Scope statement | `SN-2026-025-001`〜`008`の合成Mail gateway、Decoy proxy、Domain registration export、Vendor bulletin、Blog repost、translated excerpt、Newsletter recap、IdP sign-in summaryだけを使い、2026-07-21から2026-07-29までの判断を支援する |
| Allowed data | `synthetic-mail-gateway`, `synthetic-decoy-proxy`, `synthetic-registrar-export`, `synthetic-vendor-bulletin`, `synthetic-blog-repost`, `synthetic-translated-excerpt`, `synthetic-newsletter-recap`, `synthetic-idp-sign-in-summary` |
| Prohibited data | 実Credential / 個人情報 / 実在第三者Data |
| OWN boundary | 競合仮説、不確実性、Attribution Ladder、Judgment表現 |
| BRIDGE boundary | Identity telemetryの詳細取得要件、Partner通知手順 |
| DELEGATE boundary | 実在主体の帰属調査、法執行機関連携 |
| Stop condition | 実在Targetを調査しないと結論できない場合、または実Data混入を検知した場合 |

## 3. Candidate Threat Hypotheses

この節の`TH-*`は、対象化、反復送達、成功後のaccessという同一Case内で併存し得るBehavior仮説である。Section 5.1の`ALT-*`は焦点質問ごとに分ける。`ALT-2026-025-001`は外部誘導かSSO保守かを直接競合させ、`ALT-2026-025-002` / `003`はtechnical eventと併存し得る帰属境界の代替説明として評価する。異なる焦点質問の仮説を、一つの相互排他的なACH集合へ混在させない。Source independenceは`SEH-*` / `SEJ-*`だけで評価し、`TH-*`や`ALT-*`へ混在させない。

| Threat Hypothesis ID | Related Decision Requirement ID | Related Intelligence Requirement ID | Statement | Preconditions | Expected observable | Expected impact | Current assessment |
|---|---|---|---|---|---|---|---|
| `TH-2026-025-001` | `DR-2026-025` | `IR-2026-025` | `signin-bridge.example`と`portal-reset.example`を用いたcredential-relay型のTechnical clusterが、SYNTH-ORG-ALPHA社のPartner administratorを狙っている | 誘導メール送達、認証誘導ページ到達、redirector稼働 | lure mail、redirect chain、近接登録Domain | 認証情報の窃取、follow-on accessの試行 | Supported |
| `TH-2026-025-002` | `DR-2026-025` | `IR-2026-025` | credential-relay型Technical clusterは、近接登録した合成Domainを使いPartner administrator向けlureを反復送達する | 誘導mail送達とredirector稼働 | 同型lureの再送、近接登録Domain、同じredirect sequence | 追加の認証情報窃取試行 | Partially supported |
| `TH-2026-025-003` | `DR-2026-025` | `IR-2026-025` | credential-relayが成功した場合、Technical clusterはPartner資源へのfollow-on accessを試行する | 認証情報が入力され、有効な認証経路がある | IdP sign-in telemetry、token replay、session作成痕跡 | 不正accessと封じ込め範囲の拡大 | Inconclusive |

## 4. Observation Hypotheses and Collection Gaps

### 4.1 Observation Hypotheses

| Observation Hypothesis ID | Related Threat Hypothesis ID | Expected signal | Data source | Time window | Disconfirming observation |
|---|---|---|---|---|---|
| `OBS-2026-025-001` | `TH-2026-025-001` | `portal-reset.example`への誘導mailと`signin-bridge.example`経由のredirect chainが同一Case内に現れる | `SN-2026-025-001` Mail gateway quarantine export、`SN-2026-025-002` Decoy reverse-proxy log | 2026-07-21〜2026-07-29 | 誘導mailはあるがredirect chainが別Domain群で完結する |
| `OBS-2026-025-002` | `TH-2026-025-002` | 同型lureの再送、近接登録Domain、同じredirect sequenceが見つかる | `SN-2026-025-001` Mail gateway、`SN-2026-025-002` Decoy capture、`SN-2026-025-003` Domain registration export | 2026-07-21〜2026-07-29 | 同型lureが再送されず、redirect sequenceも再現しない |
| `OBS-2026-025-004` | `TH-2026-025-003` | 成功したfollow-on accessを示すIdP telemetryまたはtoken replay痕跡がある | `SN-2026-025-008` IdP sign-in summary | 2026-07-21〜2026-07-29 | 十分なCoverageで成功痕跡がない |

### 4.2 Source-evaluation hypotheses

Source-evaluation hypothesisは、脅威行動ではなく報告の来歴・独立性を評価するためだけに用いる。Threat Hypothesis IDへ混在させない。

| Observation Hypothesis ID | Source-evaluation hypothesis ID | Statement | Expected signal | Data source | Disconfirming observation |
|---|---|---|---|---|---|
| `OBS-2026-025-003` | `SEH-2026-025-001` | 外部報告は同一原典から派生し、独立したcorroborationを構成しない | 同一screen shot、同一hash、引用連鎖 | `SN-2026-025-004` SYNTH-MEDIA-RESEARCH-001 bulletin、`SN-2026-025-005` SYNTH-MEDIA-WEEKLY-001 repost、`SN-2026-025-007` SYNTH-MEDIA-WEEKLY-001 recap | 各媒体が別原典または独自観測を提示する |

### 4.3 Alternative-hypothesis test observations

| Observation Hypothesis ID | Related Alternative Hypothesis ID | Expected signal | Data source | Disconfirming observation |
|---|---|---|---|---|
| `OBS-2026-025-005` | `ALT-2026-025-002` | translated excerptの原文文脈、発言者provenance、取得経路が検証できる | `SN-2026-025-006` translated excerpt | 原文、発言者、取得経路がtechnical eventのOperatorへ直接接続される |

### 4.4 Collection Gaps

| Collection Gap ID | Related hypothesis or question | Missing evidence | Why it is missing | Decision impact | Priority |
|---|---|---|---|---|---|
| `GAP-2026-025-001` | `TH-2026-025-003`の成功可否 | 詳細なIdP token issuance telemetry | 保持期間が7日で、対象期間前半の詳細eventが失われた | 成功したfollow-on accessの有無を断定できない | 高 |
| `GAP-2026-025-002` | `SEH-2026-025-001`のlineage精度 | Newsletterの編集履歴 | 合成bulletin archiveにrevision履歴がない | same-origin republicationの時系列強度が限定される | 中 |
| `GAP-2026-025-003` | translated excerptの解釈 | 原文全文と発言者metadata | 合成例では抜粋と訳文だけを配布 | 意図推定の確信度が上がらない | 中 |
| `GAP-2026-025-004` | `TH-2026-025-001`のmail Coverage | quarantine exportのarchive完全性とfilter-bypass集計 | source-system完全性の別証跡を合成Caseに含めていない | exportが不完全ならlure頻度を過小評価する | 中 |

## 5. Alternative Hypotheses and Key Assumptions

### 5.1 Alternative Hypotheses

| Alternative Hypothesis ID | Explanation | Supporting evidence | Contradicting evidence | What would weaken it |
|---|---|---|---|---|
| `ALT-2026-025-001` | 認証誘導挙動は社内SSO保守検証の副作用であり、外部誘導ではない | redirect chainだけを見れば似たURL遷移があり得る | quarantine mailと外部登録Domainが同時に存在する | change ticketと送信元整合が確認されないこと |
| `ALT-2026-025-002` | translated excerptはTechnical clusterと無関係な第三者が既知報告の用語を模倣して作成したfalse flagであり、technical eventのOperatorを示さない | 出典と発言者が確認できず、用語だけが既知報告と一致する | excerpt以外の内部観測は独立に存在する | 原文、発言者、取得経路がTechnical clusterへ直接接続されること |
| `ALT-2026-025-003` | shared phishing kitの再利用であり、同一Operatorや同一Campaignは言えない | 共通HTML断片とTLS fingerprintだけではkit再利用の可能性が残る | lure内容がPartner administratorに特化し、redirect chainも一致する | kit以外の独自運用癖が反復確認されること |

焦点質問と中心Judgmentへの関係を分ける。

| Alternative Hypothesis ID | Focus question | Relationship to primary judgment | Current disposition | Related Evidence IDs |
|---|---|---|---|---|
| `ALT-2026-025-001` | 外部誘導か、承認済みSSO保守の副作用か | Directly competing | Weakened。quarantine mail、外部redirect chain、近接登録した合成Domainの組合せは保守だけでは説明しにくい | `EVD-2026-025-001`, `EVD-2026-025-002`, `EVD-2026-025-003` |
| `ALT-2026-025-002` | translated excerptはtechnical eventのOperatorを識別するか | Attribution boundary | Excerptだけではplausible。内部観測のtechnical eventを否定しない | `EVD-2026-025-006` |
| `ALT-2026-025-003` | 共通Artifactは同一OperatorまたはSponsorを識別するか | Attribution boundary | Plausible。L2を超える帰属を止める | `EVD-2026-025-002`, `EVD-2026-025-003`, `EVD-2026-025-004` |

### 5.2 Key Assumptions

| Assumption ID | Statement | Why needed | Failure trigger | Related Gap IDs |
|---|---|---|---|---|
| `ASM-2026-025-001` | quarantine exportは対象期間の誘導mail評価に対して実質的に完全である | scoped mail sourceでlure送達を評価するため | archive欠落やfilter bypassが判明した場合 | `GAP-2026-025-004` |
| `ASM-2026-025-002` | Vendor bulletinはscreen shotの撮影時刻を改変していない | 時系列比較に必要 | bulletin revision差分で時刻矛盾が見つかった場合 | `GAP-2026-025-002` |
| `ASM-2026-025-003` | translated excerptの訳語「collector」は認証誘導役を意味する | 意図解釈に必要 | 原文確認で別義が優勢と判明した場合 | `GAP-2026-025-003` |
| `ASM-2026-025-004` | IdP sign-in summaryは明示した2026-07-23〜2026-07-29のCoverage内で実質的に完全である | 観測範囲を越えずにNegative Findingを解釈するため | summary欠落またはsummary外のtoken issuance recordが判明した場合 | `GAP-2026-025-001` |

## 6. Source Notes and Evidence Register

### 6.1 Source Notes

| Source Note ID | Origin | Reliability | Credibility | Independence group | Collected at | Provenance note | Limitation |
|---|---|---|---|---|---|---|---|
| `SN-2026-025-001` | `synthetic-mail-gateway` — Synthetic mail gateway quarantine export | 高 | 中 | `IG-INT-001` | 2026-07-27T08:40:00+09:00 | Internal synthetic control-plane export。取得経路は固定 | mail bodyは要約保持のみ |
| `SN-2026-025-002` | `synthetic-decoy-proxy` — Synthetic decoy reverse-proxy log | 高 | 高 | `IG-INT-002` | 2026-07-27T09:10:00+09:00 | Decoy tenantの直接観測。hash固定 | follow-on accessの成否は含まない |
| `SN-2026-025-003` | `synthetic-registrar-export` — Synthetic domain registration export | 中 | 中 | `IG-EXT-001` | 2026-07-27T10:05:00+09:00 | registrar snapshotを無害化して保存 | privacy registrationのため登録者は判定不能 |
| `SN-2026-025-004` | `synthetic-vendor-bulletin` — SYNTH-MEDIA-RESEARCH-001 bulletin | 中 | 中 | `IG-EXT-002` | 2026-07-28T07:50:00+09:00 | screenshotと要約を掲載。原典扱い候補 | revision履歴なし |
| `SN-2026-025-005` | `synthetic-blog-repost` — SYNTH-MEDIA-WEEKLY-001 repost | 低 | 低 | `IG-EXT-002` | 2026-07-28T12:00:00+09:00 | `SN-2026-025-004`の引用が主 | 独自観測なし |
| `SN-2026-025-006` | `synthetic-translated-excerpt` — SYNTH-Translated chat excerpt | 低 | 低 | `IG-EXT-003` | 2026-07-29T08:20:00+09:00 | 抜粋のみ。訳文付与済み | 原文全文なし、発言者確認不能 |
| `SN-2026-025-007` | `synthetic-newsletter-recap` — SYNTH-MEDIA-WEEKLY-001 recap | 低 | 低 | `IG-EXT-002` | 2026-07-29T09:45:00+09:00 | repostとbulletinを再要約 | same-origin republicationの可能性 |
| `SN-2026-025-008` | `synthetic-idp-sign-in-summary` — Synthetic IdP sign-in summary | 高 | 中 | `IG-INT-003` | 2026-07-29T10:15:00+09:00 | 2026-07-23〜2026-07-29の合成sign-in summary。取得経路とhashを固定 | token issuance詳細と対象期間前半2日分は保持外 |

### 6.2 Evidence Register

| Evidence ID | Source Note ID | Related Observation / Source-evaluation hypothesis ID | Question supported | Collected at | Integrity / hash | Limitation | Synthetic confirmation |
|---|---|---|---|---|---|---|---|
| `EVD-2026-025-001` | `SN-2026-025-001` | `OBS-2026-025-001` | 誘導mailは存在したか | 2026-07-27T08:40:00+09:00 | SHA-256をdatasetへ記録 | body要約のみ | yes |
| `EVD-2026-025-002` | `SN-2026-025-002` | `OBS-2026-025-001` | redirect chainは一致するか | 2026-07-27T09:10:00+09:00 | SHA-256をdatasetへ記録 | success/failureの後段は不明 | yes |
| `EVD-2026-025-003` | `SN-2026-025-003` | `OBS-2026-025-002` | Domain登録は近接しているか | 2026-07-27T10:05:00+09:00 | SHA-256をdatasetへ記録 | privacy registration | yes |
| `EVD-2026-025-004` | `SN-2026-025-004` | `OBS-2026-025-003` | 外部報告は何を主張しているか | 2026-07-28T07:50:00+09:00 | bulletin snapshot hash | revision履歴なし | yes |
| `EVD-2026-025-005` | `SN-2026-025-005` | `OBS-2026-025-003` | Blogは独自観測を持つか | 2026-07-28T12:00:00+09:00 | article snapshot hash | Vendor bulletinの引用中心 | yes |
| `EVD-2026-025-006` | `SN-2026-025-006` | `OBS-2026-025-005` | translated excerptはOperator識別に使えるか | 2026-07-29T08:20:00+09:00 | excerpt snapshot hash | 訳語依存、原文欠落 | yes |
| `EVD-2026-025-007` | `SN-2026-025-007` | `OBS-2026-025-003` | Newsletterは独立報告か | 2026-07-29T09:45:00+09:00 | recap snapshot hash | same-originの可能性 | yes |
| `EVD-2026-025-008` | `SN-2026-025-008` | `OBS-2026-025-004` | 保持範囲内に成功したfollow-on accessまたはtoken replay痕跡があるか | 2026-07-29T10:15:00+09:00 | SHA-256をdatasetへ記録 | 7日summaryのみ。token issuance詳細なし | yes |

### 6.3 Negative Finding

Missing evidenceとevidence of absenceを分離する。

| Negative Finding ID | Related Evidence IDs | Related Observation Hypothesis ID | Searched behavior | Search window | Available coverage | Gap | Permitted conclusion |
|---|---|---|---|---|---|---|---|
| `NEG-2026-025-001` | `EVD-2026-025-008` | `OBS-2026-025-004` | 成功したfollow-on accessまたはtoken replay | 2026-07-21〜2026-07-29 | IdP sign-in summary 2026-07-23〜2026-07-29 | `GAP-2026-025-001` によりtoken issuance詳細と対象期間前半2日分が欠落 | 観測範囲では成功痕跡を確認していない。侵害不存在や未遂確定は断定しない |

## 7. Uncertainty Register

| Uncertainty ID | Type | Description | Affected IDs | Mitigation | Residual effect |
|---|---|---|---|---|---|
| `UNC-2026-025-001` | translation | `SN-2026-025-006`の訳語「collector」が認証情報収集役か一般的な回収役か不明 | `EVD-2026-025-006`, `AJ-2026-025` | 原文全文の再取得をCollection Priorityへ追加 | 意図推定は`低`確信度に留める |
| `UNC-2026-025-002` | timestamp | Vendor bulletinの撮影時刻と公開時刻が一致するか不明 | `EVD-2026-025-004`, `EVD-2026-025-005`, `EVD-2026-025-007` | 公開順ではなくhash一致と引用関係でlineageを判断 | 外部時系列強度は限定的 |
| `UNC-2026-025-003` | entity | `portal-reset.example`運用者と`signin-bridge.example`登録者が同一か不明 | `EVD-2026-025-002`, `EVD-2026-025-003` | 同一Owner前提を置かずTechnical clusterに限定 | Operator帰属は保留 |

## 8. Lineage, Circular Reporting, and Deception

### 8.1 Lineage Register

| Lineage Edge ID | From Source Note ID | To Source Note ID | Relationship | Independence effect |
|---|---|---|---|---|
| `LIN-2026-025-001` | `SN-2026-025-004` | `SN-2026-025-005` | republishes | counts-as-same |
| `LIN-2026-025-002` | `SN-2026-025-004` | `SN-2026-025-007` | derived-from | counts-as-same |
| `LIN-2026-025-003` | `SN-2026-025-005` | `SN-2026-025-007` | cites | counts-as-same |

### 8.2 Circular Reporting Candidates

| Circular Reporting ID | Related Source Note IDs | Why it is circular or same-origin | Do not count as independent corroboration |
|---|---|---|---|
| `CR-2026-025-001` | `SN-2026-025-004`, `SN-2026-025-005`, `SN-2026-025-007` | BlogとNewsletterがVendor bulletinを再掲し、NewsletterがBlogの解説も参照している。見かけ上は三報告だが原典は一つ | yes |

### 8.3 Source-evaluation judgment

| Source-evaluation Judgment ID | Statement | Basis | What would change it |
|---|---|---|---|
| `SEJ-2026-025-001` | Vendor bulletin、repost、recapの三件は独立外部観測とは言えない | `SEH-2026-025-001`、`LIN-2026-025-001`、`LIN-2026-025-002`、`LIN-2026-025-003`、同一independence group、`CR-2026-025-001` | 各媒体が別原典または独自観測を提示する |

### 8.4 Deception / False Flag / Shared Tooling / Infrastructure Reuse

| Deception Candidate ID | Category | Description | Evidence IDs | Alternative explanation supported | Analyst note |
|---|---|---|---|---|---|
| `DECPT-2026-025-001` | shared tooling | HTML断片とTLS fingerprintは既知kitの再利用でも説明できる | `EVD-2026-025-002`, `EVD-2026-025-003`, `EVD-2026-025-004` | `ALT-2026-025-003` | Technical clusterの根拠には使うが、同一Operator根拠には使わない |
| `DECPT-2026-025-002` | false flag | translated excerptの用語が既知報告を意識して混ぜられた可能性がある | `EVD-2026-025-006` | `ALT-2026-025-002` | 文書だけで意図は断定しない |
| `DECPT-2026-025-003` | infrastructure reuse | 近接登録Domainと共用hostingは短期再利用の可能性がある | `EVD-2026-025-003` | `ALT-2026-025-003` | 登録の近接だけでSponsorを示さない |

## 9. Attribution Ladder Assessment

| Attribution Assessment ID | Ladder level | Confidence | Evidence threshold met | Related Evidence IDs | Related Alternative Hypothesis IDs | Permitted language | Prohibited jump |
|---|---|---|---|---|---|---|---|
| `ATTR-2026-025-001` | L2 | 中 | 誘導mail、redirect chain、近接登録DomainによりTechnical clusterの関連は示せるが、独立外部裏付けとOperator固有癖は不足 | `EVD-2026-025-001`, `EVD-2026-025-002`, `EVD-2026-025-003`, `EVD-2026-025-004` | `ALT-2026-025-001`, `ALT-2026-025-002`, `ALT-2026-025-003` | 「同一Technical clusterの可能性がある」「Partner administratorを狙うcredential-relay型の挙動と整合する」 | Campaign、Operator、組織、国家の断定 |

## 10. Structured Analytic Judgment

### 10.1 Confirmed Facts

| Confirmed Fact ID | Statement | Evidence IDs |
|---|---|---|
| `CF-2026-025-001` | `portal-reset.example`へ誘導する隔離mailが存在した | `EVD-2026-025-001` |
| `CF-2026-025-002` | Decoy reverse-proxy logで`signin-bridge.example`を含むredirect chainを観測した | `EVD-2026-025-002` |
| `CF-2026-025-003` | `portal-reset.example`と`signin-bridge.example`は近接時刻に登録されていた | `EVD-2026-025-003` |

### 10.2 Assumptions

| Assumption ID | Statement | Why needed | Failure trigger | Related Gap IDs |
|---|---|---|---|---|
| `ASM-2026-025-001` | quarantine exportが対象期間の誘導mail評価に対して実質的に完全である | lure観測の有無を評価するため | archive欠落やfilter bypassが判明した場合 | `GAP-2026-025-004` |
| `ASM-2026-025-002` | Vendor bulletinのscreen shotは撮影後に編集されていない | lineage評価のため | bulletin revision差分が見つかった場合 | `GAP-2026-025-002` |
| `ASM-2026-025-003` | translated excerptの訳語は攻撃意図を過度に誇張していない | 意図推定のため | 原文全文で別義が優勢と分かった場合 | `GAP-2026-025-003` |
| `ASM-2026-025-004` | IdP sign-in summaryは明示した2026-07-23〜2026-07-29のCoverage内で実質的に完全である | Coverage内のNegative Findingを解釈するため | summary欠落またはsummary外のtoken issuance recordが判明した場合 | `GAP-2026-025-001` |

### 10.3 Judgments

| Analytic Judgment ID | Statement | Confidence | Basis | Related Alternative Hypothesis IDs | What would change the judgment |
|---|---|---|---|---|---|
| `AJ-2026-025` | 観測事象はPartner administratorを狙うcredential-relay型Technical clusterと整合するが、外部報告の独立性不足とshared toolingの可能性があるため、CampaignやOperatorまでの表現は支持しない | 中 | `ALT-2026-025-001`はquarantine mail、外部redirect chain、近接登録した合成Domainにより弱まる。一方、`ALT-2026-025-002` / `003`はexcerptとL2超の帰属境界として残り、成功したfollow-on accessも未確認である | `ALT-2026-025-001`, `ALT-2026-025-002`, `ALT-2026-025-003` | 承認済みSSO保守ticketがtechnical event全体を説明する、独立Partner telemetryで同一lureとfollow-on accessが確認される、またはkit再利用を示す強い証拠が出る |

### 10.4 Forecasts

| Forecast ID | Statement | Time horizon | Confidence | Indicators / Signposts |
|---|---|---|---|---|
| `FOR-2026-025-001` | 7日以内に同型Domainの追加登録または再送mailが発生する可能性がある | 7日 | 中 | `IND-2026-025-001`, `IND-2026-025-002` |
| `FOR-2026-025-002` | 追加収集がなければ、Campaign / Operator表現へ進める材料は30日以内にも不足したまま残る可能性が高い | 30日 | 中 | `IND-2026-025-003` |

### 10.5 Recommendations

| Recommendation ID | Statement | Owner | Priority | Related Decision ID |
|---|---|---|---|---|
| `REC-2026-025-001` | `portal-reset.example`と`signin-bridge.example`をBlockし、Partner administratorへ再認証と注意喚起を行う | SYNTH-Security Operations | 高 | `DEC-2026-025` |
| `REC-2026-025-002` | IdP token issuance telemetry保持を30日へ延長する | SYNTH-Identity Lead | 高 | `DEC-2026-025` |
| `REC-2026-025-003` | translated excerptの原文全文とVendor bulletin revision履歴を追加収集する | SYNTH-CTI Lead | 中 | `DEC-2026-025` |

## 11. Indicators and Signposts

| Indicator / Signpost ID | Statement | Related hypothesis | Monitoring source | Escalation trigger |
|---|---|---|---|---|
| `IND-2026-025-001` | `reset`、`portal`、`signin`を含む近接登録Domainの増加 | `TH-2026-025-001` | synthetic registration watchlist | 同一週に二件以上の追加登録 |
| `IND-2026-025-002` | Partner administrator向けの同型lure subject再送 | `TH-2026-025-001` | mail gateway synthetic rule | 24時間以内に再送一件以上 |
| `IND-2026-025-003` | kit再利用を示す公開fixture一致 | `TH-2026-025-002` | internal fixture comparison | 共通HTML断片だけでなく既知builder signatureも一致 |

## 12. Decision Record and Collection Priority

### 12.1 Decision Record

| Field | Value |
|---|---|
| Decision ID | `DEC-2026-025` |
| Related Analytic Judgment ID | `AJ-2026-025` |
| Selected option | Technical clusterとしてPartnerへ注意喚起し、Blockと再認証を実施する。Campaign / Operator表現は採用しない |
| Rejected options and reason | 何もしない案は再送リスクを無視する。Campaign / Operatorとして通知する案は証拠閾値を超えている |
| Residual risk | 成功したfollow-on accessの有無は`GAP-2026-025-001`解消まで未確定 |
| Communication scope | SYNTH-CISO、SYNTH-Partner Operations Owner、SYNTH-SOC Lead、SYNTH-Identity Lead |

### 12.2 Collection Priority

| Collection Gap ID | Priority | Why it matters to the decision | Owner | Due date |
|---|---|---|---|---|
| `GAP-2026-025-001` | 高 | 成功したfollow-on accessの有無で封じ込め範囲が変わる | SYNTH-Identity Lead | 2026-08-05T18:00:00+09:00 |
| `GAP-2026-025-002` | 中 | 外部報告の独立性評価を強化できる | SYNTH-CTI Lead | 2026-08-07T18:00:00+09:00 |
| `GAP-2026-025-003` | 中 | translated excerptの意図推定を弱化または補強できる | SYNTH-CTI Lead | 2026-08-07T18:00:00+09:00 |
| `GAP-2026-025-004` | 中 | quarantine exportの完全性によりlure頻度評価が変わる | SYNTH-Mail Telemetry Lead | 2026-08-07T18:00:00+09:00 |

## 13. Reassessment and Invalidation

| Field | Value |
|---|---|
| Reassessment ID | `REA-2026-025` |
| Review date | 2026-08-08T10:00:00+09:00 |
| Triggering indicators / signposts | `IND-2026-025-001`, `IND-2026-025-002`, `IND-2026-025-003` |
| Invalidation condition | Partner-side telemetryで成功したfollow-on accessが確認される、または原文全文確認によりtranslated excerptの意図推定が崩れる、または外部報告の独立観測が追加されCampaign閾値を満たす |
| Next action if invalidated | `AJ-2026-025`を失効させ、新しいCase snapshotでJudgmentを再作成する |

## 14. 読み方

このCaseで重要なのは、`AJ-2026-025`の結論そのものより、次の制御である。

- `CR-2026-025-001`により、外部報告の水増しを止めている
- `NEG-2026-025-001`により、不成功と不存在を混同していない
- `ATTR-2026-025-001`により、L2 Technical clusterで止めている
- `REA-2026-025`により、無効化条件を先に定義している
