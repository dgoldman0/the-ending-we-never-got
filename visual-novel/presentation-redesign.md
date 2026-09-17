# Original timeline — experience and production requirements

**Active requirements after another rejection — 17 September 2026.** Version **0.4.0-dev is failed**, archived at `1bb6d76`; see the [illustrated failure analysis](reviews/2026-09-17-rovel-rejection/README.md). Its 95 mapped pages do not clear the UI or portraits. Version 0.3.2 also remains rejected. The [visual production controls](production-controls.md) address the wrong visual judgments that earlier reviews accepted. Current work is documentation/control only; future production first delivers a small finished design proof.

## Goal and scope

Create a beautiful, fluid, engaging visual novel whose original timeline is **“entertainingly painful.”** Let the reader know and care about Tessa through her attention, humor, warmth, relationships and suffering. The losses must land because the preceding life mattered. The complete experience should draw the player toward wanting to save her at the final question.

The discomfort belongs to the fictional atmosphere and emotional experience. Reading, understanding who speaks and using the controls must remain clear and fluid.

[Rebuild 11](../screenplay/original-timeline/source.fountain) drives events, dialogue, chronology and character knowledge through **all 58 scenes**, including the complete final Bellweir interaction and fade. Only then ask **“Do you wish to save Tessa?”** The intended Yes belongs there. No earlier rescue choice, alternate original outcome or discovery-completion requirement is introduced. Neri's incursion, reincarnated Iven/Mara, the shattering transition and all post-Yes UI/UX remain deferred.

The player controls reading pace and editorial attention through **Look closer / Threads**. The player has no body, inventory, travel, interrogations or actions in the fiction. Additional historical discovery must establish that humans began the ancient war through the **first Saint summoning**; that knowledge belongs to the player. Specific historical events and evidence still require authoring.

The current adapter preserves every screenplay word. Presentation and narration changes can be proposed as adaptation work, with source mapping and consequences recorded. They are not automatic screenplay rewrites or permission to omit relationship development. Use existing time jumps and montage opportunities in [pacing.md](pacing.md).

## Authority and status

| Reference | Its job |
| --- | --- |
| User decisions and [local instructions](AGENTS.md) | Binding corrections, selected references and task scope; newer user direction takes precedence |
| Screenplay, [character designs](../characters/original-visuals.md), [locations](../worldbuilding/original-locations.md), [continuity](visual-continuity.md) | Source facts and explicitly labeled working physical designs; unspecified details do not become canon through a render |
| This brief | Experience requirements, next milestone, production order and completion gates |
| [Visual production controls](production-controls.md) | Concrete failure examples, comparative visual judgment, an early finished proof and demonstrated direction before expansion; technical checks cannot supply artistic judgment |
| [Outline](outline.md), [scene map](scene-map.md), [pacing](pacing.md), [ending](ending.md) | Full-route structure and adaptation proposals; chapter boundaries are not fixed story facts |
| [Discovery contract](investigation.md) | Reader agency, content payoff, knowledge separation and historical authoring scope |
| [Visual direction](art/visual-direction.md) and selected references | Likeness, materials, lighting and image review; a tone study is not a runtime scene |
| [Route ledger](art/route-coverage.md) / [production inventory](art/production-inventory.md) | Actual runtime coverage / required assets and available studies; neither grants artistic clearance |
| [QA](renpy/QA.md) and dated reviews | Evidence with build, platform and inspection limits; historical passes never overrule later rejection |

Track asset availability, manual inspection, integration, scene-gate result and user selection separately. A file, generated image, commit or favorable old review does not imply approval. Missing evidence remains unreviewed; observed defects remain failed. The full review is the baseline diagnosis, not a replacement art reference.

## Experience requirements

