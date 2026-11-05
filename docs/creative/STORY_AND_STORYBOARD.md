# Story and Storyboard Standard

## Script structure
A Short should have one central idea. Default structure:
1. Hook: create a clear question, contrast, or emotional tension immediately.
2. Setup: establish the situation with minimal explanation.
3. Development: escalate or reveal information.
4. Payoff: resolve the central question.
5. Ending: memorable close or intentional loop.

Avoid filler, unsupported factual claims, and narration that merely describes what is already obvious.

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
