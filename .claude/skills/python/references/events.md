# Events & Background Work — Python

Out-of-request work: reliability, retries, and idempotency. Not HTTP routing (see `api-design.md`).

## FastAPI `BackgroundTasks`

- Good for **best-effort** follow-ups (email, analytics) tied to a request lifecycle.
- **Not durable**: if the process dies after response, the task may not run — do not use for money movement without another guarantee.

## asyncio

- `asyncio.create_task` for fire-and-forget inside the app — document cancellation on shutdown (lifespan hooks).
- Prefer **structured** patterns: bounded queues + worker tasks for backpressure.

## Durable queues (when you need them)

- **Celery**, **RQ**, **Arq**, or cloud queues (SQS, Pub/Sub) for work that must survive restarts.
- Message body: **versioned schema** + **idempotency key**; consumer must handle duplicates (at-least-once delivery).

## Idempotency

- Store processed message ids or business keys in DB with a **unique constraint** — duplicate insert → noop path.
- HTTP callbacks: verify signatures (HMAC) and timestamp skew.

## Transaction boundaries

- **Outbox pattern**: write domain row + outbox row in same DB transaction; separate process publishes — avoids "DB committed but message lost".

## Logging

- Include **correlation id** (request id) propagated to background jobs when possible for traceability.
