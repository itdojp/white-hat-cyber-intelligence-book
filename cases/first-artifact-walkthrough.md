# 最初の成果物：判断と証拠不足の読解

## この読解の範囲

これは[第1章の完全な合成記入例](ch01-integrated-security-case-example.md)を読むための学習用の抜粋であり、別のCaseや短縮版Templateの正本ではない。CaseのID・Status・日時・Evidence・判断は原記録を参照する。このページで実行・収集・承認を行わない。

実データ、Credential、Token、Cookie、個人情報を投入しない。予約済みの識別子（`billing-bridge.example`）は合成記録の参照だけに使い、接続先として使用しない。第1章Caseの過去のRoEと記入例を、現在の操作許可に転用しない。

目標は「何を判断するか」「何が未確認か」「どこで止まるか」を説明することである。実務版では[ART-10の空Template](../templates/integrated-security-case-map.md)と各章契約へ戻る。

## 1. 五つの要素を読む

### 判断要求

原記録の`DR-2026-001`は、CTOが請求書連携OAuthアプリを即時停止するか、権限縮小と監視強化で継続するかを判断する問いである。選択肢、判断期限、必要な承認者は原記録の「1. Decision Requirement」にある。ここで新しい判断や期限を作らない。

### 一つの脅威仮説

原記録の`TH-2026-003`は「既に同型の不正利用が発生した」という問いで、Statusは`Inconclusive`である。これは侵害を確認したという意味でも、侵害がなかったという意味でもない。他の仮説の`Supported`をこの仮説の証拠に置き換えない。

### 一つの観測計画

`OBS-2026-003`は過去90日のSign-in / API auditを問いに対応させる。`VAL-2026-003`は保持済みLogの検索計画である。今回はQueryやToolを実行せず、原記録の「4. Hypotheses」「5. Authorized Validation Plan」を読み、どのDataがあれば問いを評価できるかを書く。

### 一つの証拠不足

`NEG-2026-001`は`EVD-2026-004`に基づく合成のNegative Findingである。同意変更とsign-inは検索対象90日のうち72日分、API利用は一部だけで、18日分の保持不足とAPI利用Field不足が残る。許される結論は、取得できた範囲で対象Behaviorに該当するEventを確認していない、という限定結論である。

原記録にある合成Evidenceと、自分が収集したEvidenceを区別する。自分の演習では実収集なし（Not collected）と記録する。Not collectedは収集状況の説明であり、TemplateのDocument Statusや仮説Statusに追加する新しい状態ではない。

### 次の判断

`HUNT-2026-001`はTelemetry Gap解消後の再実施へつながる。原記録の「9. Analytic Judgment」「10. Decision Record」「12. Reassessment」へ戻り、現在の設定に関する判断と、過去侵害の不確実性を分けて読む。自分の演習では、追加確認の必要性を提案するところまでで止め、実際の停止・設定変更・再検証・承認を実施したと書かない。

## 2. 空Templateへ必要な欄から戻る

[ART-10の空Template](../templates/integrated-security-case-map.md)を学習用に利用し、次の順で記入を始める。ここには新しい記入フォームを作らない。

1. 「0. Document Control」: 自分の学習メモであること、Owner、作成時点、`Draft`を記録する。原CaseのID・Review・収集日時を自分の成果物の実績としてコピーしない。
2. 「1. Decision Requirement」: 判断者、問い、選択肢、未確定の期限や承認を区別する。
3. 「2. Scope, Authority, and Safety」: 今回は供給された合成記録の読解だけであること、実操作なし、停止条件を記録する。必要なAuthorityが未確認なら、実務検証へ進まない。
4. 「4. Hypotheses」「5. Authorized Validation Plan」: 仮説、必要Data、反証になり得る観測を対応させる。計画を実施結果へ書き換えない。
5. 「6. Evidence Register」「9. Analytic Judgment」: 原Case参照と自分の未収集を分け、証拠不足、代替説明、結論の限界を残す。
6. 「10. Decision Record」「12. Reassessment」: 推奨と実際の承認を分け、次の確認を担うOwner、確認期限、判断を変える条件を書く。未確定は未確定とし、承認時刻を捏造しない。

最初の提出は、この六つの対応を説明した学習メモでよい。全台帳の完成を初学習の必須条件にしない。ただし、実務成果物として使う前には、Template全体、章契約、必要なEvidenceとReviewを確認する。空欄に理由があっても、実務上の必須欄を免除したことにはならない。

## 3. 誤った結論を直す

**誤った例:** 「該当Eventがないので侵害なし。記入欄が埋まったのでControlは検証済みであり、CaseをClosedにする。」

修正は結論の語尾だけではない。

- 根拠: `NEG-2026-001`のCoverageとGapへ戻る。90日全体を十分に検索できたと書かない。
- 判断: `TH-2026-003`の`Inconclusive`を保持し、取得できた範囲の限定結論へ戻す。取得していないDataで不在を断定しない。
- 記録: 自分の実収集なし・実検証なしを明示する。Controlの`Passed`、Documentの`Closed`、承認を、記入完了から推測しない。
- 次の確認: Gap、Owner、確認期限、再評価条件を残す。必要な許可や証拠が欠けているなら、追加操作せず確認を求める。

誤例は原Caseの状態を訂正する指示ではない。第1章の原CaseのStatusは`Reassessment Due`のままであり、この学習メモで更新しない。

## 4. 提出と自己点検

提出物は、自分の言葉による学習メモと、対応する原記録・Templateの節参照である。自己点検は次の問いを一つずつ説明して行う。

| 評価観点 | メモで示すもの | 不足したときの戻り先 |
|---|---|---|
| 判断要求 | 誰が何を選ぶか | 判断要求とTemplateの1節 |
| 仮説と観測 | 問いと必要Dataの対応 | 五つの要素とTemplateの4・5節 |
| Evidenceの限界 | 72日、18日分の不足、一部API利用、実収集なしの区別 | 証拠不足と原記録の6節 |
| 停止条件 | Authority未確認や実Data出現時に進まない | 読解の範囲とTemplateの2節 |
| 次の判断 | Gap、Owner、確認期限、判断を変える条件 | Templateの9・10・12節 |

Gap、`Inconclusive`、`Partial`を正確に説明することも妥当な学習成果である。未確認を確認済みに見せることは成功条件にしない。自己点検や機械検査だけで合法性、安全性、Controlの有効性、実務成果物の完成、独立レビューの承認を保証しない。

## 5. 完全例と次の学習へ

- [第1章の完全な合成記入例](ch01-integrated-security-case-example.md): 最小の問いが全台帳のどこへつながるかを確認する。広い表は横スクロールで右端まで読む。
- [ART-10の空Template](../templates/integrated-security-case-map.md): 詳細な記録へ進むときの唯一の記入元である。
- [第0章](../manuscript/00-reading-guide.md)と[第1章](../manuscript/01-integrated-discipline.md): 役割別の読書順と統合業務へ戻る。
- [Quick Start](../quickstart.md): 自己点検で説明できなかった問いからやり直す。

想定読者による試行は未実施であり、完了時間や理解しやすさを実測した主張はしない。読者試行では、判断要求、Evidence不足、停止条件、次の確認先を説明できるかを観察する。AIのレビューやCI成功を読者試行として数えない。
