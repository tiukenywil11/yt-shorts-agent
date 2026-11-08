# QA Report: 07-emergency-kit-payday-v2 (preview)

Scope: contact sheet (24 samples at 1.167 s) plus extra frames at 0.0, 10.8, 13.9, 14.0 and 26.9 s. Audio sync and loudness were not measured, only that the file decodes and has an AAC track.

## Technical
check_video --expect preview: PASS. 540x960, 24 fps, h264 yuv420p, aac, 27.80 s, full decode clean. No black frames or missing scenes seen in the sheet.

## Defects (objective)

| # | Sev | When | Description | Likely cause | Smallest fix | Fix via |
|---|-----|------|-------------|--------------|--------------|---------|
| 1 | major | ~14.0 s (scene "water is a choice") | Caption renders "SOOSKIP." with the words overlapping (an extra "O" and no gap). Snail is also drawn over the lower-left can, so the can looks merged with the snail. | Caption word timing: two words share the same window, or a word is cut and re-entered at a scene boundary. Snail position collides with the stack. | Fix caption chunk boundaries or timings at the scene seam. Move the snail right or lower in z-order of the cans. | DSL (caption timing and snail x), possibly engine if the caption splitter is at fault |
| 2 | minor (confirmed) | ~25.7 to 27.8 s (Try It Today scene) | The "Try It Today" note top edge sits about 3 px under the "FOLLOW LOCAL GUIDANCE" tag at 540 px width. They touch, with no safe gap. | Note y-position too high. | Move the note down about 40 px (or the tag up) so there are at least 16 px of clearance. | DSL |
| 3 | minor (confirmed) | ~10.5 to 11.7 s | Stage is nearly empty: a single blurred, half-faded can on the left, a lone "FOOD: BY ACCIDENT" tag, and a large empty upper area. It lasts about 1 s. This is a lull in the transition from chart to cans, not a blank or black frame. | Cans enter late relative to the narration "stock food". | Start the can enter 0.5 to 0.8 s earlier, or have the chart fade out while the cans fade in. | DSL |
| 4 | minor | 0.0 to 3.5 s | Caption "NEARLY EVERYONE" overlaps the FOOD and WATER axis labels at the ground line. At frame 0 the bar baselines and container heights differ (food 247 px, water 289 px), so the two bars do not share a baseline until about 3.5 s. | Caption zone overlaps the chart footer. Frame 0 is captured mid-animation. | Raise the chart about 40 px or lower the labels. Start the bars at their settled layout on frame 0. | DSL |
| 5 | minor | 19.8 s | Single small jug at lower left with a large empty stage while the "NEXT PAYDAY" tag appears. | Pacing and composition. | Optional: center the jug or show the plus-food element earlier. | DSL |
| 6 | minor (creative-adjacent) | 8.2 to 10.8 s | The bar chart repeats the same 96/53 data already shown at 0 to 4.7 s and on the card. About 2.6 s of repeated information. | Script structure. | Flagged only. This is a creative decision, so no change is proposed without approval. | n/a |

Checked and not defects: the "FOLLOW LOCAL GUIDANCE" tag appearing at 4.7 s rather than at frame 0 (an intentional disclaimer placement, not a rendering fault). Character and prop style were consistent across the sheet. The hand-drawn jug wobble reads as intended.

## Retention risk (prediction, not data)
Scorecard from STORY_AND_STORYBOARD.md:
- Hook 2/3: a surprising number pair in the first sentence, but not a question.
- Hold 2/3: visible state changes throughout, but the 4.7 s study card is static and the 8.2 to 10.8 s chart repeats the data.
- Share 1/2: a mild "check your kit" angle with no strong side to take.
- Look 1/1: the jug and cans read at feed size and change state.
- Packaging 1/1: the title "96% Had Food. Only 53% Had Water." pays off.
- Total: 7/10 (idea.md predicted 8; Hook and Hold are scored one half-point lower here).

Likely swipe points:
- about 4.7 s: the switch to a text card with a citation.
- about 8.2 to 10.8 s: the repeated chart, then the near-empty stage at about 10.8 s.
- about 19.8 s: the sparse "next payday" setup.

Frame 0 as a silent still: yes, largely. The 96% and 53% bars plus the "READY · EMERGENCY KIT" tag communicate the contrast without sound. The caption overlapping the axis labels and the unsettled bar baselines weaken the still slightly.

## Status after fixes (2026-11-08, preview re-render)
- Major (caption overlap and merged snail at about 14.0 s): fixed. It was a one-frame scene overlap, corrected in `src/Short.tsx`; the same frames were re-checked in the new preview.
- Fixed in DSL: Try It Today note clear of the guidance tag; chart raised clear of the caption; cans and jug enter earlier.
- Open minor: lone small jug around 19.8 s; repeated chart at 8.2-10.8 s (creative).
