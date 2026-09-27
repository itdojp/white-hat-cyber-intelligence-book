# Executive Decision Brief

## このTemplateの使い方

`ART-09`は、[ART-08](cti-report.md)と同じEvidence / Key Judgmentを意思決定に必要な順序へ整理します。[第26章](../manuscript/26-cti-distribution.md)と[完全記入例](../cases/ch26-cti-distribution-example.md)を参照してください。単なる要約や、根拠のない安心の表明にはしません。

## Decision required

| Field | 記入内容 |
|---|---|
| Artifact / Product / Version | ART-09、この版のProduct ID、版番号 |
| Case / Parent / Relation | 判断対象と、親Caseへのrefines等の関係 |
| Requirement / Decision ID | 答える問いと支援する選択 |
| Decision owner / Audience | 決定責任者と受け取る役割 |
| Deadline / Cutoff / As-of | 判断期限、根拠の締切、記録が示す時点 |
| Decision type | 合成提案、実承認などを区別。推奨を承認済みとしない |

## Key judgments

重要判断は本書の設計として最大五件とし、この教材では三件です。短縮しても確信度とGapを削りません。判断の重大度、発生確率、確信度を混同しないでください。

| KJ ID | 判断・確信度 | Evidence / Source | 代替説明・Gap | 何が変われば見直すか |
|---|---|---|---|---|
| 記入するID | 要記入（未確認なら理由・担当・期限） | 要記入（未確認なら理由・担当・期限） | 要記入（未確認なら理由・担当・期限） | 要記入（未確認なら理由・担当・期限） |

## Business exposure

| Field | 記入内容 |
|---|---|
| Service / Customer | どの業務・顧客への影響を懸念しているか |
| Data / Obligation | 許可された範囲のDataと義務。未確認の義務を断定しない |
| Maximum credible impact | 根拠と前提がある最大の懸念。実被害額と区別する |
| Unknowns / Gap | 判断に効く欠落、Owner、期限。成功可否の未確認を隠さない |

## Options

| Option ID | Benefit | Cost | Disruption | Residual risk | Reversibility |
|---|---|---|---|---|---|
| 記入するID | 要記入（未確認なら理由・担当・期限） | 要記入（未確認なら理由・担当・期限） | 要記入（未確認なら理由・担当・期限） | 要記入（未確認なら理由・担当・期限） | 要記入（未確認なら理由・担当・期限） |

現状維持や保留も、選べない理由を含めて比較します。効果未検証の案を「安全」「確実」と表現せず、誤りだった場合の影響と戻せない点を明記します。数値がない場合は推測の金額を埋めず、不明とその理由を書きます。

## Recommendation / Decision

- Recommendation ID / 根拠KJ / 推奨理由:
- Selected Option / 棄却した案と理由:
- Decision ID / Parent Decision / Owner / 期限:
- 実行承認の有無 / 承認範囲 / 実施状況:

Implicationは業務上の意味、Recommendationは選択案、Decisionは選択の記録です。読者へ共有する許可から実操作の権限を推定しません。親Caseを詳細化する場合、元のDecisionを別の選択へ無言で置き換えないでください。

## Conditions and triggers

| Field | 記入内容 |
|---|---|
| Trigger | Evidence追加、Source訂正、前提の崩れなど判断を変える条件 |
| Stop / Rollback | 許可・Scope・影響が不明な場合の停止と、戻せる範囲 |
| Reassessment ID / Date | Deadline / Expiry前の確認、Ownerと必要なGap解消 |
| Expiry / Correction / Supersedes | 旧版の扱い、訂正理由、差替え先。STIX版・revocationとは別 |

## Distribution / Feedback

| Field | 記入内容 |
|---|---|
| Recipient / Status | 読者とProduct状態、必要な受領条件 |
| Classification / Sharing | 分類とTLPを別にし、読者に共有境界を明示 |
| License / Encryption / Retention | 別々の条件として確認する |
| Action permission | 情報共有と実行の許可を分離する |
| Delivery / Receipt | 未配達はfalse / null。実配達の証跡と区別する |
| Feedback ID / Question / Answer | どの版を理解したか、判断に役立ったか。未受領なら回答null |

## 安全境界と有限Status

Product語彙は`draft` / `prepared-not-delivered` / `delivered` / `expired` / `superseded` / `withdrawn`です。配達・差替えの証拠がなければ状態を進めません。第26章の検査は供給されたprepared-not-deliveredの例だけを対象とし、一般的な配送や承認のシステムではありません。

完全記入例は公開合成教材で、実通信・実操作・実通知・実配達0、Action permission=falseです。IOCやATT&CKの一致、独立STIX構造例のActor / Campaignを、親Caseの帰属根拠へ昇格させません。実Data、実Credential、個人情報、許可外の対象が必要になれば停止してください。
