# Writing Guide

**契約状態:** 代表章Gateで凍結（2026-08-04）。以後の変更は、根拠となるIssue、影響する章、移行方法、独立レビューを伴う。

## 1. 目的

本書の文章を、技術的に正確で、安全で、判断に使え、更新可能な形へ統一する。

## 2. 章の標準構造

各章は原則として次の順にする。

1. この章の位置付け
2. 学習目標
3. 前提知識
4. 導入ケースまたは判断要求
5. 全体像
6. 基本概念
7. 攻撃者・防御者・分析者・意思決定者の接続
8. 安全な演習または分析課題
9. 作成する成果物
10. 評価基準
11. よくある誤解
12. 章のまとめ
13. 次に学ぶこと
14. 参考文献・Source Note ID

全視点を毎章均等に扱う必要はない。ただし、どの成果物を次の業務へ渡すかを明示する。

## 3. 主張の分類

本文では、次を混同しない。

- **確認事実**: 一次資料、観測、再現結果で確認できる
- **分析判断**: 複数の事実・仮定から導く評価
- **仮定**: 分析のために置く未確認条件
- **予測**: 将来についての条件付き判断
- **推奨**: 特定の目的・制約に対する行動案

分析判断と予測には、根拠、代替説明、確信度、結論を変える条件を添える。

## 4. 確信度

`高・中・低`を、感覚ではなく証拠条件で使う。

- 高: 複数の独立した高品質情報源または直接観測が整合し、主要な代替仮説が弱い
- 中: 有力な証拠があるが、情報ギャップまたは妥当な代替仮説が残る
- 低: 限定的・間接的な証拠に依存し、複数の説明が同程度に成立する

確信度は事象の重大度を意味しない。

## 5. 安全な技術記述

攻撃技法を扱う場合、最低限次を対にする。

- 成立条件
- 許可・スコープ
- 業務上の影響
- 観測可能な痕跡
- 必要Telemetry
- 検知仮説
- 防止・緩和策
- 最小影響の確認方法
- 停止条件と復旧

公開本文では、第三者への侵害に直結する実運用可能な手順、実Credential、C2、永続化、回避、破壊を掲載しない。詳細は`SAFETY_SCOPE.md`に従う。

## 6. 用語・表記

- 初出では日本語と英語を併記し、その後の表記を統一する
- 製品名と標準名を区別する
- 「安全」「検知可能」「侵害なし」などの断定は、観測範囲と前提を明記する
- ATT&CK、OWASP、NIST等の名称・版はSource Note IDで追跡する
- 「ホワイトハッカー」は入口の呼称として使い、本文では具体的な業務名を優先する

## 7. 図と表

- 図には読み方、入力、出力、境界を添える
- Coverage図は「対応付け」と「有効性検証済み」を見分けられるようにする
- 色だけで意味を伝えない
- 画像内の重要情報には文章代替を置く
- 図表IDは安定させ、図表索引から参照できるようにする

## 8. コード・設定・コマンド

- 自己所有の隔離ラボだけで実行できること
- バージョン、前提、期待結果、失敗時の戻し方を記載すること
- 予約済みドメインと文書用IP範囲だけを例に使うこと
- 実行結果を捏造しないこと
- 未検証例は明確に`未検証`と表示すること

## 9. レビュー分離

執筆と最終承認を同一コンテキストだけで完結させない。最低限、次を分ける。

- 技術的正確性
- 安全・法・倫理
- 出典・鮮度
- CTI分析品質
- 教育設計・可読性
- コマンド・ラボ再現性

## 10. Case・成果物・識別子の契約

章の成果物は、単独の記入例ではなく、判断へ至る追跡可能な記録として設計する。該当する要素を次の順で接続し、使用しない要素は理由を明記する。

```text
Decision Requirement
→ Asset / Threat Hypothesis
→ Authority / RoE
→ Assessment Hypothesis / Finding
→ Telemetry / Detection
→ Evidence / Incident context
→ Analytic Judgment / CTI
→ Action / Reassessment
```

