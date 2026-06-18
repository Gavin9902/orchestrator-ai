#!/usr/bin/env python3
"""Chrome DevTools Protocol: screenshot each section of pitch.html, then make GIF."""
import json, time, base64, subprocess, os, sys

HTML = os.path.abspath("pitch.html")
FRAMES_DIR = "pitch_frames"
GIF_OUT = "pitch.gif"
CDP_PORT = 9222

os.makedirs(FRAMES_DIR, exist_ok=True)

# Start Chrome headless
proc = subprocess.Popen([
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--headless=new", f"--remote-debugging-port={CDP_PORT}",
    "--window-size=1200,675", f"file://{HTML}"
], stderr=subprocess.DEVNULL)
time.sleep(3)

try:
    import websocket
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "websocket-client", "-q"])
    import websocket

# Get websocket URL
import urllib.request
tabs = json.loads(urllib.request.urlopen(f"http://localhost:{CDP_PORT}/json").read())
ws_url = tabs[0]["webSocketDebuggerUrl"]
ws = websocket.create_connection(ws_url)
msg_id = 1

def cdp(method, params=None):
    global msg_id
    msg = {"id": msg_id, "method": method, "params": params or {}}
    ws.send(json.dumps(msg))
    msg_id += 1
    while True:
        resp = json.loads(ws.recv())
        if resp.get("id") == msg_id - 1:
            return resp.get("result", {})

def js(expr):
    r = cdp("Runtime.evaluate", {"expression": expr})
    return r.get("result", {}).get("value")

# Get section count
n = js("document.querySelectorAll('section, .footer').length")
print(f"Found {n} sections")

for i in range(n):
    js(f"document.querySelectorAll('section, .footer')[{i}].scrollIntoView({{behavior:'instant'}})")
    time.sleep(1.2)
    r = cdp("Page.captureScreenshot", {"format": "png"})
    img = base64.b64decode(r["data"])
    fname = f"{FRAMES_DIR}/slide_{i:02d}.png"
    with open(fname, "wb") as f:
        f.write(img)
    print(f"  Section {i}: {len(img)/1024:.0f}KB")

ws.close()
proc.terminate()

# Make GIF with Pillow
from PIL import Image
frames = sorted(f for f in os.listdir(FRAMES_DIR) if f.endswith(".png"))
imgs = [Image.open(f"{FRAMES_DIR}/{f}").convert("RGB") for f in frames]

# Check actual image height
first = imgs[0]
h = first.height
print(f"Each frame: {first.width}x{h}")

if len(imgs) > 1:
    imgs[0].save(GIF_OUT, save_all=True, append_images=imgs[1:],
                 duration=5000, loop=0, optimize=True)
    mb = os.path.getsize(GIF_OUT) / 1024 / 1024
    print(f"GIF: {GIF_OUT} ({mb:.1f} MB, {len(imgs)} frames)")
else:
    print("Only 1 frame, skipping GIF")
