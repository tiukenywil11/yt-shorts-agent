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


# ================================================================== Small Change Lab (channel 2)
# Separate palette + helpers; the Paper Prepper drawers above are untouched.
# creative/style-bible.md: NO SVG filters. Shadow = flat Ink copy at 20%, offset down-right by tier
# (back 4 / mid 8 / front 12 px at 1080w, diagonal length), no blur. Wobble = hand-jittered points (fixed seeds).
SP, SI, SK, SS, SM, SC, SY = "#F5EEDD", "#26303F", "#C9A77C", "#F2B632", "#3FA37A", "#E2553F", "#7FB3D5"
SCL_PALETTE = {"paper": SP, "ink": SI, "kraft": SK, "sun": SS, "mint": SM, "coral": SC, "sky": SY}
SCL_TIER = {"back": 4, "mid": 8, "front": 12}
SCL_FONT = "Arial Black, Arial, sans-serif"


def _f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def _cr(pts, closed=True):
    """Catmull-Rom spline through points -> cubic bezier path data."""
    n = len(pts)
    P = (lambda i: pts[i % n]) if closed else (lambda i: pts[max(0, min(n - 1, i))])
    d = f"M {_f(pts[0][0])} {_f(pts[0][1])}"
    for i in range(n if closed else n - 1):
        p0, p1, p2, p3 = P(i - 1), P(i), P(i + 1), P(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C {_f(c1[0])} {_f(c1[1])} {_f(c2[0])} {_f(c2[1])} {_f(p2[0])} {_f(p2[1])}"
    return d + (" Z" if closed else "")


def _jit(pts, seed, amp):
    rnd = random.Random(seed)
    return [(x + rnd.uniform(-amp, amp), y + rnd.uniform(-amp, amp)) for x, y in pts]


def _rr_pts(x, y, w, h, r, step):
    """Points around a rounded rect (clockwise from top-left)."""
    pts = []

    def edge(ax, ay, bx, by):
        k = max(1, round(math.hypot(bx - ax, by - ay) / step))
        pts.extend((ax + (bx - ax) * i / k, ay + (by - ay) * i / k) for i in range(k))

    def arc(cx, cy, a0):
        pts.extend((cx + r * math.cos(math.radians(a0 + 30 * i)), cy + r * math.sin(math.radians(a0 + 30 * i)))
                   for i in range(3))
    edge(x + r, y, x + w - r, y); arc(x + w - r, y + r, -90)
    edge(x + w, y + r, x + w, y + h - r); arc(x + w - r, y + h - r, 0)
    edge(x + w - r, y + h, x + r, y + h); arc(x + r, y + h - r, 90)
    edge(x, y + h - r, x, y + r); arc(x + r, y + r, 180)
    return pts


def wrect(x, y, w, h, r, fill, seed, amp, step=60, attrs=""):
    return f'<path d="{_cr(_jit(_rr_pts(x, y, w, h, r, step), seed, amp))}" fill="{fill}"{attrs}/>'


def wcirc(cx, cy, r, fill, seed, amp, n=None, attrs=""):
    n = n or max(12, int(r / 14))
    pts = [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]
    return f'<path d="{_cr(_jit(pts, seed, amp))}" fill="{fill}"{attrs}/>'


def wblob(pts, fill, seed, amp, attrs=""):
    return f'<path d="{_cr(_jit(pts, seed, amp))}" fill="{fill}"{attrs}/>'


def burst(cx, cy, r_out, r_in, n, fill, seed, amp, rot=0.0):
    """Jagged rim (problem items only). Round joins give visible corner radii."""
    rnd = random.Random(seed)
    pts = []
    for i in range(2 * n):
        a = math.pi * i / n - math.pi / 2 + rot
        r = (r_out if i % 2 == 0 else r_in) + rnd.uniform(-amp, amp)
        pts.append(f"{_f(cx + r * math.cos(a))} {_f(cy + r * math.sin(a))}")
    sw = max(4, round(r_out * 0.06))
    return (f'<path d="M {" L ".join(pts)} Z" fill="{fill}" stroke="{fill}" stroke-width="{sw}" '
            f'stroke-linejoin="round"/>')


def _inkify(art):
    return re.sub(r'(fill|stroke)="#[0-9A-Fa-f]{6}"', rf'\1="{SI}"', art)


def scl_doc(w, h, art, tier, s):
    """s = canvas units per output px at the asset's main use size. tier None = no shadow."""
    sh = ""
    if tier:
        d = _f(SCL_TIER[tier] / math.sqrt(2) * s)
        sh = f'<g opacity="0.2" transform="translate({d} {d})">{_inkify(art)}</g>\n'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
            f'{sh}<g>\n{art}\n</g>\n</svg>\n')


