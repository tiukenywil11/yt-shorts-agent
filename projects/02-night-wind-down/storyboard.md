# Storyboard: Your Bedtime Screen Has a Cost

Channel Small Change Lab | Body | 1080x1920 30 fps | video 36.43 s (voiceover 35.831 s) | 14 scenes

Background: solid Ink `#26303F` (night palette) + `floor_strip` (y 0.81), chip `BODY · WIND-DOWN` on every scene, disclaimer `NOT MEDICAL ADVICE` from scene 4, caption `caption_main` at y 0.70. Hook layout: Inch neutral (0.377, 0.56), phone with jagged Sun glow (0.60). Loop layout: same Inch, open book (0.60) + dim lamp (0.83).

| # | Time | Seg | Beat | Dominant visual | On-screen text | SFX |
|---|---|---|---|---|---|---|
| 1 | 0.00-2.55 | seg-01 | hook | Inch at night beside a phone with a jagged Sun glow; chip BODY, caption states the claim | - | - |
| 2 | 2.55-5.19 | seg-02 | problem | Tired Inch watching the phone; 'ONE MORE VIDEO' then 'ONE MORE SCROLL' pop in | ONE MORE VIDEO; ONE MORE SCROLL | - |
| 3 | 5.19-7.35 | seg-02 | problem | Glow pulses larger, coral cross lands on the phone, a Sky 'Z Z Z' waits in the corner | Z Z Z | problem_bonk.wav |
| 4 | 7.35-10.85 | seg-03 | cite | Cite card held 3.5 s: THE STUDY / Chang et al., 2015 / SLOWER TO FALL ASLEEP / one lab study | THE STUDY; Chang et al., 2015 · PNAS; SLOWER TO FALL ASLEEP; one lab study; NOT MEDICAL ADVICE | paper_rustle.wav |
| 5 | 10.85-13.00 | seg-03 | cite | Coral GLOWING SCREEN bar with cross, glowing phone below | GLOWING SCREEN | problem_bonk.wav |
| 6 | 13.00-15.15 | seg-03 | cite | Mint PRINTED BOOK bar with check, open book below | PRINTED BOOK | paper_rustle.wav |
| 7 | 15.15-18.01 | seg-03 | cite | Tired Inch; Paper tag LESS ALERT NEXT MORNING | LESS ALERT NEXT MORNING | - |
| 8 | 18.01-21.66 | seg-04 | fix | Inch has an idea; dim lamp pops in; step slate 1 DIM LIGHTS, 1 HR BEFORE BED | 1; DIM LIGHTS · 1 HR BEFORE BED | paper_rustle.wav |
| 9 | 21.66-24.05 | seg-04 | fix | Step slate 2; glowing phone pops out, open book pops in with a Mint check | 2; SWAP SCREEN FOR PAPER | paper_rustle.wav |
| 10 | 24.05-28.01 | seg-04 | fix | Step slate 3 SAME ORDER EVERY NIGHT with lamp and book as the fixed routine; Mint check | 3; SAME ORDER EVERY NIGHT | - |
| 11 | 28.01-30.13 | seg-05 | caveat | Skeptical Inch with a Paper tag ONE LAB STUDY | ONE LAB STUDY | - |
| 12 | 30.13-33.12 | seg-05 | caveat | Neutral Inch; Paper tag SLEEP CONDITION? ASK A CLINICIAN | SLEEP CONDITION? ASK A CLINICIAN | - |
| 13 | 33.12-35.83 | seg-06 | try-it-today | TRY IT TODAY note slaps on with stamp thud; cheering Inch beside dim lamp and open book; Mint check | TRY IT TODAY | stamp_thud.wav |
| 14 | 35.83-36.43 | - | loop | Loop frame: hook layout with open book and dim lamp instead of the phone | - | - |

## Notes
- Night palette: solid Ink #26303F background on every scene; Sky/Sun accents only. Body pillar: chip BODY · WIND-DOWN (Sun dot) every scene.
- Disclaimer tag NOT MEDICAL ADVICE from scene-04 (cite card) to the end (scene-14).
- Cite card (scene-04, 3.5 s): THE STUDY / Chang et al., 2015 · PNAS / SLOWER TO FALL ASLEEP / one lab study. No n= and no minutes (unverified, see idea.md).
- Captions are split across scenes at word boundaries proportional to letter count (same method as focus-block). Scene cut points sit at phrase starts; 0.25 s inter-segment gaps belong to the preceding scene.
- Problem (cross_coral scenes 03, 05) before fix (check_mint scenes 06, 09, 10). page_turn only into scene-04. Camera cam_lean_in only on scene-13.
- Loop: scene-14 (0.6 s) = hook layout (Inch neutral, same spot) with phone replaced by open book plus dim lamp.
- New placeholder SVGs: phone_glow, lamp_dim, inch_tired (copy of worry). See asset-requirements.json.
