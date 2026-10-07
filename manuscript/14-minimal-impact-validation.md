# 第14章 最小影響で成立性を確認し、止め、戻す

## この章の位置付け

第13章のVerifiedは供給された記録の比較結果であり、追加操作の許可ではありません。本章は、何を確かめれば判断できるかを先に定め、必要なEvidenceが得られたら止める設計を扱います。結果が強いことと、調査を深く進めることを同じにしません。

成果物は`ART-22 Minimal-Impact Validation Record`です。`MIV-2026-014`は`CASE-2026-001`を`refines`します。第11章の`CASE-2026-011`と`ROE-2026-011`は独立した比較対象のままです。別CaseのEvidenceや許可を、本章の親記録へ付け替えません。

## 学習目標

- 最小影響の確認方法を設計できる。
- 十分な証拠と過剰な侵害を区別できる。
- Minimal-Impact Validation Recordを作成できる。

## 前提知識

[第8章](08-safe-lab-evidence.md)の記録と実ラボの区別、[第9章](09-engagement-roe.md)のAuthority / RoE、[第11章](11-web-api-hypothesis.md)の仮説、[第12章](12-enterprise-identity.md)の権限とGap、[第13章](13-platform-supply-chain.md)の供給記録の上限を前提にします。`Running`を含む第8章の八状態は、実ラボを動かした証明ではありません。

親`AUTH-CASE-2026-001`は2026-08-19T09:00:00Zに失効し、元Test windowは2026-08-06T00:00:00Z〜08:00:00Zです。`ROE-2026-009`はversion 1のDraft、三つのObjectと`executionAuthorized=false`を保持します。本章の読解課題は配布された合成資料だけを対象とし、この親記録を更新・延長しません。

## 導入ケース：あと一歩を正当化しない

架空の評価担当者は、供給Policyで二つの条件が整合することを確認しました。「実際のDataも見れば報告が強くなる」という案が出ます。しかし、今回の問いは設定条件の整合です。業務Dataの取得を必要条件にすり替えると、当初の判断要求と許可範囲を失います。

別の担当者は、一つの合成応答だけを読んで「対策は有効」と書きました。監査記録は欠けています。こちらは深く進めるのではなく、支持できる範囲と不足するEvidenceを分ける必要があります。二つの事例に共通する問題は、結論を先に決めて必要Evidenceを後から増減させることです。

## 全体像：問いから停止・残存確認まで

次の流れを左から読みます。入力は供給された仮説と親の制約、出力は主張の上限を持つ判断記録です。矢印は許可の自動継承でも、実操作の実行順でもありません。

```text
Hypothesis → Authority / RoE → Minimum evidence question
→ Safest sufficient method → Expected / Disconfirming evidence
→ Stop → Cleanup / Residual check → Finding / Reassessment
```

`F-14-01`はこの判断の接続を表します。資料の版、対象ID、操作対象、Evidenceの所有者が変われば同じ問いとは扱わず、計画へ戻します。

## 基本概念：存在条件と業務影響は別の問い

Proof of Vulnerabilityは、対象の弱点について定めた成立条件をEvidenceで評価することです。Proof of Impactは、その弱点が特定の業務へ与える影響を評価する別の問いです。前者の支持から、後者の測定済みという結論は導けません。

本章の`Supported`は合成資料内の限定された仮説が支持された状態です。実到達、実装の完全性、侵害なし、暗号検証、安全性、法的許可を意味しません。第12章のUnknown binding / Coverageと非Federation評価の三つのnull、第13章の実Build・Deploy・署名検証0も保持します。

Minimum evidence questionには、対象ID・版、判断する条件、期待する証拠、反証となる証拠、未確認なら結論を保留する条件を書きます。対象の違う二つの観測を、一つの条件を満たす証拠として合算しません。本教材では対象Resource IDと監査参照IDの二つを期待値と完全一致で比較します。これは作成者が記述した記録同士の比較であり、実製品の制御や応答を測定するものではありません。

## 四つのMethodを最小十分性で選ぶ

Methodは以下の四種類です。名称だけで強弱や実施許可を与えません。WSTGの基準との比較と複数手法の組合せという考え方を補助にしつつ、本書の有限四分類は教材独自の設計です。`SRC-WSTG-001`

| Method | 本章で読むもの | 主張できないこと |
|---|---|---|
| Static | 供給Policy・構成の条件 | 実装や実到達の確認 |
| Simulation | 作成者が供給した条件評価記録 | 実製品のPolicy engineでの実行 |
| Offline replay | 供給した応答・監査記録の比較 | 実HTTP送信や観測の再実施 |
| Minimal synthetic operation | 最小合成操作の計画と未実施理由 | 合成Accountの実作成や実操作の承認 |

