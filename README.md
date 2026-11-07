# Claude Animation Studio

A cost-conscious Claude Code workspace for producing animated YouTube Shorts with a declarative JSON plan and a reusable **2D Remotion engine** (included).

## Design goals

- Keep root `CLAUDE.md` short: it is always in context.
- Procedures live in Skills (loaded on invoke); specialist work runs in subagents with isolated context.
- Deep references live in `docs/`; agents read only what they need.
- Deterministic work is done by scripts (validation, timing, media checks, contact sheets, change detection), never by an LLM.
- Claude writes `animation.json` only. No per-video code.

## Requirements

- Claude Code
- Python 3.10+ (on Windows run `python`, not `python3`)
- Node.js 18+ and npm
- FFmpeg + FFprobe on PATH
- Free local TTS (pick one):
  - Piper (default, fastest): `pip install piper-tts`, then `python -m piper.download_voices en_US-lessac-medium --data-dir tools/tts`
  - Kokoro (higher quality): `pip install kokoro-onnx soundfile`, and put `kokoro-v1.0.onnx` + `voices-v1.0.bin` in `tools/tts/`

## Install

```bash
npm install
```

```bash
npm run typecheck
```

The first render downloads Remotion's Chrome Headless Shell (~130 MB, once).

## Typical production flow

1. `/bootstrap-channel` creates the channel's creative system (once).
2. `/analyze-references` analyzes supplied reference videos (once, or for a deliberate refresh).
3. `/create-short`: topic → script (Gate 1) → local TTS → timing → storyboard + `animation.json` → validation.
4. `/build-animation` (conditional): only when the plan needs a component or preset `engine/registry.json` lacks. Delegates to `animation-engineer`. Run it before rendering.
5. Assets: the end of `/create-short` runs `python scripts/gen_assets.py projects/<id>` (generates what it can, prints `NEEDS DRAWING` lines) and delegates those to the `asset-artist` agent, then revalidates. You can also run the script or agent by hand.
6. `/render-short`: stills (Gate 2) → draft/preview. Technical checks are automatic. Use it for iteration; fix issues and re-render only changed scenes.
7. `/review-short` is the single visual QA pass on the draft/preview (delegates to `qa-reviewer`, writes `qa-report.md`). Fix any critical/major issues, then re-render.
8. `/release-short projects/<id>` (after Gate 3 approval): renders the final once (refuses to overwrite an existing `final.mp4` unless you say so, e.g. `/release-short projects/<id> overwrite`; the old file is archived to `output/archive/` first), commits the scene manifest, then delegates to `publish-packager` to write `publish.md` (titles, description with citation and disclaimer, hashtags, captions, cover frame, upload checklist). It never uploads or posts; uploading stays manual.

`/setup-renderer` is manual-only: use it to repair or change the Remotion renderer integration, not in normal production.

Agent order: `reference-analyst` → `creative-director` (channel setup, once) → `storyboard-architect` → `animation-engineer` (if needed) → `asset-artist` → `qa-reviewer` → `publish-packager` (via `/release-short`).

## Commands

```bash
python scripts/new_short.py my-short --duration 45
```

```bash
python scripts/tts.py projects/my-short
```

```bash
python scripts/validate_project.py projects/my-short
```

```bash
npm run render:short -- --project projects/my-short --mode stills
```

```bash
npm run render:short -- --project projects/my-short --mode preview --scenes scene-03
```

```bash
npm run render:short -- --project projects/my-short --mode final
```

```bash
python scripts/gen_assets.py projects/my-short
```

```bash
python scripts/svg_preview.py projects/my-short
```

Other scripts: `gen_assets.py --list` (library drawers and assets drawn in other projects), `make_sfx.py` (sound effects), `audio_timing.py` (segment WAVs → exact timings), `scene_manifest.py` (which scenes changed, `--commit` after a good render), `check_video.py` (PASS/FAIL spec check), `make_contact_sheet.py` (timestamped sheet). Studio preview: set `SHORT_PROJECT=projects/<id>`, then `npm run studio -- --props=projects/<id>/cache/props.json`.

## Where things live

- `engine/registry.json`: the only list of allowed components, presets, cameras, transitions, and render modes.
- `src/`: the Remotion engine (single composition `Short`). Contract: `docs/technical/ENGINE_CONTRACT.md`.
- `scripts/gen_assets.py`: the shared SVG art library (palette, filters, one drawer per asset id). New art is added here by `asset-artist`, not hand-written into projects.
- `creative/`: style bible, asset registry, and animation presets for the channel.
- `templates/animation.example.json`: a complete, valid plan to copy from.
- `projects/<id>/`: one folder per video (plans, assets, voice, output).

## Cost-control rules

- Model tiers are set in frontmatter. Routine skills and the QA, storyboard, and reference agents run on Sonnet; creative-director, animation-engineer, and asset-artist inherit the main model. Run routine Shorts in a Sonnet session; switch to Opus only for engine or channel work.
- One Claude session per Short; `/clear` between Shorts.
- Review stills before rendering any video, render only changed scenes while iterating (`scene_manifest.py`), and render final once.
- Let scripts report PASS/FAIL; never paste raw ffprobe output, JSON plans, or individual frames into chat.
- Never reread all reference videos or load all docs for a single Short.
- For batch ideation, use headless `claude -p --model sonnet` instead of an interactive session.
