# Original-timeline visual novel — adaptation brief

Status: **ROVEL WORKING CANDIDATE 0.4.0-dev — 17 September 2026.** Production resumed after the [full design review](reviews/2026-09-17-full-design-review/README.md) and realignment. The first five scenes now blend detailed action/quiet illustrations with compact speaker/listener frames. The [current review](reviews/2026-09-17-rovel-work/README.md) records checks and limitations; this is not full-route completion or user approval. The [experience requirements and gates](presentation-redesign.md) remain active. **Look closer / Threads** remains the accepted reader interaction.

The goal is a beautiful, fluid, engaging and **entertainingly painful** original-timeline playthrough that makes the reader care about Tessa and want to save her at the end. Compact character frames for rapid exchanges, deliberate listener reactions, coherent reading/navigation, scene-specific performance and meaningful discovery are core requirements. The next playable milestone is the complete **S001–S005 Rovel sequence**, including the ceremony and window conversation. The full scope remains all 58 scenes and the original endpoint.

The existing text route is traversable: all 58 original screenplay scenes, ten working chapters and the complete ending through **“Do you wish to save Tessa?”** Its five mandatory discovery invitations and six card/quiz inquiries have been removed. The final question currently offers only Return to title; the intended Yes affordance remains an endpoint gap, with post-Yes work deferred. Run [play.sh](play.sh); see [build instructions](renpy/README.md) and [technical QA](renpy/QA.md). Traversal does not certify presentation or completion.

For browser inspection, run `./visual-novel/play-web.sh` from the repository root. It serves the actual Ren'Py web build at **http://127.0.0.1:8042/** and opens your browser. Keep the terminal open; Ctrl+C stops the server. Rebuild after game changes with [build-web.sh](build-web.sh). The browser edition uses the same story, investigations and runtime artwork.

The [route ledger](art/route-coverage.md) records 66 mapped opening pages, 29 room-only pages without the required cast, and 757 prose-only pages: 852 reading pages from 849 source reading blocks. The mapped opening also fails the experience review. **Settings → Lighting → Softened** reduces glare and opens shadows without changing story or discovery state; Intense remains the default. [Lighting provenance](art/lighting/README.md) records the recovered exports and GIMP alternates. This working feature does not clear the surrounding game.

## Adaptation structure

- [Route outline](outline.md): ten candidate chapters from summoning through postwar Bellweir and the question **“Do you wish to save Tessa?”**
- [Complete scene map](scene-map.md): all 58 screenplay scenes, their chapter placement and proposed full-scene or compressed treatment.
- [Look closer / Threads](investigation.md): accepted reader inspection and connected discovery, including the historical thread about humans initiating the war through the first Saint summoning. Candidate availability and historical content still need development.
- [Experience and production requirements](presentation-redesign.md): authority, conversation modes, whole-game goals, S001–S005 milestone, work order and enforceable completion criteria.
- [Pacing and time skips](pacing.md): use the screenplay's existing gaps and compact repeated visits/campaign seasons to make room for investigation.
- [Ending storyboard](ending.md): preserve the complete original ending, then address the player. The user has placed the eventual hopeful transition after the final Yes; its UI/UX and the continuation are explicitly deferred.

The screenplay remains the story authority. The design documents separately mark accepted interaction principles, presentation proposals, new historical material that needs writing, and the existing bridge-seal attribution question. The implementation preserves every screenplay action and spoken word; it has not yet applied the proposed additional montage compression. [Legacy discovery content](investigation-content.md) records what the rejected card/quiz implementation contains. Its provenance is not evidence of a successful discovery experience.

## Setting and character development

The first physical-design pass is documented in [character appearances and wardrobe](../characters/original-visuals.md), [locations and everyday setting](../worldbuilding/original-locations.md), and [objects, effects and visual continuity](visual-continuity.md). These documents distinguish established source anchors from newly filled-in working details. They cover the original cast and screenplay locations. That pass did not generate images or select an art style.

The subsequent [north-infirmary scene study](art/scene-studies/north-infirmary/README.md) uses stormy daylight, following the user's correction. Together with the summoning study it anchors the user's three lighting registers in the [visual direction](art/visual-direction.md). Individual asset selection and production-ready scene coverage remain separate.

See the [art-development index](art/README.md) for current studies and close-up review requirements. Prompt records are kept separately under `art/prompts/`. The [summoning tone study](art/scene-studies/summoning/README.md) uses the user's selected infirmary Tessa likeness and depicts arrival at the threshold, with her dropped groceries beside her and modern Earth still visible. It replaces the rejected attempts, with a targeted carton repair and shared chamber-lighting treatment in GIMP. It remains a reference study; the runtime opening uses new separate background, grocery, portrait and lighting components.

## Scope

Build a visual novel around Tessa's original timeline. [Rebuild 11](../screenplay/original-timeline/source.fountain) supplies the detailed narrative baseline, supported by the [original story map](../story/original-timeline.md), character notes and worldbuilding. Player investigation can uncover additional detail and historical context.

