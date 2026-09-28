# 第IV部 横断読解：要求から配布と判断へ

この頁は第23〜26章の供給教材を読み直すための対応表である。新しい収集、帰属判断、配送、承認を記録するCaseではない。章順は学習の順序であり、四章が同じ対象を時間順に調査したという意味ではない。

学習目標は、問いと期限から根拠を辿り、判断の限界を配布先が変わっても保持できることである。作業は公開された合成記録の読解だけに限定する。外部Feed、TAXII、AI APIへ接続せず、実在人物の追跡や第三者環境での検証を行わない。権限、取得条件、来歴が不明な資料は採用せず、その不明点をGapとして残す。

## 1. 最初にCaseと参照の種類を分ける

| 教材 | 入口となるID | 関係と読む範囲 |
|---|---|---|
| [第23章の記入例](ch23-intelligence-requirements-example.md) | `IRCP-2026-023-001` / `ART-29` | `CASE-IRP-2026-001`。要求と収集計画を読む。親教材は方法参照であり、EvidenceやAuthorityを引き継がない |
| [第24章の記入例](ch24-source-evaluation-example.md) | `EST-2026-024-001` / `ART-30` | `CASE-OS24-001`という独立Case。Source、Item、Claim、Evaluationの組合せを読む |
| [第25章の記入例](ch25-structured-analysis-attribution-example.md) | `AJ-2026-025` / `ART-12` | `CASE-2026-025`。Evidence、代替説明、限定結論を読む |
| [第26章の記入例](ch26-cti-distribution-example.md) | `CDP-2026-026-001` / `ART-08`・`ART-09` | 第25章の同じCaseを`refines`。同じ根拠と限界を技術・経営の二Productへ変換する |

第24章の`REF-EV24-023`は第23章の記録IDを指すが、`received=false`である。`REF-EV24-025`の`recordId=ART-12`はArtifactへの方法参照であり、`AJ-2026-025`を受領したという記録ではない。

第26章の`MREF-CTI26-023`と`MREF-CTI26-024`も`method-only`で、`evidenceReceived=false`、`receiptId=null`である。第23章の問いや第24章の評価記録を、そのまま親25のEvidence集合へ追加しない。直接ID参照、方法参照、予定Handoff、実際の受領は別々に確認する。

## 2. 語彙の対応を確認する

| 語彙 | 読む内容 | 同一視しないもの |
|---|---|---|
| Requirement / Collection | 判断に必要な問い、回答基準、収集計画、Owner、期限 | 優先度と収集・操作の許可 |
| Source / Item | 情報源と、特定の版・時点で保存した資料 | 掲載サイトの数と独立した観測の数 |
| Claim / Evaluation | 主張と、その主張に対する資料の用途・信用度・制約 | Source全体の評判と個別主張の裏付け |
| Hypothesis / Alternative | 比較する説明、焦点質問、支持・反証・不足 | 未排除の説明と確認済み事実 |
| Confidence / Attribution | 判断の確からしさと、帰属を述べられる水準 | 数値らしさと正確さ、IOC一致とActor断定 |
| Product / Feedback | 相手と用途に合わせた説明、理解・有用性の確認予定 | 作成と配達、受領と理解、共有ラベルと利用許可 |
| Decision / Reassessment | 選択肢、残余リスク、再評価条件 | 提案と承認、表示と実行、訂正とSTIX Objectの失効 |

Source reliabilityとinformation credibilityは別軸である。第24章の`use`、第25章の`judgments`、第26章の`confidence`は同じ列名ではないが、いずれも対象と根拠を明示して読む。用途の違うラベルを自動換算しない。特に第26章では三KJの`stixConfidence`を`null`に保ち、低・中を機械的な数値へ置換しない。

## 3. 要求と収集を読む経路：第23章

`DEC-IR23-001`の問いは「48時間以内に外部連携を停止すべきか」である。`ROLE-IR23-DECISION-OWNER`の回答期限は合成時刻`2026-10-03T00:00:00Z`。ここから五Requirementの回答基準、対象・版・観測Window、CollectionとEvidenceの対応を読む。

`IR23-R1`は`Satisfied`、R2は`Partially satisfied`、R3は`Collecting`、R4は`Planned`、R5は`Blocked`である。要求がある、収集を計画した、資料がある、回答基準を満たした、の四段階を飛ばさない。八Collectionには`Cancelled`もあり、未充足や中止を完了へ丸めない。

`HOF-IR23-24`はSource確認条件、`HOF-IR23-25`は未充足の問い、`HOF-IR23-26`は判断主体・選択肢・期限を渡す予定である。三件とも`planned-not-delivered`、`receiptId=null`、`executionAuthorized=false`。記録のasOfは合成時刻`2026-10-02T12:00:00Z`で、この時点で受領を示す証拠はない。処理18:00Z、分析21:00Z、配布22:00Zの各期限はいずれも同日中の将来の予定であり、期限経過後の結果は記録されていない。実収集・実操作・実通知は各0である。

