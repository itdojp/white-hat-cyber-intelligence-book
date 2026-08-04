#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
NOTICE_SOURCE = ROOT / "THIRD_PARTY_NOTICES.md"
NOTICE_DESTINATION = "THIRD_PARTY_NOTICES.txt"
NOTICE_MARKERS = (
    "MIT License",
    "Copyright (c) ITDO Inc.",
    "Permission is hereby granted, free of charge",
    "THE SOFTWARE IS PROVIDED \"AS IS\"",
    "764f644850c21983c96919d0e13706413d59c089",
)
REQUIRED_ASSETS = (
    "assets/css/main.css",
    "assets/css/mobile-responsive.css",
    "assets/css/syntax-highlighting.css",
    "assets/js/code-copy-lightweight.js",
    "assets/js/search.js",
    "assets/js/theme.js",
)


def expected_html(destination: str, site: Path) -> Path:
    if destination == "index.md":
        return site / "index.html"
    if destination.endswith("/index.md"):
        return site / destination[: -len("index.md")] / "index.html"
    return site / Path(destination).with_suffix(".html")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="docs")
    parser.add_argument("--site", default="_site")
    args = parser.parse_args()

    source = Path(args.source).resolve()
    site = Path(args.site).resolve()
    manifest_path = source / "_data" / "build-manifest.json"
    errors: list[str] = []

    if not manifest_path.is_file():
        print(f"ERROR: missing site-source manifest: {manifest_path}")
        return 1
    if not site.is_dir():
        print(f"ERROR: missing built site directory: {site}")
        return 1

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_pages = [
        expected_html(item["destination"], site)
        for item in manifest.get("pages", [])
    ]
    for page in expected_pages:
        if not page.is_file() or page.stat().st_size == 0:
            errors.append(f"missing or empty page: {page.relative_to(site)}")

    static_files = manifest.get("staticFiles", [])
    generated_markdown_text = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(source.rglob("*.md"))
    )
    built_html_text = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(site.rglob("*.html"))
    )
    for item in static_files:
        source_path = ROOT / item["source"]
        generated_path = source / item["destination"]
        published_path = site / item["destination"]
        if not source_path.is_file():
            errors.append(f"missing canonical static artifact: {item['source']}")
            continue
        canonical_bytes = source_path.read_bytes()
        expected_sha256 = hashlib.sha256(canonical_bytes).hexdigest()
        if item.get("sha256") != expected_sha256:
            errors.append(
                f"static artifact manifest hash mismatch: {item['destination']}"
            )
        for label, path in (
            ("generated", generated_path),
            ("published", published_path),
        ):
            if not path.is_file() or path.read_bytes() != canonical_bytes:
                errors.append(
                    f"{label} static artifact differs from canonical source: "
                    f"{item['destination']}"
                )
        if item["destination"] not in generated_markdown_text:
            errors.append(
                f"generated pages do not link to static artifact: {item['destination']}"
            )
        if item["destination"] not in built_html_text:
            errors.append(
                f"built pages do not link to static artifact: {item['destination']}"
            )
        mutable_repository_link = (
            "https://github.com/itdojp/white-hat-cyber-intelligence-book/blob/main/"
            + quote(item["source"], safe="/")
        )
        if mutable_repository_link in generated_markdown_text:
            errors.append(
                f"generated pages retain mutable static artifact link: {item['source']}"
            )
        if mutable_repository_link in built_html_text:
            errors.append(
                f"built pages retain mutable static artifact link: {item['source']}"
            )

    for asset in REQUIRED_ASSETS:
        path = site / asset
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing or empty asset: {asset}")

    notice_path = site / NOTICE_DESTINATION
    if not NOTICE_SOURCE.is_file():
        errors.append(f"missing canonical third-party notice: {NOTICE_SOURCE}")
    elif not notice_path.is_file() or notice_path.stat().st_size == 0:
        errors.append(f"missing or empty third-party notice: {NOTICE_DESTINATION}")
    else:
        source_bytes = NOTICE_SOURCE.read_bytes()
        published_bytes = notice_path.read_bytes()
        if published_bytes != source_bytes:
            errors.append(
                f"{NOTICE_DESTINATION}: published notice differs from canonical source"
            )
        else:
            notice_text = published_bytes.decode("utf-8")
            for marker in NOTICE_MARKERS:
                if marker not in notice_text:
                    errors.append(
                        f"{NOTICE_DESTINATION}: missing required marker {marker!r}"
                    )

    index_path = site / "index.html"
    if index_path.is_file():
        index = index_path.read_text(encoding="utf-8")
        for marker in (
            "<html",
            "ホワイトハッカーとサイバーインテリジェンス実践体系",
            "book-layout",
            "assets/css/main.css",
        ):
            if marker not in index:
                errors.append(f"index.html: missing marker {marker!r}")

    generated_markdown = sorted(site.rglob("*.md"))
    if generated_markdown:
        errors.append(
            "built site contains unrendered Markdown: "
            + ", ".join(
                path.relative_to(site).as_posix()
                for path in generated_markdown[:10]
            )
        )

    for message in errors:
        print(f"ERROR: {message}")
    if errors:
        return 1

    print(
        f"built site smoke check passed: {len(expected_pages)} pages, "
        f"{len(static_files)} static artifact(s), "
        f"{len(REQUIRED_ASSETS)} assets, 1 third-party notice"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