| Requirement | What the game must deliver |
| --- | --- |
| Conversation | Compact character frames for rapid exchanges, immediate speaker recognition and specific listener reactions; preserve the important faces, hands and actions |
| Reading continuity | A stable, predictable reading area within an exchange; purposeful shot/mode changes; no automatic cross-screen box jump merely because the speaker changes |
| Scene direction | Workable movement, entrances, exits, mechanisms and prop ownership; cast persists through narration unless the selected shot intentionally excludes them |
| Interface beauty | A coherent family of finished dialogue, narration, inspection and utility surfaces, composed with artwork; deliberate typography, spacing, ornament and focus treatment |
| Painful atmosphere | Bright scenes nearly blinding at the dramatic focus; ordinary scenes retain discomfort; dismal scenes visibly dreary or starved of light. Preserve human warmth within those circumstances |
| Reader controls | Intense by default, persistent Softened before/during play, coordinated scene/cast/detail grades; larger text, stable controls, keyboard access and visible focus in complete layouts |
| Visual consistency | Established faces, age progression, complete wardrobe changes, faction marks, injuries, proportions, materials and shared light; no drift across generations |
| Discovery | Inspectable details and meaningful relationships that reward attention, including additional authored material; exact story return and revisitable Threads without forced homework |
| Emotional progression | Attachment, competence, coercion, trust, betrayal, grief and continuing life remain legible through performance and pacing; moments receive appropriate visual weight |
| Full-route completion | The same standard through S058 and the final question; a finished opening or traversable prose route is not a finished visual novel |

## Presentation modes to develop together

These are working implementation directions, not approved frame artwork or pixel dimensions. Choose the treatment for the dramatic beat, then compose text and people together.

| Situation | Treatment | Continuity rule |
| --- | --- | --- |
| Rapid exchange | Compact face/bust frame paired with dialogue in a stable reading zone | The portrait is the nearby visible speaker; change expression and listener response with the line, retaining spatial context where needed |
| Staged conversation | Two-person/group view with clearly associated dialogue | Use shot-specific placement when useful. A compact frame can identify a distant priest, messenger or offscreen voice without covering foreground reactions |
| Physical action | Purpose-built composition, action states and useful inserts | Establish geography first; preserve causes/consequences across cuts; no standing portrait over incompatible action |
| Intimate or quiet beat | Close view, held two-person composition or aftermath illustration with a small finished narration treatment | Let attention, touch and silence carry meaning; a hold needs purpose, without generic title-card interruptions |
| Time passage | Existing screenplay skips and concise illustrated montage | Show changed people and circumstances while retaining causal information |
| Look closer | Reframe a detail, bring a related view alongside, follow its meaningful connection | Keep the originating scene perceptually present and the return path clear; reader operations do not require separate menu pages for every step |

Do not lock every exchange to giant standing sprites or make every sentence a full illustration. Compact framing needs designed expressions and identity consistency, not indiscriminate crops of rejected renders. Narration has a related but distinct treatment; its appearance is not a cue to remove actors.

The rejected Rovel implementation's head-only portraits, universal compact-dialogue mode, removal of stage actors and large fixed reading panel are not requirements. Follow the [portrait and layout standards](production-controls.md#compose-portraits-before-automating-crops). Compose text, people and controls together; a portrait file's presence does not prove good attribution or acting. Evaluate short replies as critically as long paragraphs, with important scene action visible while UI remains present.

**Preserve the blend.** Rich, detailed scene art remains central to arrivals, physical action, ceremonies and quiet relationship moments. Compact frames support faster exchanges within that illustrated sequence. They are an additional presentation mode, not a replacement of detailed scene work. The current Rovel plan contains 38 action pages, 10 quiet pages and 47 compact exchange pages; those counts describe this sequence and are not a quota for later scenes.

Actual interface materials and ornament remain design work. Aged metal, mineral surfaces and botanical forms are possible references, not a requirement to preserve the current gilt frame or cropped crest. Make complete edges and appropriate variants for their intended sizes. Native text and controls need room, legible hierarchy and matching visible/hit/focus areas. Keep utility positions stable when Look closer appears; distinguish advancement, rollback and return from inspection. Saves need recognizable narrative context.

Compose title, starting flow, chapter transitions, reading, inspection, Threads, history, saves, settings and endpoint as one visual language. Resolve redundant starts and interruptions through flow design. Review long/short lines and larger text in the complete screen. Correct reading surfaces without lifting scene exposure into a comfortable default.

## Next production delivery — bounded design proof

