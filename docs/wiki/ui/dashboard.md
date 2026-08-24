# Route: /dashboard — Dashboard

> **Sources** — `Proposal/Documentation/project_documentation.md:127-163`; [api/dashboard/get-dashboard.md](../api/dashboard/get-dashboard.md)
> **Status** — [spec]
> **Page-size budget** — used 39 / 300 lines

<a id="purpose"></a>
## Purpose
Shows summary counts — org-wide for admin, own stats for learner.

<a id="route"></a>
## Route
- Path: `/dashboard`
- File: `frontend/src/app/features/dashboard/dashboard.component.ts` `[planned]`
- Auth required: yes (`dashboard:read`)

<a id="state"></a>
## Local state
| Name | Type | Initial | Updated by |
|---|---|---|---|
| stats | object \| null | null | GET `/api/dashboard` response |

<a id="behavior"></a>
## Behavior
1. On init: GET `/api/dashboard` per [api/dashboard/get-dashboard.md](../api/dashboard/get-dashboard.md).
2. Admin: render `total_learners`, `total_courses`, `active_courses`, `completed_courses`, `certificates`.
3. Learner: render `assigned_courses`, `in_progress`, `completed`, `certificates`.
4. On 401/403: redirect to `/login`.

<a id="components"></a>
## Components used
- `<StatCard>` — `frontend/src/app/shared/**` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | admin logs in | 5 admin metrics visible |
| 2 | learner logs in | 4 learner metrics visible |

<a id="verify"></a>
## Verify

```bash
curl -s http://localhost:8000/api/dashboard -H "Authorization: Bearer $ADMIN_TOKEN"
```
Expected: JSON with `total_learners`, `total_courses`, `active_courses`, `completed_courses`, `certificates`.
