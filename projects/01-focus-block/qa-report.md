# QA Report: focus-block (draft gate)

Verdict: FIX FIRST. No critical issues. The story is clear muted, and the problem is shown before the fix. Three major issues should be fixed before the preview render.

Technical: check_video.py --expect draft passed all checks (360x640, 15 fps, h264, yuv420p, aac, 37.95 s, clean decode). No black frames were seen in the contact sheet or in the extra frames.

Audio measured with ffmpeg: integrated -23.4 LUFS, true peak -4.1 dBFS, LRA 1.9 LU. Silence at 16.99-17.52 s (beat before step 1) and 37.17-37.95 s (end tail). There is no clipping.

## Major

1. Audio level is low (whole file, audio).
   - Evidence: -23.4 LUFS integrated, peak -4.1 dBFS. Shorts are normally mixed around -14 LUFS. Mobile playback will sound quiet.
   - Fix: audio. Normalise the mix to about -14 LUFS with a true peak of -1.5 dBFS or lower.
   - Note: SFX levels and timing are not verified beyond the cues present in the DSL. Re-check after the mix is raised.

2. The hook at frame 0 is weak (scene-01, 0-3.2 s).
   - Evidence: At 0.0 and 1.6 s the top 60% of the frame is empty. The clock does not appear until about 3.2 s. The only hook is the caption "EVERY TIME". Nothing moves visually in the first second.
   - Fix: DSL. Start the clock and a switch cue (phone alert badge pulse) at frame 0 to 0.3 s, and move the props or Inch higher or larger. Moving the clock's appear time to 0 is the smallest change.

3. The "MIND · FOCUS BLOCK" pill overlaps the clock (scene-02, about 8.0 s).
   - Evidence: At 8.0 s the pill sits lower than at other times and touches the clock and the coral cross.
   - Related: the pill y-position wobbles between scenes (8.0, 27.2 and 36.8 s differ from the standard position).
   - Fix: DSL. Pin the pill to one fixed y in every scene. Move the clock and tally up, or out of the pill band, in scene-02.

## Minor

4. Caption word spacing is tight or merged (scene-06 and scene-08).
   - Evidence: "ATWENTY-MINUTE" at 19.2 s and "INANOTHER" at 22.4 s read as merged words. "THOUGHTPOPS" at 24.9 s is similar.
   - Cause: probably the caption renderer's word gap or the font's word spacing.
   - Fix: engine. Increase the word gap in the caption component. A DSL caption padding option, if one exists, may do it.

5. Cite card source line is small at 360 px (scene-03, 8.0-11.0 s).
   - Evidence: "Rubinstein et al., 2001 · J Exp Psych" and "Limit: lab tasks" are only about 8 px tall. "SWITCHING = SLOWER" is legible.
   - Hold: the card is visible from about 8.2 s to just under 11.2 s, roughly 2.8 s. That is inside the 2.5-3.5 s target.
   - Fix: DSL or asset. Scale the card up about 15%, or enlarge the source line in cite_card.svg.

6. Leftover pink bar and a mostly empty frame (scene-03 to scene-04, about 11.2 s).
   - Evidence: a faded pink bar fragment is visible and Inch is very small. This is a transition remnant.
   - Fix: DSL. Check the exit timing of the scene-03 elements.

7. Floating "20 MIN" label with no visible timer, and a speck (scene-06 end, about 20.8-22.4 s).
   - Evidence: the 20.8 s frame shows only the "20 MIN" text and a small speck at 22.4 s. The ice-cube timer is present, but the label drifts mid-air for about 0.7 s.
   - Fix: DSL. Anchor the label to the cube or shorten the label's hold.

8. The caveat beat is weak (scene-09, 28-33 s).
   - Evidence: the plan says "Inch skeptical", but Inch looks neutral. The "LAB TASKS" and "SOME JOBS SWITCH FAST" tags are tiny, about 8 px.
   - Fix: DSL. Use a skeptical pose if one is registered, and enlarge the tags.
   - Content: the wording is honest and has no guardrail issue.

9. Loop frame differs from the hook (scene-10, 37.8 s).
   - Evidence: the final frame has the book, a smaller phone and the laptop, but no red alert badge and no caption. The hook shows the badge.
   - Fix: DSL. Match the end layout to the scene-01 layout, including the badge.

10. Try It Today beat.
    - Evidence: the note slaps in at about 33.6 s, after the 0.4 s pause, and the check mark and ice-cube-gone are visible. It reads fine.
    - Fix: none required. Stamp SFX alignment is unverified.

## Checked and OK

- Step slates 1, 2 and 3 (about 17.5-25.5 s). Numbered circles with labels "PICK ONE TASK", "PHONE FACE DOWN" and "LATER LIST" are legible, and each is held while its step is narrated.
- Problem shown before the fix. Switching is shown in scenes 01-04, then the focus-block steps in scenes 06-08.
- Guardrail wording. The claims are scoped to "lab study" and "Limit: lab tasks", with a caveat beat. No overclaims found.
- Caption sync looked acceptable on the sampled frames. It is not frame-verified.

## Already known (not re-reported)

- Plain floor in the bottom third.
- Inch's cheer pose has no body change.
- phone_facedown is drawn upright.
- No music bed.
- The "++++" tally reads as plus signs.
