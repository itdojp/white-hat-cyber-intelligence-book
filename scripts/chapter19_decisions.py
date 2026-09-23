"""Finite ART-25 educational decision guards; not a live IR automation system.

Every receipt is a supplied synthetic assumption, not authenticated evidence.
No rendering, product operation, legal decision, network or filesystem access.
"""

from datetime import datetime

VERSION = "1.0.0"
STATES = (
    "Suspected",
    "Declared",
    "Contained",
    "Investigating",
    "Recovering",
    "Closed",
    "Reopened",
)
LIMIT = "supplied-synthetic-record-only-not-authority-or-authenticity"
TRANSITIONS = {
    "Suspected": ("Suspected", "Declared"),
    "Declared": ("Contained", "Investigating"),
    "Contained": ("Investigating", "Recovering"),
    "Investigating": ("Contained", "Recovering"),
    "Recovering": ("Investigating", "Closed"),
    "Closed": ("Reopened",),
    "Reopened": ("Investigating", "Contained"),
}
OPTIONS = {
    "OPT-IR19-DISABLE": {
        "name": "App停止案",
        "security": "当該Appの利用を抑える案。別経路の停止までは主張しない。",
        "business": "合成請求処理が停止する想定。",
        "evidence": "状態変化前の記録を保持する必要がある。",
        "rollback": "所有者の再判断と供給復旧条件の照合を要する案。実操作なし。",
    },
    "OPT-IR19-RESTRICT": {
        "name": "Permission制限案",
        "security": "問題となる権限の範囲を限定する案。侵害の終結ではない。",
        "business": "合成Export機能が一時利用不能となる想定。",
        "evidence": "変更前後の権限Snapshotを別々に保持する。",
        "rollback": "再拡大は別承認と検証の対象。実操作なし。",
    },
    "OPT-IR19-MONITOR": {
        "name": "Monitoring強化案",
        "security": "観測を増やす案であり、それだけでは封じ込めにならない。",
        "business": "保管量と分析負荷が増える想定。",
        "evidence": "新規観測と既存記録を区別する。取得済みとはしない。",
        "rollback": "追加観測の終了条件を別記する案。実操作なし。",
    },
}


def instant(value):
    """A deliberately finite UTC timestamp representation, not timezone inference."""
    if not isinstance(value, str):
        raise ValueError("ART25 UTC timestamp type")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise ValueError("ART25 UTC timestamp") from exc
    if parsed.strftime("%Y-%m-%dT%H:%M:%SZ") != value:
        raise ValueError("ART25 canonical UTC timestamp")
    return parsed


