#!/usr/bin/env bash
set -euo pipefail
vn_directory=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
vn_sdk=${RENPY_SDK:-"$vn_directory/.tools/renpy-8.5.3-sdk"}
if [[ ! -x "$vn_sdk/renpy.sh" || ! -f "$vn_sdk/web/renpy.wasm" ]]; then
    printf '%s\n' "Ren'Py SDK and matching Web Platform Support are required." \
        "Install both from https://www.renpy.org/release/8.5.3 and set RENPY_SDK if needed." >&2
    exit 1
fi
"$vn_sdk/renpy.sh" "$vn_sdk/launcher" web_build "$vn_directory/renpy" \
    --destination "$vn_directory/builds/web"
python3 "$vn_directory/tools/check-web-assets.py"
printf '%s\n' "Web build ready. Run $vn_directory/play-web.sh to open it locally."
