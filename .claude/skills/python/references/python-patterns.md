# Python Patterns — Types, Async, DI

Language and structure patterns for maintainable services. Routing and security policies live in other reference files.

## Typing

- Prefer **explicit** annotations on public functions and service methods.
- Use `from __future__ import annotations` for forward refs when needed.
- Return type `None` for side-effect functions.
- For JSON-like blobs use `TypedDict` or Pydantic models — not bare `dict` in service signatures.
- `Protocol` for narrow interfaces (e.g. cache backend) instead of concrete classes.

## Pydantic v2

- Settings: `pydantic_settings.BaseSettings` with `model_config = SettingsConfigDict(env_file=".env")`.
- Use `Field(..., description=...)` for OpenAPI; `model_validate` / `model_dump` at boundaries.
- Prefer **computed fields** and validators over mutating in routers.

## FastAPI dependency injection

- **Reusable dependencies** in `core/deps.py`: `get_db`, `get_current_user`, pagination params.
- Dependencies that open resources should be **generator** functions with `yield` and teardown after `yield`.
- Avoid calling `Depends` inside plain functions — only in route signatures or nested `Depends`.
- Keep shared endpoint response builders in `app/helpers/` and import from there in routers.

## Async

- **Consistent async stack**: async routes → async session / httpx / async DB driver.
- Do not block the event loop: use `asyncio.to_thread()` for CPU-heavy or legacy sync I/O if unavoidable.
- Timeouts on all external HTTP (`httpx.AsyncClient(timeout=...)`).

## Errors

- Raise **`HTTPException`** in the HTTP layer only when mapping from domain/service errors.
- In services, prefer **returning a result type** or raising **domain-specific exceptions** caught by an exception handler in `main.py` that maps to stable JSON error envelopes.

## Transactions

- With request-scoped DB dependencies, prefer `flush()` in services/CRUD and let `get_db` own commit/rollback.
- If conflict handling is needed inside an outer transaction, use `begin_nested()` (savepoint) instead of rolling back the whole request transaction.

## Logging

- Use **`logging`** with structured context (`extra={...}`) or structlog if the project already does.
- Never log secrets, raw tokens, or full PII — log ids and coarse outcomes.

## Small style rules

- Import order: stdlib → third party → local (`isort` / Ruff).
- Prefer `pathlib.Path` over `os.path` for filesystem work.
- `dataclasses` for simple internal structs; **Pydantic** for anything serialized or validated at API boundaries.
