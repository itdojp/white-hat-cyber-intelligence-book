# ART-31 AI / Agent Threat Model

## 目的と安全境界

Userの判断目的から、Instruction / Data / Model / Memory / Tool / Approval / Audit / Evidence / Finding / Reassessmentを結びます。[第27章](../manuscript/27-ai-agent-security.md)と[完全記入例](../cases/ch27-ai-agent-threat-model-example.md)を参照します。空Templateを埋めることは実行許可ではありません。

Purposeは境界と不足の記録、Prerequisiteは対象と版の定義、Authority / Scopeは所有・許可が明確な範囲だけです。本書の演習は完全合成・read-only・非実行に限定します。Expected evidenceは対象に結び付いた記録、Impactは教材読解だけです。外部接続を行わない。実Credentialを使用しない。実Dataの疑い、許可不明、演習範囲外の要求があればStopし、自分の演習コピーだけをCleanupします。

## Document Controlと判断要求

| Field | 記入する内容 |
|---|---|
| Artifact / Threat Model / Case ID | ART-31と固有ID、親Case、refines / independentの関係 |
| Decision Requirement / Owner / Deadline | 判断する問い、承認責任者、時刻とTimezone |
| Scope / Parent boundary | 対象外、親の未観測・停止・失効・非継承を明示 |
| Version / Updated / Review | 記録と評価対象の版、確認時点、再評価期限 |

## ComponentとData Flow

| Field | 記入する内容 |
|---|---|
| User / Agent / Model / Tool ID | 主体、役割、実効Capability、版 |
| Instruction layer / Trust / Override | 正規Instructionのorigin、untrusted Dataとの分離 |
| Input / Retrieval / Memory | Data分類、Source ID、Case、Audience、版、期限、隔離、由来 |
| Supply Chain | Model / Dataset / Tool / DependencyのVersion、Digest、Provenance。未確認理由も残す |
| Component status | Declared / Observed / Validated / Restricted / Disabled / Unknown |

Validatedには同じ対象・版の観測と検証が必要です。DeclaredをObservedと混ぜず、制限と無効化を過去のPassedで打ち消しません。六状態は本書の教材用で、外部規格の認証LevelでもLab八状態でもありません。

## Toolと承認・停止

| Field | 記入する内容 |
|---|---|
| Capability / Scope / Credential class | 必要最小機能、対象Data、利用者、Credentialを本文へ記載しない分類 |
| Side effect / Approval | 読取りと効果要求を分離、対象引数、Owner、要求ID、有効期間、再使用制約 |
| Timeout / Budget / Kill switch | 有限上限、停止優先、独立停止経路の根拠と未試験範囲 |
| Tool response / Model output | Schema、由来、仮説/Source/Fact/Commandの扱いと自動採用禁止 |

本教材で書込み等を要求する欄は拒否対象のメタデータだけです。このmockは無害な固定Responseの説明だけです。外部Network、Shell、実File mutationを実装しない。実Credentialを使用しない。実Model APIや実Dataを使用しない。

## Threatから判断まで

| Field | 記入する内容 |
|---|---|
| Threat / Misuse / Preconditions / Impact | どの主体がどの境界へ影響するか、成立条件と影響 |
| Control / Evidence / Validation / Finding | 同一対象・版・時刻の直接参照、期待と結果、差戻し理由 |
| Audit / Retention / Custodian | 要求、入力の由来、Owner、判定、Stop、保持期限、観測不足 |
| Gap / Alternative / Confidence | 未確認点、通常変更等の代替説明、根拠に基づく確信度 |
| Decision / Reassessment | 許容範囲、Owner、期限、無効化条件、再確認方法、受領未了 |

## 完成確認

全欄が揃い、Unknown・不足・停止を隠さず、何が判断できないかを書けた状態を完成とします。AIの要約を自動的にSourceやFactへ採用しません。実証のない署名、信頼、規格適合、実停止成功を主張しません。本文Rubricで境界・追跡・安全・分析・引渡しを確認します。
