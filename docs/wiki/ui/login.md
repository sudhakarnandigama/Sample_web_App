# Route: /login — Login

> **Sources** — `Proposal/Documentation/project_documentation.md:113-125,1020-1024`; [api/auth/login.md](../api/auth/login.md)
> **Status** — [spec]
> **Page-size budget** — used 40 / 300 lines

<a id="purpose"></a>
## Purpose
User authenticates with username + password, then is routed by role.

<a id="route"></a>
## Route
- Path: `/login`
- File: `frontend/src/app/features/login/login.component.ts` `[planned]`
- Auth required: no (public)

<a id="state"></a>
## Local state
| Name | Type | Initial | Updated by |
|---|---|---|---|
| username | string | "" | input change |
| password | string | "" | input change |
| isSubmitting | boolean | false | submit start/end |
| error | string \| null | null | API error |

<a id="behavior"></a>
## Behavior
1. Submit → POST `/api/auth/login` per [api/auth/login.md](../api/auth/login.md).
2. On 200: store `access_token` via `auth.service.ts`; `router.navigate(['/dashboard'])`.
3. On 401 `INVALID_CREDENTIALS`: show "Invalid username or password".
4. On 400 `MISSING_FIELDS`: show "Username and password are required".

<a id="components"></a>
## Components used
- `<TextField>`, `<Button>`, `<ErrorBanner>` — `frontend/src/app/shared/**` `[planned]`

<a id="test-plan"></a>
## Test plan
| # | Case | Expected |
|---|---|---|
| 1 | admin / admin123 | redirect to /dashboard |
| 2 | learner / learner123 | redirect to /dashboard |
| 3 | wrong password | inline error shown |

<a id="verify"></a>
## Verify

```bash
ng serve --open
```
Expected: open `http://localhost:4200/login`; login as admin lands on `/dashboard`.
