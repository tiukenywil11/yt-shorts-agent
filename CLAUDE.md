# Animation Studio — Claude Code Instructions

## Mission
Produce original, repeatable animated YouTube Shorts using a declarative JSON plan and a reusable Remotion/Three.js engine.

## Read selectively
- Start with `docs/INDEX.md` only when you need to locate a reference.
- Do not load every file in `docs/`.
- For creative tasks, read only the relevant files under `docs/creative/`.
- For DSL/engine work, read `docs/technical/ANIMATION_DSL.md`.
- For rendering/QA, read the relevant file under `docs/production/`.

## Core rules
1. Inspect the repository before changing architecture or dependencies.
2. Reuse registered assets, components, and animation presets before creating new ones.
3. AI output is declarative JSON, never arbitrary executable JavaScript.
4. Validate JSON before rendering. Validate TypeScript after code changes.
5. Use frame-based deterministic animation; avoid wall-clock/random behavior in renders.
6. Keep narration, scene timing, and visual actions synchronized.
7. Render drafts first. Render only affected scenes when possible.
8. Do not invent asset paths, Remotion composition IDs, render commands, or tool capabilities. Inspect the project.
9. Do not copy distinctive copyrighted characters, scripts, logos, or exact compositions from references.
10. Do not claim a render succeeded unless the command completed and the output file exists.

## Cost and context policy
- Delegate independent reference analysis, storyboard review, code review, and QA to specialist subagents.
- Ask subagents for concise findings and artifact paths; do not request their full reasoning.
- Prefer scripts for deterministic tasks (scaffolding, validation, FFprobe, contact sheets).
- Load detailed skill instructions only when the matching workflow is requested.
- Do not re-summarize the entire style bible in every prompt. Refer to its file path and read only the needed section.

## Engine facts
- Allowed components/presets: `engine/registry.json`. Render: `npm run render:short -- --project projects/<id> --mode stills|draft|preview|final`.
- On Windows use `python`, not `python3`. Review stills before rendering any video.

## Default video target
Vertical 9:16, 1080x1920, 30 FPS, H.264 video, AAC audio. Draft: 360x640 at 15 FPS. Preview: 540x960 at 24 FPS. Override only when project config says otherwise.

## Project outputs
Each video lives under `projects/<video-id>/`. Keep source plans, assets, previews, QA reports, and final exports together. Never overwrite a final export without an explicit instruction.

## Completion report
When done, report: files created/changed, validation performed, render command executed, output path, and any unresolved issues. Keep it brief.