本教材では四Methodとも実サービスへ接続しません。最後のMethodを選ぶ記録も計画だけで、`executionDisposition=Not performed`です。Staticで答えられる問いを、報告を強く見せるために実操作へ昇格しません。必要な証拠がない場合は、不足と代替の問いを残します。

NIST SP 800-115の計画・実施中の調整・分析・報告の枠組みを、問い、Scope、制限、連絡、Evidenceの取扱いを事前に結ぶ背景として用います。古い製品手順や侵入例を採用するものではありません。`SRC-NIST-TEST-001`

## 六つのResultと実施有無を分離する

| Result | 本教材の判定 | 必須の説明 |
|---|---|---|
| Supported | 二条件とも支持 | 対応するEvidenceと主張上限 |
| Partially supported | 支持はあるが全条件を支持できない | 支持範囲と未確認・反証範囲 |
| Weakened | 支持はなく、一部の反証がある | 反証と残るGap |
| Inconclusive | 判断材料がない、または未実施 | 不足・未実施理由と代替案 |
| Rejected | 二条件とも反証 | この仮説・対象版に限定した反証 |
| Stopped | 停止triggerが成立 | trigger、停止記録、残存確認 |

`Not performed`は第七のResultではなく実施有無の欄です。未実施の記録では問いのResultをInconclusiveとし、なぜ実施しないかを残します。Methodの四分類とResultの六分類は別の軸です。

判定はまず停止trigger、次に未実施、次に供給された二条件のEvidenceを見る順です。観測valueは合成ID文字列またはnullです。期待IDとの完全一致をtrue、不一致をfalse、未観測をnullという比較結果に変換します。nullは未観測でありfalseではありません。Evidence slotにIDを割り当てただけでは観測済みになりません。`present=false`のslotは`evidenceIds`へ含めず、時刻もnullにします。

## 十分なEvidenceで停止する

二条件の支持または反証が揃えば、供給記録についての最小Evidenceは十分です。追加の確認を続けず、停止理由を記録します。揃わなければEvidence-gapとして止め、欠落を補うための実操作を自動承認しません。

想定外の権限、外部通信、実Data、Scope外Asset、未知の入力が現れたら停止します。実Dataを取得しません。実Credentialを再利用しません。横展開、永続化、回避、DoS、破壊は実施しません。本教材の停止例は`Unexpected-input-symbol`という作成者の記号だけであり、実Dataを配布した例ではありません。

`stepsAfterStop=0`は供給記録上の継続がないことを表し、実プロセスを制御する安全装置ではありません。停止後は追加操作を行わず、責任者、対象、Evidence、未確認事項、次の判断を記録します。

## CleanupとResidual checkを別に記録する

Cleanupには対象、所有者、予定した整理、記録上の完了証拠を記載します。Residual checkには別の確認者と証拠を割り当てます。親第8章のreceiptは今回の作業コピーの証拠ではなく、別のScopeのままです。

本教材の`Recorded complete`と`Recorded clear`は、作成者が供給した読解用記録の値です。実削除や実システムの残存影響を測定したものではありません。正本や親Evidenceは削除対象にしません。現実のデータ取扱い・保存・廃棄は個別の計画と組織方針へ戻す必要があります。`SRC-NIST-TEST-001`

Cleanup未開始、またはResidual checkがUnknownなら`recordStatus=Open`です。SupportedでもCompleteへ進めません。一方、Gap・制限・Owner・期限が埋まり、読解記録の整理と確認が揃えばInconclusiveの記録もCompleteになり得ます。これは業務上の問題が解決した意味ではありません。

## 四つの視点と責任分担

| 視点 | 読むべきもの | 過剰な結論を防ぐ問い |
|---|---|---|
| 攻撃評価者 | 成立条件・最小Evidence・停止 | その追加確認は判断に必要か |
| 防御者 | 観測条件・Gap・残存確認 | 対象版と観測範囲が一致するか |
| 分析者 | 支持・反証・代替説明・確信度 | 資料不足を否定と混同していないか |
| 意思決定者 | 制限・Owner・期限・次の判断 | 記録完了を対策成功と読んでいないか |

OWNは最小十分なEvidenceと停止・残存確認の判断記録です。BRIDGEは親章のAuthority / Hypothesisと、第15章のFinding / Retest、第21章のControl ValidationへのHandoffです。後続Handoffはplanned-not-deliveredであり、本章だけで後続成果物を完成扱いにしません。

