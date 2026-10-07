# 第10章 ReconnaissanceとOSINTの境界

## この章の位置付け

証明書の記録に自社のサービスと似た名前が見つかりました。それは現在の自社資産でしょうか。存在する名前、公開された情報、組織による所有、現在の稼働、検査の許可は、別々の根拠を必要とします。発見件数を増やすだけでは、この問いに答えられません。

本章では、提供済みの合成資料を[ART-19 Attack Surface Register](../templates/attack-surface-register.md)へ変換します。Sourceと候補Assetを分離し、確認できた範囲、代替説明、確認不足、次の承認要求を記録します。[第9章RoE](09-engagement-roe.md)がDraftであることは変えません。教材の読解は実対象へのAssessment開始ではなく、新しい候補をRoEのScopeに追加する操作でもありません。

### OWN / BRIDGE / DELEGATE

- **OWN:** ReconとOSINTの収集境界、三つのCollection class、ART-19、所有Confidence、第三者関係、次Actionの承認Gateを説明します。
- **BRIDGE:** 第2章Authorization、第4章Threat Model、第9章RoEを参照し、第12〜13章へ限定したAsset候補、第23〜24章へCollection RequirementとProvenanceを渡します。
- **DELEGATE:** 検索EngineやScannerの操作、脆弱性別手順は[Pentest学習書](https://itdojp.github.io/pentest-learning-book/)の責任範囲とします。本章には実在人物の追跡、身分偽装、個人情報集約の手順を含めません。第24章の詳細な公開情報調査も重複しません。

## 学習目標

この章を終えた読者は、次を行えます。

1. 収集方法をPassive / Active / Authenticatedに分類し、実際の作用と照合する。
2. 第三者情報の所有、利用条件、機微性、時点を分けて取扱いを判断する。
3. Source、候補Asset、Confidence、Verification、Gap、次Actionの承認要求を持つAttack Surface Registerを作成する。

## 前提知識

第2章のAuthority / Scope / Safety / Disclosure、第4章のAsset / Boundary / Evidence、第9章のRoEと再承認を前提にします。DNSの設定や証明書発行の実装経験は必要ありません。本章で扱う名前は予約値、資料は作成者が記述した完全合成データです。

[完全合成Case](../cases/ch10-attack-surface-example.md)は`CASE-2026-001`をrefineします。`ASR-2026-010` / `CR-ASR10-001`を新設し、親`DR-2026-001`や`TM-2026-001`を置換しません。第11章の`CASE-2026-011`は独立Caseであり、発見結果を無根拠に結合しません。

## 10.1 発見を判断要求へ戻す

Reconnaissanceは後続判断のために対象と関係を理解する活動、OSINTは公開情報を要求に沿って評価・分析する活動、Asset Discoveryは資産候補を識別する活動として整理します。これは本書の教育用整理であり、三語を同義語として扱う定義ではありません。WSTGのInformation Gatheringは評価項目を考える分類の補助で、対象に対する許可や調査の完全性を証明しません。`SRC-WSTG-001`

本章のCollection Requirementは「供給資料内のどの候補を親Assetへ結べるか、何のEvidenceと承認が不足しているか」です。「関連する情報をすべて集める」ではありません。確認する属性、必要なSource、収集を止める条件を先に定義します。

図F-10-01: 候補発見から承認不足の記録まで（本書の教育用整理）。

```text
Decision / Collection Requirement
  → Authority / Legal / Terms boundary
  → Collection class / actual action
  → Source / Provenance / Timestamp
  → Candidate / Ownership confidence
  → Exposure / Dependency / Third party
  → Verification / next-action approval
  → Evidence / Gap / Owner / Reassessment
```

Attack Surface Registerは脆弱性一覧ではありません。URL、Package名、SaaS名が載っただけでFindingを発行せず、Exposureも実測していなければ`not-measured`と記録します。否定的な結果も「九つの供給資料では確認できない」という範囲に限定し、存在しないと断定しません。

## 10.2 公開と許可を分ける

公開閲覧可能であること、利用規約、robots、第三者の権利、個人情報の扱い、Assessmentの許可は別々の確認項目です。robotsの記述を適法性の自動保証にも、一律の法的禁止の判定器にも使いません。不明点を技術操作で埋めず、Authority ownerまたはData ownerへ戻します。Berkeley Protocolも調査の法的枠組みを文脈に応じて検討しますが、本章はその人権・国際刑事調査の文脈を企業活動の普遍的義務へ移しません。`SRC-BERKELEY-001`

security.txtは脆弱性報告の連絡情報などを機械可読にする仕様です。そのファイルの存在・不在自体からテストの許可・禁止を推定しない点を確認します。別のPolicyに示された条件と、個別対象に対するAuthorizationは別途評価します。連絡先が分かることは検査開始の承認ではありません。`SRC-SECURITYTXT-001`

親`AUTH-CASE-2026-001`の有効期限は2026-08-19T09:00:00Z、元のTest windowは2026-08-06T00:00:00Z〜08:00:00Zです。本章の基準時点2026-09-14には失効しています。`ROE-2026-009 v1`はDraft / Do not proceed / executionAuthorized=falseのままです。三つのRoE Objectに新しい候補DomainやPackageを加えません。出版や所有確認の成功で許可を更新しないことが、このCaseの中心的な停止条件です。

## 10.3 Collection classと実際の作用を照合する

表T-10-01: Collection classの教育用区分と本演習の制限。

| Class | 区分する観点 | 必要な確認 |
|---|---|---|
| Passive | 対象への能動的な試験を伴わず既存資料を検討する | 利用先・利用条件・Data・時点。第三者サービスへの照会も無条件に許可されない |
| Active | 対象へ新しいRequest等の作用を与えて情報を得る | 対象・Operation・作用量・時間・停止を含む個別承認 |
| Authenticated | 認証された権限やExport機能を使って取得する | Accountの正当性だけでなくData・目的・第三者条件・Scope |

一般的なPassiveという呼称は、すべての通信がゼロであることを意味しません。**本演習のPassive planはそれより狭く、提供済みファイルの読解だけ、外部通信・認証試行・Rate testはすべて0**です。通常の分類を本演習の許可リストへ置き換えません。

分類は自己申告だけでは成立しません。Passiveと記入しながらNetwork requestを含める計画は本演習では拒否します。認証済みという理由で取得したDataを別目的に再利用する判断も自動化しません。ActiveとAuthenticatedの両方の性質がある実作業は、その両条件を確認する必要がありますが、本章の有限モデルでは実作業を組み立てません。

供給JSONの`originalCollectionClass`は、元の取得があったと仮定した場合の分類です。SaaS exportを読者がオフラインで読む操作は、読者によるAuthenticated collectionではありません。`First-party inventory`はSource classであり、第四のCollection classではありません。取得が実際に行われたことも、仮定のAccountを使えることも主張しません。

## 10.4 Sourceが証明する範囲を限定する

表T-10-02: 供給資料から読めることと残るGap。

| Source | 限定して読めること | それだけでは証明しないこと |
|---|---|---|
| First-party inventory / Owner statement | その作成時点・対象範囲での所有者の申告 | 現時点の実稼働、記述の真正性、Assessmentの許可 |
| DNS archive | 保存されたRRと観測時点 | 法人による所有、現在の到達性、廃止後の名前の状態 |
| Certificate Transparency | CertificateまたはPrecertificateに関する記録 | 現在の所有・Deployment・Production・Testing permission |
| Public code / Package | 記載された名前、依存関係、公開者の申告 | 同名組織との同一性、安全性、Dependencyの検査許可 |
| SaaS export | Exportに含まれたWorkspace等の申告 | 組織全体の網羅性、未掲載サービスの不存在 |

DNSのRRにおけるOwnerは、RRが存在するDomain名を指す技術用語で、法人の資産所有者ではありません。`retired.billing-bridge.example`というOwner名を企業所有の確認結果へ転記しません。`SRC-DNS-TERM-001`

TTLを現在性の単独の証拠にしません。serve-staleを扱う仕様は、権威Sourceから更新できない状況で期限を過ぎたDataを応答に使う場合を説明しています。「TTL経過で必ず消失した」「正のTTLなので新鮮」とは断定できません。本章はResolverの設定や実装適合性を検査しません。`SRC-DNS-STALE-001`

RFC9162はExperimentalです。Precertificateは発行の意図を示すもので、最終Certificateが発行されない場合もあります。したがって、供給CT metadataだけで現在の所有・稼働を確定しないのが本章の分析判断です。実際のブラウザのCT対応版やLogの完全性を検証したという意味ではありません。`SRC-CT-001`

公開Codeの同名Repositoryを既存Assetへ結合する前に、別組織という代替説明を残します。Owner不明のSaaSはShadow ITの仮説になり得ますが、未掲載だけで無断利用と断定しません。許可済みサービスのInventory登録漏れも代替説明です。

## 10.5 Provenance、時点、Hashを直接結ぶ

Source IDは資料を、Provenance IDはその出所と取扱いの記録を、Evidence IDは特定の比較結果を識別します。本章の`OSRC-ASR10-*`は合成収集資料のID、`SRC-*`は仕様等の参考資料IDです。両者を混同しません。

ART-19にはSource class、取得方法、元のInteraction、原典ID、派生元、観測時点、取得時点、Hashの対象、変換、Terms、Data分類、Custodian、制限を残します。複数のWebサイトへ複製された一つの原典を、独立した複数Evidenceとして数えません。Berkeley Protocolの取得情報・保持・検証の考え方を参考にしますが、本章は供給資料の最小記録に限定します。`SRC-BERKELEY-001`

供給bundleの`content`は作成者による短い合成文です。`contentSha256`は、対応するその文字列をUTF-8にしたbyte列のSHA-256であり、囲んでいるJSONファイル全体のHashではありません。改行・空白の正規化は行いません。Hash一致が確認するのは固定教材との内容一致であり、実収集、Sourceの真正性、法的証拠能力、署名の有効性ではありません。

時刻も作成者が与えた仮定です。`observedAt ≤ acquiredAt ≤ asOf`を検査しますが、時計同期を測定したことにはなりません。Caseの確認期限は今回のレビュー用であり、親Decision Requirementの過去の期限を更新しません。

## 10.6 所有ConfidenceとVerificationを分離する

表T-10-03: 五つのVerification stateと許容結論（本書の有限教育モデル）。

| State | 許容する結論 | 自動的には進めないこと |
|---|---|---|
| Candidate | 要求に関係する候補として記録した | 自社所有・現稼働への確定 |
| Corroborated | 独立した原典が特定の属性を補強した | 所有者が確認したという判断 |
| Owner confirmed | 明示した所有者の申告と対象IDを供給資料内で照合した | 次Actionの実行承認 |
| Rejected | 当該Caseの候補集合へ結ぶ仮説を退けた | Source記録の削除や不存在の一般化 |
| Unknown | 判断に必要な根拠が足りない | 空欄のままPass扱い |

所有関係は別欄のConfirmed owned / Unverified / Historical / Third partyで記録します。`Unverified`は第六のVerification stateではありません。ConfidenceのHigh / Medium / Lowも確率や真正性の保証ではなく、供給資料内の根拠に対する本章の評価です。

`CAND-ASR10-001`はInventoryとOwner statementが合致するため、教材内に限ってOwner confirmed / Highとし、親`ASSET-2026-001`へ結びます。このAsset参照はRoEの対象Objectへの追加ではありません。`CAND-ASR10-006`は二つの独立した合成申告がPackage名を補強しても、所有者はUnverifiedのままです。

## 10.7 次Action、Gap、Handoffを記録する

確認済み候補であっても、次の実作業には現在有効なAuthorization、対象・Operation・時間のScope、System/Data owner、第三者条件の確認が必要です。本Caseはすべて`record-only`、`nextActionAuthorization=false`です。第三者Assetや所有不明Assetに、親の許可を継承させません。

各候補にEvidence ID、Gap ID、Gap owner、期限、Reassessment ID、無効化条件を付けます。新しいSource、所有者、時点、AuthorityのEvidenceが届いたら再評価し、前の判断を無記録で上書きしません。十分な限定結論とGapが残れば記入作業は完了できますが、実作業は停止したままです。

`HOF-ASR10-001`は教材内でOwner confirmedの候補一件とそのProvenanceを第12〜13章の計画入力にします。未確認候補を確認済み一覧に混ぜません。`HOF-ASR10-002`は全候補の原典関係、変換、Confidence、Gapを第23〜24章へ渡す計画です。両方ともplanned-not-deliveredで、実収集の依頼や実行許可ではありません。

## 10.8 完全合成演習と評価基準

**Purpose:** 九つの供給Sourceから六つの候補を比較し、所有確認、原典の独立性、次Actionの不足条件をART-19へ記入します。発見件数や通信成功は評価しません。

**Prerequisite / Authority / Scope:** [Case](../cases/ch10-attack-surface-example.md)、[Register JSON](../cases/fixtures/ch10-attack-surface.json)、[Source bundle JSON](../cases/fixtures/ch10-source-bundle.json)を用意します。実対象や実Dataで代替しません。以下の任意の整合性検査は本書Repositoryで、[出版基盤](../CANONICAL_SOURCE.md)の固定依存が導入済みの場合だけ実行します。新しい依存取得や外部Targetの照会は演習に含めません。JSON Schemaは二つのファイルを`register`と`bundle`に束ねた論理入力を定義し、Checkerが固定pathから読みます。

**Expected evidence:** 六候補それぞれのSource→Evidence→Gap→Owner→再評価と、二つのHandoffが記入されることです。任意検査の成功表示も実対象の許可や観測ではありません。Caseと二JSONの全Field一致、Source内容の固定Hash、三Collection classes、五Verification states、未承認の次Actionを検査します。

**Impact / Stop / Cleanup:** 操作は教材の読解・照合・限定要約だけで、外部通信・認証試行・Rate testは0です。九Source・六候補、要約65,536 bytes、30分を教育上の上限とします。未知のData、個人情報、Credential、通信要求、Hash不一致、Scope不明を認めたら追加処理と複製を止め、参照IDとGapを記録します。作業後は自分が作った教材用コピーだけを確認して除去し、正本と他者のDataを除去しません。保持の仮定は作業終了から24時間以内、CustodianはSYNTH-EVIDENCE-CUSTODIANです。これは実装済み隔離・削除・PII完全検出の保証ではありません。

```bash
python3 scripts/check_chapter10_contract.py --no-regressions
```

1. Caseを見る前に、二JSONからSourceと候補の対応表を作ります。元の取得Interactionと今回の読解操作を別欄へ記入します。
2. CT二件の原典IDを比較し、独立した裏付けの数を数え直します。古いDNS、同名別組織、Owner不明SaaSの代替説明を残します。
3. 各候補のVerification、所有Confidence、許容結論、Gapを埋めます。Owner confirmedも実行承認へ昇格させません。
4. 完全記入Caseと照合し、誤った結合や根拠不足を説明します。許可が不足していることを成果物の未記入と混同しません。

表T-10-04: 誤判断と修正の対比。

| 誤判断 | 反証・失敗の確認 | 修正後の記録 |
|---|---|---|
| CT二サイトに掲載されたので所有確認済み | 同じPrecertificateの派生コピーだった | Candidate / Unverified、原典一件、所有Gap |
| 古いDNS名を現在の資産へ統合する | 過去の廃止記録で現在状態が不明 | Unknown / Historical、再確認担当と期限 |
| 同名Repositoryを親Assetへ結ぶ | 別組織の申告がある | Rejected、第三者関係とSourceを保持 |
| Owner confirmedなので実作業を開始できる | 親Authority失効・新候補はRoE対象外 | record-only / 未承認、再承認要求 |

表T-10-05: ART-19 Rubric（各項目0〜2点、教育用）。

| 項目 | 0点 | 1点 | 2点 |
|---|---|---|---|
| 収集境界 | 呼称だけで許可 | 区分はあるが実作用が不明 | 元Interactionと今回の作用・停止を説明 |
| Source / Provenance | 出所または時点がない | 記録はあるが派生元が不明 | Hash対象・変換・原典独立性・限界を追跡 |
| 所有・検証 | 発見を所有確認と同一視 | Stateだけを記入 | Confidence・代替説明・反証を分離 |
| 承認・Handoff | 次Actionを自動許可 | Gapはあるが責任者がない | 未承認・Gap・Owner・期限・限定Handoffが一致 |

合計点だけで受入を判断しません。実対象の使用、第三者への実作業許可、失効した親の昇格、個人情報集約が一つでもあれば停止・差戻しです。満点も資格、法的適法性、実務能力の保証ではありません。

### 四つの実務視点

Assessment担当は「次の確認問い」を、Asset ownerは「所有とInventoryの根拠」を、Data/法務担当は「利用条件と第三者・機微性」を、意思決定者は「許容結論・Gap・期限」を確認します。同じ表を使っても判断責任を代替しません。

## 章のまとめ

ReconとOSINTの成果は情報量ではなく、要求に対してどこまで言えるかです。収集方法、Source、原典、時点、所有Confidence、Verification、実行許可を分離すると、誤ったAsset結合とScope拡張を防ぐ判断記録になります。本章の完成したART-19は、実作業を許可せずGapを残す成果物です。

## 次に学ぶこと

[第11章 Web/API](11-web-api-hypothesis.md)では、独立した合成Caseで仮説とEvidenceの関係を確認します。そのCaseへ本章の候補を自動投入しません。第12〜13章へは限定したAsset候補と承認不足を、第23〜24章へはCollection RequirementとProvenanceを引き継ぎます。後続の本文は各章のIssueで順次整備します。

## 参考文献・Source Note ID

- `SRC-BERKELEY-001`: Berkeley Protocol 2022。取得・保持・検証と文脈依存の法的枠組みへ限定。
- `SRC-WSTG-001`: OWASP WSTG 4.2。Information Gatheringの分類補助。5.0はdevelopment。
- `SRC-CT-001`: RFC9162、Experimental。Certificate / Precertificateの区別。
- `SRC-SECURITYTXT-001`: RFC9116、Informational。security.txtとTesting permissionの分離。
- `SRC-DNS-TERM-001`: RFC9499、BCP219。DNS RR Ownerという用語のみ。
- `SRC-DNS-STALE-001`: RFC8767、Standards Track。TTLとserve-staleの限定説明。

確認した版・節・Errata・採否・限界は[第10章Source Review Note](../references/ch10-source-review-2026-09-14.md)、Registryは[Source baseline](../references/reference-baseline.md)を参照してください。
