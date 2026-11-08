# QA Report: 05-pay-yourself-first-v2 (preview)

Scope: output/preview.mp4 (31.34 s), contact sheet pass at 1.333 s steps, plus 4 extra frames (12.7, 12.9, 13.1, 13.25 s) for the suspected transition defect.

## Technical
`python scripts/check_video.py ... --expect preview`: PASS (540x960, 24 fps, h264 yuv420p, aac, 31.34 s, full decode clean). retention_lint PASS (reported). No black frames or missing scenes seen in the sheet.

## Defects (objective)

1. Minor - scene-05 to scene-06 transition, about 13.1-13.35 s (CONFIRMED, not a false alarm)
   - At 13.25 s the outgoing "Savings plan / Join plan" form is drawn over the incoming "The study" cite card. Both scenes' HUD chips stack: two "MONEY - THE DEFAULT" pills, a clipped "NOT FINANCIAL ADVICE" pill under "AFTER: ALREADY SIGNED UP". Two snails are visible. The cite card is partly hidden, and the headline numbers are unreadable for the frames of the overlap.
   - Cause: scene-05 `transitionOut` is `slide_up` at 0.25 s (animation.json, scene-05). Both scenes carry their own persistent chips and snail, and neither is masked or faded. This is the intended page turn, but it reads as a layout collision. Duration is brief (about 3-6 frames at 24 fps), so it does not block publishing.
   - Smallest fix (DSL): change scene-05 `transitionOut` to `cut`, as the other 10 boundaries do. Alternative: keep the slide but fade the outgoing chips and snail. Which one is a creative choice, so I have not changed it.
   - Fixable by: DSL (or engine if the shared chips must stay pinned across scenes).

2. Minor - 13.3 s onward, HUD chip stack
   - Chips "MONEY - THE DEFAULT" and "NOT FINANCIAL ADVICE" are pinned at the top for the rest of the video, plus a scene chip. At feed size that is up to three pills in the top safe zone. Legible, but crowded. (This is a design-level note, not a break.)
   - Fix: DSL, optional.

No critical or major defects. No character inconsistencies. The snail is the same in every appearance. No broken poses or merged objects. No cropping. Captions are readable and inside safe margins. Audio sync was not inspected sample by sample. Captions track the narration on the sheet.

## Subjective observations (not defects, no change made)
- Roughly the bottom 35% of the frame is empty tan ground, with captions sitting in it. The hero objects sit high.
- The snail is small and absent for 0-5 s.
- 13.3-16 s is a text-heavy cite card. 28-31 s is a static "TRY IT TODAY" card.

## Retention risk (prediction)
Scorecard (docs/creative/STORY_AND_STORYBOARD.md), my estimate:
- Hook 2/3: the 37% to 86% bar is a concrete surprise, but frame 0 does not pose a question.
- Hold 2/3: visible state change every 1.5-3 s through 0-13 s and 20-27 s. It dips at the cite and low-default stretch.
- Share 1.5/2: "default" framing gives viewers a personal takeaway but little reason to take a side.
- Look 1/1: the hero bar and jar change state and read at feed size.
- Packaging 1/1: the tension pays off.
- Total: 7.5/10 (the idea.md prediction of 8.5 is more optimistic).

Likely swipe points:
- 0-1.5 s: the caption starts with the fragment "37% OF".
- 13.3-16 s: cite card and the "in a ..." lecture beat. This is the highest risk, and the transition glitch from defect 1 sits just before it.
- 28-31 s: static outro card, which risks losing viewers before the loop or end.

Frame 0 as a still with sound off: yes. "Joined the savings plan, 37%, Before" shows the number and a baseline bar. It is a clear data hook, though it is more informative than curiosity-provoking.

## Status after fixes (2026-11-08, preview re-render)
- Minor (form and cite card overlap at about 13.3 s): fixed; scene-05 now cuts instead of sliding.
