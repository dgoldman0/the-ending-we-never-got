# Original interface — rejected component pass

Historical component work used by runtime 0.3.2 / `d0c3020`, subsequently rejected. The [full design review](../../reviews/2026-09-17-full-design-review/README.md) records unfinished cropped edges, awkward layout/reading flow and inconsistent screen treatments. The [active experience brief](../../presentation-redesign.md) governs the next interface; neither these materials nor previous local corrections clear its design.

The earlier pass explored aged gilt, pale mineral inlay and restrained botanical relief with interrupted growth. These are possible material references, not a selected final interface or new faction symbols. The original timeline's painful beauty remains the goal. New designs must compose ornament, typography, reading space and acting together at ordinary window sizes.

The first component was a wide generated frame separated and sized in GIMP. Cropping its middle for narration produced visibly unfinished edges. Do not carry this construction forward as a requirement. Develop appropriate compact speaker frames, staged dialogue, narration and utility surfaces with native text/focus states. Evaluate the shared family across title, reading, discovery and utilities in connected play, with short/long lines, standard/larger type and both lighting preferences.

Use original rough references for material treatment only. They do not authorize importing their figures, gods, heraldry or architecture. Prompts live under `../prompts/interface-original/`. Preserve raw output, layered GIMP masters and concrete review observations separately.

## Historical implementation and local checks

`raw/dialogue-frame.png` is the generated material component. GIMP masters retain it separately from the cleaned, masked exports: `masters/dialogue-frame.xcf` and `masters/crest.xcf`. The [finishing script](../../tools/finish-original-interface.scm) makes speech, narration, menu surface, lip and crest assets. Their editable masks and layout serve different screen roles; no lettering is baked into the artwork.

Earlier native/browser inspection corrected two local problems: long dialogue reached the left botanical relief, and small buttons compressed the ornament into jagged marks. That pass recorded settings fitting at 1280×720 and inspected selected larger-text compositions. The [historical opening review](../opening-sequence/review/realignment-review.md) gives its exact scope. The subsequent full review and user rejection supersede any favorable impression from those local checks; this interface is not cleared for continued production.
