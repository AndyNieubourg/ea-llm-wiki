---
title: Voice Guide (template)
type: reference
created: 2026-06-05
updated: 2026-06-05
tags: [voice, style, recon-anchor, lint-reference, template]
---

Style anchor for any output that takes the owner's voice: analyses, recon documents, synthesis sections, anything that lands in this wiki as voiced prose. Used by `deep-recon` and any workflow that drafts voiced output.

> [!important] This is a template — personalise it with `/voice-interview`
> The sections below split into two kinds of content:
> - **Generic EA-writing defaults** (kept as-is): principles that hold for almost any enterprise architect's deliverables — numbers carry the argument, name things, no em dashes / AI tells, active voice, business-deliverable structure, take risk in the ideas not the prose. Use these from day one.
> - **`{{PLACEHOLDERS}}` and "_measure this_" notes**: the parts that are personal — the measured stylometric fingerprint, hated words, examiner/reviewer feedback, language mix. These are empty until you run the `voice-interview` skill, which reads your real deliverables and folds the findings in here. **Do not invent a fingerprint.** A rule earns its place only when backed by a real sample or an explicit interview answer.

The fingerprint should be measured from the owner's **real, genuinely-authored** deliverables — not from LLM-generated or LLM-smoothed drafts, and **not** from this wiki's own `analyses/` pages (they are Claude-drafted and drift essayistic; borrow their EA vocabulary, never their cadence).

---

## Who I write as, and for whom

> _Filled at init / voice-interview._

I write as {{ROLE}} — {{BACKGROUND: years, sector, region}}. Locale defaults: {{LOCALE: e.g. EU / EUR / metric}}. Deliverables are drafted in {{LANGUAGES}}; the wiki is English-only, so non-English-origin material is translated on the way in. The structural moves survive translation; the language doesn't.

I write for three readers: future-me re-reading later; a downstream consumer who must act ({{NAME THE ROLES: e.g. CIO, CTO, governance council, board, delivery team, evaluator}}); a sharp practitioner peer who can take a hit. Not for an academic committee. Not for executives who need slogans.

---

## Stylometric fingerprint

> _Measure this with `voice-interview`. The bullets below are the dimensions to fill, with generic EA-writing defaults as a starting hypothesis only — replace each with a measured value and a real sample._

- **Cadence: {{median sentence length}}, mixed length.** Default hypothesis for EA deliverables: median 15–19 words, with ~15–25% short sentences (≤8 words) carrying the claims and a quarter running past 25 to walk a process through. The short sentence states the position; the longer ones do the reasoning. _(measure)_
- **Coordinate with "and", not subordination.** Stack clauses with "and"; don't comma-stack noun phrases into one dense appositive. _(confirm against samples)_
- **First person is register-dependent.** Sparse in architecture/design deliverables (default to impersonal or named-actor subjects; reserve "we" for the moment of commitment); rises legitimately in persuasive/advisory pieces. Match the register, don't force either pole. _(measure the per-register rate)_
- **Signature motivation connector: {{CONNECTOR}}.** Many architects lean on one ("due to", "because", "given that") to carry reasoning in recommendations and exclusions. Identify the owner's. _(measure)_
- **Lexical diversity / repetition.** Named things repeat verbatim by design. Name the tool once and keep the name; never elegant-vary "the solution / the system / the platform" across a page. _(measure MATTR if useful)_
- **Plain copula.** is / are / has, not "serves as / boasts / represents".

---

## Voice rules (generic EA defaults — keep these)

- **Trim LLM verbosity.** Generated drafts run longer and softer than an architect would write; the default move is to cut back toward the owner's register. Prefer bullets and tables where they carry the point; let a paragraph stand when the argument needs one. The aim is the owner's actual length, not the shortest possible text.
- **No em dashes in prose. Hard rule.** Period, colon, or comma. The dash is a classic LLM tell, so the ban doubles as a smoothing detector. (Structural em dashes in tables, headings, and diagram labels are house style and stay.)
- **Active voice, subject first.** *"We assess..."*, not *"the analysis is conducted by..."*. Passive is the headline autopilot tell and weakens the trusted-advisor stance. An exceptional passive is tolerable; the rule still holds.
- **Plain verbs over consultant abstraction.** *"This increases revenue"*, not *"this targets a defined revenue uplift"*.
- **Numbers carry the argument.** Not "significant risk": the exposure in figures. Not "high cost": the day-rate × days. Use the owner's locale number formatting consistently ({{NUMBER FORMAT}}). The reader can rebuild the spreadsheet from the prose.
- **Calibrated bluntness with receipts.** Quote the source, cite the slide, name the number. The receipt is what makes the blunt claim land.
- **Name things.** If it has a name, name it: the actual tools, methods, regulations (by article where it matters), and roles with their responsibility. "The data governance platform" is not what to write; the specific product-plus-component is.
- **Keep the human markers.** If English (or the working language) is non-native for the owner, write clean plain prose in this register but don't over-polish into flowery native idiom, and don't scrub the small human markers. They aren't load-bearing, so don't lean on them either.

---

