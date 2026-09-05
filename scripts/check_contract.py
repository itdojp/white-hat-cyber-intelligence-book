#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
WARNINGS: list[str] = []

EXCLUDED_DIRECTORY_NAMES = {
    '.bundle',
    '.cache',
    '.git',
    '.jekyll-cache',
    '.sass-cache',
    '.tmp',
    '.venv',
    '.work',
    '__pycache__',
    '_site',
    'build',
    'coverage',
    'dist',
    'docs',
    'node_modules',
    'tmp',
    'vendor',
    'venv',
}
BINARY_SUFFIXES = {
    '.7z',
    '.avi',
    '.bin',
    '.bmp',
    '.class',
    '.db',
    '.dll',
    '.dylib',
    '.eot',
    '.exe',
    '.gif',
    '.gz',
    '.ico',
    '.jar',
    '.jpeg',
    '.jpg',
    '.mov',
    '.mp3',
    '.mp4',
    '.o',
    '.otf',
    '.pcap',
    '.pcapng',
    '.pdf',
    '.png',
    '.so',
    '.sqlite',
    '.tar',
    '.ttf',
    '.wav',
    '.webm',
    '.webp',
    '.woff',
    '.woff2',
    '.xz',
    '.zip',
}
SOURCE_ID_RE = re.compile(r'\bSRC-[A-Z0-9-]+\b')
CHAPTER_FILENAME_RE = re.compile(r'^(?:ch)?(?P<number>\d{2})(?:[-_].*)?$')


def error(message: str) -> None:
    ERRORS.append(message)


def warning(message: str) -> None:
    WARNINGS.append(message)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        error(f'{path.relative_to(ROOT)}: invalid JSON: {exc}')
        return {}


def parse_date(value: object, label: str, *, nullable: bool = False) -> date | None:
    if value is None and nullable:
        return None
    if not isinstance(value, str):
        error(f'{label}: expected ISO date string' + (' or null' if nullable else ''))
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        error(f'{label}: invalid ISO date: {exc}')
        return None


def check_local_links(markdown_files: list[Path]) -> None:
    link_re = re.compile(r'!?\[[^\]]*\]\(([^)]+)\)')
    for path in markdown_files:
        in_fence = False
        for line_no, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
            if line.strip().startswith('```'):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for raw in link_re.findall(line):
                token = raw.strip().split(maxsplit=1)[0].strip('<>')
                parsed = urlparse(token)
                if not token or token.startswith('#') or parsed.scheme or token.startswith('//'):
                    continue
                target = unquote(parsed.path)
                if not target:
                    continue
                candidate = (path.parent / target).resolve()
                try:
                    candidate.relative_to(ROOT.resolve())
                except ValueError:
                    error(f'{path.relative_to(ROOT)}:{line_no}: link escapes repository: {token}')
                    continue
                if not candidate.exists():
                    error(f'{path.relative_to(ROOT)}:{line_no}: missing local link target: {token}')


def is_excluded_repository_path(relative_path: Path) -> bool:
    return any(part in EXCLUDED_DIRECTORY_NAMES for part in relative_path.parts)


