# QA — interface pass 0.5.0-dev under review; earlier presentations failed

## Batch 9 in the game; cuts only between different pictures — 10 November 2026, second round

Maker's checks only. The user has not seen this state.

- **Batch 9 checked and placed.** Each of the 13 repaints was compared with the file it replaced, region by region at native size, and against its request item; the pixels of earlier local repairs changed only inside regions an item asked to repaint. The eight new paintings were looked at whole and at native size; an independent reviewer went over four of them at native size, and a second reviewer's pass ended early with notes on three, so `s035-water` was checked by the maker alone. The record is in [the asset request](../art/asset-request.md) under *Batch 9, checked 10 November*.
- **Decisions taken from that check.** `s026-stone` is not used (the stone is a boulder with carved capitals). Two lines gained a page of their own for a close view (the bowls, the cut pages). Two local repairs: the plan's lettering and Orren's cap.
- **Portraits.** Each new portrait was laid beside the portrait of its set that it alternates with. Four were sized by hand after measurement; measuring every speaking portrait then showed five older ones out of scale, which were recropped and looked at beside their character's other sets.
- **Cuts.** With the picture still, a change between two similar framings is a small jump. 576 framing changes inside a painting were measured by how much view they share; the direction tool now holds the picture unless the next framing is clearly different, and returns narration to the whole painting after a close view has been held three pages. A different picture comes every 1.42 pages; none is held longer than six.
- **Who is shown.** Counted for all 394 spoken lines: 125 show the person spoken to alone, 194 with the speaker also in the picture, 30 the whole painting, 45 another choice (nobody to answer, or set by hand).
- **Read in sequence.** The whole game was captured (866 pages, 35 minutes, no error) and read on labelled sheets; eleven scenes changed by that read were captured again and four of them read. The whole game was then captured a second time (867 pages, 35 minutes, no error) and read on labelled sheets from S001 to S037 and in S047–S048, including the Harrow sequence over its new painting. Six scenes changed after that (S001, S002, S023, S033, S045, S048; 114 pages) were captured once more, and S023 and S048 read.
- **Engine.** Lint is clean. The whole suite passed on the final game code: 18 cases, 227 assertions, 18 minutes 27 seconds. After it, only data and the direction tool changed (five portrait crops, hand-set framings, the rule that a painting already close on the listener is shown whole); `camera_direction` was run again on the final data and passes (25 assertions), and the 867-page and 114-page captures ran on it without error.
- **Not done.** Nobody has judged the still cuts in play. The browser build was not rebuilt. The second reviewer's pass on four paintings was not completed. The last quarter of the second whole-game capture (S038–S046, S049–S058) was not read again; those scenes were read in the first capture and changed only where recorded above.

## The camera holds still — 10 November 2026

The user played the build of 9 November and reported that the camera's movements made them nauseous; they had been flipping through chapters fast and were unsure how much was the camera.

- **Changed.** By default nothing moves: framings change on a 0.16 s dissolve and hold, with no glide and no push. While pages are turned fast, paintings are shown whole. The moving camera is an opt-in setting (Gliding), without the long drift added on 9 November.
- **Checked.** Lint is clean. `camera_direction` passes (25 assertions): no glide or push by default, the whole painting when a line arrives in a rush, the framing back at reading pace, and the three Settings choices. The Settings screen was looked at.
- **Not checked.** Whether still cuts are comfortable for the user, which only they can tell.

## Listener framing, the final question and the whole read — 9 November 2026, second round

Maker's checks only; the user chose the listener framing and has not yet reviewed the game.

- **The whole game was played and read.** All 865 pages were captured in one headless session (37 minutes, no error) with the listener framing and read in order on 29 sheets, each page labelled with its speaker and framing. Corrected from that read: lines called across a room that framed the wrong person, narration that stayed on the previous speaker, and the second hearing painting brought in at the line where Tessa stands (it had waited 12 lines past the moment it shows).
- **An overstated figure, corrected.** The first round reported that the picture changed every 1.23 pages. That counted shifts of a few pixels between framings of people standing side by side. Counted strictly (a new painting, another part of it, or a clear change of size) a different picture comes every 1.40 pages; the longest run without one is 8 pages. Near-identical framings are now one held framing, so the camera no longer twitches between them.
- **After the read.** Hand-set framings were added for the scenes with least variety, and their framing sheets were looked at. Nine scenes changed by these corrections (S012, S013, S017, S028, S032, S036, S037, S043, S048; 119 pages) were captured again without error, and S013 and S037 were read from those captures.
- **The final question.** Captured at four moments: the question alone; the question with Yes and Return to the title; Coming soon as it arrives; Coming soon complete. No support address is set, so no button shows.
- **Engine.** Lint is clean. The whole suite passes on the final code: 18 cases, 221 assertions, 21 minutes 38 seconds. It includes `camera_direction` (19 assertions, among them going back to an earlier framing and loading the next painting ahead), the ending through Yes and Coming soon, and `final_question_declined`.
- **Not done.** Nobody has judged the movement in play. The browser build was not rebuilt. The Coming soon wording is the maker's. Batch 9's files do not exist yet, so its planned stages and portraits are untested beyond the checker.

