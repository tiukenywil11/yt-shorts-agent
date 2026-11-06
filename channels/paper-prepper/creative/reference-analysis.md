# Reference Analysis: GroundNUp Shorts (8-video sample)

Protocol: `docs/creative/REFERENCE_ANALYSIS.md`. Goal: reusable structure, pacing, hook, camera, format. NOT their characters, scripts, logos, or compositions.

## 0. Inventory and evidence base
All media is in `references/groundnup/`. Frames and contact sheets are in `references/groundnup/frames/<dir>/`. Frame dir names are the first two `_` tokens of the filename, so ids containing `_` are truncated (`1356365_IcQs2`, `19560930_yBd26x`, `2471557_XGquWa`).
Contact sheet convention: `contact_sheet.jpg` = 7 columns, one frame per 2.5 s, row-major; tile k is at t = (k-1)*2.5 s. Individual frames `s_NNN.jpg` are at t = (NNN-1)*2.5 s. Full-res extras: `full_tSSS.jpg` (SSS = seconds). Below, "sNN" means sample frame NN of that video's sheet.

| Prefix | Title | Dur (s) | Uploaded | Views | Like % | Age (d)* | Avg views/day |
|---|---|---|---|---|---|---|---|
| 21521310 | Snowdrift -> Igloo | 69.2 | 2026-10-28 | 21.5M | 2.43 | 9 | 2.39M |
| 19560930 | Hole -> Bunker | 73.0 | 2026-10-16 | 19.6M | 1.88 | 21 | 0.93M |
| 2522980 | Tree -> Treehouse | 67.3 | 2026-10-30 | 2.52M | 1.37 | 7 | 360K |
| 2471557 | Hole in yard -> Bank vault | 78.1 | 2026-10-19 | 2.47M | 1.62 | 18 | 137K |
| 1356365 | Hole -> Underground city | 66.2 | 2026-10-27 | 1.36M | 1.15 | 10 | 136K |
| 1276296 | Pile of dirt -> Castle | 74.2 | 2026-10-22 | 1.28M | 1.14 | 15 | 85K |
| 101751 | Pile of wood -> Trojan horse | 69.5 | 2026-11-04 | 102K | 1.75 | 2 | 51K |
| 68105 | Gorge -> Hidden hospital | 64.0 | 2026-11-03 | 68K | 3.05 | 3 | 23K |

*Age relative to 2026-11-06; assumes the counts were scraped at file mtime (2026-11-06), unverified. Channel followers (info.json): 58,100. Fields read from `.info.json`: view_count, like_count, comment_count, upload_date, duration, tags, description, channel_follower_count. No chapters on any video.

Technical (ffprobe): all 720x1280, 60 fps, AV1 video, AAC 44.1 kHz stereo ~128 kbps. Audio mean volume is -16.9 to -17.0 dB and peak -1.7 to -3.5 dB on all 8 (consistent with a loudness-normalized master or platform processing; cannot tell which).
Transcripts are YouTube auto-captions (rolling duplicates), so wording may contain ASR errors.

Method limits: I viewed the contact sheets for all 8 and 5 full-res frames, not every frame. I cannot hear audio. Scene detection: ffmpeg `select='gt(scene,0.3)'` found 0 cuts in 7 videos and 1 in the bunker (43.08 s). Raw lists: `frames/<dir>/scene_cuts.txt` and `scene_cuts_0.08.txt`.

---
## 1. Channel promise and audience
- Observation: every title is "How a X Becomes a Y" (or "From a hole in the yard to a Y"). Descriptions repeat "The [thing] started as a [humble start]. Every part after that fixed one problem, right down to [detail]." (1276296, 1356365, 21521310 descriptions). Tags: "how things work animation", "from the ground up" plus topical survival/history terms.
- Interpretation: promise = "watch a trivial starting object become a recognizable complex structure through forced problem-solving, and learn why each part exists." Audience is curious generalists (survival, engineering, history); no prior knowledge needed (19560930 0:25-0:27 explains why field pipes look like candy canes).
- Confidence: high (observation), medium (audience).

