"""Shared helpers for the production scripts (dependency-free)."""
from pathlib import Path
import json, shutil, subprocess

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "engine" / "registry.json"


def load_registry(path: Path = REGISTRY_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def tool(name: str) -> str | None:
    return shutil.which(name)


def require_tools(*names: str) -> dict:
    found = {n: tool(n) for n in names}
    missing = [n for n, p in found.items() if not p]
    if missing:
        raise SystemExit(f"Required tool(s) not on PATH: {', '.join(missing)}")
    return found


def probe(path: Path) -> dict:
    ffprobe = require_tools("ffprobe")["ffprobe"]
    out = subprocess.run(
        [ffprobe, "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)],
        check=True, capture_output=True, text=True,
    )
    return json.loads(out.stdout)


def duration_sec(path: Path) -> float:
    return float(probe(path)["format"]["duration"])


def ratio(value: str) -> float:
    if not value or value == "0/0":
        return 0.0
    num, _, den = value.partition("/")
    return float(num) / float(den or 1)


def resolve_inside(project: Path, rel: str) -> Path | None:
    """Resolve a project-relative path; None if it escapes the project dir."""
    if not isinstance(rel, str) or not rel or Path(rel).is_absolute():
        return None
    p = (project / rel).resolve()
    try:
        p.relative_to(project.resolve())
    except ValueError:
        return None
    return p
