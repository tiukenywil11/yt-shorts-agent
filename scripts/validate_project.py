#!/usr/bin/env python3
"""Validate a Short project against the Animation DSL and engine/registry.json.

Dependency-free. Exit 1 on errors. Run before every render; render.mjs runs it automatically.
"""
from pathlib import Path
import argparse, json, math, sys

from _media import REGISTRY_PATH, load_registry, resolve_inside, tool, duration_sec

TOP_KEYS = {"schemaVersion", "video", "audio", "scenes"}
VIDEO_KEYS = {"id", "title", "width", "height", "fps", "durationSec"}
AUDIO_KEYS = {"voiceover", "music", "voiceVolume", "musicVolume"}
SCENE_KEYS = {"id", "startSec", "durationSec", "background", "camera", "elements", "sfx", "transitionOut", "notes"}
ELEMENT_KEYS = {"id", "type", "component", "asset", "startSec", "durationSec", "transform",
                "content", "preset", "loop", "exit", "params", "notes"}
TRANSFORM_KEYS = {"x", "y", "scale", "rotation", "opacity", "layer", "fixed"}
EPS = 0.001


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, msg): self.errors.append(msg)
    def warn(self, msg): self.warnings.append(msg)


def load(path, r, required=True):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        if required:
            r.err(f"Missing file: {path.name}")
    except json.JSONDecodeError as exc:
        r.err(f"{path.name}: invalid JSON at line {exc.lineno}, column {exc.colno}")
    return None


def check_keys(obj, allowed, where, r):
    for k in obj:
        if k not in allowed:
            r.err(f"{where}: unknown field '{k}'.")


def check_asset(project, rel, where, r):
    if rel is None:
        return
    p = resolve_inside(project, rel)
    if p is None:
        r.err(f"{where}: asset path '{rel}' must be relative and stay inside the project.")
    elif not p.is_file():
        r.err(f"{where}: asset not found: {rel}")


def check_param(spec, value, where, project, r):
    t = spec.get("type")
    if t == "number" and not num(value):
        r.err(f"{where}: must be a finite number.")
    elif t in ("string", "color") and not isinstance(value, str):
        r.err(f"{where}: must be a string.")
    elif t == "boolean" and not isinstance(value, bool):
        r.err(f"{where}: must be true/false.")
    elif t == "enum" and value not in spec.get("values", []):
        r.err(f"{where}: must be one of {spec.get('values')}.")
    elif t == "poses":
        if not isinstance(value, list):
            r.err(f"{where}: must be an array of {{atSec, asset}}.")
            return
        for i, pose in enumerate(value):
            if not isinstance(pose, dict) or not num(pose.get("atSec")):
                r.err(f"{where}[{i}]: needs numeric atSec.")
                continue
            check_asset(project, pose.get("asset"), f"{where}[{i}]", r)


def check_params(params, specs, where, project, r):
    if params is None:
        return
    if not isinstance(params, dict):
        r.err(f"{where}: params must be an object.")
        return
    for k, v in params.items():
        if k not in specs:
            r.err(f"{where}: unknown param '{k}' (allowed: {sorted(specs) or 'none'}).")
        else:
            check_param(specs[k], v, f"{where}.{k}", project, r)