def _scale(canvas_w, width_frac):
    return canvas_w / (width_frac * 1080)


# ------------------------------------------------------------------ Inch (Small Change Lab mascot)
# Original paper snail facing right. 1024x1024, foot baseline y 1004, centred. The body group is identical
# in every pose; only eye stalks, eyes, mouth and sparks change.
IW = 1024
IS = _scale(IW, 0.22)  # ~4.31 units/px at default width
IA = 0.9 * IS          # wobble amplitude (~1.3 px)
_INCH_OUTLINE = [(78, 992), (92, 950), (160, 920), (320, 904), (480, 898), (604, 890), (654, 846), (680, 766),
                 (740, 688), (822, 654), (898, 674), (934, 748), (940, 850), (932, 942), (916, 994), (884, 1004),
                 (650, 1004), (380, 1004), (150, 1004), (90, 1003)]


def _spiral(cx, cy, r0, r1, turns, end_deg, n=72):
    T = turns * 2 * math.pi
    a0 = math.radians(end_deg) - T
    return [(cx + (r0 + (r1 - r0) * i / n) * math.cos(a0 + T * i / n),
             cy + (r0 + (r1 - r0) * i / n) * math.sin(a0 + T * i / n)) for i in range(n + 1)]


INCH_BODY = ('<g id="inch-body">\n'
             + wblob(_INCH_OUTLINE, SK, 401, IA) + "\n"
             + wrect(120, 974, 790, 30, 15, SP, 402, IA * 0.6) + "\n"
             + wcirc(400, 716, 192, SS, 403, IA, n=20) + "\n"
             + f'<path d="{_cr(_spiral(408, 710, 12, 150, 1.8, 58), closed=False)}" fill="none" stroke="{SI}" '
               f'stroke-width="22" stroke-linecap="round"/>\n</g>')

_STALK_BASE = ((800, 700), (872, 694))
_ER, _PR = 40, 17


def _stalks(tips):
    return "".join(f'<path d="M {bx} {by} L {tx} {ty}" stroke="{SK}" stroke-width="32" stroke-linecap="round"/>'
                   for (bx, by), (tx, ty) in zip(_STALK_BASE, tips))


def _eyes(tips, look=(8, 0), closed=False, lid=None):
    out = []
    for i, (x, y) in enumerate(tips):
        out.append(f'<circle cx="{x}" cy="{y}" r="{_ER}" fill="{SP}"/>')
        if closed:
            out.append(f'<path d="M {x - 21} {y + 8} Q {x} {y - 18} {x + 21} {y + 8}" fill="none" stroke="{SI}" '
                       f'stroke-width="12" stroke-linecap="round"/>')
        else:
            out.append(f'<circle cx="{x + look[0]}" cy="{y + look[1]}" r="{_PR}" fill="{SI}"/>')
        if lid == i or lid == "both":  # narrowed eye: Kraft lid over the top half
            out.append(f'<path d="M {x - _ER - 2} {y + 2} A {_ER + 2} {_ER + 2} 0 0 1 {x + _ER + 2} {y + 2} Z" fill="{SK}"/>')
    return "".join(out)


