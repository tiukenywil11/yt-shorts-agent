# QA Report: trailer draft (output/draft.mp4)

Scope: draft only, no renders, no edits to other files. Inputs: contact sheet, 22 stills, ffmpeg samples at 6.6-8.1 s, `animation.json`, `script.json`, `voiceover.wav` energy analysis (pause positions), `creative/style-bible.md`.

## Technical (check_video.py, expect draft): PASS
360x640, 15 fps, h264, yuv420p, aac, 28.74 s, full decode clean. blackdetect: none. freezedetect (>1.2 s): none. Audio peak -3.5 dB (no clipping). VO ends 28.651 s, video 28.74 s (about 0.09 s tail), and scene-11 is the last scene, so there is no trailing scene.

## Sync at every cut
Scene starts were compared to the real pauses in `voiceover.wav` (not just script.json). All 10 cuts land inside a VO pause or within 0.05 s of a script segment start.

| Cut | Scene start | Real pause | Verdict |
|---|---|---|---|
| 01 to 02 | 2.981 | 2.58-3.02 | OK |
| 02 to 03 | 5.855 | 5.52-5.88 | OK |
| 03 to 04 | 7.95 (estimated) | 7.92-8.20 | OK, see m1 |
| 04 to 05 | 9.795 | 9.46-9.84 | OK |
| 05 to 06 | 12.115 | 11.76-12.16 | OK |
| 06 to 07 | 13.40 (estimated) | 13.36-13.60 | OK, 0.2 s early |
| 07 to 08 | 15.629 | 15.24-15.66 | OK |
| 08 to 09 | 17.80 (estimated) | 17.44-17.88 | OK |
| 09 to 10 | 21.959 | 21.64-22.00 | OK |
| 10 to 11 | 25.366 | 25.04-25.38 | OK |

The letter-count estimates for scenes 03/05/06 (and 08/09) are accurate. Nothing needs re-timing. The ~7 s problem is a layout defect, not a sync defect (see M1).

## Findings

### Major

**M1. scene-03 (5.855-7.95, the ~7 s mark): text collides with the card border.**
- Objective: "1 CITED FACT" (84 px) touches the top border of `scene-03-card`. "STUDY NAMED · LIMITS SHOWN" (40 px) sits on the bottom border. Both are visible in `scene-03_6.90s.png` and `scene-03_7.77s.png`, and the card is static for the whole 2.1 s. Reads as a layout bug.
- Cause: the card is 0.2 high but the two text lines are 0.09 apart (y 0.34 and 0.43) around a card centre of 0.38. Heights are width-relative (0.2 is about 216 px), so the card is about 173 px of the 216 px used by the text.
- Fix (DSL, `animation.json` scene-03): set `scene-03-card.params.height` from 0.2 to 0.26 (card spans y about 0.31-0.45 of the frame, text sits inside with padding). Keep `scene-03-card` y 0.38, `scene-03-num` y 0.34 and `scene-03-sub` y 0.43. Alternative: card height 0.2, `num` y 0.365, `sub` y 0.41.

**M2. scene-05 (9.795-12.115): "GETTING READY" is 34 px, below the 40 px minimum.**
- Objective: `scene-05-ptxt3` has fontSize 34 (the other three pills use 40). It also wraps to 2 lines in a 0.1-high pill.
- Fix (DSL): set `scene-05-ptxt3.params.fontSize` to 40. Set pill heights to 0.12 on `scene-05-pill2` and `scene-05-pill3` (or all four, to keep the row even) and move the text y by +0.005 so two lines fit. Do not shorten the word to "READY" without sign-off, since the narration says "getting ready".

### Minor

**m1. scene-04 (7.95-9.795): early visuals, wasted CTA stamp.**
- The caption "AND ONE" shows at 7.95, about 0.25 s before "and" is spoken (8.20). A 15 fps frame at 7.9 s already shows scene-04 as empty cream background.
- `stamp_thud` SFX plus the TRY IT TODAY note fire at 8.05, about 0.8 s before the words "try today" (about 8.9 s). The same stamp is reused at 25.47 (scene-11), where it carries the CTA.
- Fix (DSL): set `scene-04-tnote.startSec` to 0.75 and `sfx.atSec` to 0.7. Optionally shift `scene-04-cap` start by +0.2 s, with the duration reduced to match. Do not move the cut.
- Creative note: keeping the note here at all is a taste choice, so the director decides.

