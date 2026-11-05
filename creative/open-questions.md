# Open Questions and Uncertainties (GroundNUp reference set)

## Blockers / unmeasured
1. Audio content: voice type (human vs TTS, gender), music presence, SFX types, mix. Only loudness (all about -17 dB mean) and silence gaps were measured. A human listen or music/speech separation is needed. Affects our audio direction.
2. Exact caption styling: font, size, outline, per-word animation and safe zone. Only seen in 2.5 s samples. A short dense frame sample (e.g. every 2-3 frames over 2 s) is needed before cloning the caption timing in the DSL.
3. Camera cut/move count: scene detection (thresholds 0.3 and 0.08) misses smooth moves. A per-beat camera keyframe count would need manual labelling or optical-flow analysis.
4. Character faces and rigging detail not inspected at full-res.
5. Rendering engine unknown (looks game-engine-like). Not assumed.

## Performance interpretation
6. Are the Trojan (2 d) and hospital (3 d) actually underperforming? Their ages make views/day averages misleading. Re-pull view counts in about 14 days and compare against the others at equal age (early-velocity curve needs analytics data we do not have).
7. Does the missing "Congratulations" closer in the newest two matter, or is it a deliberate test (loop ending)? Check whether newer uploads keep dropping it, and whether the remaining 5 Shorts on the channel (13 total, 8 sampled) have it.
8. Is the Trojan ending cut mid-sentence on purpose (loop) or are the auto-captions truncated? Needs listening to the last 3 s.
9. Is the hospital "Every one subscriber carves their name..." line an ASR error or a subscriber-name gimmick? Frame 68105 s21 (about 50 s) shows a list of names on rock. Needs listening.
10. Why igloo (21.5M) and bunker (19.6M) outperform the 1.3-2.5M tier. Candidate factors (survival stakes, single hero, simple legible mechanic, universal subject, thumbnail/title/external traffic) cannot be separated with 8 samples. Do not treat any as established.
11. Thumbnails, Shorts feed placement, upload time, and title wording effects are not observable from the supplied files.

## Data caveats
12. Counts assumed scraped around 2026-11-06 (file mtime); true scrape time not recorded in the fields read.
13. Captions are auto-generated; numbers and names (e.g. "40 pigs", "3 ft") should be fact-checked before reuse.
14. Facts in the references (e.g. 1215 siege, Derinkuyu details) were not verified; our scripts need independent fact-checking.

## Decisions for our channel (not answered by the references)
15. Our own closing device to replace the "Congratulations" formula.
16. Our own hero, palette, backdrop, and brand marker (must differ from hi-vis worker, red-beanie figure, blue plaque, suburban backyard).
17. Whether our Remotion/Three.js engine can support cutaway-slab diorama, persistent world state, continuous camera paths and word-level captions: check `docs/technical/ANIMATION_DSL.md` and `engine/registry.json` before planning.
18. Target frame rate: references are 60 fps; the project default is 30 fps (Draft 15). Decide whether to follow the project default.

## Channel bootstrap
Decided in `creative/channel-identity.md`, `creative/style-bible.md`, `creative/animation-presets.json` and `creative/asset-registry.json`. Items 15, 16 and 18 above are answered: READY-stamp closer, Tuck host, warm 7-color palette, open-ground cutaway, and 30 fps per CLAUDE.md.

### Assumptions (confirm or override)
A1. The name is a working title. Options: **Paper Prepper** (working), Snug Doomsday, Plan B Burrow. Trademark, YouTube handle and domain checks have not been done.
A2. Audience: 18-40, US/English, everyday-preparedness-curious, not hardcore survivalists.
A3. Tone: practical, curious, reassuring, lightly witty, never fear-driven.
A4. Narration is TTS (based on `projects/tts-test`). The voice/provider is not chosen (`script.json` has `"voice": null`).
A5. Output is 1080x1920, 30 fps, H.264/AAC per CLAUDE.md.
A6. Water, air and plants share Dusty Teal `#5E8F86`, the only cool-leaning hue, capped at about 10% of the frame. The alternative is to drop it and show water as cream with teal-free wave lines.
A7. The red cross on `first_aid_kit` is allowed as the standard symbol, an exception to the "red = problem" rule.
A8. Loudness target of about -14 LUFS / -1 dBTP is an assumption. No loudness measurement script was found or verified.

### Engine findings that change the brief
- Supported: one-word captions work today via `Caption.wordsPerChunk: 1`. With 1 word per chunk the word is always "active", so `highlightColor` must equal `color`.
- Supported: static tilt via `transform.rotation`, and smooth rotation wobble via the `wiggle` loop (sine).
- NOT supported: stepped/held rotation.
- Caption timing is spread across the element by letter count. It is not real word timing, so sync is only as good as the per-sentence segments.
- Camera presets scale the whole scene layer, captions included, around frame center. They ease over the full scene and reset at the next scene.
- `scripts/validate_project.py` only accepts assets inside `projects/<id>/`. The repo-root `assets/` library in asset-registry.json must be copied per project for now.
- Each element shares one `params` object across its enter, loop and exit presets and its component params.

### Future capabilities (proposed; NOT in `engine/registry.json`; do not use in plans)
F1. `paper_grain` overlay: a full-frame texture multiply layer above the background. Workaround: bake the texture into the PNGs.
F2. `drop_shadow` element param `{dx, dy, color, opacity, blur}` for dynamic paper layering. Workaround: bake shadows into assets.
F3. `reveal_mask` / `dig_reveal` enter preset: a rectangular or torn-edge wipe that "digs" the cutaway open. Workaround: `slide_in_up` / `pop_in`.
F4. Stepped timing (`steps` / "on twos" param on presets) for a hand-animated paper feel, and a seeded stepped `paper_boil` loop (rotation/offset held for N frames).
F5. Persistent world state: elements that span scenes, or a `carryForward` scene flag. Workaround: redeclare earlier parts with preset `none` in every beat scene.
F6. Camera keyframes / persistent camera (`camera_to {x, y, zoom, atSec}`) so a move can land mid-scene on a target without resetting at the cut.
F7. Screen-space (camera-independent) layer for captions, fix counter and stamp.
F8. Word-level caption timing from TTS timestamps, plus per-word emphasis (`emphasizeWords`).
F9. Bundled custom font loading (a rounded heavy display font with a verified OFL license).
F10. Particle shapes (specks, drops, paper scraps) and per-particle palette arrays. Currently circles in one color only.
F11. Multi-part character rig (separate arms/head with pivots) and a walk cycle. Currently pose-swap PNGs only.
F12. Shared asset library resolution in the validator and renderer (repo-level `assets/`).
F13. Loudness measurement step (an FFmpeg `loudnorm`/ebur128 script) for the mix policy.

### Unresolved decisions
U1. Pick the final channel name, and check the handle and trademark.
U2. Choose the TTS voice and provider and confirm it can reach about 3.2 words/s naturally.
U3. Choose the music source and license.
U4. Who creates the assets (hand-made, vector tool, AI-assisted with review), and the shared paper texture source.
U5. Is the `FIX n/N` counter worth the screen space? A/B it on the first 2-3 uploads.
U6. Re-validate the topic slate with Google Trends / YouTube autocomplete before committing to topic #1 (evidence is low-medium).
U7. Is the title formula "A [Thing], [N] Fixes Later" distinct enough in search? Test against "[N] Problems Between You and a [Goal]".
