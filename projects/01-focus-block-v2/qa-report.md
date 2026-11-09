# QA report: 01-focus-block-v2 (draft gate)

Reviewed: output/draft.mp4, stills contact sheet (20 stills), frame 0 and last frame (extracted), script.json, animation.json (scene 1-2 structure), idea.md, storyboard.md. Checklist: docs/production/QA_CHECKLIST.md.

## Gate results
| Gate | Result |
|---|---|
| Technical (check_video.py --expect draft) | PASS: 360x640, 15 fps, h264, yuv420p, aac, 21.68 s, full decode clean |
| Black / frozen frames (ffmpeg blackdetect, freezedetect) | PASS: none reported |
| Audio levels | PASS: peak -3.1 dB (no clipping), mean -17.5 dB; 7 silences of about 0.35 s, all at segment gaps (2.30, 4.45, 8.83, 10.42, 13.69, 16.01, 18.78 s), intentional |
| Ending | PASS: video 21.68 s vs voiceover 21.59 s = ending about 0.09 s after VO; no trailing scene |
| Caption / voice sync | PASS (stills only, not frame-accurate): 1.35 s split = "One quick text is really" (20 of 35 letters x 2.368 s) is correct; scene 4 caption "STUDY, PEOPLE" at 6.17 s and "WHEN" at 7.37 s match the 7.55 s split; scene 5 "THEY SWITCHED" and "TASKS." land in the regrown-cube beat. |
| Claim accuracy | PASS with notes (below) |
| Story / retention | PASS with notes (below) |
| Visual defects | PASS: no blocking defects; minor items below |

## Blocking defects
None (no critical or major issues found).

## Defects (objective)
1. Minor, scene 8 (about 15.5-16.35 s): "OTHER ROOM" label ends flush against the "20 MIN" label (stills scene-08_16.13s). Text nearly collides. Also at 15.17 s the "FACE DOWN" label is not yet shown. Fix: DSL (shift the 20 MIN label or the slate label x, or shorten to "ROOM").
2. Minor, scene 4 to 5 (7.55 s): the ice cube is small behind the cite card (about 0.5x size in scene 4), then jumps to full size in scene 5. Probably the intended "regrow" beat, but the size jump coincides with the cut. Check in motion. Fix: DSL.
3. Minor, scene 10 (about 19.1-21.7 s): an unplanned on-screen line "HOW MANY PHONE CHECKS TODAY?" sits under the TRY IT TODAY note. It is not listed in storyboard scene 10 and competes with the caption just below it. It also duplicates the pinned-comment prompt. Fix: DSL (remove it, or add it to the storyboard if it is intended).
4. Minor, scenes 1 to 3: the character (Inch) is small (width 0.21). At 360 px wide the face and pose barely read. This is a draft-resolution effect; recheck at preview. Fix: DSL (scale), only if it still reads small at preview.
5. Minor, scene 1: storyboard says scene 1 shows only "20 MIN", but the big "2" is on screen from frame 0 (animation.json scene-01-stat2-f0). The storyboard and DSL disagree, but this matches the "number first" format in idea.md. Fix: update storyboard.md, not the video.

No character inconsistency, broken poses, merged objects, cropping, or safe-margin issues seen. The cube's right edge stays inside the frame. Captions stay at y 0.70 and are readable. Transitions show no blank frames in the sampled stills (not checked frame by frame).

## Claim accuracy vs idea.md (Rubinstein, Meyer & Evans 2001)
- "In one 2001 lab study, people were slower when they switched tasks" matches the verified finding (four experiments, alternating vs repeating tasks).
- Caveat is on the card ("SIMPLE LAB TASKS", readable at draft size) and the VO says "lab study"; it is not spoken as a limitation. This follows the rule in idea.md. Confirm that the description carries the full caveat; I did not check the description.
- "Two" is a plain-language framing (away and back) and is not presented as a measured count. Risk (minor): the big yellow "2" plus the "THE STUDY" card could be read as "the study found two switches". Scene 3 labels (1 AWAY, 2 BACK) explain it. Optional fix: description line stating "two" is a framing.
- Ice regrowing at away/back is a visual metaphor. It is not stated as a measurement. The 40% figure and the 20-minute block are not claimed as tested. OK.
- The "20 MIN" label above the cube is a timer label, not a research claim. "Try it today" is a suggestion. OK.

## Storytelling (checklist: Story)
- Hook promise (one text = two switches) is clear by 1.35 s. Setup (away, back), evidence (card), fix (3 steps), and try-it-today CTA resolve in order. Ice fully melting at the end pays off the timer image.
- Muted comprehension: mostly yes. The captions and slates (1 AWAY / 2 BACK, ONE TASK, FACE DOWN, LATER LIST, TRY IT TODAY) carry it.
- Visible change roughly every 1.5-3 s. The longest hold is the cite card (about 2.8 s), and that is intentional.

## Retention risk (prediction, not data)
Scorecard (docs/creative/STORY_AND_STORYBOARD.md), my estimate: Hook 1.5, Hold 2, Share 1, Look 0.5-1, Packaging 1 = about 6-6.5 out of 10. idea.md predicted 6.5. Both are below the 7 threshold in the doc, which says to rewrite the hook or change the format before approval. That is the user's creative call. I made no changes.
- Frame 0 as a silent still: only partly. It shows a big "2", "20 MIN", an ice cube, a snail, a phone with an alert, and the caption "ONE QUICK". The 2 has no label until 1.35 s, and the cube does not clearly read as melting. A muted viewer sees a puzzle without a reason to care. Preference-level, not a defect.
- Likely swipe points: about 0-1.4 s (2 unlabeled, hook sentence unfinished); about 4.8-7.5 s (citation card, the most lecture-like stretch, a text-heavy card with small type at feed size); about 10.7-14 s (the 3-step list begins, with less novelty than the first beats). The 2.6-4.8 s away/back beat and the closing melt are likely strong.
- Share trigger is weak (a question in-frame and a pinned comment). Share is likely to score 1 of 2.

## Non-blocking notes
- The draft is 360x640; recheck the small card text and Inch at preview (540x960).
- Frame-accurate caption/voice sync was not measured, only estimated from stills and the script timings. Confirm in a playback pass.
- Per CLAUDE.md, no final export should be rendered or overwritten without explicit instruction.
