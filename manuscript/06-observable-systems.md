# 第6章 通信・Identity・Cloudを観測可能なシステムとして読む

## この章の位置付け

第4章のAssetとTrust Boundary、第5章のBehavior Mapを、「どこで何を観測できるか」へ接続する。信号の流れ（Signal Flow）は製品構成図ではなく、操作、認可、状態変化、Event、収集、判断の依存関係を説明する図である。本章の成果物は`ART-16 Signal Flow Diagram`である。

**OWN**は操作からEvidenceまでの追跡、観測状態の分離、Gapと許容結論の記録である。**BRIDGE**は第4章の境界、第5章の行動、第12〜13章のIdentity・Platform、第16〜17章のTelemetry・Detection、第20章のEvidenceである。

**DELEGATE**として、Protocolの実装は[実践 認証認可システム設計](https://itdojp.github.io/practical-auth-book/)、基盤設定は[インフラセキュリティ実装ガイド](https://itdojp.github.io/it-infra-security-guide-book/)へ委譲する。委譲先では認証方式や収集設定の条件を確認し、本書へ戻ってDecision point、必須Field、GapをART-16へ記録する。委譲先を読まなくても、以下の合成記録の比較は完結する。

## 学習目標

- 操作とログを対応付けられる。
- 観測不能点を識別できる。
- Signal Flow Diagramを作成できる。

「ログがある」だけでなく、どの操作、主体、対象、期間について、何の判断まで許されるかを説明できれば到達である。

## 前提知識

HTTP、認証・認可、Cloud、Containerの概念と、第4章のAsset / Boundary、第5章のMappingと観測の違いを前提とする。OAuth要求の組立て、Cloudアカウント、SIEM、実ログは必要ない。演習は同梱の非実行JSONを読むS1の分析課題である。

## 導入ケース：同意変更を見つければ十分か

合成の請求書連携について、意思決定者は「連携の権限を見直す際、どの観測不足を先に解消すべきか」と問う。管理者同意の記録は存在する一方、Workloadの現在のIdentity bindingは未確認であり、Audit exportの一部は保持期間を過ぎている。

**確認事実（教材内）**は、同梱の受領記録に示されたEvent classと観測段階だけである。**仮定**として、管理面・顧客Data API・収集系を持つ架空の構成を置く。**分析判断**は「既往影響の不存在は結論できず、収集経路と期間の確認を先行する」である。代替説明は正常な変更、Export不備、保持期限切れであり、悪意を仮定しなくても欠落は説明できる。

**確信度は中**とする。有限教材内の欠落条件は明示されるが、実環境と親Caseの過去期間を示すEvidenceはない。必要な対象期間・Field・Identityの対応が確認されれば、この判断を再評価する。**推奨**はGapごとにOwnerと期限を付けて引き渡すことであり、実環境への追加操作ではない。

## 全体像：操作と証拠は別の経路を通る

### F-06-01 Signal Flowと観測経路

次は本書独自の概念図である。左から操作の通過点を読み、後半で観測経路へ切り替わる。矢印は成立や成功の証明ではなく、次に確認すべき依存関係を示す。

```text
Actor / Workload → Identity / Credential class → Protocol / Request
→ Gateway / Control plane / Data plane → Authorization decision
→ State change / Data access → Event producer → Collection path
→ Normalization / Retention → Query → Evidence / Detection consumer
→ Gap / Decision / Reassessment
```

文章代替として、操作を認証主体と要求へ結び付け、認可と状態変化を分ける。そこからEvent producer、Collector、正規化、保存、検索へ追跡する。観測の根拠が切れる箇所はGapにし、最後の判断へ引き継ぐ。図の色や配置だけに意味を持たせない。

NIST SP 800-207はPolicy DecisionとEnforcement、Control planeとData planeを論理的に分離する。構成要素が同一製品に実装されても、その責任とEvidenceは同じではない。本章ではこの区別だけを借り、Zero Trust適合性や製品の安全性を認定しない。`SRC-NIST-ZTA-001`

## Identity・要求・状態変化を分離する

### T-06-01 Human / Workload / Serviceの比較

| 主体の扱い | 確認する結び付き | 観測上の注意 |
|---|---|---|
| Human | 合成人物Roleと管理操作の承認 | ログイン成功と変更承認を分ける |
| Workload | 実行単位と非人間Identityのbinding | 管理者の承認をWorkload自身の実行証拠にしない |
| Service | 継続する機能と、その実行Identity | Service名が同じでも実行Instance・権限が同じとは限らない |
| Device | 端末の状態と主体との関連 | 端末の正常性だけで利用者や処理を認可しない |

WorkloadとServiceは排他的な普遍分類ではない。本教材では、API要求を出す実行単位をWorkload、継続的なAudit export機能をServiceと呼び分ける。Deviceは実行環境の属性として説明し、独立した実行Flowは本教材では追加しない。NIST SP 800-207Aが扱うアプリケーション・Service identityは、人のIdentityだけでアクセスを説明しないための根拠である。`SRC-NIST-ZTAA-001`

OAuthのClient、Authorization server、Resource serverは別の役割である。Clientが自分のために行動する場合と、人の委任で行動する場合を混同しない。管理者同意の変更という製品上の操作を、OAuth仕様に共通するEvent名とみなさない。RFC 6749の役割とClient credentialsの説明だけを参照し、古いGrantの選択や実装推奨は本章では行わない。`SRC-IETF-OAUTH-CORE-001`

認証は「どの主体として扱うか」、認可は「その主体にこの要求を許すか」、Enforcementは「その判断を経路上で適用したか」という問いである。認可がAllowでも、処理失敗や後段拒否があれば状態は変わらない。変更成功も、監査Eventの収集成功を意味しない。

### Control / Data / Build Plane

管理者同意やDeployment設定はControl plane、顧客Data APIの利用はData planeとして読む。CI/CDは本章ではBuild planeという補助的な呼び名を使い、Source、Build identity、Artifact、Deployment承認の対応を確認する。Build成功を実行時の権限やData accessの証拠へ昇格させない。Build planeはNISTの必須分類ではなく、本書の説明上の分割である。

Containerを再作成しても論理Serviceは残り得るため、Service名だけでは実行単位を特定できない。Cloudの管理操作とAPI内部のData操作、Gatewayの応答と後段状態も別々に記録する。製品固有のAudit schemaやPod操作は第13章と専門書へ委譲する。

## Eventの段階と観測不能点

### T-06-02 Coverage statusの意味

本書のART-16で用いるStatusは次の六つだけである。これらは製品の標準用語でも、単純な成熟度の点数でもない。

| Status | この教材で必要な根拠 | それだけでは言えないこと |
|---|---|---|
| Produced | 指定Producerに同一Eventの生成記録がある | Collectorへの到達 |
| Collected | 指定Collectorの受領記録がある | 現在の保持と検索可能性 |
| Retained | 指定時点が保持区間内で、保存先の記録がある | 検索権限と必須Fieldの充足 |
| Queryable | 期間・対象・必須Fieldを満たす検索記録がある | 検知の有効性 |
| Validated | 同一Flowの有限Testが期待値と一致する | 実製品、親Case、過去全期間の有効性 |
| Unknown | 生成段階から根拠を確定できない | Eventや侵害の不存在 |

本章ではProduced、Collected、Retained、Queryableの根拠をそれぞれ保存する。Statusはその観測時点で根拠が連続している段階を要約するが、過去の収集記録は保持期限切れでも消去しない。Collectedの記録からRetainedやQueryableを推定せず、各段階の受領記録を照合する。正規化の有無は独立Fieldであり、七番目のStatusを増やさない。

NIST SP 800-92のログ管理は、生成・転送・保存・分析を支える基盤と運用を区別し、正規化、時刻差、保持、完全性を扱う。本章の六Statusはその引用ではなく、観測不足を説明するための教材契約である。2006年版の暗号アルゴリズムや製品例を現在の推奨へ転用しない。`SRC-NIST-LOG-001`

NIST SP 800-92 Rev.1は2026-09-12確認時点でInitial Public Draftである。改訂候補として追跡するが、Final規範として使わない。`SRC-NIST-LOG-DRAFT-001`

### 時刻・相関・変換の限界

Event time、収集時刻、Query時刻を別に保存し、UTC offsetとClock uncertaintyを残す。例えば同じClockでない二つの時刻が各±2秒の誤差を持ち、表示差が1秒なら、表示順だけで前後関係を確定できない。UTCへの表記統一はClockの正確性を回復しない。

Correlation keyは合成Event ID・Tenant・Application・Request IDの組として扱う。同じApplication名だけの一致は因果関係を証明しない。Raw TokenやCookieを相関keyに使わない。正規化前後のField名と変換版、欠落したField、保持期限を記録し、変換による情報損失を明示する。

Telemetryの分類は、第5章のATT&CK v19.2固定metadataとBehavior IDを継承する。Detection Strategyを参照できることと、必要Dataを実際に保有することは別である。新たなATT&CK対応付けや親MapのStatus更新は本章では行わない。`SRC-ATTACK-001`、`SRC-ATTACK-DET-001`

## 安全な分析課題

### Purpose / Prerequisite / Authority / Scope

目的は六つの合成Flowを読み、根拠のない昇格を拒否することである。前提は本章とART-16の読了、同梱JSONを表示できる環境である。Authorityは教材の読み取りだけを許す。Scopeは`read-only-synthetic-data`、完全合成Caseに限定する。実Credential、Token、Cookie、実Tenant、実Logは使用しない。外部Serviceへの要求送信と認証試行は禁止する。

### Expected evidence / Impact / Stop / Cleanup

期待Evidenceは、Flow ID、根拠のある段階、Gap、許容結論、Owner、期限を記入したART-16である。外部への影響はなく、実行する場合もRepository内JSONの読み取りだけで完結する。実データらしい内容、非合成の識別子、外部接続の必要性、意味の不一致を見つけたら停止し、教材管理者へ報告する。追加の調査操作は行わない。

Cleanupは、自分で作成した演習用コピーだけを整理することとする。正本とEvidence記録は変更しない。第三者Systemのログや設定を変更する課題ではない。

### 手順と反証

1. [完全合成Case](../cases/ch06-signal-flow-example.md)と[読み取り専用Dataset](../cases/fixtures/ch06-signal-flow.json)を開く。
2. FlowのActorからConsumerまで、Node IDとEdge IDでたどる。
3. 各段階のEvidence IDが同じFlow・Event・対象期間を指すか確認する。
4. 保持期限切れと未収集を区別し、Statusと許容結論を記入する。
5. WorkloadのUnknownを管理者同意の記録だけで埋められるか検討する。埋められない理由を記す。
6. 第16章へ必要Field・期間、第17章へTestの限定、第20章へClockと変換の制約を渡す。

悪い例は「Collectorに届いたので過去90日の侵害はなかった」である。反証は、Collectedの受領票があっても対象期間が期限切れでQuery記録がないFlowである。良い例は「教材の受領票はあるが、指定時点の検索可能性は示せない。保持GapをOwnerへ返す」である。

Repositoryの検査を実行できる場合は、固定依存の導入済み環境で次を使う。ネットワーク取得や実環境の観測は実行しない。

```bash
python3 scripts/check_chapter06_contract.py
```

成功は教材の有限構造・参照・表示・安全境界の整合を意味する。システムの監視性能を測った結果ではない。失敗時は正本の公開を止め、検査を回避せず、不一致を修正・レビューする。

## 作成する成果物

[ART-16 Template](../templates/signal-flow-diagram.md)へ、Case、親Behavior、Asset / Boundary、Actor / Identity、Protocol、認可、状態変化、Producer、Collector、正規化、保持、Query、Consumer、Gapを記入する。

親は`CASE-2026-001`、関係は`refines`、子記録は`SFM-2026-001`である。本章の受領票は独立した完全合成の教育用補足であり、親の改修結果、Control assurance、過去の観測不足を更新しない。StatusがUnknownでも、Gap、許容結論、Owner、期限、Reassessmentが揃えば成果物として提出できる。

## 評価基準

各項目を0点（欠落）、1点（IDまたは根拠が曖昧）、2点（直接追跡できる）で評価する。

| 観点 | 2点の条件 |
|---|---|
| 操作の追跡 | Actor、Identity、認可、状態変化を分ける |
| 観測段階 | 同一FlowのEvidenceで各段階を裏付ける |
| 時刻と保持 | Offset、誤差、期限、Query時点を判断に使う |
| 結論の限界 | 代替説明とGapを残し、不存在を断定しない |
| Handoff | Owner、期限、再評価条件と次章の入力がある |

合計8点以上を教材上の目安とする。ただし実Data混入、許可外操作、根拠のないStatus昇格、親Caseへの無断転用が一つでもあれば点数にかかわらず差し戻す。これは職業資格や実環境能力の認定ではない。

## よくある誤解

- Authentication successはAuthorization successでもState change successでもない。
- 暗号化通信が存在しても、Data accessの内容や認可結果をGatewayだけから確定できない。
- Event未検出は、指定した検索条件の結果である。生成、収集、保持、権限の欠落を調べる前に不存在へ一般化しない。
- QueryableはValidatedではない。合成TestのPassも親ControlのPassではない。
- 正規化は証拠を増やさない。失われたFieldと変換版を残す。

## 章のまとめ

Signal Flowは、操作の経路と観測の経路をIDで接続する。Identity、認可、状態変化を分け、生成・収集・保持・検索・検証を個別のEvidenceで確認する。観測不能点を隠さず、許容結論、Owner、期限、Reassessmentまで記録することが本章の完成である。

## 次に学ぶこと

第7章では、観測できる範囲と不確実性を保持したまま、脆弱性、露出、悪用可能性、事業影響を分けて優先順位を判断する。Identityの詳細は第12章、Cloud / Container / CI/CDは第13章、Telemetry要件は第16章、検知検証は[第17章](17-detection-engineering.md)、証拠と時系列の再構成は第20章へ接続する。未公開章へのリンクは作らず、[全体目次](../TOC.md)で位置を確認する。

## 参考文献・Source Note ID

本章の採用箇所、版、Draft区分、確認日、除外範囲は[第6章Source Review Note](../references/ch06-source-review-2026-09-12.md)にまとめる。

- `SRC-NIST-ZTA-001`: NIST SP 800-207。論理的な判断・強制・Planeの分離。
- `SRC-NIST-ZTAA-001`: NIST SP 800-207A。Application / Service identity。
- `SRC-NIST-LOG-001`: NIST SP 800-92。生成・転送・保持・分析の区別。
- `SRC-NIST-LOG-DRAFT-001`: NIST SP 800-92 Rev.1 IPD。改訂監視だけ。
- `SRC-IETF-OAUTH-CORE-001`: RFC 6749。役割とClient自身のIdentityの区別だけ。
- `SRC-ATTACK-001`: 第5章から継承するATT&CK v19.2の版と限定。
- `SRC-ATTACK-DET-001`: StrategyとData保有・検証の分離。
