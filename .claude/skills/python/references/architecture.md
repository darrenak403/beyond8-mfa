# Architecture — Python API / Service Layout

Keep **dependency direction** clear: outer layers (HTTP) call inward; database and frameworks stay at the edges.

## Typical FastAPI package (this repo style)

```
app/
  main.py           # FastAPI app, middleware, lifespan, include_router
  api/              # HTTP: routers only — thin
    v1/
      api.py        # aggregates routers
      endpoints/    # path operations → call services / crud
  core/             # settings, security helpers, deps used app-wide
  schemas/          # Pydantic request/response DTOs (API contract)
  models/           # SQLAlchemy ORM models (persistence shape)
  crud/             # DB operations per aggregate (queries, commits)
  services/         # orchestration, domain rules spanning CRUD + external calls
  db/               # engine, session, Base
  middleware/
  tests/
```

**Rule of thumb**

| Layer | May import from | Must not |
|-------|-------------------|----------|
| `endpoints` | `schemas`, `services`, `core.deps`, FastAPI | Heavy ORM logic inline |
| `services` | `crud`, `schemas`, `models` (read), other services | FastAPI `Request` types |
| `crud` | `models`, `db.session` | HTTP concepts |
| `schemas` | stdlib, pydantic | `models` (avoid circular ORM in DTOs) |
| `models` | SQLAlchemy | business services |

## Responsibilities

- **endpoints** — parse path/query/body, call one service or crud function, map to response schema, raise HTTPException with correct status.
- **services** — business rules, transactions spanning multiple CRUD calls, call external APIs.
- **crud** — `session.execute(select(...))`, `session.add`, filters, pagination primitives.
- **schemas** — everything the client sees; version API models here, not on ORM entities.
- **core/config** — `pydantic-settings` for env; single source of truth for constants.

## Anti-patterns

- Raw SQL or `session.get` loops inside routers.
- Importing `endpoints` from `services` or `crud`.
- Putting JWT verification logic duplicated in every route instead of a dependency in `core/deps.py`.

## When to split a new module

- New bounded context (e.g. billing vs auth) → new `services/` + `endpoints/` subtree or a package boundary.
- Shared utilities used by many layers → `core/` or a small `lib/` (keep it tiny).
