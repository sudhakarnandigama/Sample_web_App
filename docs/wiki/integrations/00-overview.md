# Integrations — overview

> **Sources** — interview Q9; `Proposal/Documentation/project_documentation.md:1330-1351`
> **Status** — [spec]
> **Page-size budget** — used 20 / 200 lines

<a id="third-party"></a>
## Third-party dependencies
None. The PRD §42 explicitly excludes payment systems, email notifications, OAuth providers, and message queues. The only cross-process boundary is frontend → backend over [api/00-overview.md](../api/00-overview.md), which is internal.

| Integration | Auth | Request shape | Retry policy | Secrets ref |
|---|---|---|---|---|
| *(none)* | — | — | — | — |

<a id="verify"></a>
## Verify

```bash
grep -cE '^\| `?\*\(none\)\*`?' docs/wiki/integrations/00-overview.md
```
Expected: `1` (single "none" row).
