# Native 0.4.0-dev — bounded functional and geometry check

17 September 2026. Linux, Ren’Py 8.5.3.26051504, isolated project copies and separate Xvfb displays/save directories. This checks code and selected reading layouts; it does **not** clear art, browser behavior or the connected experience. Senn identity repairs were in progress while the shared assets were loaded.

## Functional result and correction

The first, unchanged seven-test run ended **5 passed / 2 failed**, with 90 assertions passing. Both failures were traversal timeouts: `original_reading_and_discovery` stopped at S001:11 after clicking Continue; `opening_scene_states` stopped at S001:15/page1 after clicking Continue.

The engine’s `Advance.execute` queues the logical `dismiss` event. `testkey.queue_keysym` forwards that event directly; it does not press Return or Space. `SayBehavior` requires focus for this abstract event, so it cannot advance while the footer retains focus. The existing `dismiss_unfocused` Space mapping handles an actual Space key independently.

A separate input probe passed six assertions: Continue click, Space while Continue remained focused, Enter with that focus, a scene mouse click, Space over the footer, and another Continue click all reached their exact expected source page. No runtime behavior change was justified.

With main-thread authorization, changed **only `game/testcases.rpy`**: retained the existing checks, added actual focused-Space assertions at the two boundaries, then moved the pointer to the scene before abstract `advance`. The full rerun passed **7/7 cases, 152/152 assertions, 8/8 hooks**, in 137.352 seconds. It covers single Begin, all five opening scenes and their coverage boundary, direct comparisons/Threads/exact return, discovery rollback, save/load, persistent larger text and lighting, source hash, all 58 scenes and the final question’s ordering. It does not implement or clear the deferred final Yes response.

`tools/check-rovel-plan.py` passed: 95 source pages, counts 24/18/24/16/13, required files and paired grades present. Its visual/UI/experience status remains explicitly unreviewed.

## Selected reading layouts

Measured 44 states: eleven source pages × Standard/Larger × native windows **1739×978 and 1280×720**. Pages: S001:9,11,15/page0,15/page1,17,54; S002:69,71,92; S003:118,124. Lines 54/92/124 are the longest spoken lines in their respective scenes. The copied `rovel-ui.rpy` matches the reviewed current file, SHA256 `2f416e6b1126ef485c56d5c103e8803cf78c4ef2ad5f967a51d09325d0e74476`.

All measured story text stayed inside its panel. All enabled footer labels stayed inside their focus rectangles, and the rectangles stayed inside the viewport. Logical coordinates use the game’s 1920×1080 canvas:

| Largest relevant layout | Panel | Text bottom | Footer begins |
| --- | --- | --- | --- |
| S001:11 and15/page0, Larger | bottom anchored, y735–1015 | 967 | 1018 |
| S002:69, Larger | upper right, y145–425 | 377 | 1018 |
| S003:118, Larger | expands upward, y689–1015 | 967 | 1018 |
| Longest S001/S002 dialogue, Larger | y738–1018 | 911 | 1018 |

Opened the actual large-window screenshots for arrival, milk, return, closure/empty arch, window/dress, treatment introduction and long dialogue. Opened Standard/Larger return, night-window and treatment introduction again at 1280×720. No clipped glyphs or broken frame edges appeared in those inspected captures. The treatment panel leaves the missing fingers and corrupted wrist visible; the window panel leaves Tessa, chair and discarded dress outside its bounds. Broader composition and final identity judgment remain the main thread’s separate review.

Evidence remains in `/tmp/vn-040-functional-oassfe5z/` and `/tmp/vn-040-geometry-681j6nbh/`: copied scripts and hashes, test screenshots, `measurements.jsonl`, plus separate large-window and `test-output-1280` captures. Temporary geometry code was not added to the game. No art, GIMP, runtime UI or browser files were changed in this pass.

## Refreshed variants and final ornament padding

The original 44-state geometry harness already called `renpy.restart_interaction()` and paused after **every** text-size assignment. Its different text heights and line wrapping were real; it did not inherit the separate main-thread lighting-capture refresh error.

After the main thread increased narrow-panel right padding from 50 to 90, recaptured S001:11 and15/page0, S002:69 and S003:118 in both text sizes, both lighting settings and both window sizes: **32 states, 64/64 direct assertions passed**. Every state explicitly restarted the interaction before inspection. `renpy.get_displayable('say', 'what').style.size` was asserted and recorded as 36/40; the effective stage path was asserted and recorded as the original/`art/softened/` path according to the requested grade. All 16 grade pairs and all 16 text-size pairs have different actual screenshot pixels.

No text or footer focus-label containment defects occurred. S002:69 Larger now wraps to five lines: panel y145–471, text ends423. S003:118 Larger remains y689–1015, text ends967. All lower panels still stop before the footer. Opened the largest night-window/treatment pairs at both window sizes and the return pair at1280; the wider padding keeps text clear of the right leaf ornament without hiding the key action. This remains a bounded layout check, not scene or asset approval.

Final evidence: `/tmp/vn-040-finalgeometry-l6ab7x7n/`, including `variant-validation.json`, measurements, copied scripts and screenshots. Final UI SHA256: `544666ae183dbabf530711d021ec299625b97ef4b0b19857d738caaf96dfedc8`. No product files changed and the full functional suite was not repeated for this follow-up.
