---
name: bootstrap-channel
description: Set up a new original animated Shorts channel by analyzing supplied references, defining its style bible, and creating the initial asset/preset registries. Use once per channel or when intentionally refreshing its identity.
---

# Bootstrap Channel

1. Ask for or locate the channel goal, audience, reference media, and production constraints. Do not ask for information already present in project files.
2. Read `docs/creative/REFERENCE_ANALYSIS.md`.
3. Delegate reference inspection to `reference-analyst` when there are multiple independent videos or a large media set.
4. Delegate original style decisions to `creative-director`.
5. Save outputs under `creative/`.
6. Create `creative/asset-registry.json` (reusable characters, props, backgrounds). Motion presets come from `engine/registry.json`; propose new ones in `creative/open-questions.md` instead of inventing them.
7. Record assumptions and unresolved questions in `creative/open-questions.md`.
8. Do not implement the full renderer during channel bootstrap.

Return the created files and a short summary of the channel's creative rules.
