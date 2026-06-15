# Agent Instructions

This repository is an Agent Skills repository. Preserve the open Agent Skills structure:

- Each skill lives at `skills/<skill-name>/`.
- Each skill must include `SKILL.md` with YAML frontmatter containing `name` and `description`.
- Optional skill resources should stay inside the skill directory, typically under `scripts/`, `references/`, or `assets/`.
- Keep `SKILL.md` concise and procedural; use references only for details that should load conditionally.
- Do not copy full source articles into skills.
- Keep trigger-critical wording in the `description` because agents use it for discovery.
- Verify current pricing, support windows, cloud-provider state, marketplace behavior, and Redis version support before adding claims that could drift.
- Treat destructive Redis, cloud, billing, account, or data operations as confirmation-sensitive.

Before finishing skill edits, run:

```bash
./scripts/validate-skills.sh
```
