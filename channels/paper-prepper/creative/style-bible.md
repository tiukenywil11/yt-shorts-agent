# Style Bible: Paper Prepper (working title)

Source of truth for look, motion and pacing. Identity, formulas and guardrails: `creative/channel-identity.md`. Presets: `creative/animation-presets.json`. Assets: `creative/asset-registry.json`. Unsupported features: `creative/open-questions.md` > Channel bootstrap. Engine limits: `engine/registry.json`.
Coordinates are DSL units: `x` and `y` are fractions of frame width and height; sizes are fractions of width; px values are at 1080 wide.

## Identity
- Channel name: Paper Prepper (working; 3 options in channel-identity.md).
- Audience: US/English, 18-40, curious about everyday preparedness, not hardcore survivalists.
- Content promise: an ordinary thing becomes ready for a bad day through a chain of problems and fixes.
- Emotional tone: practical, curious, reassuring, lightly witty. Never fear-driven.
- Topics to cover: the slate in `creative/topic-research.md` (fallout shelter, blackout house, go-bag, pantry, water, root cellar, and so on).
- Topics to avoid: dated doomsday predictions, conspiracies, weapons/tactics, medical dosing, gore or casualties, mushroom clouds.

## Original art direction
- Style: flat 2D paper-cutout diorama. A single cross-section cutaway that grows piece by piece. No gradients on objects. No 3D.
- Shape language: chunky rounded rectangles, arcs and trapezoids with visible corner radii. Safe/fixed things are round-cornered. Problems are jagged triangles or zigzags in Signal Red. Each object is built from 3-6 flat pieces at most.
- Edge treatment: scissor-cut edges with a slight 1-2 px irregular wobble. No outlines. Torn edges with a 3-5 px Paper Cream fiber rim appear ONLY on the ground line and the top of each soil stratum.
- Palette (7; no other hues; tints only as baked shadow):

| Name | Hex | Role |
|---|---|---|
| Paper Cream | `#F4E6C8` | Day sky, caption fill, tags, highlights on cut edges |
| Cocoa Ink | `#3A2419` | Darkest value: caption stroke, text, eyes, night sky top, shadows (at opacity) |
| Umber Soil | `#7A4B2F` | Main soil stratum, wood, night sky bottom |
| Clay | `#B86B43` | Deep stratum, brick/structure, Tuck's body |
| Lamp Mustard | `#E9A93B` | Light sources, fixes, stat callouts, scarf, READY stamp |
| Dusty Teal | `#5E8F86` | "Flow and life": water, air arrows, plants. Max ~10% of the frame. |
| Signal Red | `#D2452B` | Problems ONLY: hazard specks, problem badges, leaks |

