# LLM Wiki — Operating Manual (Enterprise Architect foundation)

Read this file at the start of every session. It defines what this wiki is, how its pages are organised, and the workflows you use to maintain it.

> [!note] House style for this file (apply to every edit)
> CLAUDE.md is injected at the start of every session, so every line is re-read each time. Keep it lean: condense **deterministic rules** (paths, syntax, fixed procedures, reference tables) to the rule itself; for **judgment calls** (when, how much, trade-offs) keep the *why* — it steers the decision — but in the fewest words that preserve it. Cut filler, duplication, and once-only backstory.

> [!important] This is a foundation, not a personalised wiki yet
> This repo is the **reusable LLM-wiki scaffold for an enterprise architect**. Before first real use, run the initialisation interview — `/init-wiki` (or paste [`INIT.md`](INIT.md)) — which interviews the owner and rewrites the owner profile, purpose, EA-discipline domains, and voice guide in place, then removes this banner. Until that is done, the `{{PLACEHOLDER}}` values throughout are generic defaults. The *structure* is already final and general-purpose — entity types, page format, the four workflows, image/diagram rules, skills, and the git workflow do not change per owner. What init personalises is the owner-specific content: the profile, the purpose, the EA-discipline domains, the voice guide, and the inline `{{…}}` settings scattered below (raw-source path, secondary jobs, confidentiality posture, shipping autonomy, locale defaults).

---

## Who I am, and why this wiki exists

> [!note] Personalise with `/init-wiki` — the block below is a template
> Replace the placeholders with the owner's real profile during initialisation.

I'm {{OWNER_NAME}} — an enterprise architect based in {{REGION}}, specialising in {{SPECIALISM}} (e.g. Data & AI, integration, security, business architecture). This wiki is my personal knowledge base in the Karpathy tradition: low-friction notes that compound through re-reading and re-asking. It is not a polished reference manual, not an enterprise architecture repository, and not a technical writer's notes-keeper.

**Primary job — knowledge base.** The wiki's first and always-on job is to be my compounding knowledge base on enterprise architecture and the topics around it (the EA disciplines below, plus whatever I want to think clearly about).

**Secondary jobs — queried at init, optional.** A wiki can serve more jobs than the KB, and which ones depend on the owner. Captured during `/init-wiki`; examples:

- **Portfolio / evidence** — pages tagged to materialise into a body of work for a certification, a master's capstone, a promotion case, or a client showcase.
- **Team / practice enablement** — a shared reference the owner curates for a team or guild.
- **Consulting reference** — anonymised patterns and decisions reusable across engagements.
- **Study** — structured digestion of a course, certification track, or reading list.

> {{SECONDARY_JOBS}} ← filled at init; if the owner only wants the KB, this is just "none — pure knowledge base".

A page can serve more than one job via tags. Do not carve the directory tree by job; tags carry the multi-job mechanism.

You own everything in `wiki/`. `raw/` is mostly hands-off, with two exceptions:

1. **Reorganisation with explicit permission.** If I ask you to restructure `raw/` (rename, move, regroup files into subfolders), you can — but only after I've said so for this specific action. Don't reorganise pre-emptively or as a side effect of another workflow.
2. **Filing attached files for ingestion.** When I attach a file in chat and ask you to ingest it, you may place it under `raw/` in the appropriate subfolder before running `ingest`. Pick the folder by analogy with what's already there; ask if no obvious home exists. Never modify files already in `raw/` as part of this — only add new ones.

Outside these two cases, treat `raw/` as immutable. This rule is also **enforced**, not just stated: the committed PreToolUse hook `.claude/hooks/guard-raw.sh` (wired in `.claude/settings.json`) denies edits of existing raw files and overwrites of them, allows new-file adds, and additionally blocks credential-shaped content anywhere in the repo. It needs `jq` and fails closed without it.

---

## Karpathy-style ethos (the part that matters)

- Cheap to write in, expensive to re-read. Capture loose ends; let synthesis emerge.
- Atomic notes are the default unit. One idea per page, dense `[[links]]`.
- Essays are earned. Write a long synthesis (in `analyses/`) only when atomic notes have actually clustered.
- Questions are first-class. Open questions are how gaps and future directions surface.
- Compounding happens during `lint` — re-reading old notes, re-asking old questions, writing back what's changed, spotting gaps.

