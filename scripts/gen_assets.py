#!/usr/bin/env python3
"""Shared channel asset library: deterministic hand-authored SVG drawers + cross-project reuse.

  python scripts/gen_assets.py projects/<id>            # fill missing visual assets for a project
  python scripts/gen_assets.py projects/<id> --force    # regenerate library assets (never overwrites copies' sources)
  python scripts/gen_assets.py projects/<id> --dry-run  # show what would happen
  python scripts/gen_assets.py --list                   # library ids + drawn assets available in other projects

For each visual entry in projects/<id>/asset-requirements.json (type != sfx), per file:
  1. already exists in the project (as .svg)  -> keep (unless --force and a drawer exists)
  2. a drawer for its id exists in DRAWERS    -> generate             (status "drawn", source "library")
  3. the same id is drawn in another project  -> copy that SVG        (status "drawn", source "projects/<other>")
  4. otherwise                                -> reported as NEEDS DRAWING (asset-artist's job)
Paths are normalised to .svg in asset-requirements.json and animation.json.

Adding a new asset: write a drawer function below, register it in DRAWERS under its
creative/asset-registry.json id, and keep the shared palette / filters / shadow tiers.
Style rules: creative/style-bible.md. Everything is deterministic (fixed seeds).
"""
from pathlib import Path
import argparse, json, math, random, re, shutil, sys

ROOT = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------ palette + shared filters
C, I, U, K, M, T, R = "#F4E6C8", "#3A2419", "#7A4B2F", "#B86B43", "#E9A93B", "#5E8F86", "#D2452B"
PALETTE = {"cream": C, "ink": I, "umber": U, "clay": K, "mustard": M, "teal": T, "red": R}

# Identical in every file (wobble seed 11, paper seed 29).
COMMON = f"""<filter id="wobble" x="-20%" y="-20%" width="140%" height="140%" color-interpolation-filters="sRGB">
<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="11" result="wn"/>
<feDisplacementMap in="SourceGraphic" in2="wn" scale="8" xChannelSelector="R" yChannelSelector="G"/>
</filter>
<filter id="paper" x="-20%" y="-20%" width="140%" height="140%" color-interpolation-filters="sRGB">
<feTurbulence type="fractalNoise" baseFrequency="0.12 0.5" numOctaves="3" seed="29" result="pn"/>
<feColorMatrix in="pn" type="matrix" values="0 0 0 0 0.2275 0 0 0 0 0.1412 0 0 0 0 0.098 0.16 0 0 0 0" result="pf"/>
<feComposite in="pf" in2="SourceAlpha" operator="in" result="pc"/>
<feBlend in="pc" in2="SourceGraphic" mode="multiply"/>
</filter>"""


def shadow_filter(fid, w, h, d, blur):
    return (f'<filter id="{fid}" filterUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}" '
            f'color-interpolation-filters="sRGB">'
            f'<feGaussianBlur in="SourceAlpha" stdDeviation="{blur}" result="b"/>'
            f'<feOffset in="b" dx="{d}" dy="{d}" result="o"/>'
            f'<feFlood flood-color="{I}" flood-opacity="0.28"/>'
            f'<feComposite in2="o" operator="in" result="s"/>'
            f'<feMerge><feMergeNode in="s"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')


def doc(w, h, body, extra_defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
            f'<defs>\n{COMMON}\n{extra_defs}\n</defs>\n{body}\n</svg>\n')


# Props: 4 canvas units per output px. Shadow tier diagonal offset (px at 1080 wide):
# back 4, mid 8, front 12 -> dx = dy = tier/sqrt2 px -> canvas units.
TIER = {"back": 11, "mid": 23, "front": 34}
BLUR = 6  # 1.5 px


def prop(w, h, tier, art, lt=10, top=None, extra=""):
    top = lt if top is None else top
    d = TIER[tier]
    defs = shadow_filter("shadow", w, h, d, BLUR) + "\n" + shadow_filter("piece", w, h, round(d / 3), 3) + extra
    body = (f'<g filter="url(#shadow)"><g filter="url(#paper)"><g filter="url(#wobble)">'
            f'<g transform="translate({lt},{top})">\n{art}\n</g></g></g></g>')
    return doc(w, h, body, defs)