- `Case ID`は一つの判断対象を束ねる。別の章で同じCaseを扱う場合は同じ`Case ID`を継承する
- 詳細化用の子Recordへ別IDを付ける場合は、親Case IDと`refines` / `supersedes` / `independent`の関係を明示する
- 別の判断対象を、章間の見かけ上の連続性だけを理由に同じCaseへ統合しない。独立Caseは`independent`と明示する
- `Artifact ID`は`artifact-index.md`を正本とし、別の成果物へ再利用しない
- 合成Case、Template、fixture、本文で、ID、Status、Evidence reference、Owner、Review dateの意味を一致させる
- 確信度は`高・中・低`、仮説の状態は成果物で定義した有限集合を使用し、自由記述の同義語を増やさない

代表章での正本となる同一Case追跡例は、`CASE-2026-001`と、それを`refines`する第17章の`CASE-DET-2026-001`である。第11章と第25章の合成Caseは、異なる判断要求を扱う独立Caseである。

## 11. Source Noteと主張の契約

- 時点依存または外部規範に依存する重要主張には、本文の該当文または段落で`SRC-*`を付ける
- 章末の`参考文献・Source Note ID`には、その章で使用した全IDを過不足なく列挙する
- `references/sources.json`の`chapters` mappingは、実際にIDを使用する章と一致させる
- Versionが存在しない継続更新Pageや、公開日の日まで特定できない資料は`null`を許容するが、理由を`notes`へ記録する
- 二次資料だけで重要主張を確定しない。Development資料はStatusを明示し、Stableな規範として扱わない
- Sourceの変更が本文、図、Template、fixture、判断基準へ及ぼす影響を確認してから`checkedAt`を更新する

## 12. Editorial Input Intake

Repository外で作成した草稿、Source review note、Blueprintは非正本のEditorial Inputである。登録と状態の機械可読な正本は`editorial-input-manifest.json`、人間向けの決定的索引は`EDITORIAL_INPUT_MANIFEST.md`とする。Issue #63の過去コメントはimmutable provenanceとして参照し、削除や書換えを行わない。

### Package identityと事前検証

Package identityは`packageId + Package SHA-256`である。`EIP-NNNN`の数値部はappend-onlyなPackage登録順であり、再採番・再利用しない。ただし、Filename、Wave label、作成日時、File size、Package登録順、Issue comment順のいずれもCandidateのidentityまたは選択根拠にしない。ZIPを展開する前に次を実行し、Package SHA-256、Target、内部path、各file SHA-256を検証する。

```bash
python3 scripts/check_editorial_input_manifest.py \
  --verify-package .work/editorial-input/<package>.zip \
  --package-id <EIP-...> \
  --target <chapter-NN|appendix-id>
```

Validatorは追跡済みJSON Schemaの有限Keywordを外部依存なしでManifestへ適用し、未対応Keywordをfail closedで拒否する。さらにduplicate path、path traversal、absolute / hidden / drive-qualified path、symlink、暗号化member、未登録file、hash不一致を拒否する。Raw ZIPと`.predraft.md`は`.work/`配下にだけ置き、Gitへ追加しない。登録済みPackageが認可済みWorkspaceに存在しない場合、内容を推測再構成せず、直接採用したと主張しない。Canonical実装はIssue、current contract、再検証済み一次資料から作成できるが、不在事実をIntake Recordへ残す。

### Candidate selectionと有限Status

TargetのStatusは次の有限集合だけを使い、`statusHistory`をappendして遷移根拠を残す。

```text
registered-pending-prerequisites
candidate-selection-required
selected-for-intake
rejected-after-comparison
deferred
canonical-pr-open
consumed
blueprint-only
generator-blueprint-only
superseded-with-record
```

- 同一Targetに複数Candidateがある場合は`candidate-selection-required`とし、自動選択しない。
- 選択時は`selectedCandidateId`を一つ指定し、代替Candidateを`rejected`、`deferred`、または`superseded`へ明示的にDispositionする。
- `selected-for-intake`はbranch作成前の選択、`canonical-pr-open`は専用Draft PRとIntake Recordの存在、`consumed`は通常mergeとmain/publication gate完了を意味する。
- `blueprint-only`と`generator-blueprint-only`を完成本文として扱わず、候補が複数になれば`candidate-selection-required`、利用開始時は`selected-for-intake`または`canonical-pr-open`へ進める。
- `statusHistory`の先頭は、Targetを最初に所有したCandidate Packageの登録日・登録URL・入力roleに一致させる。後続Candidateを追加しても初期状態を書き換えない。
- `tests/fixtures/editorial-input/registration-snapshot.json`の`statusHistoryPrefix`はManifest 1.0.0確立時の固定prefixである。削除・書換えず、状態変更はManifestの`statusHistory`末尾にだけ追加する。
- Candidateの文言、ID、Source version、Statusをcurrent Repositoryより優先しない。

