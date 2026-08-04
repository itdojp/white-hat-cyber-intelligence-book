#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -z "${BOOK_FORMATTER_DIR:-}" ]]; then
  echo "ERROR: BOOK_FORMATTER_DIR must point to the pinned book-formatter checkout" >&2
  exit 2
fi

FORMATTER_DIR="$(cd "$BOOK_FORMATTER_DIR" && pwd)"
EXPECTED_FORMATTER_SHA="$(
  python3 -c 'import json; print(json.load(open(".book-formatter/revision.json", encoding="utf-8"))["commit"])'
)"
ACTUAL_FORMATTER_SHA="$(git -C "$FORMATTER_DIR" rev-parse HEAD)"

if [[ "$ACTUAL_FORMATTER_SHA" != "$EXPECTED_FORMATTER_SHA" ]]; then
  echo "ERROR: book-formatter HEAD does not match the audited pin" >&2
  echo "expected: $EXPECTED_FORMATTER_SHA" >&2
  echo "actual:   $ACTUAL_FORMATTER_SHA" >&2
  exit 2
fi

if [[ -n "$(git -C "$FORMATTER_DIR" status --porcelain=v1 --untracked-files=no)" ]]; then
  echo "ERROR: book-formatter checkout has tracked index or worktree changes" >&2
  exit 2
fi

REPORT_DIR="$ROOT/.tmp/white-hat-book-qa"
mkdir -p "$REPORT_DIR"

npm test
npm run sync:docs

(
  cd "$FORMATTER_DIR"
  npm start -- validate-config --config "$ROOT/book-config.json"
)

node "$FORMATTER_DIR/scripts/check-unicode.js" docs --fail-on error
node "$FORMATTER_DIR/scripts/check-textlint.js" docs --fail-on error
node "$FORMATTER_DIR/scripts/check-links.js" docs
node "$FORMATTER_DIR/scripts/check-layout-risk.js" \
  docs --fail-on error --output "$REPORT_DIR/layout-risk-report.json"
node "$FORMATTER_DIR/scripts/check-markdown-structure.js" \
  docs --fail-on error --output "$REPORT_DIR/markdown-structure-report.json"

JEKYLL_ENV=production \
PAGES_REPO_NWO=itdojp/white-hat-cyber-intelligence-book \
  bundle exec jekyll build \
    --source docs \
    --config docs/_config.yml \
    --destination _site \
    --trace

python3 scripts/check_built_site.py --source docs --site _site
echo "Book QA passed with book-formatter@$ACTUAL_FORMATTER_SHA"