def validate_element(el, j, scene_id, scene_len, project, reg, ids, r):
    eid = el.get("id") if isinstance(el, dict) else None
    where = f"Element {eid or f'{scene_id}[{j}]'}"
    if not isinstance(el, dict):
        r.err(f"{where}: must be an object.")
        return
    check_keys(el, ELEMENT_KEYS, where, r)
    if not eid or eid in ids:
        r.err(f"{where}: missing or duplicate id.")
    ids.add(eid)

    start, length = el.get("startSec"), el.get("durationSec")
    if not num(start) or not num(length) or start < 0 or length <= 0:
        r.err(f"{where}: startSec/durationSec must be numbers (start >= 0, duration > 0).")
    elif start + length > scene_len + EPS:
        r.err(f"{where}: ends at {start + length:.2f}s, after scene end ({scene_len:.2f}s).")

    comp_name = el.get("component")
    comp = reg["components"].get(comp_name)
    if comp is None:
        r.err(f"{where}: component '{comp_name}' is not registered (allowed: {sorted(reg['components'])}).")
        return
    if el.get("type") != comp["type"]:
        r.err(f"{where}: type '{el.get('type')}' does not match {comp_name} (expected '{comp['type']}').")
    if comp.get("requiresAsset"):
        if not el.get("asset"):
            r.err(f"{where}: {comp_name} requires an asset.")
        else:
            check_asset(project, el.get("asset"), where, r)
    elif el.get("asset") is not None:
        check_asset(project, el.get("asset"), where, r)
    if comp.get("requiresContent") and not (isinstance(el.get("content"), str) and el["content"].strip()):
        r.err(f"{where}: {comp_name} requires non-empty text content.")

    param_specs = dict(comp.get("params", {}))
    for field, category in (("preset", "enter"), ("loop", "loop"), ("exit", "exit")):
        name = el.get(field)
        if name is None:
            continue
        preset = reg["presets"].get(name)
        if preset is None:
            r.err(f"{where}: {field} '{name}' is not a registered preset.")
        elif preset["category"] != category:
            r.err(f"{where}: '{name}' is a {preset['category']} preset; '{field}' needs a {category} preset.")
        else:
            param_specs.update(preset.get("params", {}))
    check_params(el.get("params"), param_specs, where, project, r)

    tr = el.get("transform", {})
    if not isinstance(tr, dict):
        r.err(f"{where}: transform must be an object.")
        return
    check_keys(tr, TRANSFORM_KEYS, f"{where}.transform", r)
    for k in ("x", "y"):
        if k in tr and (not num(tr[k]) or not 0 <= tr[k] <= 1):
            r.err(f"{where}: transform.{k} must be within 0-1 (normalized).")
    if "opacity" in tr and (not num(tr["opacity"]) or not 0 <= tr["opacity"] <= 1):
        r.err(f"{where}: opacity must be between 0 and 1.")
    if "scale" in tr and (not num(tr["scale"]) or tr["scale"] <= 0):
        r.err(f"{where}: scale must be > 0.")
    if "rotation" in tr and not num(tr["rotation"]):
        r.err(f"{where}: rotation must be numeric (degrees).")
    if "layer" in tr and not (isinstance(tr["layer"], int) and not isinstance(tr["layer"], bool)):
        r.err(f"{where}: layer must be an integer.")
    if "fixed" in tr and not isinstance(tr["fixed"], bool):
        r.err(f"{where}: fixed must be true/false (true = screen-fixed, ignores the camera).")


