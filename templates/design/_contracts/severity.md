# Severity scale

All reviewers use the same scale so the Maestro can compare findings across skills.

| Severity | Meaning | Effect on the bundle |
|---|---|---|
| **Blocker** | Breaks the game, soft-locks the player, contradicts a pillar, or makes a canon entry impossible. | Bundle cannot be committed until fixed. |
| **Major** | Seriously hurts the experience or contradicts canon in a fixable way. Dominant strategy, unreadable critical path, broken economy loop. | Maestro must fix or explicitly accept with a reason. |
| **Minor** | Noticeable quality issue that doesn't threaten the design. | May ship with a note. |
| **Note** | Suggestion or observation. | Optional. |

## Calibration examples

- Player can kill the only quest-giver before accepting the quest and the main path needs that quest: **Blocker**.
- One weapon has 2x the DPS of every alternative at the same cost: **Major**.
- Two enemy types share nearly identical silhouettes: **Minor**.
- A room could use another cover object: **Note**.

## Rules

- A finding that contradicts a `canon` entry is at least **Major**.
- A finding that violates a pillar is at least **Major**.
- When unsure between two levels, pick the higher and say why.
