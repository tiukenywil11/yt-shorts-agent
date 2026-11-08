---
name: review-short
description: Review a storyboard, stills contact sheet, preview, or final MP4 for storytelling, retention, animation, visual consistency, audio sync, and technical publishing defects.
model: sonnet
---

# Review Short

This is the single visual QA pass per gate. Run it at Gate 3 (preview) and optionally at Gate 4 (final).

1. Technical checks are scripted: `python scripts/check_video.py <mp4> --expect preview|final`. Only escalate to an agent if it passes.
2. Make sure a contact sheet exists (`python scripts/make_contact_sheet.py <mp4>`). Never send individual frames when a sheet will do.
3. Delegate visual inspection to `qa-reviewer` with: project dir, contact sheet path, mp4 path, check_video output. One call.
4. Prioritize critical and major issues. For each one, name the scene ID and the smallest fix (DSL, asset, audio, or engine).
5. Don't recommend changes based only on taste; tie each suggestion to clarity, storytelling, retention, or quality.
5b. Run `python scripts/retention_lint.py projects/<id>` and pass its output to `qa-reviewer`, which reports a labelled "Retention risk" section. Retention risks are predictions: they inform the publish / fix-first call but do not count as critical or major defects.

6. **Optional analytics check (only if asked: `analytics`).** Delegate once to `analytics-reviewer` with the project dir; it reads `analytics.md` (from `templates/analytics.example.md`; no file means "no data yet") and replies only, writing nothing. Report in a few lines; never apply changes automatically.

`qa-reviewer` writes `qa-report.md`. Return a short publish / fix-first recommendation.
