---
name: pyramid-structure
description: Structure a deliverable (document or presentation) before drafting a word of it, using Minto's Pyramid Principle and the "so what" test. Use when the owner has a subject, problem, or pile of raw material and needs to decide the governing thought and how to decompose it into a defensible, ordered argument, before writing prose or building slides. Triggers include "help me structure this", "what's the storyline here", "build an outline", "what's my so what", "is this MECE", "how should I break this down", "help me structure this deck/report/proposal", "what's the pyramid here". Runs upstream of drafting and polish — this is the general-purpose structuring step; the prose itself is then drafted against the wiki's voice anchor (voice-guide). Do NOT use for line-level editing, voice/tone, or open-ended brainstorming with no deliverable yet (deep-recon) — those are separate concerns this one feeds into.
allowed-tools: Read, Grep, Glob, Write, Edit, AskUserQuestion
user-invocable: true
---

# Pyramid structure: decide the argument before drafting the prose

This skill is the **structuring step**, not a voice or editing skill. It answers one question: *given a subject and a pile of raw material, what is the one thing I want the reader to take away, and how do the supporting points prove it?* It runs before a word of prose or a single slide gets built, and its output is an outline, not a draft.

**Dependencies:** none required. **Soft** input from `deep-recon` (its Synthesizer output is excellent bottom-up raw material when the topic hasn't been explored yet). **Hands off** to drafting against the wiki's voice anchor (`wiki/_resources/voice-guide.md`), and to whatever editing or grounding workflow the owner uses on top of it. This skill does not draft prose, does not check tone, and does not verify grounding. Where the wiki's own material on structuring exists (pyramid principle, SCQA, MECE pages in `concepts/` or `analyses/`), read it rather than re-deriving the method from memory (see *Wiki cross-references* below).

---

## The method (Minto's Pyramid Principle)

The reason this discipline exists at all: a reader can hold only a handful of ideas at once. Ungrouped points arrive as noise and force the reader to build their own structure, usually not the one intended. A pyramid pre-groups the ideas so the reader receives the governing thought first and descends only as far as they need.

**One governing thought.** Every deliverable has exactly one top-line message — the answer, not the topic. "Should we consolidate the CRM estate" is a topic. "Consolidate onto Platform X within 18 months" is a governing thought. If you can't state it in one sentence, the structuring isn't done yet.

**The opening is SCQA**, and it's what makes the governing thought land instead of arriving out of nowhere:
- **Situation** — the starting point the reader already agrees with, no controversy yet.
- **Complication** — what changed, or the tension that just got introduced (a deadline, a cost, a new fact).
- **Question** — the question the complication raises, given the situation. Often implicit, but always answerable in one line.
- **Answer** — the governing thought. This is what the rest of the pyramid supports.

This is not a new template: it's the reasoning engine already implicit in the classic EA deliverable spine — "Architectural Question, then scenarios" is Question-then-groupings, and "Recommendation ... due to ..." is the Answer. This skill is what decides the Question and the Answer before that spine gets filled in.

**Vertical logic — every level answers "so what" going up, "why so" going down.** Each point below the governing thought must make the reader think "so what?" and get the level above as the reply. Read the same point downward and it must survive "why is that true — how do you know?", answered by the level below it. A point that fails either test doesn't belong at that level: too thin to earn its place above it, or unsupported below it.

Run the "so what" the way the audience asks it, not the way the writer hears it: a point that states a **feature** ("runs on the new engine") is not the same as one that states the **benefit** ("cuts month-end close from three days to one"). If a point can't be translated into something the reader would act differently on, cut it or restate it as a benefit before it earns a place in the tree.

**Never an intellectually blank heading.** The single most common failure at any level: a summary box that names a *category* instead of stating the *insight* — "Findings," "Conclusions," "Issues" have no scanning value. State the actual conclusion or effect the group of points adds up to. If a heading could sit unchanged over a completely different set of supporting points, it's blank.

**Horizontal logic — MECE, and one of two kinds of grouping.** Points in the same grouping must be logically the same *kind* of idea, with no overlap and no gap a sharp reader would notice.
- **Deductive** (an argument): step A leads to step B leads to step C, summarised with "therefore" — rigorous, but harder to read because each step depends on the one before.
- **Inductive** (a grouping): same class of thing — three risks, four regions, two options — easier to read, and the more common shape in business and technical writing. The trap is listing the members without saying what they add up to: not "France, Germany, and the UK are all missing the deadline" but "European operations miss the deadline." The induced sentence *is* the group's key-line point, not a label for it.

**Prefer inductive at the key-line level when you have a genuine choice.** The reader gets the group's label immediately rather than having to hold each step to reach the last. Reach for deductive only when the content really is a chain of reasoning, not a set of like things.

Don't force a clean three when reality gives you two or five. A manufactured triad is decoration, the same failure mode as invented percentages and green-tick-everywhere tables: MECE is a real constraint on the *content*, not a target group size.

**Order within a grouping** — pick one, name which, and don't mix them inside one grouping:
- **Deductive** — the logical chain itself dictates the order.
- **Chronological / process** — time order, cause then effect, steps in a sequence.
- **Structural** — parts of a whole: geography, org structure, layers of an architecture.
- **Comparative** — ranked by importance, size, or priority.

The reader's culture can flip which end leads without changing the order type itself — see selector 4 in Step 0.

**The process writes the structure.** A deliverable that presents a solution is often the record of the process that produced it, so a sound solving method hands you the section list for free: a five-question sequential analysis (is there a problem? where? why? what could we do? what should we do?) maps straight onto introduction / causes / solution; a build-and-evaluate research method's own activities (problem → objectives → design → demonstration → evaluation → communication) double as the chapter outline; an architecture method's driver → design → documentation → evaluation cascade becomes exec summary → drivers → views → decisions → roadmap. Two corrections keep this honest: **present the rational reconstruction, never the chronology** — the pyramid is discovered bottom-up and presented top-down, cleaned of the backtracking that actually happened; and **the decision, not the document, is the unit of work** — a document frozen up front while a live decision stream keeps moving is a failure mode (the "Waterfall Wasteland"), not a feature. Write the section when the process has actually produced something to record.

---

## Building the pyramid

### Step 0 — Intake

Before building anything, establish the deliverable shape (document, deck, memo, email) and what raw material exists — a brain dump typed into chat, a `deep-recon` output, specific wiki pages, an existing rough draft, or genuinely nothing yet. Then answer five questions that select the genre; don't default to whatever template was used last time:

1. **What should the reader do after reading?** Decide, understand, audit, verify-and-build-on, or act on one thing. This alone mostly fixes the genre — see the catalogue in Step 4.
2. **What does the reader already know?** The introduction *reminds*, it never *informs* — match the SCQA's Situation to where the reader actually stands, not where you'd like them to be.
3. **How many audiences must this one deliverable serve?** A single-community piece optimises for that community's vocabulary. A boundary object (architects, business stakeholders, and auditors reading the same text) is a harder design problem, solved by layering: a headline and an anchor diagram for the fast pass, body prose for the practitioner, a sidebar for the specialist — never duplicating the content per audience.
4. **Which persuasion culture reads it?** Principles-first audiences want the theory or method built out before the conclusion; applications-first audiences want the answer or a concrete case up front. This can flip which end of the pyramid leads, on top of — not instead of — Minto's four logical orders above.
5. **Which register governs?** Consulting register optimises for the decision (answer-first, 80/20 depth). Academic register optimises for verification (a colleague must be able to replicate the study from the report alone). Pick one before drafting; don't blend them.

If the deliverable is a deck, also settle the **artifact-type fork** now, not later — it changes everything downstream (see Step 4). Use `AskUserQuestion` for anything still unclear; don't guess the audience, the ask, or the culture in the room.

### Step 1 — Pick top-down or bottom-up
- **Top-down**, if the governing thought is already known (or you have a strong hypothesis): state it, then work down to find what supports it.
- **Bottom-up**, if only scattered points or data exist: list them, group them, and let the governing thought emerge from the groups.
If it's not clear which applies, ask — don't force top-down on a genuinely unexplored topic (that's premature-conclusion, not structuring), and don't force bottom-up busywork when the answer is already obvious.

### Step 2a — Top-down build
1. Draft the SCQA: Situation, Complication, Question.
2. Draft the Answer (the governing thought) as a hypothesis.
3. Decompose it into 2-4 key-line points, each either a deductive step or an inductive grouping member.
4. Test every key-line point upward (so what — as a benefit, not just a fact?) and downward (why so / how do you know?).
5. Recurse one or two more levels, down to the level where the point is a raw fact or a citable number.

### Step 2b — Bottom-up build
1. Dump every point onto the table, one per line — from the raw material identified in Step 0.
2. Group points that are the same kind of idea.
3. For each group, ask: what does this group say, taken together? That induced sentence is the group's key-line point — not a list header, and never an intellectually blank one.
4. Roll the key-line points up one more level: what single sentence do they collectively support? That's the governing thought.
5. Back-check against SCQA: does this governing thought actually answer the Question raised by the Situation and Complication? If it doesn't, the grouping is wrong — regroup, don't force-fit the SCQA to match a shaky answer.

**If the grouping won't converge** — the points don't cluster and no governing thought emerges — the problem itself likely isn't defined precisely enough yet. Fall back to the heavier problem-definition sequence: state the **Starting Point** (context as it stands), the **Disturbing Event** (what changed or threatens), **R1** (the current, undesired result), **R2** (the desired result), then the **Question** that R1-vs-R2 raises. This converts directly into the SCQA (Starting Point → Situation; Disturbing Event + R1 → Complication; the R1/R2 gap → Question) and is Minto's own escalation for genuinely problem-oriented, multi-day, often multi-author documents. Don't reach for it on a short memo where plain SCQA already works.

### Step 3 — MECE and order pass
Run the MECE check on every grouping in the tree, not just the top one. For each grouping, name which order it uses (deductive / chronological / structural / comparative) and why that order, not another.

### Step 4 — Translate to the deliverable shape

**Document — pick the genre, don't default to one.** The governing thought and key line dress differently depending on what Step 0 selected:

| Genre | Structure | Signature failure |
|---|---|---|
| Decision memo / exec summary | SCQA intro → answer → key line → next steps; 1-3 pages, answer in the first paragraph | Burying the answer; blank headings |
| Consulting report | Full pyramid on the page: hierarchical headings, substance-carrying transitions, "Next Steps" not "Conclusion" | Anxious parade of knowledge (transcribing the reference pile to look thorough) |
| ADR | Title → Status → Context → Criteria → Options (pros *and* cons) → Decision → Implications (negatives mandatory) → Consultation | Advocacy dressed as a record; retrospective rationalisation |
| Academic report / thesis | Intro & background → theory, method, results → related work, conclusion; abstract and conclusion stand alone | Writing to impress; hiding unfavourable results |
| Solution architecture doc (SAD) | Exec summary → drivers → quality-attribute scenarios → views → decisions → risk and cost → roadmap | Frozen up front while the decision stream moves on ("Waterfall Wasteland") |
| Email / short message | Subject line as headline; 3-4 points, ordered; one ask | "Call me" with no content; five asks in one mail |

Whichever genre, the shared mechanics hold: governing thought → executive summary (mirrors the top two levels only) → section headings = key-line points → each section opens with the "so what" sentence for that section → body carries the supporting data, attributed to its source.

**Deck — which artifact: slide doc, live deck, or both?** Decide this before slide 1. "Presentation" hides two different artifacts in one file format, and the unchosen middle — a **slideument**, too dense to project and too thin to read alone — serves neither. Ask: **will this file circulate without you present?**
- **Yes** (forwarded, archived, read by people who were never in the room) → it's a **slide doc**. Treat it as a document in landscape: everything in the Document table above applies, plus two slide-specific rules — every title is a statement, never a caption, and the page (not the paragraph) is now the unit of grouping.
- **No** (you're always in the room) → it's a **live deck**. The speaker carries the message; slides stay sparse and must pass the **five-second test** — show a slide for five seconds and ask what people saw. "Three yellow boxes" means the slide has no message.
- **Both** → split the artifact. Either produce two files (a sparse projected deck plus a dense leave-behind), or storyboard one live deck and carry the read-alone prose in the speaker notes. Averaging the two densities onto one slide never works.

**Live deck — one story, shaped by purpose.** The live deck's invariant is a connected storyline — "twenty slides, one story," not twenty single-slide resets. What changes is which story and which landing devices earn a slot:

| Purpose | Artifact lean | Story shape | Landing device |
|---|---|---|---|
| Decision / steerco | Slide doc (it becomes the record) | Answer first → key line → next steps | Prewiring — nothing in the room is new |
| Governance review (ARB) | Slide-doc pack | Context → drivers → options → recommendation → risks → cost → ask | Pre-agreed decision criteria |
| Business case / pitch | Live, with a leave-behind | Story Mountain: situation → cost of inaction → resolution | SUCCESs; a So What Positioning Statement |
| Teaching / training | Both; split the artifact | A ramp, never a cliff | Build slides; consistent level of detail |
| Conference / inspiration | Pure live | Show the assembled outcome, never the brick list | Pathos; props and demonstrations |
| Academic defence | Live, examiner has the report | Structure decided before content, message over entertainment | Openness about weaknesses |
| Workshop / working session | Live frames, artifacts emerge in-session | One diagram, one story per frame | Replay; props; the group draws |

**Live and slide-doc mechanics that hold across purposes:**
- **Text slides vs. exhibit slides**, roughly 90/10. Text slides that remain get one idea, a statement not a caption ("Sales outlook is favorable," never "Sales outlook" — and never uniform-caption furniture, a classic template-deck tell), ~6 lines / ~30 words, revealed as builds where the grouping matters.
- **One message per chart, and the title states it.** A chart answers one of five questions (what are the elements / how do amounts compare / what changed / how are items distributed / how do items co-relate). State the chart's **answer as its title** ("Western Region accounts for almost half the sales," not "Share of sales by region") — the pyramid principle applied to one chart. Keep the visual simple, cite the source. A waterfall chart is the standard way to show a flow from one number to another; reach for it whenever a key-line point is "how we get from A to B."
- **Storyboard before you build.** Write the introduction in full first, confirming the Question is the one the audience actually has. On a blank storyboard, write across the top of each slide the point it illustrates (introduction, then key line, one level below). Rough out the visual for each, script the words that carry the set as a story, then produce and rehearse. The governing thought, not "Agenda," is the title slide.
- **Prewire before the room.** A good presentation contains nothing new for its audience: walk every key stakeholder through the findings privately beforehand. This is not only politics — a stakeholder can surface a fact that changes the recommendation, which sends the structure back to Step 3, not just the delivery. Freeze the deck roughly 24 hours out and spend the rest rehearsing; effort past that point belongs in prewiring, not more polish. Treat an unprewired deck as a structure that hasn't been stress-tested yet.
- **Order for the culture in the room.** Selector 4 from Step 0 applies with more force to a live deck than to a document, because the room reacts in real time: an applications-first audience wants the case before the theory; a principles-first audience reads a case-first opening as shallow.
- **When slides are the wrong tool.** A single vivid prop, drawn diagram, or told demonstration can move a room further than twenty slides, especially where the audience disagrees on facts rather than lacking them. Before opening the slide tool, ask whether one object or one story would do more.

### Step 5 — Output and handoff
Write the outline to a scratch file, not a wiki KB page — this is a working structure, not a source, concept, or analysis in its own right. Suggested shape: `<slug>-pyramid-outline.md` in the working directory (or the session scratchpad), containing the SCQA, the full tree with the so-what/why-so check marked at each level, the order type named per grouping, and which genre (Step 4) was selected and why.

Close with an explicit handoff line naming what comes next:
- Business/EA deliverable → draft against the wiki's voice anchor (`wiki/_resources/voice-guide.md`), then the owner's editing pass. Point out which key-line group maps to which scenario in the EA spine.
- Academic deliverable (thesis, paper, exam) → the governing thought becomes the thesis claim and the SCQA its establishing move; apply the owner's academic-register workflow if one is installed.
- Claims will need grounding once drafted → name them in the outline so the drafting pass carries sources with them.

---

## Worked example (EA register, for calibration)

- **Situation:** The client runs three parallel CRM platforms.
- **Complication:** Two reach end of life within 18 months, and licence cost has doubled this year.
- **Question:** Should the client consolidate, and onto which platform?
- **Answer (governing thought):** Consolidate onto Platform X within 18 months. It is the only option that clears the licence deadline without a new integration layer.
- **Key line (inductive, comparative order — strongest reason first):**
  - Platform X already holds 70% of active customer records, so migration touches the fewest records.
  - Platform X's licence is already committed group-wide, so no new procurement cycle is needed.
  - The other two platforms fail the licence deadline outright — ruled out, not merely disfavoured.
- **So-what check:** each bullet, read alone, answers "why Platform X" — passes.
- **Why-so check:** "70% of active records" and "licence already committed" are both citable facts, not assertions — passes.
- **MECE check:** three reasons, no overlap (records / licence / deadline are distinct dimensions), nothing load-bearing left out.

This maps directly onto the classic EA deliverable spine: the Question above is the Architectural Question, the key line is the scenarios (with the other two carrying their own Exclusions), and the Answer is the Recommendation with its rationale.

---

## Boundary: structure vs. landing

This skill decides the logic — the governing thought, the groupings, the order, the genre. It does not cover the separate craft of making a well-structured argument *land* emotionally: storytelling, props, physical demonstrations, or framing a message around the audience's values rather than the bare facts. That material is real and is a complement, not a substitute: a perfectly MECE pyramid can still fail to move an audience that facts alone don't reach, which is exactly the "when slides are the wrong tool" test in Step 4. Structure first with this skill, then reach for that craft separately if the deliverable needs to persuade, not just inform.

---

## Self-check before handing off

Any "no" means the structure isn't ready to draft from yet.

1. Can the governing thought be stated in one sentence, and is it an answer, not a topic?
2. Was the genre chosen deliberately using the five selectors in Step 0 (goal, reader's prior knowledge, audience count, culture, register), not defaulted to whatever template was used last time?
3. Does the Answer actually resolve the Question the Situation and Complication raise?
4. Does every point pass "so what" going up (as a benefit the reader would act on, not just a fact) and "why so / how do you know" going down?
5. Does every summary heading state the actual insight — never an intellectually blank label like "Findings" or "Issues"?
6. Is every grouping MECE — no overlap, no gap a sharp reader would flag?
7. Is each grouping consistently deductive or consistently inductive, not a mix — and inductive wherever there was a genuine choice?
8. Is the order within each grouping named, and does it fit both the content and the reader's persuasion culture?
9. If it's a deck: was the artifact type (slide doc / live deck / split) decided before slide 1, instead of drifting into the unchosen middle?
10. If it's a live deck: does every slide pass the five-second test — one message, not an inventory of boxes — and does every chart's title state its one message?
11. If it's a deck: has it been prewired, or is prewiring explicitly planned before the room?
12. If it's a document: does the executive summary mirror only the top two levels, not the whole tree?
13. Is the group size honest — a real two or a real five left alone, not padded or trimmed to a decorative three?
14. Is the handoff line present, naming which skill drafts next?

---

## Wiki cross-references

If the owner's vault has ingested the source material behind this method, read those pages rather than re-deriving the theory from scratch, and cite them in the outline's handoff line. Search `wiki/concepts/` and `wiki/analyses/` for pages on: the pyramid principle, SCQA, MECE, the "so what" test, Minto's problem-definition framework (Starting Point / Disturbing Event / R1 / R2 / Question), hypothesis-driven problem solving, and document/presentation design by goal and audience.

This is a soft, vault-local enrichment. The skill must not hard-depend on any of these pages existing — a fresh wiki has none of them; check for a page before citing it, and fall back to the self-contained explanation above if it's missing.

---

## Companion routing

| When | Skill |
|---|---|
| Topic hasn't been explored yet — no raw material to structure | `deep-recon` first; bring its Synthesizer output back here as bottom-up material |
| The problem itself isn't solved yet — no hypothesis, no discriminating facts, not just unstructured | Do the analysis first (Minto's problem-definition + logic-tree structuring, or hypothesis-driven problem solving); this skill structures an existing answer, it doesn't find one |
| Structure is settled, now write the prose | Draft against the wiki's voice anchor (`wiki/_resources/voice-guide.md`), then the owner's editing pass |
| Deliverable is a thesis, paper, or exam essay | The owner's academic-register workflow, if one is installed; the governing thought becomes the thesis claim |
| Deliverable ships to Confluence | The owner's Confluence-publishing skill, if installed (see the "Publishing to Confluence" note in `CLAUDE.md`), after drafting |
| Need the full genre catalogue or story-shape detail beyond what's condensed here | The owner's ingested design/structuring pages, if any (see *Wiki cross-references* above) |
| The structure is sound but needs to land emotionally, not just logically | See *Boundary: structure vs. landing* above — a separate concern, not this skill's job |
