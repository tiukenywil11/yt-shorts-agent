# QA report: 02-night-wind-down-v2 (draft gate, rebuild)

Inspected: output/draft.mp4, stills-contact-sheet.jpg, frame 0, frames 10.5-11.3 s, script.json, animation.json, idea.md, storyboard.md/json. Supersedes the previous report.

## Gates
| Gate | Result |
|---|---|
| Technical (check_video.py --expect draft) | PASS: 360x640, 15 fps, h264, yuv420p, aac, 18.13 s, full decode clean. No black frames detected. |
| Story / retention | PASS (see D-notes, Retention risk) |
| Visual | PASS, minor polish only |
| Caption / voice sync | PASS |
| Claim accuracy | PASS on video. One blocking text-hygiene item (D1) in storyboard files. |
| Body tag + clinician line | PASS |
| Ending | PASS |

## Blocking
### D1. Major: literal "same book" remains in project docs
- storyboard.md line 9 and storyboard.json line 68: "Inch neutral beside the same book" (stale, contradicts the correction that participants chose their own books).
- Also present as quoted negations, which will trip a string check: idea.md lines 10 and 25, storyboard.json line 15 ("NOT same book").
- Not in script.json, animation.json captions, or the video.
- Fix (docs only): reword scene 03 to "beside a paper book". Optionally reword the negations to "do not say the books were identical".

## Verified
- Voice and captions: hook is "Same bedtime, same dim room. On a screen, it took longer to fall asleep." Closing lines match the brief. Caption text equals script text in every scene.
- Sync (silencedetect vs scene starts): speech resumes at 9.598 (scene 5 starts 9.567), 10.58 "ten" (card at 10.667), 13.19 (scene 7 at 13.166), 15.68 (scene 8 at 15.656). Sampled caption chunks (0.93, 1.67, 3.27, 4.47, 5.87, 6.90, 8.33, 9.37, 10.13, 10.50, 11.90, 12.97, 14.40, 15.47, 16.87, 17.90) track the words.
- Ending: last audible speech ends about 17.92 s, file ends 18.13 s. The nominal end is 18.003 + 0.1 = 18.10. The silent tail is about 0.2 s, which is the 0.1 s target plus encoder padding. OK. No trailing loop scene.
- Transition: all transitionOut are "cut". The cite card at 10.5-11.3 s has no leftover bar elements. Frames 10.5 to 11.3 s show the SCREEN/PAPER bars cleanly replaced by the card. No flash or blank frame.
- Claims:
  - 25.65 vs 15.75 min is shown as ~26 vs ~16, which rounds correctly.
  - "nearly ten minutes" matches the voice. The caption "ten minutes longer" is fine because "nearly" is spoken and shown just before it.
  - n = 12 and "one lab study" are on the card.
  - Voice and card say "in a lab" and "twelve adults".
  - Only paper vs screen is claimed. No dimming, wind-down or sleep-disorder claims.
- Body tag: "BODY · SLEEP" chip is on every scene. "NOT MEDICAL ADVICE" appears from 10.87 s (scene 6) through the end. Clinician line "If you have a condition, ask a clinician" is on the card from about 11.17 s, and was readable in the 11.90 s and 12.97 s stills.
- Character: Inch (snail) is consistent in every scene. Poses tired, worry, neutral, idea and cheer are intact, with no broken anatomy.
- No black frames, no cropping, and captions are inside safe margins.

## Non-blocking defects (all minor, fixable in DSL)
1. Scene 6 card text is small (40 px at 1080 wide, about 13 px in the draft). "PAPER: ~16" lacks "MIN", and "SCREEN: ~26 MIN TO SLEEP" wraps to two lines, which looks uneven. Fix: "SCREEN: ~26 MIN" / "PAPER: ~16 MIN", raise fontSize to about 48.
2. The "NOT MEDICAL ADVICE" and clinician strips are very small. They are legal and readable in the full-size frame but weak at feed size. Optional: raise the font to about 46.
3. Scenes 1, 2 and 4: a thin white vertical divider floats above the phone and looks like a stray artifact because nothing else shares the split. Fix: shorten it or remove it.
4. Scene 1: the snail Inch is partly hidden behind the starburst glow and is very small relative to the phone. It is readable, but the "larger hero" benefit goes to the phone and not to the character.
5. Scene 4 (about 9.3 s): the second Inch slides in over the book (overlap). It is brief. Fix: move scene-04-inch-r to about x 0.5 or shift the book.
6. Scene 7 (13.2-15.7 s) is sparse. A tiny check sits above a book and lamp, with a large empty mid-screen area. Fix: increase the check size or add the "PAPER" label. This is also the most likely hold dip.
7. Scene 8: the "PAPER OR SCREEN?" bar and the check sit close to the note (about 16.9 s). It is readable but crowded.
8. Hero is a phone, but the study used a light-emitting eReader. The card says "SCREEN", which is acceptable. A phone is the usual viewer example, so consider keeping "screen" and never saying "phone" (currently true).
9. Scene 1 shows both numbers (~26 / ~16 MIN) at frame 0, so the answer is given immediately. Intentional for result-first, but it removes curiosity for later scenes.

## Stale-doc notes (not defects in the render)
- storyboard.md header says voiceover 18.771 s. script.json says 18.003 s (animation ends 18.1 s).
- storyboard.md scene 01 says "hero glowing phone (glow width 0.5)" and on-screen text "SCREEN; PAPER". animation.json has glow 0.42 and labels "SCREEN ~26 MIN / PAPER ~16 MIN".
- storyboard.md scene 08 omits the "PAPER OR SCREEN?" bar. Scenes 07 and 08 list NOT MEDICAL ADVICE, which matches the animation.
- storyboard.md scene 06 on-screen text lists "PAPER: ~16", matching the animation. This is acceptable, but see item 1.
- idea.md hook candidate remark and the "Corrections" block are up to date. Scorecard is 6.5.

## Retention risk (prediction)
Scorecard (docs/creative/STORY_AND_STORYBOARD.md), predicted:
- Hook 2/3: result-first contrast, a clean claim with no question and no strong surprise.
- Hold 2/3: a visible change every 1 to 3 s (bars, dots, card, lamp). Scene 6 is a read-the-card caveat stretch.
- Share 1/2: the "Paper or screen?" prompt gives viewers a side.
- Look 0.5/1: the phone and glow read at feed size. The snail is tiny.
- Packaging 1/1: the title promises "the screen lost" and the video pays it off.
- Total 6.5, below the 7 threshold in the doc. This is the same as the idea.md prediction, so it is not a regression.

Likely swipe points:
- 0-1.9 s: viewers who do not feel a hook from the declarative line.
- 4.7-7.1 s: "twelve adults read before bed in a lab" is setup, not payoff, and the answer was already shown at frame 0.
- 11-13 s: the cite card and caveat strip are text-heavy with small type.
- 13.2-15.7 s: the sparse CTA scene.

Frame 0 as a still with sound off: yes. It shows a glowing phone vs a book, SCREEN ~26 MIN vs PAPER ~16 MIN, and the caption "SAME BEDTIME". The takeaway (the screen takes longer) is legible. The weak points are the stray divider line and the tiny snail.

## Recommendation
Draft gate passes on technical, story and claim accuracy once D1 is reworded in storyboard.md/json (docs only, no re-render). Minor items 1, 3 and 6 are the best optional polish before preview. Do not treat any of this as creative direction changes.
