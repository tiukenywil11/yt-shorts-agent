# Viral Audit: Episodes 1-7 (2026-11-08)

**Status: prediction, not data.** No `analytics.md` exists for any episode. Ratings are editorial judgement from scripts, storyboards and stills contact sheets; the final MP4s were not watched or listened to. Replace these with real numbers via `analytics-reviewer` once episodes have 1,000+ views and 7+ days live.

## Ratings

Scorecard: Hook /3, Hold /3, Share or comment trigger /2, Look /1, Packaging /1. Definitions: `docs/creative/STORY_AND_STORYBOARD.md`.

| Ep | Topic | Hook | Hold | Share | Look | Pack | **Now** | After fixes |
|---|---|---|---|---|---|---|---|---|
| 06 | Snooze button | 2 | 1.5 | 1.5 | 0.5 | 0.5 | **6.0** | 8.0 |
| 03 | Motivation vs discipline | 1.5 | 1 | 1.5 | 0.5 | 0.5 | **5.0** | 7.0 |
| 07 | Emergency kit | 1.5 | 1.5 | 1 | 0.5 | 0.5 | **5.0** | 7.0 |
| 01 | Focus block | 1.5 | 1.5 | 0.5 | 0.5 | 0.5 | **4.5** | 6.5 |
| 02 | Night wind-down | 1 | 1.5 | 0.5 | 0.5 | 0.5 | **4.0** | 6.0 |
| 05 | Pay yourself first | 1 | 1 | 0.5 | 0.5 | 0.5 | **3.5** | 6.5 |
| 04 | Coin jar | 0.5 | 1 | 0.5 | 0.5 | 0.5 | **3.0** | 6.0 |

As published, none is likely to break out. They are accurate and clean, and they read as lessons rather than feed content. 06 is the one to bet on. "After fixes" assumes a re-cut, and for 04 and 05 assumes the number below survives a full-text read.

## Measured from `script.json`

| Ep | Length (s) | Hook hedged? | Longest segment (s) | Spoken caveat (s) | Share of runtime | "A practical way to try this" |
|---|---|---|---|---|---|---|
| 01 | 39.0 | no | 5.5 | 5.1 | 13% | no |
| 02 | 35.9 | yes | 10.4 | 4.9 | 14% | no |
| 03 | 39.2 | yes | 12.2 | 5.1 | 13% | yes |
| 04 | 42.3 | yes | 12.1 | 6.5 | 15% | yes |
| 05 | 40.8 | yes | 12.2 | 5.8 | 14% | yes |
| 06 | 41.4 | yes | 13.4 | 6.6 | 16% | yes |
| 07 | 40.5 | no | 11.4 | 5.4 | 13% | no |

## Flaws across the channel, by predicted impact

1. **The hook is a hedged thesis.** Five of seven open with "may". "A visible savings goal may help you save more" states the conclusion, softens it, and leaves no question open. The hedge is honest but sits in the worst possible place.
2. **Every episode has the same shape.** Hook, cite card, three steps, caveat, try it today, with the same stage layout. Viewers will recognise it by episode 4, and it edges toward the "same script, swapped nouns" risk that `docs/business/MONETIZATION_STRATEGY.md` warns about.
3. **The finding is delivered as a lecture.** In six of seven, one segment runs 10-13 s, and it names the study's year and design before the result. Retention will sag at 8-20 s.
4. **The caveat comes right before the payoff.** Five to seven seconds of "results may differ" and "not financial advice" sit just before the call to action, giving viewers a natural moment to swipe. "A practical way to try this" adds about 2 s of nothing.
5. **Nothing changes on screen.** No object carries the story. Hero props are about a quarter of the frame width, and the upper stage is often empty. The 96% vs 53% bars in 07 are the only real visual payoff in the batch.
6. **No music.** `audio.music` is `null` in all seven and no music file is in the repo, although the style bible calls for a bed. Only 03 has a sound on its hook. With a flat TTS voice, the opening is very quiet.
7. **The strongest facts were left out.** 02, 04 and 05 stop at the abstract, so they say "longer" and "significantly higher" where a number would be the hook.
8. **Titles repeat the weak hook.** "Does a Visible Savings Goal Help You Save?" is a search query, and Shorts are mostly feed-driven.
9. **No reason to comment or share.** Only 03, 06 and 07 give anyone something to argue with or send to a friend.

## Keep

Real citations on screen, the honest tone, Inch, the paper look, one concrete action, no hype. Those are the differentiators. The fix is the order and weight of these elements, not less honesty.

## Episode fixes

Each stays within what `idea.md` supports. Target 25-35 s.

| Ep | New opening line | Re-cut | Title |
|---|---|---|---|
| 06 | "Thirty minutes of snoozing cost only about six minutes of sleep." | Number first, then the myth stamp, then the comparison. Cut three steps to one rule: decide your window the night before. Limit lives on the card. Pinned comment: snooze or first alarm? | 30 Minutes of Snoozing Cost 6 Minutes of Sleep |
| 03 | "People with better self-control reported trying less." | Lead with the surprise. Drop "2,274" from speech and keep it on the card. One step: a cue plus two minutes. | People With More Self-Control Reported Trying Less |
| 07 | "Nearly everyone had food for three days. Barely half had water." | 96/53 bars on frame 0, drop the 4.6 s opener and the "too big" setup, then water first. | 96% Had Food. Only 53% Had Water. |
| 01 | "One quick text is really two task switches." | Away and back is the insight. Use the melting-timer rebuild already drafted in `theory/projects/01-focus-block-v2`. | One Quick Text Is Two Task Switches |
| 02 | "Same book, same bedtime. On a screen, it took longer to fall asleep." | Split-stage race, paper vs screen. Read the full text for the minutes difference. | Same Book, Same Bedtime. The Screen Lost. |
| 05 | "37% of new hires joined their savings plan. Then 86% did." | Before and after on one stage, then the catch that most never raised the default. | 37% Joined. Then 86% Did. Only the Default Changed. |
| 04 | "Same money, two envelopes, and people saved more." | One jar vs two jars, coin race. | Why Two Envelopes Can Beat One |

**Numbers:** 05's figures are now verified in the full text of NBER Working Paper 7682: 37% (opt-in) vs 86% (automatic enrollment) participation at 3-15 months of tenure. 04's 211 vs 456 rupees (one vs two envelopes, high target) appears only in a secondary summary, so it stays out of the narration until the paper is read.

## Test plan

Change the opening first, since it is the cheapest change and the one the feed reacts to. Compare viewed-vs-swiped between re-cuts and originals on a platform where both can run, one variable at a time. Benchmarks for this metric are creator-reported (commonly 70-80%+) and YouTube publishes none, so the channel's own baseline is the real comparison.
