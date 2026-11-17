---
name: query
description: "Answer a question against the wiki with a cited synthesis. Use when the owner asks something the wiki should be able to answer, or asks what the wiki holds on a topic. Do NOT use to file a new thought (capture) or to process a raw file (ingest)."
user-invocable: true
---

# `query` — answer a question against the wiki

> Four workflows: `ingest`, `capture`, `query`, `lint`. At any moment, you are in exactly one.

1. **Find the material before answering. Search by concept, not just by the query's surface words.**
   - Read `index.md` *by section* (heading outline first, then load the relevant section), and *grep* `glossary.md` for the term. Don't read either whole.
   - Run multi-term / OR-alternation ripgrep across **all** entity folders (`sources/ concepts/ frameworks/ analyses/ cases/ questions/`), not just the obvious one. Search the canonical term **and** synonyms; check the glossary alias for vendor/field/client labels; search filenames (kebab-case), not only body text.
   - Expand from the nearest hit along the graph: follow its `[[links]]`, and pull pages that share a `sources:` entry or a `#domain:` / `#kb:` tag (shared-source and shared-tag are strong relevance signals, often stronger than a direct link).
   - **Absence is a claim, not a default.** Never say "X isn't in the wiki" without searching multiple terms first. If the term is ambiguous or a field/vendor/client label, resolve *every* reading before answering. On a genuine miss, say "I didn't find it under the terms I searched: [list them]", not a flat "it's not here," which hides the vocabulary gap that's often the real cause.
2. Synthesise a clear answer with citations to wiki pages (`[[links]]`).
3. If the question matches an existing page in `questions/`, update that page: set `last-ruminated`, refine the body, adjust `status` if the owner's thinking has actually shifted. **This is rumination. It lives inside query, not as a separate workflow.**
4. If it doesn't match an existing question, ask whether to file it as a new question page or as an analysis. File accordingly.
5. Append to `log.md`:
   ```
   ## [YYYY-MM-DD] query | <question summary>
   Pages consulted: ...
   Output filed: <yes/no — where>
   ```
