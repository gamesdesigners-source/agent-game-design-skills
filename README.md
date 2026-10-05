# Game Design Skills

A skill pack that turns an AI agent into a game design studio. One coordinator, one keeper of canon, and seventeen specialists. Every specialist works in two modes: **Design** (generate) and **Review** (audit, with severities, evidence and fixes).

The pack follows the shape of security-audit skills: explicit checklists, severity ratings, failure-mode thinking, and findings that cite evidence. It also borrows the discipline of a code repo: one source of truth, change proposals instead of direct edits, and a changelog.

## The cast

| Skill | Role |
|---|---|
| `design-maestro` | Producer. Reads the GDD, plans which skills run in what order, runs the review pass, resolves conflicts, hands approved changes to the Owner. Writes almost no content itself. |
| `gdd-owner` | Keeper of canon. The only skill allowed to write to `design/`. Checks proposals for contradictions, manages IDs and status lifecycle, maintains the changelog. |

**Foundation:** `core-loop-mechanics`

**Content:** `character-concept`, `narrative-director`, `dialogue-voice`, `quest-designer`, `level-designer`, `encounter-director`, `puzzle-crafter`

**Systems:** `combat-balancer`, `economy-designer`, `progression-difficulty`

**Quality:** `ux-onboarding`, `audio-visual-direction`, `accessibility`, `playtest-simulator`, `scope-feasibility`, `monetization-retention`

## How it works

```
You ──request──▶ Design Maestro ──plan──▶ specialists (Design mode)
                      │                         │ proposals
                      │                         ▼
                      │              specialists (Review mode) ──findings──┐
                      │                                                     │
                      ◀───────────── conflicts, severities ────────────────┘
                      │
                      └──approved bundle──▶ GDD Owner ──commits──▶ design/ (canon)
```

1. The Maestro reads the GDD index and builds a plan.
2. Design-mode skills draft content and submit **proposals**. They never edit canon.
3. Review-mode skills audit the drafts and return **findings** with severity.
4. The Maestro resolves conflicts (by pillar priority; taste calls go to you), runs one revision round, and bundles what survives.
5. The GDD Owner validates the bundle against the ID registry and commits it.
6. You get a short summary: what was made, what changed in canon, what needs your decision.

## Repo layout

```
skills/            one folder per skill, each with a SKILL.md
templates/design/  the design bible scaffold you copy into your game project
docs/              architecture, contracts, workflows
scripts/           validators, simulators, installer
.github/workflows/ CI that lints every skill and tests the scripts
```

## Install

Copy skills into your agent's skills directory and scaffold a design bible in your game project:

```bash
git clone <this-repo> && cd game-design-skills
./scripts/install.sh --target ~/.claude/skills        # installs all skills
./scripts/install.sh --target ~/.claude/skills --only design-maestro,gdd-owner,combat-balancer
./scripts/init-project.sh /path/to/your/game          # copies templates/design into your game as design/
```

Works with any harness that loads `SKILL.md` folders (Claude Code, Claude.ai skills upload, Agent SDK). For harnesses without skill loading, paste a skill's SKILL.md into the system prompt.

## Quick start

1. Run `init-project.sh` in your game repo.
2. Fill in `design/gdd/00-overview.md` (pillars, genre, platform, audience). Everything else depends on it.
3. Ask: *"Design the first dungeon."* The Maestro takes it from there.

Common requests are routed by `skills/design-maestro/references/routing-table.md` (new enemy, new quest, rebalance weapons, audit the economy, and so on).

## Number-crunching is done in code

LLMs are unreliable at arithmetic and distribution math. The economy, combat and progression skills require running scripts instead of hand-calculating:

- `skills/economy-designer/scripts/economy_sim.py` simulates sources and sinks and reports inflation, time to goals and grind walls.
- `skills/combat-balancer/scripts/ttk_matrix.py` builds a time-to-kill matrix across weapons and enemies and flags dominant, dead and out-of-band options.
- `skills/progression-difficulty/scripts/xp_curve.py` generates level curves and time-to-level for a given session length.
- `skills/level-designer/scripts/validate_graph.py` checks level, quest and puzzle graphs for unreachable nodes, soft-locks and unobtainable gate items (a copy ships with `quest-designer` and `puzzle-crafter`).
- `skills/gdd-owner/scripts/validate_registry.py` checks the ID registry for duplicates, dangling references and bad statuses.

Scripts live inside their skill folder so a skill still works when installed on its own. They use only the Python standard library. Sample inputs are in `examples/`.

```bash
python3 skills/combat-balancer/scripts/ttk_matrix.py examples/combat.json
python3 skills/economy-designer/scripts/economy_sim.py examples/economy.json --runs 200 --seed 1
python3 skills/progression-difficulty/scripts/xp_curve.py --levels 1-30 --kind exp --base 1000 --growth 1.15 --xp-per-hour 3000 --xp-rate-growth 1.13
python3 skills/level-designer/scripts/validate_graph.py examples/level-graph.json
```

## Validate the repo

```bash
python3 scripts/lint_skills.py                 # frontmatter, required sections, severities, script references
python3 -m unittest discover -s tests          # script behavior tests
python3 skills/gdd-owner/scripts/validate_registry.py design/   # in your game project
```

The same checks run in CI (`.github/workflows/ci.yml`).

## License

MIT. See `LICENSE`.
