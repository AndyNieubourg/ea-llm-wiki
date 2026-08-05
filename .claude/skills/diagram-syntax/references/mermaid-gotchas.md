# Mermaid gotchas

Hand-written companion to the vendored upstream references in `references/mermaid/`. Those files document what Mermaid supports. This file documents what breaks, in the two renderers that matter here: Obsidian (the vault's live renderer) and `mmdc` (the headless check).

Section 1 is written from this wiki's own lesson page. The section 2 table comes from [tractorjuice/arc-kit](https://github.com/tractorjuice/arc-kit) (MIT). Section 3 is mined from the vendored upstream references.

---

## 1. Obsidian node labels and the "Unsupported markdown: list" trap

The most important entry on this page. It is Obsidian-specific, upstream does not document it, and `mmdc` does not catch it.

**Symptom.** A node renders as a grey box reading **"Unsupported markdown: list"** instead of its label text. The rest of the diagram draws normally. A text diff never catches it: the source looks correct, and the error appears only when Obsidian renders the page.

**Cause.** Obsidian's Mermaid renderer (v10+) parses node-label text as Markdown. A label whose text **begins** with a Markdown list marker is read as a list item, which Mermaid cannot draw inside a node:

- ordered: `N.` or `N)` then a space, for example `["4. Agent / NLQ surface"]`
- bullet: a leading `-`, `*`, or `+` then a space, for example `[+ Strategy Development]`

Only the **start** of the label triggers it. A marker mid-label renders fine: after a `<br/>`, or shielded by an HTML tag such as `<b>1. ...</b>`. That is why `["Gold tables<br/>Redshift"]` is safe while `["1. Metadata"]` is not.

**Fix.**

| Case | Rule | Before | After |
|---|---|---|---|
| Numbered label | Replace `N.` with `N —`. Structural em dashes in diagram labels are house style. | `["4. Agent"]` | `["4 — Agent"]` |
| Bullet or `+` where the marker carries meaning | Replace the trailing ASCII space with a non-breaking space (U+00A0). Identical glyph, identical look, no longer parses as a list. | `"+ Retire"`, an ASCII space after the `+` | `"+ Retire"`, a literal U+00A0 after the `+`. Copy the character, do not type the escape text. Verify with `python3 -c "print(open(f).read().count(chr(0xa0)))"`. |
| General | Never start a node label with `N.`, `N)`, `-`, `*`, or `+` followed by a space. | | |

**Detection grep.** Run before shipping or exporting, then discard the false positives (markers after `<br/>` or inside `<b>`):

```bash
rg -n '(\[\(?|\(\(?|\{\{?)"?([0-9]+[.)]|[-*+]) ' --glob '*.md' wiki/
```

**Why the headless check misses it.** `mermaid-cli` renders the broken label without complaint. Only an Obsidian render reproduces the bug, so a page carrying numbered or bulleted node labels needs an Obsidian render before it is called done.

**Scale.** One broken diagram triggered a vault scan that found the same trap on 22 pages and 109 labels, numbered process diagrams above all (seven-step methodologies, principle lists, capability-planning steps). Systematic, not a one-off.

---

## 2. Common syntax gotchas

The errors that recur most when a diagram is generated rather than hand-typed.

| Gotcha | Problem | Fix |
|--------|---------|-----|
| `<br/>` in flowchart edge labels — **not** a gotcha here | The upstream table claimed the flowchart parser rejects HTML in edge labels. False on `mmdc` 11.15.0: `A["A"] -->\|"Uses<br/>HTTPS"\| B["B"]` renders as a clean two-line label, verified by render, and the unquoted form gives a byte-identical PNG | Use `<br/>` when the edge label reads better on two lines. Obsidian's bundled Mermaid build was not tested, so render such a page in Obsidian before shipping it |
| `end` as node ID | `end` is a reserved keyword in Mermaid | Use a different ID: `EndNode["End"]` |
| Gantt date formats | Gantt requires a specific date format | Use `YYYY-MM-DD`, for example `2026-01-15` |
| Gantt task status | Invalid task status keywords | Valid: `done`, `active`, `crit`, `milestone` |
| Parentheses in labels | Unescaped `()` breaks node parsing | Wrap in quotes: `Node["Label (with parens)"]` |
| Special chars in IDs | Hyphens, dots, spaces in node IDs | Use camelCase or underscores: `apiGateway`, `api_gateway` |
| Missing semicolons in ER | ER attributes need a specific syntax | Follow the `entity { type name }` pattern |
| Subgraph naming | Subgraph IDs with spaces need quotes | `subgraph "My Group"` |

---

## 3. Further traps in the upstream references

Collected from the vendored files. Each one is documented upstream but easy to miss.

### The word `end`

Lowercase `end` breaks a flowchart, because it closes a `subgraph`. Capitalise any letter (`End`, `END`) or pick a different ID. In a sequence diagram the same word can break the parse: if it is unavoidable, enclose it in parentheses, quotes, or brackets, so `(end)`, `"end"`, `[end]`, `{end}`.

### Quote first, escape second

Wrap any label containing Unicode, punctuation, or shape-delimiter characters in double quotes: `id["This ❤ Unicode"]`. Quoting is the general defence against a label breaking the parser. For characters that quoting alone will not carry, use HTML entity codes (`#quot;`, `#35;`), the escape mechanism the sequence-diagram reference documents.

### Markdown strings versus `<br/>`

Double quotes plus backticks give a Markdown string: ``markdown["`This **is** _Markdown_`"]``. Markdown strings wrap long text automatically and take a literal newline for a line break, so they remove the need for `<br/>` inside node labels. They pair with `htmlLabels: false`. **Node** labels take `<br/>` or a Markdown string. **Flowchart edge** labels take `<br/>` too: tested on `mmdc` 11.15.0, `A["A"] -->|"Uses<br/>HTTPS"| B["B"]` renders as two lines, quoted and unquoted forms producing a byte-identical PNG. The behaviour of Obsidian's own bundled Mermaid build was not tested, so a page whose meaning depends on a multi-line edge label needs an Obsidian render before it is called done.

### ER diagram specifics

Entity, relationship, and attribute names accept Unicode and accept spaces when wrapped in double quotes. Keys (`PK`, `FK`, `UK`) accept neither Markdown nor Unicode. An attribute comment is a double-quoted string at the end of the attribute, and it cannot itself contain a double quote.

### Mindmap indentation

Hierarchy comes from relative indentation, not from any fixed step. Ambiguous indentation does not error: Mermaid resolves the node to the nearest ancestor with smaller indentation and draws something plausible but wrong. Keep indentation strictly consistent per level. Mindmap remains an experimental diagram type upstream, and the `::icon()` syntax depends on icon fonts the renderer must supply, so icons are not portable.

### Interaction directives are inert here

`click` bindings on class-diagram nodes and Gantt tasks need `securityLevel: 'loose'`. Vault and export renderers run strict. Treat every diagram as static and put the link in the surrounding prose instead.
