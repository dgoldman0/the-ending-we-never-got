# Near-pillar component for the deterministic duel composition

The empty hall's narrow column originally met the floor around y640. The approved geometry guide places the same impact-side face near the fighters, with the foot around y780. Leaving the earlier distant foot would make the short visible spear section imply an implausible long reach upward and backward into the hall after touching Tessa's foreground dome.

`13-empty-hall-near-pillar.png` moves the mouldings and base down 140 px in GIMP. A masked copy of the original cylindrical shaft continues its material downward without stretching the texture. Two slim, separately masked copies of adjacent floor at the same image height remove the wider old base edges. The original plate remains the bottom layer. No generator call, actor change, weapon change, perspective warp, grading or global resampling was used.

The shaft silhouette and stone pixels at the impact height y279 are unchanged. The entire correction is bounded by x488–647, y517–784. The three stair risers and the remainder of the room are byte-identical to `13-empty-hall.png`. Native output remains 1672×941 opaque RGBA; the five-layer XCF reopens to an exactly matching export. See `near-pillar-verification.json` for hashes and checks; the reproducible GIMP recipe is `art/prompts/s054-duel/batch7/near-pillar-compose.scm`.

Whole plate and native shaft/base/floor joins inspected by Citadel. This is a background component, not acceptance of the final assembled duel. Root reviews the actual whole result before the composition agent uses it; final actor/dome/spear/pillar contact must be checked together.
