# Context Budget Policy

Claude Code loads root `CLAUDE.md` at session start. Keep it short and stable.

## Three levels of information

1. Always-on: root `CLAUDE.md`; only project-wide constraints and navigation.
2. On-demand: Skills and agent bodies; procedures load when invoked and specialist work runs in isolated context.
3. Deep reference: `docs/` and channel files; read only when a task needs them.

## Rules

- Never paste the full style bible into a prompt. Pass its path.
- Never paste full JSON plans into the main conversation if a validator can summarize them.
- Prefer `python scripts/validate_project.py <project-dir>` over manually reviewing every field.
- Prefer contact sheets over sending dozens of individual frames.
- Summarize subagent outputs in no more than 10–20 bullets unless more detail is required.
- Store decisions in files, not chat history.
- Keep generated artifacts out of always-loaded instructions.
- Avoid duplicating the same rules in CLAUDE.md, skills, agents, and docs. Link to the source-of-truth document.
