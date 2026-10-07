#!/usr/bin/env python3
"""Offline asset/lock/layout wiring checks; actual rendering is a Book QA gate."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from publication_assets import (
    ROOT, LOCAL_ASSETS, MERMAID_ASSET, MERMAID_VERSION, load_publication_assets,
)
from sync_site_source import transform_shared_component, SiteGenerationError


def check_runtime_modes() -> None:
    subprocess.run(["node", str(ROOT / "scripts/check_browser_profile_cleanup.cjs")],
                   cwd=ROOT, check=True, timeout=45)
    # Children disable only this subprocess test, never the validation itself.
    probe = "import check_mermaid_contract as c; c.check_runtime_modes = lambda: None; c.main()"
    env = {**os.environ, "PYTHONPATH": str(ROOT / "scripts"),
           "LC_ALL": "C", "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0",
           "PYTHONOPTIMIZE": "0"}
    for flags in (["-O"], ["-OO"], []):
        result = subprocess.run([sys.executable, *flags, "-c", probe], cwd=ROOT,
                                env=env, capture_output=True, timeout=30)
        if flags:
            assert result.returncode != 0 and b"requires Python assertions" in result.stderr
            assert b"Mermaid contract passed" not in result.stdout
        else:
            assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
            assert b"Mermaid contract passed" in result.stdout


def main() -> None:
    if not __debug__:
        raise SystemExit("Mermaid contract requires Python assertions; unset PYTHONOPTIMIZE and do not use -O/-OO")
    assets = load_publication_assets()
    assert len(assets) == 3
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    lock = json.loads((ROOT / "package-lock.json").read_text(encoding="utf-8"))
    assert package["devDependencies"]["@mermaid-js/tiny"] == MERMAID_VERSION
    dependency = lock["packages"]["node_modules/@mermaid-js/tiny"]
    assert dependency["version"] == MERMAID_VERSION
    assert dependency["integrity"] == "sha512-ZW9YXy+3tSLPscBT+NnQO0K0qYH7BGES5nExl6Snoygey7xd2N0cO7Nq30N5k/u7gIeYoCrldyVy+VTCMWrNDQ=="
    assert lock["packages"][""]["devDependencies"] == package["devDependencies"]
    assert package["scripts"]["test"].split(" && ").count("npm run check:mermaid") == 1
    for path in ["scripts/run_book_qa.sh", ".github/workflows/book-qa.yml", ".github/workflows/pages.yml"]:
        text = (ROOT / path).read_text(encoding="utf-8")
        assert text.count("npm run check:mermaid-browser") == 1, path
        assert text.index("check_built_site.py") < text.index("npm run check:mermaid-browser"), path
    revision = json.loads((ROOT / ".book-formatter/revision.json").read_text(encoding="utf-8"))
    assert len(revision["localTransforms"]["_layouts/book.html"]) == 4
    fake = b'''<head>
<!-- Preconnect to external domains -->
fonts.googleapis.com
fonts.gstatic.com
<!-- Favicon -->
assets/favicon.ico
assets/apple-touch-icon.png
</head><body>{% if repo_url and page.path %}{{ page.path }}</body>'''
    transformed, changes = transform_shared_component("_layouts/book.html", fake)
    assert changes[-1] == "add-local-mermaid-progressive-enhancement"
    assert transformed.count(MERMAID_ASSET.encode()) == 1
    assert transformed.count(b"mermaid-loader.js") == 1
    assert transformed.count(b"mermaid-diagrams.css") == 1
    for marker in (b"</head>", b"</body>"):
        try:
            transform_shared_component("_layouts/book.html", fake.replace(marker, b""))
        except SiteGenerationError:
            pass
        else:
            raise AssertionError("missing insertion point accepted")
    assert transform_shared_component("_layouts/default.html", b"unchanged") == (b"unchanged", [])
    tmp = ROOT / ".tmp"
    tmp.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="mermaid-contract-", dir=tmp) as directory:
        root = Path(directory)
        node = root / "node_modules/@mermaid-js/tiny"
        (node / "dist").mkdir(parents=True)
        (node / "package.json").write_text(json.dumps({"name": "@mermaid-js/tiny", "version": MERMAID_VERSION}), encoding="utf-8")
        for source, target in LOCAL_ASSETS.items():
            (root / source).parent.mkdir(parents=True, exist_ok=True)
            (root / source).write_bytes(assets[target])
        for data in (b"", b"altered"):
            (node / "dist/mermaid.tiny.js").write_bytes(data)
            try:
                load_publication_assets(root)
            except ValueError:
                pass
            else:
                raise AssertionError("altered library accepted")
        (node / "dist/mermaid.tiny.js").write_bytes(assets[MERMAID_ASSET])
        assert load_publication_assets(root) == assets
        (node / "package.json").write_text('{"name":"@mermaid-js/tiny","version":"0.0.0"}', encoding="utf-8")
        try:
            load_publication_assets(root)
        except ValueError:
            pass
        else:
            raise AssertionError("different package version accepted")
    fixtures = json.loads((ROOT / "tests/fixtures/mermaid/publication.json").read_text(encoding="utf-8"))
    assert len(fixtures) == len({item["id"] for item in fixtures})
    for fixture in fixtures:
        assert len(fixture["sources"]) == len(fixture["expected"])
        assert set(fixture["expected"]) <= {"rendered", "error"}
    notice = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
    assert "@mermaid-js/tiny" in notice and MERMAID_VERSION in notice
    assert (ROOT / "node_modules/@mermaid-js/tiny/LICENSE").read_text(encoding="utf-8").strip() in notice
    check_runtime_modes()
    print(f"Mermaid contract passed: {MERMAID_VERSION}, 3 assets, locked integrity, negative asset/layout probes, {len(fixtures)} browser fixtures")


if __name__ == "__main__":
    main()
