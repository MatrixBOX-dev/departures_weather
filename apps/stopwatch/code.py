from __main__ import *
import sys, time, gc
import displayio, bitmaptools
import load_screen
from check_button import check_if_button_pressed
from load_screen import *

with open("stopwatch.html") as f: html_body = f.read()

DISP_W = settings["width"]
DISP_H = settings["height"]

try:
    with open("swsettings.txt") as f:
        swsettings = json.loads(f.read())
except:
    swsettings = {}

_DEFAULTS = {
    "fg_hex":     "#00ff88",
    "bg_hex":     "#000000",
    "accent_hex": "#ff4400",
    "mode":       "stopwatch",
    "preset_ms":  60000,
    "show_tenths": 1,
    "scale":       2,
}
for _k, _v in _DEFAULTS.items():
    if _k not in swsettings: swsettings[_k] = _v
def hex_to_rgb(h):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

# Cached RGB for hot-loop palette toggling
_fg_rgb = hex_to_rgb(_DEFAULTS["fg_hex"])
_ac_rgb = hex_to_rgb(_DEFAULTS["accent_hex"])

def apply_colors():
    global _fg_rgb, _ac_rgb
    fg = hex_to_rgb(swsettings["fg_hex"])
    bg = hex_to_rgb(swsettings["bg_hex"])
    ac = hex_to_rgb(swsettings["accent_hex"])
    _fg_rgb = fg
    _ac_rgb = ac
    palette[0]  = (0, 0, 0)
    palette[5]  = fg
    palette[12] = (20, 20, 20)   # progress bar empty track
    palette[14] = bg
    palette[19] = ac

# â”€â”€ State machine â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
SW_STOPPED  = 0
SW_RUNNING  = 1
SW_PAUSED   = 2
SW_FINISHED = 3

sw_state      = SW_STOPPED
sw_elapsed_ms = 0
sw_start_mono = 0.0

def _now_ms():
    if sw_state == SW_RUNNING:
        return int((time.monotonic() - sw_start_mono) * 1000) + sw_elapsed_ms
    return sw_elapsed_ms

def _start():
    global sw_state, sw_start_mono, sw_elapsed_ms
    if swsettings["mode"] == "countdown":
        if sw_elapsed_ms >= int(swsettings["preset_ms"]):
            sw_elapsed_ms = 0
    sw_state      = SW_RUNNING
    sw_start_mono = time.monotonic()

def _pause():
    global sw_state, sw_elapsed_ms
    if sw_state == SW_RUNNING:
        sw_elapsed_ms = _now_ms()
        sw_state = SW_PAUSED

def _reset():
    global sw_state, sw_elapsed_ms, sw_start_mono, _last_draw
    sw_state      = SW_STOPPED
    sw_elapsed_ms = 0
    sw_start_mono = 0.0
    palette[5]    = _fg_rgb
    _last_draw    = ""

def _toggle():
    if   sw_state == SW_RUNNING:  _pause()
    elif sw_state == SW_FINISHED: _reset()
    else:                         _start()

# â”€â”€ Formatting â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def _fmt(ms, tenths=True):
    ms      = max(0, int(ms))
    total_s = ms // 1000
    t       = (ms % 1000) // 100
    h       = total_s // 3600
    m       = (total_s % 3600) // 60
    s       = total_s % 60
    sm      = ("0" + str(m))[-2:]
    ss      = ("0" + str(s))[-2:]
    if h > 0:
        return str(h) + ":" + sm + ":" + ss
    if tenths:
        return sm + ":" + ss + "." + str(t)
    return sm + ":" + ss

# â”€â”€ Web server â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@ampule.route("/exit", method="GET")
def exit_webinterface(request):
    load_settings.app_running = False
    return (200, {}, """<meta http-equiv="refresh" content="0; url=../" />""")

@ampule.route("/", method="GET")
def webinterface(request):
    return (200, {}, header("Stopwatch", app=True) + html_body + footer())

@ampule.route("/settings", method="GET")
def get_settings(request):
    return (200, {}, json.dumps(swsettings))

@ampule.route("/state", method="GET")
def get_state(request):
    ms   = _now_ms()
    disp = max(0, int(swsettings["preset_ms"]) - ms) if swsettings["mode"] == "countdown" else ms
    names = ["stopped", "running", "paused", "finished"]
    return (200, {}, json.dumps({
        "state":     names[sw_state],
        "ms":        disp,
        "mode":      swsettings["mode"],
        "preset_ms": int(swsettings["preset_ms"])
    }))