---

## Directory structure

> [!important] `raw/` is gitignored and absent from worktrees
> `.gitignore` excludes `raw/*` (keeping only `raw/.gitkeep`), so the raw source documents are **not checked into git and do not exist inside `claude/*` worktrees** — a worktree's own `raw/` looks empty. The files live only in the **main checkout** at the repo root. When a session runs in a worktree and needs to read raw material, access it at the absolute main-repo path (set `{{RAW_MAIN_PATH}}` at init to the owner's main-checkout `raw/` location), **not** the worktree's `raw/`. An empty `raw/` in a worktree means "look in the main checkout," never "no source exists."

```
raw/                ← immutable source documents (read, never write)
wiki/
  index.md             ← catalog of pages
  log.md               ← append-only activity log
  overview.md          ← high-level synthesis across the wiki (rewritten during lint, not inline)
  glossary.md          ← living terminology
  domains.md           ← canonical list and scope of the EA-discipline domains
  coverage.md          ← materialised coverage matrix across the domains (rewritten during lint)
  coverage.base        ← live, page-level Bases view across the domains (companion to the .md)
  inbox/               ← quick-capture notes pending triage
  sources/          ← one parent page per raw source (chunked into concept notes for long ones)
  concepts/         ← atomic notes, one idea per page
  frameworks/       ← named methodologies and standards (TOGAF, ArchiMate, DAMA-DMBOK, EU AI Act structure, etc.)
  questions/        ← open questions I'm thinking about; first-class entity, drives gap detection
  cases/            ← real-world or hypothetical cases to reason about
  analyses/         ← essay-length syntheses (earn their way in from concept clusters)
  artifacts/        ← things I produce while learning or working; separate from the KB proper
    lessons/        ← pedagogical scaffolding I keep around (Socratic walkthroughs, course/cert digests)
    exercises/      ← assignments, exam answers, practice work, graded outputs
    projects/       ← ADRs and other artifacts produced for specific client/project work
  attachments/      ← binary attachments (images, screenshots, exported diagrams) for the wiki — see "Images and diagrams"
    sources/<slug>/      ← images extracted from or illustrating a sources/ page
    concepts/<slug>/     ← images illustrating a concept
    frameworks/<slug>/   ← images for a frameworks/ page
    cases/<slug>/        ← images for a cases/ page
    analyses/<slug>/     ← images for an analyses/ page
  _resources/       ← wiki infrastructure that isn't an entity page (e.g. voice-guide.md)
```

Create new subdirectories if you genuinely need them. Don't ask permission for the obvious ones.

**KB vs `artifacts/`.** The knowledge base (`sources/`, `concepts/`, `frameworks/`, `questions/`, `analyses/`, `glossary.md`) is what I *learn* — synthesised, atomic, evergreen. `artifacts/` is what I *produce* while learning or working — it consumes the KB rather than growing it. Lessons get re-read and refined; exercises are done-and-archived; project artifacts get referenced when similar work comes up. Keep these out of `analyses/` and `concepts/` so the KB doesn't get polluted with student work, teaching scaffolding, or client-specific deliverables. Cases (`cases/`) remain scenarios I reason *about*, not artifacts I produce.

---

## Entity types

| Type | Location | Purpose |
|---|---|---|
| Source | `sources/` | Summary of a raw document. Long sources (books, course modules) get a parent page plus atomic concept notes per chapter or idea. |
| Concept | `concepts/` | One idea per page, atomic, dense linking. Default unit of capture. |
| Framework | `frameworks/` | A named methodology or standard — purpose, structure, where it applies, limits, related concepts. |
| Question | `questions/` | An open question I'm thinking about. Status, linked notes, gap field, last-ruminated date. |
| Case | `cases/` | A scenario (anonymised client, hypothetical, exercise) to reason about. |
| Analysis | `analyses/` | Essay-length synthesis pulling concepts together. Written when a cluster has earned it. |
| Lesson | `artifacts/lessons/` | Pedagogical scaffolding — Socratic walkthroughs, course/cert digests, exercise sets I keep around to re-read. Evergreen. |
| Exercise | `artifacts/exercises/` | A graded coursework output (assignment answer, exam response, practice work). Done, then archived; rarely refined later. |
| Project artifact | `artifacts/projects/` | An ADR, design doc, or other deliverable produced for a specific client/project context. Referenced when similar work comes up, not as general-purpose KB. |
| Inbox note | `inbox/` | Quick capture, pending triage. |

