#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULE_PATH = ROOT / "detections/cloud_identity/det_2026_017_001.json"
FIXTURE_PATH = ROOT / "cases/fixtures/ch17-detection-engineering-fixture.json"
STABLE_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)+$")


class ReplayError(ValueError):
    pass


def load_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ReplayError(f"{path.relative_to(ROOT)}: root must be an object")
    return value


def parse_time(raw: object, label: str) -> datetime:
    if not isinstance(raw, str):
        raise ReplayError(f"{label}: timestamp must be a string")
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ReplayError(f"{label}: invalid timestamp {raw!r}") from exc
    if parsed.tzinfo is None:
        raise ReplayError(f"{label}: timestamp must include an offset")
    return parsed


def require_fields(record: dict, fields: list[str], label: str) -> None:
    missing = [field for field in fields if field not in record]
    if missing:
        raise ReplayError(f"{label}: missing required fields {missing}")


def require_non_empty_string(raw: object, label: str) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise ReplayError(f"{label}: must be a non-empty string")
    return raw


def require_stable_id(raw: object, label: str, prefix: str | None = None) -> str:
    value = require_non_empty_string(raw, label)
    if not STABLE_ID_RE.fullmatch(value) or (prefix and not value.startswith(prefix)):
        expected = f" with prefix {prefix!r}" if prefix else ""
        raise ReplayError(f"{label}: must be a stable lowercase identifier{expected}")
    return value


def require_string_list(raw: object, label: str, *, non_empty: bool) -> list[str]:
    if not isinstance(raw, list) or (non_empty and not raw):
        suffix = " non-empty" if non_empty else ""
        raise ReplayError(f"{label}: must be a{suffix} string array")
    if any(not isinstance(item, str) or not item for item in raw):
        raise ReplayError(f"{label}: must contain only non-empty strings")
    return raw


def records_for(fixture: dict, telemetry_id: str) -> list[dict]:
    records = fixture.get("records", [])
    if not isinstance(records, list):
        raise ReplayError(f"{fixture.get('fixtureId')}: records must be an array")
    return [
        record
        for record in records
        if isinstance(record, dict) and record.get("telemetryId") == telemetry_id
    ]


def validate_record_envelope(record: dict, fixture_id: object) -> None:
    require_fields(record, ["telemetryId", "recordId", "eventType"], f"{fixture_id} record")
    require_stable_id(record["recordId"], f"{fixture_id} recordId", "rec-")
    require_non_empty_string(record["telemetryId"], f"{fixture_id} telemetryId")
    require_non_empty_string(record["eventType"], f"{fixture_id} eventType")


def validate_candidate_record(record: dict, contract: dict, fixture_id: object) -> None:
    fields = [
        contract["eventTimeField"],
        contract["ingestTimeField"],
        contract["actorField"],
        contract["targetField"],
        contract["grantedScopeField"],
        contract["changeTicketField"],
        contract["resultField"],
    ]
    require_fields(record, fields, f"{fixture_id} candidate")
    parse_time(record[contract["eventTimeField"]], f"{fixture_id} candidate event time")
    parse_time(record[contract["ingestTimeField"]], f"{fixture_id} candidate ingest time")
    require_stable_id(record[contract["actorField"]], f"{fixture_id} candidate actor")
    require_stable_id(
        record[contract["targetField"]],
        f"{fixture_id} candidate target",
        "workload-",
    )
    require_string_list(
        record[contract["grantedScopeField"]],
        f"{fixture_id} granted scope",
        non_empty=True,
    )
    ticket = record[contract["changeTicketField"]]
    if ticket is not None:
        require_stable_id(ticket, f"{fixture_id} candidate change ticket", "chg-")
    result = require_non_empty_string(
        record[contract["resultField"]], f"{fixture_id} candidate result"
    )
    if result not in {"success", "failure"}:
        raise ReplayError(f"{fixture_id} candidate result: unsupported value {result!r}")


def validate_approval_record(record: dict, contract: dict, fixture_id: object) -> None:
    fields = [
        contract["ticketField"],
        contract["approvedScopeField"],
        contract["windowStartField"],
        contract["windowEndField"],
        contract["ownerField"],
    ]
    require_fields(record, fields, f"{fixture_id} approval")
    require_stable_id(record[contract["ticketField"]], f"{fixture_id} approval ticket", "chg-")
    require_string_list(
        record[contract["approvedScopeField"]],
        f"{fixture_id} approved scope",
        non_empty=True,
    )
    start = parse_time(record[contract["windowStartField"]], f"{fixture_id} approval window start")
    end = parse_time(record[contract["windowEndField"]], f"{fixture_id} approval window end")
    if start > end:
        raise ReplayError(f"{fixture_id} approval window: start must not be after end")
    require_stable_id(record[contract["ownerField"]], f"{fixture_id} approval owner", "owner-")


