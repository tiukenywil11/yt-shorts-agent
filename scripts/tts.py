#!/usr/bin/env python3
"""Free local TTS: synthesize one WAV per script.json segment, then reconcile timing.

Engines (install once; nothing is downloaded by this script):
  piper  (default, fastest, CPU):  pip install piper-tts
         python -m piper.download_voices en_US-lessac-medium --data-dir tools/tts
  kokoro (higher quality, CPU):    pip install kokoro-onnx soundfile
         put kokoro-v1.0.onnx and voices-v1.0.bin in tools/tts/

Segments whose text has not changed since the last run are skipped (sidecar hash), so editing one
line re-synthesizes one line. Writes assets/voice/<segment-id>.wav, then runs audio_timing.py.

Usage: python scripts/tts.py projects/<id> [--engine piper|kokoro] [--voice NAME] [--force]
Voice settings can also live in script.json: "voice": {"engine": "piper", "voice": "en_US-lessac-medium"}
"""
from pathlib import Path
import argparse, hashlib, importlib.util, json, subprocess, sys

from _media import ROOT

TTS_DIR = ROOT / "tools" / "tts"
DEFAULTS = {"piper": "en_US-lessac-medium", "kokoro": "af_heart"}


def synth_piper(text: str, voice: str, out: Path) -> None:
    if importlib.util.find_spec("piper") is None:
        raise SystemExit("Piper not installed. Run: pip install piper-tts")
    model = Path(voice) if voice.endswith(".onnx") else TTS_DIR / f"{voice}.onnx"
    if not model.is_file():
        raise SystemExit(f"Piper voice model not found: {model}\n"
                         f"Run: python -m piper.download_voices {voice} --data-dir tools/tts")
    res = subprocess.run([sys.executable, "-m", "piper", "-m", str(model), "-f", str(out)],
                         input=text, text=True, capture_output=True)
    if res.returncode != 0 or not out.is_file():
        raise SystemExit(f"Piper failed: {res.stderr.strip()[-500:]}")


_kokoro = None


def synth_kokoro(text: str, voice: str, out: Path) -> None:
    global _kokoro
    try:
        from kokoro_onnx import Kokoro
        import soundfile as sf
    except ImportError:
        raise SystemExit("Kokoro not installed. Run: pip install kokoro-onnx soundfile")
    model, voices = TTS_DIR / "kokoro-v1.0.onnx", TTS_DIR / "voices-v1.0.bin"
    if not model.is_file() or not voices.is_file():
        raise SystemExit(f"Put kokoro-v1.0.onnx and voices-v1.0.bin in {TTS_DIR}")
    if _kokoro is None:
        _kokoro = Kokoro(str(model), str(voices))
    samples, sr = _kokoro.create(text, voice=voice, speed=1.0, lang="en-us")
    sf.write(str(out), samples, sr)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("project_dir", type=Path)
    p.add_argument("--engine", choices=["piper", "kokoro"])
    p.add_argument("--voice")
    p.add_argument("--force", action="store_true", help="Re-synthesize all segments")
    args = p.parse_args()
    project = args.project_dir.resolve()

    script = json.loads((project / "script.json").read_text(encoding="utf-8-sig"))
    cfg = script.get("voice") or {}
    engine = args.engine or cfg.get("engine") or "piper"
    voice = args.voice or cfg.get("voice") or DEFAULTS[engine]
    synth = synth_piper if engine == "piper" else synth_kokoro

    voice_dir = project / "assets" / "voice"
    voice_dir.mkdir(parents=True, exist_ok=True)
    made = skipped = 0
    for seg in script.get("segments", []):
        text = seg.get("text", "").strip()
        if not text:
            continue
        key = hashlib.sha256(f"{engine}|{voice}|{text}".encode()).hexdigest()
        wav, sidecar = voice_dir / f"{seg['id']}.wav", voice_dir / f"{seg['id']}.hash"
        if not args.force and wav.is_file() and sidecar.is_file() and sidecar.read_text().strip() == key:
            skipped += 1
            continue
        synth(text, voice, wav)
        sidecar.write_text(key)
        made += 1
    print(f"TTS ({engine}, {voice}): synthesized {made}, reused {skipped}", flush=True)

    rc = subprocess.run([sys.executable, str(ROOT / "scripts" / "audio_timing.py"), str(project)]).returncode
    sys.exit(rc)


if __name__ == "__main__":
    main()
