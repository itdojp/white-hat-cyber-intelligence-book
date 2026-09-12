# 第8章 安全で再現可能なラボと証拠管理

## この章の位置付け

第7章で確認の優先順位を決めても、そのまま実環境の検証を始めてよいわけではない。本章では、許可された範囲をラボの境界へ落とし込み、開始条件、観測、停止、証拠の保持、残存確認を一つの計画にする。「動いた」と「安全に終了した」を分けるための章である。

- **OWN**: Lab Safety and Evidence Plan、証拠manifest、有限状態、停止判断、再現性と残存確認の接続。
- **BRIDGE**: 第2章のAuthority、第4章のAsset / Boundary、第6章のSignal Flow、第7章の確認優先順位、第20章の証拠処理。持ち帰るのは対象ID、許可範囲、必要な観測、残るGapである。
- **DELEGATE**: OS・コンテナ製品の構築、実環境の分離設定、専門的なDFIR取得手順。実装詳細は[インフラセキュリティ](https://itdojp.github.io/it-infra-security-guide-book/)と[ペネトレーションテスト学習](https://itdojp.github.io/pentest-learning-book/)へ委譲する。委譲先を読まなくても、付属の非実行モデルで本章の判断は完結する。

成果物は`ART-18 Lab Safety and Evidence Plan`。本章はコンテナ起動手順でも、法的証拠能力の認定手順でもない。実Runtimeは実行しない。すべてのreceiptとEventは著者が供給する合成入力である。

## 学習目標

- 安全なラボ境界を設計できる。
- 証拠manifestを作成できる。
- Lab Safety and Evidence Planを作成できる。

## 前提知識

[第2章](02-law-ethics-authorization.md)のAuthority / Scope / Stop、[第4章](04-assets-boundaries-threat-model.md)の信頼境界、[第6章](06-observable-systems.md)の観測とGap、[第7章](07-vulnerability-prioritization.md)の確認待ちの判断を前提とする。JSONのキーと値、ファイルのハッシュを比較する意味を知っていればよい。

ラボは、失敗したときに第三者や実Dataへ影響を広げず、何を確認できなかったかを残すための設計である。rootlessという名称だけで分離が成立したとは扱わない。コンテナには共有Kernelなどの残余リスクがあり、Host側の境界も必要になる。これはNIST SP 800-190の原則の要約であり、現行WSL2やPodmanの機能保証ではない。［SRC-NIST-CONTAINER-001］

## 導入ケース：終了コードだけで完了にしない

完全合成の請求書連携OAuthアプリについて、担当者が「解析は終了した。ラボも終了したはずだ」と報告した。しかし、外向き通信の境界に不整合を示すreceiptがあり、別のRunではCredentialの残存確認がUnknownだった。解析結果が得られたことを理由に、どちらも完了へ進めてよいだろうか。

教材の判断対象は`CASE-2026-001`、本章の補足は`LABPLAN-2026-001`で、関係はrefinesである。`AUTH-CASE-2026-001`と`DR-2026-001`を参照するが、実作業の許可を新たに発行するものではない。親のCoverage、Control assurance、Gap、期限を変更しない。

**確認事実**は、付属ファイルのバイト列、スキーマ適合、IDの対応、計算した状態である。**仮定**は、供給した合成receiptのPass / Fail / Unknownである。**分析判断**は、その仮定の下で開始・停止・再評価をどう扱うかである。実Hostで同じ条件が成立するかは分からない。

## 全体像：許可から再評価までを一本につなぐ

**F-08-01：Lab SafetyとEvidenceの追跡順。** 上から入力を照合し、FailまたはUnknownを見つけたら新規シナリオ操作へ戻らない。矢印は実行コマンドではなく、記録の参照関係である。

```text
Authority / Scope → Asset / Boundary → Lab Plan / Run ID
                  → Preflight → Ready → Running
                  → Stop → Evidence export → Destroy
                  → Cleanup verification → Reassessment
Fixture / Producer / Time → Evidence ID / Path / SHA-256 / Lineage
```

`SF-2026-001`と`VPR-ITEM-005`から、必要な観測と未確認条件を引き継ぐ。Evidenceの生成元、対象Run、停止記録、六種の残存確認、Owner、次回Reviewまで直接IDでたどれるようにする。同じCase IDでも、別Runの成功receiptを流用しない。

## 基本概念：境界と再現性を別々に確認する

### 境界は設定名ではなく確認項目にする

本章の構成モデルは、WSL2とrootless Podmanに相当する抽象設計である。実装版はnot-executed、Image digestはnullとする。版を固定せずに実行してよいという意味ではなく、そもそもコンテナを実行しないためである。実装へ進む場合は別のAuthority Gateで製品版、Image digest、Hostの条件、確認Evidenceをレビューする。

**T-08-01：抽象設計の境界。** 右欄は本教材で何を主張できないかを示す。

| 境界 | 計画する制約 | 本教材の限界 |
|---|---|---|
| 権限 | rootless、非特権、追加Capabilitiesなし | Host上の権限は未測定 |
| Network | 独立したLab境界、外向き通信は既定拒否 | Firewallや到達性を実測していない |
| Host | host networkを使用しない。広範なHost mountを禁止する | 実Mountは作成しない |
| Data | 合成のみ、入力は読み取り専用、出力は専用の一時領域という設計 | 実Volumeや一時領域は作成しない |
| Exposure | ローカル限定の設計、予約済みHostと文書用Addressだけ | 待受Portを開かない |
| Resource | CPU・Memory・Disk・時間の上限を確認する設計 | 具体的上限値や実測は実装時の別レビュー |

外向き通信、Runtime設定、Host側の分離を別々に確認するという考え方はSP 800-190 §§4.4–4.5を参照する。本章の項目数やPass判定は著者の有限教材契約であり、同文書の認証基準ではない。［SRC-NIST-CONTAINER-001］

### 八つの状態と三つの判定を混同しない

状態は`Planned / Preflight passed / Ready / Running / Stopped / Destroyed / Cleanup verified / Failed closed`の八つに固定する。判定は`Safe / Unsafe / Inconclusive`の三つであり、状態とは別の軸である。

**T-08-02：状態の意味と入口条件。** すべて合成receiptの評価として読む。

| 状態 | 入口条件 | まだ言えないこと |
|---|---|---|
| Planned | 対象、許可参照、境界、観測、停止、保持、Ownerを記録 | 実行可能であること |
| Preflight passed | 八項目の開始前receiptがすべてPass | 実環境で条件を測定したこと |
| Ready | 同じRunの開始条件が揃う。初期化・分離の確認をPreflightへ含める | 実作業の承認取得 |
| Running | Readyから同じRunの合成シナリオ評価に入る | プロセスやコンテナの実行 |
| Stopped | stopped receiptがPass | 残存物がないこと |
| Destroyed | 停止、Evidence export、destroyedの順にPass | Cleanupの六項目が完了したこと |
| Cleanup verified | Container・Network・Volume・File・Credential・PortがすべてPass | それ以前の異常がなかったこと |
| Failed closed | 必須チェックがFailまたはUnknown | 正常完了、同じRunの再開許可 |

正常系はPlannedからCleanup verifiedへ進む。PreflightがFailまたはUnknownならRunningに入らない。Running中の異常ではFailed closedを経由し、新規シナリオ操作を停止する。その後に扱うのは、定義済みの停止、Evidence保持、破棄、残存確認だけである。Runtimeのreceipt束は境界・権限・Data・Resource・収集・時計の条件照合であり、異常後に新しいProtocol操作を続けた記録ではない。停止を確認できなければ後続も未実施として残す。再開には新Run IDと再審査が必要になる。

`Unsafe`は訪問済みチェックにFailがある場合、`Inconclusive`はFailがなくUnknownがある場合、`Safe`は訪問済み必須チェックがすべてPassの場合である。FailはUnknownより優先して残す。未訪問の段階をPassへ補完しない。構造欠損、未知の語彙、ハッシュ不一致では判定報告自体を出さず、検証エラーで終了する。

Unsafeの後で残存確認を通過すると、最終状態はCleanup verifiedでも判定はUnsafeのままである。正常完了を示すcompletedNormallyはfalseを保持する。Cleanupで再びUnknownが出ればFailed closedを再記録する。履歴内の同じ状態名を勝手に除去しない。すべてのRunでexecutionAuthorizedはfalseであり、Safeも実作業の許可ではない。

### 再現性はバイト列と前提の組で記録する

同じ結果を得るには、Fixture ID、Model version、生成主体、固定時刻、入力順、文字コード、改行、Transform historyを固定する。付属モデル1.0.0は乱数も現在時刻も使わず、seed 208は一つの生成レシピの識別ラベルである。任意seedの生成器や一般のラボ評価器ではない。

合成OAuth同意、API認可、Telemetry収集の三種類のEventは、どの観測を必要とするかを考えるためのDataである。実TokenやCookieを含めず、Protocol requestも送らない。名前が似たEventから現実の動作を推定しない。

## 証拠manifest：同一性と意味を分ける

NIST SP 800-86は収集、検査、分析、報告を分け、取得計画、データの完全性確認、取扱いの記録を扱う。本章では、その区別を教材のEvidence ID、生成元、時刻、Hash、保持責任、変換履歴へ接続する。2006年の文書から古い製品操作やHash方式の推奨を引き継がない。［SRC-NIST-DFIR-001］

manifestには、Artifact ID、実際に読む相対Path、SHA-256、Producer、作成日時とTime zone、対象Run、元Fixture、Classification、Custodian、Retention、Transform historyを残す。SHA-256はこのRepositoryが選んだ教材の完全性契約であり、SP 800-86がその方式だけを指定するという主張ではない。

SHA-256が一致することは、指定されたバイト列と一致したことを示す。内容が真実であること、生成主体が信頼できること、取扱いの履歴が完全であること、法的証拠能力があることを単独では示さない。

Berkeley Protocolの取得時刻・Hash・文脈、取扱いの時系列、原本と作業コピーの区別を参照する。ただし同資料は人権・国際犯罪調査の文脈を持つ。本書の独自Templateは記録原則の限定的な応用であり、表の転載、法的手続の代替、Chain of custodyの認定ではない。［SRC-BERKELEY-001］

### Evidenceの保持とCleanupの対象を分ける

本教材のEVD-LAB08-001は、版管理される合成receiptファイルである。保持する教材正本と、実装モデル上で破棄する一時資源を区別する。CleanupのFileがPassでも、教材正本を削除したとは解釈しない。

Evidence exportを確認できなければ、証拠を失う破棄へ進まない。Destroyedだけで完了にせず、Container、Network、Volume、File、Credential、Portの各receiptを個別に照合する。Credential確認がUnknownなら、他の五項目がPassでもCleanup verifiedにしない。停止後の処理もAuthorityと事前計画の内側に限定する。

## 攻撃者・防御者・分析者・意思決定者の接続

攻撃者視点は「どの境界を越える条件が残るか」という仮説に留める。実Targetへ操作を追加して確認しない。防御者はNetwork、権限、Data、Resourceの制約と停止を設計する。分析者は同一RunのEvidenceとGapを分離する。意思決定者は未確認条件を隠さず、再開を許可できる根拠と責任者を求める。

親のSF-2026-001のCoverageはProducedであり、本章の合成PassによってCollectedやValidatedへ上げない。VPR-ITEM-005の確認待ちも解消しない。**確信度は低**とする。根拠は供給された合成Dataだけで、実Runtimeの隔離と残存は未測定だからである。代替説明は、実装版、Host条件、時計、収集経路がモデルと異なる可能性である。

## 安全な演習：三つのRunを読み取り専用で照合する

### Purpose / Prerequisite / Authority / Scope

目的は、開始条件、停止、Evidenceの同一性、Cleanupの判定を配布Dataから再計算することである。S0の設計とS1の合成Data解析だけを行う。LinuxまたはWSL2のLinux環境上のPython 3.11以上、取得済みの本Repository、書換えられていない付属JSON・Schema・親Caseを前提とする。この照合にNode、Ruby、コンテナ製品の起動、ネットワーク取得は不要である。

Authorityは配布された合成教材の読み取りに限定する。実対象への接続、走査、認証試行は行わない。実Credential・実Token・実Cookie・個人情報を入力しない。演習のScopeはread-only-synthetic-dataであり、実務へ転用するときは別の許可確認へ戻る。

### Expected evidence / Impact / Stop / Cleanup

期待Evidenceは三Runの判定・履歴と、EVD-LAB08-001のSHA-256一致である。実行は固定ファイルの読取りと標準出力だけで、コンテナ、待受Port、Network、Mount、Credentialを作成しない。下記ではPythonのBytecode cacheも抑止する。

実Dataの疑い、Scope不明、欠損、ID不一致、Hash不一致、未知の状態、予期しないエラーがあれば停止する。エラーを無視したり、結果をPassに書換えたりしない。付属原本と差分を照合し、教材責任者へ確認する。異常Runを正常完了に置き換えない。

このコマンド自体に削除対象の資源はない。自分で保存した報告コピーだけを所属先の取扱い規則に従って整理し、版管理された教材・親Caseは保持する。モデル内の六種Cleanup判定は、実Hostを走査または削除した証拠ではない。

### 読み取り専用Replay

Repositoryのルートで実行する。出力するのはJSON報告であり、ファイルは書き換えない。

```bash
python3 -B scripts/replay_chapter08_lab.py --json
```

期待される要約は次のとおりである。Safeはこの閉じた入力集合内の判定であり、現実の安全宣言ではない。

**T-08-03：三つの結果を比較する。** 不明や失敗を消さず、判定と終了状態を別欄で読む。

| Run | 判定 | 最終状態 | 正常完了 |
|---|---|---|---|
| RUN-LAB08-SAFE | Safe | Cleanup verified | true |
| RUN-LAB08-UNSAFE | Unsafe | Cleanup verified | false |
| RUN-LAB08-INCONCLUSIVE | Inconclusive | Failed closed | false |

UnsafeはRuntimeのegress receiptがFailである。外部通信を起こした例ではなく、境界違反を示す仮定を与えて停止判断を試す例である。InconclusiveはRuntimeのcollectionとCleanupのcredentialがUnknownであり、収集と残存を確定できない。

### 固定レシピと同じバイト列になるか

前項と同じ前提・停止条件で、固定レシピの生成結果を標準出力へ出す。BashとPOSIXのcmpが使える環境では、次の非書込み比較で元ファイルとの一致を確認できる。cmpがない場合はReplay報告のHash照合までとし、追加ツール取得を本演習の必須条件にしない。

```bash
set -o pipefail
python3 -B scripts/replay_chapter08_lab.py --emit-receipts | cmp - cases/fixtures/ch08-control-receipts.json
```

一致ならcmpは何も表示せず終了する。これは合成レシピの再現性であり、実RuntimeのEvent再現ではない。コマンドの一部でも失敗したら比較成功と報告しない。受理するファイルは三つの固定Pathだけで、任意Path、Path traversal、Symlink、非通常ファイル、上限超過は拒否する。この保護は静的な教材作業Treeを対象とし、同時に改変する攻撃者に対するFilesystem sandboxではない。

### 分析課題と反証

1. [完全合成記入例](../cases/ch08-lab-evidence-example.md)のPlanからAuthority、Boundary、Fixture、Evidence、Stop、Cleanup、Reassessmentをたどる。
2. UnsafeのCleanupがPassでも、completedNormallyをtrueにできない理由を説明する。
3. InconclusiveのcredentialがUnknownのまま、Cleanup verifiedと報告する案を差し戻す。追加で必要なEvidenceとOwnerを記入する。
4. Preflightの一項目がUnknownなら、Runningへ進めないことを状態表から説明する。配布原本を改変する必要はない。
5. Hashだけを新しい値に更新する案を退け、生成レシピ、ID、時刻、変換履歴、公開表示を同時に再審査する理由を説明する。

## 作成する成果物

[ART-18 Template](../templates/lab-safety-evidence-plan.md)に、目的、許可参照、Scope、Asset / Boundary、Lab / Run ID、版と条件、Preflight、期待・禁止Evidence、Stop、Evidence manifest、Cleanup、Owner / Reviewer、Gap、確信度、代替説明、再評価Triggerと日付を記入する。

提出物はPlanとEvidence manifestの組である。付属の[Plan JSON](../cases/fixtures/ch08-lab-plan.json)、[Control receipts](../cases/fixtures/ch08-control-receipts.json)、[Evidence manifest](../cases/fixtures/ch08-evidence-manifest.json)が完全記入例に対応する。自分の分析では実Dataを追加せず、未確認の欄をUnknownと理由で保持する。空欄を埋めるために実測したことにしない。

## 評価基準

**T-08-04：ART-18のRubric。** 各項目を0〜2点で確認する。合計点が高くても必須安全条件の欠落を相殺しない。

| 観点 | 0点 | 1点 | 2点 |
|---|---|---|---|
| Authority / 境界 | 許可・対象が不明 | IDだけ記入 | 範囲、制約、親の未変更まで接続 |
| 状態と停止 | 失敗を正常化 | 状態列のみ | 開始拒否、Fail保持、再開不可を説明 |
| Evidence | Hashだけ | 元と時刻あり | Run、Producer、実Byte、Lineage、限界が一致 |
| Cleanup | 終了を完了と同一視 | 部分確認 | 六種、Evidence保持、Unknownの扱いが明確 |
| 判断と再評価 | 安全を断定 | Gapのみ | 根拠、低確信度、代替、Owner、次回日まで追跡 |

Authority欠落、実Data混入、未知をPassへ補完、証拠保持前の破棄、親の状態の根拠なき昇格は点数に関係なく差戻しとする。Unknownが残ること自体は教材の未完成を意味しない。必要な次の判断と責任が記録されているかを評価する。

## よくある誤解

- 「rootlessならHostは安全」ではない。HostとNetworkを含む境界の確認が必要である。
- 「終了コードが0ならCleanup完了」ではない。各資源の残存確認が別に必要である。
- 「Hashが一致したので証拠内容は真実」ではない。同一性と信頼性を分ける。
- 「Destroyedなので正常完了」ではない。失敗したRunの判定を保持する。
- 「Safeなので実作業を許可できる」ではない。合成モデルは実Authorityを発行しない。
- 「同じ出力なので実環境も再現した」ではない。固定Dataと実測結果を区別する。

## 章のまとめ

安全なラボ設計は、境界を宣言するだけでなく、開始できない条件、停止後のEvidence保持、六種の残存確認、再評価までを結ぶ。八状態の履歴と三判定を分けると、異常後にCleanupだけ完了した場合も隠さず記録できる。

Evidence manifestは、バイト列の同一性と、その意味・取扱い・限界を別々に残す。ART-18は実環境の保証書ではなく、判断を再検討できる計画と記録である。

## 次に学ぶこと

次の第9章では攻撃評価のライフサイクルへ進む。本章からはAuthority、停止条件、必要Evidence、Cleanupと再評価のGateを持ち込む。具体的評価の前に、親Caseと[安全・公開範囲](../SAFETY_SCOPE.md)へ戻って対象を確認する。証拠処理の専門的な展開は第20章へ接続する。

## 参考文献・Source Note ID

- `SRC-NIST-CONTAINER-001`: NIST SP 800-190、Final、September 2017。共有Kernel、Network、Runtime、Hostの境界原則。
- `SRC-NIST-DFIR-001`: NIST SP 800-86、Final、August 2006。収集・検査・分析・報告、完全性と取扱い記録の区別。
- `SRC-BERKELEY-001`: Berkeley Protocol、2022 edition。取得時刻・Hash・文脈と、取扱い履歴・原本と作業コピーの区別に限定。

確認日は2026-09-13。版、日付の不明点、採用箇所、取得上の制約は[Source Review Note](../references/ch08-source-review-2026-09-13.md)を参照する。
