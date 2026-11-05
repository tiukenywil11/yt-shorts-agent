# Render and Asset Cache Policy

## Cache keys
Cache each scene using a hash of:
- scene JSON
- referenced asset file hashes
- voice/audio segment hashes that affect the scene
- component/preset implementation version
- renderer version
- render mode and relevant quality settings

## Invalidation
- Script changes: regenerate TTS and scenes whose timing/visuals depend on it.
- Voice changes: regenerate audio mix and scenes with voice-synchronized animation.
- One scene's camera/element change: invalidate that scene and any transition-dependent neighbors.
- Shared character asset change: invalidate scenes that reference that character.
- Music-only change: rebuild audio mix/final composition; do not rerender visual scenes if the renderer supports separate audio muxing.
- Global style change: invalidate only assets/scenes affected by the changed style token or asset.

## Rules
- Never trust filenames alone as cache keys.
- Store hashes and renderer versions in a manifest.
- Keep source files and cached outputs separate.
- Do not reuse a cache entry if its dependencies cannot be verified.
- Prefer deterministic rendering; avoid unseeded randomness.
