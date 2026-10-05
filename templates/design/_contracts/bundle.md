# Bundle contract

The bundle is the handoff from the Design Maestro to the GDD Owner. One file per run: `design/proposals/open/BUNDLE-<date>-<slug>.md`.

```markdown
---
id: BUNDLE-2026-10-04-first-dungeon
maestro_request: "Design the first dungeon"
proposals: [PROP-0040, PROP-0041, PROP-0042]
findings_open: [FIND-0107]        # must contain no Blockers
revision_rounds: 1
---

## Summary
What was designed.

## Approved
| Proposal | Result | Notes |
|---|---|---|
| PROP-0040 | approve | |
| PROP-0041 | approve | revised after FIND-0102 |

## Rejected
| Proposal | Reason |
|---|---|

## Accepted risks
Majors the Maestro chose to accept, each with a reason.

## Decisions needed from the user
Taste calls and open questions.
```

## Owner checks before commit

1. No open Blockers.
2. Every Major is fixed or listed under Accepted risks.
3. Every `adds`, `modifies`, `removes` target resolves in the registry or in the same bundle.
4. No ID collisions.
5. No pillar contradiction.
6. `scripts/validate_registry.py design/` passes after the change.
