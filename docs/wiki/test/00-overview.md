# Test strategy

> **Sources** — `Proposal/Documentation/project_documentation.md:1255-1297`
> **Status** — [spec]
> **Page-size budget** — used 30 / 200 lines

<a id="layers"></a>
## Layers
| Layer | What it tests | Tool | Command | Speed |
|---|---|---|---|---|
| unit | pure functions (scoring, status derivation, hash verify) | pytest | `pytest backend/tests` `[planned]` | ms |
| integration | one process + real SQLite via FastAPI TestClient | pytest + TestClient | `pytest backend/tests` `[planned]` | seconds |
| e2e | manual demo workflow (§37) | browser + curl | see [ops/runbooks/](../ops/runbooks/) | minutes |

PRD does not specify a test framework; `pytest` (FastAPI default) is used for backend, and the PRD §40 checklist drives e2e.

<a id="fixtures"></a>
## Fixtures
See [fixtures.md](fixtures.md) — canonical seed data referenced from feature pages.

<a id="coverage-gates"></a>
## Coverage gates
- Unit: score/status derivation functions covered.
- Integration: every endpoint in [api/](../api/) has at least one happy + one error case (see each endpoint's §Test plan).
- E2E: every route in [ui/](../ui/) has the happy path from its §Test plan plus PRD §40 checklist.

<a id="verify"></a>
## Verify

```bash
pytest backend/tests -q
```
Expected: all tests pass, 0 failures.
