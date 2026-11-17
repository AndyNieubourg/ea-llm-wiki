---
name: ingest
description: "Process a source document into the wiki, source-first. Use when the owner asks to ingest a document, book, deck or web page from raw/ or attached in chat. Do NOT use for a half-thought with no source, which is capture."
user-invocable: true
---

# `ingest` — process a source from `raw/`

> Four workflows: `ingest`, `capture`, `query`, `lint`. At any moment, you are in exactly one.

Heavy by design. Cross-linking is the wiki's whole point; the steps below each pay rent.

**Source-first principle.** Every raw file gets a `sources/` page that reflects it. That page is the canonical reflection of the raw artifact and the auditable bridge between `raw/` and the rest of the wiki. Concepts, frameworks, cases, and questions are *derived* from the source page after the reflection exists, not extracted directly to `concepts/` while skipping the source. This applies even when the raw file is thin (a short deck, a single article); a thin source page is fine, a missing one is not.

1. Read the source. For long sources (books, course modules), confirm whether to ingest in full now or chunk by section across sessions. For a web page, run `defuddle` first if it is installed.
2. Briefly discuss takeaways. Ask 1–3 clarifying questions only if the material is dense or ambiguous.
3. Create or update the parent page in `sources/` (per the source-first principle above). For long sources, also create atomic notes in `concepts/` per chapter or per distinct idea, each linked back to the source. List every raw basename the page reflects in its `sources:` frontmatter (the completeness rule in `CLAUDE.md`). Extract diagrams per `.claude/rules/diagrams.md` ("During the workflows").
4. Identify which existing pages are affected. Update them. Add back-links.
5. Create new entity pages (concept, framework, case, question) as the material warrants. Don't force-fit into existing categories.
6. Update `glossary.md` with new or refined terms; flag conflicts with existing entries. Record vendor/practitioner synonyms as aliases (the alias bridge in `CLAUDE.md`).
7. Update `index.md`.
8. Run `python3 scripts/preflight.py` and fix what it reports before committing.
9. Append to `log.md`:
   ```
   ## [YYYY-MM-DD] ingest | <source title>
   Pages created: ...
   Pages updated: ...
   Key additions: ...
   ```

`overview.md` is **not** updated inline. That happens during `lint`, to avoid recency bias and overview thrashing.

A single ingest may touch 5–15 pages. That is expected.