When production is requested, compare two or three materially different complete layouts using the same real scene/text; finish one short connected exchange. Read the complete source interaction first. Include speaker/listener changes, an action/narration beat, real short/long dialogue and relevant lighting/text-size conditions. Include a worthwhile discovery/return where it belongs to the passage. Preserve detailed illustrations. The [controls](production-controls.md) define visual comparison, portrait composition and the early delivery boundary.

Deliver the actual alternatives, recommendation and proof before expanding them. The producing model’s favorable review cannot alone establish the new direction after these failures; use the user’s response to the concrete result, or a visual reviewer explicitly designated by the user. Resolve obvious defects first. This delivery does not clear a whole source scene or reduce the route scope.

## Next playable milestone — complete Rovel sequence

**Subsequent connected target: title/start through S001–S005, ending with Tessa making room for Iven on the window sill.** Begin after the proof has established the visual direction through actual evidence and response. This is a milestone within the full route, not permission to truncate the screenplay or hide later gaps.

| Scene | What the milestone must prove |
| --- | --- |
| S001 — summoning | Interrupted stride, threshold groceries, distinct Earth, attempted return and remote lever closure; quick Tessa/Senn exchanges and crowd pressure; Mara's approach/cloak in source order |
| S002 — apartment | Compact Tessa/Mara exchange develops into blocked departure; candle, cloak, guard, lock and chair stay coherent; deeply dark solitude and drawing get space |
| S003 — treatment | Multi-person attribution/reactions; blue healing does not stop corruption, white purification clears it, missing fingers remain; Iven's care and Tessa's untouched cup matter alongside the effect |
| S004 — ceremony | Formal wardrobe, badge/mantle, Orra/messenger at the door, Olan in the crowd, announcement, sleeve grip/refused chair, Iven below the dais and then called up; no empty-room substitute |
| S005 — window | Tessa/Iven present; her bag beside her, medical chest open, mother/Mara/guards below as written; she makes room and he sits, delivering the final relationship beat |

Include the relevant title/start and utility screens, all three lighting registers where the source permits, both lighting preferences, standard/larger text, mouse/keyboard, and optional inspection/connection/Threads/return. Define a concrete discovery payoff before building its screens. The current four-screen phone/drawing explanation does not clear that requirement. A source-grounded introductory connection must make a worthwhile detail or relationship perceptible; it does not substitute for the later ancient-war reveal.

Read the complete source interactions and the [working spatial plan](art/opening-sequence/README.md) before storyboarding. The lever's separate operating bay and the plan's dimensions are provisional staging, not canon. Recheck routes, operating space, screen direction and props in the produced sequence. Preserve useful spatial repairs without promoting rejected renderings to approved references.

## Production order

1. **Honor the current task and establish a visual standard.** The present documentation task does not authorize production. On a later production request, open the illustrated failure examples and authoritative references. Make complete-screen alternatives before generating isolated frame or portrait components; explain the actual visual differences.
2. **Compare layouts and finish the proof.** Map its beats to modes, important listener, expression/gesture, reading location, transition and intentional hold. Produce only the components needed for that proof. Use selected references, the built-in generator and controlled GIMP work; inspect actual final composites. Resolve visible failures before technical audit expansion.
3. **Deliver the finished proof before further production.** Retain the comparison, connected-play evidence, candid visual verdict and open defects. Establish direction from the concrete result and response; missing response is not approval. Routine corrections already authorized need no repeated permission request.
4. **Integrate and review S001–S005 against the established visual examples.** Address the actual response and compare later screens to the demonstrated standard, including utilities/discovery and entry/exit transitions. Failed or uncertain visual quality stops expansion. Keep full-route gaps visible in the ledger.
5. **Carry the proven design through the route in small connected increments.** Give S006–S009's training, meal, checkers, market and boat the same care as spectacle. Follow the [chapter arcs](outline.md), preserving displacement, Gray Scar cooperation, reunion/laughing portrait, Harrow and its aftermath, accumulated war wear, Mara's final exchange and Bellweir's continuing life. Recheck recurring places, ages, outfits and living/dead boundaries.
6. **Complete discovery and the original endpoint.** Author the initiating history and reliable player-facing connections before producing artifacts/cutaways. Integrate optional availability without interrupting losses or requiring knowledge. Complete S058, its fade and a deliberate Yes affordance at the final question; response handling must respect the deferred post-Yes scope in [ending.md](ending.md).

