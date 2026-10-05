# Finding contract

A finding is one problem found in review. Review-mode skills write findings to `design/findings/FIND-<NNNN>.md` or return them as a list in the same format.

```markdown
---
id: FIND-0107
reviewer: encounter-director
target: PROP-0042            # proposal or canon ID under review
severity: Major              # Blocker | Major | Minor | Note
check: ENC-R04               # checklist ID from the reviewer's SKILL.md
status: open                 # open | fixed | accepted | wontfix
---

## Problem
What is wrong, in one or two sentences.

## Evidence
Concrete reference: a room ID, a number, a step in the player path.
"Ranged enemies at ENM-archer spawn 4m behind cover CVR-02, which has no flank route."

## Player impact
What the player experiences. Use a persona if it helps (newbie, speedrunner, completionist, griefer).

## Suggested fix
A specific change. If there are tradeoffs, list two options.

## Reproduction
How to trigger it, if it is an exploit or soft-lock.
```

## Rules

- No finding without evidence.
- No finding without a suggested fix, even if rough.
- Use the checklist ID so results are comparable between runs.
- Do not merge unrelated problems into one finding.
- Report what is wrong, then what is good in a short closing line. A review with zero findings must state what was checked.
