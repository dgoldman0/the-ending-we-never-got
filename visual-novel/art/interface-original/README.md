# Original interface — renewed working pass

Unapproved production work following the rejection recorded at `f3acb5e`.

The interface is part of the original timeline's painful beauty. Develop a painted surface from aged gilt, pale mineral inlay and restrained botanical relief, with visibly interrupted growth. These are interface motifs, not new faction symbols or story artifacts. Keep the main text field quiet. Ornament must survive ordinary window size without competing with acting.

First component: a wide reusable dialogue frame, separated and sized in GIMP, with native text and focus states in Ren'Py. Use it alongside narration, utility screens and the title, adjusting density for each purpose. Do not clear it from an isolated render: inspect short and long dialogue, standard/larger type, all three lighting registers and the complete connected opening.

Use original rough references for material treatment only. They do not authorize importing their figures, gods, heraldry or architecture. Prompts live under `../prompts/interface-original/`. Preserve raw output, layered GIMP masters and concrete review observations separately.

## Implemented working pass

`raw/dialogue-frame.png` is the generated material component. GIMP masters retain it separately from the cleaned, masked exports: `masters/dialogue-frame.xcf` and `masters/crest.xcf`. The [finishing script](../../tools/finish-original-interface.scm) makes speech, narration, menu surface, lip and crest assets. Their editable masks and layout serve different screen roles; no lettering is baked into the artwork.

Native and browser inspection found two problems and corrected them: long dialogue reached the left botanical relief, and small page buttons compressed the ornament into jagged marks. Speech padding now reserves that relief; utility buttons use tint and underlining. The current settings screen, including Lighting, fits at 1280×720. Larger-text promise, doorway, priest, Olan, mother and discovery captures were inspected in native play. The [opening review](../opening-sequence/review/realignment-review.md) records the exact scope and remaining failures. The new interface remains working production, not user approval.