The entity-type set applies to pages in the subdirectories above. The top-level wiki files (`index.md`, `log.md`, `glossary.md`, `overview.md`, `domains.md`, `coverage.md`) are infrastructure, not entity pages — they use semantically meaningful `type:` values outside this set (or no frontmatter at all, for `index.md` and `log.md`). Don't try to force them into the entity schema.

---

## Page format

Every page has YAML frontmatter:

```yaml
---
title: <page title>
type: source | concept | framework | question | case | analysis | lesson | exercise | project-artifact | inbox
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [list]
sources: [filenames in raw/ that informed this page]   # if applicable — see completeness rule below
confidence: settled | working | speculative | single-source   # optional, mainly concept/analysis pages
relationships:                                                # optional, structured typed links — see Relationships taxonomy below
  extends: [page-a, page-b]
  contradicts: [page-c]
  applies-to: [page-d]
  supersedes: [page-e]
  superseded-by: [page-f]
  crystallized-into: [analysis-x]   # on concept/source pages when a cluster has earned an analysis
  synthesised-into: [analysis-y]    # on question pages when the question has converged into an analysis
---
```

For `question` pages, add:

```yaml
status: open | converging | answered | dropped
last-ruminated: YYYY-MM-DD
gap: <free text — what's missing to answer this fully>
```

**`sources:` completeness rule.** List **every** raw basename a page reflects, even when the page also cites a URL or bundles several files (e.g. a per-chapter book hub, a cluster page). The `sources:` field is the machine-readable record of "this raw file is ingested" — the ingest-coverage manifest and any future un-ingested sweep trust it. A page that ingests a file's substance but omits its basename makes that file look un-ingested (the recurring false-positive). Index-only pages that deliberately *don't* transcribe their files are the one exception — they carry the titles in the body, not in `sources:`. Coverage tool + its rules: `wiki/_resources/ingest-coverage.md`.

After frontmatter:
1. One-line summary (used in `index.md`).
2. Body — atomic notes stay short; essays can section out.
3. `Related` section at the bottom with `[[links]]`.

Filenames are kebab-case. Page titles match filenames.

---

## Tagging convention

Tags carry the multi-job mechanism. Reserved prefixes:

- `#domain:<name>` — contributes to one of the EA-discipline domains in [[domains]]. A page can carry multiple `#domain:` tags when its content legitimately spans several (common case: AI governance spanning `data` + `security` + `governance` + `exponential-tech-innovation`).
- `#kb:<area>` — broad knowledge-base area (e.g. `#kb:data-mesh`, `#kb:eu-ai-act`).
- `#job:<name>` — marks a page as serving one of the wiki's secondary jobs configured at init (e.g. `#job:portfolio`, `#job:team`, `#job:study`). Only present if the owner enabled secondary jobs; the KB job needs no tag (it is the default for every page).

Free-form tags are fine alongside these.

> [!note] Domain taxonomy is owner-tunable
> The default `#domain:` set ships as the twelve EA disciplines in [[domains]]. The init interview confirms, prunes, or extends the set to match the owner's practice. The coverage machinery (the domain coverage scan in the `lint` skill) reads whatever taxonomy [[domains]] declares — it is not hard-wired to a fixed count.

---

## Cross-referencing

Use `[[filename-without-extension]]` for internal links. When you create or update a page, scan related pages and add back-links. `glossary.md` and `overview.md` link to every major entity page.

### Relationships taxonomy

Inline `[[link]]` is the default for narrative cross-references — keep using it liberally. Use the `relationships:` frontmatter block only when the relationship matters for `query` and `lint`:

- `extends` — builds on the linked page's idea
- `contradicts` — conflicts with a claim on the linked page (flag in prose too)
- `applies-to` — concept used in the linked case/analysis/framework
- `supersedes` / `superseded-by` — newer source updates an older claim
- `crystallized-into` — a concept whose cluster has earned an `analyses/` page
- `synthesised-into` — a question that converged into an `analyses/` page

Don't force every cross-reference into the taxonomy. If it's not load-bearing for queries or lint checks, leave it as an inline `[[link]]`. The frontmatter block is grep-able and lint-checkable; inline links are for prose flow.