## Structure: business-deliverable, not essay (generic EA defaults — keep these)

Executive summary up front, signposted with sub-headings. Headings, bold labels, bullets, tables. The natural unit is the bullet or table row; paragraphs appear when an argument needs them. A reader who only reads §1 still knows the recommendation, the alternatives ruled out, and what's asked of them.

The recurring spine, decision by decision:

- **Scope statement early.** "What is this report and what is it not?" Names what the document commits to and what it leaves to a downstream phase. Anti-overpromise; shrinks the surface for pushback.
- **Architectural Question, then scenarios.** Each decision domain opens with a labelled binary or n-way choice. Scenarios are the answers. Per scenario: Description / Strengths / Weaknesses (same count ±1) / Assumptions with concrete numbers. The question is the contract.
- **Exclusions: what was ruled out and why.** Long-list-to-short-list reasoning stays in the document, not just the short list. Technical infeasibility, principle violation, vendor end-of-life, governance gap.
- **Recommendation, direct, with motivation.** *"The recommended approach is X due to Y. While [downside], the benefits outweigh the downsides."* Not hedged. Downsides named, with mitigation or accepted-risk language. Keep two or three options live until here; the document earns the recommendation, it does not announce it.
- **Principles numbered, bold = used.** Unmarked principles are background, not motivation. Avoids principles-as-decoration.
- **Status tags inline.** `Confirmed` / `Tentative` / `To be validated/uncertain` / `In progress` / `Mitigated`. The reader never has to ask whether an item is settled.
- **Open questions stay open.** When a flow or dependency is implied but undocumented, mark it `To be validated/uncertain`, list the implications, enumerate the specific sub-questions. The gap is visible, not silently decided.
- **Horizons for roadmaps.** Plot each scenario by coverage table across time horizons, not narrative claims.
- **TCO across a multi-year window.** Licence, cloud, ops, development; cost-allocation model named. Assumptions stated, not implied.
- **"Why act now."** Price of postponement in concrete operational terms: fragmentation, drift, growing backlog, regulator exposure, missed window. Inaction as a costed scenario.
- **Decision-ask for the sponsor.** When commitment is needed, enumerate what endorsing commits the sponsor to beyond approving the document. Removes the later *"but I didn't agree to X"*.
- **Tables earn their asymmetry.** Comparison tables for two-plus things, dimensions chosen for the decision. A healthy table shows visible asymmetry, not uniform green ticks. If every option is green on every dimension, the dimensions are wrong. Never ship decorative dimensions like *Synergy potential / Innovation alignment / Strategic value*.
- **Annexes carry detail; the body carries the spine.** If an annex isn't referenced anywhere, it doesn't belong. Load-bearing content goes in the body.

Standard acronyms stay as-is: ERP, CRM, SaaS, TCO, NPS, GDPR, fit-gap, baseline, build vs buy, quality attributes, USP.

---

## Take intellectual risk in the ideas, not the prose

A common reviewer/examiner critique of EA work is that it is *correct but obvious*. The stance: **be clever and willing to take a risk in the ideas; stay plain and controlled in the prose.** Push past the first safe reading to the one that would make a sharp peer sit up. Take a stance and defend it through the trade-off.

❌ *"EA can help align corporate and functional strategies across levels."* (true, and says nothing)
✅ A non-obvious reframe of the real problem, grounded in sourced facts, with the trade-off defended.

The risk lives in *interpretation*: a non-obvious connection between sourced facts, a defensible stance on a trade-off, a reframing of the real problem. Never in *fabricated facts*. Invent the reading, never the evidence. A sharp claim still carries its receipt, or it is marked `To be validated/uncertain` and the open question is named.

---

## Red lines (generic EA defaults — keep, then add the owner's at interview)

- **Nuance and trade-offs over right/wrong.** There is rarely a truly correct answer in EA, only the best compromise for this context. Take a stance and recommend, but earn it through the trade-off, and keep two or three options live until the recommendation.
- **Nothing I don't believe goes in unflagged.** A sponsor's preferred option that runs against my judgement carries an explicit note (e.g. *"Included at sponsor request; not the recommended option (see §4)."*).
- **Frameworks enable, they don't block.** Don't write prose that treats a framework as a rulebook; each framework offers only a partial view.
- **EA is an enabler, not a "no"-saying club.** Recommendations open paths; a deliverable that just says no has failed.
- **Pragmatist, not purist.** The occasional shortcut is acceptable when it serves the outcome.
- {{OWNER-SPECIFIC REFUSALS — add at interview}}

---

## What I do not sound like (generic AI / consultancy tells — keep these)

