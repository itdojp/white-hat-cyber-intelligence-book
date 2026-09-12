#!/usr/bin/env python3
"""Read-only ART-18 synthetic receipt replay. Never starts or destroys a lab."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.chapter08_semantics import (  # noqa: E402
    PATHS,
    MODEL_VERSION,
    read_artifact,
    validate_bundle,
    encoded,
    generate_receipts,
)
from scripts.check_editorial_input_manifest import load_json_strict, ManifestError  # noqa: E402

SCHEMA_PATHS = tuple(
    "schemas/ch08-" + name + ".schema.json"
    for name in ("lab-plan", "control-receipts", "evidence-manifest")
)
PARENT_PATHS = (
    "cases/fixtures/ch06-signal-flow.json",
    "cases/fixtures/ch07-vulnerability-prioritization.json",
)


def load_bundle(root=ROOT):
    artifacts = [read_artifact(root, p) for p in PATHS]
    data = [item[1] for item in artifacts]
    schemas = [load_json_strict(root / p) for p in SCHEMA_PATHS]
    parents = [load_json_strict(root / p) for p in PARENT_PATHS]
    return data, artifacts[1][0], schemas, parents


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json", action="store_true", help="print the bounded replay report"
    )
    parser.add_argument(
        "--emit-receipts",
        action="store_true",
        help="print the fixed synthetic recipe bytes; never write a file",
    )
    args = parser.parse_args()
    try:
        data, raw, schemas, parents = load_bundle()
        errors = validate_bundle(*data, raw, schemas, parents)
        if errors:
            raise ValueError("; ".join(errors))
        if args.emit_receipts:
            sys.stdout.buffer.write(encoded(generate_receipts()))
        else:
            report = {
                "modelVersion": MODEL_VERSION,
                "synthetic": True,
                "runtimeExecuted": False,
                "artifactSha256": data[2]["sha256"],
                "runs": [
                    {"runId": r["runId"], **r["expected"]} for r in data[0]["runs"]
                ],
            }
            if args.json:
                print(json.dumps(report, ensure_ascii=False, indent=2))
            else:
                for r in report["runs"]:
                    print(
                        f"{r['runId']}: {r['verdict']} / {r['finalStatus']} / completedNormally={r['completedNormally']}"
                    )
                print(
                    "ART-18 offline replay passed; synthetic receipts only, no runtime execution"
                )
        return 0
    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        UnicodeError,
        ManifestError,
    ) as exc:
        print(f"ERROR: ART18 fail closed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