# ------------------------------------------------------------------ Tuck (host)
TW = 1024
TK = TW / 162.0  # canvas units per px at width 0.15
TD = round(8.49 * TK)  # front tier
TB = round(1.5 * TK)
BODY_PATH = ("M 300 990 C 236 990 220 900 236 820 C 252 720 300 660 318 600 C 300 520 296 420 340 340 "
             "C 384 262 450 236 512 236 C 574 236 640 262 684 340 C 728 420 724 520 706 600 "
             "C 724 660 772 720 788 820 C 804 900 788 990 724 990 Z")
TUCK_BODY = f"""<g id="tuck-body">
<ellipse cx="430" cy="978" rx="66" ry="22" fill="{C}"/>
<ellipse cx="624" cy="978" rx="66" ry="22" fill="{C}"/>
<path d="{BODY_PATH}" fill="{K}"/>
<g clip-path="url(#bodyclip)">
<ellipse cx="540" cy="842" rx="150" ry="124" fill="{C}"/>
<path d="M 330 318 Q 512 248 694 318 L 694 352 Q 512 284 330 352 Z" fill="{C}"/>
</g>
<g transform="translate(590,282) rotate(9)"><rect x="-48" y="-36" width="96" height="72" rx="22" fill="{M}"/>
<circle cx="4" cy="0" r="17" fill="{C}"/></g>
<path d="M 536 470 Q 548 424 640 430 Q 742 438 774 470 Q 786 490 764 504 Q 700 534 602 528 Q 532 520 536 470 Z" fill="{C}"/>
<ellipse cx="770" cy="476" rx="24" ry="21" fill="{I}"/>
<circle cx="494" cy="398" r="21" fill="{I}"/>
<circle cx="602" cy="392" r="21" fill="{I}"/>
<path d="M 298 588 Q 512 628 726 588 L 732 652 Q 512 698 292 652 Z" fill="{M}"/>
<g filter="url(#piece)">
<rect x="-31" y="0" width="62" height="172" rx="24" fill="{M}" transform="translate(392,636) rotate(12)"/>
<rect x="-28" y="0" width="56" height="138" rx="22" fill="{M}" transform="translate(448,644) rotate(-7)"/>
</g>
</g>"""


def _arm(sx, sy, ang, L, digit=False):
    dg = f'<rect x="-15" y="{L + 10}" width="30" height="58" rx="15" fill="{K}"/>' if digit else ""
    return (f'<g transform="translate({sx},{sy}) rotate({ang})">'
            f'<rect x="-34" y="0" width="68" height="{L}" rx="34" fill="{K}"/>'
            f'<ellipse cx="0" cy="{L - 18}" rx="46" ry="54" fill="{K}"/>{dg}</g>')


def _brow(x, y, ang):
    return f'<rect x="-36" y="-10" width="72" height="20" rx="10" fill="{I}" transform="translate({x},{y}) rotate({ang})"/>'


def _sparkle(x, y, s):
    return (f'<path transform="translate({x},{y}) scale({s})" fill="{M}" '
            f'd="M 0 -50 Q 8 -8 50 0 Q 8 8 0 50 Q -8 8 -50 0 Q -8 -8 0 -50 Z"/>')


# pose -> (arms, other parts). Add poses here (e.g. carry, dig) on the same canvas/baseline.
TUCK_POSES = {
    "stand": ([_arm(316, 650, 22, 168), _arm(708, 650, -22, 168)], []),
    "point": ([_arm(316, 650, 22, 168), _arm(704, 648, -100, 168, digit=True)], []),
    "worry": ([_arm(316, 650, 22, 168), _arm(704, 652, 147, 128)], [_brow(486, 348, -16), _brow(600, 340, 16)]),
    "idea": ([_arm(316, 650, 22, 168), _arm(704, 640, -160, 200)],
             [_brow(486, 336, -6), _brow(600, 328, 6), _sparkle(856, 300, 1.0), _sparkle(908, 392, 0.5)]),
    "cheer": ([_arm(330, 640, 155, 220), _arm(694, 640, -155, 220)], []),
}


