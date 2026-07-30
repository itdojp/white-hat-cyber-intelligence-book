#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
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


def render() -> str:
    data = json.loads(REGISTRY.read_text(encoding='utf-8'))
    lines = [
        '# Reference Baseline',
        '',
        f'確認基準日: **{data["checkedAt"]}**',
        '',
        'このファイルは`references/sources.json`から生成します。機械可読の正本を直接更新し、このファイルを手編集しないでください。本文へ採用する際は、章Issueで再確認します。',
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
