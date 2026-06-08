---
title: Mermaid label list-marker gotcha
type: reference
created: 2026-06-08
updated: 2026-06-08
tags: [mermaid, diagrams, tooling, lint-reference, gotcha]
---

Why a Mermaid diagram that diffs clean and renders fine under `mmdc` still shows an **"Unsupported markdown: list"** error box in Obsidian, and how to author labels so it never does. Referenced from the Mermaid verification rule in `CLAUDE.md` (Images and diagrams → Visual verification).

## The bug

Obsidian's Mermaid renderer parses node-label text as Markdown. A label whose text **begins** with a list marker is read as the start of a Markdown list, and the whole node renders as an error box at view time:

- ordered-list marker: `N.` or `N)` then a space, e.g. `["4. Agent"]`
- bullet marker: a leading `-`, `*`, or `+` then a space

The failure is **view-time only**. A text diff never shows it, and `mmdc` (headless Method A in `CLAUDE.md`) renders the same block without complaint, so the default worktree verification cannot be trusted for this check. Only an Obsidian render (Method B) catches it.

A marker **mid-label** is safe: after a `<br/>`, or inside `<b>…</b>`. Markdown list detection fires only at the label *start*.

## The fixes

**Numbered labels → `N —` (em dash), not `N.`**
`["4. Agent"]` becomes `["4 — Agent"]`. Structural em dashes in diagram labels are house style, so this costs nothing and reads the same.

**Bullet / `+` labels where the marker carries meaning → non-breaking space**
Replace the trailing ASCII space after the marker with U+00A0 (non-breaking space). The label looks identical and no longer parses as a list. Use this when the `-`/`*`/`+` is semantically part of the label (e.g. a `+` for "added").

## Detection grep (heuristic)

No grep is authoritative — the only sure check is an Obsidian render — but this catches the common node/edge-label case before you ship:

```bash
# risky leading list-markers inside Mermaid node/edge label delimiters
rg -n '[\[({|]"?[[:space:]]*([0-9]+[.)]|[-*+])[[:space:]]' wiki/
```

Inspect each hit: is it inside a ` ```mermaid ` block, and is the marker at the label *start*? If so, apply a fix above. False positives outside Mermaid blocks are expected, since the pattern is purely lexical.

## How to verify properly

Per `CLAUDE.md` → Visual verification: in a worktree, Method A (`mmdc`) is the default, but it is blind to this bug. When a diagram has any label that could begin with a digit or a bullet, either confirm with Method B (an Obsidian render on the main checkout) or fix proactively by construction (em dash / NBSP) so the question never arises.

## Related
- `CLAUDE.md` → Images and diagrams → Visual verification (the condensed rule and its placement)
