# The Ending We Never Got — project guide

This is the project-wide working reference, recovered on 16 September 2026. The current branch is `current-draft`. The screenplay is one component of a larger double-isekai story.

## Current focus — original-timeline visual novel

The active project is a **Ren'Py visual novel of Tessa's original timeline**, driven by Rebuild 11. It should be beautiful, fluid and “entertainingly painful”: attachment, warmth and suffering must earn the player's wish to save Tessa. Ten proposed chapters cover all 58 screenplay scenes through the complete Bellweir ending and fade, then **“Do you wish to save Tessa?”** and its intended Yes choice. Work on the hopeful presentation after Yes is deferred.

**Alignment as of 17 September 2026:** a text-traversable game and local web preview exist, but runtime 0.3.2 remains rejected and incomplete. The [full design review](../visual-novel/reviews/2026-09-17-full-design-review/README.md) records the failures. The [active experience brief](../visual-novel/presentation-redesign.md) sets requirements and gates; the next playable milestone is the complete S001–S005 sequence, including compact conversation frames, continuous cast performance, a crafted interface, jarring lighting with a persistent Softened option, and worthwhile discovery. This milestone does not reduce the full-route scope.

The incursion timeline—Neri's presence and Iven/Mara's reincarnated fan memories—is deferred. Its existing material remains available for later development. Original Iven and Mara remain natives without those memories.

Through **Look closer / Threads**, the player can inspect details, follow connections and discover that humans initiated the ancient war through the first Saint summoning. The player has no body or actions in the story. The [interaction contract](../visual-novel/investigation.md) identifies candidate availability spans; these are not compulsory rounds, quizzes or menu interruptions. The historical particulars and evidence still need authoring. This knowledge belongs to the player. The [pacing plan](../visual-novel/pacing.md) uses existing time jumps and proposes compression that preserves causal and relationship developments. Rebuild 11 remains unchanged.

## Read in this order

For active VN work, start with [VN instructions](../visual-novel/AGENTS.md), the [experience brief](../visual-novel/presentation-redesign.md), the relevant complete [screenplay interaction](../screenplay/original-timeline/source.fountain), and its character/location/continuity notes. The [route outline](../visual-novel/outline.md), [full review](../visual-novel/reviews/2026-09-17-full-design-review/README.md) and [coverage ledger](../visual-novel/art/route-coverage.md) distinguish the intended route from actual implementation.

For wider-story background, including deferred material:

1. [Premise, narrative levels and tone](premise.md)
2. [Continuity decisions and status rules](continuity.md)
3. [Neri](../characters/neri.md), [Tessa](../characters/tessa.md), and [the supporting cast](../characters/ensemble.md)
4. [The fantasy setting](../worldbuilding/setting.md), [magic](../worldbuilding/magic.md), [Astravus and the future](../worldbuilding/astravus-and-future.md), and [familiars](../worldbuilding/familiars.md)
5. [Original-timeline outline](../story/original-timeline.md), [altered-timeline plan](../story/altered-timeline/README.md), and [knowledge/reveal matrix](../story/knowledge-and-reveals.md)
6. [Archetype references](../references/archetypes.md) and [working method](../development/working-method.md)

For the active VN's physical design, read [character visuals](../characters/original-visuals.md), [location designs](../worldbuilding/original-locations.md), and [prop/effect continuity](../visual-novel/visual-continuity.md). Distinguish written working designs from user-selected references; Tessa's selected storm-infirmary likeness remains established.

## Current manuscript

[Staged Rebuild 11, original Tessa timeline](../screenplay/original-timeline/source.fountain) is the current detailed screenplay. Its source SHA-256 as delivered was `e5c4f7b0af53249752d2d747ebfe756bc084c76002040282d8b7cd93253a6c88`. This documentation import does not edit it; later edits are Git commits, listed in the [editorial record](../screenplay/original-timeline/review/editorial-record.md#changes-after-rebuild-11).

The altered timeline has extensive earlier development but has not received the eleven rounds applied to the original opening. Its recovered events are preserved as development material, with conflicts and superseded assumptions identified. They are not silently promoted to current canon.

## Directory purposes

- `project/`: premise, decisions and navigation.
- `worldbuilding/`: places, institutions, magic, future civilization and familiar system.
- `characters/`: protagonists, relationships, working designs and supporting cast.
- `story/`: original and altered timelines, consequences and disclosure order.
- `references/`: all eight archetypes and the retained craft/research context.
- `development/`: open work, source provenance, editorial method and historical-draft cautions.
- `visual-novel/`: the active original-timeline VN adaptation scope and next steps.
- `screenplay/`: the current original-timeline manuscript and its editing instructions.

Use stable filenames. Make future changes in Git rather than adding another numbered draft directory. The abandoned chunked import and temporary branches are not part of this working branch.
