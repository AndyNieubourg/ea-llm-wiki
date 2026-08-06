---
name: voice-draft
description: Draft prose in the owner's voice against the wiki's voice anchor. Use when writing or rewriting any prose that ships under the owner's name — an entity page, an analyses/ essay, an artifacts/ deliverable, a Confluence page, a briefing memo, an email, an ADR, CV content, an exam answer — and whenever a subagent authors a page on the owner's behalf. Runs after pyramid-structure has settled the argument and hands to voice-edit for the finishing loop. Do NOT use for code, neutral summaries, the top-level infrastructure files, or text meant to sound like someone else.
allowed-tools: Read, Grep, Glob, Write, Edit, AskUserQuestion
user-invocable: true
---

# Voice Draft

Draft prose against [[voice-guide]]. The guide is the **standard**; this skill is the **drafting process** that applies it, and it is the middle step of the shipping sequence.

```
pyramid-structure  →  voice-draft  →  voice-edit  →  traceability-ledger  →  critical-reviewer
  what the             the prose       converge on     (only with a          (only when it
  argument is                          the standard     grounding corpus)     carries an argument)
```

**Dependencies:** hard dependency on `wiki/_resources/voice-guide.md`. Read it at the start of every draft, never from memory: it is the only source of the voice, and this file deliberately does not restate its rules. **Soft** input from `pyramid-structure` (its outline is what you draft against) and from `deep-recon` (its Synthesizer output as raw material).

**This skill does not run the editing passes.** Drafting and editing at once produces prose that is over-polished in places and unstructured in others, because the altitude discipline collapses. Draft, label the result, hand over.

---

## Step 0 — Load the standard and the structure

1. **Read [[voice-guide]] in full.** Its *Voice rules*, *Structure*, *Take intellectual risk in the ideas*, *Red lines* and *What I do not sound like* sections are what you draft toward.
2. **Find the structure.**
   - If `pyramid-structure` ran, read its outline (`<slug>-pyramid-outline.md` in the working directory or scratchpad). **Draft against it, not around it:** the governing thought opens the first screen, each grouping becomes a section, and the summary headings are already written — do not silently reword them into blank labels like "Findings".
   - If no outline exists **and the piece carries an argument, a recommendation, or a scope reading**, stop and run `pyramid-structure` first. Structuring inside a draft is how a deliverable ends up with a spine nobody chose.
   - If the piece has no structure decision to make — an atomic `concepts/` note, a short `sources/` reflection, a two-line email — proceed without an outline.
3. **Name the target and the register** before writing: which entity type or external artifact, which reader, and which of the guide's registers applies.

## Step 1 — Draft

Follow the guide for the voice itself. Four rules belong to *drafting* specifically, because they are cheaper as prevention than as correction:

- **Write the receipt with the claim.** Every claim carries a number, a name, or an open point named in prose. Do not leave a bare adjective for the editing pass to chase; you have the source in front of you now and the editor will not.
- **Never fabricate to fill a gap.** No invented figure, name, source, or quote. Where you do not have the number, name the uncertainty in prose (a dedicated open-points section in a document, in the sentence in an email) rather than decorating the gap.
- **Anchor to a source page.** Source-first (`CLAUDE.md`): reasoning ties back to a `sources/` page. If none exists for the material, flag it rather than invent one.
- **Take the risk in the idea, not the prose.** Plain, controlled sentences carrying a non-obvious stance defended through its trade-off. A draft that is stylistically adventurous and intellectually obvious is the wrong way round.

## Step 2 — Wiki furniture, when the target is a wiki page

- Frontmatter per the entity schema in `CLAUDE.md`: `title`, `type`, `created`, `updated`, `tags`, `sources:` listing **every** raw basename the page reflects, and `relationships:` where a link is load-bearing for `query` or `lint`.
- `[[wikilinks]]` for internal references, and back-links added to the pages you linked.
- Glossary, index and log bookkeeping as the running workflow requires (`ingest` updates all three; `capture` updates only the log).

## Step 3 — Stop, label, hand off

A draft is not a deliverable. When the prose is complete:

1. **Label it "pre-edit draft"** in whatever you show the owner. Presenting an unedited draft as final is the failure this sequence exists to prevent.
2. **Hand to `voice-edit`**, which runs the altitude-ordered passes and stops when the guide's self-check runs clean.
3. **Say what is open** — a claim still missing its receipt, a section you were unsure belonged, a structure point where you departed from the outline and why.

---

## Guardrails

- **The guide is the only source of the voice.** Read it; do not draft from a remembered summary of it, and do not let this file substitute for it.
- **Don't structure inside drafting.** If the argument is not settled, the answer is `pyramid-structure`, not a better opening paragraph.
- **Don't edit inside drafting.** Get the thinking down at the guide's standard, then hand over. Polishing sentence three while paragraph six is unwritten wastes both passes.
- **Never invent.** Flag the gap and keep moving.
- **Scope.** Voiced prose only. Not the top-level infrastructure files (`index.md`, `log.md`, `glossary.md`, `overview.md`, coverage matrices), not verbatim block quotes, not mechanical edits (fix a cell, rename a heading, correct a link).

## Related

- [[voice-guide]] — the standard, built and refreshed by `voice-interview`.
- `pyramid-structure` — runs upstream; its outline is the structure this skill drafts against.
- `voice-edit` — runs downstream; the finishing loop that converges the draft on the guide's self-check.
