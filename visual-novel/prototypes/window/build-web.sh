#!/usr/bin/env bash
set -euo pipefail
proof_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
proof_sdk="${RENPY_SDK:-$proof_dir/../../.tools/renpy-8.5.3-sdk}"
"$proof_sdk/renpy.sh" "$proof_sdk/launcher" web_build "$proof_dir" \
    --destination "$proof_dir/../../builds/window-proof"
mkdir -p "$proof_dir/../../builds/window-proof/comparisons"
cp "$proof_dir/review/compare.html" "$proof_dir/../../builds/window-proof/compare.html"
cp "$proof_dir/review/comparisons/"*.png "$proof_dir/../../builds/window-proof/comparisons/"