def validate_sign_in_record(record: dict, contract: dict, fixture_id: object) -> None:
    fields = [
        contract["eventTimeField"],
        contract["targetField"],
        contract["resultField"],
    ]
    require_fields(record, fields, f"{fixture_id} sign-in")
    parse_time(record[contract["eventTimeField"]], f"{fixture_id} sign-in event time")
    require_stable_id(
        record[contract["targetField"]],
        f"{fixture_id} sign-in target",
        "workload-",
    )
    result = require_non_empty_string(record[contract["resultField"]], f"{fixture_id} sign-in result")
    if result not in {"success", "failure"}:
        raise ReplayError(f"{fixture_id} sign-in result: unsupported value {result!r}")
    credential_state = record.get(contract["credentialStateField"])
    if credential_state is not None and credential_state not in {"active", "disabled"}:
        raise ReplayError(
            f"{fixture_id} sign-in credential state: unsupported value {credential_state!r}"
        )
    source_label = record.get(contract["sourceLabelField"])
    if source_label is not None:
        require_non_empty_string(source_label, f"{fixture_id} sign-in source label")


def validate_fixture_records(rule: dict, fixture: dict, known_ids: set[str]) -> None:
    fixture_id = fixture.get("fixtureId")
    records = fixture.get("records")
    if not isinstance(records, list):
        raise ReplayError(f"{fixture_id}: records must be an array")
    for record in records:
        if not isinstance(record, dict):
            raise ReplayError(f"{fixture_id}: every record must be an object")
        validate_record_envelope(record, fixture_id)
        telemetry_id = record["telemetryId"]
        if telemetry_id not in known_ids:
            raise ReplayError(f"{fixture_id}: unknown telemetry ID {telemetry_id!r}")
        if telemetry_id == rule["candidate"]["telemetryId"]:
            validate_candidate_record(record, rule["candidate"], fixture_id)
        elif telemetry_id == rule["approval"]["telemetryId"]:
            validate_approval_record(record, rule["approval"], fixture_id)
        elif telemetry_id == rule["severityEscalation"]["telemetryId"]:
            validate_sign_in_record(record, rule["severityEscalation"], fixture_id)


def triage_context(
    rule: dict,
    *,
    evidence_ids: list[str],
    scope_delta: list[str] | None,
    change_ticket_status: str,
    target_workload_id: str | None,
    coverage_statement: str,
    correlation_state: str,
    category: str | None,
) -> dict:
    return {
        "case_id": rule["caseId"],
        "detection_id": rule["detectionId"],
        "evidence_ids": evidence_ids,
        "scope_delta": scope_delta,
        "change_ticket_status": change_ticket_status,
        "target_workload_id": target_workload_id,
        "coverage_statement": coverage_statement,
        "correlation_state": correlation_state,
        "category": category,
    }


