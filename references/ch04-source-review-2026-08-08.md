# 第4章 Source Review Note — 2026-08-08

- 対象: Issue #29「資産、信頼境界、攻撃面、脅威モデル」
- Parent Part: #19
- Roadmap: #17
- Draft Intake Contract: #63
- Review date: 2026-08-08
- Canonical implementation base: `main@684fa03640302f098e7ca8bcd037e0499f63284b`
- Content Safety Policy: `1.2.0`

本Noteは第4章の一次資料採否とEditorial Inputの来歴を記録する。本文、Artifact、Case、Source Registryへ採用する主張は、Chapter PR内で再検証する。

## Editorial Input

- Package: `white-hat-book-parallel-drafts-2026-08-08.zip`
- Package SHA-256: `caf8c73aa4e84c99f4062ac7cf85ac56794ad2cbb5d8ec5d9403138753eb6388`
- Input: `chapter04-assets-boundaries-threat-model.predraft.md`
- Input SHA-256: `c49f0a11ef9e37f1952199d263125aae9df273032e0a996642cfe9899750c358`
- Integration guide: `parallel-draft-integration-guide.md`
- Source note input: `source-review-notes.md`

Raw predraftはCanonical sourceではない。`.work/editorial-input/`へ展開してHashを検証し、current Repository contractへ再構成する。Raw predraftをRepositoryへcommitしない。

## NIST Cybersecurity Framework 2.0

- Official resource: https://www.nist.gov/cyberframework
- Status: Final
- Version: 2.0
- Published: 2024-02-26
- Existing Source ID: `SRC-CSF-001`

### 採用範囲

- Business outcomeとCybersecurity riskの接続
- Governを含むRisk ownershipと意思決定Context
- Threat ModelからIdentify / Protect / Detect / Respond / RecoverへのHandoff

### 限界

- CSF mappingはThreat Modelの完全性を証明しない
- Category / Subcategoryへ対応しただけでControlの実装・観測・有効性を証明しない
- 本章のAsset、Boundary、Threat、Evidence、GapをCSFへ置き換えない

## NIST SP 800-30 Rev.1

- Official publication: https://csrc.nist.gov/pubs/sp/800/30/r1/final
- Status: Final
- Version: Rev.1
- Published: 2012-09
- Candidate Source ID: `SRC-NIST-RISK-001`

### 採用範囲

- Risk assessmentの準備、実施、維持
- Threat source / Threat event
- Vulnerability / Predisposing condition
- Likelihood、Impact、Uncertainty
- Assessment結果をRisk decisionへ渡す考え方

### 限界

- Federal向けProcessを普遍的な必須手順として転載しない
- 第4章では、Decision Requirement、Asset、Boundary、Threat Hypothesis、Evidence Requirement、Gap、Reassessmentへ必要な概念だけを適用する
- Risk scoreの算出をThreat Model完成の条件にしない

## 補助資料の採用条件

OWASP Threat Modeling関連資料またはToolを参照する場合は、実装時点のStatusと公式URLを再確認する。Diagramや自動生成結果を完全性証明として扱わず、説明補助またはTooling例に限定する。

## 本章で固定する区別

- Business Asset / Data Asset / Identity / Component / Control Plane / Evidence Asset
- Data Flow / Identity Flow / Control Flow
- Trust Boundary / Network Segment
- Attack Surface / Exposure / Entry Point
- Threat / Vulnerability / Finding
- Threat Hypothesis / Misuse Case
- Control Documented / Implemented / Observed / Validated
- Confirmed / Assumed / Unknown / Gap / Not applicable
- Evidence Requirement / Collected Evidence
- Attack Path / executable exploit procedure

## Source Registry更新条件

Chapter PRでは次を同時に行う。

- `SRC-CSF-001`のcheckedAt、chapter mapping、notesをsemantic review
- `SRC-NIST-RISK-001`を追加する場合、version / status / publishedAt / checkedAt / nextReviewAt / reviewTriggers / notesを記録
- 本文のSource ID、章末一覧、Registry mappingを一致させる
- `references/reference-baseline.md`を正本Rendererから再生成する
- checkedAtだけを意味確認なしに更新しない

## 停止条件

- 公式一次資料のCurrent statusを確認できない
- Editorial Input hashが一致しない
- Sourceの適用範囲と本章のOWN / BRIDGE / DELEGATEが競合する
- Threat Modelを実行可能な侵害手順へ変える必要が生じる
- 実Target、実Credential、PII、外部接続が必要になる
