# Original timeline — experience and production requirements

**Active production requirements — 17 September 2026.** The user authorized production after realignment following the [full design review](reviews/2026-09-17-full-design-review/README.md). Runtime `d0c3020` / web 0.3.2 remains the rejected baseline. **0.4.0-dev is a new working candidate**, with S001–S005 integrated for review. [Current evidence and limits](reviews/2026-09-17-rovel-work/README.md) determine its status; neither this brief nor a successful build clears a scene.

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

**Preserve the blend.** Rich, detailed scene art remains central to arrivals, physical action, ceremonies and quiet relationship moments. Compact frames support faster exchanges within that illustrated sequence. They are an additional presentation mode, not a replacement of detailed scene work. The current Rovel plan contains 38 action pages, 10 quiet pages and 47 compact exchange pages; those counts describe this sequence and are not a quota for later scenes.

Actual interface materials and ornament remain design work. Aged metal, mineral surfaces and botanical forms are possible references, not a requirement to preserve the current gilt frame or cropped crest. Make complete edges and appropriate variants for their intended sizes. Native text and controls need room, legible hierarchy and matching visible/hit/focus areas. Keep utility positions stable when Look closer appears; distinguish advancement, rollback and return from inspection. Saves need recognizable narrative context.

Compose title, starting flow, chapter transitions, reading, inspection, Threads, history, saves, settings and endpoint as one visual language. Resolve redundant starts and interruptions through flow design. Review long/short lines and larger text in the complete screen. Correct reading surfaces without lifting scene exposure into a comfortable default.

## Next playable milestone — complete Rovel sequence

**Target: title/start through S001–S005, ending with Tessa making room for Iven on the window sill.** This replaces the narrower S001–S003 production target. It is a milestone within the full route, not authorization to truncate the screenplay or hide later gaps.

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

1. **Design connected reading flow and performances.** Map beats to modes, important listener, expression/gesture change, reading location, transition and intentional hold. Resolve compact frames and utility layout with real dialogue. Rough layout experiments are development artifacts, not completed art.
2. **Produce the components needed for that sequence.** Use written designs and selected references, the current built-in image generator for tailored visuals, and GIMP for masks, repairs, composites, grading and useful layered masters. Compare to authoritative likeness and source state after each operation. Restart without image inputs when references keep forcing a rejected feature. Do not begin another generic batch of every character key.
3. **Integrate and review S001–S005 continuously.** Correct failed experience gates before expanding the design into another batch. Keep full-route gaps visible in the ledger. Planning and historical authoring can proceed without claiming production clearance.
4. **Carry the proven design through the route.** Give S006–S009's training, meal, checkers, market and boat the same care as spectacle. Follow the [chapter arcs](outline.md), preserving displacement, Gray Scar cooperation, reunion/laughing portrait, Harrow and its aftermath, accumulated war wear, Mara's final exchange and Bellweir's continuing life. Recheck recurring places, ages, outfits and living/dead boundaries.
5. **Complete discovery and the original endpoint.** Author the initiating history and reliable player-facing connections before producing artifacts/cutaways. Integrate optional availability without interrupting losses or requiring knowledge. Complete S058, its fade and a deliberate Yes affordance at the final question; response handling must respect the deferred post-Yes scope in [ending.md](ending.md).

Audio must eventually support spaces, performance, transitions and silence; music cannot rescue weak acting or flow. Its absence remains production work. Measure reading duration in human-paced play, separately with and without discovery, rather than inferring it from automated traversal.

## Scene completion gates

The unit of completion is a connected scene, its entry/exit transitions and any optional reader detour. These are internal quality gates, not new user-permission steps. Failure sends work back to the affected design/component; it blocks completion claims and expanding a failed presentation into another batch. Already authorized corrections do not require another approval request.

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

The candidate implements compact performances, related dialogue/narration/utility surfaces, a single Begin and three direct reader comparisons. Remaining work includes final connected-experience clearance, later scene coverage and transitions, ancient history/evidence, later wardrobe/age/performance variants, sound, human reading-duration measurements and endpoint response storage/revisit behavior. These are not reasons to reopen settled scope, Tessa's identity, lighting/Softened, reader-only agency, the first-summoning war origin, source consequences or the placement of Yes.

The authorized production sequence remains linear: resolve the Rovel experience gates before expanding its presentation into another art batch. Detailed work and review records distinguish implemented components from experience clearance.
