---
name: traceability-ledger
description: Audit material against the corpus that should ground it, and emit a span-level provenance ledger distinguishing quoted / paraphrased / synthesised / inferred / user-supplied / model-original, each with a grounding status, then run a propose-not-apply loop that pulls weak claims back toward the evidence. Use when asked to "check traceability", "audit grounding", "what's grounded and what's invented", "trace this against the sources", "provenance check", or before shipping material built on raw/ sources plus the wiki KB. Do NOT use when there is no corpus to ground against — an email or an exam answer from the owner's own knowledge gets the surface receipts check in voice-edit instead.
allowed-tools: Read, Grep, Glob, Write, Edit, Bash, AskUserQuestion
user-invocable: true
---

# Traceability Ledger

Audit a piece of material against the corpus that should ground it, and produce a span-level **provenance ledger** saying, for every claim, where it came from and how well a source supports it. The point is grounded material, not invented claims.

This skill is **self-contained** — everything needed to run it is below.

**Dependencies:** none. `voice-edit` is one caller, not a requirement: it hands over the stable claim set after its content pass and treats this skill as the deep source-check. The skill also runs standalone on any page or pasted block.

**When it runs.** Whenever a corpus exists and the material is meant to be grounded in it: an `analyses/` essay built on several `sources/` pages, an `artifacts/projects/` deliverable built on customer context plus the KB, a `sources/` reflection whose fidelity to the raw file matters. **Skip it when there is no corpus** — prose written from the owner's own knowledge has nothing to trace to, and `voice-edit`'s surface receipts check is the whole source check there.

**Invoked standalone or as the grounding step of an edit, the work is identical.** The span classification in steps 4 and 5 fans out per span: each span's corpus search is independent, so the audit parallelises naturally. Grounding is a property of meaning, so inside an edit it runs concurrently with the meaning-preserving wording passes, and only spans whose assertive strength changed need re-auditing. It stays propose-not-apply, so it never writes the audited document and never collides with an editor's single-writer mutations.

---

## Prime directives

1. **Propose, never apply.** Every change is a recommendation the owner accepts, edits, or rejects, shown as a diff. Never silently mutate the audited material.
2. **Grounded, not invented.** Terminal invariant: **no span is both presented as fact and silently ungrounded.** Anything not badged `estimate`, `agent-view`, or `user-*` must trace to a source.
3. **Ground against the corpus, not the open web.** Grounding sources are `raw/`, the wiki KB, and in-session owner material only. This skill has no web tools by design. A web claim is not grounding until it has been ingested as a source.
4. **Reuse the `query` discipline** (`CLAUDE.md`). When searching for support, search the canonical term plus synonyms, glossary aliases, shared-source and shared-tag expansion — never a literal match alone. Absence of a hit is a claim: report the terms searched.

> [!warning] `raw/` is absent inside a worktree
> `.gitignore` excludes `raw/*`, so a `claude/*` worktree's own `raw/` is empty. Read raw material at the main-checkout path (`{{RAW_MAIN_PATH}}` in `CLAUDE.md`). An empty `raw/` never means "no source exists", and an audit that concludes `ungrounded` from a worktree's empty `raw/` is a false negative, not a finding.

---

## Reference — the classification model

Two orthogonal axes per span, plus a confidence scalar, plus a source-trust band inherited from the source. *Where content came from* is a different question from *how well a source supports it*; the audit signal is in the cross-product.

**Axis 1 — provenance class** (where the span originates; one per span):

| Class | Definition |
|---|---|
| `quoted` | Verbatim or near-verbatim from a source (`exact` / `near-verbatim`). |
| `paraphrased` | Single-source restatement; meaning preserved, wording changed. |
| `synthesised` | Built from two or more sources; entailed by their combination, verbatim in none. |
| `inferred` | Extends beyond what any source states. Reasoning or extrapolation. The risk class. |
| `user-assertion` | A claim the owner stated in-session with no backing document. Authority is the speaker. A span drawn from a pasted *document* is not this: use the normal classes with that document as locator. |
| `model-original` | Authored by the assistant with no source. `scaffolding` (headings, transitions) or `substantive` (a novel claim or judgement). |
| `common-knowledge` | Widely-known, citation-free fact. |

