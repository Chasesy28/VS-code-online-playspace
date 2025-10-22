# VS-code-online-playspace
This is sillly (made at tam high)

## Running the Snake game (pygame)

This repo includes two Snake versions: `Silly.py` (turtle/Tkinter) and `snake_pygame.py` (pygame).

To run `snake_pygame.py` locally (recommended on a desktop):

1. Install dependencies:

```bash
python3 -m pip install --user pygame
```

2. Run:

```bash
python3 snake_pygame.py
```

Running inside a headless container

If you're inside a headless container (no $DISPLAY), you can run a quick headless test using `xvfb-run` or the SDL dummy video driver. Note: headless runs won't be interactive unless you also run a VNC/noVNC session.

Using xvfb-run:

```bash
sudo apt update
sudo apt install -y xvfb
xvfb-run -s "-screen 0 600x600x24" python3 snake_pygame.py
```

Or use SDL dummy (requires pygame present). This runs briefly and exits (useful for CI/headless smoke tests):

```bash
export SDL_VIDEODRIVER=dummy
export HEADLESS=1
python3 snake_pygame.py
```

Running interactively in a browser via VNC / noVNC

1. Install the VNC dependencies and fetch noVNC (run as root):

```bash
sudo ./setup_vnc.sh
```

2. Start the GUI stack (Xvfb + fluxbox + x11vnc + noVNC):

```bash
sudo ./tart-gui.sh
```

3. Open your browser and go to:

```
http://<host>:6080/vnc.html
```

Replace <host> with the container/host IP or localhost if you're running locally. The page will open a VNC window where you can run `python3 snake_pygame.py` inside the desktop.

Password-protected VNC
- You can create a project-scoped VNC password file at `.vnc/passwd` using `x11vnc -storepasswd`. If present, `tart-gui.sh` will use it automatically. Example:

```bash
# create the password file (enter the password when prompted or pass it on the command line)
x11vnc -storepasswd Silly .vnc/passwd
```

When connecting via a VNC client or the noVNC browser UI you'll be prompted for the password (in this repo the example password is `Silly`).

Notes and caveats:
- `setup_vnc.sh` installs system packages (xvfb, x11vnc, fluxbox) and clones noVNC into `/opt/noVNC`.
- This repository contains a sample project password file by default for convenience; it is hashed but still lives in the workspace. If you don't want it tracked in git, add `.vnc/` to `.gitignore` (see `.gitignore` in this repo).
- If you expose ports publicly, lock them down or use SSH port forwarding.
- If you prefer not to run as root, edit `setup_vnc.sh` accordingly and choose a different install path for noVNC.

