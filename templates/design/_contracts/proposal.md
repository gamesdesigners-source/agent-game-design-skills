# Proposal contract

A proposal is how a specialist asks to change canon. One file per proposal in `design/proposals/open/`.

Filename: `PROP-<NNNN>-<skill>-<slug>.md`

```markdown
---
id: PROP-0042
author: economy-designer
created: 2026-10-04
status: proposed          # proposed | approved | rejected | needs-info
adds: [CUR-gem, ITM-gem-pouch]
modifies: [SHOP-blacksmith]
removes: []
affects: [QST-0007, ENM-ogre]   # things that depend on the above
pillars_checked: [P1, P3]
---

## Summary
One or two sentences.

## Change
The actual content. Use registry IDs for anything that already exists.
New entries use the schema in `registry-schema.md`.

## Rationale
Why this serves the pillars.

## Risks
What could go wrong. Include exploit ideas.

## Open questions
Things the Owner or user must answer.
```

## Rules

- Reference existing things by ID. Never restate their details.
- Propose new IDs in the correct prefix. The Owner may rename on conflict.
- Declare `affects` honestly. The Owner uses it to find contradictions.
- If the proposal depends on another open proposal, say so under Open questions.