## 2. Repeated story structure
Observation (all 8 transcripts):
1. Hook sentence "If you [humble action], you have a [X]." (section 3).
2. Loop: "But [problem]. So you [fix]. This is a [term]." 5-7 explicit "But"s per video (castle 6, city 5, bunker 6, igloo 6, vault 5, Trojan 7, treehouse 6, hospital 5).
3. Each fix creates the next problem, e.g. bunker: door shut -> no air (0:13-0:16) -> pipe -> rain falls in -> gooseneck (0:20-0:25) -> needs fan -> power dies -> crank -> blast overpressure -> blast valve (0:44-0:53) -> blast door (0:57-1:06) (19560930 .srt).
4. Named-term reveals ("This is a ..."), 1-6 per video.
5. A surprising real-world tie-in: "candy canes" (19560930 0:27), "basement feels cool in summer" (1356365 0:24), toilet empties into moat (1276296 1:04), "real bank robbers come in broad daylight" (2471557 0:49).
6. Payoff: "Add [leftover list]. Congratulations, you have built a [X]." in 6 of 8 (castle 1:10-1:15, city 1:01-1:04, bunker 1:06-1:11, igloo 1:05-1:08, vault 1:13-1:17, treehouse 1:01-1:05).
- Interpretation: one repeatable problem-solution escalation template; the subject is swappable.
- Confidence: high.

## 3. Hook patterns (first ~4 s)
Observation: first sentence is always a 2nd-person conditional that completes between 3.0 and 4.9 s:
- Igloo "If you dig a hole in a snowdrift to hide from a blizzard, you have an igloo." (21521310.srt 0:00-0:04)
- Bunker "If you dig a hole in your yard and put a roof over it, you have a bunker." (19560930 0:00-0:04)
- Castle (1276296 0:00-0:03), vault (2471557 0:00-0:04), city (1356365 0:00-0:04), treehouse (2522980 vtt 0:00-0:03.9), hospital (68103 vtt 0:00-0:04.3), Trojan (101741 vtt 0:00-0:04.9).
The first "But" lands within ~0.1-0.5 s of the hook ending. Frame at t=1 s (`21521310_EmJqO41Wx2A/full_t001.jpg`): a worker mid-action at a rough dome, caption word already on screen, falling snow. No title card, no logo intro, no silence.
- Interpretation: the hook promises an absurd reduction ("a hole = a bunker") and the first "But" immediately breaks it, creating the question "how does that get fixed?" Stakes (blizzard, enemies, money, being lost) appear in the first clause in most videos.
- Generic vs distinctive: the "If you X you have Y" conditional is a known explainer device; using it identically on every video is this creator's signature.
- Confidence: high (pattern), low-medium (that the hook drives views).

## 4. Scene count and duration distribution
Observation: each video is essentially one continuous in-engine take, not an edit of shots. Cut detection at 0.3: 0 in 7 videos; bunker 1 (43.08 s, a whip-pan). At 0.08: castle 0, treehouse 0, city 1 (19.3 s), igloo 1 (63.1 s), vault 1 (8.55 s), Trojan 1 (24.95 s), bunker 3 (43.08-43.57 s), hospital 3 (0.02, 44.5, 46.0 s). Lighting transitions (dusk in igloo sheet s14-s19) and camera moves are continuous.
Beat structure (from transcripts): roughly 8-14 problem-fix beats per video; typically 4-6 s early and 2-4 s late (bunker 0:44-1:06). Total 64-78 s.
- Interpretation: model a Short as narrated beats in one persistent set that accumulates objects, with a camera re-frame per beat, not as separate edited scenes. Caveat: the detector misses smooth camera moves, so reframing counts are not measured.
- Confidence: high for "no hard cuts", medium for beat counts (derived from transcripts, not frame-labelled).

## 5. Visual style and composition
Observation (contact sheets, all 8): real-time-style 3D render (PBR-looking materials, soft sun/overcast, volumetric fog in forest and gorge, particles for smoke/water/snow). Presentation is a vertical-slab cutaway ("ant-farm" cross-section) with soil/rock strata below ground and structure above (19560930 s01-s05, 2471557 s01-s05, 21521310 all, 1356365 all, 2522980 lower edge). Characters are small, near-faceless mannequin figures in one saturated colour (orange hi-vis, red jacket with yellow beanie, red tunics with gold helmets) against muted environments.
Palettes: igloo icy blue-gray with orange hero and warm lamp glow (21521310 s14-s19); bunker green lawn, brown soil, grey concrete (19560930 s01); treehouse misty green-gray with red hero (2522980 s01); Trojan sand, sky blue, beige brick, red/gold (101751 s01); hospital teal water, gray rock, green fog (68105 s01).
Composition: portrait; subject in the middle ~60 %; sky above and soil below leave clean space. Same suburban backyard backdrop in castle, bunker and vault. Red/orange used for alerts, conduits and laser sight lines; cyan arrows show airflow (bunker s07-s24).
Branding: a small in-world blue "FROM THE GROUND UP" plaque attached to objects (`101751_7Pw3oFewAoM/full_t069.jpg`, `68105_BFAFjbrwggY/full_t062.jpg`, 19560930 s07).
- Interpretation: transferable principle = toy-diorama cutaway, one saturated hero colour, uncluttered. Creator-specific: hi-vis worker, red-beanie figure, blue plaque, backyard backdrop.
- Confidence: high for 3D + cutaway; medium for engine identity (not stated, do not assume).