**m2. scene-08 (15.629-17.8): tiles off-centre, inconsistent wrap, past the right safe range.**
- `scene-08-c2` and `t2` ("ITS LIMITS", x 0.72, w 0.34) span x 0.55-0.89. The bible's range is 0.06-0.84, and the centre is 0.46. "THE STUDY" wraps to 2 lines while "ITS LIMITS" does not.
- Fix (DSL): c1/t1 x 0.27, c2/t2 x 0.65, width 0.36 (same grid as scene-05 pills), t1/t2 fontSize 48.

**m3. Disclaimer tag left edge (scene-08, scene-09).**
- `*-tag-back` is x 0.43 with w 0.8, so it spans 0.03-0.83. The bible says x 0.06-0.46 and a 0.06 left margin. The tag reaches about 32 px from the left edge.
- Fix (DSL): x 0.46, w 0.76, so it spans 0.08-0.84. The 40 px text still fits ("NOT FINANCIAL OR MEDICAL ADVICE" is about 0.7 wide). Note that the bible's tag is narrower (to 0.46), so the long wording is a deliberate deviation.

**m4. Right-edge props beyond x 0.84, which is the Shorts action-rail zone.**
- `scene-02-step2` (right edge 0.89), `scene-05-coin` (x 0.84, w 0.14, right edge 0.91, y 0.575), `scene-11-chk` (0.94), `scene-11-timer` (0.86).
- Fix (DSL): shift left by 0.05-0.08. For example, coin x 0.80 w 0.12 and scene-11-chk x 0.84.

**m5. scene-10 (21.959-25.366): contrast and caption chunking.**
- "EXPLAINED BY SCIENCE" is Mint on the Body tint, about 2.6:1 contrast (Mint is also reserved for do/gain semantics). Fix (DSL): Ink `#26303F`, or Mint on Paper.
- The caption chunk "SCIENCE, PRACTICED" is shown at about 23.67 and wraps to 2 lines, while the VO is still saying "science" ("practiced" starts at about 24.1). Fix: split the Caption's `content` so the comma ends a chunk (for example, set `wordsPerChunk` 1 for that scene), or accept it.
- `scene-10-l2` ("PRACTICED IN PUBLIC", 23.81) leads the VO by about 0.3 s against the 0.1 s bible rule. Fix: `startSec` +0.15.

**m6. scene-05 sequencing and the coin.**
- A lone coin prop appears with the first pill and stays. It reads as "money only" next to four equal pillars. Fix (DSL): remove it, or add it at the MONEY pill only if intended. This is a creative choice.
- The pill pops land at 9.85, 10.35, 10.85 and 11.35, which are within about 0.2 s of the nouns. No change needed.

**m7. scene-06: dot calendar has no narrative.** Seven dots with one highlighted at a fixed spot. They read as decoration for "every week". This is creative preference only.

### Passed checks
- Captions match narration in every scene (text-wise). Caption timing is within one chunk in all samples (scene-03: GIVES YOU at 6.90, FACT at 7.77, VO "fact" ends at 7.92).
- Min text size: all 40 px or greater except M2. Chip is 40 px, captions are 84 px.
- Palette: only core and tint hexes are used. The `#EFE2C9` Ready tint in scene-02 and scene-11 is a deliberate tint. Coral is used only for the "NOT ADVICE" text and the body dot, which is acceptable for a don't or caveat.
- Character: Inch is consistent in every scene (same size and position, poses neutral/idea/skeptical/cheer). There are no broken poses or merged objects, and no cropping.
- Guardrail wording: "general education, not financial or medical advice" is spoken, shown on the tag and shown on the scene-09 headline. "We name each study and its limits" matches the cite-card promise. The claim "every Short gives you one cited fact" is consistent with the bible. No health or financial claims are made.
- Hierarchy: new element, then caption, then Inch holds in all scenes. Motion is low, with at most 3 movers.
- Ending: last caption and VO end at 28.651. Video ends 0.09 s later. No loop scene, no silent tail.

## Fix routing
All fixes are DSL only (`projects/trailer/animation.json`). No asset, audio or engine change is needed. After applying M1, M2 and m2-m4, render stills for ALL scenes (per the project rule), then re-run check_video.py on the draft.
