# ホワイトハッカーとサイバーインテリジェンス実践体系

**攻撃者の行動を理解し、検証・検知・対応・経営判断につなげる**

本リポジトリは、IT Engineer Knowledge Architectureシリーズの書籍制作リポジトリです。攻撃技術の習得自体を目的にせず、脅威を理解し、許可された範囲で安全に検証し、観測・検知・対応・サイバー脅威インテリジェンス・経営判断へ変換する方法を体系化します。

- Repository: <https://github.com/itdojp/white-hat-cyber-intelligence-book>
- Public site: <https://itdojp.github.io/white-hat-cyber-intelligence-book/>
- Phase 0 Runbook: <https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/1>
- Bootstrap PR: <https://github.com/itdojp/white-hat-cyber-intelligence-book/pull/2>
- Parent proposal: <https://github.com/itdojp/it-engineer-knowledge-architecture/issues/280>
- Status: `0.1.0` editorial and publication foundation / Phase 0 in progress

## 中心となるループ

```text
判断要求を定義する
  → 資産・信頼境界・脅威を把握する
  → 攻撃経路と観測仮説を立てる
  → 許可された隔離環境で最小限に検証する
  → ログ・証拠・痕跡を評価する
  → 検知・対応・コントロールを改善する
  → 確信度付きインテリジェンスに変換する
  → 技術・運用・経営判断を記録する
  → 再評価する
```

## 現在の正本

| 対象 | 正本 |
|---|---|
| 書籍企画 | `BOOK_PROPOSAL.md` |
| 詳細目次 | `TOC.md` |
| 既存書籍との境界 | `CROSS_BOOK_MAP.md` |
| 執筆規約 | `WRITING_GUIDE.md` |
| 出典・鮮度 | `SOURCE_POLICY.md`, `references/` |
| Editorial Input計画 | `editorial-input-manifest.json`, `EDITORIAL_INPUT_MANIFEST.md` |
| 安全な公開範囲 | `SAFETY_SCOPE.md` |
| 演習環境 | `LAB_ARCHITECTURE.md` |
| 章本文 | `manuscript/` |
| 実務成果物 | `templates/` |
| 出版設定 | `book-config.json` |
| 共通部品固定 | `.book-formatter/revision.json` |

`docs/`は正本から生成する一時的なGitHub Pages sourceです。直接編集もcommitもしません。生成と非破壊buildの契約は`CANONICAL_SOURCE.md`を参照してください。

## 安全上の原則

掲載する評価・演習は、明示的に許可された自己所有環境、隔離ラボ、合成データだけを対象とします。実在する第三者システムへのスキャン、認証試行、アクセス、資格情報の取得・再利用、永続化、検知回避、破壊を目的としません。

詳細は`SAFETY_SCOPE.md`と`SECURITY.md`を参照してください。

## ローカル検証

前提:

- Node.js 24
- Python 3.11以上
- Ruby 3.3 / Bundler
- Git

固定済み`book-formatter`のcheckoutを利用する場合:

```bash
git clone https://github.com/itdojp/book-formatter.git ../book-formatter
git -C ../book-formatter checkout cf3f75ee9b1e200e4b6cece23501cb9c83170ec7
npm ci --prefix ../book-formatter --ignore-scripts

npm ci
bundle install
BOOK_FORMATTER_DIR=../book-formatter npm test
BOOK_FORMATTER_DIR=../book-formatter npm run check:book-qa
```

`BOOK_FORMATTER_DIR`を省略した場合、生成スクリプトは固定commitの共通部品を取得し、Git blob SHAを検証します。

主要コマンド:

| コマンド | 内容 |
|---|---|
| `npm test` | 編集・安全・出典・部品固定・生成決定性を検証 |
| `npm run check:editorial-inputs` | Package identity、Candidate disposition、Intake Record、raw input非追跡を検証 |
| `npm run render:editorial-inputs` | 機械可読Manifestから人間向け索引を再生成 |
| `npm run check:book-qa` | 固定formatterでCI相当の静的検査、Jekyll build、built-site smokeを再現（`BOOK_FORMATTER_DIR`必須） |
| `npm run sync:docs` | 正本から`docs/`を再生成 |
| `npm run check:docs-sync` | 2回生成の一致と正本非変更を検証 |
| `npm run build` | `docs/`生成後にJekyll build |
| `npm run serve` | ローカルpreview |

