# Full game design review — 17 September 2026

**Verdict: the current build fails as a coherent visual novel, including the illustrated opening.** Its central problem is direction: how the player sees a person, follows an exchange, understands an action, pauses over a detail, and stays emotionally involved. Missing production compounds that problem across most of the route. Finishing the same design with more pictures would preserve substantial failures.

Reviewed web version **0.3.2**, corresponding to runtime at `d0c3020`, on branch `current-draft`. The user stopped piecemeal fixes and requested this full review. This review changes documentation only. It does not clear any scene, generate replacement art, revise the screenplay, or begin the deferred post-Yes presentation.

## What was actually reviewed

Opened the existing local WebAssembly build in an isolated Chromium profile. Traversed all **58 scenes, 849 source reading blocks, and 852 reading pages**, capturing every scene entry and recording reading-window geometry on every page. The final fade is separate from those counts. Manually inspected consecutive opening captures, both missing-cast scenes, representative later scenes, the title and opening cards, discovery and Threads, history, saves, settings, and the final question. Compared their presentation with the screenplay and the implementation.

The main review size was 1280×720. Additional captures inspected larger text and selected screens at 1920×1080 and 960×540. Exercised save creation, return from menus, lighting switching, detail inspection, following a connection, and return to the same source page. The automated route run is coverage evidence, **not a claim that all 852 pages were manually read at natural pace**. No human playtime estimate, native-build regression, screen-reader audit, or full production-art clearance is claimed. The route collector initially queried during the ending dissolve; after the transition, the fade and question were separately reached and inspected. That timing issue was in the audit script, not a reproduced game failure.

Representative screenshots are retained under [evidence/](evidence/). [audit-summary.json](audit-summary.json) and [reading-layouts.json](reading-layouts.json) preserve the coverage and geometry evidence. Screenshots are rejected-build evidence, never approved visual references.

## 1. Conversation has no coherent presentation system

The current dominant arrangement is large standing figures, a large ornamental speech panel, and a jump to the opposite lower corner when the other person speaks. The text origin moves about **612 screen pixels at 1280×720** between the standard left and right anchors. Narration then moves back to the center or a separate side panel. That movement is repeated even when the shot and performances barely change.

