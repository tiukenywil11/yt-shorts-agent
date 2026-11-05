---
name: render-short
description: Validate a Short project, render stills/draft/preview/final MP4 with the repository's Remotion renderer, and run scripted technical checks. Use after the Animation DSL and required assets are ready.
model: sonnet
---

# Render Short

Command (the only render entry point; see `docs/technical/ENGINE_CONTRACT.md`):
`npm run render:short -- --project projects/<id> --mode stills|draft|preview|final [--scenes scene-01,scene-03]`

The adapter validates first, renders into `projects/<id>/output/`, and runs `scripts/check_video.py` automatically. Read its PASS/FAIL lines; do not re-probe manually.

1. `python scripts/scene_manifest.py projects/<id>` → lists changed scene IDs since the last render.
2. First render of a project: `--mode stills` → `output/stills-contact-sheet.jpg`. **Gate 2:** user approves stills before any video.
3. `--mode draft` (or `preview`). For iteration, pass `--scenes <changed ids>` to render only those scenes as clips.
4. `python scripts/make_contact_sheet.py projects/<id>/output/<file>.mp4` for the review gate. Visual QA is done by `/review-short`, not here.
5. **Gate 3:** after preview approval, render `--mode final` once. Never overwrite an existing `output/final.mp4` without explicit instruction (the adapter refuses unless `--overwrite`).
6. `python scripts/scene_manifest.py projects/<id> --commit` after a successful render.

Cache rules: never trust filenames as cache keys; music-only changes need only a final rerender; one scene's change → rerender only that scene during iteration.

If a render fails, report the adapter's error (it names the scene/element). Never claim success unless the command exited 0 and the output file exists.
