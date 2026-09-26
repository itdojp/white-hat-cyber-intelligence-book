"""Layer A: finite supplied requirement/collection plan, not an intelligence engine.

No collection, renderer parsing, confidence inference or legal certification.
Independent contrasts exercise references, answer bindings, time and boundaries.
"""

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import PurePosixPath
import stat

from scripts.check_editorial_input_manifest import (
    _reject_constant,
    _reject_duplicate_keys,
    validate_schema_instance,
    validate_supported_schema_nodes,
)
from scripts.content_safety_policy import scan_action_text, scan_host_policy

VERSION = "1.0.0"
DATA = "cases/fixtures/ch23-intelligence-requirements.json"
SCHEMA = "schemas/ch23-intelligence-requirements.schema.json"
CONTRACT = "tests/fixtures/chapter23/publication-contract.json"
CORPUS = "tests/fixtures/chapter23/comparison-corpus.json"
DOCUMENTS = (
    "manuscript/23-intelligence-requirements.md",
    "templates/intelligence-requirement-collection-plan.md",
    "cases/ch23-intelligence-requirements-example.md",
    "references/ch23-source-review-2026-09-27.md",
)
SOURCES = ("SRC-ICD203-001", "SRC-ODNI-OSINT-001")
PARENTS = (
    "WRITING_GUIDE.md",
    "SOURCE_POLICY.md",
    "SAFETY_SCOPE.md",
    "CROSS_BOOK_MAP.md",
    "manuscript/04-assets-boundaries-threat-model.md",
    "manuscript/16-telemetry-evidence-readiness.md",
    "cases/fixtures/ch16-telemetry-coverage.json",
    "manuscript/19-incident-response.md",
    "cases/fixtures/ch19-incident-response.json",
    "manuscript/25-structured-analysis-attribution.md",
    "scripts/content_safety_policy.py",
    "CONTENT_SAFETY_POLICY.md",
    "scripts/publication_projection.py",
    "scripts/_publication_projection_renderer.rb",
    "scripts/publication_text.py",
    "Gemfile.lock",
    "package-lock.json",
    ".book-formatter/revision.json",
)
INDEX_PATHS = (
    "artifact-index.md",
    "figure-index.md",
    "glossary.md",
    "cases/index.md",
    "cases/fixtures/index.md",
    "README.md",
    "CHANGELOG.md",
    "CANONICAL_SOURCE.md",
)
INPUTS = (
    DATA,
    SCHEMA,
    CONTRACT,
    CORPUS,
    *DOCUMENTS,
    *PARENTS,
    *INDEX_PATHS,
    "package.json",
    "site-pages.json",
    "references/sources.json",
    "book-config.json",
)
STATUSES = (
    "Planned",
    "Collecting",
    "Satisfied",
    "Partially satisfied",
    "Blocked",
    "Cancelled",
)
CONFIDENCE = {"低": 0, "中": 1, "高": 2}


def require(condition, label):
    if not condition:
        raise ValueError("IR23: " + label)


def strict(raw):
    return json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=_reject_duplicate_keys,
        parse_constant=_reject_constant,
    )


def digest(value):
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode()
    ).hexdigest()


def instant(value):
    require(type(value) is str and len(value) == 20, "UTC format")
    result = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    require(
        2000 <= result.year <= 2099 and result.strftime("%Y-%m-%dT%H:%M:%SZ") == value,
        "canonical UTC",
    )
    return result


def read_regular(root, relative):
    """Fixed bounded input set; not a concurrent hostile-rename sandbox."""
    require(relative in INPUTS and not root.is_symlink(), "fixed input/root")
    root = root.resolve(strict=True)
    path = root
    for part in PurePosixPath(relative).parts:
        path /= part
        require(not path.is_symlink(), "symlink input/ancestor")
    require(path.resolve(strict=True).is_relative_to(root), "input containment")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        require(
            stat.S_ISREG(info.st_mode) and 0 < info.st_size <= 1024 * 1024,
            "bounded regular input",
        )
        raw = stream.read(1024 * 1024 + 1)
    require(len(raw) <= 1024 * 1024, "input size")
    return raw


