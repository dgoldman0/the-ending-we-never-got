# The original timeline — playable build

**Current runtime: 0.5.0-dev, interface and infrastructure pass (23 September 2026), not yet approved by the user.** Illustrated scenes (S001–S005) keep the whole painting, graded into a permanent light register by `../tools/grade-light.py`: bright (white-hot spilling glare, halation, colour splitting at the edges), ordinary (sallow light, cold shade, uneven exposure) or night (sunk light, cold shade, glowing sources), with local detail preserved. Text sits in a soft shade at the foot, under a gilt speaker rail, beside closed laurel windows holding GIMP-cropped portraits graded to the same light. Scenes without illustrations (S006–S058) read as framed book pages with illuminated initials and the speaker and listener in the margin. Every interface image is drawn in code by `../tools/build-ui-assets.py`. This is the maker's pass, not visual approval; the [failure reviews](../reviews/2026-09-23-window-failure/README.md) still apply.

Run `../play.sh` from this directory, or `./visual-novel/play.sh` from the repository root. The local development SDK is Ren'Py 8.5.3. Elsewhere, install the [official SDK](https://www.renpy.org/release/8.5.3) and set `RENPY_SDK` to its extracted directory. The engine is not checked into Git.

The original text route is traversable: 58 source scenes, ten working chapters, and the complete Bellweir ending followed by **Do you wish to save Tessa?** The question currently offers only Return to title. The intended Yes affordance remains unfinished; all post-Yes UI/UX and continuation are deferred. Text traversal is not completion of this visual novel.

The archived opening maps 95 reading pages across S001–S005, with scene illustrations, action states and compact portraits. The user rejected the resulting presentation despite this coverage. GIMP masters retain source repairs and paired exposure layers. S004–S005 now have mapped cast/action rather than the earlier room-only fallback; S006–S058 still use prose/location cards. No music, voice or sound has been produced yet.

## Standalone Linux build

The local `../builds/TheEndingWeNeverGot-0.1.0-linux.tar.bz2` is the older, rejected first playable package; it does not include this checkpoint's changes. Extract it and run `TheEndingWeNeverGot.sh` inside the extracted directory; no separate SDK is needed. Create a diagnostic export from current source with `./visual-novel/build-linux.sh` from the repository root. Build artifacts stay out of Git. Neither edition is a completed illustrated release.

## Reading and state

Click, Space or Enter advances. Page Up/mouse wheel up rolls back; Esc opens or returns from menus. Save/load, reading history, larger text, fullscreen, reduced motion, image descriptions and Ren'Py self-voicing are available. Look closer and Threads return to the same reading point. All knowledge state is per playthrough/save, not global completion data.

**Settings → Lighting → Softened** reduces the extreme glare and opens deep shadows. **Intense** is the default. Change it from the title or while reading; it applies to the scene, cast, title image and discovery close-ups together. The preference persists independently of saves, so loading an older save keeps the current choice. Existing save thumbnails retain the lighting with which they were captured. Both modes use the same corrected compositions; [the lighting record](../art/lighting/README.md) documents their sources.

## Browser preview

From the repository root:

```sh
./visual-novel/play-web.sh
```

Open **http://127.0.0.1:8042/** if the browser does not open automatically. Leave that terminal running; Ctrl+C stops the local server. `--no-open` suppresses automatic browser launch, and `--port 8043` selects another port. Use a consistent URL and port to retain access to the same browser saves.

This runs the actual Ren'Py game through WebAssembly, including its current scene art, Look closer / Threads and ending. It needs HTTP: opening the exported `index.html` directly with `file://` is not supported. The server binds only to this computer and serves only the exported game directory. It sends the WebAssembly MIME type and revalidates files so rebuilt art is not hidden by stale HTTP caches.

Saves are local to this browser/site, separate from desktop saves. Use the **≡ menu at the top left → Export Saves** for a backup or **Import Saves** to restore one. Closing a tab does not create a manual save; use the game's Save control first. Clearing browser site data removes its local saves.

After changing scripts or art, rebuild and refresh the page:

```sh
./visual-novel/build-web.sh
```

`play-web.sh` builds automatically only if no web build exists. The reusable export is `builds/web/`; `builds/web.zip` contains the same distribution for a static web host. These generated files remain outside Git. The build requires the Ren'Py 8.5.3 SDK **and matching Web Platform Support**, both from the [official release page](https://www.renpy.org/release/8.5.3). Extract the latter's `web/` directory into the SDK directory; use `RENPY_SDK` for a nondefault installation. The installed web archive was checked against official SHA256 `954db897e65f51ea63cb2fb7b203d02be0447f4e22069514020bbe6c6691fdfc`.

`progressive_download.txt` bundles the current scene/interface images and both lighting treatments before play, so inspection starts at full image quality. The build checks the actual web package for required assets; source-file existence alone previously concealed missing browser art. Retired character cutouts are not preloaded. Browser-specific verification is recorded in [QA.md](QA.md); desktop test results alone do not certify this port.

## Source and investigation

`game/story.rpy` and `game/source-map.json` are generated by `../tools/adapt_screenplay.py`. Every action and spoken line is retained: 849 source reading blocks become 852 reading pages, with the final fade separate. Existing time skips remain in narration. Develop shot/performance/reading direction alongside this preserved source; document any proposed narration adaptation and its mapping. Do not edit generated dialogue or the Fountain manuscript to compensate for an art mistake. Any separately justified screenplay change follows its own instructions before regeneration and review.

`game/inquiry-data.rpy` contains the first-night details and per-save discovery operations. The connecting passage in `investigation.rpy` juxtaposes the drawing, dead phone and earlier milk message. The historical reveal remains required but is not implemented by this sample; its authored material is still to develop. The old quiz prose is retained in Git history, not in the game.

## Development checks

```sh
python3 visual-novel/tools/adapt_screenplay.py --check
python3 visual-novel/tools/check-rovel-plan.py
./visual-novel/play.sh lint
./visual-novel/tools/run-tests.sh
python3 visual-novel/tools/build-ui-assets.py   # redraw interface components
python3 visual-novel/tools/check-staging.py      # S006+ art present or awaited
python3 visual-novel/tools/crop-portraits.py     # after adding portraits: GIMP crops, one composition
python3 visual-novel/tools/grade-light.py        # after adding art: light registers, both modes
```

New scene paintings and portraits go at the paths in `game/staging.json`; see the [asset request](../art/asset-request.md) for sizes and composition rules. No code change is needed for a scene to switch from the typeset page to its painting.

Run tests with `./visual-novel/tools/run-tests.sh` (optionally naming one test case). It runs in a virtual display with its own temporary saves and persistent data. Running `play.sh test` directly writes test saves, preferences and read-text marks into the reader's real save folders, which earlier sessions did. The `ui_tour` case in `game/tour.rpy` captures 22 complete screens at 1920×1080 under `renpy/test-output/tour/` for visual review.

The native engine tests exercise the actual screens and full route. They create captures under `renpy/test-output/`, which must be opened and inspected; passing tests does not certify visual quality. The QA record distinguishes tested controls, inspected composites and remaining production work.

Generated `.rpyc`, caches, test saves, local SDKs and bulk test captures are ignored. Bundled fonts retain their licenses in `game/fonts/`. Prompts stay under `art/prompts/<sequence>/`; current source components and masters are under `art/opening-sequence/` and `art/interface-original/`, with lighting provenance under `art/lighting/`. Older runtime/presentation directories retain the rejected batches.
