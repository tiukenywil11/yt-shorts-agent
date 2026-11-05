#!/usr/bin/env python3
"""Hash each scene's dependencies and report which scenes changed since the last committed render.

Cache key per scene = scene JSON + bytes of referenced assets + registry + engine source + voiceover.
Music is deliberately excluded (music-only change => final rerender, no scene rework).
Usage:
  python scripts/scene_manifest.py projects/<id>            # report changes
  python scripts/scene_manifest.py projects/<id> --commit   # record current state after a good render
"""
from pathlib import Path
import argparse, hashlib, json

from _media import ROOT, REGISTRY_PATH, resolve_inside


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tree_hash(folder: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(folder.rglob("*")):
        if p.is_file():
            h.update(p.relative_to(folder).as_posix().encode())
            h.update(file_hash(p).encode())
    return h.hexdigest()


def scene_assets(scene: dict) -> list[str]:
    refs = []
    bg = scene.get("background") or {}
    if bg.get("asset"):
        refs.append(bg["asset"])
    for el in scene.get("elements", []):
        if el.get("asset"):
            refs.append(el["asset"])
        for pose in (el.get("params") or {}).get("poses", []) or []:
            if isinstance(pose, dict) and pose.get("asset"):
                refs.append(pose["asset"])
    for fx in scene.get("sfx", []) or []:
        if fx.get("asset"):
            refs.append(fx["asset"])
    return sorted(set(refs))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("project_dir", type=Path)
    p.add_argument("--commit", action="store_true")
    args = p.parse_args()
    project = args.project_dir.resolve()
    plan = json.loads((project / "animation.json").read_text(encoding="utf-8-sig"))

    globals_ = {
        "registry": file_hash(REGISTRY_PATH),
        "engine": tree_hash(ROOT / "src") if (ROOT / "src").is_dir() else "none",
        "video": hashlib.sha256(json.dumps(plan.get("video"), sort_keys=True).encode()).hexdigest(),
    }
    vo = resolve_inside(project, (plan.get("audio") or {}).get("voiceover") or "")
    globals_["voiceover"] = file_hash(vo) if vo and vo.is_file() else "none"

    current = {}
    for scene in plan.get("scenes", []):
        h = hashlib.sha256()
        h.update(json.dumps(scene, sort_keys=True).encode())
        for rel in scene_assets(scene):
            ap = resolve_inside(project, rel)
            h.update(rel.encode())
            h.update((file_hash(ap) if ap and ap.is_file() else "missing").encode())
        for v in globals_.values():
            h.update(v.encode())
        current[scene["id"]] = h.hexdigest()

    manifest_path = project / "cache" / "manifest.json"
    previous = {}
    if manifest_path.is_file():
        previous = json.loads(manifest_path.read_text(encoding="utf-8-sig")).get("scenes", {})

    order = [s["id"] for s in plan.get("scenes", [])]
    changed = [sid for sid in order if previous.get(sid) != current[sid]]
    removed = [sid for sid in previous if sid not in current]
    # Transition neighbours: a change on either side of a non-cut transition affects both scenes.
    affected = set(changed)
    for i, scene in enumerate(plan.get("scenes", [])[:-1]):
        if (scene.get("transitionOut") or {}).get("preset", "cut") != "cut":
            a, b = order[i], order[i + 1]
            if a in changed or b in changed:
                affected.update((a, b))
    affected_list = [sid for sid in order if sid in affected]

    if args.commit:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps({"globals": globals_, "scenes": current}, indent=2) + "\n", encoding="utf-8")
        print(f"Committed manifest for {len(current)} scenes -> {manifest_path.relative_to(ROOT)}")
        return

    if not previous:
        print(f"No manifest yet: all {len(order)} scenes are new.")
    print(f"Changed: {','.join(changed) if changed else 'none'}")
    print(f"Render these (incl. transition neighbours): {','.join(affected_list) if affected_list else 'none'}")
    if removed:
        print(f"Removed since last commit: {','.join(removed)}")


if __name__ == "__main__":
    main()
