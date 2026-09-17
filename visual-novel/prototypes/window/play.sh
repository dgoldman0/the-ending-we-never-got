#!/usr/bin/env bash
set -euo pipefail
proof_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
proof_sdk="${RENPY_SDK:-$proof_dir/../../.tools/renpy-8.5.3-sdk}"
exec "$proof_sdk/renpy.sh" "$proof_dir" "$@"
