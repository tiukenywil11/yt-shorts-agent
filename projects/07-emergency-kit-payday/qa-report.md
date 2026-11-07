# QA Report: 07-emergency-kit-payday (draft, re-review)

Inspected: output/draft.mp4, contact sheet (28 stills), full-res stills for scenes 4, 9, 11, script.json, animation.json (font sizes). Stills are 540x960, so "px at 1080" means 2x the still measurement.

## Technical
- `check_video.py --expect draft`: PASS (360x640, 15 fps, h264/yuv420p, aac, 40.53 s, clean decode).
- Ending rule met: the video is 40.53 s and the VO is 40.46 s, so it ends about 0.07 s after the VO. Scene 14 is last and there is no trailing silent scene.
- blackdetect: 0 black frames. Mix peak -3.4 dB, mean -17.5 dB, no clipping. Music is null. SFX-versus-VO masking cannot be checked from the mix and needs a listen.

## Resolved since last review
- Major 1 (survey year): VO now says "A 2014 survey of 572 adults", and the cite card limit line reads "self-reported 2014, n = 572". Resolved.
- Major 2 (hook breadth): VO now says "In one survey, only 53% of households stored three days of water." Resolved.
- Scene 9 tag crowding, scene 11 spacing, and the scenes 4/6/7/10 layouts were redone. See the new findings below for what remains.
- The chart in scenes 6-7 works. The tracks serve as the 100% scale, the numbers sit inside the fills, and the title is "MET THE 3-DAY GUIDANCE". The 96% and 53% bars match the VO.

## Findings

### Critical
None.

### Major
None.

### Minor
1. **Scene 9 (23-26 s): the "1 GAL / PERSON / DAY" tag is crowded.** The tag's right edge is at x~528 of 540, about 12 px from the frame edge (about 24 px at 1080), which is outside a typical safe margin. The tag also nearly touches the jug top and the check badge. The jug sits visibly above the ground line, with its bottom at y~580 against ground at y~615, so it floats. Fix: move the tag left and up (e.g. centre it under "WATER FIRST") and lower the jug onto the ground. DSL transform.
2. **Scene 4 (9.9-13 s): the "TOO BIG" tag overlaps the checklist prop.** It covers the left edge of list row 6, and the list rows run behind it. It is readable but looks like a layout collision. Fix: move the tag left of the list or above Inch. DSL transform.
3. **Scene 11 (30-32 s): the jug floats** about 35 px (at 540) above the ground and is very small next to Inch and the bin. The check badge floats in empty space to the right of "ONE LABELED BIN". Fix: lower the jug to the ground line, scale it up about 1.3x, and anchor the badge near the bin. DSL.
4. **Text under 40 px at 1080.** The "FOLLOW LOCAL GUIDANCE" tag is fontSize 30 in scenes 4-13, a 5-scene mismatch with the plan that the tag starts at scene 5. Scene 4 also shows a tag element at 30 px. Chart axis labels (FOOD / WATER), the cite card small print ("self-reported 2014, n = 572", "Hiatt et al., 2021"), and the "1 GAL / PERSON / DAY" tag measure roughly 20-30 px at 1080. This is legible in the draft but small for a phone. The guardrail line is the important one, so consider raising it to at least 40 px. Fix: DSL font sizes.
5. **Floating props, scenes 1-3 and 14.** The jug in scenes 1-2 and 14 hovers slightly above the ground line, and the scene 3 bin lid floats above the box body, with a plain engine-built box. This reads as intentional "lid off", but it is crude. Optional asset upgrade.
6. **Caption chunks are estimated, not word-timed.** Scene starts match the segment starts in script.json. Sampled stills show plausible sync (e.g. "FOOD TO" / "SHOPPING LIST" in scene 10, "SURVEY OF" / "572 ADULTS" in scene 5). Within-segment drift in seg-03 and seg-04 is possible, so a spot listen is advised. Scene 1's caption "SURVEY," is visible at 0.67 s and VO starts at 0.0 s, which is fine.
7. **Unchanged from the prior review, not a render defect.** The "about a gallon per person per day" wording is marked TO CONFIRM against Ready.gov in idea.md. Verify it and add the URL to publish.md. The framing line "Many of us mean to build an emergency kit..." is an unsourced but relatable creative choice (subjective).

## Passes
- Character consistency: Inch, palette, ground line, header chip, and caption style are consistent across all 14 scenes. No broken anatomy and no cropping of main subjects.
- Guardrails: "Try one item", "needs vary by household", and "Follow local guidance" are spoken and shown (scene 13 card, plus the tag from scene 5). No disaster prediction, product claims, or financial advice.
- Cite card (scene 5) matches idea.md and the chart values. Scenes 6-7 chart: no overlaps, no wrapping problems.
- Wrapping: no awkward text wraps found in any scene.
- Story reads muted: slates and tags carry the hook, problem, evidence, three steps, caveat, and CTA.
- Transitions: no blank or flash frames.
- Frozen frames: none seen in the stills.

## Recommendation
No blockers. Publishable as a draft. Fix minor items 1-3 (DSL transforms only; no VO re-run needed) before the final render, and confirm the Ready.gov wording.
