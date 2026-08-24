# UI flows — overview

> **Sources** — interview Q4; `Proposal/Documentation/project_documentation.md:1020-1095`
> **Status** — [spec]
> **Page-size budget** — used 40 / 200 lines

<a id="routing-model"></a>
## Routing model
Angular standalone routes in `frontend/src/app/app.routes.ts` `[planned]`. All routes except `/login` require auth via `frontend/src/app/core/guards/auth.guard.ts` `[planned]`. Nav items differ by role — admin nav per [`project_documentation.md:1043-1056`](../../../Proposal/Documentation/project_documentation.md:1043), learner nav per [`project_documentation.md:1060-1070`](../../../Proposal/Documentation/project_documentation.md:1060).

<a id="layout"></a>
## Layout shell
`navbar` + `sidebar` from [architecture/01-modules.md](../architecture/01-modules.md#frontend-modules). Base URL for API: `http://localhost:8000/api` via `frontend/src/environments/environment.ts` `[planned]`.

<a id="routes"></a>
## Routes

| Path | Page | File |
|---|---|---|
| `/login` | Login | [login.md](login.md) |
| `/dashboard` | Dashboard | [dashboard.md](dashboard.md) |
| `/courses` | Courses list | [courses.md](courses.md) |
| `/courses/:id` | Course details | [course-details.md](course-details.md) |
| `/courses/new`, `/courses/:id/edit` | Course form (add/edit) | [course-form.md](course-form.md) |
| `/learners` | Learners list | [learners.md](learners.md) |
| `/learners/new`, `/learners/:id/edit` | Learner form (add/edit) | [learner-form.md](learner-form.md) |
| `/assignments` | Course assignments | [assignments.md](assignments.md) |
| `/assessment/:courseId` | Take assessment | [assessment.md](assessment.md) |
| `/assessment/result` | Assessment result | [assessment-result.md](assessment-result.md) |
| `/certificates` | Certificates | [certificates.md](certificates.md) |
| `/reports` | Reports | [reports.md](reports.md) |

<a id="design"></a>
## Design
Simple, clean, responsive. Use standard tables, cards, forms, buttons, modals, progress bars, status badges. No unnecessary animations.

<a id="verify"></a>
## Verify

```bash
grep -cE '^\| `/' docs/wiki/ui/00-overview.md
```
Expected: `12` route rows.
