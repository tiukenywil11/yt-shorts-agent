# Reference Analysis: Improvement Pill and Psych2Go (for the "small habits, explained by science" channel)

Protocol: `docs/creative/REFERENCE_ANALYSIS.md`. Strategy context: `docs/business/MONETIZATION_STRATEGY.md` (Pillars, Formats, Series, Risks only).
Analysis date: 2026-11-06. Machine-readable version: `creative/patterns.json`. Gaps and decisions: `creative/open-questions.md`.

Legend: **O** = observation, **E** = evidence (file id + timestamp), **I** = interpretation/hypothesis, **C** = confidence (high/medium/low). Ids are YouTube ids; filenames are in `references/improvementpill/` and `references/psych2go/` (prefix = view count). Frames and sheets: `references/<channel>/frames/<viewcount>_<id>/` (`contact_sheet.jpg`, `scene_cuts.txt`, sampled `tNNN.NN.jpg`).

Naming: IP = Improvement Pill, P2G = Psych2Go. IP ids: iFIqZNdKpi4 (3.1M, study tips), ov_ceE6_GCE (1.7M, communication), KCSk0_HmMsU (1.3M, motivation), 0zY5BbMHsEY (787K, focus), mdc4SUYKnXM (107K, Parkinson's law), I_1Z6a8kVQM (103K, sleep), box851akjy4 (97K, rat race; transcript only, no video).

## 0. Sample, method, and limits (facts)

- 12 videos analysed on video + transcript; 1 (box851akjy4) on transcript + info.json only. Total n = 13. Small sample; every "pattern" below is a pattern within this sample.
- All mp4s are 360x640 AV1/Opus (not 720p as labelled), 24-30 fps. Good for layout, caption and cadence; not for fine typography or audio judgement.
- Durations: IP 56-60 s (box851akjy4: 48 s); P2G 70-100 s, plus one 24 s promo. All longer than our 30-50 s target. IP uploads are all Feb-Jun 2023; P2G uploads Dec 2025-May 2026 (info.json). View counts are not age-normalised.
- Audio was not listened to. Voice and music character come only from transcripts ("[music]" tags in P2G subs) and are marked low confidence.
- Cut detection: ffmpeg scene filter, threshold 0.25 (stored in `scene_cuts.txt`), plus a 0.1 pass counted for IP. Both undercount IP (it uses fades/pushes and in-scene change) and probably overcount P2G tO505YfXN6Y (continuous camera moves and text sliding). Treat counts as bounds; the contact sheets are the better evidence. 9 of 13 contact sheets were visually reviewed (IP: iFIqZNdKpi4, ov_ceE6_GCE, KCSk0_HmMsU, 0zY5BbMHsEY, I_1Z6a8kVQM; P2G: qGMMA04G5KE, tO505YfXN6Y, LkHi7DN1qcg, PCczfSPUw5E). The rest are described from transcript and cut data only.
- Words per second (WPS) = cleaned subtitle words / (last cue end - first cue start); rolling auto-caption duplicates removed.

### Measured table

| id | channel | views | dur s | like/view | words | WPS | cuts @0.25 | mean shot s @0.25 |
|---|---|---|---|---|---|---|---|---|
| iFIqZNdKpi4 | IP | 3.14M | 57.6 | 8.8% | 222 | 3.73 | 8 | 6.4 |
| ov_ceE6_GCE | IP | 1.74M | 59.7 | 7.1% | 187 | 3.05 | 3 | 14.9 |
| KCSk0_HmMsU | IP | 1.34M | 58.2 | 8.7% | 217 | 3.62 | 5 | 9.7 |
| 0zY5BbMHsEY | IP | 787K | 58.5 | 7.0% | 190 | 3.15 | 0 | n/a |
| mdc4SUYKnXM | IP | 107K | 55.5 | 9.0% | 205 | 3.58 | 2 | 18.5 |
| I_1Z6a8kVQM | IP | 103K | 58.4 | 7.1% | 207 | 3.44 | 2 | 19.5 |
| box851akjy4 | IP | 97K | 48 | 5.1% | 188 | 3.79 | n/a | n/a |
| qGMMA04G5KE | P2G | 420K | 73.6 | 13.4% | 182 | 2.43 | 17 | 4.1 |
| z6MEsqhUV74 | P2G | 197K | 99.5 | 6.5% | 257 | 2.54 | 5 | 16.6 |
| 8hsCMw-KxH4 | P2G | 75K | 81.4 | 5.7% | 266 | 3.20 | 22 | 3.5 |
| PCczfSPUw5E | P2G | 67K | 88.1 | 5.9% | 212 | 2.35 | 30 | 2.8 |
| LkHi7DN1qcg | P2G | 62K | 87.7 | 10.1% | 211 | 2.40 | 33 | 2.6 |
| qzsdeNEMtFw | P2G | 58K | 24.0 | 3.6% | 55 | 2.30 | 0 | n/a |
| tO505YfXN6Y | P2G | 31K | 69.6 | 7.2% | 175 | 2.47 | 68 | 1.0 (unreliable) |

IP at threshold 0.1: 8/6/10/10/19/14 cuts for I_1Z6a8kVQM, mdc4SUYKnXM, KCSk0_HmMsU, ov_ceE6_GCE, iFIqZNdKpi4, 0zY5BbMHsEY, giving mean shot ~2.9-7.9 s. Visually, new imagery appears roughly every 2.5-5 s in IP sheets (e.g. iFIqZNdKpi4 t=0-57 changes nearly every sample at 2.4 s spacing).

Summary stats: IP WPS 3.05-3.79 (mean 3.5); P2G WPS 2.30-3.20 (mean 2.5, excluding the promo 2.5). IP is about 40% faster narration.

## 1. Channel promise and audience

### IP: "one actionable idea per Short, framed as a secret or study-backed trick"
- O: Titles and openers promise a how-to or a shortcut ("tips you haven't heard of", "the secret"). Audience is self-improvement/students (study, focus, motivation, communication, sleep, money). E: iFIqZNdKpi4 0-4 s; ov_ceE6_GCE 0-4 s; descriptions in info.json (newsletter/"mini-course" link in ov_ceE6_GCE and box851akjy4).
- I: A direct problem→method channel. Closest to our target format. C: high.

### P2G: "psychology explainers and self-recognition lists"
- O: Mix of named-concept explainers (Lima syndrome, rare phobias), "signs you ..." lists, and reassurance pieces. Ends often invite self-identification. E: LkHi7DN1qcg 79-88 s ("which of these do you see in yourself"); 8hsCMw-KxH4 77-83 s; PCczfSPUw5E 83-88 s.
- O: One upload is a channel promo for a live workshop (qzsdeNEMtFw), not content.
- I: Identity and curiosity driven, less "do this tomorrow". C: high for description, medium for audience.

## 2. Repeated story structures

| Structure | Where | Confidence |
|---|---|---|
| Promise in sentence 1, then numbered steps ("first / second / third" or "tip #1-#3"), then stop | IP: I_1Z6a8kVQM, iFIqZNdKpi4, 0zY5BbMHsEY, box851akjy4 (3 numbered items each) | high (4 of 7, all with explicit numeric markers on screen) |
| Single claim + analogy/anecdote + conclusion | IP: ov_ceE6_GCE (baby learns language by observation → "get more practice"), KCSk0_HmMsU (worked example then moral), mdc4SUYKnXM (personal anecdote) | high (3 of 7) |
| Named concept: define → why surprising → causes/points → human reflection | P2G: qGMMA04G5KE (4 causes then reflection), z6MEsqhUV74 (7 items) | medium |
| Numbered "signs/habits" list with identical card per item | P2G: LkHi7DN1qcg, 8hsCMw-KxH4 | medium |
| "Different X, different fix" branching, with a caveat for conditions where advice fails | P2G: PCczfSPUw5E 21-80 s | low (one-off, but notable) |

- I: IP structures are closest to problem→fix. P2G's "different cause, different fix" and its stated limits (PCczfSPUw5E 74-83 s, "just start advice often backfires") are the only built-in guardrail behaviour in the sample.
- Neither channel has a closing "try it today" line. IP ends on a statement or a generic follow line; P2G on a reflective question or reassurance. See section 11.

## 3. Hook patterns (first ~2 s, words + visual)

| id | spoken (short) | visual | type |
|---|---|---|---|
| iFIqZNdKpi4 | "tips you probably haven't heard of" | persistent top title + character holding a blank board, question marks by ~5 s | curiosity/novelty promise |
| ov_ceE6_GCE | "reveal ... the secret" | title + illustrated scene, big numeral "1" at 5 s | secret promise |
| KCSk0_HmMsU | question about internal locus of control | large yellow "?" over dark background 0-5 s | question |
| 0zY5BbMHsEY | "slave of these technologies" | "You are a slave" lettering at 5 s, character in chains by 5 s | provocative metaphor |
| mdc4SUYKnXM | "I figured out a way to hack ..." | n/a reviewed | personal claim |
| I_1Z6a8kVQM | "follow the instructions ... within 10 to 15 minutes" | "3 things", speech bubble "10-15 min" within 2.4 s | outcome promise + number |
| box851akjy4 | "one of the only feasible methods" | no video | exclusivity |
| qGMMA04G5KE | "Lima syndrome. This is when the captor ..." | title card on blank sheet 0-3 s, then character cards | named term |
| LkHi7DN1qcg | "Ever catch yourself doing something weird ... is something wrong with me?" | blank pink 0-3 s then character | self-recognition question |
| PCczfSPUw5E | "Instead of asking what should I be doing" | title chip "Laziness isn't what you think" + character in bed | reframe |
| tO505YfXN6Y | "Have you ever tried a dopamine detox?" | night scene, character at desk | question |
| 8hsCMw-KxH4 | "Are you having trouble deciding if your friend is a real friend?" | n/a reviewed | question |
| z6MEsqhUV74 | prevalence stat, then "seven rare but very real phobias" | n/a reviewed | stat then list |

- O: Every IP hook starts talking on frame 0 (first cue 0.00-0.08 s in all seven) and states the promise/number inside 4 s. P2G starts at 0.0-0.16 s as well, but several visuals open on near-empty frames for 2-3 s (qGMMA04G5KE 0-3 s blank title sheet; LkHi7DN1qcg 0-3 s plain pink).
- I: IP front-loads the payoff; P2G front-loads curiosity or identity. For retention at 70%+, IP's number+outcome in the first sentence is the safer pattern. C: medium.
- Hypothesis (unsupported by data): questions hooks and curiosity hooks are common in both channels because they are cheap to write, not because they win. We have no per-hook retention data.

## 4. Scene count and duration distribution

- IP: about 14-30 distinct visual beats in a 58 s video (sheet-based eyeballing; detector undercounts). Typical beat 2.5-5 s. Each beat is either a title card/keyword slate (numeral + 2-4 word label, 2-3 s) or a simple illustrated action (3-5 s). E: iFIqZNdKpi4 7-10 s ("Tip #1 use sounds"), 19-21 s ("Tip #2"), 33-36 s ("The final tip").
- P2G: beat length depends on the video. LkHi7DN1qcg and PCczfSPUw5E about 2.6-2.8 s per cut; qGMMA04G5KE has long holds (t=21-37 s almost one static composition with slow push) then fast cards at 40-70 s. z6MEsqhUV74 only 5 cuts at 0.25 (probably long continuous animation or dissolves). C: medium (detection noise).
- Interpretation: both mix "slate beats" (text-led) and "scene beats" (character acting). For our engine this maps to a small set of reusable scene types (see section 13).

## 5. Visual style and composition

IP (O): A persistent top-of-frame title banner in a heavy hand-drawn display face stays on screen for the whole video (iFIqZNdKpi4, ov_ceE6_GCE, KCSk0_HmMsU, 0zY5BbMHsEY, I_1Z6a8kVQM; all sampled frames). Below it, a roughly square-ish illustration panel (not full-bleed) on a single flat colour field; the panel changes background colour per beat in iFIqZNdKpi4 (peach, pink, teal, yellow, lilac, red, green, white, blue) but stays one colour in 0zY5BbMHsEY (pale yellow) and I_1Z6a8kVQM (green). Captions sit in the lower third in a dark semi-transparent bar. Illustration is thin-line sketch with spot colour, minimal shading, white or grey figures with a single accent colour. A lot of empty space below the panel (visible in 0zY5BbMHsEY and I_1Z6a8kVQM). C: high.
- I: This is a "stock explainer" look that is cheap to produce and uses vertical space inefficiently. The persistent title makes the video self-explanatory even when scrubbed; likely helps search/relevance. C: medium (hypothesis).

P2G (O): Full-bleed vertical illustration. Style varies by video: flat bright colour with a blank-bodied mascot (LkHi7DN1qcg), soft rounded kawaii palette (PCczfSPUw5E), painterly/gradient lighting (tO505YfXN6Y), dim cinematic staging with a pinboard motif (qGMMA04G5KE). A recurring mascot with a leaf-sprout head appears in all five sampled videos (qGMMA04G5KE, tO505YfXN6Y, LkHi7DN1qcg, PCczfSPUw5E; plus the promo). Key points appear on rigid "card/book page" overlays (qGMMA04G5KE 52-62 s) or a repeated list-item template (LkHi7DN1qcg: same office-scene card at 14, 25, 40, 51, 62, 73 s). C: high for the mascot and card patterns; medium for "style varies by production team" (hypothesis: multiple artists).
- I: P2G visual quality is higher and more varied, with a consistent character as brand glue. Production cost per second is clearly higher than IP. Not replicable at our scale; the mascot concept is transferable only as "one recurring original character", never their character.

## 6. Camera language

- IP (O): almost none; flat panels, slow push on some slates, objects pop in. Rare "wipes" or crossfades (I_1Z6a8kVQM at 7.3 s shows a crossfade ghost frame). E: iFIqZNdKpi4, I_1Z6a8kVQM 7.32 s. C: medium.
- P2G (O): more camera: slow pans/pushes (qGMMA04G5KE 9-37 s), close-up crops on the character (tO505YfXN6Y 11-20 s, partial face cropped by frame edge), zoom into the brain/prop (qGMMA04G5KE 46-49 s). Text sometimes sliding in-scene so letters cut off at frame edge (tO505YfXN6Y 14-20 s, 35-60 s). C: medium.
- I: Both rely on simple moves; camera complexity is not what separates top from low performers within either channel. C: low-medium.

## 7. Character movement and expression

- IP: simple expressive faces (eyebrows, mouth, "?" bursts) on a generic figure; props do the explaining (a lightbulb equals candle with a green check, a thermometer, a dog with a treat). Several different characters per video rather than one mascot (iFIqZNdKpi4 uses at least four figures). E: iFIqZNdKpi4 0-57 s; I_1Z6a8kVQM 14-53 s. C: high.
- P2G: one mascot with strongly readable body language (slump, hug, tired face, celebrating with headphones at the end of tO505YfXN6Y 58-67 s). Emotion is central. E: LkHi7DN1qcg 3-25 s; PCczfSPUw5E 0-25 s. C: high.
- I: For a faceless science-of-habits channel, IP's "prop does the explaining" is the more transferable approach for Money (coins, jar, calendar). P2G's emotive mascot suits Mind pillar content. C: medium (hypothesis).

## 8. Animation timing and transitions

- IP: hard cuts and quick numeric slates; element pop-ins aligned to keywords ("Tip #1", "2 WAYS", check mark, red cross at iFIqZNdKpi4 55 s). Captions change roughly every 2-2.5 s. C: medium-high.
- P2G: dissolves and push-ins; key-points held on screen with words appearing line-by-line. Karaoke-style word highlight in PCczfSPUw5E (green highlight on current word, all of 7-88 s). C: medium.
- Visual-to-narration sync: key terms appear on screen within roughly 0.5-1 s of being spoken (IP slates for "Tip #2" at 19.2 s vs "second tip" speech at ~19 s). C: medium.

## 9. Typography and captions

| | IP | P2G |
|---|---|---|
| Persistent title | yes, heavy display font, 2 lines, top | no (small chip in PCczfSPUw5E first 8 s only) |
| Caption | boxed lower-third, sentence case, 2 lines, all videos | mixed: none in several (qGMMA04G5KE, LkHi7DN1qcg), word-highlight karaoke in PCczfSPUw5E, in-scene hand lettering in tO505YfXN6Y |
| Keyword treatment | coloured hand-lettered slates ("Tip #1"), accent word in red/blue | card with bold slab text, "You ..." list titles |

- O: Subtitles are burned into IP in every sampled video. Several P2G videos rely on the platform captions. C: medium (subtitle style may differ on-platform).
- I: Persistent topic title + boxed caption is the simplest copyable accessibility pattern. We should keep our own typography. C: medium.

## 10. Narration, music, sound

- WPS: IP mean 3.5, P2G mean 2.5. The faster IP pace gives about 190-220 words for 58 s. For our 30-50 s target that is about 100-175 words at 3.0-3.5 WPS. C: high for the measurement.
- Voice: both appear as a single narrator (no dialogue) in the transcripts. IP uses first person ("I've been using", "I found") in 0zY5BbMHsEY, mdc4SUYKnXM; P2G uses second person and "we" with an editorial tone. C: medium.
- Music: P2G subs mark "[music]" in 5 of 7 (qGMMA04G5KE 43 s; tO505YfXN6Y 9-33 s, 50-62 s; LkHi7DN1qcg 22-75 s; z6MEsqhUV74 70 s). IP subs carry no music tags, but that proves nothing. SFX not assessed. C: low; audio not reviewed.

## 11. Retention devices, payoff, CTA, loop

- Retention devices observed: numeric roadmap ("3 things", "1/2/3" slates); curiosity gap ("something most people don't know"); mid-video micro-payoffs per step; name a thing ("The Locus Rule" in the description of KCSk0_HmMsU); visual metaphor with a green check/red cross for do/don't (I_1Z6a8kVQM 36 s, iFIqZNdKpi4 55 s). C: medium-high.
- CTA: only 2 of 7 IP include a closing line, and it is generic ("follow us for more helpful tips", mdc4SUYKnXM 53 s, box851akjy4 44 s). The others end abruptly on the last step (I_1Z6a8kVQM ends on a single word at 58 s; 0zY5BbMHsEY mid-analogy). P2G ends with a reflective question (LkHi7DN1qcg), reassurance (PCczfSPUw5E) or a workshop invite (qzsdeNEMtFw). None says "try it today". None loops visually. C: high.
- I: The explicit "try it today" ending and a loopable closing frame are not copied from either; they are our own differentiators. Hypothesis, untested: a concrete micro-action is stronger than abstract wrap-up lines. C: low.

## 12. Citations and evidence (key finding)

- O: Neither channel puts a source on screen in any sampled frame. Spoken attributions are vague: "Huberman recommends" (iFIqZNdKpi4 ~10 s, a named person but no paper), "studies have found" (iFIqZNdKpi4 ~42 s), "they found" (KCSk0_HmMsU ~4 s), "studies show" (LkHi7DN1qcg ~17 s), "experts suggest" (tO505YfXN6Y ~56 s). Visual "evidence" is metaphor icons (a molecule diagram appears in iFIqZNdKpi4 at 45 s, no numbers or authors). C: high for "no on-screen citations in the sample".
- I: A visible named study + sample size/limit on screen is a real differentiator against both channels. It also helps with the "inauthentic content" risk in the strategy. C: medium (hypothesis; no audience-response data).

## 13. Variations and outliers

- IP: 0zY5BbMHsEY has 0 detected cuts at 0.25 but obvious beat changes (fixed pale yellow background). mdc4SUYKnXM is a personal anecdote, not a method (closest to build-in-public, 107K views). box851akjy4 is the only money item and has the lowest like/view (5.1%) and views (97K).
- P2G: qzsdeNEMtFw is a promo, exclude from performance conclusions. z6MEsqhUV74 (rare phobias) is list trivia, not a habit. tO505YfXN6Y shows heavy text-in-scene and the lowest content views (31K).

## 14. Channel comparison

### What each does that associates with views

IP (n=7). Top three (3.14M, 1.74M, 1.34M) vs lowest three (107K, 103K, 97K):
- O: Top three are all broad, high-search self-improvement topics (study, communication, motivation). The bottom three are sleep, a Parkinson's-law anecdote and a money topic. Hook type differs (novelty/secret/question vs outcome promise/anecdote/exclusivity). Length, WPS (3.05-3.73 vs 3.44-3.79) and visual style are indistinguishable. Like/view is similar (7.1-8.8% vs 5.1-9.0%).
- I: Differences in views most plausibly come from topic breadth and title-search demand, not editing craft. The one money video is the lowest performer; n=1 and not age-matched, so no conclusion. C: low-medium.
- O: iFIqZNdKpi4 and 0zY5BbMHsEY (both Feb 2023) beat the June 2023 uploads; upload age is a confound.

P2G (n=7, 6 content). Top: qGMMA04G5KE 420K (13.4% like/view) and z6MEsqhUV74 197K. Bottom content: tO505YfXN6Y 31K, LkHi7DN1qcg 62K, PCczfSPUw5E 67K, 8hsCMw-KxH4 75K.
- O: Top performer is a rare named concept with a curiosity gap; the habit-style and advice-style Shorts (dopamine, laziness, signs of intelligence) perform lower. Uploads from Dec 2025 vs Jan-May 2026 differ in age.
- I: Curiosity/novelty topics beat advice topics on P2G, which is the opposite of IP's "how to ..." strength. No cross-channel generalisation is safe. C: low.

### Transferable vs tied to their look

Transferable (to our paper-cutout habits+money channel):
1. Promise or number in the first spoken sentence (IP). C: medium-high.
2. Persistent topic title throughout plus clear numeral slates for steps. C: medium.
3. Boxed caption in lower third, readable at 360 px (IP). C: medium.
4. Slate beats plus acting beats alternation, new visual every 2.5-5 s. C: medium.
5. Prop metaphors for abstract ideas (green check = do, red cross = don't). C: medium.
6. One recurring original character as brand glue (P2G idea only). C: medium.
7. Caveat sentence: "for X, this backfires" (P2G PCczfSPUw5E). C: low-medium; strong match to our guardrails.
8. Closing question/identification prompt (P2G) only if paired with an action. C: low.

Tied to their look and not to copy: IP's thin-line figure style, the heavy title face, pastel panel-on-colour layout; P2G's sprout mascot and its kawaii/painterly sets, card/book overlays, karaoke caption colour, and their scripts.

Pace calibration: IP 3.5 WPS is fast and likely exceeds our TTS target; P2G 2.4-2.5 WPS is easier to follow with stat overlays. Suggest 2.8-3.2 WPS to leave room for the on-screen study card (hypothesis, test in drafts).

## 15. Money pillar relevance

- Only one money sample (box851akjy4, transcript only): states "the system is broken", "virtually impossible to save your way out", "asymmetrical bets" with no sources and no disclaimer. Lowest views and like/view in IP.
- Implication: this style (broad claim, no data, contrarian to saving) violates our Money guardrail (education only, "Not financial advice", no promises). Our Money Shorts should lean on a verifiable stat, a worked number and a repeatable habit. Do not reuse the "escape the rat race" framing. C: medium (n=1).
- Money content on these channels cannot tell us anything about money RPM or topic demand. Not in scope of this sample.

## 16. Patterns to avoid (per strategy guardrails)

| Pattern seen | Evidence | Why avoid |
|---|---|---|
| Absolute outcomes ("never have issues with motivation again") | KCSk0_HmMsU 54-60 s | overstates effect; strategy: don't overstate effect sizes |
| "The secret" framing for one factor | ov_ceE6_GCE 0-4 s, 55-60 s | single-cause claim, no source |
| Generic "studies show / experts suggest" | iFIqZNdKpi4, LkHi7DN1qcg, tO505YfXN6Y | unverifiable; need named study and limits |
| Trait lists that flatter the viewer ("habits that reveal high intelligence") | LkHi7DN1qcg 17-79 s | Barnum-style overclaiming |
| Personal anecdote as evidence | mdc4SUYKnXM 26-50 s | not evidence; ok only as labelled "my experiment" |
| Biology/health claims with no sourcing or limits (cold shower adrenaline, light bulbs, 40 Hz sound) | iFIqZNdKpi4 6-58 s, I_1Z6a8kVQM 14-58 s | medical-claim guardrail (Body pillar) |
| Inflammatory metaphors ("slave of machines") | 0zY5BbMHsEY 0-14 s | tone and advertiser risk |
| Financial framing without caveat | box851akjy4 | no "not financial advice", implied guaranteed route |
| Template-swapped listicles | P2G list cards, IP 3-tip pattern | inauthentic-content policy risk if script reuse |

## 17. Recommended design implications (hypotheses to test, not conclusions)

1. Target 120-160 words at about 3.0 WPS for 40-50 s; budget 2-3 s for the study card.
2. Persistent topic title + step numeral slates + boxed caption.
3. Per Short: one hook sentence with a number or outcome, 1-3 steps, one on-screen study card (author/year/sample, plus a "limit" line), one try-it-today action, loop-friendly last frame.
4. Alternate slate beats and prop-led acting beats every 2.5-5 s.
5. Reuse a single original character and prop set across pillars.
6. For Money: show a worked number (the stat) before the habit; include disclaimer line; no income promises.
7. Test hooks A/B across batches because the sample cannot decide between outcome promise and curiosity gap.
