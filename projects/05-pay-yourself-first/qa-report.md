# QA Report: 05-pay-yourself-first (draft.mp4 review, updated for re-rendered final.mp4)

Recommendation: PUBLISH after a quick ear check of scene-05/06 sync. The trailing-footage defect is fixed, and M1 appears fixed on the stills.

## Update (final re-render)
- Trailing footage fixed: the old 0.6 s silent scene-14 (40.8-41.4 s) played after the last sentence and showed a mismatched "SAVE MORE." frame. It was removed, scene-13 was extended by about 0.1 s, and video.durationSec is now 40.9 s. Voiceover ends at 40.80 s.
- final.mp4 was re-rendered with --overwrite after a stills pass of all scenes. `check_video.py --expect final` PASS: 1080x1920, 30 fps, h264/aac, yuv420p, 40.92 s, clean decode.
- M1: the new stills show scene-05 with ENROLLED AUTOMATICALLY and a check, and scene-06 with PARTICIPATION HIGHER, SIGN UP YOURSELF and a cross, in spoken order. Marked fixed on stills only; sync with the audio was not re-listened.
- m2 is resolved by removing scene-14. The video no longer ends on a loop frame.
- Not verified: the final MP4 was not watched or listened to in full. This section reflects the stills contact sheet and the scripted checks.

## Original review (draft.mp4, 360x640 / 15 fps, 41.41 s)

## Technical (check_video.py --expect draft)
PASS on all checks: 360x640, 15 fps, h264, yuv420p, aac, 41.41 s, full decode clean.
Audio: silencedetect found only natural pauses (12.82-13.37, 34.53-34.98, tail 40.75+). Peak -3.5 dB, no clipping. No black frames on the contact sheet. Not verified: I did not listen to the audio, and sync was checked only against silence gaps and scene timings.

## Critical
None.

## Major

### M1. (FIXED on stills, see update) scene-05 / scene-06: captions and visuals are in the reverse order of the narration (clarity, storytelling)
- Evidence: script seg-03 is "When new hires were enrolled ... automatically, participation was significantly higher than when they had to sign up themselves." The pause ends at 13.37, so scene-05 (13.3-17.2) carries the "When new hires were enrolled ..." audio.
- Scene-05 instead shows the caption "Participation was significantly higher than when they had to sign up themselves", the SIGN UP YOURSELF tag and a red cross.
- Scene-06 (17.2-21.25) shows "ENROLLED AUTOMATICALLY", a green check and "PARTICIPATION HIGHER" while the narrator says "...than when they had to sign up themselves."
- Effect: the viewer hears "auto-enrolled" while seeing a red cross on sign-up, then hears "sign up" while seeing a check. This is the core evidence of the video, so a muted viewer or a viewer following the captions gets a muddled comparison.
- Likely cause: the scene text split reorders the clauses. Caption text and visuals were authored as "sign-up first, auto second" instead of following spoken order.
- Smallest fix (DSL, animation.json only):
  - Scene-05: caption "When new hires were enrolled in a savings plan automatically," with the ENROLLED AUTOMATICALLY tag and check.
  - Scene-06: caption "participation was significantly higher than when they had to sign up themselves." with PARTICIPATION HIGHER first, then the SIGN UP YOURSELF tag and cross.
  - No re-synthesis is needed, because the split time at about 13.3 already matches the audio.
  - If the original visual order is kept, the script and audio would have to be reordered instead.
- Confidence: high on the order mismatch (script text plus silence gap). Re-check the exact word boundary by ear after the fix.

## Minor

### m1. scene-04 cite card (8.88-12.38): card timing
- The card enters 0.1 s after the narrator says "A 2001 study", which is good. It shows 3.5 s, which is enough to read at final resolution. Its attribution and "one study, one company" limit are present and the tag reads NOT FINANCIAL ADVICE.
- The card's finding line "AUTO-ENROLL, MORE JOINED" shows about 8 s before the narrator says it, and the card is gone by 12.4, before the finding is spoken. This is a spoiler, and the limit line leaves before the claim is made.
- Fix (DSL): after M1, reduce the card finding to "Madrian & Shea, 2001" and "one study, one company" only, or re-show the card briefly in scene-06. Optional.
- Also: the red limit-dot sits about 60 px left of its text (scene-04-limit-dot, DSL x offset, or the cite_card.svg asset).

### m2. (RESOLVED, scene-14 removed) scene-14 (40.8-41.4): loop frame
- The last frame ("SAVE MORE.", jar with coins) is a good caption-to-hook continuation, but it does not return to the hook layout as idea.md promises.
- At frame 0 the "ON AUTOPILOT" tag is present and the wallet is overlapped by the jar.
- At the end the tag is gone, and the jar covers the wallet label ("WALLE" is clipped).
- Fix (DSL): shift the scene-14 jar x by about 0.04 and add the ON AUTOPILOT tag, or accept the difference as a creative choice.
- The last 0.6 s is silent, which is fine for a loop.

### m3. Hook (scene-01, 0-2.85 s)
- "Saving on autopilot may help you save more." makes a clear but generic promise. The hedge is correct. Whether it is strong enough is a taste call, not a defect. The "ON AUTOPILOT" tag and the jar support it.

### m4. Small labels (scene-03, scene-09, scene-14)
- The WALLET and SEPARATE labels are tiny. They sit on the floor edge and are partly covered by the jar, and the two-line caption "SEPARATE ACCOUNT" crowds the WALLET label at 27.7 s.
- Fix (DSL): move the labels or enlarge them. This is lower priority because they are redundant with the narration.

### m5. Study scope
- The narration says "savings plan" and the card says "auto-enroll", but the steps use a bank transfer to a separate account. idea.md notes that this is untested (a plausible analogue only).
- "A practical way to try this" is correctly hedged, and the caveat covers "one study, one company". Optionally add "workplace plan" to the scene-12 caveat tag. Script change, optional.

## Passes
- Guardrail language: "may help", "results may differ for you", "This is not financial advice". No percentages or product names. The caveat scenes (scene-11/12, 31.1-37.1) show ONE STUDY / ONE COMPANY / NOT FINANCIAL ADVICE in sync with the audio.
- The NOT FINANCIAL ADVICE tag is on every scene from the cite card onward. It is absent from scenes 1-3 by design, since the claim is hedged there.
- Steps 1/2/3 show numbered badges in time with the narration, and the CTA note "TRY IT TODAY" lands at 37.15.
- Character (Inch the snail) is consistent, poses are intact, and there are no cropping or safe-margin issues. Caption highlight is readable.
- Caption-to-narration sync is good except for M1 (scenes 1-4 and 7-14 line up with segment starts to within one scene).
- Transitions are clean, with no blank frames.
