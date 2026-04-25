---
name: python
description: Python backend implementation — FastAPI/Starlette, Pydantic v2, SQLAlchemy 2 + Alembic, pytest and httpx, async I/O, security, performance, packaging (uvicorn, Docker). Enforces layered app/ constraints (endpoints→services→crud), stable public API paths and JSON fields unless explicit breaking change, Alembic for schema. Activate for Python APIs, services, migrations, tests, refactors, or code review.
---

# Python — Service & API Implementation

Load only the reference needed for the current task.

## Mandatory rules (always honor)

These apply to **this** FastAPI service layout (`app/` with `api`, `services`, `crud`, `schemas`, `models`, `core`, `db`). Full matrices and rationale: [`references/architecture.md`](references/architecture.md). Public HTTP rules: [`references/api-design.md`](references/api-design.md) (contract stability).

1. **Dependency direction** — `endpoints` → `services` → `crud` → `models`. Never import `endpoints` from `services` or `crud`. Never put heavy ORM/query loops in routers.
2. **Thin HTTP layer** — Routers validate via Pydantic, call service layer, return schemas. No business rules or direct CRUD access in path operations.
3. **Stable public API** — Do not rename route paths, HTTP methods, query parameter names, or **documented** JSON response field names unless the task explicitly requires a breaking change **and** a version or migration plan for clients.
4. **Persistence** — Schema changes go through **Alembic** migrations; do not hand-edit production DB without a migration. ORM models stay in `models/`; API shapes stay in `schemas/`.
5. **Auth cross-cutting** — Reuse `core.deps` / shared dependencies for JWT and admin checks; do not duplicate verification logic across endpoints.
6. **Refactors** — Readability-only cleanups must **not** change behavior, status codes, or externally visible payloads unless explicitly requested.
7. **Transaction owner** — Request scope (`db.session.get_db`) owns commit/rollback. Service/CRUD should prefer `flush()` and avoid nested `commit()` unless explicitly required by task semantics.
8. **Shared helpers** — Reusable response helpers live under `app/helpers/` (example: OTP stats/history helpers). Endpoints should import shared helpers from this package, not from sibling endpoint modules.

## Reference Map

| Task | When to load | File |
|------|----------------|------|
| **Constraints & layout** — MUST/MUST NOT layers, imports, migrations, where code goes | Any change touching `app/` | [`references/architecture.md`](references/architecture.md) |
| Idioms, typing, async, DI (`Depends`) | Writing or reviewing Python | [`references/python-patterns.md`](references/python-patterns.md) |
| REST routes, status codes, response shapes | API design or new endpoint | [`references/api-design.md`](references/api-design.md) |
| pytest, fixtures, HTTP client tests | Writing or fixing tests | [`references/testing.md`](references/testing.md) |
| Secrets, auth, validation, injection, logging | Security | [`references/security.md`](references/security.md) |
| Background work, queues, idempotency | Async side effects / events | [`references/events.md`](references/events.md) |
| DB sessions, N+1, caching, concurrency | Performance | [`references/performance.md`](references/performance.md) |
| venv, uvicorn, deps, Docker, migrations | Run / deploy / tooling | [`references/runtime-packaging.md`](references/runtime-packaging.md) |

---

## Decision Tree

```
TASK?
│
├─ New feature / endpoint
│  ├─ Layer placement?          → references/architecture.md
│  ├─ REST shape & errors?      → references/api-design.md
│  └─ Services & typing?       → references/python-patterns.md
│
├─ Tests / TDD
│  └─ pytest, mocks, API tests  → references/testing.md
│
├─ Security
│  └─ Input, DB, secrets, JWT   → references/security.md
│
├─ Side effects / messaging
│  └─ tasks, retries, dedup      → references/events.md
│
├─ Slow or heavy load
│  └─ DB, async, cache          → references/performance.md
│
├─ How to run / ship / migrate
│  └─ uvicorn, Docker, Alembic   → references/runtime-packaging.md
│
└─ Code review
   ├─ MUST / MUST NOT (layers, API freeze)? → references/architecture.md + api-design.md
   ├─ Types / async smells?      → references/python-patterns.md
   └─ OWASP-style issues?        → references/security.md
```

---

## Coverage

- **Constraints** — MUST-layer rules, import bans, public API stability, migration discipline
- **Layout** — routers vs services vs CRUD vs schemas vs `core` settings
- **Python 3.11+** — type hints, `Protocol`, structural typing, `match`, pathlib
- **FastAPI** — dependencies, lifespan, exception handlers, OpenAPI discipline
- **Pydantic v2** — models, validators, settings (`BaseSettings`)
- **SQLAlchemy 2** — `select()`, async session, Alembic migrations
- **Testing** — pytest, fixtures, `AsyncClient`, DB test strategies
- **Security** — parameterized queries, least-privilege secrets, CORS, JWT hygiene
- **Events** — `BackgroundTasks`, outbox, message consumers at a high level
- **Performance** — eager loading, indexes, pool sizing, streaming responses
- **Runtime** — uvicorn/gunicorn workers, `.env`, container entrypoints
