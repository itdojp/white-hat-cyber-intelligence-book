# 第4章 Source Review Note — 2026-08-08

- 対象: Issue #29「資産、信頼境界、攻撃面、脅威モデル」
- Parent Part: #19
- Roadmap: #17
- Draft Intake Contract: #63
- Review date: 2026-08-08
- Canonical implementation base: `main@684fa03640302f098e7ca8bcd037e0499f63284b`
- Content Safety Policy: `1.2.0`

本Noteは第4章の一次資料採否とEditorial Inputの来歴を記録する。本文、Artifact、Case、Source Registryへ採用した主張は、2026-08-08に公式一次資料で意味確認した。

## Editorial Input

- Package: `white-hat-book-parallel-drafts-2026-08-08.zip`
- Package SHA-256: `caf8c73aa4e84c99f4062ac7cf85ac56794ad2cbb5d8ec5d9403138753eb6388`
- Input: `chapter04-assets-boundaries-threat-model.predraft.md`
- Input SHA-256: `c49f0a11ef9e37f1952199d263125aae9df273032e0a996642cfe9899750c358`
- Resumed-run workspace search: 該当Package、Input、および`.work/editorial-input/`の展開済みCopyは未検出
- Direct textual adoption in this PR: なし
- Raw predraft tracked files: `0`

Raw predraftはCanonical sourceではない。再開時の認可済みWorkspace内を一度検索したが、Packageと展開済みInputは存在しなかった。したがってRaw predraftを再構成せず、Issue #29、Issue #63、本Note、現行Repository contract、公式一次資料からCanonical contentを作成する。Raw predraftを読んだ、または直接採用したとは主張しない。この欠落は非Canonicalかつ任意のEditorial Inputであるため実装Blockerではない。

## NIST Cybersecurity Framework 2.0

- Official publication: https://csrc.nist.gov/pubs/cswp/29/the-nist-cybersecurity-framework-csf-20/final
- Official resource center: https://www.nist.gov/cyberframework
- Status: Final
- Version: 2.0
- Published: 2024-02-26
- Existing Source ID: `SRC-CSF-001`
- Checked: 2026-08-08
- Next review: 2026-11-08

公式CSWP 29 final publication pageと現行Resource Centerを再確認した。CSF 2.0は高位Outcome taxonomyであり、Outcomeの達成方法を規定しない。Chapter 4 mappingは実装、観測、Control validationまたは完全性の証明ではない。

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
- Published: 2012-09-17
- Source ID: `SRC-NIST-RISK-001`
- Registry decision: 採用
- Checked: 2026-08-08
- Next review: 2026-11-08

公式final publication pageと2026-07-24更新のNIST Risk Management publications indexを再確認した。確認した公式範囲ではSP 800-30 Rev.1はFinalとして掲載され、後継版または専用Errataは確認できなかった。「後継が存在しない」と一般化せず、確認範囲と日付をSource Registryに残す。

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

## OWASP Threat Modeling Project

- Official project: https://owasp.org/www-project-threat-modeling/
- Status: Maintained Project Guidance
- Version / published date: 継続更新Projectのため固定しない
- Source ID: `SRC-OWASP-TM-001`
- Checked: 2026-08-08
- Next review: 2026-11-08

公式Project pageを再確認し、単一の公式OWASP Threat Modeling methodologyを定義しない方法論中立のProjectであることを確認した。Chapter 4では、問い、System model、Threat identification、Mitigation、Reviewを接続する補助参照として採用する。Historical `Threat Modeling Process` pageは現行Normative guidanceとして採用しない。STRIDE、Diagram、Threat count、Toolまたは自動生成結果を完全性証明として扱わない。

OWASP Threat Dragonは本文の論証に不要なため、Source Registryへ追加しない。将来Tool例として採用する場合は、その時点のProject status、Version、Release dateを別途再確認する。

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

## Source Registry反映結果

Chapter PRでは次を反映した。

- `SRC-CSF-001`の`checkedAt`、`nextReviewAt`、Chapter 4 mapping、`reviewTriggers`、`notes`を意味確認後に更新
- `SRC-NIST-RISK-001`へversion、status、publishedAt、checkedAt、nextReviewAt、reviewTriggers、limitations、Chapter 4 mappingを記録
- `SRC-OWASP-TM-001`へMaintained Project Guidance、version/dateを固定しない理由、reviewTriggers、limitations、Chapter 4 mappingを記録
- 本文のSource ID、章末一覧、Registry mappingを一致させる
- `references/reference-baseline.md`を正本Rendererから再生成する
- Registry rootの`checkedAt`は、全Sourceを再監査したかのように変更しない

## 採否結論

- 採用: `SRC-CSF-001`、`SRC-NIST-RISK-001`、`SRC-OWASP-TM-001`
- 不採用: Historical OWASP `Threat Modeling Process` page、OWASP Threat Dragon
- 保留なし: 本章の論証に必要なSource statusは確認済み
- 既知限界: Threat ModelはDecision Requirementに対するReview可能なModelであり、Framework mapping、Threat count、Diagram complexity、Tool outputまたは数値Risk scoreで完全性を証明しない

## 停止条件

- 公式一次資料のCurrent statusを確認できない
- 発見したEditorial Inputのhashが登録値と一致しない
- Sourceの適用範囲と本章のOWN / BRIDGE / DELEGATEが競合する
- Threat Modelを実行可能な侵害手順へ変える必要が生じる
- 実Target、実Credential、PII、外部接続が必要になる
