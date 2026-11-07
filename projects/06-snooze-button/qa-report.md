# QA Report: 06-snooze-button (draft)

Reviewed: output/draft.mp4, draft-contact-sheet.jpg, frames at 1.0 s, 7.8 s, and script/storyboard/animation.json.

## Technical
check_video --expect draft: all PASS (360x640, 15 fps, h264/yuv420p, aac, 41.94 s, clean decode). Mean volume -17.7 dB, peak -3.0 dB (no clipping). No black frames or blank transitions seen on the contact sheet. Scene timings cover 0-41.96 s with no gaps.

## Major
1. scene-06 (13.18-17.94 s): stamp reads "MAYBE" (asset assets/ui/actually_stamp.svg, element scene-06-actually; storyboard says ACTUALLY). It hedges against the narration "did as well or better" and the myth payoff, and the stamp was not a MYTH?/MAYBE pair in the plan. Fix: swap the stamp asset to read ACTUALLY (or approve MAYBE as a creative decision). Asset change only. Note: the stamp is vector paths, so wording cannot be read from the SVG text; confirmed visually.
2. scene-02 (2.23-4.50 s): stamp reads "MYTH?" with a question mark; storyboard and VO ("The myth says...") call for MYTH. The "?" reads as undecided and clashes with the cross badge. Fix: swap assets/ui/myth_stamp.svg to MYTH without "?". Asset only. Rated major because it pairs with issue 1; downgrade to minor if intentional.

## Minor
3. scene-01 (0-2.23 s): the clock has no visible SNOOZE button; the SNOOZE tag floats to the upper right of the clock, not attached to it. Inch is a flat, low pose, which reads as resting rather than tired, though not broken. Hook is understandable via caption. Fix: DSL, move the SNOOZE tag directly above/on the clock, or add a button shape (asset if the Sun button is wanted).
4. scene-04 (6.9-9.61 s): Inch is small at bottom left under the large cite card; readable but weak presence. Fix: DSL, scale Inch up or shift the card up. Not blocking.
5. scene-04: cite card shows "Sundelin et al., 2023", matching narration "A 2023 lab study". Verify year against the paper (doi 10.1111/jsr.14054) before final, since online vs issue year can differ. Not verifiable from rendered media.
6. Missing clinician line: script has "This is not medical advice" and the NOT MEDICAL ADVICE tag, but no "ask a clinician" wording. Fix (only if channel policy requires): script and VO change (audio rerender).
7. scene-06 length: 4.76 s, the longest scene, with a mostly static layout after the stamp and tick land. It follows the VO sentence, so sync is fine. Optional: add a small motion beat or split into two visuals (DSL).
8. scene-15 (41.36-41.96 s): the PLANNED SNOOZE tag overlaps the clock crown. Loop frame only 0.6 s; negligible. Fix: DSL, nudge tag up.

## Checked, no defect
Character (Inch the snail) is consistent across scenes. No cropping or safe-margin issues; captions are readable. Audio: intelligible, synced to scene cuts (cuts within segments are letter-count estimates). The story is understandable muted. No unsupported claims beyond the cited study, and the limits (31 snoozers, one lab study) are shown.

## Recommendation
Fix first (quick): swap the two stamp assets (issues 1 and 2) and the scene-1 tag placement, then re-render the draft. Otherwise technically publishable.
