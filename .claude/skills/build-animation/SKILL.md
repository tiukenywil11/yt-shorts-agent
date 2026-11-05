---
name: build-animation
description: Implement or extend reusable 2D Remotion components or motion presets needed by an Animation DSL plan. Use when a plan needs a capability that engine/registry.json does not have.
---

# Build Animation

1. Read the "Adding a capability" section of `docs/technical/ENGINE_CONTRACT.md` (not the whole docs folder).
2. Compare what the plan needs with `engine/registry.json`. Prefer expressing it with existing components and params; add code only if that is impossible.
3. Delegate the bounded change to `animation-engineer`: add the registry entry, implement it in `src/components/` or `src/engine/presets.ts`, and register it in `COMPONENTS`.
4. Make it generic and parameterized. Never hardcode one video's scene.
5. Checks: `npm run typecheck`, `python scripts/validate_project.py <project>`, then `npm run render:short -- --project <project> --mode stills --scenes <scene using it>`.
6. Update the summary in `docs/technical/ANIMATION_DSL.md` if a new component or preset was added.

Don't run a final render unless explicitly asked.
