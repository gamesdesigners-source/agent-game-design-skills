# Architecture

## Principles

1. **One source of truth.** Canon lives in `design/` inside the game project. Only the GDD Owner writes there.
2. **Proposals, not edits.** Specialists emit proposals. The Owner validates and commits.
3. **Design and Review are separate passes.** The skill that drafted something does not get the last word on whether it is good. A Review pass runs after the Design pass, ideally in a fresh context.
4. **Findings, not opinions.** Every review finding has an ID, severity, evidence, and a suggested fix.
5. **Numbers come from code.** Economy, combat and progression skills run scripts and report the output.
6. **Slice the context.** The Maestro passes each specialist only the GDD files it needs.

## Roles

| Role | Writes to `design/` | Generates content | Reviews |
|---|---|---|---|
| Design Maestro | no | plans only | arbitrates |
| GDD Owner | yes (only one) | no | contradictions, IDs, lifecycle |
| Specialists | no (proposals only) | yes | yes (Review mode) |

## Status lifecycle

```
proposed ──▶ approved ──▶ canon ──▶ deprecated
    │            │
    └──▶ rejected ◀┘
```

- `proposed`: drafted by a specialist, not yet reviewed.
- `approved`: passed review and Maestro arbitration, waiting for commit.
- `canon`: committed by the Owner. Other skills may depend on it.
- `deprecated`: replaced or removed. Kept in the registry so old references can be traced.
- `rejected`: kept in `proposals/resolved/` with the reason.

Only `canon` entries count as facts. Specialists treat `proposed` and `approved` entries as pending and say so in their output.

## Workflow

1. **Intake.** The Maestro reads `design/gdd/00-overview.md` and `design/registry.yaml`. If pillars, genre, platform or audience are missing, it asks the user before anything else.
2. **Plan.** The Maestro picks a chain from the routing table and writes a plan to `design/proposals/open/PLAN-<date>-<slug>.md`.
3. **Design pass.** Each specialist in the chain receives a context slice and writes proposals.
4. **Review pass.** Review-mode specialists audit the proposals and write findings to `design/findings/`.
5. **Arbitration.** The Maestro resolves conflicts by pillar priority. Taste calls go to the user. One revision round, then stop.
6. **Commit.** The Maestro sends the approved bundle to the Owner. The Owner validates (`scripts/validate_registry.py`), commits, updates `CHANGELOG.md`.
7. **Report.** The Maestro summarizes: made, changed in canon, needs decision.

## Context slicing

| Skill | Reads |
|---|---|
| level-designer | overview, mechanics, world, relevant zone entries, enemy registry |
| encounter-director | overview, mechanics, combat, enemy and zone registry |
| economy-designer | overview, economy, progression, item and currency registry |
| quest-designer | overview, narrative, world, characters, zone and item registry |

The Maestro should never dump the entire GDD into a specialist.

## Contracts

Defined in `templates/design/_contracts/`:

- `proposal.md`: change proposal format
- `finding.md`: review finding format
- `severity.md`: severity scale shared by all reviewers
- `bundle.md`: the handoff from Maestro to Owner
- `registry-schema.md`: ID prefixes and fields

## Failure containment

- Revision loops are capped at two rounds.
- Blockers stop the commit. Majors need a Maestro decision. Minors and notes ride along in the bundle.
- A contradiction against canon is always at least Major.
