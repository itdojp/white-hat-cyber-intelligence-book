#!/usr/bin/env python3
"""Optional offline re-extraction of the fixed Chapter7 primary-source corpus.

No downloading, package install, plugin execution or arbitrary vectors. Only
byte-identical, previously inspected FIRST mathematical files are executed.
Node vm is NOT claimed as a security sandbox; the SHA-256 gate is mandatory.
"""

from __future__ import annotations

import argparse
import csv
from decimal import Decimal
import gzip
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
from xml.etree import ElementTree
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.check_editorial_input_manifest import load_json_strict  # noqa: E402

SNAPSHOT = ROOT / "cases/fixtures/ch07-source-snapshot.json"
CONTRACT = ROOT / "tests/fixtures/chapter07/publication-contract.json"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verified(path, expected):
    data = path.read_bytes()
    if digest(data) != expected:
        raise ValueError(f"source bytes mismatch: {path.name}")
    return data


def extract(directory, s):
    """All upstream inputs must match the frozen audit before parsing/execution."""
    e, k, c = s["epss"], s["kev"], s["cwe"]
    raw = verified(directory / "epss.csv.gz", e["compressedSha256"])
    text = gzip.decompress(raw)
    if digest(text) != e["csvSha256"]:
        raise ValueError("EPSS decompressed digest")
    lines = text.decode("utf-8").splitlines()
    if (
        lines[0]
        != f"#model_version:{e['modelIdentifier']},score_date:{e['scoreTimestamp']}"
    ):
        raise ValueError("EPSS model/date association")
    rows = list(csv.DictReader(lines[1:]))
    for wanted in e["rows"]:
        found = [r for r in rows if r["cve"] == wanted["cveId"]]
        if len(found) != 1 or any(
            Decimal(found[0][key]) != Decimal(str(wanted[out]))
            for key, out in (("epss", "score"), ("percentile", "percentile"))
        ):
            raise ValueError("EPSS selected value")
    kev = json.loads(verified(directory / "kev.json", k["catalogSha256"]))
    if (
        any(kev[key] != k[key] for key in ("catalogVersion", "dateReleased", "count"))
        or len(kev["vulnerabilities"]) != k["count"]
    ):
        raise ValueError("KEV complete catalog metadata")
    for wanted in k["rows"]:
        found = [r for r in kev["vulnerabilities"] if r["cveID"] == wanted["cveId"]]
        if len(found) != (1 if wanted["listed"] else 0):
            raise ValueError("KEV listed/unlisted membership")
        if found:
            row = found[0]
            if (
                row["dateAdded"] != wanted["dateAdded"]
                or row["dueDate"] != wanted["catalogDueDate"]
                or digest(row["requiredAction"].encode())
                != wanted["requiredActionSha256"]
            ):
                raise ValueError("KEV selected metadata")
    with ZipFile(
        io.BytesIO(verified(directory / "cwe.zip", c["zipSha256"]))
    ) as archive:
        xml_members = [p for p in archive.namelist() if p.endswith(".xml")]
        if len(xml_members) != 1:
            raise ValueError("CWE XML member inventory")
        xml = archive.read(xml_members[0])  # In-memory; never extract paths.
    if digest(xml) != c["xmlSha256"] or b"<!DOCTYPE" in xml or b"<!ENTITY" in xml:
        raise ValueError("CWE XML digest/declaration")
    root = ElementTree.fromstring(xml)
    weakness = root.find(".//{*}Weakness[@ID='639']")
    if (
        root.attrib["Version"] != c["version"]
        or root.attrib["Date"] != c["date"]
        or weakness is None
        or weakness.attrib["Name"] != c["selectedWeakness"]["name"]
    ):
        raise ValueError("CWE version/date/weakness")
    files = [
        verified(directory / name, sha).decode("utf-8")
        for name, sha in s["cvss"]["calculatorFiles"].items()
    ]
    # Only frozen, author-synthetic pairs are passed. The official source owns
    # score computation; this wrapper supplies metric inputs, not score grammar.
    program = r"""
const fs = require('node:fs'), vm = require('node:vm');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const scores = input.pairs.map(pair => {
 const ctx = vm.createContext(Object.create(null));
 for (const src of input.files) vm.runInContext(src, ctx, {timeout:1000});
 ctx.vector = pair.vector;
 return vm.runInContext(`(() => {
  const v = Object.fromEntries(Object.keys(expectedMetricOrder).map(k => [k, 'X']));
  for (const part of vector.split('/').slice(1)) {
   const [k, value] = part.split(':');
   if (!expectedMetricOrder[k]?.includes(value)) throw Error('metric');
   v[k] = value;
  }
  return cvss_score(v, cvssLookup_global, maxSeverity, macroVector(v));
 })()`, ctx, {timeout:1000});
});
process.stdout.write(JSON.stringify(scores));
"""
    result = subprocess.run(
        ["node", "-e", program],
        input=json.dumps({"files": files, "pairs": s["cvss"]["pairs"]}),
        text=True,
        capture_output=True,
        timeout=20,
        check=True,
    )
    if json.loads(result.stdout) != [p["score"] for p in s["cvss"]["pairs"]]:
        raise ValueError("FIRST finite CVSS pair parity")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--directory",
        type=Path,
        required=True,
        help="local audited input directory; no download occurs",
    )
    args = parser.parse_args()
    try:
        contract = load_json_strict(CONTRACT)
        verified(SNAPSHOT, contract["sourceSnapshotSha256"])
        extract(args.directory, load_json_strict(SNAPSHOT))
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        print("ERROR: Chapter7 offline source verification:", exc)
        return 1
    print(
        "Chapter7 offline source parity passed: EPSS 2; KEV 2/complete catalog; CWE 1; FIRST CVSS 2"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
