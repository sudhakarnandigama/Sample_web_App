# Route: /learners — Learners list

> **Sources** — `Proposal/Documentation/project_documentation.md:196-225`; [api/learners/list-learners.md](../api/learners/list-learners.md)
> **Status** — [spec]
> **Page-size budget** — used 39 / 300 lines

<a id="purpose"></a>
## Purpose
Admin lists all learners with add/edit/delete actions.

<a id="route"></a>
## Route
- Path: `/learners`
- File: `frontend/src/app/features/learners/learners.component.ts` `[planned]`
- Auth required: yes (`learners:read`; admin-only)

<a id="state"></a>
## Local state
| Name | Type | Initial | Updated by |
|---|---|---|---|
| learners | array | [] | GET `/api/learners` response |

<a id="behavior"></a>
## Behavior
1. On init: GET `/api/learners` per [api/learners/list-learners.md](../api/learners/list-learners.md).
2. "Add" → `/learners/new`.
3. Row edit → `/learners/:id/edit`.
4. Delete → confirmation → DELETE `/api/learners/{id}` per [api/learners/delete-learner.md](../api/learners/delete-learner.md).

<a id="components"></a>
## Components used
- `<DataTable>`, `<StatusBadge>`, `<ConfirmationDialog>` — `frontend/src/app/shared/**` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | admin opens /learners | list loads |
| 2 | learner role tries /learners | guard blocks, redirect |

<a id="verify"></a>
## Verify

```bash
curl -s http://localhost:8000/api/learners -H "Authorization: Bearer $ADMIN_TOKEN"
```
Expected: HTTP 200, JSON array rendered by the page.
