# Runbook: start the Angular frontend

> **Sources** — `Proposal/Documentation/project_documentation.md:950-974`
> **Status** — [spec]
> **Page-size budget** — used 25 / 200 lines

<a id="when-to-use-this"></a>
## When to use this
Any time the UI at `http://localhost:4200` is down.

<a id="pre-checks"></a>
## Pre-checks
- [ ] `node --version` returns 18+.
- [ ] `npm --version` returns a version.

<a id="steps"></a>
## Steps
1. **Install** — `npm install` (from `frontend/`) — expected: `node_modules` populated.
2. **Configure API URL** — set `apiUrl` in `frontend/src/environments/environment.ts` `[planned]` to `http://localhost:8000/api`.
3. **Start** — `ng serve` (from `frontend/`) — expected: `Angular Live Development Server is listening on localhost:4200`.

<a id="verify"></a>
## Verify recovery

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:4200
```
Expected: `200`.

<a id="rollback"></a>
## Rollback if step 3 fails
`Ctrl+C`, inspect the compilation error, fix, rerun step 3.