## 6. Camera language
Observation: slow continuous moves. Push-ins and orbits on the discussed detail (vault door close-ups 2471557 s08-s28); pull-backs to re-establish the whole structure (igloo s21-s24); vertical pans down shafts/pipes (19560930 s09-s11, 1356365 s08-s11); overhead/drone-style opening then ground-level angle in the hospital (68105 s01-s10, s12-s19); occasional whip-pan/motion smear (vault s17, bunker 43.08 s). The camera lands on the object at the moment its word is spoken (gooseneck 0:22-0:25, 19560930 s10-s11). Construction is animated fast while the camera holds, then reframes to the finished component; no sped-up clocks.
- Interpretation: "camera follows narration" with a wide -> detail -> wide rhythm is reusable. The top performers (igloo, treehouse) use less camera movement (mostly locked side view) than the vault or hospital, so camera complexity does not correlate with views here.
- Confidence: medium-high.

## 7. Character movement and expression
Observation: characters are small mid-ground figures doing one legible action per beat (cutting blocks, kneeling, climbing, rolling off a branch 2522980 s03, standing on the dome 21521310 s25-s27). Faces are not readable at sampled size; emotion is carried by pose and props. Cast size: igloo, city, treehouse about one hero; bunker, vault and castle almost no people; Trojan soldiers and hospital stretcher teams are groups. Animals used for scale/humor (1356365 s17-s20).
- Interpretation: characters are scale/context props; the structure is the star. The two top videos have the fewest people.
- Confidence: medium (faces not inspected at full-res).

## 8. Animation timing and transitions
Observation: objects appear via fast procedural animation (blocks stack, walls rise, pipes extend, doors swing) synchronized to the spoken noun. State changes use environmental cues: rain, snow, dusk dimming, smoke puffs, lamp glow, airflow arrows, impact flashes. No wipes or dissolves; transitions are physical (camera moves, light changes) with the 1-3 hard cuts noted in section 4.
- Interpretation: the failure is simulated visibly (roof caving, fire, smoke) before the fix, which makes each "But" visual not only verbal.
- Confidence: medium (2.5 s sampling does not capture fast motion).

## 9. Typography and captions
Observation: white bold rounded sans-serif with dark stroke/shadow, one word at a time, centered, near mid-screen (about 52 % down in `21521310_EmJqO41Wx2A/full_t001.jpg`; higher or lower in other tiles as the composition changes). Size varies between words (small "Beach", "Gets", "A"), perhaps a pop animation or emphasis; cannot confirm. Term labels in ALL CAPS ("PORTCULLIS" 1276296 s25, "TOILET" s28, "TIME LOCK", "RELOCKER" 2471557, "ROLLING STONE DOOR" 1356365, "CAMOUFLAGE" 68105 s07). Numeric callouts with units, white or yellow (40 PIGS, 3 FT, 2 FT, HOUR 3, 8 AM, 55F vs 95F, -40F, 1,000 LB). Hospital s21 shows first names carved on rock (see section 12).
- Interpretation: word-by-word captions are a general Shorts convention; "term label + measured number" callouts are generalizable to our DSL.
- Confidence: high (word-by-word), medium (positions).

## 10. Narration, music, sound effects
Observation: one stereo AAC track per video. Narration speed 3.1-3.5 words/s (castle 3.13, city 3.29, bunker 3.53, igloo 3.31, vault 3.41, Trojan 3.29, treehouse 3.34, hospital 3.24) over 205-273 words per video, computed from deduplicated auto-captions divided by last cue end (which can overshoot media duration by up to ~2 s, so true rates may be up to ~0.1 higher). Silencedetect at -35 dB found short gaps (0.3-0.4 s) only in the igloo (23.2, 25.9, 27.8 s); none in Trojan or hospital. Audio is therefore nearly continuous.
Cannot determine: voice (human/TTS, gender), whether music or SFX exist, mix balance. I did not listen.
- Interpretation: ~200 wpm, one idea per sentence, no breathing room.
- Confidence: high on speed; unknown on music/SFX.

