"""Bangun HTML ClipACanvas mandiri (minified ringan) dan direct render link.

Format link (sesuai spesifikasi ZY Skill Library):
  https://clipacanvas.vercel.app/render?code=[URL_ENCODED_HTML]&width=W&height=H&fps=60&duration=D&auto=true

Orientasi:
  horizontal -> 1920 x 1080 (default, sesuai spesifikasi)
  vertical   -> 1080 x 1920

Minifier di sini SENGAJA konservatif:
  - Blok <script>, <style>, <pre>, <textarea> dibiarkan utuh (tidak merusak JS/CSS).
  - Hanya menghapus komentar HTML di luar blok tersebut, baris kosong, dan indentasi.
  - Tidak melakukan minifikasi JS. Untuk JS yang panjang, pakai minifier khusus (mis. terser, MIT).

Peringatan: URL memiliki batas panjang (praktisnya ~2000-8000 karakter tergantung
browser/server). Script memberi peringatan bila hasil terlalu panjang.
"""

from __future__ import annotations

import argparse
import re
import sys
from urllib.parse import quote

BASE_URL = "https://clipacanvas.vercel.app/render"
ORIENTATIONS = {"horizontal": (1920, 1080), "vertical": (1080, 1920)}
URL_WARN_LENGTH = 8000

_PRESERVE_RE = re.compile(r"(<(script|style|pre|textarea)\b[^>]*>.*?</\2\s*>)", re.IGNORECASE | re.DOTALL)
_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def minify_html(html: str) -> str:
    """Minifikasi konservatif. Blok sensitif whitespace dipertahankan apa adanya."""
    out: list[str] = []
    cursor = 0
    for m in _PRESERVE_RE.finditer(html):
        out.append(_squash(html[cursor:m.start()]))
        out.append(m.group(0))  # blok <script>/<style>/<pre>/<textarea> utuh
        cursor = m.end()
    out.append(_squash(html[cursor:]))
    return "".join(out).strip()


def _squash(text: str) -> str:
    text = _COMMENT_RE.sub("", text)
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]
    # Newline dipertahankan agar kata di dua baris tidak tergabung ("foo"+"bar" -> "foobar").
    return "\n".join(lines)


def build_link(
    html: str,
    orientation: str = "horizontal",
    fps: int = 60,
    duration: float = 4,
    auto: bool = True,
) -> dict:
    if orientation not in ORIENTATIONS:
        raise ValueError(f"orientation harus salah satu dari {sorted(ORIENTATIONS)}")
    if fps <= 0 or duration <= 0:
        raise ValueError("fps dan duration harus > 0")
    if not html.strip():
        raise ValueError("HTML kosong")
    minified = minify_html(html)
    width, height = ORIENTATIONS[orientation]
    encoded = quote(minified, safe="")
    url = (
        f"{BASE_URL}?code={encoded}&width={width}&height={height}"
        f"&fps={fps}&duration={_fmt_num(duration)}&auto={'true' if auto else 'false'}"
    )
    return {
        "html_minified": minified,
        "html_chars": len(minified),
        "url": url,
        "url_chars": len(url),
        "width": width,
        "height": height,
        "warning": (f"URL {len(url)} karakter, melebihi {URL_WARN_LENGTH}; "
                    "pertimbangkan memperpendek HTML atau memakai penyimpanan berbeda")
        if len(url) > URL_WARN_LENGTH else None,
    }


def _fmt_num(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else str(value)


def _main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("html_file")
    p.add_argument("--orientation", choices=sorted(ORIENTATIONS), default="horizontal")
    p.add_argument("--fps", type=int, default=60)
    p.add_argument("--duration", type=float, default=4)
    p.add_argument("--no-auto", action="store_true")
    p.add_argument("--out-html", help="Simpan HTML minified ke file ini")
    args = p.parse_args(argv)
    try:
        with open(args.html_file, encoding="utf-8") as fh:
            html = fh.read()
        result = build_link(html, args.orientation, args.fps, args.duration, not args.no_auto)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.out_html:
        with open(args.out_html, "w", encoding="utf-8") as fh:
            fh.write(result["html_minified"])
    print(result["url"])
    if result["warning"]:
        print(f"WARNING: {result['warning']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(_main())
