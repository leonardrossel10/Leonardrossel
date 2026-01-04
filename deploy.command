#!/usr/bin/env bash
# deploy.command — double-clickable helper for macOS
# Place in the project root, make executable: chmod +x deploy.command
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

echo "[deploy.command] Running Tools_push/deploy.sh"
if [ ! -f Tools_push/deploy.sh ]; then
  echo "Tools_push/deploy.sh not found. Aborting." >&2
  exit 1
fi

bash Tools_push/deploy.sh || {
  echo "[deploy.command] deploy script failed." >&2
}

echo "[deploy.command] Finished. Press Enter to close."
read -r
