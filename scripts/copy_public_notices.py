#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import os
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "THIRD_PARTY_NOTICES.md"
DOCS_DIR = ROOT / "docs"
DESTINATION = DOCS_DIR / "THIRD_PARTY_NOTICES.txt"
REQUIRED_MARKERS = (
    "MIT License",
    "Copyright (c) ITDO Inc.",
    "Permission is hereby granted, free of charge",
    "THE SOFTWARE IS PROVIDED \"AS IS\"",
    "198935ff8f60653c40e513343dc5f02573d9968e",
)


class PublicNoticeError(RuntimeError):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def source_bytes() -> bytes:
    if not SOURCE.is_file():
        raise PublicNoticeError(f"missing canonical notice: {SOURCE.relative_to(ROOT)}")
    data = SOURCE.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PublicNoticeError("third-party notice must be UTF-8") from exc
    for marker in REQUIRED_MARKERS:
        if marker not in text:
            raise PublicNoticeError(
                f"{SOURCE.relative_to(ROOT)}: missing required notice marker {marker!r}"
            )
    return data


def validate_destination() -> None:
    lexical_docs = Path(os.path.abspath(DOCS_DIR))
    lexical_destination = Path(os.path.abspath(DESTINATION))
    if lexical_destination.parent != lexical_docs:
        raise PublicNoticeError("public notice destination escaped generated docs directory")
    if DOCS_DIR.is_symlink():
        raise PublicNoticeError("generated docs directory must not be a symbolic link")
    if DESTINATION.is_symlink():
        raise PublicNoticeError("public notice destination must not be a symbolic link")


def check_contract(data: bytes) -> None:
    validate_destination()
    with tempfile.TemporaryDirectory(
        prefix="book-public-notice-a-"
    ) as first_tmp, tempfile.TemporaryDirectory(
        prefix="book-public-notice-b-"
    ) as second_tmp:
        first = Path(first_tmp) / DESTINATION.name
        second = Path(second_tmp) / DESTINATION.name
        first.write_bytes(data)
        second.write_bytes(data)
        if first.read_bytes() != second.read_bytes():
            raise PublicNoticeError("public notice generation is not deterministic")

    if DESTINATION.exists() and DESTINATION.read_bytes() != data:
        raise PublicNoticeError(
            f"{DESTINATION.relative_to(ROOT)} is stale; run npm run sync:docs"
        )

    print(
        "public notice contract passed: "
        f"{DESTINATION.relative_to(ROOT)} / sha256:{sha256(data)}"
    )


def write_notice(data: bytes) -> None:
    validate_destination()
    if not DOCS_DIR.is_dir():
        raise PublicNoticeError(
            "generated docs directory is missing; run site-source generation first"
        )
    DESTINATION.write_bytes(data)
    if DESTINATION.read_bytes() != data:
        raise PublicNoticeError("public notice copy verification failed")
    print(
        f"copied {SOURCE.relative_to(ROOT)} to {DESTINATION.relative_to(ROOT)} "
        f"(sha256:{sha256(data)})"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    try:
        data = source_bytes()
        if args.check:
            check_contract(data)
        else:
            write_notice(data)
    except (OSError, PublicNoticeError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
