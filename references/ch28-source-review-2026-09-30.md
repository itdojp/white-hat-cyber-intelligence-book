# 第28章用途限定Source確認（2026-09-30 JST / 初期Draft）

Issue50のSource→Input→Claim→Verification→HumanDecision設計に対する限定読解。第28章の初期Draftの限定用途だけを記録し、既存27監査のcheckedAtを28監査へ読み替えない。一次資料の取得URL/最終URL/時刻/bytes/SHAはローカル証拠へ保存し、以下に公式URLと実体SHAを記録する。環境既存pypdfで公式PDFテキストを抽出、PDF表紙直接画像目視/全仕様監査は未実施。初回pdftotext未導入による抽出失敗は保存、再取得して既存pypdfで完了。依存追加なし。OWASP PDFのoffset警告は原取得bytesを変更せず、版表紙・対象頁の抽出可否と内容を限定確認。

## SRC-AIRMF-001 — NIST AI600-1 / final

[公式刊行頁](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)、[公式PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)。2024-07-26刊行、頁の2026-04-08更新と区別。PDF SHA6e73620ab6b64e90ef2c04bf0e0d6246185a2f4b1b13cab0df494496cff89b6a。2.2 Confabulation（printed6 /PDF10）の誤った説明・引用と過信、MS-2.5-001/003/005の狭い試験からの汎化回避・Citation確認・Data provenanceという確認観点を読む。Suggested Actionを法的義務へ変換しない。本書五StatusやCase判定は本書独自で、GAI性能や安全保証を検証したものではない。

## SRC-AML-001 — NIST AI100-2e2025 / final

[CSRC正式頁](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)、[公式PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-2e2025.pdf)。2025-03-24 / correctedPDF04-01告知。SHA4811fb6ad73f9c9121843ab77e029b5adc6f2c86d33c2fc5b2099ef133847646。3.3/3.4の直接・間接入力と分類をSource/Tool/MemoryとInstructionの混同を読む語彙として用いる。06-03potential updates SHAac73cb5fe5e5c6dfaef566866d92ad5c9887176480f620112cc6a997d7d624d8 はpage x分類索引案で正式本文更新ではない。taxonomyや対策一覧はClaim支持・検証完了・汚染検出の網羅性の証明ではない。

## SRC-OWASP-LLM-001 — OWASP LLM Top10 2026 / released

[公式resource](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)、[PDF](https://genai.owasp.org/download/56857/?tmstv=1785822482)。122頁 / SHAef87993a4e50ae9d83b41ff7a3d3e6320a82dfa8d4ec6bf98d0ce264b2e6108e。版2026、PDF刊行dayplaceholderはnull維持。LLM01:2026 PromptInjection / LLM07:2026 Misinformation / LLM10:2026 ImproperOutputHandlingを入力の指示昇格・誤引用/過信・出力の実行非許可の分離に用いる。2025の番号を当てはめない。用途限定観点であり全分類への適合/実Model耐性/Injection検出性能を証明しない。

## SRC-OWASP-AGENT-001 — Agentic Top10 2026 guidance / released

[公式resource](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)、[PDF](https://genai.owasp.org/download/52117/?tmstv=1765059207)。57頁 / SHAa2db94cd00b08e0b3a5e5b619afe024bdbcd74503111085705e4f3dd886fcb5c。Version2026、PDF December2025、12-09 resource/blogと12-10 press本文を区別、既存publishedAtはpress精度のまま。ASI01GoalHijack / ASI06MemoryContextPoisoning / ASI09HumanAgentTrust（printed9/24/33）を未信頼Dataの指示化、永続化、human over-relianceの区別に使う。資料自身の旧LLM2025への相互参照を2026へ書換えない。実Agent試験や本書五ClaimStatusの規範的認定には使わない。

## 非採用と限界

AISVS1.0とAITGv1はIssue50登録時の補助候補。今回四Sourceのみの限定設計なので新要件番号/準拠/全テスト済を主張しない。採用追加が必要になった場合は固定実体と該当節を別監査する。原Parent25/26の合成Sourceは事案内記録、上記SRCは方法の参考文献であり混ぜない。一次資料のhash一致は実体同定で、内容やCase結論の正しさの認証ではない。
