# Attack Surface Register

`ART-19`は、Collection RequirementからSource、候補Asset、所有Confidence、Verification、次Actionの承認不足、Gap、再評価を結ぶ記録です。発見件数や公開情報の存在は、所有・稼働・実行許可の証明ではありません。

## 1. Document Controlと要求

| Field | 記入内容 |
|---|---|
| Register / Version / As of | ASR ID、審査対象の版、基準時点とTimezone |
| Case / Relation | Parent Case、refines / independent、置換なら根拠 |
| Decision / Collection Requirement | 親DRと今回のCRを分け、必要な問いとOwnerを記入 |
| Authority / RoE / Scope | 直接IDと版、現在の有効性、対象・対象外、停止理由 |
| Completion | 記入完了と実作業の許可を分離し、Gapを残す |

## 2. Collection planと実際の作用

Collection classはPassive / Active / Authenticatedの三つです。First-party inventory等のSource classとは別欄にします。元の取得Interactionと今回の学習操作も分離します。

| Field | 記入内容 |
|---|---|
| Purpose / Inputs | 最小の問い、必要なSource ID、対象範囲 |
| Original collection | 元の取得class・方法・仮定または実績の区別 |
| Current class / Actions | 現在行う操作と作用。本演習は提供資料のoffline読解だけ |
| Budgets / Stop | 外部通信・認証試行・Rate testは0、件数・量・時間、上限時の停止 |
| Data / Cleanup | 分類、Custodian、保持起点と期限、自分のコピーだけの後片付け |

Passiveという名前だけでNetwork requestを許可しません。実Target、実Credential、実在人物の情報集約を教材へ持ち込みません。DataやAuthorityが不明なら、追加取得・複製を止めてGapを記録します。

## 3. SourceとProvenance

| Field | 記入内容 |
|---|---|
| Source ID / Provenance ID | 一意の資料IDと来歴ID。参考仕様のSRC IDとは別 |
| Source class / Publisher | Inventory、DNS、CT、Code、Package、SaaS等と申告者 |
| Origin / Derived from | 原典ID、派生元Source ID、独立した原典数 |
| Acquisition / Timestamps | 方法、観測・取得・確認時点、時計の仮定と不確実性 |
| Hash / Hash scope | Algorithm、対象byteの定義、照合値。真正性や許可とは別 |
| Transformation / Terms | 変換、利用条件、第三者制約、未確認点 |
| Data / Custodian / Limitation | 最小Field、禁止Data、保管責任、証明できない範囲 |

本章の供給bundleでは、対応するcontent文字列のUTF-8 byteだけをHash対象とし、JSONファイル全体とは区別します。合成の時刻・取得・Owner statementを実観測や実署名へ読み替えません。

## 4. Asset candidateと所有

| Field | 記入内容 |
|---|---|
| Candidate ID / Type / Locator | 一意ID、種類、予約値の識別子。同名だけで結合しない |
| Source IDs / Evidence ID | 対応する資料と限定した比較結果 |
| Candidate owner / Confidence | 申告者、High / Medium / Lowの根拠、代替説明 |
| Ownership status | Confirmed owned / Unverified / Historical / Third party |
| Owner evidence / Parent Asset | 確認に使用した資料、親Assetへの限定した接続 |
| Exposure / Dependency / Third party | 実測か申告か、不明点、第三者条件を区別 |

所有者不明はUnverifiedにします。Confirmed ownedは所有者根拠と対象の対応が必要であり、RoE Scopeへの追加を意味しません。Confidenceは本章の有限な根拠評価であり、確率や真正性の認定ではありません。

## 5. Verificationと許容結論

Verification stateはCandidate / Corroborated / Owner confirmed / Rejected / Unknownの五つです。Unverifiedは所有属性であり、第六のStateではありません。

| State | 必要な根拠または制限 |
|---|---|
| Candidate | 要求との関係を記録。所有や現稼働は未確定 |
| Corroborated | 対象属性について独立原典が補強。同じ原典のコピーは加算しない |
| Owner confirmed | 対象IDと所有者の根拠を照合。次Actionの許可ではない |
| Rejected | このCaseへの接続を退ける理由を記録。Sourceは保持 |
| Unknown | 不足Evidenceと許容結論、Gapを明示 |

## 6. 次Action、Gap、再評価

各CandidateへAllowed next action、Next-action authorization、Required approval、Stop reason、Gap ID、Gap owner、Due date、Reassessment ID、無効化条件を付けます。本章Caseは全件record-only / nextActionAuthorization=falseです。

現在有効なAuthority、正確なAsset・Operation・時間のScope、System/Data owner、第三者利用条件を別々に確認します。所有確認、CT掲載、security.txt、公開URL、親の過去の許可は次Actionの承認を代替しません。

## 7. Handoffと受入

第12〜13章へ渡す確認済み候補と、第23〜24章へ渡すProvenance・不確実性を別のHandoff IDで記録します。Input ID、候補、Source/Provenance、制限、planned / deliveredの区別を保持します。合成計画を実際に送付した証跡として扱いません。

受入時は、全候補にSource、時点、Hash対象、所有Confidence、State、Evidence、Gap、Owner、期限、次Actionの不足条件があるかを確認します。記入が完成しても、未承認の実作業はDo not proceedです。

## 記入例と評価

[第10章完全合成Case](../cases/ch10-attack-surface-example.md)に全Fieldの記入例があります。[第10章](../manuscript/10-recon-osint-boundary.md)のRubricで、作用の分離、Provenance、所有判断、承認・Handoffを評価します。個別法的判断や詳細なOSINT操作手順は本Templateの責任範囲ではありません。
