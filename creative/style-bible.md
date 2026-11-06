# Style Bible: Small Change Lab

Source of truth for look, motion, pacing and on-screen guardrails. Identity, mascot, series: `creative/channel-identity.md`. Presets and component styles: `creative/animation-presets.json`. Assets: `creative/asset-registry.json`. Future capabilities: `creative/open-questions.md` > Bootstrap. Engine limits: `engine/registry.json`.
Coordinates are DSL units: `x`/`y` are fractions of frame width/height; sizes are fractions of width; px are at 1080 wide.

## Identity
- Channel name: Small Change Lab (locked 2026-11-06).
- Audience: English 18-35, early-career/students, skeptical of hype.
- Content promise: one small habit, one cited fact, one thing to try today.
- Emotional tone: calm, curious, precise, lightly warm. Never shaming, never hype.
- Topics to cover: Money ~35%, Mind ~25%, Body ~20%, Ready ~20%. Slate: `creative/topic-research.md`.
- Topics to avoid: stock/crypto picks, income promises, "get rich", supplements, dosing, diagnosis, weight-loss claims, trait lists that flatter the viewer, dated disaster fear.

## Original art direction
- Style: flat 2D paper cutout on one full-bleed tinted paper field. A small "desk-top stage": one floor line, Inch, and 1-3 props. No 3D, no gradients on objects, no panels-within-the-frame.
- Shape language: rounded rectangles and circles = calm/done; a jagged edge appears only on problem/cross items. Each prop has at most 6 flat pieces.
- Edges: clean scissor-cut with a slight 1-2 px wobble. No outlines, except an Ink 4 px stroke on text cards and the cite card.
- Palette (7 core + 4 tints; no other hues):

| Name | Hex | Role |
|---|---|---|
| Paper | `#F5EEDD` | Card fill, caption fill, eye-whites, highlights |
| Ink | `#26303F` | Text, strokes, pupils, baked shadows (at 20%), night background |
| Kraft | `#C9A77C` | Inch's body, tables, floors, neutral props |
| Sun Yellow | `#F2B632` | Inch's shell, stat numbers, step slates, TRY IT TODAY note, caption highlight |
| Mint | `#3FA37A` | DO / fix / gains: check badge, upward bars, coins saved |
| Coral | `#E2553F` | DON'T / problem / losses: cross badge, MYTH stamp, leaks. Never decorative |
| Sky | `#7FB3D5` | Calm/flow: water, sleep, focus, night accents. Max ~15% of the frame |
| Money tint | `#E3F1E7` | Money background |
| Mind tint | `#E2ECF5` | Mind background |
| Body tint | `#FBE6D6` | Body background |
| Ready tint | `#EFE2C9` | Ready background (matches Paper Prepper props) |

- Colour-blind rule: Mint vs Coral is never the only signal. Mint always has a check mark or up arrow; Coral always has a cross, jagged edge or down arrow.
- Lighting: none simulated. Night/sleep beats use a `solid` Ink background with Sky/Sun accents.
- Texture: none in the engine. Optional baked flat speck pattern in background SVGs. Do not use SVG filters (`feTurbulence`, blur): renderer support is unverified.
- Shadows: baked into each SVG as a flat Ink 20% copy offset down-right: back 4 px, mid 8 px, front 12 px. No blur.
- Background detail: tint field + floor strip only (`solid` background + `floor_strip` prop). Image backgrounds only when the setting matters (bedroom, kitchen, desk, cutaway). Max 3 decor motifs.
- Visual hierarchy per beat: new element, then the badge/number, then the caption, then Inch. One new element enters per narrated noun.

