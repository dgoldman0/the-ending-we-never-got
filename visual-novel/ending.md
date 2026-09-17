# Original ending and the question to the player

Status: **ORIGINAL ENDPOINT REQUIREMENTS — realigned 17 September 2026.** The user established the complete original ending, then **“Do you wish to save Tessa?”**, with Yes only after that final scene. The Bellweir sequence is screenplay material; the question is VN framing. The hopeful/shattering presentation after Yes and the continuation are explicitly deferred. Runtime 0.3.2 displays the question but only offers Return to title; this remains an endpoint interaction gap.

Source: [Rebuild 11](../screenplay/original-timeline/source.fountain), S058, beginning at line 2175. Preserve the earlier deaths, right-hand injury, loss of trust and unresolved route home. The player may also know the first Saint summoning's role in human-initiated war; Tessa does not learn it here.

## The original scene must finish

| Beat | Picture / action to retain | Dialogue and dramatic purpose |
| --- | --- | --- |
| 1. Return to Bellweir | Familiar square, rebuilt roofs among burned walls, heron with one wing missing; inspectors admit a northern grain barge | The source marks four years since summoning. Reconstruction and a practical agreement exist alongside damage. |
| 2. Her decision | Temple offer and her reply, **I WILL REMAIN IN BELLWEIR**; soft brace on the right hand, pencil in the left | This is a choice of where to live now. There is still no usable route to Earth for her to accept or refuse. |
| 3. The invitation | Orren with his stick; Hest and the apprentices disputing the misshapen rolls inside | Keep his invitation and Tessa's “almost done,” including his familiar prediction that she will take five more minutes. Ordinary company still matters. |
| 4. An uncertain lead | Elin puts down the catalog reference; Tessa stops writing to read it | Keep the question about the pages, Elin having written to ask, and Tessa's request to go with her. No confirmed cure, portal or complete book. |
| 5. The drawings | The reference joins her mother's kitchen and Iven's unruly-haired portrait in the packet | Let her attention remain on Iven's face. Do not add a ghost, voiceover farewell, new love letter or montage announcing recovery. |
| 6. Going inside | Ada calls; Tessa closes the packet and signs. Elin crosses with her; Renn carries plates through the doorway | The children have visibly aged. Elin's presence continues without replacing the people who died. |
| 7. A place at the table | Orren moves a chair. Tessa takes it | Preserve this final action. Do not replace it with her turning away from everyone or staring hopelessly at a closed portal. |
| 8. Fade to black | Let the final composition resolve, then fade | This completes the screenplay's original ending. Do not cut it short for a hook. |

Use the established ordinary-light register: some environmental discomfort, with real warmth between people. Tessa's physical wear and grief persist in clean civilian clothing. The missing wing, drawings and hand communicate continuity without an explanatory summary of every loss. Postwar costume design remains pending; the superseded cardigan is not a production reference.

## Then address the player

Proposed screen sequence:

`Tessa takes the chair → the source fade to black → a quiet, reader-paced transition → “Do you wish to save Tessa?”`

On black, display the exact question plainly. It has no character nameplate or established in-world speaker. It is addressed to the player. Do not show Tessa hearing it, answering it or waiting for permission to continue her life. Do not add Neri, a familiar, a reincarnation montage, a lore explanation, an achievement popup or a historical-investigation recap between the meal and the question.

Allow the final fade a beat before a fresh player advance reveals the question; do not turn one rapid click at the end of dialogue into an answer. Exact transition duration, typography and audio are presentation decisions for the prototype. An extended forced wait is unnecessary. Place credits after this framing or make them reachable separately; a credit roll must not obscure the requested endpoint.

The original endpoint must eventually offer a deliberate **Yes** at this question; Return to title alone does not meet that intended interaction. Do not preselect, time, or accidentally trigger the answer with the advance that finishes the scene. A No option, response storage and revisit behavior remain design decisions, not established new story outcomes.

The user has established the eventual shattering/hopeful change after Yes, but specifically deferred work on its UI/UX. Design the original endpoint's response handoff within that boundary when implementation reaches it; do not invent or advertise a playable rescue continuation. This realignment does not implement the response or settle its storage behavior. The placement of Yes is settled; those implementation particulars remain open.

## What the question does and does not establish

Every player reaches it after the original ending, regardless of optional investigation progress. It does not reveal that a missed click could have saved Iven or Mara, or mark this playthrough a failed route. It does not declare Tessa's continuing life worthless because she is grieving or disabled. The desire to change what she was subjected to can coexist with the people and choices that still matter to her.

The question opens the possibility of changing her course. It does not yet settle the rescuer, mechanism, price, scope of change or Tessa's own eventual choices. The deferred incursion material is available for later discussion; this framing does not silently select that entire continuation.

## Review points before implementation

- Read the whole Bellweir interaction into the fade and question, not the question in isolation.
- Verify that her body, drawings, children and heron carry the correct four-year state.
- Keep the historical investigation separate from her knowledge and the catalog lead.
- Test a straight-through playthrough and a completed-investigation playthrough: both must receive the same original ending and question.
- Confirm that the transition gives the original ending space without turning the prompt into an accidental click or mandatory pause puzzle.
- Verify that the final question has the intended deliberate Yes affordance while the deferred post-Yes visual/continuation scope is respected. A test that merely reaches the text of the question does not clear this requirement.
