# Story and Storyboard Standard

## Script structure
A Short should have one central idea. Default structure:
1. Hook: create a clear question, contrast, or emotional tension immediately.
2. Setup: establish the situation with minimal explanation.
3. Development: escalate or reveal information.
4. Payoff: resolve the central question.
5. Ending: memorable close or intentional loop.

Avoid filler, unsupported factual claims, and narration that merely describes what is already obvious.

## Trend scorecard (predicted, out of 10)
Score the script before Gate 1 and log the total in `idea.md`. Compare it with real numbers later.
- **Hook /3:** frame 0 and sentence 1 open a question or surprise. 0 = states a hedged conclusion.
- **Hold /3:** new information or a visible change every few seconds; no lecture block or caveat stretch.
- **Share /2:** viewers have a side to take or someone to send it to.
- **Look /1:** the hero object reads at feed size and changes state.
- **Packaging /1:** the title creates tension and the video pays it off.

Below 7: rewrite the hook or change the format before asking for approval. Channel rules: `creative/style-bible.md` > Story and pacing.

## Script segment fields
- `id`
- `text`
- `startSec`
- `durationSec`
- `emotion`
- `delivery`
- `visualIntent`

## Storyboard scene fields
- `id`
- `startSec`
- `durationSec`
- `narrationSegmentIds`
- `purpose`
- `background`
- `characters`
- `props`
- `actions`
- `camera`
- `onScreenText`
- `sfx`
- `transitionOut`

## Visual storytelling
- Prefer an action, reaction, or visual metaphor over a static explanatory shot.
- Make the story understandable with audio muted.
- Give each scene one dominant visual idea.
- Do not add movement without communicative purpose.
- Ensure the visual payoff matches the promise made by the hook.

## Timing
The storyboard timeline must be continuous unless a deliberate pause is specified. Narration duration should be based on the actual generated voice track after TTS, not only word-count estimates. Reconcile scene timing after voice generation.
