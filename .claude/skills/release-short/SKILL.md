---
name: release-short
description: Render the final MP4 for an approved Short project, verify it, then generate its publishing package (publish.md) with publish-packager. Use after the draft/preview is approved (Gate 3). Never uploads or posts.
model: sonnet
---

# Release Short

Input: project folder (e.g. `projects/05-pay-yourself-first`). Use `python`, not `python3`. Invoking this skill counts as Gate 3 approval of the existing draft/preview only if the user's message says so; otherwise confirm first.

## Preconditions (stop and report if any fails)
- `output/draft.mp4` or `output/preview.mp4` exists.
- `python scripts/validate_project.py projects/<id>` passes.
- `qa-report.md` (if present) has no unresolved critical/major issues. List minor items in the report; do not block.
- If `output/final.mp4` exists, do not overwrite it by default. Overwrite only when the user's invocation says so (e.g. `/release-short projects/<id> overwrite`, "new version", "better version"), which is the explicit instruction CLAUDE.md requires. Otherwise stop and ask.

## Steps
0. Overwrite case only: first copy the old file to `output/archive/final-<YYYYMMDD-HHMMSS>.mp4` (create the folder), confirm the copy exists, then render with `--overwrite`. Never delete the archive. Skip the archive step only if the user says the old version is disposable.
1. `npm run render:short -- --project projects/<id> --mode final` (add `--overwrite` in the overwrite case). Read its PASS/FAIL lines; success = exit 0, `RESULT: PASS`, and `output/final.mp4` exists (confirm with `ls -la`). On failure report the adapter's error and stop; do not package.
2. `python scripts/scene_manifest.py projects/<id> --commit`.
3. Delegate once to `publish-packager` with the project dir. It writes `projects/<id>/publish.md` (titles, description with citation and disclaimer, hashtags, tags, pinned comment, per-platform captions, cover frame, upload checklist).
4. Skim `publish.md`: titles must match the narration in `script.json` and avoid banned phrases in `creative/style-bible.md` (guardrail language).
5. If the project is linked in the topic queue, run `python scripts/topic_queue.py sync`. It sets Produced once `publish.md` exists. Published is manual: only the user marks it (`topic_queue.py set <num> Published`) after uploading.

## Report (brief)
Files created, render command (and the archive path if overwritten), output path and size, check_video result, open minor QA items, and what was not verified (the video was not watched or listened to). Never upload or post; uploading stays the user's action.