この要求IDを第25章の`IR-2026-025`へ改名して連結してはならない。前者は収集計画教材、後者は別Caseの分析要求であり、第26章が直接引き継ぐのは後者である。

## 4. 来歴と情報源評価を読む経路：第24章

`DR-OS24-001`に対して、保存したItemのSource・版・取得時刻・変換履歴を確認し、どのClaimに何として使えるかをEvaluation単位で読む。同じItemでも、別Claimへ同じ評価を複写しない。

例として`ITEM-EV24-006`は、`EV-EV24-006`で`CLM-EV24-003`、`EV-EV24-010`で`CLM-EV24-004`と結び付く。ともに`Direct evidence`かつ`supported`だが、異なるClaimについて記録された二評価である。`ITEM-EV24-009`に対応する`EV-EV24-009`と`EV-EV24-011`は、同じ二Claimに対する`Lead`かつ`limited`である。資料数、評価行数、独立観測数を混同しない。

`HOF-EV24-25`と`HOF-EV24-26`は、十一Evaluationと十一Gapを**記録として**渡す予定である。`Excluded`の`EV-EV24-008`も履歴から消さないが、採用根拠へ格上げしない。二Handoffとも`planned-not-delivered`、`receipt=null`、`executionAuthorized=false`。予定リストに含むことは、第25章や第26章のEvidenceへ採用済みという意味ではない。

第24章の独立Caseは合成の10月、第25〜26章の判断時点は合成の7月である。章番号順に連続した一つの調査時系列を作らない。教材内時刻と、Source Noteの実際の資料確認日も別である。

## 5. 分析から二つのProductを読む直接経路：第25章→第26章

ここは方法参照ではなく、同じ`CASE-2026-025`を詳細化する経路である。次のIDを両章のJSONで照合する。

| 親25の記録 | 子26で読む欄 | 保持する限界 |
|---|---|---|
| `DR-2026-025` / `IR-2026-025` | `requirement` | 別Caseの要求や意思決定者へすり替えない |
| `EVD-2026-025-001`〜`008` | `evidence`の同じIDと`sourceId` | 八Evidenceは新規観測ではない |
| `SN-2026-025-001`〜`008` | `independenceGroupId` | 派生・再掲で独立性を増やさない |
| `AJ-2026-025` | `KJ-CTI26-001`、`002`の`parentJudgmentId` | 未確定の成功可否と代替説明を残す |
| `SEJ-2026-025-001` | `KJ-CTI26-003`の`parentJudgmentId` | 情報源評価の判断を別種の成功証拠へ変えない |
| `DEC-2026-025` / `REA-2026-025` | `decision` / `reassessment`の親参照 | 親の判断を上書きせず、実行・受領を捏造しない |

### 再掲と欠測を読む

`SN-2026-025-004`・`005`・`007`は`IG-EXT-002`という同じorigin群である。親の`LIN-2026-025-001`〜`003`と`CR-2026-025-001`が再掲・派生・引用を結ぶ。第26章の`KJ-CTI26-003`も、三Sourceを三つの独立観測とせず、`independentOrigins=1`を保持する。

`KJ-CTI26-002`は`EVD-2026-025-008`と`GAP-2026-025-001`を読む。観測範囲には時間帯や記録項目の欠落があるため、限定された非観測から「成功はなかった」と断定しない。三KJはいずれも`successDetermined=false`、帰属上限は`L2`である。確信度「中」や技術的な共通性からCampaign、Operator、組織、国家へ帰属を飛躍させない。

### 同じ判断を異なる相手へ渡す

`PRD-CTI26-TECH`は`ART-08`、相手は`SYNTH-SOC Lead`、用途は`tactical-operational`。`PRD-CTI26-EXEC`は`ART-09`、相手は`SYNTH-CISO`、用途は`strategic`。両方から同じ三KJと三Recommendationへ遡れることを確認する。技術側では根拠・Coverage・条件、経営側では選択肢・影響・可逆性・残余リスクに重点を置くが、根拠やConfidenceを増量しない。

両Productは`prepared-not-delivered`、`delivered=false`、`receiptId=null`、`actionPermission=false`。`TLP:CLEAR`は共有面のラベルであり、別欄のLicense、暗号化、保持期間、操作の許可を置き換えない。三Recommendationも`not-executed`、`authorityGranted=false`である。

`DEC-CTI26-001`は親Decisionを示す`synthetic-representation`であり、`authorityGranted=false`、`executed=false`。選択肢Aが親の限定案を保持することと、実際に対象を変更してよいことは別である。二Feedbackは`planned-not-received`、`answer=null`、`receiptId=null`で、受領や理解を確認したことにしない。

