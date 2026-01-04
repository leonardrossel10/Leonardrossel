#!/usr/bin/env bash
set -euo pipefail
# Simple deploy helper — runs optimization, regeneration, git commit and push
# Usage: just run this script after you copied your new images into the `images/` folders.

REPO="/Users/leonardrossel/Desktop/MonSitePhotos_copie"
OPT_SCRIPT="/Users/leonardrossel/Desktop/MonSitePhotos_tools/optimize_images.py"

cd "$REPO"
echo "[push_photo] Working in $REPO"

if [ ! -f "$OPT_SCRIPT" ]; then
  echo "Optimization script not found: $OPT_SCRIPT" >&2
  echo "Run: python3 -m pip install --user Pillow" >&2
  exit 1
fi

echo "[push_photo] Optimizing up to 50 newest images..."
python3 "$OPT_SCRIPT" --root images --max 50 --max-width 1600 --quality 80 --convert-webp --inplace

echo "[push_photo] Regenerating gallery pages..."
python3 generate_gallery.py
python3 generate_localstorage_seed.py || true

echo "[push_photo] Staging changes..."
git add -A

if git diff --cached --quiet; then
  echo "[push_photo] No changes to commit. Exiting."
  exit 0
fi

MSG="Add/optimize photos and regenerate galleries"
git commit -m "$MSG"
echo "[push_photo] Pushing to origin/main..."
git push origin main

echo "[push_photo] Done. Preview locally with: python3 -m http.server 8000 --bind 127.0.0.1"
