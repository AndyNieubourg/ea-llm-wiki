# Ingest coverage manifest — design note

**Status: optional tool, shipped dormant.** The generator works; it is **not wired into the `lint`/`ingest` workflows** by default. Activate it when a full-corpus "ingest everything not ingested" sweep becomes a recurring need (see *Activation* below). Until then it is a convenience: run it before a sweep instead of re-grepping the whole corpus.

## What it is

`ingest-coverage.tsv` is a generated index of every file under `raw/`, recording for each: a content hash, size, type, and whether it is already reflected in a wiki page's `sources:` frontmatter. `ingest-coverage.py` builds it.

It exists because reconstructing "what's already ingested" with a filename grep is fragile and expensive: in the wiki this scaffold was cut from, one sweep burned ~20 tool calls on it and mis-flagged about half its hits (files bundled into a parent page, or listed under a reworded title). The `sources:` frontmatter is the real record of truth; this manifest just materialises it against `raw/` so the answer is a lookup, not a search.

## Why generated, not hand-maintained

A hand-curated inventory is a second source of truth and drifts the moment one ingest forgets to update it — a stale list yields confident false negatives, worse than no list. This manifest is **derived** (rebuilt from `raw/` + `sources:` fields), so it cannot silently rot. Same pattern as `coverage.md`.

## Why `wiki/_resources/`, not `raw/`

`.gitignore` is `raw/*` + `!raw/.gitkeep`. A manifest inside `raw/` would be **uncommitted and invisible inside `claude/*` worktrees** (where `raw/` is empty). Committing it under `_resources/` is the only way a worktree session sees `raw/` coverage without reaching the absolute main-checkout path.

## Status semantics — honest by design

| status | meaning | action |
|---|---|---|
| `ingested` | basename is in some page's `sources:` array | trustworthy — leave it |
| `mentioned` | basename appears in wiki text but **not** a `sources:` array | fix the page's `sources:` (convention gap), **or** it is an index-only page that deliberately lists titles in the body — verify before acting |
| `unreferenced` | basename appears nowhere in the wiki | **candidate** to ingest — verify first (may be a reworded title or a file folded into a parent page) |
| `asset` | non-source type (image / url / css / zip / …) | not assessed; size only, no hash |

`unreferenced` is a **candidate, never a verdict** — reworded titles and multi-file parent pages produce false positives. Always confirm before claiming a file is un-ingested ("absence is a claim").

## The hash — change detection

Presence-only coverage misses the case that matters most for a living KB: a source that **changed** since it was ingested (re-exported deck, new edition, updated paper). The `sha256_16` column fixes that. On re-run, the generator compares each file's hash to the prior committed manifest and sets the `changed` column:

- `new` — not in the prior manifest (first sighting)
- `no` — hash unchanged since last run
- `yes` — **hash changed → the source was updated**; consider re-ingesting and recording a `supersedes` / `superseded-by` relationship on the affected page

A re-run that reports `changed-since-last: N` is the signal to revisit those N pages.

## Columns

`status` · `sha256_16` (first 16 hex of sha256; blank for assets) · `bytes` · `ext` (`arxiv` for extensionless arXiv-id files) · `top_folder` · `relpath` · `changed` · `referenced_in` (wiki page(s) listing it in `sources:`)

## Usage

```bash
# from the MAIN checkout (raw/ populated, files local):
python3 wiki/_resources/ingest-coverage.py

# from a claude/* worktree (raw/ is empty here) — point --raw at the main checkout:
python3 wiki/_resources/ingest-coverage.py \
  --raw "/abs/path/to/main-checkout/raw" --wiki wiki

# fast presence-only (skips hashing):
python3 wiki/_resources/ingest-coverage.py --no-hash
```

Quick reads:

```bash
# real un-ingested candidates, by folder
awk -F'\t' '$1=="unreferenced"{print $5}' wiki/_resources/ingest-coverage.tsv | sort | uniq -c | sort -rn

# convention gaps to fix (mentioned but not in sources:)
awk -F'\t' '$1=="mentioned"{print $6}' wiki/_resources/ingest-coverage.tsv

# sources that changed since last manifest
awk -F'\t' '$7=="yes"{print $6}' wiki/_resources/ingest-coverage.tsv
```

## Known limitations

- **Reworded / index-only references** are not auto-resolved → they surface as `mentioned` or `unreferenced` and need a human/Claude check. Tightening the `sources:` convention (CLAUDE.md, Page format) shrinks this set over time.
- **Hashes need local files.** From a cloud-synced folder, online-only files read slowly or error (`READERR`); run from the main checkout with the working set local, or use `--no-hash`.
- **Snapshot, not live.** Regenerate after an ingest or at lint; a stale manifest is informational, not authoritative — the `sources:` fields remain the truth.

## Activation (when a sweep recurs)

1. Add a `lint` Phase-2 step: regenerate the manifest from the main checkout, commit the diff, and act on `changed=yes` (re-ingest) and `unreferenced` (triage) rows.
2. Add an `ingest` closing step: after filing pages, regenerate so the new `sources:` entries flip their raw files to `ingested`.

Both are one-line workflow additions; deferred until the recurring need is real, to avoid maintaining machinery for a rare operation.

## Related

- CLAUDE.md → *Page format* (`sources:` completeness rule) — the convention this manifest rewards
- `coverage.md` — the materialised-view pattern this follows
