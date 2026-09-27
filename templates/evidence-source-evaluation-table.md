# Evidence and Source Evaluation Table

`ART-30`は原典、取得物、変換物、個別Claimの用途を分離する成果物です。[第24章](../manuscript/24-osint-provenance-sources.md)、[全欄Case](../cases/ch24-source-evaluation-example.md)、[供給JSON](../cases/fixtures/ch24-source-evaluation.json)、[閉Schema](../schemas/ch24-source-evaluation.schema.json)を照合します。

## 利用境界

Purposeは供給資料の限定評価、Prerequisiteは完全合成教材、Authority / Scopeはオフライン読解と記入だけです。Expected evidenceは来歴と用途・Gapの対応表、Impactは教材内だけです。Terms・原典・Hash不明、実Data・個人情報・外部通信の要求があればStopし、追加処理へ進みません。Cleanupは自分の作業Copyだけを確認して終了後24時間以内に除去することです。実行権限を発行せず、実収集・実操作・実通知を行いません。

## 記入欄

| 記録 | 必須内容 | 照合点 |
|---|---|---|
| Table / Case | ID、ART-30、Case関係、判断要求、Owner、Cutoff、期限 | 方法参照とEvidence継承を分ける |
| Collection | 問い、対象、現在版、期限、Authority、Terms、分類、停止 | 公開を許可とみなさない |
| Source | ID、発行主体、記述役割、Source class、reliabilityと理由 | 個別Claimの評価と別欄 |
| Item | ID、Source ID、Resource、版、公開/取得時刻、Timezone | 同じURLでも版を上書きしない |
| Acquisition | Canonical/Acquired URL、方法、保存参照、媒体型、言語 | 教材の保存IDを実Archiveと呼ばない |
| Integrity | Content、Hash対象とSHA-256、原物/派生、親Item | Hashは真正性や許可ではない |
| Transform | ID、方法、担当/Tool版、入力/出力IDとHash、時刻 | 原本ではなく作業Copyへ作用 |
| Translation | 原語/訳語、Reviewer、Review状態、曖昧な語、意味/限界 | 可能性を確定へ強めない |
| Claim | ID、対象・版・条件、命題、modality、仮説 | 記事全体の要約で置換しない |
| Evaluation | Evidence ID、Item/Claim、支持/矛盾、credibilityと理由 | 発行者の評判だけで昇格しない |
| Independence | 根底の観測group、派生元、引用関係、理由 | 相互引用と変換の親子を分ける |
| Use / Limit | 用途、制約、Gap、Owner、再評価ID/期限/条件 | 除外を記録の削除と混同しない |
| Handoff | 受け手、Evidence/Gap、制限、期限、Status、Receipt | planned-not-delivered/null/権限false |

## 有限な評価区分

Source reliabilityはbounded / limited / unknown、個別information credibilityはsupported / limited / unverifiedです。値が似ていても別の問いであり、平均や単一Scoreを作りません。Independenceのindependent-in-supplied-model / same-origin / unknownは著者が与えた観測関係に限り、実際の発行者の独立性を保証しません。

Evidence用途はDirect evidence / Context / Lead / Unverified / Excludedの五つです。これらは本書の教育用分類で、国際規範の正式Statusや法的証拠区分ではありません。用途を変えるときは対象・版、根拠、Review、Gapも点検します。

## 記入例と差戻し

ITEM-EV24-002とその作業訳ITEM-EV24-007は、CLM-EV24-002の同じ可能性を扱い、観測groupは一つです。二つのItemを二つの独立裏付けとして数える表は差し戻します。

誤ったAI要約ITEM-EV24-008は原典にない確定へ強まったためExcludedです。入力/出力Hashが正しくても用途は変わりません。作業抽出ITEM-EV24-009はReview未完でLeadとし、原典の合成観測自体と区別します。

## 提出前確認

原典と取得時点を辿れるか、旧新版を同じ根拠へ足していないか、訳語とmodalityを保持したか、三軸を分離したか、支持だけでなく矛盾とGapも残したかを確認します。実人物の特定・追加収集・実配布で欄を埋めません。第25/26章への予定は受領や実行許可ではありません。
