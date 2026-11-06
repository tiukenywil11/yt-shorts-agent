# QA Report Final v3 (Gate 4 polish) - focus-block

Verdict: PUBLISH. check_video: all PASS (1080x1920, 30 fps, h264/yuv420p, aac, 39.62 s, clean decode). Audio unchanged from v2, not re-measured.

## Fix confirmation (contact sheet + sampled frames 20.3, 36.9, 39.5 s)
- (a) Caption gap: CONFIRMED. "A / TWENTY-MINUTE", "IN ANOTHER", "TWENTY-MINUTE BLOCK," render with clear word gaps.
- (b) Cite card scene-04 scaled: CONFIRMED, fully in frame, text legible.
- (c) "20 MIN" label above cube scene-08: CONFIRMED.
- (d) Caveat tags scene-11/12 enlarged: CONFIRMED, legible.
- (e) Tally IIII bars scene-02/03: CONFIRMED.
- (f) Loop frame scene-14: CONFIRMED, alert badge present at 39.5 s, matches frame 0.
- (g) Fixed topic chip/captions: CONFIRMED, chip and captions stable across camera_push scenes 07/10/13.

## New issues
- Minor (subjective): captions at ~20 s and ~36.9 s wrap to two lines (short word on top, long hyphenated word below). Not clipped; within frame. Fix via DSL caption split if desired.
- No overlaps, edge clipping, or overflow found.