def evaluate(rule: dict, fixture: dict) -> dict:
    required = require_string_list(
        rule.get("requiredTelemetryIds"), "rule requiredTelemetryIds", non_empty=True
    )
    optional = require_string_list(
        rule.get("optionalTelemetryIds"), "rule optionalTelemetryIds", non_empty=False
    )
    available = require_string_list(
        fixture.get("availableTelemetryIds"),
        f"{fixture.get('fixtureId')} availableTelemetryIds",
        non_empty=False,
    )
    if len(available) != len(set(available)):
        raise ReplayError(f"{fixture.get('fixtureId')}: availableTelemetryIds contains duplicates")
    evidence_ids = require_string_list(
        fixture.get("relatedEvidenceIds"),
        f"{fixture.get('fixtureId')} relatedEvidenceIds",
        non_empty=True,
    )
    if len(evidence_ids) != len(set(evidence_ids)):
        raise ReplayError(f"{fixture.get('fixtureId')}: relatedEvidenceIds contains duplicates")
    known_ids = set(required + optional)
    unknown = set(available) - known_ids
    if unknown:
        raise ReplayError(f"{fixture.get('fixtureId')}: unknown available telemetry IDs {sorted(unknown)}")
    validate_fixture_records(rule, fixture, known_ids)
    record_ids = {
        record["telemetryId"]
        for record in fixture.get("records", [])
        if isinstance(record, dict)
    }
    unavailable_records = record_ids - set(available)
    if unavailable_records:
        raise ReplayError(
            f"{fixture.get('fixtureId')}: records claim unavailable telemetry {sorted(unavailable_records)}"
        )

    candidate_contract = rule["candidate"]
    approval_contract = rule["approval"]
    escalation_contract = rule["severityEscalation"]
    candidates = records_for(fixture, candidate_contract["telemetryId"])
    approvals = records_for(fixture, approval_contract["telemetryId"])
    sign_ins = records_for(fixture, escalation_contract["telemetryId"])

    missing_required = sorted(set(required) - set(available))
    outcomes = rule.get("outcomes")
    if not isinstance(outcomes, dict):
        raise ReplayError("rule outcomes must be an object")
    if missing_required:
        known_candidate = next(
            (
                candidate
                for candidate in candidates
                if candidate.get("eventType") == candidate_contract["eventType"]
                and candidate.get(candidate_contract["resultField"]) == "success"
            ),
            None,
        )
        return {
            "outcome": outcomes["telemetryGap"],
            "severity": "none",
            "triage": triage_context(
                rule,
                evidence_ids=evidence_ids,
                scope_delta=None,
                change_ticket_status="unknown",
                target_workload_id=(
                    known_candidate[candidate_contract["targetField"]]
                    if known_candidate is not None
                    else None
                ),
                coverage_statement=f"Missing required telemetry: {', '.join(missing_required)}",
                correlation_state="indeterminate",
                category="Needs telemetry gap review",
            ),
        }

    coverage_statement = (
        "Core telemetry available; optional escalation telemetry available"
        if escalation_contract["telemetryId"] in available
        else "Core telemetry available; optional escalation telemetry unavailable"
    )

    alerts: list[dict] = []
    approved: list[dict] = []
    for candidate in candidates:
        if (
            candidate.get("eventType") != candidate_contract["eventType"]
            or candidate.get(candidate_contract["resultField"]) != "success"
        ):
            continue
        candidate_time = parse_time(
            candidate[candidate_contract["eventTimeField"]],
            f"{fixture.get('fixtureId')} candidate",
        )
        ticket = candidate[candidate_contract["changeTicketField"]]
        granted = set(candidate[candidate_contract["grantedScopeField"]])

        matching_approval = None
        for approval in approvals:
            if approval.get("eventType") != approval_contract["eventType"]:
                continue
            if not ticket or approval[approval_contract["ticketField"]] != ticket:
                continue
            start = parse_time(
                approval[approval_contract["windowStartField"]],
                f"{fixture.get('fixtureId')} approval window start",
            )
            end = parse_time(
                approval[approval_contract["windowEndField"]],
                f"{fixture.get('fixtureId')} approval window end",
            )
            if start <= candidate_time <= end:
                matching_approval = approval
                break

        approved_scopes = (
            set(matching_approval[approval_contract["approvedScopeField"]])
            if matching_approval
            else set()
        )
        scope_delta = sorted(granted - approved_scopes)
        if matching_approval and not scope_delta:
            approved.append(
                {
                    "scope_delta": [],
                    "change_ticket_status": "approved",
                    "target_workload_id": candidate[candidate_contract["targetField"]],
                }
            )
            continue

        severity = "high"
        correlation_state = (
            "optional_telemetry_unavailable"
            if escalation_contract["telemetryId"] not in available
            else "not_observed"
        )
        target = candidate[candidate_contract["targetField"]]
        for sign_in in sign_ins:
            if (
                sign_in.get("eventType") != escalation_contract["eventType"]
                or sign_in[escalation_contract["targetField"]] != target
                or sign_in[escalation_contract["resultField"]] != "success"
                or sign_in.get(escalation_contract["credentialStateField"]) != "active"
                or not sign_in.get(escalation_contract["sourceLabelField"])
            ):
                continue
            sign_in_time = parse_time(
                sign_in[escalation_contract["eventTimeField"]],
                f"{fixture.get('fixtureId')} escalation event",
            )
            elapsed_minutes = (sign_in_time - candidate_time).total_seconds() / 60
            if 0 <= elapsed_minutes <= escalation_contract["withinMinutes"]:
                severity = "critical"
                correlation_state = "successful_active_sign_in_observed"
                break
        alerts.append(
            {
                "severity": severity,
                "scope_delta": scope_delta,
                "change_ticket_status": "missing" if not ticket else "not_approved",
                "target_workload_id": target,
                "correlation_state": correlation_state,
            }
        )

    if alerts:
        selected = next((item for item in alerts if item["severity"] == "critical"), alerts[0])
        return {
            "outcome": outcomes["unapprovedScopeChange"],
            "severity": selected["severity"],
            "triage": triage_context(
                rule,
                evidence_ids=evidence_ids,
                scope_delta=selected["scope_delta"],
                change_ticket_status=selected["change_ticket_status"],
                target_workload_id=selected["target_workload_id"],
                coverage_statement=coverage_statement,
                correlation_state=selected["correlation_state"],
                category="Escalate",
            ),
        }
    if approved:
        selected = approved[0]
        return {
            "outcome": outcomes["approvedScopeChange"],
            "severity": "informational",
            "triage": triage_context(
                rule,
                evidence_ids=evidence_ids,
                scope_delta=selected["scope_delta"],
                change_ticket_status=selected["change_ticket_status"],
                target_workload_id=selected["target_workload_id"],
                coverage_statement=coverage_statement,
                correlation_state="not_required_for_approved_change",
                category="Approved change",
            ),
        }
    return {
        "outcome": outcomes["noCandidateEvent"],
        "severity": "none",
        "triage": triage_context(
            rule,
            evidence_ids=evidence_ids,
            scope_delta=[],
            change_ticket_status="not_applicable",
            target_workload_id=None,
            coverage_statement=coverage_statement,
            correlation_state="not_applicable",
            category=None,
        ),
    }


