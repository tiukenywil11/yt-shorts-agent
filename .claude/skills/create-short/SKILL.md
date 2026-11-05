---
name: create-short
description: Create a new animated YouTube Short from a topic through script, voiceover, storyboard, and validated Animation DSL JSON. Use for each new video before rendering.
model: sonnet
---

# Create Short

Inputs: topic or topic brief, target duration, channel style bible, and project ID. If the user gives a topic, do not block on optional preferences. Use `python` (not `python3`) on Windows.

1. Run `python scripts/new_short.py <id> [--duration N]` if `projects/<id>/` does not exist.
2. Read only the relevant channel style bible section and `docs/creative/STORY_AND_STORYBOARD.md`.
3. Fill `idea.md` (central idea, audience, hook, payoff).
4. Write `script.json`: `{"segments": [{"id": "seg-01", "text": "..."}], "targetDurationSec": N, "voice": null}`. **Gate 1:** show the user the narration text only and get approval.
5. Generate voiceover: `python scripts/tts.py projects/<id>` (local Piper/Kokoro). If the user supplies their own `voiceover.wav`, skip this.
6. Reconcile timing: `python scripts/audio_timing.py projects/<id>`. This writes real `startSec`/`durationSec` per segment into `script.json`.
7. Delegate to `storyboard-architect` (once) with: project dir, style bible path, target duration. It writes `storyboard.md`, `storyboard.json`, `animation.json`, `asset-requirements.json` and runs the validator. Do not write those files yourself first.
8. If the architect reports validation errors it could not fix, fix them and rerun `python scripts/validate_project.py projects/<id>`.

9. Assets: run `python scripts/gen_assets.py projects/<id>`. It generates every asset with a library drawer, copies same-id SVGs from other projects, and prints `NEEDS DRAWING` lines. If there are none, skip to step 10. Otherwise delegate to `asset-artist` (once) with the project dir and those lines; it adds drawers to `scripts/gen_assets.py`, re-runs the script, and previews the result. If an asset needs an engine component or preset that `engine/registry.json` lacks, flag it for `/build-animation` instead of drawing around it.
10. Rerun `python scripts/validate_project.py projects/<id>` after assets are drawn, since the script rewrites paths to `.svg` in `asset-requirements.json` and `animation.json`.

Do not render in this skill. Return paths, duration, scene count, assets drawn vs. still missing, and validation status. Keep JSON in files, not in chat.
