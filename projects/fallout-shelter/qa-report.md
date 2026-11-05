# QA Report: fallout-shelter (preview, re-review)

File: `output/preview.mp4` (540x960, 24 fps, 59.31 s)
Scope: contact sheet (24 frames), 13 extra frames or crops, silence/volume/black-frame scans, check_video, animation.json and script.json timing cross-check.
Not reviewed by ear: narration intelligibility at 1.25x speed, SFX balance. A listen-through is still needed. Sync was judged from silence gaps in the audio versus on-screen timings.

## Technical
- check_video: all PASS (resolution, fps, h264, yuv420p, aac, duration 59.31 s, full decode clean).
- Audio: mean -26.6 dB, peak -5.6 dB, so no clipping. The only trailing silence is the last 0.54 s (58.77 to 59.31), which is intentional. No black frames detected.

## Prior issues: status
| # | Prior issue | Status |
|---|---|---|
| 1 | FIX n/9 badge lagged narration | RESOLVED. Each badge starts at scene start (e.g. 1/9 at 3.13 s, 2/9 at 7.47 s, 8/9 at 36.74 s) and matches the contact sheet. |
| 2 | Interior props unreadable | MOSTLY RESOLVED. Fan, shelf, bucket and lanterns are now clear at 540x960 (glow and camera push help). Residual issues are listed below as M1 and m1 to m3. |
| 3 | Duration over target | RESOLVED. 59.3 s is under the 66 s target and under 60 s. |
| 4 | Tuck very small | Unchanged (minor). Still readable as a character, but the expression is not readable. |
| 5 | FIX 9/9 persists through scenes 11 and 12 | NOT FIXED (minor, m1). |
| 6 | Scene-11 fallout specks faint | NOT FIXED (minor, m2). |
| 7 | Disclaimer small | Legible at 540 px, but see M1. |
| 8 | Night swap late | RESOLVED. Night starts at scene-09 start (36.7 s) and "pitch black" is in the first words. |

## Critical
None.

## Major
M1. scene-12 disclaimer is on screen for only about 1.15 s (startSec 3.832, durationSec 1.151; roughly 58.1 to 59.3 s), and the video ends right after it.
- The text is 17 words, so it cannot be read in that time. It is a safety and accuracy disclaimer, so it should be readable.
- It also appears together with the "Ready beats lucky." caption and the READY stamp, so it competes for attention.
- Likely cause: the rescale shortened scene-12 timings proportionally (seg-12 and seg-13 are 3.4 s and 1.15 s long).
- Smallest fix: DSL. Start the disclaimer at about 1.2 s in scene-12 (about 55.5 s) so it holds for 3 s or more, or add a short end hold of about 1.5 s after the last word. This is a creative and compliance call, so I have not made the change.

## Minor
m1. "FIX 9/9" is stale for about 11 s (scenes 11 and 12, 48.05 to 59.3 s), so it stays on screen through the fallout-decay reveal and the outro. DSL: remove `s11-fix-9of9` and `s12-fix-9of9`.
m2. scene-11 "fallout-a/b/c" red specks are barely visible against the night sky (checked at 49.8 s). The stat callouts carry the reveal. DSL: raise speck size or opacity.
m3. Props with weak readability at 540x960:
- scene-02 roof (about 6.8 s) is a thin line, and scene-04 timber posts and beams (about 16.5 s) are faint, so those two fixes still look almost identical to the prior frame. The cue is clearer if the push-in or a brief highlight is applied there too (camera_push is currently only on 03, 05, 07 to 10).
- Water jugs (scene-07) read as small teal squares on the shelf. The radio (scene-10) is about 20 px and is only recognisable by the glow.
- Fix: DSL, scale up the jug, radio and timber elements, or reuse the pulse-glow preset. Visual-only, and understandable with narration.
m4. scene-12 READY stamp overlaps the top-right of the shelter cutaway (about 58.4 s) and partly covers the surface line. DSL: shift it up or left by a few percent.
m5. The scene-05 baffle tag (21.96 to 22.72 s) and the scene-10 "STAY TUNED" tag (47.27 to 48.05 s) are each on screen for under 0.8 s. They are legible and in sync with "hates corners" and "stay tuned", but they are brief. Optional.
m6. Single-word captions at 1.25x are fast (for example "A" at 21.9 s). This is a pacing preference, not a defect. Judge it by ear.

## Sync check after retime (OK)
- Stat callouts versus audio gaps:
  - "7 HRS ÷10" (50.57 to 52.55 s) ends at the pause after "weaker" (52.53 s).
  - "2 DAYS ÷100" (52.71 to 54.31 s) ends at the pause after "a hundred" (54.03 s).
  - "3 FT" and "1 GAL/DAY" appear late in their sentences, as intended.
- Roof drop (6.79 s) falls right after "So we add a roof" starts (about 6.3 s).
- Baffle tag, stay-tuned tag and badges (see M1 and m5) match their lines.
- Scene boundaries line up with natural pauses of 0.3 to 0.45 s, so no narration is clipped mid-word. The narration ends (about 58.8 s) before the video end, and there is no abrupt cut.
- No frozen-frame or transition-flash concerns. Character (Tuck) is consistent across frames, with no broken anatomy or merged objects. The "÷" glyph renders correctly. Captions are within safe margins.

## Recommendation: PUBLISH after one small fix
There are no blockers, and prior majors 1 to 3 are resolved. Fix M1 first (disclaimer timing, DSL-only, scene-12). Remove the stale FIX 9/9 badge in 11 and 12 (m1) at the same time. Then re-render only scene-12 (and 11), re-run `python scripts/check_video.py ... --expect preview` and listen once for 1.25x intelligibility. The remaining items (m2 to m6) are polish.
