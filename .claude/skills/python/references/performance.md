# Performance — Python + SQLAlchemy + Async

Measure before optimizing. Focus on **I/O**, **database**, and **concurrency** first.

## Database

- **N+1**: use `selectinload` / `joinedload` for known relationship graphs; profile with SQL logging in dev.
- **Indexes** on foreign keys and columns used in `WHERE`, `ORDER BY`, and join predicates — verify with `EXPLAIN ANALYZE` on Postgres.
- **Pagination**: keyset > offset for large tables.
- **Connection pool**: size for expected concurrency + headroom; watch pool timeouts under load.

## Async SQLAlchemy

- One session per request (dependency scope); avoid sharing mutable session across concurrent tasks.
- Keep transactions **short** — do not hold DB transactions open across external HTTP calls when avoidable.

## Caching

- **Redis** or in-process LRU for hot read-mostly keys; TTL + explicit invalidation strategy.
- Cache **stable keys** (ids), not unbounded user-defined strings without bounds.

## CPU-bound work

- Offload to **worker processes** or thread pool (`asyncio.to_thread`) so the event loop stays responsive.

## HTTP / API

- Stream large downloads with **iterators** / `StreamingResponse` instead of buffering entire payloads in memory.
- gzip/brotli at reverse proxy layer for text responses.

## Serialization

- Pydantic `model_dump` in hot loops: minimize redundant conversions; sometimes plain tuples/dicts are faster for internal paths — profile if needed.

## Observability

- Add timing metrics around slow queries and external calls; use **OpenTelemetry** if the org standardizes on it.
