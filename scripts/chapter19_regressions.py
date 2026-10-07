"""Finite ART25 semantic/selection tests; generic syntax remains shared-owned."""

from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import tempfile

from scripts.chapter19_decisions import STATES, VERSION, evaluate
from scripts.chapter19_model import (
    DATA,
    CORPUS,
    DOCUMENTS,
    strict,
    read_regular,
    digest,
    validate_model,
)
from scripts.check_chapter19_contract import (
    ROOT,
    document_errors,
    inventory,
    scan_document,
    parent_errors,
)
from scripts.check_editorial_input_manifest import (
    ManifestError,
    validate_schema_instance,
)
from scripts.publication_projection import project_documents, is_policy_scan_field


def at(value, path):
    for key in path:
        value = value[key]
    return value


def objects(value, path=()):
    if isinstance(value, dict):
        yield path, value
        for key, item in value.items():
            yield from objects(item, path + (key,))
    elif isinstance(value, list):
        for key, item in enumerate(value):
            yield from objects(item, path + (key,))


def run_regressions(data, schema, contract, source, projection):
    checks, errors = [], []

    def check(name, ok):
        if name in checks:
            errors.append("duplicate ART25 regression: " + name)
        checks.append(name)
        if not ok:
            errors.append("failed ART25 regression: " + name)

    def rejected(fn):
        try:
            result = fn()
            return isinstance(result, list) and bool(result)
        except (ValueError, ManifestError, KeyError, TypeError, StopIteration, OSError):
            return True

    check("harness-object-not-error", not rejected(lambda: {"accepted": True}))
    check("harness-bytes-not-error", not rejected(lambda: b"ok"))
    corpus = strict(read_regular(ROOT, CORPUS))
    cases = corpus["cases"]
    check(
        "corpus-inventory",
        corpus["caseCount"] == len(cases) == 60
        and [c["id"] for c in cases] == [f"ICHECK19-{i:03}" for i in range(1, 61)],
    )
    check("corpus-version", corpus["decisionVersion"] == VERSION)
    inputs = {r["id"]: r["input"] for r in data["contrasts"]}
    check("corpus-ownership", set(inputs) == {c["baseCaseId"] for c in cases})
    check(
        "corpus-seven-states",
        set(STATES) <= {c["expected"].get("status") for c in cases},
    )
    input_schema = schema["properties"]["contrasts"]["items"]["properties"]["input"]
    for case in cases:
        value = deepcopy(inputs[case["baseCaseId"]])
        for patch in case["patches"]:
            at(value, patch["path"][:-1])[patch["path"][-1]] = deepcopy(patch["value"])
        original = deepcopy(value)
        expected = case["expected"]
        try:
            validate_schema_instance(value, input_schema)
            output = evaluate(value)
            check(
                case["id"],
                "errorContains" not in expected
                and all(output[k] == v for k, v in expected.items()),
            )
            check(
                case["id"] + "-decision",
                output["decision"] == ("deferred" if output["gaps"] else "accepted"),
            )
            check(
                case["id"] + "-unique-gaps",
                len(output["gaps"]) == len(set(output["gaps"])),
            )
            changed = deepcopy(value)
            changed["evidence"].reverse()
            for items in changed["scope"].values():
                items.reverse()
            check(case["id"] + "-evidence-order", evaluate(changed) == output)
            check(
                case["id"] + "-key-order",
                evaluate(dict(reversed(list(value.items())))) == output,
            )
        except (ValueError, ManifestError) as exc:
            check(
                case["id"],
                "errorContains" in expected and expected["errorContains"] in str(exc),
            )
        check(case["id"] + "-pure", value == original)
    # PR153 review: explicit independent field inventory; refreshing authored
    # snapshots cannot bypass role ownership, closure ownership or due times.
    owner_paths = [(("notification", "escalationOwner"), "legalPrivacyReviewer")]
    for i, row in enumerate(data["contrasts"]):
        for path, role in (
            (("previous", "owner"), "decisionOwner"),
            (("decision", "owner"), "decisionOwner"),
            (("declaration", "owner"), "decisionOwner"),
            (("preservation", "owner"), "evidenceLead"),
            (("containment", "authority", "owner"), "incidentCommander"),
            (("recovery", "owner"), "recoveryOwner"),
            (("closure", "owner"), "decisionOwner"),
            (("previous", "closure", "owner"), "decisionOwner"),
            (("reopening", "owner"), "decisionOwner"),
        ):
            try:
                at(row["input"], path)
            except TypeError:  # Absent optional object, not an owner assignment.
                continue
            owner_paths.append((("contrasts", i, "input", *path), role))
        for j in range(3):
            owner_paths.append(
                (("contrasts", i, "handoffs", j, "owner"), "incidentCommander")
            )
    check("review-role-field-inventory", len(owner_paths) == 91)

    def refreshed_model(changed):
        refreshed = deepcopy(contract)
        refreshed["authoredInputs"] = {k: digest(v) for k, v in changed.items()}
        return validate_model(changed, schema, refreshed)

    for path, role in owner_paths:
        changed = deepcopy(data)
        at(changed, path[:-1])[path[-1]] = "SYNTH-UNASSIGNED"
        check(
            "review-role-owner-" + str(path),
            any("ART25 role-owner binding:" in e for e in refreshed_model(changed)),
        )
    # A coherent edited registry is allowed; these are references, not hidden
    # hard-coded identities. Blank or mismatched assignment is not coherent.
    for role in sorted({role for _, role in owner_paths}):
        changed = deepcopy(data)
        changed["roles"][role] = "SYNTH-REASSIGNED"
        check(
            "review-role-registry-only-" + role,
            any("ART25 role-owner binding:" in e for e in refreshed_model(changed)),
        )
        for path, expected_role in owner_paths:
            if expected_role == role:
                at(changed, path[:-1])[path[-1]] = "SYNTH-REASSIGNED"
        check("review-role-coherent-" + role, not refreshed_model(changed))
    for i, row in enumerate(data["contrasts"]):
        if row["input"]["decision"]["requested"] != "Closed":
            changed = deepcopy(data)
            changed["contrasts"][i]["input"]["closure"] = deepcopy(
                data["contrasts"][5]["input"]["closure"]
            )
            try:
                refreshed_model(changed)
            except ValueError as exc:
                ok = "ART25 closure record requires Closed request" in str(exc)
            else:
                ok = False
            check(f"review-closure-owner-{i}", ok)
        for j in range(3):
            changed = deepcopy(data)
            changed["contrasts"][i]["handoffs"][j]["dueAt"] = (
                "2026-09-01T10:59:59Z"
            )
            check(
                f"review-handoff-due-before-{i}-{j}",
                "ART25 handoff deadline before source decision"
                in refreshed_model(changed),
            )
            changed["contrasts"][i]["handoffs"][j]["dueAt"] = row["input"][
                "decision"
            ]["at"]
            check(
                f"review-handoff-due-equal-{i}-{j}", not refreshed_model(changed)
            )
    # Existing canonical Closed/deferred and Reopened/prior closure remain valid.
    check("review-closure-canonical-positive", not refreshed_model(data))
    # Ready review: every supplied Evidence ID has referential integrity even
    # when a different transition is requested. Unknown is not a dangling ID.
    reference_paths = (
        ("declaration", "criteriaId"),
        ("preservation", "evidenceId"),
        ("analysisId",),
        ("containment", "validationId"),
        ("recovery", "criteriaId"),
        ("recovery", "validationId"),
        ("previous", "closureValidationId"),
        ("reopening", "newEvidenceId"),
    )
    reference_count = 0
    for i, row in enumerate(data["contrasts"]):
        for path in reference_paths:
            try:
                at(row["input"], path)
            except TypeError:
                continue
            reference_count += 1
            for label, ref, diagnostic in (
                ("dangling", "EV-UNKNOWN", "unresolved evidence reference"),
                (
                    "wrong-kind",
                    f"EV-IR19-{i + 1:03}-CONSENT",
                    "evidence kind/asset binding",
                ),
            ):
                if (
                    path == ("previous", "closureValidationId")
                    and row["input"]["previous"]["status"] != "Closed"
                ):
                    diagnostic = "closure fields owned by previous Closed status"
                changed = deepcopy(data)
                at(changed["contrasts"][i]["input"], path[:-1])[path[-1]] = ref
                try:
                    refreshed_model(changed)
                except ValueError as exc:
                    ok = diagnostic in str(exc)
                else:
                    ok = False
                check(f"ready-reference-{i}-{path}-{label}", ok)
        if row["input"]["decision"]["requested"] != "Reopened":
            changed = deepcopy(data)
            changed["contrasts"][i]["input"]["reopening"] = deepcopy(
                data["contrasts"][6]["input"]["reopening"]
            )
            try:
                refreshed_model(changed)
            except ValueError as exc:
                ok = "ART25 reopening record requires Reopened request" in str(exc)
            else:
                ok = False
            check(f"ready-reopening-owner-{i}", ok)
    check("ready-reference-field-inventory", reference_count == 54)
    # Supplied unknown recovery validation remains a legitimate deferred case.
    check("ready-unknown-receipt-not-dangling", not refreshed_model(data))
    # Author self-check within the same bounded Ready remediation: refreshing
    # BOTH a result and its hash must not preserve a contradictory fixed claim.
    for i, path in (
        (1, ("declaration",)),
        (2, ("preservation",)),
        (3, ("analysisId",)),
        (4, ("recovery", "criteriaId")),
        (5, ("recovery", "validationId")),
        (6, ("reopening",)),
    ):
        changed = deepcopy(data)
        at(changed["contrasts"][i]["input"], path[:-1])[path[-1]] = None
        # An adversarial author recomputes the mutable expected result here;
        # this is a mutation payload, never the independent test oracle.
        changed["contrasts"][i]["expected"] = evaluate(changed["contrasts"][i]["input"])
        check(
            f"ready-claim-result-{i}",
            any("reviewed judgment/result binding" in e for e in refreshed_model(changed)),
        )
    # Schema closure at every existing object, not just the canonical root.
    for path, obj in objects(data):
        changed = deepcopy(data)
        at(changed, path)["unreviewedField"] = True
        check(
            "extra-" + str(path),
            rejected(lambda: validate_schema_instance(changed, schema)),
        )
        # Required-field coverage once per structural path; no fuzzing grammar.
        for key in obj:
            changed = deepcopy(data)
            del at(changed, path)[key]
            check(
                "missing-" + str(path) + key,
                rejected(lambda: validate_schema_instance(changed, schema)),
            )
    # Refresh the editorial hash as an author could: safety/claims still fail.
    for i, row in enumerate(data["contrasts"]):
        for key in row["judgment"]:
            changed = deepcopy(data)
            changed["contrasts"][i]["judgment"][key] = (
                "全組織で侵害なし、全改善完了、実通知済みと判断する。"
            )
            refreshed = deepcopy(contract)
            refreshed["authoredInputs"]["contrasts"] = digest(changed["contrasts"])
            check(
                f"judgment-{i}-{key}",
                rejected(lambda: validate_model(changed, schema, refreshed)),
            )
        claims = [(["decision", "reason"], "実Incidentを処理し、実通知も完了した。")]
        if row["input"]["containment"] is not None:
            claims += [
                (
                    ["containment", "expectedImpact"],
                    "業務影響と残余リスクはすべて解消した。",
                ),
                (["containment", "rollback"], "切戻しに承認と再検証は不要である。"),
            ]
        for path, claim in claims:
            changed = deepcopy(data)
            at(changed["contrasts"][i]["input"], path[:-1])[path[-1]] = claim
            refreshed = deepcopy(contract)
            refreshed["authoredInputs"]["contrasts"] = digest(changed["contrasts"])
            result = validate_model(changed, schema, refreshed)
            check(
                f"input-claim-{i}-{path}",
                any(
                    "reviewed decision reason profile" in e
                    or "reviewed containment impact/rollback profile" in e
                    for e in result
                ),
            )
        for key in (
            "executionAuthorized",
            "notificationDecided",
            "noIncidentClaim",
            "improvementComplete",
        ):
            changed = deepcopy(data)
            changed["contrasts"][i]["expected"][key] = True
            refreshed = deepcopy(contract)
            refreshed["authoredInputs"]["contrasts"] = digest(changed["contrasts"])
            check(
                f"claim-{i}-{key}",
                rejected(lambda: validate_model(changed, schema, refreshed)),
            )
        changed = deepcopy(data)
        changed["contrasts"][i]["expected"]["status"] = "No incident"
        check(
            f"unknown-state-{i}",
            rejected(lambda: validate_model(changed, schema, contract)),
        )
    for key in (
        "actualIncidents",
        "actualActions",
        "actualNotifications",
        "actualCollections",
    ):
        for value in (1, True, False):
            changed = deepcopy(data)
            changed["record"][key] = value
            refreshed = deepcopy(contract)
            refreshed["authoredInputs"]["record"] = digest(changed["record"])
            check(
                f"zero-claim-{key}-{value}",
                rejected(lambda: validate_model(changed, schema, refreshed)),
            )
    for key in (
        "authorityTransferred",
        "evidenceTransferred",
        "parentHandoffReceived",
        "parentStateChanged",
    ):
        changed = deepcopy(data)
        changed["parents"][key] = True
        check("parent-" + key, bool(parent_errors(changed, ROOT)))
    changed = deepcopy(data)
    changed["parents"]["huntHandoffId"] = "HOF-HUNT18-001-1"
    check("parent-hunt-wrong-target", bool(parent_errors(changed, ROOT)))
    changed = deepcopy(data)
    parent = strict(read_regular(ROOT, "cases/fixtures/ch16-telemetry-coverage.json"))
    wrong = next(h for h in parent["handoffs"] if h["targetChapter"] == 18)
    changed["parents"]["telemetryHandoffId"] = wrong["id"]
    changed["parents"]["telemetryRowIds"] = wrong["rowIds"]
    check("parent-telemetry-wrong-target", bool(parent_errors(changed, ROOT)))
    for path, value in [
        (["record", "sourceIds"], ["UNREGISTERED-1", "UNREGISTERED-2"]),
        (["record", "asOf"], "2026-02-30T00:00:00Z"),
        (["record", "asOf"], "2026-09-01T10:59:00Z"),
        (["notification", "dueAt"], "2026-02-30T00:00:00Z"),
    ]:
        changed = deepcopy(data)
        at(changed, path[:-1])[path[-1]] = value
        refreshed = deepcopy(contract)
        refreshed["authoredInputs"][path[0]] = digest(changed[path[0]])
        check(
            "record-metadata-" + str(path) + str(value),
            rejected(lambda: validate_model(changed, schema, refreshed)),
        )
    check("canonical-model", not validate_model(data, schema, contract))
    check("canonical-parent", not parent_errors(data, ROOT))
    # Direct publication selection: preamble/body/tail and new section drift.
    mutations = {}
    ownership = {}
    for path in DOCUMENTS:
        for label, text in (
            ("preamble", "追加の未レビュー前文。\n\n" + source[path]),
            ("tail", source[path] + "\n未レビューの末尾。\n"),
            ("section", source[path] + "\n## 新しい未レビュー節\n\n追加内容。\n"),
            ("unsafe", source[path] + "\n第三者の本番システムへ接続する。\n"),
        ):
            key = path + "#" + label
            mutations[key] = text
            ownership[key] = path
    projected = project_documents(mutations)
    for doc in projected.documents:
        path = ownership[doc.document_id]
        check(
            "selection-" + doc.document_id,
            bool(
                document_errors(
                    replace(doc, document_id=path), contract["documents"][path], data
                )
            ),
        )
        if doc.document_id.endswith("#unsafe"):
            check(
                "shared-unsafe-" + doc.document_id,
                any(
                    "target.real_or_external" in e
                    for e in scan_document(doc, {"hostProvenance": []})
                ),
            )
    for doc in projection.documents:
        spec = contract["documents"][doc.document_id]
        check("canonical-" + doc.document_id, not document_errors(doc, spec, data))
        check("full-inventory-" + doc.document_id, inventory(doc) == spec["fields"])
        # The generic renderer is not reimplemented. Mutate its typed visible
        # output at every selected field to prove the shared scanner is reached.
        for i, field in enumerate(doc.fields):
            if not is_policy_scan_field(field):
                continue
            changed = replace(
                field,
                text="第三者の本番システムへ接続する。",
                normalized_text="第三者の本番システムへ接続する。",
            )
            item = replace(doc, fields=(changed,))
            finding = scan_document(item, {"hostProvenance": []})
            check(
                f"policy-field-{doc.document_id}-{i}",
                any("target.real_or_external" in v for v in finding),
            )
        for n, provenance in enumerate(spec["hostProvenance"]):
            selected = next(
                f
                for f in doc.fields
                if [
                    f.field_type,
                    f.element_kind,
                    f.attribute,
                    f.metadata_value("level"),
                    f.text,
                    f.location,
                ]
                == provenance
            )
            for suffix, changed in (
                ("moved", replace(selected, line=selected.line + 1)),
                (
                    "changed",
                    replace(
                        selected,
                        text=selected.text + " other.invalid-host.net",
                        normalized_text=selected.normalized_text
                        + " other.invalid-host.net",
                    ),
                ),
            ):
                check(
                    f"provenance-{doc.document_id}-{n}-{suffix}",
                    bool(
                        scan_document(
                            replace(doc, fields=(changed,)),
                            {"hostProvenance": [provenance]},
                        )
                    ),
                )
            check(
                f"provenance-{doc.document_id}-{n}-duplicate",
                bool(
                    scan_document(
                        replace(doc, fields=(selected, selected)),
                        {"hostProvenance": [provenance]},
                    )
                ),
            )
    check("strict-duplicate-json", rejected(lambda: strict(b'{"x":1,"x":2}')))
    check("strict-nonfinite-json", rejected(lambda: strict(b'{"x":NaN}')))
    check("strict-invalid-utf8", rejected(lambda: strict(b"\xff")))
    # Bounded local IO tests: owned ignored scratch only, automatic cleanup.
    scratch = ROOT / ".work/ch19-regressions"
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=scratch) as directory:
        root = Path(directory)
        p = root / DATA
        p.parent.mkdir(parents=True)
        p.write_bytes(b"{}")
        check("regular-read", read_regular(root, DATA) == b"{}")
        p.unlink()
        p.symlink_to("absent")
        check("symlink-rejected", rejected(lambda: read_regular(root, DATA)))
        p.unlink()
        p.write_bytes(b"x" * (1024 * 1024 + 1))
        check("oversize-rejected", rejected(lambda: read_regular(root, DATA)))
        check(
            "unowned-input-rejected", rejected(lambda: read_regular(root, "other.json"))
        )
    return len(checks), errors
