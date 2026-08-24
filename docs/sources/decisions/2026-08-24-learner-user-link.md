# ADR — Linking learners to login accounts

- **Date:** 2026-08-24
- **Status:** accepted
- **Supersedes:** none

## Context

The PRD §17 relationship diagram shows `users → learners` (`Proposal/Documentation/project_documentation.md:590-592`), but the `learners` table field list in §16.3 (`Proposal/Documentation/project_documentation.md:510-518`) omits any `user_id` column. Learner login (§5.1, `Proposal/Documentation/project_documentation.md:119`) requires a link between a `users` row (role `LEARNER`) and a `learners` row.

## Decision

Add `user_id` to `learners`:

- `user_id INTEGER UNIQUE REFERENCES users(id)` — nullable.
- `NULL` until the learner record is linked to a login account.
- The demo seed links the `learner` login account (`Proposal/Documentation/project_documentation.md:833-836`) to one seeded learner.
- Learner-scoped endpoints resolve `learner_id` from the JWT `sub` (users.id) → `learners.user_id`.

## Consequences

- `docs/wiki/data/learners.md` documents `user_id` and cites this ADR.
- Seed data in `docs/wiki/test/fixtures.md` includes the `learner → learner record` link.
- Every learner-scoped endpoint page in `docs/wiki/api/` resolves the learner via `learners.user_id`.
