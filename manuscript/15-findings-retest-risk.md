# 第15章 Finding、改修、再評価、リスク受容

## この章の位置付け

第14章では、問いに必要なEvidenceを限定し、停止と整理を判断記録へ接続した。本章では、その記録を「何を直すか、何を再確認するか、誰が残るRiskを引き受けるか」へ変換する。Findingは脆弱性名の一覧ではなく、対象・条件・根拠・判断の対応を後から検証できる報告単位である。

OWNはFinding Report、Retest Record、残存リスクと受容権限の引継ぎである。BRIDGEは第7章の優先度、第11〜14章の評価、第16〜17章の観測・検知、第21〜22章の統制改善、第26章の意思決定である。DELEGATEは個別Patch、認証実装、変更管理の詳細と法的判断である。[攻撃評価専門書](https://itdojp.github.io/pentest-learning-book/)と[認証・認可専門書](https://itdojp.github.io/practical-auth-book/)で詳細を確認した場合も、対象版・変更参照・Evidenceの範囲を本章の記録へ戻す。委譲先の操作は本演習の前提ではない。

## 学習目標

- Findingを構造化できる。
- 対策の種類を分けられる。
- Finding ReportとRetest Recordを作成できる。

## 前提知識

第7章のSeverityとPriority、第9章のRoE、第12章のIdentity binding、第14章のResultとEvidence不足を理解していること。`CASE-2026-001`の親RoEはDraftで、元のAuthorization期限と実施Windowは経過している。親の三Objectと実行不可という境界は、本章でも変更しない。

必修課題は、供給された完全合成JSONを読むS1の分析課題である。実Scanner、実Account、実変更、実Retest、実届出、実公開を行わない。実在の脆弱性の認定、標準適合、法的責任や安全性の証明を目標にしない。

## 導入ケース：権限を減らしたという報告だけで閉じてよいか

架空の請求連携について、業務要件には`read-summary`、供給設計には`read-all-summaries`と書かれている。担当者は「必要な範囲へ直したので完了」と述べる。しかし、変更後の版、対象App、監査記録との対応、例外Scopeが未記載なら、報告を受け取った事実と改修成功の確認は別である。

本章の`APP-FRT15-001`は、第12章のOAuth App設計から作った別の合成教材である。親Appの現在のbindingや実装を引き継いだ実測ではない。`FRT-2026-015`はCASE-2026-001をrefinesするが、七つのScenarioは独立した判断の対比であり、一つの本番Findingの時系列ではない。

第14章の`VAL-MIV14-001`と`FND-MIV14-001`は手法の参照元である。本章の新しい対象を検証したEvidenceではない。各Findingには新たな`VAL-FRT15-*`と供給Evidenceを付ける。親の`HOF-MIV14-15`はplanned-not-deliveredのまま保持し、親を後から配達済みへ書き換えない。

## 全体像：状態より先に根拠の連鎖を作る

F-15-01は、本章で追跡する判断の流れである。入力は対象版を持つ供給記録、出力はART-04とART-23、境界は実操作や実権限を与えないことである。

```text
Finding / Subject / Revision
→ Symptom / Root condition / Validation / Evidence
→ Technical impact / Business impact / Limitation
→ Treatment / Control / Owner / Due date
→ Change reference / Retest criteria / Observation
→ Residual risk / Decision / Acceptance authority
→ Expiry / Reassessment / Disclosure audience
```

同じIDを記載するだけでは追跡は成立しない。対象、版、Scope、時点が同じかを確認する。Evidence不足を別Scenarioや親Caseの記録で埋めない。第11章のCASE-2026-011は独立した比較例であり、親Evidenceや許可へ付け替えない。

## 症状と根本条件、技術影響と事業影響を分ける

T-15-01では、観測に近い記述から判断までを分ける。確認できるのは供給された設計文字列の差であり、実システム上の過大権限そのものではない。

| 欄 | 良い記録 | 避ける飛躍 |
|---|---|---|
| Symptom | 同じ供給版で要件とpermission欄が異なる | 実データへ到達できたと書く |
| Root condition | 要件と権限宣言を照合する承認条件が供給設計にないという分析候補 | 記録がないため実運用にも承認がないと断定する |
| Technical impact | 供給設計上の範囲差。実装上の到達性は未確認 | 別Appや別版にも成立すると広げる |
| Business impact | 請求処理への影響を懸念する仮説。損失は未測定 | Severityから損害額を算出する |
| Limitation | 実装、現在のbinding、例外経路の資料がない | 未観測を不存在や安全の根拠にする |

Affected scopeはConfirmed / Candidate / Excluded / Unknownを分ける。本教材のConfirmedも「供給された文字列を確認した範囲」であり、実製品の影響範囲ではない。確信度は中とし、実装側に別の制約がある可能性を代替説明に残す。新たな対象版や実装Evidenceが得られれば、この判断を再評価する。

WSTG 4.2 Reportingは、Scope・Limitationsと読者別の報告、Findingの参照可能な識別子、再テスト時の前回結果との対応を考える補助となる。一つの報告形式の提案であって、本章の状態一覧を定める標準ではない（SRC-WSTG-001）。

## Severity、Priority、Treatmentを一つの値にしない

CVSSは技術的な深刻度を伝える材料であり、組織の業務依存や受容権限をすべて表すものではない。第7章のScore・Vector・Nomenclatureの契約を継承し、必要な情報がなければ新しいScoreを作らない。CVSSにはBase / Threat / Environmental / Supplementalがあり、組織固有の判断には範囲外の要因も必要となる（SRC-CVSS-001）。

本章は新しいScoreを付けず、JSONの三欄をnullにする。第7章のVPR-ITEM-001は「高いSignalでも別の文脈では判断が異なる」という比較参照だけであり、そのCVE評価をOAuth Appへ移す根拠ではない。修正順位、Urgency、Due dateは、業務依存、Evidence不足、変更可能な時期、Ownerの判断理由を別欄に残す。

T-15-02では、対策の便益と負担を比較する。どれも供給された計画案であり、実装済みではない。

| 種類 | 比較する案 | 限界と依存 |
|---|---|---|
| Temporary | 利用Scopeを一時的に絞る計画 | 必要連携を制約する可能性。権限宣言の根本修正ではない |
| Permanent | 業務要件と権限宣言を対応付ける改版 | 仕様確認、変更計画、別の許可判断が必要 |
| Compensating | 対象・版・判断を監査記録へ接続する代替統制 | 説明可能性は増すが、権限宣言の差自体は残る |

推奨案にはTreatment ID、Control ID、Owner、期限、Dependencyを付ける。「監視する」だけでOwnerや観測項目がなければ、未解決の作業を隠したことになる。補償的統制を恒久改修と同じ意味でClosedへ接続しない。

## Retestは変更後の問いを再確認する記録である

ART-23では、Finding ID、対象、変更前後の版、Change reference、Scope、Acceptance criteriaを先に定義する。本教材の二条件は、第一に必要な権限宣言、第二に期待した監査参照である。実際のBusiness Logicや実サービスの挙動試験は範囲外である。

T-15-03の五Resultは本書の有限教材ルールであり、一般のRetestにそのまま適用する自動判定器ではない。

| Result | 本教材の条件 | 残す説明 |
|---|---|---|
| Passed | 同じ対象・変更後版で二条件が一致 | 二条件以外のScopeは未確認 |
| Partial | 権限宣言は一致し、監査参照は不一致 | どこまで支持し、何が残るか |
| Failed | 必要な観測が揃い、第一の権限条件が不一致 | 満たさなかったAcceptance criteria |
| Inconclusive | 観測不足、またはMethodが条件を確認できない | 不足資料と次に必要な確認 |
| Stopped | 供給記録の停止triggerが成立 | 追加確認をせず、停止理由と引継ぎを残す |

停止を最優先にし、欠測をfalseとしてFailedへ変換しない。Scannerの要約だけでは、本教材の設計二条件との対応を確認できないためInconclusiveとする。Scannerを増やして再実行する演習ではない。WSTGの前回Finding・更新状態・参照関係の説明を補助に使うが、この五Resultは本書独自の設計である（SRC-WSTG-001）。

Retest記録には限界とRegression scopeも必要である。二つの供給欄がPassedでも、全システムの非回帰や実影響なしを証明したことにはならない。

## 六つのFinding状態とClosedの根拠

T-15-04は、供給された判断記録の状態を表す。状態だけで実環境の改善を証明しない。特にMitigatedの教材例は、一時的なScope制限案のレビュー記録を持つという設定であり、実装済みフラグはfalseのままである。

| Status | 記録上の意味 | 必要な根拠 |
|---|---|---|
| Open | 初回報告を受け付け、次の判断を残す | 対象・条件・Evidence・Owner |
| Mitigated | 一時的対策について限定されたレビュー記録がある | Temporary案と同じScenarioの根拠 |
| Accepted | 残存Riskを明示的な権限・期限・条件で引き受ける設定 | 有効な受容記録、Residual、Reassessment |
| Retest required | 現在の記録では再確認が必要 | 変更参照、確認すべき条件と不足Evidence |
| Closed | この記録の終了条件を満たす | 十分なRetest、または明示的で有効な受容根拠 |
| Reopened | 終了・受容の前提を再評価する | 停止や期限切れ等の無効化条件と次の担当 |

Closedの経路は二つを区別する。Retestで閉じた場合は確認したScopeを示す。受容で閉じた場合は未修正の条件と受容の根拠を示す。受容によるClosedを「修正済み」と表示しない。第14章のCompleteは読解記録の整理が完了した意味なので、本章のClosedを自動的に成立させない。

## 残存Risk、受容権限、期限と開示を接続する

受容記録にはFinding・対象・Scope、権限の参照、権限保有者と判断者、決定日時、失効日時、条件、Residual risk ID、Reassessment IDが必要である。誰かが「承知した」と書いただけでは代替にならない。期限切れや対象版の変更があれば、有効性を再確認する。

本教材のDELEGATION-FRT15-*は架空の業務判断記録であり、評価作業のAuthorizationではない。AcceptedでもClosedでも、親RoE Draft、元Window、失効したAUTH、三Object、executionAuthorized=falseを維持する。Risk acceptanceでAuthority不足や法的禁止を上書きしない。

開示はFinding状態と別の軸である。IPA/JPCERT/CCのガイドラインは、脆弱性関連情報の取扱いに関する役割と調整の枠組みを説明している。調整状況とAudienceを別記する参考にするが、評価や公表の個別許可として扱わない（SRC-IPA-VDP-001）。本章ではclassificationをSynthetic teaching only、audienceをSynthetic internal roles、coordinationStatusをNot initiatedに限定する。教材の公開と、実際の脆弱性の公表許可は別である。

## 四つの視点と後続章への引継ぎ

T-15-05では、異なる役割が同じEvidenceをどこまで使えるかを示す。

| 視点 | 問い | 渡すもの |
|---|---|---|
| 攻撃評価 | どの成立条件がどの版で支持されたか | Validation、限界、停止理由 |
| 防御 | どの変更とどの観測で条件を確認するか | Control、Retest criteria、Telemetry gap |
| 分析 | 事実と仮説、支持と未観測を区別できるか | 代替説明、確信度、反証条件 |
| 意思決定 | 誰が期限付きで残るRiskを扱うか | 選択肢、Owner、期限、再評価条件 |

第16章へ必須Fieldと未観測Gap、第17章へ検知仮説、第21章へ統制の受入条件、第22章へ改善Backlog、第26章へ経営上の含意を渡す。未実装の章へリンクがあるだけで引継ぎ完了とはしない。本JSONの五Handoffはplanned-not-deliveredである。

## 安全な演習：七つの判断を比べる

Purpose: ART-04とART-23の根拠を読み、Findingの状態とRetestの結果を別々に説明する。供給された七Scenarioの差だけを扱う。

Prerequisite / Authority / Scope: 自己所有の作業コピーと、固定済み依存を導入済みの本Repositoryを使う。教材JSONは読み取り専用である。実Target・実Credential・実Networkへ操作しない。親の実行許可を変更しない。

Expected evidence / Impact: 検査は供給ID・版・有限状態と公開文書の対応を確認する。成功出力は教材整合性であって、実脆弱性や実改修の証明ではない。ローカルでPythonと固定rendererを実行する資源を使うが、評価対象への通信はしない。

Stop / Cleanup: 未知の入力、版の不一致、追跡不能、実データの疑いがあれば読解を停止する。追加取得や操作を行わない。終了時は作業メモを整理し、正本と親資料を保持する。

```bash
python3 scripts/check_chapter15_contract.py
```

コマンドは教材自体の検査であり、実ScannerやRetestツールを起動しない。先に[全Fieldの合成記入例](../cases/ch15-findings-retest-risk-example.md)を読み、次の順で自分の判断を記録する。

1. 各FindingのSymptom、Root condition、確認済みScope、未知Scopeを分ける。
2. 同じ供給値から、Temporary / Permanent / Compensatingの便益・負担・依存を比較する。
3. 各Retestの対象と変更後版を辿り、Passed / Partial / Failed / Inconclusive / Stoppedの根拠を説明する。
4. FND-FRT15-005のRetestによるClosedと、007の受容によるClosedを比較する。未修正条件を隠していないか確認する。
5. 006の期限切れと停止からReopenedを説明する。編集日ではなく供給record.asOfを基準にする。
6. 第14章のSupported/Completeや作業コピーのRecorded clearを、実改修や業務Riskゼロへ読み替えていないか点検する。

## 作成する成果物と評価基準

[ART-04 Finding Report](../templates/finding-report.md)の既存欄を埋め、[ART-23 Retest Record](../templates/retest-record.md)をFinding IDで結ぶ。[供給JSON](../cases/fixtures/ch15-findings-retest-risk.json)と[閉じたSchema](../schemas/ch15-findings-retest-risk.schema.json)はこの有限教材専用である。Schemaの構造検査だけでは、権限の実在性や参照先の正しさは証明できない。

T-15-06では、好ましい結果の件数ではなく追跡可能性を評価する。

| 観点 | 到達基準 | 未達の例 |
|---|---|---|
| 記述 | 症状・根本条件・技術影響・事業影響が分離 | Evidenceのない断定 |
| 参照 | 対象・版・Validation・Evidenceが一致 | 別Scenarioの資料へ付替え |
| 対策 | 三種類の案、Owner、期限、依存を比較 | Severityだけで修正・受容を決める |
| Retest | 変更参照・条件・観測・限界を説明 | Scanner要約だけでPassed |
| Decision | Closedの経路と受容権限・期限が明示 | 受容を実施許可に読み替える |
| Handoff | Residual、再評価、Audience、Gapの担当を残す | 未観測や未配達を完了と表示 |

## よくある誤解

- FailedはEvidence不足と同じではない。欠測はInconclusiveとして残す。
- Partialを都合のよいPassedへ丸めない。確認できない範囲を明記する。
- Acceptedは永久免責でも評価許可でもない。ClosedでもResidual riskは残り得る。
- 供給記録の時刻と現在の編集日を混同しない。教材の受容期限を毎日延長しない。
- 対象や版を省略したEvidence数の増加は、根拠の強さを保証しない。

## 章のまとめ

Findingの品質は件数ではなく、条件からEvidence、影響、対策、Retest、Decisionまでを辿れるかで決まる。結果がInconclusiveでも、不足・Owner・期限・許容結論を記録できれば教材上の成果物は完成し得る。業務課題の解決、実環境の安全、実施許可とは区別する。

## 次に学ぶこと

第16章では、Retestと判断に必要なTelemetryを取得できる条件を設計する。先に公開済みの[第17章](17-detection-engineering.md)へ進む場合は、Findingから渡した仮説と観測Gapを検知の受入条件に接続し、対応付けだけを検知成功とみなさない。

## 参考文献・Source Note ID

- SRC-IPA-VDP-001: 2024年版。役割と情報取扱い・調整の限定範囲。
- SRC-WSTG-001: 4.2固定版Reporting。Scope、Limitations、FindingとRetestの対応。
- SRC-CVSS-001: CVSS4.0 / Specification1.2 / User Guide1.2。第7章を継承したSeverityと組織判断の分離。

[2026-09-17のSource Review](../references/ch15-source-review-2026-09-17.md)に版、取得元、採用範囲と非採用範囲を記録する。本章の六Status、五Result、二条件比較は本書独自の教材契約である。