**Axis 2 — grounding status** (how well the corpus supports it):

| Status | Meaning |
|---|---|
| `grounded` | A specific source span entails it; locator provided. |
| `partial` | A source is related but does not fully entail it (the faithfulness gap). |
| `ungrounded` | No source support. Legitimate for `user-assertion` and `model-original`; a defect for anything presented as fact. |
| `contradicted` | A source conflicts with it. Always flagged, always resolved. |

**Confidence:** `settled` / `working` / `speculative` / `single-source`, reusing the frontmatter vocabulary in `CLAUDE.md`.

**Source-trust band** (a property of the *source*, capped onto the span): `trusted` / `mixed` / `weak` / `unverified`. Assess across four dimensions — **identity** (verifiable author or publisher, track record), **expertise** (standing, peer recognition, no misinformation history), **motivation** (conflicts of interest, financial or political stake), **corroboration** (independently verifiable, supporting and contradicting sources). Gaps trigger deeper investigation, not a number. Where a source needs investigating, read laterally: check what other sources say *about* it rather than reading it harder, and trace a claim back to its original rather than stopping at whoever repeated it. **Source-trust caps confidence:** a span grounded in a `weak` source cannot be `settled`.

**Decision table — the cross-product sets the action:**

| Situation | Action |
|---|---|
| `quoted` / `synthesised` / `paraphrased` + `grounded` + source `trusted` | Clean. No action. |
| anything + `grounded` + source `weak` / `unverified` | Flag. Technically grounded, but the source has not earned the confidence; cap confidence, route to the loop. |
| `user-assertion` + `ungrounded` + cross-check `silent` | Fine, but badge it so it is never read as KB fact. |
| `user-assertion` + cross-check `contradicts-KB`, or a high-stake assertion with thin corroboration | **Stop.** Surface the conflict or the motivation gap before continuing. |
| `model-original/scaffolding` + `ungrounded` | Fine. No action. |
| `model-original/substantive` + `ungrounded` | The assistant asserting on its own authority. Hedge, confidence-mark, badge `agent-view`. |
| `inferred` + `ungrounded` + `speculative` | Highest-risk cell. Must be resolved by the loop. |
| anything + `contradicted` | **Stop** and resolve before the material ships. |

---

## Step 1 — Parse input

Establish three things, asking only what you cannot infer:

- **Target material** — a wiki page path, a pasted block, or material produced this session. If ambiguous, ask.
- **Corpus scope** — KB-grounded, customer-context, or both. For a wiki page, default to KB-grounded and seed the corpus from its `sources:` frontmatter.
- **Owner material in play** — note which pasted items are **documents** (decks, PDFs, articles: quotable ephemeral sources) and which are **assertions** (bare claims stated in chat). They are treated differently downstream.

## Step 2 — Assemble the corpus, rate source trust, build the session envelope

- **`raw/` and the wiki KB:** resolve the in-scope source set. For KB pages, **inherit** their `confidence:`, `sources:` and `relationships:` — a span grounded in a `settled` concept inherits high confidence; one grounded in a `single-source` or `speculative` page inherits that caveat.
- **Source trust:** if a source page records a trust band, read it. Otherwise assess the four dimensions above and note the band in the ledger; web-origin sources and pasted documents always need one. For assertions, lead with the motivation dimension: what is the speaker's stake in this being true? Media-provenance checks (C2PA, manipulated images) belong to `attachments/`, not the prose ledger.
- **Owner documents:** register each as an ephemeral session source with a locator (for example `client deck p.4 (session-local)`). Spans may be `quoted` / `paraphrased` / `synthesised` against them exactly as against `raw/`.
- **Owner assertions:** build the session envelope — sub-type (`stated-fact` / `goal-or-instruction` / `assumption-or-hypothesis`), an assigned confidence defaulting **below** KB-`settled`, and a KB cross-check (`confirmed-by-KB` / `silent` / `contradicts-KB`). A `contradicts-KB` assertion is surfaced, never absorbed.

## Step 3 — Segment into spans

