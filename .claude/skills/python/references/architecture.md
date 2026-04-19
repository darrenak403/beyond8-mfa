# Architecture — Python API / Service Layout

Keep **dependency direction** clear: outer layers (HTTP) call inward; database and frameworks stay at the edges.

---

## Mandatory constraints (MUST / MUST NOT)

Use these as **hard gates** in code review and implementation. They encode the layered FastAPI style used in this repo; they are **stricter than generic PEP 8**.

### Layering and imports

| Rule | MUST / MUST NOT |
|------|------------------|
| Call direction | **MUST** follow: `api/v1/endpoints` → `services` → `crud` → `models` / `db`. |
| Reverse imports | **MUST NOT** import `endpoints` or `api` from `services`, `crud`, `models`, or `schemas`. |
| HTTP in inner layers | **MUST NOT** use `FastAPI`, `APIRouter`, `Request`, or `HTTPException` inside `crud` or `models`. Raise domain errors or return values from services; map to HTTP at the router or a central exception handler. |
| SQL in routers | **MUST NOT** embed raw SQL, `session.execute`, or multi-statement ORM workflows in `endpoints`. Delegate to `crud` or `services`. |
| `schemas` purity | **MUST NOT** import SQLAlchemy `models` into Pydantic modules if it creates cycles or leaks ORM into the API contract. Prefer dedicated DTOs and explicit mapping at the service or router boundary. |
| `services` scope | **MAY** import `crud`, `schemas`, `models` (read-only metadata), and other services. **MUST NOT** depend on FastAPI request context types; pass primitives/DTOs from endpoints. |

### Public contract and persistence

| Rule | MUST / MUST NOT |
|------|------------------|
| Route and method names | **MUST NOT** rename path segments, router prefixes, or HTTP methods for existing published endpoints **unless** the user explicitly requests a breaking API change and documents client impact. |
| Query and body fields | **MUST NOT** rename query parameters or JSON fields that external clients rely on **without** the same explicit breaking-change requirement. Adding **optional** fields is allowed. |
| Database identifiers | **MUST NOT** rename tables/columns or drop objects **without** an Alembic revision (and a data plan if needed). |
| Migrations | **MUST** add or adjust Alembic versions when ORM models or constraints change; **MUST NOT** rely on silent `create_all` in production for schema evolution. |

### Refactors and cleanup

| Rule | MUST / MUST NOT |
|------|------------------|
| Behavior | **MUST NOT** change business outcomes, HTTP status codes, or response payloads during “style only” or readability refactors **unless** the user explicitly asks for a behavior change. |
| Dead code | **MAY** remove unused functions/imports when **statically verifiable** unused; **MUST NOT** remove public symbols that could be part of an undocumented external contract without confirmation. |

### Architecture style (informative)

This layout is **layered service + CRUD**, not full **Ports & Adapters / Clean Architecture**. That is intentional (YAGNI). Introduce `Protocol` repositories or a `domain/` package only when the team needs stronger isolation from the DB or framework — not by default.

---

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
