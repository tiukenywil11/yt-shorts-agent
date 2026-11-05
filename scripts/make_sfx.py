#!/usr/bin/env python3
"""Synthesize simple, original, deterministic paper-Foley SFX (no licensing issues).

  python scripts/make_sfx.py projects/<id>            # create missing SFX listed in asset-requirements.json
  python scripts/make_sfx.py projects/<id> --force    # regenerate

An SFX entry is matched to a recipe by its filename stem (e.g. assets/sfx/paper_rustle.wav).
Recipes: paper_rustle, paper_snip, problem_bonk, stamp_thud, soft_thunk.
"""
from pathlib import Path
import argparse, json, sys, wave
import numpy as np

SR = 44100


def env(n, attack, decay):
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    return a * np.exp(-t / decay)


def lowpass(x, alpha):
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc += alpha * (v - acc)
        y[i] = acc
    return y


def paper_rustle(rng):
    n = int(0.38 * SR)
    out = np.zeros(n)
    for start in (0.0, 0.07, 0.15, 0.24):
        s = int(start * SR)
        m = int(0.12 * SR)
        burst = rng.standard_normal(m) * env(m, 0.004, 0.035)
        burst = burst - lowpass(burst, 0.08)  # high-pass: crinkly
        out[s:s + m] += burst[: n - s] * rng.uniform(0.5, 1.0)
    return out


def paper_snip(rng):
    n = int(0.12 * SR)
    x = rng.standard_normal(n) * env(n, 0.001, 0.012)
    return x - lowpass(x, 0.15)


def problem_bonk(rng):
    n = int(0.32 * SR)
    t = np.arange(n) / SR
    f = 190 * np.exp(-t * 3) + 110
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.09)
    knock = lowpass(rng.standard_normal(n), 0.2) * env(n, 0.0005, 0.01)
    return tone + 0.6 * knock


def stamp_thud(rng):
    n = int(0.42 * SR)
    t = np.arange(n) / SR
    f = 120 * np.exp(-t * 8) + 60
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.11)
    slap = lowpass(rng.standard_normal(n), 0.35) * env(n, 0.0005, 0.018)
    return body + 0.8 * slap


def soft_thunk(rng):
    n = int(0.22 * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * (150 * np.exp(-t * 6) + 80) * t) * env(n, 0.001, 0.05)
    return body + 0.3 * lowpass(rng.standard_normal(n), 0.25) * env(n, 0.0005, 0.01)


RECIPES = {"paper_rustle": paper_rustle, "paper_snip": paper_snip, "problem_bonk": problem_bonk,
           "stamp_thud": stamp_thud, "soft_thunk": soft_thunk}


def write_wav(path: Path, x: np.ndarray, peak_db=-3.0):
    x = x / (np.max(np.abs(x)) or 1) * 10 ** (peak_db / 20)
    fade = int(0.005 * SR)
    x[-fade:] *= np.linspace(1, 0, fade)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project_dir", type=Path)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    req = json.loads((a.project_dir / "asset-requirements.json").read_text(encoding="utf-8"))
    missing = []
    for item in req.get("assets", []):
        if item.get("type") != "sfx":
            continue
        path = a.project_dir / item["path"]
        recipe = RECIPES.get(path.stem)
        if recipe is None:
            missing.append(item["path"]); continue
        if path.exists() and not a.force:
            print(f"skip {item['path']} (exists)"); continue
        seed = sum(map(ord, path.stem))  # stable across runs (unlike hash())
        write_wav(path, recipe(np.random.default_rng(seed)))
        print(f"ok   {item['path']}")
    if missing:
        print("No recipe for:", ", ".join(missing))
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