_MOUTHS = {
    "smile": f'<path d="M 866 826 Q 892 850 920 828" fill="none" stroke="{SI}" stroke-width="12" stroke-linecap="round"/>',
    "wavy": (f'<path d="M 862 836 Q 875 822 888 836 T 914 836" fill="none" stroke="{SI}" stroke-width="12" '
             f'stroke-linecap="round" stroke-linejoin="round"/>'),
    "open": (f'<path d="M 862 818 Q 892 866 924 818 Q 892 830 862 818 Z" fill="{SI}" stroke="{SI}" stroke-width="8" '
             f'stroke-linejoin="round"/>'),
    "big": (f'<path d="M 856 810 Q 892 880 928 810 Q 892 824 856 810 Z" fill="{SI}" stroke="{SI}" stroke-width="8" '
            f'stroke-linejoin="round"/>'),
    "flat": f'<path d="M 866 838 L 918 838" fill="none" stroke="{SI}" stroke-width="12" stroke-linecap="round"/>',
    "side": f'<path d="M 868 840 L 918 822" fill="none" stroke="{SI}" stroke-width="12" stroke-linecap="round"/>',
}


def _sparks(cx, cy):
    return "".join(f'<rect x="-11" y="-118" width="22" height="58" rx="11" fill="{SS}" '
                   f'transform="translate({cx},{cy}) rotate({a})"/>' for a in (-42, 0, 42))


def _inch_face(tips, mouth, look=(8, 0), closed=False, lid=None, extra=""):
    return _stalks(tips) + _eyes(tips, look, closed, lid) + _MOUTHS[mouth] + extra


# pose -> face group drawn over the shared body. Add poses here on the same canvas/baseline.
INCH_POSES = {
    "neutral": _inch_face([(782, 520), (892, 512)], "smile"),
    "worry": _inch_face([(744, 540), (930, 534)], "wavy", look=(0, -15)),
    "idea": _inch_face([(798, 508), (872, 504)], "open", look=(6, -10), extra=_sparks(835, 470)),
    "skeptical": _inch_face([(754, 556), (884, 490)], "side", look=(10, 2), lid=0),
    "cheer": _inch_face([(748, 520), (928, 512)], "big", closed=True),
    "tired": _inch_face([(738, 612), (944, 622)], "flat", look=(0, 12), lid="both"),
}


def inch(pose):
    return scl_doc(IW, IW, INCH_BODY + "\n" + INCH_POSES[pose], "front", IS)


# ------------------------------------------------------------------ SCL props
# Square 512 canvases with the base on the canvas bottom, so plans place them at y = 0.60 - half height.
def floor_strip():
    # 1080x884 at width 1.0, y 0.77: band top lands on y 0.60 and the band reaches the frame bottom.
    w, h, top = 1080, 884, 116
    rnd = random.Random(501)
    pts, x = [], -12
    while x <= w + 12:
        pts.append((x, top + rnd.uniform(-1.6, 1.6)))
        x += 40 * rnd.uniform(0.7, 1.3)
    d = "M " + " L ".join(f"{_f(px)} {_f(py)}" for px, py in pts) + f" L {w + 12} {h + 4} L -12 {h + 4} Z"
    grain = "".join(f'<rect x="{gx}" y="{gy}" width="{gw}" height="10" rx="5" fill="{SI}"/>'
                    for gx, gy, gw in ((150, 300, 150), (690, 520, 120)))
    return scl_doc(w, h, f'<path d="{d}" fill="{SK}"/>\n<g opacity="0.2">{grain}</g>', None, 1)


def _phone_body(s, a):
    return wrect(146, 80, 210, 428, 46, SI, 511, a)


def phone():
    s = _scale(512, 0.11); a = 0.6 * s
    return scl_doc(512, 512,
                   _phone_body(s, a)
                   + wrect(166, 116, 170, 360, 24, SY, 512, a * 0.6)
                   + f'<rect x="226" y="94" width="50" height="10" rx="5" fill="{SP}"/>'
                   + wrect(186, 160, 104, 44, 20, SP, 513, a * 0.4)
                   + wrect(212, 222, 104, 44, 20, SP, 514, a * 0.4), "front", s)


def phone_facedown():
    s = _scale(512, 0.11); a = 0.6 * s
    return scl_doc(512, 512,
                   _phone_body(s, a)
                   + wrect(160, 94, 182, 400, 36, SK, 515, a * 0.6)
                   + wrect(182, 118, 76, 110, 26, SI, 516, a * 0.4)
                   + f'<circle cx="220" cy="148" r="15" fill="{SK}"/><circle cx="220" cy="196" r="15" fill="{SK}"/>',
                   "front", s)


