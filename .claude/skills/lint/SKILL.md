---
name: lint
description: "Periodic re-reading and integrity pass over the whole wiki. Use when the owner asks to run a lint, weekly, or after a batch of ingests. Do NOT use to process a single new source, which is ingest."
user-invocable: true
---

# `lint` — periodic re-reading pass

> Four workflows: `ingest`, `capture`, `query`, `lint`. At any moment, you are in exactly one.

The compounding workflow. Run weekly, after a batch of ingests, or on demand. Start with the pre-flight audit (below), then two phases.

**Phase 1: synthesis (forward).**
- Re-read recent additions (use `log.md` to scope).
- Triage `inbox/`: promote notes to proper entity pages, merge into existing pages, or drop.
- Rewrite `overview.md` deliberately, with breadth, not as a patch.
- Surface synthesis candidates: concept clusters with enough linked notes to earn an essay in `analyses/`.

**Phase 2: integrity and gaps (backward).**
- Contradictions between pages.
- Stale claims superseded by newer sources.
- Orphan pages (no inbound links).
- Missing concept pages (terms used but undefined).
- Missing cross-references that should exist.
- Terminology drift across pages.
- **Gap detection on `questions/`:**
  - *Starved*: questions with zero or low linked notes; no source has informed them yet.
  - *Blocked*: questions stuck at `open` despite many linked notes; ideas aren't converging, need a writing pass.
  - *Converging*: questions whose notes cluster across sources; possible essay candidates.
  - *Systemic gaps*: recurring `gap` strings across multiple question pages; persistent blind spots.
- **Rumination candidates**: questions whose `last-ruminated` date is old enough to warrant re-asking. The staleness shortlist (routed check 2 below) generates the list.
- **Log rotation**: if `wiki/log.md` holds entries from more than the current month, roll each completed month into `wiki/log/YYYY-MM.md`, leaving the current month plus a one-line pointer block to the archive in `log.md`. Keeps the file the session-start checklist reads small; append-only growth otherwise pushes it past 1 MB.
- **Diagram checks**: the lint additions in `.claude/rules/diagrams.md` (orphan attachment folders, broken embeds, repo-size delta, Mermaid-candidate scan).
- **Skills-table drift check**: the Skills table in `CLAUDE.md` is hand-maintained and silently drifts from the skills that actually exist. Run from the repo root:

  ```bash
  diff <(ls .claude/skills/ | sort) <(grep -E '^\| (⬇ )?`[a-z][a-z-]*`' CLAUDE.md | sed -E 's/^\| (⬇ )?`([a-z-]+)`.*/\2/' | sort -u)
  ```

  Silence is a pass. A `<` line is a skill on disk with no table row; a `>` line is a row for a skill that is absent. Fix the table for the first. For the second, either run `setup.sh` (if it is a ⬇ installed skill) or investigate why a committed skill is gone. The `session-start.sh` hook reports the declared-but-missing half of this automatically at session start; the lint check adds the reverse direction (present-but-undeclared).