The `confidence:` field is similarly optional. Default behaviour: omit unless the page is single-source or actively contested. Concepts cross-referenced by ≥3 sources are implicitly `settled` — no need to write it.

---

## Images and diagrams

The wiki uses images where they carry the concept, not as decoration. **Bias toward inclusion:** removing a redundant image later is cheap; reconstructing visual context after the source has slipped from memory is expensive.

This section keeps the track choice and the storage convention. **Everything downstream (PlantUML conventions, render verification, redrawing source figures, selection caps, file hygiene, the lint additions) lives in `.claude/rules/diagrams.md`. Read that file before you author, materially edit, or verify any figure.** Its `paths:` header may load it automatically; the explicit read on this pointer is the fallback that must not be skipped. The **syntax** lives in the `diagram-syntax` skill (Mermaid per-type references, PlantUML and the Hosiaisluoma ArchiMate macros, C4 layout science, the render-verify loop); this file still decides the track.

**Four tracks, in order of preference:**

1. **Mermaid (default)** — flowcharts, sequence, state, class/ER, mindmap, gantt, quadrant, xychart, simple component/layer graphs. Renders natively in Obsidian (no plugin, no server). Prefer it when structure is the message: the source is the diagram, so it diffs cleanly, stays portable, and a later session can read and edit it.
2. **PlantUML** — ArchiMate (Strategy/Motivation/Business/Application/Technology with correct shapes/colours), C4 (context/container/component), and notations Mermaid lacks. Rendered by the **`obsidian-plantuml`** plugin (under `wiki/.obsidian/plugins/`) via the local JAR at `wiki/.obsidian/plantuml/plantuml.jar`. Prereq: `brew install openjdk graphviz` plus the symlink (see `wiki/.obsidian/plantuml/README.md`). Falls back to the public PlantUML server if local rendering fails.
3. **Designed SVG** (hand-/script-authored) — only for *hero figures on deliverable/portfolio pages* whose value is bespoke layout or heat/colour encoding Mermaid can't do (heatmaps, matrices, dashboards, layered architecture with overlays). Three required conditions, because the SVG is opaque to readers and later sessions: every load-bearing claim and its rationale live in the **markdown** (not only the figure); the **generator script is committed beside the SVG**; the **caption carries the message**. Verify with `rsvg-convert` before commit. Not for the atomic-note KB core — that stays Mermaid.
4. **Committed raster (fallback)** — only when even a designed vector loses meaning: iconic source screenshots (Gartner 2×2s, Magic Quadrants, reference-architecture figures, the EU AI Act risk pyramid), photographs (whiteboards, slides), hand-laid ArchiMate exports from Archi. Stored as binaries in git.

Tracks compose: include both an iconic source image and a redrawn Mermaid version when each adds distinct value.

**Choice:** ArchiMate any-layer, C4, UML deployment → PlantUML; bespoke-layout / heat / matrix / dashboard hero figures on deliverable or portfolio pages → designed SVG (claims in markdown, generator committed); everything else, and anything where portability or later-session maintainability matters → Mermaid.

**Storage.** `wiki/attachments/<entity-type>/<page-slug>/<name>.<ext>`, mirroring entity structure — e.g. a figure on `sources/strengholt-medallion-ch03.md` → `wiki/attachments/sources/strengholt-medallion-ch03/medallion-overview.png`. Kebab-case, content-describing filenames; add source coordinates when lineage matters (`fig-3-1-medallion-flow.png`).

**Embedding.** `![[attachments/sources/<slug>/<image>.png]]`, with a one-line prose caption under it saying what the image shows and why it's here. Cite the source page if from `raw/` (`Source: [[strengholt-medallion-ch03]], figure 3.1`).

---

## Terminology discipline

When a new term appears, add it to `glossary.md`. Use the canonical term consistently across pages. Flag conflicts explicitly. Note regional and regulatory variants where they matter. Default to the owner's locale conventions ({{LOCALE_DEFAULTS}} — e.g. metric units, EUR, EU regulatory framing).

