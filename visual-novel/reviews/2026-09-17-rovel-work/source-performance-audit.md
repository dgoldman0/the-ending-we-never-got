# S004–S005 source, performance and discovery audit

17 September 2026. Read-only implementation review against the complete source interactions at `screenplay/original-timeline/source.fountain:154–250`, adjacent treatment/departure context, the active experience brief, character/wardrobe/prop notes, current Rovel descriptors, reading screens and discovery code. This report is the only project file written in this pass. No game, browser, generation, pixel review or art gate was run. Remaining art production is expected, not an unexpected missing-file defect.

## Corrections before the connected review

1. **The compact performance does not yet make Tessa's refusal develop.** In `game/rovel.rpy:280–283`, she uses `tessa-wounded` both at “Tomorrow?” and at “Look at me. When did I agree to go?”, including the listener after Senn defers her. The new refused-chair brief explicitly changes hurt into direct insistence. Use the existing resolute performance at source 200 and for her response at 203, or document another deliberate performance choice that expresses the change. Hurt remains appropriate at 192/195. Review the face against the body: a forceful upright refusal cannot become a passive compact reaction merely because that portrait exists.

2. **Make the two-step/three-step hall geometry consistent.** `art/rovel/review/scene-briefs.md` specifies two low dais steps; `art/prompts/rovel/ceremony-refused-chair-v1.txt` asks for three. Neither count comes from the screenplay. Select the workable produced geometry and align the working record; do not rewrite the source. The important source requirements are the route around the unused chair, continuous sleeve contact, Iven remaining wholly below the dais through 211, and Senn yielding a usable ascent at 214. Compare 183 → 190 → 198 → 206 → 214 in that order.

3. **Remove premature announcement from the shared dais description.** The `ceremony-dais` stage description says Senn announces tomorrow's departure. It is also shown at 183, before Olan's 185 insert and the actual 187 speech, and reaches the reader through `current_art_description()`. Describe his bringing Tessa onto the platform at 183; attach the announcement to 187 or use a neutral shared description. The source speech itself is correctly ordered and unchanged.

4. **Discovery currently conceals almost all of the originating scene.** `game/rovel-ui.rpy:92–110` redraws that scene, but then adds an approximately 85%-opaque full-screen scrim and an 1820×885 panel in a 1920×1080 canvas. Only narrow edge strips remain. This does not by itself meet “keep the originating scene perceptually present” or the production brief's small optional first-night view. Preserve a recognizable current-scene strip/inset or reduce the covering surface, while retaining useful detail scale and direct Return. Actual perception and beauty require the connected review; a background draw call alone is insufficient evidence.

## Source-to-performance assessment

All **29 S004/S005 reading pages** have exact descriptors: 16 ceremony pages and 13 window pages. No source dialogue or action is omitted by this plan. Source-speaker identities match; every spoken page has a distinct listener. The following action divisions are justified by the source, subject to actual art and integration review:

| Source | Required state and current plan |
| --- | --- |
| 176 | Badge pinned to coat, then white mantle settled. The art brief deliberately depicts the second action with the badge already attached. The descriptor's `being-pinned` state should be clarified to that selected endpoint rather than suggesting both actions are literally simultaneous. |
| 178/180 | Orra offers orders; the messenger offers a blackened stone instead. Their compact exchange can hold that composition. No stone transfer, additional magic or diagnosis is established. |
| 183/185/187 | Establish Tessa/Senn on the dais, cut to **standing** Olan, return to Senn's public announcement. Orra stays at the door until 206. Add `standing` to the applause descriptor/alt as an explicit safeguard: the source says it and the replacement prompt now correctly requires it. |
| 190/192/195 | Tessa catches Senn's sleeve while applause drowns her first attempt to speak. The distinct initial refusal composition must leave the later movement around the chair possible. |
| 198/200/203 | The **new refused-chair state is necessary and correctly assigned**. She remains upright, goes around the chair, and keeps her grip. Using her healthy right hand on Senn's left sleeve is a working laterality choice, not a screenplay fact. The same choice must persist across both images. |
| 206/208/211 | Orra has stepped onto the dais; Iven addresses her from below with Tessa's bag. Showing Tessa as the listener to Iven's refusal is a useful reaction choice; Orra remains in the wider scene. |
| 214 | A separate yield illustration is appropriate. Orra now signals Iven up; Senn yields the steps. This must not be the previous below-dais still with a different caption. |
| 218–234 | Tessa sits at the window in the same complete formal outfit. Iven puts her bag beside her and packs the medical chest while standing. The mother's 226 insert is the same bedside mother, seen below; it does not bring her into the infirmary or add her daughter. |
| 237–247 | The bottle goes back into the chest, whose lid stays open. Iven stops packing but remains standing. Mara and the same two apartment guards are below at 242. Neither exterior insert gives the player a body or sends the upstairs cast outdoors. |
| 250 | Tessa makes room and Iven sits with her; chest remains open, bag nearby. This is the shared seat's first appearance. Preserve the offered space and companionship without adding an embrace, recovery, or completed departure. |

