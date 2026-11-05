# Agent Routing

Use the smallest agent set that can complete the task. Do not spawn every agent for routine work.

| Task | Agent | Expected output |
|---|---|---|
| Analyze reference videos | `reference-analyst` | Evidence-backed analysis files |
| Decide original creative direction | `creative-director` | Concise style decisions + creative files |
| Convert script into scenes | `storyboard-architect` | Storyboard and animation plan |
| Modify engine/components | `animation-engineer` | Code changes + checks |
| Inspect renders | `qa-reviewer` | Timestamped defects and fixes |

## Orchestration rules

- Main Claude session owns the workflow and final decision.
- Delegate parallel, bounded work with clear input files and output paths.
- Subagents must not independently redesign the whole architecture.
- Ask for findings, confidence, changed files, and blockers; do not ask for chain-of-thought.
- If a task is deterministic, prefer a script over an agent.
- Use one agent for one responsibility. Avoid multiple agents editing the same files concurrently.
- Do not ask the reference analyst to write scripts or code.
- Do not ask the animation engineer to invent the story or visual identity.
- Do not ask the QA reviewer to make subjective creative changes without explaining the impact.
