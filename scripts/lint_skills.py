#!/usr/bin/env python3
"""Lint every skills/*/SKILL.md.

Usage: python3 scripts/lint_skills.py [skills-dir]

Rules:
  L01 frontmatter exists with `name` and `description`
  L02 `name` matches the folder name and is lowercase-hyphenated
  L03 description is 40-1024 characters
  L04 required sections present (see COMMON and SPECIALIST below)
  L05 SKILL.md is at most 400 lines
  L06 review checklist rows use valid severities and unique IDs with the right shape
  L07 scripts referenced as `scripts/<file>` exist in the skill folder
  L08 skill never tells itself it may write to design/ (specialists only)

Folders starting with "_" (such as _template) are skipped.
Exit code 0 when clean, 1 when any error is found.
"""
import re
import sys
from pathlib import Path

COORDINATORS = {"design-maestro", "gdd-owner"}
COMMON = ["## Required context", "## Don'ts"]
SPECIALIST = ["## Design mode", "## Review mode", "## Failure modes", "## Handoff"]
# Skills whose procedure is a simulation rather than a design pass use their own headings.
SPECIALIST_OVERRIDES = {
    "playtest-simulator": ["## Procedure", "## Review checklist", "## Failure modes", "## Handoff"],
}
SEVERITIES = {"Blocker", "Major", "Minor", "Note"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
ROW_RE = re.compile(r"^\|\s*([A-Z]{3}-R\d{2})\s*\|(.+)\|\s*([^|]+?)\s*\|\s*$")
MAX_LINES = 400


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    block = text[4:end]
    body = text[end + 4:]
    data = {}
    for line in block.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            data[k.strip()] = v.strip()
    return data, body


def lint_skill(folder):
    errors = []
    path = folder / "SKILL.md"
    name = folder.name
    if not path.exists():
        return [f"{name}: SKILL.md missing"]
    text = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    if fm is None:
        errors.append(f"{name}: L01 no frontmatter")
        return errors
    for key in ("name", "description"):
        if not fm.get(key):
            errors.append(f"{name}: L01 frontmatter missing '{key}'")
    if fm.get("name") and fm["name"] != name:
        errors.append(f"{name}: L02 frontmatter name '{fm['name']}' does not match folder")
    if not NAME_RE.match(name):
        errors.append(f"{name}: L02 folder name must be lowercase-hyphenated")
    desc = fm.get("description", "")
    if desc and not (40 <= len(desc) <= 1024):
        errors.append(f"{name}: L03 description length {len(desc)} outside 40-1024")

    required = list(COMMON)
    if name not in COORDINATORS:
        required += SPECIALIST_OVERRIDES.get(name, SPECIALIST)
    for heading in required:
        if not re.search(rf"^{re.escape(heading)}\s*$", body, re.M):
            errors.append(f"{name}: L04 missing section '{heading}'")

    n_lines = len(text.splitlines())
    if n_lines > MAX_LINES:
        errors.append(f"{name}: L05 {n_lines} lines exceeds {MAX_LINES}")

    seen = set()
    rows = 0
    for line in body.splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        rows += 1
        cid, sev = m.group(1), m.group(3).strip()
        if cid in seen:
            errors.append(f"{name}: L06 duplicate check id {cid}")
        seen.add(cid)
        if sev.split(" ")[0] not in SEVERITIES:
            errors.append(f"{name}: L06 {cid} has invalid severity '{sev}'")
    if name not in COORDINATORS and rows == 0:
        errors.append(f"{name}: L06 no review checklist rows found")
    if name == "design-maestro" and rows == 0:
        errors.append(f"{name}: L06 no review checklist rows found")

    for ref in set(re.findall(r"scripts/([A-Za-z0-9_\-]+\.(?:py|sh))", text)):
        if not (folder / "scripts" / ref).exists():
            errors.append(f"{name}: L07 references scripts/{ref} which does not exist")

    if name not in COORDINATORS and not re.search(r"Don't write to `design/`", body):
        errors.append(f"{name}: L08 Don'ts must include \"Don't write to `design/`\"")
    return errors


def main(argv):
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent / "skills"
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2
    folders = sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith("_"))
    all_errors = []
    for f in folders:
        all_errors.extend(lint_skill(f))
    for e in all_errors:
        print(f"ERROR {e}")
    print(f"\nChecked {len(folders)} skills: {len(all_errors)} error(s)")
    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
