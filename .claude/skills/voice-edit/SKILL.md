---
name: voice-edit
description: Edit prose toward the wiki's voice anchor in altitude-ordered passes, until the voice-guide self-check runs clean. Use when asked to "edit", "revise", "tighten", "polish", "clean up", "proofread" or "improve" prose that ships under the owner's name, AND as the mandatory finishing loop after voice-draft on an analyses/ essay, an artifacts/ deliverable, or a deep-recon output. Do NOT use on inbox/ notes or atomic concepts/ pages (cheap to write by design), on the top-level infrastructure files, on code, or on text meant to sound like someone else.
allowed-tools: Read, Edit, Write, Grep, Glob, AskUserQuestion
user-invocable: true
---

# Voice Edit

Edit a draft toward [[voice-guide]] in altitude-ordered passes, and stop when the guide's self-check runs clean.

**The pairing: [[voice-guide]] is the standard, this skill is the process.** The guide says what good looks like and carries the convergence test — the *Self-check before shipping* block and the degradation table beneath it. Without a runner, that test is a checklist someone is meant to remember. This skill is the runner.

**Dependencies:** hard dependency on `wiki/_resources/voice-guide.md`. The skill is meaningless without it, and it is the only source of the standard: this file carries the *process* and never restates the voice rules. Read the guide at the start of every edit, not from memory.

Two entry points:

1. **As the finishing loop after `voice-draft`.** The sequence is `pyramid-structure` → `voice-draft` → `voice-edit`, and the draft is labelled "pre-edit draft" until these passes have run on it. Converge it on the standard before it ships.
2. **On its own, on prose that already exists.** The owner hands you text and asks to edit, tighten, or clean it up. Same passes, same convergence test.

---

## Scope: what gets the loop, and what does not

The wiki's ethos is cheap to write in. An editing loop on a half-thought is a regression, not a win. **The voice anchor still applies at draft time to every entity page** (see the *Voice anchor* section of `CLAUDE.md`); what this table scopes is the expensive finishing loop, not the anchor.

| Runs the loop | Draft-time anchor only |
|---|---|
| `analyses/` essays | `inbox/` quick captures |
| `artifacts/` — lessons, exercises, project ADRs and deliverables | Atomic `concepts/` notes |
| `deep-recon` deliverables before they land | `sources/` reflections, `questions/`, `cases/` |
| Anything leaving the wiki: a Confluence page, a client deliverable, an email, a briefing memo, CV content, an exam answer | The top-level infrastructure files (`index.md`, `log.md`, `glossary.md`, `overview.md`, coverage matrices) — mechanical catalog prose |
| Prose the owner pastes in and asks to clean up | Mechanical edits: fix a cell, rename a heading, move a section verbatim, correct a link |

A page in the right-hand column that gets promoted (a concept cluster crystallising into an analysis, a case written up for a client) moves to the left-hand column on promotion.

---

## Prime directives

1. **Edit toward the guide, not toward generic "good writing".** Popular editing advice partly cuts against this register; the reconciliation table below is the tie-breaker, and where anything conflicts, the guide wins.
2. **Apply mechanics, propose judgement.** Rule-bound fixes (em dash, passive, filler, number format, sentence-case headings, straight quotes, blacklist vocabulary) you apply directly. Substantive changes (cutting a section, reframing the stance, changing a recommendation, anything that moves meaning) you **propose** with a diff and a one-line reason, and let the owner accept, edit, or reject. Where a substantive change has genuinely distinct options, use `AskUserQuestion`.
3. **Converge to a fixpoint.** Iterate until the self-check runs clean with no open proposals, or until the only items left are real judgement calls for the owner. A pass that changes prose means you re-run the gate.
4. **Never invent to fill a gap.** Editing tightens and corrects; it does not fabricate a number, a name, a source, or a quote. A claim missing its receipt gets its uncertainty named in prose, never decorated with an invented figure.
5. **Preserve the human markers.** Chasing tells flattens the voice. The guide's *Don't over-correct* callout is binding here: leave the non-native-language markers, the occasional mild intensifier, legitimate content triads, and correct EA vocabulary. A tell is a tell only in a cluster.

---

## The three passes, high altitude to low

Three passes, each reading the whole piece at one altitude. This mirrors the recognised editorial stages — structural, stylistic, copy, proofreading — with copy and proofreading folded into one surface pass. Run top-down, so structure is settled before sentences and sentences before commas. Do not jump to comma-hunting: a sentence you polish in pass 3 may not survive pass 1.

