---
name: voice-interview
description: Interview the wiki owner to extract or refresh their writing voice, then update wiki/_resources/voice-guide.md. Use when asked to "update my voice guide", "interview me about my writing", "refresh the voice DNA", or when the voice-guide has drifted from how the owner actually writes.
allowed-tools: Read, Grep, Glob, Write, Edit, AskUserQuestion
user-invocable: true
---

# Voice Interview

Extract the owner's writing voice through a structured interview, then fold the findings back into [[voice-guide]]. This is the maintenance loop for the voice anchor: evidence in → interview → guide out.

It combines three methods: a **sample-first extraction** pass (read what the owner actually wrote before asking anything), a **pushy one-at-a-time interview** (no validation, demand real sentences, flag aspiration), and a **show-don't-tell output format** (paired ❌/✅ examples, self-check questions, quick-fix tables — not just prose descriptions).

The genre is fixed: **the owner's EA client deliverables and wiki analyses** — ARB packs, D&A strategies, transformation roadmaps, SAD-style architecture decisions, CV rationale, briefing memos. This is not a newsletter or blog voice. Keep every question, sample, and example inside that register.

---

## The cardinal rule: evidence beats description

A standing warning: **much of a professional archive is LLM-generated or LLM-smoothed — do not learn voice from it.** A description of how someone writes ("I like to be direct") is worth far less than a sentence they actually wrote. So:

- Anchor on the **genuinely owner-authored** files. At the start of the interview, ask the owner to point you at 2–4 of their cleanest, hand-written deliverables (an architecture decision document, an ARB pack, a strategy memo). Those are the corpus.
- Treat **LLM-smoothed** files as evidence of *structure*, never *cadence*. The em-dash test is a quick smoothing detector: a genuinely-authored EA deliverable carries roughly zero em dashes in prose, while its LLM-smoothed copy carries many.
- Treat the wiki's own `analyses/` pages as **anti-evidence** — they over-represent an essayistic register the owner is usually trying to reduce.
- When the owner describes their voice in the interview, ask for a real sentence. If they can't produce one, it isn't part of their voice yet — flag it, don't bank it.

---

## Step 0 — Load context (before any question)