CIでは`Book Contract`と`Book QA`を実行し、`main`では同じ生成契約を使ってGitHub Pagesへdeployします。

## ライセンス

- 本文、図表、教材、テンプレート: CC BY-NC-SA 4.0
- `scripts/`および将来の`lab/`に置く自作コード: Apache License 2.0
- 第三者成果物: 原ライセンスに従い`THIRD_PARTY_NOTICES.md`へ記録

商用利用には別途契約が必要です。詳細は`LICENSE.md`を参照してください。

### 第12章の有限Identity契約

`npm run check:chapter12`はART-20の完全合成Graphと全公開Fieldを検査する。四Principal/六Path state/三Method、閉じたSchema、必要EdgeとEvidenceの版・対象整合、親RoEの非実行境界、SourceとCase表示をLayer Aで所有する。Markdown/HTML/URL解釈は共有Publication Projection1.1.0、Safetyは共有Policy1.2.0のみを使う。

検査は供給レコードの比較であり、認証・IAM・Token・一般Secret認識エンジンではない。`sync:docs`は本検査の成功後にだけ生成を開始する。詳細は`tests/fixtures/chapter12/README.md`を参照する。

### 第13章の有限Supply Chain契約

`npm run check:chapter13`はART-21の供給summaryだけを検査する。Layer Aは三Plane、八Chain、五状態、SourceからRuntimeまでのID/版/Evidence、親の非実行境界、四文書とCase全Fieldの対応を所有する。Markdown/HTML/URLは共有Projection1.1.0、安全文法は共有Policy1.2.0だけを使う。

実Cloud/CI/Registry/Package/Token/署名検証や、標準適合を実装するものではない。`sync:docs`はこの検査に成功してから生成する。有限Corpusと制限は`tests/fixtures/chapter13/README.md`を参照する。

### 第14章の有限最小影響Validation契約

`npm run check:chapter14`はART-22の八つの供給記録を検査する。Layer Aは二条件の比較、六Result、四Method、未実施/停止/Cleanup/Residual、親境界、四文書とCase全Fieldの対応を所有する。Markdown/HTML/URLは共有Projection1.1.0、安全文法は共有Policy1.2.0だけを使う。

実Replay、サービス接続、Account作成、操作・削除・残存影響の測定は実装しない。`sync:docs`は本検査の成功後にだけ生成する。有限Corpusと非目標は`tests/fixtures/chapter14/README.md`を参照する。

### 第15章の有限Finding・Retest契約

`npm run check:chapter15`はART-04/ART-23の七Findingと五Retestを検査する。Layer Aは有限選択、対象版と参照、二条件比較、六Status/五Result、受容の権限・期限・残存・再評価、親境界、五文書とCase全Field対応を所有する。Markdown/HTML/URLは共有Projection1.1.0、安全文法は共有Policy1.2.0だけを使う。

実変更、Scanner、業務承認、公開通知を実装しない。既存ART04見出しとrouteを保持する。`sync:docs`は本検査成功後だけ生成する。有限Corpusと非目標は`tests/fixtures/chapter15/README.md`を参照する。

## 第II部の横断整合

[読者向け対応表](cases/part-ii-assessment-risk-map.md)と[編集上の裁定根拠](PART_II_RECONCILIATION.md)を参照してください。Ruby/Bundlerを含む上記依存の導入後、供給JSONの参照と新ページの公開面をオフライン検査できます。実操作・通信・正本変更は行いません。不整合で失敗したら公開せず、元の章契約と対象版を確認してください。Runtimeを起動しないため破棄作業は不要です。

```bash
npm run check:part02
```

## 第16章の読解契約

[第16章](manuscript/16-telemetry-evidence-readiness.md)、[ART-24](templates/telemetry-coverage-map.md)、[全欄Case](cases/ch16-telemetry-coverage-example.md)を追加する。十の独立した合成対比を七状態・二十四receipt・必要Field・時刻・Identity・保持・Gapへ接続し、親5/6/15/17の記録を変更しない。Linux / WSL2、Python 3.12と固定依存導入後の`npm run check:chapter16`は有限Layer A検査であり、実収集・実検知・実行許可の成功ではない。Markdown構文は共有Publication Projection 1.1.0、安全文法はContent Safety Policy 1.2.0だけが所有する。