def evaluate(data):
    """Schema validation is the caller's responsibility; referential failures stop.

    A valid but incomplete record is deferred, not silently promoted. A malformed
    reference/scope/time is an input error, not an alternative supported conclusion.
    """
    current = data["decision"]
    previous = data["previous"]
    context = data["context"]
    at = instant(current["at"])
    before = instant(previous["at"])
    start, end = (instant(context[k]) for k in ("start", "end"))
    if not start < end <= before < at:
        raise ValueError("ART25 observation/previous/decision chronology")
    if current["requested"] not in TRANSITIONS[previous["status"]]:
        raise ValueError("ART25 finite educational transition")
    evidence = {e["id"]: e for e in data["evidence"]}
    if len(evidence) != len(data["evidence"]):
        raise ValueError("ART25 duplicate evidence ID")
    assets = context["assets"]
    if not assets or len(set(assets)) != len(assets):
        raise ValueError("ART25 finite subject assets")
    for e in evidence.values():
        if (
            e["subject"] != context["subject"]
            or e["revision"] != context["revision"]
            or e["asset"] not in assets
            or not start <= instant(e["windowStart"]) < instant(e["windowEnd"]) <= end
            or not instant(e["windowEnd"]) <= instant(e["availableAt"]) <= at
        ):
            raise ValueError(
                "ART25 evidence subject/revision/scope/window/availability"
            )
    scope = data["scope"]
    selected = [a for values in scope.values() for a in values]
    if sorted(selected) != sorted(assets):
        raise ValueError("ART25 disjoint complete scope inventory")

    def receipt(ref, kind, deadline=at, asset=None):
        if ref is None:
            return False
        if ref not in evidence:
            raise ValueError("ART25 unresolved evidence reference")
        e = evidence[ref]
        if e["kind"] != kind or (asset is not None and e["asset"] != asset):
            raise ValueError("ART25 evidence kind/asset binding")
        return e["outcome"] == "supported" and instant(e["availableAt"]) <= deadline

    for asset in scope["confirmed"]:
        if not any(
            e["kind"] == "scope-confirmation"
            and e["asset"] == asset
            and e["outcome"] == "supported"
            for e in evidence.values()
        ):
            raise ValueError("ART25 confirmed scope requires bounded observation")
    for asset in scope["excluded"]:
        if not any(
            e["kind"] == "scope-exclusion"
            and e["asset"] == asset
            and e["outcome"] == "supported"
            for e in evidence.values()
        ):
            raise ValueError("ART25 excluded scope requires bounded exclusion evidence")
    if (
        not previous["owner"].strip()
        or not previous["reason"].strip()
        or previous["id"] == current["id"]
    ):
        raise ValueError("ART25 previous decision identity/owner/reason")
    if previous["status"] == "Closed":
        prior = previous["closure"]
        if not (
            prior is not None
            and prior["asset"] in scope["confirmed"]
            and prior["owner"].strip()
            and prior["residualRisk"].strip()
            and prior["riskOwner"].strip()
            and instant(prior["at"]) == before
            and instant(prior["dueAt"]) > before
            and receipt(
                previous["closureValidationId"],
                "recovery-validation",
                before,
                prior["asset"],
            )
        ):
            raise ValueError("ART25 supplied prior closure validation/residual risk")
    elif previous["closure"] is not None or previous["closureValidationId"] is not None:
        raise ValueError("ART25 closure fields owned by previous Closed status")
    gaps = []

    def require(condition, gap):
        if not condition:
            gaps.append(gap)

    require(
        bool(current["owner"].strip() and current["reason"].strip()),
        "decision-owner-or-reason",
    )
    target = current["requested"]
    declaration = data["declaration"]
    # A previous declared state is itself a supplied assumption, but still must
    # carry the same subject's explicit educational declaration record.
    if previous["status"] != "Suspected" or target != "Suspected":
        valid = False
        if declaration is not None:
            if declaration["asset"] not in scope["confirmed"]:
                raise ValueError("ART25 declaration confirmed scope binding")
            declared_at = instant(declaration["at"])
            valid = bool(
                declaration["owner"].strip() and declaration["reason"].strip()
            ) and end <= declared_at <= (
                at if previous["status"] == "Suspected" else before
            )
            valid = (
                receipt(
                    declaration["criteriaId"],
                    "declaration-criteria",
                    declared_at,
                    declaration["asset"],
                )
                and valid
            )
        if previous["status"] != "Suspected" and not valid:
            raise ValueError("ART25 previous declared state requires valid declaration")
        require(valid, "declaration-owner-reason-time-criteria")
    action = data["containment"]
    if action is not None:
        if action["optionId"] not in OPTIONS:
            raise ValueError("ART25 unknown containment option")
        if action["destructive"] or action["actualExecuted"]:
            raise ValueError("ART25 non-executable non-destructive illustration only")
        authority = action["authority"]
        if authority["realAuthority"]:
            raise ValueError("ART25 synthetic authority is not real authorization")
        action_at = instant(action["at"])
        approved_at = instant(authority["approvedAt"])
        if not before <= action_at <= at or not end <= approved_at <= action_at:
            raise ValueError("ART25 containment/approval chronology")
        if (
            authority["subject"] != context["subject"]
            or authority["revision"] != context["revision"]
            or authority["asset"] != action["asset"]
            or action["asset"] not in scope["confirmed"]
        ):
            raise ValueError("ART25 action authority scope binding")
    if target == "Contained":
        require(action is not None, "containment-record")
        if action is not None:
            authority = action["authority"]
            require(
                bool(authority["approved"] and authority["owner"].strip())
                and instant(authority["expiresAt"]) >= instant(action["at"]),
                "containment-authority",
            )
            require(
                bool(action["expectedImpact"].strip() and action["rollback"].strip()),
                "containment-impact-rollback",
            )
            preservation = data["preservation"]
            valid = False
            if preservation is not None:
                saved_at = instant(preservation["at"])
                valid = bool(
                    preservation["owner"].strip()
                ) and end <= saved_at <= instant(action["at"])
                valid = (
                    receipt(
                        preservation["evidenceId"],
                        "preservation",
                        saved_at,
                        action["asset"],
                    )
                    and valid
                )
            require(valid, "preservation-before-containment")
            require(
                action["optionId"] != "OPT-IR19-MONITOR"
                and receipt(
                    action["validationId"],
                    "containment-validation",
                    asset=action["asset"],
                )
                and instant(evidence[action["validationId"]]["availableAt"])
                >= instant(action["at"]),
                "containment-not-validated",
            )
    if target == "Investigating":
        require(
            receipt(data["analysisId"], "analysis"), "investigation-evidence-question"
        )
    if target in ("Recovering", "Closed"):
        recovery = data["recovery"]
        require(recovery is not None, "recovery-record")
        if recovery is not None:
            if recovery["asset"] not in scope["confirmed"]:
                raise ValueError("ART25 recovery confirmed scope binding")
            require(
                bool(recovery["owner"].strip())
                and receipt(
                    recovery["criteriaId"], "recovery-criteria", asset=recovery["asset"]
                ),
                "recovery-entry-criteria",
            )
            if target == "Closed":
                require(
                    receipt(
                        recovery["validationId"],
                        "recovery-validation",
                        asset=recovery["asset"],
                    )
                    and instant(evidence[recovery["validationId"]]["availableAt"])
                    > before,
                    "recovery-not-validated",
                )
        if target == "Closed":
            closure = data["closure"]
            require(closure is not None, "closure-record")
            if closure is not None:
                if recovery is not None and closure["asset"] != recovery["asset"]:
                    raise ValueError("ART25 closure recovery scope binding")
                require(
                    bool(
                        closure["owner"].strip()
                        and closure["residualRisk"].strip()
                        and closure["riskOwner"].strip()
                    )
                    and instant(closure["at"]) == at
                    and instant(closure["dueAt"]) > at,
                    "closure-validation-residual-risk",
                )
    if target == "Reopened":
        reopening = data["reopening"]
        require(reopening is not None, "reopen-record")
        if reopening is not None:
            new = reopening["newEvidenceId"]
            valid = receipt(new, "new-evidence")
            valid = valid and instant(evidence[new]["availableAt"]) > before
            require(
                valid
                and bool(reopening["owner"].strip() and reopening["reason"].strip())
                and reopening["closedDecisionId"] == previous["id"]
                and instant(reopening["at"]) == at,
                "reopen-new-evidence-owner-time-history",
            )
    return {
        "status": previous["status"] if gaps else target,
        "decision": "deferred" if gaps else "accepted",
        "gaps": gaps,
        "limit": LIMIT,
        "executionAuthorized": False,
        "notificationDecided": False,
        "noIncidentClaim": False,
        "improvementComplete": False,
    }
