# Fixture Catalog

このディレクトリは、章の合成Caseから参照する機械可読fixtureを公開する。

- すべてsynthetic dataである。
- 実在Target、実在Actor、実在個人、実Credentialは含まない。
- 各fixtureは対象章の契約に応じ、仮説、Evidence、Telemetry、Lineage、circular reporting、deception candidateなど必要な検証情報を保持する。

## 公開中のfixture

| File | Related chapter | Purpose |
|---|---|---|
| [ch05-attack-behavior.json](./ch05-attack-behavior.json) | 第5章 | 合成Behavior MapのStatus / Evidence / Testを有限に検証する |
| [ch11-web-api-assessment-dataset.json](./ch11-web-api-assessment-dataset.json) | 第11章 | Web/API評価の仮説、Evidence、Finding、Detection引き渡しを決定的に検証する |
| [ch17-detection-engineering-fixture.json](./ch17-detection-engineering-fixture.json) | 第17章 | Positive、Negative、Benign-near-miss、Telemetry gapのReplay契約を検証する |
| [ch25-structured-analysis-attribution-dataset.json](./ch25-structured-analysis-attribution-dataset.json) | 第25章 | Evidence、Source Note、lineage、circular reporting、deception candidate、judgment、decision、reassessmentを一括で検証する |

## 利用上の注意

- JSONは教材用の合成schemaであり、外部CTI標準そのものではない。
- fixtureの主張は、MarkdownのCaseと同じく判断構造の例示を目的とする。
- 各JSON fixtureを機械可読の正本とし、Markdown Caseは読者向けrenderingとして同じIDを表示する。`scripts/check_chapter11_contract.py`、`scripts/check_chapter17_contract.py`、`scripts/check_chapter25_contract.py`で、各章のID集合、主要参照関係、意味属性を検証する。
- 章別safety gateが機械保証する範囲は契約ごとに異なる。予約Domain、文書用IP、既知Secret / token形式、電話番号様文字列、構造化担当者の`SYNTH-`接頭辞などを検査するが、一般的な人名・住所PII検出器ではないため、自由記述は独立Reviewを併用する。

## 第6章 Signal Flow

[完全合成Dataset](ch06-signal-flow.json)はART-16の六Flow、Node / Edge、同一Flowの受領記録、保持期限・時刻誤差とGapを記録する非実行JSONである。`scripts/check_chapter06_contract.py`で閉じた構造、参照、表示、共有Policyを検査する。実Token値・実Log・外部接続は含めない。

## 第7章：優先順位の非実行分析

[六件の合成判断JSON](ch07-vulnerability-prioritization.json)と[固定公開Source snapshot](ch07-source-snapshot.json)は[記入例](../ch07-vulnerability-prioritization-example.md)に対応する。導入・到達・統制Evidence・判断は完全合成であり、EPSS / KEV値だけは固定一次資料からの抽出である。実対象への操作は行わない。

## 第8章：Lab Safetyのオフライン照合

[Plan](ch08-lab-plan.json)、[Control receipts](ch08-control-receipts.json)、[Evidence manifest](ch08-evidence-manifest.json)は[完全合成記入例](../ch08-lab-evidence-example.md)に対応する。三Run・72チェック・9合成Eventの固定レシピで、実Runtimeや通信・削除を実行しない。八状態とSafe / Unsafe / Inconclusive、実ByteのHash、停止・残存確認の区別を検査する。

## 第9章：RoEの非実行計画

[ART-02 JSON](ch09-engagement-roe.json)と[閉じたSchema](../../schemas/ch09-engagement-roe.schema.json)は[完全合成記入例](../ch09-engagement-roe-example.md)の全Fieldに対応する。供給三Object、有限八状態、Scope/Method/Data/Stop、期限と版、CompletionとReauthorizationを検査する。記録整合性の成功と実行許可は別で、executionAuthorizedは常にfalseである。

## 第10章 Attack Surface Register

- [Register](ch10-attack-surface.json): ART-19の要求、親ID、取得区分、Source、候補、Evidence/Gap/承認不足/Handoff。
- [Source bundle](ch10-source-bundle.json): 九つの作成者による合成要約。実収集・実観測はない。
- [Schema](../../schemas/ch10-attack-surface.schema.json): 二JSONをregister / bundleとして束ねた論理入力の閉じた構造。

[完全記入Case](../ch10-attack-surface-example.md)に全Fieldを掲載する。Hash対象は対応するcontent文字列のUTF-8 byteだけで、JSON全体やSourceの真正性・許可とは別。第10章公開前検査を通過しない入力はsite生成前に拒否する。
