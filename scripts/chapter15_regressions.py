"""Finite ART04/23 counterexamples, not a Markdown, operation or fuzz grammar."""

from __future__ import annotations
from copy import deepcopy
from dataclasses import replace
from itertools import product
import os
from pathlib import Path
import tempfile
from unittest.mock import patch
from scripts.chapter15_semantics import (
    DATA_PATH,
    INPUTS,
    DOCUMENTS,
    RESULTS,
    STATUSES,
    read_regular,
    strict_bytes,
    leaves,
    validate_model,
    retest_result,
    acceptance_valid as _acceptance_valid,
    finding_status as _finding_status,
)
from scripts.check_chapter15_contract import (
    ROOT,
    SOURCE_IDS,
    key,
    relations,
    scan_document,
    document_errors,
    case_parity_errors,
    repository_errors,
)
from scripts.publication_projection import project_documents, is_policy_scan_field


def run_regressions(data, schema, contract, source, projection):
    ids, errors = [], []

    def check(label, ok):
        if label in ids:
            errors.append("duplicate regression ID: " + label)
        ids.append(label)
        if not ok:
            errors.append("regression failed: " + label)

    def acceptance_valid(finding, as_of):
        return _acceptance_valid(finding, as_of, data["delegations"])

    def finding_status(finding, retest, as_of):
        return _finding_status(
            finding, retest, as_of, data["delegations"], data["temporaryReviews"]
        )

    def validate(d):
        return validate_model(d, schema, contract)

    def put(d, path, value):
        obj = d
        for part in path[:-1]:
            obj = obj[int(part) if isinstance(obj, list) else part]
        obj[int(path[-1]) if isinstance(obj, list) else path[-1]] = value

    def bad(label, path, value):
        d = deepcopy(data)
        put(d, path, value)
        check("CH15-" + label, bool(validate(d)))

    def rejects(fn):
        try:
            fn()
        except (ValueError, TypeError, KeyError):
            return True
        return False

    check("CH15-canonical", not validate(data))
    check(
        "CH15-six-statuses", set(f["status"] for f in data["findings"]) == set(STATUSES)
    )
    check(
        "CH15-five-results", set(r["result"] for r in data["retests"]) == set(RESULTS)
    )
    check(
        "CH15-eight-parent-states",
        len(data["context"]["labStates"]) == 8
        and "Running" in data["context"]["labStates"],
    )
    check(
        "CH15-schema-cannot-loosen",
        bool(validate_model(data, dict(schema, additionalProperties=True), contract)),
    )
    from scripts.check_editorial_input_manifest import validate_schema_instance

    check(
        "CH15-SCHEMA-canonical",
        not rejects(lambda: validate_schema_instance(data, schema)),
    )
    probes = [
        (("findings", "0", "status"), "Safe"),
        (("retests", "0", "result"), "Complete"),
        (("retests", "0", "method"), "Scanner completed"),
        (("retests", "0", "actualOperations"), 1),
        (("retests", "0", "stepsAfterStop"), 1),
        (("findings", "0", "acceptance", "overridesAssessmentAuthority"), True),
        (("findings", "0", "treatments", "0", "implemented"), True),
        (("findings", "0", "disclosure", "publicReleaseAuthorized"), True),
    ]
    # Every published boolean/integer boundary is typed and frozen by the
    # standalone Schema; no assumption that model-only checks protect downloads.
    for path, value in leaves(data):
        if type(value) in (bool, int):
            node = schema
            for part in path:
                node = node["items"] if part.isdigit() else node["properties"][part]
            mutated = not value if type(value) is bool else value + 1
            if mutated not in node.get("enum", []):
                probes.append((path, mutated))
            probes.append((path, "untyped-boundary"))
    for i, (path, value) in enumerate(probes):
        d = deepcopy(data)
        put(d, path, value)
        check(
            f"CH15-SCHEMA-boundary-{i}",
            rejects(lambda: validate_schema_instance(d, schema)),
        )
    for field in ("findingStatuses", "retestResults", "labStates"):
        d = deepcopy(data)
        d["context"][field].reverse()
        check(
            "CH15-SCHEMA-set-permutation-" + field,
            not rejects(lambda: validate_schema_instance(d, schema)),
        )
        for mutation in ("extra", "duplicate", "missing", "unknown"):
            d = deepcopy(data)
            a = d["context"][field]
            if mutation == "extra":
                a.append(a[0])
            elif mutation == "duplicate":
                a[-1] = a[0]
            elif mutation == "missing":
                a.pop()
            else:
                a[0] = "Unowned"
            check(
                "CH15-SCHEMA-set-" + field + "-" + mutation,
                rejects(lambda: validate_schema_instance(d, schema)),
            )
    for field in ("findings", "retests", "handoffs", "delegations", "temporaryReviews"):
        for mutation in ("extra", "duplicate", "missing"):
            d = deepcopy(data)
            a = d[field]
            if mutation == "extra":
                a.append(deepcopy(a[0]))
            elif mutation == "duplicate":
                if len(a) == 1:
                    a.append(deepcopy(a[0]))
                else:
                    a[-1] = deepcopy(a[0])
            else:
                a.pop()
            check(
                "CH15-SCHEMA-record-" + field + "-" + mutation,
                rejects(lambda: validate_schema_instance(d, schema)),
            )
    d = deepcopy(data)
    d["findings"][0]["unowned"] = "x"
    check(
        "CH15-SCHEMA-unknown-field",
        rejects(lambda: validate_schema_instance(d, schema)),
    )
    # Freeze every authored leaf independently of the derived outputs.
    # These are bounded mutations of the committed dataset, not a fuzz grammar.
    for i, (path, value) in enumerate(leaves(data)):
        if path[0] == "findings" and path[-1] == "status":
            continue
        if path[0] == "retests" and path[-1] == "result":
            continue
        new = (
            not value
            if type(value) is bool
            else value + 1
            if type(value) is int
            else "MUTATED"
            if value is None
            else value + " changed"
            if isinstance(value, str)
            else ["MUTATED"]
        )
        bad(f"LEAF-{i}", path, new)
    for i, f in enumerate(data["findings"]):
        for status in STATUSES:
            if status != f["status"]:
                bad(f"STATUS-{i}-{status}", ("findings", str(i), "status"), status)
    for i, r in enumerate(data["retests"]):
        for result in RESULTS:
            if result != r["result"]:
                bad(f"RESULT-{i}-{result}", ("retests", str(i), "result"), result)
    # Independent truth table for the two-criterion kernel; no expected-output
    # fields or fixture freeze consulted by retest_result().
    for first, second, stop, method in product(
        (True, False, None),
        (True, False, None),
        (False, True),
        ("Static authored comparison", "Scanner summary only"),
    ):
        r = deepcopy(data["retests"][0])
        r["stopTrigger"] = "Unexpected-input-symbol" if stop else "None"
        r["method"] = method
        for i, outcome in enumerate((first, second)):
            o = r["observations"][i]
            o["present"] = outcome is not None
            o["value"] = (
                None
                if outcome is None
                else r["criteria"][i]["expected"]
                if outcome
                else "different"
            )
            o["basis"] = (
                "missing-not-failed" if outcome is None else "authored-supplied-value"
            )
        expected = (
            "Stopped"
            if stop
            else "Inconclusive"
            if method == "Scanner summary only" or first is None or second is None
            else "Failed"
            if not first
            else "Passed"
            if second
            else "Partial"
        )
        check(
            f"CH15-KERNEL-{first}-{second}-{stop}-{method}",
            retest_result(r) == expected,
        )
    for field, value in [
        ("subjectId", "other"),
        ("revision", "other"),
        ("criterionId", "other"),
        ("present", 1),
        ("value", True),
        ("basis", "measured"),
    ]:
        r = deepcopy(data["retests"][0])
        r["observations"][0][field] = value
        check("CH15-KERNEL-binding-" + field, rejects(lambda: retest_result(r)))
    for field, value in [
        ("method", "execute"),
        ("requiredMethod", "Scanner summary only"),
        ("stopTrigger", "Continue"),
        ("stepsAfterStop", True),
        ("actualOperations", 1),
        ("criteria", []),
        ("observations", []),
    ]:
        r = deepcopy(data["retests"][0])
        r[field] = value
        check("CH15-KERNEL-invalid-" + field, rejects(lambda: retest_result(r)))
    r = deepcopy(data["retests"][0])
    r["criteria"][1]["id"] = r["criteria"][0]["id"]
    check("CH15-KERNEL-duplicate-criteria", rejects(lambda: retest_result(r)))
    for field, value in [("value", "invented"), ("basis", "authored-supplied-value")]:
        r = deepcopy(data["retests"][2])
        r["observations"][0][field] = value
        check("CH15-KERNEL-missing-" + field, rejects(lambda: retest_result(r)))
    # Acceptance fields, chronology, binding and expiry are evaluated separately
    # from the frozen fixture to prove actual decision guards.
    f = deepcopy(data["findings"][2])
    now = data["record"]["asOf"]
    check("CH15-ACCEPT-valid", acceptance_valid(f, now))
    for field in f["acceptance"]:
        if field in ("present", "overridesAssessmentAuthority"):
            continue
        m = deepcopy(f)
        m["acceptance"][field] = ""
        check(
            "CH15-ACCEPT-required-" + field, rejects(lambda: acceptance_valid(m, now))
        )
    for field in (
        "findingId",
        "subjectId",
        "scope",
        "authorityHolder",
        "basis",
        "residualRiskId",
        "reassessmentId",
    ):
        m = deepcopy(f)
        m["acceptance"][field] = "different"
        check("CH15-ACCEPT-binding-" + field, rejects(lambda: acceptance_valid(m, now)))
    for label, field, value in [
        ("at-expiry", "expiresAt", now),
        ("expired", "expiresAt", "2026-09-16T22:59:59Z"),
    ]:
        m = deepcopy(f)
        m["acceptance"][field] = value
        check("CH15-ACCEPT-" + label, not acceptance_valid(m, now))
        check(
            "CH15-ACCEPT-no-close-" + label,
            rejects(lambda: finding_status(m, None, now)),
        )
    for field, value in [
        ("decidedAt", "2027-01-01T00:00:00Z"),
        ("expiresAt", "2020-01-01T00:00:00Z"),
        ("decidedAt", "2026-9-16T00:00:00Z"),
        ("overridesAssessmentAuthority", True),
    ]:
        m = deepcopy(f)
        m["acceptance"][field] = value
        check(
            "CH15-ACCEPT-invalid-" + field + "-" + str(value),
            rejects(lambda: acceptance_valid(m, now)),
        )
    lookup = {r["id"]: r for r in data["retests"]}
    for i, f in enumerate(data["findings"]):
        r = lookup.get(f["retestId"])
        check(f"CH15-DECISION-canonical-{i}", finding_status(f, r, now) == f["status"])
        if r:
            for field in (
                "id",
                "findingId",
                "subjectId",
                "beforeRevision",
                "residualRiskId",
                "reassessmentId",
            ):
                m = deepcopy(r)
                m[field] = "different"
                check(
                    f"CH15-DECISION-binding-{i}-{field}",
                    rejects(lambda: finding_status(f, m, now)),
                )
        if i not in (2, 4, 6):
            m = deepcopy(f)
            m["requestedStage"] = "Close"
            m["decision"]["basis"] = "retest"
            check(
                f"CH15-DECISION-insufficient-{i}",
                rejects(lambda: finding_status(m, r, now)),
            )
    m = deepcopy(data["findings"][1])
    m["temporaryReviewEvidenceId"] = None
    check(
        "CH15-DECISION-mitigated-evidence",
        rejects(lambda: finding_status(m, lookup[m["retestId"]], now)),
    )
    m = deepcopy(data["findings"][5])
    m["reassessment"]["reopenReason"] = ""
    check(
        "CH15-DECISION-reopen-reason",
        rejects(lambda: finding_status(m, lookup[m["retestId"]], now)),
    )

    # Three independent-review P1 counterexamples, evaluated without fixture
    # freeze: resolve actual supplied owners, not just syntactically valid IDs.
    accepted = deepcopy(data["findings"][2])
    revised = deepcopy(accepted)
    revised["subjectRevision"] = "UNACCEPTED-REVISION"
    check(
        "CH15-R142-P1-REVISION",
        rejects(lambda: _acceptance_valid(revised, now, data["delegations"])),
    )
    revised = deepcopy(accepted)
    revised["acceptance"]["subjectRevision"] = "OTHER"
    check(
        "CH15-R142-P1-REVISION-acceptance",
        rejects(lambda: _acceptance_valid(revised, now, data["delegations"])),
    )
    grants = deepcopy(data["delegations"])
    grants[0]["subjectRevision"] = "OTHER"
    check(
        "CH15-R142-P1-REVISION-delegation",
        rejects(lambda: _acceptance_valid(accepted, now, grants)),
    )
    undeclared = deepcopy(accepted)
    undeclared["acceptance"]["authorityReference"] = "UNDEFINED-DELEGATION"
    check(
        "CH15-R142-P1-DELEGATION",
        rejects(lambda: _acceptance_valid(undeclared, now, data["delegations"])),
    )
    for name, grants in [
        ("missing", []),
        ("duplicate", data["delegations"] + [deepcopy(data["delegations"][0])]),
        ("foreign", data["delegations"][1:]),
    ]:
        check(
            "CH15-R142-DELEGATION-" + name,
            rejects(lambda: _acceptance_valid(accepted, now, grants)),
        )
    for field, value in [
        ("findingId", "other"),
        ("scenarioId", "other"),
        ("subjectId", "other"),
        ("subjectRevision", "other"),
        ("scope", "other"),
        ("holder", "other"),
        ("role", "Assessment operator"),
        ("authorityKind", "Assessment execution"),
        ("basis", "real-approval"),
        ("assessmentAuthorizationGranted", True),
        ("realDelegationIssued", True),
        ("limitation", ""),
        ("validFrom", "2026-09-14T00:00:01Z"),
        ("validUntil", "2026-09-29T23:59:59Z"),
        ("validUntil", "2026-09-13T00:00:00Z"),
    ]:
        grants = deepcopy(data["delegations"])
        grants[0][field] = value
        check(
            "CH15-R142-DELEGATION-field-" + field + "-" + str(value),
            rejects(lambda: _acceptance_valid(accepted, now, grants)),
        )
    # Authority-end equality closes validity; acceptance may not outlive grant.
    check(
        "CH15-R142-DELEGATION-end-exclusive",
        not _acceptance_valid(accepted, "2026-09-30T00:00:00Z", data["delegations"]),
    )
    changed = deepcopy(accepted)
    changed["acceptance"]["authorityHolder"] = changed["acceptance"][
        "decisionOwner"
    ] = "SELF-DECLARED"
    check(
        "CH15-R142-DELEGATION-joint-self-claim",
        rejects(lambda: _acceptance_valid(changed, now, data["delegations"])),
    )
    mitigated = deepcopy(data["findings"][1])
    rt = lookup[mitigated["retestId"]]
    undeclared = deepcopy(mitigated)
    undeclared["temporaryReviewEvidenceId"] = "UNDEFINED-TEMP-REVIEW"
    check(
        "CH15-R142-P1-TEMPORARY",
        rejects(
            lambda: _finding_status(
                undeclared, rt, now, data["delegations"], data["temporaryReviews"]
            )
        ),
    )
    for name, reviews in [("missing", []), ("duplicate", data["temporaryReviews"] * 2)]:
        check(
            "CH15-R142-TEMPORARY-" + name,
            rejects(
                lambda: _finding_status(
                    mitigated, rt, now, data["delegations"], reviews
                )
            ),
        )
    for field, value in [
        ("findingId", "other"),
        ("scenarioId", "other"),
        ("subjectId", "other"),
        ("subjectRevision", "other"),
        ("treatmentId", mitigated["treatments"][1]["id"]),
        ("treatmentId", "missing"),
        ("controlId", "other"),
        ("scope", "other"),
        ("basis", "measured"),
        ("requiredPlanScope", "other"),
        ("reviewedPlanScope", "other"),
        ("conclusion", "Mitigation applied"),
        ("reviewer", ""),
        ("question", ""),
        ("limitation", ""),
        ("recordedAt", "2026-09-16T23:00:01Z"),
        ("actualOperations", True),
        ("actualOperations", 1),
        ("realMitigationEffectMeasured", True),
    ]:
        reviews = deepcopy(data["temporaryReviews"])
        reviews[0][field] = value
        check(
            "CH15-R142-TEMPORARY-field-" + field + "-" + str(value),
            rejects(
                lambda: _finding_status(
                    mitigated, rt, now, data["delegations"], reviews
                )
            ),
        )
    for name, change in [
        ("duplicate-treatment", deepcopy(mitigated)),
        ("actual-implementation", deepcopy(mitigated)),
    ]:
        if name == "duplicate-treatment":
            change["treatments"].append(deepcopy(change["treatments"][0]))
        else:
            change["treatments"][0]["implemented"] = True
        check(
            "CH15-R142-TEMPORARY-" + name,
            rejects(
                lambda: _finding_status(
                    change, rt, now, data["delegations"], data["temporaryReviews"]
                )
            ),
        )

    # Exact typed field/cardinality/location provenance. No source syntax parsing.
    for di, doc in enumerate(projection.documents):
        spec = contract["documents"][doc.document_id]
        pairs = list(relations(doc))
        check(f"CH15-SURFACE-canonical-{di}", not document_errors(doc, spec, data))
        for family in ("analyticProvenance", "hostProvenance"):
            for ei, relation in enumerate(spec[family]):
                indices = [i for i, (_, r) in enumerate(pairs) if r == relation]
                check(f"CH15-EX-owned-{di}-{family}-{ei}", len(indices) == 1)
                if len(indices) != 1:
                    continue
                index = indices[0]
                f = doc.fields[index]
                text = f.text + " 実Credentialを再利用する。"
                changed = replace(f, text=text, normalized_text=text)
                probes = {
                    "changed": doc.fields[:index]
                    + (changed,)
                    + doc.fields[index + 1 :],
                    "moved": (f,) + doc.fields[:index] + doc.fields[index + 1 :],
                    "duplicate": doc.fields[:index] + (f,) + doc.fields[index:],
                    "missing": doc.fields[:index] + doc.fields[index + 1 :],
                }
                for name, fields in probes.items():
                    check(
                        f"CH15-EX-{di}-{family}-{ei}-{name}",
                        bool(scan_document(replace(doc, fields=fields), spec, True)),
                    )
                check(
                    f"CH15-EX-DIAG-{di}-{family}-{ei}",
                    any(
                        "expected 1, observed 0" in e and key(relation) in e
                        for e in scan_document(
                            replace(doc, fields=probes["missing"]), spec, True
                        )
                    ),
                )
        for ri, required in enumerate(spec["required"]):
            indices = [
                i for i, (_, relation) in enumerate(pairs) if relation == required
            ]
            check(f"CH15-REQUIRED-owned-{di}-{ri}", len(indices) == 1)
            if len(indices) == 1:
                i = indices[0]
                missing = replace(doc, fields=doc.fields[:i] + doc.fields[i + 1 :])
                check(
                    f"CH15-REQUIRED-missing-{di}-{ri}",
                    bool(document_errors(missing, spec, data)),
                )
        old = source[doc.document_id]
        for where, pos in [
            ("preamble", 0),
            ("body", old.index("\n## ")),
            ("tail", len(old)),
        ]:
            probe = project_documents(
                {
                    doc.document_id: (
                        old[:pos] + "\n\n実Credentialを再利用する。\n\n" + old[pos:]
                    ).rstrip()
                    + "\n"
                }
            ).documents[0]
            check(f"CH15-SURFACE-{di}-{where}", bool(scan_document(probe, spec)))
        probe = project_documents(
            {doc.document_id: old + "\n実Credentialを再利用しない。\n"}
        ).documents[0]
        check(f"CH15-SURFACE-safe-{di}", not scan_document(probe, spec, True))
        probe = project_documents(
            {doc.document_id: old + "\n## Unexpected section\n\n説明。\n"}
        ).documents[0]
        check(f"CH15-SURFACE-inventory-{di}", bool(document_errors(probe, spec, data)))
    unsupported = project_documents(
        {DOCUMENTS[0]: source[DOCUMENTS[0]] + "\n{% include unknown.html %}\n"}
    ).documents[0]
    check(
        "CH15-shared-unsupported",
        any(d.code == "PP1001" for d in unsupported.diagnostics),
    )
    chapter = projection.documents[0]
    spec = contract["documents"][DOCUMENTS[0]]
    for si, sid in enumerate(SOURCE_IDS):
        for scope in ["body", "references"]:
            fields = []
            for f, r in relations(chapter):
                if ("参考文献・Source Note ID" in r["headings"]) == (
                    scope == "references"
                ):
                    f = replace(
                        f,
                        text=f.text.replace(sid, sid + "x"),
                        normalized_text=f.normalized_text.replace(sid, sid + "x"),
                    )
                fields.append(f)
            check(
                f"CH15-SOURCE-{si}-{scope}",
                "Chapter15 body/reference Source ownership"
                in document_errors(replace(chapter, fields=tuple(fields)), spec, data),
            )
    positions = []
    for relation in spec["exerciseInstructionOrder"]:
        positions += [i for i, (_, r) in enumerate(relations(chapter)) if r == relation]
    check(
        "CH15-ORDER-five-blocks", len(positions) == 5 and positions == sorted(positions)
    )
    for i in positions[:-1]:
        fields = list(chapter.fields)
        cmd = fields.pop(positions[-1])
        fields.insert(i, cmd)
        check(
            "CH15-ORDER-premature-" + str(i),
            "Chapter15 exercise explanations before command"
            in document_errors(replace(chapter, fields=tuple(fields)), spec, data),
        )
    case = projection.documents[2]
    for i, f in enumerate(case.fields):
        if is_policy_scan_field(f) and f.element_kind == "table_row":
            changed = replace(
                f,
                text=f.text + " mismatched",
                normalized_text=f.normalized_text + " mismatched",
            )
            check(
                "CH15-CASE-leaf-" + str(i),
                bool(
                    case_parity_errors(
                        replace(
                            case,
                            fields=case.fields[:i] + (changed,) + case.fields[i + 1 :],
                        ),
                        data,
                    )
                ),
            )
    check("CH15-repository", not repository_errors(contract))

    badcontract = deepcopy(contract)
    badcontract["indices"]["CHANGELOG.md"] = ["unrecorded-reader-impact"]
    check(
        "CH15-reader-impact",
        any("index CHANGELOG.md" in e for e in repository_errors(badcontract)),
    )
    for raw in [b'{"x":1,"x":2}', b'{"x":NaN}', b"\xff"]:
        try:
            strict_bytes(raw)
        except (ValueError, UnicodeError):
            ok = True
        else:
            ok = False
        check("CH15-JSON-" + raw.hex(), ok)
    # Input guard probes have workspace-local scratch ownership and no network.
    work = ROOT / ".work"
    work.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ch15-input-", dir=work) as temp:
        root = Path(temp)
        p = root / DATA_PATH
        p.parent.mkdir(parents=True)
        p.write_bytes(b"{}")
        check("CH15-IO-regular", read_regular(root, DATA_PATH) == b"{}")
        for name in ["O_NOFOLLOW", "O_NONBLOCK"]:
            with patch.object(os, name, None):
                try:
                    read_regular(root, DATA_PATH)
                except ValueError:
                    ok = True
                else:
                    ok = False
            check("CH15-IO-" + name, ok)
        for n, rel in enumerate(INPUTS):
            q = root / rel
            q.parent.mkdir(parents=True, exist_ok=True)
            if q.exists():
                q.unlink()
            q.symlink_to(root / "absent")
            try:
                read_regular(root, rel)
            except (OSError, ValueError):
                ok = True
            else:
                ok = False
            check("CH15-IO-symlink-" + str(n), ok)
            q.unlink()
        for name, content in [("empty", b""), ("oversize", b"x" * (1024 * 1024 + 1))]:
            p.write_bytes(content)
            try:
                read_regular(root, DATA_PATH)
            except ValueError:
                ok = True
            else:
                ok = False
            check("CH15-IO-" + name, ok)
        p.unlink()
        os.mkfifo(p)
        try:
            read_regular(root, DATA_PATH)
        except ValueError:
            ok = True
        else:
            ok = False
        check("CH15-IO-fifo", ok)
        p.unlink()
        try:
            read_regular(root, "unregistered.json")
        except ValueError:
            ok = True
        else:
            ok = False
        check("CH15-IO-unknown", ok)
    return len(ids), errors
