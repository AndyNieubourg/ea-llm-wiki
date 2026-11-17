---
name: capture
description: Quick-capture a half-thought into wiki/inbox/ as a dated note. Use when the owner dumps in a thought, meeting reflection or paragraph without a raw source and it should not go through a full ingest. Do NOT use when there is a source document, which is ingest.
user-invocable: true
---

# `capture` — quick note for half-thoughts

> Four workflows: `ingest`, `capture`, `query`, `lint`. At any moment, you are in exactly one.

Low friction by design. Use this for anything the owner dumps in without going through a raw source: meeting reflections, shower ideas, a paragraph to write down before it is forgotten.

1. Create a dated page in `inbox/` (e.g. `2026-05-21-data-mesh-and-eu-ai-act.md`), frontmatter `type: inbox`. Body is whatever the owner wrote.
2. Add tags if obvious.
3. Append a one-line entry to `log.md`.

No glossary update, no index update, no cross-linking. Triage happens during `lint`. Inbox notes may embed images freely; at lint the image earns its place in the promoted page or moves with the note.
