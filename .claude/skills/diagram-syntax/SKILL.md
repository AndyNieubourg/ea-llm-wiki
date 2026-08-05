---
name: diagram-syntax
description: Write and debug diagrams in Mermaid, PlantUML, ArchiMate and C4. Use when authoring or fixing a diagram in a .mmd, .mermaid, .puml or .plantuml file or inside a fenced mermaid/plantuml block, when a diagram fails to render or shows an error box, when laying out a C4 or ArchiMate view, when edges cross badly, or when asked about node shapes, element and relationship macros, theming, or layout control. Do NOT use to decide whether a figure earns its place on a page, how many images a page should carry, where attachments are stored, or how images are embedded. That is diagram policy, it lives in the project CLAUDE.md, and this skill defers to it.
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
user-invocable: true
---

# Diagram syntax: draw it in the right notation, then prove it rendered

This skill owns two things: the syntax for each notation, and the rule that a diagram is not done until someone has looked at a render of it. It does not own whether a figure belongs on the page. That is policy, it lives in the project `CLAUDE.md`, and this skill defers to it.

**Dependencies.** Reads the diagram policy in the project `CLAUDE.md` (whether a figure earns its place, image counts, storage, embedding). Hands off to nothing. Loaded by any workflow that produces a figure.

## 1. Pick the notation by what you are drawing, not by element count

**This is the only routing table in the skill.** It restates the project `CLAUDE.md`, and `CLAUDE.md` wins if the two ever diverge. A second copy of this rule in a reference file is a bug, not a convenience.

| Drawing | Track | Start at |
|---|---|---|
| ArchiMate, any layer | PlantUML, Hosiaisluoma stdlib | [archimate-hosiaisluoma.md](references/archimate-hosiaisluoma.md) |
| C4 context, container, component, deployment | PlantUML, C4 stdlib | [plantuml/c4-plantuml.md](references/plantuml/c4-plantuml.md) |
| UML deployment, use case, and other notations Mermaid lacks | PlantUML | [plantuml/](references/plantuml/) |
| Flowchart, sequence, state, class, ER, gantt, mindmap, quadrant, xy, timeline, pie | Mermaid | [mermaid/](references/mermaid/) |
| Anything else, and anything where portability or later-session maintainability matters | Mermaid | [mermaid/](references/mermaid/) |

Notation decides the track. Element count is not a track rule: it measures how much layout work a diagram needs, not which tool draws it. A six-element ArchiMate view is still PlantUML, a forty-node flowchart is still Mermaid. Mermaid is the default because the source is the diagram: it diffs cleanly, renders natively in Obsidian with no plugin, and a later session can read and edit it.

Tracks 3 and 4 of the policy, designed SVG and committed raster, are not syntax and are not covered here. `CLAUDE.md` owns those.

Mermaid can draw C4-shaped diagrams and you will meet existing ones. Read them with [mermaid/c4.md](references/mermaid/c4.md); author new C4 in PlantUML.

## 2. Route to the reference

**Mermaid, per type.** [flowchart](references/mermaid/flowchart.md) · [sequenceDiagram](references/mermaid/sequenceDiagram.md) · [classDiagram](references/mermaid/classDiagram.md) · [stateDiagram](references/mermaid/stateDiagram.md) · [entityRelationshipDiagram](references/mermaid/entityRelationshipDiagram.md) · [gantt](references/mermaid/gantt.md) · [mindmap](references/mermaid/mindmap.md) · [timeline](references/mermaid/timeline.md) · [quadrantChart](references/mermaid/quadrantChart.md) · [xyChart](references/mermaid/xyChart.md) · [pie](references/mermaid/pie.md) · [c4](references/mermaid/c4.md)

**Mermaid, configuration.** [config-theming](references/mermaid/config-theming.md) · [config-directives](references/mermaid/config-directives.md) · [config-configuration](references/mermaid/config-configuration.md)

