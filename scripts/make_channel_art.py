"""Build Small Change Lab channel art (DP + banner) from the Inch SVG and the style-bible palette.

Usage: python scripts/make_channel_art.py
Writes SVGs to creative/brand/, then renders PNGs with headless Edge/Chrome.
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCH = ROOT / "projects/focus-block/assets/characters/inch/inch_cheer.svg"
OUT = ROOT / "creative/brand"
OUT.mkdir(parents=True, exist_ok=True)

PAPER, INK, KRAFT, SUN, MINT, SKY, MONEY = (
    "#F5EEDD", "#26303F", "#C9A77C", "#F2B632", "#3FA37A", "#7FB3D5", "#E3F1E7")

# Inch art bbox inside its 1024 canvas (feet baseline y~1007, stalk tops y~472, x 78..969)
BX0, BX1, BY0, BY1 = 78, 969, 472, 1008
inner = re.search(r"<svg[^>]*>(.*)</svg>", INCH.read_text(), re.S).group(1)


def inch(cx_left, base_y, scale):
    """Place Inch with bbox-left at cx_left and feet at base_y."""
    tx = cx_left - BX0 * scale
    ty = base_y - BY1 * scale
    return f'<g transform="translate({tx:.1f} {ty:.1f}) scale({scale})">{inner}</g>'


def coin(x, y, r=34):
    return (f'<g transform="translate({x} {y})"><ellipse cx="6" cy="8" rx="{r}" ry="{r}" fill="{INK}" opacity=".2"/>'
            f'<circle r="{r}" fill="{SUN}" stroke="{INK}" stroke-width="5"/>'
            f'<circle r="{r*0.6:.0f}" fill="none" stroke="{INK}" stroke-width="4" opacity=".55"/></g>')


# ---------- DP: 1024x1024, YouTube crops to a circle ----------
dp_scale = 0.84
dp_w = (BX1 - BX0) * dp_scale
dp_left = (1024 - dp_w) / 2
dp_base = 745
dp = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
<rect width="1024" height="1024" fill="{MONEY}"/>
<rect y="{dp_base-6}" width="1024" height="{1024-dp_base+6}" fill="{PAPER}"/>
<rect y="{dp_base-6}" width="1024" height="10" fill="{KRAFT}"/>
{inch(dp_left, dp_base, dp_scale)}
</svg>'''
(OUT / "dp.svg").write_text(dp)

# ---------- Banner: 2560x1440; safe area x 507..2053, y 508..931 ----------
W, H = 2560, 1440
floor_y = 931
b_scale = 0.60
text_x = 1130
banner = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" fill="{MONEY}"/>
<rect y="{floor_y}" width="{W}" height="{H-floor_y}" fill="{PAPER}"/>
<rect y="{floor_y}" width="{W}" height="12" fill="{KRAFT}"/>
<!-- outer decor (only visible on desktop/TV, outside the mobile safe area) -->
{coin(190, floor_y-34)}{coin(262, floor_y-34)}{coin(226, floor_y-96)}
{coin(2330, floor_y-34)}{coin(2402, floor_y-34)}{coin(2366, floor_y-96)}
<circle cx="2440" cy="330" r="14" fill="{SKY}"/><circle cx="130" cy="420" r="10" fill="{SKY}"/>
<!-- safe area content -->
{inch(540, floor_y, b_scale)}
<g font-family="Arial Black, Impact, sans-serif" font-weight="900">
<text x="{text_x}" y="650" font-size="98" fill="{INK}">SMALL CHANGE</text>
<text x="{text_x}" y="760" font-size="98" fill="{SUN}" stroke="{INK}" stroke-width="7" paint-order="stroke" stroke-linejoin="round">LAB</text>
</g>
<g font-family="Arial, Helvetica, sans-serif" font-weight="700" fill="{INK}" font-size="40">
<text x="{text_x}" y="830">One small habit. One cited fact.</text>
<text x="{text_x}" y="884">One thing to try today.</text>
</g>
</svg>'''
(OUT / "banner.svg").write_text(banner)


def find_browser():
    for p in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"):
        if Path(p).exists():
            return p
    raise SystemExit("No Edge/Chrome found")


def render(name, w, h):
    svg = (OUT / f"{name}.svg").resolve()
    png = (OUT / f"{name}.png").resolve()
    html = OUT / f"_{name}.html"
    html.write_text(f'<html><body style="margin:0;background:#fff"><img src="{svg.name}" width="{w}" height="{h}" style="display:block"></body></html>')
    import tempfile
    prof = tempfile.mkdtemp(prefix="edgeprof_")
    r = subprocess.run([find_browser(), "--headless", "--disable-gpu", "--hide-scrollbars",
                        f"--user-data-dir={prof}", f"--window-size={w},{h}",
                        f"--screenshot={png}", html.resolve().as_uri()],
                       capture_output=True, text=True, timeout=90)
    html.unlink()
    if not png.exists():
        raise SystemExit(f"render failed for {name}: {r.returncode} {r.stderr[-400:]}")
    print("wrote", png)


render("dp", 1024, 1024)
render("banner", W, H)
