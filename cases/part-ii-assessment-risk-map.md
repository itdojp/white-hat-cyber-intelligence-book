# 第II部 横断読解：AssessmentからRisk判断へ

## この対応表の使い方

第9〜15章の成果物を、参照IDと判断の境界から読み直す。第11章を含む七章の補助教材であり、新しいCase、実施記録、許可書ではない。登場する対象、担当、Evidence、判断は完全合成である。外部通信や実操作は行わず、リンク先の供給記録だけを読む。

**IDがつながることと、同じ対象の証拠がそろうことは異なる。** 同じCase IDでも、対象・版・Scopeが異なればEvidenceを付け替えない。参照IDだけでは、許可の有効性、観測の実施、Handoffの受領を証明できない。

この教材のOWNは、問い・根拠・不足条件・判断・再評価の追跡である。Web/API、Identity、Platformの概念は各章へBRIDGEし、製品操作や脆弱性別手順は各章のDELEGATE先へ委譲する。ここでは新しい操作手順を追加しない。

## 二つの接続を区別する

| 接続 | 読めること | 読めないこと |
|---|---|---|
| レコードの直接参照 | 参照元の欄が、参照先のどのIDを指すか。同一対象の根拠として使うには対象・版・Scopeも照合する | 同じCase IDや実在する参照IDだけを根拠にしたEvidenceの継承 |
| 比較・方法参照 | 別Caseや別対象で使われた問い、比較方法、記録の構造 | 元の許可、観測、成功、受容判断を新しい対象に移すこと |

`CASE-2026-001`は請求書連携の判断を束ねる。`CASE-2026-011`はExport APIとWebhookの段階公開を扱う独立Caseであり、前者の子Recordではない。第11章のAssessment結果を第15章へ移植せず、仮説と根拠を対応させる方法として比較する。

`refines`は親の判断を詳しく読む関係であり、対象が自動的に同一になるという意味ではない。第15章の`APP-FRT15-001`は新しい合成対象で、親の`APP-IAR12-001`の現在のbindingや実装を表さない。

## 章ごとの入口と境界

表の「版・範囲」は各記録の読解範囲であり、共通の実施Scopeを新設するものではない。合成記入例から元のJSONと空Templateへ進める。

| 章・合成記入例 | レコード | 版・範囲 | 保持する境界 |
|---|---|---|---|
| [第9章](ch09-engagement-roe-example.md) | ROE-2026-009 / ART-02 | v1 / 供給三Object | Draft、実行許可false |
| [第10章](ch10-attack-surface-example.md) | ASR-2026-010 / ART-19 | v1 / 九Source・六候補 | 所有確認と実行許可は別 |
| [第11章](ch11-web-api-assessment-example.md) | CASE-2026-011 / ART-11 | 読み取り専用Web/API Dataset | 独立ROE-2026-011、親への移植不可 |
| [第12章](ch12-identity-path-review-example.md) | IAR-2026-012 / ART-20 | GRAPH-IAR12-001 / POLICY-IAR12-001 | 現在のbindingはUnknown |
| [第13章](ch13-platform-supply-chain-example.md) | PSA-2026-013 / ART-21 | PSA13-REV-001 / 供給Chain | Verifiedは供給要約の比較 |
| [第14章](ch14-minimal-impact-validation-example.md) | MIV-2026-014 / ART-22 | MIV14-REV-001 / 供給二条件 | Supportedは限定した条件への支持 |
| [第15章](ch15-findings-retest-risk-example.md) | FRT-2026-015 / ART-04・ART-23 | FRT15-REV-001 / 七つの独立判断例 | 親Evidenceは方法参照だけ |

第9章の三Objectは`OBJ-ROE09-CONFIG`、`OBJ-ROE09-EVENT`、`OBJ-ROE09-POLICY`である。後続教材の対象をこのScopeへ自動追加しない。親Authorizationの期限`2026-08-19T09:00:00Z`と元Window`2026-08-06T00:00:00Z`〜`2026-08-06T08:00:00Z`は歴史的値のままである。後続記録の作成日へ読み替えず、現行の実行許可として再利用しない。

