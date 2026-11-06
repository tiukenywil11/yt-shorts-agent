# QA Report: focus-block (Gate 4, final)

Verdict: PUBLISH. No critical or major issues. Remaining items are minor polish.

Technical: check_video.py --expect final PASS (1080x1920, 30 fps, h264, yuv420p, aac, 37.91 s, clean decode).
Audio (ffmpeg ebur128): integrated -14.5 LUFS, LRA 1.5 LU, true peak -3.2 dBTP (limit -1). On target, no clipping.

## Draft issues: status
1. Quiet audio (major): FIXED. -23.4 -> -14.5 LUFS.
2. Weak hook (major): FIXED. The props, phone alert badge and caption "EVERY TIME" are on screen at 0.0 s, and the clock arrives by 1.6 s. The top third is still empty at 0 s, but this is a creative choice, not a defect.
3. Pill overlapping the clock (major): FIXED. No overlap at 8.0 s. Pill y still shifts by a few px at about 27.2 and 36.8 s (minor, DSL: pin one y).
4. Merged caption words (minor): NOT FIXED. "ATWENTY-MINUTE" 19.2 s, "INANOTHER" 22.4 s, "TWENTY-MINUTE" 35.2 s still read as joined. Fix: engine, widen the caption word gap.
5. Small cite-card source text (minor): NOT FIXED. The source line is still tiny at contact-sheet scale. Fix: DSL, scale the card up about 15%.
6. Leftover pink bar at the 03-04 transition (minor): partly present. The faded "SWITCH" bar still shows at 11.2 s, but it is now clearly intentional. Acceptable.
7. Floating "20 MIN" label (minor): NOT FIXED. At 20.8 s the label hangs with no cube, and there is a speck at 22.4 s. Fix: DSL, anchor the label to the cube or trim its hold.
8. Weak caveat beat (minor): NOT FIXED. The tags "LAB TASKS" and "SOME JOBS SWITCH FAST" are still small. Fix: DSL, enlarge them.
9. Loop frame mismatch (minor): NOT FIXED. At 37.8 s there is no alert badge and no caption, unlike frame 0. Fix: DSL, add the badge to the final layout. This is a loop-polish item only.

## Cover frame at 6.7 s (checked at 180 px wide)
Readable. The clock, the red cross badge, Inch and the props are clear, and the pill is legible. The "++++" tally does read as plus signs, so it looks like "+" rather than tally marks. It is not confusing, because the clock and the cross carry the idea. Optional fix: draw the tally as strokes in the asset. Minor.

## Checked and OK
Black frames: none seen. Step slates, the guardrail wording ("lab study", "Limit: lab tasks") and the "TRY IT TODAY" payoff are clear. Caption-to-audio sync looked acceptable on the sampled frames and is not frame-verified.