def notification_dot():
    s = _scale(512, 0.05)
    return scl_doc(512, 512,
                   burst(226, 226, 206, 182, 12, SC, 521, 4)
                   + f'<rect x="202" y="96" width="48" height="166" rx="24" fill="{SP}"/>'
                   + f'<circle cx="226" cy="324" r="29" fill="{SP}"/>', "front", s)


def book_closed():
    s = _scale(512, 0.2); a = 0.8 * s
    lines = "".join(f'<rect x="92" y="{y}" width="{w}" height="7" rx="3.5" fill="{SY}"/>'
                    for y, w in ((382, 330), (414, 300), (446, 320)))
    return scl_doc(512, 512,
                   wrect(40, 318, 420, 190, 22, SY, 531, a)
                   + wrect(70, 352, 376, 120, 12, SP, 532, a * 0.6)
                   + lines
                   + f'<path d="M 360 460 L 360 504 L 378 492 L 396 504 L 396 460 Z" fill="{SS}" stroke="{SS}" '
                     f'stroke-width="6" stroke-linejoin="round"/>', "front", s)


def book_open():
    s = _scale(512, 0.2); a = 1.0 * s
    cover = [(26, 380), (130, 360), (256, 392), (382, 360), (486, 380), (486, 492), (382, 478), (256, 510),
             (130, 478), (26, 492)]
    left = [(44, 364), (140, 336), (250, 372), (250, 488), (140, 458), (44, 474)]
    right = [(262, 372), (372, 336), (468, 364), (468, 474), (372, 458), (262, 488)]

    def rule(x0, x1, y0, sag, flip):
        return f'M {x0} {y0 + (sag if flip else 0)} Q {(x0 + x1) / 2} {y0 - 14} {x1} {y0 + (0 if flip else sag)}'
    lines = " ".join([rule(70, 228, 392, 18, False), rule(70, 228, 424, 18, False), rule(70, 200, 456, 16, False),
                      rule(284, 442, 392, 18, True), rule(284, 442, 424, 18, True), rule(312, 442, 456, 16, True)])
    return scl_doc(512, 512,
                   wblob(cover, SY, 541, a)
                   + wblob(left, SP, 542, a * 0.6) + wblob(right, SP, 543, a * 0.6)
                   + f'<path d="{lines}" fill="none" stroke="{SY}" stroke-width="7" stroke-linecap="round"/>'
                   + f'<path d="M 300 360 L 300 300 L 318 314 L 336 300 L 336 352 Z" fill="{SS}" stroke="{SS}" '
                     f'stroke-width="6" stroke-linejoin="round"/>', "front", s)


def laptop():
    s = _scale(512, 0.22); a = 0.8 * s
    bars = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="18" rx="9" fill="{SP}"/>'
                   for x, y, w in ((112, 226, 170), (112, 266, 230), (112, 306, 120)))
    return scl_doc(512, 512,
                   wrect(64, 168, 380, 292, 26, SI, 551, a)
                   + wrect(88, 192, 332, 244, 12, SY, 552, a * 0.6)
                   + bars
                   + wblob([(14, 462), (254, 456), (494, 462), (488, 500), (470, 508), (254, 508), (38, 508), (20, 500)],
                           SI, 553, a)
                   + f'<rect x="210" y="466" width="88" height="12" rx="6" fill="{SP}"/>', "front", s)


def clock_face():
    s = _scale(512, 0.16); a = 0.8 * s
    ticks = "".join(f'<rect x="-9" y="-176" width="18" height="38" rx="9" fill="{SI}" '
                    f'transform="translate(246,246) rotate({r})"/>' for r in (0, 90, 180, 270))
    return scl_doc(512, 512,
                   wcirc(246, 246, 226, SK, 561, a, n=22)
                   + wcirc(246, 246, 190, SP, 562, a * 0.7, n=20)
                   + ticks
                   + f'<g transform="translate(246,246)">'
                     f'<rect x="-13" y="-104" width="26" height="118" rx="13" fill="{SI}" transform="rotate(62)"/>'
                     f'<rect x="-10" y="-150" width="20" height="164" rx="10" fill="{SI}" transform="rotate(-24)"/></g>'
                   + f'<circle cx="246" cy="246" r="20" fill="{SS}"/>', "front", s)


