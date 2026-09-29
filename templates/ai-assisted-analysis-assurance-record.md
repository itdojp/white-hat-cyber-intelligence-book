# ART-32 AI-Assisted Analysis Assurance Record

## このTemplateの扱い

完全合成の固定入力・出力を読むための保証記録です。実AI利用、原データの正しさ、標準準拠、実操作のAuthorityを認定しません。Model出力をSourceへ登録しない。

## Document control

| Field | 記入要件 |
|---|---|
| Record / Case / Artifact / relation | ART32と親Case25/26の教育上refinesを識別 |
| Task / Decision Requirement / owner | 判断主体、期限、成功条件、禁止する結論 |
| As-of / Source cutoff / Review window | 過去の判断と後日の再評価を分離 |
| Classification / safety | 合成/read-only/network=false/execution=false |

## Approved Source Set

| Field | 記入要件 |
|---|---|
| Set ID / version / descriptor hash | Source束の同定。実ログ計測と混同しない |
| Source ID / Evidence ID / Parent ID | 事案内SN/EVDと方法のSRCを分離 |
| Version / origin / independence group | 三再掲を独立三件に数えない |
| Collected-at / cutoff disposition | Cutoff後の情報を過去の判断へ混入しない |
| Passage / transformation / limitation | 原句から要約、翻訳、限界を追跡 |

## Model、Instruction、Input、Output

| Field | 記入要件 |
|---|---|
| Model / version / runtime | 著者作成の固定descriptor、実Endpointなし |
| Instruction ID / hash / trust boundary | Source/Tool/Memoryを承認や指示へ昇格しない |
| Tool capability / network | none / false |
| Input ID / hash / Source IDs | Redaction、分類、変換、汚染の固定試料 |
| Output ID / hash / authored offline | 実Model実行と主張しない |
| Reproduction ID / limits | 同じ版・対象・hashを比較、汎化を認定しない |

## ClaimとVerification

| Field | 記入要件 |
|---|---|
| Claim ID / raw text / type | Fact、Assumption、Judgment、Forecast、Recommendationを分離 |
| Grounding mode | Direct / Composite / Inference |
| Source IDs / passages | 各句に対応する箇所と時点・版 |
| Citation existence / support | 在庫にあることと主張を支持することを別確認 |
| Corroboration / origin groups | 独立原典と共通原典を区別 |
| Contradiction / alternatives / gaps | 反証・未確認・不受理理由を分離 |
| Model confidence / analytic confidence | 自動転記しない、根拠とHuman責任を記録 |
| Claim Status | Unverified / Supported / Partially supported / Contradicted / Rejected |
| Verification ID / target hashes | Claim、SourceSet、Input、Instruction、Model、Outputを結合 |

## Human Decision、監査、再評価

| Field | 記入要件 |
|---|---|
| Reviewer / reviewed-at / valid-until | 不明・失効を承認済みとしない |
| Decision ID / Claim ID / disposition | Accept / Revise / Reject / Escalate |
| Accepted wording / rationale | Partialの支持箇所だけを採用、帰属L2上限を保持 |
| Judgment / Decision / CTI references | 親結論の勝手な更新、未受領/独立Productの採用をしない |
| Audit event / target / owner | 対象・版・時点と採否を追跡 |
| Reassessment ID / trigger / owner / due | 原典訂正、撤回、版、期限、汚染、Coverage、独立性、帰属閾値変更 |
| Handoff / receipt / execution authority | 第29章の受領や実操作許可を発明しない |

## StopとCleanup

実PII/Secret/外部API/実操作は対象外。由来喪失、Cutoff不一致、入力汚染、失効、不明なHuman採否を見つけたら採用を止め、Gap/Owner/期限へ記録する。実Dataと実行能力を追加していないことを再確認する。