## 第18章の読解契約

[第18章](manuscript/18-threat-hunting.md)、[ART-06](templates/hunt-report.md)、[完全合成Case](cases/ch18-hunt-plan-example.md)は仮説、Coverage、有限Query/Pivot、五Result、Gapと再評価を結ぶ。Linux / WSL2、Python 3.12と固定依存導入後の`npm run check:chapter18`は四公開文書、十二の対比、四十の独立期待値を持つ有限契約である。実SIEM・実Log・実Handoffは扱わない。Layer Aだけが章固有であり、構文は共有Projection 1.1.0、安全文法はPolicy 1.2.0に委譲する。

## 第19章の読解契約

[第19章](manuscript/19-incident-response.md)、[ART-25](templates/incident-action-plan.md)、[完全合成Case](cases/ch19-incident-action-plan-example.md)は七状態と宣言・Scope・Evidence・復旧検証・残余リスクを結ぶ。Linux / WSL2、Python 3.12と固定依存導入後の`npm run check:chapter19`は四公開面と十二の独立した供給Snapshotを検査する。実IRの自動化ではなく、実操作・通知・収集は0、親のEvidence・権限・未配達は不変である。Layer Aのみ章固有、構文はProjection 1.1.0、安全文法はPolicy 1.2.0が所有する。

## 第20章 DFIRの有限契約

`npm run check:chapter20`はART-07/26、五つの正本文書全体、閉Schemaと完全合成JSON、五Receipt・二Cutoff・六Claim、親19の直接参照と非継承を検査します。共有Projection 1.1.0とPolicy 1.2.0を使い、章別rendererは持ちません。実収集・実操作・実通知は0件です。

[本文](manuscript/20-dfir-timeline-causality.md) / [全欄Case](cases/ch20-dfir-timeline-causality-example.md) / [Source確認](references/ch20-source-review-2026-09-25.md)。`sync:docs`の生成前にも正本検査を一回行います。時刻幅・Cutoff・同一性・機構不足を扱う有限教材であり、一般DFIRツールや真正性・原因の自動認定ではありません。

## 第21章 Control Validationの有限契約

`npm run check:chapter21`は四つの正本文書全体、ART-27、十Scenario・五層・六Failure、閉Schema、完全合成JSON、親14/16/17/19/20の参照と非継承を検査します。Linux / WSL2、Python 3とRepositoryの固定Ruby bundleを準備済みの環境を前提とします。依存不足なら停止し、実Targetや実Dataを追加しません。

[本文](manuscript/21-purple-team-validation.md) / [全欄Case](cases/ch21-control-validation-example.md) / [Source確認](references/ch21-source-review-2026-09-25.md)。`sync:docs`の生成前にも正本検査を一回行います。Layer Aのみ章固有であり、構文は共有Projection 1.1.0、Action/HostはPolicy 1.2.0だけが所有します。有限比較の成功は実Controlの有効性や実権限を認定しません。

## 第22章 測定と改善の有限契約

`npm run check:chapter22`は本文・ART-28・全欄Case・Sourceの四文書、閉Schema、十Metric・八Item・七Status、42の独立した算術期待値を検査します。Linux / WSL2、Python 3.11以上とRepositoryの固定Ruby bundleを前提とし、依存不足なら停止します。

[本文](manuscript/22-measurement-improvement.md) / [全欄Case](cases/ch22-improvement-backlog-example.md) / [Source確認](references/ch22-source-review-2026-09-26.md)。分母、欠測、時間の統計量、根拠binding、受容期限と廃止を有限Layer Aで扱い、構文は共有Projection 1.1.0、Action/HostはPolicy 1.2.0に委譲します。一般KPI engineや実Risk・実権限の自動認定ではありません。検査範囲は`tests/fixtures/chapter22/README.md`を参照してください。

第III部の[横断読解](cases/part-iii-detection-improvement-map.md)は、七教材の参照・非継承・未配達と限定結論を確認する補助教材です。`npm run check:part03`は有限Layer Aの接続と全公開fieldを検査し、構文と安全文法は共有Projection/Policyへ委譲します。採用根拠と移行は[整理文書](PART_III_RECONCILIATION.md)を参照してください。
