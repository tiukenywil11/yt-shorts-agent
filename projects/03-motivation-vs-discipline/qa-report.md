# QA Report: 03-motivation-vs-discipline (draft.mp4)

Scope: output/draft.mp4, contact sheet, stills (scenes 01 and 09 viewed full size), storyboard.md, script.json, idea.md, style bible excerpts.

## Technical: PASS
`python scripts/check_video.py output/draft.mp4 --expect draft` returned PASS: 360x640, 15 fps, h264 yuv420p, aac, 39.81 s, clean full decode.
- ffmpeg blackdetect and freezedetect (1.5 s threshold): no black or frozen spans.
- Audio: peak -2.9 dB (no clipping), mean -17.5 dB. Silences (>0.3 s) fall only on segment gaps (2.63, 4.17, 8.02, 20.45, 27.70, 30.34, 35.75, 39.15 s). The 4.17 and 27.70 gaps are mid-segment sentence pauses. Trailing 0.66 s silence is the loop frame (scene-15), which is intended.

## Defects (severity-ranked)

No critical defects.

### Major
1. **Claim tone vs guardrail, scene-01 and scene-06.** The hook narration is hedged ("may not"), but the on-screen coral `MYTH` stamp (scene-01) and the mint `ACTUALLY` stamp (scene-06) are categorical. idea.md says to use "may / linked with / one set of studies", and the finding is correlational. Stamps read as "science says". Likely cause: the Habit Myths template stamps. Fix: DSL text. Relabel the stamps (for example `MYTH?` and `MAY BE`) or swap in `LINKED`. This is the same hedging the narration already uses. A creative call is needed, so I did not change it.
2. **Steps presented as study-backed, seg-04 / scenes 08-11.** Narration goes straight from the finding to "So build the habit... One: fixed cue. Two: two minutes. Three: start at the cue." idea.md says the cue and two-minute start were NOT tested. The caveat in seg-05 ("These results were linked, not proven") comes after the steps and reads as being about the steps or the study ambiguously. Nothing says the steps are a suggestion rather than a finding. Fix: DSL/script. Change the transition to "A practical way to try this:" (or add "These steps are a common-sense way to apply it, not tested here"). Re-run TTS for seg-04 only. This is a script edit, so check timing after.

### Minor
3. **Retention dip, scenes 03-07 (5.6-20.8 s).** About 15 s of narration is carried by small tag chips and a near-empty stage (scenes 05 and 07 show only a tag, a tiny Inch, a check). Scene 03 is a static clock and closed book. There is no new moving element for the 12 s study narration apart from the cite card (scene 04) and the ACTUALLY stamp (scene 06). Not a defect for publishing. Suggested fix, DSL: add a stat_callout for `N = 2,274` (style bible allows one emphasis element per beat), or shorten seg-03. Optional.
4. **Caption sync estimates, scenes 04-07 and 08-11.** Seg-level cuts line up with the audio at the 2.94, 8.33, 20.76, 30.65 and 36.05 s boundaries. Cuts inside segments (scenes 03/04-07, 08-11, 12-13) are letter-count estimates, and I could not confirm them against spoken words. Spot checks of caption text vs. visual are plausible: "STAYS UNTOUCHED" with the untouched book, "LESS EFFORT", "BREAKFAST" with slate 1, "MINUTES" with slate 2, "NOT PROVEN" with the LINKED, NOT PROVEN tag. Risk: scene-05 (BETTER SELF-CONTROL, 11.83-14.20) and scene-06 (ACTUALLY stamp at 14.20) may land a few tenths of a second off. Fix: audio/engine (force-align word timings) if a listen test finds drift.
5. **Cite card shown while "SIX STUDIES / TOTAL" captions run, scene-04.** The card does not show n, which is intentional (spoken only), so the card has a smaller claim than the narration. Acceptable. Note that `Galla & Duckworth, 2015` is legible only at 1080 size. At 360x640 it is tiny, so check in the preview render.
6. **Slate sub-labels, scenes 09-11.** "FIXED CUE · AFTER BREAKFAST" wraps to two lines and uses the same Paper-fill/Ink-stroke style as `caption_main`. A viewer can confuse it with the narration caption just below (visible in scene-09 at 24.30 s). Fix: DSL. Make the slate label a Paper tag, or shorten to "FIXED CUE".
7. **Inch scale and empty upper stage, scenes 05, 07, 08, 12, 13.** Inch is about 11% of frame width and the stage is empty above y 0.30. Matches the bible (a minimal desk-top stage) but weakens hierarchy. This is a creative preference, not a defect.
8. **Doc mismatch.** storyboard.md says the floor strip is at y 0.81, but rendered frames show the floor edge at about y 0.64, matching the style bible. Fix the storyboard text.

## Passed checks
- Hook: clear myth promise at frame 0, no number (myth hook type, which the bible allows). Sentence is 8 words. Chip is visible. No title card.
- Story works muted: problem (cross on battery), study (card), fix (3 numbered slates), caveat, try-it note.
- Colour-blind rule: coral cross (scene-02) and mint checks (scenes 06-11) are never colour-only.
- Character: Inch (snail) is consistent in shell, colour and scale across all stills. Feet sit on the floor line. No broken poses or merged objects seen.
- Safe zones: chip at about y 0.11, captions at 0.70, all text within x 0.06-0.84. No cropping. No banned phrases ("proven" appears only as "not proven", as a limit statement).
- Claim accuracy vs idea.md: "2015 paper, six studies, 2,274 people, better self-control relied more on habits, reported less effort holding themselves back" matches the abstract. "Linked, mostly self-reported" is the stated limit. Habits-link-to-outcomes is not overclaimed, and causation is not asserted.
- Loop: scene-15 returns to the hook layout with the battery replaced by a checked cue note. The last line "Try it today..." is not a sign-off.

## Could not verify
- Actual audio-to-caption alignment inside segments (no word timings; I did not listen).
- Voice intelligibility, SFX level against narration, and SFX sync (only levels and silences measured).
- Motion smoothness and transition quality (only stills and the contact sheet were reviewed; I did not step through video frames).
- Per-scene Inch pose on every scene at full size (only scenes 01 and 09 were viewed full size).
- 1080x1920 final render. Draft only.
- The primary-source text itself. I relied on idea.md's note that it was verified via PubMed, and did not re-fetch it.
