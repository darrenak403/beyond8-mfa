# Runtime & Packaging — Python Services

How to run, containerize, and migrate. Not application layer design (see `architecture.md`).

## Virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\pip install -r requirements.txt
# Unix
.venv/bin/pip install -r requirements.txt
```

- Commit **`requirements.txt`** or **`pyproject.toml` + lockfile** — pick one strategy per repo.
- Pin **production** deps; dev tools (`pytest`, `ruff`) in a separate optional group or `requirements-dev.txt` if useful.

## ASGI server

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

- Production: **gunicorn** + `uvicorn.workers.UvicornWorker` or platform-native process manager (Kubernetes, ECS).
- Workers × threads tuned to CPU and **DB pool** limits.

## Docker

- **Multi-stage** builds: slim final image, non-root user, healthcheck `curl`/`wget` to `/health` if exposed.
- Do not bake secrets into images — inject at runtime.

## Migrations (Alembic)

```bash
alembic revision --autogenerate -m "describe change"   # review diff always
alembic upgrade head
```

- Autogenerate is a **draft** — verify constraints, server defaults, and data backfills.
- Destructive changes: plan **expand/contract** migrations for zero-downtime when required.

## Static checks (optional but recommended)

```bash
ruff check .
ruff format .
mypy app
```

- Run in CI on every PR for team repos.

## Environment-specific behavior

- Use explicit `ENV=development|staging|production` to toggle docs exposure, seed data, and strict CORS.
