#!/usr/bin/env bash
# Linux setup; keep Python packages local to the extracted project.
set -euo pipefail
cd "$(dirname "$0")"
py="${PYTHON:-python3}"
if ! "$py" -c 'import sys; assert (3,11)<=sys.version_info[:2]<=(3,13)' 2>/dev/null; then
  for candidate in python3.12 python3.11 python3.13; do
    if command -v "$candidate" >/dev/null; then py="$candidate"; break; fi
  done
fi
"$py" -c 'import sys; assert (3,11)<=sys.version_info[:2]<=(3,13), "Python 3.11–3.13 required"'
if ! command -v ffmpeg >/dev/null || ! command -v ffprobe >/dev/null || ! "$py" -c 'from ctypes.util import find_library as f; assert f("cairo") and f("fontconfig")'; then
  admin=()
  if [[ $(id -u) != 0 ]]; then
    if command -v sudo >/dev/null && sudo -n true 2>/dev/null; then admin=(sudo -n)
    else echo "This host needs FFmpeg (including ffprobe), libcairo2 and libfontconfig1. Enable those system packages or use the supplied movie." >&2; exit 1; fi
  fi
  if command -v apt-get >/dev/null; then
    "${admin[@]}" apt-get update -qq
    "${admin[@]}" apt-get install -y --no-install-recommends ffmpeg libcairo2 libfontconfig1 python3-venv
  else echo 'Install FFmpeg/ffprobe, Cairo and fontconfig with this Linux distribution’s package manager.' >&2; exit 1; fi
fi
if [[ ! -x .venv/bin/python ]]; then
  if ! "$py" -m venv .venv; then
    if command -v uv >/dev/null; then uv venv --seed --python "$py" .venv
    else echo "Install the venv module for $py before running bootstrap again." >&2; exit 1; fi
  fi
fi
if [[ -d wheels ]] && .venv/bin/python -m pip install --no-index --find-links wheels -r requirements.txt; then :
else .venv/bin/python -m pip install -r requirements.txt; fi
.venv/bin/python tools/fetch_model.py
.venv/bin/python tools/preflight.py
