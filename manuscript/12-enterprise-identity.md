# 第12章 Enterprise Identityとアクセス経路を評価する

## この章の位置付け

管理者にMFAが設定されていれば、その管理者を起点とする権限上の問題は解消したと言えるでしょうか。認証が強くても、不要な権限や承認されていない委任が残ることがあります。逆に、Graphに線が一本描かれていても、その関係が現在成立するとは限りません。

本章はIdentityと権限関係を[ART-20 Identity Attack Path Review](../templates/identity-attack-path-review.md)へ整理します。実Credentialを扱わず、供給された完全合成Graph、設定Snapshot、Policyの有限比較、合成Eventから、説明できる範囲と残るGapを記録します。経路数や認証成功数は成果指標にしません。

### OWN / BRIDGE / DELEGATE

- **OWN:** 四つのPrincipal class、権限Graph、必要条件、六つのPath state、EvidenceとTreatmentを直接IDで接続します。
- **BRIDGE:** 第4章Threat Model、第6章Signal Flow、第9章RoE、第10章の候補Asset、第11章のAuthN/AuthZの区別を使い、第13〜17章へ不足条件を渡します。
- **DELEGATE:** Kerberos、OAuth、OIDC、SAMLの実装と製品固有設定は[実践 認証認可システム設計](https://itdojp.github.io/practical-auth-book/)へ委譲します。専門書から戻ったら、Protocol名ではなく主体・Resource・Action・条件・EvidenceをART-20へ記入します。Credential取得、再利用、横展開の手順は本演習に含めません。

## 学習目標

1. Human、Device、Service、WorkloadのIdentityと権限関係を図示できる。
2. 認証の強度、認可の正しさ、委任、Federation、評価実施の許可を分離できる。
3. 安全な成立性確認を設計し、根拠・観測不足・Treatmentを持つIdentity Attack Path Reviewを作成できる。

## 前提知識

[第4章](04-assets-boundaries-threat-model.md)のAsset / Boundary、[第6章](06-observable-systems.md)の認可と観測、[第9章](09-engagement-roe.md)の停止条件、[第11章](11-web-api-hypothesis.md)の認証と認可を前提にします。実Tenant、Directory、Account、Token、Cookieは必要ありません。

[完全合成Case](../cases/ch12-identity-path-review-example.md)は`CASE-2026-001`をrefinesする教育用補足`IAR-2026-012`です。第11章の`CASE-2026-011` / `ROE-2026-011`は独立で、Evidenceや許可を借用しません。

## 12.1 判断要求と親の停止状態

判断要求は「供給された権限関係のどこまでを説明でき、何の許可と観測が不足するか」です。**確認事実（教材内）**は、同梱レコードに書かれた四Principal、十四Edge、六Pathとその比較条件です。これは実測されたIdentity inventoryではありません。

**仮定**として、請求書連携OAuth App、Workload identity、管理Role、顧客Data APIのsummary面、Audit readerを持つ架空の構成を置きます。**分析判断**は、認証強度だけで権限経路を閉じず、必要条件と観測不足を個別に管理することです。代替説明は正常な変更、資料の遅延、用途の異なるIdentityの混同です。確信度は中とし、資料のない休眠利用・Device bindingについては低とします。実環境への一般化はしません。

親`DR-2026-001`の歴史的判断期限2026-07-22T00:00:00Zと`TM-2026-001`のNeeds Evidenceを保持します。`AUTH-CASE-2026-001`は2026-08-19T09:00:00Zで失効し、元のTest windowは2026-08-06T00:00:00Z〜08:00:00Zです。基準時点2026-09-15の`ROE-2026-009 v1`は **Draft / Do not proceed / executionAuthorized=false** のままです。

三つのRoE Objectへ本章のPrincipalやResourceを追加しません。第10章の`CAND-ASR10-001` / `ASSET-2026-001`は背景を結ぶIDであり、所有確認から実行許可は導きません。合成レコードを読む教材上の作業と、親の実施計画を開始することは別です。

## 12.2 PrincipalとLifecycleを分ける

表T-12-01: 本教材の四分類。製品標準の排他的な分類ではなく、責任を明確にするための呼び分けです。

| Class | 本教材での意味 | 確認する関係 |
|---|---|---|
| Human | 人の職務を表す合成Principal | Owner、在籍・休眠、Role、MFA例外の承認と期限 |
| Device | 端末のIdentityを表す合成Principal | 利用者との関連、端末状態、bindingの根拠 |
| Service | 継続するAudit参照機能のPrincipal | 機能Owner、必要権限、運用と変更の責任 |
| Workload | 請求同期という実行単位のPrincipal | Appとのbinding、実行単位のLifecycle、委任範囲 |

サービス名、App registration、実行Instance、Principal IDは同一ではありません。Deviceの健全性も、利用者の権限をそのまま証明しません。NIST SP 800-207Aが人に加えてApplication / Service identityを扱う点を、この区別の補助にします。本章の四分類を同資料の規範分類として引用しません。`SRC-NIST-ZTAA-001`

LifecycleとRoleを別欄にします。休眠という属性は「最近使っていない」という仮定を示しても、Grantが削除された証拠にはなりません。退職・廃止・Owner変更の手続と実際の権限状態を照合する問いを残します。

## 12.3 認証、認可、評価許可は別の問い

NIST SP 800-63-4はIdentity proofing、Authentication、FederationのAssuranceを区別します。対象範囲は自然人を中心とし、機械間認証や主体に代わるAPI利用等を明示的には扱いません。本章のWorkloadやDeviceへ、そのままIAL / AAL / FALへの適合を割り当てません。`SRC-NIST-DIGITAL-001`

SP 800-63A-4のIdentity proofingは、オンラインの主体と実在する自然人を一定の確かさで関連付ける過程です。架空のPrincipal IDにそれらしい名前があるだけでは、その過程を実施したことになりません。本教材のAssurance contextはすべて未評価です。`SRC-NIST-PROOFING-001`

表T-12-02: 分離して記録する問い。

| 問い | 必要な根拠 | 根拠を代用できないもの |
|---|---|---|
| Authentication | 主体とAuthenticatorのbinding、認証過程の条件 | Role名、MFAの有効フラグだけ |
| Authorization | Principal、Resource、Action、Policyと適用条件 | 認証成功、管理者という表示名 |
| Federation | 信頼するIssuer、Audience、受入側、検証責任 | SSOを導入したという説明だけ |
| Assessment authorization | 現在有効な許可、対象・作用・時間、停止と責任者 | 上記三つの技術的な成功 |

SP 800-63B-4ではAALは認証過程の強度を扱います。AAL2はphishing-resistantな選択肢を提供し、AAL3はその耐性を要求します。MFA一般とphishing resistanceは同義ではなく、手入力のOTP等を耐性の証明にしません。これらは認可Policyの正しさを保証する条件でもありません。`SRC-NIST-AUTHN-001`

本CaseのHumanはMFA Enabledですが、例外と管理Roleの残存を別に記録しています。EnabledをBrokenへ変換せず、例外の対象・期限・承認Evidence、必要な業務権限を問い直します。WorkloadにはHumanのMFA要件を機械的に流用しません。

## 12.4 Graphの線を必要条件へ変換する

図F-12-01: 権限関係と判断の接続（本書独自の概念図）。

```text
Decision Requirement / RoE
  → Principal / class / Owner / Lifecycle
  → Membership / Delegation / Federation / Trust
  → Role → Permission → Resource / Control plane
  → necessary conditions / supplied evidence
  → Path state → Telemetry / Finding / Treatment
  → Gap / Owner / Reassessment
```

図は侵害の順序ではありません。入力は合成設定、出力は条件付きの判断記録です。線が現在成立するか、どの境界を越えるか、何が不足しているかをIDで読むための図です。RoleからPermission、PermissionからResourceへ続く対応が途切れれば、経路の成立を主張しません。

Membershipは所属やRole割当て、GrantはRoleとPermissionの関係、AccessはPermissionとResourceの対応です。DelegationはあるPrincipalへ行為の範囲を委ねる関係として扱います。委任元・委任先・対象・Action・条件を残し、委任先が任意の権限を持つとは考えません。Impersonationという製品用語を使う場合も、誰として評価されるかと誰が承認したかを分離し、本章では実装しません。

Toxic combinationは、個々のRole名が危険という断定ではありません。同じ主体が同じResourceについて、相互承認を崩す複数のPermissionを持つなどの条件付き仮説です。本章の六Pathは全組合せを探索せず、未列挙経路のGapを残します。過大権限は業務上必要な範囲との比較で判断し、権限数の多さだけでは決めません。

## 12.5 FederationのIssuer、Audience、受入側

Issuerは主張を発行する側、Audienceはその主張が意図する受入側、Relying party（RP）は主張を検証して利用する側です。同じ文字列欄へ混ぜると、誰を信頼し、誰向けの主張を受け入れたかが分からなくなります。

SP 800-63C-4のIdP発行Assertionでは、IssuerとAudience、時刻・有効期間、署名等の責任を分けます。全FALでRPは自分がAudienceに含まれることを確認し、単一Audienceへの制限はFAL2以上で要求されます。本教材の単一Audienceの比較を、FAL1にも常に一つだけという規範へ拡張しません。`SRC-NIST-FEDERATION-001`

OAuthのAccess tokenと、RPへ認証情報を伝えるAssertionも同じ用途ではありません。RFC9700の§2.3は、必要なPrivilege、Resource、Action、Audienceへの制限を扱います。本章ではResource/Actionを明記する判断に限定し、実Tokenの発行・解釈・署名検証は実装しません。`SRC-IETF-OAUTH-BCP-001`

図F-12-02: 本教材のFederation条件の読み方。

```text
supplied Issuer ID ── matches trusted Issuer ID?
supplied Audience ID ── matches intended RP ID?
receiving RP ID ── matches Resource's RP ID?
  → all required bindings known and matched
  → only this authored path's finite comparison
```

実装すべきProtocol検証の完全な一覧ではありません。署名、鍵配布、時刻、失効、Replay防止などを実装済みと主張せず、供給された識別子の比較だけに限定します。Workloadの例への適用も本書の教育用モデルであって、SP 800-63Cの機械間認証への適合認証ではありません。

## 12.6 Path stateとEvidenceの上限

表T-12-03: ART-20の六状態。本書の有限契約であり、六段階の成熟度ではありません。

| State | 必要な根拠 | 言えないこと |
|---|---|---|
| Hypothesized | 主体・権限・Resource・必要条件を持つ仮説 | 現在の設定や利用が確認済み |
| Config-confirmed | 同じGraph版と必要Edgeを指す設定Evidence | 実際に利用された、Validatedである |
| Evidence-supported | 同一Path・版・主体・Resource・Actionの合成Event | 実認証の成功、全期間の観測性 |
| Validated | 同一版・入力条件・期待値・再計算値を結ぶ有限比較 | 親Controlや実環境の検証完了 |
| Broken | このPathに必須の条件の反証と、それを示す同一Pathの比較 | ほかの経路や侵害の不存在 |
| Unknown | 必要条件やbindingを確定できない | 安全、Allow、正常の証明 |

**Static review**は設定の参照を確認するだけで、Validatedへ進めません。**Policy simulation**は供給された必要条件の有限比較です。**Synthetic replay**は作成者が記述したEventのFieldを照合する意味で、認証要求やSessionを再送する処理ではありません。

このモデルの各Pathは、必要条件の論理積です。既知の否定条件があればそのPathを反証できます。否定条件がなく必要条件が不明ならUnknownです。すべての条件が既知で一致しても、同じPath・Graph版・Policy版・入力・Evidenceと期待値の組がなければValidatedにはしません。MFAは条件の代用品ではありません。

六つの記入例は、休眠Grantの仮説、MFA例外の設定確認、Audit readerの合成Event、Federation条件の有限一致、必要なDelegation承認の否定、Device binding不足です。四番目のPassでも、親`TB-2026-004`や`SF-2026-006`のcurrent binding / CoverageはUnknownのままです。

## 12.7 Telemetry、Finding、Treatmentへ渡す

第6章のProduced / Collected / Retained / Queryable / Validated / Unknownは観測経路の状態です。ART-20のPath stateとは別欄にし、同じValidatedという綴りだけでEvidenceを移しません。

各PathにTelemetry ID、Detection ID、Finding ID、Gap、Owner、期限、Reassessmentを付けます。必要FieldはPrincipal、Resource、Action、Graph/Policy版、Outcome、Event time、相関IDです。実Secretを相関keyにしません。Findingは教材内の分析で、Detectionはplanned-not-testedと明記します。Eventがない場合は、未発生以外に未収集、期限切れ、Field欠落、検索権限不足を比較します。

表T-12-04: 次章への計画入力と受入条件。

| 受入先 | 渡すもの | 受入時に残す制限 |
|---|---|---|
| 第11章 | AuthN/AuthZ、Resource/Action、条件の区別 | 独立CASE-2026-011へEvidenceや許可を移さない |
| 第13章 | WorkloadとControl planeのOwner、binding Gap | 製品操作やDeployment許可ではない |
| 第14章 | 一つの必要条件、反証、最小Evidence、停止 | 実施には新しい許可とScopeが必要 |
| 第16章 | Field、期間、相関key、Collection/Retention Gap | 観測済みと未観測を混ぜない |
| 第17章 | 合成Test計画と許容結論 | Ruleの実装・実検知率の検証済みとはしない |

Handoffはすべてplanned-not-deliveredです。将来の担当者が入力ID、版、Gapを確認した受領記録を作るまで、完了へ変更しません。TreatmentはRole縮小、例外の再確認、観測改善などの計画であり、実変更の指示ではありません。

## 12.8 安全な分析課題

**Purpose:** 六Pathについて、根拠が示す範囲と示さない範囲をART-20へ記入します。まずMFA EnabledだけでBrokenにできるか、Static reviewだけでValidatedにできるかを予想し、Caseで反証します。

**Prerequisite / Authority / Scope:** [Case](../cases/ch12-identity-path-review-example.md)、[合成JSON](../cases/fixtures/ch12-identity-paths.json)、[閉じたSchema](../schemas/ch12-identity-paths.schema.json)だけを用意します。実Credential、実Tenant、実Directory、実Account、実Token、実Cookieは使用しません。任意の検査は本書Repositoryで[出版基盤](../CANONICAL_SOURCE.md)の固定依存が導入済みの場合だけ行います。依存取得と外部通信は演習に含めません。

**Expected evidence / Impact:** 出力はPath ID、必要条件、Evidence ID、State、反証またはGap、Owner、再評価条件です。任意コマンドはローカル教材の整合性だけを検査し、実認証、通信、許可発行は0です。本文表示を得る共有rendererも固定依存を使います。

**Stop / Cleanup:** 不明な入力、実Dataらしい内容、外部接続の必要性、許可・境界の不一致を見つけたら追加の調査をせず停止します。検査失敗時は公開を止めます。自分で作成した作業コピーだけを整理し、正本・親記録・Evidence参照を変更しません。想定要約の上限は65,536byte、30分、保持は作業終了から24時間以内とし、実際の削除や隔離成功を検査結果から推定しません。

```bash
python3 scripts/check_chapter12_contract.py
```

1. Caseを見る前の予想を残し、四PrincipalとLifecycleを区別します。
2. Edgeの始点から終点をたどり、Role、Permission、Resource、境界を照合します。
3. 設定・Event・比較結果が同じPathと版を指すことを確認します。
4. 必要な委任承認がFalseの場合と、Device bindingがUnknownの場合を比較します。
5. Issuer、Audience、受入RPを交換したら何が反証になるか、実Tokenなしで説明します。
6. ART-20へStateの根拠、代替説明、Confidence、Gap、Treatment、Handoffを記入します。

Schemaは供給された有限教材の語彙と閉じたFieldを定義します。未知の値用Fieldや未登録文字列を受け入れないためのもので、任意の実Secretを識別する検知器でも、学習者の自由なGraphを採点する一般製品でもありません。

## 作成する成果物と評価基準

[ART-20 Template](../templates/identity-attack-path-review.md)はJSONなしでも記入できます。ID、Class、認証Context、Role/Permission、Edge、Resource、必要条件、検証方法、Evidence、Telemetry、Finding、Risk/Treatment、Owner、Reassessmentを残します。Unknownでも不足条件と責任者が説明できれば有効な成果物です。

表T-12-05: 各項目0点（欠落）、1点（対応が曖昧）、2点（直接追跡できる）のRubric。

| 観点 | 2点の条件 |
|---|---|
| 主体と権限 | 四分類、Lifecycle、Role/Permission/Resourceを分ける |
| 境界と許可 | Issuer/Audience/RPと実施許可を混同しない |
| 状態とEvidence | 同一Path・版・必要条件を根拠にし、反証とUnknownを分ける |
| 判断の限界 | MFA・Event・有限Passを実環境や親の安全へ一般化しない |
| 引渡し | Telemetry/Gap/Owner/期限/Treatment/Reassessmentを接続する |

8点以上を教材の目安とします。ただし実Data混入、実行許可への昇格、根拠のないValidated/Broken、親記録の無断変更が一つでもあれば、点数に関係なく差し戻します。資格や実業務能力の認定ではありません。

## よくある誤解

- MFA Enabledは、不要なRoleや委任の問題を取り除いた証拠ではありません。
- Dormantは、権限が取り消された状態でも、悪意の証拠でもありません。
- Graphの線、設定、合成Event、実際の利用は別々の根拠を持ちます。
- Brokenは特定の必要条件の反証です。未知の別経路まで安全とは言えません。
- 素材のHash一致、CIの成功、出版の完了は、親RoEの更新や実施承認ではありません。

## 章のまとめ

Identity評価では、誰が、何に、どのActionを、どの条件で許されるかをGraphとEvidenceで説明します。認証の強度、認可、Federation、実施許可を分け、必要条件の不明を隠さず、反証と観測不足を区別します。最終成果は経路数ではなく、判断と再評価へ接続したART-20です。

## 次に学ぶこと

第13章ではWorkload / Platform / Supply Chainへ責任境界を広げ、第14章では必要条件一つに対する最小影響の確認、第15章ではFindingと再評価へ進みます。第16章の観測要件と[第17章](17-detection-engineering.md)のDetection検証へ不足Fieldを渡します。未公開章へのリンクは作らず、[全体目次](../TOC.md)で位置を確認します。

## 参考文献・Source Note ID

[第12章Source Review Note](../references/ch12-source-review-2026-09-15.md)に採用箇所、版、Status、確認日、限界を記録します。

- `SRC-NIST-DIGITAL-001`: SP 800-63-4、自然人を中心とする範囲とIAL/AAL/FALの分離。
- `SRC-NIST-PROOFING-001`: SP 800-63A-4、Identity proofingの目的と自然人の範囲。
- `SRC-NIST-AUTHN-001`: SP 800-63B-4、Authentication assuranceとphishing resistance。
- `SRC-NIST-FEDERATION-001`: SP 800-63C-4、IdP発行AssertionのIssuer/AudienceとRPの責任。
- `SRC-IETF-OAUTH-BCP-001`: RFC9700 / BCP240、必要なPrivilege、Resource、Action、Audienceの制限。
- `SRC-NIST-ZTAA-001`: SP 800-207A、Application / Service identityを区別する根拠だけ。
