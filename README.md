# EA LLM Wiki — foundation

A reusable scaffold for an **enterprise architect's personal knowledge base**, maintained in the [Karpathy LLM-wiki tradition](https://gist.github.com/karpathy/1dd0294ef9567971c1e4348a90d69285): low-friction notes that compound through re-reading and re-asking, written and maintained by an LLM agent ([Claude Code](https://claude.com/claude-code)) against a single operating manual, [`CLAUDE.md`](CLAUDE.md).

This repo is the **starting point**, not a finished wiki. It ships the structure, the four workflows, the EA-discipline domain taxonomy, the Obsidian vault config, the skills, and a voice-guide template — but no content, and no owner. You make it yours by running the initialisation interview once.

## Start here — run the init interview

```
# in Claude Code, in this repo:
/init-wiki
```

`/init-wiki` (protocol in [`INIT.md`](INIT.md)) interviews you — who you are, what the wiki is for, which EA disciplines you work across, your locale and confidentiality posture — then rewrites `CLAUDE.md`, `README.md`, `wiki/domains.md`, and the voice guide in place and removes the foundation placeholders. It hands the voice work to the `voice-interview` skill, which measures your real writing. Run it once; then delete `INIT.md` and the `init-wiki` skill.

Until you run it, the `{{PLACEHOLDER}}` values in `CLAUDE.md` are generic defaults for a generalist EA.

## What this is for

The wiki's primary, always-on job is to be your compounding knowledge base on enterprise architecture and the topics around it. It can serve **secondary jobs** too — a portfolio/evidence body for a certification or degree, a team reference, a consulting pattern library, course study — chosen during init and carried by tags, not by a separate directory tree.

## Operating manual

The wiki is driven by Claude Code against [`CLAUDE.md`](CLAUDE.md), the canonical operating manual — entity types, page format, tagging conventions, image/diagram rules, and the four workflows (`ingest`, `capture`, `query`, `lint`). Read `CLAUDE.md` before touching the wiki.

## Layout

```
raw/                    # source documents, read-only (gitignored)
wiki/
  index.md              # catalog of pages
  log.md                # append-only activity log
  overview.md           # cross-wiki synthesis (rewritten during lint)
  glossary.md           # living terminology + alias bridge
  domains.md            # EA-discipline domain taxonomy
  coverage.md           # materialised domain-coverage matrix (rewritten during lint)
  coverage.base         # live Bases dashboard companion to coverage.md
  _resources/           # infrastructure (voice-guide.md)
  inbox/                # quick-capture notes pending triage
  sources/              # one page per raw document
  concepts/             # atomic notes, one idea per page
  frameworks/           # named methodologies (TOGAF, ArchiMate, DAMA-DMBOK, …)
  questions/            # open questions — first-class, drive gap detection
  cases/                # real-world or hypothetical cases
  analyses/             # essay-length syntheses
  artifacts/            # things you produce (lessons / exercises / projects)
  attachments/          # binary images, mirrored by entity type
```

## Working with it

