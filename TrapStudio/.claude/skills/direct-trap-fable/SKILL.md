---
name: direct-trap-fable
description: Turn a trap-fable script into a reference-matched portrait animation with Kokoro Hindi narration, cue-driven props, original 2D acting and an exported MP4. Use for Claude sandbox production and narration-to-visual sync.
---

# Direct a trap fable

1. Read the script and identify the choices the audience must see. In the accompanying project, read `CLAUDE.md` and `docs/reference-analysis.md`. Look at the playable example. For fresh clips inspect opening, pivot and ending; use their observable details in preference to a generic Shorts template.
2. On a Linux shell run `bash bootstrap.sh` from the extracted project. Run `bash build.sh check`. Check actual package imports, CPU inference, FFmpeg encoders, font availability and disk space. On a host without shell access, deliver the best source package and state the missing execution step. Preserve the requested voice.
3. Use two sets connected by a decision, one animal and one recurring prop. Draw actors in layers. Animate weight shift, gaze and contact, then settle. Stage a few wide shots so the viewer can see the ignored alternative. Reserve close-ups for the clue or changed belief. Keep line thickness consistent, edge shade gentle and the upper centre free for captions.
4. In the bundled project edit speech and actions in `episode/story.json`. For new subjects make the corresponding original actors and sets in `tools/actors.py` and `tools/sets.py`. Give every new shot ID a camera entry in `tools/direct.py` and implement its motion and state transitions there. A text edit alone cannot draw a new episode.
5. Use the selected natural Hindi narrator for the whole episode. For Stickbits, use Kokoro `hf_beta` at a fixed 1.01× speed. Keep the pitch contour from the recorded take. Use complete spoken phrases, conversational wording and punctuation for expression. Fit the picture, captions and Foley to the resulting voice. Read the exact take's word offsets. Bind entry, contact or reveal to the spoken anchor. A prop already established may persist; land its meaningful action on the word. Place one Roman Hindi word at a time above the action and export full-sentence SRTs. Use the duration of the take for every shot.
6. Render a four-second test with `bash build.sh preview`. Inspect before/contact/after frames for focal action and readable captions. Complete the film with `bash build.sh all`. Use restrained Foley for contacts, a quiet original bed and an uninterrupted tail on the last word.
7. Verify stream properties, first/last frame, timestamps, subtitle bounds, sound peaks and final duration. Check one animal action, the human pivot and the closing choice at phone size. If you change the script, regenerate speech, cues, score and video together. Deliver the MP4 and editable ZIP when asked.

Use the [cue sheet](references/cue-sheet.md) to plan timings. With no accompanying code, use a local renderer and the same timing contract. Record any fallback honestly.