def assert_result(rule: dict, fixture_set: dict, fixture: dict, result: dict) -> None:
    expected = (fixture.get("expectedOutcome"), fixture.get("expectedSeverity"))
    actual = (result.get("outcome"), result.get("severity"))
    if actual != expected:
        raise ReplayError(f"{fixture.get('fixtureId')}: expected {expected}, got {actual}")
    triage = result.get("triage")
    if not isinstance(triage, dict):
        raise ReplayError(f"{fixture.get('fixtureId')}: triage context must be an object")
    must_include = fixture_set.get("triage", {}).get("mustInclude")
    if not isinstance(must_include, list) or any(field not in triage for field in must_include):
        raise ReplayError(f"{fixture.get('fixtureId')}: triage context is incomplete")
    if triage.get("category") != fixture.get("expectedTriageCategory"):
        raise ReplayError(
            f"{fixture.get('fixtureId')}: expected triage category "
            f"{fixture.get('expectedTriageCategory')!r}, got {triage.get('category')!r}"
        )
    if triage.get("evidence_ids") != fixture.get("relatedEvidenceIds"):
        raise ReplayError(
            f"{fixture.get('fixtureId')}: triage evidence_ids must match relatedEvidenceIds"
        )


def build_gap_fixture(fixture_set: dict) -> dict:
    gap = fixture_set.get("coverageGapExample")
    if not isinstance(gap, dict):
        raise ReplayError("coverageGapExample must be an object")
    source_id = gap.get("sourceFixtureId")
    source = next(
        (
            fixture
            for fixture in fixture_set.get("fixtures", [])
            if isinstance(fixture, dict) and fixture.get("fixtureId") == source_id
        ),
        None,
    )
    if source is None:
        raise ReplayError(f"coverageGapExample: source fixture {source_id!r} was not found")
    missing = require_string_list(
        gap.get("missingTelemetryIds"), "coverageGapExample missingTelemetryIds", non_empty=True
    )
    derived = copy.deepcopy(source)
    derived["fixtureId"] = gap.get("gapId")
    derived["availableTelemetryIds"] = [
        item for item in source.get("availableTelemetryIds", []) if item not in missing
    ]
    derived["records"] = [
        record
        for record in source.get("records", [])
        if isinstance(record, dict) and record.get("telemetryId") not in missing
    ]
    derived["expectedOutcome"] = gap.get("expectedOutcome")
    derived["expectedSeverity"] = gap.get("expectedSeverity")
    derived["expectedTriageCategory"] = gap.get("expectedTriageCategory")
    derived["relatedEvidenceIds"] = gap.get("relatedEvidenceIds")
    return derived


def expect_replay_error(rule: dict, fixture: dict, label: str) -> None:
    try:
        evaluate(rule, fixture)
    except ReplayError:
        return
    raise ReplayError(f"regression {label}: expected ReplayError")