**Alias bridge (load-bearing for recall).** When a concept is filed under a canonical term but known in the field by a vendor/client/practitioner label, record the alias in the glossary pointing at the canonical page — e.g. *"Product & Capability Model (PCM) → [[product-and-platform-operating-model]]"*. This fixes the recurring miss where I ask about a field term ("the McKinsey thing the client calls X") but the wiki holds the substance under another name, so a literal search fails. Do it proactively at `ingest` time for any vendor/practitioner synonym, not just after a miss. The glossary is the synonym index: an alias here turns a future lexical search on the field term into a hit.

---

## Workflows

Four workflows: `ingest`, `capture`, `query`, `lint`. At any moment, you are in exactly one. Each is a project skill under `.claude/skills/<name>/`, loaded when invoked rather than carried in every session. The Skills table below is the single enumeration of the four, as it is for every other skill; this section does not repeat their procedures.

Three rules out of those procedures stay here, because a session can breach them without ever invoking the skill:

- **Source-first.** Every raw file gets a `sources/` page that reflects it, even a thin one. Concepts, frameworks, cases and questions are *derived* from that page, never extracted straight to `concepts/` while skipping the source.
- **Absence is a claim, not a default.** Never say "X isn't in the wiki" without searching multiple terms, synonyms and the glossary aliases first. On a genuine miss, name the terms you searched.
- **`overview.md` is never updated inline.** It is rewritten during `lint`, deliberately and with breadth, to avoid recency bias and overview thrashing.

**Before committing any wiki change, run `python3 scripts/preflight.py`** (frontmatter, dead links, missing embeds, stale `updated:`). The `lint` skill documents its flags and the companion `scripts/lint-aggregates.py`.

---

## Skills

Skills live under `.claude/skills/` to make Obsidian-native conventions executable and to support deep reconnaissance work. **CLAUDE.md is the authoritative spec — these skills are *executable adjuncts*, not rule sources.** If a skill's defaults conflict with anything in this file (entity schema, frontmatter taxonomy, source-first principle, workflow names, tag prefixes, voice anchor), this file wins. Skills are invoked when their trigger conditions match, but they bend to the wiki's conventions, not the other way around.