### Layout and Shorts safe zones (y = fraction of height)
| Zone | Range | Use |
|---|---|---|
| Top UI | y 0.00-0.08 | Nothing |
| Pillar chip + title | y 0.09-0.13, x 0.06-0.70 | Persistent all video: dot + "MONEY · 24-HOUR RULE" |
| Disclaimer tag | y ~0.16, x 0.06-0.46 | Money/Body/Ready, from the cite card to the end |
| Stage | y 0.19-0.64 | Props, Inch, slates, cite card. Focal point (0.46, 0.42) |
| Floor line | y 0.64 | Inch's feet and props sit here (moved from 0.60 on 2026-11-06 after the first stills left the lower frame empty) |
| Caption | y 0.70 (band 0.66-0.74) | Narration captions |
| Bottom UI | y 0.74-1.00 | Floor colour/decor only (title, channel and music UI cover it) |
| Right rail | x > 0.84, y 0.40-0.90 | Nothing essential |

Horizontal safe range x 0.06-0.84; centre content at x 0.46.

## Character system
- Character IDs: `inch` (sole recurring character). Generic one-off figures are FUTURE; do not add humans.
- Proportions: snail 1.6:1 wide; shell = 55% of the height. 1024x1024 canvas, foot baseline at the bottom centre, identical scale on every pose.
- Size: `width` 0.29 default, 0.34 for close acting beats, 0.21 when it shares a beat with the cite card or a slate. Props scale to match (desk props about 0.26-0.29, phone 0.14). A four-item desk row fills x 0.05-0.87; slight overlaps in depth are fine.
- Poses: core `neutral`, `point`, `worry`, `idea`, `cheer`, `shell_hide`; optional `tired`, `skeptical`, `carry`, `sleep`. Swap via `params.poses [{atSec, asset}]`.
- Face: eyes on stalks + mouth line. Stalk angle carries emotion (up = energy, droop = tired, one high = skeptical). Worry is mild. No tears, no anger.
- Idle: `inch_idle` loop. `talking: false` always; Inch never narrates.
- Movement: slide in from the side, pose swap on the problem/fix word (leads the word by 0.2 s), `hop` on cheer. No walk cycle (FUTURE).
- Consistency: feet on the floor line (y 0.64) or on a prop top; never floating. `flipX` to face the focal prop. Colours never change by season or pillar.

## Environment and props
- Environments: pillar-tint `solid` background + `floor_strip`; image backgrounds per `creative/asset-registry.json`. Ready may use the Paper Prepper cutaways.
- Props: registry list, Money first. A new prop must use the palette, baked shadow tiers and <=6 pieces. No logos, brand names, real banknotes or real app UIs; money is generic coins, a "$" note and plain cards.
- Do vs don't iconography: `cross_coral` badge on the wrong way (top-right of the prop), then `check_mint` on the fix. Up/down arrows in Mint/Coral for numbers. Never show both badges on one prop at once.
- Layers: 0 bg, 5 floor strip, 20 big props, 40 small props, 50 Inch, 60 particles, 70 badges, 72-74 slates/stamps, 80 cite card, 82 stat callouts, 86 pillar chip, 87 disclaimer, 90 caption, 95 TRY IT TODAY note.
- Ambient motion: at most 2 loops per beat (`coin_bob`, `soft_pulse`). Resting tilt for props from {-3,-2,-1,1,2,3} deg; cards -2 deg; slates 0.

## Animation language
- Timing: snappy. Enters 0.18-0.35 s, then hold. An element enters 0.1 s before its word.
- Easing: registry built-ins only. Stepped "on twos" timing is FUTURE.
- Follow-through: pop overshoot 0.06-0.10; 0.14 max (tags, stamps, badges).
- Squash/stretch: none (paper). Secondary motion: `paper_flutter` on paper notes/receipts only.
- Motion intensity: low. Max 3 moving elements at once, excluding the caption.
- Problem beat: prop `nope_jolt`, `cross_coral` `tag_slap` + `alert_pulse`, Inch `worry`/`shell_hide`, optional coral specks. Fix beat: new prop `snip_in`, cross `snip_out`, `check_mint` `tag_slap`, Inch `idea`/`cheer`.
- Transitions: `beat_cut` by default; `time_skip` (crossfade) for time jumps (day 1 to day 30, night to morning); `page_turn` (slide_up) only into the cite card. No fades to black.

