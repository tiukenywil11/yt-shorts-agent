#!/usr/bin/env python
"""Scripted retention checks for a Short's script.json (and animation.json when present).

  python scripts/retention_lint.py projects/<id>

Rules come from creative/style-bible.md > Story and pacing. They are hypotheses until
analytics back them (see creative/viral-audit-2026-11-08.md). Exit code 1 on any FAIL.
"""
import argparse
import json
import re
import sys
import wave
from pathlib import Path

HEDGE = re.compile(r"\b(may|might|could|possibly|perhaps|probably)\b", re.I)
FILLER = re.compile(r"(a practical way to try this|here'?s how|let'?s dive|did you know|in this video)", re.I)
CAVEAT = re.compile(
    r"(results? (may )?(vary|differ)|may differ|not (financial|medical) advice|"
    r"follow your local guidance|ask a clinician|real work varies|linked, not proven)",
    re.I,
)
STUDY_OPENER = re.compile(r"^(in )?an? (\d{4}|recent)\b.*\b(study|paper|survey)\b", re.I)


def first_sentence(text):
    return re.split(r"(?<=[.?!])\s", text.strip())[0]


def lint(project):
    segments = json.loads((project / "script.json").read_text(encoding="utf-8"))["segments"]
    results = []
    add = lambda level, msg: results.append((level, msg))

    opening = first_sentence(segments[0]["text"])
    words = len(opening.split())
    if words > 12:
        add("FAIL", f"opening sentence is {words} words (max 12): {opening!r}")
    if HEDGE.search(opening):
        add("FAIL", f"hedge word in opening sentence, move it to the finding: {opening!r}")

    timed = all("startSec" in s and "durationSec" in s for s in segments)
    end = segments[-1]["startSec"] + segments[-1]["durationSec"] if timed else None
    if timed:
        if end > 50:
            add("FAIL", f"length {end:.1f} s is over the 50 s cap")
        elif end > 35:
            add("WARN", f"length {end:.1f} s is over the 25-35 s target")
        for s in segments:
            if s["durationSec"] > 8:
                add("WARN", f"{s['id']} runs {s['durationSec']:.1f} s in one block; split it or cut it")
        caveat = sum(s["durationSec"] for s in segments if CAVEAT.search(s["text"]))
        if caveat > 2.5:
            add("FAIL", f"spoken caveat lines total {caveat:.1f} s (max 2.5); move limits to the card and tags")
    else:
        add("WARN", "no timings yet; run audio_timing.py for length and caveat checks")

    for s in segments:
        if FILLER.search(s["text"]):
            add("FAIL", f"{s['id']} contains filler: {FILLER.search(s['text']).group(0)!r}")
        if STUDY_OPENER.search(s["text"]):
            add("WARN", f"{s['id']} names the study before the result; lead with what happened")

    last = segments[-1]["text"]
    if not last.lower().startswith("try it today"):
        add("WARN", "last segment does not start with 'Try it today'")

    animation = project / "animation.json"
    voice = project / "voiceover.wav"
    if animation.exists() and voice.exists():
        duration = json.loads(animation.read_text(encoding="utf-8"))["video"].get("durationSec")
        with wave.open(str(voice), "rb") as w:
            voice_end = w.getnframes() / w.getframerate()
        if duration is not None and duration - voice_end > 0.15:
            add("FAIL", f"video runs {duration - voice_end:.2f} s past the voiceover (max 0.15)")

    return results, end


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    results, end = lint(args.project)
    for level, msg in results:
        print(f"{level}: {msg}")
    failed = any(level == "FAIL" for level, _ in results)
    length = f", {end:.1f} s" if end is not None else ""
    print(f"RESULT: {'FAIL' if failed else 'PASS'}{length}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
