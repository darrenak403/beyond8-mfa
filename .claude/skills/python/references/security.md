# Security — Python Web Services

Secrets, authn/z, input handling, data access, and dependency hygiene. Not routing structure (see `api-design.md`).

## Secrets & config

- Load from **environment** or secret manager — never commit `.env` with real credentials.
- Rotate **JWT signing keys** with a documented procedure; short-lived access tokens + refresh where applicable.
- `pydantic-settings` validates types at startup — fail fast on missing required vars in production.

## Authentication / authorization

- Verify JWT (signature, `exp`, `aud`/`iss` if used) in **one dependency**; endpoints declare role requirements explicitly.
- Prefer **scoped permissions** over a single `is_admin` flag when the product grows.
- Log **auth failures** without echoing tokens or passwords.

## Input validation

- **Pydantic** for all request bodies and query models — reject unknown fields if ambiguity is dangerous (`model_config` extra behavior).
- Normalize strings (`strip`, casefold for emails) in validators, not scattered in handlers.

## SQL injection

- **Always** bind parameters: SQLAlchemy `select(Model).where(Model.id == id)` — never string-concat SQL with user input.
- Raw SQL only with bound params (`text("... WHERE id = :id").bindparams(...)`).

## SSRF & outbound HTTP

- If user-supplied URLs are fetched server-side, **allowlist** schemes and hosts; set timeouts and size limits.

## Headers & transport

- Enforce **HTTPS** in production; set secure cookie flags if using cookies.
- **CORS** allowlist explicit origins — avoid `*` with credentials.
- Consider **rate limiting** on auth and OTP endpoints (middleware or reverse proxy).

## Dependency audit

```bash
pip-audit                           # or poetry audit / safety
```

- Pin versions in `requirements.txt` / lockfile; review major upgrades.

## Checklist (release)

- [ ] No secrets in repo or logs
- [ ] JWT / session settings appropriate for environment
- [ ] All mutating endpoints require auth unless intentionally public
- [ ] Error responses do not leak stack traces or internal ids unnecessarily
- [ ] `pip-audit` (or equivalent) clean or exceptions documented