二Productのcutoffは合成時刻`2026-07-29T09:00:00Z`、preparedは10:00Z、期限・有効期限は翌日01:00Z。第26章の再評価予定00:30Zと、第25章の歴史的な再評価予定`2026-08-08T10:00:00+09:00`は別欄に残す。参照先を同じにしても時刻を一方へ統合しない。

## 6. 交換形式と判断根拠の境界

第26章の`CASE-STIX26-DEMO`は親Caseとは独立した構造教材であり、`structure-only-not-evidence`である。`adoptedEvidenceIds=[]`、`contributesToJudgment=false`、`networkExecuted=false`。13 ObjectのBundleと静的TAXII応答例は、第25章のEvidence集合へ追加しない。

STIXの構造・ID・関係、TAXIIの`can_read=true`、静的応答の`status=200`が揃っていても、内容の真偽、実通信、信頼、実配達、実環境の権限を証明しない。これらは供給されたoffline例の値であり、この演習で接続して確かめるものではない。一般的なSTIX/TAXII適合性や全Propertyの妥当性は、この有限教材の検査対象ではない。

訂正が必要なら影響するKJ、Product版、理由、再評価先を記録する。現在の`supersedingProductId=null`、`stixObjectRevoked=false`を、訂正方針が書かれているというだけで変更しない。第29章向け`HOF-CTI26-029`も`planned-not-delivered`、`receiptId=null`、`authorityGranted=false`の予定である。

## 7. 安全な横断演習と評価

公開されている四CaseとJSONだけを使い、次の三経路を別々の表へ転記する。新しい観測値、実在Actor、実配達記録を追加しない。

1. **要求の経路**: 第23章のDecision → Requirement → Collection → Evidence / Gap → 予定Handoff。R1とR5を比較し、回答基準と停止理由を説明する。
2. **評価の経路**: 第24章のItem → Claim → Evaluation → Gap → 予定Handoff。006/010と009/011を比較し、同じ資料の評価がClaimごとである理由を説明する。Excludedも履歴に残す。
3. **配布の経路**: 親25のIR → Evidence / Source Note → Judgment / Alternative / Gap → 子26のKJ → 二Product → Decision / Feedback / Reassessment。003のorigin数と002の非観測を確認する。

記入表の列は「入口ID」「参照先ID」「関係の種類」「対象・版・時刻」「Confidenceまたは用途」「残るGap」「Owner・期限」「未受領・非実行の根拠」とする。方法参照と直接参照が交差する箇所では、受領していない情報を明示して線を止める。

| 評価観点 | 達成の目安 | 不合格となる取り違え |
|---|---|---|
| 追跡性 | 原記録のIDで三経路を区別できる | 四章を架空の一連の収集・配送実績にする |
| 根拠の質 | Item/Claim/Evaluationとoriginを分ける | 再掲を独立根拠、Excludedを採用根拠へ昇格する |
| 判断の限界 | Gap、代替説明、L2、非観測の範囲を保持する | 成功可否やActorを追加根拠なしに断定する |
| 配布と権限 | 未配達・未受領・非実行、Ownerと期限を示す | 作成済みProduct、TLP、HTTP 200を許可とする |

答え合わせでは、[Requirement / Collection Plan](../templates/intelligence-requirement-collection-plan.md)、[Source Evaluation Table](../templates/evidence-source-evaluation-table.md)、[Analytic Judgment Record](../templates/analytic-judgment-record.md)、[CTI Report](../templates/cti-report.md)、[Executive Brief](../templates/executive-brief.md)へ戻る。不一致は自分の表の参照誤りか、教材の改訂が必要かを分け、後者なら不一致のIDと欄を記録して停止する。供給記録を書き換えて正解へ合わせない。

## 8. 検査範囲と次への接続

リポジトリの`npm run check:part04`は固定した四章の教材と独立交換例について、章間参照、非継承、未配達、供給された境界値、およびこの頁の全公開fieldを検査する。各章のSchema、回答状態、来歴の評価手順、分析手法、STIX有限profileを再実装しない。構文解釈は共有Publication Projection、安全文法は共有Content Safety Policyが所有する。

この頁は内部教材の対応を説明するもので、新しい外部標準の解釈や確認日を追加しない。規範と版・状態・未確認事項は、各章のSource Noteと[第26章のSource確認記録](../references/ch26-source-review-2026-09-28.md)へ戻る。歴史的なSource版を現在版の記述で上書きしない。

第IV部がOWNするのは、要求から根拠評価、限定判断、用途別配布と再評価までの接続である。Detection / IRへの引渡しは[第III部横断読解](part-iii-detection-improvement-map.md)へBRIDGEし、製品のFeed管理、実TAXII接続、一般的なPlatform運用は専門資料へDELEGATEする。第27〜29章へ進む際も、方法参照は権限やEvidenceの継承ではなく、予定Handoffは受領ではないという境界を保つ。
