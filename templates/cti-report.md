# Cyber Threat Intelligence Report

## このTemplateの使い方

`ART-08`は判断要求へ答える技術・運用向けProductです。[第26章](../manuscript/26-cti-distribution.md)と[完全記入例](../cases/ch26-cti-distribution-example.md)を参照してください。空欄を都合のよい推測で埋めず、未確認ならGap、Owner、期限、判断への影響を記録します。

Key Judgmentを先にまとめても、Evidence・Source・代替説明への参照を失わないことが重要です。Recommendationは案であり、実行承認ではありません。親Caseを詳細化する場合は関係を`refines`とし、元の判断やDecisionを無断で変更しません。

## Document Control / Scope

| Field | 記入内容 |
|---|---|
| Artifact / Product ID | ART-08と、この版を一意に示すProduct ID |
| Case / Parent / Relation | Case ID、親Record、refines / supersedes / independentのどれかと理由 |
| Version / Status | Productの版と有限状態。STIX Objectのmodifiedとは別 |
| Owner / Reviewer | 判断内容と配布の責任者、独立Reviewer |
| Authority / Scope | 読み取る資料、許可の根拠、対象外と停止条件。許可がなければ操作しない |
| Synthetic / Data boundary | 合成か、利用を許可されたDataか。出自・機密・個人情報の有無 |

## Intelligence requirement

| Field | 記入内容 |
|---|---|
| Requirement / Decision Requirement ID | 支援する問いと判断への直接参照 |
| Customer / Audience | 具体的な役割、必要な粒度、受領条件 |
| Decision deadline | 時差を含む期限。Product作成日とは別 |
| Cutoff / Prepared / As-of | 根拠の締切、作成時点、記録が示す状態の時点 |
| Success / Out-of-scope | 回答の合格条件と、答えない問い |

## Key judgments

| Judgment ID | 判断 | 確信度 | Evidence / Source | Gap / Alternative | 無効化条件 |
|---|---|---|---|---|---|
| 記入するID | 要記入（未確認なら理由・担当・期限） | 要記入（未確認なら理由・担当・期限） | 要記入（未確認なら理由・担当・期限） | 要記入（未確認なら理由・担当・期限） | 要記入（未確認なら理由・担当・期限） |

## Confidence and uncertainty

- 各確信度は`高・中・低`の根拠条件を説明する。重大度や事象の確率と同一視しない。
- 同じ原典の再掲、共有Tooling、取得期間外、翻訳の不確実性を隠さない。
- STIX Confidenceの数値へ暗黙変換しない。未指定なら未指定とする。
- Negative Findingは観測範囲、Coverage、欠落と許容結論を一緒に記録する。

## Evidence and source evaluation

| Evidence ID | Source ID / 原典群 | 観測・取得の範囲 | 支持する主張 | 限界 / Gap | 採否 |
|---|---|---|---|---|---|
| 記入するID | 要記入（未確認なら理由・担当・期限） | 要記入（未確認なら理由・担当・期限） | 要記入（未確認なら理由・担当・期限） | 要記入（未確認なら理由・担当・期限） | 要記入（未確認なら理由・担当・期限） |

第24章の表を使う場合も、同じ資料を受領したこと、対応するClaim、利用条件を確認してから結びます。方法参照を受領証跡にしません。Hashや変換形式は真正性や独立性の証明ではありません。

## Analysis / Alternatives

| 仮説・代替説明ID | 支持するEvidence | 反するEvidence | 残るGap | KJへの影響 |
|---|---|---|---|---|
| 記入するID | 要記入（未確認なら理由・担当・期限） | 要記入（未確認なら理由・担当・期限） | 要記入（未確認なら理由・担当・期限） | 要記入（未確認なら理由・担当・期限） |

確認事実・仮定・分析判断・予測を別に記入します。IOC一致やATT&CK対応付けだけでActor / Campaign / 国家へ帰属させません。Entity / Relationshipの表現に採用できない主張は、型が存在していても保留します。

## Technical recommendations / Implications

| Recommendation ID | KJ ID | 検知・Hunt・IRへの案 | Owner / 期限 | 必要Evidence・Gap | 停止条件 |
|---|---|---|---|---|---|
| 記入するID | 要記入（未確認なら理由・担当・期限） | 要記入（未確認なら理由・担当・期限） | 要記入（未確認なら理由・担当・期限） | 要記入（未確認なら理由・担当・期限） | 要記入（未確認なら理由・担当・期限） |

Technical implicationは「何を意味するか」、Recommendationは「何を検討するか」です。実行・通知・変更は別のAuthority / Scope審査へ戻します。実施状況と承認の証跡を、推奨の文章から推定しません。

## Business / strategic implications

Decisionへつながる業務上の露出、最大の懸念、その前提を記録します。未測定の影響を実被害額に変えません。経営向けの選択肢比較は[ART-09](executive-brief.md)へ接続し、同じKJ / Confidence / Gapを保持します。

## Distribution boundaries

| Field | 記入内容 |
|---|---|
| Recipient / Channel | 承認された読者と経路。教材では紙上記録のみ |
| Classification / TLP | 組織の分類と共有ラベルを別欄にする |
| License / Encryption / Retention | ライセンス条件、保護要件、保持期間を別々に確認 |
| Action permission | 情報共有の許可と技術的実行の許可を分ける |
| Delivered / Receipt | 未配達ならfalse / null。作成や送信案を受領証跡にしない |
| Expiry / Reassessment | 期限と再評価日、早期見直しの条件 |

## Feedback / Correction / Supersede

| Field | 記入内容 |
|---|---|
| Feedback ID / Product / Audience | 誰にどの版の理解や有用性を確認するか |
| Status / Answer / Receipt | 計画中・未受領・受領済みを区別。未受領の回答を作らない |
| Correction | 訂正理由、影響KJ、対象読者、旧版の扱い、再配布状況 |
| Supersedes | 差替え先が存在し審査された場合だけ参照する |
| Reassessment ID | Trigger、Gap、Owner、期日と判断を変える条件 |

## 有限Statusと教材の範囲

Productの記録語彙は`draft` / `prepared-not-delivered` / `delivered` / `expired` / `superseded` / `withdrawn`です。配達にはReceipt、差替えには相手のProduct IDと理由が必要です。期限切れは新しい分析判断やSTIX Objectのrevocationを意味しません。

第26章の機械検査は**供給されたprepared-not-deliveredの有限例だけ**を受理します。上記全状態の運用エンジンではありません。実資料や任意のSTIXを投入して権限・適法性・真正性を認定することはできません。完全記入例では実通信・実操作・実通知・配達はすべて0です。
