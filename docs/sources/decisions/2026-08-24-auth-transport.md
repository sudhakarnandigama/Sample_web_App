# ADR — Authentication transport and password storage

- **Date:** 2026-08-24
- **Status:** accepted
- **Supersedes:** none

## Context

The PRD specifies only "simple demo authentication" (`Proposal/Documentation/project_documentation.md:69`, `:123`) and explicitly excludes complex OAuth providers (`Proposal/Documentation/project_documentation.md:1343`). The transport mechanism and password storage were unspecified.

The user confirmed on 2026-08-24: **JWT bearer with a role claim (`ADMIN` | `LEARNER`)**.

## Decision

1. **Token:** JWT, HS256, signed with `JWT_SECRET`. Claims: `sub` (user id), `role` (`ADMIN` | `LEARNER`), `exp` (epoch seconds).
   - Library: `PyJWT` (added to `backend/requirements.txt`).
   - Header required on protected endpoints: `Authorization: Bearer <jwt>`.
2. **Password storage:** never plaintext. Store `pbkdf2_sha256$<salt_hex>$<hash_hex>` in `users.password_hash`.
   - Hash function: Python stdlib `hashlib.pbkdf2_hmac('sha256', password, salt, 100_000)`.
   - No extra dependency required (stdlib).
3. **Authorization:** the JWT carries a `role` claim, not a scope list. The authorization layer maps `role` to the scope set in `docs/wiki/auth/02-scopes.md`. An endpoint requiring a scope the role does not hold returns 403.

## Consequences

- `backend/requirements.txt` gains `PyJWT`.
- `users` stores `password_hash`, never a raw password.
- Every protected endpoint page in the wiki declares a required scope per `docs/wiki/auth/02-scopes.md`.