Compare [Senn speaking](evidence/conversation-senn.png), [Tessa replying](evidence/conversation-tessa.png), and the [first-night exchange](evidence/night-tessa.png) / [Mara's reply](evidence/night-mara.png). The player must repeatedly relocate the next line, connect a small name with a distant face, and search for a reaction. The layout creates visual activity while the actors often remain static.

The user's suggestion of **smaller character frames for rapid exchanges is a missing core capability**. There is no compact portrait-and-dialogue mode. Large sprites are doing work better suited to readable face/reaction frames; dialogue boxes are being treated as movable containers rather than part of conversation direction.

Speaker placement is also ambiguous in crowded shots. In [the infirmary instruction](evidence/ward-priest.png), the priest stands far behind Tessa, while his box occupies Tessa's foreground area. The small “Priest” label carries the attribution almost by itself. A compact, recognizable speaking portrait would resolve that ambiguity without repositioning the whole scene.

**Required design direction:** establish a compact portrait/text pairing for fast speech, a stable reading zone, deliberate listener reactions, and clear identification of offscreen speakers. Keep wider staging visible when it matters. Use speech beside a staged figure when the composition supports it. The small portrait itself can supply the nearby visible speaker in a rapid exchange; do not mechanically fling a large panel across the screen on every turn. Exact dimensions and treatment must be judged in play.

Implementation cause: [opening.rpy](../../renpy/game/opening.rpy), especially `opening_actor`, `dialogue_position`, and `composed_reading`, defines large figures and fixed left/right anchors but no conversation modes or reaction policy.

## 2. Acting and visual editing do not carry the dialogue

Senn holds the same offered-hand sprite across most of source lines 29–57. Tessa alternates among a small number of poses; the apartment exchange similarly holds Tessa's questioning gesture and Mara's supper tray through changing lines. A held pose is useful when its emotional meaning remains right. Here, requests, resistance, evasion and promises frequently receive the same visual response.

The jump from a spacious action illustration to two large, sharply outlined figures also changes the visual language. Those figures read as posed cutouts; matching exposure does not establish shared depth or acting. The ward illustrations make better use of people attending to one physical action, but hold a small set of compositions through exchanges that still need specific gaze, hand and listener changes.

The adaptation needs an account of **whose response matters after each beat**, including when the listener matters more than the speaker. A response can be a held face, a changed hand, a look toward an exit, or a deliberate wider view. It does not require a new full painting for every sentence. It does require choosing the image for dramatic purpose rather than asset availability.

The accepted Tessa likeness, chronological wardrobe, injuries, faction symbols and other written designs remain authoritative. Smaller frames must not become another way to recycle a drifting face. Judge source likeness, pose, silhouette, contact and expression separately. Use the generator for tailored components and GIMP for controlled assembly and repair during production; neither tool's use is evidence that the resulting performance works.

## 3. The interface's ornament does not form a finished design

The speech frame has a heavy botanical end, narrow working text width and large padding. Its visual weight competes with gestures while the speaker name is comparatively weak. A one-line reply and a consequential speech inherit the same furniture-like treatment. The bottom controls sit on another strip with a separate gold edge. Menus repeat a partly offscreen crest and a long decorative rule, but do not acquire a distinct relationship to their contents.

There is a literal construction problem behind the cut-off appearance: `reading.png` was cropped from the middle of a larger frame, then stretched with `Frame`. Its vertical edges are unfinished. [The closure narration](evidence/narration-cut-edges.png) shows the result. The title and menu crest also run beyond the left edge by explicit negative positioning. These are visible composition choices, not proof of an old browser build.

The screen family is inconsistent: S001–S003 use the new floating frames; S004–S005 revert to the old full-width reading veil; S006 onward adds oversized location typography over plain color. Each transition changes how the reader is expected to look and read.

**Required design direction:** compose a family of complete surfaces for compact dialogue, staged speech, narration, inspection and utilities. Resolve silhouette, finished edges, optical spacing, type hierarchy and focus treatment together. Establish what ornament means and where it belongs. Preserve the material vocabulary of the references without repeating one cut-out flourish at incompatible scales. Beauty has to remain visible at ordinary playing size; denser decoration and another font change will not establish it.

Implementation: [core.rpy](../../renpy/game/core.rpy), `say` and `quick_menu`; [presentation.rpy](../../renpy/game/presentation.rpy); [finish-original-interface.scm](../../tools/finish-original-interface.scm).

## 4. Reading rhythm is mostly inherited from screenplay paragraphs

The adapter preserves the screenplay, which is useful, but most presentation advances are generated directly from its paragraphs. The length splitter and the special portal-closure split are the main explicit paging decisions. The number of clicks alone does not measure pacing. The weakness is the missing distinction between a quick interruption, an action unfolding, a listener absorbing a line, and a pause that deserves space.

Before the first scene, the new reader clicks **Begin → another Begin → chapter Continue**. The title, instruction card and chapter card repeatedly restart the experience. Later chapter cards use the same generic pause regardless of the preceding emotional event. Within scenes, moving boxes and abrupt changes of layout interrupt attention without necessarily marking an intended dramatic change.

The screenplay already contains useful compression: five weeks on the road, seasonal jumps, and the S029/S043 montage structures. Preserve those. The training meal, checkers, market, boat outing, reunion and laughing portrait are essential attachment scenes; cutting them for speed or lore would weaken the ending. [The pacing proposal](../../pacing.md) identifies these priorities, but the runtime has not directed them.

Build an authored presentation layer over the preserved source: shot, participants, reaction, reading treatment, action transition and intentional hold. Any proposed prose adaptation should be explicit; do not rewrite the screenplay to excuse a render. The goal is to make the existing causal and emotional sequence legible and compelling.

## 5. Most of the route has no performed visual experience

The latest screenshot complaint is reproducible in the current build. [The Messenger's ceremony line](evidence/ceremony-empty.png) has a room plate with no speaking cast. [The following window scene](evidence/window-empty.png) omits Tessa and Iven as well. This is where the story should show public pressure and a private offer of companionship.

| Runtime span | Reading pages | Actual presentation |
| --- | ---: | --- |
| S001–S003 | 66 | Mapped scene/performance states; design and quality remain rejected |
| S004–S005 | 29 | Legacy room plates; required cast and actions missing |
| S006–S058 | 757 | Plain location cards and text; scene and cast production missing |
| Total | 852 | Only 7.7% have mapped performance presentation |

The source has 849 reading blocks; three split into an additional page. These counts should not be mislabeled as 852 screenplay blocks.

The absence continues through [Lucan and the apprentice](evidence/river-camp-prose.png), [Tessa with Iven's coat](evidence/grief-prose.png), and [the final return to Bellweir](evidence/ending-prose.png). It removes visual access to warmth, trust, changed relationships, grief, aging and the lasting hand injury. The world, lighting and people vanish while the words ask the player to invest more deeply in them.

This is a production blocker independent of the opening's design defects. A full-route text traversal is not a finished visual novel. Restoring rejected old sprites would not resolve it either. Coverage must be planned through the ending with intentional performance or story-appropriate absence on each beat.

## 6. Painful atmosphere is not yet sustained as an emotional experience

The current summoning is strongly glaring, and the first night is deeply dark. Those directions should survive redesign. They do not make the complete presentation successful. The older ceremony plate and the plain-card route break the lighting progression; most of the story cannot express its environment visually at all.

The title puts Tessa into deep shadow while the large title and cropped ornament attract most of the attention. It borrows a story illustration without fully composing an invitation into her life. The opening's polished, repeated character poses likewise make suffering feel staged. Later warmth and loss receive the same empty layout.

The intended experience depends on attachment: humor, hesitation, ordinary kindness, intimacy, and then their cost. The lighting can remain nearly blinding, uneasy, or dreary while those human differences remain expressive. Reading and navigation should be comfortable to understand; discomfort belongs to the fictional atmosphere and emotional situation.

Keep **Intense as the default and Softened as a persistent option** before and during play. Switching the option and returning to the same story point worked in the reviewed browser. Preserve coordinated grading of scenes, people and inspection details. Do not normalize the default to repair a typography or layout problem.

## 7. Discovery makes the reader navigate an explanation

The accepted reader role is correct: Look closer / Threads does not give the player a body, inventory or in-world actions. The current implementation also returns to the exact reading page. Those behaviors are worth retaining.

Its presentation and reward are weak. The first night moves from a full scene into [a smaller picture inside the general menu](evidence/discovery-whole.png). Large headings, utility navigation and repeated target labels compete with the object being examined. The reader then selects a detail, brings another alongside, and follows the connection. [The result](evidence/discovery-followed.png) is mainly an interpretation of what the story has already shown: the dead phone, her mother's request, and the kitchen drawing.

Four selections before the interpretation create substantial ceremony around very little new discovery. The captions also announce the intended meaning instead of letting the relationship become apparent through the details. Threads contains only this pair for the rest of the game. **The human origin of the ancient war and the first Saint summoning are not implemented.** This gap cannot be described as a completed investigation system.

The better direction is to keep the scene perceptually present while attention moves into a detail, offer a related image without sending the reader through several general-menu pages, and reveal specific authored material worth following. Keep keyboard/list access without turning the visual interaction into a directory of explanations. The historical connection must be developed from project sources, with missing historical particulars explicitly authored; the player learns it, and the original cast does not silently acquire that knowledge.

Implementation: [investigation.rpy](../../renpy/game/investigation.rpy), [inquiry-data.rpy](../../renpy/game/inquiry-data.rpy).

## 8. Navigation and accessibility have concrete faults

| Finding | Evidence and consequence |
| --- | --- |
| A visible Threads caption is partly outside its hit area | At 1280×720, clicking the visible “The torn page” text at (185, 373) leaves Threads open; clicking the image opens the detail. The button's virtual rectangle ends at y=547 while the label extends below it. [Capture](evidence/threads-label.png). This is a reproduced interaction defect. |
| Utility positions change | Look closer and Threads are conditionally inserted before Save and Menu. The player's familiar targets shift during play. |
| Continue looks actionable but has no distinct button | The footer draws plain text for Continue. General scene advance makes mouse clicking there work, but it has no separate focusable control or matching hover behavior. |
| Larger text does not address the whole interface | The dialogue font grows from 32 to 36 virtual pixels; many names, controls and explanatory texts remain fixed. At 960×540 the footer controls are approximately 11 screen pixels tall in font size. Scaling the entire canvas makes them fit, not comfortably readable. |
| Discovery crowds the bottom edge | With Larger enabled, “Back to the details” reaches the virtual screen bottom at y=1080. It remained reachable in the test, but the composition has no breathing room. Do not misreport this as observed offscreen text. |
| Saves are hard to recognize by narrative context | [The grid](evidence/save-grid.png) identifies saves by thumbnail and time only. Later unillustrated scenes produce nearly identical thumbnails. Chapter/location identification would support returning to an emotional moment. |
| The reader changes navigation environments | The story footer, full-menu top navigation and web container's top-left menu expose different control locations. Discovery inherits the utility menu instead of feeling like focused attention within the story. |

The full standard-text route geometry audit did **not** find story glyphs below the controls or a reading window outside the 1920×1080 canvas. Targeted Larger checks also fitted. That does not dismiss the user's report: cut decorative edges and inconsistent panel constructions are reproduced visibly; other line/size combinations remain possible. The old general window extends six virtual pixels under the footer, although the measured text remained above it. Repair claims must distinguish text clipping, ornament clipping and composition rather than declaring “the box fits.”

History scrolling, save creation, menu return, lighting switching and connection return worked in these exercised paths. That is a limited functional result, not UX clearance. Reduced motion and image descriptions exist; full assistive-technology and input-mode validation remains outstanding. Sound, music and voice are disabled in the configuration, so there is also no sound direction supporting space, transition or silence. Audio should eventually support the scenes, but cannot rescue the visual and interaction defects.

## 9. The ending cannot accept the promised response

The full Bellweir text precedes the fade and final question, so the question is in the correct chronological position. [The question screen](evidence/final-question.png) offers **only Return to title**. The player cannot select Yes.

Record that as an endpoint interaction gap. The deferred hopeful interface and shattering transition remain outside the current work. Designing a clear endpoint response and developing a post-Yes experience are separate tasks; this review does not start either implementation.

## Why previous review did not prevent this

The written gates already required connected experience review. The production records nevertheless documented missing cast and unreviewed sequences while work continued on grading, ornament and individual corrections. A gate recorded as failed did not govern what happened next.

The reviews were too permissive about posed acting, patchwork composition and monotonous flow. They established that files loaded, source words survived, selected anatomy/props improved, and particular rectangles fit. Those observations were repeatedly allowed to stand in for whether the game made someone want to continue reading. More checklists alone would repeat that error.

There are useful foundations: preserved source chronology, the separate reachable portal control, distinct Earth/temple design, functional story state, and the lighting preference. They remain foundations. They do not approve the current art or presentation.

## Recommended design and production order

The first decision is how different dramatic situations should read. This is the proposed system to prove in the running game, not an approved new visual style:

| Situation | Presentation to develop | What it must accomplish |
| --- | --- | --- |
| Rapid exchange | Compact character portrait integrated with the speaking frame; stable nearby text; visible listener response | Immediate attribution and quick turn-taking without repeated full-screen eye travel |
| Spatial action | Composed scene with the necessary bodies, hands, exits and objects | Make the source action physically understandable; show its consequence before another decorative reset |
| Intimate exchange | Deliberate close or two-person composition, with restrained dialogue placement | Let the listener and the pause carry emotional information |
| Crowded conversation | Compact speaker frame or clearly anchored callout within an established group view | Identify a priest, messenger or offscreen voice without covering the people reacting |
| Solitude or aftermath | Held illustration and a small, finished narration treatment | Give the image room to mean something without turning every pause into a title card |
| Time passage | The screenplay's existing jumps and concise illustrated montage | Show what changed while preserving causal and relationship beats |
| Look closer | Reframing within the scene, related detail, then meaningful authored revelation | Reward attention while preserving the reader's place and non-embodied role |

1. **Resolve the combined conversation and UI design first.** Storyboard the existing Senn/Tessa exchange, Tessa/Mara exchange and multi-person treatment with text and compact character frames in the composition. Judge eye travel, attribution, reactions, dramatic focus, frame edges and controls together. Avoid another independent ornament pass.
2. **Prove the rules through a connected opening sequence.** Carry the design through S001–S005, including the ceremony and window scene that currently lose the cast, and the return from Look closer. Use the three lighting registers and both lighting preferences. Read it continuously at natural pace; record specific failures and stop expansion while its central experience fails. No passing asset count or engine test substitutes for that judgment.
3. **Plan and produce the entire route against its emotional progression.** Account for cast, ages, wardrobe, injuries, setting, action and reading mode through S058. Protect attachment scenes and grief scenes as carefully as spectacle. Author the historical discovery chain separately against the established lore, then integrate its opportunities without compulsory interruptions. Keep incomplete coverage explicit in production records; do not hide it by truncating the story.

This review recommends changing the design decisions that generate screens before producing another large asset batch. The current game remains an incomplete, rejected draft.