Audio must eventually support spaces, performance, transitions and silence; music cannot rescue weak acting or flow. Its absence remains production work. Measure reading duration in human-paced play, separately with and without discovery, rather than inferring it from automated traversal.

## Scene completion gates

The unit of completion is a connected scene, its entry/exit transitions and any optional reader detour. A bounded proof has its own limited verdict and cannot clear a whole scene. These are internal quality gates, not permission requests for routine edits. Failure or missing required evidence blocks expansion under the [production controls](production-controls.md); already authorized corrections continue within their scope. Mark the rejected Rovel interface and portrait presentation failed, not merely awaiting another review.

| Gate | Required evidence | Failure and response |
| --- | --- | --- |
| 0. Whole experience | Read the sequence at natural pace in the running game; record attention, flow, and where warmth, pressure and loss land | Awkward, monotonous, cheap-looking or emotionally flat presentation remains failed; revise direction before batch expansion |
| 1. Source and staging | Source-linked beats, roster, chronology, routes, entrances/exits, props/mechanisms; compare adjacent actions | Invented participants, knowledge leaks, obstructed levers, relocated groceries or impossible contact require staging correction before polishing |
| 2. Conversation and performance | Deliberate compact/staged modes, attribution and listener reactions; cast coverage through narration and explained intentional exclusions | Frozen incompatible gestures, ambiguous speech, absent actors or automatic box travel require performance/layout correction |
| 3. Art, identity and light | Open pixels at playing size/native detail; compare likeness, age, wardrobe, injuries, anatomy, edges/contact, symbols and shared light; verify final exports | Drift, malformed bodies, poor composites, comfortable default lighting or isolated Tessa glare require repair/replacement. Generation and XCF saves never clear the gate |
| 4. Complete interface | Inspect all screen types with short/long text, larger type, three registers and Intense/Softened at 1280×720 and a larger window; assess smaller-window legibility | Cut frame edges, clipped glyphs, hidden gestures, moving controls, wrong hit areas or an incoherent screen family require a composed UI correction |
| 5. Discovery and return | Play entry/detail/connection/Threads/exact return; identify the reader's gain; verify keyboard/list access and knowledge boundaries | Repetitive menu essays, pixel hunts, quotas, cast knowledge transfer or wrong return points require payoff/flow correction |
| 6. Technical and route regression | Source preservation, save/load/rollback, lighting persistence, package contents and endpoint; native/browser results separate; check every boundary as coverage grows | Missing files or wrong state/platform behavior require correction. Technical passes never override experience failures or clear missing later scenes |

Record build/scene/source span, platform/window/settings, what was actually read or visually opened, observations, pass/fail/unreviewed status and the concrete remaining correction. A failure list is not a pass. Crops, geometry checks and traversal supplement manual experience review. User rejection supersedes an earlier assistant pass.

## Current baseline and open work

The [ledger](art/route-coverage.md) now records **95 mapped opening pages and 757 prose-only pages**, across 852 reading pages / 849 source reading blocks. S004–S005 have source-specific cast/action coverage rather than the earlier empty-room fallback. Availability counts do not clear their experience gates. The rejected baseline and its documented UI/cast failures remain comparison evidence.

The failed implementation contains compact performances, dialogue/narration/utility surfaces, a single Begin and three direct reader comparisons. The UI/portrait direction requires a new bounded proof; it is not a final-polish task. Remaining route work includes later scene coverage/transitions, ancient history/evidence, wardrobe/age/performance variants, sound, human reading-duration measurements and endpoint response storage/revisit behavior. These are not reasons to reopen settled scope, Tessa's identity, lighting/Softened, reader-only agency, the first-summoning war origin, source consequences or the placement of Yes.

Current authorization ends with the archive and documentation/control update. When production is requested, establish and deliver the small finished proof first. The next sequence must follow a demonstrated visual direction rather than another self-certified batch. Detailed records distinguish actual visual judgments from component availability and technical evidence.