### Canonical PR Intake Record

`canonical-pr-open`ではManifestの`intakeRecord`とPR本文の「Editorial Input Record」を同時に追加する。最低限、Package ID / SHA-256、Target Issue、Input path / SHA-256、base main SHA、Content Safety Policy version、Publication Projection version、Input確認状況、Adopted / Rewritten / Rejected / Deferred、Source再確認、Canonical files、Known limitations、raw tracked files `0`を記録する。

Canonical PRは草稿を単純コピーせず、current Issue契約、既存正本、安全境界、一次資料へ再構成する。merge後にmain CI、Pages、公開markerを確認してから、別の計画metadata更新で`consumed`へ進める。Manifestと生成索引は次で検証する。

```bash
npm run check:editorial-inputs
npm run render:editorial-inputs
```

## 13. Chapter Definition of Done

各章の執筆IssueとPRは、次を満たして初めて完成とする。

**成果物の完成**は、すべてのControl、Telemetry、仮説がPassまたはAvailableになった状態を意味しない。判断に必要な必須欄が埋まり、Partial / Missing / Inconclusiveを隠さず、Gap、Owner、期限、許容結論、Decision、Reassessmentが記録された状態を含む。未解決の業務課題と、未完成の教材・成果物を混同しない。

### 内容と教育設計

- [ ] `book-config.json`の章ID、題名、学習目標と一致する
- [ ] 必須見出し、前提知識、導入Caseまたは判断要求、成果物、評価基準、まとめ、次の学習先を持つ
- [ ] 確認事実、分析判断、仮定、予測、推奨を区別し、分析判断には代替説明、情報ギャップ、確信度、無効化条件がある
- [ ] 良い例、悪い例、失敗または反証例のうち、学習目標に必要な対比がある

### 安全性と境界

- [ ] OWN / BRIDGE / DELEGATEを明示し、委譲先を読まなくても本章の論旨が成立する
- [ ] 実行内容にPurpose、Prerequisite、Authority / Scope、Expected evidence、Impact、Stop、Cleanupがある
- [ ] 実Target、実Credential、Token、Cookie、個人情報、未調整の脆弱性詳細を含まない
- [ ] 合成fixtureはfail-closedの公開前検査を通り、実Data混入時は生成・公開を停止する

### 出典と追跡性

- [ ] 重要主張を一次情報の`SRC-*`へ追跡でき、章末一覧とRegistry mappingが一致する
- [ ] 成果物、合成Case、fixtureのIDと関係が`artifact-index.md`および親Caseと一致する
- [ ] Decision RequirementからAction / Reassessmentまで、該当する追跡Chainを辿れる

### 品質Gate

- [ ] 章固有contract test、`npm test`、`BOOK_FORMATTER_DIR=<pinned checkout> npm run check:book-qa`が成功する
- [ ] Link、Anchor、Unicode、Textlint、Layout、Markdown structureのerrorが0件である
- [ ] 技術、安全・法・倫理、出典・鮮度、分析品質、教育設計を別Passでレビューする
- [ ] P0 / P1が0件、未解決Review Threadが0件であり、P2の採否と理由が記録されている
- [ ] `docs/`と`_site/`をcommitしていない

## 14. Part単位の執筆運用

Part単位の着手には`.github/ISSUE_TEMPLATE/part-writing.yml`を使用する。複数章を同じIssueで管理しても、原則として章ごとに独立PRとし、同一Repository内は依存順に直列化する。

Part Issueは、対象章、前提、非目標、Source、成果物、Case関係、安全境界、PR分割、レビュー担当Context、QA、公開確認、停止条件を持つ。代表章Gateの契約を変更する必要が生じた場合は、Part Issue内で暗黙に変更せず、契約変更Issueを分離する。
