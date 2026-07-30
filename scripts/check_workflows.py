#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / ".github" / "workflows"
EXPECTED_WORKFLOWS = {
    "contract.yml",
    "book-qa.yml",
    "pages.yml",
}
PINNED_FORMATTER = "69eb5c12f5a750b65614bc9bbbc3d7abd5aa6f6c"
FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
USES_RE = re.compile(r"^\s*-?\s*uses:\s*([^\s#]+)", re.MULTILINE)


def main() -> int:
    errors: list[str] = []
    workflows = {path.name: path for path in WORKFLOW_DIR.glob("*.yml")}
    workflows.update({path.name: path for path in WORKFLOW_DIR.glob("*.yaml")})

    missing = EXPECTED_WORKFLOWS - set(workflows)
    if missing:
        errors.append(f"missing workflows: {sorted(missing)}")

    for name, path in sorted(workflows.items()):
        text = path.read_text(encoding="utf-8")
        if "FORCE_JAVASCRIPT_ACTIONS_TO_NODE24" not in text:
            errors.append(f"{path.relative_to(ROOT)}: missing Node 24 action guard")
        for action in USES_RE.findall(text):
            if action.startswith("./"):
                continue
            if "@" not in action:
                errors.append(f"{path.relative_to(ROOT)}: action has no ref: {action}")
                continue
            repository, ref = action.rsplit("@", 1)
            if not repository or not FULL_SHA_RE.fullmatch(ref):
                errors.append(
                    f"{path.relative_to(ROOT)}: action must use a full immutable SHA: {action}"
                )

    for name in ("contract.yml", "book-qa.yml", "pages.yml"):
        path = workflows.get(name)
        if path and PINNED_FORMATTER not in path.read_text(encoding="utf-8"):
            errors.append(f"{path.relative_to(ROOT)}: missing pinned book-formatter commit")

    contract = workflows.get("contract.yml")
    if contract:
        text = contract.read_text(encoding="utf-8")
        for required in ("npm test", "BOOK_FORMATTER_DIR", "contents: read"):
            if required not in text:
                errors.append(f"contract.yml: missing {required!r}")

    book_qa = workflows.get("book-qa.yml")
    if book_qa:
        text = book_qa.read_text(encoding="utf-8")
        for required in (
            "npm run sync:docs",
            "check-unicode.js",
            "check-textlint.js",
            "check-links.js",
            "check-layout-risk.js",
            "check-markdown-structure.js",
            "bundle exec jekyll build",
            "scripts/check_built_site.py",
        ):
            if required not in text:
                errors.append(f"book-qa.yml: missing {required!r}")

    pages = workflows.get("pages.yml")
    if pages:
        text = pages.read_text(encoding="utf-8")
        if re.search(r"^\s*pull_request\s*:", text, re.MULTILINE):
            errors.append("pages.yml: deployment workflow must not run on pull_request")
        for required in (
            "pages: write",
            "id-token: write",
            "branches: [main]",
            "actions/configure-pages@",
            "actions/upload-pages-artifact@",
            "actions/deploy-pages@",
        ):
            if required not in text:
                errors.append(f"pages.yml: missing {required!r}")

    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "docs", "_site", "build"],
        check=True,
        text=True,
        capture_output=True,
    )
    tracked_generated = [line for line in result.stdout.splitlines() if line.strip()]
    if tracked_generated:
        errors.append(
            "generated output must not be tracked: " + ", ".join(tracked_generated)
        )

    for message in errors:
        print(f"ERROR: {message}")
    if errors:
        return 1

    print(
        f"workflow contract passed: {len(workflows)} workflows, immutable action refs, "
        "pinned formatter, generated output untracked"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