## 直接IDをたどり、推論を止める位置

次の対応は供給JSON内に存在する参照である。欄の位置はスラッシュで区切り、配列の0は先頭要素を指す。章番号の並びを一回の実施時系列に読み替えない。

| 参照元の欄 | 参照先 | ここで止める推論 |
|---|---|---|
| 第10章 `/parents/roeId` / `/parents/roeVersion` | 第9章 ROE-2026-009 / 1 | Draftを承認済みへ変えない |
| 第12章 `/context/reconRecordId` / `/context/reconCandidateId` | 第10章 ASR-2026-010 / CAND-ASR10-001 | Confirmed ownedは現在の実施許可ではない |
| 第13章 `/parentIdentity/reviewId` / `/parentIdentity/pathId` | 第12章 IAR-2026-012 / PTH-IAR12-004 | Validatedでも現在のbinding・coverageはUnknown |
| 第14章 `/context/assessmentId` / `/validations/0/parentFindingId` | 第13章 PSA-2026-013 / FND-PSA13-001 | 実Build・Deploy・署名検証は0 |
| 第15章 `/context/parentValidationRecord` / `/context/parentHandoffId` | 第14章 MIV-2026-014 / HOF-MIV14-15 | planned-not-deliveredのまま |
| 第15章 `/context/parentValidationId` / `/context/parentFindingId` | 第14章 VAL-MIV14-001 / FND-MIV14-001 | method-reference-not-evidence-for-new-subject |

第14章の`Complete`は供給記録の読解完了である。第15章での受領、実システムの安全性、別対象の脆弱性成立を意味しない。別対象へ応用する際は、新対象の根拠と不足条件を第15章の記録内で読まなければならない。

## 同一判断例のFindingから再評価へ

第15章の`SCN-FRT15-001`を一つ選ぶ。以下はこの判断例に限った追跡であり、他の六例を改善前後の時系列として連結しない。

| 段階 | 同じ判断例のID | 対象・根拠・判断 |
|---|---|---|
| 問いと確認 | VAL-FRT15-001 / EVD-FRT15-001 | APP-FRT15-001 / BEFORE-FRT15-001の権限宣言と業務要件の供給値を比較 |
| Finding | FND-FRT15-001 | Open。実装・実影響は未確認 |
| 対策案 | PERM-FRT15-001 | 推奨する改版案。実改修済みではない |
| 再評価用の比較 | RT-FRT15-001 / CHG-FRT15-001 | AFTER-FRT15-001は合成変更要約。元Findingの要件read-summaryを期待値にする |
| 結果 | RT-FRT15-001 | Failed。供給値read-all-summariesは要件と不一致 |
| 判断と残存Risk | DEC-FRT15-001 / RES-FRT15-001 | Remediate。実作業の指示・許可ではない |
| 次の再評価 | REA-FRT15-001 | SYNTH-CASE-OWNER / 2026-09-20T00:00:00Z |

Retestの`findingId`、`subjectId`、`beforeRevision`と、FindingのID・対象・版を照合する。Retestの`changedRevision`は改版後の比較対象であり、元の版と同じ文字列である必要はない。期待値を改版後の観測値に合わせて書き換えてはならない。

この例は受容済みでもClosedでもない。受容を使う別例は、同じ対象版・Scopeの委任根拠、権限保有者、期限、残存Risk、再評価条件を別途照合する。`Closed`にはRetestと受容の二経路があり、`Passed`と同義ではない。詳細な状態判定は[第15章](../manuscript/15-findings-retest-risk.md)とその供給記録を正とする。

## HandoffのGapと受領条件

既存のHandoffは`planned-not-delivered`である。次表の担当は、読者が不足条件を記録する際の**提案上の担当Role**であり、既存記録に新たな割当や受領を追記したものではない。受領条件も将来の確認項目であって、充足済みとは扱わない。

