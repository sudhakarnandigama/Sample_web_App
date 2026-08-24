# Scope catalog

> **Sources** — interview Q5; `Proposal/Documentation/project_documentation.md:76-108`; `docs/sources/decisions/2026-08-24-auth-transport.md`
> **Status** — [spec]
> **Page-size budget** — used 34 / 200 lines

Scopes are derived from the JWT `role` claim — the token itself carries `role`, not a scope list. The authorization layer maps `role` → the scope set below. An endpoint requiring a scope the role does not hold → 403.

| Scope | Grants | Held by roles |
|---|---|---|
<a id="dashboard-read"></a>
| `dashboard:read` | Read own dashboard stats | admin, learner |
<a id="courses-read"></a>
| `courses:read` | List + read courses | admin, learner |
<a id="courses-write"></a>
| `courses:write` | Create, update, delete courses | admin |
<a id="learners-read"></a>
| `learners:read` | List + read learners | admin |
<a id="learners-write"></a>
| `learners:write` | Create, update, delete learners | admin |
<a id="assignments-write"></a>
| `assignments:write` | Assign course to a learner | admin |
<a id="progress-write-own"></a>
| `progress:write:own` | Update own assignment progress | learner |
<a id="assessments-read"></a>
| `assessments:read` | Read assessment + questions | admin, learner |
<a id="assessments-submit"></a>
| `assessments:submit` | Submit own assessment | learner |
<a id="certificates-read"></a>
| `certificates:read` | List + read certificates (own for learner) | admin, learner |
<a id="certificates-write"></a>
| `certificates:write` | Generate certificate | admin, learner (own) |
<a id="reports-read"></a>
| `reports:read` | View reports | admin |

<a id="verify"></a>
## Verify

```bash
grep -cE '^\| `[a-z-]+:[a-z:]+` \|' docs/wiki/auth/02-scopes.md
```
Expected: `12` scope rows.
