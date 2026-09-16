#!/usr/bin/env bash
set -euo pipefail
vn_directory=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
if [[ ! -f "$vn_directory/builds/web/index.html" ]]; then
    "$vn_directory/build-web.sh"
fi
exec python3 "$vn_directory/tools/serve-web.py" "$@"
