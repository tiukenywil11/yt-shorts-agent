# QA Report: 02-night-wind-down (draft)

Artifact: `output/draft.mp4`. Reviewed: contact sheet, stills scene-01/04/12/14, animation.json, script.json, storyboard.md, idea.md.

## Verdict
PASS WITH FIXES. No critical defects. Draft is technically clean and the claims and guardrails hold. One known major caption defect (scene-12) and a few minor polish items remain.

## Technical (scripts/check_video.py --expect draft)
- RESULT: PASS. 360x640, 15 fps, h264, yuv420p, aac, 36.42 s, full decode clean.
- Audio: max peak -4.2 dB, mean -17.5 dB, so no clipping. No silence gap longer than 0.8 s (silencedetect). No black frames (blackdetect).

## Guardrails and citation (all PASS)
- Cite card (scene-04) shows THE STUDY / Chang et al., 2015 · PNAS / SLOWER TO FALL ASLEEP / one lab study. No n= and no minutes. Matches idea.md (abstract only).
- Narration says "In a 2015 lab study", "one lab study, so results vary", and "may" in the hook. No "studies show" or "proven".
- NOT MEDICAL ADVICE is visible from scene-04 to scene-14. Clinician line is in scene-12 and the narration. No melatonin or supplement claims.
- "Less alert next morning" is supported by the abstract.

## Defects (ranked)

1. **MAJOR, scene-12 (30.13-33.12 s): caption "SLEEP CONDITION," wraps to two lines.**
   - Evidence: the caption renders as SLEEP / CONDITION,. The second line drops to about y 0.75, below the 0.66-0.74 caption band. The chunk is two words and does not fit on one line at 84 px.
   - Risk: not an overlap, since it sits on the floor strip, but it breaks the one-line caption rule and the layout is inconsistent with every other scene.
   - Likely cause: the Caption maxWidth is narrower than the chunk width. Every other chunk fits one line.
   - Smallest fix: DSL only. For `scene-12-cap-05` use wordsPerChunk 1 so the chunk is "SLEEP" then "CONDITION,". Alternatively reduce fontSize to about 72 for that element. If engine code is touched, widen the Caption maxWidth to about 0.80, within the x 0.06-0.84 safe range.
   - Note: the tag above it already shows "SLEEP CONDITION? ASK A CLINICIAN", so the wrap hides nothing but it is redundant.

2. **MINOR, scene-01 (0-2.55 s): hook caption is fragmented.**
   - Evidence: at 1.27 s only "KEEP YOU" is shown. The full claim never reads as a unit, and "bedtime screen" is visible only for the first chunk. The storyboard says "caption states the claim".
   - Fix: DSL. Make the hook a 3-4 word on-screen line, or keep the 2-word chunks but start them faster. This is a creative preference, so confirm before changing.

3. **MINOR, scene-01 to scene-13: weak retention framing.**
   - Evidence: the top 45-50% of every frame is empty Ink and the floor strip fills the bottom 25%. Inch is about 12% of frame width. The hook phone is small, and its glow reads as a muted ochre spike.
   - This is on-style and not a defect. It is a retention risk. Consider scaling Inch and the phone or book 1.3-1.5x, or placing the hook phone higher.
   - Fix: DSL (transform and width params). Subjective.

4. **MINOR, scene-07 (15.15-18.01 s): storyboard element not visible.**
   - Evidence: the storyboard says a small Sun circle for "the morning". It is not visible in the stills at 16.57 s or 17.80 s. The frame is mostly empty, with just the tag and the tired Inch.
   - Fix: DSL. Check that the element exists and its startSec, or drop it from the storyboard.

5. **MINOR, scene-14 (loop, 0.6 s): loop mismatch.**
   - Evidence: the loop frame matches the hook layout (Inch, book plus lamp) but keeps the chip and the NOT MEDICAL ADVICE tag. Scene-01 has no disclaimer, so there is a small jump at the loop point. There is no caption on scene-14, which is by design.
   - Fix: optional. Either accept it or fade the disclaimer out in the last 0.2 s. Subjective.

6. **MINOR, scenes 03, 07, 10 and others: blank caption frames.**
   - Evidence: the last 0.25 s of some scenes shows no caption, which is the inter-segment gap by design. Captions are chunked by letter count, not word timing, so there are some phrase splits like "ALERT THE" and "STEPS IN". Word-level timing is a known FUTURE item.
   - Fix: none needed now. Re-check sync against audio in preview.

7. **MINOR, working title.**
   - "Your Bedtime Screen Has a Cost" is more absolute than the on-screen "may" language. Use a hedged title, for example "Your Bedtime Screen May Cost You Sleep", at publish time.
   - Fix: metadata.

## Not found
- No character inconsistency (Inch is the same snail across scenes), no broken poses, no merged objects, no cropping, and no transition flashes.
- Safe zones: the chip is at x 0.06, and all text is inside x 0.06-0.84 and above the caption band except the scene-12 second line (defect 1).

## Limits of this review
Visual checks used the contact sheet and 3 sampled stills, plus the card/loop stills. Audio and caption sync was judged from the segment timings in script.json and the stills, not by a listen-through. Items 4 and 6 are worth confirming in preview.
