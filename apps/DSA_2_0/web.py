css = ""
try:
    from css import _css as css
except:
    pass

T = {
    "connected": "Connected",
    "not_connected": "Not Connected",
    "title": "Settings",
    "network": "WLAN",
    "password": "Password",
    "connect": "Connect",
    "save": "Save",
    "info": "IP-address:",
    "instructions": "The default IP-address is 192.168.4.1.",
    "_instructions": "",
    "station": "Station",
    "api_provider": "Provider",
}


PAGE_TPL = """<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width,initial-scale=1" charset="UTF-8">
<link href="data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAA/SURBVDhPY2RgYPgPxGQDsAFAAOGRCBgZGREGgDikAJgeJiifbDDwBuAMRPQwwaVmGITBqAHUykwQLjmAgQEA3oYYFR16cP8AAAAASUVORK5CYII=" rel="icon" type="image/x-icon"/>
<title>{TITLE}</title><style>{CSS}</style></head><body>
<div class="container">
<div style="text-align:right"><a href="/exit" style="color:#ff4444;text-decoration:none;font-size:20px">&#x274C;</a></div>
<div class="card" style="text-align:center">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.5rem"><div id="network">{CONN_STATUS}</div></div>
<div class="sh">Dynamische Fahrgastinformation DSA 2.0</div>
<div style="margin-top:.3rem;font-size:.7rem;color:#aaa">{VERSION_TEXT}</div></div>
<div class="card"><small><b>{T_INFO}</b> {IP_DISPLAY}<br><br>More information at <b>www.iregio612.de/eisenbahn/matrixbox-dsa</b><br><br>info@iregio612.de</small></div>
<form method="post" action="/">
<div class="card"><div class="form-row"><div class="col">
<label for="ssid"><a href="#" onclick="doScan();return false">&#128268;</a> {T_NETWORK}</label>
<select id="ssid" class="form-control" name="ssid" data-p="ssid" data-e="change" {NET_DIS}>{SSID_OPTIONS}</select>
</div><div class="col"><label for="password">{T_PASSWORD}</label>
<input type="text" id="password" class="form-control" name="password" placeholder="*******" data-p="password" data-e="blur" data-enc="1" {NET_DIS}>
<div style="text-align:right;margin-top:.5rem">
<button type="button" class="btn btn-outline-secondary btn-sm" id="connect_wifi" data-u="/?connect_wifi=true" data-net="1" {NET_DIS}>{T_CONNECT}</button>
</div></div></div></div>

<div class="card">
<label for="api_provider">{T_API_PROVIDER}</label>
<select id="api_provider" class="form-control"
        name="api_provider"
        data-p="api_provider"
        data-e="change">
    <option value="1" {API_DB_SELECTED}>DB - Deutsche Bahn [only trains / SPNV+SPFV]</option>
    <option value="2" {API_DB_ALL_SELECTED}>DB - Deutsche Bahn [all deps / SPNV+SPFV+ÖPNV]</option>
    <option value="3" {API_VVO_SELECTED}>VVO - Verkehrsverbund Oberelbe</option>
</select>
</div>

<div class="card">
<label for="siteid">{T_STATION}</label>
<input type="text" id="siteid" class="form-control"
       name="siteid"
       value="{STATION_VALUE}"
       data-p="siteid"
       data-e="blur">
<div id="provider_help">
    <small>-</small>
</div>
</div>

<div class="card">
<label for="layout">Layout</label>
<select id="layout" class="form-control"
        name="layout"
        data-p="layout"
        data-e="change">
    <option value="1" {LAYOUT_A_SELECTED}>Layout 1</option>
    <option value="2" {LAYOUT_B_SELECTED}>Layout 2</option>
</select>
</div>

<div class="card">
<label for="utc_offset">UTC ADJUSTMENT</label>
<input type="text" id="utc_offset" class="form-control"
       name="utc_offset"
       value="{UTC_OFFSET_VALUE}"
       data-p="utc_offset"
       data-e="blur">

<label class="sw" style="margin-top:.6rem">
    <input type="checkbox"
           name="summer_time"
           value="1"
           data-p="summer_time"
           data-e="change"
           {SUMMER_TIME_CHECKED}>
    <span>Summer-Time (+1 Hour)</span>
</label>
</div>

<div style="margin-bottom:.6rem">
<button type="button" class="save-btn" data-u="/?save=true">&#128190; {T_SAVE}</button></div>

<script>
function doScan(){fetch('/checknet').then(function(r){return r.text();}).then(function(h){var sel=document.getElementById('ssid');sel.innerHTML=h;sel.disabled=false;document.getElementById('password').disabled=false;document.getElementById('connect_wifi').disabled=false;}).catch(function(){});}

document.querySelectorAll('[data-u],[data-p]').forEach(function(el){
el.addEventListener(el.dataset.e||'click',function(ev){
var u=el.dataset.u;
if(!u){var v=ev.target.value.replace(/#/g,'%23');if(el.dataset.enc)v=encodeURIComponent(v);u='/?'+el.dataset.p+'='+v;}
var f=fetch(u,{method:'GET'});
if(el.dataset.net){f.then(function(r){return r.json()}).then(function(d){
var div=document.getElementById('network');
if(d===true)div.innerHTML='{CONN_OK}';
else if(d===false)div.innerHTML='{CONN_FAIL}';
else div.innerText='Error';
}).catch(function(){});}
});});
function updateProviderInfo() {
    var p = document.getElementById('api_provider').value;
    var help = document.getElementById('provider_help');

    if (p == "3") {
        help.innerHTML =
            "<small><br><b>DHID</b> - Germany-wide standardized stop identifier</small>";
    }
    else if (p == "1" || p == "2") {
        help.innerHTML =
            "<small><br><b>IBNR</b> - International trainstation-number<br>Get it here -> https://www.michaeldittrich.de/ibnr/online.php</small>";
    }
}

document.getElementById('api_provider')
    .addEventListener('change', updateProviderInfo);

// Initial direkt nach Seitenaufbau
updateProviderInfo();
</script>
</form></div></body></html>"""