### Pass 1 — Content and structure (the widest lens)

Read for meaning, stance, and structure. The guide's *Structure* and *Take intellectual risk in the ideas* sections are the voice-side checklist; **`pyramid-structure` owns the argument side, and this pass leans on it rather than re-deriving a spine.**

- **Is the stance non-obvious?** If a sharp peer would say "well, yes, obviously", push to the reading that makes them sit up. Take a stance, defend it through the trade-off.
- **Does the structure hold?** Two routes, depending on whether the argument was structured deliberately.
  - **An outline exists** (`pyramid-structure` ran, leaving `<slug>-pyramid-outline.md`): read it, and check **conformance**. Does the first screen carry the governing thought as an answer, not a topic? Does each section land the key line the outline assigned it? Where the prose drifted from the tree, is the drift deliberate or accidental? Either way it is a finding: an argument silently rewritten during drafting is exactly what the outline exists to catch.
  - **No outline exists:** apply the pyramid tests rather than inventing a checklist. One governing thought, stated as an answer. Groupings MECE, with no overlap and no gap a sharp reader would flag. Every point passing "so what" going up and "why so" going down. Summary headings stating the insight, never a blank label like "Findings". A deliberate, consistent order inside each grouping. `pyramid-structure`'s *Self-check before handing off* is the full list; do not restate it here.
  - **Escalate rather than rebuild.** This pass moves a misordered section and cuts a paragraph carrying no load. It does **not** rebuild a pyramid inside an editing loop. Where the piece fails at the governing-thought level — no single answer, groupings that overlap, an executive summary mirroring the whole tree — stop and hand back to `pyramid-structure`. Editing prose whose argument is unsound is polishing the wrong artefact.
