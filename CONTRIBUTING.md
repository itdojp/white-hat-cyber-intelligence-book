# Contributing

## 基本方針

変更はGitHub Issueを起点とし、目的、対象外、受入条件、安全停止条件を明記してください。既存Issueと重複するPRを作成しないでください。

## Pull Request

- 一つのPRに一つの主目的
- 正本を編集し、生成物だけを手編集しない
- 事実と分析判断を分ける
- 時点依存の主張にSource Note IDを付ける
- 実Credential、Cookie、Token、個人情報を含めない
- 例示には`.example`、`.test`、RFC 5737等の文書用範囲を使う
- 攻撃技法には観測、検知、緩和、停止条件を添える
- 実行した検査と未実施の検査をPR本文へ記録する

## 章の変更

章の大幅変更は、`WRITING_GUIDE.md`の標準構造と`CROSS_BOOK_MAP.md`の境界に従います。既存専門書で詳述済みの内容をコピーせず、必要な要約と安定した参照を置いてください。

非正本のEditorial Inputを参照する場合は`editorial-input-manifest.json`でPackage、Target、Candidate、Dispositionを確認し、`WRITING_GUIDE.md`のIntake契約に従ってください。Raw ZIPと`.predraft.md`はcommitしません。

## 出典

`SOURCE_POLICY.md`に従い、一次資料を優先します。新しい主要出典は`references/sources.json`へ追加してください。

## 安全な演習

演習の新規追加は`LAB_ARCHITECTURE.md`と`SAFETY_SCOPE.md`へ適合させ、Initialize、Observe、Export Evidence、Destroy、Verify Cleanupの手順を含めてください。
