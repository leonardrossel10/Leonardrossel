#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"
echo "[push_safe] repo root: $ROOT_DIR"

SEED=localstorage_seed.json

if [ -f Tools_push/normalize_seed.py ]; then
  echo "[push_safe] Normalizing seed..."
  python3 Tools_push/normalize_seed.py "$SEED"
fi

if [ -f Tools_push/validate_seed.py ]; then
  echo "[push_safe] Validating seed..."
  python3 Tools_push/validate_seed.py "$SEED"
fi

echo "[push_safe] Regenerating galleries..."
python3 generate_localstorage_seed.py || true
python3 generate_gallery.py || true

echo "[push_safe] Staging changes..."
git add -A
if git diff --cached --quiet; then
  echo "[push_safe] No changes to commit."
  exit 0
fi

git commit -m "Regenerate seed and galleries (normalize seed)"
echo "[push_safe] Pushing to origin/main..."
git push origin main
echo "[push_safe] Done." 
