---
name: setup-renderer
description: Repair or change the Remotion renderer integration (composition, props contract, render adapter, render modes). The renderer is already configured; use this only when the contract must change or rendering is broken.
disable-model-invocation: true
---

# Setup / Repair Renderer

The renderer already exists. Read `docs/technical/ENGINE_CONTRACT.md` first; it has the real composition ID (`Short`), props, and command.

1. Reproduce: `npm run render:short -- --project <a working project> --mode stills`.
2. Look only at the failing layer: `scripts/render.mjs` (adapter), `src/Root.tsx` (metadata), `src/Short.tsx` (timeline), or `engine/registry.json` (modes).
3. Keep the interface stable: `--project`, `--mode stills|draft|preview|final`, `--scenes`, `--overwrite`.
4. Verify with `npm run typecheck`, a stills render, and a draft render whose `check_video.py` result is PASS.
5. Update `docs/technical/ENGINE_CONTRACT.md` if the contract changed.

Don't add a new rendering framework, and don't claim it works until a render has completed and the output file exists.