Three provenances, all committed-or-installed honestly (see [`NOTICE`](NOTICE)):
- **The wiki's own** (Apache-2.0, committed): the four workflow skills (`ingest`, `capture`, `query`, `lint`), `init-wiki`, the `pr-manager` agent, `voice-interview` (co-authored by the owner with LLM assistance and informed by public guidance on writing with LLMs — no third-party source redistributed in it), `critical-reviewer` (owner-authored anti-sycophancy review skill, invoked by the `pr-manager` agent's review gate — no third-party text reproduced), `pyramid-structure` (owner-authored operationalisation of Minto's Pyramid Principle and related public method; no third-party text reproduced), `voice-draft`, and `voice-edit`.
- **Adapted third-party** (committed, with attribution): `deep-recon` is adapted from [`kvarnelis/deep-recon`](https://github.com/kvarnelis/deep-recon) (MIT) — voice-anchored to this wiki and re-routed to its entity folders. `diagram-syntax` combines an owner-authored orchestration layer (SKILL.md, the verified ArchiMate/Hosiaisluoma reference, the render-verify loop) with reference files vendored from [`tractorjuice/arc-kit`](https://github.com/tractorjuice/arc-kit) (MIT; itself sourced from the mermaid.js.org docs via `WH-2099/mermaid-skill` and from `SpillwaveSolutions/plantuml`) — each vendored file records its own provenance and is refreshed from upstream, not hand-edited. Upstream MIT notices are reproduced in `NOTICE`.
- **Installed, not committed** (the **⬇** rows below): the Obsidian-native skills from [`kepano/obsidian-skills`](https://github.com/kepano/obsidian-skills) (Steph Ango's official Agent Skills, MIT), installed by `setup.sh` / `setup.ps1` into `.claude/skills/` (gitignored). Install with the setup script or `/plugin marketplace add kepano/obsidian-skills`.

| Skill | Trigger | Primary use here |
|---|---|---|
| `ingest` | "ingest this", a file in `raw/` or attached in chat | Process a source source-first: the `sources/` page, then derived concepts, frameworks, cases and questions, back-links, glossary, index, log. 5–15 pages per run is expected. |
| `capture` | a half-thought, meeting reflection or paragraph with no source | Quick dated note to `inbox/`. No glossary, index or cross-linking; triage happens at `lint`. |
| `query` | a question the wiki should answer | Concept-first search across every entity folder, synthesis cited to `[[links]]`, then rumination on the matching `questions/` page. |
| `lint` | "run a lint", weekly, after a batch of ingests | The compounding pass: inbox triage and the `overview.md` rewrite forward; pre-flight, contradictions, orphans, question gaps, the skills-table drift check, the routed checks and the domain coverage rebuild backward. |
| `init-wiki` | first-time setup of this foundation | Interviews the owner and tailors `CLAUDE.md`, `README.md`, `domains.md`, and the voice guide. Run once, then it's dormant. |
| `voice-interview` | "update my voice guide", "interview me about my writing" | Extracts the owner's writing voice from real deliverables and folds it into [[voice-guide]]. Run during init and whenever the voice anchor drifts. |
| ⬇ `obsidian-markdown` | `.md` files; mentions of wikilinks, callouts, frontmatter, embeds | Codifies the wikilink / callout / block-id / footnote conventions this wiki uses. Use callouts (`> [!warning]`) for in-page emphasis, block IDs (`^id`) when linking to specific paragraphs. |
| ⬇ `obsidian-bases` | `.base` files; database-style views | The `coverage.base` and any future live dashboards (questions triage, single-source-risk view, stale-page scan). |
| ⬇ `obsidian-cli` | "interact with my vault", live operations on the active Obsidian instance | **Conditional — see below.** Use only when Obsidian is running *and* the CLI is materially faster than `rg`/`fd`. |
| ⬇ `json-canvas` | `.canvas` files; mind maps, flowcharts | Domain-coverage canvases, concept-cluster maps, case-study network diagrams. Niche but cheap. |
| ⬇ `defuddle` | URLs to non-`.md` web pages | First-line tool for web-sourced `ingest`: cleans clutter before WebFetch. Requires `npm install -g defuddle`. |
| `diagram-syntax` | `.mmd` / `.puml` paths; authoring or debugging a Mermaid, PlantUML, ArchiMate or C4 diagram | The syntax layer under the "Images and diagrams" policy above. That policy decides *which* track and *whether* a figure earns its place; the skill supplies the Mermaid per-type and PlantUML/ArchiMate macro reference, the C4 layout science, and the render-verify loop. |
| `deep-recon` | `/deep-recon <topic>`, "brainstorm deeply", "stress-test this idea" | Multi-agent reconnaissance for `query` rumination and pre-essay scoping; voice-anchored to [[voice-guide]]. Only the final deliverable lands in the wiki, routed by type like any `query` output (essay → `analyses/`, update → in-place, half-formed → `inbox/`); intermediate agent files are scratch (see `SKILL.md`). |
| `critical-reviewer` | "be critical", "stress-test this", "devil's advocate", "what am I missing", "no flattery" | Anti-sycophancy adversarial review. Invoked by the `pr-manager` agent before it reviews a PR, and on demand when you want work challenged rather than affirmed. |
| `pyramid-structure` | "help me structure this", "what's my so what", "build an outline", "is this MECE", before drafting a document or deck | Minto Pyramid Principle + "so what" test: decides the governing thought and MECE decomposition before a word is drafted. Output is an outline in the working directory, not a wiki page; the prose is then drafted against [[voice-guide]]. |
| `voice-draft` | writing or rewriting any prose that ships under the owner's name; and whenever a subagent authors a page on the owner's behalf | The drafting *process* against [[voice-guide]], which is the *standard*. Loads the guide and the `pyramid-structure` outline, drafts against both, writes the receipt with the claim, then stops and labels the result "pre-edit draft". It does not structure and it does not edit. |
| `voice-edit` | "edit this", "tighten", "polish", "clean this up", "proofread"; and as the mandatory finishing loop after `voice-draft` | The editing *process* against the same standard. Three altitude-ordered passes (structure → line → surface), mechanical fixes applied and substantive changes proposed, looping until the guide's self-check runs clean. Pass 1 checks structure against the `pyramid-structure` outline rather than re-deriving a spine, and hands back to that skill where the argument itself is unsound. |

> [!note] Publishing to Confluence
> To publish wiki material to Confluence, add the Anthropic `anthropic-skills:confluence-edit` skill via `/plugin` and re-anchor its prose to [[voice-guide]]. It is not bundled with this scaffold.

### `obsidian-cli` — conditional gate

Obsidian is almost always open, but the CLI is not always the right tool. Before invoking any `obsidian <command>`, run:

```bash
pgrep -x "Obsidian" >/dev/null && echo "Obsidian running" || echo "Obsidian not running — skip CLI"
```

If Obsidian is not running: do not use the CLI; fall back to `rg`/`fd`/Read.

Even when Obsidian *is* running, only use the CLI for operations where it provides a meaningful efficiency gain over file-level tools:

| Worth using CLI | Use `rg`/`fd`/Read instead |
|---|---|
| `obsidian backlinks file="..."` (resolves live link index) | Plain text search across files |
| `obsidian daily:append` / `daily:read` (Daily Notes plugin integration) | Reading a known markdown file |
| `obsidian property:set` (frontmatter property mutation with index awareness) | Bulk frontmatter edits via Edit |
| `obsidian tasks daily todo` (Tasks plugin queries) | Listing files |
| `obsidian eval code="..."` (Obsidian app context for plugin/theme work) | Code in this repo |
| `obsidian dev:*` (plugin/theme development cycle) | n/a unless doing plugin work |

If in doubt, use the file-level tools — they're deterministic and don't depend on Obsidian being healthy.

### Semantic search — Smart Connections (Obsidian)

The vault ships with the **Smart Connections** community plugin (`wiki/.obsidian/plugins/smart-connections/`). It runs a local embedding model (`wiki/.smart-env/`, no API key, no external service) and keeps an incremental vector index, catching the **vocabulary-mismatch** recall failure — related notes whose words differ from the query (the glossary alias bridge's job, done semantically). It's a *browsing* aid in Obsidian (Connections pane, semantic search), **not** callable from a Claude Code session: in-session recall still uses the `query` skill's protocol plus glossary aliases. Plugin code is not committed — install from Obsidian's community browser like the PlantUML plugin (listed in `community-plugins.json`); the embeddings store (`wiki/.smart-env/`) and `data.json` are gitignored, regenerated on demand.

### Voice anchor

**Every entity page is voiced prose, source pages included.** A `sources/` page is not a neutral transcript: it selects, compresses, and frames the raw artifact, so it is synthesis in the owner's voice, not quoting. The same holds for `concepts/`, `frameworks/`, `analyses/`, `cases/`, `questions/`, and the `artifacts/` pages. So read [[voice-guide]] before drafting **any** of them, not only analyses and recon documents. This holds whether the page is written directly or by a subagent — an ingest subagent reads the voice guide too. The deep-recon Synthesizer agent points at it directly; other workflows should too. The voice guide is built and refreshed by the `voice-interview` skill.

**The anchor at draft time, the loop at ship time.** Reading [[voice-guide]] before drafting is the anchor, and it applies to every entity page. The guide also carries a *Self-check before shipping* block and a degradation table; a checklist nobody runs is not a gate, so the skills below run it.

**The sequence, and it is enforced:**

```
pyramid-structure  →  voice-draft  →  voice-edit  →  critical-reviewer
(only when the                                       (only when it carries an
 piece has an                                         argument or a
 argument to structure)                               recommendation)
```

Prose that ships is **not done and is not presented as final** until `voice-draft` and `voice-edit` have both run on it this session, in that order. Interim output is labelled "pre-edit draft", and the reply says which skills ran and what each changed. Deferring the edit pass to chase the next task is the exact failure this gate exists to stop. **Scope:** prose that ships — an `analyses/` essay, an `artifacts/` deliverable, a deep-recon output, anything leaving the wiki. **Not** `inbox/` captures or atomic `concepts/` notes, which are cheap-to-write by design and get the draft-time anchor only.

**The only exclusions:** verbatim block quotes (kept exact, in quotation marks), the top-level infrastructure files (`index.md`, `log.md`, `glossary.md`, `overview.md`, coverage matrices — mechanical catalog/record prose), and purely mechanical edits (fix a cell, rename a heading, move a section verbatim, correct a link). Third-party *quoted* text stays in its own voice; third-party ideas *restated* in a page body are the owner's to voice.

---

## Session start checklist

1. Read this file.
2. Read `wiki/index.md` **by section** — its heading outline first (`grep '^#'`), then load only the section(s) relevant to the task. Don't read the whole catalog wholesale; it's a navigable index.
3. Read only the **tail** of `wiki/log.md` (last ~5 entries, via `tail`/`grep`) — never cat the whole log. Older months live in `wiki/log/YYYY-MM.md`; consult them only if a task needs older history.
4. Ask what I want to do: `ingest`, `capture`, `query`, `lint`, or something else.

---

## Output formats

Default is a markdown page in the appropriate entity folder. Other formats on request: comparison table, doc outline, essay draft, ADR, case brief, course summary, briefing memo. Ask if it's not clear.

When an output is an applied artifact (ADR, lesson plan, exam answer, project deliverable), file it under `artifacts/{lessons,exercises,projects}/` with the matching entity type — not in `analyses/` or `concepts/`. The KB stays evergreen; artifacts live next to each other and don't crowd it.

---

## Git workflow

The wiki is a git repo. Sessions usually run inside a worktree on a branch named `claude/<slug>`. Two rules apply when committing work:

1. **Commit per logical unit of work.** A workflow step (`ingest` / `capture` / `query` / `lint` / case write-up / etc.) commits when it completes, with a message that names the workflow and the artefact. Don't accumulate unrelated changes into one commit.
2. **Push the branch to the remote, do not leave it local-only.** Whenever you commit on a `claude/*` branch, immediately push it (see the recipe below for the exact command). This makes the branch visible, reviewable from any device, and recoverable if the local worktree is lost. **A commit that only exists locally is treated as not-yet-done.**

Never push to `main` directly. Integration into `main` happens through a PR and `gh pr merge`.

### Default shipping path — the `pr-manager` agent

**When a workflow unit (`ingest` / `capture` / `query` / `lint` / case write-up / etc.) is committed and ready, ship it via the `.claude/agents/pr-manager.md` subagent by default — proactively, without being asked.** Once a unit is done and committed, invoke pr-manager on your own. It runs the full lifecycle — opens the PR, reviews it, resolves conflicts against `main`, and merges. (The session that first creates or edits the agent file is the exception — see the Note below.)

If the owner prefers a manual confirm-before-merge gate instead of full autonomy, that is set at init ({{SHIPPING_AUTONOMY}}); the agent still opens and reviews the PR but stops before merge. Absent that preference, treat a finished, committed unit as ready to ship. If you're genuinely unsure whether a unit is "done" (mid-task, half-formed, or the owner is clearly still iterating), wait — don't ship work in progress.

Guardrails the agent always keeps: it never pushes to `main` directly (merges via `gh pr merge`), and it **blocks its own merge** if its review finds a real defect.

**Review gate is content-type-aware** (the agent picks the fitting one):
- *Prose / entity pages* → the agent's wiki-convention review (frontmatter, source-first, wikilink integrity, index/log/glossary bookkeeping, orphan/secret checks).
- *Code-like artefacts* (`.claude/skills/**`, `.claude/agents/**`, `*.base`, `*.canvas`, `*.json`, scripts) → additionally the `code-review` skill.
- *Large / high-stakes changes* (new `analyses/` essay, multi-page restructure, `CLAUDE.md` rewrite) → the agent recommends a manual deeper review pass; this is the owner's call, never part of the unattended flow.

Permissions that make this possible (autonomous `git`/`gh pr` operations) live in `.claude/settings.local.json` — enablement there, behaviour here. (That file is gitignored, so each clone sets its own.)

The standard sequence after finishing a unit of work, inside a worktree:

```
git add <specific files>
git commit -m "<workflow>: <artefact>"
git push -u origin <current-branch>      # -u creates the branch on the remote + sets upstream (first push only)
# then hand off to the pr-manager agent to open → review → merge the PR
```

Note: the `pr-manager` agent only becomes invocable as a subagent in a session started *after* the agent file exists. In the session that first creates or edits it, run the same lifecycle manually.

---

## Notes

- Never guess terminology — check `glossary.md` first.
- Flag contradictions explicitly before updating.
- Prefer updating existing pages over creating new ones when content fits.
- The wiki is a git repo of markdown — everything is versioned automatically.
- Binary attachments under `wiki/attachments/` are committed normally. Keep individual images under ~500 KB and the overall attachments tree under ~500 MB. If you cross that, move to Git LFS — but don't pre-emptively set it up.
- Locale conventions: see Terminology discipline.
