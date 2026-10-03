# IPA早期警戒ガイドライン Source Review — 2026-10-03

## 確認した変更と採用範囲

[IPA公式ページ](https://www.ipa.go.jp/security/guide/vuln/partnership_guide.html)は2026-10-01に2026年版を公開した。`SRC-IPA-VDP-001`の現行参照版を更新する。ページの更新日、PDF表紙の発行月、各章の過去の確認日を混同しない。

[2026年版](https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/partnership_guideline.pdf)のI〜III、およびIV〜Vの関係者の役割・取扱いを、第2・9・15章の用途に限定して確認した。NICT連携と内閣府対応の追加は把握したが、個別の法的適用や新しい検査権限を本書へ導入しない。届出・調整は検査許可や公表承認を代替しない。

本確認は全法令の解釈、全64頁の意味監査、実届出や実検査、第三者への再配布許諾の認定ではない。PDF本文・図表を転載しない。

## 取得証跡

| 資料 | 取得日 | bytes | 頁数 | SHA-256 |
|---|---|---:|---:|---|
| 2026年版PDF | 2026-10-03 | 1,241,382 | 64 | `9c55ba412db2c38c0ce3e463e6273e5ba371ab6647664b109651493f5761ea39` |
| 2024年版PDF | 2026-10-03 | 1,221,433 | 61 | `98ec2ed52e14a2065c4a4befd154be2627d47fb08d4ed290b93d20438183e458` |

[旧2024年版の専用URL](https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/partnership_guideline_2024.pdf)のbytesは過去の監査hashと一致した。旧Source Review Noteにある`partnership_guideline.pdf`はその取得日時点の記録であり、現在も2024版を返すという主張ではない。同URLの新旧hashを混ぜない。

過去の[第2章](ch02-source-review-2026-08-05.md)、[第9章](ch09-source-review-2026-09-13.md)、[第15章](ch15-source-review-2026-09-17.md)の監査記録を履歴として保持する。Registry-wideの確認日と他58 Sourceの確認日は進めない。

## 影響する教材と変更しない判断

- [第2章](../manuscript/02-law-ethics-authorization.md): 役割と現行窓口を確認する高位の説明を維持。合成Authorizationの失効、停止、Disclosure Gateは変更しない。
- [第9章](../manuscript/09-engagement-roe.md): RoEの計画条件を維持。Source確認日を実施承認や実Runtimeの開始へ変換しない。
- [第15章](../manuscript/15-findings-retest-risk.md): Findingの状態と、対策情報の取扱い・調整を引き続き分離。実通知・公表時期・リスク受容の承認は認定しない。

採用している高位の役割・定義の説明との矛盾は今回の限定比較では見つからなかった。これは全手続の同一性や個別事案への適法性を証明するものではない。本文・Template・Caseを改訂したようには扱わず、Source Identityと限定監査契約だけを同期する。

合成Caseの`asOf`や承認期間は、各教材が表す過去の判断時点のまま保持する。2026年版のSource確認を、2026-09-13や2026-09-16等の過去のCase時点へ遡及した根拠・承認として扱わない。過去のCaseと現在のSource Baselineは異なる時点の記録である。

第9・15章末の「2024年版」は、その章の執筆・合成Case時点に使用した版の記録として保持する。現行版の表示は[Source Baseline](reference-baseline.md)で行い、過去の引用版を2026年版に置き換えたとは主張しない。旧版の本文との照合には上記の2024年版専用URLを使う。

## 次回確認と停止条件

次回確認は2027-01-03、または版・受付案内・採用範囲・関係法令の変更時。重要な意味変更が見つかれば対応章の編集・独立レビューまで止める。Sourceの確認だけで付録A/D/Hや初版Releaseを完了扱いにしない。

Source版の旧戻し、2024版のまま監査日だけ更新する移行、公開日の取り違え、限定監査の証跡欠落は出版前契約で拒否する。以後の限定再監査で日付を進めることは妨げないが、日付の機械検査だけでは主張の鮮度を証明できず、再監査の範囲と証跡を別途残す。`Content Safety Policy 1.2.0`、`Publication Projection 1.1.0`、formatter pinは変更しない。再現性検査は法的判断や真正性の自動認定ではない。

[Source Baseline](reference-baseline.md) / [移行Issue #189](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/189)
