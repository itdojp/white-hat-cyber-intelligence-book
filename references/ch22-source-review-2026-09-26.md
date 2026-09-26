# 第22章 Source Review — 2026-09-26

## 確認範囲と判定

[第22章](../manuscript/22-measurement-improvement.md)のMetric設計、品質、改善計画と再評価に必要な箇所だけを確認した。確認日はJST2026-09-26、取得記録のUTC時刻は2026-09-25T22:28〜22:30である。HTTP到達だけを意味確認とせず、以下の採用節を読解した。Registry全体や引用文献の全件再監査ではない。

本書の四つのMetric役割、七つのBacklog Status、合成ID、数値、閾値、有限比較算法は著者が設計した教材である。NISTの規範算法、認証、実有効性や法的適格性の認定として扱わない。生成モデルの出力をSourceには用いない。

## SRC-NIST-MEASURE-001 — 指標の定義と選択

- 発行主体: NIST。
- 文書: Measurement Guide for Information Security: Volume 1 — Identifying and Selecting Measures。
- 版・状態: SP 800-55v1、Final。公式Document HistoryのFinal日は2024-12-04。SP 800-55 Rev.1を置き換える。今回のFinal landingに後継版や廃止の告知は確認されなかった。
- [公式Final landing](https://csrc.nist.gov/pubs/sp/800/55/v1/final) / [公式PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-55v1.pdf)。
- PDF: 42ページ、1130125 bytes、SHA256 `29435d0db5af6dcb307e3de10e843c6eef474a0e7ae1e8993ab60af3cfc1bd04`。
- 採用: §1.4印刷p.2のMeasure / Metricの区別、§3.1.1〜3.1.5印刷pp.12〜16の記録・報告・Data管理・品質・不確実性、§3.3印刷pp.17〜18の測定の種類、§4印刷pp.19〜23の選択・優先・継続評価。
- 不採用: 普遍的な数値目標、実組織の効果推定、財務Riskモデル。NISTのImplementation / Effectiveness / Efficiency / Impactと本書のOutcome / Leading / Process / Qualityを同一分類としない。§4.4のFalse positive rateの表現を、既存章の混同行列や分母定義へ転用しない。
- 次回確認: 2027-09-26以前、または改訂・Errata・後継告知、採用する定義やData条件の変更時。

## SRC-NIST-MEASURE-002 — Measurement Programと改善

- 発行主体: NIST。
- 文書: Measurement Guide for Information Security: Volume 2 — Developing an Information Security Measurement Program。
- 版・状態: SP 800-55v2、Final。公式Document HistoryのFinal日は2024-12-04。SP 800-55 Rev.1を置き換える。今回のFinal landingに後継版や廃止の告知は確認されなかった。
- [公式Final landing](https://csrc.nist.gov/pubs/sp/800/55/v2/final) / [公式PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-55v2.pdf)。
- PDF: 33ページ、1321210 bytes、SHA256 `a5d935325735e158ff5878c633069568cc2b1f1b629aa75963cae3b300362bc7`。
- 採用: §3印刷pp.12〜22の目的・現状評価、指標の選択、Data分析、是正案、実施後の反復的な測定。§3.1.4印刷p.15の、活動や成果物の変化に応じた指標の見直し・廃止。
- 不採用: すべての組織へ同じ成熟度段階・固定手順を要求する解釈、人事評価、実施済み効果の認定。本章の供給計画を、組織のMeasurement Programが導入済みである証拠としない。
- 次回確認: 2027-09-26以前、または改訂・Errata・後継告知、改善Workflowや廃止基準の変更時。

## SRC-CSF-001 — 現在と目標のOutcome

- 発行主体・版: NIST CSWP 29 / CSF 2.0、Final2024-02-26。
- [公式Final landing](https://csrc.nist.gov/pubs/cswp/29/the-nist-cybersecurity-framework-csf-20/final) / [公式PDF](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf)。
- PDF: 32ページ、1518858 bytes、SHA256 `3c31f46fee98cac0c4323453e5109291a213b4de7fef8c058af9bf67f717433c`。
- 採用: §3.1印刷pp.6〜7のCurrent / Target Organizational Profile、Gap分析、優先的な行動計画。
- 限界: CSFはOutcomeの上位taxonomyであり、本章のMetric・七状態・有限計算を規定しない。mappingは実装、完全性、Control効果の証明でない。公式landingの2024-09-24 Planning NoteはCore移行用Spreadsheetの案内であり、CSF後継版として扱わない。
- 既存第1・4・19章のnotesとmappingを保持し、第22章用途だけを追記する。既存の次回確認2026-11-08は延長しない。

## SRC-IR-001 — 評価と運用からの改善

- 発行主体・版: NIST SP 800-61 Rev.3、Final2025-04-03。Rev.2を置き換える。
- [公式Final landing](https://csrc.nist.gov/pubs/sp/800/61/r3/final) / [公式PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf)。
- PDF: 48ページ、1040566 bytes、SHA256 `e5593d6bb85daecec7e8d9549400c7b3473bcc3f06e469c82218073afa7fba2d`。
- 採用: ID.IM-01〜03、印刷pp.19〜20。評価、演習、運用から改善を見つける文脈。
- 限界: 本章は供給記録比較であり、実Incidentの実施・教訓・効果を認定しない。親IRの未宣言、DFIRの原因未確定、Control検証の有限範囲を保持する。個別の法的通知判断は対象外。
- 既存全章のnotesとmappingを保持し、第22章用途だけを追記する。既存の次回確認2027-08-03は延長しない。

## SRC-KEV-001 — 継続更新Dataの限定例

- 発行主体: CISA。継続更新Dataのため、固定文書版とCatalog全体の単一公開日は今回も特定せず、version / publishedAtはnullを保持する。
- [canonical Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)は今回HTTP403で本文を取得できなかった。
- [公式cisagov mirror](https://github.com/cisagov/kev-data)のREADMEにあるUpdate schedule / Usage / Licenseを確認。取得READMEのSHA256は`7d18e1fc40185acc90128fcceb18f016e010c8d0cf4125c3311c9381cbafcfe2`。これは取得物の識別であり、Catalog版やGit commitの識別ではない。
- 採用: canonical側の更新後にmirrorが更新されるという説明と、変更履歴を追跡できるという用途。取得時点と適用母集団を固定する必要性を説明する例に限る。
- 未確認・不採用: 最新のCatalog値、個別CVE、実環境への適用、法的期限、BOD 26-04本文、今回の新しい固定Data Snapshot。第7章の過去Snapshotとその取得制約はそのまま保持する。非掲載を安全や未悪用の証明にしない。
- 次回確認: 利用時、Schema変更時、または既存期限2026-12-12以前。今回のREADME確認をCatalog全件確認としない。

## Reader-facing implications

全Sourceは本章の重要主張と章末一覧、Registryのchapter22 mappingへ対応させる。Registry直下のcheckedAtは全件監査の基準日を保持する。個別確認日の更新は本章用途の採用節監査だけを意味し、既存章のすべての主張を再監査したという意味ではない。

合成記録の数値は一次資料から抜き出した実統計ではない。Rule数、率、時間、Owner、承認・受容・検証はすべて教材の供給値である。TemplateとCaseにある完全性は記入欄と追跡性の完全性であり、実Riskの解消や法的許可の完全性ではない。
