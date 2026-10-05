# design/

This folder is the canon for your game. Copy it into your project root (`scripts/init-project.sh` does this).

```
design/
  registry.yaml        every named thing, by ID and status
  CHANGELOG.md         written by the GDD Owner on every commit
  gdd/                 the design bible, one file per discipline
  proposals/open/      drafts waiting for review
  proposals/resolved/  approved or rejected, kept for history
  findings/            review findings
  _contracts/          formats shared by all skills
```

## Rules

- Only the GDD Owner writes to `registry.yaml`, `CHANGELOG.md` and `gdd/`.
- Specialists write proposals and findings only.
- Start by filling in `gdd/00-overview.md`. Pillars come first.
- `gdd/` files are short and indexed so the Maestro can load only what a task needs.

## GDD index

| File | Owner skill | Contents |
|---|---|---|
| `00-overview.md` | gdd-owner | pillars, genre, platform, audience, scope |
| `01-mechanics.md` | core-loop-mechanics | verbs, loops, rules |
| `02-world.md` | narrative-director | setting, factions, lore |
| `03-narrative.md` | narrative-director | story arc, themes, tone |
| `04-characters.md` | character-concept | player, NPCs, enemies |
| `05-combat.md` | combat-balancer | stats, damage model, counters |
| `06-economy.md` | economy-designer | currencies, sources, sinks |
| `07-progression.md` | progression-difficulty | XP, unlocks, difficulty |
| `08-levels.md` | level-designer | zones, encounters, puzzles |
| `09-ux.md` | ux-onboarding | HUD, tutorial, feedback |
| `10-audio-visual.md` | audio-visual-direction | style guide, color language, sound |
| `11-accessibility.md` | accessibility | options and targets |
| `12-scope.md` | scope-feasibility | team, budget, cut list |
| `13-monetization.md` | monetization-retention | model, live-ops, retention |

"Owner skill" means the specialist whose proposals usually change that file. The GDD Owner is still the only one who writes it.
