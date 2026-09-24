"""Finite supplied DFIR records, not a forensic acquisition/causal inference tool.

Only Chapter20 semantics live here. There is no Markdown, renderer, URL or
Policy grammar. All clocks/records are educational assumptions, not attested
observations. A digest compares representations; it cannot authenticate them.
"""

from datetime import datetime, timedelta, timezone
import hashlib
import json

VERSION = "1.0.0"
RELATIONS = ("Before", "After", "Concurrent", "Possibly related", "Contradicted")
UTC = timezone.utc


def require(condition, code):
    if not condition:
        raise ValueError("DFIR20 " + code)


def instant(value):
    """Seconds with explicit Z or numeric offset; unknown -00:00 is not UTC."""
    require(isinstance(value, str), "timestamp type")
    zulu = len(value) == 20 and value.endswith("Z")
    numeric = len(value) == 25 and value[19] in "+-" and value[22] == ":"
    require(zulu or numeric, "timestamp timezone/precision")
    require(not value.endswith("-00:00"), "unknown offset")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("DFIR20 timestamp calendar") from exc
    require(2000 <= parsed.year <= 2099, "timestamp supported years")
    canonical = parsed.isoformat(timespec="seconds")
    require(
        canonical == (value[:-1] + "+00:00" if zulu else value),
        "timestamp canonical representation",
    )
    require(abs(parsed.utcoffset()) <= timedelta(hours=14), "timestamp offset range")
    return parsed.astimezone(UTC)


