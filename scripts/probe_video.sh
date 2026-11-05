#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <video.mp4>" >&2
  exit 2
fi
command -v ffprobe >/dev/null || { echo "ffprobe not found" >&2; exit 1; }
ffprobe -v error \
  -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate,avg_frame_rate,sample_rate,channels \
  -of json "$1"
# Full decode test:
ffmpeg -v error -i "$1" -f null -
echo "Decode check passed: $1"
