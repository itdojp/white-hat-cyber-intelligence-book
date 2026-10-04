#!/usr/bin/env python3
"""Bounded positive/negative navigation checks, not a real-reader trial."""
from copy import deepcopy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from scripts.check_learning_route import (  # noqa: E402
    GUIDE, MARKERS, ROOT, ROUTE, check_documents, check_route, read_input,
)
from scripts.publication_projection import destination_fields, project_documents  # noqa: E402


class LearningRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.documents = {name: read_input(ROOT, name) for name in ("quickstart.md", GUIDE)}
        cls.registry = json.loads(read_input(ROOT, "site-pages.json"))
        cls.package = json.loads(read_input(ROOT, "package.json"))

    def test_canonical_reader_route(self):
        self.assertEqual(check_documents(self.documents), [])
        self.assertEqual(check_route(self.registry, self.package), [])

    def test_boundary_markers_must_be_reader_visible(self):
        for marker in MARKERS:
            with self.subTest(marker=marker):
                docs = dict(self.documents)
                docs[GUIDE] = docs[GUIDE].replace(marker, "欠落") + f"\n<!-- {marker} -->\n"
                self.assertIn(f"LR-boundary-marker: {marker}", check_documents(docs))

    def test_missing_navigation_each_direction(self):
        for document, target in (
            ("quickstart.md", "cases/first-artifact-walkthrough.md"),
            ("quickstart.md", "templates/integrated-security-case-map.md"),
            (GUIDE, "ch01-integrated-security-case-example.md"),
            (GUIDE, "../templates/integrated-security-case-map.md"),
            (GUIDE, "../quickstart.md"),
        ):
            with self.subTest(document=document, target=target):
                docs = dict(self.documents)
                docs[document] = docs[document].replace(f"]({target})", "](missing-learning-route.md)")
                self.assertTrue(any(e.startswith("LR-link:") for e in check_documents(docs)))

    def test_minimal_submission_section_handoffs(self):
        actual = {f.text for f in destination_fields(project_documents(self.documents))
                  if f.document_id == "quickstart.md"}
        for fragment in ("2-空templateへ必要な欄から戻る", "4-提出と自己点検"):
            target = f"../cases/first-artifact-walkthrough/#{fragment}"
            with self.subTest(fragment=fragment):
                self.assertIn(target, actual)
                source = f"cases/first-artifact-walkthrough.md#{fragment}"
                for replacement in ("cases/first-artifact-walkthrough.md",
                                    "cases/first-artifact-walkthrough.md#missing-section"):
                    docs = dict(self.documents)
                    docs["quickstart.md"] = docs["quickstart.md"].replace(source, replacement)
                    self.assertIn(f"LR-link: quickstart.md: {target}", check_documents(docs))

    def test_preamble_body_tail_reach_shared_safety(self):
        for document in self.documents:
            body_at = self.documents[document].index("\n\n") + 2
            for at in (0, body_at, len(self.documents[document])):
                with self.subTest(document=document, at=at):
                    docs = dict(self.documents)
                    text = docs[document]
                    docs[document] = (
                        text.rstrip("\n") + "\n\n実Credentialを窃取する。\n"
                        if at == len(text)
                        else text[:at] + "\n\n実Credentialを窃取する。\n\n" + text[at:]
                    )
                    self.assertTrue(any(e.startswith("LR-safety:") for e in check_documents(docs)))

    def test_unsupported_interpreted_source(self):
        docs = dict(self.documents)
        docs[GUIDE] += "\n{% include unreviewed.html %}\n"
        self.assertTrue(any(e.startswith("PP1001:") for e in check_documents(docs)))

    def test_absolute_destinations_reach_shared_host_policy(self):
        for document in self.documents:
            for link in ("[補足](https://example.com)", "![図](https://example.com/image.png)",
                         "[連絡](mailto:reader@example.com)"):
                with self.subTest(document=document, link=link):
                    docs = dict(self.documents)
                    docs[document] = docs[document].rstrip() + "\n\n" + link + "\n"
                    self.assertTrue(any(e.startswith("LR-safety:") for e in check_documents(docs)))
            docs = dict(self.documents)
            docs[document] = docs[document].rstrip() + "\n\n[合成参照](https://lab.example)\n"
            self.assertEqual(check_documents(docs), [])

    def test_typed_visible_fields_use_normalized_policy_handoff(self):
        # This is literal code text, not interpreted Markdown links. The shared
        # owner defines its Policy handoff; this consumer must not parse it again.
        docs = dict(self.documents)
        docs[GUIDE] = docs[GUIDE].rstrip() + (
            "\n\n`実[C](a)[r](a)[e](a)[d](a)[e](a)[n](a)[t](a)[i](a)[a](a)[l](a)を窃取する。`\n"
        )
        self.assertEqual(check_documents(docs), [])

    def test_no_generic_heading_emulation(self):
        docs = dict(self.documents)
        docs[GUIDE] += "\n## 未レビューの追加面\n"
        self.assertIn("LR-heading-inventory: reviewed reader surface changed", check_documents(docs))

    def test_route_missing_duplicate_destination_and_order(self):
        route = next(p for p in self.registry["pages"] if p["source"] == GUIDE)
        for kind in ("missing", "duplicate", "destination", "order"):
            with self.subTest(kind=kind):
                registry = deepcopy(self.registry)
                if kind == "missing":
                    registry["pages"] = [p for p in registry["pages"] if p["source"] != GUIDE]
                else:
                    extra = dict(route)
                    if kind != "duplicate":
                        extra["source"] = "cases/other.md"
                    if kind == "order":
                        extra["destination"] = "cases/other/index.md"
                    registry["pages"].append(extra)
                self.assertTrue(check_route(registry, self.package))

    def test_test_ownership_and_command(self):
        for kind in ("owner", "command"):
            with self.subTest(kind=kind):
                package = deepcopy(self.package)
                if kind == "owner":
                    package["scripts"]["test"] = package["scripts"]["test"].replace("npm run check:learning-route && ", "")
                else:
                    package["scripts"]["check:learning-route"] = "echo skipped"
                self.assertTrue(check_route(self.registry, package))

    def test_route_order_has_one_constant_owner(self):
        # Simulate a reviewed contract update, not a runtime registry exemption.
        with patch.dict(ROUTE, {"order": 341}):
            registry = deepcopy(self.registry)
            next(p for p in registry["pages"] if p["source"] == GUIDE)["order"] = 341
            self.assertEqual(check_route(registry, self.package), [])
            registry["pages"].append({
                **ROUTE, "source": "cases/other.md", "destination": "cases/other/index.md",
            })
            self.assertIn("LR-order: navigation order must have one owner",
                          check_route(registry, self.package))

    def test_invalid_document_inventory(self):
        self.assertTrue(check_documents({GUIDE: self.documents[GUIDE]}))

    def test_malformed_registry_and_package(self):
        for registry, package in (
            ([], self.package), (self.registry, []), ({"pages": [None]}, self.package),
            (self.registry, {"scripts": []}), (self.registry, {"scripts": {"test": []}}),
        ):
            with self.subTest(registry=type(registry).__name__, package=type(package).__name__):
                with self.assertRaises(ValueError):
                    check_route(registry, package)

    def test_bounded_regular_utf8_fixed_inputs(self):
        with tempfile.TemporaryDirectory(dir=ROOT / ".tmp") as raw:
            root = Path(raw)
            p = root / "quickstart.md"
            for raw in (b"\xff", b"a" * 1_048_577):
                p.write_bytes(raw)
                with self.assertRaises(ValueError):
                    read_input(root, "quickstart.md")
            p.unlink()
            p.symlink_to(ROOT / "quickstart.md")
            with self.assertRaises(ValueError):
                read_input(root, "quickstart.md")
            p.unlink()
            os.mkfifo(p)
            with self.assertRaises(ValueError):
                read_input(root, "quickstart.md")
            with self.assertRaises(ValueError):
                read_input(root, "../quickstart.md")


if __name__ == "__main__":
    (ROOT / ".tmp").mkdir(exist_ok=True)
    unittest.main(verbosity=2)