def tuck(pose):
    arms, other = TUCK_POSES[pose]
    defs = (shadow_filter("shadow", TW, TW, TD, TB) + "\n" + shadow_filter("piece", TW, TW, 14, 5) +
            f'\n<clipPath id="bodyclip"><path d="{BODY_PATH}"/></clipPath>')
    body = (f'<g filter="url(#shadow)"><g filter="url(#paper)"><g filter="url(#wobble)">\n{TUCK_BODY}\n'
            + "\n".join(other) + '\n<g filter="url(#piece)">' + "".join(arms) + '</g>\n</g></g></g>')
    return doc(TW, TW, body, defs)


# ------------------------------------------------------------------ backgrounds (1080x1920)
BW, BH = 1080, 1920
GROUND, S1, S2 = 845, 1190, 1421  # y 0.44 / 0.62 / 0.74


def _torn(y0, amp, step, seed, bottom):
    rnd = random.Random(seed)
    pts, x = [], -10
    while x <= BW + 10:
        pts.append((x, y0 + rnd.uniform(-amp, amp)))
        x += step * rnd.uniform(0.7, 1.3)
    pts.append((BW + 10, y0))
    d = "M " + " L ".join(f"{px:.1f} {py:.1f}" for px, py in pts)
    return d + f" L {BW + 10} {bottom} L -10 {bottom} Z"


def _strata(seed0):
    out = []
    for i, (y0, fill) in enumerate([(GROUND, U), (S1, K), (S2, U)]):
        out.append(f'<path d="{_torn(y0 - 4, 1.3, 5, seed0 + i * 2, BH + 10)}" fill="{C}"/>')
        out.append(f'<path d="{_torn(y0, 1.6, 9, seed0 + i * 2 + 1, BH + 10)}" fill="{fill}"/>')
    peb = [(150, 1530, 46, 30, -10), (420, 1640, 34, 22, 15), (700, 1560, 52, 32, 5), (930, 1700, 40, 26, -20),
           (260, 1800, 38, 24, 8), (600, 1830, 48, 28, -6), (860, 1500, 30, 20, 12)]
    out.append('<g filter="url(#shadow)">' + "".join(
        f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" transform="rotate({a} {x} {y})" fill="{K}"/>'
        for x, y, rx, ry, a in peb) + "</g>")
    return "\n".join(out)


def _cloud(x, y, s):
    return (f'<g transform="translate({x},{y}) scale({s})" fill="{C}">'
            f'<rect x="-120" y="-10" width="240" height="60" rx="30"/>'
            f'<circle cx="-50" cy="-8" r="52"/><circle cx="30" cy="-30" r="66"/><circle cx="92" cy="6" r="40"/></g>')


def bg_cutaway_day():
    body = (f'<g filter="url(#paper)">\n<rect width="{BW}" height="{BH}" fill="{C}"/>\n'
            f'<g filter="url(#shadow)">{_cloud(240, 520, 1.0)}{_cloud(830, 250, 0.85)}</g>\n'
            f'<g filter="url(#shadow)" fill="{T}">'
            f'<path d="M 884 850 Q 862 800 872 762 Q 900 800 902 850 Z"/>'
            f'<path d="M 896 850 Q 900 784 922 748 Q 934 800 916 850 Z"/>'
            f'<path d="M 910 850 Q 934 806 960 790 Q 952 826 930 850 Z"/></g>\n'
            f'{_strata(100)}\n</g>')
    return doc(BW, BH, body, shadow_filter("shadow", BW, BH, 3, 1.5))


def bg_cutaway_night():
    defs = shadow_filter("shadow", BW, BH, 3, 1.5) + (
        f'\n<linearGradient id="nightsky" x1="0" y1="0" x2="0" y2="{GROUND}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{I}"/><stop offset="1" stop-color="{U}"/></linearGradient>')
    stars = [(140, 170, 6), (380, 96, 5), (610, 250, 7), (250, 600, 5), (720, 640, 6)]
    body = (f'<g filter="url(#paper)">\n<rect width="{BW}" height="{BH}" fill="url(#nightsky)"/>\n'
            + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{M}"/>' for x, y, r in stars) +
            f'\n<g filter="url(#shadow)"><circle cx="860" cy="250" r="74" fill="{C}"/></g>\n{_strata(100)}\n</g>')
    return doc(BW, BH, body, defs)


