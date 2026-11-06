#!/usr/bin/env python3
"""Reconcile script.json segment timing with real voice audio.

Mode A (exact): every segment has assets/voice/<segment-id>.wav (written by tts.py or recorded by you).
  -> concatenates them with --gap seconds of silence into voiceover.wav and writes exact timings.
Mode B (estimate): only voiceover.wav exists -> splits its duration by segment text length.

Writes startSec/durationSec into each script.json segment plus voiceoverDurationSec, and prints
the recommended video.durationSec. Usage: python scripts/audio_timing.py projects/<id> [--gap 0.25]
"""
from pathlib import Path
import argparse, json, subprocess

from _media import duration_sec, require_tools


def main():
    p = argparse.ArgumentParser()
    p.add_argument("project_dir", type=Path)
    p.add_argument("--gap", type=float, default=0.25, help="Silence between segments (exact mode)")
    p.add_argument("--tail", type=float, default=0.6, help="Padding after narration for the video end")
    p.add_argument("--lufs", type=float, default=-14.0, help="Normalise voiceover.wav to this integrated loudness (exact mode); 0 disables")
    args = p.parse_args()
    project = args.project_dir.resolve()
    tools = require_tools("ffmpeg", "ffprobe")

    script_path = project / "script.json"
    script = json.loads(script_path.read_text(encoding="utf-8-sig"))
    segments = script.get("segments", [])
    if not segments:
        raise SystemExit("script.json has no segments.")

    voice_dir = project / "assets" / "voice"
    seg_files = [voice_dir / f"{s['id']}.wav" for s in segments]
    output = project / "voiceover.wav"

    if all(f.is_file() for f in seg_files):
        mode = "exact"
        durations = [duration_sec(f) for f in seg_files]
        inputs, chains = [], []
        for i, f in enumerate(seg_files):
            inputs += ["-i", str(f)]
            pad = args.gap if i < len(seg_files) - 1 else 0
            chains.append(f"[{i}:a]aresample=48000,aformat=sample_fmts=s16:channel_layouts=mono,apad=pad_dur={pad}[a{i}]")
        graph = ";".join(chains) + ";" + "".join(f"[a{i}]" for i in range(len(seg_files))) + \
            f"concat=n={len(seg_files)}:v=0:a=1"
        if args.lufs:  # Shorts loudness target (style bible: about -14 LUFS, true peak <= -1.5 dBTP)
            # light compression first so the true-peak cap doesn't hold loudness ~2 LU under target
            graph += (f"[cat];[cat]acompressor=threshold=-24dB:ratio=4:attack=3:release=60:makeup=4,"
                      f"loudnorm=I={args.lufs}:TP=-1.5:LRA=7,aresample=48000[out]")
        else:
            graph += "[out]"
        subprocess.run([tools["ffmpeg"], "-y", "-v", "error", *inputs, "-filter_complex", graph,
                        "-map", "[out]", "-c:a", "pcm_s16le", str(output)], check=True)
        t = 0.0
        for seg, d in zip(segments, durations):
            seg["startSec"], seg["durationSec"] = round(t, 3), round(d, 3)
            t += d + args.gap
    elif output.is_file():
        mode = "estimate"
        total = duration_sec(output)
        weights = [max(len(s.get("text", "")), 1) for s in segments]
        t = 0.0
        for seg, w in zip(segments, weights):
            d = total * w / sum(weights)
            seg["startSec"], seg["durationSec"] = round(t, 3), round(d, 3)
            t += d
    else:
        raise SystemExit("No audio found: add assets/voice/<segment-id>.wav per segment (run tts.py) or voiceover.wav.")

    vo_len = duration_sec(output)
    script["voiceoverDurationSec"] = round(vo_len, 3)
    script["timingMode"] = mode
    script_path.write_text(json.dumps(script, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    recommended = round(vo_len + args.tail, 2)
    print(f"Timing mode: {mode} | segments: {len(segments)} | voiceover: {vo_len:.2f}s")
    print(f"Recommended video.durationSec: {recommended}")
    if vo_len > 60:
        print("WARNING: narration exceeds 60s; Shorts must be <= 60s for best reach. Trim the script.")


if __name__ == "__main__":
    main()
