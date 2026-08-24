# Glossary

> **Sources** — interview Q1–Q10; `Proposal/Documentation/project_documentation.md:1-1433`
> **Status** — [spec]
> **Page-size budget** — used 30 / 200 lines

<a id="project"></a>
**employee-training-demo** — a demo web application; an admin creates/edits courses and learners, and learners track progress, take assessments, and earn certificates. Stack: Angular + FastAPI + SQLite 3 + SQLAlchemy. Architecture: monolith. See: [00-INDEX.md](00-INDEX.md).

<a id="user"></a>
**User** — a login principal stored in `users` with a `role`. Authenticated via JWT bearer. See: [data/users.md](data/users.md).

<a id="admin"></a>
**Admin** — a user whose `role` is `ADMIN`. Creates/edits/deletes courses and learners; assigns courses; views reports. See: [auth/01-roles.md](auth/01-roles.md).

<a id="learner"></a>
**Learner** — a person record in `learners` (optionally linked to a `users` row of role `LEARNER`). Takes courses and assessments, earns certificates. See: [data/learners.md](data/learners.md).

<a id="course"></a>
**Course** — a training unit in `courses` with a title, description, duration, and status. See: [data/courses.md](data/courses.md).

<a id="course-assignment"></a>
**Course assignment** — a row in `course_assignments` linking one course to one learner with progress and status. See: [data/course_assignments.md](data/course_assignments.md).

<a id="progress-status"></a>
**Progress status** — enum `NOT_STARTED` | `IN_PROGRESS` | `COMPLETED`. See: [data/course_assignments.md](data/course_assignments.md#invariants).

<a id="assessment"></a>
**Assessment** — a multiple-choice quiz in `assessments`, containing `questions`, with a passing score. See: [data/assessments.md](data/assessments.md).

<a id="question"></a>
**Question** — a multiple-choice item in `questions` with four options and one correct option. See: [data/questions.md](data/questions.md).

<a id="assessment-attempt"></a>
**Assessment attempt** — one learner's submitted result in `assessment_attempts` with a score and `PASS`/`FAIL`. See: [data/assessment_attempts.md](data/assessment_attempts.md).

<a id="certificate"></a>
**Certificate** — a record in `certificates` issued when a learner completes a course and passes its assessment. See: [data/certificates.md](data/certificates.md).

<a id="scope"></a>
**Scope** — a permission string mapped from the JWT `role` claim. Example: `courses:write`. Catalog: [auth/02-scopes.md](auth/02-scopes.md).

<a id="role"></a>
**Role** — the JWT claim value `ADMIN` | `LEARNER`. Determines which scopes apply. See: [auth/01-roles.md](auth/01-roles.md).

<a id="jwt"></a>
**JWT** — a signed bearer token (HS256) with `sub`, `role`, `exp`. See: [auth/00-overview.md](auth/00-overview.md).

<a id="verify"></a>
## Verify

```bash
wc -l docs/wiki/glossary.md
```
Expected: total ≤ 200 lines (page-size cap).