## 11. Retention devices and payoff
Observation:
- Constant open loops: each "But" is a micro-cliffhanger resolved 2-4 s later (5-7 per video).
- Something new appears on screen roughly every 2-5 s.
- "That is why..." facts (about 6 of 8).
- A counter-intuitive twist late: buried igloo gets warmer (21521310 0:53-1:01); time lock locks out the owner (2471557 0:44-0:47); water erases footprints (68103 0:21-0:26).
- Ending: "Add [list]. Congratulations, you have built a [X]." (6/8).
- Possible loop design (hypothesis): the Trojan captions end mid-sentence at ~1:07 ("tears down the wall that nobody could", 101741 vtt), which would loop into the opening line about walls that "can't be broken"; the hospital ends "...find your hospital again." (68103 vtt). Both lack the "Congratulations" line. The last Trojan frame (`full_t069.jpg`) shows a smoke cloud at the gate and no caption. Alternative explanation: auto-caption truncation. Cannot be resolved from stills.
- Confidence: high for "But" loops and Congratulations ending in 6; low for loop-design hypothesis.

## 12. Variations and outliers
- Vault (78 s, 273 words) and bunker are the most mechanically dense and both performed strongly, so length near 75-78 s is not penalized in this sample.
- Igloo and city add temperature/number interjections as "science beats".
- Hospital 68105: shortest (64 s), fewest words (205), 5 "But"s, no "Congratulations", many characters, overhead opening, abstract/grim hook ("lay the wounded on the rocks"). A mid-video non-sequitur ("Every one subscriber carves their name into the cliff", ~0:49) with a name list on rock at 50 s (68105 s21) looks like a subscriber-recognition gimmick; the caption may be an ASR garble. Lowest views/day but highest like rate (3.05 %).
- Trojan 101751: most "But"s (7), longest hook (4.9 s), mythological subject, no "Congratulations".
- Treehouse: slapstick fall at 0:03-0:06.

### Top vs newest comparison
| Dimension | Top performers | Newest 2 (Trojan, hospital) | Confidence |
|---|---|---|---|
| Age | 7-21 days | 2-3 days | Major confound; cannot compare totals. |
| Avg views/day | 85K-2.4M | 51K and 23K | Low: early-days velocity is unknown, and 23-51K/day is not far below the lower-mid tier (castle 85K/day averaged over 15 days). |
| Payoff line | "Congratulations, you have built a X" in 6 of 6 of the top 6 | absent in both | Fact: high. Effect on views: low (hypothesis). |
| Subject | DIY/survival objects (igloo, bunker, treehouse, vault) | myth/war hospital | Low-medium (castle and city are historical yet 1.3M). |
| Cast | 0-1 hero | groups | Low-medium. |
| Hook length | 3.0-4.1 s | 4.3-4.9 s | Low. |
| Camera | locked side cutaway or object close-ups | overhead/dynamic (hospital) | Low. |
| Like rate | 1.1-2.4 % | 1.75 % and 3.05 % | Engagement among viewers is not weaker; suggests age/distribution rather than quality. Medium-low. |
Bottom line: this sample cannot support strong claims about what underperforms. The one clean, observed difference is the missing closing formula and a more abstract subject; everything else is weakly evidenced.

## Generic vs creator-distinctive (do not copy)
Generic genre conventions (reuse): problem-solution chain; cutaway cross-section diorama; one saturated hero colour; word-by-word captions; ALL-CAPS term labels and unit callouts; "that's why..." factoid; narration-following camera; fast narration; a closing summary sentence; 60-80 s length; almost no cuts.
Distinctive to GroundNUp (avoid): the literal "If you ... you have a ..." opener plus "Congratulations, you have built a ..." closer on every video; "This is a [term]" cadence verbatim; the orange hi-vis worker and red-beanie hero; blue "FROM THE GROUND UP" plaque; suburban backyard backdrop; their specific fact sequences (gooseneck/blast valve, time lock/relocker, etc.); subscriber-name gimmick; the "How a X Becomes a Y" title formula. Use our own title, hero design, branding, backdrop and closer.
