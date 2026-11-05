#!/usr/bin/env python3
"""Make a timestamped contact sheet from a video, or a labelled sheet from a folder of stills.

Video:  python scripts/make_contact_sheet.py out.mp4 [--tile 4x6] [--output sheet.jpg]
Stills: python scripts/make_contact_sheet.py --images projects/<id>/output/stills [--tile 4x4]
        (labels come from the PNG filenames, e.g. scene-01_1.50s.png)
"""
from pathlib import Path
import argparse, shutil, subprocess, sys, tempfile

from _media import duration_sec, require_tools

FONT_CANDIDATES = [Path("C:/Windows/Fonts/arialbd.ttf"), Path("C:/Windows/Fonts/arial.ttf"),
                   Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
                   Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")]


def font_opt() -> str:
    for f in FONT_CANDIDATES:
        if f.is_file():
            return "fontfile='" + f.as_posix().replace(":", "\\:") + "':"
    return ""


def label_filter(text_expr: str) -> str:
    return (f"drawtext={font_opt()}text='{text_expr}':fontsize=22:fontcolor=white:"
            "box=1:boxcolor=black@0.65:boxborderw=6:x=8:y=8")


def run(cmd) -> bool:
    return subprocess.run(cmd, capture_output=True, text=True).returncode == 0


def sheet_from_video(ffmpeg, video: Path, output: Path, tile: str) -> None:
    cols, rows = (int(x) for x in tile.lower().split("x"))
    n = cols * rows
    dur = duration_sec(video)
    step = dur / n  # n evenly spaced frames; select keeps source timestamps so labels are exact
    base = f"select='isnan(prev_selected_t)+gte(t-prev_selected_t\\,{step:.4f})',scale=240:-2"
    stamp = label_filter("%{pts\\:hms}")
    for vf in (base + "," + stamp + ",tile=" + tile, base + ",tile=" + tile):
        if run([ffmpeg, "-y", "-v", "error", "-i", str(video), "-vf", vf, "-frames:v", "1", "-q:v", "3", str(output)]):
            if "drawtext" not in vf:
                print("WARNING: timestamp labels unavailable (drawtext failed); sheet has no labels.")
            return
    raise SystemExit("ffmpeg failed to build the contact sheet.")


def sheet_from_images(ffmpeg, folder: Path, output: Path, tile: str) -> None:
    images = sorted(folder.glob("*.png"))
    if not images:
        raise SystemExit(f"No PNG files in {folder}")
    max_cols = int(tile.lower().split("x")[0])
    cols = min(max_cols, len(images))
    tile = f"{cols}x{-(-len(images) // cols)}"  # fit the grid to the number of stills
    with tempfile.TemporaryDirectory() as tmp:
        for i, img in enumerate(images):
            label = img.stem.replace("_", " ").replace(":", "-").replace("'", "")
            dst = Path(tmp) / f"f{i:04d}.png"
            if not run([ffmpeg, "-y", "-v", "error", "-i", str(img), "-vf", f"scale=270:-2,{label_filter(label)}", str(dst)]):
                run([ffmpeg, "-y", "-v", "error", "-i", str(img), "-vf", "scale=270:-2", str(dst)])
        if not run([ffmpeg, "-y", "-v", "error", "-framerate", "1", "-i", str(Path(tmp) / "f%04d.png"),
                    "-vf", f"tile={tile}", "-frames:v", "1", "-q:v", "3", str(output)]):
            raise SystemExit("ffmpeg failed to tile stills.")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("video", type=Path, nargs="?")
    p.add_argument("--images", type=Path, help="Folder of PNG stills instead of a video")
    p.add_argument("--output", type=Path)
    p.add_argument("--tile", default="4x6", help="Columns x rows")
    args = p.parse_args()
    ffmpeg = require_tools("ffmpeg", "ffprobe")["ffmpeg"]

    if args.images:
        folder = args.images.resolve()
        output = (args.output or folder.parent / "stills-contact-sheet.jpg").resolve()
        sheet_from_images(ffmpeg, folder, output, args.tile if args.tile != "4x6" else "4x4")
    elif args.video:
        video = args.video.resolve()
        if not video.is_file():
            raise SystemExit(f"Video not found: {video}")
        output = (args.output or video.with_name(video.stem + "-contact-sheet.jpg")).resolve()
        sheet_from_video(ffmpeg, video, output, args.tile)
    else:
        p.error("give a video path or --images <folder>")
    print(output)


if __name__ == "__main__":
    main()
