#!/usr/bin/env python3
"""Bounded A/D/H regressions, not real operations or human reader approval."""
from copy import deepcopy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
from scripts import check_appendix_adh as c  # noqa: E402


class AppendixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs = {name: c.read_input(ROOT, name) for name in c.INPUTS}
        cls.contract = c.strict(cls.inputs[c.CONTRACT])
        cls.docs = {name: cls.inputs[name] for name in c.DOCUMENTS}

    def test_canonical(self):
        self.assertEqual(c.document_errors(self.docs, self.contract), [])
        self.assertEqual(c.repository_errors(self.inputs, self.contract), [])

    def test_complete_document_inventory(self):
        for name in c.DOCUMENTS:
            docs = dict(self.docs)
            del docs[name]
            self.assertEqual(c.document_errors(docs, self.contract), ["ADH-document-inventory"])
        self.assertEqual(c.document_errors(dict(self.docs, unexpected="# New"), self.contract),
                         ["ADH-document-inventory"])

    def test_preamble_body_tail_reach_shared_policy(self):
        for name, text in self.docs.items():
            for at in (0, text.index("\n\n") + 2, len(text)):
                with self.subTest(name=name, at=at):
                    docs = dict(self.docs)
                    docs[name] = (
                        text.rstrip("\n") + "\n\n実Credentialを窃取する。\n"
                        if at == len(text)
                        else text[:at] + "\n\n実Credentialを窃取する。\n\n" + text[at:]
                    )
                    self.assertTrue(any(e.startswith("ADH-safety:")
                                        for e in c.document_errors(docs, self.contract)))

    def test_prohibition_is_safe_but_new_fields_still_require_review(self):
        for name in self.docs:
            docs = dict(self.docs)
            docs[name] += "\n実Credentialを窃取しない。\n"
            errors = c.document_errors(docs, self.contract)
            self.assertFalse(any(e.startswith("ADH-safety:") for e in errors))
            self.assertIn("ADH-reader-fields: " + name, errors)

    def test_destination_policy_and_unsupported_source(self):
        for name in self.docs:
            for source, prefix in (
                ("[補足](https://example.com)", "ADH-safety:"),
                ("![図](https://example.com/image.png)", "ADH-safety:"),
                ("{% include unreviewed.html %}", "ADH-projection:"),
            ):
                docs = dict(self.docs)
                docs[name] += "\n\n" + source + "\n"
                with self.subTest(name=name, source=source):
                    self.assertTrue(any(e.startswith(prefix)
                                        for e in c.document_errors(docs, self.contract)))

    def test_finite_meanings_not_only_keyword_presence(self):
        mutations = (
            (c.DOCUMENTS[0], "Draft / Do not proceed", "Approved / Proceed"),
            (c.DOCUMENTS[0], "2026-08-19T18:00:00+09:00", "2027-08-19T18:00:00+09:00"),
            (c.DOCUMENTS[1], "不足を残す", "不足を隠す"),
            (c.DOCUMENTS[1], "Not collected", "Pass"),
            (c.DOCUMENTS[1], "Inconclusive", "Safe"),
            (c.DOCUMENTS[2], " / Running", ""),
            (c.DOCUMENTS[2], "executionAuthorized=false", "executionAuthorized=true"),
            (c.DOCUMENTS[2], "Unsafe | Cleanup verified | false", "Unsafe | Cleanup verified | true"),
            (c.DOCUMENTS[2], "Credential・Port", "Credential"),
            (c.DOCUMENTS[3], "過去Caseの分析時点", "現在Caseの分析時点"),
        )
        for name, old, new in mutations:
            with self.subTest(name=name, old=old):
                self.assertIn(old, self.docs[name])
                docs = dict(self.docs)
                docs[name] = docs[name].replace(old, new)
                # Leaving the original words in a hidden comment cannot repair the reader field.
                docs[name] += f"\n<!-- {old} -->\n"
                self.assertIn("ADH-reader-fields: " + name,
                              c.document_errors(docs, self.contract))

    def test_parent_changes_require_review_not_reinterpretation(self):
        for name in c.PARENTS:
            inputs = dict(self.inputs)
            inputs[name] += "\n"
            self.assertIn("ADH-parent-review-required: " + name,
                          c.repository_errors(inputs, self.contract))

    def test_source_identity_is_bound_without_refreshing_unreviewed_dates(self):
        for identifier in c.SOURCE_IDS:
            for kind in ("missing", "version"):
                inputs = dict(self.inputs)
                registry = c.strict(inputs["references/sources.json"])
                source = next(s for s in registry["sources"] if s["id"] == identifier)
                if kind == "missing":
                    registry["sources"].remove(source)
                else:
                    source["version"] = "unreviewed"
                inputs["references/sources.json"] = json.dumps(registry)
                self.assertIn("ADH-source-identity: " + identifier,
                              c.repository_errors(inputs, self.contract))

    def test_appendix_review_is_discoverable_in_registry_and_baseline(self):
        from scripts.render_reference_baseline import render
        registry = c.strict(self.inputs["references/sources.json"])
        entries = {s["id"]: s for s in registry["sources"]}
        for sid in c.SOURCE_IDS:
            review = entries[sid].get("appendixReview")
            self.assertIsInstance(review, dict, sid)
            self.assertEqual(review["checkedAt"], "2026-10-17")
            self.assertGreaterEqual(entries[sid]["checkedAt"], review["checkedAt"])
            self.assertEqual(review["note"], c.DOCUMENTS[3])
        rendered = render(registry)
        self.assertIn("## 付録の用途限定確認", rendered)
        self.assertEqual(rendered.count("[限定確認](appendix-adh-source-review-2026-10-17.md)"), 5)
        self.assertEqual(c.repository_errors(self.inputs, self.contract), [])

    def test_parent_source_identity_bindings_remain_consistent(self):
        sources = {s["id"]: s for s in c.strict(self.inputs["references/sources.json"])["sources"]}
        for chapter in (8, 9, 10, 14, 15, 20):
            path = f"tests/fixtures/chapter{chapter:02}/publication-contract.json"
            parent = c.strict((ROOT / path).read_text(encoding="utf-8"))
            for sid, expected in parent["sourceIdentity"].items():
                for key, value in expected.items():
                    with self.subTest(chapter=chapter, source=sid, field=key):
                        self.assertEqual(sources[sid][key], value)

    def test_appendix_review_drift_fails_closed(self):
        for sid in c.SOURCE_IDS:
            for kind in ("missing", "date", "source-date", "target", "note", "notes", "trigger"):
                inputs = dict(self.inputs)
                registry = c.strict(inputs["references/sources.json"])
                source = next(s for s in registry["sources"] if s["id"] == sid)
                if kind == "missing":
                    source.pop("appendixReview")
                elif kind == "date":
                    source["appendixReview"]["checkedAt"] = "2026-10-18"
                elif kind == "source-date":
                    source["checkedAt"] = "2026-10-16"
                elif kind == "target":
                    source["appendixReview"]["targets"] = ["appendix-j"]
                elif kind == "note":
                    source["appendixReview"]["note"] = "references/other.md"
                elif kind == "notes":
                    source["notes"] = "review omitted"
                else:
                    source["reviewTriggers"] = []
                inputs["references/sources.json"] = json.dumps(registry)
                with self.subTest(sid=sid, kind=kind):
                    self.assertIn("ADH-source-review: " + sid,
                                  c.repository_errors(inputs, self.contract))

    def test_baseline_optional_review_metadata_is_bounded(self):
        from scripts.render_reference_baseline import render
        registry = c.strict(self.inputs["references/sources.json"])
        for source in registry["sources"]:
            source.pop("appendixReview", None)
        self.assertNotIn("## 付録の用途限定確認", render(registry))
        source = registry["sources"][0]
        good = {"checkedAt": "2026-10-17", "targets": ["appendix-a"],
                "note": c.DOCUMENTS[3]}
        for field, value in (("checkedAt", "not-a-date"), ("checkedAt", "2026-02-30"),
                             ("targets", []), ("targets", ["appendix-a", "appendix-a"]),
                             ("targets", [29]), ("note", "references/../private.md"),
                             ("note", "https://example.invalid/note.md"),
                             ("note", "references/a](bad).md")):
            source["appendixReview"] = dict(good, **{field: value})
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                render(registry)

    def test_route_missing_duplicate_collision_and_legacy_owner(self):
        for kind in ("missing", "duplicate", "destination", "order", "legacy"):
            inputs = dict(self.inputs)
            registry = c.strict(inputs["site-pages.json"])
            route = deepcopy(self.contract["routes"][0])
            if kind == "missing":
                registry["pages"].remove(route)
            else:
                if kind != "duplicate":
                    route["source"] = "appendices/other.md"
                if kind == "order":
                    route["destination"] = "appendices/other/index.md"
                if kind == "legacy":
                    route["destination"] = "appendices/lab-guide/index.md"
                registry["pages"].append(route)
            inputs["site-pages.json"] = json.dumps(registry)
            self.assertTrue(c.repository_errors(inputs, self.contract))

    def test_entry_links_and_checker_ownership(self):
        for name in c.ENTRIES:
            inputs = dict(self.inputs)
            inputs[name] = inputs[name].replace("appendices/appendix-", "missing/appendix-")
            self.assertTrue(any(e.startswith("ADH-return-link:")
                                for e in c.repository_errors(inputs, self.contract)))
        for key in ("test", "sync:docs", "check:appendix-adh"):
            inputs = dict(self.inputs)
            package = c.strict(inputs["package.json"])
            package["scripts"][key] = "echo skipped"
            inputs["package.json"] = json.dumps(package)
            self.assertIn("ADH-entrypoints", c.repository_errors(inputs, self.contract))

    def test_strict_json_and_regular_bounded_inputs(self):
        for source in ('{"x":1,"x":2}', '{"x":NaN}'):
            with self.assertRaises(ValueError):
                c.strict(source)
        temporary = ROOT / ".tmp"
        temporary.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temporary) as directory:
            root = Path(directory)
            path = root / "package.json"
            for kind in ("symlink", "directory", "fifo", "oversize", "invalid-utf8"):
                with self.subTest(kind=kind):
                    if kind == "symlink":
                        path.symlink_to(ROOT / "package.json")
                    elif kind == "directory":
                        path.mkdir()
                    elif kind == "fifo":
                        os.mkfifo(path)
                    else:
                        path.write_bytes(b"x" * 1_048_577 if kind == "oversize" else b"\xff")
                    try:
                        with self.assertRaises((ValueError, OSError)):
                            c.read_input(root, "package.json")
                    finally:
                        if kind == "directory":
                            path.rmdir()
                        else:
                            path.unlink()
            with self.assertRaises(ValueError):
                c.read_input(root, "../outside")


if __name__ == "__main__":
    unittest.main()
