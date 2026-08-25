# ADR — Admin read endpoints for reports and assignments UI

- **Date:** 2026-08-25
- **Status:** accepted
- **Supersedes:** none

## Context

The reports UI (issue #15, `docs/wiki/ui/reports.md`) must show, per learner: learner, course,
progress, assessment score, and status. `docs/wiki/ui/reports.md` says reports are "computed from
existing list and read data (no separate reports API)", but the API catalog
(`docs/wiki/api/00-overview.md`) had no read endpoint for `course_assignments` or
`assessment_attempts`, so progress and assessment score could not be sourced.

The assignments UI (issue #12) also needs to display existing assignments, which required reading
`course_assignments`.

## Decision

Add two admin-only read endpoints without changing the wiki's "no reports API" rule:

1. `GET /api/assignments` — returns all `course_assignments` joined with learner name and course
   title. Required scope: `assignments:write` (admin-only, reused as the only admin scope on the
   assignments resource).
2. `GET /api/assessments/attempts` — returns all `assessment_attempts` joined with their course id
   and learner name. Required scope: `reports:read` (admin-only).

The reports page aggregates these two reads together with the existing
`GET /api/learners` and `GET /api/courses` list endpoints.

## Consequences

- `docs/wiki/api/assignments/00-overview.md` and `docs/wiki/api/assessments/00-overview.md` do not
  list these read endpoints; this ADR is the authority for the deviation.
- Both endpoints are admin-only; no learner-visible data leak is introduced.
- No dedicated `/api/reports` endpoint is created, preserving the wiki's "no separate reports API"
  rule.
