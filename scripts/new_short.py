#!/usr/bin/env python3
"""Create a predictable project folder for one animated Short."""
from pathlib import Path
import argparse, json, re
from datetime import date

ROOT = Path(__file__).resolve().parents[1]


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video_id")
    parser.add_argument("--duration", type=float, default=45)
    args = parser.parse_args()

    video_id = args.video_id.strip().lower()
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{1,48}", video_id):
        raise SystemExit("Use 2-49 lowercase letters, numbers, hyphens, or underscores.")
    project = ROOT / "projects" / video_id
    if project.exists():
        raise SystemExit(f"Project already exists: {project}")

    for folder in ("assets/voice", "assets/sfx", "previews", "cache", "output"):
        (project / folder).mkdir(parents=True, exist_ok=True)

    (project / "idea.md").write_text(
        f"# {video_id}\n\n- Created: {date.today().isoformat()}\n"
        "- Topic: TODO\n- Audience: TODO\n- Hook: TODO\n- Payoff: TODO\n",
        encoding="utf-8",
    )
    (project / "storyboard.md").write_text(f"# Storyboard: {video_id}\n\nTODO\n", encoding="utf-8")
    write_json(project / "script.json", {"segments": [], "targetDurationSec": args.duration, "voice": None})
    write_json(project / "storyboard.json", {"scenes": [], "targetDurationSec": args.duration})
    write_json(project / "asset-requirements.json", {"missing": []})
    write_json(project / "animation.json", {
        "schemaVersion": "1.0",
        "video": {"id": video_id, "title": "", "width": 1080, "height": 1920, "fps": 30,
                  "durationSec": args.duration},
        "audio": {"voiceover": None, "music": None, "voiceVolume": 1, "musicVolume": 0.15},
        "scenes": [],
    })
    print(project.relative_to(ROOT))
    print("Created project scaffold. Next: write script.json, then run scripts/tts.py and scripts/audio_timing.py.")


if __name__ == "__main__":
    main()