- Lighting: none simulated. Mood comes from background swaps. Night or underground = `bg_*_night` assets with a Cocoa Ink to Umber Soil sky, plus mustard "glow" paper discs behind lamps. Never use blue, gray or pure black (#000).
- Texture: one shared paper-fiber texture at 6-8% multiply, baked into every PNG and background. A dynamic grain overlay is FUTURE.
- Shadow/layering: hard paper drop shadows baked into assets. Direction is down-right 45°, color Cocoa Ink at 28% opacity, blur <=2 px. Offset by depth tier: back 4 px, mid 8 px, front 12 px. Dynamic shadows are FUTURE.
- Background detail: minimal. At most 3 background motifs (for example 2 cream clouds and 1 teal paper tuft). No houses, fences or suburban yards in the default cutaway.
- Composition (9:16 cutaway layout; y = fraction of height):

| Zone | y range | Use |
|---|---|---|
| Top UI margin | 0.00-0.10 | Nothing essential |
| Fix counter | ~0.13 (x 0.20) | `FIX n/N` tag |
| Caption | 0.20 (x 0.47) | One word at a time |
| Above ground | 0.26-0.44 | Surface parts, Tuck, weather |
| **Ground line** | **0.44** | Torn-edge band |
| Build zone | 0.44-0.74 | Underground structure; focal point ~(0.47, 0.55) |
| Bedrock | 0.74-1.00 | Decor strata only (sits under the YouTube UI) |

  Horizontal safe range: x 0.06-0.84. The right rail holds the Shorts buttons. Center the build at x 0.47.
  For non-dig topics (house, garage, backpack, car), keep the same zones. The "ground line" becomes the floor or the bag's opening seam.
- Visual hierarchy: the new part, then the problem badge, then the caption, then Tuck, then the existing build. Only one element enters at a time per beat.

## Character system
- Character IDs: `tuck` (sole host). Extras are FUTURE. Animals and props may appear for scale or humor.
- Silhouette: a pear-shaped Clay body, 1.3 heads tall. Pale Cream snout and belly patch, two Cocoa Ink dot eyes, no mouth. Mustard knit scarf with 2 tails, Cream headlamp strap with a Mustard lamp. Stubby paddle hands. Readable as a black silhouette at 0.14 width.
- Size: `width` 0.14-0.18. Tuck is never larger than the build's focal part.
- Poses (6 core plus 1 optional; pose-swap PNGs on an identical 1024x1024 canvas, feet at the bottom center): `stand`, `point`, `worry`, `idea`, `carry`, `cheer`, optional `dig`.
- Face/expression: eyes only, plus brow pieces in `worry` and `idea`. Emotion comes mainly from the pose. `worry` is mild (paw to cheek), never terror.
- Idle behavior: `host_idle` wiggle. Use `talking: true` only when Tuck "speaks" a line; the narrator is otherwise off-screen.
- Movement vocabulary: slide in from the side, pose swaps on problem/fix words, hop on cheer. He never walks across the frame continuously (no walk cycle, FUTURE).
- Allowed variations: props in hand. Seasonal scarf color is NOT allowed (always Mustard).
- Consistency: same canvas, baseline and scale for every pose. `flipX` to face the build. Tuck always stands on the ground line or a built floor, never floating.

## Environment and props
- Reusable environments: the `bg_*` entries in `creative/asset-registry.json` (cutaway day/night plus room sections).
- Reusable props: registry list. A new prop must use the palette, the same shadow tiers and <=6 pieces.
- Depth/layering (`transform.layer`): 0 background, 10 back-wall/strata details, 20 structure shell, 30 structure parts, 40 props, 50 Tuck, 60 FX particles, 70 term tags, 75 fix counter, 80 stat callouts, 90 caption, 95 READY stamp.
- Environmental motion: at most 2 looping ambient elements per beat (clouds `drift`, lamps `lamp_glow`). Weather is done with `ParticleBurst` in palette colors only.
- Resting tilt: props sit at a fixed `transform.rotation` from {-3, -2, -1, 1, 2, 3}°, which gives a hand-placed feel. Structure shells sit at 0°.

## Animation language
- Timing: snappy. Enters take 0.18-0.35 s, then hold. One new element per narrated noun. The element enters 0.1 s BEFORE its word is spoken.
- Easing: registry built-ins (ease-out cubic / back). A stepped "on twos" paper feel is FUTURE. Do not fake it with jitter.
- Anticipation: none on objects. Tuck's pose swap to `worry` leads the problem word by 0.2 s.
- Follow-through: pop overshoot only. 0.06-0.10 is the norm; 0.14 is the max (term tags).
- Secondary motion: `paper_flutter` on cloth, flags and flames only.
- Squash/stretch: none. Paper does not stretch. The engine's built-in talking squash on Tuck is the only exception.
- Motion intensity: low. The structure never loops. Max 3 moving elements on screen at once, excluding the caption.
- Problem beat: affected part `problem_jolt`, red badge `paper_slap` + `alert_pulse`, optional red-speck burst. Fix beat: new part `paper_drop`/`paper_rise`, badge `paper_pluck`, mustard check `paper_slap`.
- Preferred transitions: `beat_cut` between beats (the redeclared set makes the cut invisible); `time_skip` for day/night; `topic_turn` rarely.

## Camera
- Framing: the whole cutaway is visible by default. The build focal point sits near frame center because pushes scale around center.
- Angle: flat, front-on cross-section. Always.
- Movement: one camera preset per beat (scene). The camera eases across the entire scene, so write the named object as the LAST word of the beat's sentence. The camera then "lands" as the word is spoken. No more than half the beats move. The camera resets at each scene start, so put a move only on a beat followed by a `beat_cut`.
- Zoom: `cam_lean_in` (0.06) by default, `cam_land` (0.12) only for the finale or a target within 0.15 of center.
- Pans: `cam_sink`/`cam_rise`/`cam_slide`. Pans overscale by 1+2*|d|, so keep |d| <= 0.06.
- Shake: no camera shake. Use element `problem_jolt`.
- Safe areas: captions and tags sit inside the camera layer and scale with it. Keep them within x 0.10-0.84 and y 0.12-0.70. A screen-space caption layer is FUTURE.

## Typography
- Font family: registry default `Arial Black, Impact, sans-serif` for now. A bundled rounded heavy display font is FUTURE (open question).
- Caption style: `caption_paper` preset. Cream fill, Cocoa Ink stroke, uppercase, one word per chunk. highlightColor equals the fill because the active word is always highlighted at chunk size 1.
- Emphasis: term words appear in a separate `term_tag` (Cocoa Ink text on a Paper Cream tag, rotated -2°). Numbers appear as `stat_callout` (Mustard with an Ink stroke, unit included: "3 FT", "1 GAL/DAY").
- Position: caption at (0.47, 0.20); term tag next to its object, never overlapping the caption; fix counter at (0.20, 0.13).
- Animation: tags `paper_slap`, exit `paper_pluck`. The caption enters with no preset.
- Caption sync: the engine spreads words across the element by letter count, so use one Caption per sentence segment from script.json. Word-level TTS timestamps are FUTURE.

## Audio
- Narration: TTS. Warm, mid-pitch, conversational, smiling delivery, targeting 3.2 words/s (3.0-3.4). One idea per sentence. Pauses of 0.3 s or less except before the closer (0.5 s).
- Music: a light acoustic or lo-fi bed (plucks, soft percussion), royalty-free with a documented license. `musicVolume` 0.12-0.18. No dread drones or risers.
- SFX (paper Foley): rustle on `paper_drop`, snip on `paper_pluck`, soft thunk on `paper_hop`, low "bonk" on problem, stamp thud on READY. 0.4-0.7 volume. At most 1 SFX per 1.5 s.
- Loudness/mix policy: VO always on top (`voiceVolume` 1.0). Target about -14 LUFS integrated and -1 dBTP on the final. The measurement tool is not confirmed (open question).

## Story and pacing
- Target duration: 60-72 s. 195-235 words. 8-10 fixes.
- Hook: 0-3.0 s, one sentence (formula in channel-identity.md). The humble start is already on screen at frame 0. No title card, no logo.
- Setup: the first "But" lands by 3.5 s.
- Development: `But [problem]. So [fix].` Each fix causes the next problem. Show each problem visually before fixing it. 2-4 named terms per video. One `That's why...` tie-in at 30-45 s, and one counter-intuitive twist at 45-55 s.
- Payoff: a pull-back (static, whole build visible, night background if the topic suits) with all fixes in place.
- Ending: the closer formula, then the READY stamp in the last 2 s. End-card disclaimer for construction topics.
- Typical scene duration: 1 beat = 1 scene. Early beats 4-6 s, late beats 2.5-4 s.

## Constraints
- Must always: use the 7-color palette; keep one persistent cutaway per video (redeclare earlier parts in each scene with preset `place_static`); show the problem before the fix; cite primary sources in script notes; end reassuring; use only registry components, presets, cameras and transitions.
- Must never: copy reference wording or title template ("If you... you have...", "Congratulations, you have built...", "How a X Becomes a Y", "This is a [term]"); use human worker heroes, plaques or a backyard-with-house backdrop; show weapons, casualties or mushroom clouds; use blue/gray/black; invent engine features in plans.
- Flexible elements: topic environment, night vs day finale, Tuck's held prop, the term line variant, the number of fixes (8-10).

## Preset registry
See `creative/animation-presets.json`. Every channel preset maps to a real `engine/registry.json` preset, camera or transition. It is not duplicated here.