DELEGATEは脆弱性別手順・Exploit開発・製品設定です。[Pentest学習書](https://itdojp.github.io/pentest-learning-book/)へ委譲し、本章には問いとEvidenceの選択に必要な境界だけを残します。委譲先の掲載手順も、本章の親RoEに実行許可を追加しません。

## 安全な分析課題

Purpose: [完全合成記入例](../cases/ch14-minimal-impact-validation-example.md)の八記録を、[ART-22 Template](../templates/minimal-impact-validation-record.md)へ整理し、Result・実施有無・記録完了を区別します。

Prerequisite / Authority / Scope: 配布した[JSON](../cases/fixtures/ch14-minimal-impact-validation.json)と[Schema](../schemas/ch14-minimal-impact-validation.schema.json)だけを読みます。Python 3とRepositoryの固定Ruby bundleを準備済みのローカルcheckoutを前提とし、依存不足なら停止します。実Target、実Account、外部通信は必要ありません。

Expected evidence / Impact: 次のコマンドは供給記録と公開文書の契約を読む検査です。成功時は八記録・四Method・六ResultとPolicy/Projectionの版を表示します。ソース正本や親の状態を変更せず、サービスやラボを起動しません。

Stop / Cleanup: ERROR、未知入力、依存不足、想定外の通信があれば停止します。追加の取得・再試行で判断を補完せず、自分の読解用コピーとエラー記録を区別して整理します。正本と親Evidenceは保持し、実システムの削除成功とは主張しません。

```bash
python3 scripts/check_chapter14_contract.py --no-regressions
```

最初に001と005で十分性とGapを比べ、002と003で部分支持と反証を分けます。004ではRejectedの対象範囲を確認し、006では未実施を第七Resultにしない理由を書きます。007は停止triggerを優先し、008はSupportedでも残存確認が不足すればOpenであることを説明してください。

良い記録は「供給資料の二条件は支持されたが実影響は未測定、残存確認はUnknown、Ownerと期限を残す」と書きます。悪い記録は「証拠があるので全部安全」と一般化します。反証例は「両条件の不一致」を示しても実環境全体を否定せず、対象版に結論を限定します。

## 作成する成果物

ART-22にはHypothesis、Authority、Validation、Expected / Disconfirming Evidence、Stop、Cleanup、Residual、Finding、Decision、ReassessmentをIDで接続します。Templateの空欄は記入すべき問いであり、承認済みの初期値ではありません。

完全合成CaseはJSONの全末端値を公開Field/Value表へ対応付けます。Schemaはこの有限教材用で、任意の実環境記録やNIST/OWASP適合を判定するものではありません。共有Publication Projection 1.1.0とContent Safety Policy 1.2.0へ全四文書を渡し、章固有のMarkdown/HTML parserは追加しません。

## 評価基準

各行を0点（欠落・不整合）、1点（記載はあるが追跡不足）、2点（直接Evidenceと制限を追跡可能）で評価します。合計点で安全上の欠落を相殺しません。

| 観点 | 2点の条件 | 停止・差戻し条件 |
|---|---|---|
| 問いと方法 | 対象ID・版と最小十分性が明確 | Method名を許可へ転用 |
| Evidence | 支持・反証・未観測を区別 | 別対象や空slotを根拠にする |
| 停止 | 十分性またはtriggerで終了 | 停止後の追加操作 |
| Cleanup / Residual | Scope別の証拠と所有者 | 未確認からCompleteへ昇格 |
| 判断と引継ぎ | 上限・代替・Gap・期限がある | 実影響や安全性を無根拠に断定 |

## よくある誤解

「最小合成操作なら許可不要」ではありません。「ResultがSupportedなら完了」でもありません。「未実施だからRejected」とも言えません。実施有無、問いの判定、記録の完了、実システムの状態を分けて読みます。

「NISTやOWASPに載っているので実施する」という判断も避けます。今回採用するのは計画・比較・分析・報告の考え方の限定範囲です。Sourceは個別環境のAuthorityになりません。`SRC-NIST-TEST-001` / `SRC-WSTG-001`

## 章のまとめ

最初に問いと主張上限を決め、必要な供給Evidenceだけを比較します。十分なら停止し、不足や未実施ならその理由を記録します。CleanupとResidual checkを別に扱い、SupportedからCompleteや実操作許可へ飛躍しないことがART-22の中心です。

## 次に学ぶこと

第15章ではFindingを改修・再評価・残存リスクの判断へ接続します。本章から渡すのは限定された結論とEvidence、Gap、Owner、期限であり、親RoEの更新や後続検証の成功ではありません。現在は[成果物索引](../artifact-index.md)で接続先の役割を確認します。

## 参考文献・Source Note ID

- `SRC-NIST-TEST-001`: NIST SP 800-115、September 2008 Final。採用節と非採用範囲は[第14章Source Review Note](../references/ch14-source-review-2026-09-16.md)を参照します。
- `SRC-WSTG-001`: OWASP WSTG 4.2のIntroduction、比較・版別参照・複数手法の考え方。5.0 developmentや4.3 Unreleasedを採用版にしません。
