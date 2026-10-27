#!/usr/bin/env python3
"""Finite cross-artifact reference edition; shared projection and policy own syntax.

The catalog is editorial metadata, not a workflow/status interpreter. Fixed
parent bytes and a reviewed metadata digest require review on semantic drift.
Only explicit --write replaces marked blocks; normal checks are read-only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.check_editorial_input_manifest import (  # noqa: E402
    _reject_constant, _reject_duplicate_keys,
)
from scripts.content_safety_policy import (  # noqa: E402
    POLICY_VERSION, scan_action_text, scan_host_policy,
)
from scripts.publication_projection import (  # noqa: E402
    PROJECTION_VERSION, project_documents, is_policy_scan_field, is_absolute_destination,
)

CATALOG = 'references/artifact-catalog.json'
CONTRACT = 'tests/fixtures/appendix-bci/publication-contract.json'
DOCUMENTS = (
    'appendices/appendix-b-templates.md',
    'appendices/appendix-c-checklists.md',
    'appendices/appendix-i-rubric.md',
)
INDEX = 'artifact-index.md'
ROLES = ('identifiers', 'status', 'owner', 'review', 'reassessment')
LABELS = ('必須ID・最初の記入先', 'Statusの対象と境界', 'Owner', 'Review', 'Reassessment')
START = '生成索引開始（BCI_GENERATED_START）'
END = '生成索引終了（BCI_GENERATED_END）'
COMMAND = 'python3 scripts/check_appendix_bci.py'


def require(ok, code):
    if not ok:
        raise ValueError('BCI-' + code)


def strict(text):
    return json.loads(text, object_pairs_hook=_reject_duplicate_keys, parse_constant=_reject_constant)


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def read_input(root, name, allowed):
    require(name in allowed and not root.is_symlink(), 'input-inventory')
    path = Path(name)
    require(not path.is_absolute() and all(p not in ('.', '..') and not p.startswith('.')
                                         for p in path.parts), 'relative-input')
    target = root / path
    require(not any(p.is_symlink() for p in (target, *target.parents)
                    if p.is_relative_to(root)), 'symlink-input')
    fd = os.open(target, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as stream:
        require(stat.S_ISREG(os.fstat(stream.fileno()).st_mode), 'regular-input')
        raw = stream.read(1_048_577)
    require(0 < len(raw) <= 1_048_576, 'input-size')
    return raw.decode('utf-8')


def keys(value, names):
    require(type(value) is dict and set(value) == set(names.split()), 'object-shape')


def text(value):
    # Author-authored single-line metadata, not a Markdown syntax parser.
    require(type(value) is str and 0 < len(value) <= 1000 and value == value.strip()
            and '\n' not in value and '\r' not in value, 'metadata-text')


def validate_shape(catalog):
    keys(catalog, 'version edition artifacts checklists reviewPasses')
    require(catalog['version'] == '1.0.0', 'catalog-version')
    text(catalog['edition'])
    for group, maximum in (('artifacts', 200), ('checklists', 100), ('reviewPasses', 8)):
        rows = catalog[group]
        require(type(rows) is list and 0 < len(rows) <= maximum, 'list-size')
    require(len(catalog['reviewPasses']) == 8, 'eight-review-passes')
    for row in catalog['artifacts']:
        keys(row, 'artifactId title primaryOwnerChapter indexedChapters chapter template example '
                  'fixtures purpose inputs outputs fieldRefs learningObjective chapterDoD')
        for k in ('artifactId', 'title', 'chapter', 'template', 'example', 'purpose', 'inputs', 'outputs'):
            text(row[k])
        require(type(row['primaryOwnerChapter']) is int and row['primaryOwnerChapter'] >= 0,
                'chapter-type')
        require(type(row['indexedChapters']) is list and row['indexedChapters']
                and all(type(n) is int and n >= 0 for n in row['indexedChapters'])
                and len(row['indexedChapters']) == len(set(row['indexedChapters']))
                and row['primaryOwnerChapter'] in row['indexedChapters'], 'indexed-chapters')
        keys(row['fieldRefs'], ' '.join(ROLES))
        for ref in (*row['fieldRefs'].values(), row['learningObjective'], row['chapterDoD']):
            keys(ref, 'path anchor note')
            for value in ref.values():
                text(value)
        require(type(row['fixtures']) is list and len(row['fixtures']) <= 30, 'fixtures')
        for fixture in row['fixtures']:
            keys(fixture, 'path download')
            text(fixture['path'])
            if fixture['download'] is not None:
                text(fixture['download'])
    for row in catalog['checklists']:
        keys(row, 'id title question automation limitation failureAction owner artifacts')
        for k in ('id', 'title', 'question', 'automation', 'limitation', 'failureAction', 'owner'):
            text(row[k])
        require(type(row['artifacts']) is list and row['artifacts']
                and all(type(a) is str for a in row['artifacts']), 'checklist-artifacts')
    for row in catalog['reviewPasses']:
        keys(row, 'id title evidence')
        for value in row.values():
            text(value)


def parent_paths(catalog):
    return sorted({INDEX, *(r[k] for r in catalog['artifacts']
                           for k in ('template', 'example', 'chapter')),
                   *(f['path'] for r in catalog['artifacts'] for f in r['fixtures'])})


def manifest_errors(catalog, inputs, contract, projection=None):
    validate_shape(catalog)
    errors = []
    for name, expected in contract['parentDigests'].items():
        if digest(inputs[name]) != expected:
            errors.append('BCI-parent-review-required: ' + name)
    if parent_paths(catalog) != list(contract['parentDigests']):
        errors.append('BCI-parent-inventory')
    if digest(inputs[CATALOG]) != contract['catalogSha256']:
        errors.append('BCI-metadata-review-required')
    rows = catalog['artifacts']
    ids = [r['artifactId'] for r in rows]
    if len(ids) != len(set(ids)) or len({r['template'] for r in rows}) != len(rows):
        errors.append('BCI-duplicate-artifact-or-template')
    for group in ('checklists', 'reviewPasses'):
        values = [r['id'] for r in catalog[group]]
        if len(values) != len(set(values)):
            errors.append('BCI-duplicate-' + group)
    # Only reference-bearing documents need projection here. Cases/fixtures are
    # byte-bound and checked by their existing chapter owners.
    names = sorted({INDEX, *(r[k] for r in rows for k in ('template', 'chapter'))})
    projection = projection or project_documents({n: inputs[n] for n in names})
    errors += ['BCI-parent-projection: ' + d.code for d in projection.diagnostics]
    documents = {d.document_id: d for d in projection.documents}
    actual = [f.text for f in documents[INDEX].fields if f.element_kind == 'table_row']
    expected = ['Artifact Index ID 成果物 主な章 テンプレート ' + r['artifactId'] + ' '
                + r['title'] + ' ' + ', '.join(map(str, r['indexedChapters'])) + ' '
                + r['template'] for r in rows]
    if actual != expected:
        errors.append('BCI-live-index-agreement')
    site = strict(inputs['site-pages.json'])
    static = {r['source']: r['destination'] for r in site['staticFiles']}
    for row in rows:
        aid = row['artifactId']
        if (not row['template'].startswith('templates/') or not row['example'].startswith('cases/')
                or '/fixtures/' in row['example'] or not row['chapter'].startswith('manuscript/')):
            errors.append('BCI-role-path: ' + aid)
        for role, ref in [*row['fieldRefs'].items(), ('learningObjective', row['learningObjective']),
                          ('chapterDoD', row['chapterDoD'])]:
            expected_path = row['chapter'] if role in ('learningObjective', 'chapterDoD') else row['template']
            document = documents.get(ref['path'])
            if (ref['path'] != expected_path or document is None
                    or sum(f.field_type == 'hidden_metadata' and f.element_kind == 'heading'
                           and f.text == ref['anchor'] for f in document.fields) != 1):
                errors.append('BCI-field-reference: ' + aid + '/' + role)
        fs = row['fixtures']
        if len({f['path'] for f in fs}) != len(fs):
            errors.append('BCI-duplicate-fixture: ' + aid)
        for fixture in fs:
            if (not fixture['path'].startswith('cases/fixtures/')
                    or static.get(fixture['path']) != fixture['download']):
                errors.append('BCI-fixture-download: ' + aid)
    for row in catalog['checklists']:
        if (not set(row['artifacts']) <= set(ids)
                or len(row['artifacts']) != len(set(row['artifacts']))):
            errors.append('BCI-checklist-reference: ' + row['id'])
    return errors


def link(ref, label):
    return f"[{label}](../{ref['path']}#{ref['anchor']})"


def render(catalog):
    """No clock, filesystem, renderer or workflow decisions in generation."""
    b, c, i = [], [], []
    for r in catalog['artifacts']:
        aid = r['artifactId']
        b += [f"### {aid} {r['title']}", '',
              f"- 目的: {r['purpose']}。", f"- 入力: {r['inputs']}。", f"- 出力: {r['outputs']}。",
              f"- 主担当章: [第{r['primaryOwnerChapter']}章](../{r['chapter']})。主索引の関連章: "
              + '、'.join(map(str, r['indexedChapters'])) + '。',
              f"- Template（空欄）: [元Template](../{r['template']})。",
              f"- Example（合成記入例）: [記入内容と境界](../{r['example']})。"]
        if r['fixtures']:
            for number, f in enumerate(r['fixtures'], 1):
                b.append(f"- Fixture {number}（供給合成入力）。"
                         + (f"[Download / 読み取り専用JSON](../{f['path']})。" if f['download']
                            else 'Download登録なし。記入例から確認する。'))
        else:
            b.append('- Fixture / Download: 独立したJSONの登録なし。上の合成記入例を読む。')
        for role, label in zip(ROLES, LABELS):
            ref = r['fieldRefs'][role]
            b.append(f"- {link(ref, label)}: {ref['note']}")
        b += ['']
        i += [f"### {aid}の評価対応", '',
              f"- Learning Objective: {link(r['learningObjective'], '主担当章の学習目標')}。",
              f"- Artifact Evidence: [空Template](../{r['template']})と"
              f"[合成記入例](../{r['example']})を対比し、自分の記録の根拠箇所を示す。",
              f"- Chapter DoD: {link(r['chapterDoD'], '完成条件・評価基準')}。{r['chapterDoD']['note']}",
              f"- Review / Reassessment: {link(r['fieldRefs']['review'], '確認先')} / "
              f"{link(r['fieldRefs']['reassessment'], '不足を戻す先')}。八観点の対象外には理由を記す。", '']
    for r in catalog['checklists']:
        c += [f"### {r['id']} {r['title']}", '', r['question'], '',
              f"- Automation: {r['automation']}", f"- Limitation: {r['limitation']}",
              f"- Failure action: {r['failureAction']}", f"- Owner: {r['owner']}。",
              '- 戻り先: ' + '、'.join(f'[{a}](../'+next(x['template'] for x in catalog['artifacts']
                                                         if x['artifactId'] == a)+')'
                                      for a in r['artifacts']) + '。', '']
    passes = ['### 八つのReview pass', '']
    for r in catalog['reviewPasses']:
        passes += [f"- {r['id']} {r['title']}: {r['evidence']}"]
    return dict(zip(DOCUMENTS, ['\n'.join(b).rstrip(), '\n'.join(c).rstrip(),
                               '\n'.join(passes + ['', *i]).rstrip()]))


def replace_block(source, generated):
    require(source.count(START) == source.count(END) == 1, 'generation-marker-inventory')
    before, tail = source.split(START)
    previous, after = tail.split(END)
    require(END not in before and START not in after, 'generation-marker-order')
    return before + START + '\n\n' + generated + '\n\n' + END + after


def projected_identity(document):
    return [[f.field_type, f.element_kind, f.attribute, f.metadata_value('level'), f.text, f.location]
            for f in document.fields]


def document_errors(docs, contract, require_snapshot=True):
    require(tuple(docs) == DOCUMENTS, 'document-inventory')
    projection = project_documents(docs)
    errors = ['BCI-projection: ' + d.code for d in projection.diagnostics]
    for doc in projection.documents:
        for field in doc.fields:
            findings = []
            if is_policy_scan_field(field):
                findings += scan_action_text(field.normalized_text, location=field.location)
            if is_policy_scan_field(field) or (field.field_type == 'destination'
                    and is_absolute_destination(field.normalized_text)):
                findings += scan_host_policy(field.normalized_text, location=field.location)
            errors += ['BCI-safety: ' + f.category + ': ' + f.location for f in findings]
        identity = json.dumps(projected_identity(doc), ensure_ascii=False, separators=(',', ':'))
        if require_snapshot and digest(identity) != contract['documents'].get(doc.document_id):
            errors.append('BCI-reader-review-required: ' + doc.document_id)
    return errors


def integration_errors(inputs, contract):
    require(contract['version'] == '1.0.0' and contract['projection'] == PROJECTION_VERSION
            and contract['policy'] == POLICY_VERSION and tuple(contract['documents']) == DOCUMENTS,
            'contract-identity')
    site = strict(inputs['site-pages.json'])
    errors = []
    for r in contract['routes']:
        if (site['pages'].count(r) != 1 or sum(
                p['source'] == r['source'] or p['destination'] == r['destination']
                or (p['section'], p['order']) == (r['section'], r['order'])
                for p in site['pages']) != 1):
            errors.append('BCI-route: ' + r['source'])
    if [r['source'] for r in contract['routes']] != list(DOCUMENTS):
        errors.append('BCI-route-inventory')
    scripts = strict(inputs['package.json'])['scripts']
    sync = scripts['sync:docs'].split(' && ')
    if (scripts.get('check:appendix-bci') != COMMAND + ' && python3 tests/test_appendix_bci.py'
            or scripts['test'].split(' && ').count('npm run check:appendix-bci') != 1
            or sync.count(COMMAND) != 1
            or sync.index(COMMAND) >= sync.index('python3 scripts/sync_book_site.py --output docs')):
        errors.append('BCI-entrypoints')
    return errors


def load_inputs(root=ROOT):
    contract = strict(read_input(root, CONTRACT, (CONTRACT,)))
    names = {*DOCUMENTS, CATALOG, 'site-pages.json', 'package.json', *contract['parentDigests']}
    require(len(names) <= 250, 'input-count')
    return {n: read_input(root, n, names) for n in sorted(names)}, contract


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='explicitly regenerate marked blocks only')
    args = parser.parse_args()
    try:
        inputs, contract = load_inputs()
        catalog = strict(inputs[CATALOG])
        errors = manifest_errors(catalog, inputs, contract) + integration_errors(inputs, contract)
        require(not errors, '; '.join(errors))
        expected = {n: replace_block(inputs[n], block) for n, block in render(catalog).items()}
        errors += document_errors(expected if args.write else {n: inputs[n] for n in DOCUMENTS},
                                  contract, require_snapshot=not args.write)
        if not args.write:
            errors += ['BCI-generated-drift: ' + n for n in DOCUMENTS if inputs[n] != expected[n]]
        require(not errors, '; '.join(errors))
        if args.write:
            for name in DOCUMENTS:
                if inputs[name] != expected[name]:
                    (ROOT / name).write_text(expected[name], encoding='utf-8')
        print(f"Appendix B/C/I passed: {len(catalog['artifacts'])} live artifacts; "
              f"{len(contract['parentDigests'])} parent bindings; Policy {POLICY_VERSION}; "
              f"Projection {PROJECTION_VERSION}; " + ('blocks written' if args.write else 'read-only'))
        return 0
    except (OSError, ValueError, TypeError, KeyError, RuntimeError) as exc:
        print(f'Appendix B/C/I failed closed: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
