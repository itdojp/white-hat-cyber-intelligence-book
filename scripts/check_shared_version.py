#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "book-config.json"
REVISION_PATH = ROOT / ".book-formatter" / "revision.json"

EXPECTED = {
    "repository": "itdojp/book-formatter",
    "commit": "fba61076a7d8171e8344c5d60119f737447214d1",
    "shared_version": "3.3.3",
    "shared_version_blob": "66d7d7b8cc6c11ab817603f5892d7cbe7b9726b6",
    "schema_blob": "87dcb44b0d4b543ba43ae3a8ebc27d2f3cfda3cd",
}

EXPECTED_COMPONENTS = {
    "bookLayout": (
        "shared/layouts/book.html",
        "8c862d57ddd5cee0b0ba3cd4a9e2cc86884b29d9",
        "_layouts/book.html",
    ),
    "defaultLayout": (
        "shared/layouts/default.html",
        "1ad26bd9f41b349cdd24bad844a1ee820274fdb7",
        "_layouts/default.html",
    ),
    "sidebarNavigation": (
        "shared/includes/sidebar-nav.html",
        "007edb903f6b62f00c83691ef1db7de9460328f7",
        "_includes/sidebar-nav.html",
    ),
    "pageNavigation": (
        "shared/includes/page-navigation.html",
        "7a0b1e84cd77cd423aba2dba340d879f4e1e65d9",
        "_includes/page-navigation.html",
    ),
    "mainCss": (
        "shared/assets/css/main.css",
        "f1ce8f5ea649ad7e358465bd1408df76daace8ae",
        "assets/css/main.css",
    ),
    "mobileResponsiveCss": (
        "shared/assets/css/mobile-responsive.css",
        "cd8b92d1624d6f69286b73e8efe19839514d6475",
        "assets/css/mobile-responsive.css",
    ),
    "syntaxHighlightingCss": (
        "shared/assets/css/syntax-highlighting.css",
        "b0f2cb368477a5fdcdff14f2fb878c349975d50e",
        "assets/css/syntax-highlighting.css",
    ),
    "codeCopyJs": (
        "shared/assets/js/code-copy-lightweight.js",
        "a7440238c656604baadcff8a46e83e2bb8ac6f0d",
        "assets/js/code-copy-lightweight.js",
    ),
    "searchJs": (
        "shared/assets/js/search.js",
        "30dafcf5966cd71318981fec057c1fbf7ea1113c",
        "assets/js/search.js",
    ),
    "themeJs": (
        "shared/assets/js/theme.js",
        "7c7a8cd9675305842a1cb60da322efa60c27a165",
        "assets/js/theme.js",
    ),
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
    required_component_versions = {"layouts", "includes", "assets", "templates", "schemas"}
    if set(component_versions) != required_component_versions:
        errors.append("component version keys do not match the pinned shared manifest")

    components = revision.get("components", {})
    if set(components) != set(EXPECTED_COMPONENTS):
        errors.append(
            "component manifest keys differ: "
            f"{sorted(set(components) ^ set(EXPECTED_COMPONENTS))}"
        )
    for name, (expected_path, expected_blob, expected_target) in EXPECTED_COMPONENTS.items():
        component = components.get(name, {})
        if component.get("path") != expected_path:
            errors.append(f"{name}: unexpected source path")
        if component.get("blobSha") != expected_blob:
            errors.append(f"{name}: unexpected blob SHA")
        if component.get("target") != expected_target:
            errors.append(f"{name}: unexpected target path")

    for message in errors:
        print(f"ERROR: {message}")
    if errors:
        return 1

    print(
        "shared component pin is consistent: "
        f"{revision['repository']}@{revision['commit']} / shared {config_version} / "
        f"{len(EXPECTED_COMPONENTS)} files"
    )
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
