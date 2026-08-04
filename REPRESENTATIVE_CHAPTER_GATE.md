# 代表4章 横断レビューGate

## 1. 判定

- 対象Issue: `#8`
- 親Roadmap: `#3`
- Review baseline: `b56af680863a43017475b046ed7f9280f759844f`
- Review baselineは横断レビューへ入力した基準commitであり、Gate PRの現在headではない。PR headとlive review / CIはGitHub側の証跡で固定する
- 対象章: 第1章、第11章、第17章、第25章
- Review日: 2026-08-04
- 判定: **GO**（manual editorial decision）
- Open P0: **0**
- Open P1: **0**
- Open P2: **0**
- 独立Review evidence: [Issue #8 横断Review結果と修正状況](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/8#issuecomment-5181087925)
- 未解決Review Thread: **代表4章は0**。Gate PRは作成後にlive確認し、本Issueの完了コメントへ記録する
- 契約状態: `WRITING_GUIDE.md`をPart単位執筆へ適用可能

GOは、全30章の内容が既に完成したことを意味しない。代表章で確定したChapter Definition of Done、安全境界、Source、Case、Artifact、Review、出版契約を、Part単位Issueと章単位PRへ適用できることを意味する。

## 2. Review方法

執筆時と異なるContext / Agentを使用し、次の観点を別Passで確認した。自動検査の成功だけをレビュー完了とみなさず、本文、Template、合成Case、fixture、Registry、生成・公開契約を対応付けた。

| Pass | 観点 | 主な対象 | 結果 |
|---:|---|---|---|
| 1 | Technical accuracy | 用語、役割、ATT&CK / OWASP / IR / CTIの扱い、例とTemplate | Pass |
| 2 | Safety and legal boundary | Authority、Scope、Stop、Cleanup、実Target / Credential / PII、帰属境界 | Pass |
| 3 | Source quality | 本文使用ID、章末一覧、Registry mapping、Version / Status / date | Pass after fix |
| 4 | Analytic quality | Fact、Judgment、Assumption、Forecast、Recommendation、代替仮説、Confidence | Pass |
| 5 | Instructional design | 学習目標、Case、演習、Artifact、Rubric、Prerequisite / Next | Pass |
| 6 | Cross-book boundary | OWN / BRIDGE / DELEGATE、委譲先、重複回避 | Pass after fix |
| 7 | Artifact traceability | Decision RequirementからAction / ReassessmentまでのIDと関係 | Pass after fix |
| 8 | Publication quality | contract、QA、Jekyll、Link、Unicode、Textlint、Layout、built-site | Pass |
| 9 | Command and lab reproducibility | 第11章read-only fixture、第17章offline replay、Stop / Cleanup、期待証拠 | Pass |

## 3. 指摘と解消

| ID | Severity | 指摘 | 解消 |
|---|---|---|---|
| GATE-001 | P1 | `SRC-IANA-TLD-001`は第25章向け安全Gateで使われていたが、章本文と章末Source一覧に用途が明示されていなかった | 第25章の合成Data節と章末一覧へ、Root Zone snapshotを公開前安全Gateだけに使うことを追記した |
| GATE-002 | P1 | 代表章の実装は揃っていたが、全章へ適用するChapter Definition of DoneとPart Issue雛形が未凍結だった | `WRITING_GUIDE.md`へChapter DoDを追加し、`.github/ISSUE_TEMPLATE/part-writing.yml`を追加した |
| GATE-003 | P1 | 章別checkerはfail-closedだったが、合成Case / JSON fixtureの共通公開契約と安全レビュー証跡が一か所に固定されていなかった | `SAFETY_SCOPE.md`へ合成Dataの共通公開契約と証跡条件を追加した |
| GATE-004 | P2 | 代表章間で同一Caseを継承する場合と、独立Caseを使う場合の関係語彙が暗黙的だった | `WRITING_GUIDE.md`へ`refines` / `supersedes` / `independent`と親Case IDの規則を追加した |
| GATE-005 | P2 | 委譲Linkの可用性と、Link先を読まなくても論旨が成立する条件がDoDに明記されていなかった | `CROSS_BOOK_MAP.md`へ章単位の境界受け入れ条件を追加した |
| GATE-006 | P2 | `TOC.md`の付録H〜Jの名称・順序が`book-config.json`と一致せず、Cross-book導線を誤って案内していた | `TOC.md`を正本Configの付録H「ラボ運用ガイド」、付録I「成果物評価ルーブリック」、付録J「既存書籍との学習導線」へ同期した |
| GATE-007 | P1 | `ART-11`、`ART-05`、`ART-12`のTemplateと記入例に、観点を分離したReview証跡欄がなかった | 三つのTemplateと合成記入例へ、技術、安全、Evidence / Source、分析またはDetection、判断有用性のReview結果を追加した |
| GATE-008 | P2 | 第11章記入例のTelemetryがPartial / Missingであり、完成した教材・成果物と未解決の業務課題の区別が暗黙的だった | `WRITING_GUIDE.md`と第11章記入例へ、Gap、Owner、期限、Decision、Reassessmentが揃えば成果物は完成し得ることを明記した |
| GATE-009 | P2 | 第1章の学習成果`Workflow Map`と実務成果物`Case Map`の名称関係が、Configと代表章計画では一つの成果物名に見えた | `book-config.json`の学習目標をWorkflow MapのCase Map適用へ変更し、`REPRESENTATIVE_CHAPTER_PLAN.md`の成果物名をCase Mapへ統一した |
| GATE-010 | P1 | Gate記録のGO、local build、HTTP、visual、Review Threadの主張がRepository checkerだけで証明されるように読めた | 判定をmanual editorial decisionと明記し、機械検査とGitHub live / manual evidenceの境界、Issue evidence URL、PR作成後の未完了Gateを分離した |
| GATE-011 | P2 | 合成記入例のReview表が実際のGate review証跡と誤認され得た | Review表へ`SYNTH-REV-*` Evidence referenceを追加し、合成Case内の記入例であって実際のGate承認ではないと明記した |
| GATE-012 | P1 | Source checkerが章末一覧を本文使用IDにも数え、章末だけの未使用IDを見逃し得た | 本文領域と章末領域を分割して集合比較し、章末だけへIDを追加する負例を拒否するよう修正した |
| GATE-013 | P2 | `TOC.md`第1章の成果物名に旧`Workflow Map`表記が残っていた | 読者向けTOCを`Integrated Security Case Map（Integrated Security Workflow Mapの適用記録）`へ同期した |
| GATE-014 | P2 | 凍結契約が要求するコマンド・ラボ再現性PassがGate記録とPart Issue formへ継承されていなかった | 独立PassとIssue checklistへ`Command and lab reproducibility`を追加した |
| GATE-015 | P2 | Gate記録のReview baselineとReview日が形式・Repository履歴へ束縛されず、staleまたは不正な自己申告をRepository checkerが見逃し得た | baselineを監査済み40桁commit SHAへpinし、履歴が利用可能なら実在commitかつ`HEAD`のancestorとして検証する。shallow CIではpinを検証し、Review日をISO実在日、Review evidenceをIssue #8 comment URLとして検証するようにした |
| GATE-016 | P2 | 第1章本文に旧学習目標の説明が残り、また凍結した静的出版QAをlocalで一括再現するcommandがなかった | 第1章本文とcontractをWorkflow MapからCase Mapへの適用目標へ同期し、固定formatter SHAを検証してCI相当の静的検査・Jekyll build・built-site smokeを実行する`npm run check:book-qa`を追加した |
| GATE-017 | P2 | Review日が未来でも通り、独立Review evidence欄が壊れても文書内の別URLで検査を通過できた | Review日を実在ISO日かつ実行日以前に限定し、Issue #8 comment URLを`独立Review evidence`専用行へanchorして検査するようにした |

解消後のOpen件数はP0 / P1 / P2とも0である。

## 4. Source traceability

本文中の使用ID、章末の`参考文献・Source Note ID`、`references/sources.json`の`chapters` mappingを集合として照合する。

| 章 | 使用 / 章末 / mapping | Source Note ID |
|---:|---:|---|
| 1 | 5 / 5 / 5 | `SRC-NICE-001`, `SRC-ATTACK-001`, `SRC-CSF-001`, `SRC-IR-001`, `SRC-ICD203-001` |
| 11 | 3 / 3 / 3 | `SRC-WSTG-001`, `SRC-OWASP-TOP10-001`, `SRC-API-001` |
| 17 | 5 / 5 / 5 | `SRC-ATTACK-001`, `SRC-ATTACK-DS-001`, `SRC-ATTACK-DET-001`, `SRC-SIGMA-001`, `SRC-IR-001` |
| 25 | 5 / 5 / 5 | `SRC-ICD203-001`, `SRC-CIA-SAT-001`, `SRC-ATTACK-001`, `SRC-BERKELEY-001`, `SRC-IANA-TLD-001` |

- 未登録ID: 0
- 章mapping不一致: 0
- 代表章で未使用のmapping: 0
- 二次Sourceだけで確定した重要主張: 0
- Development資料をStableとして扱う箇所: 0
- `checkedAt`または`nextReviewAt`欠落: 0

## 5. Case・Artifact traceability

### 5.1 同一Caseの正本例

`CASE-2026-001`を、代表章での同一Case追跡の正本例とする。

```text
DR-2026-001
→ ASSET-2026-* / TH-2026-*
→ ROE-2026-001
→ VAL-2026-* / FIND-2026-*
→ TEL-2026-* / DET-2026-* / HUNT-2026-001
→ EVD-2026-* / NEG-2026-001
→ AJ-2026-001
→ DEC-2026-001 / CTRL-2026-* / REA-2026-001
```

第17章の`CASE-DET-2026-001`と`DET-2026-017-001`は、このCaseの`CASE-2026-001`、`DEC-2026-001`、`DET-2026-001`、`FIX-CONSENT-001`、`CTRL-2026-003`を`refines`する。親Recordを置換または再配備しない。

### 5.2 独立Case

- 第11章: `CASE-2026-011` / `ART-11`
- 第25章: `CASE-2026-025` / `ART-12`

これらは異なるDecision Requirementを扱う独立Caseである。見かけ上の章間連続性を作るために`CASE-2026-001`へ統合しない。各Case内ではEvidence、FindingまたはJudgment、Decision、Reassessmentまで直接追跡できる。

### 5.3 Artifact ID

| 章 | Artifact | Template | 合成記入例 / fixture |
|---:|---|---|---|
| 1 | `ART-10` | `templates/integrated-security-case-map.md` | `cases/ch01-integrated-security-case-example.md` |
| 11 | `ART-11` | `templates/web-api-assessment-hypothesis-pack.md` | `cases/ch11-web-api-assessment-example.md` / 読み取り専用JSON |
| 17 | `ART-05` | `templates/detection-validation.md` | `cases/ch17-detection-validation-example.md` / オフラインReplay |
| 25 | `ART-12` | `templates/analytic-judgment-record.md` | `cases/ch25-structured-analysis-attribution-example.md` / 読み取り専用JSON |

Artifact IDの重複定義とTemplate不一致は0件である。

## 6. Safety and legal result

- 禁止された実在Target: 0
- 実Credential、Token、Cookie、秘密鍵: 0
- PIIまたは実在連絡先: 0
- 第三者へ転用できる高リスク実行手順: 0
- Authority / Scope / Stop / Cleanupの必須要素欠落: 0
- 証拠を超えたActor / 組織 / 国家の帰属: 0
- JSON fixtureの合成境界・予約Domain・文書用IP違反: 0

一般的な人名・住所を完全に判定する汎用PII検出器ではないため、自由記述は機械検査だけで承認せず、独立した安全レビューを継続する。

## 7. Cross-book boundary result

- 第11章はWeb/APIの仮説、Evidence、Detection handoffをOWN / BRIDGEし、Payload・Tool別の詳細と認証実装を専門書へDELEGATEする
- 第17章はDetection lifecycle、Telemetry contract、fixture validationをOWNし、製品固有のSIEM / EDR実装をDELEGATEする
- 第25章は構造化分析、不確実性、帰属停止線をOWNし、実在主体調査や法執行機関連携を対象外とする
- 委譲先を読まなくても各章の中心論旨は成立する
- 安定した公開Linkを使い、可用性はPR時と定期監査で確認する

## 8. Publication evidence

代表章のmerge結果とGate候補worktreeのlocal検証で次を確認した。Gate PR / main / Pagesのlive状態は、この記録へ自己申告として固定せず、後述の外部Gateでcommitとrunへ結び付ける。

- `npm ci`: audit 0
- `npm test`: Pass
- `BOOK_FORMATTER_DIR=<audited checkout> npm run check:book-qa`: Pass。固定formatter SHAの一致、静的検査、Jekyll build、built-site smokeを一括再現
- Chapter 1 / 11 / 17 / 25 contract: Pass
- Chapter 17 offline replay: positive / negative / benign / coverage-gap契約がPass
- Source baseline: deterministic and in sync
- Site source generation: deterministic、Canonical source非変更
- Jekyll build / built-site smoke: 代表章PRとGate候補worktreeのlocal QAで確認。Gate PR CIは外部Gateで別途確認する
- Link / Anchor / Unicode / Textlint / Layout / Markdown structure: error 0
- Gate候補のlocal build: 44 pages、3 static artifacts、6 assets、第三者Notice 1件をsmoke確認
- Cross-book link: 第11章とTemplateの委譲先6 URLがHTTP 200
- Visual: topと代表4章をdesktop 1440×1200 / mobile 390×844で確認し、CSS / mobile CSS / JavaScriptの取得はすべてHTTP 200、判読不能・重なり・意図しない横方向欠落は0件
- 生成物`docs/` / `_site/`: commit 0
- 代表章PRの未解決Review Thread: 0

Gate PRでは、`scripts/check_representative_gate.py`によりSource集合、Artifact、Case関係、凍結契約、Part Issue template、GO判定を継続検査する。
Source mapping不一致、Review見出し欠落、GO判定欠落、不正baseline、不正Review日、不一致formatter checkout、未来のReview日、専用欄が壊れたReview evidenceの八つの負例を一時変異で検証し、8 / 8を拒否した。検証後は正本を復元し、positive gateを再実行した。

### 証跡と保証範囲

`scripts/check_representative_gate.py`は、本文領域・章末一覧・Registry mappingのSource集合、Artifact / Case関係、正確なReview見出し、合成Review Evidence ID、凍結文書、Part Issue form、本記録の必須構造を検査する。Review baselineは監査済み40桁SHAへのpinであり、履歴が利用可能なら実在commitかつ`HEAD`のancestorであることを検査する。shallow CIでは固定pinを検査する。Review日はISO実在日かつ実行日以前、独立Review evidenceは専用行のIssue #8 comment URLであることを検査する。

**Repository checker does not validate GitHub live state.** 次は外部Gateであり、Repository内の`GO`文字列だけでは完了扱いにしない。

- GitHubのreview本文、inline、suggestion、thread
- PR / main CIとartifact
- Pages deploymentと公開HTTP / marker
- desktop / mobileの人手visual判断

これらは[Issue #8の進捗証跡](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/8#issuecomment-5181087925)、Gate PR、完了コメントでcommit / run / URLへ結び付ける。`scripts/check_representative_gate.py`の成功は、外部Gateの成功を代替しない。

## 9. 全章展開時の運用

1. Partごとに`part-writing.yml`からIssueを作成する
2. 依存順、章ごとのPR分割、Source、Artifact、Case関係、安全境界を先に確定する
3. 一つの章を一つの主目的PRとして実装する
4. 章固有contractと共通Chapter DoDを通す
5. 執筆と異なるContextで各Review Passを実施する
6. P0 / P1と未解決Threadを0にしてから次章へ進む
7. 契約変更が必要ならPart PRへ混在させず、Gate契約変更Issueを作成する
