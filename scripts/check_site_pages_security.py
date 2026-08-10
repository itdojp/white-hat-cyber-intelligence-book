#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.sync_book_site import run_registry_security_regressions  # noqa: E402


def main() -> int:
    failures = run_registry_security_regressions()
    for failure in failures:
        print(f"ERROR: {failure}")
    if failures:
        return 1
    print(
        "site page security regressions passed: object root, published-title safety, "
        "reserved destinations, canonical containment, safe static downloads, and "
        "symlink rejection"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
