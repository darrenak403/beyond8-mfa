# CLAUDE

## Priority And Scope

- This file combines project-specific execution rules and general coding behavior guidelines.
- **Priority order:** Project Rules first, General Guidelines second.
- If two rules conflict, follow project-specific rules in this repository.

## Project Rules (Repository-Specific)

### Core Principles

YAGNI · KISS · DRY · Brutal honesty over diplomacy · Challenge every assumption

### Execution Guardrails (Global)

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

### Performance Implementation Patterns

When implementing backend performance improvements, prefer these patterns:

- **Query shape first:** eliminate N+1 by batching or join-based retrieval before adding infra complexity.
- **Single-source data assembly:** build response payloads from one optimized query pass when feasible.
- **Async migration by compatibility layer:** add async variants first, keep sync fallback during transition.
- **Feature-flag rollout:** gate behavior changes (async path, optimization toggles) behind config flags.
- **Cache by volatility:** use longer TTL for rarely changing data, shorter TTL for user-progress/stateful data.
- **Versioned invalidation:** prefer key-version bumping over wildcard deletes to control cache churn.
- **Observability as part of implementation:** include slow query/request timing for any perf-sensitive change.
- **Gate progression by evidence:** move to the next optimization step only after tests and measurement pass.

### Structure

```
.claude/
  agents/     # sub-agents spawned by commands
  commands/   # slash commands (/plan, /cook, /fix, /learn, /code-review, /docs-fe)
  skills/     # behavioral guidance loaded by skill system
  rules/      # path-scoped design principles (lazy-load)
  hooks/      # shell hooks for lifecycle events
```

### Path-Scoped Rules

Path-scoped — each file loads only when touching its directory:

| File | Activates for |
|------|---------------|
| `.claude/rules/agents.md` | `.claude/agents/**` |
| `.claude/rules/commands.md` | `.claude/commands/**` |
| `.claude/rules/skills.md` | `.claude/skills/**` |

### Personal Overrides

`CLAUDE.local.md` (gitignored) — personal preferences that should not be committed.

## General Coding Guidelines

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

### 1) Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - do not pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what is confusing. Ask.

### 2) Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that was not requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3) Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Do not "improve" adjacent code, comments, or formatting.
- Do not refactor things that are not broken.
- Match existing style, even if you would do it differently.
- If you notice unrelated dead code, mention it - do not delete it.

When your changes create orphans:
- Remove imports/variables/functions that your changes made unused.
- Do not remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### 4) Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" -> "Write tests for invalid inputs, then make them pass"
- "Fix the bug" -> "Write a test that reproduces it, then make it pass"
- "Refactor X" -> "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```
1. [Step] -> verify: [check]
2. [Step] -> verify: [check]
3. [Step] -> verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