- **Domain coverage scan**: for each `#domain:<name>` tag listed in [[domains]]. **Rebuild `wiki/coverage.md`** from this scan as a materialised matrix; `wiki/coverage.base` is the live companion view. Per-domain metrics (counts alone are weak signal, so track the relative and qualitative dimensions too):

  | Metric | Definition | Why it matters |
  |---|---|---|
  | **Pages (N)** | Count of unique pages carrying the tag, across `concepts/ sources/ frameworks/ analyses/ cases/ artifacts/`. | Absolute volume, the anchor metric. |
  | **Δ since last lint** | Net change in N since the previous scan. | Direction of travel. |
  | **% of domain-tagged corpus** | N ÷ Σ(N across all domains). Sum exceeds 100% because multi-domain pages are counted in each tag. | Relative weight. Surfaces over- and under-represented domains independent of total wiki size. |
  | **% of vault** | (unique pages tagged with this domain) ÷ (total wiki pages, excluding `inbox/`). | Emphasis vs. the whole. |
  | **Entity mix** | Breakdown across {concept, source, framework, analysis, case, artifact}. Both counts and %. | A domain that's 80% sources and 5% concepts is reading-heavy and atomisation-light. |
  | **Concept share** | concepts ÷ N. | Atomic-note density. Low = passive ingest only; high = active synthesis. |
  | **Source diversity** | Distinct `sources/` pages contributing. Flag any domain depending on <3 sources for ≥30% of pages (single-source risk). | Robustness of the cluster. |
  | **Analyses count** | `analyses/` pages tagged with this domain. | Synthesis pressure released. |
  | **Synthesis lag** | (analyses ÷ N), inverted. High = lots of material, little synthesis. The `dense`/`over-saturated` buckets with zero analyses are the urgent ones. | Earns or doesn't earn the over-saturated label. |
  | **Cross-domain bridges** | Pages tagged with this domain AND ≥1 other. Both count and as % of N. | High = the domain integrates; low = it's a silo. |
  | **Confidence profile** | Among `concepts/` and `analyses/`: split across {settled, working, speculative, single-source, unmarked}. Default-omitted pages count as the implicit `settled` per the Relationships taxonomy convention. | Quality signal. |
  | **Crystallisation closure** | Among `concepts/` and `sources/` pages in synthesised clusters: count with `crystallized-into:` populated. | Lint integrity; closes the loop on completed analyses. |
  | **Question health** | Linked `questions/` page status (open / converging / answered / dropped), `gap:` populated or empty, days since `last-ruminated`. | Active-inquiry signal. |
  | **Recency** | Most recent `updated:` across the domain's pages; days since. | Staleness signal. |
  | **Status (2D)** | Volume × Synthesis. **starved** (N<25 AND source-diversity<3 AND analyses=0) / **forming** (N<25, growing or has ≥1 analysis) / **balanced** (N 25–49) / **synthesis-ripe** (N≥50 AND analyses<2) / **healthy-saturated** (N≥50 AND analyses≥2). | Surfaces synthesis lag distinctly from raw volume. |

  Volume-only bucket thresholds (kept as input to the 2D status, also reported alongside it for continuity): **thin** <25, **balanced** 25–49, **dense** 50–69, **over-saturated** 70+. Re-tune if dispersion shifts substantially or the owner's domain set differs in size.
- **Relationship-frontmatter audit**: scan prose for phrases that imply a structured relationship missing from frontmatter ("supersedes Kaiser 2019", "contradicts Strengholt's claim", "derived from cluster X") and propose `relationships:` additions. Pair with the crystallization-closure check below.
- **Crystallization closure**: when an `analyses/` page exists, ensure each source concept has `crystallized-into:` pointing back to it. Same for `synthesised-into:` on the question that motivated the analysis. Closes the loop on completed synthesis work so future `query` sees it immediately.

Propose fixes, rumination candidates, and synthesis candidates. Apply what the owner confirms. **Before writing the log entry, run `python3 scripts/lint-aggregates.py` and paste its numbers.** Every count the entry restates (inbox delta, per-directory page counts, ruminated N of M, question `status:` moves, files added / modified / deleted) comes from that output, never from memory: hand-written lint counts drift. Append to `log.md`:

```
## [YYYY-MM-DD] lint
Synthesis: ...
Integrity issues: ...
Gaps (starved / blocked / converging / systemic): ...
Rumination candidates: ...
Fixes applied: ...
```

## Pre-flight (run before committing, and at the head of every lint)

`scripts/preflight.py` runs the mechanical checks a reviewer would otherwise catch by hand: frontmatter that does not parse or lacks a required key, wikilinks and `![[attachments/...]]` embeds that resolve to nothing, links into pages the change set removed, and an entity page edited today whose `updated:` says otherwise. It takes about a second on the whole vault. On a branch it exits non-zero only on findings the branch introduced: it runs the same checks on the merge-base copy of each changed file, prints what was already there as inherited, and does not count it. `--all` counts every finding. It needs PyYAML (`pip install pyyaml`) and exits 2 rather than pass when it is missing.

```bash
python3 scripts/preflight.py            # files changed against origin/main, introduced findings only
python3 scripts/preflight.py --strict   # same files, every finding counts
python3 scripts/preflight.py --all      # whole-vault audit, for lint
```

**Do not filter its output and call the remainder clean.** A filtered scan reported as an unfiltered one is a false "clean".

**After retracting or correcting any claim, sweep for its restatements before committing:**

```bash
python3 scripts/preflight.py --claim "the exact phrase you just retracted"
```

A claim corrected in one place and left standing in others is the commonest way a wiki contradicts itself. The sweep covers `index.md`, `log.md` and `glossary.md` deliberately. Each hit is then a judgement: a dated log entry keeps what it believed on the day, and a correction note has to be true now.

`scripts/lint-aggregates.py` sits beside it: read-only, dependency-free, it derives the log entry's aggregates from the tree and the diff against `origin/main`. It gates nothing. `--base R1 --head R2` reproduces a historical state.

