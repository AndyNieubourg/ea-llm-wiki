# Rendering and verification

A diagram is not done until a render has been observed. A malformed block shows as an error box only at view time, and a text diff never catches it. So every diagram you author or materially edit gets rendered and looked at before it ships.

Never claim a render you have not read. This is the diagram form of the wiki's "absence is a claim" rule.

---

## Track selection lives in one place

Not here. `SKILL.md` section 1 carries the single routing table, and it restates the project `CLAUDE.md`, which wins on any divergence. Do not add a second copy to this file: three copies of the track rule is how the earlier draft ended up contradicting itself.

What this file owns is what happens **after** the track is chosen. Two of the four tracks produce something to render and read: Mermaid via `mmdc`, PlantUML via the local jar. A designed SVG (track 3) is verified with `rsvg-convert` before commit. A committed raster (track 4) has nothing to verify, only to compress and crop.

---

## Method A: headless render

**The default, and the only concurrency-safe one.** Renders the file on your branch with no Obsidian involved, so parallel worktrees do not collide. This is what you use in a worktree, which is the usual case.

### Mermaid

Write the block body, without the ```` ```mermaid ```` fence, to a temp path outside `wiki/`:

```bash
mmdc -i /tmp/diagram.mmd -o /tmp/diagram-check.png
```

`mmdc` prints `Generating single mermaid chart` on success and a parse error with a line number on failure. It writes no PNG when parsing fails, so a missing output file is itself the signal.

### PlantUML

Write the whole `@startuml…@enduml` block to a temp path outside `wiki/`:

```bash
java -jar wiki/.obsidian/plantuml/plantuml.jar -tpng /tmp/diagram.puml
```

Use `-tsvg` to match the vault default when you want to check how it will actually appear. PlantUML **always writes an output file**, even on failure: a syntax error produces a green-on-black image carrying the message `Some diagram description contains errors` and the offending line. So checking that the file exists proves nothing. You have to read it.

### The loop, in full

1. Write the block body to `/tmp/<name>.<ext>`. **Never inside `wiki/`**, and never inside a staging or skill directory.
2. Run the render command above.
3. `Read` the resulting PNG. Did it draw the elements you expected, or is it an error box, an empty canvas, or a diagram missing half its nodes?
4. Delete the temp files. They are tool scratch and do not belong in the vault.

Step 3 is the whole point. Steps 1, 2 and 4 without step 3 are not verification.

---

## Method B: Obsidian live-vault screenshot

Interactive, main-checkout only. Use it to see the diagram in page context, and to catch the one failure Method A cannot.

1. **Gate first.** The CLI depends on a running Obsidian:

   ```bash
   pgrep -x "Obsidian" >/dev/null && echo "Obsidian running" || echo "Obsidian not running — skip CLI"
   ```

   Not running means fall back to Method A. Do not try to start it.

2. **Focus the page**, ensure Reading or Live Preview mode, then screenshot to a path outside the vault:

   ```bash
   obsidian read path="wiki/<…>.md"
   obsidian dev:screenshot path="/tmp/diagram-check.png"
   ```

3. **Surface silent failures.** `obsidian dev:errors` shows parse failures that render as nothing rather than as an error box.

4. Read the PNG and clean up, exactly as in Method A.

> [!warning] The live vault is the main checkout, not your worktree
> Obsidian renders the main-checkout `wiki/` on its own branch, usually `main`. It does not see worktree edits, so Method B cannot render an unmerged worktree page. Use Method A there.
>
> **Never repoint the live vault at a branch.** One Obsidian instance serves every worktree, so repointing is a global mutex: it cross-contaminates parallel screenshots, and git refuses to check the same branch out twice. Last resort is a per-branch scratch note (`wiki/_diagcheck-<branch>.md`), screenshot, delete, and even that is not concurrency-safe.

---

## The failure Method A misses

Obsidian parses Mermaid label text as Markdown. A label that **begins** with `N.`, `N)`, `-`, `*` or `+` followed by a space renders as an `Unsupported markdown: list` error box in Obsidian, while `mmdc` renders it perfectly.

Verified: `A["1. First step"] --> B["2. Second step"]` renders as two clean labelled boxes under `mmdc` 11.15.0. Only an Obsidian render catches it. This is the single case where Method A gives a false pass, and the reason Method B still exists.

Fixes:

- **Numbered:** write `N —` instead of `N.`, for example `["4 — Agent"]`. An em dash inside a diagram label is house style.
- **Bullet or `+` where the marker is meaningful:** replace the trailing space with a non-breaking space (U+00A0). Visually identical, no longer parses as a list.
- A marker **mid-label**, after `<br/>` or inside `<b>…</b>`, is safe. Only the label start triggers it.

Detection sweep across the vault, then discard false positives:

```bash
rg -n '(\[\(?|\(\(?|\{\{?)"?([0-9]+[.)]|[-*+]) ' --glob '*.md' wiki/
```

See `wiki/artifacts/lessons/mermaid-label-list-marker-gotcha.md` for the full lesson.

---

## Output format in the vault

**PlantUML blocks render as SVG by default.** SVG scales cleanly and handles the dense labelling of an ArchiMate view better than a raster. Override per block with the fence language:

| Fence | Output |
|---|---|
| ` ```plantuml ` | SVG, the default |
| ` ```plantuml-png ` | PNG |
| ` ```plantuml-ascii ` | ASCII art |

Rendering runs against the local jar at `wiki/.obsidian/plantuml/plantuml.jar`: fast and offline. If local rendering fails, the plugin falls back to the public PlantUML server.

---

## When no renderer is available

Do a syntax self-check, then label the diagram **rendered-unverified** in the page. Say so in the reply too. An unverified diagram that says it is unverified is honest. An unverified diagram presented as done is the failure this whole section exists to prevent.

---

## Verified local toolchain

Checked on this machine, 2026-08-04. Re-check rather than trusting the list.

| Tool | Version | Path | Check command |
|---|---|---|---|
| `mmdc` (mermaid-cli) | 11.15.0 | `/opt/homebrew/bin/mmdc` | `mmdc --version` |
| `java` | OpenJDK 26.0.1 (Homebrew) | on PATH | `java -version` |
| `dot` (graphviz) | 15.0.0 | on PATH | `dot -V` |
| `plantuml.jar` | 1.2026.5, GPL, 29 524 499 bytes | `wiki/.obsidian/plantuml/plantuml.jar` | `java -jar <jar> --version` |
| `rsvg-convert` | 2.62.2 | `/opt/homebrew/bin/rsvg-convert` | `rsvg-convert --version` |
| `obsidian` CLI | present, `dev:screenshot` / `dev:errors` / `read` available | `/usr/local/bin/obsidian` | `pgrep -x Obsidian` |

The bundled Archimate-PlantUML stdlib inside that jar is version **3.2.2**. Macro coverage is in `archimate-hosiaisluoma.md`.

`java` and `dot` are the PlantUML prerequisites: `brew install openjdk graphviz`, plus the symlink documented in `wiki/.obsidian/plantuml/README.md`. Without `dot`, PlantUML renders sequence diagrams but fails on anything graphviz lays out, which is every ArchiMate view.
