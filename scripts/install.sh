#!/usr/bin/env bash
# Install skills into a skills directory.
#
# Usage:
#   ./scripts/install.sh --target ~/.claude/skills
#   ./scripts/install.sh --target ~/.claude/skills --only design-maestro,gdd-owner
#   ./scripts/install.sh --target ./skills-out --link      # symlink instead of copy
#
# Without --only, every skill (except folders starting with "_") is installed.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target=""
only=""
link=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) target="${2:-}"; shift 2 ;;
    --only)   only="${2:-}"; shift 2 ;;
    --link)   link=1; shift ;;
    -h|--help) sed -n '2,10p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$target" ]]; then
  echo "error: --target is required" >&2
  exit 2
fi

mkdir -p "$target"

if [[ -n "$only" ]]; then
  IFS=',' read -r -a names <<< "$only"
else
  names=()
  for d in "$here"/skills/*/; do
    n="$(basename "$d")"
    [[ "$n" == _* ]] && continue
    names+=("$n")
  done
fi

count=0
for n in "${names[@]}"; do
  src="$here/skills/$n"
  if [[ ! -d "$src" ]]; then
    echo "error: no such skill: $n" >&2
    exit 1
  fi
  dest="$target/$n"
  rm -rf "$dest"
  if [[ $link -eq 1 ]]; then
    ln -s "$src" "$dest"
  else
    cp -R "$src" "$dest"
  fi
  count=$((count + 1))
done

echo "Installed $count skill(s) into $target"
echo "Next: ./scripts/init-project.sh <your-game-dir> to scaffold design/"