## Camera direction — 9 November 2026

Maker's checks only; the user has not seen this and nothing here is approval.

- **Baseline.** Every one of the 865 reading pages was captured from the running game at 1920×1080 before any change. Each painting was on screen whole for 5.8 pages on average, 36 at most.
- **Reading shade parity.** With the camera held still, the 42 pages of S001–S002 were captured again and compared with the baseline: the mean difference per page is at most 1.3 levels of 255 (median 0.5), from the shade's blur now being laid in four layers and its grain being a tile.
- **Framings.** All 308 framings were looked at on the review sheets (`tools/direct-shots.py sheets`), under the reading shade, beside the whole painting. Names were corrected or added in 34 paintings. The framing rule was changed twice after looking: first cuts through neighbouring faces, then headless bodies at the top of the frame.
- **In sequence.** S001, S002, S007, S016, S033, S035, S046, S048 and S055 (213 pages) were played and read page by page with the camera on the speaker; S016 and S046 (67 pages) with the camera on the listener. One page was opened at full size: at 1.62 times the faces and cloth hold up, with the grade's colour fringing visible in a corner.
- **Motion.** Thirteen frames captured across two line changes in S016 show an ease between overlapping framings and a cut between distant ones. Smoothness and pacing cannot be judged from captures.
- **Engine.** The whole suite passed before the narration and listener refinements (16 cases, 192 assertions, 21 minutes). After them: lint is clean, the new `camera_direction` case passes (14 assertions: whole on arrival, speaker, hand-set insert, pronoun narration, listener, Still, the three Settings choices), and the 67-page listener capture ran without error. The whole suite was not run again after those refinements.
- **Settings.** The option in force could barely be told from the others (ivory against pale gold); unselected options are now dim.
- **Not done.** No person has played it. The browser build was not rebuilt or tested. 37 scenes use the automatic choices without hand direction.

## Portrait crops — 23 September 2026, third round

The user rejected the portraits: the crop itself was wrong, with bare neck ending in a weird shape inside an open-bottomed arch, and the earlier edge cleanup had not fixed it. Every portrait is now recropped from its source painting in GIMP (`tools/crop-portraits.py`, which generates and runs a Script-Fu batch):

