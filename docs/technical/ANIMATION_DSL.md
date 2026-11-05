# Animation DSL v1

## Purpose
The model describes WHAT appears and happens. The renderer determines HOW it is implemented.

## Hard constraints
- JSON only for machine-readable plans.
- No executable JavaScript, functions, eval, or arbitrary code in plans.
- Every component and preset must exist in the engine registry.
- Use seconds in authoring files; convert to frames in the renderer.
- Use stable IDs for caching and change detection.
- Keep coordinates normalized (0–1) unless a component explicitly requires pixels/world units.
- Unknown fields should fail validation or be explicitly versioned.

## Minimal example

```json
{
  "schemaVersion": "1.0",
  "video": {
    "id": "sample-short",
    "title": "A sample story",
    "width": 1080,
    "height": 1920,
    "fps": 30,
    "durationSec": 12
  },
  "audio": {
    "voiceover": "voiceover.wav",
    "music": null
  },
  "scenes": [
    {
      "id": "scene-01",
      "startSec": 0,
      "durationSec": 4,
      "background": { "type": "solid", "color": "#F6EBDD" },
      "camera": { "preset": "static", "params": {} },
      "elements": [
        {
          "id": "headline-01",
          "type": "text",
          "asset": null,
          "component": "KineticText",
          "startSec": 0.2,
          "durationSec": 2.5,
          "transform": {
            "x": 0.5,
            "y": 0.32,
            "scale": 1,
            "rotation": 0,
            "opacity": 1,
            "layer": 10
          },
          "content": "ONE SMALL CHANGE",
          "preset": "pop_in",
          "params": { "overshoot": 0.08 }
        }
      ],
      "sfx": [],
      "transitionOut": { "preset": "cut", "durationSec": 0 }
    }
  ]
}
```

## Allowed values: `engine/registry.json`
That file is the only list of components, presets, cameras, transitions, backgrounds and their params with defaults. Don't copy it here; read it.

Summary (v1.0.0):
- Components (`type` → `component`): text → `KineticText`, `Caption`; shape → `Shape`; prop → `Prop`; character → `Character`; particle → `ParticleBurst`.
- Element motion fields: `preset` (enter: fade_in, pop_in, slide_in_left/right/up, bounce, shake, none), `loop` (pulse, float_loop, wiggle), `exit` (fade_out, pop_out).
- `params` holds component params plus the params of the chosen presets, e.g. `{"width": 0.4, "overshoot": 0.1}`. Unknown keys fail validation.
- Camera: static, camera_push {amount}, camera_pan {dx, dy}. Transitions: cut, crossfade, slide_up.
- Background: `{"type": "solid", "color"}`, `{"type": "gradient", "from", "to", "angle"}`, `{"type": "image", "asset"}`.
- Optional: `audio.voiceVolume`/`musicVolume` (0–1); scene `sfx: [{asset, atSec, volume}]`; Character `params.poses: [{atSec, asset}]`.
- Captions: one `Caption` element per script segment, with `content` = segment text and timing = the segment's `startSec`/`durationSec` relative to the scene.
- A full working example is in `templates/animation.example.json`.

## Validation
`python scripts/validate_project.py projects/<id>` checks all of the following:
- schema version is supported
- video dimensions/fps/duration are valid
- scene IDs and element IDs are unique
- scenes do not unintentionally overlap or leave gaps
- element intervals fit within their scene
- referenced assets exist
- components and presets are registered
- all values are finite
- opacity is 0–1
- normalized x/y are 0–1
- narration and audio references exist

## Renderer contract
Renderer receives a validated plan plus an asset registry. It must be deterministic for a given input, engine version, and render configuration.
