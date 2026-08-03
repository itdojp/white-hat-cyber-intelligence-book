# 合成Case索引

このディレクトリは、本書の章で使用する完全合成Caseの索引である。

- すべての組織、担当者、Domain、ログ、判断は架空である。
- 実在Targetの調査や実在主体の帰属には使用しない。
- 機械可読fixtureは[fixtures catalog](./fixtures/index.md)で管理する。

## 公開中のCase

| 章 | Case | 主な成果物 | 備考 |
|---|---|---|---|
| 第1章 | [請求書連携OAuthアプリの権限見直し](./ch01-integrated-security-case-example.md) | Integrated Security Case Map | Assessment、Detection、Decisionの接続 |
| 第25章 | [共同報告に埋もれた技術クラスタの判断](./ch25-structured-analysis-attribution-example.md) | Analytic Judgment Record | 競合仮説、不確実性、Attribution Ladder、circular reporting |

## 利用上の注意

- `.example`、`.test`、`.invalid`以外のDomainをCaseへ追加しない。
- 実Credential、個人情報、第三者Dataを持ち込まない。
- Negative Findingは不存在証明として扱わない。
