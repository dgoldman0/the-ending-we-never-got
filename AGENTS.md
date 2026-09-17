# Project instructions

## Visual novel

Before any work on the Ren'Py visual novel, read and follow [visual-novel/AGENTS.md](visual-novel/AGENTS.md). This includes story adaptation, scene planning, image generation, GIMP editing, asset management, and changes to shared character or worldbuilding files made for the VN. The local instructions record the user's visual references and corrections; do not rely on an old prompt or generated image instead.

The accepted reader interaction is **Look closer / Threads**. Runtime `d0c3020` / web 0.3.2 remains rejected and incomplete; `529a359` records the [full design review](visual-novel/reviews/2026-09-17-full-design-review/README.md). The [experience brief, next milestone and completion gates](visual-novel/presentation-redesign.md) are the active production plan. Complete scenes must integrate compact character frames for rapid exchanges, clear speaker association and listener reactions, physically workable blocking, high-quality scene art, an expressive interface and fluid reading/navigation. Preserve jarring scene light with the persistent Softened option. Review the connected experience and every coverage boundary; isolated images and engine tests do not clear these gates. The next playable milestone is the complete S001–S005 sequence; the [route ledger](visual-novel/art/route-coverage.md) tracks the full original route through its ending.

When revising the game and rebuilding, make sure that the game experience is beautiful, fluid, and enjoyable. Evaluate the full dimensions of the game experience from start to completion, rather than simply considering individual components.

**Latest rejection, 17 September 2026:** the user rejected the 0.4.0-dev Rovel attempt for its ugly, intrusive interface and poorly composed compact portraits. It is another failed attempt, retained for diagnosis; see the [rejection and historical review](visual-novel/reviews/2026-09-17-rovel-work/README.md). Earlier favorable inspection notes do not clear it. Preserve the requirement to blend richly detailed scene illustrations with compact speaker/listener frames; the failed execution does not cancel that requirement.

## Commit

### Messages

Use rich commit messages that include multiple phrases explicitly stating the details of the commit.

### Pacing

Commit whenever reasonable progress points in terms of code, documentation, design, or similar are met.
