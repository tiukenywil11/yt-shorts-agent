# QA Report - 08-habit-21-days (preview)

Scope: one contact-sheet pass of output/preview-contact-sheet.jpg (24 frames, 1.29 s apart) plus check_video. No extra frames sampled and no audio listening pass. Audio sync, clipping and narration intelligibility are NOT verified.

## Technical (objective)
- check_video --expect preview: PASS. 540x960, 24 fps, h264, yuv420p, aac, 30.64 s, full decode clean.
- retention_lint: PASS (30.5 s, as reported).
- No black frames or blank transitions visible on the sheet.

## Defects (objective)

| # | Sev | Where | Description | Likely cause | Smallest fix | Fix via |
|---|-----|-------|-------------|--------------|--------------|---------|
| 1 | major | 5.2 s to 29.7 s | Hero is a small track (about 15% of frame width tall strip) with 8-10 px-equivalent labels ("DAYS TO LEVEL OFF", "HOW AUTOMATIC", "WHEN EACH PERSON LEVELS OFF", "96 VOLUNTEERS", "21", "DAY 1"). Labels are likely unreadable at feed size. Large empty area between the track and the ground, and the lower ~35% of the frame is empty brown. | Hero and label scale values small; layout anchors at upper third. | Scale the track and its labels up about 1.5x and enlarge the key number labels. Move the track down toward the vertical centre. | DSL |
| 2 | major | 16.8 s to 23.3 s (and 5.2 s to 16.8 s with the same track) | Same 18-254 track stays on screen with only small overlays (day marker, tick boxes). Matches the known static concern. Nothing reads as a new picture for about 6 s. | Single persistent track plus overlay-only changes. | Add a scale or colour punch on each key beat (22 days, 7 ticks, 21 fail), or cut to a different framing at about 16.8 s and 23.3 s. | DSL |
| 3 | minor | 14.2 s and 15.5 s | Study card: the "THE STUDY" tab sits against or past the card's left edge and looks clipped. The footnote "model estimate, 39 good fits" is tiny. | Rotated card with the tab offset. | Inset the tab by about 8 px. Enlarge or drop the footnote. | DSL |
| 4 | minor | 6.5 s, 9.0 s | Floating labels ("96 VOLUNTEERS", "12 WEEKS") sit right of the track with no anchor, so they look unattached. | Label offset. | Anchor each under the track or the relevant endpoint. | DSL |
| 5 | minor | 11.6 s | Caption row is empty while the audio is presumably mid-sentence. Could be a natural pause, so please confirm. | Caption chunk gap. | Fill the gap or confirm the pause in the caption timing. | DSL or audio |
| 6 | minor | 2.6 s | The big calendar disappears and only an empty bar with "ESTIMATED HABITS" remains. That is a weak visual after the strong frame 0. | Scene 2 has no hero object. | Keep a faded calendar, or show the 21 marker earlier. | DSL |
| 7 | minor | 23.3 s, 24.5 s | The checklist and clock icons are small and crowd the snail. | Icon scale and position. | Scale up about 1.5x and move away from the snail. | DSL |
| 8 | minor | Whole video | The snail is small, bottom-left, and shows no reaction on the sheet (unconfirmed: only a few frames show a slightly different pose). | Ambient only. | Optionally add a reaction on the fail and success beats. This is a creative choice. | DSL |

Not defects: caption position (about 70% down, likely clear of the Shorts UI) and consistency of the snail and header chip look fine.

## Retention risk (prediction, not defect)
Scorecard (predicted, /10):
- Hook 2/3: frame 0 is a large "21 DAYS" calendar with "FORGET 21" and a MYTH? stamp at 1.3 s. It has a surprise but no question.
- Hold 2/3: text and bar change about every 1.3 s, but changes are small after 16.8 s.
- Share 1/2: a "myth-bust" gives a side to take, but there is no obvious send-to person.
- Look 0/1: the hero reads at feed size only in the first 2 s. The track is small afterwards.
- Packaging 1/1: the myth-bust promise is paid off with the 18-254 range and the Day 1 action.
- Total: 6/10. Below the 7 threshold in the storyboard doc.

Likely swipe points:
- 2.6 to 4.0 s: the visual drops from the big calendar to an empty bar.
- 9 to 14 s: dense numbers with tiny labels and a caption gap at 11.6 s.
- 16.8 to 23.3 s: static track, the main drift risk.

Frame 0 as a silent still: yes. "21 DAYS" with "FORGET 21" reads clearly with the sound off. It states the claim but does not pose a question, and the snail adds nothing at that size.

## Creative notes (subjective, no change made)
The tracking-bar metaphor is reasonable. Tightening scale (defect 1) is the lowest-risk way to lift the Look and Hold scores.

## Status after fixes (2026-11-08, preview re-render)
- Major (small hero and labels): fixed in DSL; track and labels scaled up and moved lower, small tags enlarged.
- Major (static track, 16.8-23.3 s): reduced in DSL; camera push added on scene-10 and the icons were enlarged. Not re-scored; it remains the likeliest flat stretch.
- Fixed in DSL: study-card tab inset; icons clear of Inch.
- Open minor: caption gap at about 11.6 s (natural pause between segments); weak visual at 2.6 s.