def validate_scene(scene, i, project, reg, scene_ids, element_ids, r):
    sid = scene.get("id") if isinstance(scene, dict) else None
    where = f"Scene {sid or i}"
    if not isinstance(scene, dict):
        r.err(f"{where}: must be an object.")
        return None
    check_keys(scene, SCENE_KEYS, where, r)
    if not sid or sid in scene_ids:
        r.err(f"{where}: missing or duplicate id.")
    scene_ids.add(sid)
    start, length = scene.get("startSec"), scene.get("durationSec")
    if not num(start) or not num(length) or start < 0 or length <= 0:
        r.err(f"{where}: invalid startSec/durationSec.")
        return None

    bg = scene.get("background", {"type": "solid"})
    bg_spec = reg["backgrounds"].get(bg.get("type")) if isinstance(bg, dict) else None
    if bg_spec is None:
        r.err(f"{where}: background.type must be one of {sorted(reg['backgrounds'])}.")
    else:
        extra = {k: v for k, v in bg.items() if k not in ("type", "asset")}
        check_params(extra, bg_spec["params"], f"{where}.background", project, r)
        if bg_spec.get("requiresAsset"):
            if not bg.get("asset"):
                r.err(f"{where}: image background requires an asset.")
            else:
                check_asset(project, bg["asset"], f"{where}.background", r)

    cam = scene.get("camera", {"preset": "static"})
    cam_spec = reg["cameras"].get(cam.get("preset")) if isinstance(cam, dict) else None
    if cam_spec is None:
        r.err(f"{where}: camera.preset must be one of {sorted(reg['cameras'])}.")
    else:
        check_keys(cam, {"preset", "params"}, f"{where}.camera", r)
        check_params(cam.get("params"), cam_spec["params"], f"{where}.camera", project, r)

    tr = scene.get("transitionOut", {"preset": "cut", "durationSec": 0})
    if not isinstance(tr, dict) or tr.get("preset") not in reg["transitions"]:
        r.err(f"{where}: transitionOut.preset must be one of {sorted(reg['transitions'])}.")
        tr = {"preset": "cut", "durationSec": 0}
    else:
        check_keys(tr, {"preset", "durationSec"}, f"{where}.transitionOut", r)
        d = tr.get("durationSec", 0)
        if not num(d) or d < 0:
            r.err(f"{where}: transitionOut.durationSec must be >= 0.")
        elif tr["preset"] != "cut" and d <= 0:
            r.err(f"{where}: {tr['preset']} needs durationSec > 0.")

    elements = scene.get("elements", [])
    if not isinstance(elements, list):
        r.err(f"{where}: elements must be an array.")
        elements = []
    for j, el in enumerate(elements):
        validate_element(el, j, sid, length, project, reg, element_ids, r)

    for k, fx in enumerate(scene.get("sfx", []) or []):
        fw = f"{where}.sfx[{k}]"
        if not isinstance(fx, dict):
            r.err(f"{fw}: must be an object.")
            continue
        check_keys(fx, {"asset", "atSec", "volume"}, fw, r)
        check_asset(project, fx.get("asset"), fw, r)
        if not num(fx.get("atSec")) or not 0 <= fx["atSec"] < length:
            r.err(f"{fw}: atSec must be within the scene (0-{length}).")
        if "volume" in fx and (not num(fx["volume"]) or not 0 <= fx["volume"] <= 1):
            r.err(f"{fw}: volume must be 0-1.")
    return (start, start + length, sid, tr)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("project_dir", type=Path)
    p.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = p.parse_args()
    project = args.project_dir.resolve()
    r = Report()

    try:
        reg = load_registry(args.registry)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Cannot load registry {args.registry}: {exc}")

    animation = load(project / "animation.json", r)
    script = load(project / "script.json", r)
    load(project / "storyboard.json", r)

    if isinstance(animation, dict):
        check_keys(animation, TOP_KEYS, "animation.json", r)
        if animation.get("schemaVersion") != "1.0":
            r.err("Unsupported or missing schemaVersion (expected '1.0').")
        video = animation.get("video", {})
        check_keys(video, VIDEO_KEYS, "video", r)
        for key in ("width", "height", "fps", "durationSec"):
            if not num(video.get(key)) or video[key] <= 0:
                r.err(f"video.{key} must be a positive number.")
        duration = video.get("durationSec") if num(video.get("durationSec")) else None

        audio = animation.get("audio", {}) or {}
        check_keys(audio, AUDIO_KEYS, "audio", r)
        for key in ("voiceover", "music"):
            if audio.get(key):
                check_asset(project, audio[key], f"audio.{key}", r)
        for key in ("voiceVolume", "musicVolume"):
            if key in audio and (not num(audio[key]) or not 0 <= audio[key] <= 1):
                r.err(f"audio.{key} must be 0-1.")
        vo = resolve_inside(project, audio.get("voiceover") or "")
        if vo and vo.is_file() and duration and tool("ffprobe"):
            vo_len = duration_sec(vo)
            if vo_len > duration + 0.05:
                r.err(f"Voiceover is {vo_len:.2f}s but video.durationSec is {duration}s (narration would be cut).")
            elif vo_len < duration - 2.0:
                r.warn(f"Voiceover ({vo_len:.2f}s) ends {duration - vo_len:.1f}s before the video ends.")

        scenes = animation.get("scenes")
        if not isinstance(scenes, list) or not scenes:
            r.err("animation.scenes must be a non-empty array.")
            scenes = []
        scene_ids, element_ids, intervals = set(), set(), []
        for i, scene in enumerate(scenes):
            res = validate_scene(scene, i, project, reg, scene_ids, element_ids, r)
            if res:
                if duration and res[1] > duration + EPS:
                    r.err(f"Scene {res[2]}: ends after video duration.")
                intervals.append(res)

        intervals.sort(key=lambda t: t[0])
        for prev, cur in zip(intervals, intervals[1:]):
            if cur[0] < prev[1] - EPS:
                r.err(f"Scenes {prev[2]} and {cur[2]} overlap (transitions are handled by transitionOut, not overlap).")
            elif cur[0] > prev[1] + 0.05:
                r.warn(f"Gap of {cur[0] - prev[1]:.2f}s between {prev[2]} and {cur[2]}.")
            d = prev[3].get("durationSec", 0) if prev[3].get("preset") != "cut" else 0
            if d and d > min(prev[1] - prev[0], cur[1] - cur[0]) / 2:
                r.err(f"Scene {prev[2]}: transition {d}s is longer than half a neighbouring scene.")
        if intervals:
            if intervals[0][0] > 0.05:
                r.warn("First scene starts after 0 seconds.")
            if duration and intervals[-1][1] < duration - 0.05:
                r.warn("Last scene ends before video duration.")
            if intervals[-1][3].get("preset") not in (None, "cut"):
                r.warn(f"Last scene {intervals[-1][2]} has a transitionOut but no next scene; it is ignored.")

    if script is not None:
        if not isinstance(script, dict) or not isinstance(script.get("segments"), list):
            r.err("script.json must be an object with a 'segments' array.")
        else:
            seg_ids = set()
            for k, seg in enumerate(script["segments"]):
                if not isinstance(seg, dict) or not seg.get("id") or not isinstance(seg.get("text"), str):
                    r.err(f"script.json segment {k}: needs id and text.")
                    continue
                if seg["id"] in seg_ids:
                    r.err(f"script.json: duplicate segment id {seg['id']}.")
                seg_ids.add(seg["id"])
            if not script["segments"]:
                r.warn("script.json has no segments yet.")

    print(f"Project: {project}")
    print(f"Errors: {len(r.errors)} | Warnings: {len(r.warnings)}")
    for item in r.errors: print(f"ERROR: {item}")
    for item in r.warnings: print(f"WARNING: {item}")
    if r.errors:
        sys.exit(1)
    print("Validation passed.")


if __name__ == "__main__":
    main()
