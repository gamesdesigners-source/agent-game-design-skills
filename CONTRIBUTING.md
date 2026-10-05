# Contributing

## Skill anatomy

Every skill lives in `skills/<name>/SKILL.md` and must have:

1. **YAML frontmatter** with `name` (matches folder) and `description` (one or two sentences that say what it does and when to trigger it).
2. **Required context**: what it reads from `design/` and what it asks the user if missing.
3. **Design mode**: step-by-step procedure and output schema.
4. **Review mode**: a checklist where each item has an ID, severity guidance, and what evidence to cite.
5. **Failure modes**: how players or teammates will break the output.
6. **Handoff**: which proposals or findings it emits, using the contracts in `templates/design/_contracts/`.
7. **Don'ts**: short list of things the skill must never do.

`python3 scripts/lint_skills.py` enforces this. The two coordinators (`design-maestro`, `gdd-owner`) skip the Design/Review/Handoff sections. `playtest-simulator` uses `## Procedure` and `## Review checklist` because its job is simulation, not drafting.

Scripts a skill relies on live in that skill's own `scripts/` folder, not at the repo root, so the skill works when installed alone. Add a test for every script in `tests/test_scripts.py`.

## Rules

- Specialists never write to `design/` directly. They emit proposals and findings.
- Keep a SKILL.md under 400 lines. Move long tables and examples to `references/`.
- Findings must carry severity, evidence and a suggested fix. No vague advice.
- Numbers come from scripts, not from the model's head.
- Don't invent mechanics, IDs or lore that aren't in the GDD. Propose them instead.

## Adding a skill

1. Copy `skills/_template/SKILL.md` or any existing specialist.
2. Add a row to the README table and a route in `design-maestro/references/routing-table.md`.
3. Run the linter and tests.
4. Open a PR.
