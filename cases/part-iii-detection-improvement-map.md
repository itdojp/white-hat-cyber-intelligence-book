# 第III部 横断読解：観測から改善判断へ

## この対応表の使い方

第16〜22章の七教材を、問い、参照ID、根拠の適用範囲、残るGapから読み直す。これは補助教材であり、新しいCase、Incident、許可書、配送記録ではない。登場する対象、担当、Evidence、判断は完全合成である。外部通信や実操作を行わず、リンク先の供給記録だけを読む。

**参照IDの一致は、証拠や権限の継承ではない。** 同じCase系列でも、対象・版・Scope・Windowが異なれば、元Evidenceを新対象の根拠へ付け替えない。章番号を一回の実施時系列と解釈せず、各章の独立した供給条件を保持する。

本教材のOWNは、観測上の問いから検知・対応・改善の判断までの参照と不足条件の追跡である。ATT&CK、ログ、検知設計、IR、因果、測定の判断は各章へBRIDGEする。製品操作、一般IR運用、財務・人事評価は各章のDELEGATE先へ委譲し、新しい実行手順を追加しない。

## 接続の読み方

| 接続 | 確認できること | 先取りできないこと |
|---|---|---|
| 直接ID参照 | 参照元の欄が、供給記録のどの定義を指すか | 対象の同一性、真正性、受領、許可、実施成功 |
| 比較・方法参照 | 元の問い、比較方法、記録構造、残すべき不足条件 | 元EvidenceやAuthorityを別対象の根拠として使うこと |
| 同じ対象・条件内の比較 | 固定された対象版・Window・入力条件での供給値の差 | 実改修、実測、対象外の有効性や実リスク低下 |

`refines`は判断や方法を詳しく読む関係であって、全章が同じEvidenceを共有するという意味ではない。`CASE-DET-2026-001`の名前を参照していても、Hunt、IR、DFIR、Control、改善Backlogにはそれぞれの判断対象と条件がある。

## 七章の入口と読解範囲

表のIDは既存教材のものである。各記入例から原JSONと空Templateを確認できる。版の欄を全章共通の実施Scopeと読み替えない。

| 章・合成記入例 | 入口のレコード | 対象・版の読み方 | 保持する境界 |
|---|---|---|---|
| [第16章](ch16-telemetry-coverage-example.md) | TCM-2026-016 / ART-24 | APP-TCM16-001 / TCM16-REV-001 | 十の独立対比。実収集・Deployなし |
| [第17章](ch17-detection-validation-example.md) | DVR-2026-017-001 / ART-05 | FXSET-2026-017の固定三fixture | offline replay。Coverage mappingは有効性証明ではない |
| [第18章](ch18-hunt-plan-example.md) | HUNT-2026-018-001 / ART-06 | SYNTH-HUNT18-001 / HUNT18-REV-001 | 十二対比。親Evidenceの移送なし |
| [第19章](ch19-incident-action-plan-example.md) | IAP-2026-019-001 / ART-25 | 十二のICASEごとにsubject/revision/Windowを限定 | 判断案・承認・実施・効果を分離 |
| [第20章](ch20-dfir-timeline-causality-example.md) | DFIR-2026-020-001 / ART-07・26 | SYNTH-DFIR20-001 / REV-DFIR20-001 | 親Incident IDを借用せず、二Cutoffで読む |
| [第21章](ch21-control-validation-example.md) | CVP-2026-021-001 / ART-27 | 各ScenarioのsubjectRevision/controlRevision | 層別の供給比較。実変更なし |
| [第22章](ch22-improvement-backlog-example.md) | SIB-2026-022-001 / ART-28 | 十Metricの二版と八Itemの独立した供給条件 | Verifiedは実リスク低下の認定ではない |

親Authorizationの期限`2026-08-19T09:00:00Z`、`ROE-2026-009`のv1/Draftは歴史的値のままである。後続章の作成日へ更新された許可とは扱わない。第21・22章の`parentExecutionAuthorized`と`parentLabRuntimeExecuted`はfalseである。

## 直接IDをたどり、推論を止める

欄の位置はスラッシュで区切り、配列の0は先頭要素を示す。以下は供給JSONの参照関係であり、実際に処理されたパイプラインではない。

