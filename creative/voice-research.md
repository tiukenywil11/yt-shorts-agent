# Voice Research: Small Change Lab (2026-11-06)

## Brief: what the voice must do
From `style-bible.md` > Identity: audience is English, 18–35, students and early-career workers, **skeptical of hype**. Tone: **calm, curious, precise, lightly warm. Never shaming, never hype.** Pacing target: 3.0 words/s (2.8–3.2). Inch the mascot never talks, so the narrator is the channel's only voice. It should sound like a smart friend reading you one study, not a coach and not an ad.

The current voice is `am_michael`. It was carried over from Paper Prepper (a prepper/disaster channel) and was never chosen for this brand.

## What the research says (evidence is thin, so treat as guidance)
- **Pitch:** lower pitch tends to raise perceived competence and trustworthiness. Higher pitch reads as friendlier and more cooperative ([Voicing Uncertainty, arXiv 2408.08438](https://arxiv.org/pdf/2408.08438)). A Guelph study found low pitch hurt trust only with negative words ([U of Guelph, 2018](https://news.uoguelph.ca/2018/08/women-view-lower-voices-as-less-trustworthy-u-of-g-study-finds)). For a channel that says "a problem, then a fix", a mid-pitch voice is the safe choice.
- **Rate:** results are mixed. Moderate rate with deliberate pauses is preferred for synthetic voices ([U Twente thesis](https://purl.utwente.nl/essays/100878)). Credible synthetic speech was delivered somewhat faster than neutral speech ([HS Düsseldorf](https://opus4.kobv.de/opus4-hs-duesseldorf/frontdoor/index/index/docId/5313)). Our 3.0 w/s target is fast-moderate, which fits Shorts.
- **Prosody beats timbre:** trust impressions rise with clear vocal intent, and they depend on the listener ([trust review, Essex](https://repository.essex.ac.uk/41758/); [conversational-agent trust, BIU](https://cris.biu.ac.il/en/publications/what-makes-a-conversational-agent-sound-trustworthy-exploring-the/)). A natural, clean voice matters more than gender or accent.
- **TTS quality:** Kokoro's own VOICES.md grades training-data quality. `af_heart` is **A** (the best English voice) and `am_michael` is **C+** ([Kokoro VOICES.md](https://huggingface.co/hexgrad/Kokoro-82M/blame/main/VOICES.md)). Lower-graded voices tend to have more artifacts, odd stress and flat endings. Skeptical viewers will hear that.

## YouTube policy notes
- AI voiceover over an original script is allowed and monetizable. The risk is the **"inauthentic content"** policy (renamed 2025-07-15) for mass-produced, templated channels ([Influencer Marketing Hub](https://influencermarketinghub.com/youtube-inauthentic-content); [Typecast](https://typecast.ai/learn/youtube-ai-monetization-july-15-ypp-update/)). One consistent, well-chosen voice plus original animation and cited sources keeps the channel on the "authentic" side.
- Disclosure: sources disagree about whether a generic narration voice needs the "altered or synthetic" label ([AIR Media-Tech](https://air.io/en/youtube-hacks/youtube-ai-disclosure-in-2026-label-it-yourself-or-youtube-will)). Ticking it costs nothing (no reach or monetization effect), so keep ticking it.
- Longer term, a human voice (yours, or a hired voice actor) is the strongest protection against inauthentic-content reviews. Sources consistently say human narration is the safest option.

## Auditions (Kokoro, speed 1.15, same 55-word text)
Files are in `creative/voice-auditions/<voice>.wav`. The text is the focus-block hook, problem, study line and "Try it today". Samples are not loudness-matched, so adjust volume when comparing.

| Voice | Kokoro grade* | w/s @1.15 | Speed for 3.0 w/s | Notes |
|---|---|---|---|---|
| **af_heart** | A | 3.19 | ~1.08 | Top pick. Warm, clean, natural |
| **af_bella** | A- | 3.12 | ~1.10 | Brighter, more energy. Backup |
| am_michael (current) | C+ | 2.97 | ~1.16 | Deeper, authoritative. More artifacts |
| am_fenrir | C+ | 3.52 | ~0.98 | Best male candidate besides michael |
| am_puck | C+ | 3.53 | ~0.98 | Lighter, more playful male |
| bf_emma | B- | 3.41 | ~1.01 | British, calm and precise; best non-US |
| bm_george | C | 3.09 | ~1.12 | British, mature |
| af_nicole | B- | 2.08 | — | Whispery/ASMR delivery and too slow. Wrong for this channel |
| af_sarah, bm_fable, am_eric, am_liam | C+ to D | 3.3–3.9 | — | Included for completeness. Lower grades, rushed at 1.15 |

*Grades are from the Kokoro VOICES.md mirrors as remembered and searched. af_heart's A and am_michael's C+ are confirmed by the search; the others are approximate.

## Recommendation
1. **Default: `af_heart` at speed ~1.08–1.10.** It is the highest-quality local voice. Its warm, mid-pitch, friendly-but-precise sound matches "calm, curious, lightly warm". It also moves the channel away from the Paper Prepper sound.
2. **If you want a male voice: keep `am_michael`** (speed 1.15–1.20, not 1.25: at 1.15 it already hits 2.97 w/s). You could also try `am_fenrir` at ~1.0. Expect slightly more mispronunciations to fix.
3. **Pick one and lock it** in `style-bible.md`. Voice consistency is part of the brand, and switching voices between videos looks like a template farm.
4. **Upgrade path:** once the channel has proven traction, record your own voice or hire a narrator with the same brief (mid pitch, warm, ~3 w/s, no "radio" delivery). Paid TTS (e.g. ElevenLabs) is a middle step, but it adds cost and licensing terms to check.

To apply a choice, set `script.json` → `"voice": {"engine": "kokoro", "voice": "af_heart", "speed": 1.1}` and run `python scripts/tts.py projects/<id> --force`.
