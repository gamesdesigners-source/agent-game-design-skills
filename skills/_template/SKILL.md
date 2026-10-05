---
name: your-skill-name
description: One or two sentences. Say what the skill does and when to trigger it.
---

# Skill Title

One paragraph: the role and the one thing it must get right.

## Required context

What to read from `design/`. What to ask the user if missing.

## Design mode

1. Step-by-step procedure.
2. Output schema (tables, graph, numbers).
3. Emit proposals per `design/_contracts/proposal.md`.

## Review mode

| ID | Check | Default severity |
|---|---|---|
| XXX-R01 | | |

Emit findings per `design/_contracts/finding.md`. Cite evidence for each.

## Failure modes

How players, teammates or the model itself will break this output.

## Handoff

Which proposals and findings this skill emits, and which skills usually consume them.

## Don'ts

- Don't write to `design/`.
- Don't invent IDs, mechanics or lore that are not in the GDD. Propose them.