## Camera
- Framing: full stage visible; focal near centre (pushes scale around frame centre).
- Angle: flat front-on. Always.
- Movement: `cam_hold` on at least 60% of beats. One preset per scene; it eases over the whole scene and resets at the next scene, so put the named object as the last word of that beat's sentence.
- Zoom: `cam_lean_in` (0.05) by default; `cam_land` (0.10) at most once per video. Keep pushes small: the chip, disclaimer and caption scale with the camera (no screen-space layer; FUTURE F1).
- Pans: |d| <= 0.04. Shake: never on camera; use `nope_jolt` on the element.
- Safe areas: with any camera move, keep text inside x 0.10-0.82, y 0.10-0.70.

## Typography
- Font: registry default `Arial Black, Impact, sans-serif` (bundled rounded font is FUTURE).
- Minimum size 40 px at 1080w for any text (reads at 360 px drafts). Cite source line 44 px, limit line 40 px, stat 120-160 px, step numeral 220 px.
- Caption style `caption_main`: Paper fill, Ink stroke 10, Sun Yellow active-word highlight, 2 words per chunk, uppercase, 84 px at (0.46, 0.70). One Caption per script segment (timing spreads by letter count; word timing is FUTURE).
- Emphasis: numbers go in `stat_callout` (Sun Yellow, Ink stroke, unit included: "$5/DAY", "24 HRS"). Terms go on a Paper tag. Never more than one emphasis element per beat.
- Numbers in captions are written as digits ("24 hours", "$1,200").

## Citation card (required: one per Short)
- Build: `cite_card` SVG (Paper index card, Ink 4 px border, Sun Yellow tab, baked shadow) at (0.46, 0.38), width 0.76, rotation -2, layer 80. Text on top:
  1. Tab: `THE STUDY` (peer-reviewed) or `THE DATA` (government/agency stats). 40 px Ink.
  2. Source line: `[Author] et al., [Year]` or `[Agency], [Report], [Year]`. 44 px Ink.
  3. Finding: one number or one short clause. 96-120 px Ink, or Sun Yellow with stroke for a number.
  4. Limit line, Coral dot + 40 px Ink: one of `n = [N]`, `self-reported`, `correlation, not cause`, `one study`, `averages vary`, `illustrative math`.
- Timing: enters with `page_turn` (or `snip_in`) after the problem; hold **2.5-3.5 s**; narration says the finding in plain words and names the source ("A 2010 study of 96 people found...", with real values from idea.md). Never read the whole card aloud.
- Full citation (title, link/DOI) goes in the description and in `projects/<id>/idea.md`. No card = no publish.
- 30-Day Log uses a `MY NUMBERS` tab and the limit line "one person, not a study".

## Audio
- Narration: **locked 2026-11-06: Kokoro TTS `af_heart`, speed 1.10** (`"voice": {"engine": "kokoro", "voice": "af_heart", "speed": 1.1}` in `script.json`). Use it in every video, with no per-video voice changes. Reasons and auditions: `creative/voice-research.md`. If a script measures outside the target, adjust speed between 1.05 and 1.15. Target **3.0 words/s** (2.8-3.2). One idea per sentence. Pauses <=0.3 s, except 0.4 s before "Try it today".
- Music: soft lo-fi/acoustic bed, royalty-free with a documented license, `musicVolume` 0.10-0.15. No risers, no dread drones.
- SFX (paper Foley, 0.4-0.7 volume, max 1 per 1.5 s): rustle on `snip_in`, bonk on cross, pencil tick on check, coin clink on coin props, page flip on the cite card, stamp thud on the TRY IT TODAY note. Reuse the PP rustle/bonk/thud wavs.
- Mix: VO on top (`voiceVolume` 1.0). Target about -14 LUFS / -1 dBTP (measurement tool unconfirmed).

