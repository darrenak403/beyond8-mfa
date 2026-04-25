# API Design — REST + FastAPI

URLs, methods, status codes, bodies, and handler shape. Security policy details live in `security.md`. **Layer and import MUST/MUST NOT:** see [`architecture.md`](architecture.md).

## Contract stability (MUST for existing APIs)

When editing **published** endpoints (anything external clients or the FE already call):

- **MUST NOT** change `path`, `method`, or **names** of query parameters / JSON body keys / top-level response envelope fields **unless** the task explicitly authorizes a breaking change and mentions versioning or client migration.
- **MAY** add new **optional** query or body fields and new response fields that old clients can ignore.
- **MAY** tighten validation (stricter Pydantic rules) only if it does not reject payloads that were previously accepted **without** product agreement — otherwise treat as breaking.

New endpoints under a new prefix or version (`/api/v2/...`) follow the same conventions once published.

## URL conventions

- **Plural nouns**, **kebab-case** segments where style allows; prefix with `/api/v1` when versioning.
- **Nouns in paths**, verbs only for true RPC-style actions (`/auth/login`, `/tokens/refresh`).
- Avoid depth > 3 after the version prefix; prefer new top-level resource with filter query params.

## Methods & status codes

| Operation | Method | Success | Typical errors |
|-----------|--------|---------|----------------|
| List / query | GET | 200 | 400 bad filter |
| Get one | GET | 200 | 404 |
| Create | POST | 201 + `Location` optional | 400 / 409 conflict |
| Full replace | PUT | 200 | 400 / 404 |
| Partial update | PATCH | 200 | 400 / 404 |
| Delete | 204 (no body) or 200 with message | 404 |
| Auth missing | any | — | 401 |
| Forbidden | any | — | 403 |

Use **422** for Pydantic validation errors (FastAPI default) — document that for API consumers.

## Response shape

- Prefer **one consistent envelope** if the product already uses it (e.g. `{ "data": ..., "error": null }`).
- For errors, return a **stable machine-readable `code`** plus human `message` — avoid leaking stack traces in production.

## FastAPI handler shape

```python
@router.post("/items", status_code=201, response_model=ItemRead)
async def create_item(
    payload: ItemCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ItemRead:
    return await item_service.create(db, user, payload)
```

- Validation happens **before** the body hits the function (Pydantic).
- Keep the function **one screen**; push logic to `service` / `crud`.
- For shared response-building logic across endpoints, place helpers under `app/helpers/` and import from there.

## Pagination & filtering

- **Cursor** pagination for large/unstable lists; **offset/limit** only for small admin tables.
- Accept filters as **query params** with explicit types (`uuid`, `datetime`, enums).

## OpenAPI / versioning

- Breaking changes → new path prefix (`/api/v2`) or negotiated version header — pick one strategy per product.
- Deprecate fields in schema descriptions before removal.

## Idempotency

- `POST` that creates billing side effects should support **Idempotency-Key** header when duplicates are costly; document behavior.
