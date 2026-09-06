#!/usr/bin/env python3
"""Extract the finite Chapter 5 source metadata; never fetch or execute CTI data.

Input is the separately downloaded, hash-pinned Enterprise STIX bundle. Only
identifiers, provenance and the relationships taught by Chapter 5 are retained.
Descriptions, procedure examples and executable/log-source recipes are omitted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "tests/fixtures/attack/ch05-v19.2.json"
COMMIT = "8543c5b05bd9bbcace9fc37f30bba96b675b6f33"
BUNDLE_SHA256 = "f7eaf37fe53b50404084fe1fe67237278f7317e61c11ad550295722d13ede259"
OBJECT_IDS = (
    "AN1487",
    "AN1488",
    "DC0038",
    "DC0066",
    "DC0069",
    "DET0539",
    "T1671",
    "TA0003",
)


def stable_json(data: object) -> bytes:
    return (
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def extract(raw: bytes) -> dict:
    if hashlib.sha256(raw).hexdigest() != BUNDLE_SHA256:
        raise ValueError("Chapter 5 ATT&CK bundle SHA-256 mismatch")
    bundle = json.loads(raw)
    selected = {}
    for item in bundle["objects"]:
        for ref in item.get("external_references", []):
            external_id = ref.get("external_id")
            if ref.get("source_name") == "mitre-attack" and external_id in OBJECT_IDS:
                if external_id in selected:
                    raise ValueError("duplicate ATT&CK external ID")
                selected[external_id] = (item, ref)
    if set(selected) != set(OBJECT_IDS):
        raise ValueError("missing Chapter 5 ATT&CK object")
    by_stix_id = {
        item["id"]: external_id for external_id, (item, _) in selected.items()
    }
    objects = []
    for external_id in OBJECT_IDS:
        item, ref = selected[external_id]
        # Absence of the optional STIX revoked property means not revoked;
        # retain its presence separately so the transformation is auditable.
        obj = {
            "externalId": external_id,
            "stixId": item["id"],
            "type": item["type"],
            "name": item["name"],
            "version": item["x_mitre_version"],
            "modified": item["modified"],
            "deprecated": item.get("x_mitre_deprecated", False),
            "revoked": item.get("revoked", False),
            "revokedPropertyPresent": "revoked" in item,
            "domains": sorted(item["x_mitre_domains"]),
            "url": ref["url"],
            "objectSha256": hashlib.sha256(stable_json(item)).hexdigest(),
        }
        if "x_mitre_platforms" in item:
            obj["platforms"] = sorted(item["x_mitre_platforms"])
        if external_id == "T1671":
            obj["isSubtechnique"] = item["x_mitre_is_subtechnique"]
            obj["tactics"] = sorted(p["phase_name"] for p in item["kill_chain_phases"])
        elif external_id == "TA0003":
            obj["shortname"] = item["x_mitre_shortname"]
        elif external_id == "DET0539":
            obj["analyticIds"] = sorted(
                by_stix_id[r] for r in item["x_mitre_analytic_refs"]
            )
        elif external_id.startswith("AN"):
            obj["dataComponentIds"] = sorted(
                {
                    by_stix_id[r["x_mitre_data_component_ref"]]
                    for r in item["x_mitre_log_source_references"]
                }
            )
            obj["mutableFields"] = sorted(
                r["field"] for r in item["x_mitre_mutable_elements"]
            )
        objects.append(obj)
    relations = []
    for item in bundle["objects"]:
        if item["type"] != "relationship":
            continue
        if (
            item.get("source_ref") not in by_stix_id
            or item.get("target_ref") not in by_stix_id
        ):
            continue
        relations.append(
            {
                "stixId": item["id"],
                "type": item["relationship_type"],
                "source": by_stix_id[item["source_ref"]],
                "target": by_stix_id[item["target_ref"]],
                "modified": item["modified"],
                "revoked": item.get("revoked", False),
                "deprecated": item.get("x_mitre_deprecated", False),
                "objectSha256": hashlib.sha256(stable_json(item)).hexdigest(),
            }
        )
    return {
        "schemaVersion": "1.0.0",
        "catalogVersion": "19.2",
        "domain": "enterprise-attack",
        "checkedAt": "2026-09-06",
        "updateStartDate": "2026-08-06",
        "releasePublishedAt": "2026-08-05T22:57:35Z",
        "upstreamCommit": COMMIT,
        "bundleSha256": BUNDLE_SHA256,
        "bundleUrl": f"https://raw.githubusercontent.com/mitre/cti/{COMMIT}/enterprise-attack/enterprise-attack.json",
        "licenseUrl": f"https://github.com/mitre/cti/blob/{COMMIT}/LICENSE.txt",
        "notice": "Copyright 2026 The MITRE Corporation. See THIRD_PARTY_NOTICES.md. Metadata subset; not a complete STIX bundle.",
        "objectHashEncoding": "UTF-8 JSON, ensure_ascii=False, indent=2, sort_keys=True, trailing LF",
        "objects": objects,
        "relationships": sorted(relations, key=lambda r: r["stixId"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Compare without writing the tracked fixture",
    )
    args = parser.parse_args()
    try:
        if (
            args.bundle.is_symlink()
            or not args.bundle.is_file()
            or args.bundle.stat().st_size > 100_000_000
        ):
            raise ValueError("expected a regular bundle of at most 100 MB")
        result = stable_json(extract(args.bundle.read_bytes()))
        if args.check:
            if OUTPUT.read_bytes() != result:
                raise ValueError(
                    "Chapter 5 source fixture differs from pinned bundle extraction"
                )
        else:
            OUTPUT.parent.mkdir(parents=True, exist_ok=True)
            OUTPUT.write_bytes(result)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print(
        f"Chapter 5 ATT&CK extraction verified: {len(OBJECT_IDS)} objects; sha256={hashlib.sha256(result).hexdigest()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