**PlantUML.** [c4-plantuml](references/plantuml/c4-plantuml.md) · [sequence](references/plantuml/sequence-diagrams.md) · [class](references/plantuml/class-diagrams.md) · [activity](references/plantuml/activity-diagrams.md) · [state](references/plantuml/state-diagrams.md) · [er](references/plantuml/er-diagrams.md) · [component](references/plantuml/component-diagrams.md) · [deployment](references/plantuml/deployment-diagrams.md) · [use case](references/plantuml/use-case-diagrams.md) · [styling](references/plantuml/styling-guide.md)

**ArchiMate.** [archimate-hosiaisluoma.md](references/archimate-hosiaisluoma.md), the element and relationship macros per layer with worked views.

**Layout and quality.** [c4-layout-science.md](references/c4-layout-science.md). Declaration order feeds the barycentric heuristic that Dagre uses to minimise edge crossings, so the order you write elements in changes the picture you get. Crossings are the strongest negative predictor of diagram comprehension (Purchase et al., 2002), which makes this the highest-leverage thing in the skill after correct syntax.

**When it will not render.** [mermaid-gotchas.md](references/mermaid-gotchas.md) for Mermaid, [plantuml/common-syntax-errors.md](references/plantuml/common-syntax-errors.md) for PlantUML.

**Three ArchiMate macros that read as plausible and do not exist.** `Rel_Used_By`, `Rel_Trigger` and `Data_Object` are all fatal parse errors: the diagram renders as an error image, not a degraded one. Write `Rel_Serving` (same direction), `Rel_Triggering` and `Application_DataObject`. The full table is in [archimate-hosiaisluoma.md](references/archimate-hosiaisluoma.md).

These reference files are material to read, not scripts to run. Do not `Bash`-execute anything from `references/`.

## 3. Verify the render. This step is not optional

A malformed block shows as an error box only at view time, and a text diff never catches it. So every diagram you author or materially edit gets rendered and looked at before you call it done.

Full procedure, both methods, in [rendering-and-verification.md](references/rendering-and-verification.md). The short form:

1. Write the block body to a temp path **outside** the vault.
2. Mermaid: `mmdc -i /tmp/diagram.mmd -o /tmp/diagram-check.png`. PlantUML: `java -jar <plantuml.jar> -tpng /tmp/diagram.puml`.
3. `Read` the PNG. Did it draw, or is there an error box?
4. Delete the temp files.

**Never claim a render you have not looked at.** If no renderer is available, say so and label the diagram *rendered-unverified*.

**The one failure a headless render misses.** Obsidian parses Mermaid label text as Markdown, so a label whose text *begins* with `1.`, `-`, `*` or `+` followed by a space renders as an "Unsupported markdown: list" error box. `mmdc` draws it cleanly and tells you nothing. Write `4 — Agent`, not `4. Agent`. Full rule and the detection grep in [mermaid-gotchas.md](references/mermaid-gotchas.md).

## 4. Before handing the diagram over

1. The notation matches what is being drawn, per section 1.
2. Elements are declared in layout order: actors, presentation, API, service, data, external.
3. Edge crossings are within target: zero for six elements or fewer, under three for seven to twelve, under five above that.
4. No Mermaid label starts with a list marker.
5. A render exists and you have read it.
6. The caption carries the message. A figure whose point survives only in the picture is a figure nobody can maintain.

## Provenance

The Mermaid per-type references are vendored from [tractorjuice/arc-kit](https://github.com/tractorjuice/arc-kit) (MIT), which autogenerated them from the mermaid.js.org documentation via `WH-2099/mermaid-skill`. Each file records its own provenance and should be refreshed from upstream rather than hand-edited. `c4-layout-science.md` is ArcKit's own work, adapted. The PlantUML references are ArcKit's, adapted from `SpillwaveSolutions/plantuml`, with remote includes replaced by the local stdlib form. The ArchiMate reference and the verification loop have no upstream: ArcKit ships neither, and both are written from this wiki's own conventions and its already-rendering diagrams.
