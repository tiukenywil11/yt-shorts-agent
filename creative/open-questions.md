# Open Questions and Caveats (reference analysis, 2026-11-06)

Companion to `creative/reference-analysis.md` and `creative/patterns.json`.

## Evidence gaps
1. Audio unreviewed: voice character, music, SFX and mix are not analysed (only "[music]" tags in P2G subs). Needed before choosing TTS voice, music bed and SFX.
2. Video quality: all mp4s are 360x640 AV1 (labelled 720p). Typography and fine animation timing cannot be judged.
3. box851akjy4 (the only money sample) has no video (403). Its visual treatment of money content is unknown.
4. Visual review covered 9 of 13 contact sheets; z6MEsqhUV74, 8hsCMw-KxH4, mdc4SUYKnXM, qzsdeNEMtFw were characterised from transcript/cut data and not from frames.
5. Scene-cut counts are unreliable for both channels (IP uses fades and in-scene change; P2G tO505YfXN6Y uses continuous camera and sliding text). Shot lengths are bounds, not exact.
6. No retention curves, swipe-away rate, CTR or traffic sources. Everything about "what drives views" is an association with view counts only.
7. View counts are not age-normalised. IP uploads span Feb-Jun 2023; P2G Dec 2025-May 2026. Views per day cannot be fairly compared.
8. IP clips are 2023 uploads; "recent" in the brief means the lower-view ones in the set. Current channel behaviour in 2026 is unknown.

## Small-sample caveats
- n = 7 IP, 7 P2G (6 content). A 3-vs-3 comparison of top and bottom performers cannot establish cause.
- Topic breadth, title demand and age confound every craft-based explanation.
- The money conclusion rests on one video and is confounded.
- P2G visual style varies strongly between videos, so "P2G style" is not one thing. Possibly multiple artists/teams.

## Questions for the creative director
1. Length: both channels run 56-100 s; the strategy says 30-50 s. Hold to 30-50 s, or allow up to about 60 s for Money Shorts with a stat card?
2. Pace: IP 3.5 WPS vs P2G 2.5 WPS. Which fits the Kokoro/TTS voice and a stat card? Proposal: 2.8-3.2 WPS, test in drafts.
3. Hook type: outcome-plus-number (IP-like) or curiosity gap (P2G-like) as default? Proposal: A/B across the first batch.
4. On-screen citation format: card with author, year, sample size and one limit line? Where in the timeline (mid, after the problem)? How to stay readable at phone size.
5. Persistent title banner (IP-like): adopt, or keep the channel's own layout? It uses vertical space but helps clarity.
6. Mascot or prop-led? Proposal: one original recurring character plus a prop library, with our own design.
7. Ending: a concrete "try it today" line plus loopable frame. Should the last frame match the first so it loops?
8. Disclaimers: where does "Not financial advice" / "Not medical advice" sit (final 2 s card, caption, or description)?
9. Speaker voice: neutral narrator, or first person "I tried it" for build-in-public Shorts? IP's first-person Shorts (mdc4SUYKnXM, 0zY5BbMHsEY) are not clearly stronger or weaker.
10. Avoid-list: confirm the patterns in reference-analysis section 16 as hard guardrails for scripts and reviews.

## Suggested follow-ups (not done; needs approval or new data)
- Listen to 3-4 clips (voice, music, SFX) or extract loudness/music-presence with ffmpeg.
- Obtain 2-3 more money-topic Shorts (personal finance) for a Money-specific pattern check.
- Pull per-video upload date and view counts again later for views-per-day comparison.
- After the first 8-10 own Shorts, compare our own retention against these hypotheses and update patterns.json.

## Bootstrap (2026-11-06)
Decided in `creative/channel-identity.md`, `creative/style-bible.md`, `creative/asset-registry.json`, `creative/animation-presets.json`.

### Answers to the questions above (provisional)
- Q1 Length: 35-45 s, hard cap 50 s (7 Fixes Later may use 50 s). No 60 s exception.
- Q2 Pace: 3.0 WPS target (2.8-3.2), 105-135 words. Measure on the first TTS draft.
- Q3 Hook: alternate outcome+number and myth/curiosity across batch 1; log the type in idea.md.
- Q4 Citation: index card with tab / source / finding / limit line, held 2.5-3.5 s after the problem beat. Full citation in the description and idea.md.
- Q5 Title: a small persistent pillar chip + 3-5 word title top-left, not a heavy banner.
- Q6 Character: one original mascot (Inch, a paper snail) + prop library.
- Q7 Ending: "Try it today" + TRY IT TODAY note; the last 0.5 s returns to the frame-0 layout.
- Q8 Disclaimers: on-screen tag from the cite card to the end, plus description, pinned comment, About page.
- Q9 Voice: neutral second-person narrator; first person only in 30-Day Log.
- Q10 Avoid-list: adopted as hard guardrails (style bible > Guardrail language).

### Assumptions (confirm or override)
B1. Audience 18-35, English, US first.
B2. Palette: 7 core + 4 pillar tints. Paper Prepper props are used as-is in Ready (cocoa ink tones); recolor by hex swap only if they clash in stills.
B3. Paper Prepper SVGs, bg cutaways and 3 SFX wavs are reusable (verified under `projects/fallout-shelter/assets/`). Tuck, the READY stamp and the PP badges are retired.
B4. Narration: Kokoro `am_michael`. The brief says 1.15x but `projects/fallout-shelter/script.json` and `projects/blackout-house/script.json` record `speed: 1.25`. Which value is canonical?
B5. Font stays the registry default (Arial Black) until a bundled font exists.
B6. Loudness target about -14 LUFS / -1 dBTP; no measuring script verified.
B7. SVG filters are not used because renderer support is unverified. Test one in stills if texture is wanted.

### Decisions needing the creator
D1. RESOLVED 2026-11-06: channel name is Small Change Lab. Still open: handle, domain and USPTO checks before public launch.
D2. RESOLVED 2026-11-06: mascot is Inch the paper snail.
D3. Voice: keep `am_michael` for brand continuity with Paper Prepper, or pick a different Kokoro voice so the new channel sounds distinct. Confirm speed (B4). Decide when the creator's own voice is used (30-Day Log long-form).
D4. Music source and license.
D5. Whether a 7-step 7 Fixes Later fits in 50 s at 3.0 WPS (test in the first draft; fallback 5 fixes).

### Proposed NEW engine presets/components (proposals only; NOT in `engine/registry.json`; do not use in plans)
P1. Screen-space UI layer (camera-independent) for the pillar chip, disclaimer, caption and fix counter.
P2. Word-level caption timing from TTS timestamps, plus `emphasizeWords`.
P3. `CitationCard` composite component {tab, source, finding, limit} with a fixed layout (replaces 6 hand-placed elements).
P4. `StepSlate` composite {numeral, label}.
P5. `count_up` text preset (number tween with prefix/suffix and format) for The Numbers. Workaround: 2-3 static values across beats.
P6. `grow_y` / `reveal_wipe` enter preset (scale from the baseline, or a mask wipe) for bars and drawing on the growth curve. Workaround: `slide_in_up`.
P7. Persistent elements across scenes (`carryForward`). Workaround: redeclare with preset `none`.
P8. Element `drop_shadow` param. Workaround: baked SVG shadows.
P9. Bundled font loading (rounded heavy OFL display font).
P10. Particle shapes (coins, checks) and palette arrays.
P11. Shared repo-level asset library resolution in the validator/renderer.
P12. Scripts (not engine): first/last-frame loop-match check on stills; loudness measurement; WPS check from script.json.
P13. 16:9 composition variant for long-form (strategy, scoped separately).
