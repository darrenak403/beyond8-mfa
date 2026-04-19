---
name: python
description: Python backend implementation — FastAPI/Starlette, Pydantic v2, SQLAlchemy 2 + Alembic, pytest and httpx, async I/O, security, performance, packaging (uvicorn, Docker). Activate for Python APIs, services, migrations, tests, or code review.
---

# Python — Service & API Implementation

Load only the reference needed for the current task.

## Reference Map

| Task | When to load | File |
|------|----------------|------|
| Where does code go? Layers and imports | New feature or refactor | [`references/architecture.md`](references/architecture.md) |
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
   ├─ Layer violations?          → references/architecture.md
   ├─ Types / async smells?      → references/python-patterns.md
   └─ OWASP-style issues?        → references/security.md
```

---

## Coverage

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
