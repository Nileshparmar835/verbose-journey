# Episode decisions

## The hook

| Candidate | What the first frame would have to prove |
|---|---|
| “पीछे देखो, मेवा गिरा! और ये देखो, अभी भी खोद रही है।” | An acorn lands behind her as her paws keep digging. This is the selected contradiction. |
| “तीन सौ रुपये की टिकट तुम्हारा अगला घंटा कैसे ले सकती है?” | Strong human question, but it would move the film away from the animal-first structure. |
| “गड्ढा जितना गहरा हुआ, उसे छोड़ना उतना मुश्किल क्यों हुआ?” | The mechanism is clear, but the alternative food is missing from the opening. |
| “चिड़िया ने एक छलाँग में वो पा लिया जो गिलहरी दिन भर ढूँढती रही।” | Sets up a comparison, but gives the bird’s action away early. |
| “अगर मेवा पीछे पड़ा था, तो गिलहरी आगे क्यों खोदती रही?” | Clear geography. The selected version lets the image reveal that geography first. |

The squirrel has a reasonable initial guess that she buried nuts. The moved twig, worm, rock and feeding bird progressively weaken that guess. Her prior effort makes it harder to leave. At the cinema the ticket money is already spent and the next hour remains available. The practical question about a free ticket isolates the decision still open to the viewer.

## Art and sound

- Draw on a 360×640 design grid and render at twice that resolution. Use cubic curves for the squirrel's tail, stomach, cheeks and bent posture. Give it independently moving paws, a turning head, a blinking eye and a reaching pose. Dirt contact and the tail silhouette carry the opening.
- Use an oak-tree clearing in three lighting states and a second set with cinema seats, an aisle, an exit, a projected landscape and a clock. The seat colours and spent ticket connect the human scene to the warm colours in the clearing.
- Keep the main caption at x=180, y≈177 design units. Most words are ivory. A handful of narrative anchors use warm coral. Hold captions above the fixed action plane while the camera scales.
- Use measured Kokoro Hindi speech as the master clock. Use the same hf_beta voice, Hindi phonemization and 1.01× synthesis speed across the story. Record each connected phrase with its written punctuation. Preserve the model’s pitch contour and use one recording gain for the entire take. The soundtrack layers a soft synthesized pad with short plucks and filtered dirt sounds. Track settings and rendered voice timing are in the editable files.
- Text and timings for all 26 beats appear in the cue sheet. The rendering sources contain the episode-specific choreography. The example is an authored animation; future episodes need their own props and blocking.

## Sources and asset provenance

All picture assets, drawings, script, score and Foley in the sample were produced for this episode. Reference footage is used for comparative analysis. Model weights come from Kokoro v1.0 INT8, and the four original Hindi voice vectors are repackaged together. The narrator selected for this film is hf_beta. Fonts and model license notices are included beside those assets. Python wheels carry their respective package metadata and licenses.

- [Kokoro model card and license](https://huggingface.co/hexgrad/Kokoro-82M)
- [Kokoro voice inventory](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md)
- [Kokoro ONNX model release](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0)
- [Arkes and Blumer, The psychology of sunk cost](https://doi.org/10.1016/0749-5978(85)90049-4)
- [Claude Code project skills](https://code.claude.com/docs/en/skills)
- [Claude chat custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