- **Does load-bearing content sit in the body, not an annex?** Move the spine in; reference annexes by number. Open points belong in prose, not in a vague inline tag.
- **Does every claim carry a number, a name, or an open point named in prose?** Adjectives without numbers are the guide's own red line. Quantify or cut.
- **Do the receipts hold?** Surface test first: does a receipt *appear* for each load-bearing claim. That is a shape test, not a source check. When the prose is grounded in a corpus (`raw/` sources plus the KB), the real question is whether each receipt *traces* to a real source — hand that to the `traceability-ledger` skill, which audits span-level provenance and runs a propose-not-apply loop pulling weak claims back to the evidence. The ledger **subsumes** the surface check where a corpus exists: run the ledger, not both. Skip it when there is no corpus (an email, a post, an exam answer from the owner's own knowledge); there the surface check plus the pass-3 fabrication-shape scan is the whole source check.
- **Kill darlings.** Section by section, paragraph by paragraph: if you cut it, would anything change? If not, cut it. A clever line carrying no load is a darling.
- **Judge the whole artefact, not only the sentences.** A piece can pass every per-line rule and still read as machine-made in aggregate, because the loudest tell is emergent: uniformity, symmetry, completeness out of step with its version. Step back once and ask what a sceptical colleague would flag on sight.

### Pass 2 — Line and flow (the middle lens)

Read for cadence, clarity, and sentence-level voice. Read it as if aloud: the ear catches the metronome, the passive, and the run-on the eye skims. The guide's *Voice rules* and *Generated-prose tells* sections are the checklist.

- **Cadence is mixed, not metronome.** Short sentences carry the claim; longer ones walk the reasoning. If every sentence lands at 15-20 words, break the rhythm. A paragraph at one tempo is a rewrite.
- **Active voice, subject first. Plain copula.** "We assess", not "the analysis is conducted by". "is / are / has", not "serves as / boasts / represents".
- **Name things once, repeat the name verbatim.** Synonym cycling is itself a tell. This check is global, not paragraph-local: it needs the other places the term appears.
- **Trim toward the owner's register.** Generated drafts run longer and softer. Cut filler (just, that, really, so, very, actually), cut the "-ing" padding, cut the thesis restated five ways. Pace counts as much as length: a message taking a paragraph to land is a rewrite even when every sentence is clean.
- **Plain verbs, not consultant abstraction.** "This increases revenue", not "this targets a defined revenue uplift".
- **Mechanical concision tests.** These make "trim" testable. Propose rather than blind-apply: an agent, a passive, or a hedge may be load-bearing.
  - *Be-verb test* — for each *is / are / was / were*, recover the hidden action verb ("is a reflection of" → "reflects").
  - *Nominalisation hunt* — `-tion / -ment / -ity / -ness` nouns bury a verb and its actor ("the implementation of X led to an improvement" → "implementing X improved"). Keep genuine terms of art (medallion, bounded context, federation); revive only the lazy nominalisation of an available verb.
  - *Structural limits* — noun-to-verb gap under roughly 12 words; no more than about three prepositional phrases in a row; one "that" per sentence; every bare *it / this / that / there* resolved to a named antecedent.
  - *Bracket test* — read a clause without its modifiers; if the meaning survives, cut them ("in order to" → "to", "at this point in time" → "now").
  - *Cut target* — a generated draft usually loses 10-30% with no loss of meaning.

### Pass 3 — Copy and surface (the tightest lens)

Read for the rule-bound surface. This is the apostrophes-not-paragraphs pass. The guide's *What I do not sound like* section is the blacklist.

- **No em dashes in prose.** Period, colon, or comma. The spaced em dash is the loudest smoothing flag; clean every one. Structural em dashes in tables, headings, and diagram labels stay.
- **No § (section sign) in prose.** Write "Section 3".
- **Number, unit, and currency formatting** per the owner's locale defaults in `CLAUDE.md`. Every figure consistent between summary and body.
- **Formatting tells.** Sentence-case headings, bold only on what is used, straight quotes, no curly artefacts, no stray emoji, no scare quotes for emphasis, no uniform "Term: definition" bullets, no closing "Conclusion" restating the body.
- **The blacklist scan.** Run the guide's tells list — the trigger vocabulary cluster, phantom-authority attribution, fabricated quotes or statistics, negative parallelism, false ranges, the inspirational pivot, tell-do-tell signposting. **The flag is density, not any single word.**
- **Wiki integrity, when the target is a wiki page.** Every `[[link]]` resolves, `updated:` is bumped, the frontmatter still matches the entity schema, and `index.md` / `glossary.md` bookkeeping reflects what the edit changed.
- **Grammar and spelling** in the register the guide sets. Do not over-polish non-native English into flowery native idiom.

---

## Generic editing advice that does not apply here

Popular editing advice is sound on the universals and wrong where it cuts against this register. Do not import any of it raw.

| Common advice | Here |
|---|---|
| "Vary your words, avoid repetition" | **Overridden.** Name a thing once and repeat the name verbatim. Synonym cycling is itself an LLM tell. |
| "Use strong, colourful verbs" | **Tempered.** The real move is plain verb over weak-verb-plus-adverb *and* over consultant abstraction. No literary colour. |
| "Delete hedges: perhaps, might, could" | **Partly adopted.** Kill hedging without reason. Genuine uncertainty is named in prose, never scrubbed into false confidence. |
| "Make it engaging, no boring passages" | **Out of register.** A narrative standard. These are factual deliverables; a well-grounded aphorism still gets cut when it carries no load. |
| "Gauge which situations benefit from passive voice" | **Tightened.** Passive is the headline tell. An exceptional passive is tolerable; never reach for one because a standard permits it. |
| "Concrete over abstract, one word per meaning" | **Adapted.** Matches *name things once* and *plain verbs*, but the precise EA term wins: concreteness means the named tool, not the simplest word. |
| "Leave days between passes" | **Adapted.** No elapsed time is available, so substitute the discipline: one altitude per pass, and loop to a fixpoint instead of to a calendar. |
| "Cut filler; if it reads fine without it, cut it" | **Adopted wholesale.** |
| "Active voice everywhere" · "Read it aloud" · "Kill your darlings" | **Adopted.** Already the pass-1 and pass-2 tests above. |

---

## The loop

1. **Load the standard.** Read [[voice-guide]] and honour `CLAUDE.md`. Identify the target (wiki page or external deliverable) and the register before touching a word.
2. **Pass 1, then 2, then 3**, each over the whole piece. Apply mechanical fixes inline; collect substantive findings as proposals.
3. **Run the self-check gate** — the guide's *Self-check before shipping* list and its degradation table. Any "no" is a finding for the next iteration.
4. **Resolve proposals.** Present them compactly, grouped, with diffs and one-line reasons. Apply accepted ones. Use `AskUserQuestion` where options genuinely diverge.
5. **Re-run from the lowest pass any change touched.** A pass-1 cut opens a pass-2 cadence problem; a pass-2 rewrite introduces a pass-3 em dash. Iterate until the self-check runs clean and no proposals are open, or the only items left are judgement calls.
6. **Report the changelog**, grouped by pass: what changed and the one-line reason. Flag what is left open — an uncertainty named in prose, a proposal declined, a number still missing its receipt. The diff plus the changelog is the deliverable.

---

## Execution model

Run the loop proportionate to the document. Optimising a one-paragraph email is a regression.

**The passes are a pipeline, not a parallel fan-out.** Each pass mutates what the next reads: a pass-1 cut deletes sentences pass 2 would polish. Never run the three passes concurrently on one document.

**The parallelism is in detection, not mutation:**

- **Pass 1 is global and single-threaded.** Stance, spine, body-versus-annex, kill-darlings are whole-document judgements; partitioning by section defeats them.
- **Pass 2 is mostly section-local.** Cadence, active voice, filler and plain verbs work inside a paragraph, so on a long document the detection fans out per section. Two checks stay global: *name things once* and whole-document cadence.
- **Pass 3 decomposes into independent detectors.** Em dash, number format, formatting tells, blacklist vocabulary, wiki-link integrity and grammar are each a read-only scan over the same text. Run them concurrently, merge findings, apply once.

**Single writer.** Detection fans out; application does not. Read-only detectors (subagents) return structured findings — location, fix, one-line reason. The main loop is the only writer and applies them in one batch. Never let parallel agents write the same file.

**Bundle by size:**

- **Short prose** (an email, a post, a single section, roughly under a page): inline and sequential, no subagents. Spin-up and merge cost exceed the benefit.
- **Long deliverable** (a multi-section analysis or report): pass 1 inline over the whole document; pass 2 and pass 3 detection fanned out per section and per detector; single-writer application; the fixpoint loop re-runs only the sections a change touched.

**Where the grounding audit sits.** Run `traceability-ledger` *after pass 1*, because pass 1 is the only pass that changes *what* is claimed; passes 2 and 3 are meaning-preserving by rule (mechanical applied, substantive proposed). That invariant lets the ledger run **concurrently** with the pass-2 and pass-3 wording edits: it audits meaning, they change only wording, so they do not collide. Re-audit a span only when a later pass changed its assertive strength — a hedge tightened into a firm claim needs a firmer source. The ledger stays propose-not-apply, so it never breaks the single-writer rule.

**Cheap wins, independent of parallelism:** re-scan only changed spans each iteration; batch the rule-bound fixes before the judgement pass, so the expensive reasoning runs on already-clean text; read the guide once at the start, not every iteration.

---

## Guardrails

- **The guide wins every conflict.** When generic editing advice and [[voice-guide]] disagree, follow the guide. The reconciliation table is the tie-breaker.
- **Mechanical applied, substantive proposed.** Never silently change meaning, a recommendation, or a stance. Tightening a sentence is mechanical; cutting the section it sits in is a proposal.
- **No fabrication on edit, and no errors introduced.** Never add a number, name, source, or quote that was not there. Mark the gap, do not fill it.
- **Edit the prose, not the author.** Even on tired-draft cleanup, the fix is mechanical. Judgement does not degrade; do not rewrite the content's ideas under cover of an editing pass.
- **Don't over-correct.** Stop when the piece meets the standard. Further passes that flatten the voice are a regression.
- **Don't edit toward the AI zone.** The counterintuitive one, and the reason the stopping rule exists: detectors flag the *most polished* human writing as machine-made, because high lexical density, very clean syntax, perfectly even paragraphs and a flat tone are exactly the machine signature. Preserve mixed sentence length, verbatim phrase reuse, mild irregularity and voice. A flatter, denser, more perfectly even draft is a *more* machine-looking draft, not a better one. When a tidy-up would smooth the cadence, kill the repetition, or raise the density, stop.

---

## Related

- [[voice-guide]] — the standard this skill edits toward, built and refreshed by `voice-interview`.
- `pyramid-structure` — runs upstream: it settles the governing thought and the decomposition before a word is drafted, and pass 1 checks the prose against its outline instead of re-deriving a spine. Where the argument itself is unsound, this skill hands back rather than rebuilding.
- `voice-draft` — runs immediately upstream: it drafts against [[voice-guide]] and the pyramid outline, then hands here for the finishing loop.
- `traceability-ledger` — the deep source-check this skill calls from pass 1 when a grounding corpus is in play. Prevention lives in [[voice-guide]] (draft with receipts, never fabricate), cheap corpus-free detection lives here, and deep grounding lives there. One concern at three depths.
- `critical-reviewer` — runs downstream on anything carrying an argument or a recommendation: an adversarial pass on the substance, after the prose meets the standard.
