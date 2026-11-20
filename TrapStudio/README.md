# The Empty Hole • Stickbits

A hungry squirrel keeps digging while ripe acorns land behind her. A cinema ticket worth ₹300 turns the same decision into a question about the next hour. Play **output/The_Empty_Hole.mp4** to see the finished 93.71-second Hindi/Hinglish episode.

## Use it in Claude

**Claude chat with code execution** — Attach the compact project or make the extracted full project available to its Linux sandbox. Paste the prompt below. To keep either workflow as an account-level Claude skill, use the individual ZIPs inside `claude-upload/` under **Customize → Skills → + → Upload a skill**, then enable them. The project also works when Claude reads its skill files directly.

**Claude Code** — Open the extracted project directory. The writing and direction skills live under `.claude/skills/`. Use `/write-trap-fable` and `/direct-trap-fable` when you want to select a workflow explicitly.

> Extract this project and read CLAUDE.md, both project skills and the reference analysis. Install the required tools in your sandbox with bash bootstrap.sh and confirm that the Hindi Kokoro voice test passes. Make a new episode in a separate copy about **[my topic]**. Give it an original animal story and one everyday human decision. Use hf_beta, match each important visual action to its spoken word, and give me the finished MP4 and editable project ZIP. Inspect the first action, human pivot, captions and last frame before delivering.

## What is supplied

| Location | Contents |
|---|---|
| `output/` | Final H.264/AAC MP4 and complete Hindi and Roman Hindi SRT subtitles in the full project. |
| `episode/` | Editable Hindi lines, Roman display words, pause, action and anchor. The measured timeline includes each word and scene boundary. |
| `audio/` | Clean 24 kHz mono voice and 48 kHz mono final mix in the full project. The compact starter includes the clean take. |
| `models/` | Full project includes Kokoro v1.0 INT8, the Hindi voice arrays and license. The compact starter downloads the matching model during setup. |
| `tools/` | Voice generation, duration graph, original actors, sets, camera, sound design, rendering and validation. |
| `assets/fonts/` | Bundled DejaVu Sans and Mono fonts with license. Vector drawings live in the editable Python source. |
| `wheels/` | Full project includes CPU Python dependency wheels for CPython 3.11 and 3.12 on compatible x86-64 Linux. |
| `docs/` | Clip-by-clip analysis, script rationale, measured cue sheet, contact sheet, technical probes, export verification and sources. |
| `.claude/skills/` and `claude-upload/` | Two editable project skills and the same skills packaged separately for importing into Claude chat. |

## Sandbox setup and render

Use Linux with Python 3.11–3.13, a CPU supported by ONNX Runtime, and roughly 1 GB of free working space beyond the archive. Project fonts are registered during rendering. Required native tools are FFmpeg with libx264/AAC, ffprobe, Cairo and fontconfig. The installer can install missing native packages through apt when the sandbox grants package-manager access. It uses packages already present where possible.

```bash
bash bootstrap.sh
bash build.sh preview
bash build.sh all
```

The bootstrap creates `.venv`. On compatible Linux hosts the full ZIP uses its local wheel collection and local model. Other supported hosts need PyPI access. The compact download also needs access to the Kokoro ONNX release on GitHub. Use the full project when either domain is restricted. Missing native packages still require the host's package manager. Set `PYTHON=/path/to/python3.12` to select an interpreter. No paid service, API key or GPU is needed.

Use `bash build.sh render` to change only pictures after editing the director. In the compact starter, the preview and render commands automatically rebuild the missing mix from the supplied take. Run `bash build.sh voice` after changing narration, timing or the score. The default export is 720×1280 at 30 fps, matching the highest-resolution references. A higher-resolution export can be generated using `.venv/bin/python tools/render.py --width 1080 --out output/episode-1080.mp4`.

## Edit a beat

Each record in `episode/story.json` has an ID, Devanagari speech, Roman captions, a cue word, a production action and a post-line pause. Each Roman token corresponds to one spoken token. Write “तीन सौ” as two spoken and two displayed words. Place the cue word exactly once if possible. For this episode the `phrases` list divides a shot at a shift in thought or speaker perspective. Each breath group has Hindi text, Roman text and a pause in seconds. The studio uses the selected Hindi hf_beta preset at 1.01× for every group. Edit the display line and its groups together. The generator phonemizes each group in context and extracts word durations from the same Kokoro synthesis run. The recorded pitch and inflection come directly from Kokoro. Known Hindi loanwords can use a pronunciation override. A scene's start, cue, speech end, end and individual word times are absolute seconds. Timings come from synthesis; the package contains no manually transcribed human alignment.

Register a new ID in the camera table in `tools/direct.py` and implement its visual action there. Edit animal and human drawings in `tools/actors.py`, set paintings in `tools/sets.py`, and sound events in `tools/sound.py`. When planning a different animal or setting, redraw those parts. The existing director is a worked example with authored shots.

## Verification

`bash build.sh check` runs a real Hindi inference and checks native encoding support. The full build decodes every final frame, checks A/V duration, stream codecs, aspect ratio, word and scene bounds, SRT text and loudness. Results are recorded in `docs/export-check.json`. Rendering and package installation were tested here on Linux. Installation in another Claude account depends on that sandbox's permissions and network settings.