| 参照元の欄 | 定義のある供給記録 | 推論を止める位置 |
|---|---|---|
| 第16章 `/parents/detectionId` / `/parents/detectionRecordId` | 第17章 DET-2026-017-001 / DVR-2026-017-001 | 第16章のMapだけで第17章入力契約を充足したとは言えない |
| 第18章 `/parents/telemetryMapId` / `/parents/handoffId` | 第16章 TCM-2026-016 / HOF-TCM16-18 | 対象三Rowの参照であり、受領ではない |
| 第18章 `/parents/fixtureSetId` / `/parents/threatHypothesisId` | 第17章 FXSET-2026-017 / TH-DET-2026-001 | 固定Queryの方法比較。元のEventを移送しない |
| 第19章 `/parents/huntFindingId` / `/parents/huntHandoffId` | 第18章 FND-HUNT18-001 / HOF-HUNT18-001-2 | Supportedから実Incidentを自動宣言しない |
| 第20章 `/parent/contrastId` / `/parent/decisionId` | 第19章 ICASE19-004 / DEC-IR19-004 | 親はInvestigatingの供給例。別対象の原因は未確定 |
| 第20章 `/parent/handoffId` / `/parent/questionId` | 第19章 HOF-IR19-004-20 / EQ-IR19-004-20 | TL-IR19-004は予定する親Record。自章TimelineのIDではない |
| 第21章 `/parentReferences/dfirRcaId` / `/parentReferences/dfirHandoffId` | 第20章 RCA-DFIR20-B / HOF-DFIR20-21 | CTL-DFIR20-001はhypothesis-onlyのまま |
| 第22章 `/parentReferences/controlRetestId` / `/parentReferences/parentHandoffId` | 第21章 RT-CV21-003 / HOF-CV21-22 | 親Actionを実施済みへ変えない |

第16章`HOF-TCM16-17`と第17章`HO-DET-2026-001`は異なるIDである。前者は未配達の計画、後者は`case_id / detection_id / evidence_ids / coverage / gap / permitted_conclusion`を要求するHandoff契約であり、前者を受領した履歴ではない。

第19章の`ICASE19-004`には供給例の`INC-IR19-004`がある。しかし第20章の`/record/incidentId`はnull、`incidentReferenceStatus`は`not-declared-in-this-bundle`である。新しい対象へ親Incident IDをコピーしない。第20章の`TL-DFIR20-A/B`は自章の供給Timelineである。

## Gapと限定結論を横断して読む

同じ状態名へ統一するのではなく、何を比較できたか、何が不足しているかを読む。教材の完成は、すべての観測やControlが成功した状態とは異なる。

| 章の対比 | 許される読み方 | 不適切な一般化 |
|---|---|---|
| 第16章 RequiredからValidatedまでの条件 | 生成、収集、保持、検索、時刻、必要Fieldを別々に評価する | Logがあるので全行動を検知できる |
| 第17章 negative / benign near miss / telemetry gap | 対象Event不在、正当文脈、観測不足を分ける。Gapはindeterminate | no_alertやLogなしなら侵害なし |
| 第18章 Negative finding / Inconclusive | 前者は固定Query・Window・供給Coverage内の非観測。後者は比較条件不足 | 範囲外も反証できた、または欠測を0件にする |
| 第19章 Unknown scope / Closed | 未観測範囲を残す。Closedでも改善完了を先取りしない | Unknownは影響なし、Closedなら全Backlog完了 |
| 第20章 Before / Possibly related / 原因未確定 | 時刻区間、利用可能時刻、代替説明を照合する | 時間順序が分かったので原因も確定 |
| 第21章 Failed / Partial / Indeterminate | 層別の既知の不一致、一部結果、判断条件不足を分ける | 入力欠測をPassedや全Controlの有効性へ変える |
| 第22章 件数・Mapping・速度と品質 | 母集団、分母、Window、欠測、品質を保った限定比較 | Rule増加、速度改善、Verifiedだけで実リスク低下 |

例えば第18章の対比003は限定したNegative findingだが、対比005は生成根拠の不足によるInconclusiveである。両方を「該当0件」にまとめない。第20章のCutoff Bでも`CLM20-004`は`undetermined`であり、後着記録を追加しただけで因果関係が確定するわけではない。

## Control比較からBacklog判断への一例

第21章`RT-CV21-003`と第22章`BLI-IMP22-005`を選ぶ。これは方法比較の接続であり、一件の実変更の追跡ではない。

| 段階 | 供給記録 | 保持する意味 |
|---|---|---|
| 変更前 | SCN-CV21-003 / EVD-CV21-003-01 / CTLREV-CV21-001 | 入力三種は存在するがPositiveもno-alert。DetectionはFailed |
| 比較対象の新版 | SCN-CV21-010 / EVD-CV21-010-01 / CTLREV-CV21-002 | Positiveはalert、NegativeとNear-missはno-alert。供給結果はPassed |
| 再比較 | RT-CV21-003 | before/after両方を保持。actualChangeExecutedはfalse |
| 測定の問い | MET-IMP22-008 | 固定した三出力の一致が2/3から3/3になる限定差を読む |
| 改善項目 | BLI-IMP22-005 / ACT-IMP22-005 | 親の供給比較を参照する。親Evidenceを自章の根拠へ付け替えない |
| 自章の検証 | VAL-IMP22-005 / EVD-IMP22-V005 | 別対象SYNTH-IMP22-001 / INPUT-REV-002の供給条件に束縛 |
| 判断と再評価 | DEC-IMP22-005 / REA-IMP22-005 | 供給比較はVerifiedでも、realRiskReductionMeasuredとrealEffectivenessVerifiedはfalse |

