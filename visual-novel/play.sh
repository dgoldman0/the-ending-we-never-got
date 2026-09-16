#!/usr/bin/env bash
set -euo pipefail
vn_directory=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
vn_sdk=${RENPY_SDK:-"$vn_directory/.tools/renpy-8.5.3-sdk"}
if [[ ! -x "$vn_sdk/renpy.sh" ]]; then
    printf '%s\n' "Ren'Py SDK not found. Set RENPY_SDK to your SDK directory." >&2
    exit 1
fi
exec "$vn_sdk/renpy.sh" "$vn_directory/renpy" "$@"
