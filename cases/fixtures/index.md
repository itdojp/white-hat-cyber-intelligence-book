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

## 第12章 Identity Attack Path Review

- [供給JSON](ch12-identity-paths.json): Principal、Role、Permission、Resource、必要Edge、Path、設定Evidence、合成Event、有限比較、FindingとHandoff。
- [閉じたSchema](../../schemas/ch12-identity-paths.schema.json): 供給教材の有限語彙と未知Field拒否。任意のSecretを認識するParserではない。

[全Fieldを掲載したCase](../ch12-identity-path-review-example.md)と一対一で照合する。外部通信・実認証・親の承認変更を行わず、公開前の第12章検査を通過してから生成する。

## 第13章 Platform and Supply Chain Assessment

- [供給JSON](ch13-supply-chain.json): 合成Source、Lock、Build、Artifact、Provenance、Registry、Promotion、Deployment、Runtimeと判断の記録。
- [閉じたSchema](../../schemas/ch13-supply-chain.schema.json): 供給語彙だけの未知Field拒否。SPDX/SLSAや一般Secret認識のSchemaではない。

[全FieldのCase表示](../ch13-platform-supply-chain-example.md)と一対一で照合する。実Build/Deploy/署名検証/許可発行をせず、第13章の公開前検査後にだけ生成する。

## 第14章 Minimal-Impact Validation Record

- [供給JSON](ch14-minimal-impact-validation.json): 二つの期待条件と合成観測、停止、整理、残存確認、判断を持つ八記録。
- [閉じたSchema](../../schemas/ch14-minimal-impact-validation.schema.json): 本教材の有限語彙と未知Field拒否。実行許可や標準適合のSchemaではない。

[全FieldのCase表示](../ch14-minimal-impact-validation-example.md)と一対一で照合する。合成IDの比較だけを行い、実サービスへの接続や合成Accountの作成は行わない。

## 第15章 FindingとRetest

- [供給JSON](ch15-findings-retest-risk.json): Finding、三種類のTreatment、Retest、Residual、Acceptance、Reassessment、Disclosureを持つ七つの独立した合成対比。
- [閉じたSchema](../../schemas/ch15-findings-retest-risk.schema.json): 有限語彙・非実行フラグ・未知Field拒否。実許可の証明や一般的なWorkflow engineではない。

[全FieldのCase表示](../ch15-findings-retest-risk-example.md)と一対一で照合する。固定asOfを使い、実Scanner・実変更・実Retest・実届出を行わない。

## 第16章の合成記録

[Telemetry Coverage JSON](ch16-telemetry-coverage.json)と[閉じたSchema](../../schemas/ch16-telemetry-coverage.schema.json)は十の独立した問い・二十四の供給段階receiptを比較する読解専用入力である。実製品の測定結果ではない。[全欄Case](../ch16-telemetry-coverage-example.md)へ戻る。

## 第18章の合成記録

[Hunt JSON](ch18-threat-hunting.json)と[閉じたSchema](../../schemas/ch18-threat-hunting.schema.json)は、固定合成入力に対する十二の独立対比を示す。Receiptは教育用仮定であり、実Collectorの証拠ではない。[Artifact全欄Case](../ch18-hunt-plan-example.md)へ戻る。

## 第19章 Incident Response

- [供給JSON](ch19-incident-response.json): 十二の独立した合成対象版、前状態、宣言基準、Evidence、選択肢、復旧検証、判断、未配達Handoff。
- [閉じたSchema](../../schemas/ch19-incident-response.schema.json): 有限語彙と未知Fieldの拒否。実IR自動化や真正性認証ではない。

[全Artifact欄のCase](../ch19-incident-action-plan-example.md)と照合し、詳細Evidence列はJSONを読む。第19章公開前検査を通過しない入力は生成前に拒否する。供給Receiptは教育上の仮定で、親Evidence・権限・未配達を変更しない。

## 第20章 DFIR

[供給JSON](ch20-dfir-timeline-causality.json)と[閉じたSchema](../../schemas/ch20-dfir-timeline-causality.schema.json)は完全合成の五Receipt、Clock条件、六Claim、二Cutoff、ART-07/26、三つの未配達Handoffを持つ。[全欄Case](../ch20-dfir-timeline-causality-example.md)へ対応し、実収集や原因の自動認定は行わない。原payloadのHashは表現比較だけである。

## 第21章 Control Validation

[供給JSON](ch21-control-validation.json)と[閉じたSchema](../../schemas/ch21-control-validation.schema.json)は十Scenario、五Control、層別期待値と供給Record、改善案、Retest、未配達Handoffを持つ。[全欄Case](../ch21-control-validation-example.md)へ対応し、実攻撃・実操作・実通知は0件である。部分充足とUnknownを分離し、Hashは供給表現の比較だけとする。

## 第22章 Measurement and Improvement

[供給JSON](ch22-measurement-improvement.json)と[閉じたSchema](../../schemas/ch22-measurement-improvement.schema.json)は、十Metricの二つの供給版と八Backlog項目を持つ。[全欄Case](../ch22-improvement-backlog-example.md)へ対応し、42の独立した算術期待値と章固有の意味負例で検証する。実Log、実Collector、個人Rankingは用いず、欠測を0へ置換しない。
