#!/usr/bin/env bash
set -euo pipefail
APP_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$APP_DIR/../.." && pwd)"
STUDIO_PYTHON="$REPO_DIR/local/studio-venv/bin/python"
if [ ! -x "$STUDIO_PYTHON" ]; then
  python3 -m venv "$REPO_DIR/local/studio-venv"
  "$REPO_DIR/local/studio-venv/bin/pip" install -r "$APP_DIR/requirements.txt"
fi
cd "$APP_DIR"
exec "$STUDIO_PYTHON" app.py "$@"