# Pre-split template at import time: list of (text_fragment, placeholder_key)
_PARTS = []
_tpl_pos = 0
_tpl_last = 0
while _tpl_pos < len(PAGE_TPL):
    _i = PAGE_TPL.find('{', _tpl_pos)
    if _i < 0:
        break
    _j = PAGE_TPL.find('}', _i + 1)
    if _j < 0:
        break
    _k = PAGE_TPL[_i+1:_j]
    _ok = len(_k) > 0
    if _ok:
        for _c in _k:
            if _c != '_' and not ('A' <= _c <= 'Z'):
                _ok = False
                break
    if _ok:
        _PARTS.append((PAGE_TPL[_tpl_last:_i], _k))
        _tpl_last = _j + 1
        _tpl_pos = _j + 1
    else:
        _tpl_pos = _i + 1
_PARTS.append((PAGE_TPL[_tpl_last:], ""))


def html():
    import varinit, functions

    s = varinit.settings
    connected = functions.wifi.radio.connected
    ip = str(functions.wifi.radio.ipv4_address) if connected else ""

    vmsg = ""

    if connected:
        conn = "<green_box><small>" + T["connected"] + "</small></green_box>"
    else:
        conn = "<red_box><small>" + T["not_connected"] + "</small></red_box>"
    conn_ok = ("<green_box><small>" + T["connected"] + "</small></green_box>").replace("'", "\\'")
    conn_fail = ("<red_box><small>" + T["not_connected"] + "</small></red_box>").replace("'", "\\'")

    _p = ["<option value='", str(s["ssid"]), "' selected>", str(s["ssid"]), "</option>"]
    if hasattr(varinit, 'netlist'):
        for n in varinit.netlist:
            _ns = str(n)
            _p.append("<option value='")
            _p.append(_ns)
            _p.append("'>")
            _p.append(_ns)
            _p.append("</option>")
    ssid_opt = "".join(_p)

    if connected and not (hasattr(varinit, 'checknet') and varinit.checknet):
        net_dis = "disabled"
    else:
        net_dis = ""

    instr = T["_instructions"] if connected else T["instructions"]

    _v = {
        "CSS": css,
        "TITLE": T["title"],
        "CONN_STATUS": conn,
        "VERSION_TEXT": vmsg,
        "T_INFO": T["info"],
        "IP_DISPLAY": ip,
        "INSTR_TEXT": instr,
        "T_NETWORK": T["network"],
        "SSID_OPTIONS": ssid_opt,
        "NET_DIS": net_dis,
        "T_PASSWORD": T["password"],
        "T_CONNECT": T["connect"],
        "T_SAVE": T["save"],
        "CONN_OK": conn_ok,
        "CONN_FAIL": conn_fail,
        "T_STATION": T["station"],
        "STATION_VALUE": str(s["stations"]["1"].get("siteid", "")),
        "T_API_PROVIDER": T["api_provider"],
        "API_DB_SELECTED": "selected" if int(s.get("api_provider", 1)) == 1 else "",
        "API_DB_ALL_SELECTED": "selected" if int(s.get("api_provider", 1)) == 2 else "",
        "API_VVO_SELECTED": "selected" if int(s.get("api_provider", 1)) == 3 else "",
        "LAYOUT_A_SELECTED": "selected" if int(s.get("layout", 1)) == 1 else "",
        "LAYOUT_B_SELECTED": "selected" if int(s.get("layout", 1)) == 2 else "",
        "UTC_OFFSET_VALUE": str(s.get("utc_offset", 1)),
        "SUMMER_TIME_CHECKED": "checked" if int(s.get("summer_time", 0)) else "",
    }
    _out = []
    for _frag, _key in _PARTS:
        _out.append(_frag)
        if _key:
            _out.append(_v.get(_key, ""))
    return "".join(_out)
