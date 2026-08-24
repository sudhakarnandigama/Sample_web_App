# Route: /learners/new & /learners/:id/edit — Learner form

> **Sources** — `Proposal/Documentation/project_documentation.md:196-225`; [api/learners/create-learner.md](../api/learners/create-learner.md); [api/learners/update-learner.md](../api/learners/update-learner.md)
> **Status** — [spec]
> **Page-size budget** — used 40 / 300 lines

<a id="purpose"></a>
## Purpose
Admin creates or edits a learner.

<a id="route"></a>
## Route
- Path: `/learners/new` (create), `/learners/:id/edit` (edit)
- File: `frontend/src/app/features/learners/learner-form.component.ts` `[planned]`
- Auth required: yes (`learners:write`)

<a id="state"></a>
## Local state
| Name | Type | Initial | Updated by |
|---|---|---|---|
| name | string | "" (edit: loaded) | input change |
| email | string | "" (edit: loaded) | input change |
| department | string | "" (edit: loaded) | input change |
| isSubmitting | boolean | false | submit start/end |
| error | string \| null | null | API error |

<a id="behavior"></a>
## Behavior
1. Edit mode: GET `/api/learners/{id}` to prefill.
2. Validate: `name`, `email`, `department` required; `email` RFC 5322.
3. Create → POST `/api/learners` per [api/learners/create-learner.md](../api/learners/create-learner.md); Edit → PUT per [api/learners/update-learner.md](../api/learners/update-learner.md).
4. On 201/200: navigate `/learners`.
5. On 409 `EMAIL_EXISTS`: show "This email is already registered".

<a id="components"></a>
## Components used
- `<TextField>`, `<Button>` — `frontend/src/app/shared/**` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | valid create | POST 201, navigate /learners |
| 2 | empty name | inline "Name - Required" |
| 3 | duplicate email | banner "already registered" |

<a id="verify"></a>
## Verify

```bash
curl -s -X POST http://localhost:8000/api/learners -H "Authorization: Bearer $ADMIN_TOKEN" -H "Content-Type: application/json" -d '{"name":"Anjali Rao","email":"anjali@example.com","department":"HR"}'
```
Expected: HTTP 201.