# ------------------------------------------------------------------ props
def air_arrow():
    return prop(260, 260, "front",
                f'<path d="M 26 176 Q 52 64 148 62" fill="none" stroke="{T}" stroke-width="36" stroke-linecap="round"/>'
                f'<path d="M 140 22 L 190 62 L 140 102 Z" fill="{T}" stroke="{T}" stroke-width="16" stroke-linejoin="round"/>')


def bucket_toilet():
    return prop(304, 316, "front",
                f'<path d="M 18 120 L 230 120 L 210 250 Q 208 260 198 260 L 50 260 Q 40 260 38 250 Z" fill="{C}"/>'
                f'<rect x="32" y="180" width="184" height="18" rx="9" fill="{K}"/>'
                f'<rect x="0" y="88" width="248" height="40" rx="20" fill="{K}"/>'
                f'<path d="M 30 92 Q 124 34 218 92 Z" fill="{C}"/>'
                f'<rect x="106" y="46" width="36" height="26" rx="12" fill="{K}"/>')


def crank_radio():
    return prop(260, 206, "front",
                f'<path d="M 148 34 L 174 4" stroke="{I}" stroke-width="9" stroke-linecap="round"/>'
                f'<path d="M 176 92 L 196 92 L 196 128" fill="none" stroke="{C}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<rect x="0" y="30" width="182" height="120" rx="24" fill="{K}"/>'
                f'<circle cx="52" cy="90" r="34" fill="{C}"/>'
                f'<path d="M 52 90 L 64 68" stroke="{I}" stroke-width="7" stroke-linecap="round"/>'
                f'<path d="M 106 70 L 158 70 M 106 90 L 158 90 M 106 110 L 158 110" stroke="{I}" stroke-width="9" stroke-linecap="round"/>')


