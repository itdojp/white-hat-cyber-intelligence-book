# 第I部（第4〜8章）横断レビュー記録

## 目的・入力・判断の所在

本記録は[Issue #19](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/19)の横断レビュー用の入力と、著者側の照合結果を固定する。章ごとの完成記録を再審査可能に接続するものであり、`GO`文字列、CI成功、合成Case内のReviewerを編集承認の代わりにしない。

- 入力baseline: `f6f8b29ee14015e57c39932fed63f8de2a7bc9f9`（PR #125の通常マージ後）。以下の観察はこの入力に対するもので、将来のmainへ自動適用しない。
- 対象: 第4〜8章の本文、Template、Case、付属JSON、Schema、章別contract、Source NoteとSource Registry。親の第1〜2章、接続先の第11・17・25章は関係の境界を照合する。
- 変更範囲: 本記録だけ。既存の本文・教材・共有Publication Projection 1.1.0・Content Safety Policy 1.2.0・出版設定・依存は変更しない。
- 独立レビューの対象は本記録の差分だけではなく、下表の正本入力である。PRの最新head、CI run、Review本文と全Threadの処置は、対応PRとIssue #19に記録する。本書内にある合成の承認・Passとは別の証跡である。
- Part完了は、独立レビューの未対応blocking指摘と未解決Threadがなく、通常の編集レビュー・マージとactual-mainの公開確認を終えてからIssue #19で判断する。本記録の追加だけで次部の開始を許可しない。

## 1. 正本と成果物の連鎖

| 章・本文 | Template | 完全合成Case | 成果物 / 子記録 |
|---|---|---|---|
| [第4章](manuscript/04-assets-boundaries-threat-model.md) | [Threat Model](templates/threat-model.md) | [第4章Case](cases/ch04-threat-model-example.md) | ART-03 / TM-2026-001 |
| [第5章](manuscript/05-attack-behavior.md) | [Behavior Map](templates/attack-behavior-map.md) | [第5章Case](cases/ch05-attack-behavior-example.md) | ART-15 / BMAP-2026-001 |
| [第6章](manuscript/06-observable-systems.md) | [Signal Flow](templates/signal-flow-diagram.md) | [第6章Case](cases/ch06-signal-flow-example.md) | ART-16 / SFM-2026-001 |
| [第7章](manuscript/07-vulnerability-prioritization.md) | [Prioritization](templates/vulnerability-prioritization-record.md) | [第7章Case](cases/ch07-vulnerability-prioritization-example.md) | ART-17 / VPR-2026-001 |
| [第8章](manuscript/08-safe-lab-evidence.md) | [Lab / Evidence Plan](templates/lab-safety-evidence-plan.md) | [第8章Case](cases/ch08-lab-evidence-example.md) | ART-18 / LABPLAN-2026-001 |

共通参照は`CASE-2026-001`、`DR-2026-001`、`AUTH-CASE-2026-001`、関係は`refines`である。第4章CaseはMarkdownの表、第5〜8章の機械可読値は各CaseからリンクするJSONを正本とする。表とJSONの一致は各章contractで照合する。

### 一つの経路を最後までたどる

以下は実際のID参照をたどる編集用の読解例であり、同じ実環境の時系列を再現した記録ではない。

1. 第4章の`TH-2026-002`から、第5章の`BM-2026-002`へ進む。Assetは`ASSET-2026-002 / 005`、Boundaryは`TB-2026-001 / 003`、Flowは`FLOW-2026-002 / 004`である。
2. `BM-2026-002`は`Observed`だが、根拠は供給された合成同意Eventだけである。親のRule欠落や`CTRL-2026-007`の`Documented`を変更しない。
3. 第6章の`SF-2026-001`は同じ親Behavior・Asset・Boundary・Flowと`GAP-BM-002`を参照する。本章独立の合成受領票は`Produced`までであり、`GAP-SF-001`は収集経路の受領票不足として残る。
4. 第7章の`VPR-ITEM-005`はこのFlowとCoverageを引き継ぎ、`Evidence first / Investigate`とする。調査予定は観測不足の解消でも緩和完了でもない。
5. 第8章の三Runは`SF-2026-001 / VPR-ITEM-005`から必要な観測・未確認条件を受け取り、`EVD-LAB08-001`へ接続する。合成receiptのPassで親Coverage、Gap、優先順位、権限を更新しない。

第5章の全7行、第6章の全6Flow、第7章の全6Record、第8章の全3Runも章contractの対象である。一つの成功経路だけで全入力の整合を代替しない。

### 状態・時点・権限を昇格させない

- 第4章のModel status、Knowledge、Hypothesis、Control assurance、Evidence Requirement、Collected Evidence、Gapは別の有限集合である。
- 第5章のMapping basisとStatus、第6章のCoverage、第7章のDeployment / Affected / Reachability / Priority、第8章の状態と判定を一つの成熟度へ変換しない。例えばBehaviorのObservedはSignalのCollectedを証明しない。
- `DR-2026-001`の過去の判断期限`2026-07-22T09:00:00+09:00`、親の`REA-2026-001`、各補足のReview日は異なる時点である。9月の教材が7月の期限を更新したり、当時の実測を後付けしたりしたとは読まない。
- `AUTH-CASE-2026-001`の条件付き判断を実作業へ転用しない。第5〜8章のScopeは`read-only-synthetic-data`。第8章の全Runは`executionAuthorized=false`で、OperationalなRoEは非発行である。
- 代表章の第11章`CASE-2026-011`と第25章`CASE-2026-025`は独立Caseである。第17章の`CASE-DET-2026-001`は親Caseのrefinementだが、限定した検知Test結果をPart全体のControl validationへ拡張しない。

## 2. 出典の版と用途

次表は各章が採用した版と範囲の照合であり、全Sourceの現行版監査やRegistryの確認日の一括更新ではない。継続更新Dataは日付付き教材入力として保持し、「最新値」や組織の現状とは呼ばない。

| 章・監査記録 | 採用範囲 | 引き継がない主張 |
|---|---|---|
| [第4章Source Note](references/ch04-source-review-2026-08-08.md) | CSF 2.0、SP 800-30 Rev.1、OWASP Threat Modelingの判断・モデル化原則 | Framework対応、Threat数、単一手法による完全性 |
| [第5章Source Note](references/ch05-source-review-2026-09-06.md) | ATT&CK catalog v19.2とObject別版、8 Objectの固定抽出、T1671 / DET0539 / AN1487・AN1488の関係 | Mappingによる侵害・主体帰属・実製品の検知有効性。旧Data SourceとData Componentの同一視 |
| [第6章Source Note](references/ch06-source-review-2026-09-12.md) | SP 800-207 / 207Aの責任分離、SP 800-92のログ管理原則、RFC 6749の役割、第5章metadataの継承 | SP 800-92 Rev.1 IPDをFinalとして採用すること、旧OAuth Grantの実装推奨、NIST由来の六Statusという主張 |
| [第7章Source Note](references/ch07-source-review-2026-09-12.md) | CVSS標準4.0と文書1.2、CWE 4.20、EPSS model v5の2026-09-11値、KEV 2026.09.11固定Catalog、OWASPのawareness用途 | 著者のCVSS仮定をvendor評価にすること、EPSSを自組織侵害確率にすること、KEV未掲載を未悪用証明にすること |
| [第8章Source Note](references/ch08-source-review-2026-09-13.md) | SP 800-86（2006）、SP 800-190（2017）、Berkeley Protocol 2022 editionの限定した記録・境界原則 | 現行Runtimeの安全保証、古いHash方式の推奨、法的証拠能力・Chain of custodyの認定 |

再照合可能な固定入力は次のとおりである。

- ATT&CK: `mitre/cti@8543c5b05bd9bbcace9fc37f30bba96b675b6f33`。Enterprise bundle SHA-256は`f7eaf37fe53b50404084fe1fe67237278f7317e61c11ad550295722d13ede259`。章別抽出器と`tests/fixtures/attack/ch05-v19.2.json`を使い、可変Webページでminor版を推定しない。
- EPSS / KEV / CWE / CVSS: [第7章Source Snapshot](cases/fixtures/ch07-source-snapshot.json)が取得日、入力hash、選択行、計算器commitを所有する。再抽出は`scripts/verify_chapter07_sources.py`を用いる。Chapter7 fixtureの値から真値を再生成して一致と呼ばない。
- 第4〜8章の本文・Source Note内のSource ID集合とRegistryの該当章mappingは、章別に`3 / 5 / 7 / 7 / 3`件、重複を除き23件で一致する。未公開章の将来mappingの整理はIssue #109の範囲であり、これを全Registryの完全性証明には使わない。

CISA指令詳細の原文を取得できなかった制約は解消扱いにしない。第7章の全6件は`requiredActionApplicability=Unverified`で、Governance Ownerへ渡す。公開CVEがないことも法的適用除外の根拠にはしない。Source Noteにある403、公開日の不明、mirror同期の限界も保持する。これは法律相談や義務の免除ではない。

## 3. 第8章から再利用するもの

再利用可能なのはTemplate、Evidenceの参照条件、Stop / Cleanup / Reassessmentの設計である。三Run専用の自動検査を、任意のラボを評価する汎用Runtimeとして使うことは再利用の意味に含めない。

- 八状態: `Planned / Preflight passed / Ready / Running / Stopped / Destroyed / Cleanup verified / Failed closed`。三判定`Safe / Unsafe / Inconclusive`とは別軸である。
- モデル1.0.0、固定レシピ識別子208、合成receipt 72件・Event 9件。乱数、現在時刻、実コンテナを使用しない。
- 必須確認のFail / Unknownでは新規シナリオ操作へ進まない。停止→Evidence export→破棄→Container / Network / Volume / File / Credential / Portの六種確認という依存関係を保持する。
- Unsafe RunはCleanup verifiedでも正常完了には戻らない。Inconclusive RunはFailed closedで終わる。未訪問の段階をPassへ補完しない。
- 実際のreceiptファイルのSHA-256は`6a4b7b5b413701cec742d25fd992c88296f54043ef44cddd07d48209fa49e9a2`。Hash一致は指定バイト列の同一性であり、合成の仮定を実測事実へ変えない。
- 読み取り専用ReplayはLinux / WSL2上のPython 3.11以上を前提とし、3教材JSON・3Schema・2親JSONを同じ固定Path読取り保護に通す。同時改変する攻撃者に対するFilesystem sandboxとは主張しない。

後続章では、次の受渡しを明記してから独自の課題を設計する。

| 行先 | 再利用する入力 | 差戻し条件 |
|---|---|---|
| 第9章 RoE | Authority / Scope、Asset / Boundary、禁止事項、停止・Evidence・復旧の候補 | 許可不明、実対象の追加、合成Passを実行許可にすること |
| 第14〜15章 最小影響確認・再評価 | 同一対象の必要Evidence、最小十分性、処置・期限・Closure条件 | 調査予定を改修完了へ昇格、別Runや別CaseのEvidence流用 |
| 第16〜17章 Telemetry / Detection | Producer、Field、期間、Clock、Coverage、Gap、Testの対象範囲 | 未収集を未検出と混同、合成のPassを実製品検証へ転用 |
| 第20章 DFIR | 実ByteのHash、Producer / Time、Lineage、Custodian / Retention | Hashだけで真実性・法的証拠能力を保証、保持EvidenceをCleanupで削除 |
| 第23〜26章 Intelligence | 出典・版、事実と仮定、代替説明、確信度、情報Gap | Mappingや未観測だけで帰属を断定、独立Caseの無断統合 |

未公開章への接続は計画であり、その章の実装・受入完了ではない。[CROSS_BOOK_MAP](CROSS_BOOK_MAP.md)のOWN / BRIDGE / DELEGATEを維持する。OS・Network・認証・コンテナの実装や個別脆弱性の操作手順をPart内へ追加しない。

## 4. 学習と出版の確認範囲

五章とも、学習目標→前提→概念・比較→安全な課題→Template→記入例→Rubric→次章の接続を持つ。第4章は一仮説を通す最小例、第5章はMappingと観測の分離、第6章は受領・保持・検索の差、第7章はScore順への反証、第8章はUnsafeとCleanup完了の併存を、読解上の確認点とする。

成果物の完成はUnknownを消すことではなく、必要Evidence、Owner、期限、許容結論、再評価条件を引き渡せることである。Rubricの得点で安全条件の欠落を相殺しない。これは編集上の導線確認であり、実読者による学習効果の実証ではない。読者試行や書籍全体の導線改善はIssue #110、全体レビューは別PR #112に残る。

本文・Template・Case・Source・公開JSONの経路は`site-pages.json`、正本と公開の対応はbuild manifestで照合する。この管理記録自体は新たな読者向け公開ページとして登録しない。未公開の第9章を公開済みNavigationへ追加しない。

既存の第4章11列テーブルのlayout warningは既知の限定として残す。本変更では表構造、章別検査の所有権、formatter pinを変更しない。章別検査の保守整理はIssue #111で扱い、新たなPart専用Markdown parserや重複した状態実装を追加しない。

## 5. 検証と独立レビューの再実行

環境導入は[AGENTS.md](AGENTS.md)と[正本・build契約](CANONICAL_SOURCE.md)に従う。固定formatterは`.book-formatter/revision.json`のcommitと一致させる。依存導入後のRepositoryルートで、既存の検査を使う。

```bash
BOOK_FORMATTER_DIR=../book-formatter npm test
BOOK_FORMATTER_DIR=../book-formatter npm run check:book-qa
python3 -B scripts/replay_chapter08_lab.py --json
```

目的は有限教材・章間参照・出典の固定値・安全境界・公開の整合確認であり、実Targetへの操作ではない。外部実測は不要である。不一致、実Dataの疑い、依存版違いで停止し、検査を省略して公開しない。生成物とcacheだけを整理し、正本・親Evidenceは保持する。初回の依存取得と、導入済み環境での検査を混同しない。

レビュー担当は、(1) 技術・状態、(2) Authority・安全・法務の限定、(3) Sourceの版・用途、(4) 分析と代替説明、(5) 学習導線、(6) OWN / BRIDGE / DELEGATE、(7) ID追跡、(8) 再現性・決定性、(9) 公開・保守性を別々に確認する。既存の不変条件に反する具体例はblockingとして再現・修正し、仕様外の新機能や全体再設計を本PRへ混在させない。

最終の検証結果は、対応PRのexact-head Book Contract / Book QA、全Review本文・Thread、通常マージ後のmain CI / Pages / 公開物に結び付ける。CIの緑表示だけ、review reactionだけ、一定時間の無応答だけでは独立レビュー完了としない。
