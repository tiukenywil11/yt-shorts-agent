#!/usr/bin/env python3
"""Assert a rendered MP4 matches the expected render mode and decodes cleanly.

Prints PASS/FAIL/WARN lines so no LLM needs to read raw ffprobe output.
Usage: python scripts/check_video.py out.mp4 --expect final [--project projects/<id>] [--partial]
"""
from pathlib import Path
import argparse, json, re, subprocess, sys

from _media import load_registry, probe, ratio, require_tools


def main():
    p = argparse.ArgumentParser()
    p.add_argument("video", type=Path)
    p.add_argument("--expect", choices=["draft", "preview", "final"], required=True)
    p.add_argument("--project", type=Path, help="Project dir; checks duration against animation.json")
    p.add_argument("--partial", action="store_true", help="Scene clip: skip full-duration check")
    args = p.parse_args()
    tools = require_tools("ffprobe", "ffmpeg")

    fails, warns, passes = [], [], []
    video = args.video.resolve()
    if not video.is_file() or video.stat().st_size == 0:
        print(f"FAIL: file missing or empty: {video}")
        sys.exit(1)

    mode = load_registry()["modes"][args.expect]
    info = probe(video)
    vs = [s for s in info["streams"] if s["codec_type"] == "video"]
    aus = [s for s in info["streams"] if s["codec_type"] == "audio"]
    dur = float(info["format"].get("duration", 0))

    if not vs:
        fails.append("no video stream")
    else:
        v = vs[0]
        size = (v.get("width"), v.get("height"))
        (passes if size == (mode["width"], mode["height"]) else fails).append(
            f"resolution {size[0]}x{size[1]} (expected {mode['width']}x{mode['height']})")
        fps = ratio(v.get("avg_frame_rate") or v.get("r_frame_rate"))
        (passes if abs(fps - mode["fps"]) < 0.05 else fails).append(f"fps {fps:.2f} (expected {mode['fps']})")
        (passes if v.get("codec_name") == "h264" else fails).append(f"video codec {v.get('codec_name')} (expected h264)")
        (passes if v.get("pix_fmt") == "yuv420p" else warns).append(f"pix_fmt {v.get('pix_fmt')} (yuv420p is safest for YouTube)")
    if not aus:
        fails.append("no audio stream (expected AAC)")
    else:
        (passes if aus[0].get("codec_name") == "aac" else fails).append(f"audio codec {aus[0].get('codec_name')} (expected aac)")

    if args.project and not args.partial:
        plan = json.loads((args.project / "animation.json").read_text(encoding="utf-8-sig"))
        want = float(plan["video"]["durationSec"])
        tol = 1.0 / mode["fps"] + 0.1
        (passes if abs(dur - want) <= tol else fails).append(f"duration {dur:.2f}s (expected {want:.2f}s ±{tol:.2f})")
    else:
        passes.append(f"duration {dur:.2f}s")
    if dur > 60 and not args.partial:
        warns.append(f"duration {dur:.1f}s exceeds 60s")

    # One decode pass: decode errors + long black or silent stretches.
    cmd = [tools["ffmpeg"], "-hide_banner", "-nostats", "-loglevel", "repeat+level+info", "-i", str(video),
           "-vf", "blackdetect=d=0.5:pix_th=0.06"]
    if aus:
        cmd += ["-af", "silencedetect=n=-50dB:d=2"]
    cmd += ["-f", "null", "-"]
    res = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    errors = [ln for ln in res.stderr.splitlines() if "[error]" in ln or "[fatal]" in ln]
    if res.returncode != 0 or errors:
        fails.append("decode errors: " + "; ".join(errors[:3]) if errors else f"ffmpeg exit {res.returncode}")
    else:
        passes.append("full decode clean")
    for m in re.finditer(r"black_start:([\d.]+) black_end:([\d.]+)", res.stderr):
        warns.append(f"black frames {float(m[1]):.2f}-{float(m[2]):.2f}s")
    for m in re.finditer(r"silence_start: ([\d.]+)", res.stderr):
        warns.append(f"silence (>2s) starting at {float(m[1]):.2f}s")

    for x in passes: print(f"PASS: {x}")
    for x in warns: print(f"WARN: {x}")
    for x in fails: print(f"FAIL: {x}")
    print(f"RESULT: {'FAIL' if fails else 'PASS'} ({video.name}, mode={args.expect})")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
