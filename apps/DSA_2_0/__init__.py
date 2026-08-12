# Installs the real app from https://github.com/MatrixBOX-dev/DSA_2_0 on first run
from __main__ import *

_RAW = "https://raw.githubusercontent.com/MatrixBOX-dev/DSA_2_0/refs/heads/main/"
_API = "https://api.github.com/repos/MatrixBOX-dev/DSA_2_0/git/trees/main?recursive=1"
_DIR = "/DSA_2_0"
_MARKER = _DIR + "/.installed"

try:
    open(_MARKER).close()
except:
    pprint("Installing DSA 2.0...", 0)
    r = requests.get(_API, headers={"User-Agent": "MatrixBOX"}, timeout=10)
    tree = json.loads(r.text)["tree"]
    r.close()
    for item in tree:
        if item["type"] != "blob": continue
        path = item["path"]
        parts = path.split("/")
        if len(parts) > 1:
            d = _DIR
            for p in parts[:-1]:
                d += "/" + p
                try: os.mkdir(d)
                except: pass
        r = requests.get(_RAW + path, timeout=10)
        ext = path.rsplit(".", 1)[-1] if "." in path else ""
        mode = "wb" if ext in ("mpy", "bin", "bmp", "png", "gif", "jpg") else "w"
        with open(_DIR + "/" + path, mode) as f:
            f.write(r.content if mode == "wb" else r.text)
        r.close()
    with open(_MARKER, "w") as f: f.write("")
    pprint("Done! Restarting...", 0)
    microcontroller.reset()

exec(open(_DIR + "/__init__.py").read())