def run_regressions(rule: dict, fixture_set: dict) -> None:
    fixtures = {item["fixtureId"]: item for item in fixture_set["fixtures"]}
    positive = fixtures["FIX-2026-017-POS"]
    benign = fixtures["FIX-2026-017-BNM"]

    missing_field = copy.deepcopy(positive)
    del missing_field["records"][0]["ingest_time"]
    expect_replay_error(rule, missing_field, "missing candidate field")

    failed_candidate = copy.deepcopy(positive)
    failed_candidate["records"][0]["result"] = "failure"
    failed_candidate_result = evaluate(rule, failed_candidate)
    if (failed_candidate_result["outcome"], failed_candidate_result["severity"]) != (
        rule["outcomes"]["noCandidateEvent"],
        "none",
    ):
        raise ReplayError("regression failed candidate: failed event must not alert")

    wrong_approval = copy.deepcopy(benign)
    wrong_approval["records"][1]["eventType"] = "unrelated_snapshot"
    wrong_approval_result = evaluate(rule, wrong_approval)
    if wrong_approval_result["outcome"] != rule["outcomes"]["unapprovedScopeChange"]:
        raise ReplayError("regression wrong approval type: unrelated record must not suppress")

    for field, value, label in (
        ("result", "failure", "failed sign-in"),
        ("credential_state", "disabled", "disabled credential"),
        ("source_label", None, "partial sign-in enrichment"),
    ):
        partial = copy.deepcopy(positive)
        if value is None:
            del partial["records"][2][field]
        else:
            partial["records"][2][field] = value
        partial_result = evaluate(rule, partial)
        if (partial_result["outcome"], partial_result["severity"]) != (
            rule["outcomes"]["unapprovedScopeChange"],
            "high",
        ):
            raise ReplayError(f"regression {label}: must retain high alert without escalation")

    no_optional = copy.deepcopy(positive)
    no_optional["availableTelemetryIds"].remove("TEL-DET-2026-003")
    no_optional["records"] = [
        record for record in no_optional["records"] if record["telemetryId"] != "TEL-DET-2026-003"
    ]
    no_optional_result = evaluate(rule, no_optional)
    if (no_optional_result["outcome"], no_optional_result["severity"]) != (
        rule["outcomes"]["unapprovedScopeChange"],
        "high",
    ):
        raise ReplayError("regression optional telemetry: core detection must remain evaluable")

    missing_core_result = evaluate(rule, build_gap_fixture(fixture_set))
    if missing_core_result["outcome"] != rule["outcomes"]["telemetryGap"]:
        raise ReplayError("regression core telemetry gap: must be indeterminate")
    missing_core_triage = missing_core_result["triage"]
    if missing_core_triage["target_workload_id"] != "workload-billing-approval-01":
        raise ReplayError("regression core telemetry gap: known target must be preserved")
    if missing_core_triage["scope_delta"] is not None:
        raise ReplayError("regression core telemetry gap: approval-dependent scope delta must be unknown")

    mutated_rule = copy.deepcopy(rule)
    mutated_rule["outcomes"]["unapprovedScopeChange"] = "mutated_alert_contract"
    if evaluate(mutated_rule, positive)["outcome"] != "mutated_alert_contract":
        raise ReplayError("regression rule outcomes: runner must use the rule declaration")

    malformed_target = copy.deepcopy(positive)
    malformed_target["records"][0]["target_workload_id"] = "Billing Workload"
    expect_replay_error(rule, malformed_target, "unstable target identifier")


def main() -> int:
    try:
        rule = load_object(RULE_PATH)
        fixture_set = load_object(FIXTURE_PATH)
        if rule.get("syntheticOnly") is not True or rule.get("offlineOnly") is not True:
            raise ReplayError("rule must remain synthetic-only and offline-only")
        if rule.get("detectionId") != fixture_set.get("detectionId"):
            raise ReplayError("rule and fixture detection IDs differ")

        fixtures = fixture_set.get("fixtures", [])
        if not isinstance(fixtures, list) or not fixtures:
            raise ReplayError("fixture set is empty")
        results = []
        for fixture in fixtures:
            if not isinstance(fixture, dict):
                raise ReplayError("fixture entry must be an object")
            result = evaluate(rule, fixture)
            assert_result(rule, fixture_set, fixture, result)
            results.append(
                f"{fixture.get('fixtureId')}={result['outcome']}/{result['severity']}"
            )

        gap_fixture = build_gap_fixture(fixture_set)
        gap_result = evaluate(rule, gap_fixture)
        assert_result(rule, fixture_set, gap_fixture, gap_result)
        results.append(
            f"{gap_fixture.get('fixtureId')}={gap_result['outcome']}/{gap_result['severity']}"
        )
        run_regressions(rule, fixture_set)
    except (KeyError, OSError, json.JSONDecodeError, ReplayError) as exc:
        print(f"ERROR: {exc}")
        return 1

    print("chapter 17 offline replay passed: " + ", ".join(results) + ", regressions=10")
    return 0


if __name__ == "__main__":
    sys.exit(main())