本例の再評価担当は`SYN-IMP22-OWNER-005`、期限は`2026-09-30T00:00:00Z`である。担当名や期限が記入されていることは、実業務の割当や実行許可を意味しない。個人監視、公開Ranking、懲罰KPIへ転用しない。

## 未配達のまま残すもの

次の担当・期限は供給記録上の計画値であり、本表で新たに割り当てたものではない。「将来の確認」は読解課題として不足を整理する観点で、充足済みの受領証拠ではない。

| 計画Handoff | 記録上の担当・期限（UTC） | Gapと将来の確認 |
|---|---|---|
| HOF-TCM16-18 | SYNTH-HUNT-OWNER / 2026-09-22 | 対象版、問い、必要Field、Gap、許容結論を受け手が照合 |
| HOF-HUNT18-001-2 | SYNTH-HUNT-OWNER / 2026-09-30 | Supportedの意味と代替説明をIR評価依頼として限定 |
| HOF-IR19-004-20 | SYNTH-IR-COMMANDER / 2026-09-30 | Evidence Questionと親Scopeを確認。予定Timelineの受領を推定しない |
| HOF-DFIR20-21 | SYN-DFIR-ANALYSIS-OWNER / 2026-09-30 | 原因・Control仮説の未確定部分を別の供給反例へ接続 |
| HOF-CV21-22 | SYN-CV-VALIDATION-OWNER / 2026-09-30 | 旧失敗・不足・層別結果と受入基準を保持 |
| HOF-IMP22-26 | SYN-IMP22-DECISION-OWNER / 2026-09-30 | 選択肢、費用仮定、依存、根拠と限界を判断要求へ限定 |

いずれも`planned-not-delivered`、`receiptId: null`、`executionAuthorized: false`である。期限が到来しても自動受領にはしない。第19章や第20章から第22章へ向かう他の計画も、参照先章が完成しただけでは配送完了にならない。実環境へ応用する場合の許可判断は別工程であり、この教材は代替しない。

## オフライン読解課題と評価基準

前提は本ページと七章の供給教材である。目的は参照と推論限界の説明であり、新規収集、実通知、実改修、Rule投入は実施しない。提出物は次の五行の読解メモとする。

1. 第16章と第17章のHandoff IDを区別し、第17章の必須六欄が受領証拠ではない理由を記す。
2. 第18章Negative findingの例とInconclusiveの例を一つずつ選び、Query・Window・不足条件の差を記す。
3. 第19章の評価依頼を第20章の参照欄へたどり、対象とIncident IDを借用できない理由を記す。
4. 第21章の旧Failedと新版Passedを両方残し、第22章Verifiedとの間で移せないEvidenceと権限を記す。
5. HOF-IMP22-26の担当、期限、未配達を確認し、将来の受け手が必要とする判断要求と不足条件を記す。

各行に参照元の欄、定義側ID、対象・版・Scope、利用できる結論、Gap、再評価条件を残す。供給記録にない値は補完せず「未確認」とする。

| 評価観点 | 不適切な説明 | 合格する説明 |
|---|---|---|
| 接続 | 同じCase名だから同じ実施履歴 | 定義・参照・用途を照合し、別対象への非継承を説明 |
| 非観測 | AlertもLogもないから侵害なし | 観測不足、限定非観測、正当文脈を区別 |
| 対応 | SupportedなのでIncident宣言済み | 評価依頼と供給判断、実宣言を分離 |
| 改善 | 新版Passedなので旧Failedを削除 | 旧版・新版・条件を保持し、実変更を推定しない |
| Handoff | 次章が存在するので受領済み | 未配達・nullを保持し、将来の照合条件を記す |

五行すべてで参照と非継承の理由を説明できれば読解課題の完了とする。Gapを消したり状態を成功へ変えたりすることは合格条件ではない。実Dataらしい情報、外部接続、未知の入力、許可の不明点に気付いたら読解を止め、追加取得せず不足条件を記録する。作業後は自分のメモだけを整理し、正本や供給Evidenceを変更・削除しない。Runtimeを起動しないため環境の停止・破棄は発生しない。

## 根拠と次の判断

根拠は既存の[第16章](../manuscript/16-telemetry-evidence-readiness.md)、[第17章](../manuscript/17-detection-engineering.md)、[第18章](../manuscript/18-threat-hunting.md)、[第19章](../manuscript/19-incident-response.md)、[第20章](../manuscript/20-dfir-timeline-causality.md)、[第21章](../manuscript/21-purple-team-validation.md)、[第22章](../manuscript/22-measurement-improvement.md)と各供給記録である。外部規範の新しい主張やSource版の更新はしない。法・安全・標準の適用範囲は各章のSource Noteへ戻って確認する。

次は、残した不足条件を情報要求、追加根拠の評価、意思決定へ結び付ける。[第25章 分析判断](../manuscript/25-structured-analysis-attribution.md)にも別の判断対象と根拠がある。本表からリンクしただけでEvidenceが配送され、分析の確信度が上がるわけではない。
