# 第27章 Source再監査（2026-09-29）

対象は第27章、ART-31、完全合成Caseと有限比較です。Registry全体や第28章の未制作本文、全標準への適合性を確認したという意味ではありません。取得した公式実体のhashと限定読解範囲を記録します。図や表、攻撃例、要件全文は転載せず、独自の非実行教材を制作しました。

## NIST AI 600-1

SRC-AIRMF-001は[公式刊行頁](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)と[公式PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)を確認。NIST AI 600-1 / final / 2024-07-26を保持します。採用は1・2節のSystemとライフサイクル、3節GV-1.7の停止、GV-6.1の由来という確認観点だけです。Suggested Actionを一律の義務や侵入試験手順にはしません。PDF SHA-256は`6e73620ab6b64e90ef2c04bf0e0d6246185a2f4b1b13cab0df494496cff89b6a`です。

## NIST AML taxonomy

SRC-AML-001は[NIST AI 100-2e2025のCSRC頁](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)と[PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf)を確認。final / 2025-03-24を保持し、3.3・3.4の直接/間接入力の分類に限定します。2025-04-01 corrected PDFの告知と[2025-06-03 potential updates](https://csrc.nist.gov/files/pubs/ai/100/2/e2025/final/docs/nist.ai.100-2e2025_potential_updates.pdf)も確認しました。後者はpage xの分類索引の訂正案で、正式本文の更新ではありません。該当索引を転載せず、語彙への対応付けを対策の完全性や成功率と混同しません。PDF SHA-256は`4811fb6ad73f9c9121843ab77e029b5adc6f2c86d33c2fc5b2099ef133847646`、potential updatesは`ac73cb5fe5e5c6dfaef566866d92ad5c9887176480f620112cc6a997d7d624d8`です。公式final頁と限定した後継版探索を確認しましたが、全世界の新研究を網羅した監査ではありません。

## OWASP LLM Top 10 2026

SRC-OWASP-LLM-001は[2026公式resource](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)、[公式告知](https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/)、[公式PDF](https://genai.owasp.org/download/56857/?tmstv=1785822482)を確認しました。resource日は2026-08-03、告知頁日は09-01、本文発表日は09-02です。PDFにはVersion 2026と刊行日のplaceholderがあるため、実体のpublishedAtはnullにし、三つの日付を代入しません。

利用はLLM01 / 03 / 04 / 05 / 09 / 10の境界の区別です。Excessive Agencyが03、Supply Chainが04、Improper Output Handlingが10となり、旧2025版の番号とは異なります。Agentic資料中の旧2025参照を書き換えたとは扱いません。Registryの2025から2026への変更は意味変更で、本文、図、Template、固定Case、対比と版付き参照を同時に確認します。全Riskや攻撃例の実証は行いません。122頁PDF SHA-256は`ef87993a4e50ae9d83b41ff7a3d3e6320a82dfa8d4ec6bf98d0ce264b2e6108e`です。

## OWASP Agentic Top 10 2026

SRC-OWASP-AGENT-001は[公式resource](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)、[公式告知](https://genai.owasp.org/2025/12/09/owasp-genai-security-project-releases-top-10-risks-and-mitigations-for-agentic-ai-security/)、[PDF](https://genai.owasp.org/download/52117/?tmstv=1765059207)を確認。Version 2026、PDFはDecember 2025、告知はblog12-09 / 本文12-10です。publishedAtは告知本文の2025-12-10という既存精度を保持し、PDF自体のdayとはしません。ASI01 / 02 / 03 / 04 / 06 / 07 / 08 / 09を、目標、権限、Memory、通信、波及、人間の過信を分ける確認観点に限定します。57頁PDF SHA-256は`a2db94cd00b08e0b3a5e5b619afe024bdbcd74503111085705e4f3dd886fcb5c`です。

## AISVS 1.0 stable

SRC-AISVS-001は[公式project](https://owasp.org/projects/artificial-intelligence-security-verification-standard-aisvs-docs)、[固定commitのlocked1.0](https://github.com/OWASP/AISVS/tree/aedffade1817238a493ff4d63c28d0d3855c98db/1.0)のMarkdown/PDFを確認。latest stableは1.0、1.01-devは開発中です。現在のresearch wikiやAI生成研究補足は要件の根拠にしません。PDF/headerはJune 2026まで確認できましたが、旧Registryの06-24というdayは今回確認できませんでした。publishedAtをnullとし、旧確認履歴をnotesへ保持します。版は確認できており、dayを推測する必要はありません。

採用はv1.0-C6.1.3、C8.1.3 / C8.2.3 / C8.3.1、C9.2.1 / C9.5.3 / C9.6.1 / C9.6.2、C12.4.2 / C12.4.3という版付き確認観点です。本文で番号を短縮している場合もこの1.0だけを指します。Templateや六状態は本書独自で、AISVS Level達成を主張しません。固定commitは`aedffade1817238a493ff4d63c28d0d3855c98db`、PDF SHA-256は`ff15584843a53d4fd2b52940c98cb15f9ebe1340151d90d54bb74db9cf8468f6`です。

## 影響範囲と未確認

個別五SourceのcheckedAtだけを更新し、Registry-wide baselineは保持します。未制作の第28章へのmappingは実使用する第28章PRで追加します。現行他章の正文/親記録は変更しません。NIST SP800-218Aは入口/PDF取得のみで、今回の規範IDや本文Sourceへ新規採用しません。第13章のSupply Chainを方法参照にします。

PDFは取得bytesとテキストを確認しています。Web screenshot呼出しは画像payloadを得られなかったため表紙画像の直接目視を完了したとは主張しません。PDFの文字抽出から分かる版・日付精度と、未確認部分を分離しています。hashは取得実体の固定であり、内容の正しさの証明ではありません。

再確認Triggerは版/errata変更、Risk番号の改訂、AISVS要件ID/安定版の変更、採用した停止/由来/権限/Memory/監査の意味変更です。Source資料は独立した成功実験ではなく、供給教材の事実は著者が作成した合成記録だけです。
