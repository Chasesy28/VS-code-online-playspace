#!/usr/bin/env bash
# Helper to run snake_pygame under xvfb-run if no display is available.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if command -v xvfb-run >/dev/null 2>&1; then
  xvfb-run -s "-screen 0 600x600x24" python3 "$SCRIPT_DIR/snake_pygame.py"
else
  echo "xvfb-run not found; running directly (requires a display)." >&2
  python3 "$SCRIPT_DIR/snake_pygame.py"
fi
