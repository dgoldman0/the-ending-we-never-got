#!/usr/bin/env bash
# Run the Ren'Py test suite in a sandbox, without a visible window.
#
# Ren'Py writes saves and persistent data (preferences, read-text marks) to
# the per-user save folder and to renpy/game/saves. Tests click save slots and
# change preferences, so running them against the real game overwrote the
# reader's slots and marked every line as read. Here the game files are
# symlinked into a temporary base directory with its own empty saves, and
# --savedir points Ren'Py at a private folder; both are deleted afterwards.
#
#   visual-novel/tools/run-tests.sh                  # whole suite
#   visual-novel/tools/run-tests.sh ui_tour          # one test case
#
# Screenshots are captures for visual review, not comparisons: each run
# replaces them under renpy/test-output/.
set -euo pipefail
vn=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
sdk=${RENPY_SDK:-"$vn/.tools/renpy-8.5.3-sdk"}
sandbox=$(mktemp -d "${TMPDIR:-/tmp}/tenwg-tests.XXXXXX")
trap 'rm -rf "$sandbox"' EXIT

mkdir -p "$sandbox/game/saves" "$sandbox/savedir" "$vn/renpy/test-output"
for item in "$vn/renpy/game"/*; do
    name=$(basename -- "$item")
    case "$name" in
        saves|cache|*.rpyc|*.rpymc) continue ;;
    esac
    ln -s "$item" "$sandbox/game/$name"
done
# Screenshots land in the project's ignored test-output folder.
ln -s "$vn/renpy/test-output" "$sandbox/test-output"

export SDL_AUDIODRIVER=dummy
xvfb-run -a -s "-screen 0 1920x1080x24" \
    "$sdk/renpy.sh" "$sandbox" --savedir "$sandbox/savedir" test "$@" --overwrite-screenshots
