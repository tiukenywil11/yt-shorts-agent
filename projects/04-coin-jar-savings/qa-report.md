# QA Report: 04-coin-jar-savings (draft)

Scope: output/draft.mp4, stills-contact-sheet.jpg, script.json, animation.json, idea.md. Method: contact sheet review, check_video.py, ffmpeg volumedetect/silencedetect. No extra frames sampled, so the findings below come from contact-sheet evidence only.

## Technical: PASS
check_video.py --expect draft: 360x640, 15 fps, H.264 yuv420p, AAC, 42.88 s, full decode clean. Audio peak -3.0 dB (no clipping), mean -17.5 dB, no silence over 0.7 s. No black frames or missing scenes seen on the sheet (14 scenes present).

Note: runtime is 42.9 s against a targetDurationSec of 40 (voiceover 42.27 s). Still fine for Shorts; minor.

## Findings (ranked)

### Critical
None.

### Major
None confirmed. One item that needs a human decision is the first Minor item below (card wording).

### Minor
1. Cite card and tag wording is unhedged. Scenes 04-06 and 10: the card headline "SEE GOAL, SAVE MORE" and the tags "SAVINGS RATE UP" and "SPLIT IN TWO" with green checks state the effect as fact. The idea.md guardrail says to use "may", "linked with" and "one study". Narration is hedged, and the card does carry "one study, low-income consumers", but the headline is causal and unhedged. Fix: change the headline to "SEEING THE GOAL: SAVING MAY RISE" or "SEEN GOAL, HIGHER SAVING RATE". Optionally reword the tag to "SAVING RATE ROSE (1 STUDY)". DSL text change only.
2. Cite card accuracy otherwise OK. "Soman & Cheema, 2011", "one study", "low-income consumers" all match idea.md. No sample size is claimed. No "studies show/proven" language. The narration claims match the abstract: visual reminder raised the savings rate, and splitting into two accounts beat pooling.
3. Guardrail on screen and spoken is OK. NOT FINANCIAL ADVICE is a chip from scene 04 on (absent in scenes 01-03, as designed in idea.md). It is spoken in seg-05 (31.85-38.36 s) with a full-width tag at 36.3-38.4 s. The small chip is tiny at 360x640, so verify legibility at 1080x1920. Fix if it fails: bump the font size or chip contrast (DSL).
4. Tag timing lag in scene-11. The "RESULTS MAY DIFFER" tag appears only at about 36.3 s. The narration "results may differ for you" is spoken at roughly 34.5-36 s, and the 34.20 s frame has no tag. Fix: start the tag about 1.5 s earlier (DSL).
5. Scene-04 caption collision. At 10.20 s the two-line caption "LOW-INCOME CONSUMERS" sits over the cite card and jar bottom, and the snail is hidden by the card. Fix: shift the card up, or shorten the caption to a single line (DSL).
6. Snail and jar scale and pose vary between scenes (snail smaller in scenes 04 and 06, jar size varies). The jar and the snail are present in every scene, so continuity holds. Check whether the size change is intentional. Fix: normalize scale params (DSL). Not a blocker.
7. Loop frame. Scene-14 (42.27-42.88 s, 0.6 s, no VO) shows the labelled jar with photo and a second small jar, as idea.md intends. The jar position and size differ slightly from the hook, and the loop frame has no "ONE PILE" tag or caption. This is acceptable as a payoff. If a seamless loop is wanted, match the hook's jar x/scale. The hook shows an unlabelled jar, so the loop is a "before/after" echo rather than a pixel match. This is a creative choice; flagged only.
8. Pacing. seg-03 (7.9-19.3 s, 11.3 s of narration, scenes 04-06) is the densest stretch with the same layout, so a retention dip is possible. The 0.6 s tail after VO is fine. Optional: add a small motion beat (coin drop, card flip) mid-seg-03.
9. Caption and voice sync spot checks (1.4, 2.6, 4.5, 7.07, 12.27, 15.8, 19.33, 24.2, 31.6, 38.4, 42.07 s) are consistent with script.json segment timings (within about 0.3 s). Scene starts align with segment boundaries (e.g., scene-07 19.523, scene-11 31.848, scene-13 38.605).
10. SFX not verified. animation.json references sfx (about 20 mentions), but audio.music is null and I did not isolate SFX levels. Voice level is healthy (mean -17.5 dB, peak -3 dB). Listen once to confirm coin and check-mark sfx do not mask the voice.
11. Possible text-encoding artifact. The chip text in animation.json reads "MONEY Â· SAVINGS GOAL" in the raw file, while the render shows the correct "MONEY · SAVINGS GOAL". Likely a console decoding artifact; confirm the file is UTF-8 so this cannot corrupt a re-render.

### Safe zones
Chip and tags are at the top (about 11% of the height). Captions are at about 70% of the height, above the bottom UI zone. The cite card and sticker are within margins. No cropping seen.

## Recommended fix order
1. Reword the cite-card headline and the checkmark tags to hedged language (DSL).
2. Move the "RESULTS MAY DIFFER" tag earlier (DSL).
3. Fix the scene-04 caption/card overlap (DSL).
4. Listen-check SFX; verify tag legibility at full resolution.
No asset, audio, or engine changes required.
