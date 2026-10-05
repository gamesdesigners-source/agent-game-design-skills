#!/usr/bin/env bash
# Scaffold the design bible into a game project.
#
# Usage: ./scripts/init-project.sh <game-dir> [--force]
#
# Copies templates/design into <game-dir>/design. Refuses to overwrite an
# existing design/ folder unless --force is given.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dest_root="${1:-}"
force=0
[[ "${2:-}" == "--force" ]] && force=1

if [[ -z "$dest_root" ]]; then
  echo "usage: $0 <game-dir> [--force]" >&2
  exit 2
fi

dest="$dest_root/design"
if [[ -e "$dest" && $force -eq 0 ]]; then
  echo "error: $dest already exists (use --force to overwrite)" >&2
  exit 1
fi

mkdir -p "$dest_root"
rm -rf "$dest"
cp -R "$here/templates/design" "$dest"

echo "Created $dest"
echo "Next: fill in $dest/gdd/00-overview.md (pillars first), then ask the Design Maestro for something."
