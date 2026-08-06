#!/usr/bin/env python3
"""Fail-closed contract tests for the shared content safety policy."""

from __future__ import annotations

from dataclasses import fields, is_dataclass
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.content_safety_policy import (  # noqa: E402
    ACTION_RULES,
    POLICY_VERSION,
    PROTECTED_OBJECT_RULES,
    SafetyFinding,
    normalize_visible_text,
    scan_action_text,
    scan_fields,
    scan_host_policy,
)


EXPECTED_POLICY_VERSION = "1.0.0"
EXPECTED_ACTION_CATEGORIES = {
    "target.real_or_external",
    "secret.credential",
    "data.pii",
    "operation.authentication_or_session",
    "operation.malware",
    "operation.c2_or_phishing",
    "operation.privilege_or_evasion",
    "operation.disruption_or_destruction",
    "operation.social_engineering_or_tracking",
    "analysis.weak_evidence_attribution",
}
EXPECTED_ALL_CATEGORIES = EXPECTED_ACTION_CATEGORIES | {"network.host_or_address"}
BLOCKER_TEXTS = {
    "do not build a keylogger, but deploy it",
    "never build a keylogger; however, use it",
    "keyloggerを作ることを禁止する、しかしそれを作る",
    "building a keylogger should be prohibited, but it is deployed",
    "write a keylogger",
    "code a rootkit",
}
SAFE_BLOCKER_COUNTERPARTS = {
    "Do not build a keylogger.",
    "Building a keylogger is prohibited.",
    "Keylogger creation is outside this book's scope.",
    "この教材ではkeyloggerを作らない。",
    "keyloggerを作ることを禁止する。",
    "この語はMalware分類の説明としてのみ記録する。",
}
REQUIRED_UNSAFE_PROHIBITION_SCOPE = {
    "CONTINUATION-FORBIDDEN-CONTRAST-MALWARE": (
        "Do not build a keylogger, but it is forbidden to deploy but use it."
    ),
    "CONTINUATION-FORBIDDEN-CONTRAST-TARGET": (
        "Do not access a third-party production API, but it is forbidden to connect "
        "to it but record it."
    ),
    "CONTINUATION-FORBIDDEN-COMMA-MALWARE": (
        "Do not build a keylogger, but it is forbidden to deploy, and use it."
    ),
    "CONTINUATION-FORBIDDEN-SENTENCE-MALWARE": (
        "Do not build a keylogger, but it is forbidden to deploy. Use it."
    ),
    "CONTINUATION-FORBIDDEN-PERIOD-CHAIN-MALWARE": (
        "Do not build a keylogger. It is forbidden to deploy. Use it."
    ),
    "CONTINUATION-FORBIDDEN-PERIOD-CHAIN-TARGET": (
        "Do not access a third-party production API. It is forbidden to connect "
        "to it. Record it."
    ),
    "TRAILING-PROHIBITION-DIFFERENT-ACTION": (
        "Build a keylogger whose deployment is prohibited."
    ),
    "FORBIDDEN-COORDINATOR-NEW-SUBJECT": (
        "Do not build a keylogger, but it is forbidden to deploy it and you should "
        "use it."
    ),
    "SAME-CLAUSE-AMBIGUOUS-AND-MALWARE": (
        "Do not build a keylogger and use it."
    ),
    "SAME-CLAUSE-AMBIGUOUS-AND-TARGET": (
        "Do not access a third-party production API and scan it."
    ),
    "SAME-CLAUSE-AMBIGUOUS-JA-MALWARE": "keyloggerを作らないで使用する",
}
REQUIRED_SAFE_PROHIBITION_SCOPE = {
    "SAFE-030": "Do not build a keylogger, but it is forbidden to deploy and use it.",
    "SAFE-031": (
        "Do not access a third-party production API, but it is forbidden to connect "
        "to it and record it."
    ),
    "SAFE-032": (
        "Do not build a keylogger. It is forbidden to deploy. Do not use it."
    ),
    "SAFE-033": "Do not build or deploy a keylogger.",
    "SAFE-034": "Do not access or scan a third-party production API.",
}


errors: list[str] = []


def error(message: str) -> None:
    errors.append(message)


