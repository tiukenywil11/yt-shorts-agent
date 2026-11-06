# QA Report: focus-block final v2 (af_heart 1.05 voice swap)

Verdict: PUBLISH. No critical or major issues. Minors only.

## Specs
check_video.py (supplied): all PASS (1080x1920, 30 fps, h264, yuv420p, aac, 39.62 s, clean decode). Video 39.61 s vs voiceover 39.01 s: 0.6 s tail (scene-14 loop card, 0.503 s).

## 1. Loudness (ffmpeg ebur128 on final.mp4)
- Integrated -14.2 LUFS (target ~-14): PASS
- True peak -3.4 dBTP (limit -1): PASS
- LRA 1.2 LU, consistent. Raw voiceover.wav sample peak -1.5 dBFS (pre-mix), mean -14.6 dB; no clipping in final.

## 2. Caption sync (script.json vs animation.json)
All 10 segments PASS. Every first caption starts at its segment start (0.00 s offset) and ends at or before the next segment start (ends = segment start + durationSec, or the scene boundary where captions are split).
- seg-02: cap-2a 3.599-5.707, cap-2b 5.707-8.308 (contiguous).
- seg-03: cap-3a/3b/3c 8.308-13.833 (contiguous).
- seg-09: cap-9a 29.307-32.183, cap-9b 32.183-34.634 (ends exactly at seg-10 start).
- seg-10: 34.634-39.007.
Max start error 0.0 s.

## 3. SFX / pop-ins vs storyboard beats
Remapped times sit in the same relative positions in each scene as storyboard.json.
- scene-03 bonk 6.79 s with cross pop-in 6.79 s ("It feels fast, but you keep restarting"; segment words begin 6.10 s): PASS.
- scene-04 paper_rustle 8.36 s, card pop 8.41 s, limit dot 9.05 s: PASS.
- scene-05 bonk 12.24 s with cross; bars 11.71 / 12.61 s; check 13.19 s: PASS.
- scene-07 rustle 16.76, check 16.95; scene-08 rustle 20.33 (= cube pop 20.33); scene-09 rustle 23.68 (phone-down 23.68); scene-10 rustle 26.95 (note pop 26.95): all aligned.
- scene-13 stamp_thud 34.74 = note pop-in 34.74; check/confetti 35.27: PASS.
Note: nouns were checked by timing proportion only, with no word-level alignment available (script.json has segment-level times only). Minor: scene-10 element `scene-10-cube-b` starts at 27.88 s, after the note elements (26.95 / 27.37 s), whereas the storyboard says the ice cube shrinks with the line. It has no pop preset and is probably an existing shrink timing; verify visually if desired.

## 4. Silence / clipping at joins (silencedetect -40 dB, 0.15 s)
Gaps at segment joins: 3.28-3.62, 7.99-8.34, 13.78-14.14, 16.34-16.69, 17.97-18.36, 21.74-22.08, 24.89-25.22, 28.99-29.34, 34.31-34.66 s. They are 0.32-0.39 s each, consistent and within the 0.25 s + natural tail design. None is over 0.4 s; the seg-10 pre-pause is 0.34 s (spec 0.4 s, within tolerance). Intra-segment comma pauses are 0.15-0.35 s. No unexpected dead air and no clipped word edges detected (every segment boundary falls inside a detected silence). The voice starts at t=0 with no leading silence.

## 5. Pace and hook
- 122 words / 39.01 s = 3.13 words/s (about 188 wpm): brisk but within Shorts norm.
- Hook (0-1 s): narration begins on frame 0 ("Every time you switch...", 3.28 words/s in seg-01), Inch/props and caption present at 0 s. PASS.

## Issues
- minor (all scenes, animation.json): the ·-separator in the chip text appears as "MIND · FOCUS BLOCK" when parsed; no mojibake found in the file (grep for "Â" returned 0). No action.
- minor (scene-14): 0.5 s silent tail after narration ends at 39.01 s. Creative loop choice; leave as is.
- minor (seg-03, seg-09): captions are split over scenes with identical text blocks; the split is intentional.

No DSL, asset, audio, or engine fixes required before publish.