def earth_cover():
    flecks = [(220, 470, 18, 12), (520, 300, 14, 10), (880, 420, 20, 13), (1180, 260, 15, 10),
              (1460, 440, 19, 12), (1720, 480, 14, 9)]
    return prop(1988, 600, "mid",
                f'<rect x="0" y="380" width="1943" height="175" rx="40" fill="{U}"/>'
                f'<g filter="url(#piece)"><path d="M 30 440 C 90 300 330 190 620 160 C 840 136 1110 136 1330 160 '
                f'C 1620 192 1860 300 1915 440 Q 1920 470 1880 470 L 70 470 Q 24 470 30 440 Z" fill="{U}"/></g>'
                + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{a}" ry="{b}" fill="{C}"/>' for x, y, a, b in flecks))


def glow_disc():
    gw = 648  # no drop shadow; soft edge via blur + opacity
    defs = (f'<filter id="soft" filterUnits="userSpaceOnUse" x="0" y="0" width="{gw}" height="{gw}">'
            f'<feGaussianBlur stdDeviation="26"/></filter>')
    return doc(gw, gw,
               f'<g filter="url(#soft)" opacity="0.6"><g filter="url(#paper)"><circle cx="324" cy="324" r="248" fill="{M}"/></g></g>'
               f'<g filter="url(#soft)" opacity="0.35"><circle cx="324" cy="324" r="170" fill="{M}"/></g>', defs)


def hand_fan():
    return prop(520, 496, "front",
                f'<path d="M 396 200 L 446 200 L 446 290" fill="none" stroke="{K}" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<circle cx="446" cy="304" r="18" fill="{C}"/>'
                f'<rect x="0" y="0" width="400" height="430" rx="52" fill="{K}"/>'
                f'<circle cx="200" cy="205" r="162" fill="{C}"/>'
                f'<g fill="{K}">' + "".join(
                    f'<ellipse cx="200" cy="140" rx="44" ry="76" transform="rotate({a} 200 205)"/>' for a in (0, 120, 240)) +
                f'</g><circle cx="200" cy="205" r="30" fill="{C}"/>')


def hole_cutout():
    return prop(2160, 2224, "back",
                f'<path d="M 0 0 L 2127 0 L 2127 1991 Q 2127 2201 1917 2201 L 210 2201 Q 0 2201 0 1991 Z" fill="{I}"/>'
                f'<path d="M 70 60 L 2097 60 L 2097 1971 Q 2097 2171 1897 2171 L 250 2171 Q 70 2171 70 1991 Z" fill="{U}"/>'
                f'<g fill="{I}"><ellipse cx="1620" cy="2090" rx="60" ry="34"/><ellipse cx="1780" cy="2110" rx="40" ry="24"/>'
                f'<ellipse cx="420" cy="2100" rx="48" ry="28"/></g>', top=0)


def ladder():
    rungs = "".join(f'<rect x="18" y="{int(110 + i * 228)}" width="115" height="30" rx="15" fill="{K}"/>' for i in range(5))
    return prop(196, 1176, "mid",
                rungs + f'<g filter="url(#piece)"><rect x="0" y="0" width="32" height="1131" rx="16" fill="{K}"/>'
                f'<rect x="119" y="0" width="32" height="1131" rx="16" fill="{K}"/></g>')


def lantern():
    return prop(196, 296, "front",
                f'<path d="M 38 44 Q 70 -10 102 44" fill="none" stroke="{K}" stroke-width="12" stroke-linecap="round"/>'
                f'<rect x="30" y="60" width="80" height="130" rx="28" fill="{M}"/>'
                f'<g fill="{K}"><rect x="22" y="58" width="14" height="134" rx="7"/><rect x="63" y="58" width="14" height="134" rx="7"/>'
                f'<rect x="104" y="58" width="14" height="134" rx="7"/></g>'
                f'<path d="M 18 64 L 34 32 L 106 32 L 122 64 Z" fill="{K}" stroke="{K}" stroke-width="10" stroke-linejoin="round"/>'
                f'<rect x="8" y="186" width="124" height="44" rx="16" fill="{K}"/>')


def shelf_unit():
    boards = "".join(f'<rect x="0" y="{y}" width="615" height="46" rx="14" fill="{U}"/>' for y in (40, 380, 700))
    hl = "".join(f'<rect x="14" y="{y}" width="587" height="10" rx="5" fill="{C}"/>' for y in (40, 380, 700))
    return prop(648, 830, "back",
                f'<g fill="{U}"><rect x="0" y="0" width="50" height="797" rx="16"/><rect x="565" y="0" width="50" height="797" rx="16"/></g>'
                f'<g filter="url(#piece)">{boards}{hl}</g>')


def shovel():
    return prop(216, 700, "front",
                f'<rect x="46" y="12" width="68" height="56" rx="24" fill="none" stroke="{K}" stroke-width="22"/>'
                f'<rect x="66" y="60" width="28" height="420" rx="14" fill="{K}"/>'
                f'<path d="M 18 480 Q 80 466 142 480 L 142 600 Q 142 650 80 690 Q 18 650 18 600 Z" fill="{C}"/>'
                f'<rect x="54" y="440" width="52" height="62" rx="16" fill="{K}"/>')


def timber_beam():
    return prop(2248, 224, "mid",
                f'<rect x="0" y="0" width="2203" height="179" rx="34" fill="{U}"/>'
                f'<path d="M 140 52 C 500 40 800 64 1240 50 M 1560 56 C 1800 48 1960 58 2080 52 '
                f'M 240 96 C 600 104 900 86 1300 100 M 1500 92 C 1720 100 1900 88 2000 96 M 120 134 C 560 126 1100 142 1900 130" '
                f'fill="none" stroke="{C}" stroke-width="10" stroke-linecap="round"/>'
                f'<ellipse cx="1400" cy="80" rx="62" ry="26" fill="none" stroke="{C}" stroke-width="10"/>'
                f'<g fill="{I}"><circle cx="62" cy="90" r="13"/><circle cx="2141" cy="90" r="13"/></g>')


def vent_pipe():
    return prop(196, 924, "mid",
                f'<rect x="10" y="0" width="131" height="924" rx="6" fill="{C}"/>'
                f'<rect x="96" y="56" width="10" height="868" rx="5" fill="{I}"/>'
                f'<rect x="0" y="0" width="151" height="52" rx="14" fill="{I}"/>', top=0)


def water_jug():
    return prop(138, 164, "front",
                f'<rect x="52" y="12" width="28" height="30" rx="11" fill="none" stroke="{T}" stroke-width="10"/>'
                f'<rect x="20" y="4" width="26" height="24" rx="7" fill="{T}"/>'
                f'<rect x="0" y="22" width="84" height="88" rx="18" fill="{T}"/>'
                f'<rect x="12" y="52" width="60" height="32" rx="9" fill="{C}"/>'
                f'<path d="M 42 56 Q 52 70 52 74 A 10 10 0 0 1 32 74 Q 32 70 42 56 Z" fill="{T}"/>', lt=8)


# ------------------------------------------------------------------ UI
def fix_check():
    return prop(388, 388, "front",
                f'<circle cx="166" cy="166" r="166" fill="{M}"/>'
                f'<circle cx="166" cy="166" r="138" fill="none" stroke="{I}" stroke-width="8"/>'
                f'<path d="M 94 172 L 146 222 L 242 114" fill="none" stroke="{I}" stroke-width="42" stroke-linecap="round" stroke-linejoin="round"/>')


def problem_badge():
    rnd = random.Random(7)
    pts = []
    for i in range(24):
        a = math.pi * 2 * i / 24 - math.pi / 2
        r = (188 if i % 2 == 0 else 136) + rnd.uniform(-6, 6)
        pts.append(f"{188 + r * math.cos(a):.1f} {188 + r * math.sin(a):.1f}")
    return prop(432, 432, "front",
                f'<path d="M {" L ".join(pts)} Z" fill="{R}"/>'
                f'<path d="M 160 92 Q 188 80 216 92 L 204 236 Q 188 246 172 236 Z" fill="{C}" stroke="{C}" stroke-width="8" stroke-linejoin="round"/>'
                f'<circle cx="188" cy="284" r="27" fill="{C}"/>')


def ready_stamp():
    distress = ('<filter id="distress" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
                '<feTurbulence type="fractalNoise" baseFrequency="0.06" numOctaves="3" seed="5" result="dn"/>'
                '<feColorMatrix in="dn" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 14 0 0 0 -8.9" result="dm"/>'
                '<feComposite in="SourceGraphic" in2="dm" operator="out"/></filter>')
    return prop(1124, 1124, "front",
                f'<circle cx="534" cy="534" r="534" fill="{M}"/>'
                f'<g filter="url(#distress)" fill="{I}">'
                f'<circle cx="534" cy="534" r="478" fill="none" stroke="{I}" stroke-width="24"/>'
                f'<circle cx="534" cy="534" r="432" fill="none" stroke="{I}" stroke-width="10"/>'
                f'<rect x="284" y="348" width="500" height="28" rx="14"/>'
                f'<rect x="284" y="694" width="500" height="28" rx="14"/>'
                f'<text x="534" y="622" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" '
                f'font-size="236" textLength="770" lengthAdjust="spacingAndGlyphs">READY</text></g>', extra=distress)


# ------------------------------------------------------------------ registry: asset id -> drawer
# Characters take a pose argument; everything else takes none.
DRAWERS = {
    "tuck": tuck,
    "bg_cutaway_day": bg_cutaway_day, "bg_cutaway_night": bg_cutaway_night,
    "air_arrow": air_arrow, "bucket_toilet": bucket_toilet, "crank_radio": crank_radio,
    "earth_cover": earth_cover, "glow_disc": glow_disc, "hand_fan": hand_fan, "hole_cutout": hole_cutout,
    "ladder": ladder, "lantern": lantern, "shelf_unit": shelf_unit, "shovel": shovel,
    "timber_beam": timber_beam, "vent_pipe": vent_pipe, "water_jug": water_jug,
    "fix_check": fix_check, "problem_badge": problem_badge, "ready_stamp": ready_stamp,
}
POSES = {"tuck": TUCK_POSES}


# ------------------------------------------------------------------ project filling + cross-project reuse
def to_svg(rel: str) -> str:
    return re.sub(r"\.(png|jpe?g|webp)$", ".svg", rel, flags=re.I)


def files_for(item) -> list[tuple[str, str | None]]:
    """(relative .svg path, pose) for each file of a requirement entry."""
    path = to_svg(item["path"])
    if "<pose>" in path:
        return [(path.replace("<pose>", p), p) for p in item.get("poses", [])]
    if item.get("files"):
        return [(to_svg(f), None) for f in item["files"]]
    return [(path, None)]


def other_projects_index(this_proj: Path) -> dict[tuple[str, str], Path]:
    """(asset id, file name) -> existing drawn SVG in another project."""
    idx = {}
    for req_path in sorted((ROOT / "projects").glob("*/asset-requirements.json")):
        proj = req_path.parent
        if proj.resolve() == this_proj.resolve():
            continue
        try:
            items = json.loads(req_path.read_text(encoding="utf-8")).get("assets", [])
        except (OSError, json.JSONDecodeError):
            continue
        for item in items:
            if item.get("type") == "sfx":
                continue
            for rel, _ in files_for(item):
                f = proj / rel
                if f.is_file() and f.suffix == ".svg":
                    idx.setdefault((item["id"], Path(rel).name), f)
    return idx


def fill_project(proj: Path, force: bool, dry: bool) -> int:
    req_path = proj / "asset-requirements.json"
    req = json.loads(req_path.read_text(encoding="utf-8"))
    others = other_projects_index(proj)
    path_swaps, needs, counts = {}, [], {"kept": 0, "drawn": 0, "copied": 0}

    for item in req.get("assets", []):
        if item.get("type") == "sfx":
            continue
        drawer = DRAWERS.get(item["id"])
        sources = set()
        ok = True
        for rel, pose in files_for(item):
            out = proj / rel
            if out.is_file() and not (force and drawer):
                counts["kept"] += 1
                sources.add(item.get("source", "existing"))
                continue
            if drawer and (pose is None or pose in POSES.get(item["id"], {})):
                svg = drawer(pose) if pose else drawer()
                action, src = "drawn", "library"
            elif (item["id"], Path(rel).name) in others:
                srcf = others[(item["id"], Path(rel).name)]
                svg, action = None, "copied"
                src = next(p for p in srcf.parents if (p / "asset-requirements.json").exists()).relative_to(ROOT).as_posix()
            else:
                needs.append(f"{item['id']}{':' + pose if pose else ''} -> {rel}")
                ok = False
                continue
            print(f"{action:6} {rel}" + (f"  (from {src})" if action == "copied" else ""))
            counts[action] += 1
            sources.add(src)
            if not dry:
                out.parent.mkdir(parents=True, exist_ok=True)
                if svg is not None:
                    out.write_text(svg, encoding="utf-8")
                else:
                    shutil.copyfile(others[(item["id"], Path(rel).name)], out)
        old = item["path"]
        new = to_svg(old)
        for o in [old] + item.get("files", []):
            if to_svg(o) != o:
                path_swaps[o] = to_svg(o)
        item["path"] = new
        if item.get("files"):
            item["files"] = [to_svg(f) for f in item["files"]]
        if ok:
            item["status"] = "drawn"
            item["source"] = sorted(sources)[0] if len(sources) == 1 else sorted(sources)
        else:
            item["status"] = "missing"

    if not dry:
        req_path.write_text(json.dumps(req, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        anim = proj / "animation.json"
        if anim.is_file() and path_swaps:
            text = anim.read_text(encoding="utf-8")
            n = 0
            for o, nw in path_swaps.items():
                n += text.count(f'"{o}"')
                text = text.replace(f'"{o}"', f'"{nw}"')
            anim.write_text(text, encoding="utf-8")
            print(f"animation.json: {n} path(s) switched to .svg")
    print(f"kept {counts['kept']}, drawn {counts['drawn']}, copied {counts['copied']}, needs drawing {len(needs)}")
    for n in needs:
        print("NEEDS DRAWING", n)
    return 1 if needs else 0


def list_available() -> None:
    print("Library drawers:", ", ".join(sorted(DRAWERS)))
    for k, poses in POSES.items():
        print(f"  {k} poses: {', '.join(poses)}")
    idx = other_projects_index(ROOT / "__none__")
    extra = sorted({(aid, f.relative_to(ROOT).as_posix()) for (aid, _), f in idx.items() if aid not in DRAWERS})
    print("Drawn in projects (not in library):", "none" if not extra else "")
    for aid, f in extra:
        print(f"  {aid}: {f}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project_dir", type=Path, nargs="?")
    ap.add_argument("--force", action="store_true", help="regenerate files that have a library drawer")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list:
        list_available()
        return 0
    if not a.project_dir:
        ap.error("project_dir is required unless --list")
    return fill_project(a.project_dir.resolve(), a.force, a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
