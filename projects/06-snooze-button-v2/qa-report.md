# QA Report: 06-snooze-button-v2 (preview)

Scope: one contact-sheet pass of `output/preview-contact-sheet.jpg`, plus three extra frames (5.75, 6.1, 6.45 s) for the suspected blank stage, plus volumedetect and blackdetect on `output/preview.mp4`. Audio was not listened to, so narration intelligibility and voice/visual sync are inferred from the caption timing only.

## Technical (script result, trusted)
`check_video.py --expect preview`: PASS. 540x960, 24 fps, h264 yuv420p, aac, 26.48 s, full decode clean. Extra checks: no black frames (blackdetect, d=0.1, 0 hits). Audio max -3.5 dB, mean -17.5 dB, so no clipping.

## Defects (objective)

1. Minor, scene-04 (5.6 to ~5.7 s): near-blank stage. Not a real defect, but a small polish item.
   - Frames 5.625 and 5.75 show the stage holds only the chip and the caption "IN 31". The first dots are already popping in by 5.75 s and the grid is half built by 6.1 s.
   - So the empty beat is about 0.1 to 0.2 s, not a dead second.
   - Likely cause: the cut from scene-03 removes the clock and ruler, and the dot stagger starts a few frames after the scene start.
   - Fix: start the first dot on the scene's first frame (or hold the ruler for 3 frames). DSL change only: dot stagger offset in scene-04.
   - It also reads as the intended "filling in" beat, so leaving it is acceptable.

2. Minor, scene-02 (2.25 to 3.4 s) and the cite card (14.6 to 16.9 s): small text at feed size.
   - "30 MIN SNOOZING" and "~6 MIN OF SLEEP" labels, and the card line "31 snoozers, one lab study", are very small at 540x960.
   - The card limit is required by the source note, so only the size is a concern.
   - Fix: raise the font size by about 25 percent. DSL change.

3. Minor, scenes 06 to 12 (about 9 to 26 s): the hero clock is small and the lower ~35 percent of the frame is empty kraft floor.
   - Captions sit in the upper floor band. The bottom strip is unused, though it likely overlaps the Shorts UI, so it may be intentional.
   - Mid-video stretches (16.9 to 20 s) show a large empty area with only a headline and a small clock.
   - Fix: scale the clock up or add one state change. DSL change, and a creative call.

4. Minor, `storyboard.json` notes: the text contains mojibake ("BODY Â· HABIT MYTHS"). It does not appear on screen (the chip renders correctly). Fix: re-save the file as UTF-8. Tooling or DSL change.

No defects found in these checks: character consistency (the clock goes coral, then sky, then coral, then mint as designed, and the snail is consistent), broken poses, merged objects, cropping, caption safe margins, transitions (hard cuts, no flashes or blanks), or missing scenes. Audio sync was not verified by ear.

Not defects (creative preference, left as is): hard cuts only, the empty lower third, and the 7.4 s gap before the snail appears.

## Retention risk (prediction, not data)

Scorecard from `docs/creative/STORY_AND_STORYBOARD.md`:
- Hook: 2/3. Frame 0 shows a number contrast (30 vs 6), but it asserts a result instead of opening a question.
- Hold: 2/3. There is a visible change every 1 to 2 s through 12 s. The study-citation and advice stretch (about 14 to 21 s) is mostly static text.
- Share: 2/2. It has a myth-versus-science side to take.
- Look: 0.5/1. The clock reads at frame 0 and changes state, but it shrinks to roughly a third of its size from 2.25 s on.
- Packaging: 1/1. The title creates tension and the "SAME OR BETTER" payoff delivers it.
- **Total: 7.5/10.** The idea.md prediction was 8.5, so the delta is about 1 point (Hook, Hold and Look each scored lower here).

Likely swipe points:
- 2.2 to 3.4 s: the clock shrinks and the screen becomes bars and labels.
- 5.6 to 5.8 s: the brief blank beat.
- 14.6 to 17 s: the citation card, the text-heavy stretch.
- 17 to 21 s: advice delivered with minimal visuals.

Frame 0 as a still with the sound off: yes. "30 MIN SNOOZE ~6 MIN OF SLEEP" over a ringing clock is understandable, but it states a conclusion where a question would hook harder.

## Status after fixes (2026-11-08, preview re-render)
- Fixed in DSL: bar labels and cite-card limit line enlarged.
- Open minor: small hero clock in scenes 06-12; `storyboard.json` notes have a text-encoding artifact that does not appear on screen.