1. Read [[voice-guide]] in full. It is the current state of the anchor (on a fresh foundation it is still the template).
2. Read **at least two** genuinely owner-authored anchor files the owner named. Read for cadence, sentence shape, signature phrasing — not just structure.
3. Build a **gap list**: what the current guide under-specifies relative to what you just read. The recurring gaps (refresh, don't assume — re-derive each run):
   - **Sentence-level cadence** — how long are the owner's sentences? Where do fragments appear? Where does a paragraph earn its place over a bullet?
   - **Signature phrases / connective tissue** — the specific words and connectors that are unmistakably theirs (a recurring "Conclusion: …", arrow-notation updates, status tags). Which ones?
   - **Openings and closings** — how a document starts before the exec summary; how it ends without a motivational wrap-up.
   - **The going-through-the-motions version** — the guide's best-case voice vs. what the owner sounds like tired or rushed, and what to correct toward.
   - **Personally hated words** — distinct from the generic AI-tells already listed. Words the owner specifically dislikes in *their own* drafts.
   - **Recurring obsessions** — themes they return to unprompted.
   - **Hard refusals** — claims, framings, or positions they will not write.
   - **Feedback received vs. feedback ignored** — and why they ignore it.
   - **Per-reader action triggers** — the guide names three readers; what each needs to act.
   - **Multilingual voice** — if the owner writes in more than one language, what shifts (beyond translation) between them.

The gap list drives question selection. Do not re-ask what the guide already nails.

---

## Step 1 — Choose interview depth

Ask the owner once, up front (or honour what they already said):

- **Full pass** — 40–50 questions, rebuild the guide from the ground up. Use when the guide is the fresh template or has gone stale.
- **Focused pass (default for an existing guide)** — 15–20 questions hitting only the gap list. Use to refresh a mature guide.
- **Async** — deliver questions in small grouped batches instead of strict one-at-a-time.

On a fresh foundation, default to the **full pass**: the guide is still the template, so there is a lot to establish.

---

## Step 2 — Interview rules (non-negotiable)

Run the questions **one at a time**. Between answers, hold to these:

1. **Push back on vague answers.** "I'm direct" → "Show me a sentence from a real deliverable where that directness lands. Now show me one where you pulled the punch and shouldn't have."
2. **Demand real samples.** Descriptions are cheap. Ask for an actual sentence, an actual heading, an actual table row — ideally from a named file. A rule with a sample beside it is the only thing that makes the guide useful.
3. **Call out contradictions.** If an answer conflicts with an earlier one or with the current guide, name the conflict and make them resolve it.
4. **Don't accept "I don't know."** Reframe or come at it from the artefact: "Open your last architecture decision doc in your head — what's the first thing you'd cut if a junior wrote it?"
5. **Flag aspiration vs. reality.** If an answer describes the architect they wish they were rather than the one the anchor files show, say so: "Your last deliverable doesn't do that. Is this how you write, or how you'd like to?"
6. **Flag generic answers.** If the answer could describe any EA consultant, push: "Every consultant says 'I tailor to the audience.' What do *you* do that the one down the hall doesn't?"
7. **Go deeper on live threads** before moving on. An unusual answer is worth three follow-ups.
8. **No validation.** No "great", no "interesting", no "that's a strong point". Acknowledge minimally, then ask the next question.

---

## Step 3 — Question bank (EA-deliverable register)

Pick ~15–20 for a focused pass (more for a full pass), drawn from the gap list. These are seeds — follow the threads that open up. Each is a doorway; the real work is the follow-ups that demand a sample.

**Cadence & sentence shape**
- Paste the opening three sentences of the last deliverable you were proud of. Why those, in that order?
- Where in a document do you allow a full paragraph instead of a bullet? Show one that earned it.
- Do you write fragments on purpose? Show one.

**Signature phrasing**
- Which phrases are unmistakably yours — the ones a colleague would recognise without your name on the page?
- Show your arrow-notation updates and status tags in the wild. What governs when you reach for them?
- How do you phrase a recommendation you're certain about vs. one you're 70% on?

**Openings & closings**
- What's on the page before the executive summary? Show a real first screen.
- How do you end a deliverable without a motivational closing? Show the last paragraph of a real one.

**Failure mode**
- When you're tired or rushed, how does your writing degrade? What slips in that you'd cut on a good day?
- What's the tell that *you* wrote something while going through the motions?

**Hated words & refusals**
- Beyond the AI-tells already in the guide, what words make you wince in your *own* drafts?
- What claim, framing, or recommendation will you not write, even when a client wants it?
- Is there a position in EA / your specialism you'd never take in a deliverable? Why?

**Obsessions & feedback**
- What do you keep coming back to, even when it's not the brief?
- What feedback do you keep getting on your writing?
- What feedback do you keep ignoring — and why are you right (or wrong) to?

**Audience**
- For each of your three readers (future-you, the downstream actor, the sharp peer) — what does each one need on the page to act? Where do they conflict, and who wins?

**Multilingual (if applicable)**
- Beyond translation, what changes in your voice between deliverables in your different working languages? Show a sentence in each that proves it.

**The transformation pair (ask near the end, repeatedly)**
- Show me a sentence a competent consultant would write, then rewrite it the way *you* would. (Harvest these — they become the ❌/✅ pairs.)

---

## Step 4 — Synthesise into the guide

When the interview converges (the owner signals done, or the gap list is covered):

1. **Update [[voice-guide]] in place**, preserving its structure and frontmatter (bump `updated:`, drop the `template` tag once it's personalised, retitle from "Voice Guide (template)" to the owner's name). It is wired into `deep-recon` and other workflows — do not rename or relocate the file.
2. **Fold findings into the existing sections** rather than bolting on new ones, unless a finding genuinely has no home. Replace each `{{PLACEHOLDER}}` and "_measure this_" note with the measured value plus a real sample.
3. **Upgrade descriptions to paired examples.** Where the guide currently *describes* a pattern, add a ❌/✅ pair harvested from the interview:
   ```
   ❌ "This approach offers significant scalability benefits."
   ✅ "Scales horizontally on S3-backed Trino; sized for 80+ updates/year since 2018."
   ```
   The ✅ side must be a real or realistic owner sentence, with numbers, names, or status tags — not a cleaned-up generic.
4. **Keep / refine the `Self-check before shipping` block** — yes/no questions in the owner's voice.
5. **Keep / refine the `Quick fixes` table** — recurring degradations from the failure-mode answers, each with the correction.
6. **Log every claim's provenance in your head:** a rule earns its place only if it's backed by a real sample or an explicit interview answer. If it's neither, mark it `To be validated/uncertain` in the guide rather than asserting it.

Show the owner a diff-style summary of what changed and why before treating the update as final.

## Step 5 — Maintenance note

The guide is a living anchor. Re-run this skill when: new genuinely owner-authored deliverables land that the guide hasn't seen, `deep-recon` output starts drifting from the voice, or it's been long enough that the failure-mode list is stale. Each run reads the latest real samples first — the guide tracks the writer, not the other way around.
