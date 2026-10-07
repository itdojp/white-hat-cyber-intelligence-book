"""Reviewed, finite ART06 judgment vocabulary (Layer A), not natural-language AI.

Each profile binds an existing Case to its computed result/gap and controlled
analysis fields. Editorial data/projection digest refreshes cannot introduce new
claims. Changes to this vocabulary require explicit semantic review; do not
learn it from the current JSON or regenerate it as part of checkpoint updates.
No inference about arbitrary Japanese prose, authenticity or real incidents.
"""

from dataclasses import dataclass

from scripts.chapter18_query import LIMIT, PLAN


@dataclass(frozen=True)
class JudgmentProfile:
    corpus_id: str
    result: str
    query_gaps: tuple[str, ...]
    permittedConclusion: str
    alternative: str
    confidence: str
    confidenceBasis: str
    gap: str
    nextAction: str


# Controlled statements reviewed against each supplied example, not a hash of it.
PROFILES = {
    "HCASE18-001": JudgmentProfile(
        corpus_id="QCASE18-01",
        result="Supported",
        query_gaps=(),
        permittedConclusion="供給承認で説明できない同意変更と30分以内の同じ対象の利用が、この固定入力で組になった。",
        alternative="未記録の正当な変更かもしれない。",
        confidence="中",
        confidenceBasis="Event二件の対応は明確だが、供給Snapshot外の業務文脈はない。",
        gap="実業務文脈と原記録の真正性は未評価。",
        nextAction="Detection見直し候補とIR評価依頼を別々に記録する。",
    ),
    "HCASE18-002": JudgmentProfile(
        corpus_id="QCASE18-02",
        result="Weakened",
        query_gaps=(),
        permittedConclusion="すべての候補変更が供給承認の対象・Window・Scopeで説明され、当初の仮説は弱まった。",
        alternative="承認Snapshot自体の誤りは本比較で排除できない。",
        confidence="中",
        confidenceBasis="候補一件と承認一件を照合したが、現実の承認過程は検査していない。",
        gap="供給外の承認来歴は不明。",
        nextAction="入力版や承認条件が変わった時の再評価を記録する。",
    ),
    "HCASE18-003": JudgmentProfile(
        corpus_id="QCASE18-03",
        result="Negative finding",
        query_gaps=(),
        permittedConclusion="供給された三Streamの条件を仮定した限定Windowで該当する組を観測しなかった。",
        alternative="範囲外の期間や別行動は未観測のままである。",
        confidence="中",
        confidenceBasis="固定Queryと供給Coverageが整合する範囲に限る。",
        gap="実Coverageと対象外行動は評価していない。",
        nextAction="範囲を一般化せず、ScopeやCoverage変更時に再評価する。",
    ),
    "HCASE18-004": JudgmentProfile(
        corpus_id="QCASE18-04",
        result="Inconclusive",
        query_gaps=("behavior-not-tested",),
        permittedConclusion="合成IOCラベルの一致はあるが、行動仮説を検証していないため判断できない。",
        alternative="一致値が正当な利用を指しているかもしれない。",
        confidence="低",
        confidenceBasis="一致ラベル以外の行動比較を実施していない。",
        gap="行動仮説の比較が未実施。",
        nextAction="同じ供給ScopeでBehavior比較を計画し、実Targetは追加しない。",
    ),
    "HCASE18-005": JudgmentProfile(
        corpus_id="QCASE18-06",
        result="Inconclusive",
        query_gaps=("consent:producer-gap",),
        permittedConclusion="一致がなくてもconsentの生成根拠が不足し、仮説の反証にはならない。",
        alternative="Eventが生成されていないだけかもしれない。",
        confidence="低",
        confidenceBasis="不足するProducer条件を0件では補えない。",
        gap="consent:producer-gap。",
        nextAction="生成条件を説明する合成入力の再確認候補を記録する。",
    ),
    "HCASE18-006": JudgmentProfile(
        corpus_id="QCASE18-08",
        result="Inconclusive",
        query_gaps=("consent:retained-gap",),
        permittedConclusion="保持条件が不足するため、観測なしを限定的な反証としても扱わない。",
        alternative="必要な記録が保持範囲から外れた可能性がある。",
        confidence="低",
        confidenceBasis="比較対象が残っているという仮定を満たさない。",
        gap="consent:retained-gap。",
        nextAction="必要Windowと保持根拠の確認をCollection候補へ渡す。",
    ),
    "HCASE18-007": JudgmentProfile(
        corpus_id="QCASE18-15",
        result="Inconclusive",
        query_gaps=("arrival-incomplete",),
        permittedConclusion="判断時点までに対象Eventがそろっておらず、結論を保留する。",
        alternative="単なる到着遅延による欠測かもしれない。",
        confidence="低",
        confidenceBasis="Event時刻は範囲内でも取り込みがasOfを超える。",
        gap="arrival-incomplete。",
        nextAction="到着条件を更新した新しい入力版で再評価する。",
    ),
    "HCASE18-008": JudgmentProfile(
        corpus_id="QCASE18-16",
        result="Inconclusive",
        query_gaps=("time-uncertainty",),
        permittedConclusion="時刻誤差により固定Windowや順序を確定できず、組の成立を主張しない。",
        alternative="見かけの順序が時計誤差で生じた可能性がある。",
        confidence="低",
        confidenceBasis="時刻品質が本Queryの前提を満たさない。",
        gap="time-uncertainty。",
        nextAction="許容できる時刻根拠を備えた新入力で再評価する。",
    ),
    "HCASE18-009": JudgmentProfile(
        corpus_id="QCASE18-17",
        result="Inconclusive",
        query_gaps=("identity-unjoinable",),
        permittedConclusion="同じWorkload文字列でもNamespaceが異なり、同一対象の組と判断しない。",
        alternative="異なる対象が同じ表示名を使っているかもしれない。",
        confidence="低",
        confidenceBasis="NamespaceとNormalizerの一致が必要である。",
        gap="identity-unjoinable。",
        nextAction="合成Identity対応の確認をCollection候補へ残す。",
    ),
    "HCASE18-010": JudgmentProfile(
        corpus_id="QCASE18-24",
        result="Stopped",
        query_gaps=("scope-expansion",),
        permittedConclusion="有効なScope拡大の停止理由を優先し、行動の評価を続けない。",
        alternative="停止していない場合のResultはこの記録の主張ではない。",
        confidence="高",
        confidenceBasis="指定された停止理由の適用だけは入力から確認できる。",
        gap="scope-expansion。",
        nextAction="Scope確認へ戻し、実権限を追加せず計画を再評価する。",
    ),
    "HCASE18-011": JudgmentProfile(
        corpus_id="QCASE18-27",
        result="Supported",
        query_gaps=(),
        permittedConclusion="Ticketは一致してもScope包含が不足するため、説明できない変更と利用の組が残る。",
        alternative="未記録の追加承認があるかもしれない。",
        confidence="中",
        confidenceBasis="TicketだけでなくScope集合を比較している。",
        gap="供給Snapshot以外の承認は不明。",
        nextAction="不足する承認文脈を明示して検知候補と評価依頼を分ける。",
    ),
    "HCASE18-012": JudgmentProfile(
        corpus_id="QCASE18-19",
        result="Negative finding",
        query_gaps=(),
        permittedConclusion="成功した利用が別Workloadなので、指定Population内の該当組は観測していない。",
        alternative="別Workloadの活動は本仮説の反証にも支持にも使わない。",
        confidence="中",
        confidenceBasis="対象固定の結合条件に限った比較である。",
        gap="範囲外の対象は未評価。",
        nextAction="Populationを無断で広げず、条件変更時の再評価を残す。",
    ),
}

