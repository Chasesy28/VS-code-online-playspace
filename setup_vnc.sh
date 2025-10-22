#!/usr/bin/env bash
# Install packages and fetch noVNC for running a browser-accessible VNC session.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "This script installs packages and should be run as root or with sudo." >&2
  echo "Run: sudo $0" >&2
  exit 1
fi

apt update
apt install -y xvfb x11vnc fluxbox xterm wget git python3-pip

# Install websockify (used by noVNC)
python3 -m pip install websockify

NO_VNC_DIR="/opt/noVNC"
if [ ! -d "$NO_VNC_DIR" ]; then
  git clone https://github.com/novnc/noVNC.git "$NO_VNC_DIR"
  git clone https://github.com/novnc/websockify.git "$NO_VNC_DIR/utils/websockify"
fi

echo "noVNC installed in $NO_VNC_DIR"
echo "You can start the GUI with: sudo ./tart-gui.sh" 
