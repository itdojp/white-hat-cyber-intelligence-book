#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import date
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / 'references' / 'sources.json'
OUTPUT = ROOT / 'references' / 'reference-baseline.md'


def display_version(source: dict) -> str:
    version = source.get('version')
    status = source.get('status')
    if version:
        return f'{version} / {status}'
    return str(status)


def appendix_review_rows(data: dict) -> list[str]:
    """Render declared dependencies, not inferred chapter numbers or legal approval."""
    rows = []
    for source in data['sources']:
        if 'appendixReview' not in source:
            continue
        review = source['appendixReview']
        if not isinstance(review, dict) or set(review) != {'checkedAt', 'targets', 'note'}:
            raise ValueError('invalid appendixReview fields')
        checked, targets, note = review['checkedAt'], review['targets'], review['note']
        if not isinstance(checked, str):
            raise ValueError('invalid appendix review date')
        if date.fromisoformat(checked).isoformat() != checked:
            raise ValueError('non-canonical appendix review date')
        allowed = {'appendix-' + letter for letter in 'abcdefghij'}
        if (not isinstance(targets, list) or not targets
                or any(not isinstance(t, str) or t not in allowed for t in targets)
                or len(set(targets)) != len(targets)):
            raise ValueError('invalid appendix review targets')
        if not isinstance(note, str) or not re.fullmatch(r'references/[a-z0-9][a-z0-9-]*\.md', note):
            raise ValueError('invalid appendix review note path')
        labels = '・'.join(t[-1].upper() for t in targets)
        rows.append(f'| {source["id"]} | {checked} | {labels} | '
                    f'[限定確認]({Path(note).name}) |')
    return rows


def render(data: dict | None = None) -> str:
    if data is None:
        data = json.loads(REGISTRY.read_text(encoding='utf-8'))
    lines = [
        '# Reference Baseline',
        '',
        f'Registry全体の最終一括監査日: **{data["checkedAt"]}**',
        '',
        'このファイルは`references/sources.json`から生成します。機械可読の正本を直接更新し、このファイルを手編集しないでください。各行の確認日は個別Source Noteの最終確認日であり、本文へ採用する際は章Issueで再確認します。',
        '',
        '| ID | 発行主体 | 文書 | 版・状態 | 確認日 | 次回確認 | 主な章 |',
        '|---|---|---|---|---|---|---|',
    ]
    for source in data['sources']:
        chapters = ', '.join(str(item) for item in source.get('chapters', []))
        title = str(source['title']).replace('|', '\\|')
        publisher = str(source['publisher']).replace('|', '\\|')
        version = display_version(source).replace('|', '\\|')
        lines.append(
            f'| {source["id"]} | {publisher} | [{title}]({source["url"]}) | '
            f'{version} | {source["checkedAt"]} | {source["nextReviewAt"]} | {chapters} |'
        )
    appendix_rows = appendix_review_rows(data)
    if appendix_rows:
        lines.extend([
            '', '## 付録の用途限定確認', '',
            '対象は記載の付録・節だけです。全Source・全章・個別事案の適法性を再監査した日付ではありません。過去の章監査とCaseの時点・権限を更新せず、変更時は既存の章mappingと下表の付録を確認します。',
            '', '| ID | 用途限定確認日 | 対象付録 | 採用範囲・非採用・履歴 |',
            '|---|---|---|---|', *appendix_rows,
        ])
    lines.extend([
        '',
        '## 運用',
        '',
        '- `continuous-data`の個別値を安定本文へ固定しない',
        '- 版変更時は`reviewTriggers`から影響章を再監査する',
        '- 日付が不明な場合は推測せず`null`とする',
        '- 法令、開示ガイド、AI標準は公開直前にも再確認する',
        '',
    ])
    return '\n'.join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    expected = render()
    if args.check:
        actual = OUTPUT.read_text(encoding='utf-8') if OUTPUT.exists() else ''
        if actual != expected:
            print('references/reference-baseline.md is out of sync')
            return 1
        print('reference baseline is in sync')
        return 0
    OUTPUT.write_text(expected, encoding='utf-8')
    print(f'wrote {OUTPUT.relative_to(ROOT)}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