REASSESSMENT = (
    "入力版、Query、Scope、Window、Population、Coverage、承認文脈の変更時に再評価する。"
)
HANDOFF_ACCEPTANCE = "受け手が対象版、問い、許容結論、代替説明、Gapを別途評価する。"
HANDOFF_LIMITATION = "記録は実通知、受領、Incident宣言、実行権限を意味しない。"
ANALYSIS_FIELDS = (
    "permittedConclusion",
    "alternative",
    "confidence",
    "confidenceBasis",
    "gap",
    "nextAction",
)


def judgment_errors(row, actual):
    """Fail closed outside this reviewed vocabulary, including benign rewrites.

    Exact controlled statements are intentional: a token blacklist or merely
    checking a structured `noCompromiseClaim` flag cannot validate free prose.
    The query must independently justify the profile's result and gaps, and its
    scope stays tied to the supplied input. Existing model checks additionally
    bind handoff routes, receipt, authority, owner and due date.
    """
    profile = PROFILES.get(row["id"])
    if profile is None:
        return [row["id"] + ": unreviewed judgment profile"]
    errors = []
    if (
        row["corpusId"] != profile.corpus_id
        or actual["result"] != profile.result
        or tuple(actual["gaps"]) != profile.query_gaps
        or actual["limit"] != LIMIT
        or actual["scope"] != PLAN
    ):
        errors.append(row["id"] + ": judgment result/scope/profile binding")
    judgment = row["judgment"]
    for field in ANALYSIS_FIELDS:
        if judgment[field] != getattr(profile, field):
            errors.append(row["id"] + ": unreviewed judgment claim: " + field)
    if judgment["reassessment"] != REASSESSMENT:
        errors.append(row["id"] + ": unreviewed judgment reassessment")
    for handoff in row["handoffs"]:
        if (
            handoff["acceptance"] != HANDOFF_ACCEPTANCE
            or handoff["limitation"] != HANDOFF_LIMITATION
        ):
            errors.append(row["id"] + ": unreviewed handoff analysis boundary")
    return errors
