#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
echo "[deploy] repo root: $ROOT"

# Quick checks
if ! command -v git >/dev/null 2>&1; then
  echo "git not found — install git first" >&2
  exit 1
fi

if ! command -v git-lfs >/dev/null 2>&1; then
  echo "warning: git-lfs not found. If your repo uses LFS, install it with 'brew install git-lfs' and run 'git lfs install'"
fi

# Run safe push which normalizes/validates/regenerates and pushes
bash Tools_push/push_safe.sh

echo "[deploy] done"
