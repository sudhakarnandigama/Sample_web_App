# Auth model — overview

> **Sources** — interview Q5; `Proposal/Documentation/project_documentation.md:111-125,621-637`; `docs/sources/decisions/2026-08-24-auth-transport.md`
> **Status** — [spec]
> **Page-size budget** — used 40 / 300 lines

<a id="flow"></a>
## Flow
1. **Login** — `POST /api/auth/login` receives `username` + `password` → [api/auth/login.md](../api/auth/login.md).
2. **Verify** — lookup `users` by `username`; verify `pbkdf2_sha256` hash of `password` against `users.password_hash`.
3. **Issue** — sign JWT HS256 with `JWT_SECRET`. Claims: `sub` = users.id, `role` = users.role, `exp` = now + `JWT_EXPIRE_MINUTES`.
4. **Attach** — Angular `auth.service.ts` stores the token; `auth.interceptor.ts` sets `Authorization: Bearer <jwt>` on every request.
5. **Validate** — FastAPI dependency decodes the JWT, checks `exp`, and maps `role` → scopes per [auth/02-scopes.md](02-scopes.md). Missing/invalid/expired → 401. Insufficient scope → 403.

<a id="token"></a>
## Token
- Format: JWT, HS256.
- Claims: `sub` (integer user id), `role` (`ADMIN` | `LEARNER`), `exp` (epoch seconds).
- Signing key: `JWT_SECRET` — see [ops/env-vars.md](../ops/env-vars.md).
- Library: `PyJWT`.

<a id="password"></a>
## Password storage
- `users.password_hash` = `pbkdf2_sha256$<salt_hex>$<hash_hex>` (stdlib `hashlib.pbkdf2_hmac`, 100k iterations).
- Plaintext passwords are never stored or logged.

<a id="demo-accounts"></a>
## Demo accounts
- Admin: `admin` / `admin123` (role `ADMIN`)
- Learner: `learner` / `learner123` (role `LEARNER`)
Seeded per [test/fixtures.md](../test/fixtures.md); local demo only.

<a id="verify"></a>
## Verify

```bash
python -c "import jwt; print(sorted(jwt.PyJWS().algorithms) if hasattr(jwt.PyJWS(),'algorithms') else 'PyJWT installed')"
```
Expected: `PyJWT installed` (backend has the JWT dependency available).
