# Batch 8 optional S057 sentry horn variation

## Brief before generation

S057, screenplay 2155–2175: the ceasefire terms hold at the lower gate, with sentries remaining on both sides as medical wagons move. Lucan waits by Valcair's covered body, tucks the exposed hand beneath the cloth, then steps aside for the bearers. The current painting holds that act with Lucan, two bearers, the covered body, medical wagons and background sentries.

The optional correction concerns only the four left background sentries' repeated curled horns. Two or three small horn silhouettes may vary while their heads, helmets, faces, uniforms and positions stay. They are unnamed northern military extras; no new cast member or weapon is added. The current composition, evening light, Lucan's already corrected horns and complexion, both bearers, covered body and all other fixes remain exact. Candidate stays outside runtime for the lead's final full/native check.

Built-in image generation supplies a small local donor; GIMP handles masks and exports. This folder keeps the untouched current source and editable master.

## Candidate review

The second sentry's near horn is now a shorter smooth backward curve, while the third, seen from behind, has a pair of small conical horns angled slightly outward. The first and fourth retain their source horns. Native crop and full composition inspection found no displaced head, new face, doubled old horn outline or changed spear/helmet silhouette. The distant focus is retained.

GIMP `master.xcf` has the original source plus three individually masked horn components (second profile; third left and right). Reopened pixels equal `candidate.png`. [verification.json](verification.json) records that changes are confined to two small horn regions and that Lucan, the foreground left bearer, the first/fourth sentries, and the second sentry's face interior are unchanged. The current source is 2240 × 1260 and that native size is retained.

[Exact generation prompt](../../prompts/batch8-optional-horns/s057-sentries.txt), original crop, donor, editable mask specification and native review crop are retained. Built-in imagegen used the visible inspected GIMP crop after local file input proved unavailable earlier in the session. No CLI/API fallback. The shared masked-edit script under `art/prompts/batch7-gray-scar/` compiles `edit-spec.json` into `build.scm`.

**Delivered after root and independent full/native review.** The shorter second-sentry curve and third-sentry conical pair remain rooted in their heads, with no visible doubled outline, stray background patch or displacement. The installed `s057-father.png` equals `candidate.png` and the reopened master export. All 2,045 changed pixels are confined to the distant horn regions; foreground faces, hands, horns, litter and bearers remain exact. This clears the bounded source correction only, not runtime or user approval. No grading, interface or staging work was performed.