@ampule.route("/", method="POST")
def post_handler(request):
    global swsettings, _last_draw
    p = request.params
    if "action" in p:
        a = p["action"]
        if   a == "start":  _start()
        elif a == "pause":  _pause()
        elif a == "toggle": _toggle()
        elif a == "reset":  _reset()
    if "preset" in p:
        try:
            raw = p["preset"].replace("%3A", ":").replace("+", " ").strip()
            if ":" in raw:
                pts = raw.split(":")
                if   len(pts) == 2: swsettings["preset_ms"] = (int(pts[0]) * 60 + int(pts[1])) * 1000
                elif len(pts) == 3: swsettings["preset_ms"] = (int(pts[0]) * 3600 + int(pts[1]) * 60 + int(pts[2])) * 1000
            elif raw:
                swsettings["preset_ms"] = max(1000, int(float(raw) * 1000))
        except: pass
    if "mode" in p:
        swsettings["mode"] = p["mode"]
        _reset()
        _last_draw = ""
    if "scale" in p:
        try: swsettings["scale"] = int(p["scale"])
        except: pass
        _last_draw = ""
    if "show_tenths" in p:
        swsettings["show_tenths"] = int(p["show_tenths"])
        _last_draw = ""
    for k in ("fg_hex", "bg_hex", "accent_hex"):
        if k in p:
            swsettings[k] = "#" + p[k]
            apply_colors()
            _last_draw = ""
    if "save" in p:
        try:
            with open("swsettings.txt", "w") as f:
                f.write(json.dumps(swsettings))
        except: pass
    return (200, {}, "ok")

# â”€â”€ Display â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
screen     = None
_last_draw = ""

def rebuild_display():
    global screen, _last_draw
    screen = displayio.Bitmap(DISP_W, DISP_H, 20)
    tg     = displayio.TileGrid(screen, pixel_shader=palette)
    root   = displayio.Group()
    root.append(tg)
    display.root_group = root
    apply_colors()
    _last_draw = ""
    gc.collect()

def draw_stopwatch(ms, state):
    global _last_draw
    show_t  = bool(swsettings["show_tenths"])
    disp_ms = max(0, int(swsettings["preset_ms"]) - ms) if swsettings["mode"] == "countdown" else ms
    dstr    = _fmt(disp_ms, show_t)
    tag     = dstr + str(state)
    if tag == _last_draw:
        return
    _last_draw = tag

    f     = load_screen.currentfont
    fh    = f["fontheight"]
    scale = max(1, int(swsettings.get("scale", 2)))
    tw    = strlen(dstr, f)

    while scale > 1 and (tw * scale > DISP_W - 2 or fh * scale > DISP_H - 4):
        scale -= 1

    tmp = displayio.Bitmap(tw + 2, fh + 2, 20)
    pprint(dstr, 0, font=f, clear=False, color="white",
           top_offset=-1, _refresh=False, window=tmp, _clearscreen=False)

    progress_h = 3 if swsettings["mode"] == "countdown" and int(swsettings["preset_ms"]) > 0 else 0
    bitmaptools.fill_region(screen, 0, 0, DISP_W, DISP_H, 14)

    time_area_h = DISP_H - progress_h
    sh     = fh * scale
    time_y = max((time_area_h - sh) // 2, 0)

    if scale == 1:
        tx = max((DISP_W - tw) // 2, 0)
        bitmaptools.blit(screen, tmp, tx, time_y,
                         x1=0, y1=0, x2=tmp.width, y2=tmp.height,
                         skip_source_index=0)
    else:
        bitmaptools.rotozoom(screen, tmp,
                             ox=DISP_W // 2,
                             oy=time_y + (tmp.height // 2) * scale,
                             px=tmp.width // 2, py=tmp.height // 2,
                             angle=0.0, scale=float(scale),
                             skip_index=0)

    if progress_h:
        total  = int(swsettings["preset_ms"])
        remain = max(0, total - ms)
        bar_w  = int(DISP_W * remain // total) if total > 0 else 0
        bar_y  = DISP_H - progress_h
        bitmaptools.fill_region(screen, 0, bar_y, DISP_W, DISP_H, 12)
        if bar_w > 0:
            bitmaptools.fill_region(screen, 0, bar_y, bar_w, DISP_H, 19)

# â”€â”€ Init â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
rebuild_display()
load_screen.currentfont = font_large

while load_settings.app_running:
    ampule.listen(socket)

    b = check_if_button_pressed()
    if   b == 2: sys.exit()
    elif b == 1: _toggle()

    ms = _now_ms()

    # Countdown finish check
    if swsettings["mode"] == "countdown" and sw_state == SW_RUNNING:
        if ms >= int(swsettings["preset_ms"]):
            sw_elapsed_ms = int(swsettings["preset_ms"])
            sw_state      = SW_FINISHED

    # Flash digits (palette only, no bitmap redraw needed)
    if sw_state == SW_FINISHED:
        palette[5] = _ac_rgb if int(time.monotonic() * 2) % 2 else _fg_rgb
    else:
        palette[5] = _fg_rgb

    draw_stopwatch(ms, sw_state)
    refresh()
    time.sleep(0.05)
