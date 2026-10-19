# 第29章着手前レビュー：入力記録と非継承境界

## 1. 対象と結論の範囲

- 所有Issue: [第29章 #51](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/51)。指定順は事前レビュー、第29章、付録の最終確定。
- 基準main: `ed7f449143ec9a2f3ffafbe2a9e18574690402aa`（PR #201の通常merge後）。確認日: 2026-10-19。
- 対象: 第0〜28章、ART-01〜32、既存Part横断対応表、付録の現状、Sourceと出版契約。
- 担当: 作者AI。独立レビューの指摘・対象SHA・処理結果は本記録のPRへ残す。本記録単体は独立承認、人間読者試行、法務確認、全書Releaseの証拠ではない。

**結論:** 既存教材は、一件の実施済み調査の連続履歴ではない。第29章では最終Case `CASE-2026-001`から、同じ記録の詳細化、別対象の方法参照、独立Case、未配達の予定を区別して辿る。全ArtifactをPortfolioへ収録することは、全Evidenceを同じCaseへ採用することではない。

既存の[第II部裁定](../PART_II_RECONCILIATION.md)、[第III部整理](../PART_III_RECONCILIATION.md)、[第IV部読解](../cases/part-iv-intelligence-decision-map.md)をそのまま使う。親記録を変更しなければ接続できない欠陥は、今回の入力境界レビューでは再現していない。ただし、まだ存在しない第29章の正しさや、全leafの独立再承認を主張しない。

本変更はレビュー記録と固定入力一覧のみである。第29章の本文・ART-33・Schema・Status・Intakeを先行実装しない。共有Publication Projection 1.1.0 / Content Safety Policy 1.2.0、formatter pin、Source確認日、既存Caseの時点や許可を変更しない。新たなparserや安全除外、付録最終化を着手前提へ戻す条件は追加しない。

## 2. 再現可能な入力一覧

[証拠JSON](2026-10-19-precapstone-evidence.json)に32件のArtifact対応、59件の登録Sourceの版・状態・変更trigger・章mapping、165ファイルのSHA-256を保存した。`chapterSourceIds`は**所有章で実際に使う一次資料のID**であり、各Artifactの全欄を直接証明する一覧ではない。合成CaseのSource ID、Evidence ID、AI出力とは別である。

`caseSections`は基準版の読解箇所を示す行番号で、単なる見出し存在を意味検証の代替にはしない。下の32項目は入力から判断・担当・再評価への接続と、禁止する取り違えを記録する。型の存在検査と各章内部の意味検査は既存checkerへ委譲する。

基準版の入力を照合する最小コマンド（Repository rootで実行）:

```bash
python3 -B - <<'PYCODE'
import hashlib
import json
import subprocess
from pathlib import Path

p = Path('reviews/2026-10-19-precapstone-evidence.json')
e = json.loads(p.read_text(encoding='utf-8'))
for path, expected in e['filesSHA256'].items():
    data = subprocess.check_output(['git', 'show', e['baseline'] + ':' + path])
    if hashlib.sha256(data).hexdigest() != expected:
        raise SystemExit('baseline mismatch: ' + path)
print('baseline inputs:', len(e['filesSHA256']))
PYCODE
```

これは過去の固定入力の照合である。将来のmainに変更があれば、その差分を別に監査する。基準commitがないshallow checkoutでは取得前に失敗する。現在の完成判定、原典の最新版、権限の真正性を判定するコマンドではない。

## 3. 32 Artifactの意味上の接続

以下のIDは既存記録の識別子であり、新しいPortfolio内のRecord IDではない。同じBundleに二Artifactが含まれる場合も、Artifact種別を消去せず別の役割として読む。Templateは空欄の仕様、Caseはその限定記入例である。

### ART-01 — LRP-2026-003

[空Template](../templates/learning-route-plan.md) / [記入例](../cases/ch03-capability-evidence-example.md) / [所有章](../manuscript/00-reading-guide.md)。関係: 独立学習Case。

親Plan→Task/学習Evidence→Review→月次再評価。ART-14の親Planであって業務Caseの侵害・能力認定の根拠ではない。

### ART-02 — ROE-2026-009

[空Template](../templates/rules-of-engagement.md) / [記入例](../cases/ch09-engagement-roe-example.md) / [所有章](../manuscript/09-engagement-roe.md)。関係: CASE-2026-001 / refines。

Draft / Do not proceed。decision・approval・evidence・changeを読む。失効AUTHと旧ROE-2026-001を置換せず、承認欄のnullを埋めない。

### ART-03 — TM-2026-001

[空Template](../templates/threat-model.md) / [記入例](../cases/ch04-threat-model-example.md) / [所有章](../manuscript/04-assets-boundaries-threat-model.md)。関係: CASE-2026-001 / refines。

Needs Evidence。Threat→Control→Gap→Evidence requirement→Action/Reassessment。必要EvidenceとCollected Evidence、Case関係とControlのsupportsを分離する。

### ART-04 — FRT-2026-015

[空Template](../templates/finding-report.md) / [記入例](../cases/ch15-findings-retest-risk-example.md) / [所有章](../manuscript/15-findings-retest-risk.md)。関係: CASE-2026-001 / refines。

findings→同対象/版のvalidation・evidenceIds→treatments/decision→reassessment。七Findingは独立対比。Closedを修正成功へ一括変換しない。

### ART-05 — DVR-2026-017-001

[空Template](../templates/detection-validation.md) / [記入例](../cases/ch17-detection-validation-example.md) / [所有章](../manuscript/17-detection-engineering.md)。関係: CASE-DET-2026-001 / refines。

Threat/Observation hypothesis→Telemetry contract→三fixture→DVR→triage/handoff/control/reassessment。Mappedやfixture検証を実配備/親Control全合格としない。

### ART-06 — HUNT-2026-018-001

[空Template](../templates/hunt-report.md) / [記入例](../cases/ch18-hunt-plan-example.md) / [所有章](../manuscript/18-threat-hunting.md)。関係: CASE-HUNT-2026-001 / refines。

計画と有限対比のEvidence・Coverage・Owner・次判断を読む。SupportedはIncident宣言ではない。負の結果は利用可能な観測範囲に限定する。

### ART-07 — DFIR-2026-020-001

[空Template](../templates/incident-timeline.md) / [記入例](../cases/ch20-dfir-timeline-causality-example.md) / [所有章](../manuscript/20-dfir-timeline-causality.md)。関係: CASE-DFIR-2026-001 / refines。

TL-DFIR20-A/Bのcutoff・availableAt・Receipt→Event→Claimを読む。親予定TL-IR19-004と別ID。遅着/再送/不確かさを隠さない。

### ART-08 — PRD-CTI26-TECH

[空Template](../templates/cti-report.md) / [記入例](../cases/ch26-cti-distribution-example.md) / [所有章](../manuscript/26-cti-distribution.md)。関係: CASE-2026-025 / refines。

products[0]→三KJ→親25のEvidence/原典群→recommendations/decision/reassessment。prepared-not-delivered、L2上限、成功未確認を保持する。

### ART-09 — PRD-CTI26-EXEC

[空Template](../templates/executive-brief.md) / [記入例](../cases/ch26-cti-distribution-example.md) / [所有章](../manuscript/26-cti-distribution.md)。関係: CASE-2026-025 / refines。

products[1]も同じKJを使う。Audience/選択肢/残余リスクの表現を変えてもEvidence・確信度・実権限を増やさない。未配達を保持する。

### ART-10 — CASE-2026-001

[空Template](../templates/integrated-security-case-map.md) / [記入例](../cases/ch01-integrated-security-case-example.md) / [所有章](../manuscript/01-integrated-discipline.md)。関係: 統合の親Case。

DR→ROE→Hypothesis→Evidence→Finding/Control→DEC-2026-001→REA-2026-001。Reassessment DueのDocument状態と個別Finding/Control結果を分離する。

### ART-11 — CASE-2026-011

[空Template](../templates/web-api-assessment-hypothesis-pack.md) / [記入例](../cases/ch11-web-api-assessment-example.md) / [所有章](../manuscript/11-web-api-hypothesis.md)。関係: independent。

Hypothesis Pack→VAL/OBS/EVD→Finding・Detection handoff→再評価。別対象のExport/Webhook教材であり、CASE-2026-001へEvidence/許可を借用しない。

### ART-12 — AJ-2026-025

[空Template](../templates/analytic-judgment-record.md) / [記入例](../cases/ch25-structured-analysis-attribution-example.md) / [所有章](../manuscript/25-structured-analysis-attribution.md)。関係: CASE-2026-025 / independent。

DR/IR→Source Note/lineage/Evidence→代替説明/判断→DEC/REA。同原典の再掲を独立観測に数えず、限定非観測を成功不存在にしない。

### ART-13 — AUTH-CASE-2026-001

[空Template](../templates/authorization-checklist.md) / [記入例](../cases/ch02-authorization-decision-example.md) / [所有章](../manuscript/02-law-ethics-authorization.md)。関係: CASE-2026-001 / refines。

Decision RecordedとGate Conditionalを分離。Authority/Scope/Safety/Disclosure→Decision→条件/担当/期限。後日のSource確認は過去権限を延長しない。

### ART-14 — CAP-MATRIX-2026-003

[空Template](../templates/capability-evidence-matrix.md) / [記入例](../cases/ch03-capability-evidence-example.md) / [所有章](../manuscript/03-capability-evidence.md)。関係: LEARN-CASE-2026-003 / 独立学習Case。

LRP-2026-003→Task/Practice→Artifact Evidence/Review→Capability Judgment→Gap/再評価。Gap identifiedとPartially supportedは別軸。人事評価へ転用しない。

### ART-15 — BMAP-2026-001

[空Template](../templates/attack-behavior-map.md) / [記入例](../cases/ch05-attack-behavior-example.md) / [所有章](../manuscript/05-attack-behavior.md)。関係: CASE-2026-001 / refines。

rowsのThreat/Asset/Boundary→ATT&CK版/関係→Evidence/test→Gap/Owner/reviewDate。Not collected、対応付けと検証、教育用製品モデルと親実態を分離する。

### ART-16 — SFM-2026-001

[空Template](../templates/signal-flow-diagram.md) / [記入例](../cases/ch06-signal-flow-example.md) / [所有章](../manuscript/06-observable-systems.md)。関係: CASE-2026-001 / refines。

flowsの親ID→receipt/test→coverage/gap→allowedConclusion/owner/reassessment。六Coverageを第16章のRequired込み七状態へ暗黙変換しない。

### ART-17 — VPR-2026-001

[空Template](../templates/vulnerability-prioritization-record.md) / [記入例](../cases/ch07-vulnerability-prioritization-example.md) / [所有章](../manuscript/07-vulnerability-prioritization.md)。関係: CASE-2026-001 / refines。

recordsの版・到達条件→固定Source snapshotと合成Evidence→priority/treatment→owner/期限/再評価。公開EPSS/KEV値と合成Deployment、Catalog期日と組織期限は別。

### ART-18 — LABPLAN-2026-001

[空Template](../templates/lab-safety-evidence-plan.md) / [記入例](../cases/ch08-lab-evidence-example.md) / [所有章](../manuscript/08-safe-lab-evidence.md)。関係: CASE-2026-001 / refines。

runs→receiptIds/signalIds→八状態/三結果→export/cleanup/再評価。Runningを含む状態、正常完了、実行許可は別。Cleanup成功で過去Failを消さない。

### ART-19 — ASR-2026-010

[空Template](../templates/attack-surface-register.md) / [記入例](../cases/ch10-attack-surface-example.md) / [所有章](../manuscript/10-recon-osint-boundary.md)。関係: CASE-2026-001 / refines。

candidate→source/provenance/origin→所有/検証状態→gapOwner/期限/再評価。候補発見はRoE Scope追加でなく、所有確信度は操作許可ではない。

### ART-20 — IAR-2026-012

[空Template](../templates/identity-attack-path-review.md) / [記入例](../cases/ch12-identity-path-review-example.md) / [所有章](../manuscript/12-enterprise-identity.md)。関係: CASE-2026-001 / refines。

pathのprincipal/resource/action/graph・policy版→config/event/evaluation→finding/owner/reassessment。静的経路はValidatedでなく、Brokenには反証が必要。

### ART-21 — PSA-2026-013

[空Template](../templates/platform-supply-chain-assessment.md) / [記入例](../cases/ch13-platform-supply-chain-example.md) / [所有章](../manuscript/13-platform-supply-chain.md)。関係: CASE-2026-001 / refines。

同recordRevisionのexpectations→chains/evidence→finding/decision。Verifiedは供給summary比較に限定。Signed/Trusted/準拠/Safe/Build許可へ昇格しない。

### ART-22 — MIV-2026-014

[空Template](../templates/minimal-impact-validation-record.md) / [記入例](../cases/ch14-minimal-impact-validation-example.md) / [所有章](../manuscript/14-minimal-impact-validation.md)。関係: CASE-2026-001 / refines。

同対象/版の二条件→observations/evidenceIds→stop/cleanup/residual→judgment/finding/decision。Not performedは別欄。Inconclusiveでも記録Completeはあり得る。

### ART-23 — FRT-2026-015

[空Template](../templates/retest-record.md) / [記入例](../cases/ch15-findings-retest-risk-example.md) / [所有章](../manuscript/15-findings-retest-risk.md)。関係: CASE-2026-001 / refines。

retestsをfindingId・対象・before/after版で結ぶ。Passed、受容経由Closed、期限付き受容、残余リスクを分離。親14のEvidenceを新Appへ移さない。

### ART-24 — TCM-2026-016

[空Template](../templates/telemetry-coverage-map.md) / [記入例](../cases/ch16-telemetry-coverage-example.md) / [所有章](../manuscript/16-telemetry-evidence-readiness.md)。関係: CASE-DET-2026-001 / refines。

requirements→fixtures/receipts→rows/七Coverage→Gap/Owner/期限→handoffs。Mapの存在だけで第17章入力契約を満たしたことにしない。

### ART-25 — IAP-2026-019-001

[空Template](../templates/incident-action-plan.md) / [記入例](../cases/ch19-incident-action-plan-example.md) / [所有章](../manuscript/19-incident-response.md)。関係: CASE-IR-2026-001 / refines。

十二対比の利用可能Evidence・Scope・判断権者→宣言/対応/復旧/再評価。Hunt SupportedからDeclaredへ自動昇格せず、Closedを全改善完了にしない。

### ART-26 — DFIR-2026-020-001

[空Template](../templates/root-cause-analysis.md) / [記入例](../cases/ch20-dfir-timeline-causality-example.md) / [所有章](../manuscript/20-dfir-timeline-causality.md)。関係: CASE-DFIR-2026-001 / refines。

Timelineと同じrecord内の六Claim・仮説・Gap→担当/再評価。相関・一つの保守説明への反証を原因確定にしない。両Snapshotの原因unresolvedを保持。

### ART-27 — CVP-2026-021-001

[空Template](../templates/control-validation-plan.md) / [記入例](../cases/ch21-control-validation-example.md) / [所有章](../manuscript/21-purple-team-validation.md)。関係: CASE-CV-2026-001 / refines。

新対象/版の五層・十Scenario→Evidence/判定→Retest/Action/未配達。IndeterminateをPartialやPassedへ丸めず、非選択層は未評価のまま。

### ART-28 — SIB-2026-022-001

[空Template](../templates/security-improvement-backlog.md) / [記入例](../cases/ch22-improvement-backlog-example.md) / [所有章](../manuscript/22-measurement-improvement.md)。関係: CASE-IMP-2026-001 / 方法参照。

metricsの母集団/版/品質→items/evidence/verification→decision/acceptance/reassessment。Accepted/Retiredは修正成功ではなく、二版・八項目は実時系列ではない。

### ART-29 — IRCP-2026-023-001

[空Template](../templates/intelligence-requirement-collection-plan.md) / [記入例](../cases/ch23-intelligence-requirements-example.md) / [所有章](../manuscript/23-intelligence-requirements.md)。関係: CASE-IRP-2026-001 / 方法上refines。

decision→requirementsとcollections多対多→Evidence/Gap→owner/deadline/feedback。両者の同名六Statusを転記しない。第25章IRとは別要求。

### ART-30 — EST-2026-024-001

[空Template](../templates/evidence-source-evaluation-table.md) / [記入例](../cases/ch24-source-evaluation-example.md) / [所有章](../manuscript/24-osint-provenance-sources.md)。関係: CASE-OS24-001 / independent。

Source→版付きItem/Transform→Claim別Evaluation→Gap/Handoff。用途の五分類は法的区分でなく、同Itemの別Claim評価を複写しない。

### ART-31 — AIM-2026-027

[空Template](../templates/ai-agent-threat-model.md) / [記入例](../cases/ch27-ai-agent-threat-model-example.md) / [所有章](../manuscript/27-ai-agent-security.md)。関係: CASE-AI-2026-027 / refines。

component/tool/version/approval/request→audit/evidence/finding→decision/reassessment。Allowed-in-modelでもexecuted=false、親Evidence/Authority非継承。

### ART-32 — AAR-2026-028-001

[空Template](../templates/ai-assisted-analysis-assurance-record.md) / [記入例](../cases/ch28-ai-assisted-analysis-assurance-example.md) / [所有章](../manuscript/28-ai-assisted-analysis-assurance.md)。関係: CASE-2026-025 / refines。

sourceSet/版→Claim/part/citation→verification→humanDecision/audit→reassessment/handoff。合成Acceptは実承認でなく、acceptedDecisionIdsは第29章の受領証拠ではない。

## 4. Part横断で追う六つの欄

1. **識別と版:** Artifact type、Record instance、Case、subject、revision、asOf/cutoffを分ける。ID文字列が解決しても、対象・版・目的が違えばEvidenceの転用を止める。
2. **Status:** Document、Evidence、Hypothesis、Control、受領、承認を別欄として読む。ART-01には独自の有限Statusを新設しない。Template全語彙と供給モデルで受理する有限状態も同一ではない。
3. **Evidence:** 要求された資料、受領した資料、Claimに適用できる資料、実際の独立観測を区別する。Not collectedをInconclusiveへ機械変換しない。後者には評価した問い・入力範囲が必要である。
4. **DecisionとOwner:** Decision owner、Evidence custodian、Gap owner、受容責任者、Reviewerは別Roleである。参照先にOwnerがいてもPortfolio全体の承認者へ自動昇格しない。
5. **期限と再評価:** 親Decision期限、資料の有効期限、Product期限、Metric再評価、受容期限は別欄に保持する。合成Caseの過去期限を現在の実タスク期限とみなさず、経過を隠す延長もしない。
6. **Handoff:** `planned-not-delivered`、`prepared-not-delivered`、receipt null、実行権限falseを保持する。Portfolioがリンクを持つことと受領・採用・操作の許可は別である。

### 接続単位での重点確認

- 序部・第I部: [第1章](../cases/ch01-integrated-security-case-example.md)のDR/DEC/REAと[第4章](../cases/ch04-threat-model-example.md)の追加Evidence要求を分ける。[学習Case](../cases/ch03-capability-evidence-example.md)の能力判断は独立。第5〜8章は親結果を更新しない教育用の追加記録である。
- 第II部: [横断表](../cases/part-ii-assessment-risk-map.md)の直接IDは参照を示すだけ。第9章のDraft/失効、第11章の独立性、第12章のcustomer-summary権限と第13章のBuild権限の非継承、第15章の七つの独立対比を保持する。
- 第III部: [横断表](../cases/part-iii-detection-improvement-map.md)でHunt支持、Incident宣言、Timeline、原因、Control評価、改善判断を順番に確定した一件へ変換しない。第21章の新対象と第22章の供給Metric比較は、親17の再配備や実リスク低下の証明ではない。
- 第IV部: 第23/24章の要求・評価は第25章の別Caseへ未配達。第25→26章だけは親Evidenceを明示参照して二Productへ変換する。独立STIX/TAXII例は構造教材であり、判断への採用Evidenceは空である。
- 第V部: 第27章のCASE-2026-001系列と第28章のCASE-2026-025系列を分ける。第28章の合成Human decisionを現実の承認や第29章の受領証跡にしない。

**第29章の設計上の提案:** ART-33で参照関係と採用用途を別欄に持つ。`refines`だけで根拠を採用せず、record/版/対象/許可/受領/用途を照合する。独立Caseを比較・方法参照として収録しても、最終Caseの実証Evidenceへ転換しない。既存記録にない新しい統合用判断を作る場合は、著者作成の合成設定と分かる別記録にし、親の時点・Status・Decisionを上書きしない。これはSchemaの凍結や第29章の受入済み実装ではない。

## 5. 着手前の十種の確認結果

| 確認 | 基準版の観測・判断 | 限界・引渡し |
|---|---|---|
| Artifact manifest | ART-01〜32に32 Templateと記入例の対応がある | ART-33は未作成。数だけでPortfolio完成としない |
| Artifact→Case | §3に32型の接続と非継承を記録 | 独立Caseや同Caseの別対象を強制joinしない |
| Artifact→Source | JSONに所有章の実使用Source mappingを記録 | 一次資料IDと合成Evidence/Sourceを混同しない |
| ID collision / orphan | 32型に重複・対応先欠落なし。ART-04/23、ART-07/26は同じBundle内の別役割 | 全語句の重複を誤りとする検査ではない。各章内の直接ID検査は既存contractが所有 |
| Status vocabulary | §3/§4に型・欄ごとの区別を記録 | 単一の共通Statusや合否へ変換しない |
| Gap / Inconclusive | 親のNeeds Evidence、Not collected、未実施、未配達、unresolvedを保持 | すべてを埋めることを第29章開始条件にしない |
| Reassessment due | 過去Case内の期限と現在の出版Source期限を分離 | 架空期限を延長したり実通知したりしない |
| Source freshness | 登録59件すべてに変更triggerと使用章がある。2026-10-19時点のnextReviewAt超過0 | 原典59件の最新版を今回一括再監査した意味ではない。新しい採用主張/範囲は第29章PR、全体鮮度は#25で再確認 |
| Published route | 既存29章・32 Template・記入例を公開登録へ追跡できる | 第29章route/新downloadは未作成。公開HTTPとartifactの比較はPR/Issueのexact-main証拠を参照 |
| License / Notice | 下記の再利用区分と既存Notice配置を確認 | 法的承認・全資料の転載許可を主張しない。新転載は個別確認前に採用しない |

### Sourceの扱いと変更trigger

[Registry](../references/sources.json)と[Source Policy](../SOURCE_POLICY.md)の契約を維持する。第0〜28章の登録IDの実使用集合と章mappingを照合し、現基準では不一致を検出していない。これは過去Issue #109全体の自動close理由にはしない。

- event型のATT&CK/OWASP/AI・法律資料は版や採用範囲の変更で再確認する。日付が将来でも変更triggerを無視しない。
- [第7章のSource snapshot](../cases/fixtures/ch07-source-snapshot.json)は固定した公開入力であり、合成の実測値ではない。第29章で新しいEPSS/KEV値を取得しない限り、古い値を現在の値へ読み替えず、Snapshot/取得日/Hashを保持する。
- Deprecated Data Sourcesと現行Detection Strategies、Log管理のFinalとInitial Public Draft、WSTGの固定Stableと開発版を区別する。実際の登録版・status・nextReviewAtは証拠JSONに残す。
- [付録A/D/Hの限定Note](../references/appendix-adh-source-review-2026-10-17.md)の5 Source確認は、既存章の全主張の一括再確認ではない。Registry-wide checkedAtも更新しない。
- 最も近い登録次回日付はIANA TLDの2026-11-03。未超過は原典変更がないことの証明ではない。原典不明、版不整合、利用条件不明を発見したら、その主張の採用を止め、Source Policyの更新手順へ戻る。

### 転載とNoticeの区別

[THIRD_PARTY_NOTICES](../THIRD_PARTY_NOTICES.md)は、固定formatter部品、MITRE metadata subset、Mermaid配布物を記録し、Sourceリンク一覧とは役割が異なる。`copy_public_notices.py`と既存QAで公開側の複製を照合する。今回これらの版・ライセンス・配布物は変更しない。

既存章の概念要約・出典リンクを第29章から参照することと、原典の図表・文章・Datasetを再配布することは分ける。登録59 Sourceに一括の転載許可があるとは扱わない。第29章で外部図表・長文引用・新Datasetの転載が必要になった場合は、文書ごとの条件、帰属、配布範囲を確認し、Noticeへの追加要否を記録してから採用する。新しい転載を行わず親教材を参照する設計なら、その未発生の転載を全章停止の新前提にはしない。

## 6. 付録と責任境界の残項目

| 範囲 | 確認した現在地 | 次の所有Issue |
|---|---|---|
| A/D/H | 正本3付録と限定Source Noteは公開済み。実許可・実Runtimeを付与せず、親章へ戻す導線がある | #52は完了。新章追加の影響は#24で最終照合 |
| B/C/I | 既存Template・Checklist・Rubricは利用できるが、ART-33を含む最終収録/相互照合は未完 | [#53](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/53)、第29章後 |
| E/F/G | 用語・図表・Source Baselineは既存読者module。第29章由来の項目は未登録 | [#54](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/54)、第29章後 |
| J | CROSS_BOOK_MAPの粗い「法・倫理・許可・RoE」「AI/LLM/Agent Security」行と、章固有ArtifactのOWNは粒度が異なる | [#55](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/55)の既知課題。第29章Handoff後に根拠付きで表を更新 |
| 読者・配布 | AIレビューやbrowser自動確認は実読者試行・全PDF/EPUB可読性の代替ではない | #110の履歴と[#25](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/25)のRelease gate |

本書の許可・停止・再承認・成果物接続を、外部専門書の製品操作・個別法的助言・業務governanceへ委譲したことにはしない。一方、このレビューで粗い責任表を無言で凍結更新しない。#55の最終化を第29章開始の前提に戻して循環させない。

## 7. 重大度順の引渡しと終了条件

- **既知P2・横断編集:** #55の責任表の粒度。親の契約を変更しない既存の扱いで事前レビューを進め、最終化時に根拠・影響章・移行をレビューする。
- **第29章で拒否すべき重大な誤り（まだ実装欠陥ではない）:** 独立Caseの強制統合、別対象/版へのEvidence転用、未配達の受領化、Portfolio承認から親Control/実許可への昇格。§3/§4から有限の負例を設計する。任意構文や一般的な安全判定は共有層へ委譲する。
- **Releaseの残作業:** 第29章、付録の最終照合、全体Source freshness、配布・読者確認。既存main CIの成功で完了扱いにしない。

独立レビューでは、技術/ID、許可・安全、出典・鮮度、分析・不確実性、教育設計、出版/再現性を分けて、下記を確認する。

- 32対応のうち親契約に反するjoin、借用されたStatus、未記録の受領がないか。
- sourceSnapshot、後日のSource確認、過去asOfとAuthorityを混同していないか。
- 既知#55とReleaseの未完事項を隠さず、別Issueの完了を新しい循環前提にしていないか。
- 第29章は新規の統合記録が必要な箇所と、既存例を比較・方法参照する箇所を区別できるか。

本レビューPRのmergeを既存#51にない追加の着手条件とするものではない。#51に既にある親章main安定、事前レビューの実結果、未解決blockerの処理、独立Part横断レビューという条件で判断する。レビュー未実施を文書の存在で代替しない。第29章の執筆PRと、その最終承認は別に行う。

## 8. 検証の読み方

このPRはレビュー文書と固定証拠だけを追加する。実行ロジックを変更していないため、新しい出版Gateや意味判定テストは追加しない。入力Hash、32対応/59 Source/章mapping、リンク・構造を検査する。既存全章・Part contract、全文Book QA、固定formatterでの生成・build・公開差分も確認し、**実行した対象SHAと結果はPR本文へ記録する**。基準mainのCI証拠を別headのCI成功へ読み替えない。

第29章の本文、独立した実読者試行、native browser zoom、全書PDF/EPUBの最終視覚検査、全59原典の今回一括再認証は、本レビューでは未実施である。作者AIの意味レビューと、PRでの独立AIレビュー、人間の採用判断を別の証拠として残す。
