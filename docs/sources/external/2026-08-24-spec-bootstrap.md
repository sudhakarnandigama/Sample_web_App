# Greenfield Documentation Bootstrap — workflow archive (2026-08-24)

This file archives the workflow that generated `docs/wiki/`. It is append-only reference material. The canonical operating rules live in `.nexgilerules` at the project root.

## The three non-negotiable properties

Every wiki page MUST satisfy all three.

1. **Concrete** — schemas as schemas, endpoints as endpoints, types as types. No vague verbs ("handles", "manages", "supports") without immediate specifics.
2. **Linkable** — hard page-size cap of 300 lines (200 for catalogs/glossary). Every cross-reference is an exact `page.md#anchor` or `path:line` target. Every cross-referenced section has an explicit `<a id="anchor"></a>` before its heading. No content duplicated across pages.
3. **Verifiable** — every page ends with a `## Verify` block containing one runnable command.

## Forbidden patterns

- "handles / manages / supports / deals with" without specifics
- "see the X docs for more", "in the future", "will support", "is planned to"
- `TBD` / `TODO` / `FIXME` without a `[GAP-XX-NN]` tracking ID
- pages over the line cap; duplicate facts across pages
- API sections without method, path, request schema, response schema, error codes
- field lists without (type, required, constraints, default)
- code blocks without a `// path:line` first-line comment
- references to non-existent paths not tagged `[planned]`
- sloppy GAP IDs — use `[GAP-XX-NN]` (2–8 letter category, 1–3 digit number)
- external URLs not declared in the transcript's `## External URL allowlist`

## Page anatomy — every page MUST have

1. Exactly one `# Title` (H1) outside code fences.
2. `> **Sources** — …` line.
3. `> **Status** — [spec] | [code] | [drift]` line.
4. `> **Page-size budget** — used N / <cap> lines` line.
5. `<a id="..."></a>` immediately before every `##` heading.
6. `<a id="verify"></a>` + `## Verify` block with one runnable command (except `00-INDEX.md`).
7. Within page-size cap.

## Generation order (bottom-up, no upward references)

1. Glossary → 2. Data model → 3. Auth model → 4. Domain events (skip if not event-driven) → 5. API contracts → 6. Service/module map → 7. UI flows → 8. Integrations → 9. Operations → 10. Test strategy.

## Phases

- **Phase 1 — Interview:** ask Q1–Q10, echo a 10-line scope contract, require "confirmed".
- **Phase 2 — Scaffold:** create the directory tree with one starter file per directory (use `write_to_file`, never `mkdir`).
- **Phase 3 — Generate content** layer by layer in the generation order.
- **Phase 4 — Self-check:** run all nine audits below.
- **Phase 5 — Operational files:** `.nexgilerules`, `docs/log.md`, `docs/roadmap.md`, archive this workflow.

## The nine audits

1. **Deeplink audit** — every `path:line` resolves to an existing file or is `[planned]`; every `page.md#anchor` resolves; external URLs are allowlisted.
2. **Page-size audit** — no `docs/wiki/**/*.md` exceeds its cap.
3. **Orphan audit** — every wiki page is linked from at least one other page or from `00-INDEX.md`.
4. **Forbidden-pattern scan** — `TBD|TODO|FIXME|handles|manages|supports|see the [a-z]+ docs|in the future` either fixed or `[GAP-XX-NN]`-tagged.
5. **Provenance audit** — every page has Sources + Status + Page-size budget lines in the first 12 lines.
6. **Page-anatomy audit** — one H1, anchors before H2s, Verify block present.
7. **Operational-files audit** — `.nexgilerules`, `docs/log.md` with `[bootstrap]`, `docs/roadmap.md`, archived workflow, transcript.
8. **Interview-citation audit** — every `interview Q<N>` citation resolves to a `## Q<N>` heading in the transcript.
9. **Microservices structure audit** — conditional; skipped for non-microservices projects.

## Deeplink format rules

- Page anchors: `<a id="kebab-case-slug"></a>` immediately before the heading.
- Inter-page links: relative paths from the linking file.
- Code references: `path:line` or `path:line-line`, always with a range.
- Backticks around paths in prose.
- `[planned]` tag for paths that do not exist yet.
- No bare URLs in wiki — external links live in `sources/external/`.

## Templates

Templates for `00-INDEX.md`, `glossary.md`, `data/<table>.md`, `api/<resource>/<endpoint>.md`, `ui/<route>.md`, `services/<service>/00-overview.md`, `services/00-catalog.md`, `auth/02-scopes.md`, `ops/env-vars.md`, `ops/runbooks/<scenario>.md`, and `test/00-overview.md` are defined in the bootstrap workflow and were applied verbatim when generating this wiki.