Browse the wiki in [Obsidian](https://obsidian.md/) — the `wiki/` folder is an Obsidian vault. Drive ingest / capture / query / lint via Claude Code; it reads `CLAUDE.md` and asks which workflow you want.

## Local setup

Clone, install a small set of prerequisites plus two Obsidian community plugins, open in Obsidian, and everything renders. On macOS the path of least friction is via [Homebrew](https://brew.sh/). (The plugins and the PlantUML JAR are **not** committed to this repo — they are third-party code under their own licenses; you install them once, as below.)

> [!tip] Automated path — `setup.sh` (macOS) / `setup.ps1` (Windows)
> After cloning, run the setup script from the repo root. It installs the prerequisites, the PlantUML JAR, and the two community plugins, idempotently. Run with `--check` first to see what's already present (changes nothing).
>
> **macOS / Linux:**
> ```bash
> ./setup.sh --check     # then: ./setup.sh
> ```
> Flags: `--skip-brew`, `--skip-plugins`, `--skip-skills`, `--skip-mermaid`, `--help`.
>
> **Windows (PowerShell):**
> ```powershell
> .\setup.ps1 --check    # then: .\setup.ps1
> ```
> Uses `winget` for prerequisites. If the script is blocked, run `powershell -ExecutionPolicy Bypass -File .\setup.ps1`. Flags: `--skip-winget`, `--skip-plugins`, `--skip-skills`, `--skip-mermaid`, `--help`.
>
> The numbered steps below are the manual macOS equivalent if you'd rather do it by hand. On every platform you still finish in the Obsidian GUI: turn off Restricted Mode and enable the two plugins (step 6).

### 1. Install the prerequisites

```bash
brew install --cask obsidian
brew install git gh openjdk graphviz
```

- **Obsidian** — the vault browser (the repo is an Obsidian vault under `wiki/`).
- **git / gh** — version control and PR lifecycle (the `pr-manager` agent uses `gh`).
- **OpenJDK** — runs the PlantUML JAR for ArchiMate / C4 diagrams (you download the JAR once in step 6).
- **GraphViz** — required for ArchiMate / class / ER / activity diagrams (sequence diagrams skip it).

### 2. Link OpenJDK so macOS can find it

The macOS Java shim only sees JDKs registered under `/Library/Java/JavaVirtualMachines/`, so symlink the brew install once:

```bash
sudo ln -sfn "$(brew --prefix openjdk)/libexec/openjdk.jdk" /Library/Java/JavaVirtualMachines/openjdk.jdk
java -version   # should print the OpenJDK version, not "Unable to locate a Java Runtime"
```

### 3. Install Claude Code

Claude Code drives the four workflows. Install per [claude.com/claude-code](https://claude.com/claude-code).

### 4. Optional — defuddle CLI

Only needed for the `defuddle` skill (cleans web-page clutter before ingest):

```bash
brew install node && npm install -g defuddle
```

### Without Homebrew

Direct installers: [Obsidian](https://obsidian.md/download), [Eclipse Temurin OpenJDK](https://adoptium.net/) (its `.pkg` registers itself — no symlink step), [git](https://git-scm.com/download/mac), [gh](https://cli.github.com/), [Node.js](https://nodejs.org/). GraphViz has no official macOS installer — brew or [MacPorts](https://www.macports.org/) is the practical path.

### 5. Clone and open the vault

```bash
git clone <repo-url> ea-llm-wiki
cd ea-llm-wiki
open -a Obsidian wiki/      # vault root is wiki/, NOT the repo root
```

The vault root is **`wiki/`**. The `.obsidian/` config (which plugins to enable, the PlantUML SVG/local-JAR settings, core-plugin selections) lives there. Opening the repo root creates a fresh empty vault and misses everything. On first open, Obsidian prompts to **trust author and enable community plugins** — accept. The plugins themselves are not in the repo, so install them next.

### 6. Install the two community plugins and the PlantUML JAR

The scaffold commits its plugin *settings* but not the plugin *code* (third-party, under their own licenses). Install once:

```bash
# PlantUML JAR (~28 MB, GPLv3) — download to the path data.json already points at:
LATEST=$(gh api repos/plantuml/plantuml/releases/latest -q '.tag_name')
curl -sSL -o wiki/.obsidian/plantuml/plantuml.jar \
  "https://github.com/plantuml/plantuml/releases/download/${LATEST}/plantuml-${LATEST#v}.jar"
```

Then in Obsidian: **Settings → Community plugins → Browse**, and install **PlantUML** (by joethei) and **Smart Connections** (by brianpetro). They are already listed in `community-plugins.json`, so once installed they enable with the committed settings (SVG output, local-JAR path, no public-server round-trip). Restart Obsidian. See [`wiki/.obsidian/plantuml/README.md`](wiki/.obsidian/plantuml/README.md) for the JDK symlink and troubleshooting.

### What ships in the repo

- **Obsidian config** under `wiki/.obsidian/` — which plugins to enable (`community-plugins.json`), PlantUML settings (`obsidian-plantuml/data.json`), core-plugin selections (Bases, Daily Notes, Properties, …). The plugin *code* and the PlantUML JAR are **not** committed — see step 6.
- **The wiki's own Claude Code skills** under `.claude/skills/` (`init-wiki`, `voice-interview`, `deep-recon`) and the **`pr-manager` agent** under `.claude/agents/`.
- **All authoring conventions** in `CLAUDE.md`.

### What you install separately (third-party, own licenses)

- **PlantUML JAR** — GPLv3; download per step 6.
- **`obsidian-plantuml` and Smart Connections plugins** — from Obsidian's community plugin browser.
- **Obsidian Agent Skills** (`obsidian-markdown`, `obsidian-bases`, `obsidian-cli`, `json-canvas`, `defuddle`) — from [`kepano/obsidian-skills`](https://github.com/kepano/obsidian-skills) (MIT). The setup script clones them into `.claude/skills/` (gitignored); or run `/plugin marketplace add kepano/obsidian-skills` in Claude Code.

### What stays per-machine (gitignored)

- `raw/` — source documents (mirror via your own backup if you want them on multiple machines).
- `wiki/.obsidian/workspace.json` — per-machine UI state.
- `wiki/.smart-env/` — Smart Connections runtime embeddings, regenerated on demand.
- `.claude/settings.local.json` — local permissions for the autonomous git/PR flow.
- Brew-installed system tools, the Obsidian app, and the Claude Code CLI.

### Verifying the setup

```bash
java -version
dot -V
```

Both should print version lines. Then in Obsidian, open any page with a PlantUML ArchiMate block — it should render as a diagram with no perceptible network spinner. If you see raw `@startuml` source instead, fully quit and reopen Obsidian so the plugin re-reads its `data.json`, and confirm `java -version` / `dot -V` work in your terminal.

## Lineage

Built on [Andrej Karpathy's LLM wiki pattern](https://gist.github.com/karpathy/1dd0294ef9567971c1e4348a90d69285), via [Balu Kosuri's scaffolding](https://github.com/balukosuri/llm-wiki-karpathy). This foundation specialises the pattern for **enterprise architects**: the EA-discipline domain taxonomy, ArchiMate/C4 diagram support, a business-deliverable voice guide, and the four-workflow operating manual. The ethos — atomic notes, dense linking, lint-driven compounding — is unchanged.

## License

Copyright 2026 Andy Nieubourg. Licensed under the **Apache License, Version 2.0** — see [`LICENSE`](LICENSE).

This license covers the scaffold itself: the operating manual (`CLAUDE.md`), the workflows, the directory structure, the domain taxonomy, the skills under `.claude/skills/`, the `pr-manager` agent, the voice-guide *template*, and the Obsidian config authored here. It does **not** cover the third-party tools the wiki depends on (the PlantUML JAR under GPL, and the `obsidian-plantuml` / Smart Connections plugins) — those are installed separately, not redistributed here, and retain their own licenses. See [`NOTICE`](NOTICE).

Any wiki *content* you create after running `/init-wiki` (your `wiki/` pages, attachments, and personalised voice guide) is yours and is not part of this licensed scaffold. Keep that content in a **separate, private** repository if it derives from client work — `raw/` is gitignored precisely so source documents never enter version control, but derived pages can still carry confidential material.
