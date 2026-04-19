# Testing — pytest + FastAPI

Unit and API tests for Python services. Keep tests **fast**, **deterministic**, and **readable**.

## Layout

- Mirror package under `app/tests/` or `tests/` — one file per module or feature: `test_auth_service.py`.
- Shared fixtures in `conftest.py` next to tests (pytest auto-loads).

## pytest basics

- **Parametrize** for input matrices instead of copy-paste cases.
- Use **`pytest.mark.asyncio`** (pytest-asyncio) for async tests when not using Starlette's runner helpers consistently.
- **`monkeypatch`** for env and small replacements; **`unittest.mock`** for patching imports.

## HTTP / FastAPI

- Prefer **`httpx.AsyncClient`** with `ASGITransport(app=...)` for async apps, or `TestClient` for sync stack.
- Override dependencies for auth: `app.dependency_overrides[get_current_user] = lambda: fake_user`.
- Use a **transaction rollback** or **SQLite in-memory** pattern for DB isolation; avoid hitting production-like external services in unit tests.

## Database

- **Fixture per test function** that yields a session and rolls back, or truncate tables between tests if integration.
- For Postgres-specific behavior, reserve **integration** job (CI) with Testcontainers or a disposable DB — not every dev machine needs it.

## What to cover

- Happy path + **one representative failure** per branch (401, 404, 409).
- **Validation** edge cases: empty string, max length, malformed UUID.
- Service logic with **mocks** on external HTTP clients and email senders.

## Commands

```bash
python -m pytest                           # default discovery
python -m pytest app/tests -q              # package only
python -m pytest path/test_file.py::name  # single test
python -m pytest -k "otp and not slow"   # keyword filter
python -m pytest --tb=short --maxfail=1  # tight loop while fixing
```

## Coverage (optional)

- `pytest-cov`: aim for high coverage on **services** and **critical paths**, not blind 100% on trivial getters.
