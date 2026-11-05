# Animation Engine Contract (as implemented)

## Facts
- Framework: Remotion 4.0.541, React 19.2, 2D only (HTML/SVG/CSS, CPU rendering). No Three.js.
- Entry point: `src/index.ts` → `src/Root.tsx`
- Composition ID: `Short` (the only one)
- Props: `{ plan: AnimationPlan, mode: "draft" | "preview" | "final" | "stills" }` (types in `src/types.ts`)
- Metadata: `calculateMetadata` takes width/height/fps from `engine/registry.json` → `modes[mode]`, and duration = `plan.video.durationSec × fps`.
- Assets: the project folder is the Remotion `publicDir`. Every asset path in a plan is project-relative (`assets/x.png`, `voiceover.wav`).
- Registry (single source of truth): `engine/registry.json`. It's read by `src/engine/registry.ts` (defaults) and `scripts/validate_project.py` (allowed values and types).

## Command
```
npm run render:short -- --project projects/<id> --mode stills|draft|preview|final [--scenes a,b] [--overwrite] [--concurrency N]
```
| Mode | Output | Size / fps | Measured (9s plan, this PC) |
|---|---|---|---|
| stills | `output/stills/*.png` + `output/stills-contact-sheet.jpg` (2 per scene) | 540x960 | ~6s for 6 stills |
| draft | `output/draft.mp4` | 360x640 @15 | ~6s |
| preview | `output/preview.mp4` | 540x960 @24 | (between draft and final) |
| final | `output/final.mp4` (refuses to overwrite without `--overwrite`) | 1080x1920 @30, H.264 yuv420p BT.709 + AAC | ~12s |
| `--scenes` | `output/<scene-id>-<mode>.mp4` (scene + its transition tail) | per mode | ~4s per scene (preview) |

Bundling adds about 3–5s per run (about 20s the first time). The adapter runs `validate_project.py` before rendering and `check_video.py` after.

## Timeline semantics
- Scenes are back-to-back at exact `startSec`, so narration sync never drifts.
- A non-cut `transitionOut` (crossfade, slide_up) holds the outgoing scene's last frame for `durationSec` while the next scene enters on top during its first `durationSec`.
- Elements use local scene time. `preset` (enter) runs from element start, `loop` runs throughout, and `exit` finishes at element end.
- Motion offsets are fractions of video width; `fontSize`/`strokeWidth` are px at 1080 wide. Output looks identical in every mode.
- Randomness only comes through Remotion `random(seed)` (ParticleBurst `seed` param). Re-rendering the same plan was verified byte-identical.

## Adding a capability (build-animation)
1. Add the entry to `engine/registry.json` (type, params, defaults).
2. Implement it in `src/components/` (and add it to `COMPONENTS` in `src/components/index.ts`), or as a preset in `src/engine/presets.ts`.
3. `npm run typecheck`, then `--mode stills` on a project that uses it.
Never hardcode one video's scene into the engine.

## Not supported (by design, to keep it cheap)
3D/WebGL, network fonts (use system fonts or a local font asset), per-word audio alignment (captions are timed by text weight within the segment window).
