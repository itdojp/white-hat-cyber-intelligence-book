#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "book-config.json"
REVISION_PATH = ROOT / ".book-formatter" / "revision.json"

EXPECTED = {
    "repository": "itdojp/book-formatter",
    "commit": "69eb5c12f5a750b65614bc9bbbc3d7abd5aa6f6c",
    "shared_version": "3.2.2",
    "shared_version_blob": "fdf70965323ae2a78e8dcbe5df88aa4a6ce8b16e",
    "schema_blob": "87dcb44b0d4b543ba43ae3a8ebc27d2f3cfda3cd",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    config = load(CONFIG_PATH)
    revision = load(REVISION_PATH)
    errors: list[str] = []

    if revision.get("repository") != EXPECTED["repository"]:
        errors.append("unexpected book-formatter repository")
    if revision.get("commit") != EXPECTED["commit"]:
        errors.append("unexpected book-formatter commit")
    if revision.get("schema", {}).get("blobSha") != EXPECTED["schema_blob"]:
        errors.append("unexpected book-config schema blob SHA")
    if revision.get("shared", {}).get("blobSha") != EXPECTED["shared_version_blob"]:
        errors.append("unexpected shared/version.json blob SHA")

    config_version = config.get("shared", {}).get("version")
    revision_version = revision.get("shared", {}).get("version")
    if config_version != EXPECTED["shared_version"]:
        errors.append(
            f"book-config.json shared.version is {config_version!r}; "
            f"expected {EXPECTED['shared_version']!r}"
        )
    if revision_version != EXPECTED["shared_version"]:
        errors.append(
            f"revision shared.version is {revision_version!r}; "
            f"expected {EXPECTED['shared_version']!r}"
        )
    if config_version != revision_version:
        errors.append("book-config and pinned revision shared versions differ")

    component_versions = revision.get("shared", {}).get("componentVersions", {})
    required_components = {"layouts", "includes", "assets", "templates", "schemas"}
    if set(component_versions) != required_components:
        errors.append("component version keys do not match the pinned shared manifest")

    for message in errors:
        print(f"ERROR: {message}")
    if errors:
        return 1

    print(
        "shared component pin is consistent: "
        f"{revision['repository']}@{revision['commit']} / shared {config_version}"
    )
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
