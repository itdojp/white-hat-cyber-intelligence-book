# 付録B 実務テンプレート集

## この付録で判断すること

自分の問いにどの成果物を使い、最初にどの欄へ記入するかを選ぶ。ここはTemplate本文を複製する場所ではなく、空欄、合成記入例、供給Fixture、章の評価基準へ戻る索引である。[成果物主索引](../artifact-index.md)と同じArtifactを扱う。

初めて読む場合は、[Quick Start](../quickstart.md)から[最小読解ガイド](../cases/first-artifact-walkthrough.md)へ進み、ART-10の空TemplateでCase IDとDecision Requirementを確認する。各カードの「必須ID・最初の記入先」を入口とし、関連ID・必須項目は元Template全体で確認する。この索引に短く書かれていることは、元欄を省略する許可ではない。

## 資料を混ぜない

- Templateは記入先であり、記入済みのEvidenceではない。自分の作業Copyへ、完全合成の教材と読解メモだけを書く。
- Exampleは供給された合成記入例であり、実対象の観測・承認・配達を証明しない。過去Caseの時点・Authority・親の状態を現在へ付け替えない。
- Fixtureは比較用の供給入力である。DownloadリンクがあるJSONも読み取り専用であり、Templateとして上書きしない。
- 共通のStatusを新設しない。Document、Result、Control、配達等の対象を特定し、値と条件は元章へ戻る。ART-01のように共通Statusや再評価ID欄を持たない成果物へ架空の欄を足さない。

Evidenceが未収集ならNot collected、入力があっても問いを判断できなければInconclusiveとして、その理由・担当・次確認を区別する。未観測を「問題なし」にせず、記入完了とControlの検証を分ける。許可・Scope・出所が不明、実Dataや外部接続が必要になった場合は停止し、[付録A](appendix-a-legal-safety.md)と元章へ戻る。実データ収集や現実の対象への操作は行わない。

## 成果物別の記入先

以下は横断Artifact metadataから生成する区画である。件数を手で合わせず、現行の主索引と親文書の版を検査する。説明は記入順の索引であり、元Templateの全欄・状態定義を置き換えない。

生成索引開始（BCI_GENERATED_START）

### ART-01 Learning Route Plan