def leaves(value, path=()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from leaves(child, (*path, key))
    elif isinstance(value, list) and value:
        for i, child in enumerate(value):
            yield from leaves(child, (*path, str(i)))
    else:
        yield path, value


def case_groups(data):
    for key, value in data.items():
        groups = (
            [(row["id"], row) for row in value]
            if isinstance(value, list)
            else [(key, value)]
        )
        for title, group in groups:
            yield (
                title,
                [
                    (
                        "/".join(path) or title,
                        v if isinstance(v, str) else json.dumps(v, ensure_ascii=False),
                    )
                    for path, v in leaves(group)
                ],
            )


def idset(values, label):
    require(
        type(values) is list and len(values) == len(set(values)), label + " unique refs"
    )
    return set(values)


def by_id(rows, label):
    ids = [row["id"] for row in rows]
    idset(ids, label)
    return dict(zip(ids, rows, strict=True))


def evaluate(data):
    """Semantic assertions independent of canonical snapshot and expected outcomes.

    Confidence is supplied, not inferred. Only this bounded educational plan is
    supported. Textual truth or actual authority cannot be established here.
    """
    record, decision, pipeline = data["record"], data["decision"], data["pipeline"]
    start, cutoff, due = map(
        instant, (decision["openedAt"], record["asOf"], decision["deadline"])
    )
    require(
        start <= cutoff < due and (due - start).total_seconds() == 48 * 3600,
        "48h decision/cutoff",
    )
    times = [
        instant(pipeline[k])
        for k in ("processingDeadline", "analysisDeadline", "distributionDeadline")
    ]
    require(cutoff <= times[0] <= times[1] <= times[2] <= due, "pipeline deadlines")
    require(pipeline["distributionAudience"] == decision["owner"], "decision audience")
    require(len(by_id(decision["options"], "options")) >= 2, "decision alternatives")
    require(data["feedback"]["owner"] == decision["owner"], "feedback owner")
    require(instant(data["feedback"]["reassessmentAt"]) == due, "reassessment deadline")
    rs, cs, ss, es, gs = (
        by_id(data[k], k)
        for k in ("requirements", "collections", "sources", "evidence", "gaps")
    )
    require(
        len(rs) == 5 and len(cs) == 8 and len(ss) == 3 and len(es) == 4,
        "bounded teaching inventory",
    )
    require(
        any(len(r["collectionIds"]) > 1 for r in rs.values())
        and any(len(c["requirementIds"]) > 1 for c in cs.values()),
        "many-to-many",
    )
    allcriteria = {v["id"] for r in rs.values() for v in r["criteria"]}
    require(
        len(allcriteria) == sum(len(r["criteria"]) for r in rs.values()),
        "global criterion identity",
    )
    deliverables = [x for c in cs.values() for x in c["deliverableIds"]]
    idset(deliverables, "global deliverable")
    for c in cs.values():
        refs = idset(c["requirementIds"], "collection requirements")
        require(refs and refs <= rs.keys(), "collection requirement refs")
        require(
            refs == {r["id"] for r in rs.values() if c["id"] in r["collectionIds"]},
            "reciprocal mapping",
        )
        require(cutoff <= instant(c["deadline"]) <= times[0], "collection deadline")
        unknown = (
            c["authority"] == "unknown"
            or c["terms"] == "unknown"
            or c["classification"] == "unknown"
        )
        require(not unknown or c["status"] == "Blocked", "unknown boundary blocked")
        require(
            (c["blocker"] is not None) == (c["status"] == "Blocked"),
            "collection blocker",
        )
        require(
            (c["cancellationReason"] is not None) == (c["status"] == "Cancelled"),
            "collection cancellation",
        )
        eids = idset(c["evidenceIds"], "collection evidence")
        require(eids <= es.keys(), "collection evidence refs")
        require(
            eids == {e["id"] for e in es.values() if e["collectionId"] == c["id"]},
            "evidence ownership",
        )
        fulfilled = [es[e]["deliverableId"] for e in c["evidenceIds"]]
        idset(fulfilled, "unique supplied deliverable")
        requested = idset(c["deliverableIds"], "collection deliverables")
        require(requested and set(fulfilled) <= requested, "supplied deliverable scope")
        if c["status"] == "Satisfied":
            require(
                set(fulfilled) == requested
                and all(ss[es[e]["sourceId"]]["quality"] == "reviewed" for e in eids),
                "collection satisfaction",
            )
        elif c["status"] == "Partially satisfied":
            require(0 < len(fulfilled) < len(requested), "collection partial")
        else:
            require(not fulfilled, "unfulfilled collection evidence")
    for e in es.values():
        require(e["collectionId"] in cs and e["sourceId"] in ss, "evidence parent")
        c, s = cs[e["collectionId"]], ss[e["sourceId"]]
        require(c["sourceClass"] == s["sourceClass"], "source class binding")
        require(
            e["subjectId"] == record["subjectId"]
            and e["revision"] == record["revision"],
            "subject/revision",
        )
        require(
            start
            <= instant(e["windowStart"])
            <= instant(e["windowEnd"])
            <= instant(e["availableAt"])
            <= cutoff,
            "evidence window/cutoff",
        )
        require(
            idset(e["criterionIds"], "evidence criteria")
            <= {v["id"] for rid in c["requirementIds"] for v in rs[rid]["criteria"]},
            "evidence criterion scope",
        )
        require(e["criterionIds"], "evidence criterion required")
    remaining = set()
    answer_counts = []
    for r in rs.values():
        require(r["decisionId"] == decision["id"], "requirement decision")
        require(cutoff <= instant(r["deadline"]) <= times[1], "requirement deadline")
        require(
            r["reassessmentId"] == data["feedback"]["reassessmentId"],
            "requirement reassessment",
        )
        refs = idset(r["collectionIds"], "requirement collection")
        require(refs and refs <= cs.keys(), "requirement collection refs")
        require(
            all(instant(cs[c]["deadline"]) <= instant(r["deadline"]) for c in refs),
            "requirement collection time",
        )
        criteria = by_id(r["criteria"], "criteria")
        answered = [b["criterionId"] for b in r["answerBindings"]]
        require(idset(answered, "answers") <= criteria.keys(), "answer criterion scope")
        for b in r["answerBindings"]:
            ids = idset(b["evidenceIds"], "answer evidence")
            require(ids and ids <= es.keys(), "answer evidence refs")
            require(
                CONFIDENCE[b["confidence"]] >= CONFIDENCE[r["minimumConfidence"]],
                "minimum confidence",
            )
            groups = []
            for eid in b["evidenceIds"]:
                e = es[eid]
                s = ss[e["sourceId"]]
                require(
                    e["collectionId"] in refs and b["criterionId"] in e["criterionIds"],
                    "answer evidence criterion",
                )
                require(s["quality"] == "reviewed", "answer source quality")
                groups.append(s["independentGroup"])
            require(len(groups) == len(set(groups)), "duplicated independent source")
        missing = set(criteria) - set(answered)
        gaps = idset(r["gapIds"], "requirement gaps")
        require(gaps <= gs.keys(), "gap refs")
        own = [gs[g] for g in r["gapIds"]]
        require(
            {g["criterionId"] for g in own} == missing and len(own) == len(missing),
            "exact missing criteria",
        )
        for g in own:
            require(
                g["requirementId"] == r["id"] and g["owner"] == r["owner"],
                "gap ownership",
            )
            require(
                instant(g["deadline"]) == instant(r["deadline"])
                and g["reassessmentId"] == r["reassessmentId"],
                "gap deadline/reassessment",
            )
            require(
                CONFIDENCE[r["judgmentConfidence"]] <= CONFIDENCE[g["confidenceLimit"]],
                "gap confidence limit",
            )
        remaining |= gaps
        require(
            (r["blocker"] is not None) == (r["status"] == "Blocked"),
            "requirement blocker",
        )
        require(
            (r["cancellationReason"] is not None) == (r["status"] == "Cancelled"),
            "requirement cancellation",
        )
        if r["priority"] == "P4 Not collect":
            require(r["status"] == "Cancelled", "not-collect requirement cancelled")
        if r["priority"] == "P3 Deferred":
            require(
                r["status"] in ("Planned", "Blocked", "Cancelled"),
                "deferred requirement inactive",
            )
        if r["status"] == "Satisfied":
            require(not missing and answered, "requirement satisfaction")
            require(
                CONFIDENCE[r["judgmentConfidence"]]
                >= CONFIDENCE[r["minimumConfidence"]],
                "satisfied judgment confidence",
            )
        elif r["status"] == "Partially satisfied":
            require(answered and missing, "requirement partial")
        else:
            require(not answered and missing, "unfulfilled requirement")
        answer_counts.append(len(answered))
    require(remaining == set(gs), "unowned gap")
    for fact in data["facts"]:
        require(
            fact["evidenceId"] in es
            and fact["text"] == es[fact["evidenceId"]]["observation"],
            "fact evidence binding",
        )
        require(
            ss[es[fact["evidenceId"]]["sourceId"]]["quality"] == "reviewed",
            "fact source quality",
        )
    require(len(by_id(data["facts"], "facts")) == 3, "fact inventory")
    by_id(data["assumptions"], "assumptions")
    hs = by_id(data["handoffs"], "handoffs")
    require(
        [h["targetChapter"] for h in hs.values()] == [24, 25, 26],
        "handoff targets/order",
    )
    expected = [list(ss), list(rs)[1:], [decision["id"]]]
    for h, refs in zip(hs.values(), expected, strict=True):
        require(
            h["refs"] == refs and instant(h["deadline"]) == times[2],
            "handoff content/deadline",
        )
    return {
        "answers": answer_counts,
        "gaps": len(gs),
        "collectionStatuses": [c["status"] for c in cs.values()],
    }


def validate_model(data, schema, contract=None):
    validate_supported_schema_nodes(schema, "schema", schema)
    validate_schema_instance(data, schema)
    errors = []
    for path, value in leaves(data):
        if isinstance(value, str):
            require(
                bool(value.strip()) and value == value.strip(),
                "nonblank unpadded field",
            )
            location = DATA + ":" + "/".join(path)
            errors += [
                f"{location}: {f.category}: {f.reason}"
                for f in (
                    *scan_action_text(value, location=location),
                    *scan_host_policy(value, location=location),
                )
            ]
    evaluate(data)
    if contract is not None and digest(data) != contract["dataSha256"]:
        errors.append("IR23: canonical supplied data snapshot")
    return errors