Neri's incursion and the reincarnated versions of Iven and Mara are deferred. The active adaptation covers Tessa's story through postwar Bellweir, then the user-requested question **“Do you wish to save Tessa?”** to the player. The eventual Yes comes only after that complete ending. Its transition and post-Yes UI/UX are deferred while the original playthrough is developed. In this timeline, Iven and Mara have real local lives and no Earth or VN memories.

Ren'Py is the chosen engine, with local desktop and browser inspection builds. One original route has optional Look closer / Threads discovery; event-changing branches are not approved. Release title, final interface, production assets, budget and measured playtime remain open. **A Light for the Last Winter** is an earlier working title for the in-fiction VN, not an approved title for this release. The screenplay opening's approximate thirty-minute intention is not a VN playtime requirement.

## Narrative baseline

- Tessa is an American nineteen-year-old summoned without consent. Her desire to reach her mother remains central.
- Preserve the established distinctions between purification, healing and sanctuary, and between institutional authority and actual access.
- Develop Iven, Mara, Elin, Lucan and Bellweir's people through relationships and consequential choices as well as the war.
- Harrow destroys Tessa's trust in Lucan. Evidence, tactical cooperation and forgiveness remain separate.
- The current original outcome remains the baseline: Iven and Mara die, Tessa defeats Valcair and retains a lasting hand injury, and her worthwhile future includes an unresolved search for home. The focus change does not itself approve alternate endings or rescues.

Adaptation can expand scenes and change presentation. Track additions and their consequences explicitly; a prose or interface change can still alter what someone knows, what they can do, or why they act. Preserve the Fountain manuscript as the reference while developing the VN separately.

## Human origins of the war

The **player can learn through investigation that humans started the ancient war through the first Saint summoning**. The user has explicitly connected the initiating aggression to that first summoning; Tessa's is later. See [war and history](../worldbuilding/war-and-history.md) and [project continuity](../project/continuity.md). Humanity later forgot, obscured or recast that aggression, which underlies Valcair's distrust. The precise first operation, campaigns, dates, participants, agreements and Valcair's firsthand experience are still unresolved.

Rebuild 11 omits this revelation. Existing notes already allow explicit, reliable optional lore in the source VN. The player can discover that lore while the original cast's knowledge boundaries remain intact.

This is a player discovery, not a planned revelation to Tessa, Iven, Mara, Elin or Lucan. Do not transfer unlocked player knowledge into their dialogue or decisions. [Look closer / Threads](investigation.md) can lead from inspected details into additional authored material or historical cutaways. The specific historical scenes and records still need to be written. These knowledge restrictions guide development and must not appear as disclaimers in the player interface.

Humanity's initiating aggression does not excuse Valcair's present atrocities or remove Vask's responsibility. Historical truth, responsibility for Harrow, and Tessa's personal trust are related but distinct matters.

## Reader discovery and agency

**Look closer** lets the player inspect illustrated details, bring related moments alongside them and follow connections into additional material. **Threads** revisits those relationships. The player acts as a reader with editorial access; there is no player body, first-person travel, inventory or questioning of characters. Return preserves the exact narrative point. There are no comprehension quizzes, answer grading or mandatory clue quotas.

The old explanation cards and quizzes have been removed. The current first-night prototype still requires redesign for meaningful payoff and fluid in-scene attention; removing quizzes did not complete discovery. Essential relationships and consequences remain in the main route. Conversation branches and their effects would require a further decision and connected writing; no false rescue choices are introduced to make the interface appear interactive.

The adaptation retains the screenplay's scenes outside Tessa's viewpoint, including Harrow's planning. Its modern discovery examines events, evidence and limited witness knowledge; it must not pretend the player has not seen the order. Any change to the source's information order remains an explicit adaptation proposal.

## Remaining production

1. Prove the [connected S001–S005 milestone](presentation-redesign.md#next-playable-milestone--complete-rovel-sequence), starting with conversation/reading composition and then integrated performances, action, interface, lighting and reader discovery. Failed experience gates prevent batch expansion.
2. Author meaningful source-backed connections and the additional ancient history before producing their evidence or historical cutaways. Keep player knowledge separate from cast state and production caveats out of the reader experience.
3. Produce the full route against its emotional progression and [coverage ledger](art/route-coverage.md), preserving attachment scenes, consequences, four-year physical change and source time skips. Measure actual reading pace with and without discovery before further compression.
4. Complete original-route sound, transitions, accessibility and platform checks, then the full S058-to-question interaction including a deliberate Yes. Follow [the endpoint boundary](ending.md): post-Yes visual treatment and continuation remain deferred.

## Working references

- [Project guide](../project/README.md) and [continuity](../project/continuity.md).
- [Tessa](../characters/tessa.md), [supporting cast](../characters/ensemble.md), [magic](../worldbuilding/magic.md), and [setting](../worldbuilding/setting.md).
- [Knowledge and reveals](../story/knowledge-and-reveals.md), whose existing matrix describes the screenplay and earlier incursion development.
- [Working method](../development/working-method.md): work in connected interactions, read wider than the drafting window, and check downstream consequences. VN validation will also need to cover reachable branches and state-dependent text once implemented.
- [Open decisions](../development/open-questions.md), with active VN work separated from deferred incursion questions.
