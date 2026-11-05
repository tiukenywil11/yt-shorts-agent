#!/usr/bin/env python3
"""Rasterize SVG assets to preview PNGs with headless Chrome/Edge, for visual review.

The engine loads SVGs directly (Remotion <Img> in Chrome); these PNGs are review-only.

  python scripts/svg_preview.py projects/<id>                # all SVGs under assets/
  python scripts/svg_preview.py projects/<id> --only tuck    # path substring filter
  python scripts/svg_preview.py projects/<id> --size 640

Writes projects/<id>/previews/assets/<relative_path_with__>.png, then (unless --no-sheet)
a contact sheet via scripts/make_contact_sheet.py --images.
"""
from pathlib import Path
import argparse, html, os, re, shutil, subprocess, sys, tempfile

BROWSERS = [
    Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Google/Chrome/Application/chrome.exe",
    Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Microsoft/Edge/Application/msedge.exe",
    Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Microsoft/Edge/Application/msedge.exe",
]
for name in ("chrome", "google-chrome", "chromium", "msedge"):
    found = shutil.which(name)
    if found:
        BROWSERS.append(Path(found))

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:{s}px;height:{s}px;overflow:hidden}}
body{{background:#fff;background-image:linear-gradient(45deg,#ddd 25%,transparent 25%),
linear-gradient(-45deg,#ddd 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#ddd 75%),
linear-gradient(-45deg,transparent 75%,#ddd 75%);background-size:32px 32px;
background-position:0 0,0 16px,16px -16px,-16px 0;display:flex;align-items:center;justify-content:center}}
img{{width:{s}px;height:{s}px;object-fit:contain}}
</style></head><body><img src="{src}"></body></html>"""


def browser() -> Path:
    for b in BROWSERS:
        if b.is_file():
            return b
    sys.exit("No Chrome/Edge found for SVG preview.")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project_dir", type=Path)
    ap.add_argument("--only", default="", help="substring filter on the relative SVG path")
    ap.add_argument("--size", type=int, default=512)
    ap.add_argument("--no-sheet", action="store_true")
    a = ap.parse_args()

    proj = a.project_dir.resolve()
    svgs = sorted(p for p in (proj / "assets").rglob("*.svg") if a.only in p.relative_to(proj).as_posix())
    if not svgs:
        print("No SVGs found.")
        return 1
    out_dir = proj / "previews" / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    exe = browser()
    failed = []
    with tempfile.TemporaryDirectory() as tmp:
        for svg in svgs:
            rel = svg.relative_to(proj / "assets").with_suffix("").as_posix()
            name = re.sub(r"[^A-Za-z0-9_.-]", "__", rel) + ".png"
            page = Path(tmp) / "page.html"
            page.write_text(PAGE.format(s=a.size, src=html.escape(svg.as_uri())), encoding="utf-8")
            out = out_dir / name
            cmd = [str(exe), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                   "--allow-file-access-from-files", f"--window-size={a.size},{a.size}",
                   f"--screenshot={out}", page.as_uri()]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if r.returncode != 0 or not out.is_file():
                failed.append(rel)
            else:
                print(f"ok  {out.relative_to(proj)}")
    if failed:
        print("FAILED:", ", ".join(failed))
    if not a.no_sheet and len(svgs) > len(failed):
        sheet = proj / "previews" / "assets_contact_sheet.jpg"
        here = Path(__file__).resolve().parent
        subprocess.run([sys.executable, str(here / "make_contact_sheet.py"), "--images", str(out_dir),
                        "--tile", "6x5", "--output", str(sheet)], check=False)
        print(f"sheet: {sheet.relative_to(proj)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