The S005 compact expressions distinguish the pressure of the recurring requests (228/234/239) from the assurance of company (244/247). That is a reasonable performance plan, not a cleared acting result. Tessa is still nineteen, hands healthy; no age jump, postwar injury, campaign outfit or removal of the mantle occurs between ceremony and window.

## Reading modes and the applause panel

The 185 applause insert is a purposeful narration cut rather than a rapid dialogue turn. Its smaller lower-left panel therefore does not violate the stable exchange rule, provided the ensuing 187 speech returns to the usual text origin. In `rovel-ui.rpy:41–54`, the panel occupies x70–870, y738–1013 at minimum height, leaving only five virtual pixels above the footer. Check both text sizes with its actual source sentence: automatic height must not push the frame into the footer, and the left-palm/thigh contact, supported injured right hand, and standing posture must remain readable. The full illustration and detail crop must show the same hand state and grade.

The descriptor's `quiet` mode is currently planning metadata; the renderer selects layout from speaker presence and explicit source exceptions, not from that mode. Thus S005's quiet labels do not themselves create a closer view, pause or different narration treatment. This is not automatically a defect: a well-composed held window image may supply the needed silence. Review 237 and especially 250 at natural reading pace instead of counting the labels as achieved direction. Likewise, compact portraits must not contradict a held CG's gaze, active gesture or contact.

## Discovery payoff, knowledge and return

`inquiry-data.rpy` offers a modest source-backed progression: torn drawing/dead phone at 2:112; blue healing beside white purification at 3:172; treatment beside Olan's later applause after 4:187. First-night captions stay brief. The Olan connection can reward attention if the actual crops make the surviving digits, disappeared corruption and one-handed applause clearly comparable. Do not describe Senn's literal claim as disproved by missing fingers: he says **the curse can be broken**, and the source does show that. The useful relationship is real help with lasting limits, publicly used to announce Tessa's service without her agreement. The full playthrough must preserve both Olan's gratitude and Tessa's coercion.

Current reader operations have no inventory, travel, new cast actions, quizzes or knowledge disclaimer. The mutation helpers only record inspected details and followed connections; they do not write the source cursor, character state, or ending. Availability follows the saved narrative position, not persistent discovery unlocks. Returning through `Return()`/Escape resumes the suspended story interaction. Existing native tests target exact returns at 2:112, 3:172, 4:187 and 5:250, rollback before reveal, and earlier/later save knowledge separation. Those tests still need to run against the completed integrated assets; code inspection is not a fresh runtime pass.

Threads defaults to the newest available comparison and records that visible pair as followed. This is consistent with exposing both details immediately, without prerequisite clicks. It is not evidence that the player consciously read every detail. Keep the state out of progress quotas and narrative branches. The quiet Look closer opportunities remain optional, including the final window seat; do not turn that seat into a mandatory inspection intermission.

No ancient-origin history is authored in these three comparisons. That remains required later work for the full route; it should not be smuggled into Olan's injury or the ward stone. The first Saint's initiating event, its records and corroboration still require deliberate authoring. These opening comparisons must not be reported as fulfilling that reveal.

## Connected review focus

After the corrections and remaining art production, read 172 through 250 continuously before isolated inspection: treatment's aftermath into institutional ceremony; actual sleeve-grip/movement continuity; intervention before ascent; then pressure, uncertainty and companionship at the window. Test the new 185 panel and all discovery pairs with Standard/Larger and Intense/Softened in native and browser views. Compare exact entry/return frames, focus and hit areas, not just cursor values. Verify shared room geography, complete formal layers, supporting identities, empty-chair state, open chest and all hand/prop contacts in pixels.

**Status:** plan reviewed with the corrections above; visual, interface, atmosphere, discovery-payoff and whole-experience gates remain unreviewed by this audit. No code-based clearance is claimed.
