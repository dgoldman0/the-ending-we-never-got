# QA — current experience failed; requirements realigned

**17 September 2026: 0.4.0-dev working candidate.** See [current review](../reviews/2026-09-17-rovel-work/README.md) for native/browser evidence, manual inspection and remaining experience gates. Native functional tests pass 7 cases / 152 assertions; this does not clear art or later route coverage. The evidence below is historical and retains its original limits.

The review traversed all **852 reading pages / 849 source reading blocks**. It manually inspected selected screens and interactions, not all 852 pages at human reading pace. It found no compact speaker-frame mode, excessive dialogue-box movement, frozen reactions, unfinished frame edges, weak discovery payoff, unstable controls and a Threads caption partly outside its hit area. The [ledger](../art/route-coverage.md) records 66 mapped opening pages, 29 room-only pages and 757 prose-only pages. The final question exists, but its intended Yes choice does not.

Geometry checks did not reproduce offscreen story glyphs in the tested layouts. They do not dismiss the user's clipping report or clear the interface. Native/browser results, manual pixel inspection, continuous human-paced reading and automated traversal must remain distinct evidence.

The next build must meet the [experience and completion gates](../presentation-redesign.md#scene-completion-gates) across connected S001–S005, including compact conversations/listener reactions, cast through narration, interface/flow, discovery and return, both lighting preferences, standard/larger text and mouse/keyboard. Record build, source span, window/platform, actual manual scope and concrete failures. A technical pass cannot clear a failed experience or missing later scenes. Final-route verification must eventually exercise the deliberate Yes affordance after S058/fade, without developing the deferred post-Yes interface.

## Historical 0.3.2 component and functional evidence

The following describes earlier checks of this same rejected runtime, not new checks during realignment. The [component review](../art/opening-sequence/review/realignment-review.md) records that pass's exact inspection scope.

### Functional evidence

- The native Ren'Py 8.5.3 suite passed **6 cases / 68 assertions** in 46.859 seconds: reading/discovery, all opening scene states, save/restore, complete original route to the separate ending question, larger text, and the new lighting preference.
- The preference case switches title and in-story images, checks cast and legacy background paths, follows the first-night connection, and loads a save made in Softened while Intense remains selected. Story position and discovery knowledge survive independently of the persistent preference.
- After replacing the unchanged legacy alternatives with actual GIMP exports, the focused lighting case was rerun: **1 case / 11 assertions passed**, 5 cases skipped by selection. Only the affected case was repeated after that asset-only correction.
- The source adapter preserves 58 scenes and 11,175 words. Corrected reporting: 849 source reading blocks produce 852 reading pages; the final fade is separate. Source SHA256 remains `e5c4f7b0af53249752d2d747ebfe756bc084c76002040282d8b7cd93253a6c88`.
- The browser export check inspects `game.zip` for all **119 required art files**, including both lighting treatments. A previous export rule pruned opening-art directories before specific file rules could match; directory rules now precede exclusions. A second check rejects identical “alternate” exports after review caught unchanged legacy fallback copies.
- Selected new GIMP masters were reopened and their visible exports compared against delivered pixels. Editable source corrections and replacement grades remain separate. This is reproducibility evidence, not an art pass.
- All 11 additional softened legacy masters reopened and reproduced the delivered RGBA pixels exactly. Their two detail crops derive from the same corrected drawing master. All 52 lighting pairs now differ, and all required images are in the rebuilt web package.

### Browser evidence from that pass

The WebAssembly game was run in isolated Chromium at 1280×720. The connected S001–S003 sequence traversed and captured all 66 mapped states. Manual inspection opened selected browser captures across all three scenes, supported by native checks of the other compositions; the review lists exactly which browser images were opened.

Browser interaction exercised Look closer, an enlarged detail, the related phone, following the home connection, returning to the exact source page, manual saves before/after discovery, explicit slot loading, keyboard menu return and larger text. Version 0.3.2 separately exercised Lighting from the title and during reading: both settings persisted after a page reload; loading the saved first-night connection retained the current Intense setting at scene 2, line 112, page 0 with `home` followed. Actual screenshots of settings, both arrival/cast/night treatments, the softened title and connection, and the loaded intense scene were opened manually.

The final web rebuild was reloaded and both S004/S005 background treatments switched in place without advancing their source lines. All four browser images were opened: the softened hall has restrained stone/window highlights and the softened later window has gentler daylight. Their absent cast remains a scene-completion failure in both modes.

Browser save export/import, fullscreen and other browsers remain unverified. The local Linux 0.1.0 archive is an older package, not this build. No complete manual 58-scene visual route review, ancient-war discovery chain, audio pass or post-Yes presentation is claimed.

## Historical checkpoint: 0.3.0 rejected and incomplete

The user rejected the new opening’s lighting and interface, and the missing cast after that opening. No visual completion gate is cleared. Native functionality passed four cases / 56 assertions; a separate larger-text case passed its return-state assertion but exposed further visual collisions. The web export launched as 0.3.0; connected browser review remains incomplete. Earlier records below are history, not current artistic clearance.

## Historical 0.2.0 presentation checkpoint, 16 September 2026

**Result at that checkpoint: presentation failed.** The user rejected the partial replacement as well as the first playable. That build lacked cast/performance coverage, speaker-positioned dialogue and a convincing interface; the opening's lever placement needed spatial redesign. These observations describe 0.2.0, not the later staging changes. No finished connected sequence was established.

### Technical checks — version 0.2.0

- Source adapter reproducibility and Ren'Py lint passed. The screenplay remained unchanged: 58 scenes, SHA256 `e5c4f7b0af53249752d2d747ebfe756bc084c76002040282d8b7cd93253a6c88`. The earlier record called its 852 reading pages “blocks”; see the corrected distinction above.
- The replacement native suite passed **3 tests / 30 assertions**: reading and visual-discovery state; earlier/later save restoration; and the complete original text route without discovery through the final scene and separate question. These replace the superseded quiz tests below.
- After the final CG beat restriction and disabling old cutouts, the affected reading/discovery case was rerun: **1 test / 16 assertions passed**, with 2 cases skipped by selection. The full suite was not repeated after that final change.
- Both GIMP masters reopened with their editable layers (four for the drawing scene, two for the sealed arch). Independent exports matched runtime pixels. That verifies reproducibility, not artistic or source quality.

### Browser checks and limits — version 0.2.0

The actual web game was opened in Chromium. Title, bright reading, first-night reading, inspection, detail, connection and settings captures were viewed at 1440×900 and/or 1280×720. Local checks caught an obscuring gradient and an oversized slider; both were corrected. These isolated checks were insufficient to review the playthrough. Disabling sprites left scenes without their participants: an infirmary capture describes Mara leading Tessa between crowded beds and a porter drawing a curtain, while the screen shows an empty room. That is a visible source/presentation failure.

Manual browser saves before and after discovery were loaded and their knowledge state checked. Explicitly loading the later manual slot after a page reload restored its story beat and connection. The combined automation did **not** complete: it first assumed Continue would select that manual slot rather than the newer autosave, and a later small-window interaction missed its target after resizing. Do not report a fully passing browser suite or count the mislabeled `v2-14-720-settings.png` capture as a settings check; it shows the infirmary instead. Final combined keyboard/resize verification remains incomplete.

Browser export/import, fullscreen, other browsers and complete manual route review remain unverified. The current web export exists; the Linux 0.1.0 archive is the older build and was not rebuilt for this checkpoint. The historical discovery chain is not implemented by the first-night prototype. No post-Yes interface or continuation was developed.

## Historical first-playable record — superseded implementation

The following records describe version 0.1.0, its removed card/quiz system and its rejected presentation. They are retained as history, not current coverage or approval.

**Current assessment: presentation rejected by the user.** The technical and historical inspection results below remain records of what was tested, not evidence that the interface or artwork is good enough. The [presentation audit](../presentation-redesign.md) supersedes the earlier favorable aesthetic assessment. The card/quiz tests exercise a superseded mechanic; replacement tests must verify [Look closer / Threads](../investigation.md), not force the redesign to retain quizzes for an old passing suite.

Engine: local official Ren'Py 8.5.3 SDK. Source: Rebuild 11, SHA256 `e5c4f7b0af53249752d2d747ebfe756bc084c76002040282d8b7cd93253a6c88`.

The adapter preserves all 58 scenes and every action/dialogue word in order. An independent comparison stripped only metadata, scene headings, speaker cues and the final fade, then compared the emitted prose with the Fountain source. Additional pacing cuts have not been made. The arch-closing source paragraph is split across two advances so its open and closed images occur in order.

### Earlier engine verification

The final native suite reports **7 tests passed, 57 assertions passed**:

- Opening reading UI, settings, history and return to the same line.
- R01 material inspection, wrong-answer guidance, correct finding and exact return to its invitation.
- Opening background/portrait transitions: open arch, spill, closure, phone before cloak, cloak removed, door locked, chair moved, treatment, ceremony and window conversation.
- Save/load at two distinct reading states, including evidence and a finding saved from inside investigation; earlier saves remove later knowledge, and rollback returns to the preceding story line.
- Actual complete traversal without investigations, through S058 and the separate final question interaction; a new playthrough clears knowledge and completion.
- Actual complete traversal with all 21 evidence items and all six findings, including the gradual historical-origin inquiry, reaching the same original ending.
- Keyboard activation and menu return; 1280×720 title/settings/large text/image-description views.

The full test process printed a passing report; its isolated display wrapper subsequently exited with signal status 143 during shutdown. Individual save/load testing and a separate repeat of the small-window test completed with exit 0. This is distinct from the previously fixed game-state failure and does not change the recorded assertions. Do not treat an automated pass as a visual art approval.

Lint reports no script errors or warnings. The adapter's reproducibility check passes. No screenplay words, story outcomes or cast knowledge were changed to support an asset.

### Earlier manual interface review

Opened actual running-game captures at approximately 1740×978 and at 1280×720. Inspected title, severe-bright arrival/ceremony, very-dark apartment, ordinary treatment/window, settings, history, save slots, evidence scrolling, wrong-answer feedback, origin comparison/finding and final question. Fixed a title footer/button overlap, an oversized settings slider, an unavailable checkmark glyph and inappropriate selected styling on answers. Opaque reading panels keep text legible against extreme art lighting. Source/state and native artwork review is recorded [separately](../art/runtime/review.md).

A comparison handler initially returned a boolean, closing investigation; it now returns no value. A second real defect discarded in-menu evidence changes on load; `renpy.retain_after_load()` now preserves the intended saved state, verified with a real save/load cycle. Keyboard help matches Ren'Py's arrow-key focus controls.

Representative captures are kept in [review/](review/). Reproducible full captures are generated in ignored `test-output/` by the native tests.

### Earlier scope statement — no longer current

The complete prose route and investigations are playable. Art is an opening-chapter production batch; supporting action illustrations and most later scenes remain incomplete. There is no audio/performance pass. The final question has no invented rescue outcome. Historical context is reliable player-facing context, not fabricated ancient exhibits carried by the cast; see [content provenance](../investigation-content.md). The existing bridge-seal attribution ambiguity remains in the unchanged screenplay.

### Earlier local Linux package

A standalone Linux archive is built under `visual-novel/builds/` using [build-linux.sh](../build-linux.sh). The extracted package was launched independently of the development SDK and its actual title screen was captured and visually inspected. Packaging excludes development tests, review captures and working XCFs; the font license/notice files are explicitly included before the general text-file exclusion.

### Earlier local browser preview

The matching official 8.5.3 Web Platform Support archive was checksum-verified and used to build `builds/web/` and `builds/web.zip`. [play-web.sh](../play-web.sh) serves the export on loopback; [build-web.sh](../build-web.sh) reproduces it. The initial game archive is 40.4 MiB, with the nine current backgrounds and eleven used sprite/light variants bundled at full resolution. Font licenses remain included; tests, working XCFs and review captures are excluded.

The actual WebAssembly game loaded in an isolated Chromium browser at 1440×900. The title, introduction and chapter transition were exercised, followed by actual keyboard traversal into S001's bright dialogue and S002's dark apartment. Browser captures were opened for visual inspection. Initial title inspection reported no JavaScript page or console errors. The source adapter check and native lint still pass.

Browser save persistence, export/import, fullscreen, complete traversal and other browsers have **not** completed verification. The attempted automated save check stopped in its test harness before reaching Save; it does not count as a browser save/load pass. Desktop results above must not be relabeled as web results. This is a local inspection build; its successful launch does not certify presentation quality.