| 接続 | Gap | 提案上の担当Role | 将来の受領条件 |
|---|---|---|---|
| RoE → 評価設計 | 現在の許可、対象、操作、期間 | Engagement責任者・対象Owner | 新しい許可判断と版を明示。旧Draftを更新したふりをしない |
| Recon → Identity / Platform | 所有確認と操作Scopeの差、binding未確認 | Asset Owner・Identity担当 | 対象ID・版・関係の根拠と未確認欄を受け手が照合 |
| 独立Web/API Case → 方法比較 | 別の判断要求・対象・ROE | 評価設計担当 | 比較用途を宣言。元Evidence・許可を受領した扱いにしない |
| Platform → Minimal-impact Validation | 実測なし、条件ごとの証拠不足 | Platform担当・Validation担当 | 問い・対象版・期待条件・停止・残存Unknownを限定 |
| Validation → Finding / Risk | 親と新対象のEvidence不一致、未配達 | Finding Owner・判断Owner | 方法参照と新対象根拠を分離。受領者・受領記録がなければ未配達 |
| Finding → Telemetry / Detection | 未観測Gap、検知の有効性未測定 | Telemetry担当・Detection担当 | HOF-FRT15-16 / HOF-FRT15-17の目的と対象版を再確認。検知成功を先取りしない |

`Gap`を残したことは失敗の隠蔽ではない。観測済みの範囲と未確認の範囲を分け、次に誰が何を確認すべきかを示すことが成果物になる。教材の受領と、実環境での評価開始許可も別の判断である。

## オフライン読解課題と評価基準

前提は、このページと各章の読み取り専用教材である。新規収集、Request再送、認証、実改修は不要であり、実施しない。目的は参照の妥当性を説明することであり、新たなFindingを発見することではない。

1. 第12章から第10章への二つの参照IDを探し、所有確認だけでは開始できない理由を記す。
2. 第11章のCaseとRoEを記し、第15章へ移せる方法と、移せない根拠を区別する。
3. 第14章から第15章への参照を追い、対象が変わる位置と未配達の状態を記す。
4. 第15章の判断例001で、元要件、改版後の供給値、Retest結果、Decision、再評価Ownerを照合する。

期待する提出物は四行の読解メモである。各行へ参照元の欄、参照先ID、対象・版・Scope、利用できる結論、Gapを残す。供給欄にない値は推測せず「未確認」とする。

| 対比 | 不適切な説明 | 合格する説明 |
|---|---|---|
| 同じCase ID | 全章で同じEvidenceを使える | 対象・版・Scopeを別途照合する |
| 独立Case | 第11章のEvidenceが第15章のFindingを証明する | 比較・方法参照であり、対象の証拠は移さない |
| 親の完了 | CompleteなのでHandoffも受領済み | 読解完了とplanned-not-deliveredを分ける |
| 改版後の比較 | 観測値に合わせて期待値を変更する | 元Findingの要件に戻り、不一致ならFailedを保持する |
| 対策と判断 | RemediateやAcceptedなら実作業を開始できる | 記録上の判断と実行許可を分ける |

四課題すべてでIDの参照と非継承の理由を説明できれば、この読解課題を完了とする。外部接続、実Dataらしい内容、未知の入力、許可の不明点に気付いたら読解を止め、追加取得せず不足条件を記録する。作業後は自分の読解メモだけを整理し、正本や供給Evidenceを削除・変更しない。環境を起動しないため、Runtimeの停止・破棄は発生しない。

## 根拠と次の学習

この表の根拠は既存の[第9章](../manuscript/09-engagement-roe.md)、[第10章](../manuscript/10-recon-osint-boundary.md)、[第11章](../manuscript/11-web-api-hypothesis.md)、[第12章](../manuscript/12-enterprise-identity.md)、[第13章](../manuscript/13-platform-supply-chain.md)、[第14章](../manuscript/14-minimal-impact-validation.md)、[第15章](../manuscript/15-findings-retest-risk.md)と、各合成記入例の供給記録である。外部規範の新しい主張やSource版の更新は行わず、法・安全・標準の適用根拠は各章のSource Noteと確認範囲を参照する。

次は、記録した未観測Gapから必要なTelemetryと検知仮説を考える。[第17章 Detection Engineering](../manuscript/17-detection-engineering.md)も別の対象・fixture・判定条件を持つ。リンクをたどるだけでHandoffの受領や検知成功が成立するわけではない。
