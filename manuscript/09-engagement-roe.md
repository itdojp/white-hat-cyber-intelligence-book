# 第9章 Engagement DesignとRules of Engagement

## この章の位置付け

「実施してよい」という判断だけでは、担当者が何をどこまで行い、いつ止めるかは一意に決まりません。逆に、詳細な作業計画があっても、その対象に対する許可が存在するとは限りません。本章はDecision RequirementとAuthorization evidenceを、範囲・作用・時間・Data・停止・復旧・Evidence・完了条件を持つ **Rules of Engagement（RoE）** へ接続します。RoEは権限の発生源ではなく、確認済み権限より狭い実施条件です。

第2章の[Authorization Checklist](../templates/authorization-checklist.md)、第4章の[Threat Model](../templates/threat-model.md)、第8章の[Lab Safety and Evidence Plan](../templates/lab-safety-evidence-plan.md)を入力とし、既存の[ART-02 Rules of Engagement](../templates/rules-of-engagement.md)を完成させます。本章で行うのは供給された合成記録の読解と計画整合性の検査です。実システムへの操作や実行許可の発行は行いません。

### OWN / BRIDGE / DELEGATE

- **OWN:** 本書固有のART-02で、Decision Requirementから許可根拠、Scope、Method、Stop、Evidence、Reauthorizationへ至る直接IDと判断責任を説明します。成果物の記入、停止判断、後続章へのHandoffを本章だけで完結させます。
- **BRIDGE:** 法・倫理・許可・RoEという広いテーマの扱いは[CROSS_BOOK_MAP](../CROSS_BOOK_MAP.md)のBRIDGEを維持します。既存書籍へ進む前にも必要な入出力・判断・Evidence・責任を、本書固有の文脈に限定して残します。第2・4・8章からの継承と、第10〜15・21章への接続が対象です。
- **DELEGATE:** 個別事案の法的助言、契約書全文、業界固有規制、製品固有操作、脆弱性別の詳細手順は詳述しません。[Pentest学習書](https://itdojp.github.io/pentest-learning-book/)へ方法論の詳細を委譲します。委譲先の説明を読んでも、個別のAuthorization確認は省略できません。

NIST SP 800-115の計画項目は検討漏れを減らす補助です。Sourceにある手法が自動的に許可されるわけではありません。法の一般的な条文と個別の事実・契約・権限者の判断も区別します。`SRC-NIST-TEST-001` `SRC-JP-LAW-001`

## 学習目標

この章を終えた読者は、次を行えます。

1. Authorization evidence、RoE、Procedureの役割を分け、許可根拠と実施条件を直接IDで結ぶ。
2. Asset・Identity・Environment・Data・Operation・Timeの範囲を、明示的な対象外と対にして定義する。
3. 作用量、証拠取扱い、連絡、停止、復旧、再開の条件を確認可能な項目へ分解する。
4. 技術的な作業完了と、Decisionに必要なEvidenceの充足を別に判定する。
5. 条件不明・期限経過・Scope driftを検出し、Do not proceedとReauthorizationを記録する。

## 前提知識

第2章のAuthority / Scope / Safety / Disclosure、第4章のAsset / Trust Boundary / Threat Hypothesis、第8章の合成LabとEvidenceの限界を前提にします。第1章のCase Mapと、Decision Requirement・Information gap・Reassessmentの関係も確認してください。

本章のCaseは`CASE-2026-001`をrefineします。第2章内の`DR-AUTH-2026-001`と親の`DR-2026-001`は別の判断要求です。第1章の`ROE-2026-001`を上書きせず、本章では`ROE-2026-009`を使います。第11章の`CASE-2026-011` / `ROE-2026-011`は独立Caseのままです。

## 9.1 Authorization、RoE、Procedureを分ける

Authorization evidenceは、誰が、どの権限に基づき、何について、いつまで認めたかを検証するための根拠です。RoEはその根拠を、関係者間で共有できる実施条件へ具体化します。Procedureは条件内で成果物を得る作業順序です。この順序を逆にして、実施したいProcedureから許可の範囲を推定してはいけません。

表T-09-01: 三つの記録の役割（本書の教育用整理）。

| 記録 | 答える問い | 記録があっても証明しないこと |
|---|---|---|
| Authorization evidence | 許可者、対象、期間、制約を確認できるか | あらゆる手法や第三者Dataの利用が許可されること |
| RoE | 誰が、どの条件内で行い、何を理由に止めるか | 許可者の権限の真正性や法的適法性 |
| Procedure | 条件内で何を確認し、どのEvidenceを残すか | Scopeの拡張や失効した許可の更新 |

Sponsorは目的や予算を持つ役割、Authority ownerは許可根拠を確認する役割、System ownerとData ownerは対象とDataの責任を持つ役割です。同一人物が兼務する場合も、役割ごとの承認範囲を残します。署名の画像がある、Gitのレビューが通った、CIが成功したという事実だけでは、これらの権限を確認したことにはなりません。

不正アクセス禁止法の用語や禁止規定は確認対象ですが、条文の一般説明を個別事案への適法判断に置き換えません。所有者の同意、アクセス管理者の権限、Data利用条件、契約、第三者サービスの規約を分け、不明点は担当者へ戻します。本書の書面による許可確認は安全方針であり、あらゆる法令が同じ形式を一律に要求するという説明ではありません。`SRC-JP-LAW-001`

## 9.2 Decision Requirementと継承時点を固定する

RoEの冒頭には、Case、Decision Requirement、Decision owner、必要な判断、判断期限、Authorization Record、RoEのIDと版を置きます。過去の判断期限と今回の計画レビュー時点を混ぜないことが重要です。

本章の親`AUTH-CASE-2026-001`の記録は、歴史的には`Proceed with conditions`ですが、有効期限は **2026-08-19T18:00:00+09:00** です。合成Caseの作成基準時点2026-09-13には期限を過ぎています。第8章のSafeやCleanup verified、EvidenceのHash一致は、この期限を延長しません。

`ROE-2026-009`は項目を完全に記入した **Draft / Do not proceed** とします。空欄を隠した未完成例ではなく、実施を妨げる`GAP-ROE09-001`、責任者、次の再評価を記録した計画例です。新しいAuthorizationと判断期限が必要な場合は別の根拠とIDを用意し、親記録を改変せずに接続し直します。

親の元のTest windowは2026-08-06T09:00:00+09:00〜17:00:00+09:00です。有効期間内であっても、このWindowの外側へ無審査で移動しません。

親`DR-2026-001`の期限2026-07-22T09:00:00+09:00、`REA-2026-001`の2026-08-21、第4章`TM-2026-001`のNeeds Evidenceは保持します。本章の再評価予定は別の`REA-ROE09-001`です。Openの継続禁止条件を、後続計画が存在するだけでSatisfiedへ変更しません。

## 9.3 Scopeは対象外と既定拒否を含める

ScopeはDomainの一覧だけではありません。対象Asset、Identity、Environment、Data、Operation、時間、依存先を分け、正確な識別子で列挙します。未記載の対象は許可ではなく **既定拒否** です。Wildcardや「関連するすべて」のような表現を残すと、対象の追加時にScopeが無審査で広がります。

本章は同梱JSON内の`OBJ-ROE09-CONFIG`、`OBJ-ROE09-EVENT`、`OBJ-ROE09-POLICY`だけを対象にします。それぞれ合成OAuth設定、作成者が記述したEvent、方針Snapshotです。Eventの文章は実測Logではありません。EnvironmentとReader identityも教材用の識別子であり、接続先やログインAccountではありません。

表T-09-02: Scopeと不明時の判断（本書の教育用整理）。

| Scopeの観点 | 記入する内容 | 不明時の判断 |
|---|---|---|
| Asset / Object | ID、所有者、対象に含める理由 | 対象に加えずDo not proceed |
| Identity / Environment | 使用する役割、隔離された教材の境界 | 実Identityで代替しない |
| Data | 分類、所有者、取得・保存・削除の条件 | 読み進めずData ownerへ戻す |
| Dependency | 第三者サービスや共有基盤への依存の有無 | 自分の許可を第三者へ拡張しない |
| Out of scope | 未記載対象、実Asset、実Identity、第三者サービス、実Credential、PII | 明示的な対象外を維持する |

第4章の`TH-2026-002`とそのAsset `ASSET-2026-002` / `003`、Boundary `TB-2026-001` / `003`を計画の背景として参照します。`FLOW-2026-002` / `004`は設定・同意・APIの関係を読むための参照です。これらの親IDが存在しても、親の全AssetやFlowが本章の対象になるわけではありません。

## 9.4 Methodはツール名ではなく作用で限定する

「指定したツールを使ってよい」だけでは、Rate、Data、第三者への作用が決まりません。Permitted operationは目的・入力・出力・作用を記録し、Conditionalは追加条件と確認者が確定したものだけを扱います。Prohibitedと重なる項目や条件不明の項目は許可しません。

本章の許可候補は供給JSONの読み取り、合成Fieldの比較、上限内の要約の作成だけです。Conditionalは空集合です。実作業としての承認は未充足であり、この候補一覧が実施許可を発行するわけではありません。

実TargetへのScanや認証試行は行いません。実Credential・Token・Cookieの取得や再利用、第三者への通信、DoS、Persistence、Evasion、Log deletion、破壊的変更を許可しません。旧Guidanceに掲載された手法でも、本書の標準許可項目へ自動的に取り込みません。`SRC-NIST-TEST-001`

## 9.5 Timeと作用量を予算として定義する

Time windowにはTimezone、開始、終了を付け、Authorization期間内に含まれることを確認します。終了時刻は新規作業を許す時点に含めません。本章の機械可読例はUTCで統一し、日本時間の親期限との対応を明記します。

合成計画の提案Windowは2026-09-14T00:00:00Z〜00:30:00Zです。これは失効した親許可の外側にあるため、そのまま実施できません。数値がそろっていることと許可の有効性は別の検査です。

表T-09-03: 教育用の作用量予算（本書の教育用整理）。

| 作用量 | 本章の教育用上限 | 上限の意味 |
|---|---|---|
| Network requests | 0 | 外部通信を必要としない |
| Records | 100 | 検討対象件数の上限で、現在の供給Object数は3 |
| Evidence bytes | 65,536 | 想定する要約の上限。正本JSON全体の読取上限とは別 |
| Concurrency / Retry | 1 / 0 | 並行拡張や自動再試行をしない |
| Duration | 30分 | 作業Window内でさらに限定する |

これらはNIST等が指定した安全値でも、実行環境に適用済みの制限でもありません。本書が比較課題のために定義した数値です。上限超過時は新規作業を止め、Gapを記録します。処理完了を理由に上限を後から増やしません。

## 9.6 DataとEvidenceの取扱いを先に決める

Evidence planには、種類、最小Field、保存先、Custodian、保持期間の起点、廃棄対象、廃棄責任者を記入します。Credentialの参照IDと値を分け、不要な機微情報を証拠のつもりで複製しないことが重要です。

本章の`EVD-ROE09-001`は作成者が記入した計画記録です。RoE IDと版、Scope/Method、合成Object、時刻とCustodian、Sourceと限界、Stopと処置を必要Fieldとします。教材正本のHashはbyteの照合用であり、実測の真正性、法的証拠能力、実行成功を保証しません。

仮想の作業コピーは終了から24時間を上限に保持する計画とし、正本・承認記録・公刊教材とは区別します。本検査はファイルを削除せず、保存先の権限制御や削除を実測しません。実DataやSecretを見つけた場合は追加表示・転送・取得を止め、参照IDと発見時点だけで責任者へ連絡します。

想定外の脆弱性らしい情報を得ても、RoEに公開権限が自動的に含まれるわけではありません。Dataの取扱いと開示・届出・調整を分け、第2章のDisclosure判断へ戻します。IPAの役割・届出・調整の説明は判断材料であり、個別の検査や公表を許可する根拠ではありません。`SRC-IPA-VDP-001`

## 9.7 Stop、連絡、Recovery、Restartを分離する

Stop triggerは結果が悪い場合だけではありません。Authority不明、Scope逸脱、予期しないData、通信発生、予算超過、Evidence欠落、連絡不能、Cleanup未確認も停止理由です。不明をPassへ丸めません。

図F-09-01: Stopから再審査への接続（本書の教育用整理）。

```text
Stop triggerまたはUnknown
  → 新規作業を停止
  → 参照IDと時刻を保存
  → PrimaryまたはBackupへ連絡
  → 影響と合成作業コピーを確認
  → Cleanup記録を確認
  → 別のAuthorityで再開条件を再審査
```

主連絡先だけでなく代替連絡先、応答待ち時間、Recovery owner、Restart authorityを用意します。本例のSYNTH役割は連絡先の記入方法を示す記号で、実在担当者や稼働中の通知経路ではありません。60秒という応答計画値も連絡可能性の実証ではありません。

停止した作業を再開するには、原因と残存リスクを確認し、版に結び付いた再開承認が必要です。Cleanup完了と作業再開の許可を同じ判定にしません。連絡先や復旧可能性が不明なら、新規作業はDo not proceedのままです。

## 9.8 有限Statusと承認の意味

本章はIssue設計に基づく8状態を採用します。これは教材の記録状態であり、汎用の承認サービスや実Runtimeの状態機械を実装するものではありません。

表T-09-04: 八つのRoE状態（本書の教育用整理）。

| Status | 意味 | 新規作業の扱い |
|---|---|---|
| Draft | 条件を記入し、Gapを整理中 | 開始しない |
| Under review | 役割別に範囲と条件を審査中 | 開始しない |
| Approved | 同じ版について必要な確認がそろった記録 | 有効期間・Window等の再確認が別途必要 |
| Active | 条件を満たして実施中という記録 | 条件が失われたら停止。教材は実施しない |
| Paused | 停止理由と処置を確認中 | 再開承認まで開始しない |
| Revoked | 権限が取り消された | 開始しない |
| Expired | 許可またはRoEが期限を過ぎた | 開始しない |
| Completed | 当該版の作業を閉じた | Retestを旧記録の再開として扱わない |

機械検査は、ID、有限Scope、Data、Stop、期間、版、合成署名参照などの宣言の整合性だけを検査します。実際の署名・本人性・権限・通知・隔離は検証しません。テスト中の仮定例が条件充足となっても、`executionAuthorized=false`は変わりません。

## 9.9 Technical completionとDecision completion

検査対象をすべて読んだことはTechnical completionの候補ですが、それだけでDecisionが可能とは限りません。成果物では、次の二つを別欄で扱います。

- **Technical completion:** 対象記録の処理数、予算・停止の記録、Cleanupの参照がそろっているか。
- **Decision completion:** 必要な問いに答えたか、答えられないならGapを記録したか。代替説明・Confidence・受入責任者・再評価があるか。

Evidence不足はInconclusiveとし、成功・安全・不存在を意味する表現へ変換しません。親のNeeds EvidenceやCoverageを、この章の計画検査Passで更新しません。現CaseはtechnicalStatus=not-executed、decisionStatus=not-assessedです。

## 9.10 Change、Retest、Handoff

Scope、Method、Data、Time、Budget、Owner、版、停止条件、Retestの変更は`CR-ROE09-001`と`REA-ROE09-001`の再審査対象です。旧版の署名参照を新しい版へ使い回しません。実施後の再検査も、修正対象・範囲・手法・有効期間を確認し、`RET-ROE09-001`へ別の承認を関連付けます。

表T-09-05: Assessment・Retest・Control ValidationへのHandoff（本書の教育用整理）。

| Handoff | 渡すもの | 返すものと停止条件 |
|---|---|---|
| 第10〜14章 Assessment | RoEのID/版、Scope、Method、Stop、許可根拠 | Hypothesis→Validation→EvidenceまたはGap。未承認なら開始不可 |
| 第15章 Finding / Retest | 変更対象、Retest、ReauthorizationのID | 修正前後のEvidenceと残存Gap。旧RoEを再利用しない |
| 第21章 Control Validation | 同じ粒度のScope、Method、Stop、許可確認 | Controlの検証結果または未確認理由。Lab Safeから許可を推定しない |

第11章の独立Caseは、HypothesisとEvidenceを結ぶ形式の例として参照します。WSTGのversion指定した要求・評価・報告の語彙をBridgeに用いますが、WSTGの項目数や完了率を許可・安全・Decision充足の代替にしません。`SRC-WSTG-001`

## 安全な分析課題

### 目的と入力

[完全合成記入例](../cases/ch09-engagement-roe-example.md)と[機械可読計画](../cases/fixtures/ch09-engagement-roe.json)を読み、記録は整合していても作業を開始できない理由を説明してください。対象はこの供給教材だけです。実Credential・実Tenant・第三者システムで置き換えません。

1. `AUTH-CASE-2026-001`の期限と提案WindowをUTCで比較し、阻害条件を列挙する。
2. 三Object、明示的対象外、Permitted/Prohibited、作用量、Data、Stop/Recoveryを対応付ける。
3. Technical completionとDecision completionの差を、今得られていないEvidenceを挙げて説明する。
4. 新しい許可が必要な範囲と、親を変更せずに作るReauthorization/HandoffをART-02に記入する。

### ローカル検査

任意の補助として、Linux/WSL2、Python 3、固定済みRuby/Bundler依存とRepositoryを準備します。初回は[正本・build手順](../CANONICAL_SOURCE.md)に従って依存を導入してから実行してください。検査自体は実Targetへの通信、承認発行、コンテナ操作、削除を行いません。

```bash
python3 scripts/check_chapter09_contract.py
```

期待Evidenceは、4文書・ART-02・有限負例・Policy1.2.0・Projection1.1.0の整合性検査結果です。共有rendererを使用するため依存不足時は失敗します。Schema/JSON、親/Source、文書選択、Safetyの不一致があれば公開前検査も失敗し、生成を開始しません。入力不一致や実Data発見時は原因を調べるまで止め、検査を無効化しないでください。

影響はRepositoryの読み取りと補助検査用の一時データに限定されます。検査は教材正本を削除しません。演習で別途作った合成メモは保管方針に従って整理し、正本・親のEvidence・承認記録と混同しないでください。

### 成果物とRubric

成果物はART-02、判断`DEC-ROE09-001`に向けたGap、Reauthorization、Handoffです。次の5観点を各0〜2点で評価します。0点は欠落または矛盾、1点は記入のみ、2点は根拠と直接IDによる説明までできる状態です。合計点が高くても、Authority・Scope・Data・Stopの不明を相殺しません。

表T-09-06: ART-02のRubric（本書の教育用整理）。

| 観点 | 2点の条件 | 即時の差戻し例 |
|---|---|---|
| 権限と時点 | 親期限、今回の時点、版、必要な新承認を分ける | 期限経過を無視してApprovedにする |
| 対象と作用 | 三Objectと対象外、方法、量の関係が一意 | 未記載対象や第三者依存を許可する |
| DataとEvidence | Custodian、保持、廃棄、限界を説明する | 実Dataを合成記録へ混ぜる |
| 停止と再開 | Primary/Backup、Recovery、再承認を分ける | Cleanupだけで再開する |
| 判断と引渡し | Technical/Decision、Gap、Retestを分ける | 検査Passを実作業成功と呼ぶ |

## 章のまとめ

RoEは、許可の有無を作業条件へ落とす契約であり、権限を発明する文書ではありません。Scope、Method、時間・量、Data、Stop/Recovery、完了条件、再承認を直接IDで結ぶことで、実施できない理由も成果物として説明できます。

本章の完全合成CaseはDraft / Do not proceedです。親の期限やGapを保持し、機械的な整合性検査を実行許可と区別します。これが、後続のAssessment結果を過大評価せずDecisionへ渡すための出発点です。

## 次に学ぶこと

第10章では、確認済みのRoE内で情報収集の仮説と計画を定義します。本Caseの開始条件は未充足のままであり、章が進んだだけで許可されません。先に[第11章の独立したWeb/API評価例](11-web-api-hypothesis.md)を読む場合も、Case・RoE・Evidenceの独立性を維持してください。

## 参考文献・Source Note ID

- `SRC-NIST-TEST-001` NIST SP 800-115, Technical Guide to Information Security Testing and Assessment, Final / September 2008。§6.5–6.6とAppendix Bの計画・制約・連絡・Data・報告の観点に限定。
- `SRC-JP-LAW-001` e-Gov法令検索、不正アクセス行為の禁止等に関する法律。2025-06-01施行の現行表示を2026-09-13確認。個別の法的適用は判断しない。
- `SRC-IPA-VDP-001` IPA、情報セキュリティ早期警戒パートナーシップガイドライン、2024年版。情報取扱い・届出/調整の役割に限定。
- `SRC-WSTG-001` OWASP Web Security Testing Guide、stable v4.2。5.0開発版と区別し、第11章との評価語彙の接続に限定。
- [第9章 Source Review Note](../references/ch09-source-review-2026-09-13.md)
- [Source Registry](../references/reference-baseline.md)