def load_json(relative: str) -> dict[str, Any]:
    path = ROOT / relative
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        error(f"{relative}: cannot load strict UTF-8 JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        error(f"{relative}: root must be an object")
        return {}
    return value


def exact_keys(value: dict[str, Any], expected: set[str], context: str) -> bool:
    actual = set(value)
    if actual != expected:
        error(f"{context}: keys {sorted(actual)!r} do not match {sorted(expected)!r}")
        return False
    return True


def checked_entries(
    value: Any,
    *,
    expected_keys: set[str],
    context: str,
) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        error(f"{context}: must be an array")
        return []
    result: list[dict[str, Any]] = []
    ids: set[str] = set()
    for index, item in enumerate(value):
        item_context = f"{context}[{index}]"
        if not isinstance(item, dict):
            error(f"{item_context}: must be an object")
            continue
        exact_keys(item, expected_keys, item_context)
        identifier = item.get("id")
        if not isinstance(identifier, str) or not identifier:
            error(f"{item_context}: id must be a non-empty string")
        elif identifier in ids:
            error(f"{item_context}: duplicate id {identifier!r}")
        else:
            ids.add(identifier)
        if not isinstance(item.get("text"), str) or not item.get("text"):
            error(f"{item_context}: text must be a non-empty string")
        result.append(item)
    return result


def check_public_api() -> None:
    if POLICY_VERSION != EXPECTED_POLICY_VERSION:
        error(f"policy version {POLICY_VERSION!r} is not {EXPECTED_POLICY_VERSION!r}")
    if not is_dataclass(SafetyFinding):
        error("SafetyFinding must be a dataclass")
    actual_fields = tuple(field.name for field in fields(SafetyFinding))
    expected_fields = (
        "category",
        "location",
        "normalized_excerpt",
        "reason",
        "policy_version",
    )
    if actual_fields != expected_fields:
        error(f"SafetyFinding fields {actual_fields!r} do not match {expected_fields!r}")
    if not SafetyFinding.__dataclass_params__.frozen:
        error("SafetyFinding must remain frozen")
    for function in (normalize_visible_text, scan_action_text, scan_host_policy, scan_fields):
        if not callable(function):
            error(f"stable API member {function!r} is not callable")

    model_categories = {rule.category for rule in PROTECTED_OBJECT_RULES}
    if model_categories != EXPECTED_ACTION_CATEGORIES:
        error(
            f"protected object categories {sorted(model_categories)!r} do not match "
            f"{sorted(EXPECTED_ACTION_CATEGORIES)!r}"
        )
    required_action_kinds = {"create", "deploy-use", "access-collect", "perform", "attribute"}
    action_kinds = {rule.kind for rule in ACTION_RULES}
    if action_kinds != required_action_kinds:
        error(f"action kinds {sorted(action_kinds)!r} do not match {sorted(required_action_kinds)!r}")


def check_action_corpus() -> list[tuple[str, str]]:
    relative = "tests/fixtures/content-safety/action-corpus.json"
    corpus = load_json(relative)
    exact_keys(corpus, {"schemaVersion", "policyVersion", "unsafe", "safe"}, relative)
    if corpus.get("schemaVersion") != "1.0.0" or corpus.get("policyVersion") != POLICY_VERSION:
        error(f"{relative}: schemaVersion/policyVersion mismatch")

    unsafe = checked_entries(
        corpus.get("unsafe"),
        expected_keys={"id", "text", "expectedCategories"},
        context=f"{relative}.unsafe",
    )
    safe = checked_entries(
        corpus.get("safe"),
        expected_keys={"id", "text"},
        context=f"{relative}.safe",
    )

    unsafe_texts = {item.get("text") for item in unsafe}
    safe_texts = {item.get("text") for item in safe}
    if not BLOCKER_TEXTS <= unsafe_texts:
        error(f"{relative}: missing blocker phrases {sorted(BLOCKER_TEXTS - unsafe_texts)!r}")
    if not SAFE_BLOCKER_COUNTERPARTS <= safe_texts:
        error(
            f"{relative}: missing safe blocker counterparts "
            f"{sorted(SAFE_BLOCKER_COUNTERPARTS - safe_texts)!r}"
        )

    covered_categories: set[str] = set()
    deterministic_fields: list[tuple[str, str]] = []
    for item in unsafe:
        identifier = item.get("id")
        text = item.get("text")
        expected = item.get("expectedCategories")
        if not isinstance(identifier, str) or not isinstance(text, str):
            continue
        if (
            not isinstance(expected, list)
            or not expected
            or not all(isinstance(category, str) for category in expected)
        ):
            error(f"{relative}.{identifier}: expectedCategories must be a non-empty string array")
            continue
        if not set(expected) <= EXPECTED_ACTION_CATEGORIES:
            error(f"{relative}.{identifier}: unknown expected category")
        findings = scan_action_text(text, location=identifier)
        actual = {finding.category for finding in findings}
        if not set(expected) <= actual:
            error(
                f"{relative}.{identifier}: expected {sorted(expected)!r}, got {sorted(actual)!r}"
            )
        if any(finding.location != identifier for finding in findings):
            error(f"{relative}.{identifier}: finding location drift")
        if any(finding.policy_version != POLICY_VERSION for finding in findings):
            error(f"{relative}.{identifier}: finding policy version drift")
        covered_categories.update(expected)
        deterministic_fields.append((identifier, text))

    if covered_categories != EXPECTED_ACTION_CATEGORIES:
        error(
            f"{relative}: category coverage {sorted(covered_categories)!r} does not match "
            f"{sorted(EXPECTED_ACTION_CATEGORIES)!r}"
        )
    required_pair_ids = {"TARGET-OBJECT-FIRST", "TARGET-ACTION-FIRST"}
    unsafe_by_id = {item.get("id"): item.get("text") for item in unsafe}
    safe_by_id = {item.get("id"): item.get("text") for item in safe}
    unsafe_ids = set(unsafe_by_id)
    if not required_pair_ids <= unsafe_ids:
        error(f"{relative}: action-before/object-before regressions are incomplete")
    for identifier, expected_text in REQUIRED_UNSAFE_PROHIBITION_SCOPE.items():
        if unsafe_by_id.get(identifier) != expected_text:
            error(f"{relative}: unsafe prohibition-scope regression {identifier!r} drifted")
    for identifier, expected_text in REQUIRED_SAFE_PROHIBITION_SCOPE.items():
        if safe_by_id.get(identifier) != expected_text:
            error(f"{relative}: safe prohibition-scope regression {identifier!r} drifted")

    for item in safe:
        identifier = item.get("id")
        text = item.get("text")
        if not isinstance(identifier, str) or not isinstance(text, str):
            continue
        findings = scan_action_text(text, location=identifier)
        if findings:
            error(f"{relative}.{identifier}: safe text produced findings {findings!r}")
        deterministic_fields.append((identifier, text))

    long_coordination = "Do not build" + " or use" * 1200 + " a keylogger."
    try:
        long_findings = scan_action_text(
            long_coordination,
            location="LONG-OR-COORDINATION",
        )
    except RecursionError:
        error(f"{relative}: long coordination depends on Python recursion depth")
    else:
        if long_findings:
            error(
                f"{relative}: explicitly negated long coordination produced "
                f"{long_findings!r}"
            )
    return deterministic_fields


def check_normalization_corpus() -> None:
    relative = "tests/fixtures/content-safety/normalization-corpus.json"
    corpus = load_json(relative)
    exact_keys(corpus, {"schemaVersion", "policyVersion", "cases"}, relative)
    if corpus.get("schemaVersion") != "1.0.0" or corpus.get("policyVersion") != POLICY_VERSION:
        error(f"{relative}: schemaVersion/policyVersion mismatch")
    cases = corpus.get("cases")
    if not isinstance(cases, list):
        error(f"{relative}.cases: must be an array")
        return
    ids: set[str] = set()
    for index, item in enumerate(cases):
        context = f"{relative}.cases[{index}]"
        if not isinstance(item, dict):
            error(f"{context}: must be an object")
            continue
        exact_keys(item, {"id", "input", "expected"}, context)
        identifier, text, expected = item.get("id"), item.get("input"), item.get("expected")
        if not all(isinstance(value, str) for value in (identifier, text, expected)):
            error(f"{context}: id/input/expected must be strings")
            continue
        if identifier in ids:
            error(f"{context}: duplicate id {identifier!r}")
        ids.add(identifier)
        actual = normalize_visible_text(text)
        if actual != expected:
            error(f"{context}: normalized value {actual!r} does not match {expected!r}")


def check_host_corpus() -> list[tuple[str, str]]:
    relative = "tests/fixtures/content-safety/host-corpus.json"
    corpus = load_json(relative)
    exact_keys(corpus, {"schemaVersion", "policyVersion", "safe", "unsafe"}, relative)
    if corpus.get("schemaVersion") != "1.0.0" or corpus.get("policyVersion") != POLICY_VERSION:
        error(f"{relative}: schemaVersion/policyVersion mismatch")
    safe = checked_entries(
        corpus.get("safe"),
        expected_keys={"id", "text"},
        context=f"{relative}.safe",
    )
    unsafe = checked_entries(
        corpus.get("unsafe"),
        expected_keys={"id", "text", "requiredReason", "forbiddenReason"},
        context=f"{relative}.unsafe",
    )
    deterministic_fields: list[tuple[str, str]] = []
    for item in safe:
        identifier, text = item.get("id"), item.get("text")
        if not isinstance(identifier, str) or not isinstance(text, str):
            continue
        findings = scan_host_policy(text, location=identifier)
        if findings:
            error(f"{relative}.{identifier}: safe host/address produced findings {findings!r}")
        deterministic_fields.append((identifier, text))
    for item in unsafe:
        identifier, text = item.get("id"), item.get("text")
        required, forbidden = item.get("requiredReason"), item.get("forbiddenReason")
        if not all(isinstance(value, str) for value in (identifier, text, required, forbidden)):
            error(f"{relative}: unsafe host fields must be strings")
            continue
        findings = scan_host_policy(text, location=identifier)
        reasons = "\n".join(finding.reason for finding in findings)
        if not findings or required not in reasons:
            error(f"{relative}.{identifier}: required diagnostic {required!r} missing")
        if forbidden and forbidden in reasons:
            error(f"{relative}.{identifier}: forbidden diagnostic {forbidden!r} was used")
        if any(finding.category != "network.host_or_address" for finding in findings):
            error(f"{relative}.{identifier}: host finding category drift")
        deterministic_fields.append((identifier, text))
    return deterministic_fields


def check_representative_main_fields() -> list[tuple[str, str]]:
    relative = "tests/fixtures/content-safety/representative-main-fields.json"
    corpus = load_json(relative)
    exact_keys(
        corpus,
        {"schemaVersion", "policyVersion", "baselineMain", "scope", "fields"},
        relative,
    )
    if corpus.get("schemaVersion") != "1.0.0" or corpus.get("policyVersion") != POLICY_VERSION:
        error(f"{relative}: schemaVersion/policyVersion mismatch")
    if corpus.get("baselineMain") != "2c40869febd75b9e13fec544aec9bf90552e1556":
        error(f"{relative}: reference baseline main changed without explicit audit")
    if "not whole-book natural-language coverage" not in str(corpus.get("scope", "")):
        error(f"{relative}: bounded-scope disclaimer is missing")
    entries = checked_entries(
        corpus.get("fields"),
        expected_keys={"id", "source", "text"},
        context=f"{relative}.fields",
    )
    expected_chapters = {"CH02", "CH11", "CH17", "CH25"}
    seen_chapters: set[str] = set()
    seen_source_kinds: dict[str, set[str]] = {chapter: set() for chapter in expected_chapters}
    fields_to_scan: list[tuple[str, str]] = []
    for item in entries:
        identifier, source, text = item.get("id"), item.get("source"), item.get("text")
        if not all(isinstance(value, str) for value in (identifier, source, text)):
            error(f"{relative}: representative fields must use string id/source/text")
            continue
        chapter = identifier.split("-", 1)[0]
        if chapter not in expected_chapters:
            error(f"{relative}.{identifier}: unexpected representative chapter")
        else:
            seen_chapters.add(chapter)
            source_kind = source.split("/", 1)[0]
            seen_source_kinds[chapter].add(source_kind)
        source_path = ROOT / source
        try:
            source_text = source_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            error(f"{relative}.{identifier}: cannot read {source}: {exc}")
            continue
        if text not in source_text:
            error(f"{relative}.{identifier}: selected field is not present verbatim in {source}")
        findings = scan_fields([(identifier, text)])
        if findings:
            error(f"{relative}.{identifier}: canonical field produced false positives {findings!r}")
        fields_to_scan.append((identifier, text))
    if seen_chapters != expected_chapters:
        error(f"{relative}: representative chapters {sorted(seen_chapters)!r} incomplete")
    for chapter in expected_chapters:
        required = {"manuscript", "templates", "cases"}
        if not required <= seen_source_kinds[chapter]:
            error(
                f"{relative}: {chapter} source kinds {sorted(seen_source_kinds[chapter])!r} "
                f"do not include {sorted(required)!r}"
            )
    return fields_to_scan


def check_determinism_and_malformed(fields_to_scan: list[tuple[str, str]]) -> None:
    forward = scan_fields(fields_to_scan)
    reverse = scan_fields(reversed(fields_to_scan))
    if forward != reverse:
        error("scan_fields ordering depends on input order")
    if scan_fields(fields_to_scan + fields_to_scan) != forward:
        error("scan_fields does not deduplicate identical findings deterministically")
    if scan_fields(fields_to_scan) != scan_fields(fields_to_scan):
        error("scan_fields repeated execution is not deterministic")

    malformed_cases: list[Any] = [
        "not-a-field-list",
        [("valid-location", 7)],
        [("only-one-element",)],
        [("", "text")],
        [None],
    ]
    for index, malformed in enumerate(malformed_cases):
        findings = scan_fields(malformed)
        if not findings or not all(f.category == "policy.malformed_input" for f in findings):
            error(f"malformed case {index} did not fail closed: {findings!r}")
    if scan_action_text(None, location="bad-action")[0].category != "policy.malformed_input":  # type: ignore[arg-type]
        error("scan_action_text non-string input did not fail closed")
    if scan_host_policy(None, location="bad-host")[0].category != "policy.malformed_input":  # type: ignore[arg-type]
        error("scan_host_policy non-string input did not fail closed")


def check_documentation() -> None:
    required_files = {
        "CONTENT_SAFETY_POLICY.md": (
            "Policy version: `1.0.0`",
            "## Stable API",
            "## Structured policy model",
            "## Normalization contract",
            "## Protected categories",
            "## Host and address policy",
            "`.localhost`は技術的にはreserved",
            "## Versioning and re-audit",
            "patch:",
            "minor:",
            "major:",
            "## Non-goals",
            "自然言語安全性の完全な判定",
        ),
        "CONTENT_SAFETY_POLICY_MIGRATION.md": (
            "PR #57 / Issue #28",
            "9c4f570064372bf8278e0c53cb47709d298e39bb",
            "Issue #59ではPR #57のbranch",
            "Chapter 3固有のART-14",
            "六つのblocker phrase",
            "`.localhost`",
            "unresolved thread 0",
        ),
    }
    for relative, markers in required_files.items():
        try:
            text = (ROOT / relative).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            error(f"{relative}: cannot read policy documentation: {exc}")
            continue
        for marker in markers:
            if marker not in text:
                error(f"{relative}: missing required marker {marker!r}")


def main() -> int:
    check_public_api()
    deterministic_fields = check_action_corpus()
    check_normalization_corpus()
    deterministic_fields.extend(check_host_corpus())
    representative_fields = check_representative_main_fields()
    deterministic_fields.extend(representative_fields)
    check_determinism_and_malformed(deterministic_fields)
    check_documentation()
    if errors:
        for message in errors:
            print(f"ERROR: {message}", file=sys.stderr)
        print(f"content safety policy contract failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(
        "content safety policy contract passed: "
        f"version={POLICY_VERSION}, categories={len(EXPECTED_ALL_CATEGORIES)}, "
        f"blockers={len(BLOCKER_TEXTS)}, representative_fields={len(representative_fields)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
