# Runtime art production

**Status: current presentation rejected by the user, 16 September 2026.** The existing batch is retained for comparison and functional testing. Reassess components in the [integrated redesign](../../presentation-redesign.md) before reuse or expansion. The historical production/review notes below do not certify acceptable art direction, acting, composition or lighting.

This folder holds purpose-built backgrounds, sprites, expression components and their editable sources. Earlier scene studies remain reference material. The user rejected the initial attempt to use copies of those studies as the game presentation; those runtime copies have been removed.

## Opening production brief

The source is Rebuild 11, S001–S005. Build actual game components first for the connected summoning, confinement and first infirmary encounters. Do not populate later periods with convenient early sprites.

- **Tessa arrival, nineteen:** modern blue zip hoodie, cream T-shirt, dark straight jeans and off-white sneakers; healthy hands. Selected north-infirmary face crop is likeness only, never clothing/injury/exhaustion. An alert, frightened base and an angry questioning face are distinct from cheerful reference poses. No carried grocery bag after its fall. Phone and cloak states are separate.
- **Mara, thirty-two:** existing written face/build, low pinned dark braid, slate military coat, padded vest, trousers, boots, forearm guards, single brass captain bar. Opening dialogue is controlled, then uncomfortable when challenged; no default grin. No late injury, sword draw or shield pose in the apartment. Cloak delivery needs its own component/action.
- **Senn, late fifties:** rounded light-brown face, sandy-gray thinning hair and tended short beard; cream/wheat robes, limited sun embroidery. Persuasive composure, not a permanent villain sneer. Does not physically hold Tessa at the arch.
- **Iven, twenty-six:** medium-brown long face, wide nose, unruly black curls, olive coat, natural broad hands. Attentive and concerned at the first infirmary. Medical apron for treatment is separate from travel clothes. No Harrow damage.

The full body will be inspected even when dialogue presentation crops below the knees. A dialogue portrait is not a literal picture of every narrated action; do not show a conflicting physical action behind the narration. Important action shots require their own staging. Background-only action beats are preferable to a smiling standing sprite during a treatment or collapse.

Chamber layers need separate open/closed portal states. Earth must stay modern and visually distinct. The landing is at the threshold, groceries remain there, and the circle reaches that point. The scholar and mechanism must be subordinate, placed beside the arch. Apartment state changes include open/guarded door → Mara leaves → locked door → chair barricade; no drawing pose while Tessa is still calling at the window.

## Light and review

Neutral sprite masters preserve material/skin identity. GIMP mask and curve layers prepare scene lighting variants. The composited chamber must be almost painfully overexposed; the apartment has very dark cold space with small practical candle illumination. Review full composites and native character crops, transparent edges over both dark and light, hands, body length, feet, background geometry and narrative state. GIMP XCF files must contain useful editable layers/masks and reopen to the delivered pixels.

This is a production log, not user approval. Append specific observations and keep incomplete assets out of runtime.

### Additional opening states

Tessa's phone-only arrival sprite is confined to S001 after the failed call and before the cloak is settled. It preserves healthy hands and the arrival costume. The apartment uses the cloaked phone version until she drops the cloak; later poses cannot carry it back. First treatment is before the badge/mantle ceremony; the formal sprite is after S004's pinning, never before it. The audience hall is a separate place with a chair and temple banners, not the summoning room reused.

Apartment repairs retain the original room outside masked dress, door and chair areas. S002 starts with the closed door and chair at the window; Mara opens it at line 73, leaves and locks it at 106, and Tessa moves the chair at 108. The discarded offered dress is limp cloth, never a headless upright figure.

S005 window pause: Tessa remains in the ceremony outfit, Iven is still the working healer. The window sill seats two; the medical chest stays open. The new gray canvas bag is a provisional design for the source's travel bag, not her fallen grocery bag. Portrait framing excludes their seated/standing lower bodies; the final sitting action uses the environment alone.

## Current delivery

Eight sprite states, nine backgrounds and seventeen editable XCF masters now support the opening chapter. See the [explicit reuse manifest](manifest.json), [manual visual review and coverage limits](review.md), and [running-game QA](../../renpy/QA.md). The rest of the original route is playable in prose; it is not yet fully illustrated.