- **Rectangular crops, not cut-outs.** Each crop keeps a painted ground. The generator cut-outs (Senn, Mara, Iven, supporting cast) have their stair-stepped matte pulled in a pixel and softened, dropping the black and red fringe; Tessa's grey studio ground is taken down; GPT's busts get the same ground.
- **One composition.** The face is 62% of the crop's height with its top at 21%, with 4% gaze room; the crop ends above the lumpy generated neck base. Layered masters are saved in `art/portrait-masters/`.
- **Closed laurel windows.** The frame has a foot with a gilt tie, so the crop ends at a sill instead of fading into the shade. The speaker is mirrored when needed to face the listener (Tessa's heads all look left in the source), and on book pages both face the text.
- **Retired:** `finish-portraits.py`, `portrait-faces.py` and the per-portrait face alignment, all superseded by the shared crop.
- **Still limited:** the S001–S005 heads were painted without shoulders, so they read as close head shots beside GPT's busts. Only new paintings can add shoulders.

## Light, ornament and portraits — 23 September 2026, second round

The user found the framing too dull and asked for the uncomfortable light to stay visible and readable. They then rejected an eye-adaptation fade: the distortion must be permanent in the image.

- **Light:** `tools/grade-light.py` renders 46 stages, 8 single images and 23 portraits into bright, ordinary or night, in both modes. Each image is split edge-aware into large-scale light and local detail; the light is distorted, the detail kept. No transitions are involved. Inspected at 1920×1080 in all three registers and both modes: faces stay readable in glare and at night, and ordinary daylight reads as uneasy.
- **Ornament:** portrait arches are gilt relief with a laurel garland on celadon enamel and a twelve-ray sun keystone, lit like metal and dimmed or brightened with the scene's light. Speech gets a gilt rail under the name; narration stays plain italic. Book pages get a framed text block, a laurel rule and illuminated initials (inline, so the text and history stay exact).
- **Portraits:** the S001–S005 heads were rebuilt from their neutral sheets (`tools/finish-portraits.py`): the GIMP masks reused and refined along hair, ground colour removed from edges, painted outlines choked, necks dissolving into shadow. GPT's six Lucan and Valcair portraits appear on book pages in the margin; Tessa's bare-head portraits stand in for her missing period sets in S012–S031 only.
- **Fixed on the way:** the raised initial first opened a gap below its line and overlapped entries in History; the dead-phone detail was nearly black under the night grade.
- **Checks:** 13 test cases (191 assertions) pass in the sandbox; lint is clean.

## 0.5.0-dev interface and infrastructure pass — 23 September 2026

Built at the user's direction after the window proof failed. Not yet reviewed by the user; the maker's inspection below is not approval.

**Screens inspected at 1920×1080.** The `ui_tour` and `ui_tour_states` cases in `game/tour.rpy` capture the complete screens under `renpy/test-output/tour/`: title, S001–S005 stage reading (arrival, narration, compact exchanges, night, quiet drawing, ceremony, window), Look closer before and after bringing a detail alongside, Threads, settings, save, history, chapter card, day/dusk/night pages, a time caption, the ending and the final question, plus Softened, larger text, keyboard focus and hidden text.

**Defects found and fixed during the pass:**
- Hiding the words (H) had blanked the whole screen in every earlier build.
- Portrait masks were unmasked.
- Face scales were inconsistent.
- The scene heading overlapped the arrival foot.
- A 140 px lift cut Orra's and Senn's heads.
- The Look closer titles didn't line up.
- Save names used straight apostrophes.
- The settings sliders were invisible.
- The chapter-card test was wrong, and the full-route test timed out.

**Known open issues:**
- **Existing art:** the Intense dead-phone detail is nearly black. The arrival needs a 70 px lift. Iven's position below the dais in S004's intervention sits under the reading shade.
- **Discovery:** Look closer's payoff is still limited to the three authored comparisons.
- **Not yet reviewed:** reading pace at human speed.

**Checks run:**
- **Regression suite:** `tools/run-tests.sh` passes 12 cases (184 assertions): the full 58-scene route, page turning with rollback and save/load, discovery and exact return, lighting persistence, larger text, hiding the words and the staging pipeline.
- **Other checks:** lint is clean, and `check-rovel-plan.py`, `adapt_screenplay.py --check` and `check-staging.py` pass.
- **Web:** the web build loads in headless Chromium, and its asset check passes.
- **Linux:** the Linux package (`builds/TheEndingWeNeverGot-0.5.0-dev-linux.tar.bz2`) was extracted and launched in a virtual display, and it renders the title screen.

**Test isolation.** Running `play.sh test` directly writes test saves, preferences and read-text marks into the reader's real save folders (`~/.renpy/the-ending-we-never-got-original-v1/` and `renpy/game/saves/`). Earlier sessions' suites and this pass's first runs did so. Use `tools/run-tests.sh`, which runs in a temporary sandbox.

**Art pipeline.** `game/staging.json` maps S006–S058 to planned paintings and portrait sets. `tools/check-staging.py` reports what has arrived, and `tools/portrait-faces.py` measures new portraits. The [asset request](../art/asset-request.md) lists what to make next.

## Earlier rejections

**17 September 2026: 0.4.0-dev FAILED**, archived at `1bb6d76`. The UI and compact portrait execution were rejected after prior inspection. Read the [failure analysis](../reviews/2026-09-17-rovel-rejection/README.md) and [production controls](../production-controls.md). The prior native result was 7 cases / 152 assertions; that historical technical result cannot clear this presentation. No new engine pass is implied by the control update.

The subsequently authorized [window proof](../prototypes/window/README.md) was also rejected, and its unfinished trial 2 repeated the pattern; see the [window failure review](../reviews/2026-09-23-window-failure/README.md). The earlier session already inspected the pictures and accepted obvious defects; the correction centers on actual visual examples, comparative judgment and demonstrated direction. Read final screens before prompts/audit prose, and distinguish source, export, geometry and packaging evidence from artistic judgment. The producing model’s favorable review alone cannot clear another batch. No build gate or automated visual score is introduced.

## Historical full review of 0.3.2

The review traversed all **852 reading pages / 849 source reading blocks**. It manually inspected selected screens and interactions, not all 852 pages at human reading pace. It found no compact speaker-frame mode, excessive dialogue-box movement, frozen reactions, unfinished frame edges, weak discovery payoff, unstable controls and a Threads caption partly outside its hit area. The [ledger](../art/route-coverage.md) records 66 mapped opening pages, 29 room-only pages and 757 prose-only pages. The final question exists, but its intended Yes choice does not.

Geometry checks did not reproduce offscreen story glyphs in the tested layouts. They do not dismiss the user's clipping report or clear the interface. Native/browser results, manual pixel inspection, continuous human-paced reading and automated traversal must remain distinct evidence.

The subsequent connected milestone must meet the [experience and completion gates](../presentation-redesign.md#scene-completion-gates) across S001–S005 after the bounded proof. Include compact conversations/listener reactions, cast through narration, interface/flow, discovery and return, both lighting preferences, standard/larger text and mouse/keyboard. Record build, source span, window/platform, actual manual scope and concrete failures. Final-route verification must eventually exercise the deliberate Yes affordance after S058/fade, without developing the deferred post-Yes interface.

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