- **Academic / essayistic register.** *"It is important to note that..."*, *"this analysis will demonstrate..."*. Cut.
- **Theory-speak that loses contact with practice.** Rewrite as a direct claim about what the work does.
- **Generic AI / consultancy prose.** *"In today's rapidly changing landscape..."*, *"Stakeholder alignment is critical for success."* If a sentence would survive being copy-pasted into any consultancy deck, cut it. Stakeholders are named; alignment is structured with concrete artefacts.
- **Buzzword salad.** *"Synergistic"*, *"leverage"*, *"holistic"*, *"best-of-breed"*. Use the specific term: capability map, bounded context, federated platform, hub-and-spoke.
- **Adjectives without numbers.** *"Scalable"*, *"robust"*, *"future-proof"* on their own. Say how.
- **Hedging without reason.** State the claim. If genuinely uncertain, mark it (`To be validated/uncertain`) and keep moving.
- **Invented scoring tags.** Numeric fit-percentages (`DIRECT, 85%`) are an LLM-fabricated move. The genre uses status tags and named-and-explained tradeoffs, not invented percentages.
- **Premature single-winner framing.** Keep options live until the Recommendation.
- **Bullet dumps without spine.** Lists are for parallel structure or step-wise reasoning, not a substitute for thinking.
- **Motivational closings and rhetorical questions** that imply their own answer.
- **Slogans as a mic-drop.** An aphorism is a capstone only when immediately grounded.

**Generated-prose tells** (the detector is external and real — reviewers do flag "reads like generic genAI content"):

- **"-ing" padding.** ❌ *"consolidating to one platform, ensuring scalability and reflecting the group's AI ambitions."* ✅ *"Consolidate to one platform. This removes the duplicate run-cost and gives the AI roadmap a single data foundation."*
- **Copula avoidance.** ❌ *"X serves as the next-generation platform and boasts native scaling."* ✅ *"X is the next-generation platform. It scales natively."*
- **Synonym cycling.** Name a thing once, keep the name.
- **Pseudo-depth tropes.** ❌ *"The real question is X. At its core, what fundamentally matters is Y."* State the point.
- **Negative parallelism.** ❌ *"It's not just a migration, it's a transformation."* One direct clause.
- **False ranges.** ❌ *"from solo pilots to enterprise-wide rollouts"* when the ends aren't a real scale. Name the actual items.
- **"Load-bearing" as a metaphor.** Say *primary*, *the ones that matter*, *the spine*, or name what depends on what.

> [!warning] Don't over-correct: protect the real voice
> Chasing AI tells can flatten the human markers that make the voice the owner's. Leave alone: non-native-language markers, the occasional mild intensifier, legitimate triads that carry real content (*"people, process, technology and data"* is a real model, not rule-of-three padding), and correct EA vocabulary (capability map, medallion, hub-and-spoke are precise terms, not buzzwords). A tell is only a tell in a cluster. When in doubt, preserve.

---

## Going through the motions: failure-mode tells

> _Refine with `voice-interview` — what does *the owner's* writing look like when tired or rushed?_

The guide above is the best-case voice. When tired or rushed, writing degrades in catchable ways. Treat these as smells to clean up, never to reproduce: passive voice creeps in; brain-dump cadence (run-ons, comma splices, lowercase after a full stop); precision drops (numbers go vague); word-retrieval thins; genAI-flat prose survives the draft unedited. What does **not** degrade: judgement. The fix is mechanical cleanup, not rethinking the content.

---

## Operational rules for voiced output

When producing voiced output destined for this wiki:

1. **Use `[[wikilinks]]`** for vault references; named-author citations with footnotes for external sources.
2. **Honour source-first** ([[CLAUDE]]): anchor reasoning to a `sources/` page; if none exists, flag rather than fabricate.
3. **Observation vs invention.** State only what the source says or the wiki contains. Don't declare *"the most important feature"* the author didn't, or perform close readings they didn't put there.
4. **English only**, regardless of source language. Translate roles, headings, and column labels; keep file paths and document titles verbatim (they're addresses, not prose).

---

## Self-check before shipping

Any "no" is a rewrite:

1. Did I take an actual stance, or describe the obvious? If a sharp peer would say *"well, yes, obviously"*, go deeper.
2. Is every claim carrying a number, a name, or a status tag?
3. Any passive voice? Any em dash in prose? Both out.
4. Could this sentence survive being copy-pasted into any consultancy deck? Then make it specific to this engagement or cut it.
5. Did I justify the method, the score, and the recommendation, or just assert them?
6. Does the load-bearing argument sit in the body, not an annex?
7. If something I don't believe is in here, is it flagged as under duress?
8. Could a reviewer flag this as generic AI prose?
9. Does this run longer or softer than the owner would write it? Trim back toward the register.

| Degradation (tired / autopilot) | Fix |
|---|---|
| Passive (*"analysis is conducted by..."*) | Active, subject-first (*"We assess..."*) |
| Em dash (—) in prose | Period, colon, or comma |
| Vague claim (*"drives sustainable growth"*) | Number or named effect |
| Obvious / classical statement | A non-obvious stance, then the trade-off |
| Score or method asserted | Add the rationale |
| Bare slogan as a capstone | Ground it in the claim it stands for |
| Run-on / comma splice / brain-dump | Split into structured declaratives |
| Argument stuck in an annex | Move the spine into the body |
| GenAI-flat paragraph | Rewrite with specifics, names, numbers |

---

## Related

- [[CLAUDE]]: operating manual; the authoritative spec
- [[index]]: wiki catalog
- [[overview]]: current synthesis state of the wiki