def repository_files() -> list[Path]:
    """Return tracked and non-ignored worktree files without installed/generated trees."""
    try:
        result = subprocess.run(
            [
                'git',
                '-C',
                str(ROOT),
                'ls-files',
                '-z',
                '--cached',
                '--others',
                '--exclude-standard',
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        relative_paths = result.stdout.decode('utf-8').split('\0')
    except (OSError, subprocess.CalledProcessError, UnicodeDecodeError) as exc:
        warning(f'git file enumeration unavailable; using filesystem fallback: {exc}')
        relative_paths = [
            path.relative_to(ROOT).as_posix()
            for path in ROOT.rglob('*')
            if path.is_file()
        ]

    files: list[Path] = []
    seen: set[str] = set()
    for raw in relative_paths:
        if not raw or raw in seen:
            continue
        seen.add(raw)
        relative = Path(raw)
        if is_excluded_repository_path(relative):
            continue
        candidate = ROOT / relative
        if candidate.is_file():
            files.append(candidate)
    return sorted(files, key=lambda path: path.relative_to(ROOT).as_posix())


def read_plausibly_textual_files(paths: list[Path]) -> dict[Path, str]:
    """Decode every tracked, non-binary file, including scripts without extensions."""
    output: dict[Path, str] = {}
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() in BINARY_SUFFIXES:
            continue
        data = path.read_bytes()
        if b'\x00' in data:
            error(f'{relative}: NUL character detected in non-binary tracked file')
            continue
        try:
            output[path] = data.decode('utf-8')
        except UnicodeDecodeError:
            warning(f'{relative}: skipped non-UTF-8 tracked file; classify it explicitly if textual')
    return output


def chapter_number_from_path(path: Path) -> int | None:
    match = CHAPTER_FILENAME_RE.fullmatch(path.stem)
    if not match:
        return None
    return int(match.group('number'))


required_files = [
    'README.md',
    'AGENTS.md',
    'MAINTENANCE.md',
    'index.md',
    'title.md',
    'copyright.md',
    'preface.md',
    'afterword.md',
    'colophon.md',
    'BOOK_PROPOSAL.md',
    'TOC.md',
    'CROSS_BOOK_MAP.md',
    'WRITING_GUIDE.md',
    'SOURCE_POLICY.md',
    'SAFETY_SCOPE.md',
    'LAB_ARCHITECTURE.md',
    'CANONICAL_SOURCE.md',
    'LICENSE.md',
    'SECURITY.md',
    'CONTRIBUTING.md',
    'THIRD_PARTY_NOTICES.md',
    'book-config.json',
    'package.json',
    'package-lock.json',
    'Gemfile',
    'Gemfile.lock',
    'REPRESENTATIVE_CHAPTER_PLAN.md',
    'EDITORIAL_INPUT_MANIFEST.md',
    'editorial-input-manifest.json',
    'schemas/editorial-input-manifest.schema.json',
    'scripts/check_editorial_input_manifest.py',
    'tests/fixtures/editorial-input/manifest-regressions.json',
    'tests/fixtures/editorial-input/registration-snapshot.json',
    '.book-formatter/revision.json',
    '.github/workflows/contract.yml',
    '.github/workflows/book-qa.yml',
    '.github/workflows/pages.yml',
    'references/sources.json',
    'references/source-note-schema.json',
    'references/reference-baseline.md',
    'scripts/sync_site_source.py',
    'scripts/check_built_site.py',
    'scripts/check_shared_version.py',
    'scripts/check_workflows.py',
    'manuscript/00-reading-guide.md',
    'manuscript/01-integrated-discipline.md',
]
for rel in required_files:
    if not (ROOT / rel).is_file():
        error(f'missing required file: {rel}')

config = load_json(ROOT / 'book-config.json')
if config:
    expected_repo = 'https://github.com/itdojp/white-hat-cyber-intelligence-book'
    if config.get('title') != 'ホワイトハッカーとサイバーインテリジェンス実践体系':
        error('book-config.json: unexpected title')
    if config.get('version') != '0.1.0':
        error('book-config.json: version must be 0.1.0 during bootstrap')
    if config.get('license') != 'CC BY-NC-SA 4.0':
        error('book-config.json: unexpected content license')
    if config.get('repository', {}).get('url') != expected_repo:
        error('book-config.json: repository URL mismatch')
    if config.get('repository', {}).get('branch') != 'main':
        error('book-config.json: repository branch must be main')
    if config.get('ux', {}).get('profile') != 'B':
        error('book-config.json: ux.profile must be B')
    expected_modules = {
        'quickStart', 'readingGuide', 'checklistPack', 'troubleshootingFlow',
        'conceptMap', 'figureIndex', 'legalNotice', 'glossary',
    }
    modules = config.get('ux', {}).get('modules', {})
    if set(modules) != expected_modules:
        error(f'book-config.json: module keys mismatch: {sorted(set(modules) ^ expected_modules)}')
    if not all(modules.values()):
        error('book-config.json: all selected Profile B modules must be true')
    chapters = config.get('structure', {}).get('chapters', [])
    ids = [item.get('id') for item in chapters]
    if len(chapters) != 30:
        error(f'book-config.json: expected 30 chapters, got {len(chapters)}')
    if len(ids) != len(set(ids)):
        error('book-config.json: duplicate chapter IDs')
    if any(not isinstance(item, str) or not re.fullmatch(r'[a-z0-9-]+', item) for item in ids):
        error('book-config.json: invalid chapter ID')
    for item in chapters:
        if not item.get('objectives'):
            error(f'book-config.json: chapter {item.get("id")} has no objectives')

expected_package_license = '(CC-BY-NC-SA-4.0 AND Apache-2.0)'
package = load_json(ROOT / 'package.json')
if package and package.get('license') != expected_package_license:
    error(f'package.json: license must be {expected_package_license}')

package_lock = load_json(ROOT / 'package-lock.json')
if package_lock:
    lock_license = package_lock.get('packages', {}).get('', {}).get('license')
    if lock_license != expected_package_license:
        error(f'package-lock.json: root package license must be {expected_package_license}')

revision = load_json(ROOT / '.book-formatter/revision.json')
if revision:
    if revision.get('commit') != '198935ff8f60653c40e513343dc5f02573d9968e':
        error('.book-formatter/revision.json: unexpected pinned book-formatter commit')
    if revision.get('schema', {}).get('blobSha') != '87dcb44b0d4b543ba43ae3a8ebc27d2f3cfda3cd':
        error('.book-formatter/revision.json: unexpected schema blob SHA')

registry = load_json(ROOT / 'references/sources.json')
source_chapters: dict[str, set[int]] = {}
if registry:
    ids: set[str] = set()
    check_date_raw = os.environ.get('CHECK_DATE')
    today = parse_date(check_date_raw, 'CHECK_DATE') if check_date_raw else date.today()
    registry_checked = parse_date(registry.get('checkedAt'), 'references/sources.json.checkedAt')
    if registry_checked and today and registry_checked > today:
        warning('references/sources.json: checkedAt is later than the runner date')
    for source in registry.get('sources', []):
        sid = source.get('id')
        if not isinstance(sid, str) or not re.fullmatch(r'SRC-[A-Z0-9-]+', sid):
            error(f'references/sources.json: invalid source ID {sid!r}')
            continue
        if sid in ids:
            error(f'references/sources.json: duplicate source ID {sid}')
        ids.add(sid)
        for field in (
            'publisher', 'title', 'kind', 'status', 'version', 'url', 'publishedAt',
            'checkedAt', 'nextReviewAt', 'reviewTriggers', 'chapters', 'notes',
        ):
            if field not in source:
                error(f'{sid}: missing {field}')
        if not str(source.get('url', '')).startswith('https://'):
            error(f'{sid}: URL must use https')
        published = parse_date(source.get('publishedAt'), f'{sid}.publishedAt', nullable=True)
        checked = parse_date(source.get('checkedAt'), f'{sid}.checkedAt')
        review = parse_date(source.get('nextReviewAt'), f'{sid}.nextReviewAt')
        if published and checked and published > checked:
            error(f'{sid}: publishedAt is later than checkedAt')
        if checked and review and review < checked:
            error(f'{sid}: nextReviewAt precedes checkedAt')
        if review and today and review < today:
            warning(f'{sid}: source review is overdue')
        chapters = source.get('chapters')
        valid_chapters = (
            isinstance(chapters, list)
            and all(isinstance(ch, int) and 0 <= ch <= 29 for ch in chapters)
        )
        if not valid_chapters:
            error(f'{sid}: chapters must contain integers from 0 through 29')
        else:
            source_chapters[sid] = set(chapters)
        if not isinstance(source.get('reviewTriggers'), list) or not source.get('reviewTriggers'):
            error(f'{sid}: reviewTriggers must be a non-empty list')

repository_file_list = repository_files()
text_by_path = read_plausibly_textual_files(repository_file_list)
text_files = sorted(text_by_path, key=lambda path: path.relative_to(ROOT).as_posix())

for workflow in sorted((ROOT / '.github' / 'workflows').glob('*.y*ml')):
    if workflow.is_file() and workflow not in text_by_path:
        error(f'{workflow.relative_to(ROOT)}: workflow is not included in repository text scanning')
for path in text_files:
    relative = path.relative_to(ROOT)
    if is_excluded_repository_path(relative):
        error(f'{relative}: installed or generated path was included in repository text scanning')

secret_patterns = [
    re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    re.compile(r'AKIA[0-9A-Z]{16}'),
    re.compile(r'ASIA[0-9A-Z]{16}'),
    re.compile(r'gh[pousr]_[A-Za-z0-9_]{20,}'),
    re.compile(r'github_pat_[A-Za-z0-9_]{20,}'),
]
private_ipv4 = re.compile(
    r'\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|'
    r'172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b'
)
allowed_private_paths = {'LAB_ARCHITECTURE.md'}
for path, text in text_by_path.items():
    rel = path.relative_to(ROOT).as_posix()
    for pattern in secret_patterns:
        if pattern.search(text):
            error(f'{rel}: possible secret pattern detected')
    if rel not in allowed_private_paths and private_ipv4.search(text):
        warning(f'{rel}: private address example found; verify it is synthetic and necessary')
    stale_config_name = 'book-config' + '.draft.json'
    if stale_config_name in text:
        error(f'{rel}: stale draft config reference')
    for line_no, line in enumerate(text.splitlines(), 1):
        if line.endswith((' ', '\t')):
            error(f'{rel}:{line_no}: trailing whitespace detected')

markdown_files = [path for path in text_files if path.suffix.lower() == '.md']
for path in markdown_files:
    text = text_by_path[path]
    headings = [line for line in text.splitlines() if line.startswith('#')]
    if not headings:
        error(f'{path.relative_to(ROOT)}: no Markdown heading')
    fences = sum(1 for line in text.splitlines() if line.strip().startswith('```'))
    if fences % 2:
        error(f'{path.relative_to(ROOT)}: unbalanced code fence')
check_local_links(markdown_files)

for chapter in sorted((ROOT / 'manuscript').glob('*.md')):
    text = chapter.read_text(encoding='utf-8')
    for heading in (
        'この章の位置付け',
        '学習目標',
        '前提知識',
        '章のまとめ',
        '次に学ぶこと',
        '参考文献・Source Note ID',
    ):
        if f'## {heading}' not in text:
            error(f'{chapter.relative_to(ROOT)}: missing standard heading: {heading}')

    chapter_number = chapter_number_from_path(chapter)
    if chapter_number is None:
        warning(f'{chapter.relative_to(ROOT)}: cannot derive chapter number for source mapping validation')
        continue
    for source_id in sorted(set(SOURCE_ID_RE.findall(text))):
        registered_chapters = source_chapters.get(source_id)
        if registered_chapters is None:
            error(f'{chapter.relative_to(ROOT)}: unknown Source Note ID {source_id}')
        elif chapter_number not in registered_chapters:
            error(
                f'{chapter.relative_to(ROOT)}: {source_id} cites chapter {chapter_number}, '
                'but references/sources.json does not register that chapter'
            )

print(
    f'checked repository contract: {len(required_files)} required files, '
    f'{len(registry.get("sources", []))} sources, '
    f'{len(text_files)} textual tracked files, {len(markdown_files)} Markdown files'
)
for item in WARNINGS:
    print(f'WARNING: {item}')
for item in ERRORS:
    print(f'ERROR: {item}')
if ERRORS:
    sys.exit(1)
print('PASS')
