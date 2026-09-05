#!/usr/bin/env python3
"""Validate the finite Editorial Input portfolio and safely verify raw packages.

The repository manifest is planning metadata. Raw predrafts and ZIP packages remain
outside Git. Candidate selection is always explicit; order, filename, Wave label,
timestamp, and file size are never selection inputs.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import stat
import subprocess
import tempfile
import unicodedata
import warnings
import zipfile
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path, PurePosixPath
from typing import Any, NoReturn

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "editorial-input-manifest.json"
DEFAULT_SCHEMA = ROOT / "schemas" / "editorial-input-manifest.schema.json"
DEFAULT_SUMMARY = ROOT / "EDITORIAL_INPUT_MANIFEST.md"
REGRESSION_CORPUS = (
    ROOT / "tests" / "fixtures" / "editorial-input" / "manifest-regressions.json"
)
REGISTRATION_SNAPSHOT = (
    ROOT / "tests" / "fixtures" / "editorial-input" / "registration-snapshot.json"
)

SCHEMA_VERSION = "1.0.0"
MANIFEST_VERSION = "1.0.0"
PACKAGE_KINDS = {"draft", "mixed", "generator-blueprint"}
FILE_ROLES = {
    "candidate-input",
    "source-review",
    "integration-guide",
    "blueprint-input",
    "generator-blueprint-input",
}
TARGET_KINDS = {"chapter", "appendix", "appendix-group"}
TARGET_STATUSES = {
    "registered-pending-prerequisites",
    "candidate-selection-required",
    "selected-for-intake",
    "rejected-after-comparison",
    "deferred",
    "canonical-pr-open",
    "consumed",
    "blueprint-only",
    "generator-blueprint-only",
    "superseded-with-record",
}
CANDIDATE_DISPOSITIONS = {
    "registered",
    "pending-comparison",
    "selected",
    "adopted",
    "rewritten",
    "rejected",
    "deferred",
    "blueprint-only",
    "generator-blueprint-only",
    "superseded",
}
COLLISION_KINDS = {"filename", "wave-label"}
PRIMARY_INPUT_ROLES = {
    "candidate-input",
    "blueprint-input",
    "generator-blueprint-input",
}
TERMINAL_ALTERNATIVE_DISPOSITIONS = {"rejected", "deferred", "superseded"}
SELECTED_DISPOSITIONS = {"selected", "adopted", "rewritten"}
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
GIT_SHA_RE = re.compile(r"[0-9a-f]{40}\Z")
PACKAGE_ID_RE = re.compile(r"EIP-[0-9]{4}\Z")
TARGET_ID_RE = re.compile(
    r"(?:chapter-[0-9]{2}|appendix-[a-z]|appendices-[a-z](?:-[a-z])+)\Z"
)
CANDIDATE_ID_RE = re.compile(r"EIC-[0-9]{4}-[0-9a-f]{12}\Z")
COLLISION_ID_RE = re.compile(r"EICOLL-[0-9]{4}\Z")
WAVE_LABEL_RE = re.compile(r"(?:initial|wave-[0-9]+)\Z")
HTTPS_GITHUB_RE = re.compile(
    r"https://github\.com/itdojp/white-hat-cyber-intelligence-book/(?:issues|pull)/[0-9]+(?:#issuecomment-[0-9]+)?\Z"
)
MAX_PACKAGE_BYTES = 64 * 1024 * 1024
MAX_MEMBER_BYTES = 16 * 1024 * 1024
MAX_TOTAL_UNCOMPRESSED_BYTES = 64 * 1024 * 1024
SUPPORTED_SCHEMA_KEYWORDS = {
    "$ref",
    "type",
    "const",
    "enum",
    "oneOf",
    "additionalProperties",
    "required",
    "properties",
    "items",
    "minItems",
    "uniqueItems",
    "minLength",
    "pattern",
    "format",
    "minimum",
    "maximum",
    "$schema",
    "$id",
    "title",
    "$defs",
}


class ManifestError(ValueError):
    """A stable fail-closed manifest or package diagnostic."""


class DuplicateKeyError(ManifestError):
    pass


def fail(message: str) -> NoReturn:
    raise ManifestError(message)


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> NoReturn:
    raise ManifestError(f"non-standard JSON number is forbidden: {value}")


def load_json_strict(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_constant,
        )
    except ManifestError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ManifestError(f"{path}: invalid UTF-8 JSON: {exc}") from exc


def require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{label}: expected object")
    return value


def require_list(value: Any, label: str, *, nonempty: bool = False) -> list[Any]:
    if not isinstance(value, list):
        fail(f"{label}: expected array")
    if nonempty and not value:
        fail(f"{label}: expected non-empty array")
    return value


def require_string(value: Any, label: str, *, nonempty: bool = True) -> str:
    if not isinstance(value, str):
        fail(f"{label}: expected string")
    if nonempty and not value.strip():
        fail(f"{label}: expected non-empty string")
    if value != unicodedata.normalize("NFC", value):
        fail(f"{label}: expected Unicode NFC")
    if any(ord(character) < 0x20 or ord(character) == 0x7F for character in value):
        fail(f"{label}: control character is forbidden")
    return value


def require_exact_keys(
    value: dict[str, Any],
    label: str,
    required: set[str],
    optional: set[str] | None = None,
) -> None:
    optional = optional or set()
    missing = required - value.keys()
    extra = value.keys() - required - optional
    if missing:
        fail(f"{label}: missing keys: {', '.join(sorted(missing))}")
    if extra:
        fail(f"{label}: unsupported keys: {', '.join(sorted(extra))}")


def require_pattern(value: Any, label: str, pattern: re.Pattern[str]) -> str:
    text = require_string(value, label)
    if not pattern.fullmatch(text):
        fail(f"{label}: invalid value: {text!r}")
    return text


def require_iso_date(value: Any, label: str) -> str:
    text = require_string(value, label)
    try:
        date.fromisoformat(text)
    except ValueError as exc:
        raise ManifestError(f"{label}: invalid ISO date: {text!r}") from exc
    return text


def require_utc_timestamp(value: Any, label: str) -> str:
    text = require_string(value, label)
    if not text.endswith("Z"):
        fail(f"{label}: expected UTC timestamp ending in Z")
    try:
        datetime.fromisoformat(text.removesuffix("Z") + "+00:00")
    except ValueError as exc:
        raise ManifestError(f"{label}: invalid UTC timestamp: {text!r}") from exc
    return text


def require_issue_url(value: Any, label: str) -> str:
    return require_pattern(value, label, HTTPS_GITHUB_RE)


def require_unique_strings(
    value: Any, label: str, *, nonempty: bool = True
) -> list[str]:
    items = require_list(value, label, nonempty=nonempty)
    strings = [
        require_string(item, f"{label}[{index}]") for index, item in enumerate(items)
    ]
    if len(strings) != len(set(strings)):
        fail(f"{label}: duplicate values")
    return strings


def require_safe_relative_path(value: Any, label: str) -> str:
    text = require_string(value, label)
    if "\\" in text or text.startswith("/") or "//" in text:
        fail(f"{label}: unsafe archive path: {text!r}")
    # PurePosixPath normalizes away ``.`` components.  Inspect the raw path
    # first so two distinct ZIP names cannot collapse to one extraction path.
    raw_parts = text.split("/")
    if any(part in {"", ".", ".."} for part in raw_parts):
        fail(f"{label}: unsafe archive path: {text!r}")
    pure = PurePosixPath(text)
    if not pure.parts:
        fail(f"{label}: unsafe archive path: {text!r}")
    if any(":" in part for part in raw_parts) or any(
        part.startswith(".") for part in raw_parts
    ):
        fail(f"{label}: hidden or drive-qualified archive path: {text!r}")
    return text


def validate_schema_contract(schema: Any) -> None:
    root = require_object(schema, "schema")
    require_exact_keys(
        root,
        "schema",
        {
            "$schema",
            "$id",
            "title",
            "type",
            "additionalProperties",
            "required",
            "properties",
            "$defs",
        },
    )
    if root["$schema"] != "https://json-schema.org/draft/2020-12/schema":
        fail("schema: JSON Schema draft must be 2020-12")
    if root["type"] != "object" or root["additionalProperties"] is not False:
        fail("schema: root must be a closed object")
    properties = require_object(root["properties"], "schema.properties")
    if properties.get("schemaVersion", {}).get("const") != SCHEMA_VERSION:
        fail("schema: schemaVersion const drift")
    if properties.get("manifestVersion", {}).get("const") != MANIFEST_VERSION:
        fail("schema: manifestVersion const drift")
    defs = require_object(root["$defs"], "schema.$defs")
    enum_pairs = {
        "packageKind": PACKAGE_KINDS,
        "fileRole": FILE_ROLES,
        "targetKind": TARGET_KINDS,
        "targetStatus": TARGET_STATUSES,
        "candidateDisposition": CANDIDATE_DISPOSITIONS,
        "collisionKind": COLLISION_KINDS,
    }
    for name, expected in enum_pairs.items():
        actual = set(
            require_list(
                require_object(defs.get(name), f"schema.$defs.{name}").get("enum"),
                f"schema.$defs.{name}.enum",
            )
        )
        if actual != expected:
            fail(f"schema: {name} enum drift: {sorted(actual ^ expected)}")
    validate_supported_schema_nodes(root, "schema")


def validate_supported_schema_nodes(raw_schema: Any, label: str) -> None:
    node = require_object(raw_schema, label)
    unsupported = node.keys() - SUPPORTED_SCHEMA_KEYWORDS
    if unsupported:
        fail(f"{label}: unsupported JSON Schema keywords: {sorted(unsupported)!r}")
    if "$ref" in node and len(node) != 1:
        fail(f"{label}: sibling keywords beside $ref are unsupported")
    for container_name in ("properties", "$defs"):
        if container_name not in node:
            continue
        container = require_object(node[container_name], f"{label}.{container_name}")
        for name, child in container.items():
            validate_supported_schema_nodes(child, f"{label}.{container_name}.{name}")
    if "items" in node:
        validate_supported_schema_nodes(node["items"], f"{label}.items")
    if "oneOf" in node:
        for index, child in enumerate(
            require_list(node["oneOf"], f"{label}.oneOf", nonempty=True)
        ):
            validate_supported_schema_nodes(child, f"{label}.oneOf[{index}]")


def resolve_local_schema_ref(root: dict[str, Any], reference: Any, label: str) -> Any:
    ref = require_string(reference, f"{label}.$ref")
    prefix = "#/$defs/"
    if not ref.startswith(prefix) or "/" in ref.removeprefix(prefix):
        fail(f"{label}.$ref: only direct local $defs references are supported")
    name = ref.removeprefix(prefix)
    definitions = require_object(root.get("$defs"), "schema.$defs")
    if name not in definitions:
        fail(f"{label}.$ref: unknown definition: {name}")
    return definitions[name]


def schema_type_matches(value: Any, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    fail(f"schema.type: unsupported JSON Schema type: {expected!r}")


def validate_schema_instance_node(
    value: Any,
    raw_schema: Any,
    root: dict[str, Any],
    instance_label: str,
    schema_label: str,
) -> None:
    node = require_object(raw_schema, schema_label)
    unsupported = node.keys() - SUPPORTED_SCHEMA_KEYWORDS
    if unsupported:
        fail(
            f"{schema_label}: unsupported JSON Schema keywords: {sorted(unsupported)!r}"
        )
    if "$ref" in node:
        if len(node) != 1:
            fail(f"{schema_label}: sibling keywords beside $ref are unsupported")
        validate_schema_instance_node(
            value,
            resolve_local_schema_ref(root, node["$ref"], schema_label),
            root,
            instance_label,
            f"{schema_label}.$ref",
        )
        return
    if "oneOf" in node:
        alternatives = require_list(
            node["oneOf"], f"{schema_label}.oneOf", nonempty=True
        )
        matches = 0
        for index, alternative in enumerate(alternatives):
            try:
                validate_schema_instance_node(
                    value,
                    alternative,
                    root,
                    instance_label,
                    f"{schema_label}.oneOf[{index}]",
                )
            except ManifestError:
                continue
            matches += 1
        if matches != 1:
            fail(f"{instance_label}: JSON Schema oneOf matched {matches} branches")
        return
    if "const" in node and value != node["const"]:
        fail(f"{instance_label}: JSON Schema const mismatch")
    if "enum" in node:
        choices = require_list(node["enum"], f"{schema_label}.enum", nonempty=True)
        if value not in choices:
            fail(f"{instance_label}: JSON Schema enum mismatch")
    if "type" in node:
        raw_types = node["type"]
        types = raw_types if isinstance(raw_types, list) else [raw_types]
        if not types or not all(isinstance(item, str) for item in types):
            fail(f"{schema_label}.type: expected a type or non-empty type array")
        if not any(schema_type_matches(value, item) for item in types):
            fail(f"{instance_label}: JSON Schema type mismatch; expected {types!r}")
    if isinstance(value, dict):
        required = node.get("required", [])
        required_keys = require_unique_strings(
            required, f"{schema_label}.required", nonempty=False
        )
        missing = set(required_keys) - value.keys()
        if missing:
            fail(f"{instance_label}: JSON Schema missing keys: {sorted(missing)!r}")
        properties = require_object(
            node.get("properties", {}), f"{schema_label}.properties"
        )
        for key, item in value.items():
            if key in properties:
                validate_schema_instance_node(
                    item,
                    properties[key],
                    root,
                    f"{instance_label}.{key}",
                    f"{schema_label}.properties.{key}",
                )
            elif node.get("additionalProperties") is False:
                fail(f"{instance_label}: JSON Schema additional property: {key}")
    if isinstance(value, list):
        minimum_items = node.get("minItems")
        if minimum_items is not None and len(value) < minimum_items:
            fail(f"{instance_label}: JSON Schema minItems violation")
        if node.get("uniqueItems") is True:
            serialized = [
                json.dumps(
                    item, ensure_ascii=False, sort_keys=True, separators=(",", ":")
                )
                for item in value
            ]
            if len(serialized) != len(set(serialized)):
                fail(f"{instance_label}: JSON Schema uniqueItems violation")
        if "items" in node:
            for index, item in enumerate(value):
                validate_schema_instance_node(
                    item,
                    node["items"],
                    root,
                    f"{instance_label}[{index}]",
                    f"{schema_label}.items",
                )
    if isinstance(value, str):
        minimum_length = node.get("minLength")
        if minimum_length is not None and len(value) < minimum_length:
            fail(f"{instance_label}: JSON Schema minLength violation")
        if "pattern" in node:
            pattern = require_string(node["pattern"], f"{schema_label}.pattern")
            try:
                matched = re.search(pattern, value) is not None
            except re.error as exc:
                raise ManifestError(
                    f"{schema_label}.pattern: invalid regex: {exc}"
                ) from exc
            if not matched:
                fail(f"{instance_label}: JSON Schema pattern mismatch")
        format_name = node.get("format")
        if format_name == "date":
            require_iso_date(value, instance_label)
        elif format_name == "date-time":
            require_utc_timestamp(value, instance_label)
        elif format_name is not None:
            fail(f"{schema_label}.format: unsupported format: {format_name!r}")
    if isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in node and value < node["minimum"]:
            fail(f"{instance_label}: JSON Schema minimum violation")
        if "maximum" in node and value > node["maximum"]:
            fail(f"{instance_label}: JSON Schema maximum violation")


def validate_schema_instance(data: Any, schema: Any) -> None:
    root = require_object(schema, "schema")
    validate_schema_instance_node(data, root, root, "manifest", "schema")


def validate_source(value: Any) -> None:
    source = require_object(value, "source")
    require_exact_keys(
        source,
        "source",
        {
            "repository",
            "registrationIssue",
            "contractIssue",
            "registrationIssueSnapshotUpdatedAt",
            "contractIssueSnapshotUpdatedAt",
            "scope",
        },
    )
    if (
        source["repository"]
        != "https://github.com/itdojp/white-hat-cyber-intelligence-book"
    ):
        fail("source.repository: unexpected repository")
    if source["registrationIssue"] != 63 or source["contractIssue"] != 98:
        fail("source: owning issues must remain #63 and #98")
    require_utc_timestamp(
        source["registrationIssueSnapshotUpdatedAt"],
        "source.registrationIssueSnapshotUpdatedAt",
    )
    require_utc_timestamp(
        source["contractIssueSnapshotUpdatedAt"],
        "source.contractIssueSnapshotUpdatedAt",
    )
    require_string(source["scope"], "source.scope")


def validate_external_artifact(value: Any) -> None:
    artifact = require_object(value, "externalAuditArtifact")
    require_exact_keys(
        artifact,
        "externalAuditArtifact",
        {
            "availability",
            "package",
            "packageSha256",
            "manifest",
            "manifestSha256",
            "audit",
            "auditSha256",
            "goal",
            "goalSha256",
            "provenanceUrl",
            "note",
        },
    )
    if artifact["availability"] != "not-present-in-authorized-workspace":
        fail(
            "externalAuditArtifact.availability: local copy was not available for this audit"
        )
    for field in ("package", "manifest", "audit", "goal", "note"):
        require_string(artifact[field], f"externalAuditArtifact.{field}")
    for field in ("packageSha256", "manifestSha256", "auditSha256", "goalSha256"):
        require_pattern(artifact[field], f"externalAuditArtifact.{field}", SHA256_RE)
    require_issue_url(artifact["provenanceUrl"], "externalAuditArtifact.provenanceUrl")


def validate_packages(
    packages_raw: Any,
) -> tuple[dict[str, dict[str, Any]], dict[tuple[str, str], dict[str, Any]]]:
    packages = require_list(packages_raw, "packages", nonempty=True)
    by_id: dict[str, dict[str, Any]] = {}
    files_by_package_path: dict[tuple[str, str], dict[str, Any]] = {}
    sha_owners: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    for index, raw in enumerate(packages):
        label = f"packages[{index}]"
        package = require_object(raw, label)
        require_exact_keys(
            package,
            label,
            {
                "packageId",
                "filename",
                "sha256",
                "packageKind",
                "waveLabel",
                "registeredAt",
                "registrationUrl",
                "files",
            },
            {"aliasOf"},
        )
        package_id = require_pattern(
            package["packageId"], f"{label}.packageId", PACKAGE_ID_RE
        )
        if package_id in by_id:
            fail(f"packages: duplicate packageId: {package_id}")
        by_id[package_id] = package
        filename = require_string(package["filename"], f"{label}.filename")
        if PurePosixPath(filename).name != filename or not filename.endswith(".zip"):
            fail(f"{label}.filename: expected basename ending in .zip")
        sha = require_pattern(package["sha256"], f"{label}.sha256", SHA256_RE)
        sha_owners[sha].append(package)
        if package["packageKind"] not in PACKAGE_KINDS:
            fail(f"{label}.packageKind: unsupported value")
        require_pattern(package["waveLabel"], f"{label}.waveLabel", WAVE_LABEL_RE)
        require_iso_date(package["registeredAt"], f"{label}.registeredAt")
        require_issue_url(package["registrationUrl"], f"{label}.registrationUrl")
        if "aliasOf" in package:
            require_pattern(package["aliasOf"], f"{label}.aliasOf", PACKAGE_ID_RE)
            if package["aliasOf"] == package_id:
                fail(f"{label}.aliasOf: package cannot alias itself")
        seen_paths: set[str] = set()
        for file_index, raw_file in enumerate(
            require_list(package["files"], f"{label}.files", nonempty=True)
        ):
            file_label = f"{label}.files[{file_index}]"
            item = require_object(raw_file, file_label)
            require_exact_keys(item, file_label, {"path", "sha256", "role", "targets"})
            path = require_safe_relative_path(item["path"], f"{file_label}.path")
            if path in seen_paths:
                fail(f"{label}.files: duplicate path: {path}")
            seen_paths.add(path)
            require_pattern(item["sha256"], f"{file_label}.sha256", SHA256_RE)
            if item["role"] not in FILE_ROLES:
                fail(f"{file_label}.role: unsupported value")
            targets = require_unique_strings(item["targets"], f"{file_label}.targets")
            for target in targets:
                require_pattern(target, f"{file_label}.targets", TARGET_ID_RE)
            files_by_package_path[(package_id, path)] = item
    for sha, owners in sha_owners.items():
        if len(owners) == 1:
            if "aliasOf" in owners[0]:
                fail(
                    f"packages: aliasOf has no same-SHA canonical package: {owners[0]['packageId']}"
                )
            continue
        canonical = [item for item in owners if "aliasOf" not in item]
        if len(canonical) != 1:
            fail(
                f"packages: duplicate package SHA requires exactly one canonical owner: {sha}"
            )
        canonical_id = canonical[0]["packageId"]
        for item in owners:
            if item is canonical[0]:
                continue
            if item.get("aliasOf") != canonical_id:
                fail(
                    f"packages: duplicate SHA alias must reference {canonical_id}: {item['packageId']}"
                )
    for package in packages:
        alias = package.get("aliasOf")
        if alias:
            owner = by_id.get(alias)
            if owner is None or owner["sha256"] != package["sha256"]:
                fail(
                    f"packages: invalid aliasOf relation: {package['packageId']} -> {alias}"
                )
    return by_id, files_by_package_path


def computed_collisions(
    packages: dict[str, dict[str, Any]],
) -> dict[tuple[str, str], list[str]]:
    output: dict[tuple[str, str], list[str]] = {}
    for kind, field in (("filename", "filename"), ("wave-label", "waveLabel")):
        groups: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
        for package in packages.values():
            if "aliasOf" not in package:
                groups[package[field]].append(package)
        for value, items in groups.items():
            distinct_hashes = {item["sha256"] for item in items}
            if len(items) > 1 and (kind == "wave-label" or len(distinct_hashes) > 1):
                output[(kind, value)] = sorted(item["packageId"] for item in items)
    return output


def validate_collision_acknowledgements(
    value: Any, packages: dict[str, dict[str, Any]]
) -> None:
    acknowledgements = require_list(value, "collisionAcknowledgements")
    actual: dict[tuple[str, str], list[str]] = {}
    ids: set[str] = set()
    for index, raw in enumerate(acknowledgements):
        label = f"collisionAcknowledgements[{index}]"
        item = require_object(raw, label)
        require_exact_keys(
            item,
            label,
            {"collisionId", "kind", "value", "packageIds", "evidenceUrl", "reason"},
        )
        collision_id = require_pattern(
            item["collisionId"], f"{label}.collisionId", COLLISION_ID_RE
        )
        if collision_id in ids:
            fail(f"collisionAcknowledgements: duplicate collisionId: {collision_id}")
        ids.add(collision_id)
        kind = item["kind"]
        if kind not in COLLISION_KINDS:
            fail(f"{label}.kind: unsupported value")
        collision_value = require_string(item["value"], f"{label}.value")
        package_ids = require_unique_strings(item["packageIds"], f"{label}.packageIds")
        if package_ids != sorted(package_ids):
            fail(f"{label}.packageIds: expected deterministic sorted order")
        for package_id in package_ids:
            if package_id not in packages:
                fail(f"{label}.packageIds: unknown packageId: {package_id}")
        key = (kind, collision_value)
        if key in actual:
            fail(
                f"collisionAcknowledgements: duplicate acknowledgement: {kind} {collision_value!r}"
            )
        actual[key] = package_ids
        require_issue_url(item["evidenceUrl"], f"{label}.evidenceUrl")
        require_string(item["reason"], f"{label}.reason")
    expected = computed_collisions(packages)
    missing = expected.keys() - actual.keys()
    extra = actual.keys() - expected.keys()
    if missing:
        fail(
            f"collisionAcknowledgements: missing collision records: {sorted(missing)!r}"
        )
    if extra:
        fail(f"collisionAcknowledgements: stale collision records: {sorted(extra)!r}")
    for key in expected:
        if actual[key] != expected[key]:
            fail(f"collisionAcknowledgements: package set mismatch for {key!r}")


def validate_status_history(
    value: Any, target_label: str, current_status: str, expected_initial_status: str
) -> None:
    history_items = require_list(value, f"{target_label}.statusHistory", nonempty=True)
    previous_date: str | None = None
    previous_status: str | None = None
    allowed_transitions = {
        "registered-pending-prerequisites": {
            "candidate-selection-required",
            "selected-for-intake",
            "rejected-after-comparison",
            "deferred",
            "canonical-pr-open",
            "blueprint-only",
            "generator-blueprint-only",
            "superseded-with-record",
        },
        "candidate-selection-required": {
            "selected-for-intake",
            "rejected-after-comparison",
            "deferred",
        },
        "selected-for-intake": {
            "canonical-pr-open",
            "deferred",
            "superseded-with-record",
        },
        "canonical-pr-open": {"consumed", "deferred", "superseded-with-record"},
        "deferred": {
            "candidate-selection-required",
            "selected-for-intake",
            "superseded-with-record",
        },
        "blueprint-only": {
            "selected-for-intake",
            "canonical-pr-open",
            "deferred",
            "superseded-with-record",
        },
        "generator-blueprint-only": {
            "selected-for-intake",
            "canonical-pr-open",
            "deferred",
            "superseded-with-record",
        },
    }
    for index, raw in enumerate(history_items):
        label = f"{target_label}.statusHistory[{index}]"
        item = require_object(raw, label)
        require_exact_keys(
            item, label, {"status", "effectiveAt", "evidenceUrl", "reason"}
        )
        status_value = item["status"]
        if status_value not in TARGET_STATUSES:
            fail(f"{label}.status: unsupported value")
        effective = require_iso_date(item["effectiveAt"], f"{label}.effectiveAt")
        require_issue_url(item["evidenceUrl"], f"{label}.evidenceUrl")
        require_string(item["reason"], f"{label}.reason")
        if previous_date and effective < previous_date:
            fail(f"{target_label}.statusHistory: effectiveAt order is not monotonic")
        if previous_status:
            if status_value == previous_status:
                fail(
                    f"{target_label}.statusHistory: duplicate adjacent status: {status_value}"
                )
            if status_value not in allowed_transitions.get(previous_status, set()):
                fail(
                    f"{target_label}.statusHistory: invalid transition {previous_status} -> {status_value}"
                )
        previous_date = effective
        previous_status = status_value
    if history_items[0]["status"] != expected_initial_status:
        fail(
            f"{target_label}.statusHistory: expected immutable initial status "
            f"{expected_initial_status}"
        )
    if previous_status != current_status:
        fail(
            f"{target_label}.statusHistory: final status does not match current status"
        )


def validate_intake_record(
    value: Any,
    target_label: str,
    target: dict[str, Any],
    selected: dict[str, Any],
    package: dict[str, Any],
) -> None:
    record = require_object(value, f"{target_label}.intakeRecord")
    required = {
        "recordVersion",
        "recordUrl",
        "packageId",
        "packageSha256",
        "inputPath",
        "inputSha256",
        "targetIssue",
        "canonicalPr",
        "currentMainSha",
        "policyVersion",
        "publicationProjectionVersion",
        "inputReviewedAt",
        "adoptedSections",
        "rewrittenSections",
        "rejectedOrDeferredSections",
        "sourceRevalidation",
        "canonicalFiles",
        "knownLimitations",
        "rawTrackedFiles",
    }
    require_exact_keys(record, f"{target_label}.intakeRecord", required)
    version = require_string(
        record["recordVersion"], f"{target_label}.intakeRecord.recordVersion"
    )
    if version not in {"1.0.0", "legacy-issue-1"}:
        fail(f"{target_label}.intakeRecord.recordVersion: unsupported version")
    record_url = require_issue_url(
        record["recordUrl"], f"{target_label}.intakeRecord.recordUrl"
    )
    expected_record_url = (
        "https://github.com/itdojp/white-hat-cyber-intelligence-book/pull/"
        f"{target['canonicalPr']}"
    )
    if record_url != expected_record_url:
        fail(f"{target_label}.intakeRecord.recordUrl: expected {expected_record_url!r}")
    mirror = {
        "packageId": selected["packageId"],
        "packageSha256": package["sha256"],
        "inputPath": selected["inputPath"],
        "inputSha256": selected["inputSha256"],
        "targetIssue": target["issue"],
        "canonicalPr": target["canonicalPr"],
    }
    for field, expected in mirror.items():
        if record[field] != expected:
            fail(f"{target_label}.intakeRecord.{field}: expected {expected!r}")
    require_pattern(
        record["currentMainSha"],
        f"{target_label}.intakeRecord.currentMainSha",
        GIT_SHA_RE,
    )
    if record["policyVersion"] != "1.2.0":
        fail(f"{target_label}.intakeRecord.policyVersion: expected 1.2.0")
    projection = record["publicationProjectionVersion"]
    if version == "1.0.0":
        if projection != "1.1.0":
            fail(
                f"{target_label}.intakeRecord.publicationProjectionVersion: expected 1.1.0"
            )
    else:
        if (
            target["targetId"] != "chapter-04"
            or target["canonicalPr"] != 64
            or selected["candidateId"] != "EIC-0029-c49f0a11ef9e"
        ):
            fail(
                f"{target_label}.intakeRecord.recordVersion: legacy exception is limited "
                "to Chapter 4 / PR #64"
            )
        if projection is not None:
            fail(
                f"{target_label}.intakeRecord.publicationProjectionVersion: legacy record must use null"
            )
    require_iso_date(
        record["inputReviewedAt"], f"{target_label}.intakeRecord.inputReviewedAt"
    )
    for field in (
        "adoptedSections",
        "rewrittenSections",
        "rejectedOrDeferredSections",
        "sourceRevalidation",
        "canonicalFiles",
        "knownLimitations",
    ):
        values = require_unique_strings(
            record[field], f"{target_label}.intakeRecord.{field}"
        )
        if field == "canonicalFiles":
            for index, path in enumerate(values):
                safe = require_safe_relative_path(
                    path, f"{target_label}.intakeRecord.canonicalFiles[{index}]"
                )
                if not (ROOT / safe).is_file():
                    fail(
                        f"{target_label}.intakeRecord.canonicalFiles: missing repository file: {safe}"
                    )
    if not isinstance(record["rawTrackedFiles"], int) or isinstance(
        record["rawTrackedFiles"], bool
    ):
        fail(f"{target_label}.intakeRecord.rawTrackedFiles: expected integer")
    if record["rawTrackedFiles"] != 0:
        fail(f"{target_label}.intakeRecord.rawTrackedFiles: expected 0")


def validate_targets(
    targets_raw: Any,
    packages: dict[str, dict[str, Any]],
    files: dict[tuple[str, str], dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    targets = require_list(targets_raw, "targets", nonempty=True)
    by_id: dict[str, dict[str, Any]] = {}
    candidate_ids: set[str] = set()
    candidate_file_targets: set[tuple[str, str, str]] = set()
    for index, raw in enumerate(targets):
        label = f"targets[{index}]"
        target = require_object(raw, label)
        require_exact_keys(
            target,
            label,
            {
                "targetId",
                "issue",
                "targetKind",
                "status",
                "selectedCandidateId",
                "canonicalPr",
                "intakeRecord",
                "candidates",
                "statusHistory",
            },
        )
        target_id = require_pattern(
            target["targetId"], f"{label}.targetId", TARGET_ID_RE
        )
        if target_id in by_id:
            fail(f"targets: duplicate targetId: {target_id}")
        by_id[target_id] = target
        issue = target["issue"]
        if (
            not isinstance(issue, int)
            or isinstance(issue, bool)
            or not 1 <= issue <= 9999
        ):
            fail(f"{label}.issue: expected positive integer")
        if target["targetKind"] not in TARGET_KINDS:
            fail(f"{label}.targetKind: unsupported value")
        status_value = target["status"]
        if status_value not in TARGET_STATUSES:
            fail(f"{label}.status: unsupported value")
        selected_id = target["selectedCandidateId"]
        if selected_id is not None:
            require_pattern(
                selected_id, f"{label}.selectedCandidateId", CANDIDATE_ID_RE
            )
        canonical_pr = target["canonicalPr"]
        if canonical_pr is not None and (
            not isinstance(canonical_pr, int)
            or isinstance(canonical_pr, bool)
            or canonical_pr < 1
        ):
            fail(f"{label}.canonicalPr: expected positive integer or null")
        candidates: list[dict[str, Any]] = []
        for candidate_index, raw_candidate in enumerate(
            require_list(target["candidates"], f"{label}.candidates", nonempty=True)
        ):
            candidate_label = f"{label}.candidates[{candidate_index}]"
            candidate = require_object(raw_candidate, candidate_label)
            require_exact_keys(
                candidate,
                candidate_label,
                {
                    "candidateId",
                    "packageId",
                    "inputPath",
                    "inputSha256",
                    "disposition",
                    "dispositionEvidenceUrl",
                    "dispositionReason",
                },
            )
            candidate_id = require_pattern(
                candidate["candidateId"],
                f"{candidate_label}.candidateId",
                CANDIDATE_ID_RE,
            )
            expected_prefix = f"EIC-{issue:04d}-"
            if not candidate_id.startswith(expected_prefix):
                fail(f"{candidate_label}.candidateId: target issue prefix mismatch")
            if candidate_id in candidate_ids:
                fail(f"targets: duplicate candidateId: {candidate_id}")
            candidate_ids.add(candidate_id)
            package_id = require_pattern(
                candidate["packageId"], f"{candidate_label}.packageId", PACKAGE_ID_RE
            )
            package = packages.get(package_id)
            if package is None:
                fail(f"{candidate_label}.packageId: unknown package: {package_id}")
            input_path = require_safe_relative_path(
                candidate["inputPath"], f"{candidate_label}.inputPath"
            )
            input_sha = require_pattern(
                candidate["inputSha256"], f"{candidate_label}.inputSha256", SHA256_RE
            )
            expected_id = f"EIC-{issue:04d}-{input_sha[:12]}"
            if candidate_id != expected_id:
                fail(f"{candidate_label}.candidateId: expected {expected_id}")
            package_file = files.get((package_id, input_path))
            if package_file is None:
                fail(f"{candidate_label}: package file is not registered")
            if package_file["sha256"] != input_sha:
                fail(f"{candidate_label}.inputSha256: package file hash mismatch")
            if package_file["role"] not in PRIMARY_INPUT_ROLES:
                fail(
                    f"{candidate_label}.inputPath: package file is not a candidate/blueprint input"
                )
            if target_id not in package_file["targets"]:
                fail(f"{candidate_label}: package file does not own target {target_id}")
            key = (package_id, input_path, target_id)
            if key in candidate_file_targets:
                fail(f"{candidate_label}: duplicate package/input/target candidate")
            candidate_file_targets.add(key)
            if candidate["disposition"] not in CANDIDATE_DISPOSITIONS:
                fail(f"{candidate_label}.disposition: unsupported value")
            require_issue_url(
                candidate["dispositionEvidenceUrl"],
                f"{candidate_label}.dispositionEvidenceUrl",
            )
            require_string(
                candidate["dispositionReason"], f"{candidate_label}.dispositionReason"
            )
            candidates.append(candidate)
        candidates_by_id = {item["candidateId"]: item for item in candidates}
        if selected_id is not None and selected_id not in candidates_by_id:
            fail(f"{label}.selectedCandidateId: unknown candidate")
        selected_candidate = candidates_by_id.get(selected_id) if selected_id else None
        dispositions = [item["disposition"] for item in candidates]
        if status_value == "registered-pending-prerequisites":
            if (
                len(candidates) != 1
                or dispositions != ["registered"]
                or any(
                    item is not None
                    for item in (selected_id, canonical_pr, target["intakeRecord"])
                )
            ):
                fail(
                    f"{label}: registered target must have one unselected registered candidate"
                )
        elif status_value == "candidate-selection-required":
            if (
                len(candidates) < 2
                or selected_id is not None
                or canonical_pr is not None
                or target["intakeRecord"] is not None
            ):
                fail(
                    f"{label}: candidate-selection-required must keep multiple candidates unselected"
                )
            if sum(item == "pending-comparison" for item in dispositions) < 2:
                fail(
                    f"{label}: candidate-selection-required needs at least two pending comparisons"
                )
        elif status_value == "selected-for-intake":
            if (
                selected_candidate is None
                or selected_candidate["disposition"] != "selected"
            ):
                fail(
                    f"{label}: selected-for-intake requires one explicit selected candidate"
                )
            if canonical_pr is not None or target["intakeRecord"] is not None:
                fail(
                    f"{label}: selected-for-intake must not claim a canonical PR/record"
                )
            for item in candidates:
                if item is selected_candidate:
                    continue
                if item["disposition"] not in TERMINAL_ALTERNATIVE_DISPOSITIONS:
                    fail(
                        f"{label}: selected candidate alternative disposition is missing"
                    )
        elif status_value == "canonical-pr-open":
            if (
                selected_candidate is None
                or selected_candidate["disposition"] not in SELECTED_DISPOSITIONS
            ):
                fail(
                    f"{label}: canonical-pr-open requires an explicit selected candidate"
                )
            if canonical_pr is None or target["intakeRecord"] is None:
                fail(
                    f"{label}: canonical-pr-open requires canonicalPr and Intake Record"
                )
            for item in candidates:
                if (
                    item is not selected_candidate
                    and item["disposition"] not in TERMINAL_ALTERNATIVE_DISPOSITIONS
                ):
                    fail(
                        f"{label}: selected candidate alternative disposition is missing"
                    )
        elif status_value == "consumed":
            if selected_candidate is None or selected_candidate["disposition"] not in {
                "adopted",
                "rewritten",
            }:
                fail(
                    f"{label}: consumed requires an adopted or rewritten selected candidate"
                )
            if canonical_pr is None or target["intakeRecord"] is None:
                fail(f"{label}: consumed requires canonicalPr and Intake Record")
            for item in candidates:
                if (
                    item is not selected_candidate
                    and item["disposition"] not in TERMINAL_ALTERNATIVE_DISPOSITIONS
                ):
                    fail(f"{label}: consumed target alternative disposition is missing")
        elif status_value == "rejected-after-comparison":
            if (
                selected_id is not None
                or canonical_pr is not None
                or target["intakeRecord"] is not None
                or set(dispositions) != {"rejected"}
            ):
                fail(f"{label}: rejected-after-comparison must reject every candidate")
        elif status_value == "deferred":
            if (
                selected_id is not None
                or canonical_pr is not None
                or target["intakeRecord"] is not None
                or set(dispositions) != {"deferred"}
            ):
                fail(f"{label}: deferred target must defer every candidate")
        elif status_value == "blueprint-only":
            if (
                selected_id is not None
                or canonical_pr is not None
                or target["intakeRecord"] is not None
                or set(dispositions) != {"blueprint-only"}
            ):
                fail(f"{label}: blueprint-only target shape mismatch")
            if any(
                files[(item["packageId"], item["inputPath"])]["role"]
                != "blueprint-input"
                for item in candidates
            ):
                fail(
                    f"{label}: blueprint-only target must reference blueprint-input files"
                )
        elif status_value == "generator-blueprint-only":
            if (
                selected_id is not None
                or canonical_pr is not None
                or target["intakeRecord"] is not None
                or set(dispositions) != {"generator-blueprint-only"}
            ):
                fail(f"{label}: generator-blueprint-only target shape mismatch")
            if any(
                files[(item["packageId"], item["inputPath"])]["role"]
                != "generator-blueprint-input"
                for item in candidates
            ):
                fail(
                    f"{label}: generator-blueprint-only target must reference generator-blueprint-input files"
                )
        elif status_value == "superseded-with-record":
            if (
                selected_id is not None
                or canonical_pr is not None
                or target["intakeRecord"] is not None
                or set(dispositions) != {"superseded"}
            ):
                fail(f"{label}: superseded-with-record must supersede every candidate")
        candidate_roles = {
            files[(item["packageId"], item["inputPath"])]["role"] for item in candidates
        }
        if candidate_roles == {"blueprint-input"}:
            initial_status = "blueprint-only"
        elif candidate_roles == {"generator-blueprint-input"}:
            initial_status = "generator-blueprint-only"
        else:
            initial_status = "registered-pending-prerequisites"
        validate_status_history(
            target["statusHistory"], label, status_value, initial_status
        )
        if status_value in {"canonical-pr-open", "consumed"}:
            assert selected_candidate is not None
            validate_intake_record(
                target["intakeRecord"],
                label,
                target,
                selected_candidate,
                packages[selected_candidate["packageId"]],
            )
    # Every target declared by a package exists. Every primary input target has exactly one candidate edge.
    for (package_id, path), item in files.items():
        for target_id in item["targets"]:
            if target_id not in by_id:
                fail(
                    f"packages: {package_id}/{path} references unknown target {target_id}"
                )
            if (
                item["role"] in PRIMARY_INPUT_ROLES
                and (package_id, path, target_id) not in candidate_file_targets
            ):
                fail(
                    f"packages: unowned primary input: {package_id}/{path} -> {target_id}"
                )
    return by_id


def validate_manifest(data: Any, schema: Any | None = None) -> dict[str, Any]:
    manifest = require_object(data, "manifest")
    require_exact_keys(
        manifest,
        "manifest",
        {
            "schemaVersion",
            "manifestVersion",
            "auditedAt",
            "source",
            "externalAuditArtifact",
            "collisionAcknowledgements",
            "packages",
            "targets",
        },
    )
    if manifest["schemaVersion"] != SCHEMA_VERSION:
        fail(f"manifest.schemaVersion: expected {SCHEMA_VERSION}")
    if manifest["manifestVersion"] != MANIFEST_VERSION:
        fail(f"manifest.manifestVersion: expected {MANIFEST_VERSION}")
    require_iso_date(manifest["auditedAt"], "manifest.auditedAt")
    validate_source(manifest["source"])
    validate_external_artifact(manifest["externalAuditArtifact"])
    packages, files = validate_packages(manifest["packages"])
    validate_collision_acknowledgements(manifest["collisionAcknowledgements"], packages)
    validate_targets(manifest["targets"], packages, files)
    if schema is not None:
        validate_schema_contract(schema)
        validate_schema_instance(manifest, schema)
    return manifest


def registration_projection(manifest: dict[str, Any]) -> dict[str, Any]:
    output: list[dict[str, Any]] = []
    for package in sorted(manifest["packages"], key=lambda item: item["packageId"]):
        files = [
            {
                "path": item["path"],
                "sha256": item["sha256"],
                "role": item["role"],
                "targets": sorted(item["targets"]),
            }
            for item in package["files"]
        ]
        output.append(
            {
                "packageId": package["packageId"],
                "filename": package["filename"],
                "packageSha256": package["sha256"],
                "packageKind": package["packageKind"],
                "waveLabel": package["waveLabel"],
                "registeredAt": package["registeredAt"],
                "registrationUrl": package["registrationUrl"],
                "files": sorted(
                    files,
                    key=lambda item: (item["path"], item["sha256"], item["role"]),
                ),
            }
        )
    targets = sorted(
        (
            {
                "targetId": target["targetId"],
                "issue": target["issue"],
                "targetKind": target["targetKind"],
            }
            for target in manifest["targets"]
        ),
        key=lambda item: item["targetId"],
    )
    return {"packages": output, "targets": targets}


def validate_registration_snapshot(manifest: dict[str, Any], value: Any) -> None:
    snapshot = require_object(value, "registration snapshot")
    require_exact_keys(
        snapshot,
        "registration snapshot",
        {
            "schemaVersion",
            "capturedAt",
            "registrationIssue",
            "registrationIssueSnapshotUpdatedAt",
            "packages",
            "targets",
        },
    )
    if snapshot["schemaVersion"] != "1.0.0":
        fail("registration snapshot: unexpected schemaVersion")
    require_iso_date(snapshot["capturedAt"], "registration snapshot.capturedAt")
    if snapshot["registrationIssue"] != 63:
        fail("registration snapshot: registrationIssue must remain #63")
    timestamp = require_utc_timestamp(
        snapshot["registrationIssueSnapshotUpdatedAt"],
        "registration snapshot.registrationIssueSnapshotUpdatedAt",
    )
    if timestamp != manifest["source"]["registrationIssueSnapshotUpdatedAt"]:
        fail("registration snapshot: Issue #63 snapshot timestamp drift")
    packages = require_list(
        snapshot["packages"], "registration snapshot.packages", nonempty=True
    )
    normalized: list[dict[str, Any]] = []
    for index, raw in enumerate(packages):
        label = f"registration snapshot.packages[{index}]"
        package = require_object(raw, label)
        require_exact_keys(
            package,
            label,
            {
                "packageId",
                "filename",
                "packageSha256",
                "packageKind",
                "waveLabel",
                "registeredAt",
                "registrationUrl",
                "files",
            },
        )
        package_id = require_pattern(
            package["packageId"], f"{label}.packageId", PACKAGE_ID_RE
        )
        filename = require_string(package["filename"], f"{label}.filename")
        package_sha = require_pattern(
            package["packageSha256"], f"{label}.packageSha256", SHA256_RE
        )
        package_kind = require_string(package["packageKind"], f"{label}.packageKind")
        if package_kind not in PACKAGE_KINDS:
            fail(f"{label}.packageKind: unsupported value")
        wave_label = require_pattern(
            package["waveLabel"], f"{label}.waveLabel", WAVE_LABEL_RE
        )
        registered_at = require_iso_date(
            package["registeredAt"], f"{label}.registeredAt"
        )
        registration_url = require_issue_url(
            package["registrationUrl"], f"{label}.registrationUrl"
        )
        files: list[dict[str, Any]] = []
        for file_index, raw_file in enumerate(
            require_list(package["files"], f"{label}.files", nonempty=True)
        ):
            file_label = f"{label}.files[{file_index}]"
            item = require_object(raw_file, file_label)
            require_exact_keys(item, file_label, {"path", "sha256", "role", "targets"})
            path = require_safe_relative_path(item["path"], f"{file_label}.path")
            file_sha = require_pattern(
                item["sha256"], f"{file_label}.sha256", SHA256_RE
            )
            role = require_string(item["role"], f"{file_label}.role")
            if role not in FILE_ROLES:
                fail(f"{file_label}.role: unsupported value")
            targets = require_unique_strings(item["targets"], f"{file_label}.targets")
            for target_id in targets:
                require_pattern(target_id, f"{file_label}.targets", TARGET_ID_RE)
            files.append(
                {
                    "path": path,
                    "sha256": file_sha,
                    "role": role,
                    "targets": sorted(targets),
                }
            )
        normalized.append(
            {
                "packageId": package_id,
                "filename": filename,
                "packageSha256": package_sha,
                "packageKind": package_kind,
                "waveLabel": wave_label,
                "registeredAt": registered_at,
                "registrationUrl": registration_url,
                "files": sorted(
                    files,
                    key=lambda item: (item["path"], item["sha256"], item["role"]),
                ),
            }
        )
    if normalized != sorted(normalized, key=lambda item: item["packageId"]):
        fail("registration snapshot: packages must use deterministic packageId order")
    normalized_targets: list[dict[str, Any]] = []
    for index, raw in enumerate(
        require_list(
            snapshot["targets"], "registration snapshot.targets", nonempty=True
        )
    ):
        label = f"registration snapshot.targets[{index}]"
        target = require_object(raw, label)
        require_exact_keys(target, label, {"targetId", "issue", "targetKind"})
        target_id = require_pattern(
            target["targetId"], f"{label}.targetId", TARGET_ID_RE
        )
        issue = target["issue"]
        if (
            not isinstance(issue, int)
            or isinstance(issue, bool)
            or not 1 <= issue <= 9999
        ):
            fail(f"{label}.issue: expected positive integer")
        target_kind = require_string(target["targetKind"], f"{label}.targetKind")
        if target_kind not in TARGET_KINDS:
            fail(f"{label}.targetKind: unsupported value")
        normalized_targets.append(
            {"targetId": target_id, "issue": issue, "targetKind": target_kind}
        )
    if normalized_targets != sorted(
        normalized_targets, key=lambda item: item["targetId"]
    ):
        fail("registration snapshot: targets must use deterministic targetId order")
    expected = registration_projection(manifest)
    if {"packages": normalized, "targets": normalized_targets} != expected:
        fail("registration snapshot: registered package/target/input inventory drift")


def markdown_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def target_sort_key(target: dict[str, Any]) -> tuple[int, int, str]:
    target_id = target["targetId"]
    if target_id.startswith("chapter-"):
        return (0, int(target_id.removeprefix("chapter-")), target_id)
    return (1, target["issue"], target_id)


def render_summary(manifest: dict[str, Any]) -> str:
    packages = sorted(manifest["packages"], key=lambda item: item["packageId"])
    targets = sorted(manifest["targets"], key=target_sort_key)
    counts = Counter(item["status"] for item in targets)
    lines = [
        "# Editorial Input Manifest",
        "",
        "このファイルは`editorial-input-manifest.json`から決定的に生成します。機械可読Manifestを更新し、`npm run render:editorial-inputs`を実行してください。このファイルを手編集しないでください。",
        "",
        f"- Manifest version: `{manifest['manifestVersion']}`",
        f"- Audit date: `{manifest['auditedAt']}`",
        f"- Packages / targets / candidates: `{len(packages)} / {len(targets)} / {sum(len(item['candidates']) for item in targets)}`",
        f"- Provenance: [Issue #{manifest['source']['registrationIssue']}](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/{manifest['source']['registrationIssue']}) / [Issue #{manifest['source']['contractIssue']}](https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/{manifest['source']['contractIssue']})",
        f"- External audit artifact: `{manifest['externalAuditArtifact']['availability']}`。内容やhash一致を推測しません。",
        "- Raw ZIP / predraftはRepository正本ではなく、Gitへ追加しません。",
        "- Candidate selectionは`selectedCandidateId`だけで表します。Filename、Wave、日時、File size、配列順は選択根拠になりません。",
        "",
        "## Status summary",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    for status_value in sorted(counts):
        lines.append(f"| `{status_value}` | {counts[status_value]} |")
    lines.extend(
        [
            "",
            "## Acknowledged collisions",
            "",
            "| ID | Kind | Value | Package IDs | Reason |",
            "|---|---|---|---|---|",
        ]
    )
    for item in sorted(
        manifest["collisionAcknowledgements"], key=lambda item: item["collisionId"]
    ):
        lines.append(
            f"| `{item['collisionId']}` | `{item['kind']}` | `{markdown_escape(item['value'])}` | "
            f"{', '.join(f'`{package_id}`' for package_id in item['packageIds'])} | "
            f"{markdown_escape(item['reason'])} |"
        )
    lines.extend(
        [
            "",
            "## Package index",
            "",
            "| Package ID | Package filename | SHA-256 | Kind | Wave | Registered | Source |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for package in packages:
        lines.append(
            f"| `{package['packageId']}` | `{markdown_escape(package['filename'])}` | `{package['sha256']}` | "
            f"`{package['packageKind']}` | `{package['waveLabel']}` | `{package['registeredAt']}` | "
            f"[registration]({package['registrationUrl']}) |"
        )
    lines.extend(
        [
            "",
            "## Target index",
            "",
            "| Target | Issue | Status | Selected candidate | Canonical PR | Evidence |",
            "|---|---:|---|---|---:|---|",
        ]
    )
    for target in targets:
        selected = (
            f"`{target['selectedCandidateId']}`"
            if target["selectedCandidateId"]
            else "—"
        )
        canonical = f"#{target['canonicalPr']}" if target["canonicalPr"] else "—"
        lines.append(
            f"| `{target['targetId']}` | #{target['issue']} | `{target['status']}` | {selected} | {canonical} | "
            f"[status]({target['statusHistory'][-1]['evidenceUrl']}) |"
        )
    lines.extend(["", "## Candidate disposition", ""])
    for target in targets:
        lines.extend(
            [
                f"### `{target['targetId']}` / Issue #{target['issue']}",
                "",
                "| Candidate | Package | Input | Input SHA-256 | Disposition | Reason |",
                "|---|---|---|---|---|---|",
            ]
        )
        for candidate in sorted(
            target["candidates"], key=lambda item: item["candidateId"]
        ):
            lines.append(
                f"| `{candidate['candidateId']}` | `{candidate['packageId']}` | "
                f"`{markdown_escape(candidate['inputPath'])}` | `{candidate['inputSha256']}` | "
                f"`{candidate['disposition']}` | {markdown_escape(candidate['dispositionReason'])} |"
            )
        lines.append("")
    lines.extend(
        [
            "## Intake gate",
            "",
            "1. `packageId`、Package SHA-256、Target IDをManifestと照合する。",
            "2. ZIP展開前に`python3 scripts/check_editorial_input_manifest.py --verify-package <path> --package-id <EIP-...> --target <target-id>`を実行する。",
            "3. 複数候補は`candidate-selection-required`のまま比較し、全代替候補のDispositionを記録する。",
            "4. `canonical-pr-open`ではmachine-readable Intake RecordとPR本文のIntake Recordを同時に追加する。",
            "5. Canonical実装はraw inputをコピーせず、current contractと再検証済み一次資料へ再構成する。",
            "6. merge・main CI・Pages確認後にのみ`consumed`へ遷移する。",
            "",
        ]
    )
    return "\n".join(lines)


def forbidden_tracked_paths(paths: list[str]) -> list[str]:
    forbidden = []
    for raw in paths:
        lower = raw.lower()
        parts = PurePosixPath(raw).parts
        if (
            lower.endswith(".zip")
            or ".predraft." in lower
            or (parts and parts[0] == ".work")
        ):
            forbidden.append(raw)
    return sorted(forbidden)


def check_tracked_raw_inputs(root: Path = ROOT) -> None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ManifestError(f"raw input tracking audit failed: {exc}") from exc
    try:
        tracked = result.stdout.decode("utf-8").split("\0")
    except UnicodeDecodeError as exc:
        raise ManifestError("raw input tracking audit returned non-UTF-8 path") from exc
    forbidden = forbidden_tracked_paths([item for item in tracked if item])
    if forbidden:
        fail(f"raw Editorial Input must remain untracked: {forbidden!r}")


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_zip_member_name(name: str, label: str) -> str:
    if name.endswith("/"):
        fail(f"{label}: directory entries are forbidden: {name!r}")
    return require_safe_relative_path(name, label)


def verify_package_archive(
    package: dict[str, Any], archive_path: Path, target_id: str
) -> None:
    if not archive_path.is_file() or archive_path.is_symlink():
        fail(f"package archive must be a regular file: {archive_path}")
    if archive_path.stat().st_size > MAX_PACKAGE_BYTES:
        fail(f"package archive exceeds {MAX_PACKAGE_BYTES} bytes")
    actual_package_sha = sha256_path(archive_path)
    if actual_package_sha != package["sha256"]:
        fail(
            f"package SHA-256 mismatch for {package['packageId']}: expected {package['sha256']}, got {actual_package_sha}"
        )
    expected_files = {item["path"]: item for item in package["files"]}
    target_primary = {
        item["path"]
        for item in package["files"]
        if item["role"] in PRIMARY_INPUT_ROLES and target_id in item["targets"]
    }
    if not target_primary:
        fail(
            f"package {package['packageId']} does not own primary input for target {target_id}"
        )
    try:
        with zipfile.ZipFile(archive_path) as archive:
            infos = archive.infolist()
            actual_names: list[str] = []
            total_uncompressed = 0
            for index, info in enumerate(infos):
                label = f"zip member[{index}]"
                name = validate_zip_member_name(info.filename, label)
                if name in actual_names:
                    fail(f"package ZIP contains duplicate path: {name}")
                actual_names.append(name)
                mode = info.external_attr >> 16
                if stat.S_ISLNK(mode):
                    fail(f"package ZIP contains symbolic link: {name}")
                if info.flag_bits & 0x1:
                    fail(f"package ZIP contains encrypted member: {name}")
                if info.file_size > MAX_MEMBER_BYTES:
                    fail(f"package ZIP member exceeds {MAX_MEMBER_BYTES} bytes: {name}")
                total_uncompressed += info.file_size
                if total_uncompressed > MAX_TOTAL_UNCOMPRESSED_BYTES:
                    fail(
                        f"package ZIP exceeds {MAX_TOTAL_UNCOMPRESSED_BYTES} uncompressed bytes"
                    )
            actual_set = set(actual_names)
            expected_set = set(expected_files)
            if actual_set != expected_set:
                missing = sorted(expected_set - actual_set)
                extra = sorted(actual_set - expected_set)
                fail(
                    f"package ZIP file inventory mismatch: missing={missing!r}, extra={extra!r}"
                )
            for info in infos:
                digest = hashlib.sha256()
                size = 0
                with archive.open(info, "r") as handle:
                    while True:
                        block = handle.read(1024 * 1024)
                        if not block:
                            break
                        size += len(block)
                        if size > MAX_MEMBER_BYTES:
                            fail(
                                f"package ZIP member expands beyond limit: {info.filename}"
                            )
                        digest.update(block)
                expected_sha = expected_files[info.filename]["sha256"]
                actual_sha = digest.hexdigest()
                if actual_sha != expected_sha:
                    fail(
                        f"package member SHA-256 mismatch for {info.filename}: expected {expected_sha}, got {actual_sha}"
                    )
    except (zipfile.BadZipFile, RuntimeError, OSError) as exc:
        raise ManifestError(f"invalid package ZIP: {exc}") from exc


def verify_selected_package(
    manifest: dict[str, Any], package_path: Path, package_id: str, target_id: str
) -> None:
    packages = {item["packageId"]: item for item in manifest["packages"]}
    package = packages.get(package_id)
    if package is None:
        fail(f"unknown packageId: {package_id}")
    targets = {item["targetId"]: item for item in manifest["targets"]}
    target = targets.get(target_id)
    if target is None:
        fail(f"unknown target: {target_id}")
    if not any(item["packageId"] == package_id for item in target["candidates"]):
        fail(f"target {target_id} does not register package {package_id}")
    selected_id = target["selectedCandidateId"]
    if selected_id is not None:
        selected = next(
            item for item in target["candidates"] if item["candidateId"] == selected_id
        )
        if package_id != selected["packageId"]:
            fail(
                f"target {target_id} selected candidate requires packageId "
                f"{selected['packageId']}; got {package_id}"
            )
    verify_package_archive(package, package_path, target_id)


def apply_regression_mutation(manifest: dict[str, Any], mutation: str) -> None:
    packages = manifest["packages"]
    targets = {item["targetId"]: item for item in manifest["targets"]}
    if mutation == "duplicate-package-id":
        packages[1]["packageId"] = packages[0]["packageId"]
    elif mutation == "duplicate-package-sha-without-alias":
        packages[1]["sha256"] = packages[0]["sha256"]
    elif mutation == "missing-filename-collision-record":
        manifest["collisionAcknowledgements"] = [
            item
            for item in manifest["collisionAcknowledgements"]
            if item["kind"] != "filename"
        ]
    elif mutation == "missing-wave-collision-record":
        manifest["collisionAcknowledgements"] = [
            item
            for item in manifest["collisionAcknowledgements"]
            if item["kind"] != "wave-label"
        ]
    elif mutation == "stale-collision-record":
        manifest["collisionAcknowledgements"].append(
            copy.deepcopy(manifest["collisionAcknowledgements"][0])
        )
        manifest["collisionAcknowledgements"][-1]["collisionId"] = "EICOLL-9999"
        manifest["collisionAcknowledgements"][-1]["kind"] = "filename"
        manifest["collisionAcknowledgements"][-1]["value"] = "not-a-collision.zip"
    elif mutation == "multi-candidate-registered":
        target = targets["chapter-09"]
        target["status"] = "registered-pending-prerequisites"
        target["statusHistory"][-1]["status"] = target["status"]
    elif mutation in {
        "filename-only-selection",
        "silent-latest-wins",
        "selected-alternative-missing",
    }:
        target = targets["chapter-09"]
        target["status"] = "selected-for-intake"
        target["statusHistory"].append(
            {
                "status": "selected-for-intake",
                "effectiveAt": "2026-09-05",
                "evidenceUrl": manifest["collisionAcknowledgements"][0]["evidenceUrl"],
                "reason": "invalid fixture",
            }
        )
        if mutation == "filename-only-selection":
            target["selectedCandidateId"] = packages[4]["filename"]
        else:
            target["selectedCandidateId"] = target["candidates"][0]["candidateId"]
            target["candidates"][0]["disposition"] = "selected"
    elif mutation == "canonical-pr-missing-intake-record":
        target = targets["chapter-05"]
        target["status"] = "canonical-pr-open"
        target["canonicalPr"] = 999
        target["statusHistory"].append(
            {
                "status": "canonical-pr-open",
                "effectiveAt": "2026-09-06",
                "evidenceUrl": "https://github.com/itdojp/white-hat-cyber-intelligence-book/pull/999",
                "reason": "invalid fixture",
            }
        )
    elif mutation == "unsafe-package-path":
        packages[0]["files"][0]["path"] = "../escape.predraft.md"
    elif mutation == "candidate-package-file-hash-mismatch":
        targets["chapter-05"]["candidates"][0]["inputSha256"] = "0" * 64
    elif mutation == "candidate-package-target-mismatch":
        packages[0]["files"][1]["targets"] = ["chapter-04"]
    elif mutation == "unowned-primary-input":
        packages[0]["files"][1]["targets"].append("chapter-06")
    elif mutation == "duplicate-target":
        manifest["targets"].append(copy.deepcopy(targets["chapter-05"]))
    elif mutation == "history-current-status-mismatch":
        targets["chapter-05"]["statusHistory"][-1]["status"] = "deferred"
    elif mutation == "invalid-history-transition":
        target = targets["chapter-05"]
        target["statusHistory"].insert(
            1,
            {
                "status": "consumed",
                "effectiveAt": "2026-09-01",
                "evidenceUrl": "https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/98",
                "reason": "invalid fixture",
            },
        )
    elif mutation == "blueprint-role-mismatch":
        packages[11]["files"][1]["role"] = "candidate-input"
    elif mutation == "intake-record-package-mismatch":
        targets["chapter-04"]["intakeRecord"]["packageSha256"] = "0" * 64
    elif mutation == "future-target-claims-legacy-record":
        source = targets["chapter-04"]["intakeRecord"]
        target = targets["chapter-05"]
        candidate = target["candidates"][0]
        package = next(
            item for item in packages if item["packageId"] == candidate["packageId"]
        )
        target["status"] = "canonical-pr-open"
        target["canonicalPr"] = 999
        candidate["disposition"] = "rewritten"
        target["intakeRecord"] = copy.deepcopy(source)
        target["intakeRecord"].update(
            {
                "recordUrl": "https://github.com/itdojp/white-hat-cyber-intelligence-book/pull/999",
                "packageId": candidate["packageId"],
                "packageSha256": package["sha256"],
                "inputPath": candidate["inputPath"],
                "inputSha256": candidate["inputSha256"],
                "targetIssue": target["issue"],
                "canonicalPr": 999,
                "currentMainSha": "0" * 40,
                "publicationProjectionVersion": None,
            }
        )
        target["statusHistory"].append(
            {
                "status": "canonical-pr-open",
                "effectiveAt": "2026-09-06",
                "evidenceUrl": "https://github.com/itdojp/white-hat-cyber-intelligence-book/pull/999",
                "reason": "invalid legacy fixture",
            }
        )
    elif mutation == "intake-record-url-mismatch":
        targets["chapter-04"]["intakeRecord"]["recordUrl"] = (
            "https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/64"
        )
    elif mutation == "status-history-prefix-deleted":
        target = targets["chapter-04"]
        target["statusHistory"] = [target["statusHistory"][-1]]
    elif mutation == "schema-invalid-package-filename":
        packages[0]["filename"] = "invalid\\name.zip"
    else:
        fail(f"regression corpus: unsupported mutation: {mutation}")


def run_manifest_regressions(
    manifest: dict[str, Any], schema: Any, corpus: Any, registration_snapshot: Any
) -> int:
    root = require_object(corpus, "regression corpus")
    require_exact_keys(root, "regression corpus", {"schemaVersion", "cases"})
    if root["schemaVersion"] != "1.0.0":
        fail("regression corpus: unexpected schemaVersion")
    cases = require_list(root["cases"], "regression corpus.cases", nonempty=True)
    seen_ids: set[str] = set()
    for index, raw in enumerate(cases):
        label = f"regression corpus.cases[{index}]"
        case = require_object(raw, label)
        require_exact_keys(case, label, {"id", "family", "mutation", "expectedError"})
        case_id = require_string(case["id"], f"{label}.id")
        if case_id in seen_ids:
            fail(f"regression corpus: duplicate case id: {case_id}")
        seen_ids.add(case_id)
        require_string(case["family"], f"{label}.family")
        expected = require_string(case["expectedError"], f"{label}.expectedError")
        mutated = copy.deepcopy(manifest)
        apply_regression_mutation(
            mutated, require_string(case["mutation"], f"{label}.mutation")
        )
        try:
            validate_manifest(mutated, schema)
        except ManifestError as exc:
            if expected not in str(exc):
                fail(f"regression {case_id}: expected {expected!r}, got {str(exc)!r}")
        else:
            fail(f"regression {case_id}: mutation was accepted")
    # Renderer output cannot depend on JSON array order.
    reordered = copy.deepcopy(manifest)
    reordered["packages"].reverse()
    reordered["targets"].reverse()
    reordered["collisionAcknowledgements"].reverse()
    for package in reordered["packages"]:
        package["files"].reverse()
    for target in reordered["targets"]:
        target["candidates"].reverse()
    if render_summary(reordered) != render_summary(manifest):
        fail("deterministic summary changed after source array reordering")
    if forbidden_tracked_paths(
        ["notes/input.predraft.md", "raw/package.zip", ".work/editorial-input/x.md"]
    ) != [
        ".work/editorial-input/x.md",
        "notes/input.predraft.md",
        "raw/package.zip",
    ]:
        fail("raw tracking regression did not detect every forbidden path")
    if forbidden_tracked_paths(
        ["EDITORIAL_INPUT_MANIFEST.md", "editorial-input-manifest.json"]
    ):
        fail("raw tracking regression rejected canonical metadata")
    incomplete = copy.deepcopy(manifest)
    incomplete["packages"] = [
        package
        for package in incomplete["packages"]
        if package["packageId"] != "EIP-0014"
    ]
    incomplete["targets"] = [
        target
        for target in incomplete["targets"]
        if target["targetId"] not in {"appendices-b-c-i", "appendices-e-f-g"}
    ]
    try:
        validate_manifest(incomplete, schema)
        validate_registration_snapshot(incomplete, registration_snapshot)
    except ManifestError as exc:
        if "registered package/target/input inventory drift" not in str(exc):
            fail(
                f"registration completeness regression returned unexpected error: {exc}"
            )
    else:
        fail("registration completeness regression accepted a silently removed Package")
    support_drift = copy.deepcopy(manifest)
    support_file = next(
        item
        for package in support_drift["packages"]
        for item in package["files"]
        if item["role"] == "source-review"
    )
    support_file["sha256"] = "0" * 64
    try:
        validate_manifest(support_drift, schema)
        validate_registration_snapshot(support_drift, registration_snapshot)
    except ManifestError as exc:
        if "registered package/target/input inventory drift" not in str(exc):
            fail(
                f"support-file completeness regression returned unexpected error: {exc}"
            )
    else:
        fail("registration completeness regression accepted support-file hash drift")
    target_drift = copy.deepcopy(manifest)
    next(
        target
        for target in target_drift["targets"]
        if target["targetId"] == "appendices-b-c-i"
    )["targetKind"] = "chapter"
    try:
        validate_manifest(target_drift, schema)
        validate_registration_snapshot(target_drift, registration_snapshot)
    except ManifestError as exc:
        if "registered package/target/input inventory drift" not in str(exc):
            fail(
                f"target-index completeness regression returned unexpected error: {exc}"
            )
    else:
        fail("registration completeness regression accepted target-kind drift")
    for initial_status, next_status in (
        ("blueprint-only", "selected-for-intake"),
        ("generator-blueprint-only", "canonical-pr-open"),
    ):
        validate_status_history(
            [
                {
                    "status": initial_status,
                    "effectiveAt": "2026-09-05",
                    "evidenceUrl": "https://github.com/itdojp/white-hat-cyber-intelligence-book/issues/98",
                    "reason": "registered blueprint fixture",
                },
                {
                    "status": next_status,
                    "effectiveAt": "2026-09-06",
                    "evidenceUrl": "https://github.com/itdojp/white-hat-cyber-intelligence-book/pull/999",
                    "reason": "canonical intake fixture",
                },
            ],
            f"{initial_status} transition fixture",
            next_status,
            initial_status,
        )
    unsupported_schema = copy.deepcopy(schema)
    unsupported_schema["$defs"]["safePath"]["maxLength"] = 4096
    try:
        validate_schema_contract(unsupported_schema)
    except ManifestError as exc:
        if "unsupported JSON Schema keywords" not in str(exc):
            fail(f"unsupported-schema regression returned unexpected error: {exc}")
    else:
        fail("unsupported-schema regression accepted an unknown validator keyword")
    return len(cases) + 8


def write_test_zip(
    path: Path, entries: list[tuple[zipfile.ZipInfo | str, bytes]]
) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, content in entries:
                archive.writestr(name, content)


def run_package_regressions() -> int:
    temporary_parent = ROOT / ".work"
    temporary_parent.mkdir(parents=True, exist_ok=True)
    # Keep every test artifact under the repository subtree and clean it deterministically.
    with tempfile.TemporaryDirectory(
        prefix="editorial-input-regressions-", dir=temporary_parent
    ) as raw_root:
        work_root = Path(raw_root)
        valid_path = work_root / "valid.zip"
        content = b"synthetic editorial input\n"
        write_test_zip(valid_path, [("chapter.predraft.md", content)])
        package = {
            "packageId": "EIP-9999",
            "sha256": sha256_path(valid_path),
            "files": [
                {
                    "path": "chapter.predraft.md",
                    "sha256": hashlib.sha256(content).hexdigest(),
                    "role": "candidate-input",
                    "targets": ["chapter-99"],
                }
            ],
        }
        verify_package_archive(package, valid_path, "chapter-99")
        cases = 1

        def expect_error(
            case_id: str,
            expected: str,
            test_package: dict[str, Any],
            path: Path,
            target: str = "chapter-99",
        ) -> None:
            nonlocal cases
            cases += 1
            try:
                verify_package_archive(test_package, path, target)
            except ManifestError as exc:
                if expected not in str(exc):
                    fail(
                        f"package regression {case_id}: expected {expected!r}, got {str(exc)!r}"
                    )
            else:
                fail(f"package regression {case_id}: invalid archive was accepted")

        wrong_package = copy.deepcopy(package)
        wrong_package["sha256"] = "0" * 64
        expect_error(
            "package-sha", "package SHA-256 mismatch", wrong_package, valid_path
        )
        wrong_member = copy.deepcopy(package)
        wrong_member["files"][0]["sha256"] = "0" * 64
        expect_error(
            "member-sha", "package member SHA-256 mismatch", wrong_member, valid_path
        )
        expect_error(
            "target", "does not own primary input", package, valid_path, "chapter-98"
        )

        extra_path = work_root / "extra.zip"
        write_test_zip(
            extra_path, [("chapter.predraft.md", content), ("extra.md", b"extra")]
        )
        extra_package = copy.deepcopy(package)
        extra_package["sha256"] = sha256_path(extra_path)
        expect_error("extra", "inventory mismatch", extra_package, extra_path)

        traversal_path = work_root / "traversal.zip"
        write_test_zip(traversal_path, [("../escape.md", b"escape")])
        traversal_package = copy.deepcopy(package)
        traversal_package["sha256"] = sha256_path(traversal_path)
        expect_error(
            "traversal", "unsafe archive path", traversal_package, traversal_path
        )

        duplicate_path = work_root / "duplicate.zip"
        write_test_zip(
            duplicate_path,
            [("chapter.predraft.md", content), ("chapter.predraft.md", content)],
        )
        duplicate_package = copy.deepcopy(package)
        duplicate_package["sha256"] = sha256_path(duplicate_path)
        expect_error("duplicate", "duplicate path", duplicate_package, duplicate_path)

        normalized_duplicate_path = work_root / "normalized-duplicate.zip"
        write_test_zip(
            normalized_duplicate_path,
            [("dir/chapter.md", content), ("dir/./chapter.md", b"replacement")],
        )
        normalized_duplicate_package = copy.deepcopy(package)
        normalized_duplicate_package["sha256"] = sha256_path(normalized_duplicate_path)
        normalized_duplicate_package["files"] = [
            {
                "path": "dir/chapter.md",
                "sha256": hashlib.sha256(content).hexdigest(),
                "role": "candidate-input",
                "targets": ["chapter-99"],
            },
            {
                "path": "dir/./chapter.md",
                "sha256": hashlib.sha256(b"replacement").hexdigest(),
                "role": "candidate-input",
                "targets": ["chapter-99"],
            },
        ]
        expect_error(
            "normalized-duplicate",
            "unsafe archive path",
            normalized_duplicate_package,
            normalized_duplicate_path,
        )

        symlink_path = work_root / "symlink.zip"
        link_info = zipfile.ZipInfo("chapter.predraft.md")
        link_info.create_system = 3
        link_info.external_attr = (stat.S_IFLNK | 0o777) << 16
        write_test_zip(symlink_path, [(link_info, b"target")])
        symlink_package = copy.deepcopy(package)
        symlink_package["sha256"] = sha256_path(symlink_path)
        expect_error("symlink", "symbolic link", symlink_package, symlink_path)

        alternate_path = work_root / "alternate.zip"
        alternate_content = b"alternate editorial input\n"
        write_test_zip(alternate_path, [("chapter.predraft.md", alternate_content)])
        alternate_package = {
            "packageId": "EIP-9998",
            "sha256": sha256_path(alternate_path),
            "files": [
                {
                    "path": "chapter.predraft.md",
                    "sha256": hashlib.sha256(alternate_content).hexdigest(),
                    "role": "candidate-input",
                    "targets": ["chapter-99"],
                }
            ],
        }
        selected_manifest = {
            "packages": [package, alternate_package],
            "targets": [
                {
                    "targetId": "chapter-99",
                    "selectedCandidateId": "EIC-0099-selected",
                    "candidates": [
                        {
                            "candidateId": "EIC-0099-selected",
                            "packageId": "EIP-9999",
                        },
                        {
                            "candidateId": "EIC-0099-alternate",
                            "packageId": "EIP-9998",
                        },
                    ],
                }
            ],
        }
        verify_selected_package(selected_manifest, valid_path, "EIP-9999", "chapter-99")
        cases += 1
        try:
            verify_selected_package(
                selected_manifest, alternate_path, "EIP-9998", "chapter-99"
            )
        except ManifestError as exc:
            if "selected candidate requires packageId EIP-9999" not in str(exc):
                fail(f"selected-package regression returned unexpected error: {exc}")
        else:
            fail(
                "selected-package regression accepted an alternative candidate Package"
            )
        cases += 1

        comparison_manifest = copy.deepcopy(selected_manifest)
        comparison_manifest["targets"][0]["selectedCandidateId"] = None
        verify_selected_package(
            comparison_manifest, alternate_path, "EIP-9998", "chapter-99"
        )
        cases += 1
        return cases


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--write-summary", action="store_true")
    parser.add_argument("--verify-package", type=Path)
    parser.add_argument("--package-id")
    parser.add_argument("--target")
    parser.add_argument("--skip-regressions", action="store_true")
    args = parser.parse_args()
    if args.verify_package and (not args.package_id or not args.target):
        parser.error(
            "--verify-package requires --package-id and --target; filename-only selection is forbidden"
        )
    if not args.verify_package and (args.package_id or args.target):
        parser.error("--package-id/--target require --verify-package")
    try:
        schema = load_json_strict(args.schema)
        registration_snapshot = load_json_strict(REGISTRATION_SNAPSHOT)
        manifest = validate_manifest(load_json_strict(args.manifest), schema)
        validate_registration_snapshot(manifest, registration_snapshot)
        expected_summary = render_summary(manifest)
        if args.write_summary:
            args.summary.write_text(expected_summary, encoding="utf-8")
            print(
                f"wrote {args.summary.relative_to(ROOT) if args.summary.is_relative_to(ROOT) else args.summary}"
            )
        else:
            try:
                actual_summary = args.summary.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                raise ManifestError(f"summary unavailable: {exc}") from exc
            if actual_summary != expected_summary:
                fail(f"{args.summary}: deterministic summary is out of sync")
        check_tracked_raw_inputs()
        regression_count = 0
        package_regression_count = 0
        if not args.skip_regressions:
            regression_count = run_manifest_regressions(
                manifest,
                schema,
                load_json_strict(REGRESSION_CORPUS),
                registration_snapshot,
            )
            package_regression_count = run_package_regressions()
        if args.verify_package:
            verify_selected_package(
                manifest, args.verify_package, args.package_id, args.target
            )
            print(
                f"verified package {args.package_id} for {args.target}: {args.verify_package}"
            )
        print(
            "checked Editorial Input Manifest: "
            f"{len(manifest['packages'])} packages, {len(manifest['targets'])} targets, "
            f"{sum(len(item['candidates']) for item in manifest['targets'])} candidates, "
            f"{regression_count} manifest/determinism regressions, "
            f"{package_regression_count} package regressions; raw tracked inputs 0"
        )
        print("PASS")
        return 0
    except ManifestError as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
