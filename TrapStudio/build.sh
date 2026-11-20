#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
py=.venv/bin/python
if [[ ! -x "$py" ]]; then bash bootstrap.sh; fi
if [[ "${1:-all}" == preview || "${1:-all}" == render ]] && [[ ! -f audio/mix.wav ]]; then
  "$py" tools/sound.py
fi
case "${1:-all}" in
 check) "$py" tools/preflight.py ;;
 voice) "$py" tools/voice.py && "$py" tools/sound.py ;;
 preview) "$py" tools/render.py --width 540 --preview 4 --out output/motion-test.mp4 ;;
 render) "$py" tools/render.py && "$py" tools/verify.py ;;
 all) "$py" tools/voice.py && "$py" tools/sound.py && "$py" tools/render.py && "$py" tools/verify.py ;;
 *) echo 'Usage: bash build.sh {check|voice|preview|render|all}' >&2; exit 2 ;;
esac