def utc_text(value):
    return value.astimezone(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def digest(value):
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()


def unique(rows, key):
    result = {}
    for row in rows:
        require(row[key] not in result, "duplicate " + key)
        result[row[key]] = row
    return result


def interval(row, clocks):
    payload = row["payload"]
    require(payload["clockId"] in clocks, "unknown clock")
    clock = clocks[payload["clockId"]]
    require(clock["sourceId"] == row["sourceId"], "clock/source binding")
    for k in ("offsetSeconds", "uncertaintySeconds"):
        require(type(clock[k]) is int, "integer " + k)
    require(-3600 <= clock["offsetSeconds"] <= 3600, "offset bounds")
    require(1 <= clock["uncertaintySeconds"] <= 3600, "uncertainty includes precision")
    # Positive offset means a fast clock. Uncertainty is a total bound including
    # quantization/drift, NOT a confidence percentage or a standard deviation.
    middle = instant(payload["originalTime"]) - timedelta(
        seconds=clock["offsetSeconds"]
    )
    radius = timedelta(seconds=clock["uncertaintySeconds"])
    low, high = middle - radius, middle + radius
    require(
        instant(clock["validFrom"]) <= low <= high <= instant(clock["validUntil"]),
        "clock validity window",
    )
    return low, high


def temporal_relation(left, right):
    """Closed intervals. Touching/overlapping bounds do not prove concurrency."""
    if left[1] < right[0]:
        return "Before"
    if left[0] > right[1]:
        return "After"
    return "Possibly related"


def prepare(data):
    """Validate ALL receipts before cutoff selection, including late evidence."""
    context = data["context"]
    clocks = unique(data["clocks"], "id")
    rows = unique(data["evidence"], "id")
    groups = {}
    for row in rows.values():
        p = row["payload"]
        require(
            p["subjectId"] == context["subjectId"]
            and p["revision"] == context["revision"],
            "evidence subject/revision",
        )
        require(p["assetId"] in context["assets"], "evidence asset scope")
        require(
            p["actorId"] in context["actors"] and p["sessionId"] in context["sessions"],
            "evidence actor/session registry",
        )
        require(row["payloadSha256"] == digest(p), "payload representation digest")
        low, high = interval(row, clocks)
        collected, ingested, available = (
            instant(row[k]) for k in ("collectedAt", "ingestedAt", "availableAt")
        )
        require(
            low
            <= collected
            <= ingested
            <= available
            <= instant(data["record"]["asOf"]),
            "receipt chronology/asOf",
        )
        require(
            instant(clocks[p["clockId"]]["availableAt"]) <= available,
            "clock not available with receipt",
        )
        require(
            instant(context["windowStart"])
            <= low
            <= high
            <= instant(context["windowEnd"]),
            "event window",
        )
        if p["operation"] == "change-scope":
            detail = p["detail"]
            require(
                bool(detail["approvedAssets"])
                and len(detail["approvedAssets"]) == len(set(detail["approvedAssets"])),
                "change scope nonempty/unique",
            )
            require(
                set(detail["approvedAssets"]) <= set(context["assets"]),
                "change scope registry",
            )
            require(
                instant(detail["windowStart"]) < instant(detail["windowEnd"]),
                "change window",
            )
        key = (row["sourceId"], row["eventId"])
        if key in groups:
            require(groups[key][0]["payload"] == p, "conflicting source/event identity")
        groups.setdefault(key, []).append(row)
    # Every receipt is retained; canonical representative is chosen only among
    # evidence available at the snapshot, not from the future full-bundle list.
    return clocks, rows, groups


def evaluate_claim(claim, rows, eligible, clocks):
    refs = claim["evidenceIds"]
    require(
        len(refs) == len(set(refs)) and all(r in rows for r in refs), "claim reference"
    )
    kind = claim["kind"]
    require(kind in ("order", "change-covers", "causal-link"), "claim kind")
    require(len(refs) == 2, "claim arity")
    left, right = (rows[r] for r in refs)
    a, b = left["payload"], right["payload"]
    if kind == "order":
        require(
            claim["assertedRelation"] in ("Before", "After", "Concurrent"),
            "order assertion",
        )
        require(claim["changeId"] is None, "non-change identity")
    elif kind == "change-covers":
        require(
            a["operation"] == "change-scope" and b["operation"] == "api-read",
            "change claim roles",
        )
        require(claim["assertedRelation"] is None, "non-order relation")
        require(a["detail"]["changeId"] == claim["changeId"], "change identity")
    else:
        require(
            a["operation"] == "consent-change" and b["operation"] == "api-read",
            "causal claim roles",
        )
        require(a["assetId"] == b["assetId"], "causal scope binding")
        require(claim["assertedRelation"] is None, "non-order relation")
        require(claim["changeId"] is None, "non-change identity")
    missing = [r for r in refs if r not in eligible]
    if missing:
        return {
            "status": "undetermined",
            "relation": None,
            "gaps": ["not-available:" + r for r in missing],
        }
    if kind == "order":
        relation = temporal_relation(interval(left, clocks), interval(right, clocks))
        if claim["assertedRelation"] == "Concurrent":
            # No simultaneity witness is supplied in this frozen teaching corpus.
            # Do not manufacture one from equal strings or overlapping intervals.
            if relation == "Possibly related":
                return {
                    "status": "undetermined",
                    "relation": relation,
                    "gaps": ["independent-simultaneity-evidence"],
                }
            return {"status": "contradicted", "relation": relation, "gaps": []}
        if relation == "Possibly related":
            return {
                "status": "undetermined",
                "relation": relation,
                "gaps": ["clock-order-uncertain"],
            }
        return {
            "status": "supported"
            if relation == claim["assertedRelation"]
            else "contradicted",
            "relation": relation,
            "gaps": [],
        }
    if kind == "change-covers":
        detail = a["detail"]
        # Only the named change's asset/window component, NOT action authority,
        # method approval, any other authority or an actor's purpose is tested.
        require(detail["changeId"] == claim["changeId"], "change identity")
        low, high = interval(right, clocks)
        start, end = instant(detail["windowStart"]), instant(detail["windowEnd"])
        if b["assetId"] not in detail["approvedAssets"] or high < start or low > end:
            return {"status": "contradicted", "relation": None, "gaps": []}
        if start <= low <= high <= end:
            return {"status": "supported", "relation": None, "gaps": []}
        return {
            "status": "undetermined",
            "relation": None,
            "gaps": ["change-window-uncertain"],
        }
    # A pair of records does not demonstrate the mechanism, necessity or cause.
    # This API deliberately has no route to a supported causal conclusion.
    return {
        "status": "undetermined",
        "relation": None,
        "gaps": ["mechanism-not-supplied", "alternative-not-eliminated"],
    }


def evaluate(data, snapshot):
    clocks, rows, groups = prepare(data)
    cutoff, analysis = instant(snapshot["cutoff"]), instant(snapshot["analysisAt"])
    require(
        cutoff <= analysis <= instant(data["record"]["asOf"]), "snapshot chronology"
    )
    eligible = {
        rid for rid, row in rows.items() if instant(row["availableAt"]) <= cutoff
    }
    require(
        all(
            instant(clocks[rows[r]["payload"]["clockId"]]["availableAt"]) <= cutoff
            for r in eligible
        ),
        "future calibration",
    )
    timeline = []
    for key in sorted(groups):
        receipts = sorted(
            (r for r in groups[key] if r["id"] in eligible), key=lambda r: r["id"]
        )
        if not receipts:
            continue
        representative = receipts[0]
        low, high = interval(representative, clocks)
        timeline.append(
            {
                "sourceId": key[0],
                "eventId": key[1],
                "evidenceIds": [r["id"] for r in receipts],
                "intervalStart": utc_text(low),
                "intervalEnd": utc_text(high),
            }
        )
    claims = unique(data["claims"], "id")
    return {
        "included": sorted(eligible),
        "excluded": sorted(set(rows) - eligible),
        "timeline": timeline,
        "claims": {
            key: evaluate_claim(claims[key], rows, eligible, clocks)
            for key in sorted(claims)
        },
    }
