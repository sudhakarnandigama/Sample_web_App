# Runbook: start the FastAPI backend

> **Sources** — `Proposal/Documentation/project_documentation.md:880-947`
> **Status** — [spec]
> **Page-size budget** — used 26 / 200 lines

<a id="when-to-use-this"></a>
## When to use this
Any time the API at `http://localhost:8000` is down or needs a fresh start.

<a id="pre-checks"></a>
## Pre-checks
- [ ] `python --version` returns 3.10+.
- [ ] `backend/venv` exists (created per [`project_documentation.md:880-903`](../../../../Proposal/Documentation/project_documentation.md:880)).

<a id="steps"></a>
## Steps
1. **Activate venv (Windows)** — `backend\venv\Scripts\activate` — expected: prompt shows `(venv)`.
2. **Install deps** — `pip install -r backend/requirements.txt` — expected: `PyJWT` among installed.
3. **Export secret** — `set JWT_SECRET=demo-secret-change-me` — expected: no output.
4. **Start** — `uvicorn app.main:app --reload` (from `backend/`) — expected: `Uvicorn running on http://127.0.0.1:8000`.

<a id="verify"></a>
## Verify recovery

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs
```
Expected: `200`.

<a id="rollback"></a>
## Rollback if step 4 fails
`Ctrl+C` the uvicorn process, fix the import error shown in the traceback, rerun step 4.
