# my-skills

## Core Principles

YAGNI · KISS · DRY · Brutal honesty over diplomacy · Challenge every assumption

## Execution Guardrails (Global)

These rules apply to all implementation tasks in this repository:

1. **Plan fidelity is mandatory**
   - Implement exactly what is approved in the plan.
   - Do not change API contracts, response shapes, endpoint semantics, or migration strategy unless the plan explicitly says so.
   - If a deviation is required, stop and ask the user first.

2. **Todo discipline is mandatory**
   - Use existing todos; do not recreate duplicates.
   - Set exactly one todo to `in_progress` at a time.
   - Move to next todo only after validation for current todo is complete.
   - Do not mark `completed` without evidence (tests/verification output).

3. **Backward compatibility default**
   - Existing endpoint behavior is preserved by default.
   - Any breaking change requires explicit user approval.
   - If optimization conflicts with compatibility, prioritize compatibility and propose a phased migration.

4. **Verification before done**
   - Before claiming completion, run relevant tests/lints for changed areas.
   - Report what was executed and concrete outcomes.
   - If verification cannot be executed, state that clearly and provide exact manual commands.

5. **No hidden scope expansion**
   - Avoid unrelated refactors while implementing a plan.
   - Keep changes minimal and localized to plan scope.
   - If unexpected issues appear, surface them and ask for direction.

## Structure

```
.claude/
  agents/     # sub-agents spawned by commands
  commands/   # slash commands (/plan, /cook, /fix, /learn, /code-review, /docs-fe)
  skills/     # behavioral guidance loaded by skill system
  rules/      # path-scoped design principles (lazy-load)
  hooks/      # shell hooks for lifecycle events
```

## Rules

Path-scoped — each file loads only when touching its directory:

| File | Activates for |
|------|---------------|
| `.claude/rules/agents.md` | `.claude/agents/**` |
| `.claude/rules/commands.md` | `.claude/commands/**` |
| `.claude/rules/skills.md` | `.claude/skills/**` |

## Personal overrides

`CLAUDE.local.md` (gitignored) — personal preferences that shouldn't be committed.