def ice_cube():
    # Plans shrink it with transform.scale and lower y so the base stays on the floor: keep the base at the bottom.
    s = _scale(512, 0.13); a = 0.7 * s
    return scl_doc(512, 512,
                   wblob([(50, 497), (150, 488), (360, 488), (462, 497), (446, 508), (66, 508)], SY, 571, a * 0.5)
                   + wrect(78, 136, 348, 348, 64, SY, 572, a)
                   + f'<path d="M 128 330 L 128 238 Q 128 186 180 186 L 262 186" fill="none" stroke="{SP}" '
                     f'stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>'
                   + f'<circle cx="324" cy="186" r="16" fill="{SP}"/>',
                   "front", s)


def later_note():
    # No text: the LATER label is a KineticText element in the plan.
    s = _scale(512, 0.16); a = 1.2 * s; b = round(4 * s)  # Ink 4 px border
    lines = "".join(f'<rect x="96" y="{y}" width="{w}" height="9" rx="4.5" fill="{SY}"/>'
                    for y, w in ((300, 300), (360, 300), (420, 220)))
    return scl_doc(512, 512,
                   f'<path d="M 48 104 L 452 104 L 452 404 L 352 504 L 48 504 Z" fill="{SP}" stroke="{SI}" '
                   f'stroke-width="{b}" stroke-linejoin="round"/>'
                   + wrect(54 + b // 2, 110 + b // 2, 392 - b, 60, 6, SY, 581, a * 0.4)
                   + lines
                   + f'<path d="M 452 404 L 352 504 Q 366 432 452 404 Z" fill="{SP}" stroke="{SI}" stroke-width="{b}" '
                     f'stroke-linejoin="round"/>', "front", s)


# ------------------------------------------------------------------ SCL UI
def check_mint():
    s = _scale(512, 0.09)
    return scl_doc(512, 512,
                   wcirc(236, 236, 214, SM, 601, 1.2 * s, n=20)
                   + f'<path d="M 132 246 L 206 318 L 346 168" fill="none" stroke="{SP}" stroke-width="62" '
                     f'stroke-linecap="round" stroke-linejoin="round"/>', "front", s)


def cross_coral():
    s = _scale(512, 0.09)
    return scl_doc(512, 512,
                   burst(236, 236, 224, 192, 14, SC, 611, 5)
                   + f'<path d="M 162 162 L 310 310 M 310 162 L 162 310" fill="none" stroke="{SP}" stroke-width="58" '
                     f'stroke-linecap="round"/>', "front", s)


def cite_card():
    # 820x500 at width 0.76 (1 unit = 1 px). Tab text, source, finding, limit line and the Coral limit dot are
    # engine elements; the tab sits where the plan puts 'THE STUDY' (canvas ~ (152, 29)).
    s = _scale(820, 0.76)
    return scl_doc(820, 500,
                   wrect(8, 40, 796, 444, 18, SP, 621, 1.3, step=80, attrs=f' stroke="{SI}" stroke-width="4"')
                   + f'<path d="M 40 178 L 772 178 M 40 346 L 772 346" stroke="{SY}" stroke-width="4" stroke-linecap="round"/>'
                   + wrect(8, 4, 288, 60, 14, SS, 622, 1.0, step=60, attrs=f' stroke="{SI}" stroke-width="4"'),
                   "front", s)


def step_slate():
    # Numeral is KineticText on top.
    s = _scale(600, 0.3)
    return scl_doc(600, 600,
                   wcirc(290, 290, 262, SS, 631, 5, n=16)
                   + f'<path d="M 108 236 Q 136 140 232 104" fill="none" stroke="{SP}" stroke-width="20" stroke-linecap="round"/>',
                   "front", s)


def try_today_note():
    # Brand marker: fixed lettering baked in (safe system font, fixed textLength).
    s = _scale(600, 0.42)
    txt = (f'<text x="292" y="{{y}}" text-anchor="middle" font-family="{SCL_FONT}" font-weight="900" font-size="138" '
           f'fill="{SI}" textLength="{{tl}}" lengthAdjust="spacingAndGlyphs">{{t}}</text>')
    return scl_doc(600, 600,
                   wblob([(40, 40), (300, 38), (560, 40), (562, 240), (560, 440), (440, 560), (240, 562), (40, 560),
                          (38, 300)], SS, 641, 1.6)
                   + txt.format(y=250, tl=400, t="TRY IT")
                   + txt.format(y=410, tl=440, t="TODAY")
                   + f'<rect x="96" y="446" width="300" height="20" rx="10" fill="{SI}"/>'
                   + f'<path d="M 560 440 L 440 560 Q 452 466 560 440 Z" fill="{SP}" stroke="{SP}" stroke-width="6" '
                     f'stroke-linejoin="round"/>', "front", s)


def phone_glow():
    # Jagged 12-point Sun glow behind the phone (jagged edge = problem). Flat, no shadow, 80% opacity.
    return scl_doc(512, 512, burst(256, 256, 248, 176, 12, SS, 701, 5).replace("/>", ' opacity="0.8"/>'), None, 1)


def lamp_dim():
    # Small bedside lamp, base on the canvas bottom. 5 pieces, calm rounded shapes.
    s = _scale(512, 0.2); a = 0.8 * s
    return scl_doc(512, 512,
                   wrect(150, 456, 212, 48, 24, SK, 711, a)
                   + wrect(236, 300, 40, 170, 18, SK, 712, a * 0.6)
                   + wcirc(256, 270, 52, SP, 713, a * 0.5, n=14)
                   + wblob([(104, 292), (136, 140), (200, 100), (312, 100), (376, 140), (408, 292), (256, 306)],
                           SS, 714, a)
                   + wrect(190, 128, 80, 22, 11, SP, 715, a * 0.4, step=40, attrs=' opacity="0.7"'), "front", s)


# ------------------------------------------------------------------ 03-motivation-vs-discipline props / UI
_GLYPHS = {
    "M": [[(0, 1), (0, 0), (.5, .55), (1, 0), (1, 1)]], "Y": [[(0, 0), (.5, .5), (1, 0)], [(.5, .5), (.5, 1)]],
    "T": [[(0, 0), (1, 0)], [(.5, 0), (.5, 1)]], "H": [[(0, 0), (0, 1)], [(1, 0), (1, 1)], [(0, .5), (1, .5)]],
    "A": [[(0, 1), (.5, 0), (1, 1)], [(.2, .68), (.8, .68)]],
    "C": [[(1, .15), (.6, 0), (.2, .1), (0, .5), (.2, .9), (.6, 1), (1, .85)]],
    "U": [[(0, 0), (0, .7), (.25, 1), (.75, 1), (1, .7), (1, 0)]], "L": [[(0, 0), (0, 1), (1, 1)]],
    "E": [[(1, 0), (0, 0), (0, 1), (1, 1)], [(0, .5), (.8, .5)]],
    "B": [[(0, 0), (0, 1)], [(0, 0), (.7, 0), (1, .2), (.7, .5), (0, .5)], [(0, .5), (.8, .5), (1, .75), (.7, 1), (0, 1)]],
    "?": [[(0, .2), (.2, 0), (.8, 0), (1, .2), (.5, .55), (.5, .72)], [(.5, .96), (.5, 1)]],
}


def _word_paths(word, x0, x1, y0, h, sw, color):
    """Block letters drawn as thick round-capped stroke paths (no <text>)."""
    n = len(word); gap = h * 0.32
    lw = ((x1 - x0) - gap * (n - 1)) / n
    out = []
    for i, ch in enumerate(word):
        ox = x0 + i * (lw + gap)
        for st in _GLYPHS[ch]:
            d = " L ".join(f"{_f(ox + px * lw)} {_f(y0 + py * h)}" for px, py in st)
            out.append(f'<path d="M {d}" fill="none" stroke="{color}" stroke-width="{sw}" '
                       f'stroke-linecap="round" stroke-linejoin="round"/>')
    return "".join(out)


def _stamp(word, fill, seed, x0, x1):
    s = _scale(512, 0.4)
    return scl_doc(512, 256,
                   wrect(20, 32, 472, 192, 22, fill, seed, 1.0 * s, step=70)
                   + f'<rect x="38" y="50" width="436" height="156" rx="12" fill="none" stroke="{SP}" stroke-width="7"/>'
                   + _word_paths(word, x0, x1, 82, 92, 22, SP), "front", s)


def myth_stamp():
    return _stamp("MYTH?", SC, 801, 96, 416)


def actually_stamp():
    return _stamp("MAYBE", SM, 811, 96, 416)


def battery_low():
    # Vertical battery 400x640 (use width 0.26): nub, body, coral sliver, three dashed empty cells.
    s = _scale(400, 0.26); a = 0.8 * s
    cell = (f' fill="none" stroke="{SI}" stroke-width="{round(4 * s)}" stroke-dasharray="{round(14 * s)} {round(10 * s)}"')
    cells = "".join(f'<rect x="96" y="{y}" width="168" height="{round(62 * s * 0.8)}" rx="14"{cell}/>' for y in (190, 290, 390))
    return scl_doc(400, 640,
                   wrect(120, 22, 120, 50, 12, SI, 821, a * 0.5, step=50)
                   + wrect(60, 60, 240, 540, 36, SP, 822, a, step=80, attrs=f' stroke="{SI}" stroke-width="{round(4 * s)}"')
                   + cells
                   + wrect(96, 500, 168, 64, 14, SC, 823, a * 0.6, step=50), "front", s)


def timer_2min():
    s = _scale(512, 0.2); a = 0.8 * s
    ticks = "".join(f'<rect x="-8" y="-176" width="16" height="34" rx="8" fill="{SI}" '
                    f'transform="translate(256,290) rotate({r})"/>' for r in (0, 90, 180, 270))
    return scl_doc(512, 512,
                   wrect(222, 56, 68, 52, 14, SI, 831, a * 0.5, step=40)
                   + wcirc(256, 290, 200, SS, 832, a, n=22)
                   + wcirc(256, 290, 156, SP, 833, a * 0.7, n=20)
                   + ticks
                   + f'<rect x="250" y="190" width="14" height="108" rx="7" fill="{SI}"/>'
                   + f'<rect x="250" y="284" width="92" height="14" rx="7" fill="{SI}" transform="rotate(-40 257 291)"/>'
                   + f'<circle cx="257" cy="291" r="16" fill="{SS}" stroke="{SI}" stroke-width="6"/>', "front", s)


def checklist_note():
    # Box positions kept at x130-186, y 150/250/350 (check_mint ticks are placed on them by the plan).
    s = _scale(512, 0.2); a = 0.8 * s
    rows = "".join(f'<rect x="130" y="{y}" width="56" height="56" rx="10" fill="none" stroke="{SI}" stroke-width="7"/>'
                   f'<rect x="212" y="{y + 21}" width="170" height="14" rx="7" fill="{SY}"/>' for y in (150, 250, 350))
    return scl_doc(512, 512,
                   wrect(90, 50, 330, 430, 24, SP, 841, a, step=80, attrs=f' stroke="{SI}" stroke-width="5"')
                   + wrect(95, 55, 320, 62, 20, SY, 842, a * 0.4, step=60)
                   + rows, "front", s)


SCL_DRAWERS = {
    **{f"inch_{p}": (lambda p=p: inch(p)) for p in INCH_POSES},
    "floor_strip": floor_strip, "phone": phone, "phone_facedown": phone_facedown, "notification_dot": notification_dot,
    "book_closed": book_closed, "book_open": book_open, "laptop": laptop, "clock_face": clock_face, "ice_cube": ice_cube,
    "later_note": later_note, "check_mint": check_mint, "cross_coral": cross_coral, "cite_card": cite_card,
    "phone_glow": phone_glow, "lamp_dim": lamp_dim,
    "step_slate": step_slate, "try_today_note": try_today_note,
    "myth_stamp": myth_stamp, "actually_stamp": actually_stamp, "battery_low": battery_low,
    "timer_2min": timer_2min, "checklist_note": checklist_note,
}


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
DRAWERS.update(SCL_DRAWERS)  # Small Change Lab (inch_<pose> ids are flat files)
POSES = {"tuck": TUCK_POSES, "inch": INCH_POSES}


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
