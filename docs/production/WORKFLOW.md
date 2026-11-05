# Production Workflow

## One-time channel setup
1. Collect a small representative reference set.
2. Analyze it once; save evidence and patterns.
3. Define an original style bible.
4. Build a registry of reusable characters, props, backgrounds, and presets.
5. Define the DSL and validate it.
6. Implement one vertical slice before expanding the engine.

## Per-Short workflow
1. Topic selection
2. Script
3. Storyboard
4. TTS generation
5. Reconcile storyboard timing against actual voice duration
6. Generate DSL JSON
7. Validate JSON and assets
8. Render low-resolution preview
9. Inspect contact sheet and selected motion clips
10. Fix only failed scenes
11. Render full-resolution MP4
12. Run FFprobe and playback/visual QA
13. Archive final files and QA report

## Suggested project contents
- `idea.md`
- `script.json`
- `storyboard.json`
- `animation.json`
- `voiceover.wav`
- `assets/`
- `previews/`
- `qa-report.md`
- `final.mp4`

## Render modes
- Stills: 2 PNGs per scene + contact sheet (cheapest visual review; use before any video)
- Draft: 360x640, 15 fps
- Preview: 540x960, 24 fps
- Final: 1080x1920, 30 fps

Use the same timeline in all modes. Lower quality settings should not change animation logic.

## Review gates
- Gate 1: approve story before animation.
- Gate 2: approve storyboard and voice timing before full render.
- Gate 3: approve preview before final render.
- Gate 4: validate final MP4 before publishing.
