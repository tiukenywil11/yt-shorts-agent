# Storyboard: A Hole, 9 Fixes Later (Paper Prepper)

12 scenes, 71.61 s (voiceover 71.011 s + 0.6 s tail), 1080x1920 @ 30 fps. Timing source: `script.json` (exact mode). Each scene starts at its segment start and runs to the next segment start (the 0.25 s pauses are absorbed). Scene 12 merges seg-12 and seg-13.

Persistent cutaway: day background (`bg_cutaway_day`) for scenes 1-8, night (`bg_cutaway_night`) for 9-12. Every earlier part is redeclared in each later scene with `preset: none`. Problem first, then fix: red badge (pulse) and optional red specks, then fix part, `fix_check`, `FIX n/9` counter (staggered one at a time).

| # | Time | Beat | Dominant visual | Camera | Out |
|---|---|---|---|---|---|
| 1 | 0.00-3.56 | Hook | Plain hole at frame 0, Tuck (stand) + shovel | hold | cut |
| 2 | 3.56-8.65 | FIX 1/9 | Red specks fall into open hole; plank roof drops on | lean_in (0.06), lands on "roof" | cut |
| 3 | 8.65-13.77 | FIX 2/9 | Specks pass through thin roof; dirt mound; `3 FT` | hold | cut |
| 4 | 13.77-18.91 | FIX 3/9 | Roof + dirt sag with jolt; posts and beam drop in | lean_in (0.06), lands on "beams" | cut |
| 5 | 18.91-26.36 | FIX 4/9 | Tuck stuck outside; L-shaped entrance; `BAFFLE ENTRY` tag | hold | cut |
| 6 | 26.36-32.56 | FIX 5/9 | Stale-air badge/specks; crank fan, vent pipe to surface, teal arrows | rise (dy -0.05), lands on "vent pipe" | cut |
| 7 | 32.56-37.64 | FIX 6/9 | Empty shelf; 3 jugs hop on; `1 GAL/DAY` | hold | cut |
| 8 | 37.64-42.47 | FIX 7/9 | Tuck worry; lidded bucket toilet drops in corner | hold | time_skip (crossfade 0.4) |
| 9 | 42.47-47.30 | FIX 8/9 | Night background; 2 lanterns with mustard glow discs | hold | cut |
| 10 | 47.30-56.73 | FIX 9/9 | Silent "?" badge; crank radio on shelf; `STAY TUNED` tag | hold | cut |
| 11 | 56.73-65.27 | Twist | Surface specks thin out in 3 steps; `7 HRS ÷10`, `2 DAYS ÷100` | hold | cut |
| 12 | 65.27-71.61 | Payoff | Static full cutaway, night, Tuck cheers inside; READY stamp + confetti; end-card disclaimer | hold | (end) |

Camera moves: 3 of 12 scenes (2, 4, 6), each followed by `beat_cut`, each with the target noun as the last word.

## Conventions used
- Captions: one `Caption` per segment, `caption_paper` params, (0.47, 0.20), layer 90.
- Fix counter (0.20, 0.13) shows the previous count until the new one slaps in (scene 2 starts with none). Counter stays at 9/9 in scenes 11-12.
- Problem badge, fix_check at (0.76, 0.33); tags at (0.57, 0.335); stat callouts at (0.47, 0.30). Tuck stands on the ground line at (0.13, 0.40); finale Tuck on the shelter floor (0.385, 0.65).
- Cues are estimated by letter position inside each segment (word-level timestamps are FUTURE), each element entering ~0.1 s before its word.
- SFX: `problem_bonk` at each problem, `paper_rustle` at each fix, `stamp_thud` at READY. `musicVolume` set but `music` is null (no music file chosen yet).

## Approximations (FUTURE or missing features)
- Screen-space caption layer, dynamic shadows, tag shadow, stepped "on twos" motion: not used; baked shadows only.
- "Static pull-back" in the finale: the default framing already shows the whole cutaway, so the finale is a static full view (no zoom-out; the engine has no pull-back camera).
- L-shaped baffle entrance: no dedicated asset; built from two `hole_cutout` props (shaft + passage) plus `ladder`.
- "Plenty of bags" (seg-08) and "not candles" (seg-09): no registered bag/candle prop; not shown, carried by the narration and caption. Consider adding `trash_bags` and `candle` assets later.
- Stale-air badge reuses `problem_badge` with red specks; the "silent question badge" (seg-10) is a red circle Shape with a "?" KineticText.
- Disclaimer is a cream Shape plus KineticText instead of the `disclaimer_strip` PNG, so the wording can follow idea.md ("ready.gov").
- Stat callouts use `maxWidth` 0.74 and font sizes 120/100/88 (instead of the preset 120/0.6) so "1 GAL/DAY" and "2 DAYS ÷100" stay on one line.
- Prop positions and widths are estimates; asset aspect ratios are unknown. Tune on stills once the PNGs exist.

## Open issues
- The end-card disclaimer is only on screen for about 1.4 s (from 70.29 s). Consider extending `video.durationSec` by about 1.5 s with a final hold (the validator then warns the voiceover ends early).
- All 27 asset files are missing (see `asset-requirements.json`); the validator reports each as an error.