- 目的: 役割と学習の不足から読書順を選ぶ。
- 入力: 現在の役割、目標、前提知識。
- 出力: 学習Routeと月次に見直すEvidence。
- 主担当章: [第0章](../manuscript/00-reading-guide.md)。主索引の関連章: 0。
- Template（空欄）: [元Template](../templates/learning-route-plan.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch03-capability-evidence-example.md)。
- Fixture / Download: 独立したJSONの登録なし。上の合成記入例を読む。
- [必須ID・最初の記入先](../templates/learning-route-plan.md#learning-route-plan): Plan IDとLearner Profile IDから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/learning-route-plan.md#learning-route-plan): 共通Document Statusは未定義。月次レビュー日を進捗や能力のStatusへ変換しない。
- [Owner](../templates/learning-route-plan.md#learning-route-plan): 共通Owner欄は未定義。Learner Profileと現在・目標の役割を確認する。業務上の承認者を推定しない。
- [Review](../templates/learning-route-plan.md#learning-route-plan): 月次レビュー日と学習の証拠を使う。独立Reviewer欄は未定義で、学習者の記入を実承認へ読み替えない。
- [Reassessment](../templates/learning-route-plan.md#learning-route-plan): 再評価ID欄は未定義。月次レビュー日で目的・前提知識・読書順を見直す。

### ART-02 Rules of Engagement

- 目的: 作業開始の可否と条件を記録する。
- 入力: Authority根拠、対象、方法、時間・量の制約。
- 出力: RoEのDecision、停止・変更・再承認条件。
- 主担当章: [第9章](../manuscript/09-engagement-roe.md)。主索引の関連章: 9。
- Template（空欄）: [元Template](../templates/rules-of-engagement.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch09-engagement-roe-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch09-engagement-roe.json)。
- [必須ID・最初の記入先](../templates/rules-of-engagement.md#1-document-controlとdecision): RoE ID・Version・Case・Decision Requirementから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/rules-of-engagement.md#1-document-controlとdecision): RoEのStatusとDecisionを分ける。Approvedだけで実作業を開始しない。
- [Owner](../templates/rules-of-engagement.md#2-authorization-evidenceと役割): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/rules-of-engagement.md#12-approval-checklist): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/rules-of-engagement.md#10-changereauthorizationretest): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-03 Threat Model

- 目的: 守る対象と境界から必要なEvidenceを決める。
- 入力: 判断要求、Asset、Flow、既知のControl。
- 出力: Threat仮説、Gap、Action、Handoff。
- 主担当章: [第4章](../manuscript/04-assets-boundaries-threat-model.md)。主索引の関連章: 4。
- Template（空欄）: [元Template](../templates/threat-model.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch04-threat-model-example.md)。
- Fixture / Download: 独立したJSONの登録なし。上の合成記入例を読む。
- [必須ID・最初の記入先](../templates/threat-model.md#0-document-control): Threat Model ID・Parent Case IDから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/threat-model.md#0-document-control): Model、Knowledge、Hypothesis、Control、Evidence、Actionの状態は別の欄である。
- [Owner](../templates/threat-model.md#0-document-control): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/threat-model.md#12-review-and-rubric): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/threat-model.md#11-reassessment-and-handoff): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-04 Finding Report

- 目的: Findingの根拠と対応判断を結ぶ。
- 入力: 同じ対象版のEvidenceとValidation記録。
- 出力: 影響、Treatment案、残余リスク、Decision。
- 主担当章: [第15章](../manuscript/15-findings-retest-risk.md)。主索引の関連章: 15。
- Template（空欄）: [元Template](../templates/finding-report.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch15-findings-retest-risk-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch15-findings-retest-risk.json)。
- [必須ID・最初の記入先](../templates/finding-report.md#finding-report): Finding ID・Case ID・対象版から記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/finding-report.md#finding-report): Finding StatusはRetest Resultや受容の根拠と別に記録する。
- [Owner](../templates/finding-report.md#residual-risk-and-owner): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/finding-report.md#residual-risk-and-owner): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/finding-report.md#residual-risk-and-owner): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-05 Detection Validation Record

- 目的: Detectionの期待と供給結果を照合する。
- 入力: 仮説、Telemetry契約、合成Fixture、Ruleの版。
- 出力: Validation結果、Coverage限界、次の改善。
- 主担当章: [第17章](../manuscript/17-detection-engineering.md)。主索引の関連章: 17。
- Template（空欄）: [元Template](../templates/detection-validation.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch17-detection-validation-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch17-detection-engineering-fixture.json)。
- [必須ID・最初の記入先](../templates/detection-validation.md#0-document-control): Detection Validation Record ID・Case IDから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/detection-validation.md#0-document-control): Document Statusは個々のValidation Result・Coverage・実Control有効性と別である。
- [Owner](../templates/detection-validation.md#0-document-control): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/detection-validation.md#11-review): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/detection-validation.md#9-control-improvement-and-reassessment): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-06 Hunt Plan and Findings

- 目的: Hunt仮説に対して言える範囲を記す。
- 入力: Scope、Coverage、供給合成入力、反証条件。
- 出力: Finding、Judgment、Gap、未配達Handoff。
- 主担当章: [第18章](../manuscript/18-threat-hunting.md)。主索引の関連章: 18。
- Template（空欄）: [元Template](../templates/hunt-report.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch18-hunt-plan-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch18-threat-hunting.json)。
- [必須ID・最初の記入先](../templates/hunt-report.md#hunt-plan-and-findings): Hunt ID・Record revision・Case IDから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/hunt-report.md#findings): Hunt ResultとHandoffの配達状態を区別する。
- [Owner](../templates/hunt-report.md#judgments): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/hunt-report.md#judgments): 独立Review欄は未定義。Judgmentsの根拠・限界を第18章の評価基準と照合する。記入を実承認へ読み替えない。
- [Reassessment](../templates/hunt-report.md#follow-up): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-07 Incident Timeline

- 目的: 時刻の不確かさを保ったTimelineを作る。
- 入力: 原Record、Clock条件、Cutoff。
- 出力: 時刻幅、Event間Relation、未確定事項。
- 主担当章: [第20章](../manuscript/20-dfir-timeline-causality.md)。主索引の関連章: 20。
- Template（空欄）: [元Template](../templates/incident-timeline.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch20-dfir-timeline-causality-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch20-dfir-timeline-causality.json)。
- [必須ID・最初の記入先](../templates/incident-timeline.md#基本識別情報と境界): Timeline ID・Version・Incident IDから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/incident-timeline.md#analytic-judgments): Event間Relationは文書全体の承認Statusではない。Scopeと原因未確定も別に記す。
- [Owner](../templates/incident-timeline.md#基本識別情報と境界): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/incident-timeline.md#review-and-cleanup): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/incident-timeline.md#gaps-and-collection-actions): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-08 CTI Report

- 目的: 判断要求に答える技術向けProductを作る。
- 入力: Requirement、Evidence、Source評価、Key Judgment。
- 出力: 技術・運用向けReportと配布制約。
- 主担当章: [第26章](../manuscript/26-cti-distribution.md)。主索引の関連章: 26。
- Template（空欄）: [元Template](../templates/cti-report.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch26-cti-distribution-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch26-cti-distribution.json)。
- Fixture 2（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch26-stix-bundle.json)。
- Fixture 3（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch26-taxii-exchange.json)。
- [必須ID・最初の記入先](../templates/cti-report.md#document-control--scope): Product ID・Case・Versionから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/cti-report.md#有限statusと教材の範囲): Product StatusとFeedback Statusを分け、配達はReceiptで確認する。
- [Owner](../templates/cti-report.md#document-control--scope): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/cti-report.md#document-control--scope): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/cti-report.md#feedback--correction--supersede): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-09 Executive Brief

- 目的: 同じ根拠を意思決定向けに整理する。
- 入力: ART-08と共通のEvidenceとKey Judgment。
- 出力: Option、推奨、条件、未決事項。
- 主担当章: [第26章](../manuscript/26-cti-distribution.md)。主索引の関連章: 26、29。
- Template（空欄）: [元Template](../templates/executive-brief.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch26-cti-distribution-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch26-cti-distribution.json)。
- Fixture 2（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch26-stix-bundle.json)。
- Fixture 3（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch26-taxii-exchange.json)。
- [必須ID・最初の記入先](../templates/executive-brief.md#decision-required): Product ID・Version・Requirement・Decision IDから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/executive-brief.md#安全境界と有限status): Product・Decision・Feedbackの状態を区別し、推奨を承認へ昇格させない。
- [Owner](../templates/executive-brief.md#decision-required): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/executive-brief.md#distribution--feedback): 独立Reviewer欄は未定義。配布条件・Feedbackと第26章の評価基準を照合し、未受領の回答を作らない。
- [Reassessment](../templates/executive-brief.md#conditions-and-triggers): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-10 Integrated Security Case Map

- 目的: 証拠から判断・再評価までの接続を記録する。
- 入力: Caseの問い、許可境界、供給Evidence。
- 出力: Case Map、判断できることと残るGap。
- 主担当章: [第1章](../manuscript/01-integrated-discipline.md)。主索引の関連章: 1、29。
- Template（空欄）: [元Template](../templates/integrated-security-case-map.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch01-integrated-security-case-example.md)。
- Fixture / Download: 独立したJSONの登録なし。上の合成記入例を読む。
- [必須ID・最初の記入先](../templates/integrated-security-case-map.md#0-document-control): Case IDとDecision Requirement IDから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/integrated-security-case-map.md#0-document-control): CaseのDocument Statusと個別Evidence・Control・Decisionを区別する。
- [Owner](../templates/integrated-security-case-map.md#0-document-control): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/integrated-security-case-map.md#16-review): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/integrated-security-case-map.md#12-reassessment): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-11 Web/API Assessment Hypothesis Pack

- 目的: Web/API評価の問いと境界を具体化する。
- 入力: Asset、Actor、Boundary、Workflow、親要求。
- 出力: 仮説、限定Validation案、Finding・Detectionへの接続。
- 主担当章: [第11章](../manuscript/11-web-api-hypothesis.md)。主索引の関連章: 11。
- Template（空欄）: [元Template](../templates/web-api-assessment-hypothesis-pack.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch11-web-api-assessment-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch11-web-api-assessment-dataset.json)。
- [必須ID・最初の記入先](../templates/web-api-assessment-hypothesis-pack.md#0-document-control): Case IDとDecision Requirement IDから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/web-api-assessment-hypothesis-pack.md#0-document-control): Document StatusとHypothesis、Evidence、Handoffの状態を混ぜない。
- [Owner](../templates/web-api-assessment-hypothesis-pack.md#0-document-control): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/web-api-assessment-hypothesis-pack.md#11-review): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/web-api-assessment-hypothesis-pack.md#7-reassessment-plan): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-12 Analytic Judgment Record

- 目的: 競合仮説と不確実性を判断へ結ぶ。
- 入力: 判断要求、Source Note、Evidence、代替説明。
- 出力: 限定Judgment、確信度、指標、再評価条件。
- 主担当章: [第25章](../manuscript/25-structured-analysis-attribution.md)。主索引の関連章: 25、29。
- Template（空欄）: [元Template](../templates/analytic-judgment-record.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch25-structured-analysis-attribution-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch25-structured-analysis-attribution-dataset.json)。
- [必須ID・最初の記入先](../templates/analytic-judgment-record.md#0-document-control): Case IDとDecision Requirement・Intelligence Requirementから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/analytic-judgment-record.md#0-document-control): Document Statusと個々のJudgment・Source用途を混ぜない。
- [Owner](../templates/analytic-judgment-record.md#0-document-control): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/analytic-judgment-record.md#15-review): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/analytic-judgment-record.md#13-reassessment-and-invalidation): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-13 Authorization Checklist

- 目的: Authority・Scope・Safety・Disclosureを点検する。
- 入力: 権限根拠、対象、Data、停止・開示条件。
- 出力: Gate判断、Condition、RoEへの差戻し条件。
- 主担当章: [第2章](../manuscript/02-law-ethics-authorization.md)。主索引の関連章: 2、9。
- Template（空欄）: [元Template](../templates/authorization-checklist.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch02-authorization-decision-example.md)。
- Fixture / Download: 独立したJSONの登録なし。上の合成記入例を読む。
- [必須ID・最初の記入先](../templates/authorization-checklist.md#0-document-control): Authorization Record ID・Parent Case IDから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/authorization-checklist.md#0-document-control): Document Status、Gate、Decision、Conditionの状態を分ける。
- [Owner](../templates/authorization-checklist.md#0-document-control): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/authorization-checklist.md#12-review): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/authorization-checklist.md#10-reassessment): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-14 Capability Evidence Matrix

- 目的: 学習Evidenceから限定した能力判断を行う。
- 入力: 親Plan、Task、事前Rubric、Practice記録。
- 出力: ArtifactのReview結果、能力Claim、Gapと次の学習。
- 主担当章: [第3章](../manuscript/03-capability-evidence.md)。主索引の関連章: 3、29。
- Template（空欄）: [元Template](../templates/capability-evidence-matrix.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch03-capability-evidence-example.md)。
- Fixture / Download: 独立したJSONの登録なし。上の合成記入例を読む。
- [必須ID・最初の記入先](../templates/capability-evidence-matrix.md#0-document-control): Matrix ID・Learner Profile ID・Parent Plan IDから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/capability-evidence-matrix.md#0-document-control): 学習Lifecycle、Artifact Review Result、Capability Claim Resultを分ける。
- [Owner](../templates/capability-evidence-matrix.md#0-document-control): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/capability-evidence-matrix.md#5-review-result): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/capability-evidence-matrix.md#7-reassessment): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-15 ATT&CK Behavior Map

- 目的: 行動のMappingと観測・検証を分離する。
- 入力: Behavior、ATT&CKの版、Mapping根拠。
- 出力: 行ごとの状態、Evidence、Gap、判断寄与。
- 主担当章: [第5章](../manuscript/05-attack-behavior.md)。主索引の関連章: 5。
- Template（空欄）: [元Template](../templates/attack-behavior-map.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch05-attack-behavior-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch05-attack-behavior.json)。
- [必須ID・最初の記入先](../templates/attack-behavior-map.md#document-control): Map ID・Parent Case ID・Decision Requirementから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/attack-behavior-map.md#statusとevidence-threshold): 行ごとのMapping・観測・検証の状態。件数だけでControlの有効性を認定しない。
- [Owner](../templates/attack-behavior-map.md#document-control): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/attack-behavior-map.md#reviewとcleanup): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/attack-behavior-map.md#decisionとreassessment): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-16 Signal Flow Diagram

- 目的: 観測の各段階と不足を追跡する。
- 入力: Flow、Event、Field、Scope、時点。
- 出力: 生成・収集・保持・検索・検証のEvidence対応。
- 主担当章: [第6章](../manuscript/06-observable-systems.md)。主索引の関連章: 6。
- Template（空欄）: [元Template](../templates/signal-flow-diagram.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch06-signal-flow-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch06-signal-flow.json)。
- [必須ID・最初の記入先](../templates/signal-flow-diagram.md#document-control): Signal Flow Map ID・Case ID・Parent Behaviorから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/signal-flow-diagram.md#coverageと受入条件): Flowの段階状態。前段のEvidenceだけで後段を満たしたとはしない。
- [Owner](../templates/signal-flow-diagram.md#document-control): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/signal-flow-diagram.md#handoffとrubric): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/signal-flow-diagram.md#flowの記入): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-17 Vulnerability Prioritization Record

- 目的: 公開指標を環境条件と判断へ結ぶ。
- 入力: 指標の版、導入・影響・到達条件、Control。
- 出力: 優先度の理由、Owner、期限、残余リスク。
- 主担当章: [第7章](../manuscript/07-vulnerability-prioritization.md)。主索引の関連章: 7。
- Template（空欄）: [元Template](../templates/vulnerability-prioritization-record.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch07-vulnerability-prioritization-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch07-source-snapshot.json)。
- Fixture 2（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch07-vulnerability-prioritization.json)。
- [必須ID・最初の記入先](../templates/vulnerability-prioritization-record.md#document-control): Record Set・Item ID・Parent・Decision Requirementから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/vulnerability-prioritization-record.md#decisionと再評価): 優先度判断とControl・Closureの根拠は別。公開指標の大小を共通Statusにしない。
- [Owner](../templates/vulnerability-prioritization-record.md#document-control): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/vulnerability-prioritization-record.md#rubricと記入例): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/vulnerability-prioritization-record.md#decisionと再評価): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-18 Lab Safety and Evidence Plan

- 目的: ラボの境界と供給Evidenceを確認する。
- 入力: 許可、Lab構成、合成Receipt、停止条件。
- 出力: 八状態と三判定、Evidence manifest、Cleanup・再評価。
- 主担当章: [第8章](../manuscript/08-safe-lab-evidence.md)。主索引の関連章: 8。
- Template（空欄）: [元Template](../templates/lab-safety-evidence-plan.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch08-lab-evidence-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch08-control-receipts.json)。
- Fixture 2（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch08-evidence-manifest.json)。
- Fixture 3（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch08-lab-plan.json)。
- [必須ID・最初の記入先](../templates/lab-safety-evidence-plan.md#document-control): Plan Set・Plan・Run・Lab IDとCaseから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/lab-safety-evidence-plan.md#八状態と三判定): Lab八状態と三判定を分ける。Runningを許可やCleanup成功へ読み替えない。
- [Owner](../templates/lab-safety-evidence-plan.md#document-control): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/lab-safety-evidence-plan.md#rubricと完全記入例): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/lab-safety-evidence-plan.md#stop--cleanup--reassessment): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-19 Attack Surface Register

- 目的: Asset候補の所有と確認範囲を整理する。
- 入力: Collection Requirement、Source、時点、Provenance。
- 出力: 候補のVerification、Gap、次Actionの承認不足。
- 主担当章: [第10章](../manuscript/10-recon-osint-boundary.md)。主索引の関連章: 10。
- Template（空欄）: [元Template](../templates/attack-surface-register.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch10-attack-surface-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch10-attack-surface.json)。
- Fixture 2（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch10-source-bundle.json)。
- [必須ID・最初の記入先](../templates/attack-surface-register.md#1-document-controlと要求): Register ID・Case ID・Decision / Collection Requirementから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/attack-surface-register.md#5-verificationと許容結論): Verification stateとOwnership statusは別の語彙である。
- [Owner](../templates/attack-surface-register.md#1-document-controlと要求): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/attack-surface-register.md#記入例と評価): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/attack-surface-register.md#6-次actiongap再評価): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-20 Identity Attack Path Review

- 目的: Identityの必要Edgeと未確認点を評価する。
- 入力: Principal、Role、Permission、Resource、対象版。
- 出力: Path Review、Telemetry、Finding、Treatment案。
- 主担当章: [第12章](../manuscript/12-enterprise-identity.md)。主索引の関連章: 12。
- Template（空欄）: [元Template](../templates/identity-attack-path-review.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch12-identity-path-review-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch12-identity-paths.json)。
- [必須ID・最初の記入先](../templates/identity-attack-path-review.md#document-controlとdecision-requirement): Review ID・Case ID・Decision Requirementから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/identity-attack-path-review.md#path-review): Path stateとPrincipal・Edge・認証条件の記録を区別する。
- [Owner](../templates/identity-attack-path-review.md#document-controlとdecision-requirement): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/identity-attack-path-review.md#提出前の確認): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/identity-attack-path-review.md#telemetryfindingtreatmentreassessment): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-21 Platform and Supply Chain Assessment

- 目的: PlatformとSupply Chainの信頼主張を限定する。
- 入力: Source、Lock、Builder、Artifact、Runtimeの供給資料。
- 出力: 状態別根拠、Finding、Decision、再評価。
- 主担当章: [第13章](../manuscript/13-platform-supply-chain.md)。主索引の関連章: 13。
- Template（空欄）: [元Template](../templates/platform-supply-chain-assessment.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch13-platform-supply-chain-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch13-supply-chain.json)。
- [必須ID・最初の記入先](../templates/platform-supply-chain-assessment.md#authority--scope--safety): Assessment ID・Case ID・Service ID・RoE IDと版から記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/platform-supply-chain-assessment.md#stateと判断の規則): 対象層の五状態は署名・Trust・Compliance・実許可と同義ではない。
- [Owner](../templates/platform-supply-chain-assessment.md#authority--scope--safety): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/platform-supply-chain-assessment.md#stop--cleanup--rubric): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/platform-supply-chain-assessment.md#記入欄): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-22 Minimal-Impact Validation Record

- 目的: 最小十分なEvidenceと停止条件を結ぶ。
- 入力: 問い、Authority、対象版、供給Validation。
- 出力: 支持・反証・未観測、残存、Handoff。
- 主担当章: [第14章](../manuscript/14-minimal-impact-validation.md)。主索引の関連章: 14。
- Template（空欄）: [元Template](../templates/minimal-impact-validation-record.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch14-minimal-impact-validation-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch14-minimal-impact-validation.json)。
- [必須ID・最初の記入先](../templates/minimal-impact-validation-record.md#識別と境界): Record ID・Case・Hypothesis・Authority参照から記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/minimal-impact-validation-record.md#判断とhandoff): Resultと実施有無を分ける。未実施をSupportedにしない。
- [Owner](../templates/minimal-impact-validation-record.md#識別と境界): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/minimal-impact-validation-record.md#停止と残存確認): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/minimal-impact-validation-record.md#判断とhandoff): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-23 Retest Record

- 目的: 変更後のRetest条件と限界を記録する。
- 入力: Finding、Change参照、対象・変更前後版。
- 出力: Retest結果、Residual、再評価条件。
- 主担当章: [第15章](../manuscript/15-findings-retest-risk.md)。主索引の関連章: 15。
- Template（空欄）: [元Template](../templates/retest-record.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch15-findings-retest-risk-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch15-findings-retest-risk.json)。
- [必須ID・最初の記入先](../templates/retest-record.md#t-15-07-retestの記入欄): Retest ID・Finding ID・変更前後の対象版から記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/retest-record.md#判断を残す): Retest ResultとFinding Statusを分ける。Closedの理由はART-04へ戻す。
- [Owner](../templates/retest-record.md#t-15-07-retestの記入欄): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/retest-record.md#判断を残す): 判断の根拠をART-04と第15章の評価基準へ戻す。Retestの記入をRisk acceptanceや実承認と同義にしない。
- [Reassessment](../templates/retest-record.md#t-15-07-retestの記入欄): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-24 Telemetry Coverage Map

- 目的: 問いに必要なTelemetryの充足を記す。
- 入力: 必要Field、Consumer、期間、品質根拠。
- 出力: Coverage状態、Gap、有限ValidationとHandoff。
- 主担当章: [第16章](../manuscript/16-telemetry-evidence-readiness.md)。主索引の関連章: 16。
- Template（空欄）: [元Template](../templates/telemetry-coverage-map.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch16-telemetry-coverage-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch16-telemetry-coverage.json)。
- [必須ID・最初の記入先](../templates/telemetry-coverage-map.md#1-document-controlと親参照): Map ID・Case・Threat / Observation / Signal Flowから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/telemetry-coverage-map.md#4-coverageとvalidation): Coverage状態とHandoffの配達状態を分ける。
- [Owner](../templates/telemetry-coverage-map.md#1-document-controlと親参照): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/telemetry-coverage-map.md#6-読解の完了停止cleanup): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/telemetry-coverage-map.md#4-coverageとvalidation): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-25 Incident Action Plan

- 目的: 対応判断の根拠と選択肢を分離する。
- 入力: Signal、Scope、Evidence、判断権限の条件。
- 出力: Decision Log、対応案、復旧検証条件、残余。
- 主担当章: [第19章](../manuscript/19-incident-response.md)。主索引の関連章: 19。
- Template（空欄）: [元Template](../templates/incident-action-plan.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch19-incident-action-plan-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch19-incident-response.json)。
- [必須ID・最初の記入先](../templates/incident-action-plan.md#identity-and-roles): Incident・Case・Parent Case ID・Decision IDから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/incident-action-plan.md#classification-and-scope): Incident StatusをClassification、Severity、PriorityやScopeと混ぜない。
- [Owner](../templates/incident-action-plan.md#identity-and-roles): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/incident-action-plan.md#traceability-and-reassessment): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/incident-action-plan.md#traceability-and-reassessment): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-26 Root Cause Analysis

- 目的: 原因仮説と代替説明を照合する。
- 入力: Timeline、機構Evidence、限定影響。
- 出力: 原因未確定の理由、改善案、検証と再評価。
- 主担当章: [第20章](../manuscript/20-dfir-timeline-causality.md)。主索引の関連章: 20。
- Template（空欄）: [元Template](../templates/root-cause-analysis.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch20-dfir-timeline-causality-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch20-dfir-timeline-causality.json)。
- [必須ID・最初の記入先](../templates/root-cause-analysis.md#record-and-decision-requirement): RCA ID・Version・Incident / Case・Evidence Questionから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/root-cause-analysis.md#causal-analysis): 原因の主張と確信度は文書全体の承認Statusではない。未確定を保持する。
- [Owner](../templates/root-cause-analysis.md#record-and-decision-requirement): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/root-cause-analysis.md#review-checklist): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/root-cause-analysis.md#control-and-reassessment): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-27 Control Validation Plan

- 目的: ControlのExpectedと層別Actualを比較する。
- 入力: Control objective、同一対象版、合成Scenario。
- 出力: 層別結果、Failure、Gap、改善・Retest条件。
- 主担当章: [第21章](../manuscript/21-purple-team-validation.md)。主索引の関連章: 21。
- Template（空欄）: [元Template](../templates/control-validation-plan.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch21-control-validation-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch21-control-validation.json)。
- [必須ID・最初の記入先](../templates/control-validation-plan.md#plan-and-decision-requirement): Plan ID・Version・Case・Decision参照から記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/control-validation-plan.md#evidence-and-actual-by-layer): 層別Result、適用・未選択、Handoff状態を区別する。
- [Owner](../templates/control-validation-plan.md#plan-and-decision-requirement): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/control-validation-plan.md#review-checklist): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/control-validation-plan.md#improvement-retest-and-handoff): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-28 Security Improvement Backlog

- 目的: Metricから改善の判断を追跡する。
- 入力: 母集団、品質、判断目的、受入条件。
- 出力: 改善Backlog、検証・受容・廃止の区別。
- 主担当章: [第22章](../manuscript/22-measurement-improvement.md)。主索引の関連章: 22。
- Template（空欄）: [元Template](../templates/security-improvement-backlog.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch22-improvement-backlog-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch22-measurement-improvement.json)。
- [必須ID・最初の記入先](../templates/security-improvement-backlog.md#record-and-decision-purpose): Backlog・Item ID・Revision・Caseから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/security-improvement-backlog.md#seven-statuses): 七Statusに独自の進捗名を足さない。受容・廃止を改修成功へ算入しない。
- [Owner](../templates/security-improvement-backlog.md#priority-and-action): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/security-improvement-backlog.md#verification-and-risk-decision): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/security-improvement-backlog.md#reassessment-and-metric-retirement): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-29 Intelligence Requirement and Collection Plan

- 目的: 判断に必要な問いと収集計画を分ける。
- 入力: Decision Requirement、期限、充足条件。
- 出力: Requirement、Collection案、Evidence・Gap対応。
- 主担当章: [第23章](../manuscript/23-intelligence-requirements.md)。主索引の関連章: 23。
- Template（空欄）: [元Template](../templates/intelligence-requirement-collection-plan.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch23-intelligence-requirements-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch23-intelligence-requirements.json)。
- [必須ID・最初の記入先](../templates/intelligence-requirement-collection-plan.md#記入順序): Plan ID・Case ID・Decision・Requirement IDから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/intelligence-requirement-collection-plan.md#有限statusとpriority): RequirementとCollectionの有限Statusを分け、Priorityで停止を解除しない。
- [Owner](../templates/intelligence-requirement-collection-plan.md#記入順序): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/intelligence-requirement-collection-plan.md#提出前確認): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/intelligence-requirement-collection-plan.md#記入順序): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-30 Evidence and Source Evaluation Table

- 目的: 原典と取得物・変換物・Claimを区別する。
- 入力: Source、Item、時点、Provenance、利用条件。
- 出力: 用途限定評価、独立性、制約と再評価。
- 主担当章: [第24章](../manuscript/24-osint-provenance-sources.md)。主索引の関連章: 24。
- Template（空欄）: [元Template](../templates/evidence-source-evaluation-table.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch24-source-evaluation-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch24-source-evaluation.json)。
- [必須ID・最初の記入先](../templates/evidence-source-evaluation-table.md#記入欄): Table ID・Case ID・Source・Item・Claim IDから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/evidence-source-evaluation-table.md#有限な評価区分): Source reliability、information credibility、independence、Evidence用途は別軸である。
- [Owner](../templates/evidence-source-evaluation-table.md#記入欄): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/evidence-source-evaluation-table.md#提出前確認): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/evidence-source-evaluation-table.md#記入欄): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-31 AI / Agent Threat Model

- 目的: AI・Agentの能力と境界を評価する。
- 入力: Component、Data Flow、Instruction、Toolの供給モデル。
- 出力: Threat、Control根拠、未確認点、停止・判断条件。
- 主担当章: [第27章](../manuscript/27-ai-agent-security.md)。主索引の関連章: 27。
- Template（空欄）: [元Template](../templates/ai-agent-threat-model.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch27-ai-agent-threat-model-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch27-ai-agent-threat-model.json)。
- [必須ID・最初の記入先](../templates/ai-agent-threat-model.md#document-controlと判断要求): Threat Model ID・Case ID・Decision Requirementから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/ai-agent-threat-model.md#componentとdata-flow): Component六状態とToolの承認・停止は別の確認である。
- [Owner](../templates/ai-agent-threat-model.md#document-controlと判断要求): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/ai-agent-threat-model.md#完成確認): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/ai-agent-threat-model.md#threatから判断まで): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-32 AI-Assisted Analysis Assurance Record

- 目的: AI補助の主張を原典と人間判断へ結ぶ。
- 入力: Approved Source Set、Model・Input・Outputの版。
- 出力: Claim Verification、Human採否、監査・再評価。
- 主担当章: [第28章](../manuscript/28-ai-assisted-analysis-assurance.md)。主索引の関連章: 28。
- Template（空欄）: [元Template](../templates/ai-assisted-analysis-assurance-record.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch28-ai-assisted-analysis-assurance-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch28-ai-assisted-analysis-assurance.json)。
- [必須ID・最初の記入先](../templates/ai-assisted-analysis-assurance-record.md#document-control): Record・Case・Task・Decision Requirementから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/ai-assisted-analysis-assurance-record.md#claimとverification): Claim StatusとHuman採否、記録の完成を区別する。
- [Owner](../templates/ai-assisted-analysis-assurance-record.md#human-decision監査再評価): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/ai-assisted-analysis-assurance-record.md#human-decision監査再評価): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/ai-assisted-analysis-assurance-record.md#human-decision監査再評価): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

### ART-33 Final Security Decision Portfolio Index

- 目的: 成果物の参照と最終判断をまとめる。
- 入力: 親32種の固定記録、今回の要求、文書Evidence。
- 出力: Portfolio、二つのBrief、Gap、Action・再評価。
- 主担当章: [第29章](../manuscript/29-capstone-case-study.md)。主索引の関連章: 29。
- Template（空欄）: [元Template](../templates/final-security-decision-portfolio-index.md)。
- Example（合成記入例）: [記入内容と境界](../cases/ch29-capstone-portfolio-example.md)。
- Fixture 1（供給合成入力）。[Download / 読み取り専用JSON](../cases/fixtures/ch29-capstone-portfolio.json)。
- [必須ID・最初の記入先](../templates/final-security-decision-portfolio-index.md#0-portfolio-identity): Portfolio ID・Version・Final Case ID・Decision Requirementから記入し、関連IDの必須欄は元Template全体で確認する。
- [Statusの対象と境界](../templates/final-security-decision-portfolio-index.md#0-portfolio-identity): Portfolio Statusは親Artifactの状態でも実行許可でもない。
- [Owner](../templates/final-security-decision-portfolio-index.md#0-portfolio-identity): 記録・判断・取扱いの担当を区別し、参照だけで親Ownerを変更しない。
- [Review](../templates/final-security-decision-portfolio-index.md#5-optionreviewdecision): 対象版と根拠・限界を確認する。記入例内のReviewは実承認ではない。
- [Reassessment](../templates/final-security-decision-portfolio-index.md#6-actionとreassessment): 期限、変更条件、次の問いを元欄へ記録し、過去の判断を上書きしない。

生成索引終了（BCI_GENERATED_END）

## 自己点検と戻り先

選んだカードから、①判断する問い、②最初に記入するIDと欄、③足りないEvidence、④停止条件、⑤次の確認先を一つずつ示す。例えばART-10なら、Caseと判断要求を結び、Evidence不足をGapへ、次確認をReassessmentへ戻す。すべての欄を肯定的な結論で埋めることは求めない。

[付録Cのチェックリスト](appendix-c-checklists.md)で抜けを確認し、[付録Iの評価対応](appendix-i-rubric.md)で根拠と限界を説明する。統合提出は[第29章](../manuscript/29-capstone-case-study.md)へ戻る。印刷時も各ART見出しと元資料名を残し、DownloadはWeb版の同じカードから辿る。
