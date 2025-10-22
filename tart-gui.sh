#!/usr/bin/env bash
# Start a lightweight GUI session backed by Xvfb, exposed via x11vnc and noVNC.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DISPLAY_NUM=99
DISPLAY=":${DISPLAY_NUM}"
XVFB_RES="600x600x24"
NO_VNC_DIR="/opt/noVNC"
WEBSOCKIFY_PORT=6080
VNC_PORT=5900

# Optional project VNC password file
VNC_PASS_DIR="$SCRIPT_DIR/.vnc"
VNC_PASS_FILE="$VNC_PASS_DIR/passwd"

export DISPLAY

echo "Starting Xvfb on display $DISPLAY with resolution $XVFB_RES"
Xvfb $DISPLAY -screen 0 $XVFB_RES &
XVFB_PID=$!

sleep 0.5

echo "Starting fluxbox window manager"
fluxbox &
FLUXBOX_PID=$!

sleep 0.5

echo "Starting x11vnc on port $VNC_PORT"
# If a project VNC password file exists, use it; otherwise run without password
if [ -f "$VNC_PASS_FILE" ]; then
  echo "Using VNC password file: $VNC_PASS_FILE"
  x11vnc -display $DISPLAY -rfbauth "$VNC_PASS_FILE" -forever -shared -rfbport $VNC_PORT &
else
  x11vnc -display $DISPLAY -nopw -forever -shared -rfbport $VNC_PORT &
fi
X11VNC_PID=$!

sleep 0.5

if [ -d "$NO_VNC_DIR" ]; then
  echo "Starting noVNC (websockify) on port $WEBSOCKIFY_PORT -> VNC $VNC_PORT"
  # Launch websockify from noVNC utils if present, otherwise rely on system websockify
  if [ -x "$NO_VNC_DIR/utils/novnc_proxy" ]; then
    "$NO_VNC_DIR/utils/novnc_proxy" --vnc localhost:$VNC_PORT --listen $WEBSOCKIFY_PORT &
    WEBSOCKIFY_PID=$!
  else
    # fallback to python websockify if installed
    python3 -m websockify $WEBSOCKIFY_PORT localhost:$VNC_PORT &
    WEBSOCKIFY_PID=$!
  fi
  echo "Open http://<host>:$WEBSOCKIFY_PORT/vnc.html to connect (replace <host>)"
else
  echo "noVNC not found in $NO_VNC_DIR. Run setup_vnc.sh to install it." >&2
fi

cleanup() {
  echo "Stopping processes..."
  kill $WEBSOCKIFY_PID $X11VNC_PID $FLUXBOX_PID $XVFB_PID 2>/dev/null || true
}

trap cleanup EXIT

echo "GUI running. Press Ctrl-C to stop."
wait