Split the target into claim-level spans, one classifiable assertion each; fall back to sentence-level where a sentence carries a single claim. Give each a stable id (`S01`, `S02`, …). Scaffolding — headings, transitions — is its own span, not skipped: class it `model-original/scaffolding`.

## Step 4 — Classify every span

For each span assign, using the Reference tables: **class** (Axis 1), **grounding** (Axis 2), **confidence**, **source-trust** (the weakest band among its sources, which caps confidence), **cross-check** (assertions only), and a one-line **rationale** saying *why*. The rationale is what makes the ledger explainable rather than a wall of labels.

## Step 5 — The grounding-and-iterate loop (propose-not-apply)

For each span where `class = inferred`, **or** `grounding ∈ {partial, ungrounded, contradicted}`, **or** cross-check is `contradicts-KB`, **or** `source-trust ∈ {weak, unverified}` — **and** it is not legitimately ungrounded by design (a `user-assertion` with a `silent` cross-check, or `model-original/scaffolding`):

1. **Attempt to ground it.** Search every in-scope corpus layer with the `query` discipline.
2. **If support is found,** *propose* a re-link plus an upward reclassification (`inferred` → `synthesised` → `paraphrased` → `quoted` as inferential distance shrinks), with a candidate rewrite that tracks the source. Show the original span, the candidate source, and the proposed wording.
3. **If contradicted** by a source or by the KB cross-check, *propose* correcting to match the source — or, where the conflict is real and intended, flagging it in prose and in `relationships: contradicts`.
4. **If no support is found,** never leave it disguised. *Propose* one of: **hedge** (downgrade confidence, soften), **relabel** explicitly as `model-original` or `speculative` with a visible badge, or **cut**.

Record each as a `proposal` in the ledger with a blank `resolution`. Do not edit the document yet.

## Step 6 — Emit the ledger, then resolve to fixpoint

1. **Write the ledger** to `.claude/traceability-ledgers/<target-slug>/ledger.md`, using `templates/ledger-template.md` beside this file. That path is gitignored scratch (the `.claude/*` rule), because client-context audits may be confidential. Fill all five parts: header and corpus manifest, summary stats, span table, challenge-and-iterate log, and reverse traceability (which in-scope sources were used, flagging unused ones as a gap or an over-claim).
2. **Present the open proposals** compactly, as diffs with rationale, grouped by span. Use `AskUserQuestion` where a span has genuinely distinct resolutions (hedge versus relabel versus cut); otherwise list them for a batch accept / edit / reject.
3. **Apply only accepted proposals** to the target material, record each `resolution` (`accepted` / `edited` / `rejected`) in the ledger, and carry agreed badges (`estimate`, `agent-view`, `user-assertion`) into the document where wanted.
4. **Re-run steps 4 and 5** over changed spans until every span is `grounded` or explicitly ungrounded by design, with no open proposals. Report the final summary: grounded share of factual spans, remaining badged exceptions, and confirmation that no covert invented claim survives.

---

## Output and promotion

- Default output is the **gitignored scratch ledger** plus the **badges** that survive into the material. The durable KB record is the page's own frontmatter (`confidence:`, `sources:`, `relationships:`) updated from the audit, not the full ledger.
- **Promote on request only.** If the ledger is worth keeping, file it as a companion `project-artifact` beside the material, or embed a collapsed summary. Never auto-commit a ledger that may carry client-confidential context.

## Guardrails

- Never present an `inferred` or `ungrounded` span as sourced fact. When in doubt, badge it.
- Never inflate a class upward without a real source link behind it.
- A `contradicts-KB` assertion always stops for the owner: the client may be right and the wiki stale, or the reverse. Surface both, never pick silently.
- This is an audit of *material*, not of the author. Keep every rationale about the evidence.

---

## Related

- `voice-edit` — the caller. Its pass-1 receipts check is the surface test (does a receipt *appear*); this skill is the deep test (does the receipt *trace*). Where a corpus exists, this skill subsumes the surface check rather than running beside it.
- [[voice-guide]] — the drafting-side prevention: draft with receipts, mark uncertainty, never fabricate. One concern at three depths, not three copies of one check.
- `CLAUDE.md`, the `query` workflow — the search discipline this skill reuses, including the alias bridge and "absence is a claim".
