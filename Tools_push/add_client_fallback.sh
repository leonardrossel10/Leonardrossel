#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
echo "[add_client_fallback] repo: $ROOT"

JS=Tools_push/fallback_normalize.js

if [ ! -f "$JS" ]; then
  echo "missing $JS" >&2
  exit 1
fi

for f in index.html gallery.html; do
  if [ -f "$f" ]; then
    if grep -q 'fallback_normalize.js' "$f"; then
      echo "[add_client_fallback] $f already contains fallback include"
    else
      echo "[add_client_fallback] Injecting fallback into $f"
      sed -i.bak '/<\/head>/i\
  <script src="Tools_push/fallback_normalize.js"></script>' "$f"
      rm -f "$f.bak"
    fi
  fi
done

echo '[add_client_fallback] done'
