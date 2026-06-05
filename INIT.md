# Initialisation prompt — tailor this foundation to its owner

This file is the **initialisation interview** for the EA LLM-wiki foundation. It turns the generic scaffold into *your* wiki: it interviews you, then rewrites `CLAUDE.md`, `README.md`, `wiki/domains.md`, and the voice guide in place, and removes the foundation placeholders.

**Two ways to run it:**
- **Recommended:** in Claude Code, run the skill — `/init-wiki`. It executes this protocol.
- **Manual:** paste the contents of this file into a fresh Claude Code session in this repo and say "run this".

Run it **once**, in a session at the repo root (not a worktree, so the edits land on your main branch as the first real commit). After it completes, this `INIT.md` and the `init-wiki` skill can be deleted — they have done their job.

---

## What "tailoring" means here

The foundation is deliberately split so that initialisation is surgical:

| Stays as-is (general to any EA) | Gets personalised at init |
|---|---|
| Entity types, page format, frontmatter taxonomy | Owner profile (who you are) |
| The four workflows (`ingest` / `capture` / `query` / `lint`) | Wiki purpose + any secondary jobs |
| Image/diagram rules, PlantUML/Mermaid conventions | EA-discipline domain taxonomy (confirm / prune / extend) |
| Skills, the `pr-manager` agent, git workflow | Locale defaults, confidentiality posture, shipping autonomy |
| The Obsidian vault config (`wiki/.obsidian/`) | `raw/` main-checkout path |
| The voice guide's generic EA-writing principles | The voice guide's measured fingerprint (via `voice-interview`) |

The placeholders to replace are written as `{{LIKE_THIS}}` and appear in `CLAUDE.md` and `wiki/_resources/voice-guide.md`. Grep for `{{` to find every one.

---

## Protocol for the agent running this

You are setting up a personal EA knowledge base for its owner. Be a sharp interviewer, not a form-filler: ask one focused thing at a time, follow up when an answer is thin, and propose sensible defaults the owner can accept with one word. Keep it short — this should take a handful of exchanges, not an hour.

### Step 0 — Orient
1. Read `CLAUDE.md`, `README.md`, `wiki/domains.md`, and `wiki/_resources/voice-guide.md` so you know exactly which placeholders exist and what each controls.
2. Confirm you are in the repo root on the main branch (or the owner's chosen default branch), not a `claude/*` worktree. The init edits are the wiki's first real commit.
3. Tell the owner what you're about to ask for and roughly how many questions.

### Step 1 — Interview (one topic at a time)

Use `AskUserQuestion` where the choice is bounded; ask in prose where it's open. Cover:

1. **Identity.** Name (or handle), role/title, region, years in the craft, and the **specialism** the wiki centres on (e.g. Data & AI, integration, security, business architecture, generalist). → fills `{{OWNER_NAME}}`, `{{REGION}}`, `{{SPECIALISM}}`, and the voice guide's "Who I write as".
2. **Purpose / jobs.** The primary job is always the knowledge base. Ask what *secondary* jobs, if any, this wiki should serve — portfolio/evidence (for a cert, degree, or promotion), team/practice enablement, consulting reference, course study, or none. For each chosen job, get one line on what counts as a contributing page (this seeds `#job:<name>` tagging). → fills `{{SECONDARY_JOBS}}`. If "none", say so explicitly and drop the `#job:` tag from the tagging section.
3. **Domain taxonomy.** Show the twelve default EA-discipline domains from `wiki/domains.md`. Ask the owner to confirm, prune the ones outside their practice, rename to their vocabulary, or add any missing area. Keep it coarse — one tag per genuinely distinct area of *their* work. → rewrites `wiki/domains.md`, the `#domain:` list in `CLAUDE.md`, and the domain set + per-domain views in `wiki/coverage.base` and `wiki/coverage.md`. (When you change the domain set, update **all four** so the lint scan, the matrix, and the `.base` stay in lock-step.)
4. **Locale.** Units, currency, regulatory framing defaults (e.g. metric / EUR / EU AI Act + GDPR; or imperial / USD / US framing). → fills `{{LOCALE_DEFAULTS}}`, `{{NUMBER FORMAT}}`.
5. **`raw/` location.** The absolute path to the main-checkout `raw/` folder on the owner's machine (the source documents live there and are gitignored, so worktrees can't see them). If they don't know yet, leave a clear "set this later" note rather than a fake path. → fills `{{RAW_MAIN_PATH}}`.
6. **Confidentiality posture.** Is the repo private or shared/public? Are there NDA/PII constraints on what can be committed (especially attachments)? → fills `{{CONFIDENTIALITY_NOTE}}`.
7. **Shipping autonomy.** Should the `pr-manager` agent open → review → merge fully autonomously, or open + review and **stop before merge** for a manual confirm? → fills `{{SHIPPING_AUTONOMY}}`, and aligns the wording in the `CLAUDE.md` git-workflow section.

### Step 2 — Apply

1. Rewrite the placeholders in `CLAUDE.md` with the interview answers. Replace the `{{...}}` tokens; rewrite the "Who I am, and why this wiki exists" section into clean first-person prose (no leftover template scaffolding); and **remove the top "This is a foundation, not a personalised wiki yet" banner** and the "Personalise with `/init-wiki`" notes once their content is filled.
2. Rewrite `wiki/domains.md` to the confirmed taxonomy, and update `wiki/coverage.base` + `wiki/coverage.md` + the `#domain:` list and lint scan in `CLAUDE.md` to match. Update the `init-wiki` skill row in the `CLAUDE.md` skills table to past tense / remove it if the owner wants it gone.
3. Rewrite `README.md`: replace the project description and the "what this is for" section with the owner's identity and purpose; keep the setup/layout sections (they're general). Set the lineage line to credit Karpathy's pattern and this EA foundation.
4. Update `wiki/log.md`: append an `init` entry recording what was personalised.

### Step 3 — Voice guide

Hand off to the `voice-interview` skill: run `/voice-interview` (full pass, since the guide is still the template). It reads the owner's real deliverables and folds the measured fingerprint, hated words, and feedback into `wiki/_resources/voice-guide.md`, then drops the `template` tag and retitles the guide. If the owner wants to defer the voice work, leave the template in place and note it in the log — the generic EA-writing defaults are usable as-is until then.

### Step 4 — Verify and commit

1. Grep the repo for any leftover `{{` placeholders and for the words "foundation"/"placeholder"/"template" — there should be none left in `CLAUDE.md`, `README.md`, `domains.md`, or `voice-guide.md` (scaffold scaffolding should not survive into a personalised wiki).
2. Show the owner a short diff-style summary of what changed.
3. Commit (`init: personalise wiki for <owner>`), and optionally remove `INIT.md` and the `init-wiki` skill since setup is done.

---

## Self-check (the agent runs this before declaring done)

- [ ] No `{{PLACEHOLDER}}` tokens remain in `CLAUDE.md` or `voice-guide.md`.
- [ ] The foundation banner and "personalise with /init-wiki" notes are gone from `CLAUDE.md`.
- [ ] The `#domain:` set is identical across `domains.md`, `coverage.base`, `coverage.md`, and `CLAUDE.md`.
- [ ] `README.md` describes *this owner's* wiki, not the generic scaffold.
- [ ] The voice guide is either personalised (template tag dropped) or explicitly deferred in the log.
- [ ] `wiki/log.md` has the `init` entry.