## Routed checks (deterministic, run every lint)

Every lint pass runs these two commands from the repo root. Each is deterministic. Nothing fires them unattended; this workflow names them and the lint pass runs them.

**1. Path-exists.** Every plain backtick-quoted repo path in `CLAUDE.md` resolves on disk or in `git ls-files`; a path that exists on disk but is gitignored is flagged separately, because a session reads the pointer and a clone gets no target. Silence is a pass. The filter checks plain paths only: globs, `<placeholders>`, spaced command lines, ellipses, URLs and the allowlisted entries never reach the check, so a dangling path in one of those shapes passes silently. Other blind spots: unbackticked prose mentions, `[[wikilinks]]`, and a path that exists on disk while untracked and unignored. A path that exists is resolved through its symlinks before git sees it, because git refuses a path beyond a symbolic link and the negation in the chain would turn that refusal into a silent pass.

```bash
grep -o '`[^`]*`' CLAUDE.md | tr -d '`' \
| grep -E '^(wiki|\.claude|scripts|raw)/' \
| grep -vE '[*?<>{}]|[[:space:]]|…|YYYY|://' \
| grep -v -x -e '.claude/settings.local.json' -e 'wiki/.smart-env/' \
    -e 'wiki/.obsidian/plantuml/plantuml.jar' -e 'wiki/.obsidian/plugins/smart-connections/' \
    -e 'wiki/attachments/sources/strengholt-medallion-ch03/medallion-overview.png' \
| sort -u \
| while IFS= read -r p; do
    if [ -e "$p" ]; then
      q=$(python3 -c 'import os,sys; print(os.path.relpath(os.path.realpath(sys.argv[1])))' "$p")
      git ls-files --error-unmatch -- "$q" >/dev/null 2>&1 || ! git check-ignore -q -- "$q" \
        || printf '%s\texists but untracked/ignored\n' "$p"
    else
      git ls-files --error-unmatch -- "$p" >/dev/null 2>&1 || printf '%s\tmissing\n' "$p"
    fi
  done
```

The five `-x` allowlist entries, each with its justification: `.claude/settings.local.json` and `wiki/.smart-env/` are documented in `CLAUDE.md` *as* gitignored machine-local state, so either arm of the check would trip on them by design; `plantuml.jar` and the `smart-connections/` plugin folder are third-party code the owner installs separately and the repo deliberately does not redistribute; the `medallion-overview.png` path is an "e.g." illustration of the attachment naming convention, not a claim the file exists. A new allowlist entry gets its justification added to this paragraph in the same edit, or it is drift.

**2. Staleness shortlist.** Feeds Phase 2 the 15 pages with the oldest `updated:` plus every `questions/` page whose `last-ruminated:` is more than 60 days old. Scope: the six KB entity folders only; `wiki/artifacts/`, `wiki/inbox/` and the top-level pages stay out by design (artifacts are done-and-referenced, the inbox has its own triage, the top-level files are rewritten during lint anyway). It ranks re-reading and judges nothing: an old page can be old and correct. When many pages tie at the oldest date, the 15-row cut truncates inside the tie alphabetically; take the whole tie when Phase 2 has the budget. A `questions/` page with no `last-ruminated:` field never appears, which is a blind spot, not a pass.

```bash
python3 - <<'PY'
import os, re, datetime
roots = ['wiki/sources','wiki/concepts','wiki/frameworks','wiki/analyses','wiki/questions','wiki/cases']
def fm(path):
    d = {}
    lines = open(path, encoding='utf-8').read().splitlines()
    if not lines or lines[0].strip() != '---': return d
    for ln in lines[1:]:
        if ln.strip() == '---': break
        m = re.match(r'(updated|last-ruminated):\s*["\']?(\d{4}-\d{2}-\d{2})', ln)
        if m and m.group(1) not in d: d[m.group(1)] = m.group(2)
    return d
pages = [(os.path.join(dp, f), fm(os.path.join(dp, f)))
         for root in roots for dp, _, fs in os.walk(root) for f in sorted(fs) if f.endswith('.md')]
for date, p in sorted((d['updated'], p) for p, d in pages if 'updated' in d)[:15]:
    print(f'{date}\t{p}')
cut = (datetime.date.today() - datetime.timedelta(days=60)).isoformat()
for date, p in sorted((d['last-ruminated'], p) for p, d in pages
                      if p.startswith('wiki/questions') and 'last-ruminated' in d and d['last-ruminated'] < cut):
    print(f'{date}\t{p}')
PY
```
