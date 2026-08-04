# Fixture Catalog

このディレクトリは、章の合成Caseから参照する機械可読fixtureを公開する。

- すべてsynthetic dataである。
- 実在Target、実在Actor、実在個人、実Credentialは含まない。
- Lineage、circular reporting、deception candidateを検査可能な形で保持する。

## 公開中のfixture

| File | Related chapter | Purpose |
|---|---|---|
| [ch11-web-api-assessment-dataset.json](./ch11-web-api-assessment-dataset.json) | 第11章 | Web/API評価の仮説、Evidence、Finding、Detection引き渡しを決定的に検証する |
| [ch17-detection-engineering-fixture.json](./ch17-detection-engineering-fixture.json) | 第17章 | Positive、Negative、Benign-near-miss、Telemetry gapのReplay契約を検証する |
| [ch25-structured-analysis-attribution-dataset.json](./ch25-structured-analysis-attribution-dataset.json) | 第25章 | Evidence、Source Note、lineage、circular reporting、deception candidate、judgment、decision、reassessmentを一括で検証する |

## 利用上の注意

- JSONは教材用の合成schemaであり、外部CTI標準そのものではない。
- fixtureの主張は、MarkdownのCaseと同じく判断構造の例示を目的とする。
- JSON fixtureを機械可読の正本とし、Markdown Caseは読者向けrenderingとして同じIDを表示する。`scripts/check_chapter25_contract.py`でID集合だけでなく主要参照関係と意味属性の一致を検証する。
- safety gateが機械保証する範囲は、予約Domain、文書用IP、既知Secret / token形式、電話番号様文字列、構造化担当者の`SYNTH-`接頭辞である。一般的な人名・住所PII検出器ではないため、自由記述は独立Reviewを併用する。