## Story and pacing
- Target duration: **35-45 s** (hard cap 50 s). **105-135 words** (cap 150). 7 Fixes Later may run to 50 s.
- Scene cadence: 1 beat = 1 scene; 11-15 scenes; a new visual every **2.5-4 s**; nothing static over 4.5 s except the cite card (3.5 s max).
- Beat map (about 40 s): Hook 0-2.5 s; Problem/cost 2.5-9 s; Cite card 9-16 s; Fix steps 16-32 s (1-3 numeral slates, or 7 for 7 Fixes Later); Caveat 32-35 s; Try it today 35-40 s; loop frame in the last 0.5 s.
- Hook rules: speech on frame 0. Sentence 1 is 12 words or fewer and states a number, cost or concrete outcome ("Waiting 24 hours can kill most impulse buys" style, only if the source supports it). The problem is visible at frame 0 (Inch + prop in the problem state, chip on screen). No title card, logo or blank frame. Alternate outcome+number hooks with myth/curiosity hooks across batch 1 and log the hook type in idea.md.
- Development: show the problem before the fix; Coral cross, then Mint check. The fix is a concrete behaviour (when, where, how long), not a mindset.
- Caveat (required): one sentence on who or when this doesn't apply ("If your income is irregular, start with a smaller amount." style).
- Ending: "Try it today: [one action, 12 words or fewer, under 5 minutes]." TRY IT TODAY note `tag_slap` + stamp thud + `check_mint`. No "follow/subscribe" voice line (CTA lives in the pinned comment).
- Loop: the final 0.5 s cuts back to the frame-0 layout (same background, Inch in the same spot and pose as the hook, prop now in the fixed state). The last line must not be a sign-off; it can lead into the first line. No fade-out, no end card, no black.

## Guardrail language (on screen and spoken)
- Disclaimer tags (Paper tag, Ink 40 px, layer 87, from the cite card to the end): Money `NOT FINANCIAL ADVICE`; Body `NOT MEDICAL ADVICE`; Ready `FOLLOW LOCAL GUIDANCE`. Also in the description, the pinned comment and the About page. Affiliate links are disclosed in every description.
- Say: "one study found", "linked with", "on average", "for many people", "in this example", "assuming [X]%".
- Never say: "proven", "science says", "studies show", "experts say", "the secret", "hack", "guaranteed", "never again", "cures", "boosts metabolism", "get rich", "you should buy/invest in [X]".
- Money: illustrative maths only, with the assumed rate on screen ("assumes 5%/yr, illustrative"). No tickers, products, returns promised, or debt/tax advice for a specific situation.
- Body: no dosing, supplements, diagnosis or weight claims. Add "If you have a condition, ask a clinician" when the habit touches health.

## What we do NOT borrow from references
- Improvement Pill: thin-line sketch figures; the heavy hand-drawn title banner across the top; the square illustration panel on a colour field with empty space below; per-beat rainbow panel colours; the dark semi-transparent caption bar; the "Tip #1" lettering; "the secret / you haven't heard of" framing; rat-race or "slave" metaphors; absolute outcomes.
- Psych2Go: the sprout-headed mascot or any plant-headed/blank-bodied figure; kawaii and painterly sets; book-page/card overlays; green karaoke highlight; "signs you are..." flattering trait lists; reflective-question endings without an action.
- Both: scripts, titles, scene compositions, "studies show" attributions, unsourced health claims, 56-100 s runtimes.
- Paper Prepper: Tuck, the READY stamp, the `FIX n/N` "every fix causes the next problem" chain, the cocoa palette as our primary.
- What we keep (general techniques only): promise/number in sentence 1; a persistent topic label; numbered step slates; do/don't badges; slate beats alternating with acting beats; one recurring original character; a caveat line.

## Constraints
- Must always: palette only; one cite card with a limit line; problem before fix; a caveat line; try-it-today + loop frame; disclaimer tag per pillar; registry-only components/presets; sources in idea.md.
- Must never: copy reference looks or wording; logos/brands/real UIs; humans; Coral as decoration; absolute or medical/financial promises; the same script with swapped nouns.
- Flexible: background image vs solid tint, number of steps (1-3, or 7), Inch's held prop, hook type, night palette for sleep topics.

## Preset registry
See `creative/animation-presets.json`. Every alias maps to a real `engine/registry.json` name. Not duplicated here.
