# ADR — Schema field concretizations

- **Date:** 2026-08-24
- **Status:** accepted
- **Supersedes:** none

## Context

The PRD §16 lists table fields by name only, without types, enums, or units (`Proposal/Documentation/project_documentation.md:475-609`). A deeplink-strict wiki cannot leave these vague. This ADR pins every unspecified value so downstream pages have one source of truth.

## Decision

| Field | Decision | Source in PRD |
|---|---|---|
| `courses.duration` | `duration_hours INTEGER NOT NULL CHECK (duration_hours > 0)` — unit = hours | §6 `Duration` (unit unspecified) |
| `courses.status` | enum `ACTIVE` \| `INACTIVE`, default `ACTIVE` | §6 "Activate/deactivate course" |
| `learners.status` | enum `ACTIVE` \| `INACTIVE`, default `ACTIVE` | §7 `Status` (values unspecified) |
| `course_assignments.status` | enum `NOT_STARTED` \| `IN_PROGRESS` \| `COMPLETED`, default `NOT_STARTED` | §8 progress states |
| `course_assignments.progress` | `INTEGER NOT NULL DEFAULT 0 CHECK (progress BETWEEN 0 AND 100)` | §9 percentage + status |
| `assessments.passing_score` | `INTEGER NOT NULL DEFAULT 60 CHECK (0-100)` — pass threshold % | §10 (threshold unspecified) |
| `questions.correct_option` | enum `A` \| `B` \| `C` \| `D` | §16.6 |
| `assessment_attempts.result` | enum `PASS` \| `FAIL` | §10, §26 |
| `certificates.status` | enum `CERTIFIED`, default `CERTIFIED` | §11 "Status: Certified" |
| `certificates.certificate_number` | format `CERT-{YYYY}-{3-digit sequence}`, unique | §11 "CERT-2026-001" |

## Consequences

- Each table page in `docs/wiki/data/` pins the type/enum/default and cites this ADR.
- Field tables in endpoint pages reuse these exact enums — no drift.
