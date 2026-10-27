#!/usr/bin/env python3
"""Finite B/C/I regression probes; no external operations or human approval."""
from copy import deepcopy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'scripts')]
from scripts import check_appendix_bci as c  # noqa: E402
from scripts.publication_projection import project_documents  # noqa: E402


class AppendixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs, cls.contract = c.load_inputs(ROOT)
        cls.catalog = c.strict(cls.inputs[c.CATALOG])
        names = sorted({c.INDEX, *(r[k] for r in cls.catalog['artifacts']
                                   for k in ('template', 'chapter'))})
        cls.projection = project_documents({n: cls.inputs[n] for n in names})
        cls.docs = {n: cls.inputs[n] for n in c.DOCUMENTS}

    def errors(self, catalog=None, inputs=None):
        return c.manifest_errors(catalog or self.catalog, inputs or self.inputs,
                                 self.contract, self.projection)

    def mutated(self, mutate):
        cat = deepcopy(self.catalog)
        mutate(cat)
        inputs = dict(self.inputs)
        inputs[c.CATALOG] = json.dumps(cat, ensure_ascii=False, indent=2) + '\n'
        return cat, inputs

    def rejected(self, mutate, prefix):
        cat, inputs = self.mutated(mutate)
        try:
            errors = self.errors(cat, inputs)
        except ValueError as exc:
            errors = [str(exc)]
        self.assertTrue(any(e.startswith(prefix) for e in errors), errors)

    def test_canonical_all_surfaces(self):
        self.assertEqual(self.errors(), [])
        self.assertEqual(c.integration_errors(self.inputs, self.contract), [])
        self.assertEqual(c.document_errors(self.docs, self.contract), [])

    def test_generation_is_exact_idempotent_and_preserves_authored_parts(self):
        before = {n: (ROOT / n).read_bytes() for n in [c.CATALOG, *c.DOCUMENTS]}
        generated = c.render(self.catalog)
        for name in c.DOCUMENTS:
            actual = c.replace_block(self.docs[name], generated[name])
            self.assertEqual(actual, self.docs[name])
            self.assertEqual(c.replace_block(actual, generated[name]), actual)
            custom = '著者の前書き\n\n' + actual + '\n著者の追記\n'
            updated = c.replace_block(custom, generated[name] + '\n追加の索引')
            self.assertTrue(updated.startswith('著者の前書き\n\n'))
            self.assertTrue(updated.endswith('\n著者の追記\n'))
        self.assertEqual(before, {n: (ROOT / n).read_bytes() for n in before})

    def test_missing_duplicate_reordered_orphan_artifacts(self):
        for mutation in (lambda j: j['artifacts'].pop(),
                         lambda j: j['artifacts'].append(deepcopy(j['artifacts'][0])),
                         lambda j: j['artifacts'].reverse(),
                         lambda j: j['artifacts'][0].update(artifactId='ART-999'),
                         lambda j: j['artifacts'][0].update(title='Unreviewed name'),
                         lambda j: j['artifacts'][0].update(indexedChapters=[0, 99])):
            self.rejected(mutation, 'BCI-live-index-agreement')

    def test_template_example_fixture_roles_are_not_interchangeable(self):
        self.rejected(lambda j: j['artifacts'][0].update(template=j['artifacts'][0]['example']),
                      'BCI-role-path')
        self.rejected(lambda j: j['artifacts'][1].update(example=j['artifacts'][1]['fixtures'][0]['path']),
                      'BCI-role-path')
        self.rejected(lambda j: j['artifacts'][1]['fixtures'][0].update(path=j['artifacts'][1]['template']),
                      'BCI-fixture-download')
        self.rejected(lambda j: j['artifacts'][1]['fixtures'][0].update(download='downloads/missing.json'),
                      'BCI-fixture-download')

    def test_every_role_ref_and_dod_requires_actual_parent_anchor(self):
        for idx in range(len(self.catalog['artifacts'])):
            for role in (*c.ROLES, 'learningObjective', 'chapterDoD'):
                def mutate(j):
                    row = j['artifacts'][idx]
                    ref = row[role] if role in ('learningObjective', 'chapterDoD') else row['fieldRefs'][role]
                    ref['anchor'] = 'missing-reviewed-field'
                with self.subTest(artifact=idx, role=role):
                    self.rejected(mutate, 'BCI-field-reference')

    def test_rebound_metadata_cannot_restore_removed_learning_route_anchor(self):
        # Regression for PR213 integrated with B/C/I: a refreshed hash is not
        # proof that a Chapter DoD destination still exists in the parent.
        catalog, inputs = self.mutated(
            lambda j: j['artifacts'][0]['chapterDoD'].update(
                anchor='6-learning-route-plan'))
        contract = deepcopy(self.contract)
        contract['catalogSha256'] = c.digest(inputs[c.CATALOG])
        errors = c.manifest_errors(catalog, inputs, contract, self.projection)
        self.assertIn('BCI-field-reference: ART-01/chapterDoD', errors)
        self.assertNotIn('BCI-metadata-review-required', errors)

    def test_status_semantics_and_required_fields_are_review_bound(self):
        # This is an edition gate, NOT an arbitrary workflow or legal checker.
        for role in c.ROLES:
            def mutate(j):
                j['artifacts'][0]['fieldRefs'][role]['note'] = 'All approved; no further review'
            self.rejected(mutate, 'BCI-metadata-review-required')
            self.rejected(lambda j: j['artifacts'][0]['fieldRefs'].pop(role), 'BCI-object-shape')
        for role in ('learningObjective', 'chapterDoD'):
            self.rejected(lambda j: j['artifacts'][0].pop(role), 'BCI-object-shape')
        self.rejected(lambda j: j['artifacts'][0].update(allowedStatuses=['Always safe']),
                      'BCI-object-shape')

    def test_checklist_obligations_and_eight_passes(self):
        for key in ('automation', 'limitation', 'failureAction', 'owner'):
            self.rejected(lambda j: j['checklists'][0].pop(key), 'BCI-object-shape')
            self.rejected(lambda j: j['checklists'][0].update({key: ''}), 'BCI-metadata-text')
        self.rejected(lambda j: j['checklists'][0].update(artifacts=['ART-999']),
                      'BCI-checklist-reference')
        self.rejected(lambda j: j['reviewPasses'].pop(), 'BCI-eight-review-passes')
        self.rejected(lambda j: j['reviewPasses'][0].update(evidence='Total score erases every gap'),
                      'BCI-metadata-review-required')

    def test_all_parent_bytes_are_bound(self):
        for name in self.contract['parentDigests']:
            inputs = dict(self.inputs)
            inputs[name] += '\n'
            with self.subTest(name=name):
                self.assertIn('BCI-parent-review-required: ' + name, self.errors(inputs=inputs))

    def test_index_duplicate_hidden_by_renderer_dedup_still_fails(self):
        inputs = dict(self.inputs)
        line = next(s for s in inputs[c.INDEX].splitlines() if s.startswith('| ART-01 |'))
        inputs[c.INDEX] = inputs[c.INDEX].replace(line, line + '\n' + line)
        self.assertIn('BCI-parent-review-required: ' + c.INDEX, self.errors(inputs=inputs))

    def test_missing_duplicate_misordered_generation_markers(self):
        for source in ('no markers', c.START + c.START + c.END,
                       c.START + c.END + c.END, c.END + c.START):
            with self.subTest(source=source), self.assertRaises(ValueError):
                c.replace_block(source, 'data')

    def test_full_preamble_body_tail_reach_shared_scanner(self):
        for name in self.docs:
            for position in ('preamble', 'body', 'tail'):
                docs = dict(self.docs)
                unsafe = '\n\n実Credentialを窃取する。\n\n'
                if position == 'preamble':
                    docs[name] = unsafe + docs[name]
                elif position == 'tail':
                    docs[name] = docs[name].rstrip('\n') + unsafe.rstrip('\n') + '\n'
                else:
                    docs[name] = docs[name].replace(c.START, c.START + unsafe)
                with self.subTest(name=name, position=position):
                    self.assertTrue(any(e.startswith('BCI-safety:')
                                        for e in c.document_errors(docs, self.contract)))

    def test_safe_prohibition_still_requires_reader_review(self):
        docs = dict(self.docs)
        docs[c.DOCUMENTS[0]] += '\n実Credentialを窃取しない。\n'
        errors = c.document_errors(docs, self.contract)
        self.assertFalse(any(e.startswith('BCI-safety:') for e in errors))
        self.assertIn('BCI-reader-review-required: ' + c.DOCUMENTS[0], errors)

    def test_raw_comment_liquid_and_destination_fail_closed(self):
        for suffix, prefix in (('\n<!-- comment -->\n', 'BCI-projection:'),
                               ('\n{% include external %}\n', 'BCI-projection:'),
                               ('\n[extra](https://example.com)\n', 'BCI-safety:')):
            docs = dict(self.docs)
            docs[c.DOCUMENTS[0]] += suffix
            self.assertTrue(any(e.startswith(prefix) for e in c.document_errors(docs, self.contract)))

    def test_document_inventory_and_human_meaning_drift(self):
        with self.assertRaises(ValueError):
            c.document_errors(dict(self.docs, unknown='new'), self.contract)
        docs = dict(self.docs)
        docs[c.DOCUMENTS[2]] = docs[c.DOCUMENTS[2]].replace('低評価にしない', '低評価にする')
        self.assertNotEqual(docs, self.docs)
        self.assertIn('BCI-reader-review-required: ' + c.DOCUMENTS[2],
                      c.document_errors(docs, self.contract))

    def test_route_uniqueness_and_preflight_before_deletion(self):
        for kind in ('missing', 'duplicate', 'collision'):
            site = c.strict(self.inputs['site-pages.json'])
            route = deepcopy(self.contract['routes'][0])
            if kind == 'missing':
                site['pages'].remove(route)
            else:
                if kind == 'collision':
                    route['source'] = 'appendices/other.md'
                site['pages'].append(route)
            inputs = dict(self.inputs, **{'site-pages.json': json.dumps(site)})
            self.assertTrue(c.integration_errors(inputs, self.contract))
        for key in ('test', 'check:appendix-bci', 'sync:docs'):
            package = c.strict(self.inputs['package.json'])
            package['scripts'][key] = 'echo skipped'
            inputs = dict(self.inputs, **{'package.json': json.dumps(package)})
            self.assertIn('BCI-entrypoints', c.integration_errors(inputs, self.contract))

    def test_strict_json_and_bounded_regular_inputs(self):
        for source in ('{"x":1,"x":2}', '{"x":NaN}'):
            with self.assertRaises(ValueError):
                c.strict(source)
        temporary = ROOT / '.tmp'
        temporary.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temporary) as directory:
            root = Path(directory)
            path = root / 'input.json'
            for kind in ('symlink', 'directory', 'fifo', 'oversize', 'invalid-utf8'):
                if kind == 'symlink':
                    path.symlink_to(ROOT / c.CATALOG)
                elif kind == 'directory':
                    path.mkdir()
                elif kind == 'fifo':
                    os.mkfifo(path)
                else:
                    path.write_bytes(b'x' * 1_048_577 if kind == 'oversize' else b'\xff')
                try:
                    with self.subTest(kind=kind), self.assertRaises((ValueError, OSError)):
                        c.read_input(root, 'input.json', ['input.json'])
                finally:
                    if kind == 'directory':
                        path.rmdir()
                    else:
                        path.unlink()
            with self.assertRaises(ValueError):
                c.read_input(root, '../outside', ['../outside'])


if __name__ == '__main__':
    unittest.main()